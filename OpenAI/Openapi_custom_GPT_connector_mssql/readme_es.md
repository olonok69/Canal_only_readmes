# Servidor OpenAPI MSSQL con Autenticación Bearer Token# MSSQL MCP Server con OAuth 2.0 e Integración ChatGPT



Un servidor REST listo para producción que cumple con OpenAPI 3.1 y proporciona acceso seguro de solo lectura a bases de datos Microsoft SQL Server. Este servidor implementa autenticación Bearer Token, cifrado SSL/TLS e integración perfecta con ChatGPT Actions y otras herramientas compatibles con OpenAPI.Un servidor Model Context Protocol (MCP) listo para producción que proporciona interacciones seguras con bases de datos Microsoft SQL Server potenciadas por IA. Este servidor implementa autenticación OAuth 2.0, cifrado SSL/TLS e integración perfecta tanto con Claude.ai como con ChatGPT (Deep Research).



## 🚀 Características## 🚀 Características



### **Cumplimiento OpenAPI 3.1**### **Soporte Dual**

- **API RESTful**: Endpoints HTTP estándar con especificación OpenAPI- **Integración Claude.ai**: Servidor MCP con autenticación OAuth 2.0 para Claude Desktop

- **Autenticación Bearer Token**: Autenticación simple y segura basada en tokens- **Integración ChatGPT**: Conector personalizado compatible con ChatGPT Deep Research

- **Respuestas JSON**: Todas las respuestas en formato JSON estándar- **Acceso Universal a Base de Datos**: Consulta bases de datos MSSQL mediante lenguaje natural

- **Documentación Swagger**: Especificación OpenAPI auto-generada disponible en `/docs`

### **Operaciones de Base de Datos**

### **Operaciones de Base de Datos**- **Gestión de Tablas**: Listar todas las tablas, describir estructura, obtener datos de muestra

- **Listado de Tablas**: Listar todas las tablas en la base de datos con metadatos- **Ejecución SQL**: Ejecutar queries SELECT, INSERT, UPDATE, DELETE

- **Descripción de Schema**: Obtener estructura detallada de tablas e información de columnas- **Descubrimiento de Schema**: Recuperación automática de información de tablas y columnas

- **Ejecución SQL**: Ejecutar queries SELECT de solo lectura de forma segura- **Exploración de Datos**: Recuperación de datos de muestra con límites configurables

- **Muestreo de Datos**: Recuperar datos de muestra de tablas con límites configurables- **Modo Read-Only**: Operaciones de solo lectura opcionales para seguridad en producción

- **Modo Read-Only**: Operaciones de solo lectura forzadas para seguridad en producción

### **Características de Seguridad**

### **Características de Seguridad**- **Autenticación OAuth 2.0**: Registro dinámico de clientes con flujo de authorization code

- **Autenticación Bearer Token**: Seguridad configurable basada en tokens- **Cifrado SSL/TLS**: Certificados Let's Encrypt con renovación automática

- **Protección contra SQL Injection**: Queries parametrizadas y validación de entrada- **Gestión de Tokens**: Access tokens de corta duración (expiración de 1 hora)

- **Validación de Queries**: Filtrado estricto de declaraciones no-SELECT- **Conexiones Seguras**: TLS 1.2+ con ODBC Driver 18 para SQL Server

- **Cifrado SSL/TLS**: Certificados Let's Encrypt con renovación automática- **Whitelist de Hosts**: URIs de redirect OAuth restringidos a dominios confiables

- **Soporte CORS**: Intercambio de recursos de origen cruzado configurable

### **Capa de Transporte**

### **Características de Producción**- **Server-Sent Events (SSE)**: Conexión persistente y eficiente mediante streaming

- **Containerización Docker**: Builds Docker multi-etapa con imágenes optimizadas- **Nginx Reverse Proxy**: Proxying de grado de producción con optimización SSE

- **Nginx Reverse Proxy**: Proxying de grado de producción con terminación SSL- **Monitoreo de Salud**: Endpoints de health check integrados

- **Monitoreo de Salud**: Endpoints de health check integrados- **Auto-Reconexión**: Manejo robusto de conexiones

- **Auto Escalado**: Soporte de escalado horizontal con Docker Compose

- **Logging**: Logging comprensivo de requests y errores### **Características Específicas de ChatGPT**

- **Tool Search**: Búsqueda de base de datos multipropósito (listar tablas, describir, muestrear, consultar)

## 📋 Arquitectura- **Tool Fetch**: Recuperar registros específicos por ID con caché

- **Caché de Resultados**: Caché basado en TTL para mejor rendimiento

```- **Endpoints de Discovery**: Soporte completo de discovery OAuth 2.0 y OIDC

┌─────────────┐         ┌─────────────┐         ┌──────────────┐         ┌──────────────┐

│   ChatGPT   │◄─HTTPS─►│    Nginx    │◄─HTTP──►│ Servidor API │◄─ODBC──►│  SQL Server  │## 📋 Arquitectura

│ /AI Tools   │   443   │  (SSL/TLS)  │   8009  │   OpenAPI    │         │   Database   │

└─────────────┘         └─────────────┘         └──────────────┘         └──────────────┘```

                             │┌─────────────┐         ┌─────────────┐         ┌──────────────┐         ┌──────────────┐

                             ││  Claude.ai  │◄─HTTPS─►│    Nginx    │◄─HTTP──►│  MCP Server  │◄─ODBC──►│  SQL Server  │

                        ┌────▼────┐│  /ChatGPT   │   443   │  (SSL/TLS)  │   8008  │ (OAuth 2.0)  │         │   Database   │

                        │ Certbot │└─────────────┘         └─────────────┘         └──────────────┘         └──────────────┘

                        │  Auto   │                             │

                        │ Renewal │                             │

                        └─────────┘                        ┌────▼────┐

