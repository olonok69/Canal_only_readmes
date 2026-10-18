# MCP: El protocolo que revoluciona la interacción de la IA con el mundo digital

El Model Context Protocol (MCP) es un estándar abierto desarrollado por Anthropic a finales de 2024 que funciona como un "puerto USB-C para aplicaciones de IA", proporcionando una forma estandarizada para que los modelos de inteligencia artificial se conecten con fuentes de datos externas, herramientas y sistemas. MCP resuelve el problema de integración "M×N" transformándolo en un problema "M+N", permitiendo que cualquier modelo de IA pueda interactuar con cualquier herramienta o fuente de datos a través de un protocolo común, sin necesidad de desarrollar integraciones personalizadas para cada combinación. Este enfoque ha ganado rápida adopción por parte de empresas como Block (Square), Apollo, Replit y Sourcegraph, con más de 1,000 servidores MCP construidos por la comunidad para principios de 2025.

## Los fundamentos del MCP

El MCP surge como respuesta a una limitación fundamental de los modelos de lenguaje: aunque son potentes para generar texto, carecen de capacidad nativa para interactuar con el mundo exterior. Antes de MCP, cada integración entre un modelo de IA y una herramienta externa requería desarrollo personalizado, creando un problema de escala cuando múltiples modelos necesitaban conectarse con múltiples herramientas.

La arquitectura MCP se compone de tres elementos principales:

1. **MCP Host**: La aplicación donde se ejecuta el modelo de IA (como Claude Desktop, IDEs o herramientas empresariales).
2. **MCP Client**: Componentes que mantienen conexiones con los servidores MCP.
3. **MCP Server**: Programas ligeros que exponen capacidades específicas a través del protocolo MCP estandarizado.

Este diseño se inspiró en el Language Server Protocol (LSP), que resolvió un problema similar para editores de código e IDEs.

### Principios clave que guían el MCP:

- **Estandarización**: Formato común para la comunicación entre aplicaciones de IA y herramientas externas
- **Apertura**: Estándar abierto que cualquier desarrollador puede implementar
- **Interoperabilidad**: Independencia del modelo, permitiendo que cualquier IA utilice servidores MCP
- **Seguridad**: Control de acceso y protección de datos incorporados en el diseño
- **Descubrimiento dinámico**: Los modelos pueden descubrir herramientas disponibles sin configuración previa

## Server: El puente entre la IA y los sistemas externos

El servidor MCP actúa como intermediario entre los modelos de IA y los sistemas externos, exponiendo capacidades a través de una interfaz estandarizada. **Funciona como traductor bidireccional**, convirtiendo las peticiones del modelo en acciones específicas sobre sistemas externos y devolviendo resultados en un formato que el modelo puede comprender.

Los servidores implementan el protocolo JSON-RPC 2.0 y soportan múltiples mecanismos de transporte:
- **stdio** (entrada/salida estándar) para servidores locales
- **SSE** (Server-Sent Events) y **WebSockets** para comunicación remota

```javascript
// Ejemplo básico de un servidor MCP en TypeScript
import { Server } from "@modelcontextprotocol/sdk/server";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio";

const server = new Server({
  name: "mi-servidor-mcp",
  version: "1.0.0"
}, { capabilities: { tools: {} } });

// Registrar una herramienta
server.tool({
  name: "saludar",
  description: "Genera un saludo personalizado",
  parameters: {
    nombre: {
      type: "string",
      description: "Nombre de la persona a saludar"
    }
  },
  handler: async (params) => {
    return `Hola, ${params.nombre}!`;
  }
});

// Iniciar el servidor con transporte stdio
const transport = new StdioServerTransport();
server.listen(transport);
```

En la práctica, existen servidores MCP para diversos sistemas como bases de datos (PostgreSQL, MongoDB), sistemas de control de versiones (GitHub, GitLab), y aplicaciones de productividad (Slack, Google Drive).

## Resources: Las fuentes de datos estructurados

Los recursos en MCP son fuentes de datos estructurados, **similares a endpoints GET en una API REST**. Proporcionan información sin realizar cálculos significativos y forman parte del contexto que el modelo utiliza para generar respuestas precisas.

Características principales de los resources:
- Se acceden mediante una ruta única en formato nombre/identificador
- Pueden tener parámetros opcionales para personalizar la consulta
- Devuelven datos estructurados en formato JSON
- No modifican el estado de los sistemas externos (sin efectos secundarios)

