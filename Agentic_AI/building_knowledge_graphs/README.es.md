# Agentic Knowledge Graph (Aplicación Modular)

Este repositorio contiene una aplicación modular que construye un grafo de conocimiento Producto → Assembly → Part → Supplier en Neo4j a partir de archivos CSV. Separa responsabilidades en "agents" y un orquestador central, con configuración en YAML, secretos en `.env` y logging robusto.

- Arquitectura: `images/app_architecture.svg`
- Flujo de datos: `images/app_data_workflow.svg`
- Secuencia de ingest: `images/ingest_sequence.svg`

Resumen del pipeline:

![Entire solution](images/entire_solution_v2.svg)

![Arquitectura](images/app_architecture.svg)

Enlaces rápidos:
- Guía detallada del pipeline: docs/PIPELINE.md (English) · docs/PIPELINE.es.md (Español)
- Demo de esquema desde texto (estilo L8): docs/UNSTRUCTURED_DEMO.md
- Demo de extracción desde texto → ingestión: docs/EXTRACTION_DEMO.md

## Inicio rápido (Windows PowerShell)

1) Instalar dependencias
```
pip install -r requirements_app.txt
```

2) Configurar Neo4j en `.env`
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j
NEO4J_IMPORT_DIR=C:\\Path\\to\\Neo4j\\import
```

3) Verificar conectividad
```
python -m agentic_kg_app.cli ready --config .\configs\app.yaml
```

4) Cargar los CSVs de ejemplo
```
python -m agentic_kg_app.cli ingest --config .\configs\app.yaml --data-dir .\data
```

5) Ejecutar el pipeline (estructurado)
```
python -m agentic_kg_app.cli pipeline --config .\configs\app.yaml --data-dir .\data --llm --schema structured
```

6) Ejecutar el pipeline (esquema no estructurado desde .md/.txt → mapea a ingest vía CSV)
```
python -m agentic_kg_app.cli pipeline --config .\configs\unstructured_demo.yaml --data-dir .\data --llm --schema unstructured --text-dir .\unstructured
```

7) NUEVO: Extraer instancias directamente desde texto (sin CSV)
```
python -m agentic_kg_app.cli pipeline --config .\configs\unstructured_demo.yaml --extract-from-text --text-file .\unstructured\extract_demo.md --llm
```

8) Explorar el grafo
```
python .\examples\query_kg.py
python .\examples\query_extracted.py
```

## Qué hace la aplicación

- Carga configuración desde `configs/app.yaml` y variables de entorno desde `.env`.
- Proporciona un pipeline agentic: parsear la intención del usuario → sugerir archivos → proponer un esquema (structured + unstructured) → elegir el esquema → ingest.
- Asegura constraints de unicidad por label y clave.
- Carga nodos/relaciones usando uno de tres modos, elegido automáticamente:
  - Neo4j local: copiar CSVs a `NEO4J_IMPORT_DIR` y usar `LOAD CSV`.
  - Aura con CSVs publicados: usar `LOAD CSV` vía HTTP(S) con `csv_base_url`.
  - Aura (o cuando file imports no están disponibles): streaming desde CSVs locales con batches `UNWIND` (sin `LOAD CSV`).
- Comandos utilitarios para comprobar readiness y resetear el grafo.
- Logging a consola y a archivo rotativo `logs/app.log`.

## Estructura del paquete

```
agentic_kg_app/
  __init__.py
  cli.py                # Entry point para comandos (ready/reset/ingest/pipeline)
  orchestrator.py       # Conecta config, logging, Neo4j client y agents
  config.py             # Carga/validación de YAML + .env
  logging_setup.py      # Logging a consola + archivo rotativo
  neo4j_client.py       # Wrapper del driver de Neo4j
  utils.py              # Utilidades (copiar CSVs, construir SET dinámicos)
  agents/
    __init__.py
    data_ingest_agent.py                 # Copiar CSVs, constraints, cargar nodos/relaciones
    graph_ops_agent.py                   # Ready, clear, versiones
    user_intent_agent.py                 # Parsear objetivo del usuario (heurístico o LLM)
    file_suggestions_agent.py            # Sugerir CSVs relevantes (heurístico o LLM)
    schema_proposal_structured_agent.py  # Inferir esquema ingestable desde CSVs
    schema_proposal_unstructured_agent.py# Inferir esquema abstracto desde texto libre
    unstructured_ingest_agent.py         # NUEVO: extrae entidades/relaciones de texto e ingiere (instancias desde .md/.txt)
