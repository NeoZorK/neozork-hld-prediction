"""
Test for supertrend indicator in seaborn mode.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import matplotlib.pyplot as plt
import threading
import os

from src.plotting.dual_chart_seaborn import plot_dual_chart_seaborn

# Import from conftest with fallback
try:
    from .conftest import matplotlib_lock, is_docker_environment
except ImportError:
    # Fallback if conftest is not available
    matplotlib_lock = threading.Lock()
    
    def is_docker_environment():
        """Check if running in Docker environment"""
        return os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true'


class TestSeabornSuperTrend:
    """Test cases for supertrend indicator in seaborn mode."""

    def test_supertrend_indicator_display(self):
        """Test that supertrend indicator is displayed correctly."""
        # In Docker environment, skip the actual plotting test
        if is_docker_environment():
            pytest.skip("Skipping SuperTrend plotting test in Docker environment due to threading issues")
        
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
            'PPrice1': np.random.uniform(1.0, 2.0, len(dates)),
            'PPrice2': np.random.uniform(1.0, 2.0, len(dates)),
            'Direction': np.random.choice([0, 1, 2], len(dates))
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock the plotting function
        with matplotlib_lock:
            try:
                with patch('matplotlib.pyplot.show'), \
                     patch('matplotlib.pyplot.savefig'), \
                     patch('os.makedirs'):
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='supertrend:10,3',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    # Verify that the function completed successfully
                    assert result is not None
            except Exception as e:
                raise

    def test_supertrend_with_nan_values(self):
        """Test supertrend indicator with NaN values."""
        # In Docker environment, skip the actual plotting test
        if is_docker_environment():
            pytest.skip("Skipping SuperTrend plotting test in Docker environment due to threading issues")
        
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2021, 1, 1)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        data = {
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.randint(1000, 10000, len(dates)),
            'PPrice1': [np.nan] * len(dates),
            'PPrice2': [np.nan] * len(dates),
            'Direction': [0] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        with matplotlib_lock:
            try:
                with patch('matplotlib.pyplot.show'), \
                     patch('matplotlib.pyplot.savefig'), \
                     patch('os.makedirs'):
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='supertrend:10,3',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    assert result is not None
            except Exception as e:
                raise

    def test_supertrend_with_mixed_values(self):
        """Test supertrend indicator with mixed valid and NaN values."""
        # In Docker environment, skip the actual plotting test
        if is_docker_environment():
            pytest.skip("Skipping SuperTrend plotting test in Docker environment due to threading issues")
        
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2021, 1, 1)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        data = {
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.randint(1000, 10000, len(dates)),
            'PPrice1': [1.5 if i % 2 == 0 else np.nan for i in range(len(dates))],
            'PPrice2': [1.6 if i % 2 == 0 else np.nan for i in range(len(dates))],
            'Direction': [1 if i % 2 == 0 else 0 for i in range(len(dates))]
        }
        
        df = pd.DataFrame(data, index=dates)
        
        with matplotlib_lock:
            try:
                with patch('matplotlib.pyplot.show'), \
                     patch('matplotlib.pyplot.savefig'), \
                     patch('os.makedirs'):
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='supertrend:10,3',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    assert result is not None
            except Exception as e:
                raise

    def test_supertrend_without_required_columns(self):
        """Test supertrend indicator without required columns."""
        # In Docker environment, skip the actual plotting test
        if is_docker_environment():
            pytest.skip("Skipping SuperTrend plotting test in Docker environment due to threading issues")
        
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
        
        df = pd.DataFrame(data, index=dates)
        
        with matplotlib_lock:
            try:
                with patch('matplotlib.pyplot.show'), \
                     patch('matplotlib.pyplot.savefig'), \
                     patch('os.makedirs'):
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='supertrend:10,3',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    assert result is not None
            except Exception as e:
                raise

    def test_supertrend_minimal_data(self):
        """Test supertrend indicator with minimal required data."""
        # In Docker environment, skip the actual plotting test
        if is_docker_environment():
            pytest.skip("Skipping SuperTrend plotting test in Docker environment due to threading issues")
        
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2020, 2, 1)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        data = {
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.randint(1000, 10000, len(dates)),
            'PPrice1': np.random.uniform(1.0, 2.0, len(dates)),
            'PPrice2': np.random.uniform(1.0, 2.0, len(dates)),
            'Direction': np.random.choice([0, 1, 2], len(dates))
        }
        
        df = pd.DataFrame(data, index=dates)
        
        with matplotlib_lock:
            try:
                with patch('matplotlib.pyplot.show'), \
                     patch('matplotlib.pyplot.savefig'), \
                     patch('os.makedirs'):
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='supertrend:10,3',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    assert result is not None
            except Exception as e:
                raise 