# MCP Server Guide

Model Completion Protocol (MCP) server for enhanced GitHub Copilot capabilities in development environments.

## Overview

The MCP server extends GitHub Copilot with project-specific context, providing more accurate code completions and suggestions tailored to the NeoZork HLD Prediction codebase.

## Features

- **Enhanced Context Awareness:** Full access to project structure and codebase
- **Improved Completions:** Project-specific code suggestions
- **Offline Capability:** Works in environments with limited internet connectivity
- **Docker Integration:** Seamless container support
- **STDIO Communication:** Standard input/output protocol
- **Detailed Logging:** Session logs for debugging

## Quick Setup

### 1. Automatic Setup (Recommended)
The MCP server is automatically configured when using Docker:
```bash
docker compose up
# When prompted: "Would you like to start the MCP service? [y/N]:"
# Enter "y" to activate
```

### 2. Manual Setup
For local development without Docker:
```bash
# Ensure logs directory exists
mkdir -p logs

# Make server executable
chmod +x mcp_server.py

# Run the server (usually started by IDE)
python mcp_server.py
```

## IDE Integration

### PyCharm CE Configuration

1. **Install GitHub Copilot Plugin:**
   - Go to Settings → Plugins
   - Search for "GitHub Copilot"
   - Install and restart PyCharm

2. **Configure MCP:**
   - Go to Settings → Tools → GitHub Copilot
   - Find "Advanced" → "MCP Configuration"
   - Add path to `mcp.json` file

3. **MCP Configuration File (`mcp.json`):**
```json
{
  "command": "python",
  "args": ["/absolute/path/to/mcp_server.py"],
  "stdio": true
}
```

Replace `/absolute/path/to/mcp_server.py` with the actual path to the server file.

### VS Code Configuration

1. **Install GitHub Copilot Extension**
2. **Configure MCP in settings.json:**
```json
{
  "github.copilot.advanced.mcp": {
    "command": "python",
    "args": ["/absolute/path/to/mcp_server.py"],
    "stdio": true
  }
}
```

## Usage Modes

### Local MCP Server
Run directly on host machine for lowest latency:
```bash
python mcp_server.py
```

**Benefits:**
- Fastest response times
- Direct file system access
- No container overhead

### Docker-based MCP Server
Run inside container for consistency:
```bash
docker compose up
# MCP server starts automatically
```

**Benefits:**
- Consistent environment
- Isolated dependencies
- Easy deployment

### Hybrid Setup
Local IDE with containerized development:
- IDE and MCP server on host
- Development environment in Docker
- Best of both worlds

## Server Capabilities

### Project Analysis
- **Code Structure:** Understanding of project architecture
- **Dependencies:** Knowledge of installed packages and imports
- **File Relationships:** Awareness of module connections
- **Pattern Recognition:** Project-specific coding patterns

### Enhanced Suggestions
- **Context-Aware Completions:** Suggestions based on project context
- **Import Optimization:** Smart import suggestions
- **Function Signatures:** Accurate parameter suggestions
- **Error Prevention:** Pattern-based error detection

## Configuration

### Environment Variables
```env
# MCP Server settings
MCP_LOG_LEVEL=INFO
MCP_LOG_FILE=logs/mcp_server.log
MCP_DEBUG=false
```

### Logging Configuration
The server creates detailed logs in `logs/mcp_server.log`:
- Request/response pairs
- Processing times
- Error diagnostics
- Session information

### Performance Tuning
```bash
# Adjust server responsiveness
export MCP_TIMEOUT=30
export MCP_MAX_REQUESTS=100
```

## Monitoring and Debugging

### Log Analysis
```bash
# View recent MCP activity
tail -f logs/mcp_server.log

# Search for specific patterns
grep "ERROR" logs/mcp_server.log
grep "completion" logs/mcp_server.log
```

### Health Checks
```bash
# Check if server is running
ps aux | grep mcp_server

# Test server responsiveness
echo '{"test": "ping"}' | python mcp_server.py
```

### Performance Metrics
Monitor server performance:
- Response time per request
- Memory usage
- Request success rate

## Troubleshooting

### Common Issues

**Server won't start:**
```bash
# Check Python version
python --version

# Verify file permissions
ls -la mcp_server.py

# Check logs directory
mkdir -p logs
```

**IDE not recognizing MCP:**
```bash
# Verify configuration path
cat mcp.json

# Test server manually
python mcp_server.py --test
```

**Slow responses:**
```bash
# Check system resources
top | grep python

# Reduce request timeout
export MCP_TIMEOUT=10
```

### Debug Mode
Enable debug logging:
```bash
export MCP_DEBUG=true
python mcp_server.py
```

## Best Practices

### Performance
1. **Use local server** for development when possible
2. **Monitor memory usage** with large codebases
3. **Restart server** periodically for optimal performance

### Security
1. **Protect API keys** in .env files
2. **Use isolated environments** for sensitive projects
3. **Review logs** for unexpected activity

### Development
1. **Keep server updated** with project changes
2. **Use meaningful commit messages** for better context
3. **Document code patterns** for better AI understanding

## Advanced Configuration

### Custom Handlers
Extend server capabilities:
```python
# Add custom completion logic
def custom_completion_handler(request):
    # Project-specific logic
    return enhanced_suggestions
```

### Integration Testing
```bash
# Test MCP integration
python tests/mcp/test_mcp_server.py

# Validate configuration
python scripts/validate_mcp_config.py
```

### Deployment
For production environments:
```bash
# Run as service
systemctl enable mcp-server
systemctl start mcp-server

# Container deployment
docker compose -f docker-compose.prod.yml up -d
```
