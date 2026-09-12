# AI Home Intelligence Hub

> Understand your home. Improve every space.

AI Home Intelligence Hub is a premium, full-stack home-management platform. You build a digital
model of your home — rooms, furniture, appliances, lifestyle, energy, maintenance, and safety
information — and a small team of specialized AI agents turns it into an explainable,
room-by-room intelligence report with practical recommendations, a task roadmap, and interactive
what-if scenarios.

It is not a chatbot and not a generic CRUD dashboard: every score, recommendation, and floor-plan
block is derived directly from data you entered, and every AI claim is labeled as an estimate
where appropriate.

## Features

- **Guided home setup** — a 9-step wizard (profile, rooms, furniture, appliances, lifestyle,
  energy, maintenance, security, review) with save-as-you-go persistence.
- **Digital home model** — a simplified, interactive SVG floor plan built from your real room
  dimensions and furniture, with priority-room highlighting and zoom controls.
- **AI Home Intelligence System** — nine specialized agents (space planning, organization,
  energy, maintenance, comfort, safety awareness, accessibility, improvement planning,
  cost & priority) plus a validator and a critic/deduplication pass, orchestrated into one report.
- **Home Intelligence Report** — category scores (explicitly labeled as AI-generated planning
  indicators), top actions, quick wins, missing-information disclosure, and room-by-room
  breakdowns.
- **Recommendations** — filterable/sortable cards with save, complete, dismiss, copy, and
  "add to tasks" actions, all backed by real API calls.
- **What-if scenarios** — compare a proposed room change against the current state, with
  benefits, trade-offs, and required follow-up actions.
- **Tasks & roadmap** — a full task manager grouped into Today / This Week / This Month / Later.
- **Export & print** — download your home profile as JSON, print your report or roadmap using
  the browser's native print support.

## Tech stack

| Layer     | Technology                                             |
|-----------|---------------------------------------------------------|
| Backend   | Python, FastAPI, Uvicorn, Pydantic, Jinja2               |
| Frontend  | HTML, Tailwind CSS (CDN), vanilla JavaScript              |
| AI        | OpenAI Python SDK, `gpt-4.1-mini`                          |
| Storage   | Local JSON files (no database, no login)                  |

No React/Next/Vue, no separate frontend server, no Docker, and no external database — FastAPI
serves the entire application.

## Getting started

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your OpenAI API key
copy .env.example .env        # Windows
# cp .env.example .env        # macOS/Linux
# then edit .env and set OPENAI_API_KEY

# 4. Run the app
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000**.

The app runs and every non-AI feature (home setup, rooms, furniture, tasks, export) works
without an API key. AI features (Analyze Home, Analyze Room, scenario comparison, energy/
maintenance/organization plans) require a valid `OPENAI_API_KEY` in `.env` — without one they
fail gracefully with a clear, non-technical error message instead of crashing.

## Project structure

```text
app/
├── main.py                  # FastAPI app, router wiring, 404 handler
├── templates_config.py      # Shared Jinja2Templates instance
├── routes/                  # pages, home, rooms, insights, ai, recommendations, tasks, feedback
├── agents/                  # orchestrator + 10 specialized sub-agents + home_validator
├── services/                # openai_service + home/room/recommendation/task/maintenance services
├── models/                  # Pydantic models (one file per domain concept)
├── data/                    # seed reference JSON + local JSON "database" (app/data/store/)
└── utils/                   # ids, dates, validation, helpers

templates/                   # Jinja2 page templates (extend base.html)
static/
├── css/styles.css           # Custom styles beyond Tailwind utilities
└── js/                      # main.js (shared) + one file per page
```

## AI architecture

```text
Home Profile
     ↓
Home Data Validator
     ↓
Home Intelligence Orchestrator
     ↓
 space_planning · organization · energy · maintenance
 comfort · safety · accessibility
     ↓
 critic_agent (dedupe/validate) → priority_agent (rank) → improvement_agent (sequence)
     ↓
Structured Home Intelligence Report
```

Every sub-agent degrades gracefully: if the OpenAI API is unavailable or unconfigured, it
returns an empty, clearly-flagged section (`succeeded: false`) instead of raising, so the rest
of the report still renders as a partial result.

## Data & privacy

There is no login. Your home profile lives in local JSON files under `app/data/store/`
(git-ignored) and is fully exportable as JSON from **Settings**. Nothing is synced to a cloud
account.

## Limitations

AI recommendations are informational planning suggestions, not measurements or guarantees.
Energy figures are estimates, not utility-grade calculations. The safety-awareness feature is
general guidance, not a professional security assessment. Structural, electrical, gas, and major
construction work always requires a qualified professional.

## Author

Built by **Maryam Mumtaz** — Full Stack Developer & AI Agent Engineer.
[Portfolio](https://maryam-piaic.vercel.app) · [GitHub](https://github.com/MaryamMumtaz-piaic) ·
[LinkedIn](https://www.linkedin.com/in/maryammumtaz-)

## License

MIT — see [LICENSE](LICENSE).
