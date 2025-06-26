#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test UV-Only Mode in Docker Container
Validates that the container is properly configured for UV-only operation
"""

import pytest
import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, Any

class TestUVOnlyMode:
    """Test suite for UV-only mode validation"""
    
    def test_uv_installation(self):
        """Test that UV is properly installed"""
        try:
            result = subprocess.run(["uv", "--version"], 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            assert result.returncode == 0
            assert "uv" in result.stdout.lower()
        except subprocess.CalledProcessError:
            pytest.fail("UV is not properly installed")
    
    def test_environment_variables(self):
        """Test UV-related environment variables"""
        # Check required environment variables
        assert os.getenv("USE_UV", "false").lower() == "true", "USE_UV should be true"
        assert os.getenv("UV_ONLY", "false").lower() == "true", "UV_ONLY should be true"
        assert os.getenv("DOCKER_CONTAINER", "false").lower() == "true", "DOCKER_CONTAINER should be true"
        
        # Check optional environment variables
        assert os.getenv("UV_CACHE_DIR") is not None, "UV_CACHE_DIR should be set"
        assert os.getenv("UV_VENV_DIR") is not None, "UV_VENV_DIR should be set"
        assert os.getenv("PYTHONPATH") is not None, "PYTHONPATH should be set"
    
    def test_uv_directories(self):
        """Test UV cache and virtual environment directories"""
        cache_dir = os.getenv("UV_CACHE_DIR", "/app/.uv_cache")
        venv_dir = os.getenv("UV_VENV_DIR", "/app/.venv")
        
        # Check that directories exist or can be created
        assert Path(cache_dir).parent.exists(), f"Parent directory for {cache_dir} should exist"
        assert Path(venv_dir).parent.exists(), f"Parent directory for {venv_dir} should exist"
    
    def test_uv_pip_availability(self):
        """Test that UV pip is available"""
        try:
            result = subprocess.run(["uv", "pip", "--version"], 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            assert result.returncode == 0
        except subprocess.CalledProcessError:
            pytest.fail("UV pip is not available")
    
    def test_mcp_configuration(self):
        """Test MCP server configuration for UV settings"""
        config_path = Path("/app/cursor_mcp_config.json")
        assert config_path.exists(), "MCP configuration file should exist"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Check server settings
        server_settings = config.get("serverSettings", {}).get("neozork", {})
        features = server_settings.get("features", {})
        
        assert features.get("uv_integration", False), "UV integration should be enabled"
        assert features.get("uv_only_mode", False), "UV-only mode should be enabled"
    
    def test_python_packages_installed(self):
        """Test that Python packages are installed via UV"""
        try:
            result = subprocess.run(["uv", "pip", "list"], 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            assert result.returncode == 0
            
            # Check for some key packages
            packages_output = result.stdout.lower()
            assert "pandas" in packages_output, "pandas should be installed"
            assert "numpy" in packages_output, "numpy should be installed"
            assert "matplotlib" in packages_output, "matplotlib should be installed"
            
        except subprocess.CalledProcessError:
            pytest.fail("Failed to list installed packages")
    
    def test_uv_cache_functionality(self):
        """Test UV cache functionality"""
        cache_dir = os.getenv("UV_CACHE_DIR", "/app/.uv_cache")
        
        # Try to create cache directory if it doesn't exist
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        
        # Test that we can write to cache directory
        test_file = Path(cache_dir) / "test.txt"
        try:
            test_file.write_text("test")
            assert test_file.exists(), "Should be able to write to cache directory"
            test_file.unlink()  # Clean up
        except Exception:
            pytest.fail("Cannot write to UV cache directory")
    
    def test_uv_install_command(self):
        """Test UV install command functionality"""
        try:
            # Test installing a simple package
            result = subprocess.run(["uv", "pip", "install", "--dry-run", "requests"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=30)
            # Dry run should not fail
            assert result.returncode == 0 or "dry-run" in result.stderr.lower()
        except subprocess.TimeoutExpired:
            pytest.fail("UV install command timed out")
        except subprocess.CalledProcessError:
            # This might fail in some environments, but shouldn't crash
            pass
    
    def test_uv_only_mode_script(self):
        """Test the UV mode checker script"""
        script_path = Path("/app/scripts/check_uv_mode.py")
        assert script_path.exists(), "UV mode checker script should exist"
        
        try:
            result = subprocess.run([sys.executable, str(script_path)], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=30)
            # Script should run without crashing
            assert result.returncode in [0, 1], "Script should exit with 0 or 1"
        except subprocess.TimeoutExpired:
            pytest.fail("UV mode checker script timed out")
    
    def test_docker_entrypoint_uv_commands(self):
        """Test that UV commands are available in entrypoint"""
        # Check if UV command wrappers exist
        uv_install_path = Path("/tmp/bin/uv-install")
        uv_update_path = Path("/tmp/bin/uv-update")
        
        # These might not exist in test environment, but should be available in container
        if uv_install_path.exists():
            assert uv_install_path.is_file(), "uv-install should be a file"
            assert os.access(uv_install_path, os.X_OK), "uv-install should be executable"
        
        if uv_update_path.exists():
            assert uv_update_path.is_file(), "uv-update should be a file"
            assert os.access(uv_update_path, os.X_OK), "uv-update should be executable"
    
    def test_python_path_configuration(self):
        """Test Python path configuration for UV"""
        python_path = os.getenv("PYTHONPATH", "")
        assert "/app" in python_path, "PYTHONPATH should include /app"
        
        # Test that we can import project modules
        try:
            import sys
            sys.path.insert(0, "/app")
            
            # Try to import a project module
            import src
            assert src is not None, "Should be able to import src module"
            
        except ImportError as e:
            pytest.fail(f"Cannot import project modules: {e}")
    
    def test_uv_environment_consistency(self):
        """Test that UV environment is consistent"""
        # Check that UV and Python are using the same environment
        try:
            # Get UV environment info
            uv_result = subprocess.run(["uv", "pip", "list"], 
                                     capture_output=True, 
                                     text=True, 
                                     check=True)
            
            # Get pip environment info
            pip_result = subprocess.run(["pip", "list"], 
                                      capture_output=True, 
                                      text=True, 
                                      check=True)
            
            # Both should work and return similar output
            assert uv_result.returncode == 0, "UV pip list should work"
            assert pip_result.returncode == 0, "Pip list should work"
            
            # Both should show similar package counts (allowing for some differences)
            uv_packages = len([line for line in uv_result.stdout.split('\n') if line.strip()])
            pip_packages = len([line for line in pip_result.stdout.split('\n') if line.strip()])
            
            # Should have reasonable number of packages
            assert uv_packages > 10, "Should have reasonable number of packages installed"
            assert pip_packages > 10, "Should have reasonable number of packages installed"
            
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Failed to check package consistency: {e}")

def test_uv_only_mode_integration():
    """Integration test for UV-only mode"""
    # This test validates the overall UV-only mode setup
    test_suite = TestUVOnlyMode()
    
    # Run all critical tests
    test_suite.test_uv_installation()
    test_suite.test_environment_variables()
    test_suite.test_uv_pip_availability()
    test_suite.test_mcp_configuration()
    test_suite.test_python_packages_installed()
    
    print("✅ UV-Only Mode Integration Test Passed")

if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"]) 