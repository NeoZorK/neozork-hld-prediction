# src/plotting/term_auto_plot.py
"""
Terminal auto plotting for AUTO rule mode.
Displays each column in a parquet file as a separate chart in the terminal.
Especially useful for Docker environments where only terminal visualization works.
"""
import plotext as plt
import pandas as pd
import numpy as np
import os
from pathlib import Path
import traceback
from src.common import logger
from src.common.constants import TradingRule

def _determine_chart_type(series):
    """
    Determine the appropriate chart type for a data series.

    Args:
        series: pandas Series to analyze

    Returns:
        str: Chart type ('line', 'bar', 'scatter')
    """
    # Check if series is binary or has very few unique values (categorical-like)
    unique_values = series.nunique()

    if unique_values <= 3 and all(val in [-1, 0, 1, 2] for val in series.unique() if not pd.isna(val)):
        # For signal-like binary/categorical data
        return 'bar'
    elif unique_values <= 5:
        # For categorical data with few values
        return 'bar'
    elif series.name and any(term in str(series.name).lower() for term in ['volume', 'vol']):
        # Volume data typically looks better as bars
        return 'bar'
    else:
        # Default to line chart for most continuous data
        return 'line'

def _plot_series_in_terminal(series, x_data, x_labels, step, title=None):
    """
    Plot a single data series in the terminal with appropriate formatting.

    Args:
        series: pandas Series to plot
        x_data: list of x-axis values
        x_labels: list of x-axis labels
        step: step size for x-tick labels
        title: optional title override
    """
    if series.isna().all():
        return False  # Skip empty series

    plt.clear_data()
    chart_type = _determine_chart_type(series)

    # Determine color based on series name or content
    name_lower = str(series.name).lower() if series.name else ""

    # Color selection logic based on column name and content patterns
    if any(term in name_lower for term in ['price', 'close', 'high']):
        color = "cyan+"
    elif any(term in name_lower for term in ['low', 'min']):
        color = "blue+"
    elif any(term in name_lower for term in ['buy', 'long', 'up']):
        color = "green+"
    elif any(term in name_lower for term in ['sell', 'short', 'down']):
        color = "red+"
    elif any(term in name_lower for term in ['vol', 'amount']):
        color = "yellow+"
    elif any(term in name_lower for term in ['rsi', 'stoch']):
        color = "magenta+"
    elif any(term in name_lower for term in ['ma', 'ema', 'sma', 'average']):
        color = "blue+"
    elif any(term in name_lower for term in ['pressure', 'momentum']):
        color = "red+"
    elif any(term in name_lower for term in ['pprice', 'predict', 'forecast']):
        color = "lime+"
    elif any(term in name_lower for term in ['direction', 'signal']):
        color = "orange+"
    else:
        color = "white+"  # Default

    # Prepare title
    display_title = title if title else f"{series.name}"

    # Get data as list (handling NaN values)
    data = [float(v) if not pd.isna(v) else 0 for v in series.values]

    # Different plot types
    if chart_type == 'bar':
        # Check if data contains negative values
        if any(v < 0 for v in data):
            # For data with positive and negative values (like signals)
            plt.bar(x_data, data, label=str(series.name), color=color)
        else:
            # Standard bar chart
            plt.bar(x_data, data, label=str(series.name), color=color)
    elif chart_type == 'scatter':
        plt.scatter(x_data, data, label=str(series.name), color=color)
    else:  # Default to line chart
        plt.plot(x_data, data, label=str(series.name), color=color, marker="braille")

    # Add reference line at zero for data that crosses zero
    if min(data) < 0 and max(data) > 0:
        plt.plot(x_data, [0] * len(x_data), label="Zero", color="gray")

    # If it's a known oscillator like RSI, add reference lines
    if 'rsi' in name_lower:
        plt.plot(x_data, [70] * len(x_data), label="Overbought (70)", color="red")
        plt.plot(x_data, [30] * len(x_data), label="Oversold (30)", color="green")

    # Set chart titles and labels
    plt.title(display_title)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.xticks(x_data[::step], x_labels[::step])
    plt.show()

    return True

