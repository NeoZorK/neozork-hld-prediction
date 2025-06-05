# src/plotting/term_auto_plot.py
"""
Terminal auto plotting for AUTO rule mode.
Displays each column in a parquet file as a separate chart in the terminal.
Especially useful for Docker environments where only terminal visualization works.
"""
import pandas as pd
import plotext as plt
import os
import random
import numpy as np

# Helper function to set consistent chart styling
def set_terminal_chart_style(title="Chart"):
    """
    Apply consistent styling to terminal charts for better visibility.

    Args:
        title: Title of the chart
    """
    plt.canvas_color("black")        # Black background for better contrast
    plt.axes_color("black")          # Black axes background as requested
    plt.ticks_color("yellow")        # Yellow tick marks for better visibility
    # Grid removed as requested
    plt.title(title)


# Helper function to generate random terminal colors
def get_random_color():
    """
    Generate a random color for terminal plotting with enhanced diversity.

    Returns:
        A random color name from extended plotext available colors
    """
    # Extended list of available plotext colors for maximum diversity
    available_colors = [
        # Bright colors
        "bright_red", "bright_yellow", "bright_green", "bright_cyan",
        "bright_blue", "bright_magenta", "bright_white",
        # Regular colors
        "red", "yellow", "green", "cyan", "blue", "magenta", "white",
        # Additional colors
        "orange", "purple", "pink", "lime", "peach", "olive", "teal",
        # Darker shades
        "dark_red", "dark_yellow", "dark_green", "dark_cyan",
        "dark_blue", "dark_magenta", "grey",
        # Custom combinations (using name patterns that plotext might support)
        "light_blue", "light_green", "light_red", "light_yellow",
        "deep_purple", "deep_blue", "gold", "silver", "bronze",
        "navy", "forest", "crimson", "coral", "aqua", "violet"
    ]
    return random.choice(available_colors)

