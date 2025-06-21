# -*- coding: utf-8 -*-
# src/cli/oscillators/show_rsi_ind.py

"""
RSI (Relative Strength Index) CLI command module.
Handles RSI indicator display with support for parameterized rules and separate subplot display.
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from typing import Optional, Tuple

from ...calculation.indicators.oscillators.rsi_ind_calc import (
    calculate_rsi, calculate_rsi_signals, PriceType
)
from ...common import logger
from ...common.constants import BUY, SELL, NOTRADE


def parse_rsi_rule(rule_str: str) -> Tuple[int, float, float, PriceType]:
    """
    Parse RSI rule string in format 'rsi(period,overbought,oversold,price_type)'.
    
    Args:
        rule_str (str): Rule string like 'rsi(14,70,30,open)'
    
    Returns:
        Tuple: (period, overbought, oversold, price_type)
    """
    try:
        # Remove 'rsi(' and ')' and split by comma
        params = rule_str[4:-1].split(',')
        
        if len(params) != 4:
            raise ValueError("RSI rule must have exactly 4 parameters")
        
        period = int(params[0].strip())
        overbought = float(params[1].strip())
        oversold = float(params[2].strip())
        price_type_str = params[3].strip().lower()
        
        if price_type_str == 'open':
            price_type = PriceType.OPEN
        elif price_type_str == 'close':
            price_type = PriceType.CLOSE
        else:
            raise ValueError("Price type must be 'open' or 'close'")
        
        return period, overbought, oversold, price_type
        
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid RSI rule format: {rule_str}. Expected: rsi(period,overbought,oversold,price_type)") from e


def show_rsi_indicator(df: pd.DataFrame, rule_str: str, 
                      start_date: Optional[str] = None, 
                      end_date: Optional[str] = None,
                      save_plot: bool = False,
                      plot_filename: Optional[str] = None) -> None:
    """
    Display RSI indicator with main price chart and RSI subplot.
    
    Args:
        df (pd.DataFrame): OHLCV data
        rule_str (str): RSI rule string (e.g., 'rsi(14,70,30,open)')
        start_date (str, optional): Start date filter
        end_date (str, optional): End date filter
        save_plot (bool): Whether to save the plot
        plot_filename (str, optional): Filename for saved plot
    """
    # Parse RSI parameters
    period, overbought, oversold, price_type = parse_rsi_rule(rule_str)
    
    # Filter data by date range if specified
    if start_date:
        df = df[df.index >= start_date]
    if end_date:
        df = df[df.index <= end_date]
    
    if df.empty:
        logger.print_warning("No data available for the specified date range")
        return
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate RSI
    rsi_values = calculate_rsi(price_series, period)
    rsi_signals = calculate_rsi_signals(rsi_values, overbought, oversold)
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), height_ratios=[2, 1])
    fig.suptitle(f'RSI Indicator Analysis - {price_name} Price', fontsize=16, fontweight='bold')
    
    # Main price chart
    ax1.plot(df.index, df['Close'], label='Close Price', color='blue', linewidth=1)
    ax1.plot(df.index, df['Open'], label='Open Price', color='orange', linewidth=1, alpha=0.7)
    ax1.fill_between(df.index, df['Low'], df['High'], alpha=0.3, color='gray', label='High-Low Range')
    
    # Add overbought/oversold zones to price chart
    ax1.axhline(y=df['Close'].mean() * 1.02, color='red', linestyle='--', alpha=0.5, label='Overbought Zone')
    ax1.axhline(y=df['Close'].mean() * 0.98, color='green', linestyle='--', alpha=0.5, label='Oversold Zone')
    
    # Add trading signals to price chart
    buy_signals = df.index[rsi_signals == BUY]
    sell_signals = df.index[rsi_signals == SELL]
    
    if len(buy_signals) > 0:
        ax1.scatter(buy_signals, df.loc[buy_signals, 'Close'], 
                   color='green', marker='^', s=100, label='BUY Signal', zorder=5)
    if len(sell_signals) > 0:
        ax1.scatter(sell_signals, df.loc[sell_signals, 'Close'], 
                   color='red', marker='v', s=100, label='SELL Signal', zorder=5)
    
    ax1.set_title(f'Price Chart with RSI Signals (Period: {period}, Overbought: {overbought}, Oversold: {oversold})')
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # RSI subplot
    ax2.plot(df.index, rsi_values, label='RSI', color='purple', linewidth=2)
    ax2.axhline(y=overbought, color='red', linestyle='--', label=f'Overbought ({overbought})')
    ax2.axhline(y=oversold, color='green', linestyle='--', label=f'Oversold ({oversold})')
    ax2.axhline(y=50, color='gray', linestyle='-', alpha=0.5, label='Neutral (50)')
    
    # Fill overbought/oversold zones
    ax2.fill_between(df.index, overbought, 100, alpha=0.3, color='red')
    ax2.fill_between(df.index, 0, oversold, alpha=0.3, color='green')
    
    # Add signal markers to RSI
    if len(buy_signals) > 0:
        ax2.scatter(buy_signals, rsi_values.loc[buy_signals], 
                   color='green', marker='^', s=100, label='BUY Signal', zorder=5)
    if len(sell_signals) > 0:
        ax2.scatter(sell_signals, rsi_values.loc[sell_signals], 
                   color='red', marker='v', s=100, label='SELL Signal', zorder=5)
    
    ax2.set_title(f'RSI Indicator (Period: {period})')
    ax2.set_ylabel('RSI')
    ax2.set_ylim(0, 100)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Format x-axis
    for ax in [ax1, ax2]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(df) // 10)))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    
    # Save plot if requested
    if save_plot:
        if plot_filename is None:
            plot_filename = f"rsi_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        logger.print_info(f"Plot saved as: {plot_filename}")
    
    plt.show()
    
    # Print summary statistics
    print(f"\nRSI Analysis Summary:")
    print(f"Period: {period}")
    print(f"Overbought Level: {overbought}")
    print(f"Oversold Level: {oversold}")
    print(f"Price Type: {price_name}")
    print(f"Data Points: {len(df)}")
    print(f"BUY Signals: {len(buy_signals)}")
    print(f"SELL Signals: {len(sell_signals)}")
    print(f"RSI Range: {rsi_values.min():.2f} - {rsi_values.max():.2f}")
    print(f"Current RSI: {rsi_values.iloc[-1]:.2f}")


def main():
    """Main CLI function for RSI indicator."""
    parser = argparse.ArgumentParser(description='RSI (Relative Strength Index) Indicator')
    parser.add_argument('--rule', type=str, required=True,
                       help='RSI rule in format: rsi(period,overbought,oversold,price_type)')
    parser.add_argument('--start', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('--save', action='store_true', help='Save plot to file')
    parser.add_argument('--filename', type=str, help='Output filename for plot')
    
    args = parser.parse_args()
    
    # This would typically be called from the main CLI with data already loaded
    # For now, we'll just validate the rule format
    try:
        period, overbought, oversold, price_type = parse_rsi_rule(args.rule)
        print(f"RSI Rule parsed successfully:")
        print(f"  Period: {period}")
        print(f"  Overbought: {overbought}")
        print(f"  Oversold: {oversold}")
        print(f"  Price Type: {price_type.value}")
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 