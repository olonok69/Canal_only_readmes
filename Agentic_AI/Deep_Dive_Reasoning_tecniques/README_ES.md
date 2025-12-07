# AgentsVille Trip Planner (Guía del Notebook)

Proyecto 1: crear un Agente para planificar el viaje perfecto a la ciudad ficticia de AgentsVille aplicando técnicas modernas de razonamiento LLM. Este proyecto aborda:

- Prompting basado en roles (roles especializados de planificador)
- Razonamiento Chain-of-Thought (CoT) para diseño de itinerarios
- Prompting ReAct (THOUGHT → ACTION → OBSERVATION)
- Bucles de retroalimentación usando herramientas de evaluación (evals) y un agente de revisión
- Schemas Pydantic para entrada/salida JSON fuertemente tipada

Toda la lógica reside en el Jupyter Notebook:

- `Project_AgentsVille Trip PLanner/project_starter.ipynb`

El notebook utiliza APIs simuladas (weather y activities) y un LLM real (OpenAI) para construir, verificar y revisar un plan de viaje.

---

## Diagrama de arquitectura

<img alt="AgentsVille Trip Planner Architecture" src="./diagrams/agentsville-architecture.svg" width="980" />

---

## Contenidos

- Descripción general
- Requisitos previos
- Configuración (API key y entorno)
- Cómo ejecutar (Windows PowerShell)
- Recorrido por el notebook
- Componentes clave y arquitectura
- Evaluaciones (Evals)
- Bucle de revisión ReAct
- Configuración/Personalización
---

## Descripción general

He implementado dos agentes:

1) ItineraryAgent (CoT):
   - Crea un TravelPlan día a día para las fechas y presupuesto especificados usando el contexto de Weather + Activities proporcionado.
   - Genera un objeto JSON estricto que se ajusta a un schema Pydantic (TravelPlan).

2) ItineraryRevisionAgent (ReAct):
   - Usa herramientas para evaluar y mejorar iterativamente el plan.
   - Debe pasar todas las evaluaciones e incorporar feedback del viajero (ej., "al menos dos actividades por día").

También incluye:
- Consultar datos simulados de weather/activities para una ventana de fechas
- Aplicar schemas con Pydantic
- Ejecutar evals para detectar problemas (desajustes de presupuesto, eventos alucinados, malas coincidencias de clima, etc.)
- Cerrar el bucle con ReAct usando herramientas (calculator, activities fetcher, eval runner, final answer)

---

## Requisitos previos

- Python 3.10+ (recomendado) (usar 3.13.0)
- VS Code con soporte para Jupyter 
- Una API key de OpenAI (requerida para llamadas LLM)

Dependencias del notebook (instaladas en las primeras celdas):
- `json-repair`
- `numexpr`
- `openai`
- `pandas`
- `pydantic`
- `python-dotenv`



## Configuración (API key y entorno)


Crear un archivo `.env` en la raíz del repositorio o en la carpeta del proyecto con:

```
OPENAI_API_KEY=TU_CLAVE_OPENAI
# Override opcional
# OPENAI_BASE_URL=https://api.openai.com/v1
```

El notebook carga `.env` automáticamente a través de `python-dotenv`.

---



## Recorrido por el notebook



1) Configuración inicial
   - Agrega la ruta del workspace (si es necesario)
   - Instala dependencias
   - Inicializa el cliente OpenAI desde las variables de entorno

2) Definir detalles de las vacaciones (Pydantic)
   - Ejemplo `VACATION_INFO_DICT`
   - Modelos Pydantic: `Traveler`, `VacationInfo`
   - La validación asegura que las fechas y campos requeridos sean correctos

3) Revisar horarios de Weather y Activity (APIs simuladas)
   - `call_weather_api_mocked` para cada fecha en la ventana del viaje
   - `call_activities_api_mocked` para cada fecha
   - DataFrames para previsualizar los datos

4) El ItineraryAgent (CoT)
   - Modelos de salida Pydantic: `Weather`, `Activity`, `ActivityRecommendation`, `ItineraryDay`, `TravelPlan`
   - El system prompt incluye:
     - Rol y Tarea
     - Formato de salida con ejemplo JSON
     - JSON Schema de TravelPlan (desde Pydantic) para forzar estructura
     - Contexto: inline WeatherForDates y ActivitiesForDates
   - `ItineraryAgent.get_itinerary(...)` llama al LLM y parsea JSON en `TravelPlan`

5) Evaluando el itinerario (Evals)
   - Helper `get_eval_results(...)` y `EvaluationResults`
   - Las evals incluyen:
     - Coincidencia de fechas (llegada/salida)
     - Precisión del costo total
     - Total dentro del presupuesto
     - Sin eventos alucinados (verificación event-by-id)
     - Intereses satisfechos por viajero
     - Compatibilidad climática (verificación basada en LLM)
   - `ALL_EVAL_FUNCTIONS` agrega estas

