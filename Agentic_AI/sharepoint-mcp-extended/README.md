# SharePoint & Microsoft 365 Data Access - Complete Toolkit

A comprehensive repository showcasing **three distinct approaches** for accessing SharePoint and Microsoft 365 data through AI-powered agents and semantic search. Each method offers different trade-offs in terms of authentication, deployment complexity, licensing requirements, and capabilities.

---

## 🎯 Overview

This repository contains three production-ready solutions for integrating AI assistants with SharePoint and Microsoft 365:

| Approach | Best For | Authentication | Key Technology | Location |
|----------|----------|----------------|----------------|----------|
| **[MCP SharePoint](#1-mcp-sharepoint-agent)** | Local development, Claude Desktop, flexible tool integration | App-only (service principal) | Model Context Protocol + Microsoft Graph | [`mcp-sharepoint/`](mcp-sharepoint/) |
| **[Azure AI Foundry Agent](#2-azure-ai-foundry-sharepoint-agent)** | Production deployments, user-specific permissions | User identity (OBO) | Azure AI Foundry + SharePoint Tool | [`Foundry_sharepoint/`](Foundry_sharepoint/) |
| **[Graph Retrieval API](#3-microsoft-graph-semantic-search)** | Semantic search, content discovery, multi-source queries | Delegated (browser-based) | Microsoft Graph Copilot Retrieval API | [`copilot_client/`](copilot_client/) |

---

## 1. MCP SharePoint Agent

**Location:** [`mcp-sharepoint/`](mcp-sharepoint/) and root directory

A Model Context Protocol (MCP) server that exposes SharePoint data through standardized tools. Works with LlamaIndex agents and can be integrated with any MCP-compatible client (e.g., Claude Desktop, custom tools).

### Architecture

```
User ➜ (CLI / Streamlit) ➜ LlamaIndex FunctionAgent ➜ MemoryMCPClient ➜ MCP Server ➜ Microsoft Graph ➜ SharePoint
```

### Key Features

- **Universal MCP interface**: Standardized tools/resources compatible with any MCP client
- **App-only authentication**: Service principal (client credentials flow) for autonomous access
- **Conversation memory**: Remembers site, drive, folder context across multi-turn conversations
- **Dual UIs**: Interactive CLI (`llamaindex_bot.py`) and Streamlit web chat (`streamlit_app.py`)
- **Content extraction**: Automatic text preview for PDFs, Office documents, code files
- **Microsoft Search integration**: Semantic search across SharePoint sites

### MCP Tools Exposed

| Tool | Purpose |
|------|---------|
| `list_sites` | Enumerate SharePoint sites |
| `get_site_info` | Fetch metadata for a specific site |
| `list_site_drives` | List document libraries/drives |
| `list_drive_items` | Browse folders and files |
| `get_file_content` | Retrieve file contents with text extraction |
| `search_files` | Run Microsoft Graph search queries |

### Prerequisites

- **Python 3.9+**
- **Azure AD app registration** with client credentials flow
- **Application permissions**: `Sites.Read.All`, `Files.Read.All`
- **OpenAI API key** (or compatible LLM)

### Configuration

Create `.env` file:

```bash
# Microsoft Graph
SHAREPOINT_URL=https://contoso.sharepoint.com
TENANT_ID=00000000-0000-0000-0000-000000000000
CLIENT_ID=11111111-1111-1111-1111-111111111111
CLIENT_SECRET=super-secret
GRAPH_SEARCH_REGION=NAM  # NAM, EUR, CHE, GBR, APAC

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4.1-mini

# Optional defaults
MCP_DEFAULT_SITE_URL=https://contoso.sharepoint.com/sites/ProjectX
```

### Quick Start

```powershell
# Install dependencies
pip install -r requirements.txt

# Run CLI agent
python llamaindex_bot.py --backend graph

# Or run Streamlit UI
streamlit run streamlit_app.py
```

### Use Cases

- **Local AI workflows**: Integrate SharePoint access into your desktop AI tools
- **Claude Desktop integration**: Register as an MCP server for Claude
- **Custom automations**: Build scripts that reason about SharePoint content
- **Development & testing**: Quick prototyping without cloud deployment

### Documentation

- Full guide: [`README.md`](README.md) (detailed MCP setup)
- Search capabilities: [`docs/SEMANTIC_SEARCH.md`](docs/SEMANTIC_SEARCH.md)
- Technical overview: [`docs/TECHNICAL_OVERVIEW.md`](docs/TECHNICAL_OVERVIEW.md)

---

## 2. Azure AI Foundry SharePoint Agent

**Location:** [`Foundry_sharepoint/`](Foundry_sharepoint/)

A production-ready Streamlit chat UI connected to Azure AI Foundry Agent Service with the official **SharePoint tool** (preview). Enforces user-specific permissions via On-Behalf-Of (OBO) authentication.

### Architecture

```
User ➜ Browser ➜ Streamlit ➜ Azure AI Foundry Agent ➜ SharePoint Tool (OBO) ➜ SharePoint
```

### Key Features

- **User identity passthrough**: SharePoint tool honors per-user permissions (OBO flow)
- **Microsoft 365 Copilot integration**: Leverages semantic indexing and licensed features
- **Azure-hosted agent**: Managed runtime in Azure AI Foundry with versioning
- **Streaming responses**: Real-time chat with citations to SharePoint content
- **Token caching**: Reduces authentication prompts with persistent token storage
- **Agent reuse**: Connects to existing agents by name to avoid version sprawl

### Prerequisites

- **Python 3.9+**
- **Azure AI Foundry project** with chat model deployment (e.g., `gpt-4o-mini`)
- **SharePoint tool connection** created in Foundry portal
- **Licenses/roles**:
  - Microsoft 365 Copilot license (required for developers and end users)
  - `Azure AI User` RBAC role on Foundry project
  - SharePoint site read access
- **Same tenant**: Foundry project and SharePoint must be in the same Azure AD tenant

### Configuration

Create `.env` file in [`Foundry_sharepoint/`](Foundry_sharepoint/):

```bash
AZURE_AI_PROJECT_ENDPOINT=https://<your-project>.services.ai.azure.com
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o-mini
SHAREPOINT_PROJECT_CONNECTION_NAME=<your-sharepoint-connection-name>

# Optional
SHAREPOINT_AGENT_NAME=sharepoint-cli-agent
AZURE_TENANT_ID=<tenant-id>  # Recommended for stable auth
```

### Quick Start

```powershell
cd Foundry_sharepoint
pip install -r requirements.txt
streamlit run main.py
```

1. Browser authentication prompt appears (first run)
2. Sign in with Microsoft 365 Copilot-licensed account
3. Agent reuses existing configuration or creates new one
4. Ask questions about SharePoint content

### On-Behalf-Of (OBO) Authentication

The SharePoint tool **enforces user permissions** at runtime:

- **Flow**: User signs in → Foundry receives token → SharePoint tool performs OBO exchange → Downstream calls run as that user
- **Benefits**: Each user sees only their authorized content; no over-privileged service account
- **Requirements**: 
  - User must have M365 Copilot license
  - Same tenant for Foundry and SharePoint
  - No support for app-only tokens

### Use Cases

- **Production deployments**: Enterprise-ready with Azure SLAs
- **Multi-user scenarios**: Per-user access control without complex ACL management
- **Copilot-enabled workflows**: Leverage Microsoft's semantic indexing
- **Compliance**: Honor existing SharePoint permissions automatically

### Documentation

- Full guide: [`Foundry_sharepoint/readme.md`](Foundry_sharepoint/readme.md)
- Azure portal setup: [`docs/AZURE_PORTAL_GUIDE.md`](docs/AZURE_PORTAL_GUIDE.md)
- Intra-ID auth troubleshooting: [`docs/INTRAID_AUTH_GUIDE.md`](docs/INTRAID_AUTH_GUIDE.md)

---

## 3. Microsoft Graph Semantic Search

**Location:** [`copilot_client/`](copilot_client/) (Graph Retrieval component)

A Django-based web interface for **semantic search** across Microsoft 365 content using the Microsoft Graph Copilot Retrieval API. Searches SharePoint, OneDrive, Outlook, and external data sources with natural language queries.

### Architecture

```
User ➜ Browser (MSAL.js) ➜ Django Backend ➜ Graph Copilot Retrieval API ➜ M365 Data Sources
```

### Key Features

- **Natural language search**: AI-powered content discovery across multiple data sources
- **Multi-source queries**: SharePoint, OneDrive (Business), Outlook, External/Web content
- **Browser-based auth**: MSAL.js delegated authentication (auth code + PKCE)
- **Rich result cards**: Formatted responses with text extracts, URLs, metadata
- **No agent required**: Direct API access for content discovery without conversation context
- **Real-time results**: Immediate search results without background processing

### Data Sources Supported

| Source | Description | Scope Required |
|--------|-------------|----------------|
| **SharePoint** | Site collections and libraries | `Sites.ReadWrite.All` |
| **OneDrive (Business)** | User OneDrive files | `Files.ReadWrite.All` |
| **Outlook** | Email and attachments | `Mail.Read` |
| **External/Web** | External connectors | `ExternalItem.Read.All` |

### Prerequisites

- **Python 3.9+**
- **Django** framework
- **Microsoft 365 Copilot license** (required for Retrieval API access)
- **Azure AD app registration** (Single-page application):
  - Redirect URI: `http://localhost:8000/graph/`
  - Delegated permissions: `CopilotPackages.Read.All`, `Sites.ReadWrite.All`, `Files.ReadWrite.All`, `ExternalItem.Read.All`
  - Admin consent granted

### Configuration

Add to `.env` in [`copilot_client/`](copilot_client/):

```bash
TENANT_ID=<your-tenant-id>
CLIENT_ID_2=<your-client-id>
GRAPH_SCOPES=https://graph.microsoft.com/CopilotPackages.Read.All https://graph.microsoft.com/Sites.ReadWrite.All https://graph.microsoft.com/Files.ReadWrite.All https://graph.microsoft.com/ExternalItem.Read.All

# Optional default data source
COPILOT_DATA_SOURCE=SharePoint  # SharePoint, OneDriveBusiness, ExternalItem
```

### Quick Start

```powershell
cd copilot_client
pip install -r requirements.txt
python manage.py runserver
```

Navigate to: `http://localhost:8000/graph/`

1. Click **Sign in** (MSAL.js authentication)
2. Select data source (SharePoint, Files, OneDrive, Web)
3. Enter natural language query (e.g., "latest project updates")
4. View results as formatted cards

### Use Cases

- **Content discovery**: Find documents across multiple M365 sources
- **Search-first workflows**: Quick answers without full conversation context
- **Document exploration**: Browse and preview content with URLs
- **Multi-tenant scenarios**: User-scoped search respecting permissions

### Documentation

- Graph Retrieval guide: [`copilot_client/docs/graph-retrieval.md`](copilot_client/docs/graph-retrieval.md)
- Frontend details: [`copilot_client/docs/graph-frontend.md`](copilot_client/docs/graph-frontend.md)
- Complete copilot client: [`copilot_client/README.md`](copilot_client/README.md)

---

## 🔍 Comparison Matrix

### Authentication & Security

| Feature | MCP SharePoint | Foundry Agent | Graph Retrieval |
|---------|----------------|---------------|-----------------|
| **Auth Type** | App-only (service principal) | User identity (OBO) | Delegated (browser) |
| **User Permissions** | Service account level | Per-user (enforced) | Per-user (enforced) |
| **Token Management** | Client credentials | Interactive + cache | MSAL.js + cache |
| **Cross-Tenant** | Yes | No (same tenant required) | No (same tenant required) |

### Licensing & Requirements

| Feature | MCP SharePoint | Foundry Agent | Graph Retrieval |
|---------|----------------|---------------|-----------------|
| **M365 Copilot License** | ❌ Not required | ✅ Required | ✅ Required |
| **Azure AI Foundry** | ❌ Not required | ✅ Required | ❌ Not required |
| **Graph API Permissions** | Application | None (via tool) | Delegated |
| **Admin Consent** | Required | Not required | Required |

### Deployment & Operations

| Feature | MCP SharePoint | Foundry Agent | Graph Retrieval |
|---------|----------------|---------------|-----------------|
| **Deployment** | Local/self-hosted | Azure cloud | Local/self-hosted |
| **Scalability** | Process-based | Azure-managed | App-server based |
| **Monitoring** | Custom logging | Azure AI metrics | Django logging |
| **Cost** | OpenAI API only | Foundry compute + model | Development only |

### Capabilities

| Feature | MCP SharePoint | Foundry Agent | Graph Retrieval |
|---------|----------------|---------------|-----------------|
| **Conversation Memory** | ✅ Multi-turn context | ✅ Agent-managed | ❌ Single queries |
| **Tool Calling** | ✅ Extensible MCP tools | ✅ SharePoint tool only | ❌ Direct API |
| **Content Extraction** | ✅ Text preview | ✅ Via SharePoint tool | ✅ Text extracts |
| **Citations** | ✅ URLs in responses | ✅ Citations included | ✅ Result cards with URLs |
| **Semantic Search** | ✅ Microsoft Search | ✅ Built-in | ✅ Copilot Retrieval API |
| **Multi-Source Search** | ❌ SharePoint only | ❌ SharePoint only | ✅ SharePoint + OneDrive + Outlook |

---

## 🚀 When to Use Each Approach

### Choose **MCP SharePoint** when:
- Building local AI workflows or desktop integrations
- Need flexible tool customization and extension
- Want to integrate with Claude Desktop or other MCP clients
- Development/testing scenarios without production deployment
- Service account access is acceptable (no per-user permissions needed)

### Choose **Azure AI Foundry Agent** when:
- Deploying to production with enterprise requirements
- Per-user permissions are critical (compliance, security)
- Users have Microsoft 365 Copilot licenses
- Want Azure-managed infrastructure with SLAs
- Need audit trails tied to user identities

### Choose **Graph Retrieval API** when:
- Primary use case is search/discovery (not conversation)
- Need to query across multiple M365 sources (SharePoint + OneDrive + Outlook)
- Want quick answers without agent overhead
- Building search-first experiences or exploratory UIs
- Users interact directly with browser-based authentication

---

## 📚 Common Prerequisites

All three approaches require:

- **Azure AD tenant** with appropriate licenses
- **SharePoint Online** access
- **Python 3.9+** development environment
- **Microsoft Entra app registration(s)** with proper permissions

### Shared Documentation

- **Technical Overview**: [`docs/TECHNICAL_OVERVIEW.md`](docs/TECHNICAL_OVERVIEW.md)
- **SharePoint Access Libraries**: [`docs/SHAREPOINT_ACCESS_LIBRARIES_COMPARISON.md`](docs/SHAREPOINT_ACCESS_LIBRARIES_COMPARISON.md)
- **Azure Portal Guide**: [`docs/AZURE_PORTAL_GUIDE.md`](docs/AZURE_PORTAL_GUIDE.md)
- **Authentication Guide**: [`docs/INTRAID_AUTH_GUIDE.md`](docs/INTRAID_AUTH_GUIDE.md)

---

## 🛠️ Installation (All Components)

```powershell
# Clone repository
git clone <repository-url>
cd sharepoint-mcp-extended

# Install MCP SharePoint components
pip install -r requirements.txt

# Install Foundry agent components
cd Foundry_sharepoint
pip install -r requirements.txt
cd ..

# Install Graph retrieval components
cd copilot_client
pip install -r requirements.txt
cd ..
```

---

## 🔐 Security Best Practices

1. **Never commit secrets**: Use `.env` files and `.gitignore`
2. **Rotate credentials**: Regularly update client secrets and API keys
3. **Least privilege**: Grant minimum required permissions for each approach
4. **Monitor usage**: Track API calls, token usage, and access patterns
5. **Production secrets**: Use Azure Key Vault or similar for production deployments
6. **HTTPS only**: Use secure connections for production web applications
7. **Token caching**: Implement secure token storage with encryption

---

## 🐛 Troubleshooting

### Common Issues Across All Approaches

**Authentication Failures:**
- Verify tenant IDs match between app registration and configuration
- Check permissions are granted and admin-consented
- Ensure redirect URIs match exactly (including protocol and port)

**Permission Errors:**
- Confirm user/service principal has required Graph API permissions
- Verify SharePoint site access for the authenticated identity
- Check Microsoft 365 Copilot license status (Foundry & Graph Retrieval)

**Token Issues:**
- Clear token cache and re-authenticate
- Verify scopes match the required API permissions
- Check token expiration and refresh token availability

**Network/Connectivity:**
- Confirm firewall allows Microsoft Graph endpoints
- Check proxy settings if behind corporate network
- Verify Azure region and endpoint URLs are correct

### Approach-Specific Troubleshooting

- **MCP SharePoint**: Check `GRAPH_SEARCH_REGION` matches tenant location
- **Foundry Agent**: Ensure same tenant for Foundry project and SharePoint
- **Graph Retrieval**: Use `localhost` (not `127.0.0.1`) for redirect URI

---

## 📖 Additional Resources

### Microsoft Documentation
- [Microsoft Graph API](https://learn.microsoft.com/en-us/graph/overview)
- [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Microsoft 365 Copilot Retrieval API](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/api-reference/retrieval-api-overview)
- [SharePoint Documentation](https://learn.microsoft.com/en-us/sharepoint/)
- [OAuth 2.0 On-Behalf-Of Flow](https://learn.microsoft.com/azure/active-directory/develop/v2-oauth2-on-behalf-of-flow)

### Framework Documentation
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [LlamaIndex](https://docs.llamaindex.ai/)
- [Streamlit](https://docs.streamlit.io/)
- [Django](https://docs.djangoproject.com/)
- [MSAL.js](https://learn.microsoft.com/azure/active-directory/develop/msal-overview)

---

## 📝 License

See individual component directories for licensing information.

---

## 🤝 Contributing

Contributions welcome! Each component has its own development guidelines:
- MCP SharePoint: See root [`README.md`](README.md)
- Foundry Agent: See [`Foundry_sharepoint/readme.md`](Foundry_sharepoint/readme.md)
- Graph Retrieval: See [`copilot_client/README.md`](copilot_client/README.md)

---

## 📞 Support

For issues specific to each approach:
- **MCP SharePoint**: Check [`mcp-sharepoint/`](mcp-sharepoint/) documentation
- **Foundry Agent**: See Azure AI Foundry docs and [`docs/AZURE_PORTAL_GUIDE.md`](docs/AZURE_PORTAL_GUIDE.md)
- **Graph Retrieval**: Refer to [`copilot_client/docs/`](copilot_client/docs/) guides

---

**Last Updated**: January 2026
