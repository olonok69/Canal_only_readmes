# Bollinger Bands and Fibonacci Retracement Trading Strategy

A comprehensive technical analysis strategy that combines Bollinger Bands with Fibonacci retracement levels to generate precise trading signals with an advanced scoring system.

## Table of Contents
- [Overview](#overview)
- [Technical Indicators](#technical-indicators)
- [Strategy Implementation](#strategy-implementation)
- [Scoring System](#scoring-system)
- [Notebooks Overview](#notebooks-overview)
- [Usage Examples](#usage-examples)
- [Installation and Setup](#installation-and-setup)

## Overview

This repository contains three progressive implementations of a sophisticated trading strategy that combines two powerful technical analysis tools:

1. **Bollinger Bands** - For measuring volatility and identifying overbought/oversold conditions
2. **Fibonacci Retracements** - For identifying potential support and resistance levels

The strategy evolution spans three notebooks, from basic implementation to an advanced AI-powered trading assistant.

## Technical Indicators

### Bollinger Bands

Bollinger Bands consist of three components:
- **Middle Line**: Moving average (typically 20 periods)
- **Upper Band**: Moving average + (2 × standard deviation)
- **Lower Band**: Moving average - (2 × standard deviation)

**Key Metrics:**
- **%B Indicator**: Shows where price is relative to the bands
  - 0 = price at lower band
  - 0.5 = price at moving average  
  - 1 = price at upper band
  - >1 = price above upper band (overbought)
  - <0 = price below lower band (oversold)

- **Bollinger Bandwidth**: Measures volatility by calculating the distance between bands
  - High values = high volatility (widely separated bands)
  - Low values = low volatility (compressed bands)
  - Minimum values often precede strong directional movements

### Fibonacci Retracements

Fibonacci levels are horizontal lines indicating potential support and resistance areas:
- **0%** - Starting point of the move
- **23.6%** - Shallow retracement
- **38.2%** - Moderate retracement
- **50%** - Half retracement (not technically Fibonacci but widely used)
- **61.8%** - Golden ratio retracement
- **78.6%** - Deep retracement
- **100%** - Complete retracement

**Trend Interpretation:**
- **Uptrend**: Fibonacci levels act as support during pullbacks
- **Downtrend**: Fibonacci levels act as resistance during bounces

## Strategy Implementation

### Signal Generation Logic

**Buy Signals** are generated when:
1. Price crosses above the lower Bollinger Band (potential oversold bounce)
2. Price is within 2% of a Fibonacci support level
3. Confluence confirms higher probability of reversal

**Sell Signals** are generated when:
1. Price crosses below the upper Bollinger Band (potential overbought rejection)
2. Price is within 2% of a Fibonacci resistance level
3. Confluence confirms higher probability of reversal

### Swing Point Detection

The strategy identifies significant swing highs and lows using a configurable window (default 5-10 periods):
- **Swing High**: Price point higher than surrounding periods on both sides
- **Swing Low**: Price point lower than surrounding periods on both sides

These swing points determine the Fibonacci retracement calculation range.

## Scoring System

The advanced scoring system (introduced in v2 and v3) provides a comprehensive signal strength indicator ranging from -100 to +100.

### Signal Zones

| Score Range | Signal Category | Action |
|-------------|----------------|---------|
| +60 to +100 | **Strong Buy** | Enter long positions |
| +20 to +60 | **Moderate Buy** | Consider long positions |
| -20 to +20 | **Hold** | Maintain current position |
| -60 to -20 | **Moderate Sell** | Consider short positions |
| -100 to -60 | **Strong Sell** | Enter short positions |

### Score Components

The strategy score is a weighted combination of four key factors:

#### 1. Bollinger Band Position (30% weight)
- Based on the %B indicator
- **Positive contribution**: Price near lower band (%B close to 0)
- **Negative contribution**: Price near upper band (%B close to 1)
- **Range**: -25 to +25 points

#### 2. Volatility Assessment (15% weight)
- Analyzes current Bollinger Band width and recent changes
- **Positive factors**: Narrow bands with expanding width (potential breakouts)
- **Negative factors**: High volatility reducing signal reliability
- **Range**: -15 to +15 points

#### 3. Fibonacci Level Interaction (35% weight)
- **Highest weight** as it's the core of the combined strategy
- Measures proximity to key Fibonacci levels (within 3% for significance)
- Considers price direction relative to support/resistance levels
- Accounts for trend context (uptrend vs downtrend)
- **Range**: -35 to +35 points

#### 4. Price Momentum (20% weight)
- RSI-like momentum indicator (14-period)
- **Positive contribution**: Oversold conditions (RSI < 30)
- **Negative contribution**: Overbought conditions (RSI > 70)
- **Range**: -30 to +30 points

### Position Sizing Guidelines

- **Extreme scores** (+90 or -90): Use higher position sizes
- **Threshold scores** (+65 or -65): Use smaller position sizes
- **Conviction indicator**: Higher absolute scores indicate stronger conviction

### Risk Management

- **Confirmation**: Wait 2-3 consecutive days in same signal zone
- **Stop Loss**: Place at nearest Fibonacci level in opposite direction
- **Profit Taking**: 
  - Long positions: Consider partial profits near resistance levels
  - Short positions: Consider partial covering near support levels

## Notebooks Overview

### 1. Bollinger_bands and Fibonacci Retracement.ipynb
**Basic Implementation**

- Core strategy implementation with essential components
- Basic signal generation (buy/sell)
- Standard backtesting functionality
- Visualization with Bollinger Bands, Fibonacci levels, and signals
- Performance metrics calculation

**Key Features:**
- Clean, straightforward implementation
- Essential backtesting with buy & hold comparison
- Basic plotting functionality

### 2. Bollinger_bands and Fibonacci Retracement-v2.ipynb  
**Enhanced Version with Scoring System**

- Introduction of the comprehensive scoring system (-100 to +100)
- Advanced signal categorization (Strong Buy/Sell, Moderate Buy/Sell, Hold)
- Enhanced visualization with strategy score chart
- Improved component analysis and debugging features

**Key Features:**
- **Strategy Score System**: Weighted combination of four components
- **Signal Categories**: Clear categorization for different action levels
- **Component Analysis**: Individual score breakdown for debugging
- **Enhanced Plotting**: Strategy score visualization with colored zones
- **Better Risk Management**: Score-based position sizing guidance

### 3. Bollinger_bands and Fibonacci Retracement-v3.ipynb
**Improved Implementation**

- Refined swing point detection (reduced window size for more points)
- Enhanced Fibonacci level calculation with better trend determination
- Improved error handling and debugging capabilities
- Optimized scoring weights (Fibonacci component increased to 40%)
- Additional debugging methods for component analysis

**Key Features:**
- **Improved Swing Detection**: Smaller window (5 periods) for more swing points
- **Better Trend Logic**: Enhanced trend determination algorithm
- **Debug Mode**: Comprehensive debugging information
- **Optimized Weights**: Fibonacci 40%, Bollinger 25%, Momentum 20%, Volatility 15%
- **Analysis Tools**: `analyze_fibonacci_component()` method for detailed debugging

### 4. RAG_LangGraph_Bollinger_bands and Fibonacci Retracement.ipynb
**AI-Powered Trading Assistant**

- LangGraph-based conversational AI system
- Automated strategy analysis and recommendations
- Tool-based architecture for real-time calculations
- Natural language interaction for strategy insights

**Key Features:**
- **AI Assistant**: Conversational interface for trading recommendations
- **Real-time Analysis**: Live market data processing
- **Tool Integration**: Automated scoring system execution
- **Flexible Parameters**: Customizable periods, windows, and timeframes
- **Risk Assessment**: AI-powered interpretation of signals and recommendations

## Usage Examples

### Basic Strategy Execution

```python
# Initialize strategy
strategy = BollingerFibonacciStrategy("AAPL", "2024-01-01", "2024-12-31")

# Run complete analysis
strategy.fetch_data()
strategy.calculate_bollinger_bands()
strategy.find_swing_points()
strategy.calculate_fibonacci_levels()
strategy.generate_signals()

# Calculate strategy score (v2 and v3)
strategy.calculate_strategy_score()

# Get latest signals
latest_score = strategy.data['Strategy_Score'].iloc[-1]
latest_signal = strategy.data['Signal_Category'].iloc[-1]
print(f"Current Score: {latest_score}, Signal: {latest_signal}")
```

### AI Assistant Usage (v4)

```python
# Ask the AI assistant for recommendations
message = graph.invoke({
    "messages": [("user", """
        Recommend if buy or sell AAPL based on Bollinger Bands 
        and Fibonacci Retracement Strategy score.
        Use 1 year data with 20-day window.
    """)]
}, config)

print(message["messages"][-1].content)
```

### Component Analysis

```python
# Analyze individual score components
print("Score Components:")
print(f"Bollinger Band Score: {strategy.data['BB_Score'].iloc[-1]:.2f}")
print(f"Volatility Score: {strategy.data['Volatility_Score'].iloc[-1]:.2f}")
print(f"Fibonacci Score: {strategy.data['Fib_Score'].iloc[-1]:.2f}")
print(f"Momentum Score: {strategy.data['Momentum_Score'].iloc[-1]:.2f}")

# Detailed Fibonacci analysis (v3)
fib_analysis = strategy.analyze_fibonacci_component()
```

## Installation and Setup

### Requirements

```bash
pip install yfinance pandas numpy plotly datetime
```

### For AI Assistant (v4)
```bash
pip install langchain langgraph langchain-openai
```

### Environment Setup

Create a `.env` file for the AI assistant:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Visualization Examples

The strategy provides comprehensive visualizations:

### Strategy Chart
- Candlestick price chart with Bollinger Bands
- Fibonacci retracement levels (horizontal lines)
- Buy/sell signals (triangular markers)
- Bollinger Bandwidth and %B indicators

### Strategy Score Chart  
- Price chart with Bollinger Bands and Fibonacci levels
- Strategy score indicator with colored zones:
  - **Dark Green**: Strong Buy (+60 to +100)
  - **Light Green**: Moderate Buy (+20 to +60)
  - **Gray**: Hold (-20 to +20)
  - **Orange**: Moderate Sell (-60 to -20)
  - **Red**: Strong Sell (-100 to -60)

## Performance Metrics

The strategy calculates comprehensive performance metrics:
- **Total Return**: Strategy vs Buy & Hold comparison
- **Annualized Volatility**: Risk measurement
- **Sharpe Ratio**: Risk-adjusted return
- **Maximum Drawdown**: Worst peak-to-trough decline
- **Win Rate**: Percentage of profitable trades

## Best Practices

1. **Confirmation**: Wait for 2-3 consecutive days in same signal zone
2. **Risk Management**: Always use stop losses at Fibonacci levels
3. **Position Sizing**: Adjust based on score magnitude and confidence
4. **Market Context**: Consider overall market conditions and trends
5. **Backtesting**: Test thoroughly before live implementation

## Contributing

Feel free to contribute improvements, bug fixes, or additional features. Please ensure any modifications maintain the core strategy logic and enhance the scoring system accuracy.

## Disclaimer

This strategy is for educational and research purposes only. Past performance does not guarantee future results. Always conduct thorough testing and consider your risk tolerance before implementing any trading strategy with real capital.