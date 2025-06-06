# -*- coding: utf-8 -*-
# src/plotting/term_separate_plots.py

"""
Terminal-based separate field plotting using plotext.
Creates individual charts for each field instead of combined plots.
"""

import pandas as pd
import numpy as np
import plotext as plt
from typing import Optional, Union, List

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    # Fallback to relative imports when run as module
    from ..common import logger
    from ..common.constants import TradingRule, BUY, SELL, NOTRADE


def plot_separate_fields_terminal(df: pd.DataFrame, 
                                 rule: Union[TradingRule, str], 
                                 title: str = "Separate Field Plots",
                                 fields: Optional[List[str]] = None) -> None:
    """
    Create separate terminal plots for individual fields.
    
    Args:
        df (pd.DataFrame): DataFrame with calculation results
        rule (TradingRule | str): Trading rule
        title (str): Base title for plots
        fields (List[str], optional): Specific fields to plot. If None, plots all numeric fields.
    """
    try:
        logger.print_info("Generating separate field terminal plots...")
        
        # Validate input data
        if df is None or df.empty:
            logger.print_error("DataFrame is None or empty, cannot plot")
            return
        
        # Convert rule to string
        rule_str = rule.name if hasattr(rule, 'name') else str(rule)
        
        # Determine fields to plot
        if fields is None:
            # Skip basic OHLC and common non-indicator columns
            skip_columns = {'Open', 'High', 'Low', 'Close', 'DateTime', 'Timestamp', 'Date', 'Time', 'index'}
            
            # Get all numeric columns that are not basic OHLC
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            fields = [col for col in numeric_columns if col not in skip_columns]
        
        if not fields:
            logger.print_warning("No fields found to plot")
            return
            
        logger.print_info(f"Plotting {len(fields)} separate fields: {fields}")
        
        # Create time axis
        x_values = list(range(len(df)))
        
        # Plot each field individually
        for field in fields:
            if field not in df.columns:
                logger.print_warning(f"Field '{field}' not found in DataFrame")
                continue
                
            # Create individual plot for this field
            _plot_individual_field(df, field, x_values, f"{title} - {field}", rule_str)
        
        logger.print_success(f"Successfully generated {len(fields)} separate field plots!")
        
    except Exception as e:
        logger.print_error(f"Error generating separate field plots: {e}")


def plot_specific_fields_terminal(df: pd.DataFrame, 
                                 fields: List[str],
                                 rule: Union[TradingRule, str],
                                 title: str = "Specific Field Plots") -> None:
    """
    Plot only specific fields as requested.
    
    Args:
        df (pd.DataFrame): DataFrame with calculation results
        fields (List[str]): Specific fields to plot
        rule (TradingRule | str): Trading rule
        title (str): Base title for plots
    """
    try:
        logger.print_info(f"Plotting specific fields: {fields}")
        
        # Validate input data
        if df is None or df.empty:
            logger.print_error("DataFrame is None or empty, cannot plot")
            return
        
        if not fields:
            logger.print_warning("No fields specified to plot")
            return
        
        # Map common field names to actual column names
        field_mapping = {
            'predicted_high': ['PPrice2', 'predicted_high', 'pred_high'],
            'predicted_low': ['PPrice1', 'predicted_low', 'pred_low'], 
            'pressure_vector': ['PV', 'pressure_vector', 'pv'],
            'pressure': ['Pressure', 'pressure'],
            'high': ['High', 'high'],
            'low': ['Low', 'low'],
            'volume': ['Volume', 'volume', 'TickVolume']
        }
        
        # Find actual column names for requested fields
        actual_fields = []
        for field in fields:
            field_lower = field.lower()
            found = False
            
            # Direct match first
            if field in df.columns:
                actual_fields.append(field)
                found = True
            else:
                # Try mapped names
                for mapped_name, possible_names in field_mapping.items():
                    if field_lower == mapped_name or field in possible_names:
                        for possible_name in possible_names:
                            if possible_name in df.columns:
                                actual_fields.append(possible_name)
                                found = True
                                break
                        if found:
                            break
            
            if not found:
                logger.print_warning(f"Field '{field}' not found in DataFrame")
        
        logger.print_info(f"Found actual fields: {actual_fields}")
        
        # Plot each field separately
        plot_separate_fields_terminal(df, rule, title, actual_fields)
        
    except Exception as e:
        logger.print_error(f"Error plotting specific fields: {e}")


