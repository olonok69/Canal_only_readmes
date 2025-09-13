# Servidor MCP de Análisis Financiero en Python

Una implementación completa del Protocolo de Contexto de Modelo (MCP) que incluye herramientas de análisis financiero, comunicación por eventos enviados por el servidor (SSE) y un cliente chatbot inteligente. Este proyecto demuestra el poder del MCP como el "USB-C para integraciones de IA" proporcionando acceso estandarizado a datos y capacidades de análisis financiero.

## 🌟 Descripción General

El Protocolo de Contexto de Modelo (MCP) es un estándar abierto desarrollado por Anthropic que estandariza cómo las aplicaciones de IA se conectan con fuentes de datos externas, herramientas y sistemas. Este proyecto implementa un ecosistema MCP completo con:

- **Servidor de Análisis Financiero**: Servidor MCP que expone herramientas sofisticadas de análisis financiero
- **Transporte SSE**: Comunicación bidireccional en tiempo real usando Server-Sent Events
- **Cliente Inteligente**: Chatbot impulsado por IA que puede descubrir y usar herramientas financieras
- **Múltiples Indicadores**: Análisis MACD, Canales de Donchian, Bandas de Bollinger y Fibonacci

## 🚀 Características Principales

### Herramientas de Análisis Financiero
- **Calculadora de Puntuación MACD**: Análisis de Convergencia y Divergencia de Medias Móviles con puntuación por componentes
- **Análisis de Canales de Donchian**: Análisis de posición de precios y dirección del canal
- **Puntuación Combinada MACD-Donchian**: Indicadores integrados de momentum y rango
- **Estrategia Bollinger-Fibonacci**: Análisis técnico avanzado combinando múltiples indicadores
- **Z-Score de Bollinger**: Análisis estadístico de posición de precios

### Componentes de Arquitectura MCP
- **Servidor**: Expone herramientas financieras a través del protocolo MCP estandarizado
- **Recursos**: Acceso a datos estructurados para configuración e información de la aplicación
- **Herramientas**: Funciones ejecutables para análisis financiero impulsado por IA
- **Prompts**: Plantillas de interacción reutilizables para patrones de análisis comunes
- **Contexto**: Gestión inteligente de información para interacciones con LLM

### Transporte y Comunicación
- **SSE (Server-Sent Events)**: Comunicación bidireccional en tiempo real
- **Transporte HTTP**: Endpoints de API RESTful para verificaciones de salud y mensajería
- **JSON-RPC 2.0**: Protocolo estándar para comunicación MCP

## 📁 Estructura del Proyecto

```
mcp/python_client_server/
├── main.py                              # Punto de entrada para ejecutar el servidor
├── server.py                           # Instancia compartida del servidor MCP
├── mcp_server_sse.py                   # Servidor FastAPI con transporte SSE
├── mcp_client_sse_chat.py              # Cliente chatbot básico
├── mcp_client_sse_chat_improved.py     # Chatbot mejorado con mejor análisis
├── tools/                              # Herramientas de análisis financiero
│   ├── bollinger_bands_score.py        # Calculadora de Z-Score de Bollinger
│   ├── bollinger_fibonacci_tools.py    # Estrategia combinada Bollinger-Fibonacci
│   ├── macd_donchian_combined_score.py # Análisis MACD y Donchian
│   ├── csv_tools.py                    # Herramientas de procesamiento CSV
│   └── parquet_tools.py                # Herramientas de procesamiento Parquet
├── utils/                              # Funciones utilitarias
│   ├── yahoo_finance_tools.py          # Procesamiento de datos de Yahoo Finance
│   └── file_reader.py                  # Utilidades de lectura de archivos
├── keys/                               # Configuración y credenciales
│   └── .env                           # Variables de entorno
├── data/                               # Archivos de datos
├── pyproject.toml                      # Dependencias del proyecto
└── README.md                           # Este archivo
```

## 🛠️ Instalación

