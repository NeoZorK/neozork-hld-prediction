# src/plotting/term_plot.py
"""
Terminal plotting using plotext for OHLCV and indicator panels.
Supports line charts, bars, and multi-panel indicators in the terminal.
"""
import plotext as plt
import pandas as pd
import numpy as np
from src.common import logger
from src.common.constants import TradingRule

def plot_indicator_results_term(df: pd.DataFrame, rule: TradingRule, title: str = "Indicator Results"):
    """
    Plots OHLCV and indicators in the terminal using plotext.
    Main panel: OHLC line charts. Below: volume, PV, HL, Pressure, etc.
    """
    if df is None or df.empty:
        logger.print_warning("No data to plot in terminal mode.")
        return

    try:
        # Clear any previous plots
        plt.clear_data()
        plt.clear_color()
        
        # Ensure datetime index
        if not isinstance(df.index, pd.DatetimeIndex):
            for col in ['Timestamp', 'timestamp', 'Date', 'date', 'Datetime', 'datetime']:
                if col in df.columns:
                    df = df.copy()
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    df = df.set_index(col)
                    break
            if not isinstance(df.index, pd.DatetimeIndex):
                logger.print_warning("DataFrame index is not a DatetimeIndex after attempted conversion. Using numeric index.")
                x_data = list(range(len(df)))
                x_labels = [f"T{i}" for i in range(len(df))]
            else:
                x_data = list(range(len(df)))
                x_labels = [d.strftime('%m-%d') for d in df.index]
        else:
            x_data = list(range(len(df)))
            x_labels = [d.strftime('%m-%d') for d in df.index]

        # Limit data points for terminal display (last 50 points)
        max_points = 50
        if len(df) > max_points:
            df = df.tail(max_points)
            x_data = list(range(len(df)))
            if isinstance(df.index, pd.DatetimeIndex):
                x_labels = [d.strftime('%m-%d') for d in df.index]
            else:
                x_labels = [f"T{i}" for i in range(len(df))]

        # Set up the main plot with multiple subplots
        plt.subplots(2, 1)
        
        # Main OHLC panel (subplot 1)
        plt.subplot(1, 1)
        
        # Plot OHLC as line charts instead of candlesticks (more reliable)
        if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
            plt.plot(x_data, df['High'].tolist(), label="High", color="green", marker="dot")
            plt.plot(x_data, df['Low'].tolist(), label="Low", color="red", marker="dot") 
            plt.plot(x_data, df['Close'].tolist(), label="Close", color="blue", marker="dot")
            plt.plot(x_data, df['Open'].tolist(), label="Open", color="orange", marker="dot")
        else:
            logger.print_warning("Missing OHLC columns. Showing available price data.")
            # Try to plot any available price columns
            price_cols = [col for col in df.columns if col.lower() in ['price', 'close', 'value']]
            if price_cols:
                plt.plot(x_data, df[price_cols[0]].tolist(), label=price_cols[0], color="blue")

        plt.title(f"{title} - OHLC")
        plt.xlabel("Time")
        plt.ylabel("Price")
        
        # Set x-axis labels (sample every 5th for readability)
        step = max(1, len(x_labels) // 10)
        plt.xticks(x_data[::step], x_labels[::step])
        
        # Indicators and Volume panel (subplot 2)
        plt.subplot(2, 1)
        
        # Add volume as bar chart if present
        if 'Volume' in df.columns and df['Volume'].sum() > 0:
            # Normalize volume for better display
            vol_norm = df['Volume'] / df['Volume'].max() * 100
            plt.bar(x_data, vol_norm.tolist(), label="Volume(norm)", color="cyan")

        # Add additional indicator lines if present
        indicator_colors = {
            'PV': 'red',
            'HL': 'yellow', 
            'Pressure': 'magenta',
            'RSI': 'green',
            'MA': 'blue',
            'SMA': 'blue',
            'EMA': 'cyan'
        }
        
        plotted_indicators = []
        for col in df.columns:
            if col in indicator_colors and not df[col].isna().all():
                plt.plot(x_data, df[col].tolist(), label=col, color=indicator_colors[col])
                plotted_indicators.append(col)

        if plotted_indicators:
            plt.title("Indicators & Volume")
        else:
            plt.title("Volume")
            
        plt.xlabel("Time")
        plt.ylabel("Indicator Values")
        
        # Set x-axis labels for indicators panel
        plt.xticks(x_data[::step], x_labels[::step])
        
        # Display the plots
        plt.show()
        
        # Print summary info
        logger.print_info(f"Terminal plot generated with {len(df)} data points")
        if plotted_indicators:
            logger.print_info(f"Indicators plotted: {', '.join(plotted_indicators)}")
            
    except Exception as e:
        logger.print_error(f"Error in terminal plotting: {str(e)}")
        # Fallback to simple line plot
        try:
            plt.clear_data()
            if 'Close' in df.columns:
                plt.plot(df['Close'].tolist(), label="Close Price")
                plt.title(f"{title} - Simple Plot")
                plt.show()
        except Exception as fallback_e:
            logger.print_error(f"Fallback plotting also failed: {str(fallback_e)}")
            print(f"Terminal plotting unavailable. Error: {str(e)}")
