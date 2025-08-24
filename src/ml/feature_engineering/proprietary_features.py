# -*- coding: utf-8 -*-
# src/ml/feature_engineering/proprietary_features.py

"""
Proprietary feature generator for NeoZork HLD Prediction.

This module creates ML features based on the proprietary PHLD and Wave indicators,
providing the foundation for the ML trading system.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union, Any
import warnings
from dataclasses import dataclass

from .base_feature_generator import BaseFeatureGenerator, FeatureConfig
from .logger import logger
from .base_feature_generator import BUY, SELL, NOTRADE

# Import proprietary indicators
try:
    from src.calculation.indicators.trend.wave_ind import (
        init_wave, WaveParameters, ENUM_MOM_TR, ENUM_GLOBAL_TR
    )
except ImportError:
    logger.print_warning("Wave indicator not available, some features will be skipped")
    init_wave = None

try:
    from src.calculation.indicator import calculate_pressure_vector
except ImportError:
    logger.print_warning("PHLD indicator not available, some features will be skipped")
    calculate_pressure_vector = None


@dataclass
class ProprietaryFeatureConfig(FeatureConfig):
    """Configuration for proprietary feature generation."""
    
    # PHLD parameters
    phld_point_size: float = 0.00001  # Default for forex
    phld_trading_rules: List[str] = None
    
    # Wave parameters
    wave_parameter_sets: List[Dict[str, Any]] = None
    wave_trading_rules: List[str] = None
    
    # Feature combinations
    create_derivative_features: bool = True
    create_interaction_features: bool = True
    create_momentum_features: bool = True
    
    def __post_init__(self):
        """Set default values if not provided."""
        super().__post_init__()
        
        if self.phld_trading_rules is None:
            self.phld_trading_rules = ['PV_HighLow', 'PV_Momentum', 'PV_Divergence']
            
        if self.wave_parameter_sets is None:
            self.wave_parameter_sets = [
                # Conservative set
                {'long1': 339, 'fast1': 10, 'trend1': 2, 'long2': 22, 'fast2': 11, 'trend2': 4, 'sma_period': 22},
                # Aggressive set
                {'long1': 100, 'fast1': 5, 'trend1': 1, 'long2': 15, 'fast2': 8, 'trend2': 2, 'sma_period': 15},
                # Balanced set
                {'long1': 200, 'fast1': 8, 'trend1': 2, 'long2': 20, 'fast2': 10, 'trend2': 3, 'sma_period': 20}
            ]
            
        if self.wave_trading_rules is None:
            self.wave_trading_rules = ['TR_Fast', 'TR_Zone', 'TR_StrongTrend']


class ProprietaryFeatureGenerator(BaseFeatureGenerator):
    """
    Generator for proprietary PHLD and Wave indicator features.
    
    This class creates ML features based on the proprietary trading algorithms,
    providing the core predictive power for the ML system.
    """
    
    def __init__(self, config: ProprietaryFeatureConfig = None):
        """
        Initialize the proprietary feature generator.
        
        Args:
            config: Configuration for proprietary feature generation
        """
        super().__init__(config or ProprietaryFeatureConfig())
        self.phld_features = []
        self.wave_features = []
        self.derivative_features = []
        
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate proprietary features from the input DataFrame.
        
        Args:
            df: Input DataFrame with OHLCV data
            
        Returns:
            DataFrame with original data plus proprietary features
        """
        if not self.validate_data(df):
            return df
            
        df_features = df.copy()
        
        # Generate PHLD features
        if calculate_pressure_vector is not None:
            df_features = self._generate_phld_features(df_features)
            
        # Generate Wave features
        if init_wave is not None:
            df_features = self._generate_wave_features(df_features)
            
        # Generate derivative features
        if self.config.create_derivative_features:
            df_features = self._generate_derivative_features(df_features)
            
        # Generate interaction features
        if self.config.create_interaction_features:
            df_features = self._generate_interaction_features(df_features)
            
        # Generate momentum features
        if self.config.create_momentum_features:
            df_features = self._generate_momentum_features(df_features)
            
        logger.print_info(f"Generated {self.features_generated} proprietary features")
        return df_features
    
    def _generate_phld_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate PHLD-based features."""
        try:
            for rule in self.config.phld_trading_rules:
                # Calculate PHLD indicator
                df_phld = calculate_pressure_vector(
                    df.copy(), 
                    self.config.phld_point_size, 
                    rule
                )
                
                # Extract PHLD features
                phld_columns = ['HL', 'Pressure', 'PV', 'PPrice1', 'PPrice2', 'Direction']
                
                for col in phld_columns:
                    if col in df_phld.columns:
                        feature_name = f"phld_{rule}_{col.lower()}"
                        df[feature_name] = df_phld[col]
                        self.log_feature_generation(feature_name, importance=0.8)
                        self.phld_features.append(feature_name)
                        
                        # Create normalized versions
                        if col in ['HL', 'Pressure', 'PV']:
                            # Z-score normalization
                            mean_val = df_phld[col].mean()
                            std_val = df_phld[col].std()
                            if std_val > 0:
                                df[f"{feature_name}_zscore"] = (df_phld[col] - mean_val) / std_val
                                self.log_feature_generation(f"{feature_name}_zscore", importance=0.7)
                                
                            # Min-max normalization
                            min_val = df_phld[col].min()
                            max_val = df_phld[col].max()
                            if max_val > min_val:
                                df[f"{feature_name}_norm"] = (df_phld[col] - min_val) / (max_val - min_val)
                                self.log_feature_generation(f"{feature_name}_norm", importance=0.6)
                                
        except Exception as e:
            logger.print_error(f"Error generating PHLD features: {e}")
            
        return df
    
    def _generate_wave_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate Wave-based features."""
        try:
            for i, params in enumerate(self.config.wave_parameter_sets):
                for tr in self.config.wave_trading_rules:
                    try:
                        # Create Wave parameters
                        wave_params = WaveParameters(
                            long1=params.get('long1', 339),
                            fast1=params.get('fast1', 10),
                            trend1=params.get('trend1', 2),
                            tr1=getattr(ENUM_MOM_TR, tr),
                            long2=params.get('long2', 22),
                            fast2=params.get('fast2', 11),
                            trend2=params.get('trend2', 4),
                            tr2=getattr(ENUM_MOM_TR, tr),
                            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME,
                            sma_period=params.get('sma_period', 22)
                        )
                        
                        # Calculate Wave indicator
                        wave_values = init_wave(df['Close'], wave_params)
                        
                        if wave_values is not None and not wave_values.empty:
                            # Basic wave features
                            feature_name = f"wave_{i}_{tr}_value"
                            df[feature_name] = wave_values
                            self.log_feature_generation(feature_name, importance=0.9)
                            self.wave_features.append(feature_name)
                            
                            # Wave momentum features
                            df[f"{feature_name}_momentum"] = wave_values.diff()
                            self.log_feature_generation(f"{feature_name}_momentum", importance=0.8)
                            
                            df[f"{feature_name}_momentum_ma"] = wave_values.diff().rolling(5).mean()
                            self.log_feature_generation(f"{feature_name}_momentum_ma", importance=0.7)
                            
                            # Wave volatility features
                            df[f"{feature_name}_volatility"] = wave_values.rolling(20).std()
                            self.log_feature_generation(f"{feature_name}_volatility", importance=0.7)
                            
                            # Wave trend features
                            df[f"{feature_name}_trend"] = wave_values.rolling(50).mean()
                            self.log_feature_generation(f"{feature_name}_trend", importance=0.8)
                            
                            # Wave position features
                            df[f"{feature_name}_position"] = (wave_values - wave_values.rolling(100).min()) / \
                                                             (wave_values.rolling(100).max() - wave_values.rolling(100).min())
                            self.log_feature_generation(f"{feature_name}_position", importance=0.6)
                            
                    except Exception as e:
                        logger.print_warning(f"Error generating Wave features for params {i}, rule {tr}: {e}")
                        continue
                        
        except Exception as e:
            logger.print_error(f"Error generating Wave features: {e}")
            
        return df
    
    def _generate_derivative_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate derivative features from existing indicators."""
        try:
            # Get all PHLD and Wave features
            all_features = self.phld_features + self.wave_features
            
            for feature in all_features:
                if feature in df.columns:
                    # First derivative (rate of change)
                    df[f"{feature}_derivative"] = df[feature].diff()
                    self.log_feature_generation(f"{feature}_derivative", importance=0.6)
                    
                    # Second derivative (acceleration)
                    df[f"{feature}_derivative2"] = df[feature].diff().diff()
                    self.log_feature_generation(f"{feature}_derivative2", importance=0.5)
                    
                    # Rate of change percentage
                    df[f"{feature}_roc"] = df[feature].pct_change()
                    self.log_feature_generation(f"{feature}_roc", importance=0.6)
                    
                    # Moving average ratios
                    for period in [5, 10, 20]:
                        ma = df[feature].rolling(period).mean()
                        if not ma.isna().all():
                            df[f"{feature}_ma{period}_ratio"] = df[feature] / ma
                            self.log_feature_generation(f"{feature}_ma{period}_ratio", importance=0.5)
                            
        except Exception as e:
            logger.print_error(f"Error generating derivative features: {e}")
            
        return df
    
    def _generate_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate interaction features between different indicators."""
        try:
            # PHLD interactions
            phld_hl = [f for f in self.phld_features if 'hl' in f]
            phld_pressure = [f for f in self.phld_features if 'pressure' in f]
            phld_pv = [f for f in self.phld_features if 'pv' in f]
            
            # Wave interactions
            wave_values = [f for f in self.wave_features if 'value' in f]
            
            # Create interaction features
            if phld_hl and phld_pressure:
                for hl_feat in phld_hl[:2]:  # Limit to first 2 to avoid too many features
                    for pressure_feat in phld_pressure[:2]:
                        if hl_feat in df.columns and pressure_feat in df.columns:
                            feature_name = f"interaction_{hl_feat}_{pressure_feat}"
                            df[feature_name] = df[hl_feat] * df[pressure_feat]
                            self.log_feature_generation(feature_name, importance=0.5)
                            
            if phld_pv and wave_values:
                for pv_feat in phld_pv[:2]:
                    for wave_feat in wave_values[:2]:
                        if pv_feat in df.columns and wave_feat in df.columns:
                            feature_name = f"interaction_{pv_feat}_{wave_feat}"
                            df[feature_name] = df[pv_feat] * df[wave_feat]
                            self.log_feature_generation(feature_name, importance=0.6)
                            
        except Exception as e:
            logger.print_error(f"Error generating interaction features: {e}")
            
        return df
    
    def _generate_momentum_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate momentum-based features."""
        try:
            # Price momentum features
            for price_type in self.config.price_types:
                price_col = price_type.capitalize()
                if price_col in df.columns:
                    # Price momentum
                    for period in [5, 10, 20]:
                        df[f"price_momentum_{price_type}_{period}"] = df[price_col].pct_change(period)
                        self.log_feature_generation(f"price_momentum_{price_type}_{period}", importance=0.6)
                        
                        # Momentum acceleration
                        df[f"price_acceleration_{price_type}_{period}"] = df[f"price_momentum_{price_type}_{period}"].diff()
                        self.log_feature_generation(f"price_acceleration_{price_type}_{period}", importance=0.5)
                        
            # Volume momentum features
            if 'Volume' in df.columns:
                for period in [5, 10, 20]:
                    df[f"volume_momentum_{period}"] = df['Volume'].pct_change(period)
                    self.log_feature_generation(f"volume_momentum_{period}", importance=0.5)
                    
        except Exception as e:
            logger.print_error(f"Error generating momentum features: {e}")
            
        return df
    
    def get_feature_names(self) -> List[str]:
        """Get list of generated proprietary feature names."""
        return self.phld_features + self.wave_features + self.derivative_features
    
    def get_phld_features(self) -> List[str]:
        """Get list of PHLD feature names."""
        return self.phld_features.copy()
    
    def get_wave_features(self) -> List[str]:
        """Get list of Wave feature names."""
        return self.wave_features.copy()
    
    def get_derivative_features(self) -> List[str]:
        """Get list of derivative feature names."""
        return self.derivative_features.copy()
    
    def get_feature_categories(self) -> Dict[str, List[str]]:
        """Get features organized by category."""
        return {
            'phld': self.phld_features,
            'wave': self.wave_features,
            'derivative': self.derivative_features,
            'all': self.get_feature_names()
        }
