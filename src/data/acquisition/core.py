# -*- coding: utf-8 -*-
# src/data/acquisition/core.py

"""
Core data acquisition functionality.
Handles the main data acquisition process and orchestration.
All comments are in English.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
import pandas as pd

from .csv import CSVDataAcquisition
from .cache import DataAcquisitionCache
from .ranges import DataAcquisitionRanges
from .utils import DataAcquisitionUtils


def acquire_data(instrument: str, mode: str = 'csv', 
                start_date: Optional[str] = None, end_date: Optional[str] = None,
                **kwargs) -> pd.DataFrame:
    """
    Main function to acquire data for a given instrument.
    
    Args:
        instrument: Name of the instrument (e.g., 'EURUSD', 'AAPL')
        mode: Data acquisition mode ('csv', 'api', 'database')
        start_date: Start date for data range (optional)
        end_date: End date for data range (optional)
        **kwargs: Additional arguments for specific modes
        
    Returns:
        DataFrame with acquired data
    """
    print(f"🚀 Starting data acquisition for {instrument}")
    print(f"📊 Mode: {mode}")
    
    # Initialize components
    csv_acquisition = CSVDataAcquisition()
    cache = DataAcquisitionCache()
    ranges = DataAcquisitionRanges()
    utils = DataAcquisitionUtils()
    
    # Check cache first
    cached_data = cache.get_cached_data(instrument, start_date, end_date)
    if cached_data is not None:
        print(f"✅ Found cached data for {instrument}")
        return cached_data
    
    # Acquire data based on mode
    if mode == 'csv':
        data = csv_acquisition.acquire_csv_data(instrument, start_date, end_date, **kwargs)
    else:
        print(f"❌ Unsupported mode: {mode}")
        return pd.DataFrame()
    
    if data is not None and not data.empty:
        # Cache the acquired data
        cache.cache_data(instrument, data, start_date, end_date)
        print(f"✅ Data acquisition completed for {instrument}")
        return data
    else:
        print(f"❌ Failed to acquire data for {instrument}")
        return pd.DataFrame()


class DataAcquisitionCore:
    """Core data acquisition orchestrator."""
    
    def __init__(self):
        """Initialize the core acquisition module."""
        self.csv_acquisition = CSVDataAcquisition()
        self.cache = DataAcquisitionCache()
        self.ranges = DataAcquisitionRanges()
        self.utils = DataAcquisitionUtils()
    
    def acquire_data(self, instrument: str, mode: str = 'csv', 
                    start_date: Optional[str] = None, end_date: Optional[str] = None,
                    **kwargs) -> pd.DataFrame:
        """
        Acquire data using the core acquisition module.
        
        Args:
            instrument: Name of the instrument
            mode: Data acquisition mode
            start_date: Start date for data range
            end_date: End date for data range
            **kwargs: Additional arguments
            
        Returns:
            DataFrame with acquired data
        """
        return acquire_data(instrument, mode, start_date, end_date, **kwargs)
    
    def get_available_instruments(self) -> List[str]:
        """Get list of available instruments."""
        return self.utils.get_available_instruments()
    
    def get_data_info(self, instrument: str) -> Dict[str, Any]:
        """Get information about available data for an instrument."""
        return self.utils.get_data_info(instrument)