### Prerequisitos
- Python 3.12 o superior
- Gestor de paquetes [uv](https://github.com/astral-sh/uv)

### Instrucciones de Configuración

1. **Instalar el gestor de paquetes uv**:
   ```bash
   # Linux/Mac
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Clonar y configurar el proyecto**:
   ```bash
   git clone <url-del-repositorio>
   cd mcp/python_client_server
   ```

3. **Crear entorno virtual**:
   ```bash
   uv venv
   
   # Activar entorno
   # Linux/Mac:
   source .venv/bin/activate
   
   # Windows:
   .venv\Scripts\activate
   ```

4. **Instalar dependencias**:
   ```bash
   uv add "mcp[cli]" pandas pyarrow yfinance langchain langchain_mcp_adapters langgraph langchain_google_genai google-generativeai python-dotenv fastapi loguru numpy openai
   ```

5. **Configurar variables de entorno**:
   ```bash
   # Crear archivo keys/.env con tus claves API
   echo "OPENAI_API_KEY=tu_clave_api_openai_aqui" > keys/.env
   ```

## 🚀 Uso

### Ejecutar el Servidor MCP

Iniciar el servidor de análisis financiero con transporte SSE:

```bash
python mcp_server_sse.py
```

El servidor se iniciará en `http://localhost:8100` con los siguientes endpoints:
- `GET /sse` - Conexión Server-Sent Events
- `POST /messages/` - Manejo de mensajes MCP
- `GET /health` - Verificación de salud

### Usar el Cliente Interactivo

Iniciar el cliente chatbot inteligente:

```bash
# Cliente básico
python mcp_client_sse_chat.py

# Cliente mejorado (recomendado)
python mcp_client_sse_chat_improved.py
```

### Consultas de Ejemplo

Prueba estas consultas de ejemplo con el chatbot:

```
"¿Cuál es la puntuación MACD para AAPL durante el último año?"

"Calcula el Z-score de Bollinger para TSLA con un período de 20 días"

"Dame un análisis combinado MACD-Donchian para MSFT usando 6 meses de datos"

"Analiza NVDA usando la estrategia Bollinger-Fibonacci para los últimos 3 días"

"¿Cuál es la recomendación para comprar o vender AAPL basada en indicadores técnicos?"
```

## 🔧 Componentes Principales Explicados

### Implementación del Servidor MCP

El servidor usa FastMCP para una implementación MCP simplificada:

```python
from mcp.server.fastmcp import FastMCP

# Crear servidor MCP
mcp = FastMCP(name="Finance Tools")

# Definir una herramienta de análisis financiero
@mcp.tool()
def calculate_macd_score(symbol: str, period: str = "1y") -> str:
    """Calcular puntuación MACD para un símbolo dado"""
    # Implementación aquí
    return f"Análisis MACD para {symbol}"
```

### Capa de Transporte SSE

Los Server-Sent Events permiten comunicación bidireccional en tiempo real:

```python
from mcp.server.sse import SseServerTransport

transport = SseServerTransport("/messages/")

async def handle_sse(request):
    async with transport.connect_sse(request.scope, request.receive, request._send) as (in_stream, out_stream):
        await mcp._mcp_server.run(in_stream, out_stream, mcp._mcp_server.create_initialization_options())
```

### Arquitectura del Cliente Inteligente

El cliente implementa varios componentes especializados:

- **LLMClient**: Gestiona interacciones con los modelos GPT de OpenAI
- **PromptGenerator**: Crea prompts especializados para selección de herramientas y procesamiento de respuestas
- **ResponseParser**: Maneja análisis JSON y recuperación de errores
- **AgentProcessor**: Orquesta el flujo de descubrimiento y ejecución de herramientas

## 📊 Herramientas de Análisis Financiero

### Calculadora de Puntuación MACD
Calcula una puntuación MACD integral (-100 a +100) combinando:
- **Línea MACD vs Línea de Señal (40%)**: Dirección del momentum
- **Línea MACD vs Cero (30%)**: Fuerza de la tendencia
- **Momentum del Histograma (30%)**: Aceleración/desaceleración

### Análisis de Canales de Donchian
Evalúa la posición del precio dentro de los Canales de Donchian:
- **Posición del Precio (50%)**: Ubicación dentro de las bandas del canal
- **Dirección del Canal (30%)**: Identificación de tendencia
- **Ancho del Canal (20%)**: Evaluación de volatilidad

### Estrategia Bollinger-Fibonacci
Análisis multi-indicador avanzado:
- **Posición de Bandas de Bollinger (30%)**: Precio relativo a las bandas
- **Evaluación de Volatilidad (15%)**: Ancho de bandas y cambios
- **Interacción con Niveles de Fibonacci (35%)**: Niveles clave de soporte/resistencia
- **Momentum del Precio (20%)**: Indicador de momentum tipo RSI

### Sistema de Puntuación Combinado
Todas las herramientas proporcionan puntuación estandarizada con señales de trading claras:
- **+75 a +100**: Compra Fuerte
- **+50 a +75**: Compra
- **+25 a +50**: Compra Débil
- **-25 a +25**: Neutral (Mantener)
- **-50 a -25**: Venta Débil
- **-75 a -50**: Venta
- **-100 a -75**: Venta Fuerte

## 🔌 Detalles del Protocolo MCP

### Recursos
Endpoints de datos estructurados para configuración:

```python
@mcp.resource("config://app-version")
def get_app_version() -> str:
    return "v2.1.0"

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"¡Hola, {name}!"
```

### Herramientas
Funciones ejecutables para análisis de IA:

```python
@mcp.tool()
def calculate_z_score(symbol: str, period: int = 20) -> str:
    """Calcular Z-Score de Bollinger para análisis técnico"""
    # Implementación
    return analysis_result
```

### Prompts
Plantillas de interacción reutilizables:

```python
@mcp.prompt()
def analyze_stock(symbol: str) -> str:
    return f"Por favor analiza {symbol} usando los indicadores técnicos disponibles"
```

## 🤖 Integración con IA

El proyecto demuestra cómo MCP permite una integración perfecta con IA:

1. **Descubrimiento de Herramientas**: La IA descubre automáticamente las herramientas financieras disponibles
2. **Selección Inteligente**: GPT-4o-mini selecciona las herramientas apropiadas basándose en las consultas del usuario
3. **Extracción de Parámetros**: Las consultas en lenguaje natural se convierten en llamadas estructuradas a herramientas
4. **Interpretación de Resultados**: Las respuestas de las herramientas se formatean en explicaciones amigables para el usuario
5. **Flujos Multi-Herramienta**: Los análisis complejos pueden encadenar múltiples herramientas juntas

## 🔧 Configuración

### Variables de Entorno
Crear `keys/.env` con:

```bash
OPENAI_API_KEY=tu_clave_api_openai_aqui
# Agregar otras claves API según sea necesario
```

### Configuración del Servidor
Modificar `mcp_server_sse.py` para personalizar:
- Número de puerto (por defecto: 8100)
- Herramientas disponibles
- Fuentes de datos
- Parámetros de análisis

## 🏗️ Beneficios de la Arquitectura

### Integración Estandarizada
- **Protocolo Universal**: Un protocolo para todas las integraciones IA-herramientas
- **Interoperabilidad**: Las herramientas funcionan a través de diferentes modelos de IA y plataformas
- **Escalabilidad**: Fácil agregar nuevas herramientas y fuentes de datos

### Seguridad y Control
- **Autorización del Usuario**: Las herramientas requieren permiso del usuario antes de la ejecución
- **Aislamiento de Datos**: Cada servidor mantiene su propio contexto de datos
- **Registro de Auditoría**: Todas las llamadas a herramientas se registran y son rastreables

### Experiencia del Desarrollador
- **Implementación Simple**: FastMCP reduce el código repetitivo
- **Seguridad de Tipos**: Generación automática de esquemas desde type hints de Python
- **Manejo de Errores**: Recuperación de errores y validación incorporadas

## 🔮 Mejoras Futuras

### Características Planificadas
- **Análisis de Portfolio**: Herramientas de optimización de carteras multi-activo
- **Gestión de Riesgo**: VaR, pruebas de estrés y métricas de riesgo
- **Aprendizaje Automático**: Modelos predictivos y reconocimiento de patrones
- **Datos en Tiempo Real**: Feeds de datos de mercado en vivo y alertas
- **Backtesting**: Análisis de rendimiento histórico de estrategias

### Oportunidades de Integración
- **Conectividad de Base de Datos**: Servidores MCP para PostgreSQL, MongoDB
- **Servicios en la Nube**: Integraciones con AWS, GCP, Azure
- **Plataformas de Trading**: Conexiones con APIs de brokers
- **Noticias y Sentimiento**: Herramientas de análisis de noticias financieras

## 🤝 Contribuir

1. Hacer fork del repositorio
2. Crear una rama de característica
3. Agregar tus herramientas MCP o mejoras
4. Incluir pruebas comprehensivas
5. Enviar un pull request

### Pautas de Desarrollo
- Seguir type hints de Python
- Usar decoradores FastMCP para herramientas/recursos
- Incluir docstrings con descripciones de parámetros
- Agregar manejo de errores para llamadas a APIs externas
- Probar con múltiples modelos de IA

## 📚 Recursos Adicionales

- [Especificación MCP](https://modelcontextprotocol.io/docs)
- [Documentación FastMCP](https://github.com/pydantic/fastmcp)
- [Indicadores de Análisis Técnico](https://www.investopedia.com/technical-analysis/)
- [Guía de Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Reconocimientos

- [Anthropic](https://www.anthropic.com/) por desarrollar el estándar MCP
- [FastMCP](https://github.com/pydantic/fastmcp) por la implementación en Python
- [Yahoo Finance](https://finance.yahoo.com/) por los datos financieros
- [OpenAI](https://openai.com/) por la integración con modelos GPT

---

**El Protocolo de Contexto de Modelo representa un cambio fundamental en la interoperabilidad de sistemas de IA. Al proporcionar una forma estandarizada para que los modelos de IA accedan a datos y funcionalidad externa, MCP habilita asistentes de IA más conscientes del contexto y capaces, mientras reduce la complejidad de integración.**