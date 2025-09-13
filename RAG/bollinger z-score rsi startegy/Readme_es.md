# Estrategia de Trading con Bandas de Bollinger y RSI

Un sistema integral de trading cuantitativo que combina las Bandas de Bollinger y el Índice de Fuerza Relativa (RSI) para generar señales automáticas de compra/venta en valores financieros. Esta implementación utiliza LangGraph para crear un agente inteligente que analiza las condiciones del mercado y proporciona recomendaciones de trading.

## Descripción General

La Estrategia de Cruce de Bandas de Bollinger y RSI es un enfoque de análisis técnico que identifica puntos potenciales de reversión del mercado y cambios de tendencia mediante el monitoreo de cruces de precios con las Bandas de Bollinger y niveles de sobrecompra/sobreventa del RSI. El sistema busca capturar oportunidades de trading durante la volatilidad del mercado mientras utiliza la confirmación del RSI para mejorar la confiabilidad de las señales.

## Técnicas Financieras Implementadas

### 1. Bandas de Bollinger

Las Bandas de Bollinger son un indicador técnico basado en volatilidad que consiste en:
- **Banda Central**: Media Móvil Simple (típicamente de 20 períodos)
- **Banda Superior**: Banda Central + (2 × Desviación Estándar)
- **Banda Inferior**: Banda Central - (2 × Desviación Estándar)

**Características Clave:**
- Las bandas se expanden durante períodos de alta volatilidad
- Las bandas se contraen durante períodos de baja volatilidad
- El precio tiende a rebotar entre las bandas
- Las rupturas a menudo señalan cambios de tendencia

### 2. Z-Score de Bollinger

El Z-Score mide cuántas desviaciones estándar está el precio actual de la media móvil:

```
Z-Score = (Precio Actual - Media Móvil) / Desviación Estándar
```

**Guías de Interpretación:**
- **Z-Score > +2**: Precio en sobrecompra (considerar venta)
- **Z-Score < -2**: Precio en sobreventa (considerar compra)
- **Z-Score entre -2 y +2**: Precio en rango normal de trading

### 3. Índice de Fuerza Relativa (RSI)

El RSI es un oscilador de momentum que mide la velocidad y magnitud de los cambios de precio:

**Proceso de Cálculo:**
1. Calcular cambios de precio: `Δ = Precio(t) - Precio(t-1)`
2. Separar ganancias y pérdidas
3. Calcular ganancia promedio y pérdida promedio durante el período
4. Computar Fuerza Relativa: `RS = Ganancia Promedio / Pérdida Promedio`
5. Calcular RSI: `RSI = 100 - (100 / (1 + RS))`

**Interpretación Estándar:**
- **RSI > 70**: Condición de sobrecompra (señal potencial de venta)
- **RSI < 30**: Condición de sobreventa (señal potencial de compra)
- **RSI 30-70**: Zona neutral

### 4. Niveles de Soporte y Resistencia

**Nivel de Soporte**: Un nivel de precio donde el interés comprador previene mayor declive
- Actúa como un "piso" para el movimiento del precio
- Nivel histórico donde el precio ha rebotado hacia arriba

**Nivel de Resistencia**: Un nivel de precio donde la presión vendedora previene mayor alza
- Actúa como un "techo" para el movimiento del precio
- Nivel histórico donde el precio ha sido rechazado hacia abajo

## Generación de Señales de Trading

### Señales de Compra
El sistema genera señales de compra cuando:
1. **RSI < 30** (condición de sobreventa) Y
2. **Precio cerca de la Banda Inferior de Bollinger** (Z-Score < -2)
3. **Opcional**: Precio tocando nivel clave de soporte

### Señales de Venta
El sistema genera señales de venta cuando:
1. **RSI > 70** (condición de sobrecompra) Y
2. **Precio cerca de la Banda Superior de Bollinger** (Z-Score > +2)
3. **Opcional**: Precio cerca de nivel clave de resistencia

## Arquitectura del Sistema

### Implementación del Agente LangGraph

El sistema utiliza LangGraph para crear un agente inteligente de trading con los siguientes componentes:

**Herramientas Disponibles:**
- `calculate_bollinger_z_score()`: Calcula el Z-Score de Bollinger para cualquier símbolo
- `calculate_rsi_zscore()`: Calcula valores RSI para cualquier símbolo

**Gestión del Estado del Agente:**
- Mantiene historial de conversaciones
- Procesa solicitudes del usuario para símbolos específicos
- Proporciona recomendaciones de trading contextualizadas

**Lógica de Decisión:**
El agente chatbot analiza los indicadores calculados y proporciona recomendaciones basadas en:
- Posición actual del Z-Score relativa a los umbrales
- Niveles de sobrecompra/sobreventa del RSI
- Fuerza combinada de las señales
- Consideraciones de evaluación de riesgo

