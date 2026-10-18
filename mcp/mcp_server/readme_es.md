# Tutorial Completo: MCP (Model Context Protocol) y Configuración de Servidores

## 1. ¿Qué es MCP (Model Context Protocol)?

El Model Context Protocol (MCP) es un estándar abierto desarrollado por Anthropic que permite a los modelos de IA comunicarse con fuentes de datos externas, herramientas y recursos de manera estandarizada. 

### Conceptos Fundamentales de MCP

Los servidores MCP pueden proporcionar tres tipos principales de capacidades:

- **Resources**: Datos similares a archivos que pueden ser leídos por los clientes (como respuestas de API o contenido de archivos)
- **Tools**: Funciones que pueden ser llamadas por el LLM (con aprobación del usuario)  
- **Prompts**: Plantillas predefinidas que ayudan a los usuarios a realizar tareas específicas

### Ventajas del MCP

- **Estandarización**: Protocolo común para conectar IA con herramientas externas
- **Seguridad**: Control granular sobre qué herramientas puede usar la IA
- **Extensibilidad**: Fácil adición de nuevas capacidades
- **Interoperabilidad**: Funciona con diferentes clientes y servidores

## 2. Protocolos de Conexión con Cliente

### 2.1. STDIO (Standard Input/Output)
- **Descripción**: Comunicación a través de entrada y salida estándar
- **Uso**: Más común para aplicaciones de escritorio como Claude Desktop
- **Configuración**: Se ejecuta como proceso hijo del cliente

### 2.2. HTTP/SSE (Server-Sent Events)
- **Descripción**: Comunicación basada en HTTP con eventos del servidor
- **Uso**: Para servidores remotos y aplicaciones web
- **Configuración**: Requiere configuración de puerto y URL

### 2.3. WebSocket
- **Descripción**: Comunicación bidireccional en tiempo real
- **Uso**: Para aplicaciones que requieren baja latencia
- **Estado**: En desarrollo activo

## 3. Claude Desktop Application

### 3.1. Instalación de Claude Desktop

Puedes descargar Claude Desktop desde claude.ai/download. La aplicación está disponible para:

- **macOS**: Versión nativa para Apple Silicon y Intel
- **Windows**: Versión para Windows 10/11
- **Linux**: Actualmente no disponible oficialmente

#### Requisitos del Sistema
- **Node.js**: Versión 16 o superior
- **Python**: 3.8 o superior (para servidores Python)
- **Java**: 17 o superior (para servidores Java)

### 3.2. Configuración del Archivo de Configuración

El archivo de configuración se encuentra en:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

#### Estructura Básica del Archivo de Configuración

```json
{
  "mcpServers": {
    "nombre-servidor": {
      "command": "comando-para-ejecutar",
      "args": ["argumento1", "argumento2"],
      "env": {
        "VARIABLE_ENTORNO": "valor"
      }
    }
  }
}
```

## 4. Configuración de Servidores MCP Específicos

### 4.1. MCP Google Search

Un servidor MCP que proporciona capacidades de búsqueda web usando la API de Google Custom Search y funcionalidad de extracción de contenido de páginas web.

#### Prerrequisitos

1. **Crear un Proyecto de Google Cloud**:
   - Ir a Google Cloud Console
   - Crear un nuevo proyecto o seleccionar uno existente
   - Habilitar facturación para tu proyecto

2. **Habilitar Custom Search API**:
   - Ir a API Library
   - Buscar "Custom Search API"
   - Hacer clic en "Habilitar"

3. **Obtener API Key**:
   - Ir a Credentials
   - Hacer clic en "Create Credentials" > "API Key"
   - Copiar tu API key

4. **Crear Custom Search Engine**:
   - Ir a Programmable Search Engine
   - Ingresar los sitios que quieres buscar (usar www.google.com para búsqueda web general)
   - Hacer clic en "Create"
   - En la configuración, habilitar "Search the entire web"
   - Copiar tu Search Engine ID (cx)

#### Instalación y Configuración

```bash
# Instalación automática via Smithery
npx -y @smithery/cli install @adenot/mcp-google-search --client claude
```

**Configuración en claude_desktop_config.json**:

```json
{
  "mcpServers": {
    "google-search": {
      "command": "npx",
      "args": [
        "-y",
        "@adenot/mcp-google-search"
      ],
      "env": {
        "GOOGLE_API_KEY": "tu-api-key-aqui",
        "GOOGLE_SEARCH_ENGINE_ID": "tu-search-engine-id-aqui"
      }
    }
  }
}
```

#### Herramientas Disponibles

- **search**: Realizar búsquedas web usando Google Custom Search API
- **read_webpage**: Extraer contenido de cualquier página web

### 4.2. MCP Server Brave Search

Una implementación de servidor MCP que integra la API de Brave Search, proporcionando capacidades de búsqueda web y local.

#### Prerrequisitos

1. Registrarse para una cuenta de Brave Search API
2. Elegir un plan (plan gratuito disponible con 2,000 consultas/mes)
3. Generar tu API key desde el dashboard de desarrollador

#### Configuración

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-brave-search"
      ],
      "env": {
        "BRAVE_API_KEY": "TU_API_KEY_AQUI"
      }
    }
  }
}
```

#### Herramientas Disponibles

- **brave_web_search**: Ejecutar búsquedas web con paginación y filtrado
- **brave_local_search**: Buscar negocios y servicios locales

### 4.3. MCP Server Gmail

Un servidor MCP para integración con Gmail en Claude Desktop con soporte de autenticación automática. Este servidor permite a los asistentes de IA gestionar Gmail a través de interacciones en lenguaje natural.

#### Características Principales

- Enviar emails con asunto, contenido, adjuntos y destinatarios
- Soporte completo para caracteres internacionales
- Leer mensajes de email por ID
- Ver información de adjuntos
- Buscar emails con varios criterios
- Gestión completa de etiquetas
- Operaciones por lotes para procesamiento eficiente

#### Configuración

**1. Crear Proyecto de Google Cloud y obtener credenciales**:

a. Crear un Proyecto de Google Cloud:
   - Ir a Google Cloud Console
   - Crear un nuevo proyecto o seleccionar uno existente
   - Habilitar la Gmail API para tu proyecto

b. Crear Credenciales OAuth 2.0:
   - Ir a "APIs & Services" > "Credentials"
   - Hacer clic en "Create Credentials" > "OAuth client ID"
   - Elegir "Desktop app" o "Web application" como tipo de aplicación
   - Para aplicación web, agregar `http://localhost:3000/oauth2callback` a las URIs de redirección autorizadas
   - Descargar el archivo JSON de las claves OAuth
   - Renombrar el archivo a `gcp-oauth.keys.json`

**2. Ejecutar Autenticación**:

```bash
# Autenticación global (Recomendada)
mkdir -p ~/.gmail-mcp
mv gcp-oauth.keys.json ~/.gmail-mcp/
npx @gongrzhe/server-gmail-autoauth-mcp auth
```

**3. Configurar en Claude Desktop**:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": [
        "@gongrzhe/server-gmail-autoauth-mcp"
      ]
    }
  }
}
```

#### Herramientas Principales

- **send_message**: Envía un nuevo email inmediatamente
- **create_draft**: Crea un borrador de email sin enviarlo
- **read_message**: Recupera el contenido de un email específico por su ID
- **search_emails**: Busca emails usando sintaxis de búsqueda de Gmail
- **modify_labels**: Añade o remueve etiquetas de emails
- **delete_message**: Elimina permanentemente un email

### 4.4. MCP Server Word

Un servidor MCP para crear, leer y manipular documentos de Microsoft Word. Este servidor permite a los asistentes de IA trabajar con documentos de Word a través de una interfaz estandarizada.

#### Características Principales

- Crear nuevos documentos de Word con metadata
- Extraer texto y analizar estructura del documento
- Añadir encabezados con diferentes niveles
- Insertar párrafos con estilo opcional
- Crear tablas con datos personalizados
- Añadir imágenes con escalado proporcional
- Formatear texto específico (negrita, cursiva, subrayado)
- Buscar y reemplazar texto

#### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/GongRzhe/Office-Word-MCP-Server.git
cd Office-Word-MCP-Server

# Instalar dependencias
pip install -r requirements.txt
```

#### Configuración

**Opción 1: Instalación local**
```json
{
  "mcpServers": {
    "word-document-server": {
      "command": "python",
      "args": [
        "/ruta/absoluta/a/word_server.py"
      ]
    }
  }
}
```

