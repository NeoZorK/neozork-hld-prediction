# -*- coding: utf-8 -*-
# src/plotting/term_auto_plot.py

"""
Terminal-based auto plotting using plotext for displaying all DataFrame columns.
Beautiful candlestick charts with enhanced styling and multi-panel layouts.
"""

import pandas as pd
import numpy as np
import plotext as plt
from typing import Optional

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
except ImportError:
    # Fallback to relative imports when run as module
    from ..common import logger


def auto_plot_from_dataframe(df: pd.DataFrame, title: str = "Auto Terminal Plot", style: str = "matrix") -> None:
    """
    Automatically plot all numeric columns from a DataFrame in terminal with enhanced styling.
    Uses candlestick charts for OHLC data and line plots for other indicators.
    
    Args:
        df (pd.DataFrame): DataFrame with data to plot
        title (str): Title for the plot
        style (str): Plot style ('matrix', 'dots', 'git', etc.)
    """
    try:
        logger.print_info("Generating auto terminal plot for all DataFrame columns...")

        # Clear any previous plots
        plt.clear_data()
        plt.clear_figure()
        
        # Validate input data
        if df is None or df.empty:
            logger.print_error("DataFrame is None or empty, cannot plot")
            return
        
        # Ensure all required indicators exist for AUTO mode
        ohlc_columns = ['Open', 'High', 'Low', 'Close']
        has_ohlc = all(col in df.columns for col in ohlc_columns)

        if has_ohlc:
            # Check and add required indicators if they don't exist
            required_indicators = {
                'predicted_low': False,
                'predicted_high': False,
                'pressure': False,
                'pressure_vector': False
            }

            # Check which indicators already exist
            for col in df.columns:
                col_lower = col.lower()
                for indicator in required_indicators:
                    if indicator in col_lower or (indicator == 'pressure_vector' and 'pv' in col_lower):
                        required_indicators[indicator] = True

            # Add missing indicators
            if not required_indicators['predicted_low']:
                logger.print_info("Adding missing indicator: predicted_low")
                df['predicted_low'] = df['Low'] * 0.995  # Simple estimation

            if not required_indicators['predicted_high']:
                logger.print_info("Adding missing indicator: predicted_high")
                df['predicted_high'] = df['High'] * 1.005  # Simple estimation

            if not required_indicators['pressure']:
                logger.print_info("Adding missing indicator: pressure")
                # Calculate pressure as normalized value based on price action
                df['pressure'] = ((df['Close'] - df['Open']) / (df['High'] - df['Low']).replace(0, 1)) * 100
                # Scale pressure to be visible in price range
                min_price = df['Low'].min()
                max_price = df['High'].max()
                mid_price = (min_price + max_price) / 2
                scale_factor = (max_price - min_price) * 0.1
                df['pressure'] = mid_price + (df['pressure'] * scale_factor / 100)

            if not required_indicators['pressure_vector']:
                logger.print_info("Adding missing indicator: pressure_vector")
                # Calculate pressure_vector based on pressure with moving average
                if 'pressure' in df.columns:
                    # Use smoothed pressure as vector
                    window = min(14, len(df) // 4)  # Adjust window size based on data length
                    window = max(window, 2)  # Ensure window is at least 2
                    df['pressure_vector'] = df['pressure'].rolling(window=window, min_periods=1).mean()
                    # Make it slightly higher for better visualization
                    df['pressure_vector'] = df['pressure_vector'] * 1.02

        # Check if we have OHLC data for candlestick chart
        has_volume = 'Volume' in df.columns and not df['Volume'].isna().all()

        # Set up layout based on available data
        if has_ohlc and has_volume:
            plt.subplots(2, 1)  # Price + Volume panels
            main_plot_size = (140*3, 35*6)  # 6x larger vertically (doubled from previous 3x)
        elif has_ohlc:
            plt.subplots(1, 1)  # Single price panel
            main_plot_size = (140*3, 25*6)  # 6x larger vertically (doubled from previous 3x)
        else:
            plt.subplots(1, 1)  # Single indicator panel
            main_plot_size = (140*3, 25*6)  # 6x larger vertically (doubled from previous 3x)

        plt.plot_size(*main_plot_size)
        plt.theme('matrix')  # Use unified matrix theme for all plots
        # Note: Style is applied through marker choice in individual plot functions

        # Create time axis
        x_values = list(range(len(df)))

        # MAIN PANEL: OHLC Candlestick or Indicators
        if has_ohlc:
            logger.print_info("Creating OHLC candlestick chart with 'dots' style...")
            if has_volume:
                plt.subplot(1, 1)  # Top panel
            # Prepare OHLC data for candlestick
            ohlc_data = {
                'Open': df['Open'].ffill().fillna(df['Close']).tolist(),
                'High': df['High'].ffill().fillna(df['Close']).tolist(),
                'Low': df['Low'].ffill().fillna(df['Close']).tolist(),
                'Close': df['Close'].ffill().fillna(df['Open']).tolist()
            }
            plt.candlestick(x_values, ohlc_data)
            plt.title(f"{title} - Auto Chart (OHLC + Indicators)")
            if not has_volume:
                plt.xlabel("Time / Bar Index")
            plt.ylabel("Price")
            # Add other indicators as overlays on the price chart
            _add_indicator_overlays(df, x_values, skip_columns={'Open', 'High', 'Low', 'Close', 'Volume'}, style=style)
        else:
            logger.print_info("Creating multi-indicator chart with 'dots' style...")
            plt.title(f"{title} - Auto Indicators Chart")
            plt.xlabel("Time / Bar Index") 
            plt.ylabel("Values")
            # Plot all numeric columns as indicators
            _add_indicator_overlays(df, x_values, skip_columns={'Volume'}, style=style)
        
        # VOLUME PANEL (if available)
        if has_volume:
            logger.print_info("Creating volume panel...")
            plt.subplot(2, 1)  # Bottom panel
            
            # Safely convert volume to integers, handling NaN, inf, and non-numeric values
            volume_series = pd.to_numeric(df['Volume'], errors='coerce').replace([np.inf, -np.inf], np.nan).fillna(0)
            logger.print_debug(f"volume_series (after fillna): {volume_series.values}")
            if volume_series.isna().any():
                logger.print_warning(f"NaN values detected in volume_series at indices: {volume_series[volume_series.isna()].index.tolist()}")
                volume_series = volume_series.fillna(0)
            volume_array = np.array(volume_series.values, dtype=np.float64)
            logger.print_debug(f"volume_array (before nan_to_num): {volume_array}")
            if np.isnan(volume_array).any():
                logger.print_warning(f"NaN values detected in volume_array at indices: {np.where(np.isnan(volume_array))[0].tolist()}")
                volume_array = np.nan_to_num(volume_array, nan=0)
            logger.print_debug(f"volume_array (after nan_to_num): {volume_array}")
            volume_values = volume_array.astype(int).tolist()
            plt.bar(x_values, volume_values, color="cyan+", label="Volume")
            
            plt.title("📊 Trading Volume")
            plt.xlabel("Time / Bar Index")
            plt.ylabel("Volume")
        
        # Display the plot
        logger.print_info("Displaying auto terminal plot with all four indicators...")
        plt.show()
        
        # Show enhanced statistics
        _show_auto_statistics(df, title)
        
        logger.print_success("Auto terminal plot generated successfully!")

    except Exception as e:
        logger.print_error(f"Error generating auto terminal plot: {e}")
        logger.print_debug(f"Exception details: {type(e).__name__}: {e}")


def auto_plot_parquet_fields(file_path: str, title: str = "Auto Fields Plot", style: str = "dots") -> None:
    """
    Read a parquet file and display each field as a separate chart with green markers.

    Args:
        file_path (str): Path to the parquet file
        title (str): Base title for the plots
        style (str): Plot style ('matrix', 'dots', 'git', etc.)
    """
    try:
        logger.print_info(f"Reading parquet file and generating separate field plots: {file_path}")

        # Check if file exists
        import os
        if not os.path.exists(file_path):
            logger.print_error(f"Parquet file not found: {file_path}")
            return

        # Read parquet file
        import pandas as pd
        df = pd.read_parquet(file_path)

        # Validate data
        if df is None or df.empty:
            logger.print_error("Parquet file data is empty")
            return

        logger.print_info(f"Successfully read parquet file with {len(df)} rows and {len(df.columns)} columns")

        # Ensure all required indicators are present (predicted_low, predicted_high, pressure, pressure_vector)
        ohlc_columns = ['Open', 'High', 'Low', 'Close']
        has_ohlc = all(col in df.columns for col in ohlc_columns)

        if has_ohlc:
            # Check and add required indicators if they don't exist
            required_indicators = {
                'predicted_low': False,
                'predicted_high': False,
                'pressure': False,
                'pressure_vector': False
            }

            # Check which indicators already exist
            for col in df.columns:
                col_lower = col.lower()
                for indicator in required_indicators:
                    if indicator in col_lower or (indicator == 'pressure_vector' and 'pv' in col_lower):
                        required_indicators[indicator] = True

            # Add missing indicators
            if not required_indicators['predicted_low']:
                logger.print_info("Adding missing indicator: predicted_low")
                df['predicted_low'] = df['Low'] * 0.995  # Simple estimation

            if not required_indicators['predicted_high']:
                logger.print_info("Adding missing indicator: predicted_high")
                df['predicted_high'] = df['High'] * 1.005  # Simple estimation

            if not required_indicators['pressure']:
                logger.print_info("Adding missing indicator: pressure")
                # Calculate pressure as normalized value based on price action
                df['pressure'] = ((df['Close'] - df['Open']) / (df['High'] - df['Low']).replace(0, 1)) * 100
                # Scale pressure to be visible in price range
                min_price = df['Low'].min()
                max_price = df['High'].max()
                mid_price = (min_price + max_price) / 2
                scale_factor = (max_price - min_price) * 0.1
                df['pressure'] = mid_price + (df['pressure'] * scale_factor / 100)

            if not required_indicators['pressure_vector']:
                logger.print_info("Adding missing indicator: pressure_vector")
                # Calculate pressure_vector based on pressure with moving average
                if 'pressure' in df.columns:
                    # Use smoothed pressure as vector
                    window = min(14, len(df) // 4)  # Adjust window size based on data length
                    window = max(window, 2)  # Ensure window is at least 2
                    df['pressure_vector'] = df['pressure'].rolling(window=window, min_periods=1).mean()
                    # Make it slightly higher for better visualization
                    df['pressure_vector'] = df['pressure_vector'] * 1.02

        # Use separate field plotting with dots style
        from src.plotting.term_separate_plots import plot_separate_fields_terminal

        # First show the main OHLC chart if present
        if has_ohlc:
            logger.print_info("Creating main OHLC candlestick chart...")
            auto_plot_from_dataframe(df, f"{title} - OHLC Candlestick", style)

        # Then show separate charts for each numeric field
        plot_separate_fields_terminal(df, "AUTO", f"{title} - Fields", style=style)

        logger.print_success(f"Successfully plotted all fields from parquet file with '{style}' style!")

    except Exception as e:
        logger.print_error(f"Error processing parquet file: {type(e).__name__}: {e}")


def auto_plot_csv_fields(file_path: str, title: str = "Auto Fields Plot", style: str = "dots") -> None:
    """
    Read a CSV file and display each field as a separate chart with green markers.

    Args:
        file_path (str): Path to the CSV file
        title (str): Base title for the plots
        style (str): Plot style ('matrix', 'dots', 'git', etc.)
    """
    try:
        logger.print_info(f"Reading CSV file and generating separate field plots: {file_path}")

        # Check if file exists
        import os
        if not os.path.exists(file_path):
            logger.print_error(f"CSV file not found: {file_path}")
            return

        # Read CSV file
        import pandas as pd
        df = pd.read_csv(file_path)

        # Validate data
        if df is None or df.empty:
            logger.print_error("CSV file data is empty")
            return

        logger.print_info(f"Successfully read CSV file with {len(df)} rows and {len(df.columns)} columns")

        # Ensure all required indicators are present (predicted_low, predicted_high, pressure, pressure_vector)
        ohlc_columns = ['Open', 'High', 'Low', 'Close']
        has_ohlc = all(col in df.columns for col in ohlc_columns)

        if has_ohlc:
            # Check and add required indicators if they don't exist
            required_indicators = {
                'predicted_low': False,
                'predicted_high': False,
                'pressure': False,
                'pressure_vector': False
            }

            # Check which indicators already exist
            for col in df.columns:
                col_lower = col.lower()
                for indicator in required_indicators:
                    if indicator in col_lower or (indicator == 'pressure_vector' and 'pv' in col_lower):
                        required_indicators[indicator] = True

            # Add missing indicators
            if not required_indicators['predicted_low']:
                logger.print_info("Adding missing indicator: predicted_low")
                df['predicted_low'] = df['Low'] * 0.995  # Simple estimation

            if not required_indicators['predicted_high']:
                logger.print_info("Adding missing indicator: predicted_high")
                df['predicted_high'] = df['High'] * 1.005  # Simple estimation

            if not required_indicators['pressure']:
                logger.print_info("Adding missing indicator: pressure")
                # Calculate pressure as normalized value based on price action
                df['pressure'] = ((df['Close'] - df['Open']) / (df['High'] - df['Low']).replace(0, 1)) * 100
                # Scale pressure to be visible in price range
                min_price = df['Low'].min()
                max_price = df['High'].max()
                mid_price = (min_price + max_price) / 2
                scale_factor = (max_price - min_price) * 0.1
                df['pressure'] = mid_price + (df['pressure'] * scale_factor / 100)

            if not required_indicators['pressure_vector']:
                logger.print_info("Adding missing indicator: pressure_vector")
                # Calculate pressure_vector based on pressure with moving average
                if 'pressure' in df.columns:
                    # Use smoothed pressure as vector
                    window = min(14, len(df) // 4)  # Adjust window size based on data length
                    window = max(window, 2)  # Ensure window is at least 2
                    df['pressure_vector'] = df['pressure'].rolling(window=window, min_periods=1).mean()
                    # Make it slightly higher for better visualization
                    df['pressure_vector'] = df['pressure_vector'] * 1.02

        # Use separate field plotting with dots style
        from src.plotting.term_separate_plots import plot_separate_fields_terminal

        # First show the main OHLC chart if present
        if has_ohlc:
            logger.print_info("Creating main OHLC candlestick chart...")
            auto_plot_from_dataframe(df, f"{title} - OHLC Candlestick", style)

        # Then show separate charts for each numeric field
        plot_separate_fields_terminal(df, "AUTO", f"{title} - Fields", style=style)

        logger.print_success(f"Successfully plotted all fields from CSV file with '{style}' style!")

    except Exception as e:
        logger.print_error(f"Error processing CSV file: {type(e).__name__}: {e}")


def _add_indicator_overlays(df: pd.DataFrame, x_values: list, skip_columns: set, style: str = "matrix") -> None:
    """Add indicator overlays with different colors to visually distinguish different indicators."""

    # Fixed colors for the main indicators (to ensure consistent colors)
    indicator_colors = {
        'Predicted Low': 'green+',
        'Predicted High': 'red+',
        'Pressure': 'blue+',
        'Pressure Vector': 'yellow+'
    }

    # Other colors for additional indicators
    additional_colors = ["magenta+", "cyan+", "white+", "green", "red", "blue"]

    # Always use dot marker for better visibility in terminal
    marker = "."

    # Define mapping for indicator labels and their priority order (lower number = higher priority)
    indicator_mapping = {
        'predicted_low': {'label': 'Predicted Low', 'priority': 1},
        'predicted_high': {'label': 'Predicted High', 'priority': 2},
        'pressure': {'label': 'Pressure', 'priority': 3},
        'pressure_vector': {'label': 'Pressure Vector', 'priority': 4},
        'pprice1': {'label': 'Predicted Low', 'priority': 1},
        'pprice2': {'label': 'Predicted High', 'priority': 2},
        'pv': {'label': 'Pressure Vector', 'priority': 4},
        'direction': {'label': 'Direction', 'priority': 5},
        'signal': {'label': 'Signal', 'priority': 6}
    }

    # Standard columns to skip
    extended_skip = skip_columns.union({
        'DateTime', 'Timestamp', 'Date', 'Time', 'Index', 'index'
    })
    
    # First, let's ensure our 4 key indicators are present in the dataframe
    required_indicators = {
        'predicted_low': False,
        'predicted_high': False,
        'pressure': False,
        'pressure_vector': False
    }

    # Check which indicators already exist
    for col in df.columns:
        col_lower = col.lower()
        for indicator in required_indicators:
            if indicator in col_lower or (indicator == 'pressure_vector' and 'pv' in col_lower):
                required_indicators[indicator] = True

    # Add missing indicators automatically
    ohlc_columns = ['Open', 'High', 'Low', 'Close']
    has_ohlc = all(col in df.columns for col in ohlc_columns)

    if has_ohlc:
        # Add missing indicators
        if not required_indicators['predicted_low']:
            logger.print_info("Adding missing indicator: predicted_low")
            df['predicted_low'] = df['Low'] * 0.995  # Simple estimation

        if not required_indicators['predicted_high']:
            logger.print_info("Adding missing indicator: predicted_high")
            df['predicted_high'] = df['High'] * 1.005  # Simple estimation

        if not required_indicators['pressure']:
            logger.print_info("Adding missing indicator: pressure")
            # Calculate pressure as normalized value based on price action
            df['pressure'] = ((df['Close'] - df['Open']) / (df['High'] - df['Low']).replace(0, 1)) * 100
            # Scale pressure to be visible in price range
            min_price = df['Low'].min()
            max_price = df['High'].max()
            mid_price = (min_price + max_price) / 2
            scale_factor = (max_price - min_price) * 0.1
            df['pressure'] = mid_price + (df['pressure'] * scale_factor / 100)

        if not required_indicators['pressure_vector']:
            logger.print_info("Adding missing indicator: pressure_vector")
            # Calculate pressure_vector based on pressure with moving average
            if 'pressure' in df.columns:
                # Use smoothed pressure as vector
                window = min(14, len(df) // 4)  # Adjust window size based on data length
                window = max(window, 2)  # Ensure window is at least 2
                df['pressure_vector'] = df['pressure'].rolling(window=window, min_periods=1).mean()
                # Make it slightly higher for better visualization
                df['pressure_vector'] = df['pressure_vector'] * 1.02

    # Collect all columns to plot first, so we can sort them by priority
    columns_to_plot = []

    for col in df.columns:
        if col not in extended_skip and pd.api.types.is_numeric_dtype(df[col]):
            # Determine label and priority for this column
            label = col
            priority = 999  # Default low priority

            # Check if this column matches any of our known indicators
            for key, mapping in indicator_mapping.items():
                if key.upper() in col.upper() or (key == 'pressure_vector' and 'PV' in col.upper()):
                    label = mapping['label']
                    priority = mapping['priority']
                    break

            columns_to_plot.append({
                'column': col,
                'label': label,
                'priority': priority
            })

    # Sort columns by priority
    columns_to_plot.sort(key=lambda x: x['priority'])

    # Print debug info about what will be plotted
    logger.print_debug(f"Found {len(columns_to_plot)} columns to plot:")
    for item in columns_to_plot:
        logger.print_debug(f"  - {item['column']} → {item['label']} (priority: {item['priority']})")

    # Keep track of added labels to prevent duplicates
    added_labels = set()

    # Count of actually plotted indicators
    plotted_count = 0

    # Plot columns in priority order with different colors
    for i, column_info in enumerate(columns_to_plot):
        col = column_info['column']
        label = column_info['label']

        # Skip if this label is already added (prevents duplicates)
        if label in added_labels:
            logger.print_debug(f"Skipping duplicate label: {label} for column {col}")
            continue

        try:
            # Robustly clean numeric column before plotting
            values = pd.to_numeric(df[col], errors='coerce').replace([np.inf, -np.inf], np.nan).fillna(0).to_numpy(dtype=float)
            values = np.nan_to_num(values, nan=0)
            values = values.tolist()

            # Use fixed colors for our main indicators
            if label in indicator_colors:
                color = indicator_colors[label]
            else:
                # Use other colors for additional indicators
                color = additional_colors[(i - len(indicator_colors)) % len(additional_colors)]

            added_labels.add(label)
            plt.plot(x_values, values, color=color, label=label, marker=marker)
            plotted_count += 1

            logger.print_debug(f"Added indicator: {label} (from column {col}) with color {color}")

        except Exception as e:
            logger.print_warning(f"Could not plot column {col}: {e}")

    # Log the total number of indicators that were actually plotted
    logger.print_info(f"Successfully plotted {plotted_count} indicators on the chart")


def _show_auto_statistics(df: pd.DataFrame, title: str) -> None:
    """Display auto statistics with simplified output."""

    header_line = "=" * 80
    print(f"\n{header_line}")
    print(f"{'AUTO PLOT STATISTICS':^80}")
    print(f"{title:^80}")
    print(f"{header_line}")
    
    # Data overview
    print(f"DATA OVERVIEW:")
    print(f"   Total Rows:     {len(df)}")
    print(f"   Total Columns:  {len(df.columns)}")
    print(f"   Numeric Cols:   {df.select_dtypes(include=[np.number]).shape[1]}")

    # Column analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(f"\nCOLUMN STATISTICS:")
        for col in numeric_cols:
            if col in df.columns:
                try:
                    # More robust NaN handling
                    col_data = df[col].dropna()
                    if len(col_data) > 0:
                        print(f"   {col}:")
                        print(f"      Max: {col_data.max():.3f}")
                        print(f"      Min: {col_data.min():.3f}")

                        # Check for infinite values before calculating mean
                        clean_data = col_data.replace([np.inf, -np.inf], np.nan).dropna()
                        if len(clean_data) > 0:
                            print(f"      Avg: {clean_data.mean():.3f}")
                        else:
                            print(f"      Avg: N/A (no valid data)")
                    else:
                        print(f"   {col}: No valid data")
                except Exception as e:
                    print(f"   {col}: Error calculating statistics - {str(e)}")

    # OHLC specific stats if available
    ohlc_columns = ['Open', 'High', 'Low', 'Close']
    if all(col in df.columns for col in ohlc_columns):
        print(f"\nOHLC STATISTICS:")
        print(f"   Highest:    {df['High'].max():.5f}")
        print(f"   Lowest:     {df['Low'].min():.5f}")
        print(f"   Final:      {df['Close'].iloc[-1]:.5f}")
        print(f"   Initial:    {df['Open'].iloc[0]:.5f}")

        price_change = df['Close'].iloc[-1] - df['Open'].iloc[0]
        price_change_pct = (price_change / df['Open'].iloc[0]) * 100
        direction_symbol = "+" if price_change >= 0 else "-"
        print(f"   Change:     {price_change:+.5f} ({price_change_pct:+.2f}%)")

    print(f"\n{header_line}")
    print(f"{'Auto Terminal Charts - All Data Visualized':^80}")
    print(f"{header_line}\n")


def plot_column_comparison(df: pd.DataFrame, col1: str, col2: str, title: str = "Column Comparison") -> None:
    """
    Plot two specific columns for comparison in terminal.
    
    Args:
        df (pd.DataFrame): DataFrame containing the columns
        col1 (str): First column name
        col2 (str): Second column name
        title (str): Title for the plot
    """
    try:
        logger.print_info(f"Comparing columns: {col1} vs {col2}")
        
        # Clear any previous plots
        plt.clear_data()
        plt.clear_figure()
        
        # Validate columns exist
        if col1 not in df.columns or col2 not in df.columns:
            logger.print_error(f"Columns not found. Available: {list(df.columns)}")
            return
        
        # Set terminal size and theme
        plt.theme('retro')
        plt.plot_size(120, 25)
        
        # Create time axis
        x_values = list(range(len(df)))
        
        # Get column data
        values1 = df[col1].ffill().fillna(0).tolist()
        values2 = df[col2].ffill().fillna(0).tolist()
        
        # Plot both columns
        plt.plot(x_values, values1, color="green+", label=f"📈 {col1}")
        plt.plot(x_values, values2, color="red+", label=f"📉 {col2}")
        
        # Configure plot
        plt.title(f"📊 {title}")
        plt.xlabel("Time / Bar Index")
        plt.ylabel("Values")
        
        # Display
        plt.show()
        
        # Show comparison statistics
        print(f"\n📊 COMPARISON STATISTICS:")
        print(f"   📈 {col1}: Min={min(values1):.3f}, Max={max(values1):.3f}, Avg={np.mean(values1):.3f}")
        print(f"   📉 {col2}: Min={min(values2):.3f}, Max={max(values2):.3f}, Avg={np.mean(values2):.3f}")
        
        correlation = np.corrcoef(values1, values2)[0, 1] if len(values1) > 1 else 0
        print(f"   🔗 Correlation: {correlation:.3f}")
        
        logger.print_success("Column comparison plot generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating comparison plot: {e}")


def plot_histogram_terminal(df: pd.DataFrame, column: str, bins: int = 20, title: str = "Histogram") -> None:
    """
    Plot a histogram of a specific column in terminal.
    
    Args:
        df (pd.DataFrame): DataFrame containing the column
        column (str): Column name to plot
        bins (int): Number of histogram bins
        title (str): Title for the plot
    """
    try:
        logger.print_info(f"Creating histogram for column: {column}")
        
        if column not in df.columns:
            logger.print_error(f"Column {column} not found")
            return
        
        # Clear plots
        plt.clear_data()
        plt.clear_figure()
        
        # Set theme and size
        plt.theme('retro')
        plt.plot_size(100, 20)
        
        # Get data and create histogram
        data = df[column].dropna().tolist()
        if not data:
            logger.print_error(f"No valid data in column {column}")
            return
        
        # Use plotext's hist function
        plt.hist(data, bins=bins, color="blue+")
        plt.title(f"📊 {title} - {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        
        plt.show()
        
        # Show statistics
        print(f"\n📊 HISTOGRAM STATISTICS for {column}:")
        print(f"   📋 Count: {len(data)}")
        print(f"   📊 Mean:  {np.mean(data):.3f}")
        print(f"   📈 Std:   {np.std(data):.3f}")
        print(f"   📉 Min:   {min(data):.3f}")
        print(f"   🔺 Max:   {max(data):.3f}")
        
        logger.print_success("Histogram generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating histogram: {e}")
