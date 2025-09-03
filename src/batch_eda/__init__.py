# -*- coding: utf-8 -*-
# src/batch_eda/__init__.py

"""
Batch EDA Module

This package provides batch exploratory data analysis capabilities.
"""

from . import data_quality
from . import fix_files
from . import file_info
from . import basic_stats
from . import time_series_analysis
from . import outlier_handler
from . import stats_logger
from . import html_report_generator

__all__ = [
    'data_quality',
    'fix_files',
    'file_info',
    'basic_stats',
    'time_series_analysis',
    'outlier_handler',
    'stats_logger',
    'html_report_generator'
]