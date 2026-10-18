# 📊 Herramienta de Análisis de Mercados Financieros MCP

Una plataforma de análisis financiero impulsada por IA que combina **Model Context Protocol (MCP)**, **smolagents**, **FastAPI** y **Streamlit** para entregar informes de inversión de nivel profesional. El sistema utiliza Modelos de Lenguaje de Gran Escala para orquestar herramientas de trading e interpretar datos financieros, transformando datos de mercado en bruto en información accionable.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-1.28+-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/MCP-1.0+-purple.svg" alt="MCP">
  <img src="https://img.shields.io/badge/smolagents-1.0+-orange.svg" alt="smolagents">
</p>

---

## 🎯 Descripción General

Esta aplicación ofrece **7 tipos de análisis** desde una interfaz web moderna:

| Tipo de análisis | Descripción | Caso de uso |
|------------------|-------------|-------------|
| **📈 Análisis Técnico** | 4 estrategias de trading sobre una única acción | Profundizar en patrones de precios |
| **🔍 Escáner de Mercado** | Compara varias acciones de forma simultánea | Encontrar mejores oportunidades |
| **💰 Análisis Fundamental** | Interpretación de estados financieros | Evaluar la salud de la compañía |
| **🌐 Análisis Multi-Sector** | Comparación entre sectores | Diversificar la cartera |
| **🔄 Análisis Combinado** | Técnico + Fundamental juntos | Construir una tesis completa |
| **🌙 Gaps Nocturnos** | Cierre previo vs apertura, tasas de fill intradía, drift diario | Comportamiento de gaps/midnight returns |
| **⚡ Momentum de Earnings** | Escáner de spikes de volumen con ventana fija | Detectar rupturas tras resultados |

### ¿Qué lo hace diferente?

A diferencia de las herramientas tradicionales que solo muestran números, este sistema utiliza **IA para interpretar** los datos:

```
Herramienta tradicional: "RSI = 28.5, MACD = -2.3, P/E = 15.2"

Esta aplicación: "AAPL muestra condiciones de sobreventa con un RSI de 28.5,
                  lo que sugiere una posible oportunidad de reversión a la media.
                  Combinado con fundamentos sólidos (P/E de 15.2, por debajo del
                  promedio del sector), esto presenta una señal de COMPRA con alta convicción..."
```

---

## 🤖 Dos arquitecturas de agentes

La aplicación ofrece **dos tipos de agentes de IA**, cada uno con ventajas distintas:

### 🔧 ToolCallingAgent (Original)

El enfoque tradicional en el que el LLM emite JSON para llamar a las herramientas una por una.

<p align="center">
  <img src="docs/architecture.svg" alt="Arquitectura ToolCallingAgent" width="900">
</p>

### 🐍 CodeAgent (Nuevo - Recomendado)

El enfoque avanzado en el que el LLM escribe código Python para invocar herramientas, habilitando bucles y variables.

<p align="center">
  <img src="docs/architecture_codeagent.svg" alt="Arquitectura CodeAgent" width="900">
</p>

---

## ⚖️ Comparativa ToolCallingAgent vs CodeAgent

### Cómo funcionan

| Aspecto | 🔧 ToolCallingAgent | 🐍 CodeAgent |
|---------|---------------------|--------------|
| **Formato de salida** | Llamadas JSON | Código Python |
| **Invocación de herramientas** | `{"tool": "analyze", "args": {...}}` | `result = analyze(symbol="AAPL")` |
| **Manejo multi-herramienta** | Una llamada por ronda LLM | Puede agrupar con bucles |
| **Variables** | ❌ No almacena resultados | ✅ Usa variables |
| **Bucles** | ❌ No soportado | ✅ `for stock in stocks:` |
| **Condicionales** | ❌ No soportado | ✅ `if signal == "BUY":` |

### Ejemplo: analizar 5 acciones

**ToolCallingAgent:**
```
Ronda 1: LLM → "Call analyze(AAPL)" → Resultado
Ronda 2: LLM → "Call analyze(MSFT)" → Resultado
Ronda 3: LLM → "Call analyze(GOOGL)" → Resultado
Ronda 4: LLM → "Call analyze(META)" → Resultado
Ronda 5: LLM → "Call analyze(NVDA)" → Resultado
Ronda 6: LLM → Sintetiza todos los resultados → Informe

Total: 6 llamadas LLM
```

**CodeAgent:**
```python
# El LLM genera este código en una única ronda:
results = {}
for stock in ["AAPL", "MSFT", "GOOGL", "META", "NVDA"]:
    results[stock] = analyze(symbol=stock, period="1y")

# Calcular consenso
buy_signals = sum(1 for r in results.values() if "BUY" in r)
report = f"Consenso: {buy_signals}/5 acciones muestran señales de COMPRA..."

final_answer(report)

Total: 1-2 llamadas LLM
```

### Comparación de rendimiento

| Escenario | ToolCallingAgent | CodeAgent | Mejora |
|-----------|-----------------|-----------|--------|
| 1 acción, 4 herramientas | ~45 segundos | ~40 segundos | ~10% más rápido |
| 5 acciones, 4 herramientas | ~3 minutos | ~1.5 minutos | ~50% más rápido |
| 3 sectores, 30 acciones | ~15 minutos | ~5 minutos | ~66% más rápido |

