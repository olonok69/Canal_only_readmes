# Copilot Client - Complete Integration Demo

A comprehensive Django-based demo showcasing four different ways to integrate with Microsoft Copilot Studio agents and Microsoft Graph semantic search:

- **Agent SDK Interactive** (`/agentsdk/`): Direct SDK calls with delegated authentication
- **Direct Line Webchat** (`/directline/`): Azure Bot Service channel with web UI
- **Graph Retrieval** (`/graph/`): Semantic search across Microsoft 365 content
- **Embed Webchat** (`/embed/`): Simple iframe embedding of Copilot Studio web chat

## Architecture Overview

![Complete Copilot Client Architecture](docs/architecture.svg)

**Color-coded flows:**
- 🔵 **Blue**: Agent SDK Direct Call - Direct connection to Copilot Studio
- 🔴 **Red**: Direct Line Channel - Through Azure Bot Service
- 🟢 **Green**: Semantic Search Graph - Microsoft Graph Copilot Retrieval API
- 🟠 **Orange**: Embed Webchat - Direct Copilot Studio iframe

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your credentials

# Run the server
python manage.py runserver

# Access the interfaces:
# - Agent SDK: http://127.0.0.1:8000/agentsdk/
# - Direct Line: http://127.0.0.1:8000/directline/
# - Graph Search: http://127.0.0.1:8000/graph/
# - Embed Chat: http://127.0.0.1:8000/embed/
```

## 1. Agent SDK Interactive (`/agentsdk/`)

Direct integration using Copilot Studio SDK with delegated authentication via MSAL.js.

### Technologies
- **Microsoft Copilot Studio SDK**: Direct API calls to Copilot Studio agents
- **MSAL.js**: Browser-based delegated authentication (auth code + PKCE)
- **Django backend**: Server-side SDK integration

### How it works
- Browser authenticates via MSAL.js with Power Platform scopes
- Django backend receives tokens and makes direct SDK calls to Copilot Studio
- Real-time conversation streaming without Azure Bot Service

### Authentication Flow
1. **Browser auth**: MSAL.js redirects to Microsoft login with `https://api.powerplatform.com/CopilotStudio.Copilots.Invoke` scope
2. **Token exchange**: Django backend receives authorization code, exchanges for access token
3. **SDK calls**: Direct connection to Copilot Studio agent API
4. **Conversation**: Messages sent/received via SDK without intermediaries

### Configuration
See [docs/agentsdk-interactive.md](docs/agentsdk-interactive.md) for detailed setup including:
- Entra app registration requirements
- Power Platform API permissions
- Environment variables (`M365_*` prefixed)

### Files
- Frontend: [copilot_agent/templates/agentsdk_frontend.html](copilot_agent/templates/agentsdk_frontend.html)
- Backend: [agentsdk_console_test.py](agentsdk_console_test.py) (SDK logic)
- Docs: [docs/agentsdk-interactive.md](docs/agentsdk-interactive.md)

## 2. Direct Line Webchat (`/directline/`)

Traditional Azure Bot Service integration using Direct Line channel.

### Technologies
- **Azure Bot Service**: Hosts the bot registration and channels
- **Direct Line Channel**: REST transport for custom clients
- **Django**: Token minting and UI hosting

### How it works
- Server-side token generation using Direct Line secret
- Browser establishes conversation via Direct Line REST API
- Real-time polling for messages and bot responses
- OAuth card support for delegated authentication

### Authentication Flow
1. **Server-side secret**: Django holds `DIRECT_LINE_SECRET` securely
2. **Token minting**: `/api/directline/token/` exchanges secret for short-lived tokens
3. **Client usage**: Browser uses token for all Direct Line API calls
4. **Bot OAuth**: If agent requires auth, OAuth cards trigger user sign-in flow

### Configuration
See [docs/directline-webchat.md](docs/directline-webchat.md) for setup including:
- Azure Bot Service configuration
- Direct Line channel setup
- Environment variables (`DIRECT_LINE_*` prefixed)

### Files
- Frontend: [copilot_agent/templates/directline_frontend.html](copilot_agent/templates/directline_frontend.html)
- Token service: [directline_token_endpoint.py](directline_token_endpoint.py)
- CLI alternative: [directline_bot.py](directline_bot.py)
- Docs: [docs/directline-webchat.md](docs/directline-webchat.md)

## 3. Graph Retrieval (`/graph/`)

Semantic search across Microsoft 365 content using Microsoft Graph Copilot Retrieval API.

### Technologies
- **Microsoft Graph Copilot Retrieval API**: AI-powered content discovery
- **MSAL.js**: Delegated authentication for Microsoft Graph
- **M365 Copilot SDK**: Beta SDK for Graph integration

### How it works
- Browser authenticates with Microsoft Graph scopes
- Users select data sources (SharePoint, OneDrive, Outlook, etc.)
- Natural language queries processed by Copilot Retrieval API
- Results displayed as formatted cards with extracts and URLs

### Authentication Flow
1. **Browser auth**: MSAL.js with Graph scopes (`CopilotPackages.Read.All`, `Sites.ReadWrite.All`, etc.)
2. **Token delegation**: Access tokens sent to Django backend
3. **API calls**: Backend uses M365 Copilot SDK to query Graph API
4. **Results**: Formatted response with content extracts and metadata

### Configuration
See [docs/graph-retrieval.md](docs/graph-retrieval.md) and [docs/graph-frontend.md](docs/graph-frontend.md) for:
- Microsoft 365 Copilot licensing requirements
- Graph API permissions and consent
- Environment variables (`TENANT_ID`, `CLIENT_ID_2`, `GRAPH_SCOPES`)

