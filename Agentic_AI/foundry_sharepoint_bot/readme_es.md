> **Importante (versión preliminar)**: Los elementos marcados como "preview" se proporcionan sin SLA y no se recomiendan para producción. Consulta los [Términos de uso complementarios para las versiones preliminares de Microsoft Azure](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

# Agente con base en SharePoint en Azure AI Foundry

Interfaz de chat con Streamlit que conversa con un Azure AI Foundry Agent con base en la herramienta de Microsoft SharePoint. El agente reutiliza la misma conexión de SharePoint, respeta la identidad del usuario a través de la herramienta de SharePoint y transmite respuestas con citas a tu contenido de SharePoint.

> **Notas**
> - Este proyecto usa la herramienta de Microsoft SharePoint para Foundry Agent Service. Para documentación de producto de SharePoint, consulta la [documentación de SharePoint](https://learn.microsoft.com/en-us/sharepoint/).
> - Consulta las [mejores prácticas de herramientas de Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/tool-best-practice) para orientación de optimización.

## Características

- Experiencia de chat con Streamlit y respuestas en streaming desde el agente.
- Base en SharePoint mediante la herramienta de SharePoint de Foundry (preview) con seguridad de identidad passthrough (On-Behalf-Of).
- Reutiliza un agente existente por nombre; solo se crea si falta para evitar versiones duplicadas.
- Autenticación interactiva con Azure Identity y caché de tokens para reducir avisos repetidos.

## Arquitectura

- **Tiempo de ejecución del agente**: Azure AI Foundry Agent Service con `PromptAgentDefinition`.
- **Herramientas**: `SharepointAgentTool` con `SharepointGroundingToolParameters` y `ToolProjectConnection` apuntando a tu conexión de SharePoint.
- **Identidad**: `InteractiveBrowserCredential` con caché de token; la herramienta de SharePoint aplica la licencia de Microsoft 365 Copilot y las ACLs del sitio.
- **UI**: Aplicación de Streamlit en main_2.py.

## Requisitos previos

- Python 3.9+
- Proyecto de Azure AI Foundry con un despliegue de modelo de chat (por ejemplo, `gpt-4o-mini`).
- Conexión de herramienta de SharePoint creada en el portal de Foundry (mismo tenant que los usuarios).
- Licencias/roles:
  - Licencia de Microsoft 365 Copilot para desarrolladores y usuarios finales (requerida por el backend de la herramienta de SharePoint).
  - Rol RBAC `Azure AI User` (o superior) en el proyecto de Foundry. Consulta [RBAC en Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-foundry).
  - Acceso de lectura al sitio/carpeta de SharePoint de destino.
- Paquetes: `pip install -r requirements.txt` (instala `azure-ai-projects`, `azure-identity`, `python-dotenv`, `streamlit`).

## Configuración

Crea un archivo `.env` en la raíz del repositorio:

```
AZURE_AI_PROJECT_ENDPOINT=https://<tu-proyecto>.services.ai.azure.com
AZURE_AI_MODEL_DEPLOYMENT_NAME=<tu-despliegue-de-modelo>
SHAREPOINT_PROJECT_CONNECTION_NAME=<tu-nombre-de-conexion-sharepoint>

# Opcionales
SHAREPOINT_AGENT_NAME=sharepoint-cli-agent
AZURE_TENANT_ID=<tenant-id>  # mantiene la autenticación en el tenant correcto; útil con múltiples tenants
```

> La herramienta de SharePoint solo admite autenticación con identidad de usuario (no servicio). Asegúrate de que tu sitio de SharePoint y el proyecto de Foundry estén en el mismo tenant.

## Ejecutar la UI de chat

```powershell
pip install -r requirements.txt
streamlit run main_2.py
```

1. En la primera ejecución aparecerá un aviso de navegador interactivo. Inicia sesión con un usuario que tenga licencia de M365 Copilot y acceso a SharePoint. El token se almacena en caché para reducir avisos posteriores.
2. La aplicación reutiliza un agente existente llamado `SHAREPOINT_AGENT_NAME`. Si no se encuentra, crea uno con la herramienta de SharePoint vinculada a tu conexión.
3. Formula preguntas sobre tus documentos de SharePoint; las respuestas se transmiten en streaming con citas cuando están disponibles.

## Cómo funciona

1. **Auth**: `InteractiveBrowserCredential` obtiene un token y lo almacena en caché. La herramienta de SharePoint realiza OBO para aplicar permisos de usuario.
2. **Búsqueda de agente**: `project_client.agents.list()` verifica `SHAREPOINT_AGENT_NAME`; la creación solo sucede si falta.
3. **Enlace de herramientas**: `SharepointAgentTool` se configura con tu `ToolProjectConnection` para que las respuestas puedan recuperar contenido de SharePoint.
4. **Bucle de chat**: `st.chat_input` de Streamlit recopila los prompts; las respuestas se transmiten vía `openai_client.responses.create(stream=True, agent_reference)`.

## Autenticación On-Behalf-Of (OBO)

- Propósito: La herramienta de SharePoint intercambia el token de usuario de `InteractiveBrowserCredential` por un token delegado de SharePoint para que las ACLs del sitio y la licencia de Microsoft 365 Copilot se apliquen por usuario.
- Flujo: El usuario inicia sesión una vez; Foundry recibe el token de usuario; la herramienta de SharePoint ejecuta el intercambio OAuth2 OBO antes de llamar a SharePoint para que las llamadas posteriores se ejecuten con ese mismo usuario.
- Requisitos: El proyecto de Foundry y el sitio de SharePoint deben estar en el mismo tenant; OBO no admite tokens solo de aplicación (app-only). Configurar `AZURE_TENANT_ID` mantiene el inicio de sesión en el directorio correcto y estabiliza la caché de tokens.
- Modos de falla: Inicio de sesión entre tenants, falta de licencia de Copilot o caché de tokens borrada pueden mostrar `AppOnly OBO tokens not supported` o `invalid_grant`; resuelve iniciando sesión con un usuario con licencia en el tenant correcto y manteniendo la caché disponible.

## Archivos clave

- main_2.py: UI de Streamlit, caché de credenciales, reutilización/creación del agente, chat en streaming.
- requirements.txt: Dependencias de Python.
- schema.json: Presente pero no usado en este flujo centrado en SharePoint.

## Solución de problemas

- **Avisos de navegador repetidos**: Ejecuta la app con el mismo perfil de usuario para reutilizar la caché de tokens. Confirma que `allow_unencrypted_storage=True` es aceptable en tu entorno; en hosts restringidos quizá necesites almacenamiento de credenciales del SO.
- **AuthenticationError / AppOnly OBO tokens not supported**: La herramienta de SharePoint requiere identidad de usuario. Inicia sesión con una cuenta de usuario; no uses credenciales solo de aplicación.
- **Forbidden – User does not have valid license**: El usuario necesita una licencia de Microsoft 365 Copilot. Consulta las [notas de licenciamiento de la API de Microsoft 365 Copilot](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/api-reference/retrieval-api-overview).
- **Connection not found**: Verifica que `SHAREPOINT_PROJECT_CONNECTION_NAME` coincida con la conexión en el portal de Foundry y que apunte al `site_url` correcto.
- **Agent name invalid**: Los nombres deben iniciar y terminar con caracteres alfanuméricos, pueden incluir guiones y tener <=63 caracteres. Ajusta `SHAREPOINT_AGENT_NAME` en consecuencia.

## Consejos operativos

- Comienza con sitios/carpetas pequeñas y documentos cortos para recuperaciones más rápidas.
- Mantén el nombre del agente estable para reutilizar versiones en lugar de crear muchas.
- Si rotas tenants, define `AZURE_TENANT_ID` para evitar avisos hacia el directorio incorrecto.

## Referencias

- Mejores prácticas de herramientas de Foundry: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/tool-best-practice
- RBAC para Foundry: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-foundry
- Flujo OAuth2 On-Behalf-Of: https://learn.microsoft.com/azure/active-directory/develop/v2-oauth2-on-behalf-of-flow
- Microsoft 365 Copilot retrieval API: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/api-reference/retrieval-api-overview
- Semantic indexing for Copilot: https://learn.microsoft.com/en-us/microsoftsearch/semantic-index-for-copilot
