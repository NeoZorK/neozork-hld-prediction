"""
Test indicator terminal plotting functionality.
"""

import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

from src.plotting.term_chunked_plot import (
    plot_indicator_chunks,
    _add_indicator_chart_to_subplot,
    _add_rsi_indicator_to_subplot,
    _add_stochastic_indicator_to_subplot,
    _add_cci_indicator_to_subplot,
    _add_bollinger_bands_to_subplot,
    _add_ema_indicator_to_subplot,
    _add_adx_indicator_to_subplot,
    _add_sar_indicator_to_subplot,
    _add_supertrend_indicator_to_subplot,
    _add_atr_indicator_to_subplot,
    _add_std_indicator_to_subplot,
    _add_obv_indicator_to_subplot,
    _add_vwap_indicator_to_subplot,
    _add_hma_indicator_to_subplot,
    _add_tsf_indicator_to_subplot,
    _add_monte_carlo_indicator_to_subplot,
    _add_kelly_indicator_to_subplot,
    _add_putcall_indicator_to_subplot,
    _add_cot_indicator_to_subplot,
    _add_fear_greed_indicator_to_subplot,
    _add_pivot_points_to_subplot,
    _add_fibonacci_indicator_to_subplot,
    _add_donchian_indicator_to_subplot,
    _add_generic_indicator_to_subplot
)