configs/
  app.yaml
  unstructured_demo.yaml                 # NUEVO: config de conveniencia para demos no estructuradas
images/
  app_architecture.svg
  app_data_workflow.svg
  ingest_sequence.svg
  entire_solution.png
docs/
  PIPELINE.md · PIPELINE.es.md
  UNSTRUCTURED_DEMO.md
  EXTRACTION_DEMO.md
```

## Cómo funciona

![Flujo de datos](images/app_data_workflow.svg)

1. Ejecutas un comando CLI (`pipeline` o `ingest`) con `--config` y opcional `--data-dir`.
2. El Orchestrator carga YAML + `.env`, configura logging y crea el cliente de Neo4j.
3. Según el comando:
   - Pipeline: los agents colaboran para parsear intención → sugerir archivos → proponer esquemas → seleccionas un esquema → se ejecuta el ingest con ese esquema.
   - Ingest: aplica directamente el esquema definido en `configs/app.yaml`.
4. Se aseguran constraints de unicidad.
5. Se elige el modo de ingest:
   - `LOAD CSV file:///` en Neo4j local cuando `NEO4J_IMPORT_DIR` es accesible.
   - `LOAD CSV https://...` cuando `csv_base_url` está configurado (ideal para Aura).
   - Streaming por `UNWIND` cuando no hay file imports o prefieres no publicar CSVs.
6. Logging a consola y `logs/app.log`.

### Secuencia de ingest

![Ingest sequence](images/ingest_sequence.svg)

- `python -m agentic_kg_app.cli ingest --config .\configs\app.yaml --data-dir .\data`
- Cargar YAML + `.env` → configurar logging → crear Neo4j client
- Copiar CSVs → crear constraints → cargar nodos → cargar relaciones
- Devolver éxito o un error claro

## Configuración

`configs/app.yaml` define nodos, relaciones, logging y conexión Neo4j. Las variables de entorno pueden sobrescribir valores.

- Conexión Neo4j (valores en `.env`):
```
neo4j:
  uri: "${NEO4J_URI}"
  username: "${NEO4J_USERNAME}"
  password: "${NEO4J_PASSWORD}"
  database: "${NEO4J_DATABASE}"
  import_dir: "${NEO4J_IMPORT_DIR}"
```

- Nodos (archivo CSV, label, unique_key, properties):
```
nodes:
  - file: products.csv
    label: Product
    unique_key: product_id
    properties: [product_name, price, description]
  - file: assemblies.csv
    label: Assembly
    unique_key: assembly_id
    properties: [assembly_name, quantity, product_id]
  - file: parts.csv
    label: Part
    unique_key: part_id
    properties: [part_name, quantity, assembly_id]
  - file: suppliers.csv
    label: Supplier
    unique_key: supplier_id
    properties: [name, specialty, city, country, website, contact_email]
```

- Relaciones (archivo CSV, tipo, from/to labels y keys):
```
relationships:
  - file: assemblies.csv
    type: HAS_ASSEMBLY
    from_label: Product
    from_key: product_id
    to_label: Assembly
    to_key: assembly_id
  - file: parts.csv
    type: HAS_PART
    from_label: Assembly
    from_key: assembly_id
    to_label: Part
    to_key: part_id
  - file: part_supplier_mapping.csv
    type: SUPPLIED_BY
    from_label: Part
    from_key: part_id
    to_label: Supplier
    to_key: supplier_id
```

- Logging:
```
logging:
  level: INFO
  dir: logs
  file: app.log
  maxBytes: 5000000
  backupCount: 3
```

## Variables de entorno