### Files
- Frontend: [copilot_agent/templates/graph_frontend.html](copilot_agent/templates/graph_frontend.html)
- Backend: [graph_retrieval_endpoint.py](graph_retrieval_endpoint.py)
- Docs: [docs/graph-retrieval.md](docs/graph-retrieval.md), [docs/graph-frontend.md](docs/graph-frontend.md)

## 4. Embed Webchat (`/embed/`)

Simple iframe integration using Copilot Studio's default web chat embed.

### Technologies
- **Copilot Studio Web Chat**: Default Microsoft-hosted embed
- **Django TemplateView**: Simple iframe hosting
- **Configurable URLs**: Support for custom embed endpoints

### How it works
- Django serves a simple HTML page with iframe
- Iframe loads Copilot Studio's default web chat interface
- No custom authentication or backend processing required
- Direct connection to Copilot Studio's hosted chat

### Configuration
See [docs/embed-webchat.md](docs/embed-webchat.md) for:
- Default embed URL configuration
- Custom embed URL overrides
- Environment variable (`M365_EMBED_URL`)

### Files
- Template: [copilot_agent/templates/embed_frontend.html](copilot_agent/templates/embed_frontend.html)
- Docs: [docs/embed-webchat.md](docs/embed-webchat.md)

## Core Technologies

### Authentication & Security
- **MSAL.js**: Browser-based OAuth 2.0 flows (auth code + PKCE)
- **Microsoft Entra ID**: Identity and access management
- **Direct Line Secrets**: Server-side token generation
- **App Registrations**: Separate apps for different integration types

### Backend Framework
- **Django**: Web framework with async views and template system
- **SDKs**: CopilotStudio SDK, M365Copilot SDK (beta)
- **HTTP Clients**: httpx for REST API calls

### Frontend Components
- **HTML/CSS/JavaScript**: Vanilla web components
- **MSAL.js integration**: Authentication handling
- **Real-time updates**: Polling and WebSocket alternatives
- **Responsive design**: Mobile-friendly interfaces

## Environment Configuration

Copy `.env.example` to `.env` and configure:

### For Agent SDK (`/agentsdk/`):
```bash
M365_CONNECTION_STRING=...
M365_ENVIRONMENT_ID=...
M365_TENANT_ID=...
M365_AGENT_APP_ID=...
M365_SCHEMA_NAME=...
M365_SCOPE=...
M365_SCOPE_PYTHON=...
```

### For Direct Line (`/directline/`):
```bash
DIRECT_LINE_SECRET=...
DIRECT_LINE_BASE_URL=...
```

### For Graph Retrieval (`/graph/`):
```bash
TENANT_ID=...
CLIENT_ID_2=...
GRAPH_SCOPES=...
COPILOT_DATA_SOURCE=...
```

### For Embed (`/embed/`):
```bash
M365_EMBED_URL=...  # Optional
```

## Cloud Setup Requirements

### Microsoft Entra ID App Registrations
- **Agent SDK app**: Power Platform API permissions, SPA redirect URIs
- **Graph app**: Microsoft Graph permissions, SPA redirect URIs
- **Direct Line app**: Bot Framework token exchange URLs

### Azure Resources
- **Azure Bot Service**: For Direct Line integrations
- **Copilot Studio**: Agent authoring and publishing
- **Microsoft 365**: For Graph retrieval (Copilot license required)

### Permissions & Consent
- **Delegated permissions**: For user-interactive flows
- **Application permissions**: For service-to-service calls
- **Admin consent**: Required for many Microsoft Graph scopes

## Installation & Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Database setup (optional)
python manage.py migrate

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials

# Start development server
python manage.py runserver
```

## Security Best Practices

- **Never commit `.env`** or secrets to version control
- **Rotate secrets regularly** (Direct Line, client secrets)
- **Use production servers** (gunicorn/uvicorn + nginx) for deployments
- **Implement proper CORS** policies for production
- **Monitor token usage** and implement rate limiting
- **Use Azure Key Vault** or similar for secret management

## Troubleshooting

### Common Issues

**Agent SDK Issues:**
- **Power Platform API not available**: Follow [docs/agentsdk-interactive.md](docs/agentsdk-interactive.md) to create service principal
- **Scope errors**: Ensure `CopilotStudio.Copilots.Invoke` permission granted

**Direct Line Issues:**
- **Token fetch fails**: Verify `DIRECT_LINE_SECRET` and region match
- **No replies**: Check agent is published and Direct Line enabled

**Graph Retrieval Issues:**
- **Authentication fails**: Check Graph scopes and admin consent
- **No results**: Verify M365 Copilot licensing and data source access

**General Issues:**
- **Template not found**: Ensure all template files exist
- **Network errors**: Check firewall and proxy settings
- **CORS issues**: Configure allowed origins in production

## Documentation References

- [Authentication & Security Guide](docs/authentication-guide.md)
- [Agent SDK Interactive Guide](docs/agentsdk-interactive.md)
- [Direct Line Webchat Setup](docs/directline-webchat.md)
- [Graph Retrieval Configuration](docs/graph-retrieval.md)
- [Graph Frontend Details](docs/graph-frontend.md)
- [Embed Webchat Setup](docs/embed-webchat.md)

## Architecture Diagram

The [docs/architecture.svg](docs/architecture.svg) provides a comprehensive visual overview of all integration patterns, authentication flows, and component relationships. The color-coded legend explains each architectural path and connection type.

---

*This demo showcases multiple integration approaches for Microsoft Copilot Studio and Graph APIs. Choose the pattern that best fits your security, scalability, and user experience requirements.*
<parameter name="filePath">d:\repos3\copilot_client\README.md