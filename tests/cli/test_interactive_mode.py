# -*- coding: utf-8 -*-
# tests/cli/test_interactive_mode.py

"""
Unit tests for interactive mode functionality.
Tests the interactive mode class and its methods.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock, call
from io import StringIO
from src.cli.interactive_mode import InteractiveMode, start_interactive_mode


class TestInteractiveMode:
    """Test cases for InteractiveMode class."""
    
    def test_init(self):
        """Test InteractiveMode initialization."""
        interactive = InteractiveMode()
        
        assert interactive.searcher is not None
        assert interactive.categories is not None
        assert isinstance(interactive.current_selection, dict)
        assert interactive.current_selection['mode'] is None
        assert interactive.current_selection['indicator'] is None
        assert interactive.current_selection['draw_method'] == 'fastest'
        assert interactive.current_selection['export_formats'] == []
    
    def test_print_welcome(self, capsys):
        """Test welcome message printing."""
        interactive = InteractiveMode()
        interactive._print_welcome()
        
        captured = capsys.readouterr()
        assert "Interactive Mode" in captured.out
        assert "Welcome" in captured.out
    
    def test_show_main_menu(self, capsys):
        """Test main menu display."""
        interactive = InteractiveMode()
        interactive._show_main_menu()
        
        captured = capsys.readouterr()
        assert "Main Menu" in captured.out
        assert "Select Analysis Mode" in captured.out
        assert "Select Indicator" in captured.out
        assert "Exit" in captured.out
    
    @patch('builtins.input')
    def test_get_user_choice(self, mock_input):
        """Test getting user choice."""
        mock_input.return_value = "5"
        interactive = InteractiveMode()
        
        result = interactive._get_user_choice()
        
        assert result == "5"
        mock_input.assert_called_once()
    
    @patch('builtins.input')
    def test_select_mode_valid(self, mock_input, capsys):
        """Test mode selection with valid input."""
        mock_input.return_value = "1"
        interactive = InteractiveMode()
        
        interactive._select_mode()
        
        captured = capsys.readouterr()
        assert "Select Analysis Mode" in captured.out
        assert interactive.current_selection['mode'] == 'demo'
        assert "Selected mode: demo" in captured.out
    
    @patch('builtins.input')
    def test_select_mode_invalid(self, mock_input, capsys):
        """Test mode selection with invalid input."""
        mock_input.return_value = "invalid"
        interactive = InteractiveMode()
        
        interactive._select_mode()
        
        captured = capsys.readouterr()
        assert "Please enter a valid number" in captured.out
        assert interactive.current_selection['mode'] is None
    
    @patch('builtins.input')
    def test_select_indicator_valid(self, mock_input, capsys):
        """Test indicator selection with valid input."""
        mock_input.side_effect = ["1", "1"]  # Select first category, then first indicator
        interactive = InteractiveMode()
        
        # Mock the searcher to return known data
        mock_indicator = MagicMock()
        mock_indicator.name = "Test RSI"
        mock_indicator.description = "Test RSI indicator"
        mock_indicator.category = "oscillators"
        
        interactive.searcher.list_categories = MagicMock(return_value=["oscillators"])
        interactive.searcher.list_indicators = MagicMock(return_value=[mock_indicator])
        
        interactive._select_indicator()
        
        captured = capsys.readouterr()
        assert "Select Indicator" in captured.out
        assert interactive.current_selection['indicator'] == mock_indicator
        assert "Selected indicator: Test RSI" in captured.out
    
    @patch('builtins.input')
    def test_select_indicator_invalid_category(self, mock_input, capsys):
        """Test indicator selection with invalid category."""
        mock_input.return_value = "999"
        interactive = InteractiveMode()
        
        interactive.searcher.list_categories = MagicMock(return_value=["oscillators"])
        
        interactive._select_indicator()
        
        captured = capsys.readouterr()
        assert "Invalid choice" in captured.out
        assert interactive.current_selection['indicator'] is None
    
    def test_configure_data_source_no_mode(self, capsys):
        """Test data source configuration without mode selected."""
        interactive = InteractiveMode()
        
        interactive._configure_data_source()
        
        captured = capsys.readouterr()
        assert "Please select a mode first" in captured.out
    
    @patch('builtins.input')
    def test_configure_csv_source(self, mock_input):
        """Test CSV source configuration."""
        mock_input.side_effect = ["test.csv", "0.01"]
        interactive = InteractiveMode()
        interactive.current_selection['mode'] = 'csv'
        
        interactive._configure_csv_source()
        
        assert interactive.current_selection['data_source'] == "test.csv"
        assert interactive.current_selection['point'] == 0.01
    
    @patch('builtins.input')
    def test_configure_csv_source_invalid_point(self, mock_input, capsys):
        """Test CSV source configuration with invalid point size."""
        mock_input.side_effect = ["test.csv", "invalid"]
        interactive = InteractiveMode()
        interactive.current_selection['mode'] = 'csv'
        
        interactive._configure_csv_source()
        
        captured = capsys.readouterr()
        assert "Invalid point size" in captured.out
        assert interactive.current_selection['point'] is None
    
    @patch('builtins.input')
    def test_configure_api_source(self, mock_input):
        """Test API source configuration."""
        mock_input.side_effect = ["AAPL", "D1", "0.01", "n", "2023-01-01", "2023-12-31"]
        interactive = InteractiveMode()
        interactive.current_selection['mode'] = 'yfinance'
        
        interactive._configure_api_source()
        
        assert interactive.current_selection['ticker'] == "AAPL"
        assert interactive.current_selection['interval'] == "D1"
        assert interactive.current_selection['point'] == 0.01
        assert interactive.current_selection['start_date'] == "2023-01-01"
        assert interactive.current_selection['end_date'] == "2023-12-31"
    
    @patch('builtins.input')
    def test_configure_api_source_with_period(self, mock_input):
        """Test API source configuration with period."""
        mock_input.side_effect = ["AAPL", "D1", "0.01", "y", "1mo"]
        interactive = InteractiveMode()
        interactive.current_selection['mode'] = 'yfinance'
        
        interactive._configure_api_source()
        
        assert interactive.current_selection['ticker'] == "AAPL"
        assert interactive.current_selection['period'] == "1mo"
    
    @patch('builtins.input')
    def test_configure_plotting(self, mock_input, capsys):
        """Test plotting configuration."""
        mock_input.return_value = "3"  # Select plotly
        interactive = InteractiveMode()
        
        interactive._configure_plotting()
        
        captured = capsys.readouterr()
        assert "Configure Plotting" in captured.out
        assert interactive.current_selection['draw_method'] == "plotly"
        assert "Selected method: plotly" in captured.out
    
    @patch('builtins.input')
    def test_configure_export(self, mock_input, capsys):
        """Test export configuration."""
        mock_input.side_effect = ["y", "n", "y", "n"]  # parquet: yes, csv: no, json: yes, indicators_info: no
        interactive = InteractiveMode()
        
        interactive._configure_export()
        
        captured = capsys.readouterr()
        assert "Configure Export" in captured.out
        assert "parquet" in interactive.current_selection['export_formats']
        assert "json" in interactive.current_selection['export_formats']
        assert "csv" not in interactive.current_selection['export_formats']
        assert "indicators_info" not in interactive.current_selection['export_formats']
    
    def test_show_current_configuration(self, capsys):
        """Test current configuration display."""
        interactive = InteractiveMode()
        interactive.current_selection['mode'] = 'demo'
        interactive.current_selection['draw_method'] = 'fastest'
        interactive.current_selection['export_formats'] = ['parquet']
        
        interactive._show_current_configuration()
        
        captured = capsys.readouterr()
        assert "Current Configuration" in captured.out
        assert "mode: demo" in captured.out
        assert "draw_method: fastest" in captured.out
        assert "export_formats: parquet" in captured.out
    
    def test_show_current_configuration_with_indicator(self, capsys):
        """Test current configuration display with indicator."""
        interactive = InteractiveMode()
        mock_indicator = MagicMock()
        mock_indicator.name = "Test RSI"
        mock_indicator.category = "oscillators"
        interactive.current_selection['indicator'] = mock_indicator
        
        interactive._show_current_configuration()
        
        captured = capsys.readouterr()
        assert "indicator: Test RSI (oscillators)" in captured.out
    
    def test_run_analysis_no_mode(self, capsys):
        """Test running analysis without mode selected."""
        interactive = InteractiveMode()
        
        interactive._run_analysis()
        
        captured = capsys.readouterr()
        assert "Please select a mode first" in captured.out
    
    def test_run_analysis_no_indicator(self, capsys):
        """Test running analysis without indicator selected."""
        interactive = InteractiveMode()
        interactive.current_selection['mode'] = 'demo'
        
        interactive._run_analysis()
        
        captured = capsys.readouterr()
        assert "Please select an indicator first" in captured.out
    
    @patch('builtins.input')
    @patch('src.cli.interactive_mode.main')
    def test_run_analysis_success(self, mock_main, mock_input, capsys):
        """Test successful analysis execution."""
        mock_input.return_value = "y"
        interactive = InteractiveMode()
        interactive.current_selection['mode'] = 'demo'
        
        mock_indicator = MagicMock()
        mock_indicator.name = "RSI"
        interactive.current_selection['indicator'] = mock_indicator
        
        interactive._run_analysis()
        
        captured = capsys.readouterr()
        assert "Running Analysis" in captured.out
        assert "Command: python run_analysis.py demo --rule RSI" in captured.out
        assert "Analysis completed successfully" in captured.out
        mock_main.assert_called_once()
    
    @patch('builtins.input')
    def test_run_analysis_cancelled(self, mock_input, capsys):
        """Test cancelled analysis execution."""
        mock_input.return_value = "n"
        interactive = InteractiveMode()
        interactive.current_selection['mode'] = 'demo'
        
        mock_indicator = MagicMock()
        mock_indicator.name = "RSI"
        interactive.current_selection['indicator'] = mock_indicator
        
        interactive._run_analysis()
        
        captured = capsys.readouterr()
        assert "Analysis cancelled" in captured.out
    
    @patch('builtins.input')
    @patch('src.cli.interactive_mode.main')
    def test_run_analysis_error(self, mock_main, mock_input, capsys):
        """Test analysis execution with error."""
        mock_input.return_value = "y"
        mock_main.side_effect = Exception("Test error")
        interactive = InteractiveMode()
        interactive.current_selection['mode'] = 'demo'
        
        mock_indicator = MagicMock()
        mock_indicator.name = "RSI"
        interactive.current_selection['indicator'] = mock_indicator
        
        interactive._run_analysis()
        
        captured = capsys.readouterr()
        assert "Error running analysis: Test error" in captured.out
    
    def test_show_help(self, capsys):
        """Test help display."""
        interactive = InteractiveMode()
        interactive._show_help()
        
        captured = capsys.readouterr()
        assert "Interactive Mode Help" in captured.out
        assert "Select Analysis Mode" in captured.out
        assert "python run_analysis.py --help" in captured.out
    
    def test_list_indicators(self, capsys):
        """Test indicator listing."""
        interactive = InteractiveMode()
        interactive._list_indicators()
        
        captured = capsys.readouterr()
        assert "Available Indicators" in captured.out


class TestInteractiveModeIntegration:
    """Integration tests for InteractiveMode."""
    
    @patch('builtins.input')
    def test_full_workflow_demo_rsi(self, mock_input, capsys):
        """Test full workflow for demo mode with RSI."""
        # Simulate user input for full workflow
        mock_input.side_effect = [
            "1",  # Select mode
            "1",  # Select demo mode
            "2",  # Select indicator
            "1",  # Select first category
            "1",  # Select first indicator
            "4",  # Configure plotting
            "1",  # Select fastest plotting
            "5",  # Configure export
            "y",  # Export parquet
            "n",  # Export CSV
            "n",  # Export JSON
            "n",  # Export indicators_info
            "6",  # Show configuration
            "0",  # Exit
        ]
        
        interactive = InteractiveMode()
        
        # Mock searcher
        mock_indicator = MagicMock()
        mock_indicator.name = "RSI"
        mock_indicator.description = "Relative Strength Index"
        mock_indicator.category = "oscillators"
        
        interactive.searcher.list_categories = MagicMock(return_value=["oscillators"])
        interactive.searcher.list_indicators = MagicMock(return_value=[mock_indicator])
        
        interactive.start()
        
        captured = capsys.readouterr()
        assert "Welcome" in captured.out
        assert "Selected mode: demo" in captured.out
        assert "Selected indicator: RSI" in captured.out
        assert "Selected method: fastest" in captured.out
        assert "parquet" in interactive.current_selection['export_formats']
        assert "Goodbye" in captured.out


@patch('src.cli.interactive_mode.InteractiveMode')
def test_start_interactive_mode(mock_interactive_class):
    """Test start_interactive_mode function."""
    mock_interactive = MagicMock()
    mock_interactive_class.return_value = mock_interactive
    
    start_interactive_mode()
    
    mock_interactive_class.assert_called_once()
    mock_interactive.start.assert_called_once()


class TestInteractiveModeErrorHandling:
    """Test error handling in InteractiveMode."""
    
    @patch('builtins.input')
    def test_keyboard_interrupt(self, mock_input, capsys):
        """Test handling of KeyboardInterrupt."""
        mock_input.side_effect = KeyboardInterrupt()
        interactive = InteractiveMode()
        
        interactive.start()
        
        captured = capsys.readouterr()
        assert "Interactive mode interrupted" in captured.out
    
    @patch('builtins.input')
    def test_general_exception(self, mock_input, capsys):
        """Test handling of general exceptions."""
        mock_input.side_effect = Exception("Test exception")
        interactive = InteractiveMode()
        
        interactive.start()
        
        captured = capsys.readouterr()
        assert "Error: Test exception" in captured.out
    
    @patch('builtins.input')
    def test_invalid_menu_choice(self, mock_input, capsys):
        """Test handling of invalid menu choices."""
        mock_input.side_effect = ["999", "0"]  # Invalid choice, then exit
        interactive = InteractiveMode()
        
        interactive.start()
        
        captured = capsys.readouterr()
        assert "Invalid choice" in captured.out
        assert "Goodbye" in captured.out


class TestInteractiveModeDataValidation:
    """Test data validation in InteractiveMode."""
    
    def test_point_size_validation_positive(self):
        """Test positive point size validation."""
        interactive = InteractiveMode()
        
        # Test valid point sizes
        assert interactive._validate_point_size("0.01") == 0.01
        assert interactive._validate_point_size("0.00001") == 0.00001
        assert interactive._validate_point_size("1.0") == 1.0
    
    def test_point_size_validation_invalid(self):
        """Test invalid point size validation."""
        interactive = InteractiveMode()
        
        # Test invalid point sizes
        assert interactive._validate_point_size("invalid") is None
        assert interactive._validate_point_size("0") is None
        assert interactive._validate_point_size("-0.01") is None
    
    def test_date_validation_valid(self):
        """Test valid date validation."""
        interactive = InteractiveMode()
        
        # Test valid dates
        assert interactive._validate_date("2023-01-01") == "2023-01-01"
        assert interactive._validate_date("2024-12-31") == "2024-12-31"
    
    def test_date_validation_invalid(self):
        """Test invalid date validation."""
        interactive = InteractiveMode()
        
        # Test invalid dates
        assert interactive._validate_date("invalid") is None
        assert interactive._validate_date("2023-13-01") is None
        assert interactive._validate_date("2023-00-01") is None 