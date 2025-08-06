# -*- coding: utf-8 -*-
# src/plotting/term_chunked_utils.py

"""
Utility functions for terminal chunked plotting.
Contains helper functions for data processing, size calculations, and basic plotting operations.
"""

import pandas as pd
import numpy as np
import plotext as plt
import sys
import re
from typing import Tuple, List, Dict, Any

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    # Fallback to relative imports when run as module
    from ..common import logger
    from ..common.constants import TradingRule, BUY, SELL, NOTRADE


def get_terminal_plot_size() -> Tuple[int, int]:
    """
    Determine the plot size for terminal mode based on whether -d term is used.
    
    Returns:
        Tuple[int, int]: (width, height) for the plot
    """
    # Check if -d term is explicitly used in command line arguments
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


def calculate_optimal_chunk_size(total_rows: int, target_chunks: int = 10, min_chunk_size: int = 50, max_chunk_size: int = 200) -> int:
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


def split_dataframe_into_chunks(df: pd.DataFrame, chunk_size: int) -> List[pd.DataFrame]:
    """
    Split DataFrame into chunks of specified size.
    
    Args:
        df (pd.DataFrame): DataFrame to split
        chunk_size (int): Size of each chunk
    
    Returns:
        List[pd.DataFrame]: List of DataFrame chunks
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
            raise ValueError(f"RSI rule must have exactly 4 parameters: {rule_str}")
        
        parameters = {
            'period': int(params[0]),
            'overbought': float(params[1]),
            'oversold': float(params[2]),
            'price_type': params[3].lower()
        }
        
        return rule_type, parameters
        
    except (ValueError, IndexError) as e:
        logger.print_warning(f"Invalid RSI rule format: {rule_str}. Using defaults.")
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
            # If label is not supported, use without it
            plt.candlestick(x_values, ohlc_data)
    else:
        logger.print_error("DataFrame must contain OHLC columns (Open, High, Low, Close) for candlestick plot!")


def create_time_axis(chunk: pd.DataFrame) -> Tuple[List[int], List[str]]:
    """
    Create time axis with dates for the chunk.
    
    Args:
        chunk (pd.DataFrame): DataFrame chunk
    
    Returns:
        Tuple[List[int], List[str]]: (x_values, x_labels)
    """
    if hasattr(chunk.index, 'strftime'):
        # If index is datetime, use date strings
        x_labels = [d.strftime('%Y-%m-%d %H:%M') for d in chunk.index]
        x_values = list(range(len(chunk)))
    else:
        # Fallback to numeric indices
        x_values = list(range(len(chunk)))
        x_labels = [str(i) for i in x_values]
    
    return x_values, x_labels


def setup_plot_layout(style: str = "matrix") -> None:
    """
    Set up the plot layout with full screen size.
    
    Args:
        style (str): Plot style
    """
    plt.subplots(1, 1)  # Single price panel only
    plot_size = get_terminal_plot_size()
    plt.plot_size(*plot_size)
    plt.theme(style)


def clear_plot() -> None:
    """
    Clear previous plots.
    """
    plt.clear_data()
    plt.clear_figure()


def _add_trading_signals_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add trading signals to the chunk plot.
    BUY: large yellow triangle below Low
    SELL: large magenta triangle above High
    """
    try:
        if 'Direction' not in chunk.columns:
            return
        # Get buy/sell signals
        buy_x, buy_y, sell_x, sell_y = [], [], [], []
        for i, direction in enumerate(chunk['Direction']):
            # BUY: below Low
            if direction == BUY:
                buy_x.append(x_values[i])
                if 'Low' in chunk.columns:
                    buy_y.append(chunk['Low'].iloc[i] * 0.99)
                else:
                    buy_y.append(chunk['Close'].iloc[i] * 0.99 if 'Close' in chunk.columns else 0)
            # SELL: above High
            elif direction == SELL:
                sell_x.append(x_values[i])
                if 'High' in chunk.columns:
                    sell_y.append(chunk['High'].iloc[i] * 1.01)
                else:
                    sell_y.append(chunk['Close'].iloc[i] * 1.01 if 'Close' in chunk.columns else 0)
        # Draw large markers (if Unicode is supported)
        try:
            if buy_x:
                plt.scatter(buy_x, buy_y, color="yellow+", label="BUY", marker="▲")
            if sell_x:
                plt.scatter(sell_x, sell_y, color="magenta+", label="SELL", marker="▼")
        except Exception:
            # Fallback: duplicate regular markers
            if buy_x:
                plt.scatter(buy_x, buy_y, color="yellow+", label="BUY", marker="^^")
            if sell_x:
                plt.scatter(sell_x, sell_y, color="magenta+", label="SELL", marker="vv")
    except Exception as e:
        logger.print_error(f"Error adding trading signals: {e}") 