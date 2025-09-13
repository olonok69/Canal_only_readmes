# AI-Powered CRM & Graph Database Integration Platform

A comprehensive full-stack application that provides AI-powered interactions with Neo4j graph databases, HubSpot CRM systems, and Yahoo Finance data through Model Context Protocol (MCP) servers. This platform enables seamless data analysis, management, and automation across your database, CRM, and financial data infrastructure with enterprise-grade authentication and security.

## 🚀 System Overview

This application consists of four integrated components working together through the Model Context Protocol (MCP):

1. **Streamlit Client** - Secure AI chat interface with enterprise authentication and multi-provider support
2. **Yahoo Finance MCP Server** - Financial data analysis with proprietary algorithms and technical indicators
3. **Neo4j MCP Server** - Graph database operations via Cypher queries with schema validation
4. **HubSpot MCP Server** - Complete CRM integration with 25+ tools and full CRUD operations

### Architecture Diagram

![System Architecture](image.png)

## ⚡ Quick Start

### Prerequisites
- Docker & Docker Compose
- Neo4j database (with APOC plugin)
- HubSpot Private App Access Token
- OpenAI API key or Azure OpenAI configuration

### 1. Environment Setup

Create a `.env` file in the project root:

```env
# OpenAI Configuration (choose one)
OPENAI_API_KEY=your_openai_api_key_here

# OR Azure OpenAI Configuration
AZURE_API_KEY=your_azure_api_key
AZURE_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_DEPLOYMENT=your_deployment_name
AZURE_API_VERSION=2023-12-01-preview

# Neo4j Configuration
NEO4J_URI=bolt://host.docker.internal:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
NEO4J_DATABASE=neo4j

# HubSpot Configuration
PRIVATE_APP_ACCESS_TOKEN=your_hubspot_private_app_token

# Optional: Enable SSL for client
SSL_ENABLED=false
```

### 2. Generate User Authentication

```bash
# Generate authentication credentials
cd client
python simple_generate_password.py

# This creates default users:
# admin: very_Secure_p@ssword_123!
# juan: fl09877@
# pepe_romero: MrRok0934@#mero2024!
# demo_user: strong_password_123!
```

### 3. Launch the Platform

```bash
# Build and start all services
docker-compose up --build

# Or start individual services
docker-compose up mcpserver3  # Yahoo Finance MCP Server
docker-compose up mcpserver4  # Neo4j MCP Server
docker-compose up mcpserver5  # HubSpot MCP Server  
docker-compose up hostclient  # Streamlit Client
```

### 4. Access the Application

- **Main Interface**: http://localhost:8501
- **HTTPS Interface** (if enabled): https://localhost:8502
- **Yahoo Finance Server Health**: http://localhost:8002/health
- **Neo4j Server Health**: http://localhost:8003/health
- **HubSpot Server Health**: http://localhost:8004/health

## 🎯 Key Features

### **Enterprise Authentication & Security**
- **User Authentication System**: Secure login with bcrypt password hashing
- **Session Management**: Persistent user sessions with configurable expiry
- **Role-Based Access**: Pre-authorized email domains and user management
- **SSL Support**: Optional HTTPS with self-signed certificates
- **Secure Cookies**: Configurable authentication cookies with custom keys

### **Advanced AI-Powered Interactions**
- **Multi-provider AI Support**: OpenAI and Azure OpenAI with dynamic switching
- **Natural Language Queries**: Conversational interface for complex operations
- **Intelligent Tool Selection**: Automatic routing to appropriate MCP servers
- **Conversation Memory**: Context-aware conversations with history management
- **Schema-Aware Operations**: Automatic validation against database and CRM schemas

### **Comprehensive Financial Data Analysis**
- **Real-time Stock Data**: Access current market prices and trading information with no API costs
- **Advanced Technical Analysis**: MACD, Bollinger Bands, Donchian Channels with proprietary scoring
- **Custom Trading Algorithms**: Combined indicator scoring for investment decisions (-100 to +100 scale)
- **Portfolio Analysis**: Multi-timeframe analysis with trading signal generation
- **Fibonacci Integration**: Advanced Bollinger-Fibonacci strategy implementation

### **Complete Graph Database Operations**
- **Schema Discovery**: Automatic Neo4j structure analysis with APOC integration
- **Query Validation**: Schema-aware Cypher query validation before execution
- **Read/Write Operations**: Safe MATCH queries and controlled data modifications
- **Error Prevention**: Validates queries against actual database structure
- **Visual Results**: Structured data presentation with relationship mapping

