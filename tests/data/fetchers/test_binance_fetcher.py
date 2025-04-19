# tests/data/fetchers/test_binance_fetcher.py # CORRECTED

import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
from datetime import datetime

# Functions/classes to test or mock
from src.data.fetchers.binance_fetcher import (
    fetch_binance_data, map_binance_interval, map_binance_ticker,
    BINANCE_AVAILABLE, BinanceAPIException, BinanceRequestException # Import exceptions
)

# Dummy logger
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass
    def print_success(self, msg): pass

# Mock the BinanceClient class structure if library is available
if BINANCE_AVAILABLE:
    from binance.client import Client as BinanceClient_orig
else:
    # Define dummy for type hinting if lib not installed
     class BinanceClient_orig:
        KLINE_INTERVAL_1MINUTE = '1m'
        KLINE_INTERVAL_5MINUTE = '5m'
        KLINE_INTERVAL_15MINUTE = '15m'
        KLINE_INTERVAL_30MINUTE = '30m'
        KLINE_INTERVAL_1HOUR = '1h'
        KLINE_INTERVAL_4HOUR = '4h'
        KLINE_INTERVAL_1DAY = '1d'
        KLINE_INTERVAL_1WEEK = '1w'
        KLINE_INTERVAL_1MONTH = '1M'


