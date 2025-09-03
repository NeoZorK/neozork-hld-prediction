# -*- coding: utf-8 -*-
# src/calculation/error_handling/oscillators.py
"""
Oscillator Error Handler

This module provides error handling and validation for oscillator indicators.
"""

import logging
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

from .base_error_handler import BaseErrorHandler

logger = logging.getLogger(__name__)


class OscillatorErrorHandler(BaseErrorHandler):
    """Error handler for oscillator indicators."""
    
    def __init__(self, indicator_name: str):
        """Initialize the oscillator error handler."""
        super().__init__(indicator_name)
        self.oscillator_specific_validation = {
            'RSI': self._validate_rsi,
            'Stochastic': self._validate_stochastic,
            'CCI': self._validate_cci,
            'Williams_R': self._validate_williams_r,
            'ROC': self._validate_roc
        }
    
    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validate oscillator parameters."""
        try:
            # Common oscillator parameter validation
            if 'period' in params:
                if not self.validate_positive_value(params['period'], 'period'):
                    return False
                if params['period'] > 1000:
                    self.add_warning(f"Period {params['period']} is unusually large")
            
            # Indicator-specific validation
            if self.indicator_name in self.oscillator_specific_validation:
                return self.oscillator_specific_validation[self.indicator_name](params)
            
            return True
            
        except Exception as e:
            self.add_error(f"Parameter validation failed: {str(e)}")
            return False
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate input data for oscillator calculations."""
        try:
            # Check required columns
            required_columns = ['Open', 'High', 'Low', 'Close']
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
            
            return True
            
        except Exception as e:
            self.add_error(f"Data validation failed: {str(e)}")
            return False
    
    def handle_calculation_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle oscillator calculation errors."""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'indicator': self.indicator_name,
            'context': context,
            'suggestions': self._get_error_suggestions(error, context)
        }
        
        self.add_error(f"Calculation failed: {str(error)}", context)
        
        return error_info
    
    def _validate_rsi(self, params: Dict[str, Any]) -> bool:
        """Validate RSI parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
            if params['period'] < 14:
                self.add_warning("RSI period less than 14 may produce noisy signals")
        
        if 'overbought' in params:
            if not self.validate_numeric_range(params['overbought'], 50, 100, 'overbought'):
                return False
        
        if 'oversold' in params:
            if not self.validate_numeric_range(params['oversold'], 0, 50, 'oversold'):
                return False
        
        return True
    
    def _validate_stochastic(self, params: Dict[str, Any]) -> bool:
        """Validate Stochastic parameters."""
        if 'k_period' in params:
            if not self.validate_numeric_range(params['k_period'], 1, 100, 'k_period'):
                return False
        
        if 'd_period' in params:
            if not self.validate_numeric_range(params['d_period'], 1, 100, 'd_period'):
                return False
        
        if 'slowing' in params:
            if not self.validate_numeric_range(params['slowing'], 1, 100, 'slowing'):
                return False
        
        return True
    
    def _validate_cci(self, params: Dict[str, Any]) -> bool:
        """Validate CCI parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        if 'constant' in params:
            if not self.validate_numeric_range(params['constant'], 0.1, 1.0, 'constant'):
                return False
        
        return True
    
    def _validate_williams_r(self, params: Dict[str, Any]) -> bool:
        """Validate Williams %R parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        return True
    
    def _validate_roc(self, params: Dict[str, Any]) -> bool:
        """Validate Rate of Change parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
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
        
        return suggestions
