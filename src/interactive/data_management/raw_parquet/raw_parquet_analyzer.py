# -*- coding: utf-8 -*-
"""
Raw Parquet Analyzer for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive analysis of raw parquet files from various exchanges,
extracting detailed metadata, symbols, timeframes, and data quality information.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import time
from datetime import datetime
import colorama
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.common.logger import print_info, print_warning, print_error, print_success, print_debug

class RawParquetAnalyzer:
    """
    Comprehensive analyzer for raw parquet files from exchanges.
    
    Features:
    - Analyze file sizes and counts
    - Extract row counts and date ranges
    - Determine timeframes and symbols
    - Identify data sources and exchanges
    - Calculate data quality metrics
    - Progress tracking with ETA
    """
    
    def __init__(self):
        """Initialize the raw parquet analyzer."""
        self.project_root = PROJECT_ROOT
        self.data_root = self.project_root / "data"
        self.raw_root = self.data_root / "raw_parquet"
    
    def analyze_raw_parquet_folder(self) -> Dict[str, Any]:
        """
        Analyze raw parquet folder for detailed information with progress tracking.
        
        Returns:
            Dictionary with detailed folder and file information
        """
        if not self.raw_root.exists():
            return {
                "status": "error",
                "message": "Raw parquet directory not found",
                "folder_info": {},
                "files_info": {},
                "sources": [],
                "symbols_by_source": {}
            }
        
        # Get folder information
        folder_info = self._get_folder_info(self.raw_root)
        
        # Get files information with progress tracking
        files_info = {}
        sources = set()
        symbols_by_source = {}
        
        parquet_files = list(self.raw_root.glob("*.parquet"))
        total_files = len(parquet_files)
        
        if total_files == 0:
            return {
                "status": "success",
                "folder_info": folder_info,
                "files_info": files_info,
                "sources": [],
                "symbols_by_source": {}
            }
        
        # Progress tracking variables
        start_time = time.time()
        
        print_info("📊 Analyzing raw parquet files...")
        
        for i, file_path in enumerate(parquet_files):
            # Calculate progress
            progress = (i + 1) / total_files
            
            # Calculate ETA
            current_time = time.time()
            elapsed_time = current_time - start_time
            if i > 0:  # Avoid division by zero
                avg_time_per_file = elapsed_time / i
                remaining_files = total_files - i
                eta_seconds = remaining_files * avg_time_per_file
                eta_str = self._format_time(eta_seconds)
            else:
                eta_str = "Calculating..."
            
            # Calculate speed (files per second)
            if elapsed_time > 0:
                speed = f"{i / elapsed_time:.1f} files/s"
            else:
                speed = "Starting..."
            
            # Show progress
            self._show_progress(f"Analyzing {file_path.name}", progress, eta_str, speed)
            
            file_info = self._analyze_parquet_file(file_path)
            if file_info:
                files_info[file_path.name] = file_info
                
                # Extract source and symbol from filename
                source, symbol = self._extract_source_and_symbol_from_filename(file_path.name)
                if source:
                    sources.add(source)
                    if source not in symbols_by_source:
                        symbols_by_source[source] = set()
                    if symbol:
                        symbols_by_source[source].add(symbol)
        
        # Final progress display
        total_time = time.time() - start_time
        self._show_progress(f"Completed analysis of {total_files} files", 1.0, "", f"{total_files / total_time:.1f} files/s")
        
        # Convert sets to sorted lists
        for source in symbols_by_source:
            symbols_by_source[source] = sorted(list(symbols_by_source[source]))
        
        return {
            "status": "success",
            "folder_info": folder_info,
            "files_info": files_info,
            "sources": sorted(list(sources)),
            "symbols_by_source": symbols_by_source
        }
    
    def analyze_source_files(self, source: str) -> Dict[str, Any]:
        """
        Analyze files from a specific source.
        
        Args:
            source: Source name (e.g., 'binance', 'bybit')
            
        Returns:
            Dictionary with source-specific file information
        """
        if not self.raw_root.exists():
            return {
                "status": "error",
                "message": "Raw parquet directory not found"
            }
        
        # Find files for this source
        pattern = f"{source.lower()}_*.parquet"
        source_files = list(self.raw_root.glob(pattern))
        
        if not source_files:
            return {
                "status": "error",
                "message": f"No files found for source: {source}"
            }
        
        files_info = {}
        symbols = set()
        
        for file_path in source_files:
            file_info = self._analyze_parquet_file(file_path)
            if file_info:
                files_info[file_path.name] = file_info
                
                # Extract symbol
                _, symbol = self._extract_source_and_symbol_from_filename(file_path.name)
                if symbol:
                    symbols.add(symbol)
        
        return {
            "status": "success",
            "source": source,
            "files_info": files_info,
            "symbols": sorted(list(symbols)),
            "file_count": len(files_info)
        }
    
    def analyze_symbol_files(self, symbol: str) -> Dict[str, Any]:
        """
        Analyze files for a specific symbol across all sources.
        
        Args:
            symbol: Symbol name (e.g., 'BTCUSDT', 'EURUSD')
            
        Returns:
            Dictionary with symbol-specific file information
        """
        if not self.raw_root.exists():
            return {
                "status": "error",
                "message": "Raw parquet directory not found"
            }
        
        # Find files for this symbol
        pattern = f"*{symbol.upper()}*.parquet"
        symbol_files = list(self.raw_root.glob(pattern))
        
        if not symbol_files:
            return {
                "status": "error",
                "message": f"No files found for symbol: {symbol}"
            }
        
        files_info = {}
        sources = set()
        
        for file_path in symbol_files:
            file_info = self._analyze_parquet_file(file_path)
            if file_info:
                files_info[file_path.name] = file_info
                
                # Extract source
                source, _ = self._extract_source_and_symbol_from_filename(file_path.name)
                if source:
                    sources.add(source)
        
        return {
            "status": "success",
            "symbol": symbol.upper(),
            "files_info": files_info,
            "sources": sorted(list(sources)),
            "file_count": len(files_info)
        }
    
    def _get_folder_info(self, folder_path: Path) -> Dict[str, Any]:
        """Get detailed information about a folder."""
        try:
            # Count files
            file_count = len(list(folder_path.glob("*.parquet")))
            
            # Calculate folder size
            folder_size = sum(f.stat().st_size for f in folder_path.rglob('*.parquet') if f.is_file())
            folder_size_mb = folder_size / (1024 * 1024)
            
            # Get modification time
            mod_time = datetime.fromtimestamp(folder_path.stat().st_mtime)
            
            return {
                "path": str(folder_path),
                "file_count": file_count,
                "size_mb": round(folder_size_mb, 2),
                "modified": mod_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print_error(f"Error analyzing folder {folder_path}: {e}")
            return {
                "path": str(folder_path),
                "file_count": 0,
                "size_mb": 0,
                "modified": "Unknown"
            }
    
    def _analyze_parquet_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a parquet file for detailed information."""
        try:
            # Get file size
            file_size = file_path.stat().st_size / (1024 * 1024)  # MB
            
            # Load parquet file to get row count and date range
            df = pd.read_parquet(file_path)
            row_count = len(df)
            
            # Get date range and timeframes
            start_date, end_date, timeframes = self._get_date_range_from_dataframe(df)
            
            # Extract timeframe from filename
            timeframe_from_filename = self._extract_timeframe_from_filename(file_path.name)
            
            # Use timeframe from filename if available, otherwise use timeframes from data
            if timeframe_from_filename:
                final_timeframes = [timeframe_from_filename]
            else:
                final_timeframes = timeframes
            
            # Calculate data quality metrics
            quality_metrics = self._calculate_data_quality_metrics(df)
            
            return {
                "file_path": str(file_path),
                "size_mb": round(file_size, 2),
                "rows": row_count,
                "start_date": start_date,
                "end_date": end_date,
                "timeframes": final_timeframes,
                "columns": list(df.columns),
                "quality_metrics": quality_metrics
            }
        except Exception as e:
            print_error(f"Error analyzing parquet file {file_path}: {e}")
            return None
    
    def _get_date_range_from_dataframe(self, df: pd.DataFrame) -> Tuple[str, str, List[str]]:
        """Extract date range and timeframes from a dataframe."""
        try:
            # First check if the index is datetime
            if isinstance(df.index, pd.DatetimeIndex):
                time_series = df.index
            else:
                # Look for time columns
                time_col = None
                for col in ['timestamp', 'Timestamp', 'time', 'Time', 'datetime', 'DateTime', 'open_time', 'close_time']:
                    if col in df.columns:
                        time_col = col
                        break
                
                if time_col and not df[time_col].empty:
                    # Convert to datetime if needed
                    if not pd.api.types.is_datetime64_any_dtype(df[time_col]):
                        time_series = pd.to_datetime(df[time_col], errors='coerce')
                    else:
                        time_series = df[time_col]
                else:
                    # No time data available
                    return "No time data", "No time data", ["No time data"]
            
            if not time_series.empty:
                start_date = time_series.min()
                end_date = time_series.max()
                
                # Get timeframes (sample of unique hours)
                timeframes = time_series.floor('h').value_counts().index.tolist()[:5]
                timeframes = [str(tf) for tf in timeframes]
                
                return str(start_date), str(end_date), timeframes
            else:
                return "No time data", "No time data", ["No time data"]
        except Exception as e:
            print_error(f"Error extracting date range: {e}")
            return "No time data", "No time data", ["No time data"]
    
    def _extract_source_and_symbol_from_filename(self, filename: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract source and symbol from filename."""
        try:
            # Remove extension
            name = Path(filename).stem
            
            # Look for patterns like source_SYMBOL_TIMEFRAME
            parts = name.split("_")
            if len(parts) >= 2:
                source = parts[0].lower()
                symbol = parts[1].upper()
                return source, symbol
            
            # Look for patterns like SYMBOL_source_TIMEFRAME
            if len(parts) >= 3:
                symbol = parts[0].upper()
                source = parts[1].lower()
                return source, symbol
            
            return None, None
        except Exception as e:
            print_error(f"Error extracting source and symbol from {filename}: {e}")
            return None, None
    
    def _extract_timeframe_from_filename(self, filename: str) -> Optional[str]:
        """Extract timeframe from filename."""
        try:
            # Remove extension
            name = Path(filename).stem
            
            # Look for patterns like source_SYMBOL_TIMEFRAME
            parts = name.split("_")
            if len(parts) >= 3:
                # Check if last part looks like a timeframe
                last_part = parts[-1].upper()
                if last_part in ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1', 'W1', 'MN1']:
                    return last_part
            
            return None
        except Exception as e:
            print_error(f"Error extracting timeframe from {filename}: {e}")
            return None
    
    def _calculate_data_quality_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate data quality metrics for the dataframe."""
        try:
            metrics = {
                "total_rows": len(df),
                "null_counts": {},
                "duplicate_rows": 0,
                "data_types": {},
                "numeric_columns": [],
                "datetime_columns": []
            }
            
            # Count nulls in each column
            for col in df.columns:
                null_count = df[col].isnull().sum()
                metrics["null_counts"][col] = null_count
            
            # Count duplicate rows
            metrics["duplicate_rows"] = df.duplicated().sum()
            
            # Get data types
            for col in df.columns:
                metrics["data_types"][col] = str(df[col].dtype)
            
            # Identify numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            metrics["numeric_columns"] = numeric_cols
            
            # Identify datetime columns
            datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
            metrics["datetime_columns"] = datetime_cols
            
            return metrics
        except Exception as e:
            print_error(f"Error calculating data quality metrics: {e}")
            return {}
    
    def _show_progress(self, message: str, progress: float = 0.0, eta: str = "", speed: str = ""):
        """Show progress with ETA, percentage, and speed in a single line."""
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        percentage = int(progress * 100)
        
        # Create progress display
        progress_display = f"{Fore.CYAN}📊 {message}"
        bar_display = f"{Fore.GREEN}[{bar}]{Fore.CYAN}"
        percentage_display = f"{Fore.YELLOW}{percentage:3d}%"
        
        # Add ETA and speed if available
        extra_info = ""
        if eta:
            extra_info += f" {Fore.MAGENTA}ETA: {eta}"
        if speed:
            extra_info += f" {Fore.BLUE}Speed: {speed}"
        
        # Combine all parts
        full_display = f"\r{progress_display} {bar_display} {percentage_display}{extra_info}{Style.RESET_ALL}"
        
        # Ensure the line is long enough to clear previous content
        terminal_width = 120  # Assume minimum terminal width
        if len(full_display) < terminal_width:
            full_display += " " * (terminal_width - len(full_display))
        
        print(full_display, end="", flush=True)
        
        if progress >= 1.0:
            print()  # New line when complete
    
    def _format_time(self, seconds: float) -> str:
        """Format time in seconds to human readable format."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
