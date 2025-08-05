# -*- coding: utf-8 -*-
# src/plotting/dual_chart_mpl.py

"""
Dual chart plotting for mpl mode using matplotlib.
Creates a main OHLC chart with buy/sell signals and support/resistance lines,
plus a secondary chart below showing the selected indicator.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from typing import Dict, Any, Optional

from ..common import logger


def plot_dual_chart_mpl(
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
    Create dual chart plot using matplotlib for mpl mode.
    
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
    # Set default output path only if not None
    if output_path is None:
        # This will be handled in the display logic at the end
        pass
    else:
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
        ax1.plot(display_df.index, display_df['Support'], 
                color='blue', linestyle='--', linewidth=2, alpha=0.8, label='Support')
    
    if 'Resistance' in display_df.columns:
        ax1.plot(display_df.index, display_df['Resistance'], 
                color='red', linestyle='--', linewidth=2, alpha=0.8, label='Resistance')
    
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
    ax1.grid(True, alpha=0.3)
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
    
    # Set y-axis label based on indicator type
    y_axis_label = 'Value'  # Default label
    
    # Add indicator based on type
    if indicator_name == 'rsi':
        y_axis_label = 'RSI Value'
        if 'rsi' in display_df.columns:
            ax2.plot(display_df.index, display_df['rsi'], 
                    color='purple', linewidth=3, label='RSI')
            
            # Add overbought/oversold lines
            if 'rsi_overbought' in display_df.columns:
                overbought = display_df['rsi_overbought'].iloc[0]
                ax2.axhline(y=overbought, color='red', linestyle='--', 
                           linewidth=2, label=f'Overbought ({overbought})')
            
            if 'rsi_oversold' in display_df.columns:
                oversold = display_df['rsi_oversold'].iloc[0]
                ax2.axhline(y=oversold, color='green', linestyle='--', 
                           linewidth=2, label=f'Oversold ({oversold})')
    
    elif indicator_name == 'rsi_mom':
        y_axis_label = 'RSI Momentum'
        if 'rsi' in display_df.columns:
            ax2.plot(display_df.index, display_df['rsi'], 
                    color='purple', linewidth=2, label='RSI')
        
        if 'rsi_momentum' in display_df.columns:
            ax2.plot(display_df.index, display_df['rsi_momentum'], 
                    color='orange', linewidth=2, label='RSI Momentum')
            
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
        y_axis_label = 'RSI Divergence'
        if 'rsi' in display_df.columns:
            ax2.plot(display_df.index, display_df['rsi'], 
                    color='purple', linewidth=2, label='RSI')
        
        if 'rsi_divergence' in display_df.columns:
            ax2.plot(display_df.index, display_df['rsi_divergence'], 
                    color='orange', linewidth=2, label='RSI Divergence')
            
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
    
    elif indicator_name == 'stoch':
        y_axis_label = 'Stochastic %'
        # Plot %K line
        if 'stoch_k' in display_df.columns:
            ax2.plot(display_df.index, display_df['stoch_k'], 
                    color='blue', linewidth=3, label='%K')
        
        # Plot %D line
        if 'stoch_d' in display_df.columns:
            ax2.plot(display_df.index, display_df['stoch_d'], 
                    color='orange', linewidth=3, label='%D')
        
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
        y_axis_label = 'Stochastic Oscillator %'
        # Plot %K line
        if 'stochosc_k' in display_df.columns:
            ax2.plot(display_df.index, display_df['stochosc_k'], 
                    color='blue', linewidth=3, label='%K')
        
        # Plot %D line
        if 'stochosc_d' in display_df.columns:
            ax2.plot(display_df.index, display_df['stochosc_d'], 
                    color='orange', linewidth=3, label='%D')
        
        # Add overbought/oversold lines
        if 'stochosc_overbought' in display_df.columns:
            overbought = display_df['stochosc_overbought'].iloc[0]
            ax2.axhline(y=overbought, color='red', linestyle='--', 
                       linewidth=2, label=f'Overbought ({overbought})')
        
        if 'stochosc_oversold' in display_df.columns:
            oversold = display_df['stochosc_oversold'].iloc[0]
            ax2.axhline(y=oversold, color='green', linestyle='--', 
                       linewidth=2, label=f'Oversold ({oversold})')
    
    elif indicator_name == 'macd':
        y_axis_label = 'MACD Value'
        if 'macd' in display_df.columns:
            ax2.plot(display_df.index, display_df['macd'], 
                    color='blue', linewidth=3, label='MACD')
        
        if 'macd_signal' in display_df.columns:
            ax2.plot(display_df.index, display_df['macd_signal'], 
                    color='red', linewidth=2, label='Signal')
        
        if 'macd_histogram' in display_df.columns:
            # Color histogram bars
            colors = ['green' if val >= 0 else 'red' for val in display_df['macd_histogram']]
            ax2.bar(display_df.index, display_df['macd_histogram'], 
                   color=colors, alpha=0.7, label='Histogram', width=0.8)
        
        # Add zero line for MACD
        ax2.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    elif indicator_name == 'ema':
        y_axis_label = 'Price'
        if 'ema' in display_df.columns:
            ax2.plot(display_df.index, display_df['ema'], 
                    color='orange', linewidth=3, label='EMA')
    
    elif indicator_name == 'bb':
        y_axis_label = 'Price'
        if 'bb_upper' in display_df.columns:
            ax2.plot(display_df.index, display_df['bb_upper'], 
                    color='blue', linewidth=2, label='Upper Band')
        
        if 'bb_middle' in display_df.columns:
            ax2.plot(display_df.index, display_df['bb_middle'], 
                    color='gray', linewidth=2, label='Middle Band')
        
        if 'bb_lower' in display_df.columns:
            ax2.plot(display_df.index, display_df['bb_lower'], 
                    color='red', linewidth=2, label='Lower Band')
    
    elif indicator_name == 'atr':
        y_axis_label = 'ATR Value'
        if 'atr' in display_df.columns:
            ax2.plot(display_df.index, display_df['atr'], 
                    color='orange', linewidth=3, label='ATR')
    
    elif indicator_name == 'cci':
        y_axis_label = 'CCI Value'
        if 'cci' in display_df.columns:
            ax2.plot(display_df.index, display_df['cci'], 
                    color='purple', linewidth=3, label='CCI')
        
        # Add overbought/oversold lines
        if 'cci_overbought' in display_df.columns:
            overbought = display_df['cci_overbought'].iloc[0]
            ax2.axhline(y=overbought, color='red', linestyle='--', 
                       linewidth=2, label=f'Overbought ({overbought})')
        
        if 'cci_oversold' in display_df.columns:
            oversold = display_df['cci_oversold'].iloc[0]
            ax2.axhline(y=oversold, color='green', linestyle='--', 
                       linewidth=2, label=f'Oversold ({oversold})')
    
    elif indicator_name == 'vwap':
        y_axis_label = 'Price'
        if 'vwap' in display_df.columns:
            ax2.plot(display_df.index, display_df['vwap'], 
                    color='blue', linewidth=3, label='VWAP')
    
    elif indicator_name == 'pivot':
        y_axis_label = 'Price'
        if 'pivot' in display_df.columns:
            ax2.plot(display_df.index, display_df['pivot'], 
                    color='blue', linewidth=2, label='Pivot')
        
        if 'r1' in display_df.columns:
            ax2.plot(display_df.index, display_df['r1'], 
                    color='red', linewidth=2, linestyle='--', label='R1')
        
        if 's1' in display_df.columns:
            ax2.plot(display_df.index, display_df['s1'], 
                    color='green', linewidth=2, linestyle='--', label='S1')
    
    elif indicator_name == 'hma':
        y_axis_label = 'Price'
        if 'hma' in display_df.columns:
            ax2.plot(display_df.index, display_df['hma'], 
                    color='orange', linewidth=3, label='HMA')
    
    elif indicator_name == 'tsf':
        y_axis_label = 'Price'
        if 'tsf' in display_df.columns:
            ax2.plot(display_df.index, display_df['tsf'], 
                    color='blue', linewidth=3, label='TSF')
    
    elif indicator_name == 'monte':
        y_axis_label = 'Price'
        # Add Monte Carlo forecast line (main line)
        if 'montecarlo' in display_df.columns:
            ax2.plot(display_df.index, display_df['montecarlo'], 
                    color='blue', linewidth=3, label='Monte Carlo Forecast')
        
        # Add Monte Carlo signal line
        if 'montecarlo_signal' in display_df.columns:
            ax2.plot(display_df.index, display_df['montecarlo_signal'], 
                    color='red', linewidth=2, label='Signal Line')
        
        # Add Monte Carlo histogram
        if 'montecarlo_histogram' in display_df.columns:
            # Color histogram bars based on values
            colors = ['green' if val >= 0 else 'red' for val in display_df['montecarlo_histogram']]
            ax2.bar(display_df.index, display_df['montecarlo_histogram'], 
                   color=colors, alpha=0.7, label='Histogram', width=0.8)
        
        # Add confidence bands
        if 'montecarlo_upper' in display_df.columns:
            ax2.plot(display_df.index, display_df['montecarlo_upper'], 
                    color='lightblue', linewidth=1, linestyle='--', label='Upper Confidence')
        
        if 'montecarlo_lower' in display_df.columns:
            ax2.plot(display_df.index, display_df['montecarlo_lower'], 
                    color='lightblue', linewidth=1, linestyle='--', label='Lower Confidence')
        
        # Add zero line for histogram
        ax2.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    elif indicator_name == 'kelly':
        y_axis_label = 'Kelly %'
        if 'kelly' in display_df.columns:
            ax2.plot(display_df.index, display_df['kelly'], 
                    color='purple', linewidth=3, label='Kelly')
    
    elif indicator_name == 'putcallratio':
        y_axis_label = 'Put/Call Ratio'
        if 'putcallratio' in display_df.columns:
            ax2.plot(display_df.index, display_df['putcallratio'], 
                    color='brown', linewidth=3, label='Put/Call Ratio')
    
    elif indicator_name == 'cot':
        y_axis_label = 'COT Value'
        if 'cot' in display_df.columns:
            ax2.plot(display_df.index, display_df['cot'], 
                    color='blue', linewidth=3, label='COT')
    
    elif indicator_name in ['feargreed', 'fg']:
        y_axis_label = 'Fear & Greed Index'
        if 'feargreed' in display_df.columns:
            ax2.plot(display_df.index, display_df['feargreed'], 
                    color='purple', linewidth=3, label='Fear & Greed')
    
    elif indicator_name == 'donchain':
        y_axis_label = 'Price'
        if 'donchain_upper' in display_df.columns:
            ax2.plot(display_df.index, display_df['donchain_upper'], 
                    color='green', linewidth=2, label='Upper Channel')
        
        if 'donchain_middle' in display_df.columns:
            ax2.plot(display_df.index, display_df['donchain_middle'], 
                    color='gray', linewidth=2, label='Middle Channel')
        
        if 'donchain_lower' in display_df.columns:
            ax2.plot(display_df.index, display_df['donchain_lower'], 
                    color='blue', linewidth=2, label='Lower Channel')
    
    elif indicator_name == 'fibo':
        y_axis_label = 'Price'
        # Add Fibonacci levels
        fibo_cols = [col for col in display_df.columns if col.startswith('fibo_')]
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
        
        for i, col in enumerate(fibo_cols):
            color = colors[i % len(colors)]
            ax2.plot(display_df.index, display_df[col], 
                    color=color, linewidth=2, label=col.replace('fibo_', 'Fib '))
    
    elif indicator_name == 'obv':
        y_axis_label = 'OBV Value'
        if 'obv' in display_df.columns:
            ax2.plot(display_df.index, display_df['obv'], 
                    color='brown', linewidth=3, label='OBV')
    
    elif indicator_name == 'stdev':
        y_axis_label = 'Standard Deviation'
        if 'stdev' in display_df.columns:
            ax2.plot(display_df.index, display_df['stdev'], 
                    color='gray', linewidth=3, label='StdDev')
    
    elif indicator_name == 'adx':
        y_axis_label = 'ADX Value'
        if 'adx' in display_df.columns:
            ax2.plot(display_df.index, display_df['adx'], 
                    color='purple', linewidth=3, label='ADX')
        
        if 'di_plus' in display_df.columns:
            ax2.plot(display_df.index, display_df['di_plus'], 
                    color='green', linewidth=2, label='DI+')
        
        if 'di_minus' in display_df.columns:
            ax2.plot(display_df.index, display_df['di_minus'], 
                    color='red', linewidth=2, label='DI-')
    
    elif indicator_name == 'sar':
        y_axis_label = 'Price'
        if 'sar' in display_df.columns:
            ax2.scatter(display_df.index, display_df['sar'], 
                       color='red', s=20, label='SAR')
    
    # Set y-axis label
    ax2.set_ylabel(y_axis_label, fontsize=12)
    ax2.set_xlabel('Date', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Format x-axis for indicator chart
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # Use the same locator as main chart for consistency
    ax2.xaxis.set_major_locator(ax1.xaxis.get_major_locator())
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Adjust layout
    plt.tight_layout()
    
    # Display plot if output_path is None, otherwise save
    if output_path is None:
        plt.show()
        logger.print_info("Dual chart displayed.")
    else:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.print_info(f"Dual chart saved to: {output_path}")
    
    return fig


def plot_dual_chart_mpl_display(
    df: pd.DataFrame,
    rule: str,
    title: str = '',
    width: int = 1800,
    height: int = 1100,
    layout: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Any:
    """
    Create and display dual chart for mpl mode without saving to file.
    
    Args:
        df (pd.DataFrame): OHLCV data with indicators
        rule (str): Rule string (e.g., 'macd:12,26,9,close')
        title (str): Plot title
        width (int): Plot width
        height (int): Plot height
        layout (dict, optional): Layout configuration
        **kwargs: Additional arguments
        
    Returns:
        Any: Plot object
    """
    # Calculate additional indicator first
    from ..plotting.dual_chart_plot import calculate_additional_indicator
    df_with_indicator = calculate_additional_indicator(df, rule)
    
    return plot_dual_chart_mpl(df_with_indicator, rule, title, None, width, height, layout, **kwargs) 