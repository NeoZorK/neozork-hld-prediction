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
        visualization_manager.run_visualization_analysis(mock_system)
        
        # Check output
        captured = capsys.readouterr()
        assert "DATA VISUALIZATION" in captured.out
        assert "Visualization features coming soon!" in captured.out
        assert "interactive charts, plots, and export capabilities" in captured.out
        
        # Check that safe_input was called
        mock_system.safe_input.assert_called_once()
    
    def test_run_visualization_analysis_with_real_system(self, visualization_manager, capsys):
        """Test run_visualization_analysis with a real system-like object."""
        # Create a simple object with safe_input method
        class SimpleSystem:
            def safe_input(self):
                pass
        
        system = SimpleSystem()
        
        with patch.object(system, 'safe_input') as mock_input:
            visualization_manager.run_visualization_analysis(system)
            
            # Check output
            captured = capsys.readouterr()
            assert "DATA VISUALIZATION" in captured.out
            assert "Visualization features coming soon!" in captured.out
            
            # Check that safe_input was called
            mock_input.assert_called_once()
    
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
    
    def test_manager_with_different_system_types(self, visualization_manager):
        """Test that the manager works with different system types."""
        # Test with Mock
        mock_system = Mock()
        mock_system.safe_input = Mock()
        
        with patch.object(mock_system, 'safe_input') as mock_input:
            visualization_manager.run_visualization_analysis(mock_system)
            mock_input.assert_called_once()
        
        # Test with simple object
        class SimpleSystem:
            def safe_input(self):
                pass
        
        simple_system = SimpleSystem()
        
        with patch.object(simple_system, 'safe_input') as mock_input:
            visualization_manager.run_visualization_analysis(simple_system)
            mock_input.assert_called_once()
    
    def test_manager_output_format(self, visualization_manager, capsys):
        """Test that the manager produces expected output format."""
        mock_system = Mock()
        mock_system.safe_input = Mock()
        
        visualization_manager.run_visualization_analysis(mock_system)
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Check for expected sections
        assert "📊 DATA VISUALIZATION" in output
        assert "-" * 30 in output
        assert "⏳ Visualization features coming soon!" in output
        assert "interactive charts, plots, and export capabilities" in output
        
        # Check that output is properly formatted
        lines = output.strip().split('\n')
        assert len(lines) >= 4  # At least 4 lines of output
        assert any("📊 DATA VISUALIZATION" in line for line in lines)
        assert any("⏳ Visualization features coming soon!" in line for line in lines)
