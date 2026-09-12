# CLAUDE.md

Guidance for Claude Code (or any AI agent) working in this repository.

## What this project is

AI Home Intelligence Hub — a FastAPI + Jinja2 + Tailwind (CDN) + vanilla JS web app that lets a
user model their home (rooms, furniture, appliances, lifestyle, energy, maintenance, security)
and get an explainable AI-generated intelligence report and recommendations. Full feature spec
lives in `task.md` at the repo root — read it before making product decisions.

No login, no database — a single-user app backed by local JSON files under `app/data/store/`
(git-ignored) via `app/services/json_store.py`.

## Run it

```bash
pip install -r requirements.txt
copy .env.example .env   # then set OPENAI_API_KEY
uvicorn app.main:app --reload --port 8000
```

## Architecture

- `app/models/` — Pydantic models, one file per domain concept (home, room, furniture,
  appliance, lifestyle, energy, security, maintenance, recommendation, analysis, scenario, task,
  feedback, common enums). These are the source of truth for field names/shapes — read them
  before touching routes, services, or agents.
- `app/services/json_store.py` — the only place that reads/writes JSON files. Collections:
  `homes` (rooms/furniture/appliances nested inside), `recommendations`, `tasks`,
  `maintenance_items` (flat, each referencing a `home_id`).
- `app/services/*_service.py` — CRUD logic per domain, built on `json_store` + the Pydantic
  models. Routes should never touch `json_store` directly — go through a service.
- `app/agents/` — the AI layer. `orchestrator.py` is the entry point routes call
  (`analyze_home`, `analyze_room`, `generate_recommendations`, `compare_scenario`,
  `energy_insights`, `maintenance_plan`, `organization_plan`). Each of the nine sub-agents
  (`space_planning_agent.py`, `organization_agent.py`, `energy_agent.py`,
  `maintenance_agent.py`, `comfort_agent.py`, `safety_agent.py`, `accessibility_agent.py`,
  `improvement_agent.py`, `priority_agent.py`) plus `critic_agent.py` and `home_validator.py`
  has one clear responsibility and must never raise — on failure it returns a partial result with
  `succeeded: False`. See `AGENTS.md` for the full agent contract.
- `app/services/openai_service.py` — the only file that imports the `openai` SDK. Exposes
  `chat_json(system_prompt, user_prompt) -> dict`, raising `OpenAIServiceError` (never a raw
  provider exception) on any failure. Reads `OPENAI_API_KEY` / `OPENAI_MODEL` from the
  environment via `python-dotenv`.
- `app/routes/` — one FastAPI router per concern (`pages`, `home`, `rooms`, `insights`, `ai`,
  `recommendations`, `tasks`, `feedback`), each exporting `router`, included in `app/main.py`.
  Page routes render Jinja2 shells with minimal context; every page fetches its real data
  client-side from `/api/...` — see the per-page `static/js/*.js` file.
- `templates/` + `static/` — Jinja2 templates extending `base.html`, Tailwind loaded via CDN
  with an inline `tailwind.config` (see `base.html` `<head>`), custom CSS only for what
  utilities can't express (`static/css/styles.css`), one JS file per page plus shared
  `static/js/main.js` (toast system, modal helper, fetch wrapper `HomeHub.apiGet/apiPost/...`).

## Conventions to follow

- **Never call the OpenAI SDK outside `app/services/openai_service.py`.** Agents call
  `chat_json`; nothing else touches `openai` directly.
- **Never let an agent or route leak a raw exception, stack trace, or provider error to the
  client.** AI routes catch failures and return the exact message specified in `task.md` §37.
- **Recommendation-shaped dicts** (see `AGENTS.md`) are the common currency between agents,
  services, and the `Recommendation` model — keep field names and enum values (from
  `app/models/common.py`) in sync across all three.
- **Cost/savings language must be hedged** ("potential", "estimated", "possible") and
  `estimated_cost.is_estimate` must always be `True` — this is a product requirement, not a
  style preference (`task.md` §35–36).
- Room-level AI calls (`analyze_room`) must only send that room's data plus minimal home
  context — never the full home profile — for both cost and privacy reasons.
- When adding a new page: add the route in `app/routes/pages.py`, the template extending
  `base.html`, and a same-named JS file that fetches its data from existing (or new)
  `/api/...` endpoints — don't thread new data through Jinja context if a fetch call can do it.

## Testing

There's no formal test suite yet. Before considering a change done, at minimum:

```bash
python -c "from app.main import app"          # imports cleanly
node --check static/js/<file>.js              # any JS you touched has no syntax errors
```

and exercise the relevant flow with `fastapi.testclient.TestClient` (create home → add room →
add furniture/appliance → analyze → recommendations → tasks) if you touched routes/services/
agents.
