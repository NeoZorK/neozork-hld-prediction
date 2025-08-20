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

from src.common import logger


def add_rsi_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add RSI indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with RSI data
    """
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


def add_rsi_momentum_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add RSI Momentum indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with RSI and RSI Momentum data
    """
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
    
    if 'rsi_momentum' in display_df.columns:
        # Add RSI Momentum line
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['rsi_momentum'],
                mode='lines',
                name='RSI Momentum',
                line=dict(color='orange', width=2),
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Add zero line for momentum
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=[0] * len(display_df),
                mode='lines',
                name='Zero Line',
                line=dict(color='gray', width=1, dash='dash'),
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


def add_macd_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add MACD indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with MACD data
    """
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


def add_ema_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add EMA indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with EMA data
    """
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


def add_sma_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add SMA indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with SMA data
    """
    if 'sma' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['sma'],
                mode='lines',
                name='SMA',
                line=dict(color='blue', width=3),
                showlegend=False
            ),
            row=2, col=1
        )

def create_discontinuous_line_traces(x_data, y_data, mask, name, color, width=2, showlegend=True):
    """
    Create line traces that are discontinuous where mask is False.
    This prevents interpolation between points where there are no signals.
    
    Args:
        x_data: X-axis data (index)
        y_data: Y-axis data (values)
        mask: Boolean mask indicating where to draw lines
        name: Name for the trace
        color: Line color
        width: Line width
        showlegend: Whether to show in legend
    
    Returns:
        List of traces
    """
    traces = []
    
    if not mask.any():
        return traces
    
    # Convert mask to numpy array for easier processing
    mask_array = mask.values
    
    # Find continuous segments where mask is True
    # Use numpy diff to find transitions
    transitions = np.diff(np.concatenate(([False], mask_array, [False])).astype(int))
    starts = np.where(transitions == 1)[0]  # Transitions from False to True
    ends = np.where(transitions == -1)[0] - 1  # Transitions from True to False (adjust index)
    
    # Create traces for each continuous segment
    for i, (start_idx, end_idx) in enumerate(zip(starts, ends)):
        if start_idx <= end_idx:  # Valid segment
            # Handle both Series and Index for x_data
            if hasattr(x_data, 'iloc'):
                segment_x = x_data.iloc[start_idx:end_idx+1]
            else:
                segment_x = x_data[start_idx:end_idx+1]
            
            # y_data should always be a Series
            segment_y = y_data.iloc[start_idx:end_idx+1]
            
            # Only create trace if we have at least one point
            if len(segment_x) > 0:
                # Only show legend for first segment to avoid duplicates
                trace_name = name if i == 0 else None
                trace_showlegend = showlegend if i == 0 else False
                
                traces.append(go.Scatter(
                    x=segment_x,
                    y=segment_y,
                    mode='lines',
                    name=trace_name,
                    line=dict(color=color, width=width),
                    showlegend=trace_showlegend,
                    hoverinfo='skip' if not showlegend else None
                ))
    
    return traces


def add_wave_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Wave indicator to the secondary subplot.

    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Wave data
    """
    # Add Plot Wave (main indicator, single line with dynamic colors) - as per MQ5
    plot_wave_col = None
    plot_color_col = None
    if '_plot_wave' in display_df.columns:
        plot_wave_col = '_plot_wave'
    elif '_Plot_Wave' in display_df.columns:
        plot_wave_col = '_Plot_Wave'
    
    if '_plot_color' in display_df.columns:
        plot_color_col = '_plot_color'
    elif '_Plot_Color' in display_df.columns:
        plot_color_col = '_Plot_Color'
    
    if plot_wave_col and plot_color_col:
        # Create a single Wave line that changes color based on _Plot_Color values
        # This mimics MQ5's DRAW_COLOR_LINE behavior
        
        # Create Wave line segments that are discontinuous based on _Plot_Color values
        # This mimics MQL5's DRAW_COLOR_LINE behavior without interpolation between gaps
        
        # Create masks for different signal types
        valid_data_mask = display_df[plot_wave_col].notna() & (display_df[plot_wave_col] != 0)
        red_mask = (display_df[plot_color_col] == 1) & valid_data_mask
        blue_mask = (display_df[plot_color_col] == 2) & valid_data_mask
        notrade_mask = (display_df[plot_color_col] == 0) & valid_data_mask
        
        # Add red segments (BUY = 1) as discontinuous lines
        red_segments = create_discontinuous_line_traces(
            display_df.index, 
            display_df[plot_wave_col], 
            red_mask, 
            'Wave', 
            'red', 
            width=2, 
            showlegend=True
        )
        for segment in red_segments:
            fig.add_trace(segment, row=2, col=1)
        
        # Add blue segments (SELL = 2) as discontinuous lines
        blue_segments = create_discontinuous_line_traces(
            display_df.index, 
            display_df[plot_wave_col], 
            blue_mask, 
            'Wave', 
            'blue', 
            width=2, 
            showlegend=True
        )
        for segment in blue_segments:
            fig.add_trace(segment, row=2, col=1)
        
        # Do NOT display black segments (NOTRADE = 0) - they should be invisible
        # This matches MQL5 behavior where NOTRADE segments are not shown
    
    # Add Plot FastLine (thin red line) - as per MQ5
    plot_fastline_col = None
    if '_plot_fastline' in display_df.columns:
        plot_fastline_col = '_plot_fastline'
    elif '_Plot_FastLine' in display_df.columns:
        plot_fastline_col = '_Plot_FastLine'
    
    if plot_fastline_col:
        # Only show Fast Line when there are valid values
        fastline_valid_mask = display_df[plot_fastline_col].notna() & (display_df[plot_fastline_col] != 0)
        if fastline_valid_mask.any():
            fastline_valid_data = display_df[fastline_valid_mask]
            fig.add_trace(
                go.Scatter(
                    x=fastline_valid_data.index,
                    y=fastline_valid_data[plot_fastline_col],
                    mode='lines',
                    name='Fast Line',
                    line=dict(color='red', width=1, dash='dot'),  # Thin red dashed line as in MQ5
                    showlegend=True
                ),
                row=2, col=1
            )
    
    # Add MA Line (thin light blue line) - as per MQ5
    ma_line_col = None
    if 'ma_line' in display_df.columns:
        ma_line_col = 'ma_line'
    elif 'MA_Line' in display_df.columns:
        ma_line_col = 'MA_Line'
    
    if ma_line_col:
        # Only show MA Line when there are valid values
        ma_valid_mask = display_df[ma_line_col].notna() & (display_df[ma_line_col] != 0)
        if ma_valid_mask.any():
            ma_valid_data = display_df[ma_valid_mask]
            fig.add_trace(
                go.Scatter(
                    x=ma_valid_data.index,
                    y=ma_valid_data[ma_line_col],
                    mode='lines',
                    name='MA Line',
                    line=dict(color='lightblue', width=1),  # Thin light blue line as in MQ5
                    showlegend=True
                ),
                row=2, col=1
            )


