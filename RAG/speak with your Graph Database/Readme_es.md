# Conversando con tu Base de Datos de Grafos - Sistema RAG LangChain Neo4j

## Descripción General

Este proyecto implementa un sistema de Retrieval-Augmented Generation (RAG) que permite la interacción en lenguaje natural con bases de datos de grafos Neo4j utilizando LangChain. El sistema combina búsquedas de similitud vectorial con consultas de bases de datos de grafos para proporcionar respuestas inteligentes sobre estructuras de datos complejas e interconectadas.

El notebook demuestra tres técnicas principales para interactuar con bases de datos de grafos:
1. **Búsqueda de similitud vectorial** utilizando las capacidades vectoriales de Neo4j
2. **Consultas directas de grafos** con queries Cypher
3. **Traducción de lenguaje natural a Cypher** utilizando LLMs

## Tecnologías Clave

### Integración LangChain Neo4j
- **Neo4jGraph**: Un wrapper para el driver Python de Neo4j que simplifica las operaciones de base de datos
- **Neo4jVector**: Implementación de vector store que soporta embeddings, búsquedas de similitud y retrieval híbrido
- **GraphCypherQAChain**: Interfaz de lenguaje natural que traduce preguntas a queries Cypher

### Model Context Protocol (MCP)
El proyecto hace referencia al Model Context Protocol de Anthropic, una forma estandarizada de proporcionar contexto para LLMs, permitiendo integración fluida entre aplicaciones y modelos de lenguaje.

## Componentes de Arquitectura

### 1. Operaciones de Vector Store (Neo4jVector)

La integración Neo4jVector proporciona funcionalidad completa de base de datos vectorial:

```python
db = Neo4jVector.from_documents(
    docs, embeddings, url=uri, username=username, password=password
)
```

**Capacidades:**
- Crear embeddings vectoriales a partir de documentos LangChain
- Realizar búsquedas de similitud con scoring
- Ejecutar búsquedas híbridas combinando vectores y queries de grafos
- Aplicar filtrado de metadata
- Construir instancias vectoriales a partir de datos de grafos existentes

### 2. Interfaz de Base de Datos de Grafos (Neo4jGraph)

Interacción directa con la base de datos Neo4j utilizando queries Cypher:

```python
graph = Neo4jGraph(url=uri, username=username, password=password)
result = graph.query(cypher_query, params=parameters)
```

Esto permite traversals complejos de grafos y consultas basadas en relaciones que aprovechan todo el poder de las capacidades de grafos de Neo4j.

### 3. Interfaz de Consulta en Lenguaje Natural (GraphCypherQAChain)

El componente más sofisticado traduce preguntas en lenguaje natural a queries Cypher:

```python
chain = GraphCypherQAChain.from_llm(
    llm, graph=graph, verbose=True,
    allow_dangerous_requests=True,
    return_intermediate_steps=True
)
```

**Flujo del Proceso:**
1. El usuario envía una pregunta en lenguaje natural
2. El LLM analiza el schema del grafo y la pregunta
3. El LLM genera el query Cypher apropiado
4. El query se ejecuta contra la base de datos Neo4j
5. Los resultados son procesados por el LLM para generar una respuesta en lenguaje natural

## Modelo de Datos

El sistema trabaja con un dataset de conferencias veterinarias que contiene:

- **Visitors_this_year**: Asistentes del año actual con títulos de trabajo, roles y especializaciones
- **Visitor_last_year_lva/bva**: Asistentes del año anterior de diferentes shows
- **Sessions_this_year/past_year**: Sesiones de conferencias con clasificaciones de stream
- **Streams**: Categorías de materias (ej., "nursing", "Equine", "Small Animal")

**Relaciones Clave:**
- `Same_Visitor`: Conecta asistentes a través de años
- `attended_session`: Conecta visitantes con sesiones
- `Has_stream`: Asocia sesiones con streams de materias
- `job_to_stream`: Mapea roles de trabajo con streams relevantes

## Detalles de Implementación

### Configuración del Entorno

```python
# Dependencias requeridas
pip install langchain langchain-community langchain-neo4j
pip install langchain-openai tiktoken
pip install neo4j
```

### Configuración

El sistema utiliza variables de entorno para el manejo seguro de credenciales:

