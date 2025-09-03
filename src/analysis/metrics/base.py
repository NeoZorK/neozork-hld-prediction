"""
Base Metrics Components

This module provides base classes for analysis metrics.
"""

import pandas as pd
from typing import Dict, Any, Optional
import numpy as np
from abc import ABC, abstractmethod

from ...core.base import BaseComponent
from ...core.exceptions import DataError, ValidationError


class BaseMetric(BaseComponent, ABC):
    """
    Base class for analysis metrics.
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize base metric.
        
        Args:
            name: Name of the metric
            config: Configuration dictionary
        """
        super().__init__(name, config)
    
    @abstractmethod
    def calculate(self, actual: pd.Series, predicted: Optional[pd.Series] = None) -> float:
        """
        Calculate metric value.
        
        Args:
            actual: Actual values
            predicted: Predicted values (if applicable)
            
        Returns:
            Calculated metric value
        """
        pass
    
    def validate_data(self, actual: pd.Series, predicted: Optional[pd.Series] = None) -> None:
        """
        Validate input data.
        
        Args:
            actual: Actual values to validate
            predicted: Predicted values to validate (if applicable)
        """
        if actual.empty:
            raise DataError("Actual data is empty")
        
        if predicted is not None and predicted.empty:
            raise DataError("Predicted data is empty")
        
        if predicted is not None and len(actual) != len(predicted):
            raise DataError("Actual and predicted data must have same length")


class PerformanceMetrics(BaseMetric):
    """
    Performance metrics calculator.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize performance metrics.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("performance_metrics", config)
    
    def calculate(self, actual: pd.Series, predicted: Optional[pd.Series] = None) -> float:
        """
        Calculate basic performance metric (returns).
        
        Args:
            actual: Actual price series
            predicted: Not used for basic performance
            
        Returns:
            Total return percentage
        """
        self.validate_data(actual, predicted)
        
        if len(actual) < 2:
            raise DataError("Need at least 2 data points for return calculation")
        
        total_return = ((actual.iloc[-1] / actual.iloc[0]) - 1) * 100
        
        self.logger.debug(f"Calculated total return: {total_return:.2f}%")
        return total_return


__all__ = ["BaseMetric", "PerformanceMetrics"]
