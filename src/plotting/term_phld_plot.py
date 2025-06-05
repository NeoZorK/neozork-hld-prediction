# -*- coding: utf-8 -*-
# src/plotting/term_phld_plot.py

"""
Terminal plotting module specifically for PHLD indicator.
Handles both existing indicators in parquet files and newly calculated ones.
Displays indicators according to trading rule: OHLCV, AUTO, or PHLD.
"""

import plotext as plt
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Optional, Union, Any
from src.common import logger
from src.common.constants import TradingRule

def clean_data_for_plotting(df: pd.DataFrame, column_name: str, x_data: list) -> Tuple[list, list, int]:
    """
    Clean data by removing NaN and infinite values for safe terminal plotting.

    Args:
        df: DataFrame containing the data
        column_name: Name of the column to clean
        x_data: X-axis data corresponding to the column

    Returns:
        tuple: (cleaned_x_data, cleaned_y_data, num_removed)
    """
    series = df[column_name]

    # Create mask for finite values (not NaN, not inf, not -inf)
    finite_mask = np.isfinite(series)

    # Count how many values were removed
    num_removed = len(series) - finite_mask.sum()

    if not finite_mask.any():
        return [], [], num_removed

    # Filter both x and y data using the finite mask
    x_data_cleaned = [x_data[i] for i in range(len(x_data)) if finite_mask.iloc[i]]
    y_data_cleaned = series[finite_mask].tolist()

    return x_data_cleaned, y_data_cleaned, num_removed

def setup_terminal_chart() -> None:
    """
    Apply consistent styling to terminal charts for better visibility.
    """
    plt.clear_data()
    plt.canvas_color("black")
    plt.axes_color("black")
    plt.ticks_color("yellow")

