# -*- coding: utf-8 -*-
# src/ml/feature_engineering/technical_features.py

"""
Technical feature generator for NeoZorK HLD Prediction.

This module creates ML features based on standard technical indicators,
providing a comprehensive set of features for the ML trading system.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union, Any
import warnings
from dataclasses import dataclass

from .base_feature_generator import BaseFeatureGenerator, FeatureConfig
from .logger import logger

# Import technical indicators
try:
    from src.calculation.indicators.trend.sma_ind import apply_rule_sma
    from src.calculation.indicators.trend.ema_ind import apply_rule_ema
    from src.calculation.indicators.trend.adx_ind import apply_rule_adx
    from src.calculation.indicators.trend.sar_ind import apply_rule_sar
    from src.calculation.indicators.trend.supertrend_ind import apply_rule_supertrend
    from src.calculation.indicators.momentum.macd_ind import apply_rule_macd
    from src.calculation.indicators.oscillators.rsi_ind_calc import apply_rule_rsi
    from src.calculation.indicators.oscillators.stoch_ind import apply_rule_stochastic
    from src.calculation.indicators.oscillators.cci_ind import apply_rule_cci
    from src.calculation.indicators.volatility.bb_ind import apply_rule_bollinger_bands
    from src.calculation.indicators.volatility.atr_ind import apply_rule_atr
    from src.calculation.indicators.volume.vwap_ind import apply_rule_vwap
    from src.calculation.indicators.volume.obv_ind import apply_rule_obv
except ImportError as e:
    logger.print_warning(f"Some technical indicators not available: {e}")


@dataclass
class TechnicalFeatureConfig(FeatureConfig):
    """Configuration for technical feature generation."""
    
    # Moving average types
    ma_types: List[str] = None
    
    # RSI parameters
    rsi_periods: List[int] = None
    
    # MACD parameters
    macd_fast_periods: List[int] = None
    macd_slow_periods: List[int] = None
    macd_signal_periods: List[int] = None
    
    # Bollinger Bands parameters
    bb_periods: List[int] = None
    bb_std_devs: List[float] = None
    
    # ATR parameters
    atr_periods: List[int] = None
    
    # Stochastic parameters
    stoch_k_periods: List[int] = None
    stoch_d_periods: List[int] = None
    
    def __post_init__(self):
        """Set default values if not provided."""
        super().__post_init__()
        
        if self.ma_types is None:
            self.ma_types = ['sma', 'ema']
            
        if self.rsi_periods is None:
            self.rsi_periods = [14, 21, 50]
            
        if self.macd_fast_periods is None:
            self.macd_fast_periods = [12, 26]
            
        if self.macd_slow_periods is None:
            self.macd_slow_periods = [26, 52]
            
        if self.macd_signal_periods is None:
            self.macd_signal_periods = [9, 18]
            
        if self.bb_periods is None:
            self.bb_periods = [20, 50]
            
        if self.bb_std_devs is None:
            self.bb_std_devs = [2.0, 2.5]
            
        if self.atr_periods is None:
            self.atr_periods = [14, 20]
            
        if self.stoch_k_periods is None:
            self.stoch_k_periods = [14, 21]
            
        if self.stoch_d_periods is None:
            self.stoch_d_periods = [3, 5]


class TechnicalFeatureGenerator(BaseFeatureGenerator):
    """
    Generator for technical indicator features.
    
    This class creates ML features based on standard technical indicators,
    providing a comprehensive set of features for the ML system.
    """
    
    def __init__(self, config: TechnicalFeatureConfig = None):
        """
        Initialize the technical feature generator.
        
        Args:
            config: Configuration for technical feature generation
        """
        super().__init__(config or TechnicalFeatureConfig())
        self.ma_features = []
        self.momentum_features = []
        self.oscillator_features = []
        self.volatility_features = []
        self.volume_features = []
        
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate technical features from the input DataFrame.
        
        Args:
            df: Input DataFrame with OHLCV data
            
        Returns:
            DataFrame with original data plus technical features
        """
        if not self.validate_data(df):
            return df
            
        df_features = df.copy()
        
        # Generate moving average features
        df_features = self._generate_moving_average_features(df_features)
        
        # Generate momentum features
        df_features = self._generate_momentum_features(df_features)
        
        # Generate oscillator features
        df_features = self._generate_oscillator_features(df_features)
        
        # Generate volatility features
        df_features = self._generate_volatility_features(df_features)
        
        # Generate volume features
        df_features = self._generate_volume_features(df_features)
        
        # Generate trend features
        df_features = self._generate_trend_features(df_features)
        
        # Generate price action features
        df_features = self._generate_price_action_features(df_features)
        
        logger.print_info(f"Generated {self.features_generated} technical features")
        return df_features
    
    def _generate_moving_average_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate moving average features."""
        try:
            for ma_type in self.config.ma_types:
                for period in self.config.medium_periods + self.config.long_periods:
                    for price_type in self.config.price_types:
                        try:
                            if ma_type == 'sma':
                                # Calculate SMA
                                ma_values = df[price_type.capitalize()].rolling(period).mean()
                                feature_name = f"sma_{period}_{price_type}"
                                df[feature_name] = ma_values
                                self.log_feature_generation(feature_name, importance=0.7)
                                self.ma_features.append(feature_name)
                                
                                # Price vs MA ratio
                                df[f"{feature_name}_ratio"] = df[price_type.capitalize()] / ma_values
                                self.log_feature_generation(f"{feature_name}_ratio", importance=0.6)
                                
                                # Distance from MA
                                df[f"{feature_name}_distance"] = (df[price_type.capitalize()] - ma_values) / ma_values
                                self.log_feature_generation(f"{feature_name}_distance", importance=0.6)
                                
                            elif ma_type == 'ema':
                                # Calculate EMA
                                ma_values = df[price_type.capitalize()].ewm(span=period).mean()
                                feature_name = f"ema_{period}_{price_type}"
                                df[feature_name] = ma_values
                                self.log_feature_generation(feature_name, importance=0.7)
                                self.ma_features.append(feature_name)
                                
                                # Price vs MA ratio
                                df[f"{feature_name}_ratio"] = df[price_type.capitalize()] / ma_values
                                self.log_feature_generation(f"{feature_name}_ratio", importance=0.6)
                                
                                # Distance from MA
                                df[f"{feature_name}_distance"] = (df[price_type.capitalize()] - ma_values) / ma_values
                                self.log_feature_generation(f"{feature_name}_distance", importance=0.6)
                                
                        except Exception as e:
                            logger.print_warning(f"Error generating {ma_type} feature for period {period}, price {price_type}: {e}")
                            continue
                            
        except Exception as e:
            logger.print_error(f"Error generating moving average features: {e}")
            
        return df
    
    def _generate_momentum_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate momentum features."""
        try:
            # MACD features
            for fast in self.config.macd_fast_periods:
                for slow in self.config.macd_slow_periods:
                    if slow > fast:
                        for signal in self.config.macd_signal_periods:
                            try:
                                # Calculate MACD
                                macd_line = df['Close'].ewm(span=fast).mean() - df['Close'].ewm(span=slow).mean()
                                signal_line = macd_line.ewm(span=signal).mean()
                                histogram = macd_line - signal_line
                                
                                feature_name = f"macd_{fast}_{slow}_{signal}"
                                df[f"{feature_name}_line"] = macd_line
                                df[f"{feature_name}_signal"] = signal_line
                                df[f"{feature_name}_histogram"] = histogram
                                
                                self.log_feature_generation(f"{feature_name}_line", importance=0.8)
                                self.log_feature_generation(f"{feature_name}_signal", importance=0.7)
                                self.log_feature_generation(f"{feature_name}_histogram", importance=0.8)
                                
                                self.momentum_features.extend([
                                    f"{feature_name}_line", f"{feature_name}_signal", f"{feature_name}_histogram"
                                ])
                                
                                # MACD crossovers
                                df[f"{feature_name}_crossover"] = np.where(macd_line > signal_line, 1, -1)
                                self.log_feature_generation(f"{feature_name}_crossover", importance=0.7)
                                self.momentum_features.append(f"{feature_name}_crossover")
                                
                            except Exception as e:
                                logger.print_warning(f"Error generating MACD feature for {fast}_{slow}_{signal}: {e}")
                                continue
                                
        except Exception as e:
            logger.print_error(f"Error generating momentum features: {e}")
            
        return df
    
    def _generate_oscillator_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate oscillator features."""
        try:
            # RSI features
            for period in self.config.rsi_periods:
                try:
                    # Calculate RSI
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
                    rs = gain / loss
                    rsi = 100 - (100 / (1 + rs))
                    
                    feature_name = f"rsi_{period}"
                    df[feature_name] = rsi
                    self.log_feature_generation(feature_name, importance=0.8)
                    self.oscillator_features.append(feature_name)
                    
                    # RSI zones
                    df[f"{feature_name}_oversold"] = np.where(rsi < 30, 1, 0)
                    df[f"{feature_name}_overbought"] = np.where(rsi > 70, 1, 0)
                    df[f"{feature_name}_neutral"] = np.where((rsi >= 30) & (rsi <= 70), 1, 0)
                    
                    self.log_feature_generation(f"{feature_name}_oversold", importance=0.6)
                    self.log_feature_generation(f"{feature_name}_overbought", importance=0.6)
                    self.log_feature_generation(f"{feature_name}_neutral", importance=0.5)
                    
                    self.oscillator_features.extend([
                        f"{feature_name}_oversold", f"{feature_name}_overbought", f"{feature_name}_neutral"
                    ])
                    
                except Exception as e:
                    logger.print_warning(f"Error generating RSI feature for period {period}: {e}")
                    continue
                    
            # Stochastic features
            for k_period in self.config.stoch_k_periods:
                for d_period in self.config.stoch_d_periods:
                    try:
                        # Calculate Stochastic
                        lowest_low = df['Low'].rolling(window=k_period).min()
                        highest_high = df['High'].rolling(window=k_period).max()
                        k_percent = 100 * ((df['Close'] - lowest_low) / (highest_high - lowest_low))
                        d_percent = k_percent.rolling(window=d_period).mean()
                        
                        feature_name = f"stoch_{k_period}_{d_period}"
                        df[f"{feature_name}_k"] = k_percent
                        df[f"{feature_name}_d"] = d_percent
                        
                        self.log_feature_generation(f"{feature_name}_k", importance=0.7)
                        self.log_feature_generation(f"{feature_name}_d", importance=0.7)
                        
                        self.oscillator_features.extend([f"{feature_name}_k", f"{feature_name}_d"])
                        
                    except Exception as e:
                        logger.print_warning(f"Error generating Stochastic feature for {k_period}_{d_period}: {e}")
                        continue
                        
        except Exception as e:
            logger.print_error(f"Error generating oscillator features: {e}")
            
        return df
    
    def _generate_volatility_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate volatility features."""
        try:
            # ATR features
            for period in self.config.atr_periods:
                try:
                    # Calculate ATR
                    high_low = df['High'] - df['Low']
                    high_close = np.abs(df['High'] - df['Close'].shift())
                    low_close = np.abs(df['Low'] - df['Close'].shift())
                    true_range = np.maximum(high_low, np.maximum(high_close, low_close))
                    atr = true_range.rolling(window=period).mean()
                    
                    feature_name = f"atr_{period}"
                    df[feature_name] = atr
                    self.log_feature_generation(feature_name, importance=0.7)
                    self.volatility_features.append(feature_name)
                    
                    # ATR ratio
                    df[f"{feature_name}_ratio"] = atr / df['Close']
                    self.log_feature_generation(f"{feature_name}_ratio", importance=0.6)
                    self.volatility_features.append(f"{feature_name}_ratio")
                    
                except Exception as e:
                    logger.print_warning(f"Error generating ATR feature for period {period}: {e}")
                    continue
                    
            # Bollinger Bands features
            for period in self.config.bb_periods:
                for std_dev in self.config.bb_std_devs:
                    try:
                        # Calculate Bollinger Bands
                        sma = df['Close'].rolling(window=period).mean()
                        std = df['Close'].rolling(window=period).std()
                        upper_band = sma + (std * std_dev)
                        lower_band = sma - (std * std_dev)
                        
                        feature_name = f"bb_{period}_{int(std_dev*10)}"
                        df[f"{feature_name}_upper"] = upper_band
                        df[f"{feature_name}_lower"] = lower_band
                        df[f"{feature_name}_width"] = upper_band - lower_band
                        df[f"{feature_name}_percent_b"] = (df['Close'] - lower_band) / (upper_band - lower_band)
                        
                        self.log_feature_generation(f"{feature_name}_upper", importance=0.7)
                        self.log_feature_generation(f"{feature_name}_lower", importance=0.7)
                        self.log_feature_generation(f"{feature_name}_width", importance=0.6)
                        self.log_feature_generation(f"{feature_name}_percent_b", importance=0.7)
                        
                        self.volatility_features.extend([
                            f"{feature_name}_upper", f"{feature_name}_lower", 
                            f"{feature_name}_width", f"{feature_name}_percent_b"
                        ])
                        
                    except Exception as e:
                        logger.print_warning(f"Error generating Bollinger Bands feature for {period}_{std_dev}: {e}")
                        continue
                        
        except Exception as e:
            logger.print_error(f"Error generating volatility features: {e}")
            
        return df
    
    def _generate_volume_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate volume features."""
        try:
            if 'Volume' in df.columns:
                # Volume moving averages
                for period in self.config.volume_periods:
                    try:
                        # Volume SMA
                        feature_name = f"volume_sma_{period}"
                        df[feature_name] = df['Volume'].rolling(window=period).mean()
                        self.log_feature_generation(feature_name, importance=0.6)
                        self.volume_features.append(feature_name)
                        
                        # Volume ratio
                        df[f"{feature_name}_ratio"] = df['Volume'] / df[feature_name]
                        self.log_feature_generation(f"{feature_name}_ratio", importance=0.6)
                        self.volume_features.append(f"{feature_name}_ratio")
                        
                    except Exception as e:
                        logger.print_warning(f"Error generating volume feature for period {period}: {e}")
                        continue
                        
                # OBV (On-Balance Volume)
                try:
                    obv = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
                    df['obv'] = obv
                    self.log_feature_generation('obv', importance=0.7)
                    self.volume_features.append('obv')
                    
                    # OBV momentum
                    df['obv_momentum'] = obv.diff()
                    self.log_feature_generation('obv_momentum', importance=0.6)
                    self.volume_features.append('obv_momentum')
                    
                except Exception as e:
                    logger.print_warning(f"Error generating OBV features: {e}")
                    
        except Exception as e:
            logger.print_error(f"Error generating volume features: {e}")
            
        return df
    
    def _generate_trend_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate trend features."""
        try:
            # ADX features
            for period in self.config.medium_periods:
                try:
                    # Calculate ADX components
                    plus_dm = df['High'].diff()
                    minus_dm = df['Low'].diff()
                    plus_dm[plus_dm < 0] = 0
                    minus_dm[minus_dm > 0] = 0
                    
                    tr = pd.DataFrame({
                        'hl': df['High'] - df['Low'],
                        'hc': abs(df['High'] - df['Close'].shift(1)),
                        'lc': abs(df['Low'] - df['Close'].shift(1))
                    }).max(axis=1)
                    
                    plus_di = 100 * (plus_dm.rolling(period).mean() / tr.rolling(period).mean())
                    minus_di = 100 * (minus_dm.rolling(period).mean() / tr.rolling(period).mean())
                    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
                    adx = dx.rolling(period).mean()
                    
                    feature_name = f"adx_{period}"
                    df[f"{feature_name}_adx"] = adx
                    df[f"{feature_name}_plus_di"] = plus_di
                    df[f"{feature_name}_minus_di"] = minus_di
                    
                    self.log_feature_generation(f"{feature_name}_adx", importance=0.7)
                    self.log_feature_generation(f"{feature_name}_plus_di", importance=0.6)
                    self.log_feature_generation(f"{feature_name}_minus_di", importance=0.6)
                    
                    self.momentum_features.extend([
                        f"{feature_name}_adx", f"{feature_name}_plus_di", f"{feature_name}_minus_di"
                    ])
                    
                except Exception as e:
                    logger.print_warning(f"Error generating ADX feature for period {period}: {e}")
                    continue
                    
        except Exception as e:
            logger.print_error(f"Error generating trend features: {e}")
            
        return df
    
    def _generate_price_action_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate price action features."""
        try:
            # Candlestick patterns
            for period in [1, 2, 3]:
                try:
                    # Doji pattern
                    body_size = abs(df['Close'] - df['Open'])
                    wick_size = df['High'] - df['Low']
                    doji_threshold = 0.1
                    
                    df[f"doji_{period}"] = np.where(
                        (body_size / wick_size) < doji_threshold, 1, 0
                    )
                    self.log_feature_generation(f"doji_{period}", importance=0.5)
                    
                    # Hammer pattern
                    body_size = abs(df['Close'] - df['Open'])
                    lower_shadow = np.minimum(df['Open'], df['Close']) - df['Low']
                    upper_shadow = df['High'] - np.maximum(df['Open'], df['Close'])
                    
                    df[f"hammer_{period}"] = np.where(
                        (lower_shadow > 2 * body_size) & (upper_shadow < body_size), 1, 0
                    )
                    self.log_feature_generation(f"hammer_{period}", importance=0.5)
                    
                except Exception as e:
                    logger.print_warning(f"Error generating price action feature for period {period}: {e}")
                    continue
                    
            # Support and resistance levels
            for period in [20, 50, 100]:
                try:
                    # Support level (recent low)
                    support = df['Low'].rolling(window=period).min()
                    df[f"support_{period}"] = support
                    self.log_feature_generation(f"support_{period}", importance=0.6)
                    
                    # Resistance level (recent high)
                    resistance = df['High'].rolling(window=period).max()
                    df[f"resistance_{period}"] = resistance
                    self.log_feature_generation(f"resistance_{period}", importance=0.6)
                    
                    # Distance from support/resistance
                    df[f"distance_support_{period}"] = (df['Close'] - support) / df['Close']
                    df[f"distance_resistance_{period}"] = (resistance - df['Close']) / df['Close']
                    
                    self.log_feature_generation(f"distance_support_{period}", importance=0.5)
                    self.log_feature_generation(f"distance_resistance_{period}", importance=0.5)
                    
                except Exception as e:
                    logger.print_warning(f"Error generating support/resistance feature for period {period}: {e}")
                    continue
                    
        except Exception as e:
            logger.print_error(f"Error generating price action features: {e}")
            
        return df
    
    def get_feature_names(self) -> List[str]:
        """Get list of generated technical feature names."""
        return (self.ma_features + self.momentum_features + self.oscillator_features + 
                self.volatility_features + self.volume_features)
    
    def get_feature_categories(self) -> Dict[str, List[str]]:
        """Get features organized by category."""
        return {
            'moving_averages': self.ma_features,
            'momentum': self.momentum_features,
            'oscillators': self.oscillator_features,
            'volatility': self.volatility_features,
            'volume': self.volume_features,
            'all': self.get_feature_names()
        }
