# Caché de Contexto de Google AI con la API de Gemini

Este notebook de Jupyter demuestra cómo implementar y usar la funcionalidad de Caché de Contexto de Google con la API de Gemini para optimizar el uso de tokens y reducir costos al trabajar repetidamente con documentos grandes.

## Descripción General

El Caché de Contexto permite a los desarrolladores almacenar tokens de entrada utilizados frecuentemente en una caché dedicada y referenciarlos para solicitudes posteriores. Esto elimina la necesidad de pasar repetidamente el mismo conjunto de tokens al modelo, reduciendo significativamente los costos para solicitudes con altos recuentos de tokens de entrada y contenido repetido.

## Qué Hace Este Notebook

El notebook muestra una implementación práctica del caché de contexto con documentos legales españoles:

1. **Procesamiento de Documentos**: Carga múltiples documentos PDF desde Google Cloud Storage (textos legales españoles incluyendo ley de procedimiento civil y regulaciones de evaluación de discapacidad)
2. **Comparación de Rendimiento**: Demuestra la diferencia entre solicitudes con y sin caché
3. **Optimización de Costos**: Muestra una reducción significativa en el recuento de tokens al usar contenido en caché
4. **Múltiples Consultas**: Realiza varias consultas contra los documentos en caché para mostrar la reutilización

## Características Clave Demostradas

### Configuración Inicial
- Autenticación con Google Cloud usando credenciales de cuenta de servicio
- Inicialización de Vertex AI con configuración de proyecto y región
- Inicialización del modelo Gemini con configuraciones de seguridad y generación

### Caché de Documentos
- Crea un objeto de contenido en caché que contiene múltiples documentos PDF
- Establece TTL (Tiempo de Vida) para la expiración de la caché (60 minutos en este ejemplo)
- Almacena aproximadamente 247,954 tokens en caché

### Beneficios de Rendimiento
El notebook muestra mejoras dramáticas:

**Sin Caché (Primera Consulta):**
- Tokens: 93,114 total (92,880 documento + 39 texto + 195 respuesta)
- Tiempo: 37.24 segundos

**Con Caché (Consultas Posteriores):**
- Tokens: 273-495 total (solo tokens de texto nuevo + respuesta)
- Tiempo: 2-3 segundos
- **Reducción de Tokens: ~99.5%**
- **Mejora de Velocidad: ~12-18x más rápido**

### Casos de Uso Mostrados
- Análisis y transcripción de documentos legales
- Extracción de artículos de la ley de procedimiento civil
- Interpretación de documentos regulatorios
- Consultas multi-documento con contexto consistente

## Implementación Técnica

### Creación de Caché
```python
content_cache = caching.CachedContent.create(
    model_name="gemini-2.0-flash-001",
    system_instruction=system_instruction,
    contents=contents,  # Múltiples documentos PDF
    ttl=datetime.timedelta(minutes=60),
)
```

### Configuración del Modelo
- **Modelo**: gemini-2.0-flash-001
- **Tokens Máximos de Salida**: 8,192
- **Temperatura**: 1.0
- **Top P**: 0.95
- **Configuraciones de Seguridad**: Bloquear solo contenido de alto riesgo

### Almacenamiento de Documentos
Los documentos se almacenan en Google Cloud Storage y se referencian vía URIs de GS:
- Ley de Enjuiciamiento Civil (ley_enjuiciamiento_civil.pdf)
- Regulaciones de Evaluación de Discapacidad (BAREMO_AMA_BOE_RD_1971-1999.pdf)
- Escala de Evaluación 2015 (Baremo 2015.pdf)

## Prerrequisitos

### Dependencias Requeridas
```python
from vertexai.generative_models import GenerativeModel, Part
import vertexai.generative_models as generative_models
from google.oauth2 import service_account
import vertexai
from vertexai import caching
import datetime
```

### Credenciales Requeridas
- Credenciales de cuenta de servicio de Google Cloud
- Acceso a la API de Vertex AI
- Clave API de Gemini
- Acceso a Google Cloud Storage para almacenamiento de documentos

### Variables de Entorno
- `GEMINI_API_KEY`
- `GOOGLE_API_KEY`
- `GOOGLE_CLOUD_PROJECT`
- `GOOGLE_CLOUD_LOCATION`
- `GOOGLE_GENAI_USE_VERTEXAI`

