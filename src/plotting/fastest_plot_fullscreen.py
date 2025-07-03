# -*- coding: utf-8 -*-
# src/plotting/fastest_plot_fullscreen.py

"""
Fastest plot with dynamic fullscreen height for OHLCV rule.
This module provides a specialized plotting function for the command:
uv run run_analysis.py show csv mn1 -d fastest --rule OHLCV

The chart height is dynamically calculated to use the full screen height.
"""

import os
import pandas as pd
import numpy as np
import dask.dataframe as dd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datashader as ds
import datashader.transfer_functions as tf
from datashader.colors import Greys9
import colorcet as cc
import plotly.io as pio
import webbrowser
from functools import partial
import re
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
    
    Args:
        screen_height (int): Screen height in pixels
        rule_str (str): Rule string (e.g., 'OHLCV', 'AUTO')
        
    Returns:
        int: Calculated chart height
    """
    if screen_height is None:
        screen_height = get_screen_height()
    
    # For OHLCV rule, use most of the screen height
    if rule_str and rule_str.upper() == 'OHLCV':
        # Use 90% of screen height for OHLCV rule
        dynamic_height = int(screen_height * 0.9)
        # Ensure minimum and maximum bounds
        dynamic_height = max(800, min(dynamic_height, 2000))
        logger.print_info(f"OHLCV rule detected: using dynamic height {dynamic_height}px (screen height: {screen_height}px)")
        return dynamic_height
    
    # For other rules, use standard calculation
    return 1100


def plot_indicator_results_fastest_fullscreen(
    df,
    rule,
    title='',
    output_path="results/plots/fastest_plot_fullscreen.html",
    width=1800,
    height=None,
    mode="fastest",
    data_source="demo",
    **kwargs
):
    """
    Draws fastest mode dashboard plot with dynamic fullscreen height for OHLCV rule.
    
    This function is specifically optimized for the command:
    uv run run_analysis.py show csv mn1 -d fastest --rule OHLCV
    
    Features:
    - Uses Dask for lazy data processing to minimize memory usage
    - Leverages Datashader for efficient downsampling and rendering of dense data
    - Integrates with Plotly for interactive visualization
    - Dynamic height calculation for fullscreen display
    - Maintains the same visual structure as other plotting modes

    Layout:
    - The trading rule is displayed at the very top above the figure
    - Main panel: OHLC bars with predicted high/low lines and direction indicators
    - Subpanels: Volume, PV, HL, Pressure - each with its hover information
    - All panels are adaptive in size
    - Interactive hover tooltips are available across all panels
    - Opens plot in default browser after saving
    """
    # Define standard columns
    standard_columns = ['Open', 'High', 'Low', 'Close', 'Volume',
                       'index', 'datetime', 'DateTime', 'Timestamp', 'Date', 'Time',
                       'HL', 'PV', 'Pressure', 'Direction']
    standard_columns = [col.lower() for col in standard_columns]

    # Convert to dask dataframe if not already
    if isinstance(df, pd.DataFrame):
        ddf = dd.from_pandas(df, npartitions=max(1, min(os.cpu_count(), len(df) // 10000)))
    else:
        ddf = df  # Assume it's already a dask dataframe

    # Standardize column names
    display_df = df.copy()
    display_df.columns = [col.lower() for col in display_df.columns]

    # Ensure we have the required columns
    required_columns = ['open', 'high', 'low', 'close']
    missing_columns = [col for col in required_columns if col not in display_df.columns]
    if missing_columns:
        logger.print_error(f"Missing required columns: {missing_columns}")
        return None

    # Determine if we should show separate charts based on rule
    # Rules that should show separate charts: OHLCV, AUTO, PHLD, PV, SR
    # All other rules (like RSI, MACD, etc.) should not show separate charts
    rule_str = rule.name.upper() if hasattr(rule, 'name') else str(rule).upper()
    show_separate_charts = rule_str in ['OHLCV', 'AUTO', 'PHLD', 'PREDICT_HIGH_LOW_DIRECTION', 'PV', 'PRESSURE_VECTOR', 'SR', 'SUPPORT_RESISTANTS']

    # Calculate dynamic height based on rule
    if height is None:
        height = calculate_dynamic_height(rule_str=rule_str)
    
    logger.print_info(f"Using dynamic height: {height}px for rule: {rule_str}")

    if show_separate_charts:
        # Create subplots with separate charts
        if rule_str == 'AUTO':
            subplot_titles = ('Price Chart', '', 'Volume', '', 'Indicators', 'Predicted High/Low')
        else:
            subplot_titles = ('Price Chart', '', 'Volume', '', 'Indicators', '')
        
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=subplot_titles,
            vertical_spacing=0.05,
            horizontal_spacing=0.02,
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
    else:
        # Create subplots with only main chart
        fig = make_subplots(
            rows=1, cols=1,
            subplot_titles=('Price Chart',),
            vertical_spacing=0.05,
            horizontal_spacing=0.02
        )

    # Add candlestick chart
    # Use index if available, otherwise use DataFrame index
    x_data = display_df['index'] if 'index' in display_df.columns else display_df.index
    
    fig.add_trace(
        go.Candlestick(
            x=x_data,
            open=display_df['open'],
            high=display_df['high'],
            low=display_df['low'],
            close=display_df['close'],
            name="OHLC"
        ),
        row=1, col=1
    )

    # Add predicted high/low lines if they exist (only for non-AUTO rules)
    if rule_str != 'AUTO':
        for col in ['predicted_high', 'predicted_low']:
            if col in display_df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=x_data,
                        y=display_df[col],
                        mode='lines',
                        name=col.replace('_', ' ').title(),
                        line=dict(
                            color='blue' if col == 'predicted_high' else 'red',
                            width=1.5
                        )
                    ),
                    row=1, col=1
                )

    # Add volume (only if separate charts are enabled)
    if show_separate_charts and 'volume' in display_df.columns:
        # Use direction-based colors if direction column exists, otherwise use default color
        if 'direction' in display_df.columns:
            colors = ['green' if val else 'red' for val in display_df['direction']]
        else:
            colors = 'rgba(100, 100, 100, 0.5)'  # Default gray color
        
        fig.add_trace(
            go.Bar(
                x=x_data,
                y=display_df['volume'],
                marker_color=colors,
                name="Volume",
                opacity=0.7
            ),
            row=2, col=1
        )

    # Add other indicators (HL, PV, Pressure) to the third panel (only if separate charts are enabled)
    if show_separate_charts:
        indicator_colors = {
            'HL': 'purple',
            'PV': 'orange',
            'Pressure': 'teal',
            'pressure': 'teal',
            'pressure_vector': 'orange'
        }

        for indicator, color in indicator_colors.items():
            if indicator in display_df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=x_data,
                        y=display_df[indicator],
                        mode='lines',
                        name=indicator,
                        line=dict(color=color, width=1.5)
                    ),
                    row=3, col=1
                )

        # Add predicted high/low as separate panels for AUTO mode
        if rule_str == 'AUTO':
            # Predicted Low subplot
            if 'predicted_low' in display_df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=x_data,
                        y=display_df['predicted_low'],
                        mode='lines',
                        name='Predicted Low',
                        line=dict(color='green', width=2)
                    ),
                    row=3, col=2
                )

            # Predicted High subplot
            if 'predicted_high' in display_df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=x_data,
                        y=display_df['predicted_high'],
                        mode='lines',
                        name='Predicted High',
                        line=dict(color='red', width=2)
                    ),
                    row=3, col=2
                )

    # Add rule annotation
    # Check if we have original rule with parameters for display
    if hasattr(rule, 'original_rule_with_params'):
        display_rule = rule.original_rule_with_params
    elif hasattr(rule, 'name'):
        display_rule = rule.name
    else:
        display_rule = str(rule)

    # Update layout with dynamic height
    fig.update_layout(
        title=title,
        height=height,  # Use dynamic height
        autosize=True,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.01,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#bdc3c7',
            borderwidth=1,
            font=dict(size=11)
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=10,
            bordercolor='#bdc3c7'
        ),
        margin=dict(t=24, b=14, l=28, r=4),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Set axis ranges
    y_stats = display_df[['open', 'high', 'low', 'close']].describe()
    min_price = y_stats.loc['min'].min() * 0.998
    max_price = y_stats.loc['max'].max() * 1.002
    fig.update_yaxes(title_text="Price", row=1, col=1, tickformat=".5f", range=[min_price, max_price])

    if show_separate_charts:
        if 'volume' in display_df.columns:
            vol_max = display_df['volume'].max() * 1.1
            fig.update_yaxes(title_text="Volume", row=2, col=1, range=[0, vol_max])

        # Set proper time scale for all charts
        x_min = x_data.min()
        x_max = x_data.max()
        for i in range(1, 4):
            fig.update_xaxes(
                row=i,
                col=1,
                range=[x_min, x_max],
                type='date',
                tickformat="%b %d, %Y",  # Jan 15, 1993
                tickangle=0,
                ticklabelmode="period",
                showgrid=True,
                gridcolor="#f0f0f0",
                ticks="outside",
                ticklen=6,
                tickcolor="#b0b0b0",
                tickwidth=1.2,
                showline=True,
                linecolor="#b0b0b0",
                mirror=True,
                automargin=True,
                nticks=30,  # Maximum divisions
                rangeslider=dict(visible=False),  # Completely remove
            )

        # Show time labels only on the bottom chart
        for i in range(1, 3):
            fig.update_xaxes(row=i, col=1, showticklabels=False)
    else:
        # Set proper time scale for single chart
        x_min = x_data.min()
        x_max = x_data.max()
        fig.update_xaxes(
            row=1,
            col=1,
            range=[x_min, x_max],
            type='date',
            tickformat="%b %d, %Y",  # Jan 15, 1993
            tickangle=0,
            ticklabelmode="period",
            showgrid=True,
            gridcolor="#f0f0f0",
            ticks="outside",
            ticklen=6,
            tickcolor="#b0b0b0",
            tickwidth=1.2,
            showline=True,
            linecolor="#b0b0b0",
            mirror=True,
            automargin=True,
            nticks=30,  # Maximum divisions
            rangeslider=dict(visible=False),  # Completely remove
        )

    # Save and open
    pio.write_html(fig, output_path, auto_open=False)
    abs_path = os.path.abspath(output_path)
    webbrowser.open_new_tab(f"file://{abs_path}")
    
    logger.print_success(f"Fullscreen fastest plot saved to: {output_path}")
    logger.print_info(f"Chart height: {height}px, Rule: {rule_str}")
    
    return fig 