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

    # Main candlestick panel
    if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
        # plotext expects lists, not Series
        opens = df['Open'].tolist()
        highs = df['High'].tolist()
        lows = df['Low'].tolist()
        closes = df['Close'].tolist()
        plt.candlestick(opens, highs, lows, closes, label="OHLC")
    else:
        logger.print_warning("Missing OHLC columns for candlestick plot. Skipping main panel.")

    # Add volume as bar chart if present
    if 'Volume' in df.columns:
        plt.bar(df.index.astype(str).tolist(), df['Volume'].tolist(), label="Volume", color="cyan")

    # Add additional indicator panels if present
    for col, color in zip(['PV', 'HL', 'Pressure', 'RSI', 'MA'], ['orange', 'brown', 'blue', 'magenta', 'green']):
        if col in df.columns:
            plt.plot(df.index.astype(str).tolist(), df[col].tolist(), label=col, color=color)

    plt.title(title)
    plt.show()