6) Definiendo las herramientas (Tools)
   - `calculator_tool(expr)`
   - `get_activities_by_date_tool(date, city)`
   - `run_evals_tool(travel_plan)`
   - `final_answer_tool(final_output)`
   - Las descripciones de herramientas se derivan de docstrings para el prompt ReAct

7) El ItineraryRevisionAgent (ReAct)
   - Texto de feedback del viajero: "Quiero tener al menos dos actividades por día."
   - Una nueva eval verifica que el feedback esté incorporado en el plan revisado
   - El system prompt ReAct fuerza THOUGHT y luego exactamente una ACTION como JSON estricto:
     ```json
     {"tool_name": "run_evals_tool", "arguments": {"travel_plan": { /* ... */ }}}
     ```
   - El bucle Python repara JSON si es necesario y enruta las llamadas a herramientas; devuelve el `TravelPlan` final cuando se invoca `final_answer_tool`

8) Verificaciones finales y visualización
   - Re-ejecutar todas las evals en el plan revisado
   - Renderizar actividades día a día y un resumen narrativo opcional

---

## Componentes clave y arquitectura

- Modelos Pydantic (barreras JSON estrictas):
  - Entrada: `VacationInfo`
  - Salida: `TravelPlan` (más `ItineraryDay`, `Activity`, `Weather` anidados)
- APIs simuladas (desde `project_lib.py`):
  - `call_weather_api_mocked(date, city)`
  - `call_activities_api_mocked(date, city)`
  - `call_activity_by_id_api_mocked(activity_id)`
- Cliente LLM:
  - Cliente OpenAI instanciado con `OPENAI_API_KEY` y `OPENAI_BASE_URL` opcional
- Agentes:
  - `ItineraryAgent` (CoT de un solo disparo)
  - `ItineraryRevisionAgent` (ReAct multi-paso con herramientas)
- Herramientas (Tools):
  - `calculator_tool`, `get_activities_by_date_tool`, `run_evals_tool`, `final_answer_tool`

---

## Evaluaciones (Evals)

Cada eval lanza un `AgentError` en caso de fallo, permitiendo que el bucle de revisión diagnostique y corrija problemas:

- Las fechas y rangos son consistentes
- La suma de precios de actividades es igual a `total_cost`
- `total_cost` ≤ presupuesto
- Los eventos del itinerario coinciden con eventos reales (simulados) por ID
- Cobertura de intereses entre viajeros
- Compatibilidad weather-actividad mediante una rúbrica LLM compacta
- El feedback del viajero está completamente incorporado (post-revisión)

`run_evals_tool` devuelve un dict conciso con `success` y `failures` para guiar las decisiones ReAct.

---

## Bucle de revisión ReAct

- El prompt fuerza: THOUGHT, luego una sola ACTION (JSON), luego OBSERVATION (agregada por Python), repetir.
- Usa `json-repair` para tolerar pequeños errores de formato JSON del LLM.
- Debe llamar a `run_evals_tool` antes de finalizar y nuevamente para confirmar el éxito.
- Termina solo cuando el LLM invoca `final_answer_tool` con un `TravelPlan` válido.

---

## Configuración/Personalización

- Detalles del viaje: editar `VACATION_INFO_DICT` (viajeros, destino, fechas, presupuesto, intereses)
- Restricciones de fechas/ciudad: los datos simulados ahora se extienden para AgentsVille desde 2025-06-10 hasta 2025-06-27 (actividades adicionales incluyendo opciones interiores tempranas y enfocadas en intereses)
- Selección de modelo: por defecto `gpt-4.1-mini`; se puede cambiar a otros modelos definidos en `OpenAIModel`
- Sensibilidad de costo/presupuesto: ajustar presupuesto y densidad del plan para explorar trade-offs
- Feedback: cambiar `TRAVELER_FEEDBACK` para probar diferentes objetivos de revisión

---

## Interfaz de línea de comandos (CLI)

Además del flujo de trabajo del notebook, un driver CLI ligero (`agentsville_trip_planner.py`) soporta ejecuciones automatizadas y logging.

Invocación básica (PowerShell):

```
python agentsville_trip_planner.py --log-revision --log-path logs/latest_revision.md --max-steps 8
```

Argumentos clave:

