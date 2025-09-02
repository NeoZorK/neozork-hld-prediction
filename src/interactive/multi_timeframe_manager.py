#!/usr/bin/env python3
"""
Multi-timeframe data management utilities.
Handles loading, processing, and organizing data from multiple timeframes.
"""

import pandas as pd
import gc
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from .memory_manager import MemoryManager
from .data_loader import DataLoader


class MultiTimeframeManager:
    """Manages multi-timeframe data loading and processing."""
    
    def __init__(self, memory_manager: MemoryManager, data_loader: DataLoader):
        """
        Initialize MultiTimeframeManager.
        
        Args:
            memory_manager: MemoryManager instance
            data_loader: DataLoader instance
        """
        self.memory_manager = memory_manager
        self.data_loader = data_loader
    
    def detect_timeframe_from_filename(self, filename: str) -> str:
        """
        Detect timeframe from filename patterns.
        
        Args:
            filename: Name of the file
            
        Returns:
            str: Detected timeframe or 'UNKNOWN'
        """
        filename_upper = filename.upper()
        
        # Common timeframe patterns - order matters! Longer patterns first to avoid conflicts
        patterns = {
            'M15': ['_M15_', '_M15.', 'PERIOD_M15', '_15M_', '_15M.'],
            'M30': ['_M30_', '_M30.', 'PERIOD_M30', '_30M_', '_30M.'],
            'M5': ['_M5_', '_M5.', 'PERIOD_M5', '_5M_', '_5M.'],
            'M1': ['_M1_', '_M1.', 'PERIOD_M1', '_1M_', '_1M.'],
            'H4': ['_H4_', '_H4.', 'PERIOD_H4', '_4H_', '_4H.'],
            'H1': ['_H1_', '_H1.', 'PERIOD_H1', '_1H_', '_1H.'],
            'D1': ['_D1_', '_D1.', 'PERIOD_D1', '_1D_', '_1D.', '_DAILY_'],
            'W1': ['_W1_', '_W1.', 'PERIOD_W1', '_1W_', '_1W.', '_WEEKLY_'],
            'MN1': ['_MN1_', '_MN1.', 'PERIOD_MN1', '_1MN_', '_1MN.', '_MONTHLY_']
        }
        
        # First, try to find exact matches with longer patterns first
        for timeframe, tf_patterns in patterns.items():
            for pattern in tf_patterns:
                if pattern in filename_upper:
                    # Additional check: make sure we're not matching a shorter pattern within a longer one
                    if timeframe == 'M1':
                        if any(p in filename_upper for p in ['_M15_', '_M15.', 'PERIOD_M15', '_15M_', '_15M.']):
                            continue  # Skip M1 if M15 is found
                        if any(p in filename_upper for p in ['_M30_', '_M30.', 'PERIOD_M30', '_30M_', '_30M.']):
                            continue  # Skip M1 if M30 is found
                        if any(p in filename_upper for p in ['_M5_', '_M5.', 'PERIOD_M5', '_5M_', '_5M.']):
                            continue  # Skip M1 if M5 is found
                    elif timeframe == 'M5':
                        if any(p in filename_upper for p in ['_M15_', '_M15.', 'PERIOD_M15', '_15M_', '_15M.']):
                            continue  # Skip M5 if M15 is found
                        if any(p in filename_upper for p in ['_M30_', '_M30.', 'PERIOD_M30', '_30M_', '_30M.']):
                            continue  # Skip M5 if M30 is found
                    elif timeframe == 'H1':
                        if any(p in filename_upper for p in ['_H4_', '_H4.', 'PERIOD_H4', '_4H_', '_4H.']):
                            continue  # Skip H1 if H4 is found
                    
                    return timeframe
        
        # Additional checks for common naming conventions
        if 'MINUTE' in filename_upper:
            if '1' in filename_upper:
                return 'M1'
            elif '5' in filename_upper:
                return 'M5'
            elif '15' in filename_upper:
                return 'M15'
            elif '30' in filename_upper:
                return 'M30'
        
        if 'HOUR' in filename_upper:
            if '1' in filename_upper:
                return 'H1'
            elif '4' in filename_upper:
                return 'H4'
        
        if 'DAY' in filename_upper or 'DAILY' in filename_upper:
            return 'D1'
        
        if 'WEEK' in filename_upper or 'WEEKLY' in filename_upper:
            return 'W1'
        
        if 'MONTH' in filename_upper or 'MONTHLY' in filename_upper:
            return 'MN1'
        
        return 'UNKNOWN'
    
    def organize_files_by_timeframe(self, folder_path: Path, mask: str = None) -> Dict[str, List[Path]]:
        """
        Organize files by detected timeframe.
        
        Args:
            folder_path: Path to folder containing data files
            mask: Optional mask to filter files
            
        Returns:
            Dictionary mapping timeframes to file lists
        """
        timeframe_data = {}
        
        # Search for data files
        for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
            if mask:
                # Apply mask filter
                pattern = f"*{mask}*{ext}"
                files = list(folder_path.glob(pattern))
                # Also try case-insensitive search
                pattern_upper = f"*{mask.upper()}*{ext}"
                files.extend(folder_path.glob(pattern_upper))
                pattern_lower = f"*{mask.lower()}*{ext}"
                files.extend(folder_path.glob(pattern_lower))
            else:
                # No mask, get all files
                files = list(folder_path.glob(f"*{ext}"))
            
            # Filter out temporary files and remove duplicates
            files = [f for f in files if not f.name.startswith('tmp')]
            files = list(set(files))  # Remove duplicates
            
            for file in files:
                # Detect timeframe from filename
                timeframe = self.detect_timeframe_from_filename(file.name)
                
                # Debug: show what timeframe was detected for each file
                print(f"   🔍 {file.name} -> {timeframe}")
                
                if timeframe not in timeframe_data:
                    timeframe_data[timeframe] = []
                
                timeframe_data[timeframe].append(file)
        
        return timeframe_data
    
    def display_timeframe_summary(self, timeframe_data: Dict[str, List[Path]], mask: str = None):
        """
        Display summary of found timeframes and files.
        
        Args:
            timeframe_data: Dictionary mapping timeframes to file lists
            mask: Optional mask used for filtering
        """
        print(f"\n📊 Found data for {len(timeframe_data)} timeframes:")
        if mask:
            print(f"   Filter applied: '{mask}'")
        
        for tf, files in timeframe_data.items():
            print(f"   {tf}: {len(files)} files")
            for file in files[:3]:  # Show first 3 files
                file_size_mb = self.memory_manager.get_file_size_mb(file)
                print(f"      • {file.name} ({file_size_mb:.1f}MB)")
            if len(files) > 3:
                print(f"      • ... and {len(files) - 3} more files")
    
    def select_base_timeframe(self, timeframe_data: Dict[str, List[Path]]) -> Optional[str]:
        """
        Interactive selection of base timeframe.
        
        Args:
            timeframe_data: Dictionary mapping timeframes to file lists
            
        Returns:
            Selected base timeframe or None if selection failed
        """
        print("\n🎯 SELECT BASE TIMEFRAME")
        print("-" * 30)
        print("💡 Base timeframe will be the primary dataset for analysis.")
        print("   Other timeframes are available for separate analysis.")
        print("")
        
        available_timeframes = list(timeframe_data.keys())
        for i, tf in enumerate(available_timeframes, 1):
            print(f"{i}. {tf} ({len(timeframe_data[tf])} files)")
        
        try:
            choice = input("\nSelect base timeframe (number): ").strip()
            if not choice.isdigit():
                print("❌ Invalid choice")
                return None
                
            tf_idx = int(choice) - 1
            if tf_idx < 0 or tf_idx >= len(available_timeframes):
                print("❌ Invalid timeframe selection")
                return None
                
            base_timeframe = available_timeframes[tf_idx]
            print(f"\n✅ Selected base timeframe: {base_timeframe}")
            return base_timeframe
            
        except EOFError:
            print("\n👋 Goodbye!")
            return None
    
    def load_base_timeframe_data(self, timeframe_data: Dict[str, List[Path]], 
                               base_timeframe: str) -> List[pd.DataFrame]:
        """
        Load data for base timeframe.
        
        Args:
            timeframe_data: Dictionary mapping timeframes to file lists
            base_timeframe: Selected base timeframe
            
        Returns:
            List of DataFrames for base timeframe
        """
        print(f"\n🔄 Loading base timeframe data ({base_timeframe})...")
        base_data = []
        
        for file in timeframe_data[base_timeframe]:
            try:
                df = self.data_loader.load_data_from_file(str(file))
                df['source_file'] = file.name
                df['timeframe'] = base_timeframe
                base_data.append(df)
                print(f"✅ Loaded: {file.name} ({df.shape[0]:,} rows)")
            except Exception as e:
                print(f"❌ Error loading {file.name}: {e}")
                continue
        
        return base_data
    
    def load_other_timeframes(self, cross_timeframes: Dict[str, List[Path]]) -> Dict[str, pd.DataFrame]:
        """
        Load data for other timeframes with gap fixing.
        
        Args:
            cross_timeframes: Dictionary mapping timeframes to file lists
            
        Returns:
            Dictionary mapping timeframes to DataFrames
        """
        if not cross_timeframes:
            return {}
        
        print(f"\n🔄 MULTI-TIMEFRAME DATA LOADING")
        print("-" * 50)
        print("💡 Loading other timeframes with gap fixing for comprehensive analysis...")
        print("   Note: No features will be generated - only data loading and gap fixing.")
        
        # Ask user if they want to load other timeframes
        try:
            load_other_timeframes = input("\nLoad other timeframes with gap fixing? (y/n, default: y): ").strip().lower()
        except EOFError:
            print("\n👋 Goodbye!")
            return {}
        
        if load_other_timeframes not in ['', 'y', 'yes']:
            print("⏭️  Skipping other timeframes loading...")
            return {}
        
        print(f"\n🔧 Loading and fixing gaps in other timeframes...")
        
        # Initialize GapFixer for other timeframes
        try:
            from ..data import GapFixer
            other_gap_fixer = GapFixer(memory_limit_mb=self.memory_manager.max_memory_mb)
            print("✅ GapFixer initialized for other timeframes")
        except Exception as e:
            print(f"❌ Error initializing GapFixer: {e}")
            print("⚠️  Continuing without gap fixing for other timeframes...")
            other_gap_fixer = None
        
        # Store other timeframes data
        other_timeframes_data = {}
        total_timeframes = len(cross_timeframes)
        
        for tf_idx, (tf, files) in enumerate(cross_timeframes.items(), 1):
            print(f"\n📁 Processing {tf} timeframe ({len(files)} files) [{tf_idx}/{total_timeframes}]")
            tf_data = []
            
            for file_idx, file in enumerate(files, 1):
                try:
                    print(f"   📊 Loading {file.name} [{file_idx}/{len(files)}]...")
                    print(f"      🔄 Progress: Starting...", end="", flush=True)
                    df = self.data_loader.load_data_from_file(str(file))
                    print(f"\r      ✅ Loaded: {file.name} ({df.shape[0]:,} rows)")
                    df['source_file'] = file.name
                    df['timeframe'] = tf
                    
                    # Gap fixing for this file
                    if other_gap_fixer:
                        try:
                            timestamp_col = other_gap_fixer.utils.find_timestamp_column(df)
                            if timestamp_col:
                                gap_info = other_gap_fixer.utils.detect_gaps(df, timestamp_col)
                                if gap_info['has_gaps']:
                                    print(f"      ⚠️  Found {gap_info['gap_count']:,} gaps, fixing with auto algorithm...")
                                    print(f"         🔧 Gap fixing progress: Starting...", end="", flush=True)
                                    # Use the apply_algorithm method from GapFixingStrategy
                                    fixed_df = other_gap_fixer.algorithms.apply_algorithm(df, 'auto', gap_info)
                                    results = {
                                        'algorithm_used': 'auto',
                                        'gaps_fixed': gap_info['gap_count'],
                                        'memory_used_mb': 0.0  # Placeholder
                                    }
                                    print(f"\r         ✅ Gap fixing completed")
                                    if fixed_df is not None:
                                        df = fixed_df
                                        del fixed_df
                                        self.memory_manager.optimize_memory()
                                    else:
                                        print(f"         ❌ Gap fixing failed, keeping original data")
                                else:
                                    print(f"      ✅ No gaps found")
                            else:
                                print(f"      ⚠️  No timestamp column found, skipping gap fixing")
                        except Exception as e:
                            print(f"      ❌ Error during gap fixing: {e}")
                            print(f"      💡 Continuing with original data...")
                    
                    tf_data.append(df)
                    
                except Exception as e:
                    print(f"      ❌ Error loading {file.name}: {e}")
                    continue
                
                # Memory management
                self.memory_manager.optimize_memory()
            
            if tf_data:
                # Combine files for this timeframe
                combined_tf_data = pd.concat(tf_data, ignore_index=True)
                other_timeframes_data[tf] = combined_tf_data
                print(f"   ✅ {tf} timeframe: {combined_tf_data.shape[0]:,} rows, {combined_tf_data.shape[1]} columns")
                
                # Memory cleanup
                for df in tf_data:
                    del df
                del tf_data
                self.memory_manager.optimize_memory()
            else:
                print(f"   ❌ No data loaded for {tf} timeframe")
        
        return other_timeframes_data
    
    def create_timeframe_info(self, base_timeframe: str, timeframe_data: Dict[str, List[Path]], 
                            cross_timeframes: Dict[str, List[Path]], mask: str, folder_path: Path) -> Dict:
        """
        Create timeframe information dictionary.
        
        Args:
            base_timeframe: Selected base timeframe
            timeframe_data: All available timeframes
            cross_timeframes: Cross-timeframe data
            mask: Filter mask used
            folder_path: Path to data folder
            
        Returns:
            Dictionary with timeframe information
        """
        return {
            'base_timeframe': base_timeframe,
            'available_timeframes': timeframe_data,
            'cross_timeframes': cross_timeframes,
            'mask_used': mask if mask else None,
            'folder_path': str(folder_path)
        }
    
    def display_data_location_summary(self, system, base_timeframe: str, folder_path: Path, mask: str = None):
        """
        Display summary of where data is located.
        
        Args:
            system: InteractiveSystem instance
            base_timeframe: Selected base timeframe
            folder_path: Path to data folder
            mask: Optional filter mask
        """
        print(f"\n📊 DATA LOCATION SUMMARY:")
        print("-" * 30)
        print(f"   🎯 Base dataset: system.current_data")
        print(f"      • Shape: {system.current_data.shape[0]:,} rows × {system.current_data.shape[1]} columns")
        print(f"      • Timeframe: {base_timeframe}")
        print(f"      • Source: {folder_path}")
        
        if hasattr(system, 'other_timeframes_data') and system.other_timeframes_data:
            print(f"   🔄 Other timeframes: system.other_timeframes_data")
            for tf, df in system.other_timeframes_data.items():
                print(f"      • {tf}: {df.shape[0]:,} rows × {df.shape[1]} columns")
        
        print(f"   📁 Timeframe info: system.timeframe_info")
        print(f"      • Available: {list(system.timeframe_info['available_timeframes'].keys())}")
        print(f"      • Cross-timeframes: {list(system.timeframe_info['cross_timeframes'].keys())}")
        
        if mask:
            print(f"   🔍 Filter applied: '{mask}'")
