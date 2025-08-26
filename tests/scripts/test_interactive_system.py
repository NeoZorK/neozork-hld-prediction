#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for interactive_system.py script.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Mock imports that might not be available in test environment
sys.modules['src.ml.feature_engineering.feature_generator'] = MagicMock()
sys.modules['src.ml.feature_engineering.feature_selector'] = MagicMock()
sys.modules['src.eda'] = MagicMock()
sys.modules['src.eda.fix_files'] = MagicMock()
sys.modules['src.eda.html_report_generator'] = MagicMock()
sys.modules['src.eda.data_quality'] = MagicMock()
sys.modules['src.eda.file_info'] = MagicMock()

from scripts.ml.interactive_system import InteractiveSystem


class TestInteractiveSystem:
    """Test InteractiveSystem class."""
    
    def test_initialization(self):
        """Test InteractiveSystem initialization."""
        system = InteractiveSystem()
        
        assert system.feature_generator is None
        assert system.current_data is None
        assert system.current_results == {}
        assert 'main' in system.used_menus
        assert 'eda' in system.used_menus
        assert 'feature_engineering' in system.used_menus
    
    def test_calculate_submenu_completion_percentage(self):
        """Test submenu completion percentage calculation."""
        system = InteractiveSystem()
        
        # Test with empty menu
        percentage = system.calculate_submenu_completion_percentage('main')
        assert percentage == 0.0
        
        # Test with some completed items
        system.used_menus['main']['load_data'] = True
        system.used_menus['main']['eda_analysis'] = True
        
        percentage = system.calculate_submenu_completion_percentage('main')
        assert percentage > 0.0
        assert percentage <= 100.0
    
    def test_calculate_submenu_completion_percentage_unknown_menu(self):
        """Test submenu completion percentage with unknown menu."""
        system = InteractiveSystem()
        
        percentage = system.calculate_submenu_completion_percentage('unknown_menu')
        assert percentage == 0.0
    
    def test_calculate_submenu_completion_percentage_all_completed(self):
        """Test submenu completion percentage with all items completed."""
        system = InteractiveSystem()
        
        # Mark all items as completed
        for menu_type in system.used_menus:
            for item in system.used_menus[menu_type]:
                system.used_menus[menu_type][item] = True
        
        percentage = system.calculate_submenu_completion_percentage('main')
        assert percentage == 100.0
    
    def test_print_main_menu(self):
        """Test main menu display."""
        system = InteractiveSystem()
        
        with patch('builtins.print') as mock_print:
            system.print_main_menu()
            mock_print.assert_called()
    
    def test_print_eda_menu(self):
        """Test EDA menu display."""
        system = InteractiveSystem()
        
        with patch('builtins.print') as mock_print:
            system.print_eda_menu()
            mock_print.assert_called()
    
    def test_print_feature_engineering_menu(self):
        """Test feature engineering menu display."""
        system = InteractiveSystem()
        
        with patch('builtins.print') as mock_print:
            system.print_feature_engineering_menu()
            mock_print.assert_called()
    
    def test_print_visualization_menu(self):
        """Test visualization menu display."""
        system = InteractiveSystem()
        
        with patch('builtins.print') as mock_print:
            system.print_visualization_menu()
            mock_print.assert_called()
    
    def test_print_model_development_menu(self):
        """Test model development menu display."""
        system = InteractiveSystem()
        
        with patch('builtins.print') as mock_print:
            system.print_model_development_menu()
            mock_print.assert_called()
    
    def test_load_data_from_file(self):
        """Test data loading from file functionality."""
        system = InteractiveSystem()
        
        # Create mock data
        mock_data = pd.DataFrame({
            'Open': [100, 101, 102],
            'High': [105, 106, 107],
            'Low': [95, 96, 97],
            'Close': [103, 104, 105],
            'Volume': [1000, 1100, 1200]
        })
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pandas.read_csv', return_value=mock_data):
            result = system.load_data_from_file('test_file.csv')
            
            assert result is not None
            assert len(result) == 3
    
    def test_load_data_from_file_not_found(self):
        """Test data loading with file not found."""
        system = InteractiveSystem()
        
        with patch('pathlib.Path.exists', return_value=False), \
             patch('builtins.print') as mock_print:
            try:
                result = system.load_data_from_file('nonexistent_file.csv')
                assert False, "Should have raised FileNotFoundError"
            except FileNotFoundError:
                # Expected behavior
                pass
    
    def test_mark_menu_as_used(self):
        """Test marking menu as used."""
        system = InteractiveSystem()
        
        with patch('builtins.print') as mock_print:
            system.mark_menu_as_used('main', 'load_data')
            
            assert system.used_menus['main']['load_data'] is True
            mock_print.assert_called()
    
    def test_reset_menu_status(self):
        """Test resetting menu status."""
        system = InteractiveSystem()
        
        # Mark some items as used
        system.used_menus['main']['load_data'] = True
        system.used_menus['main']['eda_analysis'] = True
        
        with patch('builtins.print') as mock_print:
            system.reset_menu_status('main')
            
            assert system.used_menus['main']['load_data'] is False
            assert system.used_menus['main']['eda_analysis'] is False
            mock_print.assert_called()
    
    def test_show_menu_status(self):
        """Test showing menu status."""
        system = InteractiveSystem()
        
        with patch('builtins.print') as mock_print:
            system.show_menu_status()
            mock_print.assert_called()
    
    def test_safe_input(self):
        """Test safe input handling."""
        system = InteractiveSystem()
        
        with patch('builtins.input', return_value='test'):
            result = system.safe_input("Test prompt")
            assert result == 'test'
    
    def test_safe_input_eof(self):
        """Test safe input handling with EOF."""
        system = InteractiveSystem()
        
        with patch('builtins.input', side_effect=EOFError), \
             patch('builtins.print') as mock_print:
            result = system.safe_input("Test prompt")
            assert result is None
            mock_print.assert_called()
    
    def test_print_banner(self):
        """Test banner printing."""
        system = InteractiveSystem()
        
        with patch('builtins.print') as mock_print:
            system.print_banner()
            mock_print.assert_called()
    
    def test_str_representation(self):
        """Test string representation."""
        system = InteractiveSystem()
        
        result = str(system)
        assert 'InteractiveSystem' in result
    
    def test_repr_representation(self):
        """Test detailed string representation."""
        system = InteractiveSystem()
        
        result = repr(system)
        assert 'InteractiveSystem' in result


