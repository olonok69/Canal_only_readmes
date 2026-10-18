# Gemini CLI + Financial MCP Toolkit

This repository combines:

- A **Gemini CLI workflow** (skills, memory, planning, automation).
- A production-grade **financial MCP server** (`server/`) with 15+ strategy/fundamental tools.
- An **ADK/FastAPI orchestration API** (`stock_analyzer_bot/`) that consumes MCP tools.

The README is aligned with `GEMINI_CLI_GUIDE_EN.md` and `CLI material.txt`, with examples adapted to this codebase.

---

## Repository Layout

```text
.
├── server/                    # MCP server + optional OpenAPI layer
│   ├── main.py                # MCP entrypoint (FastMCP stdio)
│   ├── api_main.py            # REST/OpenAPI interface for analysis tools
│   ├── tool_registry.py       # Central tool registration
│   └── strategies/            # Strategy + scanner + fundamental modules
├── stock_analyzer_bot/        # ADK multi-agent API over MCP tools
│   ├── api.py                 # FastAPI endpoints (technical/scanner/fundamental/etc.)
│   ├── adk_bot.py             # Orchestrator/specialist/critic/reporter pipeline
│   └── mcp_tools.py           # Deterministic wrappers around MCP calls
├── skills-cli/                # Reusable skill assets (security-review)
├── test_outputs/              # Example generated analysis outputs
├── GEMINI.md                  # Project-level persistent behavior instructions
├── GEMINI_CLI_GUIDE_EN.md     # Main reference guide
└── CLI material.txt           # MCP + skills + planning implementation notes
```

---

## 1) What is Gemini CLI?

Gemini CLI is a terminal AI orchestrator that can:

- Analyze and edit local code.
- Run shell commands (with confirmation/safety controls).
- Connect to external tools through **MCP servers**.
- Apply project rules via `GEMINI.md` and local skills.

In this repo, Gemini CLI is used primarily as the interface for the `finance-tools` MCP server.

---

## 2) Installation and Setup

### Prerequisites

- **Node.js 20+** (Gemini CLI)
- **Python 3.11+** (MCP server and APIs)
- Internet access for market data (`yfinance`) and model providers

### Install Gemini CLI

```bash
npm install -g @google/gemini-cli
```

Alternative:

```bash
npx @google/gemini-cli
```

### Install Python dependencies

From the repository root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Authenticate Gemini CLI

Run:

```bash
gemini
```

Then complete browser login, or set:

```powershell
$env:GEMINI_API_KEY="YOUR_KEY"
```

---

## 3) File Management with Gemini CLI

Use `@` to include code/files in context:

- `Refactor @server/tool_registry.py`
- `Review @stock_analyzer_bot/api.py for endpoint consistency`
- `Summarize strategy logic in @server/strategies/`

Useful patterns:

```bash
gemini "Generate docs for @server/main.py" > server_docs.md
gemini "Find where analyze_trin_market_breadth is used"
```

---

## 4) Agent Skills (security-review)

This repo includes a ready skill template in `skills-cli/`.

### Register locally

Create:

```text
.gemini/skills/security-review/SKILL.md
.gemini/skills/security-review/scripts/download.js
```

Then copy:

- `skills-cli/SKILL.md` → `.gemini/skills/security-review/SKILL.md`
- `skills-cli/download.js` → `.gemini/skills/security-review/scripts/download.js`

Skill behavior:

- Pulls OWASP Top 10 categories from `https://owasp.org/Top10/`
- Audits selected code/endpoints
- Produces a Markdown report with severity, evidence, remediation

Trigger phrases:

- `check-security`
- `review-security`
- `audit-security`

---

## 5) Memory and Context Management

This project uses `GEMINI.md` as persistent instruction context.

Main policy in this repo:

- Use MCP tools as execution engine for financial analysis.
- Follow dialog-first intake (objective, symbols/sectors, period, mode, risk profile).
- Use mode-aware reporting (`strategy` vs `score`) and avoid fabricated metrics.

