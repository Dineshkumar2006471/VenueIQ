print("Starting import test...")
import os
import sys

print("Loading vertex ai env vars...")
# Set Vertex AI env vars
os.environ["GOOGLE_CLOUD_PROJECT"] = "kaggle-5b-478308"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"

print("Importing google.adk.runners...")
try:
    from google.adk.runners import Runner
    print("Successfully imported Runner!")
except Exception as e:
    print(f"Error importing Runner: {e}")

print("Importing google.adk.sessions...")
try:
    from google.adk.sessions import InMemorySessionService
    print("Successfully imported InMemorySessionService!")
except Exception as e:
    print(f"Error importing InMemorySessionService: {e}")

print("Done with import test.")
