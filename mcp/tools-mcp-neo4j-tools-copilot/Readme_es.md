# Generador de Reportes Neo4j

Una aplicación integral de línea de comandos que se conecta a Neo4j y genera reportes analíticos detallados sobre visitantes de eventos, patrones de asistencia a sesiones y comportamiento de visitantes recurrentes. La aplicación soporta múltiples tipos de eventos y conferencias comerciales.

## Características

### Análisis Integral
- **Estadísticas de Visitantes**: Conteo total de visitantes y análisis demográfico detallado
- **Seguimiento de Visitantes Recurrentes**: Análisis avanzado de visitantes que asistieron a eventos asociados en años anteriores
- **Análisis de Popularidad de Sesiones**: Top 5 de sesiones más concurridas del año anterior por visitantes recurrentes
- **Portfolio de Sesiones**: Desglose completo de sesiones del año actual con detalles de programación
- **Inteligencia Cross-Event**: Análisis del movimiento de visitantes entre eventos asociados

### Tipos de Eventos Soportados
- **Eventos Tipo A**: Conferencias y ferias comerciales de asociaciones profesionales
- **Eventos Tipo B**: Ferias comerciales de tecnología y comercio digital

### Capacidades de Reportes
- Reportes profesionales en formato Markdown con timestamps
- Resúmenes ejecutivos con indicadores clave de rendimiento
- Análisis detallado de retención de visitantes y métricas de lealtad
- Información de programación de sesiones y venues
- Insights estratégicos y recomendaciones basadas en datos

## Requisitos

- **Python**: 3.8+ (recomendado 3.9+)
- **Neo4j**: Base de datos con datos de eventos/conferencias estructurados apropiadamente
- **Dependencies**: Ver `requirements.txt` para versiones exactas
  - `neo4j==5.28.2`: Neo4j Python driver
  - `python-dotenv==1.1.1`: Gestión de environment variables

## Instalación

### Configuración Rápida
1. **Clonar el repositorio**:
   ```bash
   git clone <repository-url>
   cd neo4j-show-report-generator
   ```

2. **Crear virtual environment** (recomendado):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar environment variables** (ver sección de Configuración)

## Configuración

### Configuración de Environment Variables

Crear un archivo `.env` en el directorio raíz del proyecto con las credenciales de Neo4j:

```bash
# Configuración de Conexión Neo4j
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-actual-password
NEO4J_DATABASE=neo4j
```

#### Notas de Seguridad
- El archivo `.env` se excluye automáticamente de commits git via `.gitignore`
- Nunca hacer commit de credenciales al control de versiones
- Usar passwords fuertes y únicos para environments de producción

### Alternativa: Environment Variables Directas

Si prefieres no usar un archivo `.env`, establecer environment variables directamente:

#### Windows PowerShell:
```powershell
$env:NEO4J_URI="neo4j+s://your-instance.databases.neo4j.io"
$env:NEO4J_USERNAME="neo4j"
$env:NEO4J_PASSWORD="your-password"
$env:NEO4J_DATABASE="neo4j"
```

#### Linux/Mac:
```bash
export NEO4J_URI="neo4j+s://your-instance.databases.neo4j.io"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password"
export NEO4J_DATABASE="neo4j"
```

## Uso

### Opción 1: Usando el Script Launcher (Recomendado)
```bash
# Hacer el script ejecutable (Linux/Mac)
chmod +x run_report.sh

# Ejecutar la aplicación
./run_report.sh
```

### Opción 2: Ejecución Directa con Python
```bash
# Activar virtual environment (si se usa)
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Ejecutar la aplicación
python show_report_generator.py
```

### Opción 3: Ejecución Manual
```bash
python3 show_report_generator.py
```

## Cómo Funciona la Aplicación

