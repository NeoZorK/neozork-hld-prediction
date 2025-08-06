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
            # Use navigation system
            navigator = TerminalNavigator(chunks, title)
            
            def plot_chunk_with_navigation(chunk: pd.DataFrame, chunk_index: int, chunk_info: dict) -> None:
                """Plot a single chunk with navigation info."""
                if len(chunk) == 0:
                    logger.print_warning("Empty chunk, skipping...")
                    return
                
                # Get start and end dates for this chunk
                start_date = chunk_info['start_date']
                end_date = chunk_info['end_date']
                
                logger.print_info(f"Displaying chunk {chunk_info['index']}/{chunk_info['total']} ({start_date} to {end_date})")
                
                # Always show OHLC candles if possible
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
                
                # Then show each field separately
                for field in field_columns:
                    if field in chunk.columns:
                        _plot_single_field_chunk(chunk, field, f"{title} - {field} (Chunk {chunk_info['index']})", style)
            
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
    """
    try:
        logger.print_info("Generating SR chunked plots with support/resistance lines...")
        
        # Calculate optimal chunk size
        total_rows = len(df)
        chunk_size = calculate_optimal_chunk_size(total_rows)
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"Split {total_rows} rows into {len(chunks)} chunks of ~{chunk_size} candles each")
        
        # Plot each chunk
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


def _plot_single_field_chunk(chunk: pd.DataFrame, field: str, title: str, style: str) -> None:
    """
    Plot a single field in a chunk.
    
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
                plt.plot(x_values, values, color="green+", label=field)
            
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