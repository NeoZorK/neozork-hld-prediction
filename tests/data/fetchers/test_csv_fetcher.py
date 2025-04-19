# tests/data/fetchers/test_csv_fetcher.py

import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np
from io import StringIO

# Function to test
from src.data.fetchers.csv_fetcher import fetch_csv_data

# Dummy logger
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass

# Patch the logger for the whole class
@patch('src.data.fetchers.csv_fetcher.logger', new_callable=MockLogger)
class TestCsvFetcher(unittest.TestCase):

    def test_fetch_csv_data_success(self, _):
        # Mock CSV data including potential issues to be cleaned
        csv_content = """
,"DateTime","Open","High","Low","Close","TickVolume", "Predicted_High", "Unnamed: 7"
0,"2023.01.01 10:00",1.1000,1.1050,1.0950,1.1000,1000, 1.1060,
1,"2023.01.01 10:01",1.1001,1.1061,1.0961,1.1011,1100, 1.1071, garbage
2,"2023.01.01 10:02",1.1012,inf,1.0972,-inf,1200, 1.1082,
"""
        # Mock Path object and pd.read_csv
        with patch('src.data.fetchers.csv_fetcher.Path') as MockPath:
            mock_path_instance = MockPath.return_value
            mock_path_instance.is_file.return_value = True # Simulate file exists

            with patch('src.data.fetchers.csv_fetcher.pd.read_csv', return_value=pd.read_csv(StringIO(csv_content), sep=',', header=1, skipinitialspace=True)) as mock_read_csv:

                df = fetch_csv_data("dummy/path.csv")

                # Assertions
                mock_path_instance.is_file.assert_called_once()
                mock_read_csv.assert_called_once()
                self.assertIsNotNone(df)
                self.assertEqual(len(df), 3)
                self.assertIsInstance(df.index, pd.DatetimeIndex)
                self.assertListEqual(list(df.columns), ['Open', 'High', 'Low', 'Close', 'Volume', 'Predicted_High']) # Check final columns
                self.assertEqual(df.iloc[0]['Open'], 1.1000)
                self.assertEqual(df.iloc[0]['Volume'], 1000)
                self.assertTrue(np.isnan(df.iloc[2]['High'])) # Check inf replaced
                self.assertTrue(np.isnan(df.iloc[2]['Low'])) # Check -inf replaced

    def test_fetch_csv_data_file_not_found(self, _):
        with patch('src.data.fetchers.csv_fetcher.Path') as MockPath:
            mock_path_instance = MockPath.return_value
            mock_path_instance.is_file.return_value = False # Simulate file does not exist
            df = fetch_csv_data("nonexistent/path.csv")
            self.assertIsNone(df)

    def test_fetch_csv_data_empty_file(self, _):
        #csv_content = "" # Empty file content
        with patch('src.data.fetchers.csv_fetcher.Path') as MockPath:
            mock_path_instance = MockPath.return_value
            mock_path_instance.is_file.return_value = True
            # Simulate pd.errors.EmptyDataError or empty DataFrame return
            with patch('src.data.fetchers.csv_fetcher.pd.read_csv', side_effect=pd.errors.EmptyDataError):
                 df = fetch_csv_data("dummy/empty.csv")
                 self.assertIsNone(df)
            # OR simulate empty DataFrame return
            with patch('src.data.fetchers.csv_fetcher.pd.read_csv', return_value=pd.DataFrame()):
                 df = fetch_csv_data("dummy/empty.csv")
                 self.assertIsNone(df)


    def test_fetch_csv_data_missing_datetime(self, _):
        csv_content = """
,"Open","High","Low","Close","TickVolume"
0,1.1000,1.1050,1.0950,1.1000,1000
"""
        with patch('src.data.fetchers.csv_fetcher.Path') as MockPath:
            mock_path_instance = MockPath.return_value
            mock_path_instance.is_file.return_value = True
            with patch('src.data.fetchers.csv_fetcher.pd.read_csv', return_value=pd.read_csv(StringIO(csv_content), sep=',', header=1, skipinitialspace=True)):
                df = fetch_csv_data("dummy/no_datetime.csv")
                self.assertIsNone(df)

    def test_fetch_csv_data_missing_ohlcv(self, _):
        csv_content = """
,"DateTime","Open","High","Low","TickVolume"
0,"2023.01.01 10:00",1.1000,1.1050,1.0950,1000
""" # Missing Close
        with patch('src.data.fetchers.csv_fetcher.Path') as MockPath:
            mock_path_instance = MockPath.return_value
            mock_path_instance.is_file.return_value = True
            with patch('src.data.fetchers.csv_fetcher.pd.read_csv', return_value=pd.read_csv(StringIO(csv_content), sep=',', header=1, skipinitialspace=True)):
                df = fetch_csv_data("dummy/missing_ohlcv.csv")
                self.assertIsNone(df) # Should fail validation

    def test_fetch_csv_data_invalid_datetime_format(self, _):
        csv_content = """
,"DateTime","Open","High","Low","Close","TickVolume"
0,"2023-01-01 10:00",1.1,1.1,1.1,1.1,100 # Wrong format
1,"2023.01.01 10:01",1.2,1.2,1.2,1.2,200 # Correct format
"""
        with patch('src.data.fetchers.csv_fetcher.Path') as MockPath:
            mock_path_instance = MockPath.return_value
            mock_path_instance.is_file.return_value = True
            with patch('src.data.fetchers.csv_fetcher.pd.read_csv', return_value=pd.read_csv(StringIO(csv_content), sep=',', header=1, skipinitialspace=True)):
                df = fetch_csv_data("dummy/mixed_datetime.csv")
                self.assertIsNotNone(df)
                self.assertEqual(len(df), 1) # Only the valid row should remain
                self.assertEqual(df.index[0], pd.Timestamp('2023-01-01 10:01:00'))

# Allow running tests directly
if __name__ == '__main__':
    unittest.main()