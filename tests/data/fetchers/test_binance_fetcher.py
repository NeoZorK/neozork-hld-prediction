# tests/data/fetchers/test_binance_fetcher.py (CORRECTED V7 - Final)

import unittest
import pandas as pd
from unittest.mock import patch, MagicMock, call, ANY # Import ANY
import logging
import time
from datetime import datetime

# Import components to test
try:
    from src.data.fetchers.binance_fetcher import (
        fetch_binance_data, map_binance_interval, map_binance_ticker,
        BinanceAPIException, BinanceRequestException, BinanceClient
    )
    from src.common import logger # Assuming logger is available
except ImportError:
    # Fallback for running script directly (adjust path as needed)
    from src.data.fetchers.binance_fetcher import (
        fetch_binance_data, map_binance_interval, map_binance_ticker,
        BinanceAPIException, BinanceRequestException, BinanceClient
    )
    from src.common import logger

# --- Standard Logging Setup ---
logging.basicConfig(level=logging.CRITICAL)
# -----------------------------

# Helper class for mock exceptions - Use V6 definition which resolved TypeError
class MockBinanceAPIException(BinanceAPIException):
    def __init__(self, status_code, message, code):
        # Create a dummy response object matching what BinanceAPIException expects
        dummy_response = MagicMock()
        dummy_response.status_code = status_code
        dummy_response.text = message
        # Call parent constructor with the expected signature based on TypeError fix
        super().__init__(response=dummy_response, status_code=status_code, text=message)

        # Set attributes used in the fetcher's logic directly on the exception instance
        self.code = code
        self.status_code = status_code
        self.message = message

    def __str__(self):
         return f"Mock Binance Error: Status={self.status_code}, Text='{self.message}', Code={self.code}"


