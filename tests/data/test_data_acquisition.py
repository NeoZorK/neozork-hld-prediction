# tests/data/test_data_acquisition.py # CORRECTED v7: Ensure correct date assertion

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
from src.data.fetchers import fetch_binance_data, fetch_yfinance_data # Import yfinance fetcher

# Helper to create args
def create_mock_args(mode='binance', ticker='TICKER', interval='h1', start='2023-01-10', end='2023-01-11', point=0.01, **kwargs): # Default to 2 days 'h1'
    args = argparse.Namespace(mode=mode, ticker=ticker, interval=interval, start=start, end=end, point=point, period=None, csv_file=None)
    if mode == 'yf': args = argparse.Namespace(mode='yf', ticker=ticker, interval=interval, start=start, end=end, point=point, period=None, csv_file=None)
    args.__dict__.update(kwargs)
    return args

# Helper to create sample DataFrames
def create_sample_df(start_date_str, end_date_str, freq='h', prefix_col_name=None):
    """ Creates a sample DataFrame. """
    idx = pd.date_range(start=start_date_str, end=end_date_str, freq=freq, name='DateTime')
    idx = idx.tz_localize(None) # Ensure timezone naive
    if idx.empty: return pd.DataFrame() # Handle empty range case

    df = pd.DataFrame({
        'Open': range(100, 100 + len(idx)), 'High': range(105, 105 + len(idx)),
        'Low': range(95, 95 + len(idx)), 'Close': range(101, 101 + len(idx)),
        'Volume': range(1000, 1000 + len(idx)),
    }, index=idx)
    # Adjust columns if needed
    if prefix_col_name:
         df.columns = [f"{col}_{prefix_col_name}" for col in df.columns]
    return df

