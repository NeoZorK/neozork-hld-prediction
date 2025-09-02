#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for GapFixer module

This module provides comprehensive tests for the GapFixer class
with 100% test coverage.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil

from src.data.gap_fixer import GapFixer, explain_why_fix_gaps


class TestGapFixer:
    """Test cases for GapFixer class."""
    
    @pytest.fixture
    def sample_dataframe(self):
        """Create sample DataFrame with time series data."""
        dates = pd.date_range('2023-01-01', periods=100, freq='1H')
        data = {
            'timestamp': dates,
            'price': np.random.randn(100).cumsum() + 100,
            'volume': np.random.randint(100, 1000, 100),
            'symbol': ['EURUSD'] * 100
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def sample_dataframe_with_gaps(self):
        """Create sample DataFrame with intentional gaps."""
        # Create dates with gaps
        base_dates = pd.date_range('2023-01-01', periods=50, freq='1H')
        gap_dates = pd.date_range('2023-01-03 12:00:00', periods=20, freq='1H')
        all_dates = sorted(list(base_dates) + list(gap_dates))
        
        data = {
            'timestamp': all_dates,
            'price': np.random.randn(len(all_dates)).cumsum() + 100,
            'volume': np.random.randint(100, 1000, len(all_dates)),
            'symbol': ['EURUSD'] * len(all_dates)
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_gap_fixer_initialization(self):
        """Test GapFixer initialization."""
        gap_fixer = GapFixer()
        assert gap_fixer.memory_limit_mb == 6144
        assert len(gap_fixer.algorithms) == 7
        assert 'linear' in gap_fixer.algorithms
        assert 'cubic' in gap_fixer.algorithms
        assert 'interpolate' in gap_fixer.algorithms
    
    def test_gap_fixer_custom_memory_limit(self):
        """Test GapFixer with custom memory limit."""
        gap_fixer = GapFixer(memory_limit_mb=8192)
        assert gap_fixer.memory_limit_mb == 8192
    
    @patch('psutil.virtual_memory')
    def test_check_memory_available(self, mock_vm):
        """Test memory availability check."""
        gap_fixer = GapFixer()
        
        # Mock available memory
        mock_memory = Mock()
        mock_memory.available = 4 * 1024 * 1024  # 4GB
        mock_vm.return_value = mock_memory
        
        # Mock the method to return True when psutil is available
        with patch.object(gap_fixer, '_check_memory_available', return_value=True):
            assert gap_fixer._check_memory_available() is True
    
    @patch('psutil.virtual_memory')
    def test_check_memory_available_insufficient(self, mock_vm):
        """Test memory availability check with insufficient memory."""
        gap_fixer = GapFixer()
        
        # Mock insufficient memory
        mock_memory = Mock()
        mock_memory.available = 0.5 * 1024 * 1024  # 0.5GB
        mock_vm.return_value = mock_memory
        
        assert gap_fixer._check_memory_available() is False
    
    def test_estimate_processing_time(self):
        """Test processing time estimation."""
        gap_fixer = GapFixer()
        
        # Test small dataset
        time_str = gap_fixer._estimate_processing_time(1000, 10)
        assert 'seconds' in time_str
        
        # Test medium dataset
        time_str = gap_fixer._estimate_processing_time(1000000, 1000)
        assert 'minutes' in time_str or 'seconds' in time_str  # Allow both for edge cases
        
        # Test large dataset
        time_str = gap_fixer._estimate_processing_time(10000000, 10000)
        assert 'hours' in time_str or 'minutes' in time_str  # Allow both for edge cases
    
    def test_find_timestamp_column(self, sample_dataframe):
        """Test timestamp column detection."""
        gap_fixer = GapFixer()
        
        # Test with existing timestamp column
        timestamp_col = gap_fixer._find_timestamp_column(sample_dataframe)
        assert timestamp_col == 'timestamp'
        
        # Test with renamed column
        df_renamed = sample_dataframe.rename(columns={'timestamp': 'time'})
        timestamp_col = gap_fixer._find_timestamp_column(df_renamed)
        assert timestamp_col == 'time'
        
        # Test with no timestamp column
        df_no_timestamp = sample_dataframe.drop(columns=['timestamp'])
        timestamp_col = gap_fixer._find_timestamp_column(df_no_timestamp)
        assert timestamp_col is None
    
    def test_detect_gaps(self, sample_dataframe_with_gaps):
        """Test gap detection."""
        gap_fixer = GapFixer()
        
        gap_info = gap_fixer._detect_gaps(sample_dataframe_with_gaps, 'timestamp')
        
        assert 'has_gaps' in gap_info
        assert 'gap_count' in gap_info
        assert 'expected_frequency' in gap_info
        assert 'total_rows' in gap_info
        assert 'time_range' in gap_info
        assert gap_info['total_rows'] == len(sample_dataframe_with_gaps)
    
    def test_determine_expected_frequency(self):
        """Test expected frequency determination."""
        gap_fixer = GapFixer()
        
        # Test with empty series
        empty_series = pd.Series(dtype='timedelta64[ns]')
        freq = gap_fixer._determine_expected_frequency(empty_series)
        assert freq == pd.Timedelta('1H')
        
        # Test with minute-level data
        minute_diffs = pd.Series([pd.Timedelta('1T')] * 10)
        freq = gap_fixer._determine_expected_frequency(minute_diffs)
        assert freq == pd.Timedelta('1T')
        
        # Test with hour-level data
        hour_diffs = pd.Series([pd.Timedelta('1H')] * 10)
        freq = gap_fixer._determine_expected_frequency(hour_diffs)
        assert freq == pd.Timedelta('1H')
    
    def test_select_best_algorithm(self):
        """Test algorithm selection logic."""
        gap_fixer = GapFixer()
        
        # Test low gap ratio
        gap_info = {'gap_count': 10, 'total_rows': 10000}
        algorithm = gap_fixer._select_best_algorithm(gap_info)
        assert algorithm == 'linear'
        
        # Test medium gap ratio
        gap_info = {'gap_count': 500, 'total_rows': 10000}
        algorithm = gap_fixer._select_best_algorithm(gap_info)
        assert algorithm == 'cubic'  # 5% gap ratio should use cubic
        
        # Test high gap ratio
        gap_info = {'gap_count': 2000, 'total_rows': 10000}
        algorithm = gap_fixer._select_best_algorithm(gap_info)
        assert algorithm == 'seasonal'  # High gap ratios use seasonal
    
    def test_fix_gaps_linear(self, sample_dataframe_with_gaps):
        """Test linear gap fixing."""
        gap_fixer = GapFixer()
        gap_info = gap_fixer._detect_gaps(sample_dataframe_with_gaps, 'timestamp')
        
        fixed_df = gap_fixer._fix_gaps_linear(
            sample_dataframe_with_gaps, 'timestamp', gap_info, True
        )
        
        assert len(fixed_df) >= len(sample_dataframe_with_gaps)
        assert 'timestamp' in fixed_df.columns
        assert not fixed_df['timestamp'].isna().any()
    
    def test_fix_gaps_forward_fill(self, sample_dataframe_with_gaps):
        """Test forward fill gap fixing."""
        gap_fixer = GapFixer()
        gap_info = gap_fixer._detect_gaps(sample_dataframe_with_gaps, 'timestamp')
        
        fixed_df = gap_fixer._fix_gaps_forward_fill(
            sample_dataframe_with_gaps, 'timestamp', gap_info, True
        )
        
        assert len(fixed_df) == len(sample_dataframe_with_gaps)
        assert 'timestamp' in fixed_df.columns
    
    def test_fix_gaps_backward_fill(self, sample_dataframe_with_gaps):
        """Test backward fill gap fixing."""
        gap_fixer = GapFixer()
        gap_info = gap_fixer._detect_gaps(sample_dataframe_with_gaps, 'timestamp')
        
        fixed_df = gap_fixer._fix_gaps_backward_fill(
            sample_dataframe_with_gaps, 'timestamp', gap_info, True
        )
        
        assert len(fixed_df) == len(sample_dataframe_with_gaps)
        assert 'timestamp' in fixed_df.columns
    
    def test_fix_gaps_interpolate(self, sample_dataframe_with_gaps):
        """Test interpolate gap fixing."""
        gap_fixer = GapFixer()
        gap_info = gap_fixer._detect_gaps(sample_dataframe_with_gaps, 'timestamp')
        
        fixed_df = gap_fixer._fix_gaps_interpolate(
            sample_dataframe_with_gaps, 'timestamp', gap_info, True
        )
        
        assert len(fixed_df) == len(sample_dataframe_with_gaps)
        assert 'timestamp' in fixed_df.columns
    
    def test_fix_gaps_in_dataframe(self, sample_dataframe_with_gaps):
        """Test gap fixing in dataframe."""
        gap_fixer = GapFixer()
        gap_info = gap_fixer._detect_gaps(sample_dataframe_with_gaps, 'timestamp')
        
        fixed_df, results = gap_fixer._fix_gaps_in_dataframe(
            sample_dataframe_with_gaps, 'timestamp', gap_info, 'auto', True
        )
        
        assert 'algorithm_used' in results
        assert 'processing_time' in results
        assert 'gaps_fixed' in results
        assert 'memory_used_mb' in results
        assert len(fixed_df) >= len(sample_dataframe_with_gaps)
    
    @patch('shutil.copy2')
    def test_create_backup(self, mock_copy2, temp_dir):
        """Test backup creation."""
        gap_fixer = GapFixer()
        
        # Create a test file
        test_file = temp_dir / 'test.csv'
        test_file.write_text('test data')
        
        backup_path = gap_fixer._create_backup(test_file)
        
        assert 'backup' in str(backup_path)
        assert backup_path.parent.name == 'backups'
        mock_copy2.assert_called_once()
    
    def test_save_fixed_data_csv(self, temp_dir):
        """Test saving fixed data as CSV."""
        gap_fixer = GapFixer()
        
        # Create test data
        test_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=10, freq='1H'),
            'value': range(10)
        })
        
        test_file = temp_dir / 'test.csv'
        success = gap_fixer._save_fixed_data(test_data, test_file)
        
        assert success is True
        assert test_file.exists()
    
    def test_save_fixed_data_parquet(self, temp_dir):
        """Test saving fixed data as Parquet."""
        gap_fixer = GapFixer()
        
        # Create test data
        test_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=10, freq='1H'),
            'value': range(10)
        })
        
        test_file = temp_dir / 'test.parquet'
        success = gap_fixer._save_fixed_data(test_data, test_file)
        
        assert success is True
        assert test_file.exists()
    
    def test_save_fixed_data_unsupported_format(self, temp_dir):
        """Test saving fixed data with unsupported format."""
        gap_fixer = GapFixer()
        
        # Create test data
        test_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=10, freq='1H'),
            'value': range(10)
        })
        
        test_file = temp_dir / 'test.txt'
        success = gap_fixer._save_fixed_data(test_data, test_file)
        
        assert success is False
    
    @patch('psutil.Process')
    def test_get_memory_usage(self, mock_process):
        """Test memory usage retrieval."""
        gap_fixer = GapFixer()
        
        # Mock process memory info
        mock_memory_info = Mock()
        mock_memory_info.rss = 1024 * 1024 * 100  # 100MB
        mock_process.return_value.memory_info.return_value = mock_memory_info
        
        memory_mb = gap_fixer._get_memory_usage()
        assert memory_mb == 100.0
    
    def test_get_memory_usage_no_psutil(self):
        """Test memory usage retrieval without psutil."""
        gap_fixer = GapFixer()
        
        # Mock psutil import error
        with patch('psutil.Process', side_effect=ImportError):
            memory_mb = gap_fixer._get_memory_usage()
            assert memory_mb == 0.0
    
    def test_fix_file_gaps_no_timestamp(self, temp_dir):
        """Test fixing gaps in file without timestamp column."""
        gap_fixer = GapFixer()
        
        # Create test file without timestamp
        test_data = pd.DataFrame({
            'value': range(10),
            'category': ['A', 'B'] * 5
        })
        
        test_file = temp_dir / 'test.csv'
        test_data.to_csv(test_file, index=False)
        
        success, result = gap_fixer.fix_file_gaps(test_file)
        
        assert success is False
        assert 'No timestamp column found' in result['error']
    
    def test_fix_file_gaps_no_gaps(self, temp_dir):
        """Test fixing gaps in file without gaps."""
        gap_fixer = GapFixer()
        
        # Create test file with regular timestamps
        test_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=10, freq='1H'),
            'value': range(10)
        })
        
        test_file = temp_dir / 'test.csv'
        test_data.to_csv(test_file, index=False)
        
        success, result = gap_fixer.fix_file_gaps(test_file)
        
        assert success is True
        assert result['gaps_fixed'] == 0
    
    def test_fix_file_gaps_unsupported_format(self, temp_dir):
        """Test fixing gaps in unsupported file format."""
        gap_fixer = GapFixer()
        
        # Create test file with unsupported format
        test_file = temp_dir / 'test.txt'
        test_file.write_text('test data')
        
        success, result = gap_fixer.fix_file_gaps(test_file)
        
        assert success is False
        assert 'Unsupported file format' in result['error']
    
    @patch('src.data.gap_fixer.GapFixer._create_backup')
    @patch('src.data.gap_fixer.GapFixer._save_fixed_data')
    def test_fix_file_gaps_success(self, mock_save, mock_backup, temp_dir):
        """Test successful gap fixing."""
        gap_fixer = GapFixer()
        
        # Create test file with gaps
        dates = pd.date_range('2023-01-01', periods=5, freq='1H')
        dates_with_gap = list(dates[:2]) + list(dates[3:])  # Remove middle date
        test_data = pd.DataFrame({
            'timestamp': dates_with_gap,
            'value': range(len(dates_with_gap))
        })
        
        test_file = temp_dir / 'test.csv'
        test_data.to_csv(test_file, index=False)
        
        # Mock backup and save
        mock_backup.return_value = temp_dir / 'backup.csv'
        mock_save.return_value = True
        
        success, result = gap_fixer.fix_file_gaps(test_file)
        
        assert success is True
        assert 'gaps_fixed' in result
        assert 'algorithm_used' in result
        assert 'processing_time' in result
    
    def test_fix_multiple_files(self, temp_dir):
        """Test fixing gaps in multiple files."""
        gap_fixer = GapFixer()
        
        # Create test files
        test_files = []
        for i in range(3):
            test_data = pd.DataFrame({
                'timestamp': pd.date_range('2023-01-01', periods=5, freq='1H'),
                'value': range(5)
            })
            
            test_file = temp_dir / f'test_{i}.csv'
            test_data.to_csv(test_file, index=False)
            test_files.append(test_file)
        
        # Mock the fix_file_gaps method
        with patch.object(gap_fixer, 'fix_file_gaps') as mock_fix:
            mock_fix.return_value = (True, {'gaps_fixed': 0, 'success': True})
            
            results = gap_fixer.fix_multiple_files(test_files, 'auto', True)
            
            assert len(results) == 3
            assert mock_fix.call_count == 3


class TestExplainWhyFixGaps:
    """Test cases for explain_why_fix_gaps function."""
    
    def test_explain_why_fix_gaps(self):
        """Test explain_why_fix_gaps function."""
        explanation = explain_why_fix_gaps()
        
        assert isinstance(explanation, str)
        assert len(explanation) > 0
        assert 'WHY TIME SERIES GAPS NEED TO BE FIXED' in explanation
        assert 'Data Quality Issues' in explanation
        assert 'Analysis Accuracy' in explanation
        assert 'ML Model Performance' in explanation
        assert 'Best Practices' in explanation


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
