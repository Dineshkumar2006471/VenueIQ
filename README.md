# VenueIQ - Agentic Smart Venue Intelligence

VenueIQ is an AI-powered smart venue intelligence system built for Agentic Premier League 2026 by Google Cloud / Build with AI.

The project turns a large cricket stadium into an intelligent, conversational venue assistant. It models a match-day experience at Narendra Modi Stadium, Ahmedabad, where fans and operators need real-time help with food queues, gates, navigation, live match context, crowd load, and incident reporting.

## Live Deployment

| Service | URL |
| --- | --- |
| Frontend Cloud Run app | https://venueiq-frontend-857911435032.us-central1.run.app |
| Backend Cloud Run API | https://venueiq-backend-857911435032.us-central1.run.app |
| Backend health check | https://venueiq-backend-857911435032.us-central1.run.app/health |

Recommended review path:

1. Open the frontend URL.
2. Visit `Concierge`.
3. Try: `What is the live score?`
4. Try: `Shortest queue for food?`
5. Try: `Quickest gate to exit?`
6. Visit `Live Status`, `Match`, and `Admin` to inspect the operating surfaces.

## Executive Summary

Large venues fail when real-time information is trapped in disconnected systems. Fans do not know which gate is crowded, operators do not get enough structured incident context, and food/navigation decisions are often based on guesswork.

VenueIQ solves this with a multi-agent AI concierge backed by Google Cloud. The backend routes natural-language requests to specialized agents and tools. The frontend presents the result through a polished public-facing stadium experience and an operator console.

The submission is designed to show four things clearly:

- A practical real-world problem with high crowd impact.
- An agentic backend where the model can route, call tools, and use live data.
- Google Cloud integration through Cloud Run, Vertex AI, and Firestore.
- A complete user experience, not just an API demo.

## Why VenueIQ Is Competitive

VenueIQ is positioned as a top-tier hackathon submission because it combines a strong use case, working deployment, agentic architecture, and high-quality UI execution.

Key strengths:

- It solves a visible, high-pressure public problem: live crowd and venue decision support.
- It is domain-specific, not a generic chatbot wrapper.
- It uses specialized agents for food, match intelligence, navigation, crowd data, and incidents.
- It connects the AI layer to operational data through Firestore tools.
- It includes real-time cricket match integration for contextual fan experience.
- It has a deployed frontend and backend on Cloud Run.
- It includes a judge-friendly README, reproducible setup, and verification evidence.

Important note: no README can guarantee a top-5 placement because the final result depends on judging criteria, live demo quality, competing projects, and presentation. This repository is now structured to make the idea, engineering effort, Google Cloud usage, and product polish easy to evaluate.

## Problem Statement

Modern stadiums host tens of thousands of people at once. During a match, the most common problems are simple but urgent:

- Fans waste time in long food and restroom queues.
- Entry and exit gates become crowded without early warning.
- Visitors struggle to find facilities in a large venue.
- Operators receive scattered incident reports without a unified workflow.
- Match context and venue context live in separate systems.

VenueIQ treats the stadium as an intelligent operating environment. A fan or operator can ask a normal question, and the system responds using the correct specialist agent and data source.

Example questions:

```text
What is the live score?
Where is the shortest food queue?
Which gate should I use to exit?
How do I reach a toilet near my stand?
Report a spill in Sector B.
```

## Product Experience

The project includes five major frontend surfaces.

| Route | Purpose |
| --- | --- |
| `/` | Landing page that explains VenueIQ and the match-day problem. |
| `/chat` | Streaming AI concierge interface for fan and operator queries. |
| `/dashboard` | Live venue status view for crowd, queue, security, and telemetry signals. |
| `/match` | Cricket match intelligence page with live score context. |
| `/admin` | Operator console for incidents, heatmap view, and public access QR. |

The frontend is intentionally visual because the submission is not just a backend proof of concept. It presents the idea as a product that could be used by fans, stadium operations teams, and event organizers.

## Architecture Overview

```text
Fan / Operator
    |
    v
React + Vite frontend on Cloud Run
    |
    | HTTP and streaming text responses
    v
FastAPI backend on Cloud Run
    |
    +-- Intent routing and fast deterministic responses
    |
    +-- VenueIQ Orchestrator agent
    |      |
    |      +-- FoodAgent
    |      +-- MatchAgent
    |      +-- Navigation tool
    |      +-- Crowd status tool
    |      +-- Incident reporting tool
    |
    +-- Vertex AI Gemini model endpoint
    +-- Firestore venue and incident data
    +-- CricAPI live cricket data
```

