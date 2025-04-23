import unittest
import os
import pandas as pd
import numpy as np
from src.plotting.fast_plot import plot_indicator_results_fast

class DummyRule:
    name = "DummyRule"

class TestFastPlot(unittest.TestCase):

    def setUp(self):
        # Generate a numpy datetime64 array for the 'index' column
        date_index = np.arange(
            np.datetime64("2024-01-01T00:00"),
            np.datetime64("2024-01-01T00:00") + np.timedelta64(1000, "m"),
            np.timedelta64(1, "m"),
        )
        # Build DataFrame with 'index' column and OHLC columns
        self.df = pd.DataFrame({
            "index": date_index,
            "Open": np.random.rand(1000) * 100,
            "High": np.random.rand(1000) * 100 + 1,
            "Low": np.random.rand(1000) * 100 - 1,
            "Close": np.random.rand(1000) * 100,
        })
        # Ensure dtype is exactly datetime64[ns]
        self.df["index"] = pd.to_datetime(self.df["index"])
        self.rule = DummyRule()

    def test_fast_plot_smoke(self):
        """
        Smoke-test: ensure that fast plot runs and creates an output file.
        """
        # Uncomment to debug types:
        # print(self.df.dtypes)
        plot_indicator_results_fast(self.df, self.rule, title="Test Fast Plot")
        out_file = os.path.join("results", "plots", "fast_plot.html")
        self.assertTrue(os.path.exists(out_file))

if __name__ == '__main__':
    unittest.main()