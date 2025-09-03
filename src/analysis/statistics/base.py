"""
Base Statistics Components

This module provides base classes for statistical analysis.
"""

import pandas as pd
from typing import Dict, Any, Optional
import numpy as np
from abc import ABC, abstractmethod

from ...core.base import BaseComponent
from ...core.exceptions import DataError, ValidationError


class BaseStatistic(BaseComponent, ABC):
    """
    Base class for statistical analysis components.
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize base statistic.
        
        Args:
            name: Name of the statistic
            config: Configuration dictionary
        """
        super().__init__(name, config)
    
    @abstractmethod
    def calculate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate statistic.
        
        Args:
            data: Input data
            
        Returns:
            Dictionary containing calculated statistics
        """
        pass
    
    def validate_data(self, data: pd.DataFrame) -> None:
        """
        Validate input data.
        
        Args:
            data: Input data to validate
        """
        if data.empty:
            raise DataError("Input data is empty")
        
        if data.isnull().all().all():
            raise DataError("Input data contains only null values")


class DescriptiveStatistics(BaseStatistic):
    """
    Descriptive statistics calculator.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize descriptive statistics.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("descriptive_stats", config)
        self.include_percentiles = config.get("include_percentiles", True)
        self.percentiles = config.get("percentiles", [0.25, 0.5, 0.75])
    
    def calculate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate descriptive statistics.
        
        Args:
            data: Input data
            
        Returns:
            Dictionary containing descriptive statistics
        """
        self.validate_data(data)
        
        stats = {}
        
        # Basic statistics
        stats['count'] = data.count()
        stats['mean'] = data.mean()
        stats['std'] = data.std()
        stats['min'] = data.min()
        stats['max'] = data.max()
        
        # Percentiles
        if self.include_percentiles:
            for p in self.percentiles:
                stats[f'percentile_{int(p * 100)}'] = data.quantile(p)
        
        # Additional metrics
        stats['skewness'] = data.skew()
        stats['kurtosis'] = data.kurtosis()
        stats['variance'] = data.var()
        
        self.logger.debug(f"Calculated descriptive statistics for {len(data)} rows")
        return stats


__all__ = ["BaseStatistic", "DescriptiveStatistics"]
