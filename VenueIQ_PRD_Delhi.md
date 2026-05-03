# VenueIQ — Product Requirements Document
## Google Cloud Build With AI :: Agentic Premier League, Delhi
## Problem Statement 3 — Stadium Gate Advisory + Live Updates Platform
### Date: 3rd May 2026 | Solo Submission | Dinesh Kumar Bingi

---

## PROBLEM STATEMENT (Verbatim)

"An application to issue advisories on which gates of the stadium are
overcrowded and which gates people should use preferably, with live updates.
People can also post, and the organizers can post updates for the cricket
match."

---

## WHAT JUDGES ARE LOOKING FOR IN PS3

Three things are explicitly in the problem statement:

1. Gate overcrowding advisories with live updates
2. Attendees can post updates
3. Organizers can post updates

VenueIQ covers all three and goes significantly beyond each one.
That delta — between what was asked and what was built — is the winning gap.

---

## PRODUCT OVERVIEW

VenueIQ is a real-time stadium intelligence platform powered by Google
Gemini. It transforms the chaotic experience of attending a large cricket
match into a guided, frictionless journey for every attendee.

The platform operates on three simultaneous layers:

Layer one is the AI Concierge — a natural language chat interface where any
attendee can ask anything about the venue and receive a specific, live,
actionable answer in under three seconds.

Layer two is the Live Intelligence Dashboard — a real-time view of all gate
conditions, food court queues, toilet availability, and venue-wide crowd
density, updating every thirty seconds.

Layer three is the Community + Organizer Feed — a live social layer where
attendees post what they see on the ground and organizers push official
advisories, creating a crowd-sourced and authority-sourced stream of truth.

---

## THE UNIQUE INSIGHT

Every other team will build a gate status board. A table showing green,
yellow, red per gate. That is a database with a UI.

VenueIQ is different in one fundamental way: it does not just show you data.
It reasons about that data using AI and tells you exactly what to do.

"Gate 1 is red" tells you nothing actionable.

"Gate 1 is at 9 minute wait and rising. Gate 4 is clear at 2 minutes and
is 180 metres from your current stand. Leave now via the north concourse
aisle and you will exit before the post-match rush" tells you everything.

The AI layer is what separates VenueIQ from a dashboard.

---

## GOOGLE SERVICES USED

### Gemini 1.5 Pro
Role: Orchestrator agent. Reads all incoming user queries, determines which
specialist agent to route to, synthesises multi-agent responses into a
single coherent answer, and injects venue context into every response.

### Gemini 1.5 Flash
Role: Three specialist sub-agents running in parallel. Food Agent handles
queue times, menu, and food court recommendations. Navigation Agent handles
step-by-step directions to any venue facility. Crowd Agent handles gate
conditions, density analysis, and exit route recommendations. A fourth Match
Agent handles live score, batting, bowling, pitch, and prediction queries.

### Google Agent Development Kit (ADK)
Role: The multi-agent orchestration framework. ADK manages the routing
logic, agent-to-agent communication, session state, and tool registration.
This is the architectural layer that makes VenueIQ genuinely agentic rather
than a simple Gemini API call.

### Cloud Firestore
Role: The real-time database powering all live data. Stores venue zone
occupancy, gate crowd density, navigation routes, match events, live scores,
community posts, organizer advisories, proactive alerts, and incident
reports. All frontend components listen to Firestore collections using
onSnapshot for zero-latency updates.

### Cloud Run
Role: Serverless container hosting for both the FastAPI backend and the
React frontend. Auto-scales to handle peak load during match events. No
server management required.

### Cloud Build
Role: CI/CD pipeline. On every push to the main branch, Cloud Build
automatically rebuilds and redeploys both services to Cloud Run.

### Firebase Authentication
Role: Handles three user roles. Attendees authenticate anonymously or via
Google Sign-In. Staff authenticate via email and password. Organizers
authenticate via a privileged email domain. Role is stored in Firestore
user documents and checked on every write operation.

### Vertex AI
Role: Hosts the Gemini model endpoints used by the ADK agents. All Gemini
API calls in production route through Vertex AI for quota management,
logging, and enterprise reliability.

