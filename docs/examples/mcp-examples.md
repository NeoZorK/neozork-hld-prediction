# MCP Server Examples

Examples for using MCP (Model Context Protocol) servers with the project.

## Overview

The project includes MCP server integration for enhanced development experience:

- **Auto-start MCP Server** - Automatically manages MCP servers
- **PyCharm GitHub Copilot MCP Server** - Integration with GitHub Copilot
- **Manual MCP Server Control** - Direct server management
- **Testing and Debugging** - MCP server validation

## Auto-start MCP Server

### Basic Usage
```bash
# Start MCP servers
python scripts/auto_start_mcp.py

# Start with configuration file
python scripts/auto_start_mcp.py --config mcp_auto_config.json

# Start in debug mode
python scripts/auto_start_mcp.py --debug

# Show server status
python scripts/auto_start_mcp.py --status

# Stop all servers
python scripts/auto_start_mcp.py --stop
```

### Configuration Options
```bash
# Start with custom project path
python scripts/auto_start_mcp.py --project-path /path/to/project

# Start with specific configuration
python scripts/auto_start_mcp.py --config custom_config.json

# Start with verbose output
python scripts/auto_start_mcp.py --verbose
```

### Server Management
```bash
# Check if servers are running
python scripts/auto_start_mcp.py --status

# Restart servers
python scripts/auto_start_mcp.py --restart

# Kill all MCP processes
python scripts/auto_start_mcp.py --kill-all

# Show server logs
python scripts/auto_start_mcp.py --logs
```

## PyCharm GitHub Copilot MCP Server

### Basic Usage
```bash
# Start PyCharm GitHub Copilot MCP server
python pycharm_github_copilot_mcp.py

# Start with stdio mode for testing
python pycharm_github_copilot_mcp.py --stdio

# Start with debug logging
python pycharm_github_copilot_mcp.py --debug

# Start with specific configuration
python pycharm_github_copilot_mcp.py --config mcp_auto_config.json
```

### Advanced Options
```bash
# Start with custom port
python pycharm_github_copilot_mcp.py --port 8080

# Start with custom host
python pycharm_github_copilot_mcp.py --host 127.0.0.1

# Start with environment variables
export MCP_DEBUG=1
python pycharm_github_copilot_mcp.py
```

## Manual MCP Server Control

### Direct Server Management
```bash
# Start server directly
python pycharm_github_copilot_mcp.py --stdio

# Start with specific configuration
python pycharm_github_copilot_mcp.py --config mcp_auto_config.json

# Start in background
nohup python pycharm_github_copilot_mcp.py > mcp.log 2>&1 &

# Check if server is running
ps aux | grep pycharm_github_copilot_mcp
```

### Server Configuration
```bash
# Create custom configuration
cat > custom_mcp_config.json << EOF
{
  "mcpServers": {
    "pycharm-github-copilot": {
      "command": "python",
      "args": ["pycharm_github_copilot_mcp.py"],
      "env": {
        "MCP_DEBUG": "1"
      }
    }
  }
}
EOF

# Use custom configuration
python scripts/auto_start_mcp.py --config custom_mcp_config.json
```

## Testing MCP Servers

### Basic Testing
```bash
# Test stdio mode
python tests/test_stdio.py

# Test MCP functionality
python -m pytest tests/mcp/ -v

# Test auto-start functionality
python -m pytest tests/mcp/test_auto_start_mcp.py -v

# Test PyCharm MCP server
python -m pytest tests/mcp/test_pycharm_github_copilot_mcp.py -v
```

### Integration Testing
```bash
# Test MCP server integration
python scripts/run_cursor_mcp.py --test

# Test with coverage
python -m pytest tests/mcp/ --cov=src.mcp --cov-report=html

# Test specific MCP features
python -m pytest tests/mcp/ -k "test_connection" -v
```

### Debug Testing
```bash
# Run tests with debug output
python -m pytest tests/mcp/ -s -v

# Run specific test with debugger
python -m pytest tests/mcp/test_auto_start_mcp.py::test_start_server -s --pdb

# Run tests and show print statements
python -m pytest tests/mcp/ -s
```

## Debugging MCP Servers

### Debug Scripts
```bash
# Debug MCP servers
python scripts/debug_scripts/debug_mcp_servers.py

# Check MCP server status
python scripts/debug_scripts/debug_mcp_status.py

# Debug MCP connections
python scripts/debug_scripts/debug_mcp_connections.py
```

### Common Issues
```bash
# Check if ports are available
netstat -tulpn | grep :8080

# Check MCP server logs
tail -f mcp.log

# Check system resources
top -p $(pgrep -f pycharm_github_copilot_mcp)

# Kill stuck MCP processes
pkill -f pycharm_github_copilot_mcp
```

## Cursor Editor Integration

