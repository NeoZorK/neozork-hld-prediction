# -*- coding: utf-8 -*-
# src/data/acquisition/utils.py

"""
Utility functions for data acquisition process.
Includes interval parsing, filename generation, and CSV processing helpers.
All comments are in English.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any
from ...common.logger import print_info, print_warning, print_error, print_success


class DataAcquisitionUtils:
    """Utility functions for data acquisition."""
    
    def __init__(self):
        """Initialize the utilities module."""
        self.data_directory = Path('data')
        self.raw_parquet_dir = Path('data/raw_parquet')
    
    def get_interval_delta(self, interval_str: str) -> Optional[pd.Timedelta]:
        """
        Converts common interval strings to pandas Timedelta.
        
        Args:
            interval_str: Interval string (e.g., 'h1', 'D1', 'M1', 'W')
            
        Returns:
            Pandas Timedelta or None if unparseable
        """
        try:
            delta = pd.Timedelta(interval_str)
            if delta.total_seconds() > 0:
                return delta
        except ValueError:
            pass

        simple_map = {
            'M1': '1min', 'M5': '5min', 'M15': '15min', 'M30': '30min',
            'H1': '1h', 'h1': '1h', 'H4': '4h',
            'D1': '1d', 'D': '1d', 'W': '7d', 'W1': '7d', 'WK': '7d',
            'MN': '30d', 'MN1': '30d', 'MO': '30d'
        }
        
        pd_freq = simple_map.get(str(interval_str).upper())
        if pd_freq:
            try:
                delta = pd.Timedelta(pd_freq)
                if delta.total_seconds() > 0:
                    return delta
            except ValueError:
                pass

        print_warning(f"Could not parse interval '{interval_str}' to Timedelta. Cache delta logic may be affected.")
        return None
    
    def generate_instrument_filename(self, mode: str, ticker: str, interval: str, 
                                   file_format: str = 'parquet') -> Optional[Path]:
        """
        Generate filename for instrument data.
        
        Args:
            mode: Data source mode
            ticker: Instrument ticker
            interval: Time interval
            file_format: File format extension
            
        Returns:
            Path to the generated filename
        """
        effective_mode = 'yfinance' if mode == 'yf' else mode
        
        if effective_mode not in ['yfinance', 'polygon', 'binance', 'exrate'] or not ticker:
            return None
        
        try:
            ticker_label = str(ticker).replace('/', '_').replace('-', '_').replace('=', '_').replace(':', '_')
            interval_label = str(interval)
            filename = f"{effective_mode}_{ticker_label}_{interval_label}.{file_format}"
            filepath = self.raw_parquet_dir / filename
            return filepath
        except Exception as e:
            print_warning(f"Error generating instrument filename: {e}")
            return None
    
    def get_available_instruments(self) -> List[str]:
        """Get list of available instruments from data directory."""
        instruments = []
        
        if self.data_directory.exists():
            # Scan for instrument files
            for file_path in self.data_directory.rglob('*'):
                if file_path.is_file() and file_path.suffix in ['.csv', '.parquet', '.json']:
                    # Extract instrument name from filename
                    instrument = self._extract_instrument_from_filename(file_path.name)
                    if instrument and instrument not in instruments:
                        instruments.append(instrument)
        
        return sorted(instruments)
    
    def get_data_info(self, instrument: str) -> Dict[str, Any]:
        """Get information about available data for an instrument."""
        info = {
            'instrument': instrument,
            'available_files': [],
            'total_size_mb': 0,
            'date_range': None,
            'formats': set()
        }
        
        if self.data_directory.exists():
            # Find files for this instrument
            for file_path in self.data_directory.rglob(f'*{instrument}*'):
                if file_path.is_file():
                    file_info = self._get_file_info(file_path)
                    info['available_files'].append(file_info)
                    info['total_size_mb'] += file_info['size_mb']
                    info['formats'].add(file_path.suffix)
        
        # Calculate overall date range
        if info['available_files']:
            info['date_range'] = self._calculate_overall_date_range(info['available_files'])
        
        return info
    
    def _extract_instrument_from_filename(self, filename: str) -> Optional[str]:
        """Extract instrument name from filename."""
        # Remove file extension
        name = Path(filename).stem
        
        # Common patterns for instrument names
        if '_' in name:
            parts = name.split('_')
            if len(parts) >= 2:
                return parts[1]  # Usually the second part is the instrument
        
        return None
    
    def _get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Get information about a single file."""
        try:
            stat = file_path.stat()
            size_mb = stat.st_size / (1024 * 1024)
            
            return {
                'name': file_path.name,
                'path': str(file_path),
                'size_mb': size_mb,
                'modified': stat.st_mtime,
                'format': file_path.suffix
            }
        except Exception as e:
            return {
                'name': file_path.name,
                'path': str(file_path),
                'size_mb': 0,
                'modified': 0,
                'format': file_path.suffix,
                'error': str(e)
            }
    
    def _calculate_overall_date_range(self, files_info: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall date range from multiple files."""
        # This is a placeholder - in practice you would parse actual data
        # to determine the real date range
        
        return {
            'start_date': '2020-01-01',
            'end_date': '2024-12-31',
            'total_days': 1825
        }
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate the quality of acquired data.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dictionary with validation results
        """
        if df is None or df.empty:
            return {
                'is_valid': False,
                'errors': ['DataFrame is empty or None'],
                'warnings': [],
                'quality_score': 0
            }
        
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'quality_score': 100
        }
        
        # Check for missing values
        missing_counts = df.isnull().sum()
        total_missing = missing_counts.sum()
        total_cells = len(df) * len(df.columns)
        
        if total_missing > 0:
            missing_percentage = (total_missing / total_cells) * 100
            validation_results['quality_score'] -= missing_percentage * 10
            
            if missing_percentage > 20:
                validation_results['errors'].append(f"High missing data: {missing_percentage:.1f}%")
                validation_results['is_valid'] = False
            elif missing_percentage > 5:
                validation_results['warnings'].append(f"Missing data: {missing_percentage:.1f}%")
        
        # Check for duplicate rows
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            duplicate_percentage = (duplicate_count / len(df)) * 100
            validation_results['quality_score'] -= duplicate_percentage * 5
            
            if duplicate_percentage > 10:
                validation_results['errors'].append(f"High duplicate data: {duplicate_percentage:.1f}%")
                validation_results['is_valid'] = False
            else:
                validation_results['warnings'].append(f"Duplicate data: {duplicate_percentage:.1f}%")
        
        # Check data types
        numeric_columns = df.select_dtypes(include=['number']).columns
        if len(numeric_columns) == 0:
            validation_results['warnings'].append("No numeric columns found")
        
        # Ensure quality score is not negative
        validation_results['quality_score'] = max(0, validation_results['quality_score'])
        
        return validation_results