### Antigravity (GCP $5 Credit Integration)
Role: Used to claim and manage the development GCP credits. The project is
configured under the Antigravity-provisioned project ID to utilise the
provided trygcp.dev credit.

---

## CORE FEATURES

### Feature 1 — Gate Advisory System (Direct PS3 Answer)

The primary feature explicitly required by the problem statement.

Every gate in the stadium has a live document in Firestore containing:
current density level, entry wait in minutes, exit wait in minutes, staff
count deployed, a recommendation sentence, and a last updated timestamp.

The Live Dashboard displays all gates in a grid. Each gate card shows its
name, current density as a colour-coded pill (clear in emerald, moderate in
amber, congested in red, critical in deep red), the exact wait time in
minutes, and the AI-generated recommendation text.

The recommendation text is not static. It is generated by the Crowd Agent
using Gemini based on three inputs: the current density of this gate, the
densities of all adjacent gates, and the user's current stand location if
provided. The result is a specific sentence telling the user exactly which
alternative to use and why.

Example output: "Gate 9 is at critical density with a 13 minute wait.
Use Gate 8 instead — currently 3 minute wait, same BPCL Stand access,
180 metres west of your current position."

Updates every 30 seconds via the simulation engine and via staff reports.

### Feature 2 — Community Post Feed (Direct PS3 Answer)

Attendees can post live updates from anywhere in the stadium. This is the
crowd-sourced intelligence layer.

Any logged-in attendee opens the Community tab and types what they see.
"Toilet near Gate 6 is broken", "Gate 3 queue is moving fast now",
"Food court near gate 4 is empty go now", "Accident near section C".

Each post contains: the post text, the author's display name, their
current stand or gate (optional), a timestamp, a type tag (crowd report,
food tip, gate update, safety), and a helpful votes counter.

Posts are stored in the community_posts Firestore collection. The frontend
listens with onSnapshot and renders new posts in real time without page
refresh. Posts are displayed newest first in a scrollable feed.

The AI layer reads community posts passively. When a post about a specific
gate or zone appears and that post receives three or more helpful votes,
the Crowd Agent is triggered to cross-reference the post content against
the current Firestore zone data. If the post reveals a discrepancy — for
example the community says Gate 3 is clear but Firestore shows it as busy
— the agent flags it for organizer review and optionally adjusts the
displayed status with a "Community report: possibly clearing" annotation.

### Feature 3 — Organizer Advisory Board (Direct PS3 Answer)

Organizers have a privileged posting interface that creates official
advisories. These are visually distinct from community posts — they display
with a verified badge, a different background, and appear pinned at the top
of the feed.

Organizer advisories can be targeted: stadium-wide, specific stand,
specific gate, or specific zone type such as all food courts. Targeted
advisories also update the relevant Firestore zone documents automatically
— so if an organizer posts "Gate 7 is now closed for maintenance", the
Gate 7 document status updates to closed and the AI agents immediately
begin routing all users to alternative gates.

The organizer interface is a separate authenticated page accessible only
to users with the organizer role. It includes a post composer, a gate
status override panel (manually set any gate to any status with one click),
an incident management board, and a live view of current community posts
for monitoring.

### Feature 4 — AI Concierge Chat (Beyond PS3)

The natural language interface. Any attendee types a question in plain
English and the multi-agent system provides a specific, live answer.

This feature goes beyond what PS3 asked for. PS3 asked for advisories.
VenueIQ delivers advisories proactively AND responds to individual queries
with contextualised, actionable intelligence.

Example queries the system handles:
"Which gate should I use to exit quickly after the match?"
"Where can I eat near Gate 4 with less than 5 minute wait?"
"How do I get from Stand C to the first aid room?"
"What's the score? How many overs left?"
"The toilet near section B is overflowing, can you report it?"

### Feature 5 — Predictive Surge Intelligence (Beyond PS3)

VenueIQ does not just report the present. It predicts the near future.

The prediction engine reads occupancy velocity (how fast each zone is
filling) and cross-references it with the match event timeline (drinks
break in 6 minutes means food courts will spike by 40 percent within 8
minutes of the break starting).

