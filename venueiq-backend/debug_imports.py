import sys
print("Checking imports...")

try:
    print("Importing os, json, datetime...")
    import os, json, datetime
    print("Done.")

    print("Importing fastapi...")
    from fastapi import FastAPI
    print("Done.")

    print("Importing firebase_admin...")
    import firebase_admin
    from firebase_admin import firestore
    print("Done.")

    print("Importing venueiq_agents...")
    # This might be the one
    import venueiq_agents
    print("Done.")

    print("Importing google.adk...")
    from google.adk.runners import Runner
    print("Done.")

    print("All imports finished successfully.")
except Exception as e:
    print(f"Error during imports: {e}")