```javascript
// Ejemplo de definición de un recurso en un servidor MCP
server.resource({
  name: "documentos",
  description: "Accede a documentos almacenados",
  parameters: {
    carpeta: {
      type: "string",
      description: "Carpeta donde buscar"
    }
  },
  handler: async (params) => {
    // Lógica para obtener documentos de la carpeta especificada
    const documentos = await obtenerDocumentos(params.carpeta);
    return documentos;
  }
});
```

Los recursos facilitan el acceso a información como listados de archivos, registros de bases de datos, mensajes de canales de chat o documentación de APIs.

## Tools: Las funciones ejecutables

Las herramientas en MCP son funciones que los modelos pueden invocar para ejecutar acciones específicas, **similares a métodos POST en una API REST**. Permiten que el modelo vaya más allá de la generación de texto, actuando sobre sistemas externos.

Características de las tools:
- Tienen un nombre único y una descripción clara
- Definen un esquema de parámetros de entrada con tipos y descripciones
- Pueden devolver resultados estructurados
- Admiten gestión de errores y validación de parámetros

```javascript
// Ejemplo de definición de una herramienta en un servidor MCP
server.tool({
  name: "enviar_email",
  description: "Envía un correo electrónico",
  parameters: {
    destinatario: {
      type: "string",
      description: "Dirección de correo del destinatario"
    },
    asunto: {
      type: "string",
      description: "Asunto del correo"
    },
    cuerpo: {
      type: "string",
      description: "Contenido del correo"
    }
  },
  handler: async (params) => {
    // Lógica para enviar el correo
    await enviarEmail(params.destinatario, params.asunto, params.cuerpo);
    return { success: true, message: "Correo enviado correctamente" };
  }
});
```

Estas herramientas pueden realizar diversas operaciones como manipulación de archivos, interacción con APIs externas, consultas a bases de datos o generación de contenido multimedia.

## Prompts: Las plantillas predefinidas

Los prompts en MCP son plantillas predefinidas que estructuran las interacciones entre el usuario, el modelo y las herramientas disponibles. **Actúan como guías estandarizadas** que optimizan las consultas para casos de uso específicos.

Características de los prompts:
- Tienen un nombre único y una descripción
- Pueden aceptar argumentos personalizables
- Generan secuencias de mensajes estructurados
- Son controlados por el usuario en el flujo de MCP

