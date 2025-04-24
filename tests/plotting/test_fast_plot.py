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
            # Add additional columns needed for all plot renderers
            "Volume": np.random.randint(1000, 10000, size=1000),
            "PV": np.random.randn(1000) * 2,  # Float values around 0
            "HL": None,  # Will calculate below based on High-Low
            "Pressure": np.random.randn(1000) * 1.5,  # Float values around 0
            "PPrice1": None,  # Will calculate below based on Low values
            "PPrice2": None,  # Will calculate below based on High values
            "Direction": np.random.choice([1, 2], size=1000, p=[0.5, 0.5]),  # 1 for buy, 2 for sell
        })
        
        # Calculate HL as the difference between High and Low
        self.df["HL"] = self.df["High"] - self.df["Low"]
        
        # Calculate PPrice1 (predicted low) as slightly below actual Low
        self.df["PPrice1"] = self.df["Low"] * 0.995
        
        # Calculate PPrice2 (predicted high) as slightly above actual High
        self.df["PPrice2"] = self.df["High"] * 1.005
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