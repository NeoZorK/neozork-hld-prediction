"""
Volatility Indicators Implementation

This module provides volatility analysis indicators.
"""

import pandas as pd
from typing import Dict, Any, Tuple
import numpy as np

from .base import VolatilityIndicator
from ...core.exceptions import DataError, ValidationError


class BollingerBands(VolatilityIndicator):
    """
    Bollinger Bands indicator.
    
    Consists of a middle line (SMA) and two standard deviation bands.
    """
    
    def __init__(self, period: int, std_dev: float, config: Dict[str, Any]):
        """
        Initialize Bollinger Bands indicator.
        
        Args:
            period: Number of periods for calculation
            std_dev: Standard deviation multiplier (typically 2.0)
            config: Configuration dictionary
        """
        super().__init__(f"bollinger_{period}", config)
        self.period = period
        self.std_dev = std_dev
        self._validate_parameters()
    
    def _validate_parameters(self) -> None:
        """Validate indicator parameters."""
        if self.period < 2:
            raise ValidationError("Period must be at least 2")
        
        if self.std_dev <= 0:
            raise ValidationError("Standard deviation multiplier must be positive")
    
    def calculate(self, data: pd.Series) -> pd.DataFrame:
        """
        Calculate Bollinger Bands.
        
        Args:
            data: Price series
            
        Returns:
            DataFrame with upper, middle, and lower bands
        """
        if len(data) < self.period:
            raise DataError(f"Insufficient data: need {self.period}, got {len(data)}")
        
        # Calculate middle line (SMA)
        middle = data.rolling(window=self.period).mean()
        
        # Calculate standard deviation
        std = data.rolling(window=self.period).std()
        
        # Calculate bands
        upper = middle + (std * self.std_dev)
        lower = middle - (std * self.std_dev)
        
        result = pd.DataFrame({
            'upper': upper,
            'middle': middle,
            'lower': lower
        }, index=data.index)
        
        self.logger.debug(f"Calculated Bollinger Bands({self.period}, {self.std_dev}) for {len(data)} periods")
        return result
    
    def get_volatility_bands(self, data: pd.Series) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Get volatility bands.
        
        Args:
            data: Price series
            
        Returns:
            Tuple of (upper_band, middle_band, lower_band)
        """
        bands = self.calculate(data)
        return bands['upper'], bands['middle'], bands['lower']


__all__ = ["BollingerBands"]
