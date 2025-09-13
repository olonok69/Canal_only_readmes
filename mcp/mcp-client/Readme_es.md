# Cliente MCP con Herramientas de Análisis Financiero

Una poderosa implementación de cliente del Protocolo de Contexto del Modelo (MCP) que conecta Claude AI con herramientas externas y fuentes de datos, con capacidades especializadas de análisis financiero para indicadores técnicos de trading.

## 🚀 Descripción General

Este repositorio demuestra un ecosistema MCP completo con:
- **Soporte multi-lenguaje de servidores** (Python + Node.js)
- **Herramientas especializadas de análisis financiero** con más de 8 indicadores técnicos
- **Capacidades de procesamiento de documentos** (Word, PDF)
- **Integración de búsqueda web** (Google Custom Search)
- **Arquitectura lista para producción** con manejo integral de errores

## 📋 Tabla de Contenidos

- [¿Qué es MCP?](#qué-es-mcp)
- [Características](#características)
- [Arquitectura](#arquitectura)
- [Instalación](#instalación)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Herramientas Disponibles](#herramientas-disponibles)
- [Capacidades de Análisis Técnico](#capacidades-de-análisis-técnico)
- [Configuración](#configuración)
- [Solución de Problemas](#solución-de-problemas)
- [Contribuciones](#contribuciones)

## 🔍 ¿Qué es MCP?

El Protocolo de Contexto del Modelo (MCP) es un estándar abierto que permite la integración perfecta entre aplicaciones de IA y fuentes de datos y herramientas externas. Crea un puente entre Modelos de Lenguaje Grande (LLMs) como Claude y varios servicios, permitiendo que los asistentes de IA puedan:

- Acceder a datos en tiempo real desde APIs y bases de datos
- Ejecutar funciones y herramientas de forma segura
- Interactuar con sistemas externos eficientemente
- Mantener el contexto de conversación a través de llamadas a herramientas

```
┌─────────────┐    Protocolo MCP     ┌─────────────┐
│ Cliente MCP │ ←→ (JSON-RPC 2.0) ←→ │ Servidor MCP│
│ (+ Claude)  │                      │ (+ Herram.) │
└─────────────┘                      └─────────────┘
```

## ✨ Características

### 🤖 Integración de IA
- **Integración con Claude Sonnet 4** para orquestación inteligente de herramientas
- **Gestión de memoria de conversación** a través de llamadas a herramientas
- **Descubrimiento automático de herramientas** y validación de esquemas

### 📊 Suite de Análisis Financiero
- **Más de 8 Indicadores Técnicos**: Bandas de Bollinger, MACD, Canales de Donchian, Retrocesos de Fibonacci, variantes de RSI
- **Análisis Multi-temporales**: Soporte para períodos de 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y
- **Sistemas de Puntuación Combinados**: Combinaciones ponderadas de indicadores para señales de trading
- **Datos de Yahoo Finance en Tiempo Real**: Integración de datos de mercado en vivo

### 🔧 Arquitectura Multi-Servidor
- **Servidores Python**: Análisis financiero, procesamiento de documentos
- **Servidores Node.js**: Búsqueda web, obtención de datos
- **Diseño Modular**: Fácil agregar nuevos servidores y capacidades

### 📄 Procesamiento de Documentos
- **Creación de Documentos Word**: Generar reportes de resultados de análisis
- **Conversión a PDF**: Conversión automática de formatos de documentos
- **Soporte de Plantillas**: Generación estructurada de documentos

### 🌐 Integración Web
- **Google Custom Search**: Capacidades de búsqueda web con extracción de contenido
- **Obtención de Contenido de URLs**: Leer y procesar contenido de páginas web
- **Procesamiento de Resultados de Búsqueda**: Resumen inteligente de contenido

## 🏗️ Arquitectura

### Capa de Transporte
- **stdio**: Entrada/salida estándar (transporte principal)
- **SSE**: Eventos Enviados por el Servidor (alternativa basada en web)
- **JSON-RPC 2.0**: Protocolo de comunicación

### Estructura de Componentes
```
mcp-client/
├── client.py              # Implementación principal del cliente MCP
├── server/                 # Servidor MCP de análisis financiero
│   ├── main.py            # Servidor de herramientas financieras
│   ├── utils/             # Utilidades de cálculos financieros
│   └── mcp_server_sse.py  # Servidor SSE basado en web
├── index.js               # Servidor MCP de Google Search
└── examples/              # Reportes de análisis y documentación
```

## ⚙️ Instalación

### Prerequisitos
- **Python 3.11+** con gestor de paquetes `uv`
- **Node.js 17+** con `npm`
- **Claves API**: Anthropic, Google Custom Search

### Inicio Rápido

1. **Clonar y Configurar Entorno Python**
```bash
git clone <url-del-repositorio>
cd mcp-client

# Instalar dependencias
uv sync
```

2. **Instalar Dependencias de Node.js** (para servidor de búsqueda)
```bash
npm install axios cheerio @modelcontextprotocol/sdk
```

3. **Configurar Variables de Entorno**
```bash
# Crear archivo .env
cat > .env << EOF
ANTHROPIC_API_KEY=tu_clave_anthropic_aqui
GOOGLE_API_KEY=tu_clave_google_api
GOOGLE_SEARCH_ENGINE_ID=tu_id_motor_busqueda
CLAUDE_MODEL=claude-sonnet-4-20250514
EOF
```

4. **Probar Instalación**
```bash
# Probar servidor de análisis financiero
uv run client.py server/main.py

# Probar servidor de búsqueda (desde terminal separada)
uv run client.py index.js
```

## 🎯 Ejemplos de Uso

### Flujo de Trabajo de Análisis Financiero

```bash
# Iniciar sesión de análisis financiero
uv run client.py server/main.py

# Consultas de ejemplo:
Query: Calcula el Z-Score de Bollinger de Tesla para los últimos 20 días
Query: Analiza AAPL usando la estrategia combinada MACD-Donchian  
Query: Genera un reporte integral de análisis técnico para MSFT usando todos los indicadores
```

### Búsqueda Web e Investigación

```bash
# Iniciar sesión del servidor de búsqueda  
uv run client.py index.js

Query: Busca librerías recientes de quantum machine learning en Python
Query: Crea un reporte en markdown de herramientas de ML cuántico con resúmenes y URLs
Query: Lee el contenido de https://ejemplo.com/articulo y resume los puntos clave
```

### Flujo de Trabajo de Generación de Documentos

```bash
# Iniciar servidor de documentos Word (requiere instalación separada)
uv run client.py ruta/al/word_document_server/main.py

Query: Crea un reporte profesional de mi análisis de Tesla y conviértelo a PDF
Query: Genera un documento de análisis técnico con tablas y guárdalo como QML.docx
```

## 🛠️ Herramientas Disponibles

### Herramientas de Análisis Financiero

| Herramienta | Descripción | Parámetros |
|-------------|-------------|------------|
| `calculate_bollinger_z_score` | Análisis de reversión a la media usando Bandas de Bollinger | `symbol`, `period` |
| `calculate_macd_score_tool` | Análisis de momentum MACD con 3 componentes | `symbol`, `period`, `fast_period`, `slow_period`, `signal_period` |
| `calculate_donchian_channel_score_tool` | Posición del precio dentro de canales Donchian | `symbol`, `period`, `window` |
| `calculate_bollinger_fibonacci_score` | Estrategia combinada Bollinger-Fibonacci | `symbol`, `period`, `window`, `fibonacci_levels`, `num_days` |
| `calculate_combined_score_macd_donchian` | Análisis ponderado MACD + Donchian | `symbol`, `period`, `window` |
| `calculate_connors_rsi_score_tool` | RSI avanzado con componentes de racha y ranking | `symbol`, `period`, `rsi_period`, `streak_period`, `rank_period` |
| `calculate_zscore_indicator_tool` | Z-Score para señales de reversión a la media | `symbol`, `period`, `window` |
| `calculate_combined_connors_zscore_tool` | Análisis combinado momentum + reversión a la media | `symbol`, `period`, `connors_weight`, `zscore_weight` |

### Herramientas de Búsqueda y Web

| Herramienta | Descripción | Parámetros |
|-------------|-------------|------------|
| `search` | Google Custom Search con filtrado de resultados | `query`, `num` |
| `read_webpage` | Extraer y limpiar contenido de páginas web | `url` |

## 📈 Capacidades de Análisis Técnico

### Indicadores Soportados

1. **Z-Score de Bandas de Bollinger**
   - Mide la posición del precio relativa a bandas estadísticas
   - Rango: -3 a +3 (desviaciones estándar)
   - Uso: Señales de reversión a la media

2. **MACD (Convergencia y Divergencia de Medias Móviles)**
   - Puntuación de tres componentes: línea de señal, línea cero, histograma
   - Rango: -100 a +100
   - Uso: Análisis de tendencia y momentum

3. **Canales de Donchian**
   - Posición del precio dentro del rango máximo/mínimo
   - Componentes: Posición (50%), dirección (30%), anchura (20%)
   - Uso: Análisis de ruptura y tendencia

4. **Bollinger-Fibonacci Combinado**
   - Estrategia multi-componente con 4 factores
   - Componentes: Posición de bandas, volatilidad, niveles Fibonacci, momentum
   - Uso: Señales integrales de entrada/salida

5. **RSI de Connors**
   - RSI mejorado con rachas de precios y ranking
   - Componentes: RSI de precio, RSI de rachas, ranking percentil
   - Uso: Condiciones de sobrecompra/sobreventa

6. **Indicador Z-Score**
   - Análisis estadístico de reversión a la media
   - Cálculo de desviación estándar en ventana móvil
   - Uso: Oportunidades de arbitraje estadístico

### Ejemplo de Salida de Análisis

```
Symbol: TSLA, Period: 6mo
Latest combined score: 22.06
Latest MACD score: 9.00
Latest Donchian score: 35.12
Trading Signal: Neutral con Sesgo Alcista
```

### Interpretación de Señales

| Rango de Puntuación | Señal | Acción |
|---------------------|-------|---------|
| +75 a +100 | Compra Fuerte | Posición larga de alta convicción |
| +50 a +75 | Compra | Posición larga moderada |
| +25 a +50 | Compra Débil | Posición larga pequeña o esperar |
| -25 a +25 | Neutral | Mantener posiciones actuales |
| -50 a -25 | Venta Débil | Reducir largos o pequeño corto |
| -75 a -50 | Venta | Cerrar largos o corto moderado |
| -100 a -75 | Venta Fuerte | Señal de corto fuerte |

## ⚙️ Configuración

### Variables de Entorno

```bash
# Requerido para funcionalidad de IA
ANTHROPIC_API_KEY=sk-ant-...           # Acceso a la API de Claude
CLAUDE_MODEL=claude-sonnet-4-20250514  # Especificación del modelo

# Requerido para funcionalidad de búsqueda  
GOOGLE_API_KEY=AIza...                 # Clave API de Google
GOOGLE_SEARCH_ENGINE_ID=017...         # ID del motor de búsqueda personalizado

# Opcional para funcionalidad mejorada
BRAVE_API_KEY=BSA...                   # API de búsqueda alternativa
```

### Configuración del Servidor

El servidor de análisis financiero soporta transportes stdio y SSE:

```python
# Transporte stdio (por defecto)
uv run client.py server/main.py

# Transporte SSE para integración web
python server/mcp_server_sse.py  # Se ejecuta en puerto 8100
```

## 🔧 Solución de Problemas

### Problemas Comunes

1. **Timeouts de Conexión**
   - Las primeras respuestas pueden tomar 30+ segundos (normal para inicialización)
   - Las respuestas subsiguientes son típicamente más rápidas
   - No interrumpir durante el inicio del servidor

2. **Límites de Tasa de API**
   - Yahoo Finance: Sin límites explícitos pero respetar uso razonable
   - Google Search: 100 consultas/día en nivel gratuito
   - Anthropic: Basado en los límites de tu plan

3. **Problemas de Calidad de Datos**
   - Algunos símbolos pueden tener datos históricos limitados
   - Los cálculos de Fibonacci requieren suficientes puntos de giro
   - Verificar fines de semana/feriados que afecten datos más recientes

4. **Configuración del Entorno**
   ```bash
   # Verificar versión de Python
   python --version  # Debe ser 3.11+
   
   # Verificar instalación de uv
   uv --version
   
   # Validar variables de entorno
   echo $ANTHROPIC_API_KEY
   ```

### Modo de Depuración

Habilitar logging detallado:

```python
# En client.py, agregar:
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contribuciones

### Agregando Nuevos Indicadores Financieros

1. **Implementar función de cálculo** en `server/utils/yahoo_finance_tools.py`
2. **Crear wrapper de herramienta MCP** en `server/main.py`
3. **Agregar docstring completo** con parámetros e interpretación
4. **Probar con varios símbolos y marcos temporales**

### Agregando Nuevos Servidores

1. **Crear script de servidor** siguiendo patrones del SDK MCP
2. **Implementar manejadores de herramientas** con manejo apropiado de errores
3. **Actualizar configuración del cliente** para soporte del nuevo servidor
4. **Documentar nuevas capacidades** en README

### Estilo de Código

- **Python**: Seguir PEP 8, usar type hints
- **JavaScript**: Usar sintaxis moderna ES6+, async/await
- **Documentación**: Docstrings y comentarios completos
- **Manejo de Errores**: Degradación elegante y mensajes informativos

## 📊 Análisis de Ejemplo

El repositorio incluye varios reportes completos de análisis técnico:

- **Tesla (TSLA)**: [`4_indicators_tesla_analisys.md`](4_indicators_tesla_analisys.md) - Análisis integral de 4 estrategias
- **Apple (AAPL)**: [`technical_analisys_APPL.md`](technical_analisys_APPL.md) - Evaluación multi-indicador  
- **Microsoft (MSFT)**: [`technical_analisys_MSFT.md`](technical_analisys_MSFT.md) - Recomendaciones de estrategia de trading

## 📚 Recursos Adicionales

- **Documentación MCP**: [Documentos Oficiales del Protocolo de Contexto del Modelo](https://modelcontextprotocol.io/docs)
- **Yahoo Finance API**: [Paquete Python yfinance](https://pypi.org/project/yfinance/)
- **Análisis Técnico**: [Documentación TA-Lib](https://ta-lib.org/)
- **Anthropic Claude**: [Documentación de la API de Claude](https://docs.anthropic.com/)

## 📄 Licencia

Este proyecto es de código abierto. Por favor consulta el archivo LICENSE para más detalles.

## 🎯 Próximos Pasos

- [ ] Agregar soporte para análisis de criptomonedas
- [ ] Implementar framework de backtesting
- [ ] Crear dashboard web para visualización
- [ ] Agregar sistema de alertas para notificaciones de señales
- [ ] Expandir a mercados forex y commodities

---

**Construido con ❤️ usando el Protocolo de Contexto del Modelo y Claude AI**