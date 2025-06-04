import unittest
import pandas as pd
import numpy as np
from src.plotting.term_plot import plot_indicator_results_term
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
            'MA': np.random.rand(10) * 100 + 100
        }, index=pd.date_range('2023-01-01', periods=10, freq='D'))
        self.rule = TradingRule.Pressure_Vector

    def test_plot_indicator_results_term_runs(self):
        # Should not raise exceptions
        try:
            plot_indicator_results_term(self.df, self.rule, title="Test Terminal Plot")
        except Exception as e:
            self.fail(f"plot_indicator_results_term raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
