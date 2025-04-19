# tests/data/fetchers/test_csv_fetcher.py # FINAL CORRECTIONS V5 (PEP8 Fix)

import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np


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

    # ***** CORRECTED MOCKING APPROACH & ARGUMENT NAME *****
    @patch('src.data.fetchers.csv_fetcher.Path') # Mock Path object first
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv') # Mock pd.read_csv called inside fetch_csv_data
    # Rename MockPath -> mock_path
    def test_fetch_csv_data_success(self, mock_read_csv, mock_path, _):
        # Configure the mock Path object
        # Rename MockPath -> mock_path
        mock_path_instance = mock_path.return_value
        mock_path_instance.is_file.return_value = True

        # --- Manually define the DataFrame that pd.read_csv should return ---
        raw_data_for_mock = {
            'DateTime': ["2023.01.01 10:00", "2023.01.01 10:01", "2023.01.01 10:02"],
            'Open': [1.1000, 1.1001, 1.1012],
            'High': [1.1050, 1.1061, np.inf],
            'Low': [1.0950, 1.0961, 1.0972],
            'Close': [1.1000, 1.1011, -np.inf],
            'TickVolume': [1000.0, 1100.0, 1200.0],
            'Predicted_High ': [1.1060, 1.1071, 1.1082], # Keep potential space
            ' Unnamed: 7 ': [np.nan, 'garbage', np.nan], # Keep potential space and empty name part
            'AnotherCol': ['Text', '123', '45.6']
        }
        # Construct DataFrame assuming column names might have issues before cleaning
        raw_df_mock_return = pd.DataFrame(raw_data_for_mock)
        # Set columns as they might appear *after* pandas reads them (header=1)
        # but *before* our explicit strip/rstrip cleaning
        raw_df_mock_return.columns = ['DateTime','Open','High','Low','Close','TickVolume','Predicted_High ',' Unnamed: 7 ','AnotherCol']

        # Set the return value of the mock read_csv
        mock_read_csv.return_value = raw_df_mock_return
        # -------------------------------------------------------------------

        # Expected result *after* processing inside fetch_csv_data
        expected_dates = pd.to_datetime(["2023-01-01 10:00", "2023-01-01 10:01"])
        expected_data = {
            'Open': [1.1000, 1.1001], 'High': [1.1050, 1.1061], 'Low': [1.0950, 1.0961],
            'Close': [1.1000, 1.1011], 'Volume': [1000.0, 1100.0], # Renamed
            'Predicted_High': [1.1060, 1.1071], # Cleaned name
            'AnotherCol': [np.nan, 123.0]
        }
        expected_df = pd.DataFrame(expected_data, index=expected_dates, dtype=np.float64)
        expected_df.index.name = 'DateTime'

        # Call the actual function
        df_result = fetch_csv_data("dummy/path.csv")

        # Assertions
        # Rename MockPath -> mock_path
        mock_path.assert_called_once_with("dummy/path.csv")
        mock_path_instance.is_file.assert_called_once()
        mock_read_csv.assert_called_once_with(mock_path_instance, sep=',', header=1, skipinitialspace=True, low_memory=False)

        self.assertIsNotNone(df_result)
        self.assertEqual(len(df_result), 2)
        self.assertIsInstance(df_result.index, pd.DatetimeIndex)
        self.assertTrue(all(col in df_result.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume']))
        # Check problematic columns are handled/dropped
        self.assertNotIn('Unnamed: 7', [c.strip() for c in df_result.columns]) # Check stripped name
        self.assertNotIn('', df_result.columns)

        df_result.index.name = 'DateTime'
        pd.testing.assert_frame_equal(df_result[expected_df.columns], expected_df, check_like=True)


    # Rename MockPath -> mock_path
    def test_fetch_csv_data_file_not_found(self, mock_path, _):
        # Rename MockPath -> mock_path
        mock_path_instance = mock_path.return_value
        mock_path_instance.is_file.return_value = False
        df = fetch_csv_data("nonexistent/path.csv")
        self.assertIsNone(df)

    @patch('src.data.fetchers.csv_fetcher.Path')
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv')
    # Rename MockPath -> mock_path
    def test_fetch_csv_data_empty_file(self, mock_read_csv, mock_path, _):
        # Rename MockPath -> mock_path
        mock_path_instance = mock_path.return_value
        mock_path_instance.is_file.return_value = True
        mock_read_csv.return_value = pd.DataFrame()
        df = fetch_csv_data("dummy/empty.csv")
        self.assertIsNone(df)

    @patch('src.data.fetchers.csv_fetcher.Path')
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv')
    # Rename MockPath -> mock_path
    def test_fetch_csv_data_missing_datetime(self, mock_read_csv, mock_path, _):
        # Rename MockPath -> mock_path
        mock_path_instance = mock_path.return_value
        mock_path_instance.is_file.return_value = True
        raw_df_mock_return = pd.DataFrame({
            'Open': [1.1000], 'High': [1.1050], 'Low': [1.0950],
            'Close': [1.1000], 'TickVolume': [1000]
        })
        mock_read_csv.return_value = raw_df_mock_return

        df_result = fetch_csv_data("dummy/no_datetime.csv")
        self.assertIsNone(df_result)

    @patch('src.data.fetchers.csv_fetcher.Path')
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv')
    # Rename MockPath -> mock_path
    def test_fetch_csv_data_missing_ohlcv(self, mock_read_csv, mock_path, _):
        # Rename MockPath -> mock_path
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

    # ***** CORRECTED ARGUMENT NAME *****
    @patch('src.data.fetchers.csv_fetcher.Path')
    @patch('src.data.fetchers.csv_fetcher.pd.read_csv')
    # Rename MockPath -> mock_path
    def test_fetch_csv_data_invalid_datetime_format(self, mock_read_csv, mock_path, _):
        # Rename MockPath -> mock_path
        mock_path_instance = mock_path.return_value
        mock_path_instance.is_file.return_value = True

        # --- Manually define the DataFrame that pd.read_csv should return ---
        raw_data_for_mock = {
            'DateTime': ["2023-01-01 10:00", "2023.01.01 10:01"],
            'Open': [1.1, 1.2], 'High': [1.1, 1.2], 'Low': [1.1, 1.2],
            'Close': [1.1, 1.2], 'TickVolume': [100, 200]
        }
        raw_df_mock_return = pd.DataFrame(raw_data_for_mock)
        mock_read_csv.return_value = raw_df_mock_return
        # -------------------------------------------------------------------

        # Expected result *after* processing inside fetch_csv_data
        expected_dates = pd.to_datetime(["2023.01.01 10:01"], format='%Y.%m.%d %H:%M')
        expected_data = {
            'Open': [1.2],'High': [1.2],'Low': [1.2],'Close': [1.2],'Volume': [200.0]
        }
        expected_df = pd.DataFrame(expected_data, index=expected_dates, dtype=np.float64)
        expected_df.index.name = 'DateTime'

        # Call the actual function
        df_result = fetch_csv_data("dummy/mixed_datetime.csv")

        # Assertions
        mock_read_csv.assert_called_once()
        self.assertIsNotNone(df_result)
        self.assertEqual(len(df_result), 1)
        self.assertEqual(df_result.index[0], expected_dates[0])
        df_result.index.name = 'DateTime'
        pd.testing.assert_frame_equal(df_result, expected_df)


# Allow running tests directly
if __name__ == '__main__':
    unittest.main()