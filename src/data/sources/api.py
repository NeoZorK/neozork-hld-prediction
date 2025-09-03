"""
API Data Source Implementation

This module provides API-based data source functionality for the Neozork HLD Prediction system.
"""

import pandas as pd
import requests
from typing import Dict, Any, Optional, Union
from datetime import datetime

from .base import BaseDataSource, TimeSeriesDataSource
from ...core.exceptions import DataError, ValidationError


class APIDataSource(BaseDataSource):
    """
    API-based data source implementation.
    
    Provides functionality to fetch data from REST APIs.
    """
    
    def __init__(self, base_url: str, config: Dict[str, Any]):
        """
        Initialize API data source.
        
        Args:
            base_url: Base URL for the API
            config: Configuration dictionary
        """
        super().__init__(f"api_source_{base_url.split('/')[-1]}", config)
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self) -> None:
        """Setup requests session with authentication and headers."""
        # Add API key if provided
        api_key = self.config.get("api_key")
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        
        # Add custom headers
        headers = self.config.get("headers", {})
        self.session.headers.update(headers)
        
        # Set timeout
        self.timeout = self.config.get("timeout", 30)
    
    def fetch_data(self, endpoint: str = "", **kwargs) -> pd.DataFrame:
        """
        Fetch data from API endpoint.
        
        Args:
            endpoint: API endpoint to fetch from
            **kwargs: Additional parameters for the API request
            
        Returns:
            DataFrame containing the API response data
            
        Raises:
            DataError: If API request fails or data is invalid
        """
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}" if endpoint else self.base_url
            
            response = self.session.get(url, params=kwargs, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Convert to DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict) and "data" in data:
                df = pd.DataFrame(data["data"])
            else:
                df = pd.DataFrame([data])
            
            if df.empty:
                raise DataError("API returned empty data")
            
            self.logger.info(f"Successfully fetched {len(df)} rows from API")
            return df
            
        except requests.exceptions.RequestException as e:
            raise DataError(f"API request failed: {e}")
        except ValueError as e:
            raise DataError(f"Invalid JSON response: {e}")
        except Exception as e:
            raise DataError(f"Unexpected error fetching API data: {e}")
    
    def is_available(self) -> bool:
        """
        Check if API is available.
        
        Returns:
            True if API is reachable, False otherwise
        """
        try:
            response = self.session.head(self.base_url, timeout=5)
            return response.status_code < 500
        except Exception:
            return False
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get API metadata.
        
        Returns:
            Dictionary containing API metadata
        """
        return {
            "type": "api",
            "base_url": self.base_url,
            "available": self.is_available(),
            "timeout": self.timeout,
            "has_auth": bool(self.config.get("api_key"))
        }


class YahooFinanceSource(TimeSeriesDataSource):
    """
    Yahoo Finance API data source.
    
    Specialized data source for fetching financial data from Yahoo Finance.
    """
    
    def __init__(self, symbol: str, config: Dict[str, Any]):
        """
        Initialize Yahoo Finance data source.
        
        Args:
            symbol: Financial instrument symbol (e.g., 'AAPL', 'EURUSD=X')
            config: Configuration dictionary
        """
        super().__init__(f"yahoo_finance_{symbol}", config)
        self.symbol = symbol.upper()
        self._validate_symbol()
    
    def _validate_symbol(self) -> None:
        """Validate the financial symbol."""
        if not self.symbol or not isinstance(self.symbol, str):
            raise ValidationError("Symbol must be a non-empty string")
        
        # Basic symbol validation
        if len(self.symbol) < 1 or len(self.symbol) > 10:
            raise ValidationError("Symbol length must be between 1 and 10 characters")
    
    def fetch_data(self, start_date: Optional[str] = None, 
                   end_date: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Fetch financial data from Yahoo Finance.
        
        Args:
            start_date: Start date for data retrieval (YYYY-MM-DD)
            end_date: End date for data retrieval (YYYY-MM-DD)
            **kwargs: Additional parameters
            
        Returns:
            DataFrame containing OHLCV data
            
        Raises:
            DataError: If data cannot be fetched
        """
        try:
            import yfinance as yf
            
            ticker = yf.Ticker(self.symbol)
            
            # Fetch historical data
            data = ticker.history(
                start=start_date,
                end=end_date,
                **kwargs
            )
            
            if data.empty:
                raise DataError(f"No data available for symbol {self.symbol}")
            
            # Standardize column names
            data.columns = data.columns.str.lower()
            
            # Validate OHLCV structure
            required_columns = ['open', 'high', 'low', 'close', 'volume']
            missing_columns = [col for col in required_columns if col not in data.columns]
            
            if missing_columns:
                raise DataError(f"Missing required columns: {missing_columns}")
            
            self.logger.info(f"Successfully fetched {len(data)} rows for {self.symbol}")
            return data
            
        except ImportError:
            raise DataError("yfinance package not installed. Install with: pip install yfinance")
        except Exception as e:
            raise DataError(f"Failed to fetch data from Yahoo Finance: {e}")
    
    def is_available(self) -> bool:
        """
        Check if Yahoo Finance is available.
        
        Returns:
            True if Yahoo Finance API is accessible, False otherwise
        """
        try:
            import yfinance as yf
            
            # Try to fetch basic info for a known symbol
            ticker = yf.Ticker("AAPL")
            info = ticker.info
            return info is not None and len(info) > 0
            
        except Exception:
            return False
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get Yahoo Finance source metadata.
        
        Returns:
            Dictionary containing source metadata
        """
        return {
            "type": "yahoo_finance",
            "symbol": self.symbol,
            "available": self.is_available(),
            "data_type": "financial_ohlcv"
        }


__all__ = ["CSVDataSource", "YahooFinanceSource"]
