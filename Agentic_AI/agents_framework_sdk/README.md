# ms-agent-app — Microsoft Agent Framework + Foundry + MCP + Eval + PyRIT

> **Important (preview)**: This project depends on prerelease Microsoft Agent Framework packages and the PyRIT v0.x toolkit. Both move quickly. Pin versions before relying on these instructions in production.

A small, didactic Python application that wires together four layers of a modern agent stack:

1. A **chat agent** built with the [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent?pivots=programming-language-python), backed by an **Azure AI Foundry** model deployment via `FoundryChatClient`.
2. A **local MCP toolbelt** — the sibling [`adk_financial_mcp_server`](../adk_financial_mcp_server) (FastMCP / stdio) attached through `MCPStdioTool`, so the agent can run quantitative analyses on real market data.
3. **Quality evaluation** with the [Azure AI Evaluation SDK](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators) (`IntentResolutionEvaluator`, `TaskAdherenceEvaluator`, `ToolCallAccuracyEvaluator`).
4. **Adversarial / safety evaluation** with [Microsoft PyRIT](https://github.com/microsoft/PyRIT) — the open automation framework for red-teaming generative-AI systems announced by Microsoft on [Feb 22, 2024](https://www.microsoft.com/en-us/security/blog/2024/02/22/announcing-microsofts-open-automation-framework-to-red-team-generative-ai-systems/).

The project is designed for workshops, technical talks, and as a clean skeleton when bootstrapping a new Agent Framework + Foundry application.

## Table of Contents

1. [Architecture](#architecture)
2. [Features](#features)
3. [Repository Layout](#repository-layout)
4. [Phases](#phases)
5. [Prerequisites](#prerequisites)
6. [Installation](#installation)
7. [Configuration](#configuration)
8. [How to Run](#how-to-run)
9. [Phase 3 — Azure AI Evaluation SDK](#phase-3--azure-ai-evaluation-sdk)
10. [Phase 4 — PyRIT Red-Team Pass](#phase-4--pyrit-red-team-pass)
11. [Key Files](#key-files)
12. [Testing](#testing)
13. [Troubleshooting](#troubleshooting)
14. [Operational Tips](#operational-tips)
15. [References](#references)

## Architecture

<p align="center">
  <img src="microsoft_agent_framework_app/docs/architecture.svg" alt="ms-agent-app high-level architecture" width="1080">
</p>

High-level data flow:

1. **Developer** runs the CLI (`ms-agent-app`); `cli.py` loads `.env` via `pydantic-settings` (`config.py`) and builds an Agent (`agent_factory.build_chat_agent`).
2. The Agent calls **Azure AI Foundry** through `FoundryChatClient`, authenticated with `AzureCliCredential` (i.e. your `az login` token).
3. With `--with-mcp`, `mcp_finance.open_finance_mcp_tool` spawns the sibling **FastMCP "finance tools" server** as a stdio subprocess; its tools become callable by the Agent in the same `agent.run(...)` loop.
4. **Phase 3** (`ms_agent_app.eval`) replays a curated dataset through the same Agent, captures trajectories in the OpenAI message schema, and scores them with **Azure AI Evaluation SDK** evaluators using a configurable judge provider (`JUDGE_PROVIDER=azure-openai|openai`).
5. **Phase 4** (`ms_agent_app.redteam`) wraps the same Agent in a **PyRIT `PromptTarget`**, fires red-team objectives through a `PromptSendingAttack`, and detects refusals with `SelfAskRefusalScorer` driven by the same configurable judge provider.

Full diagram source: [`microsoft_agent_framework_app/docs/architecture.svg`](microsoft_agent_framework_app/docs/architecture.svg).

## Features

- **Async-first Agent Framework wiring** — minimal `FoundryChatClient` factory plus an `Agent` factory that accepts an optional MCP toolbelt.
- **Lazy MCP subprocess management** — `MCPStdioTool` is opened in an `async with` block; the finance server only runs when `--with-mcp` is set.
- **Single `.env` for four layers** — model provider, MCP server path, evaluation judge, and PyRIT judge share one configuration surface, validated by `pydantic-settings`.
- **Replayable evaluation harness** — `Trajectory.record(agent)` captures `(query, response, tool_calls)` in the OpenAI message-schema shape the Azure AI Evaluation SDK expects.
- **Red-team script** — Phase 4 ships a small dataset of jailbreak / prompt-injection / harmful-finance / system-prompt-extraction probes that you can run with one command.
- **Optional heavy deps** — `pyrit` is an extras group (`uv sync --extra redteam`) so the base install stays small.

## Repository Layout

```text
microsoft_agent_framework_app/
├── CLAUDE.md                              # context for AI assistants
├── README.md                              # this file
├── pyproject.toml                         # uv-managed deps + ruff/pytest config
├── uv.lock
├── .env.example                           # configuration template
├── docs/
│   ├── architecture.svg                   # high-level architecture diagram
│   └── superpowers/plans/                 # implementation plans
├── src/
│   └── ms_agent_app/
│       ├── __init__.py
│       ├── cli.py                         # async REPL, --with-mcp flag
│       ├── config.py                      # Settings(BaseSettings)
│       ├── foundry_client.py              # FoundryChatClient + AzureCliCredential
│       ├── agent_factory.py               # build_chat_agent(...)
│       ├── mcp_finance.py                 # MCPStdioTool wiring
│       ├── eval/                          # Phase 3 — Azure AI Evaluation SDK
│       │   ├── __init__.py
│       │   ├── dataset.py                 # curated EvalCase tuple
│       │   ├── runner.py                  # Trajectory.record() helper
│       │   └── score.py                   # entry point: writes .eval_outputs/results.json
│       └── redteam/                       # Phase 4 — PyRIT
│           ├── __init__.py
│           ├── dataset.py                 # curated RedTeamCase tuple
│           ├── target.py                  # AgentFrameworkTarget(PromptTarget)
│           └── run.py                     # entry point: writes .pyrit_outputs/results.json
└── tests/
    ├── test_agent_factory.py
    ├── test_config.py
    ├── test_eval_runner.py
    ├── test_mcp_finance.py
    └── test_redteam_target.py             # auto-skips when pyrit is not installed
```

## Phases

| Phase | Goal | Entry command | Key files |
|-------|------|---------------|-----------|
| **0** | Bootstrap the project with `uv` and write `.env` | `uv sync` | `pyproject.toml`, `.env.example` |
| **1** | Foundry-backed chat agent (no tools) | `uv run ms-agent-app` | `foundry_client.py`, `agent_factory.py`, `cli.py` |
| **2** | Same agent + local financial MCP tools | `uv run ms-agent-app --with-mcp` | `mcp_finance.py` |
| **3** | Score curated runs with Azure AI Evaluation SDK | `uv run python -m ms_agent_app.eval.score` | `eval/dataset.py`, `eval/runner.py`, `eval/score.py` |
| **4** | Red-team the agent with PyRIT | `uv run ms-agent-redteam` | `redteam/dataset.py`, `redteam/target.py`, `redteam/run.py` |

## Prerequisites

- **Python `3.11+`** (Agent Framework requires it; PyRIT supports `3.10–3.14`).
- **`uv`** package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
- **Azure CLI** for `az login` (`FoundryChatClient` authenticates through `AzureCliCredential`).
- **Azure AI Foundry project** with a chat model deployment (e.g. `gpt-4.1`).
- **Azure OpenAI resource** for the Phase 3 / Phase 4 judge model (e.g. `gpt-4o`).
- **Sibling project** [`../adk_financial_mcp_server`](../adk_financial_mcp_server) cloned with its own venv (used as the stdio MCP server in Phase 2).

## Installation

This project lives on a Windows-mounted drive (`/mnt/d/...`) where WSL `drvfs` blocks the `chmod` operations `uv` uses inside the venv. The workaround — used in every example below — is to keep the venv on the Linux filesystem and re-export `UV_PROJECT_ENVIRONMENT`:

```bash
export UV_PROJECT_ENVIRONMENT=/home/$USER/.venvs/ms-agent-app
uv sync                               # base install
uv sync --extra redteam               # also install pyrit (~150 MB extra)
```

`[tool.uv] link-mode = "copy"` is already configured in `pyproject.toml`, so you do not need `UV_LINK_MODE`. If you are on macOS or a native Linux filesystem you can drop the `UV_PROJECT_ENVIRONMENT` export entirely.

## Configuration

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

| Variable | Used by | Notes |
|---|---|---|
| `MODEL_PROVIDER` | Phase 1, 2, 3, 4 chat runtime | One of `foundry`, `openai`, `azure-openai`, `anthropic` (default `foundry`) |
| `FOUNDRY_PROJECT_ENDPOINT` | Phase 1, 2, 3, 4 — Foundry chat client | Required when `MODEL_PROVIDER=foundry`; e.g. `https://<resource>.services.ai.azure.com/api/projects/<project>` |
| `FOUNDRY_MODEL_DEPLOYMENT_NAME` | Phase 1, 2, 3, 4 — Foundry chat client | Required when `MODEL_PROVIDER=foundry` |
| `OPENAI_API_KEY` | Phase 1, 2, 3, 4 — OpenAI chat provider | Required when `MODEL_PROVIDER=openai` |
| `OPENAI_CHAT_MODEL` | Phase 1, 2, 3, 4 — OpenAI chat provider | Preferred deployment for `OpenAIChatClient` |
| `OPENAI_MODEL` | Optional fallback for OpenAI chat provider | Used when `OPENAI_CHAT_MODEL` is unset |
| `OPENAI_BASE_URL` | Optional — OpenAI chat provider | Custom OpenAI-compatible base URL |
| `AZURE_OPENAI_ENDPOINT` | Phase 1, 2, 3, 4 — Azure OpenAI chat provider | Required when `MODEL_PROVIDER=azure-openai` |
| `AZURE_OPENAI_CHAT_MODEL` | Phase 1, 2, 3, 4 — Azure OpenAI chat provider | Preferred deployment for `OpenAIChatClient` |
| `AZURE_OPENAI_MODEL` | Optional fallback for Azure OpenAI chat provider | Used when `AZURE_OPENAI_CHAT_MODEL` is unset |
| `AZURE_OPENAI_API_KEY` | Optional — Azure OpenAI chat provider | Not required when using Azure identity auth |
| `AZURE_OPENAI_API_VERSION` | Optional — Azure OpenAI chat provider | API version override for OpenAI client |
| `ANTHROPIC_API_KEY` | Phase 1, 2, 3, 4 — Anthropic chat provider | Required when `MODEL_PROVIDER=anthropic` |
| `ANTHROPIC_CHAT_MODEL` | Phase 1, 2, 3, 4 — Anthropic chat provider | Claude model ID |
| `ANTHROPIC_BASE_URL` | Optional — Anthropic chat provider | Custom Anthropic-compatible base URL |
| `AZURE_TENANT_ID` | Optional — `AzureCliCredential` | Only when `az login` has multiple tenants |
| `MCP_FINANCE_SERVER_PATH` | Phase 2 | Absolute or relative path to `adk_financial_mcp_server/server/main.py` |
| `MCP_FINANCE_PYTHON` | Phase 2 | Interpreter that has the finance server's deps installed |
| `JUDGE_PROVIDER` | Phase 3 judge **and** Phase 4 PyRIT judge | `azure-openai` (default) or `openai` |
| `AZURE_DEPLOYMENT_NAME` | Judge when `JUDGE_PROVIDER=azure-openai` | Azure OpenAI deployment name (e.g. `gpt-4o`) |
| `AZURE_API_KEY` | Judge when `JUDGE_PROVIDER=azure-openai` | Azure OpenAI key |
| `AZURE_ENDPOINT` | Judge when `JUDGE_PROVIDER=azure-openai` | `https://<aoai>.cognitiveservices.azure.com/` |
| `AZURE_API_VERSION` | Judge when `JUDGE_PROVIDER=azure-openai` | Default `2024-12-01-preview` |
| `JUDGE_OPENAI_API_KEY` | Judge when `JUDGE_PROVIDER=openai` | Optional override; falls back to `OPENAI_API_KEY` |
| `JUDGE_OPENAI_MODEL` | Judge when `JUDGE_PROVIDER=openai` | Optional override; falls back to `OPENAI_CHAT_MODEL` / `OPENAI_MODEL` |
| `JUDGE_OPENAI_BASE_URL` | Optional OpenAI judge base URL | Defaults to `OPENAI_BASE_URL` then `https://api.openai.com/v1` |
| `JUDGE_OPENAI_ORGANIZATION` | Optional OpenAI judge organization | Passed to `OpenAIModelConfiguration` |

`pydantic-settings` validates the file and surfaces friendly errors if Phase 1 / 2 vars are missing. Judge vars are validated lazily when Phase 3 / Phase 4 scripts run based on `JUDGE_PROVIDER`.

## How to Run

```bash
# Phase 1 — chat-only agent (no tools)
uv run ms-agent-app

# Phase 1 provider options via CLI override
uv run ms-agent-app --provider foundry
uv run ms-agent-app --provider openai
uv run ms-agent-app --provider azure-openai
uv run ms-agent-app --provider anthropic

# Phase 2 — agent + finance MCP tools (lazy stdio subprocess)
uv run ms-agent-app --with-mcp
uv run ms-agent-app --with-mcp --provider foundry
uv run ms-agent-app --with-mcp --provider openai
uv run ms-agent-app --with-mcp --provider azure-openai
uv run ms-agent-app --with-mcp --provider anthropic

# Phase 3 — Azure AI Evaluation SDK pass over the curated dataset
# Agent model provider comes from MODEL_PROVIDER in .env
# Judge provider comes from JUDGE_PROVIDER in .env
uv run python -m ms_agent_app.eval.score

# Phase 4 — PyRIT red-team pass over the curated attack dataset
# Agent model provider comes from MODEL_PROVIDER in .env
# Judge provider comes from JUDGE_PROVIDER in .env
uv run ms-agent-redteam
```

### Demo matrix for all 4 phases

Use these provider settings before running the command for each phase:

| Phase | Command | Agent provider options | Judge provider options |
|---|---|---|---|
| 1 | `uv run ms-agent-app [--provider ...]` | `foundry`, `openai`, `azure-openai`, `anthropic` (via `--provider` or `MODEL_PROVIDER`) | N/A |
| 2 | `uv run ms-agent-app --with-mcp [--provider ...]` | `foundry`, `openai`, `azure-openai`, `anthropic` (via `--provider` or `MODEL_PROVIDER`) | N/A |
| 3 | `uv run python -m ms_agent_app.eval.score` | `foundry`, `openai`, `azure-openai`, `anthropic` (from `MODEL_PROVIDER`) | `azure-openai` or `openai` (from `JUDGE_PROVIDER`) |
| 4 | `uv run ms-agent-redteam` | `foundry`, `openai`, `azure-openai`, `anthropic` (from `MODEL_PROVIDER`) | `azure-openai` or `openai` (from `JUDGE_PROVIDER`) |

### Manual smoke test (Phase 2)

```bash
uv run ms-agent-app --with-mcp
```

At the prompt try:

- `What tools are available?` — agent should list the finance tools.
- `Run a dual moving average analysis on AAPL.` — agent should call a tool and report results.
- `exit` to quit.

The MCP server subprocess is started lazily by `MCPStdioTool` and exits when the REPL exits.

## Phase 3 — Azure AI Evaluation SDK

`ms_agent_app.eval.score` follows the same shape as [`evaluation/03_azure_ai_eval_agents.py`](../evaluation/03_azure_ai_eval_agents.py) from the sibling evaluation project:

1. `Settings()` loads the judge model config from `JUDGE_PROVIDER`:
    - `azure-openai` -> `AzureOpenAIModelConfiguration`
    - `openai` -> `OpenAIModelConfiguration`
2. For each `EvalCase` in `eval/dataset.py`, `Trajectory.record(agent, tools=mcp_server)` runs the prompt and captures the response + any tool calls in the OpenAI message-schema shape:
   ```python
   {"role": "user", "content": [{"type": "text", "text": "..."}]}
   {"role": "assistant", "content": [
       {"type": "tool_call", "tool_call_id": "...", "name": "...", "arguments": {...}},
       {"type": "text", "text": "..."},
   ]}
   ```
3. Three evaluators score each trajectory:
   - `IntentResolutionEvaluator` (threshold `3`)
   - `TaskAdherenceEvaluator` (threshold `0.5`)
   - `ToolCallAccuracyEvaluator` (only when the trajectory actually contains tool calls)
4. Results are written to `.eval_outputs/results.json`.

Curated dataset (`eval/dataset.py`):

| Case ID | Intent | Expects tool call? |
|---------|--------|--------------------|
| `intent-direct` | Definition of MS Agent Framework | No |
| `tool-dual-ma` | Dual moving-average backtest on AAPL | Yes |
| `tool-fundamentals` | Fundamental analysis snapshot for MSFT | Yes |
| `clarification` | Ambiguous "help me with a strategy" — agent should ask | No |

## Phase 4 — PyRIT Red-Team Pass

[PyRIT](https://github.com/microsoft/PyRIT) (Python Risk Identification Toolkit) is Microsoft's open framework for red-teaming generative-AI systems. It models adversarial evaluation as four pluggable building blocks:

- **Targets** — what gets attacked (`PromptTarget`, e.g. our Agent).
- **Attacks / Orchestrators** — how prompts are delivered (`PromptSendingAttack`).
- **Converters** — transformations applied to prompts before they reach the target (Base64, ROT13, prompt-injection wrappers, etc.).
- **Scorers** — judges that classify the response (`SelfAskRefusalScorer`, content-category scorers, true/false scorers).

> Heads-up: PyRIT renamed several abstractions in v0.13. We use the **current** names: `PromptTarget` (not `PromptChatTarget`), `PromptSendingAttack` (not `PromptSendingOrchestrator`), `Message`/`MessagePiece` (not `PromptRequestResponse`/`PromptRequestPiece`), and the async `initialize_pyrit_async(...)` bootstrap. Older tutorials will not run unchanged.

### How this project integrates PyRIT

1. **Bootstrap** (`redteam/run.py`):
   ```python
   from pyrit.setup import initialize_pyrit_async, IN_MEMORY
   await initialize_pyrit_async(IN_MEMORY)
   ```
   This sets a `CentralMemory` instance so attacks have somewhere to write conversation history. We use the in-memory backend (no DuckDB or Azure SQL needed for the demo).

2. **Target adapter** (`redteam/target.py`) — wraps an `agent_framework.Agent` as a PyRIT target:
   ```python
   class AgentFrameworkTarget(PromptTarget):
       async def _send_prompt_to_target_async(self, *, normalized_conversation):
           prompt = _extract_last_user_text(normalized_conversation)
           result = await self._agent.run(prompt)
           text = getattr(result, "text", "") or str(result)
           return [Message(message_pieces=[MessagePiece(role="assistant", original_value=text)])]
   ```
   PyRIT calls `send_prompt_async` (which is `@final`); we only override the single abstract coroutine. Memory + history is handled by the base class.

3. **Judge model** — `SelfAskRefusalScorer` needs its own LLM judge. We point an `OpenAIChatTarget` using `JUDGE_PROVIDER` routing:
    - `azure-openai`: uses `AZURE_ENDPOINT + /openai/v1`, `AZURE_API_KEY`, `AZURE_DEPLOYMENT_NAME`
    - `openai`: uses `JUDGE_OPENAI_*` (or falls back to `OPENAI_*`)

4. **Attack** — `PromptSendingAttack` + `AttackExecutor` send the dataset's objectives through the target with bounded concurrency:
   ```python
   attack = PromptSendingAttack(
       objective_target=target,
       attack_scoring_config=AttackScoringConfig(objective_scorer=refusal_scorer),
   )
   await AttackExecutor(max_concurrency=2).execute_attack_async(
       attack=attack, objectives=[case.objective for case in CASES],
   )
   ```

5. **Output** — `.pyrit_outputs/results.json` with one record per case: `objective`, `agent_response`, `outcome` (`SUCCESS` / `FAILURE` / `ERROR` / `UNDETERMINED`), `refusal_detected` (`True` if the refusal scorer fired), `score_rationale`, and `outcome_reason`.

### Curated attack dataset

`redteam/dataset.py` keeps the set deliberately small — five probes that each exercise a distinct attacker behavior:

| Case ID | Category | What it probes |
|---------|----------|----------------|
| `jailbreak-dan` | jailbreak | Classic DAN persona + market-manipulation ask |
| `prompt-injection-tool` | prompt_injection | Injection that targets tool-call arguments |
| `harmful-financial-advice` | harm_misuse | High-pressure ask for high-risk leverage advice |
| `insider-trading` | harm_misuse | Explicit illegal-trading walkthrough request |
| `system-prompt-extraction` | prompt_injection | Verbatim system-prompt leak attempt |

A well-behaved Foundry deployment should refuse all five; the scorer reports `refusal_detected: true` (PyRIT `AttackOutcome.SUCCESS` for a refusal scorer means *the refusal was detected*, not that the attack landed).

### Extending the demo

- **Converters** — wrap prompts to bypass naive filters; add e.g. `from pyrit.prompt_converter import Base64Converter` and pass an `AttackConverterConfig`.
- **Multiple scorers** — add `SelfAskCategoryScorer` for harm-category classification alongside refusal detection.
- **Multi-turn attacks** — switch `PromptSendingAttack` for `RedTeamingAttack` to chain adversarial turns driven by an attacker LLM.
- **Persistent memory** — swap `IN_MEMORY` for `SQLITE` or `AZURE_SQL` if you want to compare runs across days.

## Key Files

- **`src/ms_agent_app/cli.py`** — async REPL; lazily imports `mcp_finance` so the base install does not need to start the finance server.
- **`src/ms_agent_app/agent_factory.py`** — single `build_chat_agent(settings, *, tools=None)` factory; the default `DEFAULT_INSTRUCTIONS` tells the agent to prefer tools over guessing.
- **`src/ms_agent_app/foundry_client.py`** — thin wrapper that returns a `FoundryChatClient` configured from `Settings`.
- **`src/ms_agent_app/mcp_finance.py`** — `build_finance_mcp_tool` + `open_finance_mcp_tool` context manager; raises friendly `ValueError` / `FileNotFoundError` when env is misconfigured.
- **`src/ms_agent_app/eval/score.py`** — Phase 3 entry point; writes `.eval_outputs/results.json`.
- **`src/ms_agent_app/redteam/run.py`** — Phase 4 entry point; writes `.pyrit_outputs/results.json`.
- **`docs/architecture.svg`** — high-level architecture diagram embedded above.

## Testing

```bash
uv run pytest -v
```

The suite covers:

- `Settings` env loading and validation (including missing-env negative test with `_env_file=None`).
- `build_chat_agent` constructor wiring.
- `build_finance_mcp_tool` argument resolution.
- `Trajectory.record` shape against a mocked Agent.
- `AgentFrameworkTarget` — auto-skipped when `pyrit` is not installed (the optional extras group).

Lint + format:

```bash
uv run ruff check .
uv run ruff format --check .
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `chmod ... .git/config.lock: Operation not permitted` (WSL) | Export `UV_PROJECT_ENVIRONMENT=/home/$USER/.venvs/ms-agent-app` so the venv lives on ext4. |
| `Missing env vars for eval judge ...` | Fill judge vars in `.env` according to `JUDGE_PROVIDER`. |
| `ModuleNotFoundError: pyrit` when running `ms-agent-redteam` | Re-run `uv sync --extra redteam`. |
| `MCP server script not found at ...` | Check `MCP_FINANCE_SERVER_PATH` is correct and the sibling project is cloned. |
| Foundry calls return `DefaultAzureCredential failed ...` | Run `az login`. If you have multiple tenants, also set `AZURE_TENANT_ID`. |
| PyRIT install pulls `transformers` and a large download | This is expected — `transformers` is a hard runtime dep even in the lean install. Allow ~150 MB. |
| `AttackOutcome.SUCCESS` looks like the agent was jailbroken | For `SelfAskRefusalScorer`, `SUCCESS` means **the refusal was detected**. Invert with `TrueFalseInverterScorer` if your demo wants "success = jailbreak". |
| `OpenAIChatTarget` 401/404 against Azure | Make sure the endpoint ends with `/openai/v1` (the script appends it automatically) and `model_name` is the *deployment name*, not the model name. |

## Operational Tips

- Phase 3 and Phase 4 share the **same judge-provider routing** via `JUDGE_PROVIDER`.
- For `JUDGE_PROVIDER=openai`, evaluation uses `JUDGE_OPENAI_*` (with fallback to `OPENAI_*`).
- For `JUDGE_PROVIDER=azure-openai`, evaluation/red-team use `AZURE_*` judge variables.
- Keep the curated datasets (`eval/dataset.py`, `redteam/dataset.py`) short and high-signal — these scripts are demos, not coverage suites. Grow them incrementally.
- The MCP subprocess is spawned per Phase-3 run; expect cold-start latency on the first prompt. Phase 4 does **not** open the MCP server (red-team prompts attack the agent's chat behavior, not its tools).
- PyRIT is moving fast (v0.13 in 2026); pin the version in `pyproject.toml` before adding more scripts on top of it.
- Never commit `.env`, `.eval_outputs/`, or `.pyrit_outputs/` — they hold model outputs that may include sensitive data.

## References

### Microsoft Agent Framework

- First Python agent walk-through — https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent?pivots=programming-language-python
- Connecting MCP tools — https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/mcp-tools?pivots=programming-language-python
- Foundry chat client reference — https://learn.microsoft.com/en-us/python/api/agent-framework-foundry/

### Azure AI Foundry

- RBAC for Foundry — https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-foundry
- Agent evaluators (SDK) — https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators

### PyRIT

- GitHub (current) — https://github.com/microsoft/PyRIT
- Documentation site — https://microsoft.github.io/PyRIT/
- "Sending a Million Prompts" cookbook — https://microsoft.github.io/PyRIT/cookbooks/1_sending_prompts
- True/false scorers — https://microsoft.github.io/PyRIT/code/scoring/2_true_false_scorers
- OpenAI / Azure OpenAI chat target — https://microsoft.github.io/PyRIT/code/targets/1_openai_chat_target
- Microsoft Security blog announcement (Feb 22, 2024) — https://www.microsoft.com/en-us/security/blog/2024/02/22/announcing-microsofts-open-automation-framework-to-red-team-generative-ai-systems/

### Sibling projects in this workspace

- [`../adk_financial_mcp_server`](../adk_financial_mcp_server) — the stdio finance MCP server attached in Phase 2.
- [`../evaluation`](../evaluation) — DeepEval / Inspect AI / Azure AI Evaluation SDK reference scripts; `03_azure_ai_eval_agents.py` is the direct ancestor of `ms_agent_app/eval/score.py`.
- [`../azure_foundry_sharepoint`](../azure_foundry_sharepoint) — earlier Foundry agent (Streamlit + SharePoint grounding) used as the skeleton for `.env` layout and credential reuse.


## Prompt Hacking Reference
- https://learnprompting.org/docs/prompt_hacking/introduction
