# Plataforma de Integración MCP de Búsqueda Impulsada por IA

Una aplicación integral que proporciona interacciones impulsadas por IA con Google Search y Perplexity AI a través de servidores Model Context Protocol (MCP). Esta plataforma permite búsqueda web sin interrupciones, análisis impulsado por IA y extracción de contenido con seguridad HTTPS opcional, autenticación de usuarios y caching avanzado para rendimiento óptimo.

## 🚀 Resumen del Sistema

Esta aplicación consta de tres componentes integrados que trabajan juntos para proporcionar capacidades completas de búsqueda impulsada por IA:

1. **Cliente Streamlit** - Interfaz de chat IA con soporte multi-proveedor, autenticación, soporte SSL y servidor MCP integrado
2. **Google Search MCP Server** - Búsqueda web y extracción de contenido vía Google Custom Search API con caching inteligente
3. **Perplexity MCP Server** - Búsqueda impulsada por IA con análisis inteligente vía Perplexity API con caching de respuestas

## 🏗️ Arquitectura del Sistema

![AI-Powered Search MCP Platform Architecture](./docs/mcp_platform_architecture.svg)

La plataforma integra cuatro capas principales:
- **User Layer**: Autenticación, interfaz Streamlit, proveedores IA, memoria de chat
- **AI Orchestration Layer**: Agentes LangChain, selección de herramientas, prompt engineering, seguridad
- **MCP Protocol Layer**: Comunicación Server-Sent Events con servidores Google Search, Perplexity y Company Tagging
- **External Data Sources**: Google APIs, Perplexity AI, servicios OpenAI/Azure AI

## 📋 Tabla de Referencia de Puertos

| Servicio | Puerto | Protocolo | Propósito |
|----------|--------|-----------|-----------|
| **Streamlit HTTP** | 8501 | HTTP | Interfaz web principal |
| **Streamlit HTTPS** | 8503 | HTTPS | Interfaz web segura (recomendado) |
| **Google Search MCP** | 8002 | HTTP/SSE | Servidor de búsqueda web con caching |
| **Perplexity MCP** | 8001 | HTTP/SSE | Servidor de búsqueda IA con caching |
| **Company Tagging** | - | stdio | Servidor MCP integrado |

## 🔧 Tecnologías Principales y Dependencias

Esta plataforma está construida utilizando tecnologías modernas y robustas que habilitan capacidades escalables de búsqueda impulsada por IA con caching inteligente para rendimiento óptimo.

### **🌐 Frontend e Interfaz de Usuario**

#### **[Streamlit](https://streamlit.io/)** - Framework de Aplicaciones Web
- **Propósito**: Interfaz web principal para interacciones de usuario
- **Versión**: 1.44+
- **Características**: Actualizaciones en tiempo real, sistema de componentes, gestión de sesiones
- **Mejorado**: Interfaz multi-pestaña con configuración, conexiones, herramientas y chat

#### **[Streamlit Authenticator](https://github.com/mkhorasani/Streamlit-Authenticator)** - Sistema de Autenticación
- **Propósito**: Inicio de sesión seguro y gestión de sesiones de usuario
- **Versión**: 0.3.2
- **Características**: Hash de contraseñas bcrypt, control de acceso basado en roles, persistencia de sesión de 30 días

### **🧠 IA y Modelos de Lenguaje**

#### **[LangChain](https://python.langchain.com/)** - Framework de IA
- **Propósito**: Orquestación de agentes IA y enrutamiento de herramientas
- **Versión**: 0.3.20+
- **Características**: Agentes ReAct, gestión de memoria, ejecución de herramientas, historial de conversaciones

#### **[OpenAI API](https://openai.com/api/)** - Modelos de Lenguaje IA
- **Modelos**: GPT-4o, GPT-4o-mini
- **Características**: Tool calling, respuestas en streaming, manejo de contexto

#### **[Azure OpenAI](https://azure.microsoft.com/es-es/products/ai-services/openai-service)** - IA Empresarial
- **Modelos**: GPT-4o, o3-mini
- **Características**: Seguridad empresarial, endpoints privados, cumplimiento, garantías SLA

#### **Soporte Mejorado de Proveedores IA** (Enhanced Mode)
- **Anthropic Claude**: Claude 3.5 Sonnet, Claude 3 Haiku, Claude 3 Opus
- **Google Gemini**: Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini Pro
- **Cohere**: Command R+, Command R, Command
- **Mistral AI**: Mistral Large, Medium, Small
- **Ollama (Local)**: Soporte para despliegue de modelos locales

### **🔍 Búsqueda y Fuentes de Datos**

