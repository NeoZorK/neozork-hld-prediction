# MCP Server Usage Guide

## Overview

Neozork MCP Server is a unified Model Context Protocol server for financial analysis with IDE integration.

## 🚀 Quick Start

### 1. Automatic Start (Recommended)

MCP server starts automatically when opening the project in supported IDEs:

- **Cursor IDE** - automatically
- **PyCharm** - automatically  
- **VS Code** - automatically

### 2. Manual Start

```bash
# Simple start
python3 start_mcp_server.py

# Direct server start
python3 neozork_mcp_server.py

# Start with debug
python3 neozork_mcp_server.py --debug
```

### 3. Status Check

```bash
# Check server status
python3 scripts/check_mcp_status.py

# Show running processes
ps aux | grep neozork_mcp_server
```

## 📁 File Structure

```
📁 MCP Server Files:
├── neozork_mcp_server.py          # Main server
├── neozork_mcp_config.json        # Server configuration
├── start_mcp_server.py            # Start script
├── cursor_mcp_config.json         # Cursor configuration
├── pycharm_mcp_config.json        # PyCharm configuration
├── mcp.json                       # Universal configuration
├── scripts/
│   ├── setup_ide_configs.py       # IDE setup
│   ├── neozork_mcp_manager.py     # Server manager
│   └── check_mcp_status.py        # Status check
└── logs/                          # Server logs
```

## ⚙️ Configuration

### Main Configuration (`neozork_mcp_config.json`)

```json
{
  "server_mode": "unified",
  "server_name": "Neozork Unified MCP Server",
  "version": "2.0.0",
  "features": {
    "financial_data": true,
    "technical_indicators": true,
    "github_copilot": true,
    "code_completion": true,
    "project_analysis": true,
    "ai_suggestions": true
  }
}
```

### IDE Configurations

#### Cursor IDE (`cursor_mcp_config.json`)
```json
{
  "mcpServers": {
    "neozork": {
      "command": "python3",
      "args": ["neozork_mcp_server.py"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "LOG_LEVEL": "INFO"
      },
      "cwd": "${workspaceFolder}"
    }
  }
}
```

#### PyCharm (`pycharm_mcp_config.json`)
```json
{
  "mcpServers": {
    "neozork": {
      "command": "python3",
      "args": ["neozork_mcp_server.py"],
      "env": {
        "PYTHONPATH": "${PROJECT_ROOT}",
        "LOG_LEVEL": "INFO"
      },
      "cwd": "${PROJECT_ROOT}"
    }
  }
}
```

## 🔧 Setup Commands

### IDE Configuration Setup

```bash
# Setup all IDEs
python3 scripts/setup_ide_configs.py

# Setup specific IDE
python3 scripts/neozork_mcp_manager.py create-config cursor
python3 scripts/neozork_mcp_manager.py create-config pycharm
python3 scripts/neozork_mcp_manager.py create-config vscode
```

### Server Management

```bash
# Start manager
python3 scripts/neozork_mcp_manager.py start

# Show status
python3 scripts/neozork_mcp_manager.py status

# Stop server
python3 scripts/neozork_mcp_manager.py stop

# Restart server
python3 scripts/neozork_mcp_manager.py restart
```

## 🐛 Troubleshooting

### Connection Issues

1. **Server won't start**
```bash
# Check Python
python3 --version

# Check dependencies
uv pip list

# Check permissions
ls -la neozork_mcp_server.py
```

2. **IDE not connecting**
```bash
# Restart IDE
# Check configuration
cat cursor_mcp_config.json

# Check logs
tail -f logs/neozork_mcp_*.log
```

3. **Multiple processes**
```bash
# Stop all processes
pkill -f neozork_mcp_server.py

# Check processes
ps aux | grep neozork_mcp_server
```

### Logs

- `logs/neozork_mcp_YYYYMMDD.log` - main server logs
- `logs/mcp_status_check.log` - status check logs
- `logs/ide_setup.log` - IDE setup logs

## 📊 Features

### Available Features

- **Financial Data Integration** - financial data integration
- **Technical Indicators** - technical indicators
- **Code Completion** - code completion
- **Project Analysis** - project analysis
- **AI Suggestions** - AI suggestions
- **GitHub Copilot** - Copilot integration

### MCP Commands

