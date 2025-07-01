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

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    # Fallback to relative imports when run as module
    from ..common import logger
    from ..common.constants import TradingRule, BUY, SELL, NOTRADE


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
        plt.candlestick(x_values, ohlc_data)
    else:
        logger.print_error("DataFrame must contain OHLC columns (Open, High, Low, Close) for candlestick plot!")


def plot_ohlcv_chunks(df: pd.DataFrame, title: str = "OHLC Chunks", style: str = "matrix") -> None:
    """
    Plot OHLC data in chunks (no volume charts).
    
    Args:
        df (pd.DataFrame): DataFrame with OHLC data
        title (str): Base title for plots
        style (str): Plot style
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
        
        # Plot each chunk
        for i, chunk in enumerate(chunks):
            chunk_start_idx = i * chunk_size
            chunk_end_idx = min((i + 1) * chunk_size, total_rows)
            
            # Clear previous plots
            plt.clear_data()
            plt.clear_figure()
            
            # Set up layout with full screen size - NO VOLUME CHARTS
            plt.subplots(1, 1)  # Single price panel only
            plot_size = (200, 50)
            
            plt.plot_size(*plot_size)
            plt.theme(style)
            
            # Create time axis with dates for this chunk
            if hasattr(chunk.index, 'strftime'):
                # If index is datetime, use date strings
                x_labels = [d.strftime('%Y-%m-%d %H:%M') for d in chunk.index]
                x_values = list(range(len(chunk)))
            else:
                # Fallback to numeric indices
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


def plot_auto_chunks(df: pd.DataFrame, title: str = "AUTO Chunks", style: str = "matrix") -> None:
    """
    Plot all fields in chunks with separate charts for each field.
    
    Args:
        df (pd.DataFrame): DataFrame with all fields
        title (str): Base title for plots
        style (str): Plot style
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
        
        # Plot each chunk
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
                    x_labels = [d.strftime('%Y-%m-%d %H:%M') for d in chunk.index]
                    x_values = list(range(len(chunk)))
                else:
                    x_values = list(range(len(chunk)))
                    x_labels = [str(i) for i in x_values]
                plt.clear_data()
                plt.clear_figure()
                plt.subplots(1, 1)
                plt.plot_size(200, 50)
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


def plot_pv_chunks(df: pd.DataFrame, title: str = "PV Chunks", style: str = "matrix") -> None:
    """
    Plot PV (Pressure Vector) data in chunks with buy/sell signals.
    
    Args:
        df (pd.DataFrame): DataFrame with PV data
        title (str): Base title for plots
        style (str): Plot style
    """
    try:
        logger.print_info("Generating PV chunked plots with buy/sell signals...")
        
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
            plt.clear_data()
            plt.clear_figure()
            
            # Get start and end dates for this chunk
            start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
            end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
            
            # Set up plot with full screen size
            plt.subplots(1, 1)
            plt.plot_size(200, 50)  # Much larger plot size
            plt.theme(style)
            
            # Create time axis with dates for this chunk
            if hasattr(chunk.index, 'strftime'):
                # If index is datetime, use date strings
                x_labels = [d.strftime('%Y-%m-%d %H:%M') for d in chunk.index]
                x_values = list(range(len(chunk)))
            else:
                # Fallback to numeric indices
                x_values = list(range(len(chunk)))
                x_labels = [str(i) for i in x_values]
            
            # OHLC Candlestick Chart
            draw_ohlc_candles(chunk, x_values)
            
            # Add PV-specific overlays
            _add_pv_overlays_to_chunk(chunk, x_values)
            
            plt.title(f"{title} - PV with Signals (Chunk {i+1}/{len(chunks)}) - {start_date} to {end_date}")
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
        
        logger.print_success(f"Successfully displayed {len(chunks)} PV chunks!")
        
    except Exception as e:
        logger.print_error(f"Error generating PV chunked plots: {e}")


def plot_sr_chunks(df: pd.DataFrame, title: str = "SR Chunks", style: str = "matrix") -> None:
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
            plt.clear_data()
            plt.clear_figure()
            
            # Get start and end dates for this chunk
            start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
            end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
            
            # Set up plot with full screen size
            plt.subplots(1, 1)
            plt.plot_size(200, 50)  # Much larger plot size
            plt.theme(style)
            
            # Create time axis with dates for this chunk
            if hasattr(chunk.index, 'strftime'):
                # If index is datetime, use date strings
                x_labels = [d.strftime('%Y-%m-%d %H:%M') for d in chunk.index]
                x_values = list(range(len(chunk)))
            else:
                # Fallback to numeric indices
                x_values = list(range(len(chunk)))
                x_labels = [str(i) for i in x_values]
            
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


