import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_indicator_results_seaborn(
    df: pd.DataFrame,
    selected_rule,
    plot_title: str = ""
):
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

    # Plot all numeric columns except volume and signal as lines
    exclude_cols = {'volume', 'signal', 'predicted_direction'}
    color_cycle = plt.cm.tab10.colors
    color_map = {}
    i = 0
    for col in df.columns:
        if col in exclude_cols or not pd.api.types.is_numeric_dtype(df[col]):
            continue
        if col == close_col:
            color_map[col] = 'blue'
            ax.plot(df.index, df[col], label='Close', color='blue', linewidth=1.5, zorder=10)
        else:
            color_map[col] = color_cycle[i % len(color_cycle)]
            ax.plot(df.index, df[col], label=col.replace('_', ' ').title(), color=color_map[col], linewidth=1, alpha=0.8)
            i += 1

    # Plot predicted_direction as markers/arrows if present
    if 'predicted_direction' in df.columns:
        up_idx = df[df['predicted_direction'] > 0].index
        down_idx = df[df['predicted_direction'] < 0].index
        ax.scatter(up_idx, df.loc[up_idx, close_col], marker='^', color='deepskyblue', s=60, label='Predicted Up', zorder=20)
        ax.scatter(down_idx, df.loc[down_idx, close_col], marker='v', color='darkred', s=60, label='Predicted Down', zorder=20)

    # Plot buy/sell signals if present
    if 'signal' in df.columns:
        buy_signals = df[df['signal'] > 0]
        sell_signals = df[df['signal'] < 0]
        ax.scatter(buy_signals.index, buy_signals[close_col], marker='o', color='green', s=80, label='Buy Signal', zorder=30)
        ax.scatter(sell_signals.index, sell_signals[close_col], marker='x', color='red', s=80, label='Sell Signal', zorder=30)

    # Optionally plot volume
    if 'volume' in df.columns:
        ax2 = ax.twinx()
        ax2.bar(df.index, df['volume'], color='gray', alpha=0.2, width=1, label='Volume')
        ax2.set_ylabel('Volume', fontsize=11)
        ax2.set_yticks([])

    # Avoid duplicate labels in legend
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    ax.legend(unique.values(), unique.keys(), loc='upper left', fontsize=10, frameon=True)

    rule_name = str(selected_rule) if selected_rule is not None else ""
    title = plot_title or f"Seaborn Plot - {rule_name}"
    ax.set_title(title, fontsize=16)
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    plt.tight_layout()
    plt.show()
