# -*- coding: utf-8 -*-
"""
Sentiment Indicator Error Handler

This module provides error handling and validation for sentiment indicators.
"""

import logging
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

from .base_error_handler import BaseErrorHandler

logger = logging.getLogger(__name__)


class SentimentErrorHandler(BaseErrorHandler):
    """Error handler for sentiment indicators."""
    
    def __init__(self, indicator_name: str):
        """Initialize the sentiment error handler."""
        super().__init__(indicator_name)
        self.sentiment_specific_validation = {
            'FearGreed': self._validate_fear_greed,
            'COT': self._validate_cot,
            'PutCallRatio': self._validate_put_call_ratio,
            'VIX': self._validate_vix,
            'Market_Sentiment': self._validate_market_sentiment
        }
    
    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validate sentiment indicator parameters."""
        try:
            # Common sentiment parameter validation
            if 'period' in params:
                if not self.validate_positive_value(params['period'], 'period'):
                    return False
                if params['period'] > 1000:
                    self.add_warning(f"Period {params['period']} is unusually large")
            
            # Indicator-specific validation
            if self.indicator_name in self.sentiment_specific_validation:
                return self.sentiment_specific_validation[self.indicator_name](params)
            
            return True
            
        except Exception as e:
            self.add_error(f"Parameter validation failed: {str(e)}")
            return False
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate input data for sentiment calculations."""
        try:
            # Check required columns based on indicator type
            if self.indicator_name == 'FearGreed':
                required_columns = ['Close']
            elif self.indicator_name == 'COT':
                required_columns = ['Open_Interest', 'Long_Positions', 'Short_Positions']
            elif self.indicator_name == 'PutCallRatio':
                required_columns = ['Put_Volume', 'Call_Volume']
            elif self.indicator_name == 'VIX':
                required_columns = ['VIX']
            else:
                required_columns = ['Close']
            
            if not self.validate_dataframe_columns(data, required_columns):
                return False
            
            # Check data length
            if not self.validate_dataframe_length(data, min_length=50):
                return False
            
            # Check for NaN values
            nan_count = data[required_columns].isna().sum().sum()
            if nan_count > 0:
                self.add_warning(f"Found {nan_count} NaN values in sentiment data")
            
            # Check for infinite values
            inf_count = np.isinf(data[required_columns].select_dtypes(include=[np.number])).sum().sum()
            if inf_count > 0:
                self.add_error(f"Found {inf_count} infinite values in sentiment data")
                return False
            
            # Indicator-specific data validation
            if self.indicator_name == 'COT':
                if not self._validate_cot_data(data):
                    return False
            elif self.indicator_name == 'PutCallRatio':
                if not self._validate_put_call_data(data):
                    return False
            
            return True
            
        except Exception as e:
            self.add_error(f"Data validation failed: {str(e)}")
            return False
    
    def handle_calculation_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle sentiment calculation errors."""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'indicator': self.indicator_name,
            'context': context,
            'suggestions': self._get_error_suggestions(error, context)
        }
        
        self.add_error(f"Calculation failed: {str(error)}", context)
        
        return error_info
    
    def _validate_fear_greed(self, params: Dict[str, Any]) -> bool:
        """Validate Fear & Greed parameters."""
        if 'smoothing_period' in params:
            if not self.validate_numeric_range(params['smoothing_period'], 1, 100, 'smoothing_period'):
                return False
        
        return True
    
    def _validate_cot(self, params: Dict[str, Any]) -> bool:
        """Validate Commitments of Traders parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        if 'threshold' in params:
            if not self.validate_numeric_range(params['threshold'], 0.0, 1.0, 'threshold'):
                return False
        
        return True
    
    def _validate_put_call_ratio(self, params: Dict[str, Any]) -> bool:
        """Validate Put/Call Ratio parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        if 'smoothing' in params:
            if not self.validate_numeric_range(params['smoothing'], 1, 100, 'smoothing'):
                return False
        
        return True
    
    def _validate_vix(self, params: Dict[str, Any]) -> bool:
        """Validate VIX parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        return True
    
    def _validate_market_sentiment(self, params: Dict[str, Any]) -> bool:
        """Validate Market Sentiment parameters."""
        if 'period' in params:
            if not self.validate_numeric_range(params['period'], 1, 1000, 'period'):
                return False
        
        if 'threshold' in params:
            if not self.validate_numeric_range(params['threshold'], 0.0, 1.0, 'threshold'):
                return False
        
        return True
    
    def _validate_cot_data(self, data: pd.DataFrame) -> bool:
        """Validate COT data specifically."""
        # Check for negative values in positions
        negative_long = (data['Long_Positions'] < 0).sum()
        negative_short = (data['Short_Positions'] < 0).sum()
        
        if negative_long > 0:
            self.add_error(f"Found {negative_long} negative long position values")
            return False
        
        if negative_short > 0:
            self.add_error(f"Found {negative_short} negative short position values")
            return False
        
        # Check that open interest is reasonable
        if 'Open_Interest' in data.columns:
            zero_oi = (data['Open_Interest'] == 0).sum()
            if zero_oi > len(data) * 0.1:  # More than 10% zero values
                self.add_warning(f"Found {zero_oi} zero open interest values")
        
        return True
    
    def _validate_put_call_data(self, data: pd.DataFrame) -> bool:
        """Validate Put/Call data specifically."""
        # Check for negative volumes
        negative_put = (data['Put_Volume'] < 0).sum()
        negative_call = (data['Call_Volume'] < 0).sum()
        
        if negative_put > 0:
            self.add_error(f"Found {negative_put} negative put volume values")
            return False
        
        if negative_call > 0:
            self.add_error(f"Found {negative_call} negative call volume values")
            return False
        
        # Check for zero volumes
        zero_put = (data['Put_Volume'] == 0).sum()
        zero_call = (data['Call_Volume'] == 0).sum()
        
        if zero_put > len(data) * 0.2:  # More than 20% zero values
            self.add_warning(f"Found {zero_put} zero put volume values")
        
        if zero_call > len(data) * 0.2:  # More than 20% zero values
            self.add_warning(f"Found {zero_call} zero call volume values")
        
        return True
    
    def _get_error_suggestions(self, error: Exception, context: Dict[str, Any]) -> list:
        """Get suggestions for fixing calculation errors."""
        suggestions = []
        
        if "division by zero" in str(error).lower():
            suggestions.append("Check for zero values in sentiment data")
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
        
        if "cot" in str(error).lower():
            suggestions.append("Check for negative position values")
            suggestions.append("Ensure open interest data is valid")
        
        if "put" in str(error).lower() or "call" in str(error).lower():
            suggestions.append("Check for negative volume values")
            suggestions.append("Ensure volume data is properly formatted")
        
        if "sentiment" in str(error).lower():
            suggestions.append("Check sentiment data ranges")
            suggestions.append("Ensure sentiment values are between expected bounds")
        
        return suggestions
