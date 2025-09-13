# Análisis de Bandas de Bollinger y Z-Score para Trading Financiero

Este repositorio contiene dos notebooks de Jupyter que implementan análisis de Bandas de Bollinger y cálculos de Z-Score para estrategias de trading financiero. La implementación demuestra tanto conceptos educativos como aplicaciones prácticas utilizando frameworks modernos de IA.

## 📊 Conceptos Financieros Fundamentales

### Desviación Estándar en Finanzas
La desviación estándar mide la cantidad de variación en un conjunto de datos. En los mercados financieros, cuantifica la volatilidad de precios - qué tanto el precio de una acción se desvía de su precio promedio durante un período específico.

**Ejemplo**: Si una acción promedia $100 con una desviación estándar de $5:
- 68% de los precios caen entre $95-$105 (1 desviación estándar)
- 95% de los precios caen entre $90-$110 (2 desviaciones estándar)
- 99.7% de los precios caen entre $85-$115 (3 desviaciones estándar)

Esto sigue la **Regla Empírica**, que establece que 99.7% de los valores en una distribución normal se encuentran dentro de 3 desviaciones estándar de la media.

### Z-Score en Trading
Un Z-Score mide cuántas desviaciones estándar está un valor de la media:
- **Z-Score = 0**: El precio iguala el promedio móvil
- **Z-Score positivo**: El precio está por encima del promedio (potencialmente sobrecomprado)
- **Z-Score negativo**: El precio está por debajo del promedio (potencialmente sobrevendido)

### Bandas de Bollinger
Desarrolladas por John Bollinger en los años 1980, las Bandas de Bollinger consisten en tres líneas:

1. **Banda Media (SMA)**: Promedio Móvil Simple de 20 períodos
2. **Banda Superior**: SMA + (2 × Desviación Estándar)
3. **Banda Inferior**: SMA - (2 × Desviación Estándar)

**Interpretación para Trading**:
- Precio cerca de la **banda superior**: Potencialmente sobrecomprado (señal de venta)
- Precio cerca de la **banda inferior**: Potencialmente sobrevendido (señal de compra)
- **Ancho de bandas**: Indica volatilidad (ancho = alta volatilidad, estrecho = baja volatilidad)

### Fórmula del Z-Score de Bollinger
```
Z-Score = (Precio Actual - Promedio Móvil) / Desviación Estándar
```

**Guías de Trading**:
- **Z > +2**: Condición de sobrecompra (considerar vender)
- **Z < -2**: Condición de sobreventa (considerar comprar)
- **-2 ≤ Z ≤ +2**: Rango de trading normal

## 📁 Estructura del Repositorio

### 1. `Bollinger_bands.ipynb`
**Notebook educativo enfocado en conceptos fundamentales y visualización**

**Características Principales**:
- Explicación comprensiva de desviación estándar y puntajes Z
- Ejemplos prácticos usando distribuciones de altura de pingüinos emperador
- Cálculo paso a paso de Bandas de Bollinger
- Visualizaciones interactivas usando Plotly
- Integración con agentes LangChain para análisis automatizado

**Implementación Técnica**:
```python
# Cálculo de Bandas de Bollinger
data['SMA'] = data['Close'].rolling(window=20).mean()
data['SD'] = data['Close'].rolling(window=20).std()
data['UB'] = data['SMA'] + 2 * data['SD']  # Banda Superior
data['LB'] = data['SMA'] - 2 * data['SD']  # Banda Inferior
```

**Fuentes de Datos**: 
- API de Yahoo Finance (yfinance)
- Datos horarios de acciones durante períodos de 180 días
- Enfoque en acciones principales (AAPL, UBS, TSLA)

### 2. `RAG_Langgraph_z-score.ipynb`
**Implementación lista para producción usando LangGraph para recomendaciones automatizadas de trading**

**Características Principales**:
- Herramienta personalizada para cálculo de Z-Score en tiempo real
- Recomendaciones de trading potenciadas por IA
- Gestión de estado usando LangGraph
- Integración con modelos GPT-4 de OpenAI
- Persistencia de memoria para contexto de conversación

