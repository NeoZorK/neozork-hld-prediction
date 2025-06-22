# MCP Servers - Neozork HLD Prediction

🚀 **Model Context Protocol (MCP) Servers for Intelligent Development**

## 📋 Overview

MCP servers provide intelligent autocompletion, context-aware suggestions, and GitHub Copilot integration for the financial analysis project.

## 🎯 Available Servers

### PyCharm GitHub Copilot MCP Server
- **File**: `pycharm_github_copilot_mcp.py`
- **Purpose**: PyCharm IDE with GitHub Copilot
- **Features**: Financial data, technical indicators, AI suggestions

### Auto-Start MCP Server
- **File**: `scripts/auto_start_mcp.py`
- **Purpose**: Automatic server startup
- **Features**: IDE detection, health monitoring, automatic restart

## 🚀 Quick Start

### Installation
```bash
# Install dependencies
pip install -e .

# Verify installation
python scripts/run_cursor_mcp.py --test --report
```

### Starting Servers
```bash
# PyCharm GitHub Copilot MCP Server
python pycharm_github_copilot_mcp.py

# Auto-Start MCP Server
python scripts/auto_start_mcp.py start

# Via runner script
python scripts/run_cursor_mcp.py --mode stdio
```

## 🧪 Testing

```bash
# All MCP server tests
pytest tests/mcp/ -v

# Specific tests
pytest tests/mcp/test_pycharm_github_copilot_mcp.py -v
pytest tests/mcp/test_auto_start_mcp.py -v

# With report
python scripts/run_cursor_mcp.py --test --report
```

## 📊 Features

### Autocompletion
- Financial symbols (BTCUSD, GBPUSD, EURUSD)
- Timeframes (D1, H1, M15, M5)
- Technical indicators (SMA, EMA, RSI, MACD)
- Project functions

### GitHub Copilot Integration
- Context-aware suggestions
- Financial analysis pattern recognition
- Ready-to-use code snippets

### Automatic Startup
- Detection of running IDEs
- Server health monitoring
- Automatic restart on failures

## 🔧 Configuration

### PyCharm
```json
{
  "name": "PyCharm GitHub Copilot MCP",
  "command": "python",
  "args": ["pycharm_github_copilot_mcp.py"],
  "cwd": "/path/to/neozork-hld-prediction",
  "env": {
    "PYTHONPATH": "/path/to/neozork-hld-prediction/src:/path/to/neozork-hld-prediction",
    "LOG_LEVEL": "INFO",
    "MCP_SERVER_TYPE": "pycharm_copilot"
  }
}
```

### Cursor
```json
{
  "mcpServers": {
    "neozork-cursor-mcp": {
      "command": "python",
      "args": ["cursor_mcp_server.py"],
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src:${workspaceFolder}",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## 📈 Performance

| Metric | Value |
|--------|-------|
| Startup time | < 3s |
| Memory usage | 25-50MB |
| Autocompletion response | 5-15ms |
| File indexing | 50ms/file |

## 🐛 Troubleshooting

### Server won't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Check dependencies
pip list | grep -E "(pandas|numpy|watchdog)"

# Check file permissions
ls -la pycharm_github_copilot_mcp.py
```

### No autocompletions
1. Ensure server is running
2. Check logs in `logs/`
3. Restart IDE

### Debugging
```bash
# Enable debug mode
export LOG_LEVEL=DEBUG
python pycharm_github_copilot_mcp.py

# Check status
python scripts/run_cursor_mcp.py --test --report
```

## 📚 Documentation

- [SETUP.md](SETUP.md) - Detailed setup and configuration
- [USAGE.md](USAGE.md) - Usage examples and API

## 🤝 Support

- Create an issue on GitHub
- Check the troubleshooting section
- Contact the development team

---

**MCP Servers** - Enhancing development experience with AI assistance 