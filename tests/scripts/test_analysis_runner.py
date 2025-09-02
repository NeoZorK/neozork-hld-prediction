# -*- coding: utf-8 -*-
# tests/interactive/test_analysis_runner.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from src.interactive.analysis_runner import AnalysisRunner
from src.interactive.core import InteractiveSystem


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    data = pd.DataFrame({
        'predicted_high': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
        'predicted_low': [95, 96, 97, 98, 99, 100, 101, 102, 103, 104],
        'pressure': [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4],
        'pressure_vector': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
        'High': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
        'Close': [100.5, 101.5, 102.5, 103.5, 104.5, 105.5, 106.5, 107.5, 108.5, 109.5],
        'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
    })
    
    # Add some outliers for testing
    data.loc[5, 'predicted_high'] = 200  # Outlier
    data.loc[7, 'pressure'] = 5.0  # Outlier
    
    return {'dataframe': data}


@pytest.fixture
def mock_system():
    """Create a mock InteractiveSystem."""
    system = Mock(spec=InteractiveSystem)
    system.current_data = None
    system.current_results = {}
    system.menu_manager = Mock()
    system.visualization_manager = Mock()
    system.data_manager = Mock()
    system.safe_input = Mock(return_value="test")
    return system


@pytest.fixture
def analysis_runner(mock_system):
    """Create an AnalysisRunner instance."""
    return AnalysisRunner(mock_system)


