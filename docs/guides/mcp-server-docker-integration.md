# MCP Server Docker Integration

## Overview

The MCP (Model Context Protocol) server status checker has been enhanced to support both Docker and non-Docker environments with intelligent detection methods. The system automatically adapts to different environments and provides reliable status monitoring.

## Features

### Automatic Environment Detection

The script automatically detects whether it's running inside a Docker container or on the host system:

- **Docker Detection Methods:**
  - Checks for `/.dockerenv` file
  - Examines `/proc/1/cgroup` for Docker references
  - Looks for `DOCKER_CONTAINER=true` environment variable

### Environment-Specific Logic

#### Docker Environment (`DockerMCPServerChecker`)

- **Ping-Based Detection:** Sends JSON-RPC ping requests to test server functionality
- **On-Demand Servers:** Works with servers that start/stop per request
- **Timeout Protection:** 10-second timeout for reliable detection
- **JSON Validation:** Validates proper JSON-RPC 2.0 responses
- **Docker-Specific Configs:** Monitors Docker environment variables and configurations

#### Host Environment (`MCPServerChecker`)

- **Process Discovery:** Uses `pgrep` to find MCP server processes
- **Process Management:** Can start/stop MCP server processes
- **PID Tracking:** Monitors multiple server instances
- **IDE Configurations:** Checks all IDE configuration files (Cursor, VS Code, PyCharm)

## Usage

### Basic Usage

```bash
# Run the status checker (automatically detects environment)
python scripts/check_mcp_status.py
```

### Environment Detection

```python
from scripts.check_mcp_status import is_running_in_docker

# Check if running in Docker
if is_running_in_docker():
    print("Running in Docker container")
else:
    print("Running on host system")
```

### Docker-Specific Usage

```python
from scripts.check_mcp_status import DockerMCPServerChecker

# Create Docker-specific checker
checker = DockerMCPServerChecker()

# Run comprehensive check
results = checker.run_comprehensive_check()
print(f"Server running: {results['server_running']}")
print(f"Environment: {results['environment']}")
```

### Host-Specific Usage

```python
from scripts.check_mcp_status import MCPServerChecker

# Create host-specific checker
checker = MCPServerChecker()

# Run comprehensive check
results = checker.run_comprehensive_check()
print(f"Server running: {results['server_running']}")
print(f"Environment: {results['environment']}")
```

## Docker Integration Details

### Ping-Based Detection

The Docker environment uses ping-based detection for on-demand servers:

```python
def _test_mcp_ping_request(self) -> bool:
    """Test MCP server by sending ping request via echo command"""
    try:
        # Create ping request JSON
        ping_request = '{"method": "neozork/ping", "id": 1, "params": {}}'
        
        # Send request to MCP server via echo command
        cmd = f'echo \'{ping_request}\' | python3 neozork_mcp_server.py'
        
        # Run command with timeout
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=self.project_root
        )
        
        # Check if we got a valid JSON response
        if result.returncode == 0 and result.stdout.strip():
            response = json.loads(result.stdout.strip())
            # Check if response contains expected ping response structure
            return (response.get("jsonrpc") == "2.0" and 
                    response.get("id") == 1 and 
                    response.get("result", {}).get("pong") is True)
        return False
        
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        return False
```

### Expected Response Format

The MCP server should respond with a valid JSON-RPC 2.0 response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "pong": true,
    "timestamp": "2025-01-27T10:30:00Z",
    "server_time": "2025-01-27T10:30:00Z",
    "timezone": "UTC"
  }
}
```

### Environment Variables

Key environment variables monitored in Docker:

```bash
DOCKER_CONTAINER=true
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

## Output Format

### JSON Results

The script saves results in JSON format:

```json
{
  "timestamp": "2025-01-27 10:30:00",
  "environment": "docker",
  "project_root": "/app",
  "server_running": true,
  "connection_test": {
    "status": "success",
    "message": "MCP server is responding to ping requests",
    "test_method": "ping_request",
    "response_time": "immediate"
  },
  "ide_configurations": {
    "cursor": {
      "exists": true,
      "size": 7418,
      "valid_json": true
    },
    "docker": {
      "exists": true,
      "size": 367,
      "valid_json": true
    }
  },
  "docker_specific": {
    "in_docker": true,
    "environment_vars": {
      "DOCKER_CONTAINER": "true",
      "PYTHONPATH": "/app",
      "PYTHONUNBUFFERED": "1"
    },
    "mcp_server_responding": true,
    "test_method": "ping_request",
    "mcp_server_file_exists": true,
    "mcp_server_file_size": 123456,
    "mcp_server_file_modified": "Mon Jan 27 10:30:00 2025",
    "log_file_exists": true,
    "log_file_size": 2048,
    "log_file_modified": "Mon Jan 27 10:30:00 2025"
  },
  "recommendations": [
    "Server is running correctly"
  ]
}
```

