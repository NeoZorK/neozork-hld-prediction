# -*- coding: utf-8 -*-
# src/plotting/term_chunked_plot_auto.py

"""
plot_auto_chunks function for terminal chunked plotting.
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


def plot_auto_chunks(
        df: pd.DataFrame,
        title: str = "AUTO Chunks",
        style: str = "matrix",
        Use_Navigation: bool = False) -> None:
    """
    Plot all fields in chunks with separate charts for each field.

    Args:
    df (pd.DataFrame): dataFrame with all fields
    title (str): Base title for plots
    style (str): Plot style
    Use_Navigation (bool): Whether to Use interactive Navigation
    """
    try:
        logger.print_info("Generating AUTO chunked plots for all fields...")

        # Calculate optimal chunk size
        total_rows = len(df)
        chunk_size = calculate_optimal_chunk_size(total_rows)
        chunks = split_dataframe_into_chunks(df, chunk_size)

logger.print_info(
    f"Split {total_rows} rows into {
        len(chunks)} chunks of ~{chunk_size} candles each")

# Get all numeric columns
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

# Skip standard columns for individual field plots
skip_columns = {
    'Open',
    'High',
    'Low',
    'Close',
    'Volume',
    'DateTime',
    'Timestamp',
    'Date',
    'Time',
    'index',
    'index'}
field_columns = [col for col in numeric_columns if col not in skip_columns]

if Use_Navigation:
    # Use AUTO Navigation system with field switching
    navigator = AutoTerminalNavigator(chunks, title, field_columns)

def plot_chunk_with_Navigation(
                chunk: pd.DataFrame,
        chunk_index: int,
        chunk_info: dict) -> None:
    """Plot a single chunk with Navigation info."""
    if len(chunk) == 0:
    logger.print_warning("Empty chunk, skipping...")
    return

    # Get start and end dates for this chunk
    start_date = chunk_info['start_date']
    end_date = chunk_info['end_date']

logger.print_info(
    f"Displaying chunk {
        chunk_info['index']}/{
            chunk_info['total']} ({start_date} to {end_date})")

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
plt.title(
    f"{title} - OHLC (Chunk {chunk_info['index']}) - {start_date} to {end_date}")
plt.xlabel("Date/Time")
if len(x_values) > 0:
    step = max(1, len(x_values) // 10)
    plt.xticks(x_values[::step], x_labels[::step])
    plt.ylabel("Price")
    plt.show()

    # Show specific field if selected and it's not OHLC
    if current_field and current_field in chunk.columns and group_info['name'] != 'OHLC':
_plot_single_field_chunk(chunk,
                         current_field,
                         f"{title} - {current_field} (Chunk {chunk_info['index']})",
                         style)

# start Navigation
navigator.navigate(plot_chunk_with_Navigation)

else:
    # Original non-Navigation behavior
    for i, chunk in enumerate(chunks):
    chunk_start_idx = i * chunk_size
    chunk_end_idx = min((i + 1) * chunk_size, total_rows)

logger.print_info(
    f"Displaying chunk {
        i + 1}/{
            len(chunks)} (candles {
                chunk_start_idx + 1}-{chunk_end_idx})")

# Get start and end dates for this chunk
start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"

logger.print_info(
    f"Displaying chunk {i + 1}/{len(chunks)} ({start_date} to {end_date})")

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
plt.title(f"{title} - OHLC (Chunk {i + 1}) - {start_date} to {end_date}")
plt.xlabel("Date/Time")
if len(x_values) > 0:
    step = max(1, len(x_values) // 10)
    plt.xticks(x_values[::step], x_labels[::step])
    plt.ylabel("Price")
    plt.show()

    # Then show each field separately
    for field in field_columns:
    if field in chunk.columns:
_plot_single_field_chunk(
    chunk, field, f"{title} - {field} (Chunk {i + 1})", style)

# Add paUse between chunks
if i < len(chunks) - 1:
input(f"\nPress Enter to View next chunk ({i + 2}/{len(chunks)})...")

logger.print_success(f"Successfully displayed {len(chunks)} AUTO chunks!")

except Exception as e:
    logger.print_error(f"Error generating AUTO chunked plots: {e}")


