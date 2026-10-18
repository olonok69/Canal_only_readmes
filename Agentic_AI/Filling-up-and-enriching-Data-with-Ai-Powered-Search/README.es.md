# Missing Practices Classification Toolkit

Este proyecto enriquece un catálogo de clínicas veterinarias combinando distintos pipelines de investigación con clasificación impulsada por Azure OpenAI. Dispone de varias estrategias intercambiables para recopilar evidencias (Perplexity, Firecrawl, Google Custom Search) junto con una utilidad de comparación para evaluar cómo se comportan los pipelines con el mismo lote de empresas. Además, incluye un bot conversacional (`firecrawl_bot.py`) que usa Firecrawl para aumentar contexto bajo demanda: si no proporcionas URLs, precarga automáticamente `https://www.promptingguide.ai/` para que puedas empezar a preguntar de inmediato y luego añadir fuentes adicionales.

## 1. Instalación y configuración

### Requisitos previos

- Python 3.11 o superior (probado con Python 3.13.3).
- Capacidad para crear un entorno virtual (`python -m venv .venv`).
- Credenciales de las APIs que vayas a utilizar (Perplexity, Firecrawl, Google Custom Search, Azure OpenAI).

### Dependencias

```powershell
# Desde la raíz del repositorio
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

El archivo `requirements.txt` incluye:

- `pandas`, `python-dotenv`, `langchain-openai` (comunes a todos los scripts).
- `perplexityai`, `firecrawl-py`, `google-api-python-client`, `requests` para las integraciones específicas.

### Variables de entorno

Todos los scripts cargan credenciales desde `.env` mediante `python-dotenv`. Añade las variables necesarias según el pipeline que vayas a ejecutar:

| Variable | Uso |
| --- | --- |
| `AZURE_API_KEY`, `AZURE_ENDPOINT`, `AZURE_DEPLOYMENT`, `AZURE_API_VERSION` | Requeridas para cualquier pipeline que use Azure OpenAI. |
| `PERPLEXITY_API_KEY`, `PERPLEXITY_MODEL` | Solo necesarias para `tag_missing_practices.py`. |
| `FIRECRAWL_API_KEY` | Necesaria para `tag_missing_practices_firecrawl.py`. |
| `GOOGLE_API_KEY` o `GOOGLE_DEVELOPER_API_KEY` | Clave para Google Custom Search. |
| `GOOGLE_SEARCH_ENGINE_ID` | ID del Custom Search Engine asociado a tu cuenta. |

> Consejo: evita duplicar las mismas claves dentro del `.env` para facilitar el mantenimiento.

## 2. Datos de entrada compartidos

Los cuatro scripts consumen idénticos CSVs ubicados en `data/`:

- `missing_practice_companies_lva2025.csv`: listado de empresas sin etiquetar (generado por `find_missing_practices.py`).
- `practices_missing.csv`: catálogo maestro con las prácticas ya enriquecidas.
- `Registration_data_with_demographicdata_bva_this.csv`: export de registros usada para enriquecer los prompts.
- `spezialization_to_stream.csv`: diccionario de tags permitidos (Small Animal, Equine, etc.).

## 3. Scripts principales

### 3.1 `tag_missing_practices.py`

- Pipeline original basado en Perplexity.
- Construye prompts con datos de registro y delega búsqueda + clasificación en Perplexity.
- Parámetros relevantes: `--limit`, `--dry-run`, `--batch-size`, `--model`, `--temperature`, `--max-tokens`.
- Ejemplo:

```powershell
python tag_missing_practices.py --limit 10 --dry-run --verbose
```

### 3.2 `tag_missing_practices_firecrawl.py`

- Sustituye Perplexity por Firecrawl (búsqueda y scraping) pero mantiene Azure OpenAI para etiquetar.
- `FirecrawlResearcher` arma la query con metadatos + `--query-keywords`.
- Parámetros clave: `--firecrawl-limit`, `--firecrawl-scrape-top`, `--firecrawl-location`, `--firecrawl-tbs`, `--firecrawl-categories`.
- Ejemplo:

```powershell
python tag_missing_practices_firecrawl.py --dry-run --limit 5 --verbose --firecrawl-scrape-top 8
```

> Nota: Firecrawl no puede scrapear ciertos dominios (Facebook, Yelp). Verás mensajes DEBUG indicando “Website Not Supported”.

### 3.3 `tag_missing_practices_google.py`

- Pipeline que usa Google Custom Search para obtener snippets y, opcionalmente, descargar páginas.
- Los resultados y extractos se incorporan al prompt enviado a Azure OpenAI.
- Parámetros interesantes: `--google-num`, `--google-fetch-top`, `--google-fetch-char-limit`, `--google-language`, `--google-country`, `--google-date-restrict`.
- Ejemplo:

```powershell
python tag_missing_practices_google.py --dry-run --limit 5 --verbose --google-fetch-top 8
```

### 3.4 `compare_classifications.py`

- Ejecuta los tres pipelines en modo `--dry-run`, analiza las líneas `Proposed entry ->` y produce un informe Markdown.
- Puedes elegir reporte detallado (por defecto) o tabla resumida usando `--summary`.
- Parámetros: `--firecrawl-args`, `--perplexity-args`, `--google-args`, `--summary`, `--output`.
- Ejemplos:

```powershell
python compare_classifications.py
python compare_classifications.py --summary --output comparacion.md
```

### 3.5 `firecrawl_bot.py`

- **Propósito:** Responder preguntas conversacionales apoyándose en contenido real obtenido con Firecrawl. Cuando no se pasan URLs, el bot carga por defecto `https://www.promptingguide.ai/` y lista las fuentes activas antes de iniciar la charla; así puedes arrancar sin fricción y sumar más contexto con el comando `/add`.
- **Modos de uso:**
	- Consulta única (`--question` + `--url`).
	- Chat interactivo (`--interactive`) con memoria configurable (`--memory-turns`) y acceso a `/sources` para ver las URLs citadas.
	- Modo agente (`--agent`) que permite al modelo lanzar búsquedas `site:<dominio>` y scrapes dinámicos definidos por `--site-root`, `--agent-search-limit`, `--agent-scrape-top`.