## Instalación y Configuración

### Prerequisitos
```bash
pip install -r requirements.txt
```

### Dependencias Requeridas
- **Fuente de Datos**: `yfinance` para datos históricos de acciones
- **Análisis**: `pandas`, `numpy` para manipulación de datos
- **Visualización**: `plotly` para gráficos interactivos
- **Framework de IA**: `langchain`, `langgraph` para agente inteligente
- **Integración LLM**: `langchain-openai` para modelos GPT

### Configuración del Entorno
1. Configurar claves API en archivo `.env`:
```bash
OPENAI_API_KEY=tu_clave_openai
GEMINI_API_KEY=tu_clave_gemini
```

2. Configurar credenciales de Google Cloud para Vertex AI (opcional)

## Ejemplos de Uso

### Análisis Básico de Señales
```python
# Calcular Z-Score de Bollinger para acciones de Apple con período de 20 días
resultado = calculate_bollinger_z_score("AAPL", period=20)

# Calcular RSI para Tesla con ventana de 14 días
resultado_rsi = calculate_rsi_zscore("TSLA", period=20, window=14)
```

### Consultas Interactivas al Agente
```python
# Obtener recomendación de trading
mensaje = graph.invoke({
    "messages": [
        ("user", "Recomienda si comprar o vender AAPL basado en Z-score de Bollinger en un período de 20 días y score RSI con ventana de 14 días")
    ]
}, config)
```

### Visualización
```python
# Generar gráfico integral con señales
plot_bollinger_rsi_with_signals("AAPL", window=20, rsi_period=14)
```

## Características Principales

### 1. Confirmación Multi-Indicador
- Combina seguimiento de tendencia (Bandas de Bollinger) con momentum (RSI)
- Reduce señales falsas mediante confirmación dual
- Considera tanto condiciones de volatilidad como de momentum

### 2. Parámetros Personalizables
- Períodos ajustables de Bandas de Bollinger (por defecto: 20)
- Ventana configurable de cálculo RSI (por defecto: 14)
- Umbrales flexibles de sobrecompra/sobreventa

### 3. Análisis Visual
- Gráficos interactivos Plotly mostrando:
  - Acción del precio con Bandas de Bollinger
  - Oscilador RSI con líneas de umbral
  - Marcadores de señales de compra/venta
  - Niveles de soporte/resistencia

### 4. Recomendaciones Inteligentes
- Explicaciones en lenguaje natural de condiciones del mercado
- Sugerencias de trading conscientes del riesgo
- Análisis sensible al contexto basado en múltiples timeframes

## Consideraciones de Riesgo

### Limitaciones de la Estrategia
1. **Indicadores Rezagados**: Tanto las Bandas de Bollinger como el RSI se basan en datos históricos
2. **Señales Falsas**: Los mercados pueden permanecer en sobrecompra/sobreventa más tiempo del esperado
3. **Mercados Tendenciales**: Las estrategias de reversión a la media pueden underperformar en tendencias fuertes
4. **Sensibilidad a Volatilidad**: Condiciones extremas del mercado pueden generar señales engañosas

### Mejores Prácticas
1. **Combinar con Análisis de Tendencia**: Considerar la dirección general del mercado
2. **Gestión de Riesgo**: Siempre usar stop-loss y dimensionamiento de posiciones
3. **Múltiples Timeframes**: Confirmar señales a través de diferentes horizontes temporales
4. **Contexto del Mercado**: Considerar factores fundamentales y sentimiento del mercado
5. **Backtesting**: Probar rendimiento de la estrategia en datos históricos antes del trading en vivo

## Aplicaciones Avanzadas

### Integración de Portfolio
- Aplicar señales a través de múltiples valores
- Análisis basado en sectores y consideración de correlación
- Dimensionamiento de posición ajustado al riesgo basado en volatilidad

### Monitoreo en Tiempo Real
- Detección automatizada de señales y alertas
- Integración con APIs de brokers para ejecución
- Seguimiento de rendimiento y optimización de estrategia

## Contribuciones

Esta implementación proporciona una base para:
- Frameworks extendidos de backtesting
- Integración de indicadores técnicos adicionales
- Mejora con machine learning de la generación de señales
- Desarrollo de sistema de trading en tiempo real

## Descargo de Responsabilidad

Esta herramienta es solo para propósitos educativos e investigativos. El trading de valores financieros involucra un riesgo sustancial de pérdida. El rendimiento pasado no garantiza resultados futuros. Siempre consulte con asesores financieros calificados y conduzca investigación exhaustiva antes de tomar decisiones de inversión.