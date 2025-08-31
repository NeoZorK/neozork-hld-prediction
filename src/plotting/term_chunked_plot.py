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
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.common import logger
        from src.common.constants import TradingRule, BUY, SELL, NOTRADE

# Import navigation system
try:
    from .term_navigation import TerminalNavigator, create_navigation_prompt, parse_navigation_input
except ImportError:
    try:
        # Fallback to relative imports when run as module
        from src.plotting.term_navigation import TerminalNavigator, create_navigation_prompt, parse_navigation_input
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
                if _has_trading_signals(chunk):
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
                if _has_trading_signals(chunk):
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
                if _has_trading_signals(chunk):
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
                if _has_trading_signals(chunk):
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
        if _has_trading_signals(chunk):
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
        if _has_trading_signals(chunk):
            _add_trading_signals_to_chunk(chunk, x_values)
        
    except Exception as e:
        logger.print_error(f"Error adding PHLD overlays: {e}")


def _add_rsi_overlays_to_chunk(chunk: pd.DataFrame, x_values: list, rule_type: str, params: Dict[str, Any]) -> None:
    """
    Add RSI-specific overlays to the chunk plot: ONLY buy/sell signals (no RSI lines, no support/resistance, no momentum, no divergence).
    """
    try:
        # Only BUY/SELL signals
        if _has_trading_signals(chunk):
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
        if _has_trading_signals(chunk):
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
        elif indicator_upper in ['BOLLINGER_BANDS', 'BB']:
            _add_bollinger_bands_to_subplot(chunk, x_values)
        
        # EMA indicators
        elif indicator_upper == 'EMA':
            _add_ema_indicator_to_subplot(chunk, x_values)
        
        # SMA indicators
        elif indicator_upper == 'SMA':
            _add_sma_indicator_to_subplot(chunk, x_values)
        
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
        elif indicator_upper in ['STANDARD_DEVIATION', 'STDEV']:
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
        elif indicator_upper in ['TIME_SERIES_FORECAST', 'TSF']:
            _add_tsf_indicator_to_subplot(chunk, x_values)
        
        # Monte Carlo
        elif indicator_upper in ['MONTE_CARLO', 'MONTE']:
            _add_monte_carlo_indicator_to_subplot(chunk, x_values)
        
        # Kelly Criterion
        elif indicator_upper in ['KELLY_CRITERION', 'KELLY']:
            _add_kelly_indicator_to_subplot(chunk, x_values)
        
        # Put/Call Ratio
        elif indicator_upper in ['PUT_CALL_RATIO', 'PUTCALLRATIO']:
            _add_putcall_indicator_to_subplot(chunk, x_values)
        
        # COT indicator
        elif indicator_upper == 'COT':
            _add_cot_indicator_to_subplot(chunk, x_values)
        
        # Fear & Greed
        elif indicator_upper in ['FEAR_GREED', 'FEARGREED']:
            _add_fear_greed_indicator_to_subplot(chunk, x_values)
        
        # Pivot Points
        elif indicator_upper in ['PIVOT_POINTS', 'PIVOT']:
            _add_pivot_points_to_subplot(chunk, x_values)
        
        # Fibonacci Retracement
        elif indicator_upper in ['FIBONACCI_RETRACEMENT', 'FIBO']:
            _add_fibonacci_indicator_to_subplot(chunk, x_values)
        
        # Donchian Channel
        elif indicator_upper in ['DONCHIAN_CHANNEL', 'DONCHAIN']:
            _add_donchian_indicator_to_subplot(chunk, x_values)
        
        # Wave indicator
        elif indicator_upper == 'WAVE':
            _add_wave_indicator_to_subplot(chunk, x_values)
        
        # Default: try to find any column with indicator name
        else:
            _add_generic_indicator_to_subplot(chunk, x_values, indicator_name)
        
    except Exception as e:
        logger.print_error(f"Error adding {indicator_name} chart to subplot: {e}")


