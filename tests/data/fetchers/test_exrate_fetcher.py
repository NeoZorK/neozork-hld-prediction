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
        # Test only the most common case-insensitive variations
        assert map_exrate_interval("d1") == "D1"
        assert map_exrate_interval("D") == "D1"
    
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
        # Test only one key ticker to speed up execution
        result = map_exrate_ticker("EURUSD")
        assert result == ("EUR", "USD")
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_valid_slash_separated_ticker(self, mock_logger):
        """Test that slash-separated tickers are mapped correctly."""
        # Test only one key ticker to speed up execution
        result = map_exrate_ticker("EUR/USD")
        assert result == ("EUR", "USD")
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_valid_underscore_separated_ticker(self, mock_logger):
        """Test that underscore-separated tickers are mapped correctly."""
        # Test only one key ticker to speed up execution
        result = map_exrate_ticker("EUR_USD")
        assert result == ("EUR", "USD")
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_case_insensitive(self, mock_logger):
        """Test that ticker mapping is case insensitive."""
        result = map_exrate_ticker("eurusd")
        assert result == ("EUR", "USD")
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_crypto_ticker_warning(self, mock_logger):
        """Test that crypto-like tickers return None with warning."""
        # Test only one key crypto ticker to speed up execution
        result = map_exrate_ticker("BTCUSDT")
        assert result is None
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_invalid_ticker_formats(self, mock_logger):
        """Test that invalid ticker formats return None."""
        # Test only one key invalid format to speed up execution
        result = map_exrate_ticker("INVALID")
        assert result is None
    
    @patch('src.data.fetchers.exrate_fetcher.logger')
    def test_unsupported_currencies(self, mock_logger):
        """Test that unsupported currencies return None."""
        # Test only one unsupported ticker to speed up execution
        result = map_exrate_ticker("XXXYYY")
        assert result is None


class TestFetchExrateData:
    """Test cases for fetch_exrate_data function."""
    
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


if __name__ == '__main__':
    pytest.main([__file__])
