# -*- coding: utf-8 -*-
# src/plotting/term_chunked/core/plot_functions.py

"""
Core plotting functions for terminal chunked plotting.
"""

import pandas as pd
import numpy as np
import plotext as plt
from typing import Optional, List, Tuple, Dict, Any

# Import navigation system
try:
    from ...term_navigation import TerminalNavigator, create_navigation_prompt, parse_navigation_input
except ImportError:
    try:
        # Fallback to relative imports when run as module
        from src.plotting.term_navigation import TerminalNavigator, create_navigation_prompt, parse_navigation_input
    except ImportError:
        # Final fallback for pytest with -n auto
        from src.plotting.term_navigation import TerminalNavigator, create_navigation_prompt, parse_navigation_input

from ..utils.plot_utils import (
    get_terminal_plot_size, calculate_optimal_chunk_size, split_dataframe_into_chunks,
    parse_rsi_rule, draw_ohlc_candles, _get_field_color_enhanced, _plot_single_field_chunk,
    _has_trading_signals, _show_chunk_statistics
)

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


def plot_ohlcv_chunks(df: pd.DataFrame, title: str = "OHLC Chunks", 
                      style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot OHLCV data in chunks with navigation.
    
    Args:
        df: DataFrame with OHLCV data
        title: Plot title
        style: Plot style
        use_navigation: Whether to use navigation
    """
    try:
        # Calculate optimal chunk size
        chunk_size = calculate_optimal_chunk_size(len(df))
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"📊 Plotting {len(chunks)} chunks of OHLCV data (chunk size: {chunk_size})")
        
        if use_navigation:
            navigator = TerminalNavigator(chunks, title)
            navigator.navigate()
        else:
            # Simple chunk display
            for i, chunk in enumerate(chunks):
                start_idx = i * chunk_size
                end_idx = min(start_idx + chunk_size - 1, len(df) - 1)
                
                print(f"\n📊 {title} - Chunk {i+1}/{len(chunks)}")
                print(f"📈 Range: {start_idx} - {end_idx}")
                
                # Draw OHLC candles
                x_values = list(range(len(chunk)))
                draw_ohlc_candles(chunk, x_values)
                
                # Show statistics
                _show_chunk_statistics(chunk, f"{title} Chunk {i+1}", start_idx, end_idx)
                
                # Wait for user input
                input("\n⏸️  Press Enter to continue to next chunk...")
        
    except Exception as e:
        logger.print_error(f"Error plotting OHLCV chunks: {e}")


def plot_auto_chunks(df: pd.DataFrame, title: str = "AUTO Chunks", 
                     style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot AUTO rule data in chunks with navigation.
    
    Args:
        df: DataFrame with AUTO rule data
        title: Plot title
        style: Plot style
        use_navigation: Whether to use navigation
    """
    try:
        # Calculate optimal chunk size
        chunk_size = calculate_optimal_chunk_size(len(df))
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"📊 Plotting {len(chunks)} chunks of AUTO data (chunk size: {chunk_size})")
        
        if use_navigation:
            navigator = TerminalNavigator(chunks, title)
            navigator.navigate()
        else:
            # Simple chunk display
            for i, chunk in enumerate(chunks):
                start_idx = i * chunk_size
                end_idx = min(start_idx + chunk_size - 1, len(df) - 1)
                
                print(f"\n📊 {title} - Chunk {i+1}/{len(chunks)}")
                print(f"📈 Range: {start_idx} - {end_idx}")
                
                # Plot OHLC data
                x_values = list(range(len(chunk)))
                draw_ohlc_candles(chunk, x_values)
                
                # Show statistics
                _show_chunk_statistics(chunk, f"{title} Chunk {i+1}", start_idx, end_idx)
                
                # Wait for user input
                input("\n⏸️  Press Enter to continue to next chunk...")
        
    except Exception as e:
        logger.print_error(f"Error plotting AUTO chunks: {e}")


