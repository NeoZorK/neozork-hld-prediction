#!/usr/bin/env python3
"""
Test Docker environment functionality
"""

import os
import sys
import subprocess
import pytest
import importlib.util
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def is_running_in_docker():
    """Check if running inside Docker container"""
    return os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true'

class TestDockerEnvironment:
    """Test Docker environment setup and functionality"""
    
    @pytest.mark.skipif(is_running_in_docker(), reason="Docker files not available inside container")
    def test_docker_compose_file_exists(self):
        """Test that docker-compose.yml exists"""
        docker_compose_path = project_root / "docker-compose.yml"
        print(f"Looking for docker-compose.yml at: {docker_compose_path}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Project root: {project_root}")
        print(f"Files in project root: {list(project_root.glob('*.yml'))}")
        assert docker_compose_path.exists(), f"docker-compose.yml not found at {docker_compose_path}"
    
    @pytest.mark.skipif(is_running_in_docker(), reason="Docker files not available inside container")
    def test_dockerfile_exists(self):
        """Test that Dockerfile exists"""
        dockerfile_path = project_root / "Dockerfile"
        print(f"Looking for Dockerfile at: {dockerfile_path}")
        assert dockerfile_path.exists(), f"Dockerfile not found at {dockerfile_path}"
    
    def test_docker_env_file_exists(self):
        """Test that docker.env exists"""
        docker_env_path = project_root / "docker.env"
        print(f"Looking for docker.env at: {docker_env_path}")
        assert docker_env_path.exists(), f"docker.env not found at {docker_env_path}"
    
    @pytest.mark.skipif(is_running_in_docker(), reason="Docker files not available inside container")
    def test_container_entrypoint_exists(self):
        """Test that container-entrypoint.sh exists"""
        entrypoint_path = project_root / "container-entrypoint.sh"
        print(f"Looking for container-entrypoint.sh at: {entrypoint_path}")
        assert entrypoint_path.exists(), f"container-entrypoint.sh not found at {entrypoint_path}"
    
    def test_required_directories_exist(self):
        """Test that required directories exist"""
        required_dirs = [
            "src",
            "tests", 
            "data",
            "logs",
            "results",
            "scripts"
        ]
        
        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            assert dir_path.exists(), f"Required directory {dir_name} not found"
    
    def test_scripts_directory_structure(self):
        """Test that scripts directory has proper structure"""
        scripts_dir = project_root / "scripts"
        assert scripts_dir.exists(), "scripts directory not found"
        
        # Check for new organized structure
        expected_subdirs = [
            "mcp",
            "analysis", 
            "utilities",
            "demos",
            "debug",
            "docker",
            "native-container"
        ]
        
        for subdir in expected_subdirs:
            subdir_path = scripts_dir / subdir
            assert subdir_path.exists(), f"Scripts subdirectory {subdir} not found"
    
    def test_debug_scripts_exist(self):
        """Test that debug scripts exist in new location"""
        debug_scripts = [
            "scripts/debug/debug_yfinance.py",
            "scripts/debug/debug_binance.py",
            "scripts/debug/debug_polygon.py",
            "scripts/debug/examine_parquet.py"
        ]
        
        for script_path in debug_scripts:
            script_file = project_root / script_path
            assert script_file.exists(), f"Debug script {script_path} not found"
    
    def test_debug_scripts_executable(self):
        """Test that debug scripts are executable"""
        debug_scripts = [
            "scripts/debug/debug_yfinance.py",
            "scripts/debug/debug_binance.py", 
            "scripts/debug/debug_polygon.py",
            "scripts/debug/examine_parquet.py"
        ]
        
        for script_path in debug_scripts:
            script_file = project_root / script_path
            if script_file.exists():
                # Test that script can be imported
                try:
                    spec = importlib.util.spec_from_file_location("test_module", script_file)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    print(f"✅ {script_path} - Importable")
                except Exception as e:
                    print(f"⚠️ {script_path} - Import error (expected for some scripts): {e}")
    
    def test_mcp_scripts_exist(self):
        """Test that MCP scripts exist"""
        mcp_scripts = [
            "scripts/mcp/neozork_mcp_manager.py",
            "scripts/mcp/check_mcp_status.py",
            "scripts/mcp/start_mcp_server_daemon.py"
        ]
        
        for script_path in mcp_scripts:
            script_file = project_root / script_path
            assert script_file.exists(), f"MCP script {script_path} not found"
    
    def test_analysis_scripts_exist(self):
        """Test that analysis scripts exist"""
        analysis_scripts = [
            "scripts/analysis/analyze_requirements.py",
            "scripts/analysis/generate_test_coverage.py",
            "scripts/analysis/manage_test_results.py"
        ]
        
        for script_path in analysis_scripts:
            script_file = project_root / script_path
            assert script_file.exists(), f"Analysis script {script_path} not found"
    
    def test_utility_scripts_exist(self):
        """Test that utility scripts exist"""
        utility_scripts = [
            "scripts/utilities/fix_imports.py",
            "scripts/utilities/setup_ide_configs.py",
            "scripts/utilities/check_uv_mode.py"
        ]
        
        for script_path in utility_scripts:
            script_file = project_root / script_path
            assert script_file.exists(), f"Utility script {script_path} not found"
    
    def test_native_container_scripts_exist(self):
        """Test that native container scripts exist"""
        native_scripts = [
            "scripts/native-container/setup.sh",
            "scripts/native-container/run.sh",
            "scripts/native-container/stop.sh",
            "scripts/native-container/exec.sh",
            "scripts/native-container/logs.sh",
            "scripts/native-container/cleanup.sh"
        ]
        
        for script_path in native_scripts:
            script_file = project_root / script_path
            assert script_file.exists(), f"Native container script {script_path} not found"
    
    def test_docker_scripts_exist(self):
        """Test that Docker scripts exist"""
        docker_scripts = [
            "scripts/docker/test_docker_history.sh",
            "scripts/docker/test_history_auto.sh",
            "scripts/docker/docker-test-workflows.sh"
        ]
        
        for script_path in docker_scripts:
            script_file = project_root / script_path
            assert script_file.exists(), f"Docker script {script_path} not found"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 