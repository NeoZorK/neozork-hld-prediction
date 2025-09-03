"""
Momentum Indicators Implementation

This module provides momentum analysis indicators.
"""

import pandas as pd
from typing import Dict, Any
import numpy as np

from .base import MomentumIndicator
from ...core.exceptions import DataError, ValidationError


class RSI(MomentumIndicator):
    """
    Relative Strength Index (RSI) indicator.
    
    Measures the speed and change of price movements.
    """
    
    def __init__(self, period: int, config: Dict[str, Any]):
        """
        Initialize RSI indicator.
        
        Args:
            period: Number of periods for calculation (typically 14)
            config: Configuration dictionary
        """
        super().__init__(f"rsi_{period}", config)
        self.period = period
        self.overbought_threshold = config.get("overbought_threshold", 70)
        self.oversold_threshold = config.get("oversold_threshold", 30)
        self._validate_parameters()
    
    def _validate_parameters(self) -> None:
        """Validate indicator parameters."""
        if self.period < 2:
            raise ValidationError("Period must be at least 2")
        
        if self.overbought_threshold <= self.oversold_threshold:
            raise ValidationError("Overbought threshold must be greater than oversold threshold")
    
    def calculate(self, data: pd.Series) -> pd.Series:
        """
        Calculate RSI values.
        
        Args:
            data: Price series
            
        Returns:
            Series containing RSI values (0-100)
        """
        if len(data) < self.period + 1:
            raise DataError(f"Insufficient data: need {self.period + 1}, got {len(data)}")
        
        # Calculate price changes
        delta = data.diff()
        
        # Separate gains and losses
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        # Calculate average gains and losses
        avg_gains = gains.rolling(window=self.period).mean()
        avg_losses = losses.rolling(window=self.period).mean()
        
        # Calculate RSI
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        
        self.logger.debug(f"Calculated RSI({self.period}) for {len(data)} periods")
        return rsi
    
    def is_overbought(self, data: pd.Series) -> bool:
        """
        Check if current RSI indicates overbought condition.
        
        Args:
            data: Price series
            
        Returns:
            True if overbought, False otherwise
        """
        rsi = self.calculate(data)
        current_rsi = rsi.iloc[-1]
        
        return not pd.isna(current_rsi) and current_rsi > self.overbought_threshold
    
    def is_oversold(self, data: pd.Series) -> bool:
        """
        Check if current RSI indicates oversold condition.
        
        Args:
            data: Price series
            
        Returns:
            True if oversold, False otherwise
        """
        rsi = self.calculate(data)
        current_rsi = rsi.iloc[-1]
        
        return not pd.isna(current_rsi) and current_rsi < self.oversold_threshold


__all__ = ["RSI"]
