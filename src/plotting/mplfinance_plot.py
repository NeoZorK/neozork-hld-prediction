# -*- coding: utf-8 -*-
# src/plotting/mplfinance_plot.py
import mplfinance as mpf
import numpy as np
import pandas as pd

from src.common import logger
from src.common.constants import TradingRule, BUY, SELL


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
        # Try to set DatetimeIndex from 'Timestamp' or similar column
        for col in ['Timestamp', 'timestamp', 'Date', 'date', 'Datetime', 'datetime']:
            if col in df_results.columns:
                df_results = df_results.copy()
                df_results[col] = pd.to_datetime(df_results[col], errors='coerce')
                df_results = df_results.set_index(col)
                logger.print_info(f"Set DataFrame index to DatetimeIndex using column '{col}' for mplfinance plot.")
                break
        if not isinstance(df_results.index, pd.DatetimeIndex):
            logger.print_warning("DataFrame index is not a DatetimeIndex after attempted conversion. Plotting might fail.")

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

    # Ensure ratios are correctly calculated
    ratios = [4]
    ratios.extend([1] * panel_count)
    if plot_volume:
        ratios.append(0.8)

    try:
        mpf.plot(
            df_results,
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
