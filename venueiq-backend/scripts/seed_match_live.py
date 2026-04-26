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

def seed_match_live_data():
    print("Seeding match_live_data collection...")
    
    match_doc_id = "GT-vs-MI-IPL2025"
    match_data = {
        "match_id": match_doc_id,
        "tournament": "Indian Premier League 2025",
        "stadium": "Narendra Modi Stadium, Ahmedabad",
        "team_home": "Gujarat Titans",
        "team_away": "Mumbai Indians",
        "toss_winner": "Mumbai Indians",
        "toss_decision": "fielding",
        "current_phase": "innings_break",
        "current_innings": 1,
        "innings_1_batting_team": "Gujarat Titans",
        "innings_1_bowling_team": "Mumbai Indians",
        "innings_1_score": 187,
        "innings_1_wickets": 4,
        "innings_1_overs_completed": 20,
        "innings_1_overs_total": 20,
        "innings_1_run_rate": 9.35,
        "innings_2_target": 188,
        "innings_2_batting_team": "Mumbai Indians",
        "innings_2_bowling_team": "Gujarat Titans",
        "innings_2_score": 0,
        "innings_2_wickets": 0,
        "innings_2_overs_completed": 0,
        "innings_2_required_rate": 9.40,
        "current_batters": [
            {
                "name": "Shubman Gill",
                "runs": 72,
                "balls": 48,
                "fours": 6,
                "sixes": 4,
                "strike_rate": 150.0,
                "status": "not out"
            },
            {
                "name": "David Miller",
                "runs": 43,
                "balls": 29,
                "fours": 3,
                "sixes": 3,
                "strike_rate": 148.3,
                "status": "not out"
            }
        ],
        "top_scorer_innings_1": "Shubman Gill — 72 off 48 balls",
        "current_bowlers_innings_1": [
            {
                "name": "Jasprit Bumrah",
                "overs": 4,
                "runs": 28,
                "wickets": 2,
                "economy": 7.0
            },
            {
                "name": "Hardik Pandya",
                "overs": 3,
                "runs": 31,
                "wickets": 1,
                "economy": 10.3
            }
        ],
        "best_bowler_innings_1": "Jasprit Bumrah — 2 wickets for 28 runs",
        "key_moments": [
            "Over 6: Shubman Gill hits Bumrah for 2 sixes in one over",
            "Over 11: Sai Sudharsan out for 34, caught at mid-off",
            "Over 15: Miller joins Gill, partnership of 78 runs in 5 overs",
            "Over 19: Gill reaches fifty off 34 balls",
            "Over 20: GT finish on 187/4, strong total on this pitch"
        ],
        "pitch_condition": "Good batting surface. Dew expected in second innings which may help batters. Spinners struggled in first innings.",
        "weather": "Clear sky, 26 degrees Celsius, humidity 58 percent, light breeze from the west, no rain risk",
        "predicted_winner": "Gujarat Titans slightly favoured — 187 is above average at this ground",
        "average_first_innings_score_at_venue": 168,
        "highest_score_at_venue": 224,
        "venue_record_chasing_team_wins": "42 percent",
        "last_updated": firestore.SERVER_TIMESTAMP
    }

    db.collection("match_live_data").document(match_doc_id).set(match_data)
    print(f"Success: {match_doc_id} seeded in match_live_data.")

if __name__ == "__main__":
    seed_match_live_data()
