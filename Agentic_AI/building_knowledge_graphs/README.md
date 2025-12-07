# Agentic Knowledge Graph (Modular App)

This repository contains a modular application that builds a Product → Assembly → Part → Supplier knowledge graph in Neo4j using CSV files. It separates responsibilities into agents and a central orchestrator, with configuration in YAML, secrets in `.env`, and robust logging.

Quick links:
- Pipeline deep-dive: docs/PIPELINE.md (English) · docs/PIPELINE.es.md (Español)
- Unstructured schema demo (L8-style): docs/UNSTRUCTURED_DEMO.md
- Text extraction → graph ingest demo: docs/EXTRACTION_DEMO.md

- Architecture overview: `images/app_architecture.svg`
- Data workflow: `images/app_data_workflow.svg`
- Ingest sequence: `images/ingest_sequence.svg`

Pipeline overview:

![Entire solution](images/entire_solution_v2.svg)

![Architecture](images/app_architecture.svg)

## Quick Start (Windows PowerShell)

1) Install dependencies
```
pip install -r requirements_app.txt
```

2) Configure Neo4j connection in `.env`
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j
NEO4J_IMPORT_DIR=C:\\Path\\to\\Neo4j\\import
```

3) Sanity check
```
python -m agentic_kg_app.cli ready --config .\configs\app.yaml
```

4) Load the sample CSVs
```
python -m agentic_kg_app.cli ingest --config .\configs\app.yaml --data-dir .\data
```

5) Run the pipeline (structured)
```
python -m agentic_kg_app.cli pipeline --config .\configs\app.yaml --data-dir .\data --llm --schema structured
```

6) Run the pipeline (unstructured schema from .md/.txt → maps to CSV ingest)
```
python -m agentic_kg_app.cli pipeline --config .\configs\unstructured_demo.yaml --data-dir .\data --llm --schema unstructured --text-dir .\unstructured
```

7) NEW: Extract instances directly from text (bypass CSV)
```
python -m agentic_kg_app.cli pipeline --config .\configs\unstructured_demo.yaml --extract-from-text --text-file .\unstructured\extract_demo.md --llm
```

8) Explore the graph
```
python .\examples\query_kg.py
python .\examples\query_extracted.py
```

## What the app does

- Loads configuration from `configs/app.yaml` and environment variables from `.env`
- Provides an agentic pipeline: parse user intent → suggest files → propose schema (structured + unstructured) → choose schema → ingest
- Ensures uniqueness constraints per node label and key
- Loads nodes/relationships using one of three ingest paths, chosen automatically:
  - Local Neo4j: copy CSVs to `NEO4J_IMPORT_DIR` and use `LOAD CSV`
  - Aura with hosted CSVs: use HTTP(S) `LOAD CSV` via `csv_base_url`
  - Aura (or when file imports are unavailable): stream local CSVs via `UNWIND` batches (no `LOAD CSV`)
- Provides utility commands to check readiness and reset the graph
- Logs to console and to a rotating file `logs/app.log`

## Package structure

```
agentic_kg_app/
  __init__.py
  cli.py                # Entry point for commands (ready/reset/ingest)
  orchestrator.py       # Wires config, logging, Neo4j client, and agents
  config.py             # YAML + .env configuration loader and validation
  logging_setup.py      # Console + rotating file logging
  neo4j_client.py       # Thin wrapper around neo4j driver and helpers
  utils.py              # Helpers (copy CSVs, build dynamic SET clauses)
  agents/
    __init__.py
    data_ingest_agent.py  # Copy CSVs, constraints, load nodes/relationships
    graph_ops_agent.py    # Ready, clear graph, version checks
    user_intent_agent.py  # Parse user goal (heuristic or LLM)
    file_suggestions_agent.py  # Suggest relevant CSVs (heuristic or LLM)
    schema_proposal_structured_agent.py  # Infer ingestable schema from CSVs
    schema_proposal_unstructured_agent.py  # Infer abstract schema from free text
    unstructured_ingest_agent.py  # NEW: extract entities/relations from text and ingest (instances from .md/.txt)
configs/
  app.yaml             # App configuration (nodes, relationships, logging, Neo4j)
  unstructured_demo.yaml  # NEW: convenience config for unstructured demos
images/
  app_architecture.svg
  app_data_workflow.svg
  ingest_sequence.svg
  entire_solution.png
