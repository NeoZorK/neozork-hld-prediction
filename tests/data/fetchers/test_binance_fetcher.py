# tests/data/fetchers/test_binance_fetcher.py (CORRECTED V4 - Mock Exception Base + Interval Assert + TZ Assert + Index Name)

import unittest
import pandas as pd
from unittest.mock import patch, MagicMock, call
import logging
import time

# Import components to test
from src.data.fetchers.binance_fetcher import (
    fetch_binance_data, map_binance_interval, map_binance_ticker,
    BinanceAPIException, BinanceRequestException, BinanceClient
)

# --- Standard Logging Setup ---
logging.basicConfig(level=logging.CRITICAL)
# -----------------------------

# Helper class for mock exceptions - CORRECTED V3: Inherit Exception, call super with message
class MockBinanceAPIException(Exception): # Inherit directly from Exception
    def __init__(self, status_code, message, code):
        super().__init__(message) # Call base Exception init with the message
        # Set attributes needed by the fetcher logic
        self.status_code = status_code
        self.message = message
        self.code = code

    # Override __str__ if needed
    def __str__(self):
         # Provide a string representation similar to the original if needed,
         # but inheriting from Exception might be sufficient.
         return f"Mock Binance Error: Status={self.status_code}, Text='{self.message}', Code={self.code}"


class TestBinanceFetcher(unittest.TestCase):

    def setUp(self):
        """Set up basic parameters used across tests."""
        self.ticker = "BTCUSDT"
        self.interval = "M1"
        # IMPORTANT: Use the actual constant value for comparison with mock calls
        self.mapped_interval = BinanceClient.KLINE_INTERVAL_1MINUTE
        self.start_date = "2023-01-01"
        self.end_date = "2023-01-01"
        self.start_ms = "1672524000000"
        self.end_ms_inclusive = "1672610399999"

        # Mock kline data
        # OpenTime, O, H, L, C, V, CloseTime, QuoteAssetVol, Trades, TakerBaseVol, TakerQuoteVol, Ignore
        self.mock_kline_data_1 = [
            [1672531200000, '20000', '20100', '19900', '20050', '100', 1672531259999, '2005000', 10, '50', '1002500', '0'],
            [1672531260000, '20050', '20150', '20000', '20100', '120', 1672531319999, '2412000', 12, '60', '1206000', '0'],
        ]
        # Mock kline data for pagination test
        self.mock_kline_page1 = [[i * 60000 + 1672524000000, '100', '110', '90', '105', '10', (i * 60000 + 1672524000000)+59999, '1050', 1, '5', '525', '0'] for i in range(1000)]
        self.last_ts_page1 = self.mock_kline_page1[-1][0]
        self.next_start_ts_page2 = str(self.last_ts_page1 + 1)
        self.mock_kline_page2 = [[self.last_ts_page1 + 60000, '106', '115', '100', '112', '15', (self.last_ts_page1 + 60000)+59999, '1680', 1, '7', '800', '0']]

    # --- Test map_binance_interval --- (Unchanged)
    def test_map_binance_interval_valid(self):
        self.assertEqual(map_binance_interval("M1"), BinanceClient.KLINE_INTERVAL_1MINUTE)
        # ... other valid mappings ...
        self.assertEqual(map_binance_interval("1d"), "1d")

    @patch('src.common.logger.print_error')
    def test_map_binance_interval_invalid(self, mock_print_error):
        self.assertIsNone(map_binance_interval("INVALID"))
        # ... assert error logged ...

    # --- Test map_binance_ticker --- (Unchanged)
    def test_map_binance_ticker(self):
        self.assertEqual(map_binance_ticker("BTC/USDT"), "BTCUSDT")
        # ... other mappings ...

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

        # CORRECTED V2: Expected index TZ-naive and named 'DateTime'
        expected_index = pd.to_datetime([1672531200000, 1672531260000], unit='ms')
        expected_index.name = 'DateTime'
        pd.testing.assert_index_equal(df.index, expected_index)

        # CORRECTED V3: Assert call uses the mapped interval *value*
        mock_get_klines.assert_called_once_with(
            symbol=self.ticker,
            interval=self.mapped_interval, # Expect the mapped value
            start_str=self.start_ms,
            end_str=self.end_ms_inclusive,
            limit=1000
        )
        self.assertGreaterEqual(metrics.get("total_latency_sec", 0), 0)

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

        # CORRECTED V3: Check calls used the mapped interval *value*
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
        # Use the CORRECTED V3 Mock Exception
        mock_get_klines.side_effect = MockBinanceAPIException(status_code=429, message="Rate limit exceeded", code=-1003)

        with patch('src.common.logger.print_error') as mock_log_error, \
             patch('src.common.logger.print_warning') as mock_log_warning:
            df, metrics = fetch_binance_data("ADAUSDT", self.interval, self.start_date, self.end_date)

            self.assertIsNone(df)
            # Call count should be 5 now with correct exception handling
            self.assertEqual(mock_get_klines.call_count, 5) # 1 initial + 4 retries
            mock_sleep.assert_called()
            self.assertTrue(any("Rate limit likely hit" in call_args[0][0] for call_args in mock_log_warning.call_args_list))
            self.assertTrue(any(f"Failed to fetch Binance chunk starting {datetime.fromtimestamp(int(self.start_ms) / 1000)} after 5 attempts" in call_args[0][0]
                                for call_args in mock_log_error.call_args_list), "Final failure log message not found")
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
        # Use the CORRECTED V3 Mock Exception
        mock_get_klines.side_effect = MockBinanceAPIException(status_code=400, message="Invalid symbol.", code=-1121)

        with patch('src.common.logger.print_error') as mock_log_error:
            df, metrics = fetch_binance_data("INVALID", self.interval, self.start_date, self.end_date)

            self.assertIsNone(df)
            mock_get_klines.assert_called_once()
            mock_sleep.assert_not_called()
            # Check the specific log message for invalid symbol
            self.assertTrue(any("Invalid symbol 'INVALID' reported by Binance API" in call_args[0][0]
                                for call_args in mock_log_error.call_args_list), "Invalid symbol log message not found")


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