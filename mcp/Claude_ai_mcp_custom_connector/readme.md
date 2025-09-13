# MSSQL MCP Server - Technical Documentation

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Technical Stack](#technical-stack)
- [System Components](#system-components)
- [Authentication Flow](#authentication-flow)
- [API Endpoints](#api-endpoints)
- [Database Tools](#database-tools)
- [Deployment](#deployment)
- [Security](#security)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)

## Overview

The MSSQL MCP Server is a production-grade Model Context Protocol (MCP) implementation that provides secure, OAuth 2.0-authenticated access to Microsoft SQL Server databases through Claude.ai and other MCP-compatible clients. The server implements the MCP specification version 2025-06-18, enabling natural language database interactions through AI assistants.

### Key Features
- Full MCP protocol implementation with SSE transport
- OAuth 2.0 authentication with dynamic client registration
- Comprehensive SQL Server operations (SELECT, INSERT, UPDATE, DELETE)
- TLS/SSL encryption with Let's Encrypt certificates
- Container-based deployment with Docker
- Nginx reverse proxy with optimized SSE handling
- Production-ready health monitoring

## Architecture

### System Architecture Diagram
```
┌─────────────┐         HTTPS/TLS            ┌──────────────┐
│  Claude.ai  │ ◄──────────────────────────► │    Nginx     │
│   Client    │         Port 443             │ Reverse Proxy│
└─────────────┘                              └──────┬───────┘
                                                    │
                                             ┌──────▼───────┐
                                             │  MCP Server  │
                                             │   (Python)   │
                                             │   Port 8008  │
                                             └──────┬───────┘
                                                    │
                                             ┌──────▼───────┐
                                             │ MSSQL Server │
                                             │   Database   │
                                             └──────────────┘
```

### Component Interaction Flow
1. Claude.ai initiates HTTPS connection to the server
2. Nginx handles SSL termination and proxies to MCP server
3. MCP server authenticates requests via OAuth 2.0
4. Authorized requests execute database operations
5. Results stream back through SSE connection

![Process Architecture](docs/mcp-architecture-diagram.svg)

### Multi-tenant Implementation

[How to add a new Mcp-Server](docs/multi-tenant-implementation-guide.md)
## Technical Stack

### Core Technologies
- **Language**: Python 3.11
- **Framework**: Starlette ASGI
- **Database**: Microsoft SQL Server 2019+
- **Driver**: ODBC Driver 18 for SQL Server
- **Protocol**: Model Context Protocol (MCP) 2025-06-18
- **Transport**: Server-Sent Events (SSE)
- **Authentication**: OAuth 2.0 with RFC 9728 discovery

### Infrastructure
- **Container**: Docker with multi-stage builds
- **Proxy**: Nginx 1.24+ with SSE optimization
- **SSL**: Let's Encrypt with Certbot auto-renewal
- **Platform**: Google Cloud Platform (GCP)

## System Components

### 1. MCP Server (`server_oauth.py`)

The core application server implementing:

#### Protocol Handlers
```python
# MCP Method Implementations
- initialize: Server capability negotiation
- tools/list: Available tool discovery
- tools/call: Tool execution
- notifications/initialized: Session establishment
```

#### Database Connection Management
```python
def get_db_config() -> tuple[dict, str]:
    """
    Constructs ODBC connection string from environment variables.
    Returns configuration dict and connection string.
    """
```

#### Data Serialization
```python
def serialize_row_data(data) -> Any:
    """
    Converts pyodbc Row objects and SQL Server types to JSON-compatible format.
    Handles: Decimal, DateTime, Date, Row objects
    """
```

### 2. Database Tools

#### Available Tools

| Tool | Purpose | Parameters |
|------|---------|------------|
| `list_tables` | Enumerate all database tables | None |
| `describe_table` | Get table schema and metadata | `table_name: str` |
| `execute_sql` | Execute arbitrary SQL queries | `query: str` |
| `get_table_sample` | Retrieve sample data from table | `table_name: str`, `limit: int` |

#### Tool Implementation Example
```python
def execute_sql_impl(query: str) -> str:
    """
    Executes SQL query with proper transaction handling.
    Returns JSON-formatted results for SELECT queries,
    or affected row count for DML operations.
    """
```

### 3. OAuth 2.0 Implementation

#### Discovery Endpoints (RFC 9728)
- `/.well-known/oauth-authorization-server`: AS metadata
- `/.well-known/oauth-protected-resource`: RS metadata

#### OAuth Flow
1. **Dynamic Registration**: `/register` - Client registration
2. **Authorization**: `/authorize` - Authorization code grant
3. **Token Exchange**: `/token` - Access token issuance
4. **Token Validation**: In-memory token store with expiration

### 4. Nginx Configuration

#### SSE Optimization
```nginx
location /sse {
    proxy_pass http://mcp-server:8008;
    
    # Critical SSE configurations
    proxy_http_version 1.1;
    proxy_set_header Connection '';
    proxy_buffering off;
    chunked_transfer_encoding off;
    proxy_read_timeout 24h;
    
    # Response headers
    add_header Content-Type text/event-stream;
    add_header Cache-Control no-cache;
    add_header X-Accel-Buffering no;
}
```

## Authentication Flow

### OAuth 2.0 Sequence
```
Client                  Server                  Resource
  │                       │                         │
  ├──► POST /register     │                         │
  │◄── client_id/secret   │                         │
  │                       │                         │
  ├──► GET /authorize     │                         │
  │◄── authorization_code │                         │
  │                       │                         │
  ├──► POST /token        │                         │
  │◄── access_token       │                         │
  │                       │                         │
  ├──► GET /sse + Bearer  │                         │
  │                       ├──► Validate Token       │
  │◄── SSE Stream         │◄── Database Results     │
```

## API Endpoints

### Public Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check and status |
| `/.well-known/oauth-authorization-server` | GET | OAuth AS discovery |
| `/.well-known/oauth-protected-resource` | GET | OAuth RS discovery |

### OAuth Endpoints

| Endpoint | Method | Purpose | Request Body |
|----------|--------|---------|--------------|
| `/register` | POST | Dynamic client registration | `{client_name, redirect_uris}` |
| `/authorize` | GET | Authorization code grant | Query: `client_id, redirect_uri, state` |
| `/token` | POST | Token exchange | `{grant_type, code, client_id, client_secret}` |

### MCP Endpoints

| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|----------------|
| `/sse` | HEAD | SSE capability check | Optional |
| `/sse` | POST | MCP message handling | Bearer token |

## Database Tools

### Tool Specifications

#### list_tables
```json
{
  "name": "list_tables",
  "description": "List all tables in the database",
  "inputSchema": {
    "type": "object",
    "properties": {},
    "required": []
  }
}
```

#### describe_table
```json
{
  "name": "describe_table",
  "description": "Get table structure and metadata",
  "inputSchema": {
    "type": "object",
    "properties": {
      "table_name": {
        "type": "string",
        "description": "Name of the table"
      }
    },
    "required": ["table_name"]
  }
}
```

#### execute_sql
```json
{
  "name": "execute_sql",
  "description": "Execute SQL query",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "SQL query to execute"
      }
    },
    "required": ["query"]
  }
}
```

### SQL Server Compatibility
[Read final Read/Only Implementation](docs/read_only.md)

#### Supported Operations
- Data Query: SELECT with TOP, JOINs, CTEs
- Data Manipulation: INSERT, UPDATE, DELETE
- Schema Discovery: INFORMATION_SCHEMA queries
- Transactions: Automatic commit/rollback

#### Data Type Mapping
| SQL Server Type | Python Type | JSON Serialization |
|----------------|-------------|-------------------|
| INT, BIGINT | int | number |
| DECIMAL, NUMERIC | Decimal | number (float) |
| VARCHAR, NVARCHAR | str | string |
| DATETIME, DATE | datetime | ISO 8601 string |
| BIT | bool | boolean |

## Deployment

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- Domain with DNS A record
- GCP VM with firewall rules configured

### Environment Configuration

Create `.env` file:
```bash
# Database Configuration
MSSQL_HOST=your-sql-server.database.windows.net
MSSQL_USER=your_username
MSSQL_PASSWORD=your_secure_password
MSSQL_DATABASE=your_database
MSSQL_DRIVER=ODBC Driver 18 for SQL Server

# Security
TrustServerCertificate=yes
Trusted_Connection=no
```

### Docker Deployment

#### Build and Run
```bash
# Build containers
docker compose build

# Start services
docker compose up -d

# View logs
docker compose logs -f mcp-server
```

#### Container Configuration
```yaml
services:
  mcp-server:
    build: .
    expose:
      - "8008"
    environment:
      - MSSQL_HOST=${MSSQL_HOST}
      - MSSQL_USER=${MSSQL_USER}
      - MSSQL_PASSWORD=${MSSQL_PASSWORD}
      - MSSQL_DATABASE=${MSSQL_DATABASE}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8008/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### SSL Certificate Setup

#### Initial Setup
```bash
# Run setup script
./setup-letsencrypt.sh

# Verify certificate
openssl s_client -connect data.forensic-bot.com:443 -servername data.forensic-bot.com
```

#### Automatic Renewal
Certbot container runs renewal checks every 12 hours:
```yaml
certbot:
  image: certbot/certbot
  entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
```

## Security

### Network Security

#### GCP Firewall Rules
```bash
# HTTPS traffic
gcloud compute firewall-rules create allow-mcp-https \
    --allow tcp:443 \
    --source-ranges 0.0.0.0/0 \
    --target-tags mcp-server

# HTTP for Let's Encrypt
gcloud compute firewall-rules create allow-letsencrypt \
    --allow tcp:80 \
    --source-ranges 0.0.0.0/0 \
    --target-tags mcp-server
```

### Application Security

#### OAuth 2.0 Protection
- Dynamic client registration
- Short-lived access tokens (1 hour)
- Secure token generation using `secrets.token_urlsafe()`

#### Database Security
- Parameterized queries (via pyodbc)
- Read-only user recommended for production
- Connection string credentials from environment variables
- TLS encryption for database connections

#### TLS Configuration
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
```

### Security Headers
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options DENY;
```

## Monitoring and Maintenance

### Health Monitoring

#### Health Check Endpoint
```bash
curl https://data.forensic-bot.com/health
```

Response:
```json
{
  "status": "healthy",
  "transport": "sse",
  "oauth": "enabled",
  "database": "your_database"
}
```

### Logging

#### Application Logs
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

#### Container Logs
```bash
# View all logs
docker compose logs

# Follow specific service
docker compose logs -f mcp-server

# Last 100 lines
docker compose logs --tail=100 mcp-server
```

### Performance Monitoring

#### Key Metrics
- Response time per tool execution
- Active SSE connections
- OAuth token generation rate
- Database query performance

#### Monitoring Commands
```bash
# Container resource usage
docker stats mcp-server

# Nginx connections
docker exec nginx-container nginx -T | grep worker_connections

# Database connections
docker exec mcp-server python -c "import pyodbc; print(pyodbc.drivers())"
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Failures
```bash
# Test ODBC installation
docker exec mcp-server odbcinst -j

# Verify environment variables
docker exec mcp-server env | grep MSSQL

# Test connection
docker exec mcp-server python -c "
import pyodbc
from os import getenv
conn_str = f\"Driver={{ODBC Driver 18 for SQL Server}};Server={getenv('MSSQL_HOST')};...\"
conn = pyodbc.connect(conn_str)
print('Connected successfully')
"
```

#### 2. SSE Connection Issues
```bash
# Test SSE endpoint
curl -N -H "Accept: text/event-stream" https://data.forensic-bot.com/sse

# Check Nginx buffering
docker exec nginx-container cat /etc/nginx/conf.d/default.conf | grep proxy_buffering
```

#### 3. OAuth Authentication Failures
```bash
# Test OAuth discovery
curl https://data.forensic-bot.com/.well-known/oauth-authorization-server

# Register test client
curl -X POST https://data.forensic-bot.com/register \
  -H "Content-Type: application/json" \
  -d '{"client_name": "test"}'
```

#### 4. Certificate Renewal Issues
```bash
# Test renewal (dry run)
docker compose exec certbot certbot renew --dry-run

# Force renewal
docker compose exec certbot certbot renew --force-renewal

# Check certificate expiration
echo | openssl s_client -servername data.forensic-bot.com -connect data.forensic-bot.com:443 2>/dev/null | openssl x509 -noout -dates
```

### Debug Mode

Enable detailed logging:
```python
# In server_oauth.py
logging.basicConfig(level=logging.DEBUG)

# Add request/response logging
logger.debug(f"Request: {method} - Body: {json.dumps(body)}")
logger.debug(f"Response: {json.dumps(response)}")
```

### Performance Optimization

#### Database Optimization
```sql
-- Add indexes for frequently queried columns
CREATE INDEX idx_table_column ON table_name(column_name);

-- Update statistics
UPDATE STATISTICS table_name;
```

#### Nginx Optimization
```nginx
# Increase worker connections
worker_connections 4096;

# Enable HTTP/2
listen 443 ssl http2;

# Optimize SSL session cache
ssl_session_cache shared:SSL:50m;
ssl_session_timeout 1d;
```

## Appendix

### MCP Protocol Reference
- Specification: https://modelcontextprotocol.io/specification
- Version: 2025-06-18
- Transport: Server-Sent Events (SSE)

### SQL Server Function Reference
| SQL Server | Description |
|------------|-------------|
| TOP n | Limit results |
| GETDATE() | Current timestamp |
| LEN() | String length |
| CHARINDEX() | Find substring |
| ISNULL() | Null handling |

### Environment Variables Reference
| Variable | Description | Example |
|----------|-------------|---------|
| MSSQL_HOST | Database server | server.database.windows.net |
| MSSQL_USER | Database username | sa |
| MSSQL_PASSWORD | Database password | SecurePass123! |
| MSSQL_DATABASE | Database name | production |
| MSSQL_DRIVER | ODBC driver | ODBC Driver 18 for SQL Server |
| TrustServerCertificate | SSL certificate trust | yes |

### Port Reference
| Port | Service | Purpose |
|------|---------|---------|
| 80 | HTTP | Let's Encrypt validation |
| 443 | HTTPS | Production traffic |
| 8008 | MCP Server | Internal API |

---

Version: 2.0.0  
Last Updated: August 2025  
Protocol: MCP 2025-06-18  
Compatibility: SQL Server 2019+, Python 3.11+, Docker 20.10+