# -*- coding: utf-8 -*-
# src/plotting/dual_chart_fastest/indicators/advanced_indicators.py

"""
Advanced indicator functions for dual chart fastest plotting.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Dict, Any, Optional

from src.common import logger


def add_wave_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Wave indicator to the main chart.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Wave data
    """
    try:
        if 'wave' in display_df.columns:
            # Create discontinuous line traces for wave
            wave_data = display_df['wave'].dropna()
            if not wave_data.empty:
                # Create mask for continuous segments
                mask = ~wave_data.isna()
                
                # Add wave line
                fig.add_trace(
                    go.Scatter(
                        x=wave_data.index,
                        y=wave_data.values,
                        mode='lines',
                        name='Wave',
                        line=dict(color='cyan', width=3),
                        showlegend=False
                    ),
                    row=1, col=1
                )
    except Exception as e:
        logger.print_error(f"Error adding Wave indicator: {e}")


def add_monte_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Monte Carlo indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Monte Carlo data
    """
    try:
        if 'monte_carlo' in display_df.columns:
            # Add Monte Carlo line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['monte_carlo'],
                    mode='lines',
                    name='Monte Carlo',
                    line=dict(color='purple', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            # Add confidence intervals if available
            if 'monte_carlo_upper' in display_df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=display_df.index,
                        y=display_df['monte_carlo_upper'],
                        mode='lines',
                        name='MC Upper',
                        line=dict(color='red', width=1, dash='dash'),
                        showlegend=False
                    ),
                    row=2, col=1
                )
            
            if 'monte_carlo_lower' in display_df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=display_df.index,
                        y=display_df['monte_carlo_lower'],
                        mode='lines',
                        name='MC Lower',
                        line=dict(color='green', width=1, dash='dash'),
                        showlegend=False
                    ),
                    row=2, col=1
                )
    except Exception as e:
        logger.print_error(f"Error adding Monte Carlo indicator: {e}")


def add_kelly_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Kelly Criterion indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Kelly Criterion data
    """
    try:
        if 'kelly' in display_df.columns:
            # Add Kelly line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['kelly'],
                    mode='lines',
                    name='Kelly Criterion',
                    line=dict(color='orange', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            # Add optimal position line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[0.25] * len(display_df),  # 25% optimal position
                    mode='lines',
                    name='Optimal Position',
                    line=dict(color='yellow', width=2, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
    except Exception as e:
        logger.print_error(f"Error adding Kelly Criterion indicator: {e}")


def add_donchain_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Donchian Channel indicator to the main chart.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Donchian Channel data
    """
    try:
        if 'donchian_upper' in display_df.columns:
            # Add upper channel
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['donchian_upper'],
                    mode='lines',
                    name='Donchian Upper',
                    line=dict(color='red', width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
        
        if 'donchian_lower' in display_df.columns:
            # Add lower channel
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['donchian_lower'],
                    mode='lines',
                    name='Donchian Lower',
                    line=dict(color='green', width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
        
        if 'donchian_middle' in display_df.columns:
            # Add middle line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['donchian_middle'],
                    mode='lines',
                    name='Donchian Middle',
                    line=dict(color='blue', width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
    except Exception as e:
        logger.print_error(f"Error adding Donchian Channel indicator: {e}")


def add_fibo_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Fibonacci Retracement indicator to the main chart.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Fibonacci data
    """
    try:
        if 'fibonacci' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['fibonacci'],
                    mode='lines',
                    name='Fibonacci',
                    line=dict(color='gold', width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
    except Exception as e:
        logger.print_error(f"Error adding Fibonacci indicator: {e}")


def add_adx_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add ADX indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with ADX data
    """
    try:
        if 'adx' in display_df.columns:
            # Add ADX line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['adx'],
                    mode='lines',
                    name='ADX',
                    line=dict(color='white', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            # Add trend strength line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[25] * len(display_df),
                    mode='lines',
                    name='Trend Strength',
                    line=dict(color='yellow', width=2, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
    except Exception as e:
        logger.print_error(f"Error adding ADX indicator: {e}")


def add_sar_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add SAR indicator to the main chart.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with SAR data
    """
    try:
        if 'sar' in display_df.columns:
            # Create discontinuous line traces for SAR
            sar_data = display_df['sar'].dropna()
            if not sar_data.empty:
                fig.add_trace(
                    go.Scatter(
                        x=sar_data.index,
                        y=sar_data.values,
                        mode='markers',
                        name='SAR',
                        marker=dict(
                            color='red',
                            size=4,
                            symbol='diamond'
                        ),
                        showlegend=False
                    ),
                    row=1, col=1
                )
    except Exception as e:
        logger.print_error(f"Error adding SAR indicator: {e}")


def add_rsi_div_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add RSI Divergence indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with RSI Divergence data
    """
    try:
        if 'rsi_div' in display_df.columns:
            # Add RSI divergence line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['rsi_div'],
                    mode='lines',
                    name='RSI Divergence',
                    line=dict(color='magenta', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            # Add divergence signals
            if 'rsi_div_signal' in display_df.columns:
                bullish_div = display_df[display_df['rsi_div_signal'] == 'BULLISH']
                bearish_div = display_df[display_df['rsi_div_signal'] == 'BEARISH']
                
                if not bullish_div.empty:
                    fig.add_trace(
                        go.Scatter(
                            x=bullish_div.index,
                            y=bullish_div['rsi_div'],
                            mode='markers',
                            name='Bullish Divergence',
                            marker=dict(
                                color='green',
                                size=8,
                                symbol='triangle-up'
                            ),
                            showlegend=False
                        ),
                        row=2, col=1
                    )
                
                if not bearish_div.empty:
                    fig.add_trace(
                        go.Scatter(
                            x=bearish_div.index,
                            y=bearish_div['rsi_div'],
                            mode='markers',
                            name='Bearish Divergence',
                            marker=dict(
                                color='red',
                                size=8,
                                symbol='triangle-down'
                            ),
                            showlegend=False
                        ),
                        row=2, col=1
                    )
    except Exception as e:
        logger.print_error(f"Error adding RSI Divergence indicator: {e}")


def add_stoch_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Stochastic indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Stochastic data
    """
    try:
        if 'stochastic' in display_df.columns:
            # Add Stochastic line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['stochastic'],
                    mode='lines',
                    name='Stochastic',
                    line=dict(color='blue', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            # Add overbought/oversold lines
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[80] * len(display_df),
                    mode='lines',
                    name='Stoch Overbought',
                    line=dict(color='red', width=2, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[20] * len(display_df),
                    mode='lines',
                    name='Stoch Oversold',
                    line=dict(color='green', width=2, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
    except Exception as e:
        logger.print_error(f"Error adding Stochastic indicator: {e}")


def add_stochoscillator_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Stochastic Oscillator indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Stochastic Oscillator data
    """
    try:
        if 'stoch_oscillator' in display_df.columns:
            # Add Stochastic Oscillator line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['stoch_oscillator'],
                    mode='lines',
                    name='Stochastic Oscillator',
                    line=dict(color='cyan', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            # Add overbought/oversold lines
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[80] * len(display_df),
                    mode='lines',
                    name='Stoch Osc Overbought',
                    line=dict(color='red', width=2, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[20] * len(display_df),
                    mode='lines',
                    name='Stoch Osc Oversold',
                    line=dict(color='green', width=2, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
    except Exception as e:
        logger.print_error(f"Error adding Stochastic Oscillator indicator: {e}")


def add_putcallratio_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Put/Call Ratio indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Put/Call Ratio data
    """
    try:
        if 'put_call_ratio' in display_df.columns:
            # Add Put/Call Ratio line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['put_call_ratio'],
                    mode='lines',
                    name='Put/Call Ratio',
                    line=dict(color='orange', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            # Add extreme levels
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[1.0] * len(display_df),
                    mode='lines',
                    name='Neutral Level',
                    line=dict(color='white', width=2, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[1.5] * len(display_df),
                    mode='lines',
                    name='Extreme Fear',
                    line=dict(color='red', width=2, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[0.5] * len(display_df),
                    mode='lines',
                    name='Extreme Greed',
                    line=dict(color='green', width=2, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
    except Exception as e:
        logger.print_error(f"Error adding Put/Call Ratio indicator: {e}")


def add_cot_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add COT indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with COT data
    """
    try:
        if 'cot' in display_df.columns:
            # Add COT line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['cot'],
                    mode='lines',
                    name='COT',
                    line=dict(color='purple', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            # Add sentiment levels
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[0] * len(display_df),
                    mode='lines',
                    name='Neutral Sentiment',
                    line=dict(color='white', width=2, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
    except Exception as e:
        logger.print_error(f"Error adding COT indicator: {e}")


def add_feargreed_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Fear & Greed indicator to the secondary subplot.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Fear & Greed data
    """
    try:
        if 'fear_greed' in display_df.columns:
            # Add Fear & Greed line
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['fear_greed'],
                    mode='lines',
                    name='Fear & Greed',
                    line=dict(color='magenta', width=3),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            # Add extreme levels
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[80] * len(display_df),
                    mode='lines',
                    name='Extreme Greed',
                    line=dict(color='red', width=2, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=[20] * len(display_df),
                    mode='lines',
                    name='Extreme Fear',
                    line=dict(color='green', width=2, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
    except Exception as e:
        logger.print_error(f"Error adding Fear & Greed indicator: {e}")


def add_supertrend_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add SuperTrend indicator to the main chart.
    
    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with SuperTrend data
    """
    try:
        if 'supertrend' in display_df.columns:
            # Create discontinuous line traces for SuperTrend
            supertrend_data = display_df['supertrend'].dropna()
            if not supertrend_data.empty:
                fig.add_trace(
                    go.Scatter(
                        x=supertrend_data.index,
                        y=supertrend_data.values,
                        mode='lines',
                        name='SuperTrend',
                        line=dict(color='lime', width=3),
                        showlegend=False
                    ),
                    row=1, col=1
                )
    except Exception as e:
        logger.print_error(f"Error adding SuperTrend indicator: {e}")
