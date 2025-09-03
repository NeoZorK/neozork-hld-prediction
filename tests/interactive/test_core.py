# -*- coding: utf-8 -*-
"""
Tests for Interactive Core Module

This module tests the interactive core functionality.
"""

import pytest
from unittest.mock import Mock, patch
from src.interactive.core.interactive_system import InteractiveSystem


class TestInteractiveSystem:
    """Test InteractiveSystem functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Mock the managers to avoid complex dependencies
        with patch('src.interactive.core.interactive_system.MenuManager') as mock_menu:
            with patch('src.interactive.core.interactive_system.DataManager') as mock_data:
                with patch('src.interactive.core.interactive_system.AnalysisRunner') as mock_analysis:
                    with patch('src.interactive.core.interactive_system.VisualizationManager') as mock_viz:
                        with patch('src.interactive.core.interactive_system.FeatureEngineeringManager') as mock_fe:
                            # Create mock instances
                            self.mock_menu_manager = Mock()
                            self.mock_data_manager = Mock()
                            self.mock_analysis_runner = Mock()
                            self.mock_viz_manager = Mock()
                            self.mock_fe_manager = Mock()
                            
                            # Configure mocks
                            mock_menu.return_value = self.mock_menu_manager
                            mock_data.return_value = self.mock_data_manager
                            mock_analysis.return_value = self.mock_analysis_runner
                            mock_viz.return_value = self.mock_viz_manager
                            mock_fe.return_value = self.mock_fe_manager
                            
                            # Set up used_menus for backward compatibility
                            self.mock_menu_manager.used_menus = {}
                            
                            # Create the system
                            self.system = InteractiveSystem()
    
    def test_initialization(self):
        """Test system initialization."""
        assert self.system.menu_manager is not None
        assert self.system.data_manager is not None
        assert self.system.analysis_runner is not None
        assert self.system.visualization_manager is not None
        assert self.system.feature_engineering_manager is not None
        assert self.system.current_data is None
        assert self.system.current_results == {}
        assert self.system.feature_generator is None
        assert self.system.used_menus == {}
    
    def test_print_banner(self, capsys):
        """Test banner printing."""
        self.system.print_banner()
        captured = capsys.readouterr()
        
        assert 'NEOZORk HLD PREDICTION - INTERACTIVE SYSTEM' in captured.out
        assert 'Advanced Feature Engineering & EDA Platform' in captured.out
        assert 'ML-Ready Trading System Development' in captured.out
        assert 'Comprehensive Data Analysis & Visualization' in captured.out
    
    def test_safe_input_normal(self, monkeypatch):
        """Test safe input with normal input."""
        # Mock input to return a normal string
        monkeypatch.setattr('builtins.input', lambda x: 'test input')
        
        result = self.system.safe_input("Enter something: ")
        assert result == 'test input'
    
    def test_safe_input_eof(self, monkeypatch):
        """Test safe input with EOF."""
        # Mock input to raise EOFError
        def mock_input(prompt):
            raise EOFError()
        
        monkeypatch.setattr('builtins.input', mock_input)
        
        result = self.system.safe_input("Enter something: ")
        assert result is None
    
    def test_safe_input_keyboard_interrupt(self, monkeypatch):
        """Test safe input with keyboard interrupt."""
        # Mock input to raise KeyboardInterrupt
        def mock_input(prompt):
            raise KeyboardInterrupt()
        
        monkeypatch.setattr('builtins.input', mock_input)
        
        result = self.system.safe_input("Enter something: ")
        assert result is None
    
    def test_calculate_submenu_completion_percentage(self):
        """Test submenu completion percentage calculation."""
        # Mock the menu manager method
        self.mock_menu_manager.calculate_submenu_completion_percentage.return_value = 75
        
        result = self.system.calculate_submenu_completion_percentage('test_category')
        
        assert result == 75
        self.mock_menu_manager.calculate_submenu_completion_percentage.assert_called_once_with('test_category')
    
    def test_mark_menu_as_used(self):
        """Test marking menu as used."""
        self.system.mark_menu_as_used('test_category', 'test_item')
        
        self.mock_menu_manager.mark_menu_as_used.assert_called_once_with('test_category', 'test_item')
    
    def test_reset_menu_status(self):
        """Test resetting menu status."""
        self.system.reset_menu_status('test_category')
        
        self.mock_menu_manager.reset_menu_status.assert_called_once_with('test_category')
    
    def test_show_menu_status(self):
        """Test showing menu status."""
        self.system.show_menu_status()
        
        self.mock_menu_manager.show_menu_status.assert_called_once()
    
    def test_print_main_menu(self, capsys):
        """Test printing main menu."""
        self.system.print_main_menu()
        
        self.mock_menu_manager.print_main_menu.assert_called_once_with(self.system)
    
    def test_print_eda_menu(self, capsys):
        """Test printing EDA menu."""
        self.system.print_eda_menu()
        
        self.mock_menu_manager.print_eda_menu.assert_called_once()
    
    def test_print_feature_engineering_menu(self, capsys):
        """Test printing feature engineering menu."""
        self.system.print_feature_engineering_menu()
        
        self.mock_fe_manager.print_feature_engineering_menu.assert_called_once()
    
    def test_print_visualization_menu(self, capsys):
        """Test printing visualization menu."""
        self.system.print_visualization_menu()
        
        self.mock_viz_manager.print_visualization_menu.assert_called_once()
    
    def test_print_data_management_menu(self, capsys):
        """Test printing data management menu."""
        self.system.print_data_management_menu()
        
        self.mock_data_manager.print_data_management_menu.assert_called_once()
    
    def test_print_analysis_menu(self, capsys):
        """Test printing analysis menu."""
        self.system.print_analysis_menu()
        
        self.mock_analysis_runner.print_analysis_menu.assert_called_once()
    
    def test_get_system_info(self):
        """Test getting system information."""
        info = self.system.get_system_info()
        
        assert info['system_name'] == 'NeoZorK HLD Prediction Interactive System'
        assert info['version'] == '1.0.0'
        assert 'managers' in info
        assert 'current_data' in info
        assert 'current_results' in info
        assert 'feature_generator' in info
        
        # Check manager types
        managers = info['managers']
        assert 'menu_manager' in managers
        assert 'data_manager' in managers
        assert 'analysis_runner' in managers
        assert 'visualization_manager' in managers
        assert 'feature_engineering_manager' in managers


class TestInteractiveSystemIntegration:
    """Test InteractiveSystem integration with mocked components."""
    
    @patch('src.interactive.core.interactive_system.MenuManager')
    @patch('src.interactive.core.interactive_system.DataManager')
    @patch('src.interactive.core.interactive_system.AnalysisRunner')
    @patch('src.interactive.core.interactive_system.VisualizationManager')
    @patch('src.interactive.core.interactive_system.FeatureEngineeringManager')
    def test_system_managers_initialization(self, mock_fe, mock_viz, mock_analysis, mock_data, mock_menu):
        """Test that all managers are properly initialized."""
        # Create mock instances
        mock_menu_instance = Mock()
        mock_data_instance = Mock()
        mock_analysis_instance = Mock()
        mock_viz_instance = Mock()
        mock_fe_instance = Mock()
        
        # Configure mocks
        mock_menu.return_value = mock_menu_instance
        mock_data.return_value = mock_data_instance
        mock_analysis.return_value = mock_analysis_instance
        mock_viz.return_value = mock_viz_instance
        mock_fe.return_value = mock_fe_instance
        
        # Set up used_menus
        mock_menu_instance.used_menus = {}
        
        # Create system
        system = InteractiveSystem()
        
        # Verify all managers were created
        mock_menu.assert_called_once()
        mock_data.assert_called_once()
        mock_analysis.assert_called_once()
        mock_viz.assert_called_once()
        mock_fe.assert_called_once()
        
        # Verify system has references to all managers
        assert system.menu_manager is mock_menu_instance
        assert system.data_manager is mock_data_instance
        assert system.analysis_runner is mock_analysis_instance
        assert system.visualization_manager is mock_viz_instance
        assert system.feature_engineering_manager is mock_fe_instance


class TestInteractiveSystemBackwardCompatibility:
    """Test InteractiveSystem backward compatibility."""
    
    @patch('src.interactive.core.interactive_system.MenuManager')
    @patch('src.interactive.core.interactive_system.DataManager')
    @patch('src.interactive.core.interactive_system.AnalysisRunner')
    @patch('src.interactive.core.interactive_system.VisualizationManager')
    @patch('src.interactive.core.interactive_system.FeatureEngineeringManager')
    def test_used_menus_backward_compatibility(self, mock_fe, mock_viz, mock_analysis, mock_data, mock_menu):
        """Test that used_menus is accessible for backward compatibility."""
        # Create mock instances
        mock_menu_instance = Mock()
        mock_data_instance = Mock()
        mock_analysis_instance = Mock()
        mock_viz_instance = Mock()
        mock_fe_instance = Mock()
        
        # Configure mocks
        mock_menu.return_value = mock_menu_instance
        mock_data.return_value = mock_data_instance
        mock_analysis.return_value = mock_analysis_instance
        mock_viz.return_value = mock_viz_instance
        mock_fe.return_value = mock_fe_instance
        
        # Set up used_menus with some data
        mock_menu_instance.used_menus = {'category1': ['item1', 'item2']}
        
        # Create system
        system = InteractiveSystem()
        
        # Verify backward compatibility
        assert system.used_menus == {'category1': ['item1', 'item2']}
        assert system.used_menus is mock_menu_instance.used_menus


class TestInteractiveSystemErrorHandling:
    """Test InteractiveSystem error handling."""
    
    @patch('src.interactive.core.interactive_system.MenuManager')
    @patch('src.interactive.core.interactive_system.DataManager')
    @patch('src.interactive.core.interactive_system.AnalysisRunner')
    @patch('src.interactive.core.interactive_system.VisualizationManager')
    @patch('src.interactive.core.interactive_system.FeatureEngineeringManager')
    def test_system_creation_with_missing_managers(self, mock_fe, mock_viz, mock_analysis, mock_data, mock_menu):
        """Test system creation handles missing manager dependencies gracefully."""
        # Configure mocks to raise exceptions
        mock_menu.side_effect = Exception("Menu manager creation failed")
        
        # System creation should handle this gracefully
        with pytest.raises(Exception):
            InteractiveSystem()


if __name__ == "__main__":
    pytest.main([__file__])