```javascript
// Ejemplo de definición de un prompt en un servidor MCP
server.prompt({
  name: "analizar_codigo",
  description: "Analiza un fragmento de código para mejoras",
  arguments: [
    {
      name: "lenguaje",
      description: "Lenguaje de programación",
      required: true
    },
    {
      name: "codigo",
      description: "Código a analizar",
      required: true
    }
  ],
  handler: async (args) => {
    return [
      {
        role: "system",
        content: {
          type: "text",
          text: `Eres un experto en ${args.lenguaje}. Analiza el siguiente código y sugiere mejoras.`
        }
      },
      {
        role: "user",
        content: {
          type: "text",
          text: `Aquí está el código a analizar:\n\n\`\`\`${args.lenguaje}\n${args.codigo}\n\`\`\``
        }
      }
    ];
  }
});
```

Los prompts se utilizan para casos como análisis de código, generación de resúmenes, plantillas para correos o informes, y flujos de revisión de proyectos.

## Images: El componente visual

El componente de imágenes en MCP permite a los modelos de IA procesar, generar y manipular contenido visual. **Extiende las capacidades del modelo al dominio visual**, facilitando interacciones multimodales.

Características técnicas:
- Maneja imágenes en formatos estándar (PNG, JPEG, etc.)
- Utiliza codificación Base64 para transmitir imágenes a través del protocolo
- Permite operaciones de procesamiento como redimensionado y filtrado
- Soporta integración con APIs de generación de imágenes (DALL-E, Stable Diffusion)

```javascript
// Ejemplo de una herramienta para generar imágenes en un servidor MCP
server.tool({
  name: "generar_imagen",
  description: "Genera una imagen a partir de una descripción",
  parameters: {
    prompt: {
      type: "string",
      description: "Descripción de la imagen a generar"
    },
    ancho: {
      type: "number",
      description: "Ancho de la imagen en píxeles",
      default: 512
    },
    alto: {
      type: "number",
      description: "Alto de la imagen en píxeles",
      default: 512
    }
  },
  handler: async (params) => {
    // Lógica para generar la imagen usando un modelo de IA
    const imagenBase64 = await generarImagen(params.prompt, params.ancho, params.alto);
    return {
      image: imagenBase64,
      mimeType: "image/png",
      width: params.ancho,
      height: params.alto
    };
  }
});
```

El procesamiento de imágenes se implementa a través de servidores especializados como MCP-DALL-E, herramientas OCR, o procesadores para diagramas y visualizaciones.

## Context: El entorno informativo

El contexto en MCP es el entorno informativo en el que opera el modelo de IA, incluyendo los datos, herramientas y recursos disponibles durante una interacción. **Funciona como la memoria de trabajo del sistema**, proporcionando la información necesaria para generar respuestas precisas.

Características del context:
- Incluye información de múltiples fuentes (recursos, historial de conversación)
- Es dinámico y puede actualizarse durante una sesión
- Se gestiona eficientemente para optimizar la ventana de contexto del modelo
- Incluye metadatos sobre disponibilidad y permisos de herramientas

```javascript
// Ejemplo de solicitud de sampling (contexto adicional) desde un servidor MCP
server.setRequestHandler(SamplingRequestSchema, async (request) => {
  // El servidor solicita que el modelo genere texto adicional basado en un contexto
  const resultado = await client.sampling({
    messages: [
      {
        role: "user",
        content: { type: "text", text: "Por favor resume este documento." }
      }
    ],
    systemPrompt: "Eres un asistente experto en resúmenes.",
    includeContext: "thisServer", // Solo incluye el contexto de este servidor
    maxTokens: 300
  });
  
  return resultado;
});
```

La gestión del contexto se implementa a nivel de arquitectura, con hosts MCP gestionando el contexto global, clientes MCP manteniendo el contexto específico de cada servidor, y actualizaciones dinámicas con los resultados de las herramientas.

## La orquesta digital: Cómo interactúan los componentes

El poder real de MCP emerge cuando todos sus componentes trabajan juntos en un flujo coordinado:

1. El **Host** (Claude Desktop, Cursor, etc.) inicia la comunicación a través del **Cliente MCP**
2. El **Cliente MCP** se conecta al **Servidor MCP** (GitHub, Google Drive, etc.)
3. El **Servidor MCP** expone **tools**, **resources** y **prompts** al cliente
4. El **Host** presenta estas capacidades al usuario y al modelo de IA
5. Cuando el modelo necesita usar una herramienta, solicita permiso al usuario
6. Con aprobación, la solicitud pasa del **Cliente** al **Servidor** para ejecución
7. Los resultados regresan al **Host** a través del **Cliente**
8. El modelo incorpora esta información en su **contexto** para generar respuestas

Este flujo se observa en implementaciones reales como:

- **Cursor IDE**: Cuando un usuario hace una pregunta sobre código en GitHub, Cursor identifica que necesita el servidor GitHub MCP, el modelo solicita permiso para usar herramientas específicas, y con aprobación, ejecuta las operaciones necesarias para obtener la información.

- **Claude Desktop**: Al interactuar con documentos en Google Drive, Claude utiliza el servidor MCP correspondiente para acceder a los archivos necesarios, manteniendo los datos dentro de la infraestructura del usuario.

- **Block (Square)**: Como señala su CTO, Dhanji R. Prasanna: "Las tecnologías abiertas como el Model Context Protocol son los puentes que conectan la IA con aplicaciones del mundo real."

## La comunidad MCP: Implementación y casos de uso

El ecosistema MCP ha crecido rápidamente, con numerosos servidores oficiales y comunitarios:

**Servidores oficiales**:
- Filesystem (operaciones de archivos locales)
- PostgreSQL y SQLite (bases de datos)
- Google Drive (archivos en la nube)
- Git, GitHub y GitLab (control de versiones)
- Sentry (gestión de errores)
- Brave Search (búsqueda web)

**Implementaciones empresariales**:
- **Confluent**: Servidor MCP para Kafka que permite interacciones en lenguaje natural con datos en tiempo real
- **Visual Studio Code**: Integración con GitHub Copilot mediante MCP
- **Zed y Replit**: Editores de código con soporte MCP para mejoras en asistencia de IA

El impacto de MCP se observa en múltiples sectores, desde desarrollo de software hasta aplicaciones empresariales, demostrando su versatilidad y potencial para transformar la forma en que las aplicaciones de IA interactúan con sistemas externos.

## Una revolución silenciosa en la integración de IA

El Model Context Protocol representa un avance fundamental en cómo las inteligencias artificiales interactúan con datos y sistemas externos. Al proporcionar un estándar común para estas interacciones, MCP elimina la necesidad de integraciones personalizadas, permite la portabilidad entre diferentes modelos, y facilita un ecosistema rico de herramientas que cualquier IA puede utilizar.

A medida que crece la adopción de MCP, podemos esperar asistentes de IA más capaces, contextuales e integrados con nuestros sistemas digitales, transformando la forma en que trabajamos con la tecnología. Esta "capa de traducción universal" para IA marca un paso crucial hacia asistentes verdaderamente útiles que pueden no solo generar texto, sino actuar efectivamente en el mundo digital en nuestro nombre.

# Python Examples

Python's Model Context Protocol implementation offers a cleaner, simpler syntax while maintaining all the power of the TypeScript version. This guide shows you the Python equivalents for key MCP components with practical, production-ready examples.

## The fundamentals: setting up a basic MCP server

TypeScript's more verbose class-based approach transforms into Python's cleaner decorator pattern. The Python SDK provides `FastMCP` which dramatically simplifies server creation:

```python
from mcp.server.fastmcp import FastMCP

