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
    try:
        # Fallback to relative imports when run as module
        from ..common import logger
        from ..common.constants import TradingRule, BUY, SELL, NOTRADE
    except ImportError:
        # Final fallback for pytest with -n auto
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.common import logger
        from src.common.constants import TradingRule, BUY, SELL, NOTRADE

# Import navigation system
try:
    from .term_navigation import TerminalNavigator, create_navigation_prompt, parse_navigation_input
except ImportError:
    try:
        # Fallback to relative imports when run as module
        from ..plotting.term_navigation import TerminalNavigator, create_navigation_prompt, parse_navigation_input
    except ImportError:
        # Final fallback for pytest with -n auto
        from src.plotting.term_navigation import TerminalNavigator, create_navigation_prompt, parse_navigation_input


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


def plot_ohlcv_chunks(df: pd.DataFrame, title: str = "OHLC Chunks", style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot OHLC data in chunks (no volume charts).
    
    Args:
        df (pd.DataFrame): DataFrame with OHLC data
        title (str): Base title for plots
        style (str): Plot style
        use_navigation (bool): Whether to use interactive navigation
    """
    try:
        logger.print_info("Generating OHLC chunked plots...")
        
        # Validate OHLC data
        ohlc_columns = ['Open', 'High', 'Low', 'Close']
        has_ohlc = all(col in df.columns for col in ohlc_columns)
        
        if not has_ohlc:
            logger.print_error("DataFrame must contain OHLC columns")
            return
        
        # Calculate optimal chunk size
        total_rows = len(df)
        chunk_size = calculate_optimal_chunk_size(total_rows)
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"Split {total_rows} rows into {len(chunks)} chunks of ~{chunk_size} candles each")
        
        if use_navigation:
            # Use navigation system
            navigator = TerminalNavigator(chunks, title)
            
            def plot_chunk_with_navigation(chunk: pd.DataFrame, chunk_index: int, chunk_info: dict) -> None:
                """Plot a single chunk with navigation info."""
                if len(chunk) == 0:
                    logger.print_warning("Empty chunk, skipping...")
                    return
                
                # Clear previous plots
                plt.clear_data()
                plt.clear_figure()
                
                # Set up layout with full screen size - NO VOLUME CHARTS
                plt.subplots(1, 1)  # Single price panel only
                plot_size = get_terminal_plot_size()
                
                plt.plot_size(*plot_size)
                plt.theme(style)
                
                # Create time axis with dates for this chunk
                if hasattr(chunk.index, 'strftime'):
                    # Use plotext-compatible date format
                    x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                
                # OHLC Candlestick Chart
                draw_ohlc_candles(chunk, x_values)
                
                plt.title(f"{title} - OHLC Chart (Chunk {chunk_info['index']}/{chunk_info['total']}) - {chunk_info['start_date']} to {chunk_info['end_date']}")
                plt.xlabel("Date/Time")
                if len(x_values) > 0:
                    step = max(1, len(x_values) // 10)
                    plt.xticks(x_values[::step], x_labels[::step])
                plt.ylabel("Price")
                
                plt.show()
            
            # Start navigation
            navigator.navigate(plot_chunk_with_navigation)
            
        else:
            # Original non-navigation behavior
            for i, chunk in enumerate(chunks):
                chunk_start_idx = i * chunk_size
                chunk_end_idx = min((i + 1) * chunk_size, total_rows)
                
                # Clear previous plots
                plt.clear_data()
                plt.clear_figure()
                
                # Set up layout with full screen size - NO VOLUME CHARTS
                plt.subplots(1, 1)  # Single price panel only
                plot_size = get_terminal_plot_size()
                
                plt.plot_size(*plot_size)
                plt.theme(style)
                
                # Create time axis with dates for this chunk
                if hasattr(chunk.index, 'strftime'):
                    # Use plotext-compatible date format
                    x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                
                # OHLC Candlestick Chart
                draw_ohlc_candles(chunk, x_values)
                
                # Get start and end dates for this chunk
                start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
                end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
                
                plt.title(f"{title} - OHLC Chart (Chunk {i+1}/{len(chunks)}) - {start_date} to {end_date}")
                plt.xlabel("Date/Time")
                # Set x-axis ticks to show dates
                if len(x_values) > 0:
                    step = max(1, len(x_values) // 10)  # Show ~10 date labels
                    plt.xticks(x_values[::step], x_labels[::step])
                plt.ylabel("Price")
                
                plt.show()
                
                # Add pause between chunks for better readability
                if i < len(chunks) - 1:
                    input(f"\nPress Enter to view next chunk ({i+2}/{len(chunks)})...")
        
        logger.print_success(f"Successfully displayed {len(chunks)} OHLC chunks!")
        
    except Exception as e:
        logger.print_error(f"Error generating OHLCV chunked plots: {e}")


def plot_auto_chunks(df: pd.DataFrame, title: str = "AUTO Chunks", style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot all fields in chunks with separate charts for each field.
    
    Args:
        df (pd.DataFrame): DataFrame with all fields
        title (str): Base title for plots
        style (str): Plot style
        use_navigation (bool): Whether to use interactive navigation
    """
    try:
        logger.print_info("Generating AUTO chunked plots for all fields...")
        
        # Calculate optimal chunk size
        total_rows = len(df)
        chunk_size = calculate_optimal_chunk_size(total_rows)
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"Split {total_rows} rows into {len(chunks)} chunks of ~{chunk_size} candles each")
        
        # Get all numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Skip standard columns for individual field plots
        skip_columns = {'Open', 'High', 'Low', 'Close', 'Volume', 'DateTime', 'Timestamp', 'Date', 'Time', 'Index', 'index'}
        field_columns = [col for col in numeric_columns if col not in skip_columns]
        
        if use_navigation:
            # Use AUTO navigation system with field switching
            from src.plotting.term_navigation import AutoTerminalNavigator
            navigator = AutoTerminalNavigator(chunks, title, field_columns)
            
            def plot_chunk_with_navigation(chunk: pd.DataFrame, chunk_index: int, chunk_info: dict) -> None:
                """Plot a single chunk with navigation info."""
                if len(chunk) == 0:
                    logger.print_warning("Empty chunk, skipping...")
                    return
                
                # Get start and end dates for this chunk
                start_date = chunk_info['start_date']
                end_date = chunk_info['end_date']
                
                logger.print_info(f"Displaying chunk {chunk_info['index']}/{chunk_info['total']} ({start_date} to {end_date})")
                
                # Get current field from navigator
                current_field = navigator.get_current_field()
                group_info = navigator.get_current_group_info()
                
                # Show OHLC candles for OHLC group or when no specific field is selected
                if group_info['name'] == 'OHLC' or current_field is None:
                    if len(chunk) > 0:
                        if hasattr(chunk.index, 'strftime'):
                            # Use plotext-compatible date format
                            x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                            x_values = list(range(len(chunk)))
                        else:
                            x_values = list(range(len(chunk)))
                            x_labels = [str(i) for i in x_values]
                        plt.clear_data()
                        plt.clear_figure()
                        plt.subplots(1, 1)
                        plot_size = get_terminal_plot_size()
                        plt.plot_size(*plot_size)
                        plt.theme(style)
                        draw_ohlc_candles(chunk, x_values)
                        plt.title(f"{title} - OHLC (Chunk {chunk_info['index']}) - {start_date} to {end_date}")
                        plt.xlabel("Date/Time")
                        if len(x_values) > 0:
                            step = max(1, len(x_values) // 10)
                            plt.xticks(x_values[::step], x_labels[::step])
                        plt.ylabel("Price")
                        plt.show()
                
                # Show specific field if selected and it's not OHLC
                if current_field and current_field in chunk.columns and group_info['name'] != 'OHLC':
                    _plot_single_field_chunk(chunk, current_field, f"{title} - {current_field} (Chunk {chunk_info['index']})", style)
            
            # Start navigation
            navigator.navigate(plot_chunk_with_navigation)
            
        else:
            # Original non-navigation behavior
            for i, chunk in enumerate(chunks):
                chunk_start_idx = i * chunk_size
                chunk_end_idx = min((i + 1) * chunk_size, total_rows)
                
                logger.print_info(f"Displaying chunk {i+1}/{len(chunks)} (candles {chunk_start_idx+1}-{chunk_end_idx})")
                
                # Get start and end dates for this chunk
                start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
                end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
                
                logger.print_info(f"Displaying chunk {i+1}/{len(chunks)} ({start_date} to {end_date})")
                
                # Always show OHLC candles if possible
                if len(chunk) > 0:
                    if hasattr(chunk.index, 'strftime'):
                        # Use plotext-compatible date format
                        x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                        x_values = list(range(len(chunk)))
                    else:
                        x_values = list(range(len(chunk)))
                        x_labels = [str(i) for i in x_values]
                    plt.clear_data()
                    plt.clear_figure()
                    plt.subplots(1, 1)
                    plot_size = get_terminal_plot_size()
                    plt.plot_size(*plot_size)
                    plt.theme(style)
                    draw_ohlc_candles(chunk, x_values)
                    plt.title(f"{title} - OHLC (Chunk {i+1}) - {start_date} to {end_date}")
                    plt.xlabel("Date/Time")
                    if len(x_values) > 0:
                        step = max(1, len(x_values) // 10)
                        plt.xticks(x_values[::step], x_labels[::step])
                    plt.ylabel("Price")
                    plt.show()
                
                # Then show each field separately
                for field in field_columns:
                    if field in chunk.columns:
                        _plot_single_field_chunk(chunk, field, f"{title} - {field} (Chunk {i+1})", style)
                
                # Add pause between chunks
                if i < len(chunks) - 1:
                    input(f"\nPress Enter to view next chunk ({i+2}/{len(chunks)})...")
        
        logger.print_success(f"Successfully displayed {len(chunks)} AUTO chunks!")
        
    except Exception as e:
        logger.print_error(f"Error generating AUTO chunked plots: {e}")


def plot_pv_chunks(df: pd.DataFrame, title: str = "PV Chunks", style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot PV (Pressure Vector) data in chunks with channels and signals (like PHLD).
    OHLC candles are always shown as the base layer (like in PHLD).
    
    Args:
        df (pd.DataFrame): DataFrame with PV data
        title (str): Base title for plots
        style (str): Plot style
        use_navigation (bool): Whether to use interactive navigation
    """
    try:
        logger.print_info("Generating PV chunked plots with channels and signals (like PHLD)...")
        
        # Calculate optimal chunk size
        total_rows = len(df)
        chunk_size = calculate_optimal_chunk_size(total_rows)
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"Split {total_rows} rows into {len(chunks)} chunks of ~{chunk_size} candles each")
        
        if use_navigation:
            # Use navigation system
            navigator = TerminalNavigator(chunks, title)
            
            def plot_chunk_with_navigation(chunk: pd.DataFrame, chunk_index: int, chunk_info: dict) -> None:
                """Plot a single chunk with navigation info."""
                if len(chunk) == 0:
                    logger.print_warning("Empty chunk, skipping...")
                    return
                
                # Clear previous plots
                plt.clear_data()
                plt.clear_figure()
                
                # Get start and end dates for this chunk
                start_date = chunk_info['start_date']
                end_date = chunk_info['end_date']
                
                # Set up plot with full screen size
                plt.subplots(1, 1)
                plot_size = get_terminal_plot_size()
                plt.plot_size(*plot_size)
                plt.theme(style)
                
                # Create time axis with dates for this chunk
                if hasattr(chunk.index, 'strftime'):
                    # Use plotext-compatible date format
                    x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                
                # OHLC Candlestick Chart (always as first layer, like in other rules)
                draw_ohlc_candles(chunk, x_values)
                
                # Add PV-specific overlays
                _add_pv_overlays_to_chunk(chunk, x_values)
                
                plt.title(f"{title} - PV Channels with Signals (Chunk {chunk_info['index']}/{chunk_info['total']}) - {start_date} to {end_date}")
                plt.xlabel("Date/Time")
                plt.ylabel("Price/Value")
                
                # Set x-axis ticks to show dates
                if len(x_values) > 0:
                    step = max(1, len(x_values) // 10)  # Show ~10 date labels
                    plt.xticks(x_values[::step], x_labels[::step])
                
                plt.show()
            
            # Start navigation
            navigator.navigate(plot_chunk_with_navigation)
            
        else:
            # Original non-navigation behavior
            for i, chunk in enumerate(chunks):
                chunk_start_idx = i * chunk_size
                chunk_end_idx = min((i + 1) * chunk_size, total_rows)
                
                # Clear previous plots
                plt.clear_data()
                plt.clear_figure()
                
                # Get start and end dates for this chunk
                start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
                end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
                
                # Set up plot with full screen size
                plt.subplots(1, 1)
                plot_size = get_terminal_plot_size()
                plt.plot_size(*plot_size)
                plt.theme(style)
                
                # Create time axis with dates for this chunk
                if hasattr(chunk.index, 'strftime'):
                    # Use plotext-compatible date format
                    x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                
                # OHLC Candlestick Chart (always as first layer, like in other rules)
                draw_ohlc_candles(chunk, x_values)
                
                # Add PV-specific overlays
                _add_pv_overlays_to_chunk(chunk, x_values)
                
                plt.title(f"{title} - PV Channels with Signals (Chunk {i+1}/{len(chunks)}) - {start_date} to {end_date}")
                plt.xlabel("Date/Time")
                plt.ylabel("Price/Value")
                
                # Set x-axis ticks to show dates
                if len(x_values) > 0:
                    step = max(1, len(x_values) // 10)  # Show ~10 date labels
                    plt.xticks(x_values[::step], x_labels[::step])
                
                plt.show()
                
                # Add pause between chunks
                if i < len(chunks) - 1:
                    input(f"\nPress Enter to view next chunk ({i+2}/{len(chunks)})...")
        
        logger.print_success(f"Successfully displayed {len(chunks)} PV chunks with channels and signals!")
        
    except Exception as e:
        logger.print_error(f"Error generating PV chunked plots: {e}")


def plot_sr_chunks(df: pd.DataFrame, title: str = "SR Chunks", style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot SR (Support/Resistance) data in chunks with two lines.
    
    Args:
        df (pd.DataFrame): DataFrame with SR data
        title (str): Base title for plots
        style (str): Plot style
        use_navigation (bool): Whether to use interactive navigation
    """
    try:
        logger.print_info("Generating SR chunked plots with support/resistance lines...")
        
        # Calculate optimal chunk size
        total_rows = len(df)
        chunk_size = calculate_optimal_chunk_size(total_rows)
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"Split {total_rows} rows into {len(chunks)} chunks of ~{chunk_size} candles each")
        
        if use_navigation:
            # Use navigation system
            navigator = TerminalNavigator(chunks, title)
            
            def plot_chunk_with_navigation(chunk: pd.DataFrame, chunk_index: int, chunk_info: dict) -> None:
                """Plot a single chunk with navigation info."""
                if len(chunk) == 0:
                    logger.print_warning("Empty chunk, skipping...")
                    return
                
                # Clear previous plots
                plt.clear_data()
                plt.clear_figure()
                
                # Get start and end dates for this chunk
                start_date = chunk_info['start_date']
                end_date = chunk_info['end_date']
                
                # Set up plot with full screen size
                plt.subplots(1, 1)
                plot_size = get_terminal_plot_size()
                plt.plot_size(*plot_size)
                plt.theme(style)
                
                # Create time axis with dates for this chunk
                if hasattr(chunk.index, 'strftime'):
                    # Use plotext-compatible date format
                    x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                
                # OHLC Candlestick Chart (always as first layer, like in other rules)
                draw_ohlc_candles(chunk, x_values)
                
                # Add SR-specific overlays (two lines without signals)
                _add_sr_overlays_to_chunk(chunk, x_values)
                
                plt.title(f"{title} - Support/Resistance (Chunk {chunk_info['index']}/{chunk_info['total']}) - {start_date} to {end_date}")
                plt.xlabel("Date/Time")
                plt.ylabel("Price/Value")
                
                # Set x-axis ticks to show dates
                if len(x_values) > 0:
                    step = max(1, len(x_values) // 10)  # Show ~10 date labels
                    plt.xticks(x_values[::step], x_labels[::step])
                
                plt.show()
            
            # Start navigation
            navigator.navigate(plot_chunk_with_navigation)
            
        else:
            # Original non-navigation behavior
            for i, chunk in enumerate(chunks):
                chunk_start_idx = i * chunk_size
                chunk_end_idx = min((i + 1) * chunk_size, total_rows)
                
                # Clear previous plots
                plt.clear_data()
                plt.clear_figure()
                
                # Get start and end dates for this chunk
                start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
                end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
                
                # Set up plot with full screen size
                plt.subplots(1, 1)
                plot_size = get_terminal_plot_size()
                plt.plot_size(*plot_size)
                plt.theme(style)
                
                # Create time axis with dates for this chunk
                if hasattr(chunk.index, 'strftime'):
                    # Use plotext-compatible date format
                    x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                
                # OHLC Candlestick Chart (always as first layer, like in other rules)
                draw_ohlc_candles(chunk, x_values)
                
                # Add SR-specific overlays (two lines without signals)
                _add_sr_overlays_to_chunk(chunk, x_values)
                
                plt.title(f"{title} - Support/Resistance (Chunk {i+1}/{len(chunks)}) - {start_date} to {end_date}")
                plt.xlabel("Date/Time")
                plt.ylabel("Price/Value")
                
                # Set x-axis ticks to show dates
                if len(x_values) > 0:
                    step = max(1, len(x_values) // 10)  # Show ~10 date labels
                    plt.xticks(x_values[::step], x_labels[::step])
                
                plt.show()
                
                # Add pause between chunks
                if i < len(chunks) - 1:
                    input(f"\nPress Enter to view next chunk ({i+2}/{len(chunks)})...")
        
        logger.print_success(f"Successfully displayed {len(chunks)} SR chunks!")
        
    except Exception as e:
        logger.print_error(f"Error generating SR chunked plots: {e}")


def plot_phld_chunks(df: pd.DataFrame, title: str = "PHLD Chunks", style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot PHLD (Predict High Low Direction) data in chunks with two channels and signals.
    
    Args:
        df (pd.DataFrame): DataFrame with PHLD data
        title (str): Base title for plots
        style (str): Plot style
        use_navigation (bool): Whether to use interactive navigation
    """
    try:
        logger.print_info("Generating PHLD chunked plots with channels and signals...")
        
        # Calculate optimal chunk size
        total_rows = len(df)
        chunk_size = calculate_optimal_chunk_size(total_rows)
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"Split {total_rows} rows into {len(chunks)} chunks of ~{chunk_size} candles each")
        
        if use_navigation:
            # Use navigation system
            navigator = TerminalNavigator(chunks, title)
            
            def plot_chunk_with_navigation(chunk: pd.DataFrame, chunk_index: int, chunk_info: dict) -> None:
                """Plot a single chunk with navigation info."""
                if len(chunk) == 0:
                    logger.print_warning("Empty chunk, skipping...")
                    return
                
                # Clear previous plots
                plt.clear_data()
                plt.clear_figure()
                
                # Get start and end dates for this chunk
                start_date = chunk_info['start_date']
                end_date = chunk_info['end_date']
                
                # Set up plot with full screen size
                plt.subplots(1, 1)
                plot_size = get_terminal_plot_size()
                plt.plot_size(*plot_size)
                plt.theme(style)
                
                # Create time axis with dates for this chunk
                if hasattr(chunk.index, 'strftime'):
                    # Use plotext-compatible date format
                    x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                
                # OHLC Candlestick Chart (always as first layer, like in other rules)
                draw_ohlc_candles(chunk, x_values)
                
                # Add PHLD-specific overlays (two channels and signals)
                _add_phld_overlays_to_chunk(chunk, x_values)
                
                plt.title(f"{title} - PHLD Channels & Signals (Chunk {chunk_info['index']}/{chunk_info['total']}) - {start_date} to {end_date}")
                plt.xlabel("Date/Time")
                plt.ylabel("Price/Value")
                
                # Set x-axis ticks to show dates
                if len(x_values) > 0:
                    step = max(1, len(x_values) // 10)  # Show ~10 date labels
                    plt.xticks(x_values[::step], x_labels[::step])
                
                plt.show()
            
            # Start navigation
            navigator.navigate(plot_chunk_with_navigation)
            
        else:
            # Original non-navigation behavior
            for i, chunk in enumerate(chunks):
                chunk_start_idx = i * chunk_size
                chunk_end_idx = min((i + 1) * chunk_size, total_rows)
                
                # Clear previous plots
                plt.clear_data()
                plt.clear_figure()
                
                # Get start and end dates for this chunk
                start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
                end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
                
                # Set up plot with full screen size
                plt.subplots(1, 1)
                plot_size = get_terminal_plot_size()
                plt.plot_size(*plot_size)
                plt.theme(style)
                
                # Create time axis with dates for this chunk
                if hasattr(chunk.index, 'strftime'):
                    # Use plotext-compatible date format
                    x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                
                # OHLC Candlestick Chart (always as first layer, like in other rules)
                draw_ohlc_candles(chunk, x_values)
                
                # Add PHLD-specific overlays (two channels and signals)
                _add_phld_overlays_to_chunk(chunk, x_values)
                
                plt.title(f"{title} - PHLD Channels & Signals (Chunk {i+1}/{len(chunks)}) - {start_date} to {end_date}")
                plt.xlabel("Date/Time")
                plt.ylabel("Price/Value")
                
                # Set x-axis ticks to show dates
                if len(x_values) > 0:
                    step = max(1, len(x_values) // 10)  # Show ~10 date labels
                    plt.xticks(x_values[::step], x_labels[::step])
                
                plt.show()
                
                # Add pause between chunks
                if i < len(chunks) - 1:
                    input(f"\nPress Enter to view next chunk ({i+2}/{len(chunks)})...")
        
        logger.print_success(f"Successfully displayed {len(chunks)} PHLD chunks!")
        
    except Exception as e:
        logger.print_error(f"Error generating PHLD chunked plots: {e}")


def plot_rsi_chunks(df: pd.DataFrame, rule: str, title: str = "RSI Chunks", style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot RSI data in chunks with different calculations based on rule type.
    
    Args:
        df (pd.DataFrame): DataFrame with RSI data
        rule (str): RSI rule type (rsi, rsi_mom, rsi_div)
        title (str): Base title for plots
        style (str): Plot style
        use_navigation (bool): Whether to use interactive navigation
    """
    try:
        rule_type, params = parse_rsi_rule(rule)
        logger.print_info(f"Generating {rule_type.upper()} chunked plots...")
        
        # Calculate optimal chunk size
        total_rows = len(df)
        chunk_size = calculate_optimal_chunk_size(total_rows)
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"Split {total_rows} rows into {len(chunks)} chunks of ~{chunk_size} candles each")
        
        if use_navigation:
            # Use navigation system
            navigator = TerminalNavigator(chunks, title)
            
            def plot_chunk_with_navigation(chunk: pd.DataFrame, chunk_index: int, chunk_info: dict) -> None:
                """Plot a single chunk with navigation info."""
                if len(chunk) == 0:
                    logger.print_warning("Empty chunk, skipping...")
                    return
                
                # Clear previous plots
                plt.clear_data()
                plt.clear_figure()
                
                # Get start and end dates for this chunk
                start_date = chunk_info['start_date']
                end_date = chunk_info['end_date']
                
                # Set up plot with full screen size
                plt.subplots(1, 1)
                plot_size = get_terminal_plot_size()
                plt.plot_size(*plot_size)
                plt.theme(style)
                
                # Create time axis with dates for this chunk
                if hasattr(chunk.index, 'strftime'):
                    # Use plotext-compatible date format
                    x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                
                # OHLC Candlestick Chart (always as first layer, like in other rules)
                draw_ohlc_candles(chunk, x_values)
                
                # Add RSI-specific overlays based on rule type
                _add_rsi_overlays_to_chunk(chunk, x_values, rule_type, params)
                
                plt.title(f"{title} - {rule_type.upper()} (Chunk {chunk_info['index']}/{chunk_info['total']}) - {start_date} to {end_date}")
                plt.xlabel("Date/Time")
                plt.ylabel("Price/Value")
                
                # Set x-axis ticks to show dates
                if len(x_values) > 0:
                    step = max(1, len(x_values) // 10)  # Show ~10 date labels
                    plt.xticks(x_values[::step], x_labels[::step])
                
                plt.show()
            
            # Start navigation
            navigator.navigate(plot_chunk_with_navigation)
            
        else:
            # Original non-navigation behavior
            for i, chunk in enumerate(chunks):
                chunk_start_idx = i * chunk_size
                chunk_end_idx = min((i + 1) * chunk_size, total_rows)
                
                # Get start and end dates for this chunk
                start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
                end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
                
                # Clear previous plots
                plt.clear_data()
                plt.clear_figure()
                
                # Set up plot with full screen size
                plt.subplots(1, 1)
                plot_size = get_terminal_plot_size()
                plt.plot_size(*plot_size)
                plt.theme(style)
                
                # Create time axis with dates for this chunk
                if hasattr(chunk.index, 'strftime'):
                    # Use plotext-compatible date format
                    x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                
                # OHLC Candlestick Chart (always as first layer, like in other rules)
                draw_ohlc_candles(chunk, x_values)
                
                # Add RSI-specific overlays based on rule type
                _add_rsi_overlays_to_chunk(chunk, x_values, rule_type, params)
                
                plt.title(f"{title} - {rule_type.upper()} (Chunk {i+1}/{len(chunks)}) - {start_date} to {end_date}")
                plt.xlabel("Date/Time")
                plt.ylabel("Price/Value")
                
                # Set x-axis ticks to show dates
                if len(x_values) > 0:
                    step = max(1, len(x_values) // 10)  # Show ~10 date labels
                    plt.xticks(x_values[::step], x_labels[::step])
                
                plt.show()
                
                # Add pause between chunks (no statistics)
                if i < len(chunks) - 1:
                    input(f"\nPress Enter to view next chunk ({i+2}/{len(chunks)})...")
        
        logger.print_success(f"Successfully displayed {len(chunks)} {rule_type.upper()} chunks!")
        
    except Exception as e:
        logger.print_error(f"Error generating {rule_type.upper()} chunked plots: {e}")


def plot_macd_chunks(df: pd.DataFrame, title: str = "MACD Chunks", style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot MACD data in chunks with MACD lines and trading signals.
    
    Args:
        df (pd.DataFrame): DataFrame with MACD data
        title (str): Base title for plots
        style (str): Plot style
        use_navigation (bool): Whether to use interactive navigation
    """
    try:
        logger.print_info(f"Generating MACD chunked plots...")
        
        # Calculate optimal chunk size
        total_rows = len(df)
        chunk_size = calculate_optimal_chunk_size(total_rows)
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"Split {total_rows} rows into {len(chunks)} chunks of ~{chunk_size} candles each")
        
        if use_navigation:
            # Use navigation system
            navigator = TerminalNavigator(chunks, title)
            
            def plot_chunk_with_navigation(chunk: pd.DataFrame, chunk_index: int, chunk_info: dict) -> None:
                """Plot a single chunk with navigation info."""
                if len(chunk) == 0:
                    logger.print_warning("Empty chunk, skipping...")
                    return
                
                # Clear previous plots
                plt.clear_data()
                plt.clear_figure()
                
                # Set up plot with two subplots: OHLC (50%) and MACD (50%)
                plt.subplots(2, 1)  # Two rows, equal heights
                plot_size = get_terminal_plot_size()
                plt.plot_size(*plot_size)
                plt.theme(style)
                
                # Create time axis with dates for this chunk
                if hasattr(chunk.index, 'strftime'):
                    # Use plotext-compatible date format
                    x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                
                # Plot 1: OHLC Candlestick Chart (top 50%)
                plt.subplot(1, 1)
                draw_ohlc_candles(chunk, x_values)
                
                # Add trading signals to OHLC chart
                if 'Direction' in chunk.columns:
                    _add_trading_signals_to_chunk(chunk, x_values)
                
                plt.title(f"{title} - OHLC Chart (Chunk {chunk_info['index']}/{chunk_info['total']}) - {chunk_info['start_date']} to {chunk_info['end_date']}")
                plt.ylabel("Price")
                
                # Set x-axis ticks to show dates (only for bottom subplot)
                plt.xticks([])  # Hide x-axis labels for top subplot
                
                # Plot 2: MACD Chart (bottom 50%)
                plt.subplot(2, 1)
                _add_macd_chart_to_subplot(chunk, x_values)
                plt.ylabel("MACD Value")
                plt.xlabel("Date/Time")
                
                # Set x-axis ticks to show dates
                if len(x_values) > 0:
                    step = max(1, len(x_values) // 10)  # Show ~10 date labels
                    plt.xticks(x_values[::step], x_labels[::step])
                
                plt.show()
            
            # Start navigation
            navigator.navigate(plot_chunk_with_navigation)
            
        else:
            # Original non-navigation behavior
            for i, chunk in enumerate(chunks):
                chunk_start_idx = i * chunk_size
                chunk_end_idx = min((i + 1) * chunk_size, total_rows)
                
                # Get start and end dates for this chunk
                start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
                end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
                
                # Clear previous plots
                plt.clear_data()
                plt.clear_figure()
                
                # Set up plot with two subplots: OHLC (50%) and MACD (50%)
                plt.subplots(2, 1)  # Two rows, equal heights
                plot_size = get_terminal_plot_size()
                plt.plot_size(*plot_size)
                plt.theme(style)
                
                # Create time axis with dates for this chunk
                if hasattr(chunk.index, 'strftime'):
                    # Use plotext-compatible date format
                    x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                
                # Plot 1: OHLC Candlestick Chart (top 50%)
                plt.subplot(1, 1)
                draw_ohlc_candles(chunk, x_values)
                
                # Add trading signals to OHLC chart
                if 'Direction' in chunk.columns:
                    _add_trading_signals_to_chunk(chunk, x_values)
                
                plt.title(f"{title} - OHLC Chart (Chunk {i+1}/{len(chunks)}) - {start_date} to {end_date}")
                plt.ylabel("Price")
                
                # Set x-axis ticks to show dates (only for bottom subplot)
                plt.xticks([])  # Hide x-axis labels for top subplot
                
                # Plot 2: MACD Chart (bottom 50%)
                plt.subplot(2, 1)
                _add_macd_chart_to_subplot(chunk, x_values)
                plt.ylabel("MACD Value")
                plt.xlabel("Date/Time")
                
                # Set x-axis ticks to show dates
                if len(x_values) > 0:
                    step = max(1, len(x_values) // 10)  # Show ~10 date labels
                    plt.xticks(x_values[::step], x_labels[::step])
                
                plt.show()
                
                # Show chunk statistics
                _show_chunk_statistics(chunk, f"{title} - MACD", chunk_start_idx, chunk_end_idx)
                
                # Wait for user input before showing next chunk
                if i < len(chunks) - 1:  # Don't wait after the last chunk
                    input("\nPress Enter to continue to next chunk...")
        
    except Exception as e:
        logger.print_error(f"Error in MACD chunked plotting: {e}")


def plot_indicator_chunks(df: pd.DataFrame, indicator_name: str, title: str = "Indicator Chunks", style: str = "matrix", use_navigation: bool = False, rule: str = "") -> None:
    """
    Universal function to plot any indicator data in chunks with dual subplot layout.
    
    Args:
        df (pd.DataFrame): DataFrame with indicator data
        indicator_name (str): Name of the indicator (RSI, Stochastic, CCI, etc.)
        title (str): Base title for plots
        style (str): Plot style
        use_navigation (bool): Whether to use interactive navigation
    """
    try:
        logger.print_info(f"Generating {indicator_name.upper()} chunked plots...")
        
        # Calculate optimal chunk size
        total_rows = len(df)
        chunk_size = calculate_optimal_chunk_size(total_rows)
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"Split {total_rows} rows into {len(chunks)} chunks of ~{chunk_size} candles each")
        
        if use_navigation:
            # Use navigation system
            navigator = TerminalNavigator(chunks, title)
            
            def plot_chunk_with_navigation(chunk: pd.DataFrame, chunk_index: int, chunk_info: dict) -> None:
                """Plot a single chunk with navigation info."""
                if len(chunk) == 0:
                    logger.print_warning("Empty chunk, skipping...")
                    return
                
                # Clear previous plots
                plt.clear_data()
                plt.clear_figure()
                
                # Set up plot with two subplots: OHLC (50%) and Indicator (50%)
                plt.subplots(2, 1)  # Two rows, equal heights
                plot_size = get_terminal_plot_size()
                plt.plot_size(*plot_size)
                plt.theme(style)
                
                # Create time axis with dates for this chunk
                if hasattr(chunk.index, 'strftime'):
                    # Use plotext-compatible date format
                    x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                
                # Plot 1: OHLC Candlestick Chart (top 50%)
                plt.subplot(1, 1)
                draw_ohlc_candles(chunk, x_values)
                
                # Add trading signals to OHLC chart
                if 'Direction' in chunk.columns:
                    _add_trading_signals_to_chunk(chunk, x_values)
                
                plt.title(f"{title} - OHLC Chart (Chunk {chunk_info['index']}/{chunk_info['total']}) - {chunk_info['start_date']} to {chunk_info['end_date']}")
                plt.ylabel("Price")
                
                # Set x-axis ticks to show dates (only for bottom subplot)
                plt.xticks([])  # Hide x-axis labels for top subplot
                
                # Plot 2: Indicator Chart (bottom 50%)
                plt.subplot(2, 1)
                _add_indicator_chart_to_subplot(chunk, x_values, indicator_name, rule)
                plt.ylabel(f"{indicator_name} Value")
                plt.xlabel("Date/Time")
                
                # Set x-axis ticks to show dates
                if len(x_values) > 0:
                    step = max(1, len(x_values) // 10)  # Show ~10 date labels
                    plt.xticks(x_values[::step], x_labels[::step])
                
                plt.show()
            
            # Start navigation
            navigator.navigate(plot_chunk_with_navigation)
            
        else:
            # Original non-navigation behavior
            for i, chunk in enumerate(chunks):
                chunk_start_idx = i * chunk_size
                chunk_end_idx = min((i + 1) * chunk_size, total_rows)
                
                # Get start and end dates for this chunk
                start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
                end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
                
                # Clear previous plots
                plt.clear_data()
                plt.clear_figure()
                
                # Set up plot with two subplots: OHLC (50%) and Indicator (50%)
                plt.subplots(2, 1)  # Two rows, equal heights
                plot_size = get_terminal_plot_size()
                plt.plot_size(*plot_size)
                plt.theme(style)
                
                # Create time axis with dates for this chunk
                if hasattr(chunk.index, 'strftime'):
                    # If index is datetime, use date strings in plotext-compatible format
                    x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    # Fallback to numeric indices
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                
                # Plot 1: OHLC Candlestick Chart (top 50%)
                plt.subplot(1, 1)
                draw_ohlc_candles(chunk, x_values)
                
                # Add trading signals to OHLC chart
                if 'Direction' in chunk.columns:
                    _add_trading_signals_to_chunk(chunk, x_values)
                
                plt.title(f"{title} - OHLC Chart (Chunk {i+1}/{len(chunks)}) - {start_date} to {end_date}")
                plt.ylabel("Price")
                
                # Set x-axis ticks to show dates (only for bottom subplot)
                plt.xticks([])  # Hide x-axis labels for top subplot
                
                # Plot 2: Indicator Chart (bottom 50%)
                plt.subplot(2, 1)
                _add_indicator_chart_to_subplot(chunk, x_values, indicator_name, rule)
                plt.ylabel(f"{indicator_name} Value")
                plt.xlabel("Date/Time")
                
                # Set x-axis ticks to show dates
                if len(x_values) > 0:
                    step = max(1, len(x_values) // 10)  # Show ~10 date labels
                    plt.xticks(x_values[::step], x_labels[::step])
                
                plt.show()
                
                # Show chunk statistics
                _show_chunk_statistics(chunk, f"{title} - {indicator_name}", chunk_start_idx, chunk_end_idx)
                
                # Wait for user input before showing next chunk
                if i < len(chunks) - 1:  # Don't wait after the last chunk
                    input("\nPress Enter to continue to next chunk...")
        
    except Exception as e:
        logger.print_error(f"Error in {indicator_name} chunked plotting: {e}")


def _get_field_color(field_name: str) -> str:
    """
    Get a unique color for a field based on its name.
    
    Args:
        field_name (str): Name of the field
        
    Returns:
        str: Color name for plotext
    """
    # Define a comprehensive color palette with high contrast for terminal
    colors = [
        "green+", "blue+", "red+", "yellow+", "magenta+", "cyan+",
        "white+", "orange+", "purple+", "pink+", "brown+", "gray+",
        "light_green+", "light_blue+", "light_red+", "light_yellow+",
        "light_magenta+", "light_cyan+", "light_white+", "light_orange+"
    ]
    
    # Create a hash-based color assignment for consistent colors per field
    import hashlib
    hash_value = int(hashlib.md5(field_name.encode()).hexdigest(), 16)
    color_index = hash_value % len(colors)
    
    return colors[color_index]


def _get_field_color_enhanced(field_name: str) -> str:
    """
    Get a unique color for a field with enhanced contrast for terminal display.
    
    Args:
        field_name (str): Name of the field
        
    Returns:
        str: Color name for plotext
    """
    # Enhanced color palette with better terminal contrast
    # Prioritizing colors that are most distinct in terminal
    colors = [
        "green+",      # Bright green - very distinct
        "blue+",       # Bright blue - very distinct  
        "red+",        # Bright red - very distinct
        "yellow+",     # Bright yellow - very distinct
        "magenta+",    # Bright magenta - very distinct
        "cyan+",       # Bright cyan - very distinct
        "white+",      # Bright white - very distinct
        "orange+",     # Bright orange - very distinct
        "purple+",     # Bright purple - very distinct
        "pink+",       # Bright pink - very distinct
        "light_green+", # Light green - distinct from dark green
        "light_blue+",  # Light blue - distinct from dark blue
        "light_red+",   # Light red - distinct from dark red
        "light_yellow+", # Light yellow - distinct from dark yellow
        "light_magenta+", # Light magenta - distinct from dark magenta
        "light_cyan+",   # Light cyan - distinct from dark cyan
        "light_white+",  # Light white - distinct from dark white
        "light_orange+", # Light orange - distinct from dark orange
        "brown+",       # Brown - distinct from other colors
        "gray+"         # Gray - distinct from other colors
    ]
    
    # Create a hash-based color assignment for consistent colors per field
    import hashlib
    hash_value = int(hashlib.md5(field_name.encode()).hexdigest(), 16)
    color_index = hash_value % len(colors)
    
    return colors[color_index]


def _plot_single_field_chunk(chunk: pd.DataFrame, field: str, title: str, style: str) -> None:
    """
    Plot a single field in a chunk with unique color.
    
    Args:
        chunk (pd.DataFrame): DataFrame chunk
        field (str): Field name to plot
        title (str): Plot title
        style (str): Plot style
    """
    try:
        # Get start and end dates for this chunk
        start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
        end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
        
        # Clear previous plots
        plt.clear_data()
        plt.clear_figure()
        
        # Set up plot with full screen size
        plt.subplots(1, 1)
        plot_size = get_terminal_plot_size()
        plt.plot_size(*plot_size)
        plt.theme(style)
        
        # Create time axis with dates
        if hasattr(chunk.index, 'strftime'):
            # Use plotext-compatible date format
            x_labels = [d.strftime('%d/%m/%Y') for d in chunk.index]
            x_values = list(range(len(chunk)))
        else:
            x_values = list(range(len(chunk)))
            x_labels = [str(i) for i in x_values]
        
        # Get field data
        if field in chunk.columns:
            # Handle NaN values properly
            field_data = chunk[field].copy()
            # Replace NaN with None for plotext compatibility
            field_data = field_data.replace([np.inf, -np.inf], np.nan)
            values = field_data.where(pd.notna(field_data), None).tolist()
            
            # Only plot if we have valid data
            if any(v is not None for v in values):
                # Get unique color for this field
                field_color = _get_field_color(field)
                plt.plot(x_values, values, color=field_color, label=field)
            
            plt.title(f"{title} - {start_date} to {end_date}")
            plt.xlabel("Date/Time")
            plt.ylabel(field)
            
            # Set x-axis ticks to show dates
            if len(x_values) > 0:
                step = max(1, len(x_values) // 10)  # Show ~10 date labels
                plt.xticks(x_values[::step], x_labels[::step])
            
            plt.show()
        
    except Exception as e:
        logger.print_error(f"Error plotting field {field}: {e}")


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


def _add_macd_overlays_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add MACD-specific overlays to the chunk plot (MACD lines and trading signals).
    
    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (list): X-axis values
    """
    try:
        # Add MACD lines
        if 'MACD_Line' in chunk.columns:
            macd_values = chunk['MACD_Line'].fillna(0).tolist()
            plt.plot(x_values, macd_values, color="blue+", label="MACD Line")
        
        if 'MACD_Signal' in chunk.columns:
            signal_values = chunk['MACD_Signal'].fillna(0).tolist()
            plt.plot(x_values, signal_values, color="orange+", label="Signal Line")
        
        # Add trading signals
        if 'Direction' in chunk.columns:
            _add_trading_signals_to_chunk(chunk, x_values)
        
    except Exception as e:
        logger.print_error(f"Error adding MACD overlays: {e}")


def _add_macd_chart_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add MACD chart to a separate subplot with proper scaling.
    
    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (list): X-axis values
    """
    try:
        # Add MACD lines with proper scaling
        if 'MACD_Line' in chunk.columns:
            macd_values = chunk['MACD_Line'].fillna(0).tolist()
            plt.plot(x_values, macd_values, color="blue+", label="MACD Line")
        
        if 'MACD_Signal' in chunk.columns:
            signal_values = chunk['MACD_Signal'].fillna(0).tolist()
            plt.plot(x_values, signal_values, color="orange+", label="Signal Line")
        
        # Add MACD histogram if available
        if 'MACD_Histogram' in chunk.columns:
            histogram_values = chunk['MACD_Histogram'].fillna(0).tolist()
            # Use bars for histogram
            for i, value in enumerate(histogram_values):
                if value >= 0:
                    plt.plot([x_values[i], x_values[i]], [0, value], color="green+")
                else:
                    plt.plot([x_values[i], x_values[i]], [0, value], color="red+")
        
        # Add zero line for reference (plotext doesn't support axhline, so we'll skip it)
        # plt.axhline(y=0, color="white+", linestyle="-", alpha=0.5)
        
    except Exception as e:
        logger.print_error(f"Error adding MACD chart to subplot: {e}")


def _add_indicator_chart_to_subplot(chunk: pd.DataFrame, x_values: list, indicator_name: str, rule: str = "") -> None:
    """
    Add indicator chart to a separate subplot with proper scaling.
    
    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (list): X-axis values
        indicator_name (str): Name of the indicator
        rule (str): Original rule string for parameter extraction
    """
    try:
        indicator_upper = indicator_name.upper()
        
        # RSI indicators
        if indicator_upper.startswith('RSI'):
            _add_rsi_indicator_to_subplot(chunk, x_values, rule)
        
        # Stochastic indicators
        elif indicator_upper in ['STOCH', 'STOCHASTIC', 'STOCHOSCILLATOR']:
            _add_stochastic_indicator_to_subplot(chunk, x_values)
        
        # CCI indicator
        elif indicator_upper == 'CCI':
            _add_cci_indicator_to_subplot(chunk, x_values)
        
        # Bollinger Bands
        elif indicator_upper == 'BOLLINGER_BANDS':
            _add_bollinger_bands_to_subplot(chunk, x_values)
        
        # EMA indicators
        elif indicator_upper == 'EMA':
            _add_ema_indicator_to_subplot(chunk, x_values)
        
        # ADX indicator
        elif indicator_upper == 'ADX':
            _add_adx_indicator_to_subplot(chunk, x_values)
        
        # SAR indicator
        elif indicator_upper == 'SAR':
            _add_sar_indicator_to_subplot(chunk, x_values)
        
        # SuperTrend indicator
        elif indicator_upper == 'SUPERTREND':
            _add_supertrend_indicator_to_subplot(chunk, x_values)
        
        # ATR indicator
        elif indicator_upper == 'ATR':
            _add_atr_indicator_to_subplot(chunk, x_values)
        
        # Standard Deviation
        elif indicator_upper == 'STANDARD_DEVIATION':
            _add_std_indicator_to_subplot(chunk, x_values)
        
        # OBV indicator
        elif indicator_upper == 'OBV':
            _add_obv_indicator_to_subplot(chunk, x_values)
        
        # VWAP indicator
        elif indicator_upper == 'VWAP':
            _add_vwap_indicator_to_subplot(chunk, x_values)
        
        # HMA indicator
        elif indicator_upper == 'HMA':
            _add_hma_indicator_to_subplot(chunk, x_values)
        
        # Time Series Forecast
        elif indicator_upper == 'TIME_SERIES_FORECAST':
            _add_tsf_indicator_to_subplot(chunk, x_values)
        
        # Monte Carlo
        elif indicator_upper == 'MONTE_CARLO':
            _add_monte_carlo_indicator_to_subplot(chunk, x_values)
        
        # Kelly Criterion
        elif indicator_upper == 'KELLY_CRITERION':
            _add_kelly_indicator_to_subplot(chunk, x_values)
        
        # Put/Call Ratio
        elif indicator_upper == 'PUT_CALL_RATIO':
            _add_putcall_indicator_to_subplot(chunk, x_values)
        
        # COT indicator
        elif indicator_upper == 'COT':
            _add_cot_indicator_to_subplot(chunk, x_values)
        
        # Fear & Greed
        elif indicator_upper == 'FEAR_GREED':
            _add_fear_greed_indicator_to_subplot(chunk, x_values)
        
        # Pivot Points
        elif indicator_upper == 'PIVOT_POINTS':
            _add_pivot_points_to_subplot(chunk, x_values)
        
        # Fibonacci Retracement
        elif indicator_upper == 'FIBONACCI_RETRACEMENT':
            _add_fibonacci_indicator_to_subplot(chunk, x_values)
        
        # Donchian Channel
        elif indicator_upper == 'DONCHIAN_CHANNEL':
            _add_donchian_indicator_to_subplot(chunk, x_values)
        
        # Default: try to find any column with indicator name
        else:
            _add_generic_indicator_to_subplot(chunk, x_values, indicator_name)
        
    except Exception as e:
        logger.print_error(f"Error adding {indicator_name} chart to subplot: {e}")


def _add_rsi_indicator_to_subplot(chunk: pd.DataFrame, x_values: list, rule: str = "") -> None:
    """Add RSI indicator to subplot."""
    try:
        if 'RSI' in chunk.columns:
            rsi_values = chunk['RSI'].fillna(50).tolist()
            plt.plot(x_values, rsi_values, color="purple+", label="RSI")
            
            # Extract overbought/oversold levels from rule
            overbought_level = 70  # default
            oversold_level = 30    # default
            
            if rule and ':' in rule:
                try:
                    # Parse rule like "rsi:14,10,90,open" -> extract 10 and 90
                    params = rule.split(':')[1].split(',')
                    if len(params) >= 3:
                        oversold_level = float(params[1])    # second parameter
                        overbought_level = float(params[2])  # third parameter
                except (ValueError, IndexError):
                    # If parsing fails, use defaults
                    pass
            
            # Add overbought/oversold lines with extracted levels
            plt.plot(x_values, [overbought_level] * len(x_values), color="red+")
            plt.plot(x_values, [oversold_level] * len(x_values), color="green+")
            plt.plot(x_values, [50] * len(x_values), color="white+")
        
    except Exception as e:
        logger.print_error(f"Error adding RSI indicator: {e}")


def _add_stochastic_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Stochastic indicator to subplot."""
    try:
        # Look for different possible column names for Stochastic
        k_col = None
        d_col = None
        
        # Check for various possible column names
        for col in chunk.columns:
            if 'stoch' in col.lower() and 'k' in col.lower():
                k_col = col
            elif 'stoch' in col.lower() and 'd' in col.lower():
                d_col = col
        
        # If not found, try exact matches
        if k_col is None and 'Stoch_K' in chunk.columns:
            k_col = 'Stoch_K'
        if d_col is None and 'Stoch_D' in chunk.columns:
            d_col = 'Stoch_D'
        
        # Plot %K line
        if k_col:
            k_values = chunk[k_col].fillna(50).tolist()
            plt.plot(x_values, k_values, color="blue+", label="%K")
        
        # Plot %D line
        if d_col:
            d_values = chunk[d_col].fillna(50).tolist()
            plt.plot(x_values, d_values, color="red+", label="%D")
            
        # Add overbought/oversold lines
        plt.plot(x_values, [80] * len(x_values), color="red+")
        plt.plot(x_values, [20] * len(x_values), color="green+")
        
    except Exception as e:
        logger.print_error(f"Error adding Stochastic indicator: {e}")


def _add_cci_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add CCI indicator to subplot."""
    try:
        if 'CCI' in chunk.columns:
            cci_values = chunk['CCI'].fillna(0).tolist()
            plt.plot(x_values, cci_values, color="orange+", label="CCI")
            
            # Add overbought/oversold lines
            plt.plot(x_values, [100] * len(x_values), color="red+")
            plt.plot(x_values, [-100] * len(x_values), color="green+")
            plt.plot(x_values, [0] * len(x_values), color="white+")
        
    except Exception as e:
        logger.print_error(f"Error adding CCI indicator: {e}")


def _add_bollinger_bands_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Bollinger Bands to subplot."""
    try:
        if 'BB_Upper' in chunk.columns:
            upper_values = chunk['BB_Upper'].fillna(0).tolist()
            plt.plot(x_values, upper_values, color="green+", label="Upper Band")
        
        if 'BB_Middle' in chunk.columns:
            middle_values = chunk['BB_Middle'].fillna(0).tolist()
            plt.plot(x_values, middle_values, color="white+", label="Middle Band")
        
        if 'BB_Lower' in chunk.columns:
            lower_values = chunk['BB_Lower'].fillna(0).tolist()
            plt.plot(x_values, lower_values, color="red+", label="Lower Band")
        
    except Exception as e:
        logger.print_error(f"Error adding Bollinger Bands: {e}")


def _add_ema_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add EMA indicator to subplot."""
    try:
        # Look for EMA columns
        ema_columns = [col for col in chunk.columns if col.startswith('EMA')]
        for ema_col in ema_columns:
            ema_values = chunk[ema_col].fillna(0).tolist()
            plt.plot(x_values, ema_values, label=ema_col)
        
    except Exception as e:
        logger.print_error(f"Error adding EMA indicator: {e}")


def _add_adx_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add ADX indicator to subplot."""
    try:
        if 'ADX' in chunk.columns:
            adx_values = chunk['ADX'].fillna(0).tolist()
            plt.plot(x_values, adx_values, color="blue+", label="ADX")
            
            # Add DI+ and DI- if available
            if 'DI_Plus' in chunk.columns:
                di_plus_values = chunk['DI_Plus'].fillna(0).tolist()
                plt.plot(x_values, di_plus_values, color="green+", label="DI+")
            
            if 'DI_Minus' in chunk.columns:
                di_minus_values = chunk['DI_Minus'].fillna(0).tolist()
                plt.plot(x_values, di_minus_values, color="red+", label="DI-")
        
    except Exception as e:
        logger.print_error(f"Error adding ADX indicator: {e}")


def _add_sar_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add SAR indicator to subplot."""
    try:
        if 'SAR' in chunk.columns:
            sar_values = chunk['SAR'].fillna(0).tolist()
            plt.plot(x_values, sar_values, color="yellow+", label="SAR")
        
    except Exception as e:
        logger.print_error(f"Error adding SAR indicator: {e}")


def _add_supertrend_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add SuperTrend indicator to subplot."""
    try:
        if 'SuperTrend' in chunk.columns:
            supertrend_values = chunk['SuperTrend'].fillna(0).tolist()
            plt.plot(x_values, supertrend_values, color="cyan+", label="SuperTrend")
        
    except Exception as e:
        logger.print_error(f"Error adding SuperTrend indicator: {e}")


def _add_atr_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add ATR indicator to subplot."""
    try:
        if 'ATR' in chunk.columns:
            atr_values = chunk['ATR'].fillna(0).tolist()
            plt.plot(x_values, atr_values, color="magenta+", label="ATR")
        
    except Exception as e:
        logger.print_error(f"Error adding ATR indicator: {e}")


def _add_std_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Standard Deviation indicator to subplot."""
    try:
        if 'Standard_Deviation' in chunk.columns:
            std_values = chunk['Standard_Deviation'].fillna(0).tolist()
            plt.plot(x_values, std_values, color="yellow+", label="Std Dev")
        
    except Exception as e:
        logger.print_error(f"Error adding Standard Deviation indicator: {e}")


def _add_obv_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add OBV indicator to subplot."""
    try:
        if 'OBV' in chunk.columns:
            obv_values = chunk['OBV'].fillna(0).tolist()
            plt.plot(x_values, obv_values, color="blue+", label="OBV")
        
    except Exception as e:
        logger.print_error(f"Error adding OBV indicator: {e}")


def _add_vwap_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add VWAP indicator to subplot."""
    try:
        if 'VWAP' in chunk.columns:
            vwap_values = chunk['VWAP'].fillna(0).tolist()
            plt.plot(x_values, vwap_values, color="orange+", label="VWAP")
        
    except Exception as e:
        logger.print_error(f"Error adding VWAP indicator: {e}")


def _add_hma_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add HMA indicator to subplot."""
    try:
        if 'HMA' in chunk.columns:
            hma_values = chunk['HMA'].fillna(0).tolist()
            # Check if we have valid HMA values
            if any(v != 0 for v in hma_values):
                plt.plot(x_values, hma_values, color="purple+", label="HMA")
        
    except Exception as e:
        logger.print_error(f"Error adding HMA indicator: {e}")


def _add_tsf_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Time Series Forecast indicator to subplot."""
    try:
        if 'TSF' in chunk.columns:
            tsf_values = chunk['TSF'].fillna(0).tolist()
            plt.plot(x_values, tsf_values, color="cyan+", label="TSF")
        
    except Exception as e:
        logger.print_error(f"Error adding TSF indicator: {e}")


def _add_monte_carlo_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Monte Carlo indicator to subplot."""
    try:
        if 'Monte_Carlo' in chunk.columns:
            mc_values = chunk['Monte_Carlo'].fillna(0).tolist()
            plt.plot(x_values, mc_values, color="green+", label="Monte Carlo")
        
    except Exception as e:
        logger.print_error(f"Error adding Monte Carlo indicator: {e}")


def _add_kelly_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Kelly Criterion indicator to subplot."""
    try:
        if 'Kelly_Criterion' in chunk.columns:
            kelly_values = chunk['Kelly_Criterion'].fillna(0).tolist()
            plt.plot(x_values, kelly_values, color="yellow+", label="Kelly")
        
    except Exception as e:
        logger.print_error(f"Error adding Kelly Criterion indicator: {e}")


def _add_putcall_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Put/Call Ratio indicator to subplot."""
    try:
        if 'Put_Call_Ratio' in chunk.columns:
            pcr_values = chunk['Put_Call_Ratio'].fillna(1).tolist()
            plt.plot(x_values, pcr_values, color="red+", label="Put/Call Ratio")
            
            # Add neutral line
            plt.plot(x_values, [1] * len(x_values), color="white+")
        
    except Exception as e:
        logger.print_error(f"Error adding Put/Call Ratio indicator: {e}")


def _add_cot_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add COT indicator to subplot."""
    try:
        if 'COT' in chunk.columns:
            cot_values = chunk['COT'].fillna(0).tolist()
            plt.plot(x_values, cot_values, color="blue+", label="COT")
        
    except Exception as e:
        logger.print_error(f"Error adding COT indicator: {e}")


def _add_fear_greed_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Fear & Greed indicator to subplot."""
    try:
        if 'Fear_Greed' in chunk.columns:
            fg_values = chunk['Fear_Greed'].fillna(50).tolist()
            plt.plot(x_values, fg_values, color="orange+", label="Fear & Greed")
            
            # Add extreme levels
            plt.plot(x_values, [80] * len(x_values), color="green+")
            plt.plot(x_values, [20] * len(x_values), color="red+")
            plt.plot(x_values, [50] * len(x_values), color="white+")
        
    except Exception as e:
        logger.print_error(f"Error adding Fear & Greed indicator: {e}")


def _add_pivot_points_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Pivot Points to subplot."""
    try:
        pivot_columns = ['PP', 'R1', 'R2', 'R3', 'S1', 'S2', 'S3']
        colors = ['white+', 'green+', 'green+', 'green+', 'red+', 'red+', 'red+']
        
        for i, col in enumerate(pivot_columns):
            if col in chunk.columns:
                values = chunk[col].fillna(0).tolist()
                plt.plot(x_values, values, color=colors[i], label=col)
        
    except Exception as e:
        logger.print_error(f"Error adding Pivot Points: {e}")


def _add_fibonacci_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Fibonacci Retracement to subplot."""
    try:
        fib_columns = ['Fib_0', 'Fib_236', 'Fib_382', 'Fib_500', 'Fib_618', 'Fib_786', 'Fib_100']
        colors = ['white+', 'yellow+', 'orange+', 'red+', 'purple+', 'blue+', 'green+']
        
        for i, col in enumerate(fib_columns):
            if col in chunk.columns:
                values = chunk[col].fillna(0).tolist()
                plt.plot(x_values, values, color=colors[i], label=col)
        
    except Exception as e:
        logger.print_error(f"Error adding Fibonacci Retracement: {e}")


def _add_donchian_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Donchian Channel to subplot."""
    try:
        if 'Donchian_Upper' in chunk.columns:
            upper_values = chunk['Donchian_Upper'].fillna(0).tolist()
            plt.plot(x_values, upper_values, color="green+", label="Upper")
        
        if 'Donchian_Middle' in chunk.columns:
            middle_values = chunk['Donchian_Middle'].fillna(0).tolist()
            plt.plot(x_values, middle_values, color="white+", label="Middle")
        
        if 'Donchian_Lower' in chunk.columns:
            lower_values = chunk['Donchian_Lower'].fillna(0).tolist()
            plt.plot(x_values, lower_values, color="red+", label="Lower")
        
    except Exception as e:
        logger.print_error(f"Error adding Donchian Channel: {e}")


def _add_generic_indicator_to_subplot(chunk: pd.DataFrame, x_values: list, indicator_name: str) -> None:
    """Add generic indicator to subplot by looking for columns with indicator name."""
    try:
        # Look for columns containing the indicator name
        indicator_columns = [col for col in chunk.columns if indicator_name.upper() in col.upper()]
        
        if not indicator_columns:
            # Try exact match
            if indicator_name in chunk.columns:
                indicator_columns = [indicator_name]
        
        if indicator_columns:
            for col in indicator_columns:
                values = chunk[col].fillna(0).tolist()
                plt.plot(x_values, values, label=col)
        else:
            logger.print_warning(f"No columns found for indicator: {indicator_name}")
        
    except Exception as e:
        logger.print_error(f"Error adding generic indicator {indicator_name}: {e}")


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


def _show_chunk_statistics(chunk: pd.DataFrame, title: str, start_idx: int, end_idx: int) -> None:
    """
    Show statistics for a chunk.
    
    Args:
        chunk (pd.DataFrame): DataFrame chunk
        title (str): Chunk title
        start_idx (int): Start index
        end_idx (int): End index
    """
    try:
        header_line = "=" * 80
        print(f"\n{header_line}")
        print(f"{title.upper():^80}")
        print(f"Candles {start_idx+1}-{end_idx} ({len(chunk)} bars)")
        print(f"{header_line}")
        
        # OHLC statistics
        ohlc_columns = ['Open', 'High', 'Low', 'Close']
        has_ohlc = all(col in chunk.columns for col in ohlc_columns)
        
        if has_ohlc:
            print(f"OHLC STATISTICS:")
            print(f"   Open:  {chunk['Open'].min():.5f} - {chunk['Open'].max():.5f}")
            print(f"   High:  {chunk['High'].min():.5f} - {chunk['High'].max():.5f}")
            print(f"   Low:   {chunk['Low'].min():.5f} - {chunk['Low'].max():.5f}")
            print(f"   Close: {chunk['Close'].min():.5f} - {chunk['Close'].max():.5f}")
        
        # Volume statistics
        if 'Volume' in chunk.columns:
            volume = chunk['Volume'].fillna(0)
            print(f"VOLUME STATISTICS:")
            print(f"   Total: {volume.sum():.0f}")
            print(f"   Avg:   {volume.mean():.0f}")
            print(f"   Max:   {volume.max():.0f}")
        
        # Trading signals
        if 'Direction' in chunk.columns:
            buy_count = (chunk['Direction'] == BUY).sum()
            sell_count = (chunk['Direction'] == SELL).sum()
            notrade_count = (chunk['Direction'] == NOTRADE).sum()
            
            print(f"TRADING SIGNALS:")
            print(f"   BUY:     {buy_count}")
            print(f"   SELL:    {sell_count}")
            print(f"   NO TRADE: {notrade_count}")
        
        # RSI statistics
        if 'RSI' in chunk.columns:
            rsi = chunk['RSI'].dropna()
            if len(rsi) > 0:
                print(f"RSI STATISTICS:")
                print(f"   Min: {rsi.min():.2f}")
                print(f"   Max: {rsi.max():.2f}")
                print(f"   Avg: {rsi.mean():.2f}")
        
        print(f"{header_line}\n")
        
    except Exception as e:
        logger.print_error(f"Error showing chunk statistics: {e}")


def _show_field_statistics(field_series: pd.Series, field_name: str) -> None:
    """
    Show statistics for a single field.
    
    Args:
        field_series (pd.Series): Field data
        field_name (str): Field name
    """
    try:
        clean_data = field_series.dropna()
        if len(clean_data) == 0:
            return
        
        print(f"\n{field_name.upper()} STATISTICS:")
        print(f"   Min: {clean_data.min():.5f}")
        print(f"   Max: {clean_data.max():.5f}")
        print(f"   Avg: {clean_data.mean():.5f}")
        print(f"   Std: {clean_data.std():.5f}")
        
    except Exception as e:
        logger.print_error(f"Error showing field statistics: {e}")


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
        
        # Handle RSI variants with dual subplot
        if rule_upper.startswith('RSI'):
            plot_indicator_chunks(df, 'RSI', title, style, use_navigation, rule)
        
        # Handle MACD (keep existing MACD logic for compatibility)
        elif rule_upper.startswith('MACD'):
            plot_macd_chunks(df, title, style, use_navigation)
        
        # Handle special rules that don't need dual subplot
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
        
        # Handle all other indicators with dual subplot
        elif rule_upper in ['STOCHASTIC', 'CCI', 'BOLLINGER_BANDS', 'EMA', 'ADX', 'SAR', 
                           'SUPERTREND', 'ATR', 'STANDARD_DEVIATION', 'OBV', 'VWAP',
                           'HMA', 'TIME_SERIES_FORECAST', 'MONTE_CARLO', 'KELLY_CRITERION',
                           'PUT_CALL_RATIO', 'COT', 'FEAR_GREED', 'PIVOT_POINTS',
                           'FIBONACCI_RETRACEMENT', 'DONCHIAN_CHANNEL']:
            plot_indicator_chunks(df, rule_upper, title, style, use_navigation, rule)
        
        # Handle parameterized indicators
        elif ':' in rule:
            # Extract indicator name from parameterized rule (e.g., "stochastic:14,3,3" -> "STOCHASTIC")
            indicator_name = rule.split(':')[0].upper()
            plot_indicator_chunks(df, indicator_name, title, style, use_navigation, rule)
        
        else:
            # Try to use as generic indicator
            plot_indicator_chunks(df, rule_upper, title, style, use_navigation, rule)
        
    except Exception as e:
        logger.print_error(f"Error in chunked terminal plotting: {e}") 