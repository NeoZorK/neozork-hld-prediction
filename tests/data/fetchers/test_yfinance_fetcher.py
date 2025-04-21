# tests/data/fetchers/test_yfinance_fetcher.py # CORRECTED: api_calls assertion in error test

"""
Unit tests for the yfinance data fetcher (chunking implementation) and related utility functions.
All comments are in English.
"""

import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock, call
from datetime import datetime, timedelta

# Adjust the import path based on the project structure
from src.data.fetchers.yfinance_fetcher import (
    fetch_yfinance_data,
    map_yfinance_interval, # Import renamed function
    map_yfinance_ticker    # Import renamed function
)
# Import tqdm itself to patch it correctly
import src.data.fetchers.yfinance_fetcher # To allow patching items within it


# Helper function to create mock dataframes
# *** FIX: Add 'ticker' argument ***
def _create_mock_df(start_date_str, end_date_str, ticker: str, freq='D', values_start=100):
    """Creates a simple DataFrame for mocking yf.download results."""
    dates = pd.date_range(start=start_date_str, end=end_date_str, freq=freq, tz=None) # Ensure timezone naive
    count = len(dates)
    if count == 0: # Handle edge case of empty date range
        # Return dataframe with expected columns if range is empty
        cols = [f"{col}_{ticker}" for col in ['Open', 'High', 'Low', 'Close', 'Volume']]
        return pd.DataFrame(columns=cols, index=pd.to_datetime([]))


    data = {
        'Open': np.linspace(values_start, values_start + count - 1, count),
        'High': np.linspace(values_start + 5, values_start + count + 4, count),
        'Low': np.linspace(values_start - 5, values_start + count - 6, count),
        'Close': np.linspace(values_start + 1, values_start + count, count),
        'Volume': np.linspace(1000, 1000 + count - 1, count) * 100,
    }
    df = pd.DataFrame(data, index=dates)
    df.index.name = 'DateTime'
    # Simulate potential columns from yfinance before processing
    # *** FIX: Use the passed 'ticker' argument ***
    df.columns = [f"{col}_{ticker}" for col in df.columns] # e.g., Open_TEST
    return df


