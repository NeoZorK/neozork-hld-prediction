# -*- coding: utf-8 -*-
"""
Indicators Data Loader for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive loading functionality for indicators data
from multiple formats (parquet, json, csv) with progress tracking and error handling.
"""

import os
import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import time
import psutil
import colorama
from colorama import Fore, Style

from src.common.logger import print_error, print_info, print_success, print_warning


class IndicatorsLoader:
    """
    Loader for indicators data from multiple formats.
    
    Provides comprehensive loading functionality with progress tracking,
    memory monitoring, and error handling for parquet, json, and csv formats.
    """
    
    def __init__(self):
        """Initialize the indicators loader."""
        self.indicators_path = Path("data/indicators")
        self.supported_formats = ['.parquet', '.json', '.csv']
        self.loaded_data = {}
        
    def load_indicators_data(self, indicator_filter: Optional[str] = None, 
                           format_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Load indicators data with optional filtering.
        
        Args:
            indicator_filter: Filter by indicator name (e.g., 'RSI', 'MACD')
            format_filter: Filter by format ('parquet', 'json', 'csv')
            
        Returns:
            Dict containing loaded data with status, metadata, and data
        """
        try:
            print_info("🔄 Loading indicators data...")
            
            # Get initial memory usage
            process = psutil.Process()
            initial_memory = process.memory_info().rss / (1024 * 1024)  # MB
            
            start_time = time.time()
            
            # Find all indicators files
            files_to_load = self._find_files_to_load(indicator_filter, format_filter)
            
            if not files_to_load:
                return {
                    "status": "error",
                    "message": "No indicators files found matching criteria"
                }
            
            print_info(f"📊 Found {len(files_to_load)} files to load")
            
            # Load files with progress tracking
            loaded_data = {}
            total_files = len(files_to_load)
            
            for i, file_path in enumerate(files_to_load):
                progress = (i + 1) / total_files
                self._show_loading_progress(f"Loading {file_path.name}", progress, start_time)
                
                # Load individual file
                file_data = self._load_single_file(file_path)
                if file_data:
                    loaded_data[file_path.name] = file_data
            
            # Calculate final statistics
            final_memory = process.memory_info().rss / (1024 * 1024)  # MB
            memory_used = final_memory - initial_memory
            loading_time = time.time() - start_time
            
            # Create metadata
            metadata = self._create_metadata(loaded_data, memory_used, loading_time)
            
            print_success(f"✅ Loaded {len(loaded_data)} indicators files in {loading_time:.2f}s")
            
            return {
                "status": "success",
                "data": loaded_data,
                "metadata": metadata,
                "memory_used": memory_used,
                "loading_time": loading_time
            }
            
        except Exception as e:
            print_error(f"Error loading indicators data: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def load_indicator_by_name(self, indicator_name: str, 
                             preferred_format: str = 'parquet') -> Dict[str, Any]:
        """
        Load specific indicator by name with format preference.
        
        Args:
            indicator_name: Name of the indicator to load
            preferred_format: Preferred format ('parquet', 'json', 'csv')
            
        Returns:
            Dict containing loaded indicator data
        """
        try:
            print_info(f"🔄 Loading indicator: {indicator_name}")
            
            # Find files for this indicator
            files = self._find_indicator_files(indicator_name)
            
            if not files:
                return {
                    "status": "error",
                    "message": f"No files found for indicator: {indicator_name}"
                }
            
            # Sort by format preference
            format_priority = {preferred_format: 1, 'parquet': 2, 'json': 3, 'csv': 4}
            files.sort(key=lambda x: format_priority.get(x.suffix[1:], 999))
            
            # Load the first (preferred) file
            file_path = files[0]
            file_data = self._load_single_file(file_path)
            
            if not file_data:
                return {
                    "status": "error",
                    "message": f"Failed to load file: {file_path}"
                }
            
            print_success(f"✅ Loaded {indicator_name} from {file_path.name}")
            
            return {
                "status": "success",
                "indicator_name": indicator_name,
                "file_path": str(file_path),
                "data": file_data,
                "format": file_path.suffix[1:]
            }
            
        except Exception as e:
            print_error(f"Error loading indicator {indicator_name}: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def load_indicators_by_format(self, format_name: str) -> Dict[str, Any]:
        """
        Load all indicators from specific format.
        
        Args:
            format_name: Format to load ('parquet', 'json', 'csv')
            
        Returns:
            Dict containing loaded indicators data
        """
        try:
            print_info(f"🔄 Loading all {format_name} indicators...")
            
            # Find files for this format
            files = self._find_files_by_format(format_name)
            
            if not files:
                return {
                    "status": "error",
                    "message": f"No {format_name} files found"
                }
            
            # Load all files
            result = self.load_indicators_data(format_filter=format_name)
            
            return result
            
        except Exception as e:
            print_error(f"Error loading {format_name} indicators: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _find_files_to_load(self, indicator_filter: Optional[str] = None,
                          format_filter: Optional[str] = None) -> List[Path]:
        """Find files to load based on filters."""
        files_to_load = []
        
        try:
            # Get all files
            all_files = []
            for format_ext in self.supported_formats:
                pattern = f"**/*{format_ext}"
                files = list(self.indicators_path.glob(pattern))
                all_files.extend(files)
            
            # Apply filters
            for file_path in all_files:
                # Format filter
                if format_filter:
                    file_format = file_path.suffix[1:].lower()
                    if file_format != format_filter.lower():
                        continue
                
                # Indicator filter
                if indicator_filter:
                    indicator_name = self._extract_indicator_name(file_path.name)
                    if indicator_name.lower() != indicator_filter.lower():
                        continue
                
                files_to_load.append(file_path)
            
            return files_to_load
            
        except Exception as e:
            print_error(f"Error finding files to load: {e}")
            return []
    
    def _find_indicator_files(self, indicator_name: str) -> List[Path]:
        """Find all files for a specific indicator."""
        files = []
        
        try:
            for format_ext in self.supported_formats:
                pattern = f"**/*{format_ext}"
                all_files = list(self.indicators_path.glob(pattern))
                
                for file_path in all_files:
                    file_indicator = self._extract_indicator_name(file_path.name)
                    if file_indicator.lower() == indicator_name.lower():
                        files.append(file_path)
            
            return files
            
        except Exception as e:
            print_error(f"Error finding files for indicator {indicator_name}: {e}")
            return []
    
    def _find_files_by_format(self, format_name: str) -> List[Path]:
        """Find all files for a specific format."""
        files = []
        
        try:
            format_ext = f".{format_name.lower()}"
            pattern = f"**/*{format_ext}"
            files = list(self.indicators_path.glob(pattern))
            
            return files
            
        except Exception as e:
            print_error(f"Error finding {format_name} files: {e}")
            return []
    
    def _load_single_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Load a single indicators file."""
        try:
            file_format = file_path.suffix.lower()
            
            if file_format == '.parquet':
                return self._load_parquet_file(file_path)
            elif file_format == '.json':
                return self._load_json_file(file_path)
            elif file_format == '.csv':
                return self._load_csv_file(file_path)
            else:
                print_warning(f"Unsupported format: {file_format}")
                return None
                
        except Exception as e:
            print_error(f"Error loading file {file_path}: {e}")
            return None
    
    def _load_parquet_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Load parquet file."""
        try:
            df = pd.read_parquet(file_path)
            
            return {
                'data': df,
                'format': 'parquet',
                'rows': len(df),
                'columns': list(df.columns),
                'file_path': str(file_path),
                'indicator': self._extract_indicator_name(file_path.name)
            }
            
        except Exception as e:
            print_error(f"Error loading parquet file {file_path}: {e}")
            return None
    
    def _load_json_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Load JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Convert to DataFrame if it's a list of records
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                df = pd.DataFrame(data)
            else:
                # For other JSON structures, create a simple DataFrame
                df = pd.DataFrame([data] if isinstance(data, dict) else data)
            
            return {
                'data': df,
                'format': 'json',
                'rows': len(df),
                'columns': list(df.columns),
                'file_path': str(file_path),
                'indicator': self._extract_indicator_name(file_path.name),
                'raw_data': data  # Keep original JSON data
            }
            
        except Exception as e:
            print_error(f"Error loading JSON file {file_path}: {e}")
            return None
    
    def _load_csv_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Load CSV file."""
        try:
            df = pd.read_csv(file_path)
            
            return {
                'data': df,
                'format': 'csv',
                'rows': len(df),
                'columns': list(df.columns),
                'file_path': str(file_path),
                'indicator': self._extract_indicator_name(file_path.name)
            }
            
        except Exception as e:
            print_error(f"Error loading CSV file {file_path}: {e}")
            return None
    
    def _extract_indicator_name(self, filename: str) -> str:
        """Extract indicator name from filename."""
        try:
            # Remove extension
            name = filename.split('.')[0]
            
            # Common patterns for indicator names
            if '_' in name:
                parts = name.split('_')
                if len(parts) >= 2:
                    # Check if first part looks like an indicator
                    indicator_candidates = ['rsi', 'macd', 'sma', 'ema', 'bb', 'stoch', 'adx', 'cci', 'williams']
                    if parts[0].lower() in indicator_candidates:
                        return parts[0].upper()
            
            return name.upper()
            
        except Exception as e:
            print_error(f"Error extracting indicator name from {filename}: {e}")
            return filename.upper()
    
    def _create_metadata(self, loaded_data: Dict[str, Any], 
                        memory_used: float, loading_time: float) -> Dict[str, Any]:
        """Create metadata for loaded data."""
        try:
            total_files = len(loaded_data)
            total_rows = sum(data['rows'] for data in loaded_data.values())
            
            # Get unique indicators
            indicators = list(set(data['indicator'] for data in loaded_data.values()))
            
            # Get unique formats
            formats = list(set(data['format'] for data in loaded_data.values()))
            
            # Calculate total size
            total_size = 0
            for file_path in [Path(data['file_path']) for data in loaded_data.values()]:
                if file_path.exists():
                    total_size += file_path.stat().st_size
            total_size_mb = total_size / (1024 * 1024)
            
            return {
                'total_files': total_files,
                'total_rows': total_rows,
                'total_size_mb': round(total_size_mb, 2),
                'indicators': indicators,
                'formats': formats,
                'memory_used_mb': round(memory_used, 2),
                'loading_time_seconds': round(loading_time, 2)
            }
            
        except Exception as e:
            print_error(f"Error creating metadata: {e}")
            return {}
    
    def _show_loading_progress(self, message: str, progress: float, start_time: float):
        """Show loading progress with ETA and percentage."""
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        percentage = int(progress * 100)
        
        # Calculate ETA
        current_time = time.time()
        elapsed_time = current_time - start_time
        if progress > 0:
            eta_seconds = (elapsed_time / progress) - elapsed_time
            eta_str = self._format_time(eta_seconds)
        else:
            eta_str = "Calculating..."
        
        # Calculate speed
        if elapsed_time > 0:
            speed = f"{progress / elapsed_time:.1f} files/s"
        else:
            speed = "Starting..."
        
        # Create progress display
        progress_display = f"{Fore.CYAN}🔄 {message}"
        bar_display = f"{Fore.GREEN}[{bar}]{Fore.CYAN}"
        percentage_display = f"{Fore.YELLOW}{percentage:3d}%"
        
        # Add ETA and speed
        extra_info = f" {Fore.MAGENTA}ETA: {eta_str} {Fore.BLUE}Speed: {speed}"
        
        # Combine all parts
        full_display = f"\r{progress_display} {bar_display} {percentage_display}{extra_info}{Style.RESET_ALL}"
        
        # Ensure the line is long enough to clear previous content
        terminal_width = 120
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
