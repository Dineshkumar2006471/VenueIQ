"""
CricketData.org API Service for VenueIQ
========================================
Fetches live cricket scores from CricAPI v1 with smart caching.

Endpoints used:
  - /v1/currentMatches — All current/live matches with scores
  - /v1/match_info     — Detailed info for a specific match

Free tier: 100 requests/day → 30s in-memory cache to stay within limits.
Fallback: API → Cache → Firestore seed data
"""

import os
import time
import httpx
import asyncio
from typing import Optional

# ─── Configuration ───────────────────────────────────────

CRICAPI_BASE = "https://api.cricapi.com/v1"
API_KEY = os.getenv("CRICKETDATA_API_KEY", "")
CACHE_TTL_SECONDS = 30  # Cache results for 30s

# ─── In-Memory Cache ────────────────────────────────────

_cache: dict[str, dict] = {}
_cache_timestamps: dict[str, float] = {}


def _is_cache_valid(key: str) -> bool:
    """Check if a cache entry is still valid."""
    if key not in _cache_timestamps:
        return False
    return (time.time() - _cache_timestamps[key]) < CACHE_TTL_SECONDS


def _set_cache(key: str, data: dict):
    """Store data in cache with current timestamp."""
    _cache[key] = data
    _cache_timestamps[key] = time.time()


def _get_cache(key: str) -> Optional[dict]:
    """Get data from cache if valid."""
    if _is_cache_valid(key):
        return _cache[key]
    return None


# ─── API Calls ──────────────────────────────────────────

async def fetch_current_matches() -> dict:
    """
    Fetch all current/live matches from CricAPI.
    Returns raw API response with match list.
    """
    cache_key = "current_matches"
    cached = _get_cache(cache_key)
    if cached:
        cached["_source"] = "cache"
        return cached

    api_key = os.getenv("CRICKETDATA_API_KEY", API_KEY)
    if not api_key:
        return {"status": "error", "error": "No API key configured", "_source": "none"}

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                f"{CRICAPI_BASE}/currentMatches",
                params={"apikey": api_key, "offset": 0}
            )
            data = resp.json()

        if data.get("status") == "success":
            _set_cache(cache_key, data)
            data["_source"] = "api"
            return data
        else:
            # API returned an error (maybe rate limit)
            return {
                "status": "error",
                "error": data.get("reason", "Unknown API error"),
                "_source": "api_error"
            }
    except Exception as e:
        return {"status": "error", "error": str(e), "_source": "network_error"}


async def fetch_match_info(match_id: str) -> dict:
    """
    Fetch detailed info for a specific match.
    """
    cache_key = f"match_{match_id}"
    cached = _get_cache(cache_key)
    if cached:
        cached["_source"] = "cache"
        return cached

    api_key = os.getenv("CRICKETDATA_API_KEY", API_KEY)
    if not api_key:
        return {"status": "error", "error": "No API key configured", "_source": "none"}

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                f"{CRICAPI_BASE}/match_info",
                params={"apikey": api_key, "id": match_id}
            )
            data = resp.json()

        if data.get("status") == "success":
            _set_cache(cache_key, data)
            data["_source"] = "api"
            return data
        else:
            return {
                "status": "error",
                "error": data.get("reason", "Unknown API error"),
                "_source": "api_error"
            }
    except Exception as e:
        return {"status": "error", "error": str(e), "_source": "network_error"}


# ─── Data Transformers ──────────────────────────────────

def _parse_score(score_list: list, team_name: str, other_team_name: str = "") -> dict:
    """
    Parse the CricAPI score array into our team format.
    CricAPI returns: [{"r": 185, "w": 4, "o": 18.3, "inning": "MI Inning 1"}, ...]
    
    CricAPI quirk: The chasing team's inning often contains BOTH team names,
    e.g., "Delhi Capitals,Punjab Kings Inning 1" for PBKS's chase.
    We handle this by:
    1. First look for innings that contain ONLY this team's name (exclusive match)
    2. Then look for innings containing both team names (ambiguous/chase innings)
       and assign them to the SECOND team listed
    """
    team_score = "Yet to bat"
    team_overs = "0.0"
    runs = 0
    wickets = 0
    overs = 0.0

    if not score_list:
        return {"score": team_score, "overs": team_overs, "run_rate": "0.00"}

    team_lower = team_name.lower()
    other_lower = other_team_name.lower() if other_team_name else ""

    # Pass 1: Look for exclusive match (this team's name only, not both)
    for s in reversed(score_list):
        inning_name = s.get("inning", "").lower()
        has_this_team = team_lower in inning_name
        has_other_team = other_lower and other_lower in inning_name
        
        if has_this_team and not has_other_team:
            # Exclusive match — this inning belongs to this team
            runs = s.get("r", 0)
            wickets = s.get("w", 0)
            overs = s.get("o", 0)
            team_score = f"{runs}/{wickets}"
            team_overs = str(overs)
            break
    else:
        # Pass 2: Handle ambiguous innings (both team names in label)
        # Format is usually "TeamA,TeamB Inning 1" → belongs to TeamB (chaser)
        for s in reversed(score_list):
            inning_name = s.get("inning", "").lower()
            has_this_team = team_lower in inning_name
            has_other_team = other_lower and other_lower in inning_name
            
            if has_this_team and has_other_team:
                # Both teams in the label — figure out who it belongs to
                # The convention is "BattingTeam,ChasingTeam Inning N"
                # Check if this team appears AFTER the comma (= chasing team)
                parts = inning_name.split(",")
                if len(parts) >= 2:
                    # If this team is in the second part (after comma), this is their inning
                    second_part = parts[-1]
                    if team_lower in second_part or (other_lower and other_lower not in second_part):
                        runs = s.get("r", 0)
                        wickets = s.get("w", 0)
                        overs = s.get("o", 0)
                        team_score = f"{runs}/{wickets}"
                        team_overs = str(overs)
                        break

    # Calculate run rate
    run_rate = "0.00"
    if overs and overs > 0:
        run_rate = f"{runs / overs:.2f}"

    return {
        "score": team_score,
        "overs": team_overs,
        "run_rate": run_rate
    }


