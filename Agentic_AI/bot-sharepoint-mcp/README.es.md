# SharePoint MCP Agent Toolkit (Versión en Español)

Este repositorio integra el servidor SharePoint Model Context Protocol (MCP) con un asistente basado en LlamaIndex y dos interfaces de usuario:

1. `llamaindex_bot.py` – bucle interactivo en CLI para flujos rápidos desde la terminal.
2. `streamlit_app.py` – interfaz Streamlit que presenta el mismo agente en un chat web.

Ambas experiencias usan el paquete `mcp-sharepoint`, el cual expone datos de SharePoint mediante herramientas MCP respaldadas por [Microsoft Graph](https://learn.microsoft.com/en-us/graph/overview).

---

## Resumen de Arquitectura

1. **Environment bootstrap** – Las variables definidas en `.env` (credenciales de Graph, clave de OpenAI, valores por defecto) se cargan con `python-dotenv`.
2. **MCP server launch** – El backend Graph (`mcp_sharepoint.graph_server`) se ejecuta como subproceso Python mediante stdio.
3. **MCP client** – `MemoryMCPClient` extiende `BasicMCPClient` para inyectar valores por defecto (site URL, drive ID, folder path, referencias de archivos).
4. **LlamaIndex FunctionAgent** – Planea las llamadas a herramientas MCP, las ejecuta y sintetiza respuestas en lenguaje natural.
5. **User interface** – CLI o Streamlit reenvían prompts y muestran respuestas mientras exponen la memoria de conversación actual.

```
Usuario ➜ (CLI / Streamlit) ➜ LlamaIndex FunctionAgent ➜ MemoryMCPClient ➜ MCP Server ➜ Microsoft Graph ➜ SharePoint
```

![Diagrama de arquitectura](docs/architecture.svg)

### Tecnologías

- **LlamaIndex FunctionAgent** – Orquesta el razonamiento y la invocación de herramientas.
- **Microsoft Graph** – API autorizada para datos y archivos de SharePoint.
- **Model Context Protocol** – Estandariza herramientas y recursos para que cualquier cliente MCP pueda operar el servidor.
- **Streamlit** – UI opcional en navegador construida sobre el mismo backend Python.

---

## Prerrequisitos y Configuración

### Aplicación de Microsoft Graph

1. Registra una aplicación Azure AD usando el flujo **client credentials**.
2. Otorga permisos de aplicación: `Sites.Read.All` y `Files.Read.All`.
3. Conserva los siguientes valores (consulta la [introducción a Graph](https://learn.microsoft.com/en-us/graph/overview) para más contexto):

| Variable        | Descripción                                             |
|-----------------|---------------------------------------------------------|
| `SHAREPOINT_URL`| Raíz del tenant, p.ej. `https://contoso.sharepoint.com` |
| `TENANT_ID`     | ID del directorio (tenant) de Azure AD                  |
| `CLIENT_ID`     | ID de la aplicación registrada                          |
| `CLIENT_SECRET` | Secreto cliente generado para la app                    |

### LLM de OpenAI (o compatible)

| Variable        | Descripción                                                         |
|-----------------|---------------------------------------------------------------------|
| `OPENAI_API_KEY`| Clave usada por LlamaIndex para invocar el modelo                   |
| `OPENAI_BASE_URL` *(opcional)* | URL base alternativa (Azure OpenAI, proxy propio, etc.) |
| `OPENAI_MODEL` *(opcional)*    | Por defecto `gpt-4.1-mini`                             |

### Valores opcionales para SharePoint

Las variables heredadas con prefijo `SHP_` pueden permanecer en `.env`; se ignoran cuando usas el backend Graph pero resultan útiles si reactivas CSOM.

### Ejemplo de `.env`

```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4.1-mini
SHAREPOINT_URL=https://contoso.sharepoint.com
TENANT_ID=00000000-0000-0000-0000-000000000000
CLIENT_ID=11111111-1111-1111-1111-111111111111
CLIENT_SECRET=super-secret
```

---

## Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Esto instala el servidor MCP de SharePoint en modo editable junto con LlamaIndex, Streamlit y librerías auxiliares.

---

## Agente en Línea de Comandos (`llamaindex_bot.py`)

```powershell
python llamaindex_bot.py --backend graph
```

Características principales:

- Carga `.env`, valida credenciales de Graph/OpenAI y extiende `PYTHONPATH` con `mcp-sharepoint/src` para desarrollo local.
- Inicia el servidor Graph (`python -m mcp_sharepoint.graph_server`).
- Descubre las herramientas MCP mediante `McpToolSpec` y las entrega a un `FunctionAgent` respaldado por el LLM configurado.
- `ConversationMemory` recuerda el último sitio/drive/folder/file, permitiendo instrucciones como “abre el tercer archivo” sin repetir parámetros.
- Acepta `exit`, `quit` o `Ctrl+C` para cerrar la sesión.

### Script "one-shot"

```powershell
python list_sharepoint_folders.py
```

Envía un único prompt a LlamaIndex para listar el document library configurado.

---

## Interfaz Streamlit (`streamlit_app.py`)

```powershell
streamlit run streamlit_app.py
```

Puntos clave:

- Reutiliza exactamente el mismo agente, cliente MCP y memoria que la CLI.
- Mantiene el backend Graph activo y el event loop asíncrono en un hilo de fondo para chats estables.
- La barra lateral permite conectar/reiniciar el backend y limpiar el historial; el panel principal muestra las burbujas de chat y la memoria contextual.
- Respeta el mismo `.env`; ejecuta Streamlit desde la raíz del repo para que las variables se carguen automáticamente.

Consejos de troubleshooting:

- Define `MCP_CLIENT_DEBUG=1` antes de lanzar si necesitas trazas detalladas de herramientas.
- Reinicia Streamlit tras modificar `.env` para aplicar nuevas credenciales.

---

## Herramientas MCP de `mcp-sharepoint`

| Tool              | Propósito |
|-------------------|-----------|
| `list_sites`      | Enumera los sitios SharePoint accesibles para el service principal |
| `get_site_info`   | Obtiene metadatos de un sitio por URL o ID |
| `list_site_drives`| Lista document libraries / drives dentro del sitio seleccionado |
| `list_drive_items`| Recorre carpetas y archivos dentro de un drive o folder path |
| `get_file_content`| Recupera el contenido de archivos (detección texto/binario manejada por MCP) |
| `search_files`    | (Opcional) Ejecuta consultas de búsqueda de Microsoft Graph |

### Tipos de archivo compatibles

El servidor Graph convierte los formatos comunes de SharePoint a vistas de texto antes de devolverlos al agente (ver `mcp_sharepoint/content_utils.py`).

| Categoría | Extensiones |
|-----------|-------------|
| Texto plano / código | `.txt`, `.csv`, `.json`, `.xml`, `.html`, `.md`, `.js`, `.css`, `.py` |
| PDF | `.pdf` |
| Excel | `.xlsx`, `.xls` |
| Word | `.docx`, `.doc` |

El resto de formatos se pueden obtener como blobs base64, pero no reciben un resumen textual automático.

---

## Flujo de Ejecución

1. **Prompt ingestion** – La UI envía tu solicitud en lenguaje natural al agente.
2. **Context injection** – `ConversationMemory.render_context_prefix()` agrega los últimos valores conocidos (site/drive/folder/file).
3. **Planning** – LlamaIndex selecciona las herramientas MCP necesarias y construye los argumentos.
4. **Execution** – `MemoryMCPClient` completa parámetros faltantes y envía la llamada por stdio al MCP server.
5. **Graph interaction** – El servidor MCP se autentica contra Microsoft Graph, ejecuta la acción y devuelve JSON estructurado.
6. **Response synthesis** – El agente resume los resultados, actualiza la memoria y responde en la CLI o Streamlit.

La memoria reside en el proceso Python, por lo que puedes reiniciar la UI cuando quieras; el backend Graph es stateless entre peticiones.

---

## Flujo de Autenticación

Este proyecto sigue las recomendaciones de [registrar una app para Microsoft Graph](https://learn.microsoft.com/en-us/graph/auth-register-app-v2):

1. **App registration** – Crea una aplicación Azure AD, habilita el flujo *client credentials* y guarda `CLIENT_ID`, `TENANT_ID` y el secreto generado.
2. **Permissions** – Otorga los permisos de aplicación `Sites.Read.All` y `Files.Read.All`, luego concede “Grant admin consent”.
3. **Token acquisition** – En tiempo de ejecución el servidor MCP obtiene un access token app-only desde `https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token`.
4. **Graph calls** – Cada herramienta MCP envía el token en la cabecera `Authorization` al invocar endpoints como `/sites/{siteId}` o `/drives/{driveId}/root`.

Protege los secretos de `.env` y rota el `CLIENT_SECRET` según la política de tu organización.

---

## Consejos Operativos

- **Rotar credenciales**: actualiza `.env` cuando cambie el client secret y reinicia CLI/Streamlit.
- **Debugging**: usa `MCP_CLIENT_DEBUG=1` para registrar argumentos/resultados; revisa el log de Streamlit para errores de UI.
- **Extender herramientas**: agrega nuevas herramientas en `mcp-sharepoint/src/mcp_sharepoint/tools.py`; aparecerán en ambas UIs tras reiniciar.
- **Headless use**: el MCP server puede registrarse en otros clientes MCP (p.ej., Claude Desktop) si necesitas otra interfaz.

---

## Recursos Adicionales

- `mcp-sharepoint/README.md` – Detalles internos del servidor y reportes de validación.
- [Microsoft Graph documentation](https://learn.microsoft.com/en-us/graph/overview) – Referencia oficial para ampliar acciones de SharePoint.
- [LlamaIndex MCP guide](https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamaindex_mcp/) – Profundiza en la integración FunctionAgent + MCP usada aquí.