## Google Cloud Usage

VenueIQ uses Google Cloud as the production platform and AI/data foundation.

| Google Cloud service | How it is used |
| --- | --- |
| Cloud Run | Hosts the frontend static container and backend FastAPI container. |
| Cloud Build | Builds the frontend production container and pushes it to Artifact Registry. |
| Artifact Registry | Stores the Cloud Run container images. |
| Vertex AI | Runs Gemini model calls for the lightweight agent loop. |
| Firestore | Stores stadium zones, crowd data, navigation records, match seed data, and incident reports. |
| Application Default Credentials / service identity | Authenticates backend access to Vertex AI and Firestore. |

Production deployment details:

| Item | Value |
| --- | --- |
| Google Cloud project | `kaggle-5b-478308` |
| Region | `us-central1` |
| Backend service | `venueiq-backend` |
| Frontend service | `venueiq-frontend` |
| Latest verified frontend revision | `venueiq-frontend-00002-t7r` |
| Initial backend revision | `venueiq-backend-00001-4l4` |

## Agentic Design

VenueIQ uses a lightweight multi-agent framework implemented in `venueiq-backend/venueiq_agents/lightweight_lib.py`. The implementation calls Vertex AI directly through the REST `generateContent` endpoint, passes function declarations as tools, executes selected tools, appends tool responses back into conversation history, and continues until a final answer is produced.

### Agents

| Agent | Role | Tools |
| --- | --- | --- |
| `VenueIQ_Orchestrator` | Root agent for intent routing and general venue help. | `transfer_to_agent`, `get_navigation`, `report_issue`, `get_crowd_status` |
| `FoodAgent` | Handles food, beverage, queue, vendor, and restroom questions. | `get_food_court_status`, `fetch_food_vendors`, `fetch_venue_amenities` |
| `MatchAgent` | Handles score, match, stadium context, and crowd-aware match questions. | `get_match_data`, `fetch_venue_amenities`, `get_crowd_status` |
| Navigation tool | Resolves destinations and facility directions. | Firestore `navigation` collection |
| Incident tool | Writes user-reported problems to operations workflow. | Firestore `incident_reports` collection |

### Tool/Data Flow

```text
User message
    |
    v
FastAPI /chat
    |
    +-- Fast path for common match, food, and gate queries
    |
    +-- Agent path for model-based routing and tool use
            |
            +-- Vertex AI Gemini chooses a function call
            +-- Backend executes Python tool
            +-- Tool reads/writes Firestore or local context
            +-- Tool result is sent back to the model
            +-- Final user-facing answer is streamed to frontend
```

### Why the Fast Path Exists

For live demos and stadium use, latency matters. The backend includes a short TTL cache and deterministic responses for common queries such as live score, food queue, and quickest gate. This makes the most important demo paths fast and reliable while preserving the full agent path for broader requests.

## Data Model

Firestore collections used by the backend:

| Collection | Purpose |
| --- | --- |
| `venue_zones` | Food courts, toilets, amenities, wait times, menus, and occupancy context. |
| `crowd_data` | Gate density, wait times, exit recommendations, and crowd state. |
| `navigation` | Destination lookup and facility routing. |
| `match_data` | Seeded or fallback live match state. |
| `incident_reports` | Operator workflow for reported issues. |

The repository includes scripts for seeding and validating Firestore demo data:

```powershell
cd venueiq-backend
python scripts/seed_stadium.py
python scripts/seed_match_live.py
python scripts/verify_seed.py
python scripts/simulate_live.py
```

## Backend API

The backend is a FastAPI service in `venueiq-backend/main.py`.

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Health check for Cloud Run and smoke tests. |
| `POST` | `/chat` | Streams AI concierge responses. |
| `GET` | `/api/matches` | Returns transformed current cricket matches. |
| `GET` | `/api/matches/primary` | Returns the most relevant live or upcoming match. |
| `GET` | `/admin/incidents` | Lists incident reports for the operations console. |
| `PATCH` | `/admin/incidents/{incident_id}` | Updates incident status. |