### Cursor Configuration
```json
{
  "mcpServers": {
    "pycharm-github-copilot": {
      "command": "python",
      "args": ["pycharm_github_copilot_mcp.py"],
      "env": {
        "MCP_DEBUG": "1"
      }
    }
  }
}
```

### Cursor MCP Setup
```bash
# Create Cursor MCP configuration
mkdir -p ~/.cursor/mcp
cp mcp_auto_config.json ~/.cursor/mcp/config.json

# Restart Cursor to load MCP configuration
# Then start MCP servers
python scripts/auto_start_mcp.py
```

## Workflow Examples

### Development Workflow
```bash
# 1. Start MCP servers
python scripts/auto_start_mcp.py

# 2. Check server status
python scripts/auto_start_mcp.py --status

# 3. Run tests
python -m pytest tests/mcp/ -v

# 4. Debug if needed
python scripts/debug_scripts/debug_mcp_servers.py

# 5. Stop servers when done
python scripts/auto_start_mcp.py --stop
```

### Testing Workflow
```bash
# 1. Start servers for testing
python scripts/auto_start_mcp.py --debug

# 2. Run MCP tests
python -m pytest tests/mcp/ -v

# 3. Test stdio mode
python tests/test_stdio.py

# 4. Check test coverage
python -m pytest tests/mcp/ --cov=src.mcp --cov-report=html

# 5. Stop servers
python scripts/auto_start_mcp.py --stop
```

### Debugging Workflow
```bash
# 1. Check server status
python scripts/auto_start_mcp.py --status

# 2. Debug servers
python scripts/debug_scripts/debug_mcp_servers.py

# 3. Check logs
tail -f mcp.log

# 4. Restart if needed
python scripts/auto_start_mcp.py --restart

# 5. Test connection
python tests/test_stdio.py
```

## Performance Optimization

### Server Optimization
```bash
# Start with optimized settings
python scripts/auto_start_mcp.py --config optimized_config.json

# Monitor server performance
python scripts/debug_scripts/debug_mcp_performance.py

# Optimize memory usage
python scripts/auto_start_mcp.py --memory-optimized
```

### Resource Management
```bash
# Check memory usage
ps aux | grep pycharm_github_copilot_mcp | awk '{print $6}'

# Monitor CPU usage
top -p $(pgrep -f pycharm_github_copilot_mcp)

# Check disk usage
du -sh logs/mcp/
```

## Troubleshooting

### Common Issues
```bash
# Issue: Server not starting
python scripts/auto_start_mcp.py --debug
python scripts/debug_scripts/debug_mcp_servers.py

# Issue: Connection refused
netstat -tulpn | grep :8080
python scripts/auto_start_mcp.py --restart

# Issue: Permission denied
chmod +x scripts/auto_start_mcp.py
chmod +x pycharm_github_copilot_mcp.py

# Issue: Port already in use
lsof -i :8080
kill -9 $(lsof -t -i:8080)
```

### Debug Mode
```bash
# Enable debug logging
export MCP_DEBUG=1
python scripts/auto_start_mcp.py

# Run with verbose output
python scripts/auto_start_mcp.py --verbose

# Check debug logs
tail -f logs/mcp_debug.log
```

### System Issues
```bash
# Check system resources
python scripts/debug_scripts/debug_system_resources.py

# Check Python environment
python -c "import sys; print(sys.version)"
python -c "import mcp; print(mcp.__version__)"

# Check dependencies
pip list | grep mcp
```

## Advanced Usage

### Custom MCP Server
```python
# Example: Creating a custom MCP server
import mcp

class CustomMCPServer(mcp.Server):
    def __init__(self):
        super().__init__()
        
    def handle_request(self, request):
        # Custom request handling
        pass

# Usage
server = CustomMCPServer()
server.start()
```

### MCP Server Configuration
```json
{
  "mcpServers": {
    "custom-server": {
      "command": "python",
      "args": ["custom_mcp_server.py"],
      "env": {
        "CUSTOM_VAR": "value"
      },
      "cwd": "/path/to/project"
    }
  }
}
```

### Integration with Other Tools
```bash
# Integration with VS Code
code --install-extension mcp.vscode-mcp

# Integration with PyCharm
# Configure MCP server in PyCharm settings

# Integration with Jupyter
jupyter lab --MCP.enabled=true
```

---

📚 **Additional Resources:**
- **[Usage Examples](usage-examples.md)** - Comprehensive usage examples
- **[Quick Examples](quick-examples.md)** - Fast start examples
- **[Indicator Examples](indicator-examples.md)** - Technical indicator examples
- **[Testing Examples](testing-examples.md)** - Testing examples
- **[Script Examples](script-examples.md)** - Utility script examples
- **[Docker Examples](docker-examples.md)** - Docker examples
- **[EDA Examples](eda-examples.md)** - EDA examples 