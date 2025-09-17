# CLTV Analysis Tool

A comprehensive mortgage lending analysis application that combines traditional Combined Loan-to-Value (CLTV) calculations with AI-powered risk assessment and borrower qualification analysis.

## Overview

This application provides mortgage professionals, underwriters, and loan officers with advanced tools to analyze borrower risk profiles, calculate lending ratios, and generate comprehensive lending recommendations. The system combines traditional mortgage calculations with modern AI analysis to provide detailed insights into loan qualification scenarios.

## Features

### Core Analysis Capabilities
- **Combined Loan-to-Value (CLTV) Analysis**: Calculate and assess CLTV ratios including all liens against a property
- **Debt-to-Income (DTI) Calculations**: Front-end and back-end DTI analysis with loan program specific thresholds
- **Comprehensive Borrower Scoring**: Multi-factor risk assessment combining CLTV, DTI, credit scores, and employment history
- **Loan Scenario Comparisons**: Compare multiple loan structures and down payment scenarios
- **PMI/MIP Analysis**: Private Mortgage Insurance calculations and removal timelines
- **Debt Consolidation Impact**: Assess the effect of debt consolidation on loan qualification
- **Home Affordability Calculator**: Determine maximum purchase price based on income and debt parameters

### AI-Powered Features
- **Intelligent Risk Assessment**: LLM-based analysis of borrower profiles
- **Natural Language Interaction**: Chat interface for mortgage lending questions
- **Automated Recommendations**: AI-generated lending advice and improvement strategies
- **Compliance Analysis**: Automated checking against lending guidelines and regulations

### Loan Program Support
- Conventional Loans (Fannie Mae/Freddie Mac)
- FHA Loans
- VA Loans
- USDA Rural Development Loans

## Installation

### Prerequisites
- Python 3.12 or higher
- Required API keys for AI features (OpenAI or Google Vertex AI)

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd cltv
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   # Choose your AI provider
   MODEL_PROVIDER=openai  # or 'vertexai'
   
   # For OpenAI
   OPENAI_API_KEY=your_openai_api_key_here
   
   # For Google Vertex AI
   GOOGLE_CLOUD_PROJECT=your_project_id
   # Ensure Google Cloud credentials are configured
   ```

4. **Verify Installation**
   ```bash
   python basic_analysis.py
   ```

## Usage

### Command Line Interface

#### Basic Borrower Analysis
```bash
python basic_analysis.py
```
This runs a sample comprehensive borrower analysis with predefined parameters.

#### Quick Loan Prequalification
```bash
python prequalification.py
```
Performs a streamlined prequalification analysis.

### Streamlit Web Interface

#### Enhanced CLTV Simulator (Recommended)
```bash
streamlit run cltv_simulator_enhanced.py
```
- Complete interface with traditional and AI-powered analysis
- Multiple analysis modes and tools
- Interactive visualizations and scenario modeling

#### Traditional CLTV Simulator
```bash
streamlit run cltv_simulator.py
```
- Classic CLTV calculator interface
- Scenario analysis and risk assessment
- Educational content about CLTV concepts

#### AI-Powered Analysis Interface
```bash
streamlit run cltv_simulator_ai.py
```
- Focused on AI-driven analysis capabilities
- Natural language interaction
- Advanced borrower risk assessment

#### Chat Interface
```bash
streamlit run cltv_chat_interface.py
```
- Interactive chat with AI lending assistant
- Real-time mortgage lending advice
- Example prompts and guided interactions

## API Reference

### Core Analysis Functions

#### `analyze_borrower_comprehensive()`
Performs complete borrower analysis using all available assessment tools.

```python
from cltv_ai_agent import analyze_borrower_comprehensive

result = analyze_borrower_comprehensive(
    property_value=500000.0,
    primary_loan_amount=400000.0,
    gross_monthly_income=8000.0,
    monthly_debt_payments=800.0,
    proposed_housing_payment=3200.0,
    credit_score=740,
    down_payment=100000.0,
    secondary_loans=[25000.0],
    employment_years=3.5,
    liquid_assets=50000.0,
    loan_type="conventional"
)
```

#### `quick_loan_prequalification()`
Streamlined prequalification analysis for initial borrower screening.

```python
from cltv_ai_agent import quick_loan_prequalification

result = quick_loan_prequalification(
    property_value=500000.0,
    down_payment=100000.0,
    gross_monthly_income=8000.0,
    monthly_debt_payments=800.0,
    credit_score=740
)
```

### Analysis Tools

#### CLTV Analysis Tool
```python
from cltv_ai_agent import create_cltv_agent
from langchain_core.messages import HumanMessage

