# Azure AI Agent Application

A Python application that demonstrates interaction with Azure AI Foundry Agent Service for automated wheat production forecasting. This application connects to Azure AI agents, processes user queries about agricultural data, and generates comprehensive markdown reports.

## Overview

This application showcases the integration capabilities of Azure AI Foundry Agent Service by implementing a complete workflow for querying specialized AI agents and documenting their responses. The application features a wheat production forecasting agent that provides detailed agricultural data analysis for major wheat-producing countries and regions worldwide.

## Features

### Core Functionality
- **Agent Integration**: Seamless connection to Azure AI Foundry agents using service principal authentication
- **Conversation Management**: Complete thread-based conversation handling with automatic state management
- **Response Processing**: Intelligent parsing and formatting of agent responses with citation handling
- **Report Generation**: Automatic creation of structured markdown reports with timestamped documentation
- **Error Handling**: Comprehensive error management with detailed logging and user feedback

### Technical Capabilities
- Service principal authentication for secure enterprise integration
- Asynchronous processing with real-time status monitoring
- Support for multiple message types and rich content formatting
- Citation and source reference extraction
- Automated file organization and report archiving

## Architecture

The application follows a modular architecture with clear separation of concerns:

```
main.py                     # Main application logic and orchestration
.env_template              # Environment configuration template
reports/                   # Generated markdown reports directory
├── agent_report_YYYYMMDD_HHMMSS.md
```

### Key Components

1. **Authentication Layer**: Handles Azure service principal authentication using ClientSecretCredential
2. **Agent Client**: Manages connections and interactions with Azure AI Foundry agents
3. **Conversation Engine**: Processes user queries and manages conversation threads
4. **Report Generator**: Creates structured markdown documentation with metadata
5. **Error Management**: Provides comprehensive error handling and user feedback

## Prerequisites

### Azure Requirements
- Azure subscription with appropriate permissions
- Azure AI Foundry resource and project configured
- Service principal with the following roles:
  - Azure AI User role (minimum required)
  - Contributor or Cognitive Services Contributor role (preferred)

### Development Environment
- Python 3.8 or higher
- Azure CLI configured and authenticated
- Required Python packages (see Installation section)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd azure-ai-agent-application
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install azure-ai-projects
   pip install azure-identity
   pip install python-dotenv
   ```

4. **Configure environment variables**
   ```bash
   cp .env_template .env
   # Edit .env with your Azure credentials and endpoints
   ```

## Configuration

### Environment Variables

The application requires the following environment variables to be configured in a `.env` file:

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_TENANT_ID` | Azure Active Directory tenant ID | `b64b8697-93dc-4cc3-b2cf-8fa28f0b81f9` |
| `AZURE_CLIENT_ID` | Service principal application ID | `947fca35-35c1-4316-af96-dc987ad57f98` |
| `AZURE_CLIENT_SECRET` | Service principal secret | `your-client-secret` |
| `PROJECT_ENDPOINT` | Azure AI Foundry project endpoint | `https://your-resource.services.ai.azure.com/api/projects/your-project` |

### Agent Configuration

The application is configured to work with a specific wheat production forecasting agent:
- **Agent ID**: `asst_qBqX2IRzQoyw68eJzo4Txzx8`
- **Agent Name**: Agent_wheat
- **Specialization**: Agricultural data analysis and wheat production forecasting

## Usage

### Running the Application

Execute the main application script:

```bash
python main.py
```

### Application Workflow

1. **Connection Establishment**: The application connects to Azure AI Foundry using service principal credentials
2. **Agent Loading**: Retrieves the specified wheat production forecasting agent
3. **Thread Creation**: Creates a new conversation thread for the session
4. **Query Processing**: Sends the predefined wheat production forecast query to the agent
5. **Response Handling**: Processes the agent's response, including citations and sources
6. **Report Generation**: Creates a timestamped markdown report with complete conversation details

### Sample Query

The application processes queries about wheat production forecasts:

```
Tell me Forecast of Production Wheat 2025 for the following Countries World, US, Russia, EU, China, India and Canada. Try to get concrete numbers.
```

## Output

### Console Output

The application provides detailed console output including:
- Connection status and agent information
- Real-time processing indicators
- Formatted conversation display with timestamps
- Source citations and references
- Session completion summary with statistics

### Generated Reports

Each session generates a comprehensive markdown report containing:
- **Session Metadata**: Timestamp, agent information, thread ID
- **Request Summary**: Overview of the user's query
- **User Question**: Complete original query
- **Agent Response**: Full formatted response with citations
- **Source References**: All cited sources and annotations

### Report Structure

```markdown
# Azure AI Agent Report

**Generated on:** YYYY-MM-DD HH:MM:SS
**Agent:** Agent_wheat (asst_qBqX2IRzQoyw68eJzo4Txzx8)
**Thread ID:** thread_xxxxxxxxxxxxx

## Request Summary
[Automated summary of the request]

## User Question
[Original user query]

## Agent Response
[Complete agent response with formatting and citations]

---
*This report was automatically generated by Azure AI Foundry Agent Service*
```

## Best Practices

### Security
- Never commit sensitive credentials to version control
- Use environment variables for all configuration
- Implement proper secret rotation procedures
- Follow principle of least privilege for role assignments

### Performance
- Implement connection pooling for high-volume scenarios
- Monitor token consumption and implement rate limiting
- Use appropriate timeout values for long-running queries
- Cache frequently requested information when applicable

### Error Handling
- Implement comprehensive retry logic with exponential backoff
- Log detailed error information for debugging
- Provide user-friendly error messages
- Monitor agent status and handle failures gracefully

## Troubleshooting

### Common Issues

**Authentication Errors**
- Verify service principal credentials are correct
- Ensure proper role assignments at the project level
- Check Azure Active Directory tenant configuration

**Connection Issues**
- Validate project endpoint URL format
- Confirm network connectivity to Azure services
- Verify regional availability of services

**Agent Errors**
- Confirm agent ID exists and is accessible
- Check agent deployment status
- Verify model deployment and quota availability

### Debug Mode

For detailed debugging, modify the application to include additional logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Implement changes with appropriate testing
4. Submit a pull request with detailed description

### Code Standards
- Follow PEP 8 Python style guidelines
- Include comprehensive error handling
- Add appropriate documentation and comments
- Maintain backward compatibility when possible

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Related Resources

### Azure AI Foundry Documentation
- [Azure AI Foundry Agent Service Overview](https://learn.microsoft.com/azure/ai-foundry/agents/overview)
- [Agent Service Quickstart Guide](https://learn.microsoft.com/azure/ai-foundry/agents/quickstart)
- [Authentication and Security](https://learn.microsoft.com/azure/ai-foundry/agents/environment-setup)

### SDK References
- [Azure AI Projects Python SDK](https://aka.ms/azsdk/azure-ai-projects/python/reference)
- [Azure Identity Library](https://docs.microsoft.com/python/api/azure-identity/)
- [Azure AI Agents Models](https://learn.microsoft.com/python/api/azure-ai-agents/)

### Support and Community
- [Azure AI Services Technical Community](https://techcommunity.microsoft.com/t5/azure-ai/ct-p/AzureAI)
- [Azure Support Portal](https://azure.microsoft.com/support/)
- [Azure Service Health Dashboard](https://azure.microsoft.com/status/)

## Changelog

### Version 1.0.0
- Initial release with basic agent interaction
- Markdown report generation
- Service principal authentication
- Error handling and logging
- Citation and source extraction