- `--max-steps N`                Limitar iteraciones del bucle de revisión (predeterminado 6).
- `--log-revision`               Habilitar logging detallado de pasos (bucle ReAct + resultados de eval).
- `--log-mode {md|json}`         Salida de log en Markdown (legible para humanos) o JSON (estructurado crudo).
- `--log-path PATH`              Archivo de destino para el log de revisión.
- `--no-log-patch`               Omitir diffs JSON patch de cambios en el itinerario (logs más pequeños).
- `--narrate`                    Incluir un resumen narrativo del plan final cuando esté soportado.

El archivo de log captura: encabezado meta, snapshot del plan inicial, resultados THOUGHT/ACTION por paso (salida LLM cruda truncada con razonamiento completo retenido si es corto), feedback de evaluación, correcciones automáticas adoptadas, y estado final del itinerario.

---

## Sistema de logging

`RevisionRunLogger` (en `logging_util.py`) registra la evolución del itinerario durante el ciclo de revisión.

Características:

- Flush incremental: escribe después de cada paso para evitar pérdida de datos en salida temprana.
- Umbral de salida cruda del modelo: las respuestas largas se truncan para mantener logs concisos mientras el razonamiento THOUGHT completo bajo un umbral de tamaño se preserva.
- Diffs JSON patch (opcional): resalta cambios estructurales en el itinerario entre pasos.
- Anotación de terminación temprana: marca claramente cuando las heurísticas acortan el bucle porque todas las evals pasaron.

Ejemplo (extracto Markdown):

```
## Steps
### Step 2 – Tool: run_evals_tool
THOUGHT: Verificando evaluaciones para ver problemas restantes.
Result: {"all_passed": false, "uncovered_interests": ["art"], ...}
Patch:
   - Agregada actividad event-2025-06-24-4 (Indoor Gallery Tour) al 2025-06-24
```

---

## Heurísticas y mejoras

Mejoras recientes para reducir uso innecesario de tokens y converger más rápido:

1. Terminación temprana de evaluación: Si una llamada a `run_evals_tool` reporta `all_passed`, el agente finaliza inmediatamente sin pasos adicionales de razonamiento.
2. Adopción automática de corrección de costos: Cuando las evals incluyen un `auto_corrected_travel_plan` (solo desajuste de costo total), se adopta automáticamente, seguido de un paso de eval confirmatorio y potencial finalización inmediata.
3. Auto evals post-mutación: Después de cualquier mutación del itinerario (agregar/eliminar/calculator), las evals se ejecutan automáticamente para prevenir que el modelo olvide y entre en bucles.
4. Guardia de bucle calculator: Detecta llamadas consecutivas redundantes a `calculator_tool` cuando el costo total permanece sin cambios; dispara evals y finalización si todas pasan.
5. Manejo de weather indoor: La eval de compatibilidad de weather puede permitir días marcados como outdoor-incompatible si al menos una actividad indoor está programada (detectada mediante keywords o flag indoor explícito en los metadatos de la actividad).
6. Prioridad de cobertura de intereses: Las actividades que coinciden con intereses no cubiertos se priorizan temprano, especialmente en días con pocas actividades.

---

## Validación de continuidad de datos

El script `validate_mock_data.py` valida que las actividades simuladas y el weather cubran cada fecha en el rango configurado y que las reglas de guardia se alineen (sin días faltantes). Ejecutarlo después de extender datasets:

```
python validate_mock_data.py
```

---

## Testing / Logging Harness

Un harness de prueba ligero (planeado `tests/test_logging_harness.py`) puede simular una ejecución de revisión corta con logging habilitado y afirmar que:

- El archivo de log se crea y no está vacío.
- Existe encabezado meta + al menos una sección Step.
- Está presente la sección de itinerario final.

Esto ayuda a proteger contra regresiones donde los cambios de serialización podrían descartar silenciosamente el contenido del log.

---

## Ideas de roadmap

- Modelos pluggables (Anthropic / local) con adaptador de schema unificado.
- Normalización de costos y manejo de moneda.
- Encadenamiento multi-ciudad con restricciones de transferencia.
- Capa de caché para búsquedas repetidas de actividad/fecha.
- Ponderación de diff estructural para sesgar revisiones hacia correcciones de cambio mínimo.

---

## Changelog (reciente)

- Agregado rango de fechas simuladas extendido (hasta 2025-06-27) con nuevos eventos indoor/art/technology.
- Implementada heurística de terminación temprana al pasar todas las evals.
- Agregada adopción automática del plan de corrección de costos.
- Agregada ejecución automática de eval post-mutación.
- Introducida guardia de bucle calculator / vía de finalización temprana.
- Agregada heurística de actividad indoor a la evaluación de weather.
- Agregado logging incremental de pasos con patches JSON opcionales.
- Agregados flags CLI: `--max-steps`, controles de logging, opción de salida narrativa.
- Agregado script de validación de continuidad de datos.
- Limpiada instrumentación de debug del código de producción.

---
