# AGENTS.md

This document describes the AI Home Intelligence System — the multi-agent architecture that
powers analysis and recommendations in this app. It is the contract every agent module in
`app/agents/` follows.

## Pipeline

```text
HomeProfile (dict)
        ↓
home_validator.validate_home()          — pure Python, no model call
        ↓
Home Intelligence Orchestrator (orchestrator.py)
        ↓
 ┌──────────────────────────────────────────────────────────────────┐
 │ space_planning_agent   organization_agent   energy_agent          │
 │ maintenance_agent      comfort_agent        safety_agent          │
 │ accessibility_agent                                               │
 └──────────────────────────────────────────────────────────────────┘
        ↓ (merged recommendation-shaped dicts)
critic_agent.review()          — dedupe, drop malformed entries, cap unsafe claims
        ↓
priority_agent.prioritize()    — rank by impact/effort/cost/urgency
        ↓
improvement_agent.build_plan() — sequence into quick wins / low-cost / medium / larger projects
        ↓
Structured result → app/routes/ai.py → HomeIntelligenceReport / RecommendationList
```

`orchestrator.py` is the only module routes import from `app/agents/`.

## Agent responsibilities

| Agent | Analyzes | Calls the model? |
|---|---|---|
| `home_validator` | Missing/incomplete fields across the whole profile | No — pure Python |
| `space_planning_agent` | Room dimensions, furniture sizes/placement, movement paths | Yes |
| `organization_agent` | Storage availability, clutter patterns, room purpose | Yes |
| `energy_agent` | Energy profile, appliance usage, cooling/heating habits | Yes |
| `maintenance_agent` | Appliance age/condition, maintenance records | Yes |
| `comfort_agent` | Natural light, layout, noise/ventilation, preferences | Yes |
| `safety_agent` | Entry points, alarms, exits, safety equipment | Yes |
| `accessibility_agent` | Layout, movement paths, stated accessibility needs | Yes |
| `improvement_agent` | Already-generated recommendations → sequenced roadmap | No — deterministic Python |
| `priority_agent` | Already-generated recommendations → ranked order | No — deterministic Python |
| `critic_agent` | Merged recommendation list → dedupe/validate | No — deterministic Python |

`improvement_agent`, `priority_agent`, and `critic_agent` are intentionally deterministic
Python rather than a second model call: ranking, sequencing, and deduplication need to be
reliable and reproducible, and keeping them model-free means the pipeline still produces a
sensible, ordered result even when every AI sub-agent has failed.

## The recommendation-shaped dict

Every sub-agent that calls the model returns recommendations in exactly this shape (see
`app/agents/_shared.py::normalize_recommendations`, which cleans and defaults every field so a
partially-formed model response can never crash downstream code):

```json
{
  "title": "string",
  "category": "space|organization|energy|maintenance|comfort|safety|accessibility|improvement",
  "room_id": "string or null",
  "room_name": "string or null",
  "priority": "low|medium|high|urgent_attention",
  "why_it_matters": "string",
  "recommended_action": "string",
  "expected_benefit": "string",
  "effort": "low|medium|high",
  "estimated_cost": {"type": "none|low|medium|high", "min": 0, "max": 0, "currency": "USD", "is_estimate": true},
  "confidence": "low|medium|high",
  "assumptions": ["string"],
  "requires_professional_assessment": false
}
```

`id`, `home_id`, `status`, `created_at`, `updated_at` are added later by
`recommendation_service.save_generated`, not by any agent.

## Safety rules every agent must follow

These are enforced via the shared system-prompt suffix in `app/agents/_shared.py::SAFETY_RULES`
and reinforced in each agent's own prompt:

1. Never invent exact savings, costs, or guarantees — always hedge ("potential", "estimated",
   "possible") and set `estimated_cost.is_estimate: true`.
2. Never suggest structural, electrical, or gas work without flagging
   `requires_professional_assessment: true`.
3. `priority: "urgent_attention"` is reserved for a genuine safety or maintenance concern —
   never for an ordinary design preference. `critic_agent.review()` downgrades any
   `urgent_attention` recommendation outside the `safety`/`maintenance` categories to `high`.
4. Never reveal internal reasoning or chain-of-thought — only the concise, user-facing fields
   above.
5. Respond with a single JSON object and nothing else (`response_format: json_object`).

## Failure handling

Every model-calling agent function catches `OpenAIServiceError` (raised by
`app/services/openai_service.py::chat_json`) internally and returns an empty-but-valid result
with `succeeded: False` and a human-readable `error`. The orchestrator never raises for a
well-formed home dict, including a home with zero rooms — it always returns a result, setting
`partial: true` when any section failed, and the API layer (`app/routes/ai.py`) surfaces
`HTTP 503` with the exact user-facing message from `task.md` §37 only if something unexpected
escapes the orchestrator entirely.

## Adding a new agent

1. Create `app/agents/<name>_agent.py` with an `analyze(home: dict) -> dict` function that
   builds a focused payload (send only what the agent needs, not the whole home profile when a
   narrower slice suffices), calls `app.agents._shared.run_agent(...)`, and normalizes its
   `recommendations` list via `normalize_recommendations`.
2. Wire it into `orchestrator.analyze_home` (add it to the `sections` list) and, if relevant,
   expose a dedicated orchestrator function (like `energy_insights`) for targeted generation.
3. Update the table above and the pipeline diagram.
