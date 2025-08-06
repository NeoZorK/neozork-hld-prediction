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

## 🚀 Quick Start Examples

### Basic MCP Server Check
```bash
# Check MCP server status (works in both Docker and host environments)
python scripts/mcp/check_mcp_status.py

# Expected output in Docker:
# 🐳 Detected Docker environment
# 🚀 MCP Server Status: ✅ Server is running
# 🔗 Connection Test: ✅ Connection successful
# 🔍 Test method: ping_request

# Expected output on host:
# 🖥️  Detected host environment
# 🚀 MCP Server Status: ✅ Server is running
# 🔗 Connection Test: ✅ Connection successful
# 👥 PIDs: 12345, 67890
```

### Manual MCP Server Test
```bash
# Test MCP server with ping request
echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py

# Expected response:
# {"jsonrpc": "2.0", "id": 1, "result": {"pong": true, "timestamp": "2025-01-27T10:30:00Z", "server_time": "2025-01-27T10:30:00Z", "timezone": "UTC"}}
```

## 🐳 Docker Environment Examples

### Docker Container MCP Check
```bash
# Build and run Docker container
docker-compose build
docker-compose run --rm app bash

# Inside container, check MCP server
python scripts/mcp/check_mcp_status.py

# Test ping request in container
echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py
```

### Docker Environment Detection
```python
# Example: Docker environment detection
from scripts.check_mcp_status import is_running_in_docker

# Check if running in Docker
if is_running_in_docker():
    print("🐳 Running in Docker environment")
    # Use ping-based detection
    checker = DockerMCPServerChecker()
else:
    print("🖥️  Running in host environment")
    # Use process-based detection
    checker = MCPServerChecker()

# Run comprehensive check
results = checker.run_comprehensive_check()
print(f"Server running: {results['server_running']}")
```

### Docker Ping Detection Example
```python
# Example: Ping-based detection in Docker
def test_docker_mcp_ping():
    """Test MCP server ping in Docker environment"""
    import subprocess
    import json
    
    # Create ping request
    ping_request = '{"method": "neozork/ping", "id": 1, "params": {}}'
    cmd = f'echo \'{ping_request}\' | python3 neozork_mcp_server.py'
    
    # Execute ping request
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0 and result.stdout.strip():
        response = json.loads(result.stdout.strip())
        if (response.get("jsonrpc") == "2.0" and 
            response.get("id") == 1 and 
            response.get("result", {}).get("pong") is True):
            print("✅ MCP server responded successfully")
            return True
        else:
            print("❌ Invalid response format")
            return False
    else:
        print("❌ MCP server not responding")
        return False
```

## 🖥️ Host Environment Examples

### Host Environment MCP Check
```bash
# Check MCP server status on host
python scripts/mcp/check_mcp_status.py

# Start MCP server manually (if not running)
python3 neozork_mcp_server.py &

# Check running processes
pgrep -f neozork_mcp_server.py
```

### Host Process Detection Example
```python
# Example: Process-based detection on host
def test_host_mcp_process():
    """Test MCP server process detection on host"""
    import subprocess
    
    # Check for running MCP server processes
    result = subprocess.run(
        ['pgrep', '-f', 'neozork_mcp_server.py'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        pids = result.stdout.strip().split('\n')
        print(f"✅ MCP server running with PIDs: {pids}")
        return True
    else:
        print("❌ MCP server not running")
        return False
```

### Host Server Management Example
```python
# Example: Start/stop MCP server on host
from scripts.check_mcp_status import MCPServerChecker

def manage_host_mcp_server():
    """Manage MCP server on host environment"""
    checker = MCPServerChecker()
    
    # Check if server is running
    if not checker.check_server_running():
        print("Starting MCP server...")
        if checker.start_server():
            print("✅ MCP server started successfully")
        else:
            print("❌ Failed to start MCP server")
    else:
        print("✅ MCP server is already running")
    
    # Test connection
    connection = checker.test_connection()
    if connection.get("status") == "success":
        print("✅ Connection test successful")
    else:
        print(f"❌ Connection test failed: {connection.get('error')}")
    
    # Stop server (optional)
    # checker.stop_server()
    # print("MCP server stopped")
```

## 🔧 Configuration Examples

