# -*- coding: utf-8 -*-
# src/ml/feature_engineering/statistical_features.py

"""
Statistical feature generator for NeoZork HLD Prediction.

This module creates ML features based on statistical analysis of price and volume data,
providing mathematical insights for the ML trading system.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union, Any
import warnings
from dataclasses import dataclass

from .base_feature_generator import BaseFeatureGenerator, FeatureConfig
from .logger import logger


@dataclass
class StatisticalFeatureConfig(FeatureConfig):
    """Configuration for statistical feature generation."""
    
    # Rolling window periods for statistical calculations
    rolling_periods: List[int] = None
    
    # Percentile levels for distribution analysis
    percentile_levels: List[float] = None
    
    # Z-score thresholds for outlier detection
    zscore_thresholds: List[float] = None
    
    # Skewness and kurtosis periods
    distribution_periods: List[int] = None
    
    def __post_init__(self):
        """Set default values if not provided."""
        super().__post_init__()
        
        if self.rolling_periods is None:
            self.rolling_periods = [10, 20, 50, 100]
            
        if self.percentile_levels is None:
            self.percentile_levels = [5, 10, 25, 75, 90, 95]
            
        if self.zscore_thresholds is None:
            self.zscore_thresholds = [2.0, 3.0]
            
        if self.distribution_periods is None:
            self.distribution_periods = [20, 50, 100]


class StatisticalFeatureGenerator(BaseFeatureGenerator):
    """
    Generator for statistical features.
    
    This class creates ML features based on statistical analysis,
    providing mathematical insights for the ML system.
    """
    
    def __init__(self, config: StatisticalFeatureConfig = None):
        """
        Initialize the statistical feature generator.
        
        Args:
            config: Configuration for statistical feature generation
        """
        super().__init__(config or StatisticalFeatureConfig())
        self.central_tendency_features = []
        self.dispersion_features = []
        self.distribution_features = []
        self.outlier_features = []
        self.percentile_features = []
        
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate statistical features from the input DataFrame.
        
        Args:
            df: Input DataFrame with OHLCV data
            
        Returns:
            DataFrame with original data plus statistical features
        """
        if not self.validate_data(df):
            return df
            
        df_features = df.copy()
        
        # Generate central tendency features
        df_features = self._generate_central_tendency_features(df_features)
        
        # Generate dispersion features
        df_features = self._generate_dispersion_features(df_features)
        
        # Generate distribution features
        df_features = self._generate_distribution_features(df_features)
        
        # Generate outlier features
        df_features = self._generate_outlier_features(df_features)
        
        # Generate percentile features
        df_features = self._generate_percentile_features(df_features)
        
        # Generate correlation features
        df_features = self._generate_correlation_features(df_features)
        
        logger.print_info(f"Generated {self.features_generated} statistical features")
        return df_features
    
    def _generate_central_tendency_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate central tendency features."""
        try:
            for price_type in self.config.price_types:
                price_col = price_type.capitalize()
                if price_col in df.columns:
                    for period in self.config.rolling_periods:
                        try:
                            # Mean
                            feature_name = f"mean_{price_type}_{period}"
                            df[feature_name] = df[price_col].rolling(window=period).mean()
                            self.log_feature_generation(feature_name, importance=0.6)
                            self.central_tendency_features.append(feature_name)
                            
                            # Median
                            feature_name = f"median_{price_type}_{period}"
                            df[feature_name] = df[price_col].rolling(window=period).median()
                            self.log_feature_generation(feature_name, importance=0.6)
                            self.central_tendency_features.append(feature_name)
                            
                            # Mode (approximated by most frequent value in window)
                            feature_name = f"mode_{price_type}_{period}"
                            df[feature_name] = df[price_col].rolling(window=period).apply(
                                lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0]
                            )
                            self.log_feature_generation(feature_name, importance=0.5)
                            self.central_tendency_features.append(feature_name)
                            
                            # Geometric mean
                            feature_name = f"geometric_mean_{price_type}_{period}"
                            df[feature_name] = df[price_col].rolling(window=period).apply(
                                lambda x: np.exp(np.log(x).mean()) if (x > 0).all() else x.mean()
                            )
                            self.log_feature_generation(feature_name, importance=0.5)
                            self.central_tendency_features.append(feature_name)
                            
                        except Exception as e:
                            logger.print_warning(f"Error generating central tendency feature for {price_type}_{period}: {e}")
                            continue
                            
        except Exception as e:
            logger.print_error(f"Error generating central tendency features: {e}")
            
        return df
    
    def _generate_dispersion_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate dispersion features."""
        try:
            for price_type in self.config.price_types:
                price_col = price_type.capitalize()
                if price_col in df.columns:
                    for period in self.config.rolling_periods:
                        try:
                            # Standard deviation
                            feature_name = f"std_{price_type}_{period}"
                            df[feature_name] = df[price_col].rolling(window=period).std()
                            self.log_feature_generation(feature_name, importance=0.7)
                            self.dispersion_features.append(feature_name)
                            
                            # Variance
                            feature_name = f"variance_{price_type}_{period}"
                            df[feature_name] = df[price_col].rolling(window=period).var()
                            self.log_feature_generation(feature_name, importance=0.6)
                            self.dispersion_features.append(feature_name)
                            
                            # Range
                            feature_name = f"range_{price_type}_{period}"
                            df[feature_name] = df[price_col].rolling(window=period).max() - df[price_col].rolling(window=period).min()
                            self.log_feature_generation(feature_name, importance=0.6)
                            self.dispersion_features.append(feature_name)
                            
                            # Interquartile range
                            feature_name = f"iqr_{price_type}_{period}"
                            df[feature_name] = df[price_col].rolling(window=period).quantile(0.75) - df[price_col].rolling(window=period).quantile(0.25)
                            self.log_feature_generation(feature_name, importance=0.6)
                            self.dispersion_features.append(feature_name)
                            
                            # Coefficient of variation
                            feature_name = f"cv_{price_type}_{period}"
                            mean = df[price_col].rolling(window=period).mean()
                            std = df[price_col].rolling(window=period).std()
                            df[feature_name] = std / mean
                            self.log_feature_generation(feature_name, importance=0.5)
                            self.dispersion_features.append(feature_name)
                            
                        except Exception as e:
                            logger.print_warning(f"Error generating dispersion feature for {price_type}_{period}: {e}")
                            continue
                            
        except Exception as e:
            logger.print_error(f"Error generating dispersion features: {e}")
            
        return df
    
    def _generate_distribution_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate distribution features."""
        try:
            for price_type in self.config.price_types:
                price_col = price_type.capitalize()
                if price_col in df.columns:
                    for period in self.config.distribution_periods:
                        try:
                            # Skewness
                            feature_name = f"skewness_{price_type}_{period}"
                            df[feature_name] = df[price_col].rolling(window=period).skew()
                            self.log_feature_generation(feature_name, importance=0.6)
                            self.distribution_features.append(feature_name)
                            
                            # Kurtosis
                            feature_name = f"kurtosis_{price_type}_{period}"
                            df[feature_name] = df[price_col].rolling(window=period).kurt()
                            self.log_feature_generation(feature_name, importance=0.6)
                            self.distribution_features.append(feature_name)
                            
                            # Jarque-Bera test statistic
                            feature_name = f"jarque_bera_{price_type}_{period}"
                            df[feature_name] = df[price_col].rolling(window=period).apply(
                                lambda x: self._calculate_jarque_bera(x) if len(x.dropna()) > 3 else np.nan
                            )
                            self.log_feature_generation(feature_name, importance=0.5)
                            self.distribution_features.append(feature_name)
                            
                        except Exception as e:
                            logger.print_warning(f"Error generating distribution feature for {price_type}_{period}: {e}")
                            continue
                            
        except Exception as e:
            logger.print_error(f"Error generating distribution features: {e}")
            
        return df
    
    def _calculate_jarque_bera(self, x: pd.Series) -> float:
        """Calculate Jarque-Bera test statistic."""
        try:
            n = len(x)
            if n < 4:
                return np.nan
                
            mean = x.mean()
            std = x.std()
            if std == 0:
                return np.nan
                
            skewness = x.skew()
            kurtosis = x.kurt()
            
            jb = n * (skewness**2 / 6 + (kurtosis - 3)**2 / 24)
            return jb
            
        except Exception:
            return np.nan
    
    def _generate_outlier_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate outlier detection features."""
        try:
            for price_type in self.config.price_types:
                price_col = price_type.capitalize()
                if price_col in df.columns:
                    for period in self.config.rolling_periods:
                        for threshold in self.config.zscore_thresholds:
                            try:
                                # Z-score based outlier detection
                                mean = df[price_col].rolling(window=period).mean()
                                std = df[price_col].rolling(window=period).std()
                                z_score = abs((df[price_col] - mean) / std)
                                
                                feature_name = f"outlier_{price_type}_{period}_{int(threshold)}"
                                df[feature_name] = np.where(z_score > threshold, 1, 0)
                                self.log_feature_generation(feature_name, importance=0.6)
                                self.outlier_features.append(feature_name)
                                
                                # IQR based outlier detection
                                q1 = df[price_col].rolling(window=period).quantile(0.25)
                                q3 = df[price_col].rolling(window=period).quantile(0.75)
                                iqr = q3 - q1
                                lower_bound = q1 - 1.5 * iqr
                                upper_bound = q3 + 1.5 * iqr
                                
                                feature_name = f"iqr_outlier_{price_type}_{period}"
                                df[feature_name] = np.where(
                                    (df[price_col] < lower_bound) | (df[price_col] > upper_bound), 1, 0
                                )
                                self.log_feature_generation(feature_name, importance=0.6)
                                self.outlier_features.append(feature_name)
                                
                            except Exception as e:
                                logger.print_warning(f"Error generating outlier feature for {price_type}_{period}_{threshold}: {e}")
                                continue
                                
        except Exception as e:
            logger.print_error(f"Error generating outlier features: {e}")
            
        return df
    
    def _generate_percentile_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate percentile-based features."""
        try:
            for price_type in self.config.price_types:
                price_col = price_type.capitalize()
                if price_col in df.columns:
                    for period in self.config.rolling_periods:
                        for percentile in self.config.percentile_levels:
                            try:
                                # Rolling percentile
                                feature_name = f"p{int(percentile)}_{price_type}_{period}"
                                df[feature_name] = df[price_col].rolling(window=period).quantile(percentile / 100)
                                self.log_feature_generation(feature_name, importance=0.6)
                                self.percentile_features.append(feature_name)
                                
                                # Distance from percentile
                                feature_name = f"distance_p{int(percentile)}_{price_type}_{period}"
                                percentile_value = df[price_col].rolling(window=period).quantile(percentile / 100)
                                df[feature_name] = (df[price_col] - percentile_value) / percentile_value
                                self.log_feature_generation(feature_name, importance=0.5)
                                self.percentile_features.append(feature_name)
                                
                            except Exception as e:
                                logger.print_warning(f"Error generating percentile feature for {price_type}_{period}_{percentile}: {e}")
                                continue
                                
        except Exception as e:
            logger.print_error(f"Error generating percentile features: {e}")
            
        return df
    
    def _generate_correlation_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate correlation-based features."""
        try:
            # Price correlations
            price_columns = [col for col in self.config.price_types if col.capitalize() in df.columns]
            
            if len(price_columns) > 1:
                for period in self.config.rolling_periods:
                    try:
                        # Correlation between Open and Close
                        if 'Open' in df.columns and 'Close' in df.columns:
                            feature_name = f"corr_open_close_{period}"
                            df[feature_name] = df['Open'].rolling(window=period).corr(df['Close'])
                            self.log_feature_generation(feature_name, importance=0.6)
                            self.dispersion_features.append(feature_name)
                            
                        # Correlation between High and Low
                        if 'High' in df.columns and 'Low' in df.columns:
                            feature_name = f"corr_high_low_{period}"
                            df[feature_name] = df['High'].rolling(window=period).corr(df['Low'])
                            self.log_feature_generation(feature_name, importance=0.6)
                            self.dispersion_features.append(feature_name)
                            
                        # Auto-correlation of Close prices
                        if 'Close' in df.columns:
                            feature_name = f"autocorr_close_{period}"
                            df[feature_name] = df['Close'].rolling(window=period).apply(
                                lambda x: x.corr(x.shift(1)) if len(x.dropna()) > 1 else np.nan
                            )
                            self.log_feature_generation(feature_name, importance=0.6)
                            self.dispersion_features.append(feature_name)
                            
                    except Exception as e:
                        logger.print_warning(f"Error generating correlation feature for period {period}: {e}")
                        continue
                        
        except Exception as e:
            logger.print_error(f"Error generating correlation features: {e}")
            
        return df
    
    def get_feature_names(self) -> List[str]:
        """Get list of generated statistical feature names."""
        return (self.central_tendency_features + self.dispersion_features + 
                self.distribution_features + self.outlier_features + self.percentile_features)
    
    def get_feature_categories(self) -> Dict[str, List[str]]:
        """Get features organized by category."""
        return {
            'central_tendency': self.central_tendency_features,
            'dispersion': self.dispersion_features,
            'distribution': self.distribution_features,
            'outliers': self.outlier_features,
            'percentiles': self.percentile_features,
            'all': self.get_feature_names()
        }
