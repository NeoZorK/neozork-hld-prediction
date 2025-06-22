# MCP Server Auto-Start Guide

## Overview

The MCP Server Auto-Start system automatically manages MCP servers based on project conditions and IDE detection. It provides intelligent server management, health monitoring, and seamless integration with various development environments.

## Features

### Core Capabilities
- **Intelligent IDE Detection**: Automatically detects running IDEs (Cursor, PyCharm, VS Code)
- **Condition-Based Startup**: Starts servers only when conditions are met
- **Health Monitoring**: Monitors server health and automatically restarts failed servers
- **File System Monitoring**: Watches for project changes and adjusts server configuration
- **Resource Management**: Monitors memory and CPU usage
- **Graceful Shutdown**: Ensures proper cleanup when stopping servers

### Advanced Features
- **Multi-Server Support**: Manages multiple MCP servers simultaneously
- **Priority Management**: Handles server priorities and resource allocation
- **Configuration Management**: Dynamic configuration updates
- **Logging and Notifications**: Comprehensive logging and optional notifications
- **Security**: Input validation and path sanitization

## Installation

### Prerequisites
- Python 3.8+
- psutil (for process monitoring)
- watchdog (for file system monitoring)

### Setup

1. **Install dependencies**:
   ```bash
   pip install psutil watchdog
   ```

2. **Configure auto-start**:
   ```bash
   # Create configuration
   cp mcp_auto_config.json.example mcp_auto_config.json
   # Edit configuration as needed
   ```

3. **Start auto-starter**:
   ```bash
   python scripts/auto_start_mcp.py start
   ```

## Configuration

### Basic Configuration

The `mcp_auto_config.json` file controls all auto-start behavior:

```json
{
  "auto_start": {
    "enabled": true,
    "check_interval": 30,
    "ide_detection": true,
    "project_detection": true
  }
}
```

### Server Configuration

Configure individual MCP servers:

```json
{
  "servers": {
    "cursor": {
      "enabled": true,
      "command": "python",
      "args": ["cursor_mcp_server.py"],
      "conditions": ["cursor_ide", "python_files"],
      "env": {
        "PYTHONPATH": "${PROJECT_ROOT}",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Condition Configuration

Define conditions for server startup:

```json
{
  "conditions": {
    "cursor_ide": {
      "processes": ["Cursor", "cursor"],
      "files": [".cursor", "cursor_mcp_config.json"]
    },
    "python_files": {
      "extensions": [".py"],
      "min_files": 1
    }
  }
}
```

## Usage

### Command Line Interface

#### Start Auto-Starter
```bash
# Start in foreground
python scripts/auto_start_mcp.py start

# Start as daemon
python scripts/auto_start_mcp.py start --daemon
```

#### Check Status
```bash
python scripts/auto_start_mcp.py status
```

#### Stop Auto-Starter
```bash
python scripts/auto_start_mcp.py stop
```

#### Restart Servers
```bash
python scripts/auto_start_mcp.py restart
```

### Programmatic Usage

```python
from scripts.auto_start_mcp import MCPAutoStarter

# Create auto starter
auto_starter = MCPAutoStarter()

# Start monitoring
auto_starter.run()

# Get status
status = auto_starter.get_status()
print(f"Running servers: {list(status['servers'].keys())}")
```

## When and How MCP Servers Start

### Automatic Startup Conditions

MCP servers start automatically when:

1. **IDE Detection**: A supported IDE is detected running
2. **Project Conditions**: Required project files and structure are present
3. **Server Conditions**: All server-specific conditions are met
4. **Resource Availability**: Sufficient system resources are available

### Startup Process

1. **Condition Evaluation**: Check all required conditions
2. **Resource Check**: Verify system resources
3. **Server Launch**: Start server process
4. **Health Verification**: Confirm server is running properly
5. **Monitoring Setup**: Begin health monitoring

### Example Scenarios

#### Scenario 1: Cursor IDE with Python Project
```
Conditions:
✅ cursor_ide: Cursor process detected
✅ python_files: Python files found in project
✅ financial_data: Financial data directory exists

Result: Cursor MCP server starts automatically
```

#### Scenario 2: PyCharm IDE with Financial Data
```
Conditions:
✅ pycharm_ide: PyCharm process detected
✅ python_files: Python files found in project
✅ financial_data: CSV files in mql5_feed directory

Result: PyCharm MCP server starts automatically
```

#### Scenario 3: No IDE Running
```
Conditions:
❌ cursor_ide: No Cursor process detected
❌ pycharm_ide: No PyCharm process detected
✅ python_files: Python files found in project

