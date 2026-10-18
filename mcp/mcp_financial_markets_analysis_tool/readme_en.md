# Financial Analysis MCP Server

A comprehensive Model Context Protocol (MCP) server that provides advanced technical analysis tools for financial markets. This server integrates with Claude Desktop and includes a command-line interface for sophisticated trading strategy analysis, performance backtesting, and market scanning capabilities.

## Overview

The Financial Analysis MCP Server implements five distinct technical analysis strategies with comprehensive performance backtesting capabilities. The system provides both an MCP server for Claude Desktop integration and a standalone command-line tool for direct analysis execution.

### Core Trading Strategies

**Bollinger Z-Score Analysis**
Mean reversion strategy using statistical Z-scores to identify overbought and oversold conditions within Bollinger Band channels.

**Bollinger-Fibonacci Strategy**
Support and resistance analysis combining Bollinger Bands with Fibonacci retracements to identify key price levels and reversal points.

**MACD-Donchian Combined Strategy**
Momentum and breakout strategy utilizing Moving Average Convergence Divergence (MACD) indicators with Donchian channel breakout signals.

**Connors RSI + Z-Score Strategy**
Short-term momentum analysis with mean reversion components, combining Connors RSI methodology with statistical Z-score calculations.

**Dual Moving Average Strategy**
Trend-following strategy implementing exponential moving average crossovers with configurable periods for trend identification.

### Analysis Capabilities

**Performance Backtesting**
Comprehensive historical performance analysis comparing strategy returns against buy-and-hold baselines with detailed metrics including Sharpe ratios, maximum drawdown, and win rates.

**Market Scanner**
Multi-symbol analysis capability for simultaneous evaluation of multiple securities with ranking and comparative analysis across all implemented strategies.

**Risk Assessment**
Advanced risk metrics including volatility analysis, drawdown calculations, and position sizing recommendations based on historical performance data.

**Signal Generation**
Real-time buy, sell, and hold recommendations with confidence scoring based on current market conditions and historical strategy performance.

## Prerequisites

- Python 3.11 or higher
- UV package manager for dependency management
- Claude Desktop with MCP support (for server integration)
- Internet connectivity for Yahoo Finance data access
- OpenAI API key (for CLI tool functionality)

## Installation

### Server Installation

```bash
# Create project directory
mkdir financial-mcp-server
cd financial-mcp-server

# Initialize with uv
uv init .

# Install core dependencies
uv add mcp fastmcp yfinance pandas numpy

# Install additional analysis dependencies
uv add python-docx docx2pdf scipy scikit-learn
```

### CLI Tool Installation

```bash
# Install additional CLI dependencies
pip install openai python-dotenv

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenAI API key
```

## Project Structure

```
financial-mcp-server/
├── server/
│   ├── main.py                     # Main MCP server entry point
│   ├── strategies/                 # Trading strategy modules
│   │   ├── bollinger_zscore.py     # Z-Score mean reversion
│   │   ├── bollinger_fibonacci.py  # Bollinger-Fibonacci strategy
│   │   ├── macd_donchian.py       # MACD-Donchian momentum
│   │   ├── connors_zscore.py      # Connors RSI analysis
│   │   ├── dual_moving_average.py # EMA crossover strategy
│   │   ├── performance_tools.py   # Performance comparison tools
│   │   ├── comprehensive_analysis.py # Multi-strategy analysis
│   │   └── unified_market_scanner.py # Market scanning tools
│   └── utils/
│       └── yahoo_finance_tools.py  # Market data utilities
├── stock_analyzer.py              # CLI application
├── analyze.py                     # Simple CLI wrapper
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
└── tests/                         # Test suite
```

## Claude Desktop Configuration

Add the following to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "finance-tools": {
      "command": "uv",
      "args": ["--directory", "/path/to/financial-mcp-server", "run", "python", "server/main.py"],
      "env": {}
    }
  }
}
```

## Command Line Interface Usage

### Basic Analysis

Execute comprehensive technical analysis on individual securities:

```bash
# Analyze Apple stock
python stock_analyzer.py AAPL

# Analyze Microsoft with verbose output
python stock_analyzer.py MSFT --verbose

# Using simplified wrapper
python analyze.py TSLA
```

### CLI Features

**Symbol Validation**
Automatic validation of ticker symbols against Yahoo Finance data availability before analysis execution.

**Comprehensive Reporting**
Generated markdown reports include executive summaries, individual strategy performance metrics, comparative analysis tables, and investment recommendations.

**Error Handling**
Robust error handling for network connectivity issues, invalid symbols, and partial analysis completion scenarios.

**OpenAI Integration**
The CLI tool utilizes OpenAI models to orchestrate analysis execution and provide intelligent interpretation of results.

### CLI Options

```bash
stock_analyzer.py [-h] [--verbose] symbol

positional arguments:
  symbol         Yahoo Finance stock symbol for analysis

optional arguments:
  -h, --help     Show help message and exit
  --verbose, -v  Enable detailed logging output
```

### Environment Configuration

Create a `.env` file with required API credentials:

```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
```

## Technical Architecture

### MCP Integration

The server utilizes the FastMCP framework for Claude Desktop integration:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("finance tools", "1.0.0")

# Register strategy tools
register_bollinger_fibonacci_tools(mcp)
register_macd_donchian_tools(mcp)
register_connors_zscore_tools(mcp)
register_dual_ma_tools(mcp)
register_bollinger_zscore_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport='stdio')
```

