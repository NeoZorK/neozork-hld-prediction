"""
CSV Data Source Implementation

This module provides CSV file data source functionality for the Neozork HLD Prediction system.
"""

import pandas as pd
from typing import Dict, Any, Optional
from pathlib import Path

from .base import BaseDataSource
from ...core.exceptions import DataError, ValidationError


class CSVDataSource(BaseDataSource):
    """
    CSV file data source implementation.
    
    Provides functionality to read and validate CSV files containing
    financial or time-series data.
    """
    
    def __init__(self, file_path: str, config: Dict[str, Any]):
        """
        Initialize CSV data source.
        
        Args:
            file_path: Path to the CSV file
            config: Configuration dictionary
            
        Raises:
            ValidationError: If file path is invalid
        """
        super().__init__(f"csv_source_{Path(file_path).stem}", config)
        self.file_path = Path(file_path)
        self._validate_file_path()
    
    def _validate_file_path(self) -> None:
        """Validate the CSV file path."""
        if not str(self.file_path).endswith('.csv'):
            raise ValidationError("File must have .csv extension")
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        Fetch data from CSV file.
        
        Args:
            **kwargs: Additional arguments passed to pd.read_csv
            
        Returns:
            DataFrame containing the CSV data
            
        Raises:
            DataError: If file cannot be read or data is invalid
        """
        try:
            if not self.is_available():
                raise DataError(f"CSV file not found: {self.file_path}")
            
            # Default CSV reading parameters
            default_params = {
                'index_col': 0,
                'parse_dates': True,
                'infer_datetime_format': True
            }
            
            # Merge with user parameters
            params = {**default_params, **kwargs}
            
            data = pd.read_csv(self.file_path, **params)
            
            if data.empty:
                raise DataError("CSV file is empty")
            
            self.logger.info(f"Successfully loaded {len(data)} rows from {self.file_path}")
            return data
            
        except FileNotFoundError:
            raise DataError(f"CSV file not found: {self.file_path}")
        except pd.errors.EmptyDataError:
            raise DataError("CSV file is empty")
        except pd.errors.ParserError as e:
            raise DataError(f"Failed to parse CSV file: {e}")
        except Exception as e:
            raise DataError(f"Unexpected error reading CSV file: {e}")
    
    def is_available(self) -> bool:
        """
        Check if CSV file is available.
        
        Returns:
            True if file exists and is readable, False otherwise
        """
        try:
            return self.file_path.exists() and self.file_path.is_file()
        except Exception:
            return False
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get CSV file metadata.
        
        Returns:
            Dictionary containing file metadata
        """
        metadata = {
            "type": "csv",
            "file_path": str(self.file_path),
            "exists": self.is_available()
        }
        
        if self.is_available():
            try:
                stat = self.file_path.stat()
                metadata.update({
                    "size_bytes": stat.st_size,
                    "modified_time": stat.st_mtime,
                    "readable": True
                })
                
                # Try to get basic info about CSV structure
                with open(self.file_path, 'r') as f:
                    first_line = f.readline().strip()
                    if first_line:
                        metadata["columns"] = len(first_line.split(','))
                        metadata["has_header"] = not first_line[0].isdigit()
                        
            except Exception as e:
                self.logger.warning(f"Could not get file metadata: {e}")
                metadata["error"] = str(e)
        
        return metadata


__all__ = ["CSVDataSource"]
