# Sistema OCR NATS

Un sistema distribuido de OCR (Reconocimiento Óptico de Caracteres) construido con mensajería NATS y RapidOCR, diseñado para el procesamiento de documentos de alto rendimiento en arquitecturas de microservicios.

## 🏗️ Descripción General de la Arquitectura

Este sistema implementa un patrón publicador-suscriptor usando NATS JetStream para entrega confiable de mensajes y procesamiento OCR:

```
Documentos → Publicador → NATS JetStream → Servicio OCR → Stream Resultados → Consumidor
```

### Componentes Clave

- **NATS JetStream**: Proporciona mensajería persistente con garantías de entrega al menos una vez
- **RapidOCR**: Motor OCR de alto rendimiento basado en ONNX
- **Servicios Publicadores**: Envían metadatos de documentos o datos binarios a colas de procesamiento
- **Servicio OCR**: Procesa documentos y extrae texto
- **Servicios Consumidores**: Reciben y manejan resultados OCR

## 📁 Estructura del Repositorio

```
Nats/
├── config.yaml                    # Configuración del motor OCR
├── consumer.ipynb                 # Notebook consumidor de resultados de texto
├── publisher-files.ipynb          # Notebook publicador de archivos binarios
├── publisher-messages.ipynb       # Notebook publicador basado en metadatos
├── publisher.ipynb                # Notebook publicador general
├── notebooks/
│   ├── consumer.ipynb             # Ejemplo simple de consumidor
│   └── publisher.ipynb            # Ejemplo simple de publicador
└── ocr/
    ├── Dockerfile_nats            # Contenedor Docker para servicio OCR
    ├── requirements.txt           # Dependencias Python
    ├── endpoint_ocr_nats.py       # Servicio OCR principal
    ├── utils/                     # Módulos de utilidades
    └── archive/
        └── ocr_rapids.py          # Procesamiento OCR independiente
```

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.11+
- Servidor NATS con JetStream habilitado
- Docker (opcional)

### 1. Iniciar Servidor NATS

```bash
# Usando Docker (recomendado)
docker run -p 4222:4222 nats -js

# O instalar localmente desde https://docs.nats.io/running-a-nats-service/introduction/installation
```

### 2. Instalar Dependencias

```bash
cd ocr/
pip install -r requirements.txt
```

### 3. Configurar Entorno

Crear `ocr/keys/.env_file`:

```env
NAT_URL=nats://localhost:4222
INPUT_STREAM=IMAGE_STREAM
INPUT_SUBJECT=images.process
OUTPUT_STREAM=TEXT_STREAM
OUTPUT_SUBJECT=text.results
DOCS_PATH=/ruta/a/tus/documentos
LOCAL_ENV=1
```

### 4. Ejecutar el Servicio OCR

```bash
cd ocr/
python endpoint_ocr_nats.py
```

### 5. Probar con Notebooks Jupyter

Abre cualquiera de los notebooks publicadores para enviar documentos para procesamiento, y usa el notebook consumidor para recibir resultados.

## 📋 Documentación Detallada

### Sistema de Mensajería NATS

#### NATS Core
NATS es un sistema de mensajería distribuido de alto rendimiento que facilita la comunicación entre aplicaciones a través de un patrón publicador/suscriptor.

**Características Clave:**
- **Rápido y Escalable**: Diseñado para alto rendimiento y escalabilidad
- **Diseño Simple**: Los publicadores envían a temas, los suscriptores reciben de temas
- **Interoperabilidad**: NATS Core y JetStream trabajan juntos sin problemas

#### NATS JetStream
JetStream es un motor de persistencia integrado en NATS que permite almacenamiento y reproducción de mensajes.

**Características Clave:**
- **Motor de Persistencia**: Los mensajes se almacenan y pueden reproducirse
- **Entrega Al Menos Una Vez**: Semántica garantizada de entrega de mensajes
- **Streaming y Reproducción**: Acceso a datos históricos y reproducción de mensajes
- **Suscripciones Duraderas**: Los consumidores pueden reiniciarse y continuar procesando
- **Almacén de Objetos**: Capacidades de almacenamiento y transferencia de archivos

### Configuración OCR

El archivo `config.yaml` controla el comportamiento del motor OCR:

```yaml
Global:
    lang_det: "en_mobile"          # Modelo de detección de idioma
    lang_rec: "en_mobile"          # Modelo de reconocimiento de idioma
    text_score: 0.5                # Umbral mínimo de confianza
    use_det: true                  # Habilitar detección de texto
    use_cls: true                  # Habilitar clasificación de texto
    use_rec: true                  # Habilitar reconocimiento de texto

Det:                               # Configuración de detección de texto
    thresh: 0.3                    # Umbral de detección
    box_thresh: 0.5                # Umbral de caja delimitadora
    
Cls:                               # Configuración de clasificación de texto
    cls_thresh: 0.9                # Umbral de clasificación
    
Rec:                               # Configuración de reconocimiento de texto
    rec_batch_num: 6               # Tamaño de lote para reconocimiento
```

