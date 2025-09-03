"""
Validation Utilities

This module provides data validation utilities.
"""

import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional, Union
import logging

from ..core.exceptions import ValidationError


logger = logging.getLogger(__name__)


def validate_dataframe(df: pd.DataFrame, required_columns: Optional[List[str]] = None) -> None:
    """
    Validate DataFrame structure and content.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
    """
    if df.empty:
        raise ValidationError("DataFrame is empty")
    
    if required_columns:
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValidationError(f"Missing required columns: {missing_columns}")
    
    logger.debug(f"Validated DataFrame with {len(df)} rows and {len(df.columns)} columns")


def validate_ohlcv_data(df: pd.DataFrame) -> None:
    """
    Validate OHLCV (Open, High, Low, Close, Volume) data.
    
    Args:
        df: DataFrame with OHLCV data
    """
    required_columns = ['open', 'high', 'low', 'close']
    validate_dataframe(df, required_columns)
    
    # Check for logical consistency
    for i, row in df.iterrows():
        if pd.notna(row['high']) and pd.notna(row['low']) and row['high'] < row['low']:
            raise ValidationError(f"Invalid OHLCV data at index {i}: high < low")
        
        if pd.notna(row['open']) and pd.notna(row['high']) and row['open'] > row['high']:
            raise ValidationError(f"Invalid OHLCV data at index {i}: open > high")
        
        if pd.notna(row['open']) and pd.notna(row['low']) and row['open'] < row['low']:
            raise ValidationError(f"Invalid OHLCV data at index {i}: open < low")
        
        if pd.notna(row['close']) and pd.notna(row['high']) and row['close'] > row['high']:
            raise ValidationError(f"Invalid OHLCV data at index {i}: close > high")
        
        if pd.notna(row['close']) and pd.notna(row['low']) and row['close'] < row['low']:
            raise ValidationError(f"Invalid OHLCV data at index {i}: close < low")
    
    logger.debug("Validated OHLCV data consistency")


def validate_numeric_range(value: Union[int, float], min_val: Optional[float] = None, 
                          max_val: Optional[float] = None, name: str = "value") -> None:
    """
    Validate numeric value is within specified range.
    
    Args:
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        name: Name of the value for error messages
    """
    if min_val is not None and value < min_val:
        raise ValidationError(f"{name} must be >= {min_val}, got {value}")
    
    if max_val is not None and value > max_val:
        raise ValidationError(f"{name} must be <= {max_val}, got {value}")


def validate_positive(value: Union[int, float], name: str = "value") -> None:
    """
    Validate value is positive.
    
    Args:
        value: Value to validate
        name: Name of the value for error messages
    """
    if value <= 0:
        raise ValidationError(f"{name} must be positive, got {value}")


def validate_percentage(value: Union[int, float], name: str = "percentage") -> None:
    """
    Validate value is a valid percentage (0-100).
    
    Args:
        value: Value to validate
        name: Name of the value for error messages
    """
    validate_numeric_range(value, 0.0, 100.0, name)


def check_missing_data(df: pd.DataFrame, threshold: float = 0.1) -> Dict[str, float]:
    """
    Check for missing data in DataFrame.
    
    Args:
        df: DataFrame to check
        threshold: Threshold for warning about missing data
        
    Returns:
        Dictionary with missing data percentages by column
    """
    missing_pct = (df.isnull().sum() / len(df)) * 100
    
    for col, pct in missing_pct.items():
        if pct > threshold * 100:
            logger.warning(f"Column '{col}' has {pct:.1f}% missing data")
    
    return missing_pct.to_dict()


__all__ = [
    "validate_dataframe",
    "validate_ohlcv_data",
    "validate_numeric_range",
    "validate_positive",
    "validate_percentage",
    "check_missing_data",
]
