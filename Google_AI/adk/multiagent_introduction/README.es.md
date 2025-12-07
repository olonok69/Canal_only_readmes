# Triage Automatizado de Siniestros con Google ADK

Este repositorio contiene una aplicación multi‑agent construida con Google Agent Development Kit (ADK) que transforma narrativas de First Notice of Loss (FNOL) en datos estructurados, asigna un nivel de severidad y enruta el siniestro a la cola de procesamiento adecuada.

La solución enfatiza: (1) responsabilidades claras por Agent, (2) quality gates en Tools usando Pydantic, y (3) uso determinista de function calling con modelos OpenAI vía LiteLLM.

## Tabla de Contenidos
- ¿Qué es Google ADK?
- Descripción de la Aplicación
- Arquitectura
- Instalación
- Configuración
- Cómo Ejecutar
- Procesamiento por Lotes (Batch)
- Tests
- Dependencias
- Solución de Problemas (Troubleshooting)
- Estructura del Proyecto
- Próximos Pasos

## ¿Qué es Google ADK?
Google ADK es un framework para componer agents impulsados por LLM que permite:
- Definir Agents con instrucciones, descripción y un conjunto de Tools
- Orquestar ejecuciones con un Runner y un servicio de Session
- Persistir estado entre turnos (session.state) para memoria y razonamiento encadenado

Conceptos clave usados aquí:
- Agent: trabajador respaldado por un LLM con Tools que puede invocar mediante function calling.
- Tools: funciones de Python expuestas al LLM; ADK infiere esquemas JSON para cada función.
- Sub‑agents: agents especializados a los que el agent raíz puede delegar.
- Runner: ejecuta un agent de forma asíncrona y emite eventos.
- Session: almacena estado por sesión (por ejemplo, datos extraídos) entre etapas.

## Descripción de la Aplicación
“Automated Claim Triage: From FNOL to the Right Queue”

Agents implementados:
- extract_claim_info
  - Extrae campos estructurados de la narrativa FNOL (número de póliza, nombre del reclamante, contacto, tipo/fecha/lugar del incidente, lesiones, assets, posibles indicadores de fraude)
  - Invoca la Tool set_claim_info(...)
- assess_severity
  - Asigna severidad (low | medium | high) con una justificación concisa, usando session.state.claim_info
  - Invoca la Tool set_severity(level, rationale)
- route_claim
  - Selecciona la cola adecuada (fast-track | standard | auto-physical-damage | medical | property | SIU | CAT) con justificación, usando claim_info y severity
  - Invoca la Tool set_route(queue, rationale)
- Root (coordinador)
  - Explica el pipeline y genera un resumen final
  - La orquestación se ejecuta de forma secuencial para garantizar el orden y los quality gates

Quality gates (Pydantic):
- ClaimInfo, SeverityAssessment y RouteDecision validan entradas de Tools antes de escribir en session.state.
- Las Tools aceptan parámetros planos (primitivos/arrays) para mantener esquemas de OpenAI válidos; la validación se hace dentro de la Tool con Pydantic.

Determinismo:
- Temperatura del modelo reducida (0.1) para fomentar invocaciones consistentes de Tools.
- Post‑stage guards: tras cada etapa, el orquestador verifica el estado y re‑indica (nudge) si falta información.

## Arquitectura
Flujo de alto nivel:
1) extract_claim_info_agent → set_claim_info → session.state.claim_info
2) assess_severity_agent → set_severity → session.state.severity
3) route_claim_agent → set_route → session.state.route
4) root_agent → resumen final

Diagrama textual:
```
+------------------+         +---------------------+
|  FNOL narrative  |  --->   |  extract_claim_info | -- set_claim_info --> state.claim_info
+------------------+         +---------------------+
                                          |
                                          v
                             +---------------------+
                             |   assess_severity   | -- set_severity --> state.severity
                             +---------------------+
                                          |
                                          v
                             +---------------------+
                             |     route_claim     | -- set_route ----> state.route
                             +---------------------+
                                          |
                                          v
                                  +---------------+
                                  |   root agent  |
                                  +---------------+
```

