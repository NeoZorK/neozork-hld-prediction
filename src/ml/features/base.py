"""
Base Feature Engineering Components

This module provides base classes for feature engineering.
"""

import pandas as pd
from typing import Dict, Any, List, Optional
import numpy as np
from abc import ABC, abstractmethod

from ...core.base import BaseComponent
from ...core.exceptions import DataError, ValidationError


class BaseFeatureEngineer(BaseComponent, ABC):
    """
    Base class for feature engineering components.
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize feature engineer.
        
        Args:
            name: Name of the feature engineer
            config: Configuration dictionary
        """
        super().__init__(name, config)
        self.feature_names = []
    
    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform data to create new features.
        
        Args:
            data: Input data
            
        Returns:
            Data with engineered features
        """
        pass
    
    def validate_data(self, data: pd.DataFrame) -> None:
        """
        Validate input data.
        
        Args:
            data: Input data to validate
        """
        if data.empty:
            raise DataError("Input data is empty")


class TechnicalFeatures(BaseFeatureEngineer):
    """
    Technical analysis feature engineer.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize technical features engineer.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("technical_features", config)
        self.moving_average_periods = config.get("ma_periods", [5, 10, 20])
        self.rsi_period = config.get("rsi_period", 14)
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Create technical analysis features.
        
        Args:
            data: Input OHLCV data
            
        Returns:
            Data with technical features added
        """
        self.validate_data(data)
        
        result = data.copy()
        
        # Ensure we have required columns
        if 'close' not in data.columns:
            raise DataError("Data must contain 'close' column")
        
        # Moving averages
        for period in self.moving_average_periods:
            ma_name = f"ma_{period}"
            result[ma_name] = data['close'].rolling(window=period).mean()
            self.feature_names.append(ma_name)
        
        # Price changes
        result['price_change'] = data['close'].pct_change()
        result['price_change_abs'] = result['price_change'].abs()
        self.feature_names.extend(['price_change', 'price_change_abs'])
        
        # High-Low spread
        if 'high' in data.columns and 'low' in data.columns:
            result['hl_spread'] = data['high'] - data['low']
            result['hl_spread_pct'] = result['hl_spread'] / data['close']
            self.feature_names.extend(['hl_spread', 'hl_spread_pct'])
        
        # Volume features (if available)
        if 'volume' in data.columns:
            result['volume_ma_10'] = data['volume'].rolling(window=10).mean()
            result['volume_ratio'] = data['volume'] / result['volume_ma_10']
            self.feature_names.extend(['volume_ma_10', 'volume_ratio'])
        
        self.logger.debug(f"Created {len(self.feature_names)} technical features")
        return result


__all__ = ["BaseFeatureEngineer", "TechnicalFeatures"]