#### **[Google Custom Search API](https://developers.google.com/custom-search)** - Motor de Búsqueda Web
- **Propósito**: Capacidades completas de búsqueda web con caching inteligente
- **Versión**: v1
- **Caching**: TTL de 30 minutos para resultados de búsqueda, TTL de 2 horas para contenido de páginas web
- **Características**: Motores de búsqueda personalizados, filtrado de resultados, optimización de extracción de contenido

#### **[Perplexity AI API](https://www.perplexity.ai/)** - Búsqueda Impulsada por IA
- **Modelos**: sonar-deep-research, sonar-reasoning-pro, sonar-reasoning, sonar-pro, sonar, r1-1776
- **Caching**: TTL de 30 minutos para respuestas de API
- **Características**: Filtrado de actualidad, selección de modelo, soporte de citas, control de temperatura

### **🔗 Protocolos de Comunicación**

#### **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)** - Comunicación IA Estandarizada
- **Propósito**: Protocolo universal para integración de herramientas IA
- **Versión**: 1.0+
- **Características**: Descubrimiento de herramientas, validación de esquemas, flexibilidad de transporte (SSE + stdio)

#### **[Server-Sent Events (SSE)](https://developer.mozilla.org/es/docs/Web/API/Server-sent_events)** - Comunicación en Tiempo Real
- **Propósito**: Comunicación bidireccional en tiempo real para servidores MCP externos
- **Características**: Reconexión automática, orden de mensajes, multiplexación

#### **stdio Transport** - Comunicación de Procesos Locales
- **Propósito**: Comunicación de servidor MCP integrado dentro de contenedores
- **Características**: Latencia de red cero, despliegue simplificado, mejor seguridad

### **🐳 Infraestructura y Despliegue**

#### **[Docker](https://www.docker.com/)** - Plataforma de Contenerización
- **Propósito**: Despliegue consistente a través de entornos
- **Características**: Orquestación multi-contenedor, chequeos de salud, montaje de volúmenes

#### **[Docker Compose](https://docs.docker.com/compose/)** - Orquestación Multi-Contenedor
- **Propósito**: Despliegue coordinado de múltiples servicios
- **Características**: Escalado de servicios, gestión de configuración, logging

### **🔒 Tecnologías de Seguridad**

#### **[bcrypt](https://github.com/pyca/bcrypt/)** - Hash de Contraseñas
- **Propósito**: Almacenamiento y validación segura de contraseñas
- **Características**: Hash adaptativo, costo configurable, resistencia a ataques de temporización

#### **[OpenSSL](https://www.openssl.org/)** - Encriptación SSL/TLS
- **Propósito**: Soporte HTTPS y generación de certificados
- **Características**: Certificados autofirmados, generación de claves, encriptación

## ⚡ Inicio Rápido

### Prerrequisitos
- Docker & Docker Compose
- Clave API de Google Custom Search e ID del Motor de Búsqueda
- Clave API de Perplexity
- Clave API de OpenAI o configuración de Azure OpenAI

### 1. Configuración del Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Configuración del Proveedor IA (elige uno)
OPENAI_API_KEY=tu_clave_api_openai_aqui

# O Configuración de Azure OpenAI
AZURE_API_KEY=tu_clave_api_azure
AZURE_ENDPOINT=https://tu-endpoint.openai.azure.com/
AZURE_DEPLOYMENT=tu_nombre_despliegue
AZURE_API_VERSION=2023-12-01-preview

# Configuración de Google Search
GOOGLE_API_KEY=tu_clave_api_google
GOOGLE_SEARCH_ENGINE_ID=tu_id_motor_busqueda_personalizada

# Configuración de Perplexity
PERPLEXITY_API_KEY=tu_clave_api_perplexity
PERPLEXITY_MODEL=sonar

# Configuración SSL (Opcional)
SSL_ENABLED=true
```

### 2. Configuración de APIs

#### Configuración de Google Custom Search
1. **Obtener Clave API**: Ve a [Google Cloud Console](https://console.cloud.google.com/), habilita Custom Search API, crea credenciales
2. **Crear Custom Search Engine**: Ve a [Google Custom Search](https://cse.google.com/cse/), crea nuevo motor de búsqueda, obtén Search Engine ID

#### Configuración de API de Perplexity
1. **Obtener Clave API**: Regístrate en [Perplexity AI](https://perplexity.ai) y obtén tu clave API
2. **Elegir Modelo**: Selecciona de los modelos disponibles (sonar, sonar-pro, sonar-reasoning, etc.)

### 3. Configuración de Autenticación de Usuario

Genera credenciales de usuario para la aplicación:

```bash
cd client
python simple_generate_password.py
```

Esto crea `keys/config.yaml` con usuarios predeterminados. Puedes modificar las credenciales de usuario según sea necesario.

### 4. Configuración de Certificado SSL (Opcional)

Para soporte HTTPS, los certificados se generarán automáticamente cuando `SSL_ENABLED=true`.

### 5. Lanzar la Plataforma

```bash
# Construir e iniciar todos los servicios
docker-compose up --build

