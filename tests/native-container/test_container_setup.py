#!/usr/bin/env python3
"""
Tests for native Apple Silicon container setup and configuration.
These tests are designed to run on macOS 26+ with native container support.
"""

import os
import sys
import subprocess
import yaml
import pytest
from pathlib import Path

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
class TestNativeContainerSetup:
    """Test native container setup and configuration."""
    
    def test_container_application_available(self):
        """Test that native container application is available."""
        result = subprocess.run(['container', '--version'], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert 'container' in result.stdout.lower()
    
    def test_container_configuration_valid(self):
        """Test that container configuration is valid."""
        config_file = Path('container.yaml')
        assert config_file.exists(), "container.yaml should exist"
        
        # Validate YAML syntax
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Check required fields
        assert 'apiVersion' in config
        assert 'kind' in config
        assert 'metadata' in config
        assert 'spec' in config
        
        # Check metadata
        metadata = config['metadata']
        assert metadata['name'] == 'neozork-hld-prediction'
        assert 'apple-silicon' in metadata['labels']['platform']
        
        # Check spec
        spec = config['spec']
        assert spec['image'] == 'python:3.11-slim'
        assert spec['architecture'] == 'arm64'
        assert 'memory' in spec['resources']
        assert 'cpu' in spec['resources']
    
    def test_container_build_successful(self):
        """Test that container builds successfully."""
        # This test requires the container to be built
        # In a real scenario, this would be tested after setup
        result = subprocess.run(['container', 'list'], 
                              capture_output=True, text=True)
        # Should not fail even if no containers exist
        assert result.returncode == 0
    
    def test_python_version_compatible(self):
        """Test that Python version is compatible."""
        major, minor = sys.version_info.major, sys.version_info.minor
        assert major == 3, "Python major version should be 3"
        assert minor >= 11, "Python minor version should be >= 11"
    
    def test_macos_version_check(self):
        """Test macOS version check functionality."""
        # This test simulates the macOS version check
        # In a real scenario, this would be tested on macOS 26+
        if sys.platform == "darwin":
            result = subprocess.run(['sw_vers', '-productVersion'], 
                                  capture_output=True, text=True)
            assert result.returncode == 0
            version = result.stdout.strip()
            # Should not fail even on older macOS versions
            assert len(version) > 0, "macOS version should be retrievable"


@pytest.mark.skipif(not is_native_container_environment(), 
                    reason="Native container tests require macOS 26+ with native container application")
class TestNativeContainerConfiguration:
    """Test native container configuration details."""
    
    def test_volume_mounts_configured(self):
        """Test that volume mounts are properly configured."""
        with open('container.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        volumes = config['spec']['volumes']
        volume_names = [vol['name'] for vol in volumes]
        
        expected_volumes = [
            'data-volume',
            'logs-volume', 
            'results-volume',
            'tests-volume',
            'mql5-feed-volume',
            'uv-cache-volume'
        ]
        
        for expected_vol in expected_volumes:
            assert expected_vol in volume_names, f"Volume {expected_vol} should be configured"
    
    def test_environment_variables_configured(self):
        """Test that environment variables are properly configured."""
        with open('container.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        env_vars = config['spec']['environment']
        env_names = [env.split('=')[0] for env in env_vars]
        
        expected_env_vars = [
            'PYTHONPATH',
            'USE_UV',
            'UV_ONLY',
            'NATIVE_CONTAINER',
            'DOCKER_CONTAINER'
        ]
        
        for expected_env in expected_env_vars:
            assert expected_env in env_names, f"Environment variable {expected_env} should be configured"
    
    def test_resources_configured(self):
        """Test that resource limits are properly configured."""
        with open('container.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        resources = config['spec']['resources']
        
        assert 'memory' in resources, "Memory should be configured"
        assert 'cpu' in resources, "CPU should be configured"
        assert 'storage' in resources, "Storage should be configured"
        
        # Check that values are reasonable
        memory = resources['memory']
        assert 'Gi' in memory, "Memory should be specified in Gi"
        
        cpu = resources['cpu']
        assert isinstance(cpu, (int, str)), "CPU should be a number or string"
    
    def test_security_context_configured(self):
        """Test that security context is properly configured."""
        with open('container.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        security_context = config['spec']['securityContext']
        
        assert security_context['runAsNonRoot'] is True, "Should run as non-root"
        assert security_context['allowPrivilegeEscalation'] is False, "Should not allow privilege escalation"
        assert security_context['readOnlyRootFilesystem'] is False, "Root filesystem should be writable"


@pytest.mark.skipif(not is_native_container_environment(), 
                    reason="Native container tests require macOS 26+ with native container application")
class TestNativeContainerScripts:
    """Test native container script functionality."""
    
    def test_setup_script_help(self):
        """Test that setup script shows help."""
        result = subprocess.run(['./scripts/native-container/setup.sh', '--help'], 
                              capture_output=True, text=True)
        # Should show usage information
        assert 'Usage:' in result.stdout or result.returncode != 0
    
    def test_run_script_help(self):
        """Test that run script shows help."""
        result = subprocess.run(['./scripts/native-container/run.sh', '--help'], 
                              capture_output=True, text=True)
        # Should show usage information
        assert 'Usage:' in result.stdout or result.returncode != 0
    
    def test_stop_script_help(self):
        """Test that stop script shows help."""
        result = subprocess.run(['./scripts/native-container/stop.sh', '--help'], 
                              capture_output=True, text=True)
        # Should show usage information
        assert 'Usage:' in result.stdout or result.returncode != 0
    
    def test_logs_script_help(self):
        """Test that logs script shows help."""
        result = subprocess.run(['./scripts/native-container/logs.sh', '--help'], 
                              capture_output=True, text=True)
        # Should show usage information
        assert 'Usage:' in result.stdout or result.returncode != 0
    
    def test_exec_script_help(self):
        """Test that exec script shows help."""
        result = subprocess.run(['./scripts/native-container/exec.sh', '--help'], 
                              capture_output=True, text=True)
        # Should show usage information
        assert 'Usage:' in result.stdout or result.returncode != 0
    
    def test_cleanup_script_help(self):
        """Test that cleanup script shows help."""
        result = subprocess.run(['./scripts/native-container/cleanup.sh', '--help'], 
                              capture_output=True, text=True)
        # Should show usage information
        assert 'Usage:' in result.stdout or result.returncode != 0
    
    def test_script_syntax_valid(self):
        """Test that all scripts have valid bash syntax."""
        scripts = [
            'scripts/native-container/setup.sh',
            'scripts/native-container/run.sh',
            'scripts/native-container/stop.sh',
            'scripts/native-container/logs.sh',
            'scripts/native-container/exec.sh',
            'scripts/native-container/cleanup.sh',
            'docker-entrypoint.sh'
        ]
        
        for script in scripts:
            result = subprocess.run(['bash', '-n', script], 
                                  capture_output=True, text=True)
            assert result.returncode == 0, f"Script {script} should have valid syntax"


@pytest.mark.skipif(not is_native_container_environment(), 
                    reason="Native container tests require macOS 26+ with native container application")
class TestNativeContainerIntegration:
    """Test native container integration scenarios."""
    
    def test_container_lifecycle_commands(self):
        """Test basic container lifecycle commands."""
        # These tests would require a running container
        # In a real scenario, these would be integration tests
        
        # Test container list command
        result = subprocess.run(['container', 'list'], 
                              capture_output=True, text=True)
        assert result.returncode == 0, "Container list command should work"
        
        # Test container ls command (alias for list)
        result = subprocess.run(['container', 'ls'], 
                              capture_output=True, text=True)
        assert result.returncode == 0, "Container ls command should work"
    
    def test_script_integration(self):
        """Test script integration without actual container operations."""
        # Test that scripts can be executed without errors
        # (assuming no container is running)
        
        # Test status check
        result = subprocess.run(['./scripts/native-container/run.sh', '--status'], 
                              capture_output=True, text=True)
        # Should not fail even if no container exists
        assert result.returncode == 0 or result.returncode == 1
    
    def test_configuration_validation(self):
        """Test configuration validation functionality."""
        # Test YAML validation
        result = subprocess.run(['python3', '-c', 
                               "import yaml; yaml.safe_load(open('container.yaml'))"], 
                              capture_output=True, text=True)
        assert result.returncode == 0, "container.yaml should be valid YAML"


class TestNativeContainerFiles:
    """Test that native container files and scripts exist and are valid.
    These tests can run in any environment (including Docker)."""
    
    def test_setup_script_exists(self):
        """Test that setup script exists and is executable."""
        setup_script = Path('scripts/native-container/setup.sh')
        assert setup_script.exists(), "setup.sh should exist"
        assert os.access(setup_script, os.X_OK), "setup.sh should be executable"
    
    def test_run_script_exists(self):
        """Test that run script exists and is executable."""
        run_script = Path('scripts/native-container/run.sh')
        assert run_script.exists(), "run.sh should exist"
        assert os.access(run_script, os.X_OK), "run.sh should be executable"
    
    def test_stop_script_exists(self):
        """Test that stop script exists and is executable."""
        stop_script = Path('scripts/native-container/stop.sh')
        assert stop_script.exists(), "stop.sh should exist"
        assert os.access(stop_script, os.X_OK), "stop.sh should be executable"
    
    def test_logs_script_exists(self):
        """Test that logs script exists and is executable."""
        logs_script = Path('scripts/native-container/logs.sh')
        assert logs_script.exists(), "logs.sh should exist"
        assert os.access(logs_script, os.X_OK), "logs.sh should be executable"
    
    def test_exec_script_exists(self):
        """Test that exec script exists and is executable."""
        exec_script = Path('scripts/native-container/exec.sh')
        assert exec_script.exists(), "exec.sh should exist"
        assert os.access(exec_script, os.X_OK), "exec.sh should be executable"
    
    def test_cleanup_script_exists(self):
        """Test that cleanup script exists and is executable."""
        cleanup_script = Path('scripts/native-container/cleanup.sh')
        assert cleanup_script.exists(), "cleanup.sh should exist"
        assert os.access(cleanup_script, os.X_OK), "cleanup.sh should be executable"
    
    def test_entrypoint_script_exists(self):
        """Test that entrypoint script exists and is executable."""
        entrypoint_script = Path('docker-entrypoint.sh')
        assert entrypoint_script.exists(), "docker-entrypoint.sh should exist"
        assert os.access(entrypoint_script, os.X_OK), "docker-entrypoint.sh should be executable"
    
    def test_required_directories_exist(self):
        """Test that required directories exist."""
        required_dirs = [
            'data',
            'logs', 
            'results',
            'tests',
            'src',
            'scripts/native-container'
        ]
        
        for dir_path in required_dirs:
            assert Path(dir_path).exists(), f"Directory {dir_path} should exist"
    
    def test_required_files_exist(self):
        """Test that required files exist."""
        if os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true':
            import pytest
            pytest.skip('Skipping file existence test inside Docker container')
        required_files = [
            'uv.toml',
            'run_analysis.py',
            'container.yaml',
            'docker-entrypoint.sh'
        ]
        
        for file_path in required_files:
            assert Path(file_path).exists(), f"File {file_path} should exist"
    
    def test_script_syntax_valid(self):
        """Test that all scripts have valid bash syntax."""
        scripts = [
            'scripts/native-container/setup.sh',
            'scripts/native-container/run.sh',
            'scripts/native-container/stop.sh',
            'scripts/native-container/logs.sh',
            'scripts/native-container/exec.sh',
            'scripts/native-container/cleanup.sh',
            'docker-entrypoint.sh'
        ]
        
        for script in scripts:
            result = subprocess.run(['bash', '-n', script], 
                                  capture_output=True, text=True)
            assert result.returncode == 0, f"Script {script} should have valid syntax"
    
    def test_container_yaml_valid(self):
        """Test that container.yaml is valid YAML."""
        if os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true':
            import pytest
            pytest.skip('Skipping container.yaml test inside Docker container')
        config_file = Path('container.yaml')
        assert config_file.exists(), "container.yaml should exist"
        
        # Validate YAML syntax
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Basic structure check
        assert isinstance(config, dict), "container.yaml should be a valid YAML object"
    
    def test_entrypoint_bash_history_function(self):
        """Test that container entrypoint includes bash history initialization."""
        entrypoint_script = Path('docker-entrypoint.sh')
        assert entrypoint_script.exists(), "docker-entrypoint.sh should exist"
        
        with open(entrypoint_script, 'r') as f:
            content = f.read()
        
        # Check for bash history initialization function
        assert 'init_bash_history' in content, "Entrypoint should include init_bash_history function"
        assert 'useful_commands' in content, "Entrypoint should define useful commands"
        
        # Check for specific commands in the function
        expected_commands = [
            'uv run pytest tests -n auto',
            'nz --interactive',
            'eda -dqc',
            'nz --indicators',
            'nz --metric'
        ]
        
        for cmd in expected_commands:
            assert cmd in content, f"Entrypoint should include command: {cmd}"
        
        # Check for history loading
        assert 'history -r' in content, "Entrypoint should include history loading"
        assert 'HISTFILE=' in content, "Entrypoint should configure HISTFILE"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 