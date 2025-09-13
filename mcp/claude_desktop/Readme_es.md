# Claude Desktop Application

## 🚀 Introducción

**Claude Desktop** es una aplicación nativa que lleva toda la potencia de Claude AI directamente a tu escritorio. Con rendimiento mejorado, soporte completo del **Protocolo de Contexto de Modelo (MCP)** y funciones avanzadas de productividad, Claude Desktop transforma tu flujo de trabajo con IA.

### ✨ ¿Por qué Claude Desktop?

- **🔌 Integración MCP**: Conecta Claude con herramientas externas y fuentes de datos
- **⚡ Rendimiento Nativo**: Velocidad y eficiencia superiores a la versión web
- **🎯 Proyectos Avanzados**: Contexto persistente de 200K tokens (~500 páginas)
- **🔗 Integración del Sistema**: Atajos globales y acceso directo al sistema de archivos
- **🛠️ Herramientas Integradas**: Análisis de código, captura de pantalla y más

## 📋 Requisitos del Sistema

### Windows
- **SO**: Windows 10 (64-bit) o posterior
- **RAM**: 16 GB mínimo (32 GB+ recomendado)
- **Almacenamiento**: SSD con 100+ GB libres
- **Extras**: Node.js para funcionalidad MCP

### macOS
- **SO**: macOS 11 (Big Sur) o posterior
- **Procesador**: Apple Silicon o Intel
- **RAM**: 16 GB mínimo (32 GB+ recomendado)
- **Almacenamiento**: SSD con 100+ GB libres

### Linux (Soporte Comunitario)
- **Distribuciones**: Ubuntu 20.04+, Debian 10+, Fedora, Arch Linux
- **Nota**: Sin soporte oficial de Anthropic

## 🔧 Instalación

### Windows
1. Descarga el instalador desde [claude.ai/download](https://claude.ai/download)
2. Ejecuta `ClaudeSetup.exe`
3. Sigue el asistente de instalación
4. Inicia sesión con tu cuenta de Claude

### macOS
1. Descarga `Claude.dmg` desde [claude.ai/download](https://claude.ai/download)
2. Arrastra Claude a la carpeta Aplicaciones
3. Abre desde Aplicaciones (puede requerir aprobación de seguridad)
4. Inicia sesión con tu cuenta

### Linux (Comunidad)
```bash
# Debian/Ubuntu
git clone https://github.com/aaddrick/claude-desktop-debian.git
cd claude-desktop-debian
./build.sh
sudo dpkg -i ./claude-desktop_VERSION_ARCHITECTURE.deb
```

## 🎮 Funciones Principales

### Capacidades Esenciales
- **Multi-modelo**: Claude 3.5 Sonnet, Haiku y Opus
- **Manejo de archivos**: Documentos, imágenes, PDFs (hasta 30MB)
- **Artefactos interactivos**: Contenido dinámico y editable
- **Dictado por voz**: Comunicación natural con Claude
- **Herramientas integradas**: Análisis, captura de pantalla

### Atajos de Teclado
- **Acceso global**: `Option + Espacio` (macOS) / `Ctrl + Alt + Espacio` (Windows)
- **Nuevo chat**: `Ctrl/Cmd + K`
- **Enviar mensaje**: `Enter`
- **Nueva línea**: `Shift + Enter`

## 🔌 Protocolo de Contexto de Modelo (MCP)

### ¿Qué es MCP?
MCP es el **"puerto USB para IA"** - un estándar abierto que permite a Claude conectarse de forma segura con herramientas externas, bases de datos y servicios.

### Configuración Básica

1. **Prerrequisitos**: Node.js 16+ instalado
2. **Acceder a configuración**: `Menú Claude → Configuración → Desarrollador → Editar Config`
3. **Ubicación del archivo**:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Ejemplo de Configuración
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop",
        "/Users/username/Documents"
      ]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "tu_token_aquí"
      }
    }
  }
}
```

### Servidores MCP Disponibles

#### Oficiales
- **Filesystem**: Operaciones de archivos locales
- **GitHub**: Gestión de repositorios
- **Slack**: Comunicación de equipos
- **Google Drive**: Acceso a almacenamiento en la nube
- **PostgreSQL**: Operaciones de base de datos
- **Puppeteer**: Automatización de navegador

#### Comunitarios
- AWS, Docker, MongoDB, Notion, Discord, Firebase, Kubernetes, y más

## 📁 Proyectos (Pro/Team/Enterprise)

### Características
- **Contexto masivo**: 200K tokens (~500 páginas)
- **Instrucciones personalizadas**: Comportamiento específico por proyecto
- **Base de conocimiento**: Documentos persistentes
- **Colaboración**: Compartir con equipos

### Creación de Proyectos
1. Clic en **"Proyectos"** (esquina superior izquierda)
2. **"Nuevo Proyecto"**
3. Nombre, descripción y configuración
4. Cargar documentos (PDF, DOCX, CSV, etc.)

### Ejemplo de Instrucciones Personalizadas
```
Rol: Desarrollador Senior de Python
Enfoque: Código limpio y eficiente con documentación integral
Estilo: Profesional pero accesible
Salida: Incluir type hints y docstrings
```

## 🆚 Desktop vs Web

| Función | Desktop | Web |
|---------|---------|-----|
| Integración MCP | ✅ | ❌ |
| Rendimiento Nativo | ✅ | ❌ |
| Atajos Globales | ✅ | ❌ |
| Acceso Sistema Archivos | ✅ | Limitado |
| Proyectos Avanzados | ✅ | ✅ |
| Computer Use | ❌ | ✅ |

## 🛠️ Mejores Prácticas

### Selección de Modelo
- **Haiku**: Tareas simples y rápidas
- **Sonnet**: Rendimiento equilibrado (recomendado)
- **Opus**: Razonamiento complejo

### Optimización MCP
1. Comenzar con acceso al sistema de archivos
2. Agregar servidores gradualmente
3. Usar rutas absolutas en configuración
4. Monitorear impacto en rendimiento

### Flujo de Trabajo Eficiente
- Agrupar tareas relacionadas
- Usar atajos de teclado
- Organizar con Proyectos
- Crear plantillas para patrones comunes

## 🔧 Solución de Problemas

### Problemas Comunes

#### MCP no conecta
```bash
# Verificar Node.js
node --version

# Validar JSON
# Usar rutas absolutas
# Reiniciar Claude después de cambios
```

#### Rendimiento lento
- Verificar recursos del sistema
- Reducir servidores MCP activos
- Limpiar caché de aplicación
- Actualizar a la última versión

#### macOS bloquea la app
```
Preferencias del Sistema → Seguridad y Privacidad → General → "Abrir de Todos Modos"
```

## 📞 Soporte

- **Estado del servicio**: [status.anthropic.com](https://status.anthropic.com)
- **Soporte oficial**: [support.anthropic.com](https://support.anthropic.com)
- **Documentación API**: [docs.anthropic.com](https://docs.anthropic.com)
- **Comunidad**: r/ClaudeAI, r/AnthropicAI

## 🚀 Próximos Pasos

1. **Instalar Claude Desktop**
2. **Configurar MCP básico** (filesystem)
3. **Crear tu primer Proyecto**
4. **Explorar servidores MCP** adicionales
5. **Optimizar tu flujo de trabajo**

---

**Claude Desktop** - Lleva tu productividad con IA al siguiente nivel 🚀