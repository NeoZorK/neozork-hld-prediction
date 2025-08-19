# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/wave_ind.py

"""
INDICATOR INFO:
Name: WAVE
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

from src.calculation.indicators.base_indicator import PriceType
from src.common import logger
from src.common.constants import BUY,SELL,NOTRADE


"""Trading Rules for Wave Momentum"""
class ENUM_MOM_TR(Enum):
    """Trading Rules for Wave Momentum

    TR_Fast: Basic momentum comparison
    TR_Zone: Simple zone-based signals
    TR_StrongTrend: Strong trend confirmation
    TR_WeakTrend: Weak trend signals
    TR_FastZoneReverse: Reverse signals in zones
    TR_BetterTrend: Enhanced trend signals avoiding false signals by comparing with previous values
    TR_BetterFast: Improved fast trading
    TR_Rost: Reverse momentum signals
    TR_TrendRost: Trend-based reverse signals
    TR_BetterTrendRost: Enhanced trend reverse signals
    """
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

    def __post_init__(self):
        # Init
        self.div_long1 = 2.0 / max(self.long1, 1)
        self.div_fast1 = 2.0 / max(self.fast1, 1)
        self.div_direction1 = 2.0 / (max(self.trend1, 1) + 1)
        self.div_long2 = 2.0 / max(self.long2, 1)
        self.div_fast2 = 2.0 / max(self.fast2, 1)
        self.div_direction2 = 2.0 / (max(self.trend2, 1) + 1)




def init_wave(price_series: pd.Series, wave_input_parameters: WaveParameters ):
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
    print(f"div_long1 value: {wave_input_parameters.div_long1}")
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



# 1
def calculate_ecore(div_long: float, price: pd.Series) -> pd.Series:
    """
    Calculates ECORE values based on price series and divisor.

    Args:
        div_long (float): Divisor value for ECORE calculation
        price (pd.Series): Price series data

    Returns:
        pd.Series: Calculated ECORE values
    """

    # Initialize ECORE series with zeros
    ecore = pd.Series(0.0, index=price.index)

    # Calculate initial diff
    prev_price = price.shift(1)
    diff = (price / prev_price - 1) * 100

    # Calculate ECORE recursively
    for i in range(1, len(price)):
        ecore.loc[ecore.index[i]] = ecore.iloc[i - 1] + div_long * (diff.iloc[i] - ecore.iloc[i - 1])

    return ecore

# 2
def calc_draw_lines(div_fast: float, div_dir: float, ecore: pd.Series) -> tuple[pd.Series, pd.Series]:
    """
    Calculates and returns two time series: 'wave' and 'fastline', representing smoothed versions
    of an input energy core series ('ecore'). The calculations are based on two divergence factors,
    'div_fast' and 'div_dir', which control the smoothing rate for each series respectively. The
    output is presented as a tuple of pandas Series.

    :param div_fast: A divergence factor controlling the smoothing of the 'wave' series.
    :param div_dir: A divergence factor controlling the smoothing of the 'fastline' series.
    :param ecore: A pandas Series representing the input energy core data, with index as time.
    :return: A tuple of two pandas Series, where the first element is the 'wave' series and the
        second element is the 'fastline' series.
    """
    wave = pd.Series(0.0, index=ecore.index)
    fastline = pd.Series(0.0, index=ecore.index)

    for i in range(1, len(ecore)):
        wave.loc[wave.index[i]] = wave.iloc[i - 1] + div_fast * (ecore.iloc[i] - wave.iloc[i - 1])
        fastline.loc[fastline.index[i]] = fastline.iloc[i - 1] + div_dir * (wave.iloc[i] - fastline.iloc[i - 1])

    return wave, fastline

# 3
def tr_switch(tr_rule: ENUM_MOM_TR, wave: pd.Series, fastline: pd.Series,
              prev_signal: float, prev_wave: float) -> pd.Series:
    """
    Applies trading rules to determine buy/sell signals based on Wave indicator values.

    Args:
        tr_rule: Trading rule to apply
        wave: Wave indicator values
        fastline: Fast line indicator values
        prev_signal: Previous trading signal
        prev_wave: Previous wave value

    Returns:
        colors: Series to store signal colors/values 
    """

    #
    colors = pd.Series(NOTRADE, index=wave.index)
    
    # Initialize previous values for tracking
    current_prev_signal = prev_signal
    current_prev_wave = prev_wave

    if len(wave) != len(fastline):
        raise ValueError("wave and fastline must have same length")

    for index in range(1, len(wave)):
        if tr_rule == ENUM_MOM_TR.TR_Zone:
            colors.loc[colors.index[index]] = BUY if wave.iloc[index] > 0 else SELL

        elif tr_rule == ENUM_MOM_TR.TR_Fast:
            colors.loc[colors.index[index]] = BUY if wave.iloc[index] > fastline.iloc[index] else SELL

        elif tr_rule == ENUM_MOM_TR.TR_StrongTrend:
            if wave.iloc[index] > 0:
                # PlusZone
                if wave.iloc[index] > fastline.iloc[index]:
                    colors.loc[colors.index[index]] = BUY
                else:
                    colors.loc[colors.index[index]] = NOTRADE
            else:
                # MinusZone 
                if wave.iloc[index] < fastline.iloc[index]:
                    colors.loc[colors.index[index]] = SELL
                else:
                    colors.loc[colors.index[index]] = NOTRADE

        elif tr_rule == ENUM_MOM_TR.TR_WeakTrend:
            if wave.iloc[index] > 0:
                # PlusZone
                if wave.iloc[index] < fastline.iloc[index]:
                    colors.loc[colors.index[index]] = BUY
                else:
                    colors.loc[colors.index[index]] = NOTRADE
            else:
                # MinusZone
                if wave.iloc[index] > fastline.iloc[index]:
                    colors.loc[colors.index[index]] = SELL
                else:
                    colors.loc[colors.index[index]] = NOTRADE

        elif tr_rule == ENUM_MOM_TR.TR_FastZoneReverse:
            if wave.iloc[index] > 0:
                # PlusZone
                if wave.iloc[index] < fastline.iloc[index]:
                    colors.loc[colors.index[index]] = SELL
                else:
                    colors.loc[colors.index[index]] = NOTRADE
            else:
                # MinusZone
                if wave.iloc[index] > fastline.iloc[index]:
                    colors.loc[colors.index[index]] = BUY
                else:
                    colors.loc[colors.index[index]] = NOTRADE

        elif tr_rule == ENUM_MOM_TR.TR_BetterTrend:
            if (wave.iloc[index - 1] < 0) and (wave.iloc[index] > 0):
                if wave.iloc[index] > fastline.iloc[index]:
                    current_prev_signal = BUY
                    current_prev_wave = wave.iloc[index]
                    colors.loc[colors.index[index]] = BUY
            elif (wave.iloc[index - 1] > 0) and (wave.iloc[index] < 0):
                if wave.iloc[index] < fastline.iloc[index]:
                    current_prev_signal = SELL
                    current_prev_wave = wave.iloc[index]
                    colors.loc[colors.index[index]] = SELL
            elif wave.iloc[index] > fastline.iloc[index]:
                if current_prev_signal == BUY and wave.iloc[index] > current_prev_wave:
                    colors.loc[colors.index[index]] = BUY
                    current_prev_wave = wave.iloc[index]
            elif wave.iloc[index] < fastline.iloc[index]:
                if current_prev_signal == SELL and wave.iloc[index] < current_prev_wave:
                    colors.loc[colors.index[index]] = SELL
                    current_prev_wave = wave.iloc[index]
            else:
                colors.loc[colors.index[index]] = NOTRADE

        elif tr_rule == ENUM_MOM_TR.TR_BetterFast:
            # First signals in positive/negative zones
            if (wave.iloc[index - 1] < 0) and (wave.iloc[index] > 0):
                if wave.iloc[index] > fastline.iloc[index]:
                    current_prev_signal = BUY
                    current_prev_wave = wave.iloc[index]
                    colors.loc[colors.index[index]] = BUY
                    continue
            elif (wave.iloc[index - 1] > 0) and (wave.iloc[index] < 0):
                if wave.iloc[index] < fastline.iloc[index]:
                    current_prev_signal = SELL
                    current_prev_wave = wave.iloc[index]
                    colors.loc[colors.index[index]] = SELL
                    continue

            # Second signals in same zone
            if wave.iloc[index] > fastline.iloc[index]:
                if current_prev_signal == BUY:
                    if wave.iloc[index] > current_prev_wave:
                        colors.loc[colors.index[index]] = BUY
                        current_prev_wave = wave.iloc[index]
                    else:
                        colors.loc[colors.index[index]] = SELL
                    continue

            if wave.iloc[index] < fastline.iloc[index]:
                if current_prev_signal == SELL:
                    if wave.iloc[index] < current_prev_wave:
                        colors.loc[colors.index[index]] = SELL
                        current_prev_wave = wave.iloc[index]
                    else:
                        colors.loc[colors.index[index]] = BUY
                    continue

            # Reverse signals
            if (wave.iloc[index] < 0) and (wave.iloc[index] > fastline.iloc[index]):
                colors.loc[colors.index[index]] = BUY
                continue

            if (wave.iloc[index] > 0) and (wave.iloc[index] < fastline.iloc[index]):
                colors.loc[colors.index[index]] = SELL
                continue

    return colors

# 4
def global_tr_switch(global_tr: ENUM_GLOBAL_TR, wave1: pd.Series, wave2: pd.Series, 
                    fastline1: pd.Series, fastline2: pd.Series, color1: pd.Series, 
                    color2: pd.Series) -> tuple[pd.Series, pd.Series, pd.Series]:
    """
    Applies global trading rules to combine signals from two wave indicators.

    Args:
        global_tr: Global trading rule to apply
        wave1: First wave indicator values
        wave2: Second wave indicator values
        fastline1: First fast line indicator values
        fastline2: Second fast line indicator values
        color1: First wave trading signals
        color2: Second wave trading signals

    Returns:
        tuple: (plot_color, plot_wave, plot_fastline) - Combined signals and values
    """
    
    # Initialize output series
    plot_color = pd.Series(NOTRADE, index=wave1.index)
    plot_wave = wave1.copy()
    plot_fastline = fastline1.copy()
    
    # Apply global trading rule
    if global_tr == ENUM_GLOBAL_TR.G_TR_PRIME:
        plot_color = g_prime_tr(wave1, wave2, fastline1, fastline2, color1, color2)
    elif global_tr == ENUM_GLOBAL_TR.G_TR_REVERSE:
        plot_color = g_reverse_tr(wave1, wave2, fastline1, fastline2, color1, color2)
    elif global_tr == ENUM_GLOBAL_TR.G_TR_PRIME_ZONE:
        plot_color = g_prime_tr_zone(wave1, wave2, fastline1, fastline2, color1, color2)
    elif global_tr == ENUM_GLOBAL_TR.G_TR_REVERSE_ZONE:
        plot_color = g_reverse_tr_zone(wave1, wave2, fastline1, fastline2, color1, color2)
    elif global_tr == ENUM_GLOBAL_TR.G_TR_NEW_ZONE:
        plot_color = g_new_zone_tr(wave1, wave2, fastline1, fastline2, color1, color2)
    elif global_tr == ENUM_GLOBAL_TR.G_TR_LONG_ZONE:
        plot_color = g_long_zone_tr(wave1, wave2, fastline1, fastline2, color1, color2)
    elif global_tr == ENUM_GLOBAL_TR.G_TR_LONG_ZONE_REVERSE:
        plot_color = g_long_zone_reverse_tr(wave1, wave2, fastline1, fastline2, color1, color2)
    else:
        # Default to G_TR_PRIME
        plot_color = g_prime_tr(wave1, wave2, fastline1, fastline2, color1, color2)
    
    return plot_color, plot_wave, plot_fastline

# 5


def sma_calculation(period: int, source_arr: pd.Series) -> pd.Series:
    """
    Calculates Simple Moving Average (SMA) for the given period and source array.

    Args:
        period (int): Calculation period for SMA
        source_arr (pd.Series): Source data array

    Returns:
        pd.Series: Series with SMA values for each index

    Raises:
        ValueError: If period is not positive or not enough data points
    """
    # Check if period is positive
    if period <= 0:
        raise ValueError("Period must be positive")

    # Check if we have enough data
    if len(source_arr) < period:
        raise ValueError("Not enough data points")

    # Create result series with same index
    result = pd.Series(0.0, index=source_arr.index)
    
    # Calculate SMA for each index
    for i in range(len(source_arr)):
        if i < period - 1:
            # For initial values (before we have enough data), use the current value
            result.iloc[i] = source_arr.iloc[i]
        else:
            # Calculate SMA for the period ending at current index
            start_idx = i - period + 1
            end_idx = i + 1
            sma_value = source_arr.iloc[start_idx:end_idx].mean()
            result.iloc[i] = sma_value
    
    return result


def g_prime_tr(wave1: pd.Series, wave2: pd.Series, fastline1: pd.Series,
               fastline2: pd.Series, color1: pd.Series, color2: pd.Series) -> pd.Series:
    """
    Global Prime TR - Use mix of Wave1 & Wave2 and FastLine1 & FastLine2 and Color1 & Color2.
    If both signals are the same, then signal to trade.

    Args:
        wave1: First wave indicator values
        wave2: Second wave indicator values
        fastline1: First fast line indicator values
        fastline2: Second fast line indicator values
        color1: First wave trading signals
        color2: Second wave trading signals

    Returns:
        pd.Series: Combined trading signals
    """
    plot_color = pd.Series(NOTRADE, index=color1.index)
    
    for i in range(len(color1)):
        # Exit when empty one of two
        if color1.iloc[i] == NOTRADE or color2.iloc[i] == NOTRADE:
            continue
            
        # If same, then signal to trade
        if color1.iloc[i] == color2.iloc[i]:
            plot_color.loc[plot_color.index[i]] = color1.iloc[i]
    
    return plot_color


def g_reverse_tr(wave1: pd.Series, wave2: pd.Series, fastline1: pd.Series, 
                fastline2: pd.Series, color1: pd.Series, color2: pd.Series) -> pd.Series:
    """
    Global Reverse TR - Reverse the signals when both are the same.

    Args:
        wave1: First wave indicator values
        wave2: Second wave indicator values
        fastline1: First fast line indicator values
        fastline2: Second fast line indicator values
        color1: First wave trading signals
        color2: Second wave trading signals

    Returns:
        pd.Series: Reversed trading signals
    """
    plot_color = pd.Series(NOTRADE, index=color1.index)
    
    for i in range(len(color1)):
        # Exit when empty one of two
        if color1.iloc[i] == NOTRADE or color2.iloc[i] == NOTRADE:
            continue
            
        # If same, then reverse signal to trade
        if color1.iloc[i] == color2.iloc[i]:
            plot_color.loc[plot_color.index[i]] = SELL if color1.iloc[i] == BUY else BUY
    
    return plot_color


def g_prime_tr_zone(wave1: pd.Series, wave2: pd.Series, fastline1: pd.Series, 
                   fastline2: pd.Series, color1: pd.Series, color2: pd.Series) -> pd.Series:
    """
    Global Prime TR + Zone - Sell only in upper zone & buy only in lower zone.

    Args:
        wave1: First wave indicator values
        wave2: Second wave indicator values
        fastline1: First fast line indicator values
        fastline2: Second fast line indicator values
        color1: First wave trading signals
        color2: Second wave trading signals

    Returns:
        pd.Series: Zone-filtered trading signals
    """
    plot_color = pd.Series(NOTRADE, index=color1.index)
    
    for i in range(len(color1)):
        # Exit when empty one of two
        if color1.iloc[i] == NOTRADE or color2.iloc[i] == NOTRADE:
            continue
            
        # If same, then check zone conditions
        if color1.iloc[i] == color2.iloc[i]:
            # Check BUY in lower zone (wave1 < 0)
            if wave1.iloc[i] < 0 and color1.iloc[i] == BUY:
                plot_color.loc[plot_color.index[i]] = color1.iloc[i]
            # Check SELL in upper zone (wave1 > 0)
            elif wave1.iloc[i] > 0 and color1.iloc[i] == SELL:
                plot_color.loc[plot_color.index[i]] = color1.iloc[i]
    
    return plot_color


def g_reverse_tr_zone(wave1: pd.Series, wave2: pd.Series, fastline1: pd.Series, 
                     fastline2: pd.Series, color1: pd.Series, color2: pd.Series) -> pd.Series:
    """
    Global Reverse TR + Zone - Reversed sell only in upper zone & buy only in lower zone.

    Args:
        wave1: First wave indicator values
        wave2: Second wave indicator values
        fastline1: First fast line indicator values
        fastline2: Second fast line indicator values
        color1: First wave trading signals
        color2: Second wave trading signals

    Returns:
        pd.Series: Reversed zone-filtered trading signals
    """
    plot_color = pd.Series(NOTRADE, index=color1.index)
    
    for i in range(len(color1)):
        # Exit when empty one of two
        if color1.iloc[i] == NOTRADE or color2.iloc[i] == NOTRADE:
            continue
            
        # If same, then check zone conditions with reverse
        if color1.iloc[i] == color2.iloc[i]:
            # Check BUY in lower zone (wave1 < 0) -> reverse to SELL
            if wave1.iloc[i] < 0 and color1.iloc[i] == BUY:
                plot_color.loc[plot_color.index[i]] = SELL
            # Check SELL in upper zone (wave1 > 0) -> reverse to BUY
            elif wave1.iloc[i] > 0 and color1.iloc[i] == SELL:
                plot_color.loc[plot_color.index[i]] = BUY
    
    return plot_color


def g_new_zone_tr(wave1: pd.Series, wave2: pd.Series, fastline1: pd.Series, 
                 fastline2: pd.Series, color1: pd.Series, color2: pd.Series) -> pd.Series:
    """
    Global New Zone TR - Generate signals when wave indicators disagree.

    Args:
        wave1: First wave indicator values
        wave2: Second wave indicator values
        fastline1: First fast line indicator values
        fastline2: Second fast line indicator values
        color1: First wave trading signals
        color2: Second wave trading signals

    Returns:
        pd.Series: New zone trading signals
    """
    plot_color = pd.Series(NOTRADE, index=color1.index)
    last_signal = pd.Series(NOTRADE, index=color1.index)
    
    for i in range(len(color1)):
        # Update last signal
        if i > 0:
            last_signal.loc[last_signal.index[i]] = last_signal.iloc[i-1]
        
        # Update last signal when both agree
        if color1.iloc[i] == color2.iloc[i] and color1.iloc[i] != NOTRADE:
            last_signal.loc[last_signal.index[i]] = color1.iloc[i]
        
        # When signals are not the same, generate opposite signal
        if color1.iloc[i] != color2.iloc[i]:
            if last_signal.iloc[i] == BUY:
                plot_color.loc[plot_color.index[i]] = SELL
            elif last_signal.iloc[i] == SELL:
                plot_color.loc[plot_color.index[i]] = BUY
    
    return plot_color


def g_long_zone_tr(wave1: pd.Series, wave2: pd.Series, fastline1: pd.Series, 
                  fastline2: pd.Series, color1: pd.Series, color2: pd.Series) -> pd.Series:
    """
    Global Long Zone TR - Always generate opposite signal to last signal.

    Args:
        wave1: First wave indicator values
        wave2: Second wave indicator values
        fastline1: First fast line indicator values
        fastline2: Second fast line indicator values
        color1: First wave trading signals
        color2: Second wave trading signals

    Returns:
        pd.Series: Long zone trading signals
    """
    plot_color = pd.Series(NOTRADE, index=color1.index)
    last_signal = pd.Series(NOTRADE, index=color1.index)
    
    for i in range(len(color1)):
        # Update last signal
        if i > 0:
            last_signal.loc[last_signal.index[i]] = last_signal.iloc[i-1]
        
        # Update last signal when both agree
        if color1.iloc[i] == color2.iloc[i] and color1.iloc[i] != NOTRADE:
            last_signal.loc[last_signal.index[i]] = color1.iloc[i]
        
        # Main signal - always opposite to last signal
        if last_signal.iloc[i] == BUY:
            plot_color.iloc[i] = SELL
        elif last_signal.iloc[i] == SELL:
            plot_color.iloc[i] = BUY
    
    return plot_color


def g_long_zone_reverse_tr(wave1: pd.Series, wave2: pd.Series, fastline1: pd.Series, 
                          fastline2: pd.Series, color1: pd.Series, color2: pd.Series) -> pd.Series:
    """
    Global Long Zone Reverse TR - Always use the last signal.

    Args:
        wave1: First wave indicator values
        wave2: Second wave indicator values
        fastline1: First fast line indicator values
        fastline2: Second fast line indicator values
        color1: First wave trading signals
        color2: Second wave trading signals

    Returns:
        pd.Series: Long zone reverse trading signals
    """
    plot_color = pd.Series(NOTRADE, index=color1.index)
    last_signal = pd.Series(NOTRADE, index=color1.index)
    
    for i in range(len(color1)):
        # Update last signal
        if i > 0:
            last_signal.loc[last_signal.index[i]] = last_signal.iloc[i-1]
        
        # Update last signal when both agree
        if color1.iloc[i] == color2.iloc[i] and color1.iloc[i] != NOTRADE:
            last_signal.loc[last_signal.index[i]] = color1.iloc[i]
        
        # Main signal - always use last signal
        plot_color.loc[plot_color.index[i]] = last_signal.iloc[i]
    
    return plot_color


# 0
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

    # Init Wave
    init_wave(price_series, wave_inputs)

    # Default Signals
    df['_Signal'] = NOTRADE
    df['_Direction'] = NOTRADE
    df['_LastSignal'] = NOTRADE

    # Calculate ECORE 1 and 2
    df['ecore1'] = calculate_ecore(wave_inputs.div_long1, price_series)
    df['ecore2'] = calculate_ecore(wave_inputs.div_long2, price_series)

    # Calculate Draw Lines 1 and 2
    df['wave1'], df['fastline1'] = calc_draw_lines(wave_inputs.div_fast1, wave_inputs.div_direction1, df['ecore1'])
    df['wave2'], df['fastline2'] = calc_draw_lines(wave_inputs.div_fast2, wave_inputs.div_direction2, df['ecore2'])

    # Check length of wave and fastline series
    if len(df['wave1']) != len(df['fastline1']):
        raise ValueError("wave and fastline must have same length")
    if len(df['wave2']) != len(df['fastline2']):
        raise ValueError("wave and fastline must have same length")

    # Switch Trading Rules
    df['Wave1'] = tr_switch(wave_inputs.tr1, df['wave1'], df['fastline1'], NOTRADE, 0.0)
    df['Wave2'] = tr_switch(wave_inputs.tr2, df['wave2'], df['fastline2'], NOTRADE, 0.0)

    # Global TR Switch - Combine signals from both wave indicators
    df['_Plot_Color'], df['_Plot_Wave'], df['_Plot_FastLine'] = global_tr_switch(
        wave_inputs.global_tr, df['wave1'], df['wave2'], 
        df['fastline1'], df['fastline2'], df['Wave1'], df['Wave2']
    )

    # SMA Calculation - Use _Plot_FastLine as source (as in MQ5)
    df['MA_Line'] = sma_calculation(wave_inputs.sma_period, df['_Plot_FastLine'])

    # Direction
    df['_Direction'] = df['_Plot_Color']

    # Signal - Only when _Direction changes (as in MQ5)
    for i in range(1, len(df)):
        if df['_Direction'].iloc[i] != df['_Direction'].iloc[i - 1]:
            df.loc[df.index[i], '_Signal'] = df['_Direction'].iloc[i]

    # DONE

    return df
