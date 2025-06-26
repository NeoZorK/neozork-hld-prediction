# Docker Examples

Examples demonstrating Docker containerization and MCP server integration in the NeoZork HLD Prediction project.

## Overview

The project includes Docker support for:

- **Containerized Development** - Consistent development environment
- **Production Deployment** - Scalable deployment options
- **Data Mounting** - Persistent data storage
- **Multi-stage Builds** - Optimized container images
- **Service Orchestration** - Docker Compose integration

## 🚀 Quick Start Examples

### Basic Docker Setup
```bash
# Build Docker image with UV package manager (recommended)
docker-compose build --build-arg USE_UV=true

# Build with pip package manager
docker-compose build --build-arg USE_UV=false

# Run container interactively
docker-compose run --rm app bash

# Run container with specific command
docker-compose run --rm app python scripts/check_mcp_status.py
```

### MCP Server in Docker
```bash
# Check MCP server status in Docker container
docker-compose run --rm app python scripts/check_mcp_status.py

# Expected output:
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
```

## 🐳 Docker Environment Examples

### Docker Container MCP Check
```bash
# Build and run Docker container
docker-compose build
docker-compose run --rm app bash

# Inside container, check MCP server
python scripts/check_mcp_status.py

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

## 🔧 Docker Configuration Examples

### Dockerfile Configuration
```dockerfile
# Example: Dockerfile with MCP server support
FROM python:3.12-slim

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV DOCKER_CONTAINER=true

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy docker.env file for environment configuration
COPY docker.env .

