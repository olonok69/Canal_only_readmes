# AgentsVille Trip Planner (Notebook Guide)

Project 1 create an Agent to plan the perfect trip to the fictional city of AgentsVille applying modern LLM reasoning techniques. This project walks through:

- Role-based prompting (specialized planner roles)
- Chain-of-Thought (CoT) reasoning for itinerary design
- ReAct prompting (THOUGHT → ACTION → OBSERVATION)
- Feedback loops using evaluation tools (evals) and a revision agent
- Pydantic schemas for strongly-typed JSON I/O


All logic lives in the Jupyter Notebook:

- `Project_AgentsVille Trip PLanner/project_starter.ipynb`

The notebook uses mocked APIs (weather and activities) and a real LLM (OpenAI) to build, check, and revise a travel plan.

---

## Architecture diagram

<img alt="AgentsVille Trip Planner Architecture" src="./diagrams/agentsville-architecture.svg" width="980" />

---

## Contents

- Overview
- Prerequisites
- Setup (API key and environment)
- How to run (Windows PowerShell)
- Notebook walkthrough
- Key components and architecture
- Evaluations (Evals)
- ReAct revision loop
- Configuration/Customization
---

## Overview

I implemented two agents:

1) ItineraryAgent (CoT):
   - Crafts a day-by-day TravelPlan for the specified dates and budget using provided Weather + Activities context.
   - Outputs a strict JSON object conforming to a Pydantic schema (TravelPlan).

2) ItineraryRevisionAgent (ReAct):
   - Uses tools to evaluate and iteratively improve the plan.
   - Must pass all evals and incorporate traveler feedback (e.g., "at least two activities per day”).

also includes:
- Query mocked weather/activities data for a date window
- Enforce schemas with Pydantic
- Run evals to catch issues (budget mismatches, hallucinated events, bad weather matches, etc.)
- Close the loop with ReAct using tools (calculator, activities fetcher, eval runner, final answer)

---

## Prerequisites

- Python 3.10+ (recommended) (use 3.13.0)
- VS Code with Jupyter support 
- An OpenAI API key (required for LLM calls)

Notebook dependencies (installed in the first few cells):
- `json-repair`
- `numexpr`
- `openai`
- `pandas`
- `pydantic`
- `python-dotenv`



## Setup (API key and environment)


create a `.env` file at the repo root or the project folder with:

```
OPENAI_API_KEY=YOUR_OPENAI_KEY
# Optional override
# OPENAI_BASE_URL=https://api.openai.com/v1
```

The notebook loads `.env` automatically via `python-dotenv`.

---



## Notebook walkthrough



1) Initial Setup
   - Adds workspace path (if needed)
   - Installs dependencies
   - Initializes OpenAI client from environment variables

2) Define Vacation Details (Pydantic)
   - `VACATION_INFO_DICT` sample
   - Pydantic models: `Traveler`, `VacationInfo`
   - Validation ensures dates and required fields are correct

3) Review Weather and Activity Schedules (Mocked APIs)
   - `call_weather_api_mocked` for each date in the trip window
   - `call_activities_api_mocked` for each date
   - DataFrames to preview data

4) The ItineraryAgent (CoT)
   - Pydantic output models: `Weather`, `Activity`, `ActivityRecommendation`, `ItineraryDay`, `TravelPlan`
   - System prompt includes:
     - Role & Task
     - Output format with JSON example
     - TravelPlan JSON Schema (from Pydantic) to enforce structure
     - Context: inline WeatherForDates and ActivitiesForDates
   - `ItineraryAgent.get_itinerary(...)` calls the LLM and parses JSON into `TravelPlan`

5) Evaluating the Itinerary (Evals)
   - `get_eval_results(...)` helper and `EvaluationResults`
   - Evals include:
     - Dates match (arrival/departure)
     - Total cost accuracy
     - Total within budget
     - No hallucinated events (event-by-id check)
     - Interests satisfied per traveler
     - Weather compatibility (LLM-based check)
   - `ALL_EVAL_FUNCTIONS` aggregates these

6) Defining the Tools
   - `calculator_tool(expr)`
   - `get_activities_by_date_tool(date, city)`
   - `run_evals_tool(travel_plan)`
   - `final_answer_tool(final_output)`
   - Tool descriptions are derived from docstrings for the ReAct prompt

7) The ItineraryRevisionAgent (ReAct)
   - Traveler feedback text: "I want to have at least two activities per day."
   - A new eval checks that feedback is incorporated in the revised plan
   - ReAct system prompt enforces THOUGHT then exactly one ACTION as strict JSON:
     ```json
     {"tool_name": "run_evals_tool", "arguments": {"travel_plan": { /* ... */ }}}
     ```
   - Python loop repairs JSON if needed and routes tool calls; returns final `TravelPlan` when `final_answer_tool` is invoked

8) Final checks and display
   - Re-run all evals on the revised plan
   - Render day-by-day activities and an optional narrative summary

---

## Key components and architecture

- Pydantic models (strict JSON guardrails):
  - Input: `VacationInfo`
  - Output: `TravelPlan` (plus nested `ItineraryDay`, `Activity`, `Weather`)
- Mocked APIs (from `project_lib.py`):
  - `call_weather_api_mocked(date, city)`
  - `call_activities_api_mocked(date, city)`
  - `call_activity_by_id_api_mocked(activity_id)`
- LLM Client:
  - OpenAI client instantiated with `OPENAI_API_KEY` and optional `OPENAI_BASE_URL`
- Agents:
  - `ItineraryAgent` (single-shot CoT)
  - `ItineraryRevisionAgent` (multi-step ReAct with tools)
- Tools:
  - `calculator_tool`, `get_activities_by_date_tool`, `run_evals_tool`, `final_answer_tool`

