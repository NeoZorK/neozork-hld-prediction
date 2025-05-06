import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import mplcursors

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
        for alt in ['Close', 'CLOSE', 'closing_price', 'price']:
            if alt in df.columns:
                close_col = alt
                break
    if close_col is None:
        print("Error: 'close' column not found in DataFrame.")
        print("Available columns:", list(df.columns))
        print("DataFrame head:\n", df.head())
        return

    # --- Prepare subplots: 1. OHLC + signals, 2. Volume, 3. PV, 4. HL, 5. Pressure ---
    nrows = 1
    indicator_panels = []
    if 'Volume' in df.columns:
        indicator_panels.append('Volume')
    if 'PV' in df.columns:
        indicator_panels.append('PV')
    if 'HL' in df.columns:
        indicator_panels.append('HL')
    if 'Pressure' in df.columns:
        indicator_panels.append('Pressure')
    nrows += len(indicator_panels)

    sns.set(style="darkgrid", context="talk")
    fig, axes = plt.subplots(nrows=nrows, ncols=1, figsize=(18, 3.5 * nrows), sharex=True, gridspec_kw={'height_ratios': [2] + [1]*(nrows-1)})

    if nrows == 1:
        axes = [axes]

    # --- Panel 1: OHLC + predicted + signals ---
    ax = axes[0]
    idx = df.index

    # Plot OHLC as lines (not candlestick, for simplicity)
    if 'Open' in df.columns and 'High' in df.columns and 'Low' in df.columns and 'Close' in df.columns:
        open_line, = ax.plot(idx, df['Open'], label='Open', color='orange', linewidth=1, alpha=0.7)
        high_line, = ax.plot(idx, df['High'], label='High', color='purple', linewidth=1, alpha=0.7)
        low_line, = ax.plot(idx, df['Low'], label='Low', color='brown', linewidth=1, alpha=0.7)
        close_line, = ax.plot(idx, df['Close'], label='Close', color='blue', linewidth=1.5, zorder=10)
    else:
        close_line, = ax.plot(idx, df[close_col], label='Close', color='blue', linewidth=1.5, zorder=10)

    # Plot predicted high/low if present (PPrice1/PPrice2 or predicted_high/predicted_low)
    if 'PPrice1' in df.columns:
        pprice1_line, = ax.plot(idx, df['PPrice1'], label='Predicted Low (PPrice1)', color='lime', linestyle='--', linewidth=1.5)
    if 'PPrice2' in df.columns:
        pprice2_line, = ax.plot(idx, df['PPrice2'], label='Predicted High (PPrice2)', color='red', linestyle='--', linewidth=1.5)
    if 'predicted_low' in df.columns:
        predicted_low_line, = ax.plot(idx, df['predicted_low'], label='Predicted Low', color='lime', linestyle='--', linewidth=1.5)
    if 'predicted_high' in df.columns:
        predicted_high_line, = ax.plot(idx, df['predicted_high'], label='Predicted High', color='red', linestyle='--', linewidth=1.5)

    # Plot predicted_direction or Direction as markers
    direction_col = None
    for dcol in ['Direction', 'predicted_direction']:
        if dcol in df.columns:
            direction_col = dcol
            break
    if direction_col is not None:
        # For compatibility with plotly/fastest: 1=BUY, 2=SELL
        buy_mask = (df[direction_col] == 1) | (df[direction_col] > 0)
        sell_mask = (df[direction_col] == 2) | (df[direction_col] < 0)
        if 'Low' in df.columns:
            buy_y = df['Low'] * 0.998
        else:
            buy_y = df[close_col]
        if 'High' in df.columns:
            sell_y = df['High'] * 1.002
        else:
            sell_y = df[close_col]
        buy_scatter = ax.scatter(df.index[buy_mask], buy_y[buy_mask], marker='^', color='lime', s=80, label='Predicted UP', zorder=20)
        sell_scatter = ax.scatter(df.index[sell_mask], sell_y[sell_mask], marker='v', color='red', s=80, label='Predicted DOWN', zorder=20)

    # Plot buy/sell signals if present
    if 'signal' in df.columns:
        buy_signals = df[df['signal'] > 0]
        sell_signals = df[df['signal'] < 0]
        buy_signal_scatter = ax.scatter(buy_signals.index, buy_signals[close_col], marker='o', color='green', s=80, label='Buy Signal', zorder=30)
        sell_signal_scatter = ax.scatter(sell_signals.index, sell_signals[close_col], marker='x', color='red', s=80, label='Sell Signal', zorder=30)

    ax.set_ylabel("Price")
    ax.set_title(f"{plot_title or 'Seaborn Plot'} - Rule: {getattr(selected_rule, 'name', selected_rule)}")
    ax.legend(loc='upper left', fontsize=9, ncol=2)

    # --- Additional panels: Volume, PV, HL, Pressure ---
    panel_idx = 1
    for panel in indicator_panels:
        ax_panel = axes[panel_idx]
        if panel == 'Volume':
            volume_bars = ax_panel.bar(idx, df['Volume'], color='gray', alpha=0.3, width=1, label='Volume')
            ax_panel.set_ylabel('Volume')
        elif panel == 'PV':
            pv_line, = ax_panel.plot(idx, df['PV'], color='orange', label='PV')
            ax_panel.axhline(0, color='gray', linestyle='--', linewidth=1)
            ax_panel.set_ylabel('PV')
        elif panel == 'HL':
            hl_line, = ax_panel.plot(idx, df['HL'], color='brown', label='HL (Points)')
            ax_panel.set_ylabel('HL')
        elif panel == 'Pressure':
            pressure_line, = ax_panel.plot(idx, df['Pressure'], color='dodgerblue', label='Pressure')
            ax_panel.axhline(0, color='gray', linestyle='--', linewidth=1)
            ax_panel.set_ylabel('Pressure')
        ax_panel.legend(loc='upper left', fontsize=9)
        panel_idx += 1

    axes[-1].set_xlabel("Time")

    # --- Add interactive cursors ---
    mplcursors.cursor(axes, hover=True)

    plt.tight_layout()
    plt.show()
