import unittest
import pandas as pd
from src.plotting import seaborn_plot

class TestSeabornPlot(unittest.TestCase):
    def test_plot_indicator_results_seaborn_empty(self):
        # Check with an empty DataFrame
        result = seaborn_plot.plot_indicator_results_seaborn(pd.DataFrame(), selected_rule='OHLCV')
        self.assertIsNone(result)

    def test_plot_indicator_results_seaborn_no_close(self):
        # DataFrame without a 'close' column
        df = pd.DataFrame({'open': [1,2], 'high': [2,3], 'low': [0,1]})
        result = seaborn_plot.plot_indicator_results_seaborn(df, selected_rule='OHLCV')
        self.assertIsNone(result)

    def test_plot_indicator_results_seaborn_with_close(self):
        # DataFrame with a 'close' column
        df = pd.DataFrame({'close': [1,2,3], 'open': [1,2,3], 'high': [2,3,4], 'low': [0,1,2]})
        # No specific rule, should plot OHLC
        result = seaborn_plot.plot_indicator_results_seaborn(df, selected_rule='OHLCV')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()

