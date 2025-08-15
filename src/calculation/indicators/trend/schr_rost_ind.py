# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/schr_rost_ind.py

"""
INDICATOR INFO:
Name: SCHR_ROST
Category: Trend
Description: SCHR Rost - Advanced ADX-based trend prediction indicator
Usage: --rule SCHR_ROST or --rule SCHR_ROST:Future,true
Parameters: speed_period, faster_reverse, price_type
Pros: + Good for Trend Detection, + Fast reverse signals, + Multiple speed modes
Cons: - Tiny noises (fast reverse signals), - Sometimes false trend signals, - Fast signals on low volatility
File: src/calculation/indicators/trend/schr_rost_ind.py

SCHR Rost indicator calculation module.
Based on MQL5 SCHR_ROST.mq5 by Shcherbyna Rostyslav.
"""

import pandas as pd
import numpy as np
from typing import Optional, Union
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


class SpeedEnum:
    """Speed enumeration for SCHR_ROST indicator."""
    SNAIL = 0
    TURTLE = 1
    FROG = 2
    MOUSE = 3
    CAT = 4
    RABBIT = 5
    GEPARD = 6
    SLOWEST = 7
    SLOW = 8
    NORMAL = 9
    FAST = 10
    FUTURE = 11


# Speed constants from MQL5
SPEED_VALUES = {
    SpeedEnum.SNAIL: 1000,
    SpeedEnum.TURTLE: 500,
    SpeedEnum.FROG: 200,
    SpeedEnum.MOUSE: 100,
    SpeedEnum.CAT: 50,
    SpeedEnum.RABBIT: 30,
    SpeedEnum.GEPARD: 10,
    SpeedEnum.SLOWEST: 5,
    SpeedEnum.SLOW: 2,
    SpeedEnum.NORMAL: 1.01,
    SpeedEnum.FAST: 0.683,
    SpeedEnum.FUTURE: 0.501
}

SPEED_NAMES = {
    SpeedEnum.SNAIL: "Snail",
    SpeedEnum.TURTLE: "Turtle", 
    SpeedEnum.FROG: "Frog",
    SpeedEnum.MOUSE: "Mouse",
    SpeedEnum.CAT: "Cat",
    SpeedEnum.RABBIT: "Rabbit",
    SpeedEnum.GEPARD: "Gepard",
    SpeedEnum.SLOWEST: "Slowest",
    SpeedEnum.SLOW: "Slow",
    SpeedEnum.NORMAL: "Normal",
    SpeedEnum.FAST: "Fast",
    SpeedEnum.FUTURE: "Future"
}


def get_speed_period(speed_enum: Union[int, str]) -> float:
    """
    Get speed period value from speed enumeration or name.
    
    Args:
        speed_enum: Speed enumeration value or name
        
    Returns:
        float: Speed period value
    """
    if isinstance(speed_enum, str):
        # Convert name to enum
        speed_name = speed_enum.lower()
        for enum_val, name in SPEED_NAMES.items():
            if name.lower() == speed_name:
                return SPEED_VALUES[enum_val]
        # Default to NORMAL if not found
        return SPEED_VALUES[SpeedEnum.NORMAL]
    else:
        return SPEED_VALUES.get(speed_enum, SPEED_VALUES[SpeedEnum.NORMAL])


