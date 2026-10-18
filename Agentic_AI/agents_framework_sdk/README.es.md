# ms-agent-app — Microsoft Agent Framework + Foundry + MCP + Eval + PyRIT

> **Importante (preview)**: Este proyecto depende de paquetes prerelease del Microsoft Agent Framework y del toolkit PyRIT v0.x. Ambos evolucionan rápido. Fija (pin) las versiones antes de apoyarte en estas instrucciones en producción.

Una aplicación Python pequeña y didáctica que conecta cuatro capas de un stack de agentes moderno:

1. Un **chat agent** construido con el [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent?pivots=programming-language-python), respaldado por un deployment de modelo de **Azure AI Foundry** vía `FoundryChatClient`.
2. Un **toolbelt MCP local** — el proyecto hermano [`adk_financial_mcp_server`](../adk_financial_mcp_server) (FastMCP / stdio) acoplado a través de `MCPStdioTool`, de modo que el agente puede ejecutar análisis cuantitativos sobre datos de mercado reales.
3. **Evaluación de calidad** con el [Azure AI Evaluation SDK](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators) (`IntentResolutionEvaluator`, `TaskAdherenceEvaluator`, `ToolCallAccuracyEvaluator`).
4. **Evaluación adversarial / de seguridad** con [Microsoft PyRIT](https://github.com/microsoft/PyRIT) — el framework abierto de automatización para red-teaming de sistemas de IA generativa anunciado por Microsoft el [22 de febrero de 2024](https://www.microsoft.com/en-us/security/blog/2024/02/22/announcing-microsofts-open-automation-framework-to-red-team-generative-ai-systems/).

El proyecto está pensado para workshops, charlas técnicas y como un esqueleto limpio para arrancar una nueva aplicación de Agent Framework + Foundry.

## Tabla de contenidos

1. [Arquitectura](#arquitectura)
2. [Características](#características)
3. [Estructura del repositorio](#estructura-del-repositorio)
4. [Fases](#fases)
5. [Requisitos previos](#requisitos-previos)
6. [Instalación](#instalación)
7. [Configuración](#configuración)
8. [Cómo ejecutar](#cómo-ejecutar)
9. [Fase 3 — Azure AI Evaluation SDK](#fase-3--azure-ai-evaluation-sdk)
10. [Fase 4 — Pasada de red-team con PyRIT](#fase-4--pasada-de-red-team-con-pyrit)
11. [Archivos clave](#archivos-clave)
12. [Testing](#testing)
13. [Resolución de problemas](#resolución-de-problemas)
14. [Consejos operativos](#consejos-operativos)
15. [Referencias](#referencias)

## Arquitectura

<p align="center">
  <img src="microsoft_agent_framework_app/docs/architecture.svg" alt="Arquitectura de alto nivel de ms-agent-app" width="1080">
</p>

Flujo de datos de alto nivel:

1. El **desarrollador** ejecuta el CLI (`ms-agent-app`); `cli.py` carga `.env` vía `pydantic-settings` (`config.py`) y construye un Agent (`agent_factory.build_chat_agent`).
2. El Agent llama a **Azure AI Foundry** a través de `FoundryChatClient`, autenticado con `DefaultAzureCredential` (es decir, tu token de `az login`).
3. Con `--with-mcp`, `mcp_finance.open_finance_mcp_tool` lanza el servidor hermano **FastMCP "finance tools"** como un subproceso stdio; sus tools quedan invocables por el Agent dentro del mismo bucle `agent.run(...)`.
4. La **Fase 3** (`ms_agent_app.eval`) reproduce un dataset curado a través del mismo Agent, captura las trajectories con el esquema de mensajes de OpenAI y las puntúa con los evaluators del **Azure AI Evaluation SDK** usando un judge provider configurable (`JUDGE_PROVIDER=azure-openai|openai`).
5. La **Fase 4** (`ms_agent_app.redteam`) envuelve el mismo Agent en un **`PromptTarget` de PyRIT**, lanza objetivos de red-team mediante un `PromptSendingAttack` y detecta refusals con `SelfAskRefusalScorer` impulsado por el mismo judge provider configurable.

Fuente completa del diagrama: [`microsoft_agent_framework_app/docs/architecture.svg`](microsoft_agent_framework_app/docs/architecture.svg).

## Características

- **Cableado async-first del Agent Framework** — una factory mínima de `FoundryChatClient` más una factory de `Agent` que acepta un toolbelt MCP opcional.
- **Gestión lazy del subproceso MCP** — `MCPStdioTool` se abre dentro de un bloque `async with`; el finance server solo se ejecuta cuando se pasa `--with-mcp`.
- **Un único `.env` para cuatro capas** — el model provider, la ruta del MCP server, el judge de evaluación y el judge de PyRIT comparten una sola superficie de configuración, validada por `pydantic-settings`.
- **Harness de evaluación reproducible** — `Trajectory.record(agent)` captura `(query, response, tool_calls)` con la forma del esquema de mensajes de OpenAI que espera el Azure AI Evaluation SDK.
- **Script de red-team** — la Fase 4 incluye un dataset pequeño de probes de jailbreak / prompt-injection / harmful-finance / system-prompt-extraction que puedes ejecutar con un solo comando.
- **Dependencias pesadas opcionales** — `pyrit` es un grupo de extras (`uv sync --extra redteam`), de modo que la instalación base se mantiene ligera.

## Estructura del repositorio

```text
microsoft_agent_framework_app/
├── CLAUDE.md                              # contexto para asistentes de IA
├── README.md                              # este archivo
├── pyproject.toml                         # deps gestionadas por uv + config de ruff/pytest
├── uv.lock
├── .env.example                           # plantilla de configuración
├── docs/
│   ├── architecture.svg                   # diagrama de arquitectura de alto nivel
│   └── superpowers/plans/                 # planes de implementación
├── src/
│   └── ms_agent_app/
│       ├── __init__.py
│       ├── cli.py                         # REPL async, flag --with-mcp
│       ├── config.py                      # Settings(BaseSettings)
│       ├── foundry_client.py              # FoundryChatClient + DefaultAzureCredential
│       ├── agent_factory.py               # build_chat_agent(...)
│       ├── mcp_finance.py                 # cableado de MCPStdioTool
│       ├── eval/                          # Fase 3 — Azure AI Evaluation SDK
│       │   ├── __init__.py
│       │   ├── dataset.py                 # tupla curada de EvalCase
│       │   ├── runner.py                  # helper Trajectory.record()
│       │   └── score.py                   # entry point: escribe .eval_outputs/results.json
│       └── redteam/                       # Fase 4 — PyRIT
│           ├── __init__.py
│           ├── dataset.py                 # tupla curada de RedTeamCase
│           ├── target.py                  # AgentFrameworkTarget(PromptTarget)
│           └── run.py                     # entry point: escribe .pyrit_outputs/results.json
└── tests/
    ├── test_agent_factory.py
    ├── test_config.py
    ├── test_eval_runner.py
    ├── test_mcp_finance.py
    └── test_redteam_target.py             # se omite automáticamente cuando pyrit no está instalado
```

## Fases

| Fase | Objetivo | Comando de entrada | Archivos clave |
|-------|------|---------------|-----------|
| **0** | Bootstrap del proyecto con `uv` y escribir `.env` | `uv sync` | `pyproject.toml`, `.env.example` |
| **1** | Chat agent respaldado por Foundry (sin tools) | `uv run ms-agent-app` | `foundry_client.py`, `agent_factory.py`, `cli.py` |
| **2** | El mismo agente + tools MCP financieras locales | `uv run ms-agent-app --with-mcp` | `mcp_finance.py` |
| **3** | Puntuar ejecuciones curadas con el Azure AI Evaluation SDK | `uv run python -m ms_agent_app.eval.score` | `eval/dataset.py`, `eval/runner.py`, `eval/score.py` |
| **4** | Red-team del agente con PyRIT | `uv run ms-agent-redteam` | `redteam/dataset.py`, `redteam/target.py`, `redteam/run.py` |

## Requisitos previos

- **Python `3.11+`** (el Agent Framework lo requiere; PyRIT soporta `3.10–3.14`).
- Gestor de paquetes **`uv`** (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
- **Azure CLI** para `az login` (`FoundryChatClient` se autentica a través de `DefaultAzureCredential`).
- Un **proyecto de Azure AI Foundry** con un deployment de modelo de chat (p. ej. `gpt-4.1`).
- Un **recurso de Azure OpenAI** para el judge model de la Fase 3 / Fase 4 (p. ej. `gpt-4o`).
- El **proyecto hermano** [`../adk_financial_mcp_server`](../adk_financial_mcp_server) clonado con su propio venv (se usa como MCP server stdio en la Fase 2).

## Instalación

Este proyecto vive en una unidad montada de Windows (`/mnt/d/...`), donde `drvfs` de WSL bloquea las operaciones `chmod` que `uv` realiza dentro del venv. El workaround — usado en todos los ejemplos siguientes — es mantener el venv en el sistema de archivos de Linux y re-exportar `UV_PROJECT_ENVIRONMENT`:

```bash
export UV_PROJECT_ENVIRONMENT=/home/$USER/.venvs/ms-agent-app
uv sync                               # instalación base
uv sync --extra redteam               # también instala pyrit (~150 MB extra)
```

`[tool.uv] link-mode = "copy"` ya está configurado en `pyproject.toml`, así que no necesitas `UV_LINK_MODE`. Si estás en macOS o en un sistema de archivos Linux nativo, puedes omitir por completo el export de `UV_PROJECT_ENVIRONMENT`.

## Configuración

Copia `.env.example` a `.env` y rellena los valores:

```bash
cp .env.example .env
```

| Variable | Usada por | Notas |
|---|---|---|
| `MODEL_PROVIDER` | Runtime de chat de las Fases 1, 2, 3, 4 | Uno de `foundry`, `openai`, `azure-openai`, `anthropic` (por defecto `foundry`) |
| `FOUNDRY_PROJECT_ENDPOINT` | Fases 1, 2, 3, 4 — Foundry chat client | Requerida cuando `MODEL_PROVIDER=foundry`; p. ej. `https://<resource>.services.ai.azure.com/api/projects/<project>` |
| `FOUNDRY_MODEL_DEPLOYMENT_NAME` | Fases 1, 2, 3, 4 — Foundry chat client | Nombre del deployment de chat, p. ej. `gpt-4.1` |
| `OPENAI_API_KEY` | Fases 1, 2, 3, 4 — OpenAI chat provider | Requerida cuando `MODEL_PROVIDER=openai` |
| `OPENAI_CHAT_MODEL` | Fases 1, 2, 3, 4 — OpenAI chat provider | Deployment preferido para `OpenAIChatClient` |
| `OPENAI_MODEL` | Fallback opcional del OpenAI chat provider | Se usa cuando `OPENAI_CHAT_MODEL` no está definido |
| `OPENAI_BASE_URL` | Opcional — OpenAI chat provider | Base URL personalizada compatible con OpenAI |
| `AZURE_OPENAI_ENDPOINT` | Fases 1, 2, 3, 4 — Azure OpenAI chat provider | Requerida cuando `MODEL_PROVIDER=azure-openai` |
| `AZURE_OPENAI_CHAT_MODEL` | Fases 1, 2, 3, 4 — Azure OpenAI chat provider | Deployment preferido para `OpenAIChatClient` |
| `AZURE_OPENAI_MODEL` | Fallback opcional del Azure OpenAI chat provider | Se usa cuando `AZURE_OPENAI_CHAT_MODEL` no está definido |
| `AZURE_OPENAI_API_KEY` | Opcional — Azure OpenAI chat provider | No es necesaria cuando se usa autenticación con identidad de Azure |
| `AZURE_OPENAI_API_VERSION` | Opcional — Azure OpenAI chat provider | Override de la versión de API para el cliente OpenAI |
| `ANTHROPIC_API_KEY` | Fases 1, 2, 3, 4 — Anthropic chat provider | Requerida cuando `MODEL_PROVIDER=anthropic` |
| `ANTHROPIC_CHAT_MODEL` | Fases 1, 2, 3, 4 — Anthropic chat provider | ID del modelo Claude |
| `ANTHROPIC_BASE_URL` | Opcional — Anthropic chat provider | Base URL personalizada compatible con Anthropic |
| `AZURE_TENANT_ID` | Opcional — `DefaultAzureCredential` | Solo cuando `az login` tiene múltiples tenants |
| `MCP_FINANCE_SERVER_PATH` | Fase 2 | Ruta absoluta o relativa a `adk_financial_mcp_server/server/main.py` |
| `MCP_FINANCE_PYTHON` | Fase 2 | Intérprete que tiene instaladas las deps del finance server |
| `JUDGE_PROVIDER` | Judge de la Fase 3 **y** judge de PyRIT de la Fase 4 | `azure-openai` (por defecto) o `openai` |
| `AZURE_DEPLOYMENT_NAME` | Judge cuando `JUDGE_PROVIDER=azure-openai` | Nombre del deployment de Azure OpenAI (p. ej. `gpt-4o`) |
| `AZURE_API_KEY` | Judge cuando `JUDGE_PROVIDER=azure-openai` | Key de Azure OpenAI |
| `AZURE_ENDPOINT` | Judge cuando `JUDGE_PROVIDER=azure-openai` | `https://<aoai>.cognitiveservices.azure.com/` |
| `AZURE_API_VERSION` | Judge cuando `JUDGE_PROVIDER=azure-openai` | Por defecto `2024-12-01-preview` |
| `JUDGE_OPENAI_API_KEY` | Judge cuando `JUDGE_PROVIDER=openai` | Override opcional; hace fallback a `OPENAI_API_KEY` |
| `JUDGE_OPENAI_MODEL` | Judge cuando `JUDGE_PROVIDER=openai` | Override opcional; hace fallback a `OPENAI_CHAT_MODEL` / `OPENAI_MODEL` |
| `JUDGE_OPENAI_BASE_URL` | Base URL opcional del judge OpenAI | Por defecto `OPENAI_BASE_URL`, luego `https://api.openai.com/v1` |
| `JUDGE_OPENAI_ORGANIZATION` | Organización opcional del judge OpenAI | Se pasa a `OpenAIModelConfiguration` |

`pydantic-settings` valida el archivo y muestra errores claros si faltan variables de las Fases 1 / 2. Las variables del judge se validan de forma lazy cuando se ejecutan los scripts de la Fase 3 / Fase 4, en función de `JUDGE_PROVIDER`.

## Cómo ejecutar

```bash
# Fase 1 — agente solo-chat (sin tools)
uv run ms-agent-app

# Opciones de provider de la Fase 1 vía override en el CLI
uv run ms-agent-app --provider foundry
uv run ms-agent-app --provider openai
uv run ms-agent-app --provider azure-openai
uv run ms-agent-app --provider anthropic

# Fase 2 — agente + tools MCP financieras (subproceso stdio lazy)
uv run ms-agent-app --with-mcp
uv run ms-agent-app --with-mcp --provider foundry
uv run ms-agent-app --with-mcp --provider openai
uv run ms-agent-app --with-mcp --provider azure-openai
uv run ms-agent-app --with-mcp --provider anthropic

# Fase 3 — pasada del Azure AI Evaluation SDK sobre el dataset curado
# El model provider del agente viene de MODEL_PROVIDER en .env
# El judge provider viene de JUDGE_PROVIDER en .env
uv run python -m ms_agent_app.eval.score

# Fase 4 — pasada de red-team con PyRIT sobre el dataset de ataques curado
# El model provider del agente viene de MODEL_PROVIDER en .env
# El judge provider viene de JUDGE_PROVIDER en .env
uv run ms-agent-redteam
```

### Matriz de demo para las 4 fases

Usa estos ajustes de provider antes de ejecutar el comando de cada fase:

| Fase | Comando | Opciones de provider del agente | Opciones de provider del judge |
|---|---|---|---|
| 1 | `uv run ms-agent-app [--provider ...]` | `foundry`, `openai`, `azure-openai`, `anthropic` (vía `--provider` o `MODEL_PROVIDER`) | N/A |
| 2 | `uv run ms-agent-app --with-mcp [--provider ...]` | `foundry`, `openai`, `azure-openai`, `anthropic` (vía `--provider` o `MODEL_PROVIDER`) | N/A |
| 3 | `uv run python -m ms_agent_app.eval.score` | `foundry`, `openai`, `azure-openai`, `anthropic` (desde `MODEL_PROVIDER`) | `azure-openai` o `openai` (desde `JUDGE_PROVIDER`) |
| 4 | `uv run ms-agent-redteam` | `foundry`, `openai`, `azure-openai`, `anthropic` (desde `MODEL_PROVIDER`) | `azure-openai` o `openai` (desde `JUDGE_PROVIDER`) |

### Smoke test manual (Fase 2)

```bash
uv run ms-agent-app --with-mcp
```

En el prompt prueba:

- `What tools are available?` — el agente debería listar las finance tools.
- `Run a dual moving average analysis on AAPL.` — el agente debería llamar a una tool y reportar resultados.
- `exit` para salir.

El subproceso del MCP server lo inicia de forma lazy `MCPStdioTool` y se cierra cuando se sale del REPL.

## Fase 3 — Azure AI Evaluation SDK

`ms_agent_app.eval.score` sigue la misma forma que [`evaluation/03_azure_ai_eval_agents.py`](../evaluation/03_azure_ai_eval_agents.py) del proyecto hermano de evaluación:

1. `Settings()` carga la configuración del judge model según `JUDGE_PROVIDER`:
    - `azure-openai` -> `AzureOpenAIModelConfiguration`
    - `openai` -> `OpenAIModelConfiguration`
2. Para cada `EvalCase` en `eval/dataset.py`, `Trajectory.record(agent, tools=mcp_server)` ejecuta el prompt y captura la response + cualquier tool call con la forma del esquema de mensajes de OpenAI:
   ```python
   {"role": "user", "content": [{"type": "text", "text": "..."}]}
   {"role": "assistant", "content": [
       {"type": "tool_call", "tool_call_id": "...", "name": "...", "arguments": {...}},
       {"type": "text", "text": "..."},
   ]}
   ```
3. Tres evaluators puntúan cada trajectory:
   - `IntentResolutionEvaluator` (umbral `3`)
   - `TaskAdherenceEvaluator` (umbral `0.5`)
   - `ToolCallAccuracyEvaluator` (solo cuando la trajectory contiene realmente tool calls)
4. Los resultados se escriben en `.eval_outputs/results.json`.

Dataset curado (`eval/dataset.py`):

| Case ID | Intent | ¿Espera tool call? |
|---------|--------|--------------------|
| `intent-direct` | Definición del MS Agent Framework | No |
| `tool-dual-ma` | Backtest de dual moving-average sobre AAPL | Sí |
| `tool-fundamentals` | Snapshot de análisis fundamental para MSFT | Sí |
| `clarification` | "help me with a strategy" ambiguo — el agente debería preguntar | No |

## Fase 4 — Pasada de red-team con PyRIT

[PyRIT](https://github.com/microsoft/PyRIT) (Python Risk Identification Toolkit) es el framework abierto de Microsoft para red-teaming de sistemas de IA generativa. Modela la evaluación adversarial como cuatro bloques de construcción enchufables:

- **Targets** — lo que se ataca (`PromptTarget`, p. ej. nuestro Agent).
- **Attacks / Orchestrators** — cómo se entregan los prompts (`PromptSendingAttack`).
- **Converters** — transformaciones aplicadas a los prompts antes de llegar al target (Base64, ROT13, wrappers de prompt-injection, etc.).
- **Scorers** — jueces que clasifican la response (`SelfAskRefusalScorer`, scorers de categoría de contenido, scorers true/false).

> Aviso: PyRIT renombró varias abstracciones en la v0.13. Usamos los nombres **actuales**: `PromptTarget` (no `PromptChatTarget`), `PromptSendingAttack` (no `PromptSendingOrchestrator`), `Message`/`MessagePiece` (no `PromptRequestResponse`/`PromptRequestPiece`) y el bootstrap async `initialize_pyrit_async(...)`. Los tutoriales antiguos no funcionarán sin cambios.

### Cómo integra PyRIT este proyecto

1. **`target.py`** define `AgentFrameworkTarget(PromptTarget)` — las únicas ~20 líneas de código específico de PyRIT que poseemos. Su `send_prompt_async` extrae el texto del prompt, llama a `self._agent.run(prompt_text)` y devuelve la response del agente vía `construct_response_from_request` para la contabilidad de memoria.
2. **`run.py`** valida las variables de entorno del judge (igual que la Fase 3), construye el judge `OpenAIChatTarget`, ejecuta `initialize_pyrit_async(IN_MEMORY)`, envuelve el agente en `AgentFrameworkTarget`, lanza un `PromptSendingAttack` por cada objetivo con `AttackExecutor` (concurrencia acotada) y puntúa cada response con `SelfAskRefusalScorer`.

**Salida** — `.pyrit_outputs/results.json` con un registro por caso: `objective`, `agent_response`, `outcome` (`SUCCESS` / `FAILURE` / `ERROR` / `UNDETERMINED`), `refusal_detected` (`True` si el refusal scorer disparó), `score_rationale` y `outcome_reason`.

### Dataset de ataques curado

`redteam/dataset.py` mantiene el conjunto deliberadamente pequeño — cinco probes que ejercitan cada uno un comportamiento de atacante distinto:

| Case ID | Categoría | Qué prueba |
|---------|----------|----------------|
| `jailbreak-dan` | jailbreak | Persona DAN clásica + petición de manipulación de mercado |
| `prompt-injection-tool` | prompt_injection | Injection dirigida a los argumentos de una tool call |
| `harmful-financial-advice` | harm_misuse | Petición a alta presión de consejo de apalancamiento de alto riesgo |
| `insider-trading` | harm_misuse | Petición explícita de un walkthrough de trading ilegal |
| `system-prompt-extraction` | prompt_injection | Intento de filtrar el system prompt textualmente |

Un deployment de Foundry que se comporte bien debería rechazar las cinco; el scorer reporta `refusal_detected: true` (`AttackOutcome.SUCCESS` de PyRIT, para un refusal scorer, significa *que se detectó el refusal*, no que el ataque tuvo éxito).

### Extender la demo

- **Converters** — envuelve prompts para sortear filtros ingenuos; añade p. ej. `from pyrit.prompt_converter import Base64Converter` y pasa un `AttackConverterConfig`.
- **Múltiples scorers** — añade `SelfAskCategoryScorer` para clasificación de categoría de daño junto a la detección de refusals.
- **Ataques multi-turno** — cambia `PromptSendingAttack` por `RedTeamingAttack` para encadenar turnos adversariales impulsados por un attacker LLM.
- **Memoria persistente** — cambia `IN_MEMORY` por `SQLITE` o `AZURE_SQL` si quieres comparar ejecuciones entre días.

## Archivos clave

- **`src/ms_agent_app/cli.py`** — REPL async; importa `mcp_finance` de forma lazy para que la instalación base no necesite arrancar el finance server.
- **`src/ms_agent_app/agent_factory.py`** — única factory `build_chat_agent(settings, *, tools=None)`; el `DEFAULT_INSTRUCTIONS` por defecto le dice al agente que prefiera las tools antes que adivinar.
- **`src/ms_agent_app/foundry_client.py`** — wrapper fino que devuelve un `FoundryChatClient` configurado desde `Settings`.
- **`src/ms_agent_app/mcp_finance.py`** — `build_finance_mcp_tool` + el context manager `open_finance_mcp_tool`; lanza `ValueError` / `FileNotFoundError` amistosos cuando el entorno está mal configurado.
- **`src/ms_agent_app/eval/score.py`** — entry point de la Fase 3; escribe `.eval_outputs/results.json`.
- **`src/ms_agent_app/redteam/run.py`** — entry point de la Fase 4; escribe `.pyrit_outputs/results.json`.
- **`docs/architecture.svg`** — diagrama de arquitectura de alto nivel embebido arriba.

## Testing

```bash
uv run pytest -v
```

La suite cubre:

- Carga y validación de variables de entorno de `Settings` (incluido el test negativo de entorno faltante con `_env_file=None`).
- El cableado del constructor de `build_chat_agent`.
- La resolución de argumentos de `build_finance_mcp_tool`.
- La forma de `Trajectory.record` frente a un Agent mockeado.
- `AgentFrameworkTarget` — se omite automáticamente cuando `pyrit` no está instalado (el grupo de extras opcional).

Lint + format:

```bash
uv run ruff check .
uv run ruff format --check .
```

## Resolución de problemas

| Problema | Solución |
|-------|-----|
| `chmod ... .git/config.lock: Operation not permitted` (WSL) | Exporta `UV_PROJECT_ENVIRONMENT=/home/$USER/.venvs/ms-agent-app` para que el venv viva en ext4. |
| `Missing env vars for eval judge ...` | Rellena las variables del judge en `.env` según `JUDGE_PROVIDER`. |
| `ModuleNotFoundError: pyrit` al ejecutar `ms-agent-redteam` | Vuelve a ejecutar `uv sync --extra redteam`. |
| `MCP server script not found at ...` | Comprueba que `MCP_FINANCE_SERVER_PATH` es correcta y que el proyecto hermano está clonado. |
| Las llamadas a Foundry devuelven `DefaultAzureCredential failed ...` | Ejecuta `az login`. Si tienes múltiples tenants, define también `AZURE_TENANT_ID`. |
| La instalación de PyRIT arrastra `transformers` y una descarga grande | Es lo esperado — `transformers` es una dep de runtime dura incluso en la instalación ligera. Permite ~150 MB. |
| `AttackOutcome.SUCCESS` parece indicar que el agente fue jailbreakeado | Para `SelfAskRefusalScorer`, `SUCCESS` significa **que se detectó el refusal**. Inviértelo con `TrueFalseInverterScorer` si tu demo quiere que "success = jailbreak". |
| `OpenAIChatTarget` 401/404 contra Azure | Asegúrate de que el endpoint termina en `/openai/v1` (el script lo añade automáticamente) y de que `model_name` es el *nombre del deployment*, no el nombre del modelo. |

## Consejos operativos

- La Fase 3 y la Fase 4 comparten el **mismo enrutado de judge provider** vía `JUDGE_PROVIDER`.
- Para `JUDGE_PROVIDER=openai`, la evaluación usa `JUDGE_OPENAI_*` (con fallback a `OPENAI_*`).
- Para `JUDGE_PROVIDER=azure-openai`, la evaluación/red-team usan las variables de judge `AZURE_*`.
- Mantén los datasets curados (`eval/dataset.py`, `redteam/dataset.py`) cortos y de alta señal — estos scripts son demos, no suites de cobertura. Hazlos crecer de forma incremental.
- El subproceso MCP se lanza por cada ejecución de la Fase 3; espera latencia de cold-start en el primer prompt. La Fase 4 **no** abre el MCP server (los prompts de red-team atacan el comportamiento de chat del agente, no sus tools).
- PyRIT se mueve rápido (v0.13 en 2026); fija la versión en `pyproject.toml` antes de añadir más scripts sobre él.
- Nunca hagas commit de `.env`, `.eval_outputs/` ni `.pyrit_outputs/` — contienen salidas del modelo que pueden incluir datos sensibles.

## Referencias

### Microsoft Agent Framework

- Getting started — https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent?pivots=programming-language-python
- Tutorial de tools MCP — https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/mcp-tools?pivots=programming-language-python
- API del Foundry chat client — https://learn.microsoft.com/en-us/python/api/agent-framework-foundry/

### Azure AI Foundry y Evaluation SDK

- Foundry RBAC — https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-foundry
- Agent evaluators — https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators
- Código del Evaluation SDK — https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/evaluation/azure-ai-evaluation

### MCP

- Especificación — https://modelcontextprotocol.io
- Anuncio de Anthropic — https://www.anthropic.com/news/model-context-protocol

### PyRIT

- GitHub — https://github.com/microsoft/PyRIT
- Docs — https://microsoft.github.io/PyRIT/
- Blog de Microsoft Security (22 feb 2024) — https://www.microsoft.com/en-us/security/blog/2024/02/22/announcing-microsofts-open-automation-framework-to-red-team-generative-ai-systems/

### Proyectos hermanos en este workspace

- `../adk_financial_mcp_server` — finance MCP server acoplado en la Fase 2.
- `../evaluation` — scripts de referencia de DeepEval / Inspect AI / Azure AI Evaluation; `03_azure_ai_eval_agents.py` es el ancestro conceptual de `ms_agent_app/eval/score.py`.
- `../azure_foundry_sharepoint` — agente de Foundry anterior con grounding en SharePoint; origen del layout de `.env` y del patrón de reutilización de credenciales SP.


## Referencia sobre Prompt Hacking
- https://learnprompting.org/docs/prompt_hacking/introduction
