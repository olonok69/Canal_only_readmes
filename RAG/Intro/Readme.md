# Financial Analysis RAG System

A comprehensive Retrieval-Augmented Generation (RAG) system for fundamental financial analysis using real-time financial data and AI-powered insights.

## Overview

This notebook implements a sophisticated financial analysis system that combines traditional fundamental analysis techniques with modern AI/ML capabilities. The system retrieves financial data, performs comprehensive analysis, and uses RAG to generate detailed financial reports and insights.

## Key Features

### 🔍 **Fundamental Analysis Implementation**
- **Balance Sheet Analysis**: Assets, liabilities, and equity examination
- **Income Statement Analysis**: Revenue, profitability, and expense tracking
- **Cash Flow Analysis**: Operating, investing, and financing cash flows
- **Financial Ratio Calculations**: Key performance indicators and ratios

### 🤖 **AI-Powered Insights**
- **RAG Architecture**: Combines retrieval with generative AI for contextual analysis
- **Vector Database**: Qdrant for efficient financial data storage and retrieval
- **LLM Integration**: Google's Gemini for intelligent financial interpretation

### 📊 **Data Visualization**
- Interactive financial charts and graphs
- Trend analysis with customizable formatting
- Multi-year comparison visualizations

## Financial Analysis Techniques

### 1. **Fundamental vs Technical Analysis**
The system focuses on fundamental analysis, which examines a company's intrinsic value through:
- Economic and financial factors
- Balance sheet strength
- Income statement performance
- Cash flow patterns

### 2. **Financial Statement Analysis**

#### **Balance Sheet Analysis**
```python
# Key metrics calculated:
- Total Assets vs Liabilities
- Debt-to-Equity Ratio (DER)
- Current vs Non-Current Assets/Liabilities
- Equity position tracking
```

#### **Income Statement Analysis**
```python
# Performance metrics:
- Revenue Growth Analysis
- Net Profit Margin (NPM)
- EBITDA Margin
- Year-over-year comparisons
```

#### **Cash Flow Analysis**
```python
# Cash flow components:
- Operating Cash Flow
- Investing Cash Flow  
- Financing Cash Flow
- Beginning vs Ending Cash Position
```

### 3. **Financial Ratios & KPIs**

#### **Profitability Ratios**
- **Net Profit Margin**: `Net Income / Total Revenue × 100`
- **EBITDA Margin**: `EBITDA / Total Revenue × 100`

#### **Leverage Ratios**
- **Debt-to-Equity Ratio**: `(Current + Non-Current Liabilities) / Equity × 100`

#### **Growth Analysis**
- Year-over-year percentage changes with 10% threshold significance
- Multi-period trend identification

## Technical Architecture

### **Data Sources**
- **Yahoo Finance API** (`yfinance`): Primary financial data source
- **Financial Modeling Prep API** (`fmpsdk`): Additional company profiles and metrics
- Real-time data fetching and processing

### **RAG Implementation**

#### **Vector Database Setup**
```python
# Qdrant Vector Store Configuration
- Collection: "rag-financial"
- Vector Size: 768 dimensions
- Distance Metric: Cosine similarity
- Embeddings: Google GenerativeAI embeddings
```

#### **Document Structure**
```json
{
  "company_description": "Business summary",
  "company_all_info": "Complete company metadata",
  "income_statement": "Processed IS data",
  "cash_flow": "CF analysis results", 
  "balance_sheet": "BS financial position"
}
```

### **AI Analysis Engine**

#### **Prompt Engineering**
The system uses structured prompts for consistent analysis:
- Company Profile Analysis
- Income Statement deep-dive
- Cash Flow examination
- Balance Sheet assessment
- Summary and recommendations

#### **Analysis Criteria**
- **Significance Threshold**: 10% change minimum for highlighting
- **Multi-period Comparison**: Tracks changes across fiscal years
- **Contextual Insights**: Relates financial changes to business context

## Data Processing Pipeline

### **1. Data Extraction**
```python
# Financial data retrieval
ticker = yf.Ticker("SYMBOL")
income_stmt = ticker.income_stmt
balance_sheet = ticker.balance_sheet
cash_flow = ticker.cash_flow
```