```python
from dotenv import load_dotenv, dotenv_values
config = dotenv_values(".env")

# Configuración del LLM OpenAI
llm = ChatOpenAI(
    model="gpt-4.1",
    openai_api_key=config["OPENAI_API_KEY"],
    temperature=0,
    max_tokens=8192
)

# Conexión Neo4j
uri = "bolt://127.0.0.1:7687"
username = "neo4j"
password = ""  # Configurar en variables de entorno
```

### Procesamiento de Documentos

Los documentos de texto se procesan utilizando el pipeline de manejo de documentos de LangChain:

```python
loader = TextLoader("state_of_the_union.txt", encoding="utf-8")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
```

## Casos de Uso Demostrados

### 1. Sistema de Recomendación de Visitantes
Encontrar asistentes similares basado en características laborales y retornar su historial de sesiones:

```python
# Encontrar visitantes con perfiles similares que asistieron años anteriores
# Retornar sesiones que atendieron para propósitos de recomendación
```

### 2. Descubrimiento de Sesiones
Identificar sesiones relevantes basado en perfiles de visitantes y mapeos de streams:

```python
# Encontrar sesiones en streams conectados al rol laboral del visitante
# Filtrar contenido irrelevante (ej., excluir "Equine" para profesionales de animales pequeños)
```

### 3. Análisis de Asistencia
Queries complejos analizando patrones de visitantes a través de múltiples años:

```python
# Rastrear comportamiento de visitantes a través de años de conferencia
# Analizar popularidad de sesiones y preferencias de streams
```

## Características Avanzadas

### Manejo de Queries Complejos
El sistema maneja consultas sofisticadas en lenguaje natural que involucran:
- Traversals de grafos multi-hop
- Coincidencia de patrones de strings y filtrado
- Lógica condicional con exclusiones
- Operaciones de agregación y ranking

### Manejo de Errores y Seguridad
- `allow_dangerous_requests=True` habilita queries complejos manteniendo control
- Logging de pasos intermedios para debugging y transparencia
- Output verbose para optimización de queries

### Capacidades de Búsqueda Híbrida
Combina las fortalezas de:
- **Similitud vectorial**: Comprensión semántica del contenido
- **Relaciones de grafos**: Contexto estructural y relacional
- **Razonamiento LLM**: Comprensión y generación de lenguaje natural

## Comenzando

1. **Instalar Dependencias**
   ```bash
   pip install langchain langchain-community langchain-neo4j langchain-openai tiktoken neo4j
   ```

2. **Configurar Base de Datos Neo4j**
   - Instalar Neo4j localmente o usar Neo4j Cloud
   - Configurar parámetros de conexión
   - Importar datos del grafo

3. **Configurar Entorno**
   ```bash
   # Crear archivo .env con:
   OPENAI_API_KEY=tu_openai_api_key
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=tu_password
   ```

4. **Ejecutar el Notebook**
   - Cargar documentos para indexación vectorial
   - Inicializar la conexión del grafo
   - Comenzar a consultar con lenguaje natural

## Integración con Claude Desktop (MCP)

El proyecto incluye instrucciones de configuración para integrar con Claude Desktop utilizando el Model Context Protocol:

```json
{
  "neo4j": {
    "command": "/Users/<username>/.local/bin/uvx",
    "args": [
      "mcp-neo4j-cypher",
      "--db-url", "bolt://localhost",
      "--username", "neo4j",
      "--password", "password"
    ]
  }
}
```

Esto habilita la interacción directa con Neo4j a través de la interfaz de Claude Desktop.

## Beneficios

- **Interfaz de Lenguaje Natural**: Usuarios no técnicos pueden consultar datos complejos de grafos
- **Conciencia Contextual**: Las relaciones de grafos proporcionan contexto rico para respuestas
- **Arquitectura Escalable**: Maneja datasets grandes con operaciones eficientes de vectores y grafos
- **Consultas Flexibles**: Soporta tanto búsqueda semántica como traversals precisos de grafos
- **Valor Educativo**: Demuestra técnicas de vanguardia en RAG y bases de datos de grafos

## Mejoras Futuras

- Integración con streams de datos en tiempo real
- Prompt engineering avanzado para optimización de queries
- Soporte de datos multi-modales (imágenes, documentos, datos estructurados)
- Monitoreo de performance y optimización de queries
- Capacidades extendidas de filtrado de metadata y búsqueda

Este notebook sirve como un ejemplo comprensivo de construcción de interfaces inteligentes y conversacionales para bases de datos de grafos, mostrando el poder de combinar LLMs con representaciones de conocimiento estructuradas.