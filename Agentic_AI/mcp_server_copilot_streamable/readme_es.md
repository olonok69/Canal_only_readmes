# Servidor MCP Streamable para Copilot (OAuth)

Este repositorio se centra ahora en el **servidor MCP streamable para Microsoft Copilot**, que expone un set de herramientas SQL de solo lectura sobre el transporte MCP 2025-03-26 con OAuth 2.0. El servicio está detrás de Nginx en `https://data.forensic-bot.com/copilot` y está pensado para conexiones MCP en Copilot Studio (no custom connectors).

## Arquitectura

![Arquitectura Copilot Streamable MCP](docs/mcp-architecture-diagram-streamable-copilot.svg)

- Nginx termina TLS y proxy la ruta `/copilot/*` hacia el contenedor streamable.
- Incluye discovery OAuth, autorización, token y dynamic client registration.
- El endpoint MCP `/mcp` sirve las herramientas SQL con guardas de solo lectura.

## Endpoints

Base: `https://data.forensic-bot.com/copilot`

- MCP (POST/OPTIONS/DELETE; GET devuelve 405): `/mcp`
- OAuth discovery: `/.well-known/oauth-authorization-server`, `/.well-known/oauth-protected-resource`
- Flujos OAuth: `/authorize`, `/token`, `/register` (dynamic client registration)
- Health: `/health`

Notas
- Los clientes deben usar POST en `/mcp`; GET se rechaza a propósito.
- El header Accept debe incluir `application/json`; `text/event-stream` se acepta pero hoy las respuestas son solo JSON (no SSE).

## OAuth 2.0

- Grant: Authorization Code (principal) o Client Credentials para smoke tests. Se emiten refresh tokens, pero el refresh grant no está implementado; pide un token nuevo si caduca.
- Dynamic Client Registration: POST `/register` devuelve `client_id` y `client_secret`.
- Los hosts de redirect deben estar en `ALLOWED_REDIRECT_HOSTS` (docker-compose añade `global.consent.azure-apim.net`).
- Authorization/token/registration respetan `X-Environment-Path` enviado por Nginx (por defecto `/copilot`).

## Herramientas MCP

El servidor expone cuatro herramientas de solo lectura:
- `list_tables`: lista tablas en MSSQL
- `describe_table`: metadatos de columnas
- `execute_sql`: SELECT/WITH/SHOW/DESCRIBE/EXPLAIN con guardas
- `get_table_sample`: filas de muestra (default 5, máximo 1000)

## Seguridad y comportamiento

- Solo lectura: bloquea INSERT/UPDATE/DELETE/MERGE/DDL/transactions/stored procedures; solo una sentencia.
- Validación de tabla/query para evitar entradas inseguras y payloads multi-statement.
- Respuestas en JSON; no se emiten SSE streams.

## Configuración (env)

| Variable | Propósito | Default |
| --- | --- | --- |
| `STREAMABLE_COPILOT_PORT` | Puerto de escucha del contenedor | `8013` |
| `ENVIRONMENT_PATH` | Prefijo de ruta en respuestas de discovery | `/copilot` |
| `SERVER_NAME` | Nombre mostrado del servidor MCP | `Copilot Streamable SQL` |
| `ALLOWED_REDIRECT_HOSTS` | Hosts de redirect permitidos | `copilot.microsoft.com,powerva.microsoft.com,agents.microsoft.com,microsoft.com,openai.com,chatgpt.com,claude.ai,anthropic.com` (compose añade `global.consent.azure-apim.net`) |
| `READ_ONLY_MODE` | Fuerza guardas de solo lectura | `true` |
| `ALLOWED_OPERATIONS` | Verbos SQL permitidos | `SELECT` |
| `BLOCK_DDL` / `BLOCK_STORED_PROCEDURES` / `BLOCK_TRANSACTIONS` | Toggles de guardas | `true` |
| `MSSQL_*`, `TrustServerCertificate`, `Trusted_Connection` | Conectividad DB | _(requerido)_ |

## Despliegue

- Servicio: `mcp-server-streamable-copilot` en `docker-compose.yml`.
- Build con `Dockerfile.copilot_mcp`; expone puerto `8013`; health check en `/health`.
- Unido a `mcp-network`; comparte env MSSQL con otros servicios.

### Ejecución local (compose)

```bash
docker compose build mcp-server-streamable-copilot
docker compose up -d mcp-server-streamable-copilot
docker compose logs -f mcp-server-streamable-copilot
```

Para pruebas locales usa `http://localhost:8013` con los mismos paths y headers.

### Routing en Nginx (resumen)

- `/copilot/mcp` → `mcp-server-streamable-copilot:8013` (POST/OPTIONS/DELETE; Accept reenviado, buffering off)
- Endpoints OAuth proxied con `X-Environment-Path: /copilot`
- CORS permite `Authorization, Content-Type, Accept, Mcp-Session-Id`

## Configuración en Copilot Studio (OAuth manual)

1. Server URL: `https://data.forensic-bot.com/copilot/mcp`
2. Auth: OAuth 2.0 → Manual
3. Completar:
   - Authorization URL: `https://data.forensic-bot.com/copilot/authorize`
   - Token URL: `https://data.forensic-bot.com/copilot/token`
   - Refresh URL: `https://data.forensic-bot.com/copilot/token`
   - Scopes: vacío o `mcp:read`
   - Client ID / secret: desde `/copilot/register` o pre-provisionados
4. Completar el consent en la URL de redirect (el host debe estar permitido).
5. Probar la conexión: Copilot debe listar tools al llamar `initialize`/`tools/list`.

### Dynamic Client Registration (opcional)

```bash
curl -X POST https://data.forensic-bot.com/copilot/register \
  -H "Content-Type: application/json" \
  -d '{"client_name":"copilot-mcp","redirect_uris":["https://global.consent.azure-apim.net/redirect/new-xxxx"]}'
```

## Smoke tests (curl)

```bash
# Health
curl https://data.forensic-bot.com/copilot/health

# Token client credentials (solo pruebas)
TOKEN=$(curl -s -X POST https://data.forensic-bot.com/copilot/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type":"client_credentials","client_id":"test","client_secret":"test"}' | jq -r .access_token)

# Initialize
curl -X POST https://data.forensic-bot.com/copilot/mcp \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"id":1,"jsonrpc":"2.0","method":"initialize"}'

# List tools
curl -X POST https://data.forensic-bot.com/copilot/mcp \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"id":2,"jsonrpc":"2.0","method":"tools/list"}'
```

## Problemas comunes

- `401` en `/mcp`: token ausente o expirado; consigue uno en `/copilot/token`.
- `405` en `/mcp`: GET está bloqueado; usa POST.
- OAuth 400 untrusted redirect: añade el host a `ALLOWED_REDIRECT_HOSTS` y reinicia.
- Copilot “server URL missing”: revisa que la URL sea `https://data.forensic-bot.com/copilot/mcp` y evita conexiones duplicadas obsoletas en Copilot Studio.