graph = create_cltv_agent()
config = {"configurable": {"thread_id": "analysis_session"}}

# Use calculate_cltv_analysis tool
result = graph.invoke({
    "messages": [HumanMessage(content="""
    Use calculate_cltv_analysis with:
    - Property Value: 500000
    - Primary Loan: 400000
    - Secondary Loans: [25000]
    - Down Payment: 100000
    """)]
}, config)
```

#### DTI Analysis Tool
```python
# Use calculate_dti_analysis tool through the agent
result = graph.invoke({
    "messages": [HumanMessage(content="""
    Use calculate_dti_analysis with:
    - Gross Monthly Income: 8000
    - Monthly Debt Payments: 800
    - Proposed Housing Payment: 3200
    - Loan Type: conventional
    """)]
}, config)
```

### Advanced Tools

#### PMI Analysis
```python
from mortgage_tools import calculate_pmi_analysis

result = calculate_pmi_analysis(
    loan_amount=400000.0,
    property_value=500000.0,
    credit_score=740,
    loan_type="conventional"
)
```

#### Debt Consolidation Analysis
```python
from mortgage_tools import analyze_debt_consolidation_impact

result = analyze_debt_consolidation_impact(
    current_monthly_debts=1200.0,
    debt_balances="[15000, 8000, 12000, 5000]",
    consolidation_amount=40000.0,
    new_payment=800.0,
    gross_monthly_income=8000.0
)
```

#### Home Affordability Calculator
```python
from mortgage_tools import calculate_affordability_analysis

result = calculate_affordability_analysis(
    gross_monthly_income=8000.0,
    monthly_debt_payments=800.0,
    down_payment_available=100000.0,
    target_dti=36.0,
    interest_rate=6.5,
    loan_term=30
)
```

## Configuration

### AI Provider Configuration

#### OpenAI Configuration
```env
MODEL_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

#### Google Vertex AI Configuration
```env
MODEL_PROVIDER=vertexai
GOOGLE_CLOUD_PROJECT=your-project-id
```
Ensure Google Cloud SDK is installed and authenticated.

### Application Settings

The application supports various configuration options through environment variables and runtime parameters:

- **Model Provider**: Choose between OpenAI and Google Vertex AI
- **Analysis Depth**: Configure comprehensive vs. quick analysis modes
- **Risk Thresholds**: Customize CLTV and DTI risk level boundaries
- **Loan Program Parameters**: Adjust lending guidelines for different loan types

## Project Structure

```
cltv/
├── cltv_simulator.py              # Traditional CLTV calculator interface
├── cltv_simulator_ai.py           # AI-enhanced analysis interface
├── cltv_simulator_enhanced.py     # Complete enhanced interface
├── cltv_chat_interface.py         # Chat-based interaction interface
├── cltv_ai_agent.py              # Core AI agent and analysis engine
├── mortgage_tools.py              # Advanced mortgage analysis tools
├── basic_analysis.py              # Command-line analysis script
├── prequalification.py            # Quick prequalification script
├── requirements.txt               # Python dependencies
├── pyproject.toml                # Project configuration
├── .env                          # Environment variables (user-created)
├── .gitignore                    # Git ignore patterns
└── README.md                     # This documentation
```

## Error Handling

The application includes comprehensive error handling for common scenarios:

- **Missing API Keys**: Graceful degradation to traditional analysis
- **Invalid Input Parameters**: Validation and user-friendly error messages
- **Network Connectivity Issues**: Retry logic and offline mode capabilities
- **Model API Failures**: Fallback to alternative analysis methods

## Performance Considerations

- **Caching**: AI analysis results are cached to improve response times
- **Batch Processing**: Multiple borrower analyses can be processed efficiently
- **Resource Management**: Memory usage is optimized for large-scale processing

## Security Notes

- API keys are stored in environment variables, not in code
- Sensitive borrower data is processed locally when possible
- All external API communications use secure protocols
- No borrower data is permanently stored by default

## Contributing

This application is designed for mortgage lending professionals and can be extended with additional analysis tools, loan programs, or AI capabilities. The modular architecture supports easy integration of new features.

## Support

For technical support or feature requests, refer to the inline documentation and code comments. The application includes extensive logging for troubleshooting purposes.

## Disclaimer

This tool is designed for professional mortgage lending analysis and educational purposes. All lending decisions should be made in accordance with applicable regulations and guidelines. Users should verify calculations and recommendations with current lending standards and legal requirements.