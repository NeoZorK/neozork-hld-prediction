# -*- coding: utf-8 -*-
# src/plotting/plotting.py

"""
Plotting functions for visualizing indicator results using Plotly (interactive)
or mplfinance (static).
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import mplfinance as mpf # Import mplfinance

# Use relative imports for constants and logger
from ..common.constants import TradingRule, BUY, SELL
from ..common import logger


# Function to create the Plotly figure
def plot_indicator_results_plotly(df_results: pd.DataFrame, rule: TradingRule, title: str = "Indicator Results") -> go.Figure | None:
    """
    Creates an interactive Plotly chart with OHLC data and selected indicator results.

    Args:
        df_results (pd.DataFrame): The DataFrame returned by calculate_pressure_vector.
                                   Must contain 'Open', 'High', 'Low', 'Close'.
                                   Should ideally contain 'Volume'.
        rule (TradingRule): The trading rule used, to customize plotting.
        title (str): The title for the chart.

    Returns:
        go.Figure | None: A Plotly Figure object ready to be shown or saved,
                          or None if input data is invalid.
    """
    # --- Input Validation ---
    required_cols = ['Open', 'High', 'Low', 'Close']
    if df_results is None or df_results.empty:
        logger.print_warning("Input DataFrame is None or empty. Cannot create plot.")
        return None
    if not all(col in df_results.columns for col in required_cols):
        # logger.print_error(f"Input DataFrame must contain columns: {required_cols}. Found: {list(df_results.columns)}")
        raise ValueError(f"Input DataFrame must contain columns: {required_cols}. Found: {list(df_results.columns)}")
        return None
    if not isinstance(df_results.index, pd.DatetimeIndex):
        logger.print_warning("DataFrame index is not a DatetimeIndex. Plotting might be affected.")
        try:
            df_results.index = pd.to_datetime(df_results.index)
        except Exception:
            logger.print_error("Failed to convert index to DatetimeIndex.")
            # return None

    # --- Determine number of subplots needed (Dynamic approach restored) ---
    indicators_to_plot = {
        'Volume': 'Volume',
        'PV': 'PV',
        'HL': 'HL (Points)',
        'Pressure': 'Pressure'
    }
    # Check which indicator columns exist and are not entirely null
    valid_indicator_cols = [col for col in indicators_to_plot if col in df_results.columns and not df_results[col].isnull().all()]
    logger.print_debug(f"Plotly: Found valid indicator columns for subplots: {valid_indicator_cols}")
    num_indicator_subplots = len(valid_indicator_cols)
    total_rows = 1 + num_indicator_subplots # Dynamic total rows
    logger.print_debug(f"Plotly: Total rows for subplots: {total_rows}")


    # --- Create Subplots (Dynamic approach restored) ---
    # Handle case where no indicators are valid to avoid division by zero
    if num_indicator_subplots > 0:
        # Distribute remaining height among indicator subplots
        row_heights = [0.6] + [0.4 / num_indicator_subplots] * num_indicator_subplots
    else:
        row_heights = [1.0] # Only the price chart

    # Dynamic subplot titles based on valid indicators
    subplot_titles = ["Price / Signals"] + [indicators_to_plot[col] for col in valid_indicator_cols]

    fig = make_subplots(
        rows=total_rows,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=row_heights, # Use dynamic heights
        subplot_titles=subplot_titles # Use dynamic titles
    )


    # --- Add Price Candlestick Trace (Row 1) ---
    fig.add_trace(go.Candlestick(
        x=df_results.index,
        open=df_results['Open'],
        high=df_results['High'],
        low=df_results['Low'],
        close=df_results['Close'],
        name='OHLC'
    ), row=1, col=1)

    # --- Add PPrice Lines (Row 1) ---
    if 'PPrice1' in df_results.columns:
        fig.add_trace(go.Scatter(
            x=df_results.index, y=df_results['PPrice1'], mode='lines',
            line=dict(color='lime', width=1, dash='dot'), name='PPrice1'
        ), row=1, col=1)
    if 'PPrice2' in df_results.columns:
        fig.add_trace(go.Scatter(
            x=df_results.index, y=df_results['PPrice2'], mode='lines',
            line=dict(color='red', width=1, dash='dot'), name='PPrice2'
        ), row=1, col=1)

    # --- Add Direction Markers (Row 1) ---
    if 'Direction' in df_results.columns:
        # (Code for direction markers remains the same)
        low_numeric = pd.to_numeric(df_results['Low'], errors='coerce')
        high_numeric = pd.to_numeric(df_results['High'], errors='coerce')
        buy_signals_y_pos = low_numeric * 0.998
        sell_signals_y_pos = high_numeric * 1.002
        direction_numeric = pd.to_numeric(df_results['Direction'], errors='coerce')
        buy_mask = (direction_numeric == BUY)
        sell_mask = (direction_numeric == SELL)
        if buy_mask.any():
            fig.add_trace(go.Scatter(x=df_results.index[buy_mask], y=buy_signals_y_pos[buy_mask], mode='markers', marker=dict(symbol='triangle-up', size=8, color='lime'), name='BUY Signal'), row=1, col=1)
        if sell_mask.any():
            fig.add_trace(go.Scatter(x=df_results.index[sell_mask], y=sell_signals_y_pos[sell_mask], mode='markers', marker=dict(symbol='triangle-down', size=8, color='red'), name='SELL Signal'), row=1, col=1)


    # --- Add Indicator Subplots (Dynamic row assignment restored) ---
    current_row = 2 # Start from row 2
    logger.print_debug(f"Plotly: Starting loop to add indicator traces. Valid columns: {valid_indicator_cols}")
    for indicator_col in valid_indicator_cols: # Loop through only valid indicators
        logger.print_debug(f"Plotly: Processing indicator column '{indicator_col}' for dynamic row {current_row}")
        indicator_name = indicators_to_plot[indicator_col]
        # Keep the fillna(0) as it seems necessary
        indicator_data = df_results[indicator_col].fillna(0)

        if indicator_col == 'Volume':
            logger.print_debug(f"Plotly: Adding Bar trace for '{indicator_col}' to row {current_row}")
            fig.add_trace(go.Bar(
                x=df_results.index, y=indicator_data, name=indicator_name,
                marker_color='rgba(100, 100, 100, 0.5)'
            ), row=current_row, col=1) # Use current_row
        else:
            line_color = 'orange' if indicator_col == 'PV' else \
                         'brown' if indicator_col == 'HL' else \
                         'dodgerblue' if indicator_col == 'Pressure' else 'purple'
            logger.print_debug(f"Plotly: Adding Scatter trace for '{indicator_col}' to row {current_row}")
            fig.add_trace(go.Scatter(
                x=df_results.index, y=indicator_data, mode='lines',
                line=dict(color=line_color, width=1), name=indicator_name
            ), row=current_row, col=1) # Use current_row

            if indicator_col in ['PV', 'Pressure']:
                 logger.print_debug(f"Plotly: Adding hline for '{indicator_col}' to row {current_row}")
                 fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="grey", row=current_row, col=1) # Use current_row

        # Update the y-axis title for the current subplot row
        fig.update_yaxes(title_text=indicator_name, row=current_row, col=1)
        current_row += 1 # Increment row for the next valid indicator
    logger.print_debug(f"Plotly: Finished loop adding indicator traces. Next row would be: {current_row}")


    # --- Update Layout ---
    chart_layout_title = f"{title} - Rule: {rule.name}"
    fig.update_layout(
        title=chart_layout_title,
        height=350 * total_rows, # Height based on dynamic number of rows
        xaxis_rangeslider_visible=False,
        showlegend=True,
        legend=dict(
            orientation="v", yanchor="top", y=1, xanchor="left", x=1.02
        ),
        margin=dict(l=50, r=150, t=80, b=50)
    )
    fig.update_xaxes(rangeslider_visible=False)
    fig.update_yaxes(title_text="Price", row=1, col=1)
    # No need for the explicit loop to update y-axis titles here,
    # as it's done inside the main loop now.

    return fig


# --- Function to create the mplfinance plot ---
# (mplfinance function remains unchanged)
def plot_indicator_results_mplfinance(df_results: pd.DataFrame, rule: TradingRule, title: str = "Indicator Results"):
    """
    Plots the OHLC data along with selected indicator results using mplfinance.
    (Original function, potentially slower for large data).

    Args:
        df_results (pd.DataFrame): The DataFrame returned by calculate_pressure_vector.
                                   Must contain 'Open', 'High', 'Low', 'Close'.
                                   Should ideally contain 'Volume'.
        rule (TradingRule): The trading rule used, to customize plotting.
        title (str): The title for the chart.
    """

    # --- Input Validation ---
    required_cols = ['Open', 'High', 'Low', 'Close']
    if df_results is None or df_results.empty:
        logger.print_warning("Input DataFrame is None or empty. Cannot create plot.")
        return
    if not all(col in df_results.columns for col in required_cols):
        logger.print_error(f"Input DataFrame must contain columns: {required_cols}. Found: {list(df_results.columns)}")
        return
    if not isinstance(df_results.index, pd.DatetimeIndex):
        logger.print_warning("DataFrame index is not a DatetimeIndex. Plotting might be affected.")

    plots_to_add = []
    panel_count = 0

    # --- Add PPrice Lines (Panel 0, Secondary Y) ---
    if 'PPrice1' in df_results.columns:
        plots_to_add.append(mpf.make_addplot(df_results['PPrice1'], panel=0, color='lime', width=0.9, linestyle='dotted',
                                             title="PPrice1", secondary_y=True))
    if 'PPrice2' in df_results.columns:
        plots_to_add.append(mpf.make_addplot(df_results['PPrice2'], panel=0, color='red', width=0.9, linestyle='dotted',
                                             title="PPrice2", secondary_y=True))

    # --- Add indicator panels ---
    panel_map = {}
    if 'PV' in df_results.columns and not df_results['PV'].isnull().all():
        panel_count += 1
        panel_map['PV'] = panel_count
        pv_panel = panel_map['PV']
        plots_to_add.append(mpf.make_addplot(df_results['PV'].fillna(0), panel=pv_panel, color='orange', width=0.8, ylabel='PV'))
        plots_to_add.append(mpf.make_addplot(pd.Series(0, index=df_results.index), panel=pv_panel, color='gray', linestyle=':', width=0.5))

    if 'HL' in df_results.columns and not df_results['HL'].isnull().all():
        panel_count += 1
        panel_map['HL'] = panel_count
        hl_panel = panel_map['HL']
        plots_to_add.append(mpf.make_addplot(df_results['HL'].fillna(0), panel=hl_panel, color='brown', width=0.8, ylabel='HL (Points)'))

    if 'Pressure' in df_results.columns and not df_results['Pressure'].isnull().all():
        panel_count += 1
        panel_map['Pressure'] = panel_count
        pressure_panel = panel_map['Pressure']
        plots_to_add.append(mpf.make_addplot(df_results['Pressure'].fillna(0), panel=pressure_panel, color='dodgerblue', width=0.8, ylabel='Pressure'))
        plots_to_add.append(mpf.make_addplot(pd.Series(0, index=df_results.index), panel=pressure_panel, color='gray', linestyle=':', width=0.5))

    # --- Add Direction markers (Panel 0) ---
    if 'Direction' in df_results.columns and 'Low' in df_results.columns and 'High' in df_results.columns:
        low_numeric = pd.to_numeric(df_results['Low'], errors='coerce')
        high_numeric = pd.to_numeric(df_results['High'], errors='coerce')
        buy_signals_y_pos = low_numeric.ffill().bfill() * 0.998
        sell_signals_y_pos = high_numeric.ffill().bfill() * 1.002
        direction_numeric = pd.to_numeric(df_results['Direction'], errors='coerce')
        buy_markers_y = np.where(direction_numeric == BUY, buy_signals_y_pos, np.nan)
        sell_markers_y = np.where(direction_numeric == SELL, sell_signals_y_pos, np.nan)
        buy_markers_series = pd.Series(buy_markers_y, index=df_results.index)
        sell_markers_series = pd.Series(sell_markers_y, index=df_results.index)

        if not buy_markers_series.dropna().empty:
            plots_to_add.append(mpf.make_addplot(buy_markers_series,
                                                 type='scatter', markersize=50, marker='^', color='lime', panel=0))
        if not sell_markers_series.dropna().empty:
            plots_to_add.append(mpf.make_addplot(sell_markers_series,
                                                 type='scatter', markersize=50, marker='v', color='red', panel=0))

    # --- Create the plot ---
    plot_volume = 'Volume' in df_results.columns and not df_results['Volume'].isnull().all()
    volume_panel = 1
    if panel_count > 0:
        volume_panel = panel_count + 1
        if plot_volume:
             pass

    ratios = [4]
    ratios.extend([1] * panel_count)
    if plot_volume:
         ratios.append(0.8)

    try:
        mpf.plot(df_results,
                 type='candle',
                 style='yahoo',
                 title=f"{title} - Rule: {rule.name}",
                 ylabel='Price',
                 volume=plot_volume,
                 volume_panel=volume_panel if plot_volume else 0,
                 addplot=plots_to_add,
                 panel_ratios=tuple(ratios),
                 figratio=(12, 6 + panel_count * 1.5 + (1 if plot_volume else 0)),
                 figscale=1.1,
                 warn_too_much_data=10000
                 )
        logger.print_success("Mplfinance plot displayed.")
    except Exception as e:
        logger.print_error(f"Error during mplfinance plotting: {e}")
        logger.print_warning("Ensure your DataFrame has sufficient data and correct columns for mplfinance.")

# --- Wrapper function to call either Plotly or mplfinance ---
def plot_indicator_results(df_results, rule, title="Indicator Results", use_plotly=True):
    """
    Wrapper function to call either Plotly or mplfinance plotting functions.
    """
    if use_plotly:
        return plot_indicator_results_plotly(df_results, rule, title)
    else:
        return plot_indicator_results_mplfinance(df_results, rule, title)