- **Opciones relevantes:** `--url`, `--firecrawl-char-limit`, `--firecrawl-formats`, `--max-sources`, `--temperature`, `--agent-scrape-char-limit`, `--agent-search-limit`, `--verbose`.
- **Ejemplos:**

```powershell
# Conversación inmediata usando el contexto por defecto
python firecrawl_bot.py --interactive --memory-turns 6

# Pregunta puntual sobre una URL concreta
python firecrawl_bot.py \
		--url https://ejemplo.com/docs/producto \
		--question "¿Qué opciones de despliegue se describen?"

# Explorar un sitio completo en modo agente
python firecrawl_bot.py \
		--agent --site-root https://ejemplo.com \
		--question "Resume las políticas de cumplimiento publicadas en 2024" \
		--agent-search-limit 5 --agent-scrape-top 3
```

## 4. Flujo de trabajo recomendado

1. Genera `missing_practice_companies_lva2025.csv` con `find_missing_practices.py`.
2. Ejecuta el pipeline seleccionado con `--dry-run` y `--verbose` para validar resultados.
3. Ajusta parámetros de búsqueda (Firecrawl/Google) o de Perplexity según convenga.
4. Rerun sin `--dry-run` cuando estés conforme; las nuevas filas se fusionan en `practices_missing.csv` conservando lo existente.
5. Usa `compare_classifications.py` para revisar discrepancias antes de consolidar.

## 5. Resolución de problemas

- **Errores de credenciales:** los scripts lanzan `RuntimeError` explicativos si falta alguna variable clave.
- **Advertencias de scraping:** ignora los avisos de Firecrawl para dominios no soportados o recurre al pipeline de Google.
- **Tokens excesivos:** si Azure rechaza prompts, reduce `--google-fetch-char-limit` / `--firecrawl-scrape-char-limit` o `--max-tokens`.
- **Empresas específicas:** `--company "Nombre Normalizado"` permite procesar casos aislados.

## 6. Próximos pasos sugeridos

- Cachear resultados de búsqueda para reducir coste.
- Añadir métricas de acuerdo entre pipelines al comparador.
- Exportar reportes a CSV/JSON para auditoría más profunda.

Con esta guía deberías poder configurar credenciales, comprender el propósito de cada script y combinar pipelines según tus necesidades. El bot Firecrawl te servirá de asistente para validar evidencias antes de automatizarlas. ¡Éxitos enriqueciendo el dataset!.