docs/
  PIPELINE.md · PIPELINE.es.md
  UNSTRUCTURED_DEMO.md  # Run schema-from-text with .md input, then ingest CSVs
  EXTRACTION_DEMO.md    # Run instance extraction from .md/.txt and ingest directly
```

## How it works

![Data workflow](images/app_data_workflow.svg)

1. You run a CLI command (e.g., `pipeline` or `ingest`) with a `--config` path and optional `--data-dir`.
2. The Orchestrator loads YAML and merges `.env` values, configures logging, and creates the Neo4j client.
3. Depending on the command:
  - Pipeline: agents collaborate to parse intent → suggest files → propose schemas → you select a schema → ingest runs with that schema.
  - Ingest: directly applies the schema declared in `configs/app.yaml`.
4. Uniqueness constraints are ensured per node type and key.
5. Ingest path is selected:
  - `LOAD CSV file:///` for local Neo4j when `NEO4J_IMPORT_DIR` is writable.
  - `LOAD CSV https://...` when `csv_base_url` is configured (ideal for Aura).
  - Streaming via `UNWIND` batches when file imports are not available or you prefer not to host CSVs.
6. Logging is emitted to console and to `logs/app.log` (rotating).

### Ingest sequence

![Ingest sequence](images/ingest_sequence.svg)

- `python -m agentic_kg_app.cli ingest --config .\configs\app.yaml --data-dir .\data`
- Load YAML & merge `.env` → setup logging → create Neo4j client
- Copy CSVs → create constraints → load nodes → load relationships
- Return success or a clear error message

## Configuration

`configs/app.yaml` controls nodes, relationships, logging, and Neo4j connection defaults. Environment variables can override values.

Example highlights:

- Neo4j connection (values can be provided via `.env`):
```
neo4j:
  uri: "${NEO4J_URI}"
  username: "${NEO4J_USERNAME}"
  password: "${NEO4J_PASSWORD}"
  database: "${NEO4J_DATABASE}"
  import_dir: "${NEO4J_IMPORT_DIR}"
```

- Node sources (CSV file, label, unique key, properties to set):
```
nodes:
  - file: products.csv
    label: Product
    unique_key: product_id
    properties: [product_name, price, description]
  - file: assemblies.csv
    label: Assembly
    unique_key: assembly_id
    properties: [assembly_name, quantity, product_id]
  - file: parts.csv
    label: Part
    unique_key: part_id
    properties: [part_name, quantity, assembly_id]
  - file: suppliers.csv
    label: Supplier
    unique_key: supplier_id
    properties: [name, specialty, city, country, website, contact_email]
```

- Relationship mappings (CSV file, edge type, from/to labels and keys):
```
relationships:
  - file: assemblies.csv
    type: HAS_ASSEMBLY
    from_label: Product
    from_key: product_id
    to_label: Assembly
    to_key: assembly_id
  - file: parts.csv
    type: HAS_PART
    from_label: Assembly
    from_key: assembly_id
    to_label: Part
    to_key: part_id
  - file: part_supplier_mapping.csv
    type: SUPPLIED_BY
    from_label: Part
    from_key: part_id
    to_label: Supplier
    to_key: supplier_id
```

- Logging configuration:
```
logging:
  level: INFO
  dir: logs
  file: app.log
  maxBytes: 5000000
  backupCount: 3
```

## Environment variables

