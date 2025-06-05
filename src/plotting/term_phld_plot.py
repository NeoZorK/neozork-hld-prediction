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

    plt.bar(x_clean, buy_points, label="Buy Signal", color="bright_green")
    plt.bar(x_clean, [-val for val in sell_points], label="Sell Signal", color="bright_red")

    plt.title(f"Trading Signals {data_source}")
    plt.xlabel("Time")
    plt.ylabel("Signal")
    plt.xticks(x_data[::step], x_labels[::step])
    plt.show()

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
def get_data_source_label(column_name: str, calculated_columns: List[str] = None) -> str:
    """
    Determine if a column is calculated or loaded from file.

    Args:
        column_name: Name of the column to check
        calculated_columns: List of columns known to be calculated

    Returns:
        String label indicating data source
    """
    calculated_columns = calculated_columns or []

    # Check if column name contains any calculation indicator
    calculation_indicators = ["predicted", "calc", "diff", "pressure", "pv", "hl", "signal",
                             "direction", "pcolor", "pprice"]

    # Special case for OHLC columns
    if column_name.lower() in ["open", "high", "low", "close", "volume"]:
        return "📁 [LOADED FROM FILE]"

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

        # Determine if data is calculated or loaded from file for PHLD columns
        phld_price_source = "calculated" if calculated_df is not None else "pre-calculated"

        # Plot PHLD specific components with source indicator
        # Use the new function get_data_source_label to determine data source
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
        if calculated_df is not None:
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