def add_bollinger_bands_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Bollinger Bands indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Bollinger Bands data
    """
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


def add_atr_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add ATR indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with ATR data
    """
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


def add_cci_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add CCI indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with CCI data
    """
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


def add_vwap_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add VWAP indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with VWAP data
    """
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


def add_pivot_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Pivot Points indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Pivot Points data
    """
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


def add_hma_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add HMA indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with HMA data
    """
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


def add_tsf_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add TSF indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with TSF data
    """
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


def add_monte_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Monte Carlo forecast line to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Monte Carlo data
    """
    # Add Monte Carlo forecast line (main line)
    if 'montecarlo' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['montecarlo'],
                mode='lines',
                name='Monte Carlo Forecast',
                line=dict(color='blue', width=3),
                showlegend=False
            ),
            row=2, col=1
        )
    
    # Add Monte Carlo signal line
    if 'montecarlo_signal' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['montecarlo_signal'],
                mode='lines',
                name='Signal Line',
                line=dict(color='red', width=2),
                showlegend=False
            ),
            row=2, col=1
        )
    
    # Add Monte Carlo histogram
    if 'montecarlo_histogram' in display_df.columns:
        # Color histogram bars based on values
        colors = ['green' if val >= 0 else 'red' for val in display_df['montecarlo_histogram']]
        fig.add_trace(
            go.Bar(
                x=display_df.index,
                y=display_df['montecarlo_histogram'],
                name='Histogram',
                marker_color=colors,
                opacity=0.7,
                showlegend=False
            ),
            row=2, col=1
        )
    
    # Add confidence bands
    if 'montecarlo_upper' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['montecarlo_upper'],
                mode='lines',
                name='Upper Confidence',
                line=dict(color='lightblue', width=1, dash='dash'),
                showlegend=False
            ),
            row=2, col=1
        )
    
    if 'montecarlo_lower' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['montecarlo_lower'],
                mode='lines',
                name='Lower Confidence',
                line=dict(color='lightblue', width=1, dash='dash'),
                showlegend=False
            ),
            row=2, col=1
        )
    
    # Add zero line for histogram
    fig.add_trace(
        go.Scatter(
            x=display_df.index,
            y=[0] * len(display_df),
            mode='lines',
            name='Zero Line',
            line=dict(color='gray', width=1, dash='dash'),
            showlegend=False
        ),
        row=2, col=1
    )