## Enlaces de Documentación

### Documentación Oficial
- **Descripción General del Caché de Contexto**: [Google Cloud Vertex AI Context Cache](https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview)
- **Tutorial Oficial de Colab**: [Introducción al Caché de Contexto](https://colab.research.google.com/github/GoogleCloudPlatform/generative-ai/blob/main/gemini/context-caching/intro_context_caching.ipynb)

### Información de Precios
- **Precios de Tokens de Modelos Gemini**: [Precios de IA Generativa de Vertex AI - Modelos Gemini](https://cloud.google.com/vertex-ai/generative-ai/pricing#gemini-models)
- **Precios de Caché de Contexto**: [Precios de IA Generativa de Vertex AI - Caché de Contexto](https://cloud.google.com/vertex-ai/generative-ai/pricing#context-caching)

## Beneficios del Caché de Contexto

### Reducción de Costos
- Los tokens en caché se cobran a una tarifa significativamente menor que los tokens de entrada regulares
- Ideal para aplicaciones que consultan repetidamente los mismos documentos grandes
- Ahorros sustanciales para aplicaciones de alto volumen

### Mejora de Rendimiento
- Tiempos de respuesta más rápidos debido al contenido preprocesado
- Latencia reducida para solicitudes posteriores
- Mejor experiencia de usuario en aplicaciones interactivas

### Casos de Uso
- **Análisis de Documentos Legales**: Como se muestra en este notebook
- **Sistemas de P&R de Documentos Grandes**: Artículos de investigación, manuales, libros
- **Soporte al Cliente**: Sistemas de FAQ con grandes bases de conocimiento
- **Plataformas Educativas**: Análisis de contenido de libros de texto y currículos
- **Cumplimiento Regulatorio**: Interpretación de políticas y regulaciones

## Mejores Prácticas

1. **Duración de Caché**: Establecer TTL apropiado basado en tu caso de uso (este ejemplo usa 60 minutos)
2. **Tamaño de Contenido**: Optimizar para documentos con altos recuentos de tokens (>10K tokens) para máximo beneficio
3. **Patrones de Consulta**: Más efectivo cuando se harán múltiples consultas contra el mismo contenido
4. **Monitoreo**: Rastrear el uso de caché y ahorro de tokens para optimizar costos

## Cómo Empezar

1. Configurar credenciales de Google Cloud y habilitar la API de Vertex AI
2. Subir tus documentos a Google Cloud Storage
3. Configurar variables de entorno
4. Ejecutar las celdas del notebook en secuencia
5. Monitorear el uso de tokens y mejoras de rendimiento

## Ejemplos de Consultas Realizadas

El notebook incluye consultas específicas sobre documentos legales españoles:

### Ley de Enjuiciamiento Civil
- **Consulta**: "¿Qué nos dice la Ley de Enjuiciamiento civil en el artículo 142? Dame una transcripción completa."
- **Resultado**: Transcripción completa del artículo sobre lengua oficial en actuaciones judiciales

### Real Decreto 1971/1999
- **Consulta**: "¿De qué trata el real Decreto de ministerio de trabajo y asuntos sociales 1971/1999 en su parte dispositiva?"
- **Resultado**: Explicación detallada del reglamento para reconocimiento de grado de minusvalía

### Ley 35/2015
- **Consulta**: "¿De qué trata la ley 35/2015 de 22 septiembre 2015 y qué nos dice en el preámbulo?"
- **Resultado**: Análisis de la reforma del sistema de valoración de daños en accidentes de circulación

## Resultados Destacados

### Eficiencia Operacional
- **Primera consulta sin caché**: 37+ segundos, 93,114 tokens
- **Consultas posteriores con caché**: 2-3 segundos, <500 tokens
- **Ahorro de tiempo**: Reducción de más del 90% en tiempo de respuesta
- **Ahorro de tokens**: Reducción de más del 99% en tokens procesados

Esta implementación demuestra cómo el caché de contexto puede transformar la economía y el rendimiento de las aplicaciones de procesamiento de documentos grandes, haciéndolas más rentables y responsivas para casos de uso en español y análisis de documentación legal.