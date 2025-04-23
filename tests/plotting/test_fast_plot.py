import unittest
import os
import pandas as pd
import numpy as np

# Import here your plotting function
from src.plotting.fast_plot import plot_indicator_results_fast

class DummyRule:
    name = "DummyRule"

class TestFastPlot(unittest.TestCase):
    def setUp(self):
        # Create artificial OHLC data
        self.df = pd.DataFrame({
            "Open": np.random.rand(1000) * 100,
            "High": np.random.rand(1000) * 100 + 1,
            "Low": np.random.rand(1000) * 100 - 1,
            "Close": np.random.rand(1000) * 100,
        }, index=pd.date_range("2024-01-01", periods=1000, freq="min"))  # 'min' instead of 'T'
        # Add index as a column for Datashader compatibility
        self.df = self.df.reset_index().rename(columns={"index": "index"})
        self.rule = DummyRule()

    def test_fast_plot_smoke(self):
        """
        Smoke-test: ensure that fast plot runs and creates an output file.
        """
        plot_indicator_results_fast(self.df, self.rule, title="Test Fast Plot")
        out_file = os.path.join("results", "plots", "fast_plot.html")
        self.assertTrue(os.path.exists(out_file))

if __name__ == '__main__':
    unittest.main()