Example chat request:

```powershell
$body = @{
  message = "What is the live score?"
  session_id = "demo"
  user_name = "Judge"
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri https://venueiq-backend-857911435032.us-central1.run.app/chat `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

## Live Cricket Integration

`venueiq-backend/cricket_api.py` integrates with CricAPI / CricketData.org.

It provides:

- Current match fetch through `/v1/currentMatches`.
- Detailed match info through `/v1/match_info`.
- 30-second in-memory caching to reduce API usage.
- Score transformation for frontend match components.
- Priority selection for the best match to show first.

This helps VenueIQ feel like a real match-day system instead of a static chatbot demo.

## Frontend Implementation

The frontend is a React 19 + TypeScript single-page app built with Vite.

Important files:

| File | Purpose |
| --- | --- |
| `venueiq-frontend/src/App.tsx` | Router, fixed header, route layout. |
| `venueiq-frontend/src/pages/LandingPage.tsx` | Product story and competition-facing first impression. |
| `venueiq-frontend/src/pages/ChatPage.tsx` | Streaming concierge UI. |
| `venueiq-frontend/src/pages/DashboardPage.tsx` | Venue telemetry dashboard. |
| `venueiq-frontend/src/pages/MatchPage.tsx` | Match intelligence interface. |
| `venueiq-frontend/src/pages/AdminPage.tsx` | Incident operations console and heatmap. |

The frontend reads `VITE_API_URL` at build time. The deployed Cloud Run frontend is built with:

```text
VITE_API_URL=https://venueiq-backend-857911435032.us-central1.run.app
```

## Repository Structure

```text
VenueIQ/
|-- README.md
|-- .gitignore
|-- tasks/
|   |-- todo.md
|   |-- lessons.md
|-- venueiq-backend/
|   |-- Dockerfile
|   |-- .dockerignore
|   |-- main.py
|   |-- cricket_api.py
|   |-- requirements.txt
|   |-- seed_firestore.py
|   |-- scripts/
|   |   |-- seed_stadium.py
|   |   |-- seed_match_live.py
|   |   |-- simulate_live.py
|   |   |-- verify_seed.py
|   |-- venueiq_agents/
|   |   |-- agent.py
|   |   |-- lightweight_lib.py
|   |   |-- stadium_data.json
|-- venueiq-frontend/
|   |-- Dockerfile
|   |-- .dockerignore
|   |-- cloudbuild.yaml
|   |-- nginx.conf
|   |-- package.json
|   |-- vite.config.ts
|   |-- public/
|   |-- src/
|       |-- App.tsx
|       |-- main.tsx
|       |-- pages/
|           |-- LandingPage.tsx
|           |-- ChatPage.tsx
|           |-- DashboardPage.tsx
|           |-- MatchPage.tsx
|           |-- AdminPage.tsx
```

## Local Setup

### Backend

```powershell
cd venueiq-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8080
```

Backend environment variables:

```env
GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE
CRICKETDATA_API_KEY=your-cricketdata-api-key
PORT=8080
HOST=0.0.0.0
```

Backend smoke checks:

```powershell
Invoke-RestMethod http://127.0.0.1:8080/health
Invoke-RestMethod http://127.0.0.1:8080/api/matches/primary
```

### Frontend

```powershell
cd venueiq-frontend
npm install
npm run dev
```

Optional local frontend environment:

```env
VITE_API_URL=http://localhost:8080
```

Open:

```text
http://localhost:5173
```

## Cloud Run Deployment

### Backend

The backend has its own Dockerfile:

```powershell
cd venueiq-backend
gcloud run deploy venueiq-backend `
  --source . `
  --project kaggle-5b-478308 `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars "GOOGLE_CLOUD_PROJECT=kaggle-5b-478308,GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=TRUE,CRICKETDATA_API_KEY=your-key,FAST_CACHE_TTL_SECONDS=30"
```

### Frontend

The frontend uses `cloudbuild.yaml` so the backend URL can be passed as a Docker build arg:

```powershell
cd venueiq-frontend

$image = "us-central1-docker.pkg.dev/kaggle-5b-478308/cloud-run-source-deploy/venueiq-frontend:latest"
$api = "https://venueiq-backend-857911435032.us-central1.run.app"