### Resumen del Workflow
1. **Conexión a Base de Datos**: Establece conexión segura a Neo4j usando credenciales del environment
2. **Descubrimiento de Eventos**: Detecta automáticamente eventos disponibles en la base de datos
3. **Interacción con Usuario**: Presenta eventos disponibles y solicita selección
4. **Recolección de Datos**: Ejecuta queries Cypher optimizados para recopilar análisis integral
5. **Generación de Reporte**: Crea reporte profesional en Markdown con insights
6. **Output de Archivo**: Guarda archivo de reporte con timestamp y muestra resultados en terminal

### Experiencia Interactiva
```bash
Generador de Reportes Neo4j
==================================================
Conectado exitosamente a la base de datos Neo4j
Eventos disponibles:
  1. Evento A (event_a)
  2. Evento B (event_b)

Ingrese nombre del evento (elija entre: event_a, event_b): event_a
Procesando datos para event_a...
Generando reporte para evento: event_a
Reporte guardado en: event_a_report_20250810_143022.md
```

## Secciones del Reporte y Análisis

### Dashboard de Métricas Clave
- **Total de Visitantes**: Conteo de asistencia del año actual
- **Visitantes Recurrentes**: Análisis cross-year de visitantes
- **Tasa de Retorno**: Cálculo porcentual de lealtad de visitantes
- **Movimiento Cross-Event**: Análisis entre diferentes tipos de eventos

### Análisis Avanzado de Visitantes
- **Sección a**: Demografía detallada de visitantes del año actual
- **Sección b**: Análisis integral de visitantes que asistieron tanto al evento actual como del año anterior
- **Insights de Retención**: Análisis profundo de patrones de lealtad de audiencia

### Inteligencia de Sesiones
- **Top 5 de Sesiones**: Sesiones más populares del año anterior entre visitantes recurrentes
- **Performance de Sesiones**: Métricas de asistencia con atribución de evento
- **Popularidad de Contenido**: Análisis de temas de sesiones y engagement

### Portfolio de Sesiones del Año Actual
- **Catálogo Completo de Sesiones**: Desglose completo de la programación del año actual
- **Detalles de Programación**: Información de fecha, hora y venue
- **Seguimiento de Sponsorship**: Identificación de sesiones patrocinadas y atribución de sponsors
- **Distribución de Teatros**: Análisis de utilización de venues

### Insights Estratégicos y Recomendaciones
- **Análisis de Retención de Audiencia**: Insights basados en datos sobre lealtad de visitantes
- **Oportunidades Cross-Event**: Recomendaciones para engagement de audiencia entre eventos
- **Estrategia de Contenido**: Insights de performance de sesiones para programación futura
- **Inteligencia de Marketing**: Patrones de comportamiento de audiencia para campañas dirigidas

## Ejemplo de Output de Reporte

### Ejemplo de Resumen Ejecutivo
```markdown
# Reporte de Evento A

**Generado el:** 2025-08-10 14:30:22

## Resumen Ejecutivo
Este reporte proporciona análisis integral del evento A, incluyendo 
estadísticas de visitantes, patrones de visitantes recurrentes e información de sesiones.

## Estadísticas de Visitantes Este Año
**Total de Visitantes:** 1,874

## Análisis de Visitantes Recurrentes
- **Mismo Evento (A) Año Pasado:** 420 visitantes
- **Evento Asociado (B) Año Pasado:** 132 visitantes  
- **Total de Visitantes Recurrentes:** 552 visitantes
- **Tasa de Visitantes Recurrentes:** 29.5%
```

### Convención de Nomenclatura de Archivos
Los reportes se guardan automáticamente con timestamps descriptivos:
```
{nombre_evento}_report_{YYYYMMDD_HHMMSS}.md
```
Ejemplos:
- `event_a_report_20250810_143022.md`
- `event_b_report_20250810_143022.md`

## Requisitos del Schema de Base de Datos

La aplicación espera una base de datos Neo4j bien estructurada con los siguientes componentes:

