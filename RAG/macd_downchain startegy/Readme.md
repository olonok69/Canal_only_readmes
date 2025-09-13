# MACD & Donchian Channels Trading Strategy

A comprehensive implementation of a combined MACD and Donchian Channels trading strategy with intelligent scoring system and automated signal generation.

## 📋 Table of Contents

- [Overview](#overview)
- [Financial Techniques](#financial-techniques)
- [Scoring System](#scoring-system)
- [Notebooks Explanation](#notebooks-explanation)
- [Installation](#installation)
- [Usage](#usage)
- [Trading Signals](#trading-signals)
- [Risk Management](#risk-management)
- [Examples](#examples)

## 🎯 Overview

This project implements a sophisticated trading strategy that combines two powerful technical indicators:

1. **MACD (Moving Average Convergence Divergence)** - A momentum indicator
2. **Donchian Channels** - A price range/volatility indicator

The strategy uses a novel scoring system that converts complex indicator patterns into intuitive numerical values (-100 to +100), making it easier to interpret market conditions and generate trading signals.

## 📈 Financial Techniques

### Donchian Channels

Donchian Channels are primarily a **price range indicator** that can indirectly reflect market volatility:

**Components:**
- **Upper Band**: Highest price during a specified period
- **Middle Band**: Average of upper and lower bands  
- **Lower Band**: Lowest price during a specified period

**Key Features:**
- Channel width indicates volatility (wider = higher volatility)
- Automatic adaptation to market conditions
- Useful for identifying breakouts and trend reversals

**Trading Applications:**
- **Breakout Strategy**: Buy when price breaks above upper band, sell when below lower band
- **Mean Reversion**: Use middle band as support/resistance level
- **Trend Following**: Channel direction indicates overall trend

### MACD (Moving Average Convergence Divergence)

MACD is a **momentum indicator** that measures the speed and direction of price movement:

**Components:**
- **MACD Line** (Blue): Difference between fast EMA (12) and slow EMA (26)
- **Signal Line** (Red): EMA of MACD line (9 periods)
- **Histogram**: Difference between MACD line and signal line

**Key Signals:**
- **Bullish Crossover**: MACD line crosses above signal line
- **Bearish Crossover**: MACD line crosses below signal line
- **Zero Line Crossing**: Indicates trend strength
- **Divergence**: Price vs. MACD disagreement signals potential reversals

## 🔢 Scoring System

### MACD Score (-100 to +100)

The MACD score combines three weighted components:

1. **MACD Line vs Signal Line (40%)**
   - Positive when MACD > Signal Line (bullish)
   - Negative when MACD < Signal Line (bearish)

2. **MACD Line vs Zero (30%)**
   - Positive when MACD > 0 (strong bullish trend)
   - Negative when MACD < 0 (strong bearish trend)

3. **Histogram Momentum (30%)**
   - Positive when histogram increasing (accelerating momentum)
   - Negative when histogram decreasing (decelerating momentum)

### Donchian Score (-100 to +100)

The Donchian score combines three weighted components:

1. **Price Position Within Channel (50%)**
   - +50 at upper band
   - 0 at middle band
   - -50 at lower band

2. **Channel Direction (30%)**
   - Positive when channel trending upward
   - Negative when channel trending downward

3. **Channel Width Trend (20%)**
   - Positive when channel widening (increasing volatility)
   - Negative when channel narrowing (decreasing volatility)

### Combined Score

**Formula**: `(MACD Score + Donchian Score) / 2`

Gives equal weight to momentum (MACD) and price range (Donchian) indicators.

### Score Interpretation

#### Individual Scores:
- **Above +50**: Strong bullish
- **+25 to +50**: Moderate bullish
- **-25 to +25**: Neutral
- **-50 to -25**: Moderate bearish
- **Below -50**: Strong bearish

#### Combined Score Trading Signals:
- **+75 to +100**: 🟢 Strong Buy
- **+50 to +75**: 🟢 Buy
- **+25 to +50**: 🟡 Weak Buy
- **-25 to +25**: ⚪ Neutral (Hold)
- **-50 to -25**: 🟡 Weak Sell
- **-75 to -50**: 🔴 Sell
- **-100 to -75**: 🔴 Strong Sell

## 📓 Notebooks Explanation

### 1. `macd_Donchian channels.ipynb`
**Purpose**: Core implementation and visualization

**Features:**
- Complete calculation functions for both indicators
- Scoring system implementation
- Four-panel visualization using Plotly
- Real-time score interpretation
- Color-coded trading signals

**Key Functions:**
- `calculate_donchian_channels()`: Computes channel bands
- `calculate_macd()`: Computes MACD components
- `calculate_macd_score()`: Generates MACD score
- `calculate_donchian_score()`: Generates Donchian score
- `plot_scores_with_indicators()`: Creates comprehensive visualization

### 2. `RAG_Langgrap_macd_z-score-donchain_channel.ipynb`
**Purpose**: AI-powered trading assistant with LangGraph

**Features:**
- LangGraph-based conversational agent
- Tool-based architecture for calculations
- Natural language interaction for trading decisions
- Automated recommendation system
- Real-time market analysis

**Key Tools:**
- `@tool calculate_macd_score()`: MACD calculation tool
- `@tool calculate_donchian_channel_score()`: Donchian calculation tool
- `@tool calculate_combined_score()`: Score combination tool
- `@tool interpret_combined_score()`: Signal interpretation tool

**Agent Capabilities:**
- Accepts stock symbols and parameters
- Provides detailed component breakdowns
- Generates actionable trading recommendations
- Explains reasoning behind signals

### 3. `ta_donchain.ipynb`
**Purpose**: Traditional signal-based approach

**Features:**
- Classic buy/sell signal identification
- MACD crossover detection
- Donchian breakout signals
- Combined signal confirmation
- Signal filtering to reduce noise

**Signal Types:**
- **MACD Crossovers**: Line crosses above/below signal
- **Donchian Breakouts**: Price breaks channel boundaries
- **Combined Signals**: Both indicators align
- **Filtered Signals**: Minimum time between signals

## 🛠 Installation

```bash
# Clone the repository
git clone <repository-url>
cd macd-donchian-strategy

# Install required packages
pip install -r requirements.txt

# For Jupyter notebook support
pip install jupyter jupyterlab
```

### Key Dependencies

```python
# Core libraries
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# AI/LangGraph (for RAG notebook)
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# Technical analysis
from ta.volatility import DonchianChannel
```

## 🚀 Usage

### Basic Usage

```python
# Set parameters
ticker = "AAPL"
period = '1y'
window = 20  # Donchian period

# MACD parameters
fast_period = 12
slow_period = 26
signal_period = 9

# Download and analyze
data = yf.download(ticker, period=period)
channels = calculate_donchian_channels(data, window)
macd_data = calculate_macd(data, fast_period, slow_period, signal_period)

# Calculate scores
macd_score = calculate_macd_score(data, macd_data)
donchian_score = calculate_donchian_score(data, channels)
combined_score = calculate_combined_score(macd_score, donchian_score)

# Get current signals
current_signal = interpret_score(combined_score.iloc[-1])
print(f"Current signal for {ticker}: {current_signal}")
```

### AI Assistant Usage (RAG Notebook)

```python
# Natural language query
message = "Recommend if buy or sell TSLA based on MACD and Donchian scores for 6 months data"

# The agent will:
# 1. Calculate MACD score
# 2. Calculate Donchian score  
# 3. Compute combined score
# 4. Provide interpretation and recommendation
```

## 📊 Trading Signals

### Entry Points

**Long Positions:**
- Combined score crosses above +50
- Both MACD and Donchian scores positive
- Price breaks above Donchian upper band with MACD bullish crossover

**Short Positions:**
- Combined score crosses below -50
- Both MACD and Donchian scores negative
- Price breaks below Donchian lower band with MACD bearish crossover

### Exit Points

**Profit Taking:**
- Combined score begins moderating from extremes (+75 or -75)
- Opposite crossover in MACD
- Score crosses zero in opposite direction

**Stop Loss:**
- Price closes outside opposite Donchian band
- Combined score shows strong reversal pattern

## ⚠️ Risk Management

### Position Sizing
- **Strong signals** (+75 to +100 or -75 to -100): Larger position size
- **Moderate signals** (+50 to +75 or -50 to -75): Standard position size
- **Weak signals** (+25 to +50 or -25 to -50): Reduced position size

### Stop-Loss Guidelines
- Set stops near Donchian middle band for breakout trades
- Tighten stops when scores show early reversal signs
- Use MACD divergence as additional exit confirmation

### Diversification
- Don't concentrate all positions in one asset
- Consider correlation between selected instruments
- Monitor overall portfolio exposure

## 📈 Examples

### Example 1: Strong Buy Signal
```
Symbol: TSLA, Period: 1y
Latest MACD score: 78.45
Latest Donchian score: 82.30
Combined score: 80.38
Interpretation: Strong Buy Signal
```

### Example 2: Neutral Market
```
Symbol: AAPL, Period: 6mo  
Latest MACD score: -12.50
Latest Donchian score: 15.20
Combined score: 1.35
Interpretation: Neutral
```

## 📋 Benefits of This System

1. **Simplification**: Converts complex patterns into intuitive numerical values
2. **Normalization**: All indicators use the same -100 to +100 scale
3. **Combination**: Easily combines momentum and price range analysis
4. **Visualization**: Clear representation of indicator strength and transitions
5. **Customization**: Component weights can be adjusted for different strategies
6. **Automation**: Suitable for algorithmic trading implementation

## 🔄 Practical Implementation

### Trend Confirmation
When both MACD and Donchian scores agree (both positive or negative), it confirms a strong trend direction.

### Divergence Detection  
When scores move in opposite directions, it may indicate a potential trend reversal requiring closer attention.

### Multi-Timeframe Analysis
- Use shorter periods (20 days) for swing trading
- Use longer periods (50+ days) for position trading
- Combine multiple timeframes for confirmation

## 📚 Further Reading

- [MACD Technical Analysis](https://www.investopedia.com/terms/m/macd.asp)
- [Donchian Channels Guide](https://www.investopedia.com/terms/d/donchianchannels.asp)
- [Technical Analysis Fundamentals](https://www.investopedia.com/technical-analysis-4689657)

## ⚖️ Disclaimer

This trading strategy is for educational and research purposes only. Past performance does not guarantee future results. Always conduct your own research and consider consulting with a financial advisor before making investment decisions. Trading involves substantial risk of loss.

---
