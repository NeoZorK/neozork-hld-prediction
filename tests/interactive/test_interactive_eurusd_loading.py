#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Interactive EURUSD Loading Issue

This test reproduces the issue with loading EURUSD data through the interactive system
and identifies where the missing timestamps problem occurs.
"""

import os
import pandas as pd
import pytest
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.interactive.data_manager import DataManager
from src.interactive import InteractiveSystem


class TestInteractiveEURUSDLoading:
    """Test interactive EURUSD loading with missing timestamps issue."""
    
    def setup_method(self):
        """Setup method for tests."""
        self.data_manager = DataManager()
        self.system = InteractiveSystem()
        
    def test_eurusd_loading_simulation(self):
        """Simulate the exact user scenario: Load Data -> 8 eurusd."""
        print("🧪 Simulating user scenario: Load Data -> 8 eurusd")
        print("=" * 60)
        
        # Simulate the folder selection logic
        data_folder = Path("data")
        subfolders = [data_folder]
        
        # Add subfolders (simulating the folder discovery logic)
        for item in data_folder.iterdir():
            if item.is_dir():
                if 'cache' not in item.name.lower() and item.name != 'mql5_feed':
                    subfolders.append(item)
                    for subitem in item.iterdir():
                        if subitem.is_dir() and 'cache' not in subitem.name.lower():
                            subfolders.append(subitem)
        
        # Add csv_converted folder specifically
        csv_converted_folder = data_folder / "cache" / "csv_converted"
        if csv_converted_folder.exists() and csv_converted_folder.is_dir():
            subfolders.append(csv_converted_folder)
        
        print(f"Available folders: {[str(f) for f in subfolders]}")
        
        # Simulate user input "8 eurusd" (folder 8 with eurusd mask)
        folder_idx = 8 - 1  # Convert to 0-based index
        mask = "eurusd"
        
        if 0 <= folder_idx < len(subfolders):
            folder_path = subfolders[folder_idx]
            print(f"Selected folder: {folder_path}")
            print(f"Mask: {mask}")
        else:
            pytest.fail(f"Invalid folder index: {folder_idx + 1}")
        
        # Find files matching the mask
        data_files = []
        for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
            if mask:
                # Apply mask filter
                pattern = f"*{mask}*{ext}"
                files = list(folder_path.glob(pattern))
                # Filter out temporary files
                files = [f for f in files if not f.name.startswith('tmp')]
                data_files.extend(files)
                
                # Also try case-insensitive search
                pattern = f"*{mask.upper()}*{ext}"
                files = list(folder_path.glob(pattern))
                files = [f for f in files if not f.name.startswith('tmp')]
                data_files.extend(files)
                
                pattern = f"*{mask.lower()}*{ext}"
                files = list(folder_path.glob(pattern))
                files = [f for f in files if not f.name.startswith('tmp')]
                data_files.extend(files)
        
        # Remove duplicates
        data_files = list(set(data_files))
        
        print(f"Found {len(data_files)} files matching '{mask}' in {folder_path}:")
        for file in data_files:
            print(f"  • {file.name}")
        
        if not data_files:
            pytest.fail(f"No files found matching mask '{mask}' in {folder_path}")
        
        # Load files and check for missing timestamps
        all_data = []
        problematic_files = []
        
        for i, file in enumerate(data_files):
            try:
                print(f"\n🔄 Loading file {i+1}/{len(data_files)}: {file.name}")
                
                # Load file
                df = self.data_manager.load_data_from_file(str(file))
                df['source_file'] = file.name
                
                # Check for missing values in Timestamp
                missing_count = 0
                missing_percent = 0
                
                if 'Timestamp' in df.columns:
                    missing_count = df['Timestamp'].isna().sum()
                    missing_percent = 100 * missing_count / len(df)
                elif df.index.name == 'Timestamp':
                    missing_count = df.index.isna().sum()
                    missing_percent = 100 * missing_count / len(df)
                
                print(f"  Shape: {df.shape}")
                print(f"  Missing timestamps: {missing_count} ({missing_percent:.2f}%)")
                
                if missing_percent > 50:  # More than 50% missing
                    problematic_files.append({
                        'file': file.name,
                        'missing_count': missing_count,
                        'missing_percent': missing_percent,
                        'shape': df.shape
                    })
                    print(f"  ⚠️  PROBLEMATIC FILE!")
                
                all_data.append(df)
                
            except Exception as e:
                print(f"  ❌ Error loading {file.name}: {e}")
                continue
        
        # Report problematic files
        if problematic_files:
            print(f"\n🚨 Found {len(problematic_files)} problematic files:")
            for file_info in problematic_files:
                print(f"   • {file_info['file']}: {file_info['missing_count']} missing ({file_info['missing_percent']:.2f}%)")
        else:
            print(f"\n✅ No problematic files found")
        
        # Test concatenation using the actual DataManager logic
        if all_data:
            print(f"\n🔄 Testing concatenation of {len(all_data)} files using DataManager logic...")
            
            try:
                # Use the same logic as DataManager
                has_datetime_index = any(isinstance(df.index, pd.DatetimeIndex) for df in all_data)
                
                if has_datetime_index:
                    print("📅 Detected DatetimeIndex in loaded DataFrames, preserving during concatenation...")
                    
                    # Convert DatetimeIndex to 'Timestamp' column for consistent concatenation
                    processed_data = []
                    for df in all_data:
                        df_copy = df.copy()
                        if isinstance(df_copy.index, pd.DatetimeIndex):
                            # Reset index to make datetime a column
                            df_copy = df_copy.reset_index()
                            # Rename the index column if it's unnamed
                            if df_copy.columns[0] == 'index':
                                df_copy = df_copy.rename(columns={'index': 'Timestamp'})
                        processed_data.append(df_copy)
                    
                    # Combine DataFrames with consistent column structure
                    combined_df = pd.concat(processed_data, ignore_index=True)
                    
                    print("✅ Successfully preserved datetime information during concatenation")
                else:
                    # No DatetimeIndex found, use standard concatenation
                    combined_df = pd.concat(all_data, ignore_index=True)
                
                print(f"Combined shape: {combined_df.shape}")
                print(f"Combined columns: {combined_df.columns.tolist()}")
                
                # Check for missing values in Timestamp after concatenation
                missing_count = 0
                missing_percent = 0
                
                if 'Timestamp' in combined_df.columns:
                    missing_count = combined_df['Timestamp'].isna().sum()
                    missing_percent = 100 * missing_count / len(combined_df)
                elif combined_df.index.name == 'Timestamp':
                    missing_count = combined_df.index.isna().sum()
                    missing_percent = 100 * missing_count / len(combined_df)
                
                print(f"Missing timestamps after concatenation: {missing_count} ({missing_percent:.2f}%)")
                
                if missing_percent > 50:
                    print(f"🚨 PROBLEM FOUND: High missing timestamps after concatenation!")
                    
                    # Show example rows with missing timestamps
                    if 'Timestamp' in combined_df.columns:
                        missing_rows = combined_df[combined_df['Timestamp'].isna()]
                        print(f"Example rows with NaN in Timestamp:")
                        print(missing_rows.head())
                else:
                    print(f"✅ Concatenation successful - no missing timestamp issues")
                
            except Exception as e:
                print(f"❌ Error during concatenation: {e}")
    
    def test_specific_eurusd_file_loading(self):
        """Test loading specific EURUSD files to identify the problematic one."""
        print("\n🔍 Testing specific EURUSD file loading...")
        
        # Test the specific file mentioned in the error
        test_files = [
            "data/cache/csv_converted/CSVExport_EURUSD_PERIOD_M15.parquet"
        ]
        
        for file_path in test_files:
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                continue
            
            print(f"\nTesting: {file_path}")
            
            try:
                # Load the file
                df = self.data_manager.load_data_from_file(file_path)
                
                print(f"  Shape: {df.shape}")
                print(f"  Columns: {df.columns.tolist()}")
                
                # Check for missing values in Timestamp
                missing_count = 0
                missing_percent = 0
                
                if 'Timestamp' in df.columns:
                    missing_count = df['Timestamp'].isna().sum()
                    missing_percent = 100 * missing_count / len(df)
                elif df.index.name == 'Timestamp':
                    missing_count = df.index.isna().sum()
                    missing_percent = 100 * missing_count / len(df)
                
                print(f"  Missing timestamps: {missing_count} ({missing_percent:.2f}%)")
                
                if missing_percent > 50:
                    print(f"  ⚠️  HIGH MISSING TIMESTAMPS!")
                    
                    # Show example rows
                    if 'Timestamp' in df.columns:
                        missing_rows = df[df['Timestamp'].isna()]
                        print(f"  Example rows with NaN in Timestamp:")
                        print(missing_rows.head())
                
            except Exception as e:
                print(f"  ❌ Error loading: {e}")


if __name__ == "__main__":
    # Run tests
    test_instance = TestInteractiveEURUSDLoading()
    test_instance.setup_method()
    
    print("🧪 Testing Interactive EURUSD Loading Issue...")
    print("=" * 60)
    
    # Test EURUSD loading simulation
    print("\n1️⃣  Testing EURUSD loading simulation...")
    test_instance.test_eurusd_loading_simulation()
    print("✅ EURUSD loading simulation completed")
    
    # Test specific EURUSD file loading
    print("\n2️⃣  Testing specific EURUSD file loading...")
    test_instance.test_specific_eurusd_file_loading()
    print("✅ Specific EURUSD file loading completed")
    
    print("\n🎉 All tests completed!")
