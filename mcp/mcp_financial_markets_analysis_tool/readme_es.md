# Servidor MCP de Análisis Financiero

Un servidor integral del Protocolo de Contexto de Modelo (MCP) que proporciona herramientas avanzadas de análisis técnico para mercados financieros. Este servidor se integra con Claude Desktop e incluye una interfaz de línea de comandos para análisis sofisticado de estrategias de trading, performance backtesting y capacidades de market scanning.

## Descripción General

El Servidor MCP de Análisis Financiero implementa cinco estrategias distintas de análisis técnico con capacidades integrales de performance backtesting. El sistema proporciona tanto un servidor MCP para integración con Claude Desktop como una herramienta de línea de comandos independiente para ejecución directa de análisis.

### Estrategias de Trading Principales

**Bollinger Z-Score Analysis**
Estrategia de mean reversion utilizando Z-scores estadísticos para identificar condiciones de overbought y oversold dentro de los canales de Bollinger Bands.

**Bollinger-Fibonacci Strategy**
Análisis de support y resistance que combina Bollinger Bands con Fibonacci retracements para identificar niveles clave de precios y puntos de reversión.

**MACD-Donchian Combined Strategy**
Estrategia de momentum y breakout utilizando indicadores Moving Average Convergence Divergence (MACD) con señales de breakout de Donchian channels.

**Connors RSI + Z-Score Strategy**
Análisis de momentum a corto plazo con componentes de mean reversion, combinando la metodología Connors RSI con cálculos estadísticos de Z-score.

**Dual Moving Average Strategy**
Estrategia de trend-following implementando crossovers de exponential moving averages con períodos configurables para identificación de tendencias.

### Capacidades de Análisis

**Performance Backtesting**
Análisis integral de rendimiento histórico comparando strategy returns contra buy-and-hold baselines con métricas detalladas incluyendo Sharpe ratios, maximum drawdown y win rates.

**Market Scanner**
Capacidad de análisis multi-símbolo para evaluación simultánea de múltiples valores con ranking y análisis comparativo a través de todas las estrategias implementadas.

**Risk Assessment**
Métricas avanzadas de riesgo incluyendo análisis de volatility, cálculos de drawdown y recomendaciones de position sizing basadas en rendimiento histórico.

**Signal Generation**
Recomendaciones en tiempo real de buy, sell y hold con confidence scoring basada en condiciones actuales del mercado y rendimiento histórico de estrategias.

## Requisitos Previos

- Python 3.11 o superior
- Gestor de paquetes UV para manejo de dependencias
- Claude Desktop con soporte MCP (para integración del servidor)
- Conectividad a internet para acceso a datos de Yahoo Finance
- Clave API de OpenAI (para funcionalidad de herramienta CLI)

## Instalación

### Instalación del Servidor

```bash
# Crear directorio del proyecto
mkdir financial-mcp-server
cd financial-mcp-server

# Inicializar con uv
uv init .

# Instalar dependencias principales
uv add mcp fastmcp yfinance pandas numpy

# Instalar dependencias adicionales de análisis
uv add python-docx docx2pdf scipy scikit-learn
```

### Instalación de Herramienta CLI

```bash
# Instalar dependencias adicionales para CLI
pip install openai python-dotenv

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu clave API de OpenAI
```

## Estructura del Proyecto

```
financial-mcp-server/
├── server/
│   ├── main.py                     # Punto de entrada principal del servidor MCP
│   ├── strategies/                 # Módulos de estrategias de trading
│   │   ├── bollinger_zscore.py     # Z-Score mean reversion
│   │   ├── bollinger_fibonacci.py  # Bollinger-Fibonacci strategy
│   │   ├── macd_donchian.py       # MACD-Donchian momentum
│   │   ├── connors_zscore.py      # Connors RSI analysis
│   │   ├── dual_moving_average.py # EMA crossover strategy
│   │   ├── performance_tools.py   # Herramientas de performance comparison
│   │   ├── comprehensive_analysis.py # Análisis multi-estrategia
│   │   └── unified_market_scanner.py # Herramientas de market scanning
│   └── utils/
│       └── yahoo_finance_tools.py  # Utilidades de market data
├── stock_analyzer.py              # Aplicación CLI
├── analyze.py                     # Wrapper CLI simple
├── requirements.txt               # Dependencias de Python
├── .env.example                   # Plantilla de entorno
└── tests/                         # Suite de pruebas
```

