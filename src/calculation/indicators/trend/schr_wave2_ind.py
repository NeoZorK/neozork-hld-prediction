# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/schr_wave2_ind.py

"""
INDICATOR INFO:
Name: SCHR_Wave2
Category: Trend
Description: SCHR Wave2 - Advanced dual-wave trend prediction indicator
Usage: --rule schr_wave2 or --rule schr_wave2:339,10,2,Fast,22,11,4,Fast,Prime,22
Parameters: long1,fast1,trend1,tr1,long2,fast2,trend2,tr2,global_tr,sma_period
Pros: + Dual-wave analysis, + Multiple trading rules, + Global rule combinations
Cons: - Complex parameter tuning, - Multiple calculation paths
File: src/calculation/indicators/trend/schr_wave2_ind.py

SCHR Wave2 indicator calculation module.
Based on MQL5 SCHR_Wave2.mq5 by Shcherbyna Rostyslav.
"""

import pandas as pd
import numpy as np
from typing import Optional, Union
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


class TradingRuleEnum:
    """Trading rule enumeration for SCHR_Wave2 indicator."""
    TR_FAST = 0
    TR_ZONE = 1
    TR_STRONG_TREND = 2
    TR_WEAK_TREND = 3
    TR_FAST_ZONE_REVERSE = 4
    TR_BETTER_TREND = 5
    TR_BETTER_FAST = 6
    TR_ROST = 7
    TR_TREND_ROST = 8
    TR_BETTER_TREND_ROST = 9


class GlobalTradingRuleEnum:
    """Global trading rule enumeration for SCHR_Wave2 indicator."""
    G_TR_PRIME = 0
    G_TR_REVERSE = 1
    G_TR_PRIME_ZONE = 2
    G_TR_REVERSE_ZONE = 3
    G_TR_NEW_ZONE = 4
    G_TR_LONG_ZONE = 5
    G_TR_LONG_ZONE_REVERSE = 6


def get_trading_rule_enum(tr_name: Union[int, str]) -> int:
    """
    Convert trading rule name to enum value.
    
    Args:
        tr_name: Trading rule name or enum value
        
    Returns:
        int: Trading rule enum value
    """
    if isinstance(tr_name, int):
        return tr_name
    
    tr_map = {
        'fast': TradingRuleEnum.TR_FAST,
        'zone': TradingRuleEnum.TR_ZONE,
        'strongtrend': TradingRuleEnum.TR_STRONG_TREND,
        'weaktrend': TradingRuleEnum.TR_WEAK_TREND,
        'fastzonereverse': TradingRuleEnum.TR_FAST_ZONE_REVERSE,
        'bettertrend': TradingRuleEnum.TR_BETTER_TREND,
        'betterfast': TradingRuleEnum.TR_BETTER_FAST,
        'rost': TradingRuleEnum.TR_ROST,
        'trendrost': TradingRuleEnum.TR_TREND_ROST,
        'bettertrendrost': TradingRuleEnum.TR_BETTER_TREND_ROST
    }
    
    return tr_map.get(tr_name.lower(), TradingRuleEnum.TR_FAST)


def get_global_trading_rule_enum(global_tr_name: Union[int, str]) -> int:
    """
    Convert global trading rule name to enum value.
    
    Args:
        global_tr_name: Global trading rule name or enum value
        
    Returns:
        int: Global trading rule enum value
    """
    if isinstance(global_tr_name, int):
        return global_tr_name
    
    global_tr_map = {
        'prime': GlobalTradingRuleEnum.G_TR_PRIME,
        'reverse': GlobalTradingRuleEnum.G_TR_REVERSE,
        'primezone': GlobalTradingRuleEnum.G_TR_PRIME_ZONE,
        'reversezone': GlobalTradingRuleEnum.G_TR_REVERSE_ZONE,
        'newzone': GlobalTradingRuleEnum.G_TR_NEW_ZONE,
        'longzone': GlobalTradingRuleEnum.G_TR_LONG_ZONE,
        'longzonereverse': GlobalTradingRuleEnum.G_TR_LONG_ZONE_REVERSE
    }
    
    return global_tr_map.get(global_tr_name.lower(), GlobalTradingRuleEnum.G_TR_PRIME)


