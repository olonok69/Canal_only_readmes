# Read-Only Mode Implementation Guide for MSSQL MCP Server

## Overview

This guide provides multiple methods to restrict the MSSQL MCP Server to read-only operations, preventing INSERT, UPDATE, DELETE, and DDL operations. You can implement one or combine multiple approaches for defense in depth.

## Method 1: Application-Level Restrictions (Recommended)

### Implementation Steps

1. **Replace the server file**:
```bash
# Backup current server
cp server_oauth.py server_oauth_readwrite.py

# Replace with read-only version
# Copy the provided server_readonly.py content to server_oauth.py
```

2. **Configure environment variables**:
```bash
# Add to .env file
READ_ONLY_MODE=true
ALLOWED_OPERATIONS=SELECT
BLOCK_DDL=true
BLOCK_STORED_PROCEDURES=true
BLOCK_TRANSACTIONS=true
```

3. **Key features of the read-only implementation**:

#### SQL Query Validation
The server validates all SQL queries before execution:

```python
# Blocked patterns
- INSERT INTO
- UPDATE ... SET
- DELETE FROM
- TRUNCATE TABLE
- DROP TABLE/INDEX/VIEW
- CREATE TABLE/INDEX/VIEW
- ALTER TABLE
- GRANT/REVOKE
- EXEC/EXECUTE (stored procedures)
- MERGE
- BULK INSERT
- SELECT INTO (creates new table)
```

#### Safe Operations Allowed
```python
# Allowed operations
- SELECT queries
- WITH (Common Table Expressions)
- SHOW commands
- DESCRIBE commands
- EXPLAIN plans
- INFORMATION_SCHEMA queries
```

## Method 2: Database User Permissions (Most Secure)

### Create a Read-Only Database User

```sql
-- Connect to SQL Server as admin
USE master;
GO

-- Create a login for read-only access
CREATE LOGIN mcp_readonly_user WITH PASSWORD = 'StrongPassword123!';
GO

-- Switch to your database
USE YourDatabase;
GO

-- Create a user for the login
CREATE USER mcp_readonly_user FOR LOGIN mcp_readonly_user;
GO

-- Grant only SELECT permissions
-- Option 1: Grant to all tables
GRANT SELECT ON SCHEMA::dbo TO mcp_readonly_user;
GO

-- Option 2: Grant to specific tables
GRANT SELECT ON dbo.TableName1 TO mcp_readonly_user;
GRANT SELECT ON dbo.TableName2 TO mcp_readonly_user;
GO

-- Explicitly DENY write permissions (extra safety)
DENY INSERT, UPDATE, DELETE ON SCHEMA::dbo TO mcp_readonly_user;
GO

-- Deny DDL operations
DENY CREATE TABLE, ALTER, DROP TO mcp_readonly_user;
GO

-- Deny execute permissions on stored procedures
DENY EXECUTE ON SCHEMA::dbo TO mcp_readonly_user;
GO
```

### Update Environment Variables
```bash
# .env file
MSSQL_USER=mcp_readonly_user
MSSQL_PASSWORD=StrongPassword123!
```

## Method 3: Connection String Configuration

### Use ApplicationIntent Parameter
```python
# In get_db_config() function
connection_string = (
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server={server};"
    f"Database={database};"
    f"UID={user};"
    f"PWD={password};"
    f"ApplicationIntent=ReadOnly;"  # This hints to SQL Server
    f"TrustServerCertificate=yes;"
)
```

## Method 4: SQL Server Read-Only Database

### Set Entire Database to Read-Only
```sql
-- Set database to read-only (requires admin privileges)
ALTER DATABASE YourDatabase SET READ_ONLY WITH NO_WAIT;
GO

-- To revert (if needed)
-- ALTER DATABASE YourDatabase SET READ_WRITE WITH NO_WAIT;
-- GO
```

## Method 5: Using Database Roles