def _add_rsi_indicator_to_subplot(chunk: pd.DataFrame, x_values: list, rule: str = "") -> None:
    """Add RSI indicator to subplot."""
    try:
        # Look for RSI column in different cases
        rsi_col = None
        if 'rsi' in chunk.columns:
            rsi_col = 'rsi'
        elif 'RSI' in chunk.columns:
            rsi_col = 'RSI'
        
        if rsi_col:
            rsi_values = chunk[rsi_col].fillna(50).tolist()
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
        else:
            logger.print_warning(f"RSI column not found in chunk. Available columns: {chunk.columns.tolist()}")
        
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
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        if 'BB_Upper' in chunk.columns:
            upper_values = chunk['BB_Upper'].fillna(0).tolist()
            # Only plot if we have valid data
            if upper_values and any(v != 0 for v in upper_values):
                plt.plot(numeric_x_values, upper_values, color="green+", label="Upper Band")
        
        if 'BB_Middle' in chunk.columns:
            middle_values = chunk['BB_Middle'].fillna(0).tolist()
            # Only plot if we have valid data
            if middle_values and any(v != 0 for v in middle_values):
                plt.plot(numeric_x_values, middle_values, color="white+", label="Middle Band")
        
        if 'BB_Lower' in chunk.columns:
            lower_values = chunk['BB_Lower'].fillna(0).tolist()
            # Only plot if we have valid data
            if lower_values and any(v != 0 for v in lower_values):
                plt.plot(numeric_x_values, lower_values, color="red+", label="Lower Band")
        
    except Exception as e:
        logger.print_error(f"Error adding Bollinger Bands: {e}")


def _add_ema_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add EMA indicator to subplot."""
    try:
        # Look for EMA columns
        ema_columns = [col for col in chunk.columns if col.startswith('EMA')]
        
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        for ema_col in ema_columns:
            ema_values = chunk[ema_col].fillna(0).tolist()
            try:
                # Try to plot with numeric x_values
                plt.plot(numeric_x_values, ema_values, label=ema_col)
            except Exception as plot_error:
                # If plotting fails, skip this column
                continue
        
    except Exception as e:
        logger.print_error(f"Error adding EMA indicator: {e}")


def _add_sma_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add SMA indicator to subplot."""
    try:
        # Look for SMA columns (case insensitive)
        sma_columns = [col for col in chunk.columns if col.upper().startswith('SMA') or col.lower() == 'sma']
        
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        for sma_col in sma_columns:
            sma_values = chunk[sma_col].fillna(0).tolist()
            try:
                # Try to plot with numeric x_values
                plt.plot(numeric_x_values, sma_values, color="blue+", label=sma_col)
            except Exception as plot_error:
                # If plotting fails, skip this column
                continue
        
        # Debug: print available columns if no SMA found
        if not sma_columns:
            logger.print_warning(f"No SMA columns found. Available columns: {list(chunk.columns)}")
        
    except Exception as e:
        logger.print_error(f"Error adding SMA indicator: {e}")


