#!/usr/bin/env python3
"""
Main data manager for interactive data operations.
Coordinates data loading, gap analysis, and multi-timeframe processing.
"""

import pandas as pd
import gc
from pathlib import Path
from typing import List, Dict, Optional
from .memory_manager import MemoryManager
from .data_loader import DataLoader
from .gap_analyzer import GapAnalyzer
from .multi_timeframe_manager import MultiTimeframeManager
from .cache_manager import CacheManager


class DataManager:
    """Main data manager coordinating all data operations."""
    
    def __init__(self):
        """Initialize DataManager with all required components."""
        self.memory_manager = MemoryManager()
        self.data_loader = DataLoader(self.memory_manager)
        self.gap_analyzer = GapAnalyzer(self.memory_manager)
        self.multi_timeframe_manager = MultiTimeframeManager(self.memory_manager, self.data_loader)
        self.cache_manager = CacheManager(self.memory_manager)
        self.chunk_size = 50000
        self.enable_memory_optimization = True
        self.max_memory_mb = 6144
    
    def load_data(self, system) -> bool:
        """
        Main data loading entry point.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print("\n📁 LOAD DATA")
        print("-" * 30)
        
        # Multi-Timeframe Loading is the only strategy now
        print("🎯 MULTI-TIMEFRAME LOADING STRATEGY")
        print("-" * 50)
        print("🎯 This method loads and prepares data by properly handling")
        print("   multiple timeframes (M1, M5, M15, M30, H1, H4, D1, W1, MN1) as separate datasets")
        print("   and fixing time series gaps before combining.")
        print("-" * 50)
        
        # Go directly to multi-timeframe loading
        return self.load_multi_timeframe_data(system)
    
    def load_multi_timeframe_data(self, system) -> bool:
        """
        Load data with proper multi-timeframe strategy.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print("\n📁 LOAD MULTI-TIMEFRAME DATA")
        print("-" * 50)
        print("🎯 This method loads and prepares data by properly handling")
        print("   multiple timeframes (M1, M5, M15, M30, H1, H4, D1, W1, MN1) as separate datasets")
        print("   and fixing time series gaps before combining.")
        print("-" * 50)
        
        # Get all subfolders in data directory
        data_folder = Path("data")
        if not data_folder.exists():
            print("❌ Data folder not found. Please ensure 'data' folder exists.")
            return False
        
        # Create cache directories
        self.cache_manager.create_cache_directories(data_folder)
        
        # Find subfolders
        subfolders = self.cache_manager.find_data_subfolders(data_folder)
        
        # Display folder selection
        self.cache_manager.display_folder_selection(subfolders)
        
        try:
            input_text = input("Enter folder number or path (with optional mask): ").strip()
        except EOFError:
            print("\n👋 Goodbye!")
            return False
        
        # Parse input
        folder_path, mask = self.cache_manager.parse_folder_input(input_text, subfolders)
        
        if folder_path == Path("CLEAR_CACHE"):
            return self.cache_manager.clear_cache(system)
        elif folder_path == Path("BACK"):
            return False
        elif folder_path is None:
            return False
        
        print(f"\n📁 Selected folder: {folder_path}")
        if mask:
            print(f"🔍 Filter mask: '{mask}'")
        
        # Organize files by timeframe
        timeframe_data = self.multi_timeframe_manager.organize_files_by_timeframe(folder_path, mask)
        
        if not timeframe_data:
            if mask:
                print(f"❌ No files found matching mask '{mask}' in {folder_path}")
            else:
                print(f"❌ No data files found in {folder_path}")
            return False
        
        # Display timeframe summary
        self.multi_timeframe_manager.display_timeframe_summary(timeframe_data, mask)
        
        # Select base timeframe
        base_timeframe = self.multi_timeframe_manager.select_base_timeframe(timeframe_data)
        if base_timeframe is None:
            return False
        
        # Load base timeframe data
        base_data = self.multi_timeframe_manager.load_base_timeframe_data(timeframe_data, base_timeframe)
        
        if not base_data:
            print("❌ No base timeframe data could be loaded")
            return False
        
        # Time Series Gap Analysis and Fixing for each file separately
        print(f"\n🔧 TIME SERIES GAP ANALYSIS & FIXING")
        print("-" * 50)
        print("💡 Analyzing and fixing time series gaps in each file before combining...")
        print("   This ensures data quality and prevents issues during ML model training.")
        
        # Ask user if they want to fix gaps
        try:
            fix_gaps = input("\nFix time series gaps in each file? (y/n, default: y): ").strip().lower()
        except EOFError:
            print("\n👋 Goodbye!")
            return False
        
        if fix_gaps in ['', 'y', 'yes']:
            print(f"\n🔧 Starting gap analysis and fixing for {len(base_data)} files...")
            
            # Initialize GapFixer
            try:
                from ..data import GapFixer
                gap_fixer = GapFixer(memory_limit_mb=self.max_memory_mb)
                print("✅ GapFixer initialized successfully")
            except Exception as e:
                print(f"❌ Error initializing GapFixer: {e}")
                print("⚠️  Continuing without gap fixing...")
                gap_fixer = None
            
            if gap_fixer:
                # Process each file separately
                for i, df in enumerate(base_data):
                    file_name = df['source_file'].iloc[0] if 'source_file' in df.columns else f"file_{i+1}"
                    print(f"\n📁 Processing file {i+1}/{len(base_data)}: {file_name}")
                    
                    try:
                        # Find timestamp column
                        timestamp_col = gap_fixer._find_timestamp_column(df)
                        
                        if timestamp_col:
                            if timestamp_col == "DATETIME_INDEX":
                                print(f"   📅 Found DatetimeIndex: {df.index.name or 'unnamed'}")
                            else:
                                print(f"   📅 Found timestamp column: {timestamp_col}")
                            
                            # Detect gaps
                            gap_info = gap_fixer._detect_gaps(df, timestamp_col)
                            
                            if gap_info['has_gaps']:
                                print(f"   ⚠️  Found {gap_info['gap_count']:,} gaps, fixing...")
                                
                                # Ask user for algorithm choice
                                print(f"   🔧 Available algorithms: auto, linear, cubic, interpolate, forward_fill, backward_fill")
                                try:
                                    algo_choice = input(f"   Select algorithm (default: auto): ").strip().lower()
                                    if algo_choice == '':
                                        algorithm = 'auto'
                                    elif algo_choice in ['auto', 'linear', 'cubic', 'interpolate', 'forward_fill', 'backward_fill']:
                                        algorithm = algo_choice
                                    else:
                                        print(f"   ⚠️  Invalid choice, using 'auto'")
                                        algorithm = 'auto'
                                except EOFError:
                                    algorithm = 'auto'
                                
                                print(f"   🔧 Using algorithm: {algorithm}")
                                
                                # Fix gaps with progress
                                print(f"   🔧 Gap fixing progress: Starting...", end="", flush=True)
                                fixed_df, results = gap_fixer._fix_gaps_in_dataframe(
                                    df, timestamp_col, gap_info, algorithm, show_progress=True
                                )
                                print(f"\r   ✅ Gap fixing completed")
                                
                                if fixed_df is not None:
                                    print(f"   ✅ Gaps fixed successfully!")
                                    print(f"      • Algorithm used: {results['algorithm_used']}")
                                    print(f"      • Gaps fixed: {results['gaps_fixed']:,}")
                                    print(f"      • Processing time: {results['processing_time']:.2f}s")
                                    print(f"      • Memory used: {results['memory_used_mb']:.1f}MB")
                                    
                                    # Replace original dataframe with fixed one
                                    base_data[i] = fixed_df
                                    
                                    # Memory cleanup
                                    del fixed_df
                                    gc.collect()
                                else:
                                    print(f"   ❌ Gap fixing failed, keeping original data")
                            else:
                                print(f"   ✅ No gaps found, file is clean")
                        else:
                            print(f"   ⚠️  No timestamp column found, skipping gap fixing")
                        
                    except Exception as e:
                        print(f"   ❌ Error processing {file_name}: {e}")
                        print(f"   💡 Continuing with original data...")
                        continue
                    
                    # Memory management
                    if self.enable_memory_optimization:
                        gc.collect()
                
                print(f"\n✅ Gap analysis and fixing completed for all files!")
            else:
                print("⚠️  Skipping gap fixing due to initialization error")
        else:
            print("⏭️  Skipping time series gap fixing...")
        
        # Create timeframe_info before using it
        cross_timeframes = {tf: files for tf, files in timeframe_data.items() if tf != base_timeframe}
        system.timeframe_info = self.multi_timeframe_manager.create_timeframe_info(
            base_timeframe, timeframe_data, cross_timeframes, mask, folder_path
        )
        
        # Load other timeframes if available
        if cross_timeframes:
            other_timeframes_data = self.multi_timeframe_manager.load_other_timeframes(cross_timeframes)
            if other_timeframes_data:
                system.other_timeframes_data = other_timeframes_data
        
        # Combine base timeframe data
        print(f"\n🔄 Combining base timeframe data...")
        system.current_data = pd.concat(base_data, ignore_index=True)
        
        # Display completion summary
        print(f"✅ Base dataset created: {system.current_data.shape[0]:,} rows, {system.current_data.shape[1]} columns")
        print(f"   Folder: {folder_path}")
        if mask:
            print(f"   Filter applied: '{mask}'")
        
        # Show information about available timeframes (no feature generation)
        if system.timeframe_info['cross_timeframes']:
            print(f"\n📊 AVAILABLE TIMEFRAMES")
            print("-" * 30)
            print("💡 Other timeframes found (available for separate analysis):")
            for tf, files in system.timeframe_info['cross_timeframes'].items():
                print(f"   • {tf}: {len(files)} files")
            print("   💡 Use 'Feature Engineering' menu to generate features from these timeframes")
        
        # Display data location summary
        self.multi_timeframe_manager.display_data_location_summary(
            system, base_timeframe, folder_path, mask
        )
        
        return True
    
    def analyze_time_series_gaps(self, data_files: List[Path], Fore, Style) -> List[Dict]:
        """
        Analyze time series gaps in data files.
        
        Args:
            data_files: List of file paths to analyze
            Fore: Colorama Fore object
            Style: Colorama Style object
            
        Returns:
            List of gap analysis results
        """
        return self.gap_analyzer.analyze_time_series_gaps(data_files, Fore, Style)
    
    def show_detailed_gap_info(self, gap_summary: List[Dict], Fore, Style):
        """
        Show detailed gap information.
        
        Args:
            gap_summary: List of gap analysis results
            Fore: Colorama Fore object
            Style: Colorama Style object
        """
        self.gap_analyzer.show_detailed_gap_info(gap_summary, Fore, Style)
    
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
        return self.gap_analyzer.fix_gaps_interactive(gap_summary, Fore, Style)
    
    def export_results(self, system) -> bool:
        """
        Export current results to file.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.cache_manager.export_results(system)
    
    def clear_cache(self, system) -> bool:
        """
        Clear all cached files.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.cache_manager.clear_cache(system)
    
    def restore_from_backup(self, system) -> bool:
        """
        Restore data from backup.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.cache_manager.restore_from_backup(system)
    
    def clear_data_backup(self, system) -> bool:
        """
        Clear data backup files.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.cache_manager.clear_data_backup(system)
