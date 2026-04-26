import os
import json
import datetime
from .lightweight_lib import LlmAgent, FunctionTool, get_db

# ─── Context ─────────────────────────────────────────────
def get_stadium_context():
    try:
        db = get_db()
        # Fallback to match_data if specific stadium doc isn't found
        match_doc = db.collection("match_data").document("current_match").get()
        match = match_doc.to_dict() if match_doc.exists else {}
        return f"Stadium: Narendra Modi Stadium, Ahmedabad. Match: {match.get('match', 'Live IPL Match')}. Score: {match.get('score', '0/0')}. Status: {match.get('status', 'Active')}."
    except Exception as e:
        print(f"[Context Error] {e}")
        return "Stadium: Narendra Modi Stadium, Ahmedabad. Status: Live Match Day."

# ─── Tools ───────────────────────────────────────────────

def get_food_court_status(zone_id: str = "all") -> str:
    """Returns wait times and menu availability for food zones or toilets."""
    db = get_db()
    if zone_id == "all":
        docs = db.collection("venue_zones").stream()
        results = [d.to_dict() for d in docs]
    else:
        doc = db.collection("venue_zones").document(zone_id).get()
        results = [doc.to_dict()] if doc.exists else []
    
    return json.dumps(results, default=str)

def get_crowd_status(gate_id: str = "all") -> str:
    """Returns real-time gate wait times and density levels."""
    db = get_db()
    if gate_id == "all":
        docs = db.collection("crowd_data").stream()
        results = [d.to_dict() for d in docs]
    else:
        # Normalize gate_id to match document ID (e.g. "Gate 1" -> "Gate_1")
        doc_id = gate_id.replace(" ", "_")
        doc = db.collection("crowd_data").document(doc_id).get()
        results = [doc.to_dict()] if doc.exists else []
        
    return json.dumps(results, default=str)

def get_navigation(destination: str) -> str:
    """Provides directions to a specific area or facility."""
    db = get_db()
    # Destination in seeded data is the doc ID
    doc = db.collection("navigation").document(destination).get()
    if doc.exists:
        return json.dumps(doc.to_dict(), default=str)
    
    # Fuzzy search if exact match fails
    docs = db.collection("navigation").stream()
    for d in docs:
        data = d.to_dict()
        if destination.lower() in data.get("destination", "").lower():
            return json.dumps(data, default=str)
            
    return json.dumps({"error": "Destination not found in map data."})

def report_issue(issue_type: str, location: str, description: str) -> str:
    """Report a venue issue (cleanliness, safety, etc.)."""
    db = get_db()
    report = {
        "type": issue_type,
        "location": location,
        "description": description,
        "status": "open",
        "priority": "medium",
        "reported_at": datetime.datetime.utcnow()
    }
    db.collection("incident_reports").add(report)
    return json.dumps({"success": True, "message": "Issue logged in Firestore. Staff notified."})

def get_match_data() -> str:
    """Reads live match state (scores, stats)."""
    db = get_db()
    match_doc = db.collection("match_data").document("current_match").get()
    match = match_doc.to_dict() if match_doc.exists else {"status": "No live match data found."}
    return json.dumps(match, default=str)

def fetch_food_vendors():
    """Fetches the list of active food and snack vendors in the stadium."""
    db = get_db()
    from google.cloud.firestore_v1.base_query import FieldFilter
    docs = db.collection("venue_zones").where(filter=FieldFilter("zone_type", "==", "food")).stream()
    return json.dumps([d.to_dict() for d in docs], default=str)

def fetch_venue_amenities():
    """Fetches info about restrooms, medical rooms, and lost & found."""
    db = get_db()
    from google.cloud.firestore_v1.base_query import FieldFilter
    # Firestore 'in' queries are limited to 10 items
    docs = db.collection("venue_zones").where(filter=FieldFilter("zone_type", "in", ["toilet", "medical", "retail"])).stream()
    return json.dumps([d.to_dict() for d in docs], default=str)

