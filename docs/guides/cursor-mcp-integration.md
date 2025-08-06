# Cursor IDE MCP Integration Guide

This guide explains how to integrate the Neozork MCP Server with Cursor IDE for enhanced financial analysis capabilities.

## Overview

The Neozork MCP Server provides intelligent code completion, financial data analysis, and AI-powered suggestions for financial analysis projects in Cursor IDE.

## Features

- **Financial Data Integration**: Access to financial symbols, timeframes, and data files
- **Technical Indicators**: Auto-completion for RSI, MACD, EMA, Bollinger Bands, and more
- **Code Snippets**: Pre-built snippets for common financial analysis tasks
- **Project Analysis**: Intelligent suggestions based on project structure
- **AI Integration**: GitHub Copilot-style suggestions for financial code
- **Real-time Monitoring**: Server status, health checks, and performance metrics

## Installation

### 1. Prerequisites

Ensure you have the following installed:
- Python 3.8+
- Cursor IDE
- uv package manager (recommended)

### 2. Server Setup

The MCP server is already configured in your project. To verify:

```bash
# Check if server file exists
ls -la neozork_mcp_server.py

# Test server startup
uv run python neozork_mcp_server.py
```

### 3. Cursor IDE Configuration

#### Automatic Setup (Recommended)

1. Copy the `cursor_mcp_config.json` file to your Cursor IDE configuration directory:
   ```bash
   # macOS
   cp cursor_mcp_config.json ~/Library/Application\ Support/Cursor/User/globalStorage/
   
   # Windows
   copy cursor_mcp_config.json %APPDATA%\Cursor\User\globalStorage\
   
   # Linux
   cp cursor_mcp_config.json ~/.config/Cursor/User/globalStorage/
   ```

2. Restart Cursor IDE

#### Manual Setup

1. Open Cursor IDE
2. Go to Settings (Cmd/Ctrl + ,)
3. Search for "MCP" or "Model Context Protocol"
4. Add the following configuration:

```json
{
  "mcpServers": {
    "neozork": {
      "command": "uv",
      "args": ["run", "python", "neozork_mcp_server.py"],
      "env": {
        "PYTHONPATH": ".",
        "LOG_LEVEL": "INFO"
      },
      "cwd": "${workspaceFolder}",
      "transport": "stdio"
    }
  }
}
```

## Usage

### 1. Starting the Server

The server can be started in several ways:

#### Automatic (Recommended)
- Cursor IDE will automatically start the server when you open a project
- The server runs in the background and provides real-time assistance

#### Manual
```bash
# Start server manually
uv run python neozork_mcp_server.py

# Start with debug mode
uv run python neozork_mcp_server.py --debug

# Start with custom config
uv run python neozork_mcp_server.py --config custom_config.json
```

### 2. Using Features

#### Code Completion
- Type `calculate_` to see available financial calculation functions
- Type `RSI`, `MACD`, `EMA` for technical indicators
- Type `GBPUSD`, `EURUSD` for financial symbols

#### Snippets
- Type `import_pandas` for pandas import snippet
- Type `read_financial_data` for data loading snippet
- Type `backtest_strategy` for strategy backtesting snippet

#### AI Suggestions
- The server provides context-aware suggestions for financial analysis code
- Suggestions appear automatically as you type

### 3. Checking Server Status

Use the status checker script:

```bash
uv run python scripts/mcp/check_mcp_status.py
```

This will show:
- Server health status
- Cursor integration status
- Dependency checks
- Performance metrics

## Configuration

### Server Configuration

