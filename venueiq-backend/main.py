import os
import json
import datetime
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Set Vertex AI env vars
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "kaggle-5b-478308").strip()
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1").strip()

# Import agents (now lightweight)
from venueiq_agents.agent import root_agent, food_agent, match_agent, get_db

from cricket_api import (
    fetch_current_matches,
    fetch_match_info,
    transform_all_matches,
    get_best_match
)

# ─── FastAPI App ─────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[VenueIQ] API starting up (Lightweight Mode)...")
    yield
    print("[VenueIQ] API shutting down...")

app = FastAPI(
    title="VenueIQ API",
    description="AI-Powered Smart Venue Experience — Agentic Premier League",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Models ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    user_name: str = "Attendee"

class ChatResponse(BaseModel):
    response: str
    session_id: str
    agent_used: str = ""

class IncidentStatusUpdate(BaseModel):
    status: str

def select_chat_agent(message: str):
    """Route obvious demo-critical intents without relying on model self-transfer."""
    lowered = message.lower()
    food_terms = ("food", "snack", "drink", "queue", "shortest", "toilet", "restroom")
    match_terms = ("score", "match", "cricket", "batting", "bowling", "wicket", "over", "prediction")

    if any(term in lowered for term in food_terms):
        return food_agent
    if any(term in lowered for term in match_terms):
        return match_agent
    return root_agent

# ─── Chat Endpoint ───────────────────────────────────────

@app.post("/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint — routes to the VenueIQ Agentic Mesh with Streaming."""
    print(f"[Chat Request] Session: {request.session_id} | Message: {request.message}")
    selected_agent = select_chat_agent(request.message)
    print(f"[Chat Routing] Selected agent: {selected_agent.name}")
    
    async def event_generator():
        try:
            # We call the root agent. It yields candidate chunks.
            # The lightweight_lib handles tool calls and agent transfers internally.
            async for cand in selected_agent.run(request.message):
                if "content" in cand and "parts" in cand["content"]:
                    for part in cand["content"]["parts"]:
                        if "text" in part:
                            text = part["text"]
                            # --- FIX FOR LINE 167 (Orchestration Leak) ---
                            # We ensure that internal orchestration strings never reach the user.
                            # We also filter out empty strings or purely whitespace.
                            if not text or "transfer_to_agent" in text.lower():
                                continue
                            yield text
                        
        except Exception as run_error:
            print(f"[Streaming Error] {run_error}")
            yield " [Concierge is updating... please wait] "

    return StreamingResponse(event_generator(), media_type="text/plain")

# ─── Scoreboard Endpoints ────────────────────────────────

@app.get("/api/matches")
async def get_matches():
    """Returns all current matches."""
    data = await fetch_current_matches()
    transformed = transform_all_matches(data)
    return {"status": "success", "matches": transformed}

@app.get("/api/matches/primary")
async def get_primary_match():
    """Returns the single most relevant live match."""
    data = await fetch_current_matches()
    transformed = transform_all_matches(data)
    best = get_best_match(transformed)
    return {"status": "success", "match": best}

@app.get("/health")
def health():
    return {"status": "ok", "mode": "lightweight"}

# Admin operations

@app.get("/admin/incidents")
async def get_incidents():
    """Returns reported venue incidents for the operations console."""
    try:
        db = get_db()
        docs = db.collection("incident_reports").stream()
        incidents = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            incidents.append(data)
        incidents.sort(key=lambda x: str(x.get("reported_at", "")), reverse=True)
        return {"status": "success", "incidents": incidents}
    except Exception as exc:
        print(f"[Admin Incidents Error] {exc}")
        return {"status": "success", "incidents": []}

@app.patch("/admin/incidents/{incident_id}")
async def update_incident_status(incident_id: str, update: IncidentStatusUpdate):
    """Updates the workflow status for a reported venue incident."""
    allowed = {"open", "in_progress", "resolved"}
    if update.status not in allowed:
        raise HTTPException(status_code=400, detail="Invalid incident status")

    try:
        db = get_db()
        db.collection("incident_reports").document(incident_id).update({
            "status": update.status,
            "updated_at": datetime.datetime.utcnow()
        })
        return {"status": "success", "incident_id": incident_id, "new_status": update.status}
    except Exception as exc:
        print(f"[Admin Update Error] {exc}")
        raise HTTPException(status_code=500, detail="Could not update incident")

# ─── Entry Point ─────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
