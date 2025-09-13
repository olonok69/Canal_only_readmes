# Azure AI Foundry Connected Agents - Sistema de Triaje de Tickets de Soporte

Una solución integral que demuestra la capacidad de connected agents de Azure AI Foundry mediante la construcción de un sistema inteligente de triaje de tickets de soporte. Este sistema utiliza múltiples agentes de IA especializados trabajando juntos para evaluar, priorizar y enrutar automáticamente tickets de soporte.

## 🏗️ Resumen de la Arquitectura

Esta solución implementa una **arquitectura multi-agent** donde un "triage agent" principal coordina con tres connected agents especializados para procesar tickets de soporte:

```
┌─────────────────┐
│   Triage Agent  │ ← Orquestador principal
│  (Coordinador)  │
└─────────┬───────┘
          │
          ├─── Priority Agent (Evaluación de Urgencia)
          ├─── Team Agent (Asignación de Equipo)  
          └─── Effort Agent (Estimación de Trabajo)
```

### Responsabilidades de los Agents

- **🎯 Triage Agent (Principal)**: Orquesta el workflow de procesamiento de tickets y delega tareas a agents especializados
- **⚡ Priority Agent**: Evalúa la urgencia del ticket (High/Medium/Low)
- **👥 Team Agent**: Determina la asignación apropiada de equipo (Frontend/Backend/Infrastructure/Marketing)
- **⏱️ Effort Agent**: Estima la complejidad del trabajo (Small/Medium/Large)

## 🔌 Protocolo de Comunicación

### Cómo se Comunican los Agents

Los connected agents de Azure AI Foundry utilizan **function calling** como protocolo principal de comunicación entre agents:

1. **Registration**: Los connected agents se registran con el main agent usando definiciones de `ConnectedAgentTool`
2. **Natural Language Routing**: El main agent utiliza comprensión de lenguaje natural para determinar cuándo delegar tareas
3. **Function Invocation**: Los connected agents son invocados como functions por el main agent
4. **Response Compilation**: El main agent compila respuestas de todos los connected agents

### Características Clave

- ✅ **No Requiere Custom Orchestration**: Azure maneja el routing automáticamente
- ✅ **Natural Language Delegation**: El main agent enruta tareas inteligentemente basado en descriptions
- ✅ **Diseño Modular**: Fácil agregar nuevos agents especializados sin modificar los existentes
- ✅ **Workflow Simplificado**: Descompone tareas complejas entre agents especializados

### Limitaciones del Protocolo

- ❌ Los connected agents no pueden llamar local functions usando function calling tool
- ❌ El citation passing desde connected agents no está garantizado
- ✅ Alternativas recomendadas: OpenAPI tools o Azure Functions para integraciones externas

## 🚀 Comenzando

### Prerequisitos

- Python 3.8+
- Proyecto de Azure AI Foundry con modelo deployado
- Service principal de Azure con permisos apropiados

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd azure-ai-foundry-agents
   ```

2. **Crear virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar environment variables**
   
   Crear un archivo `.env` en el directorio raíz:
   ```env
   # Configuración de Azure AI Foundry
   PROJECT_ENDPOINT=https://your-project.eastus.inference.ml.azure.com
   MODEL_DEPLOYMENT_NAME=your-model-deployment-name
   
   # Credenciales del Service Principal
   AZURE_TENANT_ID=your-tenant-id
   AZURE_CLIENT_ID=your-client-id
   AZURE_CLIENT_SECRET=your-client-secret
   ```

### Configuración de Azure

1. **Crear un proyecto de Azure AI Foundry**
   - Navegar a [Azure AI Foundry](https://ai.azure.com)
   - Crear un nuevo proyecto
   - Desplegar un language model (ej., GPT-4, GPT-3.5-turbo)

2. **Crear un service principal**
   ```bash
   az ad sp create-for-rbac --name "ai-foundry-agents-sp" \
     --role "Cognitive Services User" \
     --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group}
   ```

3. **Anotar los valores de output para tu archivo `.env`**

## 🎮 Uso

### Ejecutar la Aplicación

```bash
python main.py
```

### Ejemplo de Interacción

```
What's the support problem you need to resolve?: 
> The login page is completely broken and users can't access their accounts

Processing agent thread. Please wait.

USER:
The login page is completely broken and users can't access their accounts

AGENT:
Based on my analysis of this support ticket:

**Priority: High**
This is a user-facing blocking issue that prevents customers from accessing their accounts, requiring immediate attention.

**Team Assignment: Frontend**
This appears to be a user interface issue with the login page, which falls under frontend team responsibilities.

