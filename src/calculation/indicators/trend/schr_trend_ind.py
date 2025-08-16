# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/schr_trend_ind.py

"""
INDICATOR INFO:
Name: SCHR_TREND
Category: Trend
Description: SCHR Trend Helper - Advanced RSI-based trend prediction indicator
Usage: --rule SCHR_TREND or --rule SCHR_TREND:period,tr_mode,extreme_up,extreme_down
Parameters: period, tr_mode, extreme_up, extreme_down
Pros: + Good for Trend Detection, + Multiple trading rule modes, + Purchase Power analysis
Cons: - Complex parameter tuning, - Multiple RSI calculations for power modes
File: src/calculation/indicators/trend/schr_trend_ind.py

SCHR Trend Helper indicator calculation module.
Based on MQL5 SCHR_Trend.mq5 by Shcherbyna Rostyslav.
"""

import pandas as pd
import numpy as np
from typing import Optional, Union
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, DBL_BUY, DBL_SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


class TradingRuleMode:
    """Trading Rule modes for SCHR_Trend indicator."""
    TR_FirstClassic = 0
    TR_FirstTrend = 1
    TR_Trend = 2
    TR_Zone = 3
    TR_FirstZone = 4
    TR_FirstStrongZone = 5
    TR_PurchasePower = 6
    TR_PurchasePower_byCount = 7
    TR_PurchasePower_Extreme = 8
    TR_PurchasePower_Weak = 9


