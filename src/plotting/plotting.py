# -*- coding: utf-8 -*-
# src/plotting/plotting.py

"""
Plotting functions for visualizing indicator results using Plotly (interactive)
or mplfinance (static).
"""

import pandas as pd

from .mplfinance_plot import plot_indicator_results_mplfinance
from .plotly_plot import plot_indicator_results_plotly
# Use relative imports for constants and logger
from ..common.constants import TradingRule
from ..common import logger
from .fastest_plot import plot_indicator_results_fastest # Import the new fastest plot function
from .fast_plot import plot_indicator_results_fast # Import the fast plot function

# --- Wrapper function to call the appropriate plotting function ---
def plot_indicator_results(df_results, rule, title="Indicator Results", mode="plotly", data_source="demo", output_path=None):
    """
    Wrapper function to call the appropriate plotting function based on the mode parameter.
    
    Args:
        df_results (pd.DataFrame): The DataFrame with OHLC data and indicators.
        rule (TradingRule): The trading rule used in analysis.
        title (str): Title for the plot.
        mode (str): The plotting mode to use:
                    - 'fastest': Uses Plotly + Dask + Datashader for extremely large datasets
                    - 'fast': Uses Dask + Datashader + Bokeh (default for large datasets)
                    - 'plotly'/'plt': Uses Plotly for interactive HTML plots
                    - 'mplfinance'/'mpl': Uses mplfinance for static image plots
        data_source (str): Source of the data (for special formatting).
        output_path (str): Path to save the output file (for 'fastest' and 'fast' modes).
    
    Returns:
        Various types depending on the mode:
        - go.Figure for 'plotly' mode
        - Figure for 'mplfinance' mode
        - None for 'fast' and 'fastest' modes (these save to disk and open in browser)
    """
    try:
        # Standardize the mode parameter
        mode = mode.lower() if isinstance(mode, str) else 'plotly'
        
        # Route to the appropriate plotting function
        if mode == 'fastest':
            logger.print_info(f"Using 'fastest' mode (Plotly + Dask + Datashader) for plotting...")
            plot_indicator_results_fastest(df_results, rule, title=title, data_source=data_source, 
                                         output_path=output_path or "results/plots/fastest_plot.html", 
                                         mode=mode)
            return None
        elif mode in ['fast', 'dask']:
            logger.print_info(f"Using 'fast' mode (Dask + Datashader + Bokeh) for plotting...")
            plot_indicator_results_fast(df_results, rule, title=title, data_source=data_source, 
                                      output_path=output_path or "results/plots/fast_plot.html", 
                                      mode=mode)
            return None
        elif mode in ['plotly', 'plt']:
            logger.print_info(f"Using 'plotly' mode for plotting...")
            return plot_indicator_results_plotly(df_results, rule, title)
        elif mode in ['mplfinance', 'mpl']:
            logger.print_info(f"Using 'mplfinance' mode for plotting...")
            return plot_indicator_results_mplfinance(df_results, rule, title)
        else:
            logger.print_warning(f"Unknown plotting mode '{mode}', defaulting to 'plotly'...")
            return plot_indicator_results_plotly(df_results, rule, title)
    except Exception as e:
        logger.print_error(f"Error in plot_indicator_results with mode='{mode}': {str(e)}")
        # Try to fallback to plotly if another mode fails
        if mode != 'plotly':
            logger.print_warning(f"Falling back to 'plotly' mode due to error...")
            try:
                return plot_indicator_results_plotly(df_results, rule, title)
            except Exception as fallback_error:
                logger.print_error(f"Fallback to 'plotly' also failed: {str(fallback_error)}")
                return None
        return None
