import os
import httpx
import google.auth
import google.auth.transport.requests

def test_model(model_name):
    print(f"Testing model: {model_name}")
    PROJECT_ID = "kaggle-5b-478308"
    LOCATION = "us-central1"
    creds, _ = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    token = creds.token
    
    url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{model_name}:generateContent"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"contents": [{"role": "user", "parts": [{"text": "Hello"}]}]}
    
    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=10.0)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Success!")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_model("gemini-2.5-flash")
    test_model("gemini-2.0-flash")
    test_model("gemini-1.5-flash")