def add_kelly_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Kelly main line and signal line to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Kelly data
    """
    # Add Kelly main line
    if 'kelly' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['kelly'],
                mode='lines',
                name='Kelly Criterion',
                line=dict(color='blue', width=3),
                showlegend=False
            ),
            row=2, col=1
        )
    
    # Add Kelly signal line (EMA of Kelly values)
    if 'kelly_signal' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['kelly_signal'],
                mode='lines',
                name='Signal Line',
                line=dict(color='red', width=2),
                showlegend=False
            ),
            row=2, col=1
        )
    
    # Add Kelly histogram
    if 'kelly_histogram' in display_df.columns:
        # Color histogram bars based on values
        colors = ['green' if val >= 0 else 'red' for val in display_df['kelly_histogram']]
        fig.add_trace(
            go.Bar(
                x=display_df.index,
                y=display_df['kelly_histogram'],
                name='Histogram',
                marker_color=colors,
                opacity=0.7,
                showlegend=False
            ),
            row=2, col=1
        )
    
    # Add threshold levels
    if 'kelly_threshold_10' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['kelly_threshold_10'],
                mode='lines',
                name='10% Threshold',
                line=dict(color='orange', width=1, dash='dash'),
                showlegend=False
            ),
            row=2, col=1
        )
    
    if 'kelly_threshold_25' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['kelly_threshold_25'],
                mode='lines',
                name='25% Threshold',
                line=dict(color='red', width=1, dash='dash'),
                showlegend=False
            ),
            row=2, col=1
        )


def add_donchain_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Donchian Channels indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Donchian Channels data
    """
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


def add_fibo_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Fibonacci levels to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Fibonacci data
    """
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


def add_obv_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add OBV indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with OBV data
    """
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


def add_stdev_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add StdDev indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with StdDev data
    """
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


def add_adx_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add ADX indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with ADX data
    """
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


def add_sar_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add SAR indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with SAR data
    """
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


def add_rsi_div_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add RSI Divergence indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with RSI Divergence data
    """
    if 'rsi' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['rsi'],
                mode='lines',
                name='RSI',
                line=dict(color='purple', width=2),
                showlegend=False
            ),
            row=2, col=1
        )
    if 'rsi_divergence' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['rsi_divergence'],
                mode='lines',
                name='RSI Divergence',
                line=dict(color='orange', width=2),
                showlegend=False
            ),
            row=2, col=1
        )
        # Add zero line
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=[0] * len(display_df),
                mode='lines',
                name='Zero Line',
                line=dict(color='gray', width=1, dash='dash'),
                showlegend=False
            ),
            row=2, col=1
        )
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


def add_stoch_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Stochastic Oscillator indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Stochastic Oscillator data
    """
    if 'stoch_k' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['stoch_k'],
                mode='lines',
                name='%K',
                line=dict(color='blue', width=2),
                showlegend=False
            ),
            row=2, col=1
        )
    if 'stoch_d' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['stoch_d'],
                mode='lines',
                name='%D',
                line=dict(color='red', width=2),
                showlegend=False
            ),
            row=2, col=1
        )
    if 'stoch_overbought' in display_df.columns:
        overbought = display_df['stoch_overbought'].iloc[0]
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
    if 'stoch_oversold' in display_df.columns:
        oversold = display_df['stoch_oversold'].iloc[0]
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


def add_stochoscillator_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Stochastic Oscillator indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Stochastic Oscillator data
    """
    if 'stochosc_k' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['stochosc_k'],
                mode='lines',
                name='%K',
                line=dict(color='blue', width=2),
                showlegend=False
            ),
            row=2, col=1
        )
    if 'stochosc_d' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['stochosc_d'],
                mode='lines',
                name='%D',
                line=dict(color='red', width=2),
                showlegend=False
            ),
            row=2, col=1
        )
    if 'stochosc_overbought' in display_df.columns:
        overbought = display_df['stochosc_overbought'].iloc[0]
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
    if 'stochosc_oversold' in display_df.columns:
        oversold = display_df['stochosc_oversold'].iloc[0]
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


