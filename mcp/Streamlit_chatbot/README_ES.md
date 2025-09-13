# Plataforma de Integración IA para CRM y Base de Datos de Grafos

Una aplicación integral full-stack que proporciona interacciones impulsadas por IA con bases de datos de grafos Neo4j, sistemas CRM HubSpot y datos de Yahoo Finance a través de servidores del Protocolo de Contexto de Modelo (MCP). Esta plataforma permite análisis, gestión y automatización perfectos a través de tu infraestructura de base de datos, CRM y datos financieros con autenticación de grado empresarial y seguridad.

## 🚀 Visión General del Sistema

Esta aplicación consiste en cuatro componentes integrados trabajando juntos a través del Protocolo de Contexto de Modelo (MCP):

1. **Cliente Streamlit** - Interfaz de chat IA segura con autenticación empresarial y soporte multi-proveedor
2. **Servidor MCP Yahoo Finance** - Análisis de datos financieros con algoritmos propietarios e indicadores técnicos
3. **Servidor MCP Neo4j** - Operaciones de base de datos de grafos vía consultas Cypher con validación de esquema
4. **Servidor MCP HubSpot** - Integración CRM completa con 25+ herramientas y operaciones CRUD completas

### Diagrama de Arquitectura

![Arquitectura del Sistema](image_es.png)

## ⚡ Inicio Rápido

### Prerrequisitos
- Docker & Docker Compose
- Base de datos Neo4j (con plugin APOC)
- Token de Acceso de App Privada HubSpot
- Clave API OpenAI o configuración Azure OpenAI

### 1. Configuración de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# Configuración OpenAI (elegir una)
OPENAI_API_KEY=tu_clave_api_openai_aqui

# O Configuración Azure OpenAI
AZURE_API_KEY=tu_clave_azure
AZURE_ENDPOINT=https://tu-endpoint.openai.azure.com/
AZURE_DEPLOYMENT=tu_nombre_deployment
AZURE_API_VERSION=2023-12-01-preview

# Configuración Neo4j
NEO4J_URI=bolt://host.docker.internal:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=tu_contraseña_neo4j
NEO4J_DATABASE=neo4j

# Configuración HubSpot
PRIVATE_APP_ACCESS_TOKEN=tu_token_app_privada_hubspot

# Opcional: Habilitar SSL para cliente
SSL_ENABLED=false
```

### 2. Generar Autenticación de Usuario

```bash
# Generar credenciales de autenticación
cd client
python simple_generate_password.py

# Esto crea usuarios por defecto:
# admin: very_Secure_p@ssword_123!
# juan: fl09877@
# pepe_romero: MrRok0934@#mero2024!
# demo_user: strong_password_123!
```

### 3. Lanzar la Plataforma

```bash
# Construir e iniciar todos los servicios
docker-compose up --build

