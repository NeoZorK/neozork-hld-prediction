# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/wave_ind.py

"""
INDICATOR INFO:
Name: WAVE
Category Trend
Description: Wave  is a sophisticated trend-following indicator that combines multiple momentum calculations
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

    # Validate trading rules
    if not isinstance(wave_input_parameters.tr1, ENUM_MOM_TR):
        raise ValueError("tr1 must be a valid ENUM_MOM_TR value")
    if not isinstance(wave_input_parameters.tr2, ENUM_MOM_TR):
        raise ValueError("tr2 must be a valid ENUM_MOM_TR value")
    if not isinstance(wave_input_parameters.global_tr, ENUM_GLOBAL_TR):
        raise ValueError("global_tr must be a valid ENUM_GLOBAL_TR value")
