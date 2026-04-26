import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "kaggle-5b-478308").strip()
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1").strip()
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"

client = genai.Client()
try:
    models = client.models.list()
    for m in models:
        print(f"Model: {m.name}")
except Exception as e:
    print(f"Error: {e}")
