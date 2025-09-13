# Aplicación Azure AI Agent

Una aplicación Python que demuestra la integración con Azure AI Foundry Agent Service para pronósticos automatizados de producción de trigo. Esta aplicación se conecta a agentes de Azure AI, procesa consultas de usuarios sobre datos agrícolas y genera reportes comprehensivos en formato markdown.

## Descripción General

Esta aplicación muestra las capacidades de integración de Azure AI Foundry Agent Service mediante la implementación de un workflow completo para consultar agentes de IA especializados y documentar sus respuestas. La aplicación cuenta con un agente especializado en pronósticos de producción de trigo que proporciona análisis detallados de datos agrícolas para los principales países y regiones productores de trigo a nivel mundial.

## Características

### Funcionalidad Principal
- **Integración de Agentes**: Conexión fluida a agentes de Azure AI Foundry usando autenticación de service principal
- **Gestión de Conversaciones**: Manejo completo de conversaciones basadas en threads con gestión automática de estado
- **Procesamiento de Respuestas**: Análisis y formateo inteligente de respuestas de agentes con manejo de citaciones
- **Generación de Reportes**: Creación automática de reportes estructurados en markdown con documentación timestamped
- **Manejo de Errores**: Gestión comprehensiva de errores con logging detallado y feedback al usuario

### Capacidades Técnicas
- Autenticación service principal para integración empresarial segura
- Procesamiento asíncrono con monitoreo de estado en tiempo real
- Soporte para múltiples tipos de mensajes y formateo de contenido enriquecido
- Extracción de citaciones y referencias de fuentes
- Organización automática de archivos y archivado de reportes

## Arquitectura

La aplicación sigue una arquitectura modular con clara separación de responsabilidades:

```
main.py                     # Lógica principal de la aplicación y orquestación
.env_template              # Template de configuración de entorno
reports/                   # Directorio de reportes markdown generados
├── agent_report_YYYYMMDD_HHMMSS.md
```

### Componentes Clave

1. **Capa de Autenticación**: Maneja la autenticación de service principal de Azure usando ClientSecretCredential
2. **Cliente de Agente**: Gestiona conexiones e interacciones con agentes de Azure AI Foundry
3. **Motor de Conversación**: Procesa consultas de usuario y gestiona threads de conversación
4. **Generador de Reportes**: Crea documentación estructurada en markdown con metadata
5. **Gestión de Errores**: Proporciona manejo comprehensivo de errores y feedback al usuario

## Prerrequisitos

### Requisitos de Azure
- Suscripción de Azure con permisos apropiados
- Recurso y proyecto de Azure AI Foundry configurados
- Service principal con los siguientes roles:
  - Rol Azure AI User (mínimo requerido)
  - Rol Contributor o Cognitive Services Contributor (preferido)

### Entorno de Desarrollo
- Python 3.8 o superior
- Azure CLI configurado y autenticado
- Paquetes Python requeridos (ver sección de Instalación)

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd azure-ai-agent-application
   ```

2. **Crear y activar entorno virtual**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install azure-ai-projects
   pip install azure-identity
   pip install python-dotenv
   ```

4. **Configurar variables de entorno**
   ```bash
   cp .env_template .env
   # Editar .env con sus credenciales y endpoints de Azure
   ```

## Configuración

### Variables de Entorno

La aplicación requiere las siguientes variables de entorno configuradas en un archivo `.env`:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `AZURE_TENANT_ID` | ID del tenant de Azure Active Directory | `b64b8697-93dc-4cc3-b2cf-8fa28f0b81f9` |
| `AZURE_CLIENT_ID` | ID de aplicación del service principal | `947fca35-35c1-4316-af96-dc987ad57f98` |
| `AZURE_CLIENT_SECRET` | Secret del service principal | `your-client-secret` |
| `PROJECT_ENDPOINT` | Endpoint del proyecto de Azure AI Foundry | `https://your-resource.services.ai.azure.com/api/projects/your-project` |

### Configuración del Agente

La aplicación está configurada para trabajar con un agente específico de pronósticos de producción de trigo:
- **Agent ID**: `asst_qBqX2IRzQoyw68eJzo4Txzx8`
- **Nombre del Agente**: Agent_wheat
- **Especialización**: Análisis de datos agrícolas y pronósticos de producción de trigo

## Uso

### Ejecutar la Aplicación

Ejecutar el script principal de la aplicación:

```bash
python main.py
```

### Workflow de la Aplicación

1. **Establecimiento de Conexión**: La aplicación se conecta a Azure AI Foundry usando credenciales de service principal
2. **Carga del Agente**: Recupera el agente especificado de pronósticos de producción de trigo
3. **Creación de Thread**: Crea un nuevo thread de conversación para la sesión
4. **Procesamiento de Consulta**: Envía la consulta predefinida de pronóstico de producción de trigo al agente
5. **Manejo de Respuesta**: Procesa la respuesta del agente, incluyendo citaciones y fuentes
6. **Generación de Reporte**: Crea un reporte markdown timestamped con detalles completos de la conversación

