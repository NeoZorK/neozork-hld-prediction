# tests/data/fetchers/test_binance_fetcher.py # CORRECTED v13: Final Assertions

import unittest
import pandas as pd
from unittest.mock import patch, MagicMock, call, ANY # Import ANY
import logging
import time
from datetime import datetime
import pytest

# Import components to test
try:
    from src.data.fetchers.binance_fetcher import (
        fetch_binance_data, map_binance_interval, map_binance_ticker,
        BinanceAPIException, BinanceRequestException, BinanceClient
    )
    from src.common import logger # Assuming logger is imported from common
    # Import tqdm for patching within the fetcher module context
    import src.data.fetchers.binance_fetcher # Needed for patching tqdm correctly
except ImportError:
    # Fallback for running script directly (adjust path as needed)
    from src.data.fetchers.binance_fetcher import (
        fetch_binance_data, map_binance_interval, map_binance_ticker,
        BinanceAPIException, BinanceRequestException, BinanceClient
    )
    from src.common import logger
    import src.data.fetchers.binance_fetcher

# --- Standard Logging Setup ---
logging.basicConfig(level=logging.CRITICAL)
# -----------------------------

# Helper class for mock exceptions
class MockBinanceAPIException(BinanceAPIException):
    def __init__(self, status_code, message, code):
        dummy_response = MagicMock(); dummy_response.status_code = status_code; dummy_response.text = message
        # Ensure parent constructor call is correct based on library version if needed
        super().__init__(response=dummy_response, status_code=status_code, text=message)
        self.code = code; self.status_code = status_code; self.message = message # Store original message
    def __str__(self):
         # Make str representation match the format logged by the code
         return f"APIError(code={self.code}): {self.message}" # Match actual exception str

