# NATS OCR System

A distributed OCR (Optical Character Recognition) system built with NATS messaging and RapidOCR, designed for high-performance document processing in microservice architectures.

## 🏗️ Architecture Overview

This system implements a publish-subscribe pattern using NATS JetStream for reliable message delivery and OCR processing:

```
Documents → Publisher → NATS JetStream → OCR Service → Results Stream → Consumer
```

### Key Components

- **NATS JetStream**: Provides persistent messaging with at-least-once delivery guarantees
- **RapidOCR**: High-performance ONNX-based OCR engine
- **Publisher Services**: Send document metadata or binary data to processing queues
- **OCR Service**: Processes documents and extracts text
- **Consumer Services**: Receive and handle OCR results

## 📁 Repository Structure

```
Nats/
├── config.yaml                    # OCR engine configuration
├── consumer.ipynb                 # Text results consumer notebook
├── publisher-files.ipynb          # Binary file publisher notebook
├── publisher-messages.ipynb       # Metadata-based publisher notebook
├── publisher.ipynb                # General publisher notebook
├── notebooks/
│   ├── consumer.ipynb             # Simple consumer example
│   └── publisher.ipynb            # Simple publisher example
└── ocr/
    ├── Dockerfile_nats            # Docker container for OCR service
    ├── requirements.txt           # Python dependencies
    ├── endpoint_ocr_nats.py       # Main OCR service
    ├── utils/                     # Utility modules
    └── archive/
        └── ocr_rapids.py          # Standalone OCR processing
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- NATS Server with JetStream enabled
- Docker (optional)

### 1. Start NATS Server

```bash
# Using Docker (recommended)
docker run -p 4222:4222 nats -js

# Or install locally from https://docs.nats.io/running-a-nats-service/introduction/installation
```

### 2. Install Dependencies

```bash
cd ocr/
pip install -r requirements.txt
```

### 3. Configure Environment

Create `ocr/keys/.env_file`:

```env
NAT_URL=nats://localhost:4222
INPUT_STREAM=IMAGE_STREAM
INPUT_SUBJECT=images.process
OUTPUT_STREAM=TEXT_STREAM
OUTPUT_SUBJECT=text.results
DOCS_PATH=/path/to/your/documents
LOCAL_ENV=1
```

### 4. Run the OCR Service

```bash
cd ocr/
python endpoint_ocr_nats.py
```

### 5. Test with Jupyter Notebooks

Open any of the publisher notebooks to send documents for processing, and use the consumer notebook to receive results.

## 📋 Detailed Documentation

### NATS Messaging System

#### Core NATS
NATS is a high-performance, distributed messaging system that facilitates communication between applications through a publish/subscribe pattern.

**Key Features:**
- **Fast & Scalable**: Designed for high performance and scalability
- **Simple Design**: Publishers send to subjects, subscribers receive from subjects
- **Interoperability**: Core NATS and JetStream work together seamlessly

#### NATS JetStream
JetStream is a persistence engine built into NATS that enables message storage and replay.

**Key Features:**
- **Persistence Engine**: Messages are stored and can be replayed
- **At-Least-Once Delivery**: Guaranteed message delivery semantics
- **Streaming & Replay**: Historical data access and message replay
- **Durable Subscriptions**: Consumers can restart and continue processing
- **Object Store**: File storage and transfer capabilities

### OCR Configuration

The `config.yaml` file controls OCR engine behavior:

```yaml
Global:
    lang_det: "en_mobile"          # Language detection model
    lang_rec: "en_mobile"          # Language recognition model
    text_score: 0.5                # Minimum confidence threshold
    use_det: true                  # Enable text detection
    use_cls: true                  # Enable text classification
    use_rec: true                  # Enable text recognition

Det:                               # Text detection settings
    thresh: 0.3                    # Detection threshold
    box_thresh: 0.5                # Bounding box threshold
    
Cls:                               # Text classification settings
    cls_thresh: 0.9                # Classification threshold
    
Rec:                               # Text recognition settings
    rec_batch_num: 6               # Batch size for recognition
