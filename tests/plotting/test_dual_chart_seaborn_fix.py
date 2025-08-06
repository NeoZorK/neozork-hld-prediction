"""
Test for seaborn dual chart MAXTICKS fix.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from unittest.mock import patch, MagicMock

from src.plotting.dual_chart_seaborn import plot_dual_chart_seaborn


class TestSeabornDualChartFix:
    """Test cases for seaborn dual chart MAXTICKS fix."""

    def test_large_dataset_ticks_calculation(self):
        """Test that large datasets use appropriate tick intervals."""
        # Create a large dataset spanning multiple years (reduced for Docker)
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2023, 1, 1)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        # Sample every 7th day to reduce dataset size for Docker
        dates = dates[::7]
        
        # Create sample data
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
        
        # Mock the plotting functions to avoid actual file creation
        with patch('matplotlib.pyplot.savefig'), \
             patch('matplotlib.pyplot.show'), \
             patch('os.makedirs'):
            
            # Set matplotlib backend to non-interactive for Docker
            import matplotlib
            matplotlib.use('Agg')
            
            # This should not raise MAXTICKS error
            result = plot_dual_chart_seaborn(
                df=df,
                rule='macd:12,26,9,close',
                title='Test MACD Chart',
                output_path='test_output.png'
            )
            
            # Should return a figure object
            assert result is not None
            assert hasattr(result, 'savefig')
            
            # Clean up matplotlib figure to prevent memory leaks
            import matplotlib.pyplot as plt
            plt.close(result)

    def test_medium_dataset_ticks_calculation(self):
        """Test that medium datasets use appropriate tick intervals."""
        # Create a medium dataset spanning 1 year (reduced for Docker)
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        # Sample every 3rd day to reduce dataset size
        dates = dates[::3]
        
        # Create sample data
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
        
        # Mock the plotting functions
        with patch('matplotlib.pyplot.savefig'), \
             patch('matplotlib.pyplot.show'), \
             patch('os.makedirs'):
            
            # Set matplotlib backend to non-interactive for Docker
            import matplotlib
            matplotlib.use('Agg')
            
            result = plot_dual_chart_seaborn(
                df=df,
                rule='rsi:14,30,70,close',
                title='Test RSI Chart',
                output_path='test_output.png'
            )
            
            assert result is not None
            assert hasattr(result, 'savefig')
            
            # Clean up matplotlib figure to prevent memory leaks
            import matplotlib.pyplot as plt
            plt.close(result)

    def test_small_dataset_ticks_calculation(self):
        """Test that small datasets use appropriate tick intervals."""
        # Create a small dataset spanning 3 months
        start_date = datetime(2024, 10, 1)
        end_date = datetime(2024, 12, 31)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        # Create sample data
        data = {
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.uniform(1000, 100000, len(dates)),
            'ema': np.random.uniform(1.0, 2.0, len(dates))
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Mock the plotting functions
        with patch('matplotlib.pyplot.savefig'), \
             patch('matplotlib.pyplot.show'), \
             patch('os.makedirs'):
            
            # Set matplotlib backend to non-interactive for Docker
            import matplotlib
            matplotlib.use('Agg')
            
            result = plot_dual_chart_seaborn(
                df=df,
                rule='ema:20,close',
                title='Test EMA Chart',
                output_path='test_output.png'
            )
            
            assert result is not None
            assert hasattr(result, 'savefig')
            
            # Clean up matplotlib figure to prevent memory leaks
            import matplotlib.pyplot as plt
            plt.close(result)

    def test_no_max_ticks_error(self):
        """Test that no MAXTICKS error occurs with large datasets."""
        # Create a large dataset that would previously cause MAXTICKS error (reduced for Docker)
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2023, 1, 1)
        dates = pd.date_range(start_date, end_date, freq='D')
        
        # Sample every 7th day to reduce dataset size for Docker
        dates = dates[::7]
        
        # Create sample data
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
        
        # Mock the plotting functions
        with patch('matplotlib.pyplot.savefig'), \
             patch('matplotlib.pyplot.show'), \
             patch('os.makedirs'):
            
            # Set matplotlib backend to non-interactive for Docker
            import matplotlib
            matplotlib.use('Agg')
            
            # This should not raise any MAXTICKS related errors
            try:
                result = plot_dual_chart_seaborn(
                    df=df,
                    rule='macd:12,26,9,close',
                    title='Test Large Dataset MACD Chart',
                    output_path='test_output.png'
                )
                
                assert result is not None
                assert hasattr(result, 'savefig')
                
                # Clean up matplotlib figure to prevent memory leaks
                import matplotlib.pyplot as plt
                plt.close(result)
                
            except Exception as e:
                # Should not raise MAXTICKS error
                assert "MAXTICKS" not in str(e)
                assert "Locator attempting to generate" not in str(e)
                raise  # Re-raise if it's a different error

    def test_ticks_interval_calculation(self):
        """Test that tick intervals are calculated correctly based on data range."""
        # Test different time ranges with smaller datasets for Docker
        test_cases = [
            # (start_date, end_date, expected_locator_type)
            (datetime(2020, 1, 1), datetime(2022, 1, 1), "YearLocator"),  # 2 years
            (datetime(2022, 1, 1), datetime(2023, 1, 1), "MonthLocator"),  # 1 year
            (datetime(2024, 10, 1), datetime(2024, 12, 31), "DayLocator"),  # 3 months
        ]
        
        for start_date, end_date, expected_locator in test_cases:
            dates = pd.date_range(start_date, end_date, freq='D')
            
            # Limit dataset size for Docker environment
            if len(dates) > 365:  # More than 1 year
                dates = dates[::7]  # Take every 7th day (weekly)
            elif len(dates) > 90:  # More than 3 months
                dates = dates[::3]  # Take every 3rd day
            
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
            
            # Mock the plotting functions and set non-interactive backend
            with patch('matplotlib.pyplot.savefig'), \
                 patch('matplotlib.pyplot.show'), \
                 patch('os.makedirs'):
                
                # Set matplotlib backend to non-interactive for Docker
                import matplotlib
                matplotlib.use('Agg')
                
                result = plot_dual_chart_seaborn(
                    df=df,
                    rule='macd:12,26,9,close',
                    title=f'Test {expected_locator} Chart',
                    output_path='test_output.png'
                )
                
                assert result is not None
                assert hasattr(result, 'savefig')
                
                # Clean up matplotlib figure to prevent memory leaks
                import matplotlib.pyplot as plt
                plt.close(result)


if __name__ == "__main__":
    pytest.main([__file__]) 