# Chatbot SQL con OpenAPI y Google ADK

Traducciones: English (README.md)

Este repositorio alberga un asistente conversacional construido con Google Agent Development Kit (ADK). El agente aprovecha la especificación OpenAPI (`schema.json`) para generar herramientas que interactúan con una API SQL de solo lectura. Con preguntas en lenguaje natural puedes:

- Listar las tablas disponibles.
- Consultar el esquema de una tabla.
- Obtener una muestra de filas.
- Ejecutar consultas `SELECT` parametrizadas.

El proyecto usa modelos de OpenAI mediante el adaptador LiteLLM de ADK y demuestra cómo combinar agentes ADK con integraciones REST descritas en OpenAPI.


## Tabla de Contenidos
- Panorama General
- Requisitos
- Preparación del Entorno
- Configuración
- Ejecución del Chatbot
- Estructura del Proyecto
- Resolución de Problemas
- Recursos Adicionales

## Panorama General
- **Script principal:** `openapi_sql_chatbot.py`
- **Componentes destacados:**
	- `OpenAPIToolset` interpreta el esquema y expone las operaciones REST como herramientas ADK.
	- `LiteLlm` conecta con modelos de OpenAI (por defecto `openai/gpt-4o`).
	- `Runner` e `InMemorySessionService` gestionan el estado de la conversación.
	- **Diagrama de arquitectura:** `docs/architecture.svg`

## Requisitos
- Python 3.10 o superior (probado con 3.12)
- PowerShell u otra terminal compatible (los ejemplos usan sintaxis de Windows)
- Acceso a modelos de OpenAI mediante API key
- Token Bearer para la API SQL definida en `schema.json`

## Preparación del Entorno
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
```

Si utilizas un entorno existente, verifica que `google-adk`, `litellm` y `pydantic` coincidan con las versiones de `requirements.txt`.

## Configuración
Las variables de entorno se cargan desde `.env` cuando `python-dotenv` está instalado.

| Variable | Obligatoria | Descripción |
| -------- | ----------- | ----------- |
| `OPENAI_API_KEY` | Sí | Habilita las llamadas a modelos de OpenAI mediante LiteLLM. |
| `OPENAPI_BEARER_TOKEN` | Sí | Se inyecta como autenticación Bearer al consumir la API SQL. |
| `WANDB_API_KEY` | Opcional | Envía las trazas OpenTelemetry hacia Weave. |
| `WANDB_PROJECT` | Opcional | Identificador `entity/project` de tu espacio en Weave. |
| `WANDB_BASE_URL` | Opcional | Sobrescribe el endpoint de Weave (por defecto `https://trace.wandb.ai`). |

Ejemplo de `.env`:
```
OPENAI_API_KEY=sk-tu-clave
OPENAPI_BEARER_TOKEN=tu-token-bearer
```

> Mantén privadas tus credenciales. El archivo `.env` incluido se ofrece únicamente como guía local.

## Ejecución del Chatbot
```powershell
python .\openapi_sql_chatbot.py [--verbose]
```

- Haz preguntas como “Lista las tablas de la base de datos” o “Muestra filas de ejemplo de `claims`”.
- El argumento opcional `--verbose` imprime las respuestas completas de cada herramienta para depuración.
- El script gestiona la autenticación automáticamente usando el token Bearer y la especificación OpenAPI.

**Trazas en Weave (opcional):** define `WANDB_API_KEY` y `WANDB_PROJECT` (y si lo deseas `WANDB_BASE_URL`) para enviar las trazas OpenTelemetry a Weave. Si faltan, la integración se omite sin interrumpir la ejecución.

## Estructura del Proyecto
```
.
├─ openapi_sql_chatbot.py         # Agente conversacional con herramientas OpenAPI
├─ schema.json                    # Esquema OpenAPI que describe la API SQL
├─ data/                          # Archivos JSONL de ejemplo (no necesarios para el chatbot)
├─ requirements.txt               # Dependencias de Python
└─ README*.md                     # Documentación en español e inglés
```

Pueden existir archivos heredados de experimentos previos, pero no son necesarios para ejecutar el chatbot.

## Resolución de Problemas
- **Credenciales ausentes**: Asegúrate de definir `OPENAI_API_KEY` y `OPENAPI_BEARER_TOKEN`. El chatbot finalizará con error si falta alguno.
- **Errores al invocar herramientas**: La API de destino es de solo lectura. Las consultas que no sean SELECT serán rechazadas y el agente devolverá el mensaje de error.
- **Conflictos con bucles asíncronos**: En notebooks, `asyncio.run` puede chocar con un loop activo. El script detecta este caso y usa el loop existente.

## Recursos Adicionales
- [Documentación de Google ADK](https://google.github.io/adk-docs/)
- [Guía de integración OpenAPI](https://google.github.io/adk-docs/tools-custom/openapi-tools/)
- [Modelos y adaptadores LiteLLM en ADK](https://google.github.io/adk-docs/models/)

Disfruta explorando tus fuentes de datos SQL mediante lenguaje natural.
