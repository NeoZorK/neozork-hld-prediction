# -*- coding: utf-8 -*-
# src/plotting.py

"""
Plotting functions for visualizing indicator results using mplfinance.
"""

import pandas as pd
import numpy as np
import mplfinance as mpf
from .constants import TradingRule, BUY, SELL # Import constants

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

    # --- Add common indicators ---
    if 'LWMA' in df_results.columns:
      plots.append(mpf.make_addplot(df_results['LWMA'], panel=0, color='blue', width=0.7, title="LWMA"))

    # --- Add PPrice1 and PPrice2 to main panel (panel 0) ---
    if 'PPrice1' in df_results.columns:
        plots.append(mpf.make_addplot(df_results['PPrice1'], panel=0, color='green', width=0.9, linestyle='dotted', title="PPrice1"))
    if 'PPrice2' in df_results.columns:
         plots.append(mpf.make_addplot(df_results['PPrice2'], panel=0, color='red', width=0.9, linestyle='dotted', title="PPrice2"))

    # --- Add indicator panels ---
    panel_map = {} # Keep track of which indicator is on which panel

    #Add CORE1 in a separate panel if it exists
    if 'CORE1' in df_results.columns:
        panel_count += 1
        panel_map['CORE1'] = panel_count
        core1_panel = panel_map['CORE1']
        plots.append(mpf.make_addplot(df_results['CORE1'], panel=core1_panel, color='purple', width=0.8, ylabel='CORE1', ylim=(0, 100)))
        plots.append(mpf.make_addplot(pd.Series(70, index=df_results.index), panel=core1_panel, color='red', linestyle='--', width=0.5))
        plots.append(mpf.make_addplot(pd.Series(30, index=df_results.index), panel=core1_panel, color='green', linestyle='--', width=0.5))

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
    if 'Direction' in df_results.columns:
        # Place markers slightly offset from High/Low
        buy_signals = df_results['Low'] * 0.998
        sell_signals = df_results['High'] * 1.002

        # Ensure signals are numeric before comparison
        direction_numeric = pd.to_numeric(df_results['Direction'], errors='coerce')

        # Plot BUY markers where Direction is BUY (1.0)
        buy_marker_data = buy_signals[direction_numeric == BUY]
        if not buy_marker_data.dropna().empty:
             plots.append(mpf.make_addplot(buy_marker_data,
                                           type='scatter', markersize=50, marker='^', color='lime', panel=0))
        # Plot SELL markers where Direction is SELL (2.0)
        sell_marker_data = sell_signals[direction_numeric == SELL]
        if not sell_marker_data.dropna().empty:
             plots.append(mpf.make_addplot(sell_marker_data,
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
        print(f"Error during plotting: {e}")
        print("Ensure your DataFrame has sufficient data and correct columns.")