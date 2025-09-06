# -*- coding: utf-8 -*-
"""
Data Loader for NeoZork Interactive ML Trading Strategy Development.

This module handles loading data from various sources including:
- CSV converted data (.parquet files)
- Raw parquet data from exchanges
- Indicators data (parquet, csv, json)
- Cleaned data with multiple timeframes
"""

import os
import sys
import time
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import glob
import json

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.common.logger import print_info, print_warning, print_error, print_success, print_debug

class DataLoader:
    """
    Comprehensive data loader for multiple data sources.
    
    Features:
    - Load CSV converted data (.parquet)
    - Load raw parquet data from exchanges
    - Load indicators data (parquet, csv, json)
    - Load cleaned data with multiple timeframes
    - Progress tracking with ETA
    - Data validation and quality checks
    """
    
    def __init__(self):
        """Initialize the data loader."""
        self.project_root = PROJECT_ROOT
        self.data_root = self.project_root / "data"
        self.cache_root = self.data_root / "cache"
        self.raw_root = self.data_root / "raw_parquet"
        self.indicators_root = self.data_root / "indicators"
        self.cleaned_root = self.data_root / "cleaned_data"
        
        # Ensure data directories exist
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure all required data directories exist."""
        directories = [
            self.data_root,
            self.cache_root,
            self.raw_root,
            self.indicators_root,
            self.cleaned_root,
            self.cache_root / "csv_converted",
            self.indicators_root / "parquet",
            self.indicators_root / "csv",
            self.indicators_root / "json"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def load_csv_converted_data(self, symbol_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Load CSV converted data from parquet files.
        
        Args:
            symbol_filter: Optional filter for specific symbol (e.g., "eurusd")
            
        Returns:
            Dictionary containing loaded data and metadata
        """
        print_info("📁 Loading CSV converted data...")
        print_warning("This feature will be implemented in the next phase...")
        return {"status": "not_implemented", "message": "Feature coming soon"}
    
    def load_raw_parquet_data(self, symbol_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Load raw parquet data from exchanges.
        
        Args:
            symbol_filter: Optional filter for specific symbol (e.g., "btcusdt")
            
        Returns:
            Dictionary containing loaded data and metadata
        """
        print_info("📊 Loading raw parquet data...")
        print_warning("This feature will be implemented in the next phase...")
        return {"status": "not_implemented", "message": "Feature coming soon"}
    
    def load_indicators_data(self, symbol_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Load indicators data from parquet, csv, and json files.
        
        Args:
            symbol_filter: Optional filter for specific symbol (e.g., "aapl")
            
        Returns:
            Dictionary containing loaded data and metadata
        """
        print_info("📈 Loading indicators data...")
        print_warning("This feature will be implemented in the next phase...")
        return {"status": "not_implemented", "message": "Feature coming soon"}
    
    def load_cleaned_data(self, symbol_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Load cleaned data with multiple timeframes.
        
        Args:
            symbol_filter: Optional filter for specific symbol (e.g., "eurusd")
            
        Returns:
            Dictionary containing loaded data and metadata
        """
        print_info("✨ Loading cleaned data...")
        print_warning("This feature will be implemented in the next phase...")
        return {"status": "not_implemented", "message": "Feature coming soon"}
    
    def get_available_data_sources(self) -> Dict[str, List[str]]:
        """
        Get list of available data sources and files.
        
        Returns:
            Dictionary with available data sources and files
        """
        sources = {
            "csv_converted": [],
            "raw_parquet": [],
            "indicators": [],
            "cleaned_data": []
        }
        
        # Check CSV converted
        csv_dir = self.cache_root / "csv_converted"
        if csv_dir.exists():
            sources["csv_converted"] = [f.name for f in csv_dir.glob("*.parquet")]
        
        # Check raw parquet
        if self.raw_root.exists():
            sources["raw_parquet"] = [f.name for f in self.raw_root.glob("*.parquet")]
        
        # Check indicators
        if self.indicators_root.exists():
            for subdir in ["parquet", "csv", "json"]:
                subdir_path = self.indicators_root / subdir
                if subdir_path.exists():
                    sources["indicators"].extend([f.name for f in subdir_path.glob(f"*.{subdir}")])
        
        # Check cleaned data
        if self.cleaned_root.exists():
            sources["cleaned_data"] = [f.name for f in self.cleaned_root.glob("*.parquet")]
        
        return sources
