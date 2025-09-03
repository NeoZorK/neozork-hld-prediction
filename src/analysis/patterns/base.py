"""
Base Pattern Components

This module provides base classes for pattern analysis.
"""

import pandas as pd
from typing import Dict, Any, List, Optional
import numpy as np
from abc import ABC, abstractmethod

from ...core.base import BaseComponent
from ...core.exceptions import DataError, ValidationError


class BasePattern(BaseComponent, ABC):
    """
    Base class for pattern recognition components.
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize base pattern.
        
        Args:
            name: Name of the pattern
            config: Configuration dictionary
        """
        super().__init__(name, config)
        self.min_periods = config.get("min_periods", 10)
        self.confidence_threshold = config.get("confidence_threshold", 0.7)
    
    @abstractmethod
    def detect(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect pattern in data.
        
        Args:
            data: Input data
            
        Returns:
            List of detected pattern occurrences
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
        
        if len(data) < self.min_periods:
            raise DataError(f"Insufficient data: need {self.min_periods}, got {len(data)}")


class TrendPattern(BasePattern):
    """
    Trend pattern detector.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize trend pattern detector.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("trend_pattern", config)
        self.trend_window = config.get("trend_window", 20)
    
    def detect(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect trend patterns in data.
        
        Args:
            data: Input data with OHLCV columns
            
        Returns:
            List of detected trend patterns
        """
        self.validate_data(data)
        
        patterns = []
        close_prices = data['close'] if 'close' in data.columns else data.iloc[:, 0]
        
        # Simple trend detection using linear regression
        for i in range(self.trend_window, len(data)):
            window_data = close_prices.iloc[i-self.trend_window:i]
            x = np.arange(len(window_data))
            
            # Calculate linear regression slope
            slope, _ = np.polyfit(x, window_data, 1)
            
            # Determine trend direction and strength
            if abs(slope) > 0.01:  # Minimum slope threshold
                trend_type = "uptrend" if slope > 0 else "downtrend"
                confidence = min(abs(slope) * 100, 1.0)  # Normalize confidence
                
                if confidence >= self.confidence_threshold:
                    patterns.append({
                        'type': trend_type,
                        'start_index': i - self.trend_window,
                        'end_index': i,
                        'confidence': confidence,
                        'slope': slope
                    })
        
        self.logger.debug(f"Detected {len(patterns)} trend patterns")
        return patterns


__all__ = ["BasePattern", "TrendPattern"]