Crea `.env` en la raíz (basado en `.env.example`) y completa:

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j
NEO4J_IMPORT_DIR=C:\\Path\\to\\Neo4j\\import
```

- `NEO4J_IMPORT_DIR` debe apuntar al import dir del servidor Neo4j para `LOAD CSV`.
- Si no se proporciona, la app intenta detectarlo vía `dbms.listConfig()`.

Opcional (LLM/ADK):

```
# Escoge uno de estos proveedores
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# Opcional: modelo explícito con prefijo de proveedor
LLM_MODEL=openai/gpt-4.1
```

Selección de modelo/proveedor:
- Si pasas un modelo sin prefijo (p. ej., `gpt-4.1`), la app infiere el proveedor (`openai/gpt-4.1`).
- Si tienes ambas claves (OpenAI y Google), fija `LLM_MODEL` para evitar ambigüedad.

## Logging

- Logging en consola y archivo rotativo `logs/app.log` (configurable en YAML).
- Tamaño de rotación y backups ajustables en `logging`.

## Uso de CLI (PowerShell)

Comprobar readiness:
```
python -m agentic_kg_app.cli ready --config .\configs\app.yaml
```

Resetear el grafo (DESTRUCTIVO):
```
python -m agentic_kg_app.cli reset --config .\configs\app.yaml
```

Ingest directo desde `data/` a Neo4j:
```
python -m agentic_kg_app.cli ingest --config .\configs\app.yaml --data-dir .\data
```

Ejecutar el pipeline guiado:
```
python -m agentic_kg_app.cli pipeline --config .\configs\app.yaml --data-dir .\data
```

Habilitar agents con LLM y selección no interactiva:
```
python -m agentic_kg_app.cli pipeline --config .\configs\app.yaml --data-dir .\data --llm --schema structured
```

Flags:
- `--llm` usa agents con LLM (con fallback heurístico).
- `--text` provee texto semilla para el agente unstructured.
- `--schema structured|unstructured|1|2` selecciona el esquema sin prompt.
- `--text-file` puede usarse múltiples veces para incluir archivos .md/.txt como entradas no estructuradas.
- `--text-dir` incluye todos los .md/.txt de un directorio (recursivo) como entradas no estructuradas.
- `--extract-from-text` ejecuta la nueva ruta de extracción de instancias (ver abajo), omitiendo la ingesta vía CSV.

### Etapas del pipeline

1) User Intent (UserIntentAgent)
- Heurístico o LLM para extraer `{kind, description}`.

2) File Suggestions (FileSuggestionsAgent)
- Escanea `--data-dir` y ordena CSVs relevantes; LLM puede refinar la aprobación.

3) Schema Proposals
- Structured (SchemaProposalStructuredAgent): infiere nodos/relaciones desde los CSVs aprobados.
- Unstructured (SchemaProposalUnstructuredAgent): infiere entidades/relaciones desde texto; luego materializamos un esquema ingestable mapeando a tus archivos/keys.

4) Selección
- Elige entre propuestas structured o unstructured (o pasa `--schema`).

5) Ingest
- Asegura constraints y carga nodos/relaciones usando el mejor modo disponible (LOAD CSV local, LOAD CSV HTTP(S), o streaming UNWIND).

### Demo de esquema no estructurado (estilo L8)

Usa .md/.txt para derivar un esquema (labels/relaciones) con LLM y luego mapearlo a tus CSVs para ingerir:

```
# Desde la raíz del repo
python -m agentic_kg_app.cli pipeline --config .\configs\unstructured_demo.yaml --data-dir .\data --llm --schema unstructured --text-dir .\unstructured
```

Más detalles en docs/UNSTRUCTURED_DEMO.md.

### NUEVO: Extraer instancias desde texto (sin CSV)

Si quieres crear un pequeño KG directamente desde texto, usa esta ruta de extracción:

```
# Un archivo
python -m agentic_kg_app.cli pipeline --config .\configs\unstructured_demo.yaml --extract-from-text --text-file .\unstructured\extract_demo.md --llm

