# Direct Line Copilot Client

Chat with your Copilot agent over Azure Bot Service Direct Line via either a web UI (Django) or a simple CLI script.


## Architecture
![Direct Line + Graph Retrieval Architecture](docs/architecture.svg)

### Core technologies (Direct Line path)
- Microsoft Copilot Studio: agent authored and published here; the Direct Line channel surfaces that agent to custom clients. Docs: https://learn.microsoft.com/microsoft-copilot-studio/
- Azure Bot Service + Bot Framework: hosts the bot registration and channels. Docs: https://learn.microsoft.com/azure/bot-service/
- Direct Line channel: REST transport the web UI and CLI use; tokens minted server-side with the Direct Line secret. Docs: https://learn.microsoft.com/azure/bot-service/bot-service-channel-directline
- Django: lightweight server to host the UI, expose the token endpoint, and serve static templates. Docs: https://docs.djangoproject.com/en/5.0/
- httpx: server-side HTTP client used to call Direct Line `tokens/generate`. Docs: https://www.python-httpx.org/

### How the Direct Line app works (end to end)
- Entry point: the root path `/` renders the chat UI from [copilot_agent/templates/directline_frontend.html](copilot_agent/templates/directline_frontend.html). The template injects `DIRECT_LINE_BASE_URL` from settings so the browser knows which Direct Line region to hit.
- Token minting: on load, the page calls `/api/directline/token/` (Django view in [directline_token_endpoint.py](directline_token_endpoint.py)). That view exchanges the server-held `DIRECT_LINE_SECRET` for a short-lived Direct Line token via `POST {DIRECT_LINE_BASE_URL}/v3/directline/tokens/generate` using `httpx`. The secret never leaves the server.
- Conversation start: the browser posts to `{DIRECT_LINE_BASE_URL}/v3/directline/conversations` with the token to obtain `conversationId`. It logs the conversation ID to the UI so you can correlate with Bot Service logs.
- Messaging: outbound messages go to `/v3/directline/conversations/{conversationId}/activities` with the same bearer token. The JS app tags the sender as `user1` so it can filter out its own echoes when rendering.
- Polling and watermarking: the browser polls `/activities` every ~1.2s using the last watermark to avoid duplicates. Bot replies and attachments are rendered as chat bubbles. Minimal markdown is supported (bold and bullet lists).
- OAuth cards: if the bot sends an `application/vnd.microsoft.card.oauth` attachment, the UI surfaces the sign-in URL. After the user signs in and gets a magic code, they paste it back; the UI posts that code as the next message, completing the OAuth flow for the bot.
- Token lifetime: Direct Line tokens are short-lived (default ~30 minutes) but conversations remain valid longer. Reloading the page requests a fresh token and starts a new conversation.

### Authentication flow (Direct Line)
1) Server-side secret: you configure `DIRECT_LINE_SECRET` and optional `DIRECT_LINE_BASE_URL` in `.env`. Django settings expose only the base URL to the client; the secret is never sent to the browser.
2) Token exchange: [directline_token_endpoint.py](directline_token_endpoint.py) uses the secret to call the Direct Line `tokens/generate` endpoint and returns only `{ token, expires_in }` to the browser.
3) Client usage: the browser uses that token for all Direct Line REST calls (start conversation, send activities, poll activities). No Graph or app tokens are involved in this flow.
4) Bot-initiated OAuth: if your Copilot/agent triggers sign-in, it sends an OAuth card through Direct Line. The UI instructs the user to complete the auth in a new tab and paste the magic code, which the bot validates to finish the delegated auth.

### Component responsibilities (see docs/architecture.svg)
- Presentation: [copilot_agent/templates/directline_frontend.html](copilot_agent/templates/directline_frontend.html) holds the single-page UI and all Direct Line client logic (token fetch, conversation start, send, poll, OAuth card handling).
- API surface: [copilot_agent/urls.py](copilot_agent/urls.py) maps `/` to the chat UI and `/api/directline/token/` to the token view. Graph endpoints are also registered here but operate independently of Direct Line.
- Token service: [directline_token_endpoint.py](directline_token_endpoint.py) is the only place the Direct Line secret is used. It mints ephemeral tokens and returns JSON; failures include the upstream response body for diagnostics.
- CLI alternative: [directline_bot.py](directline_bot.py) reproduces the same sequence (token → conversation → send → poll) for local testing without the web UI. It also handles OAuth cards by prompting for the magic code.
- Django hosting: [manage.py](manage.py) runs the dev server; [copilot_agent/settings.py](copilot_agent/settings.py) wires env vars such as `DIRECT_LINE_BASE_URL` and template search paths.

## Components (key files)
- Web server (Django): [manage.py](manage.py), [copilot_agent/settings.py](copilot_agent/settings.py), [copilot_agent/urls.py](copilot_agent/urls.py), token view [directline_token_endpoint.py](directline_token_endpoint.py), UI template [copilot_agent/templates/directline_frontend.html](copilot_agent/templates/directline_frontend.html).
- Graph retrieval API/UI: [graph_retrieval_endpoint.py](graph_retrieval_endpoint.py), template [copilot_agent/templates/graph_frontend.html](copilot_agent/templates/graph_frontend.html) at `/graph`.
- CLI chat: [directline_bot.py](directline_bot.py).
- Sample env: [.env.example](.env.example) (copy to `.env`).

## Requirements
- Python 3.9+ recommended.
- Direct Line secret from your Azure Bot Service > Channels > Direct Line
- If your agent/tool uses OAuth, have your Entra app registration (client id/secret, tenant) ready
- For Graph retrieval UI: service principal with client secret and consented Graph scopes (see API permissions screenshot); supports multiple scopes via `GRAPH_SCOPES`.

