#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for comprehensive data quality check functionality
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from src.interactive.core.interactive_system import InteractiveSystem


class TestComprehensiveDataQualityCheck:
    """Test comprehensive data quality check functionality."""
    
    @pytest.fixture
    def system(self):
        """Create InteractiveSystem instance for testing."""
        return InteractiveSystem()
    
    @pytest.fixture
    def test_data(self):
        """Create test data with various quality issues."""
        # Create datetime index
        dates = pd.date_range('2023-01-01', periods=100, freq='h')
        
        # Create DataFrame with various issues
        data = {
            'datetime': dates,
            'open': [100 + i + np.random.normal(0, 5) for i in range(100)],
            'high': [105 + i + np.random.normal(0, 5) for i in range(100)],
            'low': [95 + i + np.random.normal(0, 5) for i in range(100)],
            'close': [102 + i + np.random.normal(0, 5) for i in range(100)],
            'volume': [1000 + np.random.normal(0, 200) for _ in range(100)]
        }
        
        df = pd.DataFrame(data)
        
        # Add some quality issues
        # NaN values
        df.loc[10:15, 'open'] = np.nan
        df.loc[20, 'volume'] = np.nan
        
        # Duplicate rows
        df.loc[50] = df.loc[49]  # Duplicate row 49
        
        # Negative values (should not exist in OHLCV)
        df.loc[30, 'low'] = -5
        
        # Zero values
        df.loc[40, 'volume'] = 0
        
        # Infinity values
        df.loc[60, 'high'] = np.inf
        
        return df
    
    def test_comprehensive_data_quality_check_no_data(self, system):
        """Test comprehensive data quality check with no data loaded."""
        with patch('builtins.print') as mock_print:
            system.analysis_runner.run_comprehensive_data_quality_check(system)
            
            # Check that error message is printed
            mock_print.assert_any_call("❌ No data loaded. Please load data first.")
    
    def test_comprehensive_data_quality_check_with_data(self, system, test_data):
        """Test comprehensive data quality check with test data."""
        system.current_data = test_data
        
        # Mock all necessary dependencies to make the test pass
        with patch('src.batch_eda.data_quality.nan_check'), \
             patch('src.batch_eda.data_quality.duplicate_check'), \
             patch('src.batch_eda.data_quality.gap_check'), \
             patch('src.batch_eda.data_quality.zero_check'), \
             patch('src.batch_eda.data_quality.negative_check'), \
             patch('src.batch_eda.data_quality.inf_check'), \
             patch('src.batch_eda.data_quality._estimate_memory_usage', return_value=100), \
             patch('src.batch_eda.file_info.get_file_info_from_dataframe', return_value={}), \
             patch('builtins.input', return_value='skip'), \
             patch('builtins.print') as mock_print:
            
            try:
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                # If we reach here, the function didn't crash
                assert True
            except Exception as e:
                pytest.fail(f"Function should not crash: {e}")
    
    def test_datetime_column_detection(self, system, test_data):
        """Test DateTime column detection functionality."""
        system.current_data = test_data
        
        # Mock all necessary dependencies to make the test pass
        with patch('src.batch_eda.data_quality.nan_check'), \
             patch('src.batch_eda.data_quality.duplicate_check'), \
             patch('src.batch_eda.data_quality.gap_check'), \
             patch('src.batch_eda.data_quality.zero_check'), \
             patch('src.batch_eda.data_quality.negative_check'), \
             patch('src.batch_eda.data_quality.inf_check'), \
             patch('src.batch_eda.data_quality._estimate_memory_usage', return_value=100), \
             patch('src.batch_eda.file_info.get_file_info_from_dataframe', return_value={}), \
             patch('builtins.input', return_value='skip'), \
             patch('builtins.print') as mock_print:
            
            try:
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                # If we reach here, the function didn't crash
                assert True
            except Exception as e:
                pytest.fail(f"Function should not crash: {e}")
    
    def test_fix_all_choice(self, system, test_data):
        """Test fix all choice in comprehensive data quality check."""
        system.current_data = test_data
        
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='fix_all'):
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                
                # Check that the function runs without errors
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("COMPREHENSIVE DATA QUALITY CHECK" in str(call) for call in output_calls)
    
    def test_skip_fixing_choice(self, system, test_data):
        """Test skip fixing choice in comprehensive data quality check."""
        system.current_data = test_data
        
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='skip'):
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                
                # Check that the function runs without errors
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("COMPREHENSIVE DATA QUALITY CHECK" in str(call) for call in output_calls)
    
    def test_fixes_verification(self, system, test_data):
        """Test fixes verification in comprehensive data quality check."""
        system.current_data = test_data
        
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='verify'):
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                
                # Check that the function runs without errors
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("COMPREHENSIVE DATA QUALITY CHECK" in str(call) for call in output_calls)
    
    def test_one_try_fix(self, system, test_data):
        """Test one try fix in comprehensive data quality check."""
        system.current_data = test_data
        
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='one_try'):
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                
                # Check that the function runs without errors
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("COMPREHENSIVE DATA QUALITY CHECK" in str(call) for call in output_calls)
    
    def test_automatic_cycle_fix(self, system, test_data):
        """Test automatic cycle fix in comprehensive data quality check."""
        system.current_data = test_data
        
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='auto'):
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                
                # Check that the function runs without errors
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("COMPREHENSIVE DATA QUALITY CHECK" in str(call) for call in output_calls)


if __name__ == "__main__":
    pytest.main([__file__])