### **Full HubSpot CRM Integration (25 Tools)**
- **Complete CRUD Operations**: Create, read, update, delete across all object types
- **Advanced Object Management**: Contacts, companies, deals, tickets, custom objects
- **Association Management**: Link and manage relationships between CRM objects
- **Property Management**: Create and manage custom fields and data structures
- **Engagement Tracking**: Notes, tasks, and activity logging with full lifecycle
- **Workflow Integration**: Access to automation insights and workflow management
- **UI Integration**: Generate direct links to HubSpot interface for seamless workflow
- **Batch Operations**: Efficient bulk data handling for large-scale operations

### **Technical Excellence**
- **Modern Tabbed Interface**: Intuitive UI with Configuration, Connections, Tools, and Chat tabs
- **Docker Containerization**: Production-ready deployment and scaling
- **Real-time Communication**: Server-Sent Events (SSE) for responsive MCP communication
- **Comprehensive Validation**: Schema validation across all tools and operations
- **Robust Error Handling**: Detailed error management with debugging capabilities
- **Health Monitoring**: Built-in health checks and system monitoring

## 💻 Technical Stack

### **Frontend & Client**
```yaml
Technology: Streamlit 1.44+
Language: Python 3.11+
Authentication: Streamlit Authenticator 0.3.2
Security: bcrypt, SSL/TLS support
UI Framework: Custom CSS, responsive design
```

### **Backend Services**
```yaml
Yahoo Finance Server:
  - FastAPI + uvicorn
  - Python 3.12+
  - yfinance library
  - Custom algorithms

Neo4j Server:
  - FastAPI + uvicorn  
  - Python 3.11+
  - neo4j-driver
  - APOC procedures

HubSpot Server:
  - Express.js + Node.js 18+
  - JavaScript ES6+
  - 25 specialized tools
  - Zod validation
```

### **Infrastructure**
```yaml
Containerization: Docker + Docker Compose
Protocol: Model Context Protocol (MCP)
Transport: Server-Sent Events (SSE)
Database: Neo4j 5.0+ with APOC
External APIs: Yahoo Finance, HubSpot REST API
```

### **AI & ML**
```yaml
Framework: LangChain + LangGraph
Providers: OpenAI GPT-4o, Azure OpenAI
Agent: ReAct (Reasoning + Acting)
Context: Conversation memory + tool history
```

## 📚 Usage Examples

### **Authentication & Getting Started**

```
# Login with default credentials:
# use your own ones
admin: very_Secure_p@ssword_123!
juan: fl09877@
pepe_romero: MrRok0934@#mero2024!
demo_user: strong_password_123!
```

### **Financial Analysis Workflows**

```
"What's the current MACD score for AAPL with custom parameters?"
"Calculate a comprehensive Bollinger-Fibonacci strategy for Tesla stock"
"Give me a combined technical analysis score for Microsoft over 6 months"
"Show me Donchian channel analysis with volatility assessment for the S&P 500"
"Compare trading signals for AAPL, TSLA, and MSFT using multiple indicators"
```

### **Database Analysis Workflows**

```
"Show me the complete database schema and explain the data relationships"
"How many visitors converted to customers this year, and what's the conversion path?"
"Find all connections between person nodes and company nodes with relationship details"
"Create a new person node with properties and link it to an existing company"
"Validate this Cypher query against the current schema before execution"
```

### **CRM Management Workflows**

```
"Get my HubSpot user details and show me all contacts created this month"
"Create a new company called Tech Solutions with complete contact information"
"List all open deals above $10,000 and their associated contacts"
"Create a follow-up task for the Amazon deal and generate a HubSpot link to view it"
"Search for all contacts in the technology industry and export their details"
"Associate John Smith with Acme Corp and add a note about their recent meeting"
```

### **Advanced Integration Workflows**

```
"Analyze AAPL stock performance using multiple technical indicators, then create a HubSpot task to review our tech investments based on the analysis"
"Compare customer data between our Neo4j graph database and HubSpot CRM to identify data inconsistencies"
"Find high-value deals in HubSpot, cross-reference with our database relationships, and generate a comprehensive investment report"
"Create a complete customer journey analysis combining graph database relationships, CRM engagement history, and market performance data"
```

## 📊 Performance & Scaling

### **Performance Metrics**

