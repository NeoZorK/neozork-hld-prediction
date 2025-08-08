#!/usr/bin/env python3
"""
Pytest configuration and fixtures for NeoZork HLD Prediction project
"""

import pytest
import os
import sys
import tempfile
import shutil
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt

# Configure matplotlib for non-interactive backend in tests
matplotlib.use('Agg')

# Set environment variables for safe testing
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib-cache'

# Container detection
def is_container():
    """Detect if running in container environment"""
    return (
        os.path.exists('/.dockerenv') or 
        os.environ.get('NATIVE_CONTAINER') == 'true' or
        os.environ.get('DOCKER_CONTAINER') == 'true'
    )

@pytest.fixture(scope="session")
def test_data_dir():
    """Provide test data directory"""
    return Path(__file__).parent.parent / "data"

@pytest.fixture(scope="session")
def logs_dir():
    """Provide logs directory"""
    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    return logs_dir

@pytest.fixture(scope="session")
def temp_dir():
    """Provide temporary directory for tests"""
    temp_dir = Path(tempfile.mkdtemp(prefix="neozork_tests_"))
    yield temp_dir
    # Cleanup
    try:
        shutil.rmtree(temp_dir)
    except:
        pass

@pytest.fixture(autouse=True)
def setup_matplotlib():
    """Setup matplotlib for safe testing"""
    # Use non-interactive backend
    plt.switch_backend('Agg')
    
    # Create temporary directory for matplotlib cache
    cache_dir = Path('/tmp/matplotlib-cache')
    cache_dir.mkdir(exist_ok=True)
    
    # Set matplotlib configuration
    matplotlib.rcParams['figure.max_open_warning'] = 0
    matplotlib.rcParams['figure.dpi'] = 72
    
    yield
    
    # Cleanup matplotlib figures
    plt.close('all')

@pytest.fixture(autouse=True)
def setup_container_environment():
    """Setup environment for container testing"""
    if is_container():
        # Set thread limits for container
        os.environ['OMP_NUM_THREADS'] = '1'
        os.environ['MKL_NUM_THREADS'] = '1'
        os.environ['OPENBLAS_NUM_THREADS'] = '1'
        
        # Set memory limits
        os.environ['PYTHONMALLOC'] = 'malloc'
        
        # Create necessary directories
        dirs_to_create = [
            '/tmp/matplotlib-cache',
            '/tmp/pytest-cache',
            '/tmp/bash_history',
            '/tmp/bin',
            '/tmp/bash_config'
        ]
        
        for dir_path in dirs_to_create:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

@pytest.fixture
def sample_dataframe():
    """Provide sample DataFrame for testing"""
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    # Create sample data
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2021, 1, 1)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    data = {
        'Open': np.random.uniform(1.0, 2.0, len(dates)),
        'High': np.random.uniform(1.0, 2.0, len(dates)),
        'Low': np.random.uniform(1.0, 2.0, len(dates)),
        'Close': np.random.uniform(1.0, 2.0, len(dates)),
        'Volume': np.random.randint(1000, 10000, len(dates))
    }
    
    return pd.DataFrame(data, index=dates)

@pytest.fixture
def sample_dataframe_with_indicators():
    """Provide sample DataFrame with indicator columns"""
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    # Create sample data
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2021, 1, 1)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    data = {
        'Open': np.random.uniform(1.0, 2.0, len(dates)),
        'High': np.random.uniform(1.0, 2.0, len(dates)),
        'Low': np.random.uniform(1.0, 2.0, len(dates)),
        'Close': np.random.uniform(1.0, 2.0, len(dates)),
        'Volume': np.random.randint(1000, 10000, len(dates)),
        'RSI': np.random.uniform(0, 100, len(dates)),
        'EMA': np.random.uniform(1.0, 2.0, len(dates)),
        'BB_Upper': np.random.uniform(1.5, 2.5, len(dates)),
        'BB_Lower': np.random.uniform(0.5, 1.5, len(dates)),
        'Direction': np.random.choice([0, 1, 2], len(dates))
    }
    
    return pd.DataFrame(data, index=dates)

@pytest.fixture
def mock_plotting_functions(monkeypatch):
    """Mock plotting functions to prevent display issues"""
    
    def mock_show(*args, **kwargs):
        pass
    
    def mock_savefig(*args, **kwargs):
        pass
    
    # Don't mock figure to avoid recursion
    # def mock_figure(*args, **kwargs):
    #     return plt.figure()
    
    # Apply mocks
    monkeypatch.setattr(plt, 'show', mock_show)
    monkeypatch.setattr(plt, 'savefig', mock_savefig)
    # monkeypatch.setattr(plt, 'figure', mock_figure)

@pytest.fixture
def safe_test_environment():
    """Provide safe test environment for container"""
    
    # Store original environment
    original_env = os.environ.copy()
    
    # Set safe environment variables
    os.environ.update({
        'PYTHONUNBUFFERED': '1',
        'PYTHONDONTWRITEBYTECODE': '1',
        'MPLCONFIGDIR': '/tmp/matplotlib-cache',
        'OMP_NUM_THREADS': '1',
        'MKL_NUM_THREADS': '1',
        'OPENBLAS_NUM_THREADS': '1'
    })
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)

# Add missing function for native-container tests
def skip_if_docker(func):
    """Decorator to skip tests when running in Docker environment"""
    def wrapper(*args, **kwargs):
        if os.environ.get('DOCKER_CONTAINER') == 'true':
            pytest.skip("Test skipped in Docker environment")
        return func(*args, **kwargs)
    return wrapper

# Markers for test categorization
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "basic: marks tests as basic functionality tests"
    )
    config.addinivalue_line(
        "markers", "flag_combinations: marks tests as flag combination tests"
    )
    config.addinivalue_line(
        "markers", "error: marks tests as error case tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running tests"
    )
    config.addinivalue_line(
        "markers", "container_safe: marks tests as safe for container execution"
    )

# Skip certain tests in container
def pytest_collection_modifyitems(config, items):
    """Modify test collection for container environment"""
    if is_container():
        skip_container_unsafe = pytest.mark.skip(reason="Not safe for container execution")
        for item in items:
            # Skip slow and performance tests in container
            if any(marker.name in ['slow', 'performance'] for marker in item.iter_markers()):
                item.add_marker(skip_container_unsafe) 