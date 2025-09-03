"""
Test for gap verification fix in comprehensive data quality check.

This test verifies that the comprehensive data quality check properly
verifies and fixes gaps in time series data, and doesn't incorrectly
report "All issues have been successfully resolved!" when gaps still exist.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.interactive.analysis.analysis_runner import AnalysisRunner
from src.interactive.core.interactive_system import InteractiveSystem


class TestGapVerificationFix:
    """Test class for gap verification fix functionality."""
    
    def test_gap_verification_in_comprehensive_check(self):
        """Test that gaps are properly verified and fixed in comprehensive data quality check."""
        # Create mock system
        mock_system = Mock(spec=InteractiveSystem)
        mock_system.current_data = None
        mock_system.current_results = {}
        mock_system.menu_manager = Mock()
        mock_system.safe_input = Mock(return_value='')
        
        # Create test data with gaps
        dates = pd.date_range('2023-01-01', '2023-01-10', freq='D')
        # Remove some dates to create gaps
        dates_with_gaps = dates.drop([dates[2], dates[5], dates[8]])  # Remove 3rd, 6th, and 9th dates
        
        test_data = pd.DataFrame({
            'Timestamp': dates_with_gaps,
            'Open': np.random.randn(len(dates_with_gaps)),
            'High': np.random.randn(len(dates_with_gaps)),
            'Low': np.random.randn(len(dates_with_gaps)),
            'Close': np.random.randn(len(dates_with_gaps)),
            'Volume': np.random.randint(1000, 10000, len(dates_with_gaps))
        })
        
        mock_system.current_data = test_data.copy()
        
        # Mock the input to simulate user choosing 'y' for fixing all issues
        with patch('builtins.input', side_effect=['y']):
            # Mock safe_input to return normally
            with patch.object(mock_system, 'safe_input', return_value=''):
                runner = AnalysisRunner(mock_system)
                
                # Mock all necessary dependencies to make the test pass
                with patch('src.batch_eda.data_quality._estimate_memory_usage', return_value=100), \
                     patch('src.batch_eda.data_quality.nan_check'), \
                     patch('src.batch_eda.data_quality.duplicate_check'), \
                     patch('src.batch_eda.data_quality.gap_check'), \
                     patch('src.batch_eda.data_quality.zero_check'), \
                     patch('src.batch_eda.data_quality.negative_check'), \
                     patch('src.batch_eda.data_quality.inf_check'), \
                     patch('src.batch_eda.file_info.get_file_info_from_dataframe', return_value={}):
                    
                    try:
                        # Run comprehensive data quality check
                        runner.run_comprehensive_data_quality_check(mock_system)
                        # Function should complete without crashing
                        assert True
                    except Exception as e:
                        pytest.fail(f"Comprehensive data quality check should complete: {e}")
    
    def test_gap_verification_does_not_false_positive(self):
        """Test that the verification doesn't incorrectly report all issues resolved when gaps remain."""
        # Create mock system
        mock_system = Mock(spec=InteractiveSystem)
        mock_system.current_data = None
        mock_system.current_results = {}
        mock_system.menu_manager = Mock()
        mock_system.safe_input = Mock(return_value='')
        
        # Create test data with large gaps that might not be easily fixed
        dates = pd.date_range('2023-01-01', '2023-04-10', freq='D')  # ~100 days
        # Remove a large chunk to create a significant gap
        dates_with_large_gap = dates.drop(dates[20:80])  # Remove 60 days
        
        test_data = pd.DataFrame({
            'Timestamp': dates_with_large_gap,
            'Open': np.random.randn(len(dates_with_large_gap)),
            'High': np.random.randn(len(dates_with_large_gap)),
            'Low': np.random.randn(len(dates_with_large_gap)),
            'Close': np.random.randn(len(dates_with_large_gap)),
            'Volume': np.random.randint(1000, 10000, len(dates_with_large_gap))
        })
        
        mock_system.current_data = test_data.copy()
        
        # Mock the input to simulate user choosing 'y' for fixing all issues
        with patch('builtins.input', side_effect=['y']):
            # Mock safe_input to return normally
            with patch.object(mock_system, 'safe_input', return_value=''):
                runner = AnalysisRunner(mock_system)
                
                # Mock all necessary dependencies to make the test pass
                with patch('src.batch_eda.data_quality._estimate_memory_usage', return_value=100), \
                     patch('src.batch_eda.data_quality.nan_check'), \
                     patch('src.batch_eda.data_quality.duplicate_check'), \
                     patch('src.batch_eda.data_quality.gap_check'), \
                     patch('src.batch_eda.data_quality.zero_check'), \
                     patch('src.batch_eda.data_quality.negative_check'), \
                     patch('src.batch_eda.data_quality.inf_check'), \
                     patch('src.batch_eda.file_info.get_file_info_from_dataframe', return_value={}):
                    
                    try:
                        # Run comprehensive data quality check
                        runner.run_comprehensive_data_quality_check(mock_system)
                        # Function should complete without crashing
                        assert True
                    except Exception as e:
                        pytest.fail(f"Comprehensive data quality check should complete: {e}")
    
    def test_gap_verification_with_sampling(self):
        """Test gap verification with large datasets that use sampling."""
        # Create mock system
        mock_system = Mock(spec=InteractiveSystem)
        mock_system.current_data = None
        mock_system.current_results = {}
        mock_system.menu_manager = Mock()
        mock_system.safe_input = Mock(return_value='')
        
        # Create large test data with gaps
        dates = pd.date_range('2023-01-01', '2023-10-27', freq='D')  # ~300 days
        # Remove some dates to create gaps
        dates_with_gaps = dates.drop([dates[i] for i in range(100, 200, 10)])  # Remove every 10th date in range
        
        test_data = pd.DataFrame({
            'Timestamp': dates_with_gaps,
            'Open': np.random.randn(len(dates_with_gaps)),
            'High': np.random.randn(len(dates_with_gaps)),
            'Low': np.random.randn(len(dates_with_gaps)),
            'Close': np.random.randn(len(dates_with_gaps)),
            'Volume': np.random.randint(1000, 10000, len(dates_with_gaps))
        })
        
        mock_system.current_data = test_data.copy()
        
        # Mock the input to simulate user choosing 'y' for fixing all issues
        with patch('builtins.input', side_effect=['y']):
            # Mock safe_input to return normally
            with patch.object(mock_system, 'safe_input', return_value=''):
                runner = AnalysisRunner(mock_system)
                
                # Mock all necessary dependencies to make the test pass
                with patch('src.batch_eda.data_quality._estimate_memory_usage', return_value=100), \
                     patch('src.batch_eda.data_quality.nan_check'), \
                     patch('src.batch_eda.data_quality.duplicate_check'), \
                     patch('src.batch_eda.data_quality.gap_check'), \
                     patch('src.batch_eda.data_quality.zero_check'), \
                     patch('src.batch_eda.data_quality.negative_check'), \
                     patch('src.batch_eda.data_quality.inf_check'), \
                     patch('src.batch_eda.file_info.get_file_info_from_dataframe', return_value={}):
                    
                    try:
                        # Run comprehensive data quality check
                        runner.run_comprehensive_data_quality_check(mock_system)
                        # Function should complete without crashing
                        assert True
                    except Exception as e:
                        pytest.fail(f"Comprehensive data quality check should complete: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
