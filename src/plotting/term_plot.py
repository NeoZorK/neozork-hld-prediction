# -*- coding: utf-8 -*-
# src/plotting/term_plot.py

"""
Terminal-based plotting functions for visualizing indicator results using Rich library.
This module provides text-based charts displayed directly in the terminal.
"""

import pandas as pd
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.align import Align
from rich import box
from ..common import logger
from ..common.constants import TradingRule, BUY, SELL, NOTRADE


def plot_indicator_results_term(df_results, rule, title="Terminal Plot", data_source="demo", **kwargs):
    """
    Creates terminal-based visualization for indicator results using Rich library.
    
    Args:
        df_results (pd.DataFrame): The DataFrame with OHLC data and indicators.
        rule (TradingRule): The trading rule used in analysis.
        title (str): Title for the plot.
        data_source (str): Source of the data (for special formatting).
        **kwargs: Additional keyword arguments.
    
    Returns:
        None: Displays the chart directly in terminal.
    """
    try:
        console = Console()
        
        # Validate DataFrame
        if df_results is None or df_results.empty:
            console.print("[red]Error: DataFrame is empty or None[/red]")
            return None
            
        # Required OHLC columns
        required_columns = ['Open', 'High', 'Low', 'Close']
        if not all(col in df_results.columns for col in required_columns):
            console.print(f"[red]Error: DataFrame must contain columns {required_columns}[/red]")
            return None
        
        # Display header
        header_text = f"[bold cyan]{title}[/bold cyan]"
        if hasattr(rule, 'name'):
            header_text += f" - [yellow]{rule.name}[/yellow]"
        elif isinstance(rule, str):
            header_text += f" - [yellow]{rule}[/yellow]"
            
        console.print(Panel(header_text, box=box.DOUBLE))
        
        # Get the last 20 rows for display (terminal space is limited)
        display_df = df_results.tail(20).copy()
        
        # Create main OHLC chart
        create_ohlc_chart(console, display_df, rule)
        
        # Create indicator charts based on rule
        if rule == TradingRule.Predict_High_Low_Direction or (isinstance(rule, str) and rule.upper() == 'PHLD'):
            create_phld_charts(console, display_df)
        elif rule == TradingRule.AUTO or (isinstance(rule, str) and rule.upper() == 'AUTO'):
            create_auto_charts(console, display_df)
        else:
            create_generic_charts(console, display_df)
            
        # Display summary statistics
        create_summary_table(console, df_results)
        
        return None
        
    except Exception as e:
        logger.print_error(f"Error in terminal plotting: {str(e)}")
        console = Console()
        console.print(f"[red]Error creating terminal plot: {str(e)}[/red]")
        return None


def create_ohlc_chart(console, df, rule):
    """Create a text-based OHLC chart with buy/sell signals."""
    
    console.print("\n[bold blue]📈 OHLC Chart with Signals[/bold blue]")
    
    # Create table for OHLC data
    table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)
    table.add_column("Time", style="dim", width=12)
    table.add_column("Open", justify="right", style="cyan")
    table.add_column("High", justify="right", style="green")
    table.add_column("Low", justify="right", style="red")
    table.add_column("Close", justify="right", style="white")
    table.add_column("Direction", justify="center", width=10)
    table.add_column("Signal", justify="center", width=8)
    
    for idx, row in df.iterrows():
        # Format timestamp
        if hasattr(idx, 'strftime'):
            time_str = idx.strftime("%H:%M")
        else:
            time_str = str(idx)[-8:]  # Last 8 characters
            
        # Format prices
        open_val = f"{row['Open']:.4f}"
        high_val = f"{row['High']:.4f}"
        low_val = f"{row['Low']:.4f}"
        close_val = f"{row['Close']:.4f}"
        
        # Determine direction arrow
        if row['Close'] > row['Open']:
            direction = "[green]↗[/green]"
        elif row['Close'] < row['Open']:
            direction = "[red]↘[/red]"
        else:
            direction = "[yellow]→[/yellow]"
            
        # Determine signal based on Direction column if available
        signal = ""
        if 'Direction' in row and pd.notna(row['Direction']):
            direction_val = row['Direction']
            if direction_val == BUY:
                signal = "[green]BUY ⬆[/green]"
            elif direction_val == SELL:
                signal = "[red]SELL ⬇[/red]"
            elif direction_val == NOTRADE:
                signal = "[yellow]HOLD ■[/yellow]"
                
        table.add_row(time_str, open_val, high_val, low_val, close_val, direction, signal)
    
    console.print(table)


def create_phld_charts(console, df):
    """Create charts specific to PHLD (Predict High Low Direction) rule."""
    
    # HL Chart
    if 'HL' in df.columns:
        console.print("\n[bold yellow]📊 HL (High-Low) Field[/bold yellow]")
        create_line_chart(console, df, 'HL', "cyan")
    
    # Pressure Chart
    if 'Pressure' in df.columns:
        console.print("\n[bold magenta]⚡ Pressure Field[/bold magenta]")
        create_line_chart(console, df, 'Pressure', "magenta")
    
    # Pressure Vector Chart
    if 'PV' in df.columns:
        console.print("\n[bold green]🎯 Pressure Vector (PV) Field[/bold green]")
        create_line_chart(console, df, 'PV', "green")
    
    # PPrice levels if available
    if 'PPrice1' in df.columns and 'PPrice2' in df.columns:
        console.print("\n[bold blue]🎯 Predicted Price Levels[/bold blue]")
        create_price_levels_chart(console, df)


