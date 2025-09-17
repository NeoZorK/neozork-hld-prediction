# -*- coding: utf-8 -*-
"""
Raw Parquet MTF Creator for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive functionality for creating Multi-Timeframe (MTF)
structures from raw parquet data for machine learning applications.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import time
import json
from datetime import datetime
import colorama
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.common.logger import print_info, print_warning, print_error, print_success, print_debug

class RawParquetMTFCreator:
    """
    Comprehensive MTF creator for raw parquet data from exchanges.
    
    Features:
    - Create MTF structures from processed raw data
    - Support for multiple timeframes
    - Cross-timeframe feature engineering
    - ML-optimized data structures
    - Progress tracking with ETA
    """
    
    def __init__(self):
        """Initialize the raw parquet MTF creator."""
        self.project_root = PROJECT_ROOT
        self.data_root = self.project_root / "data"
        self.cleaned_root = self.data_root / "cleaned_data"
        self.mtf_root = self.cleaned_root / "mtf_structures"
        
        # Ensure MTF directory exists
        self.mtf_root.mkdir(parents=True, exist_ok=True)
    
    def create_mtf_structure(self, processed_data: Dict[str, Any], symbol: str, main_timeframe: str, source: str = "raw_parquet") -> Dict[str, Any]:
        """
        Create MTF structure from processed raw parquet data.
        
        Args:
            processed_data: Dictionary containing processed data
            symbol: Symbol name (e.g., "BTCUSDT")
            main_timeframe: Main timeframe (e.g., "M1")
            source: Data source (e.g., "raw_parquet")
            
        Returns:
            Dictionary containing MTF structure
        """
        print_info(f"🔧 Creating MTF structure for {symbol} ({source})...")
        
        try:
            # Group data by timeframe
            timeframe_data = {}
            for data_key, data_info in processed_data.items():
                timeframe = data_info.get("timeframe", "unknown")
                if timeframe != "unknown":
                    timeframe_data[timeframe] = data_info["data"]
            
            if not timeframe_data:
                return {"status": "error", "message": "No valid timeframe data found"}
            
            # Sort timeframes by priority
            timeframe_priority = {'M1': 1, 'M5': 2, 'M15': 3, 'M30': 4, 'H1': 5, 'H4': 6, 'D1': 7, 'W1': 8, 'MN1': 9}
            sorted_timeframes = sorted(timeframe_data.keys(), key=lambda x: timeframe_priority.get(x, 999))
            
            print_info(f"📊 Available timeframes: {', '.join(sorted_timeframes)}")
            print_info(f"🎯 Main timeframe: {main_timeframe}")
            
            # Create MTF structure
            mtf_data = {
                'symbol': symbol.upper(),
                'source': source,
                'main_timeframe': main_timeframe,
                'timeframes': sorted_timeframes,
                'main_data': timeframe_data.get(main_timeframe, pd.DataFrame()),
                'timeframe_data': timeframe_data,
                'metadata': {
                    'created_at': pd.Timestamp.now().isoformat(),
                    'total_rows': sum(len(df) for df in timeframe_data.values()),
                    'timeframe_counts': {tf: len(df) for tf, df in timeframe_data.items()},
                    'source': source
                }
            }
            
            # Add cross-timeframe features if multiple timeframes available
            if len(timeframe_data) > 1:
                print_info("🔧 Creating cross-timeframe features...")
                mtf_data['cross_timeframe_features'] = self._create_cross_timeframe_features(
                    timeframe_data, main_timeframe)
            
            # Save MTF structure
            self._save_mtf_structure(symbol, mtf_data, source)
            
            return {
                "status": "success",
                "mtf_data": mtf_data,
                "message": f"MTF structure created successfully for {symbol}"
            }
            
        except Exception as e:
            print_error(f"Error creating MTF structure: {e}")
            return {"status": "error", "message": str(e)}
    
    def _create_cross_timeframe_features(self, timeframe_data: Dict[str, pd.DataFrame], main_timeframe: str) -> Dict[str, pd.DataFrame]:
        """Create cross-timeframe features for ML."""
        try:
            cross_features = {}
            main_df = timeframe_data[main_timeframe]
            
            # Get timeframes to process (exclude main timeframe)
            timeframes_to_process = [tf for tf in timeframe_data.keys() if tf != main_timeframe]
            
            for tf in timeframes_to_process:
                df = timeframe_data[tf]
                
                # Resample to main timeframe frequency
                resampled = df.resample('1min').ffill()  # Forward fill to 1-minute frequency
                
                # Align with main timeframe
                aligned = resampled.reindex(main_df.index, method='ffill')
                
                # Add prefix to column names to avoid conflicts
                aligned_renamed = aligned.add_prefix(f"{tf}_")
                
                cross_features[tf] = aligned_renamed
            
            return cross_features
            
        except Exception as e:
            print_error(f"Error creating cross-timeframe features: {e}")
            return {}
    
    def _save_mtf_structure(self, symbol: str, mtf_data: Dict[str, Any], source: str):
        """Save MTF structure to disk."""
        try:
            # Create source directory
            source_dir = self.mtf_root / source
            source_dir.mkdir(parents=True, exist_ok=True)
            
            # Create symbol directory
            symbol_dir = source_dir / symbol.lower()
            symbol_dir.mkdir(parents=True, exist_ok=True)
            
            # Save main data
            main_file = symbol_dir / f"{symbol.lower()}_main_{mtf_data['main_timeframe'].lower()}.parquet"
            mtf_data['main_data'].to_parquet(main_file)
            
            # Save cross-timeframe features
            if 'cross_timeframe_features' in mtf_data:
                cross_dir = symbol_dir / "cross_timeframes"
                cross_dir.mkdir(exist_ok=True)
                
                for tf, cross_df in mtf_data['cross_timeframe_features'].items():
                    cross_file = cross_dir / f"{symbol.lower()}_{tf.lower()}_cross.parquet"
                    cross_df.to_parquet(cross_file)
            
            # Save metadata
            metadata_file = symbol_dir / "mtf_metadata.json"
            metadata = mtf_data['metadata'].copy()
            metadata.update({
                'symbol': mtf_data['symbol'],
                'source': mtf_data['source'],
                'main_timeframe': mtf_data['main_timeframe'],
                'timeframes': mtf_data['timeframes'],
                'main_data_shape': list(mtf_data['main_data'].shape),
                'cross_timeframes': list(mtf_data.get('cross_timeframe_features', {}).keys())
            })
            
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            print_success(f"✅ MTF structure saved to {symbol_dir}")
            
        except Exception as e:
            print_error(f"Error saving MTF structure: {e}")
    
    def create_mtf_from_symbol_data(self, symbol_data: Dict[str, Any], main_timeframe: str) -> Dict[str, Any]:
        """
        Create MTF structure from symbol data.
        
        Args:
            symbol_data: Dictionary containing symbol data
            main_timeframe: Main timeframe (e.g., "M1")
            
        Returns:
            Dictionary containing MTF structure
        """
        try:
            symbol = symbol_data['metadata']['symbol']
            source = symbol_data['metadata'].get('source', 'raw_parquet')
            
            # Extract processed data
            processed_data = {}
            for timeframe, data_info in symbol_data['data'].items():
                processed_data[timeframe] = {
                    "data": data_info["data"],
                    "timeframe": data_info["timeframe"],
                    "source": data_info["source"],
                    "symbol": data_info["symbol"]
                }
            
            # Create MTF structure
            return self.create_mtf_structure(processed_data, symbol, main_timeframe, source)
            
        except Exception as e:
            print_error(f"Error creating MTF from symbol data: {e}")
            return {"status": "error", "message": str(e)}
    
    def create_mtf_from_processed_data(self, processed_data: Dict[str, Any], symbol: str, main_timeframe: str, source: str = "raw_parquet") -> Dict[str, Any]:
        """
        Create MTF structure from processed data with progress tracking.
        
        Args:
            processed_data: Dictionary containing processed data
            symbol: Symbol name
            main_timeframe: Main timeframe
            source: Data source
            
        Returns:
            Dictionary containing MTF structure
        """
        print_info(f"🔧 Creating MTF structure for {symbol} ({source})...")
        
        try:
            # Group data by timeframe
            timeframe_data = {}
            for data_key, data_info in processed_data.items():
                timeframe = data_info.get("timeframe", "unknown")
                if timeframe != "unknown":
                    timeframe_data[timeframe] = data_info["data"]
            
            if not timeframe_data:
                return {"status": "error", "message": "No valid timeframe data found"}
            
            # Sort timeframes by priority
            timeframe_priority = {'M1': 1, 'M5': 2, 'M15': 3, 'M30': 4, 'H1': 5, 'H4': 6, 'D1': 7, 'W1': 8, 'MN1': 9}
            sorted_timeframes = sorted(timeframe_data.keys(), key=lambda x: timeframe_priority.get(x, 999))
            
            print_info(f"📊 Available timeframes: {', '.join(sorted_timeframes)}")
            print_info(f"🎯 Main timeframe: {main_timeframe}")
            
            # Create MTF structure with progress tracking
            mtf_data = self._create_mtf_structure_with_progress(
                timeframe_data, symbol, main_timeframe, source)
            
            return {
                "status": "success",
                "mtf_data": mtf_data,
                "message": f"MTF structure created successfully for {symbol}"
            }
            
        except Exception as e:
            print_error(f"Error creating MTF from processed data: {e}")
            return {"status": "error", "message": str(e)}
    
    def _create_mtf_structure_with_progress(self, timeframe_data: Dict[str, pd.DataFrame], symbol: str, main_timeframe: str, source: str) -> Dict[str, Any]:
        """Create MTF structure with progress tracking."""
        try:
            # Calculate total steps for progress tracking
            total_steps = 3  # Main data + cross features + metadata
            if len(timeframe_data) > 1:
                total_steps += len(timeframe_data) - 1  # Additional cross-timeframe features
            
            current_step = 0
            start_time = time.time()
            
            # Step 1: Create main MTF data structure
            current_step += 1
            progress = current_step / total_steps
            self._show_mtf_progress("Creating main data structure", progress, start_time)
            
            mtf_data = {
                'symbol': symbol.upper(),
                'source': source,
                'main_timeframe': main_timeframe,
                'timeframes': list(timeframe_data.keys()),
                'main_data': timeframe_data.get(main_timeframe, pd.DataFrame()),
                'timeframe_data': timeframe_data,
                'metadata': {
                    'created_at': pd.Timestamp.now().isoformat(),
                    'total_rows': sum(len(df) for df in timeframe_data.values()),
                    'timeframe_counts': {tf: len(df) for tf, df in timeframe_data.items()},
                    'source': source
                }
            }
            
            # Step 2: Add cross-timeframe features if multiple timeframes available
            if len(timeframe_data) > 1:
                current_step += 1
                progress = current_step / total_steps
                self._show_mtf_progress("Creating cross-timeframe features", progress, start_time)
                
                mtf_data['cross_timeframe_features'] = self._create_cross_timeframe_features_with_progress(
                    timeframe_data, main_timeframe, start_time, current_step, total_steps)
            
            # Step 3: Finalize metadata
            current_step += 1
            progress = current_step / total_steps
            self._show_mtf_progress("Finalizing MTF structure", progress, start_time)
            
            # Final progress display
            total_time = time.time() - start_time
            self._show_mtf_progress("MTF structure created successfully", 1.0, start_time)
            
            return mtf_data
            
        except Exception as e:
            print_error(f"Error creating MTF structure with progress: {e}")
            return {'error': str(e)}
    
    def _create_cross_timeframe_features_with_progress(self, timeframe_data: Dict[str, pd.DataFrame], main_timeframe: str, start_time: float, current_step: int, total_steps: int) -> Dict[str, pd.DataFrame]:
        """Create cross-timeframe features with progress tracking."""
        try:
            main_df = timeframe_data[main_timeframe]
            cross_features = {}
            
            # Get timeframes to process
            timeframes_to_process = [tf for tf in timeframe_data.keys() if tf != main_timeframe]
            
            # Add features from higher timeframes
            for i, tf in enumerate(timeframes_to_process):
                # Update progress
                step_progress = (current_step + i) / total_steps
                self._show_mtf_progress(f"Processing {tf} cross-features", step_progress, start_time)
                
                df = timeframe_data[tf]
                # Resample to main timeframe frequency
                resampled = df.resample('1min').ffill()  # Forward fill to 1-minute frequency
                
                # Align with main timeframe
                aligned = resampled.reindex(main_df.index, method='ffill')
                
                # Add prefix to column names to avoid conflicts
                aligned_renamed = aligned.add_prefix(f"{tf}_")
                
                cross_features[tf] = aligned_renamed
            
            return cross_features
            
        except Exception as e:
            print_error(f"Error creating cross-timeframe features with progress: {e}")
            return {}
    
    def _show_mtf_progress(self, message: str, progress: float, start_time: float):
        """Show MTF progress with ETA and percentage."""
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
            speed = f"{progress / elapsed_time:.1f} steps/s"
        else:
            speed = "Starting..."
        
        # Create progress display
        progress_display = f"{Fore.CYAN}🔧 {message}"
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
