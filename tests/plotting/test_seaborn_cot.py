"""
Test for cot indicator in seaborn mode.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import matplotlib.pyplot as plt

from src.plotting.dual_chart_seaborn import plot_dual_chart_seaborn


class TestSeabornCOT:
    """Test cases for cot indicator in seaborn mode."""

    def test_cot_indicator_display(self):
        """Test that cot indicator is displayed correctly."""
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
            'cot': np.random.uniform(30, 70, len(dates)),
            'cot_signal': np.random.uniform(30, 70, len(dates)),
            'cot_histogram': np.random.uniform(-10, 10, len(dates)),
            'cot_bullish': [70] * len(dates),
            'cot_bearish': [30] * len(dates),
            'cot_neutral': [50] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock plt.show to verify it's called
        with patch('matplotlib.pyplot.show') as mock_show, \
             patch('matplotlib.pyplot.savefig'), \
             patch('os.makedirs'):
            
            result = plot_dual_chart_seaborn(
                df=df,
                rule='cot:20,close',
                title='Test COT Chart',
                output_path='test_output.png'
            )
            
            # Verify plt.show was called
            mock_show.assert_called_once()
            
            # Verify result is returned
            assert result is not None
            assert hasattr(result, 'savefig')

    def test_cot_without_signal_line(self):
        """Test cot indicator without signal line."""
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
            'cot': np.random.uniform(30, 70, len(dates)),
            'cot_bullish': [70] * len(dates),
            'cot_bearish': [30] * len(dates),
            'cot_neutral': [50] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock plt.show to verify it's called
        with patch('matplotlib.pyplot.show') as mock_show, \
             patch('matplotlib.pyplot.savefig'), \
             patch('os.makedirs'):
            
            result = plot_dual_chart_seaborn(
                df=df,
                rule='cot:20,close',
                title='Test COT Chart (No Signal)',
                output_path='test_output.png'
            )
            
            # Verify plt.show was called
            mock_show.assert_called_once()
            
            # Verify result is returned
            assert result is not None
            assert hasattr(result, 'savefig')

    def test_cot_with_histogram(self):
        """Test cot indicator with histogram."""
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
            'cot': np.random.uniform(30, 70, len(dates)),
            'cot_signal': np.random.uniform(30, 70, len(dates)),
            'cot_histogram': np.random.uniform(-10, 10, len(dates)),
            'cot_bullish': [70] * len(dates),
            'cot_bearish': [30] * len(dates),
            'cot_neutral': [50] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock plt.show to verify it's called
        with patch('matplotlib.pyplot.show') as mock_show, \
             patch('matplotlib.pyplot.savefig'), \
             patch('os.makedirs'):
            
            result = plot_dual_chart_seaborn(
                df=df,
                rule='cot:20,close',
                title='Test COT Chart (With Histogram)',
                output_path='test_output.png'
            )
            
            # Verify plt.show was called
            mock_show.assert_called_once()
            
            # Verify result is returned
            assert result is not None
            assert hasattr(result, 'savefig')

    def test_cot_threshold_levels(self):
        """Test cot indicator with threshold levels."""
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
            'cot': np.random.uniform(30, 70, len(dates)),
            'cot_signal': np.random.uniform(30, 70, len(dates)),
            'cot_bullish': [75] * len(dates),  # Custom bullish threshold
            'cot_bearish': [25] * len(dates),  # Custom bearish threshold
            'cot_neutral': [50] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock plt.show to verify it's called
        with patch('matplotlib.pyplot.show') as mock_show, \
             patch('matplotlib.pyplot.savefig'), \
             patch('os.makedirs'):
            
            result = plot_dual_chart_seaborn(
                df=df,
                rule='cot:20,close',
                title='Test COT Chart (Custom Thresholds)',
                output_path='test_output.png'
            )
            
            # Verify plt.show was called
            mock_show.assert_called_once()
            
            # Verify result is returned
            assert result is not None
            assert hasattr(result, 'savefig')

    def test_cot_complete_indicator(self):
        """Test cot indicator with all components."""
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
            'cot': np.random.uniform(30, 70, len(dates)),
            'cot_signal': np.random.uniform(30, 70, len(dates)),
            'cot_histogram': np.random.uniform(-10, 10, len(dates)),
            'cot_bullish': [70] * len(dates),
            'cot_bearish': [30] * len(dates),
            'cot_neutral': [50] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock plt.show to verify it's called
        with patch('matplotlib.pyplot.show') as mock_show, \
             patch('matplotlib.pyplot.savefig'), \
             patch('os.makedirs'):
            
            result = plot_dual_chart_seaborn(
                df=df,
                rule='cot:20,close',
                title='Test COT Chart (Complete)',
                output_path='test_output.png'
            )
            
            # Verify plt.show was called
            mock_show.assert_called_once()
            
            # Verify result is returned
            assert result is not None
            assert hasattr(result, 'savefig')


if __name__ == "__main__":
    pytest.main([__file__]) 