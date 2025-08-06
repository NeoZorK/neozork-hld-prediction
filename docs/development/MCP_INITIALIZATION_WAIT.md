# MCP Server Initialization Wait Logic

## Overview

Updated the MCP server status checking logic to properly wait for server initialization before performing status checks. This addresses the issue where Docker containers would check MCP server status before the server had completed its initialization process.

## Problem

The original MCP server checking logic would immediately test the server after starting it in the background, but the MCP server performs several initialization steps:

1. **Project scanning** - Scans and indexes project files
2. **Financial data scanning** - Processes financial data files  
3. **Code indexing** - Parses AST and indexes functions/classes
4. **Configuration loading** - Loads server configuration

These steps can take 30-60 seconds on first startup, causing status checks to fail prematurely.

## Solution

Implemented **initialization wait logic** that:

### Key Features

1. **Dual Detection Method**: 
   - Ping request testing
   - Log file monitoring for completion message

2. **Configurable Timeout**: 
   - Default 60 seconds maximum wait time
   - Configurable via `max_wait_time` parameter

3. **Progressive Checking**: 
   - Checks every 2 seconds
   - Stops immediately when initialization is detected

### Implementation

#### New Method: `_wait_for_mcp_initialization()`

```python
def _wait_for_mcp_initialization(self, max_wait_time: int = 60) -> bool:
    """Wait for MCP server to complete initialization"""
    # Checks ping response and log file for completion
    # Returns True when initialization is detected
    # Returns False after timeout
```

#### Updated Methods

- `check_server_running()` - Now waits for initialization first
- `test_connection()` - Now waits for initialization first

### Detection Logic

1. **Ping Response**: Tests if server responds to ping requests
2. **Log Monitoring**: Looks for completion message in logs:
   ```
   ✅ Neozork Unified MCP Server initialized successfully
   ```

## Code Changes

### Modified Files

1. **`scripts/mcp/check_mcp_status.py`**
   - Added `_wait_for_mcp_initialization()` method
   - Updated `check_server_running()` for Docker
   - Updated `test_connection()` for Docker

2. **`scripts/mcp/check_mcp_status.py`**
   - Added `_wait_for_mcp_initialization()` method  
   - Updated `check_server_running()` for Docker
   - Updated `test_connection()` for Docker

3. **`container-entrypoint.sh`**
   - Updated MCP server startup logic
   - Added informative messages about initialization wait
   - Added log file checking suggestion on failure

4. **`docker-entrypoint.sh`**
   - Updated MCP server startup logic
   - Added informative messages about initialization wait
   - Added log file checking suggestion on failure

### New Test File

- **`tests/mcp/test_mcp_initialization_wait.py`**
  - Comprehensive tests for initialization wait logic
  - Tests both success and failure scenarios
  - Tests log file detection
  - Tests timeout behavior

## Usage

### Automatic Usage

The initialization wait logic is automatically used when:

1. **Docker environment detected**
2. **MCP server status check performed**
3. **MCP server connection test performed**

### Manual Usage

```python
from scripts.mcp.check_mcp_status import DockerMCPServerChecker

checker = DockerMCPServerChecker()
result = checker.check_server_running()  # Includes initialization wait
```

### Configuration

```python
# Custom timeout (default is 60 seconds)
checker._wait_for_mcp_initialization(max_wait_time=30)
```

## Benefits

✅ **Reliable Detection**: Waits for actual initialization completion  
✅ **Dual Verification**: Uses both ping and log file detection  
✅ **Configurable**: Adjustable timeout for different environments  
✅ **Informative**: Clear messages about initialization progress  
✅ **Robust**: Handles both success and failure scenarios  

## Testing

Run the new tests:

```bash
# Run initialization wait tests
uv run pytest tests/mcp/test_mcp_initialization_wait.py -v

# Run all MCP tests
uv run pytest tests/mcp/ -v
```

## Docker Integration

The Docker entrypoint scripts now:

1. **Start MCP server** in background
2. **Wait for initialization** with informative messages
3. **Check status** only after initialization completes
4. **Provide helpful feedback** on success/failure

Example output:
```
=== Starting MCP server in background (UV Mode) ===
MCP server started in background (PID: 12345)

=== Waiting for MCP server initialization ===
This may take up to 60 seconds for first startup...

=== Checking MCP server status ===
✅ MCP server is running correctly
```

## Troubleshooting

If MCP server initialization fails:

1. **Check logs**: `tail -f /app/logs/mcp_server.log`
2. **Increase timeout**: Modify `max_wait_time` parameter
3. **Check resources**: Ensure sufficient memory/CPU
4. **Verify dependencies**: Ensure all required packages are installed

## Future Enhancements

- **Progress indicators**: Show initialization progress percentage
- **Resource monitoring**: Monitor memory/CPU during initialization
- **Parallel initialization**: Speed up initialization process
- **Caching**: Cache initialization results for faster subsequent starts 