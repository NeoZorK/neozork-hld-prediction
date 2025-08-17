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

from ..common import logger
from ..calculation.indicators.oscillators.rsi_ind_calc import calculate_rsi, PriceType
from ..calculation.indicators.momentum.macd_ind import calculate_macd
from ..calculation.indicators.trend.ema_ind import calculate_ema
from ..calculation.indicators.volatility.bb_ind import calculate_bollinger_bands
from ..calculation.indicators.volatility.atr_ind import calculate_atr
from ..calculation.indicators.oscillators.cci_ind import calculate_cci
from ..calculation.indicators.volume.vwap_ind import calculate_vwap
from ..calculation.indicators.suportresist.pivot_ind import calculate_pivot_points
from ..calculation.indicators.predictive.hma_ind import calculate_hma
from ..calculation.indicators.predictive.tsforecast_ind import calculate_tsforecast
from ..calculation.indicators.probability.montecarlo_ind import calculate_montecarlo
from ..calculation.indicators.probability.kelly_ind import calculate_kelly
from ..calculation.indicators.suportresist.donchain_ind import calculate_donchain, calculate_donchain_signals
from ..calculation.indicators.suportresist.fiboretr_ind import calculate_fiboretr
from ..calculation.indicators.volume.obv_ind import calculate_obv
from ..calculation.indicators.volatility.stdev_ind import calculate_stdev
from ..calculation.indicators.trend.adx_ind import calculate_adx
from ..calculation.indicators.trend.sar_ind import calculate_sar
from ..calculation.indicators.trend.schr_rost_ind import calculate_schr_rost
from ..calculation.indicators.sentiment.putcallratio_ind import calculate_putcallratio
from ..calculation.indicators.sentiment.cot_ind import calculate_cot
from ..calculation.indicators.sentiment.feargreed_ind import calculate_feargreed
from ..common.constants import BUY, SELL, NOTRADE
from ..cli.cli import parse_supertrend_parameters

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
    if not rule:
        return False
    
    # Special case for SCHR_DIR (no parameters but should use dual chart)
    if rule.lower().strip() == 'schr_dir':
        return True
    
    # Check for parameterized indicators (containing ':')
    if ':' not in rule:
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
        'rsi', 'rsi_mom', 'rsi_div', 'macd', 'stoch', 'ema', 'bb', 'atr',
        'cci', 'vwap', 'pivot', 'hma', 'tsf', 'monte', 'kelly', 'putcallratio', 'cot', 'feargreed', 'fg', 'donchain',
        'fibo', 'obv', 'stdev', 'adx', 'sar', 'supertrend', 'schr_rost', 'schr_trend', 'schr_wave2'
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
    # Special case for SCHR_DIR (no parameters)
    if rule.lower().strip() == 'schr_dir':
        # SCHR_DIR is already calculated in the main DataFrame
        # Just return the DataFrame as is
        return df
    
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
    
    # Initialize price_type variable to avoid scope issues
    price_type = None
    
    try:
        if indicator_name == 'rsi':
            period = int(params[0]) if len(params) > 0 else 14
            oversold = float(params[1]) if len(params) > 1 else 30
            overbought = float(params[2]) if len(params) > 2 else 70
            price_type = 'open' if len(params) > 3 and params[3].lower() == 'open' else 'close'
            
            price_series = df['Open'] if price_type == 'open' else df['Close']
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
            price_type = 'open' if len(params) > 3 and params[3].lower() == 'open' else 'close'
            
            price_series = df['Open'] if price_type == 'open' else df['Close']
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
            price_type = 'open' if len(params) > 3 and params[3].lower() == 'open' else 'close'
            
            price_series = df['Open'] if price_type == 'open' else df['Close']
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
            result_df['ema_period'] = period
            result_df['ema_price_type'] = price_type
            
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
            result_df['bb_period'] = period
            result_df['bb_std_dev'] = std_dev
            result_df['bb_price_type'] = price_type
            
        elif indicator_name == 'atr':
            period = int(params[0]) if len(params) > 0 else 14
            
            atr_values = calculate_atr(df, period)
            result_df['atr'] = atr_values
            result_df['atr_period'] = period
            
        elif indicator_name == 'cci':
            period = int(params[0]) if len(params) > 0 else 20
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            cci_values = calculate_cci(df, period, price_series)
            result_df['cci'] = cci_values
            result_df['cci_period'] = period
            result_df['cci_price_type'] = price_type
            
        elif indicator_name == 'vwap':
            price_type = 'open' if len(params) > 0 and params[0].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            vwap_values = calculate_vwap(df, price_series)
            result_df['vwap'] = vwap_values
            result_df['vwap_price_type'] = price_type
            
        elif indicator_name == 'pivot':
            price_type = 'open' if len(params) > 0 and params[0].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            # Calculate Pivot Points (returns tuple: pp, r1, s1)
            pp, r1, s1 = calculate_pivot_points(df, price_series)
            result_df['pivot_pp'] = pp
            result_df['pivot_r1'] = r1
            result_df['pivot_s1'] = s1
            result_df['pivot_price_type'] = price_type
            
        elif indicator_name == 'hma':
            period = int(params[0]) if len(params) > 0 else 20
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            hma_values = calculate_hma(price_series, period)
            result_df['hma'] = hma_values
            result_df['hma_period'] = period
            result_df['hma_price_type'] = price_type
            
        elif indicator_name == 'tsforecast':
            period = int(params[0]) if len(params) > 0 else 20
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            forecast_values = calculate_tsforecast(price_series, period)
            result_df['tsforecast'] = forecast_values
            result_df['tsforecast_period'] = period
            result_df['tsforecast_price_type'] = price_type
            
        elif indicator_name == 'monte':
            period = int(params[0]) if len(params) > 0 else 20
            simulations = int(params[1]) if len(params) > 1 else 1000
            price_type = 'open' if len(params) > 2 and params[2].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            monte_values = calculate_montecarlo(price_series, period, simulations)
            result_df['monte'] = monte_values
            result_df['monte_period'] = period
            result_df['monte_simulations'] = simulations
            result_df['monte_price_type'] = price_type
            
        elif indicator_name == 'kelly':
            period = int(params[0]) if len(params) > 0 else 20
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            kelly_values = calculate_kelly(price_series, period)
            result_df['kelly'] = kelly_values
            result_df['kelly_period'] = period
            result_df['kelly_price_type'] = price_type
            
        elif indicator_name == 'donchain':
            period = int(params[0]) if len(params) > 0 else 20
            price_type = 'open' if len(params) > 1 and params[1].lower() == 'open' else 'close'
            
            # Select price series based on price_type
            price_series = df['Open'] if price_type == 'open' else df['Close']
            
            # Calculate Donchian Channel
            donchain_values = calculate_donchain(df, period)
            result_df['donchain_upper'] = donchain_values['upper']
            result_df['donchain_lower'] = donchain_values['lower']
            result_df['donchain_middle'] = donchain_values['middle']
            result_df['donchain_period'] = period
            result_df['donchain_price_type'] = price_type
            
        elif indicator_name == 'fibo':
            # Parse custom Fibonacci levels if provided
            if len(params) == 0:
                # Use default Fibonacci levels
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
            price_type = 'open' if len(params) > 2 and params[2].lower() == 'open' else 'close'
            
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
            price_type = 'open' if len(params) > 2 and params[2].lower() == 'open' else 'close'
            
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
            from ..calculation.indicators.trend.supertrend_ind import calculate_supertrend
            if price_type == 'open':
                price_series = df['Open']
            else:
                price_series = df['Close']
            supertrend_values, trend_direction = calculate_supertrend(df, period, multiplier)
            result_df['supertrend'] = supertrend_values
            result_df['supertrend_period'] = period
            result_df['supertrend_multiplier'] = multiplier
            result_df['supertrend_price_type'] = price_type
            
        elif indicator_name == 'schr_rost':
            # Filter empty parameters
            params = [p.strip() for p in params if p.strip()]
            speed_period = params[0] if len(params) > 0 else 'Future'
            faster_reverse = params[1].lower() in ['true', '1'] if len(params) > 1 else False
            
            # Calculate SCHR_ROST indicator using the indicator class
            from ..calculation.indicators.trend.schr_rost_ind import SCHRRostIndicator, SpeedEnum
            from ..calculation.indicators.oscillators.rsi_ind_calc import PriceType
            
            # Convert speed_period string to SpeedEnum
            speed_enum = SpeedEnum.FUTURE  # Default
            speed_name = speed_period.upper()
            if speed_name == 'SNAIL':
                speed_enum = SpeedEnum.SNAIL
            elif speed_name == 'TURTLE':
                speed_enum = SpeedEnum.TURTLE
            elif speed_name == 'FROG':
                speed_enum = SpeedEnum.FROG
            elif speed_name == 'MOUSE':
                speed_enum = SpeedEnum.MOUSE
            elif speed_name == 'CAT':
                speed_enum = SpeedEnum.CAT
            elif speed_name == 'RABBIT':
                speed_enum = SpeedEnum.RABBIT
            elif speed_name == 'GEPARD':
                speed_enum = SpeedEnum.GEPARD
            elif speed_name == 'SLOWEST':
                speed_enum = SpeedEnum.SLOWEST
            elif speed_name == 'SLOW':
                speed_enum = SpeedEnum.SLOW
            elif speed_name == 'NORMAL':
                speed_enum = SpeedEnum.NORMAL
            elif speed_name == 'FAST':
                speed_enum = SpeedEnum.FAST
            elif speed_name == 'FUTURE':
                speed_enum = SpeedEnum.FUTURE
            
            # Create indicator instance
            indicator = SCHRRostIndicator(speed_enum, faster_reverse, 'open')
            schr_rost_result = indicator.calculate(df)
            
            # Handle the result - it might be a DataFrame or Series
            if isinstance(schr_rost_result, pd.DataFrame):
                # Extract all SCHR_ROST columns from the result
                schr_rost_cols = [col for col in schr_rost_result.columns if 'schr_rost' in col.lower()]
                for col in schr_rost_cols:
                    result_df[col] = schr_rost_result[col]
                
                # If main schr_rost column not found, use first numeric column
                if 'schr_rost' not in schr_rost_result.columns:
                    numeric_cols = schr_rost_result.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        result_df['schr_rost'] = schr_rost_result[numeric_cols[0]]
                    else:
                        result_df['schr_rost'] = pd.Series(index=df.index, dtype=float)
            else:
                # If it's a Series, use it directly
                result_df['schr_rost'] = schr_rost_result
            
            # Add speed period and faster reverse info
            result_df['schr_rost_speed'] = speed_period
            result_df['schr_rost_faster_reverse'] = faster_reverse
            
        elif indicator_name == 'schr_trend':
            # Filter empty parameters
            params = [p.strip() for p in params if p.strip()]
            period = int(params[0]) if len(params) > 0 else 2
            tr_mode = params[1].lower() if len(params) > 1 else 'zone'
            extreme_up = int(params[2]) if len(params) > 2 else 95
            extreme_down = int(params[3]) if len(params) > 3 else 5
            price_type = params[4].lower() if len(params) > 4 else 'open'  # Default to open
            
            # Calculate SCHR_TREND indicator using the indicator class
            from ..calculation.indicators.trend.schr_trend_ind import SCHRTrendIndicator
            
            # Create indicator instance and call calculate first to get indicator columns
            indicator = SCHRTrendIndicator(period, tr_mode, extreme_up, extreme_down, price_type)
            schr_trend_calc = indicator.calculate(df)
            
            # Extract all SCHR_TREND columns from the calculation result
            schr_trend_cols = [col for col in schr_trend_calc.columns if 'schr_trend' in col.lower()]
            logger.print_info(f"[DEBUG] SCHR_TREND calculation columns: {list(schr_trend_calc.columns)}")
            logger.print_info(f"[DEBUG] SCHR_TREND columns to add: {schr_trend_cols}")
            for col in schr_trend_cols:
                result_df[col] = schr_trend_calc[col]
                logger.print_info(f"[DEBUG] Added column {col} to result_df")
            
            # Ensure we have all required SCHR_TREND columns
            required_cols = ['schr_trend_origin', 'schr_trend', 'schr_trend_direction', 'schr_trend_signal', 'schr_trend_color', 'schr_trend_purchase_power']
            for col in required_cols:
                if col not in result_df.columns:
                    logger.print_warning(f"Missing required SCHR_TREND column: {col}")
                    # Create empty column if missing
                    result_df[col] = 0.0
            
            # Now call apply_rule to get the rule columns
            schr_trend_rule = indicator.apply_rule(df, point=0.00001)  # Use default point size
            
            # Also add the standard rule columns for compatibility
            result_df['PPrice1'] = schr_trend_rule['PPrice1']
            result_df['PColor1'] = schr_trend_rule['PColor1']
            result_df['PPrice2'] = schr_trend_rule['PPrice2']
            result_df['PColor2'] = schr_trend_rule['PColor2']
            result_df['Direction'] = schr_trend_rule['Direction']
            result_df['Diff'] = schr_trend_rule['Diff']
            
            logger.print_info(f"[DEBUG] Final result_df columns: {list(result_df.columns)}")
            
            # Add the standard rule columns for compatibility
            result_df['PPrice1'] = schr_trend_rule['PPrice1']
            result_df['PColor1'] = schr_trend_rule['PColor1']
            result_df['PPrice2'] = schr_trend_rule['PPrice2']
            result_df['PColor2'] = schr_trend_rule['PColor2']
            result_df['Direction'] = schr_trend_rule['Direction']
            result_df['Diff'] = schr_trend_rule['Diff']
            
            # Add parameters info
            result_df['schr_trend_period'] = period
            result_df['schr_trend_tr_mode'] = tr_mode
            result_df['schr_trend_extreme_up'] = extreme_up
            result_df['schr_trend_extreme_down'] = extreme_down
            result_df['schr_trend_price_type'] = price_type
            
        elif indicator_name == 'schr_wave2':
            # Filter empty parameters
            params = [p.strip() for p in params if p.strip()]
            long1 = int(params[0]) if len(params) > 0 else 339
            fast1 = int(params[1]) if len(params) > 1 else 10
            trend1 = int(params[2]) if len(params) > 2 else 2
            tr1 = params[3] if len(params) > 3 else 'Fast'
            long2 = int(params[4]) if len(params) > 4 else 22
            fast2 = int(params[5]) if len(params) > 5 else 11
            trend2 = int(params[6]) if len(params) > 6 else 4
            tr2 = params[7] if len(params) > 7 else 'Fast'
            global_tr = params[8] if len(params) > 8 else 'Prime'
            sma_period = int(params[9]) if len(params) > 9 else 22
            
            # Calculate SCHR_Wave2 indicator using the indicator class
            from ..calculation.indicators.trend.schr_wave2_ind import SCHRWave2Indicator
            
            # Create indicator instance and call calculate first to get indicator columns
            indicator = SCHRWave2Indicator(long1, fast1, trend1, tr1, long2, fast2, trend2, tr2, global_tr, sma_period, 'open')
            schr_wave2_calc = indicator.calculate(df)
            
            # Extract all SCHR_Wave2 columns from the calculation result
            schr_wave2_cols = [col for col in schr_wave2_calc.columns if 'schr_wave2' in col.lower()]
            logger.print_info(f"[DEBUG] SCHR_Wave2 calculation columns: {list(schr_wave2_calc.columns)}")
            logger.print_info(f"[DEBUG] SCHR_Wave2 columns to add: {schr_wave2_cols}")
            for col in schr_wave2_cols:
                result_df[col] = schr_wave2_calc[col]
                logger.print_info(f"[DEBUG] Added column {col} to result_df")
            
            # Ensure we have all required SCHR_Wave2 columns
            required_cols = ['schr_wave2_wave', 'schr_wave2_fast_line', 'schr_wave2_ma_line', 'schr_wave2_direction', 'schr_wave2_signal']
            for col in required_cols:
                if col not in result_df.columns:
                    logger.print_warning(f"Missing required SCHR_Wave2 column: {col}")
                    # Create empty column if missing
                    result_df[col] = 0.0
            
            # Now call apply_rule to get the rule columns
            schr_wave2_rule = indicator.apply_rule(df, point=0.00001)  # Use default point size
            
            # Also add the standard rule columns for compatibility
            result_df['PPrice1'] = schr_wave2_rule['PPrice1']
            result_df['PColor1'] = schr_wave2_rule['PColor1']
            result_df['PPrice2'] = schr_wave2_rule['PPrice2']
            result_df['PColor2'] = schr_wave2_rule['PColor2']
            result_df['Direction'] = schr_wave2_rule['Direction']
            result_df['Diff'] = schr_wave2_rule['Diff']
            
            logger.print_info(f"[DEBUG] Final result_df columns: {list(result_df.columns)}")
            
            # Add the standard rule columns for compatibility
            result_df['PPrice1'] = schr_wave2_rule['PPrice1']
            result_df['PColor1'] = schr_wave2_rule['PColor1']
            result_df['PPrice2'] = schr_wave2_rule['PPrice2']
            result_df['PColor2'] = schr_wave2_rule['PColor2']
            result_df['Direction'] = schr_wave2_rule['Direction']
            result_df['Diff'] = schr_wave2_rule['Diff']
            
            # Add parameters info
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
        'schr_rost': 'SCHR Rost',
        'schr_wave2': 'SCHR Wave2',
        'stoch': 'Stochastic',
        'stochoscillator': 'Stochastic Oscillator'
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
    
    # Calculate additional indicator
    df_with_indicator = calculate_additional_indicator(df, rule)
    
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
    # Special case for SCHR_DIR (no parameters)
    if rule.lower().strip() == 'schr_dir':
        return 'schr_dir', {}
    
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
    if not rule:
        return False
    
    # Special case for SCHR_DIR (no parameters but valid)
    if rule.lower().strip() == 'schr_dir':
        return True
    
    # Check for parameterized indicators (containing ':')
    if ':' not in rule:
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