def _add_adx_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add ADX indicator to subplot."""
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        # Check for both possible column naming conventions
        adx_column = None
        di_plus_column = None
        di_minus_column = None
        
        # Try ADX_* naming convention first (from calculation function)
        if 'ADX' in chunk.columns:
            adx_column = 'ADX'
        
        if 'ADX_PlusDI' in chunk.columns:
            di_plus_column = 'ADX_PlusDI'
        elif 'DI_Plus' in chunk.columns:
            di_plus_column = 'DI_Plus'
        
        if 'ADX_MinusDI' in chunk.columns:
            di_minus_column = 'ADX_MinusDI'
        elif 'DI_Minus' in chunk.columns:
            di_minus_column = 'DI_Minus'
        
        # Plot ADX
        if adx_column:
            adx_values = chunk[adx_column].fillna(0).tolist()
            # Only plot if we have valid data
            if adx_values and any(v != 0 for v in adx_values):
                plt.plot(numeric_x_values, adx_values, color="blue+", label="ADX")
        
        # Plot DI+
        if di_plus_column:
            di_plus_values = chunk[di_plus_column].fillna(0).tolist()
            # Only plot if we have valid data
            if di_plus_values and any(v != 0 for v in di_plus_values):
                plt.plot(numeric_x_values, di_plus_values, color="green+", label="DI+")
        
        # Plot DI-
        if di_minus_column:
            di_minus_values = chunk[di_minus_column].fillna(0).tolist()
            # Only plot if we have valid data
            if di_minus_values and any(v != 0 for v in di_minus_values):
                plt.plot(numeric_x_values, di_minus_values, color="red+", label="DI-")
        
        # Fallback to Diff column (DI+ - DI- difference)
        if not any([adx_column, di_plus_column, di_minus_column]) and 'Diff' in chunk.columns:
            diff_values = chunk['Diff'].fillna(0).tolist()
            if diff_values and any(v != 0 for v in diff_values):
                plt.plot(numeric_x_values, diff_values, color="blue+", label="DI+ - DI-")
        
    except Exception as e:
        logger.print_error(f"Error adding ADX indicator: {e}")


def _add_sar_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add SAR indicator to subplot."""
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        # Check for both possible column naming conventions
        sar_column = None
        
        # Try SAR naming convention first (from calculation function)
        if 'SAR' in chunk.columns:
            sar_column = 'SAR'
        
        # Plot SAR
        if sar_column:
            sar_values = chunk[sar_column].fillna(0).tolist()
            # Only plot if we have valid data
            if sar_values and any(v != 0 for v in sar_values):
                plt.plot(numeric_x_values, sar_values, color="yellow+", label="SAR")
        
        # Fallback to PPrice* naming convention (support and resistance levels)
        if not sar_column and 'PPrice1' in chunk.columns and 'PPrice2' in chunk.columns:
            pprice1_values = chunk['PPrice1'].fillna(0).tolist()
            pprice2_values = chunk['PPrice2'].fillna(0).tolist()
            
            # Plot PPrice1 (support level - SAR with buffer)
            if pprice1_values and any(v != 0 for v in pprice1_values):
                plt.plot(numeric_x_values, pprice1_values, color="yellow+", label="SAR Support")
            
            # Plot PPrice2 (resistance level - SAR with buffer)
            if pprice2_values and any(v != 0 for v in pprice2_values):
                plt.plot(numeric_x_values, pprice2_values, color="orange+", label="SAR Resistance")
        
    except Exception as e:
        logger.print_error(f"Error adding SAR indicator: {e}")


def _add_supertrend_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add SuperTrend indicator to subplot."""
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        # Check for both possible column naming conventions
        supertrend_column = None
        
        # Try SuperTrend naming convention first (from calculation function)
        if 'SuperTrend' in chunk.columns:
            supertrend_column = 'SuperTrend'
        
        # Plot SuperTrend
        if supertrend_column:
            supertrend_values = chunk[supertrend_column].fillna(0).tolist()
            # Only plot if we have valid data
            if supertrend_values and any(v != 0 for v in supertrend_values):
                plt.plot(numeric_x_values, supertrend_values, color="green+", label="SuperTrend")
        
        # Fallback to PPrice* naming convention (support and resistance levels)
        if not supertrend_column and 'PPrice1' in chunk.columns and 'PPrice2' in chunk.columns:
            pprice1_values = chunk['PPrice1'].fillna(0).tolist()
            pprice2_values = chunk['PPrice2'].fillna(0).tolist()
            
            # Plot PPrice1 (support level - SuperTrend with buffer)
            if pprice1_values and any(v != 0 for v in pprice1_values):
                plt.plot(numeric_x_values, pprice1_values, color="green+", label="SuperTrend Support")
            
            # Plot PPrice2 (resistance level - SuperTrend with buffer)
            if pprice2_values and any(v != 0 for v in pprice2_values):
                plt.plot(numeric_x_values, pprice2_values, color="red+", label="SuperTrend Resistance")
        
    except Exception as e:
        logger.print_error(f"Error adding SuperTrend indicator: {e}")


def _add_atr_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add ATR indicator to subplot."""
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        if 'ATR' in chunk.columns:
            atr_values = chunk['ATR'].fillna(0).tolist()
            plt.plot(numeric_x_values, atr_values, color="magenta+", label="ATR")
        
    except Exception as e:
        logger.print_error(f"Error adding ATR indicator: {e}")


