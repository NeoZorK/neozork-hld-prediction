import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot

import pandas as pd

def plot_indicator_results_fast(
    df,
    rule,
    title='',
    output_path="results/plots/fast_plot.html",
    auto_open=True,
    **kwargs
):
    """
    Render an all-in-one dashboard plot using Plotly with the same structure as plt mode:
    - Main panel: OHLC candles, indicator lines, buy/sell markers, legend.
    - Subpanels: Volume (bar), PV, HL, Pressure.
    Saves as a single interactive HTML and opens in browser if requested.
    """
    # Ensure index column for plotly
    if 'index' not in df.columns:
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.copy()
            df['index'] = df.index
        else:
            raise ValueError("DataFrame must have datetime index or 'index' column.")
    df['index'] = pd.to_datetime(df['index'])

    # Create subplots: 1 big (candles+signals+lines), 4 small (Volume, PV, HL, Pressure)
    fig = make_subplots(
        rows=5, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.45, 0.13, 0.14, 0.14, 0.14],
        subplot_titles=[
            "Price / Signals", "Volume", "PV", "HL (Points)", "Pressure"
        ]
    )

    # --- Row 1: Candles, indicators, signals ---
    fig.add_trace(go.Candlestick(
        x=df['index'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="OHLC",
        increasing_line_color='green',
        decreasing_line_color='red',
        showlegend=True
    ), row=1, col=1)

    # Indicator lines (PPrice1, PPrice2, PV, Pressure)
    if 'PPrice1' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['index'], y=df['PPrice1'],
            mode='lines',
            name='PPrice1',
            line=dict(color='lime', width=1, dash='dot')
        ), row=1, col=1)
    if 'PPrice2' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['index'], y=df['PPrice2'],
            mode='lines',
            name='PPrice2',
            line=dict(color='red', width=1, dash='dot')
        ), row=1, col=1)
    if 'PV' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['index'], y=df['PV'],
            mode='lines',
            name='PV',
            line=dict(color='gold', width=1, dash='dash')
        ), row=1, col=1)
    if 'Pressure' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['index'], y=df['Pressure'],
            mode='lines',
            name='Pressure',
            line=dict(color='blue', width=1, dash='solid')
        ), row=1, col=1)

    # Buy/Sell signals (Direction: 1=buy, 2=sell)
    if 'Direction' in df.columns:
        buy_mask = df['Direction'] == 1
        sell_mask = df['Direction'] == 2
        fig.add_trace(go.Scatter(
            x=df.loc[buy_mask, 'index'],
            y=df.loc[buy_mask, 'Low'],
            mode='markers',
            marker=dict(symbol='triangle-up', size=12, color='lime'),
            name='BUY Signal',
            showlegend=True
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=df.loc[sell_mask, 'index'],
            y=df.loc[sell_mask, 'High'],
            mode='markers',
            marker=dict(symbol='triangle-down', size=12, color='red'),
            name='SELL Signal',
            showlegend=True
        ), row=1, col=1)

    # --- Row 2: Volume (bar) ---
    if 'Volume' in df.columns:
        fig.add_trace(go.Bar(
            x=df['index'],
            y=df['Volume'],
            name='Volume',
            marker=dict(color='grey'),
            opacity=0.7,
            showlegend=False
        ), row=2, col=1)

    # --- Row 3: PV (line, zero baseline) ---
    if 'PV' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['index'], y=df['PV'],
            mode='lines+markers',
            name='PV',
            line=dict(color='orange'),
            marker=dict(size=5),
            showlegend=False
        ), row=3, col=1)
        # zero baseline
        fig.add_trace(go.Scatter(
            x=[df['index'].min(), df['index'].max()],
            y=[0, 0],
            mode='lines',
            line=dict(color='gray', width=1, dash='dash'),
            showlegend=False,
            hoverinfo='skip'
        ), row=3, col=1)

    # --- Row 4: HL (Points) ---
    if 'HL' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['index'],
            y=df['HL'],
            mode='lines+markers',
            name='HL (Points)',
            line=dict(color='brown'),
            marker=dict(size=5),
            showlegend=False
        ), row=4, col=1)

    # --- Row 5: Pressure ---
    if 'Pressure' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['index'],
            y=df['Pressure'],
            mode='lines+markers',
            name='Pressure',
            line=dict(color='blue'),
            marker=dict(size=5),
            showlegend=False
        ), row=5, col=1)
        # zero baseline
        fig.add_trace(go.Scatter(
            x=[df['index'].min(), df['index'].max()],
            y=[0, 0],
            mode='lines',
            line=dict(color='gray', width=1, dash='dash'),
            showlegend=False,
            hoverinfo='skip'
        ), row=5, col=1)

    # Layout and axis formatting
    fig.update_layout(
        title=title,
        template='plotly_white',
        height=1200,
        xaxis5=dict(title='Date'),  # Only bottom x axis title
        legend=dict(orientation='v', x=1.01, y=1),
        margin=dict(t=80, r=30, b=40, l=60)
    )
    for i in range(2, 6):
        fig.update_yaxes(showgrid=True, row=i, col=1)
    fig.update_xaxes(showgrid=True, row=5, col=1)

    # Save and open file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plot(fig, filename=output_path, auto_open=auto_open)