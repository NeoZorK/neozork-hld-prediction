# -*- coding: utf-8 -*-
"""
Indicators Data Processor for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive processing and standardization functionality
for indicators data from multiple formats with data quality validation.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import time
from datetime import datetime
import colorama
from colorama import Fore, Style

from src.common.logger import print_error, print_info, print_success, print_warning


class IndicatorsProcessor:
    """
    Processor for indicators data from multiple formats.
    
    Provides comprehensive processing, standardization, and validation
    functionality for indicators data with quality checks.
    """
    
    def __init__(self):
        """Initialize the indicators processor."""
        self.standard_columns = ['timestamp', 'symbol', 'timeframe', 'indicator']
        self.numeric_columns = []  # Will be determined dynamically
        self.required_columns = []  # Will be determined dynamically
        
    def process_indicators_data(self, loaded_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process loaded indicators data with standardization and validation.
        
        Args:
            loaded_data: Dictionary containing loaded indicators data
            
        Returns:
            Dict containing processed data with status and metadata
        """
        try:
            print_info("🔄 Processing indicators data...")
            
            start_time = time.time()
            processed_data = {}
            processing_stats = {
                'total_files': len(loaded_data),
                'successful_files': 0,
                'failed_files': 0,
                'total_rows': 0,
                'standardized_columns': 0,
                'validation_errors': []
            }
            
            for filename, file_data in loaded_data.items():
                print_info(f"  Processing {filename}...")
                
                # Process individual file
                result = self._process_single_file(file_data)
                
                if result['status'] == 'success':
                    processed_data[filename] = result['data']
                    processing_stats['successful_files'] += 1
                    processing_stats['total_rows'] += result['data']['rows']
                    processing_stats['standardized_columns'] += len(result['data']['standardized_columns'])
                else:
                    processing_stats['failed_files'] += 1
                    processing_stats['validation_errors'].append({
                        'file': filename,
                        'error': result['message']
                    })
                    print_warning(f"    Failed to process {filename}: {result['message']}")
            
            processing_time = time.time() - start_time
            
            print_success(f"✅ Processed {processing_stats['successful_files']}/{processing_stats['total_files']} files")
            
            return {
                'status': 'success',
                'data': processed_data,
                'metadata': {
                    'processing_stats': processing_stats,
                    'processing_time': processing_time,
                    'total_rows': processing_stats['total_rows']
                }
            }
            
        except Exception as e:
            print_error(f"Error processing indicators data: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def process_single_indicator(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single indicator file.
        
        Args:
            file_data: Dictionary containing single file data
            
        Returns:
            Dict containing processed indicator data
        """
        try:
            result = self._process_single_file(file_data)
            return result
            
        except Exception as e:
            print_error(f"Error processing single indicator: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _process_single_file(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single indicators file."""
        try:
            df = file_data['data'].copy()
            original_columns = list(df.columns)
            
            # Step 1: Standardize column names
            df = self._standardize_columns(df)
            
            # Step 2: Validate required columns
            validation_result = self._validate_required_columns(df)
            if not validation_result['valid']:
                return {
                    'status': 'error',
                    'message': f"Missing required columns: {validation_result['missing']}"
                }
            
            # Step 3: Clean and validate data
            df = self._clean_data(df)
            
            # Step 4: Add metadata columns
            df = self._add_metadata_columns(df, file_data)
            
            # Step 5: Sort by timestamp if available
            df = self._sort_by_timestamp(df)
            
            # Step 6: Final validation
            final_validation = self._final_validation(df)
            if not final_validation['valid']:
                return {
                    'status': 'error',
                    'message': f"Final validation failed: {final_validation['errors']}"
                }
            
            # Create processed data structure
            processed_data = {
                'data': df,
                'original_columns': original_columns,
                'standardized_columns': list(df.columns),
                'rows': len(df),
                'format': file_data.get('format', 'unknown'),
                'indicator': file_data.get('indicator', 'unknown'),
                'symbol': file_data.get('symbol', 'unknown'),
                'timeframe': file_data.get('timeframe', 'unknown'),
                'file_path': file_data.get('file_path', ''),
                'processing_timestamp': datetime.now().isoformat()
            }
            
            return {
                'status': 'success',
                'data': processed_data
            }
            
        except Exception as e:
            print_error(f"Error processing file: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names to common format."""
        try:
            # Create column mapping
            column_mapping = {}
            
            # Map common column names
            common_mappings = {
                'time': 'timestamp',
                'datetime': 'timestamp',
                'date': 'timestamp',
                't': 'timestamp',
                'ts': 'timestamp',
                'val': 'value',
                'values': 'value',
                'price': 'value',
                'close': 'value',
                'symbol': 'symbol',
                'pair': 'symbol',
                'asset': 'symbol',
                'tf': 'timeframe',
                'period': 'timeframe',
                'ind': 'indicator',
                'name': 'indicator'
            }
            
            # Apply mappings
            for old_col, new_col in common_mappings.items():
                if old_col in df.columns:
                    column_mapping[old_col] = new_col
            
            # Rename columns
            df = df.rename(columns=column_mapping)
            
            # For Wave indicators, preserve all indicator columns instead of just one 'value'
            if 'DateTime' in df.columns:
                df = df.rename(columns={'DateTime': 'timestamp'})
            
            # Keep all numeric columns as they are - don't rename to 'value'
            # This preserves all Wave indicator data (Wave1, Wave2, Pressure, PV, etc.)
            
            return df
            
        except Exception as e:
            print_error(f"Error standardizing columns: {e}")
            return df
    
    def _validate_required_columns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate that required columns are present."""
        try:
            # For indicators data, we need at least timestamp and some numeric data
            missing_columns = []
            
            # Check for timestamp
            if 'timestamp' not in df.columns and df.index.name != 'timestamp':
                missing_columns.append('timestamp')
            
            # Check for at least one numeric column (indicators data)
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                missing_columns.append('numeric_data')
            
            return {
                'valid': len(missing_columns) == 0,
                'missing': missing_columns
            }
            
        except Exception as e:
            print_error(f"Error validating required columns: {e}")
            return {
                'valid': False,
                'missing': ['validation_error']
            }
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate data quality."""
        try:
            # Remove completely empty rows
            df = df.dropna(how='all')
            
            # Handle all numeric columns dynamically
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                # Convert to numeric, coercing errors to NaN
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Handle timestamp column
            if 'timestamp' in df.columns:
                # Convert to datetime
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                
                # Remove rows with invalid timestamps
                df = df.dropna(subset=['timestamp'])
                
                # Set timestamp as index
                df = df.set_index('timestamp')
            
            # Remove duplicate rows
            df = df.drop_duplicates()
            
            # Sort by index (timestamp) if available
            if not df.index.empty and df.index.name == 'timestamp':
                df = df.sort_index()
            
            return df
            
        except Exception as e:
            print_error(f"Error cleaning data: {e}")
            return df
    
    def _add_metadata_columns(self, df: pd.DataFrame, file_data: Dict[str, Any]) -> pd.DataFrame:
        """Add metadata columns to the dataframe."""
        try:
            # Add indicator name if not present
            if 'indicator' not in df.columns:
                df['indicator'] = file_data.get('indicator', 'unknown')
            
            # Add symbol if not present
            if 'symbol' not in df.columns:
                # Use symbol from file_data if available, otherwise extract from path
                symbol = file_data.get('symbol', 'unknown')
                if symbol == 'unknown':
                    file_path = file_data.get('file_path', '')
                    if file_path:
                        symbol = self._extract_symbol_from_path(file_path)
                df['symbol'] = symbol
            
            # Add timeframe if not present
            if 'timeframe' not in df.columns:
                # Use timeframe from file_data if available, otherwise extract from path
                timeframe = file_data.get('timeframe', 'unknown')
                if timeframe == 'unknown':
                    file_path = file_data.get('file_path', '')
                    if file_path:
                        timeframe = self._extract_timeframe_from_path(file_path)
                df['timeframe'] = timeframe
            
            # Add processing timestamp
            df['processed_at'] = datetime.now().isoformat()
            
            return df
            
        except Exception as e:
            print_error(f"Error adding metadata columns: {e}")
            return df
    
    def _extract_timeframe_from_path(self, file_path: str) -> str:
        """Extract timeframe from file path."""
        try:
            import re
            from pathlib import Path
            
            filename = Path(file_path).name
            
            # Pattern for binance_BTCUSDT_D1_Wave.parquet
            binance_match = re.search(r'binance_[A-Z0-9]+_([A-Z0-9]+)_', filename)
            if binance_match:
                return binance_match.group(1)
            
            # Pattern for CSVExport_GOOG.NAS_PERIOD_MN1_Wave.parquet
            csv_match = re.search(r'CSVExport_[A-Z0-9.]+_PERIOD_([A-Z0-9]+)_', filename)
            if csv_match:
                return csv_match.group(1)
            
            # Look for common timeframe patterns
            timeframe_patterns = ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1', 'W1', 'MN1']
            for pattern in timeframe_patterns:
                if pattern in filename.upper():
                    return pattern
            
            return 'unknown'
            
        except Exception as e:
            print_error(f"Error extracting timeframe from {file_path}: {e}")
            return 'unknown'
    
    def _extract_symbol_from_path(self, file_path: str) -> str:
        """Extract symbol from file path."""
        try:
            import re
            from pathlib import Path
            
            filename = Path(file_path).name
            
            # Pattern for binance_BTCUSDT_D1_Wave.parquet
            binance_match = re.search(r'binance_([A-Z0-9]+)_', filename)
            if binance_match:
                return binance_match.group(1)
            
            # Pattern for CSVExport_GOOG.NAS_PERIOD_MN1_Wave.parquet
            csv_match = re.search(r'CSVExport_([A-Z0-9.]+)_', filename)
            if csv_match:
                return csv_match.group(1)
            
            # Look for common symbol patterns in all parts
            if '_' in filename:
                parts = filename.split('_')
                for part in parts:
                    part_upper = part.upper()
                    # Check if part looks like a trading pair (contains letters and numbers)
                    if len(part_upper) >= 3 and any(c.isalpha() for c in part_upper) and any(c.isdigit() for c in part_upper):
                        return part_upper
                    # Check for known symbols
                    if part_upper in ['BTCUSDT', 'ETHUSDT', 'EURUSD', 'GBPUSD', 'GOOG', 'TSLA', 'US500', 'XAUUSD', 'BTCUSD', 'ETHUSD']:
                        return part_upper
                    # Check for patterns like GOOG.NAS
                    if '.' in part_upper and len(part_upper.split('.')) == 2:
                        return part_upper
            
            return 'unknown'
            
        except Exception as e:
            print_error(f"Error extracting symbol from {file_path}: {e}")
            return 'unknown'
    
    def _sort_by_timestamp(self, df: pd.DataFrame) -> pd.DataFrame:
        """Sort dataframe by timestamp if available."""
        try:
            if 'timestamp' in df.columns:
                df = df.sort_values('timestamp')
            elif df.index.name == 'timestamp':
                df = df.sort_index()
            
            return df
            
        except Exception as e:
            print_error(f"Error sorting by timestamp: {e}")
            return df
    
    def _final_validation(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform final validation on processed data."""
        try:
            errors = []
            
            # Check if dataframe is empty
            if df.empty:
                errors.append("DataFrame is empty after processing")
            
            # Check for timestamp
            if 'timestamp' not in df.columns and df.index.name != 'timestamp':
                errors.append("Timestamp column is missing")
            
            # Check for at least one numeric column
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                errors.append("No numeric data columns found")
            
            # Check for valid numeric data in at least one column
            if len(numeric_cols) > 0:
                has_valid_data = False
                for col in numeric_cols:
                    if not df[col].isna().all():
                        has_valid_data = True
                        break
                
                if not has_valid_data:
                    errors.append("All numeric columns contain only NaN values")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors
            }
            
        except Exception as e:
            print_error(f"Error in final validation: {e}")
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"]
            }
    
    def get_processing_summary(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get summary of processed data."""
        try:
            summary = {
                'total_files': len(processed_data),
                'total_rows': 0,
                'indicators': set(),
                'formats': set(),
                'symbols': set(),
                'timeframes': set(),
                'date_ranges': {}
            }
            
            for filename, data in processed_data.items():
                df = data['data']
                summary['total_rows'] += len(df)
                summary['indicators'].add(data.get('indicator', 'unknown'))
                summary['formats'].add(data.get('format', 'unknown'))
                
                if 'symbol' in df.columns:
                    summary['symbols'].update(df['symbol'].unique())
                if 'timeframe' in df.columns:
                    summary['timeframes'].update(df['timeframe'].unique())
                
                # Get date range if timestamp is available
                if 'timestamp' in df.columns and not df.empty:
                    start_date = df['timestamp'].min()
                    end_date = df['timestamp'].max()
                    summary['date_ranges'][filename] = {
                        'start': str(start_date),
                        'end': str(end_date)
                    }
                elif df.index.name == 'timestamp' and not df.empty:
                    start_date = df.index.min()
                    end_date = df.index.max()
                    summary['date_ranges'][filename] = {
                        'start': str(start_date),
                        'end': str(end_date)
                    }
            
            # Convert sets to lists for JSON serialization
            summary['indicators'] = list(summary['indicators'])
            summary['formats'] = list(summary['formats'])
            summary['symbols'] = list(summary['symbols'])
            summary['timeframes'] = list(summary['timeframes'])
            
            return summary
            
        except Exception as e:
            print_error(f"Error creating processing summary: {e}")
            return {}