```                        │ Certbot │

                        │  Auto   │

### Componentes                        │ Renewal │

                        └─────────┘

1. **Servidor OpenAPI** (`server_openapi.py`)```

   - Python 3.11 con framework FastAPI

   - Cumplimiento con especificación OpenAPI 3.1### Componentes

   - Autenticación Bearer token

   - Conectividad de base de datos via pyodbc1. **MCP Server** (`server_oauth.py` / `server_chatgpt.py`)

   - Python 3.11 con Starlette (ASGI)

2. **Nginx Reverse Proxy**   - Implementación del protocolo MCP

   - Terminación SSL/TLS   - Autenticación OAuth 2.0

   - Enrutamiento de requests y balanceamiento de carga   - Conectividad a base de datos vía pyodbc

   - Headers de seguridad

   - Configuración CORS2. **Nginx Reverse Proxy**

   - Terminación SSL/TLS

3. **Certbot**   - Proxying optimizado para SSE

   - Emisión automática de certificados   - Enrutamiento de requests y load balancing

   - Verificaciones de renovación cada 12 horas   - Headers de seguridad

   - Protocolo ACME (Let's Encrypt)

3. **Certbot**

## 🛠️ Instalación y Configuración   - Emisión automática de certificados

   - Verificaciones de renovación cada 12 horas

### Prerequisitos   - Protocolo ACME (Let's Encrypt)



- **Infraestructura**:## 🛠️ Instalación y Configuración

  - Docker Engine 20.10+

  - Docker Compose 2.0+### Prerrequisitos

  - Dominio público con registro DNS A

  - VM con puertos 80, 443, 8009 accesibles- **Infraestructura**:

  - Docker Engine 20.10+

- **Base de Datos**:  - Docker Compose 2.0+

  - Microsoft SQL Server 2019+  - Dominio público con registro DNS A

  - ODBC Driver 18 para SQL Server  - VM con puertos 80, 443, 8008 accesibles

  - Usuario de base de datos con permisos apropiados

- **Base de Datos**:

### 1. Configuración de Environment  - Microsoft SQL Server 2019+

  - ODBC Driver 18 para SQL Server

Crear un archivo `.env` en la raíz del proyecto:  - Usuario de base de datos con permisos apropiados



```bash### 1. Configuración de Entorno

# Configuración de Base de Datos

MSSQL_HOST=your-sql-server.database.windows.netCrear archivo `.env` en la raíz del proyecto:

MSSQL_USER=your_username

MSSQL_PASSWORD=your_secure_password```bash

MSSQL_DATABASE=your_database# Configuración de Base de Datos

MSSQL_DRIVER=ODBC Driver 18 for SQL ServerMSSQL_HOST=your-sql-server.database.windows.net

MSSQL_USER=your_username

# Configuraciones de SeguridadMSSQL_PASSWORD=your_secure_password

TrustServerCertificate=yesMSSQL_DATABASE=your_database

Trusted_Connection=noMSSQL_DRIVER=ODBC Driver 18 for SQL Server

READ_ONLY_MODE=true

# Configuración de Seguridad

# Configuración OpenAPITrustServerCertificate=yes

OPENAPI_BEARER_TOKEN=your_secure_bearer_token_hereTrusted_Connection=no

OPENAPI_SERVER_URL=https://data.forensic-bot.com/actionsREAD_ONLY_MODE=true

OPENAPI_PORT=8009

```# Configuración OAuth

ALLOWED_REDIRECT_HOSTS=chatgpt.com,openai.com,claude.ai,anthropic.com

### 2. Configuración de Certificado SSL

# Opcional: Solo Desarrollo/Pruebas

Ejecutar la configuración automatizada de Let's Encrypt:ALLOW_UNAUTH_METHODS=false

ALLOW_UNAUTH_TOOLS_CALL=false

```bash

# Hacer el script ejecutable# Configuración ChatGPT

chmod +x setup-letsencrypt.shMAX_SEARCH_RESULTS=50

CACHE_TTL_SECONDS=3600

# Ejecutar configuración```

./setup-letsencrypt.sh

### 2. Configuración de Certificado SSL

# Seguir las indicaciones:

# - Ingresar dominio: data.forensic-bot.comEjecutar la configuración automatizada de Let's Encrypt:

# - Ingresar email: your-email@example.com

# - Elegir producción (0) o staging (1)```bash

```# Hacer script ejecutable

chmod +x setup-letsencrypt.sh

El script realizará:

1. Verificar prerequisitos (Docker, Docker Compose)# Ejecutar configuración

2. Crear directorios requeridos./setup-letsencrypt.sh

3. Descargar parámetros TLS

4. Configurar Nginx# Seguir los prompts:

5. Solicitar certificado Let's Encrypt# - Ingresar dominio: data.forensic-bot.com

6. Configurar renovación automática# - Ingresar email: tu-email@example.com

# - Elegir producción (0) o staging (1)

### 3. Despliegue Docker```



#### Despliegue de ProducciónEl script realizará:

1. Verificar prerrequisitos (Docker, Docker Compose)

```bash2. Crear directorios requeridos

# Construir e iniciar todos los servicios3. Descargar parámetros TLS

docker-compose up -d4. Configurar Nginx

5. Solicitar certificado Let's Encrypt

# Ver logs6. Configurar renovación automática

docker-compose logs -f

### 3. Despliegue Docker

# Verificar salud del servicio

curl https://your-domain.com/actions/health#### Despliegue de Producción

```

```bash

#### Despliegue de Desarrollo# Construir e iniciar todos los servicios

docker-compose -f docker-compose.prod.yml up -d

```bash

# Iniciar con hot-reload# Ver logs

docker-compose up --builddocker-compose -f docker-compose.prod.yml logs -f



# Acceder localmente# Verificar salud del servicio

curl http://localhost:8009/healthcurl https://tu-dominio.com/health

``````



### 4. Verificar Instalación#### Despliegue de Desarrollo



```bash```bash

# Probar conexión HTTPS# Iniciar con hot-reload

curl https://your-domain.com/actions/healthdocker-compose up --build



# Probar schema OpenAPI# Acceso local

curl https://your-domain.com/actions/openapi.jsoncurl http://localhost:8008/health

```

# Probar con autenticación

curl -H "Authorization: Bearer your_token" \### 4. Verificar Instalación

     https://your-domain.com/actions/list_tables

``````bash

# Probar conexión HTTPS

## 🔧 Guías de Integracióncurl https://tu-dominio.com/health



### Integración con ChatGPT Actions# Probar discovery OAuth

curl https://tu-dominio.com/.well-known/oauth-authorization-server

1. **Crear Action Personalizada** en ChatGPT:

   - Ir a ChatGPT → Configure → Create Action# Probar capacidad SSE (requiere autenticación)

   - Nombre: `Acceso Base de Datos MSSQL`curl -I https://tu-dominio.com/sse

   - Descripción: `Consultar base de datos SQL Server con acceso de solo lectura````



2. **Importar Schema OpenAPI**:## 🔧 Guías de Integración

   ```

   URL del Schema: https://your-domain.com/actions/openapi.json### Integración Claude.ai

   ```

1. **Registrar Tu Servidor**:

3. **Configurar Autenticación**:   ```json

   - Tipo: `Bearer Token`   POST https://tu-dominio.com/register

   - Token: `your_secure_bearer_token_here`   {

     "client_name": "Claude Desktop",

4. **Probar Conexión**:     "redirect_uris": ["https://claude.ai/api/mcp/auth_callback"]

   - Usar la función de prueba en ChatGPT Actions   }

   - Probar el endpoint `/list_tables`   ```



5. **Ejemplo de Uso en ChatGPT**:2. **Configurar Claude Desktop** (`claude_desktop_config.json`):

   ```   ```json

   Usuario: "Muéstrame todas las tablas en la base de datos"   {

   ChatGPT llamará: GET /actions/list_tables     "mcpServers": {

          "mssql": {

   Usuario: "Describe la estructura de la tabla Users"         "url": "https://tu-dominio.com/sse",

   ChatGPT llamará: GET /actions/describe_table?table_name=Users         "oauth": {

              "authorization_url": "https://tu-dominio.com/authorize",

   Usuario: "Obtén datos de muestra de la tabla Orders"           "token_url": "https://tu-dominio.com/token",

   ChatGPT llamará: GET /actions/get_table_sample?table_name=Orders&limit=10           "client_id": "tu_client_id",

   ```           "client_secret": "tu_client_secret"

         }

### Otras Herramientas Compatibles con OpenAPI       }

     }

El servidor funciona con cualquier herramienta que soporte especificaciones OpenAPI 3.1:   }

   ```

- **Postman**: Importar la especificación OpenAPI

- **Insomnia**: Cargar el archivo de schema3. **Autenticar**: Claude Desktop manejará el flujo OAuth automáticamente

- **Swagger UI**: Disponible en `https://your-domain.com/actions/docs`

- **Aplicaciones Personalizadas**: Usar la especificación OpenAPI para generar SDKs de cliente### Integración ChatGPT (Deep Research)



## 📚 Referencia API1. **Agregar Conector Personalizado** en Configuración de ChatGPT:

   - Nombre: `MSSQL Database`

### URL Base   - Tipo: `Custom Connector`

```   - URL: `https://tu-dominio.com/chatgpt/sse`

https://your-domain.com/actions

```2. **Discovery URL**: `https://tu-dominio.com/chatgpt/.well-known/oauth-authorization-server`



### Autenticación3. **Configuración OAuth**: ChatGPT autodescubre desde endpoints well-known

Todos los endpoints requieren autenticación Bearer token:

```4. **Autorizar**: Seguir el flujo OAuth de ChatGPT

Authorization: Bearer your_secure_bearer_token_here

```5. **Usar con Deep Research**:

   ```

### Endpoints   Query: "Buscar en la base de datos los 10 mejores clientes por ingresos"

   ChatGPT:

#### 1. Health Check   1. Llamará al tool search para ejecutar query

```http   2. Procesará resultados

GET /health   3. Llamará al tool fetch para registros detallados si es necesario

```   ```

**Descripción**: Verificar salud y estado del servidor

**Autenticación**: No requerida## 📚 Referencia de API

**Respuesta**:

```json### Endpoints OAuth

{

  "status": "ok",| Endpoint | Método | Propósito |

  "mode": "read-only",|----------|--------|-----------|

  "database": "your_database"| `/.well-known/oauth-authorization-server` | GET | Discovery OAuth AS |

}| `/.well-known/openid-configuration` | GET | Discovery OIDC (alias) |

```| `/.well-known/oauth-protected-resource` | GET | Discovery OAuth RS |

| `/register` | POST | Registro dinámico de cliente |

#### 2. Listar Tablas| `/authorize` | GET | Grant de authorization code |

```http| `/token` | POST | Intercambio de token |

GET /list_tables

```### Endpoints MCP

**Descripción**: Listar todas las tablas en la base de datos

**Autenticación**: Requerida| Endpoint | Método | Propósito | Autenticación |

**Respuesta**:|----------|--------|---------|----------------|

```json| `/sse` | HEAD | Verificación de capacidad SSE | Opcional |

{| `/sse` | POST | Manejo de mensajes MCP | Requerida (Bearer token) |

  "total_tables": 15,| `/health` | GET | Estado de salud del servidor | Ninguna |

  "tables": [

    {### Endpoints ChatGPT

      "schema": "dbo",

      "table_name": "Users",| Endpoint | Método | Propósito |

      "full_name": "Users",|----------|--------|---------|

      "type": "BASE TABLE"| `/chatgpt/sse` | POST | Endpoint SSE ChatGPT |

    }| `/chatgpt/.well-known/*` | GET | Endpoints de discovery |

  ]

}## 🔨 Tools Disponibles

```

### Tools Claude.ai

#### 3. Describir Tabla

```http#### 1. list_tables

GET /describe_table?table_name={table_name}```json

```{

**Descripción**: Obtener estructura detallada de tabla y metadatos  "name": "list_tables",

**Autenticación**: Requerida  "description": "Listar todas las tablas en la base de datos",

**Parámetros**:  "inputSchema": {

- `table_name` (requerido): Nombre de la tabla a describir    "type": "object",

    "properties": {},

**Respuesta**:    "required": []

```json  }

{}

  "table_name": "[dbo].[Users]",```

  "row_count": 1500,

  "total_columns": 8,#### 2. describe_table

  "columns": [```json

    {{

      "column_name": "id",  "name": "describe_table",

      "data_type": "int",  "description": "Obtener estructura y metadatos de tabla",

      "nullable": false,  "inputSchema": {

      "max_length": null,    "type": "object",

      "precision": 10,    "properties": {

      "scale": 0,      "table_name": {

      "default_value": null        "type": "string",

    }        "description": "Nombre de la tabla"

  ]      }

}    },

```    "required": ["table_name"]

  }

#### 4. Ejecutar SQL}

```http```

POST /execute_sql

```#### 3. execute_sql

**Descripción**: Ejecutar un query SELECT de solo lectura```json

**Autenticación**: Requerida{

**Cuerpo del Request**:  "name": "execute_sql",

```json  "description": "Ejecutar query SQL (solo SELECT en modo read-only)",

{  "inputSchema": {

  "query": "SELECT TOP 10 * FROM Users WHERE active = 1"    "type": "object",

}    "properties": {

```      "query": {

**Respuesta**:        "type": "string",

```json        "description": "Query SQL a ejecutar"

{      }

  "columns": ["id", "name", "email", "active"],    },

  "rows": [    "required": ["query"]

    [1, "John Doe", "john@example.com", true],  }

    [2, "Jane Smith", "jane@example.com", true]}

  ],```

  "row_count": 2

}#### 4. get_table_sample

``````json

{

#### 5. Obtener Muestra de Tabla  "name": "get_table_sample",

```http  "description": "Obtener datos de muestra de una tabla",

GET /get_table_sample?table_name={table_name}&limit={limit}  "inputSchema": {

```    "type": "object",

**Descripción**: Obtener datos de muestra de una tabla    "properties": {

**Autenticación**: Requerida      "table_name": {

**Parámetros**:        "type": "string",

- `table_name` (requerido): Nombre de la tabla        "description": "Nombre de la tabla"

- `limit` (opcional): Número de filas a retornar (default: 5, máx: 1000)      },

      "limit": {

**Respuesta**:        "type": "integer",

```json        "description": "Número de filas a retornar",

{        "default": 10

  "table_name": "[dbo].[Users]",      }

  "limit": 5,    },

  "columns": ["id", "name", "email", "active"],    "required": ["table_name"]

  "rows": [  }

    [1, "John Doe", "john@example.com", true],}

    [2, "Jane Smith", "jane@example.com", true]```

  ]

}### Tools ChatGPT

```

#### 1. search

### Especificación OpenAPITool de búsqueda de base de datos multipropósito que maneja:

- Listar tablas: `"list tables"`

La especificación completa OpenAPI 3.1 está disponible en:- Describir tabla: `"describe Customers"`

```- Datos de muestra: `"sample Orders limit 10"`

https://your-domain.com/actions/openapi.json- Queries SQL: `"SELECT TOP 5 * FROM Products WHERE Price > 100"`

```

```json

Documentación interactiva (Swagger UI) está disponible en:{

```  "name": "search",

https://your-domain.com/actions/docs  "description": "Buscar base de datos: listar tablas, describir schema, datos de muestra o ejecutar queries",

```  "parameters": {

    "query": {

## 🔒 Seguridad      "type": "string",

      "description": "Query en lenguaje natural o statement SQL"

### Autenticación    }

  }

El servidor usa autenticación Bearer Token para todos los endpoints protegidos:}

```

```http

Authorization: Bearer your_secure_bearer_token_here#### 2. fetch

```Recuperar registros específicos por ID (de resultados de búsqueda):



### Validación de Queries SQL```json

{

El servidor implementa validación estricta para asegurar operaciones de solo lectura:  "name": "fetch",

  "description": "Obtener un registro específico por su ID de resultados de búsqueda previos",

1. **Operaciones Permitidas**:  "parameters": {

   - Declaraciones `SELECT`    "id": {

   - Expresiones de tabla común `WITH` (CTEs)      "type": "string",

   - Queries contra vistas `INFORMATION_SCHEMA`      "description": "ID de registro de resultados de búsqueda"

    }

2. **Operaciones Bloqueadas**:  }

   - `INSERT`, `UPDATE`, `DELETE`, `MERGE`}

   - `CREATE`, `ALTER`, `DROP`, `TRUNCATE````

   - `EXEC`, `EXECUTE` (procedimientos almacenados)

   - `GRANT`, `REVOKE` (permisos)## 🔒 Seguridad

   - `BEGIN TRANSACTION`, `COMMIT`, `ROLLBACK`

   - Múltiples declaraciones (separadas por punto y coma)### Flujo de Autenticación



3. **Sanitización de Entrada**:```mermaid

   - Nombres de tabla validados contra patrones segurossequenceDiagram

   - Queries parametrizadas para todas las operaciones de base de datos    participant Client as Cliente AI (Claude/ChatGPT)

   - Protección SQL injection via pyodbc    participant Server as MCP Server

    participant DB as SQL Server

### Seguridad de Red    

    Client->>Server: POST /register

#### Configuración Nginx    Server-->>Client: {client_id, client_secret}

El servidor está protegido por Nginx con las siguientes características de seguridad:    

    Client->>Server: GET /authorize?client_id=...

```nginx    Server-->>Client: Redirect con code

# Headers de seguridad    

add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;    Client->>Server: POST /token (code, client_id, client_secret)

add_header X-Content-Type-Options nosniff;    Server-->>Client: {access_token, expires_in: 3600}

add_header X-Frame-Options DENY;    

add_header X-XSS-Protection "1; mode=block" always;    Client->>Server: POST /sse (Authorization: Bearer token)

add_header Referrer-Policy "strict-origin-when-cross-origin" always;    Server->>Server: Validar token

    Server-->>Client: Conexión SSE establecida

# Configuración CORS    

add_header Access-Control-Allow-Origin * always;    Client->>Server: MCP: initialize

add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS' always;    Server-->>Client: initialized

add_header Access-Control-Allow-Headers 'Authorization, Content-Type, Accept' always;    

```    Client->>Server: MCP: tools/call (execute_sql)

    Server->>DB: Ejecutar query

#### Seguridad de Base de Datos    DB-->>Server: Resultados

- **TLS 1.2+**: Conexiones cifradas a SQL Server    Server-->>Client: Resultados serializados

- **Modo Read-Only**: Forzado a nivel de aplicación```

- **Menor Privilegio**: Usuario de base de datos con permisos mínimos requeridos

- **Connection Pooling**: Gestión eficiente de recursos### Seguridad de Red



## 📊 Monitoreo y Mantenimiento#### Reglas de Firewall GCP (Ejemplo)

```bash

### Health Checks# Tráfico HTTPS

gcloud compute firewall-rules create allow-mcp-https \

```bash    --allow tcp:443 \

# Salud del servidor    --source-ranges 0.0.0.0/0 \

curl https://your-domain.com/actions/health    --target-tags mcp-server



# Respuesta esperada:# HTTP (solo Let's Encrypt)

{gcloud compute firewall-rules create allow-letsencrypt \

  "status": "ok",    --allow tcp:80 \

  "mode": "read-only",    --source-ranges 0.0.0.0/0 \

  "database": "your_database"    --target-tags mcp-server

}

```# SSH (gestión)

gcloud compute firewall-rules create allow-ssh \

### Gestión de Contenedores Docker    --allow tcp:22 \

    --source-ranges TU_IP/32 \

```bash    --target-tags mcp-server

# Ver todos los servicios```

docker-compose ps

### Seguridad de Aplicación

# Ver logs

docker-compose logs -f mcp-server-openapi- **OAuth 2.0**: Autorización compatible con RFC 6749

- **Expiración de Tokens**: Access tokens de 1 hora

# Reiniciar servidor OpenAPI- **Generación Segura**: `secrets.token_urlsafe()` para tokens

docker-compose restart mcp-server-openapi- **Whitelist de Hosts**: URIs de redirect restringidos

- **Modo Read-Only**: Operaciones de solo lectura opcionales en base de datos

# Escalar servicios- **Queries Parametrizadas**: Protección contra inyección SQL vía pyodbc

docker-compose up -d --scale mcp-server-openapi=3- **TLS 1.2+**: Solo cipher suites modernos

```

### Headers de Seguridad (Nginx)

### Gestión de Certificados

```nginx

```bashadd_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# Verificar expiración de certificadoadd_header X-Content-Type-Options nosniff;

echo | openssl s_client -servername your-domain.com -connect your-domain.com:443 2>/dev/null | openssl x509 -noout -datesadd_header X-Frame-Options DENY;

add_header X-XSS-Protection "1; mode=block";

# Probar renovación (dry run)add_header Referrer-Policy "strict-origin-when-cross-origin";

docker-compose exec certbot certbot renew --dry-run```



# Forzar renovación## 📊 Monitoreo y Mantenimiento

docker-compose exec certbot certbot renew --force-renewal

```### Health Checks



### Monitoreo de Performance```bash

# Salud del servidor

```bashcurl https://tu-dominio.com/health

# Uso de recursos del contenedor

docker stats mcp-server-openapi# Respuesta esperada:

{

# Prueba de conexión a base de datos  "status": "healthy",

docker exec mcp-server-openapi python -c "  "transport": "sse",

from server_openapi import _get_db_config  "oauth": "enabled",

config, conn_str = _get_db_config()  "database": "tu_database",

print(f'Conectado a: {config[\"database\"]}')"  "mcp_version": "2025-06-18",

  "read_only": true

# Prueba de tiempo de respuesta API}

time curl -H "Authorization: Bearer your_token" \```

     https://your-domain.com/actions/list_tables

```### Logging



## 🐛 Resolución de Problemas```bash

# Ver todos los logs

### Problemas Comunesdocker-compose logs -f



#### 1. Autenticación Fallida (401 Unauthorized)# Logs del servidor MCP

```bashdocker-compose logs -f mcp-server-http

# Verificar si el token está configurado correctamente

curl -H "Authorization: Bearer wrong_token" \# Logs de Nginx

     https://your-domain.com/actions/list_tablesdocker-compose logs -f nginx



# Verificar token en environment# Filtrar por nivel

docker exec mcp-server-openapi env | grep OPENAPI_BEARER_TOKENdocker-compose logs -f | grep ERROR

``````



#### 2. Falla de Conexión a Base de Datos### Gestión de Certificados

```bash

# Probar conectividad de base de datos```bash

docker exec mcp-server-openapi python -c "# Verificar expiración de certificado

from server_openapi import _get_db_config, _db_cursorecho | openssl s_client -servername tu-dominio.com -connect tu-dominio.com:443 2>/dev/null | openssl x509 -noout -dates

try:

    with _db_cursor() as cursor:# Probar renovación (dry run)

        cursor.execute('SELECT 1')docker-compose exec certbot certbot renew --dry-run

        print('Conexión a base de datos exitosa')

except Exception as e:# Forzar renovación

    print(f'Falla de conexión a base de datos: {e}')docker-compose exec certbot certbot renew --force-renewal

"

# Ver certificados

# Verificar variables de environmentdocker-compose exec certbot certbot certificates

docker exec mcp-server-openapi env | grep MSSQL```

```

### Monitoreo de Rendimiento

#### 3. Problemas de Certificado

```bash```bash

# Verificar validez del certificado# Estadísticas de contenedores

openssl s_client -connect your-domain.com:443 -servername your-domain.comdocker stats



# Verificar resolución DNS# Conexiones Nginx

nslookup your-domain.comdocker exec nginx cat /var/log/nginx/access.log | tail -100



# Verificar logs de certbot# Prueba de conexión a base de datos

docker-compose logs certbotdocker exec mcp-server-http python -c "

```from server_oauth import get_db_config

config, conn_str = get_db_config()

#### 4. Problemas de Schema OpenAPIprint(f'Conectado a: {config[\"database\"]}')"

```bash```

# Validar especificación OpenAPI

curl https://your-domain.com/actions/openapi.json | jq .## 🐛 Solución de Problemas



# Verificar si Swagger UI carga### Problemas Comunes

curl -I https://your-domain.com/actions/docs

```#### 1. Validación de Certificado Falló

```bash

### Modo Debug# Verificar certificado

openssl s_client -connect tu-dominio.com:443 -servername tu-dominio.com

Habilitar logging detallado configurando variables de environment:

# Verificar DNS

```bashnslookup tu-dominio.com

# En archivo .env

LOG_LEVEL=DEBUG# Verificar logs de certbot

docker-compose logs certbot

# O modificar código del servidor temporalmente```

```

#### 2. Token OAuth Inválido

Para debugging en producción:```bash

```bash# Verificar expiración de token

# Ver logs en tiempo real# Los tokens expiran después de 1 hora

docker-compose logs -f mcp-server-openapi

# Re-registrar cliente

# Filtrar logs de errorcurl -X POST https://tu-dominio.com/register \

docker-compose logs mcp-server-openapi | grep ERROR  -H "Content-Type: application/json" \

  -d '{"client_name": "test"}'

# Verificar logs de acceso de Nginx```

docker-compose logs nginx | grep "POST /actions"

```#### 3. Conexión a Base de Datos Falló

```bash

## 📖 Documentación# Probar driver ODBC

docker exec mcp-server-http odbcinst -j

### Estructura del Proyecto

```# Verificar variables de entorno

.docker exec mcp-server-http env | grep MSSQL

├── server_openapi.py            # Servidor FastAPI OpenAPI

├── Dockerfile.openapi           # Imagen Docker del servidor OpenAPI# Probar conexión

├── docker-compose.yml           # Compose de producción con OpenAPIdocker exec mcp-server-http python -c "

├── setup-letsencrypt.sh         # Script de configuración SSLimport pyodbc

├── requirements.txt             # Dependencias Pythonconn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=tu-servidor;...')

├── .env                         # Variables de environmentprint('Éxito')

├── nginx/"

│   ├── nginx.conf              # Configuración principal Nginx```

│   └── conf.d/

│       └── default.conf        # Configuración del sitio con proxy /actions#### 4. Problemas de Conexión SSE

├── certbot/```bash

│   ├── conf/                   # Certificados SSL# Probar endpoint SSE (con token)

│   └── www/                    # ACME challengecurl -N -H "Authorization: Bearer TU_TOKEN" \

├── logs/  -H "Accept: text/event-stream" \

│   └── nginx/                  # Logs de acceso/error de Nginx  https://tu-dominio.com/sse

└── README.md                   # Este archivo

```# Verificar configuración SSE de Nginx

docker exec nginx cat /etc/nginx/conf.d/default.conf | grep -A 10 "location /sse"

### Archivos de Configuración```



#### Configuración Docker Compose### Modo Debug

El `docker-compose.yml` incluye el servicio del servidor OpenAPI:

Habilitar logging detallado en `.env`:

```yaml```bash

services:LOG_LEVEL=DEBUG

  mcp-server-openapi:```

    build:

      context: .O modificar el código del servidor:

      dockerfile: Dockerfile.openapi```python

    container_name: mcp-server-openapi# En server_oauth.py o server_chatgpt.py

    expose:logging.basicConfig(

      - "8009"    level=logging.DEBUG,

    environment:    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'

      - MSSQL_HOST=${MSSQL_HOST})

      - MSSQL_USER=${MSSQL_USER}```

      - MSSQL_PASSWORD=${MSSQL_PASSWORD}

      - MSSQL_DATABASE=${MSSQL_DATABASE}## 📖 Documentación

      - OPENAPI_BEARER_TOKEN=${OPENAPI_BEARER_TOKEN}

      - OPENAPI_SERVER_URL=${OPENAPI_SERVER_URL}### Estructura del Proyecto

      - READ_ONLY_MODE=${READ_ONLY_MODE:-true}```

    healthcheck:.

      test: ["CMD", "curl", "-f", "http://localhost:8009/health"]├── server_oauth.py              # Servidor MCP para Claude.ai

      interval: 30s├── server_chatgpt.py            # Servidor compatible con ChatGPT

      timeout: 10s├── Dockerfile                   # Imagen servidor HTTP

      retries: 3├── Dockerfile.https             # Imagen servidor HTTPS

    networks:├── Dockerfile.chatgpt           # Imagen servidor ChatGPT

      - mcp-network├── docker-compose.yml           # Compose desarrollo

    restart: unless-stopped├── docker-compose.prod.yml      # Compose producción

```├── setup-letsencrypt.sh         # Script configuración SSL

├── requirements.txt             # Dependencias Python

#### Configuración Nginx├── .env                         # Variables de entorno

La ubicación `/actions` en Nginx proxifica al servidor OpenAPI:├── nginx/

│   ├── nginx.conf              # Configuración principal Nginx

```nginx│   └── conf.d/

location /actions/ {│       └── default.conf        # Configuración del sitio

    proxy_pass http://mcp-server-openapi:8009/;├── certbot/

    proxy_http_version 1.1;│   ├── conf/                   # Certificados SSL

    proxy_set_header Host $host;│   └── www/                    # Desafío ACME

    proxy_set_header X-Real-IP $remote_addr;├── docs/

    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;│   ├── chatgpt-connector-setup.md

    proxy_set_header X-Forwarded-Proto https;│   ├── security.md

    proxy_set_header Authorization $http_authorization;│   ├── explanation_en.md

│   ├── explicacion_es.md

    add_header Access-Control-Allow-Origin * always;│   └── read_only.md

    add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS' always;└── README.md                    # Este archivo

    add_header Access-Control-Allow-Headers 'Authorization, Content-Type, Accept' always;```

}

```### Documentación Relacionada



### Variables de Environment- [Guía de Configuración del Conector ChatGPT](docs/chatgpt-connector-setup.md)

- [Mejores Prácticas de Seguridad](docs/security.md)

| Variable | Descripción | Default | Requerido |- [Explicación Técnica (English)](docs/explanation_en.md)

|----------|-------------|---------|-----------|- [Explicación Técnica (Español)](docs/explicacion_es.md)

| `MSSQL_HOST` | Hostname de SQL Server | `localhost` | Sí |- [Guía Modo Read-Only](docs/read_only.md)

| `MSSQL_USER` | Usuario de base de datos | - | Sí |

| `MSSQL_PASSWORD` | Contraseña de base de datos | - | Sí |### Recursos Externos

| `MSSQL_DATABASE` | Nombre de base de datos | - | Sí |

| `MSSQL_DRIVER` | Driver ODBC | `ODBC Driver 18 for SQL Server` | No |- [Especificación Model Context Protocol](https://spec.modelcontextprotocol.io)

| `TrustServerCertificate` | Confiar en cert del servidor | `yes` | No |- [OAuth 2.0 RFC 6749](https://tools.ietf.org/html/rfc6749)

| `Trusted_Connection` | Usar conexión confiable | `no` | No |- [Documentación Let's Encrypt](https://letsencrypt.org/docs/)

| `READ_ONLY_MODE` | Habilitar modo solo lectura | `true` | No |- [Guía Nginx SSE](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)

| `OPENAPI_BEARER_TOKEN` | Bearer token para auth | - | No |

| `OPENAPI_SERVER_URL` | URL del servidor para spec OpenAPI | `https://data.forensic-bot.com/actions` | No |## 🔄 Flujo de Despliegue

| `OPENAPI_PORT` | Puerto interno | `8009` | No |

### Despliegue Inicial

## 🧪 Testing```bash

1. Clonar repositorio

### Testing API con curl2. Configurar archivo .env

3. Ejecutar setup-letsencrypt.sh

```bash4. Iniciar servicios: docker-compose -f docker-compose.prod.yml up -d

# Probar endpoint de health (sin auth requerida)5. Verificar salud: curl https://tu-dominio.com/health

curl https://your-domain.com/actions/health6. Configurar clientes AI (Claude/ChatGPT)

```

# Probar endpoints autenticados

TOKEN="your_bearer_token_here"### Actualizaciones

```bash

# Listar tablas# Obtener últimos cambios

curl -H "Authorization: Bearer $TOKEN" \git pull

     https://your-domain.com/actions/list_tables

# Reconstruir contenedores

# Describir tabladocker-compose -f docker-compose.prod.yml build

curl -H "Authorization: Bearer $TOKEN" \

     "https://your-domain.com/actions/describe_table?table_name=Users"# Reiniciar servicios (cero downtime)

docker-compose -f docker-compose.prod.yml up -d

# Obtener muestra de tabla

curl -H "Authorization: Bearer $TOKEN" \# Verificar

     "https://your-domain.com/actions/get_table_sample?table_name=Users&limit=5"curl https://tu-dominio.com/health

```

# Ejecutar SQL

curl -X POST \### Rollback

     -H "Authorization: Bearer $TOKEN" \```bash

     -H "Content-Type: application/json" \# Detener servicios

     -d '{"query": "SELECT TOP 5 * FROM Users"}' \docker-compose -f docker-compose.prod.yml down

     https://your-domain.com/actions/execute_sql

```# Checkout versión anterior

git checkout <commit-anterior>

### Testing con Postman

# Reconstruir y reiniciar

1. Importar especificación OpenAPI: `https://your-domain.com/actions/openapi.json`docker-compose -f docker-compose.prod.yml up --build -d

2. Configurar autenticación Bearer Token```

3. Probar todos los endpoints

## 🧪 Testing

### Load Testing

### Tests Unitarios

```bash```bash

# Usando Apache Bench# Ejecutar pytest

ab -n 1000 -c 10 -H "Authorization: Bearer TOKEN" \pytest tests/

   https://your-domain.com/actions/list_tables

# Con cobertura

# Usando heypytest --cov=server_oauth --cov=server_chatgpt tests/

hey -n 1000 -c 10 -H "Authorization: Bearer TOKEN" \```

    https://your-domain.com/actions/list_tables

```### Tests de Integración

```bash

## 🔄 Flujo de Despliegue# Probar flujo OAuth

python tests/test_oauth_flow.py

### Despliegue Inicial

```bash# Probar conectividad base de datos

1. Clonar repositoriopython tests/test_database.py

2. Configurar archivo .env con configuraciones de base de datos y token

3. Ejecutar setup-letsencrypt.sh para certificados SSL# Probar protocolo MCP

4. Iniciar servicios: docker-compose up -dpython tests/test_mcp.py

5. Verificar salud: curl https://your-domain.com/actions/health```

6. Configurar ChatGPT Actions u otros clientes

```### Load Testing

```bash

### Actualizaciones# Usando Apache Bench

```bashab -n 1000 -c 10 -H "Authorization: Bearer TOKEN" \

# Obtener últimos cambios  https://tu-dominio.com/sse

git pull

# Usando hey

# Reconstruir contenedor OpenAPIhey -n 1000 -c 10 -H "Authorization: Bearer TOKEN" \

docker-compose build mcp-server-openapi  https://tu-dominio.com/sse

```

# Reiniciar servicios (sin tiempo de inactividad)

docker-compose up -d

## 📝 Licencia

# Verificar

curl https://your-domain.com/actions/healthLicencia MIT - Ver archivo LICENSE para detalles

```

## 📧 Soporte

### Rollback

```bashPara problemas y preguntas:

# Detener servicios- GitHub Issues: [repository-url]

docker-compose down- Email: support@tu-dominio.com

- Documentación: https://tu-dominio.com/docs

# Checkout versión anterior

git checkout <previous-commit>## 🔗 Links Útiles



# Reconstruir y reiniciar- [Soporte Anthropic - Custom Connectors](https://support.anthropic.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp)

docker-compose up --build -d- [Netify AI - Claude Application](https://www.netify.ai/resources/applications/claude)

```- [Let's Encrypt](https://letsencrypt.org/)

- [Nginx](https://nginx.org/)

## 📝 Licencia- [Certbot](https://certbot.eff.org/)



Licencia MIT - Ver archivo LICENSE para detalles---



## 📧 Soporte**Versión**: 2.0.0  

**Última Actualización**: Octubre 2025  

Para problemas y preguntas:**Protocolo**: MCP 2025-06-18  

- GitHub Issues: [repository-url]**Compatibilidad**: SQL Server 2019+, Python 3.11+, Docker 20.10+  

- Email: support@your-domain.com**Plataformas**: Claude.ai, ChatGPT (Deep Research)  

- Documentación: https://your-domain.com/actions/docs**Transport**: Server-Sent Events (SSE)  

**Autenticación**: OAuth 2.0 (Authorization Code Flow)  

---**Cifrado**: TLS 1.2+ con Let's Encrypt

**Versión**: 2.0.0  
**Última Actualización**: Octubre 2025  
**Versión OpenAPI**: 3.1.0  
**Compatibilidad**: SQL Server 2019+, Python 3.11+, Docker 20.10+  
**Framework**: FastAPI con uvicorn  
**Autenticación**: Bearer Token  
**Cifrado**: TLS 1.2+ con Let's Encrypt