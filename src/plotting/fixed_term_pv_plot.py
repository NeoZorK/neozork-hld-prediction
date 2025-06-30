# -*- coding: utf-8 -*-
# src/plotting/fixed_term_pv_plot.py

"""
Fixed version of PV (Pressure Vector) terminal plotting functions.
Completely rewritten to avoid DataFrame ambiguity issues.
"""

import pandas as pd
import numpy as np
import plotext as plt
from typing import Optional, Union, List, Dict, Any

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from common.constants import TradingRule
except ImportError:
    # Fallback to relative imports when run as module
    from ..common import logger
    from ..common.constants import TradingRule


def safe_plot_pv_terminal(df: pd.DataFrame,
                         rule: Union[TradingRule, str],
                         title: str = "PV Terminal Plot",
                         output_path: Optional[str] = None) -> None:
    """
    Simplified and safe PV (Pressure Vector) terminal plot function that avoids DataFrame ambiguity.

    Args:
        df (pd.DataFrame): DataFrame with PV calculation results
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

        # Configure layout with PV panel
        # For PV analysis, we typically want 3 panels: price, pressure vector, and volume
        has_pv = any(col.lower() in ['pv', 'pressure_vector', 'pressurevector'] for col in df.columns)

        if has_ohlc and has_pv and has_volume:
            plt.subplots(3, 1)
            main_plot_size = (140, 60)  # Taller to accommodate three panels
        elif has_ohlc and has_pv:
            plt.subplots(2, 1)
            main_plot_size = (140, 50)
        elif has_ohlc and has_volume:
            plt.subplots(2, 1)
            main_plot_size = (140, 40)
        else:
            plt.subplots(1, 1)
            main_plot_size = (140, 30)

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

        # Panel 1: Main price panel
        if has_ohlc:
            plt.subplot(1, 1)  # First subplot

            # Plot candlesticks with plain data
            plt.candlestick(x_values, ohlc_data)
            plt.title(title)
            plt.ylabel("Price")

            # Add non-PV indicators to price panel
            for col in df.columns:
                if col in ['Open', 'High', 'Low', 'Close', 'Volume'] or \
                   col.lower() in ['pv', 'pressure_vector', 'pressurevector', 'pressure']:
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

                    if 'signal' in col_lower or 'direction' in col_lower:
                        # Handle signals
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
                        # Generic indicator on price panel
                        plt.plot(x_values, values, color="white", label=col, marker=".")
                except Exception as e:
                    logger.print_warning(f"Could not plot indicator {col}: {e}")

        # Panel 2: PV indicators
        if has_pv:
            if has_ohlc:
                plt.subplot(2, 1)  # Second subplot
            else:
                plt.subplot(1, 1)

            pv_plotted = False

            # Plot PV-related indicators
            for col in df.columns:
                if col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                    continue

                if col.lower() in ['pv', 'pressure_vector', 'pressurevector', 'pressure']:
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

                        # Add zero reference line for PV
                        plt.plot(x_values, [0] * len(x_values), color="gray", label="Zero Line")

                        # Plot PV as a bar chart with color coding
                        pos_x = []
                        pos_y = []
                        neg_x = []
                        neg_y = []

                        for i, val in enumerate(values):
                            if val > 0:
                                pos_x.append(x_values[i])
                                pos_y.append(val)
                            elif val < 0:
                                neg_x.append(x_values[i])
                                neg_y.append(val)

                        if pos_x:
                            plt.bar(pos_x, pos_y, color="green+", label=f"{col} Positive")
                        if neg_x:
                            plt.bar(neg_x, neg_y, color="red+", label=f"{col} Negative")

                        pv_plotted = True
                    except Exception as e:
                        logger.print_warning(f"Could not plot PV indicator {col}: {e}")

            if pv_plotted:
                plt.title("Pressure Vector")
                plt.ylabel("Pressure Magnitude")
            else:
                plt.title("No PV Data Available")

        # Panel 3: Volume panel (if we have both OHLC and PV, this is the third panel)
        if has_volume:
            if has_ohlc and has_pv:
                plt.subplot(3, 1)
            elif has_ohlc or has_pv:
                plt.subplot(2, 1)
            else:
                plt.subplot(1, 1)

            plt.bar(x_values, volume_data, color="cyan+", label="Volume")
            plt.title("Volume")
            plt.xlabel("Time / Bar Index")
        else:
            plt.xlabel("Time / Bar Index")

        # Show the plot
        plt.show()

        # Print basic statistics - without complex DataFrame operations
        print("\n" + "=" * 80)
        print(f"{title} - {rule_str}".center(80))
        print("=" * 80)
        print(f"Data points: {len(df)}")

        if has_ohlc:
            # Safe min/max calculation
            low_min = min(ohlc_data['Low'])
            high_max = max(ohlc_data['High'])
            print(f"Price range: {low_min:.5f} - {high_max:.5f}")

        print("=" * 80 + "\n")

        logger.print_success("PV plot displayed successfully")

    except Exception as e:
        logger.print_error(f"Safe PV plot failed: {e}")
        import traceback
        logger.print_debug(f"Error details: {traceback.format_exc()}")