def _plot_individual_field(df: pd.DataFrame, field: str, x_values: list, title: str, rule_str: str) -> None:
    """Plot a single field in its own chart."""
    try:
        # Clear any previous plots
        plt.clear_data()
        plt.clear_figure()
        
        # Set up plot theme and size
        plt.plot_size(120, 30)
        plt.theme('matrix')  # Unified matrix theme
        
        # Get field data
        field_data = df[field].fillna(0).tolist()
        
        # Determine plot type based on field characteristics
        if 'volume' in field.lower():
            _plot_volume_field(x_values, field_data, title, field)
        elif any(signal in field.lower() for signal in ['signal', 'direction', 'buy', 'sell']):
            _plot_signal_field(x_values, field_data, title, field)
        elif any(pred in field.lower() for pred in ['predicted', 'pprice', 'forecast']):
            _plot_prediction_field(x_values, field_data, title, field)
        elif field.lower() in ['high', 'low', 'open', 'close']:
            _plot_price_field(x_values, field_data, title, field)
        else:
            _plot_indicator_field(x_values, field_data, title, field)
        
        # Show the plot
        plt.show()
        
        # Show individual field statistics
        _show_field_statistics(df[field], field, rule_str)
        
    except Exception as e:
        logger.print_error(f"Error plotting field '{field}': {e}")


def _plot_volume_field(x_values: list, field_data: list, title: str, field: str) -> None:
    """Plot volume data as bars."""
    plt.bar(x_values, field_data, color="cyan+", label=field)
    plt.title(f"{title} - Volume")
    plt.xlabel("Time / Bar Index")
    plt.ylabel("Volume")


def _plot_signal_field(x_values: list, field_data: list, title: str, field: str) -> None:
    """Plot trading signals as scatter points."""
    # Convert signals to display positions
    buy_positions = [x for x, val in zip(x_values, field_data) if val == 1 or val == BUY]
    sell_positions = [x for x, val in zip(x_values, field_data) if val == -1 or val == SELL]
    
    if buy_positions:
        plt.scatter(buy_positions, [1] * len(buy_positions), color="green+", label="BUY", marker="^")
    if sell_positions:
        plt.scatter(sell_positions, [-1] * len(sell_positions), color="red+", label="SELL", marker="v")
    
    plt.title(f"{title} - Trading Signals")
    plt.xlabel("Time / Bar Index")
    plt.ylabel("Signal")


def _plot_prediction_field(x_values: list, field_data: list, title: str, field: str) -> None:
    """Plot prediction data as lines with special markers."""
    plt.plot(x_values, field_data, color="yellow+", label=field, marker="D")
    plt.title(f"{title} - Predictions")
    plt.xlabel("Time / Bar Index")
    plt.ylabel("Predicted Price")


def _plot_price_field(x_values: list, field_data: list, title: str, field: str) -> None:
    """Plot price data as lines."""
    color_map = {
        'high': "green+",
        'low': "red+", 
        'open': "blue+",
        'close': "white+"
    }
    color = color_map.get(field.lower(), "white+")
    
    plt.plot(x_values, field_data, color=color, label=field, marker="o")
    plt.title(f"{title} - Price Data")
    plt.xlabel("Time / Bar Index")
    plt.ylabel("Price")


def _plot_indicator_field(x_values: list, field_data: list, title: str, field: str) -> None:
    """Plot general indicator data."""
    color = "magenta+" if 'pressure' in field.lower() else "cyan+"
    marker = "+" if 'pressure' in field.lower() else "."
    
    plt.plot(x_values, field_data, color=color, label=field, marker=marker)
    plt.title(f"{title} - Indicator")
    plt.xlabel("Time / Bar Index")  
    plt.ylabel("Value")


def _show_field_statistics(field_series: pd.Series, field_name: str, rule_str: str) -> None:
    """Show statistics for individual field."""
    try:
        # Clean data
        clean_data = field_series.dropna()
        if len(clean_data) == 0:
            logger.print_warning(f"No valid data for field '{field_name}'")
            return
        
        print(f"\n{'='*60}")
        print(f"FIELD STATISTICS: {field_name}")
        print(f"Rule: {rule_str}")
        print(f"{'='*60}")
        
        # Basic statistics
        print(f"Data Points:    {len(clean_data)}")
        print(f"Min Value:      {clean_data.min():.5f}")
        print(f"Max Value:      {clean_data.max():.5f}")
        print(f"Mean Value:     {clean_data.mean():.5f}")
        print(f"Std Dev:        {clean_data.std():.5f}")
        
        # Field-specific statistics
        if 'volume' in field_name.lower():
            print(f"Total Volume:   {clean_data.sum():.0f}")
            print(f"Avg Volume:     {clean_data.mean():.0f}")
        elif any(signal in field_name.lower() for signal in ['signal', 'direction']):
            buy_count = (clean_data == 1).sum()
            sell_count = (clean_data == -1).sum()
            no_trade = (clean_data == 0).sum()
            print(f"BUY Signals:    {buy_count}")
            print(f"SELL Signals:   {sell_count}")
            print(f"NO TRADE:       {no_trade}")
            signal_rate = ((buy_count + sell_count) / len(clean_data)) * 100 if len(clean_data) > 0 else 0
            print(f"Signal Rate:    {signal_rate:.1f}%")
        
        print(f"{'='*60}\n")
        
    except Exception as e:
        logger.print_error(f"Error showing statistics for field '{field_name}': {e}")
