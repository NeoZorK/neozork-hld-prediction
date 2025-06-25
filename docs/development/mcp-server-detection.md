# MCP Server Detection Logic

## Overview

The MCP (Model Context Protocol) server detection logic has been updated to handle different environments appropriately. The system now uses different detection methods for Docker and host environments.

## Environment Detection

The system automatically detects the environment using the `is_running_in_docker()` function, which checks:

1. **Docker-specific files**: Presence of `/.dockerenv`
2. **Cgroup information**: Docker references in `/proc/1/cgroup`
3. **Environment variables**: `DOCKER_CONTAINER=true`

## Detection Methods

### Docker Environment

In Docker containers, the MCP server operates on a **request-response basis** and shuts down after processing requests. Therefore, traditional process-based detection methods are ineffective.

#### New Ping-Based Detection

The Docker environment uses a **ping-based detection method**:

```python
def _test_mcp_ping_request(self) -> bool:
    """Test MCP server by sending ping request via echo command"""
    # Create ping request JSON
    ping_request = '{"method": "neozork/ping", "id": 1, "params": {}}'
    
    # Send request to MCP server via echo command
    cmd = f'echo \'{ping_request}\' | python3 neozork_mcp_server.py'
    
    # Run command with timeout
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
    
    # Validate JSON response
    if result.returncode == 0 and result.stdout.strip():
        response = json.loads(result.stdout.strip())
        return (response.get("jsonrpc") == "2.0" and 
                response.get("id") == 1 and 
                response.get("result", {}).get("pong") is True)
    return False
```

#### Advantages of Ping-Based Detection

1. **Accurate**: Tests actual server functionality
2. **Reliable**: Works regardless of process state
3. **Fast**: Quick response time
4. **Docker-compatible**: Works with on-demand server model

### Host Environment

In host environments, the MCP server typically runs as a persistent process. The system uses traditional process-based detection:

```python
def check_server_running(self) -> bool:
    """Check if MCP server is already running"""
    result = subprocess.run(
        ['pgrep', '-f', 'neozork_mcp_server.py'],
        capture_output=True,
        text=True
    )
    return result.returncode == 0
```

## Implementation Details

### DockerMCPServerChecker Class

- **Primary method**: `_test_mcp_ping_request()`
- **Fallback**: None (ping is the only reliable method)
- **Timeout**: 10 seconds
- **Validation**: JSON-RPC 2.0 response with `pong: true`

### MCPServerChecker Class

- **Primary method**: `pgrep` command
- **Fallback**: Process management methods
- **Features**: Start/stop server capabilities
- **Validation**: Process existence check

## Usage Examples

### Docker Environment

```bash
# Inside Docker container
python3 scripts/check_mcp_status.py
```

Output:
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

🐳 Docker Information:
   📦 In Docker: True
   🔄 MCP Server responding: True
   🔍 Test method: ping_request
   📄 MCP server file: 123456 bytes
   📝 Log file: 789 bytes
```

### Host Environment

```bash
# On host system
python3 scripts/check_mcp_status.py
```

Output:
```
🔍 MCP Server Status Checker
==================================================
🖥️  Detected host environment

🚀 MCP Server Status:
   ✅ Server is running

🔗 Connection Test:
   ✅ Connection successful
   👥 PIDs: 12345, 67890
```

## Configuration

### Docker-Specific Settings

- **Timeout**: 10 seconds for ping requests
- **Command**: `echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py`
- **Working directory**: Project root
- **Validation**: JSON-RPC 2.0 response format

### Host-Specific Settings

- **Process detection**: `pgrep -f neozork_mcp_server.py`
- **Server management**: Start/stop capabilities
- **PID tracking**: Multiple process support

## Troubleshooting

### Docker Issues

1. **Ping timeout**: Check if MCP server file exists and is executable
2. **Invalid JSON response**: Verify server implementation
3. **Command not found**: Ensure Python3 is available in container

### Host Issues

1. **Process not found**: Check if server is running
2. **Permission denied**: Verify pgrep access
3. **Multiple processes**: Check for zombie processes

## Testing

The detection logic is thoroughly tested with unit tests covering:

- ✅ Successful ping requests
- ✅ Failed ping requests
- ✅ Invalid JSON responses
- ✅ Timeout scenarios
- ✅ Environment detection
- ✅ Host process detection

Run tests with:
```bash
python3 -m pytest tests/scripts/test_check_mcp_status.py -v
```

## Migration Notes

### From Old Logic

The old Docker detection logic used:
- PID file checking
- Process scanning via `/proc`
- `pgrep` and `pidof` commands

These methods were unreliable because:
- MCP server shuts down after requests
- No persistent processes to detect
- PID files may be stale

### To New Logic

The new logic uses:
- Direct ping requests
- JSON-RPC validation
- Timeout-based reliability

Benefits:
- ✅ Always accurate
- ✅ Works with on-demand servers
- ✅ Tests actual functionality
- ✅ No false positives/negatives

## Future Enhancements

Potential improvements:
1. **Caching**: Cache ping results for short periods
2. **Health checks**: More comprehensive server health validation
3. **Metrics**: Response time tracking
4. **Retry logic**: Automatic retry on failure
5. **Load balancing**: Support for multiple server instances 