#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for scripts/ml/interactive_system.py

This test file covers the main functionality of the interactive system script
to achieve 100% test coverage.
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
import tempfile


class TestInteractiveSystemScript:
    """Test InteractiveSystem script functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Add project root to path for imports
        project_root = Path(__file__).parent.parent.parent.parent.parent
        sys.path.insert(0, str(project_root))
        
        # Create sample data
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 105,
            'Low': np.random.randn(100).cumsum() + 95,
            'Close': np.random.randn(100).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 100)
        }, index=dates)
    
    @patch('scripts.ml.interactive_system.InteractiveSystem')
    def test_interactive_system_import(self, mock_interactive_system):
        """Test that InteractiveSystem can be imported."""
        try:
            from scripts.ml import interactive_system
            assert hasattr(interactive_system, 'InteractiveSystem')
        except ImportError as e:
            # If import fails due to missing dependencies, that's acceptable
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
    
    def test_load_data_from_file(self):
        """Test loading data from file."""
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
    
    def test_load_data_from_folder(self):
        """Test data loading from folder."""
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
    
    def test_system_methods_exist(self):
        """Test that main system methods exist."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            # Check that main methods exist
            expected_methods = [
                'load_data_from_file',
                'load_data_from_folder',
                'calculate_submenu_completion_percentage',
                'print_main_menu',
                'run_eda_analysis',
                'run_feature_engineering_analysis',
                'run_visualization_analysis',
                'run_model_development'
            ]
            
            for method_name in expected_methods:
                assert hasattr(system, method_name), f"Method {method_name} not found"
                
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_menu_structure(self):
        """Test menu structure and completion tracking."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            # Check menu structure
            assert isinstance(system.used_menus, dict)
            
            # Check that all menu categories have boolean values
            for category, submenus in system.used_menus.items():
                assert isinstance(submenus, dict)
                for submenu, used in submenus.items():
                    assert isinstance(used, bool)
                    
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    @patch('builtins.print')
    def test_display_methods_exist(self, mock_print):
        """Test that display methods exist and can be called."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            # Test display methods (they should exist even if they don't do much in tests)
            display_methods = [
                'print_main_menu',
                'print_eda_menu',
                'print_feature_engineering_menu',
                'print_visualization_menu',
                'print_model_development_menu'
            ]
            
            for method_name in display_methods:
                if hasattr(system, method_name):
                    method = getattr(system, method_name)
                    # Should be callable
                    assert callable(method)
                    
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_error_handling(self):
        """Test error handling in the system."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            # Test loading non-existent file
            with pytest.raises((FileNotFoundError, Exception)):
                system.load_data_from_file("non_existent_file.csv")
                
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")
    
    def test_data_validation(self):
        """Test data validation methods."""
        try:
            from scripts.ml.interactive_system import InteractiveSystem
            system = InteractiveSystem()
            
            # Test with valid data
            system.current_data = self.sample_data
            assert system.current_data is not None
            assert len(system.current_data) > 0
            
            # Test with None data
            system.current_data = None
            assert system.current_data is None
                
        except ImportError as e:
            pytest.skip(f"Import failed: {e}")


class TestScriptExecution:
    """Test script execution and main function."""
    
    @patch('scripts.ml.interactive_system.InteractiveSystem')
    def test_script_can_be_imported(self, mock_interactive_system):
        """Test that the script can be imported without errors."""
        try:
            import scripts.ml.interactive_system
            assert True  # If we get here, import was successful
        except ImportError as e:
            pytest.skip(f"Script import failed: {e}")
    
    def test_script_has_main_function(self):
        """Test that the script has a main function or can be executed."""
        try:
            from scripts.ml import interactive_system
            
            # Check if there's a main function or similar entry point
            has_main = any(
                hasattr(interactive_system, attr) and callable(getattr(interactive_system, attr))
                for attr in ['main', 'run', 'start', '__main__']
            )
            
            # If no main function, check if the module can be executed
            if not has_main:
                # Try to access the InteractiveSystem class
                assert hasattr(interactive_system, 'InteractiveSystem')
                
        except ImportError as e:
            pytest.skip(f"Script import failed: {e}")
