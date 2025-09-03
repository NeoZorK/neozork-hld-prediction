#!/usr/bin/env python3
"""
Gaps Analyzer module.

This module provides comprehensive time series gaps analysis capabilities
for financial data including file loading and gap detection.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from pathlib import Path


class GapsAnalyzer:
    """
    Analyzer for time series gaps in financial data.
    
    Features:
    - File loading for gap analysis
    - Time series gaps detection
    - Frequency determination
    - Multi-timeframe analysis
    """
    
    def __init__(self):
        """Initialize the GapsAnalyzer."""
        pass
    
    def run_time_series_gaps_analysis(self, system) -> bool:
        """
        Run time series gaps analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n⏱️  TIME SERIES GAPS ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        # Find timestamp columns
        timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
        if not timestamp_cols:
            print("❌ No timestamp columns found for gaps analysis.")
            return False
        
        print(f"🔍 Analyzing gaps in {len(timestamp_cols)} timestamp columns...")
        
        for ts_col in timestamp_cols[:3]:  # Analyze first 3 timestamp columns
            print(f"\n📅 {ts_col} Gaps Analysis:")
            
            try:
                # Convert to datetime if needed
                if df[ts_col].dtype == 'object':
                    df[ts_col] = pd.to_datetime(df[ts_col], errors='coerce')
                
                # Analyze gaps
                gap_summary = self._analyze_time_series_gaps(df)
                
                if gap_summary:
                    # Find gaps for this specific column
                    col_gaps = [gap for gap in gap_summary if gap['column'] == ts_col]
                    if col_gaps and col_gaps[0]['gap_count'] > 0:
                        print(f"   ⚠️  Found {col_gaps[0]['gap_count']} gaps")
                        print(f"   📊 Total gap time: {col_gaps[0]['total_gap_hours']:.2f} hours")
                        print(f"   📏 Largest gap: {col_gaps[0]['largest_gap']:.2f} hours")
                    else:
                        print(f"   ✅ No gaps detected")
                else:
                    print(f"   ✅ No gaps detected")
                    
            except Exception as e:
                print(f"   ❌ Error analyzing gaps: {e}")
        
        # Multi-timeframe analysis if available
        if hasattr(system, 'other_timeframes_data') and system.other_timeframes_data:
            print(f"\n🔄 MULTI-TIMEFRAME GAPS ANALYSIS:")
            
            # Check if timeframe_info exists
            if hasattr(system, 'timeframe_info') and system.timeframe_info:
                cross_timeframes = system.timeframe_info.get('cross_timeframes', {})
                
                if cross_timeframes:
                    print(f"📊 Found {len(cross_timeframes)} cross-timeframe datasets to analyze")
                    
                    for timeframe, file_list in cross_timeframes.items():
                        if file_list and len(file_list) > 0:
                            print(f"\n   ⏱️  Analyzing {timeframe} timeframe:")
                            
                            # Analyze the first file in the list
                            first_file = file_list[0]
                            if isinstance(first_file, str) and Path(first_file).exists():
                                try:
                                    df_timeframe = self._load_file_for_gap_analysis(Path(first_file))
                                    if df_timeframe is not None:
                                        gap_summary = self._analyze_time_series_gaps(df_timeframe)
                                        if gap_summary:
                                            total_gaps = sum(gap['gap_count'] for gap in gap_summary)
                                            if total_gaps > 0:
                                                print(f"     ⚠️  Found {total_gaps} gaps in {timeframe}")
                                            else:
                                                print(f"     ✅ No gaps found in {timeframe}")
                                        else:
                                            print(f"     ✅ No gaps found in {timeframe}")
                                    else:
                                        print(f"     ❌ Could not load {timeframe} data")
                                except Exception as e:
                                    print(f"     ❌ Error analyzing {timeframe}: {e}")
                            else:
                                print(f"     ⚠️  No valid file found for {timeframe}")
                        else:
                            print(f"   ⚠️  No files found for {timeframe} timeframe")
                else:
                    print(f"   💡 No cross-timeframe datasets found")
            else:
                print(f"   💡 No timeframe information available")
                
                # Fallback to other_timeframes_data if available
                if system.other_timeframes_data:
                    print(f"📊 Found {len(system.other_timeframes_data)} additional timeframes")
                    
                    for timeframe, df_timeframe in system.other_timeframes_data.items():
                        if df_timeframe is not None and not df_timeframe.empty:
                            print(f"\n   ⏱️  Analyzing {timeframe} timeframe:")
                            try:
                                gap_summary = self._analyze_time_series_gaps(df_timeframe)
                                if gap_summary:
                                    total_gaps = sum(gap['gap_count'] for gap in gap_summary)
                                    if total_gaps > 0:
                                        print(f"     ⚠️  Found {total_gaps} gaps in {timeframe}")
                                    else:
                                        print(f"     ✅ No gaps found in {timeframe}")
                                else:
                                    print(f"     ✅ No gaps found in {timeframe}")
                            except Exception as e:
                                print(f"     ❌ Error analyzing {timeframe}: {e}")
                        else:
                            print(f"     ⚠️  Empty or None data for {timeframe}")
        else:
            print(f"💡 No additional timeframes found for analysis")
            print(f"   Only main dataset was analyzed")
        
        return True
    
    def _load_file_for_gap_analysis(self, file_path) -> Optional[pd.DataFrame]:
        """
        Load file for gap analysis.
        
        Args:
            file_path: Path to the file to load
            
        Returns:
            Optional[pd.DataFrame]: Loaded dataframe or None if error
        """
        try:
            if str(file_path).endswith('.csv'):
                df = pd.read_csv(file_path)
            elif str(file_path).endswith('.parquet'):
                df = pd.read_parquet(file_path)
            else:
                print(f"❌ Unsupported file format: {file_path}")
                return None
            
            # Check if timestamp column exists
            timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
            if not timestamp_cols:
                print(f"❌ No timestamp columns found in {file_path}")
                return None
            
            # Convert timestamp to datetime
            for ts_col in timestamp_cols:
                df[ts_col] = pd.to_datetime(df[ts_col], errors='coerce')
            
            return df
            
        except Exception as e:
            print(f"❌ Error loading file {file_path}: {e}")
            return None
    
    def _analyze_time_series_gaps(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Analyze time series gaps in a dataframe.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            List[Dict[str, Any]]: List of gap summaries
        """
        gap_summaries = []
        
        # Find timestamp columns
        timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
        
        for ts_col in timestamp_cols:
            try:
                # Ensure datetime type
                if df[ts_col].dtype != 'datetime64[ns]':
                    df[ts_col] = pd.to_datetime(df[ts_col], errors='coerce')
                
                # Sort by timestamp
                df_sorted = df.sort_values(ts_col).copy()
                
                # Find gaps
                gaps = []
                for i in range(1, len(df_sorted)):
                    current_time = df_sorted[ts_col].iloc[i]
                    prev_time = df_sorted[ts_col].iloc[i-1]
                    
                    if pd.notna(current_time) and pd.notna(prev_time):
                        time_diff = current_time - prev_time
                        
                        # Check if gap is larger than expected
                        if time_diff > pd.Timedelta(hours=1):  # Assuming hourly data
                            gaps.append({
                                'start': prev_time,
                                'end': current_time,
                                'duration': time_diff,
                                'gap_size': time_diff.total_seconds() / 3600  # hours
                            })
                
                if gaps:
                    gap_summaries.append({
                        'column': ts_col,
                        'gap_count': len(gaps),
                        'total_gap_hours': sum(gap['gap_size'] for gap in gaps),
                        'largest_gap': max(gap['gap_size'] for gap in gaps),
                        'gaps': gaps
                    })
                else:
                    gap_summaries.append({
                        'column': ts_col,
                        'gap_count': 0,
                        'total_gap_hours': 0,
                        'largest_gap': 0,
                        'gaps': []
                    })
                    
            except Exception as e:
                print(f"❌ Error analyzing gaps in {ts_col}: {e}")
                gap_summaries.append({
                    'column': ts_col,
                    'gap_count': 0,
                    'total_gap_hours': 0,
                    'largest_gap': 0,
                    'gaps': [],
                    'error': str(e)
                })
        
        return gap_summaries
    
    def _determine_frequency_from_timedelta(self, td: pd.Timedelta) -> str:
        """
        Determine frequency string from timedelta.
        
        Args:
            td: pandas Timedelta object
            
        Returns:
            str: Frequency string (e.g., '1H', '30T', '1D')
        """
        total_seconds = td.total_seconds()
        
        if total_seconds < 60:  # Less than 1 minute
            return f"{int(total_seconds)}S"
        elif total_seconds < 3600:  # Less than 1 hour
            minutes = int(total_seconds / 60)
            return f"{minutes}T"
        elif total_seconds < 86400:  # Less than 1 day
            hours = int(total_seconds / 3600)
            return f"{hours}H"
        elif total_seconds < 604800:  # Less than 1 week
            days = int(total_seconds / 86400)
            return f"{days}D"
        elif total_seconds < 2592000:  # Less than 1 month (30 days)
            weeks = int(total_seconds / 604800)
            return f"{weeks}W"
        elif total_seconds < 31536000:  # Less than 1 year
            months = int(total_seconds / 2592000)
            return f"{months}M"
        else:  # 1 year or more
            years = int(total_seconds / 31536000)
            return f"{years}Y"