## Configuración de Claude Desktop

Agrega lo siguiente a la configuración MCP de Claude Desktop:

```json
{
  "mcpServers": {
    "finance-tools": {
      "command": "uv",
      "args": ["--directory", "/ruta/a/financial-mcp-server", "run", "python", "server/main.py"],
      "env": {}
    }
  }
}
```

## Uso de Interfaz de Línea de Comandos

### Análisis Básico

Ejecuta análisis técnico integral en valores individuales:

```bash
# Analizar acciones de Apple
python stock_analyzer.py AAPL

# Analizar Microsoft con salida detallada
python stock_analyzer.py MSFT --verbose

# Usando wrapper simplificado
python analyze.py TSLA
```

### Características del CLI

**Symbol Validation**
Validación automática de ticker symbols contra disponibilidad de datos de Yahoo Finance antes de la ejecución del análisis.

**Comprehensive Reporting**
Los reportes markdown generados incluyen executive summaries, métricas de rendimiento de estrategias individuales, tablas de análisis comparativo y recomendaciones de inversión.

**Error Handling**
Manejo robusto de errores para problemas de conectividad de red, símbolos inválidos y escenarios de finalización parcial de análisis.

**OpenAI Integration**
La herramienta CLI utiliza modelos de OpenAI para orquestar la ejecución del análisis y proporcionar interpretación inteligente de resultados.

### Opciones del CLI

```bash
stock_analyzer.py [-h] [--verbose] symbol

argumentos posicionales:
  symbol         Símbolo de Yahoo Finance stock para análisis

argumentos opcionales:
  -h, --help     Mostrar mensaje de ayuda y salir
  --verbose, -v  Habilitar salida de logging detallada
```

### Configuración de Entorno

Crea un archivo `.env` con las credenciales API requeridas:

```bash
OPENAI_API_KEY=tu_clave_api_openai_aqui
OPENAI_MODEL=gpt-4
```

## Arquitectura Técnica

### Integración MCP

El servidor utiliza el framework FastMCP para integración con Claude Desktop:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("finance tools", "1.0.0")

# Registrar strategy tools
register_bollinger_fibonacci_tools(mcp)
register_macd_donchian_tools(mcp)
register_connors_zscore_tools(mcp)
register_dual_ma_tools(mcp)
register_bollinger_zscore_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport='stdio')
```

### Patrón de Implementación de Estrategias

Cada trading strategy sigue un patrón de implementación estandarizado:

1. **Data Acquisition** - Integración con Yahoo Finance API para historical price data
2. **Indicator Calculation** - Cálculos de análisis técnico usando pandas y numpy
3. **Signal Generation** - Lógica de recomendaciones buy, sell y hold
4. **Performance Backtesting** - Validación histórica de estrategias con métricas integrales
5. **Report Generation** - Salida markdown estructurada con analysis summaries

### Performance Metrics

El sistema implementa evaluación integral de performance:

```python
def calculate_strategy_performance_metrics(signals_data, signal_column):
    # Calcular total returns, annualized returns, volatility
    # Generar Sharpe ratios, maximum drawdown analysis
    # Calcular win rates y average holding periods
    # Comparar contra buy-and-hold baseline performance
    return performance_metrics
```

## Parámetros de Configuración

### Opciones de Time Period

Períodos de análisis válidos: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

### Strategy Parameters

**Bollinger Bands Configuration**
- Window period: 20 días (predeterminado)
- Standard deviations: 2 (predeterminado)

**MACD Parameters**
- Fast period: 12 días
- Slow period: 26 días  
- Signal period: 9 días

**Moving Average Configuration**
- Short period: 50 días
- Long period: 200 días
- Type: Simple Moving Average (SMA) o Exponential Moving Average (EMA)

**Z-Score Calculation**
- Window para mean y standard deviation: 20 días (predeterminado)

### Output Format Options

**Detailed Analysis**
Análisis completo con todas las performance metrics, strategy breakdowns y recomendaciones integrales.

**Summary Format**
Visión general condensada enfocándose en key findings y primary investment recommendations.

**Executive Summary**
Visión estratégica de alto nivel diseñada para executive decision-making processes.

## Suite de Testing

### Test Categories

**Unit Testing**
Pruebas unitarias integrales cubriendo individual strategy calculations, data validation y utility functions.

**Integration Testing**
Pruebas de end-to-end workflow incluyendo MCP server connectivity, CLI functionality y report generation.

**Performance Testing**
Validación de timing y memory usage para large dataset processing y multiple symbol analysis.

### Test Execution

```bash
# Ejecutar complete test suite
python -m pytest tests/ -v

