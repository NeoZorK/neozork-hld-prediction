#!/usr/bin/env python3
"""
Duplicate Fixing module.

This module provides duplicate fixing capabilities for financial data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional


class DuplicateFixing:
    """
    Analyzer for fixing duplicate data in financial datasets.
    
    Features:
    - Automatic duplicate removal
    - Progress tracking with ETA
    - Cleaned data export
    - Critical issues handling
    """
    
    def __init__(self):
        """Initialize the DuplicateFixing."""
        pass
    
    def _fix_duplicates_and_save(self, system, all_dupe_summaries, critical_issues):
        """
        Fix duplicates and critical issues, then save cleaned data.
        
        Args:
            system: InteractiveSystem instance
            all_dupe_summaries: Dictionary of duplicate summaries for all timeframes
            critical_issues: List of critical issues detected
            
        Returns:
            bool: True if successful
        """
        print(f"\n🔧 FIXING DUPLICATES AND CRITICAL ISSUES")
        print("-" * 50)
        
        # Create cleaned_data directory
        cleaned_data_dir = Path("../data/cleaned_data")
        cleaned_data_dir.mkdir(exist_ok=True)
        
        # Generate timestamp for files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        fixed_count = 0
        total_files_to_fix = 1  # Main dataset
        if hasattr(system, 'other_timeframes_data') and system.other_timeframes_data:
            total_files_to_fix += len(system.other_timeframes_data)
        
        # Fix main dataset
        current_file = 1
        progress = (current_file / total_files_to_fix) * 100
        eta_remaining = total_files_to_fix - current_file
        print(f"\n🔧 Fixing main dataset: [{progress:5.1f}%] ETA: {eta_remaining} files remaining")
        
        main_summary = all_dupe_summaries.get('main', {})
        if main_summary.get('total_duplicates', 0) > 0:
            # Remove duplicates from main dataset
            initial_rows = len(system.current_data)
            system.current_data = system.current_data.drop_duplicates(keep='first')
            removed_rows = initial_rows - len(system.current_data)
            print(f"   ✅ Removed {removed_rows:,} duplicate rows from main dataset")
            fixed_count += removed_rows
        else:
            print(f"   ✅ Main dataset already clean")
        
        # Save main dataset
        main_filename = f"cleaned_main_dataset_{timestamp}.parquet"
        main_filepath = cleaned_data_dir / main_filename
        system.current_data.to_parquet(main_filepath, index=False)
        print(f"   💾 Saved: {main_filepath}")
        
        # Fix multi-timeframe datasets
        if hasattr(system, 'other_timeframes_data') and system.other_timeframes_data:
            for timeframe, timeframe_data in system.other_timeframes_data.items():
                current_file += 1
                progress = (current_file / total_files_to_fix) * 100
                eta_remaining = total_files_to_fix - current_file
                eta_str = f"ETA: {eta_remaining} files remaining" if eta_remaining > 0 else "ETA: Complete"
                
                print(f"\n🔧 Fixing {timeframe} dataset: [{progress:5.1f}%] {eta_str}")
                
                if timeframe_data is not None and not timeframe_data.empty:
                    tf_summary = all_dupe_summaries.get(timeframe, {})
                    if tf_summary.get('total_duplicates', 0) > 0:
                        # Remove duplicates from timeframe dataset
                        initial_rows = len(timeframe_data)
                        cleaned_timeframe_data = timeframe_data.drop_duplicates(keep='first')
                        removed_rows = initial_rows - len(cleaned_timeframe_data)
                        print(f"   ✅ Removed {removed_rows:,} duplicate rows from {timeframe} dataset")
                        fixed_count += removed_rows
                        
                        # Update the data in system
                        system.other_timeframes_data[timeframe] = cleaned_timeframe_data
                    else:
                        print(f"   ✅ {timeframe} dataset already clean")
                        cleaned_timeframe_data = timeframe_data
                    
                    # Save timeframe dataset
                    tf_filename = f"cleaned_{timeframe.lower()}_dataset_{timestamp}.parquet"
                    tf_filepath = cleaned_data_dir / tf_filename
                    cleaned_timeframe_data.to_parquet(tf_filepath, index=False)
                    print(f"   💾 Saved: {tf_filepath}")
                else:
                    print(f"   ⚠️  {timeframe} dataset is empty or None - skipping")
        
        # Summary of fixes
        print(f"\n✅ DUPLICATE FIXING COMPLETED")
        print("-" * 40)
        print(f"   🔧 Total duplicates removed: {fixed_count:,}")
        print(f"   📁 Files saved to: ../data/cleaned_data/")
        print(f"   🏷️  Timestamp: {timestamp}")
        
        # Note about critical issues (NaT values)
        if critical_issues:
            print(f"\n⚠️  NOTE: Critical issues (NaT values) were detected but not automatically fixed.")
            print(f"   💡 These require manual data source investigation:")
            for issue in critical_issues[:5]:  # Show first 5 issues
                print(f"      • {issue}")
            if len(critical_issues) > 5:
                print(f"      • ... and {len(critical_issues) - 5} more issues")
        
        print(f"\n🎯 CLEANED DATA IS NOW READY FOR ML USAGE")
        print(f"   📊 Use the cleaned files from ../data/cleaned_data/ for machine learning")
        print(f"   🚀 Data quality has been improved and duplicates removed")
        
        return True
