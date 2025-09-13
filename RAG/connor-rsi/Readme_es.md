# Estrategia de Trading Connors RSI con LangGraph

Una implementación sofisticada de estrategia de trading que presenta el indicador Connors RSI combinado con análisis Z-Score para señales mejoradas de reversión a la media. Este sistema utiliza LangGraph para crear un agente inteligente que proporciona análisis técnico integral y recomendaciones de trading.

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Técnicas Financieras](#técnicas-financieras)
- [Sistema de Puntuación](#sistema-de-puntuación)
- [Descripción de Notebooks](#descripción-de-notebooks)
- [Instalación](#instalación)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Características Principales](#características-principales)
- [Implementación Técnica](#implementación-técnica)
- [Señales de Trading](#señales-de-trading)
- [Análisis de Rendimiento](#análisis-de-rendimiento)
- [Mejores Prácticas](#mejores-prácticas)

## 🎯 Descripción General

Este proyecto implementa la estrategia de trading Connors RSI, un oscilador de momentum avanzado desarrollado por Larry Connors que combina tres componentes distintos para identificar condiciones de sobrecompra y sobreventa con mayor precisión que el RSI tradicional. La implementación incluye:

1. **Cálculo de Connors RSI** - Análisis de momentum multi-componente
2. **Integración Z-Score** - Confirmación estadística de reversión a la media
3. **Sistema de Puntuación Combinado** - Combinación ponderada de indicadores para señales de trading
4. **Agente LangGraph** - Análisis y recomendaciones potenciados por IA

## 📈 Técnicas Financieras

### Componentes del Connors RSI

El Connors RSI se calcula como el promedio de tres componentes con igual ponderación:

#### 1. RSI de Precios (33.33% de peso)
- **RSI tradicional** aplicado a precios de cierre
- **Período por Defecto**: 3 días (más sensible que el RSI estándar de 14 días)
- **Propósito**: Mide el momentum reciente de precios
- **Interpretación**: Valores > 50 indican momentum alcista, < 50 momentum bajista

#### 2. RSI de Rachas (33.33% de peso)  
- **RSI aplicado a rachas de precios** (movimientos consecutivos al alza/baja)
- **Período por Defecto**: 2 días
- **Proceso de Cálculo**:
  - Rastrear días consecutivos al alza (+1, +2, +3, etc.)
  - Rastrear días consecutivos a la baja (-1, -2, -3, etc.)
  - Aplicar RSI a esta serie de rachas
- **Propósito**: Mide la persistencia del movimiento direccional

#### 3. Rango Percentil (33.33% de peso)
- **Ranking percentil** de la tasa de cambio sobre ventana móvil
- **Período por Defecto**: 100 días
- **Cálculo**: Percentil del cambio de precio actual vs. rango histórico de 100 días
- **Propósito**: Proporciona contexto histórico para movimientos de precio actuales

### Fórmula del Connors RSI
```
CRSI = (RSI de Precio + RSI de Rachas + Rango Percentil) / 3
```

### Análisis Z-Score

El Z-Score mide cuántas desviaciones estándar está el precio actual de su media móvil:

```
Z-Score = (Precio Actual - Media Móvil) / Desviación Estándar
```

**Guías de Interpretación:**
- **Z > +2**: Precio significativamente sobre el promedio (potencial reversión a la baja)
- **Z < -2**: Precio significativamente bajo el promedio (potencial reversión al alza)
- **-2 ≤ Z ≤ +2**: Precio dentro del rango normal de trading

## 🔢 Sistema de Puntuación

### Conversión de Puntuación Connors RSI

El Connors RSI tradicional (0-100) se convierte a una puntuación estandarizada (-100 a +100):

```python
connors_score = (crsi - 50) * 2
```

### Cálculo de Puntuación Combinada

**Fórmula**: `(Puntuación Connors RSI × 70%) + (Z-Score × 30%)`

Esta ponderación da énfasis primario al momentum (Connors RSI) mientras usa Z-Score para confirmación de reversión a la media.

### Interpretación de Señales de Trading

| Rango de Puntuación | Señal | Condición del Mercado | Acción Recomendada |
|---------------------|-------|----------------------|-------------------|
| **+75 a +100** | 🟢 **Compra Fuerte** | Sobreventa extrema + posicionamiento favorable | Posición larga de alta convicción |
| **+50 a +75** | 🟢 **Compra** | Condiciones de sobreventa | Posición larga moderada |
| **+25 a +50** | 🟡 **Compra Débil** | Sesgo de sobreventa leve | Posición larga pequeña o esperar |
| **-25 a +25** | ⚪ **Neutral** | Rango normal | Mantener posiciones actuales |
| **-50 a -25** | 🟡 **Venta Débil** | Sesgo de sobrecompra leve | Reducir posiciones largas |
| **-75 a -50** | 🔴 **Venta** | Condiciones de sobrecompra | Cerrar largos o posición corta |
| **-100 a -75** | 🔴 **Venta Fuerte** | Sobrecompra extrema | Señal de corto fuerte |

## 📓 Descripción de Notebooks

### 1. `connor_rsi.ipynb`
**Propósito**: Implementación central y visualización

**Características Principales:**
- Cálculo completo de Connors RSI desde cero
- Visualizaciones interactivas con Plotly en layout de 3 paneles
- Análisis de componentes (RSI de Precio, RSI de Rachas, Rango Percentil)
- Generación de señales con marcadores de compra/venta
- Comparación de rendimiento vs. RSI tradicional

**Componentes de Visualización:**
- **Panel Superior**: Gráfico de precios con señales Connors RSI
- **Panel Medio**: Comparación de componentes RSI individuales
- **Panel Inferior**: Connors RSI principal con niveles de sobrecompra/sobreventa

### 2. `RAG_langgraph_connor_rsi.ipynb`
**Propósito**: Asistente de trading potenciado por IA usando LangGraph

**Características Principales:**
- Agente conversacional basado en LangGraph
- Descubrimiento y ejecución automática de herramientas
- Procesamiento de consultas en lenguaje natural
- Capacidades de análisis multi-símbolo
- Recomendaciones combinadas Connors RSI + Z-Score

**Herramientas Disponibles:**
- `@tool calculate_connors_rsi_score()`: Análisis completo de Connors RSI
- `@tool calculate_zscore_indicator()`: Cálculo e interpretación de Z-Score
- `@tool calculate_combined_connors_score()`: Puntuación de combinación ponderada
- `@tool interpret_connors_combined_score()`: Interpretación de señales

## ⚙️ Instalación

### Prerequisitos
```bash
# Dependencias principales
pip install pandas numpy plotly yfinance datetime

# Para asistente IA (notebook LangGraph)
pip install langchain langgraph langchain-openai
```

### Configuración del Entorno

Crear archivo `.env` para el asistente IA:
```bash
OPENAI_API_KEY=tu_clave_openai_aqui
```

### Inicio Rápido
```bash
# Clonar repositorio
git clone <url-repositorio>
cd RAG/connor-rsi

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar análisis básico
jupyter notebook connor_rsi.ipynb

# Ejecutar asistente IA
jupyter notebook RAG_langgraph_connor_rsi.ipynb
```

## 🚀 Ejemplos de Uso

### Análisis Básico

```python
# Calcular Connors RSI para acciones de Apple
symbol = "AAPL"
end_date = datetime.now()
start_date = end_date - timedelta(days=730)

# Descargar datos
data = yf.download(symbol, start=start_date, end=end_date)

# Calcular componentes Connors RSI
crsi_data = connors_rsi(data)
signals = generate_signals(crsi_data['CRSI'])

# Mostrar resultados
print(f"CRSI Actual: {crsi_data['CRSI'].iloc[-1]:.2f}")
print(f"Señal: {'COMPRA' if crsi_data['CRSI'].iloc[-1] < 20 else 'VENTA' if crsi_data['CRSI'].iloc[-1] > 80 else 'MANTENER'}")
```

### Uso del Asistente IA

```python
# Solicitud de análisis en lenguaje natural
result = analyze_stock("UBS", period="1y", zscore_window=20)

# El sistema:
# 1. Calculará la puntuación Connors RSI
# 2. Calculará el indicador Z-Score  
# 3. Computará la puntuación combinada
# 4. Proporcionará recomendación de trading con razonamiento
```

### Comparación Multi-Símbolo

```python
symbols = ["AAPL", "TSLA", "MSFT", "GOOGL"]
for symbol in symbols:
    analysis = analyze_stock(symbol, period="6mo")
    print(f"{symbol}: {analysis}")
```

## ✨ Características Principales

### Generación Avanzada de Señales

**Niveles Tradicionales:**
- **CRSI < 20**: Sobreventa (señal potencial de compra)
- **CRSI > 80**: Sobrecompra (señal potencial de venta)

**Confirmación Mejorada:**
- Combina momentum (Connors RSI) con reversión a la media (Z-Score)
- Reduce señales falsas mediante confirmación dual
- Proporciona niveles de confianza para cada señal

### Análisis de Componentes

```python
# Contribuciones de componentes individuales
print("Análisis de Componentes:")
print(f"RSI de Precio: {price_rsi_score:.2f}")
print(f"RSI de Rachas: {streak_rsi_score:.2f}")  
print(f"Rango Percentil: {percent_rank_score:.2f}")
print(f"Puntuación Combinada: {combined_score:.2f}")
```

### Parámetros Adaptativos

El sistema permite personalización de parámetros clave:
- **Período RSI**: Por defecto 3 (se puede ajustar para sensibilidad)
- **Período de Rachas**: Por defecto 2 (afecta cálculo de rachas)
- **Período de Ranking**: Por defecto 100 (ventana de contexto histórico)
- **Ventana Z-Score**: Por defecto 20 (marco temporal de reversión a la media)

## 🔧 Implementación Técnica

### Funciones de Cálculo Central

#### Cálculo RSI
```python
def rsi(series, period=14):
    """Calcular RSI tradicional"""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
```

#### Cálculo RSI de Rachas  
```python
def streak_rsi(series, period=2):
    """Calcular RSI de rachas de precios"""
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

#### Cálculo de Rango Percentil
```python
def percent_rank(series, period=100):
    """Calcular rango percentil sobre ventana móvil"""
    def rank_pct(x):
        if len(x) < 2:
            return 50.0
        current_value = x.iloc[-1]
        rank = (x < current_value).sum()
        return (rank / (len(x) - 1)) * 100
    
    return series.rolling(window=period).apply(rank_pct, raw=False)
```

### Arquitectura del Agente LangGraph

El asistente IA implementa un flujo de trabajo de agente sofisticado:

```python
# Gestión del estado del agente
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Chatbot con conocimiento financiero especializado
def chatbot(state: State):
    """Asistente de trading inteligente con experiencia en Connors RSI"""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}
```

## 📊 Señales de Trading

### Métricas de Calidad de Señales

El sistema proporciona varias métricas para evaluar la calidad de las señales:

#### Alineación de Componentes
- **Señales Fuertes**: Los tres componentes (RSI de Precio, RSI de Rachas, Rango Percentil) se alinean
- **Señales Moderadas**: Dos de tres componentes se alinean
- **Señales Débiles**: Solo un componente indica la dirección

#### Rendimiento Histórico
```python
# Ejemplo de métricas de efectividad de señales
buy_signals = (signals == 'BUY').sum()
sell_signals = (signals == 'SELL').sum()
print(f"Total Señales de Compra: {buy_signals}")
print(f"Total Señales de Venta: {sell_signals}")
```

### Gestión de Riesgo

#### Guías de Stop-Loss
- **Posiciones Largas**: Establecer stop en mínimo de swing reciente o -3% desde entrada
- **Posiciones Cortas**: Establecer stop en máximo de swing reciente o +3% desde entrada
- **Tamaño de Posición**: Ajustar basado en fuerza de señal y volatilidad

#### Filtrado de Señales
```python
# Filtrar señales para reducir ruido
def filter_signals(signals, min_gap_days=5):
    """Asegurar tiempo mínimo entre señales"""
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

## 📈 Análisis de Rendimiento

### Resultados de Backtesting

Características de rendimiento típicas observadas:

#### Análisis de Tesla (TSLA)
- **Señales Generadas**: Alta frecuencia debido a volatilidad
- **Mejor Rendimiento**: Durante períodos de tendencia con reversiones claras
- **Desafío**: Condiciones de whipsaw en períodos de alta volatilidad

#### Análisis de Apple (AAPL)  
- **Señales Generadas**: Frecuencia moderada, bien espaciadas
- **Mejor Rendimiento**: Identificación consistente de tendencias
- **Confiabilidad**: Mayor relación señal-ruido que TSLA

### Adaptación a Condiciones del Mercado

#### Mercados con Tendencia
- Connors RSI puede dar señales prematuras de reversión
- Z-Score proporciona contexto adicional de tendencia
- **Recomendación**: Usar marcos temporales más largos en tendencias fuertes

#### Mercados Laterales
- Condiciones óptimas para reversión a la media de Connors RSI
- Alta tasa de éxito para señales de sobrecompra/sobreventa
- **Recomendación**: Usar parámetros estándar

## 💡 Mejores Prácticas

### Optimización de Parámetros

#### Para Diferentes Clases de Activos
```python
# Acciones volátiles (como Tesla)
connors_params = {
    'rsi_period': 2,      # Más sensible
    'streak_period': 1,   # Respuesta más rápida
    'rank_period': 50     # Historia más corta
}

# Acciones estables (como Apple)  
connors_params = {
    'rsi_period': 3,      # Estándar
    'streak_period': 2,   # Estándar
    'rank_period': 100    # Historia completa
}
```

#### Análisis Multi-Marco Temporal
```python
# Confirmar señales a través de marcos temporales
daily_signal = calculate_connors_rsi_score("AAPL", period="1y")
weekly_signal = calculate_connors_rsi_score("AAPL", period="2y")

# Solo operar cuando ambos marcos temporales concuerden
if daily_signal < -60 and weekly_signal < -40:
    recommendation = "COMPRA FUERTE"
```

### Reglas de Gestión de Riesgo

1. **Nunca arriesgar más del 2% por operación**
2. **Combinar con análisis de tendencia** para contexto
3. **Usar dimensionamiento de posición** basado en fuerza de señal
4. **Implementar stop-losses** consistentemente
5. **Monitorear correlación** entre posiciones

### Monitoreo del Sistema

```python
# Rastrear rendimiento del sistema
def monitor_performance(signals, prices):
    """Calcular métricas básicas de rendimiento"""
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

## 🔮 Características Avanzadas

### Análisis Multi-Activo

El sistema soporta análisis a nivel de cartera:

```python
# Analizar múltiples activos simultáneamente
portfolio = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
results = {}

for symbol in portfolio:
    analysis = analyze_stock(symbol, period="6mo", zscore_window=20)
    results[symbol] = analysis

# Clasificar por fuerza de señal
sorted_signals = sorted(results.items(), key=lambda x: x[1]['combined_score'], reverse=True)
```

### Sistema de Alertas Personalizado

```python
def check_signals(symbols, threshold=60):
    """Verificar señales fuertes en lista de seguimiento"""
    alerts = []
    
    for symbol in symbols:
        score = get_current_score(symbol)
        if abs(score) > threshold:
            alerts.append({
                'symbol': symbol,
                'score': score,
                'signal': 'COMPRA' if score > threshold else 'VENTA',
                'timestamp': datetime.now()
            })
    
    return alerts
```

## 📚 Recursos Educativos

### Entendiendo Connors RSI

**Conceptos Clave:**
- **Reversión a la Media**: Tendencia de los precios a retornar al promedio
- **Osciladores de Momentum**: Indicadores que miden la tasa de cambio de precio  
- **Sobrecompra/Sobreventa**: Condiciones extremas de precio propensas a revertir
- **Análisis de Rachas**: Importancia de movimientos consecutivos de precio

### Lectura Recomendada

- **"Short Term Trading Strategies That Work"** por Larry Connors
- **"High Probability ETF Trading"** por Larry Connors  
- **Estudios de Análisis Técnico** sobre estrategias de reversión a la media
- **Papers académicos** sobre patrones de momentum y reversión

### Desarrollo Adicional

Mejoras potenciales para usuarios avanzados:

1. **Integración de Machine Learning**: Usar ML para optimizar parámetros
2. **Estrategias de Opciones**: Aplicar Connors RSI al trading de opciones
3. **Análisis Sectorial**: Análisis comparativo a través de sectores de mercado
4. **Alertas en Tiempo Real**: Integración con plataformas de trading
5. **Optimización de Cartera**: Dimensionamiento de posición ajustado por riesgo

## ⚠️ Descargos de Responsabilidad Importantes

- **Propósito Educativo**: Este sistema es solo para aprendizaje e investigación
- **No es Consejo Financiero**: Todas las decisiones de trading deben involucrar consulta profesional  
- **Riesgos de Mercado**: El rendimiento pasado no garantiza resultados futuros
- **Backtesting Requerido**: Siempre probar estrategias exhaustivamente antes de implementación
- **Gestión de Riesgo**: Usar dimensionamiento apropiado de posición y stop-losses consistentemente

## 🤝 Contribuir

### Oportunidades de Mejora

1. **Indicadores Adicionales**: Integrar con otros indicadores técnicos
2. **Optimización de Parámetros**: Algoritmos automáticos de ajuste de parámetros
3. **Análisis de Rendimiento**: Backtesting mejorado y métricas
4. **Visualización**: Tipos adicionales de gráficos y herramientas de análisis
5. **Integración**: Conectar con plataformas de trading y feeds de datos

### Pautas de Desarrollo

- Seguir el estilo de código existente y patrones de documentación
- Incluir testing comprehensivo para nuevas características  
- Proporcionar ejemplos claros e instrucciones de uso
- Mantener compatibilidad con implementaciones existentes
- Documentar cualquier cambio de parámetros o nuevas técnicas

---

**La estrategia Connors RSI representa un enfoque sofisticado al análisis técnico que combina conceptos tradicionales de momentum con técnicas estadísticas modernas. Cuando se implementa apropiadamente y se gestiona el riesgo, puede proporcionar insights valiosos para decisiones de trading a corto plazo y timing de mercado.**