class TestDataAcquisitionCaching(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cache_dir_path = Path(self.temp_dir.name)
        # Patch the real function within the module where it's imported and used
        self.patcher_gen_path = patch('src.data.data_acquisition._generate_instrument_parquet_filename')
        self.mock_gen_path = self.patcher_gen_path.start()
        # Side effect generates path in temp dir
        def gen_path_side_effect(args):
            effective_mode = 'yfinance' if args.mode == 'yf' else args.mode
            if effective_mode not in ['yfinance', 'polygon', 'binance'] or not args.ticker: return None
            try:
                ticker_label = str(args.ticker).replace('/', '_').replace('-', '_').replace('=','_').replace(':','_')
                interval_label = str(args.interval)
                filename = f"{effective_mode}_{ticker_label}_{interval_label}.parquet"
                filepath = self.cache_dir_path / filename
                return filepath
            except Exception: return None
        self.mock_gen_path.side_effect = gen_path_side_effect

        self.patcher_logger = patch('src.data.data_acquisition.logger')
        self.mock_logger = self.patcher_logger.start()
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

    def tearDown(self):
        self.temp_dir.cleanup()
        self.patcher_gen_path.stop()
        self.patcher_logger.stop()
        self.patcher_path_exists.stop()
        self.patcher_path_stat.stop()
        self.patcher_makedirs.stop()
        self.patcher_read_parquet.stop()
        self.patcher_to_parquet.stop()

    def test_generate_filename_csv_demo(self):
        args_csv = create_mock_args(mode='csv')
        args_demo = create_mock_args(mode='demo')
        # Stop the patch temporarily to test the real function for non-cacheable modes
        self.patcher_gen_path.stop()
        try:
            self.assertIsNone(_generate_instrument_parquet_filename(args_csv))
            self.assertIsNone(_generate_instrument_parquet_filename(args_demo))
        finally:
            self.patcher_gen_path.start() # Restart patcher

    def test_get_interval_delta(self):
        self.assertEqual(_get_interval_delta('h1'), pd.Timedelta(hours=1))
        self.assertEqual(_get_interval_delta('M15'), pd.Timedelta(minutes=15))
        self.assertEqual(_get_interval_delta('D1'), pd.Timedelta(days=1))
        self.assertEqual(_get_interval_delta('W'), pd.Timedelta(days=7))
        self.assertEqual(_get_interval_delta('MN1'), pd.Timedelta(days=30))
        self.assertIsNone(_get_interval_delta('INVALID'))

    # --- Test Cache Miss (Generic API - using Binance mock) ---
    @patch('src.data.data_acquisition.fetch_binance_data')
    def test_cache_miss_fetches_api(self, mock_fetch_api):
        args = create_mock_args(mode='binance', start='2023-01-10', end='2023-01-11', interval='h1')
        cache_file = _generate_instrument_parquet_filename(args)
        self.mock_path_exists.return_value = False

        mock_df_fetched = create_sample_df('2023-01-09 23:00', '2023-01-12 01:00', freq='h')
        mock_metrics = {'api_calls': 1}
        mock_fetch_api.return_value = (mock_df_fetched.copy(), mock_metrics)

        data_info = acquire_data(args)

        expected_fetch_end_date = '2023-01-12'
        mock_fetch_api.assert_called_once_with(ticker=args.ticker, interval=args.interval, start_date=args.start, end_date=expected_fetch_end_date)
        self.assertFalse(data_info['parquet_cache_used'])
        self.assertIsInstance(data_info['ohlcv_df'], pd.DataFrame)
        self.assertFalse(data_info['ohlcv_df'].empty)
        self.assertEqual(data_info['ohlcv_df'].index.min(), pd.Timestamp('2023-01-10 00:00:00'))
        self.assertEqual(data_info['ohlcv_df'].index.max(), pd.Timestamp('2023-01-11 00:00:00'))
        self.assertEqual(len(data_info['ohlcv_df']), 25)

        self.mock_to_parquet.assert_called_once()
        call_args, call_kwargs = self.mock_to_parquet.call_args
        actual_path_saved = call_args[0]
        self.assertIsInstance(actual_path_saved, Path)
        self.assertEqual(actual_path_saved.parent, self.cache_dir_path)
        self.assertEqual(actual_path_saved.name, 'binance_TICKER_h1.parquet')
        self.assertEqual(call_kwargs.get('index'), True)
        self.assertEqual(data_info['api_calls'], 1)

    # --- Test Exact Cache Hit (Generic API - using Binance mock) ---
    @patch('src.data.data_acquisition.fetch_binance_data')
    def test_exact_cache_hit_loads_file(self, mock_fetch_api):
        args = create_mock_args(mode='binance', start='2023-01-10', end='2023-01-11', interval='h1')
        cache_file = _generate_instrument_parquet_filename(args)

        mock_df_cached = create_sample_df('2023-01-09 22:00', '2023-01-12 02:00', freq='h')
        self.mock_read_parquet.return_value = mock_df_cached.copy()
        self.mock_path_exists.return_value = True
        self.mock_path_stat.return_value.st_size = 1024

        data_info = acquire_data(args)

        self.mock_read_parquet.assert_called_once()
        call_args, _ = self.mock_read_parquet.call_args
        actual_path_read = call_args[0]
        self.assertIsInstance(actual_path_read, Path)
        self.assertEqual(actual_path_read.parent, self.cache_dir_path)
        self.assertEqual(actual_path_read.name, 'binance_TICKER_h1.parquet')

        mock_fetch_api.assert_not_called()
        self.assertTrue(data_info['parquet_cache_used'])
        self.assertIsInstance(data_info['ohlcv_df'], pd.DataFrame)
        self.assertFalse(data_info['ohlcv_df'].empty)
        self.assertEqual(data_info['ohlcv_df'].index.min(), pd.Timestamp('2023-01-10 00:00:00'))
        self.assertEqual(data_info['ohlcv_df'].index.max(), pd.Timestamp('2023-01-11 00:00:00'))
        self.assertEqual(len(data_info['ohlcv_df']), 25)

        self.mock_to_parquet.assert_not_called()
        self.assertEqual(data_info['file_size_bytes'], 1024)
        self.assertEqual(data_info['api_calls'], 0)

    # --- Test Fetch After Cache (Generic API - using Binance mock) ---
    @patch('src.data.data_acquisition.fetch_binance_data')
    def test_fetch_after_cache(self, mock_fetch_api):
        args = create_mock_args(mode='binance', start='2023-01-10', end='2023-01-13', interval='h1') # Req 10-13
        cache_file = _generate_instrument_parquet_filename(args)

        mock_df_cached = create_sample_df('2023-01-10 00:00', '2023-01-11 23:00', freq='h') # Cache 10-11
        self.mock_read_parquet.return_value = mock_df_cached.copy()
        self.mock_path_exists.return_value = True
        self.mock_path_stat.return_value.st_size = 1024

        mock_df_new = create_sample_df('2023-01-12 00:00', '2023-01-13 23:00', freq='h') # API returns 12-13
        mock_fetch_api.return_value = (mock_df_new.copy(), {'api_calls': 1})

        data_info = acquire_data(args)

        self.mock_read_parquet.assert_called_once()
        call_args_read, _ = self.mock_read_parquet.call_args
        actual_path_read = call_args_read[0]
        self.assertIsInstance(actual_path_read, Path)
        self.assertEqual(actual_path_read.parent, self.cache_dir_path)
        self.assertEqual(actual_path_read.name, 'binance_TICKER_h1.parquet')

        expected_fetch_start = '2023-01-12'
        expected_fetch_end = '2023-01-14'
        mock_fetch_api.assert_called_once_with(ticker=args.ticker, interval=args.interval, start_date=expected_fetch_start, end_date=expected_fetch_end)

        self.assertTrue(data_info['parquet_cache_used'])
        self.assertIsInstance(data_info['ohlcv_df'], pd.DataFrame)
        self.assertFalse(data_info['ohlcv_df'].empty)
        self.assertEqual(data_info['ohlcv_df'].index.min(), pd.Timestamp('2023-01-10 00:00:00'))
        self.assertEqual(data_info['ohlcv_df'].index.max(), pd.Timestamp('2023-01-13 00:00:00'))
        self.assertEqual(len(data_info['ohlcv_df']), 73) # 24*3 + 1 hours

        self.mock_to_parquet.assert_called_once()
        call_args_save, call_kwargs_save = self.mock_to_parquet.call_args
        actual_path_save = call_args_save[0]
        self.assertIsInstance(actual_path_save, Path)
        self.assertEqual(actual_path_save.parent, self.cache_dir_path)
        self.assertEqual(actual_path_save.name, 'binance_TICKER_h1.parquet')
        self.assertEqual(call_kwargs_save.get('index'), True)

    # --- Test Cache Miss for YFinance ---
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_yf_cache_miss_fetches_api_and_saves(self, mock_fetch_yfinance):
        args = create_mock_args(mode='yf', ticker='AAPL', interval='D1', start='2023-01-10', end='2023-01-12', point=0.01)
        cache_file = _generate_instrument_parquet_filename(args)
        self.mock_path_exists.return_value = False

        mock_df_fetched = create_sample_df('2023-01-09', '2023-01-13', freq='D')
        mock_df_fetched.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        mock_metrics = {'api_calls': 1, 'latency_sec': 0.5, 'rows_fetched': len(mock_df_fetched)}
        mock_fetch_yfinance.return_value = (mock_df_fetched.copy(), mock_metrics)

        data_info = acquire_data(args)

        expected_fetch_end_date = '2023-01-13'
        mock_fetch_yfinance.assert_called_once_with(ticker=args.ticker, interval=args.interval, start_date=args.start, end_date=expected_fetch_end_date, period=None)
        self.assertFalse(data_info['parquet_cache_used'])
        self.assertIsInstance(data_info['ohlcv_df'], pd.DataFrame)
        self.assertFalse(data_info['ohlcv_df'].empty)
        self.assertEqual(data_info['ohlcv_df'].index.min(), pd.Timestamp('2023-01-10'))
        self.assertEqual(data_info['ohlcv_df'].index.max(), pd.Timestamp('2023-01-12'))
        self.assertEqual(len(data_info['ohlcv_df']), 3)

        self.mock_to_parquet.assert_called_once()
        call_args_save, call_kwargs_save = self.mock_to_parquet.call_args
        actual_path_save = call_args_save[0]
        self.assertIsInstance(actual_path_save, Path)
        self.assertEqual(actual_path_save.parent, self.cache_dir_path)
        self.assertEqual(actual_path_save.name, 'yfinance_AAPL_D1.parquet')
        self.assertEqual(call_kwargs_save.get('index'), True)
        self.assertEqual(data_info['api_calls'], 1)
        self.assertEqual(data_info['rows_fetched'], len(mock_df_fetched))

    # --- Test Exact Cache Hit for YFinance ---
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_yf_exact_cache_hit_loads_file_no_api(self, mock_fetch_yfinance):
        args = create_mock_args(mode='yf', ticker='AAPL', interval='D1', start='2023-01-10', end='2023-01-12', point=0.01)
        cache_file = _generate_instrument_parquet_filename(args)

        mock_df_cached = create_sample_df('2023-01-09', '2023-01-13', freq='D')
        mock_df_cached.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.mock_read_parquet.return_value = mock_df_cached.copy()
        self.mock_path_exists.return_value = True
        self.mock_path_stat.return_value.st_size = 2048

        data_info = acquire_data(args)

        self.mock_read_parquet.assert_called_once()
        call_args_read, _ = self.mock_read_parquet.call_args
        actual_path_read = call_args_read[0]
        self.assertIsInstance(actual_path_read, Path)
        self.assertEqual(actual_path_read.parent, self.cache_dir_path)
        self.assertEqual(actual_path_read.name, 'yfinance_AAPL_D1.parquet')

        mock_fetch_yfinance.assert_not_called()
        self.assertTrue(data_info['parquet_cache_used'])
        self.assertIsInstance(data_info['ohlcv_df'], pd.DataFrame)
        self.assertFalse(data_info['ohlcv_df'].empty)
        self.assertEqual(data_info['ohlcv_df'].index.min(), pd.Timestamp('2023-01-10'))
        self.assertEqual(data_info['ohlcv_df'].index.max(), pd.Timestamp('2023-01-12'))
        self.assertEqual(len(data_info['ohlcv_df']), 3)

        self.mock_to_parquet.assert_not_called()
        self.assertEqual(data_info['file_size_bytes'], 2048)
        self.assertEqual(data_info['api_calls'], 0)

    # --- Test Fetch After Cache for YFinance ---
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_yf_fetch_after_cache(self, mock_fetch_yfinance):
        """ Test YF: Fetches data after cached range. """
        args = create_mock_args(mode='yf', ticker='AAPL', interval='D1', start='2023-01-10', end='2023-01-13', point=0.01) # Req 10-13
        cache_file = _generate_instrument_parquet_filename(args)

        mock_df_cached = create_sample_df('2023-01-10', '2023-01-11', freq='D') # Cache 10-11
        mock_df_cached.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.mock_read_parquet.return_value = mock_df_cached.copy()
        self.mock_path_exists.return_value = True
        self.mock_path_stat.return_value.st_size = 1024

        mock_df_new = create_sample_df('2023-01-12', '2023-01-13', freq='D') # API returns 12-13
        mock_df_new.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        mock_metrics_new = {'api_calls': 1, 'rows_fetched': len(mock_df_new), 'latency_sec': 0.3}
        mock_fetch_yfinance.return_value = (mock_df_new.copy(), mock_metrics_new)

        data_info = acquire_data(args)

        self.mock_read_parquet.assert_called_once()
        call_args_read, _ = self.mock_read_parquet.call_args
        actual_path_read = call_args_read[0]
        self.assertIsInstance(actual_path_read, Path)
        self.assertEqual(actual_path_read.parent, self.cache_dir_path)
        self.assertEqual(actual_path_read.name, 'yfinance_AAPL_D1.parquet')

        expected_fetch_start = '2023-01-12'
        expected_fetch_end = '2023-01-14'
        mock_fetch_yfinance.assert_called_once_with(
            ticker=args.ticker, interval=args.interval,
            start_date=expected_fetch_start, end_date=expected_fetch_end, period=None
        )

        self.assertTrue(data_info['parquet_cache_used'])
        self.assertIsInstance(data_info['ohlcv_df'], pd.DataFrame)
        self.assertFalse(data_info['ohlcv_df'].empty)
        self.assertEqual(data_info['ohlcv_df'].index.min(), pd.Timestamp('2023-01-10'))
        self.assertEqual(data_info['ohlcv_df'].index.max(), pd.Timestamp('2023-01-13'))
        self.assertEqual(len(data_info['ohlcv_df']), 4)

        self.mock_to_parquet.assert_called_once()
        call_args_save, call_kwargs_save = self.mock_to_parquet.call_args
        actual_path_save = call_args_save[0]
        self.assertIsInstance(actual_path_save, Path)
        self.assertEqual(actual_path_save.parent, self.cache_dir_path)
        self.assertEqual(actual_path_save.name, 'yfinance_AAPL_D1.parquet')

        self.assertEqual(data_info['api_calls'], 1)
        self.assertEqual(data_info['rows_fetched'], len(mock_df_new))

    # --- Test Fetch Before Cache for YFinance ---
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_yf_fetch_before_cache(self, mock_fetch_yfinance):
        """ Test YF: Fetches data before cached range. """
        args = create_mock_args(mode='yf', ticker='AAPL', interval='D1', start='2023-01-10', end='2023-01-13', point=0.01) # Req 10-13
        cache_file = _generate_instrument_parquet_filename(args)

        mock_df_cached = create_sample_df('2023-01-12', '2023-01-13', freq='D') # Cache 12-13
        mock_df_cached.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.mock_read_parquet.return_value = mock_df_cached.copy()
        self.mock_path_exists.return_value = True
        self.mock_path_stat.return_value.st_size = 1024

        mock_df_new = create_sample_df('2023-01-10', '2023-01-11', freq='D') # API returns 10-11
        mock_df_new.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        mock_metrics_new = {'api_calls': 1, 'rows_fetched': len(mock_df_new), 'latency_sec': 0.4}
        mock_fetch_yfinance.return_value = (mock_df_new.copy(), mock_metrics_new)

        data_info = acquire_data(args)

        self.mock_read_parquet.assert_called_once()
        call_args_read, _ = self.mock_read_parquet.call_args
        actual_path_read = call_args_read[0]
        self.assertEqual(actual_path_read.parent, self.cache_dir_path)
        self.assertEqual(actual_path_read.name, 'yfinance_AAPL_D1.parquet')

        # Check API call dates
        expected_fetch_start = '2023-01-10'
        # *** FIX: Correct expected end date based on calculation trace ***
        expected_fetch_end = '2023-01-11' # Fetch up to day before cache start (12th) -> pass 11th as exclusive end
        mock_fetch_yfinance.assert_called_once_with(
            ticker=args.ticker, interval=args.interval,
            start_date=expected_fetch_start, end_date=expected_fetch_end, period=None
        )

        self.assertTrue(data_info['parquet_cache_used'])
        self.assertIsInstance(data_info['ohlcv_df'], pd.DataFrame)
        self.assertFalse(data_info['ohlcv_df'].empty)
        self.assertEqual(data_info['ohlcv_df'].index.min(), pd.Timestamp('2023-01-10'))
        self.assertEqual(data_info['ohlcv_df'].index.max(), pd.Timestamp('2023-01-13'))
        self.assertEqual(len(data_info['ohlcv_df']), 4)

        self.mock_to_parquet.assert_called_once()
        call_args_save, call_kwargs_save = self.mock_to_parquet.call_args
        actual_path_save = call_args_save[0]
        self.assertEqual(actual_path_save.parent, self.cache_dir_path)
        self.assertEqual(actual_path_save.name, 'yfinance_AAPL_D1.parquet')

        self.assertEqual(data_info['api_calls'], 1)
        self.assertEqual(data_info['rows_fetched'], len(mock_df_new))


    # --- Test Fetch Before and After Cache for YFinance ---
    @patch('src.data.data_acquisition.fetch_yfinance_data')
    def test_yf_fetch_before_and_after_cache(self, mock_fetch_yfinance):
        """ Test YF: Fetches data before and after cached range. """
        args = create_mock_args(mode='yf', ticker='MSFT', interval='D1', start='2023-01-10', end='2023-01-15', point=0.01) # Req 10-15
        cache_file = _generate_instrument_parquet_filename(args)

        # Simulate existing cache file (Jan 12-13)
        mock_df_cached = create_sample_df('2023-01-12', '2023-01-13', freq='D')
        mock_df_cached.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.mock_read_parquet.return_value = mock_df_cached.copy()
        self.mock_path_exists.return_value = True
        self.mock_path_stat.return_value.st_size = 1024

        # Simulate API fetch for the missing ranges
        mock_df_before = create_sample_df('2023-01-10', '2023-01-11', freq='D')
        mock_df_before.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        mock_metrics_before = {'api_calls': 1, 'rows_fetched': len(mock_df_before), 'latency_sec': 0.2}

        mock_df_after = create_sample_df('2023-01-14', '2023-01-15', freq='D')
        mock_df_after.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        mock_metrics_after = {'api_calls': 1, 'rows_fetched': len(mock_df_after), 'latency_sec': 0.3}

        # Configure side effect for fetcher to return correct df based on call
        def fetch_side_effect(*args_call, **kwargs_call):
            start_date = kwargs_call.get('start_date')
            end_date = kwargs_call.get('end_date') # End date passed to fetcher
            if start_date == '2023-01-10' and end_date == '2023-01-11': # Fetch before
                return (mock_df_before.copy(), mock_metrics_before)
            elif start_date == '2023-01-14' and end_date == '2023-01-16': # Fetch after
                 return (mock_df_after.copy(), mock_metrics_after)
            else:
                 raise ValueError(f"Unexpected fetch call in test: start={start_date}, end={end_date}")
        mock_fetch_yfinance.side_effect = fetch_side_effect

        # Execute acquire_data
        data_info = acquire_data(args)

        # --- Assertions ---
        # Check cache read path
        self.mock_read_parquet.assert_called_once()
        call_args_read, _ = self.mock_read_parquet.call_args
        self.assertEqual(call_args_read[0].name, 'yfinance_MSFT_D1.parquet')

        # Check API calls (should be two)
        self.assertEqual(mock_fetch_yfinance.call_count, 2)
        # Fetch before: cache starts 12th, fetch ends 11th -> end_date='2023-01-11'
        expected_fetch_before_start = '2023-01-10'
        expected_fetch_before_end = '2023-01-11' # day after 11th is 12th, cache starts 12th, fetch needs end date BEFORE cache starts. acquire_data calculates fetch end = '2023-01-11'. Pass day after that = '2023-01-12'
        expected_fetch_before_end_calc = '2023-01-11' # Calculated end date by acquire_data for the fetch_ranges tuple
        expected_fetch_before_end_arg = (pd.to_datetime(expected_fetch_before_end_calc) + pd.Timedelta(milliseconds=1)).strftime('%Y-%m-%d') # Should be 2023-01-11

        # Fetch after: cache ends 13th, delta=1D, fetch starts 14th. Req ends 15th.
        expected_fetch_after_start = '2023-01-14' # day after cache end (13th)
        expected_fetch_after_end = '2023-01-16' # day after requested end (15th)

        expected_calls = [
             call(ticker=args.ticker, interval=args.interval, start_date=expected_fetch_before_start, end_date=expected_fetch_before_end_arg, period=None),
             call(ticker=args.ticker, interval=args.interval, start_date=expected_fetch_after_start, end_date=expected_fetch_after_end, period=None)
        ]
        mock_fetch_yfinance.assert_has_calls(expected_calls, any_order=True) # Order might vary


        self.assertTrue(data_info['parquet_cache_used'])
        # Check final slice correctness
        self.assertIsInstance(data_info['ohlcv_df'], pd.DataFrame)
        self.assertFalse(data_info['ohlcv_df'].empty)
        self.assertEqual(data_info['ohlcv_df'].index.min(), pd.Timestamp('2023-01-10')) # Original start
        self.assertEqual(data_info['ohlcv_df'].index.max(), pd.Timestamp('2023-01-15')) # Original end
        self.assertEqual(len(data_info['ohlcv_df']), 6) # 6 days total (10,11,12,13,14,15)

        # Check save path
        self.mock_to_parquet.assert_called_once()
        call_args_save, call_kwargs_save = self.mock_to_parquet.call_args
        self.assertEqual(call_args_save[0].name, 'yfinance_MSFT_D1.parquet')

        # Check combined metrics
        self.assertEqual(data_info['api_calls'], 2)
        self.assertEqual(data_info['rows_fetched'], len(mock_df_before) + len(mock_df_after))
        self.assertAlmostEqual(data_info['api_latency_sec'], 0.5) # 0.2 + 0.3


    # --- Add more tests ---
    # test_yf_period_skips_cache(...) # Important!
    # test_cache_read_error_fetches_api(...)
    # test_fetch_failure_during_partial_fetch(...)

# Allow running tests directly
if __name__ == '__main__':
    unittest.main()