# Create a named MCP server
mcp = FastMCP(name="SimpleMCPServer")

# Add a basic tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b

# Run the server if executed directly
if __name__ == "__main__":
    mcp.run()
```

Python's implementation streamlines MCP server creation with cleaner type hints, automatic schema generation, and built-in runtime support.

## Defining resources: data access made simple

Resources in MCP provide data to LLMs (like GET endpoints). While TypeScript requires explicit schema objects, Python leverages type annotations and decorators:

```python
# Static resource path
@mcp.resource("config://app")
def get_app_config() -> str:
    """Serve application configuration as a resource"""
    return """
    {
        "version": "1.0.0",
        "environment": "development",
        "features": {
            "dark_mode": true,
            "beta_features": false
        }
    }
    """

# Dynamic path with parameters
@mcp.resource("users://{user_id}")
def get_user(user_id: str) -> dict:
    """Return user data as a dictionary (automatically JSON-serialized)"""
    # Simulate database lookup
    user_data = {
        "id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com",
        "active": True
    }
    return user_data  # SDK handles JSON serialization
```

The Python SDK automatically handles serialization of return values while providing intelligent URI pattern matching and parameter extraction.

## Creating powerful tools: from functions to LLM capabilities

Tools in MCP execute actions and produce results (similar to POST endpoints). Python's implementation uses type annotations to generate input schemas:

```python
# Basic tool with docstring
@mcp.tool()
def echo(message: str) -> str:
    """Echo back the provided message."""
    return f"Echo: {message}"

# Tool with complex parameters
@mcp.tool()
def process_file(
    file_path: str, 
    columns: list[str], 
    options: dict[str, str] = None,
    limit: int = None
) -> dict:
    """Process a file with the given parameters."""
    options = options or {}
    
    # Simulated processing logic
    return {
        "status": "success",
        "columns_processed": len(columns),
        "options_applied": list(options.keys()),
        "limit_used": limit
    }
```

For async operations, Python's implementation is particularly elegant:

```python
@mcp.tool()
async def fetch_weather(city: str, ctx: Context) -> dict:
    """Fetch current weather for a city."""
    # Log operation to client
    await ctx.info(f"Fetching weather for {city}...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/weather/{city}")
        response.raise_for_status()
        
        # Report progress
        await ctx.report_progress(1, 1)
        
        return response.json()
```

## Defining prompts: structured interaction templates

Prompts define reusable interaction patterns for LLMs. Python's implementation is more intuitive:

```python
# Simple prompt returning a string
@mcp.prompt()
def analyze_code(code: str) -> str:
    """Generate a prompt asking for code analysis."""
    return f"Please analyze the following code and suggest improvements:\n\n```python\n{code}\n```"

# Advanced prompts with multiple messages
from mcp.server.fastmcp.prompts import base

@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    """Create a debugging workflow with multiple messages."""
    return [
        base.UserMessage("I'm seeing this error in my application:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that error. What have you tried so far?")
    ]
```

## Handling images: seamless multimodal support

The Python SDK provides elegant handling of images through its `Image` class:

```python
from mcp.server.fastmcp import FastMCP, Image
from PIL import Image as PILImage
import io

@mcp.tool()
def create_thumbnail(image_path: str, size: int = 100) -> Image:
    """Create a thumbnail from an image file."""
    # Open the source image with PIL
    img = PILImage.open(image_path)
    img.thumbnail((size, size))
    
    # Convert to bytes and return using Image helper 
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return Image(
        data=buffer.getvalue(),
        format="png",
        width=img.width,
        height=img.height
    )
