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


def is_running_in_docker():
    """Check if running inside Docker container."""
    return os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true'


def is_running_in_native_container():
    """Check if running inside native container environment."""
    return os.environ.get('NATIVE_CONTAINER') == 'true'


def should_skip_native_container_tests():
    """Check if native container tests should be skipped."""
    # Skip if running in Docker (native container files not available)
    if is_running_in_docker():
        return True, "Skipping in Docker environment - native container files not available"
    
    # Skip if not running in native container environment
    if not is_running_in_native_container():
        return True, "Skipping outside native container environment - tests require native container setup"
    
    return False, None


def get_project_root():
    """Get project root path based on environment."""
    if is_running_in_docker():
        # In Docker, project is mounted at /app
        return Path('/app')
    else:
        # In native environment, use relative path
        return Path(__file__).parent.parent.parent


class TestNativeContainerFeatures:
    """Test native container features."""

    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.project_root = get_project_root()
        cls.entrypoint_script = cls.project_root / "container-entrypoint.sh"
        cls.native_container_dir = cls.project_root / "scripts" / "native-container"

    def test_entrypoint_script_exists(self):
        """Test that the entrypoint script exists and is executable."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        assert self.entrypoint_script.exists(), "container-entrypoint.sh should exist"
        assert os.access(self.entrypoint_script, os.X_OK), "container-entrypoint.sh should be executable"

    def test_entrypoint_script_uv_support(self):
        """Test that the entrypoint script has UV support."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
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
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for MCP server functions
        assert "start_mcp_server()" in content, "start_mcp_server function should exist"
        assert "cleanup_mcp_server()" in content, "cleanup_mcp_server function should exist"
        assert "neozork_mcp_server.py" in content, "MCP server script should be referenced"
        assert "check_mcp_status.py" in content, "MCP status check should be referenced"

    def test_entrypoint_script_command_wrappers(self):
        """Test that the entrypoint script creates command wrappers."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
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
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
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
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
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
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for data feed test function
        assert "run_data_feed_tests()" in content, "run_data_feed_tests function should exist"
        assert "run_tests_docker.py" in content, "Docker test runner should be referenced"

    def test_entrypoint_script_error_handling(self):
        """Test that the entrypoint script has proper error handling."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for error handling
        assert "run_python_safely()" in content, "run_python_safely function should exist"
        assert "exit_code=" in content, "Exit code handling should exist"
        assert "Container will remain running" in content, "Container should remain running on errors"

    def test_entrypoint_script_interactive_shell(self):
        """Test that the entrypoint script starts interactive shell."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for interactive shell - the script uses "exec bash" not "exec bash -i"
        assert "exec bash" in content, "Should start interactive bash shell"

    def test_entrypoint_script_environment_variables(self):
        """Test that the entrypoint script sets correct environment variables."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
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
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
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
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for readline configuration
        assert ".inputrc" in content, "Readline configuration should be created"
        assert "history-search-backward" in content, "History search should be configured"
        assert "history-search-forward" in content, "History search should be configured"
        assert "INPUTRC=" in content, "INPUTRC should be set"

    def test_entrypoint_script_custom_prompt(self):
        """Test that the entrypoint script sets custom prompt."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for custom prompt
        assert "PS1=" in content, "Custom prompt should be set"
        assert "neozork" in content, "Prompt should include 'neozork'"

    def test_entrypoint_script_mcp_server_management(self):
        """Test that the entrypoint script properly manages MCP server."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for MCP server management
        assert "nohup python neozork_mcp_server.py" in content, "MCP server should be started with nohup"
        assert "/tmp/mcp_server.pid" in content, "MCP server PID should be tracked"
        assert "trap cleanup_mcp_server EXIT" in content, "MCP server cleanup should be trapped"

    def test_entrypoint_script_html_file_detection(self):
        """Test that the entrypoint script detects HTML file generation."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for HTML file detection
        assert "results/plots" in content, "Results plots directory should be checked"
        assert "*.html" in content, "HTML file pattern should be checked"
        assert "New HTML file generated" in content, "HTML file detection message should exist"

    def test_entrypoint_script_welcome_message(self):
        """Test that the entrypoint script displays welcome message."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for welcome message - the script has "NeoZork HLD Prediction" in comments and usage guide
        assert "NeoZork HLD Prediction" in content, "Welcome message should exist"
        assert "Usage Guide" in content, "Usage guide should be mentioned"

    def test_entrypoint_script_script_structure(self):
        """Test that the entrypoint script has proper structure."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for script structure
        assert "#!/bin/bash" in content, "Script should start with shebang"
        assert "set -e" in content, "Script should exit on error"
        assert "main()" in content, "Main function should exist"
        assert "main \"$@\"" in content, "Main function should be called"

    def test_entrypoint_script_logging(self):
        """Test that the entrypoint script has logging functionality."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for logging
        assert "log_message()" in content, "Log message function should exist"
        assert "date" in content, "Timestamp should be used in logging"

    def test_entrypoint_script_color_output(self):
        """Test that the entrypoint script uses colored output."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for color output
        assert "\\033[" in content, "ANSI color codes should be used"
        assert "\\033[0m" in content, "Color reset should be used"

    def test_entrypoint_script_path_management(self):
        """Test that the entrypoint script manages PATH correctly."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for PATH management
        assert "export PATH=" in content, "PATH should be exported"
        assert "/tmp/bin" in content, "Custom bin directory should be in PATH"

    def test_entrypoint_script_permissions(self):
        """Test that the entrypoint script sets proper permissions."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for permission setting
        assert "chmod +x" in content, "Executable permissions should be set"
        assert "chmod 777" in content, "Directory permissions should be set"


class TestNativeContainerIntegration:
    """Test native container integration features."""

    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.project_root = get_project_root()
        cls.native_container_dir = cls.project_root / "scripts" / "native-container"

    def test_native_container_scripts_exist(self):
        """Test that native container scripts exist."""
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
            assert script_path.exists(), f"Script {script} should exist"
            assert os.access(script_path, os.X_OK), f"Script {script} should be executable"

    def test_native_container_script_consistency(self):
        """Test that native container scripts have consistent structure."""
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
            with open(script_path, 'r') as f:
                content = f.read()
            
            # Check for common elements
            assert "#!/bin/bash" in content, f"Script {script} should start with shebang"
            assert "set -e" in content, f"Script {script} should exit on error"

    def test_uv_configuration_files_exist(self):
        """Test that UV configuration files exist."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        uv_files = [
            "uv_setup/uv.toml",
            "uv_setup/setup_uv.sh",
            "uv_setup/update_deps.sh"
        ]
        
        for file_path in uv_files:
            full_path = self.project_root / file_path
            assert full_path.exists(), f"UV file {file_path} should exist"

    def test_mcp_server_files_exist(self):
        """Test that MCP server files exist."""
        mcp_files = [
            "neozork_mcp_server.py",
            "cursor_mcp_config.json",
            "scripts/check_mcp_status.py"
        ]
        
        for file_path in mcp_files:
            full_path = self.project_root / file_path
            assert full_path.exists(), f"MCP server file {file_path} should exist"

    def test_test_files_exist(self):
        """Test that test files exist."""
        test_files = [
            "tests/run_tests_docker.py",
            "tests/native-container/test_native_container_full_functionality.py"
        ]
        
        for file_path in test_files:
            full_path = self.project_root / file_path
            assert full_path.exists(), f"Test file {file_path} should exist"


class TestNativeContainerDocumentation:
    """Test native container documentation."""

    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.project_root = get_project_root()

    def test_native_container_documentation_completeness(self):
        """Test that native container documentation is complete."""
        should_skip, reason = should_skip_native_container_tests()
        if should_skip:
            pytest.skip(reason)
        
        # Check main README for native container section
        main_readme = self.project_root / "README.md"
        if main_readme.exists():
            with open(main_readme, 'r') as f:
                content = f.read()
            
            # Check for native container section
            assert "Native Apple Silicon Container" in content, "Native container section should exist in main README"
            assert "FULL DOCKER PARITY" in content, "Docker parity should be mentioned" 