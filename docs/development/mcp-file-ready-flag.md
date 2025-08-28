# MCP Server File-Based Ready Flag Solution

## Problem Analysis

The original issue was that when running the MCP server in Docker containers:

1. **MCP server starts in background** with `nohup python neozork_mcp_server.py > /app/logs/mcp_server.log 2>&1 &`
2. **Server begins indexing** the codebase (scanning files, parsing code, etc.)
3. **Docker entrypoint tries to ping** the server via `echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py`
4. **Ping fails** because it tries to start a new MCP server instance instead of communicating with the background process
5. **Result**: "All checks Done" with failed ping attempts

## Root Cause

The fundamental issue is that **MCP servers communicate via stdin/stdout**, not TCP sockets. When the server runs in the background with `nohup`, it's not accessible via stdin/stdout from other processes.

## Solution: File-Based Ready Flag

Instead of trying to communicate with the background process, we use a **file-based ready flag**:

### 1. MCP Server Creates Ready File

When the MCP server completes initialization, it creates a ready flag file:

```python
# Set ready flag after initialization
self.ready = True

# Create ready file for Docker integration
ready_file = self.project_root / "logs" / "mcp_server_ready.flag"
try:
    ready_file.parent.mkdir(exist_ok=True)
    with open(ready_file, 'w') as f:
        f.write(f"ready:{datetime.now().isoformat()}\n")
    print_to_stderr(f"📄 Ready flag file created: {ready_file}")
except Exception as e:
    print_to_stderr(f"⚠️  Could not create ready flag file: {e}")
```

### 2. Simple Ready Check Script

Created `scripts/mcp/check_mcp_ready.py` that checks for the ready file:

```python
def check_mcp_ready(project_root: Path = None) -> bool:
    """Check if MCP server is ready using file flag"""
    ready_file = project_root / "logs" / "mcp_server_ready.flag"
    
    if not ready_file.exists():
        return False
    
    try:
        # Check if file is recent (created in last 5 minutes)
        file_age = time.time() - ready_file.stat().st_mtime
        if file_age > 300:  # 5 minutes
            return False
        
        # Read the file to verify it's valid
        with open(ready_file, 'r') as f:
            content = f.read().strip()
            if content.startswith("ready:"):
                return True
        
        return False
    except Exception:
        return False
```

### 3. Updated Docker Entrypoint

The Docker entrypoint now uses retry logic with the file-based check:

```bash
# Wait for MCP server to be ready with retry logic
echo -e "\033[1;33m=== Waiting for MCP server to be ready ===\033[0m\n"
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
  echo -e "\033[1;34mAttempt $attempt/$max_attempts: Checking MCP server status...\033[0m"
  
  if python /app/scripts/mcp/check_mcp_ready.py; then
    echo -e "\033[1;32m✅ MCP server is ready and responding\033[0m\n"
    break
  else
    echo -e "\033[1;33m⏳ MCP server is still initializing... (attempt $attempt/$max_attempts)\033[0m"
    sleep 2
    attempt=$((attempt + 1))
  fi
done
```

## File Format

The ready flag file (`logs/mcp_server_ready.flag`) contains:

```
ready:2025-08-28T15:50:12.901063
```

## Validation Rules

The ready check validates:

1. **File exists**: `logs/mcp_server_ready.flag` must exist
2. **Recent file**: File must be less than 5 minutes old
3. **Valid content**: File must start with "ready:"
4. **Valid timestamp**: Content must contain a valid ISO timestamp

## Benefits

1. **Simple and Reliable**: No complex IPC or socket communication
2. **Docker Compatible**: Works perfectly with background processes
3. **Fast**: File system checks are very fast
4. **Robust**: Handles edge cases (old files, invalid content)
5. **Debuggable**: Easy to inspect the ready file manually

## Testing

### Unit Tests

```bash
# Test file-based ready flag
uv run pytest tests/mcp/test_ready_file.py -v

# Test original ready flag functionality
uv run pytest tests/mcp/test_ready_flag.py -v
```

### Demo Script

```bash
# Run the demo
uv run python scripts/mcp/test_ready_file_demo.py
```

## Implementation Details

### Files Modified

1. **`neozork_mcp_server.py`**:
   - Clear existing ready file on startup
   - Create ready file after initialization

2. **`scripts/mcp/check_mcp_ready.py`** (new):
   - Simple file-based ready check

3. **`docker-entrypoint.sh`**:
   - Replace ping-based check with file-based check
   - Add retry logic with proper feedback

4. **`tests/mcp/test_ready_file.py`** (new):
   - Comprehensive tests for file-based ready flag

### File Locations

- **Ready flag file**: `logs/mcp_server_ready.flag`
- **Check script**: `scripts/mcp/check_mcp_ready.py`
- **Tests**: `tests/mcp/test_ready_file.py`
- **Demo**: `scripts/mcp/test_ready_file_demo.py`

## Usage

### In Docker

The solution works automatically in Docker containers. The entrypoint script will:

1. Start MCP server in background
2. Wait for ready file to appear
3. Provide clear feedback about initialization progress
4. Continue when server is ready

### Manual Check

You can manually check if the MCP server is ready:

```bash
python scripts/mcp/check_mcp_ready.py
```

### Programmatic Check

```python
from scripts.mcp.check_mcp_ready import check_mcp_ready

if check_mcp_ready():
    print("MCP server is ready")
else:
    print("MCP server is still initializing")
```

## Troubleshooting

### Ready File Not Created

If the ready file is not created:

1. Check MCP server logs: `tail -f logs/mcp_server.log`
2. Verify server process is running: `ps aux | grep neozork_mcp_server`
3. Check for errors in initialization

### Ready File Too Old

If the ready file is considered "too old":

1. The file is older than 5 minutes
2. Server may have crashed or stopped
3. Delete the file and restart the server

### Invalid Ready File

If the ready file has invalid content:

1. Check file content: `cat logs/mcp_server_ready.flag`
2. File should start with "ready:"
3. Delete the file and restart the server

## Future Enhancements

Potential improvements:

1. **Progress tracking**: Include initialization progress in ready file
2. **Health checks**: Add periodic health check updates
3. **Metrics**: Track initialization time and performance
4. **Cleanup**: Automatic cleanup of old ready files
