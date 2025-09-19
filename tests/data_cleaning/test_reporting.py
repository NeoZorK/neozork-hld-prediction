"""
Tests for Reporting Module

This module contains comprehensive unit tests for the CleaningReporter class.
"""

import pytest
import pandas as pd
import numpy as np
import os
import tempfile
from datetime import datetime
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from data_cleaning.reporting import CleaningReporter


class TestCleaningReporter:
    """Test cases for CleaningReporter class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.reporter = CleaningReporter()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_show_gaps_details(self):
        """Test showing gaps details."""
        gaps = [
            {
                'column': 'timestamp',
                'gap_start': datetime(2023, 1, 1, 10, 0, 0),
                'gap_end': datetime(2023, 1, 1, 12, 0, 0),
                'gap_duration': pd.Timedelta(hours=2),
                'expected_duration': pd.Timedelta(hours=1),
                'gap_size': 2.0
            }
        ]
        
        with patch('builtins.print') as mock_print:
            self.reporter._show_gaps_details(gaps)
            
            # Should print gap information
            assert mock_print.call_count > 0
            
            # Check that gap details are printed
            printed_text = ' '.join([str(call) for call in mock_print.call_args_list])
            assert 'timestamp' in printed_text
            assert 'Gap 1:' in printed_text
    
    def test_show_duplicates_details(self):
        """Test showing duplicates details."""
        duplicates = [
            {
                'indices': [0, 3],
                'count': 2,
                'sample_data': {'value': 1, 'category': 'A'}
            }
        ]
        
        with patch('builtins.print') as mock_print:
            self.reporter._show_duplicates_details(duplicates)
            
            # Should print duplicate information
            assert mock_print.call_count > 0
            
            # Check that duplicate details are printed
            printed_text = ' '.join([str(call) for call in mock_print.call_args_list])
            assert 'duplicate groups' in printed_text
            assert 'Group 1:' in printed_text
    
    def test_show_nan_details(self):
        """Test showing NaN details."""
        nan_issues = [
            {
                'column': 'value',
                'count': 5,
                'percentage': 25.0,
                'indices': [1, 3, 5, 7, 9],
                'total_indices': 5
            }
        ]
        
        with patch('builtins.print') as mock_print:
            self.reporter._show_nan_details(nan_issues)
            
            # Should print NaN information
            assert mock_print.call_count > 0
            
            # Check that NaN details are printed
            printed_text = ' '.join([str(call) for call in mock_print.call_args_list])
            assert 'NaN values' in printed_text
            assert 'value' in printed_text
            assert '25.0%' in printed_text
    
    def test_show_zeros_details(self):
        """Test showing zero values details."""
        zero_issues = [
            {
                'column': 'value',
                'count': 3,
                'percentage': 15.0,
                'indices': [0, 5, 10],
                'total_indices': 3,
                'warning': 'Some financial data may legitimately contain zero values'
            }
        ]
        
        with patch('builtins.print') as mock_print:
            self.reporter._show_zeros_details(zero_issues)
            
            # Should print zero values information
            assert mock_print.call_count > 0
            
            # Check that zero details are printed
            printed_text = ' '.join([str(call) for call in mock_print.call_args_list])
            assert 'zero values' in printed_text
            assert 'value' in printed_text
            assert '15.0%' in printed_text
    
    def test_show_negative_details(self):
        """Test showing negative values details."""
        negative_issues = [
            {
                'column': 'value',
                'count': 2,
                'percentage': 10.0,
                'indices': [1, 3],
                'total_indices': 2,
                'warning': 'Some financial data may legitimately contain negative values'
            }
        ]
        
        with patch('builtins.print') as mock_print:
            self.reporter._show_negative_details(negative_issues)
            
            # Should print negative values information
            assert mock_print.call_count > 0
            
            # Check that negative details are printed
            printed_text = ' '.join([str(call) for call in mock_print.call_args_list])
            assert 'negative values' in printed_text
            assert 'value' in printed_text
            assert '10.0%' in printed_text
    
    def test_show_infinity_details(self):
        """Test showing infinity values details."""
        infinity_issues = [
            {
                'column': 'value',
                'count': 1,
                'percentage': 5.0,
                'indices': [2],
                'total_indices': 1
            }
        ]
        
        with patch('builtins.print') as mock_print:
            self.reporter._show_infinity_details(infinity_issues)
            
            # Should print infinity values information
            assert mock_print.call_count > 0
            
            # Check that infinity details are printed
            printed_text = ' '.join([str(call) for call in mock_print.call_args_list])
            assert 'infinity values' in printed_text
            assert 'value' in printed_text
            assert '5.0%' in printed_text
    
    def test_show_outliers_details(self):
        """Test showing outliers details."""
        outliers = [
            {
                'column': 'value',
                'methods': {
                    'IQR': {
                        'count': 3,
                        'indices': [0, 5, 10],
                        'total_indices': 3
                    },
                    'Z-Score': {
                        'count': 2,
                        'indices': [0, 10],
                        'total_indices': 2
                    }
                }
            }
        ]
        
        with patch('builtins.print') as mock_print:
            self.reporter._show_outliers_details(outliers)
            
            # Should print outliers information
            assert mock_print.call_count > 0
            
            # Check that outliers details are printed
            printed_text = ' '.join([str(call) for call in mock_print.call_args_list])
            assert 'outliers' in printed_text
            assert 'value' in printed_text
            assert 'IQR' in printed_text
            assert 'Z-Score' in printed_text
    
    def test_show_warnings(self):
        """Test showing warnings."""
        issues = [
            {
                'warning': 'Some financial data may legitimately contain zero values'
            },
            {
                'warning': 'Some financial data may legitimately contain negative values'
            }
        ]
        
        with patch('builtins.print') as mock_print:
            self.reporter._show_warnings(issues)
            
            # Should print warnings
            assert mock_print.call_count > 0
            
            # Check that warnings are printed
            printed_text = ' '.join([str(call) for call in mock_print.call_args_list])
            assert 'WARNING' in printed_text
            assert 'zero values' in printed_text
            assert 'negative values' in printed_text
    
    def test_show_detailed_results_no_issues(self):
        """Test showing detailed results with no issues."""
        with patch('builtins.print') as mock_print:
            self.reporter.show_detailed_results("Test Procedure", [], pd.DataFrame())
            
            # Should print no issues found
            assert mock_print.call_count > 0
            
            # Check that no issues message is printed
            printed_text = ' '.join([call[0][0] for call in mock_print.call_args_list])
            assert 'No issues found' in printed_text
    
    def test_show_final_report(self):
        """Test showing final report."""
        file_info = {
            'filename': 'test.parquet',
            'format': 'parquet',
            'source': 'binance',
            'symbol': 'BTCUSD',
            'timeframe': '1h',
            'indicator': 'rsi'
        }
        
        # Create test data
        original_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=100),
            'value': range(100)
        })
        
        cleaned_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=95),
            'value': range(95)
        })
        
        cleaning_results = {
            'original_data': original_data,
            'cleaned_data': cleaned_data,
            'total_issues_found': 10,
            'total_issues_fixed': 8,
            'procedures': {
                'gaps': {'issues_found': 2, 'issues_fixed': 2, 'status': 'fixed'},
                'duplicates': {'issues_found': 3, 'issues_fixed': 3, 'status': 'fixed'},
                'nan': {'issues_found': 5, 'issues_fixed': 3, 'status': 'fixed'},
                'zeros': {'issues_found': 0, 'issues_fixed': 0, 'status': 'clean'},
                'negative': {'issues_found': 0, 'issues_fixed': 0, 'status': 'clean'},
                'infinity': {'issues_found': 0, 'issues_fixed': 0, 'status': 'clean'},
                'outliers': {'issues_found': 0, 'issues_fixed': 0, 'status': 'clean'}
            }
        }
        
        with patch('builtins.print') as mock_print:
            self.reporter.show_final_report(file_info, cleaning_results)
            
            # Should print comprehensive report
            assert mock_print.call_count > 0
            
            # Check that report sections are printed
            printed_text = ' '.join([str(call) for call in mock_print.call_args_list])
            assert 'FINAL CLEANING REPORT' in printed_text
            assert 'test.parquet' in printed_text
            assert 'binance' in printed_text
            assert 'BTCUSD' in printed_text
            assert 'DATA STATISTICS' in printed_text
            assert 'CLEANING PROCEDURES SUMMARY' in printed_text
            assert 'OVERALL SUMMARY' in printed_text
    
    def test_save_report(self):
        """Test saving report to file."""
        file_info = {
            'filename': 'test.parquet',
            'format': 'parquet',
            'source': 'binance'
        }
        
        cleaning_results = {
            'original_data': pd.DataFrame({'value': [1, 2, 3]}),
            'cleaned_data': pd.DataFrame({'value': [1, 2, 3]}),
            'procedures': {}
        }
        
        output_path = os.path.join(self.temp_dir, 'test_report.txt')
        
        self.reporter.save_report(file_info, cleaning_results, output_path)
        
        # Check that file was created
        assert os.path.exists(output_path)
        
        # Check file content
        with open(output_path, 'r') as f:
            content = f.read()
            assert 'DATA CLEANING REPORT' in content
            assert 'test.parquet' in content
            assert 'binance' in content
    
    def test_generate_summary_stats(self):
        """Test generating summary statistics."""
        original_data = pd.DataFrame({
            'value': [1, 2, 3, 4, 5],
            'category': ['A', 'B', 'A', 'B', 'A']
        })
        
        cleaned_data = pd.DataFrame({
            'value': [1, 2, 3, 4],
            'category': ['A', 'B', 'A', 'B']
        })
        
        cleaning_results = {
            'original_data': original_data,
            'cleaned_data': cleaned_data,
            'total_issues_found': 10,
            'total_issues_fixed': 8,
            'procedures': {
                'gaps': {'issues_found': 2, 'issues_fixed': 2, 'status': 'fixed'},
                'duplicates': {'issues_found': 3, 'issues_fixed': 3, 'status': 'fixed'},
                'nan': {'issues_found': 5, 'issues_fixed': 3, 'status': 'fixed'},
                'zeros': {'issues_found': 0, 'issues_fixed': 0, 'status': 'clean'},
                'negative': {'issues_found': 0, 'issues_fixed': 0, 'status': 'clean'},
                'infinity': {'issues_found': 0, 'issues_fixed': 0, 'status': 'clean'},
                'outliers': {'issues_found': 0, 'issues_fixed': 0, 'status': 'clean'}
            }
        }
        
        stats = self.reporter.generate_summary_stats(cleaning_results)
        
        assert stats['original_rows'] == 5
        assert stats['cleaned_rows'] == 4
        assert stats['rows_removed'] == 1
        assert stats['original_columns'] == 2
        assert stats['cleaned_columns'] == 2
        assert stats['total_issues_found'] == 10
        assert stats['total_issues_fixed'] == 8
        assert stats['procedures_completed'] == 7
        assert stats['procedures_fixed'] == 3
        assert stats['procedures_clean'] == 4
        assert stats['row_reduction_pct'] == 20.0
        assert stats['fix_rate_pct'] == 80.0
    
    def test_show_detailed_results_unknown_procedure(self):
        """Test showing detailed results for unknown procedure."""
        issues = [{'test': 'data'}]
        data = pd.DataFrame({'value': [1, 2, 3]})
        
        with patch('builtins.print') as mock_print:
            self.reporter.show_detailed_results("Unknown Procedure", issues, data)
            
            # Should still print something
            assert mock_print.call_count > 0


# Mock patch for testing
def patch(target):
    """Simple mock patch for testing."""
    from unittest.mock import patch as _patch
    return _patch(target)