### Tipos de Nodos y Labels
- **`Visitor_this_year`**: Asistentes a eventos del año actual
- **`Visitor_last_year_type_a`**: Asistentes del año anterior a eventos tipo A
- **`Visitor_last_year_type_b`**: Asistentes del año anterior a eventos tipo B
- **`Sessions_this_year`**: Catálogo de sesiones del año actual
- **`Sessions_past_year`**: Archivo de sesiones del año anterior

### Propiedades Esenciales de Nodos
#### Nodos de Visitante:
- `show`: Identificador de evento (ej. "event_a", "event_b")
- `BadgeId`: Identificador único de visitante
- `Email`: Información de contacto para linking de visitantes

#### Nodos de Sesión:
- `title`: Nombre/título de sesión
- `show`: Identificador de evento asociado
- `date`: Fecha de sesión
- `start_time` / `end_time`: Timing de sesión
- `theatre__name`: Información de venue/sala
- `sponsored_session`: Flag de sponsorship
- `sponsored_by`: Organización sponsor

### Relaciones Críticas
- **`Same_Visitor`**: Vincula visitantes del año actual con sus registros del año anterior
- **`attended_session`**: Conecta visitantes con sesiones a las que asistieron

### Requisitos de Calidad de Datos
- Todas las queries incluyen filtrado apropiado de valores null con `WHERE field IS NOT NULL`
- Validación de non-null para campos críticos (nombres de eventos, títulos de sesiones, IDs de visitantes)
- Convención de nomenclatura consistente para identificadores de eventos

## Testing y Aseguramiento de Calidad

### Suite de Testing Integral

La aplicación incluye tanto unit tests como integration tests opcionales para asegurar confiabilidad y precisión de datos.

#### Unit Tests
Unit tests integrales con interacciones Neo4j mockeadas:
```bash
# Ejecutar todos los unit tests usando el script test runner
./run_tests.sh

# O ejecutar directamente con Python
python test_show_report_generator.py
```

**Áreas de Cobertura de Testing:**
- Manejo de conexión a base de datos y escenarios de error
- Validación de environment variables y configuración
- Métodos de retrieval de datos con varias condiciones de datos
- Lógica de generación de reportes y formateo markdown
- Operaciones de file I/O y manejo de errores
- Validación de input de usuario y edge cases
- Workflow de función main y manejo de excepciones

#### Integration Tests (Opcionales)
Tests de conectividad real a base de datos para validación de producción:
```bash
# Habilitar y ejecutar integration tests (requiere acceso real a Neo4j)
RUN_INTEGRATION_TESTS=true python test_integration.py
```

**Nota**: Los integration tests requieren credenciales válidas de Neo4j y están deshabilitados por defecto para prevenir acceso accidental a base de datos de producción.

### Configuración de Test Environment
```bash
# Activar virtual environment
source .venv/bin/activate

# Instalar test dependencies (incluidas en requirements.txt)
pip install -r requirements.txt

# Ejecutar suite de testing
./run_tests.sh
```

## Manejo de Errores y Troubleshooting

### Gestión Integral de Errores
La aplicación incluye manejo robusto de errores para escenarios comunes:

#### Problemas de Conexión a Base de Datos
- **Timeouts de conexión**: Retry automático con mensajes de error informativos
- **Fallas de autenticación**: Feedback claro de validación de credenciales
- **Conectividad de red**: Manejo graceful de disrupciones de conexión

#### Problemas de Configuración
- **Environment variables faltantes**: Guía detallada sobre configuraciones requeridas
- **Credenciales inválidas**: Mensajería de error segura sin exponer datos sensibles
- **Permisos de acceso a base de datos**: Indicación clara de problemas de control de acceso

#### Problemas de Calidad de Datos
- **Nombres de eventos inválidos**: Validación user-friendly con opciones disponibles
- **Nodos de base de datos faltantes**: Manejo graceful de datos incompletos
- **Errores de ejecución de query**: Reporte detallado de errores para debugging

