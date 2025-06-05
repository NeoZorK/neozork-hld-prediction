# -*- coding: utf-8 -*-
# src/plotting/term_auto_plot.py

"""
Terminal-based plotting functions for AUTO mode visualization using Rich library.
This module provides text-based charts displayed directly in the terminal for AUTO mode.
"""

from .term_plot import create_term_auto_plot


def auto_plot_from_parquet(parquet_file_path, **kwargs):
    """
    Terminal plotting function for AUTO mode from parquet files.
    This is a wrapper around the main terminal plotting functionality.
    
    Args:
        parquet_file_path (str): Path to the parquet file.
        **kwargs: Additional keyword arguments.
    
    Returns:
        None: Displays the chart directly in terminal.
    """
    import pandas as pd
    from ..common import logger
    
    try:
        # Read the parquet file
        df = pd.read_parquet(parquet_file_path)
        
        # Use the terminal auto plot function
        return create_term_auto_plot(df, title=f"Auto Terminal Plot - {parquet_file_path}", **kwargs)
        
    except Exception as e:
        logger.print_error(f"Error in terminal auto plot from parquet: {str(e)}")
        return None
