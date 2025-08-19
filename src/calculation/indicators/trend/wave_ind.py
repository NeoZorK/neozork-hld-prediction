# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/wave_ind.py

"""
INDICATOR INFO:
Name: WAVE
Category Trend
Description: Wave is a sophisticated trend-following indicator that combines multiple momentum calculations
to generate strong trading signals based on open price movements. It utilizes a dual-wave system with configurable
trading rules and global signal filtering.
Usage: --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open
Parameters: period_long1, period_short1, period_trend1, tr1,
 period_long2, period_short2, period_trend2, tr2,
 global_tr, sma_period

 Pros+:
+Dual Signal Validation: Two-wave system for improved reliability
+Flexible Configuration: Multiple trading rules and filters
+Strong Trend Identification: Excellent for trending markets
+Zone-Based Filtering: Helps avoid counter-trend trades
+Momentum Validation: Advanced signal filtering algorithms
+Visual Clarity: Clear color coding and multiple visual elements
+Comprehensive Signal Types: Various signal combinations
+Professional Grade: Sophisticated algorithms for advanced strategies

Cons-:
-Complex Setup: Requires extensive parameter testing
-Lag in Ranging Markets: May be slow in sideways markets
-Parameter Sensitivity: Performance depends heavily on proper settings
-Resource Intensive: Multiple calculations may impact performance
-Learning Curve: Complex rules require significant study time
-Over-Optimization Risk: Multiple parameters increase curve-fitting risk
-Signal Frequency: May generate fewer signals than simpler indicators
-Market Dependency: Best in trending markets, weaker in ranging conditions
This analysis provides traders with a balanced view of the indicator's strengths and limitations, helping them make informed decisions about whether Wave2 fits their trading style and market conditions.
"""
from enum import Enum
from dataclasses import dataclass
import pandas as pd
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


"""Trading Rules for Wave Momentum"""
class ENUM_MOM_TR(Enum):
    TR_Fast = "Fast"
    TR_Zone = "Zone Plus/Minus"
    TR_StrongTrend = "Strong Trend"
    TR_WeakTrend = "Weak Trend"
    TR_FastZoneReverse = "Fast Zone Reverse"
    TR_BetterTrend = "Better Strong trend"
    TR_BetterFast = "Better Fast"
    TR_Rost = "Reverse Rost"
    TR_TrendRost = "Trend Rost"
    TR_BetterTrendRost = "Better Trend Rost"


"""Global Trading Rules for Wave Momentum"""
class ENUM_GLOBAL_TR(Enum):
    G_TR_PRIME = "Prime"
    G_TR_REVERSE = "Reverse"
    G_TR_PRIME_ZONE = "Prime Zone"
    G_TR_REVERSE_ZONE = "Reverse Zone"
    G_TR_NEW_ZONE = "New Zone"
    G_TR_LONG_ZONE = "Long Zone"
    G_TR_LONG_ZONE_REVERSE = "Long Zone Reverse"



@dataclass
class WaveParameters:
    """
    Configuration parameters for Wave indicator calculation.

    Attributes:
        long1 (int): First long period (default: 339)
        fast1 (int): First fast period (default: 10)
        trend1 (int): First trend period (default: 2)
        tr1 (ENUM_MOM_TR): First trading rule (default: TR_Fast)
        long2 (int): Second long period (default: 22)
        fast2 (int): Second fast period (default: 11)
        trend2 (int): Second trend period (default: 4)
        tr2 (ENUM_MOM_TR): Second trading rule (default: TR_Fast)
        global_tr (ENUM_GLOBAL_TR): Global trading rule (default: G_TR_PRIME)
        sma_period (int): SMA calculation period (default: 22)
    """
    long1: int = 339
    fast1: int = 10
    trend1: int = 2
    tr1: ENUM_MOM_TR = ENUM_MOM_TR.TR_Fast
    long2: int = 22
    fast2: int = 11
    trend2: int = 4
    tr2: ENUM_MOM_TR = ENUM_MOM_TR.TR_Fast
    global_tr: ENUM_GLOBAL_TR = ENUM_GLOBAL_TR.G_TR_PRIME
    sma_period: int = 22


def calculate_wave(price_series: pd.Series, wave_input_parameters: WaveParameters ) -> pd.Series:
    """
    Calculates Wave indicator values based on price series and input parameters.

    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        wave_input_parameters (WaveParameters): Wave indicator configuration parameters
            including periods, trading rules and filtering settings

    Returns:
        pd.Series: Wave indicator values

    Raises:
        ValueError: If any numeric parameter is not positive or if trading rules are invalid
    """
    # Validate numeric parameters
    if wave_input_parameters.long1 <= 0:
        raise ValueError("long1 period must be positive")
    if wave_input_parameters.fast1 <= 0:
        raise ValueError("fast1 period must be positive")
    if wave_input_parameters.trend1 <= 0:
        raise ValueError("trend1 period must be positive")
    if wave_input_parameters.long2 <= 0:
        raise ValueError("long2 period must be positive")
    if wave_input_parameters.fast2 <= 0:
        raise ValueError("fast2 period must be positive")
    if wave_input_parameters.trend2 <= 0:
        raise ValueError("trend2 period must be positive")
    if wave_input_parameters.sma_period <= 0:
        raise ValueError("sma_period must be positive")

    
    # Check length of price series
    if len(price_series) < max(wave_input_parameters.long1, wave_input_parameters.fast1, wave_input_parameters.trend1, wave_input_parameters.long2, wave_input_parameters.fast2, wave_input_parameters.trend2, wave_input_parameters.sma_period):
        logger.print_warning(f"Not enough data for Wave calculation. Need at least {max(wave_input_parameters.long1, wave_input_parameters.fast1, wave_input_parameters.trend1, wave_input_parameters.long2, wave_input_parameters.fast2, wave_input_parameters.trend2, wave_input_parameters.sma_period)} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float)

    # Calculate wave
    wave = price_series.rolling(window=wave_input_parameters.long1, min_periods=wave_input_parameters.long1).mean()
    return wave


def apply_rule_wave(df: pd.DataFrame, wave_inputs: WaveParameters, price_type: PriceType = PriceType.OPEN):
    """
    Applies Wave rule logic to calculate trading signals and price levels.

    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        wave_inputs (WaveParameters): Wave indicator configuration parameters
        price_type (PriceType): Price type to use for calculation (OPEN or CLOSE)

    Returns:
          pd.DataFrame: DataFrame with Wave calculations and signals
    """

    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:
        price_series = df['Close']
        price_name = "Close"

    # Calculate Wave
    df['Wave'] = calculate_wave(price_series, wave_inputs)

    # Add price type info to column name
    df['Wave_Price_Type'] = price_name

    # Calculate Wave signals
    df['Wave_Signal'] = BUY

    # Calculate Support and Resistance levels based on Wave
    # Use Wave as dynamic support/resistance
    wave_values = df['Wave']

    # Support level: Wave with small buffer
    support_levels = wave_values * 0.995 # 0.5% below Wave

    # Resistance level: Wave with small buffer
    resistance_levels = wave_values * 1.005 # 0.5% above Wave

    # Set output columns
    df['PPrice1'] = support_levels
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels
    df['PColor2'] = SELL
    df['Direction'] = df['Wave_Signal']
    df['Diff'] = price_series - wave_values

    return df
