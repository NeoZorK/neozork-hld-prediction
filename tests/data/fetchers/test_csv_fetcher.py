# tests/data/fetchers/test_csv_fetcher.py # FINAL CORRECTIONS V3

import unittest
from unittest.mock import patch, mock_open, MagicMock # Import MagicMock
import pandas as pd
import numpy as np
from io import StringIO
from pathlib import Path # Import Path

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

    # ***** CORRECTED MOCKING APPROACH for pd.read_csv *****
    @patch('src.data.fetchers.csv_fetcher.Path') # Mock Path object first
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv') # Mock pd.read_csv called inside fetch_csv_data
    def test_fetch_csv_data_success(self, mock_read_csv, MockPath, _):
        csv_content = """
,"DateTime","Open","High","Low","Close","TickVolume", "Predicted_High ", " Unnamed: 7 ", "AnotherCol"
0,"2023.01.01 10:00",1.1000,1.1050,1.0950,1.1000,1000, 1.1060,, "Text"
1,"2023.01.01 10:01",1.1001,1.1061,1.0961,1.1011,1100, 1.1071, garbage, "123"
2,"2023.01.01 10:02",1.1012,inf,1.0972,-inf,1200, 1.1082,, "45.6"
"""
        # Configure the mock Path object
        mock_path_instance = MockPath.return_value
        mock_path_instance.is_file.return_value = True

        # Configure the mock pd.read_csv to return the DataFrame when called
        # We read the string here to simulate what read_csv would return
        df_read = pd.read_csv(StringIO(csv_content), sep=',', header=1, skipinitialspace=True)
        mock_read_csv.return_value = df_read

        # Expected result *after* processing inside fetch_csv_data
        expected_dates = pd.to_datetime(["2023-01-01 10:00", "2023-01-01 10:01"])
        expected_data = {
            'Open': [1.1000, 1.1001], 'High': [1.1050, 1.1061], 'Low': [1.0950, 1.0961],
            'Close': [1.1000, 1.1011], 'Volume': [1000.0, 1100.0],
            'Predicted_High': [1.1060, 1.1071], 'AnotherCol': [np.nan, 123.0] # 'Text' becomes NaN, '123' becomes float
        }
        # Use float64 for consistency, especially with NaN/Inf handling
        expected_df = pd.DataFrame(expected_data, index=expected_dates, dtype=np.float64)
        expected_df.index.name = 'DateTime'

        # Call the actual function
        df_result = fetch_csv_data("dummy/path.csv")

        # Assertions
        MockPath.assert_called_once_with("dummy/path.csv")
        mock_path_instance.is_file.assert_called_once()
        # Assert that pd.read_csv was called by fetch_csv_data with expected args
        mock_read_csv.assert_called_once_with(mock_path_instance, sep=',', header=1, skipinitialspace=True, low_memory=False)

        self.assertIsNotNone(df_result) # Should not be None now
        self.assertEqual(len(df_result), 2) # Row with inf/-inf should be dropped by dropna OHLCV
        self.assertIsInstance(df_result.index, pd.DatetimeIndex)
        self.assertTrue(all(col in df_result.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume']))
        df_result.index.name = 'DateTime' # Ensure name consistency for comparison
        # Compare only expected columns, allow for extra processed columns if any
        pd.testing.assert_frame_equal(df_result[expected_df.columns], expected_df)


    def test_fetch_csv_data_file_not_found(self, _):
        # This test was likely correct, mocking Path suffices
        with patch('src.data.fetchers.csv_fetcher.Path') as MockPath:
            mock_path_instance = MockPath.return_value
            mock_path_instance.is_file.return_value = False
            df = fetch_csv_data("nonexistent/path.csv")
            self.assertIsNone(df)

    @patch('src.data.fetchers.csv_fetcher.Path')
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv')
    def test_fetch_csv_data_empty_file(self, mock_read_csv, MockPath, _):
        # Simulate read_csv returning an empty DataFrame
        mock_path_instance = MockPath.return_value
        mock_path_instance.is_file.return_value = True
        mock_read_csv.return_value = pd.DataFrame() # Return empty DF
        df = fetch_csv_data("dummy/empty.csv")
        self.assertIsNone(df) # Function should return None if read gives empty

    @patch('src.data.fetchers.csv_fetcher.Path')
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv')
    def test_fetch_csv_data_missing_datetime(self, mock_read_csv, MockPath, _):
        csv_content = """
,"Open","High","Low","Close","TickVolume"
0,1.1000,1.1050,1.0950,1.1000,1000
"""
        mock_path_instance = MockPath.return_value
        mock_path_instance.is_file.return_value = True
        # Simulate reading this content
        df_read = pd.read_csv(StringIO(csv_content), sep=',', header=1, skipinitialspace=True)
        mock_read_csv.return_value = df_read
        df_result = fetch_csv_data("dummy/no_datetime.csv")
        self.assertIsNone(df_result) # fetch_csv_data returns None if 'DateTime' is missing

    @patch('src.data.fetchers.csv_fetcher.Path')
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv')
    def test_fetch_csv_data_missing_ohlcv(self, mock_read_csv, MockPath, _):
        csv_content = """
,"DateTime","Open","High","Low","TickVolume"
0,"2023.01.01 10:00",1.1000,1.1050,1.0950,1000
""" # Missing Close
        mock_path_instance = MockPath.return_value
        mock_path_instance.is_file.return_value = True
        df_read = pd.read_csv(StringIO(csv_content), sep=',', header=1, skipinitialspace=True)
        mock_read_csv.return_value = df_read
        df_result = fetch_csv_data("dummy/missing_ohlcv.csv")
        self.assertIsNone(df_result) # fetch_csv_data returns None if required cols missing

    # ***** CORRECTED MOCKING APPROACH for pd.read_csv *****
    @patch('src.data.fetchers.csv_fetcher.Path')
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv')
    def test_fetch_csv_data_invalid_datetime_format(self, mock_read_csv, MockPath, _):
        csv_content = """
,"DateTime","Open","High","Low","Close","TickVolume"
0,"2023-01-01 10:00",1.1,1.1,1.1,1.1,100 # Wrong format
1,"2023.01.01 10:01",1.2,1.2,1.2,1.2,200 # Correct format
"""
        mock_path_instance = MockPath.return_value
        mock_path_instance.is_file.return_value = True
        df_read = pd.read_csv(StringIO(csv_content), sep=',', header=1, skipinitialspace=True)
        mock_read_csv.return_value = df_read

        # Expected result *after* processing inside fetch_csv_data
        expected_dates = pd.to_datetime(["2023-01-01 10:01"])
        expected_data = {
            'Open': [1.2],'High': [1.2],'Low': [1.2],'Close': [1.2],'Volume': [200.0]
        }
        expected_df = pd.DataFrame(expected_data, index=expected_dates, dtype=np.float64)
        expected_df.index.name = 'DateTime' # Set name after creation

        # Call the actual function
        df_result = fetch_csv_data("dummy/mixed_datetime.csv")

        # Assertions
        mock_read_csv.assert_called_once()
        self.assertIsNotNone(df_result) # Should not be None now
        self.assertEqual(len(df_result), 1) # Only the row with valid date remains
        self.assertEqual(df_result.index[0], pd.Timestamp('2023-01-01 10:01:00'))
        df_result.index.name = 'DateTime' # Ensure name for comparison
        pd.testing.assert_frame_equal(df_result, expected_df)


# Allow running tests directly
if __name__ == '__main__':
    unittest.main()