@patch('src.data.fetchers.binance_fetcher.logger', new_callable=MockLogger)
@patch('src.data.fetchers.binance_fetcher.BINANCE_AVAILABLE', True) # Assume library is available
class TestBinanceFetcher(unittest.TestCase):

    # --- Tests for map_binance_interval ---
    def test_map_binance_interval_mql(self, _):
        # Use constants from the original/dummy class
        self.assertEqual(map_binance_interval("M1"), BinanceClient_orig.KLINE_INTERVAL_1MINUTE)
        self.assertEqual(map_binance_interval("H1"), BinanceClient_orig.KLINE_INTERVAL_1HOUR)
        self.assertEqual(map_binance_interval("D"), BinanceClient_orig.KLINE_INTERVAL_1DAY)
        self.assertEqual(map_binance_interval("W1"), BinanceClient_orig.KLINE_INTERVAL_1WEEK)
        self.assertEqual(map_binance_interval("MN"), BinanceClient_orig.KLINE_INTERVAL_1MONTH)

    def test_map_binance_interval_direct(self, _):
        self.assertEqual(map_binance_interval("5m"), "5m")
        self.assertEqual(map_binance_interval("1d"), "1d")

    def test_map_binance_interval_invalid(self, _):
        self.assertIsNone(map_binance_interval("1s"))
        self.assertIsNone(map_binance_interval("invalid"))


    # --- Tests for map_binance_ticker ---
    def test_map_binance_ticker(self, _):
        self.assertEqual(map_binance_ticker("BTC/USDT"), "BTCUSDT")
        self.assertEqual(map_binance_ticker("eth-usd"), "ETHUSD")
        self.assertEqual(map_binance_ticker("xrpusd"), "XRPUSD")
        self.assertEqual(map_binance_ticker("SOLUSDT"), "SOLUSDT") # No change


    # --- Tests for fetch_binance_data ---
    @patch('src.data.fetchers.binance_fetcher.os.getenv')
    @patch('src.data.fetchers.binance_fetcher.BinanceClient') # Patch the client import
    def test_fetch_binance_data_success_single_chunk(self, MockBinanceClient, mock_getenv, __):
        # Setup mocks
        mock_getenv.side_effect = lambda k: "fake_key" if k == "BINANCE_API_KEY" else "fake_secret" # Return keys
        mock_client_instance = MockBinanceClient.return_value

        # Simulate API returning data (Binance format: list of lists)
        # [ Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore ]
        kline1 = [1672531200000, '40000', '40100', '39900', '40050', '100', 1672531259999, '4005000', 50, '50', '2002500', '0']
        kline2 = [1672531260000, '40050', '40200', '40000', '40150', '110', 1672531319999, '4416500', 55, '60', '2409000', '0']
        mock_client_instance.get_historical_klines.return_value = [kline1, kline2]

        # Call function
        start_date = "2023-01-01"
        end_date = "2023-01-01"
        result_df = fetch_binance_data("BTCUSDT", "M1", start_date, end_date)

        # Assertions
        MockBinanceClient.assert_called_once_with(api_key="fake_key", api_secret="fake_secret")
        mock_client_instance.get_historical_klines.assert_called_once()
        # Check specific args of get_historical_klines if needed
        args_call = mock_client_instance.get_historical_klines.call_args[1] # Get keyword args
        self.assertEqual(args_call['symbol'], "BTCUSDT")
        # CORRECTED Assertion: Compare against the expected constant value
        self.assertEqual(args_call['interval'], BinanceClient_orig.KLINE_INTERVAL_1MINUTE)
        # Check start/end ms timestamps based on input dates
        # ...

        self.assertIsNotNone(result_df)
        self.assertEqual(len(result_df), 2)
        self.assertEqual(result_df.iloc[0]['Open'], 40000.0) # Check numeric conversion
        self.assertEqual(result_df.iloc[1]['Close'], 40150.0)
        self.assertListEqual(list(result_df.columns), ['Open', 'High', 'Low', 'Close', 'Volume'])

    @patch('src.data.fetchers.binance_fetcher.time.sleep') # Mock sleep for pagination test
    @patch('src.data.fetchers.binance_fetcher.os.getenv')
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    def test_fetch_binance_data_success_pagination(self, MockBinanceClient, mock_getenv, mock_sleep, __):
        # Setup mocks
        mock_getenv.return_value = None # Test without API keys
        mock_client_instance = MockBinanceClient.return_value

        # Simulate pagination: 2 chunks then empty
        kline1 = [1711929600000, '70000', '70100', '69900', '70050', '10', 1711929659999, '...', 0, '0', '0', '0'] # Apr 1 00:00
        kline2 = [1711929660000, '70050', '70200', '70000', '70150', '11', 1711929719999, '...', 0, '0', '0', '0'] # Apr 1 00:01
        kline3 = [1711929720000, '70150', '70300', '70100', '70250', '12', 1711929779999, '...', 0, '0', '0', '0'] # Apr 1 00:02

        # Simulate limit=2 case for easy testing
        # Use side_effect to return different lists on subsequent calls
        mock_client_instance.get_historical_klines.side_effect = [
            [kline1, kline2], # First call returns 2 (<= internal limit, but we set it to 2 for test)
            [kline3],       # Second call returns 1 (< internal limit)
            []              # Subsequent calls would return empty if range allows
        ]

        # Call function
        start_date = "2024-04-01"
        end_date = "2024-04-01" # Range within one day
        # REMOVED: Patching limit_per_request as it's local
        result_df = fetch_binance_data("BTCUSDT", "M1", start_date, end_date)

        # Assertions
        self.assertIsNotNone(result_df)
        self.assertEqual(len(result_df), 3) # All aggregates combined
        # The number of calls depends on the *actual* limit (1000) unless mocked differently
        # For this small dataset, it should only be called once by the real function.
        # Let's adjust side_effect to reflect getting all data in one call, then empty
        mock_client_instance.get_historical_klines.side_effect = [
             [kline1, kline2, kline3], # Assume limit > 3
             []
        ]
        result_df = fetch_binance_data("BTCUSDT", "M1", start_date, end_date)
        self.assertIsNotNone(result_df)
        self.assertEqual(len(result_df), 3)
        # It should make one call to get data, and potentially one more if the first one
        # returned exactly the limit (1000), which isn't the case here.
        # If the first call returns less than limit, loop breaks.
        # If the first call returns exactly limit, it makes another call.
        # Let's test the case where multiple calls *are* needed
        # Simulate limit=2 again for testing the loop logic
        kline4 = [1711929780000, '70250', '70350', '70200', '70300', '13', 1711929839999, '...', 0, '0', '0', '0'] # Apr 1 00:03
        mock_client_instance.get_historical_klines.side_effect = [
            [kline1, kline2], # Call 1 (limit 2)
            [kline3, kline4], # Call 2 (limit 2)
            []                # Call 3 (empty)
        ]
        with patch('src.data.fetchers.binance_fetcher.limit_per_request', 2): # Ok, patch the default value used *if* it were a global/module constant
             # Correction: limit_per_request is local, cannot patch this way easily.
             # We must rely on side_effect length to test pagination logic.
             # Revert to testing accumulation with side_effect length < actual limit.
             mock_client_instance.get_historical_klines.side_effect = [
                [kline1, kline2], # Call 1 (< 1000) -> Loop should break
                # Should not be called again
             ]
             result_df = fetch_binance_data("BTCUSDT", "M1", start_date, end_date)
             self.assertIsNotNone(result_df)
             self.assertEqual(len(result_df), 2) # Only gets first chunk
             self.assertEqual(mock_client_instance.get_historical_klines.call_count, 1) # Called only once

             # Let's rethink the test: mock return > limit to force next call
             kline_limit = [MagicMock()] * 1000 # Simulate exactly 1000 results
             kline_next = [kline3]
             mock_client_instance.reset_mock() # Reset call count etc.
             mock_client_instance.get_historical_klines.side_effect = [
                  kline_limit, # First call hits limit
                  kline_next,  # Second call gets remaining
                  []           # Third call is empty
             ]
             result_df = fetch_binance_data("BTCUSDT", "M1", start_date, end_date)
             self.assertIsNotNone(result_df)
             self.assertEqual(len(result_df), 1001) # Combined
             self.assertEqual(mock_client_instance.get_historical_klines.call_count, 3) # 3 calls needed


    @patch('src.data.fetchers.binance_fetcher.os.getenv')
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    def test_fetch_binance_data_api_error(self, MockBinanceClient, mock_getenv, __):
        mock_getenv.return_value = None
        mock_client_instance = MockBinanceClient.return_value
        # CORRECTED: Simulate API error using 'message'
        mock_client_instance.get_historical_klines.side_effect = BinanceAPIException(message="Test API Error")

        start_date = "2023-01-01"
        end_date = "2023-01-01"
        result_df = fetch_binance_data("BTCUSDT", "M1", start_date, end_date)

        self.assertIsNone(result_df) # Should fail after retries
        self.assertGreaterEqual(mock_client_instance.get_historical_klines.call_count, 5) # 5 attempts

    @patch('src.data.fetchers.binance_fetcher.os.getenv')
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    def test_fetch_binance_data_invalid_symbol(self, MockBinanceClient, mock_getenv, __):
        mock_getenv.return_value = None
        mock_client_instance = MockBinanceClient.return_value
        # CORRECTED: Simulate invalid symbol error using 'message' and mocking response if needed by code
        # Let's assume the code checks e.code and e.status_code based on previous traceback attempt
        mock_response = MagicMock(status_code=400)
        error_exception = BinanceAPIException(response=mock_response, message="Invalid symbol")
        setattr(error_exception, 'code', -1121) # Manually add code if necessary
        mock_client_instance.get_historical_klines.side_effect = error_exception

        start_date = "2023-01-01"
        end_date = "2023-01-01"
        result_df = fetch_binance_data("INVALIDTICKER", "M1", start_date, end_date)

        self.assertIsNone(result_df)
        # Should fail on first attempt for invalid symbol
        mock_client_instance.get_historical_klines.assert_called_once()


# Allow running tests directly
if __name__ == '__main__':
    unittest.main()