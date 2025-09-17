# -*- coding: utf-8 -*-
"""
Real Exchange APIs Integration for NeoZork Interactive ML Trading Strategy Development.

This module provides real API integrations with major cryptocurrency exchanges.
"""

import requests
import time
import hmac
import hashlib
import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExchangeType(Enum):
    """Exchange types."""
    BINANCE = "binance"
    BYBIT = "bybit"
    KRAKEN = "kraken"
    COINBASE = "coinbase"

@dataclass
class APIKey:
    """API key configuration."""
    api_key: str
    secret_key: str
    passphrase: Optional[str] = None  # For some exchanges like Coinbase
    sandbox: bool = True  # Use sandbox/testnet by default

@dataclass
class OrderBook:
    """Order book data structure."""
    symbol: str
    bids: List[List[float]]  # [[price, quantity], ...]
    asks: List[List[float]]  # [[price, quantity], ...]
    timestamp: datetime

@dataclass
class Trade:
    """Trade data structure."""
    symbol: str
    price: float
    quantity: float
    side: str  # 'buy' or 'sell'
    timestamp: datetime
    trade_id: str

@dataclass
class Kline:
    """Kline/Candlestick data structure."""
    symbol: str
    open_time: datetime
    close_time: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    quote_volume: float
    trades_count: int
    timestamp: datetime