### IDE Configuration Setup
```bash
# Setup all IDE configurations
python3 scripts/setup_ide_configs.py

# Verify configurations
python3 -m pytest tests/docker/test_ide_configs.py -v

# Check configuration files
ls -la cursor_mcp_config.json .vscode/settings.json pycharm_mcp_config.json docker.env
```

### Configuration Validation Example
```python
# Example: Validate IDE configurations
def validate_ide_configs():
    """Validate IDE configuration files"""
    import json
    from pathlib import Path
    
    configs = {
        'cursor': 'cursor_mcp_config.json',
        'vscode': '.vscode/settings.json',
        'pycharm': 'pycharm_mcp_config.json',
        'docker': 'docker.env'
    }
    
    for ide, config_path in configs.items():
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    content = f.read().strip()
                    # Try to parse as JSON
                    try:
                        json.loads(content)
                        print(f"✅ {ide.upper()}: Valid JSON")
                    except json.JSONDecodeError:
                        # Check environment file format
                        if all('=' in line or line.startswith('#') or not line.strip() 
                               for line in content.split('\n')):
                            print(f"✅ {ide.upper()}: Valid environment file")
                        else:
                            print(f"⚠️  {ide.upper()}: Invalid format")
            except Exception as e:
                print(f"❌ {ide.upper()}: Error reading file - {e}")
        else:
            print(f"❌ {ide.upper()}: File not found")
```

## 🧪 Testing Examples

### Unit Test Examples
```python
# Example: Test MCP server detection
import pytest
from scripts.check_mcp_status import DockerMCPServerChecker, MCPServerChecker

def test_docker_ping_detection():
    """Test ping-based detection in Docker"""
    checker = DockerMCPServerChecker()
    result = checker._test_mcp_ping_request()
    assert isinstance(result, bool)

def test_host_process_detection():
    """Test process-based detection on host"""
    checker = MCPServerChecker()
    result = checker.check_server_running()
    assert isinstance(result, bool)

def test_environment_detection():
    """Test environment detection"""
    from scripts.check_mcp_status import is_running_in_docker
    result = is_running_in_docker()
    assert isinstance(result, bool)
```

### Integration Test Examples
```python
# Example: Integration test for MCP server
def test_mcp_server_integration():
    """Test complete MCP server integration"""
    from scripts.check_mcp_status import is_running_in_docker
    
    if is_running_in_docker():
        checker = DockerMCPServerChecker()
    else:
        checker = MCPServerChecker()
    
    # Run comprehensive check
    results = checker.run_comprehensive_check()
    
    # Validate results structure
    assert "timestamp" in results
    assert "environment" in results
    assert "server_running" in results
    assert "connection_test" in results
    assert "ide_configurations" in results
    
    # Validate environment detection
    assert results["environment"] in ["docker", "host"]
    
    # Validate server status is boolean
    assert isinstance(results["server_running"], bool)
    
    # Validate connection test
    connection = results["connection_test"]
    assert "status" in connection
    assert connection["status"] in ["success", "failed", "skipped"]
```

## 📊 Status Monitoring Examples

### Comprehensive Status Check
```python
# Example: Comprehensive MCP status monitoring
def monitor_mcp_status():
    """Monitor MCP server status comprehensively"""
    from scripts.check_mcp_status import is_running_in_docker
    
    if is_running_in_docker():
        checker = DockerMCPServerChecker()
        print("🐳 Docker environment detected")
    else:
        checker = MCPServerChecker()
        print("🖥️  Host environment detected")
    
    # Run comprehensive check
    results = checker.run_comprehensive_check()
    
    # Print status summary
    print(f"\n📅 Check Time: {results['timestamp']}")
    print(f"🌍 Environment: {results['environment']}")
    print(f"🚀 Server Status: {'✅ Running' if results['server_running'] else '❌ Not Running'}")
    
    # Print connection test results
    connection = results["connection_test"]
    if connection.get("status") == "success":
        print("🔗 Connection: ✅ Successful")
        if "test_method" in connection:
            print(f"   🔍 Method: {connection['test_method']}")
    else:
        print(f"🔗 Connection: ❌ Failed - {connection.get('error', 'Unknown')}")
    
    # Print IDE configurations
    print("\n💻 IDE Configurations:")
    for ide, config in results["ide_configurations"].items():
        if config.get('exists'):
            size = config.get('size', 0)
            valid = config.get('valid_json', False)
            status = "✅" if valid else "⚠️"
            print(f"   {status} {ide.upper()}: {size} bytes")
        else:
            print(f"   ❌ {ide.upper()}: Not configured")
    
    # Print recommendations
    if results["recommendations"]:
        print(f"\n💡 Recommendations:")
        for rec in results["recommendations"]:
            print(f"   • {rec}")
    
    return results
```

