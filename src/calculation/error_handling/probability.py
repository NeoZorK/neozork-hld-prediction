# -*- coding: utf-8 -*-
"""
Probability Indicator Error Handler

This module provides error handling and validation for probability indicators.
"""

import logging
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

from .base_error_handler import BaseErrorHandler

logger = logging.getLogger(__name__)


class ProbabilityErrorHandler(BaseErrorHandler):
    """Error handler for probability indicators."""
    
    def __init__(self, indicator_name: str):
        """Initialize the probability error handler."""
        super().__init__(indicator_name)
        self.probability_specific_validation = {
            'MonteCarlo': self._validate_monte_carlo,
            'Kelly': self._validate_kelly,
            'Probability_Distribution': self._validate_prob_distribution,
            'Confidence_Interval': self._validate_confidence_interval
        }
    
    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validate probability indicator parameters."""
        try:
            # Common probability parameter validation
            if 'period' in params:
                if not self.validate_positive_value(params['period'], 'period'):
                    return False
                if params['period'] > 1000:
                    self.add_warning(f"Period {params['period']} is unusually large")
            
            # Indicator-specific validation
            if self.indicator_name in self.probability_specific_validation:
                return self.probability_specific_validation[self.indicator_name](params)
            
            return True
            
        except Exception as e:
            self.add_error(f"Parameter validation failed: {str(e)}")
            return False
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate input data for probability calculations."""
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
        """Handle probability calculation errors."""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'indicator': self.indicator_name,
            'context': context,
            'suggestions': self._get_error_suggestions(error, context)
        }
        
        self.add_error(f"Calculation failed: {str(error)}", context)
        
        return error_info
    
    def _validate_monte_carlo(self, params: Dict[str, Any]) -> bool:
        """Validate Monte Carlo parameters."""
        if 'simulations' in params:
            if not self.validate_numeric_range(params['simulations'], 100, 100000, 'simulations'):
                return False
            if params['simulations'] > 10000:
                self.add_warning("Large number of simulations may take significant time")
        
        if 'time_steps' in params:
            if not self.validate_numeric_range(params['time_steps'], 10, 1000, 'time_steps'):
                return False
        
        if 'volatility' in params:
            if not self.validate_numeric_range(params['volatility'], 0.001, 1.0, 'volatility'):
                return False
        
        return True
    
    def _validate_kelly(self, params: Dict[str, Any]) -> bool:
        """Validate Kelly Criterion parameters."""
        if 'win_rate' in params:
            if not self.validate_numeric_range(params['win_rate'], 0.0, 1.0, 'win_rate'):
                return False
        
        if 'avg_win' in params:
            if not self.validate_positive_value(params['avg_win'], 'avg_win'):
                return False
        
        if 'avg_loss' in params:
            if not self.validate_positive_value(params['avg_loss'], 'avg_loss'):
                return False
        
        return True
    
    def _validate_prob_distribution(self, params: Dict[str, Any]) -> bool:
        """Validate Probability Distribution parameters."""
        if 'distribution_type' in params:
            valid_distributions = ['normal', 'lognormal', 'exponential', 'gamma', 'weibull']
            if params['distribution_type'] not in valid_distributions:
                self.add_error(f"Invalid distribution type. Must be one of: {valid_distributions}")
                return False
        
        if 'confidence_level' in params:
            if not self.validate_numeric_range(params['confidence_level'], 0.5, 0.999, 'confidence_level'):
                return False
        
        return True
    
    def _validate_confidence_interval(self, params: Dict[str, Any]) -> bool:
        """Validate Confidence Interval parameters."""
        if 'confidence_level' in params:
            if not self.validate_numeric_range(params['confidence_level'], 0.5, 0.999, 'confidence_level'):
                return False
        
        if 'bootstrap_samples' in params:
            if not self.validate_numeric_range(params['bootstrap_samples'], 100, 10000, 'bootstrap_samples'):
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
        
        if "monte" in str(error).lower() or "simulation" in str(error).lower():
            suggestions.append("Reduce number of simulations or time steps")
            suggestions.append("Check for sufficient memory and processing power")
        
        if "kelly" in str(error).lower():
            suggestions.append("Check win rate is between 0 and 1")
            suggestions.append("Ensure average win and loss are positive")
        
        if "distribution" in str(error).lower():
            suggestions.append("Check distribution type is valid")
            suggestions.append("Ensure confidence level is between 0.5 and 0.999")
        
        if "bootstrap" in str(error).lower():
            suggestions.append("Reduce bootstrap sample size")
            suggestions.append("Check for sufficient data length")
        
        return suggestions
