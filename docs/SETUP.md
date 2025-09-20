# 🔧 IDE Setup Guide

This guide provides step-by-step instructions for integrating the Books MCP Server with different development environments and AI assistants.

## 📋 Table of Contents

- [Cursor IDE Setup](#cursor-ide-setup)
- [GitHub Copilot / Claude Desktop Setup](#github-copilot--claude-desktop-setup)
- [VS Code with Extensions](#vs-code-with-extensions)
- [Environment-Specific Configurations](#environment-specific-configurations)
- [Troubleshooting](#troubleshooting)

## 🎯 Cursor IDE Setup

### Step 1: Build Docker Image
```bash
cd /Users/omiderfanmanesh/Projects/MCP-server
docker build -t books-mcp-server .
```

### Step 2: Configure MCP Server

1. **Open Cursor Settings**:
   - Press `Cmd/Ctrl + ,` (or Cursor → Settings)
   - Navigate to **Features** → **Model Context Protocol**
   - Or search for "MCP" in the settings search bar

2. **Add Server Configuration**:
   Click "Edit in Settings JSON" and add:
   ```json
   {
     "mcpServers": {
       "books-mcp-server": {
         "command": "docker",
         "args": ["run", "-i", "--rm", "books-mcp-server"],
         "cwd": "/Users/omiderfanmanesh/Projects/MCP-server"
       }
     }
   }
   ```

3. **Alternative with Local Python**:
   ```json
   {
     "mcpServers": {
       "books-mcp-server": {
         "command": "python",
         "args": ["-m", "mcp_server.server"],
         "cwd": "/Users/username/Projects/MCP-server"
       }
     }
   }
   ```

### Step 3: Verify Connection

1. **Check Status**: Look for a **green indicator** in the MCP panel
2. **Verify Tools**: The following tools should be visible:
   - `books_query` - Search and filter books
   - `currency_exchange` - Convert currencies

### Step 4: Test Integration

Try these example queries in Cursor:
```
"Find science fiction books published after 2020"
"Convert 100 USD to EUR"
"Show me books by Isaac Asimov"
```

## 🤖 GitHub Copilot / Claude Desktop Setup

### Step 1: Locate Configuration File

**macOS**:
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows**:
```bash
%APPDATA%/Claude/claude_desktop_config.json
```

**Linux**:
```bash
~/.config/claude/claude_desktop_config.json
```

### Step 2: Edit Configuration

Create or edit the configuration file:

```json
{
  "mcpServers": {
    "books-mcp-server": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "books-mcp-server"],
      "cwd": "/Users/omiderfanmanesh/Projects/MCP-server"
    }
  }
}
```

### Step 3: Restart Application

- Close Claude Desktop completely
- Reopen the application
- Check for MCP server connection in the interface

## 🆚 VS Code with Extensions

### With MCP Extension

1. **Install MCP Extension** from VS Code Marketplace
2. **Configure in settings.json**:
   ```json
   {
     "mcp.servers": {
       "books-mcp": {
         "command": "python",
         "args": ["-m", "mcp_server.server"],
         "cwd": "/path/to/MCP-server"
       }
     }
   }
   ```

### With GitHub Copilot Chat

Add to your workspace `.vscode/settings.json`:
```json
{
  "github.copilot.chat.localeOverride": "en",
  "mcp.servers": {
    "books-mcp": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "${workspaceFolder}/path/to/MCP-server"
    }
  }
}
```

## 🌍 Environment-Specific Configurations

### Docker (Recommended)

```json
{
  "mcpServers": {
    "books-mcp": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "books-mcp-server"],
      "cwd": "/Users/omiderfanmanesh/Projects/MCP-server"
    }
  }
}
```

### Local Python Environment

```json
{
  "mcpServers": {
    "books-mcp": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/MCP-server"
    }
  }
}
```

### Python Virtual Environment

```json
{
  "mcpServers": {
    "books-mcp": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/MCP-server"
    }
  }
}
```

### Poetry Environment

```json
{
  "mcpServers": {
    "books-mcp": {
      "command": "poetry",
      "args": ["run", "python", "-m", "mcp_server.server"],
      "cwd": "/path/to/MCP-server"
    }
  }
}
```

### Docker Environment

```json
{
  "mcpServers": {
    "books-mcp": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "books-mcp-server"],
      "cwd": "/path/to/MCP-server"
    }
  }
}
```

## 🔍 Troubleshooting

### Common Issues

#### Server Not Connecting
- **Check Python Path**: Ensure Python executable is correct
- **Verify Dependencies**: Run `pip install -r requirements.txt`
- **Check Working Directory**: Use absolute paths in `cwd`

#### Tools Not Visible
- **Restart IDE**: Close and reopen your development environment
- **Check Logs**: Look for error messages in IDE console
- **Verify Syntax**: Ensure JSON configuration is valid

#### Import Errors
```bash
# Test server import
cd /path/to/MCP-server
python -c "from mcp_server.server import main; print('✓ Import successful')"
```

#### Permission Issues
```bash
# Make sure Python executable has proper permissions
which python
ls -la $(which python)
```

### Debug Mode

Add environment variables for debugging:
```json
{
  "mcpServers": {
    "books-mcp": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/MCP-server",
      "env": {
        "DEBUG": "1",
        "MCP_LOG_LEVEL": "debug"
      }
    }
  }
}
```

### Validation Commands

```bash
# Test server startup
python -m mcp_server.server --help

# Check dependencies
pip list | grep mcp

# Verify data files
ls -la data/books.csv
ls -la sample-data/BooksDatasetClean.xlsx
```

## 🎯 Example Queries

Once configured, try these queries:

**Books Search**:
- "Find fantasy books published in the last 5 years"
- "Show me books by specific author"
- "List top-rated science fiction novels"

**Currency Exchange**:
- "Convert 100 USD to EUR"
- "What's the exchange rate from GBP to JPY?"
- "How much is 50 CAD in USD?"

**Combined Queries**:
- "Find books about economics and convert their prices from USD to EUR"
- "Search for travel books and show me currency rates for European countries"

## 📞 Support

If you encounter issues:

1. **Check Configuration**: Verify JSON syntax and paths
2. **Review Logs**: Look for error messages in IDE console
3. **Test Manually**: Run server directly to check for errors
4. **Update Dependencies**: Ensure latest MCP SDK version

For additional help, please refer to:
- [API Documentation](API.md)
- [Usage Examples](EXAMPLES.md)
- [GitHub Issues](https://github.com/omiderfanmanesh/MCP-server/issues)