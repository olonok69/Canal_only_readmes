<artifact identifier="bollinger-readme" type="text/markdown" title="Bollinger Bands and Z-Score Analysis - README">
# Bollinger Bands and Z-Score Analysis for Financial Trading

This repository contains two Jupyter notebooks that implement Bollinger Bands analysis and Z-score calculations for financial trading strategies. The implementation demonstrates both educational concepts and practical applications using modern AI frameworks.

## 📊 Financial Concepts Overview

### Standard Deviation in Finance
Standard deviation measures the amount of variation in a dataset. In financial markets, it quantifies price volatility - how much a stock's price deviates from its average price over a specific period.

**Example**: If a stock averages $100 with a standard deviation of $5:
- 68% of prices fall between $95-$105 (1 standard deviation)
- 95% of prices fall between $90-$110 (2 standard deviations) 
- 99.7% of prices fall between $85-$115 (3 standard deviations)

This follows the **Empirical Rule**, which states that 99.7% of values in a normal distribution lie within 3 standard deviations of the mean.

### Z-Score in Trading
A Z-score measures how many standard deviations a value is from the mean:
- **Z-score = 0**: Price equals the moving average
- **Positive Z-score**: Price is above average (potentially overbought)
- **Negative Z-score**: Price is below average (potentially oversold)

### Bollinger Bands
Developed by John Bollinger in the 1980s, Bollinger Bands consist of three lines:

1. **Middle Band (SMA)**: 20-period Simple Moving Average
2. **Upper Band**: SMA + (2 × Standard Deviation)
3. **Lower Band**: SMA - (2 × Standard Deviation)

**Trading Interpretation**:
- Price near **upper band**: Potentially overbought (sell signal)
- Price near **lower band**: Potentially oversold (buy signal)
- **Band width**: Indicates volatility (wide = high volatility, narrow = low volatility)

### Bollinger Z-Score Formula
```
Z-Score = (Current Price - Moving Average) / Standard Deviation
```

**Trading Guidelines**:
- **Z > +2**: Overbought condition (consider selling)
- **Z < -2**: Oversold condition (consider buying)
- **-2 ≤ Z ≤ +2**: Normal trading range

## 📁 Repository Structure

### 1. `Bollinger_bands.ipynb`
**Educational notebook focusing on core concepts and visualization**

**Key Features**:
- Comprehensive explanation of standard deviation and Z-scores
- Practical examples using Emperor penguin height distributions
- Step-by-step Bollinger Bands calculation
- Interactive visualizations using Plotly
- Integration with LangChain agents for automated analysis

**Technical Implementation**:
```python
# Bollinger Bands Calculation
data['SMA'] = data['Close'].rolling(window=20).mean()
data['SD'] = data['Close'].rolling(window=20).std()
data['UB'] = data['SMA'] + 2 * data['SD']  # Upper Band
data['LB'] = data['SMA'] - 2 * data['SD']  # Lower Band
```

**Data Sources**: 
- Yahoo Finance API (yfinance)
- Hourly stock data over 180-day periods
- Focus on major stocks (AAPL, UBS, TSLA)

### 2. `RAG_Langgraph_z-score.ipynb`
**Production-ready implementation using LangGraph for automated trading recommendations**

**Key Features**:
- Custom tool for real-time Z-score calculation
- AI-powered trading recommendations
- State management using LangGraph
- Integration with OpenAI GPT-4 models
- Memory persistence for conversation context

**Core Tool Implementation**:
```python
@tool
def calculate_bollinger_z_score(symbol: str, period: int = 20) -> str:
    """Calculate Bollinger Z-Score for any stock symbol"""
    data = yf.download(symbol, period=f"{period+50}d")
    closes = data['Close']
    rolling_mean = closes.rolling(window=period).mean()
    rolling_std = closes.rolling(window=period).std()
    z_score = (closes - rolling_mean) / rolling_std
    return latest_z_score
```

**AI Agent Capabilities**:
- Automatic data fetching and analysis
- Contextual trading recommendations
- Multi-turn conversation support
- Risk assessment based on Z-score interpretation

