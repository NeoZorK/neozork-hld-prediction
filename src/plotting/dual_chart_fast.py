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

from src.common import logger


def _create_discontinuous_line_segments(x_data, y_data, mask):
    """
    Create discontinuous line segments where mask is True.
    This prevents interpolation between points where there are no signals.
    
    Args:
        x_data: X-axis data (index)
        y_data: Y-axis data (values)
        mask: Boolean mask indicating where to draw lines
    
    Returns:
        List of DataFrames, each containing a continuous segment
    """
    segments = []
    
    if not mask.any():
        return segments
    
    # Convert mask to numpy array for easier processing
    mask_array = mask.values
    
    # Find continuous segments where mask is True
    # Use numpy diff to find transitions
    transitions = np.diff(np.concatenate(([False], mask_array, [False])).astype(int))
    starts = np.where(transitions == 1)[0]  # Transitions from False to True
    ends = np.where(transitions == -1)[0] - 1  # Transitions from True to False (adjust index)
    
    # Create segments for each continuous segment
    for start_idx, end_idx in zip(starts, ends):
        if start_idx <= end_idx:  # Valid segment
            # Handle both Series and Index for x_data
            if hasattr(x_data, 'iloc'):
                segment_x = x_data.iloc[start_idx:end_idx+1]
            else:
                segment_x = x_data[start_idx:end_idx+1]
            
            # y_data should always be a Series
            segment_y = y_data.iloc[start_idx:end_idx+1]
            
            # Only create segment if we have at least one point
            if len(segment_x) > 0:
                # Create DataFrame for this segment
                segment_df = pd.DataFrame({
                    'index': segment_x,
                    y_data.name: segment_y
                })
                segments.append(segment_df)
    
    return segments


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


