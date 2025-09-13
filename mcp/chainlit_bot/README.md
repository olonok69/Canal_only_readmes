# MCP-Powered Neo4j & HubSpot Chatbot

A sophisticated conversational AI application that connects **Neo4j graph databases** and **HubSpot CRM** through the **Model Context Protocol (MCP)**, built with **Chainlit** for an intuitive chat interface.

## 🌟 Overview

This application demonstrates the power of combining multiple data sources through MCP servers, allowing users to query and analyze data from both Neo4j graph databases and HubSpot CRM systems using natural language conversations.

### Key Features

- 🗃️ **Neo4j Integration**: Query graph databases with natural language
- 🏢 **HubSpot CRM Access**: Manage contacts, companies, deals, and more
- 🔄 **Cross-System Analysis**: Find connections between Neo4j and HubSpot data
- 🤖 **Intelligent Exploration**: AI automatically explores data structures and finds relevant information
- 💬 **Natural Language Interface**: Powered by Chainlit for seamless user experience
- 🔧 **Flexible Architecture**: Easy to extend with additional MCP servers

## 🏗️ Technology Stack

### Core Technologies

#### Model Context Protocol (MCP)
**What is MCP?**
- A standardized protocol for connecting AI assistants to external data sources and tools
- Developed by Anthropic to enable secure, structured interactions between AI models and various systems
- Provides a uniform interface for accessing databases, APIs, and other services

**Why MCP?**
- **Security**: Controlled access to external systems
- **Standardization**: Consistent interface across different data sources
- **Extensibility**: Easy to add new tools and data sources
- **Type Safety**: Structured schemas for reliable data exchange

#### Chainlit
**What is Chainlit?**
- A Python framework for building conversational AI applications
- Provides chat interfaces, streaming responses, and session management
- Optimized for AI/ML workflows and integrations

**Why Chainlit?**
- **Rapid Development**: Quick setup for chat interfaces
- **Streaming Support**: Real-time response streaming
- **Session Management**: Handles user sessions and message history
- **Customizable UI**: Flexible interface customization

### Data Sources

#### Neo4j Graph Database
- **Purpose**: Store and query complex relationships between entities
- **Use Cases**: Network analysis, recommendation systems, fraud detection
- **Query Language**: Cypher for expressive graph queries

#### HubSpot CRM
- **Purpose**: Customer relationship management and sales pipeline tracking
- **Use Cases**: Contact management, deal tracking, marketing automation
- **Integration**: REST API access through MCP server

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js** (for HubSpot MCP server)
- **uvx** (for Python package management)
- **Neo4j Database** (local or Neo4j Aura)
- **HubSpot Account** with Private App access token

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd mcp-neo4j-client
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install MCP tools**
```bash
# Install uvx for Python MCP servers
pip install uvx

# Install Node.js dependencies (for HubSpot)
npm install -g @hubspot/mcp-server
```

4. **Set up environment variables**
```bash
cp .env.template .env
# Edit .env with your credentials
```

### Environment Configuration

Create a `.env` file with the following variables:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_MODEL=gpt-4o
OPENAI_API_VERSION=2024-08-01-preview

# Neo4j Configuration
NEO4J_URI=neo4j+s://your-id.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
NEO4J_DATABASE=neo4j

# HubSpot Configuration
HUBSPOT_PRIVATE_APP_TOKEN=your-hubspot-token
```

### Running the Application

1. **Verify setup**
```bash
python test_hubspot.py
```

2. **Start the application**
```bash
chainlit run app.py --port 8080 --host 0.0.0.0
```

3. **Access the interface**
Open your browser to `http://localhost:8080`

## 🔧 Architecture

### System Architecture

```
┌─────────────────┐    ┌───────────────────┐    ┌──────────────────┐
│   Chainlit UI   │    │   Python App      │    │  Azure OpenAI    │
│                 │◄──►│                   │◄──►│                  │
│ - Chat Interface│    │ - Message Routing │    │ - LLM Processing │
│ - Streaming     │    │ - MCP Integration │    │  - Tool Calling  │
│ - Session Mgmt  │    │ - Response Mgmt   │    │  - JSON Schemas  │
└─────────────────┘    └───────────────────┘    └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   MCP Client     │
                       │                  │
                       │ - Server Mgmt    │
                       │ - Tool Validation│
                       │ - Schema Fixing  │
                       └──────────────────┘
                         │              │
                         ▼              ▼
              ┌─────────────────┐  ┌─────────────────┐
              │  Neo4j MCP      │  │ HubSpot MCP     │
              │                 │  │                 │
              │ - Cypher Queries│  │ - CRM Operations│
              │ - Schema Info   │  │ - API Calls     │
              │ - Read/Write    │  │ - Object Mgmt   │
              └─────────────────┘  └─────────────────┘
                         │              │
                         ▼              ▼
              ┌─────────────────┐  ┌─────────────────┐
              │   Neo4j DB      │  │   HubSpot API   │
              │                 │  │                 │
              │ - Graph Data    │  │ - CRM Data      │
              │ - Relationships │  │ - Contacts      │
              │ - Properties    │  │ - Companies     │
              └─────────────────┘  └─────────────────┘
```

### Key Components

#### 1. **MCPClient** (`mcp_client.py`)
- Manages connections to multiple MCP servers
- Validates and fixes tool schemas for OpenAI compatibility
- Handles async cleanup and error management

#### 2. **ChatClient** (`app.py`)
- Manages conversation flow with Azure OpenAI
- Handles tool calling and response streaming
- Maintains conversation context and memory

