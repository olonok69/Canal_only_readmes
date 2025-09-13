# Dual Moving Average Crossover Strategy con Agente IA

Una implementación integral en Python de la clásica Dual Moving Average Crossover Strategy mejorada con un agente de inteligencia artificial para análisis automatizado, puntuación y escaneo de mercados.

## 📋 Tabla de Contenidos

- [Descripción de la Estrategia](#descripción-de-la-estrategia)
- [Características Principales](#características-principales)
- [Instalación](#instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Detalles de Implementación](#detalles-de-implementación)
- [Sistema de Agente IA](#sistema-de-agente-ia)
- [Sistema de Puntuación](#sistema-de-puntuación)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Descripción de Notebooks](#descripción-de-notebooks)
- [Configuración](#configuración)
- [Métricas de Rendimiento](#métricas-de-rendimiento)
- [Limitaciones](#limitaciones)
- [Contribuciones](#contribuciones)

## 🎯 Descripción de la Estrategia

La Dual Moving Average Crossover Strategy es un enfoque clásico de seguimiento de tendencias que utiliza dos medias móviles con períodos diferentes para generar señales de trading:

### Conceptos Fundamentales

- **Cruce Dorado (Golden Cross)**: Cuando la media móvil de corto plazo cruza por encima de la de largo plazo → **Señal de COMPRA**
- **Cruce de la Muerte (Death Cross)**: Cuando la media móvil de corto plazo cruza por debajo de la de largo plazo → **Señal de VENTA**
- **Configuración Clásica**: Medias móviles de 50 y 200 días (estándar institucional)

### Por Qué Funciona Esta Estrategia

1. **Identificación de Tendencias**: Captura tendencias de mercado a mediano y largo plazo
2. **Reducción de Ruido**: Suaviza las fluctuaciones de precios a corto plazo
3. **Uso Institucional**: Ampliamente utilizada por traders profesionales y gestores de fondos
4. **Rendimiento Histórico**: Estudios muestran ganancias promedio del 7.43% en 40 días post-Cruce Dorado

## 🚀 Características Principales

### 1. **Implementación Flexible de la Estrategia**
- **Tipos de Media Móvil**: SMA (Simple) y EMA (Exponencial)
- **Períodos Personalizables**: Cualquier combinación (predeterminado: 50/200)
- **Múltiples Marcos Temporales**: Soporta todos los períodos de Yahoo Finance
- **Evaluación de Calidad de Señales**: Análisis de fuerza de tendencia y momentum

### 2. **Herramientas de Análisis Potenciadas por IA**
- **Consultas en Lenguaje Natural**: Haz preguntas en español
- **Análisis Automatizado de Estrategia**: Evaluación completa de rendimiento
- **Escáner de Mercado**: Identificación de oportunidades en múltiples símbolos
- **Puntuación Inteligente**: Sistema de puntuación de -100 a +100

### 3. **Análisis Avanzado de Rendimiento**
- **Comparación Estrategia vs Comprar y Mantener**
- **Métricas Ajustadas por Riesgo**: Ratio de Sharpe, volatilidad, drawdown
- **Cálculo de Tasa de Éxito**: Análisis operación por operación
- **Historial de Señales**: Seguimiento de cruces recientes

### 4. **Visualizaciones Interactivas**
- **Gráficos de 3 Paneles**: Precio + MAs, Posiciones, Retornos
- **Marcadores de Señales**: Indicadores claros de Cruce Dorado/de la Muerte
- **Integración con Plotly**: Gráficos interactivos con zoom
- **Actualizaciones en Tiempo Real**: Generación dinámica de gráficos

## 📦 Instalación

### Requisitos Previos
- Python 3.8+
- Jupyter Lab/Notebook
- Conexión a internet (para datos de mercado)

### Paso 1: Clonar Repositorio
```bash
git clone <url-del-repositorio>
cd dual_band_strategy
```

### Paso 2: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 3: Configurar Variables de Entorno
Crear un archivo `.env` en la raíz del proyecto:

```env
# Elige tu proveedor de IA
MODEL_PROVIDER=vertexai  # o "openai"

# Para OpenAI (si se usa)
OPENAI_API_KEY=tu_clave_api_openai_aqui

# Para Vertex AI (si se usa)
GOOGLE_CLOUD_PROJECT=tu_id_proyecto
GOOGLE_APPLICATION_CREDENTIALS=ruta/a/cuenta-servicio.json
PROJECT=tu_id_proyecto
REGION=us-central1
```

### Paso 4: Configuración del Proveedor de IA

#### Opción A: OpenAI
1. Obtener clave API de [OpenAI Platform](https://platform.openai.com)
2. Agregar al archivo `.env`
3. Configurar `MODEL_PROVIDER=openai`

#### Opción B: Google Vertex AI
1. Crear Proyecto de Google Cloud
2. Habilitar API de Vertex AI
3. Crear cuenta de servicio y descargar clave JSON
4. Configurar `MODEL_PROVIDER=vertexai`

### Paso 5: Lanzar Jupyter
```bash
jupyter lab
```

## 📁 Estructura del Proyecto

```
dual_band_strategy/
├── notebook/
│   ├── Rag_agent.ipynb                    # Implementación del Agente IA
│   └── dual moving average crossover strategy.ipynb  # Estrategia Principal
├── .env                                   # Variables de entorno
├── .gitignore                            # Reglas de Git ignore
├── requirements.txt                      # Dependencias de Python
└── README.md                             # Este archivo
```

## 🔧 Detalles de Implementación

### Clase Principal de la Estrategia

```python
class DualMovingAverageStrategy:
    def __init__(self, short_period=50, long_period=200, ma_type='SMA'):
        self.short_period = short_period
        self.long_period = long_period
        self.ma_type = ma_type
    
    def generate_signals(self, data):
        # Cruce Dorado: MA corta > MA larga
        # Cruce de la Muerte: MA corta < MA larga
        # Retorna datos con señales y posiciones
```

### Lógica de Generación de Señales

1. **Calcular Medias Móviles**: SMA o EMA para ambos períodos
2. **Detectar Cruces**: Comparar períodos actuales vs anteriores
3. **Generar Posiciones**: 1 (Largo), -1 (Corto), 0 (Neutral)
4. **Avance**: Mantener posición hasta siguiente señal

### Cálculo de Rendimiento

- **Retornos de Estrategia**: Posición × Retornos Diarios
- **Comparación con Benchmark**: Estrategia vs Comprar y Mantener
- **Métricas de Riesgo**: Volatilidad, Ratio de Sharpe, Máximo Drawdown
- **Análisis de Operaciones**: Tasa de éxito, retorno promedio por operación

## 🤖 Sistema de Agente IA

### Arquitectura

El agente IA está construido usando **LangGraph** y soporta modelos **OpenAI GPT** y **Google Gemini**:

```python
# Componentes del Agente
├── Gestión de Estado (LangGraph)
├── Integración de Herramientas (4 herramientas especializadas)
├── Sistema de Memoria (historial de conversación)
└── Proveedor de Modelo (OpenAI/Vertex AI)
```

### Herramientas Disponibles

#### 1. `@tool analyze_dual_ma_strategy()`
- Análisis completo de estrategia con métricas de rendimiento
- Evaluación de posición actual del mercado y tendencia
- Historial de señales recientes y evaluación de condiciones del mercado

#### 2. `@tool calculate_dual_ma_score()`
- Sistema de puntuación (-100 a +100) para decisiones de trading
- Combina posicionamiento de MA, fuerza de señal y momentum
- Proporciona recomendaciones claras de COMPRAR/VENDER/MANTENER

#### 3. `@tool compare_ma_strategies()`
- Prueba múltiples configuraciones (20/50, 50/200, 10/30)
- Compara rendimiento SMA vs EMA
- Clasifica estrategias por ratio de Sharpe

#### 4. `@tool market_scanner_dual_ma()`
- Escanea múltiples símbolos en busca de oportunidades
- Clasifica por recencia de señal y fuerza de tendencia
- Proporciona visión general del sentimiento del mercado

### Flujo de Conversación

1. **Consulta del Usuario**: Pregunta en lenguaje natural sobre trading
2. **Selección de Herramientas**: IA elige herramientas de análisis apropiadas
3. **Procesamiento de Datos**: Obtener datos de mercado y ejecutar cálculos
4. **Síntesis de Resultados**: Combinar salidas de herramientas en respuesta coherente
5. **Recomendación**: Proporcionar insights de trading accionables

## 📊 Sistema de Puntuación

### Fórmula de Cálculo de Puntuación

**Puntuación Total = Posicionamiento MA (40%) + Fuerza de Señal (30%) + Momentum (30%)**

#### Desglose de Componentes

1. **Posicionamiento MA (40% peso)**
   - Positivo cuando MA corta > MA larga
   - Escalado por porcentaje de separación
   - Rango: -40 a +40

2. **Fuerza de Señal Reciente (30% peso)**
   - Tiempo desde último cruce
   - Movimiento de precio desde señal
   - Evaluación de calidad de señal
   - Rango: -30 a +30

3. **Momentum de Tendencia (30% peso)**
   - Tasa de cambio en separación MA
   - Comparación promedio 5 días vs 10 días
   - Aceleración/desaceleración de tendencia
   - Rango: -30 a +30

### Interpretación de Puntuación

| Rango de Puntuación | Señal | Condición del Mercado | Acción |
|---------------------|-------|----------------------|---------|
| **+80 a +100** | 🟢 **Compra Fuerte** | Cruce Dorado reciente + momentum fuerte | Entrar posición larga |
| **+60 a +80** | 🟢 **Compra** | Condiciones de Cruce Dorado favorables | Considerar entrada larga |
| **+40 a +60** | 🟡 **Compra Débil** | Tendencia alcista leve | Posición larga pequeña |
| **-40 a +40** | ⚪ **Neutral** | Señales mixtas | Mantener posición actual |
| **-60 a -40** | 🟡 **Venta Débil** | Tendencia bajista leve | Considerar salida/corto pequeño |
| **-80 a -60** | 🔴 **Venta** | Condiciones de Cruce de la Muerte | Salir largo/entrar corto |
| **-100 a -80** | 🔴 **Venta Fuerte** | Cruce de la Muerte reciente + momentum débil | Señal corta fuerte |

## 💻 Ejemplos de Uso

### Análisis Básico de Estrategia

```python
# Analizar Apple con SMA clásico 50/200
result = analyze_stock_dual_ma(
    symbol="AAPL",
    period="2y",
    short_period=50,
    long_period=200,
    ma_type='SMA',
    include_comparison=True
)
```

### Escáner de Mercado

```python
# Escanear acciones tecnológicas en busca de oportunidades
tech_stocks = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
scanner_result = scan_market_opportunities(
    symbols=tech_stocks,
    ma_type='EMA',
    short_period=20,
    long_period=50
)
```

### Chat Interactivo con IA

```python
# Iniciar sesión interactiva con agente IA
graph = create_dual_ma_agent()
result = graph.invoke({
    "messages": [HumanMessage(content="¿Cuál es la tendencia actual de TSLA?")]
})
```

## 📚 Descripción de Notebooks

### 1. `Rag_agent.ipynb` - Agente de Trading IA

**Propósito**: Asistente de trading integral potenciado por IA

**Componentes Clave**:
- **Implementación LangGraph**: Gestión de conversación basada en estado
- **Soporte Multi-Modelo**: OpenAI GPT-4o-mini o Google Gemini
- **Integración de Herramientas**: 4 herramientas especializadas de análisis de trading
- **Modo Interactivo**: Interfaz de chat para consultas en tiempo real

**Características**:
- Análisis de estrategia en lenguaje natural
- Escaneo automatizado de mercado
- Comparación de rendimiento entre configuraciones
- Puntuación y recomendaciones en tiempo real

### 2. `dual moving average crossover strategy.ipynb` - Estrategia Principal

**Propósito**: Implementación pura de estrategia y visualización

**Componentes Clave**:
- **Clase de Estrategia**: Implementación completa de MA dual
- **Generación de Señales**: Detección de cruces dorados/de la muerte
- **Análisis de Rendimiento**: Cálculo de métricas integrales
- **Gráficos Interactivos**: Visualizaciones Plotly de 3 paneles

**Características**:
- Gráficos de velas con superposiciones de MA
- Marcadores de señales de compra/venta
- Visualización de seguimiento de posiciones
- Comparación estrategia vs benchmark

## ⚙️ Configuración

### Variables de Entorno

```env
# Selección de Proveedor de Modelo
MODEL_PROVIDER=vertexai  # Opciones: "openai", "vertexai"

# Configuración OpenAI
OPENAI_API_KEY=sk-...

# Configuración Vertex AI
GOOGLE_CLOUD_PROJECT=tu-id-proyecto
GOOGLE_APPLICATION_CREDENTIALS=ruta/a/credenciales.json
PROJECT=tu-id-proyecto
REGION=us-central1
```

### Parámetros de Estrategia

```python
# Configuración Predeterminada
SHORT_PERIOD = 50      # Media móvil rápida
LONG_PERIOD = 200      # Media móvil lenta
MA_TYPE = 'SMA'        # 'SMA' o 'EMA'
DATA_PERIOD = '2y'     # Período de Yahoo Finance
```

### Configuración de Modelos

```python
# Configuración OpenAI
model = "gpt-4o-mini"
temperature = 0.1

# Configuración Vertex AI
model = "gemini-2.0-flash-001"
temperature = 0.1
max_tokens = 8192
```

## 📈 Métricas de Rendimiento

### Métricas de Estrategia

- **Retorno Total**: Retorno acumulativo de la estrategia
- **Retorno Excesivo**: Retorno de estrategia - Retorno de Comprar y Mantener
- **Tasa de Éxito**: Porcentaje de operaciones rentables
- **Ratio de Sharpe**: Métrica de retorno ajustada por riesgo
- **Máximo Drawdown**: Mayor declive pico-a-valle
- **Volatilidad**: Desviación estándar anualizada

### Métricas de Señales

- **Conteo de Cruces Dorados**: Número de cruces alcistas
- **Conteo de Cruces de la Muerte**: Número de cruces bajistas
- **Retorno Promedio por Operación**: Rentabilidad media de operaciones
- **Frecuencia de Señales**: Tiempo promedio entre señales

### Métricas de Riesgo

- **Volatilidad de Estrategia**: Volatilidad de retornos del portafolio
- **Volatilidad de Benchmark**: Volatilidad de comprar y mantener
- **Correlación**: Correlación estrategia-benchmark
- **Beta**: Medida de riesgo sistemático

## ⚠️ Limitaciones

### Limitaciones de la Estrategia

1. **Riesgo de Whipsaw**: Señales falsas en mercados laterales
2. **Efecto de Retraso**: Las medias móviles miran hacia atrás
3. **Dependencia del Mercado**: Funciona mejor en mercados con tendencia
4. **Costos de Transacción**: No incluidos en backtest

### Limitaciones Técnicas

1. **Dependencia de Datos**: Requiere feed confiable de datos de mercado
2. **Carga Computacional**: Cálculos en tiempo real para múltiples símbolos
3. **Límites de Modelo**: Límites de tasa y costos del proveedor de IA
4. **Internet Requerido**: Acceso a datos en vivo y modelo de IA

### Notas de Implementación

1. **Sin Gestión de Portafolio**: Enfoque en activo único
2. **Sin Gestión de Riesgo**: Sin stop-losses o dimensionamiento de posición
3. **Sin Slippage**: Asume ejecución perfecta
4. **Sesgo Histórico**: Rendimiento pasado no garantiza resultados futuros

## 🔄 Mejoras Futuras

### Características Planificadas

- [ ] **Gestión de Portafolio**: Asignación multi-activo
- [ ] **Gestión de Riesgo**: Stop-loss y dimensionamiento de posición
- [ ] **Alertas en Tiempo Real**: Notificaciones por email/SMS
- [ ] **Motor de Backtesting**: Pruebas históricas de estrategia
- [ ] **Paper Trading**: Modo de simulación en vivo
- [ ] **Interfaz Web**: Aplicación web Streamlit/Flask
- [ ] **Integración de Base de Datos**: Almacenamiento de historial de operaciones
- [ ] **Desarrollo de API**: API RESTful de trading

## 🤝 Contribuciones

1. Hacer fork del repositorio
2. Crear una rama de característica (`git checkout -b feature/caracteristica-increible`)
3. Hacer commit de los cambios (`git commit -m 'Agregar característica increíble'`)
4. Push a la rama (`git push origin feature/caracteristica-increible`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para detalles.


## 🙏 Reconocimientos

- **Yahoo Finance**: Por proporcionar datos de mercado gratuitos
- **LangChain/LangGraph**: Por el framework de agente IA
- **Plotly**: Por visualizaciones interactivas
- **Quantifiable Edges**: Por insights de investigación de estrategias

---

**Descargo de Responsabilidad**: Este software es solo para fines educativos. No es asesoramiento financiero. Opere bajo su propio riesgo.