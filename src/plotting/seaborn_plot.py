import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_indicator_results_seaborn(
    df: pd.DataFrame,
    selected_rule,
    plot_title: str = ""
):
    # ...existing code up to sns.set...
    if df is None or df.empty:
        print("No data to plot.")
        return

    # Try to find a column similar to 'close' if it's missing
    close_col = None
    for col in df.columns:
        if col.lower() == 'close':
            close_col = col
            break
    if close_col is None:
        # Try common alternatives
        for alt in ['Close', 'CLOSE', 'closing_price', 'price']:
            if alt in df.columns:
                close_col = alt
                break

    if close_col is None:
        print("Error: 'close' column not found in DataFrame.")
        print("Available columns:", list(df.columns))
        print("DataFrame head:\n", df.head())
        return

    sns.set(style="darkgrid", context="talk")
    fig, ax = plt.subplots(figsize=(16, 7))

    # Plot open, high, low, close
    if 'open' in df.columns:
        ax.plot(df.index, df['open'], label='Open', color='orange', linewidth=1, alpha=0.7)
    if 'high' in df.columns:
        ax.plot(df.index, df['high'], label='High', color='purple', linewidth=1, alpha=0.7)
    if 'low' in df.columns:
        ax.plot(df.index, df['low'], label='Low', color='brown', linewidth=1, alpha=0.7)
    ax.plot(df.index, df[close_col], label='Close', color='blue', linewidth=1.2)

    # Plot predicted_high and predicted_low if present
    if 'predicted_high' in df.columns:
        ax.plot(df.index, df['predicted_high'], label='Predicted High', color='lime', linestyle='--', linewidth=1.2)
    if 'predicted_low' in df.columns:
        ax.plot(df.index, df['predicted_low'], label='Predicted Low', color='red', linestyle='--', linewidth=1.2)

    # Plot predicted_direction as markers/arrows if present
    if 'predicted_direction' in df.columns:
        up_idx = df[df['predicted_direction'] > 0].index
        down_idx = df[df['predicted_direction'] < 0].index
        ax.scatter(up_idx, df.loc[up_idx, close_col], marker='^', color='deepskyblue', s=60, label='Predicted Up')
        ax.scatter(down_idx, df.loc[down_idx, close_col], marker='v', color='darkred', s=60, label='Predicted Down')

    # Plot buy/sell signals if present
    if 'signal' in df.columns:
        buy_signals = df[df['signal'] > 0]
        sell_signals = df[df['signal'] < 0]
        ax.scatter(buy_signals.index, buy_signals[close_col], marker='o', color='green', s=80, label='Buy Signal')
        ax.scatter(sell_signals.index, sell_signals[close_col], marker='x', color='red', s=80, label='Sell Signal')

    # Optionally plot volume
    if 'volume' in df.columns:
        ax2 = ax.twinx()
        ax2.bar(df.index, df['volume'], color='gray', alpha=0.2, width=1, label='Volume')
        ax2.set_ylabel('Volume', fontsize=11)
        ax2.set_yticks([])

    ax.set_title(plot_title or "Seaborn Plot", fontsize=16)
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left', fontsize=10)
    plt.tight_layout()
    plt.show()
