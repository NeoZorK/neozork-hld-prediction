"""
Time Utilities

This module provides time-related utility functions.
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Union, Optional, List
import logging

from ..core.exceptions import ValidationError


logger = logging.getLogger(__name__)


def parse_datetime(date_str: str, format_str: Optional[str] = None) -> datetime:
    """
    Parse datetime string.
    
    Args:
        date_str: Date string to parse
        format_str: Format string (if None, tries common formats)
        
    Returns:
        Parsed datetime
    """
    if format_str:
        try:
            return datetime.strptime(date_str, format_str)
        except ValueError as e:
            raise ValidationError(f"Failed to parse datetime '{date_str}' with format '{format_str}': {e}")
    
    # Try common formats
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValidationError(f"Could not parse datetime: {date_str}")


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime to string.
    
    Args:
        dt: Datetime to format
        format_str: Format string
        
    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_str)


def get_business_days(start_date: datetime, end_date: datetime) -> List[datetime]:
    """
    Get business days between two dates.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        List of business days
    """
    business_days = pd.bdate_range(start=start_date, end=end_date)
    return [dt.to_pydatetime() for dt in business_days]


def add_business_days(date: datetime, days: int) -> datetime:
    """
    Add business days to a date.
    
    Args:
        date: Base date
        days: Number of business days to add
        
    Returns:
        New date
    """
    if days == 0:
        return date
    
    # Use pandas business day functionality
    result = pd.Timestamp(date) + pd.Timedelta(days=days)
    return result.to_pydatetime()


def get_market_hours(timezone: str = "US/Eastern") -> dict:
    """
    Get market trading hours for timezone.
    
    Args:
        timezone: Market timezone
        
    Returns:
        Dictionary with market hours
    """
    # Common market hours (simplified)
    market_hours = {
        "US/Eastern": {"open": "09:30", "close": "16:00"},
        "Europe/London": {"open": "08:00", "close": "16:30"},
        "Asia/Tokyo": {"open": "09:00", "close": "15:00"},
    }
    
    return market_hours.get(timezone, {"open": "09:00", "close": "17:00"})


def is_market_open(dt: datetime, timezone: str = "US/Eastern") -> bool:
    """
    Check if market is open at given datetime.
    
    Args:
        dt: Datetime to check
        timezone: Market timezone
        
    Returns:
        True if market is open, False otherwise
    """
    # Simplified check - only considers time, not holidays
    hours = get_market_hours(timezone)
    
    # Check if it's a weekday
    if dt.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return False
    
    # Check time
    time_str = dt.strftime("%H:%M")
    return hours["open"] <= time_str <= hours["close"]


__all__ = [
    "parse_datetime",
    "format_datetime",
    "get_business_days",
    "add_business_days",
    "get_market_hours",
    "is_market_open",
]