- `neozork/status` - server status
- `neozork/health` - health check
- `neozork/ping` - ping/pong test
- `neozork/metrics` - performance metrics
- `neozork/projectInfo` - project information
- `neozork/financialData` - financial data
- `neozork/indicators` - technical indicators

## 🔄 Development

### Adding New Features

1. Add handler in `neozork_mcp_server.py`
2. Update configuration
3. Add tests
4. Update documentation

### Testing

```bash
# Run tests
python -m pytest tests/mcp/ -v

# Test server
python3 scripts/check_mcp_status.py
```

## 📝 Notes

- Server works in stdio mode for IDE integration
- Configurations are automatically updated when running `setup_ide_configs.py`
- Logs are saved in `logs/` folder
- Server supports hot reload when files change 

## 🛠️ MCP Server Methods & Manual Usage

Below is a list of all available MCP server methods, their purpose, and example requests you can use from the command line.

### How to send a manual request

You can send a request to the MCP server using:
```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "METHOD_NAME", "params": {}}' | python3 neozork_mcp_server.py
```
Replace `METHOD_NAME` and `params` as needed.

---

### List of Methods

#### 1. `neozork/ping`
- **Description:** Simple ping/pong test to check server is alive.
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/ping", "params": {}}' | python3 neozork_mcp_server.py
  ```

#### 2. `neozork/status`
- **Description:** Get server status, uptime, version, memory, etc.
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/status", "params": {}}' | python3 neozork_mcp_server.py
  ```

#### 3. `neozork/health`
- **Description:** Health check, issues, and diagnostics.
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/health", "params": {}}' | python3 neozork_mcp_server.py
  ```

#### 4. `neozork/projectInfo`
- **Description:** Project info: files, symbols, timeframes, functions, classes.
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/projectInfo", "params": {}}' | python3 neozork_mcp_server.py
  ```

#### 5. `neozork/financialData`
- **Description:** List of financial data files, available symbols, and timeframes.
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/financialData", "params": {}}' | python3 neozork_mcp_server.py
  ```
  - **To get timeframes:** Look for the `timeframes` field in the response.

#### 6. `neozork/indicators`
- **Description:** List of available technical indicators.
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/indicators", "params": {}}' | python3 neozork_mcp_server.py
  ```

#### 7. `neozork/codeSearch`
- **Description:** Search for code by query string.
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/codeSearch", "params": {"query": "def "}}' | python3 neozork_mcp_server.py
  ```

#### 8. `neozork/metrics`
- **Description:** Get server and project performance metrics.
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/metrics", "params": {}}' | python3 neozork_mcp_server.py
  ```

#### 9. `neozork/analysis`
- **Description:** Project analysis (size, file types, most recent file).
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/analysis", "params": {}}' | python3 neozork_mcp_server.py
  ```

#### 10. `neozork/suggestions`
- **Description:** Get AI-powered suggestions for project improvement.
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/suggestions", "params": {}}' | python3 neozork_mcp_server.py
  ```

#### 11. `neozork/context`
- **Description:** Get project context (type, languages, frameworks, features).
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/context", "params": {}}' | python3 neozork_mcp_server.py
  ```

#### 12. `neozork/restart`
- **Description:** Restart the MCP server (if supported in your environment).
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/restart", "params": {}}' | python3 neozork_mcp_server.py
  ```

#### 13. `neozork/reload`
- **Description:** Reload project data and re-index code.
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/reload", "params": {}}' | python3 neozork_mcp_server.py
  ```

#### 14. `neozork/version`
- **Description:** Get server version and capabilities.
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/version", "params": {}}' | python3 neozork_mcp_server.py
  ```

#### 15. `neozork/capabilities`
- **Description:** Get server capabilities and supported methods.
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "neozork/capabilities", "params": {}}' | python3 neozork_mcp_server.py
  ```

#### 16. `github/copilot/suggestions`
- **Description:** Get Copilot suggestions for a given context.
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "github/copilot/suggestions", "params": {"context": "financial"}}' | python3 neozork_mcp_server.py
  ```

#### 17. `github/copilot/context`
- **Description:** Get Copilot project context.
- **Example:**
  ```bash
  echo '{"jsonrpc": "2.0", "id": 1, "method": "github/copilot/context", "params": {}}' | python3 neozork_mcp_server.py
  ```

---

**Tip:** You can use any of these methods by changing the `method` and `params` fields in the JSON request.

--- 