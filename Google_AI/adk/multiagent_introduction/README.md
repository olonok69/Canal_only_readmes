# Automated Claim Triage with Google ADK

Translations: Español (README.es.md)

This repository contains a multi-agent application built on Google’s Agent Development Kit (ADK) that triages First Notice of Loss (FNOL) narratives into structured data, assigns a severity level, and routes the claim to the right processing queue.

The design emphasizes: (1) clear agent responsibilities, (2) strict tool schemas enforced with Pydantic, and (3) deterministic tool-calling via OpenAI models using LiteLLM.

## Table of Contents

- What is Google ADK?
- Application Overview
- Architecture
- Installation
- Configuration
- How to Run
- Batch Processing
- Tests
- Dependencies
- Troubleshooting
- Project Structure
- Next Steps

## What is Google ADK?

Google’s Agent Development Kit (ADK) is a framework for composing LLM-driven agents that:

- Define purpose-built Agents: each with instructions, a description, and callable tools
- Orchestrate agent runs with a Runner and a Session service
- Persist state across turns (session.state) for memory and chained reasoning

Key parts used here:

- Agent: LLM-backed worker with tools it can call using function calling
- Tools: Python functions exposed to the LLM (ADK builds a JSON schema for each)
- Sub-agents: Specialized agents a root agent can delegate to
- Runner: Executes an agent asynchronously and yields events
- Session: Stores per-session state to chain outputs between stages

## Application Overview

“Automated Claim Triage: From FNOL to the Right Queue”

Agents implemented:

- extract_claim_info — extracts structured claim fields, calls set_claim_info(...)
- assess_severity — assigns severity (low | medium | high) with rationale, calls set_severity(level, rationale)
- route_claim — selects queue (fast-track | standard | auto-physical-damage | medical | property | SIU | CAT) with rationale, calls set_route(queue, rationale)
- root (coordinator) — provides the summary and coordinates the pipeline

Quality Gates (Pydantic):

- All tool inputs are validated against Pydantic models (ClaimInfo, SeverityAssessment, RouteDecision) before being written to state.
- Tools accept flat, primitive parameters to keep OpenAI function schemas valid; validation happens internally.

Determinism:

- Temperature lowered to 0.1 for more consistent tool usage
- Guard & nudge: Orchestrator checks if each stage produced state; if not, it sends a stricter instruction and retries

## Architecture

High-level flow:

1. extract_claim_info → set_claim_info → session.state.claim_info
2. assess_severity → set_severity → session.state.severity
3. route_claim → set_route → session.state.route
4. root agent → final summary

Text diagram:

```
+------------------+         +---------------------+
|  FNOL narrative  |  --->   |  extract_claim_info | -- set_claim_info --> state.claim_info
+------------------+         +---------------------+
                                          |
                                          v
                             +---------------------+
                             |   assess_severity   | -- set_severity --> state.severity
                             +---------------------+
                                          |
                                          v
                             +---------------------+
                             |     route_claim     | -- set_route ----> state.route
                             +---------------------+
                                          |
                                          v
                                  +---------------+
                                  |   root agent  |
                                  +---------------+
```

Visual diagram:

![High-level architecture](docs/architecture.svg)

## Installation

- Python 3.10+ recommended
- Windows PowerShell commands shown below

Create a virtual environment (optional but recommended) and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
```

## Configuration

Environment variables (use a `.env` file or set in your shell):

- OPENAI_API_KEY (required)
  - Your OpenAI API key for LiteLLM and ADK’s LiteLlm adapter
- FNOL_EXAMPLES_PATH (optional)
  - Path to a .jsonl/.json/.csv file that contains FNOL examples to batch triage

Example `.env`:

```
OPENAI_API_KEY=sk-...redacted...
FNOL_EXAMPLES_PATH=./data/fnol_examples_more.jsonl
```

## How to Run

Single example:

```powershell
python .\claim_triage_adk.py
```

You should see a “Session State Snapshot” with:

- claim_info (dict)
- severity (dict: level + rationale)
- route (dict: queue + rationale)

## Batch Processing

- Supported inputs: JSONL (one string or object with `text` per line), JSON (array of strings or objects with `text`), CSV (column `text` by default)
- Set the file via FNOL_EXAMPLES_PATH and run the script:

```powershell
$env:FNOL_EXAMPLES_PATH = ".\data\fnol_examples_more.jsonl"
python .\claim_triage_adk.py
```

The script will triage multiple examples and print the results. You can adjust the batch limit in `__main__`.

## Tests

- Tool-level tests validate Pydantic-backed inputs and state writes
- End-to-end-style test monkeypatches the internal runner helper to simulate agent behavior and verify orchestration

Run tests:

```powershell
pytest -q
```

These tests are deterministic and do not call the LLM.

## Dependencies

See `requirements.txt` for exact versions. Key libraries include:

- google-adk — agent runtime, sessions, tools
- litellm — unified model client used by ADK’s LiteLlm adapter
- pydantic — validation for tool inputs
- pytest — unit testing
- neo4j — present for earlier lesson notebooks; not required by the triage flow

## Troubleshooting

- Invalid function schema error
  - Symptom: `Invalid schema for function ...` from OpenAI/LiteLLM
  - Fix: Tools use flat, primitive parameters; Pydantic validation inside the tool

- Tools not called / state remains None
  - Temperature is set lower (0.1)
  - Instructions demand: “CALL THE TOOL … Do not output text—just call the tool.”
  - Guard & nudge: After each stage, the orchestrator checks state and re-prompts if missing

- Missing OPENAI_API_KEY
  - The script warns and exits; set it in `.env` or the environment

## Project Structure

```
.
├─ claim_triage_adk.py           # Main triage pipeline (agents, tools, orchestrator, batch loaders)
├─ requirements.txt              # Dependencies
├─ data/
│  ├─ fnol_examples_more.jsonl   # Sample examples for batch triage
│  └─ fnol_examples.jsonl        # (optional) your examples
├─ tests/
│  └─ test_claim_triage.py       # Tool + orchestration tests
├─ .env                          # Env vars (OPENAI_API_KEY, FNOL_EXAMPLES_PATH)
└─ [lesson notebooks & legacy helpers - optional]
```

## Next Steps

- Persist sessions in a data store (instead of in-memory)
- Add specialized agents (coverage validation, fraud screening)
- Add structured logging/metrics
- Add a CLI with `--input`, `--output` to write results to JSON/CSV
