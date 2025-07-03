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
from ..calculation.indicators.suportresist.donchain_ind import calculate_donchain
from ..calculation.indicators.suportresist.fiboretr_ind import calculate_fiboretr
from ..calculation.indicators.volume.obv_ind import calculate_obv
from ..calculation.indicators.volatility.stdev_ind import calculate_stdev
from ..calculation.indicators.trend.adx_ind import calculate_adx
from ..calculation.indicators.trend.sar_ind import calculate_sar
from ..calculation.indicators.sentiment.putcallratio_ind import calculate_putcallratio
from ..calculation.indicators.sentiment.cot_ind import calculate_cot
from ..calculation.indicators.sentiment.feargreed_ind import calculate_feargreed


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
    
    return indicator_name in supported_indicators


def get_supported_indicators() -> set:
    """
    Get set of supported indicators for dual chart mode.
    
    Returns:
        set: Set of supported indicator names
    """
    return {
        'rsi', 'rsi_mom', 'rsi_div', 'macd', 'stoch', 'ema', 'bb', 'atr',
        'cci', 'vwap', 'pivot', 'hma', 'tsf', 'monte', 'kelly', 'putcallratio', 'cot', 'feargreed', 'fg', 'donchain',
        'fibo', 'obv', 'stdev', 'adx', 'sar'
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
    # Алиасы для MonteCarlo
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
            
            # Удаляем возможные дубликаты
            for col in ['RSI', 'rsi', 'rsi_divergence', 'RSI_Divergence']:
                if col in result_df.columns:
                    result_df = result_df.drop(columns=[col])
            
            # Добавляем RSI
            result_df['rsi'] = rsi_values
            # Вычисляем дивергенцию: разница между изменением цены и изменением RSI
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
            simulations = int(params[0]) if len(params) > 0 else 1000
            period = int(params[1]) if len(params) > 1 else 252
            
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
            # Фильтруем пустые параметры
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
            # Фильтруем пустые параметры
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
            # Фильтруем пустые параметры
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
            
            # Calculate Donchian Channels (returns tuple: upper, middle, lower)
            upper, middle, lower = calculate_donchain(df, period)
            result_df['donchain_upper'] = upper
            result_df['donchain_middle'] = middle
            result_df['donchain_lower'] = lower
            
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
            obv_values = calculate_obv(df)
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
            
            # Удаляем возможные дубликаты
            for col in ['stoch_k', 'stoch_d', 'Stoch_K', 'Stoch_D']:
                if col in result_df.columns:
                    result_df = result_df.drop(columns=[col])
            
            # Рассчитываем Stochastic Oscillator
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
            
            # Удаляем возможные дубликаты
            for col in ['stochosc_k', 'stochosc_d', 'StochOsc_K', 'StochOsc_D']:
                if col in result_df.columns:
                    result_df = result_df.drop(columns=[col])
            
            # Рассчитываем Stochastic Oscillator
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
        'sar': 'SAR'
    }
    
    display_name = indicator_display_names.get(indicator_name, indicator_name.upper())
    
    return {
        'mode': mode,
        'main_chart_height': 0.6,
        'indicator_chart_height': 0.4,
        'indicator_name': display_name,
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
        from .dual_chart_fastest import plot_dual_chart_fastest
        return plot_dual_chart_fastest(
            df_with_indicator, rule, title, output_path, width, height, layout, **kwargs
        )
    elif mode == 'fast':
        from .dual_chart_fast import plot_dual_chart_fast
        return plot_dual_chart_fast(
            df_with_indicator, rule, title, output_path, width, height, layout, **kwargs
        )
    elif mode in ['mpl', 'mplfinance']:
        from .dual_chart_mpl import plot_dual_chart_mpl
        return plot_dual_chart_mpl(
            df_with_indicator, rule, title, output_path, width, height, layout, **kwargs
        )
    elif mode in ['sb', 'seaborn']:
        from .dual_chart_seaborn import plot_dual_chart_seaborn
        return plot_dual_chart_seaborn(
            df_with_indicator, rule, title, output_path, width, height, layout, **kwargs
        )
    elif mode == 'term':
        from .dual_chart_terminal import plot_dual_chart_terminal
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
    # Алиасы для MonteCarlo
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