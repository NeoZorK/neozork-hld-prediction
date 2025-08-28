#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test script for interactive_system.py fixes

This script tests the fixes without interactive input.
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from interactive_system import InteractiveSystem


def create_test_data():
    """Create test data with various quality issues."""
    # Create sample data with issues
    data = {
        'open': [100, 101, np.nan, 103, 104, 105, 100, 101, 102, 103],  # NaN value
        'high': [102, 103, 104, 105, 106, 107, 102, 103, 104, 105],     # No issues
        'low': [98, 99, 100, 101, 102, 103, 98, 99, 100, 101],         # No issues
        'close': [101, 102, 103, 104, 105, 106, 101, 102, 103, 104],    # No issues
        'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1000, 1100, 1200, 1300],  # Duplicates
        'predicted_low': [0, 0, 0, 99, 100, 101, 0, 0, 0, 99],         # Many zeros
        'predicted_high': [0, 0, 0, 102, 103, 104, 0, 0, 0, 102],      # Many zeros
        'pressure': [0, 0, 0, 0.5, 0.6, 0.7, 0, 0, 0, 0.5],           # Many zeros
        'pressure_vector': [0, 0, 0, 0, 0, 0.1, 0.2, 0.3, 0, 0],      # Many zeros
        'source_file': ['test.csv'] * 10  # All same value
    }
    
    return pd.DataFrame(data)


def test_data_fixing_direct():
    """Test data fixing directly without running quality check."""
    print("🧪 Testing data fixing directly...")
    
    system = InteractiveSystem()
    system.current_data = create_test_data()
    
    # Set up quality results manually
    system.current_results['comprehensive_data_quality'] = {
        'nan_summary': [{'column': 'open', 'missing': 1, 'percent': 10.0}],
        'dupe_summary': [{'type': 'full_row', 'count': 2}],
        'gap_summary': [],
        'zero_summary': [{'column': 'predicted_low', 'zeros': 6, 'anomaly': True}],
        'negative_summary': [],
        'inf_summary': []
    }
    
    # Store original shape
    original_shape = system.current_data.shape
    original_nan_count = system.current_data['open'].isna().sum()
    
    print(f"   Original shape: {original_shape}")
    print(f"   Original NaN count in 'open': {original_nan_count}")
    
    # Run data fixing
    system.fix_all_data_issues()
    
    # Check that fixes were applied
    assert 'data_fixes' in system.current_results
    fix_data = system.current_results['data_fixes']
    
    # Check that backup was created
    assert 'backup_file' in fix_data
    assert 'nan_fixed' in fix_data
    assert 'duplicates_removed' in fix_data
    
    # Check that NaN was fixed
    final_nan_count = system.current_data['open'].isna().sum()
    assert final_nan_count == 0, f"NaN not fixed: {final_nan_count} remaining"
    
    print(f"   Final NaN count in 'open': {final_nan_count}")
    print(f"   NaN fixed: {fix_data['nan_fixed']}")
    print(f"   Duplicates removed: {fix_data['duplicates_removed']}")
    
    print("✅ Data fixing test passed!")


def test_error_handling():
    """Test error handling in data fixing."""
    print("🧪 Testing error handling...")
    
    system = InteractiveSystem()
    system.current_data = create_test_data()
    
    # Test with invalid quality results
    system.current_results['comprehensive_data_quality'] = {
        'nan_summary': ['invalid_entry'],  # Not a dict
        'dupe_summary': [],
        'gap_summary': [],
        'zero_summary': ['invalid_entry'],  # Not a dict
        'negative_summary': [],
        'inf_summary': []
    }
    
    # This should not crash
    try:
        system.fix_all_data_issues()
        print("✅ Error handling test passed!")
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        raise


def test_progress_bar_structure():
    """Test that progress bar structure is correct."""
    print("🧪 Testing progress bar structure...")
    
    system = InteractiveSystem()
    system.current_data = create_test_data()
    
    # Mock the data quality functions to avoid actual processing
    try:
        from src.eda import data_quality
        
        # Store original functions
        original_functions = {
            'nan_check': data_quality.nan_check,
            'duplicate_check': data_quality.duplicate_check,
            'gap_check': data_quality.gap_check,
            'zero_check': data_quality.zero_check,
            'negative_check': data_quality.negative_check,
            'inf_check': data_quality.inf_check
        }
        
        # Mock functions that just update progress
        def mock_nan_check(df, nan_summary, Fore, Style):
            nan_summary.append({'column': 'open', 'missing': 1, 'percent': 10.0})
        
        def mock_duplicate_check(df, dupe_summary, Fore, Style):
            dupe_summary.append({'type': 'full_row', 'count': 2})
        
        def mock_gap_check(df, gap_summary, Fore, Style, **kwargs):
            pass  # No gaps in test data
        
        def mock_zero_check(df, zero_summary, Fore, Style, **kwargs):
            zero_summary.append({'column': 'predicted_low', 'zeros': 6, 'anomaly': True})
        
        def mock_negative_check(df, negative_summary, Fore, Style, **kwargs):
            pass  # No negative values in test data
        
        def mock_inf_check(df, inf_summary, Fore, Style, **kwargs):
            pass  # No infinity values in test data
        
        # Replace functions
        data_quality.nan_check = mock_nan_check
        data_quality.duplicate_check = mock_duplicate_check
        data_quality.gap_check = mock_gap_check
        data_quality.zero_check = mock_zero_check
        data_quality.negative_check = mock_negative_check
        data_quality.inf_check = mock_inf_check
        
        # Run data quality check
        system.run_comprehensive_data_quality_check()
        
        # Check that results were saved
        assert 'comprehensive_data_quality' in system.current_results
        quality_data = system.current_results['comprehensive_data_quality']
        
        # Check that basic quality metrics are present
        assert 'total_rows' in quality_data
        assert 'total_cols' in quality_data
        assert 'missing_values' in quality_data
        assert 'duplicates' in quality_data
        
        print("✅ Progress bar structure test passed!")
        
    except Exception as e:
        print(f"❌ Progress bar structure test failed: {e}")
        raise
    finally:
        # Restore original functions
        if 'original_functions' in locals():
            from src.eda import data_quality
            for func_name, func in original_functions.items():
                setattr(data_quality, func_name, func)


def main():
    """Run all tests."""
    print("🚀 Running interactive_system.py fixes tests...")
    print("=" * 60)
    
    try:
        test_data_fixing_direct()
        test_error_handling()
        test_progress_bar_structure()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