def add_putcallratio_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Put/Call Ratio indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Put/Call Ratio data
    """
    # Add Put/Call Ratio main line
    if 'putcallratio' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['putcallratio'],
                mode='lines',
                name='Put/Call Ratio',
                line=dict(color='purple', width=3),
                showlegend=False
            ),
            row=2, col=1
        )
    
    # Add Put/Call Ratio signal line
    if 'putcallratio_signal' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['putcallratio_signal'],
                mode='lines',
                name='Signal Line',
                line=dict(color='orange', width=2),
                showlegend=False
            ),
            row=2, col=1
        )
    
    # Add Put/Call Ratio histogram
    if 'putcallratio_histogram' in display_df.columns:
        # Color histogram bars based on values
        colors = ['green' if val >= 0 else 'red' for val in display_df['putcallratio_histogram']]
        fig.add_trace(
            go.Bar(
                x=display_df.index,
                y=display_df['putcallratio_histogram'],
                name='Histogram',
                marker_color=colors,
                opacity=0.7,
                showlegend=False
            ),
            row=2, col=1
        )
    
    # Add threshold levels
    if 'putcallratio_bullish' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['putcallratio_bullish'],
                mode='lines',
                name='Bullish Threshold',
                line=dict(color='green', width=1, dash='dash'),
                showlegend=False
            ),
            row=2, col=1
        )
    
    if 'putcallratio_bearish' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['putcallratio_bearish'],
                mode='lines',
                name='Bearish Threshold',
                line=dict(color='red', width=1, dash='dash'),
                showlegend=False
            ),
            row=2, col=1
        )
    
    if 'putcallratio_neutral' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['putcallratio_neutral'],
                mode='lines',
                name='Neutral Level',
                line=dict(color='gray', width=1, dash='dash'),
                showlegend=False
            ),
            row=2, col=1
        )


def add_cot_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add COT indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with COT data
    """
    # Add COT main line
    if 'cot' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['cot'],
                mode='lines',
                name='COT',
                line=dict(color='darkblue', width=3),
                showlegend=False
            ),
            row=2, col=1
        )
    
    # Add COT signal line
    if 'cot_signal' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['cot_signal'],
                mode='lines',
                name='Signal Line',
                line=dict(color='darkorange', width=2),
                showlegend=False
            ),
            row=2, col=1
        )
    
    # Add COT histogram
    if 'cot_histogram' in display_df.columns:
        # Color histogram bars based on values
        colors = ['green' if val >= 0 else 'red' for val in display_df['cot_histogram']]
        fig.add_trace(
            go.Bar(
                x=display_df.index,
                y=display_df['cot_histogram'],
                name='Histogram',
                marker_color=colors,
                opacity=0.7,
                showlegend=False
            ),
            row=2, col=1
        )
    
    # Add threshold levels
    if 'cot_bullish' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['cot_bullish'],
                mode='lines',
                name='Bullish Threshold',
                line=dict(color='green', width=1, dash='dash'),
                showlegend=False
            ),
            row=2, col=1
        )
    
    if 'cot_bearish' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['cot_bearish'],
                mode='lines',
                name='Bearish Threshold',
                line=dict(color='red', width=1, dash='dash'),
                showlegend=False
            ),
            row=2, col=1
        )
    
    if 'cot_neutral' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['cot_neutral'],
                mode='lines',
                name='Neutral Level',
                line=dict(color='gray', width=1, dash='dash'),
                showlegend=False
            ),
            row=2, col=1
        )


