"""
Common fixtures and configurations for plotting tests.
"""

import pytest
import os
import threading
import matplotlib
import matplotlib.pyplot as plt
from unittest.mock import patch

# Docker environment detection
def is_docker_environment():
    """Check if running in Docker environment"""
    return os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true'

# Global matplotlib lock for thread safety
matplotlib_lock = threading.Lock()

@pytest.fixture(scope="session", autouse=True)
def setup_matplotlib():
    """Setup matplotlib for thread safety in tests."""
    # Use non-interactive backend for Docker
    if is_docker_environment():
        matplotlib.use('Agg')
    
    # Set thread-safe mode
    plt.ioff()
    
    yield
    
    # Cleanup
    plt.close('all')

@pytest.fixture(autouse=True)
def thread_safe_plotting():
    """Ensure thread-safe plotting operations."""
    with matplotlib_lock:
        # Clear any existing plots
        plt.close('all')
        yield
        # Cleanup after test
        plt.close('all')

@pytest.fixture
def mock_matplotlib():
    """Mock matplotlib operations for testing."""
    with patch('matplotlib.pyplot.show') as mock_show, \
         patch('matplotlib.pyplot.savefig') as mock_save, \
         patch('os.makedirs'):
        yield {
            'show': mock_show,
            'savefig': mock_save
        }
