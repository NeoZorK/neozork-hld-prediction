import unittest
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for tests
from src.plotting import mplfinance_plot
from src.common.constants import TradingRule

class TestMplfinancePlot(unittest.TestCase):
    def setUp(self):
        # Create a DataFrame with OHLCV and indicator columns
        dates = pd.date_range('2023-01-01', periods=10, freq='D')
        self.df = pd.DataFrame({
            'Open': np.random.rand(10),
            'High': np.random.rand(10),
            'Low': np.random.rand(10),
            'Close': np.random.rand(10),
            'Volume': np.random.randint(100, 200, 10),
            'PPrice1': np.random.rand(10),
            'PPrice2': np.random.rand(10),
            'PV': np.random.rand(10),
            'HL': np.random.rand(10),
            'Pressure': np.random.rand(10),
            'Direction': np.random.choice([1, -1, 0], 10)
        }, index=dates)

    def test_plot_indicator_results_mplfinance_runs(self):
        # Should not raise exceptions
        try:
            mplfinance_plot.plot_indicator_results_mplfinance(self.df, TradingRule.Pressure_Vector)
        except Exception as e:
            self.fail(f"plot_indicator_results_mplfinance raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()

