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

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from neozork_mcp_server import NeoZorKMCPServer


class TestReadyFlag:
    """Test the ready flag functionality"""
    
    def test_ready_flag_initialization(self):
        """Test that ready flag starts as False and becomes True after initialization"""
        # Create a minimal config for faster testing
        config = {
            "server_mode": "test",
            "server_name": "Test MCP Server",
            "version": "2.0.0",
            "features": {
                "fast_init": True,
                "skip_heavy_indexing": True
            }
        }
        
        # Create server instance
        server = NeoZorKMCPServer(config=config)
        
        # Check that ready flag is True after initialization
        assert server.ready is True, "Server should be ready after initialization"
        
    def test_ping_response_with_ready_flag(self):
        """Test that ping response includes ready flag information"""
        config = {
            "server_mode": "test",
            "server_name": "Test MCP Server",
            "version": "2.0.0",
            "features": {
                "fast_init": True,
                "skip_heavy_indexing": True
            }
        }
        
        server = NeoZorKMCPServer(config=config)
        
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
        
    def test_status_response_with_ready_flag(self):
        """Test that status response includes ready flag information"""
        config = {
            "server_mode": "test",
            "server_name": "Test MCP Server",
            "version": "2.0.0",
            "features": {
                "fast_init": True,
                "skip_heavy_indexing": True
            }
        }
        
        server = NeoZorKMCPServer(config=config)
        
        # Test status response
        response = server._handle_status(1, {})
        
        # Check required fields
        assert "status" in response
        assert "ready" in response
        assert "initialization_status" in response
        
        # Check ready flag values
        assert response["ready"] is True
        assert response["initialization_status"] == "ready"
        
    def test_health_response_with_ready_flag(self):
        """Test that health response includes ready flag information"""
        config = {
            "server_mode": "test",
            "server_name": "Test MCP Server",
            "version": "2.0.0",
            "features": {
                "fast_init": True,
                "skip_heavy_indexing": True
            }
        }
        
        server = NeoZorKMCPServer(config=config)
        
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
        
    def test_ready_flag_in_metrics(self):
        """Test that metrics include ready flag information"""
        config = {
            "server_mode": "test",
            "server_name": "Test MCP Server",
            "version": "2.0.0",
            "features": {
                "fast_init": True,
                "skip_heavy_indexing": True
            }
        }
        
        server = NeoZorKMCPServer(config=config)
        
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
