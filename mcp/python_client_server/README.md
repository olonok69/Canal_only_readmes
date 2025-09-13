# MCP Python Financial Analysis Server

A comprehensive Model Context Protocol (MCP) implementation featuring financial analysis tools, server-sent events (SSE) communication, and an intelligent chatbot client. This project demonstrates the power of MCP as the "USB-C for AI integrations" by providing standardized access to financial data and analysis capabilities.

## 🌟 Overview

The Model Context Protocol (MCP) is an open standard developed by Anthropic that standardizes how AI applications connect with external data sources, tools, and systems. This project implements a complete MCP ecosystem with:

- **Financial Analysis Server**: MCP server exposing sophisticated financial analysis tools
- **SSE Transport**: Real-time bidirectional communication using Server-Sent Events
- **Intelligent Client**: AI-powered chatbot that can discover and use financial tools
- **Multiple Indicators**: MACD, Donchian Channels, Bollinger Bands, and Fibonacci analysis

## 🚀 Key Features

### Financial Analysis Tools
- **MACD Score Calculator**: Moving Average Convergence Divergence analysis with component scoring
- **Donchian Channel Analysis**: Price position and channel direction analysis
- **Combined MACD-Donchian Score**: Integrated momentum and range indicators
- **Bollinger-Fibonacci Strategy**: Advanced technical analysis combining multiple indicators
- **Bollinger Z-Score**: Statistical price position analysis

### MCP Architecture Components
- **Server**: Exposes financial tools through standardized MCP protocol
- **Resources**: Structured data access for configuration and app information
- **Tools**: Executable functions for AI-driven financial analysis
- **Prompts**: Reusable interaction templates for common analysis patterns
- **Context**: Intelligent information management for LLM interactions

### Transport & Communication
- **SSE (Server-Sent Events)**: Real-time bidirectional communication
- **HTTP Transport**: RESTful API endpoints for health checks and messaging
- **JSON-RPC 2.0**: Standard protocol for MCP communication

## 📁 Project Structure

```
mcp/python_client_server/
├── main.py                              # Entry point to run the server
├── server.py                           # Shared MCP server instance
├── mcp_server_sse.py                   # FastAPI server with SSE transport
├── mcp_client_sse_chat.py              # Basic chatbot client
├── mcp_client_sse_chat_improved.py     # Enhanced chatbot with better parsing
├── tools/                              # Financial analysis tools
│   ├── bollinger_bands_score.py        # Bollinger Z-Score calculator
│   ├── bollinger_fibonacci_tools.py    # Combined Bollinger-Fibonacci strategy
│   ├── macd_donchian_combined_score.py # MACD and Donchian analysis
│   ├── csv_tools.py                    # CSV file processing tools
│   └── parquet_tools.py                # Parquet file processing tools
├── utils/                              # Utility functions
│   ├── yahoo_finance_tools.py          # Yahoo Finance data processing
│   └── file_reader.py                  # File reading utilities
├── keys/                               # Configuration and credentials
│   └── .env                           # Environment variables
├── data/                               # Data files
├── pyproject.toml                      # Project dependencies
└── README.md                           # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Setup Instructions

1. **Install uv package manager**:
   ```bash
   # Linux/Mac
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Clone and setup the project**:
   ```bash
   git clone <repository-url>
   cd mcp/python_client_server
   ```

3. **Create virtual environment**:
   ```bash
   uv venv
   
   # Activate environment
   # Linux/Mac:
   source .venv/bin/activate
   
   # Windows:
   .venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   uv add "mcp[cli]" pandas pyarrow yfinance langchain langchain_mcp_adapters langgraph langchain_google_genai google-generativeai python-dotenv fastapi loguru numpy openai
   ```

5. **Setup environment variables**:
   ```bash
   # Create keys/.env file with your API keys
   echo "OPENAI_API_KEY=your_openai_api_key_here" > keys/.env
   ```

## 🚀 Usage

### Running the MCP Server

Start the financial analysis server with SSE transport:

```bash
python mcp_server_sse.py
```

The server will start on `http://localhost:8100` with the following endpoints:
- `GET /sse` - Server-Sent Events connection
- `POST /messages/` - MCP message handling
- `GET /health` - Health check

### Using the Interactive Client

Start the intelligent chatbot client:

```bash
# Basic client
python mcp_client_sse_chat.py

# Enhanced client (recommended)
python mcp_client_sse_chat_improved.py
```

### Example Queries

Try these example queries with the chatbot:

```
"What is the MACD score for AAPL over the last year?"

"Calculate the Bollinger Z-score for TSLA with a 20-day period"

"Give me a combined MACD-Donchian analysis for MSFT using 6 months of data"

"Analyze NVDA using the Bollinger-Fibonacci strategy for the last 3 days"

"What's the recommendation for buying or selling AAPL based on technical indicators?"
```

## 🔧 Core Components Explained

### MCP Server Implementation

The server uses FastMCP for simplified MCP implementation:

```python
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP(name="Finance Tools")

# Define a financial analysis tool
@mcp.tool()
def calculate_macd_score(symbol: str, period: str = "1y") -> str:
    """Calculate MACD score for a given symbol"""
    # Implementation here
    return f"MACD analysis for {symbol}"
```

### SSE Transport Layer

Server-Sent Events enable real-time bidirectional communication:

