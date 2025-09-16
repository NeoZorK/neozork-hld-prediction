# -*- coding: utf-8 -*-
"""
Indicators Data Analyzer for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive analysis of indicators data from multiple formats
(parquet, json, csv) with detailed metadata extraction and folder structure analysis.
"""

import os
import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import colorama
from colorama import Fore, Style

from src.common.logger import print_error, print_info, print_success, print_warning


class IndicatorsAnalyzer:
    """
    Analyzer for indicators data from multiple formats.
    
    Provides comprehensive analysis of indicators folder structure,
    file metadata extraction, and data quality assessment.
    """
    
    def __init__(self):
        """Initialize the indicators analyzer."""
        self.indicators_path = Path("data/indicators")
        self.supported_formats = ['.parquet', '.json', '.csv']
        
    def analyze_indicators_folder(self) -> Dict[str, Any]:
        """
        Analyze the indicators folder structure and extract metadata.
        
        Returns:
            Dict containing analysis results with status, folder info, 
            indicators found, and subfolder information.
        """
        try:
            print_info("🔍 Analyzing indicators folder structure...")
            
            # Check if indicators folder exists
            if not self.indicators_path.exists():
                return {
                    "status": "error",
                    "message": f"Indicators folder not found: {self.indicators_path}"
                }
            
            # Analyze main folder
            folder_info = self._analyze_folder_structure(self.indicators_path)
            
            # Find all indicators files
            indicators_files = self._find_indicators_files()
            
            # Analyze subfolders (parquet, json, csv)
            subfolders_info = self._analyze_subfolders()
            
            # Extract indicators metadata
            indicators_metadata = self._extract_indicators_metadata(indicators_files)
            
            # Get unique indicators list
            indicators_list = list(set(indicators_metadata.keys()))
            
            print_success(f"✅ Found {len(indicators_list)} indicators in {len(subfolders_info)} subfolders")
            
            return {
                "status": "success",
                "folder_info": folder_info,
                "indicators": indicators_list,
                "subfolders_info": subfolders_info,
                "files_info": indicators_metadata,
                "total_files": len(indicators_files),
                "total_size_mb": sum(info['size_mb'] for info in indicators_metadata.values())
            }
            
        except Exception as e:
            print_error(f"Error analyzing indicators folder: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _analyze_folder_structure(self, folder_path: Path) -> Dict[str, Any]:
        """Analyze basic folder structure information."""
        try:
            # Get folder statistics
            files = list(folder_path.rglob('*'))
            file_count = len([f for f in files if f.is_file()])
            
            # Calculate total size
            total_size = sum(f.stat().st_size for f in files if f.is_file())
            total_size_mb = total_size / (1024 * 1024)
            
            # Get modification time
            modified_time = datetime.fromtimestamp(folder_path.stat().st_mtime)
            modified_str = modified_time.strftime("%Y-%m-%d %H:%M:%S")
            
            return {
                "path": str(folder_path),
                "file_count": file_count,
                "size_mb": round(total_size_mb, 2),
                "modified": modified_str
            }
            
        except Exception as e:
            print_error(f"Error analyzing folder structure: {e}")
            return {
                "path": str(folder_path),
                "file_count": 0,
                "size_mb": 0,
                "modified": "Unknown"
            }
    
    def _find_indicators_files(self) -> List[Path]:
        """Find all indicators files in supported formats."""
        indicators_files = []
        
        try:
            for format_ext in self.supported_formats:
                pattern = f"**/*{format_ext}"
                files = list(self.indicators_path.glob(pattern))
                indicators_files.extend(files)
            
            return indicators_files
            
        except Exception as e:
            print_error(f"Error finding indicators files: {e}")
            return []
    
    def _analyze_subfolders(self) -> Dict[str, Dict[str, Any]]:
        """Analyze subfolders (parquet, json, csv) for detailed information."""
        subfolders_info = {}
        
        try:
            for subfolder_name in ['parquet', 'json', 'csv']:
                subfolder_path = self.indicators_path / subfolder_name
                
                if subfolder_path.exists():
                    subfolder_info = self._analyze_folder_structure(subfolder_path)
                    
                    # Get files in this subfolder
                    files_info = {}
                    for file_path in subfolder_path.iterdir():
                        if file_path.is_file() and file_path.suffix in self.supported_formats:
                            file_info = self._analyze_single_file(file_path)
                            if file_info:
                                files_info[file_path.name] = file_info
                    
                    subfolder_info['files_info'] = files_info
                    subfolders_info[subfolder_name] = subfolder_info
                    
        except Exception as e:
            print_error(f"Error analyzing subfolders: {e}")
        
        return subfolders_info
    
    def _extract_indicators_metadata(self, files: List[Path]) -> Dict[str, Dict[str, Any]]:
        """Extract metadata from indicators files."""
        metadata = {}
        
        try:
            for file_path in files:
                file_info = self._analyze_single_file(file_path)
                if file_info:
                    metadata[file_path.name] = file_info
                    
        except Exception as e:
            print_error(f"Error extracting indicators metadata: {e}")
        
        return metadata
    
    def _analyze_single_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a single indicators file and extract metadata."""
        try:
            # Basic file info
            file_size = file_path.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            # Get file format
            file_format = file_path.suffix.lower()
            
            # Extract indicator name and source from filename
            indicator_name = self._extract_indicator_name(file_path.name)
            source = self._extract_source_from_filename(file_path.name)
            
            # Try to get data info based on format
            data_info = self._get_data_info(file_path, file_format)
            
            return {
                'file_path': str(file_path),
                'size_mb': round(file_size_mb, 2),
                'format': file_format,
                'indicator': indicator_name,
                'source': source,
                'rows': data_info.get('rows', 0),
                'columns': data_info.get('columns', []),
                'start_date': data_info.get('start_date', 'No time data'),
                'end_date': data_info.get('end_date', 'No time data'),
                'symbols': data_info.get('symbols', []),
                'timeframes': data_info.get('timeframes', [])
            }
            
        except Exception as e:
            print_error(f"Error analyzing file {file_path}: {e}")
            return None
    
    def _extract_indicator_name(self, filename: str) -> str:
        """Extract indicator name from filename."""
        try:
            # Remove extension
            name = filename.split('.')[0]
            
            # Common patterns for indicator names
            if '_' in name:
                # Try to extract from patterns like "rsi_btcusd" or "macd_eurusd"
                parts = name.split('_')
                if len(parts) >= 2:
                    # Check if first part looks like an indicator
                    indicator_candidates = ['rsi', 'macd', 'sma', 'ema', 'bb', 'stoch', 'adx', 'cci', 'williams', 'wave', 'rsi_mom', 'rsi_div']
                    if parts[0].lower() in indicator_candidates:
                        return parts[0].upper()
            
            # If no clear pattern, return the name as is
            return name.upper()
            
        except Exception as e:
            print_error(f"Error extracting indicator name from {filename}: {e}")
            return filename.upper()
    
    def _extract_source_from_filename(self, filename: str) -> str:
        """Extract source from filename."""
        try:
            # Remove extension
            name = filename.split('.')[0]
            
            # Common source patterns
            if 'csvexport' in name.lower():
                return 'csvexport'
            elif 'binance' in name.lower():
                return 'binance'
            elif 'polygon' in name.lower():
                return 'polygon'
            elif 'yfinance' in name.lower():
                return 'yfinance'
            else:
                return 'unknown'
                
        except Exception as e:
            print_error(f"Error extracting source from {filename}: {e}")
            return 'unknown'
    
    def _get_data_info(self, file_path: Path, file_format: str) -> Dict[str, Any]:
        """Get data information based on file format."""
        try:
            if file_format == '.parquet':
                return self._get_parquet_data_info(file_path)
            elif file_format == '.json':
                return self._get_json_data_info(file_path)
            elif file_format == '.csv':
                return self._get_csv_data_info(file_path)
            else:
                return {}
                
        except Exception as e:
            print_error(f"Error getting data info for {file_path}: {e}")
            return {}
    
    def _get_parquet_data_info(self, file_path: Path) -> Dict[str, Any]:
        """Get data info from parquet file."""
        try:
            df = pd.read_parquet(file_path)
            
            # Basic info
            rows = len(df)
            columns = list(df.columns)
            
            # Try to find time-related columns
            time_columns = [col for col in columns if any(keyword in col.lower() 
                          for keyword in ['time', 'date', 'timestamp'])]
            
            start_date = "No time data"
            end_date = "No time data"
            
            if time_columns:
                time_col = time_columns[0]
                if not df.empty:
                    start_date = str(df[time_col].min())
                    end_date = str(df[time_col].max())
            
            # Try to find symbol columns
            symbol_columns = [col for col in columns if any(keyword in col.lower() 
                            for keyword in ['symbol', 'pair', 'asset'])]
            
            symbols = []
            if symbol_columns:
                symbol_col = symbol_columns[0]
                symbols = df[symbol_col].unique().tolist() if not df.empty else []
            
            return {
                'rows': rows,
                'columns': columns,
                'start_date': start_date,
                'end_date': end_date,
                'symbols': symbols,
                'timeframes': ['Unknown']  # Parquet files usually don't have timeframe info
            }
            
        except Exception as e:
            print_error(f"Error reading parquet file {file_path}: {e}")
            return {}
    
    def _get_json_data_info(self, file_path: Path) -> Dict[str, Any]:
        """Get data info from JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                rows = len(data)
                if rows > 0 and isinstance(data[0], dict):
                    columns = list(data[0].keys())
                else:
                    columns = []
            elif isinstance(data, dict):
                rows = 1
                columns = list(data.keys())
            else:
                rows = 0
                columns = []
            
            # Try to extract time and symbol info
            start_date = "No time data"
            end_date = "No time data"
            symbols = []
            
            if isinstance(data, list) and len(data) > 0:
                first_item = data[0]
                if isinstance(first_item, dict):
                    # Look for time fields
                    time_fields = [k for k in first_item.keys() if any(keyword in k.lower() 
                                 for keyword in ['time', 'date', 'timestamp'])]
                    if time_fields:
                        time_field = time_fields[0]
                        times = [item.get(time_field) for item in data if time_field in item]
                        if times:
                            start_date = str(min(times))
                            end_date = str(max(times))
                    
                    # Look for symbol fields
                    symbol_fields = [k for k in first_item.keys() if any(keyword in k.lower() 
                                   for keyword in ['symbol', 'pair', 'asset'])]
                    if symbol_fields:
                        symbol_field = symbol_fields[0]
                        symbols = list(set(item.get(symbol_field) for item in data 
                                         if symbol_field in item and item.get(symbol_field)))
            
            return {
                'rows': rows,
                'columns': columns,
                'start_date': start_date,
                'end_date': end_date,
                'symbols': symbols,
                'timeframes': ['Unknown']
            }
            
        except Exception as e:
            print_error(f"Error reading JSON file {file_path}: {e}")
            return {}
    
    def _get_csv_data_info(self, file_path: Path) -> Dict[str, Any]:
        """Get data info from CSV file."""
        try:
            # Read just the first few rows to get column info
            df_sample = pd.read_csv(file_path, nrows=100)
            
            # Get total rows by reading the file
            with open(file_path, 'r') as f:
                total_rows = sum(1 for line in f) - 1  # Subtract header
            
            columns = list(df_sample.columns)
            
            # Try to find time-related columns
            time_columns = [col for col in columns if any(keyword in col.lower() 
                          for keyword in ['time', 'date', 'timestamp'])]
            
            start_date = "No time data"
            end_date = "No time data"
            
            if time_columns:
                time_col = time_columns[0]
                # Read the full file to get time range
                df_full = pd.read_csv(file_path, usecols=[time_col])
                if not df_full.empty:
                    start_date = str(df_full[time_col].min())
                    end_date = str(df_full[time_col].max())
            
            # Try to find symbol columns
            symbol_columns = [col for col in columns if any(keyword in col.lower() 
                            for keyword in ['symbol', 'pair', 'asset'])]
            
            symbols = []
            if symbol_columns:
                symbol_col = symbol_columns[0]
                df_symbols = pd.read_csv(file_path, usecols=[symbol_col])
                symbols = df_symbols[symbol_col].unique().tolist() if not df_symbols.empty else []
            
            return {
                'rows': total_rows,
                'columns': columns,
                'start_date': start_date,
                'end_date': end_date,
                'symbols': symbols,
                'timeframes': ['Unknown']
            }
            
        except Exception as e:
            print_error(f"Error reading CSV file {file_path}: {e}")
            return {}