def _add_std_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Standard Deviation indicator to subplot."""
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        # Check for both possible column names
        std_column = None
        if 'StDev' in chunk.columns:
            std_column = 'StDev'
        elif 'Standard_Deviation' in chunk.columns:
            std_column = 'Standard_Deviation'
        elif 'Diff' in chunk.columns:
            std_column = 'Diff'  # STDEV values are stored in Diff column
        
        if std_column:
            std_values = chunk[std_column].fillna(0).tolist()
            # Only plot if we have valid data
            if std_values and any(v != 0 for v in std_values):
                plt.plot(numeric_x_values, std_values, color="yellow+", label="Std Dev")
        
    except Exception as e:
        logger.print_error(f"Error adding Standard Deviation indicator: {e}")


def _add_obv_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add OBV indicator to subplot."""
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        # Check for both possible column names
        obv_column = None
        if 'OBV' in chunk.columns:
            obv_column = 'OBV'
        elif 'Diff' in chunk.columns:
            obv_column = 'Diff'  # OBV values are stored in Diff column
        
        if obv_column:
            obv_values = chunk[obv_column].fillna(0).tolist()
            # Only plot if we have valid data
            if obv_values and any(v != 0 for v in obv_values):
                plt.plot(numeric_x_values, obv_values, color="blue+", label="OBV")
        
    except Exception as e:
        logger.print_error(f"Error adding OBV indicator: {e}")


def _add_vwap_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add VWAP indicator to subplot."""
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        if 'VWAP' in chunk.columns:
            vwap_values = chunk['VWAP'].fillna(0).tolist()
            plt.plot(numeric_x_values, vwap_values, color="orange+", label="VWAP")
        
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
        if 'TSForecast' in chunk.columns:
            tsf_values = chunk['TSForecast'].fillna(0).tolist()
            # Ensure x_values are numeric for plotext compatibility
            numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
            plt.plot(numeric_x_values, tsf_values, color="cyan+", label="TSF")
        
    except Exception as e:
        logger.print_error(f"Error adding TSF indicator: {e}")


def _add_monte_carlo_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Monte Carlo indicator to subplot."""
    try:
        if 'MonteCarlo' in chunk.columns:
            mc_values = chunk['MonteCarlo'].fillna(0).tolist()
            # Ensure x_values are numeric for plotext compatibility
            numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
            plt.plot(numeric_x_values, mc_values, color="green+", label="Monte Carlo")
        
    except Exception as e:
        logger.print_error(f"Error adding Monte Carlo indicator: {e}")


def _add_kelly_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Kelly Criterion indicator to subplot."""
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        # Check for both possible column names
        kelly_column = None
        if 'Kelly' in chunk.columns:
            kelly_column = 'Kelly'
        elif 'Kelly_Criterion' in chunk.columns:
            kelly_column = 'Kelly_Criterion'
        elif 'Diff' in chunk.columns:
            kelly_column = 'Diff'  # Kelly values are stored in Diff column
        
        if kelly_column:
            kelly_values = chunk[kelly_column].fillna(0).tolist()
            # Only plot if we have valid data
            if kelly_values and any(v != 0 for v in kelly_values):
                plt.plot(numeric_x_values, kelly_values, color="yellow+", label="Kelly")
        
    except Exception as e:
        logger.print_error(f"Error adding Kelly Criterion indicator: {e}")


def _add_putcall_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Put/Call Ratio indicator to subplot."""
    try:
        if 'PutCallRatio' in chunk.columns:
            pcr_values = chunk['PutCallRatio'].fillna(50).tolist()
            # Ensure x_values are numeric for plotext compatibility
            numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
            plt.plot(numeric_x_values, pcr_values, color="red+", label="Put/Call Ratio")
            
            # Add neutral line
            plt.plot(numeric_x_values, [50] * len(numeric_x_values), color="white+")
        
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
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        # Check for both possible column names
        fg_column = None
        if 'FearGreed' in chunk.columns:
            fg_column = 'FearGreed'
        elif 'Fear_Greed' in chunk.columns:
            fg_column = 'Fear_Greed'
        elif 'Diff' in chunk.columns:
            fg_column = 'Diff'  # Fear & Greed values are stored in Diff column
        
        if fg_column:
            fg_values = chunk[fg_column].fillna(50).tolist()
            # Only plot if we have valid data
            if fg_values and any(v != 50 for v in fg_values):
                plt.plot(numeric_x_values, fg_values, color="orange+", label="Fear & Greed")
                
                # Add extreme levels
                plt.plot(numeric_x_values, [80] * len(numeric_x_values), color="green+")
                plt.plot(numeric_x_values, [20] * len(numeric_x_values), color="red+")
                plt.plot(numeric_x_values, [50] * len(numeric_x_values), color="white+")
        
    except Exception as e:
        logger.print_error(f"Error adding Fear & Greed indicator: {e}")