```yaml
Response Times:
  - Authentication: <200ms
  - Tool Discovery: <500ms
  - Simple Queries: <2s
  - Complex Analysis: <10s

Throughput:
  - Concurrent Users: 50+ (single instance)
  - Tool Executions: 100+ per minute
  - Data Processing: 10MB+ per query
```

### **Scaling Strategies**

#### **Horizontal Scaling**
```yaml
Load Balancing: Multiple client instances
MCP Servers: Independent scaling per service
Database: Neo4j clustering
Cache: Redis for session storage
```

#### **Vertical Scaling**
```yaml
Memory: 2GB+ per container
CPU: 2+ cores recommended
Storage: SSD for Neo4j performance
Network: 1Gbps+ for large datasets
```

## 🔧 Component Documentation

Each component has detailed documentation for advanced configuration and development:

### [🏠 Streamlit Client Documentation](./client/Readme.md)
- **Enterprise Authentication**: Secure user management with bcrypt encryption
- **Multi-Provider AI Setup**: OpenAI and Azure OpenAI with dynamic switching
- **Modern Tabbed Interface**: Configuration, Connections, Tools, and Chat organization
- **SSL Support**: Optional HTTPS with certificate generation
- **Session Management**: Persistent conversations with user isolation

### [📈 Yahoo Finance MCP Server Documentation](./servers/server3/Readme.md)
- **6 Advanced Financial Tools**: MACD scoring, Donchian channels, Bollinger-Fibonacci strategies
- **Proprietary Algorithms**: Custom scoring systems with weighted components
- **Technical Indicator Calculations**: Real-time market data with no API costs
- **Trading Signal Generation**: Automated buy/sell/hold recommendations
- **Portfolio Analysis**: Multi-timeframe and multi-indicator analysis

### [🗄️ Neo4j MCP Server Documentation](./servers/server4/Readme.md)
- **Schema-First Approach**: Mandatory schema discovery before operations
- **Query Validation**: Prevents errors by validating against actual database structure
- **APOC Integration**: Advanced procedures for comprehensive schema analysis
- **Safe Operations**: Separate read and write operations with validation
- **Connection Management**: Robust async connection handling

### [🏢 HubSpot MCP Server Documentation](./servers/server5/Readme.md)
- **25 Complete Tools**: Full coverage of HubSpot API capabilities
- **Advanced Object Management**: All CRM object types with CRUD operations
- **Association Management**: Complete relationship mapping and management
- **Property Management**: Custom fields and data structure management
- **Workflow Integration**: Automation insights and workflow access
- **UI Integration**: Direct links to HubSpot interface for seamless workflow

For comprehensive tool usage, see the [HubSpot Tools Implementation Guide](./servers/server5/HUBSPOT_TOOLS_GUIDE.md).

## 🛠️ Development & Customization

### **User Management**

```bash
# Add new users by editing simple_generate_password.py
cd client
nano simple_generate_password.py  # Add users to the users dictionary
python simple_generate_password.py  # Generate new config
```

### **AI Provider Configuration**

```python
# Add new AI providers in client/config.py
MODEL_OPTIONS = {
    'OpenAI': 'gpt-4o',
    'Azure OpenAI': 'o3-mini',
    'Custom Provider': 'your-model'
}
```

### **MCP Server Configuration**

```json
// Update client/servers_config.json for server endpoints
{
  "mcpServers": {
    "Custom Server": {
      "transport": "sse",
      "url": "http://your-server:port/sse",
      "timeout": 600
    }
  }
}
```

### **Adding Custom Tools**

1. **Yahoo Finance Tools**: Extend financial analysis with custom indicators
2. **Neo4j Tools**: Add specialized graph analysis operations
3. **HubSpot Tools**: Implement additional CRM integrations
4. **Client Tools**: Integrate new services via MCP protocol

## 🔒 Security & Best Practices

### **Authentication Security**
- **Enterprise-Grade Encryption**: bcrypt password hashing with salt
- **Session Security**: Configurable session expiry and secure cookies
- **Access Control**: Pre-authorized email domains and role-based access
- **SSL/TLS Support**: Optional HTTPS with certificate generation

### **Data Protection**
- **Input Validation**: Comprehensive validation across all components
- **Schema Validation**: Database and CRM operation validation
- **Sanitized Error Messages**: Secure error handling without data exposure
- **API Key Protection**: Environment variable based credential management

### **Network Security**
- **Containerized Deployment**: Isolated service architecture
- **Configurable Port Mapping**: Flexible network configuration
- **Health Check Endpoints**: Monitoring without exposing sensitive data
- **Rate Limiting**: Built-in protection against abuse

