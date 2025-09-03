# -*- coding: utf-8 -*-
# src/../data/processing/__init__.py

"""
Data Processing Module

This package handles data processing operations including
CSV folder processing and data transformation.
"""

from .csv_folder_processor import CSVFolderProcessor, process_csv_folder
from .csv_processor import CSVProcessor

__all__ = [
    'CSVFolderProcessor',
    'process_csv_folder',
    'CSVProcessor'
]
