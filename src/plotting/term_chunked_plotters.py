# -*- coding: utf-8 -*-
# src/plotting/term_chunked_plotters.py

"""
Plotter functions for terminal chunked plotting.
Contains main plotting functions for different chart types.
"""

import pandas as pd
import numpy as np
import plotext as plt
from typing import Optional, List, Tuple, Dict, Any

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

# Import utilities
try:
    from .term_chunked_utils import (
        calculate_optimal_chunk_size, split_dataframe_into_chunks, parse_rsi_rule,
        draw_ohlc_candles, create_time_axis, setup_plot_layout, clear_plot
    )
    from .term_chunked_overlays import (
        _add_pv_overlays_to_chunk, _add_sr_overlays_to_chunk,
        _add_phld_overlays_to_chunk, _add_rsi_overlays_to_chunk
    )
    from .term_chunked_statistics import _show_chunk_statistics, _show_field_statistics
except ImportError:
    # Fallback to relative imports when run as module
    from ..plotting.term_chunked_utils import (
        calculate_optimal_chunk_size, split_dataframe_into_chunks, parse_rsi_rule,
        draw_ohlc_candles, create_time_axis, setup_plot_layout, clear_plot
    )
    from ..plotting.term_chunked_overlays import (
        _add_pv_overlays_to_chunk, _add_sr_overlays_to_chunk,
        _add_phld_overlays_to_chunk, _add_rsi_overlays_to_chunk
    )
    from ..plotting.term_chunked_statistics import _show_chunk_statistics, _show_field_statistics


def _get_field_color(field: str, field_index: int = None) -> str:
    """
    Get unique color for a field based on field name or index.
    
    Args:
        field (str): Field name
        field_index (int, optional): Field index for fallback
        
    Returns:
        str: Color string for plotext
    """
    # Define a comprehensive color palette for different field types
    color_palette = [
        "green+", "red+", "blue+", "yellow+", "magenta+", "cyan+", "white+",
        "green", "red", "blue", "yellow", "magenta", "cyan", "white",
        "bright green", "bright red", "bright blue", "bright yellow", 
        "bright magenta", "bright cyan", "bright white"
    ]
    
    # Field-specific color mapping for common indicators
    field_colors = {
        # Pressure indicators
        'pressure_high': 'red+',
        'pressure_low': 'blue+', 
        'pressure_vector': 'magenta+',
        'pressure': 'cyan+',
        
        # Predicted values
        'predicted_high': 'bright red',
        'predicted_low': 'bright blue',
        'predicted_close': 'bright green',
        'predicted': 'yellow+',
        
        # Support/Resistance
        'support': 'green+',
        'resistance': 'red+',
        'support_level': 'green',
        'resistance_level': 'red',
        
        # RSI variants
        'rsi': 'cyan+',
        'rsi_signal': 'yellow+',
        'rsi_momentum': 'magenta+',
        'rsi_divergence': 'bright cyan',
        
        # Volume indicators
        'volume': 'white+',
        'obv': 'bright white',
        'vwap': 'bright yellow',
        
        # MACD
        'macd': 'blue+',
        'macd_signal': 'red+',
        'macd_histogram': 'yellow+',
        
        # Moving averages
        'sma': 'green+',
        'ema': 'blue+',
        'ma': 'cyan+',
        
        # Bollinger Bands
        'bb_upper': 'red+',
        'bb_lower': 'blue+',
        'bb_middle': 'yellow+',
        
        # Stochastic
        'stoch_k': 'blue+',
        'stoch_d': 'red+',
        
        # ATR
        'atr': 'magenta+',
        
        # ADX
        'adx': 'cyan+',
        'di_plus': 'green+',
        'di_minus': 'red+',
        
        # Williams %R
        'williams_r': 'yellow+',
        
        # CCI
        'cci': 'magenta+',
        
        # Momentum
        'momentum': 'bright green',
        'roc': 'bright blue',
        
        # Volatility
        'volatility': 'bright red',
        'volatility_ratio': 'bright magenta',
        
        # Sentiment
        'sentiment': 'bright cyan',
        'fear_greed': 'bright yellow',
        
        # Custom indicators
        'custom': 'white+',
        'signal': 'bright white',
        'trend': 'bright green',
        'strength': 'bright blue'
    }
    
    # Try to get color by exact field name match first
    field_lower = field.lower()
    if field_lower in field_colors:
        return field_colors[field_lower]
    
    # Try to get color by partial field name match (more specific matches first)
    # Sort keys by length (longer keys first) to prioritize more specific matches
    sorted_keys = sorted(field_colors.keys(), key=len, reverse=True)
    for key in sorted_keys:
        if key in field_lower:
            return field_colors[key]
    
    # Fallback to index-based color if provided
    if field_index is not None and field_index < len(color_palette):
        return color_palette[field_index]
    
    # Final fallback to first color
    return color_palette[0]


