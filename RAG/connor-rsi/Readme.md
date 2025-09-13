# Connors RSI Trading Strategy with LangGraph

A sophisticated trading strategy implementation featuring the Connors RSI indicator combined with Z-Score analysis for enhanced mean reversion signals. This system uses LangGraph to create an intelligent agent that provides comprehensive technical analysis and trading recommendations.

## 📋 Table of Contents

- [Overview](#overview)
- [Financial Techniques](#financial-techniques)
- [Scoring System](#scoring-system)
- [Notebooks Overview](#notebooks-overview)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Key Features](#key-features)
- [Technical Implementation](#technical-implementation)
- [Trading Signals](#trading-signals)
- [Performance Analysis](#performance-analysis)
- [Best Practices](#best-practices)

## 🎯 Overview

This project implements the Connors RSI trading strategy, an advanced momentum oscillator developed by Larry Connors that combines three distinct components to identify overbought and oversold conditions with greater precision than traditional RSI. The implementation includes:

1. **Connors RSI Calculation** - Multi-component momentum analysis
2. **Z-Score Integration** - Statistical mean reversion confirmation
3. **Combined Scoring System** - Weighted indicator combination for trading signals
4. **LangGraph Agent** - AI-powered analysis and recommendations

## 📈 Financial Techniques

### Connors RSI Components

The Connors RSI is calculated as the average of three equally weighted components:

#### 1. Price RSI (33.33% weight)
- **Traditional RSI** applied to closing prices
- **Default Period**: 3 days (more sensitive than standard 14-day RSI)
- **Purpose**: Measures recent price momentum
- **Interpretation**: Values > 50 indicate bullish momentum, < 50 bearish momentum

#### 2. Streak RSI (33.33% weight)  
- **RSI applied to price streaks** (consecutive up/down movements)
- **Default Period**: 2 days
- **Calculation Process**:
  - Track consecutive up days (+1, +2, +3, etc.)
  - Track consecutive down days (-1, -2, -3, etc.)
  - Apply RSI to this streak series
- **Purpose**: Measures persistence of directional movement

#### 3. Percent Rank (33.33% weight)
- **Percentile ranking** of rate of change over rolling window
- **Default Period**: 100 days
- **Calculation**: Current price change percentile vs. historical 100-day range
- **Purpose**: Provides historical context for current price movements

### Connors RSI Formula
```
CRSI = (Price RSI + Streak RSI + Percent Rank) / 3
```

### Z-Score Analysis

Z-Score measures how many standard deviations the current price is from its moving average:

```
Z-Score = (Current Price - Moving Average) / Standard Deviation
```

**Interpretation Guidelines:**
- **Z > +2**: Price significantly above average (potential mean reversion down)
- **Z < -2**: Price significantly below average (potential mean reversion up)
- **-2 ≤ Z ≤ +2**: Price within normal trading range

## 🔢 Scoring System

### Connors RSI Score Conversion

The traditional Connors RSI (0-100) is converted to a standardized score (-100 to +100):

```python
connors_score = (crsi - 50) * 2
```

### Combined Score Calculation

**Formula**: `(Connors RSI Score × 70%) + (Z-Score × 30%)`

This weighting gives primary emphasis to momentum (Connors RSI) while using Z-Score for mean reversion confirmation.

### Trading Signal Interpretation

| Score Range | Signal | Market Condition | Recommended Action |
|-------------|--------|------------------|-------------------|
| **+75 to +100** | 🟢 **Strong Buy** | Extreme oversold + favorable positioning | High conviction long |
| **+50 to +75** | 🟢 **Buy** | Oversold conditions | Moderate long position |
| **+25 to +50** | 🟡 **Weak Buy** | Mild oversold bias | Small long or wait |
| **-25 to +25** | ⚪ **Neutral** | Normal range | Hold current positions |
| **-50 to -25** | 🟡 **Weak Sell** | Mild overbought bias | Reduce longs |
| **-75 to -50** | 🔴 **Sell** | Overbought conditions | Close longs or short |
| **-100 to -75** | 🔴 **Strong Sell** | Extreme overbought | Strong short signal |

## 📓 Notebooks Overview

### 1. `connor_rsi.ipynb`
**Purpose**: Core implementation and visualization

**Key Features:**
- Complete Connors RSI calculation from scratch
- Interactive Plotly visualizations with 3-panel layout
- Component analysis (Price RSI, Streak RSI, Percent Rank)
- Signal generation with buy/sell markers
- Performance comparison vs. traditional RSI

**Visualization Components:**
- **Top Panel**: Price chart with Connors RSI signals
- **Middle Panel**: Individual RSI components comparison
- **Bottom Panel**: Main Connors RSI with overbought/oversold levels

### 2. `RAG_langgraph_connor_rsi.ipynb`
**Purpose**: AI-powered trading assistant using LangGraph

**Key Features:**
- LangGraph-based conversational agent
- Automated tool discovery and execution
- Natural language query processing
- Multi-symbol analysis capabilities
- Combined Connors RSI + Z-Score recommendations

**Available Tools:**
- `@tool calculate_connors_rsi_score()`: Complete Connors RSI analysis
- `@tool calculate_zscore_indicator()`: Z-Score calculation and interpretation
- `@tool calculate_combined_connors_score()`: Weighted combination scoring
- `@tool interpret_connors_combined_score()`: Signal interpretation

## ⚙️ Installation

### Prerequisites
```bash
# Core dependencies
pip install pandas numpy plotly yfinance datetime

# For AI assistant (LangGraph notebook)
pip install langchain langgraph langchain-openai
```

### Environment Setup

Create `.env` file for the AI assistant:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd RAG/connor-rsi

# Install dependencies
pip install -r requirements.txt

# Run basic analysis
jupyter notebook connor_rsi.ipynb

# Run AI assistant
jupyter notebook RAG_langgraph_connor_rsi.ipynb
```

## 🚀 Usage Examples

### Basic Analysis

```python
# Calculate Connors RSI for Apple stock
symbol = "AAPL"
end_date = datetime.now()
start_date = end_date - timedelta(days=730)

# Download data
data = yf.download(symbol, start=start_date, end=end_date)

# Calculate Connors RSI components
crsi_data = connors_rsi(data)
signals = generate_signals(crsi_data['CRSI'])

# Display results
print(f"Current CRSI: {crsi_data['CRSI'].iloc[-1]:.2f}")
print(f"Signal: {'BUY' if crsi_data['CRSI'].iloc[-1] < 20 else 'SELL' if crsi_data['CRSI'].iloc[-1] > 80 else 'HOLD'}")
```

### AI Assistant Usage

```python
# Natural language analysis request
result = analyze_stock("UBS", period="1y", zscore_window=20)

# The system will:
# 1. Calculate Connors RSI score
# 2. Calculate Z-Score indicator  
# 3. Compute combined score
# 4. Provide trading recommendation with reasoning
```

### Multi-Symbol Comparison

```python
symbols = ["AAPL", "TSLA", "MSFT", "GOOGL"]
for symbol in symbols:
    analysis = analyze_stock(symbol, period="6mo")
    print(f"{symbol}: {analysis}")
```

## ✨ Key Features

### Advanced Signal Generation

**Traditional Levels:**
- **CRSI < 20**: Oversold (potential buy signal)
- **CRSI > 80**: Overbought (potential sell signal)

**Enhanced Confirmation:**
- Combines momentum (Connors RSI) with mean reversion (Z-Score)
- Reduces false signals through dual confirmation
- Provides confidence levels for each signal

### Component Analysis

```python
# Individual component contributions
print("Component Analysis:")
print(f"Price RSI: {price_rsi_score:.2f}")
print(f"Streak RSI: {streak_rsi_score:.2f}")  
print(f"Percent Rank: {percent_rank_score:.2f}")
print(f"Combined Score: {combined_score:.2f}")
```

### Adaptive Parameters

The system allows customization of key parameters:
- **RSI Period**: Default 3 (can adjust for sensitivity)
- **Streak Period**: Default 2 (affects streak calculation)
- **Rank Period**: Default 100 (historical context window)
- **Z-Score Window**: Default 20 (mean reversion timeframe)

## 🔧 Technical Implementation

### Core Calculation Functions

#### RSI Calculation
```python
def rsi(series, period=14):
    """Calculate traditional RSI"""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
```

#### Streak RSI Calculation  
```python
def streak_rsi(series, period=2):
    """Calculate RSI of price streaks"""
    price_change = series.diff()
    streaks = []
    current_streak = 0
    
    for change in price_change:
        if pd.isna(change):
            streaks.append(0)
            current_streak = 0
        elif change > 0:
            current_streak = current_streak + 1 if current_streak >= 0 else 1
            streaks.append(current_streak)
        elif change < 0:
            current_streak = current_streak - 1 if current_streak <= 0 else -1
            streaks.append(current_streak)
        else:
            streaks.append(0)
            current_streak = 0
    
    return rsi(pd.Series(streaks, index=series.index), period)
```

#### Percent Rank Calculation
```python
def percent_rank(series, period=100):
    """Calculate percent rank over rolling window"""
    def rank_pct(x):
        if len(x) < 2:
            return 50.0
        current_value = x.iloc[-1]
        rank = (x < current_value).sum()
        return (rank / (len(x) - 1)) * 100
    
    return series.rolling(window=period).apply(rank_pct, raw=False)
```

### LangGraph Agent Architecture

The AI assistant implements a sophisticated agent workflow:

```python
# Agent state management
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Chatbot with specialized financial knowledge
def chatbot(state: State):
    """Intelligent trading assistant with Connors RSI expertise"""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}
```

## 📊 Trading Signals

### Signal Quality Metrics

The system provides several metrics to assess signal quality:

#### Component Alignment
- **Strong Signals**: All three components (Price RSI, Streak RSI, Percent Rank) align
- **Moderate Signals**: Two of three components align
- **Weak Signals**: Only one component indicates the direction

#### Historical Performance
```python
# Example signal effectiveness metrics
buy_signals = (signals == 'BUY').sum()
sell_signals = (signals == 'SELL').sum()
print(f"Total Buy Signals: {buy_signals}")
print(f"Total Sell Signals: {sell_signals}")
```

### Risk Management

#### Stop-Loss Guidelines
- **Long Positions**: Set stop at recent swing low or -3% from entry
- **Short Positions**: Set stop at recent swing high or +3% from entry
- **Position Sizing**: Adjust based on signal strength and volatility

#### Signal Filtering
```python
# Filter signals to reduce noise
def filter_signals(signals, min_gap_days=5):
    """Ensure minimum time between signals"""
    filtered = signals.copy()
    last_signal_date = None
    
    for date, signal in signals.items():
        if signal in ['BUY', 'SELL']:
            if last_signal_date and (date - last_signal_date).days < min_gap_days:
                filtered[date] = None
            else:
                last_signal_date = date
    
    return filtered
```

## 📈 Performance Analysis

### Backtesting Results

Typical performance characteristics observed:

#### Tesla (TSLA) Analysis
- **Signals Generated**: High frequency due to volatility
- **Best Performance**: During trending periods with clear reversals
- **Challenge**: Whipsaw conditions in high volatility periods

#### Apple (AAPL) Analysis  
- **Signals Generated**: Moderate frequency, well-spaced
- **Best Performance**: Consistent trend identification
- **Reliability**: Higher signal-to-noise ratio than TSLA

### Market Condition Adaptation

#### Trending Markets
- Connors RSI may give premature reversal signals
- Z-Score provides additional trend context
- **Recommendation**: Use longer timeframes in strong trends

#### Sideways Markets
- Optimal conditions for Connors RSI mean reversion
- High success rate for overbought/oversold signals
- **Recommendation**: Use standard parameters

## 💡 Best Practices

### Parameter Optimization

#### For Different Asset Classes
```python
# Volatile stocks (like Tesla)
connors_params = {
    'rsi_period': 2,      # More sensitive
    'streak_period': 1,   # Faster response
    'rank_period': 50     # Shorter history
}

# Stable stocks (like Apple)  
connors_params = {
    'rsi_period': 3,      # Standard
    'streak_period': 2,   # Standard
    'rank_period': 100    # Full history
}
```

#### Multi-Timeframe Analysis
```python
# Confirm signals across timeframes
daily_signal = calculate_connors_rsi_score("AAPL", period="1y")
weekly_signal = calculate_connors_rsi_score("AAPL", period="2y")

# Only trade when both timeframes agree
if daily_signal < -60 and weekly_signal < -40:
    recommendation = "STRONG BUY"
```

### Risk Management Rules

1. **Never risk more than 2% per trade**
2. **Combine with trend analysis** for context
3. **Use position sizing** based on signal strength
4. **Implement stop-losses** consistently
5. **Monitor correlation** across positions

### System Monitoring

```python
# Track system performance
def monitor_performance(signals, prices):
    """Calculate basic performance metrics"""
    returns = []
    position = 0
    
    for date, signal in signals.items():
        if signal == 'BUY' and position <= 0:
            entry_price = prices[date]
            position = 1
        elif signal == 'SELL' and position >= 0:
            exit_price = prices[date]
            if position == 1:
                returns.append((exit_price - entry_price) / entry_price)
            position = -1
    
    return {
        'total_trades': len(returns),
        'win_rate': sum(1 for r in returns if r > 0) / len(returns) if returns else 0,
        'avg_return': sum(returns) / len(returns) if returns else 0
    }
```

## 🔮 Advanced Features

### Multi-Asset Analysis

The system supports portfolio-wide analysis:

```python
# Analyze multiple assets simultaneously
portfolio = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
results = {}

for symbol in portfolio:
    analysis = analyze_stock(symbol, period="6mo", zscore_window=20)
    results[symbol] = analysis

# Rank by signal strength
sorted_signals = sorted(results.items(), key=lambda x: x[1]['combined_score'], reverse=True)
```

### Custom Alert System

```python
def check_signals(symbols, threshold=60):
    """Check for strong signals across watchlist"""
    alerts = []
    
    for symbol in symbols:
        score = get_current_score(symbol)
        if abs(score) > threshold:
            alerts.append({
                'symbol': symbol,
                'score': score,
                'signal': 'BUY' if score > threshold else 'SELL',
                'timestamp': datetime.now()
            })
    
    return alerts
```

## 📚 Educational Resources

### Understanding Connors RSI

**Key Concepts:**
- **Mean Reversion**: Tendency for prices to return to average
- **Momentum Oscillators**: Indicators measuring rate of price change  
- **Overbought/Oversold**: Extreme price conditions likely to reverse
- **Streak Analysis**: Importance of consecutive price movements

### Recommended Reading

- **"Short Term Trading Strategies That Work"** by Larry Connors
- **"High Probability ETF Trading"** by Larry Connors  
- **Technical Analysis studies** on mean reversion strategies
- **Academic papers** on momentum and reversal patterns

### Further Development

Potential enhancements for advanced users:

1. **Machine Learning Integration**: Use ML to optimize parameters
2. **Options Strategies**: Apply Connors RSI to options trading
3. **Sector Analysis**: Comparative analysis across market sectors
4. **Real-Time Alerts**: Integration with trading platforms
5. **Portfolio Optimization**: Risk-adjusted position sizing

## ⚠️ Important Disclaimers

- **Educational Purpose**: This system is for learning and research only
- **Not Financial Advice**: All trading decisions should involve professional consultation  
- **Market Risks**: Past performance does not guarantee future results
- **Backtesting Required**: Always test strategies thoroughly before implementation
- **Risk Management**: Use proper position sizing and stop-losses consistently

## 🤝 Contributing

### Enhancement Opportunities

1. **Additional Indicators**: Integrate with other technical indicators
2. **Parameter Optimization**: Automatic parameter tuning algorithms
3. **Performance Analytics**: Enhanced backtesting and metrics
4. **Visualization**: Additional chart types and analysis tools
5. **Integration**: Connect with trading platforms and data feeds

### Development Guidelines

- Follow existing code style and documentation patterns
- Include comprehensive testing for new features  
- Provide clear examples and usage instructions
- Maintain compatibility with existing implementations
- Document any parameter changes or new techniques

---

**The Connors RSI strategy represents a sophisticated approach to technical analysis that combines traditional momentum concepts with modern statistical techniques. When properly implemented and risk-managed, it can provide valuable insights for short-term trading and market timing decisions.**