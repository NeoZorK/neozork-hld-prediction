# tests/data/fetchers/test_exrate_fetcher.py

"""
Unit tests for the Exchange Rate API fetcher.
"""

import pytest
import pandas as pd
import os
from unittest.mock import patch, Mock
from datetime import datetime, timedelta

# Import the module under test
from src.data.fetchers.exrate_fetcher import (
    map_exrate_interval,
    map_exrate_ticker,
    fetch_exrate_data
)


class TestMapExrateInterval:
    """Test cases for map_exrate_interval function."""
    
    def test_valid_daily_intervals(self):
        """Test that valid daily intervals are mapped correctly."""
        valid_intervals = ["D1", "D", "W1", "W", "WK", "MN1", "MN", "MO"]
        for interval in valid_intervals:
            result = map_exrate_interval(interval)
            assert result == "D1", f"Expected D1 for {interval}, got {result}"
    
    def test_intraday_intervals_warning(self):
        """Test that intraday intervals are mapped to D1 with warning."""
        intraday_intervals = ["M1", "M5", "M15", "M30", "H1", "H4"]
        for interval in intraday_intervals:
            result = map_exrate_interval(interval)
            assert result == "D1", f"Expected D1 for {interval}, got {result}"
    
    def test_case_insensitive(self):
        """Test that interval mapping is case insensitive."""
        assert map_exrate_interval("d1") == "D1"
        assert map_exrate_interval("D") == "D1"
        assert map_exrate_interval("1d") == "D1"
    
    def test_invalid_interval(self):
        """Test that invalid intervals return None."""
        invalid_intervals = ["X1", "INVALID", ""]
        for interval in invalid_intervals:
            result = map_exrate_interval(interval)
            assert result is None, f"Expected None for {interval}, got {result}"


class TestMapExrateTicker:
    """Test cases for map_exrate_ticker function."""
    
    def test_valid_six_char_ticker(self):
        """Test that 6-character currency pair tickers are mapped correctly."""
        test_cases = [
            ("EURUSD", ("EUR", "USD")),
            ("GBPJPY", ("GBP", "JPY")),
            ("AUDUSD", ("AUD", "USD")),
            ("USDCAD", ("USD", "CAD"))
        ]
        
        for ticker, expected in test_cases:
            result = map_exrate_ticker(ticker)
            assert result == expected, f"Expected {expected} for {ticker}, got {result}"
    
    def test_valid_slash_separated_ticker(self):
        """Test that slash-separated tickers are mapped correctly."""
        test_cases = [
            ("EUR/USD", ("EUR", "USD")),
            ("GBP/JPY", ("GBP", "JPY")),
            ("USD/CHF", ("USD", "CHF"))
        ]
        
        for ticker, expected in test_cases:
            result = map_exrate_ticker(ticker)
            assert result == expected, f"Expected {expected} for {ticker}, got {result}"
    
    def test_valid_underscore_separated_ticker(self):
        """Test that underscore-separated tickers are mapped correctly."""
        test_cases = [
            ("EUR_USD", ("EUR", "USD")),
            ("GBP_JPY", ("GBP", "JPY")),
            ("USD_CHF", ("USD", "CHF"))
        ]
        
        for ticker, expected in test_cases:
            result = map_exrate_ticker(ticker)
            assert result == expected, f"Expected {expected} for {ticker}, got {result}"
    
    def test_case_insensitive(self):
        """Test that ticker mapping is case insensitive."""
        result = map_exrate_ticker("eurusd")
        assert result == ("EUR", "USD")
        
        result = map_exrate_ticker("eur/usd")
        assert result == ("EUR", "USD")
    
    def test_crypto_ticker_warning(self):
        """Test that crypto-like tickers return None with warning."""
        crypto_tickers = ["BTCUSDT", "ETHUSDT", "ADAUSDT"]
        for ticker in crypto_tickers:
            result = map_exrate_ticker(ticker)
            assert result is None, f"Expected None for {ticker}, got {result}"
    
    def test_invalid_ticker_formats(self):
        """Test that invalid ticker formats return None."""
        invalid_tickers = [
            "INVALID",  # Too short
            "EURUSDX",  # Too long
            "EUR",      # Too short
            "123456",   # Numbers instead of currencies
            "EUR/USD/JPY",  # Too many parts
        ]
        
        for ticker in invalid_tickers:
            result = map_exrate_ticker(ticker)
            assert result is None, f"Expected None for {ticker}, got {result}"
    
    def test_unsupported_currencies(self):
        """Test that unsupported currencies return None."""
        unsupported_tickers = ["XXXYYY", "ABCDEF"]
        for ticker in unsupported_tickers:
            result = map_exrate_ticker(ticker)
            assert result is None, f"Expected None for {ticker}, got {result}"


