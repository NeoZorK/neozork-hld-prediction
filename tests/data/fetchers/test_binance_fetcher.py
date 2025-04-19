# tests/data/fetchers/test_binance_fetcher.py # CORRECTED

import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
from datetime import datetime
import numpy as np # Import numpy for dtypes

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
    # Import the real class if available for constants
    try:
        from binance.client import Client as BinanceClient_orig
    except ImportError:
        # Define dummy if even the real import fails somehow (defensive)
        class BinanceClient_orig:
            KLINE_INTERVAL_1MINUTE = '1m'; KLINE_INTERVAL_1HOUR = '1h'; KLINE_INTERVAL_1DAY = '1d'; KLINE_INTERVAL_1WEEK = '1w'; KLINE_INTERVAL_1MONTH = '1M'
else:
    # Define dummy for type hinting if lib not installed
     class BinanceClient_orig:
        KLINE_INTERVAL_1MINUTE = '1m'; KLINE_INTERVAL_1HOUR = '1h'; KLINE_INTERVAL_1DAY = '1d'; KLINE_INTERVAL_1WEEK = '1w'; KLINE_INTERVAL_1MONTH = '1M'


@patch('src.data.fetchers.binance_fetcher.logger', new_callable=MockLogger)
@patch('src.data.fetchers.binance_fetcher.BINANCE_AVAILABLE', True) # Assume library is available
class TestBinanceFetcher(unittest.TestCase):

    # --- Tests for map_binance_interval ---
    def test_map_binance_interval_mql(self, _):
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
        mock_getenv.side_effect = lambda k: "fake_key" if k == "BINANCE_API_KEY" else "fake_secret"
        mock_client_instance = MockBinanceClient.return_value

        kline1 = [1672531200000, '40000.0', '40100.5', '39900.1', '40050.2', '100.5', 1672531259999, '...', 50, '50', '...', '0']
        kline2 = [1672531260000, '40050.2', '40200.0', '40000.0', '40150.9', '110.1', 1672531319999, '...', 55, '60', '...', '0']
        mock_client_instance.get_historical_klines.return_value = [kline1, kline2]

        # Expected DataFrame (ensure float type for OHLCV)
        expected_dates = pd.to_datetime([1672531200000, 1672531260000], unit='ms')
        expected_data = {
            'Open': [40000.0, 40050.2], 'High': [40100.5, 40200.0], 'Low': [39900.1, 40000.0],
            'Close': [40050.2, 40150.9], 'Volume': [100.5, 110.1]
        }
        expected_df = pd.DataFrame(expected_data, index=expected_dates, dtype=np.float64)

        # Call function
        start_date = "2023-01-01"
        end_date = "2023-01-01"
        result_df = fetch_binance_data("BTCUSDT", "M1", start_date, end_date)

        # Assertions
        MockBinanceClient.assert_called_once_with(api_key="fake_key", api_secret="fake_secret")
        mock_client_instance.get_historical_klines.assert_called_once()
        args_call = mock_client_instance.get_historical_klines.call_args[1]
        self.assertEqual(args_call['symbol'], "BTCUSDT")
        # CORRECTED Assertion: Compare against the expected constant value string
        self.assertEqual(args_call['interval'], BinanceClient_orig.KLINE_INTERVAL_1MINUTE)

        self.assertIsNotNone(result_df)
        # Use pandas testing function for robust comparison
        pd.testing.assert_frame_equal(result_df, expected_df)


    @patch('src.data.fetchers.binance_fetcher.time.sleep') # Mock sleep for pagination test
    @patch('src.data.fetchers.binance_fetcher.os.getenv')
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    def test_fetch_binance_data_success_pagination(self, MockBinanceClient, mock_getenv, mock_sleep, __):
        mock_getenv.return_value = None
        mock_client_instance = MockBinanceClient.return_value

        # Simulate pagination: first call returns 2 items, second returns 1
        kline1 = [1711929600000, '70000', '70100', '69900', '70050', '10', 1711929659999, '...', 0, '0', '0', '0'] # t1
        kline2 = [1711929660000, '70050', '70200', '70000', '70150', '11', 1711929719999, '...', 0, '0', '0', '0'] # t2
        kline3 = [1711929720000, '70150', '70300', '70100', '70250', '12', 1711929779999, '...', 0, '0', '0', '0'] # t3

        # CORRECTED: Setup side_effect to mimic sequential calls
        mock_client_instance.get_historical_klines.side_effect = [
            [kline1, kline2], # Call 1 returns 2 klines
            [kline3],       # Call 2 returns 1 kline (< limit)
            []              # Call 3 returns empty (or wouldn't be called if prev < limit)
        ]

        start_date = "2024-04-01"
        end_date = "2024-04-01"
        result_df = fetch_binance_data("BTCUSDT", "M1", start_date, end_date)

        # Assertions
        self.assertIsNotNone(result_df)
        self.assertEqual(len(result_df), 3) # CORRECTED: Expect all 3 results
        # The loop should break after the second call returns fewer than limit (1000)
        self.assertEqual(mock_client_instance.get_historical_klines.call_count, 2)
        self.assertEqual(mock_sleep.call_count, 1) # Slept between successful calls

        calls = mock_client_instance.get_historical_klines.call_args_list
        expected_start1_ms = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp() * 1000)
        self.assertEqual(calls[0][1]['start_str'], str(expected_start1_ms))
        expected_start2_ms = kline2[0] + 1 # Start after last kline of previous chunk
        self.assertEqual(calls[1][1]['start_str'], str(expected_start2_ms))

        self.assertEqual(result_df.iloc[0]['Open'], 70000.0)
        self.assertEqual(result_df.iloc[2]['Close'], 70250.0)
        self.assertTrue(result_df.index.is_monotonic_increasing)


    @patch('src.data.fetchers.binance_fetcher.os.getenv')
    @patch('src.data.fetchers.binance_fetcher.BinanceClient')
    def test_fetch_binance_data_api_error(self, MockBinanceClient, mock_getenv, __):
        mock_getenv.return_value = None
        mock_client_instance = MockBinanceClient.return_value
        # CORRECTED: Simulate API error without keywords unsupported by base Exception
        mock_client_instance.get_historical_klines.side_effect = BinanceAPIException() # No args

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
        # CORRECTED: Simulate invalid symbol error
        # Create a base exception and add attributes if the code actually checks them
        mock_error = BinanceAPIException()
        setattr(mock_error, 'status_code', 400) # Add attributes if needed by handling logic
        setattr(mock_error, 'code', -1121)
        mock_client_instance.get_historical_klines.side_effect = mock_error

        start_date = "2023-01-01"
        end_date = "2023-01-01"
        result_df = fetch_binance_data("INVALIDTICKER", "M1", start_date, end_date)

        self.assertIsNone(result_df)
        # Should fail on first attempt for invalid symbol
        mock_client_instance.get_historical_klines.assert_called_once()


# Allow running tests directly
if __name__ == '__main__':
    unittest.main()