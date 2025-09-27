# -*- coding: utf-8 -*-
"""
Universal data loader for AutoGluon integration.

This module provides universal data loading capabilities supporting
parquet, CSV, JSON, and other formats from the data/ folder.
"""

import pandas as pd
import os
import json
from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Tuple
import logging
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class UniversalDataLoader:
    """Universal data loader supporting multiple formats."""
    
    def __init__(self, data_path: str = "data/", recursive: bool = True):
        """
        Initialize universal data loader.
        
        Args:
            data_path: Path to data directory
            recursive: Whether to search recursively
        """
        self.data_path = Path(data_path)
        self.recursive = recursive
        self.supported_formats = ['.parquet', '.csv', '.json', '.xlsx', '.h5', '.hdf5']
        
    def discover_data_files(self) -> List[Path]:
        """
        Discover all supported data files in the data directory.
        
        Returns:
            List of discovered file paths
        """
        discovered_files = []
        
        if not self.data_path.exists():
            logger.warning(f"Data path {self.data_path} does not exist")
            return discovered_files
        
        pattern = "**/*" if self.recursive else "*"
        
        for file_path in self.data_path.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                discovered_files.append(file_path)
        
        logger.info(f"Discovered {len(discovered_files)} data files")
        return discovered_files
    
    def load_parquet(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Load parquet file with optimization.
        
        Args:
            file_path: Path to parquet file
            
        Returns:
            Loaded DataFrame
        """
        try:
            df = pd.read_parquet(file_path)
            logger.info(f"Loaded parquet file: {file_path} ({len(df)} rows, {len(df.columns)} columns)")
            return df
        except Exception as e:
            logger.error(f"Error loading parquet file {file_path}: {e}")
            return pd.DataFrame()
    
    def load_csv(self, file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
        """
        Load CSV file with auto-detection of separators and encodings.
        
        Args:
            file_path: Path to CSV file
            **kwargs: Additional arguments for pd.read_csv
            
        Returns:
            Loaded DataFrame
        """
        try:
            # Try different separators
            separators = [',', ';', '\t', '|']
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for sep in separators:
                for encoding in encodings:
                    try:
                        df = pd.read_csv(file_path, sep=sep, encoding=encoding, **kwargs)
                        if len(df.columns) > 1:  # Valid CSV
                            logger.info(f"Loaded CSV file: {file_path} ({len(df)} rows, {len(df.columns)} columns)")
                            return df
                    except:
                        continue
            
            # Fallback to default
            df = pd.read_csv(file_path, **kwargs)
            logger.info(f"Loaded CSV file: {file_path} ({len(df)} rows, {len(df.columns)} columns)")
            return df
            
        except Exception as e:
            logger.error(f"Error loading CSV file {file_path}: {e}")
            return pd.DataFrame()
    
    def load_json(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Load JSON file (flat or nested).
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Loaded DataFrame
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                df = pd.json_normalize(data)
            elif isinstance(data, dict):
                df = pd.json_normalize([data])
            else:
                logger.error(f"Unsupported JSON format in {file_path}")
                return pd.DataFrame()
            
            logger.info(f"Loaded JSON file: {file_path} ({len(df)} rows, {len(df.columns)} columns)")
            return df
            
        except Exception as e:
            logger.error(f"Error loading JSON file {file_path}: {e}")
            return pd.DataFrame()
    
    def load_excel(self, file_path: Union[str, Path], sheet_name: Optional[str] = None) -> pd.DataFrame:
        """
        Load Excel file.
        
        Args:
            file_path: Path to Excel file
            sheet_name: Sheet name to load (None for first sheet)
            
        Returns:
            Loaded DataFrame
        """
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            logger.info(f"Loaded Excel file: {file_path} ({len(df)} rows, {len(df.columns)} columns)")
            return df
        except Exception as e:
            logger.error(f"Error loading Excel file {file_path}: {e}")
            return pd.DataFrame()
    
    def load_hdf5(self, file_path: Union[str, Path], key: str = 'data') -> pd.DataFrame:
        """
        Load HDF5 file.
        
        Args:
            file_path: Path to HDF5 file
            key: HDF5 key to load
            
        Returns:
            Loaded DataFrame
        """
        try:
            df = pd.read_hdf(file_path, key=key)
            logger.info(f"Loaded HDF5 file: {file_path} ({len(df)} rows, {len(df.columns)} columns)")
            return df
        except Exception as e:
            logger.error(f"Error loading HDF5 file {file_path}: {e}")
            return pd.DataFrame()
    
    def load_file(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Load file based on its extension.
        
        Args:
            file_path: Path to file
            
        Returns:
            Loaded DataFrame
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension == '.parquet':
            return self.load_parquet(file_path)
        elif extension == '.csv':
            return self.load_csv(file_path)
        elif extension == '.json':
            return self.load_json(file_path)
        elif extension in ['.xlsx', '.xls']:
            return self.load_excel(file_path)
        elif extension in ['.h5', '.hdf5']:
            return self.load_hdf5(file_path)
        else:
            logger.error(f"Unsupported file format: {extension}")
            return pd.DataFrame()
    
    def load_multiple_files(self, file_paths: List[Union[str, Path]], 
                           merge_strategy: str = 'concat') -> pd.DataFrame:
        """
        Load multiple files and merge them.
        
        Args:
            file_paths: List of file paths
            merge_strategy: 'concat' or 'merge'
            
        Returns:
            Merged DataFrame
        """
        dataframes = []
        
        for file_path in file_paths:
            df = self.load_file(file_path)
            if not df.empty:
                dataframes.append(df)
        
        if not dataframes:
            logger.warning("No valid data files found")
            return pd.DataFrame()
        
        if merge_strategy == 'concat':
            # Simple concatenation
            result_df = pd.concat(dataframes, ignore_index=True)
            logger.info(f"Concatenated {len(dataframes)} files into {len(result_df)} rows")
        elif merge_strategy == 'merge':
            # Merge on common columns
            result_df = dataframes[0]
            for df in dataframes[1:]:
                common_cols = set(result_df.columns) & set(df.columns)
                if common_cols:
                    result_df = result_df.merge(df, on=list(common_cols), how='outer')
            logger.info(f"Merged {len(dataframes)} files into {len(result_df)} rows")
        else:
            logger.error(f"Unknown merge strategy: {merge_strategy}")
            return pd.DataFrame()
        
        return result_df
    
    def get_file_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get information about a data file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary with file information
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {'error': 'File does not exist'}
        
        info = {
            'file_path': str(file_path),
            'file_size': file_path.stat().st_size,
            'extension': file_path.suffix,
            'modified_time': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        }
        
        # Try to get basic DataFrame info
        try:
            df = self.load_file(file_path)
            if not df.empty:
                info.update({
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': df.columns.tolist(),
                    'dtypes': df.dtypes.to_dict(),
                    'memory_usage': df.memory_usage(deep=True).sum()
                })
        except Exception as e:
            info['error'] = str(e)
        
        return info
    
    def validate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate DataFrame for AutoGluon compatibility.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Validation results
        """
        validation_results = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'suggestions': []
        }
        
        if df.empty:
            validation_results['is_valid'] = False
            validation_results['errors'].append("DataFrame is empty")
            return validation_results
        
        # Check for completely empty columns
        empty_cols = df.columns[df.isnull().all()].tolist()
        if empty_cols:
            validation_results['warnings'].append(f"Empty columns found: {empty_cols}")
        
        # Check for duplicate columns
        duplicate_cols = df.columns[df.columns.duplicated()].tolist()
        if duplicate_cols:
            validation_results['warnings'].append(f"Duplicate columns found: {duplicate_cols}")
        
        # Check for high missing value ratio
        missing_ratio = df.isnull().sum() / len(df)
        high_missing_cols = missing_ratio[missing_ratio > 0.5].index.tolist()
        if high_missing_cols:
            validation_results['warnings'].append(f"Columns with >50% missing values: {high_missing_cols}")
        
        # Check for constant columns
        constant_cols = df.columns[df.nunique() <= 1].tolist()
        if constant_cols:
            validation_results['warnings'].append(f"Constant columns found: {constant_cols}")
        
        # Check for datetime index
        if not isinstance(df.index, pd.DatetimeIndex):
            validation_results['suggestions'].append("Consider setting datetime index for time series data")
        
        return validation_results
