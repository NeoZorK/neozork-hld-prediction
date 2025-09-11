# -*- coding: utf-8 -*-
"""
File Analyzer for NeoZork Interactive ML Trading Strategy Development.

This module provides utilities for analyzing files and folders to extract
detailed information about data sources, file sizes, row counts, date ranges,
and symbols.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import glob
import json
from datetime import datetime
import colorama
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.common.logger import print_info, print_warning, print_error, print_success, print_debug

class FileAnalyzer:
    """
    Comprehensive file and folder analyzer for data sources.
    
    Features:
    - Analyze file sizes and counts
    - Extract row counts from data files
    - Determine date ranges and timeframes
    - Extract symbols and sources from filenames
    - Calculate folder sizes and statistics
    """
    
    def __init__(self):
        """Initialize the file analyzer."""
        self.project_root = PROJECT_ROOT
        self.data_root = self.project_root / "data"
    
    def analyze_csv_converted_folder(self) -> Dict[str, Any]:
        """
        Analyze CSV converted folder for detailed information.
        
        Returns:
            Dictionary with detailed folder and file information
        """
        csv_dir = self.data_root / "cache" / "csv_converted"
        
        if not csv_dir.exists():
            return {
                "status": "error",
                "message": "CSV converted directory not found",
                "folder_info": {},
                "files_info": {},
                "symbols": []
            }
        
        # Get folder information
        folder_info = self._get_folder_info(csv_dir)
        
        # Get files information
        files_info = {}
        symbols = set()
        
        parquet_files = list(csv_dir.glob("*.parquet"))
        
        for file_path in parquet_files:
            file_info = self._analyze_parquet_file(file_path)
            if file_info:
                files_info[file_path.name] = file_info
                # Extract symbol from filename
                symbol = self._extract_symbol_from_filename(file_path.name)
                if symbol:
                    symbols.add(symbol)
        
        return {
            "status": "success",
            "folder_info": folder_info,
            "files_info": files_info,
            "symbols": sorted(list(symbols))
        }
    
    def analyze_raw_parquet_folder(self) -> Dict[str, Any]:
        """
        Analyze raw parquet folder for detailed information.
        
        Returns:
            Dictionary with detailed folder and file information
        """
        raw_dir = self.data_root / "raw_parquet"
        
        if not raw_dir.exists():
            return {
                "status": "error",
                "message": "Raw parquet directory not found",
                "folder_info": {},
                "files_info": {},
                "sources": [],
                "symbols_by_source": {}
            }
        
        # Get folder information
        folder_info = self._get_folder_info(raw_dir)
        
        # Get files information
        files_info = {}
        sources = set()
        symbols_by_source = {}
        
        parquet_files = list(raw_dir.glob("*.parquet"))
        
        for file_path in parquet_files:
            file_info = self._analyze_parquet_file(file_path)
            if file_info:
                files_info[file_path.name] = file_info
                
                # Extract source and symbol from filename
                source, symbol = self._extract_source_and_symbol_from_filename(file_path.name)
                if source:
                    sources.add(source)
                    if source not in symbols_by_source:
                        symbols_by_source[source] = set()
                    if symbol:
                        symbols_by_source[source].add(symbol)
        
        # Convert sets to sorted lists
        for source in symbols_by_source:
            symbols_by_source[source] = sorted(list(symbols_by_source[source]))
        
        return {
            "status": "success",
            "folder_info": folder_info,
            "files_info": files_info,
            "sources": sorted(list(sources)),
            "symbols_by_source": symbols_by_source
        }
    
    def analyze_indicators_folder(self) -> Dict[str, Any]:
        """
        Analyze indicators folder for detailed information.
        
        Returns:
            Dictionary with detailed folder and file information
        """
        indicators_dir = self.data_root / "indicators"
        
        if not indicators_dir.exists():
            return {
                "status": "error",
                "message": "Indicators directory not found",
                "folder_info": {},
                "subfolders_info": {},
                "indicators": []
            }
        
        # Get folder information
        folder_info = self._get_folder_info(indicators_dir)
        
        # Analyze subfolders
        subfolders_info = {}
        indicators = set()
        
        for subdir in ["parquet", "csv", "json"]:
            subdir_path = indicators_dir / subdir
            if subdir_path.exists():
                subfolder_info = self._get_folder_info(subdir_path)
                files_info = {}
                
                # Get files based on subdirectory type
                if subdir == "parquet":
                    pattern = "*.parquet"
                elif subdir == "csv":
                    pattern = "*.csv"
                else:  # json
                    pattern = "*.json"
                
                files = list(subdir_path.glob(pattern))
                
                for file_path in files:
                    file_info = self._analyze_data_file(file_path)
                    if file_info:
                        files_info[file_path.name] = file_info
                        # Extract indicator name from filename
                        indicator = self._extract_indicator_from_filename(file_path.name)
                        if indicator:
                            indicators.add(indicator)
                
                subfolder_info["files_info"] = files_info
                subfolders_info[subdir] = subfolder_info
        
        return {
            "status": "success",
            "folder_info": folder_info,
            "subfolders_info": subfolders_info,
            "indicators": sorted(list(indicators))
        }
    
    def analyze_cleaned_data_folder(self) -> Dict[str, Any]:
        """
        Analyze cleaned data folder for detailed information.
        
        Returns:
            Dictionary with detailed folder and file information
        """
        cleaned_dir = self.data_root / "cleaned_data"
        
        if not cleaned_dir.exists():
            return {
                "status": "error",
                "message": "Cleaned data directory not found",
                "folder_info": {},
                "files_info": {},
                "symbols": [],
                "save_dates": []
            }
        
        # Get folder information
        folder_info = self._get_folder_info(cleaned_dir)
        
        # Get files information
        files_info = {}
        symbols = set()
        save_dates = []
        
        parquet_files = list(cleaned_dir.glob("*.parquet"))
        
        for file_path in parquet_files:
            file_info = self._analyze_parquet_file(file_path)
            if file_info:
                files_info[file_path.name] = file_info
                
                # Extract symbol from filename
                symbol = self._extract_symbol_from_filename(file_path.name)
                if symbol:
                    symbols.add(symbol)
                
                # Extract save date from filename
                save_date = self._extract_save_date_from_filename(file_path.name)
                if save_date:
                    save_dates.append(save_date)
        
        return {
            "status": "success",
            "folder_info": folder_info,
            "files_info": files_info,
            "symbols": sorted(list(symbols)),
            "save_dates": sorted(save_dates)
        }
    
    def _get_folder_info(self, folder_path: Path) -> Dict[str, Any]:
        """Get detailed information about a folder."""
        try:
            # Count files
            file_count = len(list(folder_path.glob("*")))
            
            # Calculate folder size
            folder_size = sum(f.stat().st_size for f in folder_path.rglob('*') if f.is_file())
            folder_size_mb = folder_size / (1024 * 1024)
            
            # Get modification time
            mod_time = datetime.fromtimestamp(folder_path.stat().st_mtime)
            
            return {
                "path": str(folder_path),
                "file_count": file_count,
                "size_mb": round(folder_size_mb, 2),
                "modified": mod_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print_error(f"Error analyzing folder {folder_path}: {e}")
            return {
                "path": str(folder_path),
                "file_count": 0,
                "size_mb": 0,
                "modified": "Unknown"
            }
    
    def _analyze_parquet_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a parquet file for detailed information."""
        try:
            # Get file size
            file_size = file_path.stat().st_size / (1024 * 1024)  # MB
            
            # Load parquet file to get row count and date range
            df = pd.read_parquet(file_path)
            row_count = len(df)
            
            # Get date range
            start_date, end_date, timeframes = self._get_date_range_from_dataframe(df)
            
            # Extract timeframe from filename
            timeframe_from_filename = self._extract_timeframe_from_filename(file_path.name)
            
            # Use timeframe from filename if available, otherwise use timeframes from data
            if timeframe_from_filename:
                final_timeframes = [timeframe_from_filename]
            else:
                final_timeframes = timeframes
            
            return {
                "file_path": str(file_path),
                "size_mb": round(file_size, 2),
                "rows": row_count,
                "start_date": start_date,
                "end_date": end_date,
                "timeframes": final_timeframes,
                "columns": list(df.columns)
            }
        except Exception as e:
            print_error(f"Error analyzing parquet file {file_path}: {e}")
            return None
    
    def _analyze_data_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a data file (parquet, csv, json) for detailed information."""
        try:
            # Get file size
            file_size = file_path.stat().st_size / (1024 * 1024)  # MB
            
            # Load file based on extension
            if file_path.suffix == '.parquet':
                df = pd.read_parquet(file_path)
            elif file_path.suffix == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix == '.json':
                df = pd.read_json(file_path)
            else:
                return None
            
            row_count = len(df)
            
            # Get date range
            start_date, end_date, timeframes = self._get_date_range_from_dataframe(df)
            
            # Extract timeframe from filename
            timeframe_from_filename = self._extract_timeframe_from_filename(file_path.name)
            
            # Use timeframe from filename if available, otherwise use timeframes from data
            if timeframe_from_filename:
                final_timeframes = [timeframe_from_filename]
            else:
                final_timeframes = timeframes
            
            return {
                "file_path": str(file_path),
                "size_mb": round(file_size, 2),
                "rows": row_count,
                "start_date": start_date,
                "end_date": end_date,
                "timeframes": final_timeframes,
                "columns": list(df.columns),
                "file_type": file_path.suffix[1:]  # Remove the dot
            }
        except Exception as e:
            print_error(f"Error analyzing data file {file_path}: {e}")
            return None
    
    def _get_date_range_from_dataframe(self, df: pd.DataFrame) -> Tuple[str, str, List[str]]:
        """Extract date range and timeframes from a dataframe."""
        try:
            # First check if the index is datetime
            if isinstance(df.index, pd.DatetimeIndex):
                time_series = df.index
            else:
                # Look for time columns
                time_col = None
                for col in ['timestamp', 'Timestamp', 'time', 'Time', 'datetime', 'DateTime']:
                    if col in df.columns:
                        time_col = col
                        break
                
                if time_col and not df[time_col].empty:
                    # Convert to datetime if needed
                    if not pd.api.types.is_datetime64_any_dtype(df[time_col]):
                        time_series = pd.to_datetime(df[time_col], errors='coerce')
                    else:
                        time_series = df[time_col]
                else:
                    # No time data available
                    return "No time data", "No time data", ["No time data"]
            
            if not time_series.empty:
                start_date = time_series.min()
                end_date = time_series.max()
                
                # Get timeframes (sample of unique hours)
                timeframes = time_series.floor('h').value_counts().index.tolist()[:5]
                timeframes = [str(tf) for tf in timeframes]
                
                return str(start_date), str(end_date), timeframes
            else:
                return "No time data", "No time data", ["No time data"]
        except Exception as e:
            print_error(f"Error extracting date range: {e}")
            return "No time data", "No time data", ["No time data"]
    
    def _extract_symbol_from_filename(self, filename: str) -> Optional[str]:
        """Extract symbol from filename."""
        try:
            # Remove extension
            name = Path(filename).stem
            
            # Look for patterns like CSVExport_SYMBOL_PERIOD_...
            if "CSVExport_" in name:
                parts = name.split("_")
                if len(parts) >= 2:
                    return parts[1].upper()
            
            # Look for patterns like cleaned_csv_converted_SYMBOL_...
            if "cleaned_csv_converted_" in name:
                parts = name.split("_")
                if len(parts) >= 4:
                    return parts[3].upper()
            
            # Look for patterns like SYMBOL_PERIOD_...
            if "_PERIOD_" in name:
                parts = name.split("_")
                if len(parts) >= 2:
                    return parts[0].upper()
            
            return None
        except Exception as e:
            print_error(f"Error extracting symbol from {filename}: {e}")
            return None
    
    def _extract_timeframe_from_filename(self, filename: str) -> Optional[str]:
        """Extract timeframe from filename."""
        try:
            # Remove extension
            name = Path(filename).stem
            
            # Look for patterns like CSVExport_SYMBOL_PERIOD_TIMEFRAME
            if "CSVExport_" in name and "_PERIOD_" in name:
                parts = name.split("_")
                if len(parts) >= 4:
                    return parts[3].upper()
            
            # Look for patterns like cleaned_csv_converted_TIMEFRAME_...
            if "cleaned_csv_converted_" in name:
                parts = name.split("_")
                if len(parts) >= 3:
                    return parts[2].upper()
            
            return None
        except Exception as e:
            print_error(f"Error extracting timeframe from {filename}: {e}")
            return None
    
    def _extract_source_and_symbol_from_filename(self, filename: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract source and symbol from filename."""
        try:
            # Remove extension
            name = Path(filename).stem
            
            # Look for patterns like source_SYMBOL_TIMEFRAME
            parts = name.split("_")
            if len(parts) >= 2:
                source = parts[0].lower()
                symbol = parts[1].upper()
                return source, symbol
            
            return None, None
        except Exception as e:
            print_error(f"Error extracting source and symbol from {filename}: {e}")
            return None, None
    
    def _extract_indicator_from_filename(self, filename: str) -> Optional[str]:
        """Extract indicator name from filename."""
        try:
            # Remove extension
            name = Path(filename).stem
            
            # Look for patterns like DEMO_RSI, UNKNOWN_D1_PressureVector
            if "_" in name:
                parts = name.split("_")
                if len(parts) >= 2:
                    # Return the last part as indicator name
                    return parts[-1].upper()
            
            return name.upper()
        except Exception as e:
            print_error(f"Error extracting indicator from {filename}: {e}")
            return None
    
    def _extract_save_date_from_filename(self, filename: str) -> Optional[str]:
        """Extract save date from filename."""
        try:
            # Remove extension
            name = Path(filename).stem
            
            # Look for patterns like cleaned_csv_converted_MN1_20250904_182044
            if "cleaned_csv_converted_" in name:
                parts = name.split("_")
                if len(parts) >= 5:
                    # Extract date part (format: YYYYMMDD)
                    date_part = parts[4]
                    if len(date_part) == 8 and date_part.isdigit():
                        # Format as YYYY-MM-DD
                        year = date_part[:4]
                        month = date_part[4:6]
                        day = date_part[6:8]
                        return f"{year}-{month}-{day}"
            
            return None
        except Exception as e:
            print_error(f"Error extracting save date from {filename}: {e}")
            return None
