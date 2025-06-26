# Testing Examples

## Overview

Examples demonstrating the comprehensive testing framework for the NeoZork HLD Prediction project, including MCP server detection testing.

## 🚀 Quick Start Examples

### Run All Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test categories
pytest tests/mcp/ -v  # MCP server tests
pytest tests/scripts/ -v  # Script tests
pytest tests/docker/ -v  # Docker tests
```

### MCP Server Detection Tests
```bash
# Test MCP server detection
pytest tests/scripts/test_check_mcp_status.py -v

# Test MCP server functionality
pytest tests/mcp/ -v

# Test IDE configurations
pytest tests/docker/test_ide_configs.py -v
```

## 🧪 MCP Server Testing Examples

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

### Docker Environment Tests
```python
# Example: Docker environment tests
def test_docker_environment_detection():
    """Test Docker environment detection"""
    checker = DockerMCPServerChecker()
    assert checker._is_running_in_docker() == True

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

### Host Environment Tests
```python
# Example: Host environment tests
def test_host_environment_detection():
    """Test host environment detection"""
    checker = MCPServerChecker()
    # Note: This test may fail if not running in host environment
    # In Docker, this would be skipped or mocked
    
def test_host_server_management():
    """Test host server management"""
    checker = MCPServerChecker()
    
    # Test server start/stop (if not in Docker)
    if not is_running_in_docker():
        # Start server
        started = checker.start_server()
        assert isinstance(started, bool)
        
        # Stop server
        checker.stop_server()
```

## 🔧 Configuration Testing Examples

### IDE Configuration Tests
```python
# Example: Test IDE configurations
def test_ide_configurations():
    """Test IDE configuration validation"""
    from scripts.check_mcp_status import is_running_in_docker
    
    if is_running_in_docker():
        checker = DockerMCPServerChecker()
    else:
        checker = MCPServerChecker()
    
    configs = checker.check_ide_configurations()
    
    # Validate configuration structure
    assert isinstance(configs, dict)
    
    # Check for expected IDE configurations
    expected_configs = ['cursor', 'docker']
    if not is_running_in_docker():
        expected_configs.extend(['vscode', 'pycharm'])
    
    for ide in expected_configs:
        assert ide in configs
        config = configs[ide]
        assert "exists" in config
        if config["exists"]:
            assert "size" in config
            assert "valid_json" in config
```

### Configuration File Tests
```python
# Example: Test configuration file validation
def test_config_file_validation():
    """Test configuration file validation"""
    import json
    from pathlib import Path
    
    # Test Cursor configuration
    cursor_config = Path("cursor_mcp_config.json")
    if cursor_config.exists():
        with open(cursor_config, 'r') as f:
            content = f.read()
            # Should be valid JSON
            config = json.loads(content)
            assert "mcpServers" in config
            assert "neozork" in config["mcpServers"]
    
    # Test Docker configuration
    docker_config = Path("docker.env")
    if docker_config.exists():
        with open(docker_config, 'r') as f:
            content = f.read()
            # Should be valid environment file format
            lines = content.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    assert '=' in line
```

## 📊 Status Monitoring Tests

### Status Check Tests
```python
# Example: Test status monitoring
def test_status_monitoring():
    """Test status monitoring functionality"""
    from scripts.check_mcp_status import is_running_in_docker
    
    if is_running_in_docker():
        checker = DockerMCPServerChecker()
    else:
        checker = MCPServerChecker()
    
    # Test comprehensive status check
    results = checker.run_comprehensive_check()
    
    # Validate status structure
    assert "timestamp" in results
    assert "environment" in results
    assert "server_running" in results
    assert "connection_test" in results
    assert "ide_configurations" in results
    assert "recommendations" in results
    
    # Validate timestamp format
    import re
    timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
    assert re.match(timestamp_pattern, results["timestamp"])
    
    # Validate recommendations
    assert isinstance(results["recommendations"], list)
```

### Connection Test Tests
```python
# Example: Test connection functionality
def test_connection_testing():
    """Test connection testing functionality"""
    from scripts.check_mcp_status import is_running_in_docker
    
    if is_running_in_docker():
        checker = DockerMCPServerChecker()
    else:
        checker = MCPServerChecker()
    
    # Test connection
    connection = checker.test_connection()
    
    # Validate connection structure
    assert "status" in connection
    assert connection["status"] in ["success", "failed", "skipped"]
    
    if connection["status"] == "success":
        # Should have additional information
        if is_running_in_docker():
            assert "test_method" in connection
            assert connection["test_method"] == "ping_request"
        else:
            assert "pids" in connection
            assert isinstance(connection["pids"], list)
```

## 🐳 Docker-Specific Tests

### Docker Ping Tests
```python
# Example: Test Docker ping functionality
def test_docker_ping_functionality():
    """Test Docker ping functionality"""
    import subprocess
    import json
    
    # Only run in Docker environment
    if not is_running_in_docker():
        pytest.skip("Not running in Docker environment")
    
    # Test ping request
    ping_request = '{"method": "neozork/ping", "id": 1, "params": {}}'
    cmd = f'echo \'{ping_request}\' | python3 neozork_mcp_server.py'
    
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=10
    )
    
    # Validate response
    if result.returncode == 0 and result.stdout.strip():
        response = json.loads(result.stdout.strip())
        assert response.get("jsonrpc") == "2.0"
        assert response.get("id") == 1
        assert response.get("result", {}).get("pong") is True
    else:
        pytest.fail("Ping request failed")
```

