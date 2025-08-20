# -*- coding: utf-8 -*-
# src/plotting/dual_chart_plot.py

"""
Dual chart plotting functionality.
Creates a secondary chart below the main chart when user specifies --rule parameter
with indicator parameters (e.g., rsi:14,30,70,open).

This module provides the main interface for dual chart plotting across all modes:
- fastest: Plotly + Dask + Datashader
- fast: Bokeh
- mpl: Matplotlib
- sb: Seaborn
- term: Terminal

The main chart shows OHLC candlesticks with buy/sell signals and support/resistance lines.
The secondary chart shows the selected indicator with applied parameters.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple
import re

from src.common import logger
from src.calculation.indicators.oscillators.rsi_ind_calc import calculate_rsi, PriceType
from src.calculation.indicators.momentum.macd_ind import calculate_macd
from src.calculation.indicators.trend.ema_ind import calculate_ema
from src.calculation.indicators.volatility.bb_ind import calculate_bollinger_bands
from src.calculation.indicators.volatility.atr_ind import calculate_atr
from src.calculation.indicators.oscillators.cci_ind import calculate_cci
from src.calculation.indicators.volume.vwap_ind import calculate_vwap
from src.calculation.indicators.suportresist.pivot_ind import calculate_pivot_points
from src.calculation.indicators.predictive.hma_ind import calculate_hma
from src.calculation.indicators.predictive.tsforecast_ind import calculate_tsforecast
from src.calculation.indicators.probability.montecarlo_ind import calculate_montecarlo
from src.calculation.indicators.probability.kelly_ind import calculate_kelly
from src.calculation.indicators.suportresist.donchain_ind import calculate_donchain, calculate_donchain_signals
from src.calculation.indicators.suportresist.fiboretr_ind import calculate_fiboretr
from src.calculation.indicators.volume.obv_ind import calculate_obv
from src.calculation.indicators.volatility.stdev_ind import calculate_stdev
from src.calculation.indicators.trend.adx_ind import calculate_adx
from src.calculation.indicators.trend.sar_ind import calculate_sar
from src.calculation.indicators.sentiment.putcallratio_ind import calculate_putcallratio
from src.calculation.indicators.sentiment.cot_ind import calculate_cot
from src.calculation.indicators.sentiment.feargreed_ind import calculate_feargreed
from src.common.constants import BUY, SELL, NOTRADE
from src.cli.cli import parse_supertrend_parameters

# Import dual chart plotting functions
from .dual_chart_fastest import plot_dual_chart_fastest
from .dual_chart_fast import plot_dual_chart_fast
from .dual_chart_mpl import plot_dual_chart_mpl
from .dual_chart_seaborn import plot_dual_chart_seaborn
from .dual_chart_terminal import plot_dual_chart_terminal


def is_dual_chart_rule(rule: str) -> bool:
    """
    Check if the rule should trigger dual chart mode.
    
    Args:
        rule (str): Rule string (e.g., 'rsi:14,30,70,open')
        
    Returns:
        bool: True if rule should use dual chart mode
    """
    if not rule or ':' not in rule:
        return False
    
    # Extract indicator name
    indicator_name = rule.split(':', 1)[0].lower().strip()
    
    # Excluded indicators that should not use dual chart
    excluded_indicators = {
        'ohlcv', 'auto', 'pv', 'sr', 'phld', 'pressure_vector', 
        'support_resistants', 'predict_high_low_direction'
    }
    
    if indicator_name in excluded_indicators:
        return False
    
    # Check if indicator is supported
    supported_indicators = get_supported_indicators()
    
    if indicator_name not in supported_indicators:
        return False
    
    # Basic parameter validation for common indicators
    try:
        params_str = rule.split(':', 1)[1].strip()
        params = [p.strip() for p in params_str.split(',')]
        
        if indicator_name in ['rsi', 'rsi_mom', 'rsi_div']:
            if len(params) < 4:
                return False
            # Check if first 3 parameters are numeric
            int(params[0])  # period
            float(params[1])  # oversold
            float(params[2])  # overbought
            if params[3].lower() not in ['open', 'close']:
                return False
        elif indicator_name == 'macd':
            if len(params) < 4:
                return False
            # Check if first 3 parameters are numeric
            int(params[0])  # fast_period
            int(params[1])  # slow_period
            int(params[2])  # signal_period
            if params[3].lower() not in ['open', 'close']:
                return False
        elif indicator_name == 'ema':
            if len(params) < 2:
                return False
            int(params[0])  # period
            if params[1].lower() not in ['open', 'close']:
                return False
        elif indicator_name == 'bb':
            if len(params) < 3:
                return False
            int(params[0])  # period
            float(params[1])  # std_dev
            if params[2].lower() not in ['open', 'close']:
                return False
        elif indicator_name == 'wave':
            if len(params) < 11:
                return False
            # Check if first 10 parameters are numeric
            int(float(params[0]))  # long1
            int(float(params[1]))  # fast1
            int(float(params[2]))  # trend1
            if params[3].lower() not in ['fast', 'zone', 'strongtrend', 'weaktrend', 'fastzonereverse', 'bettertrend', 'betterfast']:
                return False
            int(float(params[4]))  # long2
            int(float(params[5]))  # fast2
            int(float(params[6]))  # trend2
            if params[7].lower() not in ['fast', 'zone', 'strongtrend', 'weaktrend', 'fastzonereverse', 'bettertrend', 'betterfast']:
                return False
            if params[8].lower() not in ['prime', 'reverse', 'primezone', 'reversezone', 'newzone', 'longzone', 'longzonereverse']:
                return False
            int(float(params[9]))  # sma_period
            if params[10].lower() not in ['open', 'close', 'high', 'low']:
                return False
    except (ValueError, IndexError):
        return False
    
    return True


def get_supported_indicators() -> set:
    """
    Get set of supported indicators for dual chart mode.
    
    Returns:
        set: Set of supported indicator names
    """
    return {
        'rsi', 'rsi_mom', 'rsi_div', 'macd', 'stoch', 'ema', 'sma', 'bb', 'atr',
        'cci', 'vwap', 'pivot', 'hma', 'tsf', 'monte', 'kelly', 'putcallratio', 'cot', 'feargreed', 'fg', 'donchain',
        'fibo', 'obv', 'stdev', 'adx', 'sar', 'supertrend', 'wave'
    }


def calculate_additional_indicator(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    """
    Calculate additional indicator based on the rule.
    
    Args:
        df (pd.DataFrame): OHLCV data
        rule (str): Rule string (e.g., 'rsi:14,30,70,open')
        
    Returns:
        pd.DataFrame: DataFrame with additional indicator columns
        
    Raises:
        ValueError: If indicator is not supported
    """
    if ':' not in rule:
        raise ValueError(f"Invalid rule format: {rule}")
    
    indicator_name = rule.split(':', 1)[0].lower().strip()
    # Aliases for MonteCarlo
    if indicator_name in ['monte', 'montecarlo', 'mc']:
        indicator_name = 'monte'
    params_str = rule.split(':', 1)[1].strip()
    
    # Parse parameters
    params = [p.strip() for p in params_str.split(',')]
    
    result_df = df.copy()
    
    try:
        if indicator_name == 'rsi':
            period = int(params[0]) if len(params) > 0 else 14
            oversold = float(params[1]) if len(params) > 1 else 30
            overbought = float(params[2]) if len(params) > 2 else 70
            price_type = PriceType.OPEN if len(params) > 3 and params[3].lower() == 'open' else PriceType.CLOSE
            
            price_series = df['Open'] if price_type == PriceType.OPEN else df['Close']
            rsi_values = calculate_rsi(price_series, period)
            
            # Check if RSI column already exists and remove it
            if 'RSI' in result_df.columns:
                result_df = result_df.drop(columns=['RSI'])
            if 'rsi' in result_df.columns:
                result_df = result_df.drop(columns=['rsi'])
            
            # Add RSI column with consistent naming
            result_df['rsi'] = rsi_values
            result_df['rsi_oversold'] = oversold
            result_df['rsi_overbought'] = overbought
            
        elif indicator_name == 'rsi_mom':
            period = int(params[0]) if len(params) > 0 else 14
            oversold = float(params[1]) if len(params) > 1 else 30
            overbought = float(params[2]) if len(params) > 2 else 70
            price_type = PriceType.OPEN if len(params) > 3 and params[3].lower() == 'open' else PriceType.CLOSE
            
            price_series = df['Open'] if price_type == PriceType.OPEN else df['Close']
            rsi_values = calculate_rsi(price_series, period)
            
            # Check if RSI columns already exist and remove them
            if 'RSI' in result_df.columns:
                result_df = result_df.drop(columns=['RSI'])
            if 'rsi' in result_df.columns:
                result_df = result_df.drop(columns=['rsi'])
            if 'RSI_Momentum' in result_df.columns:
                result_df = result_df.drop(columns=['RSI_Momentum'])
            if 'rsi_momentum' in result_df.columns:
                result_df = result_df.drop(columns=['rsi_momentum'])
            
            # Add RSI and RSI momentum columns
            result_df['rsi'] = rsi_values
            result_df['rsi_momentum'] = rsi_values.diff()
            result_df['rsi_oversold'] = oversold
            result_df['rsi_overbought'] = overbought
            
        elif indicator_name == 'rsi_div':
            period = int(params[0]) if len(params) > 0 else 14
            oversold = float(params[1]) if len(params) > 1 else 30
            overbought = float(params[2]) if len(params) > 2 else 70
            price_type = PriceType.OPEN if len(params) > 3 and params[3].lower() == 'open' else PriceType.CLOSE
            
            price_series = df['Open'] if price_type == PriceType.OPEN else df['Close']
            rsi_values = calculate_rsi(price_series, period)
            
            # Remove possible duplicates
            for col in ['RSI', 'rsi', 'rsi_divergence', 'RSI_Divergence']:
                if col in result_df.columns:
                    result_df = result_df.drop(columns=[col])
            
            # Add RSI
            result_df['rsi'] = rsi_values
            # Calculate divergence: difference between price change and RSI change
            price_diff = price_series.diff()
            rsi_diff = rsi_values.diff()
            result_df['rsi_divergence'] = price_diff - rsi_diff
            result_df['rsi_oversold'] = oversold
            result_df['rsi_overbought'] = overbought
            
        elif indicator_name == 'macd':
            fast_period = int(params[0]) if len(params) > 0 else 12
            slow_period = int(params[1]) if len(params) > 1 else 26
            signal_period = int(params[2]) if len(params) > 2 else 9
            price_type = 'open' if len(params) > 3 and params[3].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            # Calculate MACD (returns tuple: macd_line, signal_line, histogram)
            macd_line, signal_line, histogram = calculate_macd(price_series, fast_period, slow_period, signal_period)
            result_df['macd'] = macd_line
            result_df['macd_signal'] = signal_line
            result_df['macd_histogram'] = histogram
            
        elif indicator_name == 'ema':
            period = int(params[0]) if len(params) > 0 else 20
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            ema_values = calculate_ema(price_series, period)
            result_df['ema'] = ema_values
            
        elif indicator_name == 'sma':
            period = int(params[0]) if len(params) > 0 else 20
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            # Import SMA calculation function
            from src.calculation.indicators.trend.sma_ind import calculate_sma
            sma_values = calculate_sma(price_series, period)
            result_df['sma'] = sma_values
            
        elif indicator_name == 'bb':
            period = int(params[0]) if len(params) > 0 else 20
            std_dev = float(params[1]) if len(params) > 1 else 2.0
            price_type = 'open' if len(params) > 2 and params[2].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            # Calculate Bollinger Bands (returns tuple: upper, middle, lower)
            upper, middle, lower = calculate_bollinger_bands(price_series, period, std_dev)
            result_df['bb_upper'] = upper
            result_df['bb_middle'] = middle
            result_df['bb_lower'] = lower
            
        elif indicator_name == 'atr':
            period = int(params[0]) if len(params) > 0 else 14
            
            atr_values = calculate_atr(df, period)
            result_df['atr'] = atr_values
            
        elif indicator_name == 'cci':
            period = int(params[0]) if len(params) > 0 else 20
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            # Check if CCI column already exists and remove it
            if 'CCI' in result_df.columns:
                result_df = result_df.drop(columns=['CCI'])
            if 'cci' in result_df.columns:
                result_df = result_df.drop(columns=['cci'])
            
            cci_values = calculate_cci(price_series, period)
            result_df['cci'] = cci_values
            
        elif indicator_name == 'vwap':
            price_type = 'open' if len(params) > 0 and params[0].lower() == 'open' else 'close'
            
            vwap_values = calculate_vwap(df, price_type)
            result_df['vwap'] = vwap_values
            
        elif indicator_name == 'pivot':
            price_type = 'open' if len(params) > 0 and params[0].lower() == 'open' else 'close'
            
            # calculate_pivot_points returns tuple: (pivot_point, resistance_1, support_1)
            pivot_point, resistance_1, support_1 = calculate_pivot_points(df, price_type)
            result_df['pivot'] = pivot_point
            result_df['r1'] = resistance_1
            result_df['s1'] = support_1
            
        elif indicator_name == 'hma':
            period = int(params[0]) if len(params) > 0 else 20
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            hma_values = calculate_hma(price_series, period)
            result_df['hma'] = hma_values
            
        elif indicator_name == 'tsf':
            period = int(params[0]) if len(params) > 0 else 20
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            tsf_values = calculate_tsforecast(price_series, period)
            result_df['tsf'] = tsf_values
            
        elif indicator_name == 'monte':
            # Handle empty parameters gracefully
            simulations = 1000
            period = 252
            
            if len(params) > 0 and params[0].strip():
                try:
                    simulations = int(params[0])
                except ValueError:
                    pass  # Use default value
            
            if len(params) > 1 and params[1].strip():
                try:
                    period = int(params[1])
                except ValueError:
                    pass  # Use default value
            
            # Select price series (use Close for Monte Carlo)
            price_series = df['Close']
            
            # Calculate Monte Carlo components
            monte_values = calculate_montecarlo(price_series, simulations, period)
            result_df['montecarlo'] = monte_values
            
            # Calculate signal line (EMA of forecast)
            signal_line = monte_values.ewm(span=9, adjust=False).mean()
            result_df['montecarlo_signal'] = signal_line
            
            # Calculate histogram
            histogram = monte_values - signal_line
            result_df['montecarlo_histogram'] = histogram
            
            # Calculate confidence bands
            forecast_changes = monte_values.pct_change().rolling(window=20, min_periods=5).std()
            confidence_interval = 1.96 * forecast_changes * monte_values
            result_df['montecarlo_upper'] = monte_values + confidence_interval
            result_df['montecarlo_lower'] = monte_values - confidence_interval
            
        elif indicator_name == 'kelly':
            period = int(params[0]) if len(params) > 0 else 20
            
            # Select price series (use Close for Kelly)
            price_series = df['Close']
            
            kelly_values = calculate_kelly(price_series, period)
            result_df['kelly'] = kelly_values
            
            # Calculate signal line (EMA of Kelly values)
            signal_line = kelly_values.ewm(span=9, adjust=False).mean()
            result_df['kelly_signal'] = signal_line
            
            # Calculate histogram
            histogram = kelly_values - signal_line
            result_df['kelly_histogram'] = histogram
            
            # Add threshold levels
            result_df['kelly_threshold_10'] = 0.1  # 10% threshold
            result_df['kelly_threshold_25'] = 0.25  # 25% threshold (max Kelly)
            
        elif indicator_name == 'putcallratio':
            # Filter empty parameters
            params = [p.strip() for p in params if p.strip()]
            period = int(params[0]) if len(params) > 0 else 20
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            volume_series = df['Volume']
            
            # Calculate Put/Call Ratio sentiment
            putcall_values = calculate_putcallratio(price_series, volume_series, period)
            result_df['putcallratio'] = putcall_values
            
            # Calculate signal line (EMA of Put/Call Ratio)
            signal_line = putcall_values.ewm(span=9, adjust=False).mean()
            result_df['putcallratio_signal'] = signal_line
            
            # Calculate histogram
            histogram = putcall_values - signal_line
            result_df['putcallratio_histogram'] = histogram
            
            # Add threshold levels (sentiment scale 0-100, 50 is neutral)
            result_df['putcallratio_bullish'] = 60  # Bullish threshold
            result_df['putcallratio_bearish'] = 40  # Bearish threshold
            result_df['putcallratio_neutral'] = 50  # Neutral level
            
        elif indicator_name == 'cot':
            # Filter empty parameters
            params = [p.strip() for p in params if p.strip()]
            period = int(params[0]) if len(params) > 0 else 20
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            volume_series = df['Volume']
            
            # Calculate COT sentiment
            cot_values = calculate_cot(price_series, volume_series, period)
            result_df['cot'] = cot_values
            
            # Calculate signal line (EMA of COT)
            signal_line = cot_values.ewm(span=9, adjust=False).mean()
            result_df['cot_signal'] = signal_line
            
            # Calculate histogram
            histogram = cot_values - signal_line
            result_df['cot_histogram'] = histogram
            
            # Add threshold levels (sentiment scale 0-100, 50 is neutral)
            result_df['cot_bullish'] = 70  # Bullish threshold
            result_df['cot_bearish'] = 30  # Bearish threshold
            result_df['cot_neutral'] = 50  # Neutral level
            
        elif indicator_name in ['feargreed', 'fg']:
            # Filter empty parameters
            params = [p.strip() for p in params if p.strip()]
            period = int(params[0]) if len(params) > 0 else 14
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            # Calculate Fear & Greed Index
            feargreed_values = calculate_feargreed(price_series, period)
            result_df['feargreed'] = feargreed_values
            
            # Calculate signal line (EMA of Fear & Greed)
            signal_line = feargreed_values.ewm(span=9, adjust=False).mean()
            result_df['feargreed_signal'] = signal_line
            
            # Calculate histogram
            histogram = feargreed_values - signal_line
            result_df['feargreed_histogram'] = histogram
            
            # Add threshold levels (Fear & Greed scale 0-100, 50 is neutral)
            result_df['feargreed_fear'] = 25  # Fear threshold (buy signal)
            result_df['feargreed_greed'] = 75  # Greed threshold (sell signal)
            result_df['feargreed_neutral'] = 50  # Neutral level
            
        elif indicator_name == 'donchain':
            period = int(params[0]) if len(params) > 0 else 20
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            # Calculate Donchian Channels (returns tuple: upper, middle, lower)
            upper, middle, lower = calculate_donchain(df, period)
            result_df['donchain_upper'] = upper
            result_df['donchain_middle'] = middle
            result_df['donchain_lower'] = lower
            
            # Calculate Donchian Channel signals for buy/sell indicators
            donchain_signals = calculate_donchain_signals(price_series, upper, lower)
            result_df['Direction'] = donchain_signals
            
            # Add support and resistance levels for visualization
            result_df['PPrice1'] = lower  # Support level (lower band)
            result_df['PColor1'] = BUY
            result_df['PPrice2'] = upper  # Resistance level (upper band)
            result_df['PColor2'] = SELL
            result_df['Diff'] = price_series - middle  # Price deviation from middle band
            
        elif indicator_name == 'fibo':
            # Handle fibo parameters - they are float levels, not int period
            if len(params) > 0 and params[0].lower() == 'all':
                # Use all standard Fibonacci levels
                fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786]
            else:
                # Parse custom Fibonacci levels
                try:
                    fib_levels = [float(p.strip()) for p in params]
                except (ValueError, IndexError):
                    # Use default levels if parsing fails
                    fib_levels = [0.236, 0.382, 0.618]
            
            # Calculate Fibonacci Retracement with custom levels
            period = 20  # Default period for swing calculation
            fib_levels_dict = calculate_fiboretr(df, period, fib_levels)
            
            # Add all Fibonacci levels to result DataFrame
            for level_name, level_series in fib_levels_dict.items():
                result_df[f'fibo_{level_name[4:]}'] = level_series  # Remove 'fib_' prefix
            
        elif indicator_name == 'obv':
            obv_values = calculate_obv(df['Close'], df['Volume'])
            result_df['obv'] = obv_values
            
        elif indicator_name == 'stdev':
            period = int(params[0]) if len(params) > 0 else 20
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            stdev_values = calculate_stdev(price_series, period)
            result_df['stdev'] = stdev_values
            
        elif indicator_name == 'adx':
            period = int(params[0]) if len(params) > 0 else 14
            
            # Calculate ADX (returns tuple: adx, plus_di, minus_di)
            adx, plus_di, minus_di = calculate_adx(df, period)
            result_df['adx'] = adx
            result_df['di_plus'] = plus_di
            result_df['di_minus'] = minus_di
            
        elif indicator_name == 'sar':
            acceleration = float(params[0]) if len(params) > 0 else 0.02
            maximum = float(params[1]) if len(params) > 1 else 0.2
            
            sar_values = calculate_sar(df, acceleration, maximum)
            result_df['sar'] = sar_values
            
        elif indicator_name == 'stoch':
            k_period = int(params[0]) if len(params) > 0 else 14
            d_period = int(params[1]) if len(params) > 1 else 3
            price_type = PriceType.OPEN if len(params) > 2 and params[2].lower() == 'open' else PriceType.CLOSE
            
            # Remove possible duplicates
            for col in ['stoch_k', 'stoch_d', 'Stoch_K', 'Stoch_D']:
                if col in result_df.columns:
                    result_df = result_df.drop(columns=[col])
            
            # Calculate Stochastic Oscillator
            high_series = df['High']
            low_series = df['Low']
            close_series = df['Close']
            
            # %K = ((Close - Lowest Low) / (Highest High - Lowest Low)) * 100
            lowest_low = low_series.rolling(window=k_period).min()
            highest_high = high_series.rolling(window=k_period).max()
            stoch_k = ((close_series - lowest_low) / (highest_high - lowest_low)) * 100
            
            # %D = SMA of %K
            stoch_d = stoch_k.rolling(window=d_period).mean()
            
            result_df['stoch_k'] = stoch_k
            result_df['stoch_d'] = stoch_d
            result_df['stoch_overbought'] = 80
            result_df['stoch_oversold'] = 20
            
        elif indicator_name == 'stochoscillator':
            k_period = int(params[0]) if len(params) > 0 else 14
            d_period = int(params[1]) if len(params) > 1 else 3
            price_type = PriceType.OPEN if len(params) > 2 and params[2].lower() == 'open' else PriceType.CLOSE
            
            # Remove possible duplicates
            for col in ['stochosc_k', 'stochosc_d', 'StochOsc_K', 'StochOsc_D']:
                if col in result_df.columns:
                    result_df = result_df.drop(columns=[col])
            
            # Calculate Stochastic Oscillator
            high_series = df['High']
            low_series = df['Low']
            close_series = df['Close']
            
            # %K = ((Close - Lowest Low) / (Highest High - Lowest Low)) * 100
            lowest_low = low_series.rolling(window=k_period).min()
            highest_high = high_series.rolling(window=k_period).max()
            stochosc_k = ((close_series - lowest_low) / (highest_high - lowest_low)) * 100
            
            # %D = SMA of %K
            stochosc_d = stochosc_k.rolling(window=d_period).mean()
            
            result_df['stochosc_k'] = stochosc_k
            result_df['stochosc_d'] = stochosc_d
            result_df['stochosc_overbought'] = 80
            result_df['stochosc_oversold'] = 20
            
        elif indicator_name == 'supertrend':
            # Use centralized supertrend parameter parser
            try:
                _, st_params = parse_supertrend_parameters(','.join(params))
            except Exception as e:
                raise ValueError(f"Error parsing supertrend parameters: {e}")
            period = st_params['supertrend_period']
            multiplier = st_params['multiplier']
            price_type = st_params['price_type']
            # Remove possible duplicates
            for col in ['supertrend', 'Supertrend', 'SUPERTREND']:
                if col in result_df.columns:
                    result_df = result_df.drop(columns=[col])
            from src.calculation.indicators.trend.supertrend_ind import calculate_supertrend
            if price_type == 'open':
                price_series = df['Open']
            else:
                price_series = df['Close']
            supertrend_values, trend_direction = calculate_supertrend(df, period, multiplier)
            result_df['supertrend'] = supertrend_values
            result_df['supertrend_period'] = period
            result_df['supertrend_multiplier'] = multiplier
            result_df['supertrend_price_type'] = price_type
            
        elif indicator_name == 'wave':
            # Use centralized wave parameter parser
            try:
                from src.cli.cli import parse_wave_parameters
                _, wave_params = parse_wave_parameters(','.join(params))
            except Exception as e:
                raise ValueError(f"Error parsing wave parameters: {e}")
            
            # Remove possible duplicates
            for col in ['wave1', 'wave2', 'Wave1', 'Wave2', '_Plot_Wave', '_Plot_FastLine', 'fastline1', 'fastline2', 'MA_Line']:
                if col in result_df.columns:
                    result_df = result_df.drop(columns=[col])
            
            # Calculate Wave indicator using the existing calculation logic
            from src.calculation.rules import apply_rule_wave
            from src.calculation.indicators.trend.wave_ind import WaveParameters
            
            # Create WaveParameters object
            wave_params_obj = WaveParameters(
                long1=wave_params['long1'],
                fast1=wave_params['fast1'],
                trend1=wave_params['trend1'],
                tr1=wave_params['tr1'],
                long2=wave_params['long2'],
                fast2=wave_params['fast2'],
                trend2=wave_params['trend2'],
                tr2=wave_params['tr2'],
                global_tr=wave_params['global_tr'],
                sma_period=wave_params['sma_period']
            )
            
            # Convert price_type string to PriceType enum
            from src.calculation.indicators.base_indicator import PriceType
            price_type_enum = PriceType.OPEN if wave_params['price_type'] == 'open' else PriceType.CLOSE
            
            wave_result = apply_rule_wave(df, wave_params_obj, price_type_enum)
            
            # Add Wave columns to result DataFrame
            for col in wave_result.columns:
                if col not in result_df.columns:
                    result_df[col] = wave_result[col]
            
        else:
            raise ValueError(f"Unsupported indicator: {indicator_name}")
            
    except (ValueError, IndexError) as e:
        raise ValueError(f"Error calculating {indicator_name}: {e}")
    
    return result_df


def create_dual_chart_layout(mode: str, rule: str) -> Dict[str, Any]:
    """
    Create layout configuration for dual chart mode.
    
    Args:
        mode (str): Plotting mode (fastest, fast, mpl, sb, term)
        rule (str): Rule string
        
    Returns:
        Dict[str, Any]: Layout configuration
    """
    indicator_name = rule.split(':', 1)[0].lower().strip()
    
    # Map indicator names to display names
    indicator_display_names = {
        'rsi': 'RSI',
        'rsi_mom': 'RSI Momentum',
        'rsi_div': 'RSI Divergence',
        'macd': 'MACD',
        'ema': 'EMA',
        'sma': 'SMA',
        'bb': 'Bollinger Bands',
        'atr': 'ATR',
        'cci': 'CCI',
        'vwap': 'VWAP',
        'pivot': 'Pivot Points',
        'hma': 'HMA',
        'tsf': 'Time Series Forecast',
        'monte': 'Monte Carlo',
        'kelly': 'Kelly Criterion',
        'putcallratio': 'Put/Call Ratio',
        'cot': 'COT (Commitment of Traders)',
        'feargreed': 'Fear & Greed Index',
        'fg': 'Fear & Greed Index',
        'donchain': 'Donchian Channels',
        'fibo': 'Fibonacci Retracements',
        'obv': 'OBV',
        'stdev': 'Standard Deviation',
        'adx': 'ADX',
        'sar': 'SAR',
        'supertrend': 'SuperTrend',
        'stoch': 'Stochastic',
        'stochoscillator': 'Stochastic Oscillator',
        'wave': 'Wave'
    }
    
    display_name = indicator_display_names.get(indicator_name, indicator_name.upper())
    
    # Create title with parameters for all indicators except PV, PHLD, SR, AUTO, OHLCV
    excluded_indicators = {'pv', 'phld', 'sr', 'auto', 'ohlcv', 'pressure_vector', 'support_resistants', 'predict_high_low_direction'}
    
    if indicator_name not in excluded_indicators and ':' in rule:
        # Extract parameters from rule
        params_part = rule.split(':', 1)[1]
        # Create title with indicator name and parameters
        indicator_title = f"{display_name} with params: {params_part}"
    else:
        # For excluded indicators or rules without parameters, use just the display name
        indicator_title = display_name
    
    return {
        'mode': mode,
        'main_chart_height': 0.6,
        'indicator_chart_height': 0.4,
        'indicator_name': indicator_title,
        'show_volume': False,  # No volume on any chart as per requirements
        'indicator_rule': rule
    }


def plot_dual_chart_results(
    df: pd.DataFrame,
    rule: str,
    title: str = '',
    mode: str = 'fastest',
    output_path: Optional[str] = None,
    width: int = 1800,
    height: int = 1100,
    **kwargs
) -> Any:
    """
    Main function to create dual chart plots.
    
    Args:
        df (pd.DataFrame): OHLCV data
        rule (str): Rule string (e.g., 'rsi:14,30,70,open')
        title (str): Plot title
        mode (str): Plotting mode (fastest, fast, mpl, sb, term)
        output_path (str, optional): Output file path
        width (int): Plot width
        height (int): Plot height
        **kwargs: Additional arguments
        
    Returns:
        Any: Plot object (depends on mode)
        
    Raises:
        ValueError: If data is invalid or mode is unsupported
    """
    # Validate input data
    if df is None or df.empty:
        raise ValueError("DataFrame is empty")
    
    required_columns = ['Open', 'High', 'Low', 'Close']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Validate rule
    if not is_dual_chart_rule(rule):
        raise ValueError(f"Invalid rule for dual chart: {rule}")
    
    # Check if DataFrame already has calculated indicators
    indicator_name = rule.split(':', 1)[0].lower()
    has_indicators = False
    
    # Debug: print input DataFrame columns
    from src.common import logger
    logger.print_info(f"[dual_chart_plot] Input DataFrame columns: {list(df.columns)}")
    logger.print_info(f"[dual_chart_plot] Checking for indicator: {indicator_name}")
    
    # Check for various indicator columns based on indicator type
    if indicator_name == 'wave':
        wave_cols = ['wave1', 'wave2', 'Wave1', 'Wave2', '_Plot_Wave', '_Plot_FastLine', 'fastline1', 'fastline2', 'MA_Line']
        found_cols = [col for col in wave_cols if col in df.columns]
        has_indicators = len(found_cols) > 0
        logger.print_info(f"[dual_chart_plot] Found Wave columns: {found_cols}")
    elif indicator_name == 'rsi':
        has_indicators = 'rsi' in df.columns or 'RSI' in df.columns
    elif indicator_name == 'macd':
        has_indicators = any(col in df.columns for col in ['macd', 'MACD', 'macd_signal', 'MACD_Signal'])
    # Add more indicator checks as needed...
    
    logger.print_info(f"[dual_chart_plot] Has indicators: {has_indicators}")
    
    # Use existing DataFrame if indicators are already calculated, otherwise calculate them
    if has_indicators:
        df_with_indicator = df.copy()
        logger.print_info(f"[dual_chart_plot] Using existing DataFrame with {len(df_with_indicator.columns)} columns")
    else:
        logger.print_info(f"[dual_chart_plot] Calculating indicators anew...")
        df_with_indicator = calculate_additional_indicator(df, rule)
        logger.print_info(f"[dual_chart_plot] After calculation: {len(df_with_indicator.columns)} columns")
    
    # Create layout configuration
    layout = create_dual_chart_layout(mode, rule)
    
    # Call appropriate plotting function based on mode
    if mode == 'fastest':
        return plot_dual_chart_fastest(
            df_with_indicator, rule, title, output_path, width, height, layout, **kwargs
        )
    elif mode == 'fast':
        return plot_dual_chart_fast(
            df_with_indicator, rule, title, output_path, width, height, layout, **kwargs
        )
    elif mode in ['mpl', 'mplfinance']:
        return plot_dual_chart_mpl(
            df_with_indicator, rule, title, output_path, width, height, layout, **kwargs
        )
    elif mode in ['sb', 'seaborn']:
        return plot_dual_chart_seaborn(
            df_with_indicator, rule, title, output_path, width, height, layout, **kwargs
        )
    elif mode == 'term':
        return plot_dual_chart_terminal(
            df_with_indicator, rule, title, output_path, width, height, layout, **kwargs
        )
    else:
        raise ValueError(f"Unsupported plotting mode: {mode}")


def get_indicator_parameters(rule: str) -> Tuple[str, Dict[str, Any]]:
    """
    Parse indicator parameters from rule string.
    
    Args:
        rule (str): Rule string (e.g., 'rsi:14,30,70,open')
        
    Returns:
        Tuple[str, Dict[str, Any]]: (indicator_name, parameters_dict)
    """
    if ':' not in rule:
        return rule.lower(), {}
    
    indicator_name = rule.split(':', 1)[0].lower().strip()
    # Aliases for MonteCarlo
    if indicator_name in ['monte', 'montecarlo', 'mc']:
        indicator_name = 'monte'
    params_str = rule.split(':', 1)[1].strip()
    
    params = [p.strip() for p in params_str.split(',')]
    
    # Convert parameters to appropriate types
    parameters = {}
    for i, param in enumerate(params):
        try:
            # Try to convert to float first, then int
            if '.' in param:
                parameters[f'param_{i}'] = float(param)
            else:
                parameters[f'param_{i}'] = int(param)
        except ValueError:
            # If conversion fails, keep as string
            parameters[f'param_{i}'] = param
    
    return indicator_name, parameters


def validate_indicator_rule(rule: str) -> bool:
    """
    Validate indicator rule format.
    
    Args:
        rule (str): Rule string to validate
        
    Returns:
        bool: True if rule is valid
    """
    if not rule or ':' not in rule:
        return False
    
    indicator_name = rule.split(':', 1)[0].lower().strip()
    params_str = rule.split(':', 1)[1].strip()
    
    # Check if indicator is supported
    if indicator_name not in get_supported_indicators():
        return False
    
    # Basic parameter validation
    params = [p.strip() for p in params_str.split(',')]
    
    # Validate based on indicator type
    if indicator_name == 'rsi':
        if len(params) != 4:
            return False
        try:
            int(params[0])  # period
            float(params[1])  # oversold
            float(params[2])  # overbought
            if params[3].lower() not in ['open', 'close']:
                return False
        except (ValueError, IndexError):
            return False
    
    elif indicator_name == 'macd':
        if len(params) != 4:
            return False
        try:
            int(params[0])  # fast_period
            int(params[1])  # slow_period
            int(params[2])  # signal_period
            if params[3].lower() not in ['open', 'close']:
                return False
        except (ValueError, IndexError):
            return False
    
    elif indicator_name == 'ema':
        if len(params) != 2:
            return False
        try:
            int(params[0])  # period
            if params[1].lower() not in ['open', 'close']:
                return False
        except (ValueError, IndexError):
            return False
    
    # Add more validation for other indicators as needed
    
    return True 