# Complete Tutorial: MCP (Model Context Protocol) and Server Configuration

## Table of Contents
1. [What is MCP (Model Context Protocol)?](#1-what-is-mcp-model-context-protocol)
2. [Client Connection Protocols](#2-client-connection-protocols)
3. [Claude Desktop Application](#3-claude-desktop-application)
4. [Specific MCP Server Configurations](#4-specific-mcp-server-configurations)
5. [Complete Configuration Example](#5-complete-configuration-example)
6. [Verification and Troubleshooting](#6-verification-and-troubleshooting)
7. [Best Practices](#7-best-practices)
8. [Advanced MCP Concepts](#8-advanced-mcp-concepts)
9. [Community and Ecosystem](#9-community-and-ecosystem)
10. [Additional Resources](#10-additional-resources)

## 1. What is MCP (Model Context Protocol)?

The Model Context Protocol (MCP) is an open standard developed by Anthropic that enables AI models to communicate with external data sources, tools, and resources in a standardized way. MCP addresses one of the most significant limitations of current AI systems: their isolation from real-time data and external systems.

### Fundamental MCP Concepts

MCP servers can provide three main types of capabilities:

- **Resources**: File-like data that can be read by clients (such as API responses or file contents)
- **Tools**: Functions that can be called by the LLM (with user approval)
- **Prompts**: Predefined templates that help users perform specific tasks

### MCP Advantages

- **Standardization**: Common protocol for connecting AI with external tools
- **Security**: Granular control over which tools AI can use
- **Extensibility**: Easy addition of new capabilities
- **Interoperability**: Works with different clients and servers
- **Ecosystem Growth**: Rapid development of community-driven servers

### Architecture Overview

MCP follows a client-server architecture where:
- **Hosts** (like Claude Desktop) manage the overall application
- **Clients** maintain connections to MCP servers
- **Servers** provide capabilities to clients through the standardized protocol

This architecture enables a plug-and-play ecosystem where developers can create servers for specific use cases, and these servers can work with any MCP-compatible client.

## 2. Client Connection Protocols

### 2.1. STDIO (Standard Input/Output)
- **Description**: Communication through standard input and output
- **Use**: Most common for desktop applications like Claude Desktop
- **Configuration**: Runs as a child process of the client
- **Advantages**: 
  - Low latency
  - Simple setup
  - Secure (local only)
  - Recommended by MCP specification
- **Limitations**: 
  - Limited to local machine
  - One-to-one client-server relationship

### 2.2. HTTP/SSE (Server-Sent Events)
- **Description**: HTTP-based communication with server-sent events
- **Use**: For remote servers and web applications
- **Configuration**: Requires port and URL configuration
- **Advantages**:
  - Multi-client support
  - Remote deployment capability
  - Web-compatible
  - Authentication support
- **Limitations**:
  - Higher latency
  - Security considerations (DNS rebinding attacks)
  - More complex setup

### 2.3. WebSocket
- **Description**: Bidirectional real-time communication
- **Use**: For applications requiring low latency
- **Status**: In active development
- **Future**: Expected to become more prominent for real-time applications

## 3. Claude Desktop Application

### 3.1. Claude Desktop Installation

You can download Claude Desktop from [claude.ai/download](https://claude.ai/download). The application is available for:

- **macOS**: Native version for Apple Silicon and Intel
- **Windows**: Version for Windows 10/11
- **Linux**: Currently not officially available (community builds exist)

#### System Requirements
- **Node.js**: Version 16 or higher
- **Python**: 3.8 or higher (for Python servers)
- **Java**: 17 or higher (for Java servers)
- **Memory**: At least 4GB RAM recommended
- **Storage**: 500MB for Claude Desktop plus space for MCP servers

#### Installation Tips
1. Always download from the official source
2. Check system compatibility before installation
3. Ensure Node.js is installed and accessible from PATH
4. Consider using a package manager like Homebrew (macOS) or Chocolatey (Windows)

### 3.2. Configuration File Setup

The configuration file is located at:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

#### Basic Configuration File Structure

```json
{
  "mcpServers": {
    "server-name": {
      "command": "command-to-execute",
      "args": ["argument1", "argument2"],
      "env": {
        "ENVIRONMENT_VARIABLE": "value"
      }
    }
  }
}
```

#### Configuration Best Practices
- Always backup your configuration before making changes
- Use absolute paths when possible
- Validate JSON syntax before saving
- Test configurations incrementally
- Document your server purposes with comments (in a separate file)

## 4. Specific MCP Server Configurations

### 4.1. MCP Google Search

An MCP server that provides web search capabilities using Google's Custom Search API and web page content extraction functionality.

**Repository**: [https://github.com/adenot/mcp-google-search](https://github.com/adenot/mcp-google-search)

#### Prerequisites

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable billing for your project

2. **Enable Custom Search API**:
   - Go to [API Library](https://console.cloud.google.com/apis/library)
   - Search for "Custom Search API"
   - Click "Enable"

3. **Get API Key**:
   - Go to [Credentials](https://console.cloud.google.com/apis/credentials)
   - Click "Create Credentials" > "API Key"
   - Copy your API key
   - (Recommended) Restrict the key to Custom Search API only

4. **Create Custom Search Engine**:
   - Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
   - Enter sites you want to search (use `www.google.com` for general web search)
   - Click "Create"
   - In settings, enable "Search the entire web"
   - Copy your Search Engine ID (cx)

#### Installation and Configuration

```bash
# Automatic installation via Smithery
npx -y @smithery/cli install @adenot/mcp-google-search --client claude
```

**Configuration in claude_desktop_config.json**:

```json
{
  "mcpServers": {
    "google-search": {
      "command": "npx",
      "args": [
        "-y",
        "@adenot/mcp-google-search"
      ],
      "env": {
        "GOOGLE_API_KEY": "your-api-key-here",
        "GOOGLE_SEARCH_ENGINE_ID": "your-search-engine-id-here"
      }
    }
  }
}
```

#### Available Tools

- **search**: Perform web searches using Google Custom Search API
- **read_webpage**: Extract content from any web page

#### Usage Tips
- Optimize search queries for better results
- Respect Google's API rate limits (100 searches/day for free tier)
- Consider upgrading to paid plans for higher volume usage
- Use specific search operators when needed (site:, filetype:, etc.)

### 4.2. MCP Server Brave Search

An MCP server implementation that integrates Brave Search API, providing web and local search capabilities.

**Repository**: [https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search](https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search)

#### Prerequisites

1. Sign up for a Brave Search API account at [Brave Search API](https://api.search.brave.com/)
2. Choose a plan (free plan available with 2,000 queries/month)
3. Generate your API key from the developer dashboard

#### Configuration

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-brave-search"
      ],
      "env": {
        "BRAVE_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

#### Available Tools

- **brave_web_search**: Execute web searches with pagination and filtering
- **brave_local_search**: Search for local businesses and services

#### Advantages of Brave Search
- Privacy-focused search engine
- No tracking or profiling
- Independent search index
- Good performance for privacy-conscious users

### 4.3. MCP Server Gmail

An MCP server for Gmail integration in Claude Desktop with automatic authentication support. This server allows AI assistants to manage Gmail through natural language interactions.

**Repository**: [https://github.com/GongRzhe/Gmail-MCP-Server](https://github.com/GongRzhe/Gmail-MCP-Server)

#### Key Features

- Send emails with subject, content, attachments, and recipients
- Full support for international characters
- Read email messages by ID
- View attachment information
- Search emails with various criteria
- Complete label management
- Batch operations for efficient processing

#### Configuration

**1. Create Google Cloud Project and obtain credentials**:

a. Create a Google Cloud Project:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API for your project

b. Create OAuth 2.0 Credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" or "Web application" as application type
   - For web application, add `http://localhost:3000/oauth2callback` to authorized redirect URIs
   - Download the JSON file with OAuth keys
   - Rename the file to `gcp-oauth.keys.json`

**2. Run Authentication**:

```bash
# Global authentication (Recommended)
mkdir -p ~/.gmail-mcp
mv gcp-oauth.keys.json ~/.gmail-mcp/
npx @gongrzhe/server-gmail-autoauth-mcp auth
```

**3. Configure in Claude Desktop**:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": [
        "@gongrzhe/server-gmail-autoauth-mcp"
      ]
    }
  }
}
```

#### Main Tools

- **send_message**: Sends a new email immediately
- **create_draft**: Creates an email draft without sending it
- **read_message**: Retrieves the content of a specific email by its ID
- **search_emails**: Search emails using Gmail search syntax
- **modify_labels**: Add or remove labels from emails
- **delete_message**: Permanently delete an email

#### Gmail Search Syntax Examples
```
# Search for unread emails
is:unread

# Search for emails from specific sender
from:example@domain.com

# Search for emails with attachments
has:attachment

# Search for emails in a date range
after:2024/01/01 before:2024/12/31

# Search for emails with specific subject
subject:"Important Meeting"
```

### 4.4. MCP Server Word

An MCP server for creating, reading, and manipulating Microsoft Word documents. This server allows AI assistants to work with Word documents through a standardized interface.

**Repository**: [https://github.com/GongRzhe/Office-Word-MCP-Server](https://github.com/GongRzhe/Office-Word-MCP-Server)

#### Key Features

- Create new Word documents with metadata
- Extract text and analyze document structure
- Add headers with different levels
- Insert paragraphs with optional styling
- Create tables with custom data
- Add images with proportional scaling
- Format specific text (bold, italic, underline)
- Search and replace text
- Export to different formats (PDF, HTML)

#### Installation

```bash
# Clone the repository
git clone https://github.com/GongRzhe/Office-Word-MCP-Server.git
cd Office-Word-MCP-Server

# Install dependencies
pip install -r requirements.txt
```

#### Configuration

**Option 1: Local installation**
```json
{
  "mcpServers": {
    "word-document-server": {
      "command": "python",
      "args": [
        "/absolute/path/to/word_server.py"
      ]
    }
  }
}
```

**Option 2: Using uvx (Recommended)**
```json
{
  "mcpServers": {
    "word-document-server": {
      "command": "uvx",
      "args": [
        "--from",
        "office-word-mcp-server",
        "word_mcp_server"
      ],
      "env": {}
    }
  }
}
```

#### Main Tools

- **create_document**: Create new document with optional metadata
- **add_paragraph**: Add paragraph to document
- **add_heading**: Add heading with specific level
- **add_table**: Add table with custom data
- **format_text**: Format specific text range
- **search_and_replace**: Search and replace text throughout document
- **insert_image**: Add images with scaling options
- **export_pdf**: Convert document to PDF format

### 4.5. Additional Popular MCP Servers

#### Filesystem Server
**Purpose**: Local file system access
**Repository**: [https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"]
  }
}
```

#### SQLite Server
**Purpose**: Database operations
**Repository**: [https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite](https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite)

```json
{
  "sqlite": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/database.db"]
  }
}
```

#### GitHub Server
**Purpose**: GitHub repository interaction
**Repository**: [https://github.com/modelcontextprotocol/servers/tree/main/src/github](https://github.com/modelcontextprotocol/servers/tree/main/src/github)

```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token-here"
    }
  }
}
```

## 5. Complete Configuration Example

Based on the provided configuration file, here's the complete explained configuration:

```json
{
  "mcpServers": {
    "google-search": {
      "command": "npx",
      "args": [
        "-y",
        "@adenot/mcp-google-search"
      ],
      "env": {
        "GOOGLE_API_KEY": "your-google-api-key",
        "GOOGLE_SEARCH_ENGINE_ID": "your-search-engine-id"
      }
    },
    "gmail": {
      "command": "npx",
      "args": [
        "@gongrzhe/server-gmail-autoauth-mcp"
      ]
    },
    "brave-search": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-brave-search"
      ],
      "env": {
        "BRAVE_API_KEY": "your-brave-api-key"
      }
    },
    "word-document-server": {
      "command": "uvx",
      "args": [
        "--from",
        "office-word-mcp-server",
        "word_mcp_server"
      ],
      "env": {}
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Documents"
      ]
    }
  }
}
```

### Configuration Tips
- Replace placeholder API keys with actual values
- Use environment variables for sensitive data
- Test each server individually before adding to main config
- Keep a backup of working configurations
- Document the purpose of each server

## 6. Verification and Troubleshooting

### 6.1. Verify Configuration

After configuring, restart Claude Desktop and verify:

1. **MCP Icon**: You should see the hammer icon in the interface
2. **Developer Settings**: Go to Settings > Developer to see logs
3. **Connection Status**: Verify that servers appear as "connected"

### 6.2. Common Issues

**1. Servers not connecting**
- Verify absolute paths in configuration
- Check that dependencies are installed
- Review developer logs for specific errors
- Ensure proper JSON formatting

**2. Environment variables not recognized**
- Verify API keys are correctly configured
- Check credential file permissions
- Ensure environment variables are properly set

**3. Commands not working**
- Verify Node.js installation: `node --version`
- Check npm works: `npm --version`
- Test commands manually in terminal
- Check PATH environment variable

**4. Permission issues**
- Ensure Claude Desktop has necessary permissions
- Check file and directory access rights
- Verify API key permissions and quotas

### 6.3. Debugging

For advanced debugging, you can use the MCP Inspector:

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run inspector
mcp-inspector
```

The Inspector will provide a URL to access debugging tools in your browser.

### 6.4. Logging and Monitoring

**Enable verbose logging**:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "your-command",
      "args": ["--verbose"],
      "env": {
        "DEBUG": "mcp:*"
      }
    }
  }
}
```

**Log locations**:
- **macOS**: `~/Library/Application Support/Claude/logs/`
- **Windows**: `%APPDATA%\Claude\logs\`

## 7. Best Practices

### 7.1. Security
- Never commit credentials to version control
- Use environment variables for sensitive API keys
- Regularly review access permissions in your accounts
- Implement least privilege access for API keys
- Monitor API usage for unusual activity
- Use secure credential storage solutions

### 7.2. Performance
- Limit the number of simultaneous MCP servers
- Use batch configurations for mass operations
- Monitor API usage to avoid limits
- Implement caching where appropriate
- Optimize server startup times
- Consider server resource requirements

### 7.3. Maintenance
- Regularly update MCP servers
- Keep backups of your configurations
- Document custom configurations
- Monitor server health and availability
- Plan for API deprecations and changes
- Test configurations after updates

### 7.4. Development
- Start with simple configurations
- Test servers individually before combining
- Use version control for configuration files
- Implement proper error handling
- Follow semantic versioning for custom servers
- Contribute back to the community

## 8. Advanced MCP Concepts

### 8.1. Custom Server Development

You can create your own MCP servers using the official SDKs:

**Python SDK**: [https://github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
**TypeScript SDK**: [https://github.com/modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk)

#### Basic Python Server Example

```python
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

app = Server("my-custom-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="hello",
            description="Say hello",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "hello":
        name = arguments.get("name", "World")
        return [TextContent(type="text", text=f"Hello, {name}!")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

### 8.2. Transport Layer Considerations

#### Choosing the Right Transport

**STDIO (Recommended for most use cases)**:
- Local development
- Simple desktop integrations
- High performance requirements
- Security-sensitive applications

**SSE (Server-Sent Events)**:
- Remote server deployments
- Multi-client scenarios
- Web-based applications
- Cloud integrations

**WebSockets** (Future):
- Real-time bidirectional communication
- Low latency requirements
- Interactive applications

### 8.3. Resource Management

#### Resource Types
- **Static resources**: Configuration files, documentation
- **Dynamic resources**: API responses, database queries
- **Streaming resources**: Large files, real-time data

#### Resource Implementation Example

```python
@app.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="config://settings",
            name="Application Settings",
            mimeType="application/json"
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "config://settings":
        return json.dumps({"setting1": "value1"})
```

### 8.4. Prompt Templates

Prompt templates provide reusable, parameterized prompts for common tasks:

```python
@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    return [
        Prompt(
            name="summarize-email",
            description="Summarize an email",
            arguments=[
                PromptArgument(
                    name="email_content",
                    description="The email content to summarize",
                    required=True
                )
            ]
        )
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict) -> GetPromptResult:
    if name == "summarize-email":
        email_content = arguments["email_content"]
        return GetPromptResult(
            description="Email summary prompt",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"Please summarize this email: {email_content}"
                    )
                )
            ]
        )
```

## 9. Community and Ecosystem

### 9.1. Official Resources

**MCP Specification**: [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
**Official Servers Repository**: [https://github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
**Python SDK**: [https://github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
**TypeScript SDK**: [https://github.com/modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk)

### 9.2. Community Servers

**Awesome MCP Servers**: [https://github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Popular community servers include:
- **Database connectors**: PostgreSQL, MySQL, MongoDB
- **Cloud services**: AWS, Azure, Google Cloud
- **Development tools**: Git, Docker, Kubernetes
- **Communication**: Slack, Discord, Teams
- **Productivity**: Notion, Todoist, Calendar integrations

### 9.3. Server Discovery

**Smithery**: Package manager for MCP servers
```bash
# Install Smithery
npm install -g @smithery/cli

# Search for servers
smithery search email

# Install a server
smithery install @author/server-name --client claude
```

### 9.4. Contributing to the Ecosystem

1. **Create useful servers** for underserved use cases
2. **Contribute to existing servers** with bug fixes and features
3. **Write documentation** and tutorials
4. **Share configurations** and best practices
5. **Report issues** and provide feedback

## 10. Additional Resources

### 10.1. Official Documentation
- **MCP Specification**: [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
- **Anthropic MCP Announcement**: [https://www.anthropic.com/news/model-context-protocol](https://www.anthropic.com/news/model-context-protocol)
- **Claude Desktop MCP Guide**: [https://support.anthropic.com/en/articles/10949351-getting-started-with-model-context-protocol-mcp-on-claude-for-desktop](https://support.anthropic.com/en/articles/10949351-getting-started-with-model-context-protocol-mcp-on-claude-for-desktop)

### 10.2. Development Resources
- **MCP Debugging Guide**: [https://modelcontextprotocol.io/quickstart/debugging](https://modelcontextprotocol.io/quickstart/debugging)
- **Server Development Tutorial**: [https://modelcontextprotocol.io/quickstart/server](https://modelcontextprotocol.io/quickstart/server)
- **Client Development Guide**: [https://modelcontextprotocol.io/quickstart/client](https://modelcontextprotocol.io/quickstart/client)

### 10.3. Tools and Utilities
- **MCP Inspector**: [https://github.com/modelcontextprotocol/inspector](https://github.com/modelcontextprotocol/inspector) - Debug MCP servers
- **MCP Proxy**: Bridge between SSE and stdio transports
- **MCP Remote**: Adapter for remote MCP servers

### 10.4. API Documentation
- **Google Custom Search API**: [https://developers.google.com/custom-search/v1/overview](https://developers.google.com/custom-search/v1/overview)
- **Gmail API**: [https://developers.google.com/gmail/api/guides](https://developers.google.com/gmail/api/guides)
- **Brave Search API**: [https://api.search.brave.com/app/documentation](https://api.search.brave.com/app/documentation)

### 10.5. Community Resources
- **MCP Community Discord**: Join discussions and get help
- **Reddit r/ModelContextProtocol**: Community discussions and sharing
- **Stack Overflow**: Technical questions tagged with `model-context-protocol`
- **YouTube Tutorials**: Video guides and demonstrations

### 10.6. Learning Resources
- **MCP Workshop Series**: Hands-on learning sessions
- **Case Studies**: Real-world MCP implementations
- **Best Practices Guide**: Community-driven recommendations
- **Performance Benchmarks**: Server performance comparisons

### 10.7. Enterprise and Advanced Usage
- **Enterprise Deployment Guide**: Large-scale MCP deployments
- **Security Considerations**: Advanced security configurations
- **Scaling Strategies**: High-availability MCP setups
- **Integration Patterns**: Common architectural patterns

## Conclusion

The Model Context Protocol represents a significant advancement in how AI models can interact with external tools and data. With proper configuration of MCP servers, Claude Desktop becomes a powerful tool capable of managing emails, creating documents, performing web searches, and much more, all through natural conversational interfaces.

The key to success lies in careful configuration, secure credential handling, and understanding the specific capabilities of each MCP server you install. As the MCP ecosystem continues to grow, we can expect to see even more innovative servers and integrations that will further expand the capabilities of AI assistants.

The combination of standardization, security, and extensibility makes MCP a foundational technology for the future of AI-tool integration. Whether you're a developer creating new servers or a user configuring existing ones, MCP provides the tools and framework needed to create powerful, context-aware AI interactions.

### Next Steps

1. **Start Simple**: Begin with one or two servers to understand the basics
2. **Experiment**: Try different combinations of servers to discover new workflows
3. **Contribute**: Share your configurations and experiences with the community
4. **Develop**: Consider creating custom servers for your specific needs
5. **Stay Updated**: Follow the MCP ecosystem for new developments and servers

---

*This guide represents the current state of MCP technology as of June 2025. The MCP ecosystem is rapidly evolving, so check official documentation for the latest updates and features.*