def plot_phld_chunks(df: pd.DataFrame, title: str = "PHLD Chunks", style: str = "matrix") -> None:
    """
    Plot PHLD (Predict High Low Direction) data in chunks with two channels and signals.
    
    Args:
        df (pd.DataFrame): DataFrame with PHLD data
        title (str): Base title for plots
        style (str): Plot style
    """
    try:
        logger.print_info("Generating PHLD chunked plots with channels and signals...")
        
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
            plt.clear_data()
            plt.clear_figure()
            
            # Get start and end dates for this chunk
            start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
            end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
            
            # Set up plot with full screen size
            plt.subplots(1, 1)
            plt.plot_size(200, 50)  # Much larger plot size
            plt.theme(style)
            
            # Create time axis with dates for this chunk
            if hasattr(chunk.index, 'strftime'):
                # If index is datetime, use date strings
                x_labels = [d.strftime('%Y-%m-%d %H:%M') for d in chunk.index]
                x_values = list(range(len(chunk)))
            else:
                # Fallback to numeric indices
                x_values = list(range(len(chunk)))
                x_labels = [str(i) for i in x_values]
            
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


def plot_rsi_chunks(df: pd.DataFrame, rule: str, title: str = "RSI Chunks", style: str = "matrix") -> None:
    """
    Plot RSI data in chunks with different calculations based on rule type.
    
    Args:
        df (pd.DataFrame): DataFrame with RSI data
        rule (str): RSI rule type (rsi, rsi_mom, rsi_div)
        title (str): Base title for plots
        style (str): Plot style
    """
    try:
        rule_type, params = parse_rsi_rule(rule)
        logger.print_info(f"Generating {rule_type.upper()} chunked plots...")
        
        # Calculate optimal chunk size
        total_rows = len(df)
        chunk_size = calculate_optimal_chunk_size(total_rows)
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"Split {total_rows} rows into {len(chunks)} chunks of ~{chunk_size} candles each")
        
        # Plot each chunk
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
            plt.plot_size(200, 50)  # Much larger plot size
            plt.theme(style)
            
            # Create time axis with dates for this chunk
            if hasattr(chunk.index, 'strftime'):
                # If index is datetime, use date strings
                x_labels = [d.strftime('%Y-%m-%d %H:%M') for d in chunk.index]
                x_values = list(range(len(chunk)))
            else:
                # Fallback to numeric indices
                x_values = list(range(len(chunk)))
                x_labels = [str(i) for i in x_values]
            
            # OHLC Candlestick Chart
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
        plt.clear_data()
        plt.clear_figure()
        
        # Set up plot with full screen size
        plt.subplots(1, 1)
        plt.plot_size(200, 50)  # Much larger plot size
        plt.theme(style)
        
        # Create time axis with dates
        if hasattr(chunk.index, 'strftime'):
            # If index is datetime, use date strings
            x_labels = [d.strftime('%Y-%m-%d %H:%M') for d in chunk.index]
            x_values = list(range(len(chunk)))
        else:
            # Fallback to numeric indices
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
                plt.plot(x_values, values, color="green+", label=field, marker="o")
            
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
    Add PV-specific overlays to the chunk plot.
    
    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (list): X-axis values
    """
    try:
        # Add support and resistance lines
        if 'PPrice1' in chunk.columns:  # Support level
            pprice1_values = chunk['PPrice1'].fillna(0).tolist()
            plt.plot(x_values, pprice1_values, color="green+", label="Support", marker="D")
        
        if 'PPrice2' in chunk.columns:  # Resistance level
            pprice2_values = chunk['PPrice2'].fillna(0).tolist()
            plt.plot(x_values, pprice2_values, color="red+", label="Resistance", marker="D")
        
        # Add trading signals
        if 'Direction' in chunk.columns:
            _add_trading_signals_to_chunk(chunk, x_values)
        
        # Add PV indicator
        if 'PV' in chunk.columns:
            pv_values = chunk['PV'].fillna(0).tolist()
            plt.plot(x_values, pv_values, color="blue+", label="Pressure Vector", marker="o")
        
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
            plt.plot(x_values, pprice1_values, color="green+", label="Support", marker="D")
        
        if 'PPrice2' in chunk.columns:  # Resistance level
            pprice2_values = chunk['PPrice2'].fillna(0).tolist()
            plt.plot(x_values, pprice2_values, color="red+", label="Resistance", marker="D")
        
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
            plt.plot(x_values, pprice1_values, color="green+", label="Support Channel", marker="D")
        
        if 'PPrice2' in chunk.columns:  # Resistance level
            pprice2_values = chunk['PPrice2'].fillna(0).tolist()
            plt.plot(x_values, pprice2_values, color="red+", label="Resistance Channel", marker="D")
        
        # Add trading signals
        if 'Direction' in chunk.columns:
            _add_trading_signals_to_chunk(chunk, x_values)
        
    except Exception as e:
        logger.print_error(f"Error adding PHLD overlays: {e}")


def _add_rsi_overlays_to_chunk(chunk: pd.DataFrame, x_values: list, rule_type: str, params: Dict[str, Any]) -> None:
    """
    Add RSI-specific overlays to the chunk plot based on rule type.
    """
    try:
        # Add support and resistance lines with yellow and blue colors
        if 'PPrice1' in chunk.columns:  # Support level
            pprice1_values = chunk['PPrice1'].fillna(0).tolist()
            plt.plot(x_values, pprice1_values, color="yellow+", label="Support", marker="D")
        
        if 'PPrice2' in chunk.columns:  # Resistance level
            pprice2_values = chunk['PPrice2'].fillna(0).tolist()
            plt.plot(x_values, pprice2_values, color="blue+", label="Resistance", marker="D")
        
        # Add RSI as line plot (без маркеров, только линия)
        if 'RSI' in chunk.columns:
            rsi_values = chunk['RSI'].fillna(50).tolist()
            plt.plot(x_values, rsi_values, color="cyan+", label=f"RSI ({rule_type})")
        
        # Add RSI momentum for momentum variant
        if rule_type == 'rsi_mom' and 'RSI_Momentum' in chunk.columns:
            momentum_values = chunk['RSI_Momentum'].fillna(0).tolist()
            plt.plot(x_values, momentum_values, color="magenta+", label="RSI Momentum", marker="d")
        
        # Add divergence strength for divergence variant
        if rule_type == 'rsi_div' and 'Diff' in chunk.columns:
            diff_values = chunk['Diff'].fillna(0).tolist()
            plt.plot(x_values, diff_values, color="cyan+", label="Divergence Strength", marker="d")
        
        # Add trading signals with red/aqua colors
        if 'Direction' in chunk.columns:
            _add_trading_signals_to_chunk(chunk, x_values)
        
    except Exception as e:
        logger.print_error(f"Error adding RSI overlays: {e}")


def _add_trading_signals_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add trading signals to the chunk plot.
    
    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (list): X-axis values
    """
    try:
        if 'Direction' not in chunk.columns:
            return
        
        # Get buy and sell signals
        buy_signals = []
        sell_signals = []
        
        for i, direction in enumerate(chunk['Direction']):
            if direction == BUY:
                buy_signals.append((x_values[i], chunk['Close'].iloc[i] if 'Close' in chunk.columns else 0))
            elif direction == SELL:
                sell_signals.append((x_values[i], chunk['Close'].iloc[i] if 'Close' in chunk.columns else 0))
        
        # Plot buy signals
        if buy_signals:
            buy_x, buy_y = zip(*buy_signals)
            plt.scatter(buy_x, buy_y, color="aqua+", label="BUY", marker="^")
        
        # Plot sell signals
        if sell_signals:
            sell_x, sell_y = zip(*sell_signals)
            plt.scatter(sell_x, sell_y, color="red+", label="SELL", marker="v")
        
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


