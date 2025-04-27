# -*- coding: utf-8 -*-
# tests/plotting/test_fastest_plot.py

import unittest
import os
import pandas as pd
import numpy as np

from src.plotting.fastest_plot import plot_indicator_results_fastest

class DummyRule:
    """Dummy trading rule for testing purposes."""
    name = "DummyRule"

class TestFastestPlot(unittest.TestCase):
    """Unittest for fastest_plot.py using plot_indicator_results_fastest."""

    def setUp(self):
        # Generate a DataFrame with synthetic OHLCV data
        date_index = pd.date_range(start="2024-01-01", periods=1000, freq="min")  # was freq="T"
        self.df = pd.DataFrame({
            "index": date_index,
            "Open": np.random.rand(1000) * 100,
            "High": np.random.rand(1000) * 100 + 1,
            "Low": np.random.rand(1000) * 100 - 1,
            "Close": np.random.rand(1000) * 100,
            "Volume": np.random.randint(1000, 10000, size=1000),
            "PV": np.random.randn(1000) * 2,
            "HL": None,
            "Pressure": np.random.randn(1000) * 1.5,
            "PPrice1": None,
            "PPrice2": None,
            "Direction": np.random.choice([1, 2], size=1000, p=[0.5, 0.5]),
        })
        # Calculate HL as the difference between High and Low
        self.df["HL"] = self.df["High"] - self.df["Low"]
        # Calculate PPrice1 (predicted low) as slightly below actual Low
        self.df["PPrice1"] = self.df["Low"] * 0.995
        # Calculate PPrice2 (predicted high) as slightly above actual High
        self.df["PPrice2"] = self.df["High"] * 1.005
        self.df["index"] = pd.to_datetime(self.df["index"])
        self.rule = DummyRule()

        # Output path for the plot
        self.output_path = os.path.join("results", "plots", "test_fastest_plot.html")

    def tearDown(self):
        # Remove the generated plot file if it exists
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_plot_indicator_results_fastest_creates_html(self):
        """
        Smoke test: ensure that plot_indicator_results_fastest runs and creates an output HTML file.
        """
        # Run the plotting function
        fig = plot_indicator_results_fastest(
            df=self.df,
            rule=self.rule,
            title="Test Fastest Plot",
            output_path=self.output_path
        )
        # Check that the plotly Figure is returned
        self.assertIsNotNone(fig)
        # Check that the HTML file was created
        self.assertTrue(os.path.exists(self.output_path))

    def test_plot_indicator_results_fastest_handles_missing_optional_columns(self):
        """
        Test that plotting works if some optional columns are missing.
        """
        # Remove some optional columns
        df_small = self.df.drop(columns=["PPrice1", "PPrice2", "PV", "Pressure"])
        output_path_small = os.path.join("results", "plots", "test_fastest_plot_small.html")

        fig = plot_indicator_results_fastest(
            df=df_small,
            rule=self.rule,
            title="Test Fastest Plot Missing Columns",
            output_path=output_path_small
        )
        self.assertIsNotNone(fig)
        self.assertTrue(os.path.exists(output_path_small))

        # Clean up
        if os.path.exists(output_path_small):
            os.remove(output_path_small)

if __name__ == '__main__':
    unittest.main()