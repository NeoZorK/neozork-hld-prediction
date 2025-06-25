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