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
    HoverTool, Span, Title, ColumnDataSource, NumeralTickFormatter, Div, BoxAnnotation
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

        # Determine if we should show separate charts based on rule
        # Rules that should show separate charts: AUTO, PHLD, PV, SR (but NOT OHLCV)
        # All other rules (like RSI, MACD, OHLCV, etc.) should not show separate charts
        rule_str = display_rule.upper() if isinstance(display_rule, str) else str(display_rule).upper()
        show_separate_charts = any(key in rule_str for key in ['AUTO', 'PHLD', 'PREDICT_HIGH_LOW_DIRECTION', 'PV', 'PRESSURE_VECTOR', 'SR', 'SUPPORT_RESISTANTS'])
        logger.print_debug(f"Fast plot: Rule string: '{rule_str}', show_separate_charts: {show_separate_charts}")

        if show_separate_charts:
            # Volume subplot - only if data exists
            logger.print_debug(f"Fast plot: Checking Volume column - exists: {'Volume' in display_df.columns}, not all null: {not display_df['Volume'].isna().all() if 'Volume' in display_df.columns else False}")
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
            logger.print_debug(f"Fast plot: Checking pressure columns - Pressure exists: {'Pressure' in display_df.columns}, pressure exists: {'pressure' in display_df.columns}")
            pressure_col = None
            if 'Pressure' in display_df.columns and not display_df['Pressure'].isna().all():
                pressure_col = 'Pressure'
                logger.print_debug("Fast plot: Using 'Pressure' column for pressure subplot")
            elif 'pressure' in display_df.columns and not display_df['pressure'].isna().all():
                pressure_col = 'pressure'
                logger.print_debug("Fast plot: Using 'pressure' column for pressure subplot")
            
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
            logger.print_debug(f"Fast plot: Checking PV columns - PV exists: {'PV' in display_df.columns}, pressure_vector exists: {'pressure_vector' in display_df.columns}")
            pv_col = None
            if 'PV' in display_df.columns and not display_df['PV'].isna().all():
                pv_col = 'PV'
                logger.print_debug("Fast plot: Using 'PV' column for PV subplot")
            elif 'pressure_vector' in display_df.columns and not display_df['pressure_vector'].isna().all():
                pv_col = 'pressure_vector'
                logger.print_debug("Fast plot: Using 'pressure_vector' column for PV subplot")
            
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
                logger.print_debug(f"Fast plot: AUTO mode detected, checking predicted columns")
                # Predicted Low subplot
                logger.print_debug(f"Fast plot: Checking predicted_low - exists: {'predicted_low' in display_df.columns}, not all null: {not display_df['predicted_low'].isna().all() if 'predicted_low' in display_df.columns else False}")
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
                logger.print_debug(f"Fast plot: Checking predicted_high - exists: {'predicted_high' in display_df.columns}, not all null: {not display_df['predicted_high'].isna().all() if 'predicted_high' in display_df.columns else False}")
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

        # --- Modern Supertrend subplot (if present) ---
        # Check for Supertrend data in various column formats
        has_supertrend_direct = 'supertrend' in display_df.columns
        has_pprice_columns = 'PPrice1' in display_df.columns and 'PPrice2' in display_df.columns and 'Direction' in display_df.columns
        
        if has_supertrend_direct or has_pprice_columns:
            import numpy as np
            supertrend_fig = figure(
                width=width,
                height=int(height * 0.18),
                x_axis_type='datetime',
                title='SuperTrend',
                tools="pan,wheel_zoom,box_zoom,reset",
                active_scroll='wheel_zoom'
            )
            
            idx = display_df['index']
            
            if has_pprice_columns:
                # Use PPrice1/PPrice2 method (old format)
                p1 = display_df['PPrice1']
                p2 = display_df['PPrice2']
                direction = display_df['Direction']
                # Form SuperTrend line: if uptrend (direction > 0), use PPrice1, else PPrice2
                supertrend_values = np.where(direction > 0, p1, p2)
            else:
                # Use direct supertrend column
                supertrend_values = display_df['supertrend']
                direction = display_df['Direction']
            
            # Modern color scheme
            uptrend_color = '#00C851'      # Modern green
            downtrend_color = '#ff4444'    # Modern red
            neutral_color = '#FFC107'      # Golden yellow for neutral
            
            # Create segments for color segmentation
            segments = []
            
            # Safe first element access
            if hasattr(idx, 'iloc'):
                first_idx = idx.iloc[0]
                first_value = supertrend_values.iloc[0] if hasattr(supertrend_values, 'iloc') else supertrend_values[0]
                first_dir = direction.iloc[0] if hasattr(direction, 'iloc') else direction[0]
            else:
                first_idx = idx[0]
                first_value = supertrend_values[0]
                first_dir = direction[0]
            
            # Determine initial color
            if first_dir > 0:
                current_color = uptrend_color
            elif first_dir < 0:
                current_color = downtrend_color
            else:
                current_color = neutral_color
            
            current_segment = {'x': [first_idx], 'y': [first_value], 'color': current_color}
            
            # Build segments
            for i in range(1, len(idx)):
                # Safe element access
                if hasattr(direction, 'iloc'):
                    current_dir = direction.iloc[i]
                    prev_dir = direction.iloc[i-1]
                else:
                    current_dir = direction[i]
                    prev_dir = direction[i-1]
                    
                if hasattr(idx, 'iloc'):
                    current_idx = idx.iloc[i]
                    prev_idx = idx.iloc[i-1]
                else:
                    current_idx = idx[i]
                    prev_idx = idx[i-1]
                    
                if hasattr(supertrend_values, 'iloc'):
                    current_value = supertrend_values.iloc[i]
                    prev_value = supertrend_values.iloc[i-1]
                else:
                    current_value = supertrend_values[i]
                    prev_value = supertrend_values[i-1]
                
                # Determine segment color
                if current_dir > 0:
                    color = uptrend_color
                elif current_dir < 0:
                    color = downtrend_color
                else:
                    color = neutral_color
                    
                # Start new segment if direction changed
                if current_dir != prev_dir:
                    if len(current_segment['x']) > 0:
                        segments.append(current_segment)
                    current_segment = {'x': [prev_idx], 'y': [prev_value], 'color': color}
                
                current_segment['x'].append(current_idx)
                current_segment['y'].append(current_value)
            
            # Add last segment
            if len(current_segment['x']) > 0:
                segments.append(current_segment)
            
            # Draw segments with modern styling
            for segment in segments:
                if len(segment['x']) > 1:
                    # Glow effect (wide transparent line)
                    supertrend_fig.line(
                        segment['x'], segment['y'],
                        line_color=segment['color'],
                        line_width=12,
                        line_alpha=0.15
                    )
                    
                    # Main line with enhanced styling
                    supertrend_fig.line(
                        segment['x'], segment['y'],
                        line_color=segment['color'],
                        line_width=4,
                        line_alpha=0.9,
                        legend_label='SuperTrend'
                    )
            
            # Enhanced BUY/SELL signals with modern styling
            buy_signals = []
            sell_signals = []
            
            for i in range(1, len(direction)):
                # Safe element access
                if hasattr(direction, 'iloc'):
                    current_dir = direction.iloc[i]
                    prev_dir = direction.iloc[i-1]
                else:
                    current_dir = direction[i]
                    prev_dir = direction[i-1]
                    
                if hasattr(idx, 'iloc'):
                    current_idx = idx.iloc[i]
                else:
                    current_idx = idx[i]
                    
                if hasattr(supertrend_values, 'iloc'):
                    current_value = supertrend_values.iloc[i]
                else:
                    current_value = supertrend_values[i]
                
                if current_dir != prev_dir:
                    if current_dir > 0:  # BUY signal
                        buy_signals.append((current_idx, current_value))
                    else:  # SELL signal
                        sell_signals.append((current_idx, current_value))
            
            # Draw BUY signals with enhanced styling
            if buy_signals:
                buy_x, buy_y = zip(*buy_signals)
                # Glow effect for buy signals
                supertrend_fig.scatter(
                    buy_x, buy_y,
                    size=16,
                    color=uptrend_color,
                    marker='triangle',
                    alpha=0.3
                )
                # Main buy signal markers
                supertrend_fig.scatter(
                    buy_x, buy_y,
                    size=12,
                    color=uptrend_color,
                    marker='triangle',
                    alpha=0.9,
                    legend_label='BUY Signal'
                )
            
            # Draw SELL signals with enhanced styling
            if sell_signals:
                sell_x, sell_y = zip(*sell_signals)
                # Glow effect for sell signals
                supertrend_fig.scatter(
                    sell_x, sell_y,
                    size=16,
                    color=downtrend_color,
                    marker='inverted_triangle',
                    alpha=0.3
                )
                # Main sell signal markers
                supertrend_fig.scatter(
                    sell_x, sell_y,
                    size=12,
                    color=downtrend_color,
                    marker='inverted_triangle',
                    alpha=0.9,
                    legend_label='SELL Signal'
                )
            
            # Add transparent trend zones for enhanced visual appeal
            if len(idx) > 0:
                current_trend = direction.iloc[0] if hasattr(direction, 'iloc') else direction[0]
                zone_start = idx.iloc[0] if hasattr(idx, 'iloc') else idx[0]
                
                for i in range(1, len(direction)):
                    if hasattr(direction, 'iloc'):
                        current_dir = direction.iloc[i]
                        current_idx = idx.iloc[i]
                    else:
                        current_dir = direction[i]
                        current_idx = idx[i]
                        
                    if current_dir != current_trend or i == len(direction)-1:
                        zone_end = current_idx
                        zone_color = uptrend_color if current_trend > 0 else downtrend_color
                        
                        # Add transparent background zone
                        supertrend_fig.add_layout(BoxAnnotation(
                            left=zone_start, right=zone_end,
                            fill_color=zone_color, fill_alpha=0.08,
                            line_color=zone_color, line_alpha=0.2, line_width=1
                        ))
                        
                        zone_start = current_idx
                        current_trend = current_dir
            
            # Enhanced hover tool
            if has_pprice_columns:
                hover_st = HoverTool(
                    tooltips=[
                        ("Date", "@x{%F %H:%M}"),
                        ("Support (PPrice1)", "@PPrice1{0.5f}"),
                        ("Resistance (PPrice2)", "@PPrice2{0.5f}"),
                        ("Direction", "@Direction{0}")
                    ],
                    formatters={"@x": "datetime"},
                    mode='vline'
                )
            else:
                hover_st = HoverTool(
                    tooltips=[
                        ("Date", "@x{%F %H:%M}"),
                        ("SuperTrend", "@supertrend{0.5f}"),
                        ("Direction", "@Direction{0}")
                    ],
                    formatters={"@x": "datetime"},
                    mode='vline'
                )
            
            supertrend_fig.add_tools(hover_st)
            supertrend_fig.x_range = main_fig.x_range
            figures.append(supertrend_fig)

        # Layout: main chart + only those subplots for which data exists
        logger.print_debug(f"Fast plot: Creating layout with {len(figures)} figures")
        for i, fig in enumerate(figures):
            logger.print_debug(f"Fast plot: Figure {i}: {fig.title.text if hasattr(fig.title, 'text') else 'Main chart'}")
        
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
