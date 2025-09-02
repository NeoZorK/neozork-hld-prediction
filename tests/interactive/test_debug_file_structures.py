#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug File Structures Test

This test analyzes the structure of each parquet file to understand
why concatenation is causing missing timestamps.
"""

import os
import pandas as pd
import pytest
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.interactive.data_manager import DataManager


class TestDebugFileStructures:
    """Debug file structures to understand concatenation issue."""
    
    def setup_method(self):
        """Setup method for tests."""
        self.data_manager = DataManager()
        
    def test_individual_file_structures(self):
        """Test individual file structures to understand the issue."""
        print("🔍 Analyzing individual file structures...")
        print("=" * 60)
        
        # Test specific EURUSD files
        test_files = [
            "data/cache/csv_converted/CSVExport_EURUSD_PERIOD_H1.parquet",
            "data/cache/csv_converted/CSVExport_EURUSD_PERIOD_W1.parquet",
            "data/cache/csv_converted/CSVExport_EURUSD_PERIOD_D1.parquet",
            "data/cache/csv_converted/CSVExport_EURUSD_PERIOD_M15.parquet"
        ]
        
        file_structures = []
        
        for file_path in test_files:
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                continue
            
            print(f"\n📁 Analyzing: {os.path.basename(file_path)}")
            
            try:
                # Load the file
                df = self.data_manager.load_data_from_file(file_path)
                
                # Analyze structure
                structure = {
                    'file': os.path.basename(file_path),
                    'shape': df.shape,
                    'has_datetime_index': isinstance(df.index, pd.DatetimeIndex),
                    'index_name': df.index.name if hasattr(df.index, 'name') else None,
                    'columns': df.columns.tolist(),
                    'has_timestamp_column': 'Timestamp' in df.columns,
                    'timestamp_column_type': None,
                    'missing_timestamps': 0,
                    'missing_percent': 0
                }
                
                # Check for Timestamp column
                if 'Timestamp' in df.columns:
                    structure['timestamp_column_type'] = str(df['Timestamp'].dtype)
                    structure['missing_timestamps'] = df['Timestamp'].isna().sum()
                    structure['missing_percent'] = 100 * structure['missing_timestamps'] / len(df)
                elif isinstance(df.index, pd.DatetimeIndex):
                    structure['missing_timestamps'] = df.index.isna().sum()
                    structure['missing_percent'] = 100 * structure['missing_timestamps'] / len(df)
                
                # Print structure info
                print(f"  Shape: {structure['shape']}")
                print(f"  Has DatetimeIndex: {structure['has_datetime_index']}")
                print(f"  Index name: {structure['index_name']}")
                print(f"  Has Timestamp column: {structure['has_timestamp_column']}")
                if structure['timestamp_column_type']:
                    print(f"  Timestamp column type: {structure['timestamp_column_type']}")
                print(f"  Missing timestamps: {structure['missing_timestamps']} ({structure['missing_percent']:.2f}%)")
                print(f"  Columns: {structure['columns']}")
                
                file_structures.append(structure)
                
            except Exception as e:
                print(f"  ❌ Error loading: {e}")
        
        # Analyze the structures
        print(f"\n📊 Structure Analysis Summary:")
        print("=" * 60)
        
        datetime_index_files = [s for s in file_structures if s['has_datetime_index']]
        timestamp_column_files = [s for s in file_structures if s['has_timestamp_column']]
        
        print(f"Files with DatetimeIndex: {len(datetime_index_files)}")
        for s in datetime_index_files:
            print(f"  • {s['file']}")
        
        print(f"Files with Timestamp column: {len(timestamp_column_files)}")
        for s in timestamp_column_files:
            print(f"  • {s['file']}")
        
        # Test concatenation scenarios
        print(f"\n🧪 Testing concatenation scenarios...")
        print("=" * 60)
        
        # Scenario 1: Only DatetimeIndex files
        if len(datetime_index_files) >= 2:
            print(f"\nScenario 1: Concatenating only DatetimeIndex files...")
            self._test_concatenation_scenario(datetime_index_files[:2], "DatetimeIndex only")
        
        # Scenario 2: Only Timestamp column files
        if len(timestamp_column_files) >= 2:
            print(f"\nScenario 2: Concatenating only Timestamp column files...")
            self._test_concatenation_scenario(timestamp_column_files[:2], "Timestamp column only")
        
        # Scenario 3: Mixed files
        if datetime_index_files and timestamp_column_files:
            print(f"\nScenario 3: Concatenating mixed files...")
            mixed_files = [datetime_index_files[0], timestamp_column_files[0]]
            self._test_concatenation_scenario(mixed_files, "Mixed files")
    
    def _test_concatenation_scenario(self, file_structures, scenario_name):
        """Test concatenation for a specific scenario."""
        print(f"  Testing: {scenario_name}")
        
        # Load the files
        dataframes = []
        for structure in file_structures:
            file_path = f"data/cache/csv_converted/{structure['file']}"
            try:
                df = self.data_manager.load_data_from_file(file_path)
                df['source_file'] = structure['file']
                dataframes.append(df)
                print(f"    Loaded {structure['file']}: {df.shape}")
            except Exception as e:
                print(f"    ❌ Error loading {structure['file']}: {e}")
        
        if len(dataframes) < 2:
            print(f"    ⚠️  Not enough files to test concatenation")
            return
        
        # Test concatenation
        try:
            # Check if any DataFrames have DatetimeIndex
            has_datetime_index = any(isinstance(df.index, pd.DatetimeIndex) for df in dataframes)
            
            if has_datetime_index:
                print(f"    📅 Detected DatetimeIndex, using special concatenation...")
                
                # Convert DatetimeIndex to 'Timestamp' column for consistent concatenation
                processed_data = []
                for df in dataframes:
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
                
                print(f"    ✅ Special concatenation successful")
            else:
                # No DatetimeIndex found, use standard concatenation
                combined_df = pd.concat(dataframes, ignore_index=True)
                print(f"    ✅ Standard concatenation successful")
            
            # Check for missing values in Timestamp
            missing_count = 0
            missing_percent = 0
            
            if 'Timestamp' in combined_df.columns:
                missing_count = combined_df['Timestamp'].isna().sum()
                missing_percent = 100 * missing_count / len(combined_df)
            elif combined_df.index.name == 'Timestamp':
                missing_count = combined_df.index.isna().sum()
                missing_percent = 100 * missing_count / len(combined_df)
            
            print(f"    Combined shape: {combined_df.shape}")
            print(f"    Missing timestamps: {missing_count} ({missing_percent:.2f}%)")
            
            if missing_percent > 50:
                print(f"    🚨 PROBLEM: High missing timestamps!")
            else:
                print(f"    ✅ SUCCESS: Low missing timestamps")
                
        except Exception as e:
            print(f"    ❌ Error during concatenation: {e}")


if __name__ == "__main__":
    # Run tests
    test_instance = TestDebugFileStructures()
    test_instance.setup_method()
    
    print("🧪 Debugging File Structures...")
    print("=" * 60)
    
    # Test individual file structures
    print("\n1️⃣  Testing individual file structures...")
    test_instance.test_individual_file_structures()
    print("✅ File structure analysis completed")
    
    print("\n🎉 All tests completed!")
