# MCP Server Docker Integration

## Overview

The MCP (Model Context Protocol) server status checker has been enhanced to support both Docker and non-Docker environments. This allows for seamless MCP server monitoring regardless of the deployment environment.

## Features

### Automatic Environment Detection

The script automatically detects whether it's running inside a Docker container or on the host system:

- **Docker Detection Methods:**
  - Checks for `/.dockerenv` file
  - Examines `/proc/1/cgroup` for Docker references
  - Looks for `DOCKER_CONTAINER=true` environment variable

### Environment-Specific Logic

#### Docker Environment (`DockerMCPServerChecker`)

- **PID File Monitoring:** Uses `/tmp/mcp_server.pid` created by `docker-entrypoint.sh`
- **Process Validation:** Verifies process is actually running using `os.kill(pid, 0)`
- **Log File Analysis:** Checks `logs/mcp_server.log` for recent activity
- **Docker-Specific Configs:** Monitors Docker environment variables and configurations

#### Host Environment (`MCPServerChecker`)

- **Process Discovery:** Uses `pgrep` to find MCP server processes
- **Process Management:** Can start/stop MCP server processes
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

### PID File Management

The Docker environment uses a PID file approach for process tracking:

```bash
# PID file location
/tmp/mcp_server.pid

# Content: single line with process ID
12345
```

### Log File Monitoring

The Docker checker monitors the MCP server log file for activity:

```bash
# Log file location
/app/logs/mcp_server.log

# Recent activity check (within 30 seconds)
if (current_time - log_mtime) < 30:
    # Consider server active
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
  "timestamp": "2024-01-01 12:00:00",
  "environment": "docker",
  "project_root": "/app",
  "server_running": true,
  "connection_test": {
    "status": "success",
    "message": "Server is running (confirmed via logs)",
    "log_file": "/app/logs/mcp_server.log",
    "last_activity": "Mon Jan 1 12:00:00 2024"
  },
  "ide_configurations": {
    "cursor": {
      "exists": true,
      "size": 1024,
      "valid_json": true
    },
    "docker": {
      "exists": true,
      "size": 512
    }
  },
  "docker_specific": {
    "in_docker": true,
    "environment_vars": {
      "DOCKER_CONTAINER": "true",
      "PYTHONPATH": "/app",
      "PYTHONUNBUFFERED": "1"
    },
    "pid_file_exists": true,
    "pid": 12345,
    "process_running": true,
    "log_file_exists": true,
    "log_file_size": 2048,
    "log_file_modified": "Mon Jan 1 12:00:00 2024"
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

📅 Check Time: 2024-01-01 12:00:00
🌍 Environment: docker
📁 Project Root: /app

🚀 MCP Server Status:
   ✅ Server is running

🔗 Connection Test:
   ✅ Connection successful
   📄 Log file: /app/logs/mcp_server.log

💻 IDE Configurations:
   ✅ CURSOR: 1024 bytes
   ✅ DOCKER: 512 bytes

🐳 Docker Information:
   📦 In Docker: True
   📄 PID file: True
   🔢 PID: 12345
   🟢 Process running: True
   📝 Log file: 2048 bytes
   🕒 Last modified: Mon Jan 1 12:00:00 2024

💡 Recommendations:
   • Server is running correctly

📝 Results saved to: /app/logs/mcp_status_check_docker.json

✅ All checks passed!
```

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

## Testing

### Running Tests

```bash
# Run all MCP status checker tests
pytest tests/scripts/test_check_mcp_status.py -v

# Run specific test categories
pytest tests/scripts/test_check_mcp_status.py::TestDockerDetection -v
pytest tests/scripts/test_check_mcp_status.py::TestDockerMCPServerChecker -v
pytest tests/scripts/test_check_mcp_status.py::TestMCPServerChecker -v
```

### Test Coverage

The test suite covers:

- **Docker Detection:** All detection methods
- **Docker Checker:** PID file handling, process validation, log monitoring
- **Host Checker:** Process discovery, management, IDE configurations
- **Integration:** End-to-end functionality testing

## Configuration

### Docker Environment

The Docker environment is configured through:

1. **docker-entrypoint.sh:** Creates PID file and manages MCP server
2. **docker-compose.yml:** Sets environment variables
3. **Dockerfile:** Installs dependencies and sets up environment

### Host Environment

The host environment uses:

1. **System process management:** `pgrep`, `subprocess`
2. **IDE configuration files:** Various IDE-specific configs
3. **Standard logging:** File-based logging system

## Troubleshooting

### Docker Issues

1. **MCP Server Not Starting:**
   ```bash
   # Check Docker logs
   docker logs <container_name>
   
   # Check MCP server logs
   tail -f logs/mcp_server.log
   ```

2. **PID File Issues:**
   ```bash
   # Check PID file
   cat /tmp/mcp_server.pid
   
   # Verify process
   ps aux | grep neozork_mcp_server
   ```

3. **Permission Issues:**
   ```bash
   # Check file permissions
   ls -la /tmp/mcp_server.pid
   ls -la logs/mcp_server.log
   ```

### Host Issues

1. **Process Not Found:**
   ```bash
   # Check for MCP server processes
   pgrep -f neozork_mcp_server.py
   
   # Start server manually
   python neozork_mcp_server.py &
   ```

2. **Configuration Issues:**
   ```bash
   # Check IDE configurations
   ls -la cursor_mcp_config.json
   ls -la .vscode/settings.json
   ```

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