# O iniciar servicios individuales
docker-compose up mcpserver3  # Servidor MCP Yahoo Finance
docker-compose up mcpserver4  # Servidor MCP Neo4j
docker-compose up mcpserver5  # Servidor MCP HubSpot  
docker-compose up hostclient  # Cliente Streamlit
```

### 4. Acceder a la Aplicación

- **Interfaz Principal**: http://localhost:8501
- **Interfaz HTTPS** (si está habilitada): https://localhost:8502
- **Salud Servidor Yahoo Finance**: http://localhost:8002/health
- **Salud Servidor Neo4j**: http://localhost:8003/health
- **Salud Servidor HubSpot**: http://localhost:8004/health

## 🎯 Características Clave

### **Autenticación Empresarial y Seguridad**
- **Sistema de Autenticación de Usuario**: Inicio de sesión seguro con hash de contraseñas bcrypt
- **Gestión de Sesiones**: Sesiones de usuario persistentes con expiración configurable
- **Acceso Basado en Roles**: Dominios de email pre-autorizados y gestión de usuarios
- **Soporte SSL**: HTTPS opcional con certificados auto-firmados
- **Cookies Seguras**: Cookies de autenticación configurables con claves personalizadas

### **Interacciones IA Avanzadas**
- **Soporte IA Multi-Proveedor**: OpenAI y Azure OpenAI con cambio dinámico
- **Consultas en Lenguaje Natural**: Interfaz conversacional para operaciones complejas
- **Selección Inteligente de Herramientas**: Enrutamiento automático a servidores MCP apropiados
- **Memoria de Conversación**: Conversaciones conscientes del contexto con gestión de historial
- **Operaciones Conscientes del Esquema**: Validación automática contra esquemas de base de datos y CRM

### **Análisis Integral de Datos Financieros**
- **Datos de Acciones en Tiempo Real**: Acceso a precios actuales de mercado e información de trading sin costos de API
- **Análisis Técnico Avanzado**: MACD, Bandas de Bollinger, Canales Donchian con puntuación propietaria
- **Algoritmos de Trading Personalizados**: Puntuación de indicador combinado para decisiones de inversión (escala -100 a +100)
- **Análisis de Portafolio**: Análisis multi-timeframe con generación de señales de trading
- **Integración Fibonacci**: Implementación de estrategia avanzada Bollinger-Fibonacci

### **Operaciones Completas de Base de Datos de Grafos**
- **Descubrimiento de Esquema**: Análisis automático de estructura Neo4j con integración APOC
- **Validación de Consultas**: Validación de consultas Cypher consciente del esquema antes de ejecución
- **Operaciones Lectura/Escritura**: Consultas MATCH seguras y modificaciones de datos controladas
- **Prevención de Errores**: Valida consultas contra estructura real de base de datos
- **Resultados Visuales**: Presentación de datos estructurada con mapeo de relaciones

### **Integración CRM HubSpot Completa (25 Herramientas)**
- **Operaciones CRUD Completas**: Crear, leer, actualizar, eliminar a través de todos los tipos de objeto
- **Gestión Avanzada de Objetos**: Contactos, empresas, ofertas, tickets, objetos personalizados
- **Gestión de Asociaciones**: Enlazar y gestionar relaciones entre objetos CRM
- **Gestión de Propiedades**: Crear y gestionar campos personalizados y estructuras de datos
- **Seguimiento de Compromisos**: Notas, tareas y logging de actividad con ciclo de vida completo
- **Integración de Flujos de Trabajo**: Acceso a insights de automatización y gestión de flujos de trabajo
- **Integración UI**: Generar enlaces directos a interfaz HubSpot para flujo de trabajo perfecto
- **Operaciones Batch**: Manejo eficiente de datos masivos para operaciones a gran escala

### **Excelencia Técnica**
- **Interfaz Moderna con Pestañas**: UI intuitiva con pestañas de Configuración, Conexiones, Herramientas y Chat
- **Contenedorización Docker**: Despliegue y escalado listo para producción
- **Comunicación en Tiempo Real**: Server-Sent Events (SSE) para comunicación MCP responsiva
- **Validación Integral**: Validación de esquema a través de todas las herramientas y operaciones
- **Manejo Robusto de Errores**: Gestión detallada de errores con capacidades de depuración
- **Monitoreo de Salud**: Verificaciones de salud integradas y monitoreo del sistema

## 💻 Stack Tecnológico

### **Frontend y Cliente**
```yaml
Tecnología: Streamlit 1.44+
Lenguaje: Python 3.11+
Autenticación: Streamlit Authenticator 0.3.2
Seguridad: bcrypt, soporte SSL/TLS
Framework UI: CSS personalizado, diseño responsivo
```

### **Servicios Backend**
```yaml
Servidor Yahoo Finance:
  - FastAPI + uvicorn
  - Python 3.12+
  - librería yfinance
  - Algoritmos personalizados

