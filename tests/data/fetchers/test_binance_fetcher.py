# tests/data/fetchers/test_binance_fetcher.py (CORRECTED - Mock Exception + Interval Assert + TZ Assert)

import unittest
import pandas as pd
from unittest.mock import patch, MagicMock, call # Import call
import logging # Import standard logging library
import time # Import time for potential use

# Import components to test
from src.data.fetchers.binance_fetcher import (
    fetch_binance_data, map_binance_interval, map_binance_ticker,
    BinanceAPIException, BinanceRequestException, BinanceClient
)

# --- Standard Logging Setup ---
logging.basicConfig(level=logging.CRITICAL)
# -----------------------------

# Helper class for mock exceptions - CORRECTED: No super call
class MockBinanceAPIException(Exception): # Inherit from base Exception is enough for testing
    def __init__(self, status_code, message, code):
        self.status_code = status_code
        self.message = message
        self.code = code
        # No super().__init__() call needed if we don't rely on parent's behavior
        # Store the message for potential checks if needed
        self.args = (f"Mock Binance Error: Status={status_code}, Text='{message}', Code={code}",)

    def __str__(self):
        return self.args[0]


class TestBinanceFetcher(unittest.TestCase):

    def setUp(self):
        """Set up basic parameters used across tests."""
        self.ticker = "BTCUSDT"
        self.interval = "M1" # User-provided interval (e.g., from args)
        self.mapped_interval = BinanceClient.KLINE_INTERVAL_1MINUTE # Expected mapped value
        self.start_date = "2023-01-01"
        self.end_date = "2023-01-01"
        # Start/End Timestamps in milliseconds UTC
        self.start_ms = "1672524000000"
        self.end_ms_inclusive = "1672610399999"

        # Mock kline data (Ensure it has enough columns for processing in fetcher)
        # OpenTime, Open, High, Low, Close, Volume, CloseTime, QuoteAssetVolume, NumberTrades, TakerBuyBaseVol, TakerBuyQuoteVol, Ignore
        self.mock_kline_data_1 = [
            [1672531200000, '20000', '20100', '19900', '20050', '100', 1672531259999, '2005000', 10, '50', '1002500', '0'],
            [1672531260000, '20050', '20150', '20000', '20100', '120', 1672531319999, '2412000', 12, '60', '1206000', '0'],
        ]
        # Mock kline data for pagination test
        self.mock_kline_page1 = [[i * 60000 + 1672524000000, '100', '110', '90', '105', '10', (i * 60000 + 1672524000000)+59999, '1050', 1, '5', '525', '0'] for i in range(1000)]
        self.last_ts_page1 = self.mock_kline_page1[-1][0]
        self.next_start_ts_page2 = str(self.last_ts_page1 + 1)
        self.mock_kline_page2 = [[self.last_ts_page1 + 60000, '106', '115', '100', '112', '15', (self.last_ts_page1 + 60000)+59999, '1680', 1, '7', '800', '0']] # Single kline for page 2

    # --- Test map_binance_interval --- (Unchanged)
    def test_map_binance_interval_valid(self):
        self.assertEqual(map_binance_interval("M1"), BinanceClient.KLINE_INTERVAL_1MINUTE)
        self.assertEqual(map_binance_interval("H4"), BinanceClient.KLINE_INTERVAL_4HOUR)
        self.assertEqual(map_binance_interval("D1"), BinanceClient.KLINE_INTERVAL_1DAY)
        self.assertEqual(map_binance_interval("W"), BinanceClient.KLINE_INTERVAL_1WEEK)
        self.assertEqual(map_binance_interval("MN"), BinanceClient.KLINE_INTERVAL_1MONTH)
        self.assertEqual(map_binance_interval("15m"), "15m")
        self.assertEqual(map_binance_interval("1d"), "1d")

    @patch('src.common.logger.print_error')
    def test_map_binance_interval_invalid(self, mock_print_error):
        self.assertIsNone(map_binance_interval("INVALID"))
        mock_print_error.assert_called_once()
        self.assertIn("Invalid Binance timeframe input: 'INVALID'", mock_print_error.call_args[0][0])

    # --- Test map_binance_ticker --- (Unchanged)
    def test_map_binance_ticker(self):
        self.assertEqual(map_binance_ticker("BTC/USDT"), "BTCUSDT")
        self.assertEqual(map_binance_ticker("eth-usdt"), "ETHUSDT")
        self.assertEqual(map_binance_ticker("AdaUsdt"), "ADAUSDT")

    # --- Test fetch_binance_data ---

    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    def test_fetch_binance_data_success_single_chunk(self, mock_getenv, MockBinanceClient):
        """Test successful data fetch fitting in one API call."""
        mock_getenv.side_effect = lambda key: {"BINANCE_API_KEY": "test_key", "BINANCE_API_SECRET": "test_secret"}.get(key)
        mock_client_instance = MockBinanceClient.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        mock_get_klines.return_value = self.mock_kline_data_1

        df, metrics = fetch_binance_data(self.ticker, self.interval, self.start_date, self.end_date)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertTrue(all(col in df.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume']))
        # CORRECTED: Expected index should be timezone-naive
        expected_index = pd.to_datetime([1672531200000, 1672531260000], unit='ms')
        pd.testing.assert_index_equal(df.index, expected_index)

        # Assert call uses the mapped interval constant/value
        mock_get_klines.assert_called_once_with(
            symbol=self.ticker,
            interval=self.mapped_interval, # Use the mapped value
            start_str=self.start_ms,
            end_str=self.end_ms_inclusive,
            limit=1000
        )
        self.assertGreaterEqual(metrics.get("total_latency_sec", 0), 0) # Use GreaterEqual as mock latency can be 0

    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    @patch('time.sleep', return_value=None)
    def test_fetch_binance_data_pagination(self, mock_sleep, mock_getenv, MockBinanceClient):
        """Test successful data fetch requiring pagination."""
        mock_getenv.return_value = None
        mock_client_instance = MockBinanceClient.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        mock_get_klines.side_effect = [self.mock_kline_page1, self.mock_kline_page2]

        df, metrics = fetch_binance_data("ETHUSDT", self.interval, self.start_date, self.end_date)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1001)
        self.assertEqual(mock_get_klines.call_count, 2)

        # CORRECTED: Check calls used the mapped interval value
        calls = [
            call(symbol='ETHUSDT', interval=self.mapped_interval, start_str=self.start_ms, end_str=self.end_ms_inclusive, limit=1000),
            call(symbol='ETHUSDT', interval=self.mapped_interval, start_str=self.next_start_ts_page2, end_str=self.end_ms_inclusive, limit=1000)
        ]
        mock_get_klines.assert_has_calls(calls, any_order=False)
        self.assertGreaterEqual(metrics.get("total_latency_sec", 0), 0)

    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    @patch('time.sleep', return_value=None)
    def test_fetch_binance_data_api_error_429_retry_fail(self, mock_sleep, mock_getenv, MockBinanceClient):
        """Test API error 429 (Rate Limit), exhausting retries."""
        mock_getenv.return_value = None
        mock_client_instance = MockBinanceClient.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        # Use the corrected Mock Exception
        mock_get_klines.side_effect = MockBinanceAPIException(status_code=429, message="Rate limit exceeded", code=-1003)

        with patch('src.common.logger.print_error') as mock_log_error, \
             patch('src.common.logger.print_warning') as mock_log_warning:
            df, metrics = fetch_binance_data("ADAUSDT", self.interval, self.start_date, self.end_date)

            self.assertIsNone(df)
            self.assertEqual(mock_get_klines.call_count, 5) # 1 initial + 4 retries
            mock_sleep.assert_called()
            self.assertTrue(any("Rate limit likely hit" in call_args[0][0] for call_args in mock_log_warning.call_args_list))
            self.assertTrue(any("Failed to fetch Binance chunk" in call_args[0][0] for call_args in mock_log_error.call_args_list))
            self.assertIsNotNone(metrics.get("error_message"))
            self.assertIn("Failed to fetch Binance chunk", metrics["error_message"])

    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    @patch('os.getenv')
    @patch('time.sleep', return_value=None)
    def test_fetch_binance_data_api_error_invalid_symbol(self, mock_sleep, mock_getenv, MockBinanceClient):
        """Test API error for invalid symbol (should not retry)."""
        mock_getenv.return_value = None
        mock_client_instance = MockBinanceClient.return_value
        mock_get_klines = mock_client_instance.get_historical_klines
        # Use the corrected Mock Exception
        mock_get_klines.side_effect = MockBinanceAPIException(status_code=400, message="Invalid symbol.", code=-1121)

        with patch('src.common.logger.print_error') as mock_log_error:
            df, metrics = fetch_binance_data("INVALID", self.interval, self.start_date, self.end_date)

            self.assertIsNone(df)
            mock_get_klines.assert_called_once()
            mock_sleep.assert_not_called()
            self.assertTrue(any("Invalid symbol 'INVALID'" in call_args[0][0] for call_args in mock_log_error.call_args_list))
            self.assertIsNotNone(metrics.get("error_message"))
            self.assertIn("Invalid symbol 'INVALID'", metrics["error_message"])

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


if __name__ == '__main__':
    unittest.main()