class TestAnalysisRunner:
    
    def test_init(self, mock_system):
        """Test AnalysisRunner initialization."""
        runner = AnalysisRunner(mock_system)
        assert runner.system == mock_system
    
    def test_run_eda_analysis_exit(self, analysis_runner, mock_system):
        """Test EDA analysis menu exit."""
        with patch('builtins.input', return_value="0"):
            analysis_runner.run_eda_analysis(mock_system)
            mock_system.menu_manager.print_eda_menu.assert_called_once()
    
    def test_run_eda_analysis_data_quality(self, analysis_runner, mock_system):
        """Test EDA analysis menu data quality option."""
        with patch('builtins.input', side_effect=["1", "0"]):
            with patch.object(analysis_runner, 'run_comprehensive_data_quality_check') as mock_quality:
                analysis_runner.run_eda_analysis(mock_system)
                mock_quality.assert_called_once_with(mock_system)
    
    def test_run_eda_analysis_basic_statistics(self, analysis_runner, mock_system):
        """Test EDA analysis menu basic statistics option."""
        with patch('builtins.input', side_effect=["2", "0"]):
            with patch.object(analysis_runner, 'run_basic_statistics') as mock_basic:
                analysis_runner.run_eda_analysis(mock_system)
                mock_basic.assert_called_once_with(mock_system)
    
    def test_run_eda_analysis_correlation(self, analysis_runner, mock_system):
        """Test EDA analysis menu correlation option."""
        with patch('builtins.input', side_effect=["3", "0"]):
            with patch.object(analysis_runner, 'run_correlation_analysis') as mock_corr:
                analysis_runner.run_eda_analysis(mock_system)
                mock_corr.assert_called_once_with(mock_system)
    
    def test_run_eda_analysis_time_series(self, analysis_runner, mock_system):
        """Test EDA analysis menu time series option."""
        with patch('builtins.input', side_effect=["4", "0"]):
            with patch.object(analysis_runner, 'run_time_series_analysis') as mock_ts:
                analysis_runner.run_eda_analysis(mock_system)
                mock_ts.assert_called_once_with(mock_system)
    
    def test_run_eda_analysis_feature_importance(self, analysis_runner, mock_system):
        """Test EDA analysis menu feature importance option."""
        with patch('builtins.input', side_effect=["5", "0"]):
            analysis_runner.run_eda_analysis(mock_system)
            # Should print "Feature Importance - Coming soon!"
    
    def test_run_eda_analysis_html_report(self, analysis_runner, mock_system):
        """Test EDA analysis menu HTML report option."""
        with patch('builtins.input', side_effect=["6", "0"]):
            with patch.object(analysis_runner, 'generate_html_report') as mock_html:
                analysis_runner.run_eda_analysis(mock_system)
                mock_html.assert_called_once_with(mock_system)
    
    def test_run_eda_analysis_restore_backup(self, analysis_runner, mock_system):
        """Test EDA analysis menu restore backup option."""
        with patch('builtins.input', side_effect=["7", "0"]):
            analysis_runner.run_eda_analysis(mock_system)
            mock_system.data_manager.restore_from_backup.assert_called_once_with(mock_system)
    
    def test_run_eda_analysis_invalid_choice(self, analysis_runner, mock_system):
        """Test EDA analysis menu invalid choice."""
        with patch('builtins.input', side_effect=["99", "0"]):
            analysis_runner.run_eda_analysis(mock_system)
    
    def test_run_eda_analysis_eof(self, analysis_runner, mock_system):
        """Test EDA analysis menu EOF handling."""
        with patch('builtins.input', side_effect=EOFError):
            analysis_runner.run_eda_analysis(mock_system)
    
    def test_run_basic_statistics_no_data(self, analysis_runner, mock_system):
        """Test basic statistics with no data."""
        mock_system.current_data = None
        analysis_runner.run_basic_statistics(mock_system)
        # Should print "No data loaded" message
    
    def test_run_basic_statistics_with_data(self, analysis_runner, mock_system, sample_data):
        """Test basic statistics with data."""
        mock_system.current_data = sample_data['dataframe']
        mock_system.current_results = {}
        
        with patch('src.eda.basic_stats.outlier_analysis') as mock_outlier:
            with patch('builtins.input', return_value="n"):
                mock_outlier.return_value = {}
                
                analysis_runner.run_basic_statistics(mock_system)
                
                assert 'comprehensive_basic_statistics' in mock_system.current_results
                mock_system.menu_manager.mark_menu_as_used.assert_called_once_with('eda', 'basic_statistics')
    
    def test_run_basic_statistics_exception(self, analysis_runner, mock_system, sample_data):
        """Test basic statistics with exception."""
        mock_system.current_data = sample_data['dataframe']
        
        with patch('src.eda.basic_stats.outlier_analysis', side_effect=Exception("Test error")):
            analysis_runner.run_basic_statistics(mock_system)
    
    def test_run_data_quality_check_no_data(self, analysis_runner, mock_system):
        """Test data quality check with no data."""
        mock_system.current_data = None
        analysis_runner.run_comprehensive_data_quality_check(mock_system)
    
    def test_run_data_quality_check_with_data(self, analysis_runner, mock_system, sample_data):
        """Test data quality check with data."""
        mock_system.current_data = sample_data['dataframe']
        analysis_runner.run_comprehensive_data_quality_check(mock_system)
    
    def test_run_correlation_analysis_no_data(self, analysis_runner, mock_system):
        """Test correlation analysis with no data."""
        mock_system.current_data = None
        analysis_runner.run_correlation_analysis(mock_system)
    
    def test_run_correlation_analysis_with_data(self, analysis_runner, mock_system, sample_data):
        """Test correlation analysis with data."""
        mock_system.current_data = sample_data['dataframe']
        analysis_runner.run_correlation_analysis(mock_system)
    
    def test_run_time_series_analysis_no_data(self, analysis_runner, mock_system):
        """Test time series analysis with no data."""
        mock_system.current_data = None
        analysis_runner.run_time_series_analysis(mock_system)
    
    def test_run_time_series_analysis_with_data(self, analysis_runner, mock_system, sample_data):
        """Test time series analysis with data."""
        mock_system.current_data = sample_data['dataframe']
        analysis_runner.run_time_series_analysis(mock_system)
    
    def test_fix_data_issues_no_data(self, analysis_runner, mock_system):
        """Test fix data issues with no data."""
        mock_system.current_data = None
        analysis_runner.fix_data_issues(mock_system)
    
    def test_fix_data_issues_with_data(self, analysis_runner, mock_system, sample_data):
        """Test fix data issues with data."""
        mock_system.current_data = sample_data['dataframe']
        analysis_runner.fix_data_issues(mock_system)
    
    def test_generate_html_report_no_data(self, analysis_runner, mock_system):
        """Test generate HTML report with no data."""
        mock_system.current_data = None
        analysis_runner.generate_html_report(mock_system)
    
    def test_generate_html_report_with_data(self, analysis_runner, mock_system, sample_data):
        """Test generate HTML report with data."""
        mock_system.current_data = sample_data['dataframe']
        analysis_runner.generate_html_report(mock_system)
    
    # New tests for improved functionality
    def test_run_basic_statistics_with_data_detailed(self, analysis_runner, mock_system, sample_data):
        """Test basic statistics with detailed analysis."""
        mock_system.current_data = sample_data['dataframe']
        mock_system.current_results = {}
        
        with patch('src.eda.basic_stats.outlier_analysis') as mock_outlier:
            with patch('builtins.input', return_value="n"):
                mock_outlier.return_value = {}
                
                analysis_runner.run_basic_statistics(mock_system)
                
                assert 'comprehensive_basic_statistics' in mock_system.current_results
                mock_system.menu_manager.mark_menu_as_used.assert_called_once_with('eda', 'basic_statistics')
    
    def test_run_basic_statistics_with_plots_yes(self, analysis_runner, mock_system, sample_data):
        """Test basic statistics with plots enabled."""
        mock_system.current_data = sample_data['dataframe']
        mock_system.current_results = {}
        
        with patch('src.eda.basic_stats.outlier_analysis') as mock_outlier:
            with patch('builtins.input', side_effect=["y", "n"]):
                mock_outlier.return_value = {}
                mock_system.visualization_manager.create_statistics_plots.return_value = True
                mock_system.visualization_manager.show_plots_in_browser.return_value = True
                
                analysis_runner.run_basic_statistics(mock_system)
                
                mock_system.visualization_manager.create_statistics_plots.assert_called_once()
                mock_system.visualization_manager.show_plots_in_browser.assert_called_once()
    
    def test_run_basic_statistics_with_plots_no(self, analysis_runner, mock_system, sample_data):
        """Test basic statistics with plots disabled."""
        mock_system.current_data = sample_data['dataframe']
        mock_system.current_results = {}
        
        with patch('src.eda.basic_stats.outlier_analysis') as mock_outlier:
            with patch('builtins.input', side_effect=["n", "n"]):
                mock_outlier.return_value = {}
                
                analysis_runner.run_basic_statistics(mock_system)
                
                mock_system.visualization_manager.create_statistics_plots.assert_not_called()
    
    def test_run_basic_statistics_with_outlier_fix_yes(self, analysis_runner, mock_system, sample_data):
        """Test basic statistics with outlier fixing enabled."""
        mock_system.current_data = sample_data['dataframe']
        mock_system.current_results = {}
        
        # Create outlier results that will trigger the fix prompt
        outlier_results = {
            'predicted_high': {
                'iqr_method': {'outlier_percentage': 10.0},
                'z_score_method': {'outlier_percentage': 5.0}
            }
        }
        
        with patch('src.eda.basic_stats.outlier_analysis', return_value=outlier_results):
            with patch('builtins.input', side_effect=["n", "y", "y"]):
                with patch('src.eda.outlier_handler.OutlierHandler') as mock_handler:
                    mock_handler_instance = Mock()
                    mock_handler.return_value = mock_handler_instance
                    mock_handler_instance.treat_outliers_capping.return_value = {'values_capped': 5}
                    
                    analysis_runner.run_basic_statistics(mock_system)
                    
                    mock_handler.assert_called_once()
                    mock_handler_instance.treat_outliers_capping.assert_called_once()
    
    def test_run_basic_statistics_with_outlier_fix_no(self, analysis_runner, mock_system, sample_data):
        """Test basic statistics with outlier fixing disabled."""
        mock_system.current_data = sample_data['dataframe']
        mock_system.current_results = {}
        
        # Create outlier results that will trigger the fix prompt
        outlier_results = {
            'predicted_high': {
                'iqr_method': {'outlier_percentage': 10.0},
                'z_score_method': {'outlier_percentage': 5.0}
            }
        }
        
        with patch('src.eda.basic_stats.outlier_analysis', return_value=outlier_results):
            with patch('builtins.input', side_effect=["n", "n"]):
                analysis_runner.run_basic_statistics(mock_system)
                
                # Should not call outlier handler
                assert 'outlier_fixes' not in mock_system.current_results
    
    def test_run_basic_statistics_with_outlier_fix_revert(self, analysis_runner, mock_system, sample_data):
        """Test basic statistics with outlier fixing and revert."""
        mock_system.current_data = sample_data['dataframe']
        mock_system.current_results = {}
        original_data = sample_data['dataframe'].copy()
        
        # Create outlier results that will trigger the fix prompt
        outlier_results = {
            'predicted_high': {
                'iqr_method': {'outlier_percentage': 10.0},
                'z_score_method': {'outlier_percentage': 5.0}
            }
        }
        
        with patch('src.eda.basic_stats.outlier_analysis', return_value=outlier_results):
            with patch('builtins.input', side_effect=["n", "y", "n"]):
                with patch('src.eda.outlier_handler.OutlierHandler') as mock_handler:
                    mock_handler_instance = Mock()
                    mock_handler.return_value = mock_handler_instance
                    mock_handler_instance.treat_outliers_capping.return_value = {'values_capped': 5}
                    
                    analysis_runner.run_basic_statistics(mock_system)
                    
                    # Should revert changes
                    assert 'outlier_fixes' not in mock_system.current_results
    
    def test_run_basic_statistics_no_outliers(self, analysis_runner, mock_system, sample_data):
        """Test basic statistics with no significant outliers."""
        mock_system.current_data = sample_data['dataframe']
        mock_system.current_results = {}
        
        # Create outlier results with no significant outliers
        outlier_results = {
            'predicted_high': {
                'iqr_method': {'outlier_percentage': 0.5},
                'z_score_method': {'outlier_percentage': 0.3}
            }
        }
        
        with patch('src.eda.basic_stats.outlier_analysis', return_value=outlier_results):
            with patch('builtins.input', return_value="n"):
                analysis_runner.run_basic_statistics(mock_system)
                
                # Should not ask about outlier fixing
                assert 'outlier_fixes' not in mock_system.current_results
