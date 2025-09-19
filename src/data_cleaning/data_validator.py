"""
Data Validator Module

This module handles file path validation and metadata extraction for data cleaning.
It validates that files are from supported directories and extracts comprehensive
metadata including file size, format, symbol, timeframe, source, and data statistics.
"""

import os
import re
from pathlib import Path
from typing import Optional, Dict, Any, List
import pandas as pd
import numpy as np
from datetime import datetime


class DataValidator:
    """Validates file paths and extracts metadata from data files."""
    
    def __init__(self):
        """Initialize the data validator."""
        self.supported_formats = ['parquet', 'json', 'csv']
        
        # Regex patterns for different file naming conventions
        self.patterns = {
            'csv_converted': r'^([A-Z]+)_PERIOD_([A-Z0-9]+)\.parquet$',
            'raw_parquet': r'^([a-z]+)_([A-Z]+)_([A-Z0-9]+)\.parquet$',
            'indicators': r'^([a-z]+)_([A-Z]+)_([A-Z0-9]+)_([a-z_]+)\.(parquet|json|csv)$'
        }
    
    def validate_file_path(self, filename: str, supported_dirs: List[str]) -> Optional[Dict[str, Any]]:
        """
        Validate if file exists in supported directories and extract metadata.
        
        Args:
            filename: Name of the file to validate
            supported_dirs: List of supported directory paths
            
        Returns:
            Dictionary with file metadata if valid, None otherwise
        """
        # Check if file exists in any supported directory
        file_path = None
        folder_source = None
        
        for directory in supported_dirs:
            full_path = os.path.join(directory, filename)
            if os.path.exists(full_path):
                file_path = full_path
                folder_source = directory.rstrip('/')
                break
        
        if file_path is None:
            return None
        
        # Extract metadata
        metadata = self._extract_metadata(file_path, filename, folder_source)
        return metadata
    
    def _extract_metadata(self, file_path: str, filename: str, folder_source: str) -> Dict[str, Any]:
        """
        Extract comprehensive metadata from the file.
        
        Args:
            file_path: Full path to the file
            filename: Name of the file
            folder_source: Source folder name
            
        Returns:
            Dictionary containing file metadata
        """
        metadata = {
            'file_path': file_path,
            'filename': filename,
            'folder_source': folder_source,
            'file_size': os.path.getsize(file_path),
            'format': self._get_file_format(filename),
            'symbol': None,
            'timeframe': None,
            'source': None,
            'indicator': None,
            'rows_count': 0,
            'columns_count': 0,
            'start_date': None,
            'end_date': None,
            'datetime_format': None
        }
        
        # Parse filename based on folder source
        if 'csv_converted' in folder_source:
            self._parse_csv_converted_filename(filename, metadata)
        elif 'raw_parquet' in folder_source:
            self._parse_raw_parquet_filename(filename, metadata)
        elif 'indicators' in folder_source:
            self._parse_indicators_filename(filename, metadata)
        
        # Load data to extract additional metadata
        try:
            data = self._load_data_sample(file_path, metadata['format'])
            if data is not None:
                self._extract_data_metadata(data, metadata)
        except Exception as e:
            print(f"Warning: Could not load data for metadata extraction: {e}")
        
        return metadata
    
    def _get_file_format(self, filename: str) -> str:
        """Extract file format from filename."""
        extension = filename.split('.')[-1].lower()
        return extension if extension in self.supported_formats else 'unknown'
    
    def _parse_csv_converted_filename(self, filename: str, metadata: Dict[str, Any]) -> None:
        """Parse CSV converted filename format: SYMBOL_PERIOD_TIMEFRAME.parquet"""
        match = re.match(self.patterns['csv_converted'], filename)
        if match:
            metadata['symbol'] = match.group(1)
            metadata['timeframe'] = match.group(2)
            metadata['source'] = 'csv_converted'
    
    def _parse_raw_parquet_filename(self, filename: str, metadata: Dict[str, Any]) -> None:
        """Parse raw parquet filename format: source_SYMBOL_TIMEFRAME.parquet"""
        match = re.match(self.patterns['raw_parquet'], filename)
        if match:
            metadata['source'] = match.group(1)
            metadata['symbol'] = match.group(2)
            metadata['timeframe'] = match.group(3)
        else:
            # Fallback parsing for different formats
            parts = filename.replace('.parquet', '').split('_')
            if len(parts) >= 3:
                metadata['source'] = parts[0]
                metadata['symbol'] = parts[1]
                metadata['timeframe'] = parts[2]
    
    def _parse_indicators_filename(self, filename: str, metadata: Dict[str, Any]) -> None:
        """Parse indicators filename format: source_SYMBOL_TIMEFRAME_indicator.format"""
        match = re.match(self.patterns['indicators'], filename)
        if match:
            metadata['source'] = match.group(1)
            metadata['symbol'] = match.group(2)
            metadata['timeframe'] = match.group(3)
            metadata['indicator'] = match.group(4)
        else:
            # Fallback parsing for different formats
            parts = filename.split('.')
            if len(parts) >= 2:
                name_parts = parts[0].split('_')
                if len(name_parts) >= 4:
                    metadata['source'] = name_parts[0]
                    metadata['symbol'] = name_parts[1]
                    metadata['timeframe'] = name_parts[2]
                    metadata['indicator'] = name_parts[3]
    
    def _load_data_sample(self, file_path: str, format_type: str) -> Optional[pd.DataFrame]:
        """
        Load a sample of data to extract metadata.
        
        Args:
            file_path: Path to the data file
            format_type: Format of the file (parquet, json, csv)
            
        Returns:
            DataFrame with data sample or None if error
        """
        try:
            if format_type == 'parquet':
                return pd.read_parquet(file_path)
            elif format_type == 'json':
                return pd.read_json(file_path)
            elif format_type == 'csv':
                return pd.read_csv(file_path)
            else:
                return None
        except Exception:
            return None
    
    def _extract_data_metadata(self, data: pd.DataFrame, metadata: Dict[str, Any]) -> None:
        """
        Extract metadata from the loaded data.
        
        Args:
            data: Loaded DataFrame
            metadata: Metadata dictionary to update
        """
        metadata['rows_count'] = len(data)
        metadata['columns_count'] = len(data.columns)
        
        # Find datetime columns
        datetime_cols = self._find_datetime_columns(data)
        
        if datetime_cols:
            # Use the first datetime column for date range
            datetime_col = datetime_cols[0]
            metadata['datetime_format'] = str(data[datetime_col].dtype)
            
            # Get date range
            try:
                dates = pd.to_datetime(data[datetime_col], errors='coerce')
                valid_dates = dates.dropna()
                
                if len(valid_dates) > 0:
                    metadata['start_date'] = valid_dates.min().strftime('%Y-%m-%d %H:%M:%S')
                    metadata['end_date'] = valid_dates.max().strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                pass
    
    def _find_datetime_columns(self, data: pd.DataFrame) -> List[str]:
        """
        Find columns that contain datetime data.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            List of column names that contain datetime data
        """
        datetime_cols = []
        
        for col in data.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['time', 'date', 'timestamp', 'datetime']):
                datetime_cols.append(col)
            elif data[col].dtype in ['datetime64[ns]', 'datetime64[ns, UTC]']:
                datetime_cols.append(col)
            else:
                # Try to detect if column contains datetime strings
                try:
                    sample = data[col].dropna().head(5)
                    if len(sample) > 0:
                        # Only try if the column looks like it might contain datetime strings
                        if isinstance(sample.iloc[0], str) and any(char in str(sample.iloc[0]) for char in ['-', ':', ' ']):
                            pd.to_datetime(sample.iloc[0])
                            datetime_cols.append(col)
                except Exception:
                    pass
        
        return datetime_cols
    
    def get_supported_directories(self) -> List[str]:
        """
        Get list of supported data directories.
        
        Returns:
            List of supported directory paths
        """
        return [
            "data/cache/csv_converted/",
            "data/raw_parquet/",
            "data/indicators/parquet/",
            "data/indicators/json/",
            "data/indicators/csv/"
        ]
    
    def validate_directory_structure(self, base_path: str = ".") -> Dict[str, bool]:
        """
        Validate that all required directories exist.
        
        Args:
            base_path: Base path to check directories from
            
        Returns:
            Dictionary mapping directory names to existence status
        """
        directories = self.get_supported_directories()
        results = {}
        
        for directory in directories:
            full_path = os.path.join(base_path, directory)
            results[directory] = os.path.exists(full_path)
        
        return results
