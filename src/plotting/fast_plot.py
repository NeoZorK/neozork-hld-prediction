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

def plot_indicator_results_fast(
    df,
    rule,
    title='',
    output_path=None,
    width=1800,
    height=1100,
    mode="fast",
    data_source="demo",
    **kwargs
):
    """
    Draws fast mode dashboard plot using Bokeh.
    - The trading rule is displayed at the very top above the figure.
    - Main panel: OHLC bars, open/close ticks (fixed pixel length), open/close points, predicted high/low lines, direction arrows, legend, interactive tooltips.
    - Subpanels: Volume, PV, HL, Pressure - each with its own hover tooltip.
    - All panels are adaptive in size with right margin for scrollbar.
    - Tooltip in 'csv' (parquet) mode is concise and not duplicated.
    - Opens plot in default browser after saving.
    """
    # Create output filename based on input data and parameters
    if output_path is None:
        # Extract source file name from the original filename
        source_name = None
        if 'filename' in kwargs and kwargs['filename']:
            # Use the actual filename from the source file
            source_name = kwargs['filename']
            # Remove file extension if present
            if '.' in source_name:
                source_name = source_name.rsplit('.', 1)[0]
        elif hasattr(df, 'name') and df.name:
            source_name = df.name

        # Use data_source as fallback if source_name is still None
        if not source_name:
            # If we're using CSV data, try to extract the ticker from data_source
            if data_source.startswith('csv_'):
                source_name = data_source.replace('csv_', '')
            elif data_source == "demo":
                # Try to find file name in kwargs or from other sources
                if 'show_args' in kwargs and kwargs['show_args']:
                    # Get full file name from show_args
                    arg = kwargs['show_args'][0] if isinstance(kwargs['show_args'], list) and kwargs['show_args'] else "GBPUSD"
                    # Check if we need to add the CSVExport_ prefix
                    if not arg.startswith("CSVExport_") and not "_PERIOD_" in arg:
                        source_name = f"CSVExport_{arg}_PERIOD_MN1"
                    else:
                        source_name = arg
                elif 'source' in kwargs and kwargs['source']:
                    # Get full file name from source
                    source = kwargs['source']
                    if not source.startswith("CSVExport_") and not "_PERIOD_" in source:
                        source_name = f"CSVExport_{source}_PERIOD_MN1"
                    else:
                        source_name = source
                else:
                    # Default to full GBPUSD file name if no other source is found
                    source_name = "CSVExport_GBPUSD_PERIOD_MN1"
            else:
                source_name = data_source

        # Extract timeframe from original filename
        timeframe = "MN1"  # default to MN1 as requested
        if 'filename' in kwargs and 'PERIOD_' in kwargs['filename']:
            # Extract timeframe from filename like CSVExport_GBPUSD_PERIOD_MN1
            parts = kwargs['filename'].split('PERIOD_')
            if len(parts) > 1 and parts[1]:
                # Get timeframe part before next underscore or dot
                timeframe_part = parts[1].split('_')[0].split('.')[0]
                if timeframe_part:
                    timeframe = timeframe_part

        # Format rule name
        rule_name = rule
        if hasattr(rule, 'name'):
            rule_name = rule.name

        # Create filename following the pattern: source_timeframe_rule_mode.html
        output_path = f"results/plots/{source_name}_{timeframe}_{rule_name}_fast.html"

    # Check if we're in OHLCV mode (when rule is 'OHLCV' or 'Raw_OHLCV_Data')
    is_ohlcv_mode = (hasattr(rule, 'name') and rule.name == 'OHLCV') or \
                   (isinstance(rule, str) and rule in ['Raw_OHLCV_Data', 'OHLCV'])

    # Ensure the index column exists and is datetime type
    if 'index' not in df.columns:
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.copy()
            df['index'] = df.index
        else:
            raise ValueError("DataFrame must have datetime index or 'index' column.")
    df['index'] = pd.to_datetime(df['index'])

    # Compute direction for coloring bars
    df['direction'] = (df['Close'] >= df['Open'])

    # Prepare color columns for open/close ticks
    df['open_tick_color'] = "green"
    df['close_tick_color'] = "red"

    # Calculate tick offsets for open/close ticks
    if len(df) > 1:
        approx_bar_width = (df['index'].iloc[1] - df['index'].iloc[0]).total_seconds() * 1000
    else:
        approx_bar_width = 12 * 60 * 60 * 1000
    tick_ms = approx_bar_width // 3

    # Calculate columns for open/close tick segment coordinates
    df['open_tick_x0'] = df['index'] - pd.to_timedelta(tick_ms, unit='ms')
    df['open_tick_x1'] = df['index']
    df['open_tick_y0'] = df['Open']
    df['open_tick_y1'] = df['Open']

    df['close_tick_x0'] = df['index']
    df['close_tick_x1'] = df['index'] + pd.to_timedelta(tick_ms, unit='ms')
    df['close_tick_y0'] = df['Close']
    df['close_tick_y1'] = df['Close']

    # Prepare ColumnDataSource for interactive tooltips
    source = ColumnDataSource(df)

    # === TRADING RULE HEADER ===
    trading_rule_div = Div(
        text=f"<b style='font-size:18pt;color:#2e5cb8;text-align:center;display:block;'>Trading Rule: {rule}</b>",
        width=width, height=40
    )

    # === MAIN PANEL (PRICE & SIGNALS) ===
    p_main = figure(
        width=width, height=int(height*0.48),
        x_axis_type="datetime", title=title,
        background_fill_color="#f5f7fa",
        sizing_mode="stretch_width",
        margin=(10, 80, 10, 60)
    )
    p_main.yaxis.axis_label = "Price"
    p_main.yaxis.formatter = NumeralTickFormatter(format="0.00000")

    # Draw OHLC bar (vertical segment)
    ohlc_segment = p_main.segment(
        x0='index', y0='High', x1='index', y1='Low',
        color="black", line_width=1.5, source=source, legend_label="OHLC Bar"
    )

    # Draw open tick (left) using only column names with source
    p_main.segment(
        x0='open_tick_x0',
        y0='open_tick_y0',
        x1='open_tick_x1',
        y1='open_tick_y1',
        color='open_tick_color',
        line_width=3,
        legend_label="Open",
        source=source
    )

    # Draw close tick (right) using only column names with source
    p_main.segment(
        x0='close_tick_x0',
        y0='close_tick_y0',
        x1='close_tick_x1',
        y1='close_tick_y1',
        color='close_tick_color',
        line_width=3,
        legend_label="Close",
        source=source
    )

    # Draw open and close points as circles for clarity
    p_main.scatter(
        x='index',
        y='Open',
        marker="circle",
        size=7,
        color="green",
        source=source,
        alpha=0.7
    )
    p_main.scatter(
        x='index',
        y='Close',
        marker="circle",
        size=7,
        color="red",
        source=source,
        alpha=0.7
    )

    # Draw predicted high/low lines and direction arrows only if not in OHLCV mode
    if not is_ohlcv_mode:
        # Draw predicted high/low lines
        if 'PPrice1' in df.columns:
            p_main.line('index', 'PPrice1', line_color='green', line_dash='dotted', line_width=2, legend_label="Predicted Low (PPrice1)", source=source)
        if 'PPrice2' in df.columns:
            p_main.line('index', 'PPrice2', line_color='red', line_dash='dotted', line_width=2, legend_label="Predicted High (PPrice2)", source=source)

        # Draw predicted direction arrows
        if 'Direction' in df.columns:
            buy_idx = df['Direction'] == 1
            sell_idx = df['Direction'] == 2
            # Up arrows for predicted up
            p_main.scatter(
                x=df.loc[buy_idx, 'index'],
                y=df.loc[buy_idx, 'Low'] - (df['High'] - df['Low']).mean() * 0.08,
                size=16, color="lime", marker="triangle", legend_label="Predicted UP", alpha=0.9
            )
            # Down arrows for predicted down
            p_main.scatter(
                x=df.loc[sell_idx, 'index'],
                y=df.loc[sell_idx, 'High'] + (df['High'] - df['Low']).mean() * 0.08,
                size=16, color="red", marker="inverted_triangle", legend_label="Predicted DOWN", alpha=0.9
            )

    # Overlay legend
    p_main.legend.location = "top_left"
    p_main.legend.click_policy = "hide"
    p_main.legend.label_text_font_size = "13pt"

    # Add chart subtitle
    subtitle = Title(
        text="Fast Mode: OHLC bars, open/close points, predicted lines/arrows, indicators",
        align="center", text_font_size="11pt"
    )
    p_main.add_layout(subtitle, 'above')

    # ================== TOOLTIP CONFIG ===================================
    # For parquet/csv, short tooltip (no repeats)
    if data_source == "csv":
        tooltip_fields = [
            ("Date", "@index{%F}"),
            ("Open", "@Open{0.5f}"),
            ("High", "@High{0.5f}"),
            ("Low", "@Low{0.5f}"),
            ("Close", "@Close{0.5f}"),
            ("Volume", "@Volume{0}"),
            ("HL", "@HL{0.5f}"),
            ("Pressure", "@Pressure{0.5f}"),
            ("PV", "@PV{0.5f}")
        ]
    else:
        tooltip_fields = [
            ("Date", "@index{%F}"),
            ("Open", "@Open{0.5f}"),
            ("High", "@High{0.5f}"),
            ("Low", "@Low{0.5f}"),
            ("Close", "@Close{0.5f}"),
            ("PPrice1", "@PPrice1{0.5f}"),
            ("PPrice2", "@PPrice2{0.5f}"),
            ("Direction", "@Direction"),
            ("Pressure", "@Pressure{0.5f}"),
            ("PV", "@PV{0.5f}"),
            ("HL", "@HL{0.5f}"),
            ("Volume", "@Volume{0}")
        ]

    hover_main = HoverTool(
        renderers=[ohlc_segment],
        tooltips=tooltip_fields,
        formatters={"@index": "datetime"},
        mode='vline'
    )
    p_main.add_tools(hover_main)
    # ======================================================================

    # === VOLUME PANEL ===
    p_vol = figure(
        width=width, height=int(height*0.13), x_axis_type="datetime",
        x_range=p_main.x_range, background_fill_color="#f5f7fa",
        sizing_mode="stretch_width", margin=(5, 80, 5, 60)
    )
    p_vol.yaxis.axis_label = "Volume"
    vbar_vol = None
    if 'Volume' in df.columns:
        vbar_vol = p_vol.vbar(x='index', top='Volume', width=approx_bar_width//2 if 'approx_bar_width' in locals() else 1000000, color="#888888", alpha=0.55, legend_label="Volume", source=source)
        p_vol.legend.location = "top_left"
        p_vol.legend.label_text_font_size = "10pt"
    if vbar_vol:
        hover_vol = HoverTool(
            renderers=[vbar_vol],
            tooltips=[
                ("Date", "@index{%F}"),
                ("Volume", "@Volume{0}")
            ],
            formatters={"@index": "datetime"},
            mode='vline'
        )
        p_vol.add_tools(hover_vol)

    # Create indicator panels only if not in OHLCV mode
    p_pv = None
    p_hl = None
    p_pressure = None

    if not is_ohlcv_mode:
        # === PV PANEL ===
        p_pv = figure(
            width=width, height=int(height*0.13), x_axis_type="datetime",
            x_range=p_main.x_range, background_fill_color="#f5f7fa",
            sizing_mode="stretch_width", margin=(5, 80, 5, 60)
        )
        p_pv.yaxis.axis_label = "PV"
        p_pv.yaxis.formatter = NumeralTickFormatter(format="0.00000")
        line_pv = None
        if 'PV' in df.columns:
            line_pv = p_pv.line('index', 'PV', color="orange", line_width=2, legend_label="PV", source=source)
            zero = Span(location=0, dimension='width', line_color='gray', line_dash='dashed', line_width=1)
            p_pv.add_layout(zero)
            p_pv.legend.location = "top_left"
            p_pv.legend.label_text_font_size = "10pt"
        if line_pv:
            hover_pv = HoverTool(
                renderers=[line_pv],
                tooltips=[
                    ("Date", "@index{%F}"),
                    ("PV", "@PV{0.5f}")
                ],
                formatters={"@index": "datetime"},
                mode='vline'
            )
            p_pv.add_tools(hover_pv)

        # === HL PANEL ===
        p_hl = figure(
            width=width, height=int(height*0.13), x_axis_type="datetime",
            x_range=p_main.x_range, background_fill_color="#f5f7fa",
            sizing_mode="stretch_width", margin=(5, 80, 5, 60)
        )
        p_hl.yaxis.axis_label = "HL (Points)"
        p_hl.yaxis.formatter = NumeralTickFormatter(format="0.00000")
        line_hl = None
        if 'HL' in df.columns:
            line_hl = p_hl.line('index', 'HL', color="brown", line_width=2, legend_label="HL (Points)", source=source)
            p_hl.legend.location = "top_left"
            p_hl.legend.label_text_font_size = "10pt"
        if line_hl:
            hover_hl = HoverTool(
                renderers=[line_hl],
                tooltips=[
                    ("Date", "@index{%F}"),
                    ("HL", "@HL{0.5f}")
                ],
                formatters={"@index": "datetime"},
                mode='vline'
            )
            p_hl.add_tools(hover_hl)

        # === PRESSURE PANEL ===
        p_pressure = figure(
            width=width, height=int(height*0.13), x_axis_type="datetime",
            x_range=p_main.x_range, background_fill_color="#f5f7fa",
            sizing_mode="stretch_width", margin=(5, 80, 10, 60)
        )
        p_pressure.yaxis.axis_label = "Pressure"
        p_pressure.yaxis.formatter = NumeralTickFormatter(format="0.00000")
        line_pressure = None
        if 'Pressure' in df.columns:
            line_pressure = p_pressure.line('index', 'Pressure', color="blue", line_width=2, legend_label="Pressure", source=source)
            zero2 = Span(location=0, dimension='width', line_color='gray', line_dash='dashed', line_width=1)
            p_pressure.add_layout(zero2)
            p_pressure.legend.location = "top_left"
            p_pressure.legend.label_text_font_size = "10pt"
        if line_pressure:
            hover_pressure = HoverTool(
                renderers=[line_pressure],
                tooltips=[
                    ("Date", "@index{%F}"),
                    ("Pressure", "@Pressure{0.5f}")
                ],
                formatters={"@index": "datetime"},
                mode='vline'
            )
            p_pressure.add_tools(hover_pressure)

    # === COMBINE AND SAVE ===
    # Construct layout based on mode (OHLCV or indicator)
    if is_ohlcv_mode:
        # In OHLCV mode, only include main panel and volume
        layout = column(
            trading_rule_div,
            p_main,
            p_vol if 'Volume' in df.columns else None,
            sizing_mode="stretch_width"
        )
    else:
        # In indicator mode, include all panels
        layout = column(
            trading_rule_div,
            p_main,
            p_vol,
            p_pv,
            p_hl,
            p_pressure,
            sizing_mode="stretch_width"
        )

    # Update subtitle text based on mode
    if is_ohlcv_mode:
        subtitle.text = "Fast Mode: OHLCV bars, open/close points"
    else:
        subtitle.text = "Fast Mode: OHLC bars, open/close points, predicted lines/arrows, indicators"

    # Update tooltip for OHLCV mode - show only OHLCV data
    if is_ohlcv_mode:
        tooltip_fields = [
            ("Date", "@index{%F}"),
            ("Open", "@Open{0.5f}"),
            ("High", "@High{0.5f}"),
            ("Low", "@Low{0.5f}"),
            ("Close", "@Close{0.5f}"),
            ("Volume", "@Volume{0}")
        ]
        hover_main.tooltips = tooltip_fields

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output_file(output_path, title=title)
    save(layout)
    abs_path = os.path.abspath(output_path)
    webbrowser.open_new_tab(f"file://{abs_path}")
