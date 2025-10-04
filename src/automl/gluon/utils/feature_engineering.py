"""
Feature Engineering for SCHR Levels AutoML

Provides feature creation and engineering utilities.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, List


class FeatureEngineer:
    """Handles feature engineering for ML models"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create technical indicators"""
        try:
            if 'Close' not in df.columns:
                return df
            
            # Moving averages
            for period in [5, 10, 20, 50]:
                df[f'sma_{period}'] = df['Close'].rolling(window=period).mean()
                df[f'ema_{period}'] = df['Close'].ewm(span=period).mean()
            
            # Volatility indicators
            df['volatility_5'] = df['Close'].rolling(window=5).std()
            df['volatility_20'] = df['Close'].rolling(window=20).std()
            
            # RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # Bollinger Bands
            df['bb_middle'] = df['Close'].rolling(window=20).mean()
            bb_std = df['Close'].rolling(window=20).std()
            df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
            df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
            
            self.logger.info(f"Created technical indicators for {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"Feature engineering failed: {e}")
            return df
    
    def create_price_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create price-based features"""
        try:
            if 'Close' not in df.columns:
                return df
            
            # Price ratios
            df['close_open_ratio'] = df['Close'] / df['Open']
            df['high_low_ratio'] = df['High'] / df['Low']
            
            # Price changes
            df['price_change'] = df['Close'].pct_change()
            df['price_change_5'] = df['Close'].pct_change(5)
            df['price_change_20'] = df['Close'].pct_change(20)
            
            # Volume features
            if 'Volume' in df.columns:
                df['volume_sma'] = df['Volume'].rolling(window=20).mean()
                df['volume_ratio'] = df['Volume'] / df['volume_sma']
            
            self.logger.info(f"Created price features for {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"Price feature creation failed: {e}")
            return df
    
    def create_schr_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create SCHR-specific features"""
        try:
            # Distance to levels
            if all(col in df.columns for col in ['Close', 'predicted_high', 'predicted_low']):
                df['distance_to_high'] = (df['predicted_high'] - df['Close']) / df['Close']
                df['distance_to_low'] = (df['Close'] - df['predicted_low']) / df['Close']
                df['level_range'] = (df['predicted_high'] - df['predicted_low']) / df['Close']
            
            # Pressure features
            if 'pressure' in df.columns:
                df['pressure_ma'] = df['pressure'].rolling(window=5).mean()
                df['pressure_std'] = df['pressure'].rolling(window=20).std()
                df['pressure_momentum'] = df['pressure'].diff()
            
            # Pressure vector features
            if 'pressure_vector' in df.columns:
                df['pv_ma'] = df['pressure_vector'].rolling(window=5).mean()
                df['pv_std'] = df['pressure_vector'].rolling(window=20).std()
                df['pv_momentum'] = df['pressure_vector'].diff()
            
            self.logger.info(f"Created SCHR features for {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"SCHR feature creation failed: {e}")
            return df
