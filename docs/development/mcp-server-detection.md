# MCP Server Detection Logic

## Overview

The NeoZork HLD Prediction project implements intelligent MCP server detection that automatically adapts to different environments (Docker vs host) and provides reliable status monitoring.

## 🔍 Detection Architecture

### Environment Detection
The system automatically detects the environment using multiple methods:

```python
def is_running_in_docker() -> bool:
    """Check if the script is running inside a Docker container"""
    try:
        # Check for Docker-specific files
        if Path("/.dockerenv").exists():
            return True
        
        # Check cgroup for Docker
        try:
            with open("/proc/1/cgroup", "r") as f:
                if "docker" in f.read():
                    return True
        except FileNotFoundError:
            pass
        
        # Check environment variable
        if os.environ.get("DOCKER_CONTAINER") == "true":
            return True
        
        return False
    except Exception:
        return False
```

### Detection Methods

#### Docker Environment Detection
Uses ping-based detection for on-demand servers:

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

#### Host Environment Detection
Uses process-based detection for persistent servers:

```python
def check_server_running(self) -> bool:
    """Check if MCP server is already running"""
    try:
        # Check for Python processes running the MCP server
        result = subprocess.run(
            ['pgrep', '-f', 'neozork_mcp_server.py'],
            capture_output=True,
            text=True
        )
        
        return result.returncode == 0
        
    except Exception as e:
        return False
```

## 🐳 Docker Environment Features

### On-Demand Server Operation
- **Start**: Server starts when request is received
- **Process**: Handles the request
- **Shutdown**: Server terminates after response
- **Detection**: Ping-based testing required

### Ping-Based Detection
- **Method**: Send JSON-RPC ping request
- **Command**: `echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py`
- **Timeout**: 10 seconds maximum
- **Validation**: JSON-RPC 2.0 response with `pong: true`

### Expected Response Format
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

## 🖥️ Host Environment Features

### Persistent Server Operation
- **Start**: Server runs continuously
- **Process**: Handles multiple requests
- **Monitoring**: Process-based detection
- **Control**: Start/stop capabilities

### Process-Based Detection
- **Method**: Use `pgrep` to find running processes
- **Command**: `pgrep -f neozork_mcp_server.py`
- **Features**: PID tracking, multiple instances
- **Control**: Can start and stop server processes

### Server Management
```python
def start_server(self, timeout: int = 10) -> bool:
    """Start MCP server"""
    self.server_process = subprocess.Popen(
        [sys.executable, 'neozork_mcp_server.py'],
        cwd=self.project_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(2)
    return self.server_process.poll() is None

def stop_server(self):
    """Stop MCP server"""
    if self.server_process:
        self.server_process.terminate()
        self.server_process.wait(timeout=5)
```

## 📊 Status Monitoring

### Comprehensive Status Check
The `scripts/check_mcp_status.py` script provides:

- **Environment Detection**: Automatic Docker vs host detection
- **Server Status**: Running/not running status
- **Connection Test**: Functional connectivity verification
- **IDE Configurations**: Configuration file validation
- **Docker Information**: Container-specific details
- **Recommendations**: Actionable suggestions

### Status Output Examples

#### Docker Environment
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

#### Host Environment
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

## 🔧 Configuration Management

### IDE Configuration Files
- **Cursor**: `cursor_mcp_config.json`
- **VS Code**: `.vscode/settings.json`
- **PyCharm**: `pycharm_mcp_config.json`
- **Docker**: `docker.env`

### Configuration Validation
```python
def check_ide_configurations(self) -> Dict[str, Any]:
    """Check IDE configuration files"""
    configs = {}
    
    for ide, config_path in [
        ('cursor', 'cursor_mcp_config.json'),
        ('vscode', '.vscode/settings.json'),
        ('pycharm', 'pycharm_mcp_config.json'),
        ('docker', 'docker.env')
    ]:
        config_file = self.project_root / config_path
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    content = f.read().strip()
                    # Validate JSON format
                    try:
                        json.loads(content)
                        valid_json = True
                    except json.JSONDecodeError:
                        # Check environment file format
                        valid_json = all('=' in line or line.startswith('#') or not line.strip() 
                                       for line in content.split('\n'))
                    
                    configs[ide] = {
                        'exists': True,
                        'size': config_file.stat().st_size,
                        'valid_json': valid_json
                    }
            except Exception as e:
                configs[ide] = {
                    'exists': True,
                    'error': str(e),
                    'valid_json': False
                }
        else:
            configs[ide] = {'exists': False}
    
    return configs
```

## 🧪 Testing

### Test Coverage
- **Unit Tests**: Individual detection method testing
- **Integration Tests**: End-to-end detection workflow
- **Environment Tests**: Docker vs host environment detection
- **Ping Tests**: JSON-RPC communication validation

### Test Examples
```python
def test_docker_environment_detection():
    """Test Docker environment detection"""
    checker = DockerMCPServerChecker()
    assert checker._is_running_in_docker() == True

def test_ping_request_detection():
    """Test ping-based detection"""
    checker = DockerMCPServerChecker()
    result = checker._test_mcp_ping_request()
    assert isinstance(result, bool)

def test_host_environment_detection():
    """Test host environment detection"""
    checker = MCPServerChecker()
    result = checker.check_server_running()
    assert isinstance(result, bool)
```

## 🔄 Migration from Old Logic

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

## 📚 Related Documentation

- **[MCP Servers Reference](docs/reference/mcp-servers/README.md)** - Complete server documentation
- **[IDE Configuration](docs/guides/ide-configuration.md)** - Multi-IDE setup guide
- **[Detection Changes](docs/development/MCP_DETECTION_CHANGES.md)** - Migration notes
- **[Docker Setup](docs/deployment/docker-setup.md)** - Containerized deployment 