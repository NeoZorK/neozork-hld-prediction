# -*- coding: utf-8 -*-
"""
Raw Parquet Loader for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive loading functionality for raw parquet files
from various exchanges with progress tracking and data validation.
"""

import os
import sys
import time
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import colorama
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.common.logger import print_info, print_warning, print_error, print_success, print_debug

class RawParquetLoader:
    """
    Comprehensive loader for raw parquet files from exchanges.
    
    Features:
    - Load raw parquet data with progress tracking
    - Support for multiple sources and symbols
    - Data validation and quality checks
    - Memory-efficient loading
    - ETA calculation and speed tracking
    """
    
    def __init__(self):
        """Initialize the raw parquet loader."""
        self.project_root = PROJECT_ROOT
        self.data_root = self.project_root / "data"
        self.raw_root = self.data_root / "raw_parquet"
        self.cleaned_root = self.data_root / "cleaned_data"
    
    def load_raw_parquet_data(self, symbol_filter: Optional[str] = None, source_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Load raw parquet data with enhanced progress tracking.
        
        Args:
            symbol_filter: Optional filter for specific symbol (e.g., "btcusdt")
            source_filter: Optional filter for specific source (e.g., "binance")
            
        Returns:
            Dictionary containing loaded data and metadata
        """
        print_info("📊 Loading raw parquet data...")
        
        try:
            if not self.raw_root.exists():
                print_warning(f"Directory {self.raw_root} does not exist")
                return {"status": "error", "message": "Raw parquet directory not found"}
            
            # Find parquet files with filters
            pattern = "*.parquet"
            if symbol_filter and source_filter:
                pattern = f"{source_filter.lower()}_{symbol_filter.upper()}_*.parquet"
            elif symbol_filter:
                pattern = f"*{symbol_filter.upper()}*.parquet"
            elif source_filter:
                pattern = f"{source_filter.lower()}_*.parquet"
            
            parquet_files = list(self.raw_root.glob(pattern))
            
            if not parquet_files:
                print_warning(f"No parquet files found matching pattern: {pattern}")
                return {"status": "error", "message": f"No files found matching {pattern}"}
            
            loaded_data = {}
            total_size = 0
            total_rows = 0
            
            # Progress tracking variables
            start_time = time.time()
            total_files = len(parquet_files)
            
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
                self._show_progress(f"Loading {file_path.name}", progress, eta_str, speed)
                
                try:
                    # Load parquet file
                    df = pd.read_parquet(file_path)
                    
                    # Extract source and symbol from filename
                    source, symbol = self._extract_source_and_symbol_from_filename(file_path.name)
                    
                    # Create unique key for the data
                    if source and symbol:
                        data_key = f"{source}_{symbol}"
                    else:
                        data_key = file_path.stem
                    
                    # Calculate metadata
                    file_size = file_path.stat().st_size / (1024 * 1024)  # MB
                    total_size += file_size
                    total_rows += len(df)
                    
                    # Get time range
                    start_time_str, end_time_str, timeframes = self._get_date_range_from_dataframe(df)
                    
                    # Store loaded data
                    loaded_data[data_key] = {
                        "file_path": str(file_path),
                        "source": source or "unknown",
                        "symbol": symbol or "unknown",
                        "data": df,
                        "size_mb": round(file_size, 2),
                        "rows": len(df),
                        "start_time": start_time_str,
                        "end_time": end_time_str,
                        "timeframes": timeframes,
                        "columns": list(df.columns)
                    }
                    
                except Exception as e:
                    print_error(f"Error loading {file_path.name}: {e}")
                    continue
            
            # Final progress display
            total_time = time.time() - start_time
            self._show_progress(f"Completed loading {total_files} files", 1.0, "", f"{total_files / total_time:.1f} files/s")
            
            # Prepare metadata
            metadata = {
                "total_files": total_files,
                "total_size_mb": round(total_size, 2),
                "total_rows": total_rows,
                "sources": list(set(data["source"] for data in loaded_data.values())),
                "symbols": list(set(data["symbol"] for data in loaded_data.values())),
                "loading_time": total_time
            }
            
            return {
                "status": "success",
                "data": loaded_data,
                "metadata": metadata
            }
            
        except Exception as e:
            print_error(f"Error loading raw parquet data: {e}")
            return {"status": "error", "message": str(e)}
    
    def load_symbol_data(self, symbol: str, source: Optional[str] = None) -> Dict[str, Any]:
        """
        Load data for a specific symbol from raw parquet files.
        
        Args:
            symbol: Symbol name (e.g., "BTCUSDT")
            source: Optional source filter (e.g., "binance")
            
        Returns:
            Dictionary containing loaded symbol data
        """
        print_info(f"📊 Loading {symbol} data from raw parquet...")
        
        try:
            if not self.raw_root.exists():
                return {"status": "error", "message": "Raw parquet directory not found"}
            
            # Find files for this symbol
            if source:
                pattern = f"{source.lower()}_{symbol.upper()}_*.parquet"
            else:
                pattern = f"*{symbol.upper()}*.parquet"
            
            parquet_files = list(self.raw_root.glob(pattern))
            
            if not parquet_files:
                return {"status": "error", "message": f"No files found for symbol {symbol}"}
            
            loaded_data = {}
            total_size = 0
            total_rows = 0
            
            for file_path in parquet_files:
                try:
                    # Load parquet file
                    df = pd.read_parquet(file_path)
                    
                    # Extract source and timeframe from filename
                    source_name, _ = self._extract_source_and_symbol_from_filename(file_path.name)
                    timeframe = self._extract_timeframe_from_filename(file_path.name)
                    
                    # Calculate metadata
                    file_size = file_path.stat().st_size / (1024 * 1024)  # MB
                    total_size += file_size
                    total_rows += len(df)
                    
                    # Get time range
                    start_time_str, end_time_str, timeframes = self._get_date_range_from_dataframe(df)
                    
                    # Create timeframe key
                    timeframe_key = timeframe or "unknown"
                    
                    # Store loaded data
                    loaded_data[timeframe_key] = {
                        "file_path": str(file_path),
                        "source": source_name or "unknown",
                        "symbol": symbol.upper(),
                        "timeframe": timeframe_key,
                        "data": df,
                        "size_mb": round(file_size, 2),
                        "rows": len(df),
                        "start_time": start_time_str,
                        "end_time": end_time_str,
                        "columns": list(df.columns)
                    }
                    
                except Exception as e:
                    print_error(f"Error loading {file_path.name}: {e}")
                    continue
            
            if not loaded_data:
                return {"status": "error", "message": f"No valid data loaded for symbol {symbol}"}
            
            # Prepare metadata
            metadata = {
                "symbol": symbol.upper(),
                "source": source or "multiple",
                "timeframes": list(loaded_data.keys()),
                "total_files": len(parquet_files),
                "total_size_mb": round(total_size, 2),
                "total_rows": total_rows
            }
            
            return {
                "status": "success",
                "data": loaded_data,
                "metadata": metadata
            }
            
        except Exception as e:
            print_error(f"Error loading symbol data: {e}")
            return {"status": "error", "message": str(e)}
    
    def load_source_data(self, source: str, symbol_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Load data from a specific source.
        
        Args:
            source: Source name (e.g., "binance")
            symbol_filter: Optional symbol filter
            
        Returns:
            Dictionary containing loaded source data
        """
        print_info(f"📊 Loading {source} data from raw parquet...")
        
        try:
            if not self.raw_root.exists():
                return {"status": "error", "message": "Raw parquet directory not found"}
            
            # Find files for this source
            if symbol_filter:
                pattern = f"{source.lower()}_{symbol_filter.upper()}_*.parquet"
            else:
                pattern = f"{source.lower()}_*.parquet"
            
            parquet_files = list(self.raw_root.glob(pattern))
            
            if not parquet_files:
                return {"status": "error", "message": f"No files found for source {source}"}
            
            loaded_data = {}
            total_size = 0
            total_rows = 0
            symbols = set()
            
            for file_path in parquet_files:
                try:
                    # Load parquet file
                    df = pd.read_parquet(file_path)
                    
                    # Extract symbol and timeframe from filename
                    _, symbol = self._extract_source_and_symbol_from_filename(file_path.name)
                    timeframe = self._extract_timeframe_from_filename(file_path.name)
                    
                    if symbol:
                        symbols.add(symbol)
                    
                    # Calculate metadata
                    file_size = file_path.stat().st_size / (1024 * 1024)  # MB
                    total_size += file_size
                    total_rows += len(df)
                    
                    # Get time range
                    start_time_str, end_time_str, timeframes = self._get_date_range_from_dataframe(df)
                    
                    # Create data key
                    data_key = f"{symbol}_{timeframe}" if symbol and timeframe else file_path.stem
                    
                    # Store loaded data
                    loaded_data[data_key] = {
                        "file_path": str(file_path),
                        "source": source.lower(),
                        "symbol": symbol or "unknown",
                        "timeframe": timeframe or "unknown",
                        "data": df,
                        "size_mb": round(file_size, 2),
                        "rows": len(df),
                        "start_time": start_time_str,
                        "end_time": end_time_str,
                        "columns": list(df.columns)
                    }
                    
                except Exception as e:
                    print_error(f"Error loading {file_path.name}: {e}")
                    continue
            
            if not loaded_data:
                return {"status": "error", "message": f"No valid data loaded for source {source}"}
            
            # Prepare metadata
            metadata = {
                "source": source.lower(),
                "symbols": sorted(list(symbols)),
                "total_files": len(parquet_files),
                "total_size_mb": round(total_size, 2),
                "total_rows": total_rows
            }
            
            return {
                "status": "success",
                "data": loaded_data,
                "metadata": metadata
            }
            
        except Exception as e:
            print_error(f"Error loading source data: {e}")
            return {"status": "error", "message": str(e)}
    
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
