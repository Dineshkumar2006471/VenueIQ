import sys
import os

print("[Debug] Starting import test...")
sys.stdout.flush()

try:
    from venueiq_agents.agent import root_agent
    print("[Debug] Import successful!")
except Exception as e:
    print(f"[Debug] Import failed: {e}")

sys.stdout.flush()