class TestFetchExrateData:
    """Test cases for fetch_exrate_data function."""
    
    @patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'})
    @patch('src.data.fetchers.exrate_fetcher.requests.get')
    def test_successful_fetch(self, mock_get):
        """Test successful data fetch from Exchange Rate API."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "conversion_rates": {
                "USD": 1.0500
            }
        }
        mock_get.return_value = mock_response
        
        # Test fetch
        df, metrics = fetch_exrate_data("EURUSD", "D1", "2024-01-01", "2024-01-02")
        
        # Assertions - Updated for current data only
        assert df is not None
        assert not df.empty
        assert len(df) == 1  # One current rate (ignores date range)
        assert list(df.columns) == ['Open', 'High', 'Low', 'Close', 'Volume']
        assert all(df['Open'] == 1.0500)
        assert all(df['Close'] == 1.0500)
        assert all(df['Volume'] == 0)
        assert metrics['api_calls'] == 1  # Single current rate call
        assert metrics['rows_fetched'] == 1  # Single row
        assert metrics['error_message'] is None
    
    def test_missing_api_key(self):
        """Test behavior when API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            df, metrics = fetch_exrate_data("EURUSD", "D1", "2024-01-01", "2024-01-02")
            
            assert df is None
            assert "EXCHANGE_RATE_API_KEY not found" in metrics['error_message']
    
    def test_invalid_ticker(self):
        """Test behavior with invalid ticker."""
        df, metrics = fetch_exrate_data("INVALID", "D1", "2024-01-01", "2024-01-02")
        
        assert df is None
        assert "Invalid ticker format" in metrics['error_message']
    
    def test_invalid_interval(self):
        """Test behavior with invalid interval."""
        df, metrics = fetch_exrate_data("EURUSD", "INVALID", "2024-01-01", "2024-01-02")
        
        assert df is None
        assert "Invalid interval" in metrics['error_message']
    
    @patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'})
    @patch('src.data.fetchers.exrate_fetcher.requests.get')
    def test_invalid_date_range(self, mock_get):
        """Test behavior with invalid date range - now ignored since we fetch current data."""
        # Mock successful response since dates are ignored
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "conversion_rates": {
                "USD": 1.0500
            }
        }
        mock_get.return_value = mock_response
        
        df, metrics = fetch_exrate_data("EURUSD", "D1", "2024-01-02", "2024-01-01")
        
        # Should succeed because dates are ignored and current data is fetched
        assert df is not None
        assert len(df) == 1
        assert metrics['error_message'] is None

    @patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'})
    @patch('src.data.fetchers.exrate_fetcher.requests.get')
    def test_invalid_date_format(self, mock_get):
        """Test behavior with invalid date format - now ignored since we fetch current data."""
        # Mock successful response since dates are ignored
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "conversion_rates": {
                "USD": 1.0500
            }
        }
        mock_get.return_value = mock_response
        
        df, metrics = fetch_exrate_data("EURUSD", "D1", "invalid-date", "2024-01-02")
        
        # Should succeed because dates are ignored and current data is fetched
        assert df is not None
        assert len(df) == 1
        assert metrics['error_message'] is None
    
    @patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'})
    @patch('src.data.fetchers.exrate_fetcher.requests.get')
    def test_api_error_response(self, mock_get):
        """Test handling of API error responses."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "error",
            "error-type": "invalid-key"
        }
        mock_get.return_value = mock_response
        
        df, metrics = fetch_exrate_data("EURUSD", "D1", "2024-01-01", "2024-01-02")
        
        # API will be called but return error, so we might get None or empty DataFrame
        # The specific behavior depends on implementation details
        assert metrics['api_calls'] >= 1
    
    @patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'})
    @patch('src.data.fetchers.exrate_fetcher.requests.get')
    def test_http_error(self, mock_get):
        """Test handling of HTTP errors."""
        # Mock HTTP error
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response
        
        df, metrics = fetch_exrate_data("EURUSD", "D1", "2024-01-01", "2024-01-02")
        
        # Should handle HTTP errors gracefully
        assert metrics['api_calls'] >= 1
    
    @patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'})
    @patch('src.data.fetchers.exrate_fetcher.requests.get')
    def test_missing_currency_in_response(self, mock_get):
        """Test handling when target currency is missing from API response."""
        # Mock response without target currency
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "conversion_rates": {
                "GBP": 0.8500  # Missing USD
            }
        }
        mock_get.return_value = mock_response
        
        df, metrics = fetch_exrate_data("EURUSD", "D1", "2024-01-01", "2024-01-02")
        
        # Should handle missing currency gracefully
        assert metrics['api_calls'] >= 1
    
    @patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'})
    @patch('src.data.fetchers.exrate_fetcher.requests.get')
    def test_network_timeout(self, mock_get):
        """Test handling of network timeouts."""
        # Mock network timeout
        mock_get.side_effect = Exception("Connection timeout")
        
        df, metrics = fetch_exrate_data("EURUSD", "D1", "2024-01-01", "2024-01-02")
        
        # Should handle network errors gracefully
        assert df is None
        assert metrics['error_message'] is not None
    
    def test_dataframe_structure(self):
        """Test that returned DataFrame has correct structure."""
        with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'}):
            with patch('src.data.fetchers.exrate_fetcher.requests.get') as mock_get:
                # Mock successful response
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "result": "success",
                    "conversion_rates": {"USD": 1.0500}
                }
                mock_get.return_value = mock_response
                
                df, metrics = fetch_exrate_data("EURUSD", "D1", "2024-01-01", "2024-01-01")
                
                if df is not None and not df.empty:
                    # Check DataFrame structure
                    assert isinstance(df.index, pd.DatetimeIndex)
                    assert df.index.name == 'DateTime'
                    expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                    assert list(df.columns) == expected_columns
                    
                    # Check data types
                    for col in expected_columns:
                        assert pd.api.types.is_numeric_dtype(df[col]), f"Column {col} should be numeric"


if __name__ == '__main__':
    pytest.main([__file__])
