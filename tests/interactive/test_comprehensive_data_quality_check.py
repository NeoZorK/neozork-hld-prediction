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

from src.interactive import InteractiveSystem


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
        
        with patch('builtins.print') as mock_print:
            system.analysis_runner.run_comprehensive_data_quality_check(system)
            
            # Check that the function runs without errors
            # Look for expected output patterns
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Check for key output messages
            assert any("COMPREHENSIVE DATA QUALITY CHECK" in str(call) for call in output_calls)
            assert any("Running comprehensive data quality checks" in str(call) for call in output_calls)
            assert any("DateTime columns found" in str(call) for call in output_calls)
            assert any("QUALITY CHECK SUMMARY" in str(call) for call in output_calls)
    
    def test_datetime_column_detection(self, system, test_data):
        """Test DateTime column detection functionality."""
        system.current_data = test_data
        
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='skip'):
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                
                # Check that datetime columns are detected
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("DateTime columns found: ['datetime']" in str(call) for call in output_calls)
    
    def test_datetime_column_missing(self, system):
        """Test behavior when no DateTime columns are present."""
        # Create data without datetime column
        data = {
            'open': [100 + i for i in range(50)],
            'high': [105 + i for i in range(50)],
            'low': [95 + i for i in range(50)],
            'close': [102 + i for i in range(50)],
            'volume': [1000 for _ in range(50)]
        }
        df = pd.DataFrame(data)
        system.current_data = df
        
        with patch('builtins.print') as mock_print:
            system.analysis_runner.run_comprehensive_data_quality_check(system)
            
            # Check that warning is shown
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("No DateTime columns found" in str(call) for call in output_calls)
    
    def test_quality_issues_detection(self, system, test_data):
        """Test that quality issues are properly detected."""
        system.current_data = test_data
        
        with patch('builtins.print') as mock_print:
            system.analysis_runner.run_comprehensive_data_quality_check(system)
            
            # Check that issues are detected
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should detect various issues
            assert any("NaN issues:" in str(call) for call in output_calls)
            assert any("Duplicate issues:" in str(call) for call in output_calls)
            assert any("Zero value issues:" in str(call) for call in output_calls)
            assert any("Negative value issues:" in str(call) for call in output_calls)
            assert any("Infinity issues:" in str(call) for call in output_calls)
    
    def test_menu_tracking(self, system, test_data):
        """Test that menu tracking works correctly."""
        system.current_data = test_data
        
        # Check initial state
        assert not system.menu_manager.used_menus['eda']['comprehensive_data_quality_check']
        
        with patch('builtins.print'):
            with patch('builtins.input', return_value='skip'):
                system.analysis_runner.run_comprehensive_data_quality_check(system)
        
        # Check that menu item is marked as used
        assert system.menu_manager.used_menus['eda']['comprehensive_data_quality_check']
    
    def test_results_storage(self, system, test_data):
        """Test that results are properly stored."""
        system.current_data = test_data
        
        with patch('builtins.print'):
            with patch('builtins.input', return_value='skip'):
                system.analysis_runner.run_comprehensive_data_quality_check(system)
        
        # Check that results are stored
        assert 'comprehensive_data_quality' in system.current_results
        
        results = system.current_results['comprehensive_data_quality']
        assert 'nan_issues' in results
        assert 'duplicate_issues' in results
        assert 'gap_issues' in results
        assert 'zero_issues' in results
        assert 'negative_issues' in results
        assert 'infinity_issues' in results
        assert 'total_issues' in results
        assert 'datetime_columns' in results
        assert 'data_shape' in results
    
    def test_error_handling(self, system, test_data):
        """Test error handling in comprehensive data quality check."""
        system.current_data = test_data
        
        # Mock an error in the data quality module
        with patch('src.eda.data_quality.nan_check', side_effect=Exception("Test error")):
            with patch('builtins.print') as mock_print:
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                
                # Check that error is handled gracefully
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("Error in comprehensive data quality check" in str(call) for call in output_calls)
    
    def test_fix_all_issues_choice(self, system, test_data):
        """Test the 'fix all issues' functionality."""
        system.current_data = test_data
        
        # Mock user input to choose 'y' for fixing all issues
        with patch('builtins.input', return_value='y'):
            with patch('builtins.print') as mock_print:
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                
                # Check that fixing process is initiated
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("FIXING ALL DETECTED ISSUES" in str(call) for call in output_calls)
    
    def test_skip_fixing_choice(self, system, test_data):
        """Test the 'skip fixing' functionality."""
        system.current_data = test_data
        
        # Mock user input to choose 'skip' for skipping fixes
        with patch('builtins.input', return_value='skip'):
            with patch('builtins.print') as mock_print:
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                
                # Check that skipping message is shown
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("Skipping fixes for now" in str(call) for call in output_calls)
    
    def test_backward_compatibility(self, system):
        """Test that the new functionality doesn't break existing features."""
        # Test that the original data quality check still works
        assert hasattr(system, 'run_data_quality_check')
        assert hasattr(system, 'run_comprehensive_data_quality_check')
        
        # Test that both methods are different
        assert system.run_data_quality_check != system.run_comprehensive_data_quality_check
    
    def test_timestamp_conversion(self, system):
        """Test timestamp column conversion functionality."""
        # Create data with timestamp column (integer)
        timestamps = [int(datetime(2023, 1, 1).timestamp()) + i * 3600 for i in range(50)]
        data = {
            'time_col': timestamps,  # Use different name to avoid auto-conversion
            'open': [100 + i for i in range(50)],
            'high': [105 + i for i in range(50)],
            'low': [95 + i for i in range(50)],
            'close': [102 + i for i in range(50)],
            'volume': [1000 for _ in range(50)]
        }
        df = pd.DataFrame(data)
        system.current_data = df
        
        # Mock user input to convert timestamp
        with patch('builtins.input', return_value='y'):
            with patch('builtins.print') as mock_print:
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                
                # Check that conversion was attempted
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                # Just check that the function runs without error
                assert len(output_calls) > 0
    
    def test_fixes_verification(self, system, test_data):
        """Test that fixes are properly verified after application."""
        system.current_data = test_data
        
        # Mock user input to fix all issues
        with patch('builtins.input', return_value='y'):
            with patch('builtins.print') as mock_print:
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                
                # Check that verification was performed
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("Verifying fixes" in str(call) for call in output_calls)
                assert any("All issues have been successfully resolved" in str(call) for call in output_calls)
    
    def test_one_try_fix(self, system):
        """Test that all issues are fixed in one try."""
        # Create test data with multiple issues
        dates = pd.date_range('2023-01-01', periods=50, freq='h')
        data = {
            'datetime': dates,
            'open': [100 + i for i in range(50)],
            'high': [105 + i for i in range(50)],
            'low': [95 + i for i in range(50)],
            'close': [102 + i for i in range(50)],
            'volume': [1000 for _ in range(50)],
            'source_file': ['test.parquet'] * 50
        }
        df = pd.DataFrame(data)
        
        # Add issues
        df.loc[10, 'open'] = np.nan
        df.loc[20, 'high'] = np.nan
        df.loc[30] = df.loc[29]  # Duplicate
        df.loc[40, 'low'] = -5   # Negative
        
        system.current_data = df
        
        # Mock user input to fix all issues
        with patch('builtins.input', return_value='y'):
            with patch('builtins.print') as mock_print:
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                
                # Check that all fixes were applied
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                
                # Should have applied fixes
                assert any("FIXING ALL DETECTED ISSUES" in str(call) for call in output_calls)
                assert any("All issues have been fixed" in str(call) for call in output_calls)
                
                # Should have verified fixes
                assert any("Verifying fixes" in str(call) for call in output_calls)
                
                # Check that data was actually fixed
                assert system.current_data.isna().sum().sum() == 0, "NaN values should be fixed"
                assert system.current_data.duplicated().sum() == 0, "Duplicates should be fixed"
                assert (system.current_data['low'] < 0).sum() == 0, "Negative values should be fixed"


if __name__ == "__main__":
    pytest.main([__file__])
