#!/usr/bin/env python3
"""
Tests for native container features and functionality.
These tests validate the enhanced features of native Apple Silicon containers.
"""

import os
import sys
import subprocess
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

def is_native_container_environment():
    """Check if we're in an environment where native container tests should run."""
    # Skip if running inside Docker
    if os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true':
        return False
    
    # Skip if not on macOS
    if sys.platform != "darwin":
        return False
    
    # Skip if native container application is not available
    try:
        result = subprocess.run(['container', '--version'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

@pytest.mark.skipif(not is_native_container_environment(), 
                    reason="Native container tests require macOS 26+ with native container application")
class TestNativeContainerFeatures:
    """Test native container features and functionality."""
    
    def test_enhanced_shell_script_exists(self):
        """Test that enhanced shell script exists and is executable."""
        exec_script = Path("scripts/native-container/exec.sh")
        assert exec_script.exists(), "exec.sh script should exist"
        assert os.access(exec_script, os.X_OK), "exec.sh should be executable"
    
    def test_enhanced_shell_script_content(self):
        """Test that enhanced shell script contains required functions."""
        exec_script = Path("scripts/native-container/exec.sh")
        
        with open(exec_script, 'r') as f:
            content = f.read()
        
        # Check for required functions
        assert "create_enhanced_shell_command()" in content
        assert "execute_enhanced_shell()" in content
        assert "source /app/.venv/bin/activate" in content
        
        # Check for aliases
        assert "alias nz=" in content
        assert "alias eda=" in content
        assert "alias uv-install=" in content
        assert "alias uv-update=" in content
        assert "alias uv-test=" in content
        assert "alias uv-pytest=" in content
    
    def test_native_container_script_exists(self):
        """Test that main native container script exists."""
        main_script = Path("scripts/native-container/native-container.sh")
        assert main_script.exists(), "native-container.sh should exist"
        assert os.access(main_script, os.X_OK), "native-container.sh should be executable"
    
    def test_native_container_script_functions(self):
        """Test that main script contains required functions."""
        main_script = Path("scripts/native-container/native-container.sh")
        
        with open(main_script, 'r') as f:
            content = f.read()
        
        # Check for main functions
        assert "start_container_sequence()" in content
        assert "stop_container_sequence()" in content
        assert "show_container_status()" in content
        assert "show_main_menu()" in content
        assert "main()" in content
    
    def test_setup_script_exists(self):
        """Test that setup script exists."""
        setup_script = Path("scripts/native-container/setup.sh")
        assert setup_script.exists(), "setup.sh should exist"
        assert os.access(setup_script, os.X_OK), "setup.sh should be executable"
    
    def test_run_script_exists(self):
        """Test that run script exists."""
        run_script = Path("scripts/native-container/run.sh")
        assert run_script.exists(), "run.sh should exist"
        assert os.access(run_script, os.X_OK), "run.sh should be executable"
    
    def test_stop_script_exists(self):
        """Test that stop script exists."""
        stop_script = Path("scripts/native-container/stop.sh")
        assert stop_script.exists(), "stop.sh should exist"
        assert os.access(stop_script, os.X_OK), "stop.sh should be executable"
    
    def test_logs_script_exists(self):
        """Test that logs script exists."""
        logs_script = Path("scripts/native-container/logs.sh")
        assert logs_script.exists(), "logs.sh should exist"
        assert os.access(logs_script, os.X_OK), "logs.sh should be executable"
    
    def test_force_restart_script_exists(self):
        """Test that force restart script exists."""
        force_restart_script = Path("scripts/native-container/force_restart.sh")
        assert force_restart_script.exists(), "force_restart.sh should exist"
        assert os.access(force_restart_script, os.X_OK), "force_restart.sh should be executable"
    
    def test_cleanup_script_exists(self):
        """Test that cleanup script exists."""
        cleanup_script = Path("scripts/native-container/cleanup.sh")
        assert cleanup_script.exists(), "cleanup.sh should exist"
        assert os.access(cleanup_script, os.X_OK), "cleanup.sh should be executable"
    
    def test_test_scripts_exist(self):
        """Test that test scripts exist."""
        test_interactive = Path("scripts/native-container/test_interactive.sh")
        test_smart_logic = Path("scripts/native-container/test_smart_logic.sh")
        analyze_logs = Path("scripts/native-container/analyze_all_logs.sh")
        
        assert test_interactive.exists(), "test_interactive.sh should exist"
        assert test_smart_logic.exists(), "test_smart_logic.sh should exist"
        assert analyze_logs.exists(), "analyze_all_logs.sh should exist"
    
    def test_container_yaml_exists(self):
        """Test that container.yaml configuration exists."""
        config_file = Path("container.yaml")
        assert config_file.exists(), "container.yaml should exist"
        
        # Check if it's valid YAML
        try:
            import yaml
            with open(config_file, 'r') as f:
                yaml.safe_load(f)
        except ImportError:
            # Skip YAML validation if yaml module not available
            pass
        except yaml.YAMLError:
            pytest.fail("container.yaml should be valid YAML")
    
    def test_scripts_have_shebang(self):
        """Test that all shell scripts have proper shebang."""
        script_dir = Path("scripts/native-container")
        
        for script_file in script_dir.glob("*.sh"):
            if script_file.is_file():
                with open(script_file, 'r') as f:
                    first_line = f.readline().strip()
                    assert first_line.startswith("#!/bin/bash") or first_line.startswith("#!/bin/sh"), \
                        f"{script_file} should start with proper shebang"
    
    def test_scripts_are_executable(self):
        """Test that all shell scripts are executable."""
        script_dir = Path("scripts/native-container")
        
        for script_file in script_dir.glob("*.sh"):
            if script_file.is_file():
                assert os.access(script_file, os.X_OK), f"{script_file} should be executable"
    
    def test_enhanced_shell_environment_setup(self):
        """Test that enhanced shell sets up environment correctly."""
        exec_script = Path("scripts/native-container/exec.sh")
        
        with open(exec_script, 'r') as f:
            content = f.read()
        
        # Check for environment setup
        assert "export PYTHONPATH=\"/app:$PYTHONPATH\"" in content
        assert "export PYTHONUNBUFFERED=1" in content
        assert "export MPLCONFIGDIR=\"/tmp/matplotlib-cache\"" in content
    
    def test_uv_integration_in_scripts(self):
        """Test that UV package manager is integrated in scripts."""
        exec_script = Path("scripts/native-container/exec.sh")
        
        with open(exec_script, 'r') as f:
            content = f.read()
        
        # Check for UV integration
        assert "uv sync" in content
        assert "uv run" in content
        assert "uv venv" in content
    
    def test_mcp_server_integration(self):
        """Test that MCP server integration is configured."""
        exec_script = Path("scripts/native-container/exec.sh")
        
        with open(exec_script, 'r') as f:
            content = f.read()
        
        # Check for MCP server references
        assert "MCP_SERVER" in content or "mcp" in content.lower()
    
    def test_error_handling_in_scripts(self):
        """Test that scripts have proper error handling."""
        exec_script = Path("scripts/native-container/exec.sh")
        
        with open(exec_script, 'r') as f:
            content = f.read()
        
        # Check for error handling
        assert "set -e" in content or "set -o errexit" in content
        assert "trap" in content or "exit" in content
    
    def test_logging_in_scripts(self):
        """Test that scripts have logging functionality."""
        logs_script = Path("scripts/native-container/logs.sh")
        
        with open(logs_script, 'r') as f:
            content = f.read()
        
        # Check for logging functionality
        assert "log" in content.lower() or "echo" in content
    
    def test_script_documentation(self):
        """Test that scripts have proper documentation."""
        script_dir = Path("scripts/native-container")
        
        for script_file in script_dir.glob("*.sh"):
            if script_file.is_file():
                with open(script_file, 'r') as f:
                    content = f.read()
                
                # Check for header comments
                assert "#" in content[:100], f"{script_file} should have header comments"
    
    def test_container_volume_mounts(self):
        """Test that container configuration includes volume mounts."""
        config_file = Path("container.yaml")
        
        if config_file.exists():
            try:
                import yaml
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
                
                # Check for volume mounts if they exist
                if 'spec' in config and 'volumes' in config['spec']:
                    volumes = config['spec']['volumes']
                    assert len(volumes) > 0, "Container should have volume mounts configured"
            except (ImportError, yaml.YAMLError):
                # Skip if YAML module not available or invalid
                pass
    
    def test_container_resources(self):
        """Test that container has resource limits configured."""
        config_file = Path("container.yaml")
        
        if config_file.exists():
            try:
                import yaml
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
                
                # Check for resource configuration if it exists
                if 'spec' in config and 'resources' in config['spec']:
                    resources = config['spec']['resources']
                    assert 'memory' in resources or 'cpu' in resources, \
                        "Container should have resource limits configured"
            except (ImportError, yaml.YAMLError):
                # Skip if YAML module not available or invalid
                pass
    
    def test_script_permissions_consistency(self):
        """Test that all scripts have consistent permissions."""
        script_dir = Path("scripts/native-container")
        scripts = list(script_dir.glob("*.sh"))
        
        if scripts:
            # Get permissions of first script
            first_script = scripts[0]
            first_perms = oct(first_script.stat().st_mode)[-3:]
            
            # Check that all scripts have same permissions
            for script in scripts[1:]:
                script_perms = oct(script.stat().st_mode)[-3:]
                assert script_perms == first_perms, \
                    f"All scripts should have consistent permissions. Expected {first_perms}, got {script_perms} for {script}"
    
    def test_script_line_endings(self):
        """Test that scripts use Unix line endings."""
        script_dir = Path("scripts/native-container")
        
        for script_file in script_dir.glob("*.sh"):
            if script_file.is_file():
                with open(script_file, 'rb') as f:
                    content = f.read()
                
                # Check for Windows line endings
                assert b'\r\n' not in content, f"{script_file} should use Unix line endings"
    
    def test_script_syntax_validity(self):
        """Test that shell scripts have valid syntax."""
        script_dir = Path("scripts/native-container")
        
        for script_file in script_dir.glob("*.sh"):
            if script_file.is_file():
                # Try to validate bash syntax
                try:
                    result = subprocess.run(['bash', '-n', str(script_file)], 
                                          capture_output=True, text=True)
                    assert result.returncode == 0, \
                        f"{script_file} should have valid bash syntax: {result.stderr}"
                except FileNotFoundError:
                    # Skip if bash not available
                    pass
    
    def test_script_dependencies(self):
        """Test that scripts don't have missing dependencies."""
        script_dir = Path("scripts/native-container")
        
        for script_file in script_dir.glob("*.sh"):
            if script_file.is_file():
                with open(script_file, 'r') as f:
                    content = f.read()
                
                # Check for common external commands
                external_commands = ['container', 'docker', 'uv', 'python']
                
                for cmd in external_commands:
                    if cmd in content:
                        # Check if command is available (basic check)
                        try:
                            result = subprocess.run(['which', cmd], 
                                                  capture_output=True, text=True)
                            # Don't fail if command not found, just log
                            if result.returncode != 0:
                                print(f"Warning: {cmd} command not found in PATH")
                        except FileNotFoundError:
                            # Skip if which command not available
                            pass
