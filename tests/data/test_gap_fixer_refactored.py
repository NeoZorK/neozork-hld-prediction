# File: tests/data/test_gap_fixer_refactored.py
# -*- coding: utf-8 -*-

"""
Tests for refactored gap fixer modules.
Ensures all functionality remains working after refactoring.
All comments are in English.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import tempfile
import os

# Import the refactored modules
from src.data.gap_fixer_core import GapFixer
from src.data.gap_fixer_algorithms import GapFixingAlgorithms
from src.data.gap_fixer_utils import GapFixingUtils
from src.data.gap_fixer_explanation import (
    explain_why_fix_gaps, get_gap_fixing_benefits, 
    get_gap_fixing_methods, get_gap_detection_metrics
)


class TestGapFixerRefactored:
    """Test class for refactored gap fixer functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.gap_fixer = GapFixer(memory_limit_mb=1024)
        self.algorithms = GapFixingAlgorithms()
        self.utils = GapFixingUtils()
        
        # Create test data
        self.test_data = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01', periods=100, freq='1H'),
            'open': [100.0 + i * 0.1 for i in range(100)],
            'high': [110.0 + i * 0.1 for i in range(100)],
            'low': [90.0 + i * 0.1 for i in range(100)],
            'close': [105.0 + i * 0.1 for i in range(100)],
            'volume': [1000 + i * 10 for i in range(100)]
        })
        
        # Create data with gaps
        self.gapped_data = self.test_data.copy()
        # Remove some rows to create gaps
        self.gapped_data = self.gapped_data.drop([10, 20, 30, 40, 50])
    
    def test_gap_fixer_initialization(self):
        """Test GapFixer initialization."""
        assert self.gap_fixer.memory_limit_mb == 1024
        assert self.gap_fixer.supported_formats == ['.parquet', '.csv', '.json']
        assert hasattr(self.gap_fixer, 'algorithms')
        assert hasattr(self.gap_fixer, 'utils')
    
    def test_algorithms_initialization(self):
        """Test GapFixingAlgorithms initialization."""
        assert hasattr(self.algorithms, 'algorithms')
        expected_methods = ['linear', 'cubic', 'forward_fill', 'backward_fill', 
                           'interpolate', 'seasonal', 'ml_forecast']
        for method in expected_methods:
            assert method in self.algorithms.algorithms
    
    def test_utils_initialization(self):
        """Test GapFixingUtils initialization."""
        assert hasattr(self.utils, 'load_file')
        assert hasattr(self.utils, 'find_timestamp_column')
        assert hasattr(self.utils, 'detect_gaps')
    
    def test_find_timestamp_column(self):
        """Test timestamp column detection."""
        # Test with regular timestamp column
        df = self.test_data.copy()
        timestamp_col = self.utils.find_timestamp_column(df)
        assert timestamp_col == 'timestamp'
        
        # Test with DatetimeIndex
        df_indexed = df.set_index('timestamp')
        timestamp_col = self.utils.find_timestamp_column(df_indexed)
        assert timestamp_col == "DATETIME_INDEX"
        
        # Test with different column names
        df_renamed = df.rename(columns={'timestamp': 'time'})
        timestamp_col = self.utils.find_timestamp_column(df_renamed)
        assert timestamp_col == 'time'
        
        # Test with datetime column
        df_datetime = df.rename(columns={'timestamp': 'custom_name'})
        df_datetime['custom_name'] = pd.to_datetime(df_datetime['custom_name'])
        timestamp_col = self.utils.find_timestamp_column(df_datetime)
        assert timestamp_col == 'custom_name'
    
    def test_convert_datetime_index_to_column(self):
        """Test DatetimeIndex to column conversion."""
        df_indexed = self.test_data.set_index('timestamp')
        converted_df = self.utils.convert_datetime_index_to_column(df_indexed)
        
        # After reset_index, the timestamp column should be back in columns
        assert 'timestamp' in converted_df.columns or 'Timestamp' in converted_df.columns
        assert len(converted_df) == len(self.test_data)
    
    def test_detect_gaps(self):
        """Test gap detection functionality."""
        # Test with data without gaps
        gap_info = self.utils.detect_gaps(self.test_data, 'timestamp')
        assert gap_info['has_gaps'] == False  # Use == instead of is for numpy boolean
        assert gap_info['gap_count'] == 0
        assert gap_info['total_rows'] == 100
        assert 'time_range' in gap_info
        assert 'expected_frequency' in gap_info
        
        # Test with gapped data
        gap_info = self.utils.detect_gaps(self.gapped_data, 'timestamp')
        assert gap_info['has_gaps'] == True  # Use == instead of is for numpy boolean
        assert gap_info['gap_count'] > 0
        assert gap_info['total_rows'] == 95  # 100 - 5 removed rows
    
    def test_determine_expected_frequency(self):
        """Test expected frequency determination."""
        # Create time differences
        time_diffs = pd.Series([
            pd.Timedelta('1H'), pd.Timedelta('1H'), pd.Timedelta('1H')
        ])
        
        freq = self.utils._determine_expected_frequency(time_diffs)
        assert freq == pd.Timedelta('1H')
        
        # Test with empty series
        empty_diffs = pd.Series(dtype='timedelta64[ns]')
        freq = self.utils._determine_expected_frequency(empty_diffs)
        assert freq == pd.Timedelta('1H')  # Default value
    
    def test_memory_management(self):
        """Test memory management utilities."""
        # Test memory usage
        memory_usage = self.utils.get_memory_usage()
        assert isinstance(memory_usage, float)
        assert memory_usage >= 0
        
        # Test memory availability check
        available = self.utils.check_memory_available(1024)
        assert isinstance(available, bool)
    
    def test_estimate_processing_time(self):
        """Test processing time estimation."""
        file_paths = [Path('/dummy/path1.csv'), Path('/dummy/path2.csv')]
        
        # Mock file loading and gap detection
        with patch.object(self.utils, 'load_file') as mock_load, \
             patch.object(self.utils, 'find_timestamp_column') as mock_find, \
             patch.object(self.utils, 'detect_gaps') as mock_detect:
            
            mock_load.return_value = self.test_data
            mock_find.return_value = 'timestamp'
            mock_detect.return_value = {
                'gap_count': 5,
                'total_rows': 100
            }
            
            estimated_time = self.utils.estimate_total_processing_time(file_paths)
            assert isinstance(estimated_time, str)
            assert 'seconds' in estimated_time or 'minutes' in estimated_time or 'hours' in estimated_time
    
    def test_file_operations(self):
        """Test file operations utilities."""
        # Test backup creation
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            f.write(b"test,data\n1,2\n")
            temp_file = Path(f.name)
        
        try:
            backup_path = self.utils.create_backup(temp_file)
            assert backup_path.exists()
            assert 'backup' in backup_path.name
            assert backup_path.suffix == '.csv'
            
            # Clean up backup
            backup_path.unlink()
            
        finally:
            # Clean up temp file
            if temp_file.exists():
                temp_file.unlink()
    
    def test_save_fixed_data(self):
        """Test data saving functionality."""
        # Test saving as CSV
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            temp_file = Path(f.name)
        
        try:
            success = self.utils.save_fixed_data(self.test_data, temp_file)
            assert success is True
            assert temp_file.exists()
            assert temp_file.stat().st_size > 0
            
        finally:
            if temp_file.exists():
                temp_file.unlink()
    
    def test_algorithm_selection(self):
        """Test algorithm selection logic."""
        # Test with low gap ratio
        gap_info_low = {'gap_count': 1, 'total_rows': 1000}
        algorithm = self.algorithms._select_best_algorithm(gap_info_low)
        assert algorithm == 'linear'
        
        # Test with medium gap ratio
        gap_info_medium = {'gap_count': 50, 'total_rows': 1000}
        algorithm = self.algorithms._select_best_algorithm(gap_info_medium)
        assert algorithm == 'cubic'
        
        # Test with high gap ratio
        gap_info_high = {'gap_count': 200, 'total_rows': 1000}
        algorithm = self.algorithms._select_best_algorithm(gap_info_high)
        assert algorithm == 'seasonal'
    
    def test_linear_interpolation(self):
        """Test linear interpolation algorithm."""
        gap_info = {
            'time_range': {'start': pd.Timestamp('2024-01-01'), 'end': pd.Timestamp('2024-01-01 23:00:00')},
            'expected_frequency': pd.Timedelta('1H'),
            'gap_count': 5
        }
        
        result_df = self.algorithms._fix_gaps_linear(
            self.gapped_data, 'timestamp', gap_info, False
        )
        
        assert result_df is not None
        # The result should have 24 rows (24 hours from 00:00 to 23:00)
        assert len(result_df) == 24
        assert 'timestamp' in result_df.columns
    
    def test_cubic_interpolation(self):
        """Test cubic interpolation algorithm."""
        gap_info = {
            'time_range': {'start': pd.Timestamp('2024-01-01'), 'end': pd.Timestamp('2024-01-01 23:00:00')},
            'expected_frequency': pd.Timedelta('1H'),
            'gap_count': 5
        }
        
        result_df = self.algorithms._fix_gaps_cubic(
            self.gapped_data, 'timestamp', gap_info, False
        )
        
        assert result_df is not None
        # The result should have 24 rows (24 hours from 00:00 to 23:00)
        assert len(result_df) == 24
        assert 'timestamp' in result_df.columns
    
    def test_forward_fill(self):
        """Test forward fill algorithm."""
        gap_info = {'gap_count': 5}
        
        result_df = self.algorithms._fix_gaps_forward_fill(
            self.gapped_data, 'timestamp', gap_info, False
        )
        
        assert result_df is not None
        assert len(result_df) == len(self.gapped_data)
        assert 'timestamp' in result_df.columns
    
    def test_backward_fill(self):
        """Test backward fill algorithm."""
        gap_info = {'gap_count': 5}
        
        result_df = self.algorithms._fix_gaps_backward_fill(
            self.gapped_data, 'timestamp', gap_info, False
        )
        
        assert result_df is not None
        assert len(result_df) == len(self.gapped_data)
        assert 'timestamp' in result_df.columns
    
    def test_interpolate_algorithm(self):
        """Test interpolate algorithm."""
        gap_info = {'gap_count': 5}
        
        result_df = self.algorithms._fix_gaps_interpolate(
            self.gapped_data, 'timestamp', gap_info, False
        )
        
        assert result_df is not None
        assert len(result_df) == len(self.gapped_data)
        assert 'timestamp' in result_df.columns
    
    def test_seasonal_algorithm(self):
        """Test seasonal algorithm."""
        gap_info = {
            'time_range': {'start': pd.Timestamp('2024-01-01'), 'end': pd.Timestamp('2024-01-01 23:00:00')},
            'expected_frequency': pd.Timedelta('1H'),
            'gap_count': 5
        }
        
        result_df = self.algorithms._fix_gaps_seasonal(
            self.gapped_data, 'timestamp', gap_info, False
        )
        
        assert result_df is not None
        # The result should have 24 rows (24 hours from 00:00 to 23:00)
        assert len(result_df) == 24
        assert 'timestamp' in result_df.columns
    
    def test_chunked_algorithm(self):
        """Test chunked algorithm for large datasets."""
        gap_info = {
            'time_range': {'start': pd.Timestamp('2024-01-01'), 'end': pd.Timestamp('2024-01-01 23:00:00')},
            'expected_frequency': pd.Timedelta('1H'),
            'gap_count': 5
        }
        
        result_df = self.algorithms._fix_gaps_chunked(
            self.gapped_data, 'timestamp', gap_info, False
        )
        
        assert result_df is not None
        assert len(result_df) == len(self.gapped_data)
        assert 'timestamp' in result_df.columns
    
    def test_explanation_functions(self):
        """Test explanation module functions."""
        # Test main explanation
        explanation = explain_why_fix_gaps()
        assert isinstance(explanation, str)
        assert "WHY TIME SERIES GAPS NEED TO BE FIXED" in explanation
        
        # Test benefits
        benefits = get_gap_fixing_benefits()
        assert isinstance(benefits, dict)
        assert 'data_quality' in benefits
        assert 'analysis_accuracy' in benefits
        assert 'ml_performance' in benefits
        assert 'performance' in benefits
        
        # Test methods
        methods = get_gap_fixing_methods()
        assert isinstance(methods, dict)
        assert 'linear' in methods
        assert 'cubic' in methods
        assert 'forward_fill' in methods
        
        # Test metrics
        metrics = get_gap_detection_metrics()
        assert isinstance(metrics, dict)
        assert 'gap_count' in metrics
        assert 'gap_ratio' in metrics
        assert 'data_completeness' in metrics
    
    def test_memory_usage_tracking(self):
        """Test memory usage tracking in algorithms."""
        gap_info = {
            'gap_count': 5,
            'time_range': {'start': pd.Timestamp('2024-01-01'), 'end': pd.Timestamp('2024-01-01 23:00:00')},
            'expected_frequency': pd.Timedelta('1H')
        }
        
        # Mock memory usage functions
        with patch.object(self.algorithms, '_get_memory_usage') as mock_memory:
            mock_memory.side_effect = [100.0, 150.0]  # Initial and final memory
            
            result_df, results = self.algorithms.fix_gaps_in_dataframe(
                self.gapped_data, 'timestamp', gap_info, 'linear', False
            )
            
            assert 'memory_used_mb' in results
            assert results['memory_used_mb'] == 50.0  # 150 - 100
    
    def test_progress_bar_support(self):
        """Test progress bar support in algorithms."""
        gap_info = {
            'gap_count': 5,
            'time_range': {'start': pd.Timestamp('2024-01-01'), 'end': pd.Timestamp('2024-01-01 23:00:00')},
            'expected_frequency': pd.Timedelta('1H')
        }
        
        # Test with progress bar
        mock_progress_bar = Mock()
        mock_progress_bar.set_description = Mock()
        mock_progress_bar.update = Mock()
        
        result_df = self.algorithms._fix_gaps_linear(
            self.gapped_data, 'timestamp', gap_info, True, mock_progress_bar
        )
        
        # Verify progress bar was used
        mock_progress_bar.set_description.assert_called()
        mock_progress_bar.update.assert_called_with(5)


if __name__ == "__main__":
    pytest.main([__file__])