def transform_match(match: dict) -> dict:
    """
    Transform a CricAPI match object into our frontend MatchData format.
    
    CricAPI format:
    {
      "id": "abc123",
      "name": "Mumbai Indians vs Chennai Super Kings, 42nd Match",
      "matchType": "t20",
      "status": "Mumbai Indians won by 5 wickets",
      "venue": "Wankhede Stadium, Mumbai",
      "teams": ["Mumbai Indians", "Chennai Super Kings"],
      "teamInfo": [{"name": "Mumbai Indians", "shortname": "MI", "img": "..."}],
      "score": [{"r": 185, "w": 4, "o": 18.3, "inning": "Mumbai Indians Inning 1"}],
      "dateTimeGMT": "2026-04-25T14:00:00",
      "matchStarted": true,
      "matchEnded": false
    }
    """
    teams = match.get("teams", ["Team A", "Team B"])
    team_info = match.get("teamInfo", [])
    score_list = match.get("score", [])

    # Team 1
    team1_name = teams[0] if len(teams) > 0 else "Team A"
    team1_short = ""
    team1_img = ""
    for ti in team_info:
        if ti.get("name") == team1_name:
            team1_short = ti.get("shortname", team1_name[:3].upper())
            team1_img = ti.get("img", "")
            break
    if not team1_short:
        team1_short = team1_name[:3].upper()

    # Team 2
    team2_name = teams[1] if len(teams) > 1 else "Team B"
    team2_short = ""
    team2_img = ""
    for ti in team_info:
        if ti.get("name") == team2_name:
            team2_short = ti.get("shortname", team2_name[:3].upper())
            team2_img = ti.get("img", "")
            break
    if not team2_short:
        team2_short = team2_name[:3].upper()

    # Parse scores (pass both team names for disambiguation)
    t1_score = _parse_score(score_list, team1_name, team2_name)
    t2_score = _parse_score(score_list, team2_name, team1_name)

    # Determine match state
    match_started = match.get("matchStarted", False)
    match_ended = match.get("matchEnded", False)

    if match_ended:
        match_state = "completed"
    elif match_started:
        match_state = "live"
    else:
        match_state = "upcoming"

    return {
        "id": match.get("id", ""),
        "match": match.get("name", f"{team1_name} vs {team2_name}"),
        "match_type": match.get("matchType", "unknown"),
        "match_state": match_state,
        "team1": {
            "name": team1_name,
            "short": team1_short,
            "img": team1_img,
            "score": t1_score["score"],
            "overs": t1_score["overs"],
            "run_rate": t1_score["run_rate"]
        },
        "team2": {
            "name": team2_name,
            "short": team2_short,
            "img": team2_img,
            "score": t2_score["score"],
            "overs": t2_score["overs"],
            "run_rate": t2_score["run_rate"]
        },
        "status": match.get("status", ""),
        "venue": match.get("venue", ""),
        "date": match.get("dateTimeGMT", ""),
        "series": match.get("series_id", ""),
        "fantasy_enabled": match.get("fantasyEnabled", False),
        "bbb_enabled": match.get("bbbEnabled", False)
    }


def transform_all_matches(api_response: dict) -> list[dict]:
    """
    Transform the full currentMatches API response into a list of MatchData.
    Sorts: live first, then upcoming, then completed.
    """
    if api_response.get("status") != "success":
        return []

    matches = api_response.get("data", [])
    transformed = []

    for m in matches:
        if not m or not isinstance(m, dict):
            continue
        # Skip entries that are just match type headers
        if "id" not in m:
            continue
        transformed.append(transform_match(m))

    # Sort: live > upcoming > completed
    order = {"live": 0, "upcoming": 1, "completed": 2}
    transformed.sort(key=lambda x: order.get(x.get("match_state", ""), 3))

    return transformed


def get_best_match(matches: list[dict]) -> Optional[dict]:
    """
    Pick the "best" match to show as the primary score.
    Priority: IPL live > any live > IPL upcoming > any upcoming > latest completed
    """
    if not matches:
        return None

    # First, try live IPL
    for m in matches:
        if m.get("match_state") == "live" and "premier league" in m.get("match", "").lower():
            return m

    # Then any live match
    for m in matches:
        if m.get("match_state") == "live":
            return m

    # Then upcoming IPL
    for m in matches:
        if m.get("match_state") == "upcoming" and "premier league" in m.get("match", "").lower():
            return m

    # Then any upcoming
    for m in matches:
        if m.get("match_state") == "upcoming":
            return m

    # Fallback: first match (should be completed)
    return matches[0]
