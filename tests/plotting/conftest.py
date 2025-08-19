"""
Common fixtures and configurations for plotting tests.
"""

import pytest
import os
import threading
import matplotlib
import matplotlib.pyplot as plt
from unittest.mock import patch
import signal
import time

# Docker environment detection
def is_docker_environment():
    """Check if running in Docker environment"""
    return os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true'

# Multithreading issues detection
def should_skip_plotting_tests():
    """Check if plotting tests should be skipped due to threading issues"""
    # Skip in Docker environment
    if is_docker_environment():
        return True
    
    # Skip if running with high worker count (more than 4 workers)
    worker_count = os.environ.get('PYTEST_XDIST_WORKER_COUNT', '1')
    try:
        if int(worker_count) > 4:
            return True
    except ValueError:
        pass
    
    return False

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

@pytest.fixture(scope="session")
def timeout_handler():
    """Handle timeouts in tests."""
    def timeout_handler(signum, frame):
        raise TimeoutError("Test timed out")
    
    # Set up signal handler for timeout
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    yield
    # Restore original handler
    signal.signal(signal.SIGALRM, old_handler)
