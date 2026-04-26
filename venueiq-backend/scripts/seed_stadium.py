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

def seed_stadiums():
    print("Seeding stadiums collection...")
    batch = db.batch()
    stadium_ref = db.collection('stadiums').document('narendra_modi_stadium')
    stadium_data = {
        "name": "Narendra Modi Stadium",
        "city": "Ahmedabad",
        "state": "Gujarat",
        "country": "India",
        "capacity": 132000,
        "current_attendance": 84000,
        "total_gates": 11,
        "vip_gates": ["Gate 7"],
        "total_stands": 8,
        "total_levels": 3,
        "coordinates": {"lat": 23.0902, "lng": 72.5952},
        "active_match": "Gujarat Titans vs Mumbai Indians",
        "match_phase": "innings_break",
        "match_date": "2025-04-20",
        "facilities": {
            "food_courts": 18,
            "toilet_blocks": 22,
            "medical_rooms": 3,
            "atm_counters": 8,
            "merchandise_stores": 6
        },
        "qr_code_url": "https://venueiq.app/narendra-modi-stadium"
    }
    batch.set(stadium_ref, stadium_data)
    batch.commit()
    print("Success: stadiums collection seeded.")

def seed_venue_zones():
    print("Seeding venue_zones collection...")
    
    # Food Courts
    food_courts = [
        {"id": "FC-01", "name": "Food Court — Gate 1 North", "stand": "Adani Stand", "level": "Ground Level", "gate_nearest": "Gate 1", "coord": "30m east of Gate 1 turnstile, follow yellow food signs", "cap": 320, "occ": 289, "wait": 13, "status": "packed", "menu": ["Veg Biryani", "Paneer Roll", "Cold Drink", "Popcorn", "Ice Cream"], "price": "₹80 - ₹350"},
        {"id": "FC-02", "name": "Food Court — Gate 2 South", "stand": "Adani Stand", "level": "Ground Level", "gate_nearest": "Gate 2", "coord": "20m west of Gate 2 exit, on your left after turnstile", "cap": 280, "occ": 74, "wait": 3, "status": "quiet", "menu": ["Masala Dosa", "Sandwich", "Chai", "Lassi", "Bhel Puri"], "price": "₹60 - ₹280"},
        {"id": "FC-03", "name": "Food Court — Gate 3 East", "stand": "Reliance Stand", "level": "Ground Level", "gate_nearest": "Gate 3", "coord": "Inside Gate 3, straight ahead 25m, court on your right", "cap": 300, "occ": 271, "wait": 15, "status": "packed", "menu": ["Chole Bhature", "Pizza Slice", "Burger", "Fruit Juice", "Nachos"], "price": "₹90 - ₹400"},
        {"id": "FC-04", "name": "Food Court — Gate 4 Upper", "stand": "Campa Stand", "level": "First Floor", "gate_nearest": "Gate 4", "coord": "Take escalator at Gate 4 to First Floor, food court is immediately right", "cap": 260, "occ": 68, "wait": 2, "status": "quiet", "menu": ["Pav Bhaji", "Idli Sambhar", "Cold Coffee", "Dhokla", "Falooda"], "price": "₹70 - ₹300"},
        {"id": "FC-05", "name": "Food Court — Gate 5 Central", "stand": "SBI Stand", "level": "Ground Level", "gate_nearest": "Gate 5", "coord": "Central concourse between Gate 5 and Gate 6, follow orange signs", "cap": 350, "occ": 198, "wait": 7, "status": "busy", "menu": ["Biryani", "Tandoori Chicken", "Soft Drink", "Kulfi", "Samosa"], "price": "₹100 - ₹450"},
        {"id": "FC-06", "name": "Food Court — Gate 6 South", "stand": "ONGC Stand", "level": "Ground Level", "gate_nearest": "Gate 6", "coord": "Left side of Gate 6 lobby, 15m from security check", "cap": 290, "occ": 261, "wait": 12, "status": "packed", "menu": ["Dal Baati", "Gujarati Thali", "Buttermilk", "Ice Cream", "Pakora"], "price": "₹80 - ₹380"},
        {"id": "FC-07", "name": "Premium Food Lounge — VIP Level", "stand": "ONGC Stand", "level": "Upper Tier", "gate_nearest": "Gate 7", "coord": "VIP access only via Gate 7, elevator to Upper Tier, lounge on left", "cap": 120, "occ": 45, "wait": 0, "status": "quiet", "menu": ["Continental Buffet", "Fresh Juice Bar", "Dessert Counter", "Coffee Station", "Snack Bar"], "price": "₹500 - ₹2000"},
        {"id": "FC-08", "name": "Food Court — Gate 8 West", "stand": "BPCL Stand", "level": "Ground Level", "gate_nearest": "Gate 8", "coord": "Right of Gate 8 after entering, large yellow food sign overhead", "cap": 310, "occ": 88, "wait": 4, "status": "quiet", "menu": ["Rajma Chawal", "Noodles", "Cold Drink", "Bhel", "Vada Pav"], "price": "₹70 - ₹320"},
        {"id": "FC-09", "name": "Food Court — Gate 9 Corner", "stand": "BPCL Stand", "level": "Ground Level", "gate_nearest": "Gate 9", "coord": "Corner junction between Gate 9 and Gate 10 corridor, 40m walk", "cap": 270, "occ": 243, "wait": 11, "status": "packed", "menu": ["Frankie Roll", "Pani Puri", "Sugarcane Juice", "Popcorn", "Maggi"], "price": "₹60 - ₹290"},
        {"id": "FC-10", "name": "Food Court — Gate 10 South", "stand": "Tata Stand", "level": "Ground Level", "gate_nearest": "Gate 10", "coord": "Directly inside Gate 10 entrance, cannot miss it", "cap": 300, "occ": 112, "wait": 5, "status": "busy", "menu": ["Dahi Puri", "Spring Roll", "Lemonade", "Chaat", "Sandwich"], "price": "₹80 - ₹350"},
        {"id": "FC-11", "name": "Food Court — Gate 11 West", "stand": "IndusInd Stand", "level": "Ground Level", "gate_nearest": "Gate 11", "coord": "20m south of Gate 11, blue food sign on wall", "cap": 285, "occ": 71, "wait": 3, "status": "quiet", "menu": ["Aloo Paratha", "Curd Rice", "Chai", "Banana Chips", "Nimbu Pani"], "price": "₹65 - ₹270"},
        {"id": "FC-12", "name": "Upper Tier Food Kiosk — Adani Stand", "stand": "Adani Stand", "level": "Upper Tier", "gate_nearest": "Gate 1", "coord": "Upper Tier concourse Row 45 level, central position", "cap": 180, "occ": 156, "wait": 9, "status": "busy", "menu": ["Popcorn", "Cold Drink", "Chips", "Chocolate Bar", "Water"], "price": "₹50 - ₹200"},
        {"id": "FC-13", "name": "Upper Tier Food Kiosk — SBI Stand", "stand": "SBI Stand", "level": "Upper Tier", "gate_nearest": "Gate 5", "coord": "Upper Tier, near Row 50 stairwell, east side", "cap": 160, "occ": 44, "wait": 2, "status": "quiet", "menu": ["Popcorn", "Cold Drink", "Biscuits", "Energy Drink", "Water"], "price": "₹50 - ₹180"},
        {"id": "FC-14", "name": "Upper Tier Food Kiosk — Tata Stand", "stand": "Tata Stand", "level": "Upper Tier", "gate_nearest": "Gate 10", "coord": "Upper Tier south concourse, Row 48 level", "cap": 170, "occ": 148, "wait": 10, "status": "packed", "menu": ["Popcorn", "Soft Drink", "Sandwich", "Chips", "Ice Cream"], "price": "₹60 - ₹220"},
        {"id": "FC-15", "name": "North Concourse Street Food Row", "stand": "Reliance Stand", "level": "Ground Level", "gate_nearest": "Gate 3", "coord": "North concourse between Gate 2 and Gate 3, 6 stalls in a row", "cap": 240, "occ": 67, "wait": 4, "status": "quiet", "menu": ["Pav Bhaji", "Corn Cup", "Juice", "Momos", "Sandwich"], "price": "₹50 - ₹250"},
        {"id": "FC-16", "name": "East Concourse Food Zone", "stand": "SBI Stand", "level": "First Floor", "gate_nearest": "Gate 5", "coord": "First Floor east concourse, 35m from Gate 5 stairwell", "cap": 220, "occ": 196, "wait": 12, "status": "packed", "menu": ["Biryani", "Dosa", "Cold Drink", "Kulfi", "Samosa"], "price": "₹80 - ₹360"},
        {"id": "FC-17", "name": "West Wing Snack Bar", "stand": "IndusInd Stand", "level": "First Floor", "gate_nearest": "Gate 11", "coord": "First Floor west wing, near media entrance corridor", "cap": 190, "occ": 55, "wait": 3, "status": "quiet", "menu": ["Vada Pav", "Chai", "Biscuits", "Chips", "Cold Drink"], "price": "₹40 - ₹200"},
        {"id": "FC-18", "name": "South End Premium Kiosk", "stand": "BPCL Stand", "level": "Ground Level", "gate_nearest": "Gate 8", "coord": "South end corridor between Gate 8 and Gate 9, premium blue kiosk", "cap": 150, "occ": 49, "wait": 2, "status": "quiet", "menu": ["Fresh Juice", "Protein Bar", "Salad Bowl", "Coffee", "Smoothie"], "price": "₹150 - ₹500"}
    ]

    batch = db.batch()
    for fc in food_courts:
        ref = db.collection('venue_zones').document(fc['id'])
        batch.set(ref, {
            "zone_id": fc['id'],
            "type": "food",
            "name": fc['name'],
            "stand": fc['stand'],
            "level": fc['level'],
            "gate_nearest": fc['gate_nearest'],
            "coordinates_text": fc['coord'],
            "capacity": fc['cap'],
            "current_occupancy": fc['occ'],
            "wait_minutes": fc['wait'],
            "status": fc['status'],
            "menu_items": fc['menu'],
            "price_range": fc['price'],
            "accepts_upi": True,
            "last_updated": firestore.SERVER_TIMESTAMP
        })
    batch.commit()

    # Toilet Blocks
    stands = [
        ("Adani Stand", ["Ground Level", "First Floor", "Upper Tier"]),
        ("Reliance Stand", ["Ground Level", "Upper Tier"]),
        ("Campa Stand", ["Ground Level", "Upper Tier"]),
        ("SBI Stand", ["Ground Level", "First Floor", "Upper Tier"]),
        ("ONGC Stand", ["Ground Level", "Upper Tier"]),
        ("BPCL Stand", ["Ground Level", "First Floor", "Upper Tier"]),
        ("Tata Stand", ["Ground Level", "Upper Tier"]),
        ("IndusInd Stand", ["Ground Level", "Upper Tier"])
    ]
    
    toilet_data = []
    ids = [f"TB-{str(i).zfill(2)}" for i in range(1, 23)]
    
    # 10 quiet, 8 busy, 4 packed
    statuses = ["quiet"]*10 + ["busy"]*8 + ["packed"]*4
    import random
    random.shuffle(statuses)

    idx = 0
    for stand, levels in stands:
        for level in levels:
            if idx >= 22: break
            
            gate = "Gate 1"
            if "Reliance" in stand: gate = "Gate 3"
            elif "Campa" in stand: gate = "Gate 4"
            elif "SBI" in stand: gate = "Gate 5"
            elif "ONGC" in stand: gate = "Gate 6"
            elif "BPCL" in stand: gate = "Gate 8"
            elif "Tata" in stand: gate = "Gate 10"
            elif "IndusInd" in stand: gate = "Gate 11"
            
            total = random.randint(28, 64)
            status = statuses[idx]
            
            if status == "quiet":
                occ = random.randint(5, int(total * 0.39))
                wait = random.randint(0, 2)
            elif status == "busy":
                occ = random.randint(int(total * 0.4), int(total * 0.65))
                wait = random.randint(3, 5)
            else:
                occ = random.randint(int(total * 0.66), total)
                wait = random.randint(6, 8)

            toilet_data.append({
                "zone_id": ids[idx],
                "type": "toilet",
                "name": f"Toilet Block {chr(65+idx)} — {stand} {level}",
                "stand": stand,
                "level": level,
                "gate_nearest": gate,
                "coordinates_text": f"Located in {stand} on {level}, follow the blue WC signs from the {gate} side.",
                "total_stalls": total,
                "occupied_stalls": occ,
                "wait_minutes": wait,
                "status": status,
                "gender_split": {"male": total // 2, "female": total - (total // 2)},
                "last_updated": firestore.SERVER_TIMESTAMP
            })
            idx += 1

    batch = db.batch()
    for tb in toilet_data:
        ref = db.collection('venue_zones').document(tb['zone_id'])
        batch.set(ref, tb)
    batch.commit()

    # Medical Rooms
    medical_rooms = [
        {
            "zone_id": "MED-01", "type": "medical", "name": "Primary Medical Centre", "stand": "Adani Stand", 
            "level": "Ground Level", "gate_nearest": "Gate 2", "coordinates_text": "Follow red cross signs from Gate 2, medical room is 25m straight, white door on left", 
            "is_primary": True, "staff_count": 6, "wait_minutes": 0, "status": "open", 
            "services": ["First Aid", "Defibrillator", "Stretcher", "Oxygen", "Basic Medication"], "open_24h": True
        },
        {
            "zone_id": "MED-02", "type": "medical", "name": "First Aid Post — South End", "stand": "BPCL Stand", 
            "level": "Ground Level", "gate_nearest": "Gate 8", "coordinates_text": "Right of Gate 8 security, first aid post behind the blue screen", 
            "is_primary": False, "staff_count": 3, "wait_minutes": 0, "status": "open", 
            "services": ["First Aid", "Basic Medication", "Stretcher"], "open_24h": True
        },
        {
            "zone_id": "MED-03", "type": "medical", "name": "Upper Tier Medical Point", "stand": "SBI Stand", 
            "level": "Upper Tier", "gate_nearest": "Gate 5", "coordinates_text": "Upper Tier Row 55 level, look for red cross sign near stairwell C", 
            "is_primary": False, "staff_count": 2, "wait_minutes": 0, "status": "open", 
            "services": ["First Aid", "Basic Medication"], "open_24h": True
        }
    ]
    
    batch = db.batch()
    for med in medical_rooms:
        ref = db.collection('venue_zones').document(med['zone_id'])
        med['last_updated'] = firestore.SERVER_TIMESTAMP
        batch.set(ref, med)
    batch.commit()
    print("Success: venue_zones collection seeded.")

def seed_crowd_data():
    print("Seeding crowd_data collection...")
    gates = [
        {"id": "Gate-1", "num": 1, "name": "Gate 1", "compass": "North-West", "stand": "Adani Stand", "density": "high", "entry": 9, "exit": 14, "staff": 12, "vip": False, "status": "congested", "rec": "Very busy. Use Gate 2 instead — 3 minute wait and serves the same Adani Stand."},
        {"id": "Gate-2", "num": 2, "name": "Gate 2", "compass": "North-West", "stand": "Adani Stand", "density": "low", "entry": 3, "exit": 4, "staff": 8, "vip": False, "status": "clear", "rec": "Gate 2 is clear right now. Best entry for Adani Stand."},
        {"id": "Gate-3", "num": 3, "name": "Gate 3", "compass": "North", "stand": "Reliance Stand", "density": "medium", "entry": 6, "exit": 8, "staff": 10, "vip": False, "status": "clear", "rec": "Moderate wait. If you are near Gate 4 consider using that instead."},
        {"id": "Gate-4", "num": 4, "name": "Gate 4", "compass": "North-East", "stand": "Campa Stand", "density": "low", "entry": 2, "exit": 3, "staff": 8, "vip": False, "status": "clear", "rec": "Gate 4 is very clear. Fastest entry on the north-east side."},
        {"id": "Gate-5", "num": 5, "name": "Gate 5", "compass": "East", "stand": "SBI Stand", "density": "high", "entry": 8, "exit": 11, "staff": 14, "vip": False, "status": "congested", "rec": "SBI Stand entry is congested. Try Gate 6 for a shorter queue."},
        {"id": "Gate-6", "num": 6, "name": "Gate 6", "compass": "South-East", "stand": "ONGC Stand", "density": "medium", "entry": 5, "exit": 6, "staff": 9, "vip": False, "status": "clear", "rec": "Gate 6 is manageable. ONGC Stand access is smooth here."},
        {"id": "Gate-7", "num": 7, "name": "Gate 7", "compass": "South-East", "stand": "VIP/Media", "density": "low", "entry": 0, "exit": 0, "staff": 6, "vip": True, "status": "clear", "rec": "VIP and media access only. General public must use adjacent gates."},
        {"id": "Gate-8", "num": 8, "name": "Gate 8", "compass": "South", "stand": "BPCL Stand", "density": "low", "entry": 3, "exit": 4, "staff": 8, "vip": False, "status": "clear", "rec": "Gate 8 is clear. Good option for BPCL Stand access."},
        {"id": "Gate-9", "num": 9, "name": "Gate 9", "compass": "South", "stand": "BPCL Stand", "density": "high", "entry": 10, "exit": 13, "staff": 15, "vip": False, "status": "congested", "rec": "Very congested. Use Gate 8 or Gate 10 instead."},
        {"id": "Gate-10", "num": 10, "name": "Gate 10", "compass": "South-West", "stand": "Tata Stand", "density": "medium", "entry": 5, "exit": 7, "staff": 11, "vip": False, "status": "clear", "rec": "Tata Stand access is moderate. Manageable wait."},
        {"id": "Gate-11", "num": 11, "name": "Gate 11", "compass": "West", "stand": "IndusInd Stand", "density": "low", "entry": 2, "exit": 3, "staff": 7, "vip": False, "status": "clear", "rec": "Gate 11 is nearly empty. Fastest exit on the west side right now."}
    ]
    
    batch = db.batch()
    for gate in gates:
        ref = db.collection('crowd_data').document(gate['id'])
        batch.set(ref, {
            "gate_id": gate['id'],
            "gate_number": gate['num'],
            "display_name": gate['name'],
            "position_compass": gate['compass'],
            "stand_served": gate['stand'],
            "density": gate['density'],
            "entry_wait_minutes": gate['entry'],
            "exit_wait_minutes": gate['exit'],
            "staff_deployed": gate['staff'],
            "is_vip_only": gate['vip'],
            "current_status": gate['status'],
            "recommendation_text": gate['rec'],
            "last_updated": firestore.SERVER_TIMESTAMP
        })
    batch.commit()
    print("Success: crowd_data collection seeded.")

def seed_navigation_routes():
    print("Seeding navigation_routes collection...")
    routes = [
        {"id": "R-01", "from": "Adani Stand — Any Row", "to": "Food Court FC-02 (Gate 2)", "dist": 180, "time": 3, "levels": [], "steps": ["Face away from the pitch towards the outer concourse wall.", "Walk towards the Gate 2 exit signs, following the white concourse corridor.", "After passing the security re-entry desk, the food court is on your left — look for the yellow overhead sign.", "Queue from the left side of the counter for faster service."], "tip": "FC-02 is the quietest food court for Adani Stand right now — only 3 minute wait."},
        {"id": "R-02", "from": "Reliance Stand — Any Row", "to": "Food Court FC-15 (North Concourse)", "dist": 210, "time": 4, "levels": [], "steps": ["Exit your row towards the outer concourse via the nearest aisle.", "Turn left on the concourse and walk north towards Gate 3.", "The Street Food Row is a line of 6 stalls along the north concourse wall between Gate 2 and Gate 3.", "Choose any stall — all serve different items."], "tip": "Street food here is faster than the main food courts and less crowded."},
        {"id": "R-03", "from": "Campa Stand — Any Row", "to": "Food Court FC-04 (Gate 4 First Floor)", "dist": 150, "time": 3, "levels": ["First Floor"], "steps": ["Walk to the outer concourse aisle nearest Gate 4.", "Look for the escalator marked First Floor — it is next to the Gate 4 lobby.", "Take the escalator up one level.", "Food Court FC-04 is immediately on your right at the top."], "tip": "The First Floor court is far less crowded than Ground Level because most people do not notice the escalator."},
        {"id": "R-04", "from": "SBI Stand — Ground Level", "to": "Nearest Quiet Toilet", "dist": 90, "time": 2, "levels": [], "steps": ["Walk towards the outer wall of the SBI Stand concourse.", "Turn right towards Gate 5 stairwell area.", "Toilet Block TB-09 is on your left behind the stairwell column — marked with a blue WC sign.", "Use the left entrance for shorter queue."], "tip": "TB-09 is the quietest toilet near SBI Stand right now. Avoid TB-08 near Gate 5 main lobby — it is busy."},
        {"id": "R-05", "from": "ONGC Stand — Any Level", "to": "Primary Medical Centre (MED-01)", "dist": 380, "time": 6, "levels": [], "steps": ["Exit ONGC Stand towards the outer concourse.", "Walk north along the concourse in the direction of Gate 3 and Gate 2.", "Follow the red cross signs that appear every 30 metres on the concourse wall.", "Continue past Gate 3 and into the Adani Stand concourse.", "The medical room is 25 metres straight ahead — white door on your left."], "tip": "If this is an emergency, flag any yellow jacket steward on the concourse immediately. They have direct radio to the medical team."},
        {"id": "R-06", "from": "BPCL Stand — Any Row", "to": "Gate 8 Exit", "dist": 220, "time": 4, "levels": [], "steps": ["Face the outer concourse and walk south.", "Follow the green EXIT signs on the concourse ceiling.", "Pass the Food Court FC-08 on your right without stopping.", "Gate 8 turnstiles are at the end of this corridor — staff will direct you through."], "tip": "Gate 8 exit is currently very clear with only 4 minute wait. Use it over Gate 9 which is congested."},
        {"id": "R-07", "from": "Tata Stand — Upper Tier", "to": "Gate 10 Ground Level Exit", "dist": 320, "time": 7, "levels": ["Ground Level"], "steps": ["From Upper Tier Row 50 and above, locate stairwell B or D on either side of your section.", "Walk down two flights of stairs to Ground Level — do not take the escalator as it runs upward only during match hours.", "At Ground Level turn left and follow the EXIT signs along the south concourse.", "Gate 10 turnstiles are at the end of the south concourse.", "Show your ticket stub to exit staff."], "tip": "Leave during the 19th over to avoid the post-match rush through Gate 10. Current wait is 7 minutes and will rise to 20 minutes at match end."},
        {"id": "R-08", "from": "IndusInd Stand — Any Row", "to": "Food Court FC-11 (Gate 11)", "dist": 160, "time": 3, "levels": [], "steps": ["Walk to the outer concourse from your seat row.", "Turn south towards Gate 11.", "Food Court FC-11 is 20 metres south of Gate 11 — look for the blue food sign on the wall.", "The queue forms from the right side."], "tip": "FC-11 is very quiet right now at 3 minute wait. IndusInd Stand is lucky tonight."},
        {"id": "R-09", "from": "Any Stand — Upper Tier", "to": "Nearest ATM", "dist": 280, "time": 5, "levels": ["Ground Level"], "steps": ["From Upper Tier, descend to Ground Level via any stairwell.", "All ATMs are located at Ground Level only.", "Walk towards the nearest main gate lobby — Gate 2, Gate 5, Gate 8, or Gate 10.", "The ATM counter is inside the gate lobby area, usually on the right side as you face the exit.", "There are 2 ATMs per main gate lobby."], "tip": "All major banks are represented. UPI is accepted at all food courts so an ATM is only needed for cash stalls."},
        {"id": "R-10", "from": "Gate 1 Entrance", "to": "Adani Stand — Any Row", "dist": 200, "time": 4, "levels": [], "steps": ["After passing Gate 1 security and turnstile, walk straight ahead into the Adani Stand concourse.", "Your row is determined by your ticket — check the section letter and row number printed on it.", "Sections A through D are to your left, sections E through H are to your right.", "Find your section letter sign on the concourse wall and enter through that aisle."], "tip": "Row numbers increase as you go higher. Rows 1 to 20 are Ground Level, 21 to 40 are First Floor, 41 and above are Upper Tier."},
        {"id": "R-11", "from": "Food Court FC-02", "to": "Adani Stand — Row 15 to Row 25", "dist": 170, "time": 3, "levels": [], "steps": ["Exit Food Court FC-02 from the right side.", "Turn right back towards Gate 2 re-entry.", "Show your ticket stub to the re-entry staff at Gate 2.", "Once inside walk straight ahead to the Adani Stand concourse.", "Your First Floor rows 21 to 40 are up the stairwell on your left.", "Row 15 to 20 are at the far end of Ground Level concourse on your right."], "tip": "Always keep your ticket stub for re-entry. Security checks stub at re-entry, not the QR code."},
        {"id": "R-12", "from": "Any Location", "to": "Merchandise Store", "dist": 0, "time": 0, "levels": [], "steps": ["Merchandise stores are located at 6 points around the stadium.", "Nearest stores are at Gate 2 lobby (Adani Stand side), Gate 5 lobby (SBI Stand side), Gate 8 lobby (BPCL Stand side), and Gate 10 lobby (Tata Stand side).", "Walk to your nearest gate lobby and look for the orange merchandise signage.", "Stores close 30 minutes after match ends.", "Buy before the last 5 overs if possible."], "tip": "Stores close 30 minutes after match ends. Buy before the last 5 overs if possible."}
    ]
    
    batch = db.batch()
    for route in routes:
        ref = db.collection('navigation_routes').document(route['id'])
        batch.set(ref, {
            "route_id": route['id'],
            "from_location": route['from'],
            "to_location": route['to'],
            "distance_metres": route['dist'],
            "walk_time_minutes": route['time'],
            "level_changes": route['levels'],
            "steps": route['steps'],
            "tip": route['tip']
        })
    batch.commit()
    print("Success: navigation_routes collection seeded.")

def seed_match_events():
    print("Seeding match_events collection...")
    events = [
        {"id": "ME-01", "name": "Gates Open", "offset": -90, "time": "6:00 PM IST", "impact": "low", "zones": [], "desc": "Gates are now open for the match.", "alert": "Gates are now open. Gate 4 and Gate 11 are currently clear — recommended for fast entry."},
        {"id": "ME-02", "name": "Match Start — First Innings", "offset": 0, "time": "7:30 PM IST", "impact": "low", "zones": [], "desc": "The match has officially started.", "alert": "Match has started. Food courts are quiet for the next 10 overs — great time to grab food."},
        {"id": "ME-03", "name": "Drinks Break — First Innings", "offset": 50, "time": "8:20 PM IST", "impact": "high", "zones": ["food", "toilet"], "desc": "Strategic timeout in the first innings.", "alert": "Drinks break — expect 8 to 10 minute queues at food courts for next 15 minutes. FC-02 and FC-04 are shortest right now."},
        {"id": "ME-04", "name": "Mid-Innings Break — Over 10", "offset": 75, "time": "8:45 PM IST", "impact": "high", "zones": ["food", "toilet"], "desc": "Tenth over completed, short break.", "alert": "Mid-innings break. Toilet blocks near Gate 5 and Gate 9 are busy. Use TB-07 or TB-14 instead."},
        {"id": "ME-05", "name": "Innings Break", "offset": 110, "time": "9:10 PM IST", "impact": "critical", "zones": ["food", "toilet", "merchandise"], "desc": "First innings over, transition period.", "alert": "Innings break has started. All food courts will be busy for 20 minutes. FC-04, FC-08, FC-11, FC-13, FC-17 have shortest queues right now."},
        {"id": "ME-06", "name": "Second Innings Start", "offset": 130, "time": "9:40 PM IST", "impact": "low", "zones": [], "desc": "Mumbai Indians start their chase.", "alert": "Second innings starting. Food courts clearing up — good time to get food for the next 8 overs."},
        {"id": "ME-07", "name": "Drinks Break — Second Innings", "offset": 175, "time": "10:25 PM IST", "impact": "high", "zones": ["food", "toilet"], "desc": "Strategic timeout in the second innings.", "alert": "Drinks break. FC-02, FC-08, FC-11 still have short queues. Avoid FC-01, FC-03, FC-09."},
        {"id": "ME-08", "name": "Last 3 Overs — Exit Warning", "offset": 205, "time": "10:55 PM IST", "impact": "critical", "zones": ["gates"], "desc": "Final overs of the match.", "alert": "Match ending soon. To beat the rush: Gate 4, Gate 7 (VIP), Gate 11 are clearest exits right now. Leave after this over if you are parked far."}
    ]
    
    batch = db.batch()
    for ev in events:
        ref = db.collection('match_events').document(ev['id'])
        batch.set(ref, {
            "event_id": ev['id'],
            "event_name": ev['name'],
            "match_minute_offset": ev['offset'],
            "expected_time_ist": ev['time'],
            "crowd_impact_level": ev['impact'],
            "affected_zones": ev['zones'],
            "description": ev['desc'],
            "venueiq_alert_message": ev['alert']
        })
    batch.commit()
    print("Success: match_events collection seeded.")

if __name__ == "__main__":
    seed_stadiums()
    seed_venue_zones()
    seed_crowd_data()
    seed_navigation_routes()
    seed_match_events()
    print("\n--- Seeding Complete ---")
