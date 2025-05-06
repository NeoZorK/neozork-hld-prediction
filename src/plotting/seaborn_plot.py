import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_indicator_results_seaborn(
    df: pd.DataFrame,
    selected_rule,
    plot_title: str = ""
):
    """
    Plots OHLCV data and trading signals using seaborn/matplotlib.

    Args:
        df (pd.DataFrame): DataFrame with OHLCV and signal columns.
        selected_rule: TradingRule enum or similar (for legend/labels).
        plot_title (str): Title for the plot.
    """
    if df is None or df.empty:
        print("No data to plot.")
        return

    sns.set(style="darkgrid", context="talk")
    fig, ax = plt.subplots(figsize=(16, 7))

    # Plot close price
    ax.plot(df.index, df['close'], label='Close', color='blue', linewidth=1.2)

    # Plot buy/sell signals if present
    if 'signal' in df.columns:
        buy_signals = df[df['signal'] > 0]
        sell_signals = df[df['signal'] < 0]
        ax.scatter(buy_signals.index, buy_signals['close'], marker='^', color='green', s=80, label='Buy Signal')
        ax.scatter(sell_signals.index, sell_signals['close'], marker='v', color='red', s=80, label='Sell Signal')

    # Optionally plot volume
    if 'volume' in df.columns:
        ax2 = ax.twinx()
        ax2.bar(df.index, df['volume'], color='gray', alpha=0.2, width=1, label='Volume')
        ax2.set_ylabel('Volume', fontsize=11)
        ax2.set_yticks([])

    ax.set_title(plot_title or "Seaborn Plot", fontsize=16)
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.tight_layout()
    plt.show()