### **2. Data Transformation**
```python
def table_transform(df):
    # Transpose for proper orientation
    # Clean and format numerical data
    # Handle missing values and zeros
    # Apply reverse chronological order
```

### **3. Data Visualization**
```python
def format_numbers(x, pos):
    # Custom formatter for financial figures
    # Handles Trillions, Billions, Millions
    # Maintains readability for large numbers
```

### **4. Quality Control**
- **Zero-value filtering**: Removes rows with >70% zero values
- **Data validation**: Ensures numerical consistency
- **Missing data handling**: Robust error management

## Visualization Features

### **Chart Types**
1. **Revenue vs Net Profit**: Bar chart comparison
2. **Margin Analysis**: Line plots for NPM and EBITDA margins
3. **Balance Sheet Composition**: Stacked bar charts for assets/liabilities
4. **Debt Analysis**: Trend lines for leverage ratios
5. **Cash Flow Trends**: Multi-line cash flow component tracking

### **Visual Enhancements**
- Custom number formatting (T, B, M suffixes)
- Grid overlays for better readability
- Color-coded categories for different financial components
- Interactive legends and labels

## Installation & Setup

### **Required Dependencies**
```bash
pip install yfinance pandas matplotlib numpy streamlit
pip install langchain langchain-google-genai langchain-qdrant
pip install qdrant-client google-cloud-aiplatform
pip install fmpsdk python-dotenv
```

### **Environment Configuration**
```bash
# Required API Keys
GEMINI_API_KEY=your_gemini_api_key
FMP=your_financial_modeling_prep_api_key

# Google Cloud credentials
complete-tube-421007-208a4862c992.json
```

## Usage Examples

### **Basic Financial Analysis**
```python
# Initialize system for a company
ticker_symbol = "MSFT"
dat = yf.Ticker(ticker_symbol)

# Generate comprehensive analysis
analysis = qa_with_sources.invoke(
    "Please provide an overall financial analysis"
)
```

### **Custom Analysis Queries**
```python
# Specific financial questions
queries = [
    "What are the revenue growth trends?",
    "How has the debt-to-equity ratio changed?",
    "What's driving cash flow variations?",
    "Compare profitability across years"
]
```

## RAG Analysis Structure

The system generates structured financial reports covering:

### **Company Profile Section**
- Business description and operations
- Industry positioning and market context

### **Financial Performance Analysis**
1. **Income Statement Deep-dive**
   - Revenue growth patterns and drivers
   - Gross profit margin evolution
   - Net income trends and sustainability

2. **Cash Flow Assessment**
   - Operating cash generation efficiency
   - Investment activity analysis
   - Financing strategy evaluation

3. **Balance Sheet Strength**
   - Asset composition and quality
   - Capital structure optimization
   - Debt management effectiveness

### **Summary & Insights**
- Overall financial health assessment
- Key strengths and areas of concern
- Period-over-period performance summary

## Advanced Features

### **Threshold-Based Analysis**
- Automatically identifies significant changes (>10%)
- Highlights period-specific variations
- Provides percentage and absolute change metrics

### **Multi-Year Comparisons**
- Tracks financial evolution across multiple periods
- Identifies long-term trends and patterns
- Contextualizes short-term fluctuations

### **AI-Enhanced Interpretation**
- Natural language financial explanations
- Contextual business insights
- Automated report generation

## Future Enhancements

- **Industry Benchmarking**: Compare against sector averages
- **Predictive Analytics**: Forecast future performance
- **ESG Integration**: Environmental, Social, Governance factors
- **Risk Assessment**: Volatility and downside analysis
- **Portfolio Analysis**: Multi-company comparison tools

## Contributing

This system provides a robust foundation for financial analysis that can be extended with additional data sources, analysis techniques, and visualization capabilities.

## References

- [Investopedia: Fundamental vs Technical Analysis](https://www.investopedia.com/ask/answers/difference-between-fundamental-and-technical-analysis/)
- [Yahoo Finance API Documentation](https://pypi.org/project/yfinance/)
- [Financial Modeling Prep API](https://site.financialmodelingprep.com/)
- [Langchain Documentation](https://python.langchain.com/)
- [Qdrant Vector Database](https://qdrant.tech/)

---

**Note**: This system is designed for educational and research purposes. Always consult with qualified financial professionals for investment decisions.