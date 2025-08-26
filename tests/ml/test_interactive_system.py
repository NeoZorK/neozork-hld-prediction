# -*- coding: utf-8 -*-
"""
Tests for interactive_system.py module.

This module provides comprehensive test coverage for the interactive system
script that provides an interactive interface for the entire system.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
from pathlib import Path
import sys

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.ml.interactive_system import InteractiveSystem


class TestInteractiveSystem:
    """Test cases for InteractiveSystem class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.system = InteractiveSystem()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [95, 96, 97, 98, 99],
            'close': [102, 103, 104, 105, 106],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
    
    def test_init(self):
        """Test InteractiveSystem initialization."""
        assert self.system.feature_generator is None
        assert self.system.current_data is None
        assert self.system.current_results == {}
        assert 'main' in self.system.used_menus
        assert 'eda' in self.system.used_menus
        assert 'feature_engineering' in self.system.used_menus
    
    def test_calculate_submenu_completion_percentage(self):
        """Test submenu completion percentage calculation."""
        # Test with empty menu
        percentage = self.system.calculate_submenu_completion_percentage('nonexistent')
        assert percentage == 0
        
        # Test with all False items
        percentage = self.system.calculate_submenu_completion_percentage('main')
        assert percentage == 0
        
        # Test with some True items
        self.system.used_menus['main']['load_data'] = True
        self.system.used_menus['main']['eda_analysis'] = True
        percentage = self.system.calculate_submenu_completion_percentage('main')
        assert percentage == 22  # 2 out of 9 items = 22%
    
    def test_mark_menu_as_used(self):
        """Test marking menu items as used."""
        # Test marking existing item
        self.system.mark_menu_as_used('main', 'load_data')
        assert self.system.used_menus['main']['load_data'] is True
        
        # Test marking non-existent item (should not raise error)
        self.system.mark_menu_as_used('main', 'nonexistent')
    
    def test_reset_menu_status(self):
        """Test resetting menu status."""
        # Set some items to True
        self.system.used_menus['main']['load_data'] = True
        self.system.used_menus['main']['eda_analysis'] = True
        
        # Reset specific category
        self.system.reset_menu_status('main')
        assert self.system.used_menus['main']['load_data'] is False
        assert self.system.used_menus['main']['eda_analysis'] is False
        
        # Reset all categories
        self.system.used_menus['eda']['basic_statistics'] = True
        self.system.reset_menu_status()
        assert self.system.used_menus['eda']['basic_statistics'] is False
    
    def test_safe_input(self):
        """Test safe input handling."""
        # Test normal input
        with patch('builtins.input', return_value='test'):
            result = self.system.safe_input("Enter something: ")
            assert result == 'test'
        
        # Test EOFError handling
        with patch('builtins.input', side_effect=EOFError):
            result = self.system.safe_input("Enter something: ")
            assert result is None
    
    def test_print_banner(self):
        """Test banner printing."""
        with patch('builtins.print') as mock_print:
            self.system.print_banner()
            mock_print.assert_called()
    
    def test_print_main_menu(self):
        """Test main menu printing."""
        with patch('builtins.print') as mock_print:
            self.system.print_main_menu()
            mock_print.assert_called()
    
    def test_print_eda_menu(self):
        """Test EDA menu printing."""
        with patch('builtins.print') as mock_print:
            self.system.print_eda_menu()
            mock_print.assert_called()
    
    def test_print_feature_engineering_menu(self):
        """Test feature engineering menu printing."""
        with patch('builtins.print') as mock_print:
            self.system.print_feature_engineering_menu()
            mock_print.assert_called()
    
    def test_print_visualization_menu(self):
        """Test visualization menu printing."""
        with patch('builtins.print') as mock_print:
            self.system.print_visualization_menu()
            mock_print.assert_called()
    
    def test_print_model_development_menu(self):
        """Test model development menu printing."""
        with patch('builtins.print') as mock_print:
            self.system.print_model_development_menu()
            mock_print.assert_called()
    
    def test_load_data_from_file_csv(self):
        """Test loading data from CSV file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write('open,high,low,close,volume\n100,105,95,102,1000\n101,106,96,103,1100')
            temp_file = f.name
        
        try:
            df = self.system.load_data_from_file(temp_file)
            assert isinstance(df, pd.DataFrame)
            assert df.shape == (2, 5)
            assert list(df.columns) == ['open', 'high', 'low', 'close', 'volume']
        finally:
            os.unlink(temp_file)
    
    def test_load_data_from_file_parquet(self):
        """Test loading data from parquet file."""
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as f:
            temp_file = f.name
        
        try:
            self.sample_data.to_parquet(temp_file)
            df = self.system.load_data_from_file(temp_file)
            assert isinstance(df, pd.DataFrame)
            assert df.shape == (5, 5)
        finally:
            os.unlink(temp_file)
    
    def test_load_data_from_file_unsupported(self):
        """Test loading data from unsupported file format."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_file = f.name
        
        try:
            with pytest.raises(ValueError, match="Unsupported file format"):
                self.system.load_data_from_file(temp_file)
        finally:
            os.unlink(temp_file)
    
    def test_load_data_from_file_not_found(self):
        """Test loading data from non-existent file."""
        with pytest.raises(FileNotFoundError):
            self.system.load_data_from_file("nonexistent_file.csv")
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_load_data_no_data_folder(self, mock_print, mock_input):
        """Test load_data when data folder doesn't exist."""
        with patch('pathlib.Path.exists', return_value=False):
            result = self.system.load_data()
            assert result is False
            mock_print.assert_called()
    
    @patch('builtins.input', return_value='0')
    @patch('builtins.print')
    def test_load_data_back_to_menu(self, mock_print, mock_input):
        """Test load_data when user chooses to go back."""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.iterdir', return_value=[]):
                result = self.system.load_data()
                assert result is False
    
    @patch('builtins.input', return_value='1')
    @patch('builtins.print')
    def test_load_data_invalid_folder_number(self, mock_print, mock_input):
        """Test load_data with invalid folder number."""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.iterdir', return_value=[Path('data')]):
                with patch('pathlib.Path.glob', return_value=[]):
                    result = self.system.load_data()
                    assert result is False
    
    def test_run_basic_statistics_no_data(self):
        """Test run_basic_statistics when no data is loaded."""
        with patch('builtins.print') as mock_print:
            self.system.run_basic_statistics()
            mock_print.assert_called_with("❌ No data loaded. Please load data first.")
    
    def test_run_basic_statistics_with_data(self):
        """Test run_basic_statistics with loaded data."""
        self.system.current_data = self.sample_data
        
        with patch('builtins.print') as mock_print:
            with patch.object(self.system, '_create_statistics_plots'):
                with patch.object(self.system, '_show_plots_in_browser'):
                    with patch('builtins.input', return_value='n'):
                        self.system.run_basic_statistics()
                        mock_print.assert_called()
    
    def test_run_data_quality_check_no_data(self):
        """Test run_data_quality_check when no data is loaded."""
        with patch('builtins.print') as mock_print:
            self.system.run_data_quality_check()
            mock_print.assert_called_with("❌ No data loaded. Please load data first.")
    
    def test_run_data_quality_check_with_data(self):
        """Test run_data_quality_check with loaded data."""
        self.system.current_data = self.sample_data
        
        with patch('builtins.print') as mock_print:
            with patch('src.eda.data_quality') as mock_data_quality:
                with patch('builtins.input', return_value='n'):
                    self.system.run_data_quality_check()
                    mock_print.assert_called()
    
    def test_run_correlation_analysis_no_data(self):
        """Test run_correlation_analysis when no data is loaded."""
        with patch('builtins.print') as mock_print:
            self.system.run_correlation_analysis()
            mock_print.assert_called_with("❌ No data loaded. Please load data first.")
    
    def test_run_correlation_analysis_with_data(self):
        """Test run_correlation_analysis with loaded data."""
        self.system.current_data = self.sample_data
        
        with patch('builtins.print') as mock_print:
            self.system.run_correlation_analysis()
            mock_print.assert_called()
    
    def test_run_time_series_analysis_no_data(self):
        """Test run_time_series_analysis when no data is loaded."""
        with patch('builtins.print') as mock_print:
            self.system.run_time_series_analysis()
            mock_print.assert_called_with("❌ No data loaded. Please load data first.")
    
    def test_run_time_series_analysis_with_data(self):
        """Test run_time_series_analysis with loaded data."""
        self.system.current_data = self.sample_data
        
        with patch('builtins.print') as mock_print:
            with patch('src.eda.time_series_analysis.TimeSeriesAnalyzer') as mock_analyzer:
                with patch('builtins.input', return_value='n'):
                    self.system.run_time_series_analysis()
                    mock_print.assert_called()
    
    def test_generate_all_features_no_data(self):
        """Test generate_all_features when no data is loaded."""
        with patch('builtins.print') as mock_print:
            self.system.generate_all_features()
            mock_print.assert_called_with("❌ No data loaded. Please load data first.")
    
    def test_generate_all_features_with_data(self):
        """Test generate_all_features with loaded data."""
        self.system.current_data = self.sample_data
        
        with patch('builtins.print') as mock_print:
            with patch('src.ml.feature_engineering.feature_generator.FeatureGenerator') as mock_generator:
                with patch('src.ml.feature_engineering.feature_generator.MasterFeatureConfig') as mock_config:
                    with patch('src.ml.feature_engineering.feature_generator.FeatureSelectionConfig') as mock_selection_config:
                        mock_generator_instance = Mock()
                        mock_generator_instance.generate_features.return_value = self.sample_data
                        mock_generator_instance.get_feature_summary.return_value = {}
                        mock_generator_instance.get_memory_usage.return_value = {'rss': 100}
                        mock_generator.return_value = mock_generator_instance
                        
                        self.system.generate_all_features()
                        mock_print.assert_called()
    
    def test_show_feature_summary_no_results(self):
        """Test show_feature_summary when no feature engineering results."""
        with patch('builtins.print') as mock_print:
            self.system.show_feature_summary()
            mock_print.assert_called_with("❌ No feature engineering results available. Please generate features first.")
    
    def test_show_feature_summary_with_results(self):
        """Test show_feature_summary with feature engineering results."""
        self.system.current_results['feature_engineering'] = {
            'feature_summary': {'feature1': 0.8, 'feature2': 0.6}
        }
        
        with patch('builtins.print') as mock_print:
            self.system.show_feature_summary()
            mock_print.assert_called()
    
    def test_export_results_no_results(self):
        """Test export_results when no results to export."""
        with patch('builtins.print') as mock_print:
            self.system.export_results()
            mock_print.assert_called_with("❌ No results to export. Please run some analysis first.")
    
    def test_export_results_with_results(self):
        """Test export_results with results to export."""
        self.system.current_results = {'test': 'data'}
        
        with patch('builtins.print') as mock_print:
            with patch('pathlib.Path.mkdir'):
                with patch('builtins.open', create=True):
                    with patch('json.dump'):
                        with patch('pandas.DataFrame.to_parquet'):
                            self.system.export_results()
                            mock_print.assert_called()
    
    def test_fix_data_issues_no_data(self):
        """Test fix_data_issues when no data is loaded."""
        with patch('builtins.print') as mock_print:
            self.system.fix_data_issues()
            mock_print.assert_called_with("❌ No data loaded. Please load data first.")
    
    def test_fix_data_issues_with_data(self):
        """Test fix_data_issues with loaded data."""
        self.system.current_data = self.sample_data
        
        with patch('builtins.print') as mock_print:
            with patch('src.eda.fix_files') as mock_fix_files:
                with patch('builtins.input', return_value='y'):
                    mock_fix_files.fix_nan.return_value = self.sample_data
                    mock_fix_files.fix_duplicates.return_value = self.sample_data
                    
                    self.system.fix_data_issues()
                    mock_print.assert_called()
    
    def test_show_menu_status(self):
        """Test show_menu_status method."""
        with patch('builtins.print') as mock_print:
            self.system.show_menu_status()
            mock_print.assert_called()
    
    def test_create_statistics_plots(self):
        """Test _create_statistics_plots method."""
        self.system.current_data = self.sample_data
        
        with patch('matplotlib.pyplot') as mock_plt:
            with patch('seaborn.histplot') as mock_histplot:
                with patch('seaborn.boxplot') as mock_boxplot:
                    with patch('seaborn.heatmap') as mock_heatmap:
                        with patch('pathlib.Path.mkdir'):
                            with patch('builtins.print') as mock_print:
                                self.system._create_statistics_plots(self.sample_data.select_dtypes(include=[np.number]))
                                mock_print.assert_called()
    
    def test_show_plots_in_browser(self):
        """Test _show_plots_in_browser method."""
        with patch('webbrowser.get') as mock_webbrowser:
            with patch('tempfile.NamedTemporaryFile') as mock_tempfile:
                with patch('builtins.print') as mock_print:
                    mock_tempfile.return_value.__enter__.return_value.name = '/tmp/test.html'
                    self.system._show_plots_in_browser()
                    mock_print.assert_called()
    
    def test_fix_all_data_issues(self):
        """Test fix_all_data_issues method."""
        self.system.current_data = self.sample_data
        
        with patch('builtins.print') as mock_print:
            with patch('src.eda.fix_files') as mock_fix_files:
                mock_fix_files.fix_nan.return_value = self.sample_data
                mock_fix_files.fix_duplicates.return_value = self.sample_data
                
                self.system.fix_all_data_issues()
                mock_print.assert_called()


