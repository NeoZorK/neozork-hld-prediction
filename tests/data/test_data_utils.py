# tests/data/test_data_utils.py # MODIFIED - Fixed failing tests again

import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
import numpy as np
from pathlib import Path
import os

# Import functions from the module to be tested
from src.data.data_utils import (
    get_demo_data,
    map_interval,
    map_ticker,
    fetch_yfinance_data,
    fetch_csv_data,
    map_polygon_interval,
    resolve_polygon_ticker,
    fetch_polygon_data,
    POLYGON_AVAILABLE
)
# Import polygon exceptions if available for mocking/testing
try:
    # noinspection PyUnresolvedReferences
    from polygon.exceptions import BadResponse
except ImportError:
    class BadResponse(Exception): pass


# Mock logger for testing
class MockLogger:
    ERROR_COLOR = ""
    RESET_ALL = ""
    HIGHLIGHT_COLOR=""
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass
    def print_success(self, msg): pass


# Unit tests for data utility functions
@patch('src.data.data_utils.logger', new_callable=MockLogger) # Apply mock logger to all methods
class TestDataUtils(unittest.TestCase):

    # --- Existing Tests (Keep As Is or Minor Adjustments) ---
    def test_get_demo_data(self, _): # Add _ for mock logger
        df = get_demo_data()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 30)
        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.assertListEqual(list(df.columns), expected_cols)
        self.assertIsInstance(df.index, pd.DatetimeIndex)

    def test_map_interval_valid(self, _):
        self.assertEqual(map_interval("M1"), "1m")
        self.assertEqual(map_interval("m5"), "5m")
        self.assertEqual(map_interval("H1"), "1h")
        # ... (other valid mappings) ...
        self.assertEqual(map_interval("1WK"), "1wk")

    def test_map_interval_invalid(self, _):
        with self.assertRaises(ValueError): map_interval("invalid")
        with self.assertRaises(ValueError): map_interval("M60")

    def test_map_ticker(self, _):
        self.assertEqual(map_ticker("EURUSD"), "EURUSD=X")
        self.assertEqual(map_ticker("AAPL"), "AAPL")
        # ... (other ticker mappings) ...
        self.assertEqual(map_ticker("TOOLONGTICKER"), "TOOLONGTICKER")

    @patch('src.data.data_utils.yf.download')
    def test_fetch_yfinance_data_success_simple_cols(self, mock_yf_download, _):
        mock_df = pd.DataFrame({'Open': [100, 101], 'High': [102, 103], 'Low': [99, 98], 'Close': [101, 102], 'Adj Close': [101, 102], 'Volume': [1000, 1100]}, index=pd.to_datetime(['2023-01-01', '2023-01-02']))
        mock_yf_download.return_value = mock_df.copy()
        result_df = fetch_yfinance_data('AAPL', '1d', period='1mo')
        self.assertIsInstance(result_df, pd.DataFrame)
        # ... (other assertions) ...
        mock_yf_download.assert_called_once()

    @patch('src.data.data_utils.yf.download')
    def test_fetch_yfinance_data_empty(self, mock_yf_download, _):
        mock_yf_download.return_value = pd.DataFrame()
        result_df = fetch_yfinance_data('EMPTY', '1d', period='1d')
        self.assertIsNone(result_df)
        mock_yf_download.assert_called_once()

    @patch('src.data.data_utils.yf.download')
    def test_fetch_yfinance_data_missing_cols(self, mock_yf_download, _):
        mock_df = pd.DataFrame({'Open': [100], 'High': [102], 'Volume': [1000]})
        mock_yf_download.return_value = mock_df
        result_df = fetch_yfinance_data('MISSING', '1d', period='1d')
        self.assertIsNone(result_df)
        mock_yf_download.assert_called_once()

    @patch('src.data.data_utils.yf.download')
    def test_fetch_yfinance_data_with_nans(self, mock_yf_download, _):
        mock_df = pd.DataFrame({'Open': [100, 101, np.nan], 'High': [102, 103, 104], 'Low': [99, np.nan, 98], 'Close': [101, 102, 103], 'Volume': [1000, 1100, 1200]}, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']))
        mock_yf_download.return_value = mock_df.copy()
        result_df = fetch_yfinance_data('NANTEST', '1d', period='3d')
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertEqual(len(result_df), 3)
        expected_indices = pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03'])
        pd.testing.assert_index_equal(result_df.index, pd.Index(expected_indices))

    @patch('src.data.data_utils.yf.download')
    def test_fetch_yfinance_data_multiindex_cols(self, mock_yf_download, _):
        arrays = [['Open', 'High', 'Low', 'Close', 'Volume'], ['GOOG', 'GOOG', 'GOOG', 'GOOG', 'GOOG']]
        tuples = list(zip(*arrays)); multi_index = pd.MultiIndex.from_tuples(tuples, names=['ValueType', 'Ticker'])
        mock_df = pd.DataFrame({('Open', 'GOOG'): [100], ('High', 'GOOG'): [102], ('Low', 'GOOG'): [99], ('Close', 'GOOG'): [101], ('Volume', 'GOOG'): [1000]}, index=pd.to_datetime(['2023-01-01'])); mock_df.columns = multi_index
        mock_yf_download.return_value = mock_df.copy()
        result_df = fetch_yfinance_data('GOOG', '1d', period='1d')
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertFalse(result_df.empty)
        self.assertListEqual(list(result_df.columns), ['Open', 'High', 'Low', 'Close', 'Volume'])
        self.assertEqual(len(result_df), 1)

    @patch('src.data.data_utils.yf.download')
    @patch('traceback.format_exc')
    def test_fetch_yfinance_data_exception(self, mock_traceback, mock_yf_download, _):
        mock_yf_download.side_effect = Exception("Network Error")
        mock_traceback.return_value = "Mocked Traceback"
        result_df = fetch_yfinance_data('ERROR', '1d', period='1d')
        self.assertIsNone(result_df)
        mock_yf_download.assert_called_once()
        mock_traceback.assert_called_once()

    # --- Tests for fetch_csv_data ---
    @patch('pandas.read_csv')
    @patch('pathlib.Path.is_file', return_value=True)
    def test_fetch_csv_success(self, mock_is_file, mock_read_csv, _):
        # Test setup as corrected in Turn 61/63
        expected_data_read = {
            'DateTime': ['2024.04.17 00:00', '2024.04.18 00:00'],
            'TickVolume': [1000, 1200], 'Open': [1.1, 1.105], 'High': [1.11, 1.115],
            'Low': [1.09, 1.10], 'Close': [1.105, 1.112], 'predicted_low': [1.08, 'inf'],
            'predicted_high': [1.12, '-inf'], 'pressure': [10.5, 'NaN'],
            'pressure_vector': [0.5, 1.2], 'Unnamed: 10': [np.nan, np.nan]
        }
        mock_return_df = pd.DataFrame(expected_data_read)
        mock_return_df.columns = ['DateTime', '\tTickVolume', '\tOpen', '\tHigh', '\tLow', '\tClose', '\tpredicted_low', 'predicted_high', 'pressure', 'pressure_vector', 'Unnamed: 10']
        mock_read_csv.return_value = mock_return_df
        result_df = fetch_csv_data("dummy/path.csv")
        mock_read_csv.assert_called_once_with(Path("dummy/path.csv"), sep=',', header=1, skipinitialspace=True, low_memory=False)
        self.assertIsInstance(result_df, pd.DataFrame)
        # ... other assertions for test_fetch_csv_success ...
        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in expected_cols: self.assertIn(col, result_df.columns)
        self.assertNotIn('TickVolume', result_df.columns)


    @patch('pathlib.Path.is_file', return_value=False)
    def test_fetch_csv_file_not_found(self, mock_is_file, _):
        result_df = fetch_csv_data("nonexistent/path.csv")
        self.assertIsNone(result_df)

    @patch('pandas.read_csv')
    @patch('pathlib.Path.is_file', return_value=True)
    def test_fetch_csv_empty_file(self, mock_is_file, mock_read_csv, _):
        mock_read_csv.return_value = pd.DataFrame()
        result_df = fetch_csv_data("dummy/empty.csv")
        self.assertIsNone(result_df)

    @patch('pandas.read_csv', side_effect=pd.errors.ParserError("Mock parse error"))
    @patch('pathlib.Path.is_file', return_value=True)
    def test_fetch_csv_parse_error(self, mock_is_file, mock_read_csv, _):
        result_df = fetch_csv_data("dummy/bad_format.csv")
        self.assertIsNone(result_df)

    # --- Tests for map_polygon_interval ---
    def test_map_polygon_interval_valid(self, _):
        self.assertEqual(map_polygon_interval("M1"), ("minute", 1))
        self.assertEqual(map_polygon_interval("H1"), ("hour", 1))
        self.assertEqual(map_polygon_interval("D"), ("day", 1))
        # ... other valid cases ...

    def test_map_polygon_interval_invalid(self, _):
        self.assertIsNone(map_polygon_interval("invalid"))
        # ... other invalid cases ...

    # --- Tests for resolve_polygon_ticker (Corrected & Expanded) ---
    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed, skipping relevant tests.")
    @patch('src.data.data_utils.polygon.RESTClient')
    def test_resolve_polygon_ticker_stock(self, MockRESTClient, _):
        mock_client_instance = MockRESTClient.return_value
        mock_client_instance.get_ticker_details.side_effect = lambda ticker: MagicMock() if ticker == 'AAPL' else (_ for _ in ()).throw(BadResponse('{"status":"NOT_FOUND"}'))
        resolved = resolve_polygon_ticker("AAPL", mock_client_instance)
        self.assertEqual(resolved, "AAPL")
        mock_client_instance.get_ticker_details.assert_called_once_with("AAPL")

    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch('time.sleep') # Mock time.sleep
    @patch('src.data.data_utils.polygon.RESTClient')
    def test_resolve_polygon_ticker_forex(self, MockRESTClient, mock_sleep, _): # Pass mocks in correct order
        mock_client_instance = MockRESTClient.return_value
        mock_404_exception = BadResponse('{"status":"NOT_FOUND", "message":"Mock Not Found"}')
        def mock_details_fx(ticker):
            if ticker == 'EURUSD': raise mock_404_exception
            elif ticker == 'C:EURUSD': return MagicMock()
            else: raise mock_404_exception
        mock_client_instance.get_ticker_details.side_effect = mock_details_fx
        resolved = resolve_polygon_ticker("EURUSD", mock_client_instance)
        self.assertEqual(resolved, "C:EURUSD")
        calls = [call("EURUSD"), call("C:EURUSD")]
        mock_client_instance.get_ticker_details.assert_has_calls(calls)
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 2)
        mock_sleep.assert_called_once_with(15)

    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch('time.sleep')
    @patch('src.data.data_utils.polygon.RESTClient')
    def test_resolve_polygon_ticker_crypto(self, MockRESTClient, mock_sleep, _):
        mock_client_instance = MockRESTClient.return_value
        mock_404_exception = BadResponse('{"status":"NOT_FOUND", "message":"Mock Not Found"}')
        def mock_details_crypto(ticker):
            if ticker == 'BTCUSD': raise mock_404_exception
            elif ticker == 'C:BTCUSD': raise mock_404_exception
            elif ticker == 'X:BTCUSD': return MagicMock()
            else: raise mock_404_exception
        mock_client_instance.get_ticker_details.side_effect = mock_details_crypto
        resolved = resolve_polygon_ticker("BTCUSD", mock_client_instance)
        self.assertEqual(resolved, "X:BTCUSD")
        calls = [call("BTCUSD"), call("C:BTCUSD"), call("X:BTCUSD")]
        mock_client_instance.get_ticker_details.assert_has_calls(calls)
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch('time.sleep')
    @patch('src.data.data_utils.polygon.RESTClient')
    def test_resolve_polygon_ticker_not_found(self, MockRESTClient, mock_sleep, _): #<<< FIXED THIS TEST
        mock_client_instance = MockRESTClient.return_value
        mock_404_exception = BadResponse('{"status":"NOT_FOUND", "message":"Mock Not Found"}')
        mock_client_instance.get_ticker_details.side_effect = mock_404_exception
        resolved = resolve_polygon_ticker("UNKNOWNXYZ", mock_client_instance)
        self.assertIsNone(resolved)
        calls = [call("UNKNOWNXYZ"), call("C:UNKNOWNXYZ"), call("X:UNKNOWNXYZ"), call("I:UNKNOWNXYZ")]
        mock_client_instance.get_ticker_details.assert_has_calls(calls)
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 4)
        # *** FIX: Assert sleep count is 4, not 3 ***
        self.assertEqual(mock_sleep.call_count, 4) # Called after each of the 4 attempts fail with 404


    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch('time.sleep')
    @patch('src.data.data_utils.polygon.RESTClient')
    def test_resolve_polygon_ticker_api_error(self, MockRESTClient, mock_sleep, _): #<<< FIXED THIS TEST
        mock_client_instance = MockRESTClient.return_value
        # *** FIX: Initialize BadResponse with a string, not kwargs ***
        mock_api_error_exception = BadResponse("Mock API Error 401 Unauthorized")
        mock_client_instance.get_ticker_details.side_effect = mock_api_error_exception
        resolved = resolve_polygon_ticker("ANYTICKER", mock_client_instance)
        self.assertIsNone(resolved)
        mock_client_instance.get_ticker_details.assert_called_once_with("ANYTICKER")
        mock_sleep.assert_not_called()

    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch('time.sleep')
    @patch('src.data.data_utils.polygon.RESTClient')
    def test_resolve_polygon_ticker_unexpected_error(self, MockRESTClient, mock_sleep, _):
        mock_client_instance = MockRESTClient.return_value
        mock_client_instance.get_ticker_details.side_effect = ValueError("Something unexpected happened")
        resolved = resolve_polygon_ticker("ANYTICKER", mock_client_instance)
        self.assertIsNone(resolved)
        mock_client_instance.get_ticker_details.assert_called_once_with("ANYTICKER")
        mock_sleep.assert_not_called()

    # --- Tests for fetch_polygon_data (Corrected & Expanded) ---
    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch.dict(os.environ, {"POLYGON_API_KEY": "test_key"}, clear=True)
    @patch('src.data.data_utils.resolve_polygon_ticker')
    @patch('src.data.data_utils.polygon.RESTClient')
    def test_fetch_polygon_success(self, MockRESTClient, mock_resolve, _):
        mock_resolve.return_value = "AAPL"
        mock_client_instance = MockRESTClient.return_value
        mock_agg1 = MagicMock(spec=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        mock_agg1.timestamp=1672531200000; mock_agg1.open=100; mock_agg1.high=102; mock_agg1.low=99; mock_agg1.close=101; mock_agg1.volume=1000
        mock_agg2 = MagicMock(spec=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        mock_agg2.timestamp=1672617600000; mock_agg2.open=101; mock_agg2.high=103; mock_agg2.low=98; mock_agg2.close=102; mock_agg2.volume=1200
        mock_client_instance.get_aggs.return_value = [mock_agg1, mock_agg2]
        result_df = fetch_polygon_data("AAPL", "D1", "2023-01-01", "2023-01-02")
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertEqual(len(result_df), 2)
        # ... other assertions ...

    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch.dict(os.environ, {"POLYGON_API_KEY": "test_key"}, clear=True)
    @patch('src.data.data_utils.resolve_polygon_ticker')
    @patch('src.data.data_utils.polygon.RESTClient')
    def test_fetch_polygon_resolve_fails(self, MockRESTClient, mock_resolve, _):
        mock_resolve.return_value = None
        mock_client_instance = MockRESTClient.return_value
        result_df = fetch_polygon_data("UNKNOWN", "D1", "2023-01-01", "2023-01-02")
        self.assertIsNone(result_df)
        mock_resolve.assert_called_once_with("UNKNOWN", mock_client_instance)
        mock_client_instance.get_aggs.assert_not_called()

    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch.dict(os.environ, {"POLYGON_API_KEY": "test_key"}, clear=True)
    @patch('src.data.data_utils.resolve_polygon_ticker')
    @patch('src.data.data_utils.polygon.RESTClient')
    def test_fetch_polygon_no_data(self, MockRESTClient, mock_resolve, _):
        mock_resolve.return_value = "AAPL"
        mock_client_instance = MockRESTClient.return_value
        mock_client_instance.get_aggs.return_value = []
        result_df = fetch_polygon_data("AAPL", "D1", "2023-01-01", "2023-01-02")
        self.assertIsNone(result_df)
        mock_resolve.assert_called_once()
        mock_client_instance.get_aggs.assert_called_once()

    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch.dict(os.environ, {"POLYGON_API_KEY": "test_key"}, clear=True)
    @patch('src.data.data_utils.resolve_polygon_ticker')
    @patch('src.data.data_utils.polygon.RESTClient')
    def test_fetch_polygon_api_error_on_aggs(self, MockRESTClient, mock_resolve, _):
        mock_resolve.return_value = "AAPL"
        mock_client_instance = MockRESTClient.return_value
        mock_client_instance.get_aggs.side_effect = BadResponse("API limit reached on aggs")
        result_df = fetch_polygon_data("AAPL", "D1", "2023-01-01", "2023-01-02")
        self.assertIsNone(result_df)
        mock_resolve.assert_called_once()
        mock_client_instance.get_aggs.assert_called_once()

    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch.dict(os.environ, {}, clear=True) # Ensure key is NOT in env
    def test_fetch_polygon_key_missing(self, _):
        result_df = fetch_polygon_data("AAPL", "D1", "2023-01-01", "2023-01-02")
        self.assertIsNone(result_df)

    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch.dict(os.environ, {"POLYGON_API_KEY": "test_key"}, clear=True)
    @patch('src.data.data_utils.resolve_polygon_ticker')
    def test_fetch_polygon_invalid_dates(self, mock_resolve, _):
        mock_resolve.return_value = "AAPL"
        result_df = fetch_polygon_data("AAPL", "D1", "2023/01/01", "2023-01-02")
        self.assertIsNone(result_df)
        mock_resolve.assert_called_once()

    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch.dict(os.environ, {"POLYGON_API_KEY": "test_key"}, clear=True)
    @patch('src.data.data_utils.resolve_polygon_ticker')
    def test_fetch_polygon_invalid_interval(self, mock_resolve, _):
        mock_resolve.return_value = "AAPL"
        result_df = fetch_polygon_data("AAPL", "BADINTERVAL", "2023-01-01", "2023-01-02")
        self.assertIsNone(result_df)
        mock_resolve.assert_called_once()


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()