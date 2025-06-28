#!/usr/bin/env python3
"""
Test suite for Native Container Full Functionality
Tests all features including UV, MCP server, command wrappers, and bash history
"""

import os
import sys
import subprocess
import time
import json
import pytest
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

class TestNativeContainerFullFunctionality:
    """Test class for native container full functionality"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.project_root = project_root
        self.container_name = "neozork-hld-prediction"
        self.native_container_dir = self.project_root / "scripts" / "native-container"
        
    def test_container_setup_script_exists(self):
        """Test that setup script exists and is executable"""
        setup_script = self.native_container_dir / "setup.sh"
        assert setup_script.exists(), "Setup script should exist"
        assert os.access(setup_script, os.X_OK), "Setup script should be executable"
        
    def test_entrypoint_script_exists(self):
        """Test that entrypoint script exists and is executable"""
        entrypoint_script = self.project_root / "container-entrypoint.sh"
        assert entrypoint_script.exists(), "Entrypoint script should exist"
        assert os.access(entrypoint_script, os.X_OK), "Entrypoint script should be executable"
        
    def test_container_yaml_exists(self):
        """Test that container.yaml exists and is valid"""
        container_yaml = self.project_root / "container.yaml"
        assert container_yaml.exists(), "container.yaml should exist"
        
        # Try to parse as YAML
        try:
            import yaml
            with open(container_yaml, 'r') as f:
                yaml.safe_load(f)
        except Exception as e:
            pytest.fail(f"container.yaml should be valid YAML: {e}")
            
    def test_required_files_exist(self):
        """Test that all required files for full functionality exist"""
        required_files = [
            "run_analysis.py",
            "neozork_mcp_server.py",
            "cursor_mcp_config.json",
            "requirements.txt",
            "src/",
            "tests/",
            "data/",
            "logs/",
            "results/",
            "scripts/"
        ]
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            assert full_path.exists(), f"Required file/directory should exist: {file_path}"
            
    def test_uv_configuration_files_exist(self):
        """Test that UV configuration files exist"""
        uv_files = [
            "uv_setup/uv.toml",
            "uv_setup/setup_uv.sh",
            "uv_setup/update_deps.sh"
        ]
        
        for file_path in uv_files:
            full_path = self.project_root / file_path
            assert full_path.exists(), f"UV configuration file should exist: {file_path}"
            
    def test_mcp_server_files_exist(self):
        """Test that MCP server files exist"""
        mcp_files = [
            "neozork_mcp_server.py",
            "cursor_mcp_config.json",
            "scripts/check_mcp_status.py"
        ]
        
        for file_path in mcp_files:
            full_path = self.project_root / file_path
            assert full_path.exists(), f"MCP server file should exist: {file_path}"
            
    def test_command_wrapper_scripts_exist(self):
        """Test that command wrapper scripts exist"""
        wrapper_scripts = [
            "scripts/native-container/run.sh",
            "scripts/native-container/stop.sh",
            "scripts/native-container/exec.sh",
            "scripts/native-container/logs.sh",
            "scripts/native-container/cleanup.sh"
        ]
        
        for script_path in wrapper_scripts:
            full_path = self.project_root / script_path
            assert full_path.exists(), f"Wrapper script should exist: {script_path}"
            assert os.access(full_path, os.X_OK), f"Wrapper script should be executable: {script_path}"
            
    def test_entrypoint_script_content(self):
        """Test that entrypoint script contains required functionality"""
        entrypoint_script = self.project_root / "container-entrypoint.sh"
        
        with open(entrypoint_script, 'r') as f:
            content = f.read()
            
        # Check for required functions
        required_functions = [
            "verify_uv",
            "setup_bash_environment",
            "create_command_wrappers",
            "run_data_feed_tests",
            "start_mcp_server",
            "init_bash_history"
        ]
        
        for func in required_functions:
            assert func in content, f"Entrypoint should contain function: {func}"
            
    def test_entrypoint_environment_variables(self):
        """Test that entrypoint script sets required environment variables"""
        entrypoint_script = self.project_root / "container-entrypoint.sh"
        
        with open(entrypoint_script, 'r') as f:
            content = f.read()
            
        # Check for required environment variables
        required_env_vars = [
            "USE_UV=true",
            "UV_ONLY=true",
            "NATIVE_CONTAINER=true",
            "DOCKER_CONTAINER=false",
            "PYTHONPATH=/app"
        ]
        
        for env_var in required_env_vars:
            assert env_var in content, f"Entrypoint should set environment variable: {env_var}"
            
    def test_command_wrappers_creation(self):
        """Test that entrypoint creates command wrappers"""
        entrypoint_script = self.project_root / "container-entrypoint.sh"
        
        with open(entrypoint_script, 'r') as f:
            content = f.read()
            
        # Check for command wrapper creation
        required_wrappers = [
            "nz",
            "eda",
            "uv-install",
            "uv-update",
            "uv-test",
            "uv-pytest",
            "mcp-start",
            "mcp-check"
        ]
        
        for wrapper in required_wrappers:
            assert f"/tmp/bin/{wrapper}" in content, f"Entrypoint should create wrapper: {wrapper}"
            
    def test_bash_history_initialization(self):
        """Test that entrypoint initializes bash history"""
        entrypoint_script = self.project_root / "container-entrypoint.sh"
        
        with open(entrypoint_script, 'r') as f:
            content = f.read()
            
        # Check for bash history initialization
        history_commands = [
            "uv run pytest tests -n auto",
            "nz --interactive",
            "eda -dqc",
            "mcp-start",
            "mcp-check"
        ]
        
        for cmd in history_commands:
            assert cmd in content, f"Entrypoint should add command to history: {cmd}"
            
    def test_mcp_server_integration(self):
        """Test that MCP server integration is properly configured"""
        entrypoint_script = self.project_root / "container-entrypoint.sh"
        
        with open(entrypoint_script, 'r') as f:
            content = f.read()
            
        # Check for MCP server functionality
        mcp_features = [
            "start_mcp_server",
            "cleanup_mcp_server",
            "mcp_server.pid",
            "check_mcp_status.py"
        ]
        
        for feature in mcp_features:
            assert feature in content, f"Entrypoint should support MCP feature: {feature}"
            
    def test_data_feed_tests_integration(self):
        """Test that data feed tests are integrated"""
        entrypoint_script = self.project_root / "container-entrypoint.sh"
        
        with open(entrypoint_script, 'r') as f:
            content = f.read()
            
        # Check for data feed test integration
        test_features = [
            "run_data_feed_tests",
            "run_tests_docker.py",
            "Polygon, YFinance, Binance"
        ]
        
        for feature in test_features:
            assert feature in content, f"Entrypoint should support test feature: {feature}"
            
    def test_usage_guide_integration(self):
        """Test that usage guide is integrated"""
        entrypoint_script = self.project_root / "container-entrypoint.sh"
        
        with open(entrypoint_script, 'r') as f:
            content = f.read()
            
        # Check for usage guide functionality
        guide_features = [
            "show_usage_guide",
            "NeoZork HLD Prediction Usage Guide",
            "UV Package Manager Commands",
            "MCP Server Commands"
        ]
        
        for feature in guide_features:
            assert feature in content, f"Entrypoint should support guide feature: {feature}"
            
    def test_commands_file_creation(self):
        """Test that commands file is created"""
        entrypoint_script = self.project_root / "container-entrypoint.sh"
        
        with open(entrypoint_script, 'r') as f:
            content = f.read()
            
        # Check for commands file creation
        assert "create_commands_file" in content, "Entrypoint should create commands file"
        assert "/tmp/neozork_commands.txt" in content, "Entrypoint should create commands file"
        
    def test_setup_script_uv_support(self):
        """Test that setup script supports UV"""
        setup_script = self.native_container_dir / "setup.sh"
        
        with open(setup_script, 'r') as f:
            content = f.read()
            
        # Check for UV support in setup
        uv_features = [
            "check_uv",
            "USE_UV=true",
            "UV_ONLY=true",
            "UV_CACHE_DIR",
            "uv_cache"
        ]
        
        for feature in uv_features:
            assert feature in content, f"Setup script should support UV feature: {feature}"
            
    def test_setup_script_mcp_support(self):
        """Test that setup script supports MCP server"""
        setup_script = self.native_container_dir / "setup.sh"
        
        with open(setup_script, 'r') as f:
            content = f.read()
            
        # Check for MCP support in setup
        mcp_features = [
            "neozork_mcp_server.py",
            "cursor_mcp_config.json",
            "MCP_SERVER_TYPE"
        ]
        
        for feature in mcp_features:
            assert feature in content, f"Setup script should support MCP feature: {feature}"
            
    def test_setup_script_full_docker_parity(self):
        """Test that setup script mentions full Docker parity"""
        setup_script = self.native_container_dir / "setup.sh"
        
        with open(setup_script, 'r') as f:
            content = f.read()
            
        # Check for Docker parity mentions
        parity_features = [
            "Full feature parity with Docker container",
            "Full Docker container parity",
            "Command wrappers (nz, eda, uv-*)",
            "Bash history and configuration",
            "External data feed tests"
        ]
        
        for feature in parity_features:
            assert feature in content, f"Setup script should mention Docker parity feature: {feature}"
            
    def test_container_yaml_configuration(self):
        """Test that container.yaml has proper configuration"""
        container_yaml = self.project_root / "container.yaml"
        
        with open(container_yaml, 'r') as f:
            content = f.read()
            
        # Check for required configuration
        config_features = [
            "neozork-hld-prediction",
            "USE_UV=true",
            "UV_ONLY=true",
            "NATIVE_CONTAINER=true",
            "DOCKER_CONTAINER=false",
            "MCP_SERVER_TYPE=pycharm_copilot"
        ]
        
        for feature in config_features:
            assert feature in content, f"Container YAML should contain: {feature}"
            
    def test_required_directories_structure(self):
        """Test that required directories exist"""
        required_dirs = [
            "data/cache/uv_cache",
            "data/cache/csv_converted",
            "data/raw_parquet",
            "results/plots",
            "logs",
            "tests"
        ]
        
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            assert full_path.exists(), f"Required directory should exist: {dir_path}"
            
    def test_script_permissions(self):
        """Test that all scripts have proper permissions"""
        scripts = [
            "container-entrypoint.sh",
            "scripts/native-container/setup.sh",
            "scripts/native-container/run.sh",
            "scripts/native-container/stop.sh",
            "scripts/native-container/exec.sh",
            "scripts/native-container/logs.sh",
            "scripts/native-container/cleanup.sh"
        ]
        
        for script_path in scripts:
            full_path = self.project_root / script_path
            assert os.access(full_path, os.X_OK), f"Script should be executable: {script_path}"
            
    def test_python_files_exist(self):
        """Test that all required Python files exist"""
        python_files = [
            "run_analysis.py",
            "neozork_mcp_server.py",
            "scripts/check_mcp_status.py",
            "tests/run_tests_docker.py"
        ]
        
        for file_path in python_files:
            full_path = self.project_root / file_path
            assert full_path.exists(), f"Python file should exist: {file_path}"
            
    def test_configuration_files_exist(self):
        """Test that all configuration files exist"""
        config_files = [
            "cursor_mcp_config.json",
            "requirements.txt",
            "uv_setup/uv.toml"
        ]
        
        for file_path in config_files:
            full_path = self.project_root / file_path
            assert full_path.exists(), f"Configuration file should exist: {file_path}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 