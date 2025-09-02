# File: src/data/data_acquisition.py
# -*- coding: utf-8 -*-

"""
Handles the overall data acquisition process by dispatching to specific fetchers based on mode.
Checks for existing single Parquet cache file per instrument and fetches only missing data.
All comments are in English.

This module has been refactored into smaller components for better maintainability.
"""

# Import the main function from the refactored module
from .data_acquisition_core import acquire_data

# Re-export for backward compatibility
__all__ = ['acquire_data']