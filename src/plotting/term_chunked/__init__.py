# -*- coding: utf-8 -*-
# src/plotting/term_chunked/__init__.py

"""
Terminal chunked plotting module.

This module provides functionality for displaying data in chunks
using terminal-based plotting with navigation support.
"""

from .core.plot_functions import plot_chunked_terminal
from .utils.plot_utils import (
    get_terminal_plot_size, calculate_optimal_chunk_size, split_dataframe_into_chunks
)

__all__ = [
    'plot_chunked_terminal',
    'get_terminal_plot_size',
    'calculate_optimal_chunk_size', 
    'split_dataframe_into_chunks'
]
