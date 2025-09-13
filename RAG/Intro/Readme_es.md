# Sistema RAG para Análisis Financiero

Un sistema integral de Retrieval-Augmented Generation (RAG) para análisis fundamental financiero utilizando datos financieros en tiempo real e insights potenciados por IA.

## Descripción General

Este notebook implementa un sistema sofisticado de análisis financiero que combina técnicas tradicionales de análisis fundamental con capacidades modernas de IA/ML. El sistema extrae datos financieros, realiza análisis comprehensivo y utiliza RAG para generar reportes financieros detallados e insights.

## Características Principales

### 🔍 **Implementación de Análisis Fundamental**
- **Análisis de Balance Sheet**: Examen de assets, liabilities y equity
- **Análisis de Income Statement**: Seguimiento de revenue, profitability y expenses
- **Análisis de Cash Flow**: Operating, investing y financing cash flows
- **Cálculo de Financial Ratios**: Indicadores clave de rendimiento y ratios

### 🤖 **Insights Potenciados por IA**
- **Arquitectura RAG**: Combina retrieval con IA generativa para análisis contextual
- **Vector Database**: Qdrant para almacenamiento y recuperación eficiente de datos financieros
- **Integración LLM**: Gemini de Google para interpretación financiera inteligente

### 📊 **Visualización de Datos**
- Gráficos financieros interactivos
- Análisis de tendencias con formato personalizable
- Visualizaciones de comparación multi-año

## Técnicas de Análisis Financiero

### 1. **Análisis Fundamental vs Technical**
El sistema se enfoca en análisis fundamental, que examina el valor intrínseco de una empresa a través de:
- Factores económicos y financieros
- Solidez del balance sheet
- Performance del income statement
- Patrones de cash flow

### 2. **Análisis de Estados Financieros**

#### **Análisis de Balance Sheet**
```python
# Métricas clave calculadas:
- Total Assets vs Liabilities
- Debt-to-Equity Ratio (DER)
- Current vs Non-Current Assets/Liabilities
- Seguimiento de posición de equity
```

#### **Análisis de Income Statement**
```python
# Métricas de performance:
- Análisis de Revenue Growth
- Net Profit Margin (NPM)
- EBITDA Margin
- Comparaciones año a año
```

#### **Análisis de Cash Flow**
```python
# Componentes de cash flow:
- Operating Cash Flow
- Investing Cash Flow  
- Financing Cash Flow
- Beginning vs Ending Cash Position
```

### 3. **Financial Ratios y KPIs**

#### **Ratios de Profitability**
- **Net Profit Margin**: `Net Income / Total Revenue × 100`
- **EBITDA Margin**: `EBITDA / Total Revenue × 100`

#### **Ratios de Leverage**
- **Debt-to-Equity Ratio**: `(Current + Non-Current Liabilities) / Equity × 100`

#### **Análisis de Growth**
- Cambios porcentuales año a año con umbral de significancia del 10%
- Identificación de tendencias multi-período

## Arquitectura Técnica

### **Fuentes de Datos**
- **Yahoo Finance API** (`yfinance`): Fuente principal de datos financieros
- **Financial Modeling Prep API** (`fmpsdk`): Perfiles adicionales de empresas y métricas
- Extracción y procesamiento de datos en tiempo real

### **Implementación RAG**

#### **Configuración de Vector Database**
```python
# Configuración Qdrant Vector Store
- Collection: "rag-financial"
- Vector Size: 768 dimensiones
- Distance Metric: Similitud coseno
- Embeddings: Google GenerativeAI embeddings
```

#### **Estructura de Document**
```json
{
  "company_description": "Resumen del negocio",
  "company_all_info": "Metadata completa de la empresa",
  "income_statement": "Datos procesados del IS",
  "cash_flow": "Resultados del análisis CF", 
  "balance_sheet": "Posición financiera BS"
}
```

### **Motor de Análisis IA**

#### **Prompt Engineering**
El sistema utiliza prompts estructurados para análisis consistente:
- Análisis de Company Profile
- Deep-dive del Income Statement
- Examen de Cash Flow
- Evaluación de Balance Sheet
- Summary y recomendaciones

#### **Criterios de Análisis**
- **Umbral de Significancia**: Cambio mínimo del 10% para resaltar
- **Comparación Multi-período**: Rastrea cambios a través de años fiscales
- **Insights Contextuales**: Relaciona cambios financieros con contexto empresarial

## Pipeline de Procesamiento de Datos

### **1. Extracción de Datos**
```python
# Extracción de datos financieros
ticker = yf.Ticker("SYMBOL")
income_stmt = ticker.income_stmt
balance_sheet = ticker.balance_sheet
cash_flow = ticker.cash_flow
```

### **2. Transformación de Datos**
```python
def table_transform(df):
    # Transpose para orientación apropiada
    # Limpia y formatea datos numéricos
    # Maneja valores faltantes y ceros
    # Aplica orden cronológico inverso
```

