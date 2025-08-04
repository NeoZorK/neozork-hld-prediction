# -*- coding: utf-8 -*-
# src/plotting/mplfinance_plot.py
import mplfinance as mpf
import numpy as np
import pandas as pd

from src.common import logger
from src.common.constants import TradingRule, BUY, SELL
from src.calculation.trading_metrics import calculate_trading_metrics


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

    # Determine if we should show separate charts based on rule
    # Rules that should show separate charts: OHLCV, AUTO, PHLD, PV, SR
    # All other rules (like RSI, MACD, etc.) should not show separate charts
    rule_str = rule.name.upper() if hasattr(rule, 'name') else str(rule).upper()
    show_separate_charts = rule_str in ['OHLCV', 'AUTO', 'PHLD', 'PREDICT_HIGH_LOW_DIRECTION', 'PV', 'PRESSURE_VECTOR', 'SR', 'SUPPORT_RESISTANTS']

    plots_to_add = []
    panel_count = 0

    # --- Add PPrice Lines (Panel 0, Secondary Y) ---
    if 'PPrice1' in df_results.columns:
        plots_to_add.append(mpf.make_addplot(df_results['PPrice1'], panel=0, color='lime', width=0.9, linestyle='dotted',
                                             title="PPrice1", secondary_y=True))
    if 'PPrice2' in df_results.columns:
        plots_to_add.append(mpf.make_addplot(df_results['PPrice2'], panel=0, color='red', width=0.9, linestyle='dotted',
                                             title="PPrice2", secondary_y=True))

    # --- Add parameterized indicator panels ---
    # Check for Stochastic indicators
    if 'stoch_k' in df_results.columns and not df_results['stoch_k'].isnull().all():
        panel_count += 1
        stoch_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['stoch_k'].fillna(0), panel=stoch_panel, color='blue', width=0.8, ylabel='Stochastic %K'))
        if 'stoch_d' in df_results.columns and not df_results['stoch_d'].isnull().all():
            plots_to_add.append(mpf.make_addplot(df_results['stoch_d'].fillna(0), panel=stoch_panel, color='orange', width=0.8))
        if 'stoch_overbought' in df_results.columns:
            plots_to_add.append(mpf.make_addplot(df_results['stoch_overbought'], panel=stoch_panel, color='red', linestyle='--', width=0.5))
        if 'stoch_oversold' in df_results.columns:
            plots_to_add.append(mpf.make_addplot(df_results['stoch_oversold'], panel=stoch_panel, color='green', linestyle='--', width=0.5))

    # Check for Stochastic Oscillator indicators
    if 'stochosc_k' in df_results.columns and not df_results['stochosc_k'].isnull().all():
        panel_count += 1
        stochosc_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['stochosc_k'].fillna(0), panel=stochosc_panel, color='blue', width=0.8, ylabel='StochOsc %K'))
        if 'stochosc_d' in df_results.columns and not df_results['stochosc_d'].isnull().all():
            plots_to_add.append(mpf.make_addplot(df_results['stochosc_d'].fillna(0), panel=stochosc_panel, color='orange', width=0.8))
        if 'stochosc_overbought' in df_results.columns:
            plots_to_add.append(mpf.make_addplot(df_results['stochosc_overbought'], panel=stochosc_panel, color='red', linestyle='--', width=0.5))
        if 'stochosc_oversold' in df_results.columns:
            plots_to_add.append(mpf.make_addplot(df_results['stochosc_oversold'], panel=stochosc_panel, color='green', linestyle='--', width=0.5))

    # Check for RSI indicators
    if 'rsi' in df_results.columns and not df_results['rsi'].isnull().all():
        panel_count += 1
        rsi_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['rsi'].fillna(0), panel=rsi_panel, color='purple', width=0.8, ylabel='RSI'))
        if 'rsi_overbought' in df_results.columns:
            plots_to_add.append(mpf.make_addplot(df_results['rsi_overbought'], panel=rsi_panel, color='red', linestyle='--', width=0.5))
        if 'rsi_oversold' in df_results.columns:
            plots_to_add.append(mpf.make_addplot(df_results['rsi_oversold'], panel=rsi_panel, color='green', linestyle='--', width=0.5))

    # Check for MACD indicators
    if 'macd' in df_results.columns and not df_results['macd'].isnull().all():
        panel_count += 1
        macd_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['macd'].fillna(0), panel=macd_panel, color='blue', width=0.8, ylabel='MACD'))
        if 'macd_signal' in df_results.columns and not df_results['macd_signal'].isnull().all():
            plots_to_add.append(mpf.make_addplot(df_results['macd_signal'].fillna(0), panel=macd_panel, color='orange', width=0.8))
        if 'macd_histogram' in df_results.columns and not df_results['macd_histogram'].isnull().all():
            plots_to_add.append(mpf.make_addplot(df_results['macd_histogram'].fillna(0), panel=macd_panel, color='gray', width=0.8, type='bar'))

    # Check for EMA indicators
    if 'ema' in df_results.columns and not df_results['ema'].isnull().all():
        plots_to_add.append(mpf.make_addplot(df_results['ema'].fillna(0), panel=0, color='orange', width=0.8, secondary_y=True))

    # Check for Bollinger Bands indicators
    if 'bb_upper' in df_results.columns and not df_results['bb_upper'].isnull().all():
        plots_to_add.append(mpf.make_addplot(df_results['bb_upper'].fillna(0), panel=0, color='red', width=0.8, secondary_y=True))
    if 'bb_lower' in df_results.columns and not df_results['bb_lower'].isnull().all():
        plots_to_add.append(mpf.make_addplot(df_results['bb_lower'].fillna(0), panel=0, color='red', width=0.8, secondary_y=True))
    if 'bb_middle' in df_results.columns and not df_results['bb_middle'].isnull().all():
        plots_to_add.append(mpf.make_addplot(df_results['bb_middle'].fillna(0), panel=0, color='blue', width=0.8, secondary_y=True))

    # Check for ATR indicators
    if 'atr' in df_results.columns and not df_results['atr'].isnull().all():
        panel_count += 1
        atr_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['atr'].fillna(0), panel=atr_panel, color='brown', width=0.8, ylabel='ATR'))

    # Check for CCI indicators
    if 'cci' in df_results.columns and not df_results['cci'].isnull().all():
        panel_count += 1
        cci_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['cci'].fillna(0), panel=cci_panel, color='cyan', width=0.8, ylabel='CCI'))
        # Add zero line for CCI
        plots_to_add.append(mpf.make_addplot(pd.Series(0, index=df_results.index), panel=cci_panel, color='gray', linestyle=':', width=0.5))

    # Check for VWAP indicators
    if 'vwap' in df_results.columns and not df_results['vwap'].isnull().all():
        plots_to_add.append(mpf.make_addplot(df_results['vwap'].fillna(0), panel=0, color='magenta', width=0.8, secondary_y=True))

    # Check for Pivot indicators
    if 'pivot' in df_results.columns and not df_results['pivot'].isnull().all():
        plots_to_add.append(mpf.make_addplot(df_results['pivot'].fillna(0), panel=0, color='yellow', width=0.8, secondary_y=True))

    # Check for HMA indicators
    if 'hma' in df_results.columns and not df_results['hma'].isnull().all():
        plots_to_add.append(mpf.make_addplot(df_results['hma'].fillna(0), panel=0, color='lime', width=0.8, secondary_y=True))

    # Check for TSF indicators
    if 'tsf' in df_results.columns and not df_results['tsf'].isnull().all():
        plots_to_add.append(mpf.make_addplot(df_results['tsf'].fillna(0), panel=0, color='navy', width=0.8, secondary_y=True))

    # Check for Monte Carlo indicators
    if 'monte' in df_results.columns and not df_results['monte'].isnull().all():
        panel_count += 1
        monte_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['monte'].fillna(0), panel=monte_panel, color='purple', width=0.8, ylabel='Monte Carlo'))

    # Check for Kelly indicators
    if 'kelly' in df_results.columns and not df_results['kelly'].isnull().all():
        panel_count += 1
        kelly_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['kelly'].fillna(0), panel=kelly_panel, color='green', width=0.8, ylabel='Kelly'))

    # Check for Donchain indicators
    if 'donchain' in df_results.columns and not df_results['donchain'].isnull().all():
        panel_count += 1
        donchain_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['donchain'].fillna(0), panel=donchain_panel, color='orange', width=0.8, ylabel='Donchain'))

    # Check for Fibonacci indicators
    if 'fibo' in df_results.columns and not df_results['fibo'].isnull().all():
        plots_to_add.append(mpf.make_addplot(df_results['fibo'].fillna(0), panel=0, color='gold', width=0.8, secondary_y=True))

    # Check for OBV indicators
    if 'obv' in df_results.columns and not df_results['obv'].isnull().all():
        panel_count += 1
        obv_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['obv'].fillna(0), panel=obv_panel, color='brown', width=0.8, ylabel='OBV'))

    # Check for StDev indicators
    if 'stdev' in df_results.columns and not df_results['stdev'].isnull().all():
        panel_count += 1
        stdev_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['stdev'].fillna(0), panel=stdev_panel, color='red', width=0.8, ylabel='StDev'))

    # Check for ADX indicators
    if 'adx' in df_results.columns and not df_results['adx'].isnull().all():
        panel_count += 1
        adx_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['adx'].fillna(0), panel=adx_panel, color='blue', width=0.8, ylabel='ADX'))
        if 'di_plus' in df_results.columns and not df_results['di_plus'].isnull().all():
            plots_to_add.append(mpf.make_addplot(df_results['di_plus'].fillna(0), panel=adx_panel, color='green', width=0.8))
        if 'di_minus' in df_results.columns and not df_results['di_minus'].isnull().all():
            plots_to_add.append(mpf.make_addplot(df_results['di_minus'].fillna(0), panel=adx_panel, color='red', width=0.8))

    # Check for SAR indicators
    if 'sar' in df_results.columns and not df_results['sar'].isnull().all():
        plots_to_add.append(mpf.make_addplot(df_results['sar'].fillna(0), panel=0, color='red', width=0.8, type='scatter', markersize=20, secondary_y=True))

    # Check for SuperTrend indicators
    if 'supertrend' in df_results.columns and not df_results['supertrend'].isnull().all():
        plots_to_add.append(mpf.make_addplot(df_results['supertrend'].fillna(0), panel=0, color='purple', width=0.8, secondary_y=True))

    # Check for Put/Call Ratio indicators
    if 'putcallratio' in df_results.columns and not df_results['putcallratio'].isnull().all():
        panel_count += 1
        pcr_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['putcallratio'].fillna(0), panel=pcr_panel, color='orange', width=0.8, ylabel='Put/Call Ratio'))

    # Check for COT indicators
    if 'cot' in df_results.columns and not df_results['cot'].isnull().all():
        panel_count += 1
        cot_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['cot'].fillna(0), panel=cot_panel, color='brown', width=0.8, ylabel='COT'))

    # Check for Fear & Greed indicators
    if 'feargreed' in df_results.columns and not df_results['feargreed'].isnull().all():
        panel_count += 1
        fg_panel = panel_count
        plots_to_add.append(mpf.make_addplot(df_results['feargreed'].fillna(0), panel=fg_panel, color='purple', width=0.8, ylabel='Fear & Greed'))

    # --- Add indicator panels (only if separate charts are enabled) ---
    if show_separate_charts:
        panel_map = {}
        
        # Check for PV (both 'PV' and 'pressure_vector')
        pv_col = None
        if 'PV' in df_results.columns and not df_results['PV'].isnull().all():
            pv_col = 'PV'
        elif 'pressure_vector' in df_results.columns and not df_results['pressure_vector'].isnull().all():
            pv_col = 'pressure_vector'
        
        if pv_col:
            panel_count += 1
            panel_map['PV'] = panel_count
            pv_panel = panel_map['PV']
            plots_to_add.append(mpf.make_addplot(df_results[pv_col].fillna(0), panel=pv_panel, color='orange', width=0.8, ylabel='PV'))
            plots_to_add.append(mpf.make_addplot(pd.Series(0, index=df_results.index), panel=pv_panel, color='gray', linestyle=':', width=0.5))

        if 'HL' in df_results.columns and not df_results['HL'].isnull().all():
            panel_count += 1
            panel_map['HL'] = panel_count
            hl_panel = panel_map['HL']
            plots_to_add.append(mpf.make_addplot(df_results['HL'].fillna(0), panel=hl_panel, color='brown', width=0.8, ylabel='HL (Points)'))

        # Check for Pressure (both 'Pressure' and 'pressure')
        pressure_col = None
        if 'Pressure' in df_results.columns and not df_results['Pressure'].isnull().all():
            pressure_col = 'Pressure'
        elif 'pressure' in df_results.columns and not df_results['pressure'].isnull().all():
            pressure_col = 'pressure'
        
        if pressure_col:
            panel_count += 1
            panel_map['Pressure'] = panel_count
            pressure_panel = panel_map['Pressure']
            plots_to_add.append(mpf.make_addplot(df_results[pressure_col].fillna(0), panel=pressure_panel, color='dodgerblue', width=0.8, ylabel='Pressure'))
            plots_to_add.append(mpf.make_addplot(pd.Series(0, index=df_results.index), panel=pressure_panel, color='gray', linestyle=':', width=0.5))

        # Add predicted high/low for AUTO mode
        if rule_str == 'AUTO':
            if 'predicted_low' in df_results.columns and not df_results['predicted_low'].isnull().all():
                panel_count += 1
                panel_map['predicted_low'] = panel_count
                pred_low_panel = panel_map['predicted_low']
                plots_to_add.append(mpf.make_addplot(df_results['predicted_low'].fillna(0), panel=pred_low_panel, color='green', width=0.8, ylabel='Predicted Low'))

            if 'predicted_high' in df_results.columns and not df_results['predicted_high'].isnull().all():
                panel_count += 1
                panel_map['predicted_high'] = panel_count
                pred_high_panel = panel_map['predicted_high']
                plots_to_add.append(mpf.make_addplot(df_results['predicted_high'].fillna(0), panel=pred_high_panel, color='red', width=0.8, ylabel='Predicted High'))

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

    # --- Trading Metrics Display ---
    # NOTE: Metrics have been removed from charts as requested
    # Metrics are now displayed only in console output via universal_trading_metrics module

    ratios = [4]
    ratios.extend([1] * panel_count)
    if 'Volume' in df_results.columns and not df_results['Volume'].isnull().all():
        ratios.append(0.8)

    try:
        # Determine the rule name for the title
        if hasattr(rule, 'name'):
            rule_name = rule.name
        else:
            rule_name = str(rule)

        # Check if we have original rule with parameters for display
        if hasattr(rule, 'original_rule_with_params'):
            display_rule = rule.original_rule_with_params
        else:
            display_rule = rule_name

        mpf.plot(
            df_results,
            type='candle',
            style='yahoo',
            title=title,
            ylabel='Price',
            volume='Volume' in df_results.columns and not df_results['Volume'].isnull().all(),
            volume_panel=panel_count + 1 if 'Volume' in df_results.columns and not df_results['Volume'].isnull().all() else 0,
            addplot=plots_to_add,
            panel_ratios=tuple(ratios),
            figratio=(12, 6 + panel_count * 1.5 + (1 if 'Volume' in df_results.columns and not df_results['Volume'].isnull().all() else 0)),
            figscale=1.1,
            warn_too_much_data=10000
        )
        logger.print_success("Mplfinance plot displayed.")
    except Exception as e:
        logger.print_error(f"Error during mplfinance plotting: {e}")
        logger.print_warning("Ensure your DataFrame has sufficient data and correct columns for mplfinance.")