# O iniciar servicios individuales
docker-compose up mcpserver1    # Perplexity MCP Server (con caching)
docker-compose up mcpserver2    # Google Search MCP Server (con caching)
docker-compose up hostclient    # Streamlit Client (con MCP stdio integrado)
```

### 6. Acceder a la Aplicación

#### Modo HTTPS (Recomendado)
- **Interfaz Principal**: https://localhost:8503
- **Seguridad**: Certificado autofirmado (acepta advertencia del navegador)

#### Modo HTTP (Predeterminado)
- **Interfaz Principal**: http://localhost:8501
- **Alternativa**: http://127.0.0.1:8501

#### Chequeos de Salud y Monitoreo
- **Google Search Server**: http://localhost:8002/health
- **Perplexity Server**: http://localhost:8001/health
- **Estadísticas Detalladas de Google Search**: http://localhost:8002/health/detailed
- **Limpiar Google Search Cache**: http://localhost:8002/cache/clear

#### Autenticación
Usa las credenciales generadas en el paso 3 (predeterminado: admin/very_Secure_p@ssword_123!)

## 🎯 Características Principales

### **Sistema de Caching Inteligente** ⭐ NUEVO
- **Google Search Cache**: TTL de 30 minutos para resultados de búsqueda, TTL de 2 horas para contenido de páginas web
- **Perplexity Cache**: TTL de 30 minutos para respuestas de IA
- **Gestión de Cache**: Herramientas incorporadas para limpieza de cache y estadísticas
- **Rendimiento**: Reducción significativa en el uso de API y mejores tiempos de respuesta
- **Limpieza Automática**: Entradas expiradas limpiadas automáticamente

### **Seguridad de Nivel Empresarial**
- **Sistema de Autenticación de Usuario**: Hash de contraseñas bcrypt con gestión de sesiones
- **Soporte SSL/HTTPS**: Certificados auto-firmados con generación automática
- **Control de Acceso Basado en Roles**: Dominios de email pre-autorizados y validación de usuarios
- **Gestión Segura de Cookies**: Autenticación configurable con claves personalizadas

### **Integración Avanzada de IA**
- **Soporte Multi-Proveedor**: OpenAI GPT-4o, Azure OpenAI, y sistema de proveedores extensible
- **Configuración Mejorada**: Soporte para Anthropic Claude, Google Gemini, Cohere, Mistral AI, y Ollama
- **Framework de Agente LangChain**: Selección y ejecución inteligente de herramientas
- **Memoria de Conversación**: Historial de chat persistente con conciencia de contexto

### **Integración Dual de Motores de Búsqueda**
- **Herramientas de Google Search**: Búsqueda web completa y extracción de contenido con caching
- **Herramientas de Perplexity AI**: Búsqueda impulsada por IA con análisis inteligente y caching
- **Soporte multi-proveedor de IA** (OpenAI, Azure OpenAI con configuración mejorada)
- **Selección inteligente de herramientas** basada en tipo de consulta y requisitos

### **Capacidades Avanzadas de Búsqueda**

#### **Operaciones de Google Search (4 Herramientas)** - Mejoradas con Caching
- **google-search**: Integración de Google Custom Search API con caching de 30 minutos
- **read-webpage**: Extracción limpia de contenido de páginas web con caching de 2 horas
- **clear-cache**: Herramienta de gestión de cache para limpiar cache de búsqueda y páginas web
- **cache-stats**: Herramienta de monitoreo para rendimiento de cache y estadísticas

#### **Operaciones de Perplexity AI (5 Herramientas)** - Mejoradas con Caching
- **perplexity_search_web**: Búsqueda web estándar impulsada por IA con caching de 30 minutos
- **perplexity_advanced_search**: Búsqueda avanzada con parámetros de modelo personalizados y caching
- **search_show_categories**: Acceso a taxonomía completa basada en CSV
- **tag_company**: Investigación avanzada de empresas y etiquetado de taxonomía para expositores de ferias comerciales
- **clear_api_cache**: Gestión de cache para respuestas de API de Perplexity
- **get_cache_stats**: Estadísticas de cache y monitoreo de rendimiento

#### **Operaciones de Company Tagging (Servidor MCP stdio Integrado)**
- **search_show_categories**: Servidor MCP especializado basado en stdio para análisis de expositores de ferias comerciales
- **Gestión de Taxonomía**: Acceso a categorías estructuradas de industria/producto para 5 ferias comerciales principales
- **Acceso a Datos CSV**: Acceso en tiempo real a datos de categorías con filtrado y capacidades de búsqueda
- **Flujo de Trabajo Integrado**: Análisis sin interrupciones de empresas usando tanto herramientas de Google Search como de Perplexity

### **Excelencia Técnica**
- **Arquitectura Moderna**: Transporte SSE + stdio MCP con autenticación completa
- **Contenerización Docker**: Despliegue y escalado fácil con 3 servicios
- **Soporte SSL/HTTPS**: Conexiones seguras con generación automática de certificados
- **Comunicación en Tiempo Real**: Server-Sent Events (SSE) para servidores MCP externos
- **Integración Stdio**: Servidor MCP de Company Tagging integrado para flujos de trabajo especializados
- **Caching Inteligente**: Sistema de cache multi-capa para rendimiento óptimo
- **Monitoreo de Salud**: Chequeos de salud incorporados y monitoreo de cache para todos los servicios

## 📚 Herramientas y Capacidades Disponibles

### **Total de Herramientas Disponibles: 10 Herramientas**

#### **Google Search MCP Server (4 Herramientas)** - Con Caching Inteligente
1. **google-search**
   - Realizar búsquedas de Google con 1-10 resultados configurables
   - **Caching**: TTL de 30 minutos para consultas de búsqueda idénticas
   - Devuelve títulos, enlaces, fragmentos y conteos totales de resultados
   - Información de acierto/fallo de cache incluida en respuestas

2. **read-webpage**
   - Extraer contenido limpio de cualquier página web accesible
   - **Caching**: TTL de 2 horas para contenido de páginas web con normalización de URL
   - Análisis HTML automático y limpieza (remueve scripts, anuncios, navegación)
   - Manejo de truncamiento de contenido para páginas grandes

3. **clear-cache** ⭐ NUEVO
   - Limpiar resultados de búsqueda en cache y contenido de páginas web
   - Soporta limpieza selectiva (búsqueda, páginas web, o todo)
   - Devuelve estadísticas sobre entradas limpiadas

4. **cache-stats** ⭐ NUEVO
   - Monitorear rendimiento y eficiencia de cache
   - Muestra tasas de acierto de cache, uso de memoria, e información TTL
   - Proporciona recomendaciones para gestión de cache

#### **Perplexity Search MCP Server (5 Herramientas)** - Con Caching de Respuestas
1. **perplexity_search_web**
   - Búsqueda web estándar impulsada por IA con filtrado de actualidad
   - **Caching**: TTL de 30 minutos para respuestas de API
   - Devuelve respuestas sintetizadas por IA con citas automáticas

2. **perplexity_advanced_search**
   - Búsqueda avanzada con parámetros personalizados
   - **Caching**: Cache específico por parámetros con TTL
   - Selección de modelo, control de temperatura (0.0-1.0), máx tokens (1-2048)

3. **search_show_categories**
   - Buscar y filtrar taxonomía basada en CSV
   - Filtrar por feria (CAI, DOL, CCSE, BDAIW, DCW), industria o producto
   - **Datos Locales**: Sin llamadas a API externas, respuestas instantáneas

4. **tag_company** ⭐ CARACTERÍSTICA
   - Investigación avanzada de empresas y etiquetado de taxonomía
   - Investigación automatizada de empresas usando fuentes web y LinkedIn
   - Coincidencia de empresas con categorías precisas de industria/producto
   - Genera salida estructurada con hasta 4 pares industria/producto

5. **clear_api_cache** ⭐ NUEVO
   - Limpiar cache de respuestas de API de Perplexity
   - Devuelve estadísticas de cache y conteo de entradas limpiadas
   - Útil para forzar respuestas frescas de API

6. **get_cache_stats** ⭐ NUEVO
   - Obtener estadísticas detalladas de cache de API de Perplexity
   - Muestra eficiencia de cache y métricas de rendimiento
   - Incluye tasas de acierto de cache e información TTL

#### **Company Tagging MCP Server (1 Herramienta - stdio Integrado)**
1. **search_show_categories** (Instancia Adicional)
   - Flujo de trabajo especializado de etiquetado y categorización de empresas
   - Acceso a taxonomía de ferias comerciales con pares industria/producto
   - Integrado con Google Search y Perplexity para investigación de empresas

### **Recursos Disponibles: 7+ Recursos**

#### **Recursos de Categorías CSV**
- **categories://all**: Datos CSV completos con todas las categorías de ferias
- **categories://shows**: Categorías organizadas por feria con estadísticas
- **categories://shows/{show_name}**: Categorías para ferias específicas
- **categories://industries**: Categorías organizadas por industria
- **categories://industries/{industry_name}**: Categorías específicas de industria
- **categories://search/{query}**: Búsqueda a través de todos los datos de categorías
- **categories://for-tagging**: Categorías formateadas específicamente para company tagging

### **Prompts Disponibles: 1 Prompt**
- **company_tagging_analyst**: Prompt de analista de datos profesional para categorización de empresas

### **Características de Optimización de Rendimiento** ⭐ NUEVO

#### **Caching del Google Search MCP Server**
- **Resultados de Búsqueda**: TTL de 30 minutos con generación de clave MD5
- **Contenido de Páginas Web**: TTL de 2 horas con normalización de URL y eliminación de parámetros de seguimiento
- **Expulsión LRU**: Máximo 1000 páginas en cache con expulsión de las más antiguas primero
- **Limpieza Automática**: Entradas expiradas limpiadas cada 30 minutos (páginas web) y 10 minutos (búsqueda)
- **Estadísticas de Cache**: Monitoreo en tiempo real de eficiencia de cache y uso de memoria

#### **Caching del Perplexity MCP Server**
- **Respuestas de API**: TTL de 30 minutos con cache específico por parámetros
- **Hash Inteligente**: Claves de cache basadas en consulta y todos los parámetros (actualidad, modelo, temperatura, etc.)
- **Optimización de Chequeos de Salud**: TTL de 5 minutos para chequeos de salud para evitar llamadas innecesarias a API
- **Gestión de Cache**: Herramientas para limpiar cache y monitorear rendimiento

#### **Beneficios del Sistema de Caching**
- **Costos de API Reducidos**: Reducción significativa en llamadas a Google Custom Search y API de Perplexity
- **Tiempos de Respuesta Mejorados**: Aciertos de cache proporcionan respuestas instantáneas
- **Mejor Confiabilidad**: Resultados en cache disponibles incluso durante interrupciones de API
- **Eficiencia de Recursos**: Menor carga del servidor y uso de ancho de banda
- **Experiencia de Usuario**: Resultados de búsqueda y carga de contenido más rápidos

## 📝 Ejemplos de Uso

### **Flujo de Trabajo de Autenticación**
```
1. Navegar a https://localhost:8503 (SSL) o http://localhost:8501 (HTTP)
2. Usar el panel de autenticación de la barra lateral
3. Iniciar sesión con credenciales generadas
4. Acceder a todas las características de la aplicación
```

### **Flujos de Trabajo de Búsqueda con Caching**

#### **Datos Rápidos e Información Actual (Perplexity con Cache)**
```
"¿Cuáles son los últimos desarrollos en inteligencia artificial?"
"Encuentra noticias recientes sobre cambio climático"
"¿Cuál es el estado actual de la adopción de energías renovables?"
```
*Usa herramientas de Perplexity con cache de 30 minutos para respuestas sintetizadas por IA*

#### **Investigación Completa (Google Search con Cache)**
```
"Investiga el impacto de la IA en la industria de la salud"
"Encuentra información detallada sobre prácticas agrícolas sostenibles"
"Analiza tendencias del mercado en vehículos eléctricos"
```
*Usa Google Search con cache de búsqueda de 30 minutos y cache de contenido de 2 horas*

#### **Flujo de Trabajo de Company Tagging**
```
"Etiqueta empresas para categorización de feria comercial"
"Investiga y categoriza NVIDIA Corporation para ferias CAI y BDAIW"
"Etiqueta los siguientes datos de empresa con nombre comercial IBM para ferias de tecnología"
```
*Usa flujo de trabajo especializado de company tagging con herramientas tanto de Google Search como de Perplexity*

#### **Ejemplos de Gestión de Cache**
```
# Limpiar todos los cachés
Usar la herramienta clear-cache: {"cacheType": "all"}

