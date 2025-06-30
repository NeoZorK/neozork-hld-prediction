# -*- coding: utf-8 -*-
# src/plotting/fast_plot.py
#
# Fast plotting routines for indicator dashboard visualization using Bokeh.
# Author: NeoZorK (https://github.com/neozork)
# This module provides a fast dashboard plot for OHLC financial data and indicator signals.
# It is intended for use in research and quick result visualization, not for production trading.
# All plotting functions are designed for Python 3.x and require Bokeh, Pandas, and related scientific libraries.

import os
import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column
from bokeh.models import (
    HoverTool, Span, Title, ColumnDataSource, NumeralTickFormatter, Div
)
import webbrowser
from src.common import logger

def plot_indicator_results_fast(
    df,
    rule,
    title='',
    output_path=None,
    width=1800,
    height=1100,
    mode="fast",
    data_source="demo",
    lot_size=1.0,
    risk_reward_ratio=2.0,
    fee_per_trade=0.07,
    **kwargs
):
    """
    Draws fast mode dashboard plot using Bokeh for interactive visualization.

    Features:
    - Uses Bokeh for interactive web-based visualization
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

        # Set default output path if None
        if output_path is None:
            output_path = "results/plots/fast_plot.html"
            logger.print_info(f"No output path provided, using default: {output_path}")

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

        # Create main figure for OHLC chart
        main_fig = figure(
            width=width,
            height=int(height * 0.4),
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

        # Volume subplot - only if data exists
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

        # Pressure subplot - only if data exists
        if 'Pressure' in display_df.columns and not display_df['Pressure'].isna().all():
            pressure_fig = figure(
                width=width,
                height=int(height * 0.15),
                x_axis_type='datetime',
                title='Pressure',
                tools="pan,wheel_zoom,box_zoom,reset",
                active_scroll='wheel_zoom'
            )
            pressure_fig.line('index', 'Pressure', source=source, line_color='teal', line_width=2, legend_label='Pressure')
            hover_pressure = HoverTool(tooltips=[("Date", "@index{%F %H:%M}"), ("Pressure", "@Pressure{0.3f}")], formatters={'@index': 'datetime'}, mode='vline')
            pressure_fig.add_tools(hover_pressure)
            pressure_fig.x_range = main_fig.x_range
            figures.append(pressure_fig)

        # PV subplot - only if data exists
        if 'PV' in display_df.columns and not display_df['PV'].isna().all():
            pv_fig = figure(
                width=width,
                height=int(height * 0.15),
                x_axis_type='datetime',
                title='Pressure Vector (PV)',
                tools="pan,wheel_zoom,box_zoom,reset",
                active_scroll='wheel_zoom'
            )
            pv_fig.line('index', 'PV', source=source, line_color='orange', line_width=2, legend_label='PV')
            hover_pv = HoverTool(tooltips=[("Date", "@index{%F %H:%M}"), ("PV", "@PV{0.3f}")], formatters={'@index': 'datetime'}, mode='vline')
            pv_fig.add_tools(hover_pv)
            pv_fig.x_range = main_fig.x_range
            figures.append(pv_fig)

        # Layout: main chart + only those subplots for which data exists
        layout = column(*figures)

        # Save and open
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        output_file(output_path, title=title)
        save(layout)
        abs_path = os.path.abspath(output_path)
        webbrowser.open_new_tab(f"file://{abs_path}")

        logger.print_success(f"Fast plot saved to: {output_path}")
        return layout

    except Exception as e:
        logger.print_error(f"Error creating fast plot: {e}")
        return None