The dashboard shows a Smart Predictions panel with four live values:
best food court right now, best food court in 10 minutes, next crowd surge
event and minutes until it occurs, and recommended exit gate in 10 minutes
rather than right now.

The chat interface also uses predictions. When a user asks about food, the
Food Agent checks predictions before answering and warns if a quiet court
is about to get packed.

### Feature 6 — Proactive Alerts (Beyond PS3)

VenueIQ pushes alerts to users without them asking.

When a gate suddenly clears, a food court empties, or a match event is
three minutes away, an alert notification slides into the app from the
right side of the screen.

Alerts are delivered via Server-Sent Events from the FastAPI backend. The
alert engine monitors Firestore continuously and fires alerts when threshold
crossing events occur: gate wait crosses eight minutes upward, food court
occupancy drops below 35 percent, match event is within three minutes.

This is the feature that turns VenueIQ from a dashboard into a live
personal assistant.

### Feature 7 — Staff Natural Language Reporting (Beyond PS3)

Stadium stewards report conditions by typing plain English into the staff
portal. Gemini parses the report, extracts the structured update, applies
it to the relevant Firestore document, and triggers user-facing alerts
if appropriate.

A steward types: "Gate 5 just got really crowded after the wicket fell,
queue going outside the lobby." Gemini identifies Gate 5, sets density to
high, updates entry wait to 9 minutes, and fires an advisory to all users
whose recommended gate is Gate 5.

This closes the operational loop: physical reality observed by humans →
natural language → AI parsing → structured data → instant user impact.

---

## SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACES                       │
│                                                          │
│  Attendee Web App        Staff Portal      Organizer     │
│  (React + Vite)          (React)           Panel         │
│  Cloud Run               Cloud Run         Cloud Run     │
└──────────────┬───────────────┬─────────────────┬────────┘
               │               │                 │
               ▼               ▼                 ▼
┌─────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND                        │
│                   Cloud Run                              │
│                                                          │
│  /chat          /alerts/stream    /staff/report          │
│  /venue/status  /alerts/current   /organizer/post        │
│  /community     /predictions      /staff/incidents       │
└──────────────────────────┬──────────────────────────────┘
                           │
               ┌───────────┴────────────┐
               ▼                        ▼
┌──────────────────────┐   ┌────────────────────────────┐
│   ADK AGENT LAYER    │   │      FIRESTORE DATABASE     │
│   Vertex AI          │   │                             │
│                      │   │  stadiums                   │
│  Orchestrator        │   │  venue_zones                │
│  (Gemini 1.5 Pro)    │   │  crowd_data                 │
│       │              │   │  navigation_routes          │
│  ┌────┴──────────┐   │   │  match_live_data            │
│  ▼    ▼    ▼    ▼│   │   │  match_events               │
│  F    N    C    M │   │   │  community_posts            │
│  o    a    r    a │   │   │  organizer_advisories       │
│  o    v    o    t │   │   │  proactive_alerts           │
│  d    i    w    c │   │   │  incident_reports           │
│       g    d    h │   │   │  venue_predictions          │
│       a         │ │   │   │  user_profiles              │
│       t         │ │   │   └────────────────────────────┘
│       i         │ │   │
│       o         │ │   └──────── Firebase Auth ─────────
│       n         │ │
└─────────────────┴─┘
               │
               ▼
