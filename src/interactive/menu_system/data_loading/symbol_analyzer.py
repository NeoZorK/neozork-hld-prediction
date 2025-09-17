# -*- coding: utf-8 -*-
"""
Symbol Analyzer for NeoZork Interactive ML Trading Strategy Development.

This module provides utilities for analyzing symbol folders and extracting
detailed information about timeframes, file sizes, and data ranges.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from src.common.logger import print_error


class SymbolAnalyzer:
    """
    Analyzer for symbol folders in cleaned data directory.
    
    Features:
    - Analyze symbol folder structure
    - Extract timeframe information
    - Calculate file sizes and row counts
    - Determine date ranges
    - Load metadata from JSON files
    """
    
    def __init__(self):
        """Initialize the symbol analyzer."""
        self.data_root = Path("data/cleaned_data")
    
    def analyze_symbol_folder(self, symbol_folder: Path) -> Dict[str, Any]:
        """
        Analyze a symbol folder for detailed information.
        
        Args:
            symbol_folder: Path to the symbol folder
            
        Returns:
            Dictionary with symbol analysis results
        """
        try:
            # Get all timeframe folders
            timeframe_folders = [f for f in symbol_folder.iterdir() 
                               if f.is_dir() and f.name != '__pycache__']
            
            timeframes = []
            timeframe_details = {}
            total_size_mb = 0
            total_files = 0
            start_date = "No data"
            end_date = "No data"
            
            for tf_folder in sorted(timeframe_folders):
                tf_name = tf_folder.name.upper()
                timeframes.append(tf_name)
                
                # Get parquet file
                parquet_file = tf_folder / f"{symbol_folder.name}_{tf_name.lower()}.parquet"
                if parquet_file.exists():
                    # Get file size
                    file_size_mb = parquet_file.stat().st_size / (1024 * 1024)
                    total_size_mb += file_size_mb
                    total_files += 1
                    
                    # Load metadata if available
                    metadata_file = tf_folder / "metadata.json"
                    if metadata_file.exists():
                        try:
                            with open(metadata_file, 'r') as f:
                                metadata = json.load(f)
                            
                            tf_info = {
                                'size_mb': file_size_mb,
                                'rows': metadata.get('rows', 0),
                                'start_date': metadata.get('start_date', 'No data'),
                                'end_date': metadata.get('end_date', 'No data'),
                                'columns': metadata.get('columns', [])
                            }
                            
                            # Update overall start/end dates
                            if tf_info['start_date'] != 'No data' and start_date == "No data":
                                start_date = tf_info['start_date']
                            elif tf_info['start_date'] != 'No data' and tf_info['start_date'] < start_date:
                                start_date = tf_info['start_date']
                            
                            if tf_info['end_date'] != 'No data' and end_date == "No data":
                                end_date = tf_info['end_date']
                            elif tf_info['end_date'] != 'No data' and tf_info['end_date'] > end_date:
                                end_date = tf_info['end_date']
                                
                        except Exception as e:
                            print_error(f"Error reading metadata for {tf_name}: {e}")
                            tf_info = {
                                'size_mb': file_size_mb,
                                'rows': 0,
                                'start_date': 'No data',
                                'end_date': 'No data',
                                'columns': []
                            }
                    else:
                        tf_info = {
                            'size_mb': file_size_mb,
                            'rows': 0,
                            'start_date': 'No data',
                            'end_date': 'No data',
                            'columns': []
                        }
                    
                    timeframe_details[tf_name] = tf_info
            
            return {
                'timeframes': timeframes,
                'timeframe_details': timeframe_details,
                'total_size_mb': total_size_mb,
                'file_count': total_files,
                'start_date': start_date,
                'end_date': end_date
            }
            
        except Exception as e:
            print_error(f"Error analyzing symbol folder {symbol_folder}: {e}")
            return {
                'timeframes': [],
                'timeframe_details': {},
                'total_size_mb': 0,
                'file_count': 0,
                'start_date': 'No data',
                'end_date': 'No data'
            }
    
    def analyze_all_symbols(self) -> Dict[str, Any]:
        """
        Analyze all symbol folders in cleaned data directory.
        
        Returns:
            Dictionary with analysis results for all symbols
        """
        if not self.data_root.exists():
            return {
                "status": "error",
                "message": "Cleaned data directory not found",
                "symbols": {}
            }
        
        # Get all symbol folders
        symbol_folders = [f for f in self.data_root.iterdir() if f.is_dir()]
        
        if not symbol_folders:
            return {
                "status": "error",
                "message": "No symbol folders found in cleaned data",
                "symbols": {}
            }
        
        symbol_info = {}
        total_size = 0
        
        for symbol_folder in sorted(symbol_folders):
            symbol_name = symbol_folder.name.upper()
            symbol_info[symbol_name] = self.analyze_symbol_folder(symbol_folder)
            total_size += symbol_info[symbol_name]['total_size_mb']
        
        return {
            "status": "success",
            "symbols": symbol_info,
            "total_symbols": len(symbol_folders),
            "total_size_mb": total_size
        }
    
    def get_symbol_timeframes(self, symbol: str) -> list:
        """
        Get available timeframes for a specific symbol.
        
        Args:
            symbol: Symbol name (e.g., 'EURUSD')
            
        Returns:
            List of available timeframes
        """
        symbol_folder = self.data_root / symbol.lower()
        if not symbol_folder.exists():
            return []
        
        analysis = self.analyze_symbol_folder(symbol_folder)
        return analysis['timeframes']
    
    def get_symbol_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific symbol.
        
        Args:
            symbol: Symbol name (e.g., 'EURUSD')
            
        Returns:
            Dictionary with symbol information or None if not found
        """
        symbol_folder = self.data_root / symbol.lower()
        if not symbol_folder.exists():
            return None
        
        return self.analyze_symbol_folder(symbol_folder)