The server uses `neozork_mcp_config.json` for configuration:

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
  },
  "performance": {
    "max_files": 15000,
    "max_file_size": "10MB",
    "cache_enabled": true
  }
}
```

### Cursor IDE Configuration

Advanced Cursor IDE settings in `cursor_mcp_config.json`:

```json
{
  "serverSettings": {
    "neozork": {
      "enabled": true,
      "autoStart": true,
      "debug": false,
      "logLevel": "info",
      "features": {
        "financial_data": true,
        "technical_indicators": true,
        "code_completion": true,
        "project_analysis": true,
        "ai_suggestions": true
      }
    }
  }
}
```

## Monitoring and Diagnostics

### Available Commands

The server provides several monitoring commands:

- `neozork/status` - Server status and uptime
- `neozork/health` - Health check with issues
- `neozork/ping` - Simple ping/pong test
- `neozork/metrics` - Performance metrics
- `neozork/diagnostics` - System diagnostics
- `neozork/version` - Version information
- `neozork/capabilities` - Server capabilities
- `neozork/restart` - Restart server
- `neozork/reload` - Reload project data

### Logs

Server logs are saved to:
- `logs/neozork_mcp_server.log` - Main server log
- `logs/neozork_mcp_state.json` - Server state
- `logs/mcp_status_check.json` - Status check results

### Performance Monitoring

The server tracks:
- Memory usage
- CPU usage
- File processing statistics
- Code indexing metrics
- Financial data statistics

## Troubleshooting

### Common Issues

#### 1. Server Won't Start
```bash
# Check Python version
python --version

# Check dependencies
uv pip list

# Check file permissions
ls -la neozork_mcp_server.py
```

#### 2. Cursor IDE Not Connecting
```bash
# Check Cursor configuration
cat ~/Library/Application\ Support/Cursor/User/globalStorage/cursor_mcp_config.json

# Restart Cursor IDE
# Check Cursor logs
```

#### 3. No Code Completion
```bash
# Check server status
uv run python scripts/mcp/check_mcp_status.py

# Verify project structure
ls -la src/ data/ tests/
```

#### 4. Performance Issues
```bash
# Check server metrics
# Look for large files or slow indexing
# Consider adjusting max_files in config
```

### Debug Mode

Enable debug mode for detailed logging:

```bash
# Start with debug
uv run python neozork_mcp_server.py --debug

# Or set environment variable
LOG_LEVEL=DEBUG uv run python neozork_mcp_server.py
```

### Getting Help

1. Check the status checker output
2. Review server logs in `logs/` directory
3. Run diagnostics: `neozork/diagnostics`
4. Check Cursor IDE logs
5. Verify configuration files

## Advanced Features

### Custom Snippets

Add custom snippets by modifying the `_get_code_snippets()` method in `neozork_mcp_server.py`.

### Custom Indicators

Add new technical indicators by extending the `_get_indicator_completions()` method.

### Project-Specific Configuration

Create project-specific configurations by modifying `neozork_mcp_config.json` for different projects.

### Integration with Other Tools

The MCP server can be integrated with:
- VS Code (with MCP extension)
- PyCharm (with MCP plugin)
- Other LSP-compatible editors

## Security Considerations

- The server runs locally and doesn't send data externally
- All financial data remains on your local machine
- No API keys or sensitive data are transmitted
- Server communication is via stdio (no network ports)

## Performance Tips

1. **File Limits**: Adjust `max_files` in config for large projects
2. **Caching**: Enable caching for better performance
3. **Indexing**: Server re-indexes on startup, be patient for large projects
4. **Memory**: Monitor memory usage for very large projects

## Updates and Maintenance

### Updating the Server

```bash
# Pull latest changes
git pull

# Update dependencies
uv pip install -r requirements.txt

# Restart server
# Cursor IDE will automatically reconnect
```

### Backup Configuration

```bash
# Backup your configuration
cp cursor_mcp_config.json cursor_mcp_config.json.backup
cp neozork_mcp_config.json neozork_mcp_config.json.backup
```

## Support

For issues and questions:
1. Check this documentation
2. Run the status checker
3. Review server logs
4. Check Cursor IDE documentation
5. Open an issue in the project repository

---

**Note**: This MCP server is specifically designed for financial analysis projects and provides domain-specific assistance for trading, backtesting, and financial data analysis tasks. 