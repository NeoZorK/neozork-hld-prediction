"""
Tests for terminal plotting functionality.
These tests verify that terminal-based plotting works correctly.
"""
import unittest
import pandas as pd
import numpy as np
import os
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the src directory to the path so we can import modules from there
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.common.constants import TradingRule
from src.plotting.term_plot import plot_indicator_results_term, _plot_financial_indicators_panels, _plot_predicted_prices, _plot_trading_signals

class TestTermPlot(unittest.TestCase):
    """Test cases for terminal plotting functionality."""

    def setUp(self):
        """Set up test data."""
        # Create a test DataFrame
        self.df = pd.DataFrame({
            'Open': np.random.rand(50) * 100 + 100,
            'High': np.random.rand(50) * 100 + 110,
            'Low': np.random.rand(50) * 100 + 90,
            'Close': np.random.rand(50) * 100 + 100,
            'Volume': np.random.randint(1000, 2000, 50),
            'RSI': np.random.rand(50) * 100,
            'SMA': np.random.rand(50) * 100 + 100,
            'Direction': np.random.choice([0, 1, -1], 50),
            'Signal': np.random.rand(50) * 2 - 1,
            'PPrice1': np.random.rand(50) * 100 + 105,
            'PPrice2': np.random.rand(50) * 100 + 95,
            'Pressure': np.random.rand(50) * 2 - 1,
            'HL': np.random.rand(50) * 10 - 5,
            'PV': np.random.rand(50) * 2 - 1
        })
        # Set index to datetime
        self.df.index = pd.date_range('2023-01-01', periods=50)

        # Set rule for testing
        self.rule = TradingRule.Pressure_Vector

        # For OHLCV-only testing
        self.ohlcv_rule = TradingRule.OHLCV

    @patch('plotext.show')
    def test_plot_indicator_results_term(self, mock_show):
        """Test plotting indicator results in terminal."""
        try:
            plot_indicator_results_term(self.df, self.rule)
            mock_show.assert_called()
        except Exception as e:
            self.fail(f"Terminal plotting failed: {e}")

    @patch('plotext.show')
    def test_plot_indicator_results_ohlcv_only(self, mock_show):
        """Test plotting only OHLCV data (no indicators) with OHLCV rule."""
        try:
            plot_indicator_results_term(self.df, self.ohlcv_rule)
            mock_show.assert_called()
        except Exception as e:
            self.fail(f"OHLCV-only terminal plotting failed: {e}")

    @patch('plotext.show')
    def test_plot_financial_indicators_panels(self, mock_show):
        """Test plotting financial indicators panels."""
        x_data = list(range(len(self.df)))
        x_labels = [d.strftime('%m-%d') for d in self.df.index]
        step = max(1, len(x_labels) // 8)

        try:
            _plot_financial_indicators_panels(self.df, x_data, x_labels, step, self.rule)
            mock_show.assert_called()
        except Exception as e:
            self.fail(f"Financial indicators plotting failed: {e}")

    @patch('plotext.show')
    def test_plot_financial_indicators_panels_ohlcv(self, mock_show):
        """Test plotting financial indicators with OHLCV rule (should skip plotting)."""
        x_data = list(range(len(self.df)))
        x_labels = [d.strftime('%m-%d') for d in self.df.index]
        step = max(1, len(x_labels) // 8)

        try:
            # This should skip plotting and not call show()
            _plot_financial_indicators_panels(self.df, x_data, x_labels, step, self.ohlcv_rule)
            # The mock should NOT be called, as the function should return early
            mock_show.assert_not_called()
        except Exception as e:
            self.fail(f"OHLCV rule test failed: {e}")

    @patch('plotext.show')
    def test_plot_predicted_prices(self, mock_show):
        """Test plotting predicted prices."""
        x_data = list(range(len(self.df)))
        x_labels = [d.strftime('%m-%d') for d in self.df.index]
        step = max(1, len(x_labels) // 8)

        try:
            _plot_predicted_prices(self.df, x_data, x_labels, step, self.rule)
            # Should be called because we're using non-OHLCV rule
            mock_show.assert_called()
        except Exception as e:
            self.fail(f"Predicted prices plotting failed: {e}")

    @patch('plotext.show')
    def test_plot_predicted_prices_ohlcv(self, mock_show):
        """Test plotting predicted prices with OHLCV rule (should skip plotting)."""
        x_data = list(range(len(self.df)))
        x_labels = [d.strftime('%m-%d') for d in self.df.index]
        step = max(1, len(x_labels) // 8)

        try:
            # This should skip plotting and not call show()
            _plot_predicted_prices(self.df, x_data, x_labels, step, self.ohlcv_rule)
            # The mock should NOT be called, as the function should return early
            mock_show.assert_not_called()
        except Exception as e:
            self.fail(f"OHLCV rule test for predicted prices failed: {e}")

    @patch('plotext.show')
    def test_plot_trading_signals(self, mock_show):
        """Test plotting trading signals."""
        x_data = list(range(len(self.df)))
        x_labels = [d.strftime('%m-%d') for d in self.df.index]
        step = max(1, len(x_labels) // 8)

        try:
            _plot_trading_signals(self.df, x_data, x_labels, step, self.rule)
            # Should be called because we're using non-OHLCV rule
            mock_show.assert_called()
        except Exception as e:
            self.fail(f"Trading signals plotting failed: {e}")

    @patch('plotext.show')
    def test_plot_trading_signals_ohlcv(self, mock_show):
        """Test plotting trading signals with OHLCV rule (should skip plotting)."""
        x_data = list(range(len(self.df)))
        x_labels = [d.strftime('%m-%d') for d in self.df.index]
        step = max(1, len(x_labels) // 8)

        try:
            # This should skip plotting and not call show()
            _plot_trading_signals(self.df, x_data, x_labels, step, self.ohlcv_rule)
            # The mock should NOT be called, as the function should return early
            mock_show.assert_not_called()
        except Exception as e:
            self.fail(f"OHLCV rule test for trading signals failed: {e}")

    def test_plot_with_different_rule_types(self):
        """Test plotting with different rule types"""
        rules_to_test = [
            TradingRule.OHLCV,
            TradingRule.Pressure_Vector,
            TradingRule.Support_Resistants,
            "AUTO"
        ]
        
        for rule in rules_to_test:
            with self.subTest(rule=rule):
                try:
                    plot_indicator_results_term(self.df, rule, title=f"Test {rule}")
                except Exception as e:
                    self.fail(f"Plotting with rule {rule} failed: {e}")

    def test_large_dataset_truncation(self):
        """Test that large datasets are properly truncated"""
        large_df = pd.DataFrame({
            'Open': np.random.rand(200) * 100 + 100,
            'High': np.random.rand(200) * 100 + 110,
            'Low': np.random.rand(200) * 100 + 90,
            'Close': np.random.rand(200) * 100 + 100,
            'Volume': np.random.randint(1000, 2000, 200)
        }, index=pd.date_range('2023-01-01', periods=200, freq='D'))
        
        try:
            plot_indicator_results_term(large_df, self.rule, title="Large Dataset Test")
        except Exception as e:
            self.fail(f"Large dataset plotting failed: {e}")

if __name__ == '__main__':
    unittest.main()
