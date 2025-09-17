"""
Pytest configuration for CLI tests.

This module provides common fixtures and configuration for CLI testing.
"""

import pytest
import os
import sys
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables and configuration."""
    # Set environment variables for testing
    os.environ['MPLBACKEND'] = 'Agg'  # Non-interactive backend
    os.environ['NEOZORK_TEST'] = '1'  # Test mode flag
    os.environ['DISABLE_DOCKER_DETECTION'] = 'true'  # Disable Docker detection for consistent behavior
    os.environ['PYTHONUNBUFFERED'] = '1'  # Ensure output is not buffered
    
    # Set working directory to project root
    os.chdir(PROJECT_ROOT)
    
    yield
    
    # Cleanup if needed
    pass

@pytest.fixture(scope="function")
def test_timeout():
    """Provide appropriate timeout for tests based on environment."""
    # In Docker environment, use longer timeouts
    if os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true':
        return 120
    return 60

@pytest.fixture(scope="function")
def test_env():
    """Provide test environment variables."""
    return {
        'MPLBACKEND': 'Agg',
        'NEOZORK_TEST': '1',
        'DISABLE_DOCKER_DETECTION': 'true',
        'PYTHONUNBUFFERED': '1'
    }

@pytest.fixture(scope="session")
def project_root():
    """Provide project root path."""
    return PROJECT_ROOT

@pytest.fixture(scope="session")
def python_executable():
    """Provide Python executable path."""
    return sys.executable

@pytest.fixture(scope="session")
def script_path():
    """Provide path to run_analysis.py script."""
    return PROJECT_ROOT / 'run_analysis.py'