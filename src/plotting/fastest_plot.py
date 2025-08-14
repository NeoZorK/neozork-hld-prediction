# -*- coding: utf-8 -*-
# src/plotting/fastest_plot.py

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

def plot_indicator_results_fastest(
    df,
    rule,
    title='',
    output_path="results/plots/fastest_plot.html",
    width=1800,
    height=1100,
    mode="fastest",
    data_source="demo",
    **kwargs
):
    """
    Draws fastest mode dashboard plot using Plotly + Dask + Datashader for extremely large datasets.

    Features:
    - Uses Dask for lazy data processing to minimize memory usage
    - Leverages Datashader for efficient downsampling and rendering of dense data
    - Integrates with Plotly for interactive visualization
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
    # Rules that should show separate charts: OHLCV, AUTO, PHLD, PV, SR, SCHR_DIR
    # All other rules (like RSI, MACD, etc.) should not show separate charts
    rule_str = rule.name.upper() if hasattr(rule, 'name') else str(rule).upper()
    show_separate_charts = rule_str in ['OHLCV', 'AUTO', 'PHLD', 'PREDICT_HIGH_LOW_DIRECTION', 'PV', 'PRESSURE_VECTOR', 'SR', 'SUPPORT_RESISTANTS', 'SCHR_DIR']

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
    fig.add_trace(
        go.Candlestick(
            x=display_df['index'],
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
        # Check for PPrice1/PPrice2 columns (used by SCHR_DIR and other indicators)
        if 'pprice1' in display_df.columns and 'pprice2' in display_df.columns:
            # Add PPrice1 (Predicted Low)
            fig.add_trace(
                go.Scatter(
                    x=display_df['index'],
                    y=display_df['pprice1'],
                    mode='lines',
                    name='Predicted Low (PPrice1)',
                    line=dict(color='green', width=1.5)
                ),
                row=1, col=1
            )
            # Add PPrice2 (Predicted High)
            fig.add_trace(
                go.Scatter(
                    x=display_df['index'],
                    y=display_df['pprice2'],
                    mode='lines',
                    name='Predicted High (PPrice2)',
                    line=dict(color='red', width=1.5)
                ),
                row=1, col=1
            )
        else:
            # Fallback to old predicted_high/predicted_low columns
            for col in ['predicted_high', 'predicted_low']:
                if col in display_df.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=display_df['index'],
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
        colors = ['green' if val else 'red' for val in display_df['direction']]
        fig.add_trace(
            go.Bar(
                x=display_df['index'],
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
                        x=display_df['index'],
                        y=display_df[indicator],
                        mode='lines',
                        name=indicator,
                        line=dict(color=color, width=1.5)
                    ),
                    row=3, col=1
                )

        # Add predicted high/low as separate panels for AUTO mode
        if rule_str == 'AUTO':
            # Check for PPrice1/PPrice2 columns first (used by SCHR_DIR and other indicators)
            if 'pprice1' in display_df.columns and 'pprice2' in display_df.columns:
                # Predicted Low subplot (PPrice1)
                fig.add_trace(
                    go.Scatter(
                        x=display_df['index'],
                        y=display_df['pprice1'],
                        mode='lines',
                        name='Predicted Low (PPrice1)',
                        line=dict(color='green', width=2)
                    ),
                    row=3, col=2
                )

                # Predicted High subplot (PPrice2)
                fig.add_trace(
                    go.Scatter(
                        x=display_df['index'],
                        y=display_df['pprice2'],
                        mode='lines',
                        name='Predicted High (PPrice2)',
                        line=dict(color='red', width=2)
                    ),
                    row=3, col=2
                )
            else:
                # Fallback to old predicted_high/predicted_low columns
                # Predicted Low subplot
                if 'predicted_low' in display_df.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=display_df['index'],
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
                            x=display_df['index'],
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

    fig.update_layout(
        title=title,
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
        x_min = display_df['index'].min()
        x_max = display_df['index'].max()
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
        x_min = display_df['index'].min()
        x_max = display_df['index'].max()
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
    return fig

def render_large_dataset(ddf, canvas_width=1000, x_field='index', y_field='Close'):
    """
    Helper function to efficiently render large datasets using datashader.

    Args:
        ddf (dask.dataframe.DataFrame): The Dask DataFrame containing the data to render
        canvas_width (int): Width of the canvas in pixels. Default is 1000.
        x_field (str): The column name to use for the x-axis. Default is 'index'.
        y_field (str): The column name to use for the y-axis. Default is 'Close'.

    Returns:
        numpy.ndarray: A rendered image array that can be used with Plotly
    """
    # Define a canvas for rendering
    canvas = ds.Canvas(plot_width=canvas_width)

    # Compute the aggregation
    agg = canvas.line(ddf, x_field, y_field)

    # Shade the aggregation using a color map
    img = tf.shade(agg, cmap=cc.fire)

    # Convert to numpy array for Plotly
    return np.array(img.to_pil())