Servidor Neo4j:
  - FastAPI + uvicorn  
  - Python 3.11+
  - neo4j-driver
  - Procedimientos APOC

Servidor HubSpot:
  - Express.js + Node.js 18+
  - JavaScript ES6+
  - 25 herramientas especializadas
  - Validación Zod
```

### **Infraestructura**
```yaml
Contenedorización: Docker + Docker Compose
Protocolo: Protocolo de Contexto de Modelo (MCP)
Transporte: Server-Sent Events (SSE)
Base de Datos: Neo4j 5.0+ con APOC
APIs Externas: Yahoo Finance, API REST HubSpot
```

### **IA y ML**
```yaml
Framework: LangChain + LangGraph
Proveedores: OpenAI GPT-4o, Azure OpenAI
Agente: ReAct (Razonamiento + Actuación)
Contexto: Memoria de conversación + historial de herramientas
```

## 📚 Ejemplos de Uso

### **Autenticación y Primeros Pasos**

```
# Iniciar sesión con credenciales por defecto:
# Usa las tuyas propias
admin: very_Secure_p@ssword_123!
juan: fl09877@
pepe_romero: MrRok0934@#mero2024!
demo_user: strong_password_123!
```

### **Flujos de Trabajo de Análisis Financiero**

```
"¿Cuál es la puntuación MACD actual para AAPL con parámetros personalizados?"
"Calcula una estrategia Bollinger-Fibonacci integral para las acciones de Tesla"
"Dame una puntuación de análisis técnico combinado para Microsoft durante 6 meses"
"Muéstrame análisis de canales Donchian con evaluación de volatilidad para el S&P 500"
"Compara señales de trading para AAPL, TSLA y MSFT usando múltiples indicadores"
```

### **Flujos de Trabajo de Análisis de Base de Datos**

```
"Muéstrame el esquema completo de la base de datos y explica las relaciones de datos"
"¿Cuántos visitantes se convirtieron en clientes este año, y cuál es el path de conversión?"
"Encuentra todas las conexiones entre nodos de persona y nodos de empresa con detalles de relación"
"Crea un nuevo nodo de persona con propiedades y enlázalo a una empresa existente"
"Valida esta consulta Cypher contra el esquema actual antes de ejecución"
```

### **Flujos de Trabajo de Gestión CRM**

```
"Obtén mis detalles de usuario HubSpot y muéstrame todos los contactos creados este mes"
"Crea una nueva empresa llamada Tech Solutions con información de contacto completa"
"Lista todas las ofertas abiertas por encima de $10,000 y sus contactos asociados"
"Crea una tarea de seguimiento para la oferta de Amazon y genera un enlace HubSpot para verla"
"Busca todos los contactos en la industria tecnológica y exporta sus detalles"
"Asocia Juan García con Acme Corp y agrega una nota sobre su reunión reciente"
```

### **Flujos de Trabajo de Integración Avanzada**

```
"Analiza el rendimiento de acciones AAPL usando múltiples indicadores técnicos, luego crea una tarea HubSpot para revisar nuestras inversiones tecnológicas basadas en el análisis"
"Compara datos de clientes entre nuestra base de datos de grafos Neo4j y CRM HubSpot para identificar inconsistencias de datos"
"Encuentra ofertas de alto valor en HubSpot, haz referencia cruzada con relaciones de base de datos de grafos, y genera un reporte de inversión integral"
"Crea un análisis completo de journey del cliente combinando relaciones de base de datos de grafos, historial de compromiso CRM y datos de rendimiento de mercado"
```

## 📊 Rendimiento y Escalado

### **Métricas de Rendimiento**

```yaml
Tiempos de Respuesta:
  - Autenticación: <200ms
  - Descubrimiento de Herramientas: <500ms
  - Consultas Simples: <2s
  - Análisis Complejos: <10s