### Real-time Monitoring
```python
# Example: Real-time MCP server monitoring
import time
from scripts.check_mcp_status import is_running_in_docker

def monitor_mcp_realtime(interval=30):
    """Monitor MCP server status in real-time"""
    print(f"🔍 Starting real-time MCP monitoring (check every {interval}s)")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            if is_running_in_docker():
                checker = DockerMCPServerChecker()
            else:
                checker = MCPServerChecker()
            
            # Quick status check
            server_running = checker.check_server_running()
            status = "✅ Running" if server_running else "❌ Not Running"
            
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] MCP Server: {status}")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")
```

## 🔍 Debug Examples

### Debug MCP Server Issues
```python
# Example: Debug MCP server issues
def debug_mcp_server():
    """Debug MCP server issues"""
    import subprocess
    import json
    
    print("🔍 Debugging MCP server...")
    
    # Check if MCP server file exists
    mcp_file = Path("neozork_mcp_server.py")
    if mcp_file.exists():
        print(f"✅ MCP server file exists: {mcp_file.stat().st_size} bytes")
    else:
        print("❌ MCP server file not found")
        return
    
    # Test ping request with detailed output
    ping_request = '{"method": "neozork/ping", "id": 1, "params": {}}'
    cmd = f'echo \'{ping_request}\' | python3 neozork_mcp_server.py'
    
    print(f"🔍 Executing: {cmd}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        print(f"📊 Return code: {result.returncode}")
        print(f"📤 STDOUT: {result.stdout.strip()}")
        print(f"📥 STDERR: {result.stderr.strip()}")
        
        if result.returncode == 0 and result.stdout.strip():
            try:
                response = json.loads(result.stdout.strip())
                print("✅ Valid JSON response received")
                print(f"📋 Response: {json.dumps(response, indent=2)}")
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON response: {e}")
        else:
            print("❌ No valid response received")
            
    except subprocess.TimeoutExpired:
        print("⏰ Request timed out")
    except Exception as e:
        print(f"❌ Error: {e}")
```

## 📚 Related Examples

- **[Docker Examples](docker-examples.md)** - Containerized deployment examples
- **[Testing Examples](testing-examples.md)** - Test framework examples
- **[Script Examples](script-examples.md)** - Utility script examples

## 🔄 Migration Examples

### From Old to New Detection
```python
# Example: Migration from old detection logic
def migrate_detection_logic():
    """Example of migrating from old to new detection logic"""
    
    # Old logic (unreliable in Docker)
    def old_docker_detection():
        try:
            # Check PID file
            pid_file = Path("/tmp/mcp_server.pid")
            if pid_file.exists():
                return True
            
            # Check processes
            result = subprocess.run(['pgrep', '-f', 'neozork_mcp_server.py'])
            return result.returncode == 0
        except:
            return False
    
    # New logic (reliable in all environments)
    def new_docker_detection():
        try:
            ping_request = '{"method": "neozork/ping", "id": 1, "params": {}}'
            cmd = f'echo \'{ping_request}\' | python3 neozork_mcp_server.py'
            
            result = subprocess.run(
                cmd, shell=True, capture_output=True, 
                text=True, timeout=10
            )
            
            if result.returncode == 0 and result.stdout.strip():
                response = json.loads(result.stdout.strip())
                return (response.get("jsonrpc") == "2.0" and 
                        response.get("id") == 1 and 
                        response.get("result", {}).get("pong") is True)
            return False
        except:
            return False
    
    print("🔄 Migration completed")
    print("✅ New detection logic is more reliable")
    print("✅ Works with on-demand servers")
    print("✅ Tests actual functionality") 