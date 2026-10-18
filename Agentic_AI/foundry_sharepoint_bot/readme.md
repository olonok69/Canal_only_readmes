> **Important (preview)**: Items marked as preview are provided without an SLA and are not recommended for production. See the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

# SharePoint-Grounded Agent on Azure AI Foundry

Streamlit chat UI that talks to an Azure AI Foundry Agent grounded with the Microsoft SharePoint tool. The agent reuses the same SharePoint connection, honors user identity via the SharePoint tool, and streams answers with citations to your SharePoint content.

> **Notes**
> - This project uses the Microsoft SharePoint tool for Foundry Agent Service. For SharePoint product docs, see the [SharePoint documentation](https://learn.microsoft.com/en-us/sharepoint/).
> - See Foundry tool [best practices](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/tool-best-practice) for optimization guidance.

## Features

- Streamlit chat experience with streaming responses from the agent.
- SharePoint grounding via the Foundry SharePoint tool (preview) with identity passthrough (On-Behalf-Of) security.
- Reuse existing agent by name; create only if missing to avoid duplicate versions.
- Interactive authentication using Azure Identity with token caching to reduce repeated prompts.

## Architecture

- **Agent runtime**: Azure AI Foundry Agent Service with `PromptAgentDefinition`.
- **Tooling**: `SharepointAgentTool` with `SharepointGroundingToolParameters` and `ToolProjectConnection` targeting your SharePoint connection.
- **Identity**: `InteractiveBrowserCredential` with token cache; SharePoint tool enforces Microsoft 365 Copilot license and site ACLs.
- **UI**: Streamlit app in main_2.py.

## Prerequisites

- Python 3.9+
- Azure AI Foundry project with a chat model deployment (for example, `gpt-4o-mini`).
- SharePoint tool connection created in the Foundry portal (same tenant as users).
- Licenses/roles:
  - Microsoft 365 Copilot license for developers and end users (required by the SharePoint tool backend).
  - `Azure AI User` RBAC role (or higher) on the Foundry project. See [RBAC in Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-foundry).
  - Read access to the target SharePoint site/folder.
- Packages: `pip install -r requirements.txt` (installs `azure-ai-projects`, `azure-identity`, `python-dotenv`, `streamlit`).

## Configuration

Create a `.env` file in the repo root:

```
AZURE_AI_PROJECT_ENDPOINT=https://<your-project>.services.ai.azure.com
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment>
SHAREPOINT_PROJECT_CONNECTION_NAME=<your-sharepoint-connection-name>

# Optional overrides
SHAREPOINT_AGENT_NAME=sharepoint-cli-agent
AZURE_TENANT_ID=<tenant-id>  # keeps auth scoped; helpful when multiple tenants
```

> The SharePoint tool only supports user-identity auth (no service principal). Ensure your SharePoint site and Foundry project are in the same tenant.

## Run the chat UI

```powershell
pip install -r requirements.txt
streamlit run main_2.py
```

1. On first run, an interactive browser prompt appears. Sign in with a user that has M365 Copilot license and SharePoint access. The token is cached to reduce further prompts.
2. The app reuses an existing agent named `SHAREPOINT_AGENT_NAME`. If not found, it creates one with the SharePoint tool bound to your connection.
3. Ask questions about your SharePoint documents; responses stream in with citations when available.

## How it works

1. **Auth**: `InteractiveBrowserCredential` acquires a token and caches it. The SharePoint tool performs OBO to enforce user permissions.
2. **Agent lookup**: `project_client.agents.list()` checks for `SHAREPOINT_AGENT_NAME`; creation happens only if missing.
3. **Tool wiring**: `SharepointAgentTool` is configured with your `ToolProjectConnection` so responses can retrieve SharePoint content.
4. **Chat loop**: Streamlit `st.chat_input` gathers prompts; responses are streamed via `openai_client.responses.create(stream=True, agent_reference)`.

## On-Behalf-Of (OBO) authentication

- Purpose: The SharePoint tool exchanges the user token from `InteractiveBrowserCredential` for a delegated SharePoint token so site ACLs and Microsoft 365 Copilot licensing are enforced per user.
- Flow: User signs in once; Foundry receives the user token; the SharePoint tool performs the OAuth2 OBO exchange before calling SharePoint so downstream calls run under that same user.
- Requirements: Foundry project and SharePoint site must be in the same tenant; OBO does not support app-only tokens. Setting `AZURE_TENANT_ID` keeps sign-in scoped to the right directory and stabilizes the token cache.
- Failure modes: Cross-tenant sign-in, missing Copilot license, or cleared token cache can surface `AppOnly OBO tokens not supported` or `invalid_grant`; resolve by signing in with a licensed user in the correct tenant and keeping the cache available.

## Key files

- main_2.py: Streamlit UI, credential caching, agent reuse/creation, streaming chat.
- requirements.txt: Python dependencies.
- schema.json: Present but unused by this SharePoint-focused flow.

## Troubleshooting

- **Repeated browser prompts**: Ensure the app runs under the same user profile so the token cache is reused. Confirm `allow_unencrypted_storage=True` is acceptable in your environment; on locked-down hosts you may need OS credential storage.
- **AuthenticationError / AppOnly OBO tokens not supported**: The SharePoint tool requires user identity. Sign in with a user account; do not use app-only credentials.
- **Forbidden – User does not have valid license**: The user needs a Microsoft 365 Copilot license. See the [Microsoft 365 Copilot API licensing notes](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/api-reference/retrieval-api-overview).
- **Connection not found**: Verify `SHAREPOINT_PROJECT_CONNECTION_NAME` matches the connection in the Foundry portal and that the connection targets the correct `site_url`.
- **Agent name invalid**: Names must start/end alphanumeric, may include hyphens, and be <=63 chars. Adjust `SHAREPOINT_AGENT_NAME` accordingly.

## Operational tips

- Start with smaller sites/folders and short documents for faster retrieval.
- Keep the agent name stable so you reuse versions instead of creating many.
- If you rotate tenants, set `AZURE_TENANT_ID` to avoid being prompted for the wrong directory.

## References

- Foundry tool best practices: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/tool-best-practice
- RBAC for Foundry: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-foundry
- OAuth2 On-Behalf-Of flow: https://learn.microsoft.com/azure/active-directory/develop/v2-oauth2-on-behalf-of-flow
- Microsoft 365 Copilot retrieval API: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/api-reference/retrieval-api-overview
- Semantic indexing for Copilot: https://learn.microsoft.com/en-us/microsoftsearch/semantic-index-for-copilot
