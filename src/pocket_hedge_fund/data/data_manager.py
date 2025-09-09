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
from binance.client import Client
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class DataManager:
    """Manages data from various sources for the Pocket Hedge Fund."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize DataManager with configuration."""
        self.config = config or {}
        self.binance_client = None
        self.data_cache = {}
        self._initialize_binance()
        
    def _initialize_binance(self):
        """Initialize Binance client if API keys are available."""
        try:
            api_key = os.getenv('BINANCE_API_KEY')
            api_secret = os.getenv('BINANCE_API_SECRET')
            
            if api_key and api_secret:
                self.binance_client = Client(api_key, api_secret)
                logger.info("Binance client initialized successfully")
            else:
                logger.warning("Binance API keys not found, using public endpoints only")
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {e}")
    
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
    
    async def get_binance_data(self, symbol: str, interval: str = "1d", limit: int = 1000) -> pd.DataFrame:
        """Get data from Binance."""
        try:
            cache_key = f"binance_{symbol}_{interval}_{limit}"
            
            if cache_key in self.data_cache:
                logger.info(f"Returning cached Binance data for {symbol}")
                return self.data_cache[cache_key]
            
            logger.info(f"Fetching Binance data for {symbol}")
            
            if self.binance_client:
                # Use authenticated client
                klines = self.binance_client.get_klines(
                    symbol=symbol,
                    interval=interval,
                    limit=limit
                )
            else:
                # Use public client
                client = Client()
                klines = client.get_klines(
                    symbol=symbol,
                    interval=interval,
                    limit=limit
                )
            
            # Convert to DataFrame
            data = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            # Convert data types
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
            data['open'] = data['open'].astype(float)
            data['high'] = data['high'].astype(float)
            data['low'] = data['low'].astype(float)
            data['close'] = data['close'].astype(float)
            data['volume'] = data['volume'].astype(float)
            
            # Set timestamp as index
            data.set_index('timestamp', inplace=True)
            
            # Clean and standardize data
            data = self._clean_data(data)
            self.data_cache[cache_key] = data
            
            logger.info(f"Successfully fetched {len(data)} records for {symbol}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching Binance data for {symbol}: {e}")
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
    
    async def get_market_data(self, symbols: List[str], source: str = "yahoo", **kwargs) -> Dict[str, pd.DataFrame]:
        """Get market data for multiple symbols."""
        try:
            results = {}
            
            for symbol in symbols:
                try:
                    if source == "yahoo":
                        data = await self.get_yahoo_data(symbol, **kwargs)
                    elif source == "binance":
                        data = await self.get_binance_data(symbol, **kwargs)
                    elif source == "local":
                        data = await self.get_local_data(symbol, **kwargs)
                    else:
                        raise ValueError(f"Unsupported data source: {source}")
                    
                    results[symbol] = data
                    
                except Exception as e:
                    logger.error(f"Failed to fetch data for {symbol}: {e}")
                    results[symbol] = None
            
            return results
            
        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            raise
    
    async def get_available_symbols(self, source: str = "yahoo") -> List[str]:
        """Get list of available symbols from data source."""
        try:
            if source == "yahoo":
                # Common symbols for demonstration
                return [
                    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
                    "BTC-USD", "ETH-USD", "EURUSD=X", "GBPUSD=X",
                    "^GSPC", "^IXIC", "^DJI"
                ]
            elif source == "binance":
                if self.binance_client:
                    exchange_info = self.binance_client.get_exchange_info()
                    return [symbol['symbol'] for symbol in exchange_info['symbols']]
                else:
                    # Common crypto pairs
                    return [
                        "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT",
                        "XRPUSDT", "SOLUSDT", "DOTUSDT", "DOGEUSDT"
                    ]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting available symbols: {e}")
            return []
    
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