### Console Output

```
🔍 MCP Server Status Checker
==================================================

🐳 Detected Docker environment

📅 Check Time: 2025-01-27 10:30:00
🌍 Environment: docker
📁 Project Root: /app

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
   📄 MCP server file: 123456 bytes
   🕒 File modified: Mon Jan 27 10:30:00 2025
   📝 Log file: 2048 bytes
   🕒 Log modified: Mon Jan 27 10:30:00 2025

💡 Recommendations:
   • Server is running correctly
```

## Testing

### Manual Testing

```bash
# Test ping request manually
echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py

# Expected response:
# {"jsonrpc": "2.0", "id": 1, "result": {"pong": true, "timestamp": "...", "server_time": "...", "timezone": "UTC"}}
```

### Automated Testing

```bash
# Test Docker detection
pytest tests/scripts/test_check_mcp_status.py::TestDockerDetection -v

# Test ping functionality
pytest tests/scripts/test_check_mcp_status.py::TestDockerPing -v

# Test comprehensive Docker check
pytest tests/scripts/test_check_mcp_status.py::TestDockerComprehensive -v
```

## Migration from Old Logic

### Previous Detection Methods

The old Docker detection logic used unreliable methods:
- PID file checking
- Process scanning via `/proc`
- `pgrep` and `pidof` commands

### Problems with Old Logic

- MCP server shuts down after requests
- No persistent processes to detect
- PID files may be stale
- False positives/negatives

### New Detection Benefits

- ✅ Always accurate detection
- ✅ Works with on-demand servers
- ✅ Tests actual functionality
- ✅ No false positives/negatives
- ✅ Automatic environment detection
- ✅ Timeout protection
- ✅ JSON validation

## Troubleshooting

### Common Issues

#### Ping Timeout
```bash
# Check if MCP server file exists and is executable
ls -la neozork_mcp_server.py

# Check Python3 availability
python3 --version

# Test with verbose output
echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py 2>&1
```

#### Invalid JSON Response
```bash
# Check MCP server implementation
grep -n "neozork/ping" neozork_mcp_server.py

# Test with different request
echo '{"method": "neozork/status", "id": 1, "params": {}}' | python3 neozork_mcp_server.py
```

#### Environment Detection Issues
```bash
# Check Docker environment
ls -la /.dockerenv
cat /proc/1/cgroup | grep docker
echo $DOCKER_CONTAINER
```

## Related Documentation

- **[MCP Server Detection Logic](docs/development/mcp-server-detection.md)** - Detailed detection implementation
- **[IDE Configuration](docs/guides/ide-configuration.md)** - Multi-IDE setup guide
- **[MCP Servers Reference](docs/reference/mcp-servers/README.md)** - Complete server documentation
- **[Detection Changes](docs/development/MCP_DETECTION_CHANGES.md)** - Migration notes

## Error Handling

### Common Docker Issues

1. **Stale PID File:**
   ```
   PID file exists but process is not running
   ```
   - **Solution:** PID file is automatically cleaned up

2. **Missing Log File:**
   ```
   Log file not found or no recent activity
   ```
   - **Solution:** Check if MCP server was started properly

3. **Process Not Responsive:**
   ```
   Server process is not responsive
   ```
   - **Solution:** Restart the Docker container

### Common Host Issues

1. **No Processes Found:**
   ```
   MCP server is not running
   ```
   - **Solution:** Start the server manually

2. **Permission Issues:**
   ```
   Error checking server status
   ```
   - **Solution:** Check file permissions and user access

## Best Practices

### Docker Environment

1. **Always use PID file:** Ensures reliable process tracking
2. **Monitor log files:** Provides activity confirmation
3. **Clean up stale files:** Automatic cleanup prevents issues
4. **Use environment variables:** Consistent configuration

### Host Environment

1. **Use process discovery:** Reliable across different systems
2. **Check all IDE configs:** Comprehensive configuration validation
3. **Handle process management:** Start/stop capabilities
4. **Log all activities:** Detailed logging for debugging

## Future Enhancements

### Planned Features

1. **Network Connectivity Testing:** Test actual MCP protocol communication
2. **Health Check Endpoints:** HTTP-based health monitoring
3. **Metrics Collection:** Performance and usage metrics
4. **Auto-Recovery:** Automatic server restart on failure

### Integration Opportunities

1. **Monitoring Systems:** Integration with Prometheus, Grafana
2. **CI/CD Pipelines:** Automated testing in deployment
3. **IDE Extensions:** Direct integration with development tools
4. **Alerting:** Notification systems for server issues

## Related Documentation

- [MCP Server Setup](../getting-started/mcp-server-setup.md)
- [Docker Configuration](../deployment/docker-setup.md)
- [IDE Integration](../guides/ide-integration.md)
- [Troubleshooting Guide](../guides/troubleshooting.md) 