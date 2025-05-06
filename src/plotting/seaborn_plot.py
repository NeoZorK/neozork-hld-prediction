# -*- coding: utf-8 -*-
# src/plotting/seaborn_plot.py

"""
Plotting functions for visualizing indicator results using seaborn.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from ..common.constants import TradingRule
from ..common import logger

def plot_indicator_results_seaborn(
    df_results: pd.DataFrame,
    rule: TradingRule,
    title: str = "Indicator Results (Seaborn)",
    **kwargs
):
    """
    Plots indicator results using seaborn.
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

    plt.figure(figsize=(16, 8))
    sns.lineplot(data=df_results, x=df_results.index, y='Close', label='Close', color='blue')
    sns.lineplot(data=df_results, x=df_results.index, y='High', label='High', color='green', alpha=0.4)
    sns.lineplot(data=df_results, x=df_results.index, y='Low', label='Low', color='red', alpha=0.4)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.show()