def detect_phld_columns(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Detect and categorize PHLD-related columns in the DataFrame.

    Args:
        df: DataFrame to analyze

    Returns:
        Dictionary with categorized columns
    """
    column_groups = {
        'ohlc': [col for col in df.columns if col.lower() in ['open', 'high', 'low', 'close']],
        'volume': [col for col in df.columns if col.lower() == 'volume'],
        'price_pred': [col for col in df.columns if col.lower() in ['pprice1', 'pprice2', 'predicted_high', 'predicted_low']],
        'signals': [col for col in df.columns if col.lower() in ['direction', 'signal', 'buy_signal', 'sell_signal']],
        'colors': [col for col in df.columns if col.lower() in ['pcolor1', 'pcolor2']],
        'metrics': [col for col in df.columns if col.lower() in ['diff', 'hl', 'pressure', 'pv', 'pressure_vector']],
        'other': []
    }

    # Find columns that don't fit in any specific category
    all_categorized = []
    for category, cols in column_groups.items():
        if category != 'other':
            all_categorized.extend(cols)

    column_groups['other'] = [col for col in df.columns if col not in all_categorized]

    return column_groups

def plot_ohlc_chart(df: pd.DataFrame, x_data: list, x_labels: list, step: int) -> None:
    """
    Plot OHLC chart with specified styling.

    Args:
        df: DataFrame with financial data
        x_data: list of x positions
        x_labels: list of x-axis labels
        step: step size for x-ticks
    """
    setup_terminal_chart()
    # Add data source label
    data_source = get_data_source_label("OHLC")
    print(f"\n📈 PRICE CHART {data_source}")

    # Use consistent color mapping
    if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
        plt.plot(x_data, df['Open'].tolist(), label="Open", color="bright_magenta")
        plt.plot(x_data, df['High'].tolist(), label="High", color="bright_cyan")
        plt.plot(x_data, df['Low'].tolist(), label="Low", color="bright_red")
        plt.plot(x_data, df['Close'].tolist(), label="Close", color="bright_blue")
    else:
        # Fallback to Close price if available
        if 'Close' in df.columns:
            plt.plot(x_data, df['Close'].tolist(), label="Close", color="bright_blue")
        else:
            print("⚠️ No price data available")
            return

    plt.title(f"Price Movement {data_source}")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.xticks(x_data[::step], x_labels[::step])
    plt.show()

def plot_volume_chart(df: pd.DataFrame, x_data: list, x_labels: list, step: int) -> None:
    """
    Plot volume chart if volume data is available.

    Args:
        df: DataFrame with financial data
        x_data: list of x positions
        x_labels: list of x-axis labels
        step: step size for x-ticks
    """
    if 'Volume' not in df.columns or df['Volume'].sum() == 0:
        return

    setup_terminal_chart()
    # Add data source label
    data_source = get_data_source_label("Volume")
    print(f"\n📊 VOLUME CHART {data_source}")

    x_clean, y_clean, num_removed = clean_data_for_plotting(df, 'Volume', x_data)

    if len(y_clean) == 0:
        print("⚠️ No valid volume data available")
        return

    plt.bar(x_clean, y_clean, label="Volume", color="bright_magenta")
    plt.title(f"Volume {data_source}")
    plt.xlabel("Time")
    plt.ylabel("Volume")
    plt.xticks(x_data[::step], x_labels[::step])
    plt.show()

def plot_price_predictions(df: pd.DataFrame, columns: List[str], x_data: list, x_labels: list, step: int) -> None:
    """
    Plot predicted price levels with Close price for reference.

    Args:
        df: DataFrame with financial data
        columns: List of prediction columns to plot
        x_data: list of x positions
        x_labels: list of x-axis labels
        step: step size for x-ticks
    """
    if not columns:
        return

    setup_terminal_chart()

    # Get source label for predicted prices
    data_source = get_data_source_label(columns[0] if columns else "pprice")
    print(f"\n🎯 PREDICTED PRICES {data_source}")

    # First plot Close price for reference
    if 'Close' in df.columns:
        x_clean, y_clean, _ = clean_data_for_plotting(df, 'Close', x_data)
        if len(y_clean) > 0:
            plt.plot(x_clean, y_clean, label="Close Price", color="bright_blue")

    # Plot predicted price levels
    colors = ['bright_green', 'bright_red', 'bright_yellow', 'bright_magenta']
    for i, col in enumerate(columns):
        color = colors[i % len(colors)]
        x_clean, y_clean, num_removed = clean_data_for_plotting(df, col, x_data)

        if len(y_clean) == 0:
            print(f"⚠️ Skipping price column '{col}' - no valid data")
            continue

        plt.plot(x_clean, y_clean, label=col, color=color)

    plt.title(f"Predicted Prices {data_source}")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.xticks(x_data[::step], x_labels[::step])
    plt.show()

def plot_direction_signals(df: pd.DataFrame, x_data: list, x_labels: list, step: int) -> None:
    """
    Plot direction signals as buy/sell bars.

    Args:
        df: DataFrame with financial data
        x_data: list of x positions
        x_labels: list of x-axis labels
        step: step size for x-ticks
    """
    if 'Direction' not in df.columns or df['Direction'].isna().all():
        return

    setup_terminal_chart()
    # Get source label for direction signals
    data_source = get_data_source_label("Direction")
    print(f"\n🚦 TRADING SIGNALS {data_source}")

    x_clean, direction_data, _ = clean_data_for_plotting(df, 'Direction', x_data)

    if len(direction_data) == 0:
        print("⚠️ No valid direction data available")
        return

    # Direction: 1=Buy, -1/2=Sell, 0=Hold
    buy_points = [1 if val == 1 else 0 for val in direction_data]
    sell_points = [1 if val in [-1, 2] else 0 for val in direction_data]

    # Use more readable characters for signals instead of solid blocks
    # Character options: ▲▼△▽◆◇●○☀☂★☆♠♥♦♣
    plt.theme("clear")
    plt.canvas_color("black")
    plt.axes_color("black")
    plt.ticks_color("yellow")

    # Use line style with markers for better visibility
    # Create x-positions for buy signals (only where buy_points is 1)
    buy_x = [x_clean[i] for i in range(len(x_clean)) if buy_points[i] == 1]
    buy_y = [1] * len(buy_x)

    # Create x-positions for sell signals (only where sell_points is 1)
    sell_x = [x_clean[i] for i in range(len(x_clean)) if sell_points[i] == 1]
    sell_y = [-1] * len(sell_x)

    # Plot Buy/Sell signals as points with custom markers for better visibility
    if buy_x:
        plt.scatter(buy_x, buy_y, marker="triangle", color="bright_green", point_size=2)
        plt.text(x=buy_x[0], y=1.1, s="▲ Buy Signals", color="bright_green")

    if sell_x:
        plt.scatter(sell_x, sell_y, marker="triangle", color="bright_red", point_size=2)
        plt.text(x=sell_x[0] if sell_x else x_clean[0], y=-1.1, s="▼ Sell Signals", color="bright_red")

    # Add a zero line for reference
    plt.plot(x_clean, [0] * len(x_clean), label="Neutral", color="gray", line_color="gray")

    # Set custom y-ticks for clarity
    plt.yticks([-1, 0, 1], ["Sell", "Hold", "Buy"])

    plt.title(f"Trading Signals {data_source}")
    plt.xlabel("Time")
    plt.ylabel("Signal")
    plt.xticks(x_data[::step], x_labels[::step])
    plt.show()

    # Show signal summary (optional but helpful)
    buy_count = sum(buy_points)
    sell_count = sum(sell_points)
    hold_count = len(direction_data) - buy_count - sell_count

    print(f"Signal Summary: {buy_count} Buy signals, {sell_count} Sell signals, {hold_count} Hold signals")

def plot_additional_indicators(df: pd.DataFrame, columns: List[str], x_data: list, x_labels: list, step: int, title: str) -> None:
    """
    Plot additional indicator columns.

    Args:
        df: DataFrame with financial data
        columns: List of indicator columns to plot
        x_data: list of x positions
        x_labels: list of x-axis labels
        step: step size for x-ticks
        title: Chart title
    """
    if not columns:
        return

    setup_terminal_chart()
    print(f"\n📊 {title}")

    colors = ['bright_yellow', 'bright_cyan', 'bright_magenta', 'bright_white']
    for i, col in enumerate(columns):
        color = colors[i % len(colors)]
        x_clean, y_clean, num_removed = clean_data_for_plotting(df, col, x_data)

        if len(y_clean) == 0:
            print(f"⚠️ Skipping column '{col}' - no valid data")
            continue

        # Add zero reference line for metrics that can be positive/negative
        if col.lower() in ['hl', 'pressure', 'pv', 'pressure_vector', 'diff']:
            plt.plot(x_clean, [0] * len(x_clean), label="Zero Line", color="gray")

        plt.plot(x_clean, y_clean, label=col, color=color, marker="braille")

    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.xticks(x_data[::step], x_labels[::step])
    plt.show()

def print_summary(df: pd.DataFrame, rule: Union[TradingRule, str], column_groups: Dict[str, List[str]]) -> None:
    """
    Print summary information about the data and detected columns.

    Args:
        df: DataFrame with financial data
        rule: Trading rule applied
        column_groups: Dictionary with categorized columns
    """
    print("\n📋 DATA SUMMARY")
    print("-" * 30)
    print(f"Data points: {len(df)}")
    rule_name = rule.name if hasattr(rule, 'name') else str(rule)
    print(f"Rule applied: {rule_name}")

    if 'Close' in df.columns:
        close_prices = df['Close']
        print(f"Price range: ${close_prices.min():.2f} - ${close_prices.max():.2f}")

    # Count Buy/Sell signals if Direction column exists
    if 'Direction' in df.columns and not df['Direction'].isna().all():
        buy_signals = (df['Direction'] == 1).sum()
        sell_signals = ((df['Direction'] == -1) | (df['Direction'] == 2)).sum()
        print(f"Buy signals: {buy_signals}, Sell signals: {sell_signals}")

    # Print detected column groups
    for group, cols in column_groups.items():
        if cols:
            print(f"{group.capitalize()} columns: {', '.join(cols)}")

def compare_indicators(df: pd.DataFrame, calculated_df: Optional[pd.DataFrame] = None) -> None:
    """
    Compare indicators from the file with newly calculated ones if both are available.

    Args:
        df: DataFrame with indicators from file
        calculated_df: DataFrame with newly calculated indicators
    """
    if calculated_df is None:
        return

    # Find common indicator columns
    common_indicators = [col for col in df.columns if col in calculated_df.columns and
                        col.lower() not in ['open', 'high', 'low', 'close', 'volume'] and
                        not df[col].isna().all() and not calculated_df[col].isna().all()]

    if not common_indicators:
        return

    print("\n🔄 INDICATOR COMPARISON")
    print("-" * 30)
    print(f"Comparing {len(common_indicators)} common indicators from file vs. calculated")

    for col in common_indicators:
        if pd.api.types.is_numeric_dtype(df[col]) and pd.api.types.is_numeric_dtype(calculated_df[col]):
            diff = df[col] - calculated_df[col]
            mae = abs(diff).mean()
            max_diff = abs(diff).max()
            print(f"{col}: MAE = {mae:.6f}, Max Diff = {max_diff:.6f}")
        else:
            match_pct = (df[col] == calculated_df[col]).mean() * 100
            print(f"{col}: {match_pct:.2f}% match")

# Helper function to determine data source label
def get_data_source_label(column_name: str, calculated_columns: List[str] = None, force_loaded: bool = False) -> str:
    """
    Determine if a column is calculated or loaded from file.

    Args:
        column_name: Name of the column to check
        calculated_columns: List of columns known to be calculated
        force_loaded: Force the label to show as loaded from file regardless of name

    Returns:
        String label indicating data source
    """
    calculated_columns = calculated_columns or []

    # If force_loaded is True, always return "LOADED FROM FILE"
    if force_loaded:
        return "📁 [LOADED FROM FILE]"

    # Special case for OHLC columns
    if column_name.lower() in ["open", "high", "low", "close", "volume"]:
        return "📁 [LOADED FROM FILE]"

    # Check if column name contains any calculation indicator
    calculation_indicators = ["predicted", "calc", "diff", "pressure", "pv", "hl", "signal",
                             "direction", "pcolor", "pprice"]

    # Check if column is in calculated list or has a name pattern indicating calculation
    is_calculated = any(indicator in column_name.lower() for indicator in calculation_indicators)
    is_calculated = is_calculated or column_name in calculated_columns

    if is_calculated:
        return "🧮 [CALCULATED NOW]"
    else:
        return "📁 [LOADED FROM FILE]"

def plot_phld_term(df: pd.DataFrame, rule: Union[TradingRule, str], title: str,
                  calculated_df: Optional[pd.DataFrame] = None) -> None:
    """
    Main function to plot PHLD indicator data in terminal.
    Handles different trading rules (OHLCV, AUTO, PHLD) and displays appropriate charts.

    Args:
        df: DataFrame with financial data
        rule: Trading rule to apply (OHLCV, AUTO, PHLD)
        title: Title for the overall plot
        calculated_df: Optional DataFrame with newly calculated indicators for comparison
    """
    if df is None or df.empty:
        print("No data to plot.")
        return

    # Limit data points for terminal display (last 80 points for better visibility)
    max_points = 80
    if len(df) > max_points:
        df = df.tail(max_points).copy()
        if calculated_df is not None:
            calculated_df = calculated_df.tail(max_points).copy()

    # Prepare x-axis data
    x_data = list(range(len(df)))

    # Generate x-axis labels from index
    if isinstance(df.index, pd.DatetimeIndex):
        x_labels = [d.strftime('%m-%d') for d in df.index]
    else:
        x_labels = [f"T{i}" for i in x_data]

    # Set readable x-axis labels
    step = max(1, len(x_labels) // 8)

    print(f"\n{title}")
    print("=" * 60)

    # Add clear data source indicator to title
    data_source = "📊 DATA SOURCE: LOADED FROM FILE" if calculated_df is None else "📊 SHOWING BOTH: LOADED FROM FILE AND CALCULATED NOW"
    print(f"{data_source}")

    # Detect columns for different components of PHLD
    column_groups = detect_phld_columns(df)

    # Check if the DataFrame already has PHLD indicator columns
    existing_phld_indicators = []
    for col in df.columns:
        col_lower = col.lower()
        if any(ind in col_lower for ind in ['predicted_high', 'predicted_low', 'hl', 'pressure_vector', 'pressure', 'pprice', 'pcolor', 'direction']):
            existing_phld_indicators.append(col)

    has_existing_indicators = len(existing_phld_indicators) > 0
    if has_existing_indicators:
        print(f"Found existing PHLD indicators in file: {', '.join(existing_phld_indicators)}")

    # Get rule name in string format
    rule_str = rule.name if hasattr(rule, 'name') else str(rule)
    rule_upper = rule_str.upper()

    # OHLCV Rule - Only show OHLC and Volume
    if rule_upper == 'OHLCV':
        print("Displaying only OHLCV data (no indicators)")
        plot_ohlc_chart(df, x_data, x_labels, step)
        plot_volume_chart(df, x_data, x_labels, step)

    # AUTO Rule - Show all available columns except OHLCV
    elif rule_upper == 'AUTO' or rule_upper == 'AUTO_DISPLAY_ALL':
        print("AUTO display mode - showing all available columns")
        # Plot basic charts
        plot_ohlc_chart(df, x_data, x_labels, step)
        plot_volume_chart(df, x_data, x_labels, step)

        # Plot all non-OHLCV columns
        for group, cols in column_groups.items():
            if group not in ['ohlc', 'volume'] and cols:
                # Use the new function with source indicator
                from src.plotting.plotting_generation import plot_additional_indicators_with_source
                plot_additional_indicators_with_source(
                    df, cols, x_data, x_labels, step,
                    f"{group.upper()} INDICATORS",
                    "pre-calculated"
                )

        # Если у нас есть колонки, которые не попали ни в одну категорию, отобразим их тоже
        if column_groups['other']:
            from src.plotting.plotting_generation import plot_additional_indicators_with_source
            plot_additional_indicators_with_source(
                df, column_groups['other'], x_data, x_labels, step,
                "OTHER INDICATORS",
                "pre-calculated"
            )

    # PHLD Rule - Show OHLCV + all PHLD components
    elif rule_upper == 'PHLD' or rule_upper == 'PREDICT_HIGH_LOW_DIRECTION':
        print("PHLD indicator display mode")
        # Plot basic charts
        plot_ohlc_chart(df, x_data, x_labels, step)
        plot_volume_chart(df, x_data, x_labels, step)

        # First, display all existing indicators from the file if they exist
        if has_existing_indicators:
            print("\n📊 EXISTING PHLD INDICATORS FROM FILE")
            print("-" * 50)

            # Group existing indicators by type for better visualization
            existing_groups = {
                'price_pred': [col for col in existing_phld_indicators if any(x in col.lower() for x in ['predicted_high', 'predicted_low', 'pprice'])],
                'direction': [col for col in existing_phld_indicators if 'direction' in col.lower()],
                'colors': [col for col in existing_phld_indicators if 'pcolor' in col.lower()],
                'metrics': [col for col in existing_phld_indicators if any(x in col.lower() for x in ['hl', 'pressure', 'pv', 'diff'])]
            }

            # Display existing price prediction indicators
            if existing_groups['price_pred']:
                # Get source label for existing predicted prices, force "LOADED FROM FILE"
                for col in existing_groups['price_pred']:
                    data_source = get_data_source_label(col, force_loaded=True)
                    print(f"\n🎯 EXISTING PREDICTED PRICES {data_source}")

                # Create temporary function to plot price predictions with correct label
                def plot_loaded_price_predictions(df, columns, x_data, x_labels, step):
                    if not columns:
                        return

                    setup_terminal_chart()
                    # Force LOADED FROM FILE label
                    data_source = "📁 [LOADED FROM FILE]"
                    print(f"\n🎯 PREDICTED PRICES {data_source}")

                    # First plot Close price for reference
                    if 'Close' in df.columns:
                        x_clean, y_clean, _ = clean_data_for_plotting(df, 'Close', x_data)
                        if len(y_clean) > 0:
                            plt.plot(x_clean, y_clean, label="Close Price", color="bright_blue")

                    # Plot predicted price levels
                    colors = ['bright_green', 'bright_red', 'bright_yellow', 'bright_magenta']
                    for i, col in enumerate(columns):
                        color = colors[i % len(colors)]
                        x_clean, y_clean, num_removed = clean_data_for_plotting(df, col, x_data)

                        if len(y_clean) == 0:
                            print(f"⚠️ Skipping price column '{col}' - no valid data")
                            continue

                        plt.plot(x_clean, y_clean, label=col, color=color)

                    plt.title(f"Predicted Prices {data_source}")
                    plt.xlabel("Time")
                    plt.ylabel("Price")
                    plt.xticks(x_data[::step], x_labels[::step])
                    plt.show()

                # Use our modified function instead of the standard one
                plot_loaded_price_predictions(df, existing_groups['price_pred'], x_data, x_labels, step)

            # Display existing direction indicators
            if existing_groups['direction']:
                # Get source label for existing direction, force "LOADED FROM FILE"
                for col in existing_groups['direction']:
                    data_source = get_data_source_label(col, force_loaded=True)
                    print(f"\n🚦 EXISTING DIRECTION {data_source}")

                # Create temporary function to plot direction signals with correct label
                def plot_loaded_direction_signals(df, x_data, x_labels, step):
                    if 'Direction' not in df.columns or df['Direction'].isna().all():
                        return

                    setup_terminal_chart()
                    # Force LOADED FROM FILE label
                    data_source = "📁 [LOADED FROM FILE]"
                    print(f"\n🚦 TRADING SIGNALS {data_source}")

                    x_clean, direction_data, _ = clean_data_for_plotting(df, 'Direction', x_data)

                    if len(direction_data) == 0:
                        print("⚠️ No valid direction data available")
                        return

                    # Direction: 1=Buy, -1/2=Sell, 0=Hold
                    buy_points = [1 if val == 1 else 0 for val in direction_data]
                    sell_points = [1 if val in [-1, 2] else 0 for val in direction_data]

                    # Use more readable characters for signals instead of solid blocks
                    plt.theme("clear")
                    plt.canvas_color("black")
                    plt.axes_color("black")
                    plt.ticks_color("yellow")

                    # Use line style with markers for better visibility
                    # Create x-positions for buy signals (only where buy_points is 1)
                    buy_x = [x_clean[i] for i in range(len(x_clean)) if buy_points[i] == 1]
                    buy_y = [1] * len(buy_x)

                    # Create x-positions for sell signals (only where sell_points is 1)
                    sell_x = [x_clean[i] for i in range(len(x_clean)) if sell_points[i] == 1]
                    sell_y = [-1] * len(sell_x)

                    # Plot Buy/Sell signals as points with custom markers for better visibility
                    if buy_x:
                        plt.scatter(buy_x, buy_y, marker="triangle", color="bright_green", point_size=2)
                        plt.text(x=buy_x[0], y=1.1, s="▲ Buy Signals", color="bright_green")

                    if sell_x:
                        plt.scatter(sell_x, sell_y, marker="triangle", color="bright_red", point_size=2)
                        plt.text(x=sell_x[0] if sell_x else x_clean[0], y=-1.1, s="▼ Sell Signals", color="bright_red")

                    # Add a zero line for reference
                    plt.plot(x_clean, [0] * len(x_clean), label="Neutral", color="gray", line_color="gray")

                    # Set custom y-ticks for clarity
                    plt.yticks([-1, 0, 1], ["Sell", "Hold", "Buy"])

                    plt.title(f"Trading Signals {data_source}")
                    plt.xlabel("Time")
                    plt.ylabel("Signal")
                    plt.xticks(x_data[::step], x_labels[::step])
                    plt.show()

                    # Show signal summary
                    buy_count = sum(buy_points)
                    sell_count = sum(sell_points)
                    hold_count = len(direction_data) - buy_count - sell_count

                    print(f"Signal Summary: {buy_count} Buy signals, {sell_count} Sell signals, {hold_count} Hold signals")

                # Use our modified function instead of the standard one
                plot_loaded_direction_signals(df, x_data, x_labels, step)

            # Display existing color indicators
            if existing_groups['colors']:
                from src.plotting.plotting_generation import plot_additional_indicators_with_source
                plot_additional_indicators_with_source(
                    df, existing_groups['colors'], x_data, x_labels, step,
                    "EXISTING COLOR INDICATORS",
                    "pre-calculated"
                )

            # Display existing metric indicators
            if existing_groups['metrics']:
                from src.plotting.plotting_generation import plot_additional_indicators_with_source
                plot_additional_indicators_with_source(
                    df, existing_groups['metrics'], x_data, x_labels, step,
                    "EXISTING METRIC INDICATORS",
                    "pre-calculated"
                )

        # Determine if data is calculated or loaded from file for PHLD columns
        phld_price_source = "calculated" if calculated_df is not None else "pre-calculated"

        # Now show newly calculated indicators if available
        if calculated_df is not None:
            print("\n🧮 NEWLY CALCULATED PHLD INDICATORS")
            print("-" * 50)

            # Plot PHLD specific components with source indicator
            # Use the new function get_data_source_label to determine data source
            if 'PPrice1' in calculated_df.columns or 'PPrice2' in calculated_df.columns:
                price_pred_cols = [col for col in calculated_df.columns if col in ['PPrice1', 'PPrice2']]
                if price_pred_cols:
                    price_pred_source = get_data_source_label(price_pred_cols[0])
                    print(f"\n🎯 CALCULATED PREDICTED PRICES {price_pred_source}")
                    plot_price_predictions(calculated_df, price_pred_cols, x_data, x_labels, step)

            if 'Direction' in calculated_df.columns:
                direction_source = get_data_source_label("Direction")
                print(f"\n🚦 CALCULATED TRADING SIGNALS {direction_source}")
                plot_direction_signals(calculated_df, x_data, x_labels, step)

            # Plot color indicators with source indicator
            color_cols = [col for col in calculated_df.columns if 'PColor' in col]
            if color_cols:
                from src.plotting.plotting_generation import plot_additional_indicators_with_source
                plot_additional_indicators_with_source(
                    calculated_df, color_cols, x_data, x_labels, step,
                    "CALCULATED COLOR INDICATORS",
                    "calculated"
                )

            # Plot metrics with source indicator
            metric_cols = [col for col in calculated_df.columns if col in ['HL', 'Pressure', 'PV', 'Diff']]
            if metric_cols:
                from src.plotting.plotting_generation import plot_additional_indicators_with_source
                plot_additional_indicators_with_source(
                    calculated_df, metric_cols, x_data, x_labels, step,
                    "CALCULATED PHLD METRICS",
                    "calculated"
                )
        else:
            # No calculated data - just show file data grouped properly with indicators
            if column_groups['price_pred']:
                price_pred_source = get_data_source_label(column_groups['price_pred'][0] if column_groups['price_pred'] else "pprice")
                print(f"\n🎯 PREDICTED PRICES {price_pred_source}")
                plot_price_predictions(df, column_groups['price_pred'], x_data, x_labels, step)

            if 'Direction' in df.columns:
                direction_source = get_data_source_label("Direction")
                print(f"\n🚦 TRADING SIGNALS {direction_source}")
                plot_direction_signals(df, x_data, x_labels, step)

            # Plot color indicators with source indicator
            if column_groups['colors']:
                from src.plotting.plotting_generation import plot_additional_indicators_with_source
                plot_additional_indicators_with_source(
                    df, column_groups['colors'], x_data, x_labels, step,
                    "PHLD COLOR INDICATORS",
                    phld_price_source
                )

            # Plot metrics with source indicator
            if column_groups['metrics']:
                from src.plotting.plotting_generation import plot_additional_indicators_with_source
                plot_additional_indicators_with_source(
                    df, column_groups['metrics'], x_data, x_labels, step,
                    "PHLD METRICS",
                    phld_price_source
                )

        # Compare indicators if both original and calculated are available
        if calculated_df is not None and has_existing_indicators:
            compare_indicators(df, calculated_df)

    # Print summary for all modes
    print_summary(df, rule, column_groups)

# Main export function that will be used by other modules
def plot_phld_indicator_terminal(df: pd.DataFrame,
                                rule: Union[TradingRule, str],
                                title: str = "PHLD Indicator",
                                calculated_df: Optional[pd.DataFrame] = None) -> None:
    """
    Public function to plot PHLD indicator in terminal mode.

    Args:
        df: DataFrame with PHLD indicator data (from parquet file)
        rule: Trading rule to apply (OHLCV, AUTO, PHLD)
        title: Title for the overall plot
        calculated_df: Optional DataFrame with newly calculated indicators for comparison
    """
    try:
        plot_phld_term(df, rule, title, calculated_df)
        logger.print_info(f"Terminal plot completed successfully with {len(df)} data points")
    except Exception as e:
        logger.print_error(f"Error in terminal plotting: {str(e)}")
        # Ultra-simple fallback
        try:
            plt.clear_data()
            plt.canvas_color('black')
            plt.axes_color('black')
            plt.ticks_color('yellow')
            if 'Close' in df.columns:
                close_data = df['Close'].tolist()
                plt.plot(range(len(close_data)), close_data, label="Close Price", color="bright_blue")
                plt.title(f"{title} - Price Chart")
                plt.xlabel("Time Points")
                plt.ylabel("Price")
                plt.show()
                print(f"\n✅ Simple price chart displayed ({len(close_data)} points)")
            else:
                print(f"❌ Terminal plotting failed: {str(e)}")
        except Exception as fallback_e:
            logger.print_error(f"Even fallback plotting failed: {str(fallback_e)}")
            print(f"❌ Terminal plotting unavailable. Error: {str(e)}")