## Cloud setup (Azure + Copilot Studio)
1) Entra ID app registration (for your tool’s OAuth connection)
- App type: single-tenant Web app.
- Redirect: `https://<region>.token.botframework.com/.auth/web/redirect` (match your Direct Line region; e.g., Europe → `https://europe.token.botframework.com/.auth/web/redirect`).
- Permissions: delegated `openid profile offline_access` + your API scopes (e.g., `api://<api-client-id>/.default`).
- Create a client secret; keep tenant id, client id, client secret.

2) Azure Bot Service
- Create Bot Channels Registration, paste the same app’s client id, pick your region.

3) Enable Direct Line channel
- In the Bot resource > Channels > Direct Line > Configure > Add. Copy the Direct Line secret (this is `DIRECT_LINE_SECRET`). If you use a regional endpoint, note it (e.g., `https://europe.directline.botframework.com`).

4) Copilot Studio channel + tool connection
- In Copilot Studio, connect the bot channel to the Bot Service you created and publish your agent.
- For tools that need OAuth: set an OAuth connection using your Entra app. Match the Microsoft guidance https://learn.microsoft.com/en-us/microsoft-copilot-studio/configure-web-security and the screenshot configuration:
	- Authentication option: **Authenticate manually** (require users to sign in if you want auth on every chat).
	- Redirect URL: `https://<region>.token.botframework.com/.auth/web/redirect` (e.g., Europe region as shown in the screenshot).
	- Service provider: **Microsoft Entra ID V2 with client secrets**.
	- Client ID / Client secret: from your Entra app registration.
	- Token exchange URL (token endpoint): `https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token`.
	- Tenant ID: your directory ID.
	- Scopes: at minimum `openid profile offline_access` plus any API scopes your backend requires (e.g., `api://<api-client-id>/.default`).
- Ensure the connection shows **Connected**, then republish your agent.

Screenshot example (Copilot Studio auth config):
![Copilot Studio auth settings](docs/Securiry_copilot_auth.png)

## Install
```bash
pip install -r requirements.txt
```

## Configure
1) Copy env template and fill values:
```bash
cp .env.example .env
# edit .env
```
Required keys:
- `DIRECT_LINE_SECRET` (Direct Line secret; same as WEB_CHANNEL_TOKEN in portal)
- `DIRECT_LINE_BASE_URL` (region, e.g., https://europe.directline.botframework.com)
Graph retrieval keys (app-only):
- `TENANT_ID`, `CLIENT_ID_2` (or `CLIENT_ID`), `CLIENT_SECRET`
- `GRAPH_SCOPES` (space-separated; default `https://graph.microsoft.com/.default` — required for client credentials)
- `COPILOT_DATA_SOURCE` (optional; default `SharePoint`)
Optional if your bot/tool needs them: `TENANT_ID`, `CLIENT_ID`, `CLIENT_SECRET`, etc.

2) (If rotating secrets) do not commit `.env`. Prefer `env` vars in your shell or secret store.

## Run the web chat (recommended)
```bash
python manage.py migrate   # first run only, optional for admin/auth
python manage.py runserver
```
Then open http://127.0.0.1:8000/

What happens:
- Frontend renders from [copilot_agent/templates/directline_frontend.html](copilot_agent/templates/directline_frontend.html) and calls `/api/directline/token/`.
- Token endpoint [directline_token_endpoint.py](directline_token_endpoint.py) uses `DIRECT_LINE_SECRET` to mint a short-lived Direct Line token.
- The page starts a conversation against `DIRECT_LINE_BASE_URL` and streams messages.

## Run the Graph retrieval UI
```bash
python manage.py runserver
```
Open http://127.0.0.1:8000/graph/ and submit a query. The backend at `/api/graph/retrieval/` uses app credentials to call the Microsoft Graph Copilot retrieval API. Ensure your service principal has consented scopes (per screenshot in docs/Securiry_copilot_auth.png and API permissions) and that `TENANT_ID`, `CLIENT_ID_2`/`CLIENT_ID`, `CLIENT_SECRET`, and `GRAPH_SCOPES` (use `.default`) are set.

## Run the CLI chat (alternative)
```bash
python directline_bot.py
```
Type to chat; `exit` to quit.

## OAuth cards (magic code)
If the bot sends an OAuth card, open the sign-in link, complete login, copy the magic code shown, and send it back as the next message.

## Troubleshooting
- **Template not found**: ensure `copilot_agent/templates/directline_frontend.html` exists; settings include that path.
- **Token fetch fails**: confirm `DIRECT_LINE_SECRET` is set and valid; region matches `DIRECT_LINE_BASE_URL`.
- **Graph retrieval fails**: ensure `TENANT_ID`, `CLIENT_ID`/`CLIENT_ID_2`, `CLIENT_SECRET`, and `GRAPH_SCOPES` are set; for client credentials use `.default` (e.g., `https://graph.microsoft.com/.default`) and verify the app has the needed Graph app permissions consented.
 - If you see `AADSTS1002012` / scope invalid for client creds: use `.default` scope and grant application permissions with admin consent.
 - If you see `Unauthorized` with `.default`: ensure the service principal has Application permissions for the resources you query (e.g., Files.Read.All, Sites.Read.All) and admin consent is granted; Copilot delegated scopes do not work with client credentials.
- **No replies**: verify the agent is published and Direct Line is enabled; check network/console errors.
- **Migrations warning**: optional for this sample; run `python manage.py migrate` if you need admin/auth models.

## Security
- Never commit `.env` or secrets.
- Rotate Direct Line secrets regularly.
- Use a production-grade server (gunicorn/uvicorn + reverse proxy) for real deployments.
<parameter name="filePath">d:\repos3\copilot_client\README.md