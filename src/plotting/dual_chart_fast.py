# -*- coding: utf-8 -*-
# src/plotting/dual_chart_fast.py

"""
Dual chart plotting for fast mode using Bokeh.
Creates a main OHLC chart with buy/sell signals and support/resistance lines,
plus a secondary chart below showing the selected indicator.
"""

import os
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column
from bokeh.models import (
    HoverTool, Span, Title, ColumnDataSource, NumeralTickFormatter, Div
)
import webbrowser
from typing import Dict, Any, Optional

from ..common import logger


def plot_dual_chart_fast(
    df: pd.DataFrame,
    rule: str,
    title: str = '',
    output_path: Optional[str] = None,
    width: int = 1800,
    height: int = 1100,
    layout: Optional[Dict[str, Any]] = None,
    **kwargs
):
    """
    Create dual chart plot using Bokeh for fast mode.
    
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
        None: Saves HTML file and opens in browser
    """
    # Set default output path
    if output_path is None:
        output_path = "results/plots/dual_chart_fast.html"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Prepare data
    display_df = df.copy()
    
    # Ensure index is datetime
    if not isinstance(display_df.index, pd.DatetimeIndex):
        if 'DateTime' in display_df.columns:
            display_df['DateTime'] = pd.to_datetime(display_df['DateTime'])
            display_df.set_index('DateTime', inplace=True)
        else:
            display_df.index = pd.to_datetime(display_df.index)
    
    # Add 'index' column for Bokeh compatibility
    display_df['index'] = display_df.index
    
    # Create data source for Bokeh
    source = ColumnDataSource(display_df)
    
    # Create main figure for OHLC chart
    main_fig = figure(
        width=width,
        height=int(height * 0.6),
        title=title,
        x_axis_type='datetime',
        tools="pan,wheel_zoom,box_zoom,reset,save",
        active_scroll='wheel_zoom'
    )
    
    # Add candlestick chart
    # Upward candles (green)
    up_candles = display_df[display_df['Close'] >= display_df['Open']]
    if not up_candles.empty:
        up_source = ColumnDataSource(up_candles)
        main_fig.segment(
            'index', 'High', 'index', 'Low',
            source=up_source, color='green', line_width=2
        )
        main_fig.vbar(
            'index', 0.5, 'Open', 'Close',
            source=up_source, fill_color='green', line_color='green'
        )
    
    # Downward candles (red)
    down_candles = display_df[display_df['Close'] < display_df['Open']]
    if not down_candles.empty:
        down_source = ColumnDataSource(down_candles)
        main_fig.segment(
            'index', 'High', 'index', 'Low',
            source=down_source, color='red', line_width=2
        )
        main_fig.vbar(
            'index', 0.5, 'Open', 'Close',
            source=down_source, fill_color='red', line_color='red'
        )
    
    # Add support and resistance lines if available
    if 'Support' in display_df.columns:
        main_fig.line(
            'index', 'Support',
            source=source,
            line_color='blue',
            line_width=2,
            line_dash='dashed',
            legend_label='Support',
            alpha=0.8
        )
    
    if 'Resistance' in display_df.columns:
        main_fig.line(
            'index', 'Resistance',
            source=source,
            line_color='red',
            line_width=2,
            line_dash='dashed',
            legend_label='Resistance',
            alpha=0.8
        )
    
    # Add trading signals if available
    if 'Direction' in display_df.columns:
        buy_signals = display_df[display_df['Direction'] == 1]
        sell_signals = display_df[display_df['Direction'] == 2]
        
        if not buy_signals.empty:
            buy_source = ColumnDataSource(buy_signals)
            main_fig.scatter(
                'index', 'Low',
                source=buy_source,
                size=12, color='green', alpha=0.7,
                legend_label='Buy Signal',
                marker='triangle'
            )
        
        if not sell_signals.empty:
            sell_source = ColumnDataSource(sell_signals)
            main_fig.scatter(
                'index', 'High',
                source=sell_source,
                size=12, color='red', alpha=0.7,
                legend_label='Sell Signal',
                marker='inverted_triangle'
            )
    
    # Add hover tooltip for main chart
    hover_main = HoverTool(
        tooltips=[
            ("Date", "@index{%F %H:%M}"),
            ("Open", "@Open{0.5f}"),
            ("High", "@High{0.5f}"),
            ("Low", "@Low{0.5f}"),
            ("Close", "@Close{0.5f}")
        ],
        formatters={'@index': 'datetime'},
        mode='vline'
    )
    main_fig.add_tools(hover_main)
    
    # Create indicator figure
    indicator_name = rule.split(':', 1)[0].lower().strip()
    indicator_title = layout['indicator_name'] if layout else 'Indicator'
    
    indicator_fig = figure(
        width=width,
        height=int(height * 0.4),
        title=indicator_title,
        x_axis_type='datetime',
        tools="pan,wheel_zoom,box_zoom,reset",
        active_scroll='wheel_zoom'
    )
    
    # Add indicator based on type
    if indicator_name == 'rsi':
        if 'rsi' in display_df.columns:
            indicator_fig.line(
                'index', 'rsi',
                source=source,
                line_color='purple',
                line_width=3,
                legend_label='RSI'
            )
            
            # Add overbought/oversold lines
            if 'rsi_overbought' in display_df.columns:
                overbought = display_df['rsi_overbought'].iloc[0]
                indicator_fig.line(
                    'index', [overbought] * len(display_df),
                    line_color='red',
                    line_width=2,
                    line_dash='dashed',
                    legend_label=f'Overbought ({overbought})'
                )
            
            if 'rsi_oversold' in display_df.columns:
                oversold = display_df['rsi_oversold'].iloc[0]
                indicator_fig.line(
                    'index', [oversold] * len(display_df),
                    line_color='green',
                    line_width=2,
                    line_dash='dashed',
                    legend_label=f'Oversold ({oversold})'
                )
    
    elif indicator_name == 'macd':
        if 'macd' in display_df.columns:
            indicator_fig.line(
                'index', 'macd',
                source=source,
                line_color='blue',
                line_width=3,
                legend_label='MACD'
            )
        
        if 'macd_signal' in display_df.columns:
            indicator_fig.line(
                'index', 'macd_signal',
                source=source,
                line_color='red',
                line_width=2,
                legend_label='Signal'
            )
        
        if 'macd_histogram' in display_df.columns:
            # Color histogram bars
            colors = ['green' if val >= 0 else 'red' for val in display_df['macd_histogram']]
            display_df['histogram_color'] = colors
            hist_source = ColumnDataSource(display_df)
            
            indicator_fig.vbar(
                'index', 0.5, 'macd_histogram',
                source=hist_source,
                color='histogram_color',
                alpha=0.7,
                legend_label='Histogram'
            )
    
    elif indicator_name == 'ema':
        if 'ema' in display_df.columns:
            indicator_fig.line(
                'index', 'ema',
                source=source,
                line_color='orange',
                line_width=3,
                legend_label='EMA'
            )
    
    elif indicator_name == 'bb':
        if 'bb_upper' in display_df.columns:
            indicator_fig.line(
                'index', 'bb_upper',
                source=source,
                line_color='blue',
                line_width=2,
                legend_label='Upper Band'
            )
        
        if 'bb_middle' in display_df.columns:
            indicator_fig.line(
                'index', 'bb_middle',
                source=source,
                line_color='gray',
                line_width=2,
                legend_label='Middle Band'
            )
        
        if 'bb_lower' in display_df.columns:
            indicator_fig.line(
                'index', 'bb_lower',
                source=source,
                line_color='blue',
                line_width=2,
                legend_label='Lower Band'
            )
    
    elif indicator_name == 'atr':
        if 'atr' in display_df.columns:
            indicator_fig.line(
                'index', 'atr',
                source=source,
                line_color='brown',
                line_width=3,
                legend_label='ATR'
            )
    
    elif indicator_name == 'cci':
        if 'cci' in display_df.columns:
            indicator_fig.line(
                'index', 'cci',
                source=source,
                line_color='purple',
                line_width=3,
                legend_label='CCI'
            )
            
            # Add CCI reference lines
            indicator_fig.line(
                'index', [100] * len(display_df),
                line_color='red',
                line_width=1,
                line_dash='dashed',
                legend_label='CCI +100'
            )
            
            indicator_fig.line(
                'index', [-100] * len(display_df),
                line_color='green',
                line_width=1,
                line_dash='dashed',
                legend_label='CCI -100'
            )
    
    elif indicator_name == 'vwap':
        if 'vwap' in display_df.columns:
            indicator_fig.line(
                'index', 'vwap',
                source=source,
                line_color='orange',
                line_width=3,
                legend_label='VWAP'
            )
    
    elif indicator_name == 'pivot':
        if 'pivot' in display_df.columns:
            indicator_fig.line(
                'index', 'pivot',
                source=source,
                line_color='blue',
                line_width=2,
                legend_label='Pivot'
            )
        
        if 'r1' in display_df.columns:
            indicator_fig.line(
                'index', 'r1',
                source=source,
                line_color='red',
                line_width=1,
                line_dash='dashed',
                legend_label='R1'
            )
        
        if 's1' in display_df.columns:
            indicator_fig.line(
                'index', 's1',
                source=source,
                line_color='green',
                line_width=1,
                line_dash='dashed',
                legend_label='S1'
            )
    
    elif indicator_name == 'hma':
        if 'hma' in display_df.columns:
            indicator_fig.line(
                'index', 'hma',
                source=source,
                line_color='purple',
                line_width=3,
                legend_label='HMA'
            )
    
    elif indicator_name == 'tsf':
        if 'tsf' in display_df.columns:
            indicator_fig.line(
                'index', 'tsf',
                source=source,
                line_color='cyan',
                line_width=3,
                legend_label='TSF'
            )
    
    elif indicator_name == 'monte':
        if 'monte_expected_return' in display_df.columns:
            indicator_fig.line(
                'index', 'monte_expected_return',
                source=source,
                line_color='blue',
                line_width=3,
                legend_label='Expected Return'
            )
    
    elif indicator_name == 'kelly':
        if 'kelly' in display_df.columns:
            indicator_fig.line(
                'index', 'kelly',
                source=source,
                line_color='green',
                line_width=3,
                legend_label='Kelly'
            )
    
    elif indicator_name == 'donchain':
        if 'donchain_upper' in display_df.columns:
            indicator_fig.line(
                'index', 'donchain_upper',
                source=source,
                line_color='blue',
                line_width=2,
                legend_label='Upper Channel'
            )
        
        if 'donchain_middle' in display_df.columns:
            indicator_fig.line(
                'index', 'donchain_middle',
                source=source,
                line_color='gray',
                line_width=2,
                legend_label='Middle Channel'
            )
        
        if 'donchain_lower' in display_df.columns:
            indicator_fig.line(
                'index', 'donchain_lower',
                source=source,
                line_color='blue',
                line_width=2,
                legend_label='Lower Channel'
            )
    
    elif indicator_name == 'fibo':
        # Add Fibonacci levels
        fibo_cols = [col for col in display_df.columns if col.startswith('fibo_')]
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
        
        for i, col in enumerate(fibo_cols):
            color = colors[i % len(colors)]
            indicator_fig.line(
                'index', col,
                source=source,
                line_color=color,
                line_width=2,
                legend_label=col.replace('fibo_', 'Fib ')
            )
    
    elif indicator_name == 'obv':
        if 'obv' in display_df.columns:
            indicator_fig.line(
                'index', 'obv',
                source=source,
                line_color='brown',
                line_width=3,
                legend_label='OBV'
            )
    
    elif indicator_name == 'stdev':
        if 'stdev' in display_df.columns:
            indicator_fig.line(
                'index', 'stdev',
                source=source,
                line_color='gray',
                line_width=3,
                legend_label='StdDev'
            )
    
    elif indicator_name == 'adx':
        if 'adx' in display_df.columns:
            indicator_fig.line(
                'index', 'adx',
                source=source,
                line_color='purple',
                line_width=3,
                legend_label='ADX'
            )
        
        if 'di_plus' in display_df.columns:
            indicator_fig.line(
                'index', 'di_plus',
                source=source,
                line_color='green',
                line_width=2,
                legend_label='DI+'
            )
        
        if 'di_minus' in display_df.columns:
            indicator_fig.line(
                'index', 'di_minus',
                source=source,
                line_color='red',
                line_width=2,
                legend_label='DI-'
            )
    
    elif indicator_name == 'sar':
        if 'sar' in display_df.columns:
            indicator_fig.scatter(
                'index', 'sar',
                source=source,
                size=4,
                color='red',
                legend_label='SAR'
            )
    
    # Add hover tooltip for indicator chart
    hover_indicator = HoverTool(
        tooltips=[
            ("Date", "@index{%F %H:%M}"),
            ("Value", "@$name{0.5f}")
        ],
        formatters={'@index': 'datetime'},
        mode='vline'
    )
    indicator_fig.add_tools(hover_indicator)
    
    # Create layout
    layout_figures = column(main_fig, indicator_fig)
    
    # Save and open
    output_file(output_path)
    save(layout_figures)
    
    abs_path = os.path.abspath(output_path)
    webbrowser.open_new_tab(f"file://{abs_path}")
    
    logger.print_info(f"Dual chart saved to: {abs_path}")
    
    return layout_figures 