# -*- coding: utf-8 -*-
# src/plotting/dual_chart_fast/indicators/advanced_indicators.py

"""
Advanced indicator functions for dual chart fast plotting.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Dict, Any, Optional

from src.common import logger


def _plot_monte_indicator(indicator_fig, source, display_df):
    """
    Plot Monte Carlo indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with Monte Carlo data
    """
    try:
        if 'monte_carlo' in display_df.columns:
            # Add Monte Carlo line
            indicator_fig.add_trace(
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
                indicator_fig.add_trace(
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
                indicator_fig.add_trace(
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
        logger.print_error(f"Error plotting Monte Carlo indicator: {e}")


def _plot_kelly_indicator(indicator_fig, source, display_df):
    """
    Plot Kelly Criterion indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with Kelly Criterion data
    """
    try:
        if 'kelly' in display_df.columns:
            # Add Kelly line
            indicator_fig.add_trace(
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
            indicator_fig.add_trace(
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
        logger.print_error(f"Error plotting Kelly Criterion indicator: {e}")


def _plot_donchain_indicator(indicator_fig, source, display_df):
    """
    Plot Donchian Channel indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with Donchian Channel data
    """
    try:
        if 'donchian_upper' in display_df.columns:
            # Add upper channel
            indicator_fig.add_trace(
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
            indicator_fig.add_trace(
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
            indicator_fig.add_trace(
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
        logger.print_error(f"Error plotting Donchian Channel indicator: {e}")


def _plot_fibo_indicator(indicator_fig, source, display_df):
    """
    Plot Fibonacci Retracement indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with Fibonacci data
    """
    try:
        if 'fibonacci' in display_df.columns:
            indicator_fig.add_trace(
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
        logger.print_error(f"Error plotting Fibonacci indicator: {e}")


def _plot_adx_indicator(indicator_fig, source, display_df):
    """
    Plot ADX indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with ADX data
    """
    try:
        if 'adx' in display_df.columns:
            # Add ADX line
            indicator_fig.add_trace(
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
            indicator_fig.add_trace(
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
        logger.print_error(f"Error plotting ADX indicator: {e}")


def _plot_sar_indicator(indicator_fig, source, display_df):
    """
    Plot SAR indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with SAR data
    """
    try:
        if 'sar' in display_df.columns:
            # Create discontinuous line traces for SAR
            sar_data = display_df['sar'].dropna()
            if not sar_data.empty:
                indicator_fig.add_trace(
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
        logger.print_error(f"Error plotting SAR indicator: {e}")


def _plot_rsi_mom_indicator(indicator_fig, source, display_df):
    """
    Plot RSI Momentum indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with RSI Momentum data
    """
    try:
        if 'rsi_mom' in display_df.columns:
            # Add RSI momentum line
            indicator_fig.add_trace(
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
            indicator_fig.add_trace(
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
        logger.print_error(f"Error plotting RSI Momentum indicator: {e}")


def _plot_rsi_div_indicator(indicator_fig, source, display_df):
    """
    Plot RSI Divergence indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with RSI Divergence data
    """
    try:
        if 'rsi_div' in display_df.columns:
            # Add RSI divergence line
            indicator_fig.add_trace(
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
                    indicator_fig.add_trace(
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
                    indicator_fig.add_trace(
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
        logger.print_error(f"Error plotting RSI Divergence indicator: {e}")


def _plot_stoch_indicator(indicator_fig, source, display_df):
    """
    Plot Stochastic indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with Stochastic data
    """
    try:
        if 'stochastic' in display_df.columns:
            # Add Stochastic line
            indicator_fig.add_trace(
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
            indicator_fig.add_trace(
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
            
            indicator_fig.add_trace(
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
        logger.print_error(f"Error plotting Stochastic indicator: {e}")


def _plot_putcallratio_indicator(indicator_fig, source, display_df):
    """
    Plot Put/Call Ratio indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with Put/Call Ratio data
    """
    try:
        if 'put_call_ratio' in display_df.columns:
            # Add Put/Call Ratio line
            indicator_fig.add_trace(
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
            indicator_fig.add_trace(
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
            
            indicator_fig.add_trace(
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
            
            indicator_fig.add_trace(
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
        logger.print_error(f"Error plotting Put/Call Ratio indicator: {e}")


def _plot_cot_indicator(indicator_fig, source, display_df):
    """
    Plot COT indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with COT data
    """
    try:
        if 'cot' in display_df.columns:
            # Add COT line
            indicator_fig.add_trace(
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
            indicator_fig.add_trace(
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
        logger.print_error(f"Error plotting COT indicator: {e}")


def _plot_feargreed_indicator(indicator_fig, source, display_df):
    """
    Plot Fear & Greed indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with Fear & Greed data
    """
    try:
        if 'fear_greed' in display_df.columns:
            # Add Fear & Greed line
            indicator_fig.add_trace(
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
            indicator_fig.add_trace(
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
            
            indicator_fig.add_trace(
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
        logger.print_error(f"Error plotting Fear & Greed indicator: {e}")


def _plot_supertrend_indicator(indicator_fig, source, display_df):
    """
    Plot SuperTrend indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with SuperTrend data
    """
    try:
        if 'supertrend' in display_df.columns:
            # Create discontinuous line traces for SuperTrend
            supertrend_data = display_df['supertrend'].dropna()
            if not supertrend_data.empty:
                indicator_fig.add_trace(
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
        logger.print_error(f"Error plotting SuperTrend indicator: {e}")


def _plot_wave_indicator(indicator_fig, source, display_df):
    """
    Plot Wave indicator.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with Wave data
    """
    try:
        if 'wave' in display_df.columns:
            # Create discontinuous line traces for wave
            wave_data = display_df['wave'].dropna()
            if not wave_data.empty:
                # Add wave line
                indicator_fig.add_trace(
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
        logger.print_error(f"Error plotting Wave indicator: {e}")