### Create and Assign Read-Only Role
```sql
-- Create a custom read-only role
USE YourDatabase;
GO

CREATE ROLE db_readonly_mcp;
GO

-- Grant SELECT permissions to the role
GRANT SELECT ON SCHEMA::dbo TO db_readonly_mcp;
GO

-- Add user to the role
ALTER ROLE db_readonly_mcp ADD MEMBER mcp_readonly_user;
GO

-- Ensure user is only in read-only roles
ALTER ROLE db_datareader ADD MEMBER mcp_readonly_user;
ALTER ROLE db_datawriter DROP MEMBER mcp_readonly_user;
ALTER ROLE db_ddladmin DROP MEMBER mcp_readonly_user;
GO
```

## Method 6: Nginx Rate Limiting for Additional Protection

### Add Rate Limiting to Prevent Abuse
```nginx
# nginx/conf.d/rate-limiting.conf
# Limit write-like operations more strictly
map $request_body $contains_write {
    ~*"(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)" 1;
    default 0;
}

limit_req_zone $binary_remote_addr zone=readonly:10m rate=30r/s;
limit_req_zone $contains_write zone=writes:1m rate=1r/m;

# In location blocks
location /sse {
    # Apply rate limiting
    limit_req zone=readonly burst=50 nodelay;
    
    # Block if contains write operations
    if ($contains_write) {
        return 403 "Write operations not allowed";
    }
    
    # ... rest of configuration
}
```

## Testing Read-Only Restrictions

### Create Test Script
```python
#!/usr/bin/env python3
"""test_readonly.py - Test read-only restrictions"""

import requests
import json
import uuid

BASE_URL = "https://data.forensic-bot.com"

def get_token():
    """Get OAuth token"""
    # Register client
    reg_response = requests.post(f"{BASE_URL}/register", 
                                 json={"client_name": "test"})
    client = reg_response.json()
    
    # Get token
    token_response = requests.post(f"{BASE_URL}/token",
                                   data={
                                       "grant_type": "client_credentials",
                                       "client_id": client["client_id"],
                                       "client_secret": client["client_secret"]
                                   })
    return token_response.json()["access_token"]

def test_query(query: str, should_fail: bool = False):
    """Test a SQL query"""
    token = get_token()
    
    message = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "tools/call",
        "params": {
            "name": "execute_sql",
            "arguments": {
                "query": query
            }
        }
    }
    
    response = requests.post(f"{BASE_URL}/sse",
                            json=message,
                            headers={"Authorization": f"Bearer {token}"})
    
    result = response.json()
    
    if should_fail:
        # Check if query was blocked
        if "error" in str(result):
            print(f"✓ BLOCKED: {query[:50]}...")
            return True
        else:
            print(f"✗ ALLOWED (SHOULD BE BLOCKED): {query[:50]}...")
            return False
    else:
        # Check if query succeeded
        if "error" not in str(result):
            print(f"✓ ALLOWED: {query[:50]}...")
            return True
        else:
            print(f"✗ BLOCKED (SHOULD BE ALLOWED): {query[:50]}...")
            return False

def run_tests():
    """Run all tests"""
    print("Testing Read-Only Restrictions")
    print("=" * 50)
    
    # Should be ALLOWED
    allowed_queries = [
        "SELECT TOP 10 * FROM Customers",
        "SELECT COUNT(*) FROM Orders",
        "WITH cte AS (SELECT * FROM Products) SELECT * FROM cte",
        "SELECT * FROM INFORMATION_SCHEMA.TABLES",
    ]
    
    # Should be BLOCKED
    blocked_queries = [
        "INSERT INTO Customers (Name) VALUES ('Test')",
        "UPDATE Customers SET Name = 'Test' WHERE ID = 1",
        "DELETE FROM Customers WHERE ID = 1",
        "DROP TABLE Customers",
        "CREATE TABLE Test (ID INT)",
        "ALTER TABLE Customers ADD COLUMN Test VARCHAR(50)",
        "TRUNCATE TABLE Customers",
        "EXEC sp_executesql 'SELECT 1'",
        "SELECT * INTO NewTable FROM Customers",
        "GRANT SELECT ON Customers TO public",
    ]
    
    print("\nTesting ALLOWED queries:")
    for query in allowed_queries:
        test_query(query, should_fail=False)
    
    print("\nTesting BLOCKED queries:")
    for query in blocked_queries:
        test_query(query, should_fail=True)
    
    print("\n" + "=" * 50)
    print("Test Complete")

if __name__ == "__main__":
    run_tests()
```