Diagrama visual:

![Arquitectura de alto nivel](docs/architecture.svg)

## Instalación
- Requisitos: Python 3.10+ recomendado
- En Windows se muestran comandos PowerShell

Crear y activar un virtual environment (opcional), e instalar dependencias:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
```

## Configuración
Variables de entorno (en archivo `.env` o en tu entorno de shell):
- OPENAI_API_KEY (requerida)
  - Tu API key de OpenAI usada por LiteLLM y el adapter de ADK (LiteLlm)
- FNOL_EXAMPLES_PATH (opcional)
  - Ruta a archivo .jsonl/.json/.csv con ejemplos de FNOL para batch triage

Ejemplo `.env`:
```
OPENAI_API_KEY=sk-...redacted...
FNOL_EXAMPLES_PATH=./data/fnol_examples_more.jsonl
```

## Cómo Ejecutar
Ejecución simple (usa un ejemplo interno):
```powershell
python .\claim_triage_adk.py
```
Deberías ver un “Session State Snapshot” con:
- claim_info (dict)
- severity (dict con level + rationale)
- route (dict con queue + rationale)

## Procesamiento por Lotes (Batch)
Fuentes soportadas:
- JSONL: una línea por ejemplo; puede ser string o object con campo `text`
- JSON: array de strings, o array de objects con `text`
- CSV: columna `text` (configurable)

Configura la ruta y ejecuta:
```powershell
$env:FNOL_EXAMPLES_PATH = ".\data\fnol_examples_more.jsonl"
python .\claim_triage_adk.py
```
El script cargará los ejemplos y ejecutará el pipeline para cada uno.

## Tests
- Tests de Tools validan entradas (Pydantic) y escrituras en session.state
- Test end‑to‑end simula el Runner para verificar la orquestación sin llamar al LLM

Ejecuta tests:
```powershell
pytest -q
```

## Dependencias
Consulta `requirements.txt` para versiones exactas. Librerías clave:
- google-adk — runtime de agents, sessions, tools
- litellm — cliente unificado para modelos (usado por LiteLlm adapter)
- pydantic — validación en Tools
- pytest — framework de testing
- neo4j — presente para lecciones previas; no requerido por el triage

## Solución de Problemas (Troubleshooting)
- Error de schema de función (OpenAI/LiteLLM)
  - Síntoma: `Invalid schema for function ...`
  - Solución: Tools con parámetros planos; validación interna con Pydantic
- Las Tools no se invocan / estado queda en None
  - Temperatura reducida (0.1)
  - Instrucciones estrictas: “CALL THE TOOL … Do not output text—just call the tool.”
  - Guard & nudge: verificación del estado y re‑prompt si falta
- Falta OPENAI_API_KEY
  - El script avisa y sale; defínela en `.env` o en el entorno

## Estructura del Proyecto
```
.
├─ claim_triage_adk.py           # Pipeline principal (agents, tools, orchestrator, loaders)
├─ requirements.txt              # Dependencias
├─ data/
│  ├─ fnol_examples_more.jsonl   # Ejemplos de muestra para batch
│  └─ fnol_examples.jsonl        # (opcional) tus ejemplos
├─ tests/
│  └─ test_claim_triage.py       # Tests de tools + orquestación
├─ .env                          # Env vars (OPENAI_API_KEY, FNOL_EXAMPLES_PATH)
└─ [notebooks de lecciones y helpers — opcional]
```

## Próximos Pasos
- Persistir sessions en un data store (en lugar de in‑memory)
- Añadir agents especializados (coverage validation, fraud screening)
- Añadir logging estructurado y métricas
- Añadir un CLI con `--input` / `--output` para guardar resultados (JSON/CSV)
