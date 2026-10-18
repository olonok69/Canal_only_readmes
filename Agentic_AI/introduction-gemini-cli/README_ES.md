# Gemini CLI + Financial MCP Toolkit

Este repositorio combina:

- Un **Gemini CLI workflow** (skills, memory, planning, automation).
- Un **financial MCP server** de nivel producción (`server/`) con 15+ herramientas de strategy/fundamental.
- Una **ADK/FastAPI orchestration API** (`stock_analyzer_bot/`) que consume herramientas MCP.

Este README está alineado con `GEMINI_CLI_GUIDE_EN.md` y `CLI material.txt`, con ejemplos adaptados a este codebase.

---

## Estructura del repositorio

```text
.
├── server/                    # MCP server + capa OpenAPI opcional
│   ├── main.py                # MCP entrypoint (FastMCP stdio)
│   ├── api_main.py            # interfaz REST/OpenAPI para analysis tools
│   ├── tool_registry.py       # registro central de tools
│   └── strategies/            # módulos de strategy + scanner + fundamental
├── stock_analyzer_bot/        # ADK multi-agent API sobre MCP tools
│   ├── api.py                 # FastAPI endpoints (technical/scanner/fundamental/etc.)
│   ├── adk_bot.py             # pipeline orchestrator/specialist/critic/reporter
│   └── mcp_tools.py           # wrappers determinísticos para llamadas MCP
├── skills-cli/                # assets reutilizables de skills (security-review)
├── test_outputs/              # ejemplos de salidas de analysis
├── GEMINI.md                  # instrucciones persistentes de comportamiento del proyecto
├── GEMINI_CLI_GUIDE_EN.md     # guía principal de referencia
└── CLI material.txt           # notas de implementación MCP + skills + planning
```

---

## 1) ¿Qué es Gemini CLI?

Gemini CLI es un orquestador de IA en terminal que puede:

- Analizar y editar código local.
- Ejecutar shell commands (con controles de confirmación/seguridad).
- Conectarse a herramientas externas vía **MCP servers**.
- Aplicar reglas del proyecto usando `GEMINI.md` y skills locales.

En este repo, Gemini CLI se usa principalmente como interfaz para el MCP server `finance-tools`.

---

## 2) Instalación y Setup

### Prerrequisitos

- **Node.js 20+** (Gemini CLI)
- **Python 3.11+** (MCP server y APIs)
- Acceso a internet para market data (`yfinance`) y model providers

### Instalar Gemini CLI

```bash
npm install -g @google/gemini-cli
```

Alternativa:

```bash
npx @google/gemini-cli
```

### Instalar dependencias de Python

Desde la raíz del repositorio:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Autenticar Gemini CLI

Ejecuta:

```bash
gemini
```

Luego completa el login en navegador, o define:

```powershell
$env:GEMINI_API_KEY="YOUR_KEY"
```

---

## 3) File Management con Gemini CLI

Usa `@` para incluir código/archivos en contexto:

- `Refactor @server/tool_registry.py`
- `Review @stock_analyzer_bot/api.py for endpoint consistency`
- `Summarize strategy logic in @server/strategies/`

Patrones útiles:

```bash
gemini "Generate docs for @server/main.py" > server_docs.md
gemini "Find where analyze_trin_market_breadth is used"
```

---

## 4) Agent Skills (security-review)

Este repo incluye una plantilla lista de skill en `skills-cli/`.

### Registrar localmente

Crea:

```text
.gemini/skills/security-review/SKILL.md
.gemini/skills/security-review/scripts/download.js
```

Luego copia:

- `skills-cli/SKILL.md` → `.gemini/skills/security-review/SKILL.md`
- `skills-cli/download.js` → `.gemini/skills/security-review/scripts/download.js`

Comportamiento del skill:

- Extrae categorías OWASP Top 10 desde `https://owasp.org/Top10/`
- Audita código/endpoints seleccionados
- Genera un reporte Markdown con severity, evidence y remediation

Trigger phrases:

- `check-security`
- `review-security`
- `audit-security`

---

## 5) Memory y Context Management

Este proyecto usa `GEMINI.md` como contexto persistente de instrucciones.

Política principal en este repo:

- Usar MCP tools como execution engine para análisis financiero.
- Seguir intake dialog-first (objective, symbols/sectors, period, mode, risk profile).
- Usar reporting consciente del mode (`strategy` vs `score`) y evitar métricas inventadas.

