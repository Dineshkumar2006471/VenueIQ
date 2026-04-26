import os
import json
import datetime
import firebase_admin
from firebase_admin import firestore
from dotenv import load_dotenv

load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "kaggle-5b-478308").strip()

# Use Application Default Credentials
if not firebase_admin._apps:
    firebase_admin.initialize_app(options={"projectId": PROJECT_ID})
db = firestore.client()

def seed_all():
    """Seed all Firestore collections with realistic venue data."""
    
    print("--- Seeding VenueIQ Firestore database ---")
    
    # ─── Venue Zones (Food Courts + Facilities) ─────────
    zones = [
        {
            "zone_id": "adani_pavilion", "name": "Adani Pavilion — Premium Dining",
            "current_wait_mins": 5, "capacity": 100, "current_occupancy": 65,
            "status": "moderate", "zone_type": "food",
            "menu_items": ["Gourmet Gujarati Thali", "Pasta", "Premium Coffee", "Salads"],
            "pricing": "₹500–₹1200"
        },
        {
            "zone_id": "reliance_stand_food", "name": "Reliance Stand — Food Plaza",
            "current_wait_mins": 15, "capacity": 300, "current_occupancy": 280,
            "status": "very busy", "zone_type": "food",
            "menu_items": ["Dhokla", "Khandvi", "Pizza", "Cold Drinks", "Masala Chai"],
            "pricing": "₹150–₹400"
        },
        {
            "zone_id": "sabarmati_stand_concourse", "name": "Sabarmati Stand — Quick Bites",
            "current_wait_mins": 2, "capacity": 150, "current_occupancy": 30,
            "status": "quiet", "zone_type": "food",
            "menu_items": ["Popcorn", "Water", "Sandwiches", "Ice Cream"],
            "pricing": "₹100–₹300"
        },
        {
            "zone_id": "toilet_north", "name": "North Stand Restrooms (Gate 1)",
            "current_wait_mins": 8, "capacity": 30, "current_occupancy": 28,
            "status": "busy", "zone_type": "toilet"
        },
        {
            "zone_id": "toilet_south", "name": "South Stand Restrooms (Gate 4)",
            "current_wait_mins": 0, "capacity": 30, "current_occupancy": 5,
            "status": "quiet", "zone_type": "toilet"
        },
        {
            "zone_id": "medical_pavilion", "name": "Apollo Medical Post (Pavilion Level)",
            "current_wait_mins": 0, "capacity": 15, "current_occupancy": 1,
            "status": "available", "zone_type": "medical"
        },
        {
            "zone_id": "gt_merch", "name": "GT Official Store (Adani Pavilion)",
            "current_wait_mins": 10, "capacity": 60, "current_occupancy": 45,
            "status": "busy", "zone_type": "retail"
        }
    ]
    
    for zone in zones:
        zone["last_updated"] = datetime.datetime.utcnow()
        db.collection("venue_zones").document(zone["zone_id"]).set(zone)
    print(f"  [OK] {len(zones)} venue zones seeded")

    # ─── Crowd Data (Gates) ──────────────────────────────
    crowd = [
        {"gate": "Gate 1", "density": "high", "estimated_entry_mins": 8, 
         "alternative": "Gate 3 — only 2 min wait", "capacity": 500, "current_flow": 420},
        {"gate": "Gate 2", "density": "medium", "estimated_entry_mins": 4, 
         "alternative": "Gate 2 is manageable", "capacity": 400, "current_flow": 240},
        {"gate": "Gate 3", "density": "low", "estimated_entry_mins": 2, 
         "alternative": "Gate 3 is the best option right now!", "capacity": 400, "current_flow": 80},
        {"gate": "Gate 4 (VIP)", "density": "low", "estimated_entry_mins": 1, 
         "alternative": "VIP gate is nearly empty", "capacity": 200, "current_flow": 30},
    ]
    
    for c in crowd:
        c["timestamp"] = datetime.datetime.utcnow()
        db.collection("crowd_data").document(c["gate"].replace(" ", "_")).set(c)
    print(f"  [OK] {len(crowd)} gate records seeded")

    # ─── Navigation Data ─────────────────────────────────
    nav = [
        {"destination": "toilet_block_B", "from_stand": "Stand D", 
         "directions": "Turn left at Row 15, walk 40m, toilet block on right", "distance_meters": 45},
        {"destination": "food_court_B", "from_stand": "Stand A", 
         "directions": "Exit via Gate 2, turn left, Food Court B is 30m ahead", "distance_meters": 35},
        {"destination": "first_aid", "from_stand": "Stand C", 
         "directions": "Walk to Gate 2, ground level. Red Cross sign visible from 20m away", "distance_meters": 60},
        {"destination": "exit_gate_3", "from_stand": "Stand B", 
         "directions": "Follow green EXIT signs, down stairs at section 5, Gate 3 straight ahead", "distance_meters": 80},
        {"destination": "parking_P3", "from_stand": "Gate 3", 
         "directions": "Exit Gate 3, follow P signs, P3 is the furthest but has quickest highway access", "distance_meters": 200},
    ]
    
    for n in nav:
        n["last_updated"] = datetime.datetime.utcnow()
        db.collection("navigation").document(n["destination"]).set(n)
    print(f"  [OK] {len(nav)} navigation records seeded")

    # ─── Match Data ──────────────────────────────────────
    match_data = {
        "match_id": "IPL2026_M42",
        "match": "IPL 2026 — Match 42",
        "team1": {
            "name": "Gujarat Titans", "short": "GT",
            "score": "192/3", "overs": "19.1",
            "run_rate": "10.03",
            "top_scorer": "Shubman Gill — 84(48)"
        },
        "team2": {
            "name": "Royal Challengers Bengaluru", "short": "RCB",
            "score": "Yet to bat", "overs": "0.0",
            "run_rate": "0.00",
            "top_scorer": "—"
        },
        "status": "Live — GT batting, finishing strong in Ahmedabad!",
        "venue": "Narendra Modi Stadium, Ahmedabad",
        "toss": "RCB won toss, elected to bowl",
        "last_wicket": "Sai Sudharsan lbw b Siraj — 45(32)",
        "last_updated": datetime.datetime.utcnow().isoformat(),
        "innings_break_eta": "~10 minutes"
    }
    
    db.collection("match_data").document("current_match").set(match_data)
    print("  [OK] Match data seeded")

    # ─── Sample Incident Reports ─────────────────────────
    incidents = [
        {"type": "cleanliness", "location": "Toilet Block A", "description": "Water on floor near sinks",
         "status": "in_progress", "priority": "medium", "reported_at": datetime.datetime.utcnow()},
        {"type": "safety", "location": "Stand C Row 22", "description": "Broken handrail on stairs",
         "status": "open", "priority": "high", "reported_at": datetime.datetime.utcnow()},
        {"type": "maintenance", "location": "Food Court A", "description": "Display screen not working",
         "status": "resolved", "priority": "low", "reported_at": datetime.datetime.utcnow()},
    ]
    
    for i, inc in enumerate(incidents):
        db.collection("incident_reports").add(inc)
    print(f"  [OK] {len(incidents)} incident reports seeded")

    print("\nVenueIQ Firestore fully seeded! Ready to go.")


if __name__ == "__main__":
    seed_all()
