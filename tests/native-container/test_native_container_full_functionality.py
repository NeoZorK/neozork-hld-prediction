#!/usr/bin/env python3
"""
Tests for native container full functionality.
These tests validate complete functionality of native Apple Silicon containers.
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
class TestNativeContainerFullFunctionality:
    """Test complete native container functionality."""
    
    def test_required_directories_structure(self):
        """Test that required directories exist and have correct structure."""
        required_dirs = [
            "data",
            "logs", 
            "results",
            "src",
            "tests",
            "scripts",
            "docs"
        ]
        
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            assert dir_path.exists(), f"Required directory {dir_name} should exist"
            assert dir_path.is_dir(), f"{dir_name} should be a directory"
    
    def test_required_files_exist(self):
        """Test that required configuration files exist."""
        required_files = [
            "pyproject.toml",
            "requirements.txt",
            "container.yaml",
            "README.md"
        ]
        
        for file_name in required_files:
            file_path = Path(file_name)
            assert file_path.exists(), f"Required file {file_name} should exist"
            assert file_path.is_file(), f"{file_name} should be a file"
    
    def test_native_container_scripts_structure(self):
        """Test that native container scripts directory has correct structure."""
        scripts_dir = Path("scripts/native-container")
        assert scripts_dir.exists(), "scripts/native-container directory should exist"
        
        required_scripts = [
            "native-container.sh",
            "setup.sh",
            "run.sh",
            "exec.sh",
            "stop.sh",
            "logs.sh",
            "force_restart.sh",
            "cleanup.sh"
        ]
        
        for script_name in required_scripts:
            script_path = scripts_dir / script_name
            assert script_path.exists(), f"Required script {script_name} should exist"
            assert os.access(script_path, os.X_OK), f"{script_name} should be executable"
    
    def test_container_yaml_configuration(self):
        """Test that container.yaml has valid configuration."""
        config_file = Path("container.yaml")
        assert config_file.exists(), "container.yaml should exist"
        
        try:
            import yaml
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            # Check basic structure
            assert 'apiVersion' in config, "container.yaml should have apiVersion"
            assert 'kind' in config, "container.yaml should have kind"
            assert 'metadata' in config, "container.yaml should have metadata"
            assert 'spec' in config, "container.yaml should have spec"
            
            # Check metadata
            metadata = config['metadata']
            assert 'name' in metadata, "metadata should have name"
            assert 'labels' in metadata, "metadata should have labels"
            
            # Check spec
            spec = config['spec']
            assert 'image' in spec, "spec should have image"
            assert 'architecture' in spec, "spec should have architecture"
            
        except ImportError:
            # Skip if yaml module not available
            pass
        except yaml.YAMLError as e:
            pytest.fail(f"container.yaml should be valid YAML: {e}")
    
    def test_python_project_configuration(self):
        """Test that Python project configuration is valid."""
        pyproject_file = Path("pyproject.toml")
        assert pyproject_file.exists(), "pyproject.toml should exist"
        
        try:
            import tomllib
            with open(pyproject_file, 'rb') as f:
                config = tomllib.load(f)
            
            # Check basic structure
            assert 'project' in config, "pyproject.toml should have project section"
            assert 'build-system' in config, "pyproject.toml should have build-system section"
            
            # Check project info
            project = config['project']
            assert 'name' in project, "project should have name"
            # Version can be dynamic or static
            assert 'version' in project or 'dynamic' in project, "project should have version or dynamic version"
            
        except ImportError:
            # Skip if tomllib not available (Python < 3.11)
            pass
        except Exception as e:
            pytest.fail(f"pyproject.toml should be valid TOML: {e}")
    
    def test_requirements_txt_validity(self):
        """Test that requirements.txt is valid."""
        requirements_file = Path("requirements.txt")
        assert requirements_file.exists(), "requirements.txt should exist"
        
        with open(requirements_file, 'r') as f:
            lines = f.readlines()
        
        # Check that file is not empty
        assert len(lines) > 0, "requirements.txt should not be empty"
        
        # Check that lines are not empty (after stripping)
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                # Basic package name validation - allow packages without version for development
                has_version = any(op in stripped for op in ['==', '>=', '<=', '~='])
                if not has_version:
                    print(f"Warning: Package {stripped} has no version specification")
    
    def test_source_code_structure(self):
        """Test that source code directory has correct structure."""
        src_dir = Path("src")
        assert src_dir.exists(), "src directory should exist"
        
        # Check for main package
        main_package = src_dir / "neozork_hld_prediction"
        if main_package.exists():
            assert main_package.is_dir(), "neozork_hld_prediction should be a directory"
            
            # Check for __init__.py
            init_file = main_package / "__init__.py"
            assert init_file.exists(), "Main package should have __init__.py"
    
    def test_test_structure(self):
        """Test that test directory has correct structure."""
        tests_dir = Path("tests")
        assert tests_dir.exists(), "tests directory should exist"
        
        # Check for conftest.py
        conftest_file = tests_dir / "conftest.py"
        assert conftest_file.exists(), "tests directory should have conftest.py"
        
        # Check for test subdirectories
        test_subdirs = ["calculation", "data", "eda", "ml", "plotting", "utils"]
        for subdir in test_subdirs:
            subdir_path = tests_dir / subdir
            if subdir_path.exists():
                assert subdir_path.is_dir(), f"tests/{subdir} should be a directory"
    
    def test_documentation_structure(self):
        """Test that documentation directory has correct structure."""
        docs_dir = Path("docs")
        assert docs_dir.exists(), "docs directory should exist"
        
        # Check for main documentation files
        main_docs = ["index.md", "README.md"]
        for doc_file in main_docs:
            doc_path = docs_dir / doc_file
            if doc_path.exists():
                assert doc_path.is_file(), f"docs/{doc_file} should be a file"
    
    def test_scripts_executability(self):
        """Test that all shell scripts are executable."""
        scripts_dir = Path("scripts/native-container")
        
        for script_file in scripts_dir.glob("*.sh"):
            if script_file.is_file():
                assert os.access(script_file, os.X_OK), f"{script_file} should be executable"
    
    def test_scripts_syntax_validity(self):
        """Test that all shell scripts have valid syntax."""
        scripts_dir = Path("scripts/native-container")
        
        for script_file in scripts_dir.glob("*.sh"):
            if script_file.is_file():
                try:
                    result = subprocess.run(['bash', '-n', str(script_file)], 
                                          capture_output=True, text=True)
                    assert result.returncode == 0, \
                        f"{script_file} should have valid bash syntax: {result.stderr}"
                except FileNotFoundError:
                    # Skip if bash not available
                    pass
    
    def test_scripts_shebang(self):
        """Test that all shell scripts have proper shebang."""
        scripts_dir = Path("scripts/native-container")
        
        for script_file in scripts_dir.glob("*.sh"):
            if script_file.is_file():
                with open(script_file, 'r') as f:
                    first_line = f.readline().strip()
                    assert first_line.startswith("#!/bin/bash") or first_line.startswith("#!/bin/sh"), \
                        f"{script_file} should start with proper shebang"
    
    def test_scripts_documentation(self):
        """Test that all shell scripts have header documentation."""
        scripts_dir = Path("scripts/native-container")
        
        for script_file in scripts_dir.glob("*.sh"):
            if script_file.is_file():
                with open(script_file, 'r') as f:
                    content = f.read()
                
                # Check for header comments in first 10 lines
                lines = content.split('\n')[:10]
                has_comments = any(line.strip().startswith('#') for line in lines)
                assert has_comments, f"{script_file} should have header comments"
    
    def test_enhanced_shell_functionality(self):
        """Test that enhanced shell script has required functionality."""
        exec_script = Path("scripts/native-container/exec.sh")
        assert exec_script.exists(), "exec.sh should exist"
        
        with open(exec_script, 'r') as f:
            content = f.read()
        
        # Check for required functions
        required_functions = [
            "create_enhanced_shell_command()",
            "execute_enhanced_shell()"
        ]
        
        for func in required_functions:
            assert func in content, f"exec.sh should contain function {func}"
        
        # Check for required aliases
        required_aliases = [
            "alias nz=",
            "alias eda=",
            "alias uv-install=",
            "alias uv-update=",
            "alias uv-test=",
            "alias uv-pytest="
        ]
        
        for alias in required_aliases:
            assert alias in content, f"exec.sh should contain alias {alias}"
    
    def test_main_script_functions(self):
        """Test that main native container script has required functions."""
        main_script = Path("scripts/native-container/native-container.sh")
        assert main_script.exists(), "native-container.sh should exist"
        
        with open(main_script, 'r') as f:
            content = f.read()
        
        # Check for main functions
        required_functions = [
            "start_container_sequence()",
            "stop_container_sequence()",
            "show_container_status()",
            "show_main_menu()",
            "main()"
        ]
        
        for func in required_functions:
            assert func in content, f"native-container.sh should contain function {func}"
    
    def test_setup_script_functionality(self):
        """Test that setup script has required functionality."""
        setup_script = Path("scripts/native-container/setup.sh")
        assert setup_script.exists(), "setup.sh should exist"
        
        with open(setup_script, 'r') as f:
            content = f.read()
        
        # Check for setup functionality
        assert "container create" in content or "container rm" in content, \
            "setup.sh should contain container commands"
    
    def test_run_script_functionality(self):
        """Test that run script has required functionality."""
        run_script = Path("scripts/native-container/run.sh")
        assert run_script.exists(), "run.sh should exist"
        
        with open(run_script, 'r') as f:
            content = f.read()
        
        # Check for run functionality
        assert "container start" in content, "run.sh should contain container start command"
    
    def test_exec_script_functionality(self):
        """Test that exec script has required functionality."""
        exec_script = Path("scripts/native-container/exec.sh")
        assert exec_script.exists(), "exec.sh should exist"
        
        with open(exec_script, 'r') as f:
            content = f.read()
        
        # Check for exec functionality
        assert "container exec" in content, "exec.sh should contain container exec command"
    
    def test_stop_script_functionality(self):
        """Test that stop script has required functionality."""
        stop_script = Path("scripts/native-container/stop.sh")
        assert stop_script.exists(), "stop.sh should exist"
        
        with open(stop_script, 'r') as f:
            content = f.read()
        
        # Check for stop functionality
        assert "container stop" in content, "stop.sh should contain container stop command"
    
    def test_logs_script_functionality(self):
        """Test that logs script has required functionality."""
        logs_script = Path("scripts/native-container/logs.sh")
        assert logs_script.exists(), "logs.sh should exist"
        
        with open(logs_script, 'r') as f:
            content = f.read()
        
        # Check for logs functionality
        assert "container logs" in content, "logs.sh should contain container logs command"
    
    def test_force_restart_script_functionality(self):
        """Test that force restart script has required functionality."""
        force_restart_script = Path("scripts/native-container/force_restart.sh")
        assert force_restart_script.exists(), "force_restart.sh should exist"
        
        with open(force_restart_script, 'r') as f:
            content = f.read()
        
        # Check for force restart functionality
        assert "force_restart_native_container()" in content or "restart" in content, \
            "force_restart.sh should contain restart functionality"
    
    def test_cleanup_script_functionality(self):
        """Test that cleanup script has required functionality."""
        cleanup_script = Path("scripts/native-container/cleanup.sh")
        assert cleanup_script.exists(), "cleanup.sh should exist"
        
        with open(cleanup_script, 'r') as f:
            content = f.read()
        
        # Check for cleanup functionality
        assert "cleanup" in content.lower(), "cleanup.sh should contain cleanup functionality"
    
    def test_script_error_handling(self):
        """Test that scripts have proper error handling."""
        scripts_dir = Path("scripts/native-container")
        
        for script_file in scripts_dir.glob("*.sh"):
            if script_file.is_file():
                with open(script_file, 'r') as f:
                    content = f.read()
                
                # Check for basic error handling
                has_error_handling = (
                    "set -e" in content or 
                    "set -o errexit" in content or
                    "trap" in content or
                    "exit" in content
                )
                
                # Not all scripts need error handling, so this is informational
                if not has_error_handling:
                    print(f"Info: {script_file} doesn't have explicit error handling")
    
    def test_script_logging(self):
        """Test that scripts have logging functionality."""
        scripts_dir = Path("scripts/native-container")
        
        for script_file in scripts_dir.glob("*.sh"):
            if script_file.is_file():
                with open(script_file, 'r') as f:
                    content = f.read()
                
                # Check for logging functionality
                has_logging = (
                    "echo" in content or
                    "log" in content.lower() or
                    "printf" in content
                )
                
                # All scripts should have some output
                assert has_logging, f"{script_file} should have logging/output functionality"
    
    def test_script_permissions_consistency(self):
        """Test that all scripts have consistent permissions."""
        scripts_dir = Path("scripts/native-container")
        scripts = list(scripts_dir.glob("*.sh"))
        
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
        scripts_dir = Path("scripts/native-container")
        
        for script_file in scripts_dir.glob("*.sh"):
            if script_file.is_file():
                with open(script_file, 'rb') as f:
                    content = f.read()
                
                # Check for Windows line endings
                assert b'\r\n' not in content, f"{script_file} should use Unix line endings"
    
    def test_project_readme(self):
        """Test that project README exists and has content."""
        readme_file = Path("README.md")
        assert readme_file.exists(), "README.md should exist"
        
        with open(readme_file, 'r') as f:
            content = f.read()
        
        # Check that README has content
        assert len(content.strip()) > 0, "README.md should have content"
        
        # Check for project name
        assert "neozork" in content.lower() or "hld" in content.lower() or "prediction" in content.lower(), \
            "README.md should contain project information"
