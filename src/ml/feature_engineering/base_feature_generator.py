# -*- coding: utf-8 -*-
# src/ml/feature_engineering/base_feature_generator.py

"""
Base class for all feature generators in the NeoZorK ML system.

This module provides the foundation for creating technical, statistical,
and proprietary features from financial time series data.
"""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass
import warnings

from .logger import logger

# Constants for trading signals
BUY = 1
SELL = -1
NOTRADE = 0


@dataclass
class FeatureConfig:
    """Configuration for feature generation."""
    
    # Time periods for various calculations
    short_periods: List[int] = None
    medium_periods: List[int] = None
    long_periods: List[int] = None
    
    # Price types to use
    price_types: List[str] = None
    
    # Volatility parameters
    volatility_periods: List[int] = None
    
    # Volume parameters
    volume_periods: List[int] = None
    
    # Feature types to generate
    feature_types: List[str] = None
    
    # Custom parameters for proprietary indicators
    custom_params: Dict[str, Any] = None
    
    def __post_init__(self):
        """Set default values if not provided."""
        if self.short_periods is None:
            self.short_periods = [5, 10, 14]
        if self.medium_periods is None:
            self.medium_periods = [20, 50, 100]
        if self.long_periods is None:
            self.long_periods = [200, 500]
        if self.price_types is None:
            self.price_types = ['open', 'high', 'low', 'close']
        if self.volatility_periods is None:
            self.volatility_periods = [14, 20, 50]
        if self.volume_periods is None:
            self.volume_periods = [14, 20, 50]
        if self.feature_types is None:
            self.feature_types = ['ratio', 'difference', 'momentum', 'volatility']
        if self.custom_params is None:
            self.custom_params = {}


class BaseFeatureGenerator(ABC):
    """
    Abstract base class for all feature generators.
    
    This class provides common functionality and enforces the interface
    that all feature generators must implement.
    """
    
    def __init__(self, config: FeatureConfig = None):
        """
        Initialize the feature generator.
        
        Args:
            config: Configuration object for feature generation
        """
        self.config = config or FeatureConfig()
        self.features_generated = 0
        self.feature_names = []
        self.feature_importance = {}
        
    @abstractmethod
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate features from the input DataFrame.
        
        Args:
            df: Input DataFrame with OHLCV data
            
        Returns:
            DataFrame with original data plus generated features
        """
        pass
    
    @abstractmethod
    def get_feature_names(self) -> List[str]:
        """
        Get list of generated feature names.
        
        Returns:
            List of feature column names
        """
        pass
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Validate input data for feature generation.
        
        Args:
            df: Input DataFrame
            
        Returns:
            True if data is valid, False otherwise
        """
        if df is None or df.empty:
            logger.print_error("DataFrame is None or empty")
            return False
            
        required_columns = ['Open', 'High', 'Low', 'Close']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logger.print_error(f"Missing required columns: {missing_columns}")
            return False
            
        # Check for sufficient data
        min_required = max(self.config.long_periods) if self.config.long_periods else 200
        if len(df) < min_required:
            logger.print_warning(f"Insufficient data: {len(df)} rows, need at least {min_required}")
            return False
            
        return True
    
    def handle_missing_values(self, df: pd.DataFrame, method: str = 'forward_fill') -> pd.DataFrame:
        """
        Handle missing values in the DataFrame.
        
        Args:
            df: Input DataFrame
            method: Method to handle missing values ('forward_fill', 'backward_fill', 'interpolate')
            
        Returns:
            DataFrame with handled missing values
        """
        df_clean = df.copy()
        
        if method == 'forward_fill':
            df_clean = df_clean.ffill()
        elif method == 'backward_fill':
            df_clean = df_clean.bfill()
        elif method == 'interpolate':
            df_clean = df_clean.interpolate(method='linear')
        else:
            logger.print_warning(f"Unknown method '{method}', using forward fill")
            df_clean = df_clean.ffill()
            
        # Drop any remaining NaN rows at the beginning
        df_clean = df_clean.dropna()
        
        return df_clean
    
    def calculate_returns(self, df: pd.DataFrame, price_col: str = 'Close') -> pd.Series:
        """
        Calculate price returns.
        
        Args:
            df: Input DataFrame
            price_col: Price column to use for calculations
            
        Returns:
            Series with returns
        """
        if price_col not in df.columns:
            logger.print_error(f"Price column '{price_col}' not found")
            return pd.Series(dtype=float)
            
        returns = df[price_col].pct_change(fill_method=None)
        return returns
    
    def calculate_log_returns(self, df: pd.DataFrame, price_col: str = 'Close') -> pd.Series:
        """
        Calculate log returns.
        
        Args:
            df: Input DataFrame
            price_col: Price column to use for calculations
            
        Returns:
            Series with log returns
        """
        if price_col not in df.columns:
            logger.print_error(f"Price column '{price_col}' not found")
            return pd.Series(dtype=float)
            
        log_returns = np.log(df[price_col] / df[price_col].shift(1))
        return log_returns
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance scores.
        
        Returns:
            Dictionary mapping feature names to importance scores
        """
        return self.feature_importance.copy()
    
    def set_feature_importance(self, importance_dict: Dict[str, float]):
        """
        Set feature importance scores.
        
        Args:
            importance_dict: Dictionary mapping feature names to importance scores
        """
        self.feature_importance = importance_dict.copy()
    
    def get_feature_count(self) -> int:
        """
        Get total number of features generated.
        
        Returns:
            Number of features generated
        """
        return self.features_generated
    
    def reset_feature_count(self):
        """Reset feature count to zero."""
        self.features_generated = 0
        self.feature_names = []
    
    def log_feature_generation(self, feature_name: str, importance: float = 0.0):
        """
        Log feature generation for tracking.
        
        Args:
            feature_name: Name of the generated feature
            importance: Importance score for the feature
        """
        self.features_generated += 1
        self.feature_names.append(feature_name)
        if importance > 0:
            self.feature_importance[feature_name] = importance
            
        logger.print_debug(f"Generated feature: {feature_name} (importance: {importance:.4f})")
    
    def __str__(self) -> str:
        """String representation of the feature generator."""
        return f"{self.__class__.__name__}(features_generated={self.features_generated})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"{self.__class__.__name__}(config={self.config}, features_generated={self.features_generated})"
