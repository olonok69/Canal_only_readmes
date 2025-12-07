# Flujos de trabajo agénticos para la gestión de proyectos

## Descripción general del proyecto

Este repositorio muestra un recorrido en dos fases para construir flujos de trabajo agénticos que transforman especificaciones de producto en planes de proyecto accionables. La biblioteca de agentes ahora se encuentra en `lib/`, mientras que el flujo de trabajo orquestado vive en `agents/`.

- **Biblioteca de agentes (`lib/`)**: Implementa agentes basados en prompts, conocimiento aumentado, enrutamiento y evaluación, además de pruebas de soporte. Cada agente cumple con los requisitos de la rúbrica y se documenta en `lib/README.md` y `lib/README-es.md`.
- **Flujo de trabajo orquestado (`agents/`)**: Combina los agentes de la biblioteca para ingerir una especificación de producto, generar historias de usuario, funcionalidades y tareas de ingeniería, y capturar toda la ejecución en un informe Markdown. La documentación se encuentra en `agents/README.md` y `agents/README-es.md`.

Cada README cuenta con su versión en español o en inglés para que el proyecto se pueda explorar en ambos idiomas.

## Estructura del repositorio

```
.
├── docs/                         # Documentos de referencia sobre flujos agénticos y RAG
├── examples/                     # Scripts de demostración con patrones de flujo de trabajo
├── lib/                          # Implementaciones de agentes, pruebas y README bilingüe
├── agents/                       # Flujo orquestado, artefactos y README bilingüe
├── requirements.txt              # Dependencias compartidas de Python
├── README.md                     # (Este archivo) Resumen general en inglés
└── README-es.md                  # Resumen general en español
```

## Puesta en marcha rápida

1. **Instalar dependencias** (desde la raíz del repositorio):
   ```powershell
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno** creando un archivo `.env` en la raíz del proyecto (o dentro de `agents/`) con:
   ```text
   OPENAI_API_KEY=tu_clave_de_openai
   OPENAI_MODEL=gpt-3.5-turbo            # sobrescritura opcional
   OPENAI_EMBEDDING_MODEL=text-embedding-3-large  # sobrescritura opcional
   ```

3. **Explorar la biblioteca de agentes**:
   - Revisa `lib/README.md` para conocer las APIs y ejemplos de uso.
   - Ejecuta scripts o pruebas individuales, por ejemplo:
     ```powershell
     python lib\direct_prompt_agent_test.py
     python lib\routing_agent_test.py
     ```

4. **Ejecutar el flujo de trabajo orquestado** para generar un plan de proyecto completo y un informe en Markdown:
   ```powershell
   python agents\agentic_workflow.py
   ```
   La ejecución produce `agents\workflow_execution_report.md` y registros en consola con decisiones de enrutamiento y resultados de evaluación.

## Mapa de documentación

- `lib/README.md` – Referencia en inglés para los agentes, patrones de uso y pruebas.
- `lib/README-es.md` – Traducción al español de la guía de la biblioteca.
- `agents/README.md` – Recorrido en inglés del flujo orquestado, configuración y personalización.
- `agents/README-es.md` – Traducción al español de la guía del flujo orquestado.
- `docs/` – Lecturas de apoyo sobre generación aumentada por recuperación y modelado de flujos de trabajo.

## Notas adicionales

- El proyecto se desarrolló y validó sin hacer referencia a organizaciones o personas reales.
- Las mejoras opcionales (puntuaciones de evaluación extendidas, personas adicionales, registros más ricos) se detallan en los README de `lib/` y `agents/` para futuras exploraciones.
- Para el contexto del curso o los criterios de la rúbrica, consulta `project_overview.md`, `phase1.txt`, `phase2.txt` y `Rubric.txt` en la raíz del repositorio.

¡Disfruta descubriendo cómo los agentes modulares pueden colaborar para entregar planes de proyecto estructurados!