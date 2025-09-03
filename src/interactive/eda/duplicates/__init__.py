# -*- coding: utf-8 -*-
# src/interactive/eda/duplicates/__init__.py
#!/usr/bin/env python3
"""
Duplicates Analysis package.

This module provides comprehensive duplicate detection and fixing capabilities
for financial time series data across multiple timeframes.
"""

from .base_duplicates_analyzer import DuplicatesAnalyzer
from .duplicate_detection import DuplicateDetection
from .duplicate_fixing import DuplicateFixing

__all__ = [
    'DuplicatesAnalyzer',
    'DuplicateDetection',
    'DuplicateFixing'
]

# Version info
__version__ = "1.0.0"