def _get_field_color_by_index(field: str, field_index: int) -> str:
    """
    Get color for field based on its index in the field list.
    
    Args:
        field (str): Field name
        field_index (int): Index of field in the field list
        
    Returns:
        str: Color string for plotext
    """
    # First try to get color by field name
    color = _get_field_color(field)
    
    # If the color is the default (first color), use index-based color instead
    if color == "green+":
        color_palette = [
            "green+", "red+", "blue+", "yellow+", "magenta+", "cyan+", "white+",
            "green", "red", "blue", "yellow", "magenta", "cyan", "white",
            "bright green", "bright red", "bright blue", "bright yellow", 
            "bright magenta", "bright cyan", "bright white"
        ]
        if field_index < len(color_palette):
            return color_palette[field_index]
    
    return color


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
                clear_plot()
                
                # Set up layout with full screen size - NO VOLUME CHARTS
                setup_plot_layout(style)
                
                # Create time axis with dates for this chunk
                x_values, x_labels = create_time_axis(chunk)
                
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
                clear_plot()
                
                # Set up layout with full screen size - NO VOLUME CHARTS
                setup_plot_layout(style)
                
                # Create time axis with dates for this chunk
                x_values, x_labels = create_time_axis(chunk)
                
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
                        x_values, x_labels = create_time_axis(chunk)
                        clear_plot()
                        setup_plot_layout(style)
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
                    # Get field index from the field_columns list for proper color assignment
                    field_index = field_columns.index(current_field) if current_field in field_columns else None
                    _plot_single_field_chunk(chunk, current_field, f"{title} - {current_field} (Chunk {chunk_info['index']})", style, field_index)
            
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
                    x_values, x_labels = create_time_axis(chunk)
                    clear_plot()
                    setup_plot_layout(style)
                    draw_ohlc_candles(chunk, x_values)
                    plt.title(f"{title} - OHLC (Chunk {i+1}) - {start_date} to {end_date}")
                    plt.xlabel("Date/Time")
                    if len(x_values) > 0:
                        step = max(1, len(x_values) // 10)
                        plt.xticks(x_values[::step], x_labels[::step])
                    plt.ylabel("Price")
                    plt.show()
                
                # Then show each field separately
                for field_idx, field in enumerate(field_columns):
                    if field in chunk.columns:
                        _plot_single_field_chunk(chunk, field, f"{title} - {field} (Chunk {i+1})", style, field_idx)
                
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
                clear_plot()
                
                # Get start and end dates for this chunk
                start_date = chunk_info['start_date']
                end_date = chunk_info['end_date']
                
                # Set up plot with full screen size
                setup_plot_layout(style)
                
                # Create time axis with dates for this chunk
                x_values, x_labels = create_time_axis(chunk)
                
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
                clear_plot()
                
                # Get start and end dates for this chunk
                start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
                end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
                
                # Set up plot with full screen size
                setup_plot_layout(style)
                
                # Create time axis with dates for this chunk
                x_values, x_labels = create_time_axis(chunk)
                
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
                clear_plot()
                
                # Get start and end dates for this chunk
                start_date = chunk_info['start_date']
                end_date = chunk_info['end_date']
                
                # Set up plot with full screen size
                setup_plot_layout(style)
                
                # Create time axis with dates for this chunk
                x_values, x_labels = create_time_axis(chunk)
                
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
                clear_plot()
                
                # Get start and end dates for this chunk
                start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
                end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
                
                # Set up plot with full screen size
                setup_plot_layout(style)
                
                # Create time axis with dates for this chunk
                x_values, x_labels = create_time_axis(chunk)
                
                # OHLC Candlestick Chart
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
                clear_plot()
                
                # Get start and end dates for this chunk
                start_date = chunk_info['start_date']
                end_date = chunk_info['end_date']
                
                # Set up plot with full screen size
                setup_plot_layout(style)
                
                # Create time axis with dates for this chunk
                x_values, x_labels = create_time_axis(chunk)
                
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
                clear_plot()
                
                # Get start and end dates for this chunk
                start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
                end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
                
                # Set up plot with full screen size
                setup_plot_layout(style)
                
                # Create time axis with dates for this chunk
                x_values, x_labels = create_time_axis(chunk)
                
                # OHLC Candlestick Chart
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
                clear_plot()
                
                # Get start and end dates for this chunk
                start_date = chunk_info['start_date']
                end_date = chunk_info['end_date']
                
                # Set up plot with full screen size
                setup_plot_layout(style)
                
                # Create time axis with dates for this chunk
                x_values, x_labels = create_time_axis(chunk)
                
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
                clear_plot()
                
                # Set up plot with full screen size
                setup_plot_layout(style)
                
                # Create time axis with dates for this chunk
                x_values, x_labels = create_time_axis(chunk)
                
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


def _plot_single_field_chunk(chunk: pd.DataFrame, field: str, title: str, style: str, field_index: int = None) -> None:
    """
    Plot a single field in a chunk.
    
    Args:
        chunk (pd.DataFrame): DataFrame chunk
        field (str): Field name to plot
        title (str): Plot title
        style (str): Plot style
        field_index (int, optional): Index of field in the field list for color assignment
    """
    try:
        # Get start and end dates for this chunk
        start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
        end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
        
        # Clear previous plots
        clear_plot()
        
        # Set up plot with full screen size
        setup_plot_layout(style)
        
        # Create time axis with dates
        x_values, x_labels = create_time_axis(chunk)
        
        # Get field data
        if field in chunk.columns:
            # Handle NaN values properly
            field_data = chunk[field].copy()
            # Replace NaN with None for plotext compatibility
            field_data = field_data.replace([np.inf, -np.inf], np.nan)
            values = field_data.where(pd.notna(field_data), None).tolist()
            
            # Only plot if we have valid data
            if any(v is not None for v in values):
                # Use provided field_index or fallback to column position
                color_index = field_index if field_index is not None else chunk.columns.get_loc(field)
                plt.plot(x_values, values, color=_get_field_color_by_index(field, color_index), label=field)
            
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


def create_navigation_template(rule_name: str, plot_function: callable, overlay_function: callable = None) -> callable:
    """
    Create a navigation-enabled plotting function for new rules.
    
    Args:
        rule_name (str): Name of the rule (e.g., "MACD", "Bollinger")
        plot_function (callable): Function to create the plot
        overlay_function (callable, optional): Function to add overlays
        
    Returns:
        callable: Navigation-enabled plotting function
    """
    def plot_rule_chunks(df: pd.DataFrame, title: str = f"{rule_name} Chunks", style: str = "matrix", use_navigation: bool = False) -> None:
        """
        Plot {rule_name} data in chunks with navigation support.
        
        Args:
            df (pd.DataFrame): DataFrame with {rule_name} data
            title (str): Base title for plots
            style (str): Plot style
            use_navigation (bool): Whether to use interactive navigation
        """
        try:
            logger.print_info(f"Generating {rule_name} chunked plots...")
            
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
                    clear_plot()
                    
                    # Get start and end dates for this chunk
                    start_date = chunk_info['start_date']
                    end_date = chunk_info['end_date']
                    
                    # Set up plot with full screen size
                    setup_plot_layout(style)
                    
                    # Create time axis with dates for this chunk
                    x_values, x_labels = create_time_axis(chunk)
                    
                    # OHLC Candlestick Chart (always as first layer, like in other rules)
                    draw_ohlc_candles(chunk, x_values)
                    
                    # Add rule-specific overlays if provided
                    if overlay_function:
                        overlay_function(chunk, x_values)
                    
                    plt.title(f"{title} - {rule_name} (Chunk {chunk_info['index']}/{chunk_info['total']}) - {start_date} to {end_date}")
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
                    clear_plot()
                    
                    # Get start and end dates for this chunk
                    start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
                    end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
                    
                    # Set up plot with full screen size
                    setup_plot_layout(style)
                    
                    # Create time axis with dates for this chunk
                    x_values, x_labels = create_time_axis(chunk)
                    
                    # OHLC Candlestick Chart
                    draw_ohlc_candles(chunk, x_values)
                    
                    # Add rule-specific overlays if provided
                    if overlay_function:
                        overlay_function(chunk, x_values)
                    
                    plt.title(f"{title} - {rule_name} (Chunk {i+1}/{len(chunks)}) - {start_date} to {end_date}")
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
            
            logger.print_success(f"Successfully displayed {len(chunks)} {rule_name} chunks!")
            
        except Exception as e:
            logger.print_error(f"Error generating {rule_name} chunked plots: {e}")
    
    return plot_rule_chunks


# Example usage for future rules:
# def _add_macd_overlays_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
#     """Add MACD-specific overlays to chunk."""
#     # MACD overlay implementation
#     pass
# 
# plot_macd_chunks = create_navigation_template("MACD", None, _add_macd_overlays_to_chunk) 