### Docker Environment Tests
```python
# Example: Test Docker environment detection
def test_docker_environment_checks():
    """Test Docker environment detection methods"""
    from pathlib import Path
    import os
    
    # Test /.dockerenv file
    if Path("/.dockerenv").exists():
        assert is_running_in_docker() == True
    
    # Test cgroup method
    try:
        with open("/proc/1/cgroup", "r") as f:
            if "docker" in f.read():
                assert is_running_in_docker() == True
    except FileNotFoundError:
        pass
    
    # Test environment variable
    if os.environ.get("DOCKER_CONTAINER") == "true":
        assert is_running_in_docker() == True
```

## 🔍 Debug Testing Examples

### Debug Test Setup
```python
# Example: Debug test setup
import pytest
import logging

@pytest.fixture
def debug_logger():
    """Setup debug logging for tests"""
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger(__name__)

def test_with_debug_logging(debug_logger):
    """Test with debug logging"""
    debug_logger.debug("Starting test")
    
    # Your test code here
    result = some_function()
    
    debug_logger.debug(f"Test result: {result}")
    assert result is not None
```

### Mock Testing Examples
```python
# Example: Mock testing for MCP server
import pytest
from unittest.mock import patch, MagicMock

def test_mcp_server_with_mock():
    """Test MCP server with mocked subprocess"""
    with patch('subprocess.run') as mock_run:
        # Mock successful response
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"jsonrpc": "2.0", "id": 1, "result": {"pong": true}}'
        mock_run.return_value = mock_result
        
        checker = DockerMCPServerChecker()
        result = checker._test_mcp_ping_request()
        
        assert result == True
        mock_run.assert_called_once()

def test_mcp_server_timeout():
    """Test MCP server timeout handling"""
    with patch('subprocess.run') as mock_run:
        # Mock timeout
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="test", timeout=10)
        
        checker = DockerMCPServerChecker()
        result = checker._test_mcp_ping_request()
        
        assert result == False
```

## 📊 Performance Testing Examples

### Performance Test Examples
```python
# Example: Performance testing
import time
import pytest

def test_mcp_server_performance():
    """Test MCP server performance"""
    from scripts.check_mcp_status import is_running_in_docker
    
    if is_running_in_docker():
        checker = DockerMCPServerChecker()
    else:
        checker = MCPServerChecker()
    
    # Measure detection time
    start_time = time.time()
    server_running = checker.check_server_running()
    detection_time = time.time() - start_time
    
    # Should complete within reasonable time
    assert detection_time < 15.0  # 15 seconds max
    assert isinstance(server_running, bool)

def test_comprehensive_check_performance():
    """Test comprehensive check performance"""
    from scripts.check_mcp_status import is_running_in_docker
    
    if is_running_in_docker():
        checker = DockerMCPServerChecker()
    else:
        checker = MCPServerChecker()
    
    # Measure comprehensive check time
    start_time = time.time()
    results = checker.run_comprehensive_check()
    check_time = time.time() - start_time
    
    # Should complete within reasonable time
    assert check_time < 30.0  # 30 seconds max
    assert "timestamp" in results
```

## 🔄 Migration Testing Examples

### Migration Test Examples
```python
# Example: Test migration from old to new detection
def test_migration_compatibility():
    """Test compatibility with old detection methods"""
    from scripts.check_mcp_status import is_running_in_docker
    
    if is_running_in_docker():
        # Test new Docker detection
        checker = DockerMCPServerChecker()
        new_result = checker.check_server_running()
        
        # Old method would fail in Docker
        # New method should work
        assert isinstance(new_result, bool)
    else:
        # Test new host detection
        checker = MCPServerChecker()
        new_result = checker.check_server_running()
        
        # Both old and new methods should work on host
        assert isinstance(new_result, bool)
```

## 📚 Related Examples

- **[MCP Examples](mcp-examples.md)** - MCP server examples
- **[Docker Examples](docker-examples.md)** - Docker testing examples
- **[Script Examples](script-examples.md)** - Script testing examples

## 🔄 Test Migration Examples

### From Old to New Test Framework
```python
# Example: Migration from old test framework
def test_migration_example():
    """Example of migrating from old to new test framework"""
    
    # Old test (unreliable in Docker)
    def old_test():
        try:
            result = subprocess.run(['pgrep', '-f', 'neozork_mcp_server.py'])
            return result.returncode == 0
        except:
            return False
    
    # New test (reliable in all environments)
    def new_test():
        from scripts.check_mcp_status import is_running_in_docker
        
        if is_running_in_docker():
            checker = DockerMCPServerChecker()
        else:
            checker = MCPServerChecker()
        
        return checker.check_server_running()
    
    # Both should work, but new one is more reliable
    old_result = old_test()
    new_result = new_test()
    
    # New method should always return a boolean
    assert isinstance(new_result, bool)
    
    print("🔄 Test migration completed")
    print("✅ New test framework is more reliable")
    print("✅ Works in all environments")
``` 