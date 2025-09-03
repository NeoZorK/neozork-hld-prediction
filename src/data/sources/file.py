"""
File Data Source Implementation

This module provides file-based data source functionality.
"""

import pandas as pd
from typing import Dict, Any, Optional
from pathlib import Path

from .base import BaseDataSource
from ...core.exceptions import DataError, ValidationError


class ParquetDataSource(BaseDataSource):
    """Parquet file data source implementation."""
    
    def __init__(self, file_path: str, config: Dict[str, Any]):
        """
        Initialize Parquet data source.
        
        Args:
            file_path: Path to Parquet file
            config: Configuration dictionary
        """
        super().__init__(f"parquet_{Path(file_path).stem}", config)
        self.file_path = Path(file_path)
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """Fetch data from Parquet file."""
        try:
            if not self.is_available():
                raise DataError(f"Parquet file not found: {self.file_path}")
            
            data = pd.read_parquet(self.file_path, **kwargs)
            
            if data.empty:
                raise DataError("Parquet file is empty")
            
            return data
            
        except Exception as e:
            raise DataError(f"Failed to read Parquet file: {e}")
    
    def is_available(self) -> bool:
        """Check if Parquet file is available."""
        try:
            return self.file_path.exists() and self.file_path.is_file()
        except Exception:
            return False
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get Parquet file metadata."""
        return {
            "type": "parquet",
            "file_path": str(self.file_path),
            "exists": self.is_available()
        }


class JSONDataSource(BaseDataSource):
    """JSON file data source implementation."""
    
    def __init__(self, file_path: str, config: Dict[str, Any]):
        """
        Initialize JSON data source.
        
        Args:
            file_path: Path to JSON file
            config: Configuration dictionary
        """
        super().__init__(f"json_{Path(file_path).stem}", config)
        self.file_path = Path(file_path)
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """Fetch data from JSON file."""
        try:
            if not self.is_available():
                raise DataError(f"JSON file not found: {self.file_path}")
            
            data = pd.read_json(self.file_path, **kwargs)
            
            if data.empty:
                raise DataError("JSON file is empty")
            
            return data
            
        except Exception as e:
            raise DataError(f"Failed to read JSON file: {e}")
    
    def is_available(self) -> bool:
        """Check if JSON file is available."""
        try:
            return self.file_path.exists() and self.file_path.is_file()
        except Exception:
            return False
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get JSON file metadata."""
        return {
            "type": "json",
            "file_path": str(self.file_path),
            "exists": self.is_available()
        }


__all__ = ["ParquetDataSource", "JSONDataSource"]
