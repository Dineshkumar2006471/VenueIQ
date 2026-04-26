import google.auth
import google.auth.transport.requests
import httpx
import os

PROJECT_ID = "kaggle-5b-478308"
LOCATION = "us-central1"
MODEL_NAME = "gemini-2.5-flash"

def test_2_5():
    creds, project = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    token = creds.token
    
    url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_NAME}:generateContent"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": "Hello"}]}]
    }
    
    response = httpx.post(url, headers=headers, json=payload, timeout=10.0)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_2_5()
