import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
firebase_admin.initialize_app(options={'projectId': project_id})
db = firestore.client()

doc = db.collection('match_live_data').document('GT-vs-MI-IPL2025').get()
if doc.exists:
    print("Match document found:")
    print(doc.to_dict())
else:
    print("Match document NOT found!")
