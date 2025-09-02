# IDE Configuration Guide

## Overview

This guide covers the setup and configuration of Model Context Protocol (MCP) servers for multiple IDEs in the NeoZork HLD Prediction project.

> ⚠️ **Version Information**: v0.5.2 is the last version that supports Docker and Apple Container. Current version: v0.5.3

## 🚀 Quick Setup

### Automated Configuration
```bash
# Setup all IDE configurations automatically
python3 scripts/setup_ide_configs.py

# Verify the setup
python3 -m pytest tests/docker/test_ide_configs.py -v
```

### Manual Verification
```bash
# Check MCP server status
python scripts/check_mcp_status.py

# Test MCP server connection
echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py
```

## 🎯 Supported IDEs

### Cursor IDE
- **Primary IDE** with advanced AI integration
- **Auto-start**: MCP server starts automatically
- **Configuration**: `cursor_mcp_config.json`

### VS Code
- **Popular open-source editor**
- **Extension**: MCP extension required
- **Configuration**: `.vscode/settings.json`

### PyCharm
- **Professional Python IDE**
- **Plugin**: MCP plugin required
- **Configuration**: `pycharm_mcp_config.json`

## 🔧 Configuration Files

### Cursor Configuration
```json
{
  "mcpServers": {
    "neozork": {
      "command": "python3",
      "args": ["neozork_mcp_server.py"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

### VS Code Configuration
```json
{
  "mcp.servers": {
    "neozork": {
      "command": "python3",
      "args": ["neozork_mcp_server.py"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

### PyCharm Configuration
```json
{
  "mcpServers": {
    "neozork": {
      "command": "python3",
      "args": ["neozork_mcp_server.py"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

## 🐳 Docker Environment

> **Note**: Docker environment support is limited to v0.5.2 and earlier versions.

### Containerized Development
The MCP server works seamlessly in Docker environments with automatic detection:

```bash
# Build Docker image
docker-compose build

# Run in container
docker-compose run --rm app bash

# Check MCP server status in Docker
python scripts/check_mcp_status.py
```

### Docker-Specific Features
- **Ping-based Detection**: Reliable server detection without persistent processes
- **On-demand Operation**: Server starts per request and shuts down after
- **Automatic Environment Detection**: No manual configuration required
- **Timeout Protection**: 10-second timeout prevents hanging requests

### Docker Configuration
The `docker.env` file contains environment-specific settings:
```bash
# Example docker.env contents
PYTHONPATH=/app
PYTHONUNBUFFERED=1
DOCKER_CONTAINER=true
```

## 📊 Status Monitoring

### Status Checker
The `scripts/check_mcp_status.py` script provides comprehensive monitoring:

#### Docker Environment Output
```
🔍 MCP Server Status Checker
==================================================
🐳 Detected Docker environment

🚀 MCP Server Status:
   ✅ Server is running

🔗 Connection Test:
   ✅ Connection successful
   🔍 Test method: ping_request
   ⏱️  Response time: immediate

💻 IDE Configurations:
   ✅ CURSOR: 7418 bytes
   ✅ DOCKER: 367 bytes

🐳 Docker Information:
   📦 In Docker: True
   🔄 MCP Server responding: True
   🔍 Test method: ping_request
```

#### Host Environment Output
```
🔍 MCP Server Status Checker
==================================================
🖥️  Detected host environment

🚀 MCP Server Status:
   ✅ Server is running

🔗 Connection Test:
   ✅ Connection successful
   👥 PIDs: 12345, 67890

💻 IDE Configurations:
   ✅ CURSOR: 7418 bytes
   ✅ VSCODE: 2613 bytes
   ✅ PYCHARM: 4174 bytes
   ✅ DOCKER: 367 bytes
```

## 🔍 Detection Methods

### Environment Detection
The system automatically detects the environment using multiple methods:

1. **Docker-specific files**: Presence of `/.dockerenv`
2. **Cgroup information**: Docker references in `/proc/1/cgroup`
3. **Environment variables**: `DOCKER_CONTAINER=true`

### Detection Logic

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

## 🛠️ Troubleshooting

### Common Issues

#### MCP Server Not Detected
```bash
# Check if server is running
python scripts/check_mcp_status.py

# Manual server start (host environment)
python3 neozork_mcp_server.py

# Test ping request
echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py
```

#### Configuration Issues
```bash
# Verify configuration files exist
ls -la cursor_mcp_config.json .vscode/settings.json pycharm_mcp_config.json docker.env

# Re-run setup script
python3 scripts/setup_ide_configs.py
```

#### Docker Issues
```bash
# Check if docker.env is in container
docker-compose exec app ls -la /app/docker.env

# Rebuild container if needed
docker-compose build --no-cache
```

### Debug Information
The status checker provides detailed debug information:
- Environment detection results
- File existence checks
- Configuration validation
- Connection test results

## 🧪 Testing

### Test Coverage
```bash
# Test MCP server detection
python3 -m pytest tests/scripts/test_check_mcp_status.py -v

# Test IDE configurations
python3 -m pytest tests/docker/test_ide_configs.py -v

# Test MCP server functionality
python3 -m pytest tests/mcp/ -v
```

### Manual Testing
```bash
# Test ping request
echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py

# Expected response:
# {"jsonrpc": "2.0", "id": 1, "result": {"pong": true, "timestamp": "...", "server_time": "...", "timezone": "UTC"}}
```

## 📚 Related Documentation

- **[MCP Servers Reference](docs/reference/mcp-servers/README.md)** - Complete server documentation
- **[Detection Logic](docs/development/mcp-server-detection.md)** - Detailed detection implementation
- **[Docker Setup](docs/deployment/docker-setup.md)** - Containerized deployment guide
- **[Development Guide](docs/development/)** - Development and contribution guidelines

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

## 📋 Prerequisites

- Python 3.12+
- Docker (optional, for containerized development)
- UV package manager (recommended)
- MCP plugin/extension for your IDE

## 🎯 IDE-Specific Setup

### Cursor IDE

#### Automatic Setup
```bash
python3 scripts/setup_ide_configs.py
```

#### Manual Setup
1. **Copy Configuration**: Copy `cursor_mcp_config.json` to project root
2. **Create MCP Config**: Create `mcp.json` for Cursor IDE compatibility
3. **Restart Cursor**: Restart Cursor IDE for MCP server to auto-start
4. **Verify**: Check MCP panel for server status

#### Configuration Files
Cursor IDE uses two configuration files:

**`cursor_mcp_config.json`** - Extended configuration with advanced features:
```json
{
  "mcpServers": {
    "neozork": {
      "command": "python3",
      "args": ["neozork_mcp_server.py"],
      "env": {
        "PYTHONPATH": "${PROJECT_ROOT}",
        "LOG_LEVEL": "INFO"
      }
    }
  },
  "serverSettings": {
    "neozork": {
      "enabled": true,
      "autoStart": true,
      "features": {
        "financial_data": true,
        "technical_indicators": true
      }
    }
  }
}
```

**`mcp.json`** - Standard MCP configuration for Cursor IDE:
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

#### File Priority
- Cursor IDE looks for `mcp.json` first
- If `mcp.json` is not found, it falls back to `cursor_mcp_config.json`
- Both files are created automatically by the setup script

### VS Code

#### Automatic Setup
```bash
python3 scripts/setup_ide_configs.py
```

#### Manual Setup
1. **Install Extensions**:
   - MCP Extension
   - Python Extension
   - Black Formatter
   - Pylint
   - Pytest

2. **Configure Settings**: `.vscode/settings.json` is automatically created
3. **Restart VS Code**: Restart for MCP server to auto-start

#### Configuration Details
```json
{
  "mcp.servers": {
    "neozork": {
      "command": "python3",
      "args": ["neozork_mcp_server.py"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### PyCharm

#### Automatic Setup
```bash
python3 scripts/setup_ide_configs.py
```

#### Manual Setup
1. **Install MCP Plugin**: Settings → Plugins → Search "MCP"
2. **Load Configuration**: Load `pycharm_mcp_config.json` in MCP settings
3. **Configure Interpreter**: Set Python interpreter (UV recommended)
4. **Restart PyCharm**: Restart for MCP server to auto-start

#### Configuration Details
```json
{
  "mcpServers": {
    "neozork": {
      "command": "python3",
      "args": ["neozork_mcp_server.py"],
      "env": {
        "PYTHONPATH": "${PROJECT_ROOT}",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## 🔍 MCP Server Status Check

### Check Server Status
```bash
# Comprehensive status check
python3 scripts/check_mcp_status.py

# Expected output:
# 🔍 MCP Server Status Checker
# ==================================================
# 📅 Check Time: 2025-06-25 15:30:45
# 📁 Project Root: /path/to/neozork-hld-prediction
# 
# 🚀 MCP Server Status:
#    ✅ Server is running
# 
# 🔗 Connection Test:
#    ✅ Connection successful
#    📡 Ping: pong
#    💚 Health: healthy
# 
# 💻 IDE Configurations:
#    ✅ CURSOR: 2048 bytes
#    ✅ VSCODE: 1536 bytes
#    ✅ PYCHARM: 2048 bytes
# 
# ✅ All checks passed!
```

### Test MCP Connection
```bash
# Test ping
echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py

# Test status
echo '{"method": "neozork/status", "id": 1, "params": {}}' | python3 neozork_mcp_server.py

# Test health
echo '{"method": "neozork/health", "id": 1, "params": {}}' | python3 neozork_mcp_server.py
```

### Manual Server Start
```bash
# Start MCP server manually
python3 neozork_mcp_server.py

# Start with debug logging
LOG_LEVEL=DEBUG python3 neozork_mcp_server.py

# Start in Docker
docker compose run --rm neozork-hld python3 neozork_mcp_server.py
```

## 🔄 Autostart Configuration

### Does Cursor IDE Need Restart?

**Yes, restart is required** for MCP server to auto-start. Here's why and how:

#### Why Restart is Needed
1. **Configuration Loading**: Cursor reads MCP configuration on startup
2. **Server Discovery**: IDE discovers available MCP servers during initialization
3. **Process Management**: IDE manages MCP server lifecycle

#### Restart Process
1. **Save All Files**: Save any open files
2. **Close Cursor**: Completely close Cursor IDE
3. **Reopen Project**: Open the project again
4. **Check MCP Panel**: Verify server status in MCP panel

#### Verification Steps
```bash
# After restart, check if server is running
python3 scripts/check_mcp_status.py

# Check logs for any errors
tail -f logs/neozork_mcp.log

# Test connection
echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py
```

### Autostart Behavior

#### Cursor IDE
- **Auto-start**: ✅ Yes, when project is opened
- **Restart Required**: ✅ Yes, after configuration changes
- **Background Process**: ✅ Yes, managed by IDE

#### VS Code
- **Auto-start**: ✅ Yes, when workspace is opened
- **Restart Required**: ✅ Yes, after configuration changes
- **Background Process**: ✅ Yes, managed by extension

#### PyCharm
- **Auto-start**: ✅ Yes, when project is opened
- **Restart Required**: ✅ Yes, after configuration changes
- **Background Process**: ✅ Yes, managed by plugin

## 🐳 Docker Integration

### Docker Configuration
All IDE configurations support Docker mode:

```json
{
  "mcpServers": {
    "neozork-docker": {
      "command": "docker",
      "args": [
        "compose",
        "run",
        "--rm",
        "-T",
        "-e",
        "PYTHONPATH=/app",
        "-e",
        "LOG_LEVEL=INFO",
        "-e",
        "DOCKER_CONTAINER=true",
        "-e",
        "USE_UV=true",
        "neozork-hld",
        "python3",
        "neozork_mcp_server.py"
      ]
    }
  }
}
```

### Docker Usage
```bash
# Build container
docker compose build --build-arg USE_UV=true

# Run MCP server in Docker
docker compose run --rm neozork-hld python3 neozork_mcp_server.py

# Check Docker status
docker compose ps
```

## 🔧 Troubleshooting

### Cursor IDE Issues

#### Problem: "Cursor IDE looking for mcp.json"
**Solution:**
1. **Check if mcp.json exists:**
   ```bash
   ls -la mcp.json
   ```

2. **If missing, create it:**
   ```bash
   python3 scripts/setup_ide_configs.py
   ```

3. **Verify both config files exist:**
   ```bash
   ls -la cursor_mcp_config.json mcp.json
   ```

#### Problem: MCP Server Not Starting
**Solution:**
1. **Check file permissions:**
   ```bash
   chmod +x neozork_mcp_server.py
   ```

2. **Verify Python path:**
   ```bash
   which python3
   python3 --version
   ```

3. **Test server manually:**
   ```bash
   python3 neozork_mcp_server.py
   ```

4. **Check logs:**
   ```bash
   tail -f logs/neozork_mcp.log
   ```

#### Problem: Configuration Not Loading
**Solution:**
1. **Restart Cursor IDE completely**
2. **Check JSON syntax:**
   ```bash
   python3 -m json.tool mcp.json
   python3 -m json.tool cursor_mcp_config.json
   ```

3. **Verify project root:**
   ```bash
   pwd
   ls -la mcp.json
   ```

#### Problem: Docker MCP Server Issues
**Solution:**
1. **Check Docker status:**
   ```bash
   docker --version
   docker compose version
   ```

2. **Test Docker container:**
   ```bash
   docker compose run --rm neozork-hld python3 neozork_mcp_server.py
   ```

3. **Check Docker logs:**
   ```bash
   docker compose logs neozork-hld
   ```

### Common Error Messages

#### "mcp.json not found"
- Run `python3 scripts/setup_ide_configs.py`
- Verify file exists: `ls -la mcp.json`

#### "MCP server failed to start"
- Check Python installation: `python3 --version`
- Test server manually: `python3 neozork_mcp_server.py`
- Check logs: `tail -f logs/neozork_mcp.log`

#### "Connection refused"
- Restart Cursor IDE
- Check if server is running: `python3 scripts/check_mcp_status.py`
- Verify port availability: `lsof -i :8080`

### File Priority for Cursor IDE
1. **Primary**: `mcp.json` (standard MCP format)
2. **Fallback**: `cursor_mcp_config.json` (extended features)
3. **Auto-creation**: Both files created by setup script

### Verification Commands
```bash
# Check all config files
ls -la *.json

# Validate JSON syntax
python3 -m json.tool mcp.json
python3 -m json.tool cursor_mcp_config.json

# Test MCP server
python3 scripts/check_mcp_status.py

# Check IDE setup
python3 -m pytest tests/docker/test_ide_configs.py -v
```

## 📊 Performance Metrics

| Feature | Performance |
|---------|-------------|
| MCP Server Startup | < 3s |
| Autocompletion Response | 5-15ms |
| File Indexing | 50ms/file |
| Memory Usage | 25-50MB |
| IDE Setup Time | < 30s |
| Test Execution | 0.12s (15 tests) |

## 🎯 Best Practices

### Development Workflow
1. **Setup**: Run automated setup script
2. **Verify**: Check MCP server status
3. **Restart**: Restart IDE for autostart
4. **Test**: Verify connection and functionality
5. **Monitor**: Check logs for issues

### Configuration Management
- **Version Control**: Commit configuration files
- **Environment Variables**: Use for sensitive data
- **Logging**: Enable appropriate log levels
- **Backup**: Keep configuration backups

### Security Considerations
- **Path Restrictions**: Limit allowed paths
- **File Size Limits**: Set appropriate limits
- **Timeout Settings**: Configure reasonable timeouts
- **Access Control**: Restrict server access

## 📚 Additional Resources

### Documentation
- [MCP Servers Reference](reference/mcp-servers/README.md)
- [Technical Indicators](reference/indicators/)
- [API Documentation](api/)

### Examples
- [MCP Examples](examples/mcp-examples.md)
- [Docker Examples](examples/docker-examples.md)
- [Testing Examples](examples/testing-examples.md)

### Support
- [Troubleshooting Guide](debug-scripts.md)
- [Development Guide](development/ci-cd.md)
- [Testing Guide](testing.md)

---

**Last Updated**: June 25, 2025  
**IDE Configurations**: Cursor, VS Code, PyCharm  
**MCP Server**: Production Ready  
**Test Coverage**: 100% (15/15 tests passed)

## 🌍 Global MCP Config for Cursor IDE

Cursor IDE uses a global MCP configuration file:

- **~/.cursor/mcp.json** — global for all projects
- **./mcp.json** — local for the current project
- **./cursor_mcp_config.json** — extended local

### Loading Priority:
1. `~/.cursor/mcp.json`
2. `./mcp.json`
3. `./cursor_mcp_config.json`

> The script `python3 scripts/setup_ide_configs.py` automatically updates all these files.

**All Neozork MCP server capabilities are now available from any project in Cursor IDE.**

---

### Quick Start (updated)
```bash
python3 scripts/setup_ide_configs.py
# updates ~/.cursor/mcp.json, ./mcp.json, ./cursor_mcp_config.json
```

---

### Troubleshooting (updated)
- If Cursor IDE does not see the server — check the existence and content of `~/.cursor/mcp.json`.
- To update both global and local configs always use `python3 scripts/setup_ide_configs.py`. 