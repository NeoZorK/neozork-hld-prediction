#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for IDE Configuration Setup
Tests MCP server configurations for Cursor, VS Code, and PyCharm
"""

import json
import pytest
from pathlib import Path
from typing import Dict, Any
import sys
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))
# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts"))


def is_docker_environment():
    """Check if running in Docker environment"""
    return (
        os.getenv("DOCKER_CONTAINER", "false").lower() == "true" or
        os.path.exists("/.dockerenv") or
        os.path.exists("/app")
    )


class TestIDESetupManager:
    """Test IDE setup manager functionality"""
    
    @pytest.fixture
    def project_root(self):
        """Get project root path"""
        return Path(__file__).parent.parent.parent
    
    @pytest.fixture
    def setup_manager(self, project_root):
        """Create setup manager instance"""
        try:
            # Import from the correct path in scripts/utilities/
            sys.path.insert(0, str(project_root / "scripts" / "utilities"))
            from setup_ide_configs import IDESetupManager
            return IDESetupManager(project_root)
        except ImportError as e:
            pytest.skip(f"setup_ide_configs module not available: {e}")
    
    def test_project_root_exists(self, project_root):
        """Test that project root exists and contains expected files"""
        assert project_root.exists()
        assert (project_root / "src").exists()
        assert (project_root / "tests").exists()
        # In Docker environment, data directory might be empty or mounted differently
        if is_docker_environment():
            # Just check if the directory exists, don't require specific contents
            if (project_root / "data").exists():
                print("✅ Data directory exists in Docker environment")
            else:
                print("⚠️  Data directory not found in Docker environment - this is acceptable")
        else:
            # In non-Docker environment, require data directory
            assert (project_root / "data").exists()
        # Check for key project files
        assert (project_root / "pyproject.toml").exists()
        assert (project_root / "requirements.txt").exists()
    
    @pytest.mark.skipif(not is_docker_environment(), reason="This test should only run in Docker environment")
    def test_cursor_config_creation(self, setup_manager, project_root):
        """Test Cursor configuration creation. Only runs in Docker environment."""
        # Create config
        success = setup_manager.create_cursor_config()
        assert success
        
        # Check cursor_mcp_config.json exists
        config_path = project_root / "cursor_mcp_config.json"
        assert config_path.exists()
        
        # Check mcp.json exists (for Cursor IDE compatibility)
        mcp_json_path = project_root / "mcp.json"
        assert mcp_json_path.exists()
        
        # Validate cursor_mcp_config.json structure
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Check required sections
        assert "mcpServers" in config
        assert "serverSettings" in config
        assert "cursor" in config
        
        # Check server configurations
        mcp_servers = config["mcpServers"]
        assert "neozork" in mcp_servers
        assert "neozork-docker" in mcp_servers
        
        # Check server settings
        server_settings = config["serverSettings"]
        assert "neozork" in server_settings
        assert server_settings["neozork"]["enabled"] is True
        
        # Validate mcp.json structure
        with open(mcp_json_path, 'r', encoding='utf-8') as f:
            mcp_config = json.load(f)
        
        # Check mcp.json has correct structure
        assert "mcpServers" in mcp_config
        mcp_servers = mcp_config["mcpServers"]
        assert "neozork" in mcp_servers
        assert "neozork-docker" in mcp_servers
        
        # Verify both configs have same server definitions
        assert mcp_config["mcpServers"]["neozork"]["command"] == config["mcpServers"]["neozork"]["command"]
        assert mcp_config["mcpServers"]["neozork"]["args"] == config["mcpServers"]["neozork"]["args"]
    
    @pytest.mark.skipif(not is_docker_environment(), reason="This test should only run in Docker environment")
    def test_vscode_config_creation(self, setup_manager, project_root):
        """Test VS Code configuration creation. Only runs in Docker environment."""
        # Create config
        success = setup_manager.create_vscode_config()
        assert success
        
        # Check file exists
        config_path = project_root / ".vscode" / "settings.json"
        assert config_path.exists()
        
        # Validate JSON structure
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Check required sections
        assert "mcp.servers" in config
        assert "mcp.serverSettings" in config
        
        # Check server configurations
        mcp_servers = config["mcp.servers"]
        assert "neozork" in mcp_servers
        assert "neozork-docker" in mcp_servers
        
        # Check server settings
        server_settings = config["mcp.serverSettings"]
        assert "neozork" in server_settings
        assert server_settings["neozork"]["enabled"] is True
    
    @pytest.mark.skipif(not is_docker_environment(), reason="This test should only run in Docker environment")
    def test_pycharm_config_creation(self, setup_manager, project_root):
        """Test PyCharm configuration creation. Only runs in Docker environment."""
        # Create config
        success = setup_manager.create_pycharm_config()
        assert success
        
        # Check file exists
        config_path = project_root / "pycharm_mcp_config.json"
        assert config_path.exists()
        
        # Validate JSON structure
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Check required sections
        assert "mcpServers" in config
        assert "serverSettings" in config
        assert "pycharm" in config
        
        # Check server configurations
        mcp_servers = config["mcpServers"]
        assert "neozork" in mcp_servers
        assert "neozork-docker" in mcp_servers
        
        # Check server settings
        server_settings = config["serverSettings"]
        assert "neozork" in server_settings
        assert server_settings["neozork"]["enabled"] is True
    
    @pytest.mark.skipif(not is_docker_environment(), reason="This test should only run in Docker environment")
    def test_docker_availability_check(self, setup_manager):
        """Test Docker availability check. Only runs in Docker environment."""
        # This test will pass if Docker is available, skip if not
        docker_available = setup_manager.check_docker_availability()
        # Test should not fail regardless of Docker availability
        assert isinstance(docker_available, bool)
    
    @pytest.mark.skipif(not is_docker_environment(), reason="This test should only run in Docker environment")
    def test_uv_availability_check(self, setup_manager):
        """Test UV availability check. Only runs in Docker environment."""
        # This test will pass if UV is available, skip if not
        uv_available = setup_manager.check_uv_availability()
        # Test should not fail regardless of UV availability
        assert isinstance(uv_available, bool)
    
    def test_cursor_config_structure(self, setup_manager):
        """Test Cursor configuration structure (runs outside Docker)."""
        config = setup_manager._get_cursor_config()
        
        # Check top-level structure
        assert "mcpServers" in config
        assert "serverSettings" in config
        assert "cursor" in config
        
        # Check MCP servers
        mcp_servers = config["mcpServers"]
        assert "neozork" in mcp_servers
        assert "neozork-docker" in mcp_servers
        
        # Check server settings
        server_settings = config["serverSettings"]
        assert "neozork" in server_settings
        
        neozork_settings = server_settings["neozork"]
        assert "enabled" in neozork_settings
        assert "features" in neozork_settings
        assert "performance" in neozork_settings
        assert "monitoring" in neozork_settings
        assert "docker" in neozork_settings
    
    def test_mcp_json_config_structure(self, setup_manager):
        """Test MCP JSON configuration structure (runs outside Docker)."""
        config = setup_manager._get_mcp_json_config()
        
        # Check top-level structure
        assert "mcpServers" in config
        
        # Check MCP servers
        mcp_servers = config["mcpServers"]
        assert "neozork" in mcp_servers
        assert "neozork-docker" in mcp_servers
        
        # Check neozork server configuration
        neozork_server = mcp_servers["neozork"]
        assert "command" in neozork_server
        assert "args" in neozork_server
        assert "env" in neozork_server
        assert "cwd" in neozork_server
    
    def test_vscode_config_structure(self, setup_manager):
        """Test VS Code configuration structure (runs outside Docker)."""
        config = setup_manager._get_vscode_config()
        
        # Check top-level structure
        assert "mcp.servers" in config
        assert "mcp.serverSettings" in config
        
        # Check MCP servers
        mcp_servers = config["mcp.servers"]
        assert "neozork" in mcp_servers
        assert "neozork-docker" in mcp_servers
        
        # Check server settings
        server_settings = config["mcp.serverSettings"]
        assert "neozork" in server_settings
        
        neozork_settings = server_settings["neozork"]
        assert "enabled" in neozork_settings
        assert "features" in neozork_settings
        assert "performance" in neozork_settings
        assert "monitoring" in neozork_settings
    
    def test_pycharm_config_structure(self, setup_manager):
        """Test PyCharm configuration structure (runs outside Docker)."""
        config = setup_manager._get_pycharm_config()
        
        # Check top-level structure
        assert "mcpServers" in config
        assert "serverSettings" in config
        assert "pycharm" in config
        
        # Check MCP servers
        mcp_servers = config["mcpServers"]
        assert "neozork" in mcp_servers
        assert "neozork-docker" in mcp_servers
        
        # Check server settings
        server_settings = config["serverSettings"]
        assert "neozork" in server_settings
        
        neozork_settings = server_settings["neozork"]
        assert "enabled" in neozork_settings
        assert "features" in neozork_settings
        assert "performance" in neozork_settings
        assert "monitoring" in neozork_settings
    
    def test_docker_config_structure(self, setup_manager):
        """Test Docker configuration structure (runs outside Docker)."""
        docker_config = setup_manager.docker_config
        
        assert "enabled" in docker_config
        assert "container_name" in docker_config
        assert "port" in docker_config
        assert "volumes" in docker_config
        assert "environment" in docker_config
        
        assert isinstance(docker_config["enabled"], bool)
        assert isinstance(docker_config["container_name"], str)
        assert isinstance(docker_config["port"], int)
        assert isinstance(docker_config["volumes"], list)
        assert isinstance(docker_config["environment"], dict)
    
    def test_uv_config_structure(self, setup_manager):
        """Test UV configuration structure (runs outside Docker)."""
        uv_config = setup_manager.uv_config
        
        assert "enabled" in uv_config
        assert "python_path" in uv_config
        assert "uv_path" in uv_config
        assert "auto_install" in uv_config
        
        assert isinstance(uv_config["enabled"], bool)
        assert isinstance(uv_config["python_path"], str)
        assert isinstance(uv_config["uv_path"], str)
        assert isinstance(uv_config["auto_install"], bool)
    
    @pytest.mark.skipif(not is_docker_environment(), reason="This test should only run in Docker environment")
    def test_setup_summary_creation(self, setup_manager, project_root):
        """Test setup summary creation. Only runs in Docker environment."""
        # Mock results
        results = {
            "cursor": True,
            "vscode": True,
            "pycharm": True
        }
        
        docker_available = True
        uv_available = True
        
        # Create summary
        setup_manager._create_setup_summary(results, docker_available, uv_available)
        
        # Check summary file exists
        summary_path = project_root / "logs" / "ide_setup_summary.json"
        assert summary_path.exists()
        
        # Validate summary structure
        with open(summary_path, 'r', encoding='utf-8') as f:
            summary = json.load(f)
        
        assert "timestamp" in summary
        assert "project_root" in summary
        assert "system_capabilities" in summary
        assert "ide_setup_results" in summary
        assert "configuration_files" in summary
        
        # Check system capabilities
        capabilities = summary["system_capabilities"]
        assert "docker_available" in capabilities
        assert "uv_available" in capabilities
        
        # Check IDE results
        ide_results = summary["ide_setup_results"]
        assert "cursor" in ide_results
        assert "vscode" in ide_results
        assert "pycharm" in ide_results
        
        # Check configuration files
        config_files = summary["configuration_files"]
        assert "cursor" in config_files
        assert "vscode" in config_files
        assert "pycharm" in config_files

class TestIDEConfigValidation:
    """Test IDE configuration validation"""
    
    @pytest.fixture
    def project_root(self):
        """Get project root path"""
        return Path(__file__).parent.parent.parent
    
    def test_cursor_config_validation(self, project_root):
        """Test Cursor configuration validation"""
        config_path = project_root / "cursor_mcp_config.json"
        
        if not config_path.exists():
            pytest.skip("Cursor config file not found")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Validate JSON structure
        assert isinstance(config, dict)
        
        # Check required sections
        required_sections = ["mcpServers", "serverSettings", "cursor"]
        for section in required_sections:
            assert section in config, f"Missing required section: {section}"
        
        # Check MCP servers
        mcp_servers = config["mcpServers"]
        required_servers = ["neozork", "neozork-docker"]
        for server in required_servers:
            assert server in mcp_servers, f"Missing required server: {server}"
        
        # Check server settings
        server_settings = config["serverSettings"]
        assert "neozork" in server_settings
        
        neozork_settings = server_settings["neozork"]
        required_settings = ["enabled", "features", "performance", "monitoring"]
        for setting in required_settings:
            assert setting in neozork_settings, f"Missing required setting: {setting}"
    
    def test_vscode_config_validation(self, project_root):
        """Test VS Code configuration validation"""
        config_path = project_root / ".vscode" / "settings.json"
        
        if not config_path.exists():
            pytest.skip("VS Code config file not found")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Validate JSON structure
        assert isinstance(config, dict)
        
        # Check if it's a valid VS Code settings file
        # VS Code settings can have various structures, so we just check it's valid JSON
        assert len(config) > 0, "VS Code config should not be empty"
        
        # If MCP sections exist, validate them
        if "mcp.servers" in config:
            mcp_servers = config["mcp.servers"]
            assert isinstance(mcp_servers, dict), "mcp.servers should be a dictionary"
        
        if "mcp.serverSettings" in config:
            server_settings = config["mcp.serverSettings"]
            assert isinstance(server_settings, dict), "mcp.serverSettings should be a dictionary"
    
    def test_pycharm_config_validation(self, project_root):
        """Test PyCharm configuration validation"""
        config_path = project_root / "pycharm_mcp_config.json"
        
        if not config_path.exists():
            pytest.skip("PyCharm config file not found")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Validate JSON structure
        assert isinstance(config, dict)
        
        # Check required sections
        required_sections = ["mcpServers", "serverSettings", "pycharm"]
        for section in required_sections:
            assert section in config, f"Missing required section: {section}"
        
        # Check MCP servers
        mcp_servers = config["mcpServers"]
        required_servers = ["neozork", "neozork-docker"]
        for server in required_servers:
            assert server in mcp_servers, f"Missing required server: {server}"
        
        # Check server settings
        server_settings = config["serverSettings"]
        assert "neozork" in server_settings
        
        neozork_settings = server_settings["neozork"]
        required_settings = ["enabled", "features", "performance", "monitoring"]
        for setting in required_settings:
            assert setting in neozork_settings, f"Missing required setting: {setting}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 