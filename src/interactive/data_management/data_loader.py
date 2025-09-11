# -*- coding: utf-8 -*-
"""
Data Loader for NeoZork Interactive ML Trading Strategy Development.

This module handles loading data from various sources including:
- CSV converted data (.parquet files)
- Raw parquet data from exchanges
- Indicators data (parquet, csv, json)
- Cleaned data with multiple timeframes
"""

import os
import sys
import time
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import glob
import json
import colorama
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.common.logger import print_info, print_warning, print_error, print_success, print_debug

class DataLoader:
    """
    Comprehensive data loader for multiple data sources.
    
    Features:
    - Load CSV converted data (.parquet)
    - Load raw parquet data from exchanges
    - Load indicators data (parquet, csv, json)
    - Load cleaned data with multiple timeframes
    - Progress tracking with ETA
    - Data validation and quality checks
    """
    
    def __init__(self):
        """Initialize the data loader."""
        self.project_root = PROJECT_ROOT
        self.data_root = self.project_root / "data"
        self.cache_root = self.data_root / "cache"
        self.raw_root = self.data_root / "raw_parquet"
        self.indicators_root = self.data_root / "indicators"
        self.cleaned_root = self.data_root / "cleaned_data"
        
        # Ensure data directories exist
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure all required data directories exist."""
        directories = [
            self.data_root,
            self.cache_root,
            self.raw_root,
            self.indicators_root,
            self.cleaned_root,
            self.cache_root / "csv_converted",
            self.indicators_root / "parquet",
            self.indicators_root / "csv",
            self.indicators_root / "json"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
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
    
    def _get_date_range_from_dataframe(self, df: pd.DataFrame) -> Tuple[str, str, List[str]]:
        """Extract date range and timeframes from a dataframe."""
        try:
            # First check if the index is datetime
            if isinstance(df.index, pd.DatetimeIndex):
                time_series = df.index
            else:
                # Look for time columns
                time_col = None
                for col in ['timestamp', 'Timestamp', 'time', 'Time', 'datetime', 'DateTime']:
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
    
    def load_csv_converted_data(self, symbol_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Load CSV converted data from parquet files with enhanced progress tracking.
        
        Args:
            symbol_filter: Optional filter for specific symbol (e.g., "eurusd")
            
        Returns:
            Dictionary containing loaded data and metadata
        """
        print_info("📁 Loading CSV converted data...")
        
        try:
            csv_dir = self.cache_root / "csv_converted"
            if not csv_dir.exists():
                print_warning(f"Directory {csv_dir} does not exist")
                return {"status": "error", "message": "CSV converted directory not found"}
            
            # Find parquet files
            pattern = "*.parquet"
            if symbol_filter:
                pattern = f"*{symbol_filter.upper()}_PERIOD_*.parquet"
            
            parquet_files = list(csv_dir.glob(pattern))
            
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
                
                # Show enhanced progress
                self._show_progress(f"Loading {file_path.name}", progress, eta_str, speed)
                
                try:
                    # Load parquet file
                    df = pd.read_parquet(file_path)
                    
                    # Extract symbol from filename
                    symbol = file_path.stem.replace("_", "").upper()
                    
                    # Calculate metadata
                    file_size = file_path.stat().st_size / (1024 * 1024)  # MB
                    total_size += file_size
                    total_rows += len(df)
                    
                    # Get time range using the improved method
                    start_date, end_date, timeframes = self._get_date_range_from_dataframe(df)
                    
                    loaded_data[symbol] = {
                        "data": df,
                        "file_path": str(file_path),
                        "size_mb": round(file_size, 2),
                        "rows": len(df),
                        "start_time": start_date,
                        "end_time": end_date,
                        "timeframes": timeframes,
                        "columns": list(df.columns)
                    }
                    
                except Exception as e:
                    print_error(f"Error loading {file_path.name}: {e}")
                    continue
            
            # Final progress display
            total_time = time.time() - start_time
            self._show_progress(f"Completed loading {total_files} files", 1.0, "", f"{total_files / total_time:.1f} files/s")
            
            print_success(f"✅ Loaded {len(loaded_data)} datasets")
            print_info(f"📊 Total size: {total_size:.2f} MB")
            print_info(f"📈 Total rows: {total_rows:,}")
            print_info(f"⏱️  Total time: {self._format_time(total_time)}")
            
            return {
                "status": "success",
                "data": loaded_data,
                "metadata": {
                    "total_files": len(loaded_data),
                    "total_size_mb": round(total_size, 2),
                    "total_rows": total_rows,
                    "symbols": list(loaded_data.keys())
                }
            }
            
        except Exception as e:
            print_error(f"Error loading CSV converted data: {e}")
            return {"status": "error", "message": str(e)}
    
    def load_raw_parquet_data(self, symbol_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Load raw parquet data from exchanges.
        
        Args:
            symbol_filter: Optional filter for specific symbol (e.g., "btcusdt")
            
        Returns:
            Dictionary containing loaded data and metadata
        """
        print_info("📊 Loading raw parquet data...")
        
        try:
            if not self.raw_root.exists():
                print_warning(f"Directory {self.raw_root} does not exist")
                return {"status": "error", "message": "Raw parquet directory not found"}
            
            # Find parquet files
            pattern = "*.parquet"
            if symbol_filter:
                pattern = f"*{symbol_filter.upper()}_PERIOD_*.parquet"
            
            parquet_files = list(self.raw_root.glob(pattern))
            
            if not parquet_files:
                print_warning(f"No parquet files found matching pattern: {pattern}")
                return {"status": "error", "message": f"No files found matching {pattern}"}
            
            loaded_data = {}
            total_size = 0
            total_rows = 0
            
            for i, file_path in enumerate(parquet_files):
                # Show progress
                progress = (i + 1) / len(parquet_files)
                self._show_progress(f"Loading {file_path.name}", progress)
                
                try:
                    # Load parquet file
                    df = pd.read_parquet(file_path)
                    
                    # Extract symbol from filename
                    symbol = file_path.stem.replace("_", "").upper()
                    
                    # Calculate metadata
                    file_size = file_path.stat().st_size / (1024 * 1024)  # MB
                    total_size += file_size
                    total_rows += len(df)
                    
                    # Get time range
                    if 'timestamp' in df.columns:
                        start_time = df['timestamp'].min()
                        end_time = df['timestamp'].max()
                        timeframes = df['timestamp'].dt.floor('H').value_counts().index.tolist()[:5]
                    elif 'Timestamp' in df.columns:
                        start_time = df['Timestamp'].min()
                        end_time = df['Timestamp'].max()
                        timeframes = df['Timestamp'].dt.floor('H').value_counts().index.tolist()[:5]
                    else:
                        start_time = "Unknown"
                        end_time = "Unknown"
                        timeframes = ["Unknown"]
                    
                    loaded_data[symbol] = {
                        "data": df,
                        "file_path": str(file_path),
                        "size_mb": round(file_size, 2),
                        "rows": len(df),
                        "start_time": start_time,
                        "end_time": end_time,
                        "timeframes": timeframes,
                        "columns": list(df.columns)
                    }
                    
                except Exception as e:
                    print_error(f"Error loading {file_path.name}: {e}")
                    continue
            
            print_success(f"✅ Loaded {len(loaded_data)} datasets")
            print_info(f"📊 Total size: {total_size:.2f} MB")
            print_info(f"📈 Total rows: {total_rows:,}")
            
            return {
                "status": "success",
                "data": loaded_data,
                "metadata": {
                    "total_files": len(loaded_data),
                    "total_size_mb": round(total_size, 2),
                    "total_rows": total_rows,
                    "symbols": list(loaded_data.keys())
                }
            }
            
        except Exception as e:
            print_error(f"Error loading raw parquet data: {e}")
            return {"status": "error", "message": str(e)}
    
    def load_indicators_data(self, symbol_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Load indicators data from parquet, csv, and json files.
        
        Args:
            symbol_filter: Optional filter for specific symbol (e.g., "aapl")
            
        Returns:
            Dictionary containing loaded data and metadata
        """
        print_info("📈 Loading indicators data...")
        
        try:
            if not self.indicators_root.exists():
                print_warning(f"Directory {self.indicators_root} does not exist")
                return {"status": "error", "message": "Indicators directory not found"}
            
            loaded_data = {}
            total_size = 0
            total_rows = 0
            file_count = 0
            
            # Load from different subdirectories
            subdirs = ["parquet", "csv", "json"]
            
            for subdir in subdirs:
                subdir_path = self.indicators_root / subdir
                if not subdir_path.exists():
                    continue
                
                # Find files based on subdirectory
                if subdir == "parquet":
                    pattern = "*.parquet"
                elif subdir == "csv":
                    pattern = "*.csv"
                else:  # json
                    pattern = "*.json"
                
                if symbol_filter:
                    pattern = f"*{symbol_filter.lower()}*{pattern[1:]}"
                
                files = list(subdir_path.glob(pattern))
                
                for i, file_path in enumerate(files):
                    file_count += 1
                    progress = file_count / (len(files) + 1)  # Approximate progress
                    self._show_progress(f"Loading {file_path.name}", progress)
                    
                    try:
                        # Load file based on extension
                        if file_path.suffix == '.parquet':
                            df = pd.read_parquet(file_path)
                        elif file_path.suffix == '.csv':
                            df = pd.read_csv(file_path)
                        elif file_path.suffix == '.json':
                            df = pd.read_json(file_path)
                        else:
                            continue
                        
                        # Extract symbol from filename
                        symbol = file_path.stem.replace("_", "").upper()
                        
                        # Calculate metadata
                        file_size = file_path.stat().st_size / (1024 * 1024)  # MB
                        total_size += file_size
                        total_rows += len(df)
                        
                        # Get time range
                        time_col = None
                        for col in ['timestamp', 'Timestamp', 'time', 'Time']:
                            if col in df.columns:
                                time_col = col
                                break
                        
                        if time_col:
                            start_time = df[time_col].min()
                            end_time = df[time_col].max()
                            timeframes = df[time_col].dt.floor('h').value_counts().index.tolist()[:5]
                        else:
                            start_time = "Unknown"
                            end_time = "Unknown"
                            timeframes = ["Unknown"]
                        
                        loaded_data[symbol] = {
                            "data": df,
                            "file_path": str(file_path),
                            "size_mb": round(file_size, 2),
                            "rows": len(df),
                            "start_time": start_time,
                            "end_time": end_time,
                            "timeframes": timeframes,
                            "columns": list(df.columns),
                            "file_type": subdir
                        }
                        
                    except Exception as e:
                        print_error(f"Error loading {file_path.name}: {e}")
                        continue
            
            if not loaded_data:
                print_warning("No indicator files found")
                return {"status": "error", "message": "No indicator files found"}
            
            print_success(f"✅ Loaded {len(loaded_data)} indicator datasets")
            print_info(f"📊 Total size: {total_size:.2f} MB")
            print_info(f"📈 Total rows: {total_rows:,}")
            
            return {
                "status": "success",
                "data": loaded_data,
                "metadata": {
                    "total_files": len(loaded_data),
                    "total_size_mb": round(total_size, 2),
                    "total_rows": total_rows,
                    "symbols": list(loaded_data.keys())
                }
            }
            
        except Exception as e:
            print_error(f"Error loading indicators data: {e}")
            return {"status": "error", "message": str(e)}
    
    def load_cleaned_data(self, symbol_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Load cleaned data with multiple timeframes.
        
        Args:
            symbol_filter: Optional filter for specific symbol (e.g., "eurusd")
            
        Returns:
            Dictionary containing loaded data and metadata
        """
        print_info("✨ Loading cleaned data...")
        
        try:
            if not self.cleaned_root.exists():
                print_warning(f"Directory {self.cleaned_root} does not exist")
                return {"status": "error", "message": "Cleaned data directory not found"}
            
            # Find parquet files
            pattern = "*.parquet"
            if symbol_filter:
                pattern = f"*{symbol_filter.upper()}_PERIOD_*.parquet"
            
            parquet_files = list(self.cleaned_root.glob(pattern))
            
            if not parquet_files:
                print_warning(f"No cleaned parquet files found matching pattern: {pattern}")
                return {"status": "error", "message": f"No files found matching {pattern}"}
            
            loaded_data = {}
            total_size = 0
            total_rows = 0
            
            for i, file_path in enumerate(parquet_files):
                # Show progress
                progress = (i + 1) / len(parquet_files)
                self._show_progress(f"Loading {file_path.name}", progress)
                
                try:
                    # Load parquet file
                    df = pd.read_parquet(file_path)
                    
                    # Extract symbol from filename
                    symbol = file_path.stem.replace("_", "").upper()
                    
                    # Calculate metadata
                    file_size = file_path.stat().st_size / (1024 * 1024)  # MB
                    total_size += file_size
                    total_rows += len(df)
                    
                    # Get time range
                    time_col = None
                    for col in ['timestamp', 'Timestamp', 'time', 'Time']:
                        if col in df.columns:
                            time_col = col
                            break
                    
                    if time_col:
                        start_time = df[time_col].min()
                        end_time = df[time_col].max()
                        timeframes = df[time_col].dt.floor('h').value_counts().index.tolist()[:5]
                    else:
                        start_time = "Unknown"
                        end_time = "Unknown"
                        timeframes = ["Unknown"]
                    
                    loaded_data[symbol] = {
                        "data": df,
                        "file_path": str(file_path),
                        "size_mb": round(file_size, 2),
                        "rows": len(df),
                        "start_time": start_time,
                        "end_time": end_time,
                        "timeframes": timeframes,
                        "columns": list(df.columns)
                    }
                    
                except Exception as e:
                    print_error(f"Error loading {file_path.name}: {e}")
                    continue
            
            print_success(f"✅ Loaded {len(loaded_data)} cleaned datasets")
            print_info(f"📊 Total size: {total_size:.2f} MB")
            print_info(f"📈 Total rows: {total_rows:,}")
            
            return {
                "status": "success",
                "data": loaded_data,
                "metadata": {
                    "total_files": len(loaded_data),
                    "total_size_mb": round(total_size, 2),
                    "total_rows": total_rows,
                    "symbols": list(loaded_data.keys())
                }
            }
            
        except Exception as e:
            print_error(f"Error loading cleaned data: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_available_data_sources(self) -> Dict[str, List[str]]:
        """
        Get list of available data sources and files.
        
        Returns:
            Dictionary with available data sources and files
        """
        sources = {
            "csv_converted": [],
            "raw_parquet": [],
            "indicators": [],
            "cleaned_data": []
        }
        
        # Check CSV converted
        csv_dir = self.cache_root / "csv_converted"
        if csv_dir.exists():
            sources["csv_converted"] = [f.name for f in csv_dir.glob("*.parquet")]
        
        # Check raw parquet
        if self.raw_root.exists():
            sources["raw_parquet"] = [f.name for f in self.raw_root.glob("*.parquet")]
        
        # Check indicators
        if self.indicators_root.exists():
            for subdir in ["parquet", "csv", "json"]:
                subdir_path = self.indicators_root / subdir
                if subdir_path.exists():
                    sources["indicators"].extend([f.name for f in subdir_path.glob(f"*.{subdir}")])
        
        # Check cleaned data
        if self.cleaned_root.exists():
            sources["cleaned_data"] = [f.name for f in self.cleaned_root.glob("*.parquet")]
        
        return sources
