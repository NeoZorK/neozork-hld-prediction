"""
Feature Engineer

Creates and manages features for ML models.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from decimal import Decimal
import numpy as np
import pandas as pd

from ..models.analytics_models import MarketData, DataFrequency

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """
    Feature engineer for creating technical and statistical features.
    """
    
    def __init__(self):
        """Initialize feature engineer."""
        self._feature_cache = {}
        self._feature_configs = self._setup_feature_configs()
    
    def _setup_feature_configs(self) -> Dict[str, Any]:
        """Setup feature generation configurations."""
        return {
            'technical_indicators': {
                'sma_periods': [5, 10, 20, 50, 200],
                'ema_periods': [12, 26, 50],
                'rsi_period': 14,
                'macd_periods': (12, 26, 9),
                'bollinger_period': 20,
                'bollinger_std': 2,
                'stochastic_period': 14,
                'williams_r_period': 14,
                'atr_period': 14
            },
            'statistical_features': {
                'volatility_periods': [5, 10, 20, 30],
                'skewness_period': 20,
                'kurtosis_period': 20,
                'correlation_period': 20
            },
            'momentum_features': {
                'roc_periods': [5, 10, 20],
                'momentum_periods': [5, 10, 20],
                'rate_of_change_periods': [5, 10, 20]
            }
        }
    
    async def initialize(self):
        """Initialize feature engineer."""
        try:
            logger.info("Feature engineer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize feature engineer: {e}")
            raise
    
    async def generate_features(
        self,
        market_data: List[MarketData],
        feature_types: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate features from market data.
        
        Args:
            market_data: Market data
            feature_types: Types of features to generate
            
        Returns:
            Dictionary of generated features
        """
        try:
            if feature_types is None:
                feature_types = ['technical', 'statistical', 'momentum']
            
            if not market_data:
                return {}
            
            # Convert to DataFrame
            df = self._to_dataframe(market_data)
            
            features = {}
            
            # Generate technical indicators
            if 'technical' in feature_types:
                features.update(await self._generate_technical_features(df))
            
            # Generate statistical features
            if 'statistical' in feature_types:
                features.update(await self._generate_statistical_features(df))
            
            # Generate momentum features
            if 'momentum' in feature_types:
                features.update(await self._generate_momentum_features(df))
            
            # Generate price-based features
            if 'price' in feature_types:
                features.update(await self._generate_price_features(df))
            
            # Generate volume features
            if 'volume' in feature_types:
                features.update(await self._generate_volume_features(df))
            
            logger.info(f"Generated {len(features)} feature groups")
            return features
            
        except Exception as e:
            logger.error(f"Failed to generate features: {e}")
            raise
    
    def _to_dataframe(self, market_data: List[MarketData]) -> pd.DataFrame:
        """Convert MarketData list to DataFrame."""
        data = []
        for item in market_data:
            data.append({
                'timestamp': item.timestamp,
                'open': float(item.open_price),
                'high': float(item.high_price),
                'low': float(item.low_price),
                'close': float(item.close_price),
                'volume': float(item.volume)
            })
        return pd.DataFrame(data).set_index('timestamp')
    
    async def _generate_technical_features(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate technical indicator features."""
        features = {}
        config = self._feature_configs['technical_indicators']
        
        # Simple Moving Averages
        for period in config['sma_periods']:
            features[f'sma_{period}'] = df['close'].rolling(window=period).mean()
        
        # Exponential Moving Averages
        for period in config['ema_periods']:
            features[f'ema_{period}'] = df['close'].ewm(span=period).mean()
        
        # RSI (Relative Strength Index)
        features['rsi'] = self._calculate_rsi(df['close'], config['rsi_period'])
        
        # MACD
        macd_line, signal_line, histogram = self._calculate_macd(
            df['close'], *config['macd_periods']
        )
        features['macd'] = macd_line
        features['macd_signal'] = signal_line
        features['macd_histogram'] = histogram
        
        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = self._calculate_bollinger_bands(
            df['close'], config['bollinger_period'], config['bollinger_std']
        )
        features['bb_upper'] = bb_upper
        features['bb_middle'] = bb_middle
        features['bb_lower'] = bb_lower
        features['bb_width'] = (bb_upper - bb_lower) / bb_middle
        features['bb_position'] = (df['close'] - bb_lower) / (bb_upper - bb_lower)
        
        # Stochastic Oscillator
        stoch_k, stoch_d = self._calculate_stochastic(
            df, config['stochastic_period']
        )
        features['stoch_k'] = stoch_k
        features['stoch_d'] = stoch_d
        
        # Williams %R
        features['williams_r'] = self._calculate_williams_r(
            df, config['williams_r_period']
        )
        
        # Average True Range
        features['atr'] = self._calculate_atr(df, config['atr_period'])
        
        return features
    
    async def _generate_statistical_features(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate statistical features."""
        features = {}
        config = self._feature_configs['statistical_features']
        
        # Volatility (standard deviation of returns)
        returns = df['close'].pct_change()
        for period in config['volatility_periods']:
            features[f'volatility_{period}'] = returns.rolling(window=period).std()
        
        # Skewness
        period = config['skewness_period']
        features[f'skewness_{period}'] = returns.rolling(window=period).skew()
        
        # Kurtosis
        period = config['kurtosis_period']
        features[f'kurtosis_{period}'] = returns.rolling(window=period).kurt()
        
        # Price percentiles
        for period in [20, 50, 100]:
            features[f'price_percentile_{period}'] = df['close'].rolling(
                window=period
            ).rank(pct=True)
        
        # High-Low ratio
        features['hl_ratio'] = df['high'] / df['low']
        
        # Close-Open ratio
        features['co_ratio'] = df['close'] / df['open']
        
        return features
    
    async def _generate_momentum_features(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate momentum features."""
        features = {}
        config = self._feature_configs['momentum_features']
        
        # Rate of Change
        for period in config['roc_periods']:
            features[f'roc_{period}'] = df['close'].pct_change(periods=period)
        
        # Momentum
        for period in config['momentum_periods']:
            features[f'momentum_{period}'] = df['close'] / df['close'].shift(period) - 1
        
        # Price acceleration
        features['price_acceleration'] = df['close'].diff().diff()
        
        # Volume momentum
        features['volume_momentum'] = df['volume'].pct_change()
        
        return features
    
    async def _generate_price_features(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate price-based features."""
        features = {}
        
        # Price gaps
        features['gap'] = df['open'] - df['close'].shift(1)
        features['gap_pct'] = features['gap'] / df['close'].shift(1)
        
        # Intraday range
        features['intraday_range'] = df['high'] - df['low']
        features['intraday_range_pct'] = features['intraday_range'] / df['open']
        
        # Close position in range
        features['close_position'] = (df['close'] - df['low']) / (df['high'] - df['low'])
        
        # Price levels
        features['price_level_20'] = df['close'].rolling(window=20).quantile(0.8)
        features['price_level_80'] = df['close'].rolling(window=20).quantile(0.2)
        
        return features
    
    async def _generate_volume_features(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate volume-based features."""
        features = {}
        
        # Volume moving averages
        for period in [5, 10, 20]:
            features[f'volume_sma_{period}'] = df['volume'].rolling(window=period).mean()
        
        # Volume ratio
        features['volume_ratio'] = df['volume'] / df['volume'].rolling(window=20).mean()
        
        # Price-volume trend
        features['pvt'] = (df['close'].pct_change() * df['volume']).cumsum()
        
        # On-balance volume
        features['obv'] = self._calculate_obv(df)
        
        # Volume-weighted average price
        features['vwap'] = (df['close'] * df['volume']).rolling(window=20).sum() / df['volume'].rolling(window=20).sum()
        
        return features
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(
        self, 
        prices: pd.Series, 
        fast: int = 12, 
        slow: int = 26, 
        signal: int = 9
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate MACD indicator."""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    
    def _calculate_bollinger_bands(
        self, 
        prices: pd.Series, 
        period: int = 20, 
        std_dev: float = 2
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate Bollinger Bands."""
        middle = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        return upper, middle, lower
    
    def _calculate_stochastic(
        self, 
        df: pd.DataFrame, 
        period: int = 14
    ) -> Tuple[pd.Series, pd.Series]:
        """Calculate Stochastic Oscillator."""
        lowest_low = df['low'].rolling(window=period).min()
        highest_high = df['high'].rolling(window=period).max()
        k_percent = 100 * ((df['close'] - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=3).mean()
        return k_percent, d_percent
    
    def _calculate_williams_r(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Williams %R."""
        highest_high = df['high'].rolling(window=period).max()
        lowest_low = df['low'].rolling(window=period).min()
        williams_r = -100 * ((highest_high - df['close']) / (highest_high - lowest_low))
        return williams_r
    
    def _calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range."""
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        atr = true_range.rolling(window=period).mean()
        return atr
    
    def _calculate_obv(self, df: pd.DataFrame) -> pd.Series:
        """Calculate On-Balance Volume."""
        obv = np.where(df['close'] > df['close'].shift(), df['volume'], 
                      np.where(df['close'] < df['close'].shift(), -df['volume'], 0))
        return pd.Series(obv, index=df.index).cumsum()
    
    async def select_features(
        self,
        features: Dict[str, Any],
        method: str = 'correlation',
        top_k: int = 50
    ) -> List[str]:
        """
        Select most important features.
        
        Args:
            features: Generated features
            method: Selection method
            top_k: Number of top features to select
            
        Returns:
            List of selected feature names
        """
        try:
            if method == 'correlation':
                return await self._select_by_correlation(features, top_k)
            elif method == 'variance':
                return await self._select_by_variance(features, top_k)
            else:
                raise ValueError(f"Unsupported selection method: {method}")
                
        except Exception as e:
            logger.error(f"Failed to select features: {e}")
            raise
    
    async def _select_by_correlation(
        self, 
        features: Dict[str, Any], 
        top_k: int
    ) -> List[str]:
        """Select features by correlation with target."""
        # This is a simplified implementation
        # In practice, you would calculate correlation with actual target variable
        feature_names = list(features.keys())
        return feature_names[:top_k]
    
    async def _select_by_variance(
        self, 
        features: Dict[str, Any], 
        top_k: int
    ) -> List[str]:
        """Select features by variance."""
        # This is a simplified implementation
        feature_names = list(features.keys())
        return feature_names[:top_k]
    
    async def cleanup(self):
        """Cleanup resources."""
        try:
            self._feature_cache.clear()
            logger.info("Feature engineer cleanup completed")
        except Exception as e:
            logger.error(f"Error during feature engineer cleanup: {e}")
