# -*- coding: utf-8 -*-
# src/plotting/term_chunked/indicators/subplots.py

"""
Subplot functions for terminal chunked plotting indicators.
"""

import pandas as pd
import numpy as np
import plotext as plt
from typing import Dict, Any

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from src.common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    try:
        # Fallback to relative imports when run as module
        from src.common import logger
        from src.common.constants import TradingRule, BUY, SELL, NOTRADE
    except ImportError:
        # Final fallback for pytest with -n auto
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
        from src.common import logger
        from src.common.constants import TradingRule, BUY, SELL, NOTRADE


def _add_indicator_chart_to_subplot(chunk: pd.DataFrame, x_values: list, 
                                    indicator_name: str, rule: str = "") -> None:
    """
    Add indicator chart to subplot.
    
    Args:
        chunk: DataFrame chunk
        x_values: X-axis values
        indicator_name: Name of the indicator
        rule: Trading rule
    """
    try:
        indicator_name_lower = indicator_name.lower()
        
        # Route to specific indicator function
        if indicator_name_lower == 'rsi':
            _add_rsi_indicator_to_subplot(chunk, x_values, rule)
        elif indicator_name_lower == 'stochastic':
            _add_stochastic_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'cci':
            _add_cci_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'bollinger':
            _add_bollinger_bands_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'ema':
            _add_ema_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'sma':
            _add_sma_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'adx':
            _add_adx_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'sar':
            _add_sar_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'supertrend':
            _add_supertrend_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'atr':
            _add_atr_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'std':
            _add_std_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'obv':
            _add_obv_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'vwap':
            _add_vwap_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'hma':
            _add_hma_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'tsf':
            _add_tsf_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'monte_carlo':
            _add_monte_carlo_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'kelly':
            _add_kelly_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'put_call':
            _add_putcall_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'cot':
            _add_cot_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'fear_greed':
            _add_fear_greed_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'pivot_points':
            _add_pivot_points_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'fibonacci':
            _add_fibonacci_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'donchian':
            _add_donchian_indicator_to_subplot(chunk, x_values)
        elif indicator_name_lower == 'wave':
            _add_wave_indicator_to_subplot(chunk, x_values)
        else:
            _add_generic_indicator_to_subplot(chunk, x_values, indicator_name)
            
    except Exception as e:
        logger.print_error(f"Error adding indicator chart to subplot: {e}")


def _add_rsi_indicator_to_subplot(chunk: pd.DataFrame, x_values: list, rule: str = "") -> None:
    """Add RSI indicator to subplot."""
    try:
        if 'rsi' in chunk.columns:
            rsi_values = chunk['rsi'].tolist()
            plt.plot(x_values, rsi_values, color='bright_red', marker='█')
            
            # Add overbought/oversold lines
            plt.hline(70, color='red', style='dashed')
            plt.hline(30, color='green', style='dashed')
    except Exception as e:
        logger.print_error(f"Error adding RSI indicator: {e}")


def _add_stochastic_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Stochastic indicator to subplot."""
    try:
        if 'stochastic' in chunk.columns:
            stoch_values = chunk['stochastic'].tolist()
            plt.plot(x_values, stoch_values, color='bright_red', marker='█')
            
            # Add overbought/oversold lines
            plt.hline(80, color='red', style='dashed')
            plt.hline(20, color='green', style='dashed')
    except Exception as e:
        logger.print_error(f"Error adding Stochastic indicator: {e}")


def _add_cci_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add CCI indicator to subplot."""
    try:
        if 'cci' in chunk.columns:
            cci_values = chunk['cci'].tolist()
            plt.plot(x_values, cci_values, color='bright_blue', marker='█')
            
            # Add overbought/oversold lines
            plt.hline(100, color='red', style='dashed')
            plt.hline(-100, color='green', style='dashed')
    except Exception as e:
        logger.print_error(f"Error adding CCI indicator: {e}")


