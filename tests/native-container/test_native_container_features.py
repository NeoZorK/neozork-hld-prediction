"""
Tests for native container features.
Tests UV support, MCP server, nz/eda scripts, and command history functionality.
"""

import pytest
import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestNativeContainerFeatures:
    """Test native container features."""

    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.project_root = Path(__file__).parent.parent.parent
        cls.entrypoint_script = cls.project_root / "container-entrypoint.sh"
        cls.native_container_dir = cls.project_root / "scripts" / "native-container"

    def test_entrypoint_script_exists(self):
        """Test that the entrypoint script exists and is executable."""
        assert self.entrypoint_script.exists(), "container-entrypoint.sh should exist"
        assert os.access(self.entrypoint_script, os.X_OK), "container-entrypoint.sh should be executable"

    def test_entrypoint_script_uv_support(self):
        """Test that the entrypoint script has UV support."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for UV environment variables
        assert "USE_UV=true" in content, "USE_UV should be set to true"
        assert "UV_ONLY=true" in content, "UV_ONLY should be set to true"
        assert "UV_CACHE_DIR=" in content, "UV_CACHE_DIR should be defined"
        assert "UV_VENV_DIR=" in content, "UV_VENV_DIR should be defined"
        
        # Check for UV verification function
        assert "verify_uv()" in content, "verify_uv function should exist"
        assert "command -v uv" in content, "UV command check should exist"

    def test_entrypoint_script_mcp_support(self):
        """Test that the entrypoint script has MCP server support."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for MCP server functions
        assert "start_mcp_server()" in content, "start_mcp_server function should exist"
        assert "cleanup_mcp_server()" in content, "cleanup_mcp_server function should exist"
        assert "neozork_mcp_server.py" in content, "MCP server script should be referenced"
        assert "check_mcp_status.py" in content, "MCP status check should be referenced"

    def test_entrypoint_script_command_wrappers(self):
        """Test that the entrypoint script creates command wrappers."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for command wrapper creation
        assert "create_command_wrappers()" in content, "create_command_wrappers function should exist"
        assert "/tmp/bin/nz" in content, "nz command wrapper should be created"
        assert "/tmp/bin/eda" in content, "eda command wrapper should be created"
        assert "uv-install" in content, "uv-install wrapper should be created"
        assert "uv-update" in content, "uv-update wrapper should be created"
        assert "uv-test" in content, "uv-test wrapper should be created"

    def test_entrypoint_script_bash_history(self):
        """Test that the entrypoint script sets up bash history."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for bash history setup
        assert "setup_bash_environment()" in content, "setup_bash_environment function should exist"
        assert "init_bash_history()" in content, "init_bash_history function should exist"
        assert "HISTFILE=" in content, "HISTFILE should be defined"
        assert "HISTSIZE=" in content, "HISTSIZE should be defined"
        assert "history -r" in content, "History should be loaded"

    def test_entrypoint_script_useful_commands(self):
        """Test that the entrypoint script includes useful commands in history."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for useful commands in history
        useful_commands = [
            "uv run pytest tests -n auto",
            "nz --interactive",
            "eda -dqc",
            "nz demo --rule PHLD",
            "nz yfinance AAPL --rule PHLD",
            "nz mql5 BTCUSD --interval H4 --rule PHLD",
            "eda --data-quality-checks",
            "python scripts/check_mcp_status.py",
            "python neozork_mcp_server.py"
        ]
        
        for cmd in useful_commands:
            assert cmd in content, f"Useful command '{cmd}' should be in history"

    def test_entrypoint_script_data_feed_tests(self):
        """Test that the entrypoint script includes data feed tests."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for data feed test function
        assert "run_data_feed_tests()" in content, "run_data_feed_tests function should exist"
        assert "run_tests_docker.py" in content, "Docker test runner should be referenced"

    def test_entrypoint_script_error_handling(self):
        """Test that the entrypoint script has proper error handling."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for error handling
        assert "run_python_safely()" in content, "run_python_safely function should exist"
        assert "exit_code=" in content, "Exit code handling should exist"
        assert "Container will remain running" in content, "Container should remain running on errors"

    def test_entrypoint_script_interactive_shell(self):
        """Test that the entrypoint script starts interactive shell."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for interactive shell
        assert "exec bash -i" in content, "Should start interactive bash shell"

    def test_entrypoint_script_environment_variables(self):
        """Test that the entrypoint script sets correct environment variables."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for environment variables
        env_vars = [
            "NATIVE_CONTAINER=true",
            "DOCKER_CONTAINER=false",
            "PYTHONPATH=/app",
            "PYTHONUNBUFFERED=1",
            "PYTHONDONTWRITEBYTECODE=1",
            "MPLCONFIGDIR=/tmp/matplotlib-cache"
        ]
        
        for var in env_vars:
            assert var in content, f"Environment variable '{var}' should be set"

    def test_entrypoint_script_directory_creation(self):
        """Test that the entrypoint script creates necessary directories."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for directory creation
        directories = [
            "/app/data/cache/csv_converted",
            "/app/data/raw_parquet",
            "/app/logs",
            "/tmp/matplotlib-cache",
            "/app/results/plots",
            "/app/.pytest_cache",
            "/app/.uv_cache",
            "/app/.venv",
            "/tmp/bash_history",
            "/tmp/bin",
            "/tmp/bash_config"
        ]
        
        for directory in directories:
            assert directory in content, f"Directory '{directory}' should be created"

    def test_entrypoint_script_readline_config(self):
        """Test that the entrypoint script sets up readline configuration."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for readline configuration
        assert ".inputrc" in content, "Readline configuration should be created"
        assert "history-search-backward" in content, "History search should be configured"
        assert "history-search-forward" in content, "History search should be configured"
        assert "INPUTRC=" in content, "INPUTRC should be set"

    def test_entrypoint_script_custom_prompt(self):
        """Test that the entrypoint script sets custom prompt."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for custom prompt
        assert "PS1=" in content, "Custom prompt should be set"
        assert "neozork" in content, "Prompt should include 'neozork'"

    def test_entrypoint_script_mcp_server_management(self):
        """Test that the entrypoint script properly manages MCP server."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for MCP server management
        assert "nohup python neozork_mcp_server.py" in content, "MCP server should be started with nohup"
        assert "/tmp/mcp_server.pid" in content, "MCP server PID should be tracked"
        assert "trap cleanup_mcp_server EXIT" in content, "MCP server cleanup should be trapped"

    def test_entrypoint_script_html_file_detection(self):
        """Test that the entrypoint script detects HTML file generation."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for HTML file detection
        assert "*.html" in content, "HTML file detection should exist"
        assert "New HTML file generated" in content, "HTML file notification should exist"

    def test_entrypoint_script_welcome_message(self):
        """Test that the entrypoint script shows proper welcome message."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for welcome message
        assert "NeoZork HLD Prediction Native Container Started" in content, "Welcome message should exist"
        assert "UV-Only Mode" in content, "UV mode should be mentioned"
        assert "Available commands:" in content, "Available commands should be listed"

    def test_entrypoint_script_script_structure(self):
        """Test that the entrypoint script has proper structure."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for proper script structure
        assert "#!/bin/bash" in content, "Should start with shebang"
        assert "set -e" in content, "Should exit on error"
        assert "main()" in content, "Should have main function"
        assert "main \"$@\"" in content, "Should call main function"

    def test_entrypoint_script_logging(self):
        """Test that the entrypoint script has proper logging."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for logging function
        assert "log_message()" in content, "Logging function should exist"
        assert "date" in content, "Timestamps should be included in logs"

    def test_entrypoint_script_color_output(self):
        """Test that the entrypoint script uses colored output."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for colored output
        assert "\\033[1;32m" in content, "Green color should be used"
        assert "\\033[1;33m" in content, "Yellow color should be used"
        assert "\\033[1;31m" in content, "Red color should be used"
        assert "\\033[1;36m" in content, "Cyan color should be used"

    def test_entrypoint_script_path_management(self):
        """Test that the entrypoint script properly manages PATH."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for PATH management
        assert "export PATH=" in content, "PATH should be exported"
        assert "/tmp/bin:" in content, "Custom bin directory should be in PATH"

    def test_entrypoint_script_permissions(self):
        """Test that the entrypoint script sets proper permissions."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for permission settings
        assert "chmod 777" in content, "Directory permissions should be set"
        assert "chmod 666" in content, "File permissions should be set"
        assert "chmod +x" in content, "Executable permissions should be set"