### Strategy Implementation Pattern

Each trading strategy follows a standardized implementation pattern:

1. **Data Acquisition** - Yahoo Finance API integration for historical price data
2. **Indicator Calculation** - Technical analysis computations using pandas and numpy
3. **Signal Generation** - Buy, sell, and hold recommendation logic
4. **Performance Backtesting** - Historical strategy validation with comprehensive metrics
5. **Report Generation** - Structured markdown output with analysis summaries

### Performance Metrics

The system implements comprehensive performance evaluation:

```python
def calculate_strategy_performance_metrics(signals_data, signal_column):
    # Calculate total returns, annualized returns, volatility
    # Generate Sharpe ratios, maximum drawdown analysis
    # Compute win rates and average holding periods
    # Compare against buy-and-hold baseline performance
    return performance_metrics
```

## Configuration Parameters

### Time Period Options

Valid analysis periods: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

### Strategy Parameters

**Bollinger Bands Configuration**
- Window period: 20 days (default)
- Standard deviations: 2 (default)

**MACD Parameters**
- Fast period: 12 days
- Slow period: 26 days  
- Signal period: 9 days

**Moving Average Configuration**
- Short period: 50 days
- Long period: 200 days
- Type: Simple Moving Average (SMA) or Exponential Moving Average (EMA)

**Z-Score Calculation**
- Window for mean and standard deviation: 20 days (default)

### Output Format Options

**Detailed Analysis**
Complete analysis with all performance metrics, strategy breakdowns, and comprehensive recommendations.

**Summary Format**
Condensed overview focusing on key findings and primary investment recommendations.

**Executive Summary**
High-level strategic overview designed for executive decision-making processes.

## Testing Suite

### Test Categories

**Unit Testing**
Comprehensive unit tests covering individual strategy calculations, data validation, and utility functions.

**Integration Testing**
End-to-end workflow testing including MCP server connectivity, CLI functionality, and report generation.

**Performance Testing**
Timing and memory usage validation for large dataset processing and multiple symbol analysis.

### Test Execution

```bash
# Run complete test suite
python -m pytest tests/ -v

# Execute specific test categories
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests
pytest -m performance    # Performance tests
```

## Risk Disclaimers

**Important Notice:** This software is provided for educational and informational purposes only.

**Financial Risk Warning**
All analysis results should be independently verified before making investment decisions. Past performance does not guarantee future results. All trading and investment activities involve substantial risk of financial loss.

**Technical Limitations**
Technical analysis has inherent limitations and may produce false signals. Strategy effectiveness varies across different market conditions and asset classes.

**Data Accuracy**
Market data is sourced from Yahoo Finance and may contain delays, inaccuracies, or gaps. Users should verify data accuracy independently.

## Troubleshooting

### Common Configuration Issues

**MCP Server Connection Problems**
Verify server script paths in Claude Desktop configuration. Ensure Python and UV environments are properly configured with all required dependencies installed.

**Performance Optimization**
Initial data downloads may require 30+ seconds for completion. Subsequent analyses typically execute faster due to data caching. Consider shorter time periods for improved analysis speed.

**Data Access Issues**
Verify ticker symbols are correctly formatted and actively traded on supported exchanges. Confirm internet connectivity for Yahoo Finance API access. Some analysis tools require minimum historical data periods.

### Debug Mode

Enable detailed logging for troubleshooting:

```python
import sys
print(f"Analyzing {symbol}...", file=sys.stderr)
```

## Contributing

### Adding New Strategies

1. Create new strategy module in `server/strategies/`
2. Implement core analysis functions following established patterns
3. Add comprehensive performance backtesting capabilities
4. Register strategy with main MCP server
5. Include thorough documentation and test coverage

### Extending Analysis Capabilities

- Implement additional technical indicators
- Develop enhanced risk assessment metrics
- Create sector-specific analysis tools
- Improve report formatting and visualization

## Technical Resources

### Model Context Protocol Documentation
- [Official MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Concepts and Architecture](https://modelcontextprotocol.io/docs/concepts/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)

### Technical Analysis References

**Bollinger Bands**
Statistical price channels utilizing moving averages and standard deviations for volatility analysis and mean reversion identification.

**MACD (Moving Average Convergence Divergence)**
Momentum oscillator comparing exponential moving averages to identify trend changes and momentum shifts.

**Fibonacci Retracements**
Technical analysis tool using mathematical ratios to identify potential support and resistance levels based on previous price movements.

**Connors RSI**
Short-term momentum indicator combining traditional RSI with streak analysis and percentile ranking for enhanced mean reversion signals.

**Donchian Channels**
Breakout analysis system using highest high and lowest low values over specified periods to identify potential breakout opportunities.

### Market Data Sources

**Yahoo Finance Integration**
Free access to historical and real-time market data covering global equities, indices, currencies, and commodities with comprehensive API access.

**Data Coverage Limitations**
Subject to Yahoo Finance API rate limits and data availability constraints. Some international markets may have limited historical data coverage.

## License

This project is provided for educational purposes. Users must comply with:
- Yahoo Finance Terms of Service for market data usage
- OpenAI Terms of Service for API integration
- Anthropic Terms of Service for Claude API usage
- Applicable local regulations regarding financial analysis tools

---

**Technology Stack:** Python, FastMCP, Yahoo Finance API, OpenAI API, Claude Desktop
**Version:** 1.0.0