def plot_chunked_terminal(df: pd.DataFrame, rule: str, title: str = "Chunked Terminal Plot", style: str = "matrix") -> None:
    """
    Main function to plot data in chunks based on the rule.
    
    Args:
        df (pd.DataFrame): DataFrame with data
        rule (str): Trading rule
        title (str): Plot title
        style (str): Plot style
    """
    try:
        rule_upper = rule.upper()
        
        # Handle RSI variants
        if rule_upper.startswith('RSI'):
            if '(' in rule:  # Parameterized RSI rule
                plot_rsi_chunks(df, rule, title, style)
            else:  # Simple RSI rule
                plot_rsi_chunks(df, 'rsi(14,70,30,close)', title, style)
        elif rule_upper == 'OHLCV':
            plot_ohlcv_chunks(df, title, style)
        elif rule_upper == 'AUTO':
            plot_auto_chunks(df, title, style)
        elif rule_upper in ['PV', 'PRESSURE_VECTOR']:
            plot_pv_chunks(df, title, style)
        elif rule_upper in ['SR', 'SUPPORT_RESISTANTS']:
            plot_sr_chunks(df, title, style)
        elif rule_upper in ['PHLD', 'PREDICT_HIGH_LOW_DIRECTION']:
            plot_phld_chunks(df, title, style)
        else:
            # Default to OHLCV for unknown rules
            logger.print_warning(f"Unknown rule '{rule}', defaulting to OHLCV")
            plot_ohlcv_chunks(df, title, style)
        
    except Exception as e:
        logger.print_error(f"Error in chunked terminal plotting: {e}") 