**Opción 2: Usando uvx (Recomendada)**
```json
{
  "mcpServers": {
    "word-document-server": {
      "command": "uvx",
      "args": [
        "--from",
        "office-word-mcp-server",
        "word_mcp_server"
      ],
      "env": {}
    }
  }
}
```

#### Herramientas Principales

- **create_document**: Crear nuevo documento con metadata opcional
- **add_paragraph**: Añadir párrafo al documento
- **add_heading**: Añadir encabezado con nivel específico
- **add_table**: Añadir tabla con datos personalizados
- **format_text**: Formatear rango específico de texto
- **search_and_replace**: Buscar y reemplazar texto en todo el documento

## 5. Configuración Completa de Ejemplo

Basándome en tu archivo de configuración, aquí está la configuración completa explicada:

```json
{
  "mcpServers": {
    "google-search": {
      "command": "npx",
      "args": [
        "-y",
        "@adenot/mcp-google-search"
      ],
      "env": {
        "GOOGLE_API_KEY": "tu-google-api-key",
        "GOOGLE_SEARCH_ENGINE_ID": "tu-search-engine-id"
      }
    },
    "gmail": {
      "command": "npx",
      "args": [
        "@gongrzhe/server-gmail-autoauth-mcp"
      ]
    },
    "brave-search": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-brave-search"
      ],
      "env": {
        "BRAVE_API_KEY": "tu-brave-api-key"
      }
    },
    "word-document-server": {
      "command": "uvx",
      "args": [
        "--from",
        "office-word-mcp-server",
        "word_mcp_server"
      ],
      "env": {}
    }
  }
}
```

## 6. Verificación y Resolución de Problemas

### 6.1. Verificar Configuración

Después de configurar, reinicia Claude Desktop y verifica:

1. **Icono MCP**: Deberías ver el icono del martillo en la interfaz
2. **Configuración de Desarrollador**: Ve a Settings > Developer para ver los logs
3. **Estado de Conexión**: Verifica que los servidores aparezcan como "conectados"

### 6.2. Problemas Comunes

**1. Servidores no se conectan**
- Verificar rutas absolutas en la configuración
- Comprobar que las dependencias están instaladas
- Revisar logs de desarrollador para errores específicos

**2. Variables de entorno no reconocidas**
- Verificar que las API keys están correctamente configuradas
- Comprobar permisos de archivos de credenciales

**3. Comandos no funcionan**
- Verificar instalación de Node.js: `node --version`
- Comprobar que npm funciona: `npm --version`
- Probar comandos manualmente en terminal

### 6.3. Depuración

Para depuración avanzada, puedes usar el MCP Inspector:

```bash
npm run inspector
```

El Inspector proporcionará una URL para acceder a herramientas de depuración en tu navegador.

## 7. Mejores Prácticas

### 7.1. Seguridad
- Nunca commits credenciales al control de versiones
- Usa variables de entorno para API keys sensibles
- Revisa regularmente los permisos de acceso en tus cuentas

### 7.2. Rendimiento
- Limita el número de servidores MCP simultáneos
- Usa configuraciones de batch para operaciones masivas
- Monitorea el uso de API para evitar límites

### 7.3. Mantenimiento
- Actualiza regularmente los servidores MCP
- Mantén respaldos de tus configuraciones
- Documenta configuraciones personalizadas

## 8. Recursos Adicionales

- **Documentación oficial MCP**: https://modelcontextprotocol.io/
- **Guía de depuración**: https://modelcontextprotocol.io/docs/tools/debugging
- **Servidores oficiales**: https://github.com/modelcontextprotocol/servers
- **SDK de Python**: https://github.com/modelcontextprotocol/python-sdk

## Conclusión

El Model Context Protocol representa un avance significativo en la manera en que los modelos de IA pueden interactuar con herramientas y datos externos. Con la configuración adecuada de servidores MCP, Claude Desktop se convierte en una herramienta poderosa capaz de gestionar emails, crear documentos, realizar búsquedas web y mucho más, todo a través de interfaces conversacionales naturales.

La clave del éxito está en una configuración cuidadosa, el manejo seguro de credenciales y la comprensión de las capacidades específicas de cada servidor MCP que instalas.