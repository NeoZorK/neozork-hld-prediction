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
    HoverTool, Span, Title, ColumnDataSource, NumeralTickFormatter, Div, BoxAnnotation
)
import webbrowser
from typing import Dict, Any, Optional

from ..common import logger


def get_screen_height():
    """
    Get the screen height in pixels.
    Returns a default value if screen height cannot be determined.
    """
    try:
        # Try to get screen height using tkinter
        import tkinter as tk
        root = tk.Tk()
        screen_height = root.winfo_screenheight()
        root.destroy()
        return screen_height
    except:
        try:
            # Try using platform-specific methods
            import subprocess
            if os.name == 'nt':  # Windows
                result = subprocess.run(['wmic', 'desktopmonitor', 'get', 'screenheight'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        return int(lines[1])
            else:  # Unix-like systems
                result = subprocess.run(['xrandr', '--query'], capture_output=True, text=True)
                if result.returncode == 0:
                    import re
                    match = re.search(r'(\d+)x(\d+)', result.stdout)
                    if match:
                        return int(match.group(2))
        except:
            pass
    
    # Default fallback values
    return 1080  # Default to 1080p height


def calculate_dynamic_height(screen_height=None, rule_str=None):
    """
    Calculate dynamic height for the chart based on screen height and rule.
    For dual chart mode, use 85% of screen height, min 400, max 2000.
    """
    if screen_height is None:
        screen_height = get_screen_height()
    if rule_str:
        dynamic_height = int(screen_height * 0.85)
        dynamic_height = max(400, min(dynamic_height, 2000))
        logger.print_info(f"Dual chart mode: using fullscreen height {dynamic_height}px (screen height: {screen_height}px)")
        return dynamic_height
    return 1100


def _plot_rsi_indicator(indicator_fig, source, display_df):
    """Plot RSI indicator on the given figure."""
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


def _plot_macd_indicator(indicator_fig, source, display_df):
    """Plot MACD indicator on the given figure."""
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
        # Color histogram bars - same as fastest mode
        colors = ['green' if val >= 0 else 'red' for val in display_df['macd_histogram']]
        display_df_copy = display_df.copy()
        display_df_copy['histogram_color'] = colors
        hist_source = ColumnDataSource(display_df_copy)
        
        indicator_fig.vbar(
            'index', 0.8, 0, 'macd_histogram',
            source=hist_source,
            fill_color='histogram_color',
            line_color='histogram_color',
            alpha=0.7,
            legend_label='Histogram'
        )


def _plot_ema_indicator(indicator_fig, source, display_df):
    """Plot EMA indicator on the given figure."""
    if 'ema' in display_df.columns:
        indicator_fig.line(
            'index', 'ema',
            source=source,
            line_color='orange',
            line_width=3,
            legend_label='EMA'
        )


def _plot_bb_indicator(indicator_fig, source, display_df):
    """Plot Bollinger Bands indicator on the given figure."""
    # Ensure BB data is available in the source for hover
    bb_columns = ['bb_upper', 'bb_middle', 'bb_lower']
    for col in bb_columns:
        if col in display_df.columns and col not in source.data:
            source.data[col] = display_df[col]
    
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


def _plot_atr_indicator(indicator_fig, source, display_df):
    """Plot ATR indicator on the given figure."""
    if 'atr' in display_df.columns:
        # Ensure ATR data is available in the source for hover
        if 'atr' not in source.data:
            source.data['atr'] = display_df['atr']
        
        indicator_fig.line(
            'index', 'atr',
            source=source,
            line_color='brown',
            line_width=3,
            legend_label='ATR'
        )


def _plot_cci_indicator(indicator_fig, source, display_df):
    """Plot CCI indicator on the given figure."""
    if 'cci' in display_df.columns:
        indicator_fig.line(
            'index', 'cci',
            source=source,
            line_color='purple',
            line_width=3,
            legend_label='CCI'
        )
        
        # Add CCI reference lines as columns for proper source handling
        display_df['cci_plus_100'] = 100
        display_df['cci_minus_100'] = -100
        
        # Add CCI reference lines
        indicator_fig.line(
            'index', 'cci_plus_100',
            source=source,
            line_color='red',
            line_width=1,
            line_dash='dashed',
            legend_label='CCI +100'
        )
        
        indicator_fig.line(
            'index', 'cci_minus_100',
            source=source,
            line_color='green',
            line_width=1,
            line_dash='dashed',
            legend_label='CCI -100'
        )


def _plot_vwap_indicator(indicator_fig, source, display_df):
    """Plot VWAP indicator on the given figure."""
    if 'vwap' in display_df.columns:
        indicator_fig.line(
            'index', 'vwap',
            source=source,
            line_color='orange',
            line_width=3,
            legend_label='VWAP'
        )


def _plot_pivot_indicator(indicator_fig, source, display_df):
    """Plot Pivot indicator on the given figure."""
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


def _plot_hma_indicator(indicator_fig, source, display_df):
    """Plot HMA indicator on the given figure."""
    if 'hma' in display_df.columns:
        indicator_fig.line(
            'index', 'hma',
            source=source,
            line_color='purple',
            line_width=3,
            legend_label='HMA'
        )


def _plot_tsf_indicator(indicator_fig, source, display_df):
    """Plot TSF indicator on the given figure."""
    if 'tsf' in display_df.columns:
        indicator_fig.line(
            'index', 'tsf',
            source=source,
            line_color='cyan',
            line_width=3,
            legend_label='TSF'
        )


def _plot_monte_indicator(indicator_fig, source, display_df):
    """Plot Monte Carlo indicator on the given figure."""
    # Add Monte Carlo forecast line (main line)
    if 'montecarlo' in display_df.columns:
        indicator_fig.line(
            'index', 'montecarlo',
            source=source,
            line_color='blue',
            line_width=3,
            legend_label='Monte Carlo Forecast'
        )
    
    # Add Monte Carlo signal line
    if 'montecarlo_signal' in display_df.columns:
        indicator_fig.line(
            'index', 'montecarlo_signal',
            source=source,
            line_color='red',
            line_width=2,
            legend_label='Signal Line'
        )
    
    # Add Monte Carlo histogram
    if 'montecarlo_histogram' in display_df.columns:
        # Color histogram bars based on values
        colors = ['green' if val >= 0 else 'red' for val in display_df['montecarlo_histogram']]
        display_df_copy = display_df.copy()
        display_df_copy['histogram_color'] = colors
        hist_source = ColumnDataSource(display_df_copy)
        
        indicator_fig.vbar(
            'index', 0.5, 'montecarlo_histogram',
            source=hist_source,
            color='histogram_color',
            alpha=0.7,
            legend_label='Histogram'
        )
    
    # Add confidence bands
    if 'montecarlo_upper' in display_df.columns:
        indicator_fig.line(
            'index', 'montecarlo_upper',
            source=source,
            line_color='lightblue',
            line_width=1,
            line_dash='dashed',
            legend_label='Upper Confidence'
        )
    
    if 'montecarlo_lower' in display_df.columns:
        indicator_fig.line(
            'index', 'montecarlo_lower',
            source=source,
            line_color='lightblue',
            line_width=1,
            line_dash='dashed',
            legend_label='Lower Confidence'
        )
    
    # Add zero line for histogram
    indicator_fig.line(
        'index', [0] * len(display_df),
        line_color='gray',
        line_width=1,
        line_dash='dashed',
        legend_label='Zero Line'
    )


def _plot_kelly_indicator(indicator_fig, source, display_df):
    """Plot Kelly indicator on the given figure."""
    if 'kelly' in display_df.columns:
        indicator_fig.line(
            'index', 'kelly',
            source=source,
            line_color='green',
            line_width=3,
            legend_label='Kelly'
        )


def _plot_donchain_indicator(indicator_fig, source, display_df):
    """Plot Donchian Channel indicator on the given figure."""
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


def _plot_fibo_indicator(indicator_fig, source, display_df):
    """Plot Fibonacci indicator on the given figure."""
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


def _plot_obv_indicator(indicator_fig, source, display_df):
    """Plot OBV indicator on the given figure."""
    if 'obv' in display_df.columns:
        indicator_fig.line(
            'index', 'obv',
            source=source,
            line_color='brown',
            line_width=3,
            legend_label='OBV'
        )


def _plot_stdev_indicator(indicator_fig, source, display_df):
    """Plot Standard Deviation indicator on the given figure."""
    if 'stdev' in display_df.columns:
        indicator_fig.line(
            'index', 'stdev',
            source=source,
            line_color='gray',
            line_width=3,
            legend_label='StdDev'
        )


def _plot_adx_indicator(indicator_fig, source, display_df):
    """Plot ADX indicator on the given figure."""
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


def _plot_sar_indicator(indicator_fig, source, display_df):
    """Plot SAR indicator on the given figure."""
    if 'sar' in display_df.columns:
        indicator_fig.scatter(
            'index', 'sar',
            source=source,
            size=4,
            color='red',
            legend_label='SAR'
        )


def _plot_rsi_mom_indicator(indicator_fig, source, display_df):
    """Plot RSI Momentum indicator on the given figure."""
    # Draw RSI line
    if 'rsi' in display_df.columns:
        indicator_fig.line(
            'index', 'rsi',
            source=source,
            line_color='blue',
            line_width=2,
            legend_label='RSI'
        )
    # Draw RSI Momentum line
    if 'rsi_momentum' in display_df.columns:
        indicator_fig.line(
            'index', 'rsi_momentum',
            source=source,
            line_color='orange',
            line_width=2,
            legend_label='RSI Momentum'
        )
    # Draw overbought/oversold levels
    if 'rsi_overbought' in display_df.columns:
        indicator_fig.line(
            'index', 'rsi_overbought',
            source=source,
            line_color='red',
            line_width=1,
            line_dash='dashed',
            legend_label='Overbought'
        )
    if 'rsi_oversold' in display_df.columns:
        indicator_fig.line(
            'index', 'rsi_oversold',
            source=source,
            line_color='green',
            line_width=1,
            line_dash='dashed',
            legend_label='Oversold'
        )


def _plot_rsi_div_indicator(indicator_fig, source, display_df):
    """Plot RSI Divergence indicator on the given figure."""
    # Draw RSI line
    if 'rsi' in display_df.columns:
        indicator_fig.line(
            'index', 'rsi',
            source=source,
            line_color='blue',
            line_width=2,
            legend_label='RSI'
        )
    # Draw RSI Divergence line
    if 'rsi_divergence' in display_df.columns:
        indicator_fig.line(
            'index', 'rsi_divergence',
            source=source,
            line_color='orange',
            line_width=2,
            legend_label='RSI Divergence'
        )
    # Draw overbought/oversold levels
    if 'rsi_overbought' in display_df.columns:
        indicator_fig.line(
            'index', 'rsi_overbought',
            source=source,
            line_color='red',
            line_width=1,
            line_dash='dashed',
            legend_label='Overbought'
        )
    if 'rsi_oversold' in display_df.columns:
        indicator_fig.line(
            'index', 'rsi_oversold',
            source=source,
            line_color='green',
            line_width=1,
            line_dash='dashed',
            legend_label='Oversold'
        )


def _plot_stoch_indicator(indicator_fig, source, display_df):
    """Plot Stochastic indicator on the given figure."""
    # Draw %K line
    if 'stoch_k' in display_df.columns:
        indicator_fig.line(
            'index', 'stoch_k',
            source=source,
            line_color='blue',
            line_width=2,
            legend_label='%K'
        )
    # Draw %D line
    if 'stoch_d' in display_df.columns:
        indicator_fig.line(
            'index', 'stoch_d',
            source=source,
            line_color='orange',
            line_width=2,
            legend_label='%D'
        )
    # Draw overbought/oversold levels
    if 'stoch_overbought' in display_df.columns:
        indicator_fig.line(
            'index', 'stoch_overbought',
            source=source,
            line_color='red',
            line_width=1,
            line_dash='dashed',
            legend_label='Overbought'
        )
    if 'stoch_oversold' in display_df.columns:
        indicator_fig.line(
            'index', 'stoch_oversold',
            source=source,
            line_color='green',
            line_width=1,
            line_dash='dashed',
            legend_label='Oversold'
        )


def _plot_putcallratio_indicator(indicator_fig, source, display_df):
    """Plot Put/Call Ratio indicator on the given figure."""
    # Main Put/Call Ratio line
    if 'PutCallRatio' in display_df.columns:
        indicator_fig.line(
            'index', 'PutCallRatio',
            source=source,
            line_color='purple',
            line_width=3,
            legend_label='Put/Call Ratio'
        )
    # Signal line (EMA)
    if 'PutCallRatio_Signal' in display_df.columns:
        indicator_fig.line(
            'index', 'PutCallRatio_Signal',
            source=source,
            line_color='orange',
            line_width=2,
            legend_label='Signal Line'
        )
    # Bullish threshold
    if 'putcallratio_bullish' in display_df.columns:
        indicator_fig.line(
            'index', 'putcallratio_bullish',
            source=source,
            line_color='green',
            line_width=1,
            line_dash='dashed',
            legend_label='Bullish Threshold'
        )
    # Bearish threshold
    if 'putcallratio_bearish' in display_df.columns:
        indicator_fig.line(
            'index', 'putcallratio_bearish',
            source=source,
            line_color='red',
            line_width=1,
            line_dash='dashed',
            legend_label='Bearish Threshold'
        )
    # Neutral level
    if 'putcallratio_neutral' in display_df.columns:
        indicator_fig.line(
            'index', 'putcallratio_neutral',
            source=source,
            line_color='gray',
            line_width=1,
            line_dash='dashed',
            legend_label='Neutral Level'
        )
    # Histogram (difference between PutCallRatio and Signal)
    if 'putcallratio_histogram' in display_df.columns:
        colors = ['green' if val >= 0 else 'red' for val in display_df['putcallratio_histogram']]
        display_df_copy = display_df.copy()
        display_df_copy['histogram_color'] = colors
        hist_source = ColumnDataSource(display_df_copy)
        indicator_fig.vbar(
            'index', 0.5, 'putcallratio_histogram',
            source=hist_source,
            color='histogram_color',
            alpha=0.7,
            legend_label='Histogram'
        )


def _plot_cot_indicator(indicator_fig, source, display_df):
    """Plot COT indicator on the given figure."""
    # Main COT line
    if 'cot' in display_df.columns:
        indicator_fig.line(
            'index', 'cot',
            source=source,
            line_color='darkblue',
            line_width=3,
            legend_label='COT'
        )
    # Signal line
    if 'cot_signal' in display_df.columns:
        indicator_fig.line(
            'index', 'cot_signal',
            source=source,
            line_color='darkorange',
            line_width=2,
            legend_label='Signal Line'
        )
    # Histogram
    if 'cot_histogram' in display_df.columns:
        colors = ['green' if val >= 0 else 'red' for val in display_df['cot_histogram']]
        display_df_copy = display_df.copy()
        display_df_copy['histogram_color'] = colors
        hist_source = ColumnDataSource(display_df_copy)
        indicator_fig.vbar(
            'index', 0.5, 'cot_histogram',
            source=hist_source,
            color='histogram_color',
            alpha=0.7,
            legend_label='Histogram'
        )


def _plot_feargreed_indicator(indicator_fig, source, display_df):
    """Plot Fear & Greed indicator on the given figure."""
    # Main Fear & Greed line
    if 'feargreed' in display_df.columns:
        indicator_fig.line(
            'index', 'feargreed',
            source=source,
            line_color='purple',
            line_width=3,
            legend_label='Fear & Greed'
        )
    # Signal line
    if 'feargreed_signal' in display_df.columns:
        indicator_fig.line(
            'index', 'feargreed_signal',
            source=source,
            line_color='orange',
            line_width=2,
            legend_label='Signal Line'
        )
    # Histogram
    if 'feargreed_histogram' in display_df.columns:
        colors = ['green' if val >= 0 else 'red' for val in display_df['feargreed_histogram']]
        display_df_copy = display_df.copy()
        display_df_copy['histogram_color'] = colors
        hist_source = ColumnDataSource(display_df_copy)
        indicator_fig.vbar(
            'index', 0.5, 'feargreed_histogram',
            source=hist_source,
            color='histogram_color',
            alpha=0.7,
            legend_label='Histogram'
        )
    # Bullish threshold
    if 'feargreed_bullish' in display_df.columns:
        indicator_fig.line(
            'index', 'feargreed_bullish',
            source=source,
            line_color='green',
            line_width=1,
            line_dash='dashed',
            legend_label='Bullish Threshold'
        )
    # Bearish threshold
    if 'feargreed_bearish' in display_df.columns:
        indicator_fig.line(
            'index', 'feargreed_bearish',
            source=source,
            line_color='red',
            line_width=1,
            line_dash='dashed',
            legend_label='Bearish Threshold'
        )
    # Neutral level
    if 'feargreed_neutral' in display_df.columns:
        indicator_fig.line(
            'index', 'feargreed_neutral',
            source=source,
            line_color='gray',
            line_width=1,
            line_dash='dashed',
            legend_label='Neutral Level'
        )


def _plot_supertrend_indicator(indicator_fig, source, display_df):
    """Plot SuperTrend indicator with modern style/colors like fastest mode."""
    import numpy as np
    import pandas as pd
    from bokeh.models import BoxAnnotation, ColumnDataSource

    # Check for required columns - support both old and new column names
    has_pprice = 'PPrice1' in display_df.columns and 'PPrice2' in display_df.columns
    has_supertrend = 'supertrend' in display_df.columns
    has_direction = 'Direction' in display_df.columns
    if not (has_pprice or has_supertrend) or not has_direction:
        return

    # Convert index to datetime if needed
    if not isinstance(display_df.index, pd.DatetimeIndex):
        display_df.index = pd.to_datetime(display_df.index)

    idx = display_df['index'] if 'index' in display_df.columns else display_df.index
    
    if has_pprice:
        p1 = display_df['PPrice1']
        p2 = display_df['PPrice2']
        direction = display_df['Direction']
        
        # Handle NaN values properly
        valid_mask = ~(pd.isna(p1) | pd.isna(p2) | pd.isna(direction))
        supertrend_values = np.full(len(direction), np.nan)
        supertrend_values[valid_mask] = np.where(direction[valid_mask] == 1, p1[valid_mask], p2[valid_mask])
        
        # Add values to both display_df and source for hover tool
        display_df['supertrend'] = supertrend_values
        source.data['supertrend'] = supertrend_values
        
        # Also ensure PPrice1 and PPrice2 are in source for fallback hover
        source.data['PPrice1'] = p1.fillna(0.0) if pd.api.types.is_numeric_dtype(p1) else p1
        source.data['PPrice2'] = p2.fillna(0.0) if pd.api.types.is_numeric_dtype(p2) else p2
        
        # Ensure Direction is also in the main source for hover tool
        if 'Direction' not in source.data:
            source.data['Direction'] = direction
    else:
        supertrend_values = display_df['supertrend']
        direction = display_df['Direction']
        # Ensure Direction is in the main source for hover tool
        if 'Direction' not in source.data:
            source.data['Direction'] = direction
    
    # Modern color scheme from fastest mode
    uptrend_color = '#00C851'      # Bright Green
    downtrend_color = '#ff4444'    # Bright Red
    neutral_color = '#888888'      # Gray
    glow_alpha = 0.15              # Transparency for glow effect
    
    # Get trend from Direction column (1=uptrend, 2=downtrend, 0=neutral)
    trend = display_df['Direction'].fillna(0)
    
    # Convert trend values for consistent color mapping (1=uptrend, -1=downtrend, 0=neutral)
    trend_for_colors = np.where(trend == 1, 1, np.where(trend == 2, -1, 0))
    
    # Add trend information to source data for hover
    trend_names = np.where(trend == 1, 'Uptrend', np.where(trend == 2, 'Downtrend', 'Neutral'))
    source.data['trend_name'] = trend_names
    
    # Verify data availability
    if len(trend) == 0:
        logger.print_warning("SuperTrend: No data available to plot")
        return
    
    # Create color arrays for visualization
    line_colors = np.where(trend_for_colors == 1, uptrend_color, 
                          np.where(trend_for_colors == -1, downtrend_color, neutral_color))
    source.data['line_colors'] = line_colors
    
    # Рисуем основную линию SuperTrend с правильными цветами через один источник данных
    # Разделяем на сегменты по тренду для корректного отображения цветов
    valid_indices = ~np.isnan(supertrend_values)
    if np.any(valid_indices):
        # Создаем сегменты для разных цветов
        # Добавляем проверку на случай пустого или одноэлементного массива
        if len(trend) == 1:
            trend_changes = np.array([0])  # Один элемент - нет изменений
        else:
            trend_changes = np.diff(trend.values, prepend=trend.iloc[0])
        change_points = np.where(trend_changes != 0)[0]
        
        # Добавляем начальную и конечную точки
        segments_starts = np.concatenate([[0], change_points])
        segments_ends = np.concatenate([change_points, [len(trend)]])
        
        for start_idx, end_idx in zip(segments_starts, segments_ends):
            if end_idx > start_idx:
                segment_indices = np.arange(start_idx, min(end_idx + 1, len(trend)))
                segment_trend = trend.iloc[start_idx]
                segment_color = uptrend_color if segment_trend == 1 else downtrend_color
                
                # Create separate source for each segment with complete hover data
                segment_data = display_df.iloc[segment_indices].copy()
                segment_data['index'] = segment_data.index
                segment_source = ColumnDataSource(segment_data)
                
                # Add SuperTrend data to segment source for proper hover functionality
                segment_source.data['supertrend'] = supertrend_values[segment_indices]
                if has_pprice:
                    segment_source.data['PPrice1'] = p1.iloc[segment_indices].fillna(0.0)
                    segment_source.data['PPrice2'] = p2.iloc[segment_indices].fillna(0.0)
                segment_source.data['Direction'] = direction.iloc[segment_indices]
                segment_source.data['trend_name'] = np.where(segment_trend == 1, 'Uptrend', 'Downtrend')
                
                # Draw glow effect first (wider, more transparent line)
                indicator_fig.line(
                    x='index',
                    y='supertrend',
                    source=segment_source,
                    line_color=segment_color,
                    line_width=12,
                    line_alpha=glow_alpha
                )
                
                # Draw main line segment
                legend_text = 'SuperTrend ' + ('Uptrend' if segment_trend == 1 else 'Downtrend')
                
                # Always use a string for legend_label
                line_params = {
                    'x': 'index',
                    'y': 'supertrend',
                    'source': segment_source,
                    'line_color': segment_color,
                    'line_width': 3,
                    'line_alpha': 0.9,
                    'legend_label': str(legend_text if start_idx == 0 else 'SuperTrend')
                }
                
                indicator_fig.line(**line_params)
    
    # Add BUY/SELL signals and transparent trend zones
    idx_arr = np.array(idx)
    st_arr = np.array(supertrend_values)
    
    # Detect trend changes
    trend_diff = trend.diff().fillna(0)
    buy_points = (trend_diff > 0)  # Change from downtrend to uptrend
    sell_points = (trend_diff < 0)  # Change from uptrend to downtrend
    
    # Add trend zones using BoxAnnotation
    trend_changes = np.where(trend_diff != 0)[0]
    if len(trend_changes) > 0:
        zone_starts = np.append([0], trend_changes)
        zone_ends = np.append(trend_changes, len(trend))
        
        for start_idx, end_idx in zip(zone_starts, zone_ends):
            zone_trend = trend.iloc[start_idx]
            zone_color = uptrend_color if zone_trend == 1 else downtrend_color if zone_trend == 2 else neutral_color
            
            indicator_fig.add_layout(BoxAnnotation(
                left=idx[start_idx],
                right=idx[min(end_idx, len(idx)-1)],
                fill_color=zone_color,
                fill_alpha=0.08,
                line_color=None
            ))
    
    # Add BUY signals with enhanced visibility
    if buy_points.any():
        buy_indices = trend.index[buy_points]
        buy_values = supertrend_values[buy_points]
        # Add glow effect for buy signals
        indicator_fig.scatter(
            x=buy_indices, y=buy_values,
            size=20, color=uptrend_color, marker='triangle',
            alpha=glow_alpha
        )
        # Main buy signal markers
        indicator_fig.scatter(
            x=buy_indices, y=buy_values,
            size=12, color=uptrend_color, marker='triangle',
            alpha=0.9, legend_label='Buy'
        )
    
    # Add SELL signals with enhanced visibility
    if sell_points.any():
        sell_indices = trend.index[sell_points]
        sell_values = supertrend_values[sell_points]
        # Add glow effect for sell signals
        indicator_fig.scatter(
            x=sell_indices, y=sell_values,
            size=20, color=downtrend_color, marker='inverted_triangle',
            alpha=glow_alpha
        )
        # Main sell signal markers
        indicator_fig.scatter(
            x=sell_indices, y=sell_values,
            size=12, color=downtrend_color, marker='inverted_triangle',
            alpha=0.9, legend_label='Sell'
        )


def _get_indicator_hover_tool(indicator_name, display_df, fibo_columns=None):
    """Get appropriate hover tool for the given indicator."""
    if indicator_name == 'macd':
        # Special hover for MACD with all three components
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("MACD", "@macd{0.5f}"),
                ("Signal", "@macd_signal{0.5f}"),
                ("Histogram", "@macd_histogram{0.5f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'rsi':
        # Special hover for RSI
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("RSI", "@rsi{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'rsi_mom':
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("RSI", "@rsi{0.2f}"),
                ("RSI Momentum", "@rsi_momentum{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'rsi_div':
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("RSI", "@rsi{0.2f}"),
                ("RSI Divergence", "@rsi_divergence{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'cci':
        # Special hover for CCI
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("CCI", "@cci{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'ema':
        # Special hover for EMA
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("EMA", "@ema{0.5f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'bb':
        # Special hover for Bollinger Bands
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("Upper Band", "@bb_upper{0.5f}"),
                ("Middle Band", "@bb_middle{0.5f}"),
                ("Lower Band", "@bb_lower{0.5f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'atr':
        # Special hover for ATR
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("ATR", "@atr{0.5f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'vwap':
        # Special hover for VWAP
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("VWAP", "@vwap{0.5f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'obv':
        # Special hover for OBV
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("OBV", "@obv{0.0f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'stdev':
        # Special hover for Standard Deviation
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("StdDev", "@stdev{0.5f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'adx':
        # Special hover for ADX
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("ADX", "@adx{0.2f}"),
                ("DI+", "@di_plus{0.2f}"),
                ("DI-", "@di_minus{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'sar':
        # Special hover for SAR
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("SAR", "@sar{0.5f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'stoch':
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("%K", "@stoch_k{0.2f}"),
                ("%D", "@stoch_d{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'hma':
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("HMA", "@hma{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'tsf':
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("TSF", "@tsf{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'monte':
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("Monte Carlo", "@montecarlo{0.2f}"),
                ("Signal", "@montecarlo_signal{0.2f}"),
                ("Histogram", "@montecarlo_histogram{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'montecarlo':
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("Monte Carlo", "@montecarlo{0.2f}"),
                ("Signal", "@montecarlo_signal{0.2f}"),
                ("Histogram", "@montecarlo_histogram{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'kelly':
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("Kelly Criterion", "@kelly{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'putcallratio':
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("Put/Call Ratio", "@PutCallRatio{0.2f}"),
                ("Signal Line", "@PutCallRatio_Signal{0.2f}"),
                ("Histogram", "@putcallratio_histogram{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'cot':
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("COT", "@cot{0.2f}"),
                ("Signal Line", "@cot_signal{0.2f}"),
                ("Histogram", "@cot_histogram{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'pivot':
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("Pivot", "@pivot{0.2f}"),
                ("R1", "@r1{0.2f}"),
                ("S1", "@s1{0.2f}"),
                ("R2", "@r2{0.2f}"),
                ("S2", "@s2{0.2f}"),
                ("R3", "@r3{0.2f}"),
                ("S3", "@s3{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name in ('feargreed', 'fg'):
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("Fear & Greed", "@feargreed{0.2f}"),
                ("Signal Line", "@feargreed_signal{0.2f}"),
                ("Histogram", "@feargreed_histogram{0.2f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'fibo':
        # Динамический тултип по реальным fibo колонкам
        tooltips = [("Date", "@index{%F %H:%M}")]
        if fibo_columns:
            for col in fibo_columns:
                try:
                    lvl = float(col.replace('fibo_', ''))
                    label = f"Fib {lvl}"
                except Exception:
                    label = col
                tooltips.append((label, f"@{col}{{0.5f}}"))
        return HoverTool(
            tooltips=tooltips,
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'donchain':
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("Upper Channel", "@donchain_upper{0.5f}"),
                ("Middle Channel", "@donchain_middle{0.5f}"),
                ("Lower Channel", "@donchain_lower{0.5f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'supertrend':
        # Enhanced hover tool for SuperTrend with fallback support
        tooltips = [
            ("Date", "@index{%F %H:%M}"),
        ]
        # Always show SuperTrend value if possible
        formatters = {'@index': 'datetime'}
        if 'supertrend' in display_df.columns:
            tooltips.append(("SuperTrend", "@supertrend{0.5f}"))
            formatters['@supertrend'] = 'numeral'
        elif 'PPrice1' in display_df.columns and 'PPrice2' in display_df.columns:
            tooltips.append(("Support (PPrice1)", "@PPrice1{0.5f}"))
            tooltips.append(("Resistance (PPrice2)", "@PPrice2{0.5f}"))
            formatters['@PPrice1'] = 'numeral'
            formatters['@PPrice2'] = 'numeral'
        # Always show Direction if present
        if 'Direction' in display_df.columns:
            tooltips.append(("Direction", "@Direction{0}"))
            formatters['@Direction'] = 'numeral'
        else:
            # Fallback: show Direction as N/A if not present
            tooltips.append(("Direction", "N/A"))
        return HoverTool(
            tooltips=tooltips,
            formatters=formatters,
            mode='mouse'  # Changed from vline to mouse to avoid overlap
        )
    else:
        # Generic hover for other indicators
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )


def _plot_indicator_by_type(indicator_fig, source, display_df, indicator_name):
    """Plot indicator based on type using the appropriate function."""
    indicator_plot_functions = {
        'rsi': _plot_rsi_indicator,
        'macd': _plot_macd_indicator,
        'ema': _plot_ema_indicator,
        'bb': _plot_bb_indicator,
        'atr': _plot_atr_indicator,
        'cci': _plot_cci_indicator,
        'vwap': _plot_vwap_indicator,
        'pivot': _plot_pivot_indicator,
        'hma': _plot_hma_indicator,
        'tsf': _plot_tsf_indicator,
        'monte': _plot_monte_indicator,
        'montecarlo': _plot_monte_indicator,  # Алиас для Monte Carlo
        'kelly': _plot_kelly_indicator,
        'donchain': _plot_donchain_indicator,
        'fibo': _plot_fibo_indicator,
        'obv': _plot_obv_indicator,
        'stdev': _plot_stdev_indicator,
        'adx': _plot_adx_indicator,
        'sar': _plot_sar_indicator,
        'rsi_mom': _plot_rsi_mom_indicator,
        'rsi_div': _plot_rsi_div_indicator,
        'stoch': _plot_stoch_indicator,
        'putcallratio': _plot_putcallratio_indicator,  # Добавлено для поддержки Put/Call Ratio
        'cot': _plot_cot_indicator,  # Добавлено для поддержки COT
        'feargreed': _plot_feargreed_indicator,  # Добавлено для поддержки Fear & Greed
        'fg': _plot_feargreed_indicator,         # Алиас
        'supertrend': _plot_supertrend_indicator,  # Добавлено для поддержки SuperTrend
    }
    fibo_columns = None
    if indicator_name == 'fibo':
        fibo_columns = [col for col in display_df.columns if col.startswith('fibo_')]
    plot_function = indicator_plot_functions.get(indicator_name)
    if plot_function:
        plot_function(indicator_fig, source, display_df)
    return fibo_columns


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
    
    # Calculate dynamic height and reduce sizes by 10%
    rule_str = rule.split(':', 1)[0].lower().strip()
    if height is None:
        height = calculate_dynamic_height(rule_str=rule_str)
    
    # Reduce height by 10% and width by 5% to ensure legend and buttons are fully visible
    width = int(width * 0.95)  # Reduce width by 5%
    height = int(height * 0.9)  # Reduce height by 10%
    
    logger.print_info(f"Using reduced sizes: width={width}px, height={height}px for rule: {rule_str}")
    
    # Prepare data
    display_df = df.copy()
    
    # Validate that we have data to plot
    if display_df.empty:
        logger.print_error("Cannot plot dual chart: DataFrame is empty")
        return None
    
    # Validate we have minimum required columns
    required_columns = ['Open', 'High', 'Low', 'Close']
    missing_columns = [col for col in required_columns if col not in display_df.columns]
    if missing_columns:
        logger.print_error(f"Cannot plot dual chart: Missing required columns: {missing_columns}")
        return None
    
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
    
    # Add hover tooltip for main chart - use mouse mode to avoid overlap
    hover_main = HoverTool(
        tooltips=[
            ("Date", "@index{%F %H:%M}"),
            ("Open", "@Open{0.5f}"),
            ("High", "@High{0.5f}"),
            ("Low", "@Low{0.5f}"),
            ("Close", "@Close{0.5f}")
        ],
        formatters={'@index': 'datetime'},
        mode='mouse'  # Changed from vline to mouse to avoid overlap
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
        active_scroll='wheel_zoom',
        x_range=main_fig.x_range  # Link x-axis to main chart
    )
    
    # Plot indicator using the refactored function and get fibo_columns if needed
    fibo_columns = _plot_indicator_by_type(indicator_fig, source, display_df, indicator_name)
    
    # Add hover tool for indicator chart
    hover_indicator = _get_indicator_hover_tool(indicator_name, display_df, fibo_columns=fibo_columns)
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