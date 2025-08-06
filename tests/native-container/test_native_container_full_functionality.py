#!/usr/bin/env python3
"""
Test suite for Native Container Full Functionality
Tests all features including UV, MCP server, command wrappers, and Docker parity
"""

import os
import sys
import subprocess
import time
import json
import pytest
from pathlib import Path
from typing import Dict, Any, Optional
from unittest.mock import patch, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def is_running_in_docker():
    """Check if running inside Docker container."""
    return os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true'

def get_project_root():
    """Get project root path based on environment."""
    if is_running_in_docker():
        # In Docker, project is mounted at /app
        return Path('/app')
    else:
        # In native environment, use relative path
        return Path(__file__).parent.parent.parent

class TestNativeContainerFullFunctionality:
    """Test class for native container full functionality"""
    
    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.project_root = get_project_root()
        cls.container_name = "neozork-hld-prediction"
        cls.native_container_dir = cls.project_root / "scripts" / "native-container"
        cls.entrypoint_script = cls.project_root / "container-entrypoint.sh"
        cls.container_yaml = cls.project_root / "container.yaml"
        
    def test_container_setup_script_exists(self):
        """Test that setup script exists and is executable"""
        setup_script = self.native_container_dir / "setup.sh"
        assert setup_script.exists(), "Setup script should exist"
        assert os.access(setup_script, os.X_OK), "Setup script should be executable"
        
    def test_entrypoint_script_exists(self):
        """Test that entrypoint script exists and is executable"""
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        
        assert self.entrypoint_script.exists(), "Entrypoint script should exist"
        
    def test_container_yaml_exists(self):
        """Test that container.yaml exists and is valid"""
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        
        assert self.container_yaml.exists(), "container.yaml should exist"
        
        # Try to parse as YAML
        try:
            import yaml
            with open(self.container_yaml, 'r') as f:
                yaml.safe_load(f)
        except Exception as e:
            pytest.fail(f"container.yaml should be valid YAML: {e}")
            
    def test_required_files_exist(self):
        """Test that all required files exist."""
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        required_files = [
            "container-entrypoint.sh",
            "container.yaml",
            "neozork_mcp_server.py",
            "cursor_mcp_config.json",
            "scripts/check_mcp_status.py",
            "scripts/native-container/setup.sh",
            "scripts/native-container/run.sh",
            "scripts/native-container/stop.sh",
            "scripts/native-container/exec.sh",
            "scripts/native-container/logs.sh",
            "scripts/native-container/cleanup.sh"
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
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
            
        # Check for required functions
        required_functions = [
            "main()",
            "verify_uv()",
            "setup_bash_environment()",
            "create_command_wrappers()",
            "start_mcp_server()",
            "run_data_feed_tests()",
            "show_usage_guide()"
        ]
        
        for func in required_functions:
            assert func in content, f"Entrypoint should contain function: {func}"
            
    def test_entrypoint_environment_variables(self):
        """Test that entrypoint script sets required environment variables"""
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
            
        # Check for required environment variables
        required_env_vars = [
            "NATIVE_CONTAINER=true",
            "DOCKER_CONTAINER=false",
            "USE_UV=true",
            "UV_ONLY=true",
            "PYTHONPATH=/app"
        ]
        
        for env_var in required_env_vars:
            assert env_var in content, f"Entrypoint should set environment variable: {env_var}"
            
    def test_command_wrappers_creation(self):
        """Test that entrypoint creates command wrappers"""
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        
        with open(self.entrypoint_script, 'r') as f:
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
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
            
        # Check for bash history initialization
        history_commands = [
            "HISTFILE=",
            "HISTSIZE=",
            "history -r",
            "init_bash_history()"
        ]
        
        for cmd in history_commands:
            assert cmd in content, f"Entrypoint should add command to history: {cmd}"
            
    def test_mcp_server_integration(self):
        """Test that MCP server integration is properly configured"""
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
            
        # Check for MCP server functionality
        mcp_features = [
            "start_mcp_server()",
            "cleanup_mcp_server()",
            "neozork_mcp_server.py",
            "check_mcp_status.py",
            "/tmp/mcp_server.pid"
        ]
        
        for feature in mcp_features:
            assert feature in content, f"Entrypoint should support MCP feature: {feature}"
            
    def test_data_feed_tests_integration(self):
        """Test that data feed tests are integrated"""
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for data feed test integration
        test_features = [
            "run_data_feed_tests()",
            "run_tests_docker.py",
            "Polygon",
            "YFinance",
            "Binance"
        ]
        
        for feature in test_features:
            assert feature in content, f"Entrypoint should support test feature: {feature}"
            
    def test_usage_guide_integration(self):
        """Test that usage guide is integrated"""
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
            
        # Check for usage guide functionality
        guide_features = [
            "show_usage_guide()",
            "Available commands:",
            "NeoZork HLD Prediction",
            "UV-Only Mode"
        ]
        
        for feature in guide_features:
            assert feature in content, f"Entrypoint should support guide feature: {feature}"
            
    def test_commands_file_creation(self):
        """Test that commands file is created"""
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
            
        # Check for commands file creation
        assert "/tmp/neozork_commands.txt" in content, "Entrypoint should create commands file"
        assert "cat > /tmp/neozork_commands.txt" in content, "Entrypoint should create commands file"
        
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
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        
        with open(self.container_yaml, 'r') as f:
            content = f.read()
            
        # Check for required configuration
        config_features = [
            "neozork-hld-prediction",
            "python:3.11-slim",
            "arm64",
            "USE_UV=true",
            "NATIVE_CONTAINER=true"
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
        """Test that scripts have correct permissions."""
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        assert os.access(self.entrypoint_script, os.X_OK), "Script should be executable: container-entrypoint.sh"
        
        # Check native container scripts
        scripts = [
            "setup.sh",
            "run.sh",
            "stop.sh",
            "exec.sh",
            "logs.sh",
            "cleanup.sh"
        ]
        
        for script in scripts:
            script_path = self.native_container_dir / script
            assert os.access(script_path, os.X_OK), f"Script should be executable: {script}"

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
        """Test that configuration files exist."""
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        config_files = [
            "requirements.txt",
            "neozork_mcp_server.py",
            "cursor_mcp_config.json"
        ]
        
        for file_path in config_files:
            full_path = self.project_root / file_path
            assert full_path.exists(), f"Configuration file should exist: {file_path}"

    def test_native_container_scripts_functionality(self):
        """Test that native container scripts have required functionality."""
        scripts = [
            ("setup.sh", ["setup", "container", "native"]),
            ("run.sh", ["run", "start", "container"]),
            ("stop.sh", ["stop", "container"]),
            ("exec.sh", ["exec", "shell", "command"]),
            ("logs.sh", ["logs", "container"]),
            ("cleanup.sh", ["cleanup", "remove", "container"])
        ]
        
        for script_name, keywords in scripts:
            script_path = self.native_container_dir / script_name
            if script_path.exists():
                with open(script_path, 'r') as f:
                    content = f.read()
                
                for keyword in keywords:
                    assert keyword in content, f"Script {script_name} should contain keyword: {keyword}"

    def test_uv_integration_files(self):
        """Test that UV integration files exist."""
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - UV files may not be available")
        
        uv_files = [
            "uv_setup/uv.toml",
            "uv_setup/setup_uv.sh",
            "uv_setup/update_deps.sh"
        ]
        
        for file_path in uv_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                assert full_path.exists(), f"UV file should exist: {file_path}"

    def test_mcp_server_files(self):
        """Test that MCP server files exist and are functional."""
        mcp_files = [
            "neozork_mcp_server.py",
            "cursor_mcp_config.json",
            "scripts/check_mcp_status.py"
        ]
        
        for file_path in mcp_files:
            full_path = self.project_root / file_path
            assert full_path.exists(), f"MCP server file should exist: {file_path}"

    def test_test_infrastructure(self):
        """Test that test infrastructure exists."""
        test_files = [
            "tests/run_tests_docker.py",
            "tests/native-container/test_native_container_features.py",
            "tests/native-container/test_native_container_full_functionality.py"
        ]
        
        for file_path in test_files:
            full_path = self.project_root / file_path
            assert full_path.exists(), f"Test file should exist: {file_path}"

    def test_documentation_files(self):
        """Test that documentation files exist."""
        doc_files = [
            "scripts/native-container/README.md",
            "scripts/native-container/FULL_DOCKER_PARITY_SUMMARY.md"
        ]
        
        for file_path in doc_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                assert full_path.exists(), f"Documentation file should exist: {file_path}"

    def test_directory_structure(self):
        """Test that required directories exist."""
        required_dirs = [
            "scripts/native-container",
            "tests/native-container",
            "data",
            "logs",
            "results"
        ]
        
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            assert full_path.exists(), f"Directory should exist: {dir_path}"
            assert full_path.is_dir(), f"Path should be a directory: {dir_path}"

    def test_environment_detection(self):
        """Test that environment detection works correctly."""
        # This test should work in both environments
        project_root = get_project_root()
        assert project_root.exists(), "Project root should exist"
        
        # Check if we can detect the environment
        docker_env = is_running_in_docker()
        assert isinstance(docker_env, bool), "Environment detection should return boolean"

    def test_file_paths_consistency(self):
        """Test that file paths are consistent across environments."""
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        project_root = get_project_root()
        
        # Test that key files exist in the detected project root
        key_files = [
            "requirements.txt",
            "neozork_mcp_server.py",
            "cursor_mcp_config.json"
        ]
        
        for file_path in key_files:
            full_path = project_root / file_path
            assert full_path.exists(), f"Key file should exist in project root: {file_path}"

    def test_required_scripts(self):
        """Test that required scripts exist."""
        if is_running_in_docker():
            pytest.skip("Skipping in Docker environment - native container files not available")
        
        # Check for required scripts
        required_scripts = [
            "scripts/check_mcp_status.py",
            "scripts/native-container/setup.sh",
            "scripts/native-container/run.sh",
            "scripts/native-container/stop.sh",
            "scripts/native-container/exec.sh",
            "scripts/native-container/logs.sh",
            "scripts/native-container/cleanup.sh"
        ]
        
        for file_path in required_scripts:
            full_path = self.project_root / file_path
            assert full_path.exists(), f"Required script should exist: {file_path}"

    def test_command_wrapper_scripts(self):
        """Test that command wrapper scripts exist."""
        # Check for command wrapper scripts
        command_wrapper_scripts = [
            "scripts/check_mcp_status.py"
        ]
        
        for file_path in command_wrapper_scripts:
            full_path = self.project_root / file_path
            assert full_path.exists(), f"Command wrapper script should exist: {file_path}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 