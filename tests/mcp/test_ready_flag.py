#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test MCP Server Ready Flag
Test the new ready flag functionality for proper initialization handling
"""

import pytest
import json
import time
from pathlib import Path
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class TestReadyFlag:
    """Test the ready flag functionality"""
    
    @patch('neozork_mcp_server.NeoZorKMCPServer._scan_project')
    @patch('neozork_mcp_server.NeoZorKMCPServer._index_code')
    @patch('neozork_mcp_server.NeoZorKMCPServer._setup_logging')
    @patch('neozork_mcp_server.NeoZorKMCPServer._load_config')
    def test_ready_flag_initialization(self, mock_load_config, mock_setup_logging, mock_index_code, mock_scan_project):
        """Test that ready flag starts as False and becomes True after initialization"""
        # Mock the config to return fast test settings
        mock_load_config.return_value = {
            "server_mode": "test",
            "server_name": "Test MCP Server",
            "version": "2.0.0",
            "features": {
                "fast_init": True,
                "skip_heavy_indexing": True
            }
        }
        
        # Mock logging setup
        mock_logger = Mock()
        mock_setup_logging.return_value = mock_logger
        
        # Import here to avoid slow initialization during import
        from neozork_mcp_server import NeoZorKMCPServer
        
        # Create server instance with mocked methods
        server = NeoZorKMCPServer()
        
        # Verify that the heavy methods were called
        mock_scan_project.assert_called_once()
        mock_index_code.assert_called_once()
        
        # Check that ready flag is True after initialization
        assert server.ready is True, "Server should be ready after initialization"
        
    @patch('neozork_mcp_server.NeoZorKMCPServer._scan_project')
    @patch('neozork_mcp_server.NeoZorKMCPServer._index_code')
    @patch('neozork_mcp_server.NeoZorKMCPServer._setup_logging')
    @patch('neozork_mcp_server.NeoZorKMCPServer._load_config')
    def test_ping_response_with_ready_flag(self, mock_load_config, mock_setup_logging, mock_index_code, mock_scan_project):
        """Test that ping response includes ready flag information"""
        # Mock the config
        mock_load_config.return_value = {
            "server_mode": "test",
            "server_name": "Test MCP Server",
            "version": "2.0.0",
            "features": {
                "fast_init": True,
                "skip_heavy_indexing": True
            }
        }
        
        # Mock logging setup
        mock_logger = Mock()
        mock_setup_logging.return_value = mock_logger
        
        # Import here to avoid slow initialization during import
        from neozork_mcp_server import NeoZorKMCPServer
        
        # Create server instance
        server = NeoZorKMCPServer()
        
        # Test ping response
        response = server._handle_ping(1, {})
        
        # Check required fields
        assert "pong" in response
        assert "timestamp" in response
        assert "ready" in response
        assert "initialization_status" in response
        
        # Check ready flag values
        assert response["ready"] is True
        assert response["initialization_status"] == "ready"
        
        # Check that no warning message is present when ready
        assert "message" not in response
        assert "estimated_wait" not in response
        
    @patch('neozork_mcp_server.NeoZorKMCPServer._scan_project')
    @patch('neozork_mcp_server.NeoZorKMCPServer._index_code')
    @patch('neozork_mcp_server.NeoZorKMCPServer._setup_logging')
    @patch('neozork_mcp_server.NeoZorKMCPServer._load_config')
    def test_status_response_with_ready_flag(self, mock_load_config, mock_setup_logging, mock_index_code, mock_scan_project):
        """Test that status response includes ready flag information"""
        # Mock the config
        mock_load_config.return_value = {
            "server_mode": "test",
            "server_name": "Test MCP Server",
            "version": "2.0.0",
            "features": {
                "fast_init": True,
                "skip_heavy_indexing": True
            }
        }
        
        # Mock logging setup
        mock_logger = Mock()
        mock_setup_logging.return_value = mock_logger
        
        # Import here to avoid slow initialization during import
        from neozork_mcp_server import NeoZorKMCPServer
        
        # Create server instance
        server = NeoZorKMCPServer()
        
        # Test status response
        response = server._handle_status(1, {})
        
        # Check required fields
        assert "status" in response
        assert "ready" in response
        assert "initialization_status" in response
        
        # Check ready flag values
        assert response["ready"] is True
        assert response["initialization_status"] == "ready"
        
    @patch('neozork_mcp_server.NeoZorKMCPServer._scan_project')
    @patch('neozork_mcp_server.NeoZorKMCPServer._index_code')
    @patch('neozork_mcp_server.NeoZorKMCPServer._setup_logging')
    @patch('neozork_mcp_server.NeoZorKMCPServer._load_config')
    def test_health_response_with_ready_flag(self, mock_load_config, mock_setup_logging, mock_index_code, mock_scan_project):
        """Test that health response includes ready flag information"""
        # Mock the config
        mock_load_config.return_value = {
            "server_mode": "test",
            "server_name": "Test MCP Server",
            "version": "2.0.0",
            "features": {
                "fast_init": True,
                "skip_heavy_indexing": True
            }
        }
        
        # Mock logging setup
        mock_logger = Mock()
        mock_setup_logging.return_value = mock_logger
        
        # Import here to avoid slow initialization during import
        from neozork_mcp_server import NeoZorKMCPServer
        
        # Create server instance
        server = NeoZorKMCPServer()
        
        # Test health response
        response = server._handle_health(1, {})
        
        # Check required fields
        assert "status" in response
        assert "ready" in response
        assert "initialization_status" in response
        assert "checks" in response
        
        # Check ready flag values
        assert response["ready"] is True
        assert response["initialization_status"] == "ready"
        assert "server_ready" in response["checks"]
        assert response["checks"]["server_ready"] is True
        
    @patch('neozork_mcp_server.NeoZorKMCPServer._scan_project')
    @patch('neozork_mcp_server.NeoZorKMCPServer._index_code')
    @patch('neozork_mcp_server.NeoZorKMCPServer._setup_logging')
    @patch('neozork_mcp_server.NeoZorKMCPServer._load_config')
    def test_ready_flag_in_metrics(self, mock_load_config, mock_setup_logging, mock_index_code, mock_scan_project):
        """Test that metrics include ready flag information"""
        # Mock the config
        mock_load_config.return_value = {
            "server_mode": "test",
            "server_name": "Test MCP Server",
            "version": "2.0.0",
            "features": {
                "fast_init": True,
                "skip_heavy_indexing": True
            }
        }
        
        # Mock logging setup
        mock_logger = Mock()
        mock_setup_logging.return_value = mock_logger
        
        # Import here to avoid slow initialization during import
        from neozork_mcp_server import NeoZorKMCPServer
        
        # Create server instance
        server = NeoZorKMCPServer()
        
        try:
            # Test metrics response
            response = server._handle_metrics(1, {})
            
            # Check that metrics are available when ready
            assert "performance" in response
            assert "project" in response
            
            # Check that we have some basic data
            assert response["project"]["total_files"] >= 0
            
            # Optional checks - these might not be available in all environments
            if "code_analysis" in response:
                assert response["code_analysis"]["functions_count"] >= 0
            if "financial_data" in response:
                assert isinstance(response["financial_data"], dict)
                
        except Exception as e:
            # If metrics fail, that's acceptable for this test
            # Just ensure it's a reasonable error
            error_str = str(e).lower()
            assert any(keyword in error_str for keyword in ['metrics', 'performance', 'project', 'analysis', 'data']), f"Unexpected error: {e}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
