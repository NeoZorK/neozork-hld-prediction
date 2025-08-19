# -*- coding: utf-8 -*-
# src/plotting/fixed_term_sr_plot.py

"""
Fixed version of SR (Support/Resistance) terminal plotting functions.
Completely rewritten to avoid DataFrame ambiguity issues.
"""

import pandas as pd
import numpy as np
import plotext as plt
from typing import Optional, Union, List, Dict, Any

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from src.common.constants import TradingRule
except ImportError:
    # Fallback to relative imports when run as module
    from src.common import logger
    from src.common.constants import TradingRule


def safe_plot_sr_terminal(df: pd.DataFrame,
                         rule: Union[TradingRule, str],
                         title: str = "SR Terminal Plot",
                         output_path: Optional[str] = None) -> None:
    """
    Simplified and safe SR (Support/Resistance) terminal plot function that avoids DataFrame ambiguity.

    Args:
        df (pd.DataFrame): DataFrame with SR calculation results
        rule (Union[TradingRule, str]): Trading rule
        title (str): Plot title
        output_path (Optional[str]): Ignored for terminal plots
    """
    try:
        # Basic validation
        if df is None:
            logger.print_error("DataFrame is None, cannot plot")
            return

        if len(df) == 0:
            logger.print_error("DataFrame is empty, cannot plot")
            return

        # Prepare all data as plain Python lists to avoid any DataFrame ambiguity
        ohlc_data = {}
        has_ohlc = True
        has_volume = False

        # Create plain data with safe conversion - ensure all values are scalar
        for col in ['Open', 'High', 'Low', 'Close']:
            if col not in df.columns:
                has_ohlc = False
                break
            # Ensure we have scalar values, not nested lists
            values = df[col].fillna(0).to_numpy().tolist()
            # Flatten any nested lists
            flat_values = []
            for v in values:
                if isinstance(v, (list, tuple)):
                    flat_values.append(v[0] if v else 0.0)
                else:
                    flat_values.append(float(v))
            ohlc_data[col] = flat_values

        # Check volume explicitly
        if 'Volume' in df.columns:
            # Convert volume data safely
            volume_values = df['Volume'].fillna(0).to_numpy()
            has_volume = np.any(volume_values > 0)  # Safe numpy check

            # Ensure scalar values for volume
            volume_data = []
            for v in volume_values.tolist():
                if isinstance(v, (list, tuple)):
                    volume_data.append(int(v[0]) if v else 0)
                else:
                    volume_data.append(int(v))
        else:
            volume_data = []

        # Set up plot
        plt.clear_data()
        plt.clear_figure()

        # Identify SR-related columns
        sr_columns = []
        for col in df.columns:
            col_lower = col.lower()
            if 'support' in col_lower or 'resistance' in col_lower or 'sr_' in col_lower or 'sr' == col_lower:
                sr_columns.append(col)

        # Configure layout based on what data we have
        has_sr = len(sr_columns) > 0

        if has_ohlc and has_sr and has_volume:
            plt.subplots(2, 1)  # Price with SR + Volume
            main_plot_size = (140, 50)
        else:
            plt.subplots(1, 1)
            main_plot_size = (140, 40)  # Taller for SR visualization

        plt.plot_size(*main_plot_size)
        plt.theme('matrix')

        # Time axis as simple list
        x_values = list(range(len(df)))

        # Get rule name safely
        # Check if we have original rule with parameters for display
        if hasattr(rule, 'original_rule_with_params'):
            rule_str = rule.original_rule_with_params
        elif hasattr(rule, 'name'):
            rule_str = rule.name
        else:
            rule_str = str(rule)

        # Main price panel with SR zones
        if has_ohlc:
            plt.subplot(1, 1)

            # Plot candlesticks with plain data
            plt.candlestick(x_values, ohlc_data)
            plt.title(title)
            plt.ylabel("Price")

            # Plot SR levels as horizontal lines
            sr_colors = {
                'support': 'green+',
                'resistance': 'red+',
                'sr': 'yellow+'
            }

            # Track SR level colors for legend
            sr_colors_used = set()

            # Plot each SR column
            for col in sr_columns:
                try:
                    # Convert to plain list and ensure all values are scalar
                    raw_values = df[col].fillna(0).to_numpy().tolist()
                    values = []

                    # Flatten any nested lists
                    for v in raw_values:
                        if isinstance(v, (list, tuple)):
                            values.append(v[0] if v else 0.0)
                        else:
                            values.append(float(v))

                    # Find non-zero values (actual SR levels)
                    sr_levels = {}
                    for i, val in enumerate(values):
                        if abs(val) > 1e-6:  # Non-zero SR level
                            sr_levels[val] = sr_levels.get(val, 0) + 1

                    # Choose color based on column name
                    col_lower = col.lower()
                    color = None

                    for key, clr in sr_colors.items():
                        if key in col_lower:
                            color = clr
                            sr_colors_used.add(key)
                            break

                    if color is None:
                        color = 'white'  # Default color

                    # Draw horizontal lines for SR levels
                    for level, count in sr_levels.items():
                        # Horizontal line thickness based on strength (count)
                        thickness = min(5, max(1, count // 3 + 1))

                        # Draw SR level as horizontal line across the entire chart
                        plt.hline(y=level, color=color, label=f"{col}: {level:.5f}")
                except Exception as e:
                    logger.print_warning(f"Could not plot SR indicator {col}: {e}")

            # Plot additional indicators
            for col in df.columns:
                if col in ['Open', 'High', 'Low', 'Close', 'Volume'] or col in sr_columns:
                    continue

                try:
                    # Convert to plain list and ensure all values are scalar
                    raw_values = df[col].fillna(0).to_numpy().tolist()
                    values = []

                    # Flatten any nested lists
                    for v in raw_values:
                        if isinstance(v, (list, tuple)):
                            values.append(v[0] if v else 0.0)
                        else:
                            values.append(float(v))

                    # Skip empty indicators
                    if not any(abs(v) > 1e-10 for v in values):
                        continue

                    # Determine indicator type from name
                    col_lower = col.lower()

                    # Choose colors based on indicator type
                    if 'signal' in col_lower or 'direction' in col_lower:
                        # Handle signals with explicit values
                        buy_points_x = []
                        buy_points_y = []
                        sell_points_x = []
                        sell_points_y = []

                        # Extract points with scalar comparison
                        for i, val in enumerate(values):
                            # Safe comparison with tolerance (values are already flattened)
                            if abs(val - 1.0) < 0.0001:  # Buy signal
                                buy_points_x.append(x_values[i])
                                buy_points_y.append(ohlc_data['Low'][i] * 0.995)
                            elif abs(val - (-1.0)) < 0.0001:  # Sell signal
                                sell_points_x.append(x_values[i])
                                sell_points_y.append(ohlc_data['High'][i] * 1.005)

                        # Plot signals
                        if buy_points_x:
                            plt.scatter(buy_points_x, buy_points_y, color="green+", label=f"{col} Buy", marker="^")
                        if sell_points_x:
                            plt.scatter(sell_points_x, sell_points_y, color="red+", label=f"{col} Sell", marker="v")
                    else:
                        # Generic indicator
                        plt.plot(x_values, values, color="cyan+", label=col, marker=".")
                except Exception as e:
                    logger.print_warning(f"Could not plot indicator {col}: {e}")

        # Volume panel
        if has_volume and has_ohlc:
            plt.subplot(2, 1)
            plt.bar(x_values, volume_data, color="cyan+", label="Volume")
            plt.title("Volume")
            plt.xlabel("Time / Bar Index")
        else:
            plt.xlabel("Time / Bar Index")

        # Show the plot
        plt.show()

        # Print basic statistics and SR levels
        print("\n" + "=" * 80)
        print(f"{title} - {rule_str}".center(80))
        print("=" * 80)
        print(f"Data points: {len(df)}")

        if has_ohlc:
            # Safe min/max calculation
            low_min = min(ohlc_data['Low'])
            high_max = max(ohlc_data['High'])
            print(f"Price range: {low_min:.5f} - {high_max:.5f}")

        # Print SR levels if available
        if has_sr:
            print("\nSupport/Resistance Levels:")
            for col in sr_columns:
                try:
                    # Get unique non-zero values
                    values = [v for v in df[col].fillna(0).unique() if abs(v) > 1e-6]
                    if values:
                        print(f"  {col}: {', '.join(f'{v:.5f}' for v in sorted(values))}")
                except Exception as e:
                    logger.print_warning(f"Could not extract SR levels from {col}: {e}")

        print("=" * 80 + "\n")

        logger.print_success("SR plot displayed successfully")

    except Exception as e:
        logger.print_error(f"Safe SR plot failed: {e}")
        import traceback
        logger.print_debug(f"Error details: {traceback.format_exc()}")
