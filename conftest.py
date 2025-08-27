# -*- coding: utf-8 -*-
"""
Global pytest configuration for NeoZorK HLD Prediction project.

This file contains global pytest fixtures and configuration.
"""

import warnings
import pytest
import os
import matplotlib
import matplotlib.pyplot as plt

# Configure matplotlib for non-interactive backend in tests
matplotlib.use('Agg')
plt.ioff()

# Suppress all warnings globally
warnings.filterwarnings("ignore")

# Set environment variables for matplotlib
os.environ['MPLBACKEND'] = 'Agg'
os.environ['DISPLAY'] = ':99'

# Configure pytest to ignore all warnings
def pytest_configure(config):
    """Configure pytest to ignore all warnings."""
    config.addinivalue_line(
        "filterwarnings",
        "ignore::DeprecationWarning"
    )
    config.addinivalue_line(
        "filterwarnings",
        "ignore::PendingDeprecationWarning"
    )
    config.addinivalue_line(
        "filterwarnings",
        "ignore::UserWarning"
    )
    config.addinivalue_line(
        "filterwarnings",
        "ignore::FutureWarning"
    )
    config.addinivalue_line(
        "filterwarnings",
        "ignore::RuntimeWarning"
    )
    # InterpolationWarning is not available in builtins, so we'll handle it differently
    pass
    # PerformanceWarning and SettingWithCopyWarning are not available in builtins
    pass

def pytest_collection_modifyitems(config, items):
    """Modify test collection to suppress warnings."""
    for item in items:
        # Add marker to suppress warnings for all tests
        item.add_marker(pytest.mark.filterwarnings("ignore"))

@pytest.fixture(autouse=True)
def cleanup_matplotlib():
    """Clean up matplotlib after each test to prevent memory leaks."""
    yield
    try:
        plt.close('all')
        matplotlib.pyplot.close('all')
    except Exception:
        pass  # Ignore cleanup errors

@pytest.fixture(autouse=True)
def setup_matplotlib_backend():
    """Ensure matplotlib uses non-interactive backend for all tests."""
    import matplotlib
    matplotlib.use('Agg')
    plt.ioff()
    yield

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment for thread safety."""
    import os
    import tempfile
    
    # Create unique temp directory for each test
    temp_dir = tempfile.mkdtemp(prefix=f"test_{os.getpid()}_")
    os.environ['TMPDIR'] = temp_dir
    
    yield
    
    # Cleanup temp directory
    try:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception:
        pass