```

Python's implementation handles both receiving and returning images with clean integration with PIL (Pillow):

```python
@mcp.tool()
def analyze_image(image: Image) -> dict:
    """Analyze an image and return information about it."""
    # Convert image data to PIL Image for processing
    img_data = io.BytesIO(image.data)
    img = PILImage.open(img_data)
    
    # Return analysis results
    return {
        "format": image.format,
        "width": image.width or img.width,
        "height": image.height or img.height,
        "mode": img.mode
    }
```

## Sampling: adding AI capabilities to your server

Sampling allows MCP servers to request completions from the client's LLM. The Python implementation uses the context object:

```python
@mcp.tool()
async def summarize_text(text: str, ctx: Context) -> str:
    """Summarize the provided text using the LLM."""
    # Log a message to the client
    await ctx.info("Summarizing text...")
    
    # Request a summary from the client's LLM
    summary = await ctx.sample(
        messages=[
            {"role": "user", "content": f"Please provide a concise summary of the following text:\n\n{text}"}
        ],
        system_prompt="You are a helpful assistant that specializes in creating concise summaries.",
        max_tokens=200
    )
    
    # Return the summary text
    return summary.text
```

The Python implementation allows for extensive customization of sampling parameters:

```python
# Advanced sampling with more configuration
response = await ctx.sample(
    messages=[
        {"role": "user", "content": query}
    ],
    system_prompt="You are an expert programmer.",
    max_tokens=1000,
    temperature=0.7,
    stop_sequences=["\n\n"],
    include_context="thisServer",
    model_preferences={
        "hints": [{"name": "claude-3-opus"}],
        "intelligencePriority": 0.9
    }
)
```

## Using the context API

The Context object provides access to session capabilities within tools, resources, or prompts:

```python
@mcp.tool()
async def process_items(items: list[str], ctx: Context) -> dict:
    """Process a list of items with progress reporting."""
    total = len(items)
    results = []
    
    for i, item in enumerate(items):
        # Report progress to the client
        await ctx.report_progress(i, total)
        
        # Log processing step
        await ctx.info(f"Processing item {i+1}/{total}: {item}")
        
        # Add to results
        results.append(f"Processed: {item}")
    
    # Final progress update
    await ctx.report_progress(total, total)
    
    return {
        "status": "success",
        "processed": total,
        "results": results
    }
```

## Complete server example

Here's a complete example of a Python MCP server implementation:

```python
from mcp.server.fastmcp import FastMCP, Context, Image
from PIL import Image as PILImage
import httpx
import io

# Create MCP server
mcp = FastMCP("Complete Example Server")

# Define resources
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting."""
    return f"Hello, {name}!"

@mcp.resource("config://app")
def get_config() -> dict:
    """Get application configuration."""
    return {
        "version": "1.0.0",
        "debug": True,
        "features": ["search", "analytics"]
    }

# Define tools
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
async def fetch_data(url: str, ctx: Context) -> dict:
    """Fetch data from a URL."""
    await ctx.info(f"Fetching data from {url}...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

@mcp.tool()
def process_image(image: Image) -> dict:
    """Analyze an image."""
    img_data = io.BytesIO(image.data)
    img = PILImage.open(img_data)
    
    return {
        "format": image.format,
        "dimensions": f"{img.width}x{img.height}",
        "mode": img.mode
    }

# Define prompts
@mcp.prompt()
def code_review(code: str) -> str:
    """Generate a prompt for code review."""
    return f"Please review this code and suggest improvements:\n\n```\n{code}\n```"

# Run the server
if __name__ == "__main__":
    mcp.run()
```

## Conclusion: Python's streamlined approach

Python's implementation of the Model Context Protocol offers several advantages over TypeScript:

1. **More concise syntax** through decorators and type annotations
2. **Simpler setup and configuration** with the FastMCP helper class
3. **Cleaner async support** with Python's native async/await
4. **Elegant error handling** with Python's exception mechanisms
5. **Better integration** with Python's rich ecosystem for data processing and AI

By using Python's implementation, developers can build robust MCP servers with less code while maintaining all the functionality of the TypeScript implementation.

Whether you're building tools, resources, or working with images and sampling, the Python SDK provides an intuitive and powerful way to integrate with the Model Context Protocol ecosystem.