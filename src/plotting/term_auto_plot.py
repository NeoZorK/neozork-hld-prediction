# -*- coding: utf-8 -*-
# src/plotting/term_auto_plot.py

"""
Terminal-based auto plotting using plotext for displaying all DataFrame columns.
"""

import pandas as pd
import numpy as np
import plotext as plt
from typing import Optional

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
except ImportError:
    # Fallback to relative imports when run as module
    from ..common import logger


def auto_plot_from_dataframe(df: pd.DataFrame, title: str = "Auto Terminal Plot") -> None:
    """
    Automatically plot all numeric columns from a DataFrame in terminal.
    Each column gets its own color and is displayed on the same chart.
    
    Args:
        df (pd.DataFrame): DataFrame with data to plot
        title (str): Title for the plot
    """
    try:
        logger.print_info("Generating auto terminal plot for all DataFrame columns...")
        
        # Clear any previous plots
        plt.clear_data()
        plt.clear_figure()
        
        # Validate input data
        if df is None or df.empty:
            logger.print_error("DataFrame is None or empty, cannot plot")
            return
        
        # Set terminal size and theme
        plt.theme('dark')
        plt.plot_size(120, 35)  # Larger height for better readability with multiple series
        
        # Create time axis
        x_values = list(range(len(df)))
        
        # Define colors for different indicators - expanded color palette
        colors = [
            "red", "green", "blue", "yellow", "magenta", "cyan", "white",
            "red+", "green+", "blue+", "yellow+", "magenta+", "cyan+",
            "brown", "orange", "gray", "black"
        ]
        
        # Standard columns to skip or handle specially
        ohlc_columns = ['Open', 'High', 'Low', 'Close']
        special_columns = ['Volume', 'DateTime', 'Timestamp', 'Date', 'Time', 'index']
        
        color_index = 0
        plotted_columns = []
        
        # First, plot OHLC data if available
        if all(col in df.columns for col in ohlc_columns):
            logger.print_info("Plotting OHLC data...")
            
            # Plot OHLC as connected lines with different markers
            open_values = df['Open'].fillna(method='ffill').fillna(0).tolist()
            high_values = df['High'].fillna(method='ffill').fillna(0).tolist()
            low_values = df['Low'].fillna(method='ffill').fillna(0).tolist()
            close_values = df['Close'].fillna(method='ffill').fillna(0).tolist()
            
            plt.plot(x_values, open_values, color="green", label="Open", marker="o")
            plt.plot(x_values, high_values, color="cyan", label="High", marker="^")
            plt.plot(x_values, low_values, color="cyan", label="Low", marker="v")
            plt.plot(x_values, close_values, color="red", label="Close", marker="s")
            
            plotted_columns.extend(ohlc_columns)
            color_index = 4  # Start from color index 4 after OHLC
        
        # Plot Volume with special handling (normalized)
        if 'Volume' in df.columns and 'Volume' not in plotted_columns:
            logger.print_info("Adding Volume data (normalized)...")
            volume_values = df['Volume'].fillna(0).tolist()
            
            if max(volume_values) > 0:
                # Normalize volume to price scale
                price_cols = [col for col in ohlc_columns if col in df.columns]
                if price_cols:
                    price_max = df[price_cols].max().max()
                    price_min = df[price_cols].min().min()
                    price_range = price_max - price_min
                    
                    volume_normalized = [(v / max(volume_values)) * price_range * 0.2 + price_min 
                                       for v in volume_values]
                    plt.bar(x_values, volume_normalized, color="gray", label="Volume (norm)")
                else:
                    # If no OHLC data, plot volume as-is
                    plt.bar(x_values, volume_values, color="gray", label="Volume")
            
            plotted_columns.append('Volume')
            color_index += 1
        
        # Plot all other numeric columns
        logger.print_info("Plotting additional numeric columns...")
        for col in df.columns:
            if (col not in plotted_columns and 
                col not in special_columns and 
                pd.api.types.is_numeric_dtype(df[col])):
                
                try:
                    values = df[col].fillna(method='ffill').fillna(0).tolist()
                    
                    # Skip columns with all zeros or very small variance
                    if all(v == 0 for v in values):
                        logger.print_debug(f"Skipping column {col} - all zeros")
                        continue
                    
                    if np.var(values) < 1e-10:
                        logger.print_debug(f"Skipping column {col} - no variance")
                        continue
                    
                    # Choose color and marker style
                    color = colors[color_index % len(colors)]
                    
                    # Use different markers for different types of indicators
                    if 'direction' in col.lower() or 'signal' in col.lower():
                        # Trading signals - use scatter plot
                        plt.scatter(x_values, values, color=color, label=col, marker="*")
                    elif 'pv' in col.lower() or 'pressure' in col.lower():
                        # Pressure-related indicators - use thick lines
                        plt.plot(x_values, values, color=color, label=col, marker="+")
                    elif 'hl' in col.lower():
                        # HL indicators - use dots
                        plt.plot(x_values, values, color=color, label=col, marker=".")
                    elif 'predicted' in col.lower() or 'pprice' in col.lower():
                        # Predicted prices - use dashed lines
                        plt.plot(x_values, values, color=color, label=col, marker=".")
                    else:
                        # Default - solid line
                        plt.plot(x_values, values, color=color, label=col, marker="o")
                    
                    plotted_columns.append(col)
                    color_index += 1
                    
                    logger.print_debug(f"Plotted column: {col}")
                    
                except Exception as e:
                    logger.print_warning(f"Could not plot column {col}: {e}")
        
        # Configure plot appearance
        plt.title(title)
        plt.xlabel("Time / Bar Index")
        plt.ylabel("Values (Mixed Scale)")
        
        # Show legend
        plt.show_legend()
        
        # Display the plot
        logger.print_info("Displaying auto terminal plot...")
        plt.show()
        
        # Show summary of plotted data
        _show_auto_plot_summary(df, plotted_columns)
        
        logger.print_success(f"Auto terminal plot generated successfully! Plotted {len(plotted_columns)} columns.")
        
    except Exception as e:
        logger.print_error(f"Error generating auto terminal plot: {e}")
        logger.print_debug(f"Exception details: {type(e).__name__}: {e}")