# Ejecutar specific test categories
pytest -m unit           # Solo unit tests
pytest -m integration    # Integration tests
pytest -m performance    # Performance tests
```

## Risk Disclaimers

**Aviso Importante:** Este software se proporciona únicamente para fines educativos e informativos.

**Financial Risk Warning**
Todos los analysis results deben ser verificados independientemente antes de tomar investment decisions. Past performance no garantiza future results. Todas las trading e investment activities implican riesgo sustancial de financial loss.

**Technical Limitations**
El análisis técnico tiene inherent limitations y puede producir false signals. Strategy effectiveness varía entre diferentes market conditions y asset classes.

**Data Accuracy**
Los market data provienen de Yahoo Finance y pueden contener delays, inaccuracies o gaps. Los usuarios deben verificar data accuracy independientemente.

## Troubleshooting

### Problemas Comunes de Configuración

**MCP Server Connection Problems**
Verifica server script paths en la configuración de Claude Desktop. Asegúrate de que los Python y UV environments estén configurados correctamente con todas las required dependencies instaladas.

**Performance Optimization**
Las initial data downloads pueden requerir más de 30 segundos para completarse. Subsequent analyses típicamente se ejecutan más rápido debido al data caching. Considera shorter time periods para mejorar analysis speed.

**Data Access Issues**
Verifica que los ticker symbols estén formateados correctamente y se comercialicen activamente en supported exchanges. Confirma internet connectivity para Yahoo Finance API access. Algunas analysis tools requieren minimum historical data periods.

### Debug Mode

Habilita detailed logging para troubleshooting:

```python
import sys
print(f"Analyzing {symbol}...", file=sys.stderr)
```

## Contributing

### Agregar New Strategies

1. Crear nuevo strategy module en `server/strategies/`
2. Implementar core analysis functions siguiendo established patterns
3. Agregar comprehensive performance backtesting capabilities
4. Registrar strategy con main MCP server
5. Incluir thorough documentation y test coverage

### Extender Analysis Capabilities

- Implementar additional technical indicators
- Desarrollar enhanced risk assessment metrics
- Crear sector-specific analysis tools
- Mejorar report formatting y visualization

## Recursos Técnicos

### Model Context Protocol Documentation
- [Official MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Concepts and Architecture](https://modelcontextprotocol.io/docs/concepts/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)

### Technical Analysis References

**Bollinger Bands**
Statistical price channels utilizando moving averages y standard deviations para volatility analysis e identificación de mean reversion.

**MACD (Moving Average Convergence Divergence)**
Momentum oscillator comparando exponential moving averages para identificar trend changes y momentum shifts.

**Fibonacci Retracements**
Technical analysis tool usando mathematical ratios para identificar potential support y resistance levels basados en previous price movements.

**Connors RSI**
Short-term momentum indicator combinando traditional RSI con streak analysis y percentile ranking para enhanced mean reversion signals.

**Donchian Channels**
Breakout analysis system usando highest high y lowest low values durante specified periods para identificar potential breakout opportunities.

### Market Data Sources

**Yahoo Finance Integration**
Acceso gratuito a historical y real-time market data cubriendo global equities, indices, currencies y commodities con comprehensive API access.

**Data Coverage Limitations**
Sujeto a Yahoo Finance API rate limits y data availability constraints. Algunos international markets pueden tener limited historical data coverage.

## Licencia

Este proyecto se proporciona para fines educativos. Los usuarios deben cumplir con:
- Yahoo Finance Terms of Service para market data usage
- OpenAI Terms of Service para API integration
- Anthropic Terms of Service para Claude API usage
- Regulaciones locales aplicables respecto a financial analysis tools

---

**Technology Stack:** Python, FastMCP, Yahoo Finance API, OpenAI API, Claude Desktop
**Versión:** 1.0.0