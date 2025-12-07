# MSSQL OpenAPI Server with Bearer Token Authentication

A production-ready OpenAPI 3.1 compliant REST server that provides secure, read-only access to Microsoft SQL Server databases. This server implements Bearer Token authentication, SSL/TLS encryption, and seamless integration with ChatGPT Actions and other OpenAPI-compatible AI tools.

## 🚀 Features

### **OpenAPI 3.1 Compliance**
- **RESTful API**: Standard HTTP endpoints with OpenAPI specification
- **Bearer Token Authentication**: Simple and secure token-based authentication
- **JSON Responses**: All responses in standard JSON format
- **Swagger Documentation**: Auto-generated OpenAPI spec available at `/docs`

### **Database Operations**
- **Table Listing**: List all tables in the database with metadata
- **Schema Description**: Get detailed table structure and column information
- **SQL Execution**: Execute read-only SELECT queries safely
- **Data Sampling**: Retrieve sample data from tables with configurable limits
- **Read-Only Mode**: Enforced read-only operations for production safety

### **Security Features**
- **Bearer Token Authentication**: Configurable token-based security
- **SQL Injection Protection**: Parameterized queries and input validation
- **Query Validation**: Strict filtering of non-SELECT statements
- **SSL/TLS Encryption**: Let's Encrypt certificates with automatic renewal
- **CORS Support**: Configurable cross-origin resource sharing

### **Production Features**
- **Docker Containerization**: Multi-stage Docker builds with optimized images
- **Nginx Reverse Proxy**: Production-grade proxying with SSL termination
- **Health Monitoring**: Built-in health check endpoints
- **Auto Scaling**: Horizontal scaling support with Docker Compose
- **Logging**: Comprehensive request and error logging

## 📋 Architecture

```
┌─────────────┐         ┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│   ChatGPT   │◄─HTTPS─►│    Nginx    │◄─HTTP──►│ OpenAPI API  │◄─ODBC──►│  SQL Server  │
│  /AI Tools  │   443   │  (SSL/TLS)  │   8009  │   Server     │         │   Database   │
└─────────────┘         └─────────────┘         └──────────────┘         └──────────────┘
                             │
                             │
                        ┌────▼────┐
                        │ Certbot │
                        │  Auto   │
                        │ Renewal │
                        └─────────┘
```

### Components

1. **OpenAPI Server** (`server_openapi.py`)
   - Python 3.11 with FastAPI framework
   - OpenAPI 3.1 specification compliance
   - Bearer token authentication
   - Database connectivity via pyodbc

2. **Nginx Reverse Proxy**
   - SSL/TLS termination
   - Request routing and load balancing
   - Security headers
   - CORS configuration

