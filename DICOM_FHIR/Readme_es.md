# Proyecto de Anonimización DICOM

Una solución integral para anonimizar imágenes médicas DICOM mediante la detección y redacción de Información de Salud Personal (PHI) incrustada como texto dentro de imágenes médicas utilizando el framework Presidio de Microsoft.

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Características](#características)
- [Arquitectura](#arquitectura)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Endpoints de la API](#endpoints-de-la-api)
- [Documentación de Notebooks](#documentación-de-notebooks)
- [Despliegue con Docker](#despliegue-con-docker)
- [Pruebas](#pruebas)
- [Cumplimiento de Estándares](#cumplimiento-de-estándares)
- [Rendimiento](#rendimiento)
- [Contribuciones](#contribuciones)

## Descripción General

Este proyecto implementa un servicio de anonimización de imágenes DICOM (Digital Imaging and Communications in Medicine) que detecta y redacta automáticamente información de texto sensible incrustada en imágenes médicas. La solución utiliza el Redactor de Imágenes Presidio de Microsoft, específicamente diseñado para archivos DICOM, para garantizar el cumplimiento de HIPAA y proteger la privacidad del paciente.

### Componentes Principales

- **Servicio Web FastAPI**: API RESTful para procesar archivos DICOM
- **Integración Presidio**: Detección y redacción avanzada de PHI
- **Procesamiento por Lotes**: Soporte para procesar directorios completos
- **Notebooks Jupyter**: Ejemplos interactivos y herramientas de prueba
- **Soporte Docker**: Despliegue en contenedores

## Características

- **Detección Automática de PHI**: Identifica nombres de pacientes, fechas de nacimiento y otra información sensible
- **Redacción de Texto en Imágenes**: Elimina u oculta texto incrustado en datos de píxeles DICOM
- **Utilización de Metadatos**: Usa metadatos DICOM para mejorar la precisión de detección
- **Múltiples Opciones de Relleno**: Elija entre relleno de contraste o coincidencia de fondo
- **Información de Cajas Delimitadoras**: Devuelve coordenadas de regiones redactadas
- **Procesamiento por Lotes**: Procesa directorios completos de archivos DICOM
- **Monitoreo de Rendimiento**: Capacidades integradas de cronometraje y registro
- **Preservación de Formato**: Mantiene la estructura DICOM y la calidad de imagen médica

## Arquitectura

```
DICOM_FHIR/
├── app/
│   ├── src/
│   │   ├── __init__.py
│   │   └── utils.py              # Utilidades de procesamiento principal
│   ├── endpoint_dicom.py         # Aplicación FastAPI
│   ├── requirements.txt          # Dependencias de Python
│   ├── Dockerfile               # Configuración del contenedor
│   └── __init__.py
├── notebooks/
│   ├── example_dicom_image_redactor.ipynb
│   ├── request_dicom.ipynb
│   ├── treat dicom images.ipynb
│   ├── treat dicom images-2.ipynb
│   └── treat dicom images-3.ipynb
└── README.md
```

## Requisitos Previos

### Requerimientos del Sistema

- Python 3.11+
- Tesseract OCR 5.3.0+
- Docker (opcional, para despliegue en contenedores)
- Memoria suficiente para procesar archivos DICOM grandes

### Librerías Requeridas

- **Presidio**: Framework de protección de datos de Microsoft
- **PyDICOM**: Lectura y escritura de archivos DICOM
- **FastAPI**: Framework web para API
- **OpenCV**: Operaciones de procesamiento de imágenes
- **Matplotlib**: Capacidades de visualización

## Instalación

### 1. Dependencias del Sistema

Instalar Tesseract OCR:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y tesseract-ocr libtesseract-dev

# Verificar instalación
tesseract --version
```

### 2. Entorno Python

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias de Python
pip install -r app/requirements.txt

# Descargar modelo spaCy
python -m spacy download en_core_web_lg
```

### 3. Instalación Docker (Alternativa)

```bash
# Construir imagen Docker
docker build -t dicom-anonymizer ./app

# Ejecutar contenedor
docker run -p 8155:8155 dicom-anonymizer
```

## Uso

### Iniciar el Servicio API

```bash
# Modo desarrollo
cd app
uvicorn endpoint_dicom:app --host 0.0.0.0 --port 8155 --reload

# Modo producción
uvicorn endpoint_dicom:app --host 0.0.0.0 --port 8155
```

### Uso Básico en Python

```python
from presidio_image_redactor import DicomImageRedactorEngine
import pydicom

# Inicializar el motor
engine = DicomImageRedactorEngine()

# Cargar archivo DICOM
dicom_instance = pydicom.dcmread('ruta/al/archivo.dcm')

# Redactar PHI
redacted_instance = engine.redact(dicom_instance, fill="contrast")

# Guardar archivo redactado
redacted_instance.save_as('archivo_redactado.dcm')
```

## Endpoints de la API

### Verificación de Salud

```http
GET /health-check
```

**Respuesta:**
```json
{
  "message": "OK"
}
```

### Procesar Imagen DICOM Individual

```http
POST /process-dicom-image
```

**Parámetros:**
- `file`: Archivo DICOM (formato .dcm)

**Respuesta:**
```json
{
  "redacted_instance": "datos_dicom_codificados_base64",
  "bboxes": "[{\"x\": 10, \"y\": 20, \"width\": 100, \"height\": 30}]"
}
```

**Ejemplo usando curl:**
```bash
curl -X POST "http://localhost:8155/process-dicom-image" \
     -F "file=@muestra.dcm"
```

### Procesar Carpeta DICOM (Por Lotes)

```http
POST /process-dicom-folder
```

**Cuerpo de la Solicitud:**
```json
{
  "folder_in": "ruta_carpeta_entrada",
  "folder_out": "ruta_carpeta_salida"
}
```

**Respuesta:**
```json
{
  "status": true
}
```

**Ejemplo usando curl:**
```bash
curl -X POST "http://localhost:8155/process-dicom-folder" \
     -H "Content-Type: application/json" \
     -d '{"folder_in": "dicom_entrada", "folder_out": "dicom_salida"}'
```

## Documentación de Notebooks

### 1. example_dicom_image_redactor.ipynb

**Propósito**: Tutorial integral y demostración de capacidades de anonimización DICOM.

**Secciones Clave:**
- **Configuración y Requisitos Previos**: Instrucciones de instalación para Tesseract OCR y librerías requeridas
- **Información del Dataset**: Utiliza archivos DICOM de muestra del dataset Pseudo-PHI-DICOM-Data
- **Redacción Básica**: Demuestra procesamiento de imagen individual con diferentes opciones de relleno
- **Procesamiento por Lotes**: Muestra capacidades de procesamiento a nivel de directorio
- **Comparación de Rendimiento**: Comparación visual de imágenes originales vs. redactadas
- **Ajuste de Parámetros**: Ejemplos de ajuste de parámetros de redacción

**Funciones Clave:**
```python
def compare_dicom_images(instance_original, instance_redacted, figsize=(11, 11)):
    """Muestra comparación lado a lado de imágenes DICOM originales y redactadas"""
```

### 2. request_dicom.ipynb

**Propósito**: Pruebas y validación de los endpoints FastAPI con solicitudes reales.

**Características Clave:**
- **Pruebas de API**: Flujo de trabajo completo para probar endpoints de archivo individual y procesamiento por lotes
- **Manejo de Respuestas**: Demuestra decodificación adecuada de respuestas DICOM codificadas en base64
- **Visualización**: Muestra comparaciones antes/después de imágenes procesadas
- **Manejo de Errores**: Ejemplos de manejo de respuestas de API y errores potenciales

**Flujo de Uso:**
1. Cargar y preparar archivos DICOM
2. Enviar solicitudes a endpoints de API
3. Procesar y guardar respuestas
4. Visualizar resultados

### 3. treat dicom images.ipynb

**Propósito**: Evaluación comparativa de rendimiento y comparación entre procesamiento local y llamadas API.

**Métricas Clave:**
- **Tiempo de Procesamiento por Lotes**: Mide tiempo para operaciones a nivel de directorio
- **Tiempo de Respuesta API**: Evalúa procesamiento individual de archivos vía API
- **Análisis de Rendimiento**: Compara diferentes enfoques de procesamiento

**Funciones de Rendimiento:**
```python
def process_dicom_files(input_folder, output_folder):
    """Procesa todos los archivos DICOM en una estructura de carpetas vía llamadas API"""
```

### 4. treat dicom images-2.ipynb

**Propósito**: Manipulación avanzada de DICOM y técnicas de superposición de texto.

**Características Avanzadas:**
- **Superposición de Texto**: Métodos para agregar PHI sintético a imágenes de prueba
- **Soporte Multi-frame**: Manejo de archivos DICOM con múltiples marcos de imagen
- **Renderizado de Texto Adaptativo**: Posicionamiento y dimensionamiento de texto consciente de resolución
- **Exportación de Video**: Conversión de secuencias DICOM multi-frame a formato de video

**Funciones Clave:**
```python
def draw_text_on_image_opencv(image_array, text, position, font_scale, font_color, thickness, font):
    """Dibuja texto en arrays de imágenes DICOM usando OpenCV"""

def draw_text_on_image_opencv_adaptive(image_array, text, position_percent, font_scale_percent, font_color, thickness_percent, font):
    """Renderizado de texto adaptativo por resolución para diferentes tamaños de imagen"""
```

### 5. treat dicom images-3.ipynb

**Propósito**: Capacidades mejoradas de renderizado de texto con funciones adaptativas mejoradas.

**Mejoras:**
- **Mejor Renderizado Adaptativo**: Posicionamiento de texto más sofisticado basado en dimensiones de imagen
- **Procesamiento Multi-imagen**: Flujo de trabajo optimizado para procesar diferentes tipos de imagen
- **Manejo de Errores Mejorado**: Gestión robusta de errores para operaciones de renderizado de texto

## Despliegue con Docker

### Configuración del Dockerfile

El Dockerfile proporcionado incluye:

- **Imagen Base**: Python 3.11-slim para rendimiento óptimo
- **Dependencias del Sistema**: Tesseract OCR, OpenCV y librerías de procesamiento de imágenes
- **Dependencias Python**: Todos los paquetes requeridos con preferencia binaria para construcciones más rápidas
- **Seguridad**: Ejecución de usuario no root
- **Configuración de Puerto**: Expone puerto 8155 para acceso API

### Construcción y Ejecución

```bash
# Construir imagen
docker build -t dicom-anonymizer ./app

# Ejecutar con montaje de volúmenes para procesamiento de datos
docker run -p 8155:8155 \
           -v /ruta/a/entrada:/app/input \
           -v /ruta/a/salida:/app/output \
           dicom-anonymizer

# Ejecutar con variables de entorno
docker run -p 8155:8155 \
           -e LOG_LEVEL=debug \
           dicom-anonymizer
```

## Pruebas

### Pruebas Unitarias

Probar la funcionalidad principal:

```python
import pydicom
from presidio_image_redactor import DicomImageRedactorEngine

def test_basic_redaction():
    engine = DicomImageRedactorEngine()
    instance = pydicom.dcmread('archivo_prueba.dcm')
    redacted, bboxes = engine.redact_and_return_bbox(instance)
    assert redacted is not None
    assert len(bboxes) >= 0
```

### Pruebas de API

Probar funcionalidad de endpoints:

```bash
# Verificación de salud
curl http://localhost:8155/health-check

# Prueba de carga de archivo
curl -X POST "http://localhost:8155/process-dicom-image" \
     -F "file=@prueba.dcm"
```

### Pruebas de Rendimiento

Monitorear tiempos de procesamiento y uso de memoria:

```python
import time
import psutil

def benchmark_processing(file_path):
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss
    
    # Procesar archivo
    result = process_dicom_image(file_path)
    
    end_time = time.time()
    end_memory = psutil.Process().memory_info().rss
    
    return {
        'processing_time': end_time - start_time,
        'memory_used': end_memory - start_memory
    }
```

## Cumplimiento de Estándares

### Estándar DICOM

- **Preservación de Formato**: Mantiene estructura DICOM y metadatos
- **Calidad de Imagen**: Preserva la integridad de imagen médica
- **Cumplimiento**: Sigue las pautas del estándar DICOM

### Cumplimiento HIPAA

- **Protección PHI**: Elimina u oculta toda información de texto identificable
- **Rastro de Auditoría**: Proporciona información de caja delimitadora para verificación de cumplimiento
- **Seguridad de Datos**: Procesamiento seguro sin retención de datos

### Integración FHIR

El proyecto está diseñado para trabajar con sistemas FHIR (Fast Healthcare Interoperability Resources):

- **Intercambio de Datos Estandarizado**: Compatible con estructuras de recursos FHIR
- **Interoperabilidad**: Soporta integración con sistemas de salud
- **Preservación de Metadatos**: Mantiene contexto médico relevante mientras elimina PHI

## Rendimiento

### Estrategias de Optimización

1. **Procesamiento por Lotes**: Procesar múltiples archivos en una sola operación
2. **Gestión de Memoria**: Manejo eficiente de archivos DICOM grandes
3. **Procesamiento Paralelo**: Considerar procesamiento concurrente para datasets grandes
4. **Caché**: Reutilizar instancias de motor para mejor rendimiento

### Métricas de Rendimiento Típicas

- **Imagen Individual**: 2-5 segundos dependiendo del tamaño e imagen y complejidad
- **Procesamiento por Lotes**: 30-60 segundos por 100 imágenes
- **Uso de Memoria**: 500MB-2GB dependiendo de las dimensiones de imagen
- **Precisión**: >95% tasa de detección de PHI

## Contribuciones

### Configuración de Desarrollo

1. Hacer fork del repositorio
2. Crear una rama de características
3. Instalar dependencias de desarrollo
4. Ejecutar pruebas antes de enviar
5. Seguir pautas de estilo de código

### Estilo de Código

- Seguir estándares PEP 8
- Usar type hints donde sea posible
- Documentar funciones con docstrings
- Incluir pruebas unitarias para nuevas características


## Licencia

Este proyecto implementa el framework Presidio de Microsoft y sigue los términos de licencia aplicables. Por favor revise la licencia de Presidio para requerimientos de uso comercial.

## Soporte

Para problemas y preguntas:

1. Revisar la documentación y ejemplos
2. Revisar problemas existentes
3. Enviar reportes de errores detallados con ejemplos reproducibles
4. Incluir información del sistema y logs de errores

## Referencias

- [Estándar DICOM](https://www.dicomstandard.org/about)
- [Documentación Microsoft Presidio](https://microsoft.github.io/presidio/)
- [Especificación FHIR](https://www.hl7.org/fhir/overview.html)
- [Documentación PyDICOM](https://pydicom.github.io/)
- [Documentación FastAPI](https://fastapi.tiangolo.com/)