# Monitorear rendimiento de cache
Usar la herramienta cache-stats: {"detailed": true}

# Limpiar solo cache de búsqueda
Usar la herramienta clear-cache: {"cacheType": "search"}

# Obtener estadísticas de cache de Perplexity
Usar la herramienta get_cache_stats del servidor Perplexity
```

### **Monitoreo de Rendimiento**

#### **Monitoreo de Chequeos de Salud**
- **Google Search**: `curl http://localhost:8002/health/detailed`
- **Perplexity**: `curl http://localhost:8001/health`
- **Limpieza de Cache**: `curl http://localhost:8002/cache/clear`

#### **Indicadores de Rendimiento de Cache**
- **Tasa de Acierto de Cache**: Porcentaje de solicitudes servidas desde cache
- **Llamadas a API Evitadas**: Número de llamadas a API externas prevenidas por cache
- **Uso de Memoria**: Consumo estimado de memoria de cache
- **Efectividad TTL**: Qué tan bien funcionan las configuraciones TTL de cache para tus patrones de uso

## 🔧 Documentación de Componentes

### [🖥️ Documentación del Cliente Streamlit](./client/Readme.md)
- **Sistema de Autenticación**: Gestión segura de usuarios con bcrypt y control de sesiones
- **Configuración SSL/HTTPS**: Gestión de certificados y conexiones seguras
- **Integración de Proveedores IA**: OpenAI, Azure OpenAI, y soporte multi-proveedor mejorado
- **Operaciones Cliente MCP**: Interfaz universal para conectar con múltiples servidores MCP
- **Monitoreo de Ejecución de Herramientas**: Seguimiento en tiempo real y gestión de conversaciones
- **Integración Company Tagging**: Flujo de trabajo especializado para categorización de ferias comerciales

