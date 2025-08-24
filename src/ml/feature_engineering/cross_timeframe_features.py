# -*- coding: utf-8 -*-
# src/ml/feature_engineering/cross_timeframe_features.py

"""
Cross-timeframe feature generator for NeoZork HLD Prediction.

This module creates ML features by combining data from different timeframes,
providing multi-scale analysis for the ML trading system.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union, Any
import warnings
from dataclasses import dataclass

from .base_feature_generator import BaseFeatureGenerator, FeatureConfig
from .logger import logger


@dataclass
class CrossTimeframeFeatureConfig(FeatureConfig):
    """Configuration for cross-timeframe feature generation."""
    
    # Timeframe combinations
    timeframes: List[str] = None
    
    # Aggregation methods
    aggregation_methods: List[str] = None
    
    # Feature types to generate
    feature_types: List[str] = None
    
    # Lookback periods for cross-timeframe analysis
    lookback_periods: List[int] = None
    
    def __post_init__(self):
        """Set default values if not provided."""
        super().__post_init__()
        
        if self.timeframes is None:
            self.timeframes = ['1m', '5m', '15m', '1h', '4h', '1d']
            
        if self.aggregation_methods is None:
            self.aggregation_methods = ['mean', 'std', 'min', 'max', 'last']
            
        if self.feature_types is None:
            self.feature_types = ['ratio', 'difference', 'momentum', 'volatility']
            
        if self.lookback_periods is None:
            self.lookback_periods = [5, 10, 20, 50]


class CrossTimeframeFeatureGenerator(BaseFeatureGenerator):
    """
    Generator for cross-timeframe features.
    
    This class creates ML features by combining data from different timeframes,
    providing multi-scale analysis for the ML system.
    """
    
    def __init__(self, config: CrossTimeframeFeatureConfig = None):
        """
        Initialize the cross-timeframe feature generator.
        
        Args:
            config: Configuration for cross-timeframe feature generation
        """
        super().__init__(config or CrossTimeframeFeatureConfig())
        self.ratio_features = []
        self.difference_features = []
        self.momentum_features = []
        self.volatility_features = []
        
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate cross-timeframe features from the input DataFrame.
        
        Args:
            df: Input DataFrame with OHLCV data
            
        Returns:
            DataFrame with original data plus cross-timeframe features
        """
        if not self.validate_data(df):
            return df
            
        df_features = df.copy()
        
        # Generate ratio features
        if 'ratio' in self.config.feature_types:
            df_features = self._generate_ratio_features(df_features)
            
        # Generate difference features
        if 'difference' in self.config.feature_types:
            df_features = self._generate_difference_features(df_features)
            
        # Generate momentum features
        if 'momentum' in self.config.feature_types:
            df_features = self._generate_momentum_features(df_features)
            
        # Generate volatility features
        if 'volatility' in self.config.feature_types:
            df_features = self._generate_volatility_features(df_features)
            
        logger.print_info(f"Generated {self.features_generated} cross-timeframe features")
        return df_features
    
    def _generate_ratio_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate ratio-based cross-timeframe features."""
        try:
            # Price ratios across different lookback periods
            for period in self.config.lookback_periods:
                if len(df) > period:
                    try:
                        # Current price vs historical averages
                        for price_type in self.config.price_types:
                            price_col = price_type.capitalize()
                            if price_col in df.columns:
                                # Current vs short-term average
                                short_avg = df[price_col].rolling(window=period//2).mean()
                                feature_name = f"ratio_{price_type}_current_short_{period}"
                                df[feature_name] = df[price_col] / short_avg
                                self.log_feature_generation(feature_name, importance=0.6)
                                self.ratio_features.append(feature_name)
                                
                                # Current vs long-term average
                                long_avg = df[price_col].rolling(window=period).mean()
                                feature_name = f"ratio_{price_type}_current_long_{period}"
                                df[feature_name] = df[price_col] / long_avg
                                self.log_feature_generation(feature_name, importance=0.7)
                                self.ratio_features.append(feature_name)
                                
                                # Short-term vs long-term average
                                feature_name = f"ratio_{price_type}_short_long_{period}"
                                df[feature_name] = short_avg / long_avg
                                self.log_feature_generation(feature_name, importance=0.6)
                                self.ratio_features.append(feature_name)
                                
                    except Exception as e:
                        logger.print_warning(f"Error generating ratio features for period {period}: {e}")
                        continue
                        
        except Exception as e:
            logger.print_error(f"Error generating ratio features: {e}")
            
        return df
    
    def _generate_difference_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate difference-based cross-timeframe features."""
        try:
            # Price differences across different lookback periods
            for period in self.config.lookback_periods:
                if len(df) > period:
                    try:
                        # Price differences
                        for price_type in self.config.price_types:
                            price_col = price_type.capitalize()
                            if price_col in df.columns:
                                # Current vs short-term average difference
                                short_avg = df[price_col].rolling(window=period//2).mean()
                                feature_name = f"diff_{price_type}_current_short_{period}"
                                df[feature_name] = df[price_col] - short_avg
                                self.log_feature_generation(feature_name, importance=0.6)
                                self.difference_features.append(feature_name)
                                
                                # Current vs long-term average difference
                                long_avg = df[price_col].rolling(window=period).mean()
                                feature_name = f"diff_{price_type}_current_long_{period}"
                                df[feature_name] = df[price_col] - long_avg
                                self.log_feature_generation(feature_name, importance=0.7)
                                self.difference_features.append(feature_name)
                                
                                # Short-term vs long-term average difference
                                feature_name = f"diff_{price_type}_short_long_{period}"
                                df[feature_name] = short_avg - long_avg
                                self.log_feature_generation(feature_name, importance=0.6)
                                self.difference_features.append(feature_name)
                                
                                # Normalized differences
                                feature_name = f"norm_diff_{price_type}_current_long_{period}"
                                df[feature_name] = (df[price_col] - long_avg) / long_avg
                                self.log_feature_generation(feature_name, importance=0.6)
                                self.difference_features.append(feature_name)
                                
                    except Exception as e:
                        logger.print_warning(f"Error generating difference features for period {period}: {e}")
                        continue
                        
        except Exception as e:
            logger.print_error(f"Error generating difference features: {e}")
            
        return df
    
    def _generate_momentum_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate momentum-based cross-timeframe features."""
        try:
            # Momentum across different timeframes
            for period in self.config.lookback_periods:
                if len(df) > period:
                    try:
                        # Price momentum
                        for price_type in self.config.price_types:
                            price_col = price_type.capitalize()
                            if price_col in df.columns:
                                # Short-term momentum
                                short_momentum = df[price_col].pct_change(period//2)
                                feature_name = f"momentum_{price_type}_short_{period}"
                                df[feature_name] = short_momentum
                                self.log_feature_generation(feature_name, importance=0.6)
                                self.momentum_features.append(feature_name)
                                
                                # Long-term momentum
                                long_momentum = df[price_col].pct_change(period)
                                feature_name = f"momentum_{price_type}_long_{period}"
                                df[feature_name] = long_momentum
                                self.log_feature_generation(feature_name, importance=0.7)
                                self.momentum_features.append(feature_name)
                                
                                # Momentum acceleration
                                feature_name = f"momentum_accel_{price_type}_{period}"
                                df[feature_name] = short_momentum - long_momentum
                                self.log_feature_generation(feature_name, importance=0.6)
                                self.momentum_features.append(feature_name)
                                
                                # Momentum ratio
                                feature_name = f"momentum_ratio_{price_type}_{period}"
                                df[feature_name] = short_momentum / (long_momentum + 1e-8)  # Avoid division by zero
                                self.log_feature_generation(feature_name, importance=0.6)
                                self.momentum_features.append(feature_name)
                                
                    except Exception as e:
                        logger.print_warning(f"Error generating momentum features for period {period}: {e}")
                        continue
                        
        except Exception as e:
            logger.print_error(f"Error generating momentum features: {e}")
            
        return df
    
    def _generate_volatility_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate volatility-based cross-timeframe features."""
        try:
            # Volatility across different timeframes
            for period in self.config.lookback_periods:
                if len(df) > period:
                    try:
                        # Price volatility
                        for price_type in self.config.price_types:
                            price_col = price_type.capitalize()
                            if price_col in df.columns:
                                # Short-term volatility
                                short_vol = df[price_col].pct_change().rolling(window=period//2).std()
                                feature_name = f"volatility_{price_type}_short_{period}"
                                df[feature_name] = short_vol
                                self.log_feature_generation(feature_name, importance=0.6)
                                self.volatility_features.append(feature_name)
                                
                                # Long-term volatility
                                long_vol = df[price_col].pct_change().rolling(window=period).std()
                                feature_name = f"volatility_{price_type}_long_{period}"
                                df[feature_name] = long_vol
                                self.log_feature_generation(feature_name, importance=0.7)
                                self.volatility_features.append(feature_name)
                                
                                # Volatility ratio
                                feature_name = f"volatility_ratio_{price_type}_{period}"
                                df[feature_name] = short_vol / (long_vol + 1e-8)
                                self.log_feature_generation(feature_name, importance=0.6)
                                self.volatility_features.append(feature_name)
                                
                                # Volatility difference
                                feature_name = f"volatility_diff_{price_type}_{period}"
                                df[feature_name] = short_vol - long_vol
                                self.log_feature_generation(feature_name, importance=0.6)
                                self.volatility_features.append(feature_name)
                                
                                # Volatility momentum
                                feature_name = f"volatility_momentum_{price_type}_{period}"
                                df[feature_name] = long_vol.pct_change()
                                self.log_feature_generation(feature_name, importance=0.5)
                                self.volatility_features.append(feature_name)
                                
                    except Exception as e:
                        logger.print_warning(f"Error generating volatility features for period {period}: {e}")
                        continue
                        
        except Exception as e:
            logger.print_error(f"Error generating volatility features: {e}")
            
        return df
    
    def get_feature_names(self) -> List[str]:
        """Get list of generated cross-timeframe feature names."""
        return (self.ratio_features + self.difference_features + 
                self.momentum_features + self.volatility_features)
    
    def get_feature_categories(self) -> Dict[str, List[str]]:
        """Get features organized by category."""
        return {
            'ratio': self.ratio_features,
            'difference': self.difference_features,
            'momentum': self.momentum_features,
            'volatility': self.volatility_features,
            'all': self.get_feature_names()
        }
