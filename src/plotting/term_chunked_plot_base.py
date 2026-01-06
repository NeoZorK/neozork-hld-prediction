# -*- coding: utf-8 -*-
# src/plotting/term_chunked_plot_base.py

"""
Base utilities for terminal chunked plotting.
Contains common functions used across all plotting modules.
"""

import sys
import re
import pandas as pd
import plotext as plt
from typing import Tuple, Dict, Any, List

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


def get_terminal_plot_size() -> Tuple[int, int]:
    """
    Determine the plot size for terminal mode based on whether -d term is Used.

    Returns:
    Tuple[int, int]: (width, height) for the plot
    """
    # check if -d term is explicitly Used in command line arguments
    is_term_mode = False
    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv):
            if arg in ['-d', '--draw'] and i + 1 < len(sys.argv):
                if sys.argv[i + 1] == 'term':
                    is_term_mode = True
                    break

    if is_term_mode:
        # Reduced height for -d term mode
        return (200, 48)  # Reduced from 50 to 45 (10% reduction)
    else:
        # Default size for other terminal modes
        return (200, 50)


def calculate_optimal_chunk_size(
        total_rows: int,
        target_chunks: int = 10,
        min_chunk_size: int = 50,
        max_chunk_size: int = 200) -> int:
    """
    Calculate optimal chunk size based on total data length.

    Args:
    total_rows (int): Total number of rows in the dataset
    target_chunks (int): Target number of chunks (default: 10)
    min_chunk_size (int): Minimum chunk size (default: 50)
    max_chunk_size (int): Maximum chunk size (default: 200)

    Returns:
    int: Optimal chunk size
    """
    if total_rows <= 0:
        return min_chunk_size

    # Calculate base chunk size
    base_chunk_size = max(1, total_rows // target_chunks)

    # Ensure chunk size is within bounds
    chunk_size = max(min_chunk_size, min(max_chunk_size, base_chunk_size))

    # Round to nearest 10 for cleaner intervals
    chunk_size = round(chunk_size / 10) * 10

    return max(min_chunk_size, chunk_size)


def split_dataframe_into_chunks(df: pd.DataFrame,
                                chunk_size: int) -> List[pd.DataFrame]:
    """
    Split dataFrame into chunks of specified size.

    Args:
    df (pd.DataFrame): dataFrame to split
    chunk_size (int): Size of each chunk

    Returns:
    List[pd.DataFrame]: List of dataFrame chunks
    """
    if df is None or df.empty:
        return []

    chunks = []
    total_rows = len(df)

    for start_idx in range(0, total_rows, chunk_size):
        end_idx = min(start_idx + chunk_size, total_rows)
        chunk = df.iloc[start_idx:end_idx].copy()
        chunks.append(chunk)

    return chunks


def parse_rsi_rule(rule_str: str) -> Tuple[str, Dict[str, Any]]:
    """
    Parse RSI rule string to extract parameters.

    Args:
        rule_str (str): Rule string like 'rsi(14,70,30,open)' or 'rsi_mom(14,70,30,close)'

    Returns:
        Tuple[str, Dict]: (rule_type, parameters)
    """
    # Extract RSI variant
    rsi_match = re.match(r'(rsi|rsi_mom|rsi_div)\(([^)]+)\)', rule_str.lower())
    if not rsi_match:
        return rule_str, {}

    rule_type = rsi_match.group(1)
    params_str = rsi_match.group(2)

    try:
        params = [p.strip() for p in params_str.split(',')]
        if len(params) != 4:
            raise ValueError(
                f"RSI rule must have exactly 4 parameters: {rule_str}")

        parameters = {
            'period': int(params[0]),
            'overbought': float(params[1]),
            'oversold': float(params[2]),
            'price_type': params[3].lower()
        }

        return rule_type, parameters

    except (ValueError, IndexError) as e:
        logger.print_warning(
            f"Invalid RSI rule format: {rule_str}. Using defaults.")
        return rule_type, {
            'period': 14,
            'overbought': 70,
            'oversold': 30,
            'price_type': 'close'
        }


def draw_ohlc_candles(chunk, x_values):
    """
    Draw OHLC candles for the given chunk and x_values if possible.
    """
    ohlc_columns = ['Open', 'High', 'Low', 'Close']
    has_ohlc = all(col in chunk.columns for col in ohlc_columns)
    if has_ohlc:
        ohlc_data = {
            'Open': chunk['Open'].ffill().fillna(chunk['Close']).tolist(),
            'High': chunk['High'].ffill().fillna(chunk['Close']).tolist(),
            'Low': chunk['Low'].ffill().fillna(chunk['Close']).tolist(),
            'Close': chunk['Close'].ffill().fillna(chunk['Open']).tolist()
        }
        # Add explicit label for candles (if supported)
        try:
            plt.candlestick(x_values, ohlc_data, label="OHLC Candles")
        except TypeError:
            # If label is not supported, Use without it
            plt.candlestick(x_values, ohlc_data)
    else:
        logger.print_error(
            "dataFrame must contain OHLC columns (Open, High, Low, Close) for candlestick plot!")

