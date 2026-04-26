import os
import httpx
import google.auth
import google.auth.transport.requests
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "kaggle-5b-478308")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL_NAME = "gemini-2.5-flash"

creds, project = google.auth.default()
auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)
token = creds.token

url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_NAME}:generateContent"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
payload = {
    "contents": [{"role": "user", "parts": [{"text": "Hello, are you there?"}]}]
}

print(f"Testing Model: {MODEL_NAME}")
print(f"URL: {url}")
try:
    response = httpx.post(url, headers=headers, json=payload, timeout=30.0)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Success!")
        print(response.json()["candidates"][0]["content"]["parts"][0]["text"])
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Failed: {e}")
