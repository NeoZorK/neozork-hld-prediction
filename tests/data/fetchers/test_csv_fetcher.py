# tests/data/fetchers/test_csv_fetcher.py # FINAL CORRECTIONS V7 (Revert dtype forcing in invalid_datetime test)

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np # Import numpy for other uses if needed
from pathlib import Path

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

    # Test success case
    @patch('src.data.fetchers.csv_fetcher.Path')
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv')
    def test_fetch_csv_data_success(self, mock_read_csv, mock_path, _): # Added _ for logger mock
        mock_path_instance = mock_path.return_value
        mock_path_instance.is_file.return_value = True
        raw_data_for_mock = {
            'DateTime': ["2023.01.01 10:00", "2023.01.01 10:01", "2023.01.01 10:02"],
            'Open': [1.1000, 1.1001, 1.1012], 'High': [1.1050, 1.1061, np.inf],
            'Low': [1.0950, 1.0961, 1.0972], 'Close': [1.1000, 1.1011, -np.inf],
            'TickVolume': [1000.0, 1100.0, 1200.0], # Keep as float here if original might be float
            'Predicted_High ': [1.1060, 1.1071, 1.1082],
            ' Unnamed: 7 ': [np.nan, 'garbage', np.nan],
            'AnotherCol': ['Text', '123', '45.6']
        }
        raw_df_mock_return = pd.DataFrame(raw_data_for_mock)
        raw_df_mock_return.columns = ['DateTime','Open','High','Low','Close','TickVolume','Predicted_High ',' Unnamed: 7 ','AnotherCol']
        mock_read_csv.return_value = raw_df_mock_return

        expected_dates = pd.to_datetime(["2023-01-01 10:00", "2023-01-01 10:01"])
        expected_data = {
            'Open': [1.1000, 1.1001], 'High': [1.1050, 1.1061], 'Low': [1.0950, 1.0961],
            'Close': [1.1000, 1.1011],
            'Volume': [1000.0, 1100.0], # Keep as float if source or processing ensures float
            'Predicted_High': [1.1060, 1.1071],
            'AnotherCol': [np.nan, 123.0]
        }
        # Specify float64 dtype for the whole DataFrame *if* you expect floats consistently
        # Otherwise, let pandas infer or specify per column if needed
        expected_df = pd.DataFrame(expected_data, index=expected_dates, dtype=np.float64)
        expected_df.index.name = 'DateTime'

        df_result = fetch_csv_data("dummy/path.csv")

        mock_path.assert_called_once_with("dummy/path.csv")
        mock_path_instance.is_file.assert_called_once()
        mock_read_csv.assert_called_once_with(mock_path_instance, sep=',', header=1, skipinitialspace=True, low_memory=False)
        self.assertIsNotNone(df_result)
        self.assertEqual(len(df_result), 2)
        self.assertIsInstance(df_result.index, pd.DatetimeIndex)
        self.assertTrue(all(col in df_result.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume']))
        self.assertNotIn('Unnamed: 7', [c.strip() for c in df_result.columns])
        self.assertNotIn('', df_result.columns)
        df_result.index.name = 'DateTime'
        pd.testing.assert_frame_equal(df_result[expected_df.columns], expected_df, check_like=True)

    # Test file not found
    @patch('src.data.fetchers.csv_fetcher.Path')
    def test_fetch_csv_data_file_not_found(self, mock_path, _): # Added '_' for logger mock
        mock_path_instance = mock_path.return_value
        mock_path_instance.is_file.return_value = False
        df = fetch_csv_data("nonexistent/path.csv")
        self.assertIsNone(df)
        mock_path.assert_called_once_with("nonexistent/path.csv")
        mock_path_instance.is_file.assert_called_once()

    # Test empty file
    @patch('src.data.fetchers.csv_fetcher.Path')
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv')
    def test_fetch_csv_data_empty_file(self, mock_read_csv, mock_path, _): # Added _ for logger mock
        mock_path_instance = mock_path.return_value
        mock_path_instance.is_file.return_value = True
        mock_read_csv.return_value = pd.DataFrame()
        df = fetch_csv_data("dummy/empty.csv")
        self.assertIsNone(df)

    # Test missing DateTime
    @patch('src.data.fetchers.csv_fetcher.Path')
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv')
    def test_fetch_csv_data_missing_datetime(self, mock_read_csv, mock_path, _): # Added _ for logger mock
        mock_path_instance = mock_path.return_value
        mock_path_instance.is_file.return_value = True
        raw_df_mock_return = pd.DataFrame({
            'Open': [1.1000], 'High': [1.1050], 'Low': [1.0950],
            'Close': [1.1000], 'TickVolume': [1000]
        })
        mock_read_csv.return_value = raw_df_mock_return
        df_result = fetch_csv_data("dummy/no_datetime.csv")
        self.assertIsNone(df_result)

    # Test missing OHLCV
    @patch('src.data.fetchers.csv_fetcher.Path')
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv')
    def test_fetch_csv_data_missing_ohlcv(self, mock_read_csv, mock_path, _): # Added _ for logger mock
        mock_path_instance = mock_path.return_value
        mock_path_instance.is_file.return_value = True
        raw_df_mock_return = pd.DataFrame({
            'DateTime': ["2023.01.01 10:00"],
            'Open': [1.1000], 'High': [1.1050], 'Low': [1.0950],
            'TickVolume': [1000] # Missing Close
        })
        mock_read_csv.return_value = raw_df_mock_return
        df_result = fetch_csv_data("dummy/missing_ohlcv.csv")
        self.assertIsNone(df_result)

    # ***** CORRECTED: Removed explicit dtype forcing for expected_df *****
    @patch('src.data.fetchers.csv_fetcher.Path')
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv')
    def test_fetch_csv_data_invalid_datetime_format(self, mock_read_csv, mock_path, _): # Added _ for logger mock
        mock_path_instance = mock_path.return_value
        mock_path_instance.is_file.return_value = True
        raw_data_for_mock = {
            'DateTime': ["2023-01-01 10:00", "2023.01.01 10:01"],
            'Open': [1.1, 1.2], 'High': [1.1, 1.2], 'Low': [1.1, 1.2],
            'Close': [1.1, 1.2], 'TickVolume': [100, 200] # Integers in source
        }
        raw_df_mock_return = pd.DataFrame(raw_data_for_mock)
        mock_read_csv.return_value = raw_df_mock_return

        expected_dates = pd.to_datetime(["2023.01.01 10:01"], format='%Y.%m.%d %H:%M')
        expected_data = {
            'Open': [1.2],'High': [1.2],'Low': [1.2],'Close': [1.2],
            'Volume': [200] # Use integer here to match expected int64 output
        }
        # Let pandas infer the dtypes for expected_df
        # 'Volume' should now be inferred as int64, matching the left side
        expected_df = pd.DataFrame(expected_data, index=expected_dates)
        expected_df.index.name = 'DateTime'

        df_result = fetch_csv_data("dummy/mixed_datetime.csv")

        mock_read_csv.assert_called_once()
        self.assertIsNotNone(df_result)
        self.assertEqual(len(df_result), 1)
        self.assertEqual(df_result.index[0], expected_dates[0])
        df_result.index.name = 'DateTime'
        # assert_frame_equal should now pass the dtype check for Volume
        pd.testing.assert_frame_equal(df_result, expected_df)


# Allow running tests directly
if __name__ == '__main__':
    unittest.main()