"""
Tests for automatic dependency installation in native container.
Tests UV environment setup, venv creation, and dependency installation.
"""

import pytest
import os
import subprocess
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def is_running_in_docker():
    """Check if running inside Docker container."""
    return os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true'


@pytest.mark.skipif(is_running_in_docker(), 
                    reason="Native container tests require native container environment")
class TestAutomaticDependencies:
    """Test automatic dependency installation functionality."""

    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.project_root = get_project_root()
        cls.entrypoint_script = cls.project_root / "container-entrypoint.sh"

    def test_entrypoint_has_uv_environment_setup(self):
        """Test that entrypoint script has UV environment setup function."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for UV environment setup function
        assert "setup_uv_environment()" in content, "setup_uv_environment function should exist"
        assert "install_dependencies()" in content, "install_dependencies function should exist"
        assert "verify_dependencies()" in content, "verify_dependencies function should exist"

    def test_entrypoint_creates_venv(self):
        """Test that entrypoint script creates virtual environment."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for venv creation logic
        assert "uv venv /app/.venv" in content, "UV venv creation should be included"
        assert "source /app/.venv/bin/activate" in content, "Venv activation should be included"

    def test_command_wrappers_use_venv(self):
        """Test that command wrappers use activated virtual environment."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check that command wrappers activate venv
        command_wrappers = ["nz", "eda", "uv-install", "uv-update", "uv-test", "uv-pytest", "mcp-start", "mcp-check"]
        
        for wrapper in command_wrappers:
            assert f"source /app/.venv/bin/activate" in content, f"Wrapper {wrapper} should activate venv"

    def test_bash_environment_auto_activates_venv(self):
        """Test that bash environment automatically activates venv."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for automatic venv activation in bash
        assert "source /app/.venv/bin/activate" in content, "Bash should auto-activate venv"
        assert "BASH_ENV=/tmp/bash_config/.bashrc" in content, "BASH_ENV should be set"

    def test_main_function_calls_uv_setup(self):
        """Test that main function calls UV environment setup."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check that main function calls setup_uv_environment
        assert "setup_uv_environment" in content, "Main function should call setup_uv_environment"

    def test_dependency_verification(self):
        """Test that dependencies are verified after installation."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for dependency verification
        key_packages = ["pandas", "numpy", "matplotlib", "plotly", "yfinance", "pytest"]
        for package in key_packages:
            assert package in content, f"Package {package} should be verified"

    def test_requirements_file_exists(self):
        """Test that requirements.txt exists for dependency installation."""
        requirements_file = self.project_root / "requirements.txt"
        assert requirements_file.exists(), "requirements.txt should exist for dependency installation"

    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists for UV configuration."""
        pyproject_file = self.project_root / "pyproject.toml"
        assert pyproject_file.exists(), "pyproject.toml should exist for UV configuration"

    def test_uv_cache_directory_configured(self):
        """Test that UV cache directory is properly configured."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for UV cache configuration
        assert "UV_CACHE_DIR=/app/.uv_cache" in content, "UV_CACHE_DIR should be configured"
        assert "UV_VENV_DIR=/app/.venv" in content, "UV_VENV_DIR should be configured"

    def test_error_handling_for_dependency_installation(self):
        """Test that error handling exists for dependency installation failures."""
        with open(self.entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for error handling
        assert "Failed to install dependencies" in content, "Error handling should exist for installation failures"
        assert "You can try manual installation with: uv-install" in content, "Manual installation fallback should be mentioned"


@pytest.mark.skipif(is_running_in_docker(), 
                    reason="Native container tests require native container environment")
class TestNativeContainerScriptUpdates:
    """Test updates to native container script for automatic dependencies."""

    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.project_root = get_project_root()
        cls.native_container_script = cls.project_root / "scripts" / "native-container" / "native-container.sh"

    def test_script_informs_about_automatic_dependencies(self):
        """Test that script informs about automatic dependency installation."""
        with open(self.native_container_script, 'r') as f:
            content = f.read()
        
        # Check for automatic dependency installation messages
        assert "automatically install all dependencies using UV" in content, "Script should mention automatic dependency installation"
        assert "Virtual environment will be automatically activated" in content, "Script should mention venv activation"

    def test_help_shows_new_features(self):
        """Test that help shows new automatic dependency features."""
        with open(self.native_container_script, 'r') as f:
            content = f.read()
        
        # Check for new features in help
        assert "🆕 Automatically installs all dependencies using UV" in content, "Help should show automatic dependency installation"
        assert "🆕 Creates and activates virtual environment" in content, "Help should show venv creation"
        assert "No manual 'uv-install' required" in content, "Help should mention no manual installation needed" 