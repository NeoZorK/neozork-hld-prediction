# -*- coding: utf-8 -*-
"""
Trend Indicator Error Handler

This module provides error handling and validation for trend indicators.
"""

import logging
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

from .base_error_handler import BaseErrorHandler

logger = logging.getLogger(__name__)


class TrendErrorHandler(BaseErrorHandler):
    """Error handler for trend indicators."""
    
    def __init__(self, indicator_name: str):
        """Initialize the trend error handler."""
        super().__init__(indicator_name)
        self.trend_specific_validation = {
            'EMA': self._validate_ema,
            'SMA': self._validate_sma,
            'ADX': self._validate_adx,
            'SAR': self._validate_sar,
            'SuperTrend': self._validate_supertrend,
            'Wave': self._validate_wave
        }
    
    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validate trend indicator parameters."""
        try:
            # Common trend parameter validation
            if 'period' in params:
                if not self.validate_positive_value(params['period'], 'period'):
                    return False
                if params['period'] > 1000:
                    self.add_warning(f"Period {params['period']} is unusually large")
            
            # Indicator-specific validation
            if self.indicator_name in self.trend_specific_validation:
                return self.trend_specific_validation[self.indicator_name](params)
            
            return True
            
        except Exception as e:
            self.add_error(f"Parameter validation failed: {str(e)}")
            return False
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate input data for trend calculations."""
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
        """Handle trend calculation errors."""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'indicator': self.indicator_name,
            'context': context,
            'suggestions': self._get_error_suggestions(error, context)
        }
        
        self.add_error(f"Calculation failed: {str(error)}", context)
        
        return error_info
    
    def _validate_ema(self, params: Dict[str, Any]) -> bool:
        """Validate EMA parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
            if params['period'] < 5:
                self.add_warning("EMA period less than 5 may produce noisy signals")
        
        if 'alpha' in params:
            if not self.validate_numeric_range(params['alpha'], 0.001, 1.0, 'alpha'):
                return False
        
        return True
    
    def _validate_sma(self, params: Dict[str, Any]) -> bool:
        """Validate SMA parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
            if params['period'] < 5:
                self.add_warning("SMA period less than 5 may produce noisy signals")
        
        return True
    
    def _validate_adx(self, params: Dict[str, Any]) -> bool:
        """Validate ADX parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
            if params['period'] < 14:
                self.add_warning("ADX period less than 14 may produce noisy signals")
        
        return True
    
    def _validate_sar(self, params: Dict[str, Any]) -> bool:
        """Validate SAR parameters."""
        if 'acceleration' in params:
            if not self.validate_numeric_range(params['acceleration'], 0.01, 0.5, 'acceleration'):
                return False
        
        if 'maximum' in params:
            if not self.validate_numeric_range(params['maximum'], 0.1, 1.0, 'maximum'):
                return False
        
        return True
    
    def _validate_supertrend(self, params: Dict[str, Any]) -> bool:
        """Validate SuperTrend parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        if 'multiplier' in params:
            if not self.validate_numeric_range(params['multiplier'], 0.1, 10.0, 'multiplier'):
                return False
        
        return True
    
    def _validate_wave(self, params: Dict[str, Any]) -> bool:
        """Validate Wave parameters."""
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