## Deployment Steps

### 1. Update Docker Image
```dockerfile
# Add to Dockerfile
ENV READ_ONLY_MODE=true
ENV BLOCK_DDL=true
ENV BLOCK_STORED_PROCEDURES=true
ENV BLOCK_TRANSACTIONS=true
```

### 2. Rebuild and Deploy
```bash
# Stop current server
docker compose down

# Rebuild with read-only server
docker compose build --no-cache

# Start server
docker compose up -d

# Check logs
docker compose logs -f mcp-server
```

### 3. Verify Read-Only Mode
```bash
# Check health endpoint
curl https://data.forensic-bot.com/health

# Should show:
{
  "status": "healthy",
  "mode": "read_only",
  "allowed_operations": ["SELECT"],
  "security": {
    "block_ddl": true,
    "block_stored_procedures": true,
    "block_transactions": true
  }
}
```

## Monitoring and Alerts

### Log Monitoring
```bash
# Monitor blocked queries
docker compose logs mcp-server | grep "Blocked unsafe query"

# Create alert script
cat > monitor_blocked_queries.sh << 'EOF'
#!/bin/bash
LOG_FILE="/var/log/mcp/blocked_queries.log"
ALERT_THRESHOLD=10

# Count blocked queries in last hour
BLOCKED_COUNT=$(docker compose logs --since=1h mcp-server | grep -c "Blocked unsafe query")

if [ $BLOCKED_COUNT -gt $ALERT_THRESHOLD ]; then
    echo "Alert: $BLOCKED_COUNT write attempts blocked in the last hour" | \
    mail -s "MCP Server Security Alert" admin@example.com
fi

echo "$(date): $BLOCKED_COUNT blocked queries" >> $LOG_FILE
EOF

# Add to crontab
*/10 * * * * /path/to/monitor_blocked_queries.sh
```

## Rollback Plan

If you need to restore write capabilities:

### 1. Application Level
```bash
# Update .env
READ_ONLY_MODE=false
ALLOWED_OPERATIONS=SELECT,INSERT,UPDATE,DELETE

# Use original server
cp server_oauth_readwrite.py server_oauth.py

# Restart
docker compose restart mcp-server
```

### 2. Database Level
```sql
-- Restore permissions
GRANT INSERT, UPDATE, DELETE ON SCHEMA::dbo TO mcp_user;
GO

-- Or switch to read-write user
-- Update .env with read-write credentials
```

## Security Best Practices

1. **Use Multiple Layers**: Combine application-level and database-level restrictions
2. **Audit Regularly**: Review logs for attempted write operations
3. **Separate Environments**: Use different servers for read-only vs read-write
4. **Regular Backups**: Maintain backups before any permission changes
5. **Document Changes**: Keep track of all security modifications

## Troubleshooting

### Common Issues and Solutions

#### Issue: Legitimate SELECT queries being blocked
```python
# Check if query contains keywords that look like writes
# Example: SELECT statement with 'UPDATE' in a string
SELECT * FROM Logs WHERE message = 'UPDATE completed'

# Solution: Refine regex patterns in SQLValidator
```

#### Issue: User needs temporary write access
```bash
# Quick toggle via environment variable
docker compose exec mcp-server sh -c "export READ_ONLY_MODE=false"
docker compose restart mcp-server

# Revert after task
docker compose exec mcp-server sh -c "export READ_ONLY_MODE=true"
docker compose restart mcp-server
```

#### Issue: Performance impact from validation
```python
# Consider caching validation results
from functools import lru_cache

@lru_cache(maxsize=1000)
def is_query_safe_cached(query_hash):
    return SQLValidator.is_query_safe(query)
```

## Conclusion

The read-only implementation provides multiple layers of security:

1. **Application validation** - Fastest, catches issues before database
2. **Database permissions** - Most secure, enforced by SQL Server
3. **Connection settings** - Hints to database about intent
4. **Rate limiting** - Prevents abuse attempts
5. **Monitoring** - Alerts on suspicious activity

For maximum security, implement at least methods 1 and 2 together.

---
Implementation Guide Version: 1.0.0
Last Updated: January 2025