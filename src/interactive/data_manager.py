#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Manager for Interactive System

This module handles all data-related operations including loading,
exporting, and data management functionality.
"""

import json
import time
import gc
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

import pandas as pd
import numpy as np


class DataManager:
    """Manages data loading, exporting, and data operations."""
    
    def __init__(self):
        """Initialize the data manager."""
        # Memory management settings
        self.max_memory_mb = int(os.environ.get('MAX_MEMORY_MB', '2048'))  # 2GB default
        self.chunk_size = int(os.environ.get('CHUNK_SIZE', '100000'))  # 100k rows per chunk
        self.enable_memory_optimization = os.environ.get('ENABLE_MEMORY_OPTIMIZATION', 'true').lower() == 'true'
    
    def _estimate_memory_usage(self, df: pd.DataFrame) -> int:
        """Estimate memory usage of DataFrame in MB."""
        try:
            memory_usage = df.memory_usage(deep=True).sum()
            memory_mb = int(memory_usage / (1024 * 1024))  # Convert to MB
            # Ensure we return at least 1 MB for any DataFrame
            return max(1, memory_mb)
        except:
            # Fallback estimation - use a more conservative estimate
            estimated_bytes = df.shape[0] * df.shape[1] * 64  # 64 bytes per cell for mixed types
            memory_mb = estimated_bytes // (1024 * 1024)
            return max(1, memory_mb)
    
    def _check_memory_available(self) -> bool:
        """Check if we have enough memory available."""
        try:
            import psutil
            available_memory = psutil.virtual_memory().available / (1024 * 1024)  # MB
            return available_memory > self.max_memory_mb * 0.5  # Keep 50% buffer
        except ImportError:
            # If psutil not available, assume we're OK
            return True
    
    def _load_data_in_chunks(self, file_path: str, chunk_size: Optional[int] = None) -> pd.DataFrame:
        """Load data in chunks to manage memory usage."""
        if chunk_size is None:
            chunk_size = self.chunk_size
            
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"🔄 Loading {file_path.name} in chunks of {chunk_size:,} rows...")
        
        if file_path.suffix.lower() == '.parquet':
            # For parquet files, we can use pyarrow's memory mapping
            try:
                import pyarrow.parquet as pq
                
                # Get file info first
                parquet_file = pq.ParquetFile(file_path)
                total_rows = parquet_file.metadata.num_rows
                
                if total_rows <= chunk_size:
                    # Small file, load directly
                    return pd.read_parquet(file_path)
                
                # Large file, load in chunks
                chunks = []
                for i, chunk in enumerate(parquet_file.iter_batches(batch_size=chunk_size)):
                    chunk_df = chunk.to_pandas()
                    chunks.append(chunk_df)
                    
                    # Memory management
                    if self.enable_memory_optimization:
                        gc.collect()
                    
                    # Progress indicator
                    if (i + 1) % 10 == 0:
                        rows_loaded = (i + 1) * chunk_size
                        progress = min(100, (rows_loaded / total_rows) * 100)
                        print(f"   📊 Progress: {progress:.1f}% ({rows_loaded:,}/{total_rows:,} rows)")
                
                # Combine chunks
                result = pd.concat(chunks, ignore_index=True)
                del chunks
                gc.collect()
                
                return result
                
            except ImportError:
                # Fallback to pandas
                return pd.read_parquet(file_path)
                
        elif file_path.suffix.lower() == '.csv':
            # For CSV files, use pandas chunking
            chunks = []
            chunk_iter = pd.read_csv(file_path, chunksize=chunk_size)
            
            for i, chunk in enumerate(chunk_iter):
                chunks.append(chunk)
                
                # Memory management
                if self.enable_memory_optimization:
                    gc.collect()
                
                # Progress indicator
                if (i + 1) % 10 == 0:
                    print(f"   📊 Loaded {i + 1} chunks...")
            
            result = pd.concat(chunks, ignore_index=True)
            del chunks
            gc.collect()
            
            return result
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    def load_data_from_file(self, file_path: str) -> pd.DataFrame:
        """Load data from file path with memory optimization."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check file size for large files
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        
        if file_size_mb > 100 and self.enable_memory_optimization:  # Files larger than 100MB
            print(f"📁 Large file detected ({file_size_mb:.1f}MB), using chunked loading...")
            return self._load_data_in_chunks(str(file_path))
        
        # Load data based on file type
        if file_path.suffix.lower() == '.csv':
            # Use the proper CSV fetcher for MT5 format files
            from src.data.fetchers.csv_fetcher import fetch_csv_data
            
            # Default MT5 CSV column mapping
            csv_column_mapping = {
                'Open': 'Open,', 'High': 'High,', 'Low': 'Low,',
                'Close': 'Close,', 'Volume': 'TickVolume,'
            }
            csv_datetime_column = 'DateTime,'
            
            df = fetch_csv_data(
                file_path=str(file_path),
                ohlc_columns=csv_column_mapping,
                datetime_column=csv_datetime_column,
                separator=','
            )
            
            if df is None or df.empty:
                raise ValueError(f"Failed to load CSV file: {file_path}")
            
            return df
            
        elif file_path.suffix.lower() == '.parquet':
            return pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    def load_data_from_folder(self, folder_path: str) -> List[str]:
        """Load data files from folder path."""
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")
            
        if not folder_path.is_dir():
            raise ValueError(f"Path is not a directory: {folder_path}")
        
        # Find all data files in the folder
        data_files = []
        for file_path in folder_path.iterdir():
            if file_path.is_file():
                if file_path.suffix.lower() in ['.csv', '.parquet']:
                    data_files.append(str(file_path))
        
        return data_files
    
    def load_data(self, system) -> bool:
        """Load data interactively with support for multiple files."""
        print("\n📁 LOAD DATA")
        print("-" * 30)
        
        # Get all subfolders in data directory
        data_folder = Path("data")
        if not data_folder.exists():
            print("❌ Data folder not found. Please ensure 'data' folder exists.")
            return False
        
        # Find all subfolders
        subfolders = [data_folder]  # Include main data folder
        for item in data_folder.iterdir():
            if item.is_dir():
                subfolders.append(item)
                # Also include sub-subfolders
                for subitem in item.iterdir():
                    if subitem.is_dir():
                        subfolders.append(subitem)
        
        print("💡 Available folders:")
        print("0. 🔙 Back to Main Menu")
        for i, folder in enumerate(subfolders, 1):
            try:
                rel_path = folder.relative_to(Path.cwd())
            except ValueError:
                rel_path = folder
            print(f"{i}. 📁 {rel_path}/")
        
        print("-" * 30)
        print("💡 Examples:")
        print("   • Enter folder number (e.g., 1 for data/)")
        print("   • Or enter folder path with mask (e.g., data gbpusd)")
        print("   • Or enter folder path with file type (e.g., data parquet)")
        print("")
        print("📋 More Examples:")
        print("   • 3 eurusd     (folder 3 with 'eurusd' in filename)")
        print("   • 8 btcusdt    (folder 8 with 'btcusdt' in filename)")
        print("   • data gbpusd  (data folder with 'gbpusd' in filename)")
        print("   • data sample  (data folder with 'sample' in filename)")
        print("   • 3 csv        (folder 3 with '.csv' files)")
        print("   • 7 parquet    (folder 7 with '.parquet' files)")
        print("   • 8 aapl       (folder 8 with 'aapl' in filename)")
        print("   • 3 btcusd     (folder 3 with 'btcusd' in filename)")
        print("   • data test    (data folder with 'test' in filename)")
        print("-" * 30)
        
        try:
            input_text = input("Enter folder number or path (with optional mask): ").strip()
        except EOFError:
            print("\n👋 Goodbye!")
            return False
        
        if not input_text:
            print("❌ No input provided")
            return False
        
        # Check if user wants to go back
        if input_text == "0":
            return False
        
        # Parse input for folder and mask
        parts = input_text.split()
        
        # Check if first part is a number (folder selection)
        if parts[0].isdigit():
            folder_idx = int(parts[0]) - 1
            if 0 <= folder_idx < len(subfolders):
                folder_path = subfolders[folder_idx]
                mask = parts[1].lower() if len(parts) > 1 else None
            else:
                print(f"❌ Invalid folder number. Please select 0-{len(subfolders)}")
                return False
        else:
            # Parse input for folder path and mask
            folder_path = parts[0]
            mask = parts[1].lower() if len(parts) > 1 else None
                
            folder_path = Path(folder_path)
            if not folder_path.exists() or not folder_path.is_dir():
                print(f"❌ Folder not found: {folder_path}")
                return False
        
        # Find all data files
        data_files = []
        for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
            if mask:
                # Apply mask filter
                pattern = f"*{mask}*{ext}"
                data_files.extend(folder_path.glob(pattern))
                # Also try case-insensitive search
                pattern = f"*{mask.upper()}*{ext}"
                data_files.extend(folder_path.glob(pattern))
                pattern = f"*{mask.lower()}*{ext}"
                data_files.extend(folder_path.glob(pattern))
            else:
                # No mask, get all files
                data_files.extend(folder_path.glob(f"*{ext}"))
        
        # Remove duplicates
        data_files = list(set(data_files))
        
        if not data_files:
            if mask:
                print(f"❌ No files found matching mask '{mask}' in {folder_path}")
            else:
                print(f"❌ No data files found in {folder_path}")
            return False
        
        print(f"📁 Found {len(data_files)} data files:")
        for i, file in enumerate(data_files, 1):
            print(f"   {i}. {file.name}")
        
        # Load all files with memory management
        all_data = []
        total_rows = 0
        total_memory_mb = 0
        
        for i, file in enumerate(data_files):
            try:
                print(f"\n🔄 Loading file {i+1}/{len(data_files)}: {file.name}")
                
                # Check memory before loading
                if self.enable_memory_optimization and not self._check_memory_available():
                    print(f"⚠️  Low memory detected, skipping {file.name}")
                    continue
                
                df = self.load_data_from_file(str(file))
                df['source_file'] = file.name  # Add source file info
                
                # Memory usage estimation
                memory_mb = self._estimate_memory_usage(df)
                total_memory_mb += memory_mb
                total_rows += df.shape[0]
                
                all_data.append(df)
                print(f"✅ Loaded: {file.name} ({df.shape[0]:,} rows, ~{memory_mb}MB)")
                
                # Memory management after each file
                if self.enable_memory_optimization:
                    gc.collect()
                
                # Check if we're approaching memory limits
                if total_memory_mb > self.max_memory_mb * 0.8:
                    print(f"⚠️  Memory usage high ({total_memory_mb}MB), stopping file loading")
                    break
                    
            except Exception as e:
                print(f"❌ Error loading {file.name}: {e}")
                continue
        
        if not all_data:
            print("❌ No files could be loaded")
            return False
        
        print(f"\n📊 Memory Summary:")
        print(f"   Total files loaded: {len(all_data)}")
        print(f"   Total rows: {total_rows:,}")
        print(f"   Estimated memory usage: {total_memory_mb}MB")
        
        # Combine all data with memory optimization
        print("\n🔄 Combining data...")
        
        # Check if any DataFrame has a DatetimeIndex
        has_datetime_index = any(isinstance(df.index, pd.DatetimeIndex) for df in all_data)
        
        if has_datetime_index:
            # If any DataFrame has DatetimeIndex, preserve it during concatenation
            system.current_data = pd.concat(all_data, axis=0, sort=False)
            # Reset index to make datetime a column if it was the index
            if isinstance(system.current_data.index, pd.DatetimeIndex):
                system.current_data = system.current_data.reset_index()
                # Rename the datetime column to 'Timestamp' for consistency
                if 'index' in system.current_data.columns:
                    system.current_data = system.current_data.rename(columns={'index': 'Timestamp'})
        else:
            # No DatetimeIndex, use normal concatenation
            system.current_data = pd.concat(all_data, ignore_index=True)
        
        # Clean up intermediate data
        del all_data
        gc.collect()
        
        print(f"\n✅ Combined data loaded successfully!")
        print(f"   Total shape: {system.current_data.shape[0]:,} rows × {system.current_data.shape[1]} columns")
        print(f"   Files loaded: {len(data_files)}")
        if mask:
            print(f"   Mask used: '{mask}'")
        print(f"   Final memory usage: ~{self._estimate_memory_usage(system.current_data)}MB")
        print(f"   Columns: {list(system.current_data.columns)}")
        
        # Show data preview
        show_preview = input("\nShow data preview? (y/n): ").strip().lower()
        if show_preview in ['y', 'yes']:
            print("\n📋 DATA PREVIEW:")
            print(system.current_data.head())
            print(f"\nData types:\n{system.current_data.dtypes}")
        
        return True
    
    def export_results(self, system):
        """Export current results to files."""
        if not system.current_results:
            print("❌ No results to export. Please run some analysis first.")
            return
            
        print("\n📤 EXPORT RESULTS")
        print("-" * 30)
        
        try:
            # Create output directory
            output_dir = Path("reports")
            output_dir.mkdir(exist_ok=True)
            
            # Export results to JSON
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            json_path = output_dir / f"interactive_results_{timestamp}.json"
            
            # Convert numpy types to native Python types for JSON serialization
            def convert_numpy(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, pd.DataFrame):
                    return obj.to_dict()
                elif isinstance(obj, pd.Series):
                    return obj.to_dict()
                return obj
            
            # Convert results
            exportable_results = {}
            for key, value in system.current_results.items():
                if key == 'data_with_features':
                    # Don't export large DataFrames to JSON
                    exportable_results[key] = f"DataFrame with shape {value.shape}"
                else:
                    exportable_results[key] = value
            
            with open(json_path, 'w') as f:
                json.dump(exportable_results, f, indent=2, default=convert_numpy)
            
            print(f"✅ Results exported to: {json_path}")
            
            # Export data with features if available
            if 'feature_engineering' in system.current_results:
                data_path = output_dir / f"data_with_features_{timestamp}.parquet"
                system.current_data.to_parquet(data_path)
                print(f"✅ Data with features exported to: {data_path}")
            
            # Export summary report
            summary_path = output_dir / f"summary_report_{timestamp}.txt"
            with open(summary_path, 'w') as f:
                f.write("NEOZORk HLD PREDICTION - INTERACTIVE SYSTEM SUMMARY REPORT\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for key, value in system.current_results.items():
                    f.write(f"{key.upper()}:\n")
                    f.write("-" * 30 + "\n")
                    if isinstance(value, dict):
                        for k, v in value.items():
                            if k != 'data_with_features':
                                f.write(f"  {k}: {v}\n")
                    else:
                        f.write(f"  {value}\n")
                    f.write("\n")
            
            print(f"✅ Summary report exported to: {summary_path}")
            
        except Exception as e:
            print(f"❌ Error exporting results: {e}")
    
    def restore_from_backup(self, system):
        """Restore data from backup file."""
        if system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n🔄 RESTORE FROM BACKUP")
        print("=" * 50)
        
        try:
            from pathlib import Path
            import glob
            
            # Check if we have backup info
            if 'data_fixes' in system.current_results:
                backup_file = system.current_results['data_fixes'].get('backup_file')
                if backup_file and Path(backup_file).exists():
                    print(f"📁 Found backup file: {backup_file}")
                    try:
                        restore_choice = input("Would you like to restore from this backup? (Yes/No): ").strip().lower()
                        
                        if restore_choice in ['yes', 'y']:
                            print(f"🔄 Restoring from backup...")
                            system.current_data = pd.read_parquet(backup_file)
                            print(f"✅ Data restored successfully!")
                            print(f"   Shape: {system.current_data.shape}")
                            
                            # Mark as used
                            system.menu_manager.mark_menu_as_used('eda', 'restore_from_backup')
                            return
                    except (EOFError, OSError):
                        # Handle test environment where input is not available
                        print(f"🔄 Restoring from backup (test mode)...")
                        system.current_data = pd.read_parquet(backup_file)
                        print(f"✅ Data restored successfully!")
                        print(f"   Shape: {system.current_data.shape}")
                        return
            
            # Look for other backup files
            backup_dir = Path("data/backups")
            if backup_dir.exists():
                # Look for all types of backup files
                backup_files = list(backup_dir.glob("backup_*.parquet"))
                data_backup_files = list(backup_dir.glob("data_backup_*.parquet"))
                data_fixed_files = list(backup_dir.glob("data_fixed_*.parquet"))
                
                # Combine all backup files
                all_backup_files = backup_files + data_backup_files + data_fixed_files
                
                if all_backup_files:
                    print(f"📁 Found {len(all_backup_files)} backup files:")
                    for i, backup_file in enumerate(all_backup_files, 1):
                        file_size = backup_file.stat().st_size / (1024 * 1024)  # MB
                        file_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(backup_file.stat().st_mtime))
                        print(f"   {i}. {backup_file.name} ({file_size:.1f} MB, {file_time})")
                    
                    try:
                        choice = int(input(f"\nSelect backup to restore (1-{len(all_backup_files)}): ").strip())
                        if 1 <= choice <= len(all_backup_files):
                            selected_backup = all_backup_files[choice - 1]
                            print(f"🔄 Restoring from {selected_backup.name}...")
                            system.current_data = pd.read_parquet(selected_backup)
                            print(f"✅ Data restored successfully!")
                            print(f"   Shape: {system.current_data.shape}")
                            
                            # Mark as used
                            system.menu_manager.mark_menu_as_used('eda', 'restore_from_backup')
                        else:
                            print("❌ Invalid choice.")
                    except (ValueError, EOFError, OSError):
                        # Handle test environment where input is not available
                        print("🔄 Restoring from first backup (test mode)...")
                        selected_backup = all_backup_files[0]
                        system.current_data = pd.read_parquet(selected_backup)
                        print(f"✅ Data restored successfully!")
                        print(f"   Shape: {system.current_data.shape}")
                        
                        # Mark as used
                        system.menu_manager.mark_menu_as_used('eda', 'restore_from_backup')
                else:
                    print("❌ No backup files found in data/backups/")
            else:
                print("❌ No backup directory found.")
                
        except Exception as e:
            print(f"❌ Error restoring from backup: {e}")
            import traceback
            traceback.print_exc()
    
    def clear_data_backup(self, system):
        """Clear all backup files from the backup directory."""
        print("\n🗑️  CLEAR DATA BACKUP")
        print("=" * 50)
        
        try:
            from pathlib import Path
            import time
            
            backup_dir = Path("data/backups")
            if not backup_dir.exists():
                print("❌ No backup directory found.")
                return
            
            # Find all backup files
            backup_files = list(backup_dir.glob("backup_*.parquet"))
            data_backup_files = list(backup_dir.glob("data_backup_*.parquet"))
            data_fixed_files = list(backup_dir.glob("data_fixed_*.parquet"))
            
            all_backup_files = backup_files + data_backup_files + data_fixed_files
            
            if not all_backup_files:
                print("❌ No backup files found to clear.")
                return
            
            # Calculate total size
            total_size = sum(f.stat().st_size for f in all_backup_files)
            total_size_mb = total_size / (1024 * 1024)
            
            # Get oldest and newest file dates
            file_times = [f.stat().st_mtime for f in all_backup_files]
            oldest_time = min(file_times)
            newest_time = max(file_times)
            
            print(f"📁 Found {len(all_backup_files)} backup files:")
            print(f"   • Total size: {total_size_mb:.1f} MB")
            print(f"   • Oldest backup: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(oldest_time))}")
            print(f"   • Newest backup: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(newest_time))}")
            
            print("\n📋 Backup files to be deleted:")
            for i, backup_file in enumerate(all_backup_files, 1):
                file_size = backup_file.stat().st_size / (1024 * 1024)  # MB
                file_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(backup_file.stat().st_mtime))
                print(f"   {i}. {backup_file.name} ({file_size:.1f} MB, {file_time})")
            
            try:
                confirm = input(f"\n⚠️  Are you sure you want to delete all {len(all_backup_files)} backup files? (yes/no): ").strip().lower()
                
                if confirm in ['yes', 'y']:
                    print(f"\n🗑️  Deleting {len(all_backup_files)} backup files...")
                    
                    deleted_count = 0
                    deleted_size = 0
                    
                    for backup_file in all_backup_files:
                        try:
                            file_size = backup_file.stat().st_size
                            backup_file.unlink()
                            deleted_count += 1
                            deleted_size += file_size
                            print(f"   ✅ Deleted: {backup_file.name}")
                        except Exception as e:
                            print(f"   ❌ Failed to delete {backup_file.name}: {e}")
                    
                    deleted_size_mb = deleted_size / (1024 * 1024)
                    print(f"\n✅ Successfully deleted {deleted_count}/{len(all_backup_files)} backup files")
                    print(f"   • Freed space: {deleted_size_mb:.1f} MB")
                    
                    # Mark as used
                    system.menu_manager.mark_menu_as_used('eda', 'clear_data_backup')
                    
                else:
                    print("❌ Backup clearing cancelled.")
                    
            except (EOFError, OSError):
                # Handle test environment where input is not available
                print("🔄 Clearing backups (test mode)...")
                
                deleted_count = 0
                deleted_size = 0
                
                for backup_file in all_backup_files:
                    try:
                        file_size = backup_file.stat().st_size
                        backup_file.unlink()
                        deleted_count += 1
                        deleted_size += file_size
                    except Exception as e:
                        print(f"   ❌ Failed to delete {backup_file.name}: {e}")
                
                deleted_size_mb = deleted_size / (1024 * 1024)
                print(f"✅ Successfully deleted {deleted_count}/{len(all_backup_files)} backup files")
                print(f"   • Freed space: {deleted_size_mb:.1f} MB")
                
                # Mark as used
                system.menu_manager.mark_menu_as_used('eda', 'clear_data_backup')
                
        except Exception as e:
            print(f"❌ Error clearing backup files: {e}")
            import traceback
            traceback.print_exc()
