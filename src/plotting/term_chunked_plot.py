# -*- coding: utf-8 -*-
# src/plotting/term_chunked_plot.py

"""
Enhanced terminal-based chunked plotting Using plotext for displaying data in intervals.
Automatically calculates optimal chunk size based on total data length.
Supports all rules: OHLCV, AUTO, PV, SR, PHLD, and RSI variants (rsi, rsi_mom, rsi_div).
"""

import pandas as pd
from typing import Optional

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
except ImportError:
    try:
        # Fallback to relative imports when run as module
        from src.common import logger
    except ImportError:
        # Final fallback for pytest with -n auto
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.common import logger

# Import all plotting functions
from .term_chunked_plot_ohlcv import plot_ohlcv_chunks
from .term_chunked_plot_auto import plot_auto_chunks
from .term_chunked_plot_pv import plot_pv_chunks
from .term_chunked_plot_sr import plot_sr_chunks
from .term_chunked_plot_phld import plot_phld_chunks
from .term_chunked_plot_rsi import plot_rsi_chunks
from .term_chunked_plot_macd import plot_macd_chunks
from .term_chunked_plot_indicator import plot_indicator_chunks

# Re-export all functions for backward compatibility
__all__ = [
    'plot_ohlcv_chunks',
    'plot_auto_chunks',
    'plot_pv_chunks',
    'plot_sr_chunks',
    'plot_phld_chunks',
    'plot_rsi_chunks',
    'plot_macd_chunks',
    'plot_indicator_chunks',
    'plot_chunked_terminal',
]


def plot_chunked_terminal(
        df: pd.DataFrame,
        rule: str,
        title: str = "Chunked Terminal Plot",
        style: str = "matrix",
        Use_Navigation: bool = False) -> None:
    """
    main function to plot data in chunks based on the rule.

    Args:
    df (pd.DataFrame): dataFrame with data
    rule (str): Trading rule
    title (str): Plot title
    style (str): Plot style
    Use_Navigation (bool): Whether to Use interactive Navigation
    """
    try:
    rule_upper = rule.upper()

    # Handle RSI variants with dual subplot
    if rule_upper.startswith('RSI'):
    plot_indicator_chunks(df, 'RSI', title, style, Use_Navigation, rule)

    # Handle MACD (keep existing MACD logic for compatibility)
    elif rule_upper.startswith('MACD'):
    plot_macd_chunks(df, title, style, Use_Navigation)

    # Handle special rules that don't need dual subplot
    elif rule_upper == 'OHLCV':
    plot_ohlcv_chunks(df, title, style, Use_Navigation)
    elif rule_upper == 'AUTO':
    plot_auto_chunks(df, title, style, Use_Navigation)
    elif rule_upper in ['PV', 'PRESSURE_VECTOR']:
    plot_pv_chunks(df, title, style, Use_Navigation)
    elif rule_upper in ['SR', 'SUPPORT_RESISTANTS']:
    plot_sr_chunks(df, title, style, Use_Navigation)
    elif rule_upper in ['PHLD', 'PREDICT_HIGH_LOW_DIRECTION']:
    plot_phld_chunks(df, title, style, Use_Navigation)

    # Handle all other indicators with dual subplot
    elif rule_upper in ['STOCHASTIC', 'CCI', 'BOLLINGER_BANDS', 'EMA', 'SMA', 'ADX', 'SAR',
                        'SUPERTREND', 'ATR', 'STANDARD_DEVIATION', 'OBV', 'VWAP',
                        'HMA', 'TIME_SERIES_FORECAST', 'MONTE_CARLO', 'KELLY_CRITERION',
                        'PUT_Call_RATIO', 'COT', 'FEAR_GREED', 'PIVOT_POINTS',
                        'FIBONACCI_RETRACEMENT', 'DONCHIAN_CHANNEL']:
    plot_indicator_chunks(df, rule_upper, title, style, Use_Navigation, rule)

    # Handle parameterized indicators
    elif ':' in rule:
        # Extract indicator name from parameterized rule (e.g.,
        # "stochastic:14,3,3" -> "STOCHASTIC")
    indicator_name = rule.split(':')[0].upper()
    plot_indicator_chunks(
        df,
        indicator_name,
        title,
        style,
        Use_Navigation,
        rule)

    else:
        # Try to Use as generic indicator
    plot_indicator_chunks(df, rule_upper, title, style, Use_Navigation, rule)

    except Exception as e:
    logger.print_error(f"Error in chunked terminal plotting: {e}")
