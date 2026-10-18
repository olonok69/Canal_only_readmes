# 📊 Herramienta de Análisis de Mercados Financieros MCP

Una plataforma de análisis financiero impulsada por IA que combina **Model Context Protocol (MCP)**, **Google ADK**, **FastAPI** y **Django UI** para entregar informes de inversión de nivel profesional. El sistema utiliza orquestación multiagente para interpretar salidas de estrategias MCP y generar reportes validados por guardrails.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Google%20ADK-0.7+-red.svg" alt="Google ADK">
  <img src="https://img.shields.io/badge/MCP-1.0+-purple.svg" alt="MCP">
  <img src="https://img.shields.io/badge/Django-5.1+-orange.svg" alt="Django">
</p>

---

## 🎯 Descripción General

Esta aplicación ofrece **8 rutas de análisis + 11 rutas de estrategia standalone** desde una interfaz web moderna (**19 rutas funcionales**, excluyendo `/health`):

| Tipo de análisis | Descripción | Caso de uso |
|------------------|-------------|-------------|
| **📈 Análisis Técnico** | Consenso de estrategias o síntesis por score sobre una acción | Profundizar en patrones de precios |
| **🔍 Escáner de Mercado** | Compara varias acciones de forma simultánea | Encontrar mejores oportunidades |
| **💰 Análisis Fundamental** | Interpretación de estados financieros | Evaluar la salud de la compañía |
| **🌐 Análisis Multi-Sector** | Comparación entre sectores | Diversificar la cartera |
| **🔄 Análisis Combinado** | Técnico + Fundamental juntos | Construir una tesis completa |
| **📊 Amplitud TRIN** | Arms Index con bandas móviles y contexto de señal | Lectura de amplitud / risk-on risk-off |
| **🌙 Gaps Nocturnos** | Cierre previo vs apertura, tasas de fill intradía, drift diario | Comportamiento de gaps/midnight returns |
| **⚡ Momentum de Earnings** | Escáner de spikes de volumen con ventana fija | Detectar rupturas tras resultados |

## 🧪 Estrategias implementadas (explícito)

Rutas de análisis expuestas actualmente:

- `POST /technical`
- `POST /scanner`
- `POST /fundamental`
- `POST /multisector`
- `POST /combined`
- `POST /trin` — [Flujo TRIN](docs/trin_strategy_es.md)
- `POST /overnight_gaps` — [Gaps Nocturnos](docs/overnight_gaps_strategy_es.md)
- `POST /earnings_momentum` — [Momentum de Earnings](docs/earnings_momentum_strategy_es.md)

Rutas de estrategia standalone expuestas actualmente:

- `POST /bollinger_breakout` — [Bollinger Breakout](docs/bollinger_breakout_strategy.md)
- `POST /gap_fade` — [Gap Fade](docs/gap_fade_strategy.md)
- `POST /multi_timeframe` — [Multi Timeframe](docs/multi_timeframe_strategy.md)
- `POST /pairs_trading` — [Pairs Trading](docs/pairs_trading_strategy.md)
- `POST /statistical_arbitrage` — [Statistical Arbitrage](docs/statistical_arbitrage_strategy.md)
- `POST /vix_term_structure` — [VIX Term Structure](docs/vix_term_structure_strategy.md)
- `POST /volatility_regime` — [Volatility Regime](docs/volatility_regime_strategy.md)
- `POST /bollinger_zscore_rsi` — [Bollinger Z-Score RSI](docs/bollinger_zscore_rsi_strategy.md)
- `POST /bollinger_fibonacci` — [Bollinger + Fibonacci](docs/bollinger_fibonacci_strategy_es.md)
- `POST /macd_donchian` — [MACD + Donchian](docs/macd_donchian_strategy_es.md)
- `POST /dual_moving_average` — [Dual Moving Average](docs/dual_moving_average_strategy_es.md)

Referencia completa de taxonomía: [analysis_strategy_catalog.md](docs/analysis_strategy_catalog.md)

Referencia de clasificación de scoring: [strategy_scoring_classification_es.md](docs/strategy_scoring_classification_es.md)

### Familias de estrategias registradas (MCP)

Familias de estrategia MCP actualmente usadas de forma directa o dentro de rutas de análisis:

