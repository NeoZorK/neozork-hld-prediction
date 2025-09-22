"""
Statistics File Operations Module

This module handles reading and writing data in different formats (parquet, JSON, CSV)
for statistical analysis. It provides a unified interface for data I/O operations
with proper error handling and format-specific optimizations.

Based on the file operations from clear_data.py but adapted for statistical analysis.
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, Optional, Dict, Any, List
import json
import logging


class StatisticsFileOperations:
    """Handles file I/O operations for statistical analysis."""
    
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
            "data/fixed/"  # New supported directory
        ]
    
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
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            if format_type == 'parquet':
                return self._load_parquet(file_path)
            elif format_type == 'json':
                return self._load_json(file_path)
            elif format_type == 'csv':
                return self._load_csv(file_path)
        except Exception as e:
            self.logger.error(f"Error loading {format_type} file {file_path}: {e}")
            raise
    
    def save_data(self, data: pd.DataFrame, file_path: str, format_type: str) -> None:
        """
        Save data to file in specified format.
        
        Args:
            data: DataFrame to save
            file_path: Path where to save the file
            format_type: Format to save in (parquet, json, csv)
        """
        if format_type not in self.supported_formats:
            raise ValueError(f"Unsupported format: {format_type}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        try:
            if format_type == 'parquet':
                self._save_parquet(data, file_path)
            elif format_type == 'json':
                self._save_json(data, file_path)
            elif format_type == 'csv':
                self._save_csv(data, file_path)
        except Exception as e:
            self.logger.error(f"Error saving {format_type} file {file_path}: {e}")
            raise
    
    def _load_parquet(self, file_path: str) -> pd.DataFrame:
        """Load parquet file."""
        return pd.read_parquet(file_path)
    
    def _load_json(self, file_path: str) -> pd.DataFrame:
        """Load JSON file."""
        # Try different JSON orientations
        try:
            return pd.read_json(file_path)
        except ValueError:
            # Try with different orientations
            try:
                return pd.read_json(file_path, orient='records')
            except ValueError:
                return pd.read_json(file_path, orient='index')
    
    def _load_csv(self, file_path: str) -> pd.DataFrame:
        """Load CSV file with automatic delimiter detection."""
        # Try to detect delimiter
        with open(file_path, 'r', encoding='utf-8') as f:
            sample = f.read(1024)
        
        delimiter = ','
        if ';' in sample and sample.count(';') > sample.count(','):
            delimiter = ';'
        elif '\t' in sample and sample.count('\t') > sample.count(','):
            delimiter = '\t'
        
        return pd.read_csv(file_path, delimiter=delimiter, encoding='utf-8')
    
    def _save_parquet(self, data: pd.DataFrame, file_path: str) -> None:
        """Save data as parquet file."""
        data.to_parquet(file_path, index=False, engine='pyarrow')
    
    def _save_json(self, data: pd.DataFrame, file_path: str) -> None:
        """Save data as JSON file."""
        data.to_json(file_path, orient='records', indent=2, date_format='iso')
    
    def _save_csv(self, data: pd.DataFrame, file_path: str) -> None:
        """Save data as CSV file."""
        data.to_csv(file_path, index=False, encoding='utf-8')
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get basic file information.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        if not os.path.exists(file_path):
            return {'exists': False}
        
        stat = os.stat(file_path)
        return {
            'exists': True,
            'size': stat.st_size,
            'modified': stat.st_mtime,
            'created': stat.st_ctime
        }
    
    def validate_file_path(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Validate if file exists in supported directories and extract metadata.
        
        Args:
            filename: Name of the file to validate
            
        Returns:
            Dictionary with file metadata if valid, None otherwise
        """
        # Check if file exists in any supported directory
        file_path = None
        folder_source = None
        
        for directory in self.supported_dirs:
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
        elif 'fixed' in folder_source:
            self._parse_fixed_filename(filename, metadata)
        
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
        """Parse CSV converted filename format: CSVExport_SYMBOL_PERIOD_TIMEFRAME.parquet"""
        import re
        pattern = r'^CSVExport_([A-Z0-9.]+)_PERIOD_([A-Za-z0-9]+)\.parquet$'
        match = re.match(pattern, filename)
        if match:
            metadata['symbol'] = match.group(1)
            metadata['timeframe'] = match.group(2)
            metadata['source'] = 'CSVExport'
    
    def _parse_raw_parquet_filename(self, filename: str, metadata: Dict[str, Any]) -> None:
        """Parse raw parquet filename format: source_SYMBOL_TIMEFRAME.parquet"""
        import re
        pattern = r'^([a-z]+)_([A-Z0-9.]+)_([A-Za-z0-9]+)\.parquet$'
        match = re.match(pattern, filename)
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
        import re
        # Special handling for CSVExport files in indicators folder
        if filename.startswith('CSVExport_'):
            csv_match = re.match(r'^CSVExport_([A-Z0-9.]+)_PERIOD_([A-Za-z0-9]+)_([a-zA-Z_]+)\.(parquet|json|csv)$', filename)
            if csv_match:
                metadata['source'] = 'CSVExport'
                metadata['symbol'] = csv_match.group(1)
                metadata['timeframe'] = csv_match.group(2)
                metadata['indicator'] = csv_match.group(3)
                return
        
        # Regular indicators parsing
        pattern = r'^([a-z]+)_([A-Z0-9.]+)_([A-Za-z0-9]+)_([a-z_]+)\.(parquet|json|csv)$'
        match = re.match(pattern, filename)
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
    
    def _parse_fixed_filename(self, filename: str, metadata: Dict[str, Any]) -> None:
        """Parse fixed filename format: SYMBOL_TIMEFRAME_INDICATOR_cleaned.format"""
        import re
        # Try to parse cleaned data filename
        pattern = r'^([A-Z0-9.]+)_([A-Za-z0-9]+)_([a-zA-Z_]+)_cleaned\.(parquet|json|csv)$'
        match = re.match(pattern, filename)
        if match:
            metadata['symbol'] = match.group(1)
            metadata['timeframe'] = match.group(2)
            metadata['indicator'] = match.group(3)
            metadata['source'] = 'Fixed'
        else:
            # Fallback parsing
            parts = filename.split('.')
            if len(parts) >= 2:
                name_parts = parts[0].split('_')
                if len(name_parts) >= 3:
                    metadata['symbol'] = name_parts[0]
                    metadata['timeframe'] = name_parts[1]
                    metadata['indicator'] = name_parts[2] if len(name_parts) > 2 else 'Unknown'
                    metadata['source'] = 'Fixed'
    
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
        
        # Check if index is datetime first
        if isinstance(data.index, pd.DatetimeIndex):
            try:
                valid_dates = data.index.dropna()
                if len(valid_dates) > 0:
                    metadata['start_date'] = valid_dates.min().strftime('%Y-%m-%d %H:%M:%S')
                    metadata['end_date'] = valid_dates.max().strftime('%Y-%m-%d %H:%M:%S')
                    metadata['datetime_format'] = str(data.index.dtype)
            except Exception:
                pass
        else:
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
    
    def get_supported_directories(self) -> List[str]:
        """
        Get list of supported data directories.
        
        Returns:
            List of supported directory paths
        """
        return self.supported_dirs.copy()
