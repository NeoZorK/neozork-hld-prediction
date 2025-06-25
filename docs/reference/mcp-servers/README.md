# Neozork MCP Servers

## Overview

The Neozork project includes a unified, modern Model Context Protocol (MCP) server that provides intelligent code completion, financial data integration, and AI-powered suggestions for financial analysis projects.

## Unified MCP Server

### Features

- **Unified Architecture**: Single server supporting all IDEs (Cursor, PyCharm, VS Code)
- **Financial Data Integration**: Automatic scanning and indexing of financial data
- **Technical Indicators**: Complete library of technical analysis indicators
- **AI-Powered Suggestions**: Context-aware code suggestions and GitHub Copilot integration
- **Project Analysis**: Intelligent project structure analysis and recommendations
- **Docker Integration**: Full Docker support with containerized deployment
- **Real-time Monitoring**: Health monitoring and performance optimization

### Quick Start

#### 1. Automatic Start (Recommended)

The MCP server starts automatically when you open the project in a supported IDE:

```bash
# The server will auto-start when you open Cursor, PyCharm, or VS Code
# No manual intervention required
```

#### 2. Manual Start

```bash
# Start the unified MCP server
python neozork_mcp_server.py

# Start with custom configuration
python neozork_mcp_server.py --config custom_config.json

# Start in debug mode
python neozork_mcp_server.py --debug
```

#### 3. Using the MCP Manager

```bash
# Start auto-start mode
python scripts/neozork_mcp_manager.py start

# Check server status
python scripts/neozork_mcp_manager.py status

# Manually start server
python scripts/neozork_mcp_manager.py start-server

# Stop all servers
python scripts/neozork_mcp_manager.py stop

# Create IDE configuration
python scripts/neozork_mcp_manager.py create-config cursor
```

