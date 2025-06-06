# -*- coding: utf-8 -*-
# src/plotting/term_plot.py

"""
Terminal-based plotting using plotext for ASCII charts in terminal/SSH environments.
"""

import pandas as pd
import numpy as np
import plotext as plt
from typing import Optional, Union

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    # Fallback to relative imports when run as module
    from ..common import logger
    from ..common.constants import TradingRule, BUY, SELL, NOTRADE


def plot_indicator_results_term(df_results: pd.DataFrame, 
                               rule: Union[TradingRule, str], 
                               title: str = "Terminal Plot",
                               output_path: Optional[str] = None) -> None:
    """
    Plot indicator results in terminal using plotext (ASCII charts).
    
    Args:
        df_results (pd.DataFrame): DataFrame with OHLCV and calculation results
        rule (TradingRule | str): Trading rule enum or string
        title (str): Title for the plot
        output_path (str, optional): Not used for terminal plots, kept for compatibility
    """
    try:
        logger.print_info("Generating terminal-based ASCII plot using plotext...")
        
        # Clear any previous plots
        plt.clear_data()
        plt.clear_figure()
        
        # Validate input data
        if df_results is None or df_results.empty:
            logger.print_error("DataFrame is None or empty, cannot plot")
            return
        
        # Check for required OHLC columns
        required_columns = ['Open', 'High', 'Low', 'Close']
        missing_columns = [col for col in required_columns if col not in df_results.columns]
        if missing_columns:
            logger.print_error(f"Missing required columns: {missing_columns}")
            return
        
        # Convert rule to string for processing
        rule_str = rule.name if hasattr(rule, 'name') else str(rule)
        
        # Prepare data for plotting
        df = df_results.copy()
        
        # Create time axis - use index or create sequential numbers
        if df.index.name == 'DateTime' or 'DateTime' in df.columns:
            time_col = df.index if df.index.name == 'DateTime' else df['DateTime']
            # Convert to numeric for plotext (it doesn't handle datetime well)
            x_values = list(range(len(df)))
            x_labels = [str(t)[:10] if hasattr(t, 'strftime') else str(t) for t in time_col]
        else:
            x_values = list(range(len(df)))
            x_labels = [f"Bar {i}" for i in x_values]
        
        # Set terminal size for better visualization
        plt.theme('dark')  # Use dark theme for better terminal contrast
        plt.plot_size(120, 30)  # Width=120, Height=30 characters
        
        # Plot OHLC data as candlestick-like representation
        logger.print_info("Plotting OHLC candlestick data...")
        
        # Plot High-Low range as vertical lines (using scatter with vertical bars)
        high_values = df['High'].fillna(0).tolist()
        low_values = df['Low'].fillna(0).tolist()
        
        # Create candlestick effect using multiple plots
        plt.scatter(x_values, high_values, marker="^", color="cyan", label="High")
        plt.scatter(x_values, low_values, marker="v", color="cyan", label="Low")
        
        # Plot Open and Close
        open_values = df['Open'].fillna(0).tolist()
        close_values = df['Close'].fillna(0).tolist()
        
        plt.plot(x_values, open_values, color="green", label="Open", marker="o")
        plt.plot(x_values, close_values, color="red", label="Close", marker="s")
        
        # Add Volume if available (as bar chart on secondary scale)
        if 'Volume' in df.columns:
            logger.print_info("Adding Volume data...")
            volume_values = df['Volume'].fillna(0).tolist()
            # Normalize volume to fit with price scale
            if max(volume_values) > 0:
                volume_normalized = [(v / max(volume_values)) * (max(high_values) - min(low_values)) * 0.3 + min(low_values) 
                                   for v in volume_values]
                plt.bar(x_values, volume_normalized, color="gray", label="Volume (normalized)")
        
        # Add financial indicators based on the trading rule
        if rule_str.upper() in ['PHLD', 'PREDICT_HIGH_LOW_DIRECTION']:
            _add_phld_indicators_term(df, x_values)
        elif rule_str.upper() in ['PV', 'PRESSURE_VECTOR']:
            _add_pv_indicators_term(df, x_values)
        elif rule_str.upper() in ['AUTO', 'AUTO_DISPLAY_ALL']:
            _add_auto_indicators_term(df, x_values)
        
        # Add predicted price lines if available
        if 'PPrice1' in df.columns:  # Predicted Low
            pprice1_values = df['PPrice1'].fillna(0).tolist()
            plt.plot(x_values, pprice1_values, color="green", label="Predicted Low", marker=".")
        
        if 'PPrice2' in df.columns:  # Predicted High
            pprice2_values = df['PPrice2'].fillna(0).tolist()
            plt.plot(x_values, pprice2_values, color="red", label="Predicted High", marker=".")
        
        # Add trading signals if available
        if 'Direction' in df.columns:
            _add_trading_signals_term(df, x_values, high_values, low_values)
        
        # Configure plot appearance
        plt.title(title)
        plt.xlabel("Time / Bar Index")
        plt.ylabel("Price")
        
        # Display the plot
        logger.print_info("Displaying terminal plot...")
        plt.show()
        
        # Show additional statistics
        _show_terminal_statistics(df, rule_str)
        
        logger.print_success("Terminal plot generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating terminal plot: {e}")
        logger.print_debug(f"Exception details: {type(e).__name__}: {e}")


