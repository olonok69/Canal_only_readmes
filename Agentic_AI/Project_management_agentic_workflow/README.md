# AI-Powered Agentic Workflows for Project Management

## Project Overview

This repository showcases a two-phase journey for building agentic workflows that transform product specifications into actionable project plans. The agent library now resides in `lib/`, while the orchestrated workflow lives in `agents/`.

- **Agent Library (`lib/`)**: Implements prompt-based, knowledge-augmented, routing, and evaluation agents plus supporting tests. Each agent aligns with rubric expectations and is documented in `lib/README.md` and `lib/README-es.md`.
- **Orchestrated Workflow (`agents/`)**: Combines the library agents to ingest a product spec, generate user stories, features, and engineering tasks, and capture the full execution in a Markdown report. Documentation lives in `agents/README.md` and `agents/README-es.md`.

Spanish companions are provided for every README so the project can be explored in either language.

## Repository Structure

```
.
├── docs/                         # Reference PDFs on agentic workflows and RAG
├── examples/                     # Supplemental demo scripts exploring workflow patterns
├── lib/                          # Agent implementations, tests, and bilingual README
├── agents/                       # Orchestrated workflow, artifacts, and bilingual README
├── requirements.txt              # Shared Python dependencies
├── README.md                     # (This file) English project summary
└── README-es.md                  # Spanish project summary
```

## Quick Start

1. **Install dependencies** (from the repository root):
   ```powershell
   pip install -r requirements.txt
   ```

2. **Configure environment variables** by creating a `.env` file in the project root (or inside `agents/`) with:
   ```text
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-3.5-turbo            # optional override
   OPENAI_EMBEDDING_MODEL=text-embedding-3-large  # optional override
   ```

3. **Explore the agent library**:
   - Read `lib/README.md` for API details and usage examples.
   - Run individual agent scripts or tests, e.g.:
     ```powershell
     python lib\direct_prompt_agent_test.py
     python lib\routing_agent_test.py
     ```

4. **Run the orchestrated workflow** to generate a complete project plan and Markdown report:
   ```powershell
   python agents\agentic_workflow.py
   ```
   The run produces `agents\workflow_execution_report.md` and console logs describing routing decisions and evaluation outcomes.

## Documentation Map

- `lib/README.md` – English reference for all agents, usage patterns, and tests.
- `lib/README-es.md` – Spanish translation of the agent library guide.
- `agents/README.md` – English walkthrough of the orchestrated workflow, configuration, and customization tips.
- `agents/README-es.md` – Spanish translation of the orchestrated workflow guide.
- `docs/` – Supporting readings on retrieval-augmented generation and workflow modeling.

## Additional Notes

- The project was developed and validated without referencing real organizations or individuals.
- Optional enhancements (extended evaluation scoring, additional personas, richer logging) are outlined within the `lib/` and `agents/` READMEs for future exploration.
- For classroom context or rubric criteria, consult `project_overview.md`, `phase1.txt`, `phase2.txt`, and `Rubric.txt` in the repository root.

Enjoy exploring how modular AI agents can collaborate to deliver structured project plans!

# AI-Powered Agentic Workflow for Project Management

In this repo, you will find all the files and instructions required to complete the project. You can find more information about the project inside the Udacity Classroom.

## Getting Started

The project needs to be completed in two phases and you will find starter code for both the phases inside the `starter` folder in this repo. 

## Dependencies

A `requirements.txt` file has been provided in this repo if you want to work on the project locally. Otherwise, the workspace provided in the Udacity classroom has been configured with all the required libraries. 

## Project Instructions

You will find instructions for each of the two phases of the project in the README file inside the corresponding folder (`lib/` or `agents/`).