def calculate_ecore(open_prices: pd.Series, div: float) -> pd.Series:
    """
    Calculate ECORE (Exponential Change of Rate) values.
    Exactly matches MQL5 CalculateECORE function.
    
    Args:
        open_prices: Series of open prices
        div: Division factor (2.0 / period)
        
    Returns:
        pd.Series: ECORE values
    """
    if len(open_prices) < 2:
        # Return empty series for insufficient data
        return pd.Series([], dtype=float)
    
    # Initialize result array
    ecore = pd.Series(index=open_prices.index, dtype=float)
    ecore.iloc[0] = 0.0  # First value
    
    # Calculate ECORE for each bar
    for i in range(1, len(open_prices)):
        # Calculate price difference as percentage
        diff = (open_prices.iloc[i] / open_prices.iloc[i-1] - 1) * 100
        # Apply exponential smoothing
        ecore.iloc[i] = ecore.iloc[i-1] + div * (diff - ecore.iloc[i-1])
    
    return ecore


def calculate_draw_lines(ecore: pd.Series, div_fast: float, div_dir: float) -> tuple[pd.Series, pd.Series]:
    """
    Calculate Wave and FastLine values.
    Exactly matches MQL5 CalcDrawLines function.
    
    Args:
        ecore: ECORE values
        div_fast: Fast division factor (2.0 / fast_period)
        div_dir: Direction division factor (2.0 / (trend_period + 1))
        
    Returns:
        tuple: (Wave values, FastLine values)
    """
    if len(ecore) < 2:
        # Return empty series for insufficient data
        return pd.Series([], dtype=float), pd.Series([], dtype=float)
    
    # Initialize arrays
    wave = pd.Series(index=ecore.index, dtype=float)
    fast_line = pd.Series(index=ecore.index, dtype=float)
    
    # First values
    wave.iloc[0] = 0.0
    fast_line.iloc[0] = 0.0
    
    # Calculate Wave and FastLine for each bar
    for i in range(1, len(ecore)):
        # Wave calculation
        wave.iloc[i] = wave.iloc[i-1] + div_fast * (ecore.iloc[i] - wave.iloc[i-1])
        # FastLine calculation
        fast_line.iloc[i] = fast_line.iloc[i-1] + div_dir * (wave.iloc[i] - fast_line.iloc[i-1])
    
    return wave, fast_line


def apply_trading_rule(wave: pd.Series, fast_line: pd.Series, tr_enum: int) -> pd.Series:
    """
    Apply trading rule to generate color signals.
    Exactly matches MQL5 TR_SWITCH function.
    
    Args:
        wave: Wave values
        fast_line: FastLine values
        tr_enum: Trading rule enum value
        
    Returns:
        pd.Series: Color signals (0=NOTRADE, 1=BUY, 2=SELL)
    """
    if len(wave) < 2 or len(fast_line) < 2:
        # Return empty series for insufficient data
        return pd.Series([], dtype=float)
    
    # Initialize result array
    color = pd.Series(index=wave.index, dtype=float)
    color.iloc[0] = NOTRADE  # First value
    
    # Apply trading rule for each bar
    for i in range(1, len(wave)):
        if tr_enum == TradingRuleEnum.TR_ZONE:
            # Zone rule: BUY if Wave > 0, SELL if Wave < 0
            color.iloc[i] = BUY if wave.iloc[i] > 0 else SELL
            
        elif tr_enum == TradingRuleEnum.TR_FAST:
            # Fast rule: BUY if Wave > FastLine, SELL if Wave < FastLine
            color.iloc[i] = BUY if wave.iloc[i] > fast_line.iloc[i] else SELL
            
        elif tr_enum == TradingRuleEnum.TR_STRONG_TREND:
            # Strong Trend rule
            if wave.iloc[i] > 0:  # Plus zone
                if wave.iloc[i] > fast_line.iloc[i]:
                    color.iloc[i] = BUY
                else:
                    color.iloc[i] = NOTRADE
            else:  # Minus zone
                if wave.iloc[i] < fast_line.iloc[i]:
                    color.iloc[i] = SELL
                else:
                    color.iloc[i] = NOTRADE
                    
        elif tr_enum == TradingRuleEnum.TR_WEAK_TREND:
            # Weak Trend rule
            if wave.iloc[i] > 0:  # Plus zone
                if wave.iloc[i] < fast_line.iloc[i]:
                    color.iloc[i] = BUY
                else:
                    color.iloc[i] = NOTRADE
            else:  # Minus zone
                if wave.iloc[i] > fast_line.iloc[i]:
                    color.iloc[i] = SELL
                else:
                    color.iloc[i] = NOTRADE
                    
        elif tr_enum == TradingRuleEnum.TR_FAST_ZONE_REVERSE:
            # Fast Zone Reverse rule
            if wave.iloc[i] > 0:  # Plus zone
                if wave.iloc[i] < fast_line.iloc[i]:
                    color.iloc[i] = SELL
                else:
                    color.iloc[i] = NOTRADE
            else:  # Minus zone
                if wave.iloc[i] > fast_line.iloc[i]:
                    color.iloc[i] = BUY
                else:
                    color.iloc[i] = NOTRADE
                    
        else:
            # Default to Fast rule
            color.iloc[i] = BUY if wave.iloc[i] > fast_line.iloc[i] else SELL
    
    return color


