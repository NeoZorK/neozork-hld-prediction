#!/usr/bin/env python3
"""
Main data manager for interactive data operations.
Coordinates data loading, gap analysis, and multi-timeframe processing.
"""

import pandas as pd
import gc
import time
from pathlib import Path
from typing import List, Dict, Optional
from tqdm import tqdm
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
        
        # Create cleaned data directory
        self.cleaned_data_dir = Path("data/cleaned_data")
        self.cleaned_data_dir.mkdir(exist_ok=True)
    
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
                # Create overall progress bar for gap analysis and fixing
                total_files = len(base_data)
                overall_start_time = time.time()
                
                print(f"   📊 Overall progress: Starting gap analysis and fixing for {total_files} files...")
                
                # Process each file separately with progress bar and ETA
                for i, df in enumerate(base_data):
                    file_name = df['source_file'].iloc[0] if 'source_file' in df.columns else f"file_{i+1}"
                    
                    # Calculate overall progress and ETA
                    elapsed_time = time.time() - overall_start_time
                    if elapsed_time > 0 and i > 0:
                        avg_time_per_file = elapsed_time / i
                        remaining_files = total_files - i
                        eta_seconds = remaining_files * avg_time_per_file
                        
                        # Format ETA
                        if eta_seconds < 60:
                            eta_str = f"{eta_seconds:.0f}s"
                        elif eta_seconds < 3600:
                            eta_str = f"{eta_seconds/60:.0f}m {eta_seconds%60:.0f}s"
                        else:
                            eta_str = f"{eta_seconds/3600:.0f}h {(eta_seconds%3600)/60:.0f}m"
                        
                        # Calculate speed (files per second)
                        speed = i / elapsed_time
                        
                        print(f"\n📁 Processing file {i+1}/{total_files}: {file_name}")
                        print(f"   📈 Overall progress: {(i/total_files)*100:.1f}% ({i+1}/{total_files} files) "
                              f"🚀 {speed:.2f} files/s ⏱️ ETA: {eta_str}")
                    else:
                        print(f"\n📁 Processing file {i+1}/{total_files}: {file_name}")
                    
                    try:
                        # Find timestamp column (only once)
                        timestamp_col = gap_fixer.utils.find_timestamp_column(df)
                        
                        if timestamp_col:
                            # Detect gaps (only once)
                            gap_info = gap_fixer.utils.detect_gaps(df, timestamp_col)
                            
                            if gap_info['has_gaps']:
                                print(f"   ⚠️  Found {gap_info['gap_count']:,} gaps, fixing...")
                                
                                # Ask user for algorithm choice
                                print(f"   🔧 Available algorithms: auto, linear, cubic, interpolate, forward_fill, backward_fill")
                                try:
                                    algo_choice = input(f"   Select algorithm (default: auto): ").strip().lower()
                                    if algo_choice == '':
                                        algorithm = 'auto'
                                    elif algo_choice in ['auto', 'linear', 'cubic', 'interpolate', 'forward_fill', 'backward_fill']:
                                        algorithm = 'auto'
                                    else:
                                        print(f"   ⚠️  Invalid choice, using 'auto'")
                                        algorithm = 'auto'
                                except EOFError:
                                    algorithm = 'auto'
                                
                                print(f"   🔧 Using algorithm: {algorithm}")
                                
                                # Fix gaps with progress bar and ETA
                                file_start_time = time.time()
                                print(f"   🔧 Gap fixing progress: ", end="", flush=True)
                                
                                # Create progress bar for gap fixing
                                with tqdm(total=gap_info['gap_count'], desc="Fixing gaps", unit="gap") as pbar:
                                    # Use the apply_algorithm method from GapFixingStrategy
                                    fixed_df = gap_fixer.algorithms.apply_algorithm(df, algorithm, gap_info)
                                    results = {
                                        'algorithm_used': algorithm,
                                        'gaps_fixed': gap_info['gap_count'],
                                        'memory_used_mb': 0.0  # Placeholder
                                    }
                                
                                file_end_time = time.time()
                                file_processing_time = file_end_time - file_start_time
                                
                                if fixed_df is not None:
                                    print(f"\r   ✅ Gap fixing completed in {file_processing_time:.2f}s")
                                    print(f"      • Algorithm used: {results['algorithm_used']}")
                                    print(f"      • Gaps fixed: {results['gaps_fixed']:,}")
                                    print(f"      • Processing time: {file_processing_time:.2f}s")
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
                
                # Final overall progress summary
                total_time = time.time() - overall_start_time
                final_speed = total_files / total_time if total_time > 0 else 0
                print(f"\n✅ Gap analysis and fixing completed for all files!")
                print(f"   📊 Summary: {total_files} files processed in {total_time:.2f}s")
                print(f"   🚀 Average speed: {final_speed:.2f} files/s")
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
        
        # Ask user if they want to save cleaned data
        try:
            save_cleaned = input("\n💾 Save cleaned data to 'data/cleaned_data' folder for future ML use? (y/n, default: y): ").strip().lower()
        except EOFError:
            save_cleaned = 'y'
        
        if save_cleaned in ['', 'y', 'yes']:
            self._save_cleaned_data(system, folder_path, mask, base_timeframe)
        
        return True
    
    def _save_cleaned_data(self, system, folder_path, mask, base_timeframe):
        """
        Save cleaned data to the cleaned_data folder for future ML use.
        
        Args:
            system: InteractiveSystem instance
            folder_path: Path to the original data folder
            mask: Filter mask used
            base_timeframe: Base timeframe used
        """
        try:
            print(f"\n💾 SAVING CLEANED DATA FOR ML USE")
            print("-" * 50)
            
            # Create filename based on folder and mask
            folder_name = folder_path.name
            mask_suffix = f"_{mask}" if mask else ""
            timeframe_suffix = f"_{base_timeframe}" if base_timeframe else ""
            
            # Generate filename
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"cleaned_{folder_name}{mask_suffix}{timeframe_suffix}_{timestamp}.parquet"
            filepath = self.cleaned_data_dir / filename
            
            # Save data
            print(f"📁 Saving to: {filepath}")
            system.current_data.to_parquet(filepath, index=False, compression='snappy')
            
            # Get file size
            file_size_mb = filepath.stat().st_size / (1024 * 1024)
            
            print(f"✅ Cleaned data saved successfully!")
            print(f"   📊 File: {filename}")
            print(f"   💾 Size: {file_size_mb:.1f} MB")
            print(f"   📈 Rows: {len(system.current_data):,}")
            print(f"   🔢 Columns: {len(system.current_data.columns)}")
            print(f"   📅 Timeframe: {base_timeframe}")
            print(f"   🎯 Format: Parquet (optimized for ML)")
            
            # Show ML benefits
            print(f"\n🚀 ML MODEL BENEFITS:")
            print(f"   • Fast loading with pandas/pyarrow")
            print(f"   • Efficient memory usage")
            print(f"   • Column-oriented storage")
            print(f"   • Built-in compression")
            print(f"   • Compatible with all major ML libraries")
            print(f"   • No need to re-process data each time")
            
            # Create metadata file
            metadata_file = filepath.with_suffix('.json')
            metadata = {
                'original_folder': str(folder_path),
                'mask_applied': mask,
                'base_timeframe': base_timeframe,
                'creation_timestamp': timestamp,
                'data_shape': list(system.current_data.shape),
                'columns': list(system.current_data.columns),
                'data_types': system.current_data.dtypes.to_dict(),
                'memory_usage_mb': system.current_data.memory_usage(deep=True).sum() / (1024 * 1024),
                'description': 'Cleaned data ready for ML model training and prediction'
            }
            
            import json
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            print(f"📋 Metadata saved: {metadata_file.name}")
            
        except Exception as e:
            print(f"❌ Error saving cleaned data: {e}")
            print("💡 Data will not be saved, but you can continue working with it in memory")
    
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
    
    def load_data_from_file(self, file_path: str) -> pd.DataFrame:
        """
        Load data from file path.
        
        Args:
            file_path: Path to the file
            
        Returns:
            DataFrame with loaded data
        """
        return self.data_loader.load_data_from_file(file_path)
    
    def load_data_from_folder(self, folder_path: str) -> list:
        """
        Load data files from folder path.
        
        Args:
            folder_path: Path to the folder
            
        Returns:
            List of loaded DataFrames
        """
        return self.data_loader.load_data_from_folder(folder_path)
    
    def restore_from_backup(self, system) -> bool:
        """
        Restore data from backup file.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.cache_manager.restore_from_backup(system)
    
    def clear_data_backup(self, system) -> bool:
        """
        Clear all backup files from the backup directory.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.cache_manager.clear_data_backup(system)
    
    def export_results(self, system) -> None:
        """
        Export current results to files.
        
        Args:
            system: InteractiveSystem instance
        """
        self.cache_manager.export_results(system)
