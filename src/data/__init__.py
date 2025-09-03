# -*- coding: utf-8 -*-
# src/../data/__init__.py

"""
Data Module

This module provides comprehensive data handling capabilities including:
- Data acquisition from various sources
- Gap fixing for time series data
- Data processing and transformation
- CSV folder processing
"""

# Import from gap_fixing package
from .gap_fixing import (
    GapFixer, 
    explain_why_fix_gaps,
    get_gap_fixing_benefits,
    get_gap_fixing_methods,
    get_gap_detection_metrics
)

# Import from acquisition package
from .acquisition import (
    acquire_data,
    CSVDataAcquisition,
    DataAcquisitionCache,
    DataAcquisitionRanges,
    DataAcquisitionUtils,
    DataAcquisitionProcessing
)

# Import from processing package
from .processing import CSVFolderProcessor

__all__ = [
    # Gap fixing
    'GapFixer',
    'explain_why_fix_gaps',
    'get_gap_fixing_benefits', 
    'get_gap_fixing_methods',
    'get_gap_detection_metrics',
    
    # Data acquisition
    'acquire_data',
    'CSVDataAcquisition',
    'DataAcquisitionCache',
    'DataAcquisitionRanges',
    'DataAcquisitionUtils',
    'DataAcquisitionProcessing',
    
    # Data processing
    'CSVFolderProcessor'
]