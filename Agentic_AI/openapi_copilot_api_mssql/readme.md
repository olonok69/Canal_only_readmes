# Copilot OpenAPI Service

This repository hosts the Microsoft Copilot / Power Platform OpenAPI container that exposes a **read-only SQL surface** via Swagger 2.0 (OpenAPI 2.0) with API key authentication. It shares the same Nginx front end and Docker Compose scaffolding as the other services in this repo and is designed for import into Copilot Studio custom connectors.

## Architecture

![Copilot OpenAPI Architecture](docs/mcp-architecture-diagram-openapi.svg)

- Nginx handles TLS termination and forwards `/copilot/actions/*` to the container.
- The container serves a fixed Swagger 2.0 doc plus four read-only actions backed by MSSQL.
- API key is enforced at the edge and inside the service.

## Endpoints

Base path (public): `https://data.forensic-bot.com/copilot/actions/`

- `GET /health` (no auth)
- `GET /list_tables`
- `GET /describe_table?table_name=...`
- `POST /execute_sql` (body: `{ "query": "SELECT ..." }`)
- `GET /get_table_sample?table_name=...&limit=...`
- Swagger: `/swagger.json`

Each operation exposes a stable `operationId` (`list_tables`, `describe_table`, `execute_sql`, `get_table_sample`).

## Authentication

- Scheme: API key
- Header: defaults to `x-api-key` (override with `COPILOT_API_KEY_HEADER`)
- Value: `COPILOT_API_KEY`
- Invalid or missing keys return `401`.

## Behavior & Safety Rails

- Strictly read-only: rejects INSERT/UPDATE/DELETE/MERGE/DDL/transactions/stored procedures.
- Allows a single SELECT/WITH statement per request.
- Row values are stringified to align with Swagger 2.0/PowerFx expectations (null → empty string, datetime → ISO 8601, bytes → hex).
- `get_table_sample` limits: 1–1000 rows.

## Configuration

Environment variables (see `docker-compose.yml`):

| Variable | Purpose | Default |
| --- | --- | --- |
| `COPILOT_API_KEY` | API key value expected in the header | _(required)_ |
| `COPILOT_API_KEY_HEADER` | Header name to inspect | `x-api-key` |
| `OPENAPI_COPILOT_SERVER_URL` | URL published in the Swagger doc | `https://data.forensic-bot.com/copilot/actions` |
| `OPENAPI_COPILOT_PORT` | Container listen port | `8012` |
| `MSSQL_HOST`, `MSSQL_USER`, `MSSQL_PASSWORD`, `MSSQL_DATABASE`, `MSSQL_DRIVER`, `TrustServerCertificate`, `Trusted_Connection`, `READ_ONLY_MODE` | Shared DB configuration | _(required)_ |

## Deployment

The service is defined as `mcp-server-openapi-copilot` in `docker-compose.yml`, built from `Dockerfile.openapi_copilot`, exposed on port `8012`, and attached to `mcp-network`. Health check points to `/health`.

### Local run (compose)

```bash
docker compose build mcp-server-openapi-copilot
docker compose up -d mcp-server-openapi-copilot
docker compose logs -f mcp-server-openapi-copilot
```

For local testing, use `http://localhost:8012/` with the same paths and headers.

### Nginx routing

- Front end is shared with the other services; routing lives in `nginx/conf.d/default.conf`.
- Proxies `/copilot/actions/` to the container and forwards the API key header.
- CORS allows `GET, POST, OPTIONS` plus the configured key header, `Content-Type`, and `Accept`.

## Testing (curl)

```bash
# Health (no auth)
curl https://data.forensic-bot.com/copilot/actions/health

# List tables
curl -H "x-api-key: $COPILOT_API_KEY" \
  https://data.forensic-bot.com/copilot/actions/list_tables

# Execute SQL
curl -H "x-api-key: $COPILOT_API_KEY" -H "Content-Type: application/json" \
  -d '{"query":"SELECT TOP 3 * FROM dbo.YourTable"}' \
  https://data.forensic-bot.com/copilot/actions/execute_sql
```

## Import into Copilot Studio / Power Platform

1. Ensure the service is reachable at `https://data.forensic-bot.com/copilot/actions/swagger.json`.
2. In Copilot Studio (or Power Apps) custom connector wizard, import the Swagger 2.0 definition from that URL.
3. Set the API key parameter to the header you use (default `x-api-key`) and provide the value from `COPILOT_API_KEY`.
4. Test each action: `list_tables`, `describe_table`, `execute_sql`, `get_table_sample`.