### Pros y contras

#### 🔧 ToolCallingAgent

| ✅ Ventajas | ❌ Limitaciones |
|-------------|----------------|
| Simple y predecible | Una herramienta por ronda |
| Sin riesgos de ejecución de código | Más llamadas al LLM = más costo |
| Fácil de depurar | Más lento para multi-acción |
| Funciona con cualquier LLM | No compone lógica compleja |
| Enfoque probado | Limitado a ejecución secuencial |

**Ideal para:**
- Análisis de una sola acción
- Consultas sencillas
- Producción con requisitos de seguridad estrictos
- Modelos con baja habilidad para generar código

#### 🐍 CodeAgent

| ✅ Ventajas | ❌ Limitaciones |
|-------------|----------------|
| Bucles eficientes para múltiples acciones | Requiere sandbox para ejecutar código |
| Menos llamadas al LLM = menor costo | Más complejo de depurar |
| Puede almacenar y reutilizar resultados | Necesita LLM con buen nivel de Python |
| Razonamiento natural basado en código | Consideraciones de seguridad |
| Excelente para análisis complejos | Puede generar código inválido |

**Ideal para:**
- Escáneres multi-acción
- Análisis multi-sector
- Comparativas complejas
- Entornos de desarrollo
- Optimización de costos

### Consideraciones de seguridad

| Ejecutor | Seguridad | Caso de uso |
|----------|-----------|-------------|
| `local` | ⚠️ Baja | Desarrollo |
| `e2b` | ✅ Alta | Producción (sandbox en la nube) |
| `docker` | ✅ Alta | Producción (auto-hospedado) |

```python
# Desarrollo (ejecución local)
agent = CodeAgent(tools=tools, model=model, executor_type="local")

# Producción (sandbox e2b)
agent = CodeAgent(tools=tools, model=model, executor_type="e2b")

# Producción (sandbox Docker)
agent = CodeAgent(tools=tools, model=model, executor_type="docker")
```

### Cuándo usar cada uno

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO DE DECISIÓN                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ¿Analizas una sola acción?                                     │
│      │                                                          │
│      ├── SÍ → Cualquiera funciona                               │
│      │                                                          │
│      └── NO → Usa CodeAgent (2-3× más rápido)                   │
│                                                                 │
│  ¿Es producción?                                                │
│      │                                                          │
│      ├── SÍ + seguridad crítica → ToolCallingAgent              │
│      │                                                          │
│      ├── SÍ + rendimiento crítico → CodeAgent + e2b/docker      │
│      │                                                          │
│      └── NO → CodeAgent + local                                 │
│                                                                 │
│  ¿El LLM tiene poca habilidad en Python?                        │
│      │                                                          │
│      └── SÍ → ToolCallingAgent                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Descripción general de la arquitectura

### Estructura de carpetas

```
mcp_financial_markets_analysis_tool/
│
├── server/                          # Servidor MCP (herramientas financieras)
│   ├── main.py                      # Punto de entrada del servidor
│   ├── strategies/                  # Implementaciones de estrategias
│   │   ├── bollinger_fibonacci.py   # Bollinger + Fibonacci
│   │   ├── macd_donchian.py         # MACD + Donchian
│   │   ├── connors_zscore.py        # Connors RSI + Z-Score
│   │   ├── dual_moving_average.py   # Cruce EMA 50/200
│   │   ├── bollinger_zscore.py      # Bollinger + Z-Score
│   │   ├── fundamental_analysis.py  # Estados financieros con alias
│   │   ├── performance_tools.py     # Herramientas de backtesting
│   │   └── unified_market_scanner.py# Escáner multi-acción
│   ├── utils/
│   │   └── yahoo_finance_tools.py   # Datos e indicadores de mercado
│   └── README.md                    # 📚 Documentación detallada del servidor
│
├── stock_analyzer_bot/              # Bot smolagents (orquestación)
│   ├── __init__.py
│   ├── main.py                      # ToolCallingAgent
│   ├── main_codeagent.py            # CodeAgent (nuevo)
│   ├── api.py                       # Endpoints FastAPI
│   ├── tools.py                     # Wrappers de herramientas
│   ├── mcp_client.py                # Gestor de conexión MCP
│   └── README.md                    # 📚 Documentación detallada del bot
│
├── docs/
│   ├── architecture.svg             # Diagrama ToolCallingAgent
│   ├── architecture_codeagent.svg   # Diagrama CodeAgent (nuevo)
│   └── Sectors_reference.md         # Referencia de sectores
│
├── streamlit_app.py                 # Interfaz web (7 pestañas)
├── .env                             # Variables de entorno
├── requirements.txt                 # Dependencias
└── README.md                        # 📚 Este archivo
```

### Flujo de datos

Ambos agentes comparten el mismo flujo de alto nivel:

