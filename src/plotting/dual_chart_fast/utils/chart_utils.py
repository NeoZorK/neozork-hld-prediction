# -*- coding: utf-8 -*-
# src/plotting/dual_chart_fast/utils/chart_utils.py

"""
Utility functions for dual chart fast plotting.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Dict, Any, Optional
import os

from src.common import logger


def _create_discontinuous_line_segments(x_data, y_data, mask):
    """
    Create discontinuous line segments for plotting.
    
    Args:
        x_data: X-axis data
        y_data: Y-axis data
        mask: Boolean mask for continuous segments
    
    Returns:
        List of line segments
    """
    segments = []
    current_segment = []
    
    for i, is_continuous in enumerate(mask):
        if is_continuous:
            current_segment.append((x_data[i], y_data[i]))
        else:
            if current_segment:
                segments.append(current_segment)
                current_segment = []
    
    # Add the last segment if it exists
    if current_segment:
        segments.append(current_segment)
    
    return segments


def get_screen_height():
    """
    Get screen height for dynamic chart sizing.
    
    Returns:
        int: Screen height in pixels
    """
    try:
        import tkinter as tk
        root = tk.Tk()
        screen_height = root.winfo_screenheight()
        root.destroy()
        return screen_height
    except:
        # Fallback to default height
        return 1080


def calculate_dynamic_height(screen_height=None, rule_str=None):
    """
    Calculate dynamic height for chart based on screen size and rule.
    
    Args:
        screen_height: Screen height in pixels
        rule_str: Trading rule string
    
    Returns:
        int: Calculated chart height
    """
    if screen_height is None:
        screen_height = get_screen_height()
    
    # Base height calculation
    base_height = int(screen_height * 0.8)
    
    # Adjust based on rule complexity
    if rule_str:
        rule_lower = rule_str.lower()
        if 'wave' in rule_lower or 'monte' in rule_lower:
            # Complex indicators need more space
            base_height = int(base_height * 1.2)
        elif 'rsi' in rule_lower or 'macd' in rule_lower:
            # Standard indicators
            base_height = int(base_height * 1.0)
        else:
            # Simple indicators
            base_height = int(base_height * 0.9)
    
    # Ensure minimum and maximum heights
    min_height = 600
    max_height = 1200
    
    return max(min_height, min(base_height, max_height))


def setup_chart_layout(fig, title, height=800):
    """
    Setup chart layout with proper styling.
    
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
        logger.print_error(f"Error setting up chart layout: {e}")


def add_ohlc_candlesticks(fig, df, row=1, col=1):
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


def add_volume_bars(fig, df, row=1, col=1):
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


def add_trading_signals(fig, df, row=1, col=1):
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


def add_support_resistance_lines(fig, df, row=1, col=1):
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


def add_pressure_vector(fig, df, row=1, col=1):
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


def save_and_open_chart(fig, filename="dual_chart_fast.html"):
    """
    Save chart to HTML file and open in browser.
    
    Args:
        fig: Plotly figure
        filename: Output filename
    """
    try:
        import webbrowser
        
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


def _get_indicator_hover_tool(indicator_name, display_df, fibo_columns=None):
    """
    Get hover tool information for indicator.
    
    Args:
        indicator_name: Name of the indicator
        display_df: DataFrame with data
        fibo_columns: Fibonacci columns for special handling
    
    Returns:
        str: Hover tool information
    """
    try:
        if indicator_name.lower() == 'fibonacci' and fibo_columns:
            # Special handling for Fibonacci
            hover_info = []
            for col in fibo_columns:
                if col in display_df.columns:
                    hover_info.append(f"{col}: %{{y:.4f}}")
            return "<br>".join(hover_info)
        else:
            # Standard hover info
            return f"{indicator_name}: %{{y:.4f}}"
    except Exception as e:
        logger.print_error(f"Error getting hover tool info: {e}")
        return f"{indicator_name}: %{{y:.4f}}"