```

### Message Formats

#### Input Message (Document Metadata)
```json
{
    "version": "1.0",
    "batchId": "uuid-string",
    "source": {
        "uri": "file:///path/to/document.pdf",
        "mimeType": "application/pdf",
        "size": 1024000
    },
    "ocrOptions": {
        "languages": ["en"],
        "preProcessing": ["resize", "2x-zoom", "rgb"]
    },
    "state": {
        "fileId": "unique-file-id",
        "scanId": "scan-identifier"
    }
}
```

#### Output Message (OCR Results)
```json
{
    "version": "1.0",
    "batchId": "uuid-string",
    "source": {
        "uri": "file:///path/to/document.pdf",
        "mimeType": "application/pdf",
        "size": 1024000
    },
    "outcome": {
        "success": true,
        "texts": [
            {
                "language": "en",
                "text": "Extracted text content..."
            }
        ]
    },
    "state": {
        "fileId": "unique-file-id",
        "scanId": "scan-identifier"
    }
}
```

## 📓 Jupyter Notebooks Guide

### Publisher Notebooks

#### 1. `publisher-files.ipynb`
**Purpose**: Publishes binary file data directly to NATS

**Use Case**: When you need to send the actual file contents through NATS

**Key Functions:**
- `publish_images_from_folder()`: Sends binary data with filename headers
- Suitable for smaller files that fit within NATS payload limits

#### 2. `publisher-messages.ipynb`
**Purpose**: Publishes document metadata with file URIs

**Use Case**: Recommended approach for larger files and production systems

**Key Functions:**
- `publish_images_from_folder()`: Sends metadata with file:// URIs
- More efficient for large documents
- Supports HTTP URLs and local file paths

#### 3. `publisher.ipynb`
**Purpose**: General-purpose publisher with various examples

**Features:**
- Stream setup utilities
- File publishing functions
- Subscriber examples for testing

### Consumer Notebooks

#### 1. `consumer.ipynb`
**Purpose**: Comprehensive text results consumer

**Features:**
- Message processing with JSON parsing
- File saving capabilities
- Error handling and message acknowledgment
- Configurable output directories

#### 2. `notebooks/consumer.ipynb`
**Purpose**: Simple consumer example

**Use Case**: Basic message consumption and acknowledgment

## 🐳 Docker Deployment

### Build OCR Service Container

```bash
cd ocr/
docker build -f Dockerfile_nats -t nats-ocr-service .
```

### Run with Docker Compose

Create `docker-compose.yml`:

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

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NAT_URL` | `nats://localhost:4222` | NATS server connection URL |
| `INPUT_STREAM` | `IMAGE_STREAM` | Input stream name |
| `INPUT_SUBJECT` | `images.process` | Input subject pattern |
| `OUTPUT_STREAM` | `TEXT_STREAM` | Output stream name |
| `OUTPUT_SUBJECT` | `text.results` | Output subject pattern |
| `DOCS_PATH` | `/app/docs` | Document storage directory |
| `LOCAL_ENV` | `1` | Environment detection flag |

### OCR Pre-processing Options

Available pre-processing steps:
- `resize`: Resize image for optimal OCR
- `2x-zoom`: Apply 2x magnification
- `rgb`: Convert to RGB color space
- Custom processing can be added in `utils/utils.py`

## 📊 Monitoring and Logging

### Log Configuration

The OCR service uses structured logging with:
- Console output (INFO level)
- File logging (DEBUG level)
- Configurable log templates
- Thread and filename information

### NATS Monitoring

Monitor NATS streams and consumers:

```bash
# Install NATS CLI
curl -sf https://binaries.nats.dev/nats-io/natscli/nats@latest | sh

# Monitor streams
nats stream list
nats stream info IMAGE_STREAM
nats stream info TEXT_STREAM

# Monitor consumers
nats consumer list IMAGE_STREAM
nats consumer info IMAGE_STREAM <consumer-name>
```

## 🔍 Troubleshooting

### Common Issues

1. **NATS Connection Failed**
   ```
   Error: nats connection failed
   ```
   - Verify NATS server is running: `docker ps` or check process
   - Check NAT_URL environment variable
   - Ensure port 4222 is accessible

2. **OCR Model Loading Issues**
   ```
   Error: failed to load ONNX model
   ```
   - Verify model files exist in specified paths
   - Check file permissions
   - Ensure sufficient disk space

3. **File Not Found Errors**
   ```
   Error: Failed to read local file
   ```
   - Verify DOCS_PATH is correctly set
   - Check file permissions
   - Ensure files exist at specified URIs

4. **Message Processing Errors**
   ```
   Error: Error decoding JSON message
   ```
   - Verify message format matches expected schema
   - Check character encoding (should be UTF-8)
   - Validate JSON structure

### Debug Mode

Enable debug logging by modifying the log level in `endpoint_ocr_nats.py`:

```python
console_log_level="debug"
```

## 📚 Additional Resources

### NATS Documentation
- [NATS Official Documentation](https://docs.nats.io/)
- [NATS Installation Guide](https://docs.nats.io/running-a-nats-service/introduction/installation)
- [JetStream Guide](https://docs.nats.io/nats-concepts/jetstream)
- [NATS Python Client](https://github.com/nats-io/nats.py)

### OCR Resources
- [RapidOCR Documentation](https://github.com/RapidAI/RapidOCR)
- [ONNX Runtime](https://onnxruntime.ai/)
- [PaddleOCR Models](https://github.com/PaddlePaddle/PaddleOCR)

### Development Tools
- [NATS CLI](https://github.com/nats-io/natscli)
- [NATS Box (Docker utilities)](https://hub.docker.com/r/natsio/nats-box)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review NATS and RapidOCR documentation
3. Create an issue in the repository
4. Join the NATS community Slack for real-time help