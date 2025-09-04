# -*- coding: utf-8 -*-
# src/plotting/dual_chart_fast/utils/__init__.py

"""
Utility functions for dual chart fast plotting.
"""

from .chart_utils import (
    _create_discontinuous_line_segments, get_screen_height, calculate_dynamic_height,
    setup_chart_layout, add_ohlc_candlesticks, add_volume_bars, add_trading_signals,
    add_support_resistance_lines, add_pressure_vector, save_and_open_chart,
    _get_indicator_hover_tool
)

__all__ = [
    '_create_discontinuous_line_segments',
    'get_screen_height',
    'calculate_dynamic_height',
    'setup_chart_layout',
    'add_ohlc_candlesticks',
    'add_volume_bars',
    'add_trading_signals',
    'add_support_resistance_lines',
    'add_pressure_vector',
    'save_and_open_chart',
    '_get_indicator_hover_tool'
]
