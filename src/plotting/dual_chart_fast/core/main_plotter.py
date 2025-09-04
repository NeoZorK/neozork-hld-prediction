# -*- coding: utf-8 -*-
# src/plotting/dual_chart_fast/core/main_plotter.py

"""
Main plotter for dual chart fast mode.
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
    calculate_dynamic_height, setup_chart_layout, add_ohlc_candlesticks,
    add_volume_bars, add_trading_signals, add_support_resistance_lines,
    add_pressure_vector, save_and_open_chart, _get_indicator_hover_tool
)

from ..indicators.basic_indicators import (
    _plot_rsi_indicator, _plot_macd_indicator, _plot_ema_indicator,
    _plot_sma_indicator, _plot_bb_indicator, _plot_atr_indicator,
    _plot_cci_indicator, _plot_vwap_indicator, _plot_pivot_indicator,
    _plot_hma_indicator, _plot_tsf_indicator, _plot_obv_indicator,
    _plot_stdev_indicator
)

from ..indicators.advanced_indicators import (
    _plot_monte_indicator, _plot_kelly_indicator, _plot_donchain_indicator,
    _plot_fibo_indicator, _plot_adx_indicator, _plot_sar_indicator,
    _plot_rsi_mom_indicator, _plot_rsi_div_indicator, _plot_stoch_indicator,
    _plot_putcallratio_indicator, _plot_cot_indicator, _plot_feargreed_indicator,
    _plot_supertrend_indicator, _plot_wave_indicator
)


def _plot_indicator_by_type(indicator_fig, source, display_df, indicator_name):
    """
    Plot indicator by type.
    
    Args:
        indicator_fig: Plotly figure
        source: Data source
        display_df: DataFrame with data
        indicator_name: Name of the indicator
    """
    try:
        indicator_lower = indicator_name.lower()
        
        # Route to appropriate indicator function
        if indicator_lower == 'rsi':
            _plot_rsi_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'rsi_mom':
            _plot_rsi_mom_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'rsi_div':
            _plot_rsi_div_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'macd':
            _plot_macd_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'ema':
            _plot_ema_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'sma':
            _plot_sma_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'bollinger':
            _plot_bb_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'atr':
            _plot_atr_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'cci':
            _plot_cci_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'vwap':
            _plot_vwap_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'pivot':
            _plot_pivot_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'hma':
            _plot_hma_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'tsf':
            _plot_tsf_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'obv':
            _plot_obv_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'std':
            _plot_stdev_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'wave':
            _plot_wave_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'monte_carlo':
            _plot_monte_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'kelly':
            _plot_kelly_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'donchian':
            _plot_donchain_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'fibonacci':
            _plot_fibo_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'adx':
            _plot_adx_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'sar':
            _plot_sar_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'stochastic':
            _plot_stoch_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'put_call_ratio':
            _plot_putcallratio_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'cot':
            _plot_cot_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'fear_greed':
            _plot_feargreed_indicator(indicator_fig, source, display_df)
        elif indicator_lower == 'supertrend':
            _plot_supertrend_indicator(indicator_fig, source, display_df)
        else:
            logger.print_warning(f"Unknown indicator type: {indicator_name}")
            
    except Exception as e:
        logger.print_error(f"Error plotting indicator {indicator_name}: {e}")


def plot_dual_chart_fast(
    df: pd.DataFrame,
    rule: str,
    title: str = "Dual Chart Fast",
    height: int = None,
    filename: str = "dual_chart_fast.html"
) -> None:
    """
    Create a dual chart with main OHLC chart and secondary indicator chart.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLC and indicator data
        rule (str): Trading rule/indicator name
        title (str): Chart title
        height (int): Chart height (auto-calculated if None)
        filename (str): Output filename
    """
    try:
        logger.print_info(f"🚀 Creating dual chart fast for rule: {rule}")
        
        # Calculate dynamic height if not provided
        if height is None:
            height = calculate_dynamic_height(rule_str=rule)
        
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
        _plot_indicator_by_type(fig, None, df, rule)
        
        # Setup layout
        setup_chart_layout(fig, title, height)
        
        # Save and open chart
        save_and_open_chart(fig, filename)
        
        logger.print_success(f"✅ Dual chart fast created successfully for rule: {rule}")
        
    except Exception as e:
        logger.print_error(f"Error creating dual chart fast: {e}")


def create_dual_chart_fast(
    df: pd.DataFrame,
    rule: str,
    title: str = "Dual Chart Fast",
    height: int = None,
    filename: str = "dual_chart_fast.html"
) -> go.Figure:
    """
    Create a dual chart figure without saving/opening.
    
    Args:
        df: DataFrame with OHLC and indicator data
        rule: Trading rule/indicator name
        title: Chart title
        height: Chart height (auto-calculated if None)
        filename: Output filename
    
    Returns:
        go.Figure: Plotly figure object
    """
    try:
        logger.print_info(f"🚀 Creating dual chart fast figure for rule: {rule}")
        
        # Calculate dynamic height if not provided
        if height is None:
            height = calculate_dynamic_height(rule_str=rule)
        
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
        _plot_indicator_by_type(fig, None, df, rule)
        
        # Setup layout
        setup_chart_layout(fig, title, height)
        
        logger.print_success(f"✅ Dual chart fast figure created successfully for rule: {rule}")
        
        return fig
        
    except Exception as e:
        logger.print_error(f"Error creating dual chart fast figure: {e}")
        return None
