# -*- coding: utf-8 -*-
# src/plotting/term_auto_plot.py

"""
Terminal-based auto plotting using plotext for displaying all DataFrame columns.
Beautiful candlestick charts with enhanced styling and multi-panel layouts.
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
    Automatically plot all numeric columns from a DataFrame in terminal with beautiful styling.
    Uses candlestick charts for OHLC data and line plots for other indicators.
    
    Args:
        df (pd.DataFrame): DataFrame with data to plot
        title (str): Title for the plot
    """
    try:
        logger.print_info("Generating beautiful auto terminal plot for all DataFrame columns...")
        
        # Clear any previous plots
        plt.clear_data()
        plt.clear_figure()
        
        # Validate input data
        if df is None or df.empty:
            logger.print_error("DataFrame is None or empty, cannot plot")
            return
        
        # Check if we have OHLC data for candlestick chart
        ohlc_columns = ['Open', 'High', 'Low', 'Close']
        has_ohlc = all(col in df.columns for col in ohlc_columns)
        has_volume = 'Volume' in df.columns and not df['Volume'].isna().all()
        
        # Set up layout based on available data
        if has_ohlc and has_volume:
            plt.subplots(2, 1)  # Price + Volume panels
            main_plot_size = (140*3, 35*3)  # 3x larger
        elif has_ohlc:
            plt.subplots(1, 1)  # Single price panel
            main_plot_size = (140*3, 25*3)  # 3x larger
        else:
            plt.subplots(1, 1)  # Single indicator panel
            main_plot_size = (140*3, 25*3)  # 3x larger
        
        plt.plot_size(*main_plot_size)
        plt.theme('matrix')  # Use unified matrix theme for all plots
        
        # Create time axis
        x_values = list(range(len(df)))
        
        # MAIN PANEL: OHLC Candlestick or Indicators
        if has_ohlc:
            logger.print_info("Creating beautiful OHLC candlestick chart...")
            if has_volume:
                plt.subplot(1, 1)  # Top panel
            # Prepare OHLC data for candlestick
            ohlc_data = {
                'Open': df['Open'].ffill().fillna(df['Close']).tolist(),
                'High': df['High'].ffill().fillna(df['Close']).tolist(),
                'Low': df['Low'].ffill().fillna(df['Close']).tolist(),
                'Close': df['Close'].ffill().fillna(df['Open']).tolist()
            }
            plt.candlestick(x_values, ohlc_data)
            plt.title(f"{title} - Auto Chart (OHLC + Indicators)")
            if not has_volume:
                plt.xlabel("Time / Bar Index")
            plt.ylabel("Price")
            # Add other indicators as overlays on the price chart
            _add_indicator_overlays(df, x_values, skip_columns={'Open', 'High', 'Low', 'Close', 'Volume'})
        else:
            logger.print_info("Creating beautiful multi-indicator chart...")
            plt.title(f"{title} - Auto Indicators Chart")
            plt.xlabel("Time / Bar Index") 
            plt.ylabel("Values")
            # Plot all numeric columns as indicators
            _add_indicator_overlays(df, x_values, skip_columns={'Volume'})
        
        # VOLUME PANEL (if available)
        if has_volume:
            logger.print_info("Creating beautiful volume panel...")
            plt.subplot(2, 1)  # Bottom panel
            
            volume_values = df['Volume'].fillna(0).tolist()
            plt.bar(x_values, volume_values, color="cyan+", label="📊 Volume")
            
            plt.title("📊 Trading Volume")
            plt.xlabel("Time / Bar Index")
            plt.ylabel("Volume")
        
        # Display the plot
        logger.print_info("Displaying beautiful auto terminal plot...")
        plt.show()
        
        # Show enhanced statistics
        _show_auto_statistics(df, title)
        
        logger.print_success("Beautiful auto terminal plot generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating auto terminal plot: {e}")
        logger.print_debug(f"Exception details: {type(e).__name__}: {e}")


def _add_indicator_overlays(df: pd.DataFrame, x_values: list, skip_columns: set) -> None:
    """Add indicator overlays with beautiful styling and emojis."""
    
    # Enhanced color palette for better visual distinction
    colors = [
        "yellow+", "magenta+", "green+", "red+", "blue+", "cyan+", 
        "orange", "brown", "white", "gray"
    ]
    
    # Enhanced marker set for variety
    markers = [".", "*", "x", "+", "o", "^", "v", "s", "d"]
    
    # Clean labels for common indicators without emojis  
    indicator_labels = {
        'HL': 'HL Range', 'Pressure': 'Pressure', 'PV': 'PV', 'RSI': 'RSI', 'MACD': 'MACD',
        'SMA': 'SMA', 'EMA': 'EMA', 'BB': 'Bollinger Bands', 'Direction': 'Direction', 'Signal': 'Signal',
        'PPrice1': 'Predicted Low', 'PPrice2': 'Predicted High', 'Momentum': 'Momentum', 'Trend': 'Trend'
    }
    
    color_index = 0
    marker_index = 0
    
    # Extended skip columns
    extended_skip = skip_columns.union({
        'DateTime', 'Timestamp', 'Date', 'Time', 'Index', 'index'
    })
    
    for col in df.columns:
        if col not in extended_skip and pd.api.types.is_numeric_dtype(df[col]):
            try:
                values = df[col].fillna(0).tolist()
                color = colors[color_index % len(colors)]
                marker = markers[marker_index % len(markers)]
                
                # Add clean label if available
                label = col
                for key, clean_label in indicator_labels.items():
                    if key.upper() in col.upper():
                        label = clean_label
                        break
                
                plt.plot(x_values, values, color=color, label=label, marker=marker)
                
                color_index += 1
                marker_index += 1
                
            except Exception as e:
                logger.print_warning(f"Could not plot column {col}: {e}")


