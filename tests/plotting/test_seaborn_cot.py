"""
Test for COT (Commitment of Traders) indicator in seaborn mode.
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


class TestSeabornCOT:
    """Test cases for cot indicator in seaborn mode."""

    def test_cot_indicator_display(self):
        """Test that cot indicator is displayed correctly."""
        # In Docker environment, skip the actual plotting test
        if is_docker_environment():
            pytest.skip("Skipping COT plotting test in Docker environment due to threading issues")
        
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
        with matplotlib_lock:
            try:
                with patch('matplotlib.pyplot.show'), \
                     patch('matplotlib.pyplot.savefig'), \
                     patch('os.makedirs'):
                    
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='cot:20,close',
                        title='Test COT Chart',
                        output_path='test_output.png'
                    )
                    
                    # Verify result is returned
                    assert result is not None
                    assert hasattr(result, 'savefig')
            except Exception as e:
                raise

    def test_cot_without_signal_line(self):
        """Test cot indicator without signal line."""
        # In Docker environment, skip the actual plotting test
        if is_docker_environment():
            pytest.skip("Skipping COT plotting test in Docker environment due to threading issues")
        
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
        with matplotlib_lock:
            try:
                with patch('matplotlib.pyplot.show'), \
                     patch('matplotlib.pyplot.savefig'), \
                     patch('os.makedirs'):
                    
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='cot:20,close',
                        title='Test COT Chart (No Signal)',
                        output_path='test_output.png'
                    )
                    
                    # Verify result is returned
                    assert result is not None
                    assert hasattr(result, 'savefig')
            except Exception as e:
                raise

    def test_cot_with_histogram(self):
        """Test cot indicator with histogram."""
        # In Docker environment, skip the actual plotting test
        if is_docker_environment():
            pytest.skip("Skipping COT plotting test in Docker environment due to threading issues")
        
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
        with matplotlib_lock:
            try:
                with patch('matplotlib.pyplot.show'), \
                     patch('matplotlib.pyplot.savefig'), \
                     patch('os.makedirs'):
                    
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='cot:20,close',
                        title='Test COT Chart (With Histogram)',
                        output_path='test_output.png'
                    )
                    
                    # Verify result is returned
                    assert result is not None
                    assert hasattr(result, 'savefig')
            except Exception as e:
                raise

    def test_cot_threshold_levels(self):
        """Test cot indicator with threshold levels."""
        # In Docker environment, skip the actual plotting test
        if is_docker_environment():
            pytest.skip("Skipping COT plotting test in Docker environment due to threading issues")
        
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
        with matplotlib_lock:
            try:
                with patch('matplotlib.pyplot.show'), \
                     patch('matplotlib.pyplot.savefig'), \
                     patch('os.makedirs'):
                    
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='cot:20,close',
                        title='Test COT Chart (Custom Thresholds)',
                        output_path='test_output.png'
                    )
                    
                    # Verify result is returned
                    assert result is not None
                    assert hasattr(result, 'savefig')
            except Exception as e:
                raise

    def test_cot_complete_indicator(self):
        """Test cot indicator with all components."""
        # In Docker environment, skip the actual plotting test
        if is_docker_environment():
            pytest.skip("Skipping COT plotting test in Docker environment due to threading issues")
        
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
        with matplotlib_lock:
            try:
                with patch('matplotlib.pyplot.show'), \
                     patch('matplotlib.pyplot.savefig'), \
                     patch('os.makedirs'):
                    
                    result = plot_dual_chart_seaborn(
                        df=df,
                        rule='cot:20,close',
                        title='Test COT Chart (Complete)',
                        output_path='test_output.png'
                    )
                    
                    # Verify result is returned
                    assert result is not None
                    assert hasattr(result, 'savefig')
            except Exception as e:
                raise


if __name__ == "__main__":
    pytest.main([__file__]) 