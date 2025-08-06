#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test MCP Server Status Checker
Test the new Docker-specific socket-based detection logic
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

from mcp.check_mcp_status import DockerMCPServerChecker, MCPServerChecker, is_running_in_docker


class TestDockerMCPServerChecker:
    """Test Docker MCP Server Checker with socket-based detection"""
    
    def setup_method(self):
        """Setup test environment"""
        self.project_root = Path(__file__).parent.parent.parent
        self.checker = DockerMCPServerChecker(self.project_root)
    
    @patch('socket.socket')
    def test_test_mcp_ping_request_success(self, mock_socket):
        """Test successful ping request to MCP server via socket"""
        # Mock successful socket connection and response
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.return_value = None
        mock_sock.recv.return_value = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "result": {"pong": True, "timestamp": "2024-01-01T00:00:00"}
        }).encode('utf-8')
        mock_sock.close.return_value = None
        
        # Test ping request
        result = self.checker._test_mcp_ping_request()
        
        assert result is True
        mock_sock.connect.assert_called_once_with(('localhost', 8080))
        mock_sock.send.assert_called_once()
        mock_sock.recv.assert_called_once()
        mock_sock.close.assert_called_once()
    
    @patch('socket.socket')
    def test_test_mcp_ping_request_failure(self, mock_socket):
        """Test failed ping request to MCP server via socket"""
        # Mock connection refused
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.side_effect = ConnectionRefusedError()
        mock_sock.close.return_value = None
        
        # Test ping request
        result = self.checker._test_mcp_ping_request()
        
        assert result is False
        mock_sock.close.assert_called_once()
    
    @patch('socket.socket')
    def test_test_mcp_ping_request_invalid_json(self, mock_socket):
        """Test ping request with invalid JSON response via socket"""
        # Mock successful connection but invalid JSON response
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.return_value = None
        mock_sock.recv.return_value = b"Invalid JSON response"
        mock_sock.close.return_value = None
        
        # Test ping request
        result = self.checker._test_mcp_ping_request()
        
        assert result is False
        mock_sock.close.assert_called_once()
    
    @patch('socket.socket')
    def test_test_mcp_ping_request_timeout(self, mock_socket):
        """Test ping request timeout via socket"""
        # Mock timeout
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.side_effect = TimeoutError()
        mock_sock.close.return_value = None
        
        # Test ping request
        result = self.checker._test_mcp_ping_request()
        
        assert result is False
        mock_sock.close.assert_called_once()
    
    @patch.object(DockerMCPServerChecker, '_wait_for_mcp_initialization')
    def test_check_server_running_success(self, mock_wait):
        """Test server running check with successful initialization"""
        mock_wait.return_value = True
        
        # Mock log file with initialization message
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', create=True) as mock_open:
            mock_file = MagicMock()
            mock_open.return_value.__enter__.return_value = mock_file
            mock_file.read.return_value = "✅ Neozork Unified MCP Server initialized successfully"
            
            result = self.checker.check_server_running()
            
            assert result is True
            mock_wait.assert_called_once()
    
    @patch.object(DockerMCPServerChecker, '_wait_for_mcp_initialization')
    def test_check_server_running_failure(self, mock_wait):
        """Test server running check with failed initialization"""
        mock_wait.return_value = False
        
        result = self.checker.check_server_running()
        
        assert result is False
        mock_wait.assert_called_once()
    
    @patch.object(DockerMCPServerChecker, '_wait_for_mcp_initialization')
    @patch('socket.socket')
    def test_test_connection_success(self, mock_socket, mock_wait):
        """Test connection test with successful socket communication"""
        # Mock successful initialization and socket connection
        mock_wait.return_value = True
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.return_value = None
        mock_sock.recv.return_value = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "result": {"pong": True}
        }).encode('utf-8')
        mock_sock.close.return_value = None
        
        result = self.checker.test_connection()
        
        assert result["status"] == "success"
        assert "socket communication" in result["message"]
        assert result["test_method"] == "socket_ping"
        assert result["response_time"] == "immediate"
    
    @patch.object(DockerMCPServerChecker, '_wait_for_mcp_initialization')
    def test_test_connection_failure(self, mock_wait):
        """Test connection test with failed initialization"""
        mock_wait.return_value = False
        
        result = self.checker.test_connection()
        
        assert result["status"] == "failed"
        assert "initialization did not complete" in result["error"]
    
    @patch('socket.socket')
    def test_check_docker_specific(self, mock_socket):
        """Test Docker-specific checks"""
        # Mock successful socket connection
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.return_value = None
        mock_sock.recv.return_value = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "result": {"pong": True}
        }).encode('utf-8')
        mock_sock.close.return_value = None
        
        result = self.checker._check_docker_specific()
        
        assert "in_docker" in result
        assert "environment_vars" in result
        assert "mcp_server_responding" in result
        assert result["mcp_server_responding"] is True
        assert result["test_method"] == "socket_connection"
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
    @patch.object(MCPServerChecker, '_test_mcp_ping_request')
    def test_check_server_running_host(self, mock_ping, mock_run):
        """Test server running check on host"""
        # Mock failed ping first
        mock_ping.return_value = False
        
        # Mock pgrep response
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "12345\n67890"
        mock_run.return_value = mock_result
        
        result = self.checker.check_server_running()
        
        assert result is True
        # Expect 2 calls: one for ping test, one for pgrep
        assert mock_run.call_count == 1  # Only pgrep call
        mock_ping.assert_called_once()
        
        # Check that pgrep was called
        pgrep_call = mock_run.call_args_list[0]
        assert pgrep_call[0][0] == ['pgrep', '-f', 'neozork_mcp_server.py']
    
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
    """Integration tests"""
    
    def test_environment_detection(self):
        """Test environment detection logic"""
        # Test that the right checker is used
        checker = DockerMCPServerChecker() if is_running_in_docker() else MCPServerChecker()
        assert checker is not None
    
    def test_checker_initialization(self):
        """Test checker initialization"""
        project_root = Path(__file__).parent.parent.parent
        checker = DockerMCPServerChecker(project_root)
        assert checker.project_root == project_root 