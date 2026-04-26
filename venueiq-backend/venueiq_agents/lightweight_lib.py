import os
import json
import httpx
import asyncio
import google.auth
import google.auth.transport.requests
import datetime
from typing import List, Any, Dict, Callable

# Constants from .env or defaults
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "kaggle-5b-478308")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL_NAME = "gemini-2.5-flash" # High-speed, high-accuracy model requested by user

class FunctionTool:
    def __init__(self, func: Callable, parameters: Dict = None):
        self.func = func
        self.name = func.__name__
        self.description = func.__doc__ or ""
        self.parameters = parameters or {
            "type": "object",
            "properties": {},
            "required": []
        }

class LlmAgent:
    def __init__(self, name: str, model: str, instruction: str, tools: List[FunctionTool] = None, sub_agents: List['LlmAgent'] = None, output_key: str = "response"):
        self.name = name
        self.model = model
        self.instruction = instruction
        self.tools = tools or []
        self.sub_agents = sub_agents or []
        self.output_key = output_key
        self._token_expiry = datetime.datetime.now()

    def _get_token(self):
        if not hasattr(self, "_cached_token") or datetime.datetime.now() > self._token_expiry:
            print(f"[{self.name}] Refreshing OAuth token...")
            creds, project = google.auth.default()
            auth_req = google.auth.transport.requests.Request()
            creds.refresh(auth_req)
            self._cached_token = creds.token
            self._token_expiry = datetime.datetime.now() + datetime.timedelta(minutes=30)
            print(f"[{self.name}] Token refreshed.")
        return self._cached_token

    async def run(self, prompt: str, history: List[Dict] = None):
        """Runs the agent loop until a final text response is achieved."""
        current_history = (history or []).copy()
        
        # Add the latest user message
        current_history.append({"role": "user", "parts": [{"text": prompt}]})
        
        async with httpx.AsyncClient() as client:
            while True:
                token = self._get_token()
                url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{self.model}:generateContent"
                headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
                
                # Construct payload with system_instruction
                payload = {
                    "contents": current_history,
                    "system_instruction": {"parts": [{"text": self.instruction}]}
                }
                if self.tools:
                    payload["tools"] = [{"function_declarations": [{"name": t.name, "description": t.description, "parameters": t.parameters} for t in self.tools]}]

                print(f"[{self.name}] Calling Vertex AI ({self.model})...")
                try:
                    response = await client.post(url, headers=headers, json=payload, timeout=60.0)
                except Exception as e:
                    print(f"[{self.name}] Request failed: {e}")
                    yield {"content": {"parts": [{"text": f"[Request Failed: {e}]"}]}}
                    return
                
                print(f"[{self.name}] Response received (Status: {response.status_code}).")
                
                if response.status_code != 200:
                    error_msg = response.text
                    print(f"[Error] API {response.status_code}: {error_msg}")
                    yield {"content": {"parts": [{"text": f"[Backend Error: {response.status_code}]"}]}}
                    return

                data = response.json()
                candidates = data.get("candidates", [])
                if not candidates:
                    yield {"content": {"parts": [{"text": "[No response from model]"}]}}
                    return

                cand = candidates[0]
                content = cand.get("content", {})
                parts = content.get("parts", [])
                
                # Record the model's response in history
                current_history.append(content)
                
                # Process parts
                text_found = False
                func_calls = []
                
                for part in parts:
                    if "text" in part:
                        text = part["text"]
                        if text.strip() and "transfer_to_agent" not in text.lower():
                            yield cand # Yield the whole candidate to main.py
                            text_found = True
                    if "functionCall" in part:
                        func_calls.append(part["functionCall"])

                if not func_calls:
                    break # Done, no more tools to call
                
                # Execute function calls
                response_parts = []
                for fc in func_calls:
                    name = fc["name"]
                    args = fc.get("args", {})
                    print(f"[{self.name}] Executing Tool: {name}")
                    
                    if name == "transfer_to_agent":
                        agent_name = args.get("agent_name")
                        target = next((a for a in self.sub_agents if a.name == agent_name), None)
                        if target:
                            print(f"[{self.name}] Transferring to {agent_name}")
                            async for sub_cand in target.run(prompt, current_history):
                                yield sub_cand
                            return
                        else:
                            result = {"error": f"Agent {agent_name} not found"}
                    else:
                        tool = next((t for t in self.tools if t.name == name), None)
                        if tool:
                            try:
                                # Check if tool is async
                                if asyncio.iscoroutinefunction(tool.func):
                                    result = await tool.func(**args)
                                else:
                                    result = tool.func(**args)
                            except Exception as e:
                                result = {"error": str(e)}
                        else:
                            result = {"error": f"Tool {name} not found"}
                    
                    response_parts.append({
                        "functionResponse": {
                            "name": name,
                            "response": {"content": result}
                        }
                    })
                
                # Add the tool results back to history and loop
                current_history.append({"role": "user", "parts": response_parts})

# Mock Firestore Logic (Using local JSON)
class MockDB:
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "stadium_data.json"), "r") as f:
            self.data = json.load(f)
    
    def collection(self, name): return self
    def document(self, name):
        class Doc:
            def __init__(self, d): self.d = d; self.exists = True
            def to_dict(self): return self.d
        return Doc(self.data.get(name, {}))
    def stream(self, **kwargs): return []

def get_db():
    from google.cloud import firestore
    return firestore.Client(project=PROJECT_ID)

print("[LightweightLib] Initialized (REST + Local JSON)")