def apply_global_trading_rule(color1: pd.Series, color2: pd.Series, wave1: pd.Series, 
                             fast_line1: pd.Series, global_tr_enum: int) -> tuple[pd.Series, pd.Series, pd.Series]:
    """
    Apply global trading rule to combine signals from both waves.
    Exactly matches MQL5 global TR functions.
    
    Args:
        color1: Color signals from first wave
        color2: Color signals from second wave
        wave1: Wave values from first wave
        fast_line1: Fast line values from first wave
        global_tr_enum: Global trading rule enum value
        
    Returns:
        tuple: (Final color signals, Final wave values, Final fast line values)
    """
    if len(color1) < 2 or len(color2) < 2 or len(wave1) < 2 or len(fast_line1) < 2:
        # Return empty series for insufficient data
        return pd.Series([], dtype=float), pd.Series([], dtype=float), pd.Series([], dtype=float)
    
    # Initialize result arrays
    final_color = pd.Series(index=color1.index, dtype=float)
    final_wave = pd.Series(index=color1.index, dtype=float)
    final_fast_line = pd.Series(index=color1.index, dtype=float)
    
    # Set default values
    final_wave.iloc[0] = wave1.iloc[0]
    final_fast_line.iloc[0] = fast_line1.iloc[0]
    final_color.iloc[0] = NOTRADE
    
    # Apply global trading rule for each bar
    for i in range(1, len(color1)):
        final_wave.iloc[i] = wave1.iloc[i]
        final_fast_line.iloc[i] = fast_line1.iloc[i]  # Use actual fast_line1 values
        
        if global_tr_enum == GlobalTradingRuleEnum.G_TR_PRIME:
            # Prime rule: Use both signals when they agree
            if color1.iloc[i] != NOTRADE and color2.iloc[i] != NOTRADE:
                if color1.iloc[i] == color2.iloc[i]:
                    final_color.iloc[i] = color1.iloc[i]
                else:
                    final_color.iloc[i] = NOTRADE
            else:
                final_color.iloc[i] = NOTRADE
                
        elif global_tr_enum == GlobalTradingRuleEnum.G_TR_REVERSE:
            # Reverse rule: Reverse the signal when both agree
            if color1.iloc[i] != NOTRADE and color2.iloc[i] != NOTRADE:
                if color1.iloc[i] == color2.iloc[i]:
                    final_color.iloc[i] = SELL if color1.iloc[i] == BUY else BUY
                else:
                    final_color.iloc[i] = NOTRADE
            else:
                final_color.iloc[i] = NOTRADE
                
        elif global_tr_enum == GlobalTradingRuleEnum.G_TR_PRIME_ZONE:
            # Prime Zone rule: Prime + zone filtering
            if color1.iloc[i] != NOTRADE and color2.iloc[i] != NOTRADE:
                if color1.iloc[i] == color2.iloc[i]:
                    if wave1.iloc[i] < 0 and color1.iloc[i] == BUY:
                        final_color.iloc[i] = BUY
                    elif wave1.iloc[i] > 0 and color1.iloc[i] == SELL:
                        final_color.iloc[i] = SELL
                    else:
                        final_color.iloc[i] = NOTRADE
                else:
                    final_color.iloc[i] = NOTRADE
            else:
                final_color.iloc[i] = NOTRADE
                
        else:
            # Default to Prime rule
            if color1.iloc[i] != NOTRADE and color2.iloc[i] != NOTRADE:
                if color1.iloc[i] == color2.iloc[i]:
                    final_color.iloc[i] = color1.iloc[i]
                else:
                    final_color.iloc[i] = NOTRADE
            else:
                final_color.iloc[i] = NOTRADE
    
    return final_color, final_wave, final_fast_line


