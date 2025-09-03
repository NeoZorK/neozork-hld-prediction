# -*- coding: utf-8 -*-
# src/calculation/error_handling/predictive.py
"""
Predictive Indicator Error Handler

This module provides error handling and validation for predictive indicators.
"""

import logging
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

from .base_error_handler import BaseErrorHandler

logger = logging.getLogger(__name__)


class PredictiveErrorHandler(BaseErrorHandler):
    """Error handler for predictive indicators."""
    
    def __init__(self, indicator_name: str):
        """Initialize the predictive error handler."""
        super().__init__(indicator_name)
        self.predictive_specific_validation = {
            'HMA': self._validate_hma,
            'TSForecast': self._validate_tsforecast,
            'Linear_Regression': self._validate_linear_regression,
            'Polynomial_Regression': self._validate_polynomial_regression
        }
    
    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validate predictive indicator parameters."""
        try:
            # Common predictive parameter validation
            if 'period' in params:
                if not self.validate_positive_value(params['period'], 'period'):
                    return False
                if params['period'] > 1000:
                    self.add_warning(f"Period {params['period']} is unusually large")
            
            # Indicator-specific validation
            if self.indicator_name in self.predictive_specific_validation:
                return self.predictive_specific_validation[self.indicator_name](params)
            
            return True
            
        except Exception as e:
            self.add_error(f"Parameter validation failed: {str(e)}")
            return False
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate input data for predictive calculations."""
        try:
            # Check required columns
            required_columns = ['Close']
            if not self.validate_dataframe_columns(data, required_columns):
                return False
            
            # Check data length
            if not self.validate_dataframe_length(data, min_length=100):
                return False
            
            # Check for NaN values
            nan_count = data[required_columns].isna().sum().sum()
            if nan_count > 0:
                self.add_warning(f"Found {nan_count} NaN values in Close data")
            
            # Check for infinite values
            inf_count = np.isinf(data[required_columns].select_dtypes(include=[np.number])).sum().sum()
            if inf_count > 0:
                self.add_error(f"Found {inf_count} infinite values in Close data")
                return False
            
            return True
            
        except Exception as e:
            self.add_error(f"Data validation failed: {str(e)}")
            return False
    
    def handle_calculation_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle predictive calculation errors."""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'indicator': self.indicator_name,
            'context': context,
            'suggestions': self._get_error_suggestions(error, context)
        }
        
        self.add_error(f"Calculation failed: {str(error)}", context)
        
        return error_info
    
    def _validate_hma(self, params: Dict[str, Any]) -> bool:
        """Validate HMA parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
            if params['period'] < 10:
                self.add_warning("HMA period less than 10 may produce noisy signals")
        
        return True
    
    def _validate_tsforecast(self, params: Dict[str, Any]) -> bool:
        """Validate Time Series Forecast parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        if 'forecast_periods' in params:
            if not self.validate_numeric_range(params['forecast_periods'], 1, 100, 'forecast_periods'):
                return False
        
        return True
    
    def _validate_linear_regression(self, params: Dict[str, Any]) -> bool:
        """Validate Linear Regression parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 10, 1000, 'period'):
                return False
            if params['period'] < 20:
                self.add_warning("Linear regression period less than 20 may be unreliable")
        
        if 'forecast_periods' in params:
            if not self.validate_numeric_range(params['forecast_periods'], 1, 50, 'forecast_periods'):
                return False
        
        return True
    
    def _validate_polynomial_regression(self, params: Dict[str, Any]) -> bool:
        """Validate Polynomial Regression parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 20, 1000, 'period'):
                return False
            if params['period'] < 30:
                self.add_warning("Polynomial regression period less than 30 may be unreliable")
        
        if 'degree' in params:
            if not self.validate_numeric_range(params['degree'], 1, 5, 'degree'):
                return False
            if params['degree'] > 3:
                self.add_warning("Polynomial degree > 3 may lead to overfitting")
        
        if 'forecast_periods' in params:
            if not self.validate_numeric_range(params['forecast_periods'], 1, 30, 'forecast_periods'):
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
        
        if "singular" in str(error).lower() or "matrix" in str(error).lower():
            suggestions.append("Check for sufficient data variation")
            suggestions.append("Reduce polynomial degree or increase period")
        
        if "convergence" in str(error).lower():
            suggestions.append("Check data quality and consistency")
            suggestions.append("Reduce forecast periods or increase data length")
        
        return suggestions
