# MCP Server Usage Guide

## Overview

Neozork MCP Server is a unified Model Context Protocol server for financial analysis with IDE integration and intelligent environment detection.

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
# Check server status (works in both Docker and host environments)
python3 scripts/check_mcp_status.py

# Show running processes (host environment)
ps aux | grep neozork_mcp_server

# Test MCP server with ping (Docker environment)
echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py
```

## 📁 File Structure

```
📁 MCP Server Files:
├── neozork_mcp_server.py          # Main server
├── neozork_mcp_config.json        # Server configuration
├── start_mcp_server.py            # Start script
├── cursor_mcp_config.json         # Cursor configuration
├── pycharm_mcp_config.json        # PyCharm configuration
├── docker.env                     # Docker environment configuration
├── mcp.json                       # Universal configuration
├── scripts/
│   ├── setup_ide_configs.py       # IDE setup
│   ├── neozork_mcp_manager.py     # Server manager
│   └── check_mcp_status.py        # Status check with environment detection
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
    "ai_suggestions": true,
    "environment_detection": true
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

#### Docker Environment (`docker.env`)
```bash
PYTHONPATH=/app
PYTHONUNBUFFERED=1
DOCKER_CONTAINER=true
MCP_SERVER_ENABLED=true
LOG_LEVEL=INFO
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

## 🐳 Docker Environment

### Docker Usage

```bash
# Build and run Docker container
docker-compose build
docker-compose run --rm app bash

# Check MCP server status in Docker
python scripts/check_mcp_status.py

# Test MCP server with ping
echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py
```

### Docker Detection

The MCP server automatically detects Docker environments and uses ping-based detection:

- **Environment Detection**: Automatic Docker vs host detection
- **Ping-Based Detection**: Sends JSON-RPC ping requests for on-demand servers
- **Timeout Protection**: 10-second timeout for reliable detection
- **JSON Validation**: Validates proper JSON-RPC 2.0 responses

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

3. **Multiple processes (host environment)**
```bash
# Stop all processes
pkill -f neozork_mcp_server.py

# Check processes
ps aux | grep neozork_mcp_server
```

4. **Docker environment issues**
```bash
# Check if docker.env exists in container
docker-compose exec app ls -la /app/docker.env

# Test ping request
docker-compose exec app echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py

# Check Docker logs
docker logs <container_name>
```

### Status Check Issues

1. **Environment detection problems**
```bash
# Check Docker environment
ls -la /.dockerenv
cat /proc/1/cgroup | grep docker
echo $DOCKER_CONTAINER
```

2. **Ping request failures**
```bash
# Test ping manually
echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py

# Check for timeout
timeout 10 echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py
```

### Logs

- `logs/neozork_mcp_YYYYMMDD.log` - main server logs
- `logs/mcp_status_check.log` - status check logs (host environment)
- `logs/mcp_status_check_docker.log` - status check logs (Docker environment)
- `logs/ide_setup.log` - IDE setup logs

## 📊 Features

### Available Features

- **Financial Data Integration** - financial data integration
- **Technical Indicators** - technical indicators
- **Code Completion** - code completion
- **Project Analysis** - project analysis
- **AI Suggestions** - AI suggestions
- **GitHub Copilot** - Copilot integration
- **Environment Detection** - Automatic Docker vs host detection
- **Ping-Based Detection** - Reliable server detection in Docker

### MCP Commands

- `neozork/status` - server status
- `neozork/health` - health check
- `neozork/ping` - ping/pong test (used for detection)
- `neozork/metrics` - performance metrics

### Detection Methods

#### Docker Environment
- **Method**: Ping-based detection via JSON-RPC requests
- **Command**: `echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py`
- **Timeout**: 10 seconds
- **Validation**: JSON-RPC 2.0 response with `pong: true`

#### Host Environment
- **Method**: Process-based detection using `pgrep`
- **Command**: `pgrep -f neozork_mcp_server.py`
- **Features**: PID tracking, start/stop control
- **Monitoring**: Traditional process management

## 🔄 Migration Notes

### From Old Detection Logic

The old Docker detection logic used unreliable methods:
- PID file checking
- Process scanning via `/proc`
- `pgrep` and `pidof` commands

### To New Detection Logic

The new logic provides:
- ✅ Always accurate detection
- ✅ Works with on-demand servers
- ✅ Tests actual functionality
- ✅ No false positives/negatives
- ✅ Automatic environment detection

## 📚 Related Documentation

- **[MCP Server Detection Logic](docs/development/mcp-server-detection.md)** - Detailed detection implementation
- **[IDE Configuration](docs/guides/ide-configuration.md)** - Multi-IDE setup guide
- **[Docker Integration](docs/guides/mcp-server-docker-integration.md)** - Docker-specific guide
- **[MCP Servers Reference](docs/reference/mcp-servers/README.md)** - Complete server documentation 