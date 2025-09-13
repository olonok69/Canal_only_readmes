# Complete Guide: Adding a New MCP Server to Multi-Tenant Setup

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Implementation](#step-by-step-implementation)
4. [Configuration Files Reference](#configuration-files-reference)
5. [Testing and Verification](#testing-and-verification)
6. [Troubleshooting](#troubleshooting)
7. [Examples](#examples)

## Overview

This guide explains how to add a new MCP server instance (e.g., production, marketing, finance) to your existing multi-tenant Docker Compose setup. Each new server will be accessible via its own path (e.g., `/production/sse`, `/marketing/sse`).

## Prerequisites

- Working demo environment at `/demo/sse`
- Docker and Docker Compose installed
- SSL certificates already configured via Let's Encrypt
- Access to MSSQL database(s)
- `.env` file with database credentials

## Step-by-Step Implementation

### Step 1: Plan Your New Environment

Decide on:
- **Path name**: e.g., `production`, `marketing`, `finance`
- **Database**: Same DB with different schema, or completely separate database
- **Permissions**: Read-only or read-write access
- **User credentials**: Database user for this environment

Example planning for "production" environment:
```
Path: /production/sse
Database: ProductionDB
User: prod_user
Access: Read-Write
Container: mcp-server-production
```

### Step 2: Update Environment Variables

Edit `.env` file to add credentials for the new environment:

```bash
# Existing demo configuration
MSSQL_HOST=your-sql-server.database.windows.net
MSSQL_DATABASE=DemoDB
MSSQL_USER=demo_user
MSSQL_PASSWORD=DemoPassword123!

# ADD: New production environment
MSSQL_DATABASE_PROD=ProductionDB
MSSQL_USER_PROD=prod_user
MSSQL_PASSWORD_PROD=ProdPassword123!
# Optional: Different host for production
# MSSQL_HOST_PROD=prod-sql-server.database.windows.net
```

### Step 3: Add New Service to docker-compose.yml

Add the new service definition in `docker-compose.yml`:

```yaml
  # Production MCP Server
  mcp-server-production:
    build: 
      context: .
      dockerfile: Dockerfile
    container_name: mcp-server-production
    expose:
      - "8008"
    environment:
      # Use MSSQL_HOST_PROD if defined, otherwise use default MSSQL_HOST
      - MSSQL_HOST=${MSSQL_HOST_PROD:-${MSSQL_HOST}}
      - MSSQL_USER=${MSSQL_USER_PROD}
      - MSSQL_PASSWORD=${MSSQL_PASSWORD_PROD}
      - MSSQL_DATABASE=${MSSQL_DATABASE_PROD}
      - MSSQL_DRIVER=ODBC Driver 18 for SQL Server
      - TrustServerCertificate=yes
      - Trusted_Connection=no
      - READ_ONLY_MODE=false  # Production has write access
      - SERVER_NAME=Production Environment
      - ENVIRONMENT_PATH=/production
      # Optional: Production-specific settings
      - BLOCK_DDL=true  # Block DDL operations even in production
      - LOG_LEVEL=INFO
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8008/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - mcp-network
    restart: unless-stopped
```

Also update the nginx service dependencies:

```yaml
  nginx:
    # ... existing configuration ...
    depends_on:
      - mcp-server-demo
      - mcp-server-production  # ADD THIS LINE
    # ... rest of configuration ...
```

### Step 4: Update Nginx Configuration

Edit `nginx/conf.d/default.conf` to add routing for the new environment.

#### 4.1: Update the root endpoint JSON response

Find the root location block and update it:

```nginx
    location = / {
        add_header Content-Type application/json;
        return 200 '{
            "service": "MSSQL MCP Server",
            "status": "running",
            "environments": {
                "demo": "https://data.forensic-bot.com/demo/sse",
                "production": "https://data.forensic-bot.com/production/sse",
                "marketing": "Coming soon",
                "finance": "Coming soon"
            }
        }';
    }
```

#### 4.2: Add complete location blocks for the new environment

Add these location blocks after the demo section (around line 240, before the placeholders):

```nginx
    # =====================================
    # PRODUCTION Environment
    # https://data.forensic-bot.com/production/sse
    # =====================================
    
    # Health check for production
    location = /production/health {
        rewrite ^/production(/.*)$ $1 break;
        proxy_pass http://mcp-server-production:8008;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Environment-Path /production;
    }
    
    # OAuth discovery endpoints for production
    location ~ ^/production/\.well-known/(oauth-authorization-server|oauth-protected-resource)$ {
        rewrite ^/production(/.*)$ $1 break;
        proxy_pass http://mcp-server-production:8008;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Environment-Path /production;
        
        # CORS headers
        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS' always;
        add_header Access-Control-Allow-Headers 'Authorization, Content-Type' always;
    }
    
    # Handle OAuth discovery with /sse suffix (Claude.ai quirk)
    location ~ ^/production/\.well-known/(oauth-authorization-server|oauth-protected-resource)/sse$ {
        rewrite ^/production/\.well-known/(.*)/sse$ /production/.well-known/$1 redirect;
    }
    
    # Registration endpoint for production
    location = /production/register {
        rewrite ^/production(/.*)$ $1 break;
        proxy_pass http://mcp-server-production:8008;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header Content-Type $content_type;
        proxy_set_header X-Environment-Path /production;
        
        # CORS headers
        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS' always;
        add_header Access-Control-Allow-Headers 'Authorization, Content-Type' always;
    }
    
    # Authorization endpoint for production
    location = /production/authorize {
        rewrite ^/production(/.*)$ $1 break;
        proxy_pass http://mcp-server-production:8008;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Environment-Path /production;
        
        # CORS headers
        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS' always;
        add_header Access-Control-Allow-Headers 'Authorization, Content-Type' always;
    }
    
    # Token endpoint for production
    location = /production/token {
        rewrite ^/production(/.*)$ $1 break;
        proxy_pass http://mcp-server-production:8008;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header Content-Type $content_type;
        proxy_set_header X-Environment-Path /production;
        
        # CORS headers
        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS' always;
        add_header Access-Control-Allow-Headers 'Authorization, Content-Type' always;
    }
    
    # SSE endpoint for production
    location = /production/sse {
        if ($request_method = HEAD) {
            add_header Content-Type text/event-stream;
            add_header Cache-Control no-cache;
            add_header X-Accel-Buffering no;
            add_header Access-Control-Allow-Origin * always;
            add_header X-MCP-Environment production always;
            return 200;
        }
        
        # For GET and POST requests
        rewrite ^/production(/.*)$ $1 break;
        proxy_pass http://mcp-server-production:8008;
        
        # Critical for SSE/streaming
        proxy_http_version 1.1;
        
        # Clear connection header for SSE
        proxy_set_header Connection '';
        
        # Disable caching
        proxy_set_header Cache-Control 'no-cache';
        proxy_cache off;
        
        # Disable buffering for SSE - CRITICAL
        proxy_buffering off;
        chunked_transfer_encoding off;
        proxy_request_buffering off;
        
        # Very long timeout for persistent SSE connections
        proxy_read_timeout 24h;
        proxy_send_timeout 24h;
        send_timeout 24h;
        keepalive_timeout 24h;
        
        # SSE-specific headers
        proxy_set_header Accept text/event-stream;
        add_header Content-Type text/event-stream always;
        add_header Cache-Control 'no-cache' always;
        add_header X-Accel-Buffering 'no' always;
        add_header X-MCP-Environment 'production' always;
        
        # Standard headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Environment-Path /production;
        
        # CORS headers for Claude.ai
        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods 'GET, POST, HEAD, OPTIONS' always;
        add_header Access-Control-Allow-Headers 'Authorization, Content-Type, Accept' always;
    }
    
    # Messages endpoint for production
    location = /production/messages {
        rewrite ^/production(/.*)$ $1 break;
        proxy_pass http://mcp-server-production:8008;
        
        proxy_http_version 1.1;
        proxy_set_header Connection '';
        
        # Disable buffering
        proxy_buffering off;
        proxy_cache off;
        
        # Timeouts
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
        
        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header Content-Type $content_type;
        proxy_set_header X-Environment-Path /production;
        
        # CORS headers
        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS' always;
        add_header Access-Control-Allow-Headers 'Authorization, Content-Type' always;
    }
```

### Step 5: Create Database and User (if needed)

If using a separate database, create it in SQL Server:

```sql
-- Create database
CREATE DATABASE ProductionDB;
GO

-- Create login
CREATE LOGIN prod_user WITH PASSWORD = 'ProdPassword123!';
GO

-- Switch to the new database
USE ProductionDB;
GO

-- Create user
CREATE USER prod_user FOR LOGIN prod_user;
GO

-- Grant permissions (adjust as needed)
-- For read-write access:
ALTER ROLE db_datareader ADD MEMBER prod_user;
ALTER ROLE db_datawriter ADD MEMBER prod_user;
GO

-- For read-only access:
-- ALTER ROLE db_datareader ADD MEMBER prod_user;
-- GO
```

### Step 6: Deploy the New Environment

```bash
# 1. Stop current services
sudo docker compose down

# 2. Rebuild and start all services
sudo docker compose up -d --build

# 3. Check all services are running
sudo docker compose ps

# 4. Monitor logs
sudo docker compose logs -f
```

### Step 7: Test the New Environment

```bash
# Test health endpoint
curl https://data.forensic-bot.com/production/health

# Test OAuth discovery
curl https://data.forensic-bot.com/production/.well-known/oauth-authorization-server

# Test root endpoint (should show production as active)
curl https://data.forensic-bot.com/
```

## Configuration Files Reference

### Files to Modify When Adding New Environment

| File | What to Change | Line Numbers (approx.) |
|------|---------------|------------------------|
| `.env` | Add database credentials | End of file |
| `docker-compose.yml` | Add new service definition | After demo service |
| `docker-compose.yml` | Update nginx dependencies | Line ~55 |
| `nginx/conf.d/default.conf` | Update root JSON response | Lines 50-62 |
| `nginx/conf.d/default.conf` | Add location blocks | After demo section |

### Template for Common Environment Types

#### Marketing Department (Read-Only)
```yaml
  mcp-server-marketing:
    build: 
      context: .
      dockerfile: Dockerfile
    container_name: mcp-server-marketing
    expose:
      - "8008"
    environment:
      - MSSQL_HOST=${MSSQL_HOST}
      - MSSQL_USER=${MSSQL_USER_MARKETING}
      - MSSQL_PASSWORD=${MSSQL_PASSWORD_MARKETING}
      - MSSQL_DATABASE=${MSSQL_DATABASE_MARKETING}
      - READ_ONLY_MODE=true  # Marketing gets read-only
      - SERVER_NAME=Marketing Department
      - ENVIRONMENT_PATH=/marketing
    networks:
      - mcp-network
    restart: unless-stopped
```

#### Finance Department (Extra Secure)
```yaml
  mcp-server-finance:
    build: 
      context: .
      dockerfile: Dockerfile
    container_name: mcp-server-finance
    expose:
      - "8008"
    environment:
      - MSSQL_HOST=${MSSQL_HOST_FINANCE}  # Separate server
      - MSSQL_USER=${MSSQL_USER_FINANCE}
      - MSSQL_PASSWORD=${MSSQL_PASSWORD_FINANCE}
      - MSSQL_DATABASE=${MSSQL_DATABASE_FINANCE}
      - READ_ONLY_MODE=true
      - BLOCK_DDL=true
      - BLOCK_STORED_PROCEDURES=true
      - BLOCK_TRANSACTIONS=true
      - SERVER_NAME=Finance Department
      - ENVIRONMENT_PATH=/finance
    networks:
      - mcp-network
    restart: unless-stopped
```

## Testing and Verification

### Comprehensive Test Script

Create `test_new_environment.py`:

```python
#!/usr/bin/env python3
"""Test script for new MCP environment"""

import sys
import requests
import json

def test_environment(base_url, env_path):
    """Test all endpoints for an environment"""
    
    print(f"\nTesting Environment: {env_path}")
    print("=" * 50)
    
    tests = [
        (f"{env_path}/health", "Health Check"),
        (f"{env_path}/.well-known/oauth-authorization-server", "OAuth AS Discovery"),
        (f"{env_path}/.well-known/oauth-protected-resource", "OAuth RS Discovery"),
    ]
    
    all_passed = True
    
    for endpoint, description in tests:
        url = f"{base_url}{endpoint}"
        print(f"\n{description}:")
        print(f"  URL: {url}")
        
        try:
            response = requests.get(url, timeout=5, verify=True)
            if response.status_code == 200:
                print(f"  ✓ Status: {response.status_code}")
                # Show first 100 chars of response
                content = json.dumps(response.json(), indent=2)[:100] + "..."
                print(f"  Response: {content}")
            else:
                print(f"  ✗ Status: {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"  ✗ Error: {e}")
            all_passed = False
    
    # Test SSE endpoint with HEAD
    sse_url = f"{base_url}{env_path}/sse"
    print(f"\nSSE Endpoint (HEAD):")
    print(f"  URL: {sse_url}")
    try:
        response = requests.head(sse_url, timeout=5, verify=True)
        if response.status_code == 200:
            print(f"  ✓ Status: {response.status_code}")
            print(f"  ✓ Content-Type: {response.headers.get('Content-Type')}")
        else:
            print(f"  ✗ Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        all_passed = False
    
    return all_passed

def main():
    base_url = "https://data.forensic-bot.com"
    
    # Test specific environment passed as argument
    if len(sys.argv) > 1:
        env_path = f"/{sys.argv[1]}"
        result = test_environment(base_url, env_path)
        sys.exit(0 if result else 1)
    
    # Test all environments
    environments = ["/demo", "/production"]  # Add more as needed
    
    print("Testing All MCP Environments")
    print("=" * 50)
    
    # Test root endpoint
    print("\nRoot Endpoint:")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print(f"✓ Available environments: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"✗ Failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test each environment
    results = {}
    for env in environments:
        results[env] = test_environment(base_url, env)
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY:")
    for env, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {env}: {status}")

if __name__ == "__main__":
    main()
```

Run the test:
```bash
# Test all environments
python3 test_new_environment.py

# Test specific environment
python3 test_new_environment.py production
```

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Nginx won't start - "host not found"
**Error**: `nginx: [emerg] host not found in upstream "mcp-server-production:8008"`

**Solution**: Make sure the container name in docker-compose.yml matches exactly what's in nginx config:
```bash
# Check container is defined
grep "mcp-server-production:" docker-compose.yml

# Check nginx references
grep "mcp-server-production" nginx/conf.d/default.conf
```

#### Issue 2: Database connection fails
**Error**: `Failed to connect to database`

**Solution**: Verify credentials and create database/user:
```bash
# Check environment variables are set
docker compose exec mcp-server-production env | grep MSSQL

# Test connection from container
docker compose exec mcp-server-production python -c "
import os
import pyodbc
conn_str = f\"Driver={{ODBC Driver 18 for SQL Server}};Server={os.getenv('MSSQL_HOST')};Database={os.getenv('MSSQL_DATABASE')};UID={os.getenv('MSSQL_USER')};PWD={os.getenv('MSSQL_PASSWORD')};TrustServerCertificate=yes\"
conn = pyodbc.connect(conn_str)
print('Connected successfully!')
"
```

#### Issue 3: OAuth endpoints return 404
**Error**: 404 on `/production/.well-known/oauth-authorization-server`

**Solution**: Check nginx location blocks and rewrite rules:
```nginx
# Ensure this exists and path matches
location ~ ^/production/\.well-known/(oauth-authorization-server|oauth-protected-resource)$ {
    rewrite ^/production(/.*)$ $1 break;  # This removes /production prefix
    proxy_pass http://mcp-server-production:8008;
    # ...
}
```

#### Issue 4: SSE connection fails
**Error**: SSE endpoint doesn't stream

**Solution**: Verify all SSE-critical settings are present:
```nginx
proxy_buffering off;
chunked_transfer_encoding off;
proxy_request_buffering off;
add_header X-Accel-Buffering 'no' always;
```

### Debugging Commands

```bash
# View logs for specific container
sudo docker compose logs mcp-server-production

# Check nginx configuration is valid
sudo docker compose exec nginx nginx -t

# Test internal connectivity
sudo docker compose exec nginx curl http://mcp-server-production:8008/health

# Monitor all logs
sudo docker compose logs -f

# Check running containers
sudo docker compose ps

# Restart specific service
sudo docker compose restart mcp-server-production
```

## Examples

### Example 1: Adding Marketing Department (Read-Only)

1. **Update .env**:
```bash
MSSQL_DATABASE_MARKETING=MarketingDB
MSSQL_USER_MARKETING=marketing_readonly
MSSQL_PASSWORD_MARKETING=Marketing123!
```

2. **Add to docker-compose.yml**:
```yaml
  mcp-server-marketing:
    # ... (use template from above)
```

3. **Add to nginx/conf.d/default.conf**:
   - Copy all production location blocks
   - Replace "production" with "marketing"

4. **Deploy and test**:
```bash
sudo docker compose up -d
curl https://data.forensic-bot.com/marketing/health
```

### Example 2: Adding Development Environment

1. **Update .env**:
```bash
MSSQL_HOST_DEV=dev-server.database.windows.net
MSSQL_DATABASE_DEV=DevDB
MSSQL_USER_DEV=dev_user
MSSQL_PASSWORD_DEV=Dev123!
```

2. **Add to docker-compose.yml** with relaxed settings:
```yaml
  mcp-server-dev:
    # ... configuration
    environment:
      - READ_ONLY_MODE=false
      - BLOCK_DDL=false  # Allow DDL in dev
      - LOG_LEVEL=DEBUG  # More logging
```

3. **Configure nginx** with dev-specific headers if needed

4. **Deploy and test**

## Checklist for Adding New Environment

- [ ] Choose environment name (e.g., "production")
- [ ] Add database credentials to `.env`
- [ ] Add service to `docker-compose.yml`
- [ ] Update nginx dependencies in `docker-compose.yml`
- [ ] Update root endpoint JSON in nginx config
- [ ] Add all location blocks to nginx config (8 blocks total)
- [ ] Create database and user in SQL Server
- [ ] Test with `docker compose up -d`
- [ ] Verify health endpoint works
- [ ] Test OAuth discovery endpoints
- [ ] Test SSE endpoint with HEAD request
- [ ] Add to Claude.ai and test connection
- [ ] Update documentation

## Best Practices

1. **Naming Convention**: Use lowercase, single words (demo, production, marketing)
2. **Container Names**: Use pattern `mcp-server-{environment}`
3. **Environment Variables**: Use pattern `MSSQL_*_{ENVIRONMENT}`
4. **Security**: Production should have most restrictive settings
5. **Testing**: Always test in this order: health → OAuth → SSE
6. **Documentation**: Update root endpoint JSON to reflect actual status
7. **Backup**: Always backup configs before changes

---

This guide provides everything needed to add new MCP server environments to your multi-tenant setup. Each environment is completely isolated with its own database, credentials, and access controls.