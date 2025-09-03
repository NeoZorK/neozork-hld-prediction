# -*- coding: utf-8 -*-
# src/data/acquisition/ranges.py

"""
Data acquisition ranges functionality.
Handles date range calculations and validation for data acquisition.
All comments are in English.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd


class DataAcquisitionRanges:
    """Handles date range calculations and validation."""
    
    def __init__(self):
        """Initialize the ranges module."""
        self.default_start_date = datetime.now() - timedelta(days=30)
        self.default_end_date = datetime.now()
    
    def calculate_date_range(self, start_date: Optional[str] = None, 
                           end_date: Optional[str] = None, 
                           days_back: Optional[int] = None) -> Tuple[datetime, datetime]:
        """
        Calculate start and end dates for data acquisition.
        
        Args:
            start_date: Start date string (optional)
            end_date: End date string (optional)
            days_back: Number of days to go back from end date (optional)
            
        Returns:
            Tuple of (start_date, end_date) as datetime objects
        """
        # Parse end date
        if end_date:
            try:
                end_dt = pd.to_datetime(end_date)
            except:
                end_dt = self.default_end_date
        else:
            end_dt = self.default_end_date
        
        # Parse start date
        if start_date:
            try:
                start_dt = pd.to_datetime(start_date)
            except:
                start_dt = self._calculate_start_date(end_dt, days_back)
        else:
            start_dt = self._calculate_start_date(end_dt, days_back)
        
        # Validate date range
        if start_dt >= end_dt:
            start_dt = end_dt - timedelta(days=1)
        
        return start_dt, end_dt
    
    def _calculate_start_date(self, end_date: datetime, days_back: Optional[int]) -> datetime:
        """Calculate start date based on end date and days back."""
        if days_back is not None:
            return end_date - timedelta(days=days_back)
        else:
            return self.default_start_date
    
    def get_available_date_ranges(self, instrument: str) -> List[Dict[str, Any]]:
        """
        Get available date ranges for an instrument.
        
        Args:
            instrument: Name of the instrument
            
        Returns:
            List of available date ranges
        """
        # This is a placeholder - in practice you would scan available data files
        # and determine what date ranges are available
        
        ranges = [
            {
                'start_date': '2024-01-01',
                'end_date': '2024-12-31',
                'data_points': 10000,
                'frequency': '1H'
            },
            {
                'start_date': '2023-01-01',
                'end_date': '2023-12-31',
                'data_points': 8760,
                'frequency': '1H'
            }
        ]
        
        return ranges
    
    def validate_date_range(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Validate a date range for data acquisition.
        
        Args:
            start_date: Start date string
            end_date: End date string
            
        Returns:
            Dictionary with validation results
        """
        try:
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            
            # Calculate duration
            duration = end_dt - start_dt
            duration_days = duration.days
            
            # Validation rules
            is_valid = True
            warnings = []
            errors = []
            
            if start_dt >= end_dt:
                is_valid = False
                errors.append("Start date must be before end date")
            
            if duration_days > 365:
                warnings.append("Large date range may take significant time to process")
            
            if duration_days < 1:
                warnings.append("Very small date range may result in insufficient data")
            
            if start_dt < datetime(2000, 1, 1):
                warnings.append("Start date is very old, data may not be available")
            
            if end_dt > datetime.now() + timedelta(days=1):
                warnings.append("End date is in the future")
            
            return {
                'is_valid': is_valid,
                'start_date': start_dt,
                'end_date': end_dt,
                'duration_days': duration_days,
                'warnings': warnings,
                'errors': errors
            }
            
        except Exception as e:
            return {
                'is_valid': False,
                'start_date': None,
                'end_date': None,
                'duration_days': 0,
                'warnings': [],
                'errors': [f"Date parsing error: {str(e)}"]
            }
    
    def split_large_range(self, start_date: datetime, end_date: datetime, 
                         max_days: int = 30) -> List[Tuple[datetime, datetime]]:
        """
        Split a large date range into smaller chunks.
        
        Args:
            start_date: Start date
            end_date: End date
            max_days: Maximum days per chunk
            
        Returns:
            List of (start_date, end_date) tuples
        """
        ranges = []
        current_start = start_date
        
        while current_start < end_date:
            current_end = min(current_start + timedelta(days=max_days), end_date)
            ranges.append((current_start, current_end))
            current_start = current_end
        
        return ranges
    
    def get_optimal_chunk_size(self, total_days: int, memory_limit_mb: int = 1024) -> int:
        """
        Calculate optimal chunk size based on available memory.
        
        Args:
            total_days: Total number of days to process
            memory_limit_mb: Memory limit in MB
            
        Returns:
            Optimal chunk size in days
        """
        # Simple heuristic: assume 1MB per day of data
        # In practice, this would be more sophisticated
        estimated_mb_per_day = 1
        optimal_days = max(1, memory_limit_mb // estimated_mb_per_day)
        
        # Cap at reasonable limits
        optimal_days = min(optimal_days, 90)  # Max 90 days per chunk
        optimal_days = max(optimal_days, 1)   # Min 1 day per chunk
        
        return optimal_days
