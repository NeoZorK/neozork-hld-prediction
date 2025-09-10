#!/usr/bin/env python3
"""
Test MCP server functionality in Docker environment
"""

import os
import sys
import json
import subprocess
import time
import pytest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def is_running_in_docker():
    """Check if running inside Docker container"""
    return os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true'

class TestMCPServerDocker:
    """Test MCP server in Docker environment"""
    
    @pytest.mark.skipif(not is_running_in_docker(), reason="Only run in Docker environment")
    def test_mcp_server_file_exists(self):
        """Test that MCP server file exists"""
        mcp_server_path = project_root / "neozork_mcp_server.py"
        assert mcp_server_path.exists(), f"MCP server file not found at {mcp_server_path}"
    
    @pytest.mark.skipif(not is_running_in_docker(), reason="Only run in Docker environment")
    def test_mcp_server_importable(self):
        """Test that MCP server can be imported"""
        try:
            import neozork_mcp_server
            assert hasattr(neozork_mcp_server, 'NeozorkMCPServer')
        except ImportError as e:
            pytest.fail(f"Failed to import MCP server: {e}")
    
    @pytest.mark.skipif(not is_running_in_docker(), reason="Only run in Docker environment")
    def test_mcp_server_ping_request(self):
        """Test MCP server with ping request"""
        try:
            # Create ping request JSON
            ping_request = '{"method": "neozork/ping", "id": 1, "params": {}}'
            
            # Send request to MCP server
            cmd = f'echo \'{ping_request}\' | python3 neozork_mcp_server.py'
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=15,  # 15 second timeout
                cwd=str(project_root)
            )
            
            # Check if we got a response
            if result.returncode == 0 and result.stdout.strip():
                try:
                    response = json.loads(result.stdout.strip())
                    # Check if response contains expected ping response structure
                    assert response.get("jsonrpc") == "2.0"
                    assert response.get("id") == 1
                    assert response.get("result", {}).get("pong") is True
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON response: {result.stdout}")
            else:
                pytest.fail(f"MCP server did not respond. Return code: {result.returncode}, stderr: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            pytest.fail("MCP server ping request timed out")
        except Exception as e:
            pytest.fail(f"Error testing MCP ping request: {e}")
    
    @pytest.mark.skipif(not is_running_in_docker(), reason="Only run in Docker environment")
    def test_mcp_server_health_check(self):
        """Test MCP server health check"""
        try:
            # Create health check request JSON
            health_request = '{"method": "neozork/health", "id": 2, "params": {}}'
            
            # Send request to MCP server
            cmd = f'echo \'{health_request}\' | python3 neozork_mcp_server.py'
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=15,  # 15 second timeout
                cwd=str(project_root)
            )
            
            # Check if we got a response
            if result.returncode == 0 and result.stdout.strip():
                try:
                    response = json.loads(result.stdout.strip())
                    # Check if response contains expected health response structure
                    assert response.get("jsonrpc") == "2.0"
                    assert response.get("id") == 2
                    assert "result" in response
                    assert "status" in response["result"]
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON response: {result.stdout}")
            else:
                pytest.fail(f"MCP server did not respond to health check. Return code: {result.returncode}, stderr: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            pytest.fail("MCP server health check timed out")
        except Exception as e:
            pytest.fail(f"Error testing MCP health check: {e}")
    
    @pytest.mark.skipif(not is_running_in_docker(), reason="Only run in Docker environment")
    def test_mcp_server_initialization(self):
        """Test MCP server initialization"""
        try:
            # Create initialize request JSON
            init_request = '{"method": "initialize", "id": 3, "params": {"protocolVersion": "2024-11-05"}}'
            
            # Send request to MCP server
            cmd = f'echo \'{init_request}\' | python3 neozork_mcp_server.py'
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=15,  # 15 second timeout
                cwd=str(project_root)
            )
            
            # Check if we got a response
            if result.returncode == 0 and result.stdout.strip():
                try:
                    response = json.loads(result.stdout.strip())
                    # Check if response contains expected initialize response structure
                    assert response.get("jsonrpc") == "2.0"
                    assert response.get("id") == 3
                    assert "result" in response
                    assert "capabilities" in response["result"]
                    assert "serverInfo" in response["result"]
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON response: {result.stdout}")
            else:
                pytest.fail(f"MCP server did not respond to initialize. Return code: {result.returncode}, stderr: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            pytest.fail("MCP server initialize timed out")
        except Exception as e:
            pytest.fail(f"Error testing MCP initialize: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
