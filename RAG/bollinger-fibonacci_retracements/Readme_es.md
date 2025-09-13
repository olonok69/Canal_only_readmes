# Estrategia de Trading: Bandas de Bollinger y Retrocesos de Fibonacci

Una estrategia integral de análisis técnico que combina las Bandas de Bollinger con los niveles de retroceso de Fibonacci para generar señales de trading precisas mediante un sistema avanzado de puntuación.

## Tabla de Contenidos
- [Descripción General](#descripción-general)
- [Indicadores Técnicos](#indicadores-técnicos)
- [Implementación de la Estrategia](#implementación-de-la-estrategia)
- [Sistema de Puntuación](#sistema-de-puntuación)
- [Descripción de los Notebooks](#descripción-de-los-notebooks)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Instalación y Configuración](#instalación-y-configuración)

## Descripción General

Este repositorio contiene tres implementaciones progresivas de una estrategia sofisticada de trading que combina dos herramientas poderosas de análisis técnico:

1. **Bandas de Bollinger** - Para medir volatilidad e identificar condiciones de sobrecompra/sobreventa
2. **Retrocesos de Fibonacci** - Para identificar niveles potenciales de soporte y resistencia

La evolución de la estrategia abarca tres notebooks, desde una implementación básica hasta un asistente de trading potenciado por IA.

## Indicadores Técnicos

### Bandas de Bollinger

Las Bandas de Bollinger consisten en tres componentes:
- **Línea Media**: Media móvil (típicamente 20 períodos)
- **Banda Superior**: Media móvil + (2 × desviación estándar)
- **Banda Inferior**: Media móvil - (2 × desviación estándar)

**Métricas Clave:**
- **Indicador %B**: Muestra dónde está el precio relativo a las bandas
  - 0 = precio en la banda inferior
  - 0.5 = precio en la media móvil
  - 1 = precio en la banda superior
  - >1 = precio sobre la banda superior (sobrecompra)
  - <0 = precio bajo la banda inferior (sobreventa)

- **Ancho de Banda (Bandwidth)**: Mide volatilidad calculando la distancia entre bandas
  - Valores altos = alta volatilidad (bandas muy separadas)
  - Valores bajos = baja volatilidad (bandas comprimidas)
  - Valores mínimos frecuentemente preceden movimientos direccionales fuertes

### Retrocesos de Fibonacci

Los niveles de Fibonacci son líneas horizontales que indican áreas potenciales de soporte y resistencia:
- **0%** - Punto inicial del movimiento
- **23.6%** - Retroceso superficial
- **38.2%** - Retroceso moderado
- **50%** - Retroceso medio (no es técnicamente Fibonacci pero ampliamente usado)
- **61.8%** - Retroceso de proporción áurea
- **78.6%** - Retroceso profundo
- **100%** - Retroceso completo

**Interpretación según Tendencia:**
- **Tendencia Alcista**: Los niveles Fibonacci actúan como soporte durante correcciones
- **Tendencia Bajista**: Los niveles Fibonacci actúan como resistencia durante rebotes

## Implementación de la Estrategia

### Lógica de Generación de Señales

**Señales de Compra** se generan cuando:
1. El precio cruza por encima de la banda inferior de Bollinger (potencial rebote desde sobreventa)
2. El precio está dentro del 2% de un nivel de soporte Fibonacci
3. La confluencia confirma mayor probabilidad de reversión

**Señales de Venta** se generan cuando:
1. El precio cruza por debajo de la banda superior de Bollinger (potencial rechazo desde sobrecompra)
2. El precio está dentro del 2% de un nivel de resistencia Fibonacci
3. La confluencia confirma mayor probabilidad de reversión

### Detección de Swing Points

La estrategia identifica máximos y mínimos significativos usando una ventana configurable (por defecto 5-10 períodos):
- **Swing High**: Punto de precio más alto que los períodos circundantes en ambos lados
- **Swing Low**: Punto de precio más bajo que los períodos circundantes en ambos lados

Estos swing points determinan el rango de cálculo del retroceso Fibonacci.

## Sistema de Puntuación

El sistema avanzado de puntuación (introducido en v2 y v3) proporciona un indicador integral de fuerza de señal que va de -100 a +100.

### Zonas de Señal

| Rango de Puntuación | Categoría de Señal | Acción |
|---------------------|-------------------|---------|
| +60 a +100 | **Compra Fuerte** | Entrar posiciones largas |
| +20 a +60 | **Compra Moderada** | Considerar posiciones largas |
| -20 a +20 | **Mantener** | Conservar posición actual |
| -60 a -20 | **Venta Moderada** | Considerar posiciones cortas |
| -100 a -60 | **Venta Fuerte** | Entrar posiciones cortas |

### Componentes de la Puntuación

La puntuación de la estrategia es una combinación ponderada de cuatro factores clave:

#### 1. Posición en Bandas de Bollinger (30% peso)
- Basado en el indicador %B
- **Contribución positiva**: Precio cerca de banda inferior (%B cercano a 0)
- **Contribución negativa**: Precio cerca de banda superior (%B cercano a 1)
- **Rango**: -25 a +25 puntos

#### 2. Evaluación de Volatilidad (15% peso)
- Analiza el ancho actual de las Bandas de Bollinger y cambios recientes
- **Factores positivos**: Bandas estrechas con expansión (potenciales breakouts)
- **Factores negativos**: Alta volatilidad reduciendo confiabilidad de señales
- **Rango**: -15 a +15 puntos

#### 3. Interacción con Niveles Fibonacci (35% peso)
- **Mayor peso** ya que es el núcleo de la estrategia combinada
- Mide proximidad a niveles Fibonacci clave (dentro del 3% para significancia)
- Considera dirección del precio relativa a niveles de soporte/resistencia
- Toma en cuenta contexto de tendencia (alcista vs bajista)
- **Rango**: -35 a +35 puntos

#### 4. Momentum del Precio (20% peso)
- Indicador de momentum tipo RSI (14 períodos)
- **Contribución positiva**: Condiciones de sobreventa (RSI < 30)
- **Contribución negativa**: Condiciones de sobrecompra (RSI > 70)
- **Rango**: -30 a +30 puntos

### Directrices para Tamaño de Posición

- **Puntuaciones extremas** (+90 o -90): Usar tamaños de posición mayores
- **Puntuaciones umbral** (+65 o -65): Usar tamaños de posición menores
- **Indicador de convicción**: Puntuaciones absolutas más altas indican mayor convicción

### Gestión de Riesgo

- **Confirmación**: Esperar 2-3 días consecutivos en la misma zona de señal
- **Stop Loss**: Colocar en el nivel Fibonacci más cercano en dirección opuesta
- **Toma de Beneficios**:
  - Posiciones largas: Considerar beneficios parciales cerca de niveles de resistencia
  - Posiciones cortas: Considerar cobertura parcial cerca de niveles de soporte

## Descripción de los Notebooks

### 1. Bollinger_bands and Fibonacci Retracement.ipynb
**Implementación Básica**

- Implementación central de la estrategia con componentes esenciales
- Generación básica de señales (compra/venta)
- Funcionalidad estándar de backtesting
- Visualización con Bandas de Bollinger, niveles Fibonacci y señales
- Cálculo de métricas de rendimiento

**Características Clave:**
- Implementación limpia y directa
- Backtesting esencial con comparación buy & hold
- Funcionalidad básica de gráficos

### 2. Bollinger_bands and Fibonacci Retracement-v2.ipynb
**Versión Mejorada con Sistema de Puntuación**

- Introducción del sistema integral de puntuación (-100 a +100)
- Categorización avanzada de señales (Compra/Venta Fuerte, Moderada, Mantener)
- Visualización mejorada con gráfico de puntuación de estrategia
- Características mejoradas de análisis de componentes y debugging

**Características Clave:**
- **Sistema de Puntuación de Estrategia**: Combinación ponderada de cuatro componentes
- **Categorías de Señal**: Categorización clara para diferentes niveles de acción
- **Análisis de Componentes**: Desglose individual de puntuaciones para debugging
- **Gráficos Mejorados**: Visualización de puntuación de estrategia con zonas coloreadas
- **Mejor Gestión de Riesgo**: Orientación de tamaño de posición basada en puntuación

### 3. Bollinger_bands and Fibonacci Retracement-v3.ipynb
**Implementación Refinada**

- Detección refinada de swing points (ventana reducida para más puntos)
- Cálculo mejorado de niveles Fibonacci con mejor determinación de tendencia
- Capacidades mejoradas de manejo de errores y debugging
- Pesos de puntuación optimizados (componente Fibonacci aumentado a 40%)
- Métodos adicionales de debugging para análisis de componentes

**Características Clave:**
- **Detección Mejorada de Swing**: Ventana menor (5 períodos) para más swing points
- **Mejor Lógica de Tendencia**: Algoritmo mejorado de determinación de tendencia
- **Modo Debug**: Información integral de debugging
- **Pesos Optimizados**: Fibonacci 40%, Bollinger 25%, Momentum 20%, Volatilidad 15%
- **Herramientas de Análisis**: Método `analyze_fibonacci_component()` para debugging detallado

### 4. RAG_LangGraph_Bollinger_bands and Fibonacci Retracement.ipynb
**Asistente de Trading Potenciado por IA**

- Sistema de IA conversacional basado en LangGraph
- Análisis automatizado de estrategia y recomendaciones
- Arquitectura basada en herramientas para cálculos en tiempo real
- Interacción en lenguaje natural para insights de estrategia

**Características Clave:**
- **Asistente IA**: Interfaz conversacional para recomendaciones de trading
- **Análisis en Tiempo Real**: Procesamiento de datos de mercado en vivo
- **Integración de Herramientas**: Ejecución automatizada del sistema de puntuación
- **Parámetros Flexibles**: Períodos, ventanas y marcos temporales personalizables
- **Evaluación de Riesgo**: Interpretación potenciada por IA de señales y recomendaciones

## Ejemplos de Uso

### Ejecución Básica de Estrategia

```python
# Inicializar estrategia
strategy = BollingerFibonacciStrategy("AAPL", "2024-01-01", "2024-12-31")

# Ejecutar análisis completo
strategy.fetch_data()
strategy.calculate_bollinger_bands()
strategy.find_swing_points()
strategy.calculate_fibonacci_levels()
strategy.generate_signals()

# Calcular puntuación de estrategia (v2 y v3)
strategy.calculate_strategy_score()

# Obtener últimas señales
latest_score = strategy.data['Strategy_Score'].iloc[-1]
latest_signal = strategy.data['Signal_Category'].iloc[-1]
print(f"Puntuación Actual: {latest_score}, Señal: {latest_signal}")
```

### Uso del Asistente IA (v4)

```python
# Pedir recomendaciones al asistente IA
message = graph.invoke({
    "messages": [("user", """
        Recomienda si comprar o vender AAPL basado en la puntuación 
        de la estrategia de Bandas de Bollinger y Retrocesos Fibonacci.
        Usa datos de 1 año con ventana de 20 días.
    """)]
}, config)

print(message["messages"][-1].content)
```

### Análisis de Componentes

```python
# Analizar componentes individuales de puntuación
print("Componentes de Puntuación:")
print(f"Puntuación Bandas Bollinger: {strategy.data['BB_Score'].iloc[-1]:.2f}")
print(f"Puntuación Volatilidad: {strategy.data['Volatility_Score'].iloc[-1]:.2f}")
print(f"Puntuación Fibonacci: {strategy.data['Fib_Score'].iloc[-1]:.2f}")
print(f"Puntuación Momentum: {strategy.data['Momentum_Score'].iloc[-1]:.2f}")

# Análisis detallado de Fibonacci (v3)
fib_analysis = strategy.analyze_fibonacci_component()
```

## Instalación y Configuración

### Requisitos

```bash
pip install yfinance pandas numpy plotly datetime
```

### Para Asistente IA (v4)
```bash
pip install langchain langgraph langchain-openai
```

### Configuración de Entorno

Crear archivo `.env` para el asistente IA:
```
OPENAI_API_KEY=tu_clave_api_openai_aqui
```

## Ejemplos de Visualización

La estrategia proporciona visualizaciones integrales:

### Gráfico de Estrategia
- Gráfico de velas con Bandas de Bollinger
- Niveles de retroceso Fibonacci (líneas horizontales)
- Señales de compra/venta (marcadores triangulares)
- Indicadores de Ancho de Banda y %B

### Gráfico de Puntuación de Estrategia
- Gráfico de precios con Bandas de Bollinger y niveles Fibonacci
- Indicador de puntuación de estrategia con zonas coloreadas:
  - **Verde Oscuro**: Compra Fuerte (+60 a +100)
  - **Verde Claro**: Compra Moderada (+20 a +60)
  - **Gris**: Mantener (-20 a +20)
  - **Naranja**: Venta Moderada (-60 a -20)
  - **Rojo**: Venta Fuerte (-100 a -60)

## Métricas de Rendimiento

La estrategia calcula métricas integrales de rendimiento:
- **Retorno Total**: Comparación Estrategia vs Buy & Hold
- **Volatilidad Anualizada**: Medición de riesgo
- **Ratio de Sharpe**: Retorno ajustado por riesgo
- **Drawdown Máximo**: Peor declive pico-valle
- **Tasa de Aciertos**: Porcentaje de operaciones rentables

## Mejores Prácticas

1. **Confirmación**: Esperar 2-3 días consecutivos en la misma zona de señal
2. **Gestión de Riesgo**: Siempre usar stop losses en niveles Fibonacci
3. **Tamaño de Posición**: Ajustar basado en magnitud de puntuación y confianza
4. **Contexto de Mercado**: Considerar condiciones generales de mercado y tendencias
5. **Backtesting**: Probar exhaustivamente antes de implementación en vivo

## Contribuciones

Siéntete libre de contribuir mejoras, correcciones de bugs o características adicionales. Por favor asegúrate de que cualquier modificación mantenga la lógica central de la estrategia y mejore la precisión del sistema de puntuación.

## Descargo de Responsabilidad

Esta estrategia es solo para propósitos educativos y de investigación. El rendimiento pasado no garantiza resultados futuros. Siempre conduce pruebas exhaustivas y considera tu tolerancia al riesgo antes de implementar cualquier estrategia de trading con capital real.