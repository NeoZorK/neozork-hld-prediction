#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test MCP Server Status Checker
Test the new Docker-specific ping-based detection logic
"""

import pytest
import json
import subprocess
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
import os

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from check_mcp_status import DockerMCPServerChecker, MCPServerChecker, is_running_in_docker


class TestDockerMCPServerChecker:
    """Test Docker MCP Server Checker with ping-based detection"""
    
    def setup_method(self):
        """Setup test environment"""
        self.project_root = Path(__file__).parent.parent.parent
        self.checker = DockerMCPServerChecker(self.project_root)
    
    @patch('subprocess.run')
    def test_test_mcp_ping_request_success(self, mock_run):
        """Test successful ping request to MCP server"""
        # Mock successful response
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"jsonrpc": "2.0", "id": 1, "result": {"pong": true, "timestamp": "2024-01-01T00:00:00"}}'
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Test ping request
        result = self.checker._test_mcp_ping_request()
        
        assert result is True
        mock_run.assert_called_once()
        
        # Check command
        call_args = mock_run.call_args
        assert "echo" in call_args[0][0]
        assert "neozork_mcp_server.py" in call_args[0][0]
        assert call_args[1]['timeout'] == 10
        assert call_args[1]['cwd'] == self.project_root
    
    @patch('subprocess.run')
    def test_test_mcp_ping_request_failure(self, mock_run):
        """Test failed ping request to MCP server"""
        # Mock failed response
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Error: No such file or directory"
        mock_run.return_value = mock_result
        
        # Test ping request
        result = self.checker._test_mcp_ping_request()
        
        assert result is False
    
    @patch('subprocess.run')
    def test_test_mcp_ping_request_invalid_json(self, mock_run):
        """Test ping request with invalid JSON response"""
        # Mock invalid JSON response
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Invalid JSON response"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Test ping request
        result = self.checker._test_mcp_ping_request()
        
        assert result is False
    
    @patch('subprocess.run')
    def test_test_mcp_ping_request_timeout(self, mock_run):
        """Test ping request timeout"""
        # Mock timeout
        mock_run.side_effect = subprocess.TimeoutExpired("echo", 10)
        
        # Test ping request
        result = self.checker._test_mcp_ping_request()
        
        assert result is False
    
    @patch.object(DockerMCPServerChecker, '_test_mcp_ping_request')
    def test_check_server_running_success(self, mock_ping):
        """Test server running check with successful ping"""
        mock_ping.return_value = True
        
        result = self.checker.check_server_running()
        
        assert result is True
        mock_ping.assert_called_once()
    
    @patch.object(DockerMCPServerChecker, '_test_mcp_ping_request')
    def test_check_server_running_failure(self, mock_ping):
        """Test server running check with failed ping"""
        mock_ping.return_value = False
        
        result = self.checker.check_server_running()
        
        assert result is False
        mock_ping.assert_called_once()
    
    @patch.object(DockerMCPServerChecker, '_test_mcp_ping_request')
    def test_test_connection_success(self, mock_ping):
        """Test connection test with successful ping"""
        mock_ping.return_value = True
        
        result = self.checker.test_connection()
        
        assert result["status"] == "success"
        assert result["message"] == "MCP server is responding to ping requests"
        assert result["test_method"] == "ping_request"
        assert result["response_time"] == "immediate"
    
    @patch.object(DockerMCPServerChecker, '_test_mcp_ping_request')
    def test_test_connection_failure(self, mock_ping):
        """Test connection test with failed ping"""
        mock_ping.return_value = False
        
        result = self.checker.test_connection()
        
        assert result["status"] == "failed"
        assert "not responding" in result["error"]
    
    @patch.object(DockerMCPServerChecker, '_test_mcp_ping_request')
    def test_check_docker_specific(self, mock_ping):
        """Test Docker-specific checks"""
        mock_ping.return_value = True
        
        result = self.checker._check_docker_specific()
        
        assert "in_docker" in result
        assert "environment_vars" in result
        assert "mcp_server_responding" in result
        assert result["mcp_server_responding"] is True
        assert result["test_method"] == "ping_request"
        assert "mcp_server_file_exists" in result
        assert "log_file_exists" in result
    
    def test_is_running_in_docker(self):
        """Test Docker detection"""
        # This test depends on the actual environment
        # We can't easily mock all Docker detection methods
        result = is_running_in_docker()
        assert isinstance(result, bool)


class TestMCPServerChecker:
    """Test Host MCP Server Checker (unchanged logic)"""
    
    def setup_method(self):
        """Setup test environment"""
        self.project_root = Path(__file__).parent.parent.parent
        self.checker = MCPServerChecker(self.project_root)
    
    @patch('subprocess.run')
    def test_check_server_running_host(self, mock_run):
        """Test server running check on host"""
        # Mock pgrep response
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "12345\n67890"
        mock_run.return_value = mock_result
        
        result = self.checker.check_server_running()
        
        assert result is True
        mock_run.assert_called_once_with(
            ['pgrep', '-f', 'neozork_mcp_server.py'],
            capture_output=True,
            text=True
        )
    
    @patch('subprocess.run')
    def test_check_server_running_host_not_running(self, mock_run):
        """Test server running check on host when not running"""
        # Mock pgrep response (no processes found)
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_run.return_value = mock_result
        
        result = self.checker.check_server_running()
        
        assert result is False


class TestIntegration:
    """Integration tests for the complete checker"""
    
    def test_environment_detection(self):
        """Test environment detection logic"""
        # This test verifies that the right checker is used
        # We can't easily test this without mocking the entire environment
        # But we can verify the function exists and returns a boolean
        result = is_running_in_docker()
        assert isinstance(result, bool)
    
    def test_checker_initialization(self):
        """Test checker initialization"""
        project_root = Path(__file__).parent.parent.parent
        
        # Test Docker checker
        docker_checker = DockerMCPServerChecker(project_root)
        assert docker_checker.project_root == project_root
        assert docker_checker.logger is not None
        
        # Test Host checker
        host_checker = MCPServerChecker(project_root)
        assert host_checker.project_root == project_root
        assert host_checker.logger is not None


if __name__ == "__main__":
    pytest.main([__file__]) 