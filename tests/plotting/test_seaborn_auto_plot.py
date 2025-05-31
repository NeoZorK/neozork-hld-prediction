import unittest
import pandas as pd
import tempfile
import os
from src.plotting import seaborn_auto_plot

class TestSeabornAutoPlot(unittest.TestCase):
    def test_auto_plot_from_parquet_file_not_found(self):
        #
        result = seaborn_auto_plot.auto_plot_from_parquet('not_a_file.parquet')
        self.assertIsNone(result)

    def test_auto_plot_from_parquet_empty(self):
        # Empty DataFrame
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp:
            df = pd.DataFrame()
            df.to_parquet(tmp.name)
            result = seaborn_auto_plot.auto_plot_from_parquet(tmp.name)
            self.assertIsNone(result)
            os.remove(tmp.name)

    def test_auto_plot_from_parquet_minimal(self):
        # Minimal DataFrame with OHLC columns
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp:
            df = pd.DataFrame({
                'open': [1,2], 'high': [2,3], 'low': [0,1], 'close': [1.5,2.5],
                'volume': [100, 200], 'timestamp': [1,2]
            })
            df.to_parquet(tmp.name)
            result = seaborn_auto_plot.auto_plot_from_parquet(tmp.name)
            self.assertIsNone(result)
            os.remove(tmp.name)

if __name__ == '__main__':
    unittest.main()

