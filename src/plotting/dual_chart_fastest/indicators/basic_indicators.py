# -*- coding: utf-8 -*-
# src/plotting/dual_chart_fastest/indicators/basic_indicators.py

"""
Basic indicator functions for dual chart fastest plotting.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Dict, Any, Optional

from src.common import logger


def add_rsi_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add RSI indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with RSI data
    """
    try:
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
                        name='Overbought',
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
                        name='Oversold',
                        line=dict(color='green', width=2, dash='dash'),
                        showlegend=False
                    ),
                    row=2, col=1
                )
    except Exception as e:
        logger.print_error(f"Error adding RSI indicator: {e}")


def add_rsi_momentum_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add RSI momentum indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with RSI momentum data
    """
    try:
        if 'rsi_mom' in display_df.columns:
            # Add RSI momentum line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['rsi_mom'],
                    mode='lines',
                    name='RSI Momentum',
                    line=dict(color='orange', width=3),
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
                    line=dict(color='white', width=1, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
    except Exception as e:
        logger.print_error(f"Error adding RSI momentum indicator: {e}")


def add_macd_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add MACD indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with MACD data
    """
    try:
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
            # Add MACD signal line
            fig.add_trace(
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
            fig.add_trace(
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
        logger.print_error(f"Error adding MACD indicator: {e}")


def add_ema_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add EMA indicator to the main chart.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with EMA data
    """
    try:
        if 'ema' in display_df.columns:
            fig.add_trace(
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
        logger.print_error(f"Error adding EMA indicator: {e}")


def add_sma_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add SMA indicator to the main chart.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with SMA data
    """
    try:
        if 'sma' in display_df.columns:
            fig.add_trace(
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
        logger.print_error(f"Error adding SMA indicator: {e}")


def add_bollinger_bands_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Bollinger Bands indicator to the main chart.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Bollinger Bands data
    """
    try:
        if 'bollinger_upper' in display_df.columns:
            # Add upper band
            fig.add_trace(
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
            fig.add_trace(
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
            fig.add_trace(
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
        logger.print_error(f"Error adding Bollinger Bands indicator: {e}")


def add_atr_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add ATR indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with ATR data
    """
    try:
        if 'atr' in display_df.columns:
            fig.add_trace(
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
        logger.print_error(f"Error adding ATR indicator: {e}")


def add_cci_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add CCI indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with CCI data
    """
    try:
        if 'cci' in display_df.columns:
            # Add CCI line
            fig.add_trace(
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
            fig.add_trace(
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
            
            fig.add_trace(
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
        logger.print_error(f"Error adding CCI indicator: {e}")


def add_vwap_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add VWAP indicator to the main chart.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with VWAP data
    """
    try:
        if 'vwap' in display_df.columns:
            fig.add_trace(
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
        logger.print_error(f"Error adding VWAP indicator: {e}")


def add_pivot_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Pivot Points indicator to the main chart.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Pivot Points data
    """
    try:
        if 'pivot_points' in display_df.columns:
            fig.add_trace(
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
        logger.print_error(f"Error adding Pivot Points indicator: {e}")


def add_hma_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add HMA indicator to the main chart.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with HMA data
    """
    try:
        if 'hma' in display_df.columns:
            fig.add_trace(
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
        logger.print_error(f"Error adding HMA indicator: {e}")


def add_tsf_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add TSF indicator to the main chart.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with TSF data
    """
    try:
        if 'tsf' in display_df.columns:
            fig.add_trace(
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
        logger.print_error(f"Error adding TSF indicator: {e}")


def add_obv_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add OBV indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with OBV data
    """
    try:
        if 'obv' in display_df.columns:
            fig.add_trace(
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
        logger.print_error(f"Error adding OBV indicator: {e}")


def add_stdev_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Standard Deviation indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Standard Deviation data
    """
    try:
        if 'std' in display_df.columns:
            fig.add_trace(
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
        logger.print_error(f"Error adding Standard Deviation indicator: {e}")
