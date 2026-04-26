import os
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

def verify_seeding():
    print("\n--- VENUEIQ FIRESTORE VERIFICATION REPORT ---\n")
    
    collections = ['stadiums', 'venue_zones', 'crowd_data', 'navigation_routes', 'match_events']
    
    for coll in collections:
        docs = db.collection(coll).stream()
        count = sum(1 for _ in docs)
        print(f"[COLLECTION] {coll:20} | Found {count} documents")

    print("\n--- LIVE SYSTEM ANALYTICS ---\n")

    # 1. Quietest Food Courts
    print("QUIETEST FOOD COURTS (Wait < 5 mins):")
    # Fetch all food zones and filter in memory to avoid index requirements
    food_ref = db.collection('venue_zones').where('type', '==', 'food').stream()
    
    found_quiet = False
    for doc in food_ref:
        data = doc.to_dict()
        if data.get('wait_minutes', 0) < 5:
            name = data.get('display_name', data.get('name', 'Unknown'))
            zone = data.get('zone', 'N/A')
            wait = data.get('wait_minutes', 0)
            status = data.get('status', 'unknown')
            print(f" - {name} | Zone: {zone} | Wait: {wait}m | Status: {status}")
            found_quiet = True
    if not found_quiet:
        print(" - No quiet food courts found. Venue is currently peak busy.")

    # 2. Gate Congestion Status
    print("\nGATE CONGESTION STATUS:")
    gates_ref = db.collection('crowd_data').order_by('gate_number').stream()
    for doc in gates_ref:
        data = doc.to_dict()
        status_icon = "GO" if data.get('current_status') == 'clear' else "SLOW" if data.get('current_status') == 'congested' else "STOP"
        name = data.get('display_name', f"Gate {data.get('gate_number')}")
        wait = data.get('entry_wait_minutes', 0)
        density = data.get('density', 'unknown')
        print(f" [{status_icon}] {name:12} | Entry Wait: {wait:2}m | Density: {density}")

    # 3. Match Context
    print("\nMATCH CONTEXT:")
    stadium_doc = db.collection('stadiums').document('narendra_modi_stadium').get()
    if stadium_doc.exists:
        data = stadium_doc.to_dict()
        match = data.get('current_match')
        if match:
            print(f" Event: {match.get('event_name')}")
            print(f" Teams: {match.get('teams')}")
            print(f" Match ID: {match.get('match_id')}")
        else:
            print(" No active match data found in stadium document.")
    else:
        print(" Stadium document not found.")

    print("\n--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    verify_seeding()
