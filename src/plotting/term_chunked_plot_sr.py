# -*- coding: utf-8 -*-
# src/plotting/term_chunked_plot_sr.py

"""
plot_sr_chunks function for terminal chunked plotting.
"""

import pandas as pd
import numpy as np
import plotext as plt
from typing import Optional, List, Tuple, Dict, Any

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from src.common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    try:
        from src.common import logger
        from src.common.constants import TradingRule, BUY, SELL, NOTRADE
    except ImportError:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.common import logger
        from src.common.constants import TradingRule, BUY, SELL, NOTRADE

# import Navigation system
try:
    from .term_Navigation import TerminalNavigator, create_Navigation_prompt, parse_Navigation_input
    from .term_Navigation import AutoTerminalNavigator
except ImportError:
    try:
        from src.plotting.term_Navigation import TerminalNavigator, create_Navigation_prompt, parse_Navigation_input
        from src.plotting.term_Navigation import AutoTerminalNavigator
    except ImportError:
        from src.plotting.term_Navigation import TerminalNavigator, create_Navigation_prompt, parse_Navigation_input
        from src.plotting.term_Navigation import AutoTerminalNavigator

from .term_chunked_plot_base import (
    get_terminal_plot_size,
    calculate_optimal_chunk_size,
    split_dataframe_into_chunks,
    parse_rsi_rule,
    draw_ohlc_candles
)

from .term_chunked_plot_helpers import (
    _get_field_color,
    _plot_single_field_chunk,
    _has_trading_signals,
    _add_trading_signals_to_chunk,
    _show_chunk_statistics,
    _show_field_statistics
)

from .term_chunked_plot_overlays import (
    _add_pv_overlays_to_chunk,
    _add_sr_overlays_to_chunk,
    _add_phld_overlays_to_chunk,
    _add_rsi_overlays_to_chunk,
    _add_macd_overlays_to_chunk
)

from .term_chunked_plot_indicators import (
    _add_macd_chart_to_subplot,
    _add_indicator_chart_to_subplot
)


def plot_sr_chunks(
        df: pd.DataFrame,
        title: str = "SR Chunks",
        style: str = "matrix",
        Use_Navigation: bool = False) -> None:
    """
    Plot SR (Support/Resistance) data in chunks with two lines.

Args:
        df (pd.DataFrame): DataFrame with SR data
        title (str): Base title for plots
        style (str): Plot style
        Use_Navigation (bool): Whether to Use interactive Navigation
"""
    try:
        logger.print_info("Generating SR chunked plots with support/resistance lines...")

        # Calculate optimal chunk size
        total_rows = len(df)
        chunk_size = calculate_optimal_chunk_size(total_rows)
        chunks = split_dataframe_into_chunks(df, chunk_size)

    logger.print_info(f"Split {total_rows} rows into {len(chunks)} chunks of ~{chunk_size} candles each")

    if Use_Navigation:
    # Use Navigation system
    navigator = TerminalNavigator(chunks, title)

            def plot_chunk_with_Navigation(chunk: pd.DataFrame, chunk_index: int, chunk_info: dict) -> None:
    """Plot a single chunk with Navigation info."""
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

 # start Navigation
 navigator.navigate(plot_chunk_with_Navigation)

 else:
 # Original non-Navigation behavior
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

 # Add paUse between chunks
 if i < len(chunks) - 1:
 input(f"\nPress Enter to View next chunk ({i+2}/{len(chunks)})...")

 logger.print_success(f"Successfully displayed {len(chunks)} SR chunks!")

 except Exception as e:
 logger.print_error(f"Error generating SR chunked plots: {e}")


