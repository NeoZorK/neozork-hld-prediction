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

from ..common import logger


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
    
    # Set seaborn style
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    
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
    
    # Plot candlesticks
    for i, (date, row) in enumerate(display_df.iterrows()):
        # Determine color based on open/close
        if row['Close'] >= row['Open']:
            color = 'green'
            body_color = 'lightgreen'
        else:
            color = 'red'
            body_color = 'lightcoral'
        
        # Plot high-low line
        ax1.plot([date, date], [row['Low'], row['High']], color=color, linewidth=1)
        
        # Plot open-close body
        body_height = abs(row['Close'] - row['Open'])
        body_bottom = min(row['Open'], row['Close'])
        
        rect = Rectangle((date - pd.Timedelta(hours=6), body_bottom), 
                        pd.Timedelta(hours=12), body_height,
                        facecolor=body_color, edgecolor=color, linewidth=1)
        ax1.add_patch(rect)
    
    # Add support and resistance lines if available
    if 'Support' in display_df.columns:
        sns.lineplot(data=display_df, x=display_df.index, y='Support', 
                    ax=ax1, color='blue', linestyle='--', linewidth=2, alpha=0.8, label='Support')
    
    if 'Resistance' in display_df.columns:
        sns.lineplot(data=display_df, x=display_df.index, y='Resistance', 
                    ax=ax1, color='red', linestyle='--', linewidth=2, alpha=0.8, label='Resistance')
    
    # Add buy/sell signals if available
    if 'Direction' in display_df.columns:
        buy_signals = display_df[display_df['Direction'] == 1]
        sell_signals = display_df[display_df['Direction'] == 2]
        
        if not buy_signals.empty:
            ax1.scatter(buy_signals.index, buy_signals['Low'] * 0.995, 
                       color='green', marker='^', s=100, label='Buy Signal', zorder=5)
        
        if not sell_signals.empty:
            ax1.scatter(sell_signals.index, sell_signals['High'] * 1.005, 
                       color='red', marker='v', s=100, label='Sell Signal', zorder=5)
    
    ax1.set_ylabel('Price', fontsize=12)
    ax1.legend()
    
    # Format x-axis for main chart
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # Indicator chart
    indicator_name = rule.split(':', 1)[0].lower().strip()
    indicator_title = layout['indicator_name'] if layout else 'Indicator'
    ax2.set_title(indicator_title, fontsize=12, fontweight='bold')
    
    # Add indicator based on type
    if indicator_name == 'rsi':
        if 'rsi' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='rsi', 
                        ax=ax2, color='purple', linewidth=3, label='RSI')
            
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
                        ax=ax2, color='blue', linewidth=3, label='MACD')
        
        if 'macd_signal' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='macd_signal', 
                        ax=ax2, color='red', linewidth=2, label='Signal')
        
        if 'macd_histogram' in display_df.columns:
            # Color histogram bars
            colors = ['green' if val >= 0 else 'red' for val in display_df['macd_histogram']]
            ax2.bar(display_df.index, display_df['macd_histogram'], 
                   color=colors, alpha=0.7, label='Histogram', width=0.8)
    
    elif indicator_name == 'ema':
        if 'ema' in display_df.columns:
            sns.lineplot(data=display_df, x=display_df.index, y='ema', 
                        ax=ax2, color='orange', linewidth=3, label='EMA')
    
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
    ax2.legend()
    
    # Format x-axis for indicator chart
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save plot
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    logger.print_info(f"Dual chart saved to: {output_path}")
    
    return fig 