def plot_pv_chunks(df: pd.DataFrame, title: str = "PV Chunks", 
                   style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot Pressure Vector data in chunks with navigation.
    
    Args:
        df: DataFrame with Pressure Vector data
        title: Plot title
        style: Plot style
        use_navigation: Whether to use navigation
    """
    try:
        # Calculate optimal chunk size
        chunk_size = calculate_optimal_chunk_size(len(df))
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"📊 Plotting {len(chunks)} chunks of PV data (chunk size: {chunk_size})")
        
        if use_navigation:
            navigator = TerminalNavigator(chunks, title)
            navigator.navigate()
        else:
            # Simple chunk display
            for i, chunk in enumerate(chunks):
                start_idx = i * chunk_size
                end_idx = min(start_idx + chunk_size - 1, len(df) - 1)
                
                print(f"\n📊 {title} - Chunk {i+1}/{len(chunks)}")
                print(f"📈 Range: {start_idx} - {end_idx}")
                
                # Plot OHLC data with PV overlay
                x_values = list(range(len(chunk)))
                draw_ohlc_candles(chunk, x_values)
                
                # Add PV overlay if available
                if 'pressure_vector' in chunk.columns:
                    _add_pv_overlays_to_chunk(chunk, x_values)
                
                # Show statistics
                _show_chunk_statistics(chunk, f"{title} Chunk {i+1}", start_idx, end_idx)
                
                # Wait for user input
                input("\n⏸️  Press Enter to continue to next chunk...")
        
    except Exception as e:
        logger.print_error(f"Error plotting PV chunks: {e}")


def plot_sr_chunks(df: pd.DataFrame, title: str = "SR Chunks", 
                   style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot Support/Resistance data in chunks with navigation.
    
    Args:
        df: DataFrame with Support/Resistance data
        title: Plot title
        style: Plot style
        use_navigation: Whether to use navigation
    """
    try:
        # Calculate optimal chunk size
        chunk_size = calculate_optimal_chunk_size(len(df))
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"📊 Plotting {len(chunks)} chunks of SR data (chunk size: {chunk_size})")
        
        if use_navigation:
            navigator = TerminalNavigator(chunks, title)
            navigator.navigate()
        else:
            # Simple chunk display
            for i, chunk in enumerate(chunks):
                start_idx = i * chunk_size
                end_idx = min(start_idx + chunk_size - 1, len(df) - 1)
                
                print(f"\n📊 {title} - Chunk {i+1}/{len(chunks)}")
                print(f"📈 Range: {start_idx} - {end_idx}")
                
                # Plot OHLC data with SR overlay
                x_values = list(range(len(chunk)))
                draw_ohlc_candles(chunk, x_values)
                
                # Add SR overlay if available
                if 'support' in chunk.columns or 'resistance' in chunk.columns:
                    _add_sr_overlays_to_chunk(chunk, x_values)
                
                # Show statistics
                _show_chunk_statistics(chunk, f"{title} Chunk {i+1}", start_idx, end_idx)
                
                # Wait for user input
                input("\n⏸️  Press Enter to continue to next chunk...")
        
    except Exception as e:
        logger.print_error(f"Error plotting SR chunks: {e}")


