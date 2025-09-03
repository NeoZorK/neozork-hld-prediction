#!/usr/bin/env python3
"""
Base Duplicates Analyzer module.

This module provides the main interface for duplicate analysis,
orchestrating calls to specialized analyzers.
"""

import pandas as pd
import numpy as np
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Import specialized analyzers
from .duplicate_detection import DuplicateDetection
from .duplicate_fixing import DuplicateFixing


class DuplicatesAnalyzer:
    """
    Main Duplicates Analyzer class that orchestrates all duplicate analysis operations.
    
    This class provides a unified interface for:
    - Exact duplicate detection
    - Timestamp-based duplicate detection
    - OHLCV-based duplicate detection
    - Business logic duplicate detection
    - Progress tracking with ETA
    - Automatic duplicate removal
    - Cleaned data export
    """
    
    def __init__(self):
        """Initialize the Duplicates Analyzer with specialized analyzers."""
        self.duplicate_detection = DuplicateDetection()
        self.duplicate_fixing = DuplicateFixing()
    
    def run_duplicates_analysis(self, system) -> bool:
        """
        Run detailed duplicates analysis on all preloaded data with fixing option.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🔄 DUPLICATES ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        # Analyze main dataset
        print(f"\n📊 MAIN TIMEFRAME DATASET ANALYSIS")
        print("-" * 40)
        df = system.current_data
        main_dupe_summary = self.duplicate_detection._analyze_duplicates(df)
        
        # Show detailed duplicates info for main dataset
        if main_dupe_summary.get('total_duplicates', 0) > 0:
            print(f"\n📊 Main Dataset Duplicates Summary:")
            print(f"   • Total duplicates: {main_dupe_summary['total_duplicates']:,}")
            print(f"   • Duplicate percentage: {main_dupe_summary['duplicate_percent']:.2f}%")
            
            if main_dupe_summary.get('key_columns'):
                print(f"   • Key columns with duplicates:")
                for key_col in main_dupe_summary['key_columns']:
                    print(f"     - {key_col['column']}: {key_col['duplicate_count']:,} duplicates")
        else:
            print("✅ No duplicates found in main dataset")
        
        # Store all duplicate summaries for potential fixing
        all_dupe_summaries = {'main': main_dupe_summary}
        
        # Analyze multi-timeframe datasets if available
        if hasattr(system, 'other_timeframes_data') and system.other_timeframes_data:
            print(f"\n🔄 MULTI-TIMEFRAME DATASETS ANALYSIS")
            print("-" * 50)
            
            total_timeframes = len(system.other_timeframes_data)
            print(f"📊 Found {total_timeframes} additional timeframes to analyze")
            
            # Progress tracking with ETA
            current_timeframe = 0
            total_rows = len(system.current_data)
            start_time = time.time()
            
            for timeframe, timeframe_data in system.other_timeframes_data.items():
                current_timeframe += 1
                if timeframe_data is not None and not timeframe_data.empty:
                    total_rows += len(timeframe_data)
                    
                    # Progress bar with ETA (single line)
                    progress = (current_timeframe / total_timeframes) * 100
                    elapsed_time = time.time() - start_time
                    avg_time_per_tf = elapsed_time / current_timeframe if current_timeframe > 0 else 0
                    eta_remaining = avg_time_per_tf * (total_timeframes - current_timeframe)
                    eta_str = f"ETA: {eta_remaining:.1f}s" if eta_remaining > 0 else "ETA: Complete"
                    
                    print(f"\n⏱️  Analyzing {timeframe} timeframe: [{progress:5.1f}%] {eta_str}")
                    print(f"   📊 Shape: {timeframe_data.shape[0]:,} rows × {timeframe_data.shape[1]} columns")
                    
                    # Analyze duplicates for this timeframe
                    tf_dupe_summary = self.duplicate_detection._analyze_duplicates(timeframe_data)
                    all_dupe_summaries[timeframe] = tf_dupe_summary
                    
                    if tf_dupe_summary.get('total_duplicates', 0) > 0:
                        print(f"   🔄 Duplicates found: {tf_dupe_summary['total_duplicates']:,} ({tf_dupe_summary['duplicate_percent']:.2f}%)")
                        
                        if tf_dupe_summary.get('key_columns'):
                            print(f"   📋 Key columns with duplicates:")
                            for key_col in tf_dupe_summary['key_columns']:
                                print(f"      - {key_col['column']}: {key_col['duplicate_count']:,} duplicates")
                    else:
                        print(f"   ✅ No duplicates found in {timeframe} timeframe")
                else:
                    current_timeframe += 1  # Count empty timeframes too
                    print(f"   ⚠️  {timeframe} timeframe data is empty or None")
        else:
            print(f"\n💡 No additional timeframes found for analysis")
            print("   Only main dataset was analyzed")
            total_rows = len(system.current_data)
        
        # Overall summary
        print(f"\n📋 OVERALL DUPLICATES ANALYSIS SUMMARY")
        print("-" * 50)
        
        # Count total duplicates across all datasets
        total_duplicates = main_dupe_summary.get('total_duplicates', 0)
        
        if hasattr(system, 'other_timeframes_data') and system.other_timeframes_data:
            for timeframe, timeframe_data in system.other_timeframes_data.items():
                if timeframe_data is not None and not timeframe_data.empty:
                    tf_summary = all_dupe_summaries.get(timeframe, {})
                    total_duplicates += tf_summary.get('total_duplicates', 0)
        
        overall_duplicate_percent = (total_duplicates / total_rows) * 100 if total_rows > 0 else 0
        
        print(f"   📊 Total rows analyzed: {total_rows:,}")
        print(f"   🔄 Total duplicates found: {total_duplicates:,}")
        print(f"   📈 Overall duplicate percentage: {overall_duplicate_percent:.2f}%")
        
        # Check for critical issues (NaT values)
        critical_issues = []
        
        # Check main dataset for NaT values
        timestamp_cols = [col for col in system.current_data.columns if 'time' in col.lower() or 'date' in col.lower()]
        for ts_col in timestamp_cols:
            nat_count = system.current_data[ts_col].isna().sum()
            if nat_count > 0:
                critical_issues.append(f"Main: {nat_count:,} NaT values in {ts_col}")
        
        # Check multi-timeframe datasets for NaT values
        if hasattr(system, 'other_timeframes_data') and system.other_timeframes_data:
            for timeframe, timeframe_data in system.other_timeframes_data.items():
                if timeframe_data is not None and not timeframe_data.empty:
                    timestamp_cols = [col for col in timeframe_data.columns if 'time' in col.lower() or 'date' in col.lower()]
                    for ts_col in timestamp_cols:
                        nat_count = timeframe_data[ts_col].isna().sum()
                        if nat_count > 0:
                            critical_issues.append(f"{timeframe}: {nat_count:,} NaT values in {ts_col}")
        
        if critical_issues:
            print(f"\n⚠️  CRITICAL ISSUES DETECTED:")
            print("-" * 40)
            for issue in critical_issues:
                print(f"   • {issue}")
            print(f"\n💡 These issues may affect data quality and ML model performance!")
        
        if total_duplicates > 0 or critical_issues:
            print(f"\n💡 RECOMMENDATIONS:")
            print(f"   • Consider fixing duplicates and critical issues")
            print(f"   • Review data sources for potential duplicate generation")
            print(f"   • Check data loading processes for redundancy")
            print(f"   • Fix timestamp column issues before ML usage")
            
            # Ask user if they want to fix duplicates
            try:
                fix_choice = input("\n❓ Fix Duplicates and Critical Issues? (y/n, default: y): ").strip().lower()
                if fix_choice in ['', 'y', 'yes']:
                    return self.duplicate_fixing._fix_duplicates_and_save(system, all_dupe_summaries, critical_issues)
                else:
                    print("   ⏭️  Skipping duplicate fixing...")
            except EOFError:
                print("   ⏭️  Skipping duplicate fixing...")
        else:
            print(f"\n✅ All datasets are clean - no duplicates found!")
        
        return True