1. **Streamlit** → El usuario interactúa con la interfaz.
2. **FastAPI** → La API recibe la petición y selecciona el agente.
3. **Agente** → ToolCallingAgent o CodeAgent procesan la solicitud.
4. **LLM API** → OpenAI/HuggingFace guían la selección de herramientas.
5. **Cliente MCP** → Actúa como puente con el servidor MCP.
6. **Servidor MCP** → Ejecuta las herramientas financieras.
7. **Estrategias** → Calculan indicadores técnicos.
8. **Yahoo Finance** → Suministra los datos de mercado.

---

## 🤖 Conociendo Smolagents

### ¿Qué es smolagents?

[**Smolagents**](https://huggingface.co/docs/smolagents/index) es una librería Python de Hugging Face que facilita construir agentes que utilizan herramientas.

> *"smolagents está diseñado para que construir y ejecutar agentes requiera solo unas pocas líneas de código."* — Hugging Face

### Por qué preferir CodeAgent

Según [Hugging Face](https://huggingface.co/docs/smolagents/tutorials/secure_code_execution):

> *"Diversos estudios demuestran que pedir al LLM que escriba sus acciones en código funciona mejor que los formatos de JSON usados habitualmente para tool calling."*

**Ventajas del código:**
- **Composibilidad**: permite bucles, funciones y lógica reutilizable.
- **Gestión de objetos**: conserva resultados en variables.
- **Generalidad**: expresa cualquier cálculo, no solo llamadas a herramientas.
- **Datos de entrenamiento**: los LLM han visto mucho Python durante su entrenamiento.

### Cómo usamos smolagents

```python
from smolagents import ToolCallingAgent, tool

@tool
def bollinger_fibonacci_analysis(symbol: str, period: str = "1y") -> str:
    """Analiza una acción con Bandas de Bollinger y retrocesos de Fibonacci."""
    return _call_mcp_tool("analyze_bollinger_fibonacci_performance", {...})

model = LiteLLMModel(model_id="gpt-4o")
agent = ToolCallingAgent(
    tools=[bollinger_fibonacci_analysis, macd_donchian_analysis, ...],
    model=model,
    max_steps=25,
)

report = agent.run("""
    Analiza la acción AAPL con las 4 estrategias técnicas y devuelve un informe en markdown.
""")
```

### Ciclo de decisión del agente

```
1. LEE: "Analiza AAPL con 4 estrategias"
2. PLANIFICA: decide qué herramientas necesita
3. EJECUTA: llama a cada herramienta y recopila datos
4. SINTETIZA: combina resultados y detecta patrones
5. GENERA: produce un informe profesional en markdown
```

---

## 📱 Interfaz Streamlit

### Selector de agente en la barra lateral

```
┌─────────────────────────────────────┐
│  ⚙️ Configuración                   │
│                                     │
│  🤖 Tipo de agente                  │
│  ○ 🔧 ToolCallingAgent (Original)   │
│  ● 🐍 CodeAgent (Nuevo - Rápido)    │
│                                     │
│  Ejecutor de código: [local ▼]      │
│                                     │
└─────────────────────────────────────┘
```

### Las 7 pestañas de análisis

| Pestaña | Descripción | Agente recomendado |
|---------|-------------|--------------------|
| 📈 Técnica | Una acción, 4 estrategias | Cualquiera |
| 🔍 Escáner | Comparación multi-acción | 🐍 CodeAgent |
| 💰 Fundamental | Estados financieros | Cualquiera |
| 🌐 Multi-Sector | Comparativa entre sectores | 🐍 CodeAgent |
| 🔄 Combinado | Técnica + Fundamental | Cualquiera |
| 🌙 Gaps Nocturnos | Gaps de cierre→apertura, fill intradía | Determinista o 🐍 CodeAgent resumen |
| ⚡ Momentum de Earnings | Spikes de volumen + cierre alcista | 🔧 ToolCalling o 🐍 CodeAgent |

---

## 🚀 Inicio rápido

### Requisitos previos

- Python 3.10+
- Clave de API de OpenAI (recomendada) o token de Hugging Face
- Conexión a internet (para datos de Yahoo Finance)

### Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd mcp_financial_markets_analysis_tool

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
.\venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Configurar entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Claves del LLM (elige una)
OPENAI_API_KEY=sk-tu-clave-openai
# O
HF_TOKEN=hf_tu-token

# Configuración del modelo
SMOLAGENT_MODEL_ID=gpt-4o
SMOLAGENT_MODEL_PROVIDER=litellm

# Configuración del agente
SMOLAGENT_AGENT_TYPE=code_agent
SMOLAGENT_EXECUTOR=local
SMOLAGENT_MAX_STEPS=25
SMOLAGENT_TEMPERATURE=0.1
SMOLAGENT_MAX_TOKENS=8192

# Valores opcionales
DEFAULT_ANALYSIS_PERIOD=1y
DEFAULT_SCANNER_SYMBOLS=AAPL,MSFT,GOOGL,AMZN
```

### Ejecutar la aplicación

```bash
# Terminal 1: backend FastAPI
uvicorn stock_analyzer_bot.api:app --reload --port 8000

# Terminal 2: frontend Streamlit
streamlit run streamlit_app.py
```

Abre el navegador en `http://localhost:8501`.

---

## 🔧 Componentes principales

### 1. Servidor MCP (`server/`)

El servidor MCP proporciona todas las herramientas de análisis financiero.

**Características clave:**
- 5 estrategias de análisis técnico
- Backtesting con métricas completas
- Análisis fundamental con más de 70 alias de filas
- Escáner unificado de múltiples acciones

📚 Documentación: `server/README.md`

### 2. Stock Analyzer Bot (`stock_analyzer_bot/`)

La capa de orquestación con smolagents y doble agente.

**Archivos clave:**
- `main.py` — ToolCallingAgent (herramientas de alto nivel)
- `main_codeagent.py` — CodeAgent (herramientas de bajo nivel)
- `api.py` — Endpoints FastAPI
- `tools.py` — Wrappers MCP

📚 Documentación: `stock_analyzer_bot/README.md`

### 3. Frontend Streamlit (`streamlit_app.py`)

Interfaz web con selector de agente y 7 pestañas de análisis.

---

## 📡 Referencia de API

### Selección de agente

Todos los endpoints aceptan el parámetro `agent_type`:

```json
{
  "symbol": "AAPL",
  "period": "1y",
  "agent_type": "code_agent",
  "executor_type": "local"
}
```

### Endpoints disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Estado y agentes disponibles |
| `/technical` | POST | Acción única, 4 estrategias |
| `/scanner` | POST | Comparación multi-acción |
| `/fundamental` | POST | Análisis fundamental |
| `/multisector` | POST | Comparativa entre sectores |
| `/combined` | POST | Análisis técnico + fundamental |

### Formato de respuesta

```json
{
  "report": "# AAPL Comprehensive Technical Analysis\n...",
  "symbol": "AAPL",
  "analysis_type": "technical",
  "duration_seconds": 35.2,
  "agent_type": "code_agent",
  "tools_approach": "LOW-LEVEL tools (4 strategies + Python code orchestration)"
}
```

---

## ⚙️ Configuración

### Variables de entorno

```bash
# Configuración LLM
OPENAI_API_KEY=sk-...
HF_TOKEN=hf-...
OPENAI_BASE_URL=

# Ajustes del modelo
SMOLAGENT_MODEL_ID=gpt-4o
SMOLAGENT_MODEL_PROVIDER=litellm
SMOLAGENT_TEMPERATURE=0.1
SMOLAGENT_MAX_TOKENS=8192

# Ajustes del agente
SMOLAGENT_AGENT_TYPE=code_agent
SMOLAGENT_EXECUTOR=local
SMOLAGENT_MAX_STEPS=25

# Valores por defecto
DEFAULT_ANALYSIS_PERIOD=1y
DEFAULT_SCANNER_SYMBOLS=AAPL,MSFT,GOOGL,AMZN
```

### Modelos soportados

| Proveedor | Modelo | Soporte CodeAgent |
|-----------|--------|-------------------|
| OpenAI | `gpt-4o` | ✅ Excelente |
| OpenAI | `gpt-4o-mini` | ✅ Bueno |
| OpenAI | `gpt-4-turbo` | ✅ Excelente |
| Hugging Face | `meta-llama/Llama-3.1-70B-Instruct` | ⚠️ Variable |

**Nota:** CodeAgent funciona mejor con modelos fuertes en generación de Python. GPT-4o es la opción recomendada.

### Períodos permitidos

`1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

---

## 📝 Reglas de formato de salida

| Regla | Descripción |
|-------|-------------|
| **Moneda** | Usar el prefijo "USD" en lugar del símbolo `"$"` |
| **Tablas** | Evitar caracteres de tubería en tablas (mejor legibilidad) |
| **Datos** | Un dato por línea para mayor claridad |
| **Encabezados** | Secciones numeradas y jerarquizadas |
| **Sin itálicas** | Evitar `*texto*` |

### Número de estrategias por tipo de análisis

| Tipo de análisis | Herramienta | Estrategias |
|------------------|------------|-------------|
| Análisis técnico | `comprehensive_performance_report` | 4 |
| Escáner de mercado | `unified_market_scanner` | 5 |
| Multi-sector | `unified_market_scanner` | 5 |

**Estrategias del escáner de mercado:**
1. Bollinger Bands Z-Score
2. Bollinger Bands + Fibonacci
3. MACD-Donchian combinado
4. Connors RSI + Z-Score
5. Cruce de medias móviles (EMA 50/200)

---

## 🧪 Pruebas de ambos agentes

### Comparativa rápida

```bash
# Probar ambos agentes con la misma acción
python test_codeagent.py AAPL

# Probar el escáner de mercado
python test_codeagent.py AAPL --mode scanner --symbols "AAPL,MSFT,GOOGL"
```

### En Streamlit

1. Ejecuta el análisis técnico con **ToolCallingAgent**.
2. Observa la duración en el historial.
3. Cambia a **CodeAgent**.
4. Ejecuta el mismo análisis.
5. Compara tiempos.

---

## 🔒 Seguridad y avisos

### Seguridad en la ejecución de código

Si usas CodeAgent:
- **Desarrollo**: el ejecutor `local` es suficiente.
- **Producción**: usa `e2b` o `docker` para sandboxing.
- Evita ejecutar código no confiable en `local`.

### Descargo de responsabilidad financiera

⚠️ **Importante:** Este software es solo para fines educativos e investigativos.

- Verifica cualquier resultado por tu cuenta.
- El rendimiento pasado no garantiza resultados futuros.
- Esto **no** es asesoramiento financiero.
- Consulta con un profesional antes de invertir.

---

## 🛠️ Solución de problemas

| Problema | Solución |
|----------|----------|
| "CodeAgent no disponible" | Asegúrate de que `main_codeagent.py` exista |
| "Falló la ejecución de código" | Valida la sintaxis del Python generado; usa gpt-4o |
| "Servidor MCP no encontrado" | Verifica que `server/main.py` esté en la raíz |
| "Conexión rechazada" | Inicia FastAPI con `uvicorn stock_analyzer_bot.api:app --port 8000` |
| "Timeout" | Reduce símbolos o incrementa el tiempo de espera; usa CodeAgent |
| "Agente se detuvo pronto" | Aumenta `max_steps` |
| "Salida truncada" | Sube `SMOLAGENT_MAX_TOKENS` a 8192+ |
| "Errores de formato" | Usa "USD" en lugar de `"$"` |
| "Faltan estrategias en el escáner" | Asegura que `unified_market_scanner` use modo "detailed" |

---

## 🔄 Cambios recientes

### v2.3.0 – Formato de salida y estabilidad

- Temperatura ajustada a 0.1 para respuestas deterministas.
- Límite de tokens por defecto ampliado a 8192.
- Formato de moneda cambiado a prefijo USD.
- Escáner de mercado: reactivadas MACD-Donchian y Connors RSI-ZScore.
- Plantillas: corregidos conflictos de formato en cadenas Python.
- Nuevo helper `format_agent_result()` para limpiar la salida.

### v2.2.0 – Mejoras en análisis fundamental

- Más de 70 alias para extracción robusta con yfinance.
- Matching multinivel: exacto → alias → substring difusa.
- Ratios financieros ampliados en 4 categorías.
- Manejo elegante ante ausencias de datos.

### v2.1.0 – Doble arquitectura de agentes

- Añadido CodeAgent con ejecución de código Python.
- Ejecutores disponibles: local, e2b, docker.
- Separación entre herramientas de ALTO y BAJO nivel.
- Selección de agente por petición en la API.

---

## 📚 Documentación adicional

| Documento | Descripción |
|-----------|-------------|
| [server/README.md](server/README.md) | Herramientas MCP, estrategias, parámetros |
| [stock_analyzer_bot/README.md](stock_analyzer_bot/README.md) | Implementaciones de agentes y endpoints |
| [docs/Sectors_reference.md](docs/Sectors_reference.md) | Símbolos y configuración de sectores |
| [docs/comprehensive_analysis_tool_es.md](docs/comprehensive_analysis_tool_es.md) | Reporte técnico integral de una acción (4 estrategias) |
| [docs/unified_market_scanner_tool_es.md](docs/unified_market_scanner_tool_es.md) | Escáner multiactivo de alto nivel (5 estrategias) |
| [docs/fundamental_analysis_tool_es.md](docs/fundamental_analysis_tool_es.md) | Herramienta MCP enfocada en fundamentales |
| [docs/combined_analysis_flow_es.md](docs/combined_analysis_flow_es.md) | Flujo combinado técnico + fundamental (API/agente) |
| [docs/multi_sector_analysis_flow_es.md](docs/multi_sector_analysis_flow_es.md) | Flujo de análisis multisector (API/agente) |
| [docs/overnight_gaps_strategy_es.md](docs/overnight_gaps_strategy_es.md) | Herramienta de gaps nocturnos y uso con agente |
| [docs/earnings_momentum_strategy_es.md](docs/earnings_momentum_strategy_es.md) | Estrategia de momentum de resultados |
| [docs/bollinger_fibonacci_strategy_es.md](docs/bollinger_fibonacci_strategy_es.md) | Estrategia: Bollinger + Fibonacci |
| [docs/bollinger_zscore_strategy_es.md](docs/bollinger_zscore_strategy_es.md) | Estrategia: Bollinger + Z-Score |
| [docs/macd_donchian_strategy_es.md](docs/macd_donchian_strategy_es.md) | Estrategia: MACD + Donchian |
| [docs/connors_zscore_strategy_es.md](docs/connors_zscore_strategy_es.md) | Estrategia: Connors RSI + Z-Score |
| [docs/dual_moving_average_strategy_es.md](docs/dual_moving_average_strategy_es.md) | Estrategia: Cruce de medias EMA |
| [Hugging Face Smolagents](https://huggingface.co/docs/smolagents/index) | Documentación oficial |
| [Secure Code Execution](https://huggingface.co/docs/smolagents/tutorials/secure_code_execution) | Guía de seguridad para CodeAgent |

---

## 🤝 Contribuciones

1. Haz un fork del repositorio.
2. Crea una rama de feature.
3. Implementa tus cambios.
4. Añade pruebas si aplica.
5. Envía un pull request.

### Añadir nuevos tipos de agente

1. Crea un módulo en `stock_analyzer_bot/`.
2. Replica las firmas de `main.py`.
3. Registra el nuevo tipo en `api.py`.
4. Actualiza la UI en `streamlit_app.py`.

---

## 📄 Licencia

Proyecto disponible para fines educativos. Los usuarios deben cumplir con:
- Términos de servicio de Yahoo Finance.
- Términos de OpenAI / Hugging Face.
- Regulaciones financieras locales.

---

## 🙏 Agradecimientos

- [Smolagents](https://huggingface.co/docs/smolagents/index) de Hugging Face.
- [FastMCP](https://github.com/jlowin/fastmcp) como framework MCP.
- [yfinance](https://github.com/ranaroussi/yfinance) por los datos de mercado.
- [FastAPI](https://fastapi.tiangolo.com/) por la API REST.
- [Streamlit](https://streamlit.io/) por la interfaz web.

---

<p align="center">
  <b>Construido con ❤️ usando smolagents, MCP, FastAPI y Streamlit</b><br>
  <i>Ahora con soporte dual de agentes: ToolCallingAgent y CodeAgent</i>
</p>

**Mejor Para:** "¿Cuál acción en este grupo es la mejor oportunidad?"

---

### Pestaña 3: 📊 Análisis Fundamental

**Propósito:** Analizar la salud financiera de la empresa desde sus estados financieros

**Qué Hace:**
- Recupera estado de resultados, balance general, flujo de caja
- Calcula ratios clave: P/E, ROE, deuda-capital, márgenes
- La IA interpreta la salud financiera
- Crea tesis de inversión

**Métricas Analizadas:**
- **Rentabilidad:** Ingresos, Ingreso Neto, Márgenes
- **Crecimiento:** Crecimiento de ingresos, crecimiento de ganancias
- **Liquidez:** Ratio corriente, ratio rápido
- **Apalancamiento:** Ratios de deuda, cobertura de intereses
- **Retornos:** ROE, ROA

**Mejor Para:** "¿Esta empresa es financieramente saludable?"

---

### Pestaña 4: 🌐 Análisis Multi-Sector

**Propósito:** Comparar acciones a través de diferentes sectores del mercado

**Qué Hace:**
- Analiza múltiples sectores (Banca, Tecnología, Energía Limpia, etc.)
- Ejecuta 4 estrategias en cada acción de cada sector
- Compara el rendimiento ENTRE sectores
- Identifica las mejores oportunidades de todo el universo

**Sectores Predeterminados:**
```
Banca: JPM, BAC, WFC, C, GS, MS, USB, PNC, TFC, COF
Tecnología: AAPL, MSFT, GOOGL, META, NVDA, AMD, CRM, ORCL, ADBE, INTC
Energía Limpia: TSLA, NIO, RIVN, LCID, PLUG, SEDG, NEE, ICLN, ENPH
```

**Mejor Para:** "¿Dónde debería invertir en todo el mercado?"

⚠️ **Nota:** Esto es computacionalmente intensivo (120+ llamadas de herramientas para 3 sectores × 10 acciones)

---

### Pestaña 5: 🔄 Análisis Combinado

**Propósito:** Fusionar análisis Técnico y Fundamental para una imagen completa

**Filosofía:**
- **Análisis Fundamental** = "QUÉ comprar" (calidad de la empresa)
- **Análisis Técnico** = "CUÁNDO comprar" (timing)
- **Combinado** = Vista de inversión de 360 grados

**Alineación de Señales:**
| Señal FA | Señal AT | Interpretación |
|----------|----------|----------------|
| Alcista | Alcista | ✅ Alta convicción COMPRAR |
| Alcista | Bajista | ⚠️ Buena empresa, mal timing - ESPERAR |
| Bajista | Alcista | ⚠️ Rebote técnico, fundamentos débiles - PRECAUCIÓN |
| Bajista | Bajista | ❌ Alta convicción EVITAR |

**Mejor Para:** "Dame la imagen completa de inversión"

---

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.10+
- Clave de API de OpenAI (recomendado) o token de HuggingFace
- Conexión a internet (datos de Yahoo Finance)

### Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd mcp_financial_markets_analysis_tool

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
.\venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Configuración del Entorno

Crear un archivo `.env` en la raíz del proyecto:

```bash
# Requerido - Clave API LLM (elegir una)
OPENAI_API_KEY=sk-tu-clave-openai-aqui
# O
HF_TOKEN=hf_tu-token-huggingface

# Configuración del Modelo
SMOLAGENT_MODEL_ID=gpt-4o           # Recomendado para CodeAgent
SMOLAGENT_MODEL_PROVIDER=litellm     # litellm o inference

# Configuración del Agente (NUEVO)
SMOLAGENT_AGENT_TYPE=code_agent      # tool_calling o code_agent
SMOLAGENT_EXECUTOR=local             # local, e2b, o docker
SMOLAGENT_MAX_STEPS=25               # Pasos máximos de razonamiento

# Opcional - Valores Predeterminados
DEFAULT_ANALYSIS_PERIOD=1y
DEFAULT_SCANNER_SYMBOLS=AAPL,MSFT,GOOGL,AMZN
```

### Ejecutar la Aplicación

```bash
# Terminal 1: Iniciar el backend FastAPI
uvicorn stock_analyzer_bot.api:app --reload --port 8000

# Terminal 2: Iniciar el frontend Streamlit
streamlit run streamlit_app.py
```

Abrir el navegador en `http://localhost:8501`

---

## 🔧 Componentes Principales

### 1. MCP Server (`server/`)

El **Model Context Protocol Server** proporciona todas las herramientas de análisis financiero. Es un proceso independiente al que el bot se conecta vía stdio.

**Características Clave:**
- 5 estrategias de análisis técnico
- Backtesting de rendimiento con métricas
- Análisis fundamental desde estados financieros
- Escáner de mercado multi-acción

📚 **Documentación Detallada:** [server/README.md](server/README.md)

### 2. Stock Analyzer Bot (`stock_analyzer_bot/`)

La **capa de orquestación impulsada por smolagents** con soporte dual de agentes.

**Archivos Clave:**
- `main.py` - Implementación ToolCallingAgent
- `main_codeagent.py` - Implementación CodeAgent
- `api.py` - Endpoints FastAPI con selección de agente
- `tools.py` - Wrappers de herramientas MCP

📚 **Documentación Detallada:** [stock_analyzer_bot/README.md](stock_analyzer_bot/README.md)

### 3. Frontend Streamlit (`streamlit_app.py`)

La **interfaz web** con alternancia de agente y 5 pestañas de análisis.

---

## 📡 Referencia de API

### Selección de Agente

Todos los endpoints ahora aceptan el parámetro `agent_type`:

```json
{
  "symbol": "AAPL",
  "period": "1y",
  "agent_type": "code_agent",
  "executor_type": "local"
}
```

### Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Verificación de salud, muestra agentes disponibles |
| `/technical` | POST | Acción única, 4 estrategias |
| `/scanner` | POST | Comparación multi-acción |
| `/fundamental` | POST | Análisis de estados financieros |
| `/multisector` | POST | Análisis entre sectores |
| `/combined` | POST | Técnico + Fundamental |

### Formato de Respuesta

```json
{
  "report": "# Análisis Técnico Completo de AAPL\n...",
  "symbol": "AAPL",
  "analysis_type": "technical",
  "duration_seconds": 35.2,
  "agent_type": "code_agent"
}
```

---

## ⚙️ Configuración

### Modelos LLM Soportados

| Proveedor | Model ID | Soporte CodeAgent |
|-----------|----------|-------------------|
| OpenAI | `gpt-4o` | ✅ Excelente |
| OpenAI | `gpt-4o-mini` | ✅ Bueno |
| OpenAI | `gpt-4-turbo` | ✅ Excelente |
| HuggingFace | `meta-llama/Llama-3.1-70B-Instruct` | ⚠️ Variable |

**Nota:** CodeAgent funciona mejor con modelos que tienen fuertes habilidades de generación de código Python. Se recomienda GPT-4o.

### Períodos de Análisis

Períodos válidos: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

---

## 🧪 Probando Ambos Agentes

### Comparación Rápida

```bash
# Probar ambos agentes en la misma acción
python test_codeagent.py AAPL

# Probar en escáner de mercado
python test_codeagent.py AAPL --mode scanner --symbols "AAPL,MSFT,GOOGL"
```

### En Streamlit

1. Ejecutar Análisis Técnico con **ToolCallingAgent**
2. Anotar la duración en Historial
3. Cambiar a **CodeAgent** en la barra lateral
4. Ejecutar el mismo análisis
5. Comparar tiempos

### Parámetros de Estrategia

| Estrategia | Parámetros Clave |
|------------|------------------|
| Bollinger-Fibonacci | window=20, num_std=2 |
| MACD-Donchian | fast=12, slow=26, signal=9 |
| Connors RSI | rsi_period=3, streak=2, rank=100 |
| Dual MA | short=50, long=200, type=EMA |

---

## 🧪 Ejemplos de Informes

### Estructura del Informe de Análisis Técnico

```markdown
# Análisis Técnico Completo de AAPL
*Fecha de Análisis: 2024-01-15*
*Precio Actual: $185.92*

## Resumen Ejecutivo
[2-3 párrafos sintetizando todos los hallazgos de las estrategias]

## Comparación de Rendimiento de Estrategias
| Estrategia | Señal | Puntaje | Retorno | Sharpe | DD Máx |
|------------|-------|---------|---------|--------|--------|
| Bollinger-Fib | COMPRA | +45 | 12.3% | 1.2 | -8.5% |
| MACD-Donchian | MANTENER | +15 | 8.1% | 0.9 | -12.1% |
| ... | ... | ... | ... | ... | ... |

## Análisis Individual de Estrategias
[Desglose detallado de cada estrategia]

## Evaluación de Riesgo
[Análisis de volatilidad y caída]

## Recomendación Final: **COMPRAR**
[Razonamiento de apoyo]
```

---

## 🔒 Seguridad y Descargos de Responsabilidad

### Seguridad de Ejecución de Código

Cuando se usa CodeAgent:
- **Desarrollo**: El ejecutor `local` está bien
- **Producción**: Usar `e2b` o `docker` para ejecución en sandbox
- Nunca ejecutar código no confiable en ejecutor local

### Seguridad de Claves API

- Nunca envíes archivos `.env` al control de versiones
- Usa variables de entorno para todos los datos sensibles
- Las claves API nunca se registran ni almacenan

### Descargo de Responsabilidad Financiera

⚠️ **IMPORTANTE:** Este software es solo para **fines educativos e investigación**.

- Todos los resultados de análisis deben ser verificados independientemente
- El rendimiento pasado no garantiza resultados futuros
- Esto NO es asesoría financiera
- Consulta un asesor financiero licenciado antes de invertir

---

## 🛠️ Solución de Problemas

| Problema | Solución |
|----------|----------|
| "CodeAgent not available" | Asegúrate de que `main_codeagent.py` existe en `stock_analyzer_bot/` |
| "Code execution failed" | Verifica sintaxis Python en salida LLM, prueba diferente modelo |
| "MCP server not found" | Verifica que `server/main.py` existe en la raíz del proyecto |
| "Timeout" | Reduce acciones o aumenta timeout; usa CodeAgent para multi-acción |
| "Agent stopped early" | Aumenta el parámetro `max_steps` |

---

## 📚 Documentación Adicional

| Documento | Descripción |
|-----------|-------------|
| [server/README.md](server/README.md) | Herramientas del MCP Server, estrategias, parámetros |
| [stock_analyzer_bot/README.md](stock_analyzer_bot/README.md) | Implementaciones de agentes, endpoints API |
| [docs/Sectors_reference.md](docs/Sectors_reference.md) | Símbolos de sectores y configuración |
| [docs/comprehensive_analysis_tool_es.md](docs/comprehensive_analysis_tool_es.md) | Reporte técnico integral de una acción (4 estrategias) |
| [docs/unified_market_scanner_tool_es.md](docs/unified_market_scanner_tool_es.md) | Escáner multiactivo de alto nivel (5 estrategias) |
| [docs/fundamental_analysis_tool_es.md](docs/fundamental_analysis_tool_es.md) | Herramienta MCP enfocada en fundamentales |
| [docs/combined_analysis_flow_es.md](docs/combined_analysis_flow_es.md) | Flujo combinado técnico + fundamental (API/agente) |
| [docs/multi_sector_analysis_flow_es.md](docs/multi_sector_analysis_flow_es.md) | Flujo de análisis multisector (API/agente) |
| [docs/overnight_gaps_strategy_es.md](docs/overnight_gaps_strategy_es.md) | Herramienta de gaps nocturnos y uso con agente |
| [docs/trin_strategy_es.md](docs/trin_strategy_es.md) | Herramienta de amplitud TRIN y uso con agente |
| [docs/bollinger_fibonacci_strategy_es.md](docs/bollinger_fibonacci_strategy_es.md) | Estrategia: Bollinger + Fibonacci |
| [docs/bollinger_zscore_strategy_es.md](docs/bollinger_zscore_strategy_es.md) | Estrategia: Bollinger + Z-Score |
| [docs/macd_donchian_strategy_es.md](docs/macd_donchian_strategy_es.md) | Estrategia: MACD + Donchian |
| [docs/connors_zscore_strategy_es.md](docs/connors_zscore_strategy_es.md) | Estrategia: Connors RSI + Z-Score |
| [docs/dual_moving_average_strategy_es.md](docs/dual_moving_average_strategy_es.md) | Estrategia: Cruce de medias EMA |
| [HuggingFace Smolagents](https://huggingface.co/docs/smolagents/index) | Documentación oficial de smolagents |
| [Secure Code Execution](https://huggingface.co/docs/smolagents/tutorials/secure_code_execution) | Guía de seguridad de CodeAgent |

---

## 🤝 Contribuir

1. Haz fork del repositorio
2. Crea una rama de característica
3. Implementa tus cambios
4. Agrega pruebas si aplica
5. Envía un pull request

### Agregar Nuevos Tipos de Agentes

La arquitectura soporta agregar nuevos tipos de agentes:

1. Crear nuevo módulo en `stock_analyzer_bot/`
2. Implementar las mismas firmas de función que `main.py`
3. Registrar en `api.py` con nueva opción de tipo de agente
4. Actualizar UI en `streamlit_app.py`

---

## 📄 Licencia

Este proyecto se proporciona para fines educativos. Los usuarios deben cumplir con:
- Términos de Servicio de Yahoo Finance
- Términos de Servicio de OpenAI / HuggingFace
- Regulaciones financieras locales aplicables

---

## 🙏 Agradecimientos

- [Smolagents](https://huggingface.co/docs/smolagents/index) por Hugging Face
- [FastMCP](https://github.com/jlowin/fastmcp) por el framework MCP
- [yfinance](https://github.com/ranaroussi/yfinance) por los datos de mercado
- [FastAPI](https://fastapi.tiangolo.com/) por la API REST
- [Streamlit](https://streamlit.io/) por la interfaz web

---

<p align="center">
  <b>Construido con ❤️ usando smolagents, MCP, FastAPI y Streamlit</b><br>
  <i>Ahora con soporte dual de agentes: ToolCallingAgent y CodeAgent</i>
</p>
