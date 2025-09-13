# Chatbot Potenciado por MCP: Neo4j y HubSpot

Una aplicación sofisticada de IA conversacional que conecta **bases de datos de grafos Neo4j** y **CRM de HubSpot** a través del **Protocolo de Contexto de Modelo (MCP)**, construida con **Chainlit** para una interfaz de chat intuitiva.

## 🌟 Descripción General

Esta aplicación demuestra el poder de combinar múltiples fuentes de datos a través de servidores MCP, permitiendo a los usuarios consultar y analizar datos de bases de datos de grafos Neo4j y sistemas CRM de HubSpot usando conversaciones en lenguaje natural.

### Características Principales

- 🗃️ **Integración con Neo4j**: Consulta bases de datos de grafos con lenguaje natural
- 🏢 **Acceso a CRM de HubSpot**: Gestiona contactos, empresas, tratos y más
- 🔄 **Análisis Entre Sistemas**: Encuentra conexiones entre datos de Neo4j y HubSpot
- 🤖 **Exploración Inteligente**: La IA explora automáticamente estructuras de datos y encuentra información relevante
- 💬 **Interfaz de Lenguaje Natural**: Potenciada por Chainlit para una experiencia de usuario fluida
- 🔧 **Arquitectura Flexible**: Fácil de extender con servidores MCP adicionales

## 🏗️ Stack Tecnológico

### Tecnologías Principales

#### Protocolo de Contexto de Modelo (MCP)
**¿Qué es MCP?**
- Un protocolo estandarizado para conectar asistentes de IA a fuentes de datos y herramientas externas
- Desarrollado por Anthropic para permitir interacciones seguras y estructuradas entre modelos de IA y varios sistemas
- Proporciona una interfaz uniforme para acceder a bases de datos, APIs y otros servicios

**¿Por qué MCP?**
- **Seguridad**: Acceso controlado a sistemas externos
- **Estandarización**: Interfaz consistente entre diferentes fuentes de datos
- **Extensibilidad**: Fácil agregar nuevas herramientas y fuentes de datos
- **Seguridad de Tipos**: Esquemas estructurados para intercambio confiable de datos

#### Chainlit
**¿Qué es Chainlit?**
- Un framework de Python para construir aplicaciones de IA conversacional
- Proporciona interfaces de chat, respuestas en streaming y gestión de sesiones
- Optimizado para flujos de trabajo de IA/ML e integraciones

**¿Por qué Chainlit?**
- **Desarrollo Rápido**: Configuración rápida para interfaces de chat
- **Soporte de Streaming**: Streaming de respuestas en tiempo real
- **Gestión de Sesiones**: Maneja sesiones de usuario e historial de mensajes
- **UI Personalizable**: Personalización flexible de la interfaz

### Fuentes de Datos

#### Base de Datos de Grafos Neo4j
- **Propósito**: Almacenar y consultar relaciones complejas entre entidades
- **Casos de Uso**: Análisis de redes, sistemas de recomendación, detección de fraude
- **Lenguaje de Consulta**: Cypher para consultas expresivas de grafos

#### CRM de HubSpot
- **Propósito**: Gestión de relaciones con clientes y seguimiento de pipeline de ventas
- **Casos de Uso**: Gestión de contactos, seguimiento de tratos, automatización de marketing
- **Integración**: Acceso a API REST a través de servidor MCP

## 🚀 Primeros Pasos

### Prerequisitos

- **Python 3.11+**
- **Node.js** (para servidor MCP de HubSpot)
- **uvx** (para gestión de paquetes de Python)
- **Base de Datos Neo4j** (local o Neo4j Aura)
- **Cuenta de HubSpot** con token de acceso de App Privada

### Instalación

1. **Clonar el repositorio**
```bash
git clone <url-de-tu-repo>
cd mcp-neo4j-client
```

2. **Instalar dependencias de Python**
```bash
pip install -r requirements.txt
```

3. **Instalar herramientas MCP**
```bash
# Instalar uvx para servidores MCP de Python
pip install uvx

# Instalar dependencias de Node.js (para HubSpot)
npm install -g @hubspot/mcp-server
```

4. **Configurar variables de entorno**
```bash
cp .env.template .env
# Editar .env con tus credenciales
```

### Configuración del Entorno

Crear un archivo `.env` con las siguientes variables:

```env
# Configuración de Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://tu-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=tu-api-key
AZURE_OPENAI_MODEL=gpt-4o
OPENAI_API_VERSION=2024-08-01-preview

# Configuración de Neo4j
NEO4J_URI=neo4j+s://tu-id.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=tu-contraseña
NEO4J_DATABASE=neo4j

# Configuración de HubSpot
HUBSPOT_PRIVATE_APP_TOKEN=tu-token-hubspot
```

### Ejecutar la Aplicación

1. **Verificar configuración**
```bash
python test_hubspot.py
```

2. **Iniciar la aplicación**
```bash
chainlit run app.py --port 8080 --host 0.0.0.0
```