### [🔍 Documentación del Google Search MCP Server](./servers/server2/readme.md)
- **Integración Google Custom Search**: Integración API con caching inteligente
- **Búsqueda Web y Extracción de Contenido**: 4 herramientas incluyendo gestión de cache
- **Optimización de Rendimiento**: Cache de búsqueda de 30 minutos, cache de contenido de 2 horas
- **Implementación de Transporte SSE**: Comunicación en tiempo real con chequeos de salud
- **Gestión de Cache**: Herramientas de estadísticas, limpieza y monitoreo
- **Auto-registro**: Descubrimiento dinámico de herramientas y validación

### [🔮 Documentación del Perplexity MCP Server](./servers/server1/Readme.md)
- **Integración Perplexity AI**: Integración API con cache de respuestas
- **Búsqueda Potenciada por IA**: 5 herramientas incluyendo búsqueda avanzada y company tagging
- **Soporte de Múltiples Modelos**: sonar, sonar-pro, sonar-reasoning, y más
- **Company Tagging**: Flujo de trabajo avanzado de investigación y coincidencia de taxonomía
- **Gestión de Categorías CSV**: Acceso y filtrado de datos de ferias comerciales
- **Optimización de Cache**: TTL de 30 minutos con limpieza inteligente

## 🛠️ Desarrollo y Personalización