# Helper function to generate random non-repeating colors for charts
def get_random_non_repeating_colors(count):
    """
    Generate a list of random non-repeating colors for terminal plotting.

    Args:
        count: Number of unique colors needed

    Returns:
        List of unique random colors
    """
    import time
    
    # Extended list of available plotext colors for maximum diversity
    available_colors = [
        # Bright colors
        "bright_red", "bright_yellow", "bright_green", "bright_cyan",
        "bright_blue", "bright_magenta", "bright_white",
        # Regular colors
        "red", "yellow", "green", "cyan", "blue", "magenta", "white",
        # Additional colors
        "orange", "purple", "pink", "lime", "peach", "olive", "teal",
        # Darker shades
        "dark_red", "dark_yellow", "dark_green", "dark_cyan",
        "dark_blue", "dark_magenta", "grey",
        # Custom combinations (using name patterns that plotext might support)
        "light_blue", "light_green", "light_red", "light_yellow",
        "deep_purple", "deep_blue", "gold", "silver", "bronze",
        "navy", "forest", "crimson", "coral", "aqua", "violet"
    ]
    
    # Use time-based seed to ensure different results each call
    random.seed(int(time.time() * 1000000) % 2**32)
    
    # Shuffle the colors and return the requested count
    shuffled_colors = available_colors.copy()
    random.shuffle(shuffled_colors)
    
    # If we need more colors than available, cycle through them
    if count > len(shuffled_colors):
        cycles = (count // len(shuffled_colors)) + 1
        shuffled_colors = shuffled_colors * cycles
    
    return shuffled_colors[:count]

# Helper function to generate consistent beautiful marker
def get_beautiful_marker():
    """
    Generate a consistent beautiful marker for terminal plotting.
    Uses braille marker (same as OHLC High) for consistency.

    Returns:
        A beautiful consistent marker for all terminal charts
    """
    # Use braille as the same marker used for OHLC High
    return "braille"

def clean_data_for_plotting(df, column_name, x_data):
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

def auto_plot_from_parquet(parquet_path: str, rule: str, plot_title: str = "Auto Terminal Plot"):
    """
    Plot data from a parquet file in the terminal based on the specified rule.

    Args:
        parquet_path: Path to the parquet file
        rule: Rule to determine which columns to plot (e.g., AUTO, PHLD, PV, SR)
        plot_title: Title for the overall plot
    """
    if not os.path.exists(parquet_path):
        print(f"File not found: {parquet_path}")
        return

    # Configure plotext theme for better contrast in terminal
    plt.theme("dark")  # Use dark theme for better visibility in terminal

    df = pd.read_parquet(parquet_path)
    if df.empty:
        print("Empty DataFrame.")
        return

    # Print the custom title
    print(f"\n📊 {plot_title}")
    print("=" * (len(plot_title) + 5))

    # Determine OHLC columns, volume, and time columns
    ohlc_cols = [col for col in df.columns if col.lower() in ["open", "high", "low", "close"]]
    volume_col = next((col for col in df.columns if col.lower() == "volume"), None)
    time_col = next((col for col in df.columns if col.lower() in ["timestamp", "datetime", "date", "time"]), None)

    # Other indicator columns
    exclude = set(ohlc_cols + ([volume_col] if volume_col else []) + ([time_col] if time_col else []))
    indicator_cols = [col for col in df.columns if col not in exclude]

    # Prepare x-axis data
    if time_col:
        x_data = df[time_col].tolist()
    else:
        x_data = list(range(len(df)))

    # Define color palette for all charts - rainbow colors for better visibility
    rainbow_colors = [
        "bright_red", "bright_yellow", "bright_green", "bright_cyan",
        "bright_blue", "bright_magenta", "bright_white",
        "red", "yellow", "green", "cyan", "blue", "magenta", "white"
    ]

    # Plot OHLC data
    plt.clear_data()
    print("\n📈 OHLC Chart")
    set_terminal_chart_style("OHLC Chart")

    # Use different colors for each OHLC component with maximum contrast
    ohlc_colors = {
        "open": "bright_magenta",   # Changed: Bright magenta for open price (better visual distinction)
        "high": "bright_cyan",      # Bright cyan for high price
        "low": "bright_red",        # Bright red for low price
        "close": "bright_blue"      # Changed: Bright blue for close price (better contrast and readability)
    }

    # Use consistent braille markers for all OHLC components
    markers = {
        "open": "braille",   # Changed: Braille marker for open (same as high/low)
        "high": "braille",   # Braille marker for high
        "low": "braille",    # Braille marker for low
        "close": "braille"   # Changed: Braille marker for close (same as high/low)
    }

    for col in ohlc_cols:
        col_lower = col.lower()
        color = ohlc_colors.get(col_lower, "bright_white")  # Default to bright white if not found
        marker = markers.get(col_lower, "braille")          # Default to braille if not found
        
        # Clean data for plotting (remove NaN and infinite values)
        x_clean, y_clean, num_removed = clean_data_for_plotting(df, col, x_data)
        
        if len(y_clean) == 0:
            print(f"⚠️  Skipping OHLC column '{col}' - no valid finite data")
            continue
            
        if num_removed > 0:
            print(f"ℹ️  Cleaned {num_removed} non-finite values from '{col}'")
            
        plt.plot(x_clean, y_clean, label=col, marker=marker, color=color)
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.show()

    # Plot Volume
    if volume_col:
        plt.clear_data()
        print("\n📊 Volume Chart")
        set_terminal_chart_style("Volume Chart")
        
        # Clean volume data for plotting (remove NaN and infinite values)
        x_clean, y_clean, num_removed = clean_data_for_plotting(df, volume_col, x_data)
        
        if len(y_clean) == 0:
            print(f"⚠️  Skipping Volume column '{volume_col}' - no valid finite data")
        else:
            if num_removed > 0:
                print(f"ℹ️  Cleaned {num_removed} non-finite values from '{volume_col}'")
            plt.bar(x_clean, y_clean, label="Volume", color="bright_magenta")
            plt.xlabel("Time")
            plt.ylabel("Volume")
            plt.show()

    # Plot indicators based on the rule
    if rule.upper() == "AUTO":
        # Get random non-repeating colors for all indicators at once
        indicator_colors = get_random_non_repeating_colors(len(indicator_cols))
        
        for idx, col in enumerate(indicator_cols):
            plt.clear_data()
            print(f"\n📈 Indicator: {col}")
            set_terminal_chart_style(f"Indicator: {col}")

            # Clean data for plotting (remove NaN and infinite values)
            x_clean, y_clean, num_removed = clean_data_for_plotting(df, col, x_data)
            
            if len(y_clean) == 0:
                print(f"⚠️  Skipping indicator '{col}' - no valid finite data")
                continue
            
            if num_removed > 0:
                print(f"ℹ️  Cleaned {num_removed} non-finite values from '{col}'")
                
            # Use consistent beautiful marker and unique non-repeating color for each column
            plt.plot(x_clean, y_clean, label=col, marker=get_beautiful_marker(), color=indicator_colors[idx])
            plt.xlabel("Time")
            plt.ylabel("Value")
            plt.show()
    elif rule.upper() in ["PHLD", "PV", "SR"]:
        relevant_cols = [col for col in indicator_cols if rule.lower() in col.lower()]
        for idx, col in enumerate(relevant_cols):
            plt.clear_data()
            print(f"\n📈 Rule {rule}: {col}")
            set_terminal_chart_style(f"Rule {rule}: {col}")

            # Clean data for plotting (remove NaN and infinite values)
            x_clean, y_clean, num_removed = clean_data_for_plotting(df, col, x_data)
            
            if len(y_clean) == 0:
                print(f"⚠️  Skipping indicator '{col}' - no valid finite data")
                continue
            
            if num_removed > 0:
                print(f"ℹ️  Cleaned {num_removed} non-finite values from '{col}'")
                
            # Use a unique color for each column based on its index or hash
            color = rainbow_colors[idx % len(rainbow_colors)] if idx < len(rainbow_colors) else rainbow_colors[hash(col) % len(rainbow_colors)]
            plt.plot(x_clean, y_clean, label=col, marker=get_beautiful_marker(), color=color)
            plt.xlabel("Time")
            plt.ylabel("Value")
            plt.show()
    else:
        print(f"Rule {rule} not recognized.")

def auto_plot_from_dataframe(df: pd.DataFrame, plot_title: str = "Auto Terminal Plot"):
    """
    Plot all columns in a DataFrame as separate charts in the terminal.

    Args:
        df: DataFrame with data to plot
        plot_title: Title for the overall plot
    """
    if df.empty:
        print("Empty DataFrame.")
        return

    # Configure plotext theme for better contrast in terminal
    plt.theme("clear")  # Clear theme first
    plt.theme("dark")   # Then apply dark theme for better visibility

    # Print the custom title
    print(f"\n📊 {plot_title}")
    print("=" * (len(plot_title) + 5))

    # Determine OHLC columns, volume, and time columns
    ohlc_cols = [col for col in df.columns if col.lower() in ["open", "high", "low", "close"]]
    volume_col = next((col for col in df.columns if col.lower() == "volume"), None)
    time_col = next((col for col in df.columns if col.lower() in ["timestamp", "datetime", "date", "time"]), None)

    # Group columns by categories for better organization
    phld_price_cols = [col for col in df.columns if col.lower() in ["pprice1", "pprice2", "predicted_high", "predicted_low"]]
    phld_signal_cols = [col for col in df.columns if col.lower() in ["direction", "pcolor1", "pcolor2"]]
    phld_metric_cols = [col for col in df.columns if col.lower() in ["diff", "hl", "pressure", "pv"]]

    # Check if this dataframe has pre-calculated or calculated indicators
    has_precalculated = any(col.lower() in ["pprice1", "pprice2", "predicted_high", "predicted_low", "direction"] for col in df.columns)
    has_calculated = any(col.lower().endswith("_calc") for col in df.columns)

    # Print data source information for clarity
    if has_precalculated and not has_calculated:
        print(f"\n📁 [DATA SOURCE: LOADED FROM FILE] - Using pre-calculated indicators")
    elif has_calculated and not has_precalculated:
        print(f"\n🧮 [DATA SOURCE: CALCULATED NOW] - Using newly calculated indicators")
    elif has_precalculated and has_calculated:
        print(f"\n📊 [DATA SOURCE: BOTH] - Showing both pre-calculated and newly calculated indicators")
    else:
        print(f"\n📄 [DATA SOURCE: RAW DATA] - No indicators detected")

    # Other indicator columns - exclude all categorized columns
    exclude = set(ohlc_cols + ([volume_col] if volume_col else []) +
                 ([time_col] if time_col else []) +
                 phld_price_cols + phld_signal_cols + phld_metric_cols)
    indicator_cols = [col for col in df.columns if col not in exclude]

    # Prepare x-axis data
    if time_col:
        x_data = df[time_col].tolist()
    else:
        x_data = list(range(len(df)))

    # Process OHLC data
    if ohlc_cols:
        plt.clear_figure()  # Completely clear the figure
        plt.clear_data()    # Clear any plotted data
        print("\n📈 OHLC Chart")
        plt.canvas_color("black")
        plt.axes_color("black")
        plt.ticks_color("yellow")
        plt.title("OHLC Chart")

        # Use different colors for each OHLC component
        ohlc_colors = {
            "open": "bright_magenta",
            "high": "bright_cyan",
            "low": "bright_red",
            "close": "bright_blue"
        }

        for col in ohlc_cols:
            col_lower = col.lower()
            color = ohlc_colors.get(col_lower, "bright_white")

            # Clean data for plotting (remove NaN and infinite values)
            x_clean, y_clean, num_removed = clean_data_for_plotting(df, col, x_data)
            
            if len(y_clean) == 0:
                print(f"⚠️  Skipping OHLC column '{col}' - no valid finite data")
                continue
                
            if num_removed > 0:
                print(f"ℹ️  Cleaned {num_removed} non-finite values from '{col}'")

            # Plot the OHLC component with its unique color
            plt.plot(x_clean, y_clean, label=f"{col} 📁 [LOADED]", marker="braille", color=color)

        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.show()

    # Process Volume
    if volume_col:
        plt.clear_figure()  # Completely clear the figure
        plt.clear_data()    # Clear any plotted data
        print("\n📊 Volume Chart")
        plt.canvas_color("black")
        plt.axes_color("black")
        plt.ticks_color("yellow")
        plt.title("Volume Chart")

        # Clean volume data for plotting (remove NaN and infinite values)
        x_clean, y_clean, num_removed = clean_data_for_plotting(df, volume_col, x_data)
        
        if len(y_clean) == 0:
            print(f"⚠️  Skipping Volume column '{volume_col}' - no valid finite data")
        else:
            if num_removed > 0:
                print(f"ℹ️  Cleaned {num_removed} non-finite values from '{volume_col}'")
            plt.bar(x_clean, y_clean, label=f"Volume 📁 [LOADED]", color="bright_magenta")
            plt.xlabel("Time")
            plt.ylabel("Volume")
            plt.show()

    # Process PHLD predicted price columns (PPrice1, PPrice2, etc.)
    if phld_price_cols:
        plt.clear_figure()
        plt.clear_data()
        print("\n🎯 PHLD PREDICTED PRICES")
        plt.canvas_color("black")
        plt.axes_color("black")
        plt.ticks_color("yellow")
        plt.title("PHLD Predicted Prices")

        # First, plot Close price for reference
        if 'Close' in df.columns:
            x_clean, y_clean, num_removed = clean_data_for_plotting(df, 'Close', x_data)
            if len(y_clean) > 0:
                plt.plot(x_clean, y_clean, label="Close 📁 [LOADED]", color="bright_blue", marker="braille")

        # Plot predicted price levels
        colors = ['bright_green', 'bright_red', 'bright_yellow', 'bright_magenta']
        for i, col in enumerate(phld_price_cols):
            color = colors[i % len(colors)]
            x_clean, y_clean, num_removed = clean_data_for_plotting(df, col, x_data)

            if len(y_clean) == 0:
                print(f"⚠️  Skipping price column '{col}' - no valid finite data")
                continue

            if num_removed > 0:
                print(f"ℹ️  Cleaned {num_removed} non-finite values from '{col}'")

            # Add source indicator to the label
            source_label = "📁 [LOADED]" if not col.lower().endswith("_calc") else "🧮 [CALCULATED]"
            plt.plot(x_clean, y_clean, label=f"{col} {source_label}", color=color, marker="braille")

        plt.xlabel("Time")
        plt.ylabel("Price Level")
        plt.show()

    # Process PHLD signal columns (Direction, PColor1, PColor2)
    if phld_signal_cols:
        plt.clear_figure()
        plt.clear_data()
        print("\n🚦 PHLD TRADING SIGNALS")
        plt.canvas_color("black")
        plt.axes_color("black")
        plt.ticks_color("yellow")
        plt.title("PHLD Trading Signals")

        # Process Direction specially if it exists
        if 'Direction' in df.columns:
            x_clean, dir_data, num_removed = clean_data_for_plotting(df, 'Direction', x_data)

            if len(dir_data) > 0:
                # Direction: 1=Buy, -1/2=Sell, 0=Hold
                buy_points = [1 if val == 1 else 0 for val in dir_data]
                sell_points = [1 if val in [-1, 2] else 0 for val in dir_data]

                # Print signal summary above the chart
                buy_count = sum(buy_points)
                sell_count = sum(sell_points)
                hold_count = len(dir_data) - buy_count - sell_count

                # Clear source information to avoid confusion
                source_label = "📁 [LOADED]" if not 'Direction'.lower().endswith("_calc") else "🧮 [CALCULATED]"
                print(f"▲ Buy Signals: {buy_count}")
                print(f"▼ Sell Signals: {sell_count}")
                print(f"○ Hold Signals: {hold_count}")
                print(f"Signal summary: {buy_count} Buy, {sell_count} Sell, {hold_count} Hold - {source_label}")

                # Use scatter plot with triangles instead of bars
                # Create x-positions for buy signals (only where buy_points is 1)
                buy_x = [x_clean[i] for i in range(len(x_clean)) if buy_points[i] == 1]
                buy_y = [1] * len(buy_x)

                # Create x-positions for sell signals (only where sell_points is 1)
                sell_x = [x_clean[i] for i in range(len(x_clean)) if sell_points[i] == 1]
                sell_y = [-1] * len(sell_x)

                # Plot Buy/Sell signals as points with custom markers for better visibility
                if buy_x:
                    # Removed 's' parameter as it's not supported in plotext
                    plt.scatter(buy_x, buy_y, marker="triangle", color="bright_green")

                if sell_x:
                    # Removed 's' parameter as it's not supported in plotext
                    plt.scatter(sell_x, sell_y, marker="triangle", color="bright_red")

                # Add a zero line for reference
                plt.plot(x_clean, [0] * len(x_clean), label="Neutral", color="gray")

                # Set custom y-ticks for clarity
                plt.yticks([-1, 0, 1], ["Sell", "Hold", "Buy"])

                phld_signal_cols.remove('Direction')

        # Plot other signal columns
        colors = ['bright_cyan', 'bright_yellow', 'orange']
        for i, col in enumerate(phld_signal_cols):
            if col not in df.columns:
                continue

            color = colors[i % len(colors)]
            x_clean, y_clean, num_removed = clean_data_for_plotting(df, col, x_data)

            if len(y_clean) == 0:
                print(f"⚠️  Skipping signal column '{col}' - no valid finite data")
                continue

            if num_removed > 0:
                print(f"ℹ️  Cleaned {num_removed} non-finite values from '{col}'")

            # Add source indicator to the label
            source_label = "📁 [LOADED]" if not col.lower().endswith("_calc") else "🧮 [CALCULATED]"
            plt.plot(x_clean, y_clean, label=f"{col} {source_label}", color=color, marker="braille")

        plt.xlabel("Time")
        plt.ylabel("Signal Value")
        plt.show()

    # Process PHLD metric columns (HL, Pressure, PV, Diff)
    if phld_metric_cols:
        plt.clear_figure()
        plt.clear_data()
        print("\n📊 PHLD METRICS")
        plt.canvas_color("black")
        plt.axes_color("black")
        plt.ticks_color("yellow")
        plt.title("PHLD Metrics")

        colors = ['bright_yellow', 'bright_magenta', 'bright_cyan', 'bright_white']
        for i, col in enumerate(phld_metric_cols):
            if col not in df.columns:
                continue

            color = colors[i % len(colors)]
            x_clean, y_clean, num_removed = clean_data_for_plotting(df, col, x_data)

            if len(y_clean) == 0:
                print(f"⚠️  Skipping metric column '{col}' - no valid finite data")
                continue

            if num_removed > 0:
                print(f"ℹ️  Cleaned {num_removed} non-finite values from '{col}'")

            # Add zero line for metrics that can be positive/negative
            if col.lower() in ['hl', 'pressure', 'pv']:
                plt.plot(x_clean, [0] * len(x_clean), label="Zero Line", color="gray")

            # Add source indicator to the label
            source_label = "📁 [LOADED]" if not col.lower().endswith("_calc") else "🧮 [CALCULATED]"
            plt.plot(x_clean, y_clean, label=f"{col} {source_label}", color=color, marker="braille")

        plt.xlabel("Time")
        plt.ylabel("Metric Value")
        plt.show()

    # Define marker - always use braille for consistency
    marker = "braille"

    # For each other indicator, create a standalone plot with its own random color
    for idx, col in enumerate(indicator_cols):
        # Filter out columns with '_calc' suffix for special handling
        if col.lower().endswith('_calc'):
            # These will be shown in comparison charts
            continue

        # Force a clean slate for each new plot to avoid interference
        plt.clear_figure()
        plt.clear_data()

        # Generate a random color for this indicator
        color = get_random_color()  # Use random color generation for each chart

        # Set up this specific plot with clean settings
        print(f"\n📈 Indicator: {col}")
        plt.canvas_color("black")
        plt.axes_color("black")
        plt.ticks_color("yellow")
        plt.title(f"Indicator: {col}")

        # Log what we're attempting to use
        print(f"Plotting indicator with color={color}, marker={marker}")

        # Clean data for plotting
        x_clean, y_clean, num_removed = clean_data_for_plotting(df, col, x_data)
        
        if len(y_clean) == 0:
            print(f"⚠️  Skipping indicator '{col}' - no valid finite data")
            continue

        if num_removed > 0:
            print(f"ℹ️  Cleaned {num_removed} non-finite values from '{col}'")

        # Check if there's a calculated version of this column
        calc_col = f"{col.lower()}_calc"
        has_calc_version = calc_col in df.columns

        # Add source indicator to the label
        source_label = "📁 [LOADED]" if not col.lower().endswith("_calc") else "🧮 [CALCULATED]"

        # Plot just this one indicator with random color and braille marker
        plt.plot(x_clean, y_clean, label=f"{col} {source_label}", marker=marker, color=color)

        # If we have both original and calculated versions, plot them together for comparison
        if has_calc_version:
            x_calc, y_calc, num_removed_calc = clean_data_for_plotting(df, calc_col, x_data)
            if len(y_calc) > 0:
                # Use a different color for calculated version
                calc_color = get_random_color()
                while calc_color == color:  # Ensure different color
                    calc_color = get_random_color()
                plt.plot(x_calc, y_calc, label=f"{calc_col} 🧮 [CALCULATED]", marker=marker, color=calc_color)
                plt.title(f"Comparison: {col} (Original vs Calculated)")

        # Add a title that includes the color name for verification
        if not has_calc_version:
            plt.title(f"Indicator: {col} (Color: {color})")

        # Show special style for even/odd indicators for better visual distinction
        if idx % 2 == 0:
            # For even indexes, add a zero reference line
            min_val = min(y_clean) if y_clean else 0
            max_val = max(y_clean) if y_clean else 1
            mid_val = (min_val + max_val) / 2
            # Using only supported parameters (color) with same random color
            plt.horizontal_line(mid_val, color=color)

        plt.xlabel("Time")
        plt.ylabel(f"Value: {col}")
        plt.show()
