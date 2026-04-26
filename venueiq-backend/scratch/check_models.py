import google.auth
import google.auth.transport.requests
import httpx
import os

PROJECT_ID = "kaggle-5b-478308"
LOCATION = "us-central1"

def check_models():
    creds, project = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    token = creds.token
    
    url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        models = response.json().get("models", [])
        for m in models:
            print(m.get("name"))
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    check_models()
