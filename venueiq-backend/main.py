import os
import json
import datetime
import asyncio
import time
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

FAST_CACHE_TTL_SECONDS = int(os.getenv("FAST_CACHE_TTL_SECONDS", "30"))
_fast_cache: dict[str, object] = {}
_fast_cache_timestamps: dict[str, float] = {}

def _cache_get(key: str):
    timestamp = _fast_cache_timestamps.get(key)
    if timestamp and (time.time() - timestamp) < FAST_CACHE_TTL_SECONDS:
        return _fast_cache.get(key)
    return None

def _cache_set(key: str, value: object):
    _fast_cache[key] = value
    _fast_cache_timestamps[key] = time.time()
    return value

def warm_fast_cache():
    """Prime Firestore-backed fast responses so first user chat is not slow."""
    try:
        db = get_db()
        match_doc = db.collection("match_data").document("current_match").get()
        _cache_set("match", match_doc.to_dict() if match_doc.exists else {})
        _cache_set("venue_zones", [doc.to_dict() for doc in db.collection("venue_zones").stream()])
        _cache_set("crowd_data", [doc.to_dict() for doc in db.collection("crowd_data").stream()])
        print("[VenueIQ] Fast concierge cache warmed.")
    except Exception as exc:
        print(f"[VenueIQ] Fast cache warm skipped: {exc}")

# ─── FastAPI App ─────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[VenueIQ] API starting up (Lightweight Mode)...")
    warm_fast_cache()
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

def _read_numeric(data: dict, keys: tuple[str, ...], default: int = 0) -> int:
    for key in keys:
        value = data.get(key)
        if value is None:
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return default

def _format_match_fast_response(match: dict) -> str:
    team1 = match.get("team1", {})
    team2 = match.get("team2", {})
    if not team1:
        return "No live match data is available right now."

    team1_name = team1.get("name", "Team 1")
    team1_short = team1.get("short", team1_name)
    team2_name = team2.get("name", "Team 2")
    score = team1.get("score", "N/A")
    overs = team1.get("overs", "N/A")
    top_scorer = team1.get("top_scorer")
    status = match.get("status", "Live")

    response = f"{team1_name} ({team1_short}) are {score} after {overs} overs against {team2_name}. {status}"
    if top_scorer and top_scorer != "—":
        response += f" Top scorer: {top_scorer}."
    return response

def _format_food_fast_response(zones: list[dict]) -> str:
    food_zones = [
        zone for zone in zones
        if zone.get("type") == "food" or zone.get("zone_type") == "food"
    ]
    if not food_zones:
        return "I could not find live food-court queue data right now."

    best = min(food_zones, key=lambda zone: _read_numeric(zone, ("wait_minutes", "current_wait_mins", "wait_time"), 999))
    wait = _read_numeric(best, ("wait_minutes", "current_wait_mins", "wait_time"), 0)
    name = best.get("name") or best.get("zone_id") or "the nearest food court"
    gate = best.get("gate_nearest")
    items = best.get("menu_items") or best.get("popular_items") or []

    response = f"The shortest food queue is at {name} with about a {wait}-minute wait."
    if gate:
        response += f" It is nearest to {gate}."
    if items:
        response += f" Popular options include {', '.join(items[:3])}."
    return response

def _format_gate_fast_response(gates: list[dict]) -> str:
    public_gates = [gate for gate in gates if not gate.get("is_vip_only")]
    if not public_gates:
        return "I could not find live gate data right now."

    best = min(public_gates, key=lambda gate: _read_numeric(gate, ("exit_wait_minutes", "entry_wait_minutes", "wait_minutes"), 999))
    wait = _read_numeric(best, ("exit_wait_minutes", "entry_wait_minutes", "wait_minutes"), 0)
    name = best.get("display_name") or best.get("gate_id") or "the clearest gate"
    status = best.get("current_status") or best.get("density")
    recommendation = best.get("recommendation_text")

    response = f"The quickest exit option is {name} with about a {wait}-minute wait."
    if status:
        response += f" Current status: {status}."
    if recommendation:
        response += f" {recommendation}"
    return response

def get_fast_concierge_response(message: str) -> str | None:
    """Return low-latency answers for common match-day queries."""
    lowered = message.lower()
    try:
        if any(term in lowered for term in ("score", "match", "cricket", "batting", "wicket", "over")):
            match = _cache_get("match")
            if match is None:
                db = get_db()
                doc = db.collection("match_data").document("current_match").get()
                match = _cache_set("match", doc.to_dict() if doc.exists else {})
            return _format_match_fast_response(match)

        if any(term in lowered for term in ("food", "snack", "drink", "queue", "shortest")):
            zones = _cache_get("venue_zones")
            if zones is None:
                db = get_db()
                zones = _cache_set("venue_zones", [doc.to_dict() for doc in db.collection("venue_zones").stream()])
            return _format_food_fast_response(zones)

        if any(term in lowered for term in ("exit", "gate", "crowd", "least crowded", "quickest")):
            gates = _cache_get("crowd_data")
            if gates is None:
                db = get_db()
                gates = _cache_set("crowd_data", [doc.to_dict() for doc in db.collection("crowd_data").stream()])
            return _format_gate_fast_response(gates)
    except Exception as exc:
        print(f"[Fast Concierge Error] {exc}")
    return None

# ─── Chat Endpoint ───────────────────────────────────────

@app.post("/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint — routes to the VenueIQ Agentic Mesh with Streaming."""
    print(f"[Chat Request] Session: {request.session_id} | Message: {request.message}")
    fast_response = get_fast_concierge_response(request.message)
    if fast_response:
        print("[Chat Routing] Fast response")

        async def fast_event_generator():
            yield fast_response

        return StreamingResponse(fast_event_generator(), media_type="text/plain")

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