1. Bollinger-Fibonacci
2. MACD-Donchian
3. Connors-ZScore
4. Dual Moving Average
5. Bollinger Z-Score
6. Bollinger Z-Score RSI
7. TRIN (Arms Index)
8. Overnight Gaps
9. Earnings Momentum
10. Bollinger Breakout
11. Gap Fade
12. Multi-Timeframe
13. Pairs Trading
14. Statistical Arbitrage
15. VIX Term Structure
16. Volatility Regime

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

## 🤖 Arquitectura actual de agentes (ADK)

El runtime actual de la aplicación es **ADK-first**.

- Los endpoints FastAPI llaman a la orquestación ADK en `stock_analyzer_bot/adk_bot.py`.
- Los agentes ADK (orquestador, especialista, crítico y reportero) consumen la salida MCP y construyen el informe final.
- Los guardrails de taxonomía se aplican con `docs/analysis_strategy_catalog.json`.
- Los archivos legacy de smolagents quedan como referencia histórica, pero no son la ruta backend activa.

<p align="center">
  <img src="docs/architecture_adk.svg" alt="Arquitectura ADK" width="900">
</p>

- Arquitectura runtime completa: [docs/architecture_adk.svg](docs/architecture_adk.svg)

<p align="center">
  <img src="docs/architecture_adk_agents_workflow.svg" alt="Flujo de agentes ADK" width="900">
</p>

- Flujo de agentes (enfoque específico): [docs/architecture_adk_agents_workflow.svg](docs/architecture_adk_agents_workflow.svg)

### Resumen del flujo ADK

1. **Django UI / cliente HTTP** envía la petición a FastAPI.
2. **FastAPI** ejecuta herramientas MCP determinísticas y pipeline ADK.
3. **Pipeline ADK** corre orquestador → especialista → crítico → reportero.
4. **Guardrails** validan taxonomía (analysis vs strategy) y pueden reescribir/bloquear respuestas inválidas.
5. **Respuesta** devuelve reporte final + metadatos/timeseries.

### Ciclo concreto de una solicitud (ejemplo técnico)

Usa esta secuencia para una llamada real a `/technical` desde la UI hasta el reporte final.

1. **La UI construye endpoint y payload**
  - `django_ui/analyzer/views.py` → `_payload_from_action(action, post_data)`
  - Para `action == "technical"`, arma `symbol`, `period`, `technical_mode`, `risk_profile`.

2. **La UI envía la solicitud HTTP al backend**
  - `django_ui/analyzer/services.py` → `call_backend(api_url, endpoint, payload)`
  - Ejecuta `POST {api_url}/technical`.

3. **FastAPI valida y despacha al runner**
  - `stock_analyzer_bot/api.py` → `TechnicalAnalysisRequest`
  - `stock_analyzer_bot/api.py` → `technical_analysis(request)`
  - La ruta llama a `run_technical_analysis(...)` vía `run_in_threadpool(...)`.

4. **El runtime ADK obtiene output MCP determinístico**
  - `stock_analyzer_bot/adk_bot.py` → `run_technical_analysis(...)`
  - En modo score llama a `comprehensive_performance_report(symbol, period)`.

5. **El wrapper MCP invoca la tool por nombre**
  - `stock_analyzer_bot/mcp_tools.py` → `_call_finance_tool(tool_name, parameters)`
  - Tool usada en esta ruta: `generate_comprehensive_analysis_report`.

6. **El cliente MCP abre/usa sesión stdio y ejecuta la invocación**
  - `stock_analyzer_bot/mcp_client.py` → `MCPFinanceSession`
  - Ruta de invocación: `call_tool(...)` → `_async_call_tool(...)` → `self._session.call_tool(...)`.

7. **El servidor MCP hospeda y enruta la implementación**
  - `server/main.py` crea `FastMCP("finance tools", "1.0.0")`
  - `register_all_tools(mcp)` registra capacidades desde `server/tool_registry.py`
  - El servidor corre por stdio con `mcp.run(transport='stdio')`.

8. **La implementación concreta se ejecuta y devuelve salida raw**
  - `server/strategies/performance_tools.py` registra `generate_comprehensive_analysis_report(symbol, period)` con `@mcp.tool()`.

