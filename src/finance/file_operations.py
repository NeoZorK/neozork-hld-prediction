"""
Financial Analysis File Operations Module

This module handles reading and writing data in different formats (parquet, JSON, CSV)
for financial analysis. It provides a unified interface for data I/O operations
with proper error handling and format-specific optimizations.

Based on the file operations from clear_data.py, stat_analysis.py, and time_analysis.py
but adapted for financial analysis.
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, Optional, Dict, Any, List
import json
import logging


class FinanceFileOperations:
    """Handles file I/O operations for financial analysis."""
    
    def __init__(self):
        """Initialize the file operations handler."""
        self.supported_formats = ['parquet', 'json', 'csv']
        self.logger = logging.getLogger(__name__)
        
        # Supported data directories (including new data/fixed/)
        self.supported_dirs = [
            "data/cache/csv_converted/",
            "data/raw_parquet/",
            "data/indicators/parquet/",
            "data/indicators/json/",
            "data/indicators/csv/",
            "data/fixed/"  # New supported directory for cleaned data
        ]
    
    def get_supported_directories(self) -> List[str]:
        """Get list of supported directories."""
        return self.supported_dirs
    
    def load_data(self, file_path: str, format_type: str) -> Optional[pd.DataFrame]:
        """
        Load data from file in specified format.
        
        Args:
            file_path: Path to the data file
            format_type: Format of the file (parquet, json, csv)
            
        Returns:
            DataFrame with loaded data or None if error
        """
        if format_type not in self.supported_formats:
            raise ValueError(f"Unsupported format: {format_type}")
        
        try:
            if format_type == 'parquet':
                return pd.read_parquet(file_path)
            elif format_type == 'json':
                return pd.read_json(file_path)
            elif format_type == 'csv':
                return pd.read_csv(file_path)
        except Exception as e:
            self.logger.error(f"Error loading {format_type} file {file_path}: {str(e)}")
            return None
    
    def save_data(self, data: pd.DataFrame, file_path: str, format_type: str) -> bool:
        """
        Save data to file in specified format.
        
        Args:
            data: DataFrame to save
            file_path: Path where to save the file
            format_type: Format to save as (parquet, json, csv)
            
        Returns:
            True if successful, False otherwise
        """
        if format_type not in self.supported_formats:
            raise ValueError(f"Unsupported format: {format_type}")
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            if format_type == 'parquet':
                data.to_parquet(file_path, index=False)
            elif format_type == 'json':
                data.to_json(file_path, orient='records', indent=2)
            elif format_type == 'csv':
                data.to_csv(file_path, index=False)
            
            return True
        except Exception as e:
            self.logger.error(f"Error saving {format_type} file {file_path}: {str(e)}")
            return False
    
    def validate_file_path(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Validate if the file exists in supported directories.
        
        Args:
            filename: Name of the file to validate
            
        Returns:
            Dictionary with file metadata if valid, None otherwise
        """
        for directory in self.supported_dirs:
            file_path = os.path.join(directory, filename)
            if os.path.exists(file_path):
                return self._extract_file_metadata(file_path, directory)
        
        return None
    
    def _extract_file_metadata(self, file_path: str, directory: str) -> Dict[str, Any]:
        """
        Extract metadata from file path and content.
        
        Args:
            file_path: Full path to the file
            directory: Directory where file was found
            
        Returns:
            Dictionary with file metadata
        """
        try:
            # Get file stats
            file_stats = os.stat(file_path)
            file_size = file_stats.st_size
            
            # Determine format
            format_type = file_path.split('.')[-1].lower()
            
            # Extract symbol, timeframe, and indicator from filename
            filename = os.path.basename(file_path)
            symbol, timeframe, indicator = self._parse_filename(filename)
            
            # Determine source from directory
            source = self._determine_source(directory)
            
            # Load data to get dimensions
            data = self.load_data(file_path, format_type)
            if data is not None:
                rows_count = len(data)
                columns_count = len(data.columns)
                
                # Get date range if available
                start_date, end_date = self._get_date_range(data)
            else:
                rows_count = 0
                columns_count = 0
                start_date = None
                end_date = None
            
            return {
                "file_path": file_path,
                "file_size": file_size,
                "format": format_type,
                "symbol": symbol,
                "timeframe": timeframe,
                "source": source,
                "indicator": indicator,
                "folder_source": directory,
                "rows_count": rows_count,
                "columns_count": columns_count,
                "start_date": start_date,
                "end_date": end_date,
                "datetime_format": "Unknown"
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting metadata from {file_path}: {str(e)}")
            return None
    
    def _parse_filename(self, filename: str) -> tuple:
        """
        Parse filename to extract symbol, timeframe, and indicator.
        
        Args:
            filename: Name of the file
            
        Returns:
            Tuple of (symbol, timeframe, indicator)
        """
        # Remove file extension
        name = filename.split('.')[0]
        
        # Common symbols
        symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'EURUSD', 'GBPUSD', 'XAUUSD', 'US500', 'AAPL', 'GOOG', 'TSLA']
        symbol = "Unknown"
        for s in symbols:
            if s in name.upper():
                symbol = s
                break
        
        # Common timeframes
        timeframes = ['M1', 'M5', 'M15', 'H1', 'H4', 'D1', 'W1', 'MN1']
        timeframe = "Unknown"
        for t in timeframes:
            if t in name.upper():
                timeframe = t
                break
        
        # Common indicators
        indicators = ['Wave', 'RSI', 'MACD', 'BB', 'SMA', 'EMA', 'Stochastic', 'ADX', 'CCI', 'Williams', 'ATR', 'OBV']
        indicator = "Unknown"
        for i in indicators:
            if i in name:
                indicator = i
                break
        
        return symbol, timeframe, indicator
    
    def _determine_source(self, directory: str) -> str:
        """
        Determine data source from directory path.
        
        Args:
            directory: Directory path
            
        Returns:
            Source name
        """
        if 'binance' in directory.lower():
            return 'Binance'
        elif 'polygon' in directory.lower():
            return 'Polygon'
        elif 'yfinance' in directory.lower():
            return 'YFinance'
        elif 'csexport' in directory.lower():
            return 'CSVExport'
        elif 'fixed' in directory.lower():
            return 'Fixed'
        else:
            return 'Unknown'
    
    def _get_date_range(self, data: pd.DataFrame) -> tuple:
        """
        Get date range from DataFrame.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            Tuple of (start_date, end_date)
        """
        try:
            # Look for datetime columns
            datetime_cols = [col for col in data.columns if 'time' in col.lower() or 'date' in col.lower()]
            
            if datetime_cols:
                # Use the first datetime column
                datetime_col = datetime_cols[0]
                dates = pd.to_datetime(data[datetime_col])
                return str(dates.min()), str(dates.max())
            elif isinstance(data.index, pd.DatetimeIndex):
                # Use datetime index
                return str(data.index.min()), str(data.index.max())
            else:
                return None, None
        except:
            return None, None
    
    def get_files_in_directory(self, directory: str) -> List[str]:
        """
        Get all supported files in a directory.
        
        Args:
            directory: Directory path to scan
            
        Returns:
            List of filenames in the directory
        """
        if not os.path.exists(directory):
            return []
        
        files = []
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                # Check if file has supported format
                if any(file.lower().endswith(ext) for ext in ['.parquet', '.json', '.csv']):
                    files.append(file)
        
        return sorted(files)
    
    def validate_custom_path(self, custom_path: str) -> Optional[Dict[str, Any]]:
        """
        Validate custom file path for financial analysis.
        
        Args:
            custom_path: Custom file or directory path
            
        Returns:
            File metadata if valid, None otherwise
        """
        if not os.path.exists(custom_path):
            return None
        
        if os.path.isfile(custom_path):
            # Single file
            format_type = custom_path.split('.')[-1].lower()
            if format_type not in self.supported_formats:
                return None
            
            return self._extract_file_metadata(custom_path, os.path.dirname(custom_path))
        elif os.path.isdir(custom_path):
            # Directory - return basic info
            return {
                "is_directory": True,
                "path": custom_path,
                "files_count": len(self.get_files_in_directory(custom_path))
            }
        
        return None
