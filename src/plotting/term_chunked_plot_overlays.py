# -*- coding: utf-8 -*-
# src/plotting/term_chunked_plot_overlays.py

"""
Overlay functions for terminal chunked plotting.
Contains functions to add specific overlays (PV, SR, PHLD, RSI, MACD) to chunk plots.
"""

import pandas as pd
import plotext as plt
from typing import List, Dict, Any

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
except ImportError:
    try:
        from src.common import logger
    except ImportError:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.common import logger

from .term_chunked_plot_helpers import _has_trading_signals, _add_trading_signals_to_chunk


def _add_pv_overlays_to_chunk(chunk: pd.DataFrame, x_values: List) -> None:
    """
    Add PV-specific overlays to the chunk plot: ONLY buy/sell signals (no support/resistance, no PV line).

    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (List): X-axis values
    """
    try:
        # Only BUY/SELL signals
        if _has_trading_signals(chunk):
            _add_trading_signals_to_chunk(chunk, x_values)
    except Exception as e:
        logger.print_error(f"Error adding PV overlays: {e}")


def _add_sr_overlays_to_chunk(chunk: pd.DataFrame, x_values: List) -> None:
    """
    Add SR-specific overlays to the chunk plot (two lines without signals).

    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (List): X-axis values
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


def _add_phld_overlays_to_chunk(chunk: pd.DataFrame, x_values: List) -> None:
    """
    Add PHLD-specific overlays to the chunk plot (two channels and signals).

    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (List): X-axis values
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
        if _has_trading_signals(chunk):
            _add_trading_signals_to_chunk(chunk, x_values)

    except Exception as e:
        logger.print_error(f"Error adding PHLD overlays: {e}")


def _add_rsi_overlays_to_chunk(chunk: pd.DataFrame, x_values: List, rule_type: str, params: Dict[str, Any]) -> None:
    """
    Add RSI-specific overlays to the chunk plot based on rule type.

    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (List): X-axis values
        rule_type (str): RSI rule type (rsi, rsi_mom, rsi_div)
        params (Dict): RSI parameters
    """
    try:
        # Add support and resistance lines with yellow and blue colors
        if 'PPrice1' in chunk.columns:  # Support level
            pprice1_values = chunk['PPrice1'].fillna(0).tolist()
            plt.plot(
                x_values,
                pprice1_values,
                color="yellow+",
                label="Support",
                marker="s")

        if 'PPrice2' in chunk.columns:  # Resistance level
            pprice2_values = chunk['PPrice2'].fillna(0).tolist()
            plt.plot(
                x_values,
                pprice2_values,
                color="blue+",
                label="Resistance",
                marker="s")

        # Add RSI as Line table (without markers, only line)
        # check for RSI column (case insensitive)
        rsi_col = None
        for col in chunk.columns:
            if col.lower() == 'rsi':
                rsi_col = col
                break

        if rsi_col:
            rsi_values = chunk[rsi_col].fillna(50).tolist()
            plt.plot(x_values, rsi_values, color="cyan+", label=f"RSI ({rule_type})")

        # Add RSI momentum for momentum variant
        if rule_type == 'rsi_mom' and 'RSI_Momentum' in chunk.columns:
            momentum_values = chunk['RSI_Momentum'].fillna(0).tolist()
            plt.plot(x_values, momentum_values, color="magenta+", label="RSI Momentum")

        # Add divergence strength for divergence variant
        if rule_type == 'rsi_div' and 'Diff' in chunk.columns:
            diff_values = chunk['Diff'].fillna(0).tolist()
            plt.plot(x_values, diff_values, color="cyan+", label="Divergence Strength")

        # Add trading signals with red/aqua colors
        if 'Direction' in chunk.columns:
            _add_trading_signals_to_chunk(chunk, x_values)

    except Exception as e:
        logger.print_error(f"Error adding RSI overlays: {e}")


def _add_macd_overlays_to_chunk(chunk: pd.DataFrame, x_values: List) -> None:
    """
    Add MACD-specific overlays to the chunk plot (MACD lines and trading signals).

    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (List): X-axis values
    """
    try:
        # Add MACD lines
        if 'MACD_Line' in chunk.columns:
            macd_values = chunk['MACD_Line'].fillna(0).tolist()
            plt.plot(x_values, macd_values, color="blue+", label="MACD Line")

        if 'MACD_signal' in chunk.columns:
            signal_values = chunk['MACD_signal'].fillna(0).tolist()
            plt.plot(x_values, signal_values, color="orange+", label="signal Line")

        # Add trading signals
        if _has_trading_signals(chunk):
            _add_trading_signals_to_chunk(chunk, x_values)

    except Exception as e:
        logger.print_error(f"Error adding MACD overlays: {e}")

