#!/usr/bin/env python3
"""
Gap analysis and fixing utilities for time series data.
Handles detection, analysis, and correction of data gaps.
"""

import pandas as pd
import gc
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from .memory_manager import MemoryManager


class GapAnalyzer:
    """Analyzes and fixes time series gaps in data."""
    
    def __init__(self, memory_manager: MemoryManager):
        """
        Initialize GapAnalyzer.
        
        Args:
            memory_manager: MemoryManager instance
        """
        self.memory_manager = memory_manager
    
    def analyze_time_series_gaps(self, data_files: List[Path], 
                                Fore, Style) -> List[Dict]:
        """
        Analyze time series gaps in multiple data files.
        
        Args:
            data_files: List of file paths to analyze
            Fore: Colorama Fore object for colored output
            Style: Colorama Style object for styling
            
        Returns:
            List of gap analysis results
        """
        print(f"\n🔍 TIME SERIES GAP ANALYSIS")
        print("-" * 50)
        print(f"📁 Analyzing {len(data_files)} files for time series gaps...")
        
        gap_summary = []
        
        for i, file_path in enumerate(data_files, 1):
            try:
                print(f"\n📊 File {i}/{len(data_files)}: {file_path.name}")
                
                # Load data
                df = self._load_file_for_analysis(file_path)
                if df is None:
                    continue
                
                # Find timestamp column
                timestamp_col = self._find_timestamp_column(df)
                if timestamp_col is None:
                    print(f"   ⚠️  No timestamp column found, skipping...")
                    continue
                
                print(f"   📅 Timestamp column: {timestamp_col}")
                
                # Analyze gaps
                gap_info = self._detect_gaps(df, timestamp_col)
                
                # Store results
                gap_summary.append({
                    'file_path': file_path,
                    'file_name': file_path.name,
                    'timestamp_column': timestamp_col,
                    'total_rows': len(df),
                    'gap_info': gap_info,
                    'dataframe': df
                })
                
                # Memory cleanup
                del df
                self.memory_manager.optimize_memory()
                
            except Exception as e:
                print(f"   ❌ Error analyzing {file_path.name}: {e}")
                continue
        
        return gap_summary
    
    def _load_file_for_analysis(self, file_path: Path) -> Optional[pd.DataFrame]:
        """
        Load file for gap analysis.
        
        Args:
            file_path: Path to file
            
        Returns:
            DataFrame or None if loading failed
        """
        try:
            if file_path.suffix.lower() == '.csv':
                return pd.read_csv(file_path, nrows=10000)  # Sample for analysis
            elif file_path.suffix.lower() == '.parquet':
                return pd.read_parquet(file_path)
            else:
                print(f"   ⚠️  Unsupported file format: {file_path.suffix}")
                return None
        except Exception as e:
            print(f"   ❌ Error loading {file_path.name}: {e}")
            return None
    
    def _find_timestamp_column(self, df: pd.DataFrame) -> Optional[str]:
        """
        Find timestamp column in DataFrame.
        
        Args:
            df: DataFrame to search
            
        Returns:
            Column name or None if not found
        """
        if df is None or df.empty:
            return None
        
        # Common timestamp column names
        timestamp_names = [
            'timestamp', 'time', 'date', 'datetime', 'dt', 'ts',
            'Timestamp', 'Time', 'Date', 'DateTime', 'DT', 'TS'
        ]
        
        for col in timestamp_names:
            if col in df.columns:
                return col
        
        # Try to find by data type
        for col in df.columns:
            try:
                # Check if column contains datetime-like data
                sample_data = df[col].dropna().head(10)
                if len(sample_data) > 0:
                    pd.to_datetime(sample_data, errors='raise')
                    return col
            except Exception:
                continue
        
        return None
    
    def _detect_gaps(self, df: pd.DataFrame, timestamp_column: str) -> Dict:
        """
        Detect gaps in time series data.
        
        Args:
            df: DataFrame with time series data
            timestamp_column: Name of timestamp column
            
        Returns:
            Dictionary with gap information
        """
        if df is None or df.empty or timestamp_column not in df.columns:
            return {'has_gaps': False, 'gap_count': 0, 'gaps': []}
        
        try:
            # Ensure timestamp column is datetime
            df_copy = df.copy()
            df_copy[timestamp_column] = pd.to_datetime(df_copy[timestamp_column], errors='coerce')
            df_copy = df_copy.dropna(subset=[timestamp_column])
            
            if len(df_copy) == 0:
                return {'has_gaps': False, 'gap_count': 0, 'gaps': []}
            
            # Sort by timestamp
            df_copy = df_copy.sort_values(timestamp_column)
            
            # Calculate time differences
            time_diffs = df_copy[timestamp_column].diff().dropna()
            
            if len(time_diffs) == 0:
                return {'has_gaps': False, 'gap_count': 0, 'gaps': []}
            
            # Determine expected frequency
            expected_freq = self._determine_expected_frequency(df_copy, timestamp_column)
            
            # Set gap threshold (1.5x expected frequency)
            if expected_freq:
                threshold = pd.Timedelta(expected_freq) * 1.5
            else:
                # Use median + 2*std as threshold
                median_diff = time_diffs.median()
                std_diff = time_diffs.std()
                threshold = median_diff + (2 * std_diff)
            
            # Find gaps
            gaps = time_diffs[time_diffs > threshold]
            gap_count = len(gaps)
            
            return {
                'has_gaps': gap_count > 0,
                'gap_count': gap_count,
                'gaps': gaps.tolist() if gap_count > 0 else [],
                'expected_frequency': expected_freq,
                'threshold': threshold,
                'time_differences': time_diffs
            }
            
        except Exception as e:
            print(f"   ❌ Error detecting gaps: {e}")
            return {'has_gaps': False, 'gap_count': 0, 'gaps': []}
    
    def _determine_expected_frequency(self, df: pd.DataFrame, 
                                    datetime_column: str = 'Timestamp') -> Optional[str]:
        """
        Determine expected frequency of time series data.
        
        Args:
            df: DataFrame with time series data
            datetime_column: Name of datetime column
            
        Returns:
            Frequency string or None if cannot determine
        """
        if df is None or df.empty or datetime_column not in df.columns:
            return None
        
        try:
            # Calculate time differences
            time_diffs = df[datetime_column].diff().dropna()
            
            if len(time_diffs) == 0:
                return None
            
            # Get median time difference
            median_diff = time_diffs.median()
            
            # Convert to frequency string
            if median_diff <= pd.Timedelta(minutes=1):
                return '1T'  # 1 minute
            elif median_diff <= pd.Timedelta(minutes=5):
                return '5T'  # 5 minutes
            elif median_diff <= pd.Timedelta(minutes=15):
                return '15T'  # 15 minutes
            elif median_diff <= pd.Timedelta(minutes=30):
                return '30T'  # 30 minutes
            elif median_diff <= pd.Timedelta(hours=1):
                return '1H'  # 1 hour
            elif median_diff <= pd.Timedelta(hours=4):
                return '4H'  # 4 hours
            elif median_diff <= pd.Timedelta(days=1):
                return '1D'  # 1 day
            elif median_diff <= pd.Timedelta(weeks=1):
                return '1W'  # 1 week
            elif median_diff <= pd.Timedelta(days=30):
                return '1M'  # 1 month
            else:
                return '1Y'  # 1 year
                
        except Exception:
            return None
    
    def show_detailed_gap_info(self, gap_summary: List[Dict], Fore, Style):
        """
        Show detailed gap information.
        
        Args:
            gap_summary: List of gap analysis results
            Fore: Colorama Fore object
            Style: Colorama Style object
        """
        if not gap_summary:
            print(f"{Fore.YELLOW}No gap analysis results to display{Style.RESET_ALL}")
            return
        
        print(f"\n📊 DETAILED GAP ANALYSIS RESULTS")
        print("-" * 60)
        
        total_files = len(gap_summary)
        files_with_gaps = sum(1 for item in gap_summary if item['gap_info']['has_gaps'])
        
        print(f"📁 Total files analyzed: {total_files}")
        print(f"⚠️  Files with gaps: {files_with_gaps}")
        print(f"✅ Files without gaps: {total_files - files_with_gaps}")
        
        for item in gap_summary:
            file_name = item['file_name']
            gap_info = item['gap_info']
            
            print(f"\n📄 {file_name}")
            print(f"   📅 Timestamp column: {item['timestamp_column']}")
            print(f"   📊 Total rows: {item['total_rows']:,}")
            
            if gap_info['has_gaps']:
                print(f"   ⚠️  Gaps found: {gap_info['gap_count']:,}")
                if gap_info['expected_frequency']:
                    print(f"   ⏱️  Expected frequency: {gap_info['expected_frequency']}")
                print(f"   🚨 Gap threshold: {gap_info['threshold']}")
            else:
                print(f"   ✅ No gaps found")
    
    def fix_gaps_interactive(self, gap_summary: List[Dict], Fore, Style) -> List[Dict]:
        """
        Interactively fix gaps in data files.
        
        Args:
            gap_summary: List of gap analysis results
            Fore: Colorama Fore object
            Style: Colorama Style object
            
        Returns:
            List of updated gap summary with fixed data
        """
        if not gap_summary:
            print(f"{Fore.YELLOW}No gap analysis results to fix{Style.RESET_ALL}")
            return gap_summary
        
        print(f"\n🔧 INTERACTIVE GAP FIXING")
        print("-" * 50)
        
        files_to_fix = [item for item in gap_summary if item['gap_info']['has_gaps']]
        
        if not files_to_fix:
            print(f"✅ No files with gaps to fix!")
            return gap_summary
        
        print(f"📁 Files with gaps: {len(files_to_fix)}")
        
        # Ask user if they want to fix gaps
        try:
            fix_gaps = input(f"\nFix time series gaps? (y/n, default: y): ").strip().lower()
            if fix_gaps not in ['', 'y', 'yes']:
                print(f"⏭️  Skipping gap fixing...")
                return gap_summary
        except EOFError:
            print(f"\n👋 Goodbye!")
            return gap_summary
        
        # Initialize GapFixer
        try:
            from ..data import GapFixer
            gap_fixer = GapFixer(memory_limit_mb=self.memory_manager.max_memory_mb)
            print(f"✅ GapFixer initialized with memory limit: {self.memory_manager.max_memory_mb}MB")
        except Exception as e:
            print(f"❌ Error initializing GapFixer: {e}")
            print(f"⚠️  Cannot proceed with gap fixing...")
            return gap_summary
        
        # Fix gaps for each file
        for i, item in enumerate(files_to_fix, 1):
            file_name = item['file_name']
            print(f"\n🔧 Fixing gaps in {file_name} [{i}/{len(files_to_fix)}]...")
            
            try:
                # Load full file for fixing
                full_df = self._load_full_file_for_fixing(item['file_path'])
                if full_df is None:
                    continue
                
                # Fix gaps
                fixed_df = self._fix_gaps_in_dataframe(
                    gap_fixer, full_df, item['timestamp_column'], 
                    item['gap_info']
                )
                
                if fixed_df is not None:
                    # Update gap summary
                    item['dataframe'] = fixed_df
                    item['gap_info']['has_gaps'] = False
                    item['gap_info']['gap_count'] = 0
                    print(f"   ✅ Gaps fixed successfully!")
                else:
                    print(f"   ❌ Gap fixing failed, keeping original data")
                
                # Memory cleanup
                del full_df
                if 'fixed_df' in locals():
                    del fixed_df
                self.memory_manager.optimize_memory()
                
            except Exception as e:
                print(f"   ❌ Error fixing gaps in {file_name}: {e}")
                continue
        
        return gap_summary
    
    def _load_full_file_for_fixing(self, file_path: Path) -> Optional[pd.DataFrame]:
        """
        Load full file for gap fixing.
        
        Args:
            file_path: Path to file
            
        Returns:
            DataFrame or None if loading failed
        """
        try:
            if file_path.suffix.lower() == '.csv':
                return pd.read_csv(file_path)
            elif file_path.suffix.lower() == '.parquet':
                return pd.read_parquet(file_path)
            else:
                return None
        except Exception as e:
            print(f"   ❌ Error loading full file {file_path.name}: {e}")
            return None
    
    def _fix_gaps_in_dataframe(self, gap_fixer, df: pd.DataFrame, 
                              timestamp_column: str, gap_info: Dict) -> Optional[pd.DataFrame]:
        """
        Fix gaps in DataFrame using GapFixer.
        
        Args:
            gap_fixer: GapFixer instance
            df: DataFrame to fix
            timestamp_column: Name of timestamp column
            gap_info: Gap information dictionary
            
        Returns:
            Fixed DataFrame or None if fixing failed
        """
        try:
            # Use auto algorithm for fixing
            algorithm = 'auto'
            
            # Fix gaps
            fixed_df, results = gap_fixer._fix_gaps_in_dataframe(
                df, timestamp_column, gap_info, algorithm, show_progress=True
            )
            
            if fixed_df is not None:
                print(f"   ✅ Gaps fixed using {results['algorithm_used']}")
                print(f"      • Gaps fixed: {results['gaps_fixed']:,}")
                print(f"      • Processing time: {results['processing_time']:.2f}s")
                return fixed_df
            else:
                return None
                
        except Exception as e:
            print(f"   ❌ Error during gap fixing: {e}")
            return None
