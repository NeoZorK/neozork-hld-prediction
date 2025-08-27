# -*- coding: utf-8 -*-
"""
Tests for visualization manager module.

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
        system.safe_input = Mock(return_value=None)
        return system
    
    def test_init(self, visualization_manager):
        """Test VisualizationManager initialization."""
        assert visualization_manager is not None
    
    def test_run_visualization_analysis(self, visualization_manager, mock_system, capsys):
        """Test run_visualization_analysis method."""
        visualization_manager.run_visualization_analysis(mock_system)
        captured = capsys.readouterr()
        assert "DATA VISUALIZATION" in captured.out
        assert "Visualization features coming soon!" in captured.out
        mock_system.safe_input.assert_called_once()
    
    def test_create_statistics_plots_no_data(self, visualization_manager, mock_system):
        """Test create_statistics_plots with no data."""
        mock_system.current_data = None
        result = visualization_manager.create_statistics_plots(mock_system)
        assert result is False
    
    def test_create_statistics_plots_empty_data(self, visualization_manager, mock_system):
        """Test create_statistics_plots with empty data."""
        mock_system.current_data = pd.DataFrame()
        result = visualization_manager.create_statistics_plots(mock_system)
        assert result is False
    
    @patch('matplotlib.pyplot')
    @patch('seaborn.set_palette')
    @patch('seaborn.histplot')
    @patch('seaborn.boxplot')
    @patch('seaborn.heatmap')
    @patch('pathlib.Path.mkdir')
    def test_create_statistics_plots_success(self, mock_mkdir, mock_heatmap, mock_boxplot, mock_histplot, mock_set_palette, mock_plt, visualization_manager, mock_system):
        """Test create_statistics_plots with successful execution."""
        # Mock matplotlib and seaborn
        mock_plt.subplots.return_value = (Mock(), np.array([[Mock(), Mock()], [Mock(), Mock()]]))
        mock_plt.figure.return_value = Mock()
        mock_plt.savefig.return_value = None
        mock_plt.close.return_value = None
        mock_plt.tight_layout.return_value = None
        
        # Mock seaborn
        mock_histplot.return_value = None
        mock_boxplot.return_value = None
        mock_heatmap.return_value = None
        mock_set_palette.return_value = None
        
        result = visualization_manager.create_statistics_plots(mock_system)
        assert result is True
        mock_mkdir.assert_called()
    
    @patch('matplotlib.pyplot')
    @patch('seaborn.set_palette')
    @patch('seaborn.histplot')
    @patch('seaborn.boxplot')
    @patch('seaborn.heatmap')
    @patch('pathlib.Path.mkdir')
    def test_create_statistics_plots_with_data_parameter(self, mock_mkdir, mock_heatmap, mock_boxplot, mock_histplot, mock_set_palette, mock_plt, visualization_manager, mock_system):
        """Test create_statistics_plots with data parameter."""
        # Mock matplotlib and seaborn
        mock_plt.subplots.return_value = (Mock(), np.array([[Mock(), Mock()], [Mock(), Mock()]]))
        mock_plt.figure.return_value = Mock()
        mock_plt.savefig.return_value = None
        mock_plt.close.return_value = None
        mock_plt.tight_layout.return_value = None
        
        # Mock seaborn
        mock_histplot.return_value = None
        mock_boxplot.return_value = None
        mock_heatmap.return_value = None
        mock_set_palette.return_value = None
        
        test_data = pd.DataFrame({
            'col1': [1, 2, 3, 4, 5],
            'col2': [6, 7, 8, 9, 10]
        })
        
        result = visualization_manager.create_statistics_plots(mock_system, test_data)
        assert result is True
    
    @patch('matplotlib.pyplot')
    @patch('seaborn.set_palette')
    @patch('seaborn.histplot')
    @patch('seaborn.boxplot')
    @patch('seaborn.heatmap')
    @patch('pathlib.Path.mkdir')
    def test_create_statistics_plots_single_column(self, mock_mkdir, mock_heatmap, mock_boxplot, mock_histplot, mock_set_palette, mock_plt, visualization_manager, mock_system):
        """Test create_statistics_plots with single column data."""
        # Mock matplotlib and seaborn
        mock_plt.subplots.return_value = (Mock(), np.array([[Mock(), Mock()], [Mock(), Mock()]]))
        mock_plt.figure.return_value = Mock()
        mock_plt.savefig.return_value = None
        mock_plt.close.return_value = None
        mock_plt.tight_layout.return_value = None
        
        # Mock seaborn
        mock_histplot.return_value = None
        mock_boxplot.return_value = None
        mock_heatmap.return_value = None
        mock_set_palette.return_value = None
        
        single_column_data = pd.DataFrame({'col1': [1, 2, 3, 4, 5]})
        
        result = visualization_manager.create_statistics_plots(mock_system, single_column_data)
        assert result is True
    
    @patch('matplotlib.pyplot')
    @patch('seaborn.set_palette')
    @patch('seaborn.histplot')
    @patch('seaborn.boxplot')
    @patch('seaborn.heatmap')
    @patch('pathlib.Path.mkdir')
    def test_create_statistics_plots_exception(self, mock_mkdir, mock_heatmap, mock_boxplot, mock_histplot, mock_set_palette, mock_plt, visualization_manager, mock_system):
        """Test create_statistics_plots with exception."""
        mock_mkdir.side_effect = Exception("Test error")
        
        result = visualization_manager.create_statistics_plots(mock_system)
        assert result is False
    
    def test_show_plots_in_browser_no_plots_dir(self, visualization_manager, mock_system):
        """Test show_plots_in_browser with no plots directory."""
        with patch('pathlib.Path.exists', return_value=False):
            result = visualization_manager.show_plots_in_browser(mock_system)
            assert result is False
    
    @patch('webbrowser.open')
    @patch('builtins.open', create=True)
    @patch('pathlib.Path.exists', return_value=True)
    def test_show_plots_in_browser_success(self, mock_exists, mock_open, mock_webbrowser, visualization_manager, mock_system):
        """Test show_plots_in_browser with successful execution."""
        # Mock plot files
        mock_plot_files = [
            Mock(name='distributions.png'),
            Mock(name='boxplots.png'),
            Mock(name='correlation_heatmap.png'),
            Mock(name='statistical_summary.png')
        ]
        
        with patch('pathlib.Path.glob', return_value=mock_plot_files):
            with patch('pathlib.Path.iterdir', return_value=mock_plot_files):
                result = visualization_manager.show_plots_in_browser(mock_system)
                assert result is True
                mock_webbrowser.open.assert_called_once()
    
    @patch('webbrowser.open')
    @patch('builtins.open', create=True)
    @patch('pathlib.Path.exists', return_value=True)
    def test_show_plots_in_browser_some_plots_missing(self, mock_exists, mock_open, mock_webbrowser, visualization_manager, mock_system):
        """Test show_plots_in_browser with some plot files missing."""
        # Mock only some plot files
        mock_plot_files = [
            Mock(name='distributions.png'),
            Mock(name='boxplots.png')
        ]
        
        with patch('pathlib.Path.glob', return_value=mock_plot_files):
            with patch('pathlib.Path.iterdir', return_value=mock_plot_files):
                result = visualization_manager.show_plots_in_browser(mock_system)
                assert result is True
                mock_webbrowser.open.assert_called_once()
    
    @patch('webbrowser.open')
    @patch('builtins.open', create=True)
    @patch('pathlib.Path.exists', return_value=True)
    def test_show_plots_in_browser_exception(self, mock_exists, mock_open, mock_webbrowser, visualization_manager, mock_system):
        """Test show_plots_in_browser with exception."""
        mock_webbrowser.open.side_effect = Exception("Test error")
        
        mock_plot_files = [Mock(name='distributions.png')]
        with patch('pathlib.Path.glob', return_value=mock_plot_files):
            with patch('pathlib.Path.iterdir', return_value=mock_plot_files):
                result = visualization_manager.show_plots_in_browser(mock_system)
                assert result is False
    
    @patch('webbrowser.open')
    @patch('builtins.open', create=True)
    @patch('pathlib.Path.exists', return_value=True)
    def test_show_plots_in_browser_file_write_exception(self, mock_exists, mock_open, mock_webbrowser, visualization_manager, mock_system):
        """Test show_plots_in_browser with file write exception."""
        mock_open.side_effect = Exception("Test error")
        
        mock_plot_files = [Mock(name='distributions.png')]
        with patch('pathlib.Path.glob', return_value=mock_plot_files):
            with patch('pathlib.Path.iterdir', return_value=mock_plot_files):
                result = visualization_manager.show_plots_in_browser(mock_system)
                assert result is False
