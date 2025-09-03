# -*- coding: utf-8 -*-
# src/interactive/eda/base/__init__.py
#!/usr/bin/env python3
"""
Base EDA Analyzer package.

This package provides the main interface for all EDA operations,
delegating specific analysis tasks to specialized analyzer classes.
"""

from .base_analyzer import EDAAnalyzer
from .core_methods import CoreMethods
from .delegation_methods import DelegationMethods

__all__ = [
    'EDAAnalyzer',
    'CoreMethods',
    'DelegationMethods'
]

# Version info
__version__ = "1.0.0"