def _show_auto_plot_summary(df: pd.DataFrame, plotted_columns: list) -> None:
    """Display summary of the auto plot."""
    
    print("\n" + "="*70)
    print("📊 AUTO TERMINAL PLOT SUMMARY")
    print("="*70)
    
    print(f"📈 DATA OVERVIEW:")
    print(f"   Total Rows:        {len(df)}")
    print(f"   Total Columns:     {len(df.columns)}")
    print(f"   Plotted Columns:   {len(plotted_columns)}")
    print(f"   Skipped Columns:   {len(df.columns) - len(plotted_columns)}")
    
    print(f"\n🎨 PLOTTED COLUMNS:")
    for i, col in enumerate(plotted_columns, 1):
        if col in df.columns:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                print(f"   {i:2d}. {col:<20} | Min: {col_data.min():>10.3f} | Max: {col_data.max():>10.3f} | Avg: {col_data.mean():>10.3f}")
            else:
                print(f"   {i:2d}. {col:<20} | No valid data")
    
    # Show non-plotted columns
    non_plotted = [col for col in df.columns if col not in plotted_columns]
    if non_plotted:
        print(f"\n⏭️  SKIPPED COLUMNS:")
        for col in non_plotted:
            dtype = str(df[col].dtype)
            print(f"      • {col:<20} ({dtype})")
    
    print("\n" + "="*70)
    print("💡 Auto plotting displays all numeric columns with unique colors and markers")
    print("   Different marker styles are used for different types of indicators:")
    print("   • Trading signals: * (star markers)")
    print("   • Pressure/PV: + (plus markers)")
    print("   • HL indicators: . (dot markers)")
    print("   • Predicted prices: dashed lines")
    print("   • OHLC data: connected lines with specific markers")
    print("="*70 + "\n")


def plot_column_comparison(df: pd.DataFrame, col1: str, col2: str, title: str = "Column Comparison") -> None:
    """
    Plot two specific columns for comparison in terminal.
    
    Args:
        df (pd.DataFrame): DataFrame containing the columns
        col1 (str): First column name
        col2 (str): Second column name
        title (str): Title for the plot
    """
    try:
        logger.print_info(f"Comparing columns: {col1} vs {col2}")
        
        # Clear any previous plots
        plt.clear_data()
        plt.clear_figure()
        
        # Validate columns exist
        if col1 not in df.columns or col2 not in df.columns:
            logger.print_error(f"Columns not found. Available: {list(df.columns)}")
            return
        
        # Set terminal size and theme
        plt.theme('dark')
        plt.plot_size(120, 25)
        
        # Create time axis
        x_values = list(range(len(df)))
        
        # Get column data
        values1 = df[col1].fillna(method='ffill').fillna(0).tolist()
        values2 = df[col2].fillna(method='ffill').fillna(0).tolist()
        
        # Plot both columns
        plt.plot(x_values, values1, color="green", label=col1, marker="o")
        plt.plot(x_values, values2, color="red", label=col2, marker="s")
        
        # Configure plot
        plt.title(title)
        plt.xlabel("Time / Bar Index")
        plt.ylabel("Values")
        plt.show_legend()
        
        # Display
        plt.show()
        
        # Show comparison statistics
        print(f"\n📊 COMPARISON STATISTICS:")
        print(f"   {col1}: Min={min(values1):.3f}, Max={max(values1):.3f}, Avg={np.mean(values1):.3f}")
        print(f"   {col2}: Min={min(values2):.3f}, Max={max(values2):.3f}, Avg={np.mean(values2):.3f}")
        
        correlation = np.corrcoef(values1, values2)[0, 1] if len(values1) > 1 else 0
        print(f"   Correlation: {correlation:.3f}")
        
        logger.print_success("Column comparison plot generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating comparison plot: {e}")


def plot_histogram_terminal(df: pd.DataFrame, column: str, bins: int = 20, title: str = "Histogram") -> None:
    """
    Plot a histogram of a specific column in terminal.
    
    Args:
        df (pd.DataFrame): DataFrame containing the column
        column (str): Column name to plot
        bins (int): Number of histogram bins
        title (str): Title for the plot
    """
    try:
        logger.print_info(f"Creating histogram for column: {column}")
        
        if column not in df.columns:
            logger.print_error(f"Column {column} not found")
            return
        
        # Clear plots
        plt.clear_data()
        plt.clear_figure()
        
        # Set theme and size
        plt.theme('dark')
        plt.plot_size(100, 20)
        
        # Get data and create histogram
        data = df[column].dropna().tolist()
        if not data:
            logger.print_error(f"No valid data in column {column}")
            return
        
        # Use plotext's hist function
        plt.hist(data, bins=bins, color="blue")
        plt.title(f"{title} - {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        
        plt.show()
        
        # Show statistics
        print(f"\n📊 HISTOGRAM STATISTICS for {column}:")
        print(f"   Count: {len(data)}")
        print(f"   Mean:  {np.mean(data):.3f}")
        print(f"   Std:   {np.std(data):.3f}")
        print(f"   Min:   {min(data):.3f}")
        print(f"   Max:   {max(data):.3f}")
        
        logger.print_success("Histogram generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating histogram: {e}")