def _plot_sma_indicator(indicator_fig, source, display_df):
    """Plot SMA indicator on the given figure."""
    if 'sma' in display_df.columns:
        indicator_fig.line(
            'index', 'sma',
            source=source,
            line_color='blue',
            line_width=3,
            legend_label='SMA'
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

    idx = display_df['index'] if 'index' in display_df.columns else display_df.index
    if has_pprice:
        p1 = display_df['PPrice1']
        p2 = display_df['PPrice2']
        direction = display_df['Direction']
        
        # Handle NaN values properly - only compute supertrend where both p1 and p2 are not NaN
        valid_mask = ~(pd.isna(p1) | pd.isna(p2))
        supertrend_values = np.full(len(direction), np.nan)
        supertrend_values[valid_mask] = np.where(direction[valid_mask] > 0, p1[valid_mask], p2[valid_mask])
        
        # Add supertrend values to both display_df and source for hover tool
        display_df['supertrend'] = supertrend_values
        if source is not None:
            source.data['supertrend'] = supertrend_values
            
            # Also ensure PPrice1 and PPrice2 are in source for fallback hover
            # Keep NaN values as NaN for proper numeric formatting in hover tool
            source.data['PPrice1'] = p1
            source.data['PPrice2'] = p2
            
            # Ensure Direction is also in the main source for hover tool
            if 'Direction' not in source.data:
                source.data['Direction'] = direction
                
            # Ensure all required columns are in source for proper hover functionality
            source.data['index'] = display_df['index'] if 'index' in display_df.columns else display_df.index
    else:
        supertrend_values = display_df['supertrend']
        direction = display_df['Direction']
        # Ensure Direction is in the main source for hover tool
        if source is not None and 'Direction' not in source.data:
            source.data['Direction'] = direction
            
        # Ensure supertrend values are in source for hover tool
        if source is not None and 'supertrend' not in source.data:
            source.data['supertrend'] = supertrend_values
    
    # Colors and style like in fastest
    uptrend_color = '#00C851'  # Green
    downtrend_color = '#FF4444'  # Red
    signal_change_color = '#FFC107'  # Golden
    
    # Determine trend (analog to fastest)
    if 'Close' in display_df.columns:
        price_series = display_df['Close']
    elif 'close' in display_df.columns:
        price_series = display_df['close']
    else:
        # If no price column available, use supertrend values as reference
        price_series = supertrend_values
    
    trend = np.where(price_series > supertrend_values, 1, -1)
    trend = pd.Series(trend, index=display_df.index)
    
    # Add trend colors to the main source for proper hover functionality
    trend_colors = np.where(trend == 1, uptrend_color, downtrend_color)
    if source is not None:
        source.data['supertrend_color'] = trend_colors
        
        # Removed invisible line that was causing multiple hover tooltips
        # The indicator chart already has its own hover tool, so this invisible line
        # was redundant and causing the "3 dates" issue
    
    # Now draw the visual segments for styling
    # Segmentation with signal change consideration
    segments = []
    color_arr = np.where(trend == 1, uptrend_color, downtrend_color)
    idx_arr = np.array(idx)
    st_arr = np.array(supertrend_values)
    last_color = color_arr[0]
    seg_x, seg_y = [idx_arr[0]], [st_arr[0]]
    for i in range(1, len(idx_arr)):
        current_color = color_arr[i]
        # Signal change
        if (trend.iloc[i] == 1 and trend.iloc[i-1] == -1) or (trend.iloc[i] == -1 and trend.iloc[i-1] == 1):
            if len(seg_x) > 1:
                segments.append((seg_x.copy(), seg_y.copy(), last_color))
            # Insert yellow segment
            segments.append(([idx_arr[i-1], idx_arr[i]], [st_arr[i-1], st_arr[i]], signal_change_color))
            seg_x, seg_y = [idx_arr[i]], [st_arr[i]]
            last_color = current_color
        elif current_color != last_color:
            segments.append((seg_x.copy(), seg_y.copy(), last_color))
            seg_x, seg_y = [idx_arr[i-1]], [st_arr[i-1]]
            last_color = current_color
        seg_x.append(idx_arr[i])
        seg_y.append(st_arr[i])
    if len(seg_x) > 0:
        segments.append((seg_x, seg_y, last_color))
    
    # Draw lines and glow with different labels in legend
    legend_shown = {uptrend_color: False, downtrend_color: False, signal_change_color: False}
    for seg_x, seg_y, seg_color in segments:
        if len(seg_x) > 1:
            # Glow
            glow_color = seg_color + '4D'  # Add 30% opacity (4D in hex)
            indicator_fig.line(
                x=seg_x, y=seg_y,
                line_color=glow_color, line_width=10, line_alpha=1.0
            )
            # Legend
            if seg_color == uptrend_color:
                legend_label = 'SuperTrend (Uptrend)'
            elif seg_color == downtrend_color:
                legend_label = 'SuperTrend (Downtrend)'
            elif seg_color == signal_change_color:
                legend_label = 'SuperTrend (Signal Change)'
            else:
                legend_label = 'SuperTrend'
            show_legend = not legend_shown.get(seg_color, False)
            legend_shown[seg_color] = True
            line_kwargs = dict(x=seg_x, y=seg_y, line_color=seg_color, line_width=5, line_alpha=1.0)
            if show_legend:
                line_kwargs['legend_label'] = legend_label
            
            # Create line with proper source for hover
            segment_source = ColumnDataSource({
                'x': seg_x,
                'y': seg_y,
                'supertrend': seg_y  # Add supertrend column for hover
            })
            
            # Update line_kwargs to use source properly
            line_kwargs = dict(
                x='x', y='y',  # Use column names when using source
                source=segment_source,
                line_color=seg_color, 
                line_width=5, 
                line_alpha=1.0
            )
            if show_legend:
                line_kwargs['legend_label'] = legend_label
            
            indicator_fig.line(**line_kwargs)
    
    # BUY/SELL signals with white outline and pulse
    buy_idx = idx_arr[(trend == 1) & (trend.shift(1) == -1)]
    sell_idx = idx_arr[(trend == -1) & (trend.shift(1) == 1)]
    buy_y = st_arr[(trend == 1) & (trend.shift(1) == -1)]
    sell_y = st_arr[(trend == -1) & (trend.shift(1) == 1)]
    # BUY
    if len(buy_idx) > 0:
        indicator_fig.scatter(
            x=buy_idx, y=buy_y,
            size=18, color='#00C851', marker='triangle', alpha=0.95, legend_label='BUY Signal',
            line_color='white', line_width=2.5
        )
        indicator_fig.scatter(
            x=buy_idx, y=buy_y,
            size=28, color='rgba(0, 200, 81, 0.4)', marker='circle', alpha=0.4
        )
    # SELL
    if len(sell_idx) > 0:
        indicator_fig.scatter(
            x=sell_idx, y=sell_y,
            size=18, color='#FF4444', marker='inverted_triangle', alpha=0.95, legend_label='SELL Signal',
            line_color='white', line_width=2.5
        )
        indicator_fig.scatter(
            x=sell_idx, y=sell_y,
            size=28, color='rgba(255, 68, 68, 0.4)', marker='circle', alpha=0.4
        )
    # Transparent trend zones
    trend_changes = idx_arr[trend != trend.shift(1)]
    if len(trend_changes) > 0:
        for i in range(len(trend_changes)):
            start_idx = trend_changes[i]
            end_idx = trend_changes[i + 1] if i + 1 < len(trend_changes) else idx_arr[-1]
            # Find the index of start_idx in idx_arr
            start_idx_pos = np.where(idx_arr == start_idx)[0][0]
            zone_color = '#00C851' if trend.iloc[start_idx_pos] == 1 else '#FF4444'
            indicator_fig.add_layout(BoxAnnotation(
                left=start_idx, right=end_idx,
                fill_color=zone_color + '14', fill_alpha=0.08,  # 14 in hex = 8% opacity
                line_color=zone_color + '33', line_alpha=0.2, line_width=1  # 33 in hex = 20% opacity
            ))
    
    # Add hover tool for SuperTrend indicator
    hover_supertrend = HoverTool(
        tooltips=[
            ("Value", "@supertrend{0.5f}")
        ],
        formatters={},
        mode='vline'
    )
    indicator_fig.add_tools(hover_supertrend)


def _plot_wave_indicator(indicator_fig, source, display_df):
    """Plot Wave indicator on the given figure."""
    # Add Plot Wave (main indicator, single line with dynamic colors) - as per MQ5
    plot_wave_col = None
    plot_color_col = None
    if '_plot_wave' in display_df.columns:
        plot_wave_col = '_plot_wave'
    elif '_Plot_Wave' in display_df.columns:
        plot_wave_col = '_Plot_Wave'
    
    if '_plot_color' in display_df.columns:
        plot_color_col = '_plot_color'
    elif '_Plot_Color' in display_df.columns:
        plot_color_col = '_Plot_Color'
    
    if plot_wave_col and plot_color_col:
        # Create discontinuous line segments like in fastest mode
        valid_data_mask = display_df[plot_wave_col].notna() & (display_df[plot_wave_col] != 0)
        if valid_data_mask.any():
            wave_data = display_df[valid_data_mask].copy()
            
            # Create masks for different signal types
            red_mask = wave_data[plot_color_col] == 1
            blue_mask = wave_data[plot_color_col] == 2
            
            # Create discontinuous line segments for red (BUY = 1)
            if red_mask.any():
                red_segments = _create_discontinuous_line_segments(
                    wave_data.index, 
                    wave_data[plot_wave_col], 
                    red_mask
                )
                for segment_data in red_segments:
                    segment_source = ColumnDataSource(segment_data)
                    indicator_fig.line(
                        'index', plot_wave_col,
                        source=segment_source,
                        line_color='red',
                        line_width=2,
                        legend_label='Wave'
                    )
            
            # Create discontinuous line segments for blue (SELL = 2)
            if blue_mask.any():
                blue_segments = _create_discontinuous_line_segments(
                    wave_data.index, 
                    wave_data[plot_wave_col], 
                    blue_mask
                )
                for segment_data in blue_segments:
                    segment_source = ColumnDataSource(segment_data)
                    indicator_fig.line(
                        'index', plot_wave_col,
                        source=segment_source,
                        line_color='blue',
                        line_width=2,
                        legend_label='Wave'
                    )
    
    # Add Plot FastLine (thin red dotted line) - as per MQ5
    plot_fastline_col = None
    if '_plot_fastline' in display_df.columns:
        plot_fastline_col = '_plot_fastline'
    elif '_Plot_FastLine' in display_df.columns:
        plot_fastline_col = '_Plot_FastLine'
    
    if plot_fastline_col:
        # Only show Fast Line when there are valid values
        fastline_valid_mask = display_df[plot_fastline_col].notna() & (display_df[plot_fastline_col] != 0)
        if fastline_valid_mask.any():
            fastline_valid_data = display_df[fastline_valid_mask]
            fastline_source = ColumnDataSource(fastline_valid_data)
            indicator_fig.line(
                'index', plot_fastline_col,
                source=fastline_source,
                line_color='red',
                line_width=1,
                line_dash='dotted',
                legend_label='Fast Line'
            )
    
    # Add MA Line (light blue line) - as per MQ5
    ma_line_col = None
    if 'ma_line' in display_df.columns:
        ma_line_col = 'ma_line'
    elif 'MA_Line' in display_df.columns:
        ma_line_col = 'MA_Line'
    
    if ma_line_col:
        # Only show MA Line when there are valid values
        ma_valid_mask = display_df[ma_line_col].notna() & (display_df[ma_line_col] != 0)
        if ma_valid_mask.any():
            ma_valid_data = display_df[ma_valid_mask]
            ma_source = ColumnDataSource(ma_valid_data)
            indicator_fig.line(
                'index', ma_line_col,
                source=ma_source,
                line_color='lightblue',
                line_width=1,
                legend_label='MA Line'
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
        # Dynamic tooltip based on real fibo columns
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
        # Always use supertrend column (created in _plot_supertrend_indicator)
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("SuperTrend", "@supertrend{0.5f}"),
                ("Direction", "@Direction")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    elif indicator_name == 'wave':
        # Special hover for Wave indicator
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("Wave", "@_Plot_Wave{0.5f}"),
                ("Fast Line", "@_Plot_FastLine{0.5f}"),
                ("MA Line", "@MA_Line{0.5f}"),
                ("Signal", "@_Plot_Color")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
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
        'sma': _plot_sma_indicator,
        'bb': _plot_bb_indicator,
        'atr': _plot_atr_indicator,
        'cci': _plot_cci_indicator,
        'vwap': _plot_vwap_indicator,
        'pivot': _plot_pivot_indicator,
        'hma': _plot_hma_indicator,
        'tsf': _plot_tsf_indicator,
        'monte': _plot_monte_indicator,
        'montecarlo': _plot_monte_indicator,  # Alias for Monte Carlo
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
        'putcallratio': _plot_putcallratio_indicator,  # Added for Put/Call Ratio support
        'cot': _plot_cot_indicator,  # Added for COT support
        'feargreed': _plot_feargreed_indicator,  # Added for Fear & Greed support
        'fg': _plot_feargreed_indicator,         # Alias
        'supertrend': _plot_supertrend_indicator,  # Added for SuperTrend support
        'wave': _plot_wave_indicator, # Added for Wave indicator support
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
        output_path = "../results/../plots/dual_chart_fast.html"
    
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
    
    # Add trading signals if available - check both _Signal and Direction columns
    signal_col = None
    if '_Signal' in display_df.columns:
        signal_col = '_Signal'
    elif 'Direction' in display_df.columns:
        signal_col = 'Direction'
    
    if signal_col:
        buy_signals = display_df[display_df[signal_col] == 1]
        sell_signals = display_df[display_df[signal_col] == 2]
        
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
    
    # Add hover tool for indicator chart (only for non-supertrend indicators)
    if indicator_name != 'supertrend':
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