def _add_pivot_points_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Pivot Points to subplot."""
    try:
        # Check for both possible column naming conventions
        pivot_columns = []
        colors = []
        
        # Try Pivot_* naming convention first (from calculation function)
        if 'Pivot_PP' in chunk.columns:
            pivot_columns = ['Pivot_PP', 'Pivot_R1', 'Pivot_S1']
            colors = ['white+', 'green+', 'red+']
        # Fallback to short naming convention
        elif 'PP' in chunk.columns:
            pivot_columns = ['PP', 'R1', 'R2', 'R3', 'S1', 'S2', 'S3']
            colors = ['white+', 'green+', 'green+', 'green+', 'red+', 'red+', 'red+']
        
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        for i, col in enumerate(pivot_columns):
            if col in chunk.columns:
                values = chunk[col].fillna(0).tolist()
                # Only plot if we have valid data
                if values and any(v != 0 for v in values):
                    plt.plot(numeric_x_values, values, color=colors[i], label=col)
        
    except Exception as e:
        logger.print_error(f"Error adding Pivot Points: {e}")


def _add_fibonacci_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Fibonacci Retracement to subplot."""
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        # Check for both possible column naming conventions
        fib_columns = []
        colors = []
        
        # Try FibRetr_* naming convention first (from calculation function)
        if 'FibRetr_236' in chunk.columns:
            fib_columns = ['FibRetr_236', 'FibRetr_382', 'FibRetr_618']
            colors = ['yellow+', 'orange+', 'purple+']
        # Fallback to Fib_* naming convention
        elif 'Fib_236' in chunk.columns:
            fib_columns = ['Fib_0', 'Fib_236', 'Fib_382', 'Fib_500', 'Fib_618', 'Fib_786', 'Fib_100']
            colors = ['white+', 'yellow+', 'orange+', 'red+', 'purple+', 'blue+', 'green+']
        # Fallback to PPrice* naming convention (support and resistance levels)
        elif 'PPrice1' in chunk.columns and 'PPrice2' in chunk.columns:
            fib_columns = ['PPrice1', 'PPrice2']  # Support and resistance levels
            colors = ['green+', 'red+']  # Support (green), Resistance (red)
        
        for i, col in enumerate(fib_columns):
            if col in chunk.columns:
                values = chunk[col].fillna(0).tolist()
                # Only plot if we have valid data
                if values and any(v != 0 for v in values):
                    plt.plot(numeric_x_values, values, color=colors[i], label=col)
        
    except Exception as e:
        logger.print_error(f"Error adding Fibonacci Retracement: {e}")