def calculate_schr_rost(df: pd.DataFrame, speed_period: float = 1.01) -> pd.Series:
    """
    Calculate SCHR Rost indicator values.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        speed_period (float): Speed period for calculation (default: 1.01 for NORMAL)
    
    Returns:
        pd.Series: SCHR Rost indicator values
    """
    if len(df) < 2:
        logger.print_warning("Not enough data for SCHR Rost calculation. Need at least 2 points.")
        return pd.Series(index=df.index, dtype=float)
    
    # Initialize arrays for calculations
    n = len(df)
    main_array = np.zeros((n, 7))  # 7 columns as in MQL5
    
    # Column indices (matching MQL5 defines)
    ADXVMA_WPDM = 1  # +DM smoothed
    ADXVMA_WMDM = 2  # -DM smoothed  
    ADXVMA_WPDI = 3  # +DI smoothed
    ADXVMA_WMDI = 4  # -DI smoothed
    ADXVMA_WOUT = 5  # DX smoothed
    ADXVMA_WVAL = 6  # Final value
    
    # Use Open prices as in MQL5
    prices = df['Open'].values
    
    # Initialize first value
    main_array[0, ADXVMA_WVAL] = prices[0]
    
    # Main calculation loop
    for i in range(1, n):
        main_array[i, 0] = prices[i]  # Current price
        
        # Calculate price difference
        diff = main_array[i, 0] - main_array[i-1, 0]
        
        # Calculate +DM and -DM
        tpdm = max(diff, 0)  # +DM
        tmdm = max(-diff, 0)  # -DM
        
        # Smooth +DM and -DM
        if i == 1:
            main_array[i, ADXVMA_WPDM] = tpdm
            main_array[i, ADXVMA_WMDM] = tmdm
        else:
            main_array[i, ADXVMA_WPDM] = ((speed_period - 1.0) * main_array[i-1, ADXVMA_WPDM] + tpdm) / speed_period
            main_array[i, ADXVMA_WMDM] = ((speed_period - 1.0) * main_array[i-1, ADXVMA_WMDM] + tmdm) / speed_period
        
        # Calculate True Range
        true_range = main_array[i, ADXVMA_WPDM] + main_array[i, ADXVMA_WMDM]
        
        # Calculate +DI and -DI
        tpdi = 0
        tmdi = 0
        if true_range > 0:
            tpdi = main_array[i, ADXVMA_WPDM] / true_range
            tmdi = main_array[i, ADXVMA_WMDM] / true_range
        
        # Smooth +DI and -DI
        if i == 1:
            main_array[i, ADXVMA_WPDI] = tpdi
            main_array[i, ADXVMA_WMDI] = tmdi
        else:
            main_array[i, ADXVMA_WPDI] = ((speed_period - 1.0) * main_array[i-1, ADXVMA_WPDI] + tpdi) / speed_period
            main_array[i, ADXVMA_WMDI] = ((speed_period - 1.0) * main_array[i-1, ADXVMA_WMDI] + tmdi) / speed_period
        
        # Calculate DX
        tout = 0
        if (main_array[i, ADXVMA_WPDI] + main_array[i, ADXVMA_WMDI]) > 0:
            tout = abs(main_array[i, ADXVMA_WPDI] - main_array[i, ADXVMA_WMDI]) / (main_array[i, ADXVMA_WPDI] + main_array[i, ADXVMA_WMDI])
        
        # Smooth DX
        if i == 1:
            main_array[i, ADXVMA_WOUT] = tout
        else:
            main_array[i, ADXVMA_WOUT] = ((speed_period - 1.0) * main_array[i-1, ADXVMA_WOUT] + tout) / speed_period
        
        # Calculate high and low of DX over period
        thi = max(main_array[i, ADXVMA_WOUT], main_array[i-1, ADXVMA_WOUT])
        tlo = min(main_array[i, ADXVMA_WOUT], main_array[i-1, ADXVMA_WOUT])
        
        # Look back over the period
        lookback = min(int(speed_period), i)
        for j in range(2, lookback + 1):
            if i - j >= 0:
                thi = max(main_array[i-j, ADXVMA_WOUT], thi)
                tlo = min(main_array[i-j, ADXVMA_WOUT], tlo)
        
        # Calculate VI (Volatility Index)
        vi = 0
        if (thi - tlo) > 0:
            vi = (main_array[i, ADXVMA_WOUT] - tlo) / (thi - tlo)
        
        # Calculate final value
        if i == 1:
            main_array[i, ADXVMA_WVAL] = main_array[i, 0]
        else:
            main_array[i, ADXVMA_WVAL] = ((speed_period - vi) * main_array[i-1, ADXVMA_WVAL] + vi * main_array[i, 0]) / speed_period
    
    return pd.Series(main_array[:, ADXVMA_WVAL], index=df.index)


