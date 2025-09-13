# Building MCP Servers with LLMs: PDF Document Processor

A comprehensive guide to accelerate MCP server development using language models like Claude, with a practical example of PDF document processing.

## 📋 Table of Contents

- [Introduction](#introduction)
- [Building MCP with LLMs](#building-mcp-with-llms)
- [Practical Example: PDF Document Processor](#practical-example-pdf-document-processor)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)

## 🚀 Introduction

This guide will teach you how to use language models (LLMs) like Claude to accelerate the development of Model Context Protocol (MCP) servers. It includes a complete example of a server that processes PDF documents and applies custom prompts for analysis and summarization.

## 🤖 Building MCP with LLMs

### Why Use LLMs for MCP Development?

LLMs like Claude can significantly accelerate MCP server development by:
- Generating structured and functional code
- Explaining complex MCP protocol concepts
- Assisting with tool, resource, and prompt implementation
- Helping with debugging and optimization

### Preparing the Documentation

Before starting, gather the necessary documentation to help Claude understand MCP:

1. **Complete MCP Documentation**: Visit [https://modelcontextprotocol.io/llms-full.txt](https://modelcontextprotocol.io/llms-full.txt) and copy the full text
2. **SDK Documentation**: Navigate to the [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) or [Python SDK](https://github.com/modelcontextprotocol/python-sdk) repository
3. **Paste these documents** into your conversation with Claude

### Describing Your Server

Once you've provided the documentation, clearly describe to Claude what kind of server you want to build:

```
Build an MCP server that:
- Extracts content from PDF documents
- Applies OCR for scanned documents
- Offers tools for analysis with custom prompts
- Converts content to markdown format
- Manages a library of prompts for different analysis types
```

### Working with Claude

When working with Claude on MCP servers:

1. **Start with core functionality** first, then iterate to add more features
2. **Ask Claude to explain** any parts of the code you don't understand
3. **Request modifications** or improvements as needed
4. **Have Claude help you** test the server and handle edge cases

Claude can help implement all key MCP features:
- Resource management and exposure
- Tool definitions and implementations
- Prompt templates and handlers
- Error handling and logging
- Connection and transport setup

## 📄 Practical Example: PDF Document Processor

### Overview

Our example is a complete MCP server that demonstrates:

- **PDF Extraction**: Extracts text from regular PDF documents
- **OCR Support**: Processes scanned PDFs using optical character recognition
- **Custom Prompts**: Applies predefined templates for specific analysis
- **Markdown Output**: Generates well-formatted content
- **Prompt Management**: Lists and manages custom analysis prompts

### Server Architecture

```python
# Main structure using FastMCP
from mcp.server.fastmcp import FastMCP

# Initialize server
mcp = FastMCP("PDF Document Processor")

# Main tools
@mcp.tool()
async def extract_pdf_to_markdown(pdf_base64: str, filename: str = "document.pdf") -> str:
    """Extract PDF content and convert to markdown"""
    
@mcp.tool()
async def extract_scanned_pdf_to_markdown(pdf_base64: str, filename: str = "document.pdf") -> str:
    """Extract text from scanned PDFs using OCR"""

@mcp.tool()
async def apply_prompt_to_content(content: str, prompt_id: str) -> str:
    """Apply a specific prompt to extracted content"""
```

## 🛠 Installation

### Prerequisites

1. **Python 3.8+** is required
2. **Tesseract OCR** for scanned document processing

#### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-spa tesseract-ocr-eng
```

#### On macOS:
```bash
brew install tesseract tesseract-lang
```

#### On Windows:
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

### Installation with UV (Recommended)

#### Using PowerShell (Windows):
```powershell
.\install_windows_uv.ps1
```

#### Using Batch (Windows):
```cmd
install_windows_uv.bat
```

#### Manual Installation:

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create project
uv init pdf-processor-mcp
cd pdf-processor-mcp

# Install dependencies
uv add "mcp[cli]>=1.2.0"
uv add "PyMuPDF>=1.23.0"
uv add "pytesseract>=0.3.10"
uv add "Pillow>=10.0.0"
uv add "opencv-python>=4.8.0"
```

### Traditional Installation with pip

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Server Files

Copy these files to the project directory:
- `pdf_processor_server.py` - Main MCP server
- `prompts.json` - Custom prompts configuration

### 2. Claude Desktop Configuration

Add this server to your Claude Desktop configuration:

**macOS/Linux:**
```json
{
  "mcpServers": {
    "pdf-processor": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/DIRECTORY/pdf-processor-mcp",
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
        "C:\\ABSOLUTE\\PATH\\TO\\DIRECTORY\\pdf-processor-mcp\\pdf_processor_server.py"
      ],
      "cwd": "C:\\ABSOLUTE\\PATH\\TO\\DIRECTORY\\pdf-processor-mcp"
    }
  }
}
```

### 3. Prompts Configuration

The `prompts.json` file contains analysis templates:

```json
[
  {
    "id": "638f3f81-0082-4df9-929f-e7b120d4f954",
    "name_prompt": "Expert Report: Current State",
    "prompt": "Write an extensive report describing the patient's current medical condition...",
    "keywords": "state,current,limitations,sequelae"
  }
]
```

## 🎯 Usage

### Available Tools

#### 1. `list_prompts()`
Lists all available prompts with their IDs, names, and keywords.

#### 2. `extract_pdf_to_markdown(pdf_base64, filename)`
Extracts text content from PDFs and converts to markdown format.

#### 3. `extract_scanned_pdf_to_markdown(pdf_base64, filename)`
Extracts text from scanned PDFs using OCR.

#### 4. `get_prompt_by_id(prompt_id)`
Retrieves a specific prompt by its ID.

#### 5. `apply_prompt_to_content(content, prompt_id)`
Applies a specific prompt to extracted content for analysis.

#### 6. `process_pdf_with_prompt(pdf_base64, prompt_id, filename, use_ocr)`
Complete workflow: extracts PDF content and applies a prompt.

### Example Workflow

1. **Upload a PDF document** (converted to base64)
2. **List available prompts** to see analysis options
3. **Process the PDF** with a specific prompt:

```python
# Example using the complete workflow
result = await process_pdf_with_prompt(
    pdf_base64="<base64_content>",
    prompt_id="638f3f81-0082-4df9-929f-e7b120d4f954",
    filename="medical_report.pdf",
    use_ocr=False
)
```

### Using in Claude Desktop

Once configured, you'll see the tools icon 🔨 in Claude Desktop:

1. **Upload a PDF document**
2. **Ask**: "Can you extract the content from this PDF and apply the expert report prompt?"
3. **Claude will automatically use** the MCP server tools

## 🔧 Advanced Features

### Intelligent OCR Processing

The server automatically detects if a PDF needs OCR:

```python
def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF using PyMuPDF with OCR fallback"""
    doc = fitz.open(pdf_path)
    text = ""
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text()
        
        if page_text.strip():
            text += f"\n\n## Page {page_num + 1}\n\n{page_text}"
        else:
            # If no text found, page might be scanned
            ocr_text = extract_text_from_scanned_page(page)
            if ocr_text.strip():
                text += f"\n\n## Page {page_num + 1} (OCR)\n\n{ocr_text}"
```

### Dynamic Prompt Management

Prompts are dynamically loaded from `prompts.json`:

```python
def load_prompts():
    """Load prompts from JSON file"""
    global prompts_data
    try:
        if os.path.exists(PROMPTS_FILE):
            with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
                prompts_data = json.load(f)
            logger.info(f"Loaded {len(prompts_data)} prompts")
    except Exception as e:
        logger.error(f"Error loading prompts: {e}")
```

### Structured Markdown Output

Extracted content is automatically converted to well-formatted markdown:

```python
def convert_to_markdown(text: str) -> str:
    """Convert extracted text to markdown format"""
    if not text.strip():
        return "# Document\n\nNo text content could be extracted from this document."
    
    markdown = f"# Extracted Document Content\n\n{text}"
    
    # Clean up extra whitespace
    lines = markdown.split('\n')
    cleaned_lines = []
    
    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line or (cleaned_lines and cleaned_lines[-1].strip()):
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Tesseract not found
**Solution:**
- Ensure Tesseract OCR is properly installed and in your PATH
- On Windows, verify it was added to PATH during installation

#### 2. PDF processing errors
**Solution:**
- Check that the PDF file is not corrupted or password-protected
- For large PDFs, consider processing them in smaller chunks

#### 3. Memory issues with large PDFs
**Solution:**
- Process large documents in smaller sections
- Increase available memory for the Python process

#### 4. Server not showing up in Claude Desktop
**Solution:**
- Check the syntax of your `claude_desktop_config.json` file
- Make sure to use absolute paths, not relative ones
- Restart Claude Desktop completely

### Diagnostic Commands

```bash
# Check uv installation
uv --version

# Check Tesseract
tesseract --version

# Test server directly
uv run python pdf_processor_server.py

# Check dependencies
uv run python -c "import mcp; import fitz; import pytesseract; print('All dependencies imported successfully!')"
```

### Logging and Debugging

The server provides detailed logging:

```python
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Logs appear in console when running the server
logger.info(f"Loaded {len(prompts_data)} prompts from {PROMPTS_FILE}")
logger.error(f"Error processing PDF: {e}")
```

### Claude Desktop Verification

To verify that Claude Desktop is picking up the server:

1. **Look for the tools icon** 🔨 in the interface
2. **Check Claude Desktop logs**:
   
   **macOS:**
   ```bash
   tail -f ~/Library/Logs/Claude/mcp*.log
   ```
   
   **Windows:**
   ```cmd
   type "%APPDATA%\Claude\logs\mcp*.log"
   ```

## 📚 Best Practices with LLMs

### 1. Incremental Iteration
- Start with basic functionality
- Add features one by one
- Test each component before continuing

### 2. Clear Documentation
- Maintain detailed docstrings in all functions
- Comment complex code
- Document design decisions

### 3. Robust Error Handling
- Implement try-catch in all critical operations
- Provide clear error messages
- Log errors for debugging

### 4. Security
- Validate all inputs
- Limit file access as needed
- Handle sensitive data appropriately

## 🔄 Next Steps

After Claude helps you build your server:

1. **Review the generated code** carefully
2. **Test the server** with the MCP Inspector tool
3. **Connect it to Claude Desktop** or other MCP clients
4. **Iterate based on real usage** and feedback

### Suggested Extensions

- **Support for more formats**: Word, PowerPoint, Excel
- **Sentiment analysis**: Emotional analysis of content
- **Entity extraction**: Identification of names, dates, places
- **Automatic summaries**: Generation of summaries without prompts
- **Translation**: Multi-language support

## 📞 Support

Need more guidance? Simply ask Claude specific questions about:
- Implementing MCP features
- Troubleshooting issues that arise
- Performance optimization
- Security best practices

Remember that Claude can help you modify and improve your server as requirements change over time!

---