Throughput:
  - Usuarios Concurrentes: 50+ (instancia única)
  - Ejecuciones de Herramientas: 100+ por minuto
  - Procesamiento de Datos: 10MB+ por consulta
```

### **Estrategias de Escalado**

#### **Escalado Horizontal**
```yaml
Balanceador de Carga: Múltiples instancias de cliente
Servidores MCP: Escalado independiente por servicio
Base de Datos: Clustering Neo4j
Caché: Redis para almacenamiento de sesión
```

#### **Escalado Vertical**
```yaml
Memoria: 2GB+ por contenedor
CPU: 2+ cores recomendados
Almacenamiento: SSD para rendimiento Neo4j
Red: 1Gbps+ para datasets grandes
```

## 🔧 Documentación de Componentes

Cada componente tiene documentación detallada para configuración avanzada y desarrollo:

### [🏠 Documentación Cliente Streamlit](./client/Readme_es.md)
- **Autenticación Empresarial**: Gestión segura de usuarios con cifrado bcrypt
- **Configuración IA Multi-Proveedor**: OpenAI y Azure OpenAI con cambio dinámico
- **Interfaz Moderna con Pestañas**: Organización de Configuración, Conexiones, Herramientas y Chat
- **Soporte SSL**: HTTPS opcional con generación de certificados
- **Gestión de Sesiones**: Conversaciones persistentes con aislamiento de usuario

### [📈 Documentación Servidor MCP Yahoo Finance](./servers/server3/Readme_es.md)
- **6 Herramientas Financieras Avanzadas**: Puntuación MACD, canales Donchian, estrategias Bollinger-Fibonacci
- **Algoritmos Propietarios**: Sistemas de puntuación personalizados con componentes ponderados
- **Cálculos de Indicadores Técnicos**: Datos de mercado en tiempo real sin costos de API
- **Generación de Señales de Trading**: Recomendaciones automatizadas comprar/vender/mantener
- **Análisis de Portafolio**: Análisis multi-timeframe y multi-indicador

### [🗄️ Documentación Servidor MCP Neo4j](./servers/server4/Readme_es.md)
- **Enfoque Schema-First**: Descubrimiento obligatorio de esquema antes de operaciones
- **Validación de Consultas**: Previene errores validando contra estructura real de base de datos
- **Integración APOC**: Procedimientos avanzados para análisis integral de esquema
- **Operaciones Seguras**: Operaciones separadas de lectura y escritura con validación
- **Gestión de Conexiones**: Manejo robusto de conexiones asíncronas

### [🏢 Documentación Servidor MCP HubSpot](./servers/server5/Readme_es.md)
- **25 Herramientas Completas**: Cobertura completa de capacidades API HubSpot
- **Gestión Avanzada de Objetos**: Todos los tipos de objeto CRM con operaciones CRUD
- **Gestión de Asociaciones**: Mapeo completo de relaciones y gestión
- **Gestión de Propiedades**: Gestión de campos personalizados y estructura de datos
- **Integración de Flujos de Trabajo**: Insights de automatización y acceso a flujos de trabajo
- **Integración UI**: Enlaces directos a interfaz HubSpot para flujo de trabajo perfecto

Para uso integral de herramientas, ver la [Guía de Implementación de Herramientas HubSpot](./servers/server5/HUBSPOT_TOOLS_GUIDE.md).

## 🛠️ Desarrollo y Personalización

### **Gestión de Usuarios**

```bash
# Agregar nuevos usuarios editando simple_generate_password.py
cd client
nano simple_generate_password.py  # Agregar usuarios al diccionario users
python simple_generate_password.py  # Generar nueva configuración
```

### **Configuración de Proveedor IA**

```python
# Agregar nuevos proveedores IA en client/config.py
MODEL_OPTIONS = {
    'OpenAI': 'gpt-4o',
    'Azure OpenAI': 'o3-mini',
    'Proveedor Personalizado': 'tu-modelo'
}
```

### **Configuración de Servidor MCP**

```json
// Actualizar client/servers_config.json para endpoints de servidor
{
  "mcpServers": {
    "Servidor Personalizado": {
      "transport": "sse",
      "url": "http://tu-servidor:puerto/sse",
      "timeout": 600
    }
  }
}
```

### **Agregar Herramientas Personalizadas**

1. **Herramientas Yahoo Finance**: Extender análisis financiero con indicadores personalizados
2. **Herramientas Neo4j**: Agregar operaciones especializadas de análisis de grafos
3. **Herramientas HubSpot**: Implementar integraciones CRM adicionales
4. **Herramientas Cliente**: Integrar nuevos servicios vía protocolo MCP

## 🔒 Seguridad y Mejores Prácticas

### **Seguridad de Autenticación**
- **Cifrado de Grado Empresarial**: Hash de contraseñas bcrypt con salt
- **Seguridad de Sesión**: Expiración de sesión configurable y cookies seguras
- **Control de Acceso**: Dominios de email pre-autorizados y acceso basado en roles
- **Soporte SSL/TLS**: HTTPS opcional con generación de certificados

### **Protección de Datos**
- **Validación de Entrada**: Validación integral a través de todos los componentes
- **Validación de Esquema**: Validación de operaciones de base de datos y CRM
- **Mensajes de Error Sanitizados**: Manejo seguro de errores sin exposición de datos
- **Protección de Claves API**: Gestión de credenciales basada en variables de entorno

### **Seguridad de Red**
- **Despliegue Contenerizado**: Arquitectura de servicios aislados
- **Mapeo de Puertos Configurable**: Configuración de red flexible
- **Endpoints de Verificación de Salud**: Monitoreo sin exponer datos sensibles
- **Limitación de Tasa**: Protección integrada contra abuso

## 📊 Monitoreo y Depuración

### **Verificaciones de Salud y Estado del Sistema**
- **Sistema General**: Estado de autenticación e indicadores de conexión
- **Servidor Yahoo Finance**: http://localhost:8002/health
- **Servidor Neo4j**: http://localhost:8003/health (incluye conectividad de base de datos)
- **Servidor HubSpot**: http://localhost:8004/health (incluye validación de token API)

### **Herramientas de Depuración Avanzadas**
- **Historial de Ejecución de Herramientas**: Logs de ejecución detallados en secciones UI expandibles
- **Seguimiento de Sesión de Usuario**: Tiempo de inicio de sesión, monitoreo de actividad y datos de sesión
- **Memoria de Conversación**: Depuración consciente del contexto con análisis de conversación
- **Logs de Autenticación**: Seguimiento integral de inicio de sesión y acceso

### **Monitoreo de Rendimiento**
- **Timing de Ejecución de Consultas**: Seguimiento de tiempo de respuesta de base de datos y API
- **Analíticas de Uso de Herramientas**: Monitorear herramientas más usadas y patrones de ejecución
- **Uso de Recursos**: Rendimiento de contenedor Docker y utilización de memoria
- **Actualización de Datos Financieros**: Frecuencias de actualización de datos de mercado y caché

## 🚀 Opciones de Despliegue

### **Despliegue de Desarrollo**
```bash
# Inicio rápido para desarrollo
docker-compose up --build
```

### **Despliegue de Producción**
```bash
# Habilitar SSL para producción
echo "SSL_ENABLED=true" >> .env

