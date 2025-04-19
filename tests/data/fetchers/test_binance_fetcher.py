# tests/data/fetchers/test_binance_fetcher.py

import unittest
from unittest.mock import patch
from datetime import datetime

# Functions/classes to test or mock
from src.data.fetchers.binance_fetcher import (
    fetch_binance_data, map_binance_interval, map_binance_ticker,
    BINANCE_AVAILABLE, BinanceAPIException # Import exceptions
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
        self.assertEqual(args_call['interval'], '1m')
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

        # Assume limit=2 for testing pagination easily
        with patch('src.data.fetchers.binance_fetcher.limit_per_request', 2):
             mock_client_instance.get_historical_klines.side_effect = [
                 [kline1, kline2], # First call returns 2
                 [kline3],       # Second call returns 1 (< limit)
                 # No third call needed as previous returned < limit
             ]

             # Call function
             start_date = "2024-04-01"
             end_date = "2024-04-01" # Range within one day
             result_df = fetch_binance_data("BTCUSDT", "M1", start_date, end_date)

             # Assertions
             self.assertIsNotNone(result_df)
             self.assertEqual(len(result_df), 3) # All aggregates combined
             self.assertEqual(mock_client_instance.get_historical_klines.call_count, 2)

             # Verify start_str logic
             calls = mock_client_instance.get_historical_klines.call_args_list
             # First call starts at the beginning of the day
             expected_start1_ms = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp() * 1000)
             self.assertEqual(calls[0][1]['start_str'], str(expected_start1_ms))
             # Second call starts 1ms after the last kline of the first call
             expected_start2_ms = kline2[0] + 1
             self.assertEqual(calls[1][1]['start_str'], str(expected_start2_ms))

             # Verify final DataFrame content
             self.assertEqual(result_df.iloc[0]['Open'], 70000.0)
             self.assertEqual(result_df.iloc[2]['Close'], 70250.0)
             self.assertTrue(result_df.index.is_monotonic_increasing)


    @patch('src.data.fetchers.binance_fetcher.os.getenv')
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    def test_fetch_binance_data_api_error(self, MockBinanceClient, mock_getenv, __):
        mock_getenv.return_value = None
        mock_client_instance = MockBinanceClient.return_value
        # Simulate API error
        mock_client_instance.get_historical_klines.side_effect = BinanceAPIException("Test API Error", status_code=500)

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
        # Simulate invalid symbol error (-1121)
        mock_client_instance.get_historical_klines.side_effect = BinanceAPIException("Invalid symbol", status_code=400, code=-1121)

        start_date = "2023-01-01"
        end_date = "2023-01-01"
        result_df = fetch_binance_data("INVALIDTICKER", "M1", start_date, end_date)

        self.assertIsNone(result_df)
        # Should fail on first attempt for invalid symbol
        mock_client_instance.get_historical_klines.assert_called_once()


# Allow running tests directly
if __name__ == '__main__':
    unittest.main()