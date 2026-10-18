# Workflow reporting basado en Graficos de Conocimiento con Deep Agents LangChain
Una capa de automatización que prepara y ejecuta el reporte analítico  de  tareas usando [DeepAgents](https://github.com/deepagents/deepagents), Neo4j y LLMs compatibles con LangChain. El flujo compila un plan TODO determinista, prepara al agente con contexto de esquema/configuración y dirige el ciclo completo de generación de reportes para cualquier configuración de evento soportada.

## ¿Qué es DeepAgents?
[DeepAgents](https://docs.langchain.com/oss/python/deepagents/overview) es el runtime multiagente, guiado por tareas, de LangChain. Empareja manifiestos TODO deterministas con subagentes que conocen sus herramientas. Cada agente monta su propio set de herramientas (filesystem, Neo4j, evaluadores) mientras el coordinador hace cumplir la ejecución ordenada, los reintentos y los pasos de recuperación. En este proyecto usamos DeepAgents para: (1) ingerir un plan TODO canónico, (2) delegar trabajo pesado en Cypher a un especialista en Neo4j, (3) enviar borradores a un subagente de crítica y (4) preservar cada artefacto intermedio para auditoría.


## Capacidades Clave
- **Orquestación determinista** – construye el manifiesto de tareas, el plan TODO, el snapshot de esquema y el inventario de recuperación antes de contactar al LLM (`arc/pre_show/manifest.py`).
- **Acceso al filesystem con enfoque en seguridad** – enruta la escritura/lectura del agente mediante un backend aislado que refleja artefactos en `/memories/<event><year>/pre_show` para recuperación ante desastres (`arc/pre_show/backends.py`).
- **Herramientas Neo4j directas** – expone `get_neo4j_schema`, `read_neo4j_cypher` y `write_neo4j_cypher` con normalización de identificadores y reescritura de queries (`arc/pre_show/generator.py`).
- **Flexibilidad de proveedores LLM** – soporta Azure OpenAI, OpenAI y Anthropic (Claude 4.5) mediante la abstracción unificada `ModelSettings` (`deep_agents_reports/src/models.py`).
- **Persistencia de artefactos** – archiva estados TODO, respuestas del agente, archivos de resultados y snapshots de esquema en `deep_agents_reports/reports/artifacts/` y `deep_agents_reports/outputs/<event><year>/pre_show/`.

## Arquitectura de Alto Nivel
```
CLI (deep_agents_workflow.py)
    │
    └── ShowReportGenerator (arc/pre_show/generator.py)
          ├─ load_event_config / prompt template resolution
          ├─ manifest + TODO builders (arc/pre_show/manifest.py)
          ├─ prompt/context assembly (arc/pre_show/prompts.py)
          ├─ DeepAgents + SubAgents + Neo4j tools
          ├─ TODO reconciliation + execution loop
          └─ artifact/memory persistence
```
- **CLI** – `deep_agents_workflow.py` analiza los argumentos y crea `ShowReportGenerator`.
- **Generator** – encapsula inicialización (config, prompt, Neo4j, modelo), producción de manifiesto, creación del DeepAgent, ejecución y manejo de errores.
- **Backends** – `SafeFilesystemBackend` impone IO relativo al repositorio y enruta `/memories/` para almacenamiento de largo plazo.
- **Prompts** – `arc/pre_show/prompts.py` crea la instrucción principal y los prompts de los subagentes (análisis Neo4j + crítica QA).

## Stack Tecnológico
- **Runtime** – Python 3.11 (ver `.python-version`).
- **Orquestación** – DeepAgents 0.2.x (tooling de tareas, middleware TODO, delegación de subagentes).
- **Acceso LLM** – LangChain, `langchain-openai`, `langchain-anthropic`, `langchain-mcp-adapters`.
- **Capa de grafo** – Neo4j 5.x con el driver oficial de Python.
- **Configuración** – Configs YAML en `deep_agents_reports/config` y templates Markdown en `deep_agents_reports/reports/prompts`.
- **Dependencias** – `requirements.txt` (pip / uv) + `pyproject.toml` para installs editables.

## Estructura del Repositorio
| Ruta | Descripción |
| --- | --- |
| `deep_agents_workflow.py` | Entrada CLI que conecta argumentos con el generador y muestra resúmenes. |
| `arc/pre_show/` | Componentes modulares del flujo (generator, helpers de manifiesto, prompts, filesystem backends). |
| `config/` | Configs YAML por evento usadas por el pipeline de datos y este flujo. |
| `docs/` | Material de referencia (prompts, protocolos, guía de configuración). |
| `reports/prompts/` | Templates genéricos y específicos por evento. |
| `reports/artifacts/` | Snapshots automáticos de manifiestos/TODOs/respuestas por corrida. |
| `outputs/<event><year>/pre_show/` | Dumps de esquema Neo4j, exports JSON y archivos reflejados del agente. |
| `memory/` | Sandbox de largo plazo utilizado por el filesystem backend. |

## Prerrequisitos
1. **Python** – 3.11.x.
2. **Neo4j** – Instancia 4.4+ (ideal 5.x) con APOC para descubrimiento de esquema.
3. **Variables de entorno** – Guardadas en `keys/.env` o exportadas:
   - `NEO4J_URI_<PROFILE>` (ej. `NEO4J_URI_TEST=bolt://...`).
   - `NEO4J_PASSWORD_<PROFILE>` y `NEO4J_USERNAME` (por defecto `neo4j`).
   - `OPENAI_API_KEY`, `AZURE_OPENAI_API_KEY`/`AZURE_OPENAI_ENDPOINT`/`AZURE_OPENAI_DEPLOYMENT` o `ANTHROPIC_API_KEY` según proveedor.
4. **Configuración del evento** – Copia o ajusta un YAML en `deep_agents_reports/config`. Consulta `docs/readme_config.md` para detalles.
5. **Prompt template** – Normalmente `deep_agents_reports/reports/prompts/prompt_initial_run_generic_short.md` o una variante por evento.

## Instalación
```bash
cd deep_agents_reports
python -m venv .venv
. .venv/Scripts/activate            # PowerShell: ./.venv/Scripts/Activate.ps1
pip install -U pip
pip install -r requirements.txt
# install editable opcional para libs compartidas
pip install -e .
```
> Usa `uv pip sync requirements.txt` si tienes el CLI `uv`; mantiene el lockfile sincronizado.

## Configuración
### Variables de Entorno
Crea `keys/.env` (o expórtalas):
```env
# perfiles Neo4j usados por --neo4j-profile
NEO4J_URI_DEV=bolt://localhost:7687
NEO4J_URI_TEST=neo4j+s://test.db.neo4j.io
NEO4J_URI_PROD=neo4j+s://prod.db.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD_DEV=dev-password
NEO4J_PASSWORD_TEST=test-password
NEO4J_PASSWORD_PROD=prod-password

# proveedores LLM
OPENAI_API_KEY=sk-...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
ANTHROPIC_API_KEY=...
```
`ShowReportGenerator` selecciona el par URI/password correcto según `--neo4j-profile` y usa `NEO4J_USERNAME` si no hay usuario específico.

### YAML del Evento
Cada config en `deep_agents_reports/config` refleja las opciones del pipeline PA (registration/scans/sessions/recommendations). Este flujo consume principalmente:
- `mode`, `event.*` y `neo4j.*` para formatear prompts y normalizar identificadores Cypher.
- `recommendation.similarity_attributes` para expandir queries placeholder en el manifiesto.
- Rutas para reflejar outputs.
Consulta `docs/readme_config.md` para la explicación completa.

### Prompt Templates
Los prompts viven en `deep_agents_reports/reports/prompts`. El flujo lee el template, reemplaza `[PLACEHOLDER]` con valores de config y guarda la versión resuelta en `reports/artifacts/processed_prompt_<event><year>.md`. Mantén sincronizados los templates con las expectativas del manifiesto TODO (secciones `### TASK n`).

## Ejecución del Flujo
```powershell
python deep_agents_workflow.py `
  --event CPCN `
  --year 2025 `
  --config deep_agents_reports\config\config_cpcn.yaml `
  --prompt-template deep_agents_reports\reports\prompts\prompt_initial_run_generic_short.md `
  --neo4j-profile test `
  --neo4j-database neo4j `
  --provider anthropic `
  --model claude-haiku-4-5 `
  --temperature 0.1 `
  --example-report deep_agents_reports\reports\report_cpcn_13112025_short.md `
  --verbose
```
**Flags clave**
- `--provider` / `--model` – Selecciona Azure/OpenAI/Anthropic.
- `--example-report` – Referencia opcional de tono/estilo.
- `--neo4j-profile` – Usa las credenciales definidas.
- `--verbose` – Aumenta el nivel de logging.

## Pipeline de Reportes en Dos Fases
- `reporting_pipeline.py` orquesta corridas end-to-end a partir de perfiles YAML (ver `config/reporting_pipeline.yaml`). Cada perfil describe metadatos del evento, paths de config/prompt, overrides de provider/model para ambas fases, flags de enriquecimiento y referencias opcionales a `pre_show_report` cuando se generan reportes post-show.
- **Fase 1** (`run_phase_one`) invoca `ShowReportGenerator` con el template y config del perfil. Detecta automáticamente `report_type` (`pre_show` vs `post_show`) mediante `determine_report_type()` para escribir en la subcarpeta correcta (`pre_show/` o `post_show/`).
- **Fase 2** (`run_phase_two`) ejecuta la pasada de enriquecimiento para pulir el Markdown base. Se controla vía `enable_enrichment` en el perfil o con `--skip-enrichment` desde la CLI.
- Ejemplo de ejecución:
  ```powershell
  python -m deep_agents_reports.reporting_pipeline --profile lva2025 --config-file deep_agents_reports/config/reporting_pipeline.yaml
  python -m deep_agents_reports.reporting_pipeline --profile lva2025_post --skip-enrichment
  ```
  El runner imprime las rutas del reporte base y del enriquecido bajo `outputs/<event><year>/<pre|post>_show/`.

## Pasada de Enriquecimiento LLM
`enrich_report.py` reescribe el Markdown de la Fase 1 con un prompt restringido que preserva todos los números/tablas y mejora el tono ejecutivo. Acepta cualquier provider soportado por `ModelSettings` y usa Anthropic por defecto.

```powershell
python -m deep_agents_reports.enrich_report \
  --input outputs/cpcn2025/pre_show/final_report_cpcn2025.md \
  --output outputs/cpcn2025/pre_show/final_report_cpcn2025_enriched.md \
  --provider anthropic --model claude-opus-3 --temperature 0.1 --max-tokens 8000
```
`reporting_pipeline` llama a este helper automáticamente durante la Fase 2, pero el CLI standalone sirve para volver a pulir reportes archivados o probar modelos alternativos.

## Ciclo de Vida de Ejecución
![Execution Lifecycle Diagram](docs/execution_lifecycle.svg)

1. **Parseo CLI y configuración del generador** – valida los flags de runtime, resuelve rutas y crea `ShowReportGenerator` con el provider/model solicitados.
2. **Inicialización del entorno** – carga `.env`, monta filesystem/memory backends, configura el cliente LLM y verifica la conectividad Neo4j.
3. **Template resolution** – inyecta valores de la config en el prompt y guarda la copia procesada en `reports/artifacts/`.
4. **Manifest & TODO synthesis** – traduce el prompt en manifest JSON, checklist TODO en Markdown, inventario de recuperación y snapshot de esquema.
5. **Agent bootstrap** – crea el DeepAgent con bindings a filesystem/Neo4j, un subagente Neo4j y un subagente de crítica.
6. **TODO alignment loop** – reconcilia la lista TODO emitida con el plan canónico y reintenta hasta `max_todo_plan_attempts` si detecta drift.
7. **Ejecución y monitoreo** – supervisa las tareas, valida outputs Neo4j/filesystem y levanta errores accionables si algo se detiene.
8. **Artifact persistence** – guarda TODOs, payloads JSON, respuestas del agente y artefactos reflejados en `reports/artifacts/` y `outputs/<event><year>/pre_show/`.

> ¿Necesitas más detalle? Revisa [docs/report_generation_steps.md](docs/report_generation_steps.md) para un desglose Input → Function → Output.

## Coordinación Multiagente
![DeepAgents Coordination Diagram](docs/agent_coordination.svg)

`ShowReportGenerator` alimenta al coordinador con el contexto del manifiesto y supervisa al subagente Neo4j (autor/ejecutor de Cypher) y al subagente de crítica (QA + guardrails). El diagrama resalta los enlaces bidireccionales entre agentes, el filesystem aislado, la superficie de herramientas Neo4j, los outputs espejados y el proveedor LLM.

## Superficie de Datos Neo4j
![Neo4j Database Map](docs/neo4j_database_map.svg)

El layout de Neo4j muestra las entidades específicas del evento (registrations, sessions, recommendations) consultadas mediante `get_neo4j_schema`, `read_neo4j_cypher` y `write_neo4j_cypher`. Usa este mapa para alinear el manifiesto con el esquema cuando diseñes configs o depures queries.

## Artefactos Generados
| Artefacto | Ubicación | Propósito |
| --- | --- | --- |
| Processed prompt | `reports/artifacts/processed_prompt_<event><year>.md` | Instrucciones exactas usadas por el agente. |
| Task manifest | `reports/artifacts/task_manifest_<event><year>.json` | Lista determinista de queries y tareas de síntesis. |
| TODO plan | `reports/artifacts/prebuilt_todos_<event><year>.md` | Markdown inyectado en `write_todos`. |
| Schema snapshot | `outputs/<event><year>/pre_show/neo4j_schema_<event><year>.json` | Exportación APOC fresca por corrida. |
| Recovery inventory | `reports/artifacts/recovery_inventory_<event><year>.md` | Enlaces a artefactos existentes/localizaciones en `/memories`. |
| Agent files | `reports/artifacts/todo_generation_<timestamp>/agent_files/` | Archivos creados por DeepAgents vía filesystem tools. |
| Memory mirrors | `/memories/<event><year>/pre_show/` | Copias redundantes para reruns y recuperación. |

## Observabilidad y Troubleshooting
- **Logging** – Usa `--verbose` para ver mensajes detallados.
- **Neo4j issues** – Busca `Neo4j Error executing read query`; `_normalize_cypher_identifiers` ayuda, pero configs inválidas aparecerán aquí.
- **TODO drift** – Si el agente modifica el plan canónico, los reintentos fuerzan la recarga del Markdown.
- **Filesystem writes** – El flujo falla si no encuentra archivos en `outputs/<event><year>/pre_show` para evitar falsos positivos.

## Extensiones y Personalización
- **Nuevos eventos** – Duplica un YAML, ajusta metadatos y apunta el CLI al nuevo archivo.
- **Evolución de prompts** – Actualiza `reports/prompts/*.md` y confirma que los regex del manifiesto siguen coincidiendo.
- **Herramientas adicionales** – Registra más herramientas DeepAgents (HTTP, analytics) dentro de `_create_agent`.
- **Almacenamiento alterno** – Extiende `SafeFilesystemBackend` para nuevas raíces sandbox o adaptadores cloud.

## Checklist de Mantenimiento
1. Mantén `requirements.txt` y `uv.lock` alineados.
2. Rota API keys y passwords Neo4j en `.env` por entorno.
3. Depura periódicamente `reports/artifacts/` y `/memories/` para controlar disco.
4. Valida nuevas configs con `python -m py_compile arc/pre_show/*.py` y una corrida en perfil staging.
5. Monitorea cambios de esquema Neo4j y ajusta `label_aliases`, `relationships` o `_normalize_cypher_identifiers` según sea necesario.