---

## Evaluations (Evals)

Each eval raises an `AgentError` on failure, allowing the revision loop to diagnose and fix issues:

- Dates and ranges are consistent
- Sum of activity prices equals `total_cost`
- `total_cost` ≤ budget
- Itinerary events match real (mocked) events by ID
- Interests coverage across travelers
- Weather-activity compatibility via a compact LLM rubric
- Traveler feedback is fully incorporated (post-revision)

`run_evals_tool` returns a concise dict with `success` and `failures` to guide ReAct decisions.

---

## ReAct revision loop

- Prompt enforces: THOUGHT, then a single ACTION (JSON), then OBSERVATION (added by Python), repeat.
- Uses `json-repair` to tolerate minor JSON formatting hiccups from the LLM.
- Must call `run_evals_tool` before finalization and again to confirm success.
- Ends only when the LLM invokes `final_answer_tool` with a valid `TravelPlan`.

---

## Configuration/Customization

- Trip details: edit `VACATION_INFO_DICT` (travelers, destination, dates, budget, interests)
- Dates/City constraints: mocked data now extends for AgentsVille from 2025-06-10 through 2025-06-27 (additional activities including early indoor & interest-focused options)
- Model selection: defaults to `gpt-4.1-mini`; can switch to other models defined in `OpenAIModel`
- Cost/budget sensitivity: adjust budget and plan density to explore trade-offs
- Feedback: change `TRAVELER_FEEDBACK` to test different revision goals

---

## Command-Line Interface (CLI)

In addition to the notebook workflow, a lightweight CLI driver (`agentsville_trip_planner.py`) supports automated runs and logging.

Basic invocation (PowerShell):

```
python agentsville_trip_planner.py --log-revision --log-path logs/latest_revision.md --max-steps 8
```

Key arguments:

- `--max-steps N`                Limit revision loop iterations (default 6).
- `--log-revision`               Enable detailed step logging (ReAct loop + eval outcomes).
- `--log-mode {md|json}`         Markdown (human readable) or JSON (raw structured) log output.
- `--log-path PATH`              Destination file for the revision log.
- `--no-log-patch`               Omit JSON patch diffs of itinerary changes (smaller logs).
- `--narrate`                    Include a narrative summary of the final plan when supported.

The log file captures: meta header, initial plan snapshot, per-step THOUGHT/ACTION results (truncated raw LLM output with full reasoning retained if short), evaluation feedback, adopted auto-corrections, and final itinerary state.

---

## Logging System

`RevisionRunLogger` (in `logging_util.py`) records the evolution of the itinerary during the revision cycle.

Features:

- Incremental flush: writes after each step to avoid data loss on early exit.
- Raw model output threshold: long responses are truncated to keep logs concise while full THOUGHT reasoning under a size threshold is preserved.
- JSON patch diffs (optional): highlights structural changes to the itinerary between steps.
- Early termination annotation: clearly marks when heuristics short‑circuit the loop because all evals passed.

Example (Markdown excerpt):

```
## Steps
### Step 2 – Tool: run_evals_tool
THOUGHT: Checking evaluations to see remaining issues.
Result: {"all_passed": false, "uncovered_interests": ["art"], ...}
Patch:
   - Added activity event-2025-06-24-4 (Indoor Gallery Tour) to 2025-06-24
```

---

## Heuristics & Enhancements

Recent improvements to reduce unnecessary token usage and converge faster:

1. Early Evaluation Termination: If a call to `run_evals_tool` reports `all_passed`, the agent immediately finalizes without extra reasoning steps.
2. Auto Cost Correction Adoption: When evals include an `auto_corrected_travel_plan` (only total cost mismatch), it is adopted automatically, followed by a confirmatory eval pass & potential immediate finalization.
3. Post-Mutation Auto Evals: After any itinerary mutation (add/remove/calculator), evals are auto‑run to prevent the model from forgetting and looping.
4. Calculator Loop Guard: Detects redundant consecutive `calculator_tool` calls when total cost remains unchanged; triggers evals and finalization if all pass.
5. Indoor Weather Handling: Weather compatibility eval can allow flagged outdoor-incompatible days if at least one indoor activity is scheduled (detected via keywords or explicit indoor flag in activity metadata).
6. Interest Coverage Priority: Activities matching uncovered interests are prioritized early, especially on under-filled days.

---

## Data Continuity Validation

`validate_mock_data.py` script validates that mocked activities & weather cover each date in the configured range and that guard rules align (no missing days). Run it after extending datasets:

```
python validate_mock_data.py
```

---

## Testing / Logging Harness

A lightweight test harness (planned `tests/test_logging_harness.py`) can simulate a short revision run with logging enabled and assert that:

- Log file is created and non‑empty.
- Meta header + at least one Step section exists.
- Final itinerary section present.

This helps guard against regressions where serialization changes could silently drop log content.

---

## Roadmap Ideas

- Pluggable models (Anthropic / local) with unified schema adapter.
- Cost normalization & currency handling.
- Multi-city chaining with transfer constraints.
- Caching layer for repeated activity/date fetches.
- Structural diff weighting to bias revisions toward minimal-change fixes.

---

## Changelog (Recent)

- Added extended mock date range (through 2025-06-27) with new indoor/art/technology events.
- Implemented early termination heuristic on passing all evals.
- Added auto adoption of cost correction plan.
- Added post-mutation automatic eval execution.
- Introduced calculator loop guard / early finalize pathway.
- Added indoor activity heuristic to weather evaluation.
- Added incremental step logging with optional JSON patches.
- Added CLI flags: `--max-steps`, logging controls, narrative output option.
- Added data continuity validation script.
- Cleaned debug instrumentation from production code.

---


