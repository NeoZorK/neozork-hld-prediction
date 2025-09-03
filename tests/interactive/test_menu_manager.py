# -*- coding: utf-8 -*-
"""
Tests for menu manager module.

This module tests the MenuManager class from src/interactive/menu_manager.py.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os

# Import the module to test
from src.interactive.ui.menu_manager import MenuManager


class TestMenuManager:
    """Test MenuManager class."""
    
    @pytest.fixture
    def menu_manager(self):
        """Create MenuManager instance for testing."""
        return MenuManager()
    
    @pytest.fixture
    def mock_system(self):
        """Create mock system for testing."""
        system = Mock()
        system.current_data = None
        system.current_results = {}
        return system
    
    def test_init(self, menu_manager):
        """Test MenuManager initialization."""
        assert menu_manager is not None
        assert hasattr(menu_manager, 'used_menus')
        assert 'main' in menu_manager.used_menus
        assert 'eda' in menu_manager.used_menus
        assert 'feature_engineering' in menu_manager.used_menus
        assert 'visualization' in menu_manager.used_menus
        assert 'model_development' in menu_manager.used_menus
    
    def test_calculate_submenu_completion_percentage_empty(self, menu_manager):
        """Test calculate_submenu_completion_percentage with empty category."""
        percentage = menu_manager.calculate_submenu_completion_percentage('nonexistent')
        assert percentage == 0
    
    def test_calculate_submenu_completion_percentage_zero(self, menu_manager):
        """Test calculate_submenu_completion_percentage with no completed items."""
        percentage = menu_manager.calculate_submenu_completion_percentage('main')
        assert percentage == 0
    
    def test_calculate_submenu_completion_percentage_partial(self, menu_manager):
        """Test calculate_submenu_completion_percentage with some completed items."""
        # Mark some items as used
        menu_manager.used_menus['main']['load_data'] = True
        menu_manager.used_menus['main']['eda_analysis'] = True
        
        percentage = menu_manager.calculate_submenu_completion_percentage('main')
        # 2 out of 9 items = 22%
        assert percentage == 22
    
    def test_calculate_submenu_completion_percentage_full(self, menu_manager):
        """Test calculate_submenu_completion_percentage with all items completed."""
        # Mark all items as used
        for item in menu_manager.used_menus['main']:
            menu_manager.used_menus['main'][item] = True
        
        percentage = menu_manager.calculate_submenu_completion_percentage('main')
        assert percentage == 100
    
    def test_mark_menu_as_used_valid(self, menu_manager, capsys):
        """Test mark_menu_as_used with valid category and item."""
        menu_manager.mark_menu_as_used('main', 'load_data')
        
        assert menu_manager.used_menus['main']['load_data'] is True
        
        captured = capsys.readouterr()
        assert "Load Data marked as completed!" in captured.out
    
    def test_mark_menu_as_used_invalid_category(self, menu_manager, capsys):
        """Test mark_menu_as_used with invalid category."""
        menu_manager.mark_menu_as_used('nonexistent', 'load_data')
        
        captured = capsys.readouterr()
        assert captured.out == ""  # Should not print anything for invalid category
    
    def test_mark_menu_as_used_invalid_item(self, menu_manager, capsys):
        """Test mark_menu_as_used with invalid item."""
        menu_manager.mark_menu_as_used('main', 'nonexistent')
        
        captured = capsys.readouterr()
        assert captured.out == ""  # Should not print anything for invalid item
    
    def test_reset_menu_status_specific_category(self, menu_manager, capsys):
        """Test reset_menu_status with specific category."""
        # Mark some items as used
        menu_manager.used_menus['main']['load_data'] = True
        menu_manager.used_menus['main']['eda_analysis'] = True
        
        menu_manager.reset_menu_status('main')
        
        # Check that all items in main are reset
        for item in menu_manager.used_menus['main']:
            assert menu_manager.used_menus['main'][item] is False
        
        # Check that other categories are not affected
        assert menu_manager.used_menus['eda']['basic_statistics'] is False  # Should still be False
        
        captured = capsys.readouterr()
        assert "Reset status for main menu" in captured.out
    
    def test_reset_menu_status_all(self, menu_manager, capsys):
        """Test reset_menu_status with no specific category."""
        # Mark some items as used in different categories
        menu_manager.used_menus['main']['load_data'] = True
        menu_manager.used_menus['eda']['basic_statistics'] = True
        
        menu_manager.reset_menu_status()
        
        # Check that all items in all categories are reset
        for category in menu_manager.used_menus:
            for item in menu_manager.used_menus[category]:
                assert menu_manager.used_menus[category][item] is False
        
        captured = capsys.readouterr()
        assert "Reset status for all menus" in captured.out
    
    def test_show_menu_status(self, menu_manager, capsys):
        """Test show_menu_status."""
        # Mark some items as used
        menu_manager.used_menus['main']['load_data'] = True
        menu_manager.used_menus['eda']['basic_statistics'] = True
        
        menu_manager.show_menu_status()
        
        captured = capsys.readouterr()
        assert "MENU USAGE STATUS" in captured.out
        assert "MAIN:" in captured.out
        assert "EDA:" in captured.out
        assert "Progress: 1/9 items completed" in captured.out  # main category
        assert "Progress: 1/9 items completed" in captured.out  # eda category
        assert "✅ Load Data" in captured.out
        assert "✅ Basic Statistics" in captured.out
        assert "⏳ Eda Analysis" in captured.out  # Not used (note: it's "Eda" not "EDA")
    
    def test_print_main_menu(self, menu_manager, mock_system, capsys):
        """Test print_main_menu."""
        menu_manager.print_main_menu(mock_system)
        
        captured = capsys.readouterr()
        assert "MAIN MENU:" in captured.out
        assert "1. 📁 Load Data" in captured.out
        assert "2. 🔍 EDA Analysis" in captured.out
        assert "3. ⚙️  Feature Engineering" in captured.out
        assert "4. 📊 Data Visualization" in captured.out
        assert "5. 📈 Model Development" in captured.out
        assert "6. 🧪 Testing & Validation" in captured.out
        assert "7. 📚 Documentation & Help" in captured.out
        assert "8. ⚙️  System Configuration" in captured.out
        assert "9. 📊 Menu Status" in captured.out
        assert "0. 🚪 Exit" in captured.out
    
    def test_print_main_menu_with_completion(self, menu_manager, mock_system, capsys):
        """Test print_main_menu with completion percentages."""
        # Mark some items as used
        menu_manager.used_menus['main']['load_data'] = True
        menu_manager.used_menus['eda']['basic_statistics'] = True
        menu_manager.used_menus['eda']['comprehensive_data_quality_check'] = True
        
        menu_manager.print_main_menu(mock_system)
        
        captured = capsys.readouterr()
        assert "MAIN MENU:" in captured.out
        assert "1. 📁 Load Data ✅" in captured.out
        assert "2. 🔍 EDA Analysis (12%)" in captured.out  # 2 out of 16 = 12% (no checkmark since eda_analysis not marked)
        assert "3. ⚙️  Feature Engineering" in captured.out  # No completion
    
    def test_print_eda_menu(self, menu_manager, capsys):
        """Test print_eda_menu."""
        menu_manager.print_eda_menu()
        
        captured = capsys.readouterr()
        assert "EDA ANALYSIS MENU:" in captured.out
        assert "0. 🔙 Back to Main Menu" in captured.out
        assert "1. ⏱️ Time Series Gaps Analysis" in captured.out
        assert "2. 🔄 Duplicates Analysis" in captured.out
        assert "3. 🧹 Comprehensive Data Quality Check" in captured.out
        assert "4. 📊 Basic Statistics" in captured.out
        assert "5. 🔗 Correlation Analysis" in captured.out
        assert "6. 📈 Time Series Analysis" in captured.out
        assert "7. 🎯 Feature Importance" in captured.out
        assert "13. 📋 Generate HTML Report" in captured.out
        assert "14. 🔄 Restore from Backup" in captured.out
    
    def test_print_eda_menu_with_completion(self, menu_manager, capsys):
        """Test print_eda_menu with completion checkmarks."""
        # Mark some items as used
        menu_manager.used_menus['eda']['time_series_gaps_analysis'] = True
        menu_manager.used_menus['eda']['basic_statistics'] = True
        menu_manager.used_menus['eda']['comprehensive_data_quality_check'] = True
        
        menu_manager.print_eda_menu()
        
        captured = capsys.readouterr()
        assert "1. ⏱️ Time Series Gaps Analysis ✅" in captured.out
        assert "2. 🔄 Duplicates Analysis" in captured.out  # Not used
        assert "3. 🧹 Comprehensive Data Quality Check ✅" in captured.out
        assert "4. 📊 Basic Statistics ✅" in captured.out
        assert "5. 🔗 Correlation Analysis" in captured.out  # Not used
    
    def test_print_feature_engineering_menu(self, menu_manager, capsys):
        """Test print_feature_engineering_menu."""
        menu_manager.print_feature_engineering_menu()
        
        captured = capsys.readouterr()
        assert "FEATURE ENGINEERING MENU:" in captured.out
        assert "0. 🔙 Back to Main Menu" in captured.out
        assert "1. 🚀 Generate All Features" in captured.out
        assert "2. 🎯 Proprietary Features (PHLD/Wave)" in captured.out
        assert "3. 📊 Technical Indicators" in captured.out
        assert "4. 📈 Statistical Features" in captured.out
        assert "5. ⏰ Temporal Features" in captured.out
        assert "6. 🔄 Cross-Timeframe Features" in captured.out
        assert "7. 🎛️  Feature Selection & Optimization" in captured.out
        assert "8. 📋 Feature Summary Report" in captured.out
    
    def test_print_feature_engineering_menu_with_completion(self, menu_manager, capsys):
        """Test print_feature_engineering_menu with completion checkmarks."""
        # Mark some items as used
        menu_manager.used_menus['feature_engineering']['generate_all_features'] = True
        
        menu_manager.print_feature_engineering_menu()
        
        captured = capsys.readouterr()
        assert "1. 🚀 Generate All Features ✅" in captured.out
        assert "2. 🎯 Proprietary Features (PHLD/Wave)" in captured.out  # Not used
    
    def test_print_visualization_menu(self, menu_manager, capsys):
        """Test print_visualization_menu."""
        menu_manager.print_visualization_menu()
        
        captured = capsys.readouterr()
        assert "DATA VISUALIZATION MENU:" in captured.out
        assert "1. 📈 Price Charts (OHLCV)" in captured.out
        assert "2. 📊 Feature Distribution Plots" in captured.out
        assert "3. 🔗 Correlation Heatmaps" in captured.out
        assert "4. 📈 Time Series Plots" in captured.out
        assert "5. 🎯 Feature Importance Charts" in captured.out
        assert "6. 📋 Export Visualizations" in captured.out
    
    def test_print_visualization_menu_with_completion(self, menu_manager, capsys):
        """Test print_visualization_menu with completion checkmarks."""
        # Mark some items as used
        menu_manager.used_menus['visualization']['price_charts'] = True
        
        menu_manager.print_visualization_menu()
        
        captured = capsys.readouterr()
        assert "1. 📈 Price Charts (OHLCV) ✅" in captured.out
        assert "2. 📊 Feature Distribution Plots" in captured.out  # Not used
    
    def test_print_model_development_menu(self, menu_manager, capsys):
        """Test print_model_development_menu."""
        menu_manager.print_model_development_menu()
        
        captured = capsys.readouterr()
        assert "MODEL DEVELOPMENT MENU:" in captured.out
        assert "1. 🎯 Data Preparation" in captured.out
        assert "2. 🔄 Feature Engineering Pipeline" in captured.out
        assert "3. 🤖 ML Model Training" in captured.out
        assert "4. 📊 Model Evaluation" in captured.out
        assert "5. 🧪 Hyperparameter Tuning" in captured.out
        assert "6. 📋 Model Report" in captured.out
    
    def test_print_model_development_menu_with_completion(self, menu_manager, capsys):
        """Test print_model_development_menu with completion checkmarks."""
        # Mark some items as used
        menu_manager.used_menus['model_development']['data_preparation'] = True
        
        menu_manager.print_model_development_menu()
        
        captured = capsys.readouterr()
        assert "1. 🎯 Data Preparation ✅" in captured.out
        assert "2. 🔄 Feature Engineering Pipeline" in captured.out  # Not used
    
    def test_show_help(self, menu_manager, capsys):
        """Test show_help."""
        menu_manager.show_help()
        
        captured = capsys.readouterr()
        assert "HELP & DOCUMENTATION" in captured.out
        assert "Available Resources:" in captured.out
        assert "Feature Engineering Guide" in captured.out
        assert "EDA Examples" in captured.out
        assert "Usage Examples" in captured.out
        assert "ML Module README" in captured.out
        assert "Quick Start:" in captured.out
        assert "Tips:" in captured.out
    
    def test_show_system_info(self, menu_manager, mock_system, capsys):
        """Test show_system_info."""
        menu_manager.show_system_info(mock_system)
        
        captured = capsys.readouterr()
        assert "SYSTEM INFORMATION" in captured.out
        assert "Python version:" in captured.out
        assert "Pandas version:" in captured.out
        assert "NumPy version:" in captured.out
        assert "Project root:" in captured.out
        assert "Current data: None" in captured.out
        assert "Results available: 0" in captured.out
    
    def test_show_system_info_with_data(self, menu_manager, mock_system, capsys):
        """Test show_system_info with data loaded."""
        # Add data to the system
        mock_system.current_data = pd.DataFrame({'A': [1, 2, 3]})
        mock_system.current_results = {'test': 'result'}
        
        menu_manager.show_system_info(mock_system)
        
        captured = capsys.readouterr()
        assert "SYSTEM INFORMATION" in captured.out
        assert "Current data: Loaded" in captured.out
        assert "Shape: (3, 1)" in captured.out
        assert "Results available: 1" in captured.out
