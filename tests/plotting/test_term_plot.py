import unittest
import pandas as pd
import numpy as np
from src.plotting.term_plot import (
    plot_indicator_results_term,
    _plot_financial_indicators_panels,
    _plot_predicted_prices,
    _plot_trading_signals,
    _calculate_simple_indicators
)
from src.common.constants import TradingRule

class TestTermPlot(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'Open': np.random.rand(10) * 100 + 100,
            'High': np.random.rand(10) * 100 + 110,
            'Low': np.random.rand(10) * 100 + 90,
            'Close': np.random.rand(10) * 100 + 100,
            'Volume': np.random.randint(1000, 2000, 10),
            'PV': np.random.randn(10),
            'HL': np.random.randn(10),
            'Pressure': np.random.randn(10),
            'RSI': np.random.rand(10) * 100,
            'MA': np.random.rand(10) * 100 + 100,
            'MACD': np.random.randn(10),
            'Signal': np.random.randn(10),
            'PPrice1': np.random.rand(10) * 100 + 95,
            'PPrice2': np.random.rand(10) * 100 + 105,
            'Direction': np.random.choice([1, -1, 0], 10),
            'predicted_high': np.random.rand(10) * 100 + 105,
            'predicted_low': np.random.rand(10) * 100 + 95
        }, index=pd.date_range('2023-01-01', periods=10, freq='D'))
        self.rule = TradingRule.Pressure_Vector

    def test_plot_indicator_results_term_runs(self):
        """Test that main plotting function runs without exceptions"""
        try:
            plot_indicator_results_term(self.df, self.rule, title="Test Terminal Plot")
        except Exception as e:
            self.fail(f"plot_indicator_results_term raised an exception: {e}")

    def test_plot_with_empty_dataframe(self):
        """Test plotting with empty DataFrame"""
        empty_df = pd.DataFrame()
        try:
            plot_indicator_results_term(empty_df, self.rule, title="Empty Test")
        except Exception as e:
            self.fail(f"Plotting empty DataFrame should not raise exception: {e}")

    def test_plot_with_minimal_data(self):
        """Test plotting with minimal OHLC data only"""
        minimal_df = pd.DataFrame({
            'Open': [100, 101, 102],
            'High': [105, 106, 107],
            'Low': [95, 96, 97],
            'Close': [102, 103, 104]
        }, index=pd.date_range('2023-01-01', periods=3, freq='D'))
        
        try:
            plot_indicator_results_term(minimal_df, self.rule, title="Minimal Test")
        except Exception as e:
            self.fail(f"Plotting minimal DataFrame should not raise exception: {e}")

    def test_calculate_simple_indicators(self):
        """Test automatic indicator calculation"""
        df_basic = pd.DataFrame({
            'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
        }, index=pd.date_range('2023-01-01', periods=10, freq='D'))
        
        df_with_indicators = _calculate_simple_indicators(df_basic)
        
        # Check that SMA and RSI were calculated
        self.assertIn('SMA', df_with_indicators.columns)
        self.assertIn('RSI', df_with_indicators.columns)
        
        # Check that calculated values are reasonable
        self.assertTrue(df_with_indicators['SMA'].notna().any())
        self.assertTrue(df_with_indicators['RSI'].notna().any())
        
        # RSI should be between 0 and 100
        rsi_values = df_with_indicators['RSI'].dropna()
        if len(rsi_values) > 0:
            self.assertTrue(all(0 <= val <= 100 for val in rsi_values))

    def test_financial_indicators_panels(self):
        """Test plotting of financial indicators in separate panels"""
        x_data = list(range(len(self.df)))
        x_labels = ['T' + str(i) for i in x_data]
        step = 2
        
        try:
            _plot_financial_indicators_panels(self.df, x_data, x_labels, step)
        except Exception as e:
            self.fail(f"Financial indicators panel plotting failed: {e}")

    def test_predicted_prices_plotting(self):
        """Test plotting of predicted prices"""
        x_data = list(range(len(self.df)))
        x_labels = ['T' + str(i) for i in x_data]
        step = 2
        
        try:
            _plot_predicted_prices(self.df, x_data, x_labels, step)
        except Exception as e:
            self.fail(f"Predicted prices plotting failed: {e}")

    def test_trading_signals_plotting(self):
        """Test plotting of trading signals"""
        x_data = list(range(len(self.df)))
        x_labels = ['T' + str(i) for i in x_data]
        step = 2
        
        try:
            _plot_trading_signals(self.df, x_data, x_labels, step)
        except Exception as e:
            self.fail(f"Trading signals plotting failed: {e}")

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
