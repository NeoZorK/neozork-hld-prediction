# -*- coding: utf-8 -*-
# src/plotting/seaborn_plot.py

"""
Plotting functions for visualizing indicator results using seaborn only (no direct matplotlib primitives).
Draws lineplots for OHLC and all available indicators, signals as colored markers, using modern seaborn style.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.patches import Rectangle
from ..common.constants import TradingRule
from ..common import logger

def plot_indicator_results_seaborn(
    df_results: pd.DataFrame,
    rule: TradingRule,
    title: str = "Indicator Results (Seaborn Lines)",
    **kwargs
):
    """
    Plots indicator results using only seaborn lineplots and scatterplots for a visually rich, modern look.

    Args:
        df_results (pd.DataFrame): Results dataframe (must include 'Open', 'High', 'Low', 'Close').
        rule (TradingRule): Trading rule used.
        title (str): Plot title.
        **kwargs: Additional keyword arguments (ignored).
    """
    required_cols = ['Open', 'High', 'Low', 'Close']
    if df_results is None or df_results.empty or not all(col in df_results.columns for col in required_cols):
        logger.print_warning("Input DataFrame is None, empty, or missing required columns. Cannot plot.")
        return

    # Convert index to DatetimeIndex if necessary
    if not isinstance(df_results.index, pd.DatetimeIndex):
        try:
            df_results = df_results.copy()
            df_results.index = pd.to_datetime(df_results.index)
        except Exception:
            logger.print_warning("Failed to convert index to DatetimeIndex for seaborn plotting.")
            return

    # Add a 'date' column (string) for seaborn barplot compatibility
    df_results = df_results.copy()
    df_results['date'] = df_results.index.strftime('%Y-%m-%d')

    # Use seaborn's dark theme, and tune matplotlib defaults for dark background
    sns.set_theme(style="darkgrid", palette="deep", context="talk")
    plt.rcParams.update({
        'axes.facecolor': '#13131a',
        'figure.facecolor': '#13131a',
        'axes.edgecolor': 'white',
        'axes.labelcolor': 'white',
        'xtick.color': 'white',
        'ytick.color': 'white',
        'text.color': 'white',
        'legend.edgecolor': 'white',
        'legend.facecolor': '#23232e',
        'axes.titlecolor': 'white',
        'figure.titlesize': 18
    })

    # Prepare subplots: main price, then for each additional indicator if present
    indicator_specs = [
        ("Volume", "bar", "gray"),
        ("PV", "line", "#ff9800"),
        ("HL", "line", "#8d6e63"),
        ("Pressure", "line", "#2196f3"),
    ]
    subplot_indicators = []
    for col, kind, color in indicator_specs:
        if col in df_results.columns and not df_results[col].isnull().all():
            subplot_indicators.append((col, kind, color))

    n_subplots = 1 + len(subplot_indicators)
    fig_height = 5 + 2 * len(subplot_indicators)
    fig, axes = plt.subplots(
        nrows=n_subplots,
        ncols=1,
        figsize=(16, fig_height),
        sharex=False,
        gridspec_kw={'height_ratios': [3]+[1]*len(subplot_indicators)}
    )

    if n_subplots == 1:
        axes = [axes]

    # --------- Gradient or solid black background ---------
    # Gradient: vertical from #23232e to #13131a
    def set_gradient_background(fig, ax_list, color_top='#23232e', color_bottom='#13131a'):
        # Create gradient background for the whole figure
        from matplotlib.transforms import Bbox
        from matplotlib.colors import to_rgb
        img = np.linspace(0, 1, 256).reshape(-1, 1)
        color_top_rgb = np.array(mcolors.to_rgb(color_top))
        color_bottom_rgb = np.array(mcolors.to_rgb(color_bottom))
        grad = img * color_bottom_rgb + (1 - img) * color_top_rgb
        grad = grad.reshape((256, 1, 3))
        fig.figimage(grad, xo=0, yo=0, origin='upper', zorder=0, alpha=1, resize=True)

    set_gradient_background(fig, axes)

    # --------- Title with trading rule ----------
    trading_rule_str = f"{rule.name}" if hasattr(rule, "name") else str(rule)
    full_title = f"{title} | Rule: {trading_rule_str}"
    fig.suptitle(full_title, fontsize=18, color="white", fontweight="bold", y=0.98)

    # ---------- Main plot (OHLC lines + signals) ----------
    ax = axes[0]
    ax.set_ylabel("Price", fontsize=13, color='white')
    ax.set_facecolor("none")

    # Plot OHLC as lines
    sns.lineplot(ax=ax, x=df_results.index, y='Open', data=df_results, label='Open', color='#90caf9', linewidth=2, alpha=0.8)
    sns.lineplot(ax=ax, x=df_results.index, y='High', data=df_results, label='High', color='#66bb6a', linewidth=2, alpha=0.7, linestyle="--")
    sns.lineplot(ax=ax, x=df_results.index, y='Low', data=df_results, label='Low', color='#ef5350', linewidth=2, alpha=0.7, linestyle="--")
    sns.lineplot(ax=ax, x=df_results.index, y='Close', data=df_results, label='Close', color='#ffa726', linewidth=2.5, alpha=0.95)

    # Predicted high/low as accent lines
    if "predicted_high" in df_results.columns:
        sns.lineplot(ax=ax, x=df_results.index, y='predicted_high', data=df_results, label='Predicted High', color='#f44336', linewidth=1.8, linestyle='dotted')
    if "predicted_low" in df_results.columns:
        sns.lineplot(ax=ax, x=df_results.index, y='predicted_low', data=df_results, label='Predicted Low', color='#43a047', linewidth=1.8, linestyle='dotted')

    # Predicted direction as colored markers
    if "predicted_direction" in df_results.columns:
        dirs = df_results["predicted_direction"].values
        up_idx = np.where(dirs > 0)[0]
        down_idx = np.where(dirs < 0)[0]
        if len(up_idx) > 0:
            sns.scatterplot(ax=ax, x=df_results.index[up_idx], y=df_results['Close'].values[up_idx],
                            marker="^", color="#00e676", s=110, edgecolor="white", label="Predicted Up", zorder=3)
        if len(down_idx) > 0:
            sns.scatterplot(ax=ax, x=df_results.index[down_idx], y=df_results['Close'].values[down_idx],
                            marker="v", color="#ff1744", s=110, edgecolor="white", label="Predicted Down", zorder=3)

    # BUY/SELL signals
    if "BUY" in df_results.columns:
        buy_idx = df_results.index[df_results["BUY"] == 1]
        if len(buy_idx) > 0:
            sns.scatterplot(ax=ax, x=buy_idx, y=df_results.loc[buy_idx, 'Close'],
                            marker="^", color="#00bfae", s=140, edgecolor="white", label="BUY Signal", zorder=4)
    if "SELL" in df_results.columns:
        sell_idx = df_results.index[df_results["SELL"] == 1]
        if len(sell_idx) > 0:
            sns.scatterplot(ax=ax, x=sell_idx, y=df_results.loc[sell_idx, 'Close'],
                            marker="v", color="#ff9100", s=140, edgecolor="white", label="SELL Signal", zorder=4)

    # Always show legend, even if it overflows — best outside upper right
    legend = ax.legend(loc="upper left", fontsize=11, ncol=2, frameon=True, facecolor="#23232e", edgecolor="white", labelcolor='white')
    for text in legend.get_texts():
        text.set_color("white")
    ax.grid(True, which='major', linestyle='--', alpha=0.3)

    # Make all spines white
    for spine in ax.spines.values():
        spine.set_color('white')

    # ---------- Additional indicators on subplots ----------
    for i, (col, kind, color) in enumerate(subplot_indicators):
        ax_ind = axes[i + 1]
        ax_ind.set_ylabel(col, fontsize=12, color='white')
        ax_ind.set_facecolor("none")
        if kind == "bar":
            # Barplot for Volume — use 'date' column as x!
            sns.barplot(ax=ax_ind, x="date", y=col, data=df_results, color=color, alpha=0.55)
            # Beautify x-ticks for readability (rotate and reduce number)
            xticks = ax_ind.get_xticks()
            if len(xticks) > 20:
                for j, label in enumerate(ax_ind.get_xticklabels()):
                    if j % 2 != 0:
                        label.set_visible(False)
            for label in ax_ind.get_xticklabels():
                label.set_rotation(22)
                label.set_color('white')
        elif kind == "line":
            sns.lineplot(ax=ax_ind, x=df_results.index, y=col, data=df_results, color=color, linewidth=2.2)
        ax_ind.grid(True, linestyle="--", alpha=0.22)
        # Draw zero line for oscillators
        if col in ["PV", "Pressure"]:
            ax_ind.axhline(0, color="gray", lw=1, linestyle="--", alpha=0.6)
        if col == "HL":
            ax_ind.set_ylabel("HL (Points)", fontsize=12, color='white')
        for label in ax_ind.get_yticklabels():
            label.set_fontsize(11)
            label.set_color('white')
        for spine in ax_ind.spines.values():
            spine.set_color('white')
        # Show y-axis always
        ax_ind.yaxis.set_visible(True)

    # ---------- Final cosmetic adjustments ----------
    if len(axes) > 1:
        plt.setp(axes[0].get_xticklabels(), visible=False)
        for i in range(1, n_subplots):
            plt.setp(axes[i].get_xticklabels(), rotation=22, color='white')
    axes[-1].set_xlabel("Date", fontsize=13, color='white')
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()