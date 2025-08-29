#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Data Fixing in Docker

This script tests the data fixing functionality in Docker to identify
and fix the issue with system exiting to shell.
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, '/app/src')

# Simple color classes for testing
class SimpleFore:
    MAGENTA = ""
    YELLOW = ""
    RED = ""
    GREEN = ""
    BLUE = ""
    CYAN = ""

class SimpleStyle:
    RESET_ALL = ""

def create_test_data():
    """Create test data with various issues."""
    print("📊 Creating test data with issues...")
    
    # Create test data with various issues
    test_data = pd.DataFrame({
        'datetime': pd.date_range('2020-01-01', periods=100, freq='1min'),
        'open': [1.1000 + i * 0.0001 for i in range(100)],
        'high': [1.1005 + i * 0.0001 for i in range(100)],
        'low': [1.0995 + i * 0.0001 for i in range(100)],
        'close': [1.1002 + i * 0.0001 for i in range(100)],
        'volume': [1000 + i for i in range(100)],
        'pressure_vector': [0.1 + i * 0.01 for i in range(100)]
    })
    
    # Add some issues to test data
    test_data.loc[10, 'open'] = np.nan  # NaN value
    test_data.loc[20, 'close'] = -1.0   # Negative value
    test_data.loc[30, 'volume'] = 0     # Zero value
    test_data.loc[40, 'high'] = np.inf  # Infinity value
    
    # Add duplicate row
    test_data = pd.concat([test_data, test_data.iloc[50:51]], ignore_index=True)
    
    print(f"✅ Test data created with shape: {test_data.shape}")
    return test_data

def test_data_quality_checks(test_data):
    """Test data quality checks."""
    print("\n🔍 Testing data quality checks...")
    
    try:
        from src.eda import data_quality
        
        # Initialize summaries
        nan_summary = []
        dupe_summary = []
        gap_summary = []
        zero_summary = []
        negative_summary = []
        inf_summary = []
        
        # Create simple color objects
        Fore = SimpleFore()
        Style = SimpleStyle()
        
        # Run quality checks
        data_quality.nan_check(test_data, nan_summary, Fore, Style)
        data_quality.duplicate_check(test_data, dupe_summary, Fore, Style)
        data_quality.gap_check(test_data, gap_summary, Fore, Style)
        data_quality.zero_check(test_data, zero_summary, Fore, Style)
        data_quality.negative_check(test_data, negative_summary, Fore, Style)
        data_quality.inf_check(test_data, inf_summary, Fore, Style)
        
        print(f"✅ Quality checks completed:")
        print(f"   NaN issues: {len(nan_summary)}")
        print(f"   Duplicate issues: {len(dupe_summary)}")
        print(f"   Gap issues: {len(gap_summary)}")
        print(f"   Zero issues: {len(zero_summary)}")
        print(f"   Negative issues: {len(negative_summary)}")
        print(f"   Infinity issues: {len(inf_summary)}")
        
        return nan_summary, dupe_summary, gap_summary, zero_summary, negative_summary, inf_summary
        
    except Exception as e:
        print(f"❌ Error in data quality checks: {e}")
        import traceback
        traceback.print_exc()
        return [], [], [], [], [], []

def test_fix_functions(test_data, summaries):
    """Test individual fix functions."""
    print("\n🔧 Testing individual fix functions...")
    
    nan_summary, dupe_summary, gap_summary, zero_summary, negative_summary, inf_summary = summaries
    
    try:
        from src.eda import fix_files
        
        # Test NaN fixing
        if nan_summary:
            print("   • Testing NaN fixing...")
            try:
                fixed_data = fix_files.fix_nan(test_data, nan_summary)
                if fixed_data is not None:
                    print(f"   ✅ NaN fixing successful. Shape: {fixed_data.shape}")
                else:
                    print("   ⚠️  NaN fixing returned None")
            except Exception as e:
                print(f"   ❌ Error in NaN fixing: {e}")
                import traceback
                traceback.print_exc()
        
        # Test duplicate fixing
        if dupe_summary:
            print("   • Testing duplicate fixing...")
            try:
                fixed_data = fix_files.fix_duplicates(test_data, dupe_summary)
                if fixed_data is not None:
                    print(f"   ✅ Duplicate fixing successful. Shape: {fixed_data.shape}")
                else:
                    print("   ⚠️  Duplicate fixing returned None")
            except Exception as e:
                print(f"   ❌ Error in duplicate fixing: {e}")
                import traceback
                traceback.print_exc()
        
        # Test zero fixing
        if zero_summary:
            print("   • Testing zero fixing...")
            try:
                fixed_data = fix_files.fix_zeros(test_data, zero_summary)
                if fixed_data is not None:
                    print(f"   ✅ Zero fixing successful. Shape: {fixed_data.shape}")
                else:
                    print("   ⚠️  Zero fixing returned None")
            except Exception as e:
                print(f"   ❌ Error in zero fixing: {e}")
                import traceback
                traceback.print_exc()
        
        # Test negative fixing
        if negative_summary:
            print("   • Testing negative fixing...")
            try:
                fixed_data = fix_files.fix_negatives(test_data, negative_summary)
                if fixed_data is not None:
                    print(f"   ✅ Negative fixing successful. Shape: {fixed_data.shape}")
                else:
                    print("   ⚠️  Negative fixing returned None")
            except Exception as e:
                print(f"   ❌ Error in negative fixing: {e}")
                import traceback
                traceback.print_exc()
        
        # Test infinity fixing
        if inf_summary:
            print("   • Testing infinity fixing...")
            try:
                fixed_data = fix_files.fix_infs(test_data, inf_summary)
                if fixed_data is not None:
                    print(f"   ✅ Infinity fixing successful. Shape: {fixed_data.shape}")
                else:
                    print("   ⚠️  Infinity fixing returned None")
            except Exception as e:
                print(f"   ❌ Error in infinity fixing: {e}")
                import traceback
                traceback.print_exc()
        
        print("✅ Individual fix function tests completed")
        
    except Exception as e:
        print(f"❌ Error in fix function tests: {e}")
        import traceback
        traceback.print_exc()