**Effort Estimation: Medium**
This will likely require 2-3 days of work to diagnose the root cause, implement a fix, and thoroughly test the login functionality.

**Summary:** High-priority frontend ticket requiring medium effort to resolve the login access issue.
```

## 📁 Estructura del Proyecto

```
azure-ai-foundry-agents/
├── main.py              # Script principal de la aplicación
├── requirements.txt     # Dependencias de Python
├── .env                # Variables de entorno (crear este archivo)
├── .gitignore          # Reglas de Git ignore
└── README.md           # Este archivo
```

## 🔧 Arquitectura del Código

### Componentes Principales

1. **Inicialización de Agents**
   ```python
   # Crear agents especializados
   priority_agent = agents_client.create_agent(
       model=model_deployment,
       name="priority_agent",
       instructions=priority_instructions
   )
   ```

2. **Connected Agent Tools**
   ```python
   # Registrar agents como tools para el main agent
   priority_agent_tool = ConnectedAgentTool(
       id=priority_agent.id,
       name="priority_agent",
       description="Assess the priority of a ticket"
   )
   ```

3. **Main Triage Agent**
   ```python
   # Crear agent orquestador con connected tools
   triage_agent = agents_client.create_agent(
       model=model_deployment,
       name="triage_agent",
       instructions=triage_instructions,
       tools=[priority_tool, team_tool, effort_tool]
   )
   ```

### Instructions de los Agents

Cada agent tiene instructions específicas y enfocadas:

- **Priority Agent**: Categoriza urgencia como High/Medium/Low basado en impacto al usuario
- **Team Agent**: Enruta a equipos Frontend/Backend/Infrastructure/Marketing
- **Effort Agent**: Estima como Small/Medium/Large basado en complejidad

## 🛡️ Consideraciones de Seguridad

- **Environment Variables**: Todas las credenciales sensibles almacenadas en archivo `.env`
- **Service Principal**: Usa acceso de privilegios mínimos con role assignments específicos
- **Credential Management**: Aprovecha Azure Identity library para autenticación segura

## 🚀 Extendiendo la Solución

### Agregando Nuevos Agents

1. **Crear el agent especializado**
   ```python
   new_agent = agents_client.create_agent(
       model=model_deployment,
       name="new_agent_name",
       instructions="Instructions específicas para el nuevo agent"
   )
   ```

2. **Registrar como connected tool**
   ```python
   new_agent_tool = ConnectedAgentTool(
       id=new_agent.id,
       name="new_agent_name",
       description="Description clara de cuándo usar este agent"
   )
   ```

3. **Agregar a los tools del main agent**
   ```python
   triage_agent = agents_client.create_agent(
       # ... otros parámetros
       tools=[existing_tools + [new_agent_tool.definitions[0]]]
   )
   ```

### Extensiones Potenciales

- **🔍 Research Agent**: Recopilar contexto adicional de knowledge bases
- **📧 Notification Agent**: Enviar alertas a miembros apropiados del equipo
- **📊 Analytics Agent**: Rastrear patterns de tickets y generar insights
- **🌐 Translation Agent**: Manejar tickets de soporte multi-idioma

## 📊 Consideraciones de Performance

- **Parallel Processing**: Los agents pueden potencialmente procesar diferentes aspectos simultáneamente
- **Cost Optimization**: Cada agent se enfoca en tareas específicas, reduciendo uso de tokens
- **Scalability**: Fácil agregar nuevos agents especializados sin afectar el workflow existente

## 🐛 Troubleshooting

### Problemas Comunes

1. **Authentication Errors**
   - Verificar credenciales del service principal en `.env`
   - Asegurar role assignments apropiados en Azure

2. **Model Deployment Issues**
   - Confirmar que el modelo está deployado y accesible
   - Verificar que el deployment name coincida con environment variable

3. **Agent Creation Failures**
   - Verificar que el project endpoint sea correcto
   - Asegurar permisos suficientes para creación de agents

### Debug Mode

Agregar logging para troubleshooting detallado:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Recursos Adicionales

- [Documentación de Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Guía de Connected Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/connected-agents)
- [Documentación de Azure Identity](https://docs.microsoft.com/en-us/python/api/azure-identity/)

## 🤝 Contribuyendo

1. Hacer fork del repositorio
2. Crear una feature branch
3. Realizar los cambios
4. Agregar tests si es aplicable
5. Enviar un pull request

## 📄 Licencia

Este proyecto está licenciado bajo la MIT License - ver el archivo LICENSE para detalles.

---