### Consulta de Ejemplo

La aplicación procesa consultas sobre pronósticos de producción de trigo:

```
Tell me Forecast of Production Wheat 2025 for the following Countries World, US, Russia, EU, China, India and Canada. Try to get concrete numbers.
```

## Salida

### Salida de Consola

La aplicación proporciona salida detallada en consola incluyendo:
- Estado de conexión e información del agente
- Indicadores de procesamiento en tiempo real
- Visualización formateada de conversación con timestamps
- Citaciones de fuentes y referencias
- Resumen de completado de sesión con estadísticas

### Reportes Generados

Cada sesión genera un reporte comprehensivo en markdown que contiene:
- **Metadata de Sesión**: Timestamp, información del agente, thread ID
- **Resumen de Request**: Descripción general de la consulta del usuario
- **Pregunta del Usuario**: Consulta original completa
- **Respuesta del Agente**: Respuesta completa formateada con citaciones
- **Referencias de Fuentes**: Todas las fuentes citadas y anotaciones

### Estructura del Reporte

```markdown
# Azure AI Agent Report

**Generated on:** YYYY-MM-DD HH:MM:SS
**Agent:** Agent_wheat (asst_qBqX2IRzQoyw68eJzo4Txzx8)
**Thread ID:** thread_xxxxxxxxxxxxx

## Request Summary
[Resumen automatizado del request]

## User Question
[Consulta original del usuario]

## Agent Response
[Respuesta completa del agente con formato y citaciones]

---
*This report was automatically generated by Azure AI Foundry Agent Service*
```

## Mejores Prácticas

### Seguridad
- Nunca comprometer credenciales sensibles en control de versiones
- Usar variables de entorno para toda la configuración
- Implementar procedimientos apropiados de rotación de secrets
- Seguir el principio de menor privilegio para asignación de roles

### Rendimiento
- Implementar connection pooling para escenarios de alto volumen
- Monitorear consumo de tokens e implementar rate limiting
- Usar valores de timeout apropiados para consultas de larga duración
- Cachear información solicitada frecuentemente cuando sea aplicable

### Manejo de Errores
- Implementar lógica de retry comprehensiva con exponential backoff
- Registrar información detallada de errores para debugging
- Proporcionar mensajes de error amigables al usuario
- Monitorear estado del agente y manejar fallas graciosamente

## Resolución de Problemas

### Problemas Comunes

**Errores de Autenticación**
- Verificar que las credenciales del service principal sean correctas
- Asegurar asignaciones de rol apropiadas a nivel de proyecto
- Revisar configuración del tenant de Azure Active Directory

**Problemas de Conexión**
- Validar formato de URL del endpoint del proyecto
- Confirmar conectividad de red a servicios de Azure
- Verificar disponibilidad regional de servicios

**Errores del Agente**
- Confirmar que el Agent ID existe y es accesible
- Revisar estado de deployment del agente
- Verificar deployment del modelo y disponibilidad de quota

### Modo Debug

Para debugging detallado, modificar la aplicación para incluir logging adicional:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contribución

### Setup de Desarrollo
1. Fork del repositorio
2. Crear branch de feature
3. Implementar cambios con testing apropiado
4. Enviar pull request con descripción detallada

### Estándares de Código
- Seguir guías de estilo PEP 8 de Python
- Incluir manejo comprehensivo de errores
- Agregar documentación y comentarios apropiados
- Mantener compatibilidad hacia atrás cuando sea posible

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo LICENSE para detalles.

## Recursos Relacionados

### Documentación de Azure AI Foundry
- [Azure AI Foundry Agent Service Overview](https://learn.microsoft.com/azure/ai-foundry/agents/overview)
- [Agent Service Quickstart Guide](https://learn.microsoft.com/azure/ai-foundry/agents/quickstart)
- [Authentication and Security](https://learn.microsoft.com/azure/ai-foundry/agents/environment-setup)

### Referencias de SDK
- [Azure AI Projects Python SDK](https://aka.ms/azsdk/azure-ai-projects/python/reference)
- [Azure Identity Library](https://docs.microsoft.com/python/api/azure-identity/)
- [Azure AI Agents Models](https://learn.microsoft.com/python/api/azure-ai-agents/)

### Soporte y Comunidad
- [Azure AI Services Technical Community](https://techcommunity.microsoft.com/t5/azure-ai/ct-p/AzureAI)
- [Azure Support Portal](https://azure.microsoft.com/support/)
- [Azure Service Health Dashboard](https://azure.microsoft.com/status/)

## Changelog

### Versión 1.0.0
- Release inicial con interacción básica de agente
- Generación de reportes markdown
- Autenticación service principal
- Manejo de errores y logging
- Extracción de citaciones y fuentes