### Formatos de Mensaje

#### Mensaje de Entrada (Metadatos del Documento)
```json
{
    "version": "1.0",
    "batchId": "cadena-uuid",
    "source": {
        "uri": "file:///ruta/al/documento.pdf",
        "mimeType": "application/pdf",
        "size": 1024000
    },
    "ocrOptions": {
        "languages": ["en"],
        "preProcessing": ["resize", "2x-zoom", "rgb"]
    },
    "state": {
        "fileId": "id-archivo-unico",
        "scanId": "identificador-escaneo"
    }
}
```

#### Mensaje de Salida (Resultados OCR)
```json
{
    "version": "1.0",
    "batchId": "cadena-uuid",
    "source": {
        "uri": "file:///ruta/al/documento.pdf",
        "mimeType": "application/pdf",
        "size": 1024000
    },
    "outcome": {
        "success": true,
        "texts": [
            {
                "language": "en",
                "text": "Contenido de texto extraído..."
            }
        ]
    },
    "state": {
        "fileId": "id-archivo-unico",
        "scanId": "identificador-escaneo"
    }
}
```

## 📓 Guía de Notebooks Jupyter

### Notebooks Publicadores

#### 1. `publisher-files.ipynb`
**Propósito**: Publica datos de archivos binarios directamente a NATS

**Caso de Uso**: Cuando necesitas enviar el contenido real del archivo a través de NATS

**Funciones Clave:**
- `publish_images_from_folder()`: Envía datos binarios con encabezados de nombre de archivo
- Adecuado para archivos más pequeños que caben dentro de los límites de carga útil de NATS

#### 2. `publisher-messages.ipynb`
**Propósito**: Publica metadatos de documentos con URIs de archivos

**Caso de Uso**: Enfoque recomendado para archivos grandes y sistemas de producción

**Funciones Clave:**
- `publish_images_from_folder()`: Envía metadatos con URIs file://
- Más eficiente para documentos grandes
- Soporta URLs HTTP y rutas de archivos locales

#### 3. `publisher.ipynb`
**Propósito**: Publicador de propósito general con varios ejemplos

**Características:**
- Utilidades de configuración de stream
- Funciones de publicación de archivos
- Ejemplos de suscriptor para pruebas

### Notebooks Consumidores

#### 1. `consumer.ipynb`
**Propósito**: Consumidor integral de resultados de texto

**Características:**
- Procesamiento de mensajes con análisis JSON
- Capacidades de guardado de archivos
- Manejo de errores y reconocimiento de mensajes
- Directorios de salida configurables

#### 2. `notebooks/consumer.ipynb`
**Propósito**: Ejemplo simple de consumidor

**Caso de Uso**: Consumo básico de mensajes y reconocimiento

## 🐳 Despliegue con Docker

### Construir Contenedor del Servicio OCR

```bash
cd ocr/
docker build -f Dockerfile_nats -t nats-ocr-service .
```

### Ejecutar con Docker Compose

Crear `docker-compose.yml`:

```yaml
version: '3.8'
services:
  nats:
    image: nats:latest
    ports:
      - "4222:4222"
    command: ["-js"]
    
  ocr-service:
    build:
      context: ./ocr
      dockerfile: Dockerfile_nats
    depends_on:
      - nats
    environment:
      - NAT_URL=nats://nats:4222
      - DOCS_PATH=/app/docs
    volumes:
      - ./docs:/app/docs
```

```bash
docker-compose up -d
```

## 🔧 Opciones de Configuración

### Variables de Entorno

| Variable | Valor por Defecto | Descripción |
|----------|-------------------|-------------|
| `NAT_URL` | `nats://localhost:4222` | URL de conexión del servidor NATS |
| `INPUT_STREAM` | `IMAGE_STREAM` | Nombre del stream de entrada |
| `INPUT_SUBJECT` | `images.process` | Patrón del tema de entrada |
| `OUTPUT_STREAM` | `TEXT_STREAM` | Nombre del stream de salida |
| `OUTPUT_SUBJECT` | `text.results` | Patrón del tema de salida |
| `DOCS_PATH` | `/app/docs` | Directorio de almacenamiento de documentos |
| `LOCAL_ENV` | `1` | Bandera de detección de entorno |

### Opciones de Pre-procesamiento OCR

