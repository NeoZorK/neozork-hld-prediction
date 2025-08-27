# -*- coding: utf-8 -*-
"""
Tests for interactive_system.py.

This module tests the interactive system interface for NeoZorK HLD Prediction.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os

# Import the module to test
from scripts.ml.interactive_system import InteractiveSystem


class TestInteractiveSystem:
    """Test InteractiveSystem class."""
    
    @pytest.fixture
    def interactive_system(self):
        """Create InteractiveSystem instance for testing."""
        return InteractiveSystem()
    
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
    
    def test_init(self, interactive_system):
        """Test InteractiveSystem initialization."""
        assert interactive_system.feature_generator is None
        assert interactive_system.current_data is None
        assert interactive_system.current_results == {}
        assert 'main' in interactive_system.used_menus
        assert 'eda' in interactive_system.used_menus
        assert 'feature_engineering' in interactive_system.used_menus
    
    def test_calculate_submenu_completion_percentage(self, interactive_system):
        """Test submenu completion percentage calculation."""
        # Test with no completion
        percentage = interactive_system.calculate_submenu_completion_percentage('main')
        assert percentage == 0
        
        # Test with partial completion
        interactive_system.used_menus['main']['load_data'] = True
        interactive_system.used_menus['main']['eda_analysis'] = True
        percentage = interactive_system.calculate_submenu_completion_percentage('main')
        assert percentage == 22  # 2/9 * 100 rounded
        
        # Test with full completion
        for key in interactive_system.used_menus['main']:
            interactive_system.used_menus['main'][key] = True
        percentage = interactive_system.calculate_submenu_completion_percentage('main')
        assert percentage == 100
        
        # Test with invalid category
        percentage = interactive_system.calculate_submenu_completion_percentage('invalid')
        assert percentage == 0
    
    def test_mark_menu_as_used(self, interactive_system):
        """Test marking menu items as used."""
        # Test marking a valid menu item
        interactive_system.mark_menu_as_used('main', 'load_data')
        assert interactive_system.used_menus['main']['load_data'] is True
        
        # Test marking an invalid menu item (should not raise error)
        interactive_system.mark_menu_as_used('main', 'invalid_item')
        # Should not affect anything
    
    def test_reset_menu_status(self, interactive_system):
        """Test resetting menu status."""
        # Set some menu items as used
        interactive_system.used_menus['main']['load_data'] = True
        interactive_system.used_menus['eda']['basic_statistics'] = True
        
        # Reset specific category
        interactive_system.reset_menu_status('main')
        assert interactive_system.used_menus['main']['load_data'] is False
        assert interactive_system.used_menus['eda']['basic_statistics'] is True  # Should remain
        
        # Reset all categories
        interactive_system.reset_menu_status()
        assert interactive_system.used_menus['main']['load_data'] is False
        assert interactive_system.used_menus['eda']['basic_statistics'] is False
    
    def test_safe_input(self, interactive_system):
        """Test safe input handling."""
        # Test normal input
        with patch('builtins.input', return_value='test input'):
            result = interactive_system.safe_input("Enter something: ")
            assert result == 'test input'
        
        # Test EOF handling
        with patch('builtins.input', side_effect=EOFError):
            result = interactive_system.safe_input("Enter something: ")
            assert result is None
    
    def test_print_banner(self, interactive_system, capsys):
        """Test banner printing."""
        interactive_system.print_banner()
        captured = capsys.readouterr()
        assert "NEOZORk HLD PREDICTION" in captured.out
        assert "INTERACTIVE SYSTEM" in captured.out
    
    def test_load_data_from_file_csv(self, interactive_system, sample_data):
        """Test loading data from CSV file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            sample_data.to_csv(f.name, index=True)
            temp_file = f.name
        
        try:
            result = interactive_system.load_data_from_file(temp_file)
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 100
            assert 'Open' in result.columns
        finally:
            os.unlink(temp_file)
    
    def test_load_data_from_file_parquet(self, interactive_system, sample_data):
        """Test loading data from parquet file."""
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as f:
            sample_data.to_parquet(f.name)
            temp_file = f.name
        
        try:
            result = interactive_system.load_data_from_file(temp_file)
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 100
            assert 'Open' in result.columns
        finally:
            os.unlink(temp_file)
    
    def test_load_data_from_file_invalid_format(self, interactive_system):
        """Test loading data from invalid file format."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b"invalid data")
            temp_file = f.name
        
        try:
            with pytest.raises(ValueError, match="Unsupported file format"):
                interactive_system.load_data_from_file(temp_file)
        finally:
            os.unlink(temp_file)
    
    def test_load_data_from_file_not_found(self, interactive_system):
        """Test loading data from non-existent file."""
        with pytest.raises(FileNotFoundError):
            interactive_system.load_data_from_file("nonexistent_file.csv")
    
    def test_load_data_from_folder(self, interactive_system, sample_data):
        """Test loading data files from folder."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some data files
            csv_file = os.path.join(temp_dir, "data1.csv")
            parquet_file = os.path.join(temp_dir, "data2.parquet")
            txt_file = os.path.join(temp_dir, "ignore.txt")
            
            sample_data.to_csv(csv_file, index=True)
            sample_data.to_parquet(parquet_file)
            with open(txt_file, 'w') as f:
                f.write("ignore this")
            
            result = interactive_system.load_data_from_folder(temp_dir)
            assert len(result) == 2
            assert any('data1.csv' in f for f in result)
            assert any('data2.parquet' in f for f in result)
            assert not any('ignore.txt' in f for f in result)
    
    def test_load_data_from_folder_not_found(self, interactive_system):
        """Test loading data from non-existent folder."""
        with pytest.raises(FileNotFoundError):
            interactive_system.load_data_from_folder("nonexistent_folder")
    
    def test_load_data_from_folder_not_directory(self, interactive_system):
        """Test loading data from path that is not a directory."""
        with tempfile.NamedTemporaryFile() as f:
            with pytest.raises(ValueError, match="Path is not a directory"):
                interactive_system.load_data_from_folder(f.name)
    
    @patch('builtins.input')
    def test_load_data_interactive(self, mock_input, interactive_system, sample_data):
        """Test interactive data loading."""
        # Mock input to select first folder and exit
        mock_input.side_effect = ['0']  # Go back to main menu
        
        # Mock data folder structure
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.iterdir') as mock_iterdir:
                mock_iterdir.return_value = [Mock(is_dir=lambda: True)]
                
                result = interactive_system.load_data()
                assert result is False  # User chose to go back
    
    def test_run_basic_statistics_no_data(self, interactive_system, capsys):
        """Test running basic statistics with no data loaded."""
        interactive_system.run_basic_statistics()
        captured = capsys.readouterr()
        assert "No data loaded" in captured.out
    
    def test_run_basic_statistics_with_data(self, interactive_system, sample_data, capsys):
        """Test running basic statistics with data loaded."""
        interactive_system.current_data = sample_data
        
        with patch('builtins.input', return_value='n'):  # Don't show preview
            interactive_system.run_basic_statistics()
        
        captured = capsys.readouterr()
        assert "COMPREHENSIVE BASIC STATISTICS" in captured.out
        assert "DESCRIPTIVE STATISTICS" in captured.out
    
    def test_run_data_quality_check_no_data(self, interactive_system, capsys):
        """Test running data quality check with no data loaded."""
        interactive_system.run_data_quality_check()
        captured = capsys.readouterr()
        assert "No data loaded" in captured.out
    
    def test_run_data_quality_check_with_data(self, interactive_system, sample_data, capsys):
        """Test running data quality check with data loaded."""
        interactive_system.current_data = sample_data
        
        with patch('builtins.input', return_value='n'):  # Don't fix issues
            interactive_system.run_data_quality_check()
        
        captured = capsys.readouterr()
        assert "COMPREHENSIVE DATA QUALITY CHECK" in captured.out
    
    def test_run_correlation_analysis_no_data(self, interactive_system, capsys):
        """Test running correlation analysis with no data loaded."""
        interactive_system.run_correlation_analysis()
        captured = capsys.readouterr()
        assert "No data loaded" in captured.out
    
    def test_run_correlation_analysis_with_data(self, interactive_system, sample_data, capsys):
        """Test running correlation analysis with data loaded."""
        interactive_system.current_data = sample_data
        interactive_system.run_correlation_analysis()
        
        captured = capsys.readouterr()
        assert "CORRELATION ANALYSIS" in captured.out
        assert "Correlation analysis completed" in captured.out
    
    def test_run_time_series_analysis_no_data(self, interactive_system, capsys):
        """Test running time series analysis with no data loaded."""
        interactive_system.run_time_series_analysis()
        captured = capsys.readouterr()
        assert "No data loaded" in captured.out
    
    def test_show_menu_status(self, interactive_system, capsys):
        """Test showing menu status."""
        # Set some menu items as used
        interactive_system.used_menus['main']['load_data'] = True
        interactive_system.used_menus['eda']['basic_statistics'] = True
        
        interactive_system.show_menu_status()
        captured = capsys.readouterr()
        assert "MENU USAGE STATUS" in captured.out
        assert "MAIN:" in captured.out
        assert "EDA:" in captured.out
    
    def test_str_repr(self, interactive_system):
        """Test string representation."""
        assert "InteractiveSystem" in str(interactive_system)
        assert "InteractiveSystem" in repr(interactive_system)


