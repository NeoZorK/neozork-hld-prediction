# -*- coding: utf-8 -*-
"""
Tests for analysis runner module.

This module tests the AnalysisRunner class from src/interactive/analysis_runner.py.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os

# Import the module to test
from src.interactive.analysis_runner import AnalysisRunner


class TestAnalysisRunner:
    """Test AnalysisRunner class."""
    
    @pytest.fixture
    def analysis_runner(self):
        """Create AnalysisRunner instance for testing."""
        return AnalysisRunner()
    
    @pytest.fixture
    def mock_system(self):
        """Create mock system for testing."""
        system = Mock()
        system.current_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [95, 96, 97, 98, 99],
            'Close': [102, 103, 104, 105, 106],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
        system.current_results = {}
        system.menu_manager = Mock()
        system.safe_input = Mock(return_value=None)
        return system
    
    @pytest.fixture
    def mock_system_no_data(self):
        """Create mock system without data for testing."""
        system = Mock()
        system.current_data = None
        system.current_results = {}
        system.menu_manager = Mock()
        system.safe_input = Mock(return_value=None)
        return system
    
    def test_init(self, analysis_runner):
        """Test AnalysisRunner initialization."""
        assert analysis_runner is not None
    
    @patch('builtins.input', side_effect=['0'])
    def test_run_eda_analysis_exit(self, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with exit option."""
        analysis_runner.run_eda_analysis(mock_system)
        mock_system.menu_manager.print_eda_menu.assert_called_once()
    
    @patch('builtins.input', side_effect=['1', '0'])
    def test_run_eda_analysis_basic_statistics(self, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with basic statistics option."""
        analysis_runner.run_eda_analysis(mock_system)
        assert mock_system.menu_manager.print_eda_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['2', '0'])
    def test_run_eda_analysis_data_quality(self, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with data quality check option."""
        analysis_runner.run_eda_analysis(mock_system)
        assert mock_system.menu_manager.print_eda_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['3', '0'])
    def test_run_eda_analysis_correlation(self, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with correlation analysis option."""
        analysis_runner.run_eda_analysis(mock_system)
        assert mock_system.menu_manager.print_eda_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['4', '0'])
    def test_run_eda_analysis_time_series(self, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with time series analysis option."""
        analysis_runner.run_eda_analysis(mock_system)
        assert mock_system.menu_manager.print_eda_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['5', '0'])
    def test_run_eda_analysis_feature_importance(self, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with feature importance option."""
        analysis_runner.run_eda_analysis(mock_system)
        assert mock_system.menu_manager.print_eda_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['6', '0'])
    def test_run_eda_analysis_fix_data(self, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with fix data issues option."""
        analysis_runner.run_eda_analysis(mock_system)
        assert mock_system.menu_manager.print_eda_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['7', '0'])
    def test_run_eda_analysis_html_report(self, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with generate HTML report option."""
        analysis_runner.run_eda_analysis(mock_system)
        assert mock_system.menu_manager.print_eda_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['8', '0'])
    def test_run_eda_analysis_restore_backup(self, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with restore from backup option."""
        analysis_runner.run_eda_analysis(mock_system)
        assert mock_system.menu_manager.print_eda_menu.call_count == 2
    
    @patch('builtins.input', side_effect=['9', '0'])
    def test_run_eda_analysis_invalid_choice(self, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with invalid choice."""
        analysis_runner.run_eda_analysis(mock_system)
        assert mock_system.menu_manager.print_eda_menu.call_count == 2
    
    @patch('builtins.input', side_effect=EOFError)
    def test_run_eda_analysis_eof(self, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with EOFError."""
        analysis_runner.run_eda_analysis(mock_system)
        mock_system.menu_manager.print_eda_menu.assert_called_once()
    
    def test_run_basic_statistics_no_data(self, analysis_runner, mock_system_no_data):
        """Test run_basic_statistics with no data."""
        analysis_runner.run_basic_statistics(mock_system_no_data)
    
    @patch('src.interactive.analysis_runner.outlier_analysis')
    def test_run_basic_statistics_with_data(self, mock_outlier_analysis, analysis_runner, mock_system):
        """Test run_basic_statistics with data."""
        mock_outlier_analysis.return_value = {'outliers': []}
        analysis_runner.run_basic_statistics(mock_system)
        assert 'comprehensive_basic_statistics' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_with('eda', 'basic_statistics')
    
    @patch('src.interactive.analysis_runner.outlier_analysis')
    def test_run_basic_statistics_exception(self, mock_outlier_analysis, analysis_runner, mock_system):
        """Test run_basic_statistics with exception."""
        mock_outlier_analysis.side_effect = Exception("Test error")
        analysis_runner.run_basic_statistics(mock_system)
    
    def test_run_data_quality_check_no_data(self, analysis_runner, mock_system_no_data):
        """Test run_data_quality_check with no data."""
        analysis_runner.run_data_quality_check(mock_system_no_data)
    
    def test_run_data_quality_check_with_data(self, analysis_runner, mock_system):
        """Test run_data_quality_check with data."""
        analysis_runner.run_data_quality_check(mock_system)
        assert 'comprehensive_data_quality' in mock_system.current_results
        assert 'data_quality' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_with('eda', 'data_quality_check')
    
    def test_run_data_quality_check_exception(self, analysis_runner, mock_system):
        """Test run_data_quality_check with exception."""
        mock_system.current_data.isnull.side_effect = Exception("Test error")
        analysis_runner.run_data_quality_check(mock_system)
    
    def test_run_correlation_analysis_no_data(self, analysis_runner, mock_system_no_data):
        """Test run_correlation_analysis with no data."""
        analysis_runner.run_correlation_analysis(mock_system_no_data)
    
    def test_run_correlation_analysis_with_data(self, analysis_runner, mock_system):
        """Test run_correlation_analysis with data."""
        analysis_runner.run_correlation_analysis(mock_system)
        assert 'correlation_analysis' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_with('eda', 'correlation_analysis')
    
    def test_run_correlation_analysis_insufficient_columns(self, analysis_runner, mock_system):
        """Test run_correlation_analysis with insufficient numeric columns."""
        mock_system.current_data = pd.DataFrame({'col1': [1, 2, 3]})
        analysis_runner.run_correlation_analysis(mock_system)
    
    def test_run_correlation_analysis_exception(self, analysis_runner, mock_system):
        """Test run_correlation_analysis with exception."""
        mock_system.current_data.select_dtypes.side_effect = Exception("Test error")
        analysis_runner.run_correlation_analysis(mock_system)
    
    def test_run_time_series_analysis_no_data(self, analysis_runner, mock_system_no_data):
        """Test run_time_series_analysis with no data."""
        analysis_runner.run_time_series_analysis(mock_system_no_data)
    
    @patch('builtins.input', return_value='Close')
    def test_run_time_series_analysis_with_data(self, mock_input, analysis_runner, mock_system):
        """Test run_time_series_analysis with data."""
        analysis_runner.run_time_series_analysis(mock_system)
        assert 'time_series_analysis' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_with('eda', 'time_series_analysis')
    
    @patch('builtins.input', return_value='InvalidColumn')
    def test_run_time_series_analysis_invalid_column(self, mock_input, analysis_runner, mock_system):
        """Test run_time_series_analysis with invalid column."""
        analysis_runner.run_time_series_analysis(mock_system)
        assert 'time_series_analysis' in mock_system.current_results
    
    def test_run_time_series_analysis_no_numeric_columns(self, analysis_runner, mock_system):
        """Test run_time_series_analysis with no numeric columns."""
        mock_system.current_data = pd.DataFrame({'text_col': ['a', 'b', 'c']})
        analysis_runner.run_time_series_analysis(mock_system)
    
    def test_run_time_series_analysis_exception(self, analysis_runner, mock_system):
        """Test run_time_series_analysis with exception."""
        mock_system.current_data.select_dtypes.side_effect = Exception("Test error")
        analysis_runner.run_time_series_analysis(mock_system)
    
    def test_fix_data_issues_no_data(self, analysis_runner, mock_system_no_data):
        """Test fix_data_issues with no data."""
        analysis_runner.fix_data_issues(mock_system_no_data)
    
    @patch('builtins.input', return_value='y')
    def test_fix_data_issues_with_data(self, mock_input, analysis_runner, mock_system):
        """Test fix_data_issues with data."""
        analysis_runner.fix_data_issues(mock_system)
        assert 'data_fixes' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_with('eda', 'fix_data_issues')
    
    @patch('builtins.input', return_value='n')
    def test_fix_data_issues_revert_changes(self, mock_input, analysis_runner, mock_system):
        """Test fix_data_issues with revert changes."""
        original_data = mock_system.current_data.copy()
        analysis_runner.fix_data_issues(mock_system)
    
    @patch('builtins.input', side_effect=EOFError)
    def test_fix_data_issues_eof(self, mock_input, analysis_runner, mock_system):
        """Test fix_data_issues with EOFError."""
        analysis_runner.fix_data_issues(mock_system)
    
    def test_fix_data_issues_exception(self, analysis_runner, mock_system):
        """Test fix_data_issues with exception."""
        mock_system.current_data.copy.side_effect = Exception("Test error")
        analysis_runner.fix_data_issues(mock_system)
    
    def test_generate_html_report_no_data(self, analysis_runner, mock_system_no_data):
        """Test generate_html_report with no data."""
        analysis_runner.generate_html_report(mock_system_no_data)
    
    def test_generate_html_report_with_data(self, analysis_runner, mock_system):
        """Test generate_html_report with data."""
        analysis_runner.generate_html_report(mock_system)
        mock_system.menu_manager.mark_menu_as_used.assert_called_with('eda', 'generate_html_report')
    
    def test_generate_html_report_with_results(self, analysis_runner, mock_system):
        """Test generate_html_report with existing results."""
        mock_system.current_results = {
            'comprehensive_data_quality': {
                'total_rows': 100,
                'total_cols': 5,
                'missing_values': 0,
                'missing_percentage': 0.0,
                'duplicates': 0,
                'duplicate_percentage': 0.0
            }
        }
        analysis_runner.generate_html_report(mock_system)
    
    def test_generate_html_report_exception(self, analysis_runner, mock_system):
        """Test generate_html_report with exception."""
        mock_system.current_data.memory_usage.side_effect = Exception("Test error")
        analysis_runner.generate_html_report(mock_system)
    
    def test_run_model_development(self, analysis_runner, mock_system):
        """Test run_model_development."""
        analysis_runner.run_model_development(mock_system)
        mock_system.safe_input.assert_called_once()