class TestNativeContainerIntegration:
    """Integration tests for native container features."""

    def test_native_container_scripts_exist(self):
        """Test that all native container scripts exist."""
        project_root = Path(__file__).parent.parent.parent
        native_container_dir = project_root / "scripts" / "native-container"
        
        required_scripts = [
            "native-container.sh",
            "setup.sh",
            "run.sh",
            "stop.sh",
            "logs.sh",
            "exec.sh",
            "cleanup.sh"
        ]
        
        for script in required_scripts:
            script_path = native_container_dir / script
            assert script_path.exists(), f"Script {script} should exist"
            assert os.access(script_path, os.X_OK), f"Script {script} should be executable"

    def test_native_container_script_consistency(self):
        """Test that native container scripts are consistent with Docker features."""
        project_root = Path(__file__).parent.parent.parent
        
        # Check that nz and eda scripts exist
        nz_script = project_root / "nz"
        eda_script = project_root / "eda"
        
        if nz_script.exists():
            assert os.access(nz_script, os.X_OK), "nz script should be executable"
        
        if eda_script.exists():
            assert os.access(eda_script, os.X_OK), "eda script should be executable"

    def test_uv_configuration_files_exist(self):
        """Test that UV configuration files exist."""
        project_root = Path(__file__).parent.parent.parent
        
        # Check for UV configuration files
        uv_files = [
            "uv.toml",
            "requirements.txt"
        ]
        
        for file_name in uv_files:
            file_path = project_root / file_name
            assert file_path.exists(), f"UV file {file_name} should exist"

    def test_mcp_server_files_exist(self):
        """Test that MCP server files exist."""
        project_root = Path(__file__).parent.parent.parent
        
        # Check for MCP server files
        mcp_files = [
            "neozork_mcp_server.py",
            "scripts/check_mcp_status.py"
        ]
        
        for file_name in mcp_files:
            file_path = project_root / file_name
            assert file_path.exists(), f"MCP file {file_name} should exist"

    def test_test_files_exist(self):
        """Test that test files exist."""
        project_root = Path(__file__).parent.parent.parent
        
        # Check for test files
        test_files = [
            "tests/run_tests_docker.py",
            "scripts/test_uv_docker.py"
        ]
        
        for file_name in test_files:
            file_path = project_root / file_name
            assert file_path.exists(), f"Test file {file_name} should exist"


class TestNativeContainerDocumentation:
    """Tests for native container documentation."""

    def test_native_container_readme_exists(self):
        """Test that native container README exists."""
        project_root = Path(__file__).parent.parent.parent
        readme_path = project_root / "scripts" / "native-container" / "README.md"
        assert readme_path.exists(), "Native container README should exist"

    def test_native_container_documentation_completeness(self):
        """Test that native container documentation is complete."""
        project_root = Path(__file__).parent.parent.parent
        readme_path = project_root / "scripts" / "native-container" / "README.md"
        
        with open(readme_path, 'r') as f:
            content = f.read()
        
        # Check for important documentation sections
        sections = [
            "Native Apple Silicon Container",
            "Quick Start",
            "Prerequisites",
            "Scripts Overview",
            "Available Commands",
            "Configuration",
            "Testing",
            "Troubleshooting"
        ]
        
        for section in sections:
            assert section in content, f"Documentation section '{section}' should exist" 