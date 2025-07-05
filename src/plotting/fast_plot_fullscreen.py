# -*- coding: utf-8 -*-
# src/plotting/fast_plot_fullscreen.py

"""
Fast plot with dynamic fullscreen height for OHLCV rule.
This module provides a specialized plotting function for the command:
uv run run_analysis.py show csv mn1 -d fast --rule OHLCV

The chart height is dynamically calculated to use the full screen height.
"""

import os
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column
from bokeh.models import (
    HoverTool, Span, Title, ColumnDataSource, NumeralTickFormatter, Div
)
import webbrowser
from src.common import logger


def get_screen_height():
    """
    Get the screen height in pixels.
    Returns a default value if screen height cannot be determined.
    """
    try:
        # Try to get screen height using tkinter
        import tkinter as tk
        root = tk.Tk()
        screen_height = root.winfo_screenheight()
        root.destroy()
        return screen_height
    except:
        try:
            # Try using platform-specific methods
            import subprocess
            if os.name == 'nt':  # Windows
                result = subprocess.run(['wmic', 'desktopmonitor', 'get', 'screenheight'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        return int(lines[1])
            else:  # Unix-like systems
                result = subprocess.run(['xrandr', '--query'], capture_output=True, text=True)
                if result.returncode == 0:
                    import re
                    match = re.search(r'(\d+)x(\d+)', result.stdout)
                    if match:
                        return int(match.group(2))
        except:
            pass
    
    # Default fallback values
    return 1080  # Default to 1080p height


def calculate_dynamic_height(screen_height=None, rule_str=None):
    """
    Calculate dynamic height for the chart based on screen height and rule.
    For OHLCV rule, use 85% of screen height, min 400, max 2000.
    """
    if screen_height is None:
        screen_height = get_screen_height()
    if rule_str and (rule_str.upper() == 'OHLCV' or 'OHLCV' in rule_str.upper()):
        dynamic_height = int(screen_height * 0.85)
        dynamic_height = max(400, min(dynamic_height, 2000))
        logger.print_info(f"OHLCV rule detected: using fullscreen height {dynamic_height}px (screen height: {screen_height}px)")
        return dynamic_height
    return 1100


def plot_indicator_results_fast_fullscreen(
    df,
    rule,
    title='',
    output_path="results/plots/fast_plot_fullscreen.html",
    width=1000,  # Reduced to fit screen with toolbar buttons
    height=None,
    mode="fast",
    data_source="demo",
    lot_size=1.0,
    risk_reward_ratio=2.0,
    fee_per_trade=0.07,
    **kwargs
):
    """
    Draws fast mode dashboard plot with dynamic fullscreen height for OHLCV rule.
    
    This function is specifically optimized for the command:
    uv run run_analysis.py show csv mn1 -d fast --rule OHLCV
    
    Features:
    - Uses Bokeh for interactive web-based visualization
    - Dynamic height calculation for fullscreen display
    - Displays OHLC candlestick chart with volume
    - Shows trading signals and indicators
    - Interactive hover tooltips with detailed information
    - Responsive design that works in web browsers

    Layout:
    - Main panel: OHLC candlestick chart with trading signals
    - Subpanel: Volume bars with color coding
    - Additional panels for indicators (if available)
    - Interactive hover tooltips across all panels
    - Opens plot in default browser after saving
    """
    try:
        # Validate input data
        if df is None or df.empty:
            logger.print_error("DataFrame is None or empty")
            return None

        # Check for required columns
        required_columns = ['Open', 'High', 'Low', 'Close']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            logger.print_error(f"Missing required columns: {missing_columns}")
            return None

        # Prepare data
        display_df = df.copy()
        
        # Ensure index is datetime
        if not isinstance(display_df.index, pd.DatetimeIndex):
            if 'DateTime' in display_df.columns:
                display_df['DateTime'] = pd.to_datetime(display_df['DateTime'])
                display_df.set_index('DateTime', inplace=True)
            else:
                display_df.index = pd.to_datetime(display_df.index)

        # Add 'index' column for Bokeh compatibility
        display_df['index'] = display_df.index

        # Create data source for Bokeh
        source = ColumnDataSource(display_df)

        # Check if we have original rule with parameters for display
        if hasattr(rule, 'original_rule_with_params'):
            display_rule = rule.original_rule_with_params
        elif hasattr(rule, 'name'):
            display_rule = rule.name
        else:
            display_rule = str(rule)

        # Calculate dynamic height based on rule
        rule_str = display_rule.upper() if isinstance(display_rule, str) else str(display_rule).upper()
        if height is None:
            height = calculate_dynamic_height(rule_str=rule_str)
        
        logger.print_info(f"Using dynamic height: {height}px for rule: {rule_str}")

        # Determine if we should show separate charts based on rule
        # Rules that should show separate charts: AUTO, PHLD, PV, SR (but NOT OHLCV)
        # All other rules (like RSI, MACD, OHLCV, etc.) should not show separate charts
        show_separate_charts = any(key in rule_str for key in ['AUTO', 'PHLD', 'PREDICT_HIGH_LOW_DIRECTION', 'PV', 'PRESSURE_VECTOR', 'SR', 'SUPPORT_RESISTANTS'])
        logger.print_debug(f"Fast fullscreen plot: Rule string: '{rule_str}', show_separate_charts: {show_separate_charts}")

        # Calculate main figure height based on whether we show separate charts
        if show_separate_charts:
            main_fig_height = int(height * 0.4)  # 40% for main chart when showing subplots
        else:
            main_fig_height = int(height * 1.0)  # 100% for main chart when no subplots (like OHLCV)

        # Create main figure for OHLC chart
        main_fig = figure(
            width=width,
            height=main_fig_height,
            title=title,
            x_axis_type='datetime',
            tools="pan,wheel_zoom,box_zoom,reset,save",
            active_scroll='wheel_zoom'
        )

        # Add candlestick chart
        # Upward candles (green)
        up_candles = display_df[display_df['Close'] >= display_df['Open']]
        if not up_candles.empty:
            up_source = ColumnDataSource(up_candles)
            main_fig.segment(
                'index', 'High', 'index', 'Low',
                source=up_source, color='green', line_width=2
            )
            main_fig.vbar(
                'index', 0.5, 'Open', 'Close',
                source=up_source, fill_color='green', line_color='green'
            )

        # Downward candles (red)
        down_candles = display_df[display_df['Close'] < display_df['Open']]
        if not down_candles.empty:
            down_source = ColumnDataSource(down_candles)
            main_fig.segment(
                'index', 'High', 'index', 'Low',
                source=down_source, color='red', line_width=2
            )
            main_fig.vbar(
                'index', 0.5, 'Open', 'Close',
                source=down_source, fill_color='red', line_color='red'
            )

        # Add trading signals if available
        if 'Direction' in display_df.columns:
            buy_signals = display_df[display_df['Direction'] == 1]
            sell_signals = display_df[display_df['Direction'] == 2]
            
            if not buy_signals.empty:
                buy_source = ColumnDataSource(buy_signals)
                main_fig.scatter(
                    'index', 'Low',
                    source=buy_source,
                    size=10, color='green', alpha=0.7,
                    legend_label='Buy Signal',
                    marker='triangle'
                )
            
            if not sell_signals.empty:
                sell_source = ColumnDataSource(sell_signals)
                main_fig.scatter(
                    'index', 'High',
                    source=sell_source,
                    size=10, color='red', alpha=0.7,
                    legend_label='Sell Signal',
                    marker='inverted_triangle'
                )

        # Add hover tooltip for main chart
        hover_main = HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("Open", "@Open{0.5f}"),
                ("High", "@High{0.5f}"),
                ("Low", "@Low{0.5f}"),
                ("Close", "@Close{0.5f}"),
                ("Volume", "@Volume{0}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
        main_fig.add_tools(hover_main)

        # Create list of figures for layout
        figures = [main_fig]

        if show_separate_charts:
            # Volume subplot - only if data exists
            logger.print_debug(f"Fast fullscreen plot: Checking Volume column - exists: {'Volume' in display_df.columns}, not all null: {not display_df['Volume'].isna().all() if 'Volume' in display_df.columns else False}")
            if 'Volume' in display_df.columns and not display_df['Volume'].isna().all():
                volume_fig = figure(
                    width=width,
                    height=int(height * 0.15),
                    x_axis_type='datetime',
                    title='Volume',
                    tools="pan,wheel_zoom,box_zoom,reset",
                    active_scroll='wheel_zoom'
                )
                
                # Color volume bars based on price direction
                volume_colors = ['green' if close >= open else 'red' 
                               for close, open in zip(display_df['Close'], display_df['Open'])]
                display_df['volume_color'] = volume_colors
                
                volume_source = ColumnDataSource(display_df)
                volume_fig.vbar(
                    'index', 0.5, 0, 'Volume',
                    source=volume_source,
                    fill_color='volume_color',
                    line_color='volume_color',
                    alpha=0.7
                )
                
                hover_volume = HoverTool(
                    tooltips=[
                        ("Date", "@index{%F %H:%M}"),
                        ("Volume", "@Volume{0}")
                    ],
                    formatters={'@index': 'datetime'},
                    mode='vline'
                )
                volume_fig.add_tools(hover_volume)
                volume_fig.x_range = main_fig.x_range
                figures.append(volume_fig)

            # HL subplot - only if data exists
            if 'HL' in display_df.columns and not display_df['HL'].isna().all():
                hl_fig = figure(
                    width=width,
                    height=int(height * 0.15),
                    x_axis_type='datetime',
                    title='HL',
                    tools="pan,wheel_zoom,box_zoom,reset",
                    active_scroll='wheel_zoom'
                )
                hl_fig.line('index', 'HL', source=source, line_color='purple', line_width=2, legend_label='HL')
                hover_hl = HoverTool(tooltips=[("Date", "@index{%F %H:%M}"), ("HL", "@HL{0.3f}")], formatters={'@index': 'datetime'}, mode='vline')
                hl_fig.add_tools(hover_hl)
                hl_fig.x_range = main_fig.x_range
                figures.append(hl_fig)

            # Pressure subplot - only if data exists (check both 'Pressure' and 'pressure')
            logger.print_debug(f"Fast fullscreen plot: Checking pressure columns - Pressure exists: {'Pressure' in display_df.columns}, pressure exists: {'pressure' in display_df.columns}")
            pressure_col = None
            if 'Pressure' in display_df.columns and not display_df['Pressure'].isna().all():
                pressure_col = 'Pressure'
                logger.print_debug("Fast fullscreen plot: Using 'Pressure' column for pressure subplot")
            elif 'pressure' in display_df.columns and not display_df['pressure'].isna().all():
                pressure_col = 'pressure'
                logger.print_debug("Fast fullscreen plot: Using 'pressure' column for pressure subplot")
            
            if pressure_col:
                pressure_fig = figure(
                    width=width,
                    height=int(height * 0.15),
                    x_axis_type='datetime',
                    title='Pressure',
                    tools="pan,wheel_zoom,box_zoom,reset",
                    active_scroll='wheel_zoom'
                )
                pressure_fig.line('index', pressure_col, source=source, line_color='teal', line_width=2, legend_label='Pressure')
                hover_pressure = HoverTool(tooltips=[("Date", "@index{%F %H:%M}"), ("Pressure", f"@{pressure_col}{{0.3f}}")], formatters={'@index': 'datetime'}, mode='vline')
                pressure_fig.add_tools(hover_pressure)
                pressure_fig.x_range = main_fig.x_range
                figures.append(pressure_fig)

            # PV subplot - only if data exists (check both 'PV' and 'pressure_vector')
            logger.print_debug(f"Fast fullscreen plot: Checking PV columns - PV exists: {'PV' in display_df.columns}, pressure_vector exists: {'pressure_vector' in display_df.columns}")
            pv_col = None
            if 'PV' in display_df.columns and not display_df['PV'].isna().all():
                pv_col = 'PV'
                logger.print_debug("Fast fullscreen plot: Using 'PV' column for PV subplot")
            elif 'pressure_vector' in display_df.columns and not display_df['pressure_vector'].isna().all():
                pv_col = 'pressure_vector'
                logger.print_debug("Fast fullscreen plot: Using 'pressure_vector' column for PV subplot")
            
            if pv_col:
                pv_fig = figure(
                    width=width,
                    height=int(height * 0.15),
                    x_axis_type='datetime',
                    title='Pressure Vector (PV)',
                    tools="pan,wheel_zoom,box_zoom,reset",
                    active_scroll='wheel_zoom'
                )
                pv_fig.line('index', pv_col, source=source, line_color='orange', line_width=2, legend_label='PV')
                hover_pv = HoverTool(tooltips=[("Date", "@index{%F %H:%M}"), ("PV", f"@{pv_col}{{0.3f}}")], formatters={'@index': 'datetime'}, mode='vline')
                pv_fig.add_tools(hover_pv)
                pv_fig.x_range = main_fig.x_range
                figures.append(pv_fig)

            # Predicted High/Low subplots for AUTO mode
            if 'AUTO' in rule_str:
                logger.print_debug(f"Fast fullscreen plot: AUTO mode detected, checking predicted columns")
                # Predicted Low subplot
                logger.print_debug(f"Fast fullscreen plot: Checking predicted_low - exists: {'predicted_low' in display_df.columns}, not all null: {not display_df['predicted_low'].isna().all() if 'predicted_low' in display_df.columns else False}")
                if 'predicted_low' in display_df.columns and not display_df['predicted_low'].isna().all():
                    pred_low_fig = figure(
                        width=width,
                        height=int(height * 0.15),
                        x_axis_type='datetime',
                        title='Predicted Low',
                        tools="pan,wheel_zoom,box_zoom,reset",
                        active_scroll='wheel_zoom'
                    )
                    pred_low_fig.line('index', 'predicted_low', source=source, line_color='green', line_width=2, legend_label='Predicted Low')
                    hover_pred_low = HoverTool(tooltips=[("Date", "@index{%F %H:%M}"), ("Predicted Low", "@predicted_low{0.5f}")], formatters={'@index': 'datetime'}, mode='vline')
                    pred_low_fig.add_tools(hover_pred_low)
                    pred_low_fig.x_range = main_fig.x_range
                    figures.append(pred_low_fig)

                # Predicted High subplot
                logger.print_debug(f"Fast fullscreen plot: Checking predicted_high - exists: {'predicted_high' in display_df.columns}, not all null: {not display_df['predicted_high'].isna().all() if 'predicted_high' in display_df.columns else False}")
                if 'predicted_high' in display_df.columns and not display_df['predicted_high'].isna().all():
                    pred_high_fig = figure(
                        width=width,
                        height=int(height * 0.15),
                        x_axis_type='datetime',
                        title='Predicted High',
                        tools="pan,wheel_zoom,box_zoom,reset",
                        active_scroll='wheel_zoom'
                    )
                    pred_high_fig.line('index', 'predicted_high', source=source, line_color='red', line_width=2, legend_label='Predicted High')
                    hover_pred_high = HoverTool(tooltips=[("Date", "@index{%F %H:%M}"), ("Predicted High", "@predicted_high{0.5f}")], formatters={'@index': 'datetime'}, mode='vline')
                    pred_high_fig.add_tools(hover_pred_high)
                    pred_high_fig.x_range = main_fig.x_range
                    figures.append(pred_high_fig)

        # Layout: main chart + only those subplots for which data exists
        logger.print_debug(f"Fast fullscreen plot: Creating layout with {len(figures)} figures")
        for i, fig in enumerate(figures):
            logger.print_debug(f"Fast fullscreen plot: Figure {i}: {fig.title.text if hasattr(fig.title, 'text') else 'Main chart'}")
        
        layout = column(*figures)

        # Save and open
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        output_file(output_path, title=title)
        save(layout)
        abs_path = os.path.abspath(output_path)
        webbrowser.open_new_tab(f"file://{abs_path}")

        logger.print_success(f"Fast fullscreen plot saved to: {output_path}")
        logger.print_info(f"Chart height: {height}px, Rule: {rule_str}")
        
        return layout

    except Exception as e:
        logger.print_error(f"Error creating fast fullscreen plot: {e}")
        return None 