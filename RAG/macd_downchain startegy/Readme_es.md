# Estrategia de Trading MACD y Canales de Donchian

Una implementación completa de una estrategia combinada de MACD y Canales de Donchian con sistema de puntuación inteligente y generación automática de señales.

## 📋 Tabla de Contenidos

- [Resumen Ejecutivo](#resumen-ejecutivo)
- [Técnicas Financieras](#técnicas-financieras)
- [Sistema de Puntuación](#sistema-de-puntuación)
- [Explicación de los Notebooks](#explicación-de-los-notebooks)
- [Instalación](#instalación)
- [Uso](#uso)
- [Señales de Trading](#señales-de-trading)
- [Gestión de Riesgo](#gestión-de-riesgo)
- [Ejemplos Prácticos](#ejemplos-prácticos)

## 🎯 Resumen Ejecutivo

Este proyecto implementa una estrategia de trading sofisticada que combina dos indicadores técnicos poderosos:

1. **MACD (Moving Average Convergence Divergence)** - Indicador de momentum
2. **Canales de Donchian** - Indicador de rango de precios y volatilidad

La estrategia utiliza un sistema de puntuación innovador que convierte patrones complejos de indicadores en valores numéricos intuitivos (-100 a +100), facilitando la interpretación de las condiciones del mercado y la generación de señales de trading.

## 📈 Técnicas Financieras

### Canales de Donchian

Los Canales de Donchian son principalmente un **indicador de rangos de precio** que puede reflejar indirectamente la volatilidad del mercado:

**Componentes:**
- **Banda Superior (Upper Band)**: Precio más alto durante un período específico
- **Banda Media (Middle Band)**: Promedio entre las bandas superior e inferior
- **Banda Inferior (Lower Band)**: Precio más bajo durante un período específico

**Características Clave:**
- La amplitud del canal indica volatilidad (más ancho = mayor volatilidad)
- Adaptación automática a las condiciones del mercado
- Útil para identificar breakouts y reversiones de tendencia

**Aplicaciones en Trading:**
- **Estrategia de Breakout**: Comprar cuando el precio rompe por encima de la banda superior, vender cuando cae por debajo de la inferior
- **Reversión a la Media**: Usar la banda media como nivel de soporte/resistencia
- **Seguimiento de Tendencia**: La dirección del canal indica la tendencia general

### MACD (Moving Average Convergence Divergence)

El MACD es un **indicador de momentum** que mide la velocidad y dirección del movimiento del precio:

**Componentes:**
- **Línea MACD** (Azul): Diferencia entre EMA rápido (12) y EMA lento (26)
- **Línea de Señal** (Roja): EMA de la línea MACD (9 períodos)
- **Histograma**: Diferencia entre la línea MACD y la línea de señal

**Señales Clave:**
- **Cruce Alcista**: Línea MACD cruza por encima de la línea de señal
- **Cruce Bajista**: Línea MACD cruza por debajo de la línea de señal
- **Cruce de Línea Cero**: Indica la fuerza de la tendencia
- **Divergencia**: Desacuerdo entre precio y MACD señala posibles reversiones

## 🔢 Sistema de Puntuación

### Puntuación MACD (-100 a +100)

La puntuación MACD combina tres componentes ponderados:

1. **Línea MACD vs Línea de Señal (40%)**
   - Positiva cuando MACD > Línea de Señal (alcista)
   - Negativa cuando MACD < Línea de Señal (bajista)

2. **Línea MACD vs Cero (30%)**
   - Positiva cuando MACD > 0 (tendencia alcista fuerte)
   - Negativa cuando MACD < 0 (tendencia bajista fuerte)

3. **Momentum del Histograma (30%)**
   - Positiva cuando el histograma aumenta (momentum acelerando)
   - Negativa cuando el histograma disminuye (momentum desacelerando)

### Puntuación Donchian (-100 a +100)

La puntuación Donchian combina tres componentes ponderados:

1. **Posición del Precio Dentro del Canal (50%)**
   - +50 en la banda superior
   - 0 en la banda media
   - -50 en la banda inferior

2. **Dirección del Canal (30%)**
   - Positiva cuando el canal tiene tendencia ascendente
   - Negativa cuando el canal tiene tendencia descendente

3. **Tendencia del Ancho del Canal (20%)**
   - Positiva cuando el canal se ensancha (volatilidad creciente)
   - Negativa cuando el canal se estrecha (volatilidad decreciente)

### Puntuación Combinada

**Fórmula**: `(Puntuación MACD + Puntuación Donchian) / 2`

Da igual peso al momentum (MACD) y al rango de precios (Donchian).

### Interpretación de Puntuaciones

#### Puntuaciones Individuales:
- **Arriba de +50**: Fuertemente alcista
- **+25 a +50**: Moderadamente alcista
- **-25 a +25**: Neutral
- **-50 a -25**: Moderadamente bajista
- **Debajo de -50**: Fuertemente bajista

#### Señales de Trading de la Puntuación Combinada:
- **+75 a +100**: 🟢 Señal Fuerte de Compra
- **+50 a +75**: 🟢 Señal de Compra
- **+25 a +50**: 🟡 Señal Débil de Compra
- **-25 a +25**: ⚪ Neutral (Mantener)
- **-50 a -25**: 🟡 Señal Débil de Venta
- **-75 a -50**: 🔴 Señal de Venta
- **-100 a -75**: 🔴 Señal Fuerte de Venta

## 📓 Explicación de los Notebooks

### 1. `macd_Donchian channels.ipynb`
**Propósito**: Implementación central y visualización

**Características:**
- Funciones completas de cálculo para ambos indicadores
- Implementación del sistema de puntuación
- Visualización de cuatro paneles usando Plotly
- Interpretación de puntuaciones en tiempo real
- Señales de trading codificadas por colores

**Funciones Clave:**
- `calculate_donchian_channels()`: Calcula las bandas del canal
- `calculate_macd()`: Calcula los componentes del MACD
- `calculate_macd_score()`: Genera la puntuación MACD
- `calculate_donchian_score()`: Genera la puntuación Donchian
- `plot_scores_with_indicators()`: Crea visualización completa

### 2. `RAG_Langgrap_macd_z-score-donchain_channel.ipynb`
**Propósito**: Asistente de trading potenciado por IA con LangGraph

**Características:**
- Agente conversacional basado en LangGraph
- Arquitectura basada en herramientas para cálculos
- Interacción en lenguaje natural para decisiones de trading
- Sistema de recomendaciones automatizado
- Análisis de mercado en tiempo real

**Herramientas Clave:**
- `@tool calculate_macd_score()`: Herramienta de cálculo MACD
- `@tool calculate_donchian_channel_score()`: Herramienta de cálculo Donchian
- `@tool calculate_combined_score()`: Herramienta de combinación de puntuaciones
- `@tool interpret_combined_score()`: Herramienta de interpretación de señales

**Capacidades del Agente:**
- Acepta símbolos de acciones y parámetros
- Proporciona desgloses detallados de componentes
- Genera recomendaciones de trading accionables
- Explica el razonamiento detrás de las señales

### 3. `ta_donchain.ipynb`
**Propósito**: Enfoque tradicional basado en señales

**Características:**
- Identificación clásica de señales de compra/venta
- Detección de cruces MACD
- Señales de breakout Donchian
- Confirmación de señales combinadas
- Filtrado de señales para reducir ruido

**Tipos de Señales:**
- **Cruces MACD**: Línea cruza por encima/debajo de la señal
- **Breakouts Donchian**: Precio rompe los límites del canal
- **Señales Combinadas**: Ambos indicadores se alinean
- **Señales Filtradas**: Tiempo mínimo entre señales

## 🛠 Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd macd-donchian-strategy

# Instalar paquetes requeridos
pip install -r requirements.txt

# Para soporte de Jupyter notebook
pip install jupyter jupyterlab
```

### Dependencias Principales

```python
# Librerías principales
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# IA/LangGraph (para notebook RAG)
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# Análisis técnico
from ta.volatility import DonchianChannel
```

## 🚀 Uso

### Uso Básico

```python
# Configurar parámetros
ticker = "AAPL"
period = '1y'
window = 20  # Período Donchian

# Parámetros MACD
fast_period = 12
slow_period = 26
signal_period = 9

# Descargar y analizar
data = yf.download(ticker, period=period)
channels = calculate_donchian_channels(data, window)
macd_data = calculate_macd(data, fast_period, slow_period, signal_period)

# Calcular puntuaciones
macd_score = calculate_macd_score(data, macd_data)
donchian_score = calculate_donchian_score(data, channels)
combined_score = calculate_combined_score(macd_score, donchian_score)

# Obtener señales actuales
current_signal = interpret_score(combined_score.iloc[-1])
print(f"Señal actual para {ticker}: {current_signal}")
```

### Uso del Asistente IA (Notebook RAG)

```python
# Consulta en lenguaje natural
message = "Recomienda si comprar o vender TSLA basado en puntuaciones MACD y Donchian para datos de 6 meses"

# El agente:
# 1. Calculará la puntuación MACD
# 2. Calculará la puntuación Donchian  
# 3. Computará la puntuación combinada
# 4. Proporcionará interpretación y recomendación
```

## 📊 Señales de Trading

### Puntos de Entrada

**Posiciones Largas (Long):**
- Puntuación combinada cruza por encima de +50
- Ambas puntuaciones MACD y Donchian positivas
- Precio rompe por encima de la banda superior Donchian con cruce alcista MACD

**Posiciones Cortas (Short):**
- Puntuación combinada cruza por debajo de -50
- Ambas puntuaciones MACD y Donchian negativas
- Precio rompe por debajo de la banda inferior Donchian con cruce bajista MACD

### Puntos de Salida

**Toma de Ganancias:**
- Puntuación combinada comienza a moderarse desde extremos (+75 o -75)
- Cruce opuesto en MACD
- Puntuación cruza cero en dirección opuesta

**Stop Loss:**
- Precio cierra fuera de la banda Donchian opuesta
- Puntuación combinada muestra patrón de reversión fuerte

## ⚠️ Gestión de Riesgo

### Dimensionamiento de Posición
- **Señales fuertes** (+75 a +100 o -75 a -100): Tamaño de posición mayor
- **Señales moderadas** (+50 a +75 o -50 a -75): Tamaño de posición estándar
- **Señales débiles** (+25 a +50 o -25 a -50): Tamaño de posición reducido

### Guías de Stop-Loss
- Colocar stops cerca de la banda media Donchian para trades de breakout
- Ajustar stops cuando las puntuaciones muestren signos tempranos de reversión
- Usar divergencia MACD como confirmación adicional de salida

### Diversificación
- No concentrar todas las posiciones en un activo
- Considerar correlación entre instrumentos seleccionados
- Monitorear exposición general del portafolio

## 📈 Ejemplos Prácticos

### Ejemplo 1: Señal Fuerte de Compra
```
Símbolo: TSLA, Período: 1y
Última puntuación MACD: 78.45
Última puntuación Donchian: 82.30
Puntuación combinada: 80.38
Interpretación: Señal Fuerte de Compra
```

### Ejemplo 2: Mercado Neutral
```
Símbolo: AAPL, Período: 6mo  
Última puntuación MACD: -12.50
Última puntuación Donchian: 15.20
Puntuación combinada: 1.35
Interpretación: Neutral
```

## 📋 Beneficios de Este Sistema

1. **Simplificación**: Convierte patrones complejos en valores numéricos intuitivos
2. **Normalización**: Todos los indicadores usan la misma escala de -100 a +100
3. **Combinación**: Combina fácilmente análisis de momentum y rango de precios
4. **Visualización**: Representación clara de fuerza de indicadores y transiciones
5. **Personalización**: Los pesos de componentes pueden ajustarse para diferentes estrategias
6. **Automatización**: Adecuado para implementación de trading algorítmico

## 🔄 Implementación Práctica

### Confirmación de Tendencia
Cuando ambas puntuaciones MACD y Donchian concuerdan (ambas positivas o negativas), confirma una dirección de tendencia fuerte.

### Detección de Divergencia  
Cuando las puntuaciones se mueven en direcciones opuestas, puede indicar una posible reversión de tendencia que requiere mayor atención.

### Análisis Multi-Timeframe
- Usar períodos cortos (20 días) para swing trading
- Usar períodos largos (50+ días) para trading de posición
- Combinar múltiples marcos temporales para confirmación

## 🎯 Casos de Uso Específicos

### Trading Intradía
- Usar ventanas más cortas (5-10 períodos)
- Enfocarse en señales de momentum rápido
- Salidas más agresivas en reversiones

### Inversión a Largo Plazo
- Usar ventanas más largas (50-100 períodos)
- Enfocarse en tendencias macro
- Mantener posiciones durante señales débiles temporales

### Gestión de Portafolio
- Aplicar a múltiples activos simultáneamente
- Usar para rotación sectorial
- Implementar como filtro de timing de mercado

## 📚 Interpretación Visual

### Panel Superior: Precio con Canales Donchian
- **Líneas Rojas**: Banda superior (resistencia dinámica)
- **Líneas Azules**: Banda media (soporte/resistencia neutral)
- **Líneas Verdes**: Banda inferior (soporte dinámico)
- **Velas**: Precio OHLC del activo

### Panel MACD
- **Línea Azul**: Línea MACD principal
- **Línea Roja**: Línea de señal
- **Histograma Verde/Rojo**: Diferencia entre líneas (momentum)

### Panel de Puntuaciones
- **Línea Azul**: Puntuación MACD
- **Línea Naranja**: Puntuación Donchian
- **Línea Morada**: Puntuación combinada (la más importante)

### Panel de Señales
- **Verde Oscuro**: Señal fuerte de compra
- **Verde**: Señal de compra
- **Verde Claro**: Señal débil de compra
- **Gris**: Neutral
- **Rosa**: Señal débil de venta
- **Rojo**: Señal de venta
- **Rojo Oscuro**: Señal fuerte de venta

## 🧮 Fórmulas Matemáticas

### Cálculo MACD
```
EMA_rápido = EMA(precio, 12)
EMA_lento = EMA(precio, 26)
Línea_MACD = EMA_rápido - EMA_lento
Línea_señal = EMA(Línea_MACD, 9)
Histograma = Línea_MACD - Línea_señal
```

### Cálculo Canales Donchian
```
Banda_superior = MAX(máximo, ventana)
Banda_inferior = MIN(mínimo, ventana)
Banda_media = (Banda_superior + Banda_inferior) / 2
```

### Sistema de Puntuación
```
Componente_1 = normalizar(diferencia_líneas) * peso_1
Componente_2 = normalizar(posición_cero) * peso_2
Componente_3 = normalizar(momentum) * peso_3
Puntuación_final = Componente_1 + Componente_2 + Componente_3
```

## 🚨 Consideraciones Importantes

### Limitaciones del Sistema
- No considera eventos fundamentales
- Funciona mejor en mercados con tendencias claras
- Puede generar señales falsas en mercados laterales
- Requiere ajuste de parámetros según el activo

### Optimización de Parámetros
- **Mercados volátiles**: Reducir ventanas temporales
- **Mercados estables**: Aumentar ventanas temporales
- **Activos específicos**: Ajustar pesos de componentes
- **Condiciones de mercado**: Adaptar umbrales de señales

## 📚 Referencias Adicionales

- [Análisis Técnico MACD](https://www.investopedia.com/terms/m/macd.asp)
- [Guía de Canales de Donchian](https://www.investopedia.com/terms/d/donchianchannels.asp)
- [Fundamentos de Análisis Técnico](https://www.investopedia.com/technical-analysis-4689657)

## ⚖️ Disclaimer

Esta estrategia de trading es únicamente para propósitos educativos e de investigación. El rendimiento pasado no garantiza resultados futuros. Siempre realice su propia investigación y considere consultar con un asesor financiero antes de tomar decisiones de inversión. El trading involucra un riesgo sustancial de pérdida.

---
