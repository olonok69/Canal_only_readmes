# Google AI Context Caching with Gemini API

This Jupyter notebook demonstrates how to implement and use Google's Context Caching feature with the Gemini API to optimize token usage and reduce costs when working with large documents repeatedly.

## Overview

Context Caching allows developers to store frequently used input tokens in a dedicated cache and reference them for subsequent requests. This eliminates the need to repeatedly pass the same set of tokens to a model, significantly reducing costs for requests with high input token counts and repeat content.

## What This Notebook Does

The notebook showcases a practical implementation of context caching with Spanish legal documents:

1. **Document Processing**: Loads multiple PDF documents from Google Cloud Storage (Spanish legal texts including civil procedure law and disability assessment regulations)
2. **Performance Comparison**: Demonstrates the difference between cached and non-cached requests
3. **Cost Optimization**: Shows significant token count reduction when using cached content
4. **Multiple Queries**: Performs various queries against the cached documents to show reusability

## Key Features Demonstrated

### Initial Setup
- Authentication with Google Cloud using service account credentials
- Vertex AI initialization with project and region configuration
- Gemini model initialization with safety settings and generation config

### Document Caching
- Creates a cached content object containing multiple PDF documents
- Sets TTL (Time To Live) for cache expiration (60 minutes in this example)
- Stores approximately 247,954 tokens in cache

### Performance Benefits
The notebook shows dramatic improvements:

**Without Cache (First Query):**
- Tokens: 93,114 total (92,880 document + 39 text + 195 response)
- Time: 37.24 seconds

**With Cache (Subsequent Queries):**
- Tokens: 273-495 total (only new text + response tokens)
- Time: 2-3 seconds
- **Token Reduction: ~99.5%**
- **Speed Improvement: ~12-18x faster**

### Use Cases Shown
- Legal document analysis and transcription
- Article extraction from civil procedure law
- Regulatory document interpretation
- Multi-document querying with consistent context

## Technical Implementation

### Cache Creation
```python
content_cache = caching.CachedContent.create(
    model_name="gemini-2.0-flash-001",
    system_instruction=system_instruction,
    contents=contents,  # Multiple PDF documents
    ttl=datetime.timedelta(minutes=60),
)
```

### Model Configuration
- **Model**: gemini-2.0-flash-001
- **Max Output Tokens**: 8,192
- **Temperature**: 1.0
- **Top P**: 0.95
- **Safety Settings**: Block only high-risk content

### Document Storage
Documents are stored in Google Cloud Storage and referenced via GS URIs:
- Civil Procedure Law (ley_enjuiciamiento_civil.pdf)
- Disability Assessment Regulations (BAREMO_AMA_BOE_RD_1971-1999.pdf)
- 2015 Assessment Scale (Baremo 2015.pdf)

## Prerequisites

### Required Dependencies
```python
from vertexai.generative_models import GenerativeModel, Part
import vertexai.generative_models as generative_models
from google.oauth2 import service_account
import vertexai
from vertexai import caching
import datetime
```

### Required Credentials
- Google Cloud service account credentials
- Vertex AI API access
- Gemini API key
- Google Cloud Storage access for document storage

### Environment Variables
- `GEMINI_API_KEY`
- `GOOGLE_API_KEY`
- `GOOGLE_CLOUD_PROJECT`
- `GOOGLE_CLOUD_LOCATION`
- `GOOGLE_GENAI_USE_VERTEXAI`

## Documentation Links

### Official Documentation
- **Context Caching Overview**: [Google Cloud Vertex AI Context Cache](https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview)
- **Official Colab Tutorial**: [Context Caching Introduction](https://colab.research.google.com/github/GoogleCloudPlatform/generative-ai/blob/main/gemini/context-caching/intro_context_caching.ipynb)

### Pricing Information
- **Gemini Models Token Pricing**: [Vertex AI Generative AI Pricing - Gemini Models](https://cloud.google.com/vertex-ai/generative-ai/pricing#gemini-models)
- **Context Caching Pricing**: [Vertex AI Generative AI Pricing - Context Caching](https://cloud.google.com/vertex-ai/generative-ai/pricing#context-caching)

## Benefits of Context Caching

### Cost Reduction
- Cached tokens are charged at a significantly lower rate than regular input tokens
- Ideal for applications that repeatedly query the same large documents
- Substantial savings for high-volume applications

### Performance Improvement
- Faster response times due to pre-processed content
- Reduced latency for subsequent requests
- Better user experience in interactive applications

### Use Cases
- **Legal Document Analysis**: As shown in this notebook
- **Large Document Q&A Systems**: Research papers, manuals, books
- **Customer Support**: FAQ systems with large knowledge bases
- **Educational Platforms**: Textbook and curriculum content analysis
- **Regulatory Compliance**: Policy and regulation interpretation

## Best Practices

1. **Cache Duration**: Set appropriate TTL based on your use case (this example uses 60 minutes)
2. **Content Size**: Optimize for documents with high token counts (>10K tokens) for maximum benefit
3. **Query Patterns**: Most effective when multiple queries will be made against the same content
4. **Monitoring**: Track cache usage and token savings to optimize costs

## Getting Started

1. Set up Google Cloud credentials and enable Vertex AI API
2. Upload your documents to Google Cloud Storage
3. Configure environment variables
4. Run the notebook cells in sequence
5. Monitor token usage and performance improvements

This implementation demonstrates how context caching can transform the economics and performance of large document processing applications, making them more cost-effective and responsive.