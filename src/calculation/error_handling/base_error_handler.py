# -*- coding: utf-8 -*-
# src/calculation/error_handling/base_error_handler.py
"""
Base Error Handler for Indicator Calculations

This module provides the base class for all indicator error handlers.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class BaseErrorHandler(ABC):
    """Base class for indicator error handlers."""
    
    def __init__(self, indicator_name: str):
        """Initialize the error handler."""
        self.indicator_name = indicator_name
        self.errors = []
        self.warnings = []
        self.validation_results = {}
    
    @abstractmethod
    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validate indicator parameters."""
        pass
    
    @abstractmethod
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate input data for the indicator."""
        pass
    
    @abstractmethod
    def handle_calculation_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle calculation errors."""
        pass
    
    def add_error(self, error_msg: str, context: Optional[Dict[str, Any]] = None):
        """Add an error message."""
        error_info = {
            'message': error_msg,
            'indicator': self.indicator_name,
            'context': context or {},
            'timestamp': pd.Timestamp.now()
        }
        self.errors.append(error_info)
        logger.error(f"{self.indicator_name}: {error_msg}")
    
    def add_warning(self, warning_msg: str, context: Optional[Dict[str, Any]] = None):
        """Add a warning message."""
        warning_info = {
            'message': warning_msg,
            'indicator': self.indicator_name,
            'context': context or {},
            'timestamp': pd.Timestamp.now()
        }
        self.warnings.append(warning_info)
        logger.warning(f"{self.indicator_name}: {warning_msg}")
    
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get a summary of all errors and warnings."""
        return {
            'indicator': self.indicator_name,
            'total_errors': len(self.errors),
            'total_warnings': len(self.warnings),
            'errors': self.errors,
            'warnings': self.warnings,
            'validation_results': self.validation_results
        }
    
    def clear_errors(self):
        """Clear all errors and warnings."""
        self.errors.clear()
        self.warnings.clear()
        self.validation_results.clear()
    
    def validate_numeric_range(self, value: float, min_val: float, max_val: float, param_name: str) -> bool:
        """Validate that a numeric parameter is within range."""
        if not isinstance(value, (int, float)):
            self.add_error(f"Parameter {param_name} must be numeric, got {type(value)}")
            return False
        
        if value < min_val or value > max_val:
            self.add_error(f"Parameter {param_name} must be between {min_val} and {max_val}, got {value}")
            return False
        
        return True
    
    def validate_positive_value(self, value: float, param_name: str) -> bool:
        """Validate that a parameter is positive."""
        if not isinstance(value, (int, float)) or value <= 0:
            self.add_error(f"Parameter {param_name} must be a positive number, got {value}")
            return False
        return True
    
    def validate_dataframe_columns(self, data: pd.DataFrame, required_columns: List[str]) -> bool:
        """Validate that required columns exist in the dataframe."""
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            self.add_error(f"Missing required columns: {missing_columns}")
            return False
        return True
    
    def validate_dataframe_length(self, data: pd.DataFrame, min_length: int = 1) -> bool:
        """Validate that dataframe has sufficient data."""
        if len(data) < min_length:
            self.add_error(f"Dataframe must have at least {min_length} rows, got {len(data)}")
            return False
        return True