9. **El pipeline multiagente ADK produce reporte gobernado**
  - `stock_analyzer_bot/adk_bot.py` → `_run_pipeline_sync(...)`
  - `AgenticFinancePipeline.execute(...)` ejecuta orquestador → especialista → crítico → reportero.
  - Guardrails aplican validaciones de taxonomía y modo antes de devolver resultado.

10. **La respuesta vuelve a la UI y puede persistirse**
   - La API retorna envelope (`report`, `symbol`, `analysis_type`, `duration_seconds`, etc.).
   - Django `index(request)` guarda historial en sesión y puede persistir `SavedReport`.

<p align="center">
  <img src="docs/technical.png" alt="Ciclo de solicitud técnica" width="900">
</p>

### Rama scanner por modo (strategy vs score)

- `scanner_mode` define la ruta de formato en `run_market_scanner(...)`:
  - `strategy` → `output_format="detailed"`
  - `score` → `output_format="summary"`
- Ambos caminos llaman a `unified_market_scanner(...)` y luego al mismo pipeline ADK con guardrails.

Leyenda:
- `technical_mode` aplica a `/technical` y al bloque técnico dentro de `/combined`.
- `scanner_mode` aplica a `/scanner` y `/multisector`.
- Ambos aceptan `strategy | score`, pero gobiernan familias de rutas distintas.

<p align="center">
  <img src="docs/scanner.png" alt="Rama de modo scanner" width="900">
</p>

---

## 🏗️ Descripción general de la arquitectura

### Estructura de carpetas

```
mcp_financial_markets_analysis_tool/
│
├── server/                          # Servidor MCP (herramientas financieras)
│   ├── main.py                      # Punto de entrada del servidor
│   ├── strategies/                  # Implementaciones de estrategias
│   │   ├── bollinger_breakout.py    # Estrategia de ruptura Bollinger
│   │   ├── bollinger_fibonacci.py   # Bollinger + Fibonacci
│   │   ├── macd_donchian.py         # MACD + Donchian
│   │   ├── connors_zscore.py        # Connors RSI + Z-Score
│   │   ├── dual_moving_average.py   # Cruce EMA 50/200
│   │   ├── bollinger_zscore.py      # Bollinger + Z-Score
│   │   ├── bollinger_zscore_rsi.py  # Bollinger + Z-Score + RSI
│   │   ├── gap_fade.py              # Gap fade intradía
│   │   ├── multi_timeframe.py       # Tendencia multi-timeframe
│   │   ├── pairs_trading.py         # Mean reversion por pares
│   │   ├── statistical_arbitrage.py # Arbitraje estadístico de cesta
│   │   ├── vix_term_structure.py    # Estrategia por curva de volatilidad
│   │   ├── volatility_regime.py     # Estrategia por régimen de volatilidad
│   │   ├── trin_strategy.py         # Estrategia de amplitud TRIN
│   │   ├── overnight_gaps.py        # Análisis de gaps nocturnos
│   │   ├── earnings_momentum.py     # Escáner momentum de earnings
│   │   ├── fundamental_analysis.py  # Estados financieros con alias
│   │   ├── performance_tools.py     # Herramientas de backtesting
│   │   └── unified_market_scanner.py# Escáner multi-acción
│   ├── utils/
│   │   └── yahoo_finance_tools.py   # Datos e indicadores de mercado
│   └── README.md                    # 📚 Documentación detallada del servidor
│
├── stock_analyzer_bot/              # Runtime de orquestación ADK
│   ├── __init__.py
│   ├── adk_bot.py                   # Pipeline multiagente ADK + guardrails
│   ├── adk_bridge.py                # Helpers de integración ADK
│   ├── main.py                      # Exportaciones ADK (compat)
│   ├── api.py                       # Endpoints FastAPI
│   ├── mcp_tools.py                 # Wrappers MCP usados por ADK
│   ├── mcp_client.py                # Gestor de conexión MCP
│   └── README.md                    # 📚 Documentación detallada del bot
│
├── django_ui/                       # Frontend principal (Django)
│   └── analyzer/
│
├── docs/
│   ├── architecture_adk.svg         # Diagrama del runtime ADK
│   ├── architecture_adk_agents_workflow.svg # Diagrama del flujo de agentes ADK
│   └── Sectors_reference.md         # Referencia de sectores
│
├── streamlit_app.py                 # UI legacy (opcional)
├── .env                             # Variables de entorno
├── requirements.txt                 # Dependencias
└── README.md                        # 📚 Este archivo
```

