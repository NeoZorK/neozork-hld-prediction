"""
Unit tests for data sources in data module.

This module tests the data source implementations.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from src.data.sources.base import BaseDataSource, TimeSeriesDataSource, FinancialDataSource


class MockDataSource(BaseDataSource):
    """Mock data source for testing."""
    
    def fetch(self, **kwargs):
        """Mock fetch implementation."""
        self.fetch_count += 1
        self.last_fetch = datetime.now()
        
        # Return mock data
        data = pd.DataFrame({
            'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H'),
            'open': np.random.randn(100),
            'high': np.random.randn(100),
            'low': np.random.randn(100),
            'close': np.random.randn(100),
            'volume': np.random.randint(1000, 10000, 100)
        })
        
        return data
    
    def is_available(self):
        """Mock availability check."""
        return True
    
    def get_metadata(self):
        """Mock metadata."""
        return {
            "name": self.name,
            "type": "mock",
            "last_update": self.last_fetch
        }


class MockTimeSeriesDataSource(TimeSeriesDataSource):
    """Mock time series data source for testing."""
    
    def fetch(self, **kwargs):
        """Mock fetch implementation."""
        self.fetch_count += 1
        self.last_fetch = datetime.now()
        
        # Return mock time series data
        data = pd.DataFrame({
            'timestamp': pd.date_range(start='2023-01-01', periods=100, freq=self.timeframe),
            'value': np.random.randn(100)
        })
        
        return data
    
    def is_available(self):
        """Mock availability check."""
        return True
    
    def get_metadata(self):
        """Mock metadata."""
        return {
            "name": self.name,
            "type": "time_series",
            "timeframe": self.timeframe,
            "symbol": self.symbol
        }


class MockFinancialDataSource(FinancialDataSource):
    """Mock financial data source for testing."""
    
    def fetch(self, **kwargs):
        """Mock fetch implementation."""
        self.fetch_count += 1
        self.last_fetch = datetime.now()
        
        # Return mock OHLCV data
        data = pd.DataFrame({
            'timestamp': pd.date_range(start='2023-01-01', periods=100, freq=self.timeframe),
            'open': np.random.randn(100),
            'high': np.random.randn(100),
            'low': np.random.randn(100),
            'close': np.random.randn(100),
            'volume': np.random.randint(1000, 10000, 100)
        })
        
        return data
    
    def is_available(self):
        """Mock availability check."""
        return True
    
    def get_metadata(self):
        """Mock metadata."""
        return {
            "name": self.name,
            "type": "financial",
            "timeframe": self.timeframe,
            "symbol": self.symbol,
            "currency": self.currency,
            "exchange": self.exchange
        }


class TestBaseDataSource:
    """Test cases for BaseDataSource class."""
    
    def test_init(self):
        """Test BaseDataSource initialization."""
        source = MockDataSource("test_source")
        
        assert source.name == "test_source"
        assert source.config == {}
        assert source.last_fetch is None
        assert source.fetch_count == 0
        assert source.error_count == 0
    
    def test_init_with_config(self):
        """Test BaseDataSource initialization with config."""
        config = {"param1": "value1", "param2": 42}
        source = MockDataSource("test_source", config)
        
        assert source.config == config
    
    def test_fetch(self):
        """Test data fetching."""
        source = MockDataSource("test_source")
        
        data = source.fetch()
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) == 100
        assert source.fetch_count == 1
        assert source.last_fetch is not None
    
    def test_is_available(self):
        """Test availability check."""
        source = MockDataSource("test_source")
        
        assert source.is_available() is True
    
    def test_get_metadata(self):
        """Test metadata retrieval."""
        source = MockDataSource("test_source")
        
        metadata = source.get_metadata()
        
        assert isinstance(metadata, dict)
        assert metadata["name"] == "test_source"
        assert metadata["type"] == "mock"
    
    def test_get_status(self):
        """Test status retrieval."""
        source = MockDataSource("test_source")
        
        # Fetch some data first
        source.fetch()
        
        status = source.get_status()
        
        assert isinstance(status, dict)
        assert status["name"] == "test_source"
        assert status["available"] is True
        assert status["fetch_count"] == 1
        assert status["error_count"] == 0
        assert status["error_rate"] == 0.0
    
    def test_error_handling(self):
        """Test error handling."""
        source = MockDataSource("test_source")
        
        # Simulate an error
        source.error_count = 1
        source.fetch_count = 2
        
        status = source.get_status()
        
        assert status["error_rate"] == 0.5


class TestTimeSeriesDataSource:
    """Test cases for TimeSeriesDataSource class."""
    
    def test_init(self):
        """Test TimeSeriesDataSource initialization."""
        source = MockTimeSeriesDataSource("test_source")
        
        assert source.name == "test_source"
        assert source.timeframe == "1H"
        assert source.symbol == ""
    
    def test_init_with_config(self):
        """Test TimeSeriesDataSource initialization with config."""
        config = {"timeframe": "1D", "symbol": "AAPL"}
        source = MockTimeSeriesDataSource("test_source", config)
        
        assert source.timeframe == "1D"
        assert source.symbol == "AAPL"
    
    def test_get_timeframe_info(self):
        """Test timeframe information retrieval."""
        source = MockTimeSeriesDataSource("test_source", {"timeframe": "4H", "symbol": "BTC"})
        
        info = source.get_timeframe_info()
        
        assert isinstance(info, dict)
        assert info["timeframe"] == "4H"
        assert info["symbol"] == "BTC"
        assert info["is_intraday"] is True
    
    def test_is_intraday_timeframe(self):
        """Test intraday timeframe detection."""
        # Test intraday timeframes
        source = MockTimeSeriesDataSource("test_source", {"timeframe": "1m"})
        assert source._is_intraday_timeframe() is True
        
        source = MockTimeSeriesDataSource("test_source", {"timeframe": "5m"})
        assert source._is_intraday_timeframe() is True
        
        source = MockTimeSeriesDataSource("test_source", {"timeframe": "1H"})
        assert source._is_intraday_timeframe() is True
        
        source = MockTimeSeriesDataSource("test_source", {"timeframe": "4H"})
        assert source._is_intraday_timeframe() is True
        
        # Test non-intraday timeframes
        source = MockTimeSeriesDataSource("test_source", {"timeframe": "1D"})
        assert source._is_intraday_timeframe() is False
        
        source = MockTimeSeriesDataSource("test_source", {"timeframe": "1W"})
        assert source._is_intraday_timeframe() is False
    
    def test_validate_timeframe(self):
        """Test timeframe validation."""
        source = MockTimeSeriesDataSource("test_source")
        
        # Valid timeframes
        assert source.validate_timeframe("1m") is True
        assert source.validate_timeframe("5m") is True
        assert source.validate_timeframe("15m") is True
        assert source.validate_timeframe("30m") is True
        assert source.validate_timeframe("1H") is True
        assert source.validate_timeframe("4H") is True
        assert source.validate_timeframe("1D") is True
        assert source.validate_timeframe("1W") is True
        assert source.validate_timeframe("1M") is True
        
        # Invalid timeframes
        assert source.validate_timeframe("2m") is False
        assert source.validate_timeframe("3H") is False
        assert source.validate_timeframe("2D") is False
        assert source.validate_timeframe("invalid") is False


class TestFinancialDataSource:
    """Test cases for FinancialDataSource class."""
    
    def test_init(self):
        """Test FinancialDataSource initialization."""
        source = MockFinancialDataSource("test_source")
        
        assert source.name == "test_source"
        assert source.timeframe == "1H"
        assert source.symbol == ""
        assert source.currency == "USD"
        assert source.exchange == ""
    
    def test_init_with_config(self):
        """Test FinancialDataSource initialization with config."""
        config = {
            "timeframe": "1D",
            "symbol": "AAPL",
            "currency": "EUR",
            "exchange": "NASDAQ"
        }
        source = MockFinancialDataSource("test_source", config)
        
        assert source.timeframe == "1D"
        assert source.symbol == "AAPL"
        assert source.currency == "EUR"
        assert source.exchange == "NASDAQ"
    
    def test_get_financial_info(self):
        """Test financial information retrieval."""
        config = {
            "timeframe": "4H",
            "symbol": "BTC",
            "currency": "USD",
            "exchange": "BINANCE"
        }
        source = MockFinancialDataSource("test_source", config)
        
        info = source.get_financial_info()
        
        assert isinstance(info, dict)
        assert info["timeframe"] == "4H"
        assert info["symbol"] == "BTC"
        assert info["currency"] == "USD"
        assert info["exchange"] == "BINANCE"
    
    def test_validate_symbol(self):
        """Test symbol validation."""
        source = MockFinancialDataSource("test_source")
        
        # Valid symbols
        assert source.validate_symbol("AAPL") is True
        assert source.validate_symbol("BTC") is True
        assert source.validate_symbol("EURUSD") is True
        assert source.validate_symbol("123") is True
        
        # Invalid symbols
        assert source.validate_symbol("") is False
        assert source.validate_symbol("AAPL-") is False
        assert source.validate_symbol("BTC/USD") is False
    
    def test_get_ohlcv_columns(self):
        """Test OHLCV column names."""
        source = MockFinancialDataSource("test_source")
        
        columns = source.get_ohlcv_columns()
        
        expected_columns = ["open", "high", "low", "close", "volume"]
        assert columns == expected_columns
    
    def test_validate_ohlcv_data(self):
        """Test OHLCV data validation."""
        source = MockFinancialDataSource("test_source")
        
        # Valid OHLCV data
        valid_data = pd.DataFrame({
            "open": [1.0, 2.0, 3.0],
            "high": [1.5, 2.5, 3.5],
            "low": [0.5, 1.5, 2.5],
            "close": [1.2, 2.2, 3.2],
            "volume": [100, 200, 300]
        })
        assert source.validate_ohlcv_data(valid_data) is True
        
        # Invalid OHLCV data - missing columns
        invalid_data = pd.DataFrame({
            "open": [1.0, 2.0, 3.0],
            "high": [1.5, 2.5, 3.5],
            "low": [0.5, 1.5, 2.5]
            # Missing close and volume
        })
        assert source.validate_ohlcv_data(invalid_data) is False
        
        # Invalid OHLCV data - wrong column names
        invalid_data = pd.DataFrame({
            "Open": [1.0, 2.0, 3.0],
            "High": [1.5, 2.5, 3.5],
            "Low": [0.5, 1.5, 2.5],
            "Close": [1.2, 2.2, 3.2],
            "Volume": [100, 200, 300]
        })
        assert source.validate_ohlcv_data(invalid_data) is False


class TestDataSourceIntegration:
    """Test cases for data source integration."""
    
    def test_data_source_hierarchy(self):
        """Test that data sources properly inherit from base classes."""
        # Check inheritance
        assert issubclass(TimeSeriesDataSource, BaseDataSource)
        assert issubclass(FinancialDataSource, TimeSeriesDataSource)
        
        # Check that they can be instantiated
        ts_source = MockTimeSeriesDataSource("test")
        fin_source = MockFinancialDataSource("test")
        
        assert isinstance(ts_source, BaseDataSource)
        assert isinstance(fin_source, TimeSeriesDataSource)
        assert isinstance(fin_source, BaseDataSource)
    
    def test_data_fetching_flow(self):
        """Test complete data fetching flow."""
        source = MockFinancialDataSource("test", {
            "timeframe": "1H",
            "symbol": "AAPL",
            "currency": "USD",
            "exchange": "NASDAQ"
        })
        
        # Check initial state
        assert source.fetch_count == 0
        assert source.last_fetch is None
        
        # Fetch data
        data = source.fetch()
        
        # Check state after fetch
        assert source.fetch_count == 1
        assert source.last_fetch is not None
        assert isinstance(data, pd.DataFrame)
        assert len(data) == 100
        
        # Check data structure
        expected_columns = ["timestamp", "open", "high", "low", "close", "volume"]
        for col in expected_columns:
            assert col in data.columns
    
    def test_error_tracking(self):
        """Test error tracking functionality."""
        source = MockDataSource("test")
        
        # Simulate multiple fetches with some errors
        source.fetch()  # Successful fetch
        source.fetch()  # Successful fetch
        source.error_count = 1  # Simulate one error
        
        status = source.get_status()
        
        assert status["fetch_count"] == 2
        assert status["error_count"] == 1
        assert status["error_rate"] == 0.5
