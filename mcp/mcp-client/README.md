# MCP Client with Financial Analysis Tools

A powerful Model Context Protocol (MCP) client implementation that bridges Claude AI with external tools and data sources, featuring specialized financial analysis capabilities for technical trading indicators.

## 🚀 Overview

This repository demonstrates a complete MCP ecosystem with:
- **Multi-language server support** (Python + Node.js)
- **Specialized financial analysis tools** with 8+ technical indicators
- **Document processing capabilities** (Word, PDF)
- **Web search integration** (Google Custom Search)
- **Production-ready architecture** with comprehensive error handling

## 📋 Table of Contents

- [What is MCP?](#what-is-mcp)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Available Tools](#available-tools)
- [Technical Analysis Capabilities](#technical-analysis-capabilities)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🔍 What is MCP?

Model Context Protocol (MCP) is an open standard that enables seamless integration between AI applications and external data sources and tools. It creates a bridge between Large Language Models (LLMs) like Claude and various services, allowing AI assistants to:

- Access real-time data from APIs and databases
- Execute functions and tools safely
- Interact with external systems efficiently
- Maintain conversation context across tool calls

```
┌─────────────┐    MCP Protocol      ┌─────────────┐
│ MCP Client  │ ←→ (JSON-RPC 2.0) ←→ │ MCP Server  │
│ (+ Claude)  │                      │ (+ Tools)   │
└─────────────┘                      └─────────────┘
```

## ✨ Features

### 🤖 AI Integration
- **Claude Sonnet 4** integration for intelligent tool orchestration
- **Conversation memory** management across tool calls
- **Automatic tool discovery** and schema validation

### 📊 Financial Analysis Suite
- **8+ Technical Indicators**: Bollinger Bands, MACD, Donchian Channels, Fibonacci Retracements, RSI variants
- **Multi-timeframe Analysis**: Support for 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y periods
- **Combined Scoring Systems**: Weighted indicator combinations for trading signals
- **Real-time Yahoo Finance Data**: Live market data integration

### 🔧 Multi-Server Architecture
- **Python Servers**: Financial analysis, document processing
- **Node.js Servers**: Web search, data fetching
- **Modular Design**: Easy to add new servers and capabilities

### 📄 Document Processing
- **Word Document Creation**: Generate reports from analysis results
- **PDF Conversion**: Automated document format conversion
- **Template Support**: Structured document generation

### 🌐 Web Integration
- **Google Custom Search**: Web search capabilities with content extraction
- **URL Content Fetching**: Read and parse webpage content
- **Search Result Processing**: Intelligent content summarization

## 🏗️ Architecture

### Transport Layer
- **stdio**: Standard input/output (primary transport)
- **SSE**: Server-Sent Events (web-based alternative)
- **JSON-RPC 2.0**: Communication protocol

### Component Structure
```
mcp-client/
├── client.py              # Main MCP client implementation
├── server/                 # Financial analysis MCP server
│   ├── main.py            # Financial tools server
│   ├── utils/             # Financial calculation utilities
│   └── mcp_server_sse.py  # Web-based SSE server
├── index.js               # Google Search MCP server
└── examples/              # Analysis reports and documentation
```

## ⚙️ Installation

### Prerequisites
- **Python 3.11+** with `uv` package manager
- **Node.js 17+** with `npm`
- **API Keys**: Anthropic, Google Custom Search

### Quick Start

1. **Clone and Setup Python Environment**
```bash
git clone <repository-url>
cd mcp-client

# Install dependencies
uv sync
```

2. **Install Node.js Dependencies** (for search server)
```bash
npm install axios cheerio @modelcontextprotocol/sdk
```

3. **Configure Environment Variables**
```bash
# Create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
CLAUDE_MODEL=claude-sonnet-4-20250514
EOF
```

4. **Test Installation**
```bash
# Test financial analysis server
uv run client.py server/main.py

# Test search server (from separate terminal)
uv run client.py index.js
```

## 🎯 Usage Examples

### Financial Analysis Workflow

```bash
# Start financial analysis session
uv run client.py server/main.py

# Example queries:
Query: Calculate Tesla's Bollinger Z-Score for the last 20 days
Query: Analyze AAPL using MACD-Donchian combined strategy  
Query: Generate a comprehensive technical analysis report for MSFT using all indicators
```

### Web Search and Research

```bash
# Start search server session  
uv run client.py index.js

Query: Search for recent quantum machine learning libraries in Python
Query: Create a markdown report of quantum ML tools with summaries and URLs
Query: Read content from https://example.com/article and summarize key points
```

### Document Generation Workflow

```bash
# Start Word document server (requires separate installation)
uv run client.py path/to/word_document_server/main.py

Query: Create a professional report from my Tesla analysis and convert to PDF
Query: Generate a technical analysis document with tables and save as QML.docx
```

## 🛠️ Available Tools

### Financial Analysis Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `calculate_bollinger_z_score` | Mean reversion analysis using Bollinger Bands | `symbol`, `period` |
| `calculate_macd_score_tool` | MACD momentum analysis with 3 components | `symbol`, `period`, `fast_period`, `slow_period`, `signal_period` |
| `calculate_donchian_channel_score_tool` | Price position within Donchian channels | `symbol`, `period`, `window` |
| `calculate_bollinger_fibonacci_score` | Combined Bollinger-Fibonacci strategy | `symbol`, `period`, `window`, `fibonacci_levels`, `num_days` |
| `calculate_combined_score_macd_donchian` | Weighted MACD + Donchian analysis | `symbol`, `period`, `window` |
| `calculate_connors_rsi_score_tool` | Advanced RSI with streak and rank components | `symbol`, `period`, `rsi_period`, `streak_period`, `rank_period` |
| `calculate_zscore_indicator_tool` | Z-Score for mean reversion signals | `symbol`, `period`, `window` |
| `calculate_combined_connors_zscore_tool` | Momentum + mean reversion combined analysis | `symbol`, `period`, `connors_weight`, `zscore_weight` |

### Search and Web Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `search` | Google Custom Search with result filtering | `query`, `num` |
| `read_webpage` | Extract and clean webpage content | `url` |

## 📈 Technical Analysis Capabilities

### Supported Indicators

1. **Bollinger Bands Z-Score**
   - Measures price position relative to statistical bands
   - Range: -3 to +3 (standard deviations)
   - Use: Mean reversion signals

2. **MACD (Moving Average Convergence Divergence)**
   - Three-component scoring: Signal line, zero line, histogram
   - Range: -100 to +100
   - Use: Trend and momentum analysis

3. **Donchian Channels**
   - Price position within highest/lowest range
   - Components: Position (50%), direction (30%), width (20%)
   - Use: Breakout and trend analysis

4. **Bollinger-Fibonacci Combined**
   - Multi-component strategy with 4 factors
   - Components: Band position, volatility, Fibonacci levels, momentum
   - Use: Comprehensive entry/exit signals

5. **Connors RSI**
   - Enhanced RSI with price streaks and ranking
   - Components: Price RSI, streak RSI, percent rank
   - Use: Overbought/oversold conditions

6. **Z-Score Indicator**
   - Statistical mean reversion analysis
   - Rolling window standard deviation calculation
   - Use: Statistical arbitrage opportunities

### Example Analysis Output

```
Symbol: TSLA, Period: 6mo
Latest combined score: 22.06
Latest MACD score: 9.00
Latest Donchian score: 35.12
Trading Signal: Neutral with Bullish Bias
```

### Signal Interpretation

| Score Range | Signal | Action |
|-------------|---------|---------|
| +75 to +100 | Strong Buy | High conviction long |
| +50 to +75 | Buy | Moderate long position |
| +25 to +50 | Weak Buy | Small long or wait |
| -25 to +25 | Neutral | Hold current positions |
| -50 to -25 | Weak Sell | Reduce longs or small short |
| -75 to -50 | Sell | Close longs or moderate short |
| -100 to -75 | Strong Sell | Strong short signal |

## ⚙️ Configuration

### Environment Variables

```bash
# Required for AI functionality
ANTHROPIC_API_KEY=sk-ant-...           # Claude API access
CLAUDE_MODEL=claude-sonnet-4-20250514  # Model specification

# Required for search functionality  
GOOGLE_API_KEY=AIza...                 # Google API key
GOOGLE_SEARCH_ENGINE_ID=017...         # Custom search engine ID

# Optional for enhanced functionality
BRAVE_API_KEY=BSA...                   # Alternative search API
```

### Server Configuration

Financial analysis server supports both stdio and SSE transports:

```python
# stdio transport (default)
uv run client.py server/main.py

# SSE transport for web integration
python server/mcp_server_sse.py  # Runs on port 8100
```

## 🔧 Troubleshooting

### Common Issues

1. **Connection Timeouts**
   - First responses may take 30+ seconds (normal for initialization)
   - Subsequent responses are typically faster
   - Don't interrupt during server startup

2. **API Rate Limits**
   - Yahoo Finance: No explicit limits but respect fair usage
   - Google Search: 100 queries/day free tier
   - Anthropic: Based on your plan limits

3. **Data Quality Issues**
   - Some symbols may have limited historical data
   - Fibonacci calculations require sufficient swing points
   - Check for weekends/holidays affecting latest data

4. **Environment Setup**
   ```bash
   # Verify Python version
   python --version  # Should be 3.11+
   
   # Check uv installation
   uv --version
   
   # Validate environment variables
   echo $ANTHROPIC_API_KEY
   ```

### Debug Mode

Enable detailed logging:

```python
# In client.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

### Adding New Financial Indicators

1. **Implement calculation function** in `server/utils/yahoo_finance_tools.py`
2. **Create MCP tool wrapper** in `server/main.py`
3. **Add comprehensive docstring** with parameters and interpretation
4. **Test with various symbols and timeframes**

### Adding New Servers

1. **Create server script** following MCP SDK patterns
2. **Implement tool handlers** with proper error handling
3. **Update client configuration** for new server support
4. **Document new capabilities** in README

### Code Style

- **Python**: Follow PEP 8, use type hints
- **JavaScript**: Use modern ES6+ syntax, async/await
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Graceful degradation and informative messages

## 📊 Example Analyses

The repository includes several complete technical analysis reports:

- **Tesla (TSLA)**: [`4_indicators_tesla_analisys.md`](4_indicators_tesla_analisys.md) - Comprehensive 4-strategy analysis
- **Apple (AAPL)**: [`technical_analisys_APPL.md`](technical_analisys_APPL.md) - Multi-indicator assessment  
- **Microsoft (MSFT)**: [`technical_analisys_MSFT.md`](technical_analisys_MSFT.md) - Trading strategy recommendations

## 📚 Additional Resources

- **MCP Documentation**: [Model Context Protocol Official Docs](https://modelcontextprotocol.io/docs)
- **Yahoo Finance API**: [yfinance Python Package](https://pypi.org/project/yfinance/)
- **Technical Analysis**: [TA-Lib Documentation](https://ta-lib.org/)
- **Anthropic Claude**: [Claude API Documentation](https://docs.anthropic.com/)

## 📄 License

This project is open source. Please refer to the LICENSE file for details.

## 🎯 Next Steps

- [ ] Add cryptocurrency analysis support
- [ ] Implement backtesting framework
- [ ] Create web dashboard for visualization
- [ ] Add alert system for signal notifications
- [ ] Expand to forex and commodities markets

---

**Built with ❤️ using Model Context Protocol and Claude AI**