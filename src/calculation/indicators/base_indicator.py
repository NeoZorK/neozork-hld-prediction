# -*- coding: utf-8 -*-
# src/calculation/indicators/base_indicator.py

"""
Base indicator class with price_type support.
Provides common functionality for all indicators.
"""

import pandas as pd
from enum import Enum
from typing import Optional, Union
from src.common import logger


class PriceType(Enum):
    """Enum for price type selection in indicator calculations."""
    OPEN = "open"
    CLOSE = "close"


class BaseIndicator:
    """Base class for all indicators with price_type support."""
    
    def __init__(self, price_type: Union[PriceType, str] = PriceType.CLOSE):
        """
        Initialize indicator with price type.
        
        Args:
            price_type: Price type to use for calculations ('open' or 'close')
        """
        if isinstance(price_type, str):
            self.price_type = PriceType.OPEN if price_type.lower() == 'open' else PriceType.CLOSE
        else:
            self.price_type = price_type
    
    def get_price_series(self, df: pd.DataFrame) -> pd.Series:
        """
        Get the appropriate price series based on price_type.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            Price series (Open or Close)
        """
        if self.price_type == PriceType.OPEN:
            return df['Open']
        else:
            return df['Close']
    
    def get_price_name(self) -> str:
        """Get the name of the selected price type."""
        return self.price_type.value.title()
    
    def validate_data(self, df: pd.DataFrame, min_periods: int = 1) -> bool:
        """
        Validate that DataFrame has required data for calculation.
        
        Args:
            df: DataFrame to validate
            min_periods: Minimum number of periods required
            
        Returns:
            True if data is valid, False otherwise
        """
        required_cols = ['Open', 'High', 'Low', 'Close']
        if not all(col in df.columns for col in required_cols):
            logger.print_warning(f"Missing required columns: {required_cols}")
            return False
        
        if len(df) < min_periods:
            logger.print_warning(f"Not enough data for calculation. Need at least {min_periods} points, got {len(df)}")
            return False
        
        return True
    
    def calculate(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Calculate indicator values. Must be implemented by subclasses.
        
        Args:
            df: DataFrame with OHLCV data
            **kwargs: Additional parameters for calculation
            
        Returns:
            DataFrame with calculated indicator values
        """
        raise NotImplementedError("Subclasses must implement calculate method")
    
    def apply_rule(self, df: pd.DataFrame, point: float, **kwargs) -> pd.DataFrame:
        """
        Apply trading rule logic. Must be implemented by subclasses.
        
        Args:
            df: DataFrame with OHLCV data
            point: Instrument point size
            **kwargs: Additional parameters for rule
            
        Returns:
            DataFrame with trading signals and levels
        """
        raise NotImplementedError("Subclasses must implement apply_rule method")


def parse_price_type(price_type_str: str) -> PriceType:
    """
    Parse price type string to PriceType enum.
    
    Args:
        price_type_str: String representation of price type
        
    Returns:
        PriceType enum value
    """
    if price_type_str.lower() == 'open':
        return PriceType.OPEN
    elif price_type_str.lower() == 'close':
        return PriceType.CLOSE
    else:
        raise ValueError(f"Invalid price type: {price_type_str}. Must be 'open' or 'close'")


def parse_indicator_rule(rule_str: str) -> tuple:
    """
    Parse indicator rule string to extract parameters.
    
    Args:
        rule_str: Rule string like 'indicator(param1,param2,price_type)'
        
    Returns:
        Tuple of (indicator_name, parameters, price_type)
    """
    try:
        # Extract indicator name and parameters
        if '(' in rule_str and rule_str.endswith(')'):
            name_part = rule_str[:rule_str.find('(')]
            params_part = rule_str[rule_str.find('(')+1:rule_str.rfind(')')]
            
            # Split parameters
            params = [p.strip() for p in params_part.split(',') if p.strip()]
            
            # Check if last parameter is price_type
            price_type = PriceType.CLOSE  # Default
            if params and params[-1].lower() in ['open', 'close']:
                price_type = parse_price_type(params[-1])
                params = params[:-1]  # Remove price_type from params
            
            return name_part, params, price_type
        else:
            return rule_str, [], PriceType.CLOSE
            
    except Exception as e:
        raise ValueError(f"Invalid rule format: {rule_str}. Error: {e}") 