**Implementación de Herramienta Principal**:
```python
@tool
def calculate_bollinger_z_score(symbol: str, period: int = 20) -> str:
    """Calcular Z-Score de Bollinger para cualquier símbolo de acción"""
    data = yf.download(symbol, period=f"{period+50}d")
    closes = data['Close']
    rolling_mean = closes.rolling(window=period).mean()
    rolling_std = closes.rolling(window=period).std()
    z_score = (closes - rolling_mean) / rolling_std
    return latest_z_score
```

**Capacidades del Agente IA**:
- Obtención y análisis automático de datos
- Recomendaciones contextuales de trading
- Soporte para conversaciones multi-turno
- Evaluación de riesgo basada en interpretación de Z-Score

## 🛠 Requisitos Técnicos

### Dependencias
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

### Configuración del Entorno
1. **Claves API Requeridas**:
   - Clave API de OpenAI para integración con GPT-4
   - Credenciales de Google Cloud para Vertex AI (opcional)

2. **Configuración**:
   ```python
   # archivo .env
   OPENAI_API_KEY=tu_clave_openai
   GEMINI_API_KEY=tu_clave_gemini
   PROJECT=tu_proyecto_gcp
   REGION=tu_region_gcp
   ```

## 📈 Implementación de Estrategia de Trading

### Generación de Señales
Los notebooks implementan un enfoque sistemático para generar señales de trading:

1. **Recolección de Datos**: Obtener datos históricos de precios
2. **Cálculo de Indicadores**: Computar Bandas de Bollinger y puntajes Z
3. **Análisis de Señales**: Evaluar condiciones de sobrecompra/sobreventa
4. **Evaluación de Riesgo**: Considerar contexto de tendencia y volatilidad
5. **Recomendación**: Proporcionar consejos de comprar/vender/mantener

### Consideraciones de Gestión de Riesgo
- **Señales Falsas**: Los puntajes Z pueden generar señales falsas en mercados con tendencia
- **Impacto de Volatilidad**: La alta volatilidad afecta el ancho de bandas y la confiabilidad de señales
- **Contexto de Tendencia**: Las señales deben interpretarse dentro de tendencias de mercado más amplias
- **Confirmación**: Usar indicadores adicionales (RSI, volumen) para confirmar señales

### Ejemplo de Lógica de Trading
```python
if z_score > 2:
    recomendacion = "VENDER - Condición de sobrecompra"
elif z_score < -2:
    recomendacion = "COMPRAR - Condición de sobreventa"
else:
    recomendacion = "MANTENER - Rango de trading normal"
```

## 🚀 Ejemplos de Uso

### Análisis Básico
```python
# Calcular Z-Score para acciones de Apple
resultado = calculate_bollinger_z_score("AAPL", period=20)
print(resultado)
```

### Recomendaciones Potenciadas por IA
```python
# Obtener recomendación de trading usando agente LangGraph
respuesta = graph.invoke({
    "messages": [("user", "¿Debería comprar o vender TSLA basado en el Z-Score de Bollinger?")]
})
```

## 📚 Valor Educativo

Estos notebooks sirven como recursos educativos comprensivos para:

- **Finanzas Cuantitativas**: Entender medidas estadísticas en trading
- **Análisis Técnico**: Aplicación práctica de Bandas de Bollinger
- **Integración de IA**: Enfoques modernos para trading algorítmico
- **Gestión de Riesgo**: Interpretar señales dentro del contexto de mercado
- **Ciencia de Datos**: Aplicación del mundo real de conceptos estadísticos

## ⚠️ Descargos de Responsabilidad Importantes

1. **Propósito Educativo**: Estas herramientas son solo para aprendizaje e investigación
2. **No es Consejo Financiero**: Todas las decisiones de trading deben involucrar consulta profesional
3. **Riesgos de Mercado**: El rendimiento pasado no garantiza resultados futuros
4. **Backtesting Requerido**: Las estrategias deben probarse exhaustivamente antes de la implementación
5. **Gestión de Riesgo**: Siempre usar dimensionamiento adecuado de posiciones y stop-losses

## 🔄 Mejoras Futuras

Mejoras potenciales para la base de código:
- Integración con feeds de datos en tiempo real
- Características avanzadas de gestión de riesgo
- Capacidades de análisis a nivel de portafolio
- Implementación de framework de backtesting
- Integración de indicadores técnicos adicionales
- Dashboard basado en web usando Streamlit

Esta implementación demuestra la poderosa combinación del análisis técnico tradicional con frameworks modernos de IA, proporcionando tanto valor educativo como insights prácticos de trading.