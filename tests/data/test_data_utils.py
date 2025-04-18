# tests/data/test_data_utils.py # MODIFIED
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open
import pandas as pd
from datetime import date, timedelta, datetime
import numpy as np
import io # Added for StringIO
from pathlib import Path # Added for Path mocking

# Import functions from the module to be tested
# Ensure all relevant functions are imported
from src.data.data_utils import (
    get_demo_data,
    map_interval,
    map_ticker,
    fetch_yfinance_data,
    fetch_csv_data,          # Added
    map_polygon_interval,    # Added
    resolve_polygon_ticker,  # Added
    fetch_polygon_data,      # Added
    POLYGON_AVAILABLE      # Import flag for conditional tests
)
# Import polygon exceptions if available for mocking/testing
try:
    from polygon.exceptions import BadResponse
except ImportError:
    class BadResponse(Exception): pass # Dummy for tests if not installed


# Mock logger for testing (keep as is)
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
# Use patch decorators at the class level if logger is used in most methods
@patch('src.data.data_utils.logger', new_callable=MockLogger)
class TestDataUtils(unittest.TestCase):

    # --- Existing Tests (Keep As Is) ---
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
        self.assertEqual(map_interval("h4"), "4h")
        self.assertEqual(map_interval("D1"), "1d")
        self.assertEqual(map_interval("d"), "1d")
        self.assertEqual(map_interval("W1"), "1wk")
        self.assertEqual(map_interval("W"), "1wk")
        self.assertEqual(map_interval("WK"), "1wk")
        self.assertEqual(map_interval("MN1"), "1mo")
        self.assertEqual(map_interval("MN"), "1mo")
        self.assertEqual(map_interval("MO"), "1mo")
        self.assertEqual(map_interval("15m"), "15m")
        self.assertEqual(map_interval("1d"), "1d")
        self.assertEqual(map_interval("1WK"), "1wk")

    def test_map_interval_invalid(self, _):
        with self.assertRaises(ValueError): map_interval("invalid")
        with self.assertRaises(ValueError): map_interval("M60")

    def test_map_ticker(self, _):
        self.assertEqual(map_ticker("EURUSD"), "EURUSD=X")
        self.assertEqual(map_ticker("GBPUSD=X"), "GBPUSD=X")
        self.assertEqual(map_ticker("usdjpy=x"), "USDJPY=X")
        self.assertEqual(map_ticker("AAPL"), "AAPL")
        self.assertEqual(map_ticker("BTC-USD"), "BTC-USD")
        self.assertEqual(map_ticker("ES=F"), "ES=F")
        self.assertEqual(map_ticker("6E=F"), "6E=F")
        self.assertEqual(map_ticker("EUR"), "EUR")
        self.assertEqual(map_ticker("TOOLONGTICKER"), "TOOLONGTICKER")

    @patch('src.data.data_utils.yf.download')
    def test_fetch_yfinance_data_success_simple_cols(self, mock_yf_download, _):
        mock_df = pd.DataFrame({'Open': [100, 101], 'High': [102, 103], 'Low': [99, 98], 'Close': [101, 102], 'Adj Close': [101, 102], 'Volume': [1000, 1100]}, index=pd.to_datetime(['2023-01-01', '2023-01-02']))
        mock_yf_download.return_value = mock_df.copy()
        result_df = fetch_yfinance_data('AAPL', '1d', period='1mo')
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertFalse(result_df.empty)
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_cols: self.assertIn(col, result_df.columns)
        self.assertEqual(len(result_df), 2)
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

    # --- NEW Tests for fetch_csv_data ---

    # Helper method to create mock CSV data
    def _create_mock_csv(self, content):
        # Simulates reading from a file path using io.StringIO
        # Path().is_file() needs patching separately if used before open
        # pandas.read_csv can directly read StringIO
        return io.StringIO(content)

    @patch('pandas.read_csv')
    @patch('pathlib.Path.is_file', return_value=True) # Mock file exists
    def test_fetch_csv_success(self, mock_is_file, mock_read_csv, _):
        # Sample CSV content similar to the MQL5 export
        csv_content = (
            "Info line to skip\n"
            "DateTime,\tTickVolume,\tOpen,\tHigh,\tLow,\tClose,\tpredicted_low,\tpredicted_high,\tpressure,\tpressure_vector,\tUnnamed: 10,\n"
            "2024.04.17 00:00,1000,1.1,1.11,1.09,1.105,1.08,1.12,10.5,0.5,,\n"
            "2024.04.18 00:00,1200,1.105,1.115,1.10,1.112,inf,-inf,NaN,1.2,,\n" # Include inf/NaN
        )
        mock_df = pd.read_csv(self._create_mock_csv(csv_content), sep=',', header=1, skipinitialspace=True)
        mock_read_csv.return_value = mock_df

        result_df = fetch_csv_data("dummy/path.csv")

        mock_is_file.assert_called_once()
        mock_read_csv.assert_called_once()
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertEqual(len(result_df), 2)
        # Check standard columns exist and TickVolume is renamed
        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in expected_cols: self.assertIn(col, result_df.columns)
        self.assertNotIn('TickVolume', result_df.columns)
        # Check unnamed column is dropped
        self.assertNotIn('Unnamed: 10', result_df.columns)
        self.assertNotIn('', result_df.columns) # Check for empty string column name
        # Check DateTime index
        self.assertIsInstance(result_df.index, pd.DatetimeIndex)
        self.assertEqual(result_df.index[0], pd.Timestamp('2024-04-17 00:00'))
        # Check inf replaced by NaN
        self.assertTrue(pd.isna(result_df.loc['2024-04-18', 'predicted_low']))
        self.assertTrue(pd.isna(result_df.loc['2024-04-18', 'predicted_high']))
        # Check other numeric columns exist
        self.assertIn('pressure', result_df.columns)
        self.assertIn('pressure_vector', result_df.columns)

    @patch('pathlib.Path.is_file', return_value=False) # Mock file does NOT exist
    def test_fetch_csv_file_not_found(self, mock_is_file, _):
        result_df = fetch_csv_data("nonexistent/path.csv")
        self.assertIsNone(result_df)
        mock_is_file.assert_called_once()

    @patch('pandas.read_csv')
    @patch('pathlib.Path.is_file', return_value=True)
    def test_fetch_csv_empty_file(self, mock_is_file, mock_read_csv, _):
        mock_read_csv.return_value = pd.DataFrame() # Simulate empty file
        result_df = fetch_csv_data("dummy/empty.csv")
        self.assertIsNone(result_df)

    @patch('pandas.read_csv', side_effect=pd.errors.ParserError("Mock parse error"))
    @patch('pathlib.Path.is_file', return_value=True)
    def test_fetch_csv_parse_error(self, mock_is_file, mock_read_csv, _):
        result_df = fetch_csv_data("dummy/bad_format.csv")
        self.assertIsNone(result_df)

    # --- NEW Tests for map_polygon_interval ---

    def test_map_polygon_interval_valid(self, _):
        self.assertEqual(map_polygon_interval("M1"), ("minute", 1))
        self.assertEqual(map_polygon_interval("M15"), ("minute", 15))
        self.assertEqual(map_polygon_interval("H1"), ("hour", 1))
        self.assertEqual(map_polygon_interval("H4"), ("hour", 4))
        self.assertEqual(map_polygon_interval("D1"), ("day", 1))
        self.assertEqual(map_polygon_interval("D"), ("day", 1))
        self.assertEqual(map_polygon_interval("W1"), ("week", 1))
        self.assertEqual(map_polygon_interval("WK"), ("week", 1))
        self.assertEqual(map_polygon_interval("MN1"), ("month", 1))
        self.assertEqual(map_polygon_interval("MO"), ("month", 1))
        # Test direct timespan input
        self.assertEqual(map_polygon_interval("minute"), ("minute", 1))
        self.assertEqual(map_polygon_interval("day"), ("day", 1))

    def test_map_polygon_interval_invalid(self, _):
        self.assertIsNone(map_polygon_interval("invalid"))
        self.assertIsNone(map_polygon_interval("M60")) # Not directly supported by mapping

    # --- NEW Tests for resolve_polygon_ticker ---
    # These require mocking the polygon client and its methods

    # Use unittest.skipIf to skip Polygon tests if library not available
    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed, skipping relevant tests.")
    @patch('src.data.data_utils.polygon.RESTClient') # Patch the client class
    def test_resolve_polygon_ticker_stock(self, MockRESTClient, _):
        # Mock the client instance and its method
        mock_client_instance = MockRESTClient.return_value
        # Configure get_ticker_details to succeed only for 'AAPL'
        def mock_details(ticker):
            if ticker == 'AAPL':
                mock_response = MagicMock() # Mock the response object itself if needed
                # Normally details would be inside response.results, but we just need it to NOT raise error
                return mock_response
            else:
                # Simulate 404 Not Found for other attempts
                mock_err_response = MagicMock()
                mock_err_response.status_code = 404
                raise BadResponse(response=mock_err_response)

        mock_client_instance.get_ticker_details.side_effect = mock_details

        resolved = resolve_polygon_ticker("AAPL", mock_client_instance)
        self.assertEqual(resolved, "AAPL")
        mock_client_instance.get_ticker_details.assert_called_once_with("AAPL")

    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch('time.sleep') # Mock time.sleep to avoid actual delays
    @patch('src.data.data_utils.polygon.RESTClient')
    def test_resolve_polygon_ticker_forex(self, MockRESTClient, mock_sleep, _):
        mock_client_instance = MockRESTClient.return_value
        # Configure side effect for get_ticker_details
        mock_404_response = MagicMock(status_code=404)
        mock_success_response = MagicMock()
        call_count = {'count': 0} # Use dict to allow modification in side_effect

        def mock_details_fx(ticker):
            call_count['count'] += 1
            if ticker == 'EURUSD':
                raise BadResponse(response=mock_404_response) # Raise 404 for base ticker
            elif ticker == 'C:EURUSD':
                return mock_success_response # Succeed for prefixed ticker
            else:
                # Fail any other unexpected calls
                raise BadResponse(response=mock_404_response)

        mock_client_instance.get_ticker_details.side_effect = mock_details_fx

        resolved = resolve_polygon_ticker("EURUSD", mock_client_instance)
        self.assertEqual(resolved, "C:EURUSD")
        # Check it was called twice (EURUSD then C:EURUSD)
        self.assertEqual(mock_client_instance.get_ticker_details.call_count, 2)
        mock_client_instance.get_ticker_details.assert_any_call("EURUSD")
        mock_client_instance.get_ticker_details.assert_any_call("C:EURUSD")
        # Check sleep was called after the 404
        mock_sleep.assert_called_once()

    # --- TODO: Add more tests for resolve_polygon_ticker ---
    #    - test_resolve_polygon_ticker_crypto (similar to forex, checks X:)
    #    - test_resolve_polygon_ticker_not_found (all attempts raise 404)
    #    - test_resolve_polygon_ticker_api_error (raises non-404 BadResponse)
    #    - test_resolve_polygon_ticker_unexpected_error (raises generic Exception)

    # --- NEW Tests for fetch_polygon_data ---

    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch.dict(os.environ, {"POLYGON_API_KEY": "test_key"}, clear=True) # Mock env var
    @patch('src.data.data_utils.resolve_polygon_ticker') # Mock the resolver
    @patch('src.data.data_utils.polygon.RESTClient') # Mock the client
    def test_fetch_polygon_success(self, MockRESTClient, mock_resolve, _):
        # Mock resolver to return a valid ticker
        mock_resolve.return_value = "AAPL"
        # Mock client and get_aggs
        mock_client_instance = MockRESTClient.return_value
        # Create mock aggregate objects
        mock_agg1 = MagicMock(timestamp=1672531200000, open=100, high=102, low=99, close=101, volume=1000)
        mock_agg2 = MagicMock(timestamp=1672617600000, open=101, high=103, low=98, close=102, volume=1200)
        mock_client_instance.get_aggs.return_value = [mock_agg1, mock_agg2] # Return a list of mocks

        result_df = fetch_polygon_data("AAPL", "D1", "2023-01-01", "2023-01-02")

        mock_resolve.assert_called_once_with("AAPL", mock_client_instance)
        mock_client_instance.get_aggs.assert_called_once()
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertEqual(len(result_df), 2)
        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in expected_cols: self.assertIn(col, result_df.columns)
        self.assertIsInstance(result_df.index, pd.DatetimeIndex)
        self.assertEqual(result_df.iloc[0]['Open'], 100)
        self.assertEqual(result_df.iloc[1]['Volume'], 1200)

    @unittest.skipIf(not POLYGON_AVAILABLE, "polygon-api-client library not installed.")
    @patch.dict(os.environ, {"POLYGON_API_KEY": "test_key"}, clear=True)
    @patch('src.data.data_utils.resolve_polygon_ticker') # Mock the resolver
    @patch('src.data.data_utils.polygon.RESTClient') # Mock the client
    def test_fetch_polygon_resolve_fails(self, MockRESTClient, mock_resolve, _):
        mock_resolve.return_value = None # Simulate resolver failure
        mock_client_instance = MockRESTClient.return_value

        result_df = fetch_polygon_data("UNKNOWN", "D1", "2023-01-01", "2023-01-02")

        self.assertIsNone(result_df)
        mock_resolve.assert_called_once_with("UNKNOWN", mock_client_instance)
        # get_aggs should not be called if resolution fails
        mock_client_instance.get_aggs.assert_not_called()

    # --- TODO: Add more tests for fetch_polygon_data ---
    #    - test_fetch_polygon_no_data (get_aggs returns empty list)
    #    - test_fetch_polygon_api_error (get_aggs raises BadResponse)
    #    - test_fetch_polygon_key_missing (patch os.getenv or environ)
    #    - test_fetch_polygon_invalid_dates
    #    - test_fetch_polygon_invalid_interval


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()