### **Configuración de Cache**

#### **Caching del Servidor de Google Search**
```javascript
// En servers/server2/tools/searchTool.js
const searchCache = new SearchCache(30); // TTL de 30 minutos

// En servers/server2/tools/readWebpageTool.js
const webpageCache = new WebpageCacheClass(2); // TTL de 2 horas
```

#### **Caching del Servidor de Perplexity**
```python
# En servers/server1/perplexity_sse_server.py
api_cache = APICache(ttl_seconds=1800)  # Cache de 30 minutos
health_check_cache = {"ttl": 300}  # Cache de chequeo de salud de 5 minutos
```

### **Ajuste de Rendimiento de Cache**
- **TTL de Cache de Búsqueda**: Ajustar basado en requisitos de frescura de contenido
- **TTL de Cache de Páginas Web**: Equilibrar entre frescura de contenido y carga del servidor
- **Tamaño Máximo de Cache**: Configurar basado en memoria disponible
- **Intervalos de Limpieza**: Optimizar basado en patrones de uso

### **Agregando Nuevas Características**

#### **Agregando Proveedores IA**
Habilita Enhanced Mode en la pestaña Configuración para acceso a:
- Modelos Anthropic Claude
- Modelos Google Gemini
- Modelos Cohere Command
- Modelos Mistral AI
- Despliegue local Ollama

#### **Agregando Servidores MCP**
Configura nuevos servidores en `servers_config.json`:
```json
{
  "mcpServers": {
    "Nuevo Servidor": {
      "transport": "sse",
      "url": "http://nuevo-servidor:8004/sse",
      "timeout": 600,
      "sse_read_timeout": 900
    }
  }
}
```

## 🔒 Seguridad y Mejores Prácticas

### **Seguridad de API**
- Usar claves API seguras con alcance apropiado
- Implementar limitación de velocidad para solicitudes de búsqueda (automático con cache)
- Habilitar SSL/TLS para todas las comunicaciones
- Rotar regularmente claves API y credenciales

### **Seguridad de Autenticación**
- **Hash de Contraseñas**: bcrypt estándar de la industria con salt
- **Gestión de Sesiones**: Timeout configurable (30 días por defecto)
- **Cookies Seguras**: Atributos HTTPOnly y secure
- **Control de Acceso**: Validación de dominios de email pre-autorizados