def _show_auto_statistics(df: pd.DataFrame, title: str) -> None:
    """Display beautiful auto statistics."""
    
    header_line = "═" * 80
    print(f"\n{header_line}")
    print(f"{'📊 BEAUTIFUL AUTO PLOT STATISTICS':^80}")
    print(f"{title:^80}")
    print(f"{header_line}")
    
    # Data overview
    print(f"📈 DATA OVERVIEW:")
    print(f"   📊 Total Rows:     {len(df)}")
    print(f"   📋 Total Columns:  {len(df.columns)}")
    print(f"   🔢 Numeric Cols:   {df.select_dtypes(include=[np.number]).shape[1]}")
    
    # Column analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(f"\n📊 COLUMN STATISTICS:")
        for col in numeric_cols:
            if col in df.columns:
                try:
                    col_data = df[col].dropna()
                    if len(col_data) > 0:
                        print(f"   📋 {col}:")
                        print(f"      📈 Max: {col_data.max():.3f}")
                        print(f"      📉 Min: {col_data.min():.3f}")
                        print(f"      📊 Avg: {col_data.mean():.3f}")
                except Exception:
                    pass
    
    # OHLC specific stats if available
    ohlc_columns = ['Open', 'High', 'Low', 'Close']
    if all(col in df.columns for col in ohlc_columns):
        print(f"\n📈 OHLC STATISTICS:")
        print(f"   🔺 Highest:    {df['High'].max():.5f}")
        print(f"   🔻 Lowest:     {df['Low'].min():.5f}")
        print(f"   🎯 Final:      {df['Close'].iloc[-1]:.5f}")
        print(f"   🚀 Initial:    {df['Open'].iloc[0]:.5f}")
        
        price_change = df['Close'].iloc[-1] - df['Open'].iloc[0]
        price_change_pct = (price_change / df['Open'].iloc[0]) * 100
        direction_emoji = "📈" if price_change >= 0 else "📉"
        print(f"   {direction_emoji} Change:     {price_change:+.5f} ({price_change_pct:+.2f}%)")
    
    print(f"\n{header_line}")
    print(f"{'🎨 Beautiful Auto Terminal Charts - All Your Data Visualized':^80}")
    print(f"{header_line}\n")


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
        plt.theme('retro')
        plt.plot_size(120, 25)
        
        # Create time axis
        x_values = list(range(len(df)))
        
        # Get column data
        values1 = df[col1].ffill().fillna(0).tolist()
        values2 = df[col2].ffill().fillna(0).tolist()
        
        # Plot both columns
        plt.plot(x_values, values1, color="green+", label=f"📈 {col1}", marker="o")
        plt.plot(x_values, values2, color="red+", label=f"📉 {col2}", marker="s")
        
        # Configure plot
        plt.title(f"📊 {title}")
        plt.xlabel("Time / Bar Index")
        plt.ylabel("Values")
        
        # Display
        plt.show()
        
        # Show comparison statistics
        print(f"\n📊 COMPARISON STATISTICS:")
        print(f"   📈 {col1}: Min={min(values1):.3f}, Max={max(values1):.3f}, Avg={np.mean(values1):.3f}")
        print(f"   📉 {col2}: Min={min(values2):.3f}, Max={max(values2):.3f}, Avg={np.mean(values2):.3f}")
        
        correlation = np.corrcoef(values1, values2)[0, 1] if len(values1) > 1 else 0
        print(f"   🔗 Correlation: {correlation:.3f}")
        
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
        plt.theme('retro')
        plt.plot_size(100, 20)
        
        # Get data and create histogram
        data = df[column].dropna().tolist()
        if not data:
            logger.print_error(f"No valid data in column {column}")
            return
        
        # Use plotext's hist function
        plt.hist(data, bins=bins, color="blue+")
        plt.title(f"📊 {title} - {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        
        plt.show()
        
        # Show statistics
        print(f"\n📊 HISTOGRAM STATISTICS for {column}:")
        print(f"   📋 Count: {len(data)}")
        print(f"   📊 Mean:  {np.mean(data):.3f}")
        print(f"   📈 Std:   {np.std(data):.3f}")
        print(f"   📉 Min:   {min(data):.3f}")
        print(f"   🔺 Max:   {max(data):.3f}")
        
        logger.print_success("Histogram generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating histogram: {e}")