## 📊 Monitoring & Debugging

### **Health Checks & System Status**
- **Overall System**: Authentication status and connection indicators
- **Yahoo Finance Server**: http://localhost:8002/health
- **Neo4j Server**: http://localhost:8003/health (includes database connectivity)
- **HubSpot Server**: http://localhost:8004/health (includes API token validation)

### **Advanced Debugging Tools**
- **Tool Execution History**: Detailed execution logs in expandable UI sections
- **User Session Tracking**: Login time, activity monitoring, and session data
- **Conversation Memory**: Context-aware debugging with conversation analysis
- **Authentication Logs**: Comprehensive login and access tracking

### **Performance Monitoring**
- **Query Execution Timing**: Database and API response time tracking
- **Tool Usage Analytics**: Monitor most-used tools and execution patterns
- **Resource Usage**: Docker container performance and memory utilization
- **Financial Data Refresh**: Market data update frequencies and caching

## 🚀 Deployment Options

### **Development Deployment**
```bash
# Quick start for development
docker-compose up --build
```

### **Production Deployment**
```bash
# Enable SSL for production
echo "SSL_ENABLED=true" >> .env

# Use production-grade passwords
cd client && python simple_generate_password.py

# Deploy with reverse proxy
# Configure nginx/traefik for SSL termination
# Implement proper secret management
# Set up monitoring and alerting
```

### **Enterprise Scaling**
- **Horizontal Scaling**: Multiple MCP server instances with load balancing
- **Database Connection Pooling**: Optimized Neo4j connection management
- **Session Clustering**: Multi-instance session management
- **Monitoring Integration**: Prometheus/Grafana compatible metrics

## 🐛 Troubleshooting

### **Authentication Issues**
- **Login Failures**: Check `keys/config.yaml` exists and credentials match
- **Session Problems**: Clear browser cookies and restart application
- **Permission Errors**: Verify email domains in preauthorized list

### **Connection Problems**
- **MCP Server Issues**: Verify all services running with `docker-compose ps`
- **Network Connectivity**: Check Docker network configuration
- **API Authentication**: Validate API keys and HubSpot token permissions

### **Tool Execution Issues**
- **Schema Validation**: Always call `get_neo4j_schema` before database operations
- **HubSpot Operations**: Start with `hubspot-get-user-details` for context
- **Query Failures**: Check tool execution history for detailed error messages

### **Performance Issues**
- **Slow Responses**: Monitor tool execution timing in debug panels
- **Memory Usage**: Check Docker container resource utilization
- **API Rate Limits**: Monitor HubSpot and financial data API usage

## 📄 Technical Documentation

For detailed technical information and presentations:

### [📋 Technical Overview (English)](./technical_en.md)
Complete technical presentation covering:
- Architecture deep dive
- Component analysis
- Performance considerations
- Security implementation
- Deployment strategies

### [📋 Presentación Técnica (Español)](./technical_es.md)
Presentación técnica completa que cubre:
- Análisis profundo de arquitectura
- Análisis de componentes
- Consideraciones de rendimiento
- Implementación de seguridad
- Estrategias de despliegue

## 🤝 Contributing

### **Development Workflow**
1. **Authentication Testing**: Verify login/logout functionality
2. **Tool Integration**: Test all MCP server connections and tool availability
3. **Security Review**: Validate input sanitization and access controls
4. **Performance Testing**: Monitor response times and resource usage

### **Code Standards**
- **Python**: PEP 8 compliance with comprehensive type hints
- **JavaScript**: ES6+ standards with Zod schema validation
- **Docker**: Security best practices with non-root users
- **Authentication**: Secure credential handling and session management

## 🔗 Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Yahoo Finance API Documentation](https://pypi.org/project/yfinance/)
- [Neo4j Documentation](https://neo4j.com/docs/) with [APOC Procedures](https://neo4j.com/docs/apoc/)
- [HubSpot API Documentation](https://developers.hubspot.com/docs/api/overview)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Authenticator Documentation](https://github.com/mkhorasani/Streamlit-Authenticator)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

**Version**: 2.0.0  
**Last Updated**: June 2025  
**Authentication**: Streamlit Authenticator 0.3.2 with bcrypt encryption  
**Compatibility**: Docker 20+, Python 3.11+, Node.js 18+, Neo4j 5.0+  
**Security**: Enterprise-grade authentication with SSL/TLS support