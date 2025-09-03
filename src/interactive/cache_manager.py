# -*- coding: utf-8 -*-
# src/interactive/cache_manager.py
#!/usr/bin/env python3
"""
Cache and backup management utilities.
Handles data caching, backup creation, and restoration.
"""

import shutil
import os
from pathlib import Path
from typing import List, Optional, Tuple
from .memory_manager import MemoryManager
import pandas as pd


class CacheManager:
    """Manages data caching and backup operations."""
    
    def __init__(self, memory_manager: MemoryManager):
        """
        Initialize CacheManager.
        
        Args:
            memory_manager: MemoryManager instance
        """
        self.memory_manager = memory_manager
    
    def create_cache_directories(self, data_folder: Path) -> List[Path]:
        """
        Create necessary cache directories.
        
        Args:
            data_folder: Main data folder
            
        Returns:
            List of created cache directories
        """
        cache_dirs = [
            data_folder / "cache",
            data_folder / "cache" / "csv_converted",
            data_folder / "cache" / "uv_cache",
            data_folder / "backups"
        ]
        
        created_dirs = []
        for cache_dir in cache_dirs:
            if not cache_dir.exists():
                cache_dir.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created cache directory: {cache_dir}")
                created_dirs.append(cache_dir)
        
        return created_dirs
    
    def find_data_subfolders(self, data_folder: Path) -> List[Path]:
        """
        Find all subfolders in data directory.
        
        Args:
            data_folder: Main data folder
            
        Returns:
            List of subfolder paths
        """
        subfolders = [data_folder]  # Include main data folder
        
        for item in data_folder.iterdir():
            if item.is_dir():
                # Skip cache folders and mql5_feed to avoid loading cached files
                if 'cache' not in item.name.lower() and item.name != 'mql5_feed':
                    subfolders.append(item)
                    # Also include sub-subfolders (but skip cache and mql5_feed)
                    for subitem in item.iterdir():
                        if subitem.is_dir() and 'cache' not in subitem.name.lower():
                            subfolders.append(subitem)
        
        # Add csv_converted folder specifically if it exists
        csv_converted_folder = data_folder / "cache" / "csv_converted"
        if csv_converted_folder.exists() and csv_converted_folder.is_dir():
            subfolders.append(csv_converted_folder)
        
        # Add mql5_feed folder if it exists
        mql5_feed_folder = Path("mql5_feed")
        if mql5_feed_folder.exists() and mql5_feed_folder.is_dir():
            subfolders.append(mql5_feed_folder)
        
        return subfolders
    
    def display_folder_selection(self, subfolders: List[Path]):
        """
        Display folder selection menu.
        
        Args:
            subfolders: List of available subfolders
        """
        print("💡 Available folders:")
        print("0. 🔙 Back to Main Menu")
        for i, folder in enumerate(subfolders, 1):
            try:
                rel_path = folder.relative_to(Path.cwd())
            except ValueError:
                rel_path = folder
            print(f"{i}. 📁 {rel_path}/")
        
        print("\n💡 Note: Cache directories are excluded from this list")
        print("   ../data/cache/csv_converted is included for loading converted CSV files")
        print("   mql5_feed is included for loading MQL5 data")
        
        print("-" * 30)
        print("💡 Examples:")
        print("   • Enter folder number (e.g., 1 for ../data/)")
        print("   • Or enter folder path with mask (e.g., data eurusd)")
        print("   • Or enter folder path with file type (e.g., data parquet)")
        print("")
        print("📋 More Examples:")
        print("   • 2 eurusd     (folder 2 with 'eurusd' in filename)")
        print("   • 2 gbpusd     (folder 2 with 'gbpusd' in filename)")
        print("   • data sample  (data folder with 'sample' in filename)")
        print("   • 1 csv        (folder 1 with '.csv' files)")
        print("   • 7 parquet    (folder 7 with '.parquet' files)")
        print("   • data test    (data folder with 'test' in filename)")
        print("")
        print("🗑️  Cache Management:")
        print("   • Enter 'clear cache' to clear all cached files")
        print("-" * 30)
    
    def parse_folder_input(self, input_text: str, subfolders: List[Path]) -> Tuple[Optional[Path], Optional[str]]:
        """
        Parse user input for folder selection and mask.
        
        Args:
            input_text: User input string
            subfolders: List of available subfolders
            
        Returns:
            Tuple of (folder_path, mask) or (None, None) if invalid
        """
        input_text = input_text.strip()
        
        # Handle special commands
        if input_text.lower() == 'clear cache':
            return Path("CLEAR_CACHE"), None
        
        # Parse input
        parts = input_text.split()
        
        if not parts:
            return None, None
        
        # Check if first part is a number (folder selection)
        if parts[0].isdigit():
            folder_idx = int(parts[0])
            if folder_idx == 0:
                return Path("BACK"), None
            elif 1 <= folder_idx <= len(subfolders):
                folder_path = subfolders[folder_idx - 1]
                mask = parts[1].lower() if len(parts) > 1 else None
                return folder_path, mask
            else:
                print(f"❌ Invalid folder number. Please select 0-{len(subfolders)}")
                return None, None
        else:
            # Parse input for folder path and mask
            folder_path = parts[0]
            mask = parts[1].lower() if len(parts) > 1 else None
            
            folder_path = Path(folder_path)
            if not folder_path.exists() or not folder_path.is_dir():
                print(f"❌ Folder not found: {folder_path}")
                return None, None
            
            return folder_path, mask
    
    def clear_cache(self, system) -> bool:
        """
        Clear all cached files.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🗑️  CLEAR CACHE")
        print("-" * 30)
        
        try:
            # Find cache directories
            cache_dirs = []
            data_folder = Path("data")
            
            if data_folder.exists():
                cache_dirs.extend([
                    data_folder / "cache",
                    data_folder / "cache" / "csv_converted",
                    data_folder / "cache" / "uv_cache"
                ])
            
            # Count files to be removed
            total_files = 0
            total_size_mb = 0
            
            for cache_dir in cache_dirs:
                if cache_dir.exists():
                    for file_path in cache_dir.rglob("*"):
                        if file_path.is_file():
                            total_files += 1
                            total_size_mb += self.memory_manager.get_file_size_mb(file_path)
            
            if total_files == 0:
                print("✅ No cached files found to remove")
                return True
            
            print(f"📁 Found {total_files:,} cached files ({total_size_mb:.1f}MB)")
            
            # Ask for confirmation
            try:
                confirm = input(f"\nRemove all cached files? (y/n, default: n): ").strip().lower()
                if confirm not in ['y', 'yes']:
                    print("⏭️  Cache clearing cancelled")
                    return False
            except EOFError:
                print("⏭️  Cache clearing cancelled")
                return False
            
            # Remove cache directories
            removed_files = 0
            for cache_dir in cache_dirs:
                if cache_dir.exists():
                    try:
                        shutil.rmtree(cache_dir)
                        print(f"✅ Removed cache directory: {cache_dir}")
                        removed_files += 1
                    except Exception as e:
                        print(f"❌ Error removing {cache_dir}: {e}")
            
            # Recreate empty cache directories
            self.create_cache_directories(data_folder)
            
            print(f"\n✅ Cache clearing completed!")
            print(f"   Removed {removed_files} cache directories")
            print(f"   Freed {total_size_mb:.1f}MB of disk space")
            
            return True
            
        except Exception as e:
            print(f"❌ Error clearing cache: {e}")
            return False
    
    def export_results(self, system) -> bool:
        """
        Export current results to file.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n📤 EXPORT RESULTS")
        print("-" * 30)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data to export")
            return False
        
        try:
            # Get export path
            export_path = input("Enter export file path (e.g., results.csv): ").strip()
            if not export_path:
                print("⏭️  Export cancelled")
                return False
            
            export_path = Path(export_path)
            
            # Determine format from extension
            if export_path.suffix.lower() == '.csv':
                system.current_data.to_csv(export_path, index=False)
                print(f"✅ Data exported to CSV: {export_path}")
            elif export_path.suffix.lower() == '.parquet':
                system.current_data.to_parquet(export_path, index=False)
                print(f"✅ Data exported to Parquet: {export_path}")
            elif export_path.suffix.lower() == '.xlsx':
                system.current_data.to_excel(export_path, index=False)
                print(f"✅ Data exported to Excel: {export_path}")
            else:
                print(f"❌ Unsupported export format: {export_path.suffix}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
            return False
    
    def restore_from_backup(self, system) -> bool:
        """
        Restore data from backup.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n📥 RESTORE FROM BACKUP")
        print("-" * 30)
        
        try:
            # Find backup directory
            backup_dir = Path("../data/backups")
            if not backup_dir.exists():
                print("❌ No backup directory found")
                return False
            
            # List available backups
            backup_files = list(backup_dir.glob("*.parquet"))
            if not backup_files:
                print("❌ No backup files found")
                return False
            
            print(f"📁 Available backups:")
            for i, backup_file in enumerate(backup_files, 1):
                file_size_mb = self.memory_manager.get_file_size_mb(backup_file)
                print(f"   {i}. {backup_file.name} ({file_size_mb:.1f}MB)")
            
            # Select backup
            try:
                choice = input(f"\nSelect backup to restore (1-{len(backup_files)}): ").strip()
                if not choice.isdigit():
                    print("❌ Invalid choice")
                    return False
                
                backup_idx = int(choice) - 1
                if backup_idx < 0 or backup_idx >= len(backup_files):
                    print("❌ Invalid backup selection")
                    return False
                
                selected_backup = backup_files[backup_idx]
                
            except EOFError:
                print("\n👋 Goodbye!")
                return False
            
            # Confirm restoration
            try:
                confirm = input(f"\nRestore from {selected_backup.name}? (y/n, default: n): ").strip().lower()
                if confirm not in ['y', 'yes']:
                    print("⏭️  Restoration cancelled")
                    return False
            except EOFError:
                print("⏭️  Restoration cancelled")
                return False
            
            # Load backup
            print(f"📥 Loading backup: {selected_backup.name}")
            backup_data = pd.read_parquet(selected_backup)
            
            # Restore to system
            system.current_data = backup_data
            
            print(f"✅ Backup restored successfully!")
            print(f"   Shape: {backup_data.shape[0]:,} rows × {backup_data.shape[1]} columns")
            print(f"   Source: {selected_backup}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error restoring backup: {e}")
            return False
    
    def clear_data_backup(self, system) -> bool:
        """
        Clear data backup files.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🗑️  CLEAR DATA BACKUP")
        print("-" * 30)
        
        try:
            # Find backup directory
            backup_dir = Path("../data/backups")
            if not backup_dir.exists():
                print("✅ No backup directory found")
                return True
            
            # Count backup files
            backup_files = list(backup_dir.glob("*.parquet"))
            if not backup_files:
                print("✅ No backup files found")
                return True
            
            total_size_mb = sum(self.memory_manager.get_file_size_mb(f) for f in backup_files)
            print(f"📁 Found {len(backup_files):,} backup files ({total_size_mb:.1f}MB)")
            
            # Ask for confirmation
            try:
                confirm = input(f"\nRemove all backup files? (y/n, default: n): ").strip().lower()
                if confirm not in ['y', 'yes']:
                    print("⏭️  Backup clearing cancelled")
                    return False
            except EOFError:
                print("⏭️  Backup clearing cancelled")
                return False
            
            # Remove backup files
            removed_files = 0
            for backup_file in backup_files:
                try:
                    backup_file.unlink()
                    removed_files += 1
                except Exception as e:
                    print(f"❌ Error removing {backup_file.name}: {e}")
            
            print(f"\n✅ Backup clearing completed!")
            print(f"   Removed {removed_files} backup files")
            print(f"   Freed {total_size_mb:.1f}MB of disk space")
            
            return True
            
        except Exception as e:
            print(f"❌ Error clearing backups: {e}")
            return False