def calculate_schr_rost_signals(rost_values: pd.Series, faster_reverse: bool = False) -> tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculate trading signals based on SCHR Rost values.
    Exactly matches MQL5 logic for Direction and Signal calculation.
    
    Args:
        rost_values (pd.Series): SCHR Rost indicator values
        faster_reverse (bool): Enable faster reverse signals
        
    Returns:
        tuple: (prediction, direction, signal)
        - prediction: 0=No trend, 1=Up, 2=Down
        - direction: 0=No Trade, 1=Buy (Up), 2=Sell (Down)
        - signal: 0=No Signal, 1=Buy (first occurrence), 2=Sell (first occurrence)
    """
    n = len(rost_values)
    prediction = pd.Series(0, index=rost_values.index)
    direction = pd.Series(0, index=rost_values.index)  # 0=NOTRADE, 1=BUY, 2=SELL
    signal = pd.Series(0, index=rost_values.index)     # 0=No Signal, 1=Buy, 2=Sell
    
    for i in range(n):
        # Calculate prediction - exactly as in MQL5
        if i > 0:
            if rost_values.iloc[i] > rost_values.iloc[i-1]:
                prediction.iloc[i] = 1  # Up trend
            elif rost_values.iloc[i] < rost_values.iloc[i-1]:
                prediction.iloc[i] = 2  # Down trend
            else:
                prediction.iloc[i] = prediction.iloc[i-1]  # Keep previous trend
        else:
            prediction.iloc[i] = 0  # First bar
        
        # Faster reverse logic - exactly as in MQL5
        if i > 0 and faster_reverse and (rost_values.iloc[i] == rost_values.iloc[i-1]):
            if prediction.iloc[i] == 1:
                prediction.iloc[i] = 2
            elif prediction.iloc[i] == 2:
                prediction.iloc[i] = 1
        
        # Set direction - exactly as in MQL5
        if prediction.iloc[i] == 0:
            direction.iloc[i] = 0  # NOTRADE
        elif prediction.iloc[i] == 1:
            direction.iloc[i] = 1  # BUY
        elif prediction.iloc[i] == 2:
            direction.iloc[i] = 2  # SELL
        
        # Generate signals - exactly as in MQL5 (only first occurrences)
        if i > 0:
            if direction.iloc[i] != direction.iloc[i-1]:
                signal.iloc[i] = direction.iloc[i]  # Signal on trend change
            else:
                signal.iloc[i] = 0  # No signal when trend continues
        else:
            signal.iloc[i] = 0  # First bar
    
    return prediction, direction, signal


class SCHRRostIndicator(BaseIndicator):
    """SCHR Rost indicator implementation."""
    
    def __init__(self, speed_period: Union[int, str] = SpeedEnum.FUTURE, 
                 faster_reverse: bool = False,
                 price_type: Union[PriceType, str] = PriceType.OPEN):
        """
        Initialize SCHR Rost indicator.
        
        Args:
            speed_period: Speed period (enum value or name)
            faster_reverse: Enable faster reverse signals
            price_type: Price type for calculations
        """
        super().__init__(price_type)
        self.speed_period = get_speed_period(speed_period)
        self.faster_reverse = faster_reverse
    
    def calculate(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Calculate SCHR Rost indicator values.
        
        Args:
            df: DataFrame with OHLCV data
            **kwargs: Additional parameters
            
        Returns:
            DataFrame with calculated indicator values
        """
        if not self.validate_data(df, min_periods=2):
            return df
        
        result_df = df.copy()
        
        # Calculate SCHR Rost values
        rost_values = calculate_schr_rost(df, self.speed_period)
        result_df['schr_rost'] = rost_values
        
        # Calculate signals
        prediction, direction, signal = calculate_schr_rost_signals(rost_values, self.faster_reverse)
        result_df['schr_rost_prediction'] = prediction
        result_df['schr_rost_direction'] = direction
        result_df['schr_rost_signal'] = signal
        
        return result_df
    
    def apply_rule(self, df: pd.DataFrame, point: float, **kwargs) -> pd.DataFrame:
        """
        Apply SCHR Rost trading rule logic.
        
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
        result_df['PColor1'] = result_df['schr_rost_signal']
        result_df['PPrice2'] = result_df['schr_rost']
        result_df['PColor2'] = result_df['schr_rost_direction']
        result_df['Direction'] = result_df['schr_rost_direction']
        result_df['Diff'] = result_df['schr_rost']
        
        return result_df


def apply_rule_schr_rost(df: pd.DataFrame, point: float, speed_period: Union[int, str] = SpeedEnum.FUTURE,
                        faster_reverse: bool = False, price_type: str = 'open', **kwargs) -> pd.DataFrame:
    """
    Apply SCHR Rost trading rule to DataFrame.
    
    Args:
        df: DataFrame with OHLCV data
        point: Instrument point size
        speed_period: Speed period (enum value or name)
        faster_reverse: Enable faster reverse signals
        price_type: Price type for calculations
        **kwargs: Additional parameters
        
    Returns:
        DataFrame with trading signals and levels
    """
    indicator = SCHRRostIndicator(speed_period, faster_reverse, price_type)
    return indicator.apply_rule(df, point, **kwargs)