def calculate_sma(source: pd.Series, period: int) -> pd.Series:
    """
    Calculate Simple Moving Average.
    Exactly matches MQL5 SMA_Calculation function.
    
    Args:
        source: Source data series
        period: SMA period
        
    Returns:
        pd.Series: SMA values
    """
    if len(source) < period:
        return source
    
    return source.rolling(window=period, min_periods=1).mean()


def calculate_schr_wave2(df: pd.DataFrame, long1: int = 339, fast1: int = 10, trend1: int = 2,
                         tr1: str = 'Fast', long2: int = 22, fast2: int = 11, trend2: int = 4,
                         tr2: str = 'Fast', global_tr: str = 'Prime', sma_period: int = 22) -> pd.DataFrame:
    """
    Calculate SCHR Wave2 indicator values.
    Exactly matches MQL5 SCHR_Wave2.mq5 algorithm.
    
    Args:
        df: DataFrame with OHLCV data
        long1: First long period (default: 339)
        fast1: First fast period (default: 10)
        trend1: First trend period (default: 2)
        tr1: First trading rule (default: 'Fast')
        long2: Second long period (default: 22)
        fast2: Second fast period (default: 11)
        trend2: Second trend period (default: 4)
        tr2: Second trading rule (default: 'Fast')
        global_tr: Global trading rule (default: 'Prime')
        sma_period: SMA period (default: 22)
        
    Returns:
        DataFrame: DataFrame with calculated indicator values
    """
    if len(df) < max(long1, long2, fast1, fast2, trend1, trend2, sma_period):
        logger.print_warning("Not enough data for SCHR Wave2 calculation.")
        return df
    
    # Use Open prices as in MQL5
    open_prices = df['Open']
    
    # Calculate division factors
    div_long1 = 2.0 / max(long1, 1)
    div_fast1 = 2.0 / max(fast1, 1)
    div_direction1 = 2.0 / (max(trend1, 1) + 1)
    
    div_long2 = 2.0 / max(long2, 1)
    div_fast2 = 2.0 / max(fast2, 1)
    div_direction2 = 2.0 / (max(trend2, 1) + 1)
    
    # Calculate ECORE for both waves
    ecore1 = calculate_ecore(open_prices, div_long1)
    ecore2 = calculate_ecore(open_prices, div_long2)
    
    # Calculate Wave and FastLine for both waves
    wave1, fast_line1 = calculate_draw_lines(ecore1, div_fast1, div_direction1)
    wave2, fast_line2 = calculate_draw_lines(ecore2, div_fast2, div_direction2)
    
    # Apply trading rules to both waves
    tr1_enum = get_trading_rule_enum(tr1)
    tr2_enum = get_trading_rule_enum(tr2)
    
    color1 = apply_trading_rule(wave1, fast_line1, tr1_enum)
    color2 = apply_trading_rule(wave2, fast_line2, tr2_enum)
    
    # Apply global trading rule
    global_tr_enum = get_global_trading_rule_enum(global_tr)
    final_color, final_wave, final_fast_line = apply_global_trading_rule(
        color1, color2, wave1, fast_line1, global_tr_enum
    )
    
    # Calculate SMA
    ma_line = calculate_sma(final_fast_line, sma_period)
    
    # Calculate direction and signal
    direction = final_color.copy()
    signal = pd.Series(index=df.index, dtype=float)
    signal.iloc[0] = NOTRADE
    
    for i in range(1, len(direction)):
        if direction.iloc[i] != direction.iloc[i-1]:
            signal.iloc[i] = direction.iloc[i]
        else:
            signal.iloc[i] = NOTRADE
    
    # Create result DataFrame
    result_df = df.copy()
    result_df['schr_wave2_wave'] = final_wave
    result_df['schr_wave2_fast_line'] = final_fast_line
    result_df['schr_wave2_ma_line'] = ma_line
    result_df['schr_wave2_direction'] = direction
    result_df['schr_wave2_signal'] = signal
    
    # Add wave components for analysis
    result_df['schr_wave2_wave1'] = wave1
    result_df['schr_wave2_wave2'] = wave2
    result_df['schr_wave2_fast_line1'] = fast_line1
    result_df['schr_wave2_fast_line2'] = fast_line2
    result_df['schr_wave2_color1'] = color1
    result_df['schr_wave2_color2'] = color2
    
    # Add parameters for reference
    result_df['schr_wave2_long1'] = long1
    result_df['schr_wave2_fast1'] = fast1
    result_df['schr_wave2_trend1'] = trend1
    result_df['schr_wave2_tr1'] = tr1
    result_df['schr_wave2_long2'] = long2
    result_df['schr_wave2_fast2'] = fast2
    result_df['schr_wave2_trend2'] = trend2
    result_df['schr_wave2_tr2'] = tr2
    result_df['schr_wave2_global_tr'] = global_tr
    result_df['schr_wave2_sma_period'] = sma_period
    
    return result_df


