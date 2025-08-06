#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test MCP server initialization wait logic
"""

import pytest
import time
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import json

# Import the modules we want to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from scripts.check_mcp_status import DockerMCPServerChecker, is_running_in_docker


class TestMCPInitializationWait:
    """Test MCP server initialization wait logic"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_root = Path(self.temp_dir)
        self.logs_dir = self.project_root / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
    def teardown_method(self):
        """Cleanup test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('scripts.check_mcp_status.is_running_in_docker')
    def test_wait_for_initialization_success(self, mock_docker):
        """Test successful initialization wait"""
        mock_docker.return_value = True
        
        checker = DockerMCPServerChecker(self.project_root)
        
        # Mock successful ping response
        with patch.object(checker, '_test_mcp_ping_request', return_value=True):
            result = checker._wait_for_mcp_initialization(max_wait_time=5)
            assert result is True
    
    @patch('scripts.check_mcp_status.is_running_in_docker')
    def test_wait_for_initialization_log_detection(self, mock_docker):
        """Test initialization detection via log file"""
        mock_docker.return_value = True
        
        checker = DockerMCPServerChecker(self.project_root)
        
        # Create log file with initialization message
        log_file = self.logs_dir / "mcp_server.log"
        with open(log_file, 'w') as f:
            f.write("🚀 Starting Neozork Unified MCP Server...\n")
            f.write("📊 Scanning project files...\n")
            f.write("✅ Neozork Unified MCP Server initialized successfully\n")
        
        # Mock failed ping but successful log detection
        with patch.object(checker, '_test_mcp_ping_request', return_value=False):
            result = checker._wait_for_mcp_initialization(max_wait_time=5)
            assert result is True
    
    @patch('scripts.check_mcp_status.is_running_in_docker')
    def test_wait_for_initialization_timeout(self, mock_docker):
        """Test initialization timeout"""
        mock_docker.return_value = True
        
        checker = DockerMCPServerChecker(self.project_root)
        
        # Mock failed ping and no log file
        with patch.object(checker, '_test_mcp_ping_request', return_value=False):
            result = checker._wait_for_mcp_initialization(max_wait_time=2)
            assert result is False
    
    @patch('scripts.check_mcp_status.is_running_in_docker')
    def test_check_server_running_with_initialization_wait(self, mock_docker):
        """Test check_server_running with initialization wait"""
        mock_docker.return_value = True
        
        checker = DockerMCPServerChecker(self.project_root)
        
        # Mock successful initialization wait and ping
        with patch.object(checker, '_wait_for_mcp_initialization', return_value=True), \
             patch.object(checker, '_test_mcp_ping_request', return_value=True):
            result = checker.check_server_running()
            assert result is True
    
    @patch('scripts.check_mcp_status.is_running_in_docker')
    def test_check_server_running_initialization_timeout(self, mock_docker):
        """Test check_server_running with initialization timeout"""
        mock_docker.return_value = True
        
        checker = DockerMCPServerChecker(self.project_root)
        
        # Mock failed initialization wait
        with patch.object(checker, '_wait_for_mcp_initialization', return_value=False):
            result = checker.check_server_running()
            assert result is False
    
    @patch('scripts.check_mcp_status.is_running_in_docker')
    def test_test_connection_with_initialization_wait(self, mock_docker):
        """Test test_connection with initialization wait"""
        mock_docker.return_value = True
        
        checker = DockerMCPServerChecker(self.project_root)
        
        # Mock successful initialization wait and ping
        with patch.object(checker, '_wait_for_mcp_initialization', return_value=True), \
             patch.object(checker, '_test_mcp_ping_request', return_value=True):
            result = checker.test_connection()
            assert result["status"] == "success"
            assert "MCP server is responding to ping requests" in result["message"]
    
    @patch('scripts.check_mcp_status.is_running_in_docker')
    def test_test_connection_initialization_timeout(self, mock_docker):
        """Test test_connection with initialization timeout"""
        mock_docker.return_value = True
        
        checker = DockerMCPServerChecker(self.project_root)
        
        # Mock failed initialization wait
        with patch.object(checker, '_wait_for_mcp_initialization', return_value=False):
            result = checker.test_connection()
            assert result["status"] == "failed"
            assert "initialization did not complete" in result["error"]
    
    def test_is_running_in_docker_detection(self):
        """Test Docker environment detection"""
        # Test should work in both Docker and non-Docker environments
        result = is_running_in_docker()
        assert isinstance(result, bool)
    
    @patch('scripts.check_mcp_status.is_running_in_docker')
    def test_docker_checker_initialization(self, mock_docker):
        """Test DockerMCPServerChecker initialization"""
        mock_docker.return_value = True
        
        checker = DockerMCPServerChecker(self.project_root)
        assert checker.project_root == self.project_root
        assert hasattr(checker, 'logger')
    
    def test_log_file_reading(self):
        """Test log file reading functionality"""
        checker = DockerMCPServerChecker(self.project_root)
        
        # Test reading non-existent log file
        result = checker._wait_for_mcp_initialization(max_wait_time=1)
        assert result is False
        
        # Test reading log file with initialization message
        log_file = self.logs_dir / "mcp_server.log"
        with open(log_file, 'w') as f:
            f.write("✅ Neozork Unified MCP Server initialized successfully\n")
        
        with patch.object(checker, '_test_mcp_ping_request', return_value=False):
            result = checker._wait_for_mcp_initialization(max_wait_time=2)
            assert result is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 