```python
from mcp.server.sse import SseServerTransport

transport = SseServerTransport("/messages/")

async def handle_sse(request):
    async with transport.connect_sse(request.scope, request.receive, request._send) as (in_stream, out_stream):
        await mcp._mcp_server.run(in_stream, out_stream, mcp._mcp_server.create_initialization_options())
```

### Intelligent Client Architecture

The client implements several specialized components:

- **LLMClient**: Manages interactions with OpenAI's GPT models
- **PromptGenerator**: Creates specialized prompts for tool selection and response processing
- **ResponseParser**: Handles JSON parsing and error recovery
- **AgentProcessor**: Orchestrates the tool discovery and execution workflow

## 📊 Financial Analysis Tools

### MACD Score Calculator
Calculates a comprehensive MACD score (-100 to +100) combining:
- **MACD Line vs Signal Line (40%)**: Momentum direction
- **MACD Line vs Zero (30%)**: Trend strength
- **Histogram Momentum (30%)**: Acceleration/deceleration

### Donchian Channel Analysis
Evaluates price position within Donchian Channels:
- **Price Position (50%)**: Location within channel bands
- **Channel Direction (30%)**: Trend identification
- **Channel Width (20%)**: Volatility assessment

### Bollinger-Fibonacci Strategy
Advanced multi-indicator analysis:
- **Bollinger Band Position (30%)**: Price relative to bands
- **Volatility Assessment (15%)**: Band width and changes
- **Fibonacci Level Interaction (35%)**: Key support/resistance levels
- **Price Momentum (20%)**: RSI-like momentum indicator

### Combined Scoring System
All tools provide standardized scoring with clear trading signals:
- **+75 to +100**: Strong Buy
- **+50 to +75**: Buy
- **+25 to +50**: Weak Buy
- **-25 to +25**: Neutral (Hold)
- **-50 to -25**: Weak Sell
- **-75 to -50**: Sell
- **-100 to -75**: Strong Sell

## 🔌 MCP Protocol Details

### Resources
Structured data endpoints for configuration:

```python
@mcp.resource("config://app-version")
def get_app_version() -> str:
    return "v2.1.0"

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}!"
```

### Tools
Executable functions for AI analysis:

```python
@mcp.tool()
def calculate_z_score(symbol: str, period: int = 20) -> str:
    """Calculate Bollinger Z-Score for technical analysis"""
    # Implementation
    return analysis_result
```

### Prompts
Reusable interaction templates:

```python
@mcp.prompt()
def analyze_stock(symbol: str) -> str:
    return f"Please analyze {symbol} using available technical indicators"
```

## 🤖 AI Integration

The project demonstrates how MCP enables seamless AI integration:

1. **Tool Discovery**: AI automatically discovers available financial tools
2. **Intelligent Selection**: GPT-4o-mini selects appropriate tools based on user queries
3. **Parameter Extraction**: Natural language queries are converted to structured tool calls
4. **Result Interpretation**: Tool responses are formatted into user-friendly explanations
5. **Multi-Tool Workflows**: Complex analyses can chain multiple tools together

## 🔧 Configuration

### Environment Variables
Create `keys/.env` with:

```bash
OPENAI_API_KEY=your_openai_api_key_here
# Add other API keys as needed
```

### Server Configuration
Modify `mcp_server_sse.py` to customize:
- Port number (default: 8100)
- Available tools
- Data sources
- Analysis parameters

## 🏗️ Architecture Benefits

### Standardized Integration
- **Universal Protocol**: One protocol for all AI-tool integrations
- **Interoperability**: Tools work across different AI models and platforms
- **Scalability**: Easy to add new tools and data sources

### Security & Control
- **User Authorization**: Tools require user permission before execution
- **Data Isolation**: Each server maintains its own data context
- **Audit Trail**: All tool calls are logged and traceable

### Developer Experience
- **Simple Implementation**: FastMCP reduces boilerplate code
- **Type Safety**: Automatic schema generation from Python type hints
- **Error Handling**: Built-in error recovery and validation

## 🔮 Future Enhancements

### Planned Features
- **Portfolio Analysis**: Multi-asset portfolio optimization tools
- **Risk Management**: VaR, stress testing, and risk metrics
- **Machine Learning**: Predictive models and pattern recognition
- **Real-time Data**: Live market data feeds and alerts
- **Backtesting**: Historical strategy performance analysis

### Integration Opportunities
- **Database Connectivity**: PostgreSQL, MongoDB MCP servers
- **Cloud Services**: AWS, GCP, Azure integrations
- **Trading Platforms**: Broker API connections
- **News & Sentiment**: Financial news analysis tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your MCP tools or improvements
4. Include comprehensive tests
5. Submit a pull request

### Development Guidelines
- Follow Python type hints
- Use FastMCP decorators for tools/resources
- Include docstrings with parameter descriptions
- Add error handling for external API calls
- Test with multiple AI models

## 📚 Additional Resources

- [MCP Specification](https://modelcontextprotocol.io/docs)
- [FastMCP Documentation](https://github.com/pydantic/fastmcp)
- [Technical Analysis Indicators](https://www.investopedia.com/technical-analysis/)
- [Server-Sent Events Guide](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for developing the MCP standard
- [FastMCP](https://github.com/pydantic/fastmcp) for the Python implementation
- [Yahoo Finance](https://finance.yahoo.com/) for financial data
- [OpenAI](https://openai.com/) for GPT model integration

---

**The Model Context Protocol represents a fundamental shift in AI system interoperability. By providing a standardized way for AI models to access external data and functionality, MCP enables more context-aware, capable AI assistants while reducing integration complexity.**