class TestInteractiveSystemIntegration:
    """Integration tests for InteractiveSystem."""
    
    def test_full_menu_navigation_workflow(self):
        """Test complete menu navigation workflow."""
        system = InteractiveSystem()
        
        # Test main menu
        with patch('builtins.input', return_value='0'), \
             patch('builtins.print') as mock_print:
            system.run()
            mock_print.assert_called()
    
    def test_data_loading_workflow(self):
        """Test data loading workflow."""
        system = InteractiveSystem()
        
        # Create mock data
        mock_data = pd.DataFrame({
            'Open': [100, 101, 102],
            'High': [105, 106, 107],
            'Low': [95, 96, 97],
            'Close': [103, 104, 105],
            'Volume': [1000, 1100, 1200]
        })
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pandas.read_csv', return_value=mock_data):
            result = system.load_data_from_file('test_file.csv')
            
            # Validate data is loaded
            assert result is not None
            assert len(result) == 3
            assert 'Open' in result.columns
    
    def test_menu_completion_tracking(self):
        """Test menu completion tracking."""
        system = InteractiveSystem()
        
        # Initially no completion
        assert system.calculate_submenu_completion_percentage('main') == 0.0
        
        # Mark some items as completed
        system.used_menus['main']['load_data'] = True
        system.used_menus['main']['eda_analysis'] = True
        
        # Check completion percentage
        percentage = system.calculate_submenu_completion_percentage('main')
        assert percentage > 0.0
        assert percentage < 100.0
        
        # Mark all items as completed
        for item in system.used_menus['main']:
            system.used_menus['main'][item] = True
        
        # Check 100% completion
        assert system.calculate_submenu_completion_percentage('main') == 100.0


if __name__ == "__main__":
    pytest.main([__file__])