class TestInteractiveSystemIntegration:
    """Integration tests for InteractiveSystem."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.system = InteractiveSystem()
    
    def test_full_workflow(self):
        """Test a complete workflow from data loading to feature generation."""
        # Create sample data
        sample_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [95, 96, 97, 98, 99],
            'close': [102, 103, 104, 105, 106],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        # Test data loading
        self.system.current_data = sample_data
        assert self.system.current_data is not None
        assert self.system.current_data.shape == (5, 5)
        
        # Test basic statistics
        with patch('builtins.print'):
            with patch.object(self.system, '_create_statistics_plots'):
                with patch.object(self.system, '_show_plots_in_browser'):
                    with patch('builtins.input', return_value='n'):
                        self.system.run_basic_statistics()
        
        # Test feature generation
        with patch('builtins.print'):
            with patch('src.ml.feature_engineering.feature_generator.FeatureGenerator') as mock_generator:
                with patch('src.ml.feature_engineering.feature_generator.MasterFeatureConfig'):
                    with patch('src.ml.feature_engineering.feature_generator.FeatureSelectionConfig'):
                        mock_generator_instance = Mock()
                        mock_generator_instance.generate_features.return_value = sample_data
                        mock_generator_instance.get_feature_summary.return_value = {}
                        mock_generator_instance.get_memory_usage.return_value = {'rss': 100}
                        mock_generator.return_value = mock_generator_instance
                        
                        self.system.generate_all_features()
        
        # Verify results
        assert 'feature_engineering' in self.system.current_results
        assert 'comprehensive_basic_statistics' in self.system.current_results


if __name__ == '__main__':
    pytest.main([__file__])
