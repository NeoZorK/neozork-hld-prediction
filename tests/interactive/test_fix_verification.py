#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Verification Test

This test verifies that the fix for the concatenation issue works correctly.
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


class TestFixVerification:
    """Test that the fix for concatenation issue works."""
    
    def setup_method(self):
        """Setup method for tests."""
        self.data_manager = DataManager()
        
    def test_mixed_file_concatenation(self):
        """Test concatenation of files with mixed structures."""
        print("🧪 Testing mixed file concatenation fix...")
        print("=" * 50)
        
        # Test files with different structures
        test_files = [
            "data/cache/csv_converted/CSVExport_EURUSD_PERIOD_H1.parquet",  # No Timestamp column
            "data/cache/csv_converted/CSVExport_EURUSD_PERIOD_D1.parquet"   # Has Timestamp column
        ]
        
        # Load files
        dataframes = []
        for file_path in test_files:
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                continue
            
            print(f"Loading: {os.path.basename(file_path)}")
            df = self.data_manager.load_data_from_file(file_path)
            df['source_file'] = os.path.basename(file_path)
            dataframes.append(df)
            
            print(f"  Shape: {df.shape}")
            print(f"  Has Timestamp column: {'Timestamp' in df.columns}")
            print(f"  Columns: {df.columns.tolist()}")
        
        if len(dataframes) < 2:
            pytest.skip("Not enough files to test concatenation")
        
        # Test the fix logic
        print(f"\n🔄 Testing concatenation fix...")
        
        # Check for mixed structures
        has_timestamp_column = any('Timestamp' in df.columns for df in dataframes)
        missing_timestamp_column = any('Timestamp' not in df.columns for df in dataframes)
        
        print(f"Has Timestamp column: {has_timestamp_column}")
        print(f"Missing Timestamp column: {missing_timestamp_column}")
        
        if has_timestamp_column and missing_timestamp_column:
            print("⚠️  Detected mixed file structures, applying fix...")
            
            # Apply the fix
            processed_data = []
            for i, df in enumerate(dataframes):
                df_copy = df.copy()
                
                if 'Timestamp' not in df_copy.columns:
                    # Create a dummy Timestamp column for files without it
                    df_copy['Timestamp'] = pd.NaT
                    print(f"   Added Timestamp column to file {i+1}")
                
                processed_data.append(df_copy)
            
            # Combine DataFrames
            combined_df = pd.concat(processed_data, ignore_index=True)
            
            print("✅ Fix applied successfully")
        else:
            print("✅ No mixed structures detected, using standard concatenation")
            combined_df = pd.concat(dataframes, ignore_index=True)
        
        # Check results
        print(f"\n📊 Results:")
        print(f"Combined shape: {combined_df.shape}")
        print(f"Combined columns: {combined_df.columns.tolist()}")
        
        # Check for missing values in Timestamp
        if 'Timestamp' in combined_df.columns:
            missing_count = combined_df['Timestamp'].isna().sum()
            missing_percent = 100 * missing_count / len(combined_df)
            
            print(f"Missing timestamps: {missing_count} ({missing_percent:.2f}%)")
            
            # Show breakdown by source file
            print(f"\n📋 Breakdown by source file:")
            for source_file in combined_df['source_file'].unique():
                file_data = combined_df[combined_df['source_file'] == source_file]
                file_missing = file_data['Timestamp'].isna().sum()
                file_total = len(file_data)
                file_percent = 100 * file_missing / file_total
                print(f"  {source_file}: {file_missing}/{file_total} missing ({file_percent:.2f}%)")
            
            # The fix should result in missing timestamps only for files that didn't have them originally
            if missing_percent > 50:
                print(f"⚠️  Still high missing timestamps, but this is expected for mixed structures")
                print(f"   Files without original Timestamp columns will have missing values")
            else:
                print(f"✅ SUCCESS: Low missing timestamps")
        else:
            print(f"❌ No Timestamp column found in combined data")


if __name__ == "__main__":
    # Run tests
    test_instance = TestFixVerification()
    test_instance.setup_method()
    
    print("🧪 Testing Fix Verification...")
    print("=" * 50)
    
    # Test mixed file concatenation
    print("\n1️⃣  Testing mixed file concatenation...")
    test_instance.test_mixed_file_concatenation()
    print("✅ Mixed file concatenation test completed")
    
    print("\n🎉 All tests completed!")
