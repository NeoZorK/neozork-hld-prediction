# -*- coding: utf-8 -*-
# src/plotting/term_chunked_plot_helpers.py

"""
Helper functions for terminal chunked plotting.
Contains utility functions for colors, field plotting, signals, and statistics.
"""

import hashlib
import pandas as pd
import numpy as np
import plotext as plt
from typing import List

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from src.common.constants import BUY, SELL, NOTRADE
except ImportError:
    try:
        from src.common import logger
        from src.common.constants import BUY, SELL, NOTRADE
    except ImportError:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.common import logger
        from src.common.constants import BUY, SELL, NOTRADE

from .term_chunked_plot_base import get_terminal_plot_size


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
        "green+",  # Bright green - very distinct
        "blue+",  # Bright blue - very distinct
        "red+",  # Bright red - very distinct
        "yellow+",  # Bright yellow - very distinct
        "magenta+",  # Bright magenta - very distinct
        "cyan+",  # Bright cyan - very distinct
        "white+",  # Bright white - very distinct
        "orange+",  # Bright orange - very distinct
        "purple+",  # Bright purple - very distinct
        "pink+",  # Bright pink - very distinct
        "light_green+",  # Light green - distinct from dark green
        "light_blue+",  # Light blue - distinct from dark blue
        "light_red+",  # Light red - distinct from dark red
        "light_yellow+",  # Light yellow - distinct from dark yellow
        "light_magenta+",  # Light magenta - distinct from dark magenta
        "light_cyan+",  # Light cyan - distinct from dark cyan
        "light_white+",  # Light white - distinct from dark white
        "light_orange+",  # Light orange - distinct from dark orange
        "brown+",  # Brown - distinct from other colors
        "gray+"  # Gray - distinct from other colors
    ]

    # Create a hash-based color assignment for consistent colors per field
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


def _has_trading_signals(chunk: pd.DataFrame) -> bool:
    """Check if chunk has trading signals."""
    return any(col in chunk.columns for col in ['Direction', '_signal'])


def _add_trading_signals_to_chunk(chunk: pd.DataFrame, x_values: List) -> None:
    """
    Add trading signals to the chunk plot.
    BUY: large yellow triangle below Low
    SELL: large magenta triangle above High

    Supports signal sources (same as other modes):
    - _signal column (wave indicator - only direction changes)
    - Direction column (standard indicator)
    """
    try:
        # check for different signal sources (same priority as other modes)
        signal_source = None
        if '_signal' in chunk.columns:
            signal_source = '_signal'
        elif 'Direction' in chunk.columns:
            signal_source = 'Direction'
        else:
            return

        # Get buy/sell signals
        buy_x, buy_y, sell_x, sell_y = [], [], [], []

        for i, signal in enumerate(chunk[signal_source]):
            # Handle different signal formats
            if signal_source == '_signal':
                # Wave indicator signal: 1 = BUY, 2 = SELL, 0 = NO TRADE (only direction changes)
                if signal == 1:  # BUY
                    buy_x.append(x_values[i])
                    if 'Low' in chunk.columns:
                        buy_y.append(chunk['Low'].iloc[i] * 0.99)
                    else:
                        buy_y.append(chunk['Close'].iloc[i] *
                                     0.99 if 'Close' in chunk.columns else 0)
                elif signal == 2:  # SELL
                    sell_x.append(x_values[i])
                    if 'High' in chunk.columns:
                        sell_y.append(chunk['High'].iloc[i] * 1.01)
                    else:
                        sell_y.append(chunk['Close'].iloc[i] *
                                      1.01 if 'Close' in chunk.columns else 0)
            else:
                # Standard Direction column
                if signal == BUY:
                    buy_x.append(x_values[i])
                    if 'Low' in chunk.columns:
                        buy_y.append(chunk['Low'].iloc[i] * 0.99)
                    else:
                        buy_y.append(chunk['Close'].iloc[i] *
                                     0.99 if 'Close' in chunk.columns else 0)
                elif signal == SELL:
                    sell_x.append(x_values[i])
                    if 'High' in chunk.columns:
                        sell_y.append(chunk['High'].iloc[i] * 1.01)
                    else:
                        sell_y.append(chunk['Close'].iloc[i] *
                                      1.01 if 'Close' in chunk.columns else 0)

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


def _show_chunk_statistics(
        chunk: pd.DataFrame,
        title: str,
        start_idx: int,
        end_idx: int) -> None:
    """
    Show statistics for a chunk.

    Args:
        chunk (pd.DataFrame): DataFrame chunk
        title (str): Chunk title
        start_idx (int): start index
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
            print(f" Open: {chunk['Open'].min():.5f} - {chunk['Open'].max():.5f}")
            print(f" High: {chunk['High'].min():.5f} - {chunk['High'].max():.5f}")
            print(f" Low: {chunk['Low'].min():.5f} - {chunk['Low'].max():.5f}")
            print(f" Close: {chunk['Close'].min():.5f} - {chunk['Close'].max():.5f}")

        # Volume statistics
        if 'Volume' in chunk.columns:
            volume = chunk['Volume'].fillna(0)
            print(f"VOLUME STATISTICS:")
            print(f" Total: {volume.sum():.0f}")
            print(f" Avg: {volume.mean():.0f}")
            print(f" Max: {volume.max():.0f}")

        # Trading signals
        if _has_trading_signals(chunk):
            buy_count = (chunk['Direction'] == BUY).sum()
            sell_count = (chunk['Direction'] == SELL).sum()
            notrade_count = (chunk['Direction'] == NOTRADE).sum()

            print(f"TRADING signALS:")
            print(f" BUY: {buy_count}")
            print(f" SELL: {sell_count}")
            print(f" NO TRADE: {notrade_count}")

        # RSI statistics
        if 'RSI' in chunk.columns:
            rsi = chunk['RSI'].dropna()
            if len(rsi) > 0:
                print(f"RSI STATISTICS:")
                print(f" Min: {rsi.min():.2f}")
                print(f" Max: {rsi.max():.2f}")
                print(f" Avg: {rsi.mean():.2f}")

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
        print(f" Min: {clean_data.min():.5f}")
        print(f" Max: {clean_data.max():.5f}")
        print(f" Avg: {clean_data.mean():.5f}")
        print(f" Std: {clean_data.std():.5f}")

    except Exception as e:
        logger.print_error(f"Error showing field statistics: {e}")