#### Operaciones de Archivo
- **Limitaciones de espacio en disco**: Verificación proactiva antes de generación de reporte
- **Problemas de permisos de archivo**: Mensajes de error claros para problemas de acceso
- **Creación de directorios**: Manejo automático de directorios faltantes

### Pasos Comunes de Troubleshooting

1. **Verificar Environment Variables**:
   ```bash
   # Verificar si las variables están establecidas
   echo $NEO4J_URI
   echo $NEO4J_USERNAME
   # Nota: Nunca hacer echo del password en producción
   ```

2. **Probar Conexión a Base de Datos**:
   ```bash
   # Usar Neo4j browser o cypher-shell para verificar conectividad
   cypher-shell -a $NEO4J_URI -u $NEO4J_USERNAME
   ```

3. **Validar Schema de Base de Datos**:
   ```cypher
   # Verificar tipos de nodos requeridos
   MATCH (n) RETURN DISTINCT labels(n) as node_types
   
   # Verificar tipos de relaciones
   MATCH ()-[r]->() RETURN DISTINCT type(r) as relationships
   ```

4. **Verificar Disponibilidad de Datos**:
   ```cypher
   # Verificar que existen datos de eventos
   MATCH (v:Visitor_this_year) 
   RETURN DISTINCT v.show as available_events
   ```

## Estructura del Proyecto

```
neo4j-show-report-generator/
├── show_report_generator.py    # Aplicación principal con clase ShowReportGenerator
├── requirements.txt            # Dependencies de Python (neo4j, python-dotenv)
├── .env                       # Configuración de environment (crear desde template)
├── .gitignore                 # Exclusiones de Git (incluye .env y archivos de reporte)
│
├── run_report.sh              # Script launcher de aplicación (Linux/Mac)
├── run_tests.sh               # Script de ejecución de tests
│
├── test_show_report_generator.py  # Suite integral de unit tests
├── test_integration.py           # Integration tests opcionales
├── TEST_INFO.md                  # Documentación y guidelines de testing
│
├── README.md                     # Esta documentación integral
├── README_APP.md                 # Detalles específicos de aplicación
├── LICENSE                       # Información de licencia
│
├── examples/                     # Ejemplos de configuración
│   ├── mcp.json.adoc            # Ejemplo de configuración MCP
│   └── mcp-no-env.json.adoc     # Configuración MCP alternativa
│
└── *_report_*.md                # Reportes generados (ignorados por git)
    ├── event_a_report_20250808_100155.md
    └── event_b_report_20250810_143022.md
```

## Dependencies y Requisitos

### Dependencies Principales
- **`neo4j==5.28.2`**: Driver oficial de Python para Neo4j para conectividad a base de datos
- **`python-dotenv==1.1.1`**: Gestión de environment variables desde archivos `.env`

### Requisitos de Sistema
- **Python**: 3.8+ (probado con 3.9, 3.10, 3.11)
- **Sistema Operativo**: Cross-platform (Windows, macOS, Linux)
- **Memoria**: Mínimo 512MB RAM (recomendado 1GB+ para datasets grandes)
- **Red**: Acceso HTTPS a base de datos Neo4j (puerto 7687 para protocolo Bolt)

### Requisitos de Neo4j
- **Versión**: Neo4j 4.0+ (probado con 4.4, 5.x)
- **Autenticación**: Username/password o autenticación enterprise
- **Protocolos**: Soporta conexiones Bolt, Bolt+TLS, Neo4j+S
- **Permisos**: Acceso de lectura a nodos de visitantes y sesiones

## Consideraciones de Seguridad

### Gestión de Credenciales
- **Environment Variables**: Datos sensibles almacenados en archivos `.env` (excluidos de git)
- **Sin Credenciales Hardcoded**: Todos los datos de autenticación externalizados
- **Protocolos Seguros**: Encriptación TLS para conexiones a base de datos (URLs `neo4j+s://`)