def _add_phld_indicators_term(df: pd.DataFrame, x_values: list) -> None:
    """Add PHLD-specific indicators to terminal plot."""
    
    # Add HL (High-Low range in points)
    if 'HL' in df.columns:
        hl_values = df['HL'].fillna(0).tolist()
        plt.plot(x_values, hl_values, color="brown", label="HL Points", marker=".")
    
    # Add Pressure
    if 'Pressure' in df.columns:
        pressure_values = df['Pressure'].fillna(0).tolist()
        plt.plot(x_values, pressure_values, color="blue", label="Pressure", marker="x")
    
    # Add Pressure Vector (PV)
    if 'PV' in df.columns:
        pv_values = df['PV'].fillna(0).tolist()
        plt.plot(x_values, pv_values, color="orange", label="PV", marker="+")


def _add_pv_indicators_term(df: pd.DataFrame, x_values: list) -> None:
    """Add Pressure Vector specific indicators to terminal plot."""
    
    if 'PV' in df.columns:
        pv_values = df['PV'].fillna(0).tolist()
        plt.plot(x_values, pv_values, color="yellow", label="Pressure Vector", marker="*")
    
    if 'Pressure' in df.columns:
        pressure_values = df['Pressure'].fillna(0).tolist()
        plt.plot(x_values, pressure_values, color="magenta", label="Pressure", marker="x")


def _add_auto_indicators_term(df: pd.DataFrame, x_values: list) -> None:
    """Add all available indicators for AUTO mode."""
    
    # Define colors for different indicators
    colors = ["yellow", "magenta", "orange", "brown", "white", "blue+", "green+", "red+"]
    color_index = 0
    
    # Standard columns to skip
    skip_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'DateTime', 'Timestamp', 'Date', 'Time']
    
    for col in df.columns:
        if col not in skip_columns and pd.api.types.is_numeric_dtype(df[col]):
            try:
                values = df[col].fillna(0).tolist()
                color = colors[color_index % len(colors)]
                plt.plot(x_values, values, color=color, label=col, marker=".")
                color_index += 1
            except Exception as e:
                logger.print_warning(f"Could not plot column {col}: {e}")


def _add_trading_signals_term(df: pd.DataFrame, x_values: list, high_values: list, low_values: list) -> None:
    """Add trading signal markers to the plot."""
    
    direction_values = df['Direction'].fillna(NOTRADE).tolist()
    
    # Find buy and sell signals
    buy_indices = [i for i, direction in enumerate(direction_values) if direction == BUY]
    sell_indices = [i for i, direction in enumerate(direction_values) if direction == SELL]
    
    if buy_indices:
        buy_x = [x_values[i] for i in buy_indices]
        buy_y = [low_values[i] * 0.999 for i in buy_indices]  # Place slightly below Low
        plt.scatter(buy_x, buy_y, color="green+", marker="^", label="BUY Signal")
    
    if sell_indices:
        sell_x = [x_values[i] for i in sell_indices]
        sell_y = [high_values[i] * 1.001 for i in sell_indices]  # Place slightly above High
        plt.scatter(sell_x, sell_y, color="red+", marker="v", label="SELL Signal")


def _show_terminal_statistics(df: pd.DataFrame, rule_str: str) -> None:
    """Display summary statistics in terminal."""
    
    print("\n" + "="*60)
    print(f"📊 TERMINAL PLOT STATISTICS - {rule_str.upper()}")
    print("="*60)
    
    # Basic OHLC statistics
    if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
        print(f"📈 PRICE STATISTICS:")
        print(f"   Highest Price: {df['High'].max():.5f}")
        print(f"   Lowest Price:  {df['Low'].min():.5f}")
        print(f"   Close Price:   {df['Close'].iloc[-1]:.5f}")
        print(f"   Open Price:    {df['Open'].iloc[0]:.5f}")
        print(f"   Price Range:   {df['High'].max() - df['Low'].min():.5f}")
    
    # Volume statistics
    if 'Volume' in df.columns:
        print(f"📊 VOLUME STATISTICS:")
        print(f"   Total Volume:  {df['Volume'].sum():,.0f}")
        print(f"   Avg Volume:    {df['Volume'].mean():.0f}")
        print(f"   Max Volume:    {df['Volume'].max():,.0f}")
    
    # Trading signals statistics
    if 'Direction' in df.columns:
        buy_count = (df['Direction'] == BUY).sum()
        sell_count = (df['Direction'] == SELL).sum()
        notrade_count = (df['Direction'] == NOTRADE).sum()
        
        print(f"🎯 TRADING SIGNALS:")
        print(f"   BUY Signals:   {buy_count}")
        print(f"   SELL Signals:  {sell_count}")
        print(f"   NO TRADE:      {notrade_count}")
        print(f"   Total Bars:    {len(df)}")
    
    # PHLD-specific statistics
    if rule_str.upper() in ['PHLD', 'PREDICT_HIGH_LOW_DIRECTION']:
        if 'HL' in df.columns:
            print(f"📏 HL STATISTICS:")
            print(f"   Avg HL:        {df['HL'].mean():.3f} points")
            print(f"   Max HL:        {df['HL'].max():.3f} points")
        
        if 'Pressure' in df.columns:
            print(f"💨 PRESSURE STATISTICS:")
            print(f"   Avg Pressure:  {df['Pressure'].mean():.3f}")
            print(f"   Max Pressure:  {df['Pressure'].max():.3f}")
            print(f"   Min Pressure:  {df['Pressure'].min():.3f}")
        
        if 'PV' in df.columns:
            print(f"🎯 PRESSURE VECTOR STATISTICS:")
            print(f"   Avg PV:        {df['PV'].mean():.3f}")
            print(f"   Max PV:        {df['PV'].max():.3f}")
            print(f"   Min PV:        {df['PV'].min():.3f}")
    
    print("="*60)
    print("💡 Terminal plotting with plotext - ASCII charts for SSH/Docker environments")
    print("="*60 + "\n")
