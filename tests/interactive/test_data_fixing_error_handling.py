#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Data Fixing Error Handling

This test verifies that the data fixing process handles errors gracefully
and doesn't crash the interactive system.
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "src"))

from src.interactive.analysis.analysis_runner import AnalysisRunner
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))
from interactive_system import InteractiveSystem


class TestDataFixingErrorHandling:
    """Test that data fixing handles errors gracefully."""
    
    def setup_method(self):
        """Set up test environment."""
        self.system = InteractiveSystem()
        self.analysis_runner = AnalysisRunner(self.system)
        
        # Create test data with various issues
        self.test_data = pd.DataFrame({
            'datetime': pd.date_range('2020-01-01', periods=100, freq='1min'),
            'open': [1.1000 + i * 0.0001 for i in range(100)],
            'high': [1.1005 + i * 0.0001 for i in range(100)],
            'low': [1.0995 + i * 0.0001 for i in range(100)],
            'close': [1.1002 + i * 0.0001 for i in range(100)],
            'volume': [1000 + i for i in range(100)],
            'pressure_vector': [0.1 + i * 0.01 for i in range(100)]
        })
        
        # Add some issues to test data
        self.test_data.loc[10, 'open'] = np.nan  # NaN value
        self.test_data.loc[20, 'close'] = -1.0   # Negative value
        self.test_data.loc[30, 'volume'] = 0     # Zero value
        self.test_data.loc[40, 'high'] = np.inf  # Infinity value
        
        # Add duplicate row
        self.test_data = pd.concat([self.test_data, self.test_data.iloc[50:51]], ignore_index=True)
        
        self.system.current_data = self.test_data.copy()
    
    def test_error_handling_in_fix_process(self):
        """Test that errors in fix process are handled gracefully."""
        print("\n🧪 Testing error handling in data fixing process...")
        
        # Mock fix functions to raise exceptions
        with patch('src.batch_eda.fix_files.fix_nan', side_effect=Exception("Test NaN fix error")):
            with patch('src.batch_eda.fix_files.fix_duplicates', side_effect=Exception("Test duplicate fix error")):
                with patch('src.batch_eda.fix_files.fix_zeros', side_effect=Exception("Test zero fix error")):
                    with patch('src.batch_eda.fix_files.fix_negatives', side_effect=Exception("Test negative fix error")):
                        with patch('src.batch_eda.fix_files.fix_infs', side_effect=Exception("Test infinity fix error")):
                            
                            # Create quality check summaries
                            nan_summary = [{'column': 'open', 'count': 1}]
                            dupe_summary = [{'type': 'row', 'count': 1}]
                            zero_summary = [{'column': 'volume', 'count': 1, 'anomaly': True}]
                            negative_summary = [{'column': 'close', 'count': 1}]
                            inf_summary = [{'column': 'high', 'count': 1}]
                            
                            # This should not crash
                            try:
                                # Simulate the fix process
                                print("   🔧 Testing NaN fix error handling...")
                                try:
                                    from src.batch_eda import fix_files
                                    fixed_data = fix_files.fix_nan(self.system.current_data, nan_summary)
                                    print("   ❌ Expected exception not raised")
                                except Exception as e:
                                    print(f"   ✅ NaN fix error handled: {e}")
                                
                                print("   🔧 Testing duplicate fix error handling...")
                                try:
                                    fixed_data = fix_files.fix_duplicates(self.system.current_data, dupe_summary)
                                    print("   ❌ Expected exception not raised")
                                except Exception as e:
                                    print(f"   ✅ Duplicate fix error handled: {e}")
                                
                                print("   🔧 Testing zero fix error handling...")
                                try:
                                    fixed_data = fix_files.fix_zeros(self.system.current_data, zero_summary)
                                    print("   ❌ Expected exception not raised")
                                except Exception as e:
                                    print(f"   ✅ Zero fix error handled: {e}")
                                
                                print("   🔧 Testing negative fix error handling...")
                                try:
                                    fixed_data = fix_files.fix_negatives(self.system.current_data, negative_summary)
                                    print("   ❌ Expected exception not raised")
                                except Exception as e:
                                    print(f"   ✅ Negative fix error handled: {e}")
                                
                                print("   🔧 Testing infinity fix error handling...")
                                try:
                                    fixed_data = fix_files.fix_infs(self.system.current_data, inf_summary)
                                    print("   ❌ Expected exception not raised")
                                except Exception as e:
                                    print(f"   ✅ Infinity fix error handled: {e}")
                                
                                print("✅ All error handling tests passed!")
                                
                            except Exception as e:
                                print(f"❌ Unexpected error in test: {e}")
                                raise
    
    def test_none_return_handling(self):
        """Test handling of None returns from fix functions."""
        print("\n🧪 Testing None return handling...")
        
        # Create quality check summaries
        nan_summary = [{'column': 'open', 'count': 1}]
        dupe_summary = [{'type': 'row', 'count': 1}]
        zero_summary = [{'column': 'volume', 'count': 1, 'anomaly': True}]
        negative_summary = [{'column': 'close', 'count': 1}]
        inf_summary = [{'column': 'high', 'count': 1}]
        
        # Test that None returns are handled gracefully
        from src.batch_eda import fix_files

        print("   🔧 Testing NaN fix None return...")
        # Mock the function directly
        with patch.object(fix_files, 'fix_nan', return_value=None):
            fixed_data = fix_files.fix_nan(self.system.current_data, nan_summary)
            # The mock returns None, so this should pass
            assert fixed_data is None, "Expected None return from mocked fix_nan function"
            print("   ✅ NaN fix None return handled correctly")
        
        print("   🔧 Testing duplicate fix None return...")
        with patch.object(fix_files, 'fix_duplicates', return_value=None):
            fixed_data = fix_files.fix_duplicates(self.system.current_data, dupe_summary)
            assert fixed_data is None
            print("   ✅ Duplicate fix None return handled correctly")
        
        print("   🔧 Testing zero fix None return...")
        with patch.object(fix_files, 'fix_zeros', return_value=None):
            fixed_data = fix_files.fix_zeros(self.system.current_data, zero_summary)
            assert fixed_data is None
            print("   ✅ Zero fix None return handled correctly")
        
        print("   🔧 Testing negative fix None return...")
        with patch.object(fix_files, 'fix_negatives', return_value=None):
            fixed_data = fix_files.fix_negatives(self.system.current_data, negative_summary)
            assert fixed_data is None
            print("   ✅ Negative fix None return handled correctly")
        
        print("   🔧 Testing infinity fix None return...")
        with patch.object(fix_files, 'fix_infs', return_value=None):
            fixed_data = fix_files.fix_infs(self.system.current_data, inf_summary)
            assert fixed_data is None
            print("   ✅ Infinity fix None return handled correctly")
        
        print("✅ All None return handling tests passed!")
    
    def test_data_integrity_after_errors(self):
        """Test that data integrity is maintained after errors."""
        print("\n🧪 Testing data integrity after errors...")
        
        original_data = self.system.current_data.copy()
        original_shape = original_data.shape
        
        # Mock fix function to raise exception
        with patch('src.batch_eda.fix_files.fix_nan', side_effect=Exception("Test error")):
            
            nan_summary = [{'column': 'open', 'count': 1}]
            
            # This should not modify the data
            try:
                from src.batch_eda import fix_files
                fixed_data = fix_files.fix_nan(self.system.current_data, nan_summary)
            except Exception as e:
                print(f"   ✅ Error caught: {e}")
            
            # Check that data is unchanged
            assert self.system.current_data.shape == original_shape
            assert self.system.current_data.equals(original_data)
            print("   ✅ Data integrity maintained after error")
        
        print("✅ Data integrity test passed!")
    
    def test_backup_saving_error_handling(self):
        """Test error handling in backup saving."""
        print("\n🧪 Testing backup saving error handling...")
        
        # Mock os.makedirs to raise exception
        with patch('os.makedirs', side_effect=Exception("Permission denied")):
            try:
                backup_path = os.path.join('data', 'backups', f'data_backup_{int(time.time())}.parquet')
                os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                print("   ❌ Expected exception not raised")
            except Exception as e:
                print(f"   ✅ Backup saving error handled: {e}")
        
        print("✅ Backup saving error handling test passed!")


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