### Flujo de datos

Flujo actual ADK:

1. **Django UI / cliente HTTP** envía la solicitud.
2. **FastAPI** valida y enruta la petición.
3. **Herramientas MCP** calculan métricas y series temporales.
4. **Pipeline ADK** sintetiza, critica y formatea el informe.
5. **Guardrails** validan taxonomía y grounding de métricas.
6. **Cliente** recibe reporte final + metadatos.

---

## 🤖 Notas del runtime ADK

- Orquestación activa con Google ADK en `stock_analyzer_bot/adk_bot.py`.
- Salida grounded en herramientas MCP y catálogo de taxonomía.
- Frontend operativo principal: `django_ui/`.

---

## 🔐 Seguridad y almacenamiento de datos

Comportamiento actual de persistencia en la capa Django UI:

- **Cuentas de usuario:** Se almacenan en `django_ui/db.sqlite3` mediante Django Auth con **hashes de contraseña con sal** (nunca texto plano).
- **Reportes guardados:** Se almacenan en el modelo `SavedReport` (`title`, `analysis_type`, `symbol`, `duration_seconds`, `agent_type`, `markdown_report`, timestamps).
- **Configuración/tema/historial UI:** Se almacenan en sesión Django (`ui_settings`, `ui_theme`, `analysis_history`, `latest_result`).
- **Contexto de sesión ADK:** Es en memoria para cada ejecución (no persistente entre reinicios del proceso, salvo que configures backend externo de sesiones).

Notas operativas:

- No subas `django_ui/db.sqlite3` a repositorios públicos.
- Para producción multiusuario, usa backends de DB/sesión de nivel productivo (por ejemplo PostgreSQL + Redis).
- Mantén API keys en variables de entorno y evita guardar secretos en reportes.

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
ADK_MODEL_ID=gpt-4.1
ADK_MODEL_PROVIDER=openai

# Valores opcionales
DEFAULT_ANALYSIS_PERIOD=1y
DEFAULT_SCANNER_SYMBOLS=AAPL,MSFT,GOOGL,AMZN
```

### Ejecutar la aplicación

```bash
# Terminal 1: backend FastAPI
uvicorn stock_analyzer_bot.api:app --reload --port 8000

# Terminal 2: frontend Django
python django_ui/manage.py runserver
```

Abre el navegador en `http://127.0.0.1:8000` (Django UI) o llama directamente los endpoints API.

---

## 🔧 Componentes principales

### 1. Servidor MCP (`server/`)

El servidor MCP proporciona todas las herramientas de análisis financiero.

**Características clave:**
- Cobertura de análisis y estrategias standalone según taxonomía ADK/MCP
- Backtesting con métricas completas
- Análisis fundamental con más de 70 alias de filas
- Escáner unificado de múltiples acciones

📚 Documentación: `server/README.md`

### 2. Stock Analyzer Bot (`stock_analyzer_bot/`)

La capa de orquestación con ADK.

**Archivos clave:**
- `adk_bot.py` — Pipeline ADK multiagente y guardrails
- `api.py` — Endpoints FastAPI
- `mcp_tools.py` — Wrappers MCP usados por ADK
- `mcp_client.py` — Ciclo de vida de sesión MCP

📚 Documentación: `stock_analyzer_bot/README.md`

### 3. Frontend Django (`django_ui/`)

La interfaz web principal para operación diaria.

---

## 📡 Referencia de API

### Runtime del agente

Todos los endpoints usan runtime ADK (`agent_type` se mantiene por compatibilidad):

```json
{
  "symbol": "AAPL",
  "period": "1y",
  "technical_mode": "strategy",
  "risk_profile": "balanced",
  "agent_type": "adk_agentic"
}
```

`technical_mode` aplica solo a `POST /technical` y soporta:
- `strategy` (por defecto): síntesis desde salidas de estrategias standalone
- `score`: salida de modelo de scoring de alto nivel

