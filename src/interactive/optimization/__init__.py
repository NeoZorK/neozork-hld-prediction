# -*- coding: utf-8 -*-
"""
Optimization module for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive performance optimization capabilities.
"""

from .performance_profiler import PerformanceProfiler
from .cache_manager import CacheManager
from .async_processor import AsyncProcessor

class OptimizationSystem:
    """Main optimization system class."""
    def __init__(self):
        self.performance_profiler = PerformanceProfiler()
        self.cache_manager = CacheManager()
        self.async_processor = AsyncProcessor()

__all__ = [
    'OptimizationSystem',
    'PerformanceProfiler',
    'CacheManager',
    'AsyncProcessor'
]