3. **Acceder a la interfaz**
Abrir tu navegador en `http://localhost:8080`

## 🔧 Arquitectura

### Arquitectura del Sistema

```
┌─────────────────┐    ┌───────────────────┐    ┌──────────────────┐
│   UI Chainlit   │    │   App Python      │    │  Azure OpenAI    │
│                 │◄──►│                   │◄──►│                  │
│ - Interfaz Chat │    │ - Enrutamiento    │    │ - Procesamiento  │
│ - Streaming     │    │ - Integración MCP │    │   LLM            │
│ - Gestión Sesión│    │ - Gestión Resp.   │    │ - Llamadas Herram│
└─────────────────┘    └───────────────────┘    └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Cliente MCP    │
                       │                  │
                       │ - Gestión Serv.  │
                       │ - Validación     │
                       │ - Corrección Esq.│
                       └──────────────────┘
                         │              │
                         ▼              ▼
              ┌─────────────────┐  ┌─────────────────┐
              │  MCP Neo4j      │  │ MCP HubSpot     │
              │                 │  │                 │
              │ - Consultas     │  │ - Operaciones   │
              │   Cypher        │  │   CRM           │
              │ - Info Esquema  │  │ - Llamadas API  │
              │ - Leer/Escribir │  │ - Gestión Obj.  │
              └─────────────────┘  └─────────────────┘
                         │              │
                         ▼              ▼
              ┌─────────────────┐  ┌─────────────────┐
              │   BD Neo4j      │  │   API HubSpot   │
              │                 │  │                 │
              │ - Datos Grafo   │  │ - Datos CRM     │
              │ - Relaciones    │  │ - Contactos     │
              │ - Propiedades   │  │ - Empresas      │
              └─────────────────┘  └─────────────────┘
```

### Componentes Clave

#### 1. **MCPClient** (`mcp_client.py`)
- Gestiona conexiones a múltiples servidores MCP
- Valida y corrige esquemas de herramientas para compatibilidad con OpenAI
- Maneja limpieza asíncrona y gestión de errores

#### 2. **ChatClient** (`app.py`)
- Gestiona el flujo de conversación con Azure OpenAI
- Maneja llamadas de herramientas y streaming de respuestas
- Mantiene contexto de conversación y memoria

#### 3. **Servidores MCP**
- **Servidor Neo4j**: Proporciona ejecución de consultas Cypher y acceso a esquemas
- **Servidor HubSpot**: Ofrece operaciones CRM comprehensivas

### Validación de Esquemas de Herramientas

La aplicación incluye validación sofisticada de esquemas que:
- Corrige propiedades `items` faltantes en esquemas de arrays
- Elimina propiedades problemáticas de JSON Schema
- Asegura compatibilidad con llamadas de función de OpenAI
- Proporciona reportes detallados de errores

## 🔍 Ejemplos de Uso

### Consultas Neo4j

**Explorar estructura de tu base de datos:**
```
"¿Qué hay en mi base de datos Neo4j?"
```

**Encontrar relaciones específicas:**
```
"Muéstrame todos los cirujanos y sus sesiones relacionadas"
```

**Análisis complejo:**
```
"¿Cuáles son las relaciones más comunes en mi grafo?"
```

### Operaciones HubSpot

**Explorar datos CRM:**
```
"Muéstrame mis contactos de HubSpot"
```

**Buscar y filtrar:**
```
"Encuentra todas las empresas del sector tecnológico"
```

**Crear y actualizar:**
```
"Crea un nuevo contacto para Juan Pérez en Acme Corp"
```

### Análisis Entre Sistemas

**Correlación de datos:**
```
"Compara mis datos de usuarios de Neo4j con contactos de HubSpot"
```

**Oportunidades de enriquecimiento:**
```
"¿Qué entidades de Neo4j podrían mejorarse con datos de HubSpot?"
```

## 🛠️ Desarrollo

### Estructura del Proyecto

```
mcp-neo4j-client/
├── app.py                 # Aplicación principal Chainlit
├── mcp_client.py          # Implementación cliente MCP
├── mcp_config.json        # Configuraciones servidor MCP
├── main.py                # Interfaz cliente alternativa
├── requirements.txt       # Dependencias Python
├── pyproject.toml         # Configuración proyecto
├── .env                   # Variables entorno
├── test_*.py              # Utilidades pruebas
└── README.md              # Este archivo
```

### Pruebas

La aplicación incluye utilidades de prueba comprehensivas:

```bash
# Probar conexión Neo4j
python test_neo4j.py

# Probar conexiones MCP
python test_mcp.py

# Probar validación esquemas
python test_schema.py

# Verificación comprehensiva
python test_hubspot.py
```

### Agregar Nuevos Servidores MCP

