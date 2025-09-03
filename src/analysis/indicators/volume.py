"""
Volume Indicators Implementation

This module provides volume analysis indicators.
"""

import pandas as pd
from typing import Dict, Any
import numpy as np

from .base import BaseIndicator
from ...core.exceptions import DataError, ValidationError


class VolumeMovingAverage(BaseIndicator):
    """
    Volume Moving Average indicator.
    
    Calculates the moving average of trading volume.
    """
    
    def __init__(self, period: int, config: Dict[str, Any]):
        """
        Initialize Volume Moving Average indicator.
        
        Args:
            period: Number of periods for calculation
            config: Configuration dictionary
        """
        super().__init__(f"volume_ma_{period}", config)
        self.period = period
        self._validate_parameters()
    
    def _validate_parameters(self) -> None:
        """Validate indicator parameters."""
        if self.period < 2:
            raise ValidationError("Period must be at least 2")
    
    def calculate(self, data: pd.Series) -> pd.Series:
        """
        Calculate Volume Moving Average.
        
        Args:
            data: Volume series
            
        Returns:
            Series containing volume MA values
        """
        if len(data) < self.period:
            raise DataError(f"Insufficient data: need {self.period}, got {len(data)}")
        
        result = data.rolling(window=self.period).mean()
        
        self.logger.debug(f"Calculated Volume MA({self.period}) for {len(data)} periods")
        return result


__all__ = ["VolumeMovingAverage"]
