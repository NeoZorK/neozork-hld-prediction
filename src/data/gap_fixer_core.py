# File: src/data/gap_fixer_core.py
# -*- coding: utf-8 -*-

"""
Core gap fixing functionality for time series data.
Provides the main GapFixer class with gap detection and fixing algorithms.
All comments are in English.
"""

import time
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import gc

import pandas as pd
import numpy as np
from tqdm import tqdm
import psutil

from .gap_fixer_algorithms import GapFixingAlgorithms
from .gap_fixer_utils import GapFixingUtils

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)


class GapFixer:
    """
    Advanced gap fixer for time series data with multiple algorithms.
    
    This class provides sophisticated methods for detecting and fixing
    time series gaps using various interpolation and forecasting techniques.
    """
    
    def __init__(self, memory_limit_mb: int = 6144):
        """
        Initialize the gap fixer.
        
        Args:
            memory_limit_mb: Memory limit in MB for processing
        """
        self.memory_limit_mb = memory_limit_mb
        self.supported_formats = ['.parquet', '.csv', '.json']
        
        # Initialize algorithm and utility modules
        self.algorithms = GapFixingAlgorithms()
        self.utils = GapFixingUtils()
        
        print(f"🔧 GapFixer initialized with memory limit: {memory_limit_mb}MB")
    
    def fix_file_gaps(self, file_path: Path, algorithm: str = 'auto', 
                      show_progress: bool = True) -> Tuple[bool, Dict]:
        """
        Fix gaps in a single file.
        
        Args:
            file_path: Path to the file to fix
            algorithm: Algorithm to use for gap fixing
            show_progress: Whether to show progress bar
            
        Returns:
            Tuple of (success, results_dict)
        """
        try:
            print(f"   📁 Loading file: {file_path.name}")
            print(f"   📊 File size: {file_path.stat().st_size / (1024*1024):.1f} MB")
            
            # Load file
            df = self.utils.load_file(file_path)
            if df is None:
                return False, {'error': f'Failed to load file: {file_path}'}
            
            print(f"   📊 Loaded data shape: {df.shape}")
            print(f"   💾 Memory usage after loading: {self.utils.get_memory_usage():.1f} MB")
            
            # Check if timestamp column exists or if we have a DatetimeIndex
            timestamp_col = self.utils.find_timestamp_column(df)
            
            if timestamp_col is None and not isinstance(df.index, pd.DatetimeIndex):
                return False, {'error': 'No timestamp column found'}
            
            # Handle DatetimeIndex case
            if isinstance(df.index, pd.DatetimeIndex):
                print(f"   📅 Converting DatetimeIndex to column for gap analysis...")
                df = self.utils.convert_datetime_index_to_column(df)
                timestamp_col = df.columns[0]  # First column after reset_index
            
            # Convert timestamp to datetime if needed
            if timestamp_col and not pd.api.types.is_datetime64_any_dtype(df[timestamp_col]):
                df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')
            
            print(f"   🔍 Detecting gaps...")
            # Detect gaps
            gap_info = self.utils.detect_gaps(df, timestamp_col)
            
            if not gap_info['has_gaps']:
                print(f"   ✅ No gaps detected")
                return True, {
                    'success': True,
                    'message': 'No gaps found', 
                    'gaps_fixed': 0,
                    'algorithm_used': algorithm,
                    'processing_time': 0.0,
                    'original_gaps': 0,
                    'memory_used_mb': self.utils.get_memory_usage()
                }
            
            print(f"   📊 Gap detection completed: {gap_info['gap_count']} gaps found")
            print(f"   ⏱️  Expected frequency: {gap_info['expected_frequency']}")
            print(f"   🕐 Time range: {gap_info['time_range']['start']} to {gap_info['time_range']['end']}")
            
            # Check memory before fixing
            if not self.utils.check_memory_available(self.memory_limit_mb):
                print(f"   ⚠️  Memory usage high before gap fixing: {self.utils.get_memory_usage():.1f} MB")
                print(f"   🧹 Forcing garbage collection...")
                gc.collect()
                if not self.utils.check_memory_available(self.memory_limit_mb):
                    return False, {'error': 'Insufficient memory for gap fixing'}
            
            # Fix gaps
            print(f"   🔧 Starting gap fixing with algorithm: {algorithm}")
            fixed_df, fix_results = self.algorithms.fix_gaps_in_dataframe(
                df, timestamp_col, gap_info, algorithm, show_progress
            )
            
            # Save fixed data
            print(f"   🔄 Creating backup...")
            backup_path = self.utils.create_backup(file_path)
            print(f"   📦 Backup created: {backup_path}")
            
            print(f"   💾 Saving fixed data...")
            success = self.utils.save_fixed_data(fixed_df, file_path)
            
            if success:
                print(f"   ✅ Data saved successfully")
                results = {
                    'success': True,
                    'gaps_fixed': fix_results['gaps_fixed'],
                    'algorithm_used': fix_results['algorithm_used'],
                    'processing_time': fix_results['processing_time'],
                    'backup_created': str(backup_path),
                    'original_gaps': gap_info['gap_count'],
                    'memory_used_mb': fix_results['memory_used_mb']
                }
                return True, results
            else:
                print(f"   ❌ Failed to save fixed data")
                return False, {'error': 'Failed to save fixed data'}
                
        except Exception as e:
            print(f"   ❌ Exception during gap fixing: {e}")
            import traceback
            traceback.print_exc()
            return False, {'error': str(e)}
    
    def fix_multiple_files(self, file_paths: List[Path], algorithm: str = 'auto',
                          show_progress: bool = True) -> Dict[str, Dict]:
        """
        Fix gaps in multiple files with progress tracking.
        
        Args:
            file_paths: List of file paths to fix
            algorithm: Algorithm to use for gap fixing
            show_progress: Whether to show progress bars
            
        Returns:
            Dictionary with results for each file
        """
        results = {}
        total_files = len(file_paths)
        
        print(f"\n🚀 Starting gap fixing for {total_files} files...")
        print(f"📊 Algorithm: {algorithm}")
        
        # Estimate total time
        estimated_time = self.utils.estimate_total_processing_time(file_paths)
        print(f"⏱️  Estimated total processing time: {estimated_time}")
        
        # Process files
        start_time = time.time()
        
        for i, file_path in enumerate(file_paths, 1):
            print(f"\n📁 Processing file {i}/{total_files}: {file_path.name}")
            
            success, file_results = self.fix_file_gaps(
                file_path, algorithm, show_progress
            )
            
            results[str(file_path)] = file_results
            
            if success:
                print(f"✅ {file_path.name}: {file_results['gaps_fixed']} gaps fixed")
            else:
                print(f"❌ {file_path.name}: {file_results.get('error', 'Unknown error')}")
            
            # Memory cleanup
            gc.collect()
            
            # Check memory usage
            if not self.utils.check_memory_available(self.memory_limit_mb):
                print("⚠️  Memory usage high, forcing garbage collection...")
                gc.collect()
        
        total_time = time.time() - start_time
        
        # Summary
        successful_fixes = sum(1 for r in results.values() if r.get('success', False))
        total_gaps_fixed = sum(r.get('gaps_fixed', 0) for r in results.values() if r.get('success', False))
        
        print(f"\n🎉 Gap fixing completed!")
        print(f"📊 Files processed: {total_files}")
        print(f"✅ Successful fixes: {successful_fixes}")
        print(f"📈 Total gaps fixed: {total_gaps_fixed:,}")
        print(f"⏱️  Total time: {total_time:.1f} seconds")
        
        return results
