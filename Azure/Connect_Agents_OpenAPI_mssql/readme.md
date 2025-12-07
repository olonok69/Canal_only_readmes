# Azure AI Foundry OpenAPI SQL Chatbot

This project hosts a command-line chatbot that runs on Azure AI Foundry Agents and is powered by an OpenAPI tool exposing a read-only SQL surface. Azure AI Foundry Agents provide a managed orchestration layer for creating, running, and scaling AI assistants that can call tools and maintain conversational context. OpenAPI is a vendor-neutral specification for describing HTTP APIs in a machine-readable JSON or YAML format, enabling automatic validation and client generation. The agent can inspect database metadata and run SELECT queries through the provided OpenAPI spec, returning structured answers directly in the chat loop.

## Features

- Single Azure AI Foundry agent wired to a custom OpenAPI SQL tool.
- Interactive CLI loop for natural language questions about the connected dataset.
- Automatic enforcement of read-only SQL via the OpenAPI schema.
- Optional cleanup flag to delete the transient agent after each run.

## Prerequisites

- Python 3.9 or later.
- An Azure AI Foundry project with a language model deployment (for example, `gpt-4o-mini`).
- A service principal with access to the project endpoint.
- An OpenAPI connection in the Azure AI project that injects the `data-sql` header required by `schema.json`.

## Installation

1. **Clone and enter the repository**
   ```powershell
   git clone https://github.com/olonok69/multi-agent-solution.git
   Set-Location multi-agent-solution\foundry_agent_openapi
   ```

2. **Create and activate a virtual environment**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```
# Azure AI project
PROJECT_ENDPOINT=https://<your-project-region>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=<model-deployment-name>
PROJECT_OPENAPI_CONNECTION_NAME=<existing-openapi-connection-name>

# Service principal credentials
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
AZURE_CLIENT_SECRET=<client-secret>

# Optional
DELETE_CREATED_AGENT=false
```

### Key Files

- `main.py` – Entry point that loads the OpenAPI spec, creates the agent, and runs the interactive chat loop.
- `schema.json` – OpenAPI 3.1 document defining four read-only SQL helper endpoints (`list_tables`, `describe_table`, `get_table_sample`, `execute_sql`). The `data-sql` header matches the Azure connection security scheme `dataSqlHeader`.

## Usage

Run the chatbot from the project directory:

```powershell
python main.py
```

1. The script creates the OpenAPI tool using `schema.json` and the connection identified by `PROJECT_OPENAPI_CONNECTION_NAME`.
2. An agent named `openapi_chat_agent` is registered with that tool and a conversation thread is created.
3. You are dropped into a CLI loop. Ask natural language questions such as:
   - `List the available tables.`
   - `Describe the columns in tbl_asp_exhibitors.`
   - `Run a select to count registrations by day.`
4. Type `exit` (or press `Ctrl+C`) to leave the loop. If `DELETE_CREATED_AGENT` is truthy (`true`, `1`, `yes`, `y`), the agent is deleted before the script exits.

## Tests

Run the schema-focused unit tests to verify that `schema.json` retains the expected security scheme and read-only endpoints:

```powershell
python -m unittest discover -s test
```

The suite in `test/test_schema.py` loads the OpenAPI document and checks for:
- Presence of the `dataSqlHeader` security scheme with the correct `data-sql` header mapping.
- Enforcement of the four read-only endpoints (`list_tables`, `describe_table`, `get_table_sample`, `execute_sql`).
- Project-wide security configuration requiring the Azure connection header.

## Troubleshooting

- **401 Unauthorized when calling the API**: Verify that the Azure AI connection’s injected header name is `data-sql` and that the connection name matches `PROJECT_OPENAPI_CONNECTION_NAME` in `.env`.
- **Model not found**: Confirm the deployment name in `.env` matches the deployment registered with your Azure AI project.
- **Missing environment variables**: The script relies on `python-dotenv`; ensure `.env` is present or export the variables in your shell.

## Next Steps

- Extend `schema.json` with additional read-only endpoints if your dataset grows.
- Wrap the CLI in a web or Teams interface by reusing the same agent/thread pattern.
- Automate runs via CI/CD after securing secrets in Azure Key Vault or GitHub Actions secrets.
- Consult the Azure AI Agents Python SDK overview for advanced usage: https://learn.microsoft.com/en-us/python/api/overview/azure/ai-agents-readme?view=azure-python
- Refer to the OpenAPI Specification for schema design guidance: https://swagger.io/specification/