def auto_plot_from_parquet(parquet_path, plot_title=None):
    """
    Plot all columns in a parquet file as separate charts in the terminal.

    Args:
        parquet_path: Path to the parquet file
        plot_title: Optional title for the overall plot

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Load the parquet file
        df = pd.read_parquet(parquet_path)

        if df.empty:
            logger.print_warning(f"Empty dataframe loaded from {parquet_path}")
            return False

        # Get title from file name if not provided
        if not plot_title:
            file_name = os.path.basename(parquet_path)
            plot_title = f"Auto Terminal Plot: {file_name}"

        # Set theme
        plt.theme("dark")

        # Limit data points for better terminal display
        max_points = 80
        if len(df) > max_points:
            logger.print_info(f"Limiting dataframe from {len(df)} to {max_points} points for terminal display")
            df = df.tail(max_points).copy()

        # Prepare x-axis data
        x_data = list(range(len(df)))

        # Generate x-axis labels from index
        if isinstance(df.index, pd.DatetimeIndex):
            x_labels = [d.strftime('%m-%d') for d in df.index]
        else:
            x_labels = [f"T{i}" for i in x_data]

        # Set a reasonable tick step based on data length
        step = max(1, len(x_labels) // 8)

        # Print header
        print(f"\n{plot_title}")
        print("=" * 60)
        print(f"Displaying {len(df.columns)} columns from parquet file: {os.path.basename(parquet_path)}")
        print(f"Time range: {df.index[0]} to {df.index[-1]}" if isinstance(df.index, pd.DatetimeIndex) else f"Data points: {len(df)}")
        print("-" * 60)

        # Identify column categories
        ohlcv_cols = [col for col in df.columns if col in ['Open', 'High', 'Low', 'Close', 'Volume']]
        time_cols = [col for col in df.columns if col.lower() in ['date', 'time', 'datetime', 'timestamp']]

        # First plot OHLCV if available (standard price chart)
        if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
            plt.clear_data()
            plt.plot(x_data, df['Close'].tolist(), label="Close", color="cyan+", marker="braille")
            plt.plot(x_data, df['High'].tolist(), label="High", color="green+", marker="braille")
            plt.plot(x_data, df['Low'].tolist(), label="Low", color="red+", marker="braille")

            plt.title("Price Chart (OHLC)")
            plt.xlabel("Time")
            plt.ylabel("Price")
            plt.xticks(x_data[::step], x_labels[::step])
            print("\n📈 PRICE CHART")
            plt.show()

            # Plot volume separately if available
            if 'Volume' in df.columns and df['Volume'].sum() > 0:
                plt.clear_data()
                vol_data = df['Volume'].tolist()
                plt.bar(x_data, vol_data, label="Volume", color="blue+")
                plt.title("Volume")
                plt.xlabel("Time")
                plt.ylabel("Volume")
                plt.xticks(x_data[::step], x_labels[::step])
                print("\n📊 VOLUME")
                plt.show()

        # Now plot each non-OHLCV column separately
        special_cols = set(ohlcv_cols + time_cols)
        other_cols = [col for col in df.columns if col not in special_cols]

        if other_cols:
            print("\n📊 ADDITIONAL INDICATORS AND METRICS")
            logger.print_info(f"Plotting {len(other_cols)} additional columns: {other_cols}")

            plots_shown = 0
            # Ensure important prediction columns are plotted first and separately
            important_cols = ['predicted_high', 'predicted_low', 'pressure', 'pressure_vector']
            priority_cols = [col for col in important_cols if col in other_cols]
            remaining_cols = [col for col in other_cols if col not in important_cols]

            # First plot Close with predicted_high and predicted_low on a separate chart
            if 'predicted_high' in other_cols and 'predicted_low' in other_cols and 'Close' in df.columns:
                plt.clear_data()
                plt.plot(x_data, df['Close'].tolist(), label="Close", color="cyan+", marker="braille")
                plt.plot(x_data, df['predicted_high'].tolist(), label="Predicted High", color="green+", marker="braille")
                plt.plot(x_data, df['predicted_low'].tolist(), label="Predicted Low", color="red+", marker="braille")
                plt.title("Close with Predictions")
                plt.xlabel("Time")
                plt.ylabel("Price")
                plt.xticks(x_data[::step], x_labels[::step])
                print("\n📈 CLOSE WITH PREDICTIONS")
                plt.show()
                plots_shown += 1

                # We still want to plot each prediction separately too
                # Do not remove these from priority_cols as they need to be plotted individually as well

            # Now plot each priority column individually on its own chart
            for col in priority_cols:
                try:
                    plt.clear_data()
                    print(f"\n📈 Plotting {col.upper()}")
                    data = df[col].tolist()

                    # Determine color based on column name
                    name_lower = col.lower()
                    if 'high' in name_lower:
                        color = "green+"
                    elif 'low' in name_lower:
                        color = "red+"
                    elif 'pressure' in name_lower:
                        color = "magenta+"
                    elif 'vector' in name_lower:
                        color = "yellow+"
                    else:
                        color = "white+"  # Default color

                    chart_type = _determine_chart_type(df[col])
                    if chart_type == 'bar':
                        plt.bar(x_data, data, label=col, color=color)
                    else:
                        plt.plot(x_data, data, label=col, color=color, marker="braille")

                    # Add zero line for reference if data crosses zero
                    if min(data) < 0 and max(data) > 0:
                        plt.plot(x_data, [0] * len(x_data), label="Zero", color="gray")

                    plt.title(col)
                    plt.xlabel("Time")
                    plt.ylabel("Value")
                    plt.xticks(x_data[::step], x_labels[::step])
                    plt.show()
                    plots_shown += 1
                    logger.print_debug(f"Successfully plotted priority column: {col}")
                except Exception as e:
                    logger.print_warning(f"Error plotting priority column '{col}': {str(e)}")
                    logger.print_warning(f"Data sample for '{col}': {df[col].head(3).tolist()}")

            # Then plot remaining columns
            for col in remaining_cols:
                try:
                    if _plot_series_in_terminal(df[col], x_data, x_labels, step):
                        plots_shown += 1
                        logger.print_debug(f"Successfully plotted: {col}")
                except Exception as e:
                    logger.print_warning(f"Error plotting column '{col}': {str(e)}")

            print(f"\n✅ Displayed {plots_shown} additional charts")

        return True

    except Exception as e:
        logger.print_error(f"Error in auto terminal plotting: {str(e)}")
        traceback.print_exc()

        # Ultra-simple fallback
        try:
            plt.clear_data()
            plt.theme("dark")
            print("\n⚠️ Error occurred, showing simplified view")
            df = pd.read_parquet(parquet_path)
            if 'Close' in df.columns:
                if len(df) > max_points:
                    df = df.tail(max_points)
                close_data = df['Close'].tolist()
                plt.plot(range(len(close_data)), close_data, label="Close Price", color="cyan+")
                plt.title(f"Simplified Price Chart")
                plt.xlabel("Time Points")
                plt.ylabel("Price")
                plt.show()
                return True
        except Exception as fallback_e:
            logger.print_error(f"Even fallback plotting failed: {str(fallback_e)}")

        return False

def auto_plot_from_dataframe(df, plot_title=None):
    """
    Plot all columns in a DataFrame as separate charts in the terminal.
    This is a variant of auto_plot_from_parquet that works directly with DataFrame.

    Args:
        df: DataFrame with data to plot
        plot_title: Optional title for the overall plot

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if df is None or df.empty:
            logger.print_warning("Empty or None dataframe provided")
            return False

        # Print column names for debugging
        logger.print_debug(f"Columns in DataFrame: {df.columns.tolist()}")

        # Get default title if not provided
        if not plot_title:
            plot_title = "Auto Terminal Plot from DataFrame"

        # Set theme
        plt.theme("dark")

        # Limit data points for better terminal display
        max_points = 80
        if len(df) > max_points:
            logger.print_info(f"Limiting dataframe from {len(df)} to {max_points} points for terminal display")
            df = df.tail(max_points).copy()

        # Prepare x-axis data
        x_data = list(range(len(df)))

        # Generate x-axis labels from index
        if isinstance(df.index, pd.DatetimeIndex):
            x_labels = [d.strftime('%m-%d') for d in df.index]
        else:
            x_labels = [f"T{i}" for i in x_data]

        # Set a reasonable tick step based on data length
        step = max(1, len(x_labels) // 8)

        # Print header
        print(f"\n{plot_title}")
        print("=" * 60)
        print(f"Displaying {len(df.columns)} columns from DataFrame")
        print(f"Time range: {df.index[0]} to {df.index[-1]}" if isinstance(df.index, pd.DatetimeIndex) else f"Data points: {len(df)}")
        print("-" * 60)

        # Exclude standard OHLCV and time-like columns
        exclude_cols = {c.lower() for c in ['open', 'high', 'low', 'close', 'volume', 'timestamp', 'datetime', 'index', 'date', 'time']}
        plot_cols = [col for col in df.columns if col.lower() not in exclude_cols and pd.api.types.is_numeric_dtype(df[col])]

        if not plot_cols:
            logger.print_warning("No numeric columns to plot.")
            return False

        # Plot each numeric column separately
        for col in plot_cols:
            try:
                plt.clear_data()
                print(f"\n📈 Plotting {col.upper()}")
                data = df[col].tolist()

                # Determine color based on column name
                color = "white+"  # Default color
                chart_type = 'line'  # Default to line chart

                # Plot the data
                plt.plot(x_data, data, label=col, color=color, marker="braille")

                # Add zero line for reference if data crosses zero
                if min(data) < 0 and max(data) > 0:
                    plt.plot(x_data, [0] * len(x_data), label="Zero", color="gray")

                plt.title(col)
                plt.xlabel("Time")
                plt.ylabel("Value")
                plt.xticks(x_data[::step], x_labels[::step])
                plt.show()
            except Exception as e:
                logger.print_warning(f"Error plotting column '{col}': {str(e)}")

        return True

    except Exception as e:
        logger.print_error(f"Error in auto terminal plotting from DataFrame: {str(e)}")
        traceback.print_exc()
        return False