# O una carpeta completa de .md/.txt
python -m agentic_kg_app.cli pipeline --config .\configs\unstructured_demo.yaml --extract-from-text --text-dir .\unstructured --llm
```

Qué hace:
- Llama a un LLM para producir JSON con nodos (label, key?, props) y relaciones (type, from/to label+key?).
- Genera un `_key` estable si no se provee (hash de label+name/props).
- Ingresa nodos y aristas vía UNWIND. Puede convivir con tu grafo basado en CSVs.

Consulta docs/EXTRACTION_DEMO.md para pasos de verificación y notas.

## Dependencias

Instala dependencias mínimas:
```
pip install -r requirements_app.txt
```

O asegúrate de tener:
- neo4j
- python-dotenv
- PyYAML

## Solución de problemas

- Errores renderizando SVG: si ves `xmlParseEntityRef: no name`, asegura usar `&amp;` en vez de `&` en el texto de los SVGs.
- Autenticación Neo4j: revisa `NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD` y que la DB esté corriendo.
- Permisos import dir: el usuario debe poder escribir en el import dir de Neo4j.
- Codificaciones CSV mixtas: se espera UTF-8; ajusta si usas otra.

## Ejecución en Neo4j Aura

Neo4j Aura no permite `file:///` en `LOAD CSV`. Usa URLs HTTP(S) y configura una base:

1) Publica tus CSVs (GitHub raw, Azure Blob static website, S3, GCS, etc.).
2) Configura `csv_base_url` en `configs/app.yaml` o `NEO4J_CSV_BASE_URL` en `.env`.
3) Ejecuta ingest normalmente:
```
python -m agentic_kg_app.cli ingest --config .\configs\app.yaml --data-dir .\data
```

Cuando `csv_base_url` está presente:
- Se construyen URLs como `https://.../products.csv` en vez de `file:///products.csv`.
- Se omite copiar archivos al import dir de Neo4j.
- No se requiere `dbms.security.allow_csv_import_from_file_urls`.

Alternativa (sin publicar): Streaming ingest

Si no quieres publicar CSVs, la app puede hacer streaming con batches `UNWIND` hacia Aura. Evita `LOAD CSV` completamente y se elige automáticamente cuando no hay file imports ni `csv_base_url`.

## ADK y agents con LLM (opcional)

La app incluye adaptadores opcionales para Google ADK y flujos con LLM. Si no los instalas, el CLI principal sigue funcionando.

### Instalar dependencias opcionales
```
pip install google-adk==1.5.0 google-genai>=0.3.0 litellm==1.73.6
```

Claves en `.env`:
```
# Una es suficiente
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# Opcional: model con prefijo de proveedor
LLM_MODEL=openai/gpt-4.1
```

Herramientas/agents disponibles:
- ADK tools wrapper: `agentic_kg_app/adk/tools_adk.py`
  - `neo4j_is_ready`, `clear_neo4j_data`, `drop_neo4j_indexes`, `get_apoc_version`, `get_neo4j_version`, `sample_file`
  - State helpers: `get_approved_user_goal`, `get_approved_files`
- ADK bridge: `agentic_kg_app/adk/bridge.py` expone `AgentCaller` y `make_agent_caller`
- LLM router: `agentic_kg_app/adk/llm.py` selecciona Gemini u OpenAI vía `litellm`

Flujos con LLM (con fallback):
- User intent: `UserIntentAgent.parse_llm(prompt)` → `{kind, description}`
- File suggestions: `FileSuggestionsAgent.suggest_llm(data_dir, user_goal)` → `approved_files`
- Schema proposal (structured): `SchemaProposalStructuredAgent.propose_llm(data_dir, approved_files)` → nodes/relationships
- Schema proposal (unstructured): `SchemaProposalUnstructuredAgent.propose_llm(texts)` → entities/relations

Todos los métodos con LLM hacen fallback a heurísticas si no hay clave o falla la llamada. La app normaliza nombres de modelos (p. ej., `gpt-4.1` → `openai/gpt-4.1`) para evitar errores de proveedor.