# Usar contraseñas de grado producción
cd client && python simple_generate_password.py

# Desplegar con proxy reverso
# Configurar nginx/traefik para terminación SSL
# Implementar gestión apropiada de secretos
# Configurar monitoreo y alertas
```

### **Escalado Empresarial**
- **Escalado Horizontal**: Múltiples instancias de servidor MCP con balanceador de carga
- **Pooling de Conexión de Base de Datos**: Gestión optimizada de conexiones Neo4j
- **Clustering de Sesión**: Gestión de sesión multi-instancia
- **Integración de Monitoreo**: Métricas compatibles con Prometheus/Grafana

## 🐛 Solución de Problemas

### **Problemas de Autenticación**
- **Fallos de Inicio de Sesión**: Verificar que `keys/config.yaml` existe y credenciales coinciden
- **Problemas de Sesión**: Limpiar cookies del navegador y reiniciar aplicación
- **Errores de Permisos**: Verificar dominios de email en lista pre-autorizada

### **Problemas de Conexión**
- **Problemas de Servidor MCP**: Verificar que todos los servicios estén ejecutándose con `docker-compose ps`
- **Conectividad de Red**: Verificar configuración de red Docker
- **Autenticación API**: Validar claves API y permisos de token HubSpot

### **Problemas de Ejecución de Herramientas**
- **Validación de Esquema**: Siempre llamar `get_neo4j_schema` antes de operaciones de base de datos
- **Operaciones HubSpot**: Comenzar con `hubspot-get-user-details` para contexto
- **Fallos de Consulta**: Verificar historial de ejecución de herramientas para mensajes de error detallados

### **Problemas de Rendimiento**
- **Respuestas Lentas**: Monitorear timing de ejecución de herramientas en paneles de depuración
- **Uso de Memoria**: Verificar utilización de recursos de contenedor Docker
- **Límites de Tasa API**: Monitorear uso de API HubSpot y datos financieros

## 📄 Documentación Técnica

Para información técnica detallada y presentaciones:

### [📋 Visión General Técnica (Inglés)](./technical_en.md)
Presentación técnica completa cubriendo:
- Análisis profundo de arquitectura
- Análisis de componentes
- Consideraciones de rendimiento
- Implementación de seguridad
- Estrategias de despliegue

### [📋 Presentación Técnica (Español)](./technical_es.md)
Presentación técnica completa que cubre:
- Análisis profundo de arquitectura
- Análisis de componentes
- Consideraciones de rendimiento
- Implementación de seguridad
- Estrategias de despliegue

## 🤝 Contribuir

### **Flujo de Trabajo de Desarrollo**
1. **Pruebas de Autenticación**: Verificar funcionalidad de inicio/cierre de sesión
2. **Integración de Herramientas**: Probar todas las conexiones de servidor MCP y disponibilidad de herramientas
3. **Revisión de Seguridad**: Validar sanitización de entrada y controles de acceso
4. **Pruebas de Rendimiento**: Monitorear tiempos de respuesta y uso de recursos

### **Estándares de Código**
- **Python**: Cumplimiento PEP 8 con type hints integrales
- **JavaScript**: Estándares ES6+ con validación de esquema Zod
- **Docker**: Mejores prácticas de seguridad con usuarios no-root
- **Autenticación**: Manejo seguro de credenciales y gestión de sesión

## 🔗 Recursos Adicionales

- [Documentación del Protocolo de Contexto de Modelo](https://modelcontextprotocol.io/)
- [Documentación de API Yahoo Finance](https://pypi.org/project/yfinance/)
- [Documentación Neo4j](https://neo4j.com/docs/) con [Procedimientos APOC](https://neo4j.com/docs/apoc/)
- [Documentación de API HubSpot](https://developers.hubspot.com/docs/api/overview)
- [Documentación Streamlit](https://docs.streamlit.io/)
- [Documentación Streamlit Authenticator](https://github.com/mkhorasani/Streamlit-Authenticator)
- [Documentación Docker Compose](https://docs.docker.com/compose/)

---

**Versión**: 2.0.0  
**Última Actualización**: Junio 2025  
**Autenticación**: Streamlit Authenticator 0.3.2 con cifrado bcrypt  
**Compatibilidad**: Docker 20+, Python 3.11+, Node.js 18+, Neo4j 5.0+  
**Seguridad**: Autenticación de grado empresarial con soporte SSL/TLS