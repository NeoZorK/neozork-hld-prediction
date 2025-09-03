# -*- coding: utf-8 -*-
# src/calculation/error_handling/volume.py
"""
Volume Indicator Error Handler

This module provides error handling and validation for volume indicators.
"""

import logging
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

from .base_error_handler import BaseErrorHandler

logger = logging.getLogger(__name__)


class VolumeErrorHandler(BaseErrorHandler):
    """Error handler for volume indicators."""
    
    def __init__(self, indicator_name: str):
        """Initialize the volume error handler."""
        super().__init__(indicator_name)
        self.volume_specific_validation = {
            'OBV': self._validate_obv,
            'VWAP': self._validate_vwap,
            'Volume_SMA': self._validate_volume_sma,
            'Volume_EMA': self._validate_volume_ema
        }
    
    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validate volume indicator parameters."""
        try:
            # Common volume parameter validation
            if 'period' in params:
                if not self.validate_positive_value(params['period'], 'period'):
                    return False
                if params['period'] > 1000:
                    self.add_warning(f"Period {params['period']} is unusually large")
            
            # Indicator-specific validation
            if self.indicator_name in self.volume_specific_validation:
                return self.volume_specific_validation[self.indicator_name](params)
            
            return True
            
        except Exception as e:
            self.add_error(f"Parameter validation failed: {str(e)}")
            return False
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate input data for volume calculations."""
        try:
            # Check required columns
            required_columns = ['Close', 'Volume']
            if not self.validate_dataframe_columns(data, required_columns):
                return False
            
            # Check data length
            if not self.validate_dataframe_length(data, min_length=50):
                return False
            
            # Check for NaN values
            nan_count = data[required_columns].isna().sum().sum()
            if nan_count > 0:
                self.add_warning(f"Found {nan_count} NaN values in Close/Volume data")
            
            # Check for infinite values
            inf_count = np.isinf(data[required_columns].select_dtypes(include=[np.number])).sum().sum()
            if inf_count > 0:
                self.add_error(f"Found {inf_count} infinite values in Close/Volume data")
                return False
            
            # Check for negative volume
            negative_volume = (data['Volume'] < 0).sum()
            if negative_volume > 0:
                self.add_error(f"Found {negative_volume} negative volume values")
                return False
            
            return True
            
        except Exception as e:
            self.add_error(f"Data validation failed: {str(e)}")
            return False
    
    def handle_calculation_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle volume calculation errors."""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'indicator': self.indicator_name,
            'context': context,
            'suggestions': self._get_error_suggestions(error, context)
        }
        
        self.add_error(f"Calculation failed: {str(error)}", context)
        
        return error_info
    
    def _validate_obv(self, params: Dict[str, Any]) -> bool:
        """Validate OBV parameters."""
        # OBV typically doesn't have parameters
        return True
    
    def _validate_vwap(self, params: Dict[str, Any]) -> bool:
        """Validate VWAP parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        return True
    
    def _validate_volume_sma(self, params: Dict[str, Any]) -> bool:
        """Validate Volume SMA parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        return True
    
    def _validate_volume_ema(self, params: Dict[str, Any]) -> bool:
        """Validate Volume EMA parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        if 'alpha' in params:
            if not self.validate_numeric_range(params['alpha'], 0.001, 1.0, 'alpha'):
                return False
        
        return True
    
    def _get_error_suggestions(self, error: Exception, context: Dict[str, Any]) -> list:
        """Get suggestions for fixing calculation errors."""
        suggestions = []
        
        if "division by zero" in str(error).lower():
            suggestions.append("Check for zero values in volume data")
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
        
        if "volume" in str(error).lower():
            suggestions.append("Check for negative or zero volume values")
            suggestions.append("Ensure volume data is properly formatted")
        
        return suggestions
