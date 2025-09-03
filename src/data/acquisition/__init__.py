# -*- coding: utf-8 -*-
# src/data/acquisition/__init__.py

"""
Data Acquisition Module

This package handles data acquisition from various sources including
CSV files, caching, and processing.
"""

from .core import acquire_data
from .csv import CSVDataAcquisition
from .cache import DataAcquisitionCache
from .ranges import DataAcquisitionRanges
from .utils import DataAcquisitionUtils
from .processing import DataAcquisitionProcessing

__all__ = [
    'acquire_data',
    'CSVDataAcquisition',
    'DataAcquisitionCache',
    'DataAcquisitionRanges',
    'DataAcquisitionUtils',
    'DataAcquisitionProcessing'
]
