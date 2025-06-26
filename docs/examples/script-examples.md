# Script Examples

## Overview

Examples demonstrating utility scripts and automation tools in the NeoZork HLD Prediction project, including MCP server detection scripts.

## 🚀 Quick Start Examples

### MCP Server Status Check
```bash
# Check MCP server status (works in both Docker and host environments)
python scripts/check_mcp_status.py

# Expected output in Docker:
# 🔍 MCP Server Status Checker
# ==================================================
# 🐳 Detected Docker environment
# 
# 🚀 MCP Server Status:
#    ✅ Server is running
# 
# 🔗 Connection Test:
#    ✅ Connection successful
#    🔍 Test method: ping_request
#    ⏱️  Response time: immediate
# 
# 💻 IDE Configurations:
#    ✅ CURSOR: 7418 bytes
#    ✅ DOCKER: 367 bytes
# 
# 🐳 Docker Information:
#    📦 In Docker: True
#    🔄 MCP Server responding: True
#    🔍 Test method: ping_request

# Expected output on host:
# 🔍 MCP Server Status Checker
# ==================================================
# 🖥️  Detected host environment
# 
# 🚀 MCP Server Status:
#    ✅ Server is running
# 
# 🔗 Connection Test:
#    ✅ Connection successful
#    👥 PIDs: 12345, 67890
# 
# 💻 IDE Configurations:
#    ✅ CURSOR: 7418 bytes
#    ✅ VSCODE: 2613 bytes
#    ✅ PYCHARM: 4174 bytes
#    ✅ DOCKER: 367 bytes
```

### IDE Configuration Setup
```bash
# Setup all IDE configurations automatically
python3 scripts/setup_ide_configs.py

# Verify the setup
python3 -m pytest tests/docker/test_ide_configs.py -v

# Check configuration files
ls -la cursor_mcp_config.json .vscode/settings.json pycharm_mcp_config.json docker.env
```

## 🔧 MCP Server Script Examples

### Manual MCP Server Test
```bash
# Test MCP server with ping request
echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 neozork_mcp_server.py

# Expected response:
# {"jsonrpc": "2.0", "id": 1, "result": {"pong": true, "timestamp": "2025-01-27T10:30:00Z", "server_time": "2025-01-27T10:30:00Z", "timezone": "UTC"}}
```

### MCP Server Detection Script
```python
# Example: MCP server detection script
#!/usr/bin/env python3
"""
MCP Server Detection Script
Detect and test MCP server in different environments
"""

import sys
from pathlib import Path
from scripts.check_mcp_status import is_running_in_docker, DockerMCPServerChecker, MCPServerChecker

def main():
    """Main detection function"""
    print("🔍 MCP Server Detection Script")
    print("=" * 40)
    
    # Detect environment
    if is_running_in_docker():
        print("🐳 Docker environment detected")
        checker = DockerMCPServerChecker()
    else:
        print("🖥️  Host environment detected")
        checker = MCPServerChecker()
    
    # Check server status
    server_running = checker.check_server_running()
    print(f"🚀 Server Status: {'✅ Running' if server_running else '❌ Not Running'}")
    
    # Test connection
    connection = checker.test_connection()
    if connection.get("status") == "success":
        print("🔗 Connection: ✅ Successful")
        if "test_method" in connection:
            print(f"   🔍 Method: {connection['test_method']}")
    else:
        print(f"🔗 Connection: ❌ Failed - {connection.get('error', 'Unknown')}")
    
    # Check configurations
    configs = checker.check_ide_configurations()
    print("\n💻 IDE Configurations:")
    for ide, config in configs.items():
        if config.get('exists'):
            size = config.get('size', 0)
            valid = config.get('valid_json', False)
            status = "✅" if valid else "⚠️"
            print(f"   {status} {ide.upper()}: {size} bytes")
        else:
            print(f"   ❌ {ide.upper()}: Not configured")
    
    return 0 if server_running else 1

if __name__ == "__main__":
    sys.exit(main())
```

## 🐳 Docker Script Examples

