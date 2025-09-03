# -*- coding: utf-8 -*-
# src/calculation/error_handling/support_resistance.py
"""
Support/Resistance Indicator Error Handler

This module provides error handling and validation for support/resistance indicators.
"""

import logging
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

from .base_error_handler import BaseErrorHandler

logger = logging.getLogger(__name__)


class SupportResistanceErrorHandler(BaseErrorHandler):
    """Error handler for support/resistance indicators."""
    
    def __init__(self, indicator_name: str):
        """Initialize the support/resistance error handler."""
        super().__init__(indicator_name)
        self.sr_specific_validation = {
            'Pivot_Points': self._validate_pivot_points,
            'Fibonacci_Retracement': self._validate_fibonacci,
            'Donchian_Channels': self._validate_donchian,
            'Support_Resistance': self._validate_support_resistance
        }
    
    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validate support/resistance indicator parameters."""
        try:
            # Common SR parameter validation
            if 'period' in params:
                if not self.validate_positive_value(params['period'], 'period'):
                    return False
                if params['period'] > 1000:
                    self.add_warning(f"Period {params['period']} is unusually large")
            
            # Indicator-specific validation
            if self.indicator_name in self.sr_specific_validation:
                return self.sr_specific_validation[self.indicator_name](params)
            
            return True
            
        except Exception as e:
            self.add_error(f"Parameter validation failed: {str(e)}")
            return False
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate input data for support/resistance calculations."""
        try:
            # Check required columns
            required_columns = ['High', 'Low', 'Close']
            if not self.validate_dataframe_columns(data, required_columns):
                return False
            
            # Check data length
            if not self.validate_dataframe_length(data, min_length=50):
                return False
            
            # Check for NaN values
            nan_count = data[required_columns].isna().sum().sum()
            if nan_count > 0:
                self.add_warning(f"Found {nan_count} NaN values in OHLC data")
            
            # Check for infinite values
            inf_count = np.isinf(data[required_columns].select_dtypes(include=[np.number])).sum().sum()
            if inf_count > 0:
                self.add_error(f"Found {inf_count} infinite values in OHLC data")
                return False
            
            # Check for invalid price relationships
            invalid_high_low = (data['High'] < data['Low']).sum()
            if invalid_high_low > 0:
                self.add_error(f"Found {invalid_high_low} rows where High < Low")
                return False
            
            return True
            
        except Exception as e:
            self.add_error(f"Data validation failed: {str(e)}")
            return False
    
    def handle_calculation_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle support/resistance calculation errors."""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'indicator': self.indicator_name,
            'context': context,
            'suggestions': self._get_error_suggestions(error, context)
        }
        
        self.add_error(f"Calculation failed: {str(error)}", context)
        
        return error_info
    
    def _validate_pivot_points(self, params: Dict[str, Any]) -> bool:
        """Validate Pivot Points parameters."""
        # Pivot points typically don't have parameters
        return True
    
    def _validate_fibonacci(self, params: Dict[str, Any]) -> bool:
        """Validate Fibonacci Retracement parameters."""
        if 'levels' in params:
            if not isinstance(params['levels'], (list, tuple)):
                self.add_error("Fibonacci levels must be a list or tuple")
                return False
            
            for level in params['levels']:
                if not self.validate_numeric_range(level, 0.0, 1.0, 'fibonacci_level'):
                    return False
        
        return True
    
    def _validate_donchian(self, params: Dict[str, Any]) -> bool:
        """Validate Donchian Channels parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        return True
    
    def _validate_support_resistance(self, params: Dict[str, Any]) -> bool:
        """Validate Support/Resistance parameters."""
        if 'sensitivity' in params:
            if not self.validate_numeric_range(params['sensitivity'], 0.001, 1.0, 'sensitivity'):
                return False
        
        if 'min_touches' in params:
            if not self.validate_numeric_range(params['min_touches'], 1, 10, 'min_touches'):
                return False
        
        return True
    
    def _get_error_suggestions(self, error: Exception, context: Dict[str, Any]) -> list:
        """Get suggestions for fixing calculation errors."""
        suggestions = []
        
        if "division by zero" in str(error).lower():
            suggestions.append("Check for zero values in price data")
            suggestions.append("Ensure period parameter is not zero")
        
        if "nan" in str(error).lower():
            suggestions.append("Remove or interpolate NaN values in data")
            suggestions.append("Check for missing data points")
        
        if "index" in str(error).lower():
            suggestions.append("Ensure data has sufficient length for period")
            suggestions.append("Check period parameter is not larger than data length")
        
        if "type" in str(error).lower():
            suggestions.append("Ensure all parameters are numeric")
            suggestions.append("Check data types in input dataframe")
        
        if "high" in str(error).lower() or "low" in str(error).lower():
            suggestions.append("Check for invalid High/Low price relationships")
            suggestions.append("Ensure High >= Low for all data points")
        
        if "fibonacci" in str(error).lower():
            suggestions.append("Check Fibonacci levels are between 0 and 1")
            suggestions.append("Ensure levels are provided as a list")
        
        return suggestions
