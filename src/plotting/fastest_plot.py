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
    # Create a directory for output if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Convert to dask dataframe if not already
    if isinstance(df, pd.DataFrame):
        ddf = dd.from_pandas(df, npartitions=max(1, min(os.cpu_count(), len(df) // 10000)))
    else:
        ddf = df  # Assume it's already a dask dataframe

    # Ensure the index column exists and is datetime type
    if 'index' not in ddf.columns:
        if isinstance(ddf.index, pd.DatetimeIndex):
            ddf = ddf.reset_index()
            ddf = ddf.rename(columns={'index': 'date'})
            ddf['index'] = ddf['date']
        else:
            raise ValueError("DataFrame must have datetime index or 'index' column.")

    # Compute basic statistics to determine plot ranges (minimizing compute operations)
    y_stats = ddf[['Open', 'High', 'Low', 'Close']].describe().compute()
    min_price = y_stats.loc['min'].min() * 0.998
    max_price = y_stats.loc['max'].max() * 1.002

    # Compute a subset of data if very large (for initial visualization)
    if len(ddf) > 50000:
        # Sample data for initial display
        display_df = ddf.sample(frac=min(1.0, 50000/len(ddf)), random_state=42).compute()
        # Sort by index for proper display
        display_df = display_df.sort_values('index')
    else:
        display_df = ddf.compute()

    # Compute direction for coloring
    display_df = display_df.copy()  # Ensure no view warning
    display_df.loc[:, 'direction'] = (display_df['Close'] >= display_df['Open'])
    display_df.loc[:, 'increasing'] = display_df['direction']
    display_df.loc[:, 'decreasing'] = ~display_df['direction']

    # Create subplots layout
    fig = make_subplots(
        rows=5,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.48, 0.13, 0.13, 0.13, 0.13],
        subplot_titles=["OHLC Chart", "Volume", "PV", "HL (Points)", "Pressure"]
    )

    # Main OHLC chart
    fig.add_trace(
        go.Candlestick(
            x=display_df['index'],
            open=display_df['Open'],
            high=display_df['High'],
            low=display_df['Low'],
            close=display_df['Close'],
            name="OHLC",
            increasing_line_color='green',
            decreasing_line_color='red'
        ),
        row=1, col=1
    )

    # Add predicted high/low lines if present
    if 'PPrice1' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df['index'],
                y=display_df['PPrice1'],
                mode='lines',
                name="Predicted Low (PPrice1)",
                line=dict(color='green', dash='dot', width=2)
            ),
            row=1, col=1
        )

    if 'PPrice2' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df['index'],
                y=display_df['PPrice2'],
                mode='lines',
                name="Predicted High (PPrice2)",
                line=dict(color='red', dash='dot', width=2)
            ),
            row=1, col=1
        )

    # Add direction arrows if present
    if 'Direction' in display_df.columns:
        buy_idx = display_df['Direction'] == 1
        sell_idx = display_df['Direction'] == 2

        if any(buy_idx):
            avg_range = (display_df['High'] - display_df['Low']).mean() * 0.08
            fig.add_trace(
                go.Scatter(
                    x=display_df.loc[buy_idx, 'index'],
                    y=display_df.loc[buy_idx, 'Low'] - avg_range,
                    mode='markers',
                    marker=dict(symbol='triangle-up', size=12, color='lime'),
                    name="Predicted UP"
                ),
                row=1, col=1
            )

        if any(sell_idx):
            avg_range = (display_df['High'] - display_df['Low']).mean() * 0.08
            fig.add_trace(
                go.Scatter(
                    x=display_df.loc[sell_idx, 'index'],
                    y=display_df.loc[sell_idx, 'High'] + avg_range,
                    mode='markers',
                    marker=dict(symbol='triangle-down', size=12, color='red'),
                    name="Predicted DOWN"
                ),
                row=1, col=1
            )

    # Volume panel
    if 'Volume' in display_df.columns:
        # Use datashader to efficiently render large volume data
        if len(display_df) > 10000:
            # Create canvas
            cvs = ds.Canvas(plot_width=width, plot_height=int(height*0.13))
            # Aggregate volume data
            agg = cvs.line(display_df, 'index', 'Volume')
            # Convert to image
            img = tf.shade(agg, cmap=Greys9[::-1])
            # Convert to numpy array for plotly
            img_arr = np.array(img.to_pil())

            # Add as an image
            fig.add_trace(
                go.Image(
                    z=img_arr,
                    x0=display_df['index'].min(),
                    y0=0,
                    dx=(display_df['index'].max() - display_df['index'].min()) / img_arr.shape[1],
                    dy=display_df['Volume'].max() / img_arr.shape[0],
                    name="Volume"
                ),
                row=2, col=1
            )
        else:
            # For smaller datasets, use regular bar chart
            colors = ['#7E7E7E' if val else '#7E7E7E' for val in display_df['direction']]
            fig.add_trace(
                go.Bar(
                    x=display_df['index'],
                    y=display_df['Volume'],
                    marker_color=colors,
                    name="Volume",
                    opacity=0.7
                ),
                row=2, col=1
            )

    # PV panel
    if 'PV' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df['index'],
                y=display_df['PV'],
                mode='lines',
                name="PV",
                line=dict(color='orange', width=2)
            ),
            row=3, col=1
        )
        # Add zero line
        fig.add_shape(
            type="line",
            x0=display_df['index'].min(),
            y0=0,
            x1=display_df['index'].max(),
            y1=0,
            line=dict(color="gray", width=1, dash="dash"),
            row=3, col=1
        )

    # HL panel
    if 'HL' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df['index'],
                y=display_df['HL'],
                mode='lines',
                name="HL (Points)",
                line=dict(color='brown', width=2)
            ),
            row=4, col=1
        )

    # Pressure panel
    if 'Pressure' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df['index'],
                y=display_df['Pressure'],
                mode='lines',
                name="Pressure",
                line=dict(color='blue', width=2)
            ),
            row=5, col=1
        )
        # Add zero line
        fig.add_shape(
            type="line",
            x0=display_df['index'].min(),
            y0=0,
            x1=display_df['index'].max(),
            y1=0,
            line=dict(color="gray", width=1, dash="dash"),
            row=5, col=1
        )

    # Add Trading Rule text at top
    fig.add_annotation(
        text=f"Trading Rule: {rule}",
        xref="paper", yref="paper",
        x=0.5, y=1.05,
        showarrow=False,
        font=dict(size=18, color="#2e5cb8"),
        align="center",
    )

    # Add subtitle about the fastest mode
    fig.add_annotation(
        text="Fastest Mode: Plotly + Dask + Datashader for large datasets",
        xref="paper", yref="paper",
        x=0.5, y=1.02,
        showarrow=False,
        font=dict(size=12),
        align="center",
    )

    # Update layout for better appearance
    fig.update_layout(
        title=title,
        width=width,
        height=height,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=12
        ),
        margin=dict(t=100, b=10)
    )

    # Set y-axis formats and ranges
    fig.update_yaxes(title_text="Price", row=1, col=1, tickformat=".5f", range=[min_price, max_price])

    if 'Volume' in display_df.columns:
        vol_max = display_df['Volume'].max() * 1.1
        fig.update_yaxes(title_text="Volume", row=2, col=1, range=[0, vol_max])

    if 'PV' in display_df.columns:
        pv_min = min(0, display_df['PV'].min() * 1.1)
        pv_max = max(0, display_df['PV'].max() * 1.1)
        fig.update_yaxes(title_text="PV", row=3, col=1, tickformat=".5f", range=[pv_min, pv_max])

    if 'HL' in display_df.columns:
        hl_min = display_df['HL'].min() * 1.1
        hl_max = display_df['HL'].max() * 1.1
        fig.update_yaxes(title_text="HL (Points)", row=4, col=1, tickformat=".5f", range=[hl_min, hl_max])

    if 'Pressure' in display_df.columns:
        pressure_min = min(0, display_df['Pressure'].min() * 1.1)
        pressure_max = max(0, display_df['Pressure'].max() * 1.1)
        fig.update_yaxes(title_text="Pressure", row=5, col=1, tickformat=".5f", range=[pressure_min, pressure_max])

    # Do not set hovertemplate for candlestick, as it's not supported
    # To customize hover, consider using hovertext/hoverinfo if needed

    # Save the figure to HTML
    pio.write_html(fig, output_path, auto_open=False)

    # Open the plot in the default browser
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
    # Function implementation would go here
    pass