### Docker Environment Detection Script
```python
# Example: Docker environment detection script
#!/usr/bin/env python3
"""
Docker Environment Detection Script
Detect and configure Docker environment for MCP server
"""

import os
import subprocess
import json
from pathlib import Path

def detect_docker_environment():
    """Detect if running in Docker environment"""
    methods = []
    
    # Method 1: Check /.dockerenv file
    if Path("/.dockerenv").exists():
        methods.append("/.dockerenv file")
    
    # Method 2: Check cgroup
    try:
        with open("/proc/1/cgroup", "r") as f:
            if "docker" in f.read():
                methods.append("cgroup contains docker")
    except FileNotFoundError:
        pass
    
    # Method 3: Check environment variable
    if os.environ.get("DOCKER_CONTAINER") == "true":
        methods.append("DOCKER_CONTAINER environment variable")
    
    return len(methods) > 0, methods

def test_docker_mcp_ping():
    """Test MCP server ping in Docker"""
    try:
        ping_request = '{"method": "neozork/ping", "id": 1, "params": {}}'
        cmd = f'echo \'{ping_request}\' | python3 neozork_mcp_server.py'
        
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
                return True, "Ping successful"
            else:
                return False, "Invalid response format"
        else:
            return False, "No response received"
            
    except subprocess.TimeoutExpired:
        return False, "Request timed out"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Main Docker detection function"""
    print("🐳 Docker Environment Detection")
    print("=" * 40)
    
    # Detect Docker environment
    in_docker, methods = detect_docker_environment()
    
    if in_docker:
        print("✅ Running in Docker environment")
        print(f"   Detection methods: {', '.join(methods)}")
        
        # Test MCP server
        ping_success, ping_message = test_docker_mcp_ping()
        if ping_success:
            print("✅ MCP server ping successful")
        else:
            print(f"❌ MCP server ping failed: {ping_message}")
    else:
        print("❌ Not running in Docker environment")
    
    return 0 if in_docker else 1

if __name__ == "__main__":
    main()
```

### Docker Container Management Script
```python
# Example: Docker container management script
#!/usr/bin/env python3
"""
Docker Container Management Script
Manage Docker containers for MCP server development
"""

import subprocess
import sys
import json
from pathlib import Path

def run_docker_command(cmd, capture_output=True):
    """Run Docker command and return result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=capture_output,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def build_docker_image():
    """Build Docker image"""
    print("🔨 Building Docker image...")
    success, stdout, stderr = run_docker_command("docker-compose build")
    
    if success:
        print("✅ Docker image built successfully")
    else:
        print(f"❌ Docker build failed: {stderr}")
    
    return success

def run_docker_container():
    """Run Docker container"""
    print("🚀 Running Docker container...")
    success, stdout, stderr = run_docker_command("docker-compose run --rm app python scripts/check_mcp_status.py")
    
    if success:
        print("✅ Docker container ran successfully")
        print(stdout)
    else:
        print(f"❌ Docker container failed: {stderr}")
    
    return success

def check_docker_status():
    """Check Docker container status"""
    print("📊 Checking Docker container status...")
    success, stdout, stderr = run_docker_command("docker ps -a")
    
    if success:
        print("✅ Docker containers:")
        print(stdout)
    else:
        print(f"❌ Failed to check Docker status: {stderr}")
    
    return success

def main():
    """Main Docker management function"""
    print("🐳 Docker Container Management")
    print("=" * 40)
    
    if len(sys.argv) < 2:
        print("Usage: python docker_manage.py [build|run|status]")
        return 1
    
    command = sys.argv[1]
    
    if command == "build":
        return 0 if build_docker_image() else 1
    elif command == "run":
        return 0 if run_docker_container() else 1
    elif command == "status":
        return 0 if check_docker_status() else 1
    else:
        print(f"❌ Unknown command: {command}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

## 🔧 Configuration Script Examples

### IDE Configuration Validation Script
```python
# Example: IDE configuration validation script
#!/usr/bin/env python3
"""
IDE Configuration Validation Script
Validate IDE configuration files for MCP server
"""

import json
import sys
from pathlib import Path

