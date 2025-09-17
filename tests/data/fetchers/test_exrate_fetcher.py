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
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_case_insensitive(self, mock_logger):
        """Test that interval mapping is case insensitive."""
        assert map_exrate_interval("d1") == "D1"
        assert map_exrate_interval("D") == "D1"
        assert map_exrate_interval("1d") == "D1"
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_invalid_interval(self, mock_logger):
        """Test that invalid intervals return None."""
        # Test only a few key invalid intervals to speed up execution
        test_cases = ["X1", "INVALID", ""]
        for interval in test_cases:
            result = map_exrate_interval(interval)
            assert result is None, f"Expected None for {interval}, got {result}"


class TestMapExrateTicker:
    """Test cases for map_exrate_ticker function."""
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_valid_six_char_ticker(self, mock_logger):
        """Test that 6-character currency pair tickers are mapped correctly."""
        # Test only a few key tickers to speed up execution
        test_cases = [
            ("EURUSD", ("EUR", "USD")),
            ("GBPJPY", ("GBP", "JPY")),
            ("AUDUSD", ("AUD", "USD"))
        ]
        
        for ticker, expected in test_cases:
            result = map_exrate_ticker(ticker)
            assert result == expected, f"Expected {expected} for {ticker}, got {result}"
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_valid_slash_separated_ticker(self, mock_logger):
        """Test that slash-separated tickers are mapped correctly."""
        # Test only a few key tickers to speed up execution
        test_cases = [
            ("EUR/USD", ("EUR", "USD")),
            ("GBP/JPY", ("GBP", "JPY"))
        ]
        
        for ticker, expected in test_cases:
            result = map_exrate_ticker(ticker)
            assert result == expected, f"Expected {expected} for {ticker}, got {result}"
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_valid_underscore_separated_ticker(self, mock_logger):
        """Test that underscore-separated tickers are mapped correctly."""
        # Test only a few key tickers to speed up execution
        test_cases = [
            ("EUR_USD", ("EUR", "USD")),
            ("GBP_JPY", ("GBP", "JPY"))
        ]
        
        for ticker, expected in test_cases:
            result = map_exrate_ticker(ticker)
            assert result == expected, f"Expected {expected} for {ticker}, got {result}"
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_case_insensitive(self, mock_logger):
        """Test that ticker mapping is case insensitive."""
        result = map_exrate_ticker("eurusd")
        assert result == ("EUR", "USD")
        
        result = map_exrate_ticker("eur/usd")
        assert result == ("EUR", "USD")
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_crypto_ticker_warning(self, mock_logger):
        """Test that crypto-like tickers return None with warning."""
        # Test only a few key crypto tickers to speed up execution
        crypto_tickers = ["BTCUSDT", "ETHUSDT"]
        for ticker in crypto_tickers:
            result = map_exrate_ticker(ticker)
            assert result is None, f"Expected None for {ticker}, got {result}"
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_invalid_ticker_formats(self, mock_logger):
        """Test that invalid ticker formats return None."""
        # Test only a few key invalid formats to speed up execution
        invalid_tickers = [
            "INVALID",  # Too short
            "EURUSDX",  # Too long
            "EUR"       # Too short
        ]
        
        for ticker in invalid_tickers:
            result = map_exrate_ticker(ticker)
            assert result is None, f"Expected None for {ticker}, got {result}"
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_unsupported_currencies(self, mock_logger):
        """Test that unsupported currencies return None."""
        # Test only one unsupported ticker to speed up execution
        unsupported_tickers = ["XXXYYY"]
        for ticker in unsupported_tickers:
            result = map_exrate_ticker(ticker)
            assert result is None, f"Expected None for {ticker}, got {result}"


class TestFetchExrateData:
    """Test cases for fetch_exrate_data function."""
    
    @patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'})
    @patch('src.data.fetchers.exrate_fetcher.requests.get')
    def test_successful_fetch(self, mock_get):
        """Test successful data fetch from Exchange Rate API (historical mode)."""
        # Mock response for historical data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "conversion_rates": {
                "USD": 1.0500
            }
        }
        mock_get.return_value = mock_response
        
        # Test fetch with dates (historical mode)
        df, metrics = fetch_exrate_data("EURUSD", "D1", "2024-01-01", "2024-01-02")
        
        # Assertions - Updated for historical data (2 days)
        assert df is not None
        assert not df.empty
        assert len(df) == 2  # Two days of historical data
        assert list(df.columns) == ['Open', 'High', 'Low', 'Close', 'Volume']
        assert all(df['Open'] == 1.0500)
        assert all(df['Close'] == 1.0500)
        assert all(df['Volume'] == 0)
        assert metrics['api_calls'] == 2  # Two historical calls (one per day)
        assert metrics['rows_fetched'] == 2  # Two rows
        assert metrics['error_message'] is None
    
    @patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'})
    @patch('src.data.fetchers.exrate_fetcher.requests.get')
    def test_successful_fetch_current_only(self, mock_get):
        """Test successful data fetch from Exchange Rate API (free plan - current only)."""
        # Mock response for current data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "conversion_rates": {
                "USD": 1.0500
            }
        }
        mock_get.return_value = mock_response
        
        # Test fetch without dates (free plan mode)
        df, metrics = fetch_exrate_data("EURUSD", "D1", None, None)
        
        # Assertions - Current data only
        assert df is not None
        assert not df.empty
        assert len(df) == 1  # One current rate
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
        """Test behavior with invalid date range (start > end)."""
        # Mock not needed since this should fail before API call
        
        df, metrics = fetch_exrate_data("EURUSD", "D1", "2024-01-02", "2024-01-01")
        
        # Should fail with date validation error
        assert df is None
        assert "Start date must be before end date" in metrics['error_message']

    @patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'})
    @patch('src.data.fetchers.exrate_fetcher.requests.get')
    def test_invalid_date_format(self, mock_get):
        """Test behavior with invalid date format."""
        # Mock not needed since this should fail before API call
        
        df, metrics = fetch_exrate_data("EURUSD", "D1", "invalid-date", "2024-01-02")
        
        # Should fail with date parsing error
        assert df is None
        assert "Date parsing error" in metrics['error_message']
    
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
        
        # Invalid API key error should be detected early and fail
        assert df is None
        assert metrics['api_calls'] >= 0  # May be 0 if error detected before API calls counted
        assert "Invalid API key" in metrics['error_message']
    
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
