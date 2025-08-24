# -*- coding: utf-8 -*-
# src/ml/feature_engineering/logger.py

"""
Simple logger for ML module when src.common.logger is not available.
"""

import sys
from typing import Optional


class SimpleLogger:
    """Simple logger implementation for ML module."""
    
    @staticmethod
    def print_info(message: str):
        """Print info message."""
        print(f"[INFO] {message}")
        
    @staticmethod
    def print_warning(message: str):
        """Print warning message."""
        print(f"[WARNING] {message}")
        
    @staticmethod
    def print_error(message: str):
        """Print error message."""
        print(f"[ERROR] {message}")
        
    @staticmethod
    def print_success(message: str):
        """Print success message."""
        print(f"[SUCCESS] {message}")
        
    @staticmethod
    def print_debug(message: str):
        """Print debug message."""
        print(f"[DEBUG] {message}")


# Try to import the real logger, fallback to simple one
try:
    from src.common import logger
except ImportError:
    logger = SimpleLogger()