Result: No servers start (waiting for IDE)
```

## Monitoring and Health Checks

### Health Check Process

1. **Process Status**: Check if server process is running
2. **Resource Usage**: Monitor memory and CPU usage
3. **Response Time**: Test server responsiveness
4. **Error Detection**: Check for error conditions

### Automatic Recovery

When a server fails:

1. **Detection**: Health check detects failure
2. **Logging**: Log failure details
3. **Restart**: Attempt server restart
4. **Verification**: Confirm restart success
5. **Escalation**: Notify if restart fails repeatedly

### Resource Monitoring

```json
{
  "monitoring": {
    "max_memory_mb": 512,
    "max_cpu_percent": 80,
    "health_check_interval": 60
  }
}
```

## File System Monitoring

### Watched Events

The auto-starter monitors:

- **File Creation**: New Python files, configuration files
- **File Modification**: Changes to existing files
- **File Deletion**: Removal of important files
- **Directory Changes**: New directories, project structure changes

### Triggered Actions

When changes are detected:

1. **Condition Re-evaluation**: Re-check all conditions
2. **Server Re-evaluation**: Determine which servers should run
3. **Configuration Update**: Update server configurations
4. **Server Management**: Start/stop servers as needed

## Integration with IDEs

### Cursor IDE Integration

```json
{
  "integration": {
    "ide_integration": {
      "cursor": {
        "config_file": ".cursor/settings.json",
        "auto_config": true
      }
    }
  }
}
```

### PyCharm Integration

```json
{
  "integration": {
    "ide_integration": {
      "pycharm": {
        "config_file": "pycharm_mcp_config.json",
        "auto_config": true
      }
    }
  }
}
```

### VS Code Integration

```json
{
  "integration": {
    "ide_integration": {
      "vscode": {
        "config_file": ".vscode/settings.json",
        "auto_config": true
      }
    }
  }
}
```

## Performance Optimization

### Caching

```json
{
  "performance": {
    "cache_enabled": true,
    "cache_size": 1000,
    "cache_ttl": 3600
  }
}
```

### Lazy Loading

- **File Scanning**: Only scan files when needed
- **AST Parsing**: Parse AST trees on demand
- **Index Building**: Build indexes incrementally

### Parallel Processing

```json
{
  "performance": {
    "parallel_processing": true,
    "max_workers": 4
  }
}
```

## Security Considerations

### Input Validation

```json
{
  "security": {
    "validate_inputs": true,
    "sanitize_paths": true
  }
}
```

### Path Restrictions

```json
{
  "security": {
    "allowed_paths": ["${PROJECT_ROOT}"],
    "max_file_size": 10485760
  }
}
```

### Timeout Protection

```json
{
  "security": {
    "timeout": 30000
  }
}
```

## Troubleshooting

### Common Issues

#### Server Not Starting
```bash
# Check conditions
python scripts/auto_start_mcp.py status

# Check logs
tail -f logs/mcp_auto_starter_*.log

# Manual start test
python cursor_mcp_server.py
```

#### High Resource Usage
```bash
# Check resource usage
ps aux | grep mcp

# Adjust limits in config
{
  "monitoring": {
    "max_memory_mb": 256,
    "max_cpu_percent": 50
  }
}
```

#### Frequent Restarts
```bash
# Check restart logs
grep "restart" logs/mcp_auto_starter_*.log

# Increase restart delay
{
  "auto_start": {
    "restart_delay": 10
  }
}
```

### Debug Mode

Enable debug logging:

```json
{
  "logging": {
    "level": "DEBUG"
  }
}
```

### Manual Override

```bash
# Force start specific server
python scripts/run_cursor_mcp.py --mode stdio

# Stop auto-starter and run manually
python scripts/auto_start_mcp.py stop
python cursor_mcp_server.py
```

## Advanced Configuration

### Custom Conditions

```json
{
  "conditions": {
    "custom_condition": {
      "script": "scripts/check_custom_condition.py",
      "timeout": 30,
      "required": true
    }
  }
}
```

### Notification Setup

```json
{
  "notifications": {
    "enabled": true,
    "providers": {
      "slack": {
        "enabled": true,
        "webhook_url": "https://hooks.slack.com/..."
      }
    }
  }
}
```

### CI/CD Integration

```yaml
# .github/workflows/mcp-auto-start.yml
name: MCP Auto-Start Test
on: [push, pull_request]

jobs:
  test-auto-start:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Test Auto-Start
        run: |
          python scripts/auto_start_mcp.py start &
          sleep 10
          python scripts/auto_start_mcp.py status
          python scripts/auto_start_mcp.py stop
```

## Best Practices

### Configuration Management

1. **Version Control**: Keep configuration in version control
2. **Environment Variables**: Use environment variables for sensitive data
3. **Validation**: Validate configuration on startup
4. **Backup**: Keep backup configurations

### Monitoring

1. **Log Rotation**: Configure log rotation to prevent disk space issues
2. **Resource Limits**: Set appropriate resource limits
3. **Health Checks**: Regular health check intervals
4. **Alerting**: Configure notifications for critical events

### Security

1. **Path Validation**: Always validate file paths
2. **Input Sanitization**: Sanitize all inputs
3. **Resource Limits**: Set maximum file sizes and timeouts
4. **Access Control**: Restrict access to project directories only

### Performance

1. **Caching**: Enable caching for frequently accessed data
2. **Lazy Loading**: Use lazy loading for large datasets
3. **Parallel Processing**: Enable parallel processing where appropriate
4. **Resource Monitoring**: Monitor and adjust resource usage

## Conclusion

The MCP Server Auto-Start system provides intelligent, automated management of MCP servers based on project conditions and IDE detection. It ensures optimal performance, reliability, and seamless integration with development workflows.

Key benefits:

- **Automatic Management**: No manual intervention required
- **Intelligent Detection**: Context-aware server startup
- **Health Monitoring**: Proactive health checks and recovery
- **Resource Optimization**: Efficient resource usage
- **Security**: Built-in security measures
- **Flexibility**: Highly configurable for different environments

For more information, see the main MCP server documentation and examples. 