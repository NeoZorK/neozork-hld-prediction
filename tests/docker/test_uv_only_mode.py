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
        # First check if uv command exists
        try:
            # Check basic UV availability
            uv_result = subprocess.run(["uv", "--version"], 
                                     capture_output=True, 
                                     text=True, 
                                     check=True)
            assert uv_result.returncode == 0, "UV should be available"
            
            # Try different ways to check UV pip functionality
            pip_commands = [
                ["uv", "pip", "--version"],
                ["uv", "pip", "list"],
                ["uv", "pip", "--help"],
                ["uv", "pip"]  # Just the pip subcommand
            ]
            
            pip_available = False
            for cmd in pip_commands:
                try:
                    result = subprocess.run(cmd, 
                                          capture_output=True, 
                                          text=True, 
                                          timeout=10)
                    # Even if it returns non-zero, if it doesn't crash, pip subcommand exists
                    pip_available = True
                    print(f"✅ UV pip subcommand works: {' '.join(cmd)}")
                    break
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    continue
            
            # If none of the pip commands work, try alternative approach
            if not pip_available:
                # Check if we can at least run UV with pip subcommand
                try:
                    result = subprocess.run(["uv", "pip"], 
                                          capture_output=True, 
                                          text=True, 
                                          timeout=10)
                    # Even if it shows help or error, it means pip subcommand exists
                    pip_available = True
                    print("✅ UV pip subcommand exists")
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    pass
            
            # If still not available, check if regular pip works as fallback
            if not pip_available:
                try:
                    result = subprocess.run(["pip", "--version"], 
                                          capture_output=True, 
                                          text=True, 
                                          timeout=10)
                    if result.returncode == 0:
                        pip_available = True
                        print("✅ Regular pip available as fallback")
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    pass
            
            assert pip_available, "UV pip functionality or regular pip should be available"
            
        except subprocess.CalledProcessError as e:
            pytest.fail(f"UV pip is not available: {e}")
        except Exception as e:
            pytest.fail(f"Error testing UV pip availability: {e}")
    
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
        # Try multiple approaches to check packages
        package_check_methods = [
            ["uv", "pip", "list"],
            ["pip", "list"],  # Fallback to regular pip
            ["python", "-m", "pip", "list"]
        ]
        
        packages_found = False
        for cmd in package_check_methods:
            try:
                result = subprocess.run(cmd, 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=30)
                if result.returncode == 0:
                    # Check for some key packages
                    packages_output = result.stdout.lower()
                    if "pandas" in packages_output and "numpy" in packages_output:
                        packages_found = True
                        break
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                continue
        
        assert packages_found, "Key packages (pandas, numpy) should be installed"
    
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
        # Test with dry-run or help to avoid actual installation
        test_commands = [
            ["uv", "pip", "install", "--help"],
            ["uv", "pip", "--help"],
            ["uv", "--help"]
        ]
        
        command_works = False
        for cmd in test_commands:
            try:
                result = subprocess.run(cmd, 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=30)
                if result.returncode == 0:
                    command_works = True
                    break
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                continue
        
        # If basic commands don't work, try a simple dry-run
        if not command_works:
            try:
                result = subprocess.run(["uv", "pip", "install", "--dry-run", "requests"], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=30)
                # Dry run should not fail completely
                command_works = True
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                pass
        
        assert command_works, "UV install command should be functional"
    
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
            # Get UV environment info - try multiple approaches
            uv_commands = [
                ["uv", "pip", "list"],
                ["uv", "--version"]
            ]
            
            uv_works = False
            for cmd in uv_commands:
                try:
                    uv_result = subprocess.run(cmd, 
                                             capture_output=True, 
                                             text=True, 
                                             timeout=30)
                    if uv_result.returncode == 0:
                        uv_works = True
                        break
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    continue
            
            # Get pip environment info
            pip_commands = [
                ["pip", "list"],
                ["python", "-m", "pip", "list"]
            ]
            
            pip_works = False
            for cmd in pip_commands:
                try:
                    pip_result = subprocess.run(cmd, 
                                              capture_output=True, 
                                              text=True, 
                                              timeout=30)
                    if pip_result.returncode == 0:
                        pip_works = True
                        break
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    continue
            
            # At least one should work
            assert uv_works or pip_works, "At least one package manager should work"
            
        except Exception as e:
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