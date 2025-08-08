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

# Thread lock for matplotlib operations
matplotlib_lock = threading.Lock()

# Container detection
def is_container():
    """Detect if running in container environment"""
    return (
        os.path.exists('/.dockerenv') or 
        os.environ.get('NATIVE_CONTAINER') == 'true' or
        os.environ.get('DOCKER_CONTAINER') == 'true'
    )

class TestSeabornSuperTrend:
    """Test cases for supertrend indicator in seaborn mode."""

    @pytest.mark.container_safe
    def test_supertrend_indicator_display(self, mock_plotting_functions):
        """Test that supertrend indicator is displayed correctly."""
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
            with patch('matplotlib.pyplot.show') as mock_show:
                with patch('matplotlib.pyplot.savefig') as mock_save:
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='supertrend:10,3',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    # Verify that the function completed successfully
                    assert result is not None
                    mock_save.assert_called_once()
                    mock_show.assert_called_once()

    @pytest.mark.container_safe
    def test_supertrend_with_nan_values(self, mock_plotting_functions):
        """Test supertrend indicator with NaN values."""
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
            with patch('matplotlib.pyplot.show') as mock_show:
                with patch('matplotlib.pyplot.savefig') as mock_save:
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='supertrend:10,3',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    assert result is not None
                    mock_save.assert_called_once()
                    mock_show.assert_called_once()

    @pytest.mark.container_safe
    def test_supertrend_with_mixed_values(self, mock_plotting_functions):
        """Test supertrend indicator with mixed valid and NaN values."""
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2021, 1, 1)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        data = {
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.randint(1000, 10000, len(dates)),
            'PPrice1': [np.nan if i % 3 == 0 else np.random.uniform(1.0, 2.0) for i in range(len(dates))],
            'PPrice2': [np.nan if i % 4 == 0 else np.random.uniform(1.0, 2.0) for i in range(len(dates))],
            'Direction': np.random.choice([0, 1, 2], len(dates))
        }
        
        df = pd.DataFrame(data, index=dates)
        
        with matplotlib_lock:
            with patch('matplotlib.pyplot.show') as mock_show:
                with patch('matplotlib.pyplot.savefig') as mock_save:
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='supertrend:10,3',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    assert result is not None
                    mock_save.assert_called_once()
                    mock_show.assert_called_once()

    @pytest.mark.container_safe
    def test_supertrend_without_required_columns(self, mock_plotting_functions):
        """Test supertrend indicator without required columns."""
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
            with patch('matplotlib.pyplot.show') as mock_show:
                with patch('matplotlib.pyplot.savefig') as mock_save:
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='supertrend:10,3',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    assert result is not None
                    mock_save.assert_called_once()
                    mock_show.assert_called_once()

    @pytest.mark.container_safe
    def test_supertrend_minimal_data(self, mock_plotting_functions):
        """Test supertrend indicator with minimal data."""
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2020, 1, 10)  # Only 10 days
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
            with patch('matplotlib.pyplot.show') as mock_show:
                with patch('matplotlib.pyplot.savefig') as mock_save:
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='supertrend:10,3',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    assert result is not None
                    mock_save.assert_called_once()
                    mock_show.assert_called_once() 