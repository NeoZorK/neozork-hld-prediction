# -*- coding: utf-8 -*-
# src/plotting/term_chunked_plot.py

"""
Enhanced terminal-based chunked plotting using plotext for displaying data in intervals.
Automatically calculates optimal chunk size based on total data length.
Supports all rules: OHLCV, AUTO, PV, SR, PHLD, and RSI variants (rsi, rsi_mom, rsi_div).
"""

import pandas as pd
import numpy as np
import plotext as plt
from typing import Optional, List, Tuple, Dict, Any
import math
import re
import sys

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    # Fallback to relative imports when run as module
    from ..common import logger
    from ..common.constants import TradingRule, BUY, SELL, NOTRADE

# Import navigation system
try:
    from .term_navigation import TerminalNavigator, create_navigation_prompt, parse_navigation_input
except ImportError:
    # Fallback to relative imports when run as module
    from ..plotting.term_navigation import TerminalNavigator, create_navigation_prompt, parse_navigation_input

# Import from refactored modules
try:
    from .term_chunked_plotters import (
        plot_ohlcv_chunks, plot_auto_chunks, plot_pv_chunks,
        plot_sr_chunks, plot_phld_chunks, plot_rsi_chunks
    )
except ImportError:
    # Fallback to relative imports when run as module
    from ..plotting.term_chunked_plotters import (
        plot_ohlcv_chunks, plot_auto_chunks, plot_pv_chunks,
        plot_sr_chunks, plot_phld_chunks, plot_rsi_chunks
    )


def plot_chunked_terminal(df: pd.DataFrame, rule: str, title: str = "Chunked Terminal Plot", style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Main function to plot data in chunks based on the rule.
    
    Args:
        df (pd.DataFrame): DataFrame with data
        rule (str): Trading rule
        title (str): Plot title
        style (str): Plot style
        use_navigation (bool): Whether to use interactive navigation
    """
    try:
        rule_upper = rule.upper()
        
        # Handle RSI variants
        if rule_upper.startswith('RSI'):
            if '(' in rule:  # Parameterized RSI rule
                plot_rsi_chunks(df, rule, title, style, use_navigation)
            else:  # Simple RSI rule
                plot_rsi_chunks(df, 'rsi(14,70,30,close)', title, style, use_navigation)
        elif rule_upper == 'OHLCV':
            plot_ohlcv_chunks(df, title, style, use_navigation)
        elif rule_upper == 'AUTO':
            plot_auto_chunks(df, title, style, use_navigation)
        elif rule_upper in ['PV', 'PRESSURE_VECTOR']:
            plot_pv_chunks(df, title, style, use_navigation)
        elif rule_upper in ['SR', 'SUPPORT_RESISTANTS']:
            plot_sr_chunks(df, title, style, use_navigation)
        elif rule_upper in ['PHLD', 'PREDICT_HIGH_LOW_DIRECTION']:
            plot_phld_chunks(df, title, style, use_navigation)
        else:
            # Default to OHLCV for unknown rules
            logger.print_warning(f"Unknown rule '{rule}', defaulting to OHLCV")
            plot_ohlcv_chunks(df, title, style, use_navigation)
        
    except Exception as e:
        logger.print_error(f"Error in chunked terminal plotting: {e}") 