## 🛠 Technical Requirements

### Dependencies
```
streamlit==latest
pandas==latest
numpy==latest
yfinance==latest
langchain==latest
langchain-openai==latest
langgraph==latest
plotly==latest
matplotlib==latest
google-cloud-aiplatform==latest
python-dotenv==latest
```

### Environment Setup
1. **API Keys Required**:
   - OpenAI API key for GPT-4 integration
   - Google Cloud credentials for Vertex AI (optional)

2. **Configuration**:
   ```python
   # .env file
   OPENAI_API_KEY=your_openai_key
   GEMINI_API_KEY=your_gemini_key
   PROJECT=your_gcp_project
   REGION=your_gcp_region
   ```

## 📈 Trading Strategy Implementation

### Signal Generation
The notebooks implement a systematic approach to generate trading signals:

1. **Data Collection**: Fetch historical price data
2. **Indicator Calculation**: Compute Bollinger Bands and Z-scores
3. **Signal Analysis**: Evaluate overbought/oversold conditions
4. **Risk Assessment**: Consider trend context and volatility
5. **Recommendation**: Provide buy/sell/hold advice

### Risk Management Considerations
- **False Signals**: Z-scores can generate false signals in trending markets
- **Volatility Impact**: High volatility affects band width and signal reliability
- **Trend Context**: Signals should be interpreted within broader market trends
- **Confirmation**: Use additional indicators (RSI, volume) for signal confirmation

### Example Trading Logic
```python
if z_score > 2:
    recommendation = "SELL - Overbought condition"
elif z_score < -2:
    recommendation = "BUY - Oversold condition"
else:
    recommendation = "HOLD - Normal trading range"
```

## 🚀 Usage Examples

### Basic Analysis
```python
# Calculate Z-score for Apple stock
result = calculate_bollinger_z_score("AAPL", period=20)
print(result)
```

### AI-Powered Recommendations
```python
# Get trading recommendation using LangGraph agent
response = graph.invoke({
    "messages": [("user", "Should I buy or sell TSLA based on Bollinger Z-score?")]
})
```

## 📚 Educational Value

These notebooks serve as comprehensive educational resources for:

- **Quantitative Finance**: Understanding statistical measures in trading
- **Technical Analysis**: Practical application of Bollinger Bands
- **AI Integration**: Modern approaches to algorithmic trading
- **Risk Management**: Interpreting signals within market context
- **Data Science**: Real-world application of statistical concepts

## ⚠️ Important Disclaimers

1. **Educational Purpose**: These tools are for learning and research only
2. **Not Financial Advice**: All trading decisions should involve professional consultation
3. **Market Risks**: Past performance does not guarantee future results
4. **Backtesting Required**: Strategies should be thoroughly tested before implementation
5. **Risk Management**: Always use proper position sizing and stop-losses

## 🔄 Future Enhancements

Potential improvements for the codebase:
- Integration with real-time data feeds
- Advanced risk management features
- Portfolio-level analysis capabilities
- Backtesting framework implementation
- Additional technical indicators integration
- Web-based dashboard using Streamlit

This implementation demonstrates the powerful combination of traditional technical analysis with modern AI frameworks, providing both educational value and practical trading insights.
</artifact>

I've created a comprehensive README that explains both notebooks and the financial techniques they implement. The document covers:

**Financial Concepts**:
- Standard deviation and its role in measuring volatility
- Z-scores and their interpretation in trading
- Bollinger Bands theory and practical application
- Trading signal generation and risk management

**Technical Implementation**:
- Detailed explanation of both notebooks' purposes and features
- Code examples showing Bollinger Bands calculations
- LangGraph integration for AI-powered trading recommendations
- Environment setup and dependency requirements

**Educational Value**:
- Step-by-step breakdown of statistical concepts
- Real-world trading applications
- Risk management considerations
- Practical usage examples

The README serves as both a technical guide and educational resource, making these complex financial concepts accessible while highlighting the practical implementation using modern AI frameworks. The document emphasizes that these are educational tools and includes appropriate disclaimers about financial risks.