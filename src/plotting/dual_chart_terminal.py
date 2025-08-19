# -*- coding: utf-8 -*-
# src/plotting/dual_chart_terminal.py

"""
Dual chart plotting for terminal mode.
Creates a main OHLC chart with buy/sell signals and support/resistance lines,
plus a secondary chart below showing the selected indicator.
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

from src.common import logger


def plot_dual_chart_terminal(
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
    Create dual chart plot using terminal output for term mode.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data and calculated indicators
        rule (str): Rule string (e.g., 'rsi:14,30,70,open')
        title (str): Plot title
        output_path (str, optional): Output file path
        width (int): Plot width (ignored for terminal)
        height (int): Plot height (ignored for terminal)
        layout (dict, optional): Layout configuration
        **kwargs: Additional arguments
        
    Returns:
        str: Terminal output string
    """
    # Set default output path
    if output_path is None:
        output_path = "results/plots/dual_chart_terminal.txt"
    
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
    
    # Create terminal output
    output_lines = []
    
    # Header
    output_lines.append("=" * 80)
    output_lines.append(f"DUAL CHART - {title.upper()}")
    output_lines.append("=" * 80)
    
    # Main chart data (last 20 rows)
    output_lines.append("\nMAIN CHART (OHLC):")
    output_lines.append("-" * 80)
    
    # Get last 20 rows for display
    last_rows = display_df.tail(20)
    
    # Create table header
    header = f"{'Date':<20} {'Open':<10} {'High':<10} {'Low':<10} {'Close':<10}"
    if 'Volume' in last_rows.columns:
        header += " {'Volume':<10}"
    output_lines.append(header)
    output_lines.append("-" * len(header))
    
    # Add data rows
    for date, row in last_rows.iterrows():
        date_str = date.strftime('%Y-%m-%d %H:%M')
        row_str = f"{date_str:<20} {row['Open']:<10.2f} {row['High']:<10.2f} {row['Low']:<10.2f} {row['Close']:<10.2f}"
        if 'Volume' in row:
            row_str += f" {row['Volume']:<10.0f}"
        output_lines.append(row_str)
    
    # Indicator chart
    indicator_name = rule.split(':', 1)[0].lower().strip() if ':' in rule else rule
    output_lines.append(f"\nINDICATOR CHART ({indicator_name.upper()}):")
    output_lines.append("-" * 80)
    
    # Find indicator columns
    indicator_columns = []
    for col in display_df.columns:
        if col.lower().startswith(indicator_name.lower()) or col.lower() == indicator_name.lower():
            indicator_columns.append(col)
    
    if indicator_columns:
        # Create indicator table header
        indicator_header = f"{'Date':<20}"
        for col in indicator_columns:
            indicator_header += f" {col:<15}"
        output_lines.append(indicator_header)
        output_lines.append("-" * len(indicator_header))
        
        # Add indicator data rows
        for date, row in last_rows.iterrows():
            date_str = date.strftime('%Y-%m-%d %H:%M')
            row_str = f"{date_str:<20}"
            for col in indicator_columns:
                if col in row and pd.notna(row[col]):
                    row_str += f" {row[col]:<15.4f}"
                else:
                    row_str += f" {'N/A':<15}"
            output_lines.append(row_str)
    else:
        output_lines.append("No indicator data found.")
    
    # Summary statistics
    output_lines.append("\nSUMMARY STATISTICS:")
    output_lines.append("-" * 80)
    
    if 'Close' in display_df.columns:
        close_stats = display_df['Close'].describe()
        output_lines.append("Close Price Statistics:")
        output_lines.append(f"  Count: {close_stats['count']:.0f}")
        output_lines.append(f"  Mean: {close_stats['mean']:.4f}")
        output_lines.append(f"  Std: {close_stats['std']:.4f}")
        output_lines.append(f"  Min: {close_stats['min']:.4f}")
        output_lines.append(f"  Max: {close_stats['max']:.4f}")
    
    # Footer
    output_lines.append("\n" + "=" * 80)
    output_lines.append("END OF DUAL CHART")
    output_lines.append("=" * 80)
    
    # Join all lines
    output_text = "\n".join(output_lines)
    
    # Write to file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_text)
        logger.info(f"Terminal chart saved to: {output_path}")
    except Exception as e:
        logger.error(f"Error saving terminal chart: {e}")
    
    return output_text 