Create a `.env` at the repo root (copy from `.env.example`) and fill in values:

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j
NEO4J_IMPORT_DIR=C:\\Path\\to\\Neo4j\\import
```

- `NEO4J_IMPORT_DIR` must point to your Neo4j server’s import directory for `LOAD CSV`.
- If not provided, the app attempts to discover the import directory via `dbms.listConfig()`.

Optional (LLM/ADK):

```
# Choose one of these providers
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# Optional: prefer an explicit model; provider prefix is supported
LLM_MODEL=openai/gpt-4.1
```

Model/provider selection:
- If you pass a model without a prefix (e.g., `gpt-4.1`), the app infers the provider (`openai/gpt-4.1`).
- If both OpenAI and Google keys are present, set `LLM_MODEL` to remove ambiguity.

## Logging

- Console logging and a rotating file at `logs/app.log` are enabled by default (configurable in YAML).
- Rotate size and backup count can be tuned via the `logging` section.

## CLI usage (PowerShell)

Check connectivity:
```
python -m agentic_kg_app.cli ready --config .\configs\app.yaml
```

Reset the graph (DESTRUCTIVE – removes all nodes and relationships):
```
python -m agentic_kg_app.cli reset --config .\configs\app.yaml
```

Ingest all CSVs from `data/` into Neo4j (copies required files to the import directory first):
```
python -m agentic_kg_app.cli ingest --config .\configs\app.yaml --data-dir .\data
```

Run the guided pipeline:
```
python -m agentic_kg_app.cli pipeline --config .\configs\app.yaml --data-dir .\data
```

Enable LLM-powered agents and choose schema non-interactively:
```
python -m agentic_kg_app.cli pipeline --config .\configs\app.yaml --data-dir .\data --llm --schema structured
```

Flags:
- `--llm` uses LLM-backed agents with heuristic fallback.
- `--text` seeds the unstructured schema agent (default provided).
- `--schema structured|unstructured|1|2` selects which proposal to apply without a prompt.
- `--text-file` can be provided multiple times to include .md/.txt files as unstructured inputs.
- `--text-dir` includes all .md/.txt under a directory (recursively) as unstructured inputs.
- `--extract-from-text` runs the new instance extraction path (see below), bypassing CSV ingest.

### Pipeline stages explained

1) User Intent (UserIntentAgent)
- Heuristic or LLM extracts `{kind, description}` of the KG to build.

2) File Suggestions (FileSuggestionsAgent)
- Scans `--data-dir` for CSVs and ranks relevance; LLM can refine approvals.

3) Schema Proposals
- Structured (SchemaProposalStructuredAgent): infers nodes and relationships from the approved CSVs.
- Unstructured (SchemaProposalUnstructuredAgent): infers entities/relations from free text; we then materialize an ingestable schema by mapping to your dataset’s files/keys.

4) Selection
- You choose between the structured and unstructured proposals (or pass `--schema` to auto-select).

5) Ingest
- Ensures uniqueness constraints, then loads nodes and relationships via the best available ingest mode (local LOAD CSV, HTTP(S) LOAD CSV, or streaming UNWIND).

### Unstructured schema demo (L8-style)

Use .md/.txt to derive a schema (labels/relations) with the LLM, then map to your CSVs and ingest:

```
# From repo root
python -m agentic_kg_app.cli pipeline --config .\configs\unstructured_demo.yaml --data-dir .\data --llm --schema unstructured --text-dir .\unstructured
```

See docs/UNSTRUCTURED_DEMO.md for details.

### NEW: Extract instances from unstructured text (bypass CSV)

If you want to create a small KG directly from text, use the extraction path:

```
# Single file
python -m agentic_kg_app.cli pipeline --config .\configs\unstructured_demo.yaml --extract-from-text --text-file .\unstructured\extract_demo.md --llm

# Or an entire folder of .md/.txt
python -m agentic_kg_app.cli pipeline --config .\configs\unstructured_demo.yaml --extract-from-text --text-dir .\unstructured --llm
```

What it does:
- Calls an LLM to produce JSON with nodes (label, key?, properties) and relationships (type, from/to label+key?).
- Generates a stable `_key` if none is provided (hash of label+name/properties).
- Ingests nodes and edges via UNWIND. This can coexist with your CSV-based graph.

See docs/EXTRACTION_DEMO.md for verification steps and notes.

### Example: Query the Knowledge Graph

After running ingest or the pipeline, you can query the graph using the example script:

```
python .\examples\query_kg.py --config .\configs\app.yaml
```

This prints:
- Top 5 products,
- Assemblies for a sample product (P-1001),
- Parts and suppliers for a sample assembly (A-1062).

## Dependencies

Install the minimal dependencies for the app:
```
pip install -r requirements_app.txt
```

Alternatively, ensure these packages are available in your environment:
- neo4j
- python-dotenv
- PyYAML

## Troubleshooting

- SVG render error (XML entity): If you see `xmlParseEntityRef: no name`, ensure any `&` in text is written as `&amp;` in SVG files. This has been fixed in the included diagrams.
- Neo4j authentication: Ensure `NEO4J_URI`, `NEO4J_USERNAME`, and `NEO4J_PASSWORD` are correct and the database is running.
- Import directory permission: The user running the app must have permission to write into the Neo4j import directory.
- Mixed CSV encodings: Expected UTF-8. If you have other encodings, convert or adjust the loader accordingly.

## Running on Neo4j Aura

Neo4j Aura does not permit `file:///` CSV imports. Use HTTP(S) hosted CSVs and set a base URL:

