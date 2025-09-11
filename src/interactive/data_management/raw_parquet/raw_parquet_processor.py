# -*- coding: utf-8 -*-
"""
Raw Parquet Processor for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive processing and standardization functionality
for raw parquet data from various exchanges.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
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

class RawParquetProcessor:
    """
    Comprehensive processor for raw parquet data from exchanges.
    
    Features:
    - Standardize column names and data types
    - Handle different exchange formats
    - Data cleaning and validation
    - Timeframe detection and standardization
    - Progress tracking with ETA
    """
    
    def __init__(self):
        """Initialize the raw parquet processor."""
        self.project_root = PROJECT_ROOT
        self.data_root = self.project_root / "data"
        self.raw_root = self.data_root / "raw_parquet"
        self.cleaned_root = self.data_root / "cleaned_data"
        
        # Exchange-specific column mappings
        self.exchange_mappings = {
            'binance': {
                'open_time': 'timestamp',
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'volume': 'volume',
                'close_time': 'close_timestamp',
                'quote_asset_volume': 'quote_volume',
                'number_of_trades': 'trades_count',
                'taker_buy_base_asset_volume': 'taker_buy_volume',
                'taker_buy_quote_asset_volume': 'taker_buy_quote_volume'
            },
            'bybit': {
                'start_time': 'timestamp',
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'volume': 'volume',
                'turnover': 'quote_volume'
            },
            'kraken': {
                'time': 'timestamp',
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'vwap': 'vwap',
                'volume': 'volume',
                'count': 'trades_count'
            },
            'polygon': {
                't': 'timestamp',
                'o': 'open',
                'h': 'high',
                'l': 'low',
                'c': 'close',
                'v': 'volume',
                'vw': 'vwap',
                'n': 'trades_count'
            }
        }
    
    def process_raw_data(self, loaded_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw parquet data with standardization and cleaning.
        
        Args:
            loaded_data: Dictionary containing loaded raw data
            
        Returns:
            Dictionary containing processed data
        """
        print_info("🔄 Processing raw parquet data...")
        
        try:
            processed_data = {}
            total_files = len(loaded_data)
            
            # Progress tracking variables
            start_time = time.time()
            
            for i, (data_key, data_info) in enumerate(loaded_data.items()):
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
                self._show_progress(f"Processing {data_key}", progress, eta_str, speed)
                
                try:
                    # Process individual data
                    processed_info = self._process_single_data(data_info)
                    if processed_info:
                        processed_data[data_key] = processed_info
                    
                except Exception as e:
                    print_error(f"Error processing {data_key}: {e}")
                    continue
            
            # Final progress display
            total_time = time.time() - start_time
            self._show_progress(f"Completed processing {total_files} files", 1.0, "", f"{total_files / total_time:.1f} files/s")
            
            return {
                "status": "success",
                "data": processed_data,
                "metadata": {
                    "total_processed": len(processed_data),
                    "processing_time": total_time
                }
            }
            
        except Exception as e:
            print_error(f"Error processing raw data: {e}")
            return {"status": "error", "message": str(e)}
    
    def _process_single_data(self, data_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single data entry."""
        try:
            df = data_info["data"].copy()
            source = data_info.get("source", "unknown")
            symbol = data_info.get("symbol", "unknown")
            timeframe = data_info.get("timeframe", "unknown")
            
            # Standardize column names based on source
            df = self._standardize_columns(df, source)
            
            # Standardize data types
            df = self._standardize_data_types(df)
            
            # Clean data
            df = self._clean_data(df)
            
            # Detect and standardize timeframe
            detected_timeframe = self._detect_timeframe(df)
            if detected_timeframe:
                timeframe = detected_timeframe
            
            # Set timestamp as index
            df = self._set_timestamp_index(df)
            
            # Sort by timestamp
            df = df.sort_index()
            
            # Add metadata columns
            df['symbol'] = symbol.upper()
            df['timeframe'] = timeframe
            df['source'] = source.lower()
            
            # Create processed data info
            processed_info = {
                "file_path": data_info["file_path"],
                "source": source,
                "symbol": symbol,
                "timeframe": timeframe,
                "data": df,
                "size_mb": data_info["size_mb"],
                "rows": len(df),
                "start_time": str(df.index.min()) if not df.empty else "No data",
                "end_time": str(df.index.max()) if not df.empty else "No data",
                "columns": list(df.columns)
            }
            
            return processed_info
            
        except Exception as e:
            print_error(f"Error processing single data: {e}")
            return None
    
    def _standardize_columns(self, df: pd.DataFrame, source: str) -> pd.DataFrame:
        """Standardize column names based on source."""
        try:
            # Get mapping for this source
            mapping = self.exchange_mappings.get(source.lower(), {})
            
            # Apply column mapping
            df = df.rename(columns=mapping)
            
            # Ensure standard columns exist
            standard_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            
            # Check if we have the required columns
            missing_columns = []
            for col in standard_columns:
                if col not in df.columns:
                    missing_columns.append(col)
            
            if missing_columns:
                print_warning(f"Missing standard columns for {source}: {missing_columns}")
            
            return df
            
        except Exception as e:
            print_error(f"Error standardizing columns: {e}")
            return df
    
    def _standardize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize data types for OHLCV data."""
        try:
            # Convert timestamp to datetime if it exists
            if 'timestamp' in df.columns:
                if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                    # Try different timestamp formats
                    try:
                        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                    except:
                        try:
                            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
                        except:
                            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            
            # Convert OHLCV to numeric
            ohlcv_columns = ['open', 'high', 'low', 'close', 'volume']
            for col in ohlcv_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Convert other numeric columns
            numeric_columns = ['quote_volume', 'trades_count', 'taker_buy_volume', 'taker_buy_quote_volume', 'vwap']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            return df
            
        except Exception as e:
            print_error(f"Error standardizing data types: {e}")
            return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate data."""
        try:
            # Remove rows with all NaN values
            df = df.dropna(how='all')
            
            # Remove rows with NaN in critical columns
            critical_columns = ['open', 'high', 'low', 'close']
            existing_critical = [col for col in critical_columns if col in df.columns]
            if existing_critical:
                df = df.dropna(subset=existing_critical)
            
            # Validate OHLC data
            if all(col in df.columns for col in ['open', 'high', 'low', 'close']):
                # High should be >= max(open, close)
                df = df[df['high'] >= df[['open', 'close']].max(axis=1)]
                
                # Low should be <= min(open, close)
                df = df[df['low'] <= df[['open', 'close']].min(axis=1)]
                
                # Remove rows where high < low
                df = df[df['high'] >= df['low']]
            
            # Remove duplicate timestamps
            if 'timestamp' in df.columns:
                df = df.drop_duplicates(subset=['timestamp'], keep='first')
            
            # Sort by timestamp
            if 'timestamp' in df.columns:
                df = df.sort_values('timestamp')
            
            return df
            
        except Exception as e:
            print_error(f"Error cleaning data: {e}")
            return df
    
    def _detect_timeframe(self, df: pd.DataFrame) -> Optional[str]:
        """Detect timeframe from data."""
        try:
            if 'timestamp' not in df.columns or df.empty:
                return None
            
            # Convert to datetime if needed
            if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            
            # Set as index for resampling
            df_temp = df.set_index('timestamp')
            
            # Get time differences
            time_diffs = df_temp.index.to_series().diff().dropna()
            
            if time_diffs.empty:
                return None
            
            # Get most common time difference
            most_common_diff = time_diffs.mode().iloc[0] if not time_diffs.mode().empty else time_diffs.iloc[0]
            
            # Convert to minutes
            diff_minutes = most_common_diff.total_seconds() / 60
            
            # Map to timeframe
            timeframe_mapping = {
                1: 'M1',
                5: 'M5',
                15: 'M15',
                30: 'M30',
                60: 'H1',
                240: 'H4',
                1440: 'D1',
                10080: 'W1',
                43200: 'MN1'
            }
            
            # Find closest timeframe
            closest_timeframe = min(timeframe_mapping.keys(), key=lambda x: abs(x - diff_minutes))
            
            return timeframe_mapping[closest_timeframe]
            
        except Exception as e:
            print_error(f"Error detecting timeframe: {e}")
            return None
    
    def _set_timestamp_index(self, df: pd.DataFrame) -> pd.DataFrame:
        """Set timestamp as index."""
        try:
            if 'timestamp' in df.columns:
                # Convert to datetime if needed
                if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                
                # Set as index
                df = df.set_index('timestamp')
            
            return df
            
        except Exception as e:
            print_error(f"Error setting timestamp index: {e}")
            return df
    
    def process_symbol_data(self, symbol_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data for a specific symbol.
        
        Args:
            symbol_data: Dictionary containing symbol data
            
        Returns:
            Dictionary containing processed symbol data
        """
        print_info(f"🔄 Processing {symbol_data['metadata']['symbol']} data...")
        
        try:
            processed_data = {}
            
            for timeframe, data_info in symbol_data['data'].items():
                try:
                    # Process individual timeframe data
                    processed_info = self._process_single_data(data_info)
                    if processed_info:
                        processed_data[timeframe] = processed_info
                    
                except Exception as e:
                    print_error(f"Error processing {timeframe}: {e}")
                    continue
            
            if not processed_data:
                return {"status": "error", "message": "No data processed successfully"}
            
            # Prepare metadata
            metadata = symbol_data['metadata'].copy()
            metadata['processed_timeframes'] = list(processed_data.keys())
            metadata['processed_count'] = len(processed_data)
            
            return {
                "status": "success",
                "data": processed_data,
                "metadata": metadata
            }
            
        except Exception as e:
            print_error(f"Error processing symbol data: {e}")
            return {"status": "error", "message": str(e)}
    
    def _show_progress(self, message: str, progress: float = 0.0, eta: str = "", speed: str = ""):
        """Show progress with ETA, percentage, and speed in a single line."""
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        percentage = int(progress * 100)
        
        # Create progress display
        progress_display = f"{Fore.CYAN}🔄 {message}"
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
