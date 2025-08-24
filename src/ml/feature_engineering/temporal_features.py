# -*- coding: utf-8 -*-
# src/ml/feature_engineering/temporal_features.py

"""
Temporal feature generator for NeoZork HLD Prediction.

This module creates ML features based on time and date information,
providing temporal patterns for the ML trading system.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union, Any
import warnings
from dataclasses import dataclass
from datetime import datetime, timedelta

from .base_feature_generator import BaseFeatureGenerator, FeatureConfig
from .logger import logger


@dataclass
class TemporalFeatureConfig(FeatureConfig):
    """Configuration for temporal feature generation."""
    
    # Time-based features
    enable_time_features: bool = True
    enable_date_features: bool = True
    enable_seasonal_features: bool = True
    enable_cyclical_features: bool = True
    
    # Time periods for cyclical encoding
    cyclical_periods: Dict[str, int] = None
    
    # Seasonal decomposition periods
    seasonal_periods: List[int] = None
    
    def __post_init__(self):
        """Set default values if not provided."""
        super().__post_init__()
        
        if self.cyclical_periods is None:
            self.cyclical_periods = {
                'hour': 24,
                'day': 7,
                'month': 12,
                'quarter': 4
            }
            
        if self.seasonal_periods is None:
            self.seasonal_periods = [24, 168, 720, 8760]  # Hour, week, month, year


class TemporalFeatureGenerator(BaseFeatureGenerator):
    """
    Generator for temporal features.
    
    This class creates ML features based on time and date information,
    providing temporal patterns for the ML system.
    """
    
    def __init__(self, config: TemporalFeatureConfig = None):
        """
        Initialize the temporal feature generator.
        
        Args:
            config: Configuration for temporal feature generation
        """
        super().__init__(config or TemporalFeatureConfig())
        self.time_features = []
        self.date_features = []
        self.seasonal_features = []
        self.cyclical_features = []
        
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate temporal features from the input DataFrame.
        
        Args:
            df: Input DataFrame with OHLCV data
            
        Returns:
            DataFrame with original data plus temporal features
        """
        if not self.validate_data(df):
            return df
            
        df_features = df.copy()
        
        # Ensure datetime index
        df_features = self._ensure_datetime_index(df_features)
        
        if df_features is None:
            logger.print_warning("Could not create datetime index, skipping temporal features")
            return df
            
        # Generate time features
        if self.config.enable_time_features:
            df_features = self._generate_time_features(df_features)
            
        # Generate date features
        if self.config.enable_date_features:
            df_features = self._generate_date_features(df_features)
            
        # Generate seasonal features
        if self.config.enable_seasonal_features:
            df_features = self._generate_seasonal_features(df_features)
            
        # Generate cyclical features
        if self.config.enable_cyclical_features:
            df_features = self._generate_cyclical_features(df_features)
            
        logger.print_info(f"Generated {self.features_generated} temporal features")
        return df_features
    
    def _ensure_datetime_index(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """Ensure DataFrame has a proper datetime index."""
        try:
            df_copy = df.copy()
            
            # Check if index is already datetime
            if isinstance(df_copy.index, pd.DatetimeIndex):
                return df_copy
                
            # Try to convert index to datetime
            try:
                df_copy.index = pd.to_datetime(df_copy.index)
                return df_copy
            except:
                pass
                
            # Check for datetime columns
            datetime_columns = []
            for col in df_copy.columns:
                if df_copy[col].dtype == 'object':
                    try:
                        pd.to_datetime(df_copy[col].iloc[0])
                        datetime_columns.append(col)
                    except:
                        continue
                        
            if datetime_columns:
                # Use first datetime column as index
                datetime_col = datetime_columns[0]
                df_copy.index = pd.to_datetime(df_copy[datetime_col])
                df_copy = df_copy.drop(columns=[datetime_col])
                return df_copy
                
            # Create synthetic datetime index if none available
            logger.print_warning("No datetime information found, creating synthetic index")
            df_copy.index = pd.date_range(
                start='2020-01-01', 
                periods=len(df_copy), 
                freq='1H'
            )
            return df_copy
            
        except Exception as e:
            logger.print_error(f"Error creating datetime index: {e}")
            return None
    
    def _generate_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate time-based features."""
        try:
            # Hour of day
            df['hour'] = df.index.hour
            self.log_feature_generation('hour', importance=0.7)
            self.time_features.append('hour')
            
            # Minute of hour (if available)
            if hasattr(df.index, 'minute'):
                df['minute'] = df.index.minute
                self.log_feature_generation('minute', importance=0.5)
                self.time_features.append('minute')
                
            # Second of minute (if available)
            if hasattr(df.index, 'second'):
                df['second'] = df.index.second
                self.log_feature_generation('second', importance=0.3)
                self.time_features.append('second')
                
            # Time of day (0-1 normalized)
            df['time_of_day'] = (df.index.hour * 3600 + df.index.minute * 60) / 86400
            self.log_feature_generation('time_of_day', importance=0.6)
            self.time_features.append('time_of_day')
            
            # Business hours indicator
            df['business_hours'] = np.where(
                (df.index.hour >= 9) & (df.index.hour < 17), 1, 0
            )
            self.log_feature_generation('business_hours', importance=0.6)
            self.time_features.append('business_hours')
            
            # Market session indicators
            df['asian_session'] = np.where(
                (df.index.hour >= 0) & (df.index.hour < 8), 1, 0
            )
            df['london_session'] = np.where(
                (df.index.hour >= 8) & (df.index.hour < 16), 1, 0
            )
            df['ny_session'] = np.where(
                (df.index.hour >= 13) & (df.index.hour < 21), 1, 0
            )
            
            self.log_feature_generation('asian_session', importance=0.6)
            self.log_feature_generation('london_session', importance=0.6)
            self.log_feature_generation('ny_session', importance=0.6)
            
            self.time_features.extend(['asian_session', 'london_session', 'ny_session'])
            
        except Exception as e:
            logger.print_error(f"Error generating time features: {e}")
            
        return df
    
    def _generate_date_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate date-based features."""
        try:
            # Day of week (0=Monday, 6=Sunday)
            df['day_of_week'] = df.index.dayofweek
            self.log_feature_generation('day_of_week', importance=0.7)
            self.date_features.append('day_of_week')
            
            # Day of month
            df['day_of_month'] = df.index.day
            self.log_feature_generation('day_of_month', importance=0.6)
            self.date_features.append('day_of_month')
            
            # Day of year
            df['day_of_year'] = df.index.dayofyear
            self.log_feature_generation('day_of_year', importance=0.6)
            self.date_features.append('day_of_year')
            
            # Week of year
            df['week_of_year'] = df.index.isocalendar().week
            self.log_feature_generation('week_of_year', importance=0.6)
            self.date_features.append('week_of_year')
            
            # Month
            df['month'] = df.index.month
            self.log_feature_generation('month', importance=0.7)
            self.date_features.append('month')
            
            # Quarter
            df['quarter'] = df.index.quarter
            self.log_feature_generation('quarter', importance=0.6)
            self.date_features.append('quarter')
            
            # Year
            df['year'] = df.index.year
            self.log_feature_generation('year', importance=0.5)
            self.date_features.append('year')
            
            # Weekend indicator
            df['is_weekend'] = np.where(df.index.dayofweek >= 5, 1, 0)
            self.log_feature_generation('is_weekend', importance=0.6)
            self.date_features.append('is_weekend')
            
            # Month end indicator
            df['is_month_end'] = df.index.is_month_end.astype(int)
            self.log_feature_generation('is_month_end', importance=0.5)
            self.date_features.append('is_month_end')
            
            # Quarter end indicator
            df['is_quarter_end'] = df.index.is_quarter_end.astype(int)
            self.log_feature_generation('is_quarter_end', importance=0.5)
            self.date_features.append('is_quarter_end')
            
            # Year end indicator
            df['is_year_end'] = df.index.is_year_end.astype(int)
            self.log_feature_generation('is_year_end', importance=0.5)
            self.date_features.append('is_year_end')
            
        except Exception as e:
            logger.print_error(f"Error generating date features: {e}")
            
        return df
    
    def _generate_seasonal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate seasonal features."""
        try:
            # Seasonal decomposition for different periods
            for period in self.seasonal_periods:
                if len(df) >= period * 2:
                    try:
                        # Trend component
                        feature_name = f"trend_{period}"
                        df[feature_name] = df['Close'].rolling(window=period).mean()
                        self.log_feature_generation(feature_name, importance=0.6)
                        self.seasonal_features.append(feature_name)
                        
                        # Seasonal component (simplified)
                        feature_name = f"seasonal_{period}"
                        seasonal = df['Close'] - df[f"trend_{period}"]
                        df[feature_name] = seasonal
                        self.log_feature_generation(feature_name, importance=0.5)
                        self.seasonal_features.append(feature_name)
                        
                        # Residual component
                        feature_name = f"residual_{period}"
                        df[feature_name] = df['Close'] - df[f"trend_{period}"] - df[f"seasonal_{period}"]
                        self.log_feature_generation(feature_name, importance=0.5)
                        self.seasonal_features.append(feature_name)
                        
                    except Exception as e:
                        logger.print_warning(f"Error generating seasonal features for period {period}: {e}")
                        continue
                        
        except Exception as e:
            logger.print_error(f"Error generating seasonal features: {e}")
            
        return df
    
    def _generate_cyclical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate cyclical features using sine/cosine encoding."""
        try:
            for feature, period in self.config.cyclical_periods.items():
                if feature in df.columns:
                    # Sine encoding
                    feature_name = f"{feature}_sin"
                    df[feature_name] = np.sin(2 * np.pi * df[feature] / period)
                    self.log_feature_generation(feature_name, importance=0.6)
                    self.cyclical_features.append(feature_name)
                    
                    # Cosine encoding
                    feature_name = f"{feature}_cos"
                    df[feature_name] = np.cos(2 * np.pi * df[feature] / period)
                    self.log_feature_generation(feature_name, importance=0.6)
                    self.cyclical_features.append(feature_name)
                    
            # Special cyclical features for time
            if 'hour' in df.columns:
                # Hour cyclical (24-hour cycle)
                df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
                df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
                self.log_feature_generation('hour_sin', importance=0.6)
                self.log_feature_generation('hour_cos', importance=0.6)
                self.cyclical_features.extend(['hour_sin', 'hour_cos'])
                
            if 'day_of_week' in df.columns:
                # Day of week cyclical (7-day cycle)
                df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
                df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
                self.log_feature_generation('day_sin', importance=0.6)
                self.log_feature_generation('day_cos', importance=0.6)
                self.cyclical_features.extend(['day_sin', 'day_cos'])
                
            if 'month' in df.columns:
                # Month cyclical (12-month cycle)
                df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
                df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
                self.log_feature_generation('month_sin', importance=0.6)
                self.log_feature_generation('month_cos', importance=0.6)
                self.cyclical_features.extend(['month_sin', 'month_cos'])
                
        except Exception as e:
            logger.print_error(f"Error generating cyclical features: {e}")
            
        return df
    
    def get_feature_names(self) -> List[str]:
        """Get list of generated temporal feature names."""
        return (self.time_features + self.date_features + 
                self.seasonal_features + self.cyclical_features)
    
    def get_feature_categories(self) -> Dict[str, List[str]]:
        """Get features organized by category."""
        return {
            'time': self.time_features,
            'date': self.date_features,
            'seasonal': self.seasonal_features,
            'cyclical': self.cyclical_features,
            'all': self.get_feature_names()
        }
