# tests/data/fetchers/test_binance_fetcher.py (CORRECTED - Expect MagicMock Interval)

import unittest
import pandas as pd
from unittest.mock import patch, MagicMock, call # Import call
from src.data.fetchers.binance_fetcher import fetch_binance_data, map_binance_interval, map_binance_ticker, BinanceAPIException, BinanceRequestException, BinanceClient
from src.common import logger # Assume logger setup works

# Disable logging for tests unless explicitly needed
logger.set_level(logger.logging.CRITICAL)
# logger.set_level(logger.logging.DEBUG) # Uncomment for debugging test runs

# Helper class for mock exceptions
class MockBinanceAPIException(BinanceAPIException):
    def __init__(self, status_code, message, code):
        self.status_code = status_code
        self.message = message
        self.code = code
        super().__init__(f"Mock Binance Error: Status={status_code}, Text='{message}', Code={code}")

class TestBinanceFetcher(unittest.TestCase):

    def setUp(self):
        """Set up basic parameters used across tests."""
        self.ticker = "BTCUSDT"
        self.interval = "M1"
        self.start_date = "2023-01-01"
        self.end_date = "2023-01-01"
        self.start_ms = "1672524000000" # 2023-01-01 00:00:00 UTC
        self.end_ms_inclusive = "1672610399999" # 2023-01-01 23:59:59.999 UTC

        # Standard mock kline data (OpenTime, O, H, L, C, V, CloseTime, ...)
        self.mock_kline_data_1 = [
            [1672531200000, '20000', '20100', '19900', '20050', '100', 1672531259999],
            [1672531260000, '20050', '20150', '20000', '20100', '120', 1672531319999],
        ]
        # Mock kline data for pagination test
        self.mock_kline_page1 = [[i * 60000 + 1672524000000, '100', '110', '90', '105', '10'] for i in range(1000)]
        # Ensure last timestamp is correct for next start
        self.last_ts_page1 = self.mock_kline_page1[-1][0] # 1672524000000 + 999*60000 = 1672583940000
        self.next_start_ts_page2 = str(self.last_ts_page1 + 1) # 1672583940001
        self.mock_kline_page2 = [[self.last_ts_page1 + 60000, '106', '115', '100', '112', '15']] # Single kline for page 2

    # --- Test map_binance_interval ---
    def test_map_binance_interval_valid(self):
        self.assertEqual(map_binance_interval("M1"), BinanceClient.KLINE_INTERVAL_1MINUTE)
        self.assertEqual(map_binance_interval("H4"), BinanceClient.KLINE_INTERVAL_4HOUR)
        self.assertEqual(map_binance_interval("D1"), BinanceClient.KLINE_INTERVAL_1DAY)
        self.assertEqual(map_binance_interval("W"), BinanceClient.KLINE_INTERVAL_1WEEK)
        self.assertEqual(map_binance_interval("MN"), BinanceClient.KLINE_INTERVAL_1MONTH)
        self.assertEqual(map_binance_interval("15m"), "15m") # Direct passthrough
        self.assertEqual(map_binance_interval("1d"), "1d") # Direct passthrough

    @patch('src.common.logger.print_error')
    def test_map_binance_interval_invalid(self, mock_print_error):
        self.assertIsNone(map_binance_interval("INVALID"))
        mock_print_error.assert_called_once()
        self.assertIn("Invalid Binance timeframe input: 'INVALID'", mock_print_error.call_args[0][0])

    # --- Test map_binance_ticker ---
    def test_map_binance_ticker(self):
        self.assertEqual(map_binance_ticker("BTC/USDT"), "BTCUSDT")
        self.assertEqual(map_binance_ticker("eth-usdt"), "ETHUSDT")
        self.assertEqual(map_binance_ticker("AdaUsdt"), "ADAUSDT")

    # --- Test fetch_binance_data ---

    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    def test_fetch_binance_data_success_single_chunk(self, mock_getenv, MockBinanceClient):
        """Test successful data fetch fitting in one API call."""
        # Mock environment variables
        mock_getenv.side_effect = lambda key: {"BINANCE_API_KEY": "test_key", "BINANCE_API_SECRET": "test_secret"}.get(key)

        # Mock BinanceClient instance and its method
        mock_client_instance = MockBinanceClient.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        mock_get_klines.return_value = self.mock_kline_data_1

        # Call the function
        df, metrics = fetch_binance_data(self.ticker, self.interval, self.start_date, self.end_date)

        # --- Assertions ---
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertTrue(all(col in df.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume']))
        pd.testing.assert_index_equal(df.index, pd.to_datetime([1672531200000, 1672531260000], unit='ms'))

        # ** CORRECTED: Expect MagicMock for interval **
        expected_interval = BinanceClient.KLINE_INTERVAL_1MINUTE
        mock_get_klines.assert_called_once_with(
            symbol=self.ticker,
            interval=expected_interval, # Expect the mapped interval string/constant
            start_str=self.start_ms,
            end_str=self.end_ms_inclusive,
            limit=1000
        )
        self.assertGreater(metrics.get("total_latency_sec", 0), 0) # Check latency metric

    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    @patch('time.sleep', return_value=None) # Mock time.sleep
    def test_fetch_binance_data_pagination(self, mock_sleep, mock_getenv, MockBinanceClient):
        """Test successful data fetch requiring pagination."""
        mock_getenv.return_value = None # Simulate no API keys

        mock_client_instance = MockBinanceClient.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        # Simulate pagination: first call gets 1000, second gets 1
        mock_get_klines.side_effect = [self.mock_kline_page1, self.mock_kline_page2]

        df, metrics = fetch_binance_data("ETHUSDT", "M1", self.start_date, self.end_date)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1001) # 1000 + 1
        self.assertEqual(mock_get_klines.call_count, 2)

        # ** CORRECTED: Expect MagicMock for interval **
        expected_interval = BinanceClient.KLINE_INTERVAL_1MINUTE
        calls = [
            call(symbol='ETHUSDT', interval=expected_interval, start_str=self.start_ms, end_str=self.end_ms_inclusive, limit=1000),
            call(symbol='ETHUSDT', interval=expected_interval, start_str=self.next_start_ts_page2, end_str=self.end_ms_inclusive, limit=1000)
        ]
        mock_get_klines.assert_has_calls(calls, any_order=False) # Check calls in order
        self.assertGreater(metrics.get("total_latency_sec", 0), 0)

    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    @patch('time.sleep', return_value=None) # Mock time.sleep
    def test_fetch_binance_data_api_error_429_retry_fail(self, mock_sleep, mock_getenv, MockBinanceClient):
        """Test API error 429 (Rate Limit), exhausting retries."""
        mock_getenv.return_value = None

        mock_client_instance = MockBinanceClient.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        # Simulate consistent 429 error
        mock_get_klines.side_effect = MockBinanceAPIException(status_code=429, message="Rate limit exceeded", code=-1003)

        with patch('src.common.logger.print_error') as mock_log_error, \
             patch('src.common.logger.print_warning') as mock_log_warning:
            df, metrics = fetch_binance_data("ADAUSDT", "M1", self.start_date, self.end_date)

            self.assertIsNone(df) # Should return None after failed retries
            self.assertEqual(mock_get_klines.call_count, 5) # 1 initial + 4 retries
            mock_sleep.assert_called() # time.sleep should have been called for waits
            # Check logs for warnings about rate limit and final error
            self.assertTrue(any("Rate limit likely hit" in call_args[0][0] for call_args in mock_log_warning.call_args_list))
            self.assertTrue(any("Failed to fetch Binance chunk" in call_args[0][0] for call_args in mock_log_error.call_args_list))

    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    @patch('time.sleep', return_value=None)
    def test_fetch_binance_data_api_error_invalid_symbol(self, mock_sleep, mock_getenv, MockBinanceClient):
        """Test API error for invalid symbol (should not retry)."""
        mock_getenv.return_value = None

        mock_client_instance = MockBinanceClient.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        # Simulate invalid symbol error
        mock_get_klines.side_effect = MockBinanceAPIException(status_code=400, message="Invalid symbol.", code=-1121)

        with patch('src.common.logger.print_error') as mock_log_error:
            df, metrics = fetch_binance_data("INVALID", "M1", self.start_date, self.end_date)

            self.assertIsNone(df) # Should return None immediately
            mock_get_klines.assert_called_once() # Should only be called once
            mock_sleep.assert_not_called() # No retries, no sleep
            self.assertTrue(any("Invalid symbol 'INVALID'" in call_args[0][0] for call_args in mock_log_error.call_args_list))

    @patch('src.common.logger.print_error')
    def test_fetch_binance_data_invalid_date_format(self, mock_log_error):
        """Test handling of invalid date format inputs."""
        df, metrics = fetch_binance_data(self.ticker, self.interval, "01/01/2023", self.end_date)
        self.assertIsNone(df)
        mock_log_error.assert_called()
        self.assertIn("Invalid date format", mock_log_error.call_args[0][0])

    @patch('src.common.logger.print_error')
    def test_fetch_binance_data_invalid_interval(self, mock_log_error):
        """Test handling of invalid interval format."""
        df, metrics = fetch_binance_data(self.ticker, "INVALID", self.start_date, self.end_date)
        self.assertIsNone(df)
        mock_log_error.assert_called()
        self.assertIn("Invalid Binance timeframe input", mock_log_error.call_args[0][0])

    # Add more tests: empty data return, unexpected exception during client call, etc.


if __name__ == '__main__':
    unittest.main()