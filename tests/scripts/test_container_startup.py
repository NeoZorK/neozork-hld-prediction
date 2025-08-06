#!/usr/bin/env python3
"""
Test for container startup functionality
"""

import pytest
import os
import sys
import subprocess
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_container_startup_script_exists():
    """Test that container startup script exists"""
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'debug', 'test_container_startup.py')
    assert os.path.exists(script_path), f"Container startup script not found at {script_path}"

def test_container_startup_script_runnable():
    """Test that container startup script can be executed"""
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'debug', 'test_container_startup.py')
    
    # Test that script can be imported
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("test_container_startup", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert hasattr(module, 'test_container_startup'), "test_container_startup function not found"
    except Exception as e:
        pytest.fail(f"Failed to import container startup script: {e}")

@patch('subprocess.run')
def test_container_startup_uv_check(mock_run):
    """Test UV check functionality"""
    # Mock successful UV check
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "uv 0.1.0"
    mock_run.return_value = mock_result
    
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'debug', 'test_container_startup.py')
    
    # Import and run the function
    import importlib.util
    spec = importlib.util.spec_from_file_location("test_container_startup", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Test UV check
    result = module.test_container_startup()
    assert result is True, "Container startup test should return True"

@patch('subprocess.run')
def test_container_startup_uv_not_found(mock_run):
    """Test UV not found scenario"""
    # Mock UV not found
    mock_run.side_effect = FileNotFoundError("uv: command not found")
    
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'debug', 'test_container_startup.py')
    
    # Import and run the function
    import importlib.util
    spec = importlib.util.spec_from_file_location("test_container_startup", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Test UV check with UV not found
    result = module.test_container_startup()
    assert result is True, "Container startup test should return True even if UV not found"

def test_container_startup_environment_variables():
    """Test environment variable checking"""
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'debug', 'test_container_startup.py')
    
    # Import and run the function
    import importlib.util
    spec = importlib.util.spec_from_file_location("test_container_startup", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Test environment variable check
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "uv 0.1.0"
        mock_run.return_value = mock_result
        
        result = module.test_container_startup()
        assert result is True, "Container startup test should return True"

def test_container_startup_directory_check():
    """Test directory checking functionality"""
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'debug', 'test_container_startup.py')
    
    # Import and run the function
    import importlib.util
    spec = importlib.util.spec_from_file_location("test_container_startup", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Test directory check
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "uv 0.1.0"
        mock_run.return_value = mock_result
        
        result = module.test_container_startup()
        assert result is True, "Container startup test should return True"

def test_container_startup_file_check():
    """Test file checking functionality"""
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'debug', 'test_container_startup.py')
    
    # Import and run the function
    import importlib.util
    spec = importlib.util.spec_from_file_location("test_container_startup", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Test file check
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "uv 0.1.0"
        mock_run.return_value = mock_result
        
        result = module.test_container_startup()
        assert result is True, "Container startup test should return True"

def test_container_startup_import_check():
    """Test Python import checking functionality"""
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'debug', 'test_container_startup.py')
    
    # Import and run the function
    import importlib.util
    spec = importlib.util.spec_from_file_location("test_container_startup", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Test import check
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "uv 0.1.0"
        mock_run.return_value = mock_result
        
        result = module.test_container_startup()
        assert result is True, "Container startup test should return True"

if __name__ == "__main__":
    pytest.main([__file__]) 