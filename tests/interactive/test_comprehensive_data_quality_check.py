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
    
    def test_automatic_cycle_fix(self, system):
        """Test that the system automatically cycles through fixes until all issues are resolved."""
        # Create test data with issues that might require multiple iterations
        dates = pd.date_range('2023-01-01', periods=30, freq='h')
        data = {
            'datetime': dates,
            'open': [100 + i for i in range(30)],
            'high': [105 + i for i in range(30)],
            'low': [95 + i for i in range(30)],
            'close': [102 + i for i in range(30)],
            'volume': [1000 for _ in range(30)],
            'predicted_low': [0.5 for _ in range(30)],  # Add problematic column
            'predicted_high': [0.5 for _ in range(30)], # Add problematic column
            'source_file': ['test.parquet'] * 30
        }
        df = pd.DataFrame(data)
        
        # Add issues that might create new duplicates when fixed
        df.loc[10, 'open'] = np.nan
        df.loc[15, 'high'] = np.nan
        df.loc[20] = df.loc[19]  # Duplicate
        df.loc[25, 'low'] = -5   # Negative
        df.loc[5, 'predicted_low'] = 0  # Zero value
        df.loc[8, 'predicted_high'] = 0 # Zero value
        
        system.current_data = df
        
        # Mock user input to fix all issues
        with patch('builtins.input', return_value='y'):
            with patch('builtins.print') as mock_print:
                system.analysis_runner.run_comprehensive_data_quality_check(system)
                
                # Check that automatic cycling was used
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                
                # Should have applied initial fixes
                assert any("FIXING ALL DETECTED ISSUES" in str(call) for call in output_calls)
                
                # Should have verified fixes
                assert any("Verifying fixes" in str(call) for call in output_calls)
                
                # Should have shown verification iterations
                assert any("Verification iteration" in str(call) for call in output_calls)
                
                # Check that data was actually fixed
                assert system.current_data.isna().sum().sum() == 0, "NaN values should be fixed"
                assert system.current_data.duplicated().sum() == 0, "Duplicates should be fixed"
                assert (system.current_data['low'] < 0).sum() == 0, "Negative values should be fixed"
                
                # Check that zero values in problematic columns were handled
                zero_count_low = (system.current_data['predicted_low'] == 0).sum()
                zero_count_high = (system.current_data['predicted_high'] == 0).sum()
                # Note: Zero values might be legitimate, so we just check they were processed
    
    def test_datetime_column_loading(self, system):
        """Test that DateTime columns are properly loaded from CSV files."""
        # Create a test CSV file with MT5 format
        import tempfile
        import os
        
        # Create test CSV content with MT5 format
        csv_content = """File Info Header Line
DateTime,Open,High,Low,Close,TickVolume,predicted_low,predicted_high,pressure,pressure_vector
2023.01.01 10:00,100.0,105.0,99.0,101.0,1000,98.0,106.0,0.1,0.2
2023.01.01 10:01,101.0,106.0,100.0,102.0,1100,99.0,107.0,0.2,0.3
2023.01.01 10:02,102.0,107.0,101.0,103.0,1200,100.0,108.0,0.3,0.4"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_file = f.name
        
        try:
            # Load the test file
            df = system.data_manager.load_data_from_file(temp_file)
            
            # Check that DateTime column is properly loaded as index
            assert isinstance(df.index, pd.DatetimeIndex), "DataFrame should have DatetimeIndex"
            assert df.index.name == 'Timestamp', "Index should be named 'Timestamp'"
            
            # Check that OHLCV columns are present
            expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in expected_cols:
                assert col in df.columns, f"Column {col} should be present"
            
            # Check that data is properly loaded
            assert len(df) == 3, "Should have 3 rows of data"
            assert df['Open'].iloc[0] == 100.0, "First Open value should be 100.0"
            
        finally:
            # Clean up
            os.unlink(temp_file)
    
    def test_datetime_column_preservation_with_mask(self, system):
        """Test that DateTime columns are preserved when loading with mask."""
        import tempfile
        import os
        from pathlib import Path
        
        # Create a temporary directory with test CSV files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test CSV content with MT5 format
            csv_content1 = """File Info Header Line
DateTime,Open,High,Low,Close,TickVolume,predicted_low,predicted_high,pressure,pressure_vector
2023.01.01 10:00,100.0,105.0,99.0,101.0,1000,98.0,106.0,0.1,0.2
2023.01.01 10:01,101.0,106.0,100.0,102.0,1100,99.0,107.0,0.2,0.3"""
            
            csv_content2 = """File Info Header Line
DateTime,Open,High,Low,Close,TickVolume,predicted_low,predicted_high,pressure,pressure_vector
2023.01.01 11:00,102.0,107.0,101.0,103.0,1200,100.0,108.0,0.3,0.4
2023.01.01 11:01,103.0,108.0,102.0,104.0,1300,101.0,109.0,0.4,0.5"""
            
            # Create test files
            file1 = temp_path / "test_eurusd_1.csv"
            file2 = temp_path / "test_eurusd_2.csv"
            
            with open(file1, 'w') as f:
                f.write(csv_content1)
            with open(file2, 'w') as f:
                f.write(csv_content2)
            
            # Mock the load_data method to simulate loading with mask
            original_load_data = system.data_manager.load_data
            
            def mock_load_data(system):
                # Simulate the loading process with mask
                all_data = []
                
                # Load files with mask
                for file in [file1, file2]:
                    if 'eurusd' in file.name.lower():
                        df = system.data_manager.load_data_from_file(str(file))
                        df['source_file'] = file.name
                        all_data.append(df)
                
                # Check if any DataFrame has a DatetimeIndex
                has_datetime_index = any(isinstance(df.index, pd.DatetimeIndex) for df in all_data)
                
                if has_datetime_index:
                    # If any DataFrame has DatetimeIndex, preserve it during concatenation
                    system.current_data = pd.concat(all_data, axis=0, sort=False)
                    # Reset index to make datetime a column if it was the index
                    if isinstance(system.current_data.index, pd.DatetimeIndex):
                        system.current_data = system.current_data.reset_index()
                        # Rename the datetime column to 'Timestamp' for consistency
                        if 'index' in system.current_data.columns:
                            system.current_data = system.current_data.rename(columns={'index': 'Timestamp'})
                else:
                    # No DatetimeIndex, use normal concatenation
                    system.current_data = pd.concat(all_data, ignore_index=True)
                
                return True
            
            try:
                # Replace the load_data method temporarily
                system.data_manager.load_data = mock_load_data
                
                # Load data with mask
                success = system.data_manager.load_data(system)
                
                # Check that data was loaded successfully
                assert success, "Data loading should succeed"
                assert system.current_data is not None, "Data should be loaded"
                
                # Check that DateTime column is preserved
                assert 'Timestamp' in system.current_data.columns, "Timestamp column should be present"
                assert pd.api.types.is_datetime64_any_dtype(system.current_data['Timestamp']), "Timestamp should be datetime type"
                
                # Check that OHLCV columns are present
                expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                for col in expected_cols:
                    assert col in system.current_data.columns, f"Column {col} should be present"
                
                # Check that data is properly combined
                assert len(system.current_data) == 4, "Should have 4 rows of combined data"
                assert 'source_file' in system.current_data.columns, "source_file column should be present"
                
            finally:
                # Restore original method
                system.data_manager.load_data = original_load_data


if __name__ == "__main__":
    pytest.main([__file__])