class TestInteractiveSystemMenuPrinting:
    """Test menu printing methods."""
    
    @pytest.fixture
    def interactive_system(self):
        """Create InteractiveSystem instance for testing."""
        return InteractiveSystem()
    
    def test_print_main_menu(self, interactive_system, capsys):
        """Test main menu printing."""
        interactive_system.print_main_menu()
        captured = capsys.readouterr()
        assert "MAIN MENU:" in captured.out
        assert "Load Data" in captured.out
        assert "EDA Analysis" in captured.out
        assert "Feature Engineering" in captured.out
    
    def test_print_eda_menu(self, interactive_system, capsys):
        """Test EDA menu printing."""
        interactive_system.print_eda_menu()
        captured = capsys.readouterr()
        assert "EDA ANALYSIS MENU:" in captured.out
        assert "Basic Statistics" in captured.out
        assert "Data Quality Check" in captured.out
    
    def test_print_feature_engineering_menu(self, interactive_system, capsys):
        """Test feature engineering menu printing."""
        interactive_system.print_feature_engineering_menu()
        captured = capsys.readouterr()
        assert "FEATURE ENGINEERING MENU:" in captured.out
        assert "Generate All Features" in captured.out
        assert "Technical Indicators" in captured.out
    
    def test_print_visualization_menu(self, interactive_system, capsys):
        """Test visualization menu printing."""
        interactive_system.print_visualization_menu()
        captured = capsys.readouterr()
        assert "DATA VISUALIZATION MENU:" in captured.out
        assert "Price Charts" in captured.out
        assert "Feature Distribution Plots" in captured.out
    
    def test_print_model_development_menu(self, interactive_system, capsys):
        """Test model development menu printing."""
        interactive_system.print_model_development_menu()
        captured = capsys.readouterr()
        assert "MODEL DEVELOPMENT MENU:" in captured.out
        assert "Data Preparation" in captured.out
        assert "ML Model Training" in captured.out


class TestInteractiveSystemDataHandling:
    """Test data handling methods."""
    
    @pytest.fixture
    def interactive_system(self):
        """Create InteractiveSystem instance for testing."""
        return InteractiveSystem()
    
    # Note: InteractiveSystem doesn't have these methods, so we skip these tests
    # They are tested in the base_feature_generator tests instead


class TestInteractiveSystemFeatureManagement:
    """Test feature management methods."""
    
    @pytest.fixture
    def interactive_system(self):
        """Create InteractiveSystem instance for testing."""
        return InteractiveSystem()
    
    # Note: InteractiveSystem doesn't have these methods, so we skip these tests
    # They are tested in the feature engineering modules instead
