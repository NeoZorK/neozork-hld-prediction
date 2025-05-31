import pandas as pd
import matplotlib.pyplot as plt
import os

# Function to plot all columns except OHLCV and timestamp/datetime from a parquet file
def auto_plot_from_parquet(parquet_path):
    """
    Reads a parquet file, finds all columns except open, high, low, close, volume, timestamp/datetime,
    and creates a separate plot for each of these columns.
    """
    # Read the parquet file into a DataFrame
    df = pd.read_parquet(parquet_path)

    # Define columns to exclude from plotting
    exclude_cols = {'open', 'high', 'low', 'close', 'volume', 'timestamp', 'datetime'}

    # Find columns to plot
    columns_to_plot = [col for col in df.columns if col.lower() not in exclude_cols]

    # Create a plot for each column
    for col in columns_to_plot:
        plt.figure(figsize=(10, 4))
        plt.plot(df[col], label=col)
        plt.title(f"{col} over index")
        plt.xlabel("Index")
        plt.ylabel(col)
        plt.legend()
        plt.tight_layout()
        # Show the plot (or save if needed)
        plt.show()