def plot_phld_chunks(df: pd.DataFrame, title: str = "PHLD Chunks", 
                     style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot PHLD data in chunks with navigation.
    
    Args:
        df: DataFrame with PHLD data
        title: Plot title
        style: Plot style
        use_navigation: Whether to use navigation
    """
    try:
        # Calculate optimal chunk size
        chunk_size = calculate_optimal_chunk_size(len(df))
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"📊 Plotting {len(chunks)} chunks of PHLD data (chunk size: {chunk_size})")
        
        if use_navigation:
            navigator = TerminalNavigator(chunks, title)
            navigator.navigate()
        else:
            # Simple chunk display
            for i, chunk in enumerate(chunks):
                start_idx = i * chunk_size
                end_idx = min(start_idx + chunk_size - 1, len(df) - 1)
                
                print(f"\n📊 {title} - Chunk {i+1}/{len(chunks)}")
                print(f"📈 Range: {start_idx} - {end_idx}")
                
                # Plot OHLC data with PHLD overlay
                x_values = list(range(len(chunk)))
                draw_ohlc_candles(chunk, x_values)
                
                # Add PHLD overlay if available
                if 'phld_signal' in chunk.columns:
                    _add_phld_overlays_to_chunk(chunk, x_values)
                
                # Show statistics
                _show_chunk_statistics(chunk, f"{title} Chunk {i+1}", start_idx, end_idx)
                
                # Wait for user input
                input("\n⏸️  Press Enter to continue to next chunk...")
        
    except Exception as e:
        logger.print_error(f"Error plotting PHLD chunks: {e}")


def plot_rsi_chunks(df: pd.DataFrame, rule: str, title: str = "RSI Chunks", 
                    style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot RSI data in chunks with navigation.
    
    Args:
        df: DataFrame with RSI data
        rule: RSI rule type
        title: Plot title
        style: Plot style
        use_navigation: Whether to use navigation
    """
    try:
        # Parse RSI rule
        rule_type, params = parse_rsi_rule(rule)
        
        # Calculate optimal chunk size
        chunk_size = calculate_optimal_chunk_size(len(df))
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"📊 Plotting {len(chunks)} chunks of RSI data (chunk size: {chunk_size})")
        
        if use_navigation:
            navigator = TerminalNavigator(chunks, title)
            navigator.navigate()
        else:
            # Simple chunk display
            for i, chunk in enumerate(chunks):
                start_idx = i * chunk_size
                end_idx = min(start_idx + chunk_size - 1, len(df) - 1)
                
                print(f"\n📊 {title} - Chunk {i+1}/{len(chunks)}")
                print(f"📈 Range: {start_idx} - {end_idx}")
                
                # Plot OHLC data with RSI overlay
                x_values = list(range(len(chunk)))
                draw_ohlc_candles(chunk, x_values)
                
                # Add RSI overlay if available
                rsi_columns = ['rsi', 'rsi_mom', 'rsi_div']
                if any(col in chunk.columns for col in rsi_columns):
                    _add_rsi_overlays_to_chunk(chunk, x_values, rule_type, params)
                
                # Show statistics
                _show_chunk_statistics(chunk, f"{title} Chunk {i+1}", start_idx, end_idx)
                
                # Wait for user input
                input("\n⏸️  Press Enter to continue to next chunk...")
        
    except Exception as e:
        logger.print_error(f"Error plotting RSI chunks: {e}")


