"""
Common fixtures and configurations for time_series tests.
"""

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
import matplotlib.pyplot as plt

@pytest.fixture(scope="session", autouse=True)
def setup_matplotlib():
    """Setup matplotlib for time_series tests."""
    # Backend already set to 'Agg' at module level
    # Set thread-safe mode
    plt.ioff()
    
    yield
    
    # Cleanup
    plt.close('all')
    
    # Restore recursion limit if changed
    if sys.version_info >= (3, 14) and original_recursion_limit is not None:
        sys.setrecursionlimit(original_recursion_limit)

