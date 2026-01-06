"""
Common fixtures and configurations for plotting tests.
"""

<<<<<<< HEAD
import pytest
import os
import threading
import matplotlib
=======
import sys
import copy

# CRITICAL: Set matplotlib backend BEFORE any matplotlib imports
# This must be done before importing matplotlib to avoid GUI issues
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

# CRITICAL: Increase recursion limit for Python 3.14.2 compatibility
# matplotlib deepcopy operations can exceed default limit
original_recursion_limit = None
if sys.version_info >= (3, 14):
    original_recursion_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(5000, original_recursion_limit * 2))

# CRITICAL: Patch matplotlib.path.Path.__deepcopy__ to avoid RecursionError
# Python 3.14.2 has issues with deepcopy(super(), memo) in matplotlib.path.Path
def _patched_path_deepcopy(self, memo):
    """Patched __deepcopy__ for matplotlib.path.Path to avoid recursion."""
    import matplotlib.path as mpath
    # Create a new Path without calling super().__deepcopy__ which causes recursion
    new_path = mpath.Path.__new__(mpath.Path)
    new_path._vertices = copy.deepcopy(self._vertices, memo)
    new_path._codes = copy.deepcopy(self._codes, memo)
    new_path._interpolation_steps = copy.deepcopy(self._interpolation_steps, memo)
    new_path._should_simplify = copy.deepcopy(self._should_simplify, memo)
    new_path._simplify_threshold = copy.deepcopy(self._simplify_threshold, memo)
    return new_path

# Apply the patch before any matplotlib.path imports
import matplotlib.path
if hasattr(matplotlib.path.Path, '__deepcopy__'):
    matplotlib.path.Path.__deepcopy__ = _patched_path_deepcopy

import pytest
import os
import threading
>>>>>>> origin/master
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
<<<<<<< HEAD
    # Use non-interactive backend for Docker
    if is_docker_environment():
        matplotlib.use('Agg')
    
=======
    # Backend already set to 'Agg' at module level
>>>>>>> origin/master
    # Set thread-safe mode
    plt.ioff()
    
    yield
    
    # Cleanup
    plt.close('all')
<<<<<<< HEAD
=======
    
    # Restore recursion limit if changed
    if sys.version_info >= (3, 14) and 'original_recursion_limit' in globals():
        sys.setrecursionlimit(original_recursion_limit)
>>>>>>> origin/master

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