# Make scripts executable
RUN chmod +x scripts/*.py

# Expose port (if needed)
EXPOSE 8000

# Default command
CMD ["python", "neozork_mcp_server.py"]
```

### Docker Compose Configuration
```yaml
# Example: docker-compose.yml with MCP server support
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        USE_UV: "true"  # Use UV package manager
    environment:
      - PYTHONPATH=/app
      - PYTHONUNBUFFERED=1
      - DOCKER_CONTAINER=true
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./results:/app/results
    working_dir: /app
    command: python scripts/check_mcp_status.py
```

### Environment Configuration
```bash
# Example: docker.env file
PYTHONPATH=/app
PYTHONUNBUFFERED=1
DOCKER_CONTAINER=true
MCP_SERVER_ENABLED=true
LOG_LEVEL=INFO
```

## 📊 Docker Status Monitoring

### Comprehensive Docker Status Check
```python
# Example: Comprehensive Docker status monitoring
def monitor_docker_mcp_status():
    """Monitor MCP server status in Docker environment"""
    from scripts.check_mcp_status import DockerMCPServerChecker
    
    checker = DockerMCPServerChecker()
    results = checker.run_comprehensive_check()
    
    # Print Docker-specific information
    print(f"🐳 Docker Environment Status")
    print(f"📅 Check Time: {results['timestamp']}")
    print(f"🌍 Environment: {results['environment']}")
    print(f"🚀 Server Status: {'✅ Running' if results['server_running'] else '❌ Not Running'}")
    
    # Print Docker-specific details
    if results.get("docker_specific"):
        docker_info = results["docker_specific"]
        print(f"\n🐳 Docker Information:")
        print(f"   📦 In Docker: {docker_info.get('in_docker', 'Unknown')}")
        print(f"   🔄 MCP Server responding: {docker_info.get('mcp_server_responding', False)}")
        print(f"   🔍 Test method: {docker_info.get('test_method', 'unknown')}")
        
        # MCP server file info
        if docker_info.get('mcp_server_file_exists'):
            print(f"   📄 MCP server file: {docker_info.get('mcp_server_file_size', 0)} bytes")
            print(f"   🕒 File modified: {docker_info.get('mcp_server_file_modified', 'Unknown')}")
        else:
            print(f"   ❌ MCP server file: Not found")
        
        # Log file info
        if docker_info.get('log_file_exists'):
            print(f"   📝 Log file: {docker_info.get('log_file_size', 0)} bytes")
            print(f"   🕒 Log modified: {docker_info.get('log_file_modified', 'Unknown')}")
        else:
            print(f"   ❌ Log file: Not found")
    
    return results
```

### Real-time Docker Monitoring
```python
# Example: Real-time Docker monitoring
import time
from scripts.check_mcp_status import DockerMCPServerChecker

def monitor_docker_realtime(interval=30):
    """Monitor MCP server in Docker in real-time"""
    print(f"🐳 Starting real-time Docker MCP monitoring (check every {interval}s)")
    print("Press Ctrl+C to stop")
    
    checker = DockerMCPServerChecker()
    
    try:
        while True:
            # Quick status check
            server_running = checker.check_server_running()
            status = "✅ Running" if server_running else "❌ Not Running"
            
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] Docker MCP Server: {status}")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n🛑 Docker monitoring stopped")
```

## 🧪 Docker Testing Examples

### Docker Unit Tests
```python
# Example: Docker unit tests
import pytest
from scripts.check_mcp_status import DockerMCPServerChecker

def test_docker_environment_detection():
    """Test Docker environment detection"""
    checker = DockerMCPServerChecker()
    assert checker._is_running_in_docker() == True

def test_docker_ping_detection():
    """Test ping-based detection in Docker"""
    checker = DockerMCPServerChecker()
    result = checker._test_mcp_ping_request()
    assert isinstance(result, bool)

def test_docker_comprehensive_check():
    """Test comprehensive Docker check"""
    checker = DockerMCPServerChecker()
    results = checker.run_comprehensive_check()
    
    # Validate results structure
    assert "timestamp" in results
    assert results["environment"] == "docker"
    assert "server_running" in results
    assert "docker_specific" in results
    
    # Validate Docker-specific information
    docker_info = results["docker_specific"]
    assert "in_docker" in docker_info
    assert "mcp_server_responding" in docker_info
    assert "test_method" in docker_info
```

### Docker Integration Tests
```python
# Example: Docker integration tests
def test_docker_mcp_integration():
    """Test complete Docker MCP integration"""
    from scripts.check_mcp_status import DockerMCPServerChecker
    
    checker = DockerMCPServerChecker()
    
    # Test environment detection
    assert checker._is_running_in_docker() == True
    
    # Test server detection
    server_running = checker.check_server_running()
    assert isinstance(server_running, bool)
    
    # Test connection
    connection = checker.test_connection()
    assert "status" in connection
    assert connection["status"] in ["success", "failed"]
    
    # Test comprehensive check
    results = checker.run_comprehensive_check()
    assert results["environment"] == "docker"
    assert "docker_specific" in results
```

## 🔍 Docker Debug Examples

### Debug Docker MCP Issues
```python
# Example: Debug Docker MCP issues
def debug_docker_mcp():
    """Debug MCP server issues in Docker"""
    import subprocess
    import json
    from pathlib import Path
    
    print("🔍 Debugging Docker MCP server...")
    
    # Check if we're in Docker
    if not Path("/.dockerenv").exists():
        print("❌ Not running in Docker environment")
        return
    
    print("✅ Running in Docker environment")
    
    # Check if MCP server file exists
    mcp_file = Path("/app/neozork_mcp_server.py")
    if mcp_file.exists():
        print(f"✅ MCP server file exists: {mcp_file.stat().st_size} bytes")
    else:
        print("❌ MCP server file not found")
        return
    
    # Test ping request with detailed output
    ping_request = '{"method": "neozork/ping", "id": 1, "params": {}}'
    cmd = f'echo \'{ping_request}\' | python3 /app/neozork_mcp_server.py'
    
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

### Docker Container Inspection
```bash
# Example: Inspect Docker container
# Check container status
docker ps -a

# Check container logs
docker logs <container_name>

# Execute command in running container
docker exec -it <container_name> bash

# Check environment variables
docker exec <container_name> env | grep -E "(PYTHON|DOCKER|MCP)"

# Check file system
docker exec <container_name> ls -la /app/

# Check MCP server file
docker exec <container_name> ls -la /app/neozork_mcp_server.py

# Test MCP server directly
docker exec <container_name> echo '{"method": "neozork/ping", "id": 1, "params": {}}' | python3 /app/neozork_mcp_server.py
```

## 📚 Related Examples

- **[MCP Examples](mcp-examples.md)** - MCP server examples
- **[Testing Examples](testing-examples.md)** - Test framework examples
- **[Script Examples](script-examples.md)** - Utility script examples

## 🔄 Migration Examples

### From Old to New Docker Detection
```python
# Example: Migration from old Docker detection logic
def migrate_docker_detection():
    """Example of migrating from old to new Docker detection logic"""
    
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
    
    # New logic (reliable in Docker)
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
    
    print("🔄 Docker detection migration completed")
    print("✅ New detection logic is more reliable")
    print("✅ Works with on-demand servers")
    print("✅ Tests actual functionality")
```

## Basic Docker Commands

### Build and Run
```bash
# Build and run container
docker compose up --build

# Build without cache
docker compose build --no-cache

# Run in detached mode
docker compose up -d

# Stop containers
docker compose down

# View logs
docker compose logs neozork-hld
```

### Interactive Sessions
```bash
# Interactive session in container
docker compose run --rm neozork-hld bash

# Run with specific user
docker compose run --rm -u $(id -u):$(id -g) neozork-hld bash

# Run with environment variables
docker compose run --rm -e DEBUG=1 neozork-hld bash

# Run with working directory
docker compose run --rm -w /app/src neozork-hld bash
```

## Data Analysis in Docker

### Demo Analysis
```bash
# Run demo in container
docker compose run --rm neozork-hld python run_analysis.py demo

# Demo with specific indicator
docker compose run --rm neozork-hld python run_analysis.py demo --rule RSI

# Demo with different backends
docker compose run --rm neozork-hld python run_analysis.py demo -d plotly
docker compose run --rm neozork-hld python run_analysis.py demo -d seaborn
docker compose run --rm neozork-hld python run_analysis.py demo -d term
```

### Real Data Analysis
```bash
# Yahoo Finance analysis
docker compose run --rm neozork-hld python run_analysis.py yf -t AAPL --period 1mo --point 0.01

# CSV analysis
docker compose run --rm neozork-hld python run_analysis.py csv --csv-file data.csv --point 0.01

# Binance analysis
docker compose run --rm neozork-hld python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01
```

### Interactive Mode
```bash
# Interactive mode in container
docker compose run --rm neozork-hld python run_analysis.py --interactive

# Interactive mode with alias
docker compose run --rm neozork-hld nz --interactive
```

## Data Mounting

### Mount Data Directory
```bash
# Mount data directory
docker compose run --rm -v $(pwd)/data:/app/data neozork-hld python run_analysis.py csv --csv-file data.csv

# Mount with read-only
docker compose run --rm -v $(pwd)/data:/app/data:ro neozork-hld python run_analysis.py csv --csv-file data.csv

# Mount specific files
docker compose run --rm -v $(pwd)/data/file.csv:/app/data/file.csv neozork-hld python run_analysis.py csv --csv-file data/file.csv
```

### Mount Results Directory
```bash
# Mount results directory
docker compose run --rm -v $(pwd)/results:/app/results neozork-hld python run_analysis.py demo --export-parquet

# Mount with custom permissions
docker compose run --rm -v $(pwd)/results:/app/results:rw neozork-hld python run_analysis.py demo --export-parquet

# Mount multiple directories
docker compose run --rm -v $(pwd)/data:/app/data -v $(pwd)/results:/app/results neozork-hld python run_analysis.py demo --export-parquet
```

### Mount Configuration
```bash
# Mount configuration files
docker compose run --rm -v $(pwd)/config:/app/config neozork-hld python run_analysis.py demo

# Mount with environment variables
docker compose run --rm -v $(pwd)/config:/app/config -e CONFIG_PATH=/app/config neozork-hld python run_analysis.py demo
```

## Testing in Docker

### Run Tests
```bash
# Run all tests in container
docker compose run --rm neozork-hld python -m pytest tests/

# Run specific test categories
docker compose run --rm neozork-hld python -m pytest tests/calculation/ -v
docker compose run --rm neozork-hld python -m pytest tests/cli/ -v
docker compose run --rm neozork-hld python -m pytest tests/data/ -v

# Run with coverage
docker compose run --rm neozork-hld python -m pytest tests/ --cov=src --cov-report=html
```

### Test Coverage Analysis
```bash
# Analyze test coverage in container
docker compose run --rm neozork-hld python tests/zzz_analyze_test_coverage.py

# Analyze with verbose output
docker compose run --rm neozork-hld python tests/zzz_analyze_test_coverage.py --verbose
```

### MCP Server Testing
```bash
# Test stdio mode in container
docker compose run --rm neozork-hld python tests/test_stdio.py

# Test MCP functionality
docker compose run --rm neozork-hld python -m pytest tests/mcp/ -v
```

## MCP Servers in Docker

### Auto-start MCP Servers
```bash
# Start MCP servers in container
docker compose run --rm neozork-hld python scripts/auto_start_mcp.py

# Start with configuration
docker compose run --rm neozork-hld python scripts/auto_start_mcp.py --config mcp_auto_config.json

# Start in debug mode
docker compose run --rm neozork-hld python scripts/auto_start_mcp.py --debug

# Show server status
docker compose run --rm neozork-hld python scripts/auto_start_mcp.py --status
```

### Manual MCP Server Management
```bash
# Start PyCharm GitHub Copilot MCP server
docker compose run --rm neozork-hld python pycharm_github_copilot_mcp.py

# Start with stdio mode
docker compose run --rm neozork-hld python pycharm_github_copilot_mcp.py --stdio

# Start with debug logging
docker compose run --rm neozork-hld python pycharm_github_copilot_mcp.py --debug
```

## Scripts in Docker

### Utility Scripts
```bash
# Fix imports in container
docker compose run --rm neozork-hld python scripts/fix_imports.py

# Create test data in container
docker compose run --rm neozork-hld python scripts/create_test_parquet.py

# Analyze requirements in container
docker compose run --rm neozork-hld python scripts/analyze_requirements.py
```

### Debug Scripts
```bash
# Debug Binance connection in container
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_binance_connection.py

# Check Parquet files in container
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_check_parquet.py

# Debug indicators in container
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_indicators.py

# Debug CLI in container
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_cli.py
```

## EDA in Docker

### Basic EDA
```bash
# Run EDA script in container
docker compose run --rm neozork-hld bash eda

# EDA with UV in container
docker compose run --rm neozork-hld uv run ./eda

# EDA with verbose output
docker compose run --rm neozork-hld bash eda --verbose

# EDA with export results
docker compose run --rm neozork-hld bash eda --export-results
```

### EDA with Data Mounting
```bash
# EDA with mounted data
docker compose run --rm -v $(pwd)/data:/app/data neozork-hld bash eda

# EDA with mounted results
docker compose run --rm -v $(pwd)/results:/app/results neozork-hld bash eda --export-results
```

## Performance Optimization

### Resource Limits
```bash
# Run with memory limit
docker compose run --rm --memory=2g neozork-hld python run_analysis.py demo

# Run with CPU limit
docker compose run --rm --cpus=2 neozork-hld python run_analysis.py demo

# Run with both limits
docker compose run --rm --memory=2g --cpus=2 neozork-hld python run_analysis.py demo
```

### Fastest Backend
```bash
# Use fastest backend for large datasets
docker compose run --rm neozork-hld python run_analysis.py demo -d fastest

# Use terminal backend for SSH/Docker
docker compose run --rm neozork-hld python run_analysis.py demo -d term
```

## Multi-stage Builds

### Development Build
```bash
# Build development image
docker build -f Dockerfile.dev -t neozork-hld:dev .

# Run development image
docker run --rm -v $(pwd):/app neozork-hld:dev python run_analysis.py demo
```

### Production Build
```bash
# Build production image
docker build -f Dockerfile.prod -t neozork-hld:prod .

# Run production image
docker run --rm neozork-hld:prod python run_analysis.py demo
```

## Docker Compose Services

### Multiple Services
```yaml
# docker-compose.yml example
version: '3.8'
services:
  neozork-hld:
    build: .
    volumes:
      - ./data:/app/data
      - ./results:/app/results
    environment:
      - DEBUG=0
    ports:
      - "8000:8000"
  
  mcp-server:
    build: .
    command: python scripts/auto_start_mcp.py
    volumes:
      - ./config:/app/config
    environment:
      - MCP_DEBUG=1
```

### Service Orchestration
```bash
# Start all services
docker compose up -d

# Start specific service
docker compose up -d neozork-hld

# Scale services
docker compose up -d --scale neozork-hld=3

# View service logs
docker compose logs -f neozork-hld
```

## Environment Variables

### Development Environment
```bash
# Run with development environment
docker compose run --rm -e ENV=development neozork-hld python run_analysis.py demo

# Run with debug mode
docker compose run --rm -e DEBUG=1 neozork-hld python run_analysis.py demo

# Run with custom configuration
docker compose run --rm -e CONFIG_PATH=/app/config neozork-hld python run_analysis.py demo
```

### Production Environment
```bash
# Run with production environment
docker compose run --rm -e ENV=production neozork-hld python run_analysis.py demo

# Run with optimized settings
docker compose run --rm -e OPTIMIZE=1 neozork-hld python run_analysis.py demo

# Run with logging configuration
docker compose run --rm -e LOG_LEVEL=INFO neozork-hld python run_analysis.py demo
```

## Networking

### Port Mapping
```bash
# Map specific port
docker compose run --rm -p 8000:8000 neozork-hld python run_analysis.py demo

# Map multiple ports
docker compose run --rm -p 8000:8000 -p 8080:8080 neozork-hld python run_analysis.py demo
```

### Network Configuration
```bash
# Use specific network
docker compose run --rm --network=host neozork-hld python run_analysis.py demo

# Create custom network
docker network create neozork-network
docker compose run --rm --network=neozork-network neozork-hld python run_analysis.py demo
```

## Troubleshooting

### Common Issues
```bash
# Issue: Permission denied
docker compose run --rm -u $(id -u):$(id -g) neozork-hld python run_analysis.py demo

# Issue: Container not starting
docker compose logs neozork-hld
docker compose run --rm neozork-hld bash

# Issue: Data not persisting
docker compose run --rm -v $(pwd)/data:/app/data:rw neozork-hld python run_analysis.py demo

# Issue: Memory problems
docker compose run --rm --memory=4g neozork-hld python run_analysis.py demo
```

### Debug Mode
```bash
# Run with debug output
docker compose run --rm -e DEBUG=1 neozork-hld python run_analysis.py demo

# Run with verbose logging
docker compose run --rm -e VERBOSE=1 neozork-hld python run_analysis.py demo

# Run with shell access
docker compose run --rm neozork-hld bash
```

### Container Inspection
```bash
# Inspect running container
docker compose ps
docker inspect $(docker compose ps -q neozork-hld)

# Check container resources
docker stats $(docker compose ps -q neozork-hld)

# Check container logs
docker compose logs -f neozork-hld
```

## Advanced Usage

### Custom Dockerfile
```dockerfile
# Custom Dockerfile example
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV DEBUG=0

# Expose port
EXPOSE 8000

# Default command
CMD ["python", "run_analysis.py", "demo"]
```

### Docker Compose Override
```yaml
# docker-compose.override.yml
version: '3.8'
services:
  neozork-hld:
    volumes:
      - ./data:/app/data
      - ./results:/app/results
    environment:
      - DEBUG=1
    ports:
      - "8000:8000"
```

### Health Checks
```yaml
# Health check configuration
services:
  neozork-hld:
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

📚 **Additional Resources:**
- **[Usage Examples](usage-examples.md)** - Comprehensive usage examples
- **[Quick Examples](quick-examples.md)** - Fast start examples
- **[Indicator Examples](indicator-examples.md)** - Technical indicator examples
- **[MCP Examples](mcp-examples.md)** - MCP server examples
- **[Testing Examples](testing-examples.md)** - Testing examples
- **[Script Examples](script-examples.md)** - Utility script examples
- **[EDA Examples](eda-examples.md)** - EDA examples 