Fuentes de contexto:

- **Project memory:** `GEMINI.md`
- **Ad-hoc context:** `@path/to/file`
- **Cross-session memory:** instrucciones explícitas de “remember ...” en Gemini CLI

---

## 6) Shell Commands

Dentro de Gemini CLI:

- Ejecuta shell commands directos con `!` (por ejemplo: `!git status`).
- Pide al asistente ejecutar tests, linters o startup commands.

Comandos locales típicos para este repo:

```bash
python server/main.py
uvicorn server.api_main:app --reload
uvicorn stock_analyzer_bot.api:app --reload --port 8001
```

---

## 7) Sessions e History

Comandos útiles de sesión:

- `gemini --resume` para continuar sesiones previas
- `/resume` para explorar/buscar sesiones pasadas
- `/rewind` para deshacer turnos recientes de conversación/código

Esto ayuda al iterar sobre strategy prompts, API schemas o migration plans.

---

## 8) Task Planning (Todos)

Para cambios complejos, usa prompts de planning-first, por ejemplo:

- “Make a plan first, then save as todo list in Markdown.”

Ejemplos en este repo:

- `OPENAPI_MIGRATION_PLAN.md`
- `todo.md`

Flujo recomendado:

1. Pedir un plan a Gemini CLI.
2. Guardarlo como markdown todo checklist.
3. Ejecutar tareas de forma incremental y validar cada fase.

---

## 9) Web Search y Fetch

Gemini CLI puede search/fetch documentación y aplicarla al código local:

- Detectar breaking changes antes de actualizar dependencias.
- Traer referencias externas para validar strategies.
- Obtener docs y adaptar ejemplos a archivos de este repo.

Example prompt:

- “Fetch latest FastAPI auth patterns and apply to `server/api_main.py`.”

---

## 10) Setup de MCP Server (`finance-tools`)

### Ejecutar el MCP server

```bash
python server/main.py
```

### Agregar server a Gemini CLI

```bash
gemini mcp add finance-tools python D:\repos\gemini-cli\server\main.py
```

### Refrescar y verificar en una sesión activa de Gemini

```text
/mcp refresh
/mcp list
```

También puedes configurar manualmente en `.gemini/settings.json`:

```json
{
  "mcpServers": {
    "finance-tools": {
      "command": "python",
      "args": ["D:\\repos\\gemini-cli\\server\\main.py"]
    }
  }
}
```

---

## 11) Automation (Headless Mode)

Gemini CLI puede correr de forma no interactiva para scripts/CI:

```bash
git diff --staged | gemini "Write a concise commit message" > commit_msg.txt
gemini "Summarize @server/tool_registry.py and output JSON" --output-format json
tail -n 100 logs.txt | gemini "Analyze failures and suggest fixes" > report.md
```

---

## Finance Capabilities en este repo

`server/tool_registry.py` registra un catálogo extendido que incluye:

- Core strategy scoring (Bollinger-Fibonacci, MACD-Donchian, Connors+ZScore, Dual MA, Bollinger Z-Score, Bollinger Z-Score RSI)
- Breadth/event/volatility/relative-value tools (TRIN, overnight gaps, earnings momentum, breakout/fade, multi-timeframe, pairs, stat-arb, VIX term structure, volatility regime)
- Performance/backtesting tools
- Unified scanner + comprehensive report tools
- Fundamental analysis + financial statement index tools

---

## API Layers

- `server/api_main.py`: interfaz REST OpenAPI-first para endpoints directos de strategy/fundamental/scanner.
- `stock_analyzer_bot/api.py`: ADK multi-agent API (orchestrator/specialist/critic/reporter) sobre MCP tools.

Esta separación permite:

- acceso determinístico directo a tools (OpenAPI), y
- análisis narrativo de mayor nivel con guardrails (ruta ADK).

---

## Resumen Quick Start

1. Instala Gemini CLI y dependencias de Python.
2. Inicia MCP server: `python server/main.py`.
3. Registra MCP server: `gemini mcp add finance-tools ...`.
4. En la sesión de Gemini: `/mcp refresh` y luego `/mcp list`.
5. Ejecuta prompts de análisis usando MCP tools.

---

## Disclaimer

Este proyecto es para workflows de investigación/educación. **No** ofrece asesoría financiera. Valida siempre supuestos, calidad de datos y restricciones de riesgo antes de tomar decisiones.
