# OpenAPI SQL Chatbot with Google ADK

Translations: Español (README.es.md)

This repository contains a conversational assistant powered by Google’s Agent Development Kit (ADK). The agent uses an OpenAPI specification (`schema.json`) to auto-generate tools that talk to a read-only SQL API. With natural-language prompts you can:

- List available tables.
- Inspect table schemas.
- Sample rows.
- Run parameterized `SELECT` queries.

The chatbot relies on OpenAI models via ADK’s LiteLLM adapter and demonstrates how to combine ADK agents with external REST integrations described in OpenAPI.

## Table of Contents
- Overview
- Prerequisites
- Setup
- Configuration
- Running the Chatbot
- Project Structure
- Troubleshooting
- Further Reading

## Overview
- **Entry point:** `openapi_sql_chatbot.py`
- **Key components:**
	- `OpenAPIToolset` parses the spec and exposes REST operations as ADK tools.
	- `LiteLlm` connects to OpenAI models (default: `openai/gpt-4o`).
	- `Runner` and `InMemorySessionService` manage conversation state.
 - **Architecture diagram:** `docs/architecture.svg`

## Prerequisites
- Python 3.10 or newer (3.12 tested)
- PowerShell or a compatible shell (examples use Windows syntax)
- Access to OpenAI models via API key
- Bearer token for the SQL API described in `schema.json`

## Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
```

If you are using an existing environment, ensure `google-adk`, `litellm`, and `pydantic` match the versions in `requirements.txt`.

## Configuration
Environment variables are loaded from `.env` when `python-dotenv` is available.

| Variable | Required | Purpose |
| -------- | -------- | ------- |
| `OPENAI_API_KEY` | Yes | Enables LiteLLM to call OpenAI models. |
| `OPENAPI_BEARER_TOKEN` | Yes | Injected as HTTP Bearer auth for the SQL API endpoints. |
| `WANDB_API_KEY` | Optional | Enables OpenTelemetry traces to be forwarded to W&B Weave. |
| `WANDB_PROJECT` | Optional | `entity/project` identifier for your Weave workspace. |
| `WANDB_BASE_URL` | Optional | Override the default Weave trace endpoint (defaults to `https://trace.wandb.ai`). |

Example `.env`:
```
OPENAI_API_KEY=sk-your-key
OPENAPI_BEARER_TOKEN=your-bearer-token
```

> Keep credentials private. The repository ships a sample `.env` only for local development.

## Running the Chatbot
```powershell
python .\openapi_sql_chatbot.py [--verbose]
```

- Type natural-language questions such as “List tables in the database” or “Show sample rows from `claims`.”
- The optional `--verbose` flag prints raw tool responses for debugging.
- The script handles authentication automatically using the bearer token and OpenAPI spec.

**Weave tracing (optional):** set `WANDB_API_KEY` and `WANDB_PROJECT` (and optionally `WANDB_BASE_URL`) to forward OpenTelemetry traces to Weave. If the variables are absent, tracing is skipped automatically.

## Project Structure
```
.
├─ openapi_sql_chatbot.py         # Conversational ADK agent using OpenAPI tools
├─ schema.json                    # OpenAPI spec powering the generated tools
├─ data/                          # Sample JSONL files (not required by the chatbot)
├─ requirements.txt               # Python dependencies
└─ README*.md                     # Documentation (English & Spanish)
```

Legacy files from earlier experiments may still be present but are not needed for the chatbot demo.

## Troubleshooting
- **Missing credentials** – Ensure both `OPENAI_API_KEY` and `OPENAPI_BEARER_TOKEN` are set. The chatbot exits with an error if either is absent.
- **Tool call failures** – The target API is read-only. Non-SELECT queries are rejected and the agent surfaces the error message.
- **Async runtime errors** – When running inside notebooks, `asyncio.run` can clash with an existing event loop. The script detects this and falls back to the active loop.

## Further Reading
- [Google ADK documentation](https://google.github.io/adk-docs/)
- [OpenAPI tool integration guide](https://google.github.io/adk-docs/tools-custom/openapi-tools/)
- [LiteLLM adapters in ADK](https://google.github.io/adk-docs/models/)

Enjoy exploring your SQL data sources through natural language.