`risk_profile` aplica solo a `POST /technical` y soporta:
- `conservative`: enfoque más estricto en control de downside
- `balanced` (por defecto): balance riesgo/retorno
- `aggressive`: adopción más rápida de señales con mayor tolerancia a riesgo

`scanner_mode`/`multisector_mode` y `technical_mode` (dentro de `POST /combined`) soportan:
- `strategy` (por defecto): enfoque por consenso de estrategias
- `score`: enfoque por síntesis de scoring

`risk_profile` también está disponible en `POST /scanner`, `POST /multisector` y `POST /combined`
(en combined aplica al bloque técnico).

`tools_approach` en las respuestas API también depende del modo en esas rutas:
- `strategy`: `MCP tools + ADK strategy-consensus review`
- `score`: `MCP tools + ADK score-synthesis review`

### Endpoints disponibles

| Endpoint | Método | Tipo | Descripción |
|----------|--------|------|-------------|
| `/health` | GET | Sistema | Estado y agentes disponibles |
| `/technical` | POST | Analysis | Reporte técnico de acción única con `technical_mode` (`strategy`/`score`) y `risk_profile` (`conservative`/`balanced`/`aggressive`) |
| `/scanner` | POST | Analysis | Comparación multi-acción con `scanner_mode` (`strategy`/`score`) y `risk_profile` |
| `/fundamental` | POST | Analysis | Análisis de estados financieros |
| `/multisector` | POST | Analysis | Comparativa entre sectores con `multisector_mode` (`strategy`/`score`) y `risk_profile` |
| `/combined` | POST | Analysis | Análisis técnico + fundamental con `technical_mode` (`strategy`/`score`) y `risk_profile` para el bloque técnico |
| `/earnings_momentum` | POST | Analysis | Escáner de momentum por volumen en earnings |
| `/trin` | POST | Analysis | Análisis de amplitud de mercado (TRIN) |
| `/overnight_gaps` | POST | Analysis | Análisis de comportamiento de gaps nocturnos |
| `/bollinger_breakout` | POST | Strategy | Reporte estrategia Bollinger breakout |
| `/gap_fade` | POST | Strategy | Reporte estrategia gap fade |
| `/multi_timeframe` | POST | Strategy | Reporte estrategia multi-timeframe |
| `/pairs_trading` | POST | Strategy | Reporte estrategia pairs trading |
| `/statistical_arbitrage` | POST | Strategy | Reporte estrategia statistical arbitrage |
| `/vix_term_structure` | POST | Strategy | Reporte estrategia curva VIX |
| `/volatility_regime` | POST | Strategy | Reporte estrategia régimen de volatilidad |
| `/bollinger_zscore_rsi` | POST | Strategy | Reporte Bollinger + Z-Score + RSI |
| `/bollinger_fibonacci` | POST | Strategy | Reporte Bollinger + Fibonacci |
| `/macd_donchian` | POST | Strategy | Reporte MACD + Donchian |
| `/dual_moving_average` | POST | Strategy | Reporte de cruce de medias móviles |

### Formato de respuesta

```json
{
  "report": "# AAPL Comprehensive Technical Analysis\n...",
  "symbol": "AAPL",
  "analysis_type": "technical",
  "duration_seconds": 35.2,
  "agent_type": "adk_agentic",
  "tools_approach": "MCP tools + ADK multi-agent review"
}
```

Para rutas con modo (`/technical`, `/scanner`, `/multisector` y el bloque técnico de `/combined`),
el reporte comienza con una línea de metadatos determinística, por ejemplo:

- `> Mode used: Technical=strategy | risk=balanced`
- `> Mode used: Scanner=score | risk=aggressive`

---

## ⚙️ Configuración

### Variables de entorno

```bash
# Configuración LLM
OPENAI_API_KEY=sk-...
HF_TOKEN=hf-...
OPENAI_BASE_URL=

# Ajustes del modelo ADK
ADK_MODEL_ID=gpt-4.1
ADK_MODEL_PROVIDER=openai

# Valores por defecto
DEFAULT_ANALYSIS_PERIOD=1y
DEFAULT_SCANNER_SYMBOLS=AAPL,MSFT,GOOGL,AMZN
```