### Configuration

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
  }
}
```

### IDE Integration

#### Cursor IDE

1. **Automatic**: Server starts automatically when Cursor detects the project
2. **Manual**: Create configuration in `.cursor/settings.json`

```json
{
  "mcpServers": {
    "neozork-mcp": {
      "command": "python",
      "args": ["neozork_mcp_server.py"],
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src:${workspaceFolder}",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

#### PyCharm IDE

1. **Automatic**: Server starts automatically when PyCharm detects the project
2. **Manual**: Create configuration in `.idea/mcp_servers.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="MCPProjectSettings">
    <option name="mcpServers">
      <map>
        <entry key="neozork-mcp">
          <value>
            <MCPProjectSettings.MCPServer>
              <option name="command" value="python" />
              <option name="args" value="neozork_mcp_server.py" />
              <option name="cwd" value="$PROJECT_DIR$" />
              <option name="env">
                <map>
                  <entry key="PYTHONPATH" value="$PROJECT_DIR$/src:$PROJECT_DIR$" />
                  <entry key="LOG_LEVEL" value="INFO" />
                </map>
              </option>
            </MCPProjectSettings.MCPServer>
          </value>
        </entry>
      </map>
    </option>
  </component>
</project>
```

#### VS Code

1. **Automatic**: Server starts automatically when VS Code detects the project
2. **Manual**: Create configuration in `.vscode/settings.json`

```json
{
  "mcp.servers": {
    "neozork-mcp": {
      "command": "python",
      "args": ["neozork_mcp_server.py"],
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src:${workspaceFolder}",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Features

#### Code Completion

- **Project Functions**: Auto-completion for all project functions
- **Classes**: Class definitions and methods
- **Financial Symbols**: Available trading symbols (GBPUSD, EURUSD, etc.)
- **Timeframes**: Trading timeframes (MN1, H1, M15, etc.)
- **Technical Indicators**: Complete library of indicators
- **Code Snippets**: Pre-built code templates

#### Financial Data Integration

- **Automatic Scanning**: Scans `data/`, `mql5_feed/` directories
- **Multiple Formats**: Supports CSV, Parquet, JSON
- **Symbol Detection**: Automatically detects trading symbols
- **Timeframe Detection**: Identifies trading timeframes
- **Sample Data**: Provides sample data for analysis

#### Technical Indicators

- **Trend Indicators**: SMA, EMA, ADX, SAR, HMA
- **Oscillators**: RSI, Stochastic, CCI
- **Momentum**: MACD, Stochastic Oscillator
- **Volatility**: ATR, Bollinger Bands, Standard Deviation
- **Volume**: OBV, VWAP
- **Support/Resistance**: Donchian Channels, Fibonacci, Pivot Points
- **Predictive**: Time Series Forecast
- **Probability**: Kelly Criterion, Monte Carlo
- **Sentiment**: COT, Fear & Greed, Social Sentiment

#### AI Suggestions

- **Context-Aware**: Suggestions based on current code context
- **Financial Patterns**: Trading strategy suggestions
- **Code Quality**: Best practices and optimization tips
- **Performance**: Performance optimization suggestions
- **GitHub Copilot**: Integration with GitHub Copilot

### Docker Support

The MCP server works seamlessly in Docker environments:

```dockerfile
# Dockerfile example
FROM python:3.11-slim

WORKDIR /workspace
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "neozork_mcp_server.py"]
```

```yaml
# docker-compose.yml example
version: '3.8'
services:
  neozork-mcp:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - .:/workspace
      - ./logs:/workspace/logs
    environment:
      - PYTHONPATH=/workspace/src:/workspace
      - LOG_LEVEL=INFO
```

### Monitoring and Health

#### Health Checks

```bash
# Check server status
python scripts/neozork_mcp_manager.py status

# Monitor server health
python scripts/neozork_mcp_manager.py start --monitor
```

#### Logs

Logs are stored in `logs/` directory:

- `neozork_mcp_YYYYMMDD.log` - Main server logs
- `neozork_mcp_manager_YYYYMMDD.log` - Manager logs
- `neozork_mcp_state.json` - Server state information

#### Performance Metrics

- **Memory Usage**: Configurable limits (default: 512MB)
- **CPU Usage**: Performance monitoring
- **Response Time**: Completion response time tracking
- **File Indexing**: Project file scanning performance

### Testing

Run comprehensive tests:

```bash
# Run all MCP tests
python -m pytest tests/mcp/ -v

# Run specific test categories
python -m pytest tests/mcp/test_neozork_mcp_server.py -v
python -m pytest tests/mcp/test_neozork_mcp_manager.py -v

# Run with coverage
python -m pytest tests/mcp/ --cov=neozork_mcp_server --cov-report=html
```

### Troubleshooting

#### Common Issues

1. **Server not starting**
   - Check Python path configuration
   - Verify dependencies are installed
   - Check log files for errors

2. **No completions**
   - Ensure project files are scanned
   - Check financial data directories exist
   - Verify IDE configuration

3. **Performance issues**
   - Reduce file scanning scope
   - Adjust memory limits
   - Enable caching

#### Debug Mode

```bash
# Enable debug logging
python neozork_mcp_server.py --debug

# Check detailed status
python scripts/neozork_mcp_manager.py status
```

### Development

#### Adding New Features

1. **New Indicators**: Add to `technical_indicators` section in config
2. **New Snippets**: Add to `code_snippets` section in config
3. **New Handlers**: Implement new MCP protocol handlers
4. **New Integrations**: Add IDE-specific configurations

#### Contributing

1. Follow the project's coding standards
2. Add comprehensive tests for new features
3. Update documentation
4. Ensure Docker compatibility

### Migration from Legacy Servers

If you're migrating from the old PyCharm or Cursor-specific servers:

1. **Backup**: Backup your existing configurations
2. **Install**: The unified server replaces all previous servers
3. **Configure**: Update IDE configurations if needed
4. **Test**: Verify all features work correctly
5. **Remove**: Remove old server files

### Support

For issues and questions:

1. Check the troubleshooting section
2. Review log files in `logs/` directory
3. Run tests to verify functionality
4. Check the project documentation

## Legacy Servers (Deprecated)

> **Note**: The following servers are deprecated in favor of the unified server.

### PyCharm GitHub Copilot MCP Server

The PyCharm-specific server has been replaced by the unified server.

### Cursor MCP Server

The Cursor-specific server has been replaced by the unified server.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   IDE Client    │    │  Unified MCP     │    │   Project       │
│  (Cursor/PyCharm│◄──►│     Server       │◄──►│   Files & Data  │
│   /VS Code)     │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   MCP Manager    │
                       │  (Auto-start &   │
                       │   Monitoring)    │
                       └──────────────────┘
```

## Performance

- **Startup Time**: < 5 seconds
- **Memory Usage**: < 512MB
- **Completion Response**: < 1 second
- **File Indexing**: < 10 seconds for 10,000 files
- **Docker Overhead**: < 5% performance impact

## Security

- **Path Validation**: All file paths are validated
- **Input Sanitization**: All inputs are sanitized
- **Resource Limits**: Configurable memory and CPU limits
- **Timeout Protection**: Request timeout protection
- **Access Control**: Project-scoped access only 