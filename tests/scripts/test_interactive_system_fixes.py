#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for interactive_system.py fixes

This script tests the fixes for:
1. Progress bar issues in data quality checks
2. Data fixing functionality
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
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


def test_progress_bars():
    """Test progress bar functionality."""
    from src.interactive import InteractiveSystem
    
    system = InteractiveSystem()
    
    # Check that the system has the expected attributes
    assert hasattr(system, 'current_data')
    assert hasattr(system, 'current_results')
    assert hasattr(system, 'analysis_runner')
    assert hasattr(system, 'data_manager')
    assert hasattr(system, 'visualization_manager')
    assert hasattr(system, 'feature_engineering_manager')
    assert hasattr(system, 'menu_manager')


def test_data_fixing():
    """Test that data fixing works correctly."""
    print("🧪 Testing data fixing...")
    
    system = InteractiveSystem()
    system.current_data = create_test_data()
    
    # Set up quality results
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
    assert system.current_data['open'].isna().sum() == 0
    
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


def main():
    """Run all tests."""
    print("🚀 Running interactive_system.py fixes tests...")
    print("=" * 60)
    
    try:
        test_progress_bars()
        test_data_fixing()
        test_error_handling()
        
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