### Modelos soportados

| Proveedor | Modelo | Soporte runtime ADK |
|-----------|--------|---------------------|
| OpenAI | `gpt-4.1` | ✅ Recomendado |
| OpenAI | `gpt-4o` | ✅ Soportado |
| OpenAI | `gpt-4o-mini` | ✅ Soportado |
| Otros vía LiteLLM | provider/model | ⚠️ Validar calidad |

**Nota:** Prioriza modelos estables para mejor consistencia de crítica y reporte.

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
| Análisis técnico (`technical_mode=strategy`) | `bollinger_fibonacci` + `macd_donchian` + `dual_moving_average` + `bollinger_zscore_rsi` | 4 |
| Análisis técnico (`technical_mode=score`) | `comprehensive_performance_report` | modelo de scoring sintetizado de 4 estrategias |
| Escáner de mercado | `unified_market_scanner` | 5 |
| Multi-sector | `unified_market_scanner` | 5 |

**Estrategias del escáner de mercado:**
1. Bollinger Bands Z-Score
2. Bollinger Bands + Fibonacci
3. MACD-Donchian combinado
4. Connors RSI + Z-Score
5. Cruce de medias móviles (EMA 50/200)

---

## 🧪 Pruebas

### Smoke tests de API

```bash
python -c "import requests; r=requests.post('http://127.0.0.1:8000/technical', json={'symbol':'AAPL','period':'1y'}); print(r.status_code); print(r.json().get('analysis_type'))"
python -c "import requests; r=requests.post('http://127.0.0.1:8000/technical', json={'symbol':'AAPL','period':'1y','technical_mode':'score'}); print(r.status_code); print(r.json().get('analysis_type'))"
python -c "import requests; r=requests.post('http://127.0.0.1:8000/technical', json={'symbol':'AAPL','period':'1y','technical_mode':'strategy','risk_profile':'conservative'}); print(r.status_code); print(r.json().get('tools_approach'))"
python -c "import requests; r=requests.post('http://127.0.0.1:8000/scanner', json={'symbols':'AAPL,MSFT,NVDA','period':'1y','scanner_mode':'score','risk_profile':'aggressive'}); print(r.status_code); print(r.json().get('tools_approach'))"
python -c "import requests; r=requests.post('http://127.0.0.1:8000/multisector', json={'period':'1y','multisector_mode':'strategy','risk_profile':'conservative','sectors':[{'name':'Tech','symbols':'AAPL,MSFT,NVDA'},{'name':'Financials','symbols':'JPM,BAC,GS'}]}); print(r.status_code); print(r.json().get('analysis_type'))"
python -c "import requests; r=requests.post('http://127.0.0.1:8000/combined', json={'symbol':'AAPL','technical_period':'1y','fundamental_period':'3y','technical_mode':'score','risk_profile':'balanced'}); print(r.status_code); print(r.json().get('tools_approach'))"
python -c "import requests; r=requests.post('http://127.0.0.1:8000/macd_donchian', json={'symbol':'AAPL','period':'5y','fast_period':12,'slow_period':26,'signal_period':9,'window':20}); print(r.status_code); print(r.json().get('analysis_type'))"
```

### Verificación de compilación

```bash
python -m py_compile stock_analyzer_bot/adk_bot.py stock_analyzer_bot/api.py
```

---

## 🔒 Seguridad y avisos

### Seguridad del runtime

- Mantén credenciales en `.env` y fuera de reportes/logs.
- Conserva guardrails de taxonomía activos.
- Evita claims no respaldados por métricas MCP.

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
| "Servidor MCP no encontrado" | Verifica que `server/main.py` esté en la raíz |
| "Conexión rechazada" | Inicia FastAPI con `uvicorn stock_analyzer_bot.api:app --port 8000` |
| "Timeout" | Reduce alcance de símbolos o incrementa timeout del cliente |
| "Bloqueo de guardrail" | Revisa taxonomía y grounding de métricas MCP |
| "Agente se detuvo pronto" | Reintenta con modelo más robusto |
| "Salida truncada" | Reduce verbosidad y tamaño de prompt |
| "Errores de formato" | Usa "USD" en lugar de `"$"` |
| "Faltan estrategias en el escáner" | Asegura que `unified_market_scanner` use modo "detailed" |

