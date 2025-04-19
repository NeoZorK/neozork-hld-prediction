# tests/data/fetchers/test_demo_fetcher.py

import unittest
import pandas as pd
from unittest.mock import patch

# Function to test
from src.data.fetchers.demo_fetcher import get_demo_data

# Dummy logger
class MockLogger:
    def print_info(self, msg): pass

@patch('src.data.fetchers.demo_fetcher.logger', new_callable=MockLogger)
class TestDemoFetcher(unittest.TestCase):

    def test_get_demo_data_returns_dataframe(self, _):
        df = get_demo_data()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)

    def test_get_demo_data_columns(self, _):
        df = get_demo_data()
        expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.assertListEqual(list(df.columns), expected_columns)

    def test_get_demo_data_index_type(self, _):
        df = get_demo_data()
        self.assertIsInstance(df.index, pd.DatetimeIndex)

    def test_get_demo_data_data_types(self, _):
        df = get_demo_data()
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            self.assertTrue(pd.api.types.is_numeric_dtype(df[col]))

# Allow running tests directly
if __name__ == '__main__':
    unittest.main()