### **3. Visualización de Datos**
```python
def format_numbers(x, pos):
    # Formatter personalizado para cifras financieras
    # Maneja Trillones, Billones, Millones
    # Mantiene legibilidad para números grandes
```

### **4. Control de Calidad**
- **Filtrado de valores cero**: Elimina filas con >70% valores cero
- **Validación de datos**: Asegura consistencia numérica
- **Manejo de datos faltantes**: Gestión robusta de errores

## Características de Visualización

### **Tipos de Gráficos**
1. **Revenue vs Net Profit**: Comparación con gráficos de barras
2. **Análisis de Margin**: Line plots para NPM y EBITDA margins
3. **Composición de Balance Sheet**: Gráficos de barras apiladas para assets/liabilities
4. **Análisis de Debt**: Líneas de tendencia para leverage ratios
5. **Tendencias de Cash Flow**: Seguimiento multi-línea de componentes de cash flow

### **Mejoras Visuales**
- Formato personalizado de números (sufijos T, B, M)
- Grid overlays para mejor legibilidad
- Categorías codificadas por color para diferentes componentes financieros
- Legends y labels interactivos

## Instalación y Configuración

### **Dependencias Requeridas**
```bash
pip install yfinance pandas matplotlib numpy streamlit
pip install langchain langchain-google-genai langchain-qdrant
pip install qdrant-client google-cloud-aiplatform
pip install fmpsdk python-dotenv
```

### **Configuración del Environment**
```bash
# API Keys requeridas
GEMINI_API_KEY=tu_gemini_api_key
FMP=tu_financial_modeling_prep_api_key

# Credenciales de Google Cloud
complete-tube-421007-208a4862c992.json
```

## Ejemplos de Uso

### **Análisis Financiero Básico**
```python
# Inicializar sistema para una empresa
ticker_symbol = "MSFT"
dat = yf.Ticker(ticker_symbol)

# Generar análisis comprehensivo
analysis = qa_with_sources.invoke(
    "Por favor proporciona un análisis financiero general"
)
```

### **Queries de Análisis Personalizados**
```python
# Preguntas financieras específicas
queries = [
    "¿Cuáles son las tendencias de crecimiento de revenue?",
    "¿Cómo ha cambiado el debt-to-equity ratio?",
    "¿Qué está impulsando las variaciones de cash flow?",
    "Compara la profitability a través de los años"
]
```

## Estructura de Análisis RAG

El sistema genera reportes financieros estructurados que cubren:

### **Sección de Company Profile**
- Descripción del negocio y operaciones
- Posicionamiento en la industria y contexto de mercado

### **Análisis de Performance Financiero**
1. **Deep-dive del Income Statement**
   - Patrones de revenue growth y drivers
   - Evolución del gross profit margin
   - Tendencias de net income y sostenibilidad

2. **Evaluación de Cash Flow**
   - Eficiencia de generación de operating cash
   - Análisis de actividad de investment
   - Evaluación de estrategia de financing

3. **Solidez del Balance Sheet**
   - Composición y calidad de assets
   - Optimización de capital structure
   - Efectividad del debt management

### **Summary e Insights**
- Evaluación general de salud financiera
- Fortalezas clave y áreas de preocupación
- Summary de performance período a período

## Características Avanzadas

### **Análisis Basado en Threshold**
- Identifica automáticamente cambios significativos (>10%)
- Resalta variaciones específicas de período
- Proporciona métricas de cambio porcentual y absoluto

### **Comparaciones Multi-Año**
- Rastrea evolución financiera a través de múltiples períodos
- Identifica tendencias y patrones de largo plazo
- Contextualiza fluctuaciones de corto plazo

### **Interpretación Mejorada por IA**
- Explicaciones financieras en lenguaje natural
- Insights contextuales de negocio
- Generación automatizada de reportes

## Mejoras Futuras

- **Industry Benchmarking**: Comparar contra promedios del sector
- **Predictive Analytics**: Forecasting de performance futura
- **Integración ESG**: Factores Environmental, Social, Governance
- **Risk Assessment**: Análisis de volatility y downside
- **Portfolio Analysis**: Herramientas de comparación multi-empresa

## Contribuciones

Este sistema proporciona una base robusta para análisis financiero que puede extenderse con fuentes de datos adicionales, técnicas de análisis y capacidades de visualización.

## Referencias

- [Investopedia: Fundamental vs Technical Analysis](https://www.investopedia.com/ask/answers/difference-between-fundamental-and-technical-analysis/)
- [Documentación Yahoo Finance API](https://pypi.org/project/yfinance/)
- [Financial Modeling Prep API](https://site.financialmodelingprep.com/)
- [Documentación Langchain](https://python.langchain.com/)
- [Qdrant Vector Database](https://qdrant.tech/)

---

**Nota**: Este sistema está diseñado para propósitos educativos y de investigación. Siempre consulta con profesionales financieros calificados para decisiones de inversión.