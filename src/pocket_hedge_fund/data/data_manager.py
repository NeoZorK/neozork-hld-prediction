"""
Data Manager for Pocket Hedge Fund.

This module provides data integration with various sources including
Yahoo Finance, Binance, and local data files.
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import yfinance as yf
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class DataManager:
    """Manages data from various sources for the Pocket Hedge Fund."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize DataManager with configuration."""
        self.config = config or {}
        self.data_cache = {}
        
    async def get_yahoo_data(self, symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """Get data from Yahoo Finance."""
        try:
            cache_key = f"yahoo_{symbol}_{period}_{interval}"
            
            if cache_key in self.data_cache:
                logger.info(f"Returning cached data for {symbol}")
                return self.data_cache[cache_key]
            
            logger.info(f"Fetching Yahoo Finance data for {symbol}")
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                raise ValueError(f"No data found for symbol {symbol}")
            
            # Clean and standardize data
            data = self._clean_data(data)
            self.data_cache[cache_key] = data
            
            logger.info(f"Successfully fetched {len(data)} records for {symbol}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching Yahoo Finance data for {symbol}: {e}")
            raise
    
    async def get_local_data(self, file_path: str) -> pd.DataFrame:
        """Get data from local files."""
        try:
            cache_key = f"local_{file_path}"
            
            if cache_key in self.data_cache:
                logger.info(f"Returning cached local data from {file_path}")
                return self.data_cache[cache_key]
            
            logger.info(f"Loading local data from {file_path}")
            
            # Determine file type and load accordingly
            file_path = Path(file_path)
            
            if file_path.suffix == '.parquet':
                data = pd.read_parquet(file_path)
            elif file_path.suffix == '.csv':
                data = pd.read_csv(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
            # Clean and standardize data
            data = self._clean_data(data)
            self.data_cache[cache_key] = data
            
            logger.info(f"Successfully loaded {len(data)} records from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading local data from {file_path}: {e}")
            raise
    
    def _clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize data format."""
        try:
            # Ensure we have the required columns
            required_columns = ['open', 'high', 'low', 'close', 'volume']
            
            # Map common column names
            column_mapping = {
                'Open': 'open',
                'High': 'high', 
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume',
                'Adj Close': 'adj_close'
            }
            
            data = data.rename(columns=column_mapping)
            
            # Check if we have required columns
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                logger.warning(f"Missing columns: {missing_columns}")
            
            # Remove rows with NaN values
            data = data.dropna()
            
            # Ensure numeric types
            for col in ['open', 'high', 'low', 'close', 'volume']:
                if col in data.columns:
                    data[col] = pd.to_numeric(data[col], errors='coerce')
            
            # Remove any remaining NaN values
            data = data.dropna()
            
            # Sort by index (timestamp)
            data = data.sort_index()
            
            return data
            
        except Exception as e:
            logger.error(f"Error cleaning data: {e}")
            raise
    
    def clear_cache(self):
        """Clear data cache."""
        self.data_cache.clear()
        logger.info("Data cache cleared")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about cached data."""
        return {
            "cache_size": len(self.data_cache),
            "cached_symbols": list(self.data_cache.keys()),
            "memory_usage": sum(
                data.memory_usage(deep=True).sum() 
                for data in self.data_cache.values() 
                if isinstance(data, pd.DataFrame)
            )
        }
