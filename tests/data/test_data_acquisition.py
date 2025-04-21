# tests/data/test_data_acquisition.py (Outline for Refactoring)

import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
import argparse
import tempfile
from pathlib import Path
from datetime import datetime

# Import the function and helpers to test/mock
from src.data.data_acquisition import acquire_data, _generate_instrument_parquet_filename, _get_interval_delta
# Import fetchers to mock
from src.data.fetchers import fetch_binance_data # ... import others as needed

# Helper to create args
def create_mock_args(mode='binance', ticker='TICKER', interval='H1', start='2023-01-10', end='2023-01-15', point=0.01, **kwargs):
    args = argparse.Namespace(mode=mode, ticker=ticker, interval=interval, start=start, end=end, point=point, period=None, csv_file=None)
    args.__dict__.update(kwargs)
    return args

# Helper to create sample DataFrames
def create_sample_df(start_date_str, end_date_str, freq='H'):
    idx = pd.date_range(start=start_date_str, end=end_date_str, freq=freq, name='DateTime')
    # Ensure index is timezone-naive to match cache logic
    idx = idx.tz_localize(None)
    return pd.DataFrame({'Close': range(len(idx))}, index=idx)


class TestDataAcquisitionCaching(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for cache files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cache_dir_path = Path(self.temp_dir.name)
        # Patch the PARQUET_DIR constant or path generation if needed,
        # here we assume the helper function uses "data/raw_parquet" but we'll save to temp dir
        self.patcher_path = patch('src.data.data_acquisition.Path')
        self.MockPath = self.patcher_path.start()
        # Make Path('data/raw_parquet') return our temp dir path
        # This is slightly complex, might need adjustment based on exact Path usage
        def path_side_effect(*args):
            if args == ('data/raw_parquet',):
                return self.cache_dir_path
            return Path(*args) # Default Path behavior
        self.MockPath.side_effect = path_side_effect
        # Mock logger
        self.patcher_logger = patch('src.data.data_acquisition.logger')
        self.mock_logger = self.patcher_logger.start()


    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()
        self.patcher_path.stop()
        self.patcher_logger.stop()

    # --- Test Filename Generation ---
    def test_generate_filename_api(self):
        args = create_mock_args(mode='binance', ticker='BTC/USDT', interval='M15')
        expected_path = self.cache_dir_path / "binance_BTC_USDT_M15.parquet"
        self.assertEqual(_generate_instrument_parquet_filename(args), expected_path)

    def test_generate_filename_csv_demo(self):
        args_csv = create_mock_args(mode='csv')
        args_demo = create_mock_args(mode='demo')
        self.assertIsNone(_generate_instrument_parquet_filename(args_csv))
        self.assertIsNone(_generate_instrument_parquet_filename(args_demo))

    # --- Test Interval Delta ---
    def test_get_interval_delta(self):
        self.assertEqual(_get_interval_delta('H1'), pd.Timedelta(hours=1))
        self.assertEqual(_get_interval_delta('M15'), pd.Timedelta(minutes=15))
        self.assertEqual(_get_interval_delta('D1'), pd.Timedelta(days=1))
        self.assertEqual(_get_interval_delta('W'), pd.Timedelta(days=7))
        self.assertIsNone(_get_interval_delta('MN1')) # Check handling of unsupported yet
        self.assertIsNone(_get_interval_delta('INVALID'))


    # --- Test Cache Miss ---
    @patch('src.data.data_acquisition.fetch_binance_data')
    @patch('pandas.DataFrame.to_parquet') # Mock saving
    def test_cache_miss_fetches_api(self, mock_to_parquet, mock_fetch_binance):
        args = create_mock_args(start='2023-01-10', end='2023-01-12')
        cache_file = _generate_instrument_parquet_filename(args)
        # Ensure file does NOT exist
        self.assertFalse(cache_file.exists())

        # Mock API return
        mock_df_fetched = create_sample_df('2023-01-10', '2023-01-12 23:00')
        mock_metrics = {'api_calls': 1}
        mock_fetch_binance.return_value = (mock_df_fetched.copy(), mock_metrics)

        data_info = acquire_data(args)

        # Assertions
        mock_fetch_binance.assert_called_once_with(ticker=args.ticker, interval=args.interval, start_date=args.start, end_date=args.end)
        self.assertFalse(data_info['parquet_cache_used'])
        pd.testing.assert_frame_equal(data_info['ohlcv_df'], mock_df_fetched)
        mock_to_parquet.assert_called_once() # Should save the newly fetched data
        self.assertEqual(data_info['api_calls'], 1)


    # --- Test Exact Cache Hit ---
    @patch('src.data.data_acquisition.fetch_binance_data')
    @patch('pandas.read_parquet')
    @patch('pandas.DataFrame.to_parquet')
    def test_exact_cache_hit_loads_file(self, mock_to_parquet, mock_read_parquet, mock_fetch_binance):
        args = create_mock_args(start='2023-01-10', end='2023-01-12')
        cache_file = _generate_instrument_parquet_filename(args)

        # Simulate existing cache file
        mock_df_cached = create_sample_df('2023-01-10', '2023-01-12 23:00')
        mock_read_parquet.return_value = mock_df_cached.copy()
        # Need to mock Path.exists() for this specific file
        with patch.object(Path, 'exists', return_value=True): # Mock exists method of Path instances
            # Also mock stat().st_size if needed by logic
             with patch.object(Path, 'stat') as mock_stat:
                 mock_stat.return_value.st_size = 1024
                 data_info = acquire_data(args)

        # Assertions
        mock_read_parquet.assert_called_once_with(cache_file)
        mock_fetch_binance.assert_not_called() # API should NOT be called
        self.assertTrue(data_info['parquet_cache_used'])
        pd.testing.assert_frame_equal(data_info['ohlcv_df'], mock_df_cached) # Should return cached data
        mock_to_parquet.assert_not_called() # Should not save if only cache was used
        self.assertEqual(data_info['file_size_bytes'], 1024)
        self.assertEqual(data_info['api_calls'], 0) # No API calls

    # --- Test Fetch After Cache ---
    @patch('src.data.data_acquisition.fetch_binance_data')
    @patch('pandas.read_parquet')
    @patch('pandas.DataFrame.to_parquet')
    def test_fetch_after_cache(self, mock_to_parquet, mock_read_parquet, mock_fetch_binance):
        # Request 10th to 15th, Cache has 10th to 12th
        args = create_mock_args(start='2023-01-10', end='2023-01-15')
        cache_file = _generate_instrument_parquet_filename(args)

        # Simulate existing cache file (10-12)
        mock_df_cached = create_sample_df('2023-01-10', '2023-01-12 23:00')
        mock_read_parquet.return_value = mock_df_cached.copy()

        # Simulate API fetch for the missing range (13-15)
        mock_df_new = create_sample_df('2023-01-13', '2023-01-15 23:00')
        mock_fetch_binance.return_value = (mock_df_new.copy(), {'api_calls': 1})

        with patch.object(Path, 'exists', return_value=True), patch.object(Path, 'stat') as mock_stat:
             mock_stat.return_value.st_size = 1024
             data_info = acquire_data(args)

        # Assertions
        mock_read_parquet.assert_called_once_with(cache_file)
        # Check API was called ONLY for the missing range (13th to 15th)
        # Need interval delta (H1 -> 1 hour)
        expected_fetch_start = '2023-01-13' # Day after cache end
        expected_fetch_end = '2023-01-15'   # Requested end
        mock_fetch_binance.assert_called_once_with(ticker=args.ticker, interval=args.interval, start_date=expected_fetch_start, end_date=expected_fetch_end)

        self.assertTrue(data_info['parquet_cache_used']) # Cache was used as base
        # Check combined and sliced result
        expected_combined_len = len(mock_df_cached) + len(mock_df_new)
        # The final df should be the slice requested (10th to 15th)
        self.assertEqual(len(data_info['ohlcv_df']), expected_combined_len)
        self.assertEqual(data_info['ohlcv_df'].index.min(), pd.Timestamp('2023-01-10 00:00:00'))
        self.assertEqual(data_info['ohlcv_df'].index.max(), pd.Timestamp('2023-01-15 23:00:00'))
        mock_to_parquet.assert_called_once() # Should save the combined data

    # --- Add more tests ---
    # test_fetch_before_cache(...)
    # test_fetch_before_and_after_cache(...)
    # test_cache_read_error_fetches_api(...)
    # test_fetch_failure_during_partial_fetch(...)
    # test_yfinance_period_skips_cache(...)


# Allow running tests directly
if __name__ == '__main__':
    unittest.main()