Context sources:

- **Project memory:** `GEMINI.md`
- **Ad-hoc context:** `@path/to/file`
- **Cross-session memory:** explicit “remember ...” instructions in Gemini CLI

---

## 6) Shell Commands

Inside Gemini CLI:

- Run direct shell commands with `!` (for example: `!git status`).
- Ask the assistant to run tests, linters, or startup commands.

Typical local commands for this repo:

```bash
python server/main.py
uvicorn server.api_main:app --reload
uvicorn stock_analyzer_bot.api:app --reload --port 8001
```

---

## 7) Sessions and History

Useful session commands:

- `gemini --resume` to continue previous sessions
- `/resume` to browse/search past sessions
- `/rewind` to undo recent conversation/code turns

This is helpful when iterating on strategy prompts, API schemas, or migration plans.

---

## 8) Task Planning (Todos)

For complex changes, use planning-first prompts, e.g.:

- “Make a plan first, then save as todo list in Markdown.”

Examples in this repo:

- `OPENAPI_MIGRATION_PLAN.md`
- `todo.md`

Recommended flow:

1. Ask Gemini CLI for a plan.
2. Save it as a markdown todo checklist.
3. Execute tasks incrementally and validate after each phase.

---

## 9) Web Search and Fetch

Gemini CLI can search/fetch documentation and apply it to local code:

- Find breaking changes before updating dependencies.
- Pull external references for strategy validation.
- Fetch docs and adapt examples to files in this repo.

Example prompt:

- “Fetch latest FastAPI auth patterns and apply to `server/api_main.py`.”

---

## 10) MCP Server Setup (`finance-tools`)

### Run the MCP server

```bash
python server/main.py
```

### Add server to Gemini CLI

```bash
gemini mcp add finance-tools python D:\repos\gemini-cli\server\main.py
```

### Refresh and verify in active Gemini session

```text
/mcp refresh
/mcp list
```

You can also configure manually in `.gemini/settings.json`:

```json
{
  "mcpServers": {
    "finance-tools": {
      "command": "python",
      "args": ["D:\\repos\\gemini-cli\\server\\main.py"]
    }
  }
}
```

---

## 11) Automation (Headless Mode)

Gemini CLI can run non-interactively for scripts/CI:

```bash
git diff --staged | gemini "Write a concise commit message" > commit_msg.txt
gemini "Summarize @server/tool_registry.py and output JSON" --output-format json
tail -n 100 logs.txt | gemini "Analyze failures and suggest fixes" > report.md
```

---

## Finance Capabilities in This Repo

`server/tool_registry.py` registers an extended catalog including:

- Core strategy scoring (Bollinger-Fibonacci, MACD-Donchian, Connors+ZScore, Dual MA, Bollinger Z-Score, Bollinger Z-Score RSI)
- Breadth/event/volatility/relative-value tools (TRIN, overnight gaps, earnings momentum, breakout/fade, multi-timeframe, pairs, stat-arb, VIX term structure, volatility regime)
- Performance/backtesting tools
- Unified scanner + comprehensive report tools
- Fundamental analysis + financial statement index tools

---

## API Layers

- `server/api_main.py`: OpenAPI-first REST interface for direct strategy/fundamental/scanner endpoints.
- `stock_analyzer_bot/api.py`: ADK multi-agent API (orchestrator/specialist/critic/reporter) over MCP tools.

This separation allows:

- deterministic direct tool access (OpenAPI), and
- higher-level narrative/guardrailed analysis (ADK path).

---

## Quick Start Summary

1. Install Gemini CLI and Python dependencies.
2. Start MCP server: `python server/main.py`.
3. Register MCP server: `gemini mcp add finance-tools ...`.
4. In Gemini session: `/mcp refresh` then `/mcp list`.
5. Run analysis prompts using the MCP tools.

---

## Disclaimer

This project is for research/education workflows. It does **not** provide financial advice. Always validate assumptions, data quality, and risk constraints before making decisions.
