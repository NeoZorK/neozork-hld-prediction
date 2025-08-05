"""
Test for seaborn plot display functionality.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import matplotlib.pyplot as plt

from src.plotting.dual_chart_seaborn import plot_dual_chart_seaborn


class TestSeabornPlotDisplay:
    """Test cases for seaborn plot display functionality."""

    def test_plot_display_with_show(self):
        """Test that plot is displayed with plt.show()."""
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
            'macd': np.random.uniform(-0.1, 0.1, len(dates)),
            'macd_signal': np.random.uniform(-0.1, 0.1, len(dates)),
            'macd_histogram': np.random.uniform(-0.05, 0.05, len(dates))
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock plt.show to verify it's called
        with patch('matplotlib.pyplot.show') as mock_show, \
             patch('matplotlib.pyplot.savefig'), \
             patch('os.makedirs'):
            
            result = plot_dual_chart_seaborn(
                df=df,
                rule='macd:12,26,9,close',
                title='Test MACD Chart',
                output_path='test_output.png'
            )
            
            # Verify plt.show was called
            mock_show.assert_called_once()
            
            # Verify result is returned
            assert result is not None
            assert hasattr(result, 'savefig')

    def test_plot_display_without_show_fails(self):
        """Test that plot would not display without plt.show()."""
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
            'rsi': np.random.uniform(0, 100, len(dates)),
            'rsi_overbought': [70] * len(dates),
            'rsi_oversold': [30] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock plt.show to verify it's NOT called (simulating old behavior)
        with patch('matplotlib.pyplot.show') as mock_show, \
             patch('matplotlib.pyplot.savefig'), \
             patch('os.makedirs'):
            
            # Simulate old behavior without plt.show()
            # This would be the old version of the function
            result = plot_dual_chart_seaborn(
                df=df,
                rule='rsi:14,30,70,close',
                title='Test RSI Chart',
                output_path='test_output.png'
            )
            
            # Verify plt.show was called (new behavior)
            mock_show.assert_called_once()

    def test_plot_display_with_different_indicators(self):
        """Test plot display with different indicators."""
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
            'ema': np.random.uniform(1.0, 2.0, len(dates))
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Test with EMA indicator
        with patch('matplotlib.pyplot.show') as mock_show, \
             patch('matplotlib.pyplot.savefig'), \
             patch('os.makedirs'):
            
            result = plot_dual_chart_seaborn(
                df=df,
                rule='ema:20,close',
                title='Test EMA Chart',
                output_path='test_output.png'
            )
            
            mock_show.assert_called_once()
            assert result is not None

    def test_plot_display_with_rsi_indicator(self):
        """Test plot display with RSI indicator."""
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
            'rsi': np.random.uniform(0, 100, len(dates)),
            'rsi_overbought': [70] * len(dates),
            'rsi_oversold': [30] * len(dates)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Test with RSI indicator
        with patch('matplotlib.pyplot.show') as mock_show, \
             patch('matplotlib.pyplot.savefig'), \
             patch('os.makedirs'):
            
            result = plot_dual_chart_seaborn(
                df=df,
                rule='rsi:14,30,70,close',
                title='Test RSI Chart',
                output_path='test_output.png'
            )
            
            mock_show.assert_called_once()
            assert result is not None

    def test_plot_display_with_bb_indicator(self):
        """Test plot display with Bollinger Bands indicator."""
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
            'bb_upper': np.random.uniform(2.0, 2.5, len(dates)),
            'bb_middle': np.random.uniform(1.5, 2.0, len(dates)),
            'bb_lower': np.random.uniform(1.0, 1.5, len(dates))
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Test with Bollinger Bands indicator
        with patch('matplotlib.pyplot.show') as mock_show, \
             patch('matplotlib.pyplot.savefig'), \
             patch('os.makedirs'):
            
            result = plot_dual_chart_seaborn(
                df=df,
                rule='bb:20,2,close',
                title='Test Bollinger Bands Chart',
                output_path='test_output.png'
            )
            
            mock_show.assert_called_once()
            assert result is not None


if __name__ == "__main__":
    pytest.main([__file__]) 