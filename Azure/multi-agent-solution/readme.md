# Azure AI Foundry Connected Agents - Support Ticket Triage System

A comprehensive solution that demonstrates Azure AI Foundry's connected agents capability by building an intelligent support ticket triage system. This system uses multiple specialized AI agents working together to automatically assess, prioritize, and route support tickets.

## 🏗️ Architecture Overview

This solution implements a **multi-agent architecture** where a main "triage agent" coordinates with three specialized connected agents to process support tickets:

```
┌─────────────────┐
│   Triage Agent  │ ← Main orchestrator
│  (Coordinator)  │
└─────────┬───────┘
          │
          ├─── Priority Agent (Urgency Assessment)
          ├─── Team Agent (Team Assignment)  
          └─── Effort Agent (Work Estimation)
```

### Agent Responsibilities

- **🎯 Triage Agent (Main)**: Orchestrates the ticket processing workflow and delegates tasks to specialized agents
- **⚡ Priority Agent**: Assesses ticket urgency (High/Medium/Low)
- **👥 Team Agent**: Determines appropriate team assignment (Frontend/Backend/Infrastructure/Marketing)
- **⏱️ Effort Agent**: Estimates work complexity (Small/Medium/Large)

## 🔌 Communication Protocol

### How Agents Communicate

Azure AI Foundry's connected agents use **function calling** as the primary communication protocol between agents:

1. **Registration**: Connected agents are registered with the main agent using `ConnectedAgentTool` definitions
2. **Natural Language Routing**: The main agent uses natural language understanding to determine when to delegate tasks
3. **Function Invocation**: Connected agents are invoked as functions by the main agent
4. **Response Compilation**: The main agent compiles responses from all connected agents

### Key Features

- ✅ **No Custom Orchestration Required**: Azure handles routing automatically
- ✅ **Natural Language Delegation**: Main agent intelligently routes tasks based on descriptions
- ✅ **Modular Design**: Easy to add new specialized agents without modifying existing ones
- ✅ **Simplified Workflow**: Break down complex tasks across specialized agents

### Protocol Limitations

- ❌ Connected agents cannot call local functions using the function calling tool
- ❌ Citation passing from connected agents is not guaranteed
- ✅ Recommended alternatives: OpenAPI tools or Azure Functions for external integrations

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Azure AI Foundry project with deployed model
- Azure service principal with appropriate permissions

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd azure-ai-foundry-agents
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # Azure AI Foundry Configuration
   PROJECT_ENDPOINT=https://your-project.eastus.inference.ml.azure.com
   MODEL_DEPLOYMENT_NAME=your-model-deployment-name
   
   # Service Principal Credentials
   AZURE_TENANT_ID=your-tenant-id
   AZURE_CLIENT_ID=your-client-id
   AZURE_CLIENT_SECRET=your-client-secret
   ```

### Azure Setup

1. **Create an Azure AI Foundry project**
   - Navigate to [Azure AI Foundry](https://ai.azure.com)
   - Create a new project
   - Deploy a language model (e.g., GPT-4, GPT-3.5-turbo)

2. **Create a service principal**
   ```bash
   az ad sp create-for-rbac --name "ai-foundry-agents-sp" \
     --role "Cognitive Services User" \
     --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group}
   ```

3. **Note the output values for your `.env` file**

## 🎮 Usage

### Running the Application

```bash
python main.py
```

### Example Interaction

```
What's the support problem you need to resolve?: 
> The login page is completely broken and users can't access their accounts

Processing agent thread. Please wait.

USER:
The login page is completely broken and users can't access their accounts

AGENT:
Based on my analysis of this support ticket:

**Priority: High**
This is a user-facing blocking issue that prevents customers from accessing their accounts, requiring immediate attention.

**Team Assignment: Frontend**
This appears to be a user interface issue with the login page, which falls under frontend team responsibilities.

**Effort Estimation: Medium**
This will likely require 2-3 days of work to diagnose the root cause, implement a fix, and thoroughly test the login functionality.

**Summary:** High-priority frontend ticket requiring medium effort to resolve the login access issue.
```

## 📁 Project Structure

```
azure-ai-foundry-agents/
├── main.py              # Main application script
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (create this)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🔧 Code Architecture

### Core Components

1. **Agent Initialization**
   ```python
   # Create specialized agents
   priority_agent = agents_client.create_agent(
       model=model_deployment,
       name="priority_agent",
       instructions=priority_instructions
   )
   ```

2. **Connected Agent Tools**
   ```python
   # Register agents as tools for the main agent
   priority_agent_tool = ConnectedAgentTool(
       id=priority_agent.id,
       name="priority_agent",
       description="Assess the priority of a ticket"
   )
   ```

3. **Main Triage Agent**
   ```python
   # Create orchestrating agent with connected tools
   triage_agent = agents_client.create_agent(
       model=model_deployment,
       name="triage_agent",
       instructions=triage_instructions,
       tools=[priority_tool, team_tool, effort_tool]
   )
   ```

### Agent Instructions

Each agent has specific, focused instructions:

- **Priority Agent**: Categorizes urgency as High/Medium/Low based on user impact
- **Team Agent**: Routes to Frontend/Backend/Infrastructure/Marketing teams
- **Effort Agent**: Estimates as Small/Medium/Large based on complexity

## 🛡️ Security Considerations

- **Environment Variables**: All sensitive credentials stored in `.env` file
- **Service Principal**: Uses least-privilege access with specific role assignments
- **Credential Management**: Leverages Azure Identity library for secure authentication

## 🚀 Extending the Solution

### Adding New Agents

1. **Create the specialized agent**
   ```python
   new_agent = agents_client.create_agent(
       model=model_deployment,
       name="new_agent_name",
       instructions="Specific instructions for the new agent"
   )
   ```

2. **Register as connected tool**
   ```python
   new_agent_tool = ConnectedAgentTool(
       id=new_agent.id,
       name="new_agent_name",
       description="Clear description of when to use this agent"
   )
   ```

3. **Add to main agent's tools**
   ```python
   triage_agent = agents_client.create_agent(
       # ... other parameters
       tools=[existing_tools + [new_agent_tool.definitions[0]]]
   )
   ```

### Potential Extensions

- **🔍 Research Agent**: Gather additional context from knowledge bases
- **📧 Notification Agent**: Send alerts to appropriate team members
- **📊 Analytics Agent**: Track ticket patterns and generate insights
- **🌐 Translation Agent**: Handle multi-language support tickets

## 📊 Performance Considerations

- **Parallel Processing**: Agents can potentially process different aspects simultaneously
- **Cost Optimization**: Each agent focuses on specific tasks, reducing token usage
- **Scalability**: Easy to add new specialized agents without affecting existing workflow

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify service principal credentials in `.env`
   - Ensure proper role assignments in Azure

2. **Model Deployment Issues**
   - Confirm model is deployed and accessible
   - Check deployment name matches environment variable

3. **Agent Creation Failures**
   - Verify project endpoint is correct
   - Ensure sufficient permissions for agent creation

### Debug Mode

Add logging for detailed troubleshooting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Additional Resources

- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Connected Agents Guide](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/connected-agents)
- [Azure Identity Documentation](https://docs.microsoft.com/en-us/python/api/azure-identity/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
