import os
import httpx
import google.auth
import google.auth.transport.requests

PROJECT_ID = "kaggle-5b-478308"
LOCATION = "us-central1"
MODELS = ["gemini-1.5-flash-002", "gemini-2.0-flash-exp", "gemini-2.5-flash"]

def get_token():
    creds, project = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    return creds.token

def test_model(model):
    token = get_token()
    url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{model}:generateContent"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "contents": [{"role": "user", "parts": [{"text": "hi"}]}]
    }
    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=10.0)
        print(f"Model {model}: {response.status_code}")
        if response.status_code != 200:
            print(f"  Error: {response.text[:100]}")
    except Exception as e:
        print(f"Model {model}: Failed - {e}")

if __name__ == "__main__":
    for m in MODELS:
        test_model(m)
