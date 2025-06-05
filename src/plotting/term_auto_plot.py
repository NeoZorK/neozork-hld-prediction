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

    # Other indicator columns
    exclude = set(ohlc_cols + ([volume_col] if volume_col else []) + ([time_col] if time_col else []))
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
            plt.plot(x_clean, y_clean, label=col, marker="braille", color=color)

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
            plt.bar(x_clean, y_clean, label="Volume", color="bright_magenta")
            plt.xlabel("Time")
            plt.ylabel("Volume")
            plt.show()

    # Define colors and markers for separate indicator plots
    # These colors are well-supported in terminal environments
    basic_colors = [
        "bright_red", "bright_green", "bright_yellow", "bright_blue",
        "bright_magenta", "bright_cyan", "bright_white",
        "red", "green", "yellow", "blue", "magenta", "cyan", "white"
    ]

    # Define diverse markers
    # Use only braille markers for all plots for consistency
    markers = ["braille"]

    # For each indicator, create a standalone plot with its own color
    for idx, col in enumerate(indicator_cols):
        # Force a clean slate for each new plot to avoid interference
        plt.clear_figure()
        plt.clear_data()

        # Explicitly select a color for this indicator from basic_colors
        color_idx = idx % len(basic_colors)
        color = basic_colors[color_idx]
        # Always use braille marker for consistency
        marker = "braille"

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

        # Plot just this one indicator
        plt.plot(x_clean, y_clean, label=col, marker=marker, color=color)

        # Add a title that includes the color name for verification
        plt.title(f"Indicator: {col} (Color: {color})")

        # Show special style for even/odd indicators for better visual distinction
        if idx % 2 == 0:
            # For even indexes, add a zero reference line
            min_val = min(y_clean) if y_clean else 0
            max_val = max(y_clean) if y_clean else 1
            mid_val = (min_val + max_val) / 2
            # Using only supported parameters (color) without style
            plt.horizontal_line(mid_val, color=color)

        plt.xlabel("Time")
        plt.ylabel(f"Value: {col}")
        plt.show()