class TestIndicatorTerminalPlot(unittest.TestCase):
    """Test indicator terminal plotting functionality."""

    def setUp(self):
        """Set up test data."""
        # Create sample data
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': np.random.uniform(1.0, 2.0, 50),
            'High': np.random.uniform(1.0, 2.0, 50),
            'Low': np.random.uniform(1.0, 2.0, 50),
            'Close': np.random.uniform(1.0, 2.0, 50),
            'Volume': np.random.uniform(1000, 10000, 50),
            'RSI': np.random.uniform(0, 100, 50),
            'Stochastic_K': np.random.uniform(0, 100, 50),
            'Stochastic_D': np.random.uniform(0, 100, 50),
            'CCI': np.random.uniform(-200, 200, 50),
            'BB_Upper': np.random.uniform(1.5, 2.5, 50),
            'BB_Middle': np.random.uniform(1.0, 2.0, 50),
            'BB_Lower': np.random.uniform(0.5, 1.5, 50),
            'EMA_20': np.random.uniform(1.0, 2.0, 50),
            'ADX': np.random.uniform(0, 100, 50),
            'DI_Plus': np.random.uniform(0, 100, 50),
            'DI_Minus': np.random.uniform(0, 100, 50),
            'SAR': np.random.uniform(1.0, 2.0, 50),
            'SuperTrend': np.random.uniform(1.0, 2.0, 50),
            'ATR': np.random.uniform(0.01, 0.1, 50),
            'Standard_Deviation': np.random.uniform(0.01, 0.1, 50),
            'OBV': np.random.uniform(1000000, 10000000, 50),
            'VWAP': np.random.uniform(1.0, 2.0, 50),
            'HMA': np.random.uniform(1.0, 2.0, 50),
            'TSF': np.random.uniform(1.0, 2.0, 50),
            'Monte_Carlo': np.random.uniform(0, 1, 50),
            'Kelly_Criterion': np.random.uniform(-0.5, 0.5, 50),
            'Put_Call_Ratio': np.random.uniform(0.5, 2.0, 50),
            'COT': np.random.uniform(-100, 100, 50),
            'Fear_Greed': np.random.uniform(0, 100, 50),
            'PP': np.random.uniform(1.0, 2.0, 50),
            'R1': np.random.uniform(1.5, 2.5, 50),
            'S1': np.random.uniform(0.5, 1.5, 50),
            'Fib_0': np.random.uniform(1.0, 2.0, 50),
            'Fib_236': np.random.uniform(1.0, 2.0, 50),
            'Fib_618': np.random.uniform(1.0, 2.0, 50),
            'Donchian_Upper': np.random.uniform(1.5, 2.5, 50),
            'Donchian_Middle': np.random.uniform(1.0, 2.0, 50),
            'Donchian_Lower': np.random.uniform(0.5, 1.5, 50),
            'Direction': np.random.choice([0, 1, 2], 50)
        }, index=dates)

    @patch('src.plotting.term_chunked_plot.plt')
    def test_plot_indicator_chunks(self, mock_plt):
        """Test plot_indicator_chunks function."""
        try:
            plot_indicator_chunks(self.sample_data, 'RSI', 'Test RSI')
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_rsi_indicator_to_subplot(self):
        """Test adding RSI indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_rsi_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_rsi_indicator_to_subplot_with_custom_levels(self):
        """Test adding RSI indicator to subplot with custom levels."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_rsi_indicator_to_subplot(chunk, x_values, "rsi:14,10,90,open")
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_stochastic_indicator_to_subplot(self):
        """Test adding Stochastic indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_stochastic_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_cci_indicator_to_subplot(self):
        """Test adding CCI indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_cci_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_bollinger_bands_to_subplot(self):
        """Test adding Bollinger Bands to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_bollinger_bands_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_ema_indicator_to_subplot(self):
        """Test adding EMA indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_ema_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_adx_indicator_to_subplot(self):
        """Test adding ADX indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_adx_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_sar_indicator_to_subplot(self):
        """Test adding SAR indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_sar_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_supertrend_indicator_to_subplot(self):
        """Test adding SuperTrend indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_supertrend_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_atr_indicator_to_subplot(self):
        """Test adding ATR indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_atr_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_std_indicator_to_subplot(self):
        """Test adding Standard Deviation indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_std_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_obv_indicator_to_subplot(self):
        """Test adding OBV indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_obv_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_vwap_indicator_to_subplot(self):
        """Test adding VWAP indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_vwap_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_hma_indicator_to_subplot(self):
        """Test adding HMA indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_hma_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_tsf_indicator_to_subplot(self):
        """Test adding Time Series Forecast indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_tsf_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_monte_carlo_indicator_to_subplot(self):
        """Test adding Monte Carlo indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_monte_carlo_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_kelly_indicator_to_subplot(self):
        """Test adding Kelly Criterion indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_kelly_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_putcall_indicator_to_subplot(self):
        """Test adding Put/Call Ratio indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_putcall_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_cot_indicator_to_subplot(self):
        """Test adding COT indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_cot_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_fear_greed_indicator_to_subplot(self):
        """Test adding Fear & Greed indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_fear_greed_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_pivot_points_to_subplot(self):
        """Test adding Pivot Points to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_pivot_points_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_fibonacci_indicator_to_subplot(self):
        """Test adding Fibonacci Retracement to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_fibonacci_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_donchian_indicator_to_subplot(self):
        """Test adding Donchian Channel to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_donchian_indicator_to_subplot(chunk, x_values)
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_generic_indicator_to_subplot(self):
        """Test adding generic indicator to subplot."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        try:
            _add_generic_indicator_to_subplot(chunk, x_values, 'Custom_Indicator')
            self.assertTrue(True)  # Function executed successfully
        except Exception as e:
            self.fail(f"Function failed with error: {e}")

    def test_add_indicator_chart_to_subplot_all_indicators(self):
        """Test _add_indicator_chart_to_subplot with all indicator types."""
        chunk = self.sample_data.head(10)
        x_values = list(range(len(chunk)))
        
        indicators = [
            'RSI', 'STOCHASTIC', 'CCI', 'BOLLINGER_BANDS', 'EMA', 'ADX', 'SAR',
            'SUPERTREND', 'ATR', 'STANDARD_DEVIATION', 'OBV', 'VWAP', 'HMA',
            'TIME_SERIES_FORECAST', 'MONTE_CARLO', 'KELLY_CRITERION',
            'PUT_CALL_RATIO', 'COT', 'FEAR_GREED', 'PIVOT_POINTS',
            'FIBONACCI_RETRACEMENT', 'DONCHIAN_CHANNEL', 'UNKNOWN_INDICATOR'
        ]
        
        for indicator in indicators:
            try:
                _add_indicator_chart_to_subplot(chunk, x_values, indicator)
                self.assertTrue(True)  # Function executed successfully
            except Exception as e:
                self.fail(f"Function failed for indicator {indicator} with error: {e}")


if __name__ == '__main__':
    unittest.main()
