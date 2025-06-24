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
from src.plotting.metrics_display import add_metrics_to_plotly_chart
from src.common import logger
from src.calculation.trading_metrics import calculate_trading_metrics

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

    # Ensure the index column exists and is datetime type
    if 'index' not in ddf.columns:
        if isinstance(ddf.index, pd.DatetimeIndex):
            ddf = ddf.reset_index()
            ddf = ddf.rename(columns={'index': 'date'})
            ddf['index'] = ddf['date']
        else:
            raise ValueError("DataFrame must have datetime index or 'index' column.")

    # Compute a subset of data if very large (for initial visualization)
    if len(ddf) > 50000:
        display_df = ddf.sample(frac=min(1.0, 50000/len(ddf)), random_state=42).compute()
        display_df = display_df.sort_values('index')
    else:
        display_df = ddf.compute()

    # Compute direction for coloring
    display_df = display_df.copy()
    display_df.loc[:, 'direction'] = (display_df['Close'] >= display_df['Open'])
    display_df.loc[:, 'increasing'] = display_df['direction']
    display_df.loc[:, 'decreasing'] = ~display_df['direction']

    # Создаём 2 колонки: график (col=1), метрики (col=2)
    fig = make_subplots(
        rows=3, cols=2,
        column_widths=[0.8, 0.2],
        shared_xaxes=True,
        vertical_spacing=0.03,
        horizontal_spacing=0.05,
        row_heights=[0.6, 0.2, 0.2],
        subplot_titles=["OHLC Chart", "", "Volume", "", "Indicators", ""]
    )

    # Add OHLC candlestick chart
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

    # Add predicted high/low lines if they exist
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

    # Add volume
    if 'Volume' in display_df.columns:
        colors = ['green' if val else 'red' for val in display_df['direction']]
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

    # Add other indicators (HL, PV, Pressure) to the third panel
    indicator_colors = {
        'HL': 'purple',
        'PV': 'orange',
        'Pressure': 'teal'
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

    # Add rule annotation
    fig.add_annotation(
        text=f"Trading Rule: {rule}",
        xref="paper", yref="paper",
        x=0.5, y=1.05,
        showarrow=False,
        font=dict(size=18, color="#2e5cb8"),
        align="center",
    )

    # === Метрики в отдельной колонке справа (col=2, row=1) ===
    if 'Direction' in display_df.columns:
        metrics = calculate_trading_metrics(display_df,
            lot_size=kwargs.get('lot_size', 1.0),
            risk_reward_ratio=kwargs.get('risk_reward_ratio', 2.0),
            fee_per_trade=kwargs.get('fee_per_trade', 0.07))
        def color(val, good=0.7, warn=0.4):
            try:
                v = float(str(val).replace('%',''))
                if v >= good*100: return '#2ecc40'
                if v >= warn*100: return '#e67e22'
                return '#e74c3c'
            except: return '#222'
        metrics_html = f'''
<div style="margin:40px auto 0 auto;max-width:900px;padding:18px 28px 18px 28px;
            background: #f8f9fa; border-radius: 12px; border: 1.5px solid #e0e0e0;
            font-family: 'Segoe UI', Arial, sans-serif; font-size: 17px; color: #222;">
  <h2 style="margin-top:0;margin-bottom:12px;font-size:1.5em;">
    📊 <span style="color:#2e5cb8;">Trading Metrics</span>
  </h2>
  <div style="display:flex;flex-wrap:wrap;gap:18px 32px;">
    <div>🟢 <b>Buy Signals:</b> {metrics.get('buy_count',0)}</div>
    <div>🔴 <b>Sell Signals:</b> {metrics.get('sell_count',0)}</div>
    <div>📈 <b>Total Trades:</b> {metrics.get('total_trades',0)}</div>
    <div>🎯 <b>Win Ratio:</b> <span style="color:{color(metrics.get('win_ratio',0)/100)};">{metrics.get('win_ratio',0):.1f}%</span></div>
    <div>💰 <b>Profit Factor:</b> <span style="color:{color(metrics.get('profit_factor',0)/2)};">{metrics.get('profit_factor',0):.2f}</span></div>
    <div>📊 <b>Sharpe Ratio:</b> <span style="color:{color(metrics.get('sharpe_ratio',0)/2)};">{metrics.get('sharpe_ratio',0):.2f}</span></div>
    <div>⚖️ <b>Risk/Reward:</b> {metrics.get('risk_reward_setting',0):.2f}</div>
    <div>💸 <b>Fee per Trade:</b> {metrics.get('fee_per_trade',0):.2f}%</div>
    <div>🎯 <b>Kelly Fraction:</b> {metrics.get('kelly_fraction',0):.3f}</div>
    <div>💰 <b>Net Return:</b> <span style="color:{color(metrics.get('net_return',0)/100)};">{metrics.get('net_return',0):.2f}%</span></div>
    <div>🛡️ <b>Strategy Sustainability:</b> <span style="color:{color(metrics.get('strategy_sustainability',0)/100)};">{metrics.get('strategy_sustainability',0):.1f}%</span></div>
  </div>
</div>
'''
        with open(output_path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = html.replace('</body>', metrics_html + '\n</body>')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
    # Отключить оси для колонки метрик
    for r in [1,2,3]:
        fig.update_xaxes(visible=False, row=r, col=2)
        fig.update_yaxes(visible=False, row=r, col=2)

    # Update layout
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

    # Set axis ranges
    y_stats = display_df[['Open', 'High', 'Low', 'Close']].describe()
    min_price = y_stats.loc['min'].min() * 0.998
    max_price = y_stats.loc['max'].max() * 1.002
    fig.update_yaxes(title_text="Price", row=1, col=1, tickformat=".5f", range=[min_price, max_price])

    if 'Volume' in display_df.columns:
        vol_max = display_df['Volume'].max() * 1.1
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
            tickformat='%Y-%m-%d %H:%M',
            tickangle=45
        )

    # Show time labels only on the bottom chart
    for i in range(1, 3):
        fig.update_xaxes(row=i, col=1, showticklabels=False)

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