### **Seguridad de Cache**
- Las claves de cache usan hash MD5 para seguridad
- La normalización de URL elimina parámetros de seguimiento
- No se almacenan datos sensibles en cache
- Limpieza automática de entradas expiradas

### **Protección de Datos**
- **Aislamiento de Usuario**: Historiales de conversación separados por usuario
- **Seguimiento de Sesión**: Monitoreo de tiempo de inicio de sesión y actividad
- **Privacidad de Conversación**: Sesiones de chat aisladas por usuario
- **Limpieza Segura**: Gestión automática de datos de sesión

### **Monitoreo de Rendimiento**
- Monitorear tasas de acierto de cache para optimizar configuraciones TTL
- Rastrear reducción de uso de API a través de cache
- Monitorear uso de memoria para dimensionamiento de cache
- Usar endpoints de chequeo de salud para monitoreo del sistema

## 🐛 Solución de Problemas

### **Problemas Relacionados con Cache**

#### **Cache No Funciona**
```bash
# Verificar estadísticas de cache
curl http://localhost:8002/health/detailed

# Limpiar cache si está corrupto
curl http://localhost:8002/cache/clear

# Verificar logs del servidor para errores de cache
docker-compose logs mcpserver2 | grep cache
```

#### **Alto Uso de Memoria**
```bash
# Verificar tamaños de cache
curl http://localhost:8002/health/detailed
curl http://localhost:8001/health

# Limpiar cachés grandes
Usar herramienta clear-cache con {"cacheType": "webpage"}
Usar herramienta clear_api_cache para Perplexity
```

#### **Problemas de Rendimiento de Cache**
- **Baja Tasa de Acierto**: Considerar aumentar valores TTL
- **Alto Uso de Memoria**: Reducir tamaños de cache o valores TTL
- **Respuestas Lentas**: Verificar si los intervalos de limpieza de cache son apropiados

### **Problemas de Autenticación**
```bash
# Problema: El inicio de sesión falla con credenciales correctas
# Solución: Regenerar hashes de contraseñas
cd client && python simple_generate_password.py

# Problema: La sesión expira inmediatamente
# Verificar: configuración de cookies en keys/config.yaml
```

### **Problemas de Conexión MCP**
```bash
# Problema: No se puede conectar a servidores MCP
# Depurar: Verificar configuración del servidor
cat servers_config.json

# Probar: Accesibilidad del servidor
curl http://localhost:8002/sse
curl http://localhost:8001/sse

# Solución: Actualizar URLs del servidor en configuración
```

### **Problemas de API con Cache**

#### **Datos Obsoletos en Cache**
```bash
# Forzar datos frescos
Usar herramientas con parámetro skipCache donde esté disponible
Limpiar tipo específico de cache
Reducir TTL para actualizaciones más frecuentes
```

#### **Limitación de Velocidad de API**
- **El Cache Ayuda**: Automáticamente reduce llamadas a API
- **Monitorear Uso**: Usar estadísticas de cache para rastrear reducción de llamadas a API
- **Optimizar TTL**: Equilibrar frescura con uso de API

## 📈 Métricas de Rendimiento

### **Rendimiento de Cache** ⭐ NUEVO
- **Tasa de Acierto de Cache de Google Search**: Típicamente 40-60% para consultas repetidas
- **Tasa de Acierto de Cache de Contenido de Páginas Web**: Típicamente 60-80% para páginas populares
- **Tasa de Acierto de Cache de Perplexity**: Típicamente 30-50% para consultas similares
- **Reducción de Llamadas a API**: 40-70% de reducción en llamadas a API externas
- **Mejora de Tiempo de Respuesta**: 80-95% más rápido para respuestas en cache

### **Características de Rendimiento Actuales**
- **Tiempo de Respuesta de Búsqueda en Cache**: ~50-100ms (vs 1-3s fresco)
- **Extracción de Contenido en Cache**: ~100-200ms (vs 2-8s fresco)
- **Respuesta de Perplexity en Cache**: ~100-300ms (vs 2-5s fresco)
- **Autenticación**: <1s operaciones de inicio/cierre de sesión
- **Descubrimiento de Herramientas**: <2s para conexión de servidor MCP

### **Características de Escalabilidad**
- Contenerización Docker para escalado horizontal
- Cache inteligente para dependencias externas reducidas
- Operaciones async para manejo concurrente de solicitudes
- Pooling de conexiones para conexiones de base de datos y API

## 🚀 Despliegue en Producción

### **Configuración Docker de Producción**