---

## 🔄 Cambios recientes

### v4.x – Consolidación ADK

- Runtime ADK-first para todas las rutas API.
- Catálogo analysis/strategy para gobernanza.
- Enforcement crítico + post-check determinístico.
- Documentación y arquitectura actualizadas.

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
| [docs/bollinger_breakout_strategy.md](docs/bollinger_breakout_strategy.md) | Estrategia standalone: Bollinger breakout |
| [docs/gap_fade_strategy.md](docs/gap_fade_strategy.md) | Estrategia standalone: gap fade intradía |
| [docs/multi_timeframe_strategy.md](docs/multi_timeframe_strategy.md) | Estrategia standalone: tendencia multi-timeframe |
| [docs/pairs_trading_strategy.md](docs/pairs_trading_strategy.md) | Estrategia standalone: pairs trading |
| [docs/statistical_arbitrage_strategy.md](docs/statistical_arbitrage_strategy.md) | Estrategia standalone: arbitraje estadístico |
| [docs/vix_term_structure_strategy.md](docs/vix_term_structure_strategy.md) | Estrategia standalone: curva VIX |
| [docs/volatility_regime_strategy.md](docs/volatility_regime_strategy.md) | Estrategia standalone: régimen de volatilidad |
| [docs/bollinger_zscore_rsi_strategy.md](docs/bollinger_zscore_rsi_strategy.md) | Estrategia standalone: Bollinger + Z-Score + RSI |
| [docs/bollinger_fibonacci_strategy_es.md](docs/bollinger_fibonacci_strategy_es.md) | Estrategia: Bollinger + Fibonacci |
| [docs/bollinger_zscore_strategy_es.md](docs/bollinger_zscore_strategy_es.md) | Estrategia: Bollinger + Z-Score |
| [docs/macd_donchian_strategy_es.md](docs/macd_donchian_strategy_es.md) | Estrategia: MACD + Donchian |
| [docs/connors_zscore_strategy_es.md](docs/connors_zscore_strategy_es.md) | Estrategia: Connors RSI + Z-Score |
| [docs/dual_moving_average_strategy_es.md](docs/dual_moving_average_strategy_es.md) | Estrategia: Cruce de medias EMA |
| [docs/strategy_scoring_classification_es.md](docs/strategy_scoring_classification_es.md) | Clasificación score-driven vs rule-driven de estrategias MCP |
| [docs/analysis_strategy_catalog.md](docs/analysis_strategy_catalog.md) | Taxonomía oficial analysis/strategy |
| [docs/analysis_strategy_catalog.json](docs/analysis_strategy_catalog.json) | Contrato machine-readable de guardrails |

---

## 🤝 Contribuciones

1. Haz un fork del repositorio.
2. Crea una rama de feature.
3. Implementa tus cambios.
4. Añade pruebas si aplica.
5. Envía un pull request.

### Añadir nuevo análisis/estrategia

1. Registra herramienta MCP en `server/strategies/` + `server/tool_registry.py`.
2. Añade wrapper en `stock_analyzer_bot/mcp_tools.py`.
3. Añade runner ADK en `stock_analyzer_bot/adk_bot.py`.
4. Añade endpoint en `stock_analyzer_bot/api.py`.
5. Añade entrada en `docs/analysis_strategy_catalog.json`.

---

## 📄 Licencia

Proyecto disponible para fines educativos. Los usuarios deben cumplir con:
- Términos de servicio de Yahoo Finance.
- Términos de OpenAI / Hugging Face.
- Regulaciones financieras locales.

---

## 🙏 Agradecimientos

- Google ADK para orquestación multiagente.
- [FastMCP](https://github.com/jlowin/fastmcp) como framework MCP.
- [yfinance](https://github.com/ranaroussi/yfinance) por los datos de mercado.
- [FastAPI](https://fastapi.tiangolo.com/) por la API REST.
- Django por la interfaz web principal.

---

<p align="center">
  <b>Construido con ❤️ usando Google ADK, MCP, FastAPI y Django</b>
</p>