Pasos de pre-procesamiento disponibles:
- `resize`: Redimensionar imagen para OCR óptimo
- `2x-zoom`: Aplicar magnificación 2x
- `rgb`: Convertir a espacio de color RGB
- El procesamiento personalizado se puede agregar en `utils/utils.py`

## 📊 Monitoreo y Registro

### Configuración de Logs

El servicio OCR usa registro estructurado con:
- Salida de consola (nivel INFO)
- Registro de archivos (nivel DEBUG)
- Plantillas de log configurables
- Información de hilo y nombre de archivo

### Monitoreo de NATS

Monitorear streams y consumidores de NATS:

```bash
# Instalar CLI de NATS
curl -sf https://binaries.nats.dev/nats-io/natscli/nats@latest | sh

# Monitorear streams
nats stream list
nats stream info IMAGE_STREAM
nats stream info TEXT_STREAM

# Monitorear consumidores
nats consumer list IMAGE_STREAM
nats consumer info IMAGE_STREAM <nombre-consumidor>
```

## 🔍 Solución de Problemas

### Problemas Comunes

1. **Fallo de Conexión NATS**
   ```
   Error: nats connection failed
   ```
   - Verificar que el servidor NATS esté ejecutándose: `docker ps` o verificar proceso
   - Revisar variable de entorno NAT_URL
   - Asegurar que el puerto 4222 sea accesible

2. **Problemas de Carga de Modelo OCR**
   ```
   Error: failed to load ONNX model
   ```
   - Verificar que los archivos del modelo existan en las rutas especificadas
   - Revisar permisos de archivos
   - Asegurar espacio en disco suficiente

3. **Errores de Archivo No Encontrado**
   ```
   Error: Failed to read local file
   ```
   - Verificar que DOCS_PATH esté configurado correctamente
   - Revisar permisos de archivos
   - Asegurar que los archivos existan en las URIs especificadas

4. **Errores de Procesamiento de Mensajes**
   ```
   Error: Error decoding JSON message
   ```
   - Verificar que el formato del mensaje coincida con el esquema esperado
   - Revisar codificación de caracteres (debería ser UTF-8)
   - Validar estructura JSON

### Modo Debug

Habilitar registro de debug modificando el nivel de log en `endpoint_ocr_nats.py`:

```python
console_log_level="debug"
```

## 📚 Recursos Adicionales

### Documentación NATS
- [Documentación Oficial de NATS](https://docs.nats.io/)
- [Guía de Instalación NATS](https://docs.nats.io/running-a-nats-service/introduction/installation)
- [Guía JetStream](https://docs.nats.io/nats-concepts/jetstream)
- [Cliente Python NATS](https://github.com/nats-io/nats.py)

### Recursos OCR
- [Documentación RapidOCR](https://github.com/RapidAI/RapidOCR)
- [ONNX Runtime](https://onnxruntime.ai/)
- [Modelos PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

### Herramientas de Desarrollo
- [CLI NATS](https://github.com/nats-io/natscli)
- [NATS Box (utilidades Docker)](https://hub.docker.com/r/natsio/nats-box)

## 🤝 Contribución

1. Hacer fork del repositorio
2. Crear una rama de característica
3. Realizar los cambios
4. Agregar pruebas si aplica
5. Enviar un pull request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para detalles.

## 🆘 Soporte

Para problemas y preguntas:
1. Revisar la sección de solución de problemas arriba
2. Revisar la documentación de NATS y RapidOCR
3. Crear un issue en el repositorio
4. Unirse al Slack de la comunidad NATS para ayuda en tiempo real

## 🌟 Características Adicionales

### Escalabilidad
- **Procesamiento Distribuido**: Múltiples instancias del servicio OCR pueden procesar en paralelo
- **Balanceado de Carga**: NATS JetStream distribuye automáticamente los mensajes entre consumidores
- **Tolerancia a Fallos**: Los mensajes se reintentarán automáticamente en caso de falla

### Seguridad
- **Autenticación NATS**: Soporta autenticación basada en tokens y certificados
- **Encriptación TLS**: Comunicación segura entre clientes y servidor
- **Control de Acceso**: Configuración granular de permisos por stream y tema

### Rendimiento
- **Procesamiento Asíncrono**: Operaciones no bloqueantes para máximo throughput
- **Configuración de Lotes**: Procesamiento optimizado de múltiples documentos
- **Caché de Modelos**: Los modelos OCR se cargan una vez y se reutilizan

### Monitoreo Avanzado
- **Métricas de Rendimiento**: Tiempo de procesamiento por documento
- **Estadísticas de Cola**: Monitoreo de backlog y throughput
- **Alertas**: Configuración de alertas para fallos y umbrales de rendimiento