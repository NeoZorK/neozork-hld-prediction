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
import time
from typing import Dict, Any, Optional

from ..common import logger


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


def add_schr_dir_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add SCHR Direction indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with SCHR Direction data
    """
    if 'pprice1' in display_df.columns and 'pprice2' in display_df.columns:
        # Add High line (PPrice1)
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['pprice1'],
                mode='lines',
                name='SCHR High Line',
                line=dict(color='dodgerblue', width=3),
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Add Low line (PPrice2)
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['pprice2'],
                mode='lines',
                name='SCHR Low Line',
                line=dict(color='gold', width=3),
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Add buy/sell signals if available
        if 'direction' in display_df.columns:
            buy_signals = display_df[display_df['direction'] == 1]
            sell_signals = display_df[display_df['direction'] == 2]
            
            # Removed standard Buy/Sell signals - keeping only SCHR signals


def add_schr_rost_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add SCHR_ROST indicator to the chart.
    Signal (0=No Signal, 1=Buy, 2=Sell) on upper OHLC chart
    Direction (1=Up, 2=Down) on lower subplot
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with SCHR_ROST data
    """
    t_start = time.time()
    logger.print_info(f"[PERF] Starting SCHR_ROST indicator addition")
    # Check if SCHR_ROST columns exist
    schr_rost_cols = [col for col in display_df.columns if 'schr_rost' in col.lower()]
    if not schr_rost_cols:
        logger.print_warning("SCHR_ROST columns not found in DataFrame")
        return
    
    # Get Signal values for upper OHLC chart (0=No Signal, 1=Buy, 2=Sell)
    signal_values = None
    for col in ['schr_rost_signal', 'SCHR_ROST_Signal']:
        if col in display_df.columns:
            signal_values = display_df[col]
            break
    
    if signal_values is not None:
        # Add Signal markers on upper OHLC chart
        # Only show when signal is not 0 (No Signal)
        buy_signals = signal_values == 1
        sell_signals = signal_values == 2
        
        if buy_signals.any():
            fig.add_trace(
                go.Scatter(
                    x=display_df.index[buy_signals],
                    y=display_df['high'][buy_signals] * 1.001,  # Slightly above high
                    mode='markers',
                    name='SCHR Buy Signal',
                    marker=dict(
                        symbol='triangle-up',
                        size=12,
                        color='green',
                        line=dict(color='darkgreen', width=2)
                    ),
                    showlegend=True
                ),
                row=1, col=1
            )
        
        if sell_signals.any():
            fig.add_trace(
                go.Scatter(
                    x=display_df.index[sell_signals],
                    y=display_df['low'][sell_signals] * 0.999,  # Slightly below low
                    mode='markers',
                    name='SCHR Sell Signal',
                    marker=dict(
                        symbol='triangle-down',
                        size=12,
                        color='red',
                        line=dict(color='darkred', width=2)
                    ),
                    showlegend=True
                ),
                row=1, col=1
            )
    
    logger.print_info(f"[PERF] SCHR_ROST signal markers: {(time.time() - t_start)*1000:.1f}ms")
    
    # Get Direction values for lower subplot (1=Up, 2=Down)
    direction_values = None
    for col in ['schr_rost_direction', 'SCHR_ROST_Direction']:
        if col in display_df.columns:
            direction_values = display_df[col]
            break
    
    if direction_values is not None:
        # Add Direction line on lower subplot with enhanced styling
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=direction_values,
                mode='lines',
                name='SCHR Direction',
                line=dict(
                    color='#e67e22', 
                    width=4,
                    shape='hv'  # Horizontal-vertical steps for clean step-like appearance
                ),
                yaxis='y2',
                hovertemplate='<b>SCHR Direction</b><br>' +
                             'Value: %{y}<br>' +
                             'Date: %{x}<br>' +
                             '<extra></extra>',
                showlegend=True
            ),
            row=2, col=1
        )
        
        # Background shapes removed for performance optimization
        logger.print_info(f"[PERF] SCHR_ROST background shapes: 0.0ms (removed for performance)")
    
    # Get main SCHR_ROST values for reference
    schr_rost_values = None
    for col in ['schr_rost', 'SCHR_ROST']:
        if col in display_df.columns:
            schr_rost_values = display_df[col]
            break
    
    if schr_rost_values is not None:
        # Add main SCHR_ROST line on lower subplot with enhanced styling
        # Scale the values to make them more visible on the chart (between 1.0 and 2.0 - middle of orange line range)
        scaled_values = (schr_rost_values - schr_rost_values.min()) / (schr_rost_values.max() - schr_rost_values.min()) * 1.0 + 1.0
        
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=scaled_values,
                mode='lines',
                name='SCHR Rost',
                line=dict(
                    color='#3498db', 
                    width=3,
                    dash='solid'
                ),
                yaxis='y2',
                hovertemplate='<b>SCHR Rost</b><br>' +
                             'Value: %{text}<br>' +
                             'Date: %{x}<br>' +
                             '<extra></extra>',
                text=[f'{val:.6f}' for val in schr_rost_values],
                showlegend=True
            ),
            row=2, col=1
        )
    
    # Add zero line with enhanced styling
    fig.add_hline(
        y=0,
        line_dash="dot",
        line_color="#95a5a6",
        opacity=0.7,
        line_width=1.5,
        row=2, col=1
    )
    
    # Update y-axis title and range
    fig.update_yaxes(
        title_text="SCHR Direction", 
        row=2, col=1,
        range=[0.8, 2.0],  # Adjusted range for better visibility
        tickmode='array',
        tickvals=[1, 1.5, 2],  # Show ticks for Direction and SCHR Rost values
        ticktext=['Up', 'SCHR Rost', 'Down']  # Custom labels for better readability
    )
    
    logger.print_info(f"[PERF] Total SCHR_ROST indicator: {(time.time() - t_start)*1000:.1f}ms")


