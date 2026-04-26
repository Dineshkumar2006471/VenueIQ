import os
import firebase_admin
from firebase_admin import firestore
from dotenv import load_dotenv

load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "kaggle-5b-478308").strip()

print(f"Connecting to Firestore project: {PROJECT_ID}")
if not firebase_admin._apps:
    firebase_admin.initialize_app(options={"projectId": PROJECT_ID})

db = firestore.client()
print("Firestore client created.")

try:
    print("Fetching venue_zones...")
    docs = db.collection("venue_zones").limit(1).stream()
    found = False
    for doc in docs:
        print(f"Found zone: {doc.id} => {doc.to_dict().get('name')}")
        found = True
    if not found:
        print("No zones found.")
    print("Firestore test successful.")
except Exception as e:
    print(f"Firestore test failed: {e}")
