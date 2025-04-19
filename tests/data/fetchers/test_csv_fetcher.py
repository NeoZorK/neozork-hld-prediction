# tests/data/fetchers/test_csv_fetcher.py # CORRECTED

import unittest
from unittest.mock import patch, mock_open
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
,"DateTime","Open","High","Low","Close","TickVolume", "Predicted_High ", " Unnamed: 7 ", "AnotherCol"
0,"2023.01.01 10:00",1.1000,1.1050,1.0950,1.1000,1000, 1.1060,, "Text"
1,"2023.01.01 10:01",1.1001,1.1061,1.0961,1.1011,1100, 1.1071, garbage, "123"
2,"2023.01.01 10:02",1.1012,inf,1.0972,-inf,1200, 1.1082,, "45.6"
"""
        # Expected DataFrame after cleaning (OHLCV must be present and not NaN)
        # Rows with NaN in required OHLCV columns after coercion/inf handling will be dropped
        expected_dates = pd.to_datetime(["2023-01-01 10:00", "2023-01-01 10:01"]) # Row 2 dropped due to NaN High/Close
        expected_data = {
            'Open': [1.1000, 1.1001],
            'High': [1.1050, 1.1061],
            'Low': [1.0950, 1.0961],
            'Close': [1.1000, 1.1011],
            'Volume': [1000.0, 1100.0],
            'Predicted_High': [1.1060, 1.1071], # This column might exist or not depending on CSV
            'AnotherCol': [np.nan, 123.0] # Coerced to numeric
        }
        # Only include columns expected to be present after cleaning and potential drops
        expected_df = pd.DataFrame(expected_data, index=expected_dates)

        with patch('src.data.fetchers.csv_fetcher.Path') as MockPath:
            mock_path_instance = MockPath.return_value
            mock_path_instance.is_file.return_value = True
            with patch('src.data.fetchers.csv_fetcher.pd.read_csv', return_value=pd.read_csv(StringIO(csv_content), sep=',', header=1, skipinitialspace=True)):
                df = fetch_csv_data("dummy/path.csv")

                self.assertIsNotNone(df) # CORRECTED: Should not be None
                self.assertEqual(len(df), 2) # CORRECTED: Only 2 rows should remain
                self.assertIsInstance(df.index, pd.DatetimeIndex)
                self.assertTrue(all(col in df.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume']))
                # Compare relevant parts, allow extra columns if needed
                pd.testing.assert_frame_equal(df[['Open','High','Low','Close','Volume']], expected_df[['Open','High','Low','Close','Volume']])

    def test_fetch_csv_data_file_not_found(self, _):
        with patch('src.data.fetchers.csv_fetcher.Path') as MockPath:
            mock_path_instance = MockPath.return_value
            mock_path_instance.is_file.return_value = False
            df = fetch_csv_data("nonexistent/path.csv")
            self.assertIsNone(df)

    def test_fetch_csv_data_empty_file(self, _):
        # CORRECTED: Simulate read_csv returning an empty DataFrame directly
        with patch('src.data.fetchers.csv_fetcher.Path') as MockPath:
            mock_path_instance = MockPath.return_value
            mock_path_instance.is_file.return_value = True
            with patch('src.data.fetchers.csv_fetcher.pd.read_csv', return_value=pd.DataFrame()):
                 df = fetch_csv_data("dummy/empty.csv")
                 self.assertIsNone(df) # Function should return None if read_csv gives empty

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
0,"2023-01-01 10:00",1.1,1.1,1.1,1.1,100 # Wrong format -> NaN DateTime -> Row dropped
1,"2023.01.01 10:01",1.2,1.2,1.2,1.2,200 # Correct format
"""
        expected_dates = pd.to_datetime(["2023-01-01 10:01"])
        expected_data = {
            'Open': [1.2],'High': [1.2],'Low': [1.2],'Close': [1.2],'Volume': [200.0]
        }
        expected_df = pd.DataFrame(expected_data, index=expected_dates, dtype=np.float64)

        with patch('src.data.fetchers.csv_fetcher.Path') as MockPath:
            mock_path_instance = MockPath.return_value
            mock_path_instance.is_file.return_value = True
            with patch('src.data.fetchers.csv_fetcher.pd.read_csv', return_value=pd.read_csv(StringIO(csv_content), sep=',', header=1, skipinitialspace=True)):
                df = fetch_csv_data("dummy/mixed_datetime.csv")

                self.assertIsNotNone(df) # CORRECTED: Should not be None
                self.assertEqual(len(df), 1) # Only the valid row should remain
                self.assertEqual(df.index[0], pd.Timestamp('2023-01-01 10:01:00'))
                pd.testing.assert_frame_equal(df, expected_df)

# Allow running tests directly
if __name__ == '__main__':
    unittest.main()