def _add_donchian_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Donchian Channel to subplot."""
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        # Check for both possible column naming conventions
        upper_column = None
        middle_column = None
        lower_column = None
        
        # Try Donchain_* naming convention first (from calculation function)
        if 'Donchain_Upper' in chunk.columns:
            upper_column = 'Donchain_Upper'
        elif 'Donchian_Upper' in chunk.columns:
            upper_column = 'Donchian_Upper'
        
        if 'Donchain_Middle' in chunk.columns:
            middle_column = 'Donchain_Middle'
        elif 'Donchian_Middle' in chunk.columns:
            middle_column = 'Donchian_Middle'
        
        if 'Donchain_Lower' in chunk.columns:
            lower_column = 'Donchain_Lower'
        elif 'Donchian_Lower' in chunk.columns:
            lower_column = 'Donchian_Lower'
        
        # Plot upper band
        if upper_column:
            upper_values = chunk[upper_column].fillna(0).tolist()
            # Only plot if we have valid data
            if upper_values and any(v != 0 for v in upper_values):
                plt.plot(numeric_x_values, upper_values, color="green+", label="Upper")
        
        # Plot middle band
        if middle_column:
            middle_values = chunk[middle_column].fillna(0).tolist()
            # Only plot if we have valid data
            if middle_values and any(v != 0 for v in middle_values):
                plt.plot(numeric_x_values, middle_values, color="white+", label="Middle")
        
        # Plot lower band
        if lower_column:
            lower_values = chunk[lower_column].fillna(0).tolist()
            # Only plot if we have valid data
            if lower_values and any(v != 0 for v in lower_values):
                plt.plot(numeric_x_values, lower_values, color="red+", label="Lower")
        
        # Fallback to PPrice* naming convention (support and resistance levels)
        if not any([upper_column, middle_column, lower_column]) and 'PPrice1' in chunk.columns and 'PPrice2' in chunk.columns:
            upper_column = 'PPrice2'  # Resistance level (upper band)
            middle_column = None  # No middle band in PPrice columns
            lower_column = 'PPrice1'  # Support level (lower band)
            
            # Plot upper band (PPrice2)
            upper_values = chunk[upper_column].fillna(0).tolist()
            if upper_values and any(v != 0 for v in upper_values):
                plt.plot(numeric_x_values, upper_values, color="green+", label="Upper")
            
            # Plot lower band (PPrice1)
            lower_values = chunk[lower_column].fillna(0).tolist()
            if lower_values and any(v != 0 for v in lower_values):
                plt.plot(numeric_x_values, lower_values, color="red+", label="Lower")
        
    except Exception as e:
        logger.print_error(f"Error adding Donchian Channel: {e}")


def _add_wave_indicator_to_subplot(chunk: pd.DataFrame, x_values: list) -> None:
    """Add Wave indicator to subplot."""
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        
        # Check for Wave indicator columns with different naming conventions
        plot_wave_col = None
        plot_color_col = None
        plot_fastline_col = None
        ma_line_col = None
        
        # Try different column naming conventions
        if '_plot_wave' in chunk.columns:
            plot_wave_col = '_plot_wave'
        elif '_Plot_Wave' in chunk.columns:
            plot_wave_col = '_Plot_Wave'
        
        if '_plot_color' in chunk.columns:
            plot_color_col = '_plot_color'
        elif '_Plot_Color' in chunk.columns:
            plot_color_col = '_Plot_Color'
        
        if '_plot_fastline' in chunk.columns:
            plot_fastline_col = '_plot_fastline'
        elif '_Plot_FastLine' in chunk.columns:
            plot_fastline_col = '_Plot_FastLine'
        
        if 'MA_Line' in chunk.columns:
            ma_line_col = 'MA_Line'
        
        # Plot Wave line with dynamic colors based on signals
        if plot_wave_col and plot_color_col:
            wave_values = chunk[plot_wave_col].fillna(0).tolist()
            color_values = chunk[plot_color_col].fillna(0).tolist()
            
            # Create separate arrays for different signal types
            red_x = []
            red_y = []
            blue_x = []
            blue_y = []
            
            for i, (wave_val, color_val) in enumerate(zip(wave_values, color_values)):
                if wave_val != 0 and not pd.isna(wave_val):
                    if color_val == 1:  # BUY signal
                        red_x.append(numeric_x_values[i])
                        red_y.append(wave_val)
                    elif color_val == 2:  # SELL signal
                        blue_x.append(numeric_x_values[i])
                        blue_y.append(wave_val)
            
            # Plot red segments (BUY signals)
            if red_x and red_y:
                plt.plot(red_x, red_y, color="red+", label="Wave (BUY)")
            
            # Plot blue segments (SELL signals)
            if blue_x and blue_y:
                plt.plot(blue_x, blue_y, color="blue+", label="Wave (SELL)")
        
        # Plot Fast Line (thin red dotted line)
        if plot_fastline_col:
            fastline_values = chunk[plot_fastline_col].fillna(0).tolist()
            if fastline_values and any(v != 0 for v in fastline_values):
                plt.plot(numeric_x_values, fastline_values, color="red+", label="Fast Line")
        
        # Plot MA Line (light blue line)
        if ma_line_col:
            ma_values = chunk[ma_line_col].fillna(0).tolist()
            if ma_values and any(v != 0 for v in ma_values):
                plt.plot(numeric_x_values, ma_values, color="cyan+", label="MA Line")
        
        # Add zero line for reference
        plt.plot(numeric_x_values, [0] * len(numeric_x_values), color="white+", label="Zero Line")
        
    except Exception as e:
        logger.print_error(f"Error adding Wave indicator: {e}")


def _add_generic_indicator_to_subplot(chunk: pd.DataFrame, x_values: list, indicator_name: str) -> None:
    """Add generic indicator to subplot by looking for columns with indicator name."""
    try:
        # Look for columns containing the indicator name
        indicator_columns = [col for col in chunk.columns if indicator_name.upper() in col.upper()]
        
        if not indicator_columns:
            # Try exact match (case insensitive)
            if indicator_name.lower() in [col.lower() for col in chunk.columns]:
                indicator_columns = [col for col in chunk.columns if col.lower() == indicator_name.lower()]
            elif indicator_name in chunk.columns:
                indicator_columns = [indicator_name]
        
        if indicator_columns:
            for col in indicator_columns:
                values = chunk[col].fillna(0).tolist()
                # Ensure x_values are numeric for plotext compatibility
                numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
                plt.plot(numeric_x_values, values, label=col)
        else:
            logger.print_warning(f"No columns found for indicator: {indicator_name}")
        
    except Exception as e:
        logger.print_error(f"Error adding generic indicator {indicator_name}: {e}")


def _has_trading_signals(chunk: pd.DataFrame) -> bool:
    """Check if chunk has any trading signals."""
    return any(col in chunk.columns for col in ['Direction', '_Signal'])


def _add_trading_signals_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add trading signals to the chunk plot.
    BUY: large yellow triangle below Low
    SELL: large magenta triangle above High
    
    Supports signal sources (same as other modes):
    - _Signal column (wave indicator - only direction changes)
    - Direction column (standard indicator)
    """
    try:
        # Check for different signal sources (same priority as other modes)
        signal_source = None
        if '_Signal' in chunk.columns:
            signal_source = '_Signal'
        elif 'Direction' in chunk.columns:
            signal_source = 'Direction'
        else:
            return
        
        # Get buy/sell signals
        buy_x, buy_y, sell_x, sell_y = [], [], [], []
        
        for i, signal in enumerate(chunk[signal_source]):
            # Handle different signal formats
            if signal_source == '_Signal':
                # Wave indicator signal: 1 = BUY, 2 = SELL, 0 = NO TRADE (only direction changes)
                if signal == 1:  # BUY
                    buy_x.append(x_values[i])
                    if 'Low' in chunk.columns:
                        buy_y.append(chunk['Low'].iloc[i] * 0.99)
                    else:
                        buy_y.append(chunk['Close'].iloc[i] * 0.99 if 'Close' in chunk.columns else 0)
                elif signal == 2:  # SELL
                    sell_x.append(x_values[i])
                    if 'High' in chunk.columns:
                        sell_y.append(chunk['High'].iloc[i] * 1.01)
                    else:
                        sell_y.append(chunk['Close'].iloc[i] * 1.01 if 'Close' in chunk.columns else 0)
            else:
                # Standard Direction column
                if signal == BUY:
                    buy_x.append(x_values[i])
                    if 'Low' in chunk.columns:
                        buy_y.append(chunk['Low'].iloc[i] * 0.99)
                    else:
                        buy_y.append(chunk['Close'].iloc[i] * 0.99 if 'Close' in chunk.columns else 0)
                elif signal == SELL:
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
        if _has_trading_signals(chunk):
            buy_count = (chunk['Direction'] == BUY).sum()
            sell_count = (chunk['Direction'] == SELL).sum()
            notrade_count = (chunk['Direction'] == NOTRADE).sum()
            
            print(f"TRADING SIGNALS:")
            print(f"   BUY:     {buy_count}")
            print(f"   SELL:    {sell_count}")
            print(f"   NO TRADE: {notrade_count}")
        
        # RSI statistics
        rsi_col = None
        if 'rsi' in chunk.columns:
            rsi_col = 'rsi'
        elif 'RSI' in chunk.columns:
            rsi_col = 'RSI'
            
        if rsi_col:
            rsi = chunk[rsi_col].dropna()
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
        elif rule_upper in ['STOCHASTIC', 'CCI', 'BOLLINGER_BANDS', 'EMA', 'SMA', 'ADX', 'SAR', 
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