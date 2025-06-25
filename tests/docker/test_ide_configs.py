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
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

class TestIDESetupManager:
    """Test IDE setup manager functionality"""
    
    @pytest.fixture
    def project_root(self):
        """Get project root path"""
        return Path(__file__).parent.parent.parent
    
    @pytest.fixture
    def setup_manager(self, project_root):
        """Create setup manager instance"""
        from scripts.setup_ide_configs import IDESetupManager
        return IDESetupManager(project_root)
    
    def test_project_root_exists(self, project_root):
        """Test that project root exists and contains expected files"""
        assert project_root.exists()
        assert (project_root / "src").exists()
        assert (project_root / "tests").exists()
        assert (project_root / "data").exists()
    
    def test_cursor_config_creation(self, setup_manager, project_root):
        """Test Cursor configuration creation"""
        # Create config
        success = setup_manager.create_cursor_config()
        assert success
        
        # Check file exists
        config_path = project_root / "cursor_mcp_config.json"
        assert config_path.exists()
        
        # Validate JSON structure
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
    
    def test_vscode_config_creation(self, setup_manager, project_root):
        """Test VS Code configuration creation"""
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
    
    def test_pycharm_config_creation(self, setup_manager, project_root):
        """Test PyCharm configuration creation"""
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
    
    def test_docker_availability_check(self, setup_manager):
        """Test Docker availability check"""
        # This test will pass if Docker is available, skip if not
        docker_available = setup_manager.check_docker_availability()
        # Test should not fail regardless of Docker availability
        assert isinstance(docker_available, bool)
    
    def test_uv_availability_check(self, setup_manager):
        """Test UV availability check"""
        # This test will pass if UV is available, skip if not
        uv_available = setup_manager.check_uv_availability()
        # Test should not fail regardless of UV availability
        assert isinstance(uv_available, bool)
    
    def test_cursor_config_structure(self, setup_manager):
        """Test Cursor configuration structure"""
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
    
    def test_vscode_config_structure(self, setup_manager):
        """Test VS Code configuration structure"""
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
        """Test PyCharm configuration structure"""
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
        """Test Docker configuration structure"""
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
        """Test UV configuration structure"""
        uv_config = setup_manager.uv_config
        
        assert "enabled" in uv_config
        assert "python_path" in uv_config
        assert "uv_path" in uv_config
        assert "auto_install" in uv_config
        
        assert isinstance(uv_config["enabled"], bool)
        assert isinstance(uv_config["python_path"], str)
        assert isinstance(uv_config["uv_path"], str)
        assert isinstance(uv_config["auto_install"], bool)
    
    def test_setup_summary_creation(self, setup_manager, project_root):
        """Test setup summary creation"""
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
        
        # Check required sections
        required_sections = ["mcp.servers", "mcp.serverSettings"]
        for section in required_sections:
            assert section in config, f"Missing required section: {section}"
        
        # Check MCP servers
        mcp_servers = config["mcp.servers"]
        required_servers = ["neozork", "neozork-docker"]
        for server in required_servers:
            assert server in mcp_servers, f"Missing required server: {server}"
        
        # Check server settings
        server_settings = config["mcp.serverSettings"]
        assert "neozork" in server_settings
        
        neozork_settings = server_settings["neozork"]
        required_settings = ["enabled", "features", "performance", "monitoring"]
        for setting in required_settings:
            assert setting in neozork_settings, f"Missing required setting: {setting}"
    
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