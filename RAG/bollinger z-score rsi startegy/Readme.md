# Bollinger Bands and RSI Crossover Trading Strategy

A comprehensive quantitative trading system that combines Bollinger Bands and Relative Strength Index (RSI) indicators to generate automated buy/sell signals for financial securities. This implementation uses LangGraph to create an intelligent agent that analyzes market conditions and provides trading recommendations.

## Overview

The Bollinger Bands and RSI Crossover Trading Strategy is a technical analysis approach that identifies potential market reversal points and trend changes by monitoring price crossovers with Bollinger Bands and RSI overbought/oversold levels. The system aims to capture trading opportunities during market volatility while using RSI confirmation to improve signal reliability.

## Financial Techniques Implemented

### 1. Bollinger Bands

Bollinger Bands are a volatility-based technical indicator consisting of:
- **Middle Band**: Simple Moving Average (typically 20-period)
- **Upper Band**: Middle Band + (2 × Standard Deviation)
- **Lower Band**: Middle Band - (2 × Standard Deviation)

**Key Characteristics:**
- Bands expand during high volatility periods
- Bands contract during low volatility periods
- Price tends to bounce between the bands
- Breakouts often signal trend changes

### 2. Bollinger Z-Score

The Z-Score measures how many standard deviations the current price is from the moving average:

```
Z-Score = (Current Price - Moving Average) / Standard Deviation
```

**Interpretation Guidelines:**
- **Z-Score > +2**: Price is overbought (consider selling)
- **Z-Score < -2**: Price is oversold (consider buying)
- **Z-Score between -2 and +2**: Price is within normal trading range

### 3. Relative Strength Index (RSI)

RSI is a momentum oscillator that measures the speed and magnitude of price changes:

**Calculation Process:**
1. Calculate price changes: `Δ = Price(t) - Price(t-1)`
2. Separate gains and losses
3. Calculate average gain and average loss over the period
4. Compute Relative Strength: `RS = Average Gain / Average Loss`
5. Calculate RSI: `RSI = 100 - (100 / (1 + RS))`

**Standard Interpretation:**
- **RSI > 70**: Overbought condition (potential sell signal)
- **RSI < 30**: Oversold condition (potential buy signal)
- **RSI 30-70**: Neutral zone

### 4. Support and Resistance Levels

**Support Level**: A price level where buying interest prevents further decline
- Acts as a "floor" for price movement
- Historical level where price has bounced upward

**Resistance Level**: A price level where selling pressure prevents further rise
- Acts as a "ceiling" for price movement
- Historical level where price has been rejected downward

## Trading Signal Generation

### Buy Signals
The system generates buy signals when:
1. **RSI < 30** (oversold condition) AND
2. **Price near lower Bollinger Band** (Z-Score < -2)
3. **Optional**: Price touching key support level

### Sell Signals
The system generates sell signals when:
1. **RSI > 70** (overbought condition) AND
2. **Price near upper Bollinger Band** (Z-Score > +2)
3. **Optional**: Price near key resistance level

## System Architecture

### LangGraph Agent Implementation

The system uses LangGraph to create an intelligent trading agent with the following components:

**Tools Available:**
- `calculate_bollinger_z_score()`: Computes Bollinger Z-Score for any symbol
- `calculate_rsi_zscore()`: Calculates RSI values for any symbol

**Agent State Management:**
- Maintains conversation history
- Processes user requests for specific symbols
- Provides contextualized trading recommendations

**Decision Logic:**
The chatbot agent analyzes the calculated indicators and provides recommendations based on:
- Current Z-Score position relative to thresholds
- RSI overbought/oversold levels
- Combined signal strength
- Risk assessment considerations

## Installation and Setup

### Prerequisites
```bash
pip install -r requirements.txt
```

### Required Dependencies
- **Data Source**: `yfinance` for historical stock data
- **Analysis**: `pandas`, `numpy` for data manipulation
- **Visualization**: `plotly` for interactive charts
- **AI Framework**: `langchain`, `langgraph` for intelligent agent
- **LLM Integration**: `langchain-openai` for GPT models

### Environment Configuration
1. Set up API keys in `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

2. Configure Google Cloud credentials for Vertex AI (optional)

## Usage Examples

### Basic Signal Analysis
```python
# Calculate Bollinger Z-Score for Apple stock with 20-day period
result = calculate_bollinger_z_score("AAPL", period=20)

# Calculate RSI for Tesla with 14-day window
rsi_result = calculate_rsi_zscore("TSLA", period=20, window=14)
```

### Interactive Agent Queries
```python
# Get trading recommendation
message = graph.invoke({
    "messages": [
        ("user", "Recommend if buy or sell AAPL based on Bollinger Z-score within a 20-day period and RSI score with a window of 14 days")
    ]
}, config)
```

### Visualization
```python
# Generate comprehensive chart with signals
plot_bollinger_rsi_with_signals("AAPL", window=20, rsi_period=14)
```

## Key Features

### 1. Multi-Indicator Confirmation
- Combines trend-following (Bollinger Bands) with momentum (RSI)
- Reduces false signals through dual confirmation
- Accounts for both volatility and momentum conditions

### 2. Customizable Parameters
- Adjustable Bollinger Band periods (default: 20)
- Configurable RSI calculation window (default: 14)
- Flexible overbought/oversold thresholds

### 3. Visual Analysis
- Interactive Plotly charts showing:
  - Price action with Bollinger Bands
  - RSI oscillator with threshold lines
  - Buy/sell signal markers
  - Support/resistance levels

### 4. Intelligent Recommendations
- Natural language explanations of market conditions
- Risk-aware trading suggestions
- Context-sensitive analysis based on multiple timeframes

## Risk Considerations

### Strategy Limitations
1. **Lagging Indicators**: Both Bollinger Bands and RSI are based on historical data
2. **False Signals**: Markets can remain overbought/oversold longer than expected
3. **Trending Markets**: Mean-reversion strategies may underperform in strong trends
4. **Volatility Sensitivity**: Extreme market conditions can generate misleading signals

### Best Practices
1. **Combine with Trend Analysis**: Consider overall market direction
2. **Risk Management**: Always use stop-losses and position sizing
3. **Multiple Timeframes**: Confirm signals across different time horizons
4. **Market Context**: Consider fundamental factors and market sentiment
5. **Backtesting**: Test strategy performance on historical data before live trading

## Advanced Applications

### Portfolio Integration
- Apply signals across multiple securities
- Sector-based analysis and correlation consideration
- Risk-adjusted position sizing based on volatility

### Real-Time Monitoring
- Automated signal detection and alerting
- Integration with broker APIs for execution
- Performance tracking and strategy optimization

## Contributing

This implementation provides a foundation for:
- Extended backtesting frameworks
- Additional technical indicators integration
- Machine learning enhancement of signal generation
- Real-time trading system development

## Disclaimer

This tool is for educational and research purposes only. Trading financial securities involves substantial risk of loss. Past performance does not guarantee future results. Always consult with qualified financial advisors and conduct thorough research before making investment decisions.