def add_schr_trend_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add SCHR_TREND indicator to the chart with simplified legend:
    - _Origin (RSI-like values) - NOT VISIBLE on chart
    - Trend (Line values)
    - Direction (0=no_signal, 1=buy, 2=sell, 3=dbl_buy, 4=dbl_sell)
    - Signal (0=no_signal, 1=buy, 2=sell, 3=dbl_buy, 4=dbl_sell) - only changes
    - PurchasePower (enabled only for Purchase Power modes)
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with SCHR_TREND data
    """
    t_start = time.time()
    logger.print_info(f"[PERF] Starting SCHR_TREND indicator addition")
    
    # Check if SCHR_TREND columns exist
    schr_trend_cols = [col for col in display_df.columns if 'schr_trend' in col.lower()]
    if not schr_trend_cols:
        logger.print_warning("SCHR_TREND columns not found in DataFrame")
        return
    
    # Get Color values for OHLC candle coloring (0=no_signal, 1=buy, 2=sell, 3=dbl_buy, 4=dbl_sell)
    # Color shows the actual color assignment for candles, matching MQL5 _arr_Color behavior
    color_values = None
    for col in ['schr_trend_color', 'SCHR_TREND_Color']:
        if col in display_df.columns:
            color_values = display_df[col]
            break
    
    # Get Direction values for trend line (0=no_signal, 1=buy, 2=sell, 3=dbl_buy, 4=dbl_sell)
    # Direction shows current trend state, used for trend line
    direction_values = None
    for col in ['schr_trend_direction', 'SCHR_TREND_Direction']:
        if col in display_df.columns:
            direction_values = display_df[col]
            break
    
    if direction_values is not None:
        # Add Direction line on lower subplot with enhanced styling
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=direction_values,
                mode='lines',
                name='SCHR Trend Direction',
                line=dict(
                    color='#e67e22', 
                    width=4,
                    shape='hv'  # Horizontal-vertical steps for clean step-like appearance
                ),
                yaxis='y2',
                hovertemplate='<b>SCHR Trend Direction</b><br>' +
                             'Value: %{y}<br>' +
                             'Date: %{x}<br>' +
                             '<extra></extra>',
                showlegend=True
            ),
            row=2, col=1
        )
    
    # REMOVED: Triangle signals to simplify legend and avoid duplication
    # Candle colors already show the signals clearly
    
    # Now draw OHLC candles with proper SCHR_TREND coloring
    # Use color_values (schr_trend_color) for candle coloring, matching MQL5 _arr_Color behavior
    if color_values is not None:
        # No Signal (0) - Grey (matches MQL5 clrNONE)
        no_signal_mask = color_values == 0
        if no_signal_mask.any():
            fig.add_trace(
                go.Candlestick(
                    x=display_df.index[no_signal_mask],
                    open=display_df['open'][no_signal_mask],
                    high=display_df['high'][no_signal_mask],
                    low=display_df['low'][no_signal_mask],
                    close=display_df['close'][no_signal_mask],
                    name="SCHR_TREND: No Signal",
                    increasing_line_color='#95a5a6',
                    decreasing_line_color='#95a5a6',
                    increasing_fillcolor='#95a5a6',
                    decreasing_fillcolor='#95a5a6',
                    line=dict(width=1.2)
                ),
                row=1, col=1
            )
        
        # Buy (1) - Blue (matches MQL5 clrBlue)
        buy_mask = color_values == 1
        if buy_mask.any():
            fig.add_trace(
                go.Candlestick(
                    x=display_df.index[buy_mask],
                    open=display_df['open'][buy_mask],
                    high=display_df['high'][buy_mask],
                    low=display_df['low'][buy_mask],
                    close=display_df['close'][buy_mask],
                    name="SCHR_TREND: Buy",
                    increasing_line_color='#3498db',
                    decreasing_line_color='#3498db',
                    increasing_fillcolor='#3498db',
                    decreasing_fillcolor='#3498db',
                    line=dict(width=1.2)
                ),
                row=1, col=1
            )
        
        # Sell (2) - Yellow (matches MQL5 clrYellow)
        sell_mask = color_values == 2
        if sell_mask.any():
            fig.add_trace(
                go.Candlestick(
                    x=display_df.index[sell_mask],
                    open=display_df['open'][sell_mask],
                    high=display_df['high'][sell_mask],
                    low=display_df['low'][sell_mask],
                    close=display_df['close'][sell_mask],
                    name="SCHR_TREND: Sell",
                    increasing_line_color='#f1c40f',
                    decreasing_line_color='#f1c40f',
                    increasing_fillcolor='#f1c40f',
                    decreasing_fillcolor='#f1c40f',
                    line=dict(width=1.2)
                ),
                row=1, col=1
            )
        
        # DBL Buy (3) - Aqua (matches MQL5 clrAqua)
        dbl_buy_mask = color_values == 3
        if dbl_buy_mask.any():
            fig.add_trace(
                go.Candlestick(
                    x=display_df.index[dbl_buy_mask],
                    open=display_df['open'][dbl_buy_mask],
                    high=display_df['high'][dbl_buy_mask],
                    low=display_df['low'][dbl_buy_mask],
                    close=display_df['close'][dbl_buy_mask],
                    name="SCHR_TREND: DBL Buy",
                    increasing_line_color='#00ffff',
                    decreasing_line_color='#00ffff',
                    increasing_fillcolor='#00ffff',
                    decreasing_fillcolor='#00ffff',
                    line=dict(width=1.2)
                ),
                row=1, col=1
            )
        
        # DBL Sell (4) - Red (matches MQL5 clrRed)
        dbl_sell_mask = color_values == 4
        if dbl_sell_mask.any():
            fig.add_trace(
                go.Candlestick(
                    x=display_df.index[dbl_sell_mask],
                    open=display_df['open'][dbl_sell_mask],
                    high=display_df['high'][dbl_sell_mask],
                    low=display_df['low'][dbl_sell_mask],
                    close=display_df['close'][dbl_sell_mask],
                    name="SCHR_TREND: DBL Sell",
                    increasing_line_color='#e74c3c',
                    decreasing_line_color='#e74c3c',
                    increasing_fillcolor='#e74c3c',
                    decreasing_fillcolor='#e74c3c',
                    line=dict(width=1.2)
                ),
                row=1, col=1
            )
    
    # Get main SCHR_TREND values for reference
    schr_trend_values = None
    for col in ['schr_trend', 'SCHR_TREND']:
        if col in display_df.columns:
            schr_trend_values = display_df[col]
            break
    
    if schr_trend_values is not None:
        # Add main SCHR_TREND line on lower subplot with enhanced styling
        # Scale the values to make them more visible on the chart (between 1.0 and 2.0)
        scaled_values = (schr_trend_values - schr_trend_values.min()) / (schr_trend_values.max() - schr_trend_values.min()) * 1.0 + 1.0
        
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=scaled_values,
                mode='lines',
                name='SCHR Trend',
                line=dict(
                    color='#3498db', 
                    width=3,
                    dash='solid'
                ),
                yaxis='y2',
                hovertemplate='<b>SCHR Trend</b><br>' +
                             'Value: %{text}<br>' +
                             'Date: %{x}<br>' +
                             '<extra></extra>',
                text=[f'{val:.6f}' for val in schr_trend_values],
                showlegend=True
            ),
            row=2, col=1
        )
    
    # Add zero line with enhanced styling
    fig.add_hline(
        y=0,
        line_dash="dot",
        line_color="#95a5a6",
        opacity=0.7,
        line_width=1.5,
        row=2, col=1
    )
    
    # Update y-axis title and range
    fig.update_yaxes(
        title_text="SCHR Trend Direction", 
        row=2, col=1,
        range=[0.8, 4.2],  # Adjusted range for better visibility
        tickmode='array',
        tickvals=[1, 2, 3, 4],  # Show ticks for Direction values
        ticktext=['Buy', 'Sell', 'DBL Buy', 'DBL Sell']  # Custom labels for better readability
    )
    
    logger.print_info(f"[PERF] Total SCHR_TREND indicator: {(time.time() - t_start)*1000:.1f}ms")


def add_schr_wave2_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add SCHR_Wave2 indicator to the chart.
    Signal (0=No Signal, 1=Buy, 2=Sell) on upper OHLC chart
    Direction (1=Up, 2=Down) on lower subplot
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with SCHR_Wave2 data
    """
    t_start = time.time()
    logger.print_info(f"[PERF] Starting SCHR_Wave2 indicator addition")
    
    # Check if SCHR_Wave2 columns exist
    schr_wave2_cols = [col for col in display_df.columns if 'schr_wave2' in col.lower()]
    if not schr_wave2_cols:
        logger.print_warning("SCHR_Wave2 columns not found in DataFrame")
        return
    
    # Get Signal values for upper OHLC chart (0=No Signal, 1=Buy, 2=Sell)
    signal_values = None
    for col in ['schr_wave2_signal', 'SCHR_Wave2_Signal']:
        if col in display_df.columns:
            signal_values = display_df[col]
            break
    
    if signal_values is not None:
        # Add buy signals (green triangles pointing up)
        buy_signals = signal_values == 1
        if buy_signals.any():
            # Safely get low prices for buy signals
            low_col = None
            for col in ['low', 'Low']:
                if col in display_df.columns:
                    low_col = col
                    break
            
            if low_col is not None:
                fig.add_trace(
                    go.Scatter(
                        x=display_df.index[buy_signals],
                        y=display_df.loc[buy_signals, low_col] * 0.9995,  # Slightly below low
                        mode='markers',
                        marker=dict(
                            symbol='triangle-up',
                            size=12,
                            color='green',
                            line=dict(color='darkgreen', width=1)
                        ),
                        name='SCHR_Wave2 Buy Signal',
                        showlegend=False,
                        hovertemplate='<b>SCHR_Wave2 Buy Signal</b><br>' +
                                    'Date: %{x}<br>' +
                                    'Price: %{y:.4f}<br>' +
                                    '<extra></extra>'
                    ),
                    row=1, col=1
                )
        
        # Add sell signals (red triangles pointing down)
        sell_signals = signal_values == 2
        if sell_signals.any():
            # Safely get high prices for sell signals
            high_col = None
            for col in ['high', 'High']:
                if col in display_df.columns:
                    high_col = col
                    break
            
            if high_col is not None:
                fig.add_trace(
                    go.Scatter(
                        x=display_df.index[sell_signals],
                        y=display_df.loc[sell_signals, high_col] * 1.0005,  # Slightly above high
                        mode='markers',
                        marker=dict(
                            symbol='triangle-down',
                            size=12,
                            color='red',
                            line=dict(color='darkred', width=1)
                        ),
                        name='SCHR_Wave2 Sell Signal',
                        showlegend=False,
                        hovertemplate='<b>SCHR_Wave2 Sell Signal</b><br>' +
                                    'Date: %{x}<br>' +
                                    'Price: %{y:.4f}<br>' +
                                    '<extra></extra>'
                    ),
                    row=1, col=1
                )
    
    # Get Direction values for lower subplot (1=Up, 2=Down)
    direction_values = None
    for col in ['schr_wave2_direction', 'SCHR_Wave2_Direction']:
        if col in display_df.columns:
            direction_values = display_df[col]
            break
    
    if direction_values is not None:
        # Add direction line on lower subplot
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=direction_values,
                mode='lines',
                name='SCHR_Wave2 Direction',
                line=dict(color='purple', width=2),
                showlegend=False,
                hovertemplate='<b>SCHR_Wave2 Direction</b><br>' +
                            'Date: %{x}<br>' +
                            'Direction: %{y}<br>' +
                            '<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Add reference lines for direction values
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=[1] * len(display_df),
                mode='lines',
                name='Up Trend',
                line=dict(color='green', width=1, dash='dash'),
                showlegend=False
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=[2] * len(display_df),
                mode='lines',
                name='Down Trend',
                line=dict(color='red', width=1, dash='dash'),
                showlegend=False
            ),
            row=2, col=1
        )
    
    # Add SCHR_Wave2 main wave line if available
    wave_values = None
    for col in ['schr_wave2_wave', 'SCHR_Wave2_Wave']:
        if col in display_df.columns:
            wave_values = display_df[col]
            break
    
    if wave_values is not None:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=wave_values,
                mode='lines',
                name='SCHR_Wave2 Wave',
                line=dict(color='blue', width=2),
                showlegend=False,
                hovertemplate='<b>SCHR_Wave2 Wave</b><br>' +
                            'Date: %{x}<br>' +
                            'Value: %{y:.4f}<br>' +
                            '<extra></extra>'
            ),
            row=2, col=1
        )
    
    # Add SCHR_Wave2 fast line if available
    fast_line_values = None
    for col in ['schr_wave2_fast_line', 'SCHR_Wave2_Fast_Line']:
        if col in display_df.columns:
            fast_line_values = display_df[col]
            break
    
    if fast_line_values is not None:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=fast_line_values,
                mode='lines',
                name='SCHR_Wave2 Fast Line',
                line=dict(color='orange', width=2),
                showlegend=False,
                hovertemplate='<b>SCHR_Wave2 Fast Line</b><br>' +
                            'Date: %{x}<br>' +
                            'Value: %{y:.4f}<br>' +
                            '<extra></extra>'
            ),
            row=2, col=1
        )
    
    # Add SCHR_Wave2 MA line if available
    ma_line_values = None
    for col in ['schr_wave2_ma_line', 'SCHR_Wave2_MA_Line']:
        if col in display_df.columns:
            ma_line_values = display_df[col]
            break
    
    if ma_line_values is not None:
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=ma_line_values,
                mode='lines',
                name='SCHR_Wave2 MA Line',
                line=dict(color='yellow', width=3),
                showlegend=False,
                hovertemplate='<b>SCHR_Wave2 MA Line</b><br>' +
                            'Date: %{x}<br>' +
                            'Value: %{y:.4f}<br>' +
                            '<extra></extra>'
            ),
            row=2, col=1
        )
    
    # Add zero line with enhanced styling
    fig.add_hline(
        y=0,
        line_dash="dot",
        line_color="#95a5a6",
        opacity=0.7,
        line_width=1.5,
        row=2, col=1
    )
    
    # Update y-axis title and range for SCHR_Wave2
    fig.update_yaxes(
        title_text="SCHR Wave2", 
        row=2, col=1,
        range=[-0.5, 0.5],  # Adjusted range for wave values
        tickmode='auto',
        showgrid=True,
        gridcolor='rgba(0,0,0,0.1)',
        zeroline=True,
        zerolinecolor='#95a5a6',
        zerolinewidth=1.5
    )
    
    t_end = time.time()
    logger.print_info(f"[PERF] SCHR_Wave2 indicator addition completed in {t_end - t_start:.3f}s")


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
        
        # Removed standard BUY/SELL signals - keeping only SCHR signals
        
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
    
    # Start timing
    start_time = time.time()
    logger.print_info(f"[PERF] Starting dual chart creation for {len(df)} rows")
    
    # DataFrame already contains calculated indicators from plot_dual_chart_results
    # Just use the provided DataFrame directly
    display_df = df.copy()
    
    # Standardize column names
    t1 = time.time()
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
    logger.print_info(f"[PERF] Data preparation: {(time.time() - t1)*1000:.1f}ms")
    
    # Ensure we have required columns
    required_columns = ['open', 'high', 'low', 'close']
    missing_columns = [col for col in required_columns if col not in display_df.columns]
    if missing_columns:
        logger.print_error(f"Missing required columns: {missing_columns}")
        return None
    
    # Create subplots: main chart (60%) and indicator chart (40%)
    t2 = time.time()
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(None, None),  # Without titles inside the chart
        vertical_spacing=0.04,
        row_heights=[0.62, 0.38],
        specs=[[{"secondary_y": False}],
               [{"secondary_y": False}]]
    )
    logger.print_info(f"[PERF] Subplot creation: {(time.time() - t2)*1000:.1f}ms")
    
    # Add candlestick chart to main subplot
    t3 = time.time()
    
    # Check if we have SCHR_TREND Direction values for custom coloring
    schr_direction_col = None
    for col in ['schr_trend_direction', 'SCHR_TREND_Direction']:
        if col in display_df.columns:
            schr_direction_col = col
            break
    
    if schr_direction_col is not None:
        # SCHR_TREND coloring will be handled by add_schr_trend_indicator function
        # Skip creating duplicate OHLC candles here to avoid legend duplication
        # The add_schr_trend_indicator function will create properly named SCHR_TREND candles
        pass
    else:
        # Standard candlestick coloring for non-SCHR_TREND indicators
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
    
    logger.print_info(f"[PERF] Candlestick chart: {(time.time() - t3)*1000:.1f}ms")
    
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
    
    # Removed standard buy/sell signals - keeping only SCHR signals
    
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
    
    elif indicator_name == 'schr_dir':
        add_schr_dir_indicator(fig, display_df)
    
    elif indicator_name == 'schr_rost':
        add_schr_rost_indicator(fig, display_df)
    
    elif indicator_name == 'schr_trend':
        try:
            logger.print_info("[PERF] Starting SCHR_TREND indicator addition")
            add_schr_trend_indicator(fig, display_df)
            logger.print_info("[PERF] SCHR_TREND indicator addition completed")
        except Exception as e:
            logger.print_error(f"Error adding SCHR_TREND indicator: {e}")
            logger.print_debug(f"Display DataFrame columns: {list(display_df.columns)}")
            logger.print_debug(f"Display DataFrame shape: {display_df.shape}")
    
    elif indicator_name == 'schr_wave2':
        try:
            logger.print_info("[PERF] Starting SCHR_Wave2 indicator addition")
            add_schr_wave2_indicator(fig, display_df)
            logger.print_info("[PERF] SCHR_Wave2 indicator addition completed")
        except Exception as e:
            logger.print_error(f"Error adding SCHR_Wave2 indicator: {e}")
            logger.print_debug(f"Display DataFrame columns: {list(display_df.columns)}")
            logger.print_debug(f"Display DataFrame shape: {display_df.shape}")
    
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
    t_save = time.time()
    pio.write_html(fig, output_path, auto_open=False)
    abs_path = os.path.abspath(output_path)
    webbrowser.open_new_tab(f"file://{abs_path}")
    
    total_time = time.time() - start_time
    logger.print_info(f"[PERF] File save: {(time.time() - t_save)*1000:.1f}ms")
    logger.print_info(f"[PERF] Total dual chart creation: {total_time*1000:.1f}ms")
    logger.print_info(f"Dual chart saved to: {abs_path}")
    
    return fig 