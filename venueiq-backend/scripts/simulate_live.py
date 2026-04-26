import os
import time
import random
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase Admin SDK
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', './serviceAccount.json')

if os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
else:
    # Fallback to ADC
    firebase_admin.initialize_app(options={'projectId': project_id})

db = firestore.client()

def update_live_data():
    while True:
        try:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Updating live metrics...")
            
            # 1. Update Food and Toilets in venue_zones
            zones_ref = db.collection('venue_zones').where('type', 'in', ['food', 'toilet']).stream()
            batch = db.batch()
            updated_count = 0
            
            for doc in zones_ref:
                data = doc.to_dict()
                cap = data.get('capacity', data.get('total_stalls', 100))
                occ_key = 'current_occupancy' if data['type'] == 'food' else 'occupied_stalls'
                curr_occ = data.get(occ_key, 0)
                
                # Random shift -12 to +12
                shift = random.randint(-12, 12)
                new_occ = max(0, min(cap, curr_occ + shift))
                
                # Calculate wait and status
                occ_pct = (new_occ / cap) * 100
                if occ_pct < 40:
                    wait = random.randint(0, 2)
                    status = "quiet"
                elif occ_pct <= 65:
                    wait = random.randint(3, 6)
                    status = "busy"
                elif occ_pct <= 85:
                    wait = random.randint(7, 11)
                    status = "packed"
                else:
                    wait = random.randint(12, 18)
                    status = "packed"
                
                batch.update(doc.reference, {
                    occ_key: new_occ,
                    "wait_minutes": wait,
                    "status": status,
                    "last_updated": firestore.SERVER_TIMESTAMP
                })
                updated_count += 1
            
            batch.commit()

            # 2. Update Gate Crowd Data
            gates_ref = db.collection('crowd_data').stream()
            batch = db.batch()
            
            for doc in gates_ref:
                data = doc.to_dict()
                if data.get('is_vip_only'):
                    continue
                
                # Robustness check: Skip legacy or malformed docs
                if 'gate_number' not in data or 'display_name' not in data:
                    continue
                
                curr_wait = data.get('entry_wait_minutes', 5)
                new_wait = max(0, min(15, curr_wait + random.randint(-2, 2)))
                
                # Recalculate density
                if new_wait <= 3:
                    density = "low"
                    status = "clear"
                elif new_wait <= 6:
                    density = "medium"
                    status = "clear"
                elif new_wait <= 10:
                    density = "high"
                    status = "congested"
                else:
                    density = "critical"
                    status = "critical"
                
                update_payload = {
                    "entry_wait_minutes": new_wait,
                    "exit_wait_minutes": max(0, min(20, data.get('exit_wait_minutes', 5) + random.randint(-1, 2))),
                    "density": density,
                    "current_status": status,
                    "last_updated": firestore.SERVER_TIMESTAMP
                }
                
                # Dynamic recommendation if status changes to congested
                if status in ["congested", "critical"]:
                    # Simple heuristic: suggest even/odd adjacent gate
                    suggest = (data['gate_number'] % 11) + 1
                    update_payload["recommendation_text"] = f"{data['display_name']} is {status}. Please consider using Gate {suggest} which has a lower density."
                else:
                    update_payload["recommendation_text"] = f"{data['display_name']} is clear right now. Entry is smooth."

                batch.update(doc.reference, update_payload)
                updated_count += 1

            batch.commit()

            # 3. Update Match Data (GT vs MI IPL 2025)
            match_ref = db.collection('match_live_data').document('GT-vs-MI-IPL2025')
            match_doc = match_ref.get()
            if match_doc.exists:
                m = match_doc.to_dict()
                
                # If innings break, start the 2nd innings
                if m.get('current_phase') == 'innings_break':
                    m['current_phase'] = 'live'
                    m['current_innings'] = 2
                    m['innings_2_overs_completed'] = 0
                    m['innings_2_score'] = 0
                    m['innings_2_wickets'] = 0
                    m['innings_2_run_rate'] = 0
                    m['current_batters'] = [
                        {
                            "name": "Rohit Sharma",
                            "runs": 0,
                            "balls": 0,
                            "fours": 0,
                            "sixes": 0,
                            "strike_rate": 0,
                            "status": "not out"
                        },
                        {
                            "name": "Ishan Kishan",
                            "runs": 0,
                            "balls": 0,
                            "fours": 0,
                            "sixes": 0,
                            "strike_rate": 0,
                            "status": "not out"
                        }
                    ]
                    print("--- 2nd Innings Started: Mumbai Indians Batting ---")

                if m.get('current_phase') == 'live' and m.get('current_innings') == 2:
                    # Simulate 1 ball every 30s
                    balls_added = 1
                    # 8-14 runs/over target -> ~1.3 to 2.3 runs per ball average.
                    # We'll use 0-6 runs for a single ball.
                    runs_added = random.choice([0, 1, 1, 2, 4, 6]) 
                    
                    curr_overs = m.get('innings_2_overs_completed', 0)
                    whole = int(curr_overs)
                    balls = int(round((curr_overs - whole) * 10))
                    
                    balls += balls_added
                    if balls >= 6:
                        whole += 1
                        balls = 0
                    
                    new_overs = float(f"{whole}.{balls}")
                    
                    if whole >= 20 or m['innings_2_score'] + runs_added >= m['innings_2_target']:
                        m['current_phase'] = 'finished'
                        m['innings_2_score'] += runs_added
                        print(f"--- Match Finished! Final Score: {m['innings_2_score']}/{m['innings_2_wickets']} ---")
                    else:
                        m['innings_2_overs_completed'] = new_overs
                        m['innings_2_score'] += runs_added
                        
                        # Recalculate Run Rate
                        total_balls = (whole * 6) + balls
                        if total_balls > 0:
                            m['innings_2_run_rate'] = round((m['innings_2_score'] / (total_balls / 6.0)), 2)
                        
                        # Recalculate Required Rate
                        balls_left = (20 * 6) - total_balls
                        runs_needed = m['innings_2_target'] - m['innings_2_score']
                        if balls_left > 0:
                            m['innings_2_required_rate'] = round((runs_needed / (balls_left / 6.0)), 2)
                        else:
                            m['innings_2_required_rate'] = 0
                            
                        # Update current batter (batter 1)
                        if m.get('current_batters') and len(m['current_batters']) > 0:
                            m['current_batters'][0]['runs'] += runs_added
                            m['current_batters'][0]['balls'] += balls_added
                            m['current_batters'][0]['strike_rate'] = round((m['current_batters'][0]['runs'] / m['current_batters'][0]['balls']) * 100, 2)

                        print(f"Match Update: {m['innings_2_batting_team']} {m['innings_2_score']}/{m['innings_2_wickets']} ({new_overs} ov). Target: {m['innings_2_target']}")

                match_ref.set(m)
                updated_count += 1

            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Success: Updated {updated_count} documents.")

        except Exception as e:
            print(f"Error in simulation loop: {e}")
            
        time.sleep(30)

if __name__ == "__main__":
    update_live_data()
