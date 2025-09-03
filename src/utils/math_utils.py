"""
Mathematical Utilities

This module provides mathematical utility functions.
"""

import numpy as np
import pandas as pd
from typing import Union, List, Optional
import logging

from ..core.exceptions import ValidationError


logger = logging.getLogger(__name__)


def normalize(data: Union[pd.Series, np.ndarray], method: str = "minmax") -> Union[pd.Series, np.ndarray]:
    """
    Normalize data using specified method.
    
    Args:
        data: Data to normalize
        method: Normalization method ('minmax', 'zscore')
        
    Returns:
        Normalized data
    """
    if method == "minmax":
        min_val = np.min(data)
        max_val = np.max(data)
        if max_val == min_val:
            return np.zeros_like(data)
        return (data - min_val) / (max_val - min_val)
    
    elif method == "zscore":
        mean_val = np.mean(data)
        std_val = np.std(data)
        if std_val == 0:
            return np.zeros_like(data)
        return (data - mean_val) / std_val
    
    else:
        raise ValidationError(f"Unknown normalization method: {method}")


def calculate_returns(prices: Union[pd.Series, np.ndarray], periods: int = 1) -> Union[pd.Series, np.ndarray]:
    """
    Calculate returns for given periods.
    
    Args:
        prices: Price series
        periods: Number of periods for return calculation
        
    Returns:
        Returns series
    """
    if isinstance(prices, pd.Series):
        return prices.pct_change(periods=periods)
    else:
        return np.diff(prices, n=periods) / prices[:-periods]


def calculate_volatility(returns: Union[pd.Series, np.ndarray], window: int = 20) -> Union[pd.Series, np.ndarray]:
    """
    Calculate rolling volatility.
    
    Args:
        returns: Returns series
        window: Rolling window size
        
    Returns:
        Volatility series
    """
    if isinstance(returns, pd.Series):
        return returns.rolling(window=window).std() * np.sqrt(252)  # Annualized
    else:
        # Simple rolling standard deviation for numpy arrays
        volatility = []
        for i in range(window - 1, len(returns)):
            window_data = returns[i - window + 1:i + 1]
            vol = np.std(window_data) * np.sqrt(252)
            volatility.append(vol)
        return np.array([np.nan] * (window - 1) + volatility)


def safe_divide(numerator: Union[float, np.ndarray], denominator: Union[float, np.ndarray], 
                default: float = 0.0) -> Union[float, np.ndarray]:
    """
    Safely divide two numbers/arrays, handling division by zero.
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value for division by zero
        
    Returns:
        Division result
    """
    if isinstance(denominator, np.ndarray):
        result = np.divide(numerator, denominator, out=np.full_like(numerator, default), where=(denominator != 0))
        return result
    else:
        return numerator / denominator if denominator != 0 else default


def calculate_drawdown(prices: Union[pd.Series, np.ndarray]) -> Union[pd.Series, np.ndarray]:
    """
    Calculate drawdown series.
    
    Args:
        prices: Price series
        
    Returns:
        Drawdown series
    """
    if isinstance(prices, pd.Series):
        peak = prices.expanding().max()
        drawdown = (prices - peak) / peak
        return drawdown
    else:
        peak = np.maximum.accumulate(prices)
        drawdown = (prices - peak) / peak
        return drawdown


__all__ = [
    "normalize",
    "calculate_returns",
    "calculate_volatility",
    "safe_divide",
    "calculate_drawdown",
]
