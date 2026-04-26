# VenueIQ

VenueIQ is an AI-powered smart venue intelligence system built for Agent Premier League 2026 as part of the Build with AI program in collaboration with Google Cloud.

The project models a match-day experience at Narendra Modi Stadium, Ahmedabad. It combines a React frontend, a FastAPI backend, Google Cloud Vertex AI, Firestore-backed venue data, and live cricket-score integration to help fans and operators make better decisions inside a crowded stadium.

## What VenueIQ Does

VenueIQ acts as a real-time intelligence layer for large venues. A fan can ask natural-language questions such as:

- "Where is the shortest food queue?"
- "What is the live score?"
- "Which gate should I use to exit?"
- "How do I reach a toilet near my stand?"
- "Report a spill in Sector B."

The backend routes these questions through a lightweight multi-agent system. Each specialized agent can query venue data, match data, crowd density, navigation records, or incident reports, then stream a concise response back to the frontend.

## Repository Structure

```text
VenueIQ/
├── venueiq-backend/
│   ├── main.py                         # FastAPI app and API routes
│   ├── cricket_api.py                  # CricAPI integration and match transformers
│   ├── requirements.txt                # Backend Python dependencies
│   ├── seed_firestore.py               # Firestore seed helper
│   ├── test_*.py                       # Backend smoke/debug scripts
│   ├── scripts/
│   │   ├── seed_stadium.py             # Detailed venue data seeding
│   │   ├── seed_match_live.py          # Match data seed helper
│   │   ├── simulate_live.py            # Live data simulation helper
│   │   └── verify_seed.py              # Firestore seed verification
│   └── venueiq_agents/
│       ├── agent.py                    # VenueIQ root agent and specialist agents
│       ├── lightweight_lib.py          # Lightweight Vertex AI function-calling loop
│       └── stadium_data.json           # Local reference stadium data
├── venueiq-frontend/
│   ├── src/
│   │   ├── App.tsx                     # React router and shared layout
│   │   ├── main.tsx                    # React entrypoint
│   │   └── pages/
│   │       ├── LandingPage.tsx         # Product story and feature overview
│   │       ├── DashboardPage.tsx       # Live venue telemetry dashboard
│   │       ├── MatchPage.tsx           # Cricket scoreboard experience
│   │       ├── ChatPage.tsx            # Streaming AI concierge UI
│   │       └── AdminPage.tsx           # Operations console
│   ├── public/                         # Stadium, crowd, dashboard, and venue images
│   ├── package.json                    # Frontend scripts and dependencies
│   └── vite.config.ts                  # Vite config
├── tasks/
│   ├── todo.md                         # Work log for this documentation/release pass
│   └── lessons.md                      # Correction patterns, currently empty
├── .gitignore
└── README.md
```

## Architecture

```text
User / Operator
      |
      v
React + Vite frontend
      |
      | HTTP / streaming text
      v
FastAPI backend
      |
      +--> VenueIQ root agent
      |       |
      |       +--> FoodAgent
      |       +--> Navigation tools
      |       +--> MatchAgent
      |       +--> Crowd and incident tools
      |
      +--> Firestore venue data
      +--> Vertex AI Gemini model endpoint
      +--> CricAPI current match data
```

### Frontend

The frontend is a React 19 and TypeScript single-page app built with Vite. Routing is defined in `venueiq-frontend/src/App.tsx`.

Routes:

- `/` - Landing page with the project story, problem framing, and capability overview.
- `/dashboard` - Live venue status view for attendance, queue velocity, zone load, crowd flow, and security status.
- `/match` - Cricket match page with scoreboard, pitch intelligence, over analysis, batting ledger, and event ticker.
- `/chat` - AI concierge terminal that streams responses from the backend.
- `/admin` - Operator console with incident tracking, heatmap view, and QR access node.

The chat and admin pages use `VITE_API_URL` when present and default to `http://localhost:8080`.

### Backend

The backend is a FastAPI service in `venueiq-backend/main.py`.

Primary routes:

- `GET /health` - health check.
- `POST /chat` - streams AI concierge responses.
- `GET /api/matches` - returns transformed current cricket matches.
- `GET /api/matches/primary` - returns the highest-priority live or upcoming match.
- `GET /admin/incidents` - lists incident reports for the operations console.
- `PATCH /admin/incidents/{incident_id}` - updates incident status.

The backend loads environment variables with `python-dotenv`, uses Firestore for venue state, calls Vertex AI for Gemini generation, and uses `httpx` for CricAPI calls.

### Agent Workflow

The agent layer lives in `venueiq-backend/venueiq_agents/`.

1. `VenueIQ_Orchestrator` receives the user message.
2. The root agent decides whether the request is about food, navigation, match data, crowd status, or incidents.
3. Tool calls fetch data from Firestore collections such as `venue_zones`, `crowd_data`, `navigation`, `match_data`, and `incident_reports`.
4. Food and match requests can transfer to specialist agents.
5. The backend filters internal transfer text and streams only user-facing response chunks to the frontend.

## Features

- AI concierge for stadium questions.
- Multi-agent routing for food, match, crowd, navigation, and incident tasks.
- Streaming chat responses in the browser.
- Live cricket match endpoints using CricAPI with short in-memory caching.
- Firestore-backed stadium data for venue zones, crowd status, navigation, match data, and incident reports.
- Operator admin console for incident triage.
- Visual stadium dashboard with crowd-density, gate, security, and telemetry views.
- QR access page for public concierge entry.
- Firestore seed and simulation scripts for demo data.

## Google Cloud Usage

VenueIQ is designed around Google Cloud services:

- Vertex AI: Gemini model calls for the concierge and specialist agents.
- Firestore: real-time venue, crowd, navigation, match, and incident data.
- Application Default Credentials or service credentials: authentication for Google Cloud APIs.

Expected backend environment variables:

```env
GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id
GOOGLE_CLOUD_LOCATION=us-central1
CRICKETDATA_API_KEY=your-cricapi-key
```

## Local Setup

### 1. Backend

```powershell
cd venueiq-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8080
```

Check the API:

```powershell
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/api/matches
curl http://127.0.0.1:8080/api/matches/primary
```

### 2. Frontend

```powershell
cd venueiq-frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

Optional frontend environment:

```env
VITE_API_URL=http://localhost:8080
```

## Data Seeding Workflow

The backend includes scripts for populating and validating Firestore demo data.

```powershell
cd venueiq-backend
python scripts/seed_stadium.py
python scripts/seed_match_live.py
python scripts/verify_seed.py
python scripts/simulate_live.py
```

Use these scripts after configuring Google Cloud credentials and the `GOOGLE_CLOUD_PROJECT` environment variable.

## Development Workflow

1. Start the backend on port `8080`.
2. Start the frontend on port `5173`.
3. Seed Firestore if the agent needs live venue data.
4. Use `/chat` for fan-facing AI interactions.
5. Use `/admin` for operations and incident management.
6. Use `/dashboard` and `/match` for venue and match visualizations.

## Verification

The current repository has been checked with:

```powershell
cd venueiq-frontend
npm run lint
npm run build
```

```powershell
cd venueiq-backend
python -m py_compile main.py cricket_api.py venueiq_agents\agent.py venueiq_agents\lightweight_lib.py
python -c "import main; print(main.app.title); print([r.path for r in main.app.routes])"
```

Frontend lint and production build pass. Backend syntax compilation and FastAPI route import pass. Full live AI and Firestore behavior requires valid Google Cloud credentials and seeded Firestore data.

## Fixes Made During Review

- Restored missing `LandingPage.css`, which was breaking the frontend production build.
- Fixed quick-query chat buttons so they submit the selected query instead of stale input.
- Switched chat API access to `VITE_API_URL` with a localhost fallback.
- Added the missing backend `asyncio` import for agent tool execution.
- Added `/admin/incidents` and `/admin/incidents/{incident_id}` routes used by the admin console.
- Updated the backend API smoke script to target `/api/matches`.
- Added a root `.gitignore` to keep `.env`, `node_modules`, build output, logs, and Python caches out of git.

## Notes

- `venueiq-backend/.env` is intentionally ignored because it may contain API keys or project credentials.
- `venueiq-frontend/node_modules` and generated build output are intentionally ignored.
- Some UI copy in the existing source contains mojibake artifacts from earlier encoding issues. The app now builds, but a future cleanup pass should normalize those strings for production polish.
