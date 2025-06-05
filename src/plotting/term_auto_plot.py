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
    plt.figure_color("black")        # Set figure background to black
    # Grid removed as requested
    plt.title(title)


# Helper function to generate random terminal colors
def get_random_color():
    """
    Generate a random color for terminal plotting.

    Returns:
        A random color name from plotext available colors
    """
    # List of available plotext colors for better visibility in terminal
    available_colors = [
        "bright_red", "bright_yellow", "bright_green", "bright_cyan",
        "bright_blue", "bright_magenta", "bright_white",
        "red", "yellow", "green", "cyan", "blue", "magenta", "white",
        "orange", "purple", "pink", "lime", "peach", "olive", "teal"
    ]
    return random.choice(available_colors)

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
        "open": "bright_green",   # Bright green for open price
        "high": "bright_cyan",    # Bright cyan for high price
        "low": "bright_red",      # Bright red for low price
        "close": "bright_yellow"  # Bright yellow for close price
    }

    # Use thicker lines and different markers for better distinction
    markers = {
        "open": "hd",     # Horizontal dash marker for open
        "high": "braille", # Braille marker for high
        "low": "braille",  # Braille marker for low
        "close": "sd"     # Small dot marker for close
    }

    for col in ohlc_cols:
        col_lower = col.lower()
        color = ohlc_colors.get(col_lower, "bright_white")  # Default to bright white if not found
        marker = markers.get(col_lower, "braille")          # Default to braille if not found
        plt.plot(x_data, df[col].tolist(), label=col, marker=marker, color=color)
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.show()

    # Plot Volume
    if volume_col:
        plt.clear_data()
        print("\n📊 Volume Chart")
        set_terminal_chart_style("Volume Chart")
        plt.bar(x_data, df[volume_col].tolist(), label="Volume", color="bright_magenta")
        plt.xlabel("Time")
        plt.ylabel("Volume")
        plt.show()

    # Plot indicators based on the rule
    if rule.upper() == "AUTO":
        for col in indicator_cols:
            # Skip columns that are all NaN or empty
            if df[col].isna().all() or df[col].empty:
                print(f"\n⚠️  Skipping indicator '{col}' - no valid data")
                continue
                
            plt.clear_data()
            print(f"\n📈 Indicator: {col}")
            set_terminal_chart_style(f"Indicator: {col}")

            # Filter out NaN values for plotting
            valid_mask = ~df[col].isna()
            if not valid_mask.any():
                print(f"⚠️  No valid data points for {col}")
                continue
                
            x_data_filtered = [x_data[i] for i in range(len(x_data)) if valid_mask.iloc[i]]
            y_data_filtered = df[col].dropna().tolist()
            
            if len(y_data_filtered) == 0:
                print(f"⚠️  No valid data points for {col}")
                continue
                
            # Use random color for each column
            plt.plot(x_data_filtered, y_data_filtered, label=col, marker="braille", color=get_random_color())
            plt.xlabel("Time")
            plt.ylabel("Value")
            plt.show()
    elif rule.upper() in ["PHLD", "PV", "SR"]:
        relevant_cols = [col for col in indicator_cols if rule.lower() in col.lower()]
        for idx, col in enumerate(relevant_cols):
            # Skip columns that are all NaN or empty
            if df[col].isna().all() or df[col].empty:
                print(f"\n⚠️  Skipping indicator '{col}' - no valid data")
                continue
                
            plt.clear_data()
            print(f"\n📈 Rule {rule}: {col}")
            set_terminal_chart_style(f"Rule {rule}: {col}")

            # Filter out NaN values for plotting
            valid_mask = ~df[col].isna()
            if not valid_mask.any():
                print(f"⚠️  No valid data points for {col}")
                continue
                
            x_data_filtered = [x_data[i] for i in range(len(x_data)) if valid_mask.iloc[i]]
            y_data_filtered = df[col].dropna().tolist()
            
            if len(y_data_filtered) == 0:
                print(f"⚠️  No valid data points for {col}")
                continue
                
            # Use a unique color for each column based on its index or hash
            color = rainbow_colors[idx % len(rainbow_colors)] if idx < len(rainbow_colors) else rainbow_colors[hash(col) % len(rainbow_colors)]
            plt.plot(x_data_filtered, y_data_filtered, label=col, marker="braille", color=color)
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
    plt.theme("dark")  # Use dark theme for better visibility in terminal

    # Define color palette for all charts - rainbow colors for better visibility
    rainbow_colors = [
        "bright_red", "bright_yellow", "bright_green", "bright_cyan",
        "bright_blue", "bright_magenta", "bright_white",
        "red", "yellow", "green", "cyan", "blue", "magenta", "white"
    ]

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

    # Plot OHLC data
    if ohlc_cols:
        plt.clear_data()
        print("\n📈 OHLC Chart")
        set_terminal_chart_style("OHLC Chart")

        # Use different colors for each OHLC component with maximum contrast
        ohlc_colors = {
            "open": "bright_green",   # Bright green for open price
            "high": "bright_cyan",    # Bright cyan for high price
            "low": "bright_red",      # Bright red for low price
            "close": "bright_yellow"  # Bright yellow for close price
        }

        # Use different markers for better distinction
        markers = {
            "open": "hd",      # Horizontal dash marker for open
            "high": "braille", # Braille marker for high
            "low": "braille",  # Braille marker for low
            "close": "sd"      # Small dot marker for close
        }

        for col in ohlc_cols:
            col_lower = col.lower()
            color = ohlc_colors.get(col_lower, "bright_white")  # Default to bright white if not found
            marker = markers.get(col_lower, "braille")          # Default to braille if not found
            plt.plot(x_data, df[col].tolist(), label=col, marker=marker, color=color)
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.show()

    # Plot Volume
    if volume_col:
        plt.clear_data()
        print("\n📊 Volume Chart")
        set_terminal_chart_style("Volume Chart")
        plt.bar(x_data, df[volume_col].tolist(), label="Volume", color="bright_magenta")
        plt.xlabel("Time")
        plt.ylabel("Volume")
        plt.show()

    # Plot indicators
    for idx, col in enumerate(indicator_cols):
        # Skip columns that are all NaN or empty
        if df[col].isna().all() or df[col].empty:
            print(f"\n⚠️  Skipping indicator '{col}' - no valid data")
            continue
            
        plt.clear_data()
        print(f"\n📈 Indicator: {col}")
        set_terminal_chart_style(f"Indicator: {col}")

        # Filter out NaN values for plotting
        valid_mask = ~df[col].isna()
        if not valid_mask.any():
            print(f"⚠️  No valid data points for {col}")
            continue
            
        x_data_filtered = [x_data[i] for i in range(len(x_data)) if valid_mask.iloc[i]]
        y_data_filtered = df[col].dropna().tolist()
        
        if len(y_data_filtered) == 0:
            print(f"⚠️  No valid data points for {col}")
            continue

        # Use random color for each indicator
        plt.plot(x_data_filtered, y_data_filtered, label=col, marker="braille", color=get_random_color())
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.show()
