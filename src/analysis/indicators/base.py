"""
Base classes for technical indicators in Neozork HLD Prediction system.

This module provides abstract base classes for all technical indicators.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, Tuple
import pandas as pd
import numpy as np
from ...core.base import BaseComponent
from ...core.exceptions import ValidationError


class BaseIndicator(BaseComponent):
    """Base class for all technical indicators."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.parameters = config.get("parameters", {})
        self.lookback_periods = config.get("lookback_periods", 14)
        self.min_data_points = config.get("min_data_points", 1)
        
    @abstractmethod
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """Calculate indicator values for the given data."""
        pass
    
    @abstractmethod
    def validate_input(self, data: pd.DataFrame) -> bool:
        """Validate input data before calculation."""
        pass
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get current indicator parameters."""
        return self.parameters.copy()
    
    def set_parameters(self, parameters: Dict[str, Any]):
        """Set indicator parameters."""
        self.parameters.update(parameters)
        if "lookback_periods" in parameters:
            self.lookback_periods = parameters["lookback_periods"]
        if "min_data_points" in parameters:
            self.min_data_points = parameters["min_data_points"]
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the indicator."""
        return {
            "name": self.name,
            "class": self.__class__.__name__,
            "parameters": self.parameters,
            "lookback_periods": self.lookback_periods,
            "min_data_points": self.min_data_points
        }


class TrendIndicator(BaseIndicator):
    """Base class for trend-following indicators."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.trend_direction = None
        self.trend_strength = 0.0
        
    def get_trend_info(self) -> Dict[str, Any]:
        """Get current trend information."""
        return {
            "direction": self.trend_direction,
            "strength": self.trend_strength,
            "indicator_name": self.name
        }
    
    def is_uptrend(self) -> bool:
        """Check if current trend is up."""
        return self.trend_direction == "up"
    
    def is_downtrend(self) -> bool:
        """Check if current trend is down."""
        return self.trend_direction == "down"
    
    def is_sideways(self) -> bool:
        """Check if current trend is sideways."""
        return self.trend_direction == "sideways"


class MomentumIndicator(BaseIndicator):
    """Base class for momentum indicators."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.overbought_threshold = config.get("overbought_threshold", 70)
        self.oversold_threshold = config.get("oversold_threshold", 30)
        
    def is_overbought(self, value: float) -> bool:
        """Check if value indicates overbought condition."""
        return value > self.overbought_threshold
    
    def is_oversold(self, value: float) -> bool:
        """Check if value indicates oversold condition."""
        return value < self.oversold_threshold
    
    def get_momentum_info(self) -> Dict[str, Any]:
        """Get momentum information."""
        return {
            "overbought_threshold": self.overbought_threshold,
            "oversold_threshold": self.oversold_threshold,
            "indicator_name": self.name
        }


class VolatilityIndicator(BaseIndicator):
    """Base class for volatility indicators."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.volatility_period = config.get("volatility_period", 20)
        self.volatility_multiplier = config.get("volatility_multiplier", 2.0)
        
    def get_volatility_info(self) -> Dict[str, Any]:
        """Get volatility information."""
        return {
            "volatility_period": self.volatility_period,
            "volatility_multiplier": self.volatility_multiplier,
            "indicator_name": self.name
        }
    
    def calculate_bands(self, data: pd.Series) -> Tuple[pd.Series, pd.Series]:
        """Calculate upper and lower volatility bands."""
        # This is a basic implementation - subclasses should override
        mean = data.rolling(window=self.volatility_period).mean()
        std = data.rolling(window=self.volatility_period).std()
        
        upper_band = mean + (std * self.volatility_multiplier)
        lower_band = mean - (std * self.volatility_multiplier)
        
        return upper_band, lower_band