3. **Certbot**
   - Automatic certificate issuance
   - Renewal checks every 12 hours
   - ACME protocol (Let's Encrypt)

## 🛠️ Installation & Setup

### Prerequisites

- **Infrastructure**:
  - Docker Engine 20.10+
  - Docker Compose 2.0+
  - Public domain with DNS A record
  - VM with ports 80, 443, 8009 accessible

- **Database**:
  - Microsoft SQL Server 2019+
  - ODBC Driver 18 for SQL Server
  - Database user with appropriate permissions

### 1. Environment Configuration

Create a `.env` file in the project root:

```bash
# Database Configuration
MSSQL_HOST=your-sql-server.database.windows.net
MSSQL_USER=your_username
MSSQL_PASSWORD=your_secure_password
MSSQL_DATABASE=your_database
MSSQL_DRIVER=ODBC Driver 18 for SQL Server

# Security Settings
TrustServerCertificate=yes
Trusted_Connection=no
READ_ONLY_MODE=true

# OpenAPI Configuration
OPENAPI_BEARER_TOKEN=your_secure_bearer_token_here
OPENAPI_SERVER_URL=https://data.forensic-bot.com/actions
OPENAPI_PORT=8009
```

### 2. SSL Certificate Setup

Run the automated Let's Encrypt setup:

```bash
# Make script executable
chmod +x setup-letsencrypt.sh

# Run setup
./setup-letsencrypt.sh

# Follow prompts:
# - Enter domain: data.forensic-bot.com
# - Enter email: your-email@example.com
# - Choose production (0) or staging (1)
```

The script will:
1. Check prerequisites (Docker, Docker Compose)
2. Create required directories
3. Download TLS parameters
4. Configure Nginx
5. Request Let's Encrypt certificate
6. Set up automatic renewal

### 3. Docker Deployment

#### Production Deployment

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service health
curl https://your-domain.com/actions/health
```

#### Development Deployment

```bash
# Start with hot-reload
docker-compose up --build

# Access locally
curl http://localhost:8009/health
```

### 4. Verify Installation

```bash
# Test HTTPS connection
curl https://your-domain.com/actions/health

# Test OpenAPI schema
curl https://your-domain.com/actions/openapi.json

# Test with authentication
curl -H "Authorization: Bearer your_token" \
     https://your-domain.com/actions/list_tables
```

## 🔧 Integration Guides

### ChatGPT Actions Integration

1. **Create Custom Action** in ChatGPT:
   - Go to ChatGPT → Configure → Create Action
   - Name: `MSSQL Database Access`
   - Description: `Query SQL Server database with read-only access`

2. **Import OpenAPI Schema**:
   ```
   Schema URL: https://your-domain.com/actions/openapi.json
   ```

3. **Configure Authentication**:
   - Type: `Bearer Token`
   - Token: `your_secure_bearer_token_here`

4. **Test Connection**:
   - Use the test feature in ChatGPT Actions
   - Try the `/list_tables` endpoint

5. **Example Usage in ChatGPT**:
   ```
   User: "Show me all tables in the database"
   ChatGPT will call: GET /actions/list_tables
   
   User: "Describe the structure of the Users table"
   ChatGPT will call: GET /actions/describe_table?table_name=Users
   
   User: "Get sample data from the Orders table"
   ChatGPT will call: GET /actions/get_table_sample?table_name=Orders&limit=10
   ```

### Other OpenAPI-Compatible Tools

The server works with any tool that supports OpenAPI 3.1 specifications:

- **Postman**: Import the OpenAPI spec
- **Insomnia**: Load the schema file
- **Swagger UI**: Available at `https://your-domain.com/actions/docs`
- **Custom Applications**: Use the OpenAPI spec to generate client SDKs

## 📚 API Reference

### Base URL
```
https://your-domain.com/actions
```

### Authentication
All endpoints require Bearer token authentication:
```
Authorization: Bearer your_secure_bearer_token_here
```

### Endpoints

#### 1. Health Check
```http
GET /health
```
**Description**: Check server health and status
**Authentication**: None required
**Response**:
```json
{
  "status": "ok",
  "mode": "read-only",
  "database": "your_database"
}
```

#### 2. List Tables
```http
GET /list_tables
```
**Description**: List all tables in the database
**Authentication**: Required
**Response**:
```json
{
  "total_tables": 15,
  "tables": [
    {
      "schema": "dbo",
      "table_name": "Users",
      "full_name": "Users",
      "type": "BASE TABLE"
    }
  ]
}
```

#### 3. Describe Table
```http
GET /describe_table?table_name={table_name}
```
**Description**: Get detailed table structure and metadata
**Authentication**: Required
**Parameters**:
- `table_name` (required): Name of the table to describe

**Response**:
```json
{
  "table_name": "[dbo].[Users]",
  "row_count": 1500,
  "total_columns": 8,
  "columns": [
    {
      "column_name": "id",
      "data_type": "int",
      "nullable": false,
      "max_length": null,
      "precision": 10,
      "scale": 0,
      "default_value": null
    }
  ]
}
```

#### 4. Execute SQL
```http
POST /execute_sql
```
**Description**: Execute a read-only SELECT query
**Authentication**: Required
**Request Body**:
```json
{
  "query": "SELECT TOP 10 * FROM Users WHERE active = 1"
}
```
**Response**:
```json
{
  "columns": ["id", "name", "email", "active"],
  "rows": [
    [1, "John Doe", "john@example.com", true],
    [2, "Jane Smith", "jane@example.com", true]
  ],
  "row_count": 2
}
```

#### 5. Get Table Sample
```http
GET /get_table_sample?table_name={table_name}&limit={limit}
```
**Description**: Get sample data from a table
**Authentication**: Required
**Parameters**:
- `table_name` (required): Name of the table
- `limit` (optional): Number of rows to return (default: 5, max: 1000)

**Response**:
```json
{
  "table_name": "[dbo].[Users]",
  "limit": 5,
  "columns": ["id", "name", "email", "active"],
  "rows": [
    [1, "John Doe", "john@example.com", true],
    [2, "Jane Smith", "jane@example.com", true]
  ]
}
```

### OpenAPI Specification

The complete OpenAPI 3.1 specification is available at:
```
https://your-domain.com/actions/openapi.json
```

Interactive documentation (Swagger UI) is available at:
```
https://your-domain.com/actions/docs
```

## 🔒 Security

### Authentication

The server uses Bearer Token authentication for all protected endpoints:

```http
Authorization: Bearer your_secure_bearer_token_here
```

### SQL Query Validation

The server implements strict validation to ensure read-only operations:

1. **Allowed Operations**:
   - `SELECT` statements
   - `WITH` common table expressions (CTEs)
   - Queries against `INFORMATION_SCHEMA` views

2. **Blocked Operations**:
   - `INSERT`, `UPDATE`, `DELETE`, `MERGE`
   - `CREATE`, `ALTER`, `DROP`, `TRUNCATE`
   - `EXEC`, `EXECUTE` (stored procedures)
   - `GRANT`, `REVOKE` (permissions)
   - `BEGIN TRANSACTION`, `COMMIT`, `ROLLBACK`
   - Multiple statements (semicolon-separated)

3. **Input Sanitization**:
   - Table names validated against safe patterns
   - Parameterized queries for all database operations
   - SQL injection protection via pyodbc

### Network Security

#### Nginx Configuration
The server is protected by Nginx with the following security features:

```nginx
# Security headers
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options DENY;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# CORS configuration
add_header Access-Control-Allow-Origin * always;
add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS' always;
add_header Access-Control-Allow-Headers 'Authorization, Content-Type, Accept' always;
```

#### Database Security
- **TLS 1.2+**: Encrypted connections to SQL Server
- **Read-Only Mode**: Enforced at application level
- **Least Privilege**: Database user with minimal required permissions
- **Connection Pooling**: Efficient resource management

## 📊 Monitoring & Maintenance

### Health Checks

```bash
# Server health
curl https://your-domain.com/actions/health

# Expected response:
{
  "status": "ok",
  "mode": "read-only",
  "database": "your_database"
}
```

### Docker Container Management

```bash
# View all services
docker-compose ps

# View logs
docker-compose logs -f mcp-server-openapi

# Restart OpenAPI server
docker-compose restart mcp-server-openapi

# Scale services
docker-compose up -d --scale mcp-server-openapi=3
```

### Certificate Management

```bash
# Check certificate expiration
echo | openssl s_client -servername your-domain.com -connect your-domain.com:443 2>/dev/null | openssl x509 -noout -dates

# Test renewal (dry run)
docker-compose exec certbot certbot renew --dry-run

# Force renewal
docker-compose exec certbot certbot renew --force-renewal
```

### Performance Monitoring

```bash
# Container resource usage
docker stats mcp-server-openapi

# Database connection test
docker exec mcp-server-openapi python -c "
from server_openapi import _get_db_config
config, conn_str = _get_db_config()
print(f'Connected to: {config[\"database\"]}')"

# API response time test
time curl -H "Authorization: Bearer your_token" \
     https://your-domain.com/actions/list_tables
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Authentication Failed (401 Unauthorized)
```bash
# Check if token is correctly set
curl -H "Authorization: Bearer wrong_token" \
     https://your-domain.com/actions/list_tables

# Verify token in environment
docker exec mcp-server-openapi env | grep OPENAPI_BEARER_TOKEN
```

#### 2. Database Connection Failed
```bash
# Test database connectivity
docker exec mcp-server-openapi python -c "
from server_openapi import _get_db_config, _db_cursor
try:
    with _db_cursor() as cursor:
        cursor.execute('SELECT 1')
        print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')
"

# Check environment variables
docker exec mcp-server-openapi env | grep MSSQL
```

#### 3. Certificate Issues
```bash
# Check certificate validity
openssl s_client -connect your-domain.com:443 -servername your-domain.com

# Verify DNS resolution
nslookup your-domain.com

# Check certbot logs
docker-compose logs certbot
```

#### 4. OpenAPI Schema Issues
```bash
# Validate OpenAPI spec
curl https://your-domain.com/actions/openapi.json | jq .

# Check if Swagger UI loads
curl -I https://your-domain.com/actions/docs
```

### Debug Mode

Enable detailed logging by setting environment variables:

```bash
# In .env file
LOG_LEVEL=DEBUG

# Or modify server code temporarily
```

For production debugging:
```bash
# View real-time logs
docker-compose logs -f mcp-server-openapi

# Filter error logs
docker-compose logs mcp-server-openapi | grep ERROR

# Check Nginx access logs
docker-compose logs nginx | grep "POST /actions"
```

## 📖 Documentation

### Project Structure
```
.
├── server_openapi.py            # FastAPI OpenAPI server
├── Dockerfile.openapi           # OpenAPI server Docker image
├── docker-compose.yml           # Production compose with OpenAPI
├── setup-letsencrypt.sh         # SSL setup script
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── nginx/
│   ├── nginx.conf              # Main Nginx config
│   └── conf.d/
│       └── default.conf        # Site configuration with /actions proxy
├── certbot/
│   ├── conf/                   # SSL certificates
│   └── www/                    # ACME challenge
├── logs/
│   └── nginx/                  # Nginx access/error logs
└── README.md                   # This file
```

### Configuration Files

#### Docker Compose Configuration
The `docker-compose.yml` includes the OpenAPI server service:

```yaml
services:
  mcp-server-openapi:
    build:
      context: .
      dockerfile: Dockerfile.openapi
    container_name: mcp-server-openapi
    expose:
      - "8009"
    environment:
      - MSSQL_HOST=${MSSQL_HOST}
      - MSSQL_USER=${MSSQL_USER}
      - MSSQL_PASSWORD=${MSSQL_PASSWORD}
      - MSSQL_DATABASE=${MSSQL_DATABASE}
      - OPENAPI_BEARER_TOKEN=${OPENAPI_BEARER_TOKEN}
      - OPENAPI_SERVER_URL=${OPENAPI_SERVER_URL}
      - READ_ONLY_MODE=${READ_ONLY_MODE:-true}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8009/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - mcp-network
    restart: unless-stopped
```

#### Nginx Configuration
The `/actions` location in Nginx proxies to the OpenAPI server:

```nginx
location /actions/ {
    proxy_pass http://mcp-server-openapi:8009/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_set_header Authorization $http_authorization;

    add_header Access-Control-Allow-Origin * always;
    add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS' always;
    add_header Access-Control-Allow-Headers 'Authorization, Content-Type, Accept' always;
}
```

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MSSQL_HOST` | SQL Server hostname | `localhost` | Yes |
| `MSSQL_USER` | Database username | - | Yes |
| `MSSQL_PASSWORD` | Database password | - | Yes |
| `MSSQL_DATABASE` | Database name | - | Yes |
| `MSSQL_DRIVER` | ODBC driver | `ODBC Driver 18 for SQL Server` | No |
| `TrustServerCertificate` | Trust server cert | `yes` | No |
| `Trusted_Connection` | Use trusted connection | `no` | No |
| `READ_ONLY_MODE` | Enable read-only mode | `true` | No |
| `OPENAPI_BEARER_TOKEN` | Bearer token for auth | - | No |
| `OPENAPI_SERVER_URL` | Server URL for OpenAPI spec | `https://data.forensic-bot.com/actions` | No |
| `OPENAPI_PORT` | Internal port | `8009` | No |

## 🧪 Testing

### API Testing with curl

```bash
# Test health endpoint (no auth required)
curl https://your-domain.com/actions/health

# Test authenticated endpoints
TOKEN="your_bearer_token_here"

# List tables
curl -H "Authorization: Bearer $TOKEN" \
     https://your-domain.com/actions/list_tables

# Describe table
curl -H "Authorization: Bearer $TOKEN" \
     "https://your-domain.com/actions/describe_table?table_name=Users"

# Get table sample
curl -H "Authorization: Bearer $TOKEN" \
     "https://your-domain.com/actions/get_table_sample?table_name=Users&limit=5"

# Execute SQL
curl -X POST \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"query": "SELECT TOP 5 * FROM Users"}' \
     https://your-domain.com/actions/execute_sql
```

### Testing with Postman

1. Import OpenAPI spec: `https://your-domain.com/actions/openapi.json`
2. Set up Bearer Token authentication
3. Test all endpoints

### Load Testing

```bash
# Using Apache Bench
ab -n 1000 -c 10 -H "Authorization: Bearer TOKEN" \
   https://your-domain.com/actions/list_tables

# Using hey
hey -n 1000 -c 10 -H "Authorization: Bearer TOKEN" \
    https://your-domain.com/actions/list_tables
```

## 🔄 Deployment Workflow

### Initial Deployment
```bash
1. Clone repository
2. Configure .env file with database and token settings
3. Run setup-letsencrypt.sh for SSL certificates
4. Start services: docker-compose up -d
5. Verify health: curl https://your-domain.com/actions/health
6. Configure ChatGPT Actions or other clients
```

### Updates
```bash
# Pull latest changes
git pull

# Rebuild OpenAPI container
docker-compose build mcp-server-openapi

# Restart services (zero-downtime)
docker-compose up -d

# Verify
curl https://your-domain.com/actions/health
```

### Rollback
```bash
# Stop services
docker-compose down

# Checkout previous version
git checkout <previous-commit>

# Rebuild and restart
docker-compose up --build -d
```

## 📝 License

MIT License - See LICENSE file for details

## 📧 Support

For issues and questions:
- GitHub Issues: [repository-url]
- Email: support@your-domain.com
- Documentation: https://your-domain.com/actions/docs

---

**Version**: 2.0.0  
**Last Updated**: October 2025  
**OpenAPI Version**: 3.1.0  
**Compatibility**: SQL Server 2019+, Python 3.11+, Docker 20.10+  
**Framework**: FastAPI with uvicorn  
**Authentication**: Bearer Token  
**Encryption**: TLS 1.2+ with Let's Encrypt