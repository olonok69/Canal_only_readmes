# Speak with your Graph Database - LangChain Neo4j RAG System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system that allows natural language interaction with Neo4j graph databases using LangChain. The system combines vector similarity search with graph database querying to provide intelligent responses about complex, interconnected data structures.

The notebook demonstrates three primary techniques for interacting with graph databases:
1. **Vector similarity search** using Neo4j's vector capabilities
2. **Direct graph querying** with Cypher queries
3. **Natural language to Cypher translation** using LLMs

## Key Technologies

### LangChain Neo4j Integration
- **Neo4jGraph**: A wrapper for the Neo4j Python driver that simplifies database operations
- **Neo4jVector**: Vector store implementation supporting embeddings, similarity search, and hybrid retrieval
- **GraphCypherQAChain**: Natural language interface that translates questions into Cypher queries

### Model Context Protocol (MCP)
The project references Anthropic's Model Context Protocol, a standardized way to provide context for LLMs, enabling seamless integration between applications and language models.

## Architecture Components

### 1. Vector Store Operations (Neo4jVector)

The Neo4jVector integration provides comprehensive vector database functionality:

```python
db = Neo4jVector.from_documents(
    docs, embeddings, url=uri, username=username, password=password
)
```

**Capabilities:**
- Create vector embeddings from LangChain documents
- Perform similarity searches with scoring
- Execute hybrid searches combining vector and graph queries
- Apply metadata filtering
- Construct vector instances from existing graph data

### 2. Graph Database Interface (Neo4jGraph)

Direct interaction with the Neo4j database using Cypher queries:

```python
graph = Neo4jGraph(url=uri, username=username, password=password)
result = graph.query(cypher_query, params=parameters)
```

This allows for complex graph traversals and relationship-based queries that leverage the full power of Neo4j's graph capabilities.

### 3. Natural Language Query Interface (GraphCypherQAChain)

The most sophisticated component translates natural language questions into Cypher queries:

```python
chain = GraphCypherQAChain.from_llm(
    llm, graph=graph, verbose=True,
    allow_dangerous_requests=True,
    return_intermediate_steps=True
)
```

**Process Flow:**
1. User submits natural language question
2. LLM analyzes graph schema and question
3. LLM generates appropriate Cypher query
4. Query executes against Neo4j database
5. Results are processed by LLM to generate natural language response

## Data Model

The system works with a veterinary conference dataset containing:

- **Visitors_this_year**: Current year attendees with job titles, roles, and specializations
- **Visitor_last_year_lva/bva**: Previous year attendees from different shows
- **Sessions_this_year/past_year**: Conference sessions with stream classifications
- **Streams**: Subject matter categories (e.g., "nursing", "Equine", "Small Animal")

**Key Relationships:**
- `Same_Visitor`: Links attendees across years
- `attended_session`: Connects visitors to sessions
- `Has_stream`: Associates sessions with subject streams
- `job_to_stream`: Maps job roles to relevant streams

## Implementation Details

### Environment Setup

```python
# Required dependencies
pip install langchain langchain-community langchain-neo4j
pip install langchain-openai tiktoken
pip install neo4j
```

### Configuration

The system uses environment variables for secure credential management:

```python
from dotenv import load_dotenv, dotenv_values
config = dotenv_values(".env")

# OpenAI LLM configuration
llm = ChatOpenAI(
    model="gpt-4.1",
    openai_api_key=config["OPENAI_API_KEY"],
    temperature=0,
    max_tokens=8192
)

# Neo4j connection
uri = "bolt://127.0.0.1:7687"
username = "neo4j"
password = ""  # Set in environment
```

### Document Processing

Text documents are processed using LangChain's document handling pipeline:

```python
loader = TextLoader("state_of_the_union.txt", encoding="utf-8")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
```

## Use Cases Demonstrated

### 1. Visitor Recommendation System
Find similar attendees based on job characteristics and return their session history:

```python
# Find visitors with similar profiles who attended previous years
# Return sessions they attended for recommendation purposes
```

### 2. Session Discovery
Identify relevant sessions based on visitor profiles and stream mappings:

```python
# Find sessions in streams connected to visitor's job role
# Filter out irrelevant content (e.g., excluding "Equine" for small animal practitioners)
```

### 3. Attendance Analysis
Complex queries analyzing visitor patterns across multiple years:

```python
# Track visitor behavior across conference years
# Analyze session popularity and stream preferences
```

## Advanced Features

### Complex Query Handling
The system handles sophisticated natural language queries involving:
- Multi-hop graph traversals
- String pattern matching and filtering
- Conditional logic with exclusions
- Aggregation and ranking operations

### Error Handling and Safety
- `allow_dangerous_requests=True` enables complex queries while maintaining control
- Intermediate step logging for debugging and transparency
- Verbose output for query optimization

### Hybrid Search Capabilities
Combines the strengths of:
- **Vector similarity**: Semantic understanding of content
- **Graph relationships**: Structural and relational context
- **LLM reasoning**: Natural language understanding and generation

## Getting Started

1. **Install Dependencies**
   ```bash
   pip install langchain langchain-community langchain-neo4j langchain-openai tiktoken neo4j
   ```

2. **Setup Neo4j Database**
   - Install Neo4j locally or use Neo4j Cloud
   - Configure connection parameters
   - Import your graph data

3. **Configure Environment**
   ```bash
   # Create .env file with:
   OPENAI_API_KEY=your_openai_api_key
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_password
   ```

4. **Run the Notebook**
   - Load your documents for vector indexing
   - Initialize the graph connection
   - Start querying with natural language

## Integration with Claude Desktop (MCP)

The project includes setup instructions for integrating with Claude Desktop using the Model Context Protocol:

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

This enables direct Neo4j interaction through Claude Desktop's interface.

## Benefits

- **Natural Language Interface**: Non-technical users can query complex graph data
- **Contextual Awareness**: Graph relationships provide rich context for responses
- **Scalable Architecture**: Handles large datasets with efficient vector and graph operations
- **Flexible Querying**: Supports both semantic search and precise graph traversals
- **Educational Value**: Demonstrates cutting-edge techniques in RAG and graph databases

## Future Enhancements

- Integration with real-time data streams
- Advanced prompt engineering for query optimization
- Multi-modal data support (images, documents, structured data)
- Performance monitoring and query optimization
- Extended metadata filtering and search capabilities

This notebook serves as a comprehensive example of building intelligent, conversational interfaces for graph databases, showcasing the power of combining LLMs with structured knowledge representations.