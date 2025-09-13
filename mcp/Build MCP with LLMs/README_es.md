# Creando Servidores MCP con LLMs: Procesador de Documentos PDF

Una guía completa para acelerar el desarrollo de servidores MCP usando modelos de lenguaje como Claude, con un ejemplo práctico de procesamiento de documentos PDF.

## 📋 Tabla de Contenidos

- [Introducción](#introducción)
- [Construyendo MCP con LLMs](#construyendo-mcp-con-llms)
- [Ejemplo Práctico: Procesador de Documentos PDF](#ejemplo-práctico-procesador-de-documentos-pdf)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Características Avanzadas](#características-avanzadas)
- [Solución de Problemas](#solución-de-problemas)

## 🚀 Introducción

Esta guía te enseñará cómo usar modelos de lenguaje (LLMs) como Claude para acelerar el desarrollo de servidores del Protocolo de Contexto de Modelo (MCP). Incluye un ejemplo completo de un servidor que procesa documentos PDF y aplica prompts personalizados para análisis y resumen.

## 🤖 Construyendo MCP con LLMs

### ¿Por qué usar LLMs para desarrollar MCP?

Los LLMs como Claude pueden acelerar significativamente el desarrollo de servidores MCP al:
- Generar código estructurado y funcional
- Explicar conceptos complejos del protocolo MCP
- Ayudar con la implementación de herramientas, recursos y prompts
- Asistir en la depuración y optimización

### Preparando la Documentación

Antes de comenzar, reúne la documentación necesaria para ayudar a Claude a entender MCP:

1. **Documentación Completa de MCP**: Visita [https://modelcontextprotocol.io/llms-full.txt](https://modelcontextprotocol.io/llms-full.txt) y copia el texto completo
2. **SDK Documentation**: Navega al repositorio del [SDK de TypeScript](https://github.com/modelcontextprotocol/typescript-sdk) o [SDK de Python](https://github.com/modelcontextprotocol/python-sdk)
3. **Pega estos documentos** en tu conversación con Claude

### Describiendo tu Servidor

Una vez que hayas proporcionado la documentación, describe claramente a Claude qué tipo de servidor quieres construir:

```
Construye un servidor MCP que:
- Extraiga contenido de documentos PDF
- Aplique OCR para documentos escaneados  
- Ofrezca herramientas para análisis con prompts personalizados
- Convierta contenido a formato markdown
- Gestione una biblioteca de prompts para diferentes tipos de análisis
```

### Trabajando con Claude

Al trabajar con Claude en servidores MCP:

1. **Comienza con la funcionalidad principal** primero, luego itera para agregar más características
2. **Pide a Claude que explique** cualquier parte del código que no entiendas
3. **Solicita modificaciones** o mejoras según sea necesario
4. **Haz que Claude te ayude** a probar el servidor y manejar casos extremos

Claude puede ayudar a implementar todas las características clave de MCP:
- Gestión y exposición de recursos
- Definiciones e implementaciones de herramientas
- Plantillas y manejadores de prompts
- Manejo de errores y logging
- Configuración de conexión y transporte

## 📄 Ejemplo Práctico: Procesador de Documentos PDF

### Descripción General

Nuestro ejemplo es un servidor MCP completo que demuestra:

- **Extracción de PDF**: Extrae texto de documentos PDF regulares
- **Soporte OCR**: Procesa PDFs escaneados usando reconocimiento óptico de caracteres
- **Prompts Personalizados**: Aplica plantillas predefinidas para análisis específicos
- **Salida en Markdown**: Genera contenido bien formateado
- **Gestión de Prompts**: Lista y administra prompts de análisis personalizados

### Arquitectura del Servidor

```python
# Estructura principal usando FastMCP
from mcp.server.fastmcp import FastMCP

# Inicializar el servidor
mcp = FastMCP("PDF Document Processor")

# Herramientas principales
@mcp.tool()
async def extract_pdf_to_markdown(pdf_base64: str, filename: str = "document.pdf") -> str:
    """Extrae contenido de PDF y convierte a markdown"""
    
@mcp.tool()
async def extract_scanned_pdf_to_markdown(pdf_base64: str, filename: str = "document.pdf") -> str:
    """Extrae texto de PDFs escaneados usando OCR"""

@mcp.tool()
async def apply_prompt_to_content(content: str, prompt_id: str) -> str:
    """Aplica un prompt específico al contenido extraído"""
```

## 🛠 Instalación

### Requisitos Previos

1. **Python 3.8+** es requerido
2. **Tesseract OCR** para procesamiento de documentos escaneados

#### En Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-spa tesseract-ocr-eng
```

#### En macOS:
```bash
brew install tesseract tesseract-lang
```

#### En Windows:
Descarga e instala desde: https://github.com/UB-Mannheim/tesseract/wiki

### Instalación con UV (Recomendado)

#### Usando PowerShell (Windows):
```powershell
.\install_windows_uv.ps1
```

#### Usando Batch (Windows):
```cmd
install_windows_uv.bat
```

#### Instalación Manual:

```bash
# Instalar UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Crear proyecto
uv init pdf-processor-mcp
cd pdf-processor-mcp

# Instalar dependencias
uv add "mcp[cli]>=1.2.0"
uv add "PyMuPDF>=1.23.0"
uv add "pytesseract>=0.3.10"
uv add "Pillow>=10.0.0"
uv add "opencv-python>=4.8.0"
```

### Instalación Tradicional con pip

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### 1. Archivos del Servidor

Copia estos archivos al directorio del proyecto:
- `pdf_processor_server.py` - Servidor principal MCP
- `prompts.json` - Configuración de prompts personalizados

### 2. Configuración de Claude Desktop

Agrega este servidor a tu configuración de Claude Desktop:

**macOS/Linux:**
```json
{
  "mcpServers": {
    "pdf-processor": {
      "command": "uv",
      "args": [
        "--directory",
        "/RUTA/ABSOLUTA/AL/DIRECTORIO/pdf-processor-mcp",
        "run",
        "python",
        "pdf_processor_server.py"
      ]
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "pdf-processor": {
      "command": "uv",
      "args": [
        "run",
        "python", 
        "C:\\RUTA\\ABSOLUTA\\AL\\DIRECTORIO\\pdf-processor-mcp\\pdf_processor_server.py"
      ],
      "cwd": "C:\\RUTA\\ABSOLUTA\\AL\\DIRECTORIO\\pdf-processor-mcp"
    }
  }
}
```

### 3. Configuración de Prompts

El archivo `prompts.json` contiene plantillas de análisis:

```json
[
  {
    "id": "638f3f81-0082-4df9-929f-e7b120d4f954",
    "name_prompt": "Informe Pericial: estado actual",
    "prompt": "Haz una redacción extensa describiendo el estado médico actual del paciente...",
    "keywords": "estado,actual,limitaciones,secuelas"
  }
]
```

## 🎯 Uso

### Herramientas Disponibles

#### 1. `list_prompts()`
Lista todos los prompts disponibles con IDs, nombres y palabras clave.

#### 2. `extract_pdf_to_markdown(pdf_base64, filename)`
Extrae contenido de texto de PDFs y convierte a formato markdown.

#### 3. `extract_scanned_pdf_to_markdown(pdf_base64, filename)`
Extrae texto de PDFs escaneados usando OCR.

#### 4. `get_prompt_by_id(prompt_id)`
Recupera un prompt específico por su ID.

#### 5. `apply_prompt_to_content(content, prompt_id)`
Aplica un prompt específico al contenido extraído para análisis.

#### 6. `process_pdf_with_prompt(pdf_base64, prompt_id, filename, use_ocr)`
Flujo completo: extrae contenido del PDF y aplica un prompt.

### Ejemplo de Flujo de Trabajo

1. **Sube un documento PDF** (convertido a base64)
2. **Lista los prompts disponibles** para ver opciones de análisis
3. **Procesa el PDF** con un prompt específico:

```python
# Ejemplo usando el flujo completo
result = await process_pdf_with_prompt(
    pdf_base64="<contenido_base64>",
    prompt_id="638f3f81-0082-4df9-929f-e7b120d4f954",
    filename="informe_medico.pdf",
    use_ocr=False
)
```

### Usando en Claude Desktop

Una vez configurado, verás el ícono de herramientas 🔨 en Claude Desktop:

1. **Sube un documento PDF**
2. **Pregunta**: "¿Puedes extraer el contenido de este PDF y aplicar el prompt de informe pericial?"
3. **Claude usará automáticamente** las herramientas del servidor MCP

## 🔧 Características Avanzadas

### Procesamiento OCR Inteligente

El servidor detecta automáticamente si un PDF necesita OCR:

```python
def extract_text_from_pdf(pdf_path: str) -> str:
    """Extrae texto de PDF usando PyMuPDF con fallback a OCR"""
    doc = fitz.open(pdf_path)
    text = ""
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text()
        
        if page_text.strip():
            text += f"\n\n## Página {page_num + 1}\n\n{page_text}"
        else:
            # Si no se encuentra texto, la página podría estar escaneada
            ocr_text = extract_text_from_scanned_page(page)
            if ocr_text.strip():
                text += f"\n\n## Página {page_num + 1} (OCR)\n\n{ocr_text}"
```

### Gestión de Prompts Dinámicos

Los prompts se cargan dinámicamente desde `prompts.json`:

```python
def load_prompts():
    """Carga prompts desde archivo JSON"""
    global prompts_data
    try:
        if os.path.exists(PROMPTS_FILE):
            with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
                prompts_data = json.load(f)
            logger.info(f"Cargados {len(prompts_data)} prompts")
    except Exception as e:
        logger.error(f"Error cargando prompts: {e}")
```

### Salida en Markdown Estructurado

El contenido extraído se convierte automáticamente a markdown bien formateado:

```python
def convert_to_markdown(text: str) -> str:
    """Convierte texto extraído a formato markdown"""
    if not text.strip():
        return "# Documento\n\nNo se pudo extraer contenido de texto de este documento."
    
    markdown = f"# Contenido del Documento Extraído\n\n{text}"
    
    # Limpieza de espacios en blanco extra
    lines = markdown.split('\n')
    cleaned_lines = []
    
    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line or (cleaned_lines and cleaned_lines[-1].strip()):
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)
```

## 🐛 Solución de Problemas

### Problemas Comunes

#### 1. Tesseract no encontrado
**Solución:**
- Asegúrate de que Tesseract OCR esté instalado correctamente y en tu PATH
- En Windows, verifica que se agregó al PATH durante la instalación

#### 2. Errores de procesamiento de PDF
**Solución:**
- Verifica que el archivo PDF no esté corrupto o protegido con contraseña
- Para PDFs grandes, considera procesarlos en chunks más pequeños

#### 3. Problemas de memoria con PDFs grandes
**Solución:**
- Procesa documentos grandes en secciones más pequeñas
- Aumenta la memoria disponible para el proceso Python

#### 4. El servidor no aparece en Claude Desktop
**Solución:**
- Verifica la sintaxis del archivo `claude_desktop_config.json`
- Asegúrate de usar rutas absolutas, no relativas
- Reinicia Claude Desktop completamente

### Comandos de Diagnóstico

```bash
# Verificar instalación de uv
uv --version

# Verificar Tesseract
tesseract --version

# Probar el servidor directamente
uv run python pdf_processor_server.py

# Verificar dependencias
uv run python -c "import mcp; import fitz; import pytesseract; print('Todas las dependencias importadas correctamente!')"
```

### Logs y Depuración

El servidor proporciona logging detallado:

```python
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Los logs aparecen en la consola al ejecutar el servidor
logger.info(f"Cargados {len(prompts_data)} prompts desde {PROMPTS_FILE}")
logger.error(f"Error procesando PDF: {e}")
```

### Verificación de Claude Desktop

Para verificar que Claude Desktop esté recogiendo el servidor:

1. **Busca el ícono de herramientas** 🔨 en la interfaz
2. **Verifica los logs** de Claude Desktop:
   
   **macOS:**
   ```bash
   tail -f ~/Library/Logs/Claude/mcp*.log
   ```
   
   **Windows:**
   ```cmd
   type "%APPDATA%\Claude\logs\mcp*.log"
   ```

## 📚 Mejores Prácticas con LLMs

### 1. Iteración Incremental
- Comienza con funcionalidades básicas
- Agrega características una por una
- Prueba cada componente antes de continuar

### 2. Documentación Clara
- Mantén docstrings detallados en todas las funciones
- Comenta el código complejo
- Documenta las decisiones de diseño

### 3. Manejo de Errores Robusto
- Implementa try-catch en todas las operaciones críticas
- Proporciona mensajes de error claros
- Registra errores para depuración

### 4. Seguridad
- Valida todas las entradas
- Limita el acceso a archivos según sea necesario
- Maneja datos sensibles apropiadamente

## 🔄 Próximos Pasos

Después de que Claude te ayude a construir tu servidor:

1. **Revisa el código generado** cuidadosamente
2. **Prueba el servidor** con la herramienta MCP Inspector
3. **Conéctalo a Claude Desktop** u otros clientes MCP
4. **Itera basándose en el uso real** y comentarios

### Extensiones Sugeridas

- **Soporte para más formatos**: Word, PowerPoint, Excel
- **Análisis de sentimientos**: Análisis emocional del contenido
- **Extracción de entidades**: Identificación de nombres, fechas, lugares
- **Resúmenes automáticos**: Generación de resúmenes sin prompts
- **Traducción**: Soporte multiidioma

## 📞 Soporte

¿Necesitas más orientación? Simplemente haz preguntas específicas a Claude sobre:
- Implementación de características MCP
- Solución de problemas que surjan
- Optimización de rendimiento
- Mejores prácticas de seguridad

¡Recuerda que Claude puede ayudarte a modificar y mejorar tu servidor a medida que los requisitos cambien con el tiempo!

---