def _add_bollinger_bands_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Bollinger Bands to subplot."""
    try:
        if 'bollinger_upper' in chunk.columns:
            upper_values = chunk['bollinger_upper'].tolist()
            plt.plot(x_values, upper_values, color='bright_green', marker='█')
        
        if 'bollinger_lower' in chunk.columns:
            lower_values = chunk['bollinger_lower'].tolist()
            plt.plot(x_values, lower_values, color='bright_red', marker='█')
        
        if 'bollinger_middle' in chunk.columns:
            middle_values = chunk['bollinger_middle'].tolist()
            plt.plot(x_values, middle_values, color='bright_yellow', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding Bollinger Bands: {e}")


def _add_ema_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add EMA indicator to subplot."""
    try:
        if 'ema' in chunk.columns:
            ema_values = chunk['ema'].tolist()
            plt.plot(x_values, ema_values, color='bright_cyan', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding EMA indicator: {e}")


def _add_sma_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add SMA indicator to subplot."""
    try:
        if 'sma' in chunk.columns:
            sma_values = chunk['sma'].tolist()
            plt.plot(x_values, sma_values, color='bright_magenta', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding SMA indicator: {e}")


def _add_adx_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add ADX indicator to subplot."""
    try:
        if 'adx' in chunk.columns:
            adx_values = chunk['adx'].tolist()
            plt.plot(x_values, adx_values, color='bright_white', marker='█')
            
            # Add trend strength line
            plt.hline(25, color='yellow', style='dashed')
    except Exception as e:
        logger.print_error(f"Error adding ADX indicator: {e}")


def _add_sar_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add SAR indicator to subplot."""
    try:
        if 'sar' in chunk.columns:
            sar_values = chunk['sar'].tolist()
            plt.plot(x_values, sar_values, color='bright_red', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding SAR indicator: {e}")


def _add_supertrend_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add SuperTrend indicator to subplot."""
    try:
        if 'supertrend' in chunk.columns:
            supertrend_values = chunk['supertrend'].tolist()
            plt.plot(x_values, supertrend_values, color='bright_green', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding SuperTrend indicator: {e}")


def _add_atr_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add ATR indicator to subplot."""
    try:
        if 'atr' in chunk.columns:
            atr_values = chunk['atr'].tolist()
            plt.plot(x_values, atr_values, color='bright_blue', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding ATR indicator: {e}")


def _add_std_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Standard Deviation indicator to subplot."""
    try:
        if 'std' in chunk.columns:
            std_values = chunk['std'].tolist()
            plt.plot(x_values, std_values, color='bright_yellow', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding Standard Deviation indicator: {e}")


def _add_obv_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add OBV indicator to subplot."""
    try:
        if 'obv' in chunk.columns:
            obv_values = chunk['obv'].tolist()
            plt.plot(x_values, obv_values, color='bright_cyan', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding OBV indicator: {e}")


def _add_vwap_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add VWAP indicator to subplot."""
    try:
        if 'vwap' in chunk.columns:
            vwap_values = chunk['vwap'].tolist()
            plt.plot(x_values, vwap_values, color='bright_magenta', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding VWAP indicator: {e}")


def _add_hma_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add HMA indicator to subplot."""
    try:
        if 'hma' in chunk.columns:
            hma_values = chunk['hma'].tolist()
            plt.plot(x_values, hma_values, color='bright_white', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding HMA indicator: {e}")


def _add_tsf_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add TSF indicator to subplot."""
    try:
        if 'tsf' in chunk.columns:
            tsf_values = chunk['tsf'].tolist()
            plt.plot(x_values, tsf_values, color='bright_red', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding TSF indicator: {e}")


def _add_monte_carlo_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Monte Carlo indicator to subplot."""
    try:
        if 'monte_carlo' in chunk.columns:
            mc_values = chunk['monte_carlo'].tolist()
            plt.plot(x_values, mc_values, color='bright_green', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding Monte Carlo indicator: {e}")


def _add_kelly_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Kelly Criterion indicator to subplot."""
    try:
        if 'kelly' in chunk.columns:
            kelly_values = chunk['kelly'].tolist()
            plt.plot(x_values, kelly_values, color='bright_blue', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding Kelly Criterion indicator: {e}")


def _add_putcall_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Put/Call Ratio indicator to subplot."""
    try:
        if 'put_call' in chunk.columns:
            pc_values = chunk['put_call'].tolist()
            plt.plot(x_values, pc_values, color='bright_yellow', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding Put/Call Ratio indicator: {e}")


def _add_cot_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add COT indicator to subplot."""
    try:
        if 'cot' in chunk.columns:
            cot_values = chunk['cot'].tolist()
            plt.plot(x_values, cot_values, color='bright_cyan', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding COT indicator: {e}")


def _add_fear_greed_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Fear & Greed indicator to subplot."""
    try:
        if 'fear_greed' in chunk.columns:
            fg_values = chunk['fear_greed'].tolist()
            plt.plot(x_values, fg_values, color='bright_magenta', marker='█')
            
            # Add extreme levels
            plt.hline(80, color='red', style='dashed')  # Extreme greed
            plt.hline(20, color='green', style='dashed')  # Extreme fear
    except Exception as e:
        logger.print_error(f"Error adding Fear & Greed indicator: {e}")


def _add_pivot_points_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Pivot Points to subplot."""
    try:
        if 'pivot_points' in chunk.columns:
            pp_values = chunk['pivot_points'].tolist()
            plt.plot(x_values, pp_values, color='bright_white', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding Pivot Points: {e}")


def _add_fibonacci_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Fibonacci Retracement to subplot."""
    try:
        if 'fibonacci' in chunk.columns:
            fib_values = chunk['fibonacci'].tolist()
            plt.plot(x_values, fib_values, color='bright_red', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding Fibonacci Retracement: {e}")


def _add_donchian_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Donchian Channel to subplot."""
    try:
        if 'donchian_upper' in chunk.columns:
            upper_values = chunk['donchian_upper'].tolist()
            plt.plot(x_values, upper_values, color='bright_green', marker='█')
        
        if 'donchian_lower' in chunk.columns:
            lower_values = chunk['donchian_lower'].tolist()
            plt.plot(x_values, lower_values, color='bright_red', marker='█')
        
        if 'donchian_middle' in chunk.columns:
            middle_values = chunk['donchian_middle'].tolist()
            plt.plot(x_values, middle_values, color='bright_yellow', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding Donchian Channel: {e}")


def _add_wave_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Wave indicator to subplot."""
    try:
        if 'wave' in chunk.columns:
            wave_values = chunk['wave'].tolist()
            plt.plot(x_values, wave_values, color='bright_blue', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding Wave indicator: {e}")


def _add_generic_indicator_to_subplot(chunk: pd.DataFrame, x_values: list, indicator_name: str) -> None:
    """Add generic indicator to subplot."""
    try:
        if indicator_name.lower() in chunk.columns:
            indicator_values = chunk[indicator_name.lower()].tolist()
            plt.plot(x_values, indicator_values, color='bright_white', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding generic indicator '{indicator_name}': {e}")
