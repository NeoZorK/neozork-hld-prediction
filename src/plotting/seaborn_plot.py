import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from typing import List, Optional

from src.common import logger
from src.common.constants import TradingRule, BUY, SELL
from src.plotting.metrics_display import add_metrics_to_matplotlib_chart
from src.calculation.trading_metrics import calculate_trading_metrics

def plot_indicator_results_seaborn(
    df: pd.DataFrame,
    selected_rule,
    plot_title: str = ""
):
    """
    Creates a seaborn-based chart with OHLC data and selected indicator results.

    Args:
        df (pd.DataFrame): The DataFrame returned by calculate_pressure_vector.
                           Must contain 'Open', 'High', 'Low', 'Close'.
                           Should ideally contain 'Volume'.
        selected_rule: The trading rule used, to customize plotting.
        plot_title (str): The title for the chart.
    """
    # --- Input Validation ---
    required_cols = ['Open', 'High', 'Low', 'Close']
    if df is None or df.empty:
        logger.print_warning("Input DataFrame is None or empty. Cannot create plot.")
        return
    if not all(col in df.columns for col in required_cols):
        logger.print_error(f"Input DataFrame must contain columns: {required_cols}. Found: {list(df.columns)}")
        return
    if not isinstance(df.index, pd.DatetimeIndex):
        logger.print_warning("DataFrame index is not a DatetimeIndex. Plotting might be affected.")
        try:
            df.index = pd.to_datetime(df.index)
        except Exception:
            logger.print_error("Failed to convert index to DatetimeIndex.")

    # --- Determine number of subplots needed ---
    indicators_to_plot = {
        'Volume': 'Volume',
        'PV': 'PV',
        'HL': 'HL (Points)',
        'Pressure': 'Pressure'
    }
    # Check which indicator columns exist and are not entirely null
    valid_indicator_cols = [col for col in indicators_to_plot if col in df.columns and not df[col].isnull().all()]
    logger.print_debug(f"Seaborn: Found valid indicator columns for subplots: {valid_indicator_cols}")
    num_indicator_subplots = len(valid_indicator_cols)
    total_rows = 1 + num_indicator_subplots  # Dynamic total rows
    logger.print_debug(f"Seaborn: Total rows for subplots: {total_rows}")

    # --- Create Subplots ---
    # Handle case where no indicators are valid to avoid division by zero
    if num_indicator_subplots > 0:
        # Distribute remaining height among indicator subplots
        row_heights = [0.6] + [0.4 / num_indicator_subplots] * num_indicator_subplots
    else:
        row_heights = [1.0]  # Only the price chart

    # Dynamic subplot titles based on valid indicators
    subplot_titles = ["Price / Signals"] + [indicators_to_plot[col] for col in valid_indicator_cols]

    fig, axes = plt.subplots(total_rows, 1, figsize=(15, 5 * total_rows), height_ratios=row_heights)
    if total_rows == 1:
        axes = [axes]  # Make it iterable

    # --- Add Price Candlestick Trace (Row 1) ---
    ax_price = axes[0]
    
    # Create candlestick-like visualization
    idx = range(len(df))
    
    # Plot candlesticks
    for i in idx:
        open_price = df['Open'].iloc[i]
        close_price = df['Close'].iloc[i]
        high_price = df['High'].iloc[i]
        low_price = df['Low'].iloc[i]
        
        # Determine color based on open vs close
        color = 'green' if close_price >= open_price else 'red'
        
        # Plot the body
        body_height = abs(close_price - open_price)
        body_bottom = min(open_price, close_price)
        ax_price.bar(i, body_height, bottom=body_bottom, color=color, alpha=0.7, width=0.8)
        
        # Plot the wick
        ax_price.plot([i, i], [low_price, high_price], color='black', linewidth=1)

    # --- Add PPrice Lines (Row 1) ---
    if 'PPrice1' in df.columns:
        ax_price.plot(idx, df['PPrice1'], color='lime', linestyle='--', linewidth=1, label='PPrice1')
    if 'PPrice2' in df.columns:
        ax_price.plot(idx, df['PPrice2'], color='red', linestyle='--', linewidth=1, label='PPrice2')

    # --- Add Direction Markers (Row 1) ---
    if 'Direction' in df.columns:
        buy_signals = df['Direction'] == BUY
        sell_signals = df['Direction'] == SELL
        
        if buy_signals.any():
            buy_indices = [i for i, signal in enumerate(buy_signals) if signal]
            buy_prices = df.loc[buy_signals, 'Low'] * 0.998
            ax_price.scatter(buy_indices, buy_prices, color='lime', marker='^', s=50, label='BUY Signal')
        
        if sell_signals.any():
            sell_indices = [i for i, signal in enumerate(sell_signals) if signal]
            sell_prices = df.loc[sell_signals, 'High'] * 1.002
            ax_price.scatter(sell_indices, sell_prices, color='red', marker='v', s=50, label='SELL Signal')

    # Set price chart title and labels
    ax_price.set_title(plot_title)
    ax_price.set_ylabel("Price")
    ax_price.legend()
    ax_price.grid(True, alpha=0.3)

    # --- Add Indicator Subplots ---
    current_row = 1  # Start from row 1
    for indicator_col in valid_indicator_cols:
        ax_panel = axes[current_row]
        indicator_name = indicators_to_plot[indicator_col]
        indicator_data = df[indicator_col].fillna(0)

        if indicator_col == 'Volume':
            ax_panel.bar(idx, indicator_data, color='gray', alpha=0.3, label='Volume')
            ax_panel.set_ylabel('Volume')
        else:
            line_color = 'orange' if indicator_col == 'PV' else \
                         'brown' if indicator_col == 'HL' else \
                         'dodgerblue' if indicator_col == 'Pressure' else 'purple'
            ax_panel.plot(idx, indicator_data, color=line_color, label=indicator_name)
            
            if indicator_col in ['PV', 'Pressure']:
                ax_panel.axhline(0, color='gray', linestyle='--', linewidth=1)
            ax_panel.set_ylabel(indicator_name)
        
        ax_panel.legend(loc='upper left', fontsize=9)
        ax_panel.grid(True, alpha=0.3)
        current_row += 1

    # Set x-axis label for the last subplot
    axes[-1].set_xlabel("Time")

    # --- Trading Metrics Display ---
    # NOTE: Metrics have been removed from charts as requested
    # Metrics are now displayed only in console output via universal_trading_metrics module

    plt.tight_layout()
    plt.show()
