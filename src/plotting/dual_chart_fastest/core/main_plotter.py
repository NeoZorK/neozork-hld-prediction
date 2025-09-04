# -*- coding: utf-8 -*-
# src/plotting/dual_chart_fastest/core/main_plotter.py

"""
Main plotter for dual chart fastest mode.
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

from ..utils.chart_utils import (
    add_ohlc_candlesticks, add_volume_bars, add_trading_signals,
    add_support_resistance_lines, add_pressure_vector, setup_figure_layout,
    save_and_open_chart
)

from ..indicators.basic_indicators import (
    add_rsi_indicator, add_rsi_momentum_indicator, add_macd_indicator,
    add_ema_indicator, add_sma_indicator, add_bollinger_bands_indicator,
    add_atr_indicator, add_cci_indicator, add_vwap_indicator,
    add_pivot_indicator, add_hma_indicator, add_tsf_indicator,
    add_obv_indicator, add_stdev_indicator
)

from ..indicators.advanced_indicators import (
    add_wave_indicator, add_monte_indicator, add_kelly_indicator,
    add_donchain_indicator, add_fibo_indicator, add_adx_indicator,
    add_sar_indicator, add_rsi_div_indicator, add_stoch_indicator,
    add_stochoscillator_indicator, add_putcallratio_indicator,
    add_cot_indicator, add_feargreed_indicator, add_supertrend_indicator
)


def plot_dual_chart_fastest(
    df: pd.DataFrame,
    rule: str,
    title: str = "Dual Chart Fastest",
    height: int = 800,
    filename: str = "dual_chart_fastest.html"
) -> None:
    """
    Create a dual chart with main OHLC chart and secondary indicator chart.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLC and indicator data
        rule (str): Trading rule/indicator name
        title (str): Chart title
        height (int): Chart height
        filename (str): Output filename
    """
    try:
        logger.print_info(f"🚀 Creating dual chart fastest for rule: {rule}")
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=('Price Chart', f'{rule.upper()} Indicator'),
            row_heights=[0.7, 0.3]
        )
        
        # Add main chart elements
        add_ohlc_candlesticks(fig, df, row=1, col=1)
        add_volume_bars(fig, df, row=1, col=1)
        add_trading_signals(fig, df, row=1, col=1)
        add_support_resistance_lines(fig, df, row=1, col=1)
        add_pressure_vector(fig, df, row=1, col=1)
        
        # Add indicator based on rule
        add_indicator_to_chart(fig, df, rule)
        
        # Setup layout
        setup_figure_layout(fig, title, height)
        
        # Save and open chart
        save_and_open_chart(fig, filename)
        
        logger.print_success(f"✅ Dual chart fastest created successfully for rule: {rule}")
        
    except Exception as e:
        logger.print_error(f"Error creating dual chart fastest: {e}")


def add_indicator_to_chart(fig: go.Figure, df: pd.DataFrame, rule: str) -> None:
    """
    Add specific indicator to chart based on rule.
    
    Args:
        fig: Plotly figure
        df: DataFrame with data
        rule: Trading rule/indicator name
    """
    try:
        rule_lower = rule.lower()
        
        # Route to appropriate indicator function
        if rule_lower == 'rsi':
            add_rsi_indicator(fig, df)
        elif rule_lower == 'rsi_mom':
            add_rsi_momentum_indicator(fig, df)
        elif rule_lower == 'rsi_div':
            add_rsi_div_indicator(fig, df)
        elif rule_lower == 'macd':
            add_macd_indicator(fig, df)
        elif rule_lower == 'ema':
            add_ema_indicator(fig, df)
        elif rule_lower == 'sma':
            add_sma_indicator(fig, df)
        elif rule_lower == 'bollinger':
            add_bollinger_bands_indicator(fig, df)
        elif rule_lower == 'atr':
            add_atr_indicator(fig, df)
        elif rule_lower == 'cci':
            add_cci_indicator(fig, df)
        elif rule_lower == 'vwap':
            add_vwap_indicator(fig, df)
        elif rule_lower == 'pivot':
            add_pivot_indicator(fig, df)
        elif rule_lower == 'hma':
            add_hma_indicator(fig, df)
        elif rule_lower == 'tsf':
            add_tsf_indicator(fig, df)
        elif rule_lower == 'obv':
            add_obv_indicator(fig, df)
        elif rule_lower == 'std':
            add_stdev_indicator(fig, df)
        elif rule_lower == 'wave':
            add_wave_indicator(fig, df)
        elif rule_lower == 'monte_carlo':
            add_monte_indicator(fig, df)
        elif rule_lower == 'kelly':
            add_kelly_indicator(fig, df)
        elif rule_lower == 'donchian':
            add_donchain_indicator(fig, df)
        elif rule_lower == 'fibonacci':
            add_fibo_indicator(fig, df)
        elif rule_lower == 'adx':
            add_adx_indicator(fig, df)
        elif rule_lower == 'sar':
            add_sar_indicator(fig, df)
        elif rule_lower == 'stochastic':
            add_stoch_indicator(fig, df)
        elif rule_lower == 'stoch_oscillator':
            add_stochoscillator_indicator(fig, df)
        elif rule_lower == 'put_call_ratio':
            add_putcallratio_indicator(fig, df)
        elif rule_lower == 'cot':
            add_cot_indicator(fig, df)
        elif rule_lower == 'fear_greed':
            add_feargreed_indicator(fig, df)
        elif rule_lower == 'supertrend':
            add_supertrend_indicator(fig, df)
        else:
            logger.print_warning(f"Unknown indicator rule: {rule}")
            
    except Exception as e:
        logger.print_error(f"Error adding indicator {rule} to chart: {e}")


def create_dual_chart_fastest(
    df: pd.DataFrame,
    rule: str,
    title: str = "Dual Chart Fastest",
    height: int = 800,
    filename: str = "dual_chart_fastest.html"
) -> go.Figure:
    """
    Create a dual chart figure without saving/opening.
    
    Args:
        df: DataFrame with OHLC and indicator data
        rule: Trading rule/indicator name
        title: Chart title
        height: Chart height
        filename: Output filename
    
    Returns:
        go.Figure: Plotly figure object
    """
    try:
        logger.print_info(f"🚀 Creating dual chart fastest figure for rule: {rule}")
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=('Price Chart', f'{rule.upper()} Indicator'),
            row_heights=[0.7, 0.3]
        )
        
        # Add main chart elements
        add_ohlc_candlesticks(fig, df, row=1, col=1)
        add_volume_bars(fig, df, row=1, col=1)
        add_trading_signals(fig, df, row=1, col=1)
        add_support_resistance_lines(fig, df, row=1, col=1)
        add_pressure_vector(fig, df, row=1, col=1)
        
        # Add indicator based on rule
        add_indicator_to_chart(fig, df, rule)
        
        # Setup layout
        setup_figure_layout(fig, title, height)
        
        logger.print_success(f"✅ Dual chart fastest figure created successfully for rule: {rule}")
        
        return fig
        
    except Exception as e:
        logger.print_error(f"Error creating dual chart fastest figure: {e}")
        return None
