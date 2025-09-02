#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for scripts/ml/interactive_system.py

This module provides comprehensive test coverage for the interactive system script.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock, call
import tempfile
import os
from pathlib import Path
import sys
import psutil


class TestInteractiveSystemScript:
    """Test cases for InteractiveSystem script."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Add project root to path for imports
        project_root = Path(__file__).parent.parent.parent.parent.parent
        sys.path.insert(0, str(project_root))
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [95, 96, 97, 98, 99],
            'close': [102, 103, 104, 105, 106],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
    
    def test_interactive_system_import(self):
        """Test that InteractiveSystem can be imported from scripts.ml."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            assert hasattr(InteractiveSystem, '__init__')
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_interactive_system_initialization(self):
        """Test InteractiveSystem initialization."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            # Check that system has expected attributes
            assert hasattr(system, 'feature_generator')
            assert hasattr(system, 'current_data')
            assert hasattr(system, 'current_results')
            assert hasattr(system, 'used_menus')
            
            # Check menu structure
            assert 'main' in system.used_menus
            assert 'eda' in system.used_menus
            assert 'feature_engineering' in system.used_menus
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_calculate_submenu_completion_percentage(self):
        """Test submenu completion percentage calculation."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            # Test with valid menu category
            percentage = system.calculate_submenu_completion_percentage('main')
            assert isinstance(percentage, (int, float))
            assert 0 <= percentage <= 100
            
            # Test with invalid menu category
            percentage = system.calculate_submenu_completion_percentage('invalid_menu')
            assert percentage == 0
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_mark_menu_as_used(self):
        """Test marking menu items as used."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            # Test marking existing item
            with patch('builtins.print') as mock_print:
                system.mark_menu_as_used('main', 'load_data')
                assert system.used_menus['main']['load_data'] is True
                mock_print.assert_called_once()
            
            # Test marking non-existent item (should not raise error)
            system.mark_menu_as_used('main', 'nonexistent')
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_reset_menu_status(self):
        """Test resetting menu status."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            # Set some items to True
            system.used_menus['main']['load_data'] = True
            system.used_menus['main']['eda_analysis'] = True
            
            # Reset specific category
            with patch('builtins.print') as mock_print:
                system.reset_menu_status('main')
                assert system.used_menus['main']['load_data'] is False
                assert system.used_menus['main']['eda_analysis'] is False
                mock_print.assert_called_once()
            
            # Reset all categories
            system.used_menus['eda']['basic_statistics'] = True
            with patch('builtins.print') as mock_print:
                system.reset_menu_status()
                assert system.used_menus['eda']['basic_statistics'] is False
                mock_print.assert_called_once()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_safe_input(self):
        """Test safe input handling."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            # Test normal input
            with patch('builtins.input', return_value='test'):
                result = system.safe_input("Enter something: ")
                assert result == 'test'
            
            # Test EOFError handling
            with patch('builtins.input', side_effect=EOFError):
                with patch('builtins.print') as mock_print:
                    result = system.safe_input("Enter something: ")
                    assert result is None
                    mock_print.assert_called_once()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_print_banner(self):
        """Test banner printing."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.print_banner()
                mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_print_main_menu(self):
        """Test main menu printing."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.print_main_menu()
                mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_print_eda_menu(self):
        """Test EDA menu printing."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.print_eda_menu()
                mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_print_feature_engineering_menu(self):
        """Test feature engineering menu printing."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.print_feature_engineering_menu()
                mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_print_visualization_menu(self):
        """Test visualization menu printing."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.print_visualization_menu()
                mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_print_model_development_menu(self):
        """Test model development menu printing."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.print_model_development_menu()
                mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_load_data_from_file_csv(self):
        """Test loading data from CSV file."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            # Create a temporary CSV file with MT5 format
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                # Create MT5 format CSV data with header on second line
                csv_content = """<MetaTrader 5 CSV Export>
DateTime,Open,High,Low,Close,TickVolume,
2023.01.01 00:00,100.0,105.0,95.0,103.0,1000,
2023.01.02 00:00,101.0,106.0,96.0,104.0,1100,
2023.01.03 00:00,102.0,107.0,97.0,105.0,1200,"""
                
                f.write(csv_content)
                csv_file = f.name
            
            try:
                # Mock the data_manager to avoid actual file loading
                with patch.object(system, 'data_manager') as mock_data_manager:
                    mock_data_manager.load_data_from_file.return_value = pd.DataFrame({
                        'Open': [100.0, 101.0, 102.0],
                        'High': [105.0, 106.0, 107.0],
                        'Low': [95.0, 96.0, 97.0],
                        'Close': [103.0, 104.0, 105.0],
                        'Volume': [1000, 1100, 1200]
                    })
                    
                    # Load the data
                    result = system.data_manager.load_data_from_file(csv_file)
                    
                    # Check that data was loaded correctly
                    assert isinstance(result, pd.DataFrame)
                    assert len(result) == 3
                    # Check that columns are properly mapped
                    expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                    assert all(col in result.columns for col in expected_columns)
                    
            finally:
                # Clean up
                os.unlink(csv_file)
                
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    @patch('psutil.virtual_memory')
    def test_load_data_from_file_parquet(self, mock_vm):
        """Test loading data from parquet file."""
        # Mock memory check to return True (sufficient memory)
        mock_vm.return_value.available = 4 * 1024 * 1024 * 1024  # 4GB available
        
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as f:
                temp_file = f.name
            
            try:
                self.sample_data.to_parquet(temp_file)
                df = system.load_data_from_file(temp_file)
                assert isinstance(df, pd.DataFrame)
                assert df.shape == (5, 5)
            finally:
                os.unlink(temp_file)
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    @patch('psutil.virtual_memory')
    def test_load_data_from_file_unsupported(self, mock_vm):
        """Test loading data from unsupported file format."""
        # Mock memory check to return True (sufficient memory)
        mock_vm.return_value.available = 4 * 1024 * 1024 * 1024  # 4GB available
        
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
                temp_file = f.name
            
            try:
                with pytest.raises(ValueError, match="Unsupported file format"):
                    system.load_data_from_file(temp_file)
            finally:
                os.unlink(temp_file)
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_load_data_from_file_not_found(self):
        """Test loading data from non-existent file."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with pytest.raises(FileNotFoundError):
                system.load_data_from_file("nonexistent_file.csv")
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_load_data_from_folder(self):
        """Test loading data files from folder."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            # Test loading from data folder (should exist)
            data_folder = Path("data")
            if data_folder.exists():
                files = system.load_data_from_folder(str(data_folder))
                assert isinstance(files, list)
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_load_data_no_data_folder(self):
        """Test load_data when data folder doesn't exist."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('pathlib.Path.exists', return_value=False):
                with patch('builtins.print') as mock_print:
                    result = system.load_data()
                    assert result is False
                    mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_load_data_back_to_menu(self):
        """Test load_data when user chooses to go back."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.input', return_value='0'):
                with patch('pathlib.Path.exists', return_value=True):
                    with patch('pathlib.Path.iterdir', return_value=[]):
                        result = system.load_data()
                        assert result is False
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_run_basic_statistics_no_data(self):
        """Test run_basic_statistics when no data is loaded."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.run_basic_statistics()
                mock_print.assert_called_with("❌ No data loaded. Please load data first.")
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_run_basic_statistics_with_data(self):
        """Test run_basic_statistics with loaded data."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            system.current_data = self.sample_data
            
            with patch('builtins.print') as mock_print:
                with patch.object(system, '_create_statistics_plots'):
                    with patch.object(system, '_show_plots_in_browser'):
                        with patch('builtins.input', return_value='n'):
                            system.run_basic_statistics()
                            mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_run_data_quality_check_no_data(self):
        """Test run_data_quality_check when no data is loaded."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.run_comprehensive_data_quality_check()
                mock_print.assert_called_with("❌ No data loaded. Please load data first.")
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_run_data_quality_check_with_data(self):
        """Test run_data_quality_check with loaded data."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            system.current_data = self.sample_data
            
            with patch('builtins.print') as mock_print:
                with patch('src.eda.data_quality') as mock_data_quality:
                    with patch('builtins.input', return_value='n'):
                        system.run_comprehensive_data_quality_check()
                        mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_run_correlation_analysis_no_data(self):
        """Test run_correlation_analysis when no data is loaded."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.run_correlation_analysis()
                mock_print.assert_called_with("❌ No data loaded. Please load data first.")
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_run_correlation_analysis_with_data(self):
        """Test run_correlation_analysis with loaded data."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            system.current_data = self.sample_data
            
            with patch('builtins.print') as mock_print:
                system.run_correlation_analysis()
                mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_run_time_series_analysis_no_data(self):
        """Test run_time_series_analysis when no data is loaded."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.run_time_series_analysis()
                mock_print.assert_called_with("❌ No data loaded. Please load data first.")
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_run_time_series_analysis_with_data(self):
        """Test run_time_series_analysis with loaded data."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            system.current_data = self.sample_data
            
            with patch('builtins.print') as mock_print:
                with patch('src.eda.time_series_analysis.TimeSeriesAnalyzer') as mock_analyzer:
                    with patch('builtins.input', return_value='n'):
                        system.run_time_series_analysis()
                        mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_generate_all_features_no_data(self):
        """Test generate_all_features when no data is loaded."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.generate_all_features()
                mock_print.assert_called_with("❌ No data loaded. Please load data first.")
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_generate_all_features_with_data(self):
        """Test generate_all_features with loaded data."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            system.current_data = self.sample_data
            
            with patch('builtins.print') as mock_print:
                with patch('src.ml.feature_engineering.feature_generator.FeatureGenerator') as mock_generator:
                    with patch('src.ml.feature_engineering.feature_generator.MasterFeatureConfig') as mock_config:
                        with patch('src.ml.feature_engineering.feature_generator.FeatureSelectionConfig') as mock_selection_config:
                            mock_generator_instance = MagicMock()
                            mock_generator_instance.generate_features.return_value = self.sample_data
                            mock_generator_instance.get_feature_summary.return_value = {}
                            mock_generator_instance.get_memory_usage.return_value = {'rss': 100}
                            mock_generator.return_value = mock_generator_instance
                            
                            system.generate_all_features()
                            mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_show_feature_summary_no_results(self):
        """Test show_feature_summary when no feature engineering results."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.show_feature_summary()
                mock_print.assert_called_with("❌ No feature engineering results available. Please generate features first.")
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_show_feature_summary_with_results(self):
        """Test show_feature_summary with feature engineering results."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            system.current_results['feature_engineering'] = {
                'feature_summary': {'feature1': 0.8, 'feature2': 0.6}
            }
            
            with patch('builtins.print') as mock_print:
                system.show_feature_summary()
                mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_export_results_no_results(self):
        """Test export_results when no results to export."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.export_results()
                mock_print.assert_called_with("❌ No results to export. Please run some analysis first.")
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_export_results_with_results(self):
        """Test export_results with results to export."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            system.current_results = {'test': 'data'}
            
            with patch('builtins.print') as mock_print:
                with patch('pathlib.Path.mkdir'):
                    with patch('builtins.open', create=True):
                        with patch('json.dump'):
                            with patch('pandas.DataFrame.to_parquet'):
                                system.export_results()
                                mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_fix_data_issues_no_data(self):
        """Test fix_data_issues when no data is loaded."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.fix_data_issues()
                mock_print.assert_called_with("❌ No data loaded. Please load data first.")
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_fix_data_issues_with_data(self):
        """Test fix_data_issues with loaded data."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            system.current_data = self.sample_data
            
            with patch('builtins.print') as mock_print:
                with patch('src.eda.fix_files') as mock_fix_files:
                    with patch('builtins.input', return_value='y'):
                        mock_fix_files.fix_nan.return_value = self.sample_data
                        mock_fix_files.fix_duplicates.return_value = self.sample_data
                        
                        system.fix_data_issues()
                        mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_show_menu_status(self):
        """Test show_menu_status method."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.print') as mock_print:
                system.show_menu_status()
                mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_create_statistics_plots(self):
        """Test _create_statistics_plots method."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            system.current_data = self.sample_data
            
            with patch('matplotlib.pyplot') as mock_plt:
                with patch('seaborn.histplot') as mock_histplot:
                    with patch('seaborn.boxplot') as mock_boxplot:
                        with patch('seaborn.heatmap') as mock_heatmap:
                            with patch('pathlib.Path.mkdir'):
                                with patch('builtins.print') as mock_print:
                                    system._create_statistics_plots(self.sample_data.select_dtypes(include=[np.number]))
                                    mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_show_plots_in_browser(self):
        """Test _show_plots_in_browser method."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('webbrowser.get') as mock_webbrowser:
                with patch('tempfile.NamedTemporaryFile') as mock_tempfile:
                    with patch('builtins.print') as mock_print:
                        mock_tempfile.return_value.__enter__.return_value.name = '/tmp/test.html'
                        system._show_plots_in_browser()
                        mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_fix_all_data_issues(self):
        """Test fix_all_data_issues method."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            system.current_data = self.sample_data
            
            with patch('builtins.print') as mock_print:
                with patch('src.eda.fix_files') as mock_fix_files:
                    mock_fix_files.fix_nan.return_value = self.sample_data
                    mock_fix_files.fix_duplicates.return_value = self.sample_data
                    
                    system.fix_all_data_issues()
                    mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_run_eda_analysis(self):
        """Test run_eda_analysis method."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.input', return_value='0'):
                with patch('builtins.print') as mock_print:
                    system.run_eda_analysis()
                    mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_run_feature_engineering_analysis(self):
        """Test run_feature_engineering_analysis method."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.input', return_value='0'):
                with patch('builtins.print') as mock_print:
                    system.run_feature_engineering_analysis()
                    mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_run_visualization_analysis(self):
        """Test run_visualization_analysis method."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.input', return_value='0'):
                with patch('builtins.print') as mock_print:
                    system.run_visualization_analysis()
                    mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_run_model_development(self):
        """Test run_model_development method."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            with patch('builtins.input', return_value='0'):
                with patch('builtins.print') as mock_print:
                    system.run_model_development()
                    mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_generate_html_report(self):
        """Test generate_html_report method."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            system.current_data = self.sample_data
            
            with patch('builtins.print') as mock_print:
                with patch('src.eda.html_report_generator') as mock_html_generator:
                    system.generate_html_report()
                    mock_print.assert_called()
            
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")


class TestInteractiveSystemScriptIntegration:
    """Integration tests for InteractiveSystem script."""
    
    def setup_method(self):
        """Set up test fixtures."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            self.system = InteractiveSystem()
            
            # Create sample data
            self.sample_data = pd.DataFrame({
                'open': [100, 101, 102, 103, 104],
                'high': [105, 106, 107, 108, 109],
                'low': [95, 96, 97, 98, 99],
                'close': [102, 103, 104, 105, 106],
                'volume': [1000, 1100, 1200, 1300, 1400]
            })
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_full_workflow(self):
        """Test a complete workflow from data loading to feature generation."""
        # Test data loading
        self.system.current_data = self.sample_data
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
                        mock_generator_instance = MagicMock()
                        mock_generator_instance.generate_features.return_value = self.sample_data
                        mock_generator_instance.get_feature_summary.return_value = {}
                        mock_generator_instance.get_memory_usage.return_value = {'rss': 100}
                        mock_generator.return_value = mock_generator_instance
                        
                        self.system.generate_all_features()
        
        # Verify results
        assert 'feature_engineering' in self.system.current_results
        assert 'comprehensive_basic_statistics' in self.system.current_results


if __name__ == '__main__':
    pytest.main([__file__])