1. **Actualizar configuración** (`mcp_config.json`):
```json
{
  "mcpServers": {
    "tu-nuevo-servidor": {
      "command": "tu-comando",
      "args": ["arg1", "arg2"],
      "env": {
        "API_KEY": "${TU_API_KEY}"
      }
    }
  }
}
```

2. **Agregar variables de entorno** (`.env`):
```env
TU_API_KEY=valor-de-tu-api-key
```

3. **La aplicación automáticamente**:
   - Se conectará al nuevo servidor
   - Validará y corregirá esquemas de herramientas
   - Hará las herramientas disponibles para la IA

## 🔧 Configuración

### Configuración de Servidores MCP

El archivo `mcp_config.json` define cómo conectarse a servidores MCP:

```json
{
  "mcpServers": {
    "neo4j": {
      "command": "uvx",
      "args": ["mcp-neo4j-cypher@0.2.1"],
      "env": {
        "NEO4J_URI": "${NEO4J_URI}",
        "NEO4J_USERNAME": "${NEO4J_USERNAME}",
        "NEO4J_PASSWORD": "${NEO4J_PASSWORD}",
        "NEO4J_DATABASE": "${NEO4J_DATABASE}"
      }
    },
    "hubspot": {
      "command": "npx",
      "args": ["-y", "@hubspot/mcp-server"],
      "env": {
        "PRIVATE_APP_ACCESS_TOKEN": "${HUBSPOT_PRIVATE_APP_TOKEN}"
      }
    }
  }
}
```

### Prompts del Sistema

La aplicación usa un prompt de sistema inteligente que:
- Fomenta el análisis exploratorio de datos
- Promueve coincidencias flexibles y consultas inclusivas
- Guía la correlación de datos entre sistemas
- Enfatiza entender los datos antes de consultarlos

## 🚨 Solución de Problemas

### Problemas Comunes

#### 1. **Fallas de Conexión MCP**
```bash
# Ejecutar diagnósticos comprehensivos
python test_hubspot.py
```

#### 2. **Problemas de Conexión Neo4j**
- Verificar credenciales de Neo4j Aura
- Revisar formato URI: `neo4j+s://xxxxx.databases.neo4j.io`
- Probar conexión: `python test_neo4j.py`

#### 3. **Problemas API HubSpot**
- Verificar permisos del token de App Privada
- Asegurar que Node.js esté instalado para `npx`
- Revisar requerimientos de alcance del token

#### 4. **Errores de Esquemas de Herramientas**
- La aplicación corrige automáticamente la mayoría de problemas de esquemas
- Revisar salida de consola para advertencias de validación
- Ejecutar: `python test_schema.py`

### Scripts de Debug

- `debug_mcp.py`: Diagnosticar problemas MCP Neo4j
- `test_workflow.py`: Demostrar patrones de consulta flexibles
- `setup.py`: Verificar configuración completa del entorno

## 🔐 Consideraciones de Seguridad

- **Variables de Entorno**: Mantener credenciales sensibles en archivos `.env`
- **Aislamiento MCP**: Cada servidor MCP ejecuta en procesos aislados
- **Validación de Esquemas**: Previene llamadas de herramientas malformadas
- **Manejo de Errores**: Manejo elegante de fallas de conexión

## 🚀 Características Avanzadas

### Construcción Inteligente de Consultas

La IA automáticamente:
1. **Explora esquemas** antes de construir consultas
2. **Usa coincidencias flexibles** (CONTAINS, insensible a mayúsculas)
3. **Encuentra variaciones** de términos de búsqueda
4. **Construye consultas inclusivas** que capturan datos relacionados

### Manejo de Errores Asíncronos

- Supresión dirigida de errores de limpieza asíncrona
- Degradación elegante cuando servidores no están disponibles
- Intentos automáticos de reconexión

### Compatibilidad de Esquemas

- Corrección automática de problemas de llamadas de función OpenAI
- Soporte para esquemas anidados complejos
- Validación y reporte de errores

## 📈 Optimización de Rendimiento

- **Pool de Conexiones**: Reutiliza conexiones MCP
- **Cache de Esquemas**: Evita validación repetida de esquemas
- **Respuestas en Streaming**: Retroalimentación en tiempo real al usuario
- **Limpieza Dirigida**: Overhead asíncrono mínimo

## 🤝 Contribuir

1. Hacer fork del repositorio
2. Crear una rama de característica
3. Agregar pruebas para nueva funcionalidad
4. Asegurar que todas las pruebas pasen
5. Enviar un pull request

## 📄 Licencia

[Agregar información de tu licencia aquí]

## 🙏 Reconocimientos

- **Anthropic** por el Protocolo de Contexto de Modelo
- **Chainlit** por el framework de IA conversacional
- **Neo4j** por la tecnología de base de datos de grafos
- **HubSpot** por las capacidades de integración CRM

---

*Esta aplicación demuestra el poder de conectar asistentes de IA a fuentes de datos del mundo real a través de protocolos estandarizados, habilitando análisis sofisticado de datos a través de conversaciones en lenguaje natural.*