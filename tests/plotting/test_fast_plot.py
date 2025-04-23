import unittest
import os
import pandas as pd
import numpy as np
from src.plotting.fast_plot import plot_indicator_results_fast

class DummyRule:
    name = "DummyRule"

class TestFastPlot(unittest.TestCase):

    def setUp(self):
        # Generate datetime index
        date_index = pd.date_range("2024-01-01", periods=1000, freq="min")
        # Create DataFrame with required OHLC data
        self.df = pd.DataFrame({
            "Open": np.random.rand(1000) * 100,
            "High": np.random.rand(1000) * 100 + 1,
            "Low": np.random.rand(1000) * 100 - 1,
            "Close": np.random.rand(1000) * 100,
        })
        # Add 'index' column as datetime64[ns]
        self.df["index"] = date_index.astype("datetime64[ns]")
        # OPTIONAL: set index if your plotting function expects it
        # self.df = self.df.set_index("index")
        self.rule = DummyRule()

    def test_fast_plot_smoke(self):
        """
        Smoke-test: ensure that fast plot runs and creates an output file.
        """
        # Debug: check dtype
        # print(self.df.dtypes)
        plot_indicator_results_fast(self.df, self.rule, title="Test Fast Plot")
        out_file = os.path.join("results", "plots", "fast_plot.html")
        self.assertTrue(os.path.exists(out_file))

if __name__ == '__main__':
    unittest.main()