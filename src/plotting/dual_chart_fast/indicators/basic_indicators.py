# -*- coding: utf-8 -*-
# src/plotting/dual_chart_fast/indicators/basic_indicators.py

"""
Basic indicator functions for dual chart fast plotting.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Dict, Any, Optional

from src.common import logger


def _plot_rsi_indicator(indicator_fig, source, display_df):
    """
    Plot RSI indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with RSI data
    """
    try:
        if 'rsi' in display_df.columns:
            # Add RSI line
            indicator_fig.add_trace(
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
                indicator_fig.add_trace(
                    go.Scatter(
                        x=display_df.index,
                        y=[overbought] * len(display_df),
                        mode='lines',
                        name='Overbought',
                        line=dict(color='red', width=2, dash='dash'),
                        showlegend=False
                    ),
                    row=2, col=1
                )
            
            if 'rsi_oversold' in display_df.columns:
                oversold = display_df['rsi_oversold'].iloc[0]
                indicator_fig.add_trace(
                    go.Scatter(
                        x=display_df.index,
                        y=[oversold] * len(display_df),
                        mode='lines',
                        name='Oversold',
                        line=dict(color='green', width=2, dash='dash'),
                        showlegend=False
                    ),
                    row=2, col=1
                )
    except Exception as e:
        logger.print_error(f"Error plotting RSI indicator: {e}")


def _plot_macd_indicator(indicator_fig, source, display_df):
    """
    Plot MACD indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with MACD data
    """
    try:
        if 'macd' in display_df.columns:
            # Add MACD line
            indicator_fig.add_trace(
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
            # Add MACD signal line
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['macd_signal'],
                    mode='lines',
                    name='MACD Signal',
                    line=dict(color='red', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        if 'macd_histogram' in display_df.columns:
            # Add MACD histogram
            colors = ['green' if val >= 0 else 'red' for val in display_df['macd_histogram']]
            indicator_fig.add_trace(
                go.Bar(
                    x=display_df.index,
                    y=display_df['macd_histogram'],
                    name='MACD Histogram',
                    marker_color=colors,
                    showlegend=False
                ),
                row=2, col=1
            )
    except Exception as e:
        logger.print_error(f"Error plotting MACD indicator: {e}")


def _plot_ema_indicator(indicator_fig, source, display_df):
    """
    Plot EMA indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with EMA data
    """
    try:
        if 'ema' in display_df.columns:
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['ema'],
                    mode='lines',
                    name='EMA',
                    line=dict(color='yellow', width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
    except Exception as e:
        logger.print_error(f"Error plotting EMA indicator: {e}")


def _plot_sma_indicator(indicator_fig, source, display_df):
    """
    Plot SMA indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with SMA data
    """
    try:
        if 'sma' in display_df.columns:
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['sma'],
                    mode='lines',
                    name='SMA',
                    line=dict(color='orange', width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
    except Exception as e:
        logger.print_error(f"Error plotting SMA indicator: {e}")


def _plot_bb_indicator(indicator_fig, source, display_df):
    """
    Plot Bollinger Bands indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with Bollinger Bands data
    """
    try:
        if 'bollinger_upper' in display_df.columns:
            # Add upper band
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['bollinger_upper'],
                    mode='lines',
                    name='BB Upper',
                    line=dict(color='red', width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
        
        if 'bollinger_lower' in display_df.columns:
            # Add lower band
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['bollinger_lower'],
                    mode='lines',
                    name='BB Lower',
                    line=dict(color='green', width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
        
        if 'bollinger_middle' in display_df.columns:
            # Add middle band
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['bollinger_middle'],
                    mode='lines',
                    name='BB Middle',
                    line=dict(color='blue', width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
    except Exception as e:
        logger.print_error(f"Error plotting Bollinger Bands indicator: {e}")


def _plot_atr_indicator(indicator_fig, source, display_df):
    """
    Plot ATR indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with ATR data
    """
    try:
        if 'atr' in display_df.columns:
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['atr'],
                    mode='lines',
                    name='ATR',
                    line=dict(color='purple', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
    except Exception as e:
        logger.print_error(f"Error plotting ATR indicator: {e}")


def _plot_cci_indicator(indicator_fig, source, display_df):
    """
    Plot CCI indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with CCI data
    """
    try:
        if 'cci' in display_df.columns:
            # Add CCI line
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['cci'],
                    mode='lines',
                    name='CCI',
                    line=dict(color='blue', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            # Add overbought/oversold lines
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[100] * len(display_df),
                    mode='lines',
                    name='CCI Overbought',
                    line=dict(color='red', width=2, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[-100] * len(display_df),
                    mode='lines',
                    name='CCI Oversold',
                    line=dict(color='green', width=2, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
    except Exception as e:
        logger.print_error(f"Error plotting CCI indicator: {e}")


def _plot_vwap_indicator(indicator_fig, source, display_df):
    """
    Plot VWAP indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with VWAP data
    """
    try:
        if 'vwap' in display_df.columns:
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['vwap'],
                    mode='lines',
                    name='VWAP',
                    line=dict(color='cyan', width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
    except Exception as e:
        logger.print_error(f"Error plotting VWAP indicator: {e}")


def _plot_pivot_indicator(indicator_fig, source, display_df):
    """
    Plot Pivot Points indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with Pivot Points data
    """
    try:
        if 'pivot_points' in display_df.columns:
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['pivot_points'],
                    mode='lines',
                    name='Pivot Points',
                    line=dict(color='white', width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
    except Exception as e:
        logger.print_error(f"Error plotting Pivot Points indicator: {e}")


def _plot_hma_indicator(indicator_fig, source, display_df):
    """
    Plot HMA indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with HMA data
    """
    try:
        if 'hma' in display_df.columns:
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['hma'],
                    mode='lines',
                    name='HMA',
                    line=dict(color='magenta', width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
    except Exception as e:
        logger.print_error(f"Error plotting HMA indicator: {e}")


def _plot_tsf_indicator(indicator_fig, source, display_df):
    """
    Plot TSF indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with TSF data
    """
    try:
        if 'tsf' in display_df.columns:
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['tsf'],
                    mode='lines',
                    name='TSF',
                    line=dict(color='lime', width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
    except Exception as e:
        logger.print_error(f"Error plotting TSF indicator: {e}")


def _plot_obv_indicator(indicator_fig, source, display_df):
    """
    Plot OBV indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with OBV data
    """
    try:
        if 'obv' in display_df.columns:
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['obv'],
                    mode='lines',
                    name='OBV',
                    line=dict(color='orange', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
    except Exception as e:
        logger.print_error(f"Error plotting OBV indicator: {e}")


def _plot_stdev_indicator(indicator_fig, source, display_df):
    """
    Plot Standard Deviation indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with Standard Deviation data
    """
    try:
        if 'std' in display_df.columns:
            indicator_fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['std'],
                    mode='lines',
                    name='Standard Deviation',
                    line=dict(color='yellow', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
    except Exception as e:
        logger.print_error(f"Error plotting Standard Deviation indicator: {e}")
