"""
Seed community_posts and organizer_advisories collections in Firestore.
Run this once to populate the community feed for demo purposes.
"""
import os
import datetime
import firebase_admin
from firebase_admin import credentials, firestore

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "kaggle-5b-478308").strip()

# Initialize Firebase Admin SDK
cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', './serviceAccount.json')
if os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
else:
    firebase_admin.initialize_app(options={'projectId': PROJECT_ID})

db = firestore.client()

def seed_community_posts():
    """Seed 4 realistic community posts for the demo."""
    
    posts = [
        {
            "text": "Gate 3 queue just cleared up, barely anyone waiting now! Go go go! 🏃‍♂️",
            "author_name": "Rahul S.",
            "stand_location": "North Stand — Near Gate 3",
            "type": "gate_update",
            "timestamp": datetime.datetime.utcnow() - datetime.timedelta(minutes=12),
            "helpful_count": 7,
            "is_advisory": False,
        },
        {
            "text": "Sabarmati food court is almost empty and the khandvi is incredible. Skip the Reliance Stand food plaza, it's a 15 min wait over there.",
            "author_name": "Priya M.",
            "stand_location": "Sabarmati Stand",
            "type": "food_tip",
            "timestamp": datetime.datetime.utcnow() - datetime.timedelta(minutes=8),
            "helpful_count": 14,
            "is_advisory": False,
        },
        {
            "text": "Toilet near Gate 1 (North Stand restrooms) is flooded. Avoid if possible, use the South Stand restrooms near Gate 4 instead.",
            "author_name": "Amit K.",
            "stand_location": "North Stand — Gate 1",
            "type": "crowd_report",
            "timestamp": datetime.datetime.utcnow() - datetime.timedelta(minutes=4),
            "helpful_count": 22,
            "is_advisory": False,
        },
        {
            "text": "Amazing atmosphere at the Adani Pavilion! Gill just hit a massive six and the whole stand erupted. GT fans are electric tonight 🔥🏏",
            "author_name": "Sneha D.",
            "stand_location": "Adani Pavilion",
            "type": "crowd_report",
            "timestamp": datetime.datetime.utcnow() - datetime.timedelta(minutes=1),
            "helpful_count": 31,
            "is_advisory": False,
        },
    ]
    
    for post in posts:
        db.collection("community_posts").add(post)
    print(f"  [OK] {len(posts)} community posts seeded")


def seed_organizer_advisories():
    """Seed 2 sample organizer advisories."""
    
    advisories = [
        {
            "text": "⚠️ Gate 9 temporarily closed for maintenance. Please use Gate 8 for access to the BPCL Stand. Staff available to assist with directions.",
            "author_name": "VenueIQ Operations",
            "severity": "warning",
            "target": "stadium-wide",
            "timestamp": datetime.datetime.utcnow() - datetime.timedelta(minutes=20),
            "is_advisory": True,
            "is_pinned": True,
        },
        {
            "text": "🏏 Innings break in approximately 10 minutes. Food courts will experience high demand. We recommend visiting Sabarmati Stand Quick Bites for the shortest wait times.",
            "author_name": "VenueIQ Operations",
            "severity": "info",
            "target": "stadium-wide",
            "timestamp": datetime.datetime.utcnow() - datetime.timedelta(minutes=6),
            "is_advisory": True,
            "is_pinned": False,
        },
    ]
    
    for adv in advisories:
        db.collection("organizer_advisories").add(adv)
    print(f"  [OK] {len(advisories)} organizer advisories seeded")


if __name__ == "__main__":
    print("--- Seeding Community & Advisory Data ---")
    seed_community_posts()
    seed_organizer_advisories()
    print("\nDone! Community feed is ready for demo.")
