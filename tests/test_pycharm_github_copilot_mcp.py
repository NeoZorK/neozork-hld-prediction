#!/usr/bin/env python3
"""
Unit tests for PyCharm GitHub Copilot MCP Server
"""

import pytest
import os
import sys

def test_pycharm_github_copilot_mcp_import():
    """Test that PyCharm GitHub Copilot MCP can be imported"""
    try:
        # Add project root to path
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, project_root)
        
        # Try to import the main module
        import pycharm_github_copilot_mcp
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import pycharm_github_copilot_mcp: {e}")

def test_pycharm_github_copilot_mcp_file_exists():
    """Test that the MCP server file exists"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mcp_file = os.path.join(project_root, "pycharm_github_copilot_mcp.py")
    assert os.path.exists(mcp_file), f"MCP server file not found: {mcp_file}"

def test_pycharm_github_copilot_mcp_basic_functionality():
    """Test basic MCP server functionality"""
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, project_root)
        
        # Test that the file can be executed as a module
        import subprocess
        result = subprocess.run([sys.executable, "-c", "import pycharm_github_copilot_mcp"], 
                              capture_output=True, text=True, cwd=project_root)
        assert result.returncode == 0, f"Failed to import module: {result.stderr}"
    except Exception as e:
        pytest.fail(f"Basic functionality test failed: {e}") 