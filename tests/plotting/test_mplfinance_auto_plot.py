import unittest
import pandas as pd
import numpy as np
import os
import tempfile
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for tests
from src.plotting import mplfinance_auto_plot

class TestMplfinanceAutoPlot(unittest.TestCase):
    def setUp(self):
        # Create a temporary parquet file with OHLCV and extra columns
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.temp_dir.name, 'test.parquet')
        dates = pd.date_range('2023-01-01', periods=10, freq='D')
        df = pd.DataFrame({
            'datetime': dates,
            'open': np.random.rand(10),
            'high': np.random.rand(10),
            'low': np.random.rand(10),
            'close': np.random.rand(10),
            'volume': np.random.randint(100, 200, 10),
            'predicted_high': np.random.rand(10),
            'predicted_low': np.random.rand(10)
        })
        df.to_parquet(self.file_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_auto_plot_from_parquet_runs(self):
        # Should not raise exceptions
        try:
            mplfinance_auto_plot.auto_plot_from_parquet(self.file_path)
        except Exception as e:
            self.fail(f"auto_plot_from_parquet raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()