gcloud builds submit `
  --project kaggle-5b-478308 `
  --region us-central1 `
  --config cloudbuild.yaml `
  --substitutions "_IMAGE=$image,_VITE_API_URL=$api" .

gcloud run deploy venueiq-frontend `
  --image $image `
  --project kaggle-5b-478308 `
  --region us-central1 `
  --allow-unauthenticated
```

## Verification Evidence

Latest verified checks:

```powershell
cd venueiq-frontend
npm run lint
npm run build
```

```powershell
cd venueiq-backend
python -m py_compile main.py cricket_api.py venueiq_agents\agent.py venueiq_agents\lightweight_lib.py
```

Deployed smoke checks performed:

| Check | Result |
| --- | --- |
| Frontend `/health` | `ok` |
| Frontend `/` | HTTP 200 |
| Backend `/health` | `{"status":"ok","mode":"lightweight"}` |
| Backend `/api/matches/primary` | Successful match payload |
| Backend `/chat` with `What is the live score?` | Live-score response |
| Frontend bundle API URL | Contains deployed backend URL, not localhost |

Example deployed chat response from the smoke test:

```text
Gujarat Titans (GT) are 192/3 after 19.1 overs against Royal Challengers Bengaluru.
Live - GT batting, finishing strong in Ahmedabad! Top scorer: Shubman Gill - 84(48).
```

## Security and Secrets

The repository intentionally ignores local secrets and generated files.

Ignored examples:

- `venueiq-backend/.env`
- `node_modules/`
- `dist/`
- Python caches
- Server logs

Do not commit API keys, Twilio credentials, service account keys, or local Cloud credentials.

## Design Decisions

### Why a stadium?

A stadium is a strong agentic AI use case because it requires multiple live decisions at once: queues, movement, safety, score context, and operations. This makes it more interesting than a single-purpose chatbot.

### Why multiple agents?

Different venue questions need different tools and context. Food queue optimization, match updates, navigation, and incident handling each need separate instructions and data access. Specialist agents make the system easier to reason about and easier to extend.

### Why Cloud Run?

Cloud Run is a good fit for hackathon deployment because it supports containerized services, automatic HTTPS, scale-to-zero behavior, and fast iteration. The frontend and backend can be deployed independently.

### Why Firestore?

Firestore works well for operational venue state because it can represent live documents for zones, gates, navigation, and incidents without requiring a heavy relational schema.

### Why fast deterministic responses?

Live demos should not depend only on model latency. VenueIQ answers common high-value questions through a fast cached path first, then uses the full agent path for broader requests.

## Current Limitations

The repository is demo-ready, but a production stadium deployment would need:

- Authenticated operator access for `/admin`.
- Stronger role-based permissions for incident updates.
- Real venue IoT or turnstile integrations.
- More robust observability with structured logs and dashboards.
- Formal load testing for match-day traffic.
- Firestore security rules and service account hardening.
- UI copy cleanup in a few files that still contain historical encoding artifacts in comments or static strings.

## Future Roadmap

Potential next improvements:

- Add live map routing with crowd-aware path recommendations.
- Add multilingual fan support for Hindi, Gujarati, and English.
- Add operator alerts for predicted gate surges.
- Add incident prioritization using Gemini classification.
- Add BigQuery analytics for historical crowd and queue patterns.
- Add Firebase Authentication or Identity Platform for admin users.
- Add real QR code value pointing to the deployed frontend URL.

## Competition Review Checklist

For an Agentic Premier League reviewer or AI analyzer, the most important evidence is:

- Working deployed app: yes.
- Backend deployed on Google Cloud Run: yes.
- Frontend deployed on Google Cloud Run: yes.
- Uses Google Cloud AI: yes, Vertex AI Gemini through REST calls.
- Uses Google Cloud database: yes, Firestore.
- Has an agentic pattern: yes, root orchestrator plus specialist agents and function tools.
- Has real APIs: yes, CricAPI live cricket data and Firestore-backed venue data.
- Has a complete UI: yes, landing page, concierge, dashboard, match page, and admin console.
- Has reproducible deployment assets: yes, Dockerfiles and Cloud Build config.
- Has verification evidence: yes, local and deployed checks are documented.

## Project Status

VenueIQ is live, deployed, and ready for competition review.

Primary demo URL:

```text
https://venueiq-frontend-857911435032.us-central1.run.app
```