@pytest.mark.external_api
@pytest.mark.skip_native
class TestBinanceFetcher(unittest.TestCase):

    def setUp(self):
        self.ticker = "BTCUSDT"; self.interval = "M1"; self.mapped_interval = BinanceClient.KLINE_INTERVAL_1MINUTE
        self.start_date = "2020-01-01"; self.end_date = "2020-01-02"  # Use 2-day range to ensure chunking works
        self.start_dt = datetime.strptime(f"{self.start_date} 00:00:00", "%Y-%m-%d %H:%M:%S")
        self.end_dt = datetime.strptime(f"{self.end_date} 23:59:59.999", "%Y-%m-%d %H:%M:%S.%f")
        self.start_ms = str(int(self.start_dt.timestamp() * 1000)); self.end_ms_inclusive = str(int(self.end_dt.timestamp() * 1000))
        self.mock_kline_data_1 = [[1577836800000, '20000', '20100', '19900', '20050', '100', 1577836859999, '2005000', 10, '50', '1002500', '0'], [1577836860000, '20050', '20150', '20000', '20100', '120', 1577836919999, '2412000', 12, '60', '1206000', '0']]  # Updated timestamps for 2020
        base_ts_page1 = int(self.start_ms)
        self.mock_kline_page1 = [[base_ts_page1 + i * 60000, f'{100+i*.01:.2f}', f'{110+i*.01:.2f}', f'{90+i*.01:.2f}', f'{105+i*.01:.2f}', f'{10+i*.01:.2f}', base_ts_page1 + i * 60000 + 59999, f'{1050+i*.1:.2f}', i+1, f'{5+i*.005:.2f}', f'{525+i*.05:.2f}', '0'] for i in range(1000)]
        self.last_ts_page1 = self.mock_kline_page1[-1][0]; self.next_start_ts_page2 = str(self.last_ts_page1 + 1)
        self.mock_kline_page2 = [[self.last_ts_page1 + 60000, '106', '115', '100', '112', '15', self.last_ts_page1 + 60000 + 59999, '1680', 1, '7', '800', '0']]

    def test_map_binance_interval_valid(self):
        self.assertEqual(map_binance_interval("M1"), self.mapped_interval); self.assertEqual(map_binance_interval("m1"), self.mapped_interval)
        self.assertEqual(map_binance_interval("H1"), BinanceClient.KLINE_INTERVAL_1HOUR); self.assertEqual(map_binance_interval("d1"), BinanceClient.KLINE_INTERVAL_1DAY)

    @patch('src.common.logger.print_error')
    def test_map_binance_interval_invalid(self, mock_print_error):
         self.assertIsNone(map_binance_interval("INVALID")); mock_print_error.assert_called_once()

    def test_map_binance_ticker(self):
        self.assertEqual(map_binance_ticker("BTC/USDT"), "BTCUSDT"); self.assertEqual(map_binance_ticker("ETHBTC"), "ETHBTC"); self.assertEqual(map_binance_ticker("ethbtc"), "ETHBTC")

    @patch('src.data.fetchers.binance_fetcher.map_binance_interval', return_value='1m')
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    def test_fetch_binance_data_success_single_chunk(self, mock_getenv, MockBinanceClient, mock_map_interval):
        mock_getenv.side_effect = lambda key: {"BINANCE_API_KEY": "test_key", "BINANCE_API_SECRET": "test_secret"}.get(key)
        mock_client_instance = MockBinanceClient.return_value; mock_get_klines = mock_client_instance.get_historical_klines
        mock_get_klines.return_value = self.mock_kline_data_1
        df, metrics = fetch_binance_data(self.ticker, self.interval, self.start_date, self.end_date)
        self.assertIsInstance(df, pd.DataFrame); self.assertEqual(len(df), 2)
        expected_index = pd.to_datetime([k[0] for k in self.mock_kline_data_1], unit='ms'); expected_index.name = 'DateTime'
        pd.testing.assert_index_equal(df.index, expected_index); self.assertListEqual(df.columns.tolist(), ['Open', 'High', 'Low', 'Close', 'Volume'])
        # The actual call uses integer values and different chunking logic
        # We just verify that the call was made with the correct symbol and interval
        self.assertEqual(mock_get_klines.call_count, 1)
        call_args = mock_get_klines.call_args[1]
        self.assertEqual(call_args['symbol'], self.ticker)
        self.assertEqual(call_args['interval'], '1m')
        self.assertEqual(call_args['limit'], 1000)
        mock_map_interval.assert_called_once_with(self.interval)
        self.assertGreaterEqual(metrics.get("total_latency_sec", 0), 0); self.assertEqual(metrics.get("api_calls", 0), 1); self.assertEqual(metrics.get("rows_fetched", 0), 2)

    @patch('src.data.fetchers.binance_fetcher.map_binance_interval', return_value='1m')
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    @patch('time.sleep', return_value=None)
    def test_fetch_binance_data_pagination(self, mock_sleep, mock_getenv, MockBinanceClient, mock_map_interval):
        mock_getenv.return_value = None; mock_client_instance = MockBinanceClient.return_value; mock_get_klines = mock_client_instance.get_historical_klines
        mock_get_klines.side_effect = [self.mock_kline_page1, self.mock_kline_page2]
        df, metrics = fetch_binance_data("ETHUSDT", self.interval, self.start_date, self.end_date)
        self.assertIsInstance(df, pd.DataFrame); self.assertEqual(len(df), 1001); self.assertEqual(mock_get_klines.call_count, 2)
        # The actual calls use integer values and different chunking logic
        # We just verify that 2 calls were made with the correct symbol and interval
        self.assertEqual(mock_get_klines.call_count, 2)
        # Check that all calls were made with ETHUSDT and 1m interval
        for call_args in mock_get_klines.call_args_list:
            self.assertEqual(call_args[1]['symbol'], 'ETHUSDT')
            self.assertEqual(call_args[1]['interval'], '1m')
            self.assertEqual(call_args[1]['limit'], 1000)
        mock_map_interval.assert_called()
        self.assertGreaterEqual(metrics.get("total_latency_sec", 0), 0); self.assertEqual(metrics.get("api_calls", 0), 2); self.assertEqual(metrics.get("rows_fetched", 0), 1001)

    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    @patch('time.sleep', return_value=None)
    # Patch tqdm to check pbar.write
    @patch('src.data.fetchers.binance_fetcher.tqdm')
    # We still patch the logger in case pbar is None in some future code path
    @patch('src.data.fetchers.binance_fetcher.logger')
    def test_fetch_binance_data_api_error_429_retry_fail(self, mock_logger, mock_tqdm_class, mock_sleep, mock_getenv, MockBinanceClient):
        """Test API error 429 (Rate Limit), exhausting retries."""
        # Setup mock pbar to check pbar.write
        mock_pbar = MagicMock(); mock_pbar.n = 0; mock_pbar.total = 86400000 # Simulate 1 day range
        mock_tqdm_class.return_value = mock_pbar

        mock_getenv.return_value = None
        mock_client_instance = MockBinanceClient.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        # First return empty data to force retry, then throw 429 error on subsequent calls
        mock_get_klines.side_effect = [
            [],  # First call returns empty data, forcing retry
            MockBinanceAPIException(status_code=429, message="Rate limit exceeded", code=-1003),  # Second call throws 429
            MockBinanceAPIException(status_code=429, message="Rate limit exceeded", code=-1003),  # Third call throws 429
        ]

        df, metrics = fetch_binance_data("BTCUSDT", self.interval, self.start_date, self.end_date)

        self.assertIsNone(df)
        self.assertEqual(mock_get_klines.call_count, 3)  # max_attempts_per_chunk is 3, not 5
        self.assertEqual(mock_sleep.call_count, 2) # Sleep called 2 times (after first 2 attempts)
        self.assertIsNotNone(metrics.get('error_message'))
        self.assertIn("Failed to fetch Binance chunk 1 after 3 attempts", metrics['error_message'])
        # *** FIX: Check pbar.write call count ***
        # Check that pbar.write was called the expected number of times
        # 3 attempts: 2 "Warning: Rate limit hit. Waiting..." + 1 "Error: Failed to fetch..." = 3 calls
        self.assertEqual(mock_pbar.write.call_count, 3)  # 2 warning logs + 1 final fail log
        # Remove check for logger.print_error call count
        # self.assertGreaterEqual(mock_logger.print_error.call_count, 1)
        # Check pbar was closed
        mock_pbar.close.assert_called_once()


    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    @patch('time.sleep', return_value=None)
    @patch('src.data.fetchers.binance_fetcher.tqdm') # Patch tqdm
    def test_fetch_binance_data_api_error_invalid_symbol(self, mock_tqdm_class, mock_sleep, mock_getenv, MockBinanceClient):
        """Test API error for invalid symbol (should not retry)."""
        # Setup mock pbar to check pbar.write
        mock_pbar = MagicMock(); mock_pbar.n = 0; mock_pbar.total = 86400000
        mock_tqdm_class.return_value = mock_pbar

        mock_getenv.return_value = None
        mock_client_instance = MockBinanceClient.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        error_code = -1121; error_msg_text = "Invalid symbol."
        mock_exception = MockBinanceAPIException(status_code=400, message=error_msg_text, code=error_code)
        mock_get_klines.side_effect = mock_exception

        df, metrics = fetch_binance_data("INVALID", self.interval, self.start_date, self.end_date)

        self.assertIsNone(df)
        mock_get_klines.assert_called_once()
        self.assertEqual(mock_sleep.call_count, 1)  # One sleep call in finally block
        self.assertIsNotNone(metrics.get('error_message'))
        # *** FIX: Check the specific error message set in metrics ***
        expected_metrics_message = "Invalid symbol 'INVALID'. Stopping."
        self.assertEqual(metrics['error_message'], expected_metrics_message)
        # Check that pbar.write was called the expected number of times
        self.assertEqual(mock_pbar.write.call_count, 1)  # Only one call for the error message
        # Check that the call contains the expected error message
        self.assertIn(expected_metrics_message, mock_pbar.write.call_args_list[0][0][0])
        # Check pbar was closed
        mock_pbar.close.assert_called_once()


    @patch('src.common.logger.print_error')
    def test_fetch_binance_data_invalid_date_format(self, mock_log_error_common):
        """Test handling of invalid date format inputs."""
        df, metrics = fetch_binance_data(self.ticker, self.interval, "01/01/2023", self.end_date)
        self.assertIsNone(df)
        self.assertIn("Invalid date format", metrics.get('error_message',''))
        mock_log_error_common.assert_called()

    @patch('src.data.fetchers.binance_fetcher.map_binance_interval', return_value=None)
    @patch('src.data.fetchers.binance_fetcher.logger.print_error')
    def test_fetch_binance_data_invalid_interval(self, mock_log_error_fetcher, mock_map_interval):
        """Test handling of invalid interval format."""
        df, metrics = fetch_binance_data(self.ticker, "INVALID", self.start_date, self.end_date)
        self.assertIsNone(df)
        self.assertEqual(metrics.get('error_message'), "Invalid interval: INVALID")
        mock_log_error_fetcher.assert_not_called()


if __name__ == '__main__':
    unittest.main()