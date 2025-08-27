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
        system.current_data = None
        system.current_results = {}
        system.menu_manager = Mock()
        system.safe_input = Mock(return_value=None)
        return system
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data for testing."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        data = {
            'Open': np.random.uniform(100, 200, 100),
            'High': np.random.uniform(150, 250, 100),
            'Low': np.random.uniform(50, 150, 100),
            'Close': np.random.uniform(100, 200, 100),
            'Volume': np.random.uniform(1000, 10000, 100)
        }
        return pd.DataFrame(data, index=dates)
    
    def test_init(self, analysis_runner):
        """Test AnalysisRunner initialization."""
        assert analysis_runner is not None
    
    @patch('builtins.input', side_effect=['0'])
    def test_run_eda_analysis_exit(self, mock_input, analysis_runner, mock_system, capsys):
        """Test run_eda_analysis with exit option."""
        analysis_runner.run_eda_analysis(mock_system)
        captured = capsys.readouterr()
        # Should not print any error messages
        assert "Invalid choice" not in captured.out
    
    @patch('builtins.input', side_effect=['1', '0'])
    @patch('src.interactive.analysis_runner.AnalysisRunner.run_basic_statistics')
    def test_run_eda_analysis_basic_statistics(self, mock_basic_stats, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with basic statistics option."""
        analysis_runner.run_eda_analysis(mock_system)
        mock_basic_stats.assert_called_once_with(mock_system)
    
    @patch('builtins.input', side_effect=['2', '0'])
    @patch('src.interactive.analysis_runner.AnalysisRunner.run_data_quality_check')
    def test_run_eda_analysis_data_quality(self, mock_data_quality, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with data quality check option."""
        analysis_runner.run_eda_analysis(mock_system)
        mock_data_quality.assert_called_once_with(mock_system)
    
    @patch('builtins.input', side_effect=['3', '0'])
    @patch('src.interactive.analysis_runner.AnalysisRunner.run_correlation_analysis')
    def test_run_eda_analysis_correlation(self, mock_correlation, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with correlation analysis option."""
        analysis_runner.run_eda_analysis(mock_system)
        mock_correlation.assert_called_once_with(mock_system)
    
    @patch('builtins.input', side_effect=['4', '0'])
    @patch('src.interactive.analysis_runner.AnalysisRunner.run_time_series_analysis')
    def test_run_eda_analysis_time_series(self, mock_time_series, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with time series analysis option."""
        analysis_runner.run_eda_analysis(mock_system)
        mock_time_series.assert_called_once_with(mock_system)
    
    @patch('builtins.input', side_effect=['5', '0'])
    def test_run_eda_analysis_feature_importance(self, mock_input, analysis_runner, mock_system, capsys):
        """Test run_eda_analysis with feature importance option."""
        analysis_runner.run_eda_analysis(mock_system)
        captured = capsys.readouterr()
        assert "Coming soon!" in captured.out
    
    @patch('builtins.input', side_effect=['6', '0'])
    @patch('src.interactive.analysis_runner.AnalysisRunner.fix_data_issues')
    def test_run_eda_analysis_fix_data(self, mock_fix_data, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with fix data issues option."""
        analysis_runner.run_eda_analysis(mock_system)
        mock_fix_data.assert_called_once_with(mock_system)
    
    @patch('builtins.input', side_effect=['7', '0'])
    @patch('src.interactive.analysis_runner.AnalysisRunner.generate_html_report')
    def test_run_eda_analysis_html_report(self, mock_html_report, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with generate HTML report option."""
        analysis_runner.run_eda_analysis(mock_system)
        mock_html_report.assert_called_once_with(mock_system)
    
    @patch('builtins.input', side_effect=['8', '0'])
    def test_run_eda_analysis_restore_backup(self, mock_input, analysis_runner, mock_system):
        """Test run_eda_analysis with restore from backup option."""
        analysis_runner.run_eda_analysis(mock_system)
        mock_system.data_manager.restore_from_backup.assert_called_once_with(mock_system)
    
    @patch('builtins.input', side_effect=['9', '0'])
    def test_run_eda_analysis_invalid_choice(self, mock_input, analysis_runner, mock_system, capsys):
        """Test run_eda_analysis with invalid choice."""
        analysis_runner.run_eda_analysis(mock_system)
        captured = capsys.readouterr()
        assert "Invalid choice" in captured.out
    
    @patch('builtins.input', side_effect=EOFError)
    def test_run_eda_analysis_eof_error(self, mock_input, analysis_runner, mock_system, capsys):
        """Test run_eda_analysis with EOFError."""
        analysis_runner.run_eda_analysis(mock_system)
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out
    
    def test_run_basic_statistics_no_data(self, analysis_runner, mock_system, capsys):
        """Test run_basic_statistics with no data."""
        analysis_runner.run_basic_statistics(mock_system)
        captured = capsys.readouterr()
        assert "No data loaded" in captured.out
    
    @patch('src.eda.basic_stats.outlier_analysis')
    def test_run_basic_statistics_with_data(self, mock_outlier_analysis, analysis_runner, mock_system, sample_data, capsys):
        """Test run_basic_statistics with data."""
        mock_system.current_data = sample_data
        mock_outlier_analysis.return_value = {'outliers': []}
        
        analysis_runner.run_basic_statistics(mock_system)
        
        captured = capsys.readouterr()
        assert "COMPREHENSIVE BASIC STATISTICS" in captured.out
        assert "DESCRIPTIVE STATISTICS" in captured.out
        assert "STATISTICAL INTERPRETATIONS" in captured.out
        
        # Check that results were saved
        assert 'comprehensive_basic_statistics' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_once_with('eda', 'basic_statistics')
    
    def test_run_data_quality_check_no_data(self, analysis_runner, mock_system, capsys):
        """Test run_data_quality_check with no data."""
        analysis_runner.run_data_quality_check(mock_system)
        captured = capsys.readouterr()
        assert "No data loaded" in captured.out
    
    def test_run_data_quality_check_with_data(self, analysis_runner, mock_system, sample_data, capsys):
        """Test run_data_quality_check with data."""
        mock_system.current_data = sample_data
        
        analysis_runner.run_data_quality_check(mock_system)
        
        captured = capsys.readouterr()
        assert "COMPREHENSIVE DATA QUALITY CHECK" in captured.out
        assert "QUALITY METRICS" in captured.out
        assert "COLUMN ANALYSIS" in captured.out
        
        # Check that results were saved
        assert 'comprehensive_data_quality' in mock_system.current_results
        assert 'data_quality' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_once_with('eda', 'data_quality_check')
    
    def test_run_correlation_analysis_no_data(self, analysis_runner, mock_system, capsys):
        """Test run_correlation_analysis with no data."""
        analysis_runner.run_correlation_analysis(mock_system)
        captured = capsys.readouterr()
        assert "No data loaded" in captured.out
    
    def test_run_correlation_analysis_with_data(self, analysis_runner, mock_system, sample_data, capsys):
        """Test run_correlation_analysis with data."""
        mock_system.current_data = sample_data
        
        analysis_runner.run_correlation_analysis(mock_system)
        
        captured = capsys.readouterr()
        assert "CORRELATION ANALYSIS" in captured.out
        
        # Check that results were saved
        assert 'correlation_analysis' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_once_with('eda', 'correlation_analysis')
    
    def test_run_correlation_analysis_insufficient_columns(self, analysis_runner, mock_system, capsys):
        """Test run_correlation_analysis with insufficient numeric columns."""
        # Create data with only one numeric column
        data = pd.DataFrame({'Close': [1, 2, 3, 4, 5]})
        mock_system.current_data = data
        
        analysis_runner.run_correlation_analysis(mock_system)
        
        captured = capsys.readouterr()
        assert "Insufficient numeric columns" in captured.out
    
    def test_run_time_series_analysis_no_data(self, analysis_runner, mock_system, capsys):
        """Test run_time_series_analysis with no data."""
        analysis_runner.run_time_series_analysis(mock_system)
        captured = capsys.readouterr()
        assert "No data loaded" in captured.out
    
    @patch('builtins.input', return_value='Close')
    def test_run_time_series_analysis_with_data(self, mock_input, analysis_runner, mock_system, sample_data, capsys):
        """Test run_time_series_analysis with data."""
        mock_system.current_data = sample_data
        
        analysis_runner.run_time_series_analysis(mock_system)
        
        captured = capsys.readouterr()
        assert "TIME SERIES ANALYSIS" in captured.out
        assert "ANALYSIS SUMMARY" in captured.out
        
        # Check that results were saved
        assert 'time_series_analysis' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_once_with('eda', 'time_series_analysis')
    
    def test_run_time_series_analysis_no_numeric_columns(self, analysis_runner, mock_system, capsys):
        """Test run_time_series_analysis with no numeric columns."""
        # Create data with no numeric columns
        data = pd.DataFrame({'Date': ['2023-01-01', '2023-01-02'], 'Text': ['A', 'B']})
        mock_system.current_data = data
        
        analysis_runner.run_time_series_analysis(mock_system)
        
        captured = capsys.readouterr()
        assert "No numeric columns found" in captured.out
    
    def test_fix_data_issues_no_data(self, analysis_runner, mock_system, capsys):
        """Test fix_data_issues with no data."""
        analysis_runner.fix_data_issues(mock_system)
        captured = capsys.readouterr()
        assert "No data loaded" in captured.out
    
    @patch('builtins.input', return_value='y')
    def test_fix_data_issues_with_data(self, mock_input, analysis_runner, mock_system, sample_data, capsys):
        """Test fix_data_issues with data."""
        mock_system.current_data = sample_data
        
        analysis_runner.fix_data_issues(mock_system)
        
        captured = capsys.readouterr()
        assert "FIX DATA ISSUES" in captured.out
        assert "Backup created" in captured.out
        assert "Data issues check completed" in captured.out
        
        # Check that results were saved
        assert 'data_fixes' in mock_system.current_results
        mock_system.menu_manager.mark_menu_as_used.assert_called_once_with('eda', 'fix_data_issues')
    
    @patch('builtins.input', return_value='n')
    def test_fix_data_issues_revert_changes(self, mock_input, analysis_runner, mock_system, sample_data, capsys):
        """Test fix_data_issues with revert changes."""
        original_data = sample_data.copy()
        mock_system.current_data = sample_data
        
        analysis_runner.fix_data_issues(mock_system)
        
        captured = capsys.readouterr()
        assert "Changes reverted" in captured.out
    
    def test_generate_html_report_no_data(self, analysis_runner, mock_system, capsys):
        """Test generate_html_report with no data."""
        analysis_runner.generate_html_report(mock_system)
        captured = capsys.readouterr()
        assert "No data loaded" in captured.out
    
    def test_generate_html_report_with_data(self, analysis_runner, mock_system, sample_data, capsys):
        """Test generate_html_report with data."""
        mock_system.current_data = sample_data
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('src.interactive.analysis_runner.Path') as mock_path:
                # Create a proper mock that behaves like Path
                mock_path_instance = Mock()
                mock_path_instance.__truediv__ = Mock(return_value=mock_path_instance)
                mock_path_instance.exists = Mock(return_value=True)
                mock_path_instance.mkdir = Mock()
                mock_path_instance.parent = mock_path_instance
                mock_path_instance.name = "test_report.html"
                mock_path_instance.__str__ = Mock(return_value=f"{temp_dir}/test_report.html")
                mock_path_instance.__fspath__ = Mock(return_value=f"{temp_dir}/test_report.html")
                mock_path.return_value = mock_path_instance
                
                analysis_runner.generate_html_report(mock_system)
                
                captured = capsys.readouterr()
                assert "GENERATE HTML REPORT" in captured.out
                assert "HTML report generated" in captured.out
                
                mock_system.menu_manager.mark_menu_as_used.assert_called_once_with('eda', 'generate_html_report')
    
    def test_run_model_development(self, analysis_runner, mock_system, capsys):
        """Test run_model_development."""
        analysis_runner.run_model_development(mock_system)
        captured = capsys.readouterr()
        assert "MODEL DEVELOPMENT" in captured.out
        assert "coming soon" in captured.out.lower()
        mock_system.safe_input.assert_called_once()
