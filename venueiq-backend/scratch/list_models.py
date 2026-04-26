import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Set Vertex AI env vars
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "kaggle-5b-478308").strip()
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1").strip()
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION

client = genai.Client()

print(f"Project: {PROJECT_ID}")
print(f"Location: {LOCATION}")

print("\n--- Available Models ---")
try:
    for model in client.models.list():
        print(f"Model: {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
