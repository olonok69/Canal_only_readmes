# Azure AI Foundry OpenAPI SQL Chatbot

Este proyecto ofrece un chatbot de línea de comandos que se ejecuta sobre Azure AI Foundry Agents y usa una herramienta OpenAPI que expone una superficie SQL de solo lectura. Azure AI Foundry Agents proporcionan una capa administrada de orquestación para crear, ejecutar y escalar asistentes de IA capaces de invocar tools y mantener el contexto conversacional. OpenAPI es una especificación independiente del proveedor para describir APIs HTTP en formato JSON o YAML de forma legible por máquinas, lo que habilita validación automática y generación de clientes. El agente puede inspeccionar metadatos de la base de datos y ejecutar consultas SELECT a través del OpenAPI spec, devolviendo respuestas estructuradas directamente en el bucle de chat.

## Características

- Agente único de Azure AI Foundry conectado a una herramienta OpenAPI SQL personalizada.
- CLI interactiva para preguntas en lenguaje natural sobre el dataset conectado.
- Aplicación automática de las restricciones de solo lectura definidas en el OpenAPI schema.
- Flag opcional para limpiar el agente temporal después de cada ejecución.

## Requisitos previos

- Python 3.9 o superior.
- Un proyecto de Azure AI Foundry con un deployment de modelo (por ejemplo, `gpt-4o-mini`).
- Un service principal con acceso al project endpoint.
- Una conexión OpenAPI en el Azure AI project que inserte el header `data-sql` requerido por `schema.json`.

## Instalación

1. **Clonar y acceder al repositorio**
   ```powershell
   git clone https://github.com/olonok69/multi-agent-solution.git
   Set-Location multi-agent-solution\foundry_agent_openapi
   ```

2. **Crear y activar un virtual environment**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Instalar dependencias**
   ```powershell
   pip install -r requirements.txt
   ```

## Configuración

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
# Azure AI project
PROJECT_ENDPOINT=https://<tu-región>.services.ai.azure.com/api/projects/<tu-proyecto>
MODEL_DEPLOYMENT_NAME=<deployment-del-modelo>
PROJECT_OPENAPI_CONNECTION_NAME=<nombre-de-la-conexión-openapi>

# Credenciales del service principal
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
AZURE_CLIENT_SECRET=<client-secret>

# Opcional
DELETE_CREATED_AGENT=false
```

### Archivos clave

- `main.py` – Punto de entrada que carga el OpenAPI spec, crea el agente y ejecuta el bucle interactivo.
- `schema.json` – OpenAPI 3.1 document con cuatro endpoints SQL de solo lectura (`list_tables`, `describe_table`, `get_table_sample`, `execute_sql`). El header `data-sql` coincide con el esquema de seguridad `dataSqlHeader` de la conexión en Azure.

## Uso

Ejecuta el chatbot desde el directorio del proyecto:

```powershell
python main.py
```

1. El script crea la herramienta OpenAPI usando `schema.json` y la conexión indicada por `PROJECT_OPENAPI_CONNECTION_NAME`.
2. Se registra un agente llamado `openapi_chat_agent` con esa herramienta y se crea un thread de conversación.
3. Accedes al loop interactivo. Realiza preguntas como:
   - `Lista las tablas disponibles.`
   - `Describe las columnas de tbl_asp_exhibitors.`
   - `Ejecuta un select que cuente registros por día.`
4. Escribe `exit` (o presiona `Ctrl+C`) para salir. Si `DELETE_CREATED_AGENT` es verdadero (`true`, `1`, `yes`, `y`), el agente se elimina antes de finalizar el script.

## Tests

Ejecuta los unit tests centrados en el esquema para verificar que `schema.json` mantiene el esquema de seguridad y los endpoints de solo lectura esperados:

```powershell
python -m unittest discover -s test
```

La suite en `test/test_schema.py` carga el OpenAPI document y comprueba:
- La presencia del esquema de seguridad `dataSqlHeader` con el mapeo correcto al header `data-sql`.
- Que solo existan los cuatro endpoints de solo lectura (`list_tables`, `describe_table`, `get_table_sample`, `execute_sql`).
- Que la configuración de seguridad global requiera el header de la conexión Azure.

## Resolución de problemas

- **401 Unauthorized al llamar a la API**: Verifica que la conexión OpenAPI inserte el header `data-sql` y que el nombre de la conexión coincida con `PROJECT_OPENAPI_CONNECTION_NAME`.
- **Modelo no encontrado**: Confirma que `MODEL_DEPLOYMENT_NAME` corresponde a un deployment existente en tu Azure AI project.
- **Variables de entorno ausentes**: El script usa `python-dotenv`; asegúrate de que `.env` exista o exporta las variables en tu shell.

## Próximos pasos

- Extiende `schema.json` con más endpoints de solo lectura según crezca tu dataset.
- Reutiliza el mismo patrón de agente/thread para envolver la CLI en una interfaz web o Teams.
- Automatiza ejecuciones vía CI/CD tras resguardar secretos en Azure Key Vault o GitHub Actions secrets.
- Consulta la guía del Azure AI Agents Python SDK para escenarios avanzados: https://learn.microsoft.com/en-us/python/api/overview/azure/ai-agents-readme?view=azure-python
- Revisa la documentación oficial de OpenAPI Specification para definir el schema: https://swagger.io/specification/