class BaseExchangeAPI:
    """Base class for exchange API implementations."""
    
    def __init__(self, api_key: APIKey, exchange_type: ExchangeType):
        self.api_key = api_key
        self.exchange_type = exchange_type
        self.base_url = self._get_base_url()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NeoZork-Trading-System/1.0',
            'Content-Type': 'application/json'
        })
    
    def _get_base_url(self) -> str:
        """Get base URL for the exchange."""
        if self.exchange_type == ExchangeType.BINANCE:
            return "https://testnet.binance.vision" if self.api_key.sandbox else "https://api.binance.com"
        elif self.exchange_type == ExchangeType.BYBIT:
            return "https://api-testnet.bybit.com" if self.api_key.sandbox else "https://api.bybit.com"
        elif self.exchange_type == ExchangeType.KRAKEN:
            return "https://api.kraken.com"
        elif self.exchange_type == ExchangeType.COINBASE:
            return "https://api-public.sandbox.exchange.coinbase.com" if self.api_key.sandbox else "https://api.exchange.coinbase.com"
        else:
            raise ValueError(f"Unsupported exchange type: {self.exchange_type}")
    
    def _generate_signature(self, query_string: str) -> str:
        """Generate API signature for authentication."""
        return hmac.new(
            self.api_key.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _make_request(self, method: str, endpoint: str, params: Dict[str, Any] = None, 
                     signed: bool = False) -> Dict[str, Any]:
        """Make authenticated request to exchange API."""
        url = f"{self.base_url}{endpoint}"
        
        if params is None:
            params = {}
        
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
            params['signature'] = self._generate_signature(query_string)
            params['apiKey'] = self.api_key.api_key
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=10)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=params, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return {"error": str(e), "status": "error"}
    
    def get_server_time(self) -> Dict[str, Any]:
        """Get server time."""
        return self._make_request('GET', '/api/v3/time')
    
    def get_exchange_info(self) -> Dict[str, Any]:
        """Get exchange information."""
        return self._make_request('GET', '/api/v3/exchangeInfo')
    
    def get_order_book(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """Get order book for symbol."""
        params = {'symbol': symbol, 'limit': limit}
        return self._make_request('GET', '/api/v3/depth', params)
    
    def get_recent_trades(self, symbol: str, limit: int = 500) -> Dict[str, Any]:
        """Get recent trades for symbol."""
        params = {'symbol': symbol, 'limit': limit}
        return self._make_request('GET', '/api/v3/trades', params)
    
    def get_klines(self, symbol: str, interval: str, start_time: Optional[datetime] = None,
                   end_time: Optional[datetime] = None, limit: int = 500) -> Dict[str, Any]:
        """Get kline/candlestick data."""
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        
        if start_time:
            params['startTime'] = int(start_time.timestamp() * 1000)
        if end_time:
            params['endTime'] = int(end_time.timestamp() * 1000)
        
        return self._make_request('GET', '/api/v3/klines', params)
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information."""
        return self._make_request('GET', '/api/v3/account', signed=True)
    
    def get_open_orders(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get open orders."""
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self._make_request('GET', '/api/v3/openOrders', params, signed=True)

class BinanceAPI(BaseExchangeAPI):
    """Binance API implementation."""
    
    def __init__(self, api_key: APIKey):
        super().__init__(api_key, ExchangeType.BINANCE)
    
    def get_24hr_ticker(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get 24hr ticker price change statistics."""
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self._make_request('GET', '/api/v3/ticker/24hr', params)
    
    def get_price(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get symbol price ticker."""
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self._make_request('GET', '/api/v3/ticker/price', params)

class BybitAPI(BaseExchangeAPI):
    """Bybit API implementation."""
    
    def __init__(self, api_key: APIKey):
        super().__init__(api_key, ExchangeType.BYBIT)
        # Bybit uses different endpoints
        self.base_url = "https://api-testnet.bybit.com" if self.api_key.sandbox else "https://api.bybit.com"
    
    def get_server_time(self) -> Dict[str, Any]:
        """Get server time."""
        return self._make_request('GET', '/v2/public/time')
    
    def get_symbols(self) -> Dict[str, Any]:
        """Get trading symbols."""
        return self._make_request('GET', '/v2/public/symbols')
    
    def get_order_book(self, symbol: str) -> Dict[str, Any]:
        """Get order book for symbol."""
        params = {'symbol': symbol}
        return self._make_request('GET', '/v2/public/orderBook/L2', params)
    
    def get_klines(self, symbol: str, interval: str, from_time: Optional[datetime] = None,
                   limit: int = 200) -> Dict[str, Any]:
        """Get kline data."""
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        
        if from_time:
            params['from'] = int(from_time.timestamp())
        
        return self._make_request('GET', '/v2/public/kline/list', params)

class ExchangeAPIManager:
    """Manager for multiple exchange APIs."""
    
    def __init__(self):
        self.apis: Dict[ExchangeType, BaseExchangeAPI] = {}
        self.data_cache: Dict[str, Any] = {}
        self.cache_ttl = 60  # Cache TTL in seconds
    
    def add_exchange(self, exchange_type: ExchangeType, api_key: APIKey) -> bool:
        """Add exchange API."""
        try:
            if exchange_type == ExchangeType.BINANCE:
                api = BinanceAPI(api_key)
            elif exchange_type == ExchangeType.BYBIT:
                api = BybitAPI(api_key)
            else:
                logger.error(f"Unsupported exchange type: {exchange_type}")
                return False
            
            # Test connection
            server_time = api.get_server_time()
            if 'error' in server_time:
                logger.error(f"Failed to connect to {exchange_type.value}: {server_time['error']}")
                return False
            
            self.apis[exchange_type] = api
            logger.info(f"Successfully connected to {exchange_type.value}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add exchange {exchange_type.value}: {e}")
            return False
    
    def get_klines_data(self, symbol: str, interval: str, exchange_type: ExchangeType,
                       start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                       limit: int = 500) -> pd.DataFrame:
        """Get klines data as DataFrame."""
        if exchange_type not in self.apis:
            logger.error(f"Exchange {exchange_type.value} not available")
            return pd.DataFrame()
        
        api = self.apis[exchange_type]
        
        # Check cache first
        cache_key = f"{exchange_type.value}_{symbol}_{interval}_{start_time}_{end_time}_{limit}"
        if cache_key in self.data_cache:
            cached_data, cache_time = self.data_cache[cache_key]
            if time.time() - cache_time < self.cache_ttl:
                return cached_data
        
        try:
            response = api.get_klines(symbol, interval, start_time, end_time, limit)
            
            if 'error' in response:
                logger.error(f"Failed to get klines: {response['error']}")
                return pd.DataFrame()
            
            # Convert to DataFrame
            if exchange_type == ExchangeType.BINANCE:
                df = self._convert_binance_klines(response, symbol)
            elif exchange_type == ExchangeType.BYBIT:
                df = self._convert_bybit_klines(response, symbol)
            else:
                logger.error(f"Unsupported exchange for klines conversion: {exchange_type}")
                return pd.DataFrame()
            
            # Cache the data
            self.data_cache[cache_key] = (df, time.time())
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting klines data: {e}")
            return pd.DataFrame()
    
    def _convert_binance_klines(self, response: List, symbol: str) -> pd.DataFrame:
        """Convert Binance klines response to DataFrame."""
        if not response:
            return pd.DataFrame()
        
        data = []
        for kline in response:
            data.append({
                'symbol': symbol,
                'open_time': pd.to_datetime(kline[0], unit='ms'),
                'close_time': pd.to_datetime(kline[6], unit='ms'),
                'open': float(kline[1]),
                'high': float(kline[2]),
                'low': float(kline[3]),
                'close': float(kline[4]),
                'volume': float(kline[5]),
                'quote_volume': float(kline[7]),
                'trades_count': int(kline[8]),
                'timestamp': pd.to_datetime(kline[0], unit='ms')
            })
        
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        return df
    
    def _convert_bybit_klines(self, response: Dict, symbol: str) -> pd.DataFrame:
        """Convert Bybit klines response to DataFrame."""
        if 'result' not in response or not response['result']:
            return pd.DataFrame()
        
        data = []
        for kline in response['result']:
            data.append({
                'symbol': symbol,
                'open_time': pd.to_datetime(kline['open_time'], unit='s'),
                'close_time': pd.to_datetime(kline['open_time'] + kline['interval'], unit='s'),
                'open': float(kline['open']),
                'high': float(kline['high']),
                'low': float(kline['low']),
                'close': float(kline['close']),
                'volume': float(kline['volume']),
                'quote_volume': float(kline['turnover']),
                'trades_count': int(kline.get('trades', 0)),
                'timestamp': pd.to_datetime(kline['open_time'], unit='s')
            })
        
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        return df
    
    def get_multiple_exchange_data(self, symbol: str, interval: str, 
                                  start_time: Optional[datetime] = None,
                                  end_time: Optional[datetime] = None,
                                  limit: int = 500) -> Dict[ExchangeType, pd.DataFrame]:
        """Get klines data from multiple exchanges."""
        results = {}
        
        for exchange_type in self.apis.keys():
            df = self.get_klines_data(symbol, interval, exchange_type, start_time, end_time, limit)
            if not df.empty:
                results[exchange_type] = df
        
        return results
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get connection status for all exchanges."""
        status = {}
        
        for exchange_type, api in self.apis.items():
            try:
                server_time = api.get_server_time()
                if 'error' in server_time:
                    status[exchange_type.value] = {
                        'connected': False,
                        'error': server_time['error']
                    }
                else:
                    status[exchange_type.value] = {
                        'connected': True,
                        'server_time': server_time.get('serverTime', 'N/A')
                    }
            except Exception as e:
                status[exchange_type.value] = {
                    'connected': False,
                    'error': str(e)
                }
        
        return status

# Example usage and testing
def test_exchange_apis():
    """Test exchange APIs with demo data."""
    print("🧪 Testing Real Exchange APIs...")
    
    # Create API manager
    manager = ExchangeAPIManager()
    
    # Add exchanges (using demo API keys - replace with real ones for production)
    binance_key = APIKey(
        api_key="demo_binance_api_key",
        secret_key="demo_binance_secret_key",
        sandbox=True
    )
    
    bybit_key = APIKey(
        api_key="demo_bybit_api_key",
        secret_key="demo_bybit_secret_key",
        sandbox=True
    )
    
    # Add exchanges
    binance_added = manager.add_exchange(ExchangeType.BINANCE, binance_key)
    bybit_added = manager.add_exchange(ExchangeType.BYBIT, bybit_key)
    
    print(f"  • Binance API: {'✅ Connected' if binance_added else '❌ Failed'}")
    print(f"  • Bybit API: {'✅ Connected' if bybit_added else '❌ Failed'}")
    
    # Get connection status
    status = manager.get_connection_status()
    print(f"  • Connection Status: {status}")
    
    # Test data retrieval (will fail with demo keys, but shows the structure)
    if binance_added:
        try:
            df = manager.get_klines_data("BTCUSDT", "1h", ExchangeType.BINANCE, limit=10)
            print(f"  • Binance BTCUSDT data: {len(df)} rows")
        except Exception as e:
            print(f"  • Binance data test: Expected error with demo keys - {e}")
    
    if bybit_added:
        try:
            df = manager.get_klines_data("BTCUSDT", "1h", ExchangeType.BYBIT, limit=10)
            print(f"  • Bybit BTCUSDT data: {len(df)} rows")
        except Exception as e:
            print(f"  • Bybit data test: Expected error with demo keys - {e}")
    
    print("✅ Exchange APIs test completed!")
    
    return manager

if __name__ == "__main__":
    test_exchange_apis()
