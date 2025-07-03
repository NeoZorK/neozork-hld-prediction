# -*- coding: utf-8 -*-
# src/plotting/dual_chart_fastest.py

"""
Dual chart plotting for fastest mode using Plotly + Dask + Datashader.
Creates a main OHLC chart with buy/sell signals and support/resistance lines,
plus a secondary chart below showing the selected indicator.
"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import webbrowser
from typing import Dict, Any, Optional

from ..common import logger


def plot_dual_chart_fastest(
    df: pd.DataFrame,
    rule: str,
    title: str = '',
    output_path: Optional[str] = None,
    width: int = 1800,
    height: int = 1100,
    layout: Optional[Dict[str, Any]] = None,
    **kwargs
) -> go.Figure:
    """
    Create dual chart plot using Plotly for fastest mode.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data and calculated indicators
        rule (str): Rule string (e.g., 'rsi:14,30,70,open')
        title (str): Plot title
        output_path (str, optional): Output file path
        width (int): Plot width
        height (int): Plot height
        layout (dict, optional): Layout configuration
        **kwargs: Additional arguments
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Set default output path
    if output_path is None:
        output_path = "results/plots/dual_chart_fastest.html"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Standardize column names
    display_df = df.copy()
    display_df.columns = [col.lower() for col in display_df.columns]
    
    # Ensure we have required columns
    required_columns = ['open', 'high', 'low', 'close']
    missing_columns = [col for col in required_columns if col not in display_df.columns]
    if missing_columns:
        logger.print_error(f"Missing required columns: {missing_columns}")
        return None
    
    # Create subplots: main chart (60%) and indicator chart (40%)
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(None, None),  # Без заголовков внутри графика
        vertical_spacing=0.04,
        row_heights=[0.62, 0.38],
        specs=[[{"secondary_y": False}],
               [{"secondary_y": False}]]
    )
    
    # Add candlestick chart to main subplot
    fig.add_trace(
        go.Candlestick(
            x=display_df.index,
            open=display_df['open'],
            high=display_df['high'],
            low=display_df['low'],
            close=display_df['close'],
            name="OHLC",
            increasing_line_color='#2ecc71',
            decreasing_line_color='#e74c3c',
            increasing_fillcolor='#2ecc71',
            decreasing_fillcolor='#e74c3c',
            line=dict(width=1.2)
        ),
        row=1, col=1
    )
    
    # Add support and resistance lines if available
    if 'support' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['support'],
                mode='lines',
                name='Support',
                line=dict(color='#3498db', width=2, dash='dash'),
                opacity=0.7
            ),
            row=1, col=1
        )
    
    if 'resistance' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['resistance'],
                mode='lines',
                name='Resistance',
                line=dict(color='#e67e22', width=2, dash='dash'),
                opacity=0.7
            ),
            row=1, col=1
        )
    
    # Add buy/sell signals if available
    if 'direction' in display_df.columns:
        buy_signals = display_df[display_df['direction'] == 1]
        sell_signals = display_df[display_df['direction'] == 2]
        
        if not buy_signals.empty:
            fig.add_trace(
                go.Scatter(
                    x=buy_signals.index,
                    y=buy_signals['low'] * 0.995,  # Position below the low
                    mode='markers',
                    name='Buy Signal',
                    marker=dict(
                        symbol='triangle-up',
                        size=10,
                        color='#27ae60',
                        line=dict(color='#229954', width=1.5)
                    ),
                    showlegend=True
                ),
                row=1, col=1
            )
        
        if not sell_signals.empty:
            fig.add_trace(
                go.Scatter(
                    x=sell_signals.index,
                    y=sell_signals['high'] * 1.005,  # Position above the high
                    mode='markers',
                    name='Sell Signal',
                    marker=dict(
                        symbol='triangle-down',
                        size=10,
                        color='#c0392b',
                        line=dict(color='#a93226', width=1.5)
                    ),
                    showlegend=True
                ),
                row=1, col=1
            )
    
    # Add indicator to secondary subplot based on rule
    indicator_name = rule.split(':', 1)[0].lower().strip()
    
    if indicator_name == 'rsi':
        if 'rsi' in display_df.columns:
            # Add RSI line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['rsi'],
                    mode='lines',
                    name='RSI',
                    line=dict(color='purple', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            # Add overbought/oversold lines
            if 'rsi_overbought' in display_df.columns:
                overbought = display_df['rsi_overbought'].iloc[0]
                fig.add_trace(
                    go.Scatter(
                        x=display_df.index,
                        y=[overbought] * len(display_df),
                        mode='lines',
                        name=f'Overbought ({overbought})',
                        line=dict(color='red', width=2, dash='dash'),
                        showlegend=False
                    ),
                    row=2, col=1
                )
            
            if 'rsi_oversold' in display_df.columns:
                oversold = display_df['rsi_oversold'].iloc[0]
                fig.add_trace(
                    go.Scatter(
                        x=display_df.index,
                        y=[oversold] * len(display_df),
                        mode='lines',
                        name=f'Oversold ({oversold})',
                        line=dict(color='green', width=2, dash='dash'),
                        showlegend=False
                    ),
                    row=2, col=1
                )
    
    elif indicator_name == 'macd':
        if 'macd' in display_df.columns:
            # Add MACD line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['macd'],
                    mode='lines',
                    name='MACD',
                    line=dict(color='blue', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        if 'macd_signal' in display_df.columns:
            # Add Signal line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['macd_signal'],
                    mode='lines',
                    name='Signal',
                    line=dict(color='red', width=2),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        if 'macd_histogram' in display_df.columns:
            # Add Histogram
            colors = ['green' if val >= 0 else 'red' for val in display_df['macd_histogram']]
            fig.add_trace(
                go.Bar(
                    x=display_df.index,
                    y=display_df['macd_histogram'],
                    name='Histogram',
                    marker_color=colors,
                    opacity=0.7,
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'ema':
        if 'ema' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['ema'],
                    mode='lines',
                    name='EMA',
                    line=dict(color='orange', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'bb':
        if 'bb_upper' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['bb_upper'],
                    mode='lines',
                    name='Upper Band',
                    line=dict(color='blue', width=2),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        if 'bb_middle' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['bb_middle'],
                    mode='lines',
                    name='Middle Band',
                    line=dict(color='gray', width=2),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        if 'bb_lower' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['bb_lower'],
                    mode='lines',
                    name='Lower Band',
                    line=dict(color='blue', width=2),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'atr':
        if 'atr' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['atr'],
                    mode='lines',
                    name='ATR',
                    line=dict(color='brown', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'cci':
        if 'cci' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['cci'],
                    mode='lines',
                    name='CCI',
                    line=dict(color='purple', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            # Add CCI reference lines
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[100] * len(display_df),
                    mode='lines',
                    name='CCI +100',
                    line=dict(color='red', width=1, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[-100] * len(display_df),
                    mode='lines',
                    name='CCI -100',
                    line=dict(color='green', width=1, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'vwap':
        if 'vwap' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['vwap'],
                    mode='lines',
                    name='VWAP',
                    line=dict(color='orange', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'pivot':
        if 'pivot' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['pivot'],
                    mode='lines',
                    name='Pivot',
                    line=dict(color='blue', width=2),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        if 'r1' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['r1'],
                    mode='lines',
                    name='R1',
                    line=dict(color='red', width=1, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        if 's1' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['s1'],
                    mode='lines',
                    name='S1',
                    line=dict(color='green', width=1, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'hma':
        if 'hma' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['hma'],
                    mode='lines',
                    name='HMA',
                    line=dict(color='purple', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'tsf':
        if 'tsf' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['tsf'],
                    mode='lines',
                    name='TSF',
                    line=dict(color='cyan', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'monte':
        if 'monte_expected_return' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['monte_expected_return'],
                    mode='lines',
                    name='Expected Return',
                    line=dict(color='blue', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'kelly':
        if 'kelly' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['kelly'],
                    mode='lines',
                    name='Kelly',
                    line=dict(color='green', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'donchain':
        if 'donchain_upper' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['donchain_upper'],
                    mode='lines',
                    name='Upper Channel',
                    line=dict(color='blue', width=2),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        if 'donchain_middle' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['donchain_middle'],
                    mode='lines',
                    name='Middle Channel',
                    line=dict(color='gray', width=2),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        if 'donchain_lower' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['donchain_lower'],
                    mode='lines',
                    name='Lower Channel',
                    line=dict(color='blue', width=2),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'fibo':
        # Add Fibonacci levels
        fibo_cols = [col for col in display_df.columns if col.startswith('fibo_')]
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
        
        for i, col in enumerate(fibo_cols):
            color = colors[i % len(colors)]
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df[col],
                    mode='lines',
                    name=col.replace('fibo_', 'Fib '),
                    line=dict(color=color, width=2),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'obv':
        if 'obv' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['obv'],
                    mode='lines',
                    name='OBV',
                    line=dict(color='brown', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'stdev':
        if 'stdev' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['stdev'],
                    mode='lines',
                    name='StdDev',
                    line=dict(color='gray', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'adx':
        if 'adx' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['adx'],
                    mode='lines',
                    name='ADX',
                    line=dict(color='purple', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        if 'di_plus' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['di_plus'],
                    mode='lines',
                    name='DI+',
                    line=dict(color='green', width=2),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        if 'di_minus' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['di_minus'],
                    mode='lines',
                    name='DI-',
                    line=dict(color='red', width=2),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    elif indicator_name == 'sar':
        if 'sar' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['sar'],
                    mode='markers',
                    name='SAR',
                    marker=dict(
                        symbol='circle',
                        size=4,
                        color='red'
                    ),
                    showlegend=False
                ),
                row=2, col=1
            )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            font=dict(size=15, color='#2c3e50'),
            pad=dict(t=2, b=2)
        ),
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
    
    # Update axes
    # Main chart (price)
    fig.update_yaxes(
        title_text="Price", 
        row=1, 
        col=1, 
        tickformat=".4f",
        title_font=dict(size=12, color='#2c3e50'),
        tickfont=dict(size=10, color='#34495e'),
        gridcolor='#ecf0f1',
        zeroline=False
    )
    fig.update_xaxes(
        row=1, col=1,
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
        nticks=30,  # Максимум делений
        rangeslider=dict(visible=False),  # Полностью убираем
    )
    
    # Indicator chart
    indicator_title = layout['indicator_name'] if layout else 'Indicator'
    fig.update_yaxes(
        title_text=indicator_title, 
        row=2, 
        col=1,
        title_font=dict(size=12, color='#2c3e50'),
        tickfont=dict(size=10, color='#34495e'),
        gridcolor='#ecf0f1',
        zeroline=False
    )
    
    # Детализированная временная шкала для нижней диаграммы
    fig.update_xaxes(
        row=2, col=1,
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
        nticks=30,  # Максимум делений
        rangeslider=dict(visible=False),  # Полностью убираем
    )
    

    
    # Set proper time scale for both charts
    x_min = display_df.index.min()
    x_max = display_df.index.max()
    
    for i in range(1, 3):
        fig.update_xaxes(
            row=i,
            col=1,
            range=[x_min, x_max],
            type='date'
        )
    
    # Save and open
    pio.write_html(fig, output_path, auto_open=False)
    abs_path = os.path.abspath(output_path)
    webbrowser.open_new_tab(f"file://{abs_path}")
    
    logger.print_info(f"Dual chart saved to: {abs_path}")
    
    return fig 