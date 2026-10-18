## Deep Research Ai Agent

Production-ready research agent built on the [deepagents](https://github.com/langchain-ai/deepagents) stack. The project packages a fully wired example that exercises task planning, file-based memory, sub-agent delegation, and a dual web-research toolchain that now integrates Tavily search with optional Perplexity synthesis.

## Highlights
- Task planning with mandatory TODO creation, recitation, and status tracking
- File system offloading so every tool call saves durable artifacts
- Sub-agent delegation for focused, parallel research threads
- Dual research pipeline: Tavily for raw evidence, Perplexity for cited synthesis when configured
- CLI, programmatic, and streaming entry points with artifact export support

## Architecture

![Architecture diagram](docs/architecture.svg)

Optional Perplexity tool plugs into the main agent's evidence gathering loop to produce an additional cited summary that is persisted alongside Tavily results.

## What the Agent Guarantees
- Always creates TODO lists for non-trivial work, recites them before major decisions, and tracks status
- Persists every important artifact (TODO summary, tool outputs, final report) when `--save-artifacts` is enabled
- Executes Tavily search first and Perplexity synthesis second whenever Perplexity is available, storing each result in separate files
- Delegates deep dives to sub-agents with isolated context when extra focus is needed

## Setup

### Prerequisites
- Python 3.11+
- [Tavily](https://tavily.com) API key
- LLM provider key supported by LangChain (OpenAI or Anthropic out of the box)
- Optional [Perplexity](https://www.perplexity.ai/) API key for synthesis

### Install dependencies
```bash
pip install -r requirements.txt
```

Recommended alternative using [uv](https://github.com/astral-sh/uv):
```bash
uv pip install -r requirements.txt
```

### Configure environment
1. Copy the template (if available) and create a `.env` file alongside `research_agent.py`.
2. Provide the required keys:

```
TAVILY_API_KEY=...
# Choose the provider you will use
OPENAI_API_KEY=...    # if provider=openai
ANTHROPIC_API_KEY=... # if provider=anthropic

# Optional integrations
PERPLEXITY_API_KEY=...
PERPLEXITY_MODEL=sonar-reasoning-pro   # optional override
LANGSMITH_API_KEY=...
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=deep-research-agent
```

If `PERPLEXITY_API_KEY` is present and the `perplexity`/`perplexityai` SDK is installed, the agent automatically exposes the `perplexity_research` tool and enforces the dual-tool workflow.

## Running the agent

```bash
python research_agent.py [--provider openai|anthropic] [--model <model-id>] \
    [--temperature 0.0] [--max-concurrent 3] [--max-iterations 10] \
    [--save-artifacts] [--artifact-dir artifacts]
```

You will be prompted to choose between:
- **Example mode** – runs bundled sample queries so you can observe TODO creation, tool usage, and artifact capture
- **Interactive mode** – accepts your own prompt and produces a final research report

When `--save-artifacts` is supplied, each run creates a timestamped folder inside `--artifact-dir` containing:
- `final_report.md` – the assistant's final message
- `todos.md` – every recorded TODO with status history
- `agent_files/` – all files written by the agent (evidence dumps, Perplexity summaries, drafts) plus an index manifest

## Programmatic access

```python
from research_agent import DeepResearchAgent

agent = DeepResearchAgent(
    provider="openai",             # or "anthropic"
    model_name="gpt-4.1",          # provider prefix optional when it matches
    temperature=0.0,
    max_concurrent_research_units=3,
    max_researcher_iterations=10,
)

result = agent.research("Latest advances in quantum machine learning")
report = result["messages"][-1].content
print(report)

# Stream updates instead of waiting for completion
agent.stream_research("Compare EV vs hydrogen fuel adoption constraints")
```

The returned payload includes the final message, captured TODO list, and the complete set of files the agent wrote so you can persist or post-process them however you like.

## Tooling

| Tool | Purpose |
|------|---------|
| `write_todos` / `read_todos` | Manage task plans with explicit status updates |
| `ls`, `read_file`, `write_file`, `edit_file` | Virtual filesystem for context offloading |
| `task` | Delegate work to registered sub-agents |
| `internet_search` | Tavily search (configurable topic, max results, raw content) |
| `perplexity_research` | Optional Perplexity summary with inline citations |

All tools write their important outputs to files as part of the governed workflow, ensuring artifacts survive beyond the conversation.

## Workflow in practice
1. **Plan** – Immediately writes a structured TODO list covering planning, each tool call, file review, and synthesis tasks.
2. **Orient** – Saves the user’s prompt, lists existing files, and reads any prior context if present.
3. **Gather** – Calls Tavily first, stores raw evidence, then calls Perplexity (when configured) for a cited synopsis stored separately.
4. **Organise** – Reads saved files, optionally launches sub-agents for deep dives, and keeps TODOs in sync.
5. **Synthesize** – Produces a citation-rich report referencing all gathered evidence.
6. **Recite** – Reviews the TODO list aloud, verifies every step was completed, and only then finalises the response.

## Artifact layout

```
artifacts/
  20251116-101504_latest-advances-in-quantum-ml-and-applications-of-quantum-ml-in-real-world/
    final_report.md
    todos.md
    agent_files/
      index.md
      tavily_findings.md
      perplexity_summary.md
      ...
```

The directory structure makes it easy to inspect runs later, diff reports, or feed the outputs into downstream workflows.

## Troubleshooting
- **Missing API keys** – The script stops with a clear error listing missing keys; double-check `.env`.
- **Perplexity tool not listed** – Either `PERPLEXITY_API_KEY` is absent or the SDK is not installed (`pip install perplexity` or `pip install perplexityai`).
- **Model mismatch errors** – Ensure `--provider` aligns with the model name; you can prefix `provider:model` to skip inference.
- **Empty artifact folders** – The agent only persists files when `--save-artifacts` is set; otherwise it prints summaries to the console.

## Further reading
- [deepagents documentation](https://docs.langchain.com/oss/python/deepagents/overview)
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)

## License and contributions

This project is provided as-is for educational and research purposes. Feel free to fork and adapt it for your own use cases and based on the course Deep Agents from Scratch curriculum with proper attribution of almost all code. I only extend it with Perprexity integration and some additional Logic together with Spanish translation.

```python
