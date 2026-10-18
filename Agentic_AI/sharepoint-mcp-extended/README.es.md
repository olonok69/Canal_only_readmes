# Toolkit de Acceso a SharePoint y Datos de Microsoft 365

Un repositorio completo que presenta **tres enfoques distintos** para acceder a SharePoint y datos de Microsoft 365 mediante agentes potenciados por IA y búsqueda semántica. Cada método ofrece diferentes compromisos en términos de autenticación, complejidad de despliegue, requisitos de licenciamiento y capacidades.

---

## 🎯 Resumen

Este repositorio contiene tres soluciones listas para producción para integrar asistentes de IA con SharePoint y Microsoft 365:

| Enfoque | Mejor Para | Autenticación | Tecnología Clave | Ubicación |
|---------|------------|---------------|------------------|-----------|
| **[MCP SharePoint Agent](#1-mcp-sharepoint-agent)** | Desarrollo local, Claude Desktop, integración flexible de herramientas | App-only (service principal) | Model Context Protocol + Microsoft Graph | [`mcp-sharepoint/`](mcp-sharepoint/) |
| **[Azure AI Foundry Agent](#2-azure-ai-foundry-sharepoint-agent)** | Despliegues en producción, permisos específicos de usuario | User identity (OBO) | Azure AI Foundry + SharePoint Tool | [`Foundry_sharepoint/`](Foundry_sharepoint/) |
| **[Graph Retrieval API](#3-búsqueda-semántica-microsoft-graph)** | Búsqueda semántica, descubrimiento de contenido, consultas multi-fuente | Delegated (basada en navegador) | Microsoft Graph Copilot Retrieval API | [`copilot_client/`](copilot_client/) |

---

## 1. MCP SharePoint Agent

**Ubicación:** [`mcp-sharepoint/`](mcp-sharepoint/) y directorio raíz

Un servidor Model Context Protocol (MCP) que expone datos de SharePoint mediante herramientas estandarizadas. Funciona con agentes LlamaIndex y puede integrarse con cualquier cliente compatible con MCP (ej., Claude Desktop, herramientas personalizadas).

### Arquitectura

```
Usuario ➜ (CLI / Streamlit) ➜ LlamaIndex FunctionAgent ➜ MemoryMCPClient ➜ MCP Server ➜ Microsoft Graph ➜ SharePoint
```

### Características Clave

- **Interfaz MCP universal**: Herramientas/recursos estandarizados compatibles con cualquier cliente MCP
- **Autenticación app-only**: Service principal (flujo client credentials) para acceso autónomo
- **Conversation memory**: Recuerda contexto de site, drive, folder a través de conversaciones multi-turno
- **UIs duales**: CLI interactivo (`llamaindex_bot.py`) y web chat Streamlit (`streamlit_app.py`)
- **Extracción de contenido**: Vista previa automática de texto para PDFs, documentos Office, archivos de código
- **Integración Microsoft Search**: Búsqueda semántica en sitios SharePoint

### Herramientas MCP Expuestas

| Tool | Propósito |
|------|-----------|
| `list_sites` | Enumera sitios SharePoint |
| `get_site_info` | Obtiene metadatos para un sitio específico |
| `list_site_drives` | Lista document libraries/drives |
| `list_drive_items` | Navega carpetas y archivos |
| `get_file_content` | Recupera contenido de archivos con extracción de texto |
| `search_files` | Ejecuta consultas de búsqueda Microsoft Graph |

### Requisitos Previos

- **Python 3.9+**
- **Registro de app Azure AD** con flujo client credentials
- **Permisos de aplicación**: `Sites.Read.All`, `Files.Read.All`
- **OpenAI API key** (o LLM compatible)

### Configuración

Crea archivo `.env`:

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

# Valores opcionales por defecto
MCP_DEFAULT_SITE_URL=https://contoso.sharepoint.com/sites/ProjectX
```

### Inicio Rápido

```powershell
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar agente CLI
python llamaindex_bot.py --backend graph

# O ejecutar UI Streamlit
streamlit run streamlit_app.py
```

### Casos de Uso

- **Workflows de IA locales**: Integra acceso a SharePoint en tus herramientas de IA de escritorio
- **Integración Claude Desktop**: Registra como servidor MCP para Claude
- **Automatizaciones personalizadas**: Construye scripts que razonan sobre contenido SharePoint
- **Desarrollo y pruebas**: Prototipado rápido sin despliegue en la nube

### Documentación

- Guía completa: [`README.es.md`](README.es.md) (configuración detallada MCP)
- Capacidades de búsqueda: [`docs/SEMANTIC_SEARCH.md`](docs/SEMANTIC_SEARCH.md)
- Resumen técnico: [`docs/TECHNICAL_OVERVIEW.es.md`](docs/TECHNICAL_OVERVIEW.es.md)

---

## 2. Azure AI Foundry SharePoint Agent

**Ubicación:** [`Foundry_sharepoint/`](Foundry_sharepoint/)

Una UI de chat Streamlit lista para producción conectada a Azure AI Foundry Agent Service con la **herramienta oficial de SharePoint** (preview). Aplica permisos específicos de usuario mediante autenticación On-Behalf-Of (OBO).

### Arquitectura

```
Usuario ➜ Navegador ➜ Streamlit ➜ Azure AI Foundry Agent ➜ SharePoint Tool (OBO) ➜ SharePoint
```

### Características Clave

- **User identity passthrough**: La herramienta SharePoint respeta permisos por usuario (flujo OBO)
- **Integración Microsoft 365 Copilot**: Aprovecha indexación semántica y características licenciadas
- **Agente hospedado en Azure**: Runtime administrado en Azure AI Foundry con versionado
- **Respuestas streaming**: Chat en tiempo real con citas a contenido SharePoint
- **Token caching**: Reduce avisos de autenticación con almacenamiento persistente de tokens
- **Reutilización de agentes**: Conecta a agentes existentes por nombre para evitar proliferación de versiones

### Requisitos Previos

- **Python 3.9+**
- **Proyecto Azure AI Foundry** con despliegue de modelo de chat (ej., `gpt-4o-mini`)
- **Conexión de herramienta SharePoint** creada en portal Foundry
- **Licencias/roles**:
  - Licencia Microsoft 365 Copilot (requerida para desarrolladores y usuarios finales)
  - Rol RBAC `Azure AI User` en proyecto Foundry
  - Acceso de lectura a sitio SharePoint
- **Mismo tenant**: Proyecto Foundry y SharePoint deben estar en el mismo tenant Azure AD

### Configuración

Crea archivo `.env` en [`Foundry_sharepoint/`](Foundry_sharepoint/):

```bash
AZURE_AI_PROJECT_ENDPOINT=https://<tu-proyecto>.services.ai.azure.com
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o-mini
SHAREPOINT_PROJECT_CONNECTION_NAME=<tu-nombre-de-conexion-sharepoint>

# Opcionales
SHAREPOINT_AGENT_NAME=sharepoint-cli-agent
AZURE_TENANT_ID=<tenant-id>  # Recomendado para autenticación estable
```

### Inicio Rápido

```powershell
cd Foundry_sharepoint
pip install -r requirements.txt
streamlit run main.py
```

1. Aparece aviso de autenticación en navegador (primera ejecución)
2. Inicia sesión con cuenta que tenga licencia Microsoft 365 Copilot
3. El agente reutiliza configuración existente o crea una nueva
4. Formula preguntas sobre contenido SharePoint

### Autenticación On-Behalf-Of (OBO)

La herramienta SharePoint **aplica permisos de usuario** en tiempo de ejecución:

- **Flujo**: Usuario inicia sesión → Foundry recibe token → Herramienta SharePoint realiza intercambio OBO → Llamadas posteriores se ejecutan como ese usuario
- **Beneficios**: Cada usuario ve solo su contenido autorizado; sin cuenta de servicio con privilegios excesivos
- **Requisitos**: 
  - Usuario debe tener licencia M365 Copilot
  - Mismo tenant para Foundry y SharePoint
  - Sin soporte para tokens app-only

### Casos de Uso

- **Despliegues en producción**: Listo para empresa con SLAs de Azure
- **Escenarios multi-usuario**: Control de acceso por usuario sin gestión compleja de ACLs
- **Workflows habilitados con Copilot**: Aprovecha indexación semántica de Microsoft
- **Cumplimiento**: Respeta permisos SharePoint existentes automáticamente

### Documentación

- Guía completa: [`Foundry_sharepoint/readme_es.md`](Foundry_sharepoint/readme_es.md)
- Configuración Azure portal: [`docs/AZURE_PORTAL_GUIDE.md`](docs/AZURE_PORTAL_GUIDE.md)
- Troubleshooting autenticación: [`docs/INTRAID_AUTH_GUIDE.md`](docs/INTRAID_AUTH_GUIDE.md)

---

## 3. Búsqueda Semántica Microsoft Graph

**Ubicación:** [`copilot_client/`](copilot_client/) (componente Graph Retrieval)

Una interfaz web basada en Django para **búsqueda semántica** a través de contenido Microsoft 365 usando Microsoft Graph Copilot Retrieval API. Busca en SharePoint, OneDrive, Outlook y fuentes de datos externas con consultas en lenguaje natural.

### Arquitectura

```
Usuario ➜ Navegador (MSAL.js) ➜ Django Backend ➜ Graph Copilot Retrieval API ➜ Fuentes de Datos M365
```

### Características Clave

- **Búsqueda en lenguaje natural**: Descubrimiento de contenido potenciado por IA a través de múltiples fuentes
- **Consultas multi-fuente**: SharePoint, OneDrive (Business), Outlook, contenido External/Web
- **Autenticación basada en navegador**: Autenticación delegada MSAL.js (auth code + PKCE)
- **Tarjetas de resultados enriquecidas**: Respuestas formateadas con extractos de texto, URLs, metadatos
- **Sin agente requerido**: Acceso directo a API para descubrimiento de contenido sin contexto de conversación
- **Resultados en tiempo real**: Resultados de búsqueda inmediatos sin procesamiento en segundo plano

### Fuentes de Datos Soportadas

| Fuente | Descripción | Scope Requerido |
|--------|-------------|-----------------|
| **SharePoint** | Colecciones de sitios y libraries | `Sites.ReadWrite.All` |
| **OneDrive (Business)** | Archivos OneDrive de usuario | `Files.ReadWrite.All` |
| **Outlook** | Email y adjuntos | `Mail.Read` |
| **External/Web** | Conectores externos | `ExternalItem.Read.All` |

### Requisitos Previos

- **Python 3.9+**
- **Framework Django**
- **Licencia Microsoft 365 Copilot** (requerida para acceso a Retrieval API)
- **Registro de app Azure AD** (Single-page application):
  - URI de redireccionamiento: `http://localhost:8000/graph/`
  - Permisos delegados: `CopilotPackages.Read.All`, `Sites.ReadWrite.All`, `Files.ReadWrite.All`, `ExternalItem.Read.All`
  - Admin consent concedido

### Configuración

Agrega a `.env` en [`copilot_client/`](copilot_client/):

```bash
TENANT_ID=<tu-tenant-id>
CLIENT_ID_2=<tu-client-id>
GRAPH_SCOPES=https://graph.microsoft.com/CopilotPackages.Read.All https://graph.microsoft.com/Sites.ReadWrite.All https://graph.microsoft.com/Files.ReadWrite.All https://graph.microsoft.com/ExternalItem.Read.All

# Fuente de datos predeterminada opcional
COPILOT_DATA_SOURCE=SharePoint  # SharePoint, OneDriveBusiness, ExternalItem
```

### Inicio Rápido

```powershell
cd copilot_client
pip install -r requirements.txt
python manage.py runserver
```

Navega a: `http://localhost:8000/graph/`

1. Haz clic en **Sign in** (autenticación MSAL.js)
2. Selecciona fuente de datos (SharePoint, Files, OneDrive, Web)
3. Ingresa consulta en lenguaje natural (ej., "latest project updates")
4. Ver resultados como tarjetas formateadas

### Casos de Uso

- **Descubrimiento de contenido**: Encuentra documentos a través de múltiples fuentes M365
- **Workflows search-first**: Respuestas rápidas sin contexto completo de conversación
- **Exploración de documentos**: Navega y previsualiza contenido con URLs
- **Escenarios multi-tenant**: Búsqueda con alcance de usuario respetando permisos

### Documentación

- Guía Graph Retrieval: [`copilot_client/docs/graph-retrieval.es.md`](copilot_client/docs/graph-retrieval.es.md)
- Detalles frontend: [`copilot_client/docs/graph-frontend.es.md`](copilot_client/docs/graph-frontend.es.md)
- Cliente copilot completo: [`copilot_client/README.es.md`](copilot_client/README.es.md)

---

## 🔍 Matriz de Comparación

### Autenticación y Seguridad

| Característica | MCP SharePoint | Foundry Agent | Graph Retrieval |
|----------------|----------------|---------------|-----------------|
| **Tipo Auth** | App-only (service principal) | User identity (OBO) | Delegated (navegador) |
| **Permisos Usuario** | Nivel cuenta de servicio | Por usuario (aplicado) | Por usuario (aplicado) |
| **Gestión Tokens** | Client credentials | Interactive + cache | MSAL.js + cache |
| **Cross-Tenant** | Sí | No (mismo tenant requerido) | No (mismo tenant requerido) |

### Licenciamiento y Requisitos

| Característica | MCP SharePoint | Foundry Agent | Graph Retrieval |
|----------------|----------------|---------------|-----------------|
| **Licencia M365 Copilot** | ❌ No requerida | ✅ Requerida | ✅ Requerida |
| **Azure AI Foundry** | ❌ No requerido | ✅ Requerido | ❌ No requerido |
| **Permisos Graph API** | Aplicación | Ninguno (vía tool) | Delegados |
| **Admin Consent** | Requerido | No requerido | Requerido |

### Despliegue y Operaciones

| Característica | MCP SharePoint | Foundry Agent | Graph Retrieval |
|----------------|----------------|---------------|-----------------|
| **Deployment** | Local/self-hosted | Azure cloud | Local/self-hosted |
| **Escalabilidad** | Basada en procesos | Gestionada por Azure | Basada en app-server |
| **Monitoreo** | Logging personalizado | Métricas Azure AI | Django logging |
| **Costo** | Solo API OpenAI | Compute Foundry + modelo | Solo desarrollo |

### Capacidades

| Característica | MCP SharePoint | Foundry Agent | Graph Retrieval |
|----------------|----------------|---------------|-----------------|
| **Conversation Memory** | ✅ Contexto multi-turno | ✅ Gestionado por agente | ❌ Consultas únicas |
| **Tool Calling** | ✅ Herramientas MCP extensibles | ✅ Solo herramienta SharePoint | ❌ API directa |
| **Extracción Contenido** | ✅ Vista previa texto | ✅ Vía herramienta SharePoint | ✅ Extractos texto |
| **Citas** | ✅ URLs en respuestas | ✅ Citas incluidas | ✅ Tarjetas resultado con URLs |
| **Búsqueda Semántica** | ✅ Microsoft Search | ✅ Integrada | ✅ Copilot Retrieval API |
| **Búsqueda Multi-Fuente** | ❌ Solo SharePoint | ❌ Solo SharePoint | ✅ SharePoint + OneDrive + Outlook |

---

## 🚀 Cuándo Usar Cada Enfoque

### Elige **MCP SharePoint** cuando:
- Construyas workflows de IA locales o integraciones de escritorio
- Necesites personalización y extensión flexible de herramientas
- Quieras integrar con Claude Desktop u otros clientes MCP
- Escenarios de desarrollo/pruebas sin despliegue en producción
- El acceso con cuenta de servicio sea aceptable (sin permisos por usuario necesarios)

### Elige **Azure AI Foundry Agent** cuando:
- Despliegues a producción con requisitos empresariales
- Los permisos por usuario sean críticos (cumplimiento, seguridad)
- Los usuarios tengan licencias Microsoft 365 Copilot
- Quieras infraestructura gestionada por Azure con SLAs
- Necesites audit trails vinculados a identidades de usuario

### Elige **Graph Retrieval API** cuando:
- El caso de uso primario sea búsqueda/descubrimiento (no conversación)
- Necesites consultar a través de múltiples fuentes M365 (SharePoint + OneDrive + Outlook)
- Quieras respuestas rápidas sin overhead de agente
- Construyas experiencias search-first o UIs exploratorias
- Los usuarios interactúen directamente con autenticación basada en navegador

---

## 📚 Requisitos Previos Comunes

Los tres enfoques requieren:

- **Tenant Azure AD** con licencias apropiadas
- **SharePoint Online** acceso
- **Python 3.9+** entorno de desarrollo
- **Registro(s) de app Microsoft Entra** con permisos apropiados

### Documentación Compartida

- **Resumen Técnico**: [`docs/TECHNICAL_OVERVIEW.es.md`](docs/TECHNICAL_OVERVIEW.es.md)
- **Librerías Acceso SharePoint**: [`docs/SHAREPOINT_ACCESS_LIBRARIES_COMPARISON.md`](docs/SHAREPOINT_ACCESS_LIBRARIES_COMPARISON.md)
- **Guía Azure Portal**: [`docs/AZURE_PORTAL_GUIDE.md`](docs/AZURE_PORTAL_GUIDE.md)
- **Guía Autenticación**: [`docs/INTRAID_AUTH_GUIDE.md`](docs/INTRAID_AUTH_GUIDE.md)

---

## 🛠️ Instalación (Todos los Componentes)

```powershell
# Clonar repositorio
git clone <repository-url>
cd sharepoint-mcp-extended

# Instalar componentes MCP SharePoint
pip install -r requirements.txt

# Instalar componentes agente Foundry
cd Foundry_sharepoint
pip install -r requirements.txt
cd ..

# Instalar componentes graph retrieval
cd copilot_client
pip install -r requirements.txt
cd ..
```

---

## 🔐 Mejores Prácticas de Seguridad

1. **Nunca commits secretos**: Usa archivos `.env` y `.gitignore`
2. **Rotar credenciales**: Actualiza regularmente client secrets y API keys
3. **Least privilege**: Otorga permisos mínimos requeridos para cada enfoque
4. **Monitorear uso**: Rastrea llamadas API, uso de tokens y patrones de acceso
5. **Secretos producción**: Usa Azure Key Vault o similar para despliegues producción
6. **Solo HTTPS**: Usa conexiones seguras para aplicaciones web en producción
7. **Token caching**: Implementa almacenamiento seguro de tokens con encriptación

---

## 🐛 Solución de Problemas

### Problemas Comunes en Todos los Enfoques

**Fallos de Autenticación:**
- Verifica que los IDs de tenant coincidan entre app registration y configuración
- Revisa que los permisos estén otorgados y con admin consent
- Asegura que los URIs de redireccionamiento coincidan exactamente (incluyendo protocolo y puerto)

**Errores de Permisos:**
- Confirma que usuario/service principal tenga permisos requeridos de Graph API
- Verifica acceso a sitio SharePoint para la identidad autenticada
- Revisa estado de licencia Microsoft 365 Copilot (Foundry & Graph Retrieval)

**Problemas de Tokens:**
- Limpia caché de tokens y re-autentica
- Verifica que los scopes coincidan con los permisos API requeridos
- Revisa expiración de token y disponibilidad de refresh token

**Red/Conectividad:**
- Confirma que firewall permita endpoints Microsoft Graph
- Revisa configuración de proxy si estás detrás de red corporativa
- Verifica que región Azure y URLs de endpoint sean correctas

### Troubleshooting Específico por Enfoque

- **MCP SharePoint**: Revisa que `GRAPH_SEARCH_REGION` coincida con ubicación del tenant
- **Foundry Agent**: Asegura mismo tenant para proyecto Foundry y SharePoint
- **Graph Retrieval**: Usa `localhost` (no `127.0.0.1`) para URI de redireccionamiento

---

## 📖 Recursos Adicionales

### Documentación Microsoft
- [Microsoft Graph API](https://learn.microsoft.com/en-us/graph/overview)
- [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Microsoft 365 Copilot Retrieval API](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/api-reference/retrieval-api-overview)
- [Documentación SharePoint](https://learn.microsoft.com/en-us/sharepoint/)
- [Flujo OAuth 2.0 On-Behalf-Of](https://learn.microsoft.com/azure/active-directory/develop/v2-oauth2-on-behalf-of-flow)

### Documentación de Frameworks
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [LlamaIndex](https://docs.llamaindex.ai/)
- [Streamlit](https://docs.streamlit.io/)
- [Django](https://docs.djangoproject.com/)
- [MSAL.js](https://learn.microsoft.com/azure/active-directory/develop/msal-overview)

---

## 📝 Licencia

Ver directorios de componentes individuales para información de licenciamiento.

---

## 🤝 Contribuciones

¡Contribuciones bienvenidas! Cada componente tiene sus propias guías de desarrollo:
- MCP SharePoint: Ver [`README.es.md`](README.es.md) raíz
- Foundry Agent: Ver [`Foundry_sharepoint/readme_es.md`](Foundry_sharepoint/readme_es.md)
- Graph Retrieval: Ver [`copilot_client/README.es.md`](copilot_client/README.es.md)

---

## 📞 Soporte

Para problemas específicos de cada enfoque:
- **MCP SharePoint**: Revisa documentación [`mcp-sharepoint/`](mcp-sharepoint/)
- **Foundry Agent**: Ver docs Azure AI Foundry y [`docs/AZURE_PORTAL_GUIDE.md`](docs/AZURE_PORTAL_GUIDE.md)
- **Graph Retrieval**: Consulta guías en [`copilot_client/docs/`](copilot_client/docs/)

---

**Última Actualización**: Enero 2026
