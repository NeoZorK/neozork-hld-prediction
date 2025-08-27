# -*- coding: utf-8 -*-
# src/plotting/dual_chart_seaborn.py

"""
Dual chart plotting for seaborn mode using seaborn and matplotlib.
Creates a main OHLC chart with buy/sell signals and support/resistance lines,
plus a secondary chart below showing the selected indicator.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from typing import Dict, Any, Optional

from src.common import logger


def _create_wave_line_segments(index, values, mask):
    """
    Create discontinuous line segments for Wave indicator.
    
    Args:
        index: Index array
        values: Values array
        mask: Boolean mask for valid segments
        
    Returns:
        list: List of (x, y) segment tuples
    """
    segments = []
    if not mask.any():
        return segments
    
    # Find continuous segments
    segment_start = None
    for i, is_valid in enumerate(mask):
        if is_valid and segment_start is None:
            segment_start = i
        elif not is_valid and segment_start is not None:
            # End of segment
            segments.append((
                index[segment_start:i],
                values[segment_start:i]
            ))
            segment_start = None
    
    # Handle last segment
    if segment_start is not None:
        segments.append((
            index[segment_start:],
            values[segment_start:]
        ))
    
    return segments


def plot_dual_chart_seaborn(
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
    Create dual chart plot using seaborn for sb mode.
    
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
        matplotlib.figure.Figure: Figure object
    """
    # Set default output path
    if output_path is None:
        output_path = "results/plots/dual_chart_seaborn.png"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Set modern seaborn style with enhanced aesthetics
    sns.set_style("whitegrid", {
        'grid.linestyle': '--',
        'grid.alpha': 0.3,
        'axes.facecolor': '#f8f9fa',
        'figure.facecolor': 'white',
        'axes.spines.top': False,
        'axes.spines.right': False
    })
    sns.set_palette("husl")
    
    # Set modern font settings
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif']
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 16
    
    # Prepare data
    display_df = df.copy()
    
    # Ensure index is datetime
    if not isinstance(display_df.index, pd.DatetimeIndex):
        if 'DateTime' in display_df.columns:
            display_df['DateTime'] = pd.to_datetime(display_df['DateTime'])
            display_df.set_index('DateTime', inplace=True)
        else:
            display_df.index = pd.to_datetime(display_df.index)
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(width/100, height/100), 
                                   height_ratios=[0.6, 0.4], 
                                   sharex=True)
    
    # Main chart (OHLC)
    ax1.set_title(title, fontsize=14, fontweight='bold')
    
    # Plot candlesticks with modern styling
    for i, (date, row) in enumerate(display_df.iterrows()):
        # Determine color based on open/close with modern colors
        if row['Close'] >= row['Open']:
            color = '#00C851'  # Modern green
            body_color = '#E8F5E8'  # Light green background
        else:
            color = '#FF4444'  # Modern red
            body_color = '#FFE8E8'  # Light red background
        
        # Plot high-low line with enhanced styling
        ax1.plot([date, date], [row['Low'], row['High']], color=color, linewidth=1.5, alpha=0.8)
        
        # Plot open-close body with modern styling
        body_height = abs(row['Close'] - row['Open'])
        body_bottom = min(row['Open'], row['Close'])
        
        rect = Rectangle((date - pd.Timedelta(hours=6), body_bottom), 
                        pd.Timedelta(hours=12), body_height,
                        facecolor=body_color, edgecolor=color, linewidth=1.5, alpha=0.9)
        ax1.add_patch(rect)
    
    # Add support and resistance lines if available with modern styling
    if 'Support' in display_df.columns:
        sns.lineplot(data=display_df, x=display_df.index, y='Support', 
                    ax=ax1, color='#007BFF', linestyle='--', linewidth=2.5, alpha=0.9, label='Support')
    
    if 'Resistance' in display_df.columns:
        sns.lineplot(data=display_df, x=display_df.index, y='Resistance', 
                    ax=ax1, color='#DC3545', linestyle='--', linewidth=2.5, alpha=0.9, label='Resistance')
    
    # Add buy/sell signals if available with modern styling
    if 'Direction' in display_df.columns:
        buy_signals = display_df[display_df['Direction'] == 1]
        sell_signals = display_df[display_df['Direction'] == 2]
        
        if not buy_signals.empty:
            ax1.scatter(buy_signals.index, buy_signals['Low'] * 0.995, 
                       color='#00C851', marker='^', s=120, edgecolors='white', linewidth=2,
                       alpha=0.95, label='Buy Signal', zorder=5)
            # Add pulse effect for buy signals
            ax1.scatter(buy_signals.index, buy_signals['Low'] * 0.995, 
                       color='#00C851', marker='o', s=180, alpha=0.3, label="", zorder=4)
        
        if not sell_signals.empty:
            ax1.scatter(sell_signals.index, sell_signals['High'] * 1.005, 
                       color='#FF4444', marker='v', s=120, edgecolors='white', linewidth=2,
                       alpha=0.95, label='Sell Signal', zorder=5)
            # Add pulse effect for sell signals
            ax1.scatter(sell_signals.index, sell_signals['High'] * 1.005, 
                       color='#FF4444', marker='o', s=180, alpha=0.3, label="", zorder=4)
    
    # Add Wave indicator signals to main chart if available
    plot_color_col = None
    if '_plot_color' in display_df.columns:
        plot_color_col = '_plot_color'
    elif '_Plot_Color' in display_df.columns:
        plot_color_col = '_Plot_Color'
    
    if plot_color_col:
        # Get Wave buy and sell signals - use _Signal for actual trading signals (only when direction changes)
        signal_col = None
        if '_signal' in display_df.columns:
            signal_col = '_signal'
        elif '_Signal' in display_df.columns:
            signal_col = '_Signal'
        
        if signal_col:
            # Use _Signal for actual trading signals (only when direction changes)
            wave_buy_signals = display_df[display_df[signal_col] == 1]  # BUY = 1
            wave_sell_signals = display_df[display_df[signal_col] == 2]  # SELL = 2
        else:
            # Fallback to _Plot_Color if _Signal not available
            wave_buy_signals = display_df[display_df[plot_color_col] == 1]  # BUY = 1
            wave_sell_signals = display_df[display_df[plot_color_col] == 2]  # SELL = 2
        
        # Add buy signals to main chart
        if not wave_buy_signals.empty:
            ax1.scatter(wave_buy_signals.index, wave_buy_signals['Low'] * 0.995, 
                       color='#0066CC', marker='^', s=100, label='Wave BUY', zorder=5, alpha=0.9)
        
        # Add sell signals to main chart
        if not wave_sell_signals.empty:
            ax1.scatter(wave_sell_signals.index, wave_sell_signals['High'] * 1.005, 
                       color='#FF4444', marker='v', s=100, label='Wave SELL', zorder=5, alpha=0.9)
    
    ax1.set_ylabel('Price', fontsize=12)
    # Only show legend if there are labeled artists
    if ax1.get_legend_handles_labels()[0]:
        ax1.legend()
    
    # Format x-axis for main chart
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # Calculate appropriate interval based on data length and time range
    data_length = len(display_df)
    date_range = display_df.index.max() - display_df.index.min()
    days_range = date_range.days
    
    # Choose appropriate locator based on time range
    if days_range > 365 * 5:  # More than 5 years
        ax1.xaxis.set_major_locator(mdates.YearLocator(2))  # Every 2 years
    elif days_range > 365 * 2:  # More than 2 years
        ax1.xaxis.set_major_locator(mdates.YearLocator(1))  # Every year
    elif days_range > 365:  # More than 1 year
        ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Every 3 months
    elif days_range > 90:  # More than 3 months
        ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Every month
    else:  # Less than 3 months
        ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days_range // 10)))
    
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Indicator chart
    indicator_name = rule.split(':', 1)[0].lower().strip()
    indicator_title = layout['indicator_name'] if layout else 'Indicator'
    ax2.set_title(indicator_title, fontsize=12, fontweight='bold')
    
    # Add indicator based on type with modern styling
    if indicator_name == 'rsi':
        if 'rsi' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='rsi', 
                        ax=ax2, color='#9C27B0', linewidth=3, alpha=0.9, label='RSI')
            
            # Add overbought/oversold lines with modern styling
            if 'rsi_overbought' in display_df.columns:
                overbought = display_df['rsi_overbought'].iloc[0]
                ax2.axhline(y=overbought, color='#FF4444', linestyle='--', 
                           linewidth=2.5, alpha=0.8, label=f'Overbought ({overbought})')
            
            if 'rsi_oversold' in display_df.columns:
                oversold = display_df['rsi_oversold'].iloc[0]
                ax2.axhline(y=oversold, color='#00C851', linestyle='--', 
                           linewidth=2.5, alpha=0.8, label=f'Oversold ({oversold})')
    
    elif indicator_name == 'rsi_mom':
        if 'rsi' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='rsi', 
                        ax=ax2, color='purple', linewidth=2, label='RSI')
        
        if 'rsi_momentum' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='rsi_momentum', 
                        ax=ax2, color='orange', linewidth=2, label='RSI Momentum')
            
            # Add zero line for momentum
            ax2.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        
        # Add overbought/oversold lines
        if 'rsi_overbought' in display_df.columns:
            overbought = display_df['rsi_overbought'].iloc[0]
            ax2.axhline(y=overbought, color='red', linestyle='--', 
                       linewidth=2, label=f'Overbought ({overbought})')
        
        if 'rsi_oversold' in display_df.columns:
            oversold = display_df['rsi_oversold'].iloc[0]
            ax2.axhline(y=oversold, color='green', linestyle='--', 
                       linewidth=2, label=f'Oversold ({oversold})')
    
    elif indicator_name == 'rsi_div':
        if 'rsi' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='rsi', 
                        ax=ax2, color='purple', linewidth=2, label='RSI')
        
        if 'rsi_divergence' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='rsi_divergence', 
                        ax=ax2, color='orange', linewidth=2, label='RSI Divergence')
            
            # Add zero line for divergence
            ax2.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        
        # Add overbought/oversold lines
        if 'rsi_overbought' in display_df.columns:
            overbought = display_df['rsi_overbought'].iloc[0]
            ax2.axhline(y=overbought, color='red', linestyle='--', 
                       linewidth=2, label=f'Overbought ({overbought})')
        
        if 'rsi_oversold' in display_df.columns:
            oversold = display_df['rsi_oversold'].iloc[0]
            ax2.axhline(y=oversold, color='green', linestyle='--', 
                       linewidth=2, label=f'Oversold ({oversold})')
    
    elif indicator_name == 'macd':
        if 'macd' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='macd', 
                        ax=ax2, color='#2196F3', linewidth=3, alpha=0.9, label='MACD')
        
        if 'macd_signal' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='macd_signal', 
                        ax=ax2, color='#FF4444', linewidth=2.5, alpha=0.9, label='Signal')
        
        if 'macd_histogram' in display_df.columns:
            # Color histogram bars with modern colors
            colors = ['#00C851' if val >= 0 else '#FF4444' for val in display_df['macd_histogram']]
            ax2.bar(display_df.index, display_df['macd_histogram'], 
                   color=colors, alpha=0.8, label='Histogram', width=0.8)
    
    elif indicator_name == 'ema':
        if 'ema' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='ema', 
                        ax=ax2, color='orange', linewidth=3, label='EMA')
    
    elif indicator_name == 'sma':
        if 'sma' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='sma', 
                        ax=ax2, color='blue', linewidth=3, label='SMA')
    
    elif indicator_name == 'bb':
        if 'bb_upper' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='bb_upper', 
                        ax=ax2, color='blue', linewidth=2, label='Upper Band')
        
        if 'bb_middle' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='bb_middle', 
                        ax=ax2, color='gray', linewidth=2, label='Middle Band')
        
        if 'bb_lower' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='bb_lower', 
                        ax=ax2, color='blue', linewidth=2, label='Lower Band')
    
    elif indicator_name == 'atr':
        if 'atr' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='atr', 
                        ax=ax2, color='brown', linewidth=3, label='ATR')
    
    elif indicator_name == 'cci':
        if 'cci' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='cci', 
                        ax=ax2, color='purple', linewidth=3, label='CCI')
            
            # Add CCI reference lines
            ax2.axhline(y=100, color='red', linestyle='--', linewidth=1, label='CCI +100')
            ax2.axhline(y=-100, color='green', linestyle='--', linewidth=1, label='CCI -100')
    
    elif indicator_name == 'vwap':
        if 'vwap' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='vwap', 
                        ax=ax2, color='orange', linewidth=3, label='VWAP')
    
    elif indicator_name == 'pivot':
        if 'pivot' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='pivot', 
                        ax=ax2, color='blue', linewidth=2, label='Pivot')
        
        if 'r1' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='r1', 
                        ax=ax2, color='red', linestyle='--', linewidth=1, label='R1')
        
        if 's1' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='s1', 
                        ax=ax2, color='green', linestyle='--', linewidth=1, label='S1')
    
    elif indicator_name == 'hma':
        if 'hma' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='hma', 
                        ax=ax2, color='purple', linewidth=3, label='HMA')
    
    elif indicator_name == 'tsf':
        if 'tsf' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='tsf', 
                        ax=ax2, color='cyan', linewidth=3, label='TSF')
    
    elif indicator_name == 'monte':
        # Add Monte Carlo forecast line (main line)
        if 'montecarlo' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='montecarlo', 
                        ax=ax2, color='blue', linewidth=3, label='Monte Carlo Forecast')
        
        # Add Monte Carlo signal line
        if 'montecarlo_signal' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='montecarlo_signal', 
                        ax=ax2, color='red', linewidth=2, label='Signal Line')
        
        # Add Monte Carlo histogram
        if 'montecarlo_histogram' in display_df.columns:
            # Color histogram bars based on values
            colors = ['green' if val >= 0 else 'red' for val in display_df['montecarlo_histogram']]
            ax2.bar(display_df.index, display_df['montecarlo_histogram'], 
                   color=colors, alpha=0.7, label='Histogram', width=0.8)
        
        # Add confidence bands
        if 'montecarlo_upper' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='montecarlo_upper', 
                        ax=ax2, color='lightblue', linewidth=1, linestyle='--', label='Upper Confidence')
        
        if 'montecarlo_lower' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='montecarlo_lower', 
                        ax=ax2, color='lightblue', linewidth=1, linestyle='--', label='Lower Confidence')
        
        # Add zero line for histogram
        ax2.axhline(y=0, color='gray', linestyle='--', linewidth=1, label='Zero Line')
    
    elif indicator_name == 'kelly':
        if 'kelly' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='kelly', 
                        ax=ax2, color='green', linewidth=3, label='Kelly')
    
    elif indicator_name == 'donchain':
        if 'donchain_upper' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='donchain_upper', 
                        ax=ax2, color='blue', linewidth=2, label='Upper Channel')
        
        if 'donchain_middle' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='donchain_middle', 
                        ax=ax2, color='gray', linewidth=2, label='Middle Channel')
        
        if 'donchain_lower' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='donchain_lower', 
                        ax=ax2, color='blue', linewidth=2, label='Lower Channel')
    
    elif indicator_name == 'fibo':
        # Add Fibonacci levels
        fibo_cols = [col for col in display_df.columns if col.startswith('fibo_')]
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
        
        for i, col in enumerate(fibo_cols):
            color = colors[i % len(colors)]
            sns.lineplot(data=display_df, x=display_df.index, y=col, 
                        ax=ax2, color=color, linewidth=2, label=col.replace('fibo_', 'Fib '))
    
    elif indicator_name == 'obv':
        if 'obv' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='obv', 
                        ax=ax2, color='brown', linewidth=3, label='OBV')
    
    elif indicator_name == 'stdev':
        if 'stdev' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='stdev', 
                        ax=ax2, color='gray', linewidth=3, label='StdDev')
    
    elif indicator_name == 'stoch':
        if 'stoch_k' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='stoch_k', 
                        ax=ax2, color='blue', linewidth=3, label='%K')
        
        if 'stoch_d' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='stoch_d', 
                        ax=ax2, color='orange', linewidth=3, label='%D')
        
        # Add overbought/oversold lines
        if 'stoch_overbought' in display_df.columns:
            overbought = display_df['stoch_overbought'].iloc[0]
            ax2.axhline(y=overbought, color='red', linestyle='--', 
                       linewidth=2, label=f'Overbought ({overbought})')
        
        if 'stoch_oversold' in display_df.columns:
            oversold = display_df['stoch_oversold'].iloc[0]
            ax2.axhline(y=oversold, color='green', linestyle='--', 
                       linewidth=2, label=f'Oversold ({oversold})')
    
    elif indicator_name == 'stochoscillator':
        if 'stochosc_k' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='stochosc_k', 
                        ax=ax2, color='blue', linewidth=3, label='%K')
        
        if 'stochosc_d' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='stochosc_d', 
                        ax=ax2, color='orange', linewidth=3, label='%D')
        
        # Add overbought/oversold lines
        if 'stochosc_overbought' in display_df.columns:
            overbought = display_df['stochosc_overbought'].iloc[0]
            ax2.axhline(y=overbought, color='red', linestyle='--', 
                       linewidth=2, label=f'Overbought ({overbought})')
        
        if 'stochosc_oversold' in display_df.columns:
            oversold = display_df['stochosc_oversold'].iloc[0]
            ax2.axhline(y=oversold, color='green', linestyle='--', 
                       linewidth=2, label=f'Oversold ({oversold})')
    
    elif indicator_name == 'putcallratio':
        if 'putcallratio' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='putcallratio', 
                        ax=ax2, color='brown', linewidth=3, label='Put/Call Ratio')
        
        if 'putcallratio_signal' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='putcallratio_signal', 
                        ax=ax2, color='orange', linewidth=2, label='Signal Line')
        
        # Add threshold levels
        if 'putcallratio_bullish' in display_df.columns:
            bullish = display_df['putcallratio_bullish'].iloc[0]
            ax2.axhline(y=bullish, color='green', linestyle='--', 
                       linewidth=2, label=f'Bullish Threshold ({bullish})')
        
        if 'putcallratio_bearish' in display_df.columns:
            bearish = display_df['putcallratio_bearish'].iloc[0]
            ax2.axhline(y=bearish, color='red', linestyle='--', 
                       linewidth=2, label=f'Bearish Threshold ({bearish})')
        
        if 'putcallratio_neutral' in display_df.columns:
            neutral = display_df['putcallratio_neutral'].iloc[0]
            ax2.axhline(y=neutral, color='gray', linestyle='--', 
                       linewidth=1, label=f'Neutral Level ({neutral})')
        
        # Add histogram
        if 'putcallratio_histogram' in display_df.columns:
            # Color histogram bars based on values
            colors = ['green' if val >= 0 else 'red' for val in display_df['putcallratio_histogram']]
            ax2.bar(display_df.index, display_df['putcallratio_histogram'], 
                   color=colors, alpha=0.7, label='Histogram', width=0.8)
    
    elif indicator_name == 'cot':
        if 'cot' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='cot', 
                        ax=ax2, color='darkblue', linewidth=3, label='COT')
        
        if 'cot_signal' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='cot_signal', 
                        ax=ax2, color='darkorange', linewidth=2, label='Signal Line')
        
        # Add threshold levels
        if 'cot_bullish' in display_df.columns:
            bullish = display_df['cot_bullish'].iloc[0]
            ax2.axhline(y=bullish, color='green', linestyle='--', 
                       linewidth=2, label=f'Bullish Threshold ({bullish})')
        
        if 'cot_bearish' in display_df.columns:
            bearish = display_df['cot_bearish'].iloc[0]
            ax2.axhline(y=bearish, color='red', linestyle='--', 
                       linewidth=2, label=f'Bearish Threshold ({bearish})')
        
        if 'cot_neutral' in display_df.columns:
            neutral = display_df['cot_neutral'].iloc[0]
            ax2.axhline(y=neutral, color='gray', linestyle='--', 
                       linewidth=1, label=f'Neutral Level ({neutral})')
        
        # Add histogram
        if 'cot_histogram' in display_df.columns:
            # Color histogram bars based on values
            colors = ['green' if val >= 0 else 'red' for val in display_df['cot_histogram']]
            ax2.bar(display_df.index, display_df['cot_histogram'], 
                   color=colors, alpha=0.7, label='Histogram', width=0.8)
    
    elif indicator_name in ['feargreed', 'fg']:
        if 'feargreed' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='feargreed', 
                        ax=ax2, color='purple', linewidth=3, label='Fear & Greed')
        
        if 'feargreed_signal' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='feargreed_signal', 
                        ax=ax2, color='orange', linewidth=2, label='Signal Line')
        
        # Add threshold levels
        if 'feargreed_fear' in display_df.columns:
            fear = display_df['feargreed_fear'].iloc[0]
            ax2.axhline(y=fear, color='red', linestyle='--', 
                       linewidth=2, label=f'Fear Threshold ({fear})')
        
        if 'feargreed_greed' in display_df.columns:
            greed = display_df['feargreed_greed'].iloc[0]
            ax2.axhline(y=greed, color='green', linestyle='--', 
                       linewidth=2, label=f'Greed Threshold ({greed})')
        
        if 'feargreed_neutral' in display_df.columns:
            neutral = display_df['feargreed_neutral'].iloc[0]
            ax2.axhline(y=neutral, color='gray', linestyle='--', 
                       linewidth=1, label=f'Neutral Level ({neutral})')
        
        # Add histogram
        if 'feargreed_histogram' in display_df.columns:
            # Color histogram bars based on values
            colors = ['green' if val >= 0 else 'red' for val in display_df['feargreed_histogram']]
            ax2.bar(display_df.index, display_df['feargreed_histogram'], 
                   color=colors, alpha=0.7, label='Histogram', width=0.8)
    
    elif indicator_name == 'supertrend':
        # Check for SuperTrend columns
        has_supertrend = 'SuperTrend' in display_df.columns
        has_direction = 'SuperTrend_Direction' in display_df.columns
        has_signal = 'SuperTrend_Signal' in display_df.columns
        
        if has_supertrend:
            # Get SuperTrend values and determine trend direction
            supertrend_values = display_df['SuperTrend']
            
            # Determine trend direction based on price vs SuperTrend
            if 'Close' in display_df.columns:
                price_series = display_df['Close']
            elif 'close' in display_df.columns:
                price_series = display_df['close']
            else:
                price_series = supertrend_values
            
            # Calculate trend direction: 1 for uptrend, -1 for downtrend
            trend = np.where(price_series > supertrend_values, 1, -1)
            trend = pd.Series(trend, index=display_df.index)
            
            # Modern color scheme matching fastest style
            uptrend_color = '#00C851'  # Modern green for uptrend
            downtrend_color = '#FF4444'  # Modern red for downtrend
            signal_change_color = '#FFC107'  # Golden yellow for signal changes
            
            # Detect signal change points
            buy_signals = (trend == 1) & (trend.shift(1) == -1)
            sell_signals = (trend == -1) & (trend.shift(1) == 1)
            signal_changes = buy_signals | sell_signals
            
            # Create color array with signal change highlighting
            color_arr = np.where(trend == 1, uptrend_color, downtrend_color)
            
            # Enhanced segmentation with signal change detection
            segments = []
            last_color = color_arr[0]
            seg_x, seg_y = [display_df.index[0]], [supertrend_values.iloc[0]]
            
            for i in range(1, len(display_df.index)):
                current_color = color_arr[i]
                
                # Check if this is a signal change point
                if signal_changes.iloc[i]:
                    # Add previous segment
                    if len(seg_x) > 1:
                        segments.append((seg_x.copy(), seg_y.copy(), last_color))
                    
                    # Add signal change point with golden color
                    segments.append(([display_df.index[i-1], display_df.index[i]], 
                                  [supertrend_values.iloc[i-1], supertrend_values.iloc[i]], 
                                  signal_change_color))
                    
                    # Start new segment
                    seg_x, seg_y = [display_df.index[i]], [supertrend_values.iloc[i]]
                    last_color = current_color
                elif current_color != last_color:
                    # Regular trend change (not a signal)
                    segments.append((seg_x.copy(), seg_y.copy(), last_color))
                    seg_x, seg_y = [display_df.index[i-1]], [supertrend_values.iloc[i-1]]
                    last_color = current_color
                
                seg_x.append(display_df.index[i])
                seg_y.append(supertrend_values.iloc[i])
            
            # Add final segment
            if len(seg_x) > 0:
                segments.append((seg_x, seg_y, last_color))
            
            # Plot SuperTrend line segments with enhanced styling
            legend_shown = {uptrend_color: False, downtrend_color: False, signal_change_color: False}
            for seg_x, seg_y, seg_color in segments:
                # Determine legend name based on color
                if seg_color == uptrend_color:
                    legend_name = 'SuperTrend (Uptrend)'
                elif seg_color == downtrend_color:
                    legend_name = 'SuperTrend (Downtrend)'
                elif seg_color == signal_change_color:
                    legend_name = 'SuperTrend (Signal Change)'
                else:
                    legend_name = 'SuperTrend'
                
                show_legend = not legend_shown.get(seg_color, False)
                legend_shown[seg_color] = True
                
                # Plot segment with enhanced styling
                linewidth = 4 if seg_color == signal_change_color else 3
                alpha = 0.95 if seg_color == signal_change_color else 0.9
                
                ax2.plot(seg_x, seg_y, color=seg_color, linewidth=linewidth, 
                        alpha=alpha, label=legend_name if show_legend else "")
                
                # Add subtle glow effect for enhanced visual appeal
                if seg_color != signal_change_color:
                    ax2.plot(seg_x, seg_y, color=seg_color, linewidth=linewidth+2, 
                            alpha=0.3, label="")
            
            # Enhanced trend change markers with modern styling
            buy_idx = display_df.index[(trend == 1) & (trend.shift(1) == -1)]
            sell_idx = display_df.index[(trend == -1) & (trend.shift(1) == 1)]
            
            # BUY signals with enhanced styling
            if len(buy_idx) > 0:
                buy_values = supertrend_values.loc[buy_idx]
                ax2.scatter(buy_idx, buy_values, color=uptrend_color, s=100, 
                           marker='^', edgecolors='white', linewidth=2, 
                           alpha=0.95, label='BUY Signal', zorder=5)
                
                # Add pulse effect for buy signals
                ax2.scatter(buy_idx, buy_values, color=uptrend_color, s=150, 
                           marker='o', alpha=0.4, label="", zorder=4)
            
            # SELL signals with enhanced styling
            if len(sell_idx) > 0:
                sell_values = supertrend_values.loc[sell_idx]
                ax2.scatter(sell_idx, sell_values, color=downtrend_color, s=100, 
                           marker='v', edgecolors='white', linewidth=2, 
                           alpha=0.95, label='SELL Signal', zorder=5)
                
                # Add pulse effect for sell signals
                ax2.scatter(sell_idx, sell_values, color=downtrend_color, s=150, 
                           marker='o', alpha=0.4, label="", zorder=4)
            
            # Add trend background zones for better visual context
            trend_changes = display_df.index[trend != trend.shift(1)]
            if len(trend_changes) > 0:
                for i in range(len(trend_changes)):
                    start_idx = trend_changes[i]
                    end_idx = trend_changes[i + 1] if i + 1 < len(trend_changes) else display_df.index[-1]
                    
                    zone_color = (0, 200/255, 81/255, 0.08) if trend.loc[start_idx] == 1 else (255/255, 68/255, 68/255, 0.08)
                    
                    # Create background rectangle
                    rect = Rectangle((start_idx, supertrend_values.min() * 0.995), 
                                   end_idx - start_idx, 
                                   supertrend_values.max() * 1.005 - supertrend_values.min() * 0.995,
                                   facecolor=zone_color, edgecolor='none', alpha=0.3, zorder=1)
                    ax2.add_patch(rect)
        
        # Fallback: use PPrice1/PPrice2 if SuperTrend column not available
        elif 'PPrice1' in display_df.columns and 'PPrice2' in display_df.columns:
            # Create SuperTrend values from PPrice1/PPrice2
            p1 = display_df['PPrice1']
            p2 = display_df['PPrice2']
            direction = display_df.get('Direction', pd.Series(0, index=display_df.index))
            
            # Use PPrice1 as SuperTrend (support level)
            supertrend_values = p1
            
            # Determine trend direction
            if 'Close' in display_df.columns:
                price_series = display_df['Close']
            elif 'close' in display_df.columns:
                price_series = display_df['close']
            else:
                price_series = supertrend_values
            
            trend = np.where(price_series > supertrend_values, 1, -1)
            trend = pd.Series(trend, index=display_df.index)
            
            # Modern color scheme
            uptrend_color = '#00C851'
            downtrend_color = '#FF4444'
            signal_change_color = '#FFC107'
            
            # Detect signal change points
            buy_signals = (trend == 1) & (trend.shift(1) == -1)
            sell_signals = (trend == -1) & (trend.shift(1) == 1)
            signal_changes = buy_signals | sell_signals
            
            # Create color array
            color_arr = np.where(trend == 1, uptrend_color, downtrend_color)
            
            # Enhanced segmentation
            segments = []
            last_color = color_arr[0]
            seg_x, seg_y = [display_df.index[0]], [supertrend_values.iloc[0]]
            
            for i in range(1, len(display_df.index)):
                current_color = color_arr[i]
                
                if signal_changes.iloc[i]:
                    if len(seg_x) > 1:
                        segments.append((seg_x.copy(), seg_y.copy(), last_color))
                    segments.append(([display_df.index[i-1], display_df.index[i]], 
                                  [supertrend_values.iloc[i-1], supertrend_values.iloc[i]], 
                                  signal_change_color))
                    seg_x, seg_y = [display_df.index[i]], [supertrend_values.iloc[i]]
                    last_color = current_color
                elif current_color != last_color:
                    segments.append((seg_x.copy(), seg_y.copy(), last_color))
                    seg_x, seg_y = [display_df.index[i-1]], [supertrend_values.iloc[i-1]]
                    last_color = current_color
                
                seg_x.append(display_df.index[i])
                seg_y.append(supertrend_values.iloc[i])
            
            if len(seg_x) > 0:
                segments.append((seg_x, seg_y, last_color))
            
            # Plot segments with modern styling
            legend_shown = {uptrend_color: False, downtrend_color: False, signal_change_color: False}
            for seg_x, seg_y, seg_color in segments:
                if seg_color == uptrend_color:
                    legend_name = 'SuperTrend (Uptrend)'
                elif seg_color == downtrend_color:
                    legend_name = 'SuperTrend (Downtrend)'
                elif seg_color == signal_change_color:
                    legend_name = 'SuperTrend (Signal Change)'
                else:
                    legend_name = 'SuperTrend'
                
                show_legend = not legend_shown.get(seg_color, False)
                legend_shown[seg_color] = True
                
                linewidth = 4 if seg_color == signal_change_color else 3
                alpha = 0.95 if seg_color == signal_change_color else 0.9
                
                ax2.plot(seg_x, seg_y, color=seg_color, linewidth=linewidth, 
                        alpha=alpha, label=legend_name if show_legend else "")
                
                if seg_color != signal_change_color:
                    ax2.plot(seg_x, seg_y, color=seg_color, linewidth=linewidth+2, 
                            alpha=0.3, label="")
            
            # Enhanced signal markers
            buy_idx = display_df.index[(trend == 1) & (trend.shift(1) == -1)]
            sell_idx = display_df.index[(trend == -1) & (trend.shift(1) == 1)]
            
            if len(buy_idx) > 0:
                buy_values = supertrend_values.loc[buy_idx]
                ax2.scatter(buy_idx, buy_values, color=uptrend_color, s=100, 
                           marker='^', edgecolors='white', linewidth=2, 
                           alpha=0.95, label='BUY Signal', zorder=5)
                ax2.scatter(buy_idx, buy_values, color=uptrend_color, s=150, 
                           marker='o', alpha=0.4, label="", zorder=4)
            
            if len(sell_idx) > 0:
                sell_values = supertrend_values.loc[sell_idx]
                ax2.scatter(sell_idx, sell_values, color=downtrend_color, s=100, 
                           marker='v', edgecolors='white', linewidth=2, 
                           alpha=0.95, label='SELL Signal', zorder=5)
                ax2.scatter(sell_idx, sell_values, color=downtrend_color, s=150, 
                           marker='o', alpha=0.4, label="", zorder=4)
        
        # Simple fallback for basic SuperTrend display
        else:
            # Check if we have PPrice1/PPrice2 or direct supertrend column
            has_pprice = 'PPrice1' in display_df.columns and 'PPrice2' in display_df.columns
            if has_pprice:
                # Use PPrice1 for hover (support level)
                p1 = display_df['PPrice1']
                p2 = display_df['PPrice2']
                direction = display_df.get('Direction', pd.Series(0, index=display_df.index))
                
                # Handle NaN values properly
                valid_mask = ~(pd.isna(p1) | pd.isna(p2))
                supertrend_values = np.full(len(direction), np.nan)
                supertrend_values[valid_mask] = np.where(direction[valid_mask] > 0, p1[valid_mask], p2[valid_mask])
                
                # Determine trend direction
                if 'Close' in display_df.columns:
                    price_series = display_df['Close']
                else:
                    price_series = supertrend_values
                
                trend = np.where(price_series > supertrend_values, 1, -1)
                trend = pd.Series(trend, index=display_df.index)
                
                # Colors for trend
                uptrend_color = '#00C851'  # Green for uptrend
                downtrend_color = '#FF4444'  # Red for downtrend
                
                # Plot SuperTrend line with color based on trend
                for i in range(1, len(display_df.index)):
                    if not pd.isna(supertrend_values[i]) and not pd.isna(supertrend_values[i-1]):
                        color = uptrend_color if trend[i] == 1 else downtrend_color
                        ax2.plot([display_df.index[i-1], display_df.index[i]], 
                                [supertrend_values[i-1], supertrend_values[i]], 
                                color=color, linewidth=3, alpha=0.8)
                
                # Add legend entries
                ax2.plot([], [], color=uptrend_color, linewidth=3, label='SuperTrend (Uptrend)')
                ax2.plot([], [], color=downtrend_color, linewidth=3, label='SuperTrend (Downtrend)')
    
    elif indicator_name == 'wave':
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
                red_mask = wave_data[plot_color_col] == 1  # BUY
                blue_mask = wave_data[plot_color_col] == 2  # SELL
                
                # Create discontinuous line segments for red (BUY = 1)
                if red_mask.any():
                    red_segments = _create_wave_line_segments(
                        wave_data.index, 
                        wave_data[plot_wave_col], 
                        red_mask
                    )
                    # Plot first segment with label, others without
                    for i, (seg_x, seg_y) in enumerate(red_segments):
                        if i == 0:
                            ax2.plot(seg_x, seg_y, color='#FF4444', linewidth=1.5, label='Wave (BUY)', alpha=0.9)
                        else:
                            ax2.plot(seg_x, seg_y, color='#FF4444', linewidth=1.5, alpha=0.9)
                
                # Create discontinuous line segments for blue (SELL = 2)
                if blue_mask.any():
                    blue_segments = _create_wave_line_segments(
                        wave_data.index, 
                        wave_data[plot_wave_col], 
                        blue_mask
                    )
                    # Plot first segment with label, others without
                    for i, (seg_x, seg_y) in enumerate(blue_segments):
                        if i == 0:
                            ax2.plot(seg_x, seg_y, color='#0066CC', linewidth=1.5, label='Wave (SELL)', alpha=0.9)
                        else:
                            ax2.plot(seg_x, seg_y, color='#0066CC', linewidth=1.5, alpha=0.9)
        
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
                ax2.plot(fastline_valid_data.index, fastline_valid_data[plot_fastline_col],
                        color='#FF6B6B', linewidth=0.8, linestyle=':', label='Fast Line', alpha=0.7)
        
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
                ax2.plot(ma_valid_data.index, ma_valid_data[ma_line_col],
                        color='#4ECDC4', linewidth=0.8, label='MA Line', alpha=0.8)
        
        # Add zero line for reference
        ax2.axhline(y=0, color='#95A5A6', linestyle='--', linewidth=0.8, alpha=0.6)
    
    elif indicator_name == 'adx':
        if 'adx' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='adx', 
                        ax=ax2, color='purple', linewidth=3, label='ADX')
        
        if 'di_plus' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='di_plus', 
                        ax=ax2, color='green', linewidth=2, label='DI+')
        
        if 'di_minus' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='di_minus', 
                        ax=ax2, color='red', linewidth=2, label='DI-')
    
    elif indicator_name == 'sar':
        if 'sar' in display_df.columns:
            ax2.scatter(display_df.index, display_df['sar'], 
                       color='red', s=20, label='SAR')
    
    ax2.set_ylabel(indicator_title, fontsize=12)
    ax2.set_xlabel('Date', fontsize=12)
    # Only show legend if there are labeled artists
    if ax2.get_legend_handles_labels()[0]:
        ax2.legend()
    
    # Format x-axis for indicator chart
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # Use the same locator logic as main chart for consistency
    if days_range > 365 * 5:  # More than 5 years
        ax2.xaxis.set_major_locator(mdates.YearLocator(2))  # Every 2 years
    elif days_range > 365 * 2:  # More than 2 years
        ax2.xaxis.set_major_locator(mdates.YearLocator(1))  # Every year
    elif days_range > 365:  # More than 1 year
        ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Every 3 months
    elif days_range > 90:  # More than 3 months
        ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Every month
    else:  # Less than 3 months
        ax2.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days_range // 10)))
    
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save plot
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    logger.print_info(f"Dual chart saved to: {output_path}")
    
    # Show plot
    # Use plt.close() instead of plt.show() to avoid non-interactive warning in test environment
    plt.close()
    
    return fig 