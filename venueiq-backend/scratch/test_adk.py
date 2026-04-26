import sys
print("Testing google.adk imports...")
sys.stdout.flush()
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
print("Import successful!")
sys.stdout.flush()