def calculate_rsi(df: pd.DataFrame, period: int, price_type: PriceType = PriceType.OPEN) -> pd.Series:
    """
    Calculate RSI indicator.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        period (int): RSI period
        price_type (PriceType): Price type for calculations
        
    Returns:
        pd.Series: RSI values
    """
    if len(df) < period + 1:
        logger.print_warning(f"Not enough data for RSI calculation. Need at least {period + 1} points.")
        return pd.Series(index=df.index, dtype=float)
    
    # Get price series based on price type
    if price_type == PriceType.OPEN:
        prices = df['Open']
    elif price_type == PriceType.CLOSE:
        prices = df['Close']
    else:
        prices = df['Open']  # Default to Open as in MQL5
    
    # Calculate price changes
    delta = prices.diff()
    
    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    # Calculate average gains and losses
    avg_gains = gains.rolling(window=period).mean()
    avg_losses = losses.rolling(window=period).mean()
    
    # Calculate RS and RSI
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_schr_trend(df: pd.DataFrame, period: int = 2, 
                        tr_mode: int = TradingRuleMode.TR_Zone,
                        extreme_up: int = 95, extreme_down: int = 5,
                        price_type: PriceType = PriceType.OPEN) -> tuple[pd.Series, pd.Series, pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Calculate SCHR Trend Helper indicator values.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        period (int): RSI period (default: 2)
        tr_mode (int): Trading rule mode (default: TR_Zone)
        extreme_up (int): Extreme up point (default: 95)
        extreme_down (int): Extreme down point (default: 5)
        price_type (PriceType): Price type for calculations
        
    Returns:
        tuple: (origin, trend, direction, signal, color, purchase_power)
        - origin: RSI origin values (like RSI)
        - trend: Trend line values
        - direction: Direction values (0=no_signal, 1=buy, 2=sell, 3=dbl_buy, 4=dbl_sell)
        - signal: Signal values (0=no_signal, 1=buy, 2=sell, 3=dbl_buy, 4=dbl_sell) - only changes
        - color: Color index for signals
        - purchase_power: Purchase Power values (only when enabled)
    """
    if len(df) < period + 1:
        logger.print_warning(f"Not enough data for SCHR Trend calculation. Need at least {period + 1} points.")
        empty_series = pd.Series(index=df.index, dtype=float)
        return empty_series, empty_series, empty_series, empty_series
    
    # Calculate main RSI
    rsi_values = calculate_rsi(df, period, price_type)
    
    # Initialize arrays
    n = len(df)
    origin = pd.Series(index=df.index, dtype=float)  # RSI origin values
    trend = pd.Series(index=df.index, dtype=float)   # Trend line values
    direction = pd.Series(NOTRADE, index=df.index)   # Direction values
    signal = pd.Series(NOTRADE, index=df.index)      # Signal values (only changes)
    color = pd.Series(NOTRADE, index=df.index)       # Color index
    purchase_power = pd.Series(0, index=df.index)    # Purchase Power values
    
    # Get price series based on price type
    if price_type == PriceType.OPEN:
        prices = df['Open']
    elif price_type == PriceType.CLOSE:
        prices = df['Close']
    else:
        prices = df['Open']
    
    # Calculate Purchase Power if needed
    power_rsis = []
    if tr_mode >= TradingRuleMode.TR_PurchasePower:
        for i in range(10):
            power_period = (i + 1) * period
            power_rsi = calculate_rsi(df, power_period, price_type)
            power_rsis.append(power_rsi)
    
    # Main calculation loop
    for i in range(n):
        if i == 0:
            # First bar - initialize values
            origin.iloc[i] = rsi_values.iloc[i]
            trend.iloc[i] = prices.iloc[i]
            direction.iloc[i] = NOTRADE
            signal.iloc[i] = NOTRADE
            color.iloc[i] = NOTRADE
            purchase_power.iloc[i] = 0
            continue
        
        # Set origin (RSI values)
        origin.iloc[i] = rsi_values.iloc[i]
        
        # Set trend line to open price
        trend.iloc[i] = prices.iloc[i]
        
        # Apply trading rule based on mode to get direction and color
        if tr_mode == TradingRuleMode.TR_FirstClassic:
            color.iloc[i], direction.iloc[i], _ = _first_classic_tr(
                rsi_values.iloc[i], extreme_up, extreme_down, direction.iloc[i-1])
        elif tr_mode == TradingRuleMode.TR_FirstTrend:
            color.iloc[i], direction.iloc[i], _ = _first_trend_tr(
                rsi_values.iloc[i], extreme_up, extreme_down, direction.iloc[i-1])
        elif tr_mode == TradingRuleMode.TR_Trend:
            color.iloc[i], direction.iloc[i], _ = _trend_tr(
                rsi_values.iloc[i], extreme_up, extreme_down, direction.iloc[i-1])
        elif tr_mode == TradingRuleMode.TR_Zone:
            color.iloc[i], direction.iloc[i], _ = _zone_tr(
                rsi_values.iloc[i], extreme_up, extreme_down, direction.iloc[i-1])
        elif tr_mode == TradingRuleMode.TR_FirstZone:
            color.iloc[i], direction.iloc[i], _ = _first_zone_tr(
                rsi_values.iloc[i], extreme_up, extreme_down, direction.iloc[i-1])
        elif tr_mode == TradingRuleMode.TR_FirstStrongZone:
            color.iloc[i], direction.iloc[i], _ = _first_strong_zone_tr(
                rsi_values.iloc[i], direction.iloc[i-1])
        elif tr_mode == TradingRuleMode.TR_PurchasePower:
            color.iloc[i], direction.iloc[i], _ = _purchase_power_tr(
                power_rsis, i, direction.iloc[i-1])
        elif tr_mode == TradingRuleMode.TR_PurchasePower_byCount:
            color.iloc[i], direction.iloc[i], _ = _purchase_power_by_count_tr(
                power_rsis, i, direction.iloc[i-1])
        elif tr_mode == TradingRuleMode.TR_PurchasePower_Extreme:
            color.iloc[i], direction.iloc[i], _ = _purchase_power_extreme_tr(
                power_rsis, i, direction.iloc[i-1])
        elif tr_mode == TradingRuleMode.TR_PurchasePower_Weak:
            color.iloc[i], direction.iloc[i], _ = _purchase_power_weak_tr(
                power_rsis, i, direction.iloc[i-1])
        else:
            # Default to Zone mode
            color.iloc[i], direction.iloc[i], _ = _zone_tr(
                rsi_values.iloc[i], extreme_up, extreme_down, direction.iloc[i-1])
        
        # Calculate signal based on direction change
        if i > 0:
            if direction.iloc[i] != direction.iloc[i-1] and direction.iloc[i] != NOTRADE:
                # Direction changed - signal shows the new direction
                signal.iloc[i] = direction.iloc[i]
            else:
                # Direction unchanged - no signal
                signal.iloc[i] = NOTRADE
        
        # Calculate Purchase Power if enabled
        if tr_mode >= TradingRuleMode.TR_PurchasePower and len(power_rsis) > 0:
            purchase_power.iloc[i] = _calculate_purchase_power(power_rsis, i)
    
    return origin, trend, direction, signal, color, purchase_power


def _first_classic_tr(rsi_value: float, extreme_up: int, extreme_down: int, prev_direction: float) -> tuple[float, float, float]:
    """First Classic TR: >95 Sell, <5 Buy."""
    if rsi_value > extreme_up:
        color = DBL_SELL
    elif rsi_value < extreme_down:
        color = DBL_BUY
    else:
        color = NOTRADE
    
    direction = color
    signal = DBL_BUY if direction != prev_direction and direction != NOTRADE else NOTRADE
    
    return color, direction, signal


def _first_trend_tr(rsi_value: float, extreme_up: int, extreme_down: int, prev_direction: float) -> tuple[float, float, float]:
    """First Trend TR: >95 Buy, <5 Sell."""
    if rsi_value > extreme_up:
        color = DBL_BUY
    elif rsi_value < extreme_down:
        color = DBL_SELL
    else:
        color = NOTRADE
    
    direction = color
    signal = DBL_BUY if direction != prev_direction and direction != NOTRADE else NOTRADE
    
    return color, direction, signal


def _trend_tr(rsi_value: float, extreme_up: int, extreme_down: int, prev_direction: float) -> tuple[float, float, float]:
    """Trend TR: Best Up 70| Down 30."""
    if rsi_value > extreme_up:
        color = DBL_BUY
    elif rsi_value < extreme_down:
        color = DBL_SELL
    else:
        # If no extreme then copy previous color
        color = prev_direction if prev_direction != NOTRADE else NOTRADE
    
    direction = color
    signal = DBL_BUY if direction != prev_direction and direction != NOTRADE else NOTRADE
    
    return color, direction, signal


def _zone_tr(rsi_value: float, extreme_up: int, extreme_down: int, prev_direction: float) -> tuple[float, float, float]:
    """Zone TR: >50 Buy, <50 Sell."""
    if rsi_value > 50:
        color = BUY
        # Check Extreme Point UP
        if rsi_value > extreme_up:
            color = DBL_BUY
    else:
        color = SELL
        # Check Extreme Point DOWN
        if rsi_value < extreme_down:
            color = DBL_SELL
    
    direction = color
    signal = DBL_BUY if direction != prev_direction and direction != NOTRADE else NOTRADE
    
    return color, direction, signal


def _first_zone_tr(rsi_value: float, extreme_up: int, extreme_down: int, prev_direction: float) -> tuple[float, float, float]:
    """First Zone TR: Include New Extreme Signals."""
    if rsi_value > 50:
        color = BUY
        # Check Extreme Point UP
        if rsi_value > extreme_up:
            color = DBL_BUY
    else:
        color = SELL
        # Check Extreme Point DOWN
        if rsi_value < extreme_down:
            color = DBL_SELL
    
    direction = color
    signal = DBL_BUY if direction != prev_direction and direction != NOTRADE else NOTRADE
    
    # Draw only First Signal
    final_color = signal if signal != NOTRADE else NOTRADE
    
    return final_color, direction, signal


def _first_strong_zone_tr(rsi_value: float, prev_direction: float) -> tuple[float, float, float]:
    """First Strong Zone TR: Without New Extreme Signals."""
    if rsi_value > 50:
        color = BUY
    else:
        color = SELL
    
    direction = color
    signal = DBL_BUY if direction != prev_direction and direction != NOTRADE else NOTRADE
    
    # Draw only First Signal
    final_color = signal if signal != NOTRADE else NOTRADE
    
    return final_color, direction, signal


def _purchase_power_tr(power_rsis: list, i: int, prev_direction: float) -> tuple[float, float, float]:
    """Purchase Power TR: 10 indicators."""
    if not power_rsis or i >= len(power_rsis[0]):
        return NOTRADE, NOTRADE, NOTRADE
    
    buy_count = 0
    sell_count = 0
    buy_power = 0.0
    sell_power = 0.0
    
    # Calculate power for each RSI
    for power_rsi in power_rsis:
        if i < len(power_rsi):
            if power_rsi.iloc[i] > 50:
                buy_power += power_rsi.iloc[i]
                buy_count += 1
            else:
                sell_power += power_rsi.iloc[i]
                sell_count += 1
    
    # Check Zero
    if buy_count == 0 and sell_count == 0:
        return NOTRADE, NOTRADE, NOTRADE
    
    # Draw Extreme
    if buy_count == 0:
        # Super SELL!
        color = DBL_SELL
    elif sell_count == 0:
        # Super BUY!
        color = DBL_BUY
    else:
        # Check Power
        buy_avg = 50 - (buy_power / buy_count)
        sell_avg = 50 - (sell_power / sell_count)
        
        if abs(buy_avg) > sell_avg:
            color = BUY
        else:
            color = SELL
    
    direction = color
    signal = DBL_BUY if direction != prev_direction and direction != NOTRADE else NOTRADE
    
    return color, direction, signal


def _purchase_power_by_count_tr(power_rsis: list, i: int, prev_direction: float) -> tuple[float, float, float]:
    """Purchase Power by Count TR: 10 indicators."""
    if not power_rsis or i >= len(power_rsis[0]):
        return NOTRADE, NOTRADE, NOTRADE
    
    buy_count = 0
    sell_count = 0
    buy_power = 0.0
    sell_power = 0.0
    
    # Calculate power for each RSI
    for power_rsi in power_rsis:
        if i < len(power_rsi):
            if power_rsi.iloc[i] > 50:
                buy_power += power_rsi.iloc[i]
                buy_count += 1
            else:
                sell_power += power_rsi.iloc[i]
                sell_count += 1
    
    # Check Zero
    if buy_count == 0 and sell_count == 0:
        return NOTRADE, NOTRADE, NOTRADE
    
    # Draw Extreme
    if buy_count == 0:
        # Super SELL!
        color = DBL_SELL
    elif sell_count == 0:
        # Super BUY!
        color = DBL_BUY
    else:
        # Check BUY Count
        if buy_count > sell_count:
            color = BUY
        else:
            color = SELL
    
    direction = color
    signal = DBL_BUY if direction != prev_direction and direction != NOTRADE else NOTRADE
    
    return color, direction, signal


def _purchase_power_extreme_tr(power_rsis: list, i: int, prev_direction: float) -> tuple[float, float, float]:
    """Purchase Power Extreme TR: 10 indicators Only Extreme."""
    if not power_rsis or i >= len(power_rsis[0]):
        return NOTRADE, NOTRADE, NOTRADE
    
    buy_count = 0
    sell_count = 0
    buy_power = 0.0
    sell_power = 0.0
    
    # Calculate power for each RSI
    for power_rsi in power_rsis:
        if i < len(power_rsi):
            if power_rsi.iloc[i] > 50:
                buy_power += power_rsi.iloc[i]
                buy_count += 1
            else:
                sell_power += power_rsi.iloc[i]
                sell_count += 1
    
    # Check Zero
    if buy_count == 0 and sell_count == 0:
        return NOTRADE, NOTRADE, NOTRADE
    
    # Draw Extreme
    if buy_count == 0:
        # Super SELL!
        color = DBL_SELL
    elif sell_count == 0:
        # Super BUY!
        color = DBL_BUY
    else:
        # NOT EXTREME (Who Bigger?)
        if abs(50 - buy_power) > (50 - sell_power):
            color = DBL_BUY
        else:
            color = DBL_SELL
    
    direction = color
    signal = DBL_BUY if direction != prev_direction and direction != NOTRADE else NOTRADE
    
    return color, direction, signal


def _purchase_power_weak_tr(power_rsis: list, i: int, prev_direction: float) -> tuple[float, float, float]:
    """Purchase Power Weak TR: 10 indicators."""
    if not power_rsis or i >= len(power_rsis[0]):
        return NOTRADE, NOTRADE, NOTRADE
    
    buy_count = 0
    sell_count = 0
    buy_power = 0.0
    sell_power = 0.0
    
    # Calculate power for each RSI
    for power_rsi in power_rsis:
        if i < len(power_rsi):
            if power_rsi.iloc[i] > 50:
                buy_power += power_rsi.iloc[i]
                buy_count += 1
            else:
                sell_power += power_rsi.iloc[i]
                sell_count += 1
    
    # Check Zero
    if buy_count == 0 and sell_count == 0:
        return NOTRADE, NOTRADE, NOTRADE
    
    # Draw Extreme
    if buy_count == 0:
        # Super SELL!
        color = SELL
    elif sell_count == 0:
        # Super BUY!
        color = BUY
    else:
        # Check Power
        buy_avg = 50 - (buy_power / buy_count)
        sell_avg = 50 - (sell_power / sell_count)
        
        if abs(buy_avg) > sell_avg:
            color = BUY
        else:
            color = SELL
    
    direction = color
    signal = DBL_BUY if direction != prev_direction and direction != NOTRADE else NOTRADE
    
    return color, direction, signal


class SCHRTrendIndicator(BaseIndicator):
    """SCHR Trend Helper indicator implementation."""
    
    def __init__(self, period: int = 2, 
                 tr_mode: Union[int, str] = TradingRuleMode.TR_Zone,
                 extreme_up: int = 95, extreme_down: int = 5,
                 price_type: Union[PriceType, str] = PriceType.OPEN):
        """
        Initialize SCHR Trend Helper indicator.
        
        Args:
            period: RSI period (default: 2)
            tr_mode: Trading rule mode (enum value or name)
            extreme_up: Extreme up point (default: 95)
            extreme_down: Extreme down point (default: 5)
            price_type: Price type for calculations
        """
        super().__init__(price_type)
        self.period = period
        self.tr_mode = self._parse_tr_mode(tr_mode)
        self.extreme_up = extreme_up
        self.extreme_down = extreme_down
    
    def _parse_tr_mode(self, tr_mode: Union[int, str]) -> int:
        """Parse trading rule mode from string or int."""
        if isinstance(tr_mode, str):
            tr_mode_map = {
                'firstclassic': TradingRuleMode.TR_FirstClassic,
                'firsttrend': TradingRuleMode.TR_FirstTrend,
                'trend': TradingRuleMode.TR_Trend,
                'zone': TradingRuleMode.TR_Zone,
                'firstzone': TradingRuleMode.TR_FirstZone,
                'firststrongzone': TradingRuleMode.TR_FirstStrongZone,
                'purchasepower': TradingRuleMode.TR_PurchasePower,
                'purchasepower_bycount': TradingRuleMode.TR_PurchasePower_byCount,
                'purchasepower_extreme': TradingRuleMode.TR_PurchasePower_Extreme,
                'purchasepower_weak': TradingRuleMode.TR_PurchasePower_Weak
            }
            return tr_mode_map.get(tr_mode.lower(), TradingRuleMode.TR_Zone)
        return tr_mode
    
    def calculate(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Calculate SCHR Trend Helper indicator values.
        
        Args:
            df: DataFrame with OHLCV data
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with calculated indicator values
        """
        if not self.validate_data(df, min_periods=self.period + 1):
            return df
        
        result_df = df.copy()
        
        # Calculate SCHR Trend values
        origin, trend, direction, signal, color, purchase_power = calculate_schr_trend(
            df, self.period, self.tr_mode, self.extreme_up, self.extreme_down, self.price_type)
        
        result_df['schr_trend_origin'] = origin
        result_df['schr_trend'] = trend
        result_df['schr_trend_direction'] = direction
        result_df['schr_trend_signal'] = signal
        result_df['schr_trend_color'] = color
        result_df['schr_trend_purchase_power'] = purchase_power
        
        return result_df
    
    def apply_rule(self, df: pd.DataFrame, point: float, **kwargs) -> pd.DataFrame:
        """
        Apply SCHR Trend Helper trading rule logic.
        
        Args:
            df: DataFrame with OHLCV data
            point: Instrument point size
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with trading signals and levels
        """
        result_df = self.calculate(df, **kwargs)
        
        # Set output columns for compatibility with rule system
        result_df['PPrice1'] = result_df['Open']
        result_df['PColor1'] = result_df['schr_trend_signal']
        result_df['PPrice2'] = result_df['schr_trend']
        result_df['PColor2'] = result_df['schr_trend_direction']
        result_df['Direction'] = result_df['schr_trend_direction']
        result_df['Diff'] = result_df['schr_trend']
        
        return result_df


def _calculate_purchase_power(power_rsis: list, index: int) -> float:
    """
    Calculate Purchase Power value based on multiple RSI periods.
    
    Args:
        power_rsis: List of RSI series for different periods
        index: Current index in the series
        
    Returns:
        float: Purchase Power value (0-100)
    """
    if not power_rsis or index >= len(power_rsis[0]):
        return 0.0
    
    # Calculate average RSI value across all periods
    total_rsi = 0.0
    valid_count = 0
    
    for rsi_series in power_rsis:
        if index < len(rsi_series) and not pd.isna(rsi_series.iloc[index]):
            total_rsi += rsi_series.iloc[index]
            valid_count += 1
    
    if valid_count == 0:
        return 0.0
    
    return total_rsi / valid_count


def apply_rule_schr_trend(df: pd.DataFrame, point: float, period: int = 2,
                          tr_mode: Union[int, str] = TradingRuleMode.TR_Zone,
                          extreme_up: int = 95, extreme_down: int = 5,
                          price_type: str = 'open', **kwargs) -> pd.DataFrame:
    """
    Apply SCHR Trend Helper trading rule to DataFrame.
    
    Args:
        df: DataFrame with OHLCV data
        point: Instrument point size
        period: RSI period (default: 2)
        tr_mode: Trading rule mode (default: TR_Zone)
        extreme_up: Extreme up point (default: 95)
        extreme_down: Extreme down point (default: 5)
        price_type: Price type for calculations
        **kwargs: Additional parameters
        
    Returns:
        DataFrame with trading signals and levels
    """
    # Convert price_type string to PriceType enum
    if isinstance(price_type, str):
        if price_type.lower() == 'open':
            price_type_enum = PriceType.OPEN
        elif price_type.lower() == 'close':
            price_type_enum = PriceType.CLOSE
        else:
            price_type_enum = PriceType.OPEN
    else:
        price_type_enum = price_type
    
    indicator = SCHRTrendIndicator(period, tr_mode, extreme_up, extreme_down, price_type_enum)
    return indicator.apply_rule(df, point, **kwargs)