### Privacidad de Datos
- **Reportes Generados**: Pueden contener información sensible de visitantes de negocio
- **Archivos de Reporte**: Automáticamente excluidos del control de versiones via `.gitignore`
- **Retención de Datos**: Considerar políticas de retención de archivos de reporte locales

### Seguridad de Red
- **Encriptación de Conexión**: Usa TLS/SSL para comunicación con base de datos
- **Consideraciones de Firewall**: Asegurar que puertos de Neo4j (7687, 7474) sean accesibles
- **Autenticación**: Soporta mecanismos de autenticación enterprise

## Consideraciones de Performance

### Optimización de Queries
- **Propiedades Indexadas**: Asegurar que la propiedad `show` esté indexada en nodos de visitantes
- **Indexado de Relaciones**: Indexar relaciones `Same_Visitor` y `attended_session`
- **Uso de Memoria**: Datasets grandes pueden requerir tuning de memoria de Neo4j

### Recomendaciones de Escalado
- **Para Datasets Grandes (>10K visitantes)**:
  - Considerar batching de queries para result sets muy grandes
  - Monitorear uso de heap memory de Neo4j
  - Implementar connection pooling para múltiples ejecuciones concurrentes

- **Performance de Base de Datos**:
  ```cypher
  # Índices recomendados para performance óptimo
  CREATE INDEX visitor_show_index FOR (v:Visitor_this_year) ON (v.show)
  CREATE INDEX session_show_index FOR (s:Sessions_this_year) ON (s.show)
  ```

## Desarrollo y Contribución

### Configuración de Desarrollo
```bash
# 1. Clonar repositorio
git clone <repository-url>
cd neo4j-show-report-generator

# 2. Crear virtual environment
python3 -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows

# 3. Instalar development dependencies
pip install -r requirements.txt

# 4. Configurar environment
cp .env.example .env  # Editar con sus credenciales

# 5. Ejecutar tests
./run_tests.sh
```

### Guidelines de Contribución
1. **Calidad de Código**: Seguir guidelines de estilo Python PEP 8
2. **Testing**: Todas las nuevas features deben incluir unit tests integrales
3. **Documentación**: Actualizar README.md para cualquier cambio user-facing
4. **Validación de Base de Datos**: Probar todas las queries Cypher contra datos reales antes de implementación
5. **Manejo de Errores**: Incluir manejo apropiado de excepciones y mensajes de error user-friendly

### Mejores Prácticas de Estructura de Código
- **Filtrado de Null**: Siempre incluir `WHERE field IS NOT NULL` en queries Cypher
- **Type Hints**: Usar Python type hints para mejor documentación de código
- **Mensajes de Error**: Proporcionar mensajes de error claros y accionables para usuarios
- **Cleanup de Recursos**: Asegurar cleanup apropiado de conexiones del driver Neo4j

## Licencia y Soporte

### Licencia
Este proyecto está licenciado bajo los términos especificados en el archivo `LICENSE`. Por favor revisar términos de licencia antes de uso comercial.

### Recursos de Soporte
Para problemas, preguntas o requests de features:

1. **Verificar Documentación**: Revisar este README y documentación inline del código
2. **Validar Environment**: Asegurar que todas las environment variables estén configuradas correctamente
3. **Probar Acceso a Base de Datos**: Verificar conectividad Neo4j y que el schema requerido exista
4. **Revisar Suite de Testing**: Ejecutar unit tests para identificar problemas de configuración
5. **Verificar Dependencies**: Asegurar que todos los packages requeridos estén instalados con versiones correctas

### Guidelines de Comunidad
- **Reportes de Bugs**: Incluir mensajes de error completos, detalles de environment y pasos de reproducción
- **Requests de Features**: Proporcionar casos de uso claros y comportamiento esperado
- **Problemas de Performance**: Incluir tamaño de dataset y tiempos de ejecución de queries

---

*Generador de Reportes Neo4j - Análisis profesional de conferencias y ferias comerciales powered by tecnología de graph database.*