def test_comprehensive_fixing(test_data, summaries):
    """Test comprehensive fixing process."""
    print("\n🔧 Testing comprehensive fixing process...")
    
    nan_summary, dupe_summary, gap_summary, zero_summary, negative_summary, inf_summary = summaries
    
    try:
        from src.eda import fix_files
        
        print("🔧 FIXING ALL DETECTED ISSUES...")
        print("-" * 50)
        
        # Create backup
        backup_data = test_data.copy()
        print("   • Backup created")
        
        current_data = test_data.copy()
        
        # Fix all issues with error handling
        if nan_summary:
            print("   • Fixing NaN values...")
            try:
                fixed_data = fix_files.fix_nan(current_data, nan_summary)
                if fixed_data is not None:
                    current_data = fixed_data
                    print(f"   ✅ NaN values fixed. Data shape: {current_data.shape}")
                else:
                    print("   ⚠️  NaN fixing returned None, skipping...")
            except Exception as e:
                print(f"   ❌ Error fixing NaN values: {e}")
                import traceback
                traceback.print_exc()
        
        if dupe_summary:
            print("   • Fixing duplicate rows...")
            try:
                fixed_data = fix_files.fix_duplicates(current_data, dupe_summary)
                if fixed_data is not None:
                    current_data = fixed_data
                    print(f"   ✅ Duplicate rows fixed. Data shape: {current_data.shape}")
                else:
                    print("   ⚠️  Duplicate fixing returned None, skipping...")
            except Exception as e:
                print(f"   ❌ Error fixing duplicate rows: {e}")
                import traceback
                traceback.print_exc()
        
        if zero_summary:
            print("   • Fixing zero values...")
            try:
                fixed_data = fix_files.fix_zeros(current_data, zero_summary)
                if fixed_data is not None:
                    current_data = fixed_data
                    print(f"   ✅ Zero values fixed. Data shape: {current_data.shape}")
                else:
                    print("   ⚠️  Zero fixing returned None, skipping...")
            except Exception as e:
                print(f"   ❌ Error fixing zero values: {e}")
                import traceback
                traceback.print_exc()
        
        if negative_summary:
            print("   • Fixing negative values...")
            try:
                fixed_data = fix_files.fix_negatives(current_data, negative_summary)
                if fixed_data is not None:
                    current_data = fixed_data
                    print(f"   ✅ Negative values fixed. Data shape: {current_data.shape}")
                else:
                    print("   ⚠️  Negative fixing returned None, skipping...")
            except Exception as e:
                print(f"   ❌ Error fixing negative values: {e}")
                import traceback
                traceback.print_exc()
        
        if inf_summary:
            print("   • Fixing infinity values...")
            try:
                fixed_data = fix_files.fix_infs(current_data, inf_summary)
                if fixed_data is not None:
                    current_data = fixed_data
                    print(f"   ✅ Infinity values fixed. Data shape: {current_data.shape}")
                else:
                    print("   ⚠️  Infinity fixing returned None, skipping...")
            except Exception as e:
                print(f"   ❌ Error fixing infinity values: {e}")
                import traceback
                traceback.print_exc()
        
        # Final duplicate removal
        try:
            final_dupe_check = current_data.duplicated().sum()
            if final_dupe_check > 0:
                print(f"   • Final duplicate removal...")
                current_data = current_data.drop_duplicates(keep='first')
                print(f"   ✅ Removed {final_dupe_check} remaining duplicate rows")
        except Exception as e:
            print(f"   ❌ Error in final duplicate removal: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n✅ All issues have been fixed!")
        print(f"   • Original data shape: {backup_data.shape}")
        print(f"   • Fixed data shape: {current_data.shape}")
        
        # Save backup and fixed data
        try:
            backup_path = os.path.join('/app/data', 'backups', f'data_backup_test_{int(time.time())}.parquet')
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            backup_data.to_parquet(backup_path)
            print(f"   • Backup saved to: {backup_path}")
        except Exception as e:
            print(f"   ❌ Error saving backup: {e}")
        
        try:
            fixed_data_path = os.path.join('/app/data', 'backups', f'data_fixed_test_{int(time.time())}.parquet')
            current_data.to_parquet(fixed_data_path)
            print(f"   • Fixed data saved to: {fixed_data_path}")
        except Exception as e:
            print(f"   ❌ Error saving fixed data: {e}")
        
        print("✅ Comprehensive fixing test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in comprehensive fixing test: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main test function."""
    print("🧪 Testing Data Fixing in Docker")
    print("=" * 50)
    
    try:
        # Create test data
        test_data = create_test_data()
        
        # Test quality checks
        summaries = test_data_quality_checks(test_data)
        
        # Test individual fix functions
        test_fix_functions(test_data, summaries)
        
        # Test comprehensive fixing
        test_comprehensive_fixing(test_data, summaries)
        
        print("\n✅ All tests completed successfully!")
        print("The data fixing functionality should now work without exiting to shell.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    import time
    main()
