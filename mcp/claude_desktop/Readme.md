# Claude Desktop Application

## 🚀 Introduction

**Claude Desktop** is a native desktop application that brings the full power of Claude AI directly to your desktop. With enhanced performance, complete **Model Context Protocol (MCP)** support, and advanced productivity features, Claude Desktop transforms your AI workflow.

### ✨ Why Claude Desktop?

- **🔌 MCP Integration**: Connect Claude with external tools and data sources
- **⚡ Native Performance**: Superior speed and efficiency compared to the web version
- **🎯 Advanced Projects**: Persistent context of 200K tokens (~500 pages)
- **🔗 System Integration**: Global shortcuts and direct file system access
- **🛠️ Built-in Tools**: Code analysis, screenshot capture, and more

## 📋 System Requirements

### Windows
- **OS**: Windows 10 (64-bit) or later
- **RAM**: 16 GB minimum (32 GB+ recommended)
- **Storage**: SSD with 100+ GB free space
- **Extras**: Node.js for MCP functionality

### macOS
- **OS**: macOS 11 (Big Sur) or later
- **Processor**: Apple Silicon or Intel
- **RAM**: 16 GB minimum (32 GB+ recommended)
- **Storage**: SSD with 100+ GB free space

### Linux (Community Support)
- **Distributions**: Ubuntu 20.04+, Debian 10+, Fedora, Arch Linux
- **Note**: No official support from Anthropic

## 🔧 Installation

### Windows
1. Download installer from [claude.ai/download](https://claude.ai/download)
2. Run `ClaudeSetup.exe`
3. Follow the installation wizard
4. Sign in with your Claude account

### macOS
1. Download `Claude.dmg` from [claude.ai/download](https://claude.ai/download)
2. Drag Claude to Applications folder
3. Open from Applications (may require security approval)
4. Sign in with your account

### Linux (Community)
```bash
# Debian/Ubuntu
git clone https://github.com/aaddrick/claude-desktop-debian.git
cd claude-desktop-debian
./build.sh
sudo dpkg -i ./claude-desktop_VERSION_ARCHITECTURE.deb
```

## 🎮 Core Features

### Essential Capabilities
- **Multi-model**: Claude 3.5 Sonnet, Haiku, and Opus
- **File handling**: Documents, images, PDFs (up to 30MB)
- **Interactive artifacts**: Dynamic and editable content
- **Voice dictation**: Natural communication with Claude
- **Integrated tools**: Analysis, screenshot capture

### Keyboard Shortcuts
- **Global access**: `Option + Space` (macOS) / `Ctrl + Alt + Space` (Windows)
- **New chat**: `Ctrl/Cmd + K`
- **Send message**: `Enter`
- **New line**: `Shift + Enter`

## 🔌 Model Context Protocol (MCP)

### What is MCP?
MCP is the **"USB port for AI"** - an open standard that enables Claude to securely connect with external tools, databases, and services.

### Basic Setup

1. **Prerequisites**: Node.js 16+ installed
2. **Access configuration**: `Claude menu → Settings → Developer → Edit Config`
3. **File location**:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Configuration Example
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop",
        "/Users/username/Documents"
      ]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

### Available MCP Servers

#### Official
- **Filesystem**: Local file operations
- **GitHub**: Repository management
- **Slack**: Team communication
- **Google Drive**: Cloud storage access
- **PostgreSQL**: Database operations
- **Puppeteer**: Browser automation

#### Community
- AWS, Docker, MongoDB, Notion, Discord, Firebase, Kubernetes, and more

## 📁 Projects (Pro/Team/Enterprise)

### Features
- **Massive context**: 200K tokens (~500 pages)
- **Custom instructions**: Project-specific behavior
- **Knowledge base**: Persistent documents
- **Collaboration**: Team sharing

### Creating Projects
1. Click **"Projects"** (top left corner)
2. **"New Project"**
3. Name, description, and configuration
4. Upload documents (PDF, DOCX, CSV, etc.)

### Custom Instructions Example
```
Role: Senior Python Developer
Focus: Clean, efficient code with comprehensive documentation
Style: Professional but approachable
Output: Include type hints and docstrings
```

## 🆚 Desktop vs Web

| Feature | Desktop | Web |
|---------|---------|-----|
| MCP Integration | ✅ | ❌ |
| Native Performance | ✅ | ❌ |
| Global Shortcuts | ✅ | ❌ |
| File System Access | ✅ | Limited |
| Advanced Projects | ✅ | ✅ |
| Computer Use | ❌ | ✅ |

## 🛠️ Best Practices

### Model Selection
- **Haiku**: Simple and fast tasks
- **Sonnet**: Balanced performance (recommended)
- **Opus**: Complex reasoning

### MCP Optimization
1. Start with file system access
2. Add servers gradually
3. Use absolute paths in configuration
4. Monitor performance impact

### Efficient Workflow
- Group related tasks
- Use keyboard shortcuts
- Organize with Projects
- Create templates for common patterns

## 🔧 Troubleshooting

### Common Issues

#### MCP not connecting
```bash
# Check Node.js
node --version

# Validate JSON
# Use absolute paths
# Restart Claude after changes
```

#### Slow performance
- Check system resources
- Reduce active MCP servers
- Clear application cache
- Update to latest version

#### macOS blocks app
```
System Preferences → Security & Privacy → General → "Open Anyway"
```

## 📞 Support

- **Service status**: [status.anthropic.com](https://status.anthropic.com)
- **Official support**: [support.anthropic.com](https://support.anthropic.com)
- **API documentation**: [docs.anthropic.com](https://docs.anthropic.com)
- **Community**: r/ClaudeAI, r/AnthropicAI

## 🚀 Next Steps

1. **Install Claude Desktop**
2. **Configure basic MCP** (filesystem)
3. **Create your first Project**
4. **Explore additional MCP servers**
5. **Optimize your workflow**

---

**Claude Desktop** - Take your AI productivity to the next level 🚀