#### **Docker Compose Completo**
```yaml
version: '3.8'

services:
  hostclient:
    build: 
      context: ./client
      dockerfile: Dockerfile
    ports:
      - "8501:8501"
      - "8503:8503"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - GOOGLE_SEARCH_ENGINE_ID=${GOOGLE_SEARCH_ENGINE_ID}
      - PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY}
      - SSL_ENABLED=true
    volumes:
      - ./client/keys:/app/keys
      - ./client/ssl:/app/ssl
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501"]
      interval: 30s
      timeout: 10s
      retries: 3

  mcpserver2:
    build: 
      context: ./servers/server2
      dockerfile: Dockerfile
    ports:
      - "8002:8002"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - GOOGLE_SEARCH_ENGINE_ID=${GOOGLE_SEARCH_ENGINE_ID}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  mcpserver1:
    build: 
      context: ./servers/server1
      dockerfile: Dockerfile
    ports:
      - "8001:8001"
    environment:
      - PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY}
      - PERPLEXITY_MODEL=sonar
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### **Opciones de Despliegue en la Nube**

#### **AWS ECS/Fargate**
- Orquestación escalable de contenedores
- Balanceamiento de carga con Application Load Balancer
- Auto-escalado basado en métricas CPU/memoria
- Logging y monitoreo CloudWatch

#### **Google Cloud Run**
- Despliegue de contenedores serverless
- Escalado automático a cero
- Modelo de precios pay-per-request
- Balanceamiento de carga global

#### **Azure Container Instances**
- Despliegue simple de contenedores
- Integración de red virtual
- Opciones de almacenamiento persistente
- Integración Azure Monitor

## 🤝 Contribuyendo

### **Flujo de Trabajo de Desarrollo**
1. Hacer fork del repositorio
2. Crear ramas de características para cada componente
3. Probar características de autenticación y seguridad
4. Probar funcionalidad de búsqueda tanto de Google como de Perplexity con cache
5. Verificar company tagging y acceso a datos CSV
6. Probar gestión de cache y monitoreo de rendimiento
7. Enviar pull requests con pruebas completas

### **Pruebas de Cache**
- Probar escenarios de acierto/fallo de cache para todas las herramientas
- Verificar comportamiento TTL de cache y limpieza
- Probar herramientas de gestión de cache (clear-cache, cache-stats)
- Monitorear rendimiento de cache bajo carga
- Probar comportamiento de cache durante interrupciones de API

### **Estándares de Código**
- Seguir PEP 8 para código Python
- Usar ESLint para código JavaScript/Node.js
- Escribir docstrings y comentarios comprensivos
- Agregar pruebas para nuevas características
- Actualizar documentación para cambios

## 📚 Recursos Adicionales

### **Documentación Oficial**
- [Especificación Model Context Protocol](https://spec.modelcontextprotocol.io/)
- [Documentación MCP de Anthropic](https://docs.anthropic.com/en/docs/mcp)
- [Repositorio GitHub MCP](https://github.com/modelcontextprotocol)

### **Recursos de la Comunidad**
- [MCP Market](https://mcpmarket.com/) - Descubrir servidores MCP
- [Foro Comunidad MCP](https://github.com/modelcontextprotocol/discussions)
- [Awesome MCP](https://github.com/punkpeye/awesome-mcp) - Lista curada de recursos MCP

### **Proyectos Relacionados**
- [Claude Desktop](https://claude.ai/download) - Cliente MCP oficial
- [Cursor IDE](https://cursor.sh/) - Editor de código habilitado para MCP
- [Cline](https://github.com/clinebot/cline) - Extensión MCP para VS Code

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Reconocimientos

- **Anthropic** por crear el Model Context Protocol
- **Streamlit** por el excelente framework web
- **LangChain** por el framework de agentes
- **La Comunidad MCP** por herramientas e inspiración

---

**Versión**: 2.1.0  
**Última Actualización**: Enero 2025  
**Compatibilidad**: Docker 20+, Python 3.11+, Node.js 18+, Google Custom Search API v1, Perplexity API v1  
**Seguridad**: Streamlit Authenticator 0.3.2, hash de contraseñas bcrypt, soporte SSL/HTTPS  
**Total de Herramientas**: 10 herramientas (4 Google Search con cache, 5 Perplexity AI con cache, 1 Company Tagging)  
**Servidores**: 3 servicios (Cliente con MCP stdio integrado, Google Search MCP con cache, Perplexity MCP con cache)  
**Arquitectura**: Transporte SSE + stdio MCP con autenticación completa y cache inteligente  
**Rendimiento**: Sistema de cache inteligente con 40-70% de reducción de uso de API y 80-95% de mejora en tiempo de respuesta para contenido en cache