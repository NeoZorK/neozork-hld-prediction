# tests/data/test_data_acquisition.py
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, MagicMock, call, ANY
import pandas as pd
import argparse
import tempfile
from pathlib import Path
from datetime import datetime

# Import the function and helpers to test/mock
from src.data.data_acquisition import acquire_data, _generate_instrument_parquet_filename, _get_interval_delta
# Import fetchers to mock
from src.data.fetchers import fetch_binance_data, fetch_yfinance_data, fetch_csv_data, get_demo_data


# Helper to create args remains the same...
def create_mock_args(mode='binance', ticker='TICKER', interval='h1', start='2023-01-10', end='2023-01-11', point=0.01,
                     **kwargs):
    args = argparse.Namespace(mode=mode, ticker=ticker, interval=interval, start=start, end=end, point=point,
                              period=None, csv_file=None)
    if mode == 'yf': args = argparse.Namespace(mode='yf', ticker=ticker, interval=interval, start=start, end=end,
                                               point=point, period=None, csv_file=None)
    if 'period' in kwargs and kwargs['period'] is not None: args.start = None; args.end = None
    if 'csv_file' in kwargs: args.csv_file = kwargs['csv_file']
    args.__dict__.update(kwargs)
    return args


# Helper to create sample DataFrames remains the same...
def create_sample_df(start_date_str, end_date_str, freq='h', prefix_col_name=None):
    idx = pd.date_range(start=start_date_str, end=end_date_str, freq=freq,
                        name='DateTime')  # Keep original name for simplicity here
    idx = idx.tz_localize(None)
    if idx.empty: return pd.DataFrame()
    df = pd.DataFrame({'Open': 100, 'High': 105, 'Low': 95, 'Close': 101, 'Volume': 1000}, index=idx)
    # Ensure standard OHLCV names expected by acquire_data AFTER fetcher returns
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df.index.name = 'Timestamp'  # Set standard index name
    return df


