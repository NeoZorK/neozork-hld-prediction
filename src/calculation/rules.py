# -*- coding: utf-8 -*-
# src/rules.py

"""
Functions implementing the specific logic for each TradingRule.
Each function updates the DataFrame with rule-specific outputs
(PPrice1, PColor1, PPrice2, PColor2, Direction, Diff).
"""

import pandas as pd
import numpy as np
from ..common import logger
from ..common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from typing import Any

# Import RSI calculation functions from new structure
from .indicators.oscillators.rsi_ind_calc import apply_rule_rsi, apply_rule_rsi_momentum, apply_rule_rsi_divergence, PriceType

# Import new indicators with price_type support
from .indicators.oscillators.cci_ind import apply_rule_cci
from .indicators.oscillators.stoch_ind import apply_rule_stochastic
from .indicators.trend.ema_ind import apply_rule_ema
from .indicators.volatility.bb_ind import apply_rule_bollinger_bands
from .indicators.volatility.atr_ind import apply_rule_atr
from .indicators.volume.vwap_ind import apply_rule_vwap
from .indicators.suportresist.pivot_ind import apply_rule_pivot

# Import all new indicators
# Momentum indicators
from .indicators.momentum.macd_ind import apply_rule_macd
from .indicators.momentum.stochoscillator_ind import apply_rule_stochoscillator

# Predictive indicators
from .indicators.predictive.hma_ind import apply_rule_hma
from .indicators.predictive.tsforecast_ind import apply_rule_tsforecast

# Probability indicators
from .indicators.probability.montecarlo_ind import apply_rule_montecarlo
from .indicators.probability.kelly_ind import apply_rule_kelly

# Sentiment indicators
from .indicators.sentiment.feargreed_ind import apply_rule_feargreed
from .indicators.sentiment.cot_ind import apply_rule_cot
from .indicators.sentiment.putcallratio_ind import apply_rule_putcallratio

# Support/Resistance indicators
from .indicators.suportresist.donchain_ind import apply_rule_donchain
from .indicators.suportresist.fiboretr_ind import apply_rule_fiboretr

# Volume indicators
from .indicators.volume.obv_ind import apply_rule_obv

# Volatility indicators
from .indicators.volatility.stdev_ind import apply_rule_stdev

# Trend indicators
from .indicators.trend.adx_ind import apply_rule_adx
from .indicators.trend.sar_ind import apply_rule_sar
from .indicators.trend.supertrend_ind import apply_rule_supertrend

# Helper to safely get series or default
def _get_series(df, col_name, default_val=0):
    if col_name in df.columns:
        return df[col_name].fillna(default_val)
    return pd.Series(default_val, index=df.index)

# Predict High/Low Direction
def apply_rule_predict_hld(df: pd.DataFrame, point: float):
    """
    Combines Support/Resistants levels with Pressure Vector direction.
    Calculates PPrice1/2 based on Open +/- HL/2.
    Calculates Direction based on PV sign.
    """
    open_curr = _get_series(df, 'Open')
    hl_val = _get_series(df, 'HL') # HL in points
    pv_val = _get_series(df, 'PV') # Original PV

    # --- Calculate PPrice1/PPrice2 (from Support_Resistants) ---
    hl_term = hl_val / 2.0 * point # HL in price units
    df['PPrice1'] = open_curr - hl_term
    df['PPrice2'] = open_curr + hl_term
    # Assign colors like Support_Resistants
    df['PColor1'] = BUY
    df['PColor2'] = SELL

    # --- Calculate Direction (from Pressure_Vector) ---
    df['Direction'] = np.where(pv_val > 0, BUY, np.where(pv_val < 0, SELL, NOTRADE))

    # --- Set other outputs ---
    df['Diff'] = EMPTY_VALUE # Not calculated for this rule

    return df

