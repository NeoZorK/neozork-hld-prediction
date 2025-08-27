import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mplfinance as mpf

# Function to plot OHLCV and all other columns from a parquet file in a multi-panel figure
# Main chart: candlesticks (open, high, low, close), below: volume, below: each other column as a separate subplot

def auto_plot_from_parquet(parquet_path):
    """
    Reads a parquet file, plots OHLCV as candlesticks on the main panel (smaller), volume below, and each other column as a separate subplot below.
    """
    df = pd.read_parquet(parquet_path)

    # Normalize column names to lower for exclusion
    cols_lower = [col.lower() for col in df.columns]
    col_map = {col.lower(): col for col in df.columns}

    # Identify OHLCV columns
    ohlc_cols = ['open', 'high', 'low', 'close']
    volume_col = 'volume' if 'volume' in cols_lower else None
    datetime_col = None
    for candidate in ['datetime', 'timestamp', 'date', 'time']:
        if candidate in cols_lower:
            datetime_col = col_map[candidate]
            break

    # Set datetime as index if present
    if datetime_col:
        df[datetime_col] = pd.to_datetime(df[datetime_col], errors='coerce')
        df = df.set_index(datetime_col)

    # Prepare OHLCV DataFrame for mplfinance
    ohlc_df = df[[col_map[c] for c in ohlc_cols if c in cols_lower]].copy() if all(c in cols_lower for c in ohlc_cols) else None
    if ohlc_df is not None:
        ohlc_df.columns = [c.capitalize() for c in ohlc_df.columns]
    vol_df = df[[col_map['volume']]] if volume_col else None

    # Find all other columns to plot as separate subplots
    exclude_cols = set(ohlc_cols + ['volume', 'timestamp', 'datetime', 'date', 'time'])
    other_cols = [col for col in df.columns if col.lower() not in exclude_cols]

    n_other = len(other_cols)
    nrows = 2 + n_other  # 1 for candlestick, 1 for volume, rest for each other column
    height_ratios = [1, 1] + [1]*n_other  # Make candlestick smaller
    fig = plt.figure(figsize=(14, 3 + 2*nrows))
    gs = gridspec.GridSpec(nrows, 1, height_ratios=height_ratios)

    # Main panel: candlesticks
    ax_main = fig.add_subplot(gs[0])
    if ohlc_df is not None:
        mpf.plot(ohlc_df, type='candle', ax=ax_main, volume=False, show_nontrading=True)
        ax_main.set_title('OHLC Candlestick Chart')
    else:
        ax_main.plot(df.index, df[df.columns[0]], label=df.columns[0])
        ax_main.set_title('Main Chart')
    if ax_main.get_legend_handles_labels()[0]:  # Check if there are legend handles
        ax_main.legend()

    # Volume panel
    ax_vol = fig.add_subplot(gs[1], sharex=ax_main)
    if vol_df is not None:
        ax_vol.bar(vol_df.index, vol_df[vol_df.columns[0]], color='gray', width=0.8)
        ax_vol.set_ylabel('Volume')
    else:
        ax_vol.set_visible(False)

    # Other columns: each as a separate subplot
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key().get('color', [])
    for i, col in enumerate(other_cols):
        ax = fig.add_subplot(gs[2 + i], sharex=ax_main)
        color = color_cycle[i % len(color_cycle)] if color_cycle else None
        ax.plot(df.index, df[col], label=col, color=color, linewidth=2)
        ax.set_ylabel(col)
        if ax.get_legend_handles_labels()[0]:  # Check if there are legend handles
            ax.legend(loc='upper right')

    plt.tight_layout()
    # Use plt.close() instead of plt.show() to avoid non-interactive warning in test environment
    try:
        plt.show()
    except Exception:
        plt.close()

