# -*- coding: utf-8 -*-
"""
Live Data Manager for NeoZork Interactive ML Trading Strategy Development.

This module provides real-time data management for live trading and backtesting.
"""

import asyncio
import aiohttp
import time
import logging
import threading
import queue
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import pandas as pd
import numpy as np
import json
import ssl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataSource(Enum):
    """Data source types."""
    BINANCE = "binance"
    BYBIT = "bybit"
    COINBASE = "coinbase"
    KRAKEN = "kraken"
    YAHOO_FINANCE = "yahoo_finance"
    ALPHA_VANTAGE = "alpha_vantage"

class DataType(Enum):
    """Data types."""
    OHLCV = "ohlcv"
    ORDER_BOOK = "order_book"
    TRADES = "trades"
    TICKER = "ticker"
    FUNDING_RATE = "funding_rate"

@dataclass
class DataConfig:
    """Data configuration."""
    source: DataSource
    symbol: str
    interval: str
    data_type: DataType
    limit: int = 1000
    update_interval: int = 60  # seconds
    retry_attempts: int = 3
    timeout: int = 30

class LiveDataManager:
    """Live data manager for real-time market data."""
    
    def __init__(self):
        self.data_sources = {}
        self.data_cache = {}
        self.subscribers = {}
        self.is_running = False
        self.data_thread = None
        self.update_queue = queue.Queue()
        
        # API endpoints
        self.api_endpoints = {
            DataSource.BINANCE: {
                'base_url': 'https://api.binance.com',
                'testnet_url': 'https://testnet.binance.vision',
                'endpoints': {
                    DataType.OHLCV: '/api/v3/klines',
                    DataType.TICKER: '/api/v3/ticker/24hr',
                    DataType.ORDER_BOOK: '/api/v3/depth',
                    DataType.TRADES: '/api/v3/trades'
                }
            },
            DataSource.BYBIT: {
                'base_url': 'https://api.bybit.com',
                'testnet_url': 'https://api-testnet.bybit.com',
                'endpoints': {
                    DataType.OHLCV: '/v5/market/kline',
                    DataType.TICKER: '/v5/market/tickers',
                    DataType.ORDER_BOOK: '/v5/market/orderbook',
                    DataType.TRADES: '/v5/market/recent-trade'
                }
            }
        }
        
    async def initialize_data_source(self, source: DataSource, testnet: bool = True) -> Dict[str, Any]:
        """Initialize a data source."""
        try:
            config = self.api_endpoints.get(source)
            if not config:
                return {
                    'status': 'error',
                    'message': f'Data source {source.value} not supported'
                }
            
            base_url = config['testnet_url'] if testnet else config['base_url']
            
            # Test connection with SSL context
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            
            async with aiohttp.ClientSession(connector=connector) as session:
                test_url = f"{base_url}/api/v3/ping" if source == DataSource.BINANCE else f"{base_url}/v5/market/time"
                
                async with session.get(test_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        self.data_sources[source] = {
                            'base_url': base_url,
                            'endpoints': config['endpoints'],
                            'testnet': testnet,
                            'connected': True,
                            'last_ping': time.time()
                        }
                        
                        logger.info(f"Data source {source.value} initialized successfully")
                        
                        return {
                            'status': 'success',
                            'source': source.value,
                            'testnet': testnet,
                            'message': f'Data source {source.value} initialized'
                        }
                    else:
                        return {
                            'status': 'error',
                            'message': f'Failed to connect to {source.value}: HTTP {response.status}'
                        }
                        
        except Exception as e:
            logger.error(f"Failed to initialize {source.value}: {e}")
            return {
                'status': 'error',
                'message': f'Failed to initialize {source.value}: {str(e)}'
            }
    
    async def get_historical_data(self, config: DataConfig, 
                                 start_time: Optional[datetime] = None,
                                 end_time: Optional[datetime] = None) -> Dict[str, Any]:
        """Get historical data from a source."""
        try:
            if config.source not in self.data_sources:
                return {
                    'status': 'error',
                    'message': f'Data source {config.source.value} not initialized'
                }
            
            source_config = self.data_sources[config.source]
            endpoint = source_config['endpoints'].get(config.data_type)
            
            if not endpoint:
                return {
                    'status': 'error',
                    'message': f'Data type {config.data_type.value} not supported for {config.source.value}'
                }
            
            # Build request parameters
            params = self._build_request_params(config, start_time, end_time)
            
            # Make request with SSL context
            url = f"{source_config['base_url']}{endpoint}"
            
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=config.timeout)) as response:
                    if response.status == 200:
                        data = await response.json()
                        processed_data = self._process_data(data, config)
                        
                        # Cache data
                        cache_key = f"{config.source.value}_{config.symbol}_{config.interval}_{config.data_type.value}"
                        self.data_cache[cache_key] = {
                            'data': processed_data,
                            'timestamp': time.time(),
                            'config': config
                        }
                        
                        return {
                            'status': 'success',
                            'data': processed_data,
                            'source': config.source.value,
                            'symbol': config.symbol,
                            'data_type': config.data_type.value,
                            'rows': len(processed_data) if isinstance(processed_data, (list, pd.DataFrame)) else 1,
                            'message': f'Historical data retrieved for {config.symbol}'
                        }
                    else:
                        return {
                            'status': 'error',
                            'message': f'Failed to get data: HTTP {response.status}'
                        }
                        
        except Exception as e:
            logger.error(f"Failed to get historical data: {e}")
            return {
                'status': 'error',
                'message': f'Failed to get historical data: {str(e)}'
            }
    
    def _build_request_params(self, config: DataConfig, 
                            start_time: Optional[datetime] = None,
                            end_time: Optional[datetime] = None) -> Dict[str, Any]:
        """Build request parameters based on data source."""
        params = {}
        
        if config.source == DataSource.BINANCE:
            params['symbol'] = config.symbol
            params['interval'] = config.interval
            params['limit'] = config.limit
            
            if start_time:
                params['startTime'] = int(start_time.timestamp() * 1000)
            if end_time:
                params['endTime'] = int(end_time.timestamp() * 1000)
                
        elif config.source == DataSource.BYBIT:
            params['category'] = 'spot'  # or 'linear' for futures
            params['symbol'] = config.symbol
            params['interval'] = config.interval
            params['limit'] = config.limit
            
            if start_time:
                params['start'] = int(start_time.timestamp() * 1000)
            if end_time:
                params['end'] = int(end_time.timestamp() * 1000)
        
        return params
    
    def _process_data(self, raw_data: Any, config: DataConfig) -> pd.DataFrame:
        """Process raw data based on source and type."""
        try:
            if config.source == DataSource.BINANCE:
                if config.data_type == DataType.OHLCV:
                    # Process klines data
                    df = pd.DataFrame(raw_data, columns=[
                        'open_time', 'open', 'high', 'low', 'close', 'volume',
                        'close_time', 'quote_volume', 'trades_count',
                        'taker_buy_volume', 'taker_buy_quote_volume', 'ignore'
                    ])
                    
                    # Convert timestamps
                    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
                    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
                    
                    # Convert numeric columns
                    numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'quote_volume', 'trades_count']
                    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
                    
                    # Set index
                    df.set_index('open_time', inplace=True)
                    
                    return df[['open', 'high', 'low', 'close', 'volume']]
                
                elif config.data_type == DataType.TICKER:
                    # Process ticker data
                    return pd.DataFrame([raw_data])
                
            elif config.source == DataSource.BYBIT:
                if config.data_type == DataType.OHLCV:
                    # Process Bybit klines data
                    if 'result' in raw_data and 'list' in raw_data['result']:
                        klines = raw_data['result']['list']
                        df = pd.DataFrame(klines, columns=[
                            'start_time', 'open', 'high', 'low', 'close', 'volume', 'turnover'
                        ])
                        
                        # Convert timestamps
                        df['start_time'] = pd.to_datetime(df['start_time'], unit='ms')
                        
                        # Convert numeric columns
                        numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'turnover']
                        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
                        
                        # Set index
                        df.set_index('start_time', inplace=True)
                        
                        return df[['open', 'high', 'low', 'close', 'volume']]
                
            # Fallback: return raw data
            return pd.DataFrame([raw_data]) if isinstance(raw_data, dict) else pd.DataFrame(raw_data)
            
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            return pd.DataFrame()
    
    def subscribe_to_data(self, config: DataConfig, callback: Callable):
        """Subscribe to real-time data updates."""
        subscription_key = f"{config.source.value}_{config.symbol}_{config.interval}_{config.data_type.value}"
        
        if subscription_key not in self.subscribers:
            self.subscribers[subscription_key] = []
        
        self.subscribers[subscription_key].append({
            'callback': callback,
            'config': config,
            'last_update': time.time()
        })
        
        logger.info(f"Subscribed to {subscription_key}")
    
    def unsubscribe_from_data(self, config: DataConfig, callback: Callable):
        """Unsubscribe from data updates."""
        subscription_key = f"{config.source.value}_{config.symbol}_{config.interval}_{config.data_type.value}"
        
        if subscription_key in self.subscribers:
            self.subscribers[subscription_key] = [
                sub for sub in self.subscribers[subscription_key] 
                if sub['callback'] != callback
            ]
            
            if not self.subscribers[subscription_key]:
                del self.subscribers[subscription_key]
        
        logger.info(f"Unsubscribed from {subscription_key}")
    
    def start_live_data(self):
        """Start live data updates."""
        if not self.is_running:
            self.is_running = True
            self.data_thread = threading.Thread(target=self._data_update_loop, daemon=True)
            self.data_thread.start()
            logger.info("Live data updates started")
    
    def stop_live_data(self):
        """Stop live data updates."""
        self.is_running = False
        if self.data_thread:
            self.data_thread.join(timeout=5)
        logger.info("Live data updates stopped")
    
    def _data_update_loop(self):
        """Main data update loop."""
        while self.is_running:
            try:
                # Update all subscriptions
                for subscription_key, subscribers in self.subscribers.items():
                    if subscribers:
                        # Get the first subscriber's config (they should all be the same)
                        config = subscribers[0]['config']
                        
                        # Check if it's time to update
                        current_time = time.time()
                        if current_time - subscribers[0]['last_update'] >= config.update_interval:
                            # Fetch new data
                            asyncio.run(self._update_subscription_data(subscription_key, config, subscribers))
                
                time.sleep(1)  # Check every second
                
            except Exception as e:
                logger.error(f"Error in data update loop: {e}")
                time.sleep(5)
    
    async def _update_subscription_data(self, subscription_key: str, config: DataConfig, subscribers: List[Dict]):
        """Update data for a subscription."""
        try:
            # Get latest data
            result = await self.get_historical_data(config)
            
            if result['status'] == 'success':
                # Notify all subscribers
                for subscriber in subscribers:
                    try:
                        subscriber['callback'](result['data'], config)
                        subscriber['last_update'] = time.time()
                    except Exception as e:
                        logger.error(f"Error in subscriber callback: {e}")
            else:
                logger.warning(f"Failed to update data for {subscription_key}: {result['message']}")
                
        except Exception as e:
            logger.error(f"Error updating subscription data: {e}")
    
    def get_cached_data(self, config: DataConfig) -> Optional[pd.DataFrame]:
        """Get cached data if available."""
        cache_key = f"{config.source.value}_{config.symbol}_{config.interval}_{config.data_type.value}"
        
        if cache_key in self.data_cache:
            cache_entry = self.data_cache[cache_key]
            # Check if cache is still valid (less than 5 minutes old)
            if time.time() - cache_entry['timestamp'] < 300:
                return cache_entry['data']
        
        return None
    
    def get_data_sources_status(self) -> Dict[str, Any]:
        """Get status of all data sources."""
        status = {}
        
        for source, config in self.data_sources.items():
            status[source.value] = {
                'connected': config['connected'],
                'testnet': config['testnet'],
                'last_ping': config['last_ping'],
                'endpoints': list(config['endpoints'].keys())
            }
        
        return {
            'status': 'success',
            'sources': status,
            'total_sources': len(status),
            'active_subscriptions': len(self.subscribers),
            'cached_datasets': len(self.data_cache),
            'message': f'Data sources status for {len(status)} sources'
        }

