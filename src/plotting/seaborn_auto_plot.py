import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

def auto_plot_from_parquet(parquet_path: str, plot_title: str = "Auto Plot from Parquet"):
    if not os.path.exists(parquet_path):
        print(f"File not found: {parquet_path}")
        return

    df = pd.read_parquet(parquet_path)
    if df.empty:
        print("Empty DataFrame.")
        return

    # Determining OHLC columns, volume, and time columns
    ohlc_cols = [col for col in df.columns if col.lower() in ["open", "high", "low", "close"]]
    volume_col = next((col for col in df.columns if col.lower() == "volume"), None)
    time_col = next((col for col in df.columns if col.lower() in ["timestamp", "datetime", "date", "time"]), None)

    # Other indicator columns
    exclude = set(ohlc_cols + ([volume_col] if volume_col else []) + ([time_col] if time_col else []))
    indicator_cols = [col for col in df.columns if col not in exclude]

    # --- COLOR MAP ---
    color_map = {
        'PV': 'orange',
        'pressure_vector': 'orange',
        'HL': 'brown',
        'Pressure': 'dodgerblue',
        'pressure': 'dodgerblue',
        'predicted_high': 'red',
        'predicted_low': 'green',
        'Volume': 'gray'
    }

    n_panels = 2 + len(indicator_cols)  # OHLC, Volume, indicators
    fig, axes = plt.subplots(
        n_panels, 1, sharex=True, figsize=(14, 3 * n_panels),
        gridspec_kw={'height_ratios': [2, 1] + [1]*len(indicator_cols)}
    )
    axes = np.atleast_1d(axes).flatten().tolist()

    # OHLC Chart
    ax_ohlc = axes[0]
    if time_col:
        x = df[time_col]
    else:
        x = df.index
    for col in ohlc_cols:
        ax_ohlc.plot(x, df[col], label=col)
    ax_ohlc.set_ylabel("OHLC")
    ax_ohlc.legend()
    ax_ohlc.set_title(plot_title)

    # Volume
    ax_vol = axes[1]
    if volume_col:
        ax_vol.bar(x, df[volume_col], color='gray', alpha=0.5)
        ax_vol.set_ylabel("Volume")
    else:
        ax_vol.set_visible(False)

    # Indicators
    for i, col in enumerate(indicator_cols):
        ax = axes[2 + i]
        line_color = color_map.get(col, 'purple')
        print(f"Seaborn auto plot: Plotting {col} with color {line_color}")
        sns.lineplot(x=x, y=df[col], ax=ax, color=line_color)
        ax.set_ylabel(col)
        ax.set_title(col)

    plt.tight_layout()
    # Use plt.close() instead of plt.show() to avoid non-interactive warning in test environment
    plt.close()