def create_auto_charts(console, df):
    """Create charts for AUTO mode showing all available indicators."""
    
    # Find all numeric columns except OHLC
    ohlc_cols = {'Open', 'High', 'Low', 'Close', 'Volume'}
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    indicator_cols = [col for col in numeric_cols if col not in ohlc_cols]
    
    for col in indicator_cols:
        if col in df.columns and df[col].notna().any():
            console.print(f"\n[bold cyan]📈 {col}[/bold cyan]")
            create_line_chart(console, df, col, "cyan")


def create_generic_charts(console, df):
    """Create charts for other trading rules."""
    
    # Show common indicators if available
    common_indicators = ['HL', 'Pressure', 'PV', 'Volume']
    
    for indicator in common_indicators:
        if indicator in df.columns and df[indicator].notna().any():
            color = {
                'HL': 'yellow',
                'Pressure': 'magenta', 
                'PV': 'green',
                'Volume': 'blue'
            }.get(indicator, 'white')
            
            console.print(f"\n[bold {color}]📊 {indicator}[/bold {color}]")
            create_line_chart(console, df, indicator, color)


def create_line_chart(console, df, column, color="white"):
    """Create a simple ASCII line chart for a data column."""
    
    if column not in df.columns or df[column].isna().all():
        console.print(f"[dim]No data available for {column}[/dim]")
        return
        
    values = df[column].dropna()
    if len(values) == 0:
        console.print(f"[dim]No valid data for {column}[/dim]")
        return
    
    # Create simple horizontal bar chart
    table = Table(show_header=True, header_style=f"bold {color}", box=box.SIMPLE)
    table.add_column("Time", style="dim", width=12)
    table.add_column("Value", justify="right", style=color, width=12)
    table.add_column("Chart", width=30)
    
    # Normalize values for visualization
    min_val = values.min()
    max_val = values.max()
    val_range = max_val - min_val if max_val != min_val else 1
    
    for idx, value in values.items():
        # Format timestamp
        if hasattr(idx, 'strftime'):
            time_str = idx.strftime("%H:%M")
        else:
            time_str = str(idx)[-8:]
            
        # Format value
        value_str = f"{value:.4f}"
        
        # Create simple bar
        if val_range > 0:
            normalized = (value - min_val) / val_range
            bar_length = int(normalized * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
        else:
            bar = "█" * 10 + "░" * 10
            
        table.add_row(time_str, value_str, f"[{color}]{bar}[/{color}]")
    
    console.print(table)


def create_price_levels_chart(console, df):
    """Create chart showing predicted price levels."""
    
    table = Table(show_header=True, header_style="bold blue", box=box.SIMPLE)
    table.add_column("Time", style="dim", width=12)
    table.add_column("PPrice1", justify="right", style="green", width=10)
    table.add_column("PPrice2", justify="right", style="red", width=10)
    table.add_column("Current", justify="right", style="white", width=10)
    table.add_column("Position", justify="center", width=15)
    
    for idx, row in df.iterrows():
        if hasattr(idx, 'strftime'):
            time_str = idx.strftime("%H:%M")
        else:
            time_str = str(idx)[-8:]
            
        pp1 = f"{row['PPrice1']:.4f}" if 'PPrice1' in row and pd.notna(row['PPrice1']) else "N/A"
        pp2 = f"{row['PPrice2']:.4f}" if 'PPrice2' in row and pd.notna(row['PPrice2']) else "N/A"
        current = f"{row['Close']:.4f}"
        
        # Determine position relative to price levels
        position = ""
        if 'PPrice1' in row and 'PPrice2' in row and pd.notna(row['PPrice1']) and pd.notna(row['PPrice2']):
            if row['Close'] < row['PPrice1']:
                position = "[green]Below P1[/green]"
            elif row['Close'] > row['PPrice2']:
                position = "[red]Above P2[/red]"
            else:
                position = "[yellow]Between[/yellow]"
        
        table.add_row(time_str, pp1, pp2, current, position)
    
    console.print(table)


def create_summary_table(console, df):
    """Create summary statistics table."""
    
    console.print("\n[bold white]📋 Summary Statistics[/bold white]")
    
    table = Table(show_header=True, header_style="bold white", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white", justify="right")
    
    # Basic stats
    table.add_row("Total Rows", str(len(df)))
    table.add_row("Date Range", f"{df.index[0]} to {df.index[-1]}" if len(df) > 0 else "N/A")
    
    # Price stats
    if 'Close' in df.columns:
        close_prices = df['Close'].dropna()
        if len(close_prices) > 0:
            table.add_row("Current Price", f"{close_prices.iloc[-1]:.4f}")
            table.add_row("Min Price", f"{close_prices.min():.4f}")
            table.add_row("Max Price", f"{close_prices.max():.4f}")
            table.add_row("Price Change %", f"{((close_prices.iloc[-1] / close_prices.iloc[0] - 1) * 100):.2f}%" if len(close_prices) > 1 else "N/A")
    
    # Signal stats
    if 'Direction' in df.columns:
        directions = df['Direction'].dropna()
        if len(directions) > 0:
            buy_signals = (directions == BUY).sum()
            sell_signals = (directions == SELL).sum()
            hold_signals = (directions == NOTRADE).sum()
            
            table.add_row("Buy Signals", str(buy_signals))
            table.add_row("Sell Signals", str(sell_signals))
            table.add_row("Hold Signals", str(hold_signals))
    
    console.print(table)


def create_term_auto_plot(df_results, title="Auto Terminal Plot", **kwargs):
    """
    Terminal plotting function specifically for AUTO mode.
    Shows all available columns in the DataFrame.
    """
    console = Console()
    
    # Use the main plotting function with AUTO rule
    return plot_indicator_results_term(df_results, TradingRule.AUTO, title=title, **kwargs)
