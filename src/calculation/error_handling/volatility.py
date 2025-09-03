# -*- coding: utf-8 -*-
# src/calculation/error_handling/volatility.py
"""
Volatility Indicator Error Handler

This module provides error handling and validation for volatility indicators.
"""

import logging
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

from .base_error_handler import BaseErrorHandler

logger = logging.getLogger(__name__)


class VolatilityErrorHandler(BaseErrorHandler):
    """Error handler for volatility indicators."""
    
    def __init__(self, indicator_name: str):
        """Initialize the volatility error handler."""
        super().__init__(indicator_name)
        self.volatility_specific_validation = {
            'ATR': self._validate_atr,
            'Bollinger_Bands': self._validate_bollinger_bands,
            'StDev': self._validate_stdev,
            'Keltner_Channels': self._validate_keltner_channels
        }
    
    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validate volatility indicator parameters."""
        try:
            # Common volatility parameter validation
            if 'period' in params:
                if not self.validate_positive_value(params['period'], 'period'):
                    return False
                if params['period'] > 1000:
                    self.add_warning(f"Period {params['period']} is unusually large")
            
            # Indicator-specific validation
            if self.indicator_name in self.volatility_specific_validation:
                return self.volatility_specific_validation[self.indicator_name](params)
            
            return True
            
        except Exception as e:
            self.add_error(f"Parameter validation failed: {str(e)}")
            return False
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate input data for volatility calculations."""
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
        """Handle volatility calculation errors."""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'indicator': self.indicator_name,
            'context': context,
            'suggestions': self._get_error_suggestions(error, context)
        }
        
        self.add_error(f"Calculation failed: {str(error)}", context)
        
        return error_info
    
    def _validate_atr(self, params: Dict[str, Any]) -> bool:
        """Validate ATR parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        return True
    
    def _validate_bollinger_bands(self, params: Dict[str, Any]) -> bool:
        """Validate Bollinger Bands parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        if 'std_dev' in params:
            if not self.validate_numeric_range(params['std_dev'], 0.1, 5.0, 'std_dev'):
                return False
        
        return True
    
    def _validate_stdev(self, params: Dict[str, Any]) -> bool:
        """Validate Standard Deviation parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        return True
    
    def _validate_keltner_channels(self, params: Dict[str, Any]) -> bool:
        """Validate Keltner Channels parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        if 'multiplier' in params:
            if not self.validate_numeric_range(params['multiplier'], 0.1, 10.0, 'multiplier'):
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
        
        return suggestions
