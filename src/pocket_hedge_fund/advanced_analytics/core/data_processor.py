"""
Data Processor

Handles data cleaning, transformation, and preparation for analytics.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from decimal import Decimal
import pandas as pd
import numpy as np

from ..models.analytics_models import MarketData, DataFrequency

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Data processor for cleaning and transforming market data.
    """
    
    def __init__(self, db_manager=None):
        """Initialize data processor."""
        self.db_manager = db_manager
        self._data_cache = {}
        self._validation_rules = self._setup_validation_rules()
    
    def _setup_validation_rules(self) -> Dict[str, Any]:
        """Setup data validation rules."""
        return {
            'price_range': (0.01, 1000000),  # Min/max price
            'volume_range': (0, 1e12),       # Min/max volume
            'missing_threshold': 0.05,        # Max 5% missing data
            'outlier_threshold': 3.0,         # Z-score threshold
            'min_data_points': 10             # Minimum data points
        }
    
    async def initialize(self):
        """Initialize data processor."""
        try:
            logger.info("Data processor initialized")
        except Exception as e:
            logger.error(f"Failed to initialize data processor: {e}")
            raise
    
    async def get_market_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        frequency: DataFrequency = DataFrequency.DAILY
    ) -> List[MarketData]:
        """
        Retrieve market data from database.
        
        Args:
            symbol: Asset symbol
            start_date: Start date
            end_date: End date
            frequency: Data frequency
            
        Returns:
            List of market data
        """
        try:
            if self.db_manager is None:
                # Return mock data for testing
                return await self._generate_mock_data(
                    symbol, start_date, end_date, frequency
                )
            
            # Query database for market data
            query = """
                SELECT symbol, timestamp, open_price, high_price, 
                       low_price, close_price, volume, adjusted_close
                FROM market_data 
                WHERE symbol = $1 
                AND timestamp BETWEEN $2 AND $3
                AND frequency = $4
                ORDER BY timestamp
            """
            
            results = await self.db_manager.execute_query(
                query, [symbol, start_date, end_date, frequency.value]
            )
            
            market_data = []
            for row in results:
                data = MarketData(
                    symbol=row['symbol'],
                    timestamp=row['timestamp'],
                    open_price=Decimal(str(row['open_price'])),
                    high_price=Decimal(str(row['high_price'])),
                    low_price=Decimal(str(row['low_price'])),
                    close_price=Decimal(str(row['close_price'])),
                    volume=Decimal(str(row['volume'])),
                    adjusted_close=Decimal(str(row['adjusted_close'])) if row['adjusted_close'] else None,
                    frequency=frequency,
                    source="database"
                )
                market_data.append(data)
            
            logger.info(f"Retrieved {len(market_data)} records for {symbol}")
            return market_data
            
        except Exception as e:
            logger.error(f"Failed to get market data for {symbol}: {e}")
            raise
    
    async def _generate_mock_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        frequency: DataFrequency
    ) -> List[MarketData]:
        """Generate mock market data for testing."""
        import random
        
        market_data = []
        current_date = start_date
        base_price = Decimal('100.0')
        
        while current_date <= end_date:
            # Generate realistic price movement
            price_change = Decimal(str(random.uniform(-0.05, 0.05)))
            new_price = base_price * (1 + price_change)
            
            # Generate OHLC data
            open_price = base_price
            close_price = new_price
            high_price = max(open_price, close_price) * Decimal(str(random.uniform(1.0, 1.02)))
            low_price = min(open_price, close_price) * Decimal(str(random.uniform(0.98, 1.0)))
            volume = Decimal(str(random.randint(1000, 100000)))
            
            data = MarketData(
                symbol=symbol,
                timestamp=current_date,
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                close_price=close_price,
                volume=volume,
                frequency=frequency,
                source="mock"
            )
            market_data.append(data)
            
            base_price = close_price
            current_date += timedelta(days=1)
        
        return market_data
    
    async def clean_data(self, market_data: List[MarketData]) -> List[MarketData]:
        """
        Clean and validate market data.
        
        Args:
            market_data: Raw market data
            
        Returns:
            Cleaned market data
        """
        try:
            if not market_data:
                return market_data
            
            # Convert to DataFrame for easier processing
            df = self._to_dataframe(market_data)
            
            # Remove duplicates
            df = df.drop_duplicates(subset=['timestamp'])
            
            # Sort by timestamp
            df = df.sort_values('timestamp')
            
            # Validate data quality
            df = await self._validate_data(df)
            
            # Handle missing values
            df = await self._handle_missing_values(df)
            
            # Remove outliers
            df = await self._remove_outliers(df)
            
            # Convert back to MarketData objects
            cleaned_data = self._from_dataframe(df)
            
            logger.info(f"Cleaned {len(cleaned_data)} records")
            return cleaned_data
            
        except Exception as e:
            logger.error(f"Failed to clean data: {e}")
            raise
    
    def _to_dataframe(self, market_data: List[MarketData]) -> pd.DataFrame:
        """Convert MarketData list to DataFrame."""
        data = []
        for item in market_data:
            data.append({
                'symbol': item.symbol,
                'timestamp': item.timestamp,
                'open_price': float(item.open_price),
                'high_price': float(item.high_price),
                'low_price': float(item.low_price),
                'close_price': float(item.close_price),
                'volume': float(item.volume),
                'adjusted_close': float(item.adjusted_close) if item.adjusted_close else None,
                'frequency': item.frequency.value,
                'source': item.source
            })
        return pd.DataFrame(data)
    
    def _from_dataframe(self, df: pd.DataFrame) -> List[MarketData]:
        """Convert DataFrame to MarketData list."""
        market_data = []
        for _, row in df.iterrows():
            data = MarketData(
                symbol=row['symbol'],
                timestamp=row['timestamp'],
                open_price=Decimal(str(row['open_price'])),
                high_price=Decimal(str(row['high_price'])),
                low_price=Decimal(str(row['low_price'])),
                close_price=Decimal(str(row['close_price'])),
                volume=Decimal(str(row['volume'])),
                adjusted_close=Decimal(str(row['adjusted_close'])) if pd.notna(row['adjusted_close']) else None,
                frequency=DataFrequency(row['frequency']),
                source=row['source']
            )
            market_data.append(data)
        return market_data
    
    async def _validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate data quality."""
        rules = self._validation_rules
        
        # Check price ranges
        price_columns = ['open_price', 'high_price', 'low_price', 'close_price']
        for col in price_columns:
            df = df[(df[col] >= rules['price_range'][0]) & 
                   (df[col] <= rules['price_range'][1])]
        
        # Check volume range
        df = df[(df['volume'] >= rules['volume_range'][0]) & 
               (df['volume'] <= rules['volume_range'][1])]
        
        # Check OHLC relationships
        df = df[df['high_price'] >= df['low_price']]
        df = df[df['high_price'] >= df['open_price']]
        df = df[df['high_price'] >= df['close_price']]
        df = df[df['low_price'] <= df['open_price']]
        df = df[df['low_price'] <= df['close_price']]
        
        return df
    
    async def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in data."""
        # Forward fill for price data
        price_columns = ['open_price', 'high_price', 'low_price', 'close_price']
        df[price_columns] = df[price_columns].fillna(method='ffill')
        
        # Backward fill for any remaining missing values
        df[price_columns] = df[price_columns].fillna(method='bfill')
        
        # Fill volume with median
        df['volume'] = df['volume'].fillna(df['volume'].median())
        
        return df
    
    async def _remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove outliers using Z-score method."""
        threshold = self._validation_rules['outlier_threshold']
        
        # Calculate Z-scores for price data
        price_columns = ['open_price', 'high_price', 'low_price', 'close_price']
        for col in price_columns:
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            df = df[z_scores < threshold]
        
        return df
    
    async def resample_data(
        self,
        market_data: List[MarketData],
        target_frequency: DataFrequency
    ) -> List[MarketData]:
        """
        Resample data to different frequency.
        
        Args:
            market_data: Input market data
            target_frequency: Target frequency
            
        Returns:
            Resampled market data
        """
        try:
            if not market_data:
                return market_data
            
            df = self._to_dataframe(market_data)
            df.set_index('timestamp', inplace=True)
            
            # Resample based on target frequency
            if target_frequency == DataFrequency.HOUR:
                freq = 'H'
            elif target_frequency == DataFrequency.DAILY:
                freq = 'D'
            elif target_frequency == DataFrequency.WEEKLY:
                freq = 'W'
            elif target_frequency == DataFrequency.MONTHLY:
                freq = 'M'
            else:
                raise ValueError(f"Unsupported frequency: {target_frequency}")
            
            # Resample OHLC data
            resampled = df.resample(freq).agg({
                'open_price': 'first',
                'high_price': 'max',
                'low_price': 'min',
                'close_price': 'last',
                'volume': 'sum',
                'adjusted_close': 'last'
            }).dropna()
            
            resampled.reset_index(inplace=True)
            resampled['symbol'] = market_data[0].symbol
            resampled['frequency'] = target_frequency.value
            resampled['source'] = market_data[0].source
            
            result = self._from_dataframe(resampled)
            logger.info(f"Resampled {len(market_data)} records to {target_frequency}")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to resample data: {e}")
            raise
    
    async def calculate_returns(
        self,
        market_data: List[MarketData],
        return_type: str = 'simple'
    ) -> List[float]:
        """
        Calculate returns from market data.
        
        Args:
            market_data: Market data
            return_type: Type of returns (simple, log)
            
        Returns:
            List of returns
        """
        try:
            if len(market_data) < 2:
                return []
            
            prices = [float(item.close_price) for item in market_data]
            returns = []
            
            for i in range(1, len(prices)):
                if return_type == 'simple':
                    ret = (prices[i] - prices[i-1]) / prices[i-1]
                elif return_type == 'log':
                    ret = np.log(prices[i] / prices[i-1])
                else:
                    raise ValueError(f"Unsupported return type: {return_type}")
                
                returns.append(ret)
            
            return returns
            
        except Exception as e:
            logger.error(f"Failed to calculate returns: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup resources."""
        try:
            self._data_cache.clear()
            logger.info("Data processor cleanup completed")
        except Exception as e:
            logger.error(f"Error during data processor cleanup: {e}")
