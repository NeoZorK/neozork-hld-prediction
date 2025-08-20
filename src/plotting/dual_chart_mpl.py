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
    ax1.set_title(title, fontsize=13, fontweight='bold', pad=20)
    
    # Enhanced grid for main chart
    ax1.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)
    ax1.set_axisbelow(True)  # Put grid behind data
    
    # Plot candlesticks
    for i, (date, row) in enumerate(display_df.iterrows()):
        # Determine color based on open/close
        if row['Close'] >= row['Open']:
            color = '#2ECC71'  # Modern green
            body_color = '#A8E6CF'  # Light green
        else:
            color = '#E74C3C'  # Modern red
            body_color = '#FADBD8'  # Light red
        
        # Plot high-low line
        ax1.plot([date, date], [row['Low'], row['High']], color=color, linewidth=0.8, alpha=0.8)
        
        # Plot open-close body
        body_height = abs(row['Close'] - row['Open'])
        body_bottom = min(row['Open'], row['Close'])
        
        rect = Rectangle((date - pd.Timedelta(hours=6), body_bottom), 
                        pd.Timedelta(hours=12), body_height,
                        facecolor=body_color, edgecolor=color, linewidth=0.8, alpha=0.9)
        ax1.add_patch(rect)
    
    # Add support and resistance lines if available
    if 'Support' in display_df.columns:
        ax1.plot(display_df.index, display_df['Support'], 
                color='#3498DB', linestyle='--', linewidth=1.5, alpha=0.8, label='Support')
    
    if 'Resistance' in display_df.columns:
        ax1.plot(display_df.index, display_df['Resistance'], 
                color='#E67E22', linestyle='--', linewidth=1.5, alpha=0.8, label='Resistance')
    
    # Add buy/sell signals if available
    if 'Direction' in display_df.columns:
        buy_signals = display_df[display_df['Direction'] == 1]
        sell_signals = display_df[display_df['Direction'] == 2]
        
        if not buy_signals.empty:
            ax1.scatter(buy_signals.index, buy_signals['Low'] * 0.995, 
                       color='#2ECC71', marker='^', s=80, label='Buy Signal', zorder=5, alpha=0.9)
        
        if not sell_signals.empty:
            ax1.scatter(sell_signals.index, sell_signals['High'] * 1.005, 
                       color='#E74C3C', marker='v', s=80, label='Sell Signal', zorder=5, alpha=0.9)
    
    ax1.set_ylabel('Price', fontsize=11, fontweight='bold')
    
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
    
    elif indicator_name == 'sma':
        y_axis_label = 'Price'
        if 'sma' in display_df.columns:
            ax2.plot(display_df.index, display_df['sma'], 
                    color='blue', linewidth=3, label='SMA')
    
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
    
    elif indicator_name == 'supertrend':
        y_axis_label = 'Price'
        
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
    
    elif indicator_name == 'wave':
        y_axis_label = 'Wave Value'
        
        # Add Wave signals to the main chart (ax1)
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

    # Add legend to main chart after all signals are added
    ax1.legend(loc='upper right', framealpha=0.9, fancybox=True, shadow=True, fontsize=9)
    
    # Set y-axis label
    ax2.set_ylabel(y_axis_label, fontsize=11, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=11, fontweight='bold')
    
    # Enhanced grid styling
    ax2.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)
    ax2.set_axisbelow(True)  # Put grid behind data
    
    # Enhanced legend
    ax2.legend(loc='upper right', framealpha=0.9, fancybox=True, shadow=True, fontsize=9)
    
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
    from src.plotting.dual_chart_plot import calculate_additional_indicator
    df_with_indicator = calculate_additional_indicator(df, rule)
    
    return plot_dual_chart_mpl(df_with_indicator, rule, title, None, width, height, layout, **kwargs) 