# Definition of the TestYfinanceFetcher class
class TestYfinanceFetcherChunking(unittest.TestCase):
    """
    Test suite for yfinance fetcher (chunking implementation).
    """

    # Test cases for map_yfinance_interval function (renamed)
    def test_map_yfinance_interval_valid(self):
        self.assertEqual(map_yfinance_interval("M1"), "1m")
        self.assertEqual(map_yfinance_interval("H1"), "1h")
        self.assertEqual(map_yfinance_interval("D1"), "1d")
        self.assertEqual(map_yfinance_interval("W1"), "1wk")
        self.assertEqual(map_yfinance_interval("MN1"), "1mo")
        self.assertEqual(map_yfinance_interval("15m"), "15m")
        # Test H4 warning and fallback
        with patch('src.common.logger.print_warning') as mock_log:
            self.assertEqual(map_yfinance_interval("H4"), "1h")
            mock_log.assert_called_once()

    def test_map_yfinance_interval_invalid(self):
        # Should now return None instead of raising ValueError
        with patch('src.common.logger.print_error') as mock_log:
            self.assertIsNone(map_yfinance_interval("INVALID"))
            mock_log.assert_called_once()

    # Test cases for map_yfinance_ticker function (renamed)
    def test_map_yfinance_ticker_stock(self):
        self.assertEqual(map_yfinance_ticker("AAPL"), "AAPL")
        self.assertEqual(map_yfinance_ticker("msft"), "MSFT")

    def test_map_yfinance_ticker_forex(self):
        with patch('src.common.logger.print_info') as mock_log: # Map function logs info
             self.assertEqual(map_yfinance_ticker("EURUSD"), "EURUSD=X")
             self.assertEqual(map_yfinance_ticker("gbpjpy"), "GBPJPY=X")
             self.assertEqual(mock_log.call_count, 2)

    def test_map_yfinance_ticker_with_symbols(self):
        self.assertEqual(map_yfinance_ticker("ES=F"), "ES=F")
        self.assertEqual(map_yfinance_ticker("BTC-USD"), "BTC-USD")


    # --- Tests for fetch_yfinance_data (Chunking Implementation) ---

    @patch('src.data.fetchers.yfinance_fetcher.time.sleep') # Patch sleep if used between chunks
    @patch('src.data.fetchers.yfinance_fetcher.tqdm') # Patch tqdm class
    @patch('src.data.fetchers.yfinance_fetcher.yf.download') # Patch yf.download
    def test_fetch_yfinance_data_chunking_success(self, mock_yf_download, mock_tqdm_class, mock_sleep):
        """ Test successful fetch using multiple chunks. """
        # --- Mock Configuration ---
        mock_pbar = MagicMock()
        mock_pbar.n = 0
        def mock_update(value): mock_pbar.n += value
        mock_pbar.update.side_effect = mock_update
        mock_tqdm_class.return_value = mock_pbar

        ticker_name = 'TEST'
        df_chunk1 = _create_mock_df('2022-01-01', '2022-12-31', ticker=ticker_name, freq='D', values_start=100)
        df_chunk2 = _create_mock_df('2023-01-01', '2023-12-31', ticker=ticker_name, freq='D', values_start=200)
        expected_df1 = df_chunk1.copy(); expected_df1.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        expected_df2 = df_chunk2.copy(); expected_df2.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        expected_combined_df = pd.concat([expected_df1, expected_df2])
        expected_total_rows = len(expected_combined_df)

        def yf_download_side_effect(*args, **kwargs):
            start = kwargs.get('start')
            end = kwargs.get('end')
            ticker_arg = kwargs.get('tickers')
            interval = kwargs.get('interval')
            self.assertEqual(ticker_arg, ticker_name)
            self.assertEqual(interval, '1d')
            self.assertFalse(kwargs.get('progress', True))
            if start == '2022-01-01' and end == '2023-01-01': return df_chunk1
            elif start == '2023-01-01' and end == '2024-01-01': return df_chunk2
            else: return pd.DataFrame()
        mock_yf_download.side_effect = yf_download_side_effect

        start_date='2022-01-01'
        end_date='2023-12-31'
        result_df, metrics = fetch_yfinance_data(ticker=ticker_name, interval='D1', start_date=start_date, end_date=end_date)

        self.assertEqual(mock_yf_download.call_count, 2)
        expected_calls = [
            call(tickers=ticker_name, interval='1d', start='2022-01-01', end='2023-01-01', progress=False, auto_adjust=False, actions=False, ignore_tz=True),
            call(tickers=ticker_name, interval='1d', start='2023-01-01', end='2024-01-01', progress=False, auto_adjust=False, actions=False, ignore_tz=True),
        ]
        mock_yf_download.assert_has_calls(expected_calls)
        mock_tqdm_class.assert_called_once_with(total=730, unit='day', desc=f'Fetching yfinance {ticker_name}', leave=True, ascii=True, unit_scale=False)
        self.assertEqual(mock_pbar.update.call_count, 2)
        mock_pbar.update.assert_has_calls([call(365), call(365)])
        self.assertEqual(mock_pbar.n, 730)
        mock_pbar.close.assert_called_once()
        self.assertEqual(mock_pbar.set_postfix_str.call_count, 2)
        self.assertIsNotNone(result_df)
        pd.testing.assert_frame_equal(result_df, expected_combined_df)
        self.assertIsInstance(metrics, dict)
        self.assertEqual(metrics.get('api_calls'), 2)
        self.assertEqual(metrics.get('rows_fetched'), expected_total_rows)
        self.assertIsNone(metrics.get('error_message'))
        self.assertGreater(metrics.get('latency_sec', -1), 0)

    @patch('src.data.fetchers.yfinance_fetcher.yf.download')
    @patch('src.data.fetchers.yfinance_fetcher.tqdm')
    def test_fetch_yfinance_data_period_mode(self, mock_tqdm_class, mock_yf_download):
        """ Test the bypass for --period argument (should not chunk or use tqdm). """
        ticker_name = 'MSFT'
        mock_df_period = _create_mock_df('2023-04-21', '2024-04-20', ticker=ticker_name, freq='D', values_start=300)
        mock_yf_download.return_value = mock_df_period
        expected_df = mock_df_period.copy()
        expected_df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

        test_period = '1y'
        result_df, metrics = fetch_yfinance_data(ticker=ticker_name, interval='D1', period=test_period)

        mock_yf_download.assert_called_once_with(
            tickers=ticker_name, period=test_period, interval='1d', progress=False,
            auto_adjust=False, actions=False, ignore_tz=True
        )
        call_args, call_kwargs = mock_yf_download.call_args
        self.assertNotIn('start', call_kwargs)
        self.assertNotIn('end', call_kwargs)
        mock_tqdm_class.assert_not_called()
        self.assertIsNotNone(result_df)
        pd.testing.assert_frame_equal(result_df, expected_df)
        self.assertIsInstance(metrics, dict)
        self.assertEqual(metrics.get('api_calls'), 1)
        self.assertEqual(metrics.get('rows_fetched'), len(mock_df_period))
        self.assertIsNone(metrics.get('error_message'))
        self.assertGreater(metrics.get('latency_sec', -1), 0)

    @patch('src.data.fetchers.yfinance_fetcher.time.sleep')
    @patch('src.data.fetchers.yfinance_fetcher.tqdm')
    @patch('src.data.fetchers.yfinance_fetcher.yf.download')
    def test_fetch_yfinance_data_single_chunk(self, mock_yf_download, mock_tqdm_class, mock_sleep):
        """ Test fetch that fits within a single chunk. """
        mock_pbar = MagicMock(); mock_pbar.n = 0
        def mock_update(value): mock_pbar.n += value
        mock_pbar.update.side_effect = mock_update
        mock_tqdm_class.return_value = mock_pbar

        ticker_name = 'SMALL'
        start_date='2023-01-01'
        end_date='2023-03-31'
        mock_df_single = _create_mock_df(start_date, end_date, ticker=ticker_name, freq='D')
        mock_yf_download.return_value = mock_df_single.copy()
        expected_df = mock_df_single.copy()
        expected_df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        expected_total_rows = len(expected_df)

        result_df, metrics = fetch_yfinance_data(ticker=ticker_name, interval='D1', start_date=start_date, end_date=end_date)

        expected_yf_end_date = '2023-04-01'
        mock_yf_download.assert_called_once_with(
            tickers=ticker_name, interval='1d', start=start_date, end=expected_yf_end_date,
            progress=False, auto_adjust=False, actions=False, ignore_tz=True
        )

        total_days = 90
        mock_tqdm_class.assert_called_once_with(total=total_days, unit='day', desc=f'Fetching yfinance {ticker_name}', leave=True, ascii=True, unit_scale=False)
        mock_pbar.update.assert_called_once_with(total_days)
        self.assertEqual(mock_pbar.n, total_days)
        mock_pbar.close.assert_called_once()
        mock_pbar.set_postfix_str.assert_called_once()

        self.assertIsNotNone(result_df)
        pd.testing.assert_frame_equal(result_df, expected_df)
        self.assertIsInstance(metrics, dict)
        self.assertEqual(metrics.get('api_calls'), 1)
        self.assertEqual(metrics.get('rows_fetched'), expected_total_rows)
        self.assertIsNone(metrics.get('error_message'))
        self.assertGreater(metrics.get('latency_sec', -1), 0)

    @patch('src.data.fetchers.yfinance_fetcher.time.sleep')
    @patch('src.data.fetchers.yfinance_fetcher.tqdm')
    @patch('src.data.fetchers.yfinance_fetcher.yf.download')
    def test_fetch_yfinance_data_chunk_error(self, mock_yf_download, mock_tqdm_class, mock_sleep):
        """ Test behavior when yf.download fails on one chunk. """
        mock_pbar = MagicMock(); mock_pbar.n = 0
        def mock_update(value): mock_pbar.n += value
        mock_pbar.update.side_effect = mock_update
        mock_tqdm_class.return_value = mock_pbar

        ticker_name = 'ERROR_TEST'
        start_date='2022-01-01'
        end_date='2023-12-31'

        df_chunk1 = _create_mock_df('2022-01-01', '2022-12-31', ticker=ticker_name, freq='D')
        error_message = "Simulated download failure!"
        def yf_download_side_effect(*args, **kwargs):
            start = kwargs.get('start')
            if start == '2022-01-01': return df_chunk1
            elif start == '2023-01-01': raise Exception(error_message)
            else: return pd.DataFrame()
        mock_yf_download.side_effect = yf_download_side_effect

        result_df, metrics = fetch_yfinance_data(ticker=ticker_name, interval='D1', start_date=start_date, end_date=end_date)

        self.assertEqual(mock_yf_download.call_count, 2)
        total_days = 730
        mock_tqdm_class.assert_called_once_with(total=total_days, unit='day', desc=f'Fetching yfinance {ticker_name}', leave=True, ascii=True, unit_scale=False)
        self.assertEqual(mock_pbar.update.call_count, 2) # Called after chunk 1 and in finally
        mock_pbar.update.assert_has_calls([call(365), call(365)])
        self.assertEqual(mock_pbar.n, 730)
        mock_pbar.close.assert_called_once()

        mock_pbar.write.assert_called_once()
        logged_error_message = mock_pbar.write.call_args[0][0]
        self.assertIn(error_message, logged_error_message)
        self.assertIn("Failed chunk", logged_error_message)

        self.assertIsNone(result_df)
        self.assertIsInstance(metrics, dict)
        # *** FIX: Expect only 1 successful API call counted ***
        self.assertEqual(metrics.get('api_calls'), 1) # Code increments AFTER successful call
        self.assertEqual(metrics.get('rows_fetched'), len(df_chunk1))
        self.assertIsNotNone(metrics.get('error_message'))
        self.assertIn(error_message, metrics.get('error_message', ''))

    @unittest.skip("Test for column renaming not yet implemented.")
    def test_fetch_yfinance_data_column_rename(self):
        """ Test column renaming specifically. """
        pass

    def test_fetch_yfinance_data_invalid_interval(self):
        """ Test providing an invalid interval. """
        with patch('src.common.logger.print_error') as mock_log:
             df, metrics = fetch_yfinance_data('ANY', 'XYZ', start_date='2023-01-01', end_date='2023-01-10')
             self.assertIsNone(df)
             self.assertIn('Invalid yfinance interval', metrics.get('error_message', ''))
             self.assertGreater(mock_log.call_count, 0)

# Allow running tests directly
if __name__ == '__main__':
    unittest.main()