def add_feargreed_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Fear & Greed indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Fear & Greed data
    """
    # Add Fear & Greed main line
    if 'feargreed' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['feargreed'],
                mode='lines',
                name='Fear & Greed',
                line=dict(color='purple', width=3),
                showlegend=False
            ),
            row=2, col=1
        )
    # Add Fear & Greed signal line
    if 'feargreed_signal' in display_df.columns:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['feargreed_signal'],
                mode='lines',
                name='Signal Line',
                line=dict(color='orange', width=2),
                showlegend=False
            ),
            row=2, col=1
        )
    # Add Fear & Greed histogram (difference between main and signal)
    if 'feargreed' in display_df.columns and 'feargreed_signal' in display_df.columns:
        histogram = display_df['feargreed'] - display_df['feargreed_signal']
        colors = ['green' if val >= 0 else 'red' for val in histogram]
        fig.add_trace(
            go.Bar(
                x=display_df.index,
                y=histogram,
                name='Histogram',
                marker_color=colors,
                opacity=0.7,
                showlegend=False
            ),
            row=2, col=1
        )
    # Add threshold levels (constant lines)
    fear_threshold = 25
    greed_threshold = 75
    neutral_level = 50
    # Fear threshold line
    fig.add_trace(
        go.Scatter(
            x=display_df.index,
            y=[fear_threshold] * len(display_df),
            mode='lines',
            name='Fear Threshold',
            line=dict(color='red', width=1, dash='dash'),
            showlegend=False
        ),
        row=2, col=1
    )
    # Greed threshold line
    fig.add_trace(
        go.Scatter(
            x=display_df.index,
            y=[greed_threshold] * len(display_df),
            mode='lines',
            name='Greed Threshold',
            line=dict(color='green', width=1, dash='dash'),
            showlegend=False
        ),
        row=2, col=1
    )
    # Neutral level line
    fig.add_trace(
        go.Scatter(
            x=display_df.index,
            y=[neutral_level] * len(display_df),
            mode='lines',
            name='Neutral Level',
            line=dict(color='gray', width=1, dash='dash'),
            showlegend=False
        ),
        row=2, col=1
    )


def add_supertrend_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add SuperTrend indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with SuperTrend data
    """
    if 'supertrend' in display_df.columns and 'supertrend_direction' in display_df.columns:
        st = display_df['supertrend']
        trend = display_df['supertrend_direction']
    elif 'supertrend' in display_df.columns and 'direction' in display_df.columns:
        # Fallback: use direction column but we need to convert signal values to trend direction
        st = display_df['supertrend']
        # Convert signal values to trend direction: 0=no trend, 1=uptrend, 2=downtrend
        direction_signals = display_df['direction']
        trend = pd.Series(index=direction_signals.index, dtype=int)
        trend.fillna(0, inplace=True)
        
        # Convert signal values to trend direction
        # We need to infer trend direction from SuperTrend values
        # If price > SuperTrend, trend is up (1), else down (-1)
        price_series = display_df['close']
        trend = np.where(price_series > st, 1, -1)
        trend = pd.Series(trend, index=direction_signals.index)
        idx = display_df.index
        
        # Three-color scheme for signal changes
        uptrend_color = 'rgba(0, 200, 81, 0.95)'  # Modern green for uptrend
        downtrend_color = 'rgba(255, 68, 68, 0.95)'  # Modern red for downtrend
        signal_change_color = 'rgba(255, 193, 7, 0.95)'  # Golden yellow for signal changes
        
        # Detect signal change points
        buy_signals = (trend == 1) & (trend.shift(1) == -1)
        sell_signals = (trend == -1) & (trend.shift(1) == 1)
        signal_changes = buy_signals | sell_signals
        
        # Create color array with signal change highlighting
        color_arr = np.where(trend == 1, uptrend_color, downtrend_color)
        
        # Enhanced segmentation with signal change detection
        segments = []
        last_color = color_arr[0]
        seg_x, seg_y = [idx[0]], [st.iloc[0]]
        
        for i in range(1, len(idx)):
            current_color = color_arr[i]
            
            # Check if this is a signal change point
            if signal_changes.iloc[i]:
                # Add previous segment
                if len(seg_x) > 1:
                    segments.append((seg_x.copy(), seg_y.copy(), last_color))
                
                # Add signal change point with golden color
                segments.append(([idx[i-1], idx[i]], [st.iloc[i-1], st.iloc[i]], signal_change_color))
                
                # Start new segment
                seg_x, seg_y = [idx[i]], [st.iloc[i]]
                last_color = current_color
            elif current_color != last_color:
                # Regular trend change (not a signal)
                segments.append((seg_x.copy(), seg_y.copy(), last_color))
                seg_x, seg_y = [idx[i-1]], [st.iloc[i-1]]
                last_color = current_color
            
            seg_x.append(idx[i])
            seg_y.append(st.iloc[i])
        
        # Add final segment
        if len(seg_x) > 0:
            segments.append((seg_x, seg_y, last_color))
        
        # Add SuperTrend line segments with enhanced styling
        legend_shown = {uptrend_color: False, downtrend_color: False, signal_change_color: False}
        for seg_x, seg_y, seg_color in segments:
            # Main SuperTrend line with smooth curve
            # Determine legend name based on color
            if seg_color == uptrend_color:
                legend_name = 'SuperTrend (Uptrend)'
            elif seg_color == downtrend_color:
                legend_name = 'SuperTrend (Downtrend)'
            elif seg_color == signal_change_color:
                legend_name = 'SuperTrend (Signal Change)'
            else:
                legend_name = 'SuperTrend'
            
            show_legend = not legend_shown.get(seg_color, False)
            legend_shown[seg_color] = True
            
            fig.add_trace(
                go.Scatter(
                    x=seg_x,
                    y=seg_y,
                    mode='lines',
                    name=legend_name,
                    line=dict(
                        color=seg_color,
                        width=5,
                        shape='spline'  # Smooth curve for modern look
                    ),
                    showlegend=show_legend,
                    hoverinfo='y+name',
                    hoverlabel=dict(
                        bgcolor=seg_color,
                        font_size=12,
                        font_color='white',
                        font_family='Arial, sans-serif'
                    )
                ),
                row=2, col=1
            )
            
            # Add subtle glow effect for enhanced visual appeal
            fig.add_trace(
                go.Scatter(
                    x=seg_x,
                    y=seg_y,
                    mode='lines',
                    name='SuperTrend Glow',
                    line=dict(
                        color=seg_color.replace('0.95', '0.3'),
                        width=10
                    ),
                    showlegend=False,
                    hoverinfo='skip'
                ),
                row=2, col=1
            )
        
        # Enhanced trend change markers with modern styling
        buy_idx = idx[(trend == 1) & (trend.shift(1) == -1)]
        sell_idx = idx[(trend == -1) & (trend.shift(1) == 1)]
        
        # BUY signals with enhanced styling
        if len(buy_idx) > 0:
            fig.add_trace(
                go.Scatter(
                    x=buy_idx,
                    y=st.loc[buy_idx],
                    mode='markers',
                    name='BUY Signal',
                    marker=dict(
                        symbol='triangle-up',
                        size=18,
                        color='#00C851',
                        line=dict(
                            color='white',
                            width=2.5
                        ),
                        opacity=0.95
                    ),
                    showlegend=True,
                    hoverinfo='x+y+name',
                    hoverlabel=dict(
                        bgcolor='#00C851',
                        font_size=12,
                        font_color='white',
                        font_family='Arial, sans-serif'
                    )
                ),
                row=2, col=1
            )
            
            # Add pulse effect for buy signals
            fig.add_trace(
                go.Scatter(
                    x=buy_idx,
                    y=st.loc[buy_idx],
                    mode='markers',
                    name='BUY Pulse',
                    marker=dict(
                        symbol='circle',
                        size=28,
                        color='rgba(0, 200, 81, 0.4)',
                        line=dict(width=0)
                    ),
                    showlegend=False,
                    hoverinfo='skip'
                ),
                row=2, col=1
            )
        
        # SELL signals with enhanced styling
        if len(sell_idx) > 0:
            fig.add_trace(
                go.Scatter(
                    x=sell_idx,
                    y=st.loc[sell_idx],
                    mode='markers',
                    name='SELL Signal',
                    marker=dict(
                        symbol='triangle-down',
                        size=18,
                        color='#FF4444',
                        line=dict(
                            color='white',
                            width=2.5
                        ),
                        opacity=0.95
                    ),
                    showlegend=True,
                    hoverinfo='x+y+name',
                    hoverlabel=dict(
                        bgcolor='#FF4444',
                        font_size=12,
                        font_color='white',
                        font_family='Arial, sans-serif'
                    )
                ),
                row=2, col=1
            )
            
            # Add pulse effect for sell signals
            fig.add_trace(
                go.Scatter(
                    x=sell_idx,
                    y=st.loc[sell_idx],
                    mode='markers',
                    name='SELL Pulse',
                    marker=dict(
                        symbol='circle',
                        size=28,
                        color='rgba(255, 68, 68, 0.4)',
                        line=dict(width=0)
                    ),
                    showlegend=False,
                    hoverinfo='skip'
                ),
                row=2, col=1
            )
        
        # Add trend background zones for better visual context
        trend_changes = idx[trend != trend.shift(1)]
        if len(trend_changes) > 0:
            for i in range(len(trend_changes)):
                start_idx = trend_changes[i]
                end_idx = trend_changes[i + 1] if i + 1 < len(trend_changes) else idx[-1]
                
                zone_color = 'rgba(0, 200, 81, 0.08)' if trend.loc[start_idx] == 1 else 'rgba(255, 68, 68, 0.08)'
                
                fig.add_shape(
                    type="rect",
                    x0=start_idx,
                    x1=end_idx,
                    y0=st.min() * 0.995,
                    y1=st.max() * 1.005,
                    fillcolor=zone_color,
                    line=dict(width=0),
                    row=2, col=1
                )
                
    elif 'supertrend' in display_df.columns:
        # Enhanced fallback: modern single line
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['supertrend'],
                mode='lines',
                name='SuperTrend',
                line=dict(
                    color='#3498db',
                    width=4,
                    shape='spline'
                ),
                showlegend=False,
                hoverinfo='y+name',
                hoverlabel=dict(
                    bgcolor='#3498db',
                    font_size=12,
                    font_color='white'
                )
            ),
            row=2, col=1
        )
    elif 'pprice1' in display_df.columns and 'pprice2' in display_df.columns:
        # Fallback for PPrice1/PPrice2 columns (like in dual_chart_fast.py)
        p1 = display_df['pprice1']
        p2 = display_df['pprice2']
        direction = display_df['direction'] if 'direction' in display_df.columns else pd.Series(0, index=display_df.index)
        
        # Create supertrend column for consistency
        supertrend_values = np.where(direction > 0, p1, p2)
        display_df['supertrend'] = supertrend_values
        
        # Use the same logic as when supertrend column exists
        price_series = display_df['close']
        trend = np.where(price_series > supertrend_values, 1, -1)
        trend = pd.Series(trend, index=display_df.index)
        idx = display_df.index
        
        # Three-color scheme for signal changes
        uptrend_color = 'rgba(0, 200, 81, 0.95)'  # Modern green for uptrend
        downtrend_color = 'rgba(255, 68, 68, 0.95)'  # Modern red for downtrend
        signal_change_color = 'rgba(255, 193, 7, 0.95)'  # Golden yellow for signal changes
        
        # Detect signal change points
        buy_signals = (trend == 1) & (trend.shift(1) == -1)
        sell_signals = (trend == -1) & (trend.shift(1) == 1)
        signal_changes = buy_signals | sell_signals
        
        # Create color array with signal change highlighting
        color_arr = np.where(trend == 1, uptrend_color, downtrend_color)
        
        # Enhanced segmentation with signal change detection
        segments = []
        last_color = color_arr[0]
        seg_x, seg_y = [idx[0]], [supertrend_values[0]]
        
        for i in range(1, len(idx)):
            current_color = color_arr[i]
            
            # Check if this is a signal change point
            if signal_changes.iloc[i]:
                # Add previous segment
                if len(seg_x) > 1:
                    segments.append((seg_x.copy(), seg_y.copy(), last_color))
                
                # Add signal change point with golden color
                segments.append(([idx[i-1], idx[i]], [supertrend_values[i-1], supertrend_values[i]], signal_change_color))
                
                # Start new segment
                seg_x, seg_y = [idx[i]], [supertrend_values[i]]
                last_color = current_color
            elif current_color != last_color:
                # Regular trend change (not a signal)
                segments.append((seg_x.copy(), seg_y.copy(), last_color))
                seg_x, seg_y = [idx[i-1]], [supertrend_values[i-1]]
                last_color = current_color
            
            seg_x.append(idx[i])
            seg_y.append(supertrend_values[i])
        
        # Add final segment
        if len(seg_x) > 0:
            segments.append((seg_x, seg_y, last_color))
        
        # Add SuperTrend line segments with enhanced styling
        legend_shown = {uptrend_color: False, downtrend_color: False, signal_change_color: False}
        for seg_x, seg_y, seg_color in segments:
            # Main SuperTrend line with smooth curve
            # Determine legend name based on color
            if seg_color == uptrend_color:
                legend_name = 'SuperTrend (Uptrend)'
            elif seg_color == downtrend_color:
                legend_name = 'SuperTrend (Downtrend)'
            elif seg_color == signal_change_color:
                legend_name = 'SuperTrend (Signal Change)'
            else:
                legend_name = 'SuperTrend'
            
            show_legend = not legend_shown.get(seg_color, False)
            legend_shown[seg_color] = True
            
            fig.add_trace(
                go.Scatter(
                    x=seg_x,
                    y=seg_y,
                    mode='lines',
                    name=legend_name,
                    line=dict(
                        color=seg_color,
                        width=5,
                        shape='spline'  # Smooth curve for modern look
                    ),
                    showlegend=show_legend,
                    hoverinfo='y+name',
                    hoverlabel=dict(
                        bgcolor=seg_color,
                        font_size=12,
                        font_color='white',
                        font_family='Arial, sans-serif'
                    )
                ),
                row=2, col=1
            )


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
    # Remove duplicate columns by name (case-insensitive, keep first occurrence)
    cols_lower = pd.Series(display_df.columns)
    _, idx = np.unique(cols_lower.str.lower(), return_index=True)
    display_df = display_df.iloc[:, idx]
    # Ensure index is DatetimeIndex (align with original df)
    if not isinstance(display_df.index, pd.DatetimeIndex):
        display_df.index = df.index
    # Debug: print all column names and index type
    logger.print_info(f"[dual_chart_fastest] Columns: {list(display_df.columns)}")
    logger.print_info(f"[dual_chart_fastest] Index type: {type(display_df.index)}")
    
    # Ensure we have required columns
    required_columns = ['open', 'high', 'low', 'close']
    missing_columns = [col for col in required_columns if col not in display_df.columns]
    if missing_columns:
        logger.print_error(f"Missing required columns: {missing_columns}")
        return None
    
    # Create subplots: main chart (60%) and indicator chart (40%)
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(None, None),  # Without titles inside the chart
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
    
    # Add buy/sell signals if available - ONLY when _Signal == 1 (BUY) or _Signal == 2 (SELL)
    if '_signal' in display_df.columns:
        # Ensure boolean masks are aligned with DataFrame index
        buy_mask = (display_df['_signal'] == 1)  # BUY signal ONLY
        buy_mask = buy_mask.reindex(display_df.index, fill_value=False)
        buy_signals = display_df[buy_mask]
        sell_mask = (display_df['_signal'] == 2)  # SELL signal ONLY
        sell_mask = sell_mask.reindex(display_df.index, fill_value=False)
        sell_signals = display_df[sell_mask]
        
        # Only add BUY signals when _Signal == 1
        if not buy_signals.empty:
            fig.add_trace(
                go.Scatter(
                    x=buy_signals.index,
                    y=buy_signals['low'] * 0.995,  # Position below the low
                    mode='markers',
                    name='Buy Signal (_Signal=1)',
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
        
        # Only add SELL signals when _Signal == 2
        if not sell_signals.empty:
            fig.add_trace(
                go.Scatter(
                    x=sell_signals.index,
                    y=sell_signals['high'] * 1.005,  # Position above the high
                    mode='markers',
                    name='Sell Signal (_Signal=2)',
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
    
    # Fallback to direction if _signal not available (for backward compatibility)
    elif 'direction' in display_df.columns:
        # Ensure boolean masks are aligned with DataFrame index
        buy_mask = (display_df['direction'] == 1)
        buy_mask = buy_mask.reindex(display_df.index, fill_value=False)
        buy_signals = display_df[buy_mask]
        sell_mask = (display_df['direction'] == 2)
        sell_mask = sell_mask.reindex(display_df.index, fill_value=False)
        sell_signals = display_df[sell_mask]
        if not buy_signals.empty:
            fig.add_trace(
                go.Scatter(
                    x=buy_signals.index,
                    y=buy_signals['low'] * 0.995,  # Position below the low
                    mode='markers',
                    name='Buy Signal (direction=1)',
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
                    name='Sell Signal (direction=2)',
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
        add_rsi_indicator(fig, display_df)
    
    elif indicator_name == 'rsi_mom':
        add_rsi_momentum_indicator(fig, display_df)
    
    elif indicator_name == 'macd':
        add_macd_indicator(fig, display_df)
    
    elif indicator_name == 'ema':
        add_ema_indicator(fig, display_df)
    
    elif indicator_name == 'sma':
        add_sma_indicator(fig, display_df)

    elif indicator_name == 'wave':
        add_wave_indicator(fig, display_df)
    
    elif indicator_name == 'bb':
        add_bollinger_bands_indicator(fig, display_df)
    
    elif indicator_name == 'atr':
        add_atr_indicator(fig, display_df)
    
    elif indicator_name == 'cci':
        add_cci_indicator(fig, display_df)
            
    elif indicator_name == 'vwap':
        add_vwap_indicator(fig, display_df)
    
    elif indicator_name == 'pivot':
        add_pivot_indicator(fig, display_df)
    
    elif indicator_name == 'hma':
        add_hma_indicator(fig, display_df)
    
    elif indicator_name == 'tsf':
        add_tsf_indicator(fig, display_df)
    
    elif indicator_name == 'monte':
        add_monte_indicator(fig, display_df)
    
    elif indicator_name == 'kelly':
        add_kelly_indicator(fig, display_df)
    
    elif indicator_name == 'donchain':
        add_donchain_indicator(fig, display_df)
    
    elif indicator_name == 'fibo':
        add_fibo_indicator(fig, display_df)
    
    elif indicator_name == 'obv':
        add_obv_indicator(fig, display_df)
    
    elif indicator_name == 'stdev':
        add_stdev_indicator(fig, display_df)
    
    elif indicator_name == 'adx':
        add_adx_indicator(fig, display_df)
    
    elif indicator_name == 'sar':
        add_sar_indicator(fig, display_df)
    
    elif indicator_name == 'rsi_div':
        add_rsi_div_indicator(fig, display_df)
    
    elif indicator_name == 'stoch':
        add_stoch_indicator(fig, display_df)
    
    elif indicator_name == 'stochoscillator':
        add_stochoscillator_indicator(fig, display_df)
    
    elif indicator_name == 'putcallratio':
        add_putcallratio_indicator(fig, display_df)
    
    elif indicator_name == 'cot':
        add_cot_indicator(fig, display_df)
    
    elif indicator_name in ['feargreed', 'fg']:
        add_feargreed_indicator(fig, display_df)
    
    elif indicator_name == 'supertrend':
        add_supertrend_indicator(fig, display_df)
    
    # Update layout with modern styling
    fig.update_layout(
        title=dict(
            text=title or f"SuperTrend Analysis - {indicator_name.upper()}",
            x=0.5,
            xanchor='center',
            font=dict(
                size=18,
                color='#2c3e50',
                family='Arial, sans-serif'
            ),
            pad=dict(t=10, b=10)
        ),
        autosize=True,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='#e1e8ed',
            borderwidth=1,
            font=dict(size=12, color='#2c3e50'),
            itemsizing='constant'
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=11,
            bordercolor='#e1e8ed',
            font_family='Arial, sans-serif'
        ),
        margin=dict(t=40, b=20, l=40, r=20),
        plot_bgcolor='rgba(248, 249, 250, 0.8)',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif')
    )
    
    # Update axes with modern styling
    # Main chart (price)
    fig.update_yaxes(
        title_text="Price", 
        row=1, 
        col=1, 
        tickformat=".4f",
        title_font=dict(size=14, color='#2c3e50'),
        tickfont=dict(size=11, color='#34495e'),
        gridcolor='rgba(0,0,0,0.1)',
        zeroline=False,
        showline=True,
        linecolor='#e1e8ed',
        linewidth=1
    )
    fig.update_xaxes(
        row=1, col=1,
        tickformat="%b %d, %Y",
        tickangle=0,
        ticklabelmode="period",
        showgrid=True,
        gridcolor="rgba(0,0,0,0.05)",
        ticks="outside",
        ticklen=8,
        tickcolor="#b0b0b0",
        tickwidth=1.5,
        showline=True,
        linecolor="#e1e8ed",
        mirror=True,
        automargin=True,
        nticks=20,
        rangeslider=dict(visible=False)
    )
    
    # Indicator chart
    indicator_title = layout['indicator_name'] if layout else 'SuperTrend'
    fig.update_yaxes(
        title_text=indicator_title, 
        row=2, 
        col=1,
        title_font=dict(size=14, color='#2c3e50'),
        tickfont=dict(size=11, color='#34495e'),
        gridcolor='rgba(0,0,0,0.1)',
        zeroline=False,
        showline=True,
        linecolor='#e1e8ed',
        linewidth=1
    )
    
    # Enhanced time scale for indicator chart
    fig.update_xaxes(
        row=2, col=1,
        tickformat="%b %d, %Y",
        tickangle=0,
        ticklabelmode="period",
        showgrid=True,
        gridcolor="rgba(0,0,0,0.05)",
        ticks="outside",
        ticklen=8,
        tickcolor="#b0b0b0",
        tickwidth=1.5,
        showline=True,
        linecolor="#e1e8ed",
        mirror=True,
        automargin=True,
        nticks=20,
        rangeslider=dict(visible=False)
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