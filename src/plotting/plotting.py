# -*- coding: utf-8 -*-
# src/plotting.py

"""
Plotting functions for visualizing indicator results using mplfinance.
"""

import pandas as pd
import mplfinance as mpf
import numpy as np
from ..common.constants import TradingRule, BUY, SELL
from ..common import logger

def plot_indicator_results(df_results: pd.DataFrame, rule: TradingRule, title: str = "Indicator Results"):
    """
    Plots the OHLC data along with selected indicator results using mplfinance.

    Args:
        df_results (pd.DataFrame): The DataFrame returned by calculate_pressure_vector.
                                   Must contain 'Open', 'High', 'Low', 'Close'.
                                   Should ideally contain 'Volume'.
        rule (TradingRule): The trading rule used, to customize plotting.
        title (str): The title for the chart.
    """
    # Ensure required OHLC columns exist
    required_cols = ['Open', 'High', 'Low', 'Close']
    if not all(col in df_results.columns for col in required_cols):
        raise ValueError(f"Input DataFrame must contain columns: {required_cols}")

    plots = [] # List to hold additional plots (addplot)
    panel_count = 0 # Start with main panel 0

    # Definition of the plot_indicator_results function
    if 'PPrice1' in df_results.columns:
        # Add plot for PPrice1 without secondary y-axis
        # panel=0: Plot on the main price panel
        # color='green': Set line color
        # width=0.9: Set line width
        # linestyle='dotted': Set line style
        # title="PPrice1": Set legend title
        plots.append(mpf.make_addplot(df_results['PPrice1'], panel=0, color='green', width=0.9, linestyle='dotted',
                                      title="PPrice1"))  # secondary_y=True removed
    if 'PPrice2' in df_results.columns:
        # Add plot for PPrice2 without secondary y-axis
        # panel=0: Plot on the main price panel
        # color='red': Set line color
        # width=0.9: Set line width
        # linestyle='dotted': Set line style
        # title="PPrice2": Set legend title
        plots.append(mpf.make_addplot(df_results['PPrice2'], panel=0, color='red', width=0.9, linestyle='dotted',
                                      title="PPrice2"))  # secondary_y=True removed
    # --- Add indicator panels ---
    panel_map = {} # Keep track of which indicator is on which panel

    # Add PV in a separate panel if it exists
    if 'PV' in df_results.columns:
        panel_count += 1
        panel_map['PV'] = panel_count
        pv_panel = panel_map['PV']
        # Fill NaN for plotting PV, NaNs might break scatter plots otherwise
        plots.append(mpf.make_addplot(df_results['PV'].fillna(0), panel=pv_panel, color='orange', width=0.8, ylabel='PV'))
        plots.append(mpf.make_addplot(pd.Series(0, index=df_results.index), panel=pv_panel, color='gray', linestyle=':', width=0.5))

    # --- Add NEW panels for HL and Pressure ---
    if 'HL' in df_results.columns:
        panel_count += 1
        panel_map['HL'] = panel_count
        hl_panel = panel_map['HL']
        plots.append(mpf.make_addplot(df_results['HL'].fillna(0), panel=hl_panel, color='brown', width=0.8, ylabel='HL (Points)'))
        # Optionally add a zero line if HL can be zero or negative (though unlikely here)
        # plots.append(mpf.make_addplot(pd.Series(0, index=df_results.index), panel=hl_panel, color='gray', linestyle=':', width=0.5))

    if 'Pressure' in df_results.columns:
        panel_count += 1
        panel_map['Pressure'] = panel_count
        pressure_panel = panel_map['Pressure']
        plots.append(mpf.make_addplot(df_results['Pressure'].fillna(0), panel=pressure_panel, color='dodgerblue', width=0.8, ylabel='Pressure'))
        plots.append(mpf.make_addplot(pd.Series(0, index=df_results.index), panel=pressure_panel, color='gray', linestyle=':', width=0.5))


    # --- Add rule-specific plots (e.g., Direction markers) ---
        # --- Add rule-specific plots (e.g., Direction markers) ---
        if 'Direction' in df_results.columns and 'Low' in df_results.columns and 'High' in df_results.columns:
            # Ensure Low and High are numeric before calculation
            low_numeric = pd.to_numeric(df_results['Low'], errors='coerce')
            high_numeric = pd.to_numeric(df_results['High'], errors='coerce')

            # Calculate marker positions slightly offset from High/Low
            # Use obj.ffill() or obj.bfill() instead of fillna(method=...)
            buy_signals_y_pos = low_numeric.ffill().bfill() * 0.998
            sell_signals_y_pos = high_numeric.ffill().bfill() * 1.002

            # Ensure signals are numeric before comparison
            direction_numeric = pd.to_numeric(df_results['Direction'], errors='coerce')

            # --- CORRECTED MARKER LOGIC ---
            # Create full-size series with NaN where condition is false
            buy_markers_y = np.where(direction_numeric == BUY, buy_signals_y_pos, np.nan)
            sell_markers_y = np.where(direction_numeric == SELL, sell_signals_y_pos, np.nan)

            # Create Pandas Series with the same index as the main DataFrame
            # This ensures alignment for plotting
            buy_markers_series = pd.Series(buy_markers_y, index=df_results.index)
            sell_markers_series = pd.Series(sell_markers_y, index=df_results.index)

            # Add scatter plots using the full-size NaN-filled series
            # mplfinance/matplotlib will ignore NaNs automatically when plotting points
            if not buy_markers_series.dropna().empty:
                plots.append(mpf.make_addplot(buy_markers_series,
                                              type='scatter', markersize=50, marker='^', color='lime', panel=0))
            if not sell_markers_series.dropna().empty:
                plots.append(mpf.make_addplot(sell_markers_series,
                                              type='scatter', markersize=50, marker='v', color='red', panel=0))

    # --- Create the plot ---
    # Ensure volume is plotted if available
    plot_volume = 'Volume' in df_results.columns

    # Define panel ratios dynamically
    # Main panel gets larger share (e.g., 4), subplots get 1
    ratios = (4,) + (1,) * panel_count if panel_count > 0 else (1,)

    try:
        mpf.plot(df_results,
                 type='candle', # Use candlestick chart
                 style='yahoo', # Choose a style
                 title=f"{title} - Rule: {rule.name}",
                 ylabel='Price',
                 volume=plot_volume, # Plot volume if column exists
                 addplot=plots, # Add the extra indicator plots
                 panel_ratios=ratios,
                 figratio=(12, 6 + panel_count * 1.5), # Adjust fig size based on panels
                 figscale=1.1, # Scale figure size
                 warn_too_much_data=10000 # Adjust threshold if needed
                 )
    except Exception as e:
        logger.print_error(f"Error during plotting: {e}")
        logger.print_warning("Ensure your DataFrame has sufficient data and correct columns.")