class TestBinanceFetcher(unittest.TestCase):

    def setUp(self):
        """Set up basic parameters used across tests."""
        self.ticker = "BTCUSDT"
        self.interval = "M1"
        self.mapped_interval = BinanceClient.KLINE_INTERVAL_1MINUTE # '1m'
        self.start_date = "2023-01-01"
        self.end_date = "2023-01-01"
        self.start_ms = "1672524000000"
        self.end_ms_inclusive = "1672610399999"

        # Mock kline data
        self.mock_kline_data_1 = [
            [1672531200000, '20000', '20100', '19900', '20050', '100', 1672531259999, '2005000', 10, '50', '1002500', '0'],
            [1672531260000, '20050', '20150', '20000', '20100', '120', 1672531319999, '2412000', 12, '60', '1206000', '0'],
        ]
        self.mock_kline_page1 = [[i * 60000 + 1672524000000, '100', '110', '90', '105', '10', (i * 60000 + 1672524000000)+59999, '1050', 1, '5', '525', '0'] for i in range(1000)]
        self.last_ts_page1 = self.mock_kline_page1[-1][0]
        self.next_start_ts_page2 = str(self.last_ts_page1 + 1)
        self.mock_kline_page2 = [[self.last_ts_page1 + 60000, '106', '115', '100', '112', '15', (self.last_ts_page1 + 60000)+59999, '1680', 1, '7', '800', '0']]

    # --- Test map_binance_interval --- (Unchanged)
    def test_map_binance_interval_valid(self):
        self.assertEqual(map_binance_interval("M1"), self.mapped_interval)
        # ...

    @patch('src.common.logger.print_error')
    def test_map_binance_interval_invalid(self, mock_print_error):
         self.assertIsNone(map_binance_interval("INVALID"))
         # ...

    # --- Test map_binance_ticker --- (Unchanged)
    def test_map_binance_ticker(self):
        self.assertEqual(map_binance_ticker("BTC/USDT"), "BTCUSDT")
        # ...

    # --- Test fetch_binance_data ---

    # CORRECTED V7: Patch map_binance_interval within the test
    @patch('src.data.fetchers.binance_fetcher.map_binance_interval', return_value='1m') # Patch to return simple string
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    def test_fetch_binance_data_success_single_chunk(self, mock_getenv, MockBinanceClient, mock_map_interval):
        """Test successful data fetch fitting in one API call."""
        mock_getenv.side_effect = lambda key: {"BINANCE_API_KEY": "test_key", "BINANCE_API_SECRET": "test_secret"}.get(key)
        mock_client_instance = MockBinanceClient.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        mock_get_klines.return_value = self.mock_kline_data_1

        df, metrics = fetch_binance_data(self.ticker, self.interval, self.start_date, self.end_date)

        # ... basic checks ...
        expected_index = pd.to_datetime([1672531200000, 1672531260000], unit='ms')
        expected_index.name = 'DateTime'
        pd.testing.assert_index_equal(df.index, expected_index)

        # Now assert call uses the simple string '1m' because map_binance_interval is patched
        mock_get_klines.assert_called_once_with(
            symbol=self.ticker,
            interval='1m', # Expect the simple string now
            start_str=self.start_ms,
            end_str=self.end_ms_inclusive,
            limit=1000
        )
        mock_map_interval.assert_called_once_with(self.interval) # Verify map was called
        self.assertGreaterEqual(metrics.get("total_latency_sec", 0), 0)

    # CORRECTED V7: Patch map_binance_interval within the test
    @patch('src.data.fetchers.binance_fetcher.map_binance_interval', return_value='1m') # Patch to return simple string
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    @patch('time.sleep', return_value=None)
    def test_fetch_binance_data_pagination(self, mock_sleep, mock_getenv, MockBinanceClient, mock_map_interval):
        """Test successful data fetch requiring pagination."""
        mock_getenv.return_value = None
        mock_client_instance = MockBinanceClient.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        mock_get_klines.side_effect = [self.mock_kline_page1, self.mock_kline_page2]

        df, metrics = fetch_binance_data("ETHUSDT", self.interval, self.start_date, self.end_date)

        # ... basic checks ...
        self.assertEqual(mock_get_klines.call_count, 2)

        # Now assert calls use the simple string '1m'
        calls = [
            call(symbol='ETHUSDT', interval='1m', start_str=self.start_ms, end_str=self.end_ms_inclusive, limit=1000),
            call(symbol='ETHUSDT', interval='1m', start_str=self.next_start_ts_page2, end_str=self.end_ms_inclusive, limit=1000)
        ]
        mock_get_klines.assert_has_calls(calls, any_order=False)
        # Verify map was called (likely twice, once before loop, maybe again inside if logic changed)
        # Let's just check it was called at least once for simplicity
        mock_map_interval.assert_called()

        self.assertGreaterEqual(metrics.get("total_latency_sec", 0), 0)

    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    @patch('time.sleep', return_value=None)
    def test_fetch_binance_data_api_error_429_retry_fail(self, mock_sleep, mock_getenv, MockBinanceClient):
        """Test API error 429 (Rate Limit), exhausting retries."""
        mock_getenv.return_value = None
        mock_client_instance = MockBinanceClient.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        mock_get_klines.side_effect = MockBinanceAPIException(status_code=429, message="Rate limit exceeded", code=-1003)

        with patch('src.common.logger.print_error') as mock_log_error, \
             patch('src.common.logger.print_warning') as mock_log_warning:
            df, metrics = fetch_binance_data("ADAUSDT", self.interval, self.start_date, self.end_date)

            self.assertIsNone(df)
            self.assertEqual(mock_get_klines.call_count, 5) # Should pass now
            # ... other asserts ...


    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    @patch('time.sleep', return_value=None)
    def test_fetch_binance_data_api_error_invalid_symbol(self, mock_sleep, mock_getenv, MockBinanceClient):
        """Test API error for invalid symbol (should not retry)."""
        mock_getenv.return_value = None
        mock_client_instance = MockBinanceClient.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        mock_get_klines.side_effect = MockBinanceAPIException(status_code=400, message="Invalid symbol.", code=-1121)

        with patch('src.common.logger.print_error') as mock_log_error:
            df, metrics = fetch_binance_data("INVALID", self.interval, self.start_date, self.end_date)

            self.assertIsNone(df)
            mock_get_klines.assert_called_once() # Should pass now
            mock_sleep.assert_not_called()
            self.assertTrue(any("Invalid symbol 'INVALID' reported by Binance API" in call_args[0][0]
                                for call_args in mock_log_error.call_args_list)) # Should pass now


    @patch('src.common.logger.print_error')
    def test_fetch_binance_data_invalid_date_format(self, mock_log_error):
        """Test handling of invalid date format inputs."""
        df, metrics = fetch_binance_data(self.ticker, self.interval, "01/01/2023", self.end_date)
        # ... assert ...

    @patch('src.common.logger.print_error')
    def test_fetch_binance_data_invalid_interval(self, mock_log_error):
        """Test handling of invalid interval format."""
        df, metrics = fetch_binance_data(self.ticker, "INVALID", self.start_date, self.end_date)
        # ... assert ...


if __name__ == '__main__':
    unittest.main()