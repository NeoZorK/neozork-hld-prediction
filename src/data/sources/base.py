"""
Base data source classes for Neozork HLD Prediction system.

This module provides abstract base classes for data sources.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import pandas as pd
from datetime import datetime, timedelta
from ...core.base import BaseComponent
from ...core.interfaces import DataSource


class BaseDataSource(BaseComponent, DataSource):
    """Base class for all data sources."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.last_fetch = None
        self.fetch_count = 0
        self.error_count = 0
        
    @abstractmethod
    def fetch(self, **kwargs) -> Any:
        """Fetch data from source."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if data source is available."""
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the data source."""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the data source."""
        return {
            "name": self.name,
            "available": self.is_available(),
            "last_fetch": self.last_fetch,
            "fetch_count": self.fetch_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.fetch_count, 1)
        }


class TimeSeriesDataSource(BaseDataSource):
    """Base class for time series data sources."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.timeframe = config.get("timeframe", "1H")
        self.symbol = config.get("symbol", "")
        
    def get_timeframe_info(self) -> Dict[str, Any]:
        """Get information about the timeframe."""
        return {
            "timeframe": self.timeframe,
            "symbol": self.symbol,
            "is_intraday": self._is_intraday_timeframe()
        }
    
    def _is_intraday_timeframe(self) -> bool:
        """Check if timeframe is intraday."""
        intraday_timeframes = ["1m", "5m", "15m", "30m", "1H", "4H"]
        return self.timeframe in intraday_timeframes
    
    def validate_timeframe(self, timeframe: str) -> bool:
        """Validate if timeframe is supported."""
        supported_timeframes = ["1m", "5m", "15m", "30m", "1H", "4H", "1D", "1W", "1M"]
        return timeframe in supported_timeframes


class FinancialDataSource(TimeSeriesDataSource):
    """Base class for financial data sources."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.currency = config.get("currency", "USD")
        self.exchange = config.get("exchange", "")
        
    def get_financial_info(self) -> Dict[str, Any]:
        """Get financial information about the data source."""
        return {
            "currency": self.currency,
            "exchange": self.exchange,
            "symbol": self.symbol,
            "timeframe": self.timeframe
        }
    
    def validate_symbol(self, symbol: str) -> bool:
        """Validate if symbol is supported."""
        # Basic validation - can be overridden by subclasses
        return len(symbol) > 0 and symbol.isalnum()
    
    def get_ohlcv_columns(self) -> List[str]:
        """Get standard OHLCV column names."""
        return ["open", "high", "low", "close", "volume"]
    
    def validate_ohlcv_data(self, data: pd.DataFrame) -> bool:
        """Validate OHLCV data structure."""
        required_columns = self.get_ohlcv_columns()
        return all(col in data.columns for col in required_columns)
