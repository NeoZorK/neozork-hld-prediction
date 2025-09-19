"""
File Operations Module

This module handles reading and writing data in different formats (parquet, JSON, CSV).
It provides a unified interface for data I/O operations with proper error handling
and format-specific optimizations.
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, Optional, Dict, Any
import json
import logging


class FileOperations:
    """Handles file I/O operations for different data formats."""
    
    def __init__(self):
        """Initialize the file operations handler."""
        self.supported_formats = ['parquet', 'json', 'csv']
        self.logger = logging.getLogger(__name__)
    
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
    
    def backup_file(self, file_path: str, backup_suffix: str = '.backup') -> str:
        """
        Create a backup of the file.
        
        Args:
            file_path: Path to the file to backup
            backup_suffix: Suffix to add to backup filename
            
        Returns:
            Path to the backup file
        """
        backup_path = file_path + backup_suffix
        backup_path = self._get_unique_filename(backup_path)
        
        import shutil
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def _get_unique_filename(self, file_path: str) -> str:
        """
        Get a unique filename if the original exists.
        
        Args:
            file_path: Original file path
            
        Returns:
            Unique file path
        """
        if not os.path.exists(file_path):
            return file_path
        
        base, ext = os.path.splitext(file_path)
        counter = 1
        
        while True:
            new_path = f"{base}_{counter}{ext}"
            if not os.path.exists(new_path):
                return new_path
            counter += 1
    
    def validate_data_integrity(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate data integrity and return statistics.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            Dictionary with validation results
        """
        results = {
            'total_rows': len(data),
            'total_columns': len(data.columns),
            'memory_usage': data.memory_usage(deep=True).sum(),
            'dtypes': data.dtypes.to_dict(),
            'null_counts': data.isnull().sum().to_dict(),
            'duplicate_rows': data.duplicated().sum(),
            'numeric_columns': data.select_dtypes(include=[np.number]).columns.tolist(),
            'datetime_columns': data.select_dtypes(include=['datetime64']).columns.tolist(),
            'object_columns': data.select_dtypes(include=['object']).columns.tolist()
        }
        
        # Check for infinite values in numeric columns
        numeric_data = data.select_dtypes(include=[np.number])
        results['infinite_values'] = np.isinf(numeric_data).sum().sum()
        
        # Check for negative values in numeric columns
        results['negative_values'] = (numeric_data < 0).sum().sum()
        
        # Check for zero values in numeric columns
        results['zero_values'] = (numeric_data == 0).sum().sum()
        
        return results
    
    def optimize_dataframe(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize DataFrame memory usage.
        
        Args:
            data: DataFrame to optimize
            
        Returns:
            Optimized DataFrame
        """
        optimized_data = data.copy()
        
        # Optimize numeric columns
        for col in optimized_data.select_dtypes(include=[np.number]).columns:
            col_data = optimized_data[col]
            
            # Check if column can be downcast to smaller integer type
            if col_data.dtype in ['int64', 'int32']:
                if col_data.min() >= 0:
                    if col_data.max() < 255:
                        optimized_data[col] = col_data.astype('uint8')
                    elif col_data.max() < 65535:
                        optimized_data[col] = col_data.astype('uint16')
                    elif col_data.max() < 4294967295:
                        optimized_data[col] = col_data.astype('uint32')
                else:
                    if col_data.min() >= -128 and col_data.max() <= 127:
                        optimized_data[col] = col_data.astype('int8')
                    elif col_data.min() >= -32768 and col_data.max() <= 32767:
                        optimized_data[col] = col_data.astype('int16')
                    elif col_data.min() >= -2147483648 and col_data.max() <= 2147483647:
                        optimized_data[col] = col_data.astype('int32')
            
            # Check if column can be downcast to smaller float type
            elif col_data.dtype == 'float64':
                if col_data.min() >= np.finfo(np.float32).min and col_data.max() <= np.finfo(np.float32).max:
                    optimized_data[col] = col_data.astype('float32')
        
        # Optimize object columns
        for col in optimized_data.select_dtypes(include=['object']).columns:
            col_data = optimized_data[col]
            
            # Try to convert to category if it has few unique values
            if col_data.nunique() / len(col_data) < 0.5:
                optimized_data[col] = col_data.astype('category')
        
        return optimized_data
