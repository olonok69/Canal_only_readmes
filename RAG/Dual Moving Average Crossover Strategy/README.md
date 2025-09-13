# Dual Moving Average Crossover Strategy with AI Agent

A comprehensive Python implementation of the classic Dual Moving Average Crossover Strategy enhanced with an intelligent AI agent for automated analysis, scoring, and market scanning.

## 📋 Table of Contents

- [Strategy Overview](#strategy-overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Implementation Details](#implementation-details)
- [AI Agent System](#ai-agent-system)
- [Scoring System](#scoring-system)
- [Usage Examples](#usage-examples)
- [Notebook Descriptions](#notebook-descriptions)
- [Configuration](#configuration)
- [Performance Metrics](#performance-metrics)
- [Limitations](#limitations)
- [Contributing](#contributing)

## 🎯 Strategy Overview

The Dual Moving Average Crossover Strategy is a classic trend-following approach that uses two moving averages with different periods to generate trading signals:

### Core Concepts

- **Golden Cross**: When the short-term moving average crosses above the long-term moving average → **BUY Signal**
- **Death Cross**: When the short-term moving average crosses below the long-term moving average → **SELL Signal**
- **Classic Configuration**: 50-day and 200-day moving averages (institutional standard)

### Why This Strategy Works

1. **Trend Identification**: Captures medium to long-term market trends
2. **Noise Reduction**: Smooths out short-term price fluctuations
3. **Institutional Usage**: Widely used by professional traders and fund managers
4. **Historical Performance**: Studies show 7.43% average gains over 40 days post-Golden Cross

## 🚀 Key Features

### 1. **Flexible Strategy Implementation**
- **Moving Average Types**: SMA (Simple) and EMA (Exponential)
- **Customizable Periods**: Any combination (default: 50/200)
- **Multiple Timeframes**: Supports all Yahoo Finance periods
- **Signal Quality Assessment**: Trend strength and momentum analysis

### 2. **AI-Powered Analysis Tools**
- **Natural Language Queries**: Ask questions in plain English
- **Automated Strategy Analysis**: Complete performance evaluation
- **Market Scanner**: Multi-symbol opportunity identification
- **Intelligent Scoring**: -100 to +100 scoring system

### 3. **Advanced Performance Analytics**
- **Strategy vs Buy & Hold** comparison
- **Risk-Adjusted Metrics**: Sharpe ratio, volatility, drawdown
- **Win Rate Calculation**: Trade-by-trade analysis
- **Signal History**: Recent crossover tracking

### 4. **Interactive Visualizations**
- **3-Panel Charts**: Price + MAs, Positions, Returns
- **Signal Markers**: Clear Golden/Death Cross indicators
- **Plotly Integration**: Interactive, zoomable charts
- **Real-time Updates**: Dynamic chart generation

## 📦 Installation

### Prerequisites
- Python 3.8+
- Jupyter Lab/Notebook
- Internet connection (for market data)

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd dual_band_strategy
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
Create a `.env` file in the project root:

```env
# Choose your AI provider
MODEL_PROVIDER=vertexai  # or "openai"

# For OpenAI (if using)
OPENAI_API_KEY=your_openai_api_key_here

# For Vertex AI (if using)
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
PROJECT=your_project_id
REGION=us-central1
```

### Step 4: AI Provider Setup

#### Option A: OpenAI
1. Get API key from [OpenAI Platform](https://platform.openai.com)
2. Add to `.env` file
3. Set `MODEL_PROVIDER=openai`

#### Option B: Google Vertex AI
1. Create Google Cloud Project
2. Enable Vertex AI API
3. Create service account and download JSON key
4. Set `MODEL_PROVIDER=vertexai`

### Step 5: Launch Jupyter
```bash
jupyter lab
```

## 📁 Project Structure

```
dual_band_strategy/
├── notebook/
│   ├── Rag_agent.ipynb                    # AI Agent Implementation
│   └── dual moving average crossover strategy.ipynb  # Core Strategy
├── .env                                   # Environment variables
├── .gitignore                            # Git ignore rules
├── requirements.txt                      # Python dependencies
└── README.md                             # This file
```

## 🔧 Implementation Details

### Core Strategy Class

```python
class DualMovingAverageStrategy:
    def __init__(self, short_period=50, long_period=200, ma_type='SMA'):
        self.short_period = short_period
        self.long_period = long_period
        self.ma_type = ma_type
    
    def generate_signals(self, data):
        # Golden Cross: short MA > long MA
        # Death Cross: short MA < long MA
        # Returns data with signals and positions
```

### Signal Generation Logic

1. **Calculate Moving Averages**: SMA or EMA for both periods
2. **Detect Crossovers**: Compare current vs previous periods
3. **Generate Positions**: 1 (Long), -1 (Short), 0 (Neutral)
4. **Forward Fill**: Maintain position until next signal

### Performance Calculation

- **Strategy Returns**: Position × Daily Returns
- **Benchmark Comparison**: Strategy vs Buy & Hold
- **Risk Metrics**: Volatility, Sharpe Ratio, Maximum Drawdown
- **Trade Analysis**: Win rate, average return per trade

## 🤖 AI Agent System

### Architecture

The AI agent is built using **LangGraph** and supports both **OpenAI GPT** and **Google Gemini** models:

```python
# Agent Components
├── State Management (LangGraph)
├── Tool Integration (4 specialized tools)
├── Memory System (conversation history)
└── Model Provider (OpenAI/Vertex AI)
```

### Available Tools

#### 1. `@tool analyze_dual_ma_strategy()`
- Complete strategy analysis with performance metrics
- Current market position and trend assessment
- Recent signal history and market condition evaluation

#### 2. `@tool calculate_dual_ma_score()`
- Scoring system (-100 to +100) for trading decisions
- Combines MA positioning, signal strength, and momentum
- Provides clear BUY/SELL/HOLD recommendations

#### 3. `@tool compare_ma_strategies()`
- Tests multiple configurations (20/50, 50/200, 10/30)
- Compares SMA vs EMA performance
- Ranks strategies by Sharpe ratio

#### 4. `@tool market_scanner_dual_ma()`
- Scans multiple symbols for opportunities
- Ranks by signal recency and trend strength
- Provides market sentiment overview

### Conversation Flow

1. **User Query**: Natural language question about trading
2. **Tool Selection**: AI chooses appropriate analysis tools
3. **Data Processing**: Fetch market data and run calculations
4. **Result Synthesis**: Combine tool outputs into coherent response
5. **Recommendation**: Provide actionable trading insights

## 📊 Scoring System

### Score Calculation Formula

**Total Score = MA Positioning (40%) + Signal Strength (30%) + Momentum (30%)**

#### Component Breakdown

1. **MA Positioning (40% weight)**
   - Positive when short MA > long MA
   - Scaled by separation percentage
   - Range: -40 to +40

2. **Recent Signal Strength (30% weight)**
   - Time since last crossover
   - Price movement since signal
   - Signal quality assessment
   - Range: -30 to +30

3. **Trend Momentum (30% weight)**
   - Rate of MA separation change
   - 5-day vs 10-day average comparison
   - Trend acceleration/deceleration
   - Range: -30 to +30

### Score Interpretation

| Score Range | Signal | Market Condition | Action |
|-------------|--------|------------------|---------|
| **+80 to +100** | 🟢 **Strong Buy** | Recent Golden Cross + strong momentum | Enter long position |
| **+60 to +80** | 🟢 **Buy** | Golden Cross conditions favorable | Consider long entry |
| **+40 to +60** | 🟡 **Weak Buy** | Mild bullish trend | Small long position |
| **-40 to +40** | ⚪ **Neutral** | Mixed signals | Hold current position |
| **-60 to -40** | 🟡 **Weak Sell** | Mild bearish trend | Consider exit/small short |
| **-80 to -60** | 🔴 **Sell** | Death Cross conditions | Exit long/enter short |
| **-100 to -80** | 🔴 **Strong Sell** | Recent Death Cross + weak momentum | Strong short signal |

## 💻 Usage Examples

### Basic Strategy Analysis

```python
# Analyze Apple with classic 50/200 SMA
result = analyze_stock_dual_ma(
    symbol="AAPL",
    period="2y",
    short_period=50,
    long_period=200,
    ma_type='SMA',
    include_comparison=True
)
```

### Market Scanner

```python
# Scan tech stocks for opportunities
tech_stocks = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
scanner_result = scan_market_opportunities(
    symbols=tech_stocks,
    ma_type='EMA',
    short_period=20,
    long_period=50
)
```

### Interactive AI Chat

```python
# Start interactive session with AI agent
graph = create_dual_ma_agent()
result = graph.invoke({
    "messages": [HumanMessage(content="What's the current trend for TSLA?")]
})
```

## 📚 Notebook Descriptions

### 1. `Rag_agent.ipynb` - AI Trading Agent

**Purpose**: Comprehensive AI-powered trading assistant

**Key Components**:
- **LangGraph Implementation**: State-based conversation management
- **Multi-Model Support**: OpenAI GPT-4o-mini or Google Gemini
- **Tool Integration**: 4 specialized trading analysis tools
- **Interactive Mode**: Chat interface for real-time queries

**Features**:
- Natural language strategy analysis
- Automated market scanning
- Performance comparison across configurations
- Real-time scoring and recommendations

### 2. `dual moving average crossover strategy.ipynb` - Core Strategy

**Purpose**: Pure strategy implementation and visualization

**Key Components**:
- **Strategy Class**: Complete dual MA implementation
- **Signal Generation**: Golden/Death cross detection
- **Performance Analytics**: Comprehensive metrics calculation
- **Interactive Charts**: 3-panel Plotly visualizations

**Features**:
- Candlestick charts with MA overlays
- Buy/sell signal markers
- Position tracking visualization
- Strategy vs benchmark comparison

## ⚙️ Configuration

### Environment Variables

```env
# Model Provider Selection
MODEL_PROVIDER=vertexai  # Options: "openai", "vertexai"

# OpenAI Configuration
OPENAI_API_KEY=sk-...

# Vertex AI Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
PROJECT=your-project-id
REGION=us-central1
```

### Strategy Parameters

```python
# Default Configuration
SHORT_PERIOD = 50      # Fast moving average
LONG_PERIOD = 200      # Slow moving average
MA_TYPE = 'SMA'        # 'SMA' or 'EMA'
DATA_PERIOD = '2y'     # Yahoo Finance period
```

### Model Settings

```python
# OpenAI Settings
model = "gpt-4o-mini"
temperature = 0.1

# Vertex AI Settings
model = "gemini-2.0-flash-001"
temperature = 0.1
max_tokens = 8192
```

## 📈 Performance Metrics

### Strategy Metrics

- **Total Return**: Strategy cumulative return
- **Excess Return**: Strategy return - Buy & Hold return
- **Win Rate**: Percentage of profitable trades
- **Sharpe Ratio**: Risk-adjusted return metric
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Volatility**: Annualized standard deviation

### Signal Metrics

- **Golden Cross Count**: Number of bullish crossovers
- **Death Cross Count**: Number of bearish crossovers
- **Average Return per Trade**: Mean trade profitability
- **Signal Frequency**: Average time between signals

### Risk Metrics

- **Strategy Volatility**: Portfolio return volatility
- **Benchmark Volatility**: Buy & hold volatility
- **Correlation**: Strategy-benchmark correlation
- **Beta**: Systematic risk measure

## ⚠️ Limitations

### Strategy Limitations

1. **Whipsaw Risk**: False signals in sideways markets
2. **Lag Effect**: Moving averages are backward-looking
3. **Market Dependency**: Works best in trending markets
4. **Transaction Costs**: Not included in backtest

### Technical Limitations

1. **Data Dependency**: Requires reliable market data feed
2. **Computational Load**: Real-time calculations for multiple symbols
3. **Model Limits**: AI provider rate limits and costs
4. **Internet Required**: Live data and AI model access

### Implementation Notes

1. **No Portfolio Management**: Single-asset focus
2. **No Risk Management**: No stop-losses or position sizing
3. **No Slippage**: Assumes perfect execution
4. **Historical Bias**: Past performance doesn't guarantee future results

## 🔄 Future Enhancements

### Planned Features

- [ ] **Portfolio Management**: Multi-asset allocation
- [ ] **Risk Management**: Stop-loss and position sizing
- [ ] **Real-time Alerts**: Email/SMS notifications
- [ ] **Backtesting Engine**: Historical strategy testing
- [ ] **Paper Trading**: Live simulation mode
- [ ] **Web Interface**: Streamlit/Flask web app
- [ ] **Database Integration**: Trade history storage
- [ ] **API Development**: RESTful trading API

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions and support:
- Create an issue in the repository
- Check the notebook documentation
- Review the configuration examples

## 🙏 Acknowledgments

- **Yahoo Finance**: For providing free market data
- **LangChain/LangGraph**: For AI agent framework
- **Plotly**: For interactive visualizations
- **Quantifiable Edges**: For strategy research insights

---

**Disclaimer**: This software is for educational purposes only. Not financial advice. Trade at your own risk.