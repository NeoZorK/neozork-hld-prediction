"""
Test for putcallratio indicator in seaborn mode.
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


class TestSeabornPutCallRatio:
    """Test cases for putcallratio indicator in seaborn mode."""

    def test_putcallratio_indicator_display(self):
        """Test that putcallratio indicator is displayed correctly."""
        # Create sample data
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2021, 1, 1)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        data = {
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.uniform(1000, 100000, len(dates)),
            'putcallratio': np.random.uniform(30, 70, len(dates)),
            'putcallratio_signal': np.random.uniform(30, 70, len(dates)),
            'putcallratio_histogram': np.random.uniform(-10, 10, len(dates)),
            'putcallratio_bullish': [60] * len(dates),
            'putcallratio_bearish': [40] * len(dates),
            'putcallratio_neutral': [50] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock plt.show to verify it's called
        with matplotlib_lock:
            with patch('matplotlib.pyplot.show') as mock_show, \
                 patch('matplotlib.pyplot.savefig'), \
                 patch('os.makedirs'):
                
                result = plot_dual_chart_seaborn(
                    df=df,
                    rule='putcallratio:20,close,60,40',
                    title='Test Put/Call Ratio Chart',
                    output_path='test_output.png'
                )
                
                # Verify plt.show was called
                mock_show.assert_called_once()
                
                # Verify result is returned
                assert result is not None
                assert hasattr(result, 'savefig')

    def test_putcallratio_without_signal_line(self):
        """Test putcallratio indicator without signal line."""
        # Create sample data
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2020, 6, 1)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        data = {
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.uniform(1000, 100000, len(dates)),
            'putcallratio': np.random.uniform(30, 70, len(dates)),
            'putcallratio_bullish': [60] * len(dates),
            'putcallratio_bearish': [40] * len(dates),
            'putcallratio_neutral': [50] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock plt.show to verify it's called
        with matplotlib_lock:
            with patch('matplotlib.pyplot.show') as mock_show, \
                 patch('matplotlib.pyplot.savefig'), \
                 patch('os.makedirs'):
                
                result = plot_dual_chart_seaborn(
                    df=df,
                    rule='putcallratio:20,close,60,40',
                    title='Test Put/Call Ratio Chart (No Signal)',
                    output_path='test_output.png'
                )
                
                # Verify plt.show was called
                mock_show.assert_called_once()
                
                # Verify result is returned
                assert result is not None
                assert hasattr(result, 'savefig')

    def test_putcallratio_with_histogram(self):
        """Test putcallratio indicator with histogram."""
        # Create sample data
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2020, 12, 31)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        data = {
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.uniform(1000, 100000, len(dates)),
            'putcallratio': np.random.uniform(30, 70, len(dates)),
            'putcallratio_signal': np.random.uniform(30, 70, len(dates)),
            'putcallratio_histogram': np.random.uniform(-10, 10, len(dates)),
            'putcallratio_bullish': [60] * len(dates),
            'putcallratio_bearish': [40] * len(dates),
            'putcallratio_neutral': [50] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock plt.show to verify it's called
        with matplotlib_lock:
            with patch('matplotlib.pyplot.show') as mock_show, \
                 patch('matplotlib.pyplot.savefig'), \
                 patch('os.makedirs'):
                
                result = plot_dual_chart_seaborn(
                    df=df,
                    rule='putcallratio:20,close,60,40',
                    title='Test Put/Call Ratio Chart (With Histogram)',
                    output_path='test_output.png'
                )
                
                # Verify plt.show was called
                mock_show.assert_called_once()
                
                # Verify result is returned
                assert result is not None
                assert hasattr(result, 'savefig')

    def test_putcallratio_threshold_levels(self):
        """Test putcallratio indicator with threshold levels."""
        # Create sample data
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2020, 12, 31)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        data = {
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.uniform(1000, 100000, len(dates)),
            'putcallratio': np.random.uniform(30, 70, len(dates)),
            'putcallratio_signal': np.random.uniform(30, 70, len(dates)),
            'putcallratio_bullish': [65] * len(dates),  # Custom bullish threshold
            'putcallratio_bearish': [35] * len(dates),  # Custom bearish threshold
            'putcallratio_neutral': [50] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock plt.show to verify it's called
        with matplotlib_lock:
            with patch('matplotlib.pyplot.show') as mock_show, \
                 patch('matplotlib.pyplot.savefig'), \
                 patch('os.makedirs'):
                
                result = plot_dual_chart_seaborn(
                    df=df,
                    rule='putcallratio:20,close,65,35',
                    title='Test Put/Call Ratio Chart (Custom Thresholds)',
                    output_path='test_output.png'
                )
                
                # Verify plt.show was called
                mock_show.assert_called_once()
                
                # Verify result is returned
                assert result is not None
                assert hasattr(result, 'savefig')

    def test_putcallratio_complete_indicator(self):
        """Test putcallratio indicator with all components."""
        # Create sample data
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2021, 1, 1)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        data = {
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.uniform(1000, 100000, len(dates)),
            'putcallratio': np.random.uniform(30, 70, len(dates)),
            'putcallratio_signal': np.random.uniform(30, 70, len(dates)),
            'putcallratio_histogram': np.random.uniform(-10, 10, len(dates)),
            'putcallratio_bullish': [60] * len(dates),
            'putcallratio_bearish': [40] * len(dates),
            'putcallratio_neutral': [50] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock plt.show to verify it's called
        with matplotlib_lock:
            with patch('matplotlib.pyplot.show') as mock_show, \
                 patch('matplotlib.pyplot.savefig'), \
                 patch('os.makedirs'):
                
                result = plot_dual_chart_seaborn(
                    df=df,
                    rule='putcallratio:20,close,60,40',
                    title='Test Put/Call Ratio Chart (Complete)',
                    output_path='test_output.png'
                )
                
                # Verify plt.show was called
                mock_show.assert_called_once()
                
                # Verify result is returned
                assert result is not None
                assert hasattr(result, 'savefig')


if __name__ == "__main__":
    pytest.main([__file__]) 