# Example usage and testing
async def test_live_data_manager():
    """Test live data manager."""
    print("🧪 Testing Live Data Manager...")
    
    # Create data manager
    data_manager = LiveDataManager()
    
    # Initialize data sources
    print("  • Testing data source initialization...")
    sources_to_test = [DataSource.BINANCE, DataSource.BYBIT]
    
    for source in sources_to_test:
        result = await data_manager.initialize_data_source(source, testnet=True)
        print(f"    {source.value}: {'✅' if result['status'] == 'success' else '❌'} {result['message']}")
    
    # Test historical data retrieval
    print("  • Testing historical data retrieval...")
    
    # Test Binance data
    binance_config = DataConfig(
        source=DataSource.BINANCE,
        symbol='BTCUSDT',
        interval='1h',
        data_type=DataType.OHLCV,
        limit=100
    )
    
    binance_result = await data_manager.get_historical_data(binance_config)
    if binance_result['status'] == 'success':
        data = binance_result['data']
        print(f"    ✅ Binance: {binance_result['rows']} rows of {binance_result['data_type']} data")
        print(f"        - Columns: {list(data.columns) if hasattr(data, 'columns') else 'N/A'}")
        print(f"        - Date range: {data.index.min()} to {data.index.max()}" if hasattr(data, 'index') else 'N/A')
    else:
        print(f"    ❌ Binance: {binance_result['message']}")
    
    # Test Bybit data
    bybit_config = DataConfig(
        source=DataSource.BYBIT,
        symbol='BTCUSDT',
        interval='1h',
        data_type=DataType.OHLCV,
        limit=100
    )
    
    bybit_result = await data_manager.get_historical_data(bybit_config)
    if bybit_result['status'] == 'success':
        data = bybit_result['data']
        print(f"    ✅ Bybit: {bybit_result['rows']} rows of {bybit_result['data_type']} data")
        print(f"        - Columns: {list(data.columns) if hasattr(data, 'columns') else 'N/A'}")
        print(f"        - Date range: {data.index.min()} to {data.index.max()}" if hasattr(data, 'index') else 'N/A')
    else:
        print(f"    ❌ Bybit: {bybit_result['message']}")
    
    # Test data subscription
    print("  • Testing data subscription...")
    
    def data_callback(data, config):
        print(f"    📊 Data update received for {config.symbol}: {len(data)} rows")
    
    data_manager.subscribe_to_data(binance_config, data_callback)
    print("    ✅ Data subscription created")
    
    # Test data source status
    print("  • Testing data source status...")
    status = data_manager.get_data_sources_status()
    print(f"    ✅ {status['total_sources']} data sources, {status['active_subscriptions']} subscriptions")
    
    # Test caching
    print("  • Testing data caching...")
    cached_data = data_manager.get_cached_data(binance_config)
    if cached_data is not None:
        print(f"    ✅ Cached data available: {len(cached_data)} rows")
    else:
        print("    ⚠️ No cached data available")
    
    print("✅ Live Data Manager test completed!")
    
    return data_manager

if __name__ == "__main__":
    asyncio.run(test_live_data_manager())
