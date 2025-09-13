# MCP Servers Demo with Claude AI - Complete Guide

## Table of Contents
1. [Introduction to Model Context Protocol (MCP)](#introduction)
2. [Transport Mechanisms: SSE vs STDIO](#transport-mechanisms)
3. [Prerequisites and Setup](#prerequisites)
4. [MCP Server Configurations](#mcp-server-configurations)
5. [Google Search MCP Server](#google-search-mcp-server)
6. [Gmail API MCP Server](#gmail-api-mcp-server)
7. [Brave Search MCP Server](#brave-search-mcp-server)
8. [Microsoft Office Word MCP Server](#microsoft-office-word-mcp-server)
9. [Claude Desktop Configuration](#claude-desktop-configuration)
10. [Testing and Validation](#testing-and-validation)
11. [Best Practices and Security](#best-practices)
12. [Troubleshooting](#troubleshooting)
13. [Additional Resources](#additional-resources)

## Introduction to Model Context Protocol (MCP) {#introduction}

The **Model Context Protocol (MCP)** is an open standard developed by Anthropic that enables seamless integration between AI assistants like Claude and external data sources, tools, and systems. MCP addresses the challenge of AI models being isolated from data—trapped behind information silos and legacy systems, by providing a universal, open standard for connecting AI systems with data sources, replacing fragmented integrations with a single protocol.

### Key Components

MCP adopts a client-server architecture with three main components:
- **Hosts**: AI applications that initiate connections (e.g., Claude Desktop)
- **Clients**: Systems that maintain one-to-one connections with servers within the host application
- **Servers**: Systems that provide context, tools, and prompts to clients

### Benefits of MCP

- **Standardized Integration**: MCP replaces fragmented approaches with a single, standardized protocol, accelerating development and reducing maintenance burden
- **Flexibility**: Easy switching between different AI models and vendors
- **Security**: Keeps data within your infrastructure while interacting with AI
- **Scalability**: Supports various transports like stdio, WebSockets, HTTP SSE, and UNIX sockets

## Transport Mechanisms: SSE vs STDIO {#transport-mechanisms}

MCP currently defines two standard transport mechanisms for client-server communication: stdio (communication over standard input and output) and HTTP with Server-Sent Events (SSE)

### STDIO Transport

**Characteristics:**
- Enables communication through standard input and output streams, particularly useful for local integrations and command-line tools
- The client launches the MCP server as a subprocess, with the server receiving JSON-RPC messages on stdin and writing responses to stdout
- Low latency for local communication
- Recommended by the specification: "Clients SHOULD support stdio whenever possible"

**Use Cases:**
- Local development environments
- Command-line tools
- In-process integrations
- Local connections where communication occurs within the same machine

**Configuration Example:**
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"]
}
```

### SSE (Server-Sent Events) Transport

**Characteristics:**
- Enables server-to-client streaming with HTTP POST requests for client-to-server communication
- Uses HTTP with Server-Sent Events, and when hosted on HTTPS endpoints, supports encrypted connections via TLS
- Real-time, web-based scenarios
- Seamlessly integrates with OpenAPI endpoints and supports distributed systems with its HTTP foundation

**Use Cases:**
- Remote server connections
- Web-based applications
- Real-time data streaming
- Distributed systems

**Security Considerations:**
SSE transports can be vulnerable to DNS rebinding attacks if not properly secured. To prevent this:
- Always validate Origin headers on incoming SSE connections
- Avoid binding servers to all network interfaces (0.0.0.0) - bind only to localhost (127.0.0.1)
- Implement proper authentication for all SSE connections

### Comparison Summary

| Feature | STDIO | SSE |
|---------|-------|-----|
| **Latency** | Low (local) | Higher (network) |
| **Setup Complexity** | Simple | Moderate |
| **Security** | Local only | Requires HTTPS/auth |
| **Scalability** | Limited to local | High (distributed) |
| **Real-time** | Yes | Yes |
| **OpenAPI Compatible** | Requires proxy | Native |
| **Remote Access** | Requires proxy | Native |

While SSE aligns naturally with modern client tools demanding web-accessible APIs, stdio's local focus necessitates additional steps for broader accessibility

## Prerequisites and Setup {#prerequisites}

### Required Software

1. **Node.js**: Download from [nodejs.org](https://nodejs.org/en/download/)
   ```bash
   # Verify installation
   node --version
   npm --version
   ```

2. **Claude Desktop App**: Download the latest version
   - Ensure it's updated to support MCP
   - Available for macOS and Windows (Linux support via client building)

3. **Python (for Word MCP Server)**: Python 3.10+ required
   ```bash
   # Install uv package manager (Mac/Linux)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### System Requirements

- Operating System: macOS, Windows, or Linux
- Internet connection for API services
- Administrative privileges for installation

## MCP Server Configurations {#mcp-server-configurations}

## Google Search MCP Server {#google-search-mcp-server}

### Overview
The Google Search MCP server enables Claude to perform web searches using Google's Custom Search API.

**Repository**: [https://github.com/adenot/mcp-google-search](https://github.com/adenot/mcp-google-search)

### Setup Process

#### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable billing for your project

#### 2. Enable Custom Search API
1. Navigate to [API Library](https://console.cloud.google.com/apis/library)
2. Search for "Custom Search API"
3. Click "Enable"

#### 3. Generate API Key
1. Go to [Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" > "API Key"
3. Copy your API key
4. (Optional) Restrict the API key to Custom Search API only

#### 4. Create Custom Search Engine
1. Visit [Programmable Search Engine](https://programmablesearchengine.google.com/create/new)
2. Enter sites to search (use `www.google.com` for general web search)
3. Click "Create"
4. On the next page, click "Customize"
5. In settings, enable "Search the entire web"
6. Copy your Search Engine ID (cx parameter)

### Installation
```bash
# Install via npm
npx -y @adenot/mcp-google-search
```

### Configuration
```json
{
  "google-search": {
    "command": "npx",
    "args": ["-y", "@adenot/mcp-google-search"],
    "env": {
      "GOOGLE_API_KEY": "your_api_key_here",
      "GOOGLE_SEARCH_ENGINE_ID": "your_search_engine_id_here"
    }
  }
}
```

## Gmail API MCP Server {#gmail-api-mcp-server}

### Overview
Enables Claude to interact with Gmail, providing email management capabilities.

**Repository**: [https://github.com/GongRzhe/Gmail-MCP-Server](https://github.com/GongRzhe/Gmail-MCP-Server)

### Setup Process

#### 1. Enable Gmail API
1. In Google Cloud Console, go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop app" or "Web application"
4. For Web application, add `http://localhost:3000/oauth2callback` to authorized redirect URIs
5. Download the JSON file with OAuth keys
6. Rename file to `gcp-oauth.keys.json`

#### 2. Install and Configure
```bash
# Install MCP server
npx -y @smithery/cli install @gongrzhe/server-gmail-autoauth-mcp --client claude

# Authenticate client
npx @gongrzhe/server-gmail-autoauth-mcp auth
```

### Configuration
```json
{
  "gmail": {
    "command": "npx",
    "args": ["@gongrzhe/server-gmail-autoauth-mcp"]
  }
}
```

### Capabilities
- Search emails using Gmail search syntax
- Read email content
- Send and draft emails
- Modify email labels
- Batch operations for multiple emails
- Create and manage Gmail labels

## Brave Search MCP Server {#brave-search-mcp-server}

### Overview
Provides web search capabilities using Brave Search API with enhanced privacy features.

**Repository**: [https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search](https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search)

### Setup Process

#### 1. Get Brave Search API Key
1. Sign up for Brave Search API account
2. Choose a plan (Free tier: 2,000 queries/month)
3. Generate API key from developer dashboard

#### 2. Installation
```bash
# Install via npm
npx -y @modelcontextprotocol/server-brave-search
```

### Configuration
```json
{
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": {
      "BRAVE_API_KEY": "your_brave_api_key_here"
    }
  }
}
```

### Features
- General web search
- Local business search  
- News search
- Image search (if supported by API plan)
- Enhanced privacy compared to other search engines

## Microsoft Office Word MCP Server {#microsoft-office-word-mcp-server}

### Overview
Enables Claude to create, edit, and manage Microsoft Word documents programmatically.

**Repository**: [https://github.com/GongRzhe/Office-Word-MCP-Server](https://github.com/GongRzhe/Office-Word-MCP-Server)

### Setup Process

#### 1. Clone Repository
```bash
git clone https://github.com/GongRzhe/Office-Word-MCP-Server.git
cd Office-Word-MCP-Server
```

#### 2. Install Dependencies
```bash
# Using uvx (recommended)
uvx --from office-word-mcp-server word_mcp_server
```

### Configuration
```json
{
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
```

### Capabilities
- Create new Word documents
- Add paragraphs, headings, tables
- Insert images and page breaks
- Format text (bold, italic, colors, fonts)
- Search and replace text
- Add footnotes and endnotes
- Convert documents to PDF
- Password protection
- Document templating

## Claude Desktop Configuration {#claude-desktop-configuration}

### Complete Configuration File

Create or edit `claude_desktop_config.json` in your Claude Desktop application support directory:

**Location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

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
        "GOOGLE_API_KEY": "your_google_api_key",
        "GOOGLE_SEARCH_ENGINE_ID": "your_search_engine_id"
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
        "BRAVE_API_KEY": "your_brave_api_key"
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
    }
  }
}
```

### Configuration Steps

1. **Backup Existing Config**: Always backup your existing configuration
2. **Replace API Keys**: Fill in your actual API keys and credentials
3. **Validate JSON**: Ensure proper JSON formatting
4. **Restart Claude Desktop**: Required for changes to take effect

## Testing and Validation {#testing-and-validation}

### Verification Steps

#### 1. Check MCP Server Status
After restarting Claude Desktop, look for:
- Slider icon in bottom-left corner of input box
- Available tools listed when clicking the slider

#### 2. Test Each Server

**Google Search Server:**
```
Search for "latest AI developments 2025"
```

**Gmail Server:**
```
Show me my recent emails from this week
```

**Brave Search Server:**
```
Search for "sustainable technology trends" using Brave
```

**Word Document Server:**
```
Create a new Word document with a title "MCP Demo" and add a paragraph about MCP benefits
```

#### 3. Manual Server Testing
Test servers individually from command line:

```bash
# Test Google Search server
npx -y @adenot/mcp-google-search

# Test Gmail server  
npx @gongrzhe/server-gmail-autoauth-mcp

# Test Brave Search server
npx -y @modelcontextprotocol/server-brave-search

# Test Word server
uvx --from office-word-mcp-server word_mcp_server
```

### Log Checking

**macOS/Linux:**
```bash
# Check server logs
ls -la ~/Library/Application\ Support/Claude/logs/
tail -f ~/Library/Application\ Support/Claude/logs/mcp-server-*.log
```

**Windows:**
```cmd
# Check logs in AppData/Claude/logs/
dir %APPDATA%\Claude\logs\
```

## Best Practices and Security {#best-practices}

### Security Guidelines

#### 1. API Key Management
- **Never commit API keys** to version control
- Use environment variables for sensitive data
- Regularly rotate API keys
- Apply principle of least privilege to API permissions

#### 2. Transport Security
For SSE servers:
- Always use HTTPS in production
- Validate Origin headers
- Implement proper authentication
- Bind only to localhost for local development

#### 3. Server Permissions
- Claude Desktop runs commands with your user account permissions and file access. Only add commands if you understand and trust the source
- Review server code before installation
- Use sandboxed environments when possible

### Performance Optimization

#### 1. Resource Management
- Monitor memory usage of MCP servers
- Implement connection pooling for high-traffic servers
- Use caching for frequently accessed data

#### 2. Transport Selection
While stdio is great for simple, local developments, SSE offers more in terms of scalability and real-time interaction, making it more suitable for fully-fledged applications

Choose based on your needs:
- **Local development**: Use stdio for simplicity
- **Production/Remote**: Use SSE with proper security
- **High performance**: Consider custom transports

## Troubleshooting {#troubleshooting}

### Common Issues

#### 1. MCP Tools Not Appearing
**Symptoms**: No slider icon or tools visible in Claude Desktop

**Solutions:**
1. Verify JSON syntax in configuration file
2. Check that all required dependencies are installed
3. Restart Claude Desktop completely
4. Verify API keys and credentials

#### 2. Server Connection Failures
**Symptoms**: Error messages about server connectivity

**Solutions:**
1. Test servers manually from command line
2. Check network connectivity
3. Verify firewall settings
4. Review server logs for specific errors

#### 3. Authentication Issues
**Symptoms**: "Authentication failed" or "Unauthorized" errors

**Solutions:**
1. Re-run authentication commands
2. Check API key validity and permissions
3. Verify OAuth credentials and redirect URIs
4. Check API quotas and billing status

#### 4. Node.js/Python Issues
**Symptoms**: "Command not found" or module errors

**Solutions:**
```bash
# Verify Node.js installation
node --version
npm --version

# Verify Python installation  
python --version
uv --version

# Reinstall if necessary
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Debug Commands

```bash
# Test individual servers
npx -y @adenot/mcp-google-search --help
npx @gongrzhe/server-gmail-autoauth-mcp --version

# Check Claude Desktop logs
tail -f ~/Library/Application\ Support/Claude/logs/mcp-server-*.log

# Validate JSON configuration
python -m json.tool claude_desktop_config.json
```

### Getting Help

If issues persist:
1. Check the [MCP debugging guide](https://modelcontextprotocol.io/quickstart/debugging)
2. Review server-specific documentation
3. Join the MCP community discussions
4. Report issues to respective GitHub repositories

## Additional Resources {#additional-resources}

### Official Documentation
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol)
- [Claude Desktop MCP Guide](https://support.anthropic.com/en/articles/10949351-getting-started-with-model-context-protocol-mcp-on-claude-for-desktop)

### Community Resources
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [Claude MCP Community](https://www.claudemcp.com/)
- [MCP Client Boot Starters](https://spring.io/projects/spring-ai)

### Development Tools
- [MCP Inspector Tool](https://github.com/modelcontextprotocol/inspector) - Debug MCP servers
- [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) - Bridge between SSE and stdio transports
- [MCP Remote](https://github.com/modelcontextprotocol/mcp-remote) - Adapter for remote MCP servers

### Example Projects
- [DataCamp MCP Tutorial](https://www.datacamp.com/tutorial/mcp-model-context-protocol) - PR Review Server
- [Weather Server Tutorial](https://modelcontextprotocol.io/quickstart/server) - Basic MCP server implementation

### API Documentation
- [Google Custom Search API](https://developers.google.com/custom-search/v1/overview)
- [Gmail API](https://developers.google.com/gmail/api/guides)
- [Brave Search API](https://api.search.brave.com/app/documentation)

---

## Conclusion

This comprehensive guide covers the setup and configuration of multiple MCP servers with Claude AI, demonstrating the power and flexibility of the Model Context Protocol. MCP provides a universal, open standard for connecting AI systems with data sources, replacing fragmented integrations with a single protocol, enabling more intelligent and context-aware AI interactions.

The combination of Google Search, Gmail, Brave Search, and Word document servers showcases how MCP can connect Claude to various external services and tools, significantly expanding its capabilities beyond text generation to include web search, email management, and document creation.

Remember to prioritize security, follow best practices, and regularly update your MCP servers and Claude Desktop application to benefit from the latest features and security improvements.

**Next Steps:**
1. Experiment with the configured servers
2. Explore additional MCP servers from the community repository
3. Consider developing custom MCP servers for your specific needs
4. Share your experiences with the MCP community

---

*This guide represents the current state of MCP technology as of May 2025. The MCP ecosystem is rapidly evolving, so check official documentation for the latest updates and features.*