def apply_rule_pv_highlow(df: pd.DataFrame, point: float):
    """Applies PV_HighLow rule logic."""
    open_curr = _get_series(df, 'Open')
    hl_val = _get_series(df, 'HL')
    pv_val = _get_series(df, 'PV')
    pv_e = 0.5 * np.log(np.pi) # approx 0.57236

    pv_term = np.power(pv_e, 3) * pv_val * point
    hl_term = hl_val * pv_e * point

    df['PPrice1'] = open_curr - (hl_term + pv_term)
    df['PColor1'] = BUY
    df['PPrice2'] = open_curr + (hl_term - pv_term)
    df['PColor2'] = SELL
    df['Direction'] = NOTRADE
    df['Diff'] = EMPTY_VALUE
    return df

def apply_rule_support_resistants(df: pd.DataFrame, point: float):
    """Applies Support_Resistants rule logic."""
    open_curr = _get_series(df, 'Open')
    hl_val = _get_series(df, 'HL')
    hl_term = hl_val / 2.0 * point

    df['PPrice1'] = open_curr - hl_term
    df['PColor1'] = BUY
    df['PPrice2'] = open_curr + hl_term
    df['PColor2'] = SELL
    df['Direction'] = NOTRADE
    df['Diff'] = EMPTY_VALUE
    return df

def apply_rule_pressure_vector(df: pd.DataFrame, point: float):
    """Applies Pressure_Vector rule logic."""
    open_curr = _get_series(df, 'Open')
    pv_val = _get_series(df, 'PV')

    df['PPrice1'] = open_curr
    df['PPrice2'] = open_curr
    df['PColor1'] = np.where(pv_val > 0, BUY, np.where(pv_val < 0, SELL, NOTRADE))
    df['PColor2'] = EMPTY_VALUE
    df['Direction'] = df['PColor1']
    df['Diff'] = EMPTY_VALUE
    return df

def apply_rule_auto(df: pd.DataFrame, point: float):
    """
    AUTO rule - returns the data as-is with all available indicator columns.
    This rule is designed for displaying all non-standard OHLCV fields in terminal.
    """
    # For AUTO rule, we don't modify the data, just ensure the required output columns exist
    # Set default values for expected output columns but don't calculate specific indicators
    df['PPrice1'] = df['Open']  # Default to Open price
    df['PColor1'] = NOTRADE     # No trading signal
    df['PPrice2'] = df['Open']  # Default to Open price  
    df['PColor2'] = NOTRADE     # No trading signal
    df['Direction'] = NOTRADE   # No direction signal

    # Ensure Diff column exists
    if 'Diff' not in df.columns:
        df['Diff'] = pd.Series(dtype=float)
    #df['Diff'] = EMPTY_VALUE    # No difference calculation
    return df

# --- Rule Dispatcher ---
# Maps TradingRule enum to the corresponding function
RULE_DISPATCHER = {
    TradingRule.PV_HighLow: apply_rule_pv_highlow,
    TradingRule.Support_Resistants: apply_rule_support_resistants,
    TradingRule.Pressure_Vector: apply_rule_pressure_vector,
    TradingRule.Predict_High_Low_Direction: apply_rule_predict_hld,
    TradingRule.AUTO: apply_rule_auto,  # Add AUTO rule support
    TradingRule.RSI: apply_rule_rsi,
    TradingRule.RSI_Momentum: apply_rule_rsi_momentum,
    TradingRule.RSI_Divergence: apply_rule_rsi_divergence,
    # Add new indicators with price_type support
    TradingRule.CCI: apply_rule_cci,
    TradingRule.Stochastic: apply_rule_stochastic,
    TradingRule.EMA: apply_rule_ema,
    TradingRule.Bollinger_Bands: apply_rule_bollinger_bands,
    TradingRule.ATR: apply_rule_atr,
    TradingRule.VWAP: apply_rule_vwap,
    TradingRule.Pivot_Points: apply_rule_pivot,
    # Add all new indicators
    # Momentum indicators
    TradingRule.MACD: apply_rule_macd,
    TradingRule.StochOscillator: apply_rule_stochoscillator,
    # Predictive indicators
    TradingRule.HMA: apply_rule_hma,
    TradingRule.TSForecast: apply_rule_tsforecast,
    # Probability indicators
    TradingRule.MonteCarlo: apply_rule_montecarlo,
    TradingRule.Kelly: apply_rule_kelly,
    # Sentiment indicators
    TradingRule.FearGreed: apply_rule_feargreed,
    TradingRule.COT: apply_rule_cot,
    TradingRule.PutCallRatio: apply_rule_putcallratio,
    # Support/Resistance indicators
    TradingRule.Donchain: apply_rule_donchain,
    TradingRule.FiboRetr: apply_rule_fiboretr,
    # Volume indicators
    TradingRule.OBV: apply_rule_obv,
    # Volatility indicators
    TradingRule.StDev: apply_rule_stdev,
    # Trend indicators
    TradingRule.ADX: apply_rule_adx,
    TradingRule.SAR: apply_rule_sar,
    TradingRule.SuperTrend: apply_rule_supertrend,
}

