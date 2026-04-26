import sys
import os

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print(f"[Debug] Starting import test from {project_root}...")
sys.stdout.flush()

try:
    print("[Debug] Attempting to import venueiq_agents.agent...")
    sys.stdout.flush()
    from venueiq_agents.agent import root_agent
    print("[Debug] Import successful!")
except Exception as e:
    print(f"[Debug] Import failed: {e}")
    import traceback
    traceback.print_exc()

sys.stdout.flush()
