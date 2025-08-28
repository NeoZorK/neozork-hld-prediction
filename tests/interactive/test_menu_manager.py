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
from src.interactive.menu_manager import MenuManager


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
        system.current_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [95, 96, 97, 98, 99],
            'Close': [102, 103, 104, 105, 106],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
        system.current_results = {}
        return system
    
    def test_init(self, menu_manager):
        """Test MenuManager initialization."""
        assert menu_manager is not None
        assert 'main' in menu_manager.used_menus
        assert 'eda' in menu_manager.used_menus
        assert 'feature_engineering' in menu_manager.used_menus
        assert 'visualization' in menu_manager.used_menus
        assert 'model_development' in menu_manager.used_menus
    
    def test_calculate_submenu_completion_percentage_main(self, menu_manager):
        """Test calculate_submenu_completion_percentage for main menu."""
        result = menu_manager.calculate_submenu_completion_percentage('main')
        assert result == 0  # Initially no items are used
    
    def test_calculate_submenu_completion_percentage_eda(self, menu_manager):
        """Test calculate_submenu_completion_percentage for eda menu."""
        result = menu_manager.calculate_submenu_completion_percentage('eda')
        assert result == 0  # Initially no items are used
    
    def test_calculate_submenu_completion_percentage_feature_engineering(self, menu_manager):
        """Test calculate_submenu_completion_percentage for feature_engineering menu."""
        result = menu_manager.calculate_submenu_completion_percentage('feature_engineering')
        assert result == 0  # Initially no items are used
    
    def test_calculate_submenu_completion_percentage_visualization(self, menu_manager):
        """Test calculate_submenu_completion_percentage for visualization menu."""
        result = menu_manager.calculate_submenu_completion_percentage('visualization')
        assert result == 0  # Initially no items are used
    
    def test_calculate_submenu_completion_percentage_model_development(self, menu_manager):
        """Test calculate_submenu_completion_percentage for model_development menu."""
        result = menu_manager.calculate_submenu_completion_percentage('model_development')
        assert result == 0  # Initially no items are used
    
    def test_calculate_submenu_completion_percentage_invalid_category(self, menu_manager):
        """Test calculate_submenu_completion_percentage with invalid category."""
        result = menu_manager.calculate_submenu_completion_percentage('invalid_category')
        assert result == 0
    
    def test_calculate_submenu_completion_percentage_with_used_items(self, menu_manager):
        """Test calculate_submenu_completion_percentage with some used items."""
        # Mark some items as used
        menu_manager.used_menus['main']['load_data'] = True
        menu_manager.used_menus['main']['eda_analysis'] = True
        
        result = menu_manager.calculate_submenu_completion_percentage('main')
        assert result == 22  # 2 out of 9 items = 22%
    
    def test_calculate_submenu_completion_percentage_all_used(self, menu_manager):
        """Test calculate_submenu_completion_percentage with all items used."""
        # Mark all items as used
        for item in menu_manager.used_menus['main']:
            menu_manager.used_menus['main'][item] = True
        
        result = menu_manager.calculate_submenu_completion_percentage('main')
        assert result == 100  # All items used = 100%
    
    def test_mark_menu_as_used_valid(self, menu_manager):
        """Test mark_menu_as_used with valid category and item."""
        menu_manager.mark_menu_as_used('main', 'load_data')
        assert menu_manager.used_menus['main']['load_data'] is True
    
    def test_mark_menu_as_used_invalid_category(self, menu_manager):
        """Test mark_menu_as_used with invalid category."""
        menu_manager.mark_menu_as_used('invalid_category', 'load_data')
        # Should not raise an error, just do nothing
    
    def test_mark_menu_as_used_invalid_item(self, menu_manager):
        """Test mark_menu_as_used with invalid item."""
        menu_manager.mark_menu_as_used('main', 'invalid_item')
        # Should not raise an error, just do nothing
    
    def test_reset_menu_status_specific_category(self, menu_manager):
        """Test reset_menu_status for specific category."""
        # Mark some items as used
        menu_manager.used_menus['main']['load_data'] = True
        menu_manager.used_menus['eda']['basic_statistics'] = True
        
        menu_manager.reset_menu_status('main')
        
        # Main menu should be reset
        assert menu_manager.used_menus['main']['load_data'] is False
        # EDA menu should remain unchanged
        assert menu_manager.used_menus['eda']['basic_statistics'] is True
    
    def test_reset_menu_status_all(self, menu_manager):
        """Test reset_menu_status for all categories."""
        # Mark some items as used
        menu_manager.used_menus['main']['load_data'] = True
        menu_manager.used_menus['eda']['basic_statistics'] = True
        menu_manager.used_menus['feature_engineering']['generate_all_features'] = True
        
        menu_manager.reset_menu_status()
        
        # All menus should be reset
        assert menu_manager.used_menus['main']['load_data'] is False
        assert menu_manager.used_menus['eda']['basic_statistics'] is False
        assert menu_manager.used_menus['feature_engineering']['generate_all_features'] is False
    
    def test_show_menu_status(self, menu_manager, capsys):
        """Test show_menu_status method."""
        menu_manager.show_menu_status()
        captured = capsys.readouterr()
        assert "MENU USAGE STATUS" in captured.out
        assert "MAIN:" in captured.out
        assert "EDA:" in captured.out
        assert "FEATURE ENGINEERING:" in captured.out
        assert "VISUALIZATION:" in captured.out
        assert "MODEL DEVELOPMENT:" in captured.out
    
    def test_show_menu_status_with_used_items(self, menu_manager, capsys):
        """Test show_menu_status with some used items."""
        # Mark some items as used
        menu_manager.used_menus['main']['load_data'] = True
        menu_manager.used_menus['eda']['basic_statistics'] = True
        
        menu_manager.show_menu_status()
        captured = capsys.readouterr()
        assert "1/9 items completed" in captured.out  # Main menu
        assert "1/9 items completed" in captured.out  # EDA menu (9 items total)
    
    def test_print_main_menu(self, menu_manager, capsys):
        """Test print_main_menu method."""
        menu_manager.print_main_menu(Mock())
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
    
    def test_print_main_menu_with_used_items(self, menu_manager, capsys):
        """Test print_main_menu with some used items."""
        # Mark some items as used
        menu_manager.used_menus['main']['load_data'] = True
        menu_manager.used_menus['eda']['basic_statistics'] = True
        menu_manager.used_menus['eda']['comprehensive_data_quality_check'] = True
        
        menu_manager.print_main_menu(Mock())
        captured = capsys.readouterr()
        assert "1. 📁 Load Data ✅" in captured.out
        assert "2. 🔍 EDA Analysis (22%)" in captured.out  # 2 out of 9 EDA items = 22%
    
    def test_print_eda_menu(self, menu_manager, capsys):
        """Test print_eda_menu method."""
        menu_manager.print_eda_menu()
        captured = capsys.readouterr()
        assert "EDA ANALYSIS MENU:" in captured.out
        assert "0. 🔙 Back to Main Menu" in captured.out
        assert "1. 🧹 Comprehensive Data Quality Check" in captured.out
        assert "2. 📊 Basic Statistics" in captured.out
        assert "3. 🔗 Correlation Analysis" in captured.out
        assert "4. 📈 Time Series Analysis" in captured.out
        assert "5. 🎯 Feature Importance" in captured.out
        assert "6. 📋 Generate HTML Report" in captured.out
        assert "7. 🔄 Restore from Backup" in captured.out
    
    def test_print_eda_menu_with_used_items(self, menu_manager, capsys):
        """Test print_eda_menu with some used items."""
        # Mark some items as used
        menu_manager.used_menus['eda']['basic_statistics'] = True
        menu_manager.used_menus['eda']['comprehensive_data_quality_check'] = True
        
        menu_manager.print_eda_menu()
        captured = capsys.readouterr()
        assert "1. 🧹 Comprehensive Data Quality Check ✅" in captured.out
        assert "2. 📊 Basic Statistics ✅" in captured.out
        assert "3. 🔗 Correlation Analysis" in captured.out  # Not used
    
    def test_print_feature_engineering_menu(self, menu_manager, capsys):
        """Test print_feature_engineering_menu method."""
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
    
    def test_print_feature_engineering_menu_with_used_items(self, menu_manager, capsys):
        """Test print_feature_engineering_menu with some used items."""
        # Mark some items as used
        menu_manager.used_menus['feature_engineering']['generate_all_features'] = True
        menu_manager.used_menus['feature_engineering']['feature_summary'] = True
        
        menu_manager.print_feature_engineering_menu()
        captured = capsys.readouterr()
        assert "1. 🚀 Generate All Features ✅" in captured.out
        assert "8. 📋 Feature Summary Report ✅" in captured.out
        assert "2. 🎯 Proprietary Features (PHLD/Wave)" in captured.out  # Not used
    
    def test_print_visualization_menu(self, menu_manager, capsys):
        """Test print_visualization_menu method."""
        menu_manager.print_visualization_menu()
        captured = capsys.readouterr()
        assert "DATA VISUALIZATION MENU:" in captured.out
        assert "1. 📈 Price Charts (OHLCV)" in captured.out
        assert "2. 📊 Feature Distribution Plots" in captured.out
        assert "3. 🔗 Correlation Heatmaps" in captured.out
        assert "4. 📈 Time Series Plots" in captured.out
        assert "5. 🎯 Feature Importance Charts" in captured.out
        assert "6. 📋 Export Visualizations" in captured.out
    
    def test_print_visualization_menu_with_used_items(self, menu_manager, capsys):
        """Test print_visualization_menu with some used items."""
        # Mark some items as used
        menu_manager.used_menus['visualization']['price_charts'] = True
        menu_manager.used_menus['visualization']['correlation_heatmaps'] = True
        
        menu_manager.print_visualization_menu()
        captured = capsys.readouterr()
        assert "1. 📈 Price Charts (OHLCV) ✅" in captured.out
        assert "3. 🔗 Correlation Heatmaps ✅" in captured.out
        assert "2. 📊 Feature Distribution Plots" in captured.out  # Not used
    
    def test_print_model_development_menu(self, menu_manager, capsys):
        """Test print_model_development_menu method."""
        menu_manager.print_model_development_menu()
        captured = capsys.readouterr()
        assert "MODEL DEVELOPMENT MENU:" in captured.out
        assert "1. 🎯 Data Preparation" in captured.out
        assert "2. 🔄 Feature Engineering Pipeline" in captured.out
        assert "3. 🤖 ML Model Training" in captured.out
        assert "4. 📊 Model Evaluation" in captured.out
        assert "5. 🧪 Hyperparameter Tuning" in captured.out
        assert "6. 📋 Model Report" in captured.out
    
    def test_print_model_development_menu_with_used_items(self, menu_manager, capsys):
        """Test print_model_development_menu with some used items."""
        # Mark some items as used
        menu_manager.used_menus['model_development']['data_preparation'] = True
        menu_manager.used_menus['model_development']['ml_model_training'] = True
        
        menu_manager.print_model_development_menu()
        captured = capsys.readouterr()
        assert "1. 🎯 Data Preparation ✅" in captured.out
        assert "3. 🤖 ML Model Training ✅" in captured.out
        assert "2. 🔄 Feature Engineering Pipeline" in captured.out  # Not used
    
    def test_show_help(self, menu_manager, capsys):
        """Test show_help method."""
        menu_manager.show_help()
        captured = capsys.readouterr()
        assert "HELP & DOCUMENTATION" in captured.out
        assert "Available Resources:" in captured.out
        assert "Quick Start:" in captured.out
        assert "Tips:" in captured.out
        assert "Feature Engineering Guide:" in captured.out
        assert "EDA Examples:" in captured.out
        assert "Usage Examples:" in captured.out
        assert "ML Module README:" in captured.out
    
    def test_show_system_info(self, menu_manager, capsys, mock_system):
        """Test show_system_info method."""
        menu_manager.show_system_info(mock_system)
        captured = capsys.readouterr()
        assert "SYSTEM INFORMATION" in captured.out
        assert "Python version:" in captured.out
        assert "Pandas version:" in captured.out
        assert "NumPy version:" in captured.out
        assert "Project root:" in captured.out
        assert "Current data: Loaded" in captured.out
        assert "Shape: (5, 5)" in captured.out
        assert "Results available: 0" in captured.out
    
    def test_show_system_info_no_data(self, menu_manager, capsys):
        """Test show_system_info method with no data."""
        system_no_data = Mock()
        system_no_data.current_data = None
        system_no_data.current_results = {}
        
        menu_manager.show_system_info(system_no_data)
        captured = capsys.readouterr()
        assert "Current data: None" in captured.out
        assert "Results available: 0" in captured.out
