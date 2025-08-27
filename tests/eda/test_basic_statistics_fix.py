#!/usr/bin/env python3
"""
Test script to verify the fixed run_basic_statistics function
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import numpy as np
import pytest
from interactive_system import InteractiveSystem


class TestBasicStatisticsFix:
    """Test class for basic statistics function fixes"""
    
    def test_basic_statistics_fix(self):
        """Test the fixed run_basic_statistics function"""
        print("🧪 Testing fixed run_basic_statistics function...")
        
        # Create test data
        np.random.seed(42)
        test_data = pd.DataFrame({
            'A': np.random.normal(0, 1, 1000),
            'B': np.random.exponential(1, 1000),
            'C': np.random.uniform(0, 10, 1000),
            'D': ['category_' + str(i % 5) for i in range(1000)]
        })
        
        # Add some NaN values
        test_data.loc[100:150, 'A'] = np.nan
        test_data.loc[200:250, 'B'] = np.nan
        
        print(f"📊 Test data shape: {test_data.shape}")
        print(f"📊 Test data columns: {list(test_data.columns)}")
        print(f"📊 Test data types: {test_data.dtypes.value_counts().to_dict()}")
        
        # Create InteractiveSystem instance
        system = InteractiveSystem()
        system.current_data = test_data
        
        # Test the function with seaborn mocking to avoid warnings
        try:
            print("\n" + "="*60)
            print("🧪 RUNNING BASIC STATISTICS TEST")
            print("="*60)
            
            # Mock seaborn to avoid warnings
            from unittest.mock import patch
            with patch('seaborn.boxplot') as mock_boxplot, \
                 patch('seaborn.histplot') as mock_histplot, \
                 patch('seaborn.heatmap') as mock_heatmap:
                
                system.run_basic_statistics()
            
            print("\n" + "="*60)
            print("✅ TEST COMPLETED SUCCESSFULLY!")
            print("="*60)
            
            # Check if results were saved
            assert 'comprehensive_basic_statistics' in system.current_results, "Results not saved"
            
            results = system.current_results['comprehensive_basic_statistics']
            assert 'basic_stats' in results, "Basic stats not found"
            assert 'descriptive_stats' in results, "Descriptive stats not found"
            assert 'distribution_analysis' in results, "Distribution analysis not found"
            assert 'outlier_analysis' in results, "Outlier analysis not found"
            
            print("✅ All test assertions passed!")
            
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            pytest.fail(f"Test failed: {e}")
    
    def test_large_dataset_handling(self):
        """Test the run_basic_statistics function with a large dataset"""
        print("🧪 Testing run_basic_statistics with large dataset...")
        
        # Create large test data (150k rows to trigger the limit)
        np.random.seed(42)
        print("📊 Creating large test dataset (150,000 rows)...")
        
        test_data = pd.DataFrame({
            'A': np.random.normal(0, 1, 150000),
            'B': np.random.exponential(1, 150000),
            'C': np.random.uniform(0, 10, 150000),
            'D': ['category_' + str(i % 5) for i in range(150000)]
        })
        
        # Add some NaN values
        test_data.loc[1000:1500, 'A'] = np.nan
        test_data.loc[2000:2500, 'B'] = np.nan
        
        print(f"📊 Test data shape: {test_data.shape}")
        print(f"📊 Test data columns: {list(test_data.columns)}")
        print(f"📊 Test data types: {test_data.dtypes.value_counts().to_dict()}")
        
        # Create InteractiveSystem instance
        system = InteractiveSystem()
        system.current_data = test_data
        
        # Test the function with seaborn mocking to avoid warnings
        try:
            print("\n" + "="*60)
            print("🧪 RUNNING BASIC STATISTICS TEST WITH LARGE DATASET")
            print("="*60)
            
            # Mock seaborn to avoid warnings
            from unittest.mock import patch
            with patch('seaborn.boxplot') as mock_boxplot, \
                 patch('seaborn.histplot') as mock_histplot, \
                 patch('seaborn.heatmap') as mock_heatmap:
                
                system.run_basic_statistics()
            
            print("\n" + "="*60)
            print("✅ TEST COMPLETED SUCCESSFULLY!")
            print("="*60)
            
            # Check if results were saved
            assert 'comprehensive_basic_statistics' in system.current_results, "Results not saved"
            
            results = system.current_results['comprehensive_basic_statistics']
            assert 'basic_stats' in results, "Basic stats not found"
            assert 'descriptive_stats' in results, "Descriptive stats not found"
            assert 'distribution_analysis' in results, "Distribution analysis not found"
            assert 'outlier_analysis' in results, "Outlier analysis not found"
            
            # Check that we have the expected structure
            assert 'summary' in results, "Summary not found in large dataset results"
            
            print("✅ Large dataset test passed!")
            
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            pytest.fail(f"Test failed: {e}")
    
    def test_error_handling(self):
        """Test error handling in run_basic_statistics"""
        print("🧪 Testing error handling in run_basic_statistics...")
        
        # Create InteractiveSystem instance without data
        system = InteractiveSystem()
        system.current_data = None
        
        # Test the function should handle None data gracefully
        try:
            system.run_basic_statistics()
            # Should print error message and return early
            print("✅ Error handling test passed!")
        except Exception as e:
            print(f"❌ Error handling test failed: {e}")
            pytest.fail(f"Error handling test failed: {e}")


if __name__ == "__main__":
    # Run tests manually
    test_instance = TestBasicStatisticsFix()
    
    print("🧪 Running basic statistics fix tests...")
    
    try:
        test_instance.test_basic_statistics_fix()
        test_instance.test_large_dataset_handling()
        test_instance.test_error_handling()
        print("\n🎉 All tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Tests failed: {e}")
        sys.exit(1)