def plot_macd_chunks(df: pd.DataFrame, title: str = "MACD Chunks", 
                     style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Plot MACD data in chunks with navigation.
    
    Args:
        df: DataFrame with MACD data
        title: Plot title
        style: Plot style
        use_navigation: Whether to use navigation
    """
    try:
        # Calculate optimal chunk size
        chunk_size = calculate_optimal_chunk_size(len(df))
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"📊 Plotting {len(chunks)} chunks of MACD data (chunk size: {chunk_size})")
        
        if use_navigation:
            navigator = TerminalNavigator(chunks, title)
            navigator.navigate()
        else:
            # Simple chunk display
            for i, chunk in enumerate(chunks):
                start_idx = i * chunk_size
                end_idx = min(start_idx + chunk_size - 1, len(df) - 1)
                
                print(f"\n📊 {title} - Chunk {i+1}/{len(chunks)}")
                print(f"📈 Range: {start_idx} - {end_idx}")
                
                # Plot OHLC data with MACD overlay
                x_values = list(range(len(chunk)))
                draw_ohlc_candles(chunk, x_values)
                
                # Add MACD overlay if available
                if 'macd' in chunk.columns:
                    _add_macd_overlays_to_chunk(chunk, x_values)
                
                # Show statistics
                _show_chunk_statistics(chunk, f"{title} Chunk {i+1}", start_idx, end_idx)
                
                # Wait for user input
                input("\n⏸️  Press Enter to continue to next chunk...")
        
    except Exception as e:
        logger.print_error(f"Error plotting MACD chunks: {e}")


def plot_indicator_chunks(df: pd.DataFrame, indicator_name: str, title: str = "Indicator Chunks", 
                          style: str = "matrix", use_navigation: bool = False, rule: str = "") -> None:
    """
    Plot generic indicator data in chunks with navigation.
    
    Args:
        df: DataFrame with indicator data
        indicator_name: Name of the indicator
        title: Plot title
        style: Plot style
        use_navigation: Whether to use navigation
        rule: Trading rule
    """
    try:
        # Calculate optimal chunk size
        chunk_size = calculate_optimal_chunk_size(len(df))
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        logger.print_info(f"📊 Plotting {len(chunks)} chunks of {indicator_name} data (chunk size: {chunk_size})")
        
        if use_navigation:
            navigator = TerminalNavigator(chunks, title)
            navigator.navigate()
        else:
            # Simple chunk display
            for i, chunk in enumerate(chunks):
                start_idx = i * chunk_size
                end_idx = min(start_idx + chunk_size - 1, len(df) - 1)
                
                print(f"\n📊 {title} - Chunk {i+1}/{len(chunks)}")
                print(f"📈 Range: {start_idx} - {end_idx}")
                
                # Plot OHLC data with indicator overlay
                x_values = list(range(len(chunk)))
                draw_ohlc_candles(chunk, x_values)
                
                # Add indicator overlay if available
                if indicator_name.lower() in chunk.columns:
                    _add_indicator_chart_to_subplot(chunk, x_values, indicator_name, rule)
                
                # Show statistics
                _show_chunk_statistics(chunk, f"{title} Chunk {i+1}", start_idx, end_idx)
                
                # Wait for user input
                input("\n⏸️  Press Enter to continue to next chunk...")
        
    except Exception as e:
        logger.print_error(f"Error plotting {indicator_name} chunks: {e}")


def plot_chunked_terminal(df: pd.DataFrame, rule: str, title: str = "Chunked Terminal Plot", 
                          style: str = "matrix", use_navigation: bool = False) -> None:
    """
    Main function to plot data in chunks based on the rule.
    
    Args:
        df: DataFrame to plot
        rule: Trading rule to use
        title: Plot title
        style: Plot style
        use_navigation: Whether to use navigation
    """
    try:
        logger.print_info(f"🚀 Starting chunked terminal plot for rule: {rule}")
        
        # Route to appropriate plotting function based on rule
        if rule.upper() == 'OHLCV':
            plot_ohlcv_chunks(df, title, style, use_navigation)
        elif rule.upper() == 'AUTO':
            plot_auto_chunks(df, title, style, use_navigation)
        elif rule.upper() == 'PV':
            plot_pv_chunks(df, title, style, use_navigation)
        elif rule.upper() == 'SR':
            plot_sr_chunks(df, title, style, use_navigation)
        elif rule.upper() == 'PHLD':
            plot_phld_chunks(df, title, style, use_navigation)
        elif rule.upper().startswith('RSI'):
            plot_rsi_chunks(df, rule, title, style, use_navigation)
        elif rule.upper() == 'MACD':
            plot_macd_chunks(df, title, style, use_navigation)
        else:
            # Generic indicator plotting
            plot_indicator_chunks(df, rule, title, style, use_navigation, rule)
        
        logger.print_success(f"✅ Completed chunked terminal plot for rule: {rule}")
        
    except Exception as e:
        logger.print_error(f"Error in chunked terminal plot: {e}")


# Import overlay functions from indicators module
from ..indicators.overlays import (
    _add_pv_overlays_to_chunk, _add_sr_overlays_to_chunk, _add_phld_overlays_to_chunk,
    _add_rsi_overlays_to_chunk, _add_macd_overlays_to_chunk
)

from ..indicators.subplots import (
    _add_indicator_chart_to_subplot
)