#### 3. **MCP Servers**
- **Neo4j Server**: Provides Cypher query execution and schema access
- **HubSpot Server**: Offers comprehensive CRM operations

### Tool Schema Validation

The application includes sophisticated schema validation that:
- Fixes missing `items` properties in array schemas
- Removes problematic JSON Schema properties
- Ensures OpenAI function calling compatibility
- Provides detailed error reporting

## 🔍 Usage Examples

### Neo4j Queries

**Explore your database structure:**
```
"What's in my Neo4j database?"
```

**Find specific relationships:**
```
"Show me all surgeons and their related sessions"
```

**Complex analysis:**
```
"What are the most common relationships in my graph?"
```

### HubSpot Operations

**Explore CRM data:**
```
"Show me my HubSpot contacts"
```

**Search and filter:**
```
"Find all companies in the technology sector"
```

**Create and update:**
```
"Create a new contact for John Smith at Acme Corp"
```

### Cross-System Analysis

**Data correlation:**
```
"Compare my Neo4j user data with HubSpot contacts"
```

**Enrichment opportunities:**
```
"Which Neo4j entities could be enhanced with HubSpot data?"
```

## 🛠️ Development

### Project Structure

```
mcp-neo4j-client/
├── app.py                 # Main Chainlit application
├── mcp_client.py          # MCP client implementation
├── mcp_config.json        # MCP server configurations
├── main.py                # Alternative client interface
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── .env                   # Environment variables
├── test_*.py              # Testing utilities
└── README.md              # This file
```

### Testing

The application includes comprehensive testing utilities:

```bash
# Test Neo4j connection
python test_neo4j.py

# Test MCP connections
python test_mcp.py

# Test schema validation
python test_schema.py

# Comprehensive verification
python test_hubspot.py
```

### Adding New MCP Servers

1. **Update configuration** (`mcp_config.json`):
```json
{
  "mcpServers": {
    "your-new-server": {
      "command": "your-command",
      "args": ["arg1", "arg2"],
      "env": {
        "API_KEY": "${YOUR_API_KEY}"
      }
    }
  }
}
```

2. **Add environment variables** (`.env`):
```env
YOUR_API_KEY=your-api-key-value
```

3. **The application will automatically**:
   - Connect to the new server
   - Validate and fix tool schemas
   - Make tools available to the AI

## 🔧 Configuration

### MCP Server Configuration

The `mcp_config.json` file defines how to connect to MCP servers:

```json
{
  "mcpServers": {
    "neo4j": {
      "command": "uvx",
      "args": ["mcp-neo4j-cypher@0.2.1"],
      "env": {
        "NEO4J_URI": "${NEO4J_URI}",
        "NEO4J_USERNAME": "${NEO4J_USERNAME}",
        "NEO4J_PASSWORD": "${NEO4J_PASSWORD}",
        "NEO4J_DATABASE": "${NEO4J_DATABASE}"
      }
    },
    "hubspot": {
      "command": "npx",
      "args": ["-y", "@hubspot/mcp-server"],
      "env": {
        "PRIVATE_APP_ACCESS_TOKEN": "${HUBSPOT_PRIVATE_APP_TOKEN}"
      }
    }
  }
}
```

### System Prompts

The application uses an intelligent system prompt that:
- Encourages exploratory data analysis
- Promotes flexible matching and inclusive queries
- Guides cross-system data correlation
- Emphasizes understanding data before querying

## 🚨 Troubleshooting

### Common Issues

#### 1. **MCP Connection Failures**
```bash
# Run comprehensive diagnostics
python test_hubspot.py
```

#### 2. **Neo4j Connection Issues**
- Verify Neo4j Aura credentials
- Check URI format: `neo4j+s://xxxxx.databases.neo4j.io`
- Test connection: `python test_neo4j.py`

#### 3. **HubSpot API Issues**
- Verify Private App token permissions
- Ensure Node.js is installed for `npx`
- Check token scope requirements

#### 4. **Tool Schema Errors**
- The application automatically fixes most schema issues
- Check console output for validation warnings
- Run: `python test_schema.py`

### Debug Scripts

- `debug_mcp.py`: Diagnose MCP Neo4j issues
- `test_workflow.py`: Demonstrate flexible query patterns
- `setup.py`: Verify complete environment setup

## 🔐 Security Considerations

- **Environment Variables**: Keep sensitive credentials in `.env` files
- **MCP Isolation**: Each MCP server runs in isolated processes
- **Schema Validation**: Prevents malformed tool calls
- **Error Handling**: Graceful handling of connection failures

## 🚀 Advanced Features

### Intelligent Query Building

The AI automatically:
1. **Explores schema** before building queries
2. **Uses flexible matching** (CONTAINS, case-insensitive)
3. **Finds variations** of search terms
4. **Builds inclusive queries** that capture related data

### Async Error Handling

- Targeted suppression of async cleanup errors
- Graceful degradation when servers are unavailable
- Automatic reconnection attempts

### Schema Compatibility

- Automatic fixing of OpenAI function calling issues
- Support for complex nested schemas
- Validation and error reporting

## 📈 Performance Optimization

- **Connection Pooling**: Reuses MCP connections
- **Schema Caching**: Avoids repeated schema validation
- **Streaming Responses**: Real-time user feedback
- **Targeted Cleanup**: Minimal async overhead

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🙏 Acknowledgments

- **Anthropic** for the Model Context Protocol
- **Chainlit** for the conversational AI framework
- **Neo4j** for graph database technology
- **HubSpot** for CRM integration capabilities

---

*This application demonstrates the power of connecting AI assistants to real-world data sources through standardized protocols, enabling sophisticated data analysis through natural language conversations.*