# ─── AGENTS ─────────────────────────────────────────────
# Model to use (Gemini 1.5 Flash 002 is verified available and ultra-fast for hackathons)
MODEL_NAME = "gemini-2.5-flash"

food_agent = LlmAgent(
    name="FoodAgent",
    model=MODEL_NAME,
    instruction="""You are the Food & Beverage specialist for VenueIQ.
    - Use get_food_court_status to find wait times and menus.
    - Use fetch_food_vendors to find available vendors.
    - Use fetch_venue_amenities for toilets.
    - Recommend the shortest queue.
    - Be brief and helpful.""",
    tools=[
        FunctionTool(get_food_court_status, {
            "type": "object",
            "properties": {"zone_id": {"type": "string", "description": "The zone ID (e.g. 'adani_pavilion')"}},
        }),
        FunctionTool(fetch_food_vendors, {
            "type": "object", "properties": {}
        }),
        FunctionTool(fetch_venue_amenities, {
            "type": "object", "properties": {}
        })
    ],
    output_key="food_response"
)

navigation_agent = LlmAgent(
    name="NavigationAgent",
    model=MODEL_NAME,
    instruction="""You are the Navigation specialist for VenueIQ.
    - Use get_navigation for step-by-step directions.
    - Provide concise directions.""",
    tools=[
        FunctionTool(get_navigation, {
            "type": "object",
            "properties": {"destination": {"type": "string", "description": "The destination area (e.g. 'toilet_block_B')"}},
            "required": ["destination"]
        })
    ],
    output_key="nav_response"
)

match_agent = LlmAgent(
    name="MatchAgent",
    model=MODEL_NAME,
    instruction="""You are the Match Intelligence specialist for VenueIQ.
    - Use get_match_data for scores, stats, and match status.
    - Use get_crowd_status for gate info and wait times.
    - Use fetch_venue_amenities for general stadium info.
    - Be energetic and accurate.""",
    tools=[
        FunctionTool(get_match_data, {"type": "object", "properties": {}}),
        FunctionTool(fetch_venue_amenities, {"type": "object", "properties": {}}),
        FunctionTool(get_crowd_status, {
            "type": "object",
            "properties": {"gate_id": {"type": "string", "description": "The gate ID (e.g. 'Gate 1')"}}
        })
    ],
    output_key="match_response"
)

# Root agent transfers
def transfer_to_agent(agent_name: str):
    """Transfer the conversation to a specialized agent (FoodAgent or MatchAgent)."""
    return f"Transferred to {agent_name}"

root_agent = LlmAgent(
    name="VenueIQ_Orchestrator",
    model=MODEL_NAME,
    instruction=f"""You are VenueIQ — the AI concierge for Narendra Modi Stadium.
    
    STADIUM CONTEXT: {get_stadium_context()}
    
    - For food, snacks, drinks, or toilets: Use transfer_to_agent(agent_name="FoodAgent").
    - For match details, stadium info, crowd status, or venue issues: Use transfer_to_agent(agent_name="MatchAgent").
    - For directions: Use get_navigation.
    - Be brief and helpful.
    """,
    tools=[
        FunctionTool(transfer_to_agent, {
            "type": "object",
            "properties": {"agent_name": {"type": "string", "enum": ["FoodAgent", "MatchAgent"]}},
            "required": ["agent_name"]
        }),
        FunctionTool(get_navigation, {
            "type": "object",
            "properties": {"destination": {"type": "string"}},
            "required": ["destination"]
        }),
        FunctionTool(report_issue, {
            "type": "object",
            "properties": {
                "issue_type": {"type": "string"},
                "location": {"type": "string"},
                "description": {"type": "string"}
            },
            "required": ["issue_type", "location", "description"]
        }),
        FunctionTool(get_crowd_status, {
            "type": "object",
            "properties": {"gate_id": {"type": "string"}}
        })
    ],
    sub_agents=[food_agent, match_agent],
    output_key="final_response"
)

print("[VenueIQ] Agents Refactored (Real Firestore + Gemini 1.5 Flash 002)")