class SCHRWave2Indicator(BaseIndicator):
    """SCHR Wave2 indicator implementation."""
    
    def __init__(self, long1: int = 339, fast1: int = 10, trend1: int = 2,
                 tr1: str = 'Fast', long2: int = 22, fast2: int = 11, trend2: int = 4,
                 tr2: str = 'Fast', global_tr: str = 'Prime', sma_period: int = 22,
                 price_type: Union[PriceType, str] = PriceType.OPEN):
        """
        Initialize SCHR Wave2 indicator.
        
        Args:
            long1: First long period
            fast1: First fast period
            trend1: First trend period
            tr1: First trading rule
            long2: Second long period
            fast2: Second fast period
            trend2: Second trend period
            tr2: Second trading rule
            global_tr: Global trading rule
            sma_period: SMA period
            price_type: Price type for calculations
        """
        super().__init__(price_type)
        self.long1 = long1
        self.fast1 = fast1
        self.trend1 = trend1
        self.tr1 = tr1
        self.long2 = long2
        self.fast2 = fast2
        self.trend2 = trend2
        self.tr2 = tr2
        self.global_tr = global_tr
        self.sma_period = sma_period
    
    def calculate(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Calculate SCHR Wave2 indicator values.
        
        Args:
            df: DataFrame with OHLCV data
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with calculated indicator values
        """
        if not self.validate_data(df, min_periods=max(self.long1, self.long2, self.fast1, self.fast2, self.trend1, self.trend2, self.sma_period)):
            return df
        
        return calculate_schr_wave2(
            df, self.long1, self.fast1, self.trend1, self.tr1,
            self.long2, self.fast2, self.trend2, self.tr2,
            self.global_tr, self.sma_period
        )
    
    def apply_rule(self, df: pd.DataFrame, point: float, **kwargs) -> pd.DataFrame:
        """
        Apply SCHR Wave2 trading rule logic.
        
        Args:
            df: DataFrame with OHLCV data
            point: Instrument point size
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with trading signals and levels
        """
        result_df = self.calculate(df, **kwargs)
        
        # Set output columns for compatibility with rule system
        result_df['PPrice1'] = result_df['schr_wave2_wave']
        result_df['PColor1'] = result_df['schr_wave2_signal']
        result_df['PPrice2'] = result_df['schr_wave2_fast_line']
        result_df['PColor2'] = result_df['schr_wave2_direction']
        result_df['Direction'] = result_df['schr_wave2_direction']
        result_df['Diff'] = result_df['schr_wave2_wave']
        
        return result_df


def apply_rule_schr_wave2(df: pd.DataFrame, point: float, long1: int = 339, fast1: int = 10, trend1: int = 2,
                          tr1: str = 'Fast', long2: int = 22, fast2: int = 11, trend2: int = 4,
                          tr2: str = 'Fast', global_tr: str = 'Prime', sma_period: int = 22,
                          price_type: Union[str, PriceType] = 'open', **kwargs) -> pd.DataFrame:
    """
    Apply SCHR Wave2 trading rule to DataFrame.
    
    Args:
        df: DataFrame with OHLCV data
        point: Instrument point size
        long1: First long period
        fast1: First fast period
        trend1: First trend period
        tr1: First trading rule
        long2: Second long period
        fast2: Second fast period
        trend2: Second trend period
        tr2: Second trading rule
        global_tr: Global trading rule
        sma_period: SMA period
        price_type: Price type for calculations
        **kwargs: Additional parameters
        
    Returns:
        DataFrame with trading signals and levels
    """
    # Convert price_type string or enum to PriceType enum
    if isinstance(price_type, str):
        price_type_enum = PriceType.OPEN if price_type.lower() == 'open' else PriceType.CLOSE
    else:
        price_type_enum = price_type
    
    indicator = SCHRWave2Indicator(
        long1, fast1, trend1, tr1, long2, fast2, trend2, tr2,
        global_tr, sma_period, price_type_enum
    )
    return indicator.apply_rule(df, point, **kwargs)
