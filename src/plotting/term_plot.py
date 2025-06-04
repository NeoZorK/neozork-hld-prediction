# src/plotting/term_plot.py
"""
Terminal plotting using plotext for OHLCV and indicator panels.
Supports candlesticks, bars, and multi-panel indicators in the terminal.
"""
import plotext as plt
import pandas as pd
from src.common import logger
from src.common.constants import TradingRule

def plot_indicator_results_term(df: pd.DataFrame, rule: TradingRule, title: str = "Indicator Results"):
    """
    Plots OHLCV and indicators in the terminal using plotext.
    Main panel: candlestick chart. Below: volume, PV, HL, Pressure, etc.
    """
    if df is None or df.empty:
        logger.print_warning("No data to plot in terminal mode.")
        return

    # Ensure datetime index
    if not isinstance(df.index, pd.DatetimeIndex):
        for col in ['Timestamp', 'timestamp', 'Date', 'date', 'Datetime', 'datetime']:
            if col in df.columns:
                df = df.copy()
                df[col] = pd.to_datetime(df[col], errors='coerce')
                df = df.set_index(col)
                break
        if not isinstance(df.index, pd.DatetimeIndex):
            logger.print_warning("DataFrame index is not a DatetimeIndex after attempted conversion. Plotting might fail.")

    # Clear any previous plots
    plt.clear_figure()
    
    # Main candlestick panel
    if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
        # Convert dates to string format that plotext expects
        dates = [date.strftime('%Y-%m-%d') for date in df.index]
        
        # Prepare data in the format plotext expects
        data = {
            'Open': df['Open'].tolist(),
            'High': df['High'].tolist(),
            'Low': df['Low'].tolist(),
            'Close': df['Close'].tolist()
        }
        
        # Create candlestick plot
        plt.candlestick(dates, data, label="OHLC")
        
        # Add volume as bar chart if present (on a subplot)
        if 'Volume' in df.columns and len(df) > 0:
            plt.subplot(2, 1, 2)  # Create subplot for volume
            plt.bar(dates, df['Volume'].tolist(), label="Volume", color="cyan")
            plt.title("Volume")
            
            # Switch back to main plot for any additional indicators
            plt.subplot(2, 1, 1)
        
        # Add additional indicator lines if present
        for col, color in zip(['PV', 'HL', 'Pressure', 'RSI', 'MA'], ['orange', 'brown', 'blue', 'magenta', 'green']):
            if col in df.columns:
                plt.plot(dates, df[col].tolist(), label=col, color=color)
                
    else:
        logger.print_warning("Missing OHLC columns for candlestick plot. Skipping main panel.")
        return

    plt.title(title)
    plt.show()