def apply_trading_rule(df: pd.DataFrame, rule: TradingRule | Any, point: float, price_type: str = 'close', **kwargs) -> pd.DataFrame:
    """
    Applies the selected trading rule logic to the DataFrame.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        rule (TradingRule): Trading rule to apply
        point (float): Instrument point size
        price_type (str): Price type for calculations ('open' or 'close')
        **kwargs: Additional parameters for specific indicators
    """
    selected_rule: TradingRule | None = None
    rule_func = None
    is_valid_rule = False

    if isinstance(rule, TradingRule):
        selected_rule = rule
        if rule in RULE_DISPATCHER:
            is_valid_rule = True
            rule_func = RULE_DISPATCHER[rule]
        else:
            pass # is_valid_rule will remain False

    if not is_valid_rule:
        logger.print_warning(
            f"TradingRule {repr(rule)} not recognized or supported. "
            f"Applying default ({TradingRule.Predict_High_Low_Direction.name})."
        )
        selected_rule = TradingRule.Predict_High_Low_Direction
        rule_func = RULE_DISPATCHER[selected_rule]

    # Convert price_type string to PriceType enum for rules that support it
    price_type_enum = PriceType.OPEN if price_type.lower() == 'open' else PriceType.CLOSE

    # Call the rule function with the DataFrame and point
    if selected_rule in [TradingRule.PV_HighLow, TradingRule.Support_Resistants, TradingRule.Pressure_Vector, TradingRule.Predict_High_Low_Direction, TradingRule.AUTO]:
        return rule_func(df, point=point)
    elif selected_rule in [TradingRule.RSI, TradingRule.RSI_Momentum, TradingRule.RSI_Divergence]:
        # Extract RSI-specific parameters
        rsi_period = kwargs.get('rsi_period', 14)
        oversold = kwargs.get('oversold', 30)
        overbought = kwargs.get('overbought', 70)
        return rule_func(df, point=point, rsi_period=rsi_period, overbought=overbought, oversold=oversold, price_type=price_type_enum)
    elif selected_rule == TradingRule.CCI:
        # Extract CCI-specific parameters
        cci_period = kwargs.get('cci_period', 20)
        return rule_func(df, point=point, cci_period=cci_period, price_type=price_type_enum)
    elif selected_rule == TradingRule.Stochastic:
        # Extract Stochastic-specific parameters
        stoch_k_period = kwargs.get('stoch_k_period', 14)
        stoch_d_period = kwargs.get('stoch_d_period', 3)
        return rule_func(df, point=point, stoch_k_period=stoch_k_period, stoch_d_period=stoch_d_period, price_type=price_type_enum)
    elif selected_rule == TradingRule.EMA:
        # Extract EMA-specific parameters
        ema_period = kwargs.get('ema_period', 20)
        return rule_func(df, point=point, ema_period=ema_period, price_type=price_type_enum)
    elif selected_rule == TradingRule.Bollinger_Bands:
        # Extract Bollinger Bands-specific parameters
        bb_period = kwargs.get('bb_period', 20)
        bb_std_dev = kwargs.get('bb_std_dev', 2.0)
        return rule_func(df, point=point, bb_period=bb_period, bb_std_dev=bb_std_dev, price_type=price_type_enum)
    elif selected_rule == TradingRule.ATR:
        # Extract ATR-specific parameters
        atr_period = kwargs.get('atr_period', 14)
        return rule_func(df, point=point, atr_period=atr_period)
    elif selected_rule == TradingRule.VWAP:
        return rule_func(df, point=point, price_type=price_type_enum)
    elif selected_rule == TradingRule.Pivot_Points:
        return rule_func(df, point=point, price_type=price_type_enum)
    elif selected_rule == TradingRule.MACD:
        # Extract MACD-specific parameters
        macd_fast = kwargs.get('macd_fast', 12)
        macd_slow = kwargs.get('macd_slow', 26)
        macd_signal = kwargs.get('macd_signal', 9)
        return rule_func(df, point=point, macd_fast=macd_fast, macd_slow=macd_slow, macd_signal=macd_signal, price_type=price_type_enum)
    elif selected_rule == TradingRule.StochOscillator:
        return rule_func(df, point=point, price_type=price_type_enum)
    elif selected_rule == TradingRule.HMA:
        # Extract HMA-specific parameters
        hma_period = kwargs.get('hma_period', 20)
        return rule_func(df, point=point, hma_period=hma_period, price_type=price_type_enum)
    elif selected_rule == TradingRule.TSForecast:
        # Extract TSF-specific parameters
        tsforecast_period = kwargs.get('tsforecast_period', 14)
        return rule_func(df, point=point, tsforecast_period=tsforecast_period, price_type=price_type_enum)
    elif selected_rule == TradingRule.MonteCarlo:
        # Extract Monte Carlo-specific parameters
        simulations = kwargs.get('simulations', 1000)
        period = kwargs.get('period', 252)
        return rule_func(df, point=point, simulations=simulations, period=period)
    elif selected_rule == TradingRule.Kelly:
        # Extract Kelly-specific parameters
        kelly_period = kwargs.get('kelly_period', 20)
        return rule_func(df, point=point, kelly_period=kelly_period)
    elif selected_rule == TradingRule.FearGreed:
        feargreed_period = kwargs.get('feargreed_period', 14)
        price_type = kwargs.get('price_type', price_type_enum)
        return rule_func(df, point=point, feargreed_period=feargreed_period, price_type=price_type)
    elif selected_rule == TradingRule.COT:
        return rule_func(df, point=point)
    elif selected_rule == TradingRule.PutCallRatio:
        return rule_func(df, point=point)
    elif selected_rule == TradingRule.Donchain:
        # Extract Donchian-specific parameters
        donchain_period = kwargs.get('donchain_period', 20)
        return rule_func(df, point=point, donchain_period=donchain_period)
    elif selected_rule == TradingRule.FiboRetr:
        # Extract Fibonacci-specific parameters
        fib_levels = kwargs.get('fib_levels', [0.236, 0.382, 0.5, 0.618, 0.786])
        return rule_func(df, point=point, fib_levels=fib_levels)
    elif selected_rule == TradingRule.OBV:
        return rule_func(df, point=point)
    elif selected_rule == TradingRule.StDev:
        # Extract StDev-specific parameters
        stdev_period = kwargs.get('stdev_period', 20)
        return rule_func(df, point=point, stdev_period=stdev_period, price_type=price_type_enum)
    elif selected_rule == TradingRule.ADX:
        # Extract ADX-specific parameters
        adx_period = kwargs.get('adx_period', 14)
        return rule_func(df, point=point, adx_period=adx_period)
    elif selected_rule == TradingRule.SAR:
        # Extract SAR-specific parameters
        sar_acceleration = kwargs.get('sar_acceleration', 0.02)
        sar_maximum = kwargs.get('sar_maximum', 0.2)
        return rule_func(df, point=point, sar_acceleration=sar_acceleration, sar_maximum=sar_maximum)
    elif selected_rule == TradingRule.SuperTrend:
        # Extract SuperTrend-specific parameters
        supertrend_period = kwargs.get('supertrend_period', 10)
        multiplier = kwargs.get('multiplier', 3.0)
        return rule_func(df, point=point, supertrend_period=supertrend_period, multiplier=multiplier, price_type=price_type_enum)
    else:
        # Default case for any other rules
        return rule_func(df, point=point, price_type=price_type_enum)
