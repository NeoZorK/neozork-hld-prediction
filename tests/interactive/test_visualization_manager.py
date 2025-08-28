# -*- coding: utf-8 -*-
# tests/interactive/test_visualization_manager.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from src.interactive.visualization_manager import VisualizationManager


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'predicted_high': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
        'predicted_low': [95, 96, 97, 98, 99, 100, 101, 102, 103, 104],
        'pressure': [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4],
        'pressure_vector': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
        'High': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
        'Close': [100.5, 101.5, 102.5, 103.5, 104.5, 105.5, 106.5, 107.5, 108.5, 109.5],
        'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
    })


@pytest.fixture
def mock_system():
    """Create a mock system for testing."""
    system = Mock()
    system.current_data = None
    system.current_results = {}
    return system


@pytest.fixture
def visualization_manager():
    """Create a VisualizationManager instance."""
    return VisualizationManager()


class TestVisualizationManager:
    
    def test_init(self, visualization_manager):
        """Test VisualizationManager initialization."""
        assert visualization_manager is not None
    
    def test_run_visualization_analysis(self, visualization_manager, mock_system):
        """Test run_visualization_analysis."""
        with patch('builtins.input', return_value='0'):
            visualization_manager.run_visualization_analysis(mock_system)
    
    def test_create_statistics_plots_no_data(self, visualization_manager, mock_system):
        """Test create_statistics_plots with no data."""
        result = visualization_manager.create_statistics_plots(mock_system)
        assert result is False
    
    def test_create_statistics_plots_empty_data(self, visualization_manager, mock_system):
        """Test create_statistics_plots with empty data."""
        mock_system.current_data = pd.DataFrame()
        result = visualization_manager.create_statistics_plots(mock_system)
        assert result is False
    
    def test_create_statistics_plots_success(self, visualization_manager, mock_system, sample_data):
        """Test create_statistics_plots with valid data."""
        mock_system.current_data = sample_data
        
        with patch('pathlib.Path.mkdir'):
            with patch('builtins.open', create=True):
                with patch('tqdm.tqdm') as mock_tqdm:
                    mock_tqdm.return_value.__enter__ = Mock(return_value=mock_tqdm.return_value)
                    mock_tqdm.return_value.__exit__ = Mock(return_value=None)
                    
                    result = visualization_manager.create_statistics_plots(mock_system)
                    assert result is True
    
    def test_create_statistics_plots_with_data_parameter(self, visualization_manager, mock_system, sample_data):
        """Test create_statistics_plots with data parameter."""
        with patch('pathlib.Path.mkdir'):
            with patch('builtins.open', create=True):
                with patch('tqdm.tqdm') as mock_tqdm:
                    mock_tqdm.return_value.__enter__ = Mock(return_value=mock_tqdm.return_value)
                    mock_tqdm.return_value.__exit__ = Mock(return_value=None)
                    
                    result = visualization_manager.create_statistics_plots(mock_system, sample_data)
                    assert result is True
    
    def test_create_statistics_plots_single_column(self, visualization_manager, mock_system):
        """Test create_statistics_plots with single column data."""
        single_column_data = pd.DataFrame({'col1': [1, 2, 3, 4, 5]})
        
        with patch('pathlib.Path.mkdir'):
            with patch('builtins.open', create=True):
                with patch('tqdm.tqdm') as mock_tqdm:
                    mock_tqdm.return_value.__enter__ = Mock(return_value=mock_tqdm.return_value)
                    mock_tqdm.return_value.__exit__ = Mock(return_value=None)
                    
                    result = visualization_manager.create_statistics_plots(mock_system, single_column_data)
                    assert result is True
    
    def test_create_statistics_plots_exception(self, visualization_manager, mock_system, sample_data):
        """Test create_statistics_plots with exception."""
        mock_system.current_data = sample_data
        
        with patch('pathlib.Path.mkdir', side_effect=Exception("Test error")):
            result = visualization_manager.create_statistics_plots(mock_system)
            assert result is False
    
    def test_show_plots_in_browser_no_plots_dir(self, visualization_manager, mock_system):
        """Test show_plots_in_browser with no plots directory."""
        with patch('pathlib.Path.exists', return_value=False):
            result = visualization_manager.show_plots_in_browser(mock_system)
            assert result is False
    
    def test_show_plots_in_browser_success(self, visualization_manager, mock_system):
        """Test show_plots_in_browser with successful execution."""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('webbrowser.get') as mock_get:
                with patch('webbrowser.open') as mock_open:
                    mock_get.return_value.open = Mock()
                    
                    result = visualization_manager.show_plots_in_browser(mock_system)
                    assert result is True
    
    def test_show_plots_in_browser_some_plots_missing(self, visualization_manager, mock_system):
        """Test show_plots_in_browser with some plot files missing."""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('webbrowser.get', side_effect=Exception("Safari not found")):
                with patch('webbrowser.open') as mock_open:
                    result = visualization_manager.show_plots_in_browser(mock_system)
                    assert result is True
    
    def test_show_plots_in_browser_exception(self, visualization_manager, mock_system):
        """Test show_plots_in_browser with exception."""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('webbrowser.get', side_effect=Exception("Safari not found")):
                with patch('webbrowser.open', side_effect=Exception("Test error")):
                    result = visualization_manager.show_plots_in_browser(mock_system)
                    assert result is False
    
    def test_show_plots_in_browser_file_write_exception(self, visualization_manager, mock_system):
        """Test show_plots_in_browser with file write exception."""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', side_effect=Exception("Test error")):
                result = visualization_manager.show_plots_in_browser(mock_system)
                assert result is True  # Method returns True even with file write errors due to fallback
    
    # New tests for improved functionality
    def test_calculate_field_statistics(self, visualization_manager, sample_data):
        """Test _calculate_field_statistics method."""
        field_data = sample_data['predicted_high']
        stats = visualization_manager._calculate_field_statistics(field_data)
        
        assert 'basic' in stats
        assert 'distribution' in stats
        assert 'outliers' in stats
        
        assert stats['basic']['count'] == 10
        assert stats['basic']['mean'] == pytest.approx(104.5, rel=1e-10)
        assert stats['distribution']['skewness'] is not None
        assert stats['outliers']['iqr']['count'] >= 0
    
    def test_detect_outliers(self, visualization_manager, sample_data):
        """Test _detect_outliers method."""
        field_data = sample_data['predicted_high']
        outliers = visualization_manager._detect_outliers(field_data)
        
        assert 'iqr' in outliers
        assert 'zscore' in outliers
        assert outliers['iqr']['count'] >= 0
        assert outliers['zscore']['count'] >= 0
    
    def test_create_field_plots(self, visualization_manager, sample_data):
        """Test _create_field_plots method."""
        field_data = sample_data['predicted_high']
        plots = visualization_manager._create_field_plots(field_data, 'test_field')
        
        assert isinstance(plots, dict)
        assert 'distribution' in plots
        assert 'boxplot' in plots
        assert 'qqplot' in plots
    
    def test_simple_kde(self, visualization_manager, sample_data):
        """Test _simple_kde method."""
        field_data = sample_data['predicted_high']
        x_range = np.linspace(field_data.min(), field_data.max(), 100)
        
        kde_values = visualization_manager._simple_kde(field_data, x_range)
        assert len(kde_values) == len(x_range)
        assert all(np.isfinite(kde_values))
    
    def test_generate_interpretations(self, visualization_manager, sample_data):
        """Test _generate_interpretations method."""
        field_data = sample_data['predicted_high']
        stats = visualization_manager._calculate_field_statistics(field_data)
        
        interpretations = visualization_manager._generate_interpretations(stats)
        assert isinstance(interpretations, str)
        assert len(interpretations) > 0
    
    def test_create_field_html_report(self, visualization_manager, sample_data):
        """Test _create_field_html_report method."""
        with patch('builtins.open', create=True):
            # Use an existing field name from sample_data
            field_name = sample_data.columns[0]  # Use first column
            visualization_manager._create_field_html_report(sample_data, field_name, Path('/tmp'))
    
    def test_create_summary_html_report(self, visualization_manager, sample_data):
        """Test _create_summary_html_report method."""
        with patch('builtins.open', create=True):
            visualization_manager._create_summary_html_report(sample_data, Path('/tmp'))
    
    def test_generate_field_html_content(self, visualization_manager, sample_data):
        """Test _generate_field_html_content method."""
        field_data = sample_data['predicted_high']
        stats = visualization_manager._calculate_field_statistics(field_data)
        plots = visualization_manager._create_field_plots(field_data, 'test_field')
        
        html_content = visualization_manager._generate_field_html_content('test_field', stats, plots)
        assert isinstance(html_content, str)
        assert 'test_field' in html_content
        assert 'Basic Statistics' in html_content
        assert 'Distribution Analysis' in html_content
    
    def test_create_statistics_plots_progress_bar(self, visualization_manager, mock_system, sample_data):
        """Test create_statistics_plots with progress bar."""
        mock_system.current_data = sample_data
        
        with patch('pathlib.Path.mkdir'):
            with patch('builtins.open', create=True):
                with patch('src.interactive.visualization_manager.tqdm') as mock_tqdm:
                    mock_tqdm.return_value.__enter__ = Mock(return_value=mock_tqdm.return_value)
                    mock_tqdm.return_value.__exit__ = Mock(return_value=None)
                    mock_tqdm.return_value.update = Mock()
                    
                    result = visualization_manager.create_statistics_plots(mock_system)
                    
                    assert result is True
                    # Check that tqdm was called (progress bar was used)
                    assert mock_tqdm.called
    
    def test_create_statistics_plots_field_error_handling(self, visualization_manager, mock_system, sample_data):
        """Test create_statistics_plots with field error handling."""
        mock_system.current_data = sample_data
        
        with patch('pathlib.Path.mkdir'):
            with patch('builtins.open', create=True):
                with patch('src.interactive.visualization_manager.tqdm') as mock_tqdm:
                    with patch.object(visualization_manager, '_create_field_html_report', side_effect=Exception("Field error")):
                        mock_tqdm.return_value.__enter__ = Mock(return_value=mock_tqdm.return_value)
                        mock_tqdm.return_value.__exit__ = Mock(return_value=None)
                        mock_tqdm.return_value.write = Mock()
                        
                        result = visualization_manager.create_statistics_plots(mock_system)
                        assert result is True  # Should continue despite field errors
    
    def test_create_statistics_plots_all_fields(self, visualization_manager, mock_system, sample_data):
        """Test create_statistics_plots creates reports for all fields."""
        mock_system.current_data = sample_data
        
        with patch('pathlib.Path.mkdir'):
            with patch('builtins.open', create=True):
                with patch('src.interactive.visualization_manager.tqdm') as mock_tqdm:
                    mock_tqdm.return_value.__enter__ = Mock(return_value=mock_tqdm.return_value)
                    mock_tqdm.return_value.__exit__ = Mock(return_value=None)
                    mock_tqdm.return_value.update = Mock()
                    
                    result = visualization_manager.create_statistics_plots(mock_system)
                    
                    assert result is True
                    # Should process all numeric columns
                    expected_calls = len(sample_data.select_dtypes(include=['number']).columns)
                    # Check that update was called for each field
                    assert mock_tqdm.return_value.update.call_count == expected_calls
    
    def test_plotly_integration(self, visualization_manager, sample_data):
        """Test Plotly integration in field plots."""
        field_data = sample_data['predicted_high']
        plots = visualization_manager._create_field_plots(field_data, 'test_field')
        
        # Check that plots contain Plotly HTML
        for plot_type, plot_html in plots.items():
            assert isinstance(plot_html, str)
            assert 'plotly' in plot_html.lower() or 'div' in plot_html.lower()
    
    def test_html_content_structure(self, visualization_manager, sample_data):
        """Test HTML content structure."""
        field_data = sample_data['predicted_high']
        stats = visualization_manager._calculate_field_statistics(field_data)
        plots = visualization_manager._create_field_plots(field_data, 'test_field')
        
        html_content = visualization_manager._generate_field_html_content('test_field', stats, plots)
        
        # Check for required HTML elements
        assert '<!DOCTYPE html>' in html_content
        assert '<html>' in html_content
        assert '<head>' in html_content
        assert '<body>' in html_content
        assert 'test_field' in html_content
        assert 'Basic Statistics' in html_content
        assert 'Distribution Properties' in html_content
        assert 'Outlier Analysis' in html_content