def validate_json_config(config_path):
    """Validate JSON configuration file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check for required MCP server configuration
        if "mcpServers" in config:
            if "neozork" in config["mcpServers"]:
                server_config = config["mcpServers"]["neozork"]
                if "command" in server_config and "args" in server_config:
                    return True, "Valid MCP server configuration"
                else:
                    return False, "Missing command or args in MCP server configuration"
            else:
                return False, "Missing neozork MCP server configuration"
        else:
            return False, "Missing mcpServers section"
            
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"

def validate_env_config(config_path):
    """Validate environment configuration file"""
    try:
        with open(config_path, 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' not in line:
                    return False, f"Invalid format at line {line_num}: {line}"
        
        return True, "Valid environment file format"
        
    except Exception as e:
        return False, f"Error reading file: {e}"

def main():
    """Main validation function"""
    print("🔧 IDE Configuration Validation")
    print("=" * 40)
    
    configs = {
        'cursor': ('cursor_mcp_config.json', validate_json_config),
        'vscode': ('.vscode/settings.json', validate_json_config),
        'pycharm': ('pycharm_mcp_config.json', validate_json_config),
        'docker': ('docker.env', validate_env_config)
    }
    
    all_valid = True
    
    for ide, (config_path, validator) in configs.items():
        config_file = Path(config_path)
        
        if config_file.exists():
            valid, message = validator(config_file)
            status = "✅" if valid else "❌"
            print(f"{status} {ide.upper()}: {message}")
            
            if not valid:
                all_valid = False
        else:
            print(f"⚠️  {ide.upper()}: File not found")
    
    return 0 if all_valid else 1

if __name__ == "__main__":
    sys.exit(main())
```

## 📊 Monitoring Script Examples

### Real-time MCP Monitoring Script
```python
# Example: Real-time MCP monitoring script
#!/usr/bin/env python3
"""
Real-time MCP Server Monitoring Script
Monitor MCP server status in real-time
"""

import time
import sys
from scripts.check_mcp_status import is_running_in_docker, DockerMCPServerChecker, MCPServerChecker

def monitor_mcp_server(interval=30, max_checks=None):
    """Monitor MCP server status in real-time"""
    print(f"🔍 Starting real-time MCP monitoring (check every {interval}s)")
    print("Press Ctrl+C to stop")
    
    if is_running_in_docker():
        checker = DockerMCPServerChecker()
        env_name = "Docker"
    else:
        checker = MCPServerChecker()
        env_name = "Host"
    
    check_count = 0
    
    try:
        while True:
            if max_checks and check_count >= max_checks:
                print(f"\n🛑 Reached maximum checks ({max_checks})")
                break
            
            # Check server status
            server_running = checker.check_server_running()
            status = "✅ Running" if server_running else "❌ Not Running"
            
            timestamp = time.strftime("%H:%M:%S")
            check_count += 1
            
            print(f"[{timestamp}] {env_name} MCP Server: {status} (check #{check_count})")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Monitoring stopped after {check_count} checks")
    
    return check_count

def main():
    """Main monitoring function"""
    print("📊 Real-time MCP Server Monitoring")
    print("=" * 40)
    
    # Parse command line arguments
    interval = 30
    max_checks = None
    
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except ValueError:
            print(f"❌ Invalid interval: {sys.argv[1]}")
            return 1
    
    if len(sys.argv) > 2:
        try:
            max_checks = int(sys.argv[2])
        except ValueError:
            print(f"❌ Invalid max checks: {sys.argv[2]}")
            return 1
    
    # Start monitoring
    check_count = monitor_mcp_server(interval, max_checks)
    
    print(f"📈 Monitoring completed: {check_count} checks performed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Performance Monitoring Script
```python
# Example: Performance monitoring script
#!/usr/bin/env python3
"""
Performance Monitoring Script
Monitor MCP server performance metrics
"""

import time
import statistics
from scripts.check_mcp_status import is_running_in_docker, DockerMCPServerChecker, MCPServerChecker

def measure_detection_performance(checker, iterations=10):
    """Measure detection performance"""
    times = []
    
    for i in range(iterations):
        start_time = time.time()
        checker.check_server_running()
        end_time = time.time()
        
        detection_time = (end_time - start_time) * 1000  # Convert to milliseconds
        times.append(detection_time)
        
        print(f"  Check {i+1}: {detection_time:.2f}ms")
    
    return times

def analyze_performance(times):
    """Analyze performance metrics"""
    if not times:
        return {}
    
    return {
        'count': len(times),
        'min': min(times),
        'max': max(times),
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'std': statistics.stdev(times) if len(times) > 1 else 0
    }

def main():
    """Main performance monitoring function"""
    print("⚡ MCP Server Performance Monitoring")
    print("=" * 40)
    
    if is_running_in_docker():
        checker = DockerMCPServerChecker()
        env_name = "Docker"
    else:
        checker = MCPServerChecker()
        env_name = "Host"
    
    print(f"🌍 Environment: {env_name}")
    print(f"🔍 Running performance tests...")
    
    # Measure detection performance
    times = measure_detection_performance(checker, iterations=10)
    
    # Analyze results
    metrics = analyze_performance(times)
    
    print(f"\n📊 Performance Metrics:")
    print(f"   Count: {metrics['count']}")
    print(f"   Min: {metrics['min']:.2f}ms")
    print(f"   Max: {metrics['max']:.2f}ms")
    print(f"   Mean: {metrics['mean']:.2f}ms")
    print(f"   Median: {metrics['median']:.2f}ms")
    print(f"   Std Dev: {metrics['std']:.2f}ms")
    
    # Performance assessment
    mean_time = metrics['mean']
    if mean_time < 100:
        assessment = "✅ Excellent"
    elif mean_time < 500:
        assessment = "✅ Good"
    elif mean_time < 1000:
        assessment = "⚠️  Acceptable"
    else:
        assessment = "❌ Poor"
    
    print(f"\n📈 Performance Assessment: {assessment}")
    
    return 0

if __name__ == "__main__":
    main()
```

## 🔄 Migration Script Examples

### Migration Helper Script
```python
# Example: Migration helper script
#!/usr/bin/env python3
"""
Migration Helper Script
Help migrate from old to new MCP server detection
"""

import subprocess
import sys
from scripts.check_mcp_status import is_running_in_docker, DockerMCPServerChecker, MCPServerChecker

def test_old_detection_method():
    """Test old detection method"""
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'neozork_mcp_server.py'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0, "Process found" if result.returncode == 0 else "Process not found"
    except Exception as e:
        return False, f"Error: {e}"

def test_new_detection_method():
    """Test new detection method"""
    try:
        if is_running_in_docker():
            checker = DockerMCPServerChecker()
        else:
            checker = MCPServerChecker()
        
        result = checker.check_server_running()
        return result, "Server responding" if result else "Server not responding"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Main migration function"""
    print("🔄 MCP Server Detection Migration Helper")
    print("=" * 40)
    
    # Test old method
    print("🔍 Testing old detection method...")
    old_success, old_message = test_old_detection_method()
    old_status = "✅" if old_success else "❌"
    print(f"{old_status} Old method: {old_message}")
    
    # Test new method
    print("🔍 Testing new detection method...")
    new_success, new_message = test_new_detection_method()
    new_status = "✅" if new_success else "❌"
    print(f"{new_status} New method: {new_message}")
    
    # Compare results
    print(f"\n📊 Comparison:")
    if old_success == new_success:
        print("✅ Both methods agree")
    else:
        print("⚠️  Methods disagree - new method is more reliable")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if is_running_in_docker():
        print("   • Use new ping-based detection in Docker")
        print("   • Old process-based detection is unreliable in Docker")
    else:
        print("   • Both methods work in host environment")
        print("   • New method provides better error handling")
    
    print("   • New method automatically detects environment")
    print("   • New method tests actual functionality")
    
    return 0

if __name__ == "__main__":
    main()
```

## 📚 Related Examples

- **[MCP Examples](mcp-examples.md)** - MCP server examples
- **[Docker Examples](docker-examples.md)** - Docker script examples
- **[Testing Examples](testing-examples.md)** - Script testing examples

## 🔄 Script Migration Examples

### From Old to New Script Framework
```python
# Example: Migration from old to new script framework
def migrate_script_framework():
    """Example of migrating from old to new script framework"""
    
    # Old script (unreliable in Docker)
    def old_script():
        try:
            result = subprocess.run(['pgrep', '-f', 'neozork_mcp_server.py'])
            return result.returncode == 0
        except:
            return False
    
    # New script (reliable in all environments)
    def new_script():
        from scripts.check_mcp_status import is_running_in_docker
        
        if is_running_in_docker():
            checker = DockerMCPServerChecker()
        else:
            checker = MCPServerChecker()
        
        return checker.check_server_running()
    
    # Both should work, but new one is more reliable
    old_result = old_script()
    new_result = new_script()
    
    # New method should always return a boolean
    assert isinstance(new_result, bool)
    
    print("🔄 Script migration completed")
    print("✅ New script framework is more reliable")
    print("✅ Works in all environments")
    print("✅ Better error handling")
``` 