# src/plotting/term_auto_plot.py
"""
Terminal auto plotting for AUTO rule mode.
Displays each column in a parquet file as a separate chart in the terminal.
Especially useful for Docker environments where only terminal visualization works.
"""
import pandas as pd
import plotext as plt
import os

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

    # Plot OHLC data
    plt.clear_data()
    print("\n📈 OHLC Chart")
    plt.canvas_color("black")  # Set the background color to black for better contrast
    plt.axes_color("white")    # Set axes color to white
    plt.ticks_color("white")   # Set tick marks color to white
    for col in ohlc_cols:
        plt.plot(x_data, df[col].tolist(), label=col, marker="braille", color="cyan")
    plt.title("OHLC")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.show()

    # Plot Volume
    if volume_col:
        plt.clear_data()
        print("\n📊 Volume Chart")
        plt.canvas_color("black")  # Set the background color to black for better contrast
        plt.axes_color("white")    # Set axes color to white
        plt.ticks_color("white")   # Set tick marks color to white
        plt.bar(x_data, df[volume_col].tolist(), label="Volume", color="magenta")
        plt.title("Volume")
        plt.xlabel("Time")
        plt.ylabel("Volume")
        plt.show()

    # Plot indicators based on the rule
    if rule.upper() == "AUTO":
        # Define unique colors for different plots
        colors = ["yellow", "green", "red", "cyan", "magenta", "blue", "white"]

        for col in indicator_cols:
            # Skip columns that are all NaN or empty
            if df[col].isna().all() or df[col].empty:
                print(f"\n⚠️  Skipping indicator '{col}' - no valid data")
                continue
                
            plt.clear_data()
            print(f"\n📈 Indicator: {col}")
            plt.canvas_color("black")    # Black background for better contrast
            plt.axes_color("yellow")     # Yellow axes for better visibility
            plt.ticks_color("cyan")      # Cyan tick marks for better visibility
            plt.label_color("magenta")   # Magenta labels for better visibility

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
                
            plt.plot(x_data_filtered, y_data_filtered, label=col, marker="braille", color=colors[hash(col) % len(colors)])
            plt.title(col)
            plt.xlabel("Time")
            plt.ylabel("Value")
            plt.show()
    elif rule.upper() in ["PHLD", "PV", "SR"]:
        # Define unique colors for different plots if not defined earlier
        if 'colors' not in locals():
            colors = ["yellow", "green", "red", "cyan", "magenta", "blue", "white"]

        relevant_cols = [col for col in indicator_cols if rule.lower() in col.lower()]
        for col in relevant_cols:
            # Skip columns that are all NaN or empty
            if df[col].isna().all() or df[col].empty:
                print(f"\n⚠️  Skipping indicator '{col}' - no valid data")
                continue
                
            plt.clear_data()
            print(f"\n📈 Rule {rule}: {col}")
            plt.canvas_color("black")     # Black background for better contrast
            plt.axes_color("yellow")      # Yellow axes for better visibility
            plt.ticks_color("cyan")       # Cyan tick marks for better visibility
            plt.label_color("magenta")    # Magenta labels for better visibility

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
                
            plt.plot(x_data_filtered, y_data_filtered, label=col, marker="braille")
            plt.title(f"{rule} - {col}")
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

    # Define unique colors for different plots
    colors = ["yellow", "green", "red", "cyan", "magenta", "blue", "white"]

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
    plt.clear_data()
    print("\n📈 OHLC Chart")
    plt.canvas_color("black")  # Set the background color to black for better contrast
    plt.axes_color("white")    # Set axes color to white
    plt.ticks_color("white")   # Set tick marks color to white
    for col in ohlc_cols:
        plt.plot(x_data, df[col].tolist(), label=col, marker="braille", color="cyan")
    plt.title("OHLC")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.show()

    # Plot Volume
    if volume_col:
        plt.clear_data()
        print("\n📊 Volume Chart")
        plt.canvas_color("black")  # Set the background color to black for better contrast
        plt.axes_color("white")    # Set axes color to white
        plt.ticks_color("white")   # Set tick marks color to white
        plt.bar(x_data, df[volume_col].tolist(), label="Volume", color="magenta")
        plt.title("Volume")
        plt.xlabel("Time")
        plt.ylabel("Volume")
        plt.show()

    # Plot indicators
    for col in indicator_cols:
        # Skip columns that are all NaN or empty
        if df[col].isna().all() or df[col].empty:
            print(f"\n⚠️  Skipping indicator '{col}' - no valid data")
            continue
            
        plt.clear_data()
        print(f"\n📈 Indicator: {col}")
        plt.canvas_color("black")  # Set the background color to black for better contrast
        plt.axes_color("white")    # Set axes color to white
        plt.ticks_color("white")   # Set tick marks color to white

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
            
        plt.plot(x_data_filtered, y_data_filtered, label=col, marker="braille", color=colors[hash(col) % len(colors)])
        plt.title(col)
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.show()
