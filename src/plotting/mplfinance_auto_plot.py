import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mplfinance as mpf

# Function to plot OHLCV and all other columns from a parquet file in a multi-panel figure
# Main chart: candlesticks (open, high, low, close), below: volume, below: all other columns as lines

def auto_plot_from_parquet(parquet_path):
    """
    Reads a parquet file, plots OHLCV as candlesticks on the main panel, volume below, and all other columns as lines on the lowest panel.
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

    # Find all other columns to plot
    exclude_cols = set(ohlc_cols + ['volume', 'timestamp', 'datetime', 'date', 'time'])
    other_cols = [col for col in df.columns if col.lower() not in exclude_cols]

    # Set up the figure with 3 rows (main, volume, others)
    nrows = 3 if other_cols else 2
    fig = plt.figure(figsize=(14, 7 if nrows == 2 else 10))
    gs = gridspec.GridSpec(nrows, 1, height_ratios=[3, 1] + ([1] if nrows == 3 else []))

    # Main panel: candlesticks
    ax_main = fig.add_subplot(gs[0])
    if ohlc_df is not None:
        mpf.plot(ohlc_df, type='candle', ax=ax_main, volume=False, show_nontrading=True)
        ax_main.set_title('OHLC Candlestick Chart')
    else:
        ax_main.plot(df.index, df[df.columns[0]], label=df.columns[0])
        ax_main.set_title('Main Chart')
    ax_main.legend()

    # Volume panel
    ax_vol = fig.add_subplot(gs[1], sharex=ax_main)
    if vol_df is not None:
        ax_vol.bar(vol_df.index, vol_df[vol_df.columns[0]], color='gray', width=0.8)
        ax_vol.set_ylabel('Volume')
    else:
        ax_vol.set_visible(False)

    # Other columns panel
    if nrows == 3:
        ax_other = fig.add_subplot(gs[2], sharex=ax_main)
        for col in other_cols:
            ax_other.plot(df.index, df[col], label=col)
        ax_other.set_ylabel('Other')
        ax_other.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