class TestDataAcquisitionCaching(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cache_dir_path = Path(self.temp_dir.name)

        self.patcher_gen_path = patch('src.data.data_acquisition._generate_instrument_parquet_filename')
        self.mock_gen_path = self.patcher_gen_path.start()

        # Updated side effect to handle cache dir structure
        def gen_path_side_effect(args):
            effective_mode = 'yfinance' if args.mode == 'yf' else args.mode
            # Cache file only relevant for API modes with a ticker
            if effective_mode not in ['yfinance', 'polygon', 'binance'] or not args.ticker:
                return None
            try:
                # API cache goes into raw_parquet subdir
                cache_dir = self.cache_dir_path / "raw_parquet"
                ticker_label = str(args.ticker).replace('/', '_').replace('-', '_').replace('=', '_').replace(':', '_')
                interval_label = str(args.interval)
                filename = f"{effective_mode}_{ticker_label}_{interval_label}.parquet"
                filepath = cache_dir / filename
                return filepath
            except Exception:
                return None

        self.mock_gen_path.side_effect = gen_path_side_effect

        # Patch the individual print functions imported into data_acquisition
        self.patcher_print_info = patch('src.data.data_acquisition.print_info')
        self.patcher_print_warning = patch('src.data.data_acquisition.print_warning')
        self.patcher_print_error = patch('src.data.data_acquisition.print_error')
        self.patcher_print_debug = patch('src.data.data_acquisition.print_debug')

        # Start the patchers
        self.mock_print_info = self.patcher_print_info.start()
        self.mock_print_warning = self.patcher_print_warning.start()
        self.mock_print_error = self.patcher_print_error.start()
        self.mock_print_debug = self.patcher_print_debug.start()

        self.patcher_path_exists = patch.object(Path, 'exists')
        self.mock_path_exists = self.patcher_path_exists.start()
        self.patcher_path_stat = patch.object(Path, 'stat')
        self.mock_path_stat = self.patcher_path_stat.start()
        self.patcher_makedirs = patch('os.makedirs')
        self.mock_makedirs = self.patcher_makedirs.start()
        self.patcher_read_parquet = patch('pandas.read_parquet')
        self.mock_read_parquet = self.patcher_read_parquet.start()
        self.patcher_to_parquet = patch('pandas.DataFrame.to_parquet')
        self.mock_to_parquet = self.patcher_to_parquet.start()

        self.patcher_fetch_csv = patch('src.data.data_acquisition.fetch_csv_data')
        self.mock_fetch_csv = self.patcher_fetch_csv.start()
        self.mock_fetch_csv.return_value = pd.DataFrame()

    def tearDown(self):
        self.temp_dir.cleanup()
        self.patcher_gen_path.stop()
        # Stop logger patchers
        self.patcher_print_info.stop()
        self.patcher_print_warning.stop()
        self.patcher_print_error.stop()
        self.patcher_print_debug.stop()
        self.patcher_path_exists.stop()
        self.patcher_path_stat.stop()
        self.patcher_makedirs.stop()
        self.patcher_read_parquet.stop()
        self.patcher_to_parquet.stop()
        self.patcher_fetch_csv.stop()

        # --- Test _generate_instrument_parquet_filename ---

    def test_generate_filename_logic(self):
        self.patcher_gen_path.stop()  # Test real function
        try:
            args_yf = create_mock_args(mode='yf', ticker='MSFT', interval='1d')
            # Real function uses relative path 'data/raw_parquet'
            expected_yf = Path("data/raw_parquet") / "yfinance_MSFT_1d.parquet"
            self.assertEqual(_generate_instrument_parquet_filename(args_yf), expected_yf)

            args_poly = create_mock_args(mode='polygon', ticker='X:BTCUSD', interval='5m')
            expected_poly = Path("data/raw_parquet") / "polygon_X_BTCUSD_5m.parquet"
            self.assertEqual(_generate_instrument_parquet_filename(args_poly), expected_poly)

            args_csv = create_mock_args(mode='csv')
            self.assertIsNone(_generate_instrument_parquet_filename(args_csv))
            args_demo = create_mock_args(mode='demo')
            self.assertIsNone(_generate_instrument_parquet_filename(args_demo))

            args_no_ticker = create_mock_args(mode='binance', ticker=None)
            self.assertIsNone(_generate_instrument_parquet_filename(args_no_ticker))

        finally:
            self.patcher_gen_path.start()


        # --- Test _get_interval_delta ---
    def test_get_interval_delta(self):
            # Stop logger patchers to test real print_warning
            self.patcher_print_warning.stop()
            try:
                self.assertEqual(_get_interval_delta('h1'), pd.Timedelta(hours=1))
                self.assertEqual(_get_interval_delta('M15'), pd.Timedelta(minutes=15))
                self.assertEqual(_get_interval_delta('D1'), pd.Timedelta(days=1))
                self.assertEqual(_get_interval_delta('W'), pd.Timedelta(days=7))
                self.assertEqual(_get_interval_delta('MN1'), pd.Timedelta(days=30))  # Approx
                self.assertIsNone(_get_interval_delta('INVALID'))
                # --- FIXED ASSERTION ---
                # '15m' should be parsed directly by pd.Timedelta
                self.assertEqual(_get_interval_delta('15m'), pd.Timedelta(minutes=15))
                # --- END FIXED ASSERTION ---
                self.assertEqual(_get_interval_delta('4h'), pd.Timedelta(hours=4))
            finally:
                self.patcher_print_warning.start()  # Restart patcher


    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_cache_miss_fetches_api(self, mock_fetch_api):
        """Test YF: Cache miss fetches API and saves."""
        args = create_mock_args(mode='yf', start='2023-01-10', end='2023-01-11', interval='1d', ticker='MSFT')
        cache_file = self.cache_dir_path / "raw_parquet" / "yfinance_MSFT_1d.parquet"
        self.mock_gen_path.return_value = cache_file
        self.mock_path_exists.return_value = False
        mock_df_fetched = create_sample_df('2023-01-09', '2023-01-12', freq='D')
        mock_metrics = {'api_calls': 1, 'latency_sec': 0.5, 'rows_fetched': 4}
        mock_fetch_api.return_value = (mock_df_fetched.copy(), mock_metrics)

        data_info = acquire_data(args)

        # Check API call arguments (end_date is inclusive day + 1 day buffer)
        mock_fetch_api.assert_called_once_with(ticker='MSFT', interval='1d', start_date='2023-01-10',
                                               end_date='2023-01-12', period=None)
        self.assertFalse(data_info['parquet_cache_used'])
        self.assertEqual(data_info['ohlcv_df'].index.min(), pd.Timestamp('2023-01-10'))
        self.assertEqual(data_info['ohlcv_df'].index.max(), pd.Timestamp('2023-01-11'))
        self.assertEqual(len(data_info['ohlcv_df']), 2)
        self.mock_to_parquet.assert_called_once_with(cache_file, index=True, engine='pyarrow')
        self.assertEqual(data_info['api_calls'], 1)
        self.assertEqual(data_info['api_latency_sec'], 0.5)
        self.assertEqual(data_info['rows_fetched'], 4)

    # --- Test API Exact Cache Hit ---
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_exact_cache_hit_loads_file(self, mock_fetch_api):
        """Test YF: Exact cache hit loads file, no API call."""
        args = create_mock_args(mode='yf', start='2023-01-10', end='2023-01-11', interval='1d', ticker='MSFT')
        cache_file = self.cache_dir_path / "raw_parquet" / "yfinance_MSFT_1d.parquet"
        self.mock_gen_path.return_value = cache_file
        mock_df_cached = create_sample_df('2023-01-09', '2023-01-12', freq='D')
        self.mock_read_parquet.return_value = mock_df_cached.copy()
        self.mock_path_exists.return_value = True
        self.mock_path_stat.return_value.st_size = 1024

        data_info = acquire_data(args)

        self.mock_read_parquet.assert_called_once_with(cache_file)
        mock_fetch_api.assert_not_called()
        self.assertTrue(data_info['parquet_cache_used'])
        self.assertEqual(data_info['ohlcv_df'].index.min(), pd.Timestamp('2023-01-10'))
        self.assertEqual(data_info['ohlcv_df'].index.max(), pd.Timestamp('2023-01-11'))
        self.assertEqual(len(data_info['ohlcv_df']), 2)
        self.mock_to_parquet.assert_not_called()
        self.assertEqual(data_info['file_size_bytes'], 1024)
        self.assertEqual(data_info['api_calls'], 0)

    # --- Test API Fetch After Cache ---
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_fetch_after_cache(self, mock_fetch_api):
        """Test YF: Fetch data after cached range."""
        args = create_mock_args(mode='yf', start='2023-01-10', end='2023-01-13', interval='1d', ticker='MSFT')
        cache_file = self.cache_dir_path / "raw_parquet" / "yfinance_MSFT_1d.parquet"
        self.mock_gen_path.return_value = cache_file
        mock_df_cached = create_sample_df('2023-01-10', '2023-01-11', freq='D')
        self.mock_read_parquet.return_value = mock_df_cached.copy()
        self.mock_path_exists.return_value = True
        self.mock_path_stat.return_value.st_size = 1024
        mock_df_new = create_sample_df('2023-01-12', '2023-01-13', freq='D')
        mock_metrics_new = {'api_calls': 1, 'rows_fetched': len(mock_df_new), 'latency_sec': 0.3}
        mock_fetch_api.return_value = (mock_df_new.copy(), mock_metrics_new)

        data_info = acquire_data(args)

        self.mock_read_parquet.assert_called_once_with(cache_file)
        # Fetch should start day after cache ends (12th), API end date is inclusive requested (13th) + 1d buffer
        mock_fetch_api.assert_called_once_with(ticker='MSFT', interval='1d', start_date='2023-01-12',
                                               end_date='2023-01-14', period=None)
        self.assertTrue(data_info['parquet_cache_used'])
        self.assertEqual(data_info['ohlcv_df'].index.min(), pd.Timestamp('2023-01-10'))
        self.assertEqual(data_info['ohlcv_df'].index.max(), pd.Timestamp('2023-01-13'))
        self.assertEqual(len(data_info['ohlcv_df']), 4)
        self.mock_to_parquet.assert_called_once_with(cache_file, index=True, engine='pyarrow')
        self.assertEqual(data_info['api_calls'], 1)
        self.assertEqual(data_info['rows_fetched'], len(mock_df_new))

    # --- Test API Fetch Before Cache ---
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_yf_fetch_before_cache(self, mock_fetch_yfinance):
        """Test YF: Fetch data before cached range."""
        args = create_mock_args(mode='yf', ticker='MSFT', interval='1d', start='2023-01-10', end='2023-01-13')
        cache_file = self.cache_dir_path / "raw_parquet" / "yfinance_MSFT_1d.parquet"
        self.mock_gen_path.return_value = cache_file
        mock_df_cached = create_sample_df('2023-01-12', '2023-01-13', freq='D')
        self.mock_read_parquet.return_value = mock_df_cached.copy()
        self.mock_path_exists.return_value = True
        self.mock_path_stat.return_value.st_size = 1024
        mock_df_new = create_sample_df('2023-01-10', '2023-01-11', freq='D')
        mock_metrics_new = {'api_calls': 1, 'rows_fetched': len(mock_df_new), 'latency_sec': 0.4}
        mock_fetch_yfinance.return_value = (mock_df_new.copy(), mock_metrics_new)

        data_info = acquire_data(args)

        self.mock_read_parquet.assert_called_once_with(cache_file)
        # Fetch starts at requested start, API end date is day before cache starts (12th)
        mock_fetch_yfinance.assert_called_once_with(ticker='MSFT', interval='1d', start_date='2023-01-10',
                                                    end_date='2023-01-12', period=None)
        self.assertTrue(data_info['parquet_cache_used'])
        self.assertEqual(data_info['ohlcv_df'].index.min(), pd.Timestamp('2023-01-10'))
        self.assertEqual(data_info['ohlcv_df'].index.max(), pd.Timestamp('2023-01-13'))
        self.assertEqual(len(data_info['ohlcv_df']), 4)
        self.mock_to_parquet.assert_called_once_with(cache_file, index=True, engine='pyarrow')
        self.assertEqual(data_info['api_calls'], 1)
        self.assertEqual(data_info['rows_fetched'], len(mock_df_new))

    # --- Test API Fetch Before AND After Cache ---
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_yf_fetch_before_and_after_cache(self, mock_fetch_yfinance):
        """Test YF: Fetches data before and after cached range."""
        args = create_mock_args(mode='yf', ticker='MSFT', interval='1d', start='2023-01-10', end='2023-01-15')
        cache_file = self.cache_dir_path / "raw_parquet" / "yfinance_MSFT_1d.parquet"
        self.mock_gen_path.return_value = cache_file
        mock_df_cached = create_sample_df('2023-01-12', '2023-01-13', freq='D')
        self.mock_read_parquet.return_value = mock_df_cached.copy()
        self.mock_path_exists.return_value = True
        self.mock_path_stat.return_value.st_size = 1024
        mock_df_before = create_sample_df('2023-01-10', '2023-01-11', freq='D')
        mock_metrics_before = {'api_calls': 1, 'rows_fetched': len(mock_df_before), 'latency_sec': 0.2}
        mock_df_after = create_sample_df('2023-01-14', '2023-01-15', freq='D')
        mock_metrics_after = {'api_calls': 1, 'rows_fetched': len(mock_df_after), 'latency_sec': 0.3}

        def fetch_side_effect(**kwargs_call):  # Use **kwargs to accept args
            start_date = kwargs_call.get('start_date')
            end_date = kwargs_call.get('end_date')
            if start_date == '2023-01-10' and end_date == '2023-01-12':
                return (mock_df_before.copy(), mock_metrics_before)
            # Fetch after starts day after cache ends (14th), API end is req end (15th) + buffer
            elif start_date == '2023-01-14' and end_date == '2023-01-16':
                return (mock_df_after.copy(), mock_metrics_after)
            else:
                raise ValueError(f"Unexpected fetch call: start={start_date}, end={end_date}")

        mock_fetch_yfinance.side_effect = fetch_side_effect

        data_info = acquire_data(args)

        self.mock_read_parquet.assert_called_once_with(cache_file)
        self.assertEqual(mock_fetch_yfinance.call_count, 2)
        expected_calls = [
            call(ticker='MSFT', interval='1d', start_date='2023-01-10', end_date='2023-01-12', period=None),
            call(ticker='MSFT', interval='1d', start_date='2023-01-14', end_date='2023-01-16', period=None)
        ]
        mock_fetch_yfinance.assert_has_calls(expected_calls, any_order=True)
        self.assertTrue(data_info['parquet_cache_used'])
        self.assertEqual(data_info['ohlcv_df'].index.min(), pd.Timestamp('2023-01-10'))
        self.assertEqual(data_info['ohlcv_df'].index.max(), pd.Timestamp('2023-01-15'))
        self.assertEqual(len(data_info['ohlcv_df']), 6)
        self.mock_to_parquet.assert_called_once_with(cache_file, index=True, engine='pyarrow')
        self.assertEqual(data_info['api_calls'], 2)
        self.assertEqual(data_info['rows_fetched'], len(mock_df_before) + len(mock_df_after))
        self.assertAlmostEqual(data_info['api_latency_sec'], 0.5)

    # --- Test Period argument skips cache check ---
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_yf_period_skips_cache(self, mock_fetch_yfinance):
        """ Test YF: Using --period skips cache read and fetches fresh data. """
        args = create_mock_args(mode='yf', ticker='IBM', interval='1d', period='6mo')
        cache_file = self.cache_dir_path / "raw_parquet" / "yfinance_IBM_1d.parquet"
        self.mock_gen_path.return_value = cache_file
        self.mock_path_exists.return_value = True
        mock_df_period = create_sample_df('2023-10-21', '2024-04-20', freq='D')
        mock_metrics = {'api_calls': 1, 'rows_fetched': len(mock_df_period), 'latency_sec': 0.6}
        mock_fetch_yfinance.return_value = (mock_df_period.copy(), mock_metrics)

        data_info = acquire_data(args)

        self.mock_read_parquet.assert_not_called()
        self.assertFalse(data_info['parquet_cache_used'])
        # Call should use period kwarg
        mock_fetch_yfinance.assert_called_once_with(ticker=args.ticker, interval=args.interval, period=args.period,
                                                    start_date=None, end_date=None)
        pd.testing.assert_frame_equal(data_info['ohlcv_df'], mock_df_period)
        self.mock_to_parquet.assert_called_once_with(cache_file, index=True, engine='pyarrow')

    # --- Test Cache read error triggers API fetch ---
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_cache_read_error_fetches_api(self, mock_fetch_yfinance):
        """ Test YF: Cache read error ignores cache and fetches from API. """
        args = create_mock_args(mode='yf', ticker='CSCO', interval='1d', start='2023-02-01', end='2023-02-05')
        cache_file = self.cache_dir_path / "raw_parquet" / "yfinance_CSCO_1d.parquet"
        self.mock_gen_path.return_value = cache_file
        self.mock_path_exists.return_value = True
        self.mock_read_parquet.side_effect = Exception("Simulated Parquet read error")

        mock_df_api = create_sample_df('2023-01-31', '2023-02-06', freq='D')  # API returns wider range
        mock_metrics = {'api_calls': 1, 'latency_sec': 0.7, 'rows_fetched': len(mock_df_api)}
        mock_fetch_yfinance.return_value = (mock_df_api.copy(), mock_metrics)

        data_info = acquire_data(args)

        self.mock_read_parquet.assert_called_once_with(cache_file)
        # Should fetch full requested range (API end date needs buffer)
        mock_fetch_yfinance.assert_called_once_with(ticker='CSCO', interval='1d', start_date='2023-02-01',
                                                    end_date='2023-02-06', period=None)
        self.assertFalse(data_info['parquet_cache_used'])
        expected_slice = mock_df_api.loc[args.start:args.end]
        pd.testing.assert_frame_equal(data_info['ohlcv_df'], expected_slice)
        self.mock_to_parquet.assert_called_once_with(cache_file, index=True, engine='pyarrow')
        self.assertEqual(data_info['api_calls'], 1)
        self.assertEqual(data_info['rows_fetched'], len(mock_df_api))

    # --- Test CSV Mode ---
    # fetch_csv_data is mocked in setUp
    def test_csv_mode_calls_fetch_csv(self):
        """Test CSV: Correctly calls fetch_csv_data."""
        csv_path = "/fake/path/data.csv"
        args = create_mock_args(mode='csv', csv_file=csv_path)
        mock_df_csv = create_sample_df('2023-03-01', '2023-03-05', freq='D')
        # Configure mock fetch_csv_data to return only DataFrame
        self.mock_fetch_csv.return_value = mock_df_csv.copy()

        # Mock Path stat and exists for the CSV file itself
        with patch.object(Path, 'exists') as mock_path_obj_exists, \
                patch.object(Path, 'stat') as mock_path_obj_stat:
            # Ensure the mock applies to the specific Path(csv_path) call
            def exists_side_effect(p): return str(p) == csv_path

            def stat_side_effect(p):
                if str(p) == csv_path:
                    mock_stat_result = MagicMock()
                    mock_stat_result.st_size = 512
                    return mock_stat_result
                raise FileNotFoundError  # Should not happen if exists returns True

            mock_path_obj_exists.side_effect = exists_side_effect
            mock_path_obj_stat.side_effect = stat_side_effect

            data_info = acquire_data(args)

        self.mock_fetch_csv.assert_called_once()
        call_args, call_kwargs = self.mock_fetch_csv.call_args
        self.assertEqual(call_kwargs.get('file_path'), csv_path)
        # Check the default mappings passed by data_acquisition
        self.assertEqual(call_kwargs.get('ohlc_columns'), {
            'Open': 'Open,', 'High': 'High,', 'Low': 'Low,',
            'Close': 'Close,', 'Volume': 'TickVolume,'
        })
        self.assertEqual(call_kwargs.get('datetime_column'), 'DateTime,')
        self.assertEqual(call_kwargs.get('skiprows'), 1)
        # Check result
        self.assertEqual(data_info['effective_mode'], 'csv')
        self.assertIsNone(data_info['error_message'])
        pd.testing.assert_frame_equal(data_info['ohlcv_df'], mock_df_csv)
        self.assertEqual(data_info['file_size_bytes'], 512)  # Now checked via mock Path
        self.assertEqual(data_info['data_source_label'], csv_path)

    # --- Test Demo Mode ---
    @patch('src.data.data_acquisition.get_demo_data')
    def test_demo_mode_calls_get_demo(self, mock_get_demo):
        """Test DEMO: Correctly calls get_demo_data."""
        args = create_mock_args(mode='demo')
        mock_df_demo = create_sample_df('2023-04-01', '2023-04-03', freq='D')
        mock_get_demo.return_value = mock_df_demo.copy()

        data_info = acquire_data(args)

        mock_get_demo.assert_called_once()
        self.assertEqual(data_info['effective_mode'], 'demo')
        self.assertIsNone(data_info['error_message'])
        pd.testing.assert_frame_equal(data_info['ohlcv_df'], mock_df_demo)
        self.assertEqual(data_info['data_source_label'], "Demo Data")


# Allow running tests directly
if __name__ == '__main__':
    unittest.main()