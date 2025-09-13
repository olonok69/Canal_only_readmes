# Servidores MCP Demo con Claude AI - Guía Completa

## Tabla de Contenidos
1. [Introducción al Protocolo de Contexto de Modelo (MCP)](#introduccion)
2. [Mecanismos de Transporte: SSE vs STDIO](#mecanismos-de-transporte)
3. [Prerrequisitos y Configuración](#prerrequisitos)
4. [Configuraciones de Servidores MCP](#configuraciones-servidores-mcp)
5. [Servidor MCP de Google Search](#servidor-google-search)
6. [Servidor MCP de Gmail API](#servidor-gmail-api)
7. [Servidor MCP de Brave Search](#servidor-brave-search)
8. [Servidor MCP de Microsoft Office Word](#servidor-microsoft-office-word)
9. [Configuración de Claude Desktop](#configuracion-claude-desktop)
10. [Pruebas y Validación](#pruebas-y-validacion)
11. [Mejores Prácticas y Seguridad](#mejores-practicas)
12. [Solución de Problemas](#solucion-de-problemas)
13. [Recursos Adicionales](#recursos-adicionales)

## Introducción al Protocolo de Contexto de Modelo (MCP) {#introduccion}

El **Protocolo de Contexto de Modelo (MCP)** es un estándar abierto desarrollado por Anthropic que permite la integración perfecta entre asistentes de IA como Claude y fuentes de datos externas, herramientas y sistemas. MCP aborda el desafío de los modelos de IA que están aislados de los datos—atrapados detrás de silos de información y sistemas heredados, proporcionando un estándar universal y abierto para conectar sistemas de IA con fuentes de datos, reemplazando integraciones fragmentadas con un protocolo único.

### Componentes Clave

MCP adopta una arquitectura cliente-servidor con tres componentes principales:
- **Hosts**: Aplicaciones de IA que inician conexiones (ej., Claude Desktop)
- **Clientes**: Sistemas que mantienen conexiones uno a uno con servidores dentro de la aplicación host
- **Servidores**: Sistemas que proporcionan contexto, herramientas y prompts a los clientes

### Beneficios de MCP

- **Integración Estandarizada**: MCP reemplaza enfoques fragmentados con un protocolo único y estandarizado, acelerando el desarrollo y reduciendo la carga de mantenimiento
- **Flexibilidad**: Fácil cambio entre diferentes modelos de IA y proveedores
- **Seguridad**: Mantiene los datos dentro de tu infraestructura mientras interactúa con IA
- **Escalabilidad**: Soporta varios transportes como stdio, WebSockets, HTTP SSE y sockets UNIX

## Mecanismos de Transporte: SSE vs STDIO {#mecanismos-de-transporte}

MCP actualmente define dos mecanismos de transporte estándar para la comunicación cliente-servidor: stdio (comunicación sobre entrada y salida estándar) y HTTP con Server-Sent Events (SSE)

### Transporte STDIO

**Características:**
- Permite comunicación a través de flujos de entrada y salida estándar, particularmente útil para integraciones locales y herramientas de línea de comandos
- El cliente lanza el servidor MCP como un subproceso, con el servidor recibiendo mensajes JSON-RPC en stdin y escribiendo respuestas a stdout
- Baja latencia para comunicación local
- Recomendado por la especificación: "Los clientes DEBERÍAN soportar stdio siempre que sea posible"

**Casos de Uso:**
- Entornos de desarrollo local
- Herramientas de línea de comandos
- Integraciones en proceso
- Conexiones locales donde la comunicación ocurre dentro de la misma máquina

**Ejemplo de Configuración:**
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/ruta/al/directorio"]
}
```

### Transporte SSE (Server-Sent Events)

**Características:**
- Permite streaming servidor-a-cliente con solicitudes HTTP POST para comunicación cliente-a-servidor
- Usa HTTP con Server-Sent Events, y cuando se hospeda en endpoints HTTPS, soporta conexiones encriptadas vía TLS
- Escenarios en tiempo real basados en web
- Se integra perfectamente con endpoints OpenAPI y soporta sistemas distribuidos con su fundación HTTP

**Casos de Uso:**
- Conexiones de servidor remoto
- Aplicaciones basadas en web
- Streaming de datos en tiempo real
- Sistemas distribuidos

**Consideraciones de Seguridad:**
Los transportes SSE pueden ser vulnerables a ataques de DNS rebinding si no están apropiadamente asegurados. Para prevenir esto:
- Siempre validar headers de Origin en conexiones SSE entrantes
- Evitar vincular servidores a todas las interfaces de red (0.0.0.0) - vincular solo a localhost (127.0.0.1)
- Implementar autenticación apropiada para todas las conexiones SSE

### Resumen de Comparación

| Característica | STDIO | SSE |
|----------------|-------|-----|
| **Latencia** | Baja (local) | Mayor (red) |
| **Complejidad de Configuración** | Simple | Moderada |
| **Seguridad** | Solo local | Requiere HTTPS/auth |
| **Escalabilidad** | Limitada a local | Alta (distribuida) |
| **Tiempo Real** | Sí | Sí |
| **Compatible con OpenAPI** | Requiere proxy | Nativo |
| **Acceso Remoto** | Requiere proxy | Nativo |

Mientras que SSE se alinea naturalmente con herramientas cliente modernas que demandan APIs accesibles web, el enfoque local de stdio necesita pasos adicionales para mayor accesibilidad

## Prerrequisitos y Configuración {#prerrequisitos}

### Software Requerido

1. **Node.js**: Descargar de [nodejs.org](https://nodejs.org/en/download/)
   ```bash
   # Verificar instalación
   node --version
   npm --version
   ```

2. **Aplicación Claude Desktop**: Descargar la última versión
   - Asegurar que esté actualizada para soportar MCP
   - Disponible para macOS y Windows (soporte para Linux vía construcción de cliente)

3. **Python (para Servidor MCP de Word)**: Python 3.10+ requerido
   ```bash
   # Instalar gestor de paquetes uv (Mac/Linux)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### Requisitos del Sistema

- Sistema Operativo: macOS, Windows o Linux
- Conexión a internet para servicios API
- Privilegios administrativos para la instalación

## Configuraciones de Servidores MCP {#configuraciones-servidores-mcp}

## Servidor MCP de Google Search {#servidor-google-search}

### Descripción General
El servidor MCP de Google Search permite a Claude realizar búsquedas web usando la API de Búsqueda Personalizada de Google.

**Repositorio**: [https://github.com/adenot/mcp-google-search](https://github.com/adenot/mcp-google-search)

### Proceso de Configuración

#### 1. Crear Proyecto de Google Cloud
1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear un nuevo proyecto o seleccionar uno existente
3. Habilitar facturación para tu proyecto

#### 2. Habilitar API de Búsqueda Personalizada
1. Navegar a [Biblioteca de APIs](https://console.cloud.google.com/apis/library)
2. Buscar "Custom Search API"
3. Hacer clic en "Habilitar"

#### 3. Generar Clave API
1. Ir a [Credenciales](https://console.cloud.google.com/apis/credentials)
2. Hacer clic en "Crear Credenciales" > "Clave API"
3. Copiar tu clave API
4. (Opcional) Restringir la clave API solo a la API de Búsqueda Personalizada

#### 4. Crear Motor de Búsqueda Personalizada
1. Visitar [Motor de Búsqueda Programable](https://programmablesearchengine.google.com/create/new)
2. Ingresar sitios para buscar (usar `www.google.com` para búsqueda web general)
3. Hacer clic en "Crear"
4. En la siguiente página, hacer clic en "Personalizar"
5. En configuraciones, habilitar "Buscar en toda la web"
6. Copiar tu ID del Motor de Búsqueda (parámetro cx)

### Instalación
```bash
# Instalar vía npm
npx -y @adenot/mcp-google-search
```

### Configuración
```json
{
  "google-search": {
    "command": "npx",
    "args": ["-y", "@adenot/mcp-google-search"],
    "env": {
      "GOOGLE_API_KEY": "tu_clave_api_aqui",
      "GOOGLE_SEARCH_ENGINE_ID": "tu_id_motor_busqueda_aqui"
    }
  }
}
```

## Servidor MCP de Gmail API {#servidor-gmail-api}

### Descripción General
Permite a Claude interactuar con Gmail, proporcionando capacidades de gestión de correo electrónico.

**Repositorio**: [https://github.com/GongRzhe/Gmail-MCP-Server](https://github.com/GongRzhe/Gmail-MCP-Server)

### Proceso de Configuración

#### 1. Habilitar API de Gmail
1. En Google Cloud Console, ir a "APIs y Servicios" > "Credenciales"
2. Hacer clic en "Crear Credenciales" > "ID de cliente OAuth"
3. Elegir "Aplicación de escritorio" o "Aplicación web"
4. Para aplicación web, agregar `http://localhost:3000/oauth2callback` a URIs de redirección autorizadas
5. Descargar el archivo JSON con claves OAuth
6. Renombrar archivo a `gcp-oauth.keys.json`

#### 2. Instalar y Configurar
```bash
# Instalar servidor MCP
npx -y @smithery/cli install @gongrzhe/server-gmail-autoauth-mcp --client claude

# Autenticar cliente
npx @gongrzhe/server-gmail-autoauth-mcp auth
```

### Configuración
```json
{
  "gmail": {
    "command": "npx",
    "args": ["@gongrzhe/server-gmail-autoauth-mcp"]
  }
}
```

### Capacidades
- Buscar correos usando sintaxis de búsqueda de Gmail
- Leer contenido de correos
- Enviar y borrador de correos
- Modificar etiquetas de correo
- Operaciones en lote para múltiples correos
- Crear y gestionar etiquetas de Gmail

## Servidor MCP de Brave Search {#servidor-brave-search}

### Descripción General
Proporciona capacidades de búsqueda web usando la API de Brave Search con características mejoradas de privacidad.

**Repositorio**: [https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search](https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search)

### Proceso de Configuración

#### 1. Obtener Clave API de Brave Search
1. Registrarse para una cuenta de API de Brave Search
2. Elegir un plan (Nivel gratuito: 2,000 consultas/mes)
3. Generar clave API desde el dashboard de desarrollador

#### 2. Instalación
```bash
# Instalar vía npm
npx -y @modelcontextprotocol/server-brave-search
```

### Configuración
```json
{
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": {
      "BRAVE_API_KEY": "tu_clave_api_brave_aqui"
    }
  }
}
```

### Características
- Búsqueda web general
- Búsqueda de negocios locales
- Búsqueda de noticias
- Búsqueda de imágenes (si está soportado por el plan API)
- Privacidad mejorada comparado con otros motores de búsqueda

## Servidor MCP de Microsoft Office Word {#servidor-microsoft-office-word}

### Descripción General
Permite a Claude crear, editar y gestionar documentos de Microsoft Word programáticamente.

**Repositorio**: [https://github.com/GongRzhe/Office-Word-MCP-Server](https://github.com/GongRzhe/Office-Word-MCP-Server)

### Proceso de Configuración

#### 1. Clonar Repositorio
```bash
git clone https://github.com/GongRzhe/Office-Word-MCP-Server.git
cd Office-Word-MCP-Server
```

#### 2. Instalar Dependencias
```bash
# Usando uvx (recomendado)
uvx --from office-word-mcp-server word_mcp_server
```

### Configuración
```json
{
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
```

### Capacidades
- Crear nuevos documentos de Word
- Agregar párrafos, encabezados, tablas
- Insertar imágenes y saltos de página
- Formatear texto (negrita, cursiva, colores, fuentes)
- Buscar y reemplazar texto
- Agregar notas al pie y notas finales
- Convertir documentos a PDF
- Protección con contraseña
- Plantillas de documentos

## Configuración de Claude Desktop {#configuracion-claude-desktop}

### Archivo de Configuración Completo

Crear o editar `claude_desktop_config.json` en tu directorio de soporte de aplicación de Claude Desktop:

**Ubicación:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

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
        "GOOGLE_API_KEY": "tu_clave_api_google",
        "GOOGLE_SEARCH_ENGINE_ID": "tu_id_motor_busqueda"
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
        "BRAVE_API_KEY": "tu_clave_api_brave"
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

### Pasos de Configuración

1. **Respaldar Configuración Existente**: Siempre respalda tu configuración existente
2. **Reemplazar Claves API**: Completa con tus claves API y credenciales reales
3. **Validar JSON**: Asegurar formato JSON apropiado
4. **Reiniciar Claude Desktop**: Requerido para que los cambios tomen efecto

## Pruebas y Validación {#pruebas-y-validacion}

### Pasos de Verificación

#### 1. Verificar Estado del Servidor MCP
Después de reiniciar Claude Desktop, buscar:
- Icono deslizante en la esquina inferior izquierda de la caja de entrada
- Herramientas disponibles listadas al hacer clic en el deslizante

#### 2. Probar Cada Servidor

**Servidor de Google Search:**
```
Buscar "últimos desarrollos de IA 2025"
```

**Servidor de Gmail:**
```
Muéstrame mis correos recientes de esta semana
```

**Servidor de Brave Search:**
```
Buscar "tendencias de tecnología sostenible" usando Brave
```

**Servidor de Documentos Word:**
```
Crear un nuevo documento de Word con título "MCP Demo" y agregar un párrafo sobre los beneficios de MCP
```

#### 3. Prueba Manual de Servidores
Probar servidores individualmente desde línea de comandos:

```bash
# Probar servidor de Google Search
npx -y @adenot/mcp-google-search

# Probar servidor de Gmail  
npx @gongrzhe/server-gmail-autoauth-mcp

# Probar servidor de Brave Search
npx -y @modelcontextprotocol/server-brave-search

# Probar servidor de Word
uvx --from office-word-mcp-server word_mcp_server
```

### Verificación de Registros

**macOS/Linux:**
```bash
# Verificar registros del servidor
ls -la ~/Library/Application\ Support/Claude/logs/
tail -f ~/Library/Application\ Support/Claude/logs/mcp-server-*.log
```

**Windows:**
```cmd
# Verificar registros en AppData/Claude/logs/
dir %APPDATA%\Claude\logs\
```

## Mejores Prácticas y Seguridad {#mejores-practicas}

### Pautas de Seguridad

#### 1. Gestión de Claves API
- **Nunca confirmar claves API** al control de versiones
- Usar variables de entorno para datos sensibles
- Rotar regularmente las claves API
- Aplicar principio de menor privilegio a permisos API

#### 2. Seguridad de Transporte
Para servidores SSE:
- Siempre usar HTTPS en producción
- Validar headers de Origin
- Implementar autenticación apropiada
- Vincular solo a localhost para desarrollo local

#### 3. Permisos de Servidor
- Claude Desktop ejecuta comandos con los permisos de tu cuenta de usuario y acceso a archivos. Solo agregar comandos si entiendes y confías en la fuente
- Revisar código del servidor antes de la instalación
- Usar entornos sandbox cuando sea posible

### Optimización de Rendimiento

#### 1. Gestión de Recursos
- Monitorear uso de memoria de servidores MCP
- Implementar pooling de conexiones para servidores de alto tráfico
- Usar caché para datos accedidos frecuentemente

#### 2. Selección de Transporte
Mientras que stdio es excelente para desarrollos simples y locales, SSE ofrece más en términos de escalabilidad e interacción en tiempo real, haciéndolo más adecuado para aplicaciones completamente desarrolladas

Elegir basado en tus necesidades:
- **Desarrollo local**: Usar stdio por simplicidad
- **Producción/Remoto**: Usar SSE con seguridad apropiada
- **Alto rendimiento**: Considerar transportes personalizados

## Solución de Problemas {#solucion-de-problemas}

### Problemas Comunes

#### 1. Herramientas MCP No Aparecen
**Síntomas**: Sin icono deslizante o herramientas visibles en Claude Desktop

**Soluciones:**
1. Verificar sintaxis JSON en archivo de configuración
2. Verificar que todas las dependencias requeridas estén instaladas
3. Reiniciar Claude Desktop completamente
4. Verificar claves API y credenciales

#### 2. Fallas de Conexión del Servidor
**Síntomas**: Mensajes de error sobre conectividad del servidor

**Soluciones:**
1. Probar servidores manualmente desde línea de comandos
2. Verificar conectividad de red
3. Verificar configuraciones de firewall
4. Revisar registros del servidor para errores específicos

#### 3. Problemas de Autenticación
**Síntomas**: Errores de "Autenticación fallida" o "No autorizado"

**Soluciones:**
1. Re-ejecutar comandos de autenticación
2. Verificar validez y permisos de clave API
3. Verificar credenciales OAuth y URIs de redirección
4. Verificar cuotas API y estado de facturación

#### 4. Problemas de Node.js/Python
**Síntomas**: Errores de "Comando no encontrado" o errores de módulo

**Soluciones:**
```bash
# Verificar instalación de Node.js
node --version
npm --version

# Verificar instalación de Python  
python --version
uv --version

# Reinstalar si es necesario
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Comandos de Depuración

```bash
# Probar servidores individuales
npx -y @adenot/mcp-google-search --help
npx @gongrzhe/server-gmail-autoauth-mcp --version

# Verificar registros de Claude Desktop
tail -f ~/Library/Application\ Support/Claude/logs/mcp-server-*.log

# Validar configuración JSON
python -m json.tool claude_desktop_config.json
```

### Obtener Ayuda

Si los problemas persisten:
1. Verificar la [guía de depuración MCP](https://modelcontextprotocol.io/quickstart/debugging)
2. Revisar documentación específica del servidor
3. Unirse a las discusiones de la comunidad MCP
4. Reportar problemas a los respectivos repositorios de GitHub

## Recursos Adicionales {#recursos-adicionales}

### Documentación Oficial
- [Especificación del Protocolo de Contexto de Modelo](https://modelcontextprotocol.io/)
- [Anuncio MCP de Anthropic](https://www.anthropic.com/news/model-context-protocol)
- [Guía MCP de Claude Desktop](https://support.anthropic.com/en/articles/10949351-getting-started-with-model-context-protocol-mcp-on-claude-for-desktop)

### Recursos de la Comunidad
- [Repositorio de Servidores MCP](https://github.com/modelcontextprotocol/servers)
- [Comunidad Claude MCP](https://www.claudemcp.com/)
- [MCP Client Boot Starters](https://spring.io/projects/spring-ai)

### Herramientas de Desarrollo
- [Herramienta Inspector MCP](https://github.com/modelcontextprotocol/inspector) - Depurar servidores MCP
- [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) - Puente entre transportes SSE y stdio
- [MCP Remote](https://github.com/modelcontextprotocol/mcp-remote) - Adaptador para servidores MCP remotos

### Proyectos de Ejemplo
- [Tutorial MCP de DataCamp](https://www.datacamp.com/tutorial/mcp-model-context-protocol) - Servidor de Revisión de PR
- [Tutorial de Servidor del Clima](https://modelcontextprotocol.io/quickstart/server) - Implementación básica de servidor MCP

### Documentación de APIs
- [API de Búsqueda Personalizada de Google](https://developers.google.com/custom-search/v1/overview)
- [API de Gmail](https://developers.google.com/gmail/api/guides)
- [API de Brave Search](https://api.search.brave.com/app/documentation)

---

## Conclusión

Esta guía completa cubre la configuración e instalación de múltiples servidores MCP con Claude AI, demostrando el poder y flexibilidad del Protocolo de Contexto de Modelo. MCP proporciona un estándar universal y abierto para conectar sistemas de IA con fuentes de datos, reemplazando integraciones fragmentadas con un protocolo único, habilitando interacciones de IA más inteligentes y conscientes del contexto.

La combinación de servidores de Google Search, Gmail, Brave Search y documentos Word muestra cómo MCP puede conectar Claude a varios servicios y herramientas externos, expandiendo significativamente sus capacidades más allá de la generación de texto para incluir búsqueda web, gestión de correo electrónico y creación de documentos.

Recuerda priorizar la seguridad, seguir las mejores prácticas y actualizar regularmente tus servidores MCP y la aplicación Claude Desktop para beneficiarte de las últimas características y mejoras de seguridad.

**Próximos Pasos:**
1. Experimentar con los servidores configurados
2. Explorar servidores MCP adicionales del repositorio de la comunidad
3. Considerar desarrollar servidores MCP personalizados para tus necesidades específicas
4. Compartir tus experiencias con la comunidad MCP

---

*Esta guía representa el estado actual de la tecnología MCP al mayo de 2025. El ecosistema MCP está evolucionando rápidamente, así que verifica la documentación oficial para las últimas actualizaciones y características.*