┌──────────────────────────────┐
│     BACKGROUND SERVICES      │
│     (run in parallel)        │
│                              │
│  simulate_live.py            │
│  prediction_engine.py        │
│  alert_engine.py             │
└──────────────────────────────┘
```

---

## DATA MODELS

### stadiums collection
One document per stadium. Contains name, city, capacity, current
attendance, total gates, total stands, coordinates, active match name,
match phase, and facility counts.

### venue_zones collection
One document per zone. Type field is one of: food, toilet, medical,
merchandise, atm. Contains zone name, stand, level, nearest gate,
coordinates as plain text directions, capacity, current occupancy,
wait minutes, status (quiet/busy/packed/critical/closed), menu items
for food zones, staff count for medical zones, accepts UPI boolean,
last updated timestamp, occupancy five minutes ago for velocity
calculation, predictions sub-object with five, ten, and fifteen minute
forecasts, is available boolean, staff reported issue string.

### crowd_data collection
One document per gate. Contains gate number, display name, compass
position, stand served, density (low/medium/high/critical), entry wait
minutes, exit wait minutes, staff deployed, is VIP only boolean,
current status (clear/congested/critical/closed), recommendation text,
previous entry wait for velocity tracking, last updated timestamp.

### community_posts collection
One document per post. Contains post text, author ID, author display
name, stand or gate location (optional), type tag, helpful votes array
of user IDs, created at timestamp, is flagged boolean, AI reviewed
boolean.

### organizer_advisories collection
One document per advisory. Contains title, body, severity (info/
warning/critical), target type (stadium/stand/gate/zone-type),
target value, author display name, created at timestamp, is pinned
boolean, auto-updates-zone boolean, linked zone IDs array.

### proactive_alerts collection
One document per alert. Contains type, severity, title, message,
affected zone IDs, action label, created at, expires at, shown count.

### match_live_data collection
One document per match. Contains all live match state including scores,
wickets, overs, current batters, current bowlers, key moments, pitch
report, weather, and prediction.

### venue_predictions collection
One document with ID "current". Contains best food now, best food in
ten minutes, best gate now, best gate in ten minutes, next surge event,
last calculated timestamp.

### incident_reports collection
One document per incident. Created by staff portal submissions.
Contains original report text, Gemini parsed result, reported by,
reported at, status (open/resolved), resolved at.

---

## API ENDPOINTS

POST /chat
Accepts message string, session ID, user name. Routes through ADK
orchestrator. Returns AI response string and session ID.

GET /venue/status
Returns current summary of all gates and food courts. Used for
dashboard initial load and judge-facing demo.

GET /alerts/stream
Server-Sent Events stream. Polls proactive alerts collection every
three seconds. Yields non-expired alerts as SSE data events.

GET /alerts/current
Returns five most recent non-expired alerts as JSON. Used for initial
page load.

POST /community/post
Accepts post text, author ID, stand location, type tag. Writes to
community posts collection. Returns post ID.

POST /community/vote
Accepts post ID and user ID. Adds user to helpful votes array if not
already present. Returns updated vote count.

POST /organizer/advisory
Authenticated organizer only. Accepts advisory content and targeting.
Writes to organizer advisories collection. If auto update zone is true,
updates linked zone documents. Returns advisory ID.

POST /organizer/gate-override
Authenticated organizer only. Accepts gate ID and new status. Directly
updates crowd data document. Bypasses simulation. Triggers alert engine.

POST /staff/report
Accepts report text and staff ID. Calls Gemini to parse report. Updates
relevant Firestore documents. Triggers alert engine. Returns confirmation.

GET /staff/incidents
Returns twenty most recent open incident reports.

GET /predictions/current
Returns current venue predictions document.

---

## BACKGROUND PROCESSES

### simulate_live.py
Runs continuously. Every thirty seconds: reads all venue zones and
crowd data documents, applies random occupancy deltas clamped within
capacity bounds, recalculates wait times and statuses, saves previous
occupancy to occupancy five minutes ago field, writes all updates in
a single batch, then calls prediction engine and alert engine.

In demo mode (activated by environment variable) runs every five
seconds and auto-fires one alert of each type in sequence.

### prediction_engine.py
Called at end of each simulation loop. Reads occupancy velocities,
fetches upcoming match events within twenty minutes, calculates
predicted occupancy at five, ten, and fifteen minutes per zone,
writes predictions back to zone documents, writes summary to venue
predictions collection.

### alert_engine.py
Called at end of each simulation loop with current state data. Applies
five trigger rules: surge warning when a zone is about to spike,
opportunity when a zone clears, match event when an event is under
three minutes away, exit window when a gate suddenly clears, critical
crowd when a gate reaches critical density. Creates alert documents.
Cleans expired alerts.

---

## USER ROLES AND PERMISSIONS

### Attendee
Authenticated via anonymous Firebase Auth or Google Sign-In.
Can read all venue data, gate conditions, predictions, and alerts.
Can use AI chat concierge.
Can post community updates.
Can vote on community posts.
Cannot write to venue zones, crowd data, or organizer collections.

### Staff
Authenticated via email and password, staff role in user profile.
All attendee permissions.
Can submit staff reports via natural language portal.
Can view incident reports.
Cannot post organizer advisories.
Cannot override gate statuses directly.

### Organizer
Authenticated via privileged email, organizer role in user profile.
All staff permissions.
Can post official advisories with stadium-wide or targeted reach.
Can directly override any gate or zone status.
Can resolve incident reports.
Can view all community posts including flagged ones.
Can pin or remove community posts.

---

## DEMO FLOW FOR JUDGES (5 minutes)

Minute one: Open the landing page. Explain the problem in two sentences.
"At IPL, 84,000 fans have no real-time guidance. VenueIQ fixes that."
Show the story scroll cards. Let the visual tell the scale of the problem.

Minute two: Navigate to Live Dashboard. Show the gate grid — some red,
some green. Point to Gate 1 in red and Gate 4 in green. Show that the
AI recommendation text under Gate 1 says specifically "Use Gate 4 —
2 minute wait, same stand access, 180m west." Open Firebase Console in
a side window. Show the actual Firestore documents with real data.

Minute three: Navigate to Concierge chat. Type "Which gate should I
use after the match?" Let Gemini respond live. The response names a
specific gate with specific reasoning from real data. Then type "What's
the score?" Match Agent responds with Shubman Gill's live run tally.
Judges see two completely different agent types answering two completely
different questions from the same chat interface.

Minute four: Show the Community Feed. Type a post as an attendee —
"Gate 3 queue just cleared, moving fast now." Post appears instantly.
Switch to the Organizer Panel in a second tab. Post an official advisory
— "Gate 9 temporarily closed. Use Gate 8." Show it appear in the feed
with the verified badge. Show the Gate 9 Firestore document update
automatically. Show the alert notification slide in from the right.

Minute five: Show simulate_live.py running in a terminal. Numbers
ticking. Dashboard updating live in the browser. Explain the prediction
panel — "This court is quiet now but will be packed in 8 minutes
because drinks break starts in 6 minutes." That is the prediction
engine at work. Close with one line: "This is not a dashboard.
This is a live operating system for the stadium."

---

## WHY THIS WINS

PS3 asked for three things: gate advisories, attendee posts, organizer
posts. Every team will build those three things.

VenueIQ builds those three things AND adds: a multi-agent AI concierge
that reasons in natural language, a predictive intelligence engine that
sees the future, a proactive alert system that messages users without
being asked, and a staff reporting loop that closes the gap between
physical reality and digital data.

The evaluation criteria are innovation, impact, and execution.

Innovation: multi-agent ADK architecture is the most advanced AI
pattern possible in this context. Nobody else in the room is using ADK.

Impact: the problem of crowd management at large events is real,
measurable, and affects tens of thousands of people simultaneously.
The solution demonstrably reduces wasted time and improves safety.

Execution: the system is fully deployed on Google Cloud, connected to
real Firestore data, visually polished, and demonstrable end-to-end
in five minutes with no preparation required.

---

## SUBMISSION CHECKLIST

Commudle post at commudle.com/builds with project name VenueIQ,
problem statement 3, GitHub repository link, live Cloud Run URL,
brief description of what was built and which Google services were used.

LinkedIn post (optional) with project screenshot, GitHub link,
tags for GDG Cloud New Delhi and GDG New Delhi,
hashtag BWAI-APL-DELHI.

GitHub repository must contain: all source code, README with setup
instructions, architecture diagram, and the seed data script.

Live demo URL must be accessible without login for the basic dashboard
and gate advisory view. The AI chat must be accessible after anonymous
sign-in which completes in one click.

---

*VenueIQ | Built by Dinesh Kumar Bingi*
*Google Cloud Build With AI :: Agentic Premier League | Delhi | 3rd May 2026*
*Stack: Gemini 1.5 Pro + Flash | Google ADK | Cloud Firestore | Cloud Run*
*Firebase Auth | Vertex AI | React | FastAPI | Python*
