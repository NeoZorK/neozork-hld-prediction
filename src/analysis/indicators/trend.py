"""
Trend Indicators Implementation

This module provides trend analysis indicators.
"""

import pandas as pd
from typing import Dict, Any
import numpy as np

from .base import TrendIndicator
from ...core.exceptions import DataError, ValidationError


class MovingAverage(TrendIndicator):
    """
    Simple Moving Average (SMA) indicator.
    
    Calculates the arithmetic mean of prices over a specified period.
    """
    
    def __init__(self, period: int, config: Dict[str, Any]):
        """
        Initialize Moving Average indicator.
        
        Args:
            period: Number of periods for calculation
            config: Configuration dictionary
        """
        super().__init__(f"sma_{period}", config)
        self.period = period
        self._validate_parameters()
    
    def _validate_parameters(self) -> None:
        """Validate indicator parameters."""
        if self.period < 2:
            raise ValidationError("Period must be at least 2")
        
        if self.period > 500:
            raise ValidationError("Period cannot exceed 500")
    
    def calculate(self, data: pd.Series) -> pd.Series:
        """
        Calculate Simple Moving Average.
        
        Args:
            data: Price series (typically close prices)
            
        Returns:
            Series containing SMA values
        """
        if len(data) < self.period:
            raise DataError(f"Insufficient data: need {self.period}, got {len(data)}")
        
        result = data.rolling(window=self.period).mean()
        
        self.logger.debug(f"Calculated SMA({self.period}) for {len(data)} periods")
        return result
    
    def get_trend_direction(self, data: pd.Series) -> str:
        """
        Get current trend direction.
        
        Args:
            data: Price series
            
        Returns:
            Trend direction: 'uptrend', 'downtrend', or 'sideways'
        """
        sma = self.calculate(data)
        
        if len(sma) < 2:
            return "sideways"
        
        current = sma.iloc[-1]
        previous = sma.iloc[-2]
        
        if pd.isna(current) or pd.isna(previous):
            return "sideways"
        
        if current > previous:
            return "uptrend"
        elif current < previous:
            return "downtrend"
        else:
            return "sideways"


class ExponentialMovingAverage(TrendIndicator):
    """
    Exponential Moving Average (EMA) indicator.
    
    Calculates exponentially weighted moving average that gives more weight to recent prices.
    """
    
    def __init__(self, period: int, config: Dict[str, Any]):
        """
        Initialize Exponential Moving Average indicator.
        
        Args:
            period: Number of periods for calculation
            config: Configuration dictionary
        """
        super().__init__(f"ema_{period}", config)
        self.period = period
        self.alpha = 2.0 / (period + 1)
        self._validate_parameters()
    
    def _validate_parameters(self) -> None:
        """Validate indicator parameters."""
        if self.period < 2:
            raise ValidationError("Period must be at least 2")
        
        if self.period > 500:
            raise ValidationError("Period cannot exceed 500")
    
    def calculate(self, data: pd.Series) -> pd.Series:
        """
        Calculate Exponential Moving Average.
        
        Args:
            data: Price series
            
        Returns:
            Series containing EMA values
        """
        if len(data) < self.period:
            raise DataError(f"Insufficient data: need {self.period}, got {len(data)}")
        
        result = data.ewm(span=self.period).mean()
        
        self.logger.debug(f"Calculated EMA({self.period}) for {len(data)} periods")
        return result
    
    def get_trend_direction(self, data: pd.Series) -> str:
        """
        Get current trend direction.
        
        Args:
            data: Price series
            
        Returns:
            Trend direction: 'uptrend', 'downtrend', or 'sideways'
        """
        ema = self.calculate(data)
        
        if len(ema) < 2:
            return "sideways"
        
        current = ema.iloc[-1]
        previous = ema.iloc[-2]
        
        if pd.isna(current) or pd.isna(previous):
            return "sideways"
        
        if current > previous:
            return "uptrend"
        elif current < previous:
            return "downtrend"
        else:
            return "sideways"


__all__ = ["MovingAverage", "ExponentialMovingAverage"]
