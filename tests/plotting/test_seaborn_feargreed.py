"""
Test for feargreed indicator in seaborn mode.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import matplotlib.pyplot as plt
import threading

from src.plotting.dual_chart_seaborn import plot_dual_chart_seaborn

# Thread lock for matplotlib operations
matplotlib_lock = threading.Lock()


class TestSeabornFearGreed:
    """Test cases for feargreed indicator in seaborn mode."""

    def test_feargreed_indicator_display(self):
        """Test that feargreed indicator is displayed correctly."""
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
            'feargreed': np.random.uniform(0, 100, len(dates)),
            'feargreed_signal': np.random.uniform(0, 100, len(dates)),
            'feargreed_histogram': np.random.uniform(-10, 10, len(dates)),
            'feargreed_fear': [25] * len(dates),
            'feargreed_greed': [75] * len(dates),
            'feargreed_neutral': [50] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock the plotting function with thread safety
        with matplotlib_lock:
            with patch('matplotlib.pyplot.show') as mock_show:
                with patch('matplotlib.pyplot.savefig') as mock_save:
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='feargreed:14,close',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    # Verify that the function completed successfully
                    assert result is not None
                    mock_save.assert_called_once()
                    mock_show.assert_called_once()

    def test_feargreed_without_signal_line(self):
        """Test feargreed indicator without signal line."""
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2021, 1, 1)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        data = {
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.randint(1000, 10000, len(dates)),
            'feargreed': np.random.uniform(0, 100, len(dates)),
            'feargreed_fear': [25] * len(dates),
            'feargreed_greed': [75] * len(dates),
            'feargreed_neutral': [50] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        with matplotlib_lock:
            with patch('matplotlib.pyplot.show') as mock_show:
                with patch('matplotlib.pyplot.savefig') as mock_save:
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='feargreed:14,close',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    assert result is not None
                    mock_save.assert_called_once()
                    mock_show.assert_called_once()

    def test_feargreed_with_histogram(self):
        """Test feargreed indicator with histogram."""
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2021, 1, 1)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        data = {
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.randint(1000, 10000, len(dates)),
            'feargreed': np.random.uniform(0, 100, len(dates)),
            'feargreed_signal': np.random.uniform(0, 100, len(dates)),
            'feargreed_histogram': np.random.uniform(-10, 10, len(dates)),
            'feargreed_fear': [25] * len(dates),
            'feargreed_greed': [75] * len(dates),
            'feargreed_neutral': [50] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        with matplotlib_lock:
            with patch('matplotlib.pyplot.show') as mock_show:
                with patch('matplotlib.pyplot.savefig') as mock_save:
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='feargreed:14,close',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    assert result is not None
                    mock_save.assert_called_once()
                    mock_show.assert_called_once()

    def test_feargreed_short_name(self):
        """Test feargreed indicator with short name 'fg'."""
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2021, 1, 1)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        data = {
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.randint(1000, 10000, len(dates)),
            'feargreed': np.random.uniform(0, 100, len(dates)),
            'feargreed_signal': np.random.uniform(0, 100, len(dates)),
            'feargreed_histogram': np.random.uniform(-10, 10, len(dates)),
            'feargreed_fear': [25] * len(dates),
            'feargreed_greed': [75] * len(dates),
            'feargreed_neutral': [50] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        with matplotlib_lock:
            with patch('matplotlib.pyplot.show') as mock_show:
                with patch('matplotlib.pyplot.savefig') as mock_save:
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='fg:14,close',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    assert result is not None
                    mock_save.assert_called_once()
                    mock_show.assert_called_once()

    def test_feargreed_minimal_data(self):
        """Test feargreed indicator with minimal required data."""
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2020, 2, 1)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        data = {
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.randint(1000, 10000, len(dates)),
            'feargreed': np.random.uniform(0, 100, len(dates))
        }
        
        df = pd.DataFrame(data, index=dates)
        
        with matplotlib_lock:
            with patch('matplotlib.pyplot.show') as mock_show:
                with patch('matplotlib.pyplot.savefig') as mock_save:
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='feargreed:14,close',
                        output_path='tests/plotting/test_output.png'
                    )
                    
                    assert result is not None
                    mock_save.assert_called_once()
                    mock_show.assert_called_once() 