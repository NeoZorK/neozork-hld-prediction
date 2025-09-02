# -*- coding: utf-8 -*-
"""
Tests for interactive visualization manager module.

This module tests the VisualizationManager class from src/interactive/visualization_manager.py.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os

# Import the module to test
from src.interactive.visualization_manager import VisualizationManager


class TestVisualizationManager:
    """Test VisualizationManager class."""
    
    @pytest.fixture
    def visualization_manager(self):
        """Create VisualizationManager instance for testing."""
        return VisualizationManager()
    
    @pytest.fixture
    def mock_system(self):
        """Create a mock system for testing."""
        system = Mock()
        system.safe_input = Mock()
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
    
    def test_init(self, visualization_manager):
        """Test VisualizationManager initialization."""
        assert visualization_manager is not None
        assert isinstance(visualization_manager, VisualizationManager)
    
    def test_run_visualization_analysis(self, visualization_manager, mock_system, capsys):
        """Test run_visualization_analysis method."""
        # Mock menu_manager to actually print the menu
        mock_menu_manager = MagicMock()
        mock_menu_manager.print_visualization_menu.side_effect = lambda: print("📊 DATA VISUALIZATION MENU:")
        mock_system.menu_manager = mock_menu_manager
        
        with patch('builtins.input', return_value='0'):
            visualization_manager.run_visualization_analysis(mock_system)
            
            # Check output
            captured = capsys.readouterr()
            assert "DATA VISUALIZATION MENU:" in captured.out
            
            # Check that menu_manager.print_visualization_menu was called
            mock_menu_manager.print_visualization_menu.assert_called()
    
    def test_run_visualization_analysis_with_real_system(self, visualization_manager, capsys):
        """Test run_visualization_analysis with a real system-like object."""
        # Create a simple object with safe_input method
        class SimpleSystem:
            def safe_input(self):
                pass
            
            @property
            def menu_manager(self):
                return MagicMock()
        
        system = SimpleSystem()
        
        with patch('builtins.input', return_value='0'):
            with patch.object(system, 'safe_input') as mock_input:
                visualization_manager.run_visualization_analysis(system)
                
                # Check that the method completed without error
                # The MagicMock menu_manager won't print anything, so we just verify it runs
    
    def test_str_repr(self, visualization_manager):
        """Test string representation."""
        assert "VisualizationManager" in str(visualization_manager)
        assert "VisualizationManager" in repr(visualization_manager)


class TestVisualizationManagerIntegration:
    """Test VisualizationManager integration scenarios."""
    
    @pytest.fixture
    def visualization_manager(self):
        """Create VisualizationManager instance for testing."""
        return VisualizationManager()
    
    def test_manager_initialization(self, visualization_manager):
        """Test that the manager is properly initialized."""
        assert visualization_manager is not None
        assert hasattr(visualization_manager, 'run_visualization_analysis')
    
    def test_manager_methods_exist(self, visualization_manager):
        """Test that all expected methods exist."""
        assert hasattr(visualization_manager, '__init__')
        assert hasattr(visualization_manager, 'run_visualization_analysis')
        assert callable(visualization_manager.__init__)
        assert callable(visualization_manager.run_visualization_analysis)
    
    def test_manager_interface_consistency(self, visualization_manager):
        """Test that the manager interface is consistent."""
        # Test that the manager can be instantiated multiple times
        manager1 = VisualizationManager()
        manager2 = VisualizationManager()
        
        assert isinstance(manager1, VisualizationManager)
        assert isinstance(manager2, VisualizationManager)
        assert manager1 is not manager2  # Different instances
    
    def test_manager_with_different_system_types(self):
        """Test manager with different system types."""
        from src.interactive import InteractiveSystem
        
        system = InteractiveSystem()
        visualization_manager = VisualizationManager()
        
        with patch.object(system, 'safe_input'):
            with patch('builtins.input', return_value='0'):
                visualization_manager.run_visualization_analysis(system)
    
    def test_manager_output_format(self):
        """Test manager output format."""
        from src.interactive import InteractiveSystem
        
        system = InteractiveSystem()
        visualization_manager = VisualizationManager()
        
        with patch.object(system, 'safe_input'):
            with patch('builtins.input', return_value='0'):
                visualization_manager.run_visualization_analysis(system)
