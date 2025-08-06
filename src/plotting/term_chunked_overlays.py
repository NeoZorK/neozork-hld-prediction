# -*- coding: utf-8 -*-
# src/plotting/term_chunked_overlays.py

"""
Overlay functions for terminal chunked plotting.
Contains functions for adding specific overlays to different chart types.
"""

import pandas as pd
import plotext as plt
from typing import Dict, Any

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    # Fallback to relative imports when run as module
    from ..common import logger
    from ..common.constants import TradingRule, BUY, SELL, NOTRADE

# Import from utils
try:
    from .term_chunked_utils import _add_trading_signals_to_chunk
except ImportError:
    # Fallback to relative imports when run as module
    from ..plotting.term_chunked_utils import _add_trading_signals_to_chunk


def _add_pv_overlays_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add PV-specific overlays to the chunk plot: ONLY buy/sell signals (no support/resistance, no PV line).
    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (list): X-axis values
    """
    try:
        # Only BUY/SELL signals
        if 'Direction' in chunk.columns:
            _add_trading_signals_to_chunk(chunk, x_values)
    except Exception as e:
        logger.print_error(f"Error adding PV overlays: {e}")


def _add_sr_overlays_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add SR-specific overlays to the chunk plot (two lines without signals).
    
    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (list): X-axis values
    """
    try:
        # Add support and resistance lines (no signals)
        if 'PPrice1' in chunk.columns:  # Support level
            pprice1_values = chunk['PPrice1'].fillna(0).tolist()
            plt.plot(x_values, pprice1_values, color="green+", label="Support")
        
        if 'PPrice2' in chunk.columns:  # Resistance level
            pprice2_values = chunk['PPrice2'].fillna(0).tolist()
            plt.plot(x_values, pprice2_values, color="red+", label="Resistance")
        
    except Exception as e:
        logger.print_error(f"Error adding SR overlays: {e}")


def _add_phld_overlays_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add PHLD-specific overlays to the chunk plot (two channels and signals).
    
    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (list): X-axis values
    """
    try:
        # Add support and resistance lines (channels)
        if 'PPrice1' in chunk.columns:  # Support level
            pprice1_values = chunk['PPrice1'].fillna(0).tolist()
            plt.plot(x_values, pprice1_values, color="green+", label="Support Channel")
        
        if 'PPrice2' in chunk.columns:  # Resistance level
            pprice2_values = chunk['PPrice2'].fillna(0).tolist()
            plt.plot(x_values, pprice2_values, color="red+", label="Resistance Channel")
        
        # Add trading signals
        if 'Direction' in chunk.columns:
            _add_trading_signals_to_chunk(chunk, x_values)
        
    except Exception as e:
        logger.print_error(f"Error adding PHLD overlays: {e}")


def _add_rsi_overlays_to_chunk(chunk: pd.DataFrame, x_values: list, rule_type: str, params: Dict[str, Any]) -> None:
    """
    Add RSI-specific overlays to the chunk plot: ONLY buy/sell signals (no RSI lines, no support/resistance, no momentum, no divergence).
    """
    try:
        # Only BUY/SELL signals
        if 'Direction' in chunk.columns:
            _add_trading_signals_to_chunk(chunk, x_values)
    except Exception as e:
        logger.print_error(f"Error adding RSI overlays: {e}") 