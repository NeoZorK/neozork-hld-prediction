# -*- coding: utf-8 -*-
# src/plotting/dual_chart_fastest/utils/chart_utils.py

"""
Utility functions for dual chart fastest plotting.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Dict, Any, Optional

from src.common import logger


def create_discontinuous_line_traces(x_data, y_data, mask, name, color, width=2, showlegend=True):
    """
    Create discontinuous line traces for plotting.
    
    Args:
        x_data: X-axis data
        y_data: Y-axis data
        mask: Boolean mask for continuous segments
        name: Trace name
        color: Line color
        width: Line width
        showlegend: Whether to show in legend
    
    Returns:
        List of trace objects
    """
    traces = []
    
    # Find continuous segments
    segments = []
    current_segment = []
    
    for i, is_continuous in enumerate(mask):
        if is_continuous:
            current_segment.append(i)
        else:
            if current_segment:
                segments.append(current_segment)
                current_segment = []
    
    # Add the last segment if it exists
    if current_segment:
        segments.append(current_segment)
    
    # Create traces for each segment
    for i, segment in enumerate(segments):
        if len(segment) > 1:  # Only create trace if segment has more than one point
            segment_x = [x_data[j] for j in segment]
            segment_y = [y_data[j] for j in segment]
            
            trace = go.Scatter(
                x=segment_x,
                y=segment_y,
                mode='lines',
                name=name if i == 0 else None,  # Only show name for first segment
                line=dict(color=color, width=width),
                showlegend=showlegend and i == 0,
                connectgaps=False
            )
            traces.append(trace)
    
    return traces


def add_ohlc_candlesticks(fig: go.Figure, df: pd.DataFrame, row: int = 1, col: int = 1) -> None:
    """
    Add OHLC candlestick chart to figure.
    
    Args:
        fig: Plotly figure
        df: DataFrame with OHLC data
        row: Subplot row
        col: Subplot column
    """
    try:
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='OHLC',
                showlegend=False
            ),
            row=row, col=col
        )
    except Exception as e:
        logger.print_error(f"Error adding OHLC candlesticks: {e}")


def add_volume_bars(fig: go.Figure, df: pd.DataFrame, row: int = 1, col: int = 1) -> None:
    """
    Add volume bars to figure.
    
    Args:
        fig: Plotly figure
        df: DataFrame with volume data
        row: Subplot row
        col: Subplot column
    """
    try:
        if 'volume' in df.columns:
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df['volume'],
                    name='Volume',
                    marker_color='rgba(158,202,225,0.6)',
                    showlegend=False
                ),
                row=row, col=col
            )
    except Exception as e:
        logger.print_error(f"Error adding volume bars: {e}")


def add_trading_signals(fig: go.Figure, df: pd.DataFrame, row: int = 1, col: int = 1) -> None:
    """
    Add trading signals to figure.
    
    Args:
        fig: Plotly figure
        df: DataFrame with trading signals
        row: Subplot row
        col: Subplot column
    """
    try:
        # Add buy signals
        if 'phld_signal' in df.columns:
            buy_signals = df[df['phld_signal'] == 'BUY']
            if not buy_signals.empty:
                fig.add_trace(
                    go.Scatter(
                        x=buy_signals.index,
                        y=buy_signals['close'],
                        mode='markers',
                        marker=dict(
                            symbol='triangle-up',
                            size=12,
                            color='green',
                            line=dict(width=2, color='darkgreen')
                        ),
                        name='Buy Signal',
                        showlegend=False
                    ),
                    row=row, col=col
                )
        
        # Add sell signals
        if 'phld_signal' in df.columns:
            sell_signals = df[df['phld_signal'] == 'SELL']
            if not sell_signals.empty:
                fig.add_trace(
                    go.Scatter(
                        x=sell_signals.index,
                        y=sell_signals['close'],
                        mode='markers',
                        marker=dict(
                            symbol='triangle-down',
                            size=12,
                            color='red',
                            line=dict(width=2, color='darkred')
                        ),
                        name='Sell Signal',
                        showlegend=False
                    ),
                    row=row, col=col
                )
    except Exception as e:
        logger.print_error(f"Error adding trading signals: {e}")


def add_support_resistance_lines(fig: go.Figure, df: pd.DataFrame, row: int = 1, col: int = 1) -> None:
    """
    Add support and resistance lines to figure.
    
    Args:
        fig: Plotly figure
        df: DataFrame with support/resistance data
        row: Subplot row
        col: Subplot column
    """
    try:
        # Add support lines
        if 'support' in df.columns:
            support_values = df['support'].dropna()
            if not support_values.empty:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['support'],
                        mode='lines',
                        name='Support',
                        line=dict(color='green', width=2, dash='dash'),
                        showlegend=False
                    ),
                    row=row, col=col
                )
        
        # Add resistance lines
        if 'resistance' in df.columns:
            resistance_values = df['resistance'].dropna()
            if not resistance_values.empty:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['resistance'],
                        mode='lines',
                        name='Resistance',
                        line=dict(color='red', width=2, dash='dash'),
                        showlegend=False
                    ),
                    row=row, col=col
                )
    except Exception as e:
        logger.print_error(f"Error adding support/resistance lines: {e}")


def add_pressure_vector(fig: go.Figure, df: pd.DataFrame, row: int = 1, col: int = 1) -> None:
    """
    Add pressure vector to figure.
    
    Args:
        fig: Plotly figure
        df: DataFrame with pressure vector data
        row: Subplot row
        col: Subplot column
    """
    try:
        if 'pressure_vector' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['pressure_vector'],
                    mode='lines',
                    name='Pressure Vector',
                    line=dict(color='cyan', width=2),
                    showlegend=False
                ),
                row=row, col=col
            )
    except Exception as e:
        logger.print_error(f"Error adding pressure vector: {e}")


def setup_figure_layout(fig: go.Figure, title: str, height: int = 800) -> None:
    """
    Setup figure layout.
    
    Args:
        fig: Plotly figure
        title: Chart title
        height: Chart height
    """
    try:
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                font=dict(size=16, color='white')
            ),
            height=height,
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True
            ),
            xaxis2=dict(
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True
            ),
            yaxis2=dict(
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True
            )
        )
    except Exception as e:
        logger.print_error(f"Error setting up figure layout: {e}")


def save_and_open_chart(fig: go.Figure, filename: str = "dual_chart_fastest.html") -> None:
    """
    Save chart to HTML file and open in browser.
    
    Args:
        fig: Plotly figure
        filename: Output filename
    """
    try:
        import webbrowser
        import os
        
        # Create output directory if it doesn't exist
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filepath = os.path.join(output_dir, filename)
        
        # Save the figure
        fig.write_html(filepath)
        
        # Open in browser
        webbrowser.open(f"file://{os.path.abspath(filepath)}")
        
        logger.print_success(f"Chart saved to: {filepath}")
        
    except Exception as e:
        logger.print_error(f"Error saving and opening chart: {e}")
