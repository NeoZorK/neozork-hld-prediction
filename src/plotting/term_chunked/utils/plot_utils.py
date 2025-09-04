# -*- coding: utf-8 -*-
# src/plotting/term_chunked/utils/plot_utils.py

"""
Utility functions for terminal chunked plotting.
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


def get_terminal_plot_size() -> Tuple[int, int]:
    """
    Determine the plot size for terminal mode based on whether -d term is used.
    
    Returns:
        Tuple[int, int]: (width, height) for the plot
    """
    try:
        # Try to get terminal size
        import shutil
        terminal_size = shutil.get_terminal_size()
        width = min(terminal_size.columns, 120)  # Cap at 120 for readability
        height = min(terminal_size.lines - 5, 30)  # Leave space for navigation
    except:
        # Fallback to default size
        width = 100
        height = 25
    
    return width, height


def calculate_optimal_chunk_size(total_rows: int, target_chunks: int = 10, 
                                min_chunk_size: int = 50, max_chunk_size: int = 200) -> int:
    """
    Calculate optimal chunk size based on total data length.
    
    Args:
        total_rows: Total number of rows in the dataset
        target_chunks: Target number of chunks to create
        min_chunk_size: Minimum chunk size
        max_chunk_size: Maximum chunk size
    
    Returns:
        int: Optimal chunk size
    """
    if total_rows <= min_chunk_size:
        return total_rows
    
    # Calculate base chunk size
    base_chunk_size = total_rows // target_chunks
    
    # Ensure it's within bounds
    chunk_size = max(min_chunk_size, min(base_chunk_size, max_chunk_size))
    
    # Adjust to ensure we don't have too many small chunks at the end
    if total_rows % chunk_size < min_chunk_size and total_rows > chunk_size:
        chunk_size = total_rows // (target_chunks - 1)
        chunk_size = max(min_chunk_size, min(chunk_size, max_chunk_size))
    
    return chunk_size


def split_dataframe_into_chunks(df: pd.DataFrame, chunk_size: int) -> List[pd.DataFrame]:
    """
    Split DataFrame into chunks of specified size.
    
    Args:
        df: DataFrame to split
        chunk_size: Size of each chunk
    
    Returns:
        List[pd.DataFrame]: List of DataFrame chunks
    """
    chunks = []
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size].copy()
        chunks.append(chunk)
    return chunks


def parse_rsi_rule(rule_str: str) -> Tuple[str, Dict[str, Any]]:
    """
    Parse RSI rule string to extract rule type and parameters.
    
    Args:
        rule_str: RSI rule string (e.g., 'rsi', 'rsi_mom', 'rsi_div')
    
    Returns:
        Tuple[str, Dict[str, Any]]: (rule_type, parameters)
    """
    rule_type = rule_str.lower()
    params = {}
    
    if rule_type == 'rsi':
        params = {'period': 14, 'overbought': 70, 'oversold': 30}
    elif rule_type == 'rsi_mom':
        params = {'period': 14, 'momentum_period': 5}
    elif rule_type == 'rsi_div':
        params = {'period': 14, 'divergence_threshold': 0.1}
    else:
        # Default RSI parameters
        params = {'period': 14, 'overbought': 70, 'oversold': 30}
    
    return rule_type, params


def draw_ohlc_candles(chunk, x_values):
    """
    Draw OHLC candlestick chart for a chunk.
    
    Args:
        chunk: DataFrame chunk with OHLC data
        x_values: X-axis values for plotting
    """
    try:
        # Clear previous plot
        plt.clear_data()
        plt.clear_figure()
        
        # Set up the plot
        plt.plotsize(100, 25)
        plt.theme('matrix')
        
        # Plot candlesticks
        for i, (idx, row) in enumerate(chunk.iterrows()):
            open_price = row['open']
            high_price = row['high']
            low_price = row['low']
            close_price = row['close']
            
            # Determine candle color
            color = 'green' if close_price >= open_price else 'red'
            
            # Draw the candle body
            body_top = max(open_price, close_price)
            body_bottom = min(open_price, close_price)
            
            # Draw high-low line
            plt.plot([i, i], [low_price, high_price], color='white', marker='')
            
            # Draw candle body
            if body_top != body_bottom:
                plt.plot([i, i], [body_bottom, body_top], color=color, marker='█')
            else:
                plt.plot([i], [body_top], color=color, marker='█')
        
        plt.show()
        
    except Exception as e:
        logger.print_error(f"Error drawing OHLC candles: {e}")


def _get_field_color(field_name: str) -> str:
    """
    Get color for a specific field name.
    
    Args:
        field_name: Name of the field
    
    Returns:
        str: Color name for the field
    """
    color_map = {
        'open': 'blue',
        'high': 'green', 
        'low': 'red',
        'close': 'yellow',
        'volume': 'magenta',
        'pressure_vector': 'cyan',
        'support': 'white',
        'resistance': 'white',
        'phld_signal': 'bright_green',
        'rsi': 'bright_red',
        'rsi_mom': 'bright_blue',
        'rsi_div': 'bright_magenta',
        'macd': 'bright_cyan',
        'macd_signal': 'bright_yellow',
        'macd_histogram': 'bright_white'
    }
    
    return color_map.get(field_name.lower(), 'white')


def _get_field_color_enhanced(field_name: str) -> str:
    """
    Get enhanced color for a specific field name with more options.
    
    Args:
        field_name: Name of the field
    
    Returns:
        str: Enhanced color name for the field
    """
    color_map = {
        'open': 'blue',
        'high': 'green',
        'low': 'red', 
        'close': 'yellow',
        'volume': 'magenta',
        'pressure_vector': 'cyan',
        'support': 'white',
        'resistance': 'white',
        'phld_signal': 'bright_green',
        'rsi': 'bright_red',
        'rsi_mom': 'bright_blue',
        'rsi_div': 'bright_magenta',
        'macd': 'bright_cyan',
        'macd_signal': 'bright_yellow',
        'macd_histogram': 'bright_white',
        'stochastic': 'bright_red',
        'cci': 'bright_blue',
        'bollinger_upper': 'bright_green',
        'bollinger_lower': 'bright_red',
        'bollinger_middle': 'bright_yellow',
        'ema': 'bright_cyan',
        'sma': 'bright_magenta',
        'adx': 'bright_white',
        'sar': 'bright_red',
        'supertrend': 'bright_green',
        'atr': 'bright_blue',
        'std': 'bright_yellow',
        'obv': 'bright_cyan',
        'vwap': 'bright_magenta',
        'hma': 'bright_white',
        'tsf': 'bright_red',
        'monte_carlo': 'bright_green',
        'kelly': 'bright_blue',
        'put_call': 'bright_yellow',
        'cot': 'bright_cyan',
        'fear_greed': 'bright_magenta',
        'pivot_points': 'bright_white',
        'fibonacci': 'bright_red',
        'donchian': 'bright_green',
        'wave': 'bright_blue'
    }
    
    return color_map.get(field_name.lower(), 'white')


def _plot_single_field_chunk(chunk: pd.DataFrame, field: str, title: str, style: str) -> None:
    """
    Plot a single field for a chunk.
    
    Args:
        chunk: DataFrame chunk
        field: Field name to plot
        title: Plot title
        style: Plot style
    """
    try:
        if field not in chunk.columns:
            logger.print_warning(f"Field '{field}' not found in chunk")
            return
        
        plt.clear_data()
        plt.clear_figure()
        
        # Set up the plot
        plt.plotsize(100, 25)
        plt.theme(style)
        
        # Get data
        x_values = list(range(len(chunk)))
        y_values = chunk[field].tolist()
        
        # Get color for the field
        color = _get_field_color_enhanced(field)
        
        # Plot the data
        plt.plot(x_values, y_values, color=color, marker='█')
        
        # Set title and labels
        plt.title(title)
        plt.xlabel("Index")
        plt.ylabel(field.upper())
        
        plt.show()
        
    except Exception as e:
        logger.print_error(f"Error plotting field '{field}': {e}")


def _has_trading_signals(chunk: pd.DataFrame) -> bool:
    """
    Check if chunk has trading signals.
    
    Args:
        chunk: DataFrame chunk
    
    Returns:
        bool: True if chunk has trading signals
    """
    signal_columns = ['phld_signal', 'rsi_signal', 'macd_signal', 'stochastic_signal']
    return any(col in chunk.columns for col in signal_columns)


def _show_chunk_statistics(chunk: pd.DataFrame, title: str, start_idx: int, end_idx: int) -> None:
    """
    Show statistics for a chunk.
    
    Args:
        chunk: DataFrame chunk
        title: Chunk title
        start_idx: Start index
        end_idx: End index
    """
    try:
        print(f"\n{'='*60}")
        print(f"📊 {title} - Chunk Statistics")
        print(f"{'='*60}")
        print(f"📈 Range: {start_idx} - {end_idx} ({len(chunk)} rows)")
        print(f"📅 Date Range: {chunk.index[0]} to {chunk.index[-1]}")
        
        # Show basic statistics for numeric columns
        numeric_cols = chunk.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(f"\n📊 Basic Statistics:")
            for col in numeric_cols[:5]:  # Show first 5 numeric columns
                _show_field_statistics(chunk[col], col)
        
        # Show trading signals if available
        if _has_trading_signals(chunk):
            print(f"\n🎯 Trading Signals:")
            signal_columns = ['phld_signal', 'rsi_signal', 'macd_signal', 'stochastic_signal']
            for col in signal_columns:
                if col in chunk.columns:
                    signals = chunk[col].value_counts()
                    print(f"   {col}: {dict(signals)}")
        
        print(f"{'='*60}")
        
    except Exception as e:
        logger.print_error(f"Error showing chunk statistics: {e}")


def _show_field_statistics(field_series: pd.Series, field_name: str) -> None:
    """
    Show statistics for a specific field.
    
    Args:
        field_series: Series with field data
        field_name: Name of the field
    """
    try:
        if field_series.dtype in ['object', 'string']:
            # For string fields, show value counts
            value_counts = field_series.value_counts()
            print(f"   {field_name}: {dict(value_counts.head(3))}")
        else:
            # For numeric fields, show basic stats
            stats = {
                'min': field_series.min(),
                'max': field_series.max(),
                'mean': field_series.mean(),
                'std': field_series.std()
            }
            print(f"   {field_name}: min={stats['min']:.4f}, max={stats['max']:.4f}, mean={stats['mean']:.4f}, std={stats['std']:.4f}")
    except Exception as e:
        logger.print_error(f"Error showing field statistics for '{field_name}': {e}")