1) Host your CSVs somewhere publicly accessible over HTTPS, for example:
  - GitHub raw: `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/data`
  - Cloud storage with public read (Azure Blob Static Website, S3, GCS, etc.)
2) Configure a base URL in either place:
  - In `configs/app.yaml` → `csv_base_url: "${NEO4J_CSV_BASE_URL}"`
  - Or in `.env` → `NEO4J_CSV_BASE_URL=https://.../data`
3) Run ingest as usual:
  - `python -m agentic_kg_app.cli ingest --config .\configs\app.yaml --data-dir .\data`

When `csv_base_url` is set, the app will:
- Build URLs like `https://.../products.csv` instead of `file:///products.csv`
- Skip copying files to the Neo4j import directory entirely
- Work without requiring `dbms.security.allow_csv_import_from_file_urls`

Alternative (no hosting): Streaming ingest

If you prefer not to host CSVs, the app can stream local CSVs into Aura using batched `UNWIND`. This avoids `LOAD CSV` entirely. This mode is chosen automatically when file imports are unavailable and no `csv_base_url` is configured.

## Extending

- Add APOC-powered procedures in agents for faster/bulk operations.
- Add more node/edge sources by extending `configs/app.yaml`.
- Add tests using a local Neo4j test container or mock the client.

---

With the above architecture and configuration, you can reproduce and extend this agentic knowledge graph in a clean, maintainable app structure.

## ADK integration and LLM-powered agents

This app includes optional adapters for Google ADK and LLM-backed flows. If you don’t install ADK/LLM deps, the core CLI still works.

### Install optional dependencies

```
pip install google-adk==1.5.0 google-genai>=0.3.0 litellm==1.73.6
```

Add keys to your `.env`:

```
# One of these is enough
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# optional, to override autodetected model (provider prefix supported)
LLM_MODEL=openai/gpt-4.1
```

### Available ADK tools and agents

- ADK tools wrapper: `agentic_kg_app/adk/tools_adk.py`
  - `neo4j_is_ready`, `clear_neo4j_data`, `drop_neo4j_indexes`, `get_apoc_version`, `get_neo4j_version`, `sample_file`
  - State helpers: `get_approved_user_goal`, `get_approved_files`
- ADK bridge: `agentic_kg_app/adk/bridge.py` provides `AgentCaller` and `make_agent_caller`
- LLM router: `agentic_kg_app/adk/llm.py` selects Gemini or OpenAI via `litellm`

### LLM-powered flows (with fallback)

- User intent: `UserIntentAgent.parse_llm(prompt)` → `{kind, description}`
- File suggestions: `FileSuggestionsAgent.suggest_llm(data_dir, user_goal)` → `approved_files`
- Schema proposal (structured): `SchemaProposalStructuredAgent.propose_llm(data_dir, approved_files)` → nodes/relationships
- Schema proposal (unstructured): `SchemaProposalUnstructuredAgent.propose_llm(texts)` → entities/relations

All LLM methods fall back to deterministic heuristics if no key is configured or the call fails. The app also normalizes model names (e.g., `gpt-4.1` → `openai/gpt-4.1`) to avoid provider errors.

### Minimal example

```python
from pathlib import Path
from agentic_kg_app.orchestrator import Orchestrator

orch = Orchestrator("configs/app.yaml")

ui = orch.user_intent.parse_llm("Please build a product-assembly-part-supplier graph for BOM analysis")
approved = orch.file_suggestions.suggest_llm(Path("data"), user_goal=ui.description)
schema = orch.schema_proposal_structured.propose_llm(Path("data"), approved.get("approved_files", []))
schema_u = orch.schema_proposal_unstructured.propose_llm([
    "Products are composed of assemblies. Parts are supplied by suppliers."
])

print(ui)
print(approved)
print(schema)
print(schema_u)

orch.close()
```

If you prefer a pure-ADK flow, you can use `AgentCaller` and pass state with `approved_user_goal` / `approved_files` while invoking `ADKTools` within your agent graph.
