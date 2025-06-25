import pytest
from unittest.mock import MagicMock, patch
from src.cli.interactive_mode import InteractiveMode, start_interactive_mode


@patch('src.cli.interactive_mode.IndicatorSearcher')
class TestInteractiveModeSimple:
    """Simple tests for InteractiveMode that don't hang."""
    
    def test_init(self, mock_searcher_class):
        """Test InteractiveMode initialization."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators', 'momentum']
        mock_searcher_class.return_value = mock_searcher
        
        interactive = InteractiveMode()
        
        assert interactive.current_selection['mode'] is None
        assert interactive.current_selection['indicator'] is None
        assert interactive.current_selection['interval'] == 'D1'
        assert interactive.current_selection['draw_method'] == 'fastest'
        assert interactive.current_selection['export_formats'] == []
        assert interactive.categories == ['oscillators', 'momentum']
        assert interactive.searcher == mock_searcher
    
    def test_print_welcome(self, mock_searcher_class, capsys):
        """Test welcome message printing."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators']
        mock_searcher_class.return_value = mock_searcher
        
        interactive = InteractiveMode()
        interactive._print_welcome()
        
        captured = capsys.readouterr()
        assert "Interactive Mode" in captured.out
        assert "Welcome" in captured.out
    
    def test_show_main_menu(self, mock_searcher_class, capsys):
        """Test main menu display."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators']
        mock_searcher_class.return_value = mock_searcher
        
        interactive = InteractiveMode()
        interactive._show_main_menu()
        
        captured = capsys.readouterr()
        assert "Main Menu" in captured.out
        assert "Select Analysis Mode" in captured.out
        assert "Exit" in captured.out
    
    @patch('builtins.input')
    def test_get_user_choice(self, mock_input, mock_searcher_class):
        """Test getting user choice."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators']
        mock_searcher_class.return_value = mock_searcher
        
        mock_input.return_value = "5"
        interactive = InteractiveMode()
        
        result = interactive._get_user_choice()
        
        assert result == "5"
        mock_input.assert_called_once()
    
    @patch('builtins.input')
    def test_select_mode_valid(self, mock_input, mock_searcher_class, capsys):
        """Test mode selection with valid input."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators']
        mock_searcher_class.return_value = mock_searcher
        
        mock_input.return_value = "1"
        interactive = InteractiveMode()
        
        interactive._select_mode()
        
        captured = capsys.readouterr()
        assert "Select Analysis Mode" in captured.out
        assert "Selected mode: demo" in captured.out
        assert interactive.current_selection['mode'] == 'demo'
    
    @patch('builtins.input')
    def test_select_mode_invalid(self, mock_input, mock_searcher_class, capsys):
        """Test mode selection with invalid input."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators']
        mock_searcher_class.return_value = mock_searcher
        
        mock_input.return_value = "999"
        interactive = InteractiveMode()
        
        interactive._select_mode()
        
        captured = capsys.readouterr()
        assert "Invalid choice" in captured.out
        assert interactive.current_selection['mode'] is None
    
    def test_configure_data_source_no_mode(self, mock_searcher_class, capsys):
        """Test data source configuration without mode."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators']
        mock_searcher_class.return_value = mock_searcher
        
        interactive = InteractiveMode()
        
        interactive._configure_data_source()
        
        captured = capsys.readouterr()
        assert "Please select a mode first" in captured.out
    
    @patch('builtins.input')
    def test_configure_csv_source(self, mock_input, mock_searcher_class):
        """Test CSV source configuration."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators']
        mock_searcher_class.return_value = mock_searcher
        
        mock_input.side_effect = ["test.csv", "0.01"]
        interactive = InteractiveMode()
        interactive.current_selection['mode'] = 'csv'
        
        interactive._configure_csv_source()
        
        assert interactive.current_selection['data_source'] == 'test.csv'
        assert interactive.current_selection['point'] == 0.01
    
    @patch('builtins.input')
    def test_configure_plotting(self, mock_input, mock_searcher_class, capsys):
        """Test plotting configuration."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators']
        mock_searcher_class.return_value = mock_searcher
        
        mock_input.return_value = "1"
        interactive = InteractiveMode()
        
        interactive._configure_plotting()
        
        captured = capsys.readouterr()
        assert "Configure Plotting" in captured.out
        assert interactive.current_selection['draw_method'] == 'fastest'
    
    @patch('builtins.input')
    def test_configure_export(self, mock_input, mock_searcher_class):
        """Test export configuration."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators']
        mock_searcher_class.return_value = mock_searcher
        
        mock_input.side_effect = ["y", "n", "n", "n"]
        interactive = InteractiveMode()
        
        interactive._configure_export()
        
        assert 'parquet' in interactive.current_selection['export_formats']
        assert 'csv' not in interactive.current_selection['export_formats']
    
    def test_show_current_configuration(self, mock_searcher_class, capsys):
        """Test current configuration display."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators']
        mock_searcher_class.return_value = mock_searcher
        
        interactive = InteractiveMode()
        interactive.current_selection['mode'] = 'demo'
        interactive.current_selection['draw_method'] = 'fastest'
        
        interactive._show_current_configuration()
        
        captured = capsys.readouterr()
        assert "Current Configuration" in captured.out
        assert "mode: demo" in captured.out
        assert "draw_method: fastest" in captured.out
    
    def test_run_analysis_no_mode(self, mock_searcher_class, capsys):
        """Test running analysis without mode selected."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators']
        mock_searcher_class.return_value = mock_searcher
        
        interactive = InteractiveMode()
        
        interactive._run_analysis()
        
        captured = capsys.readouterr()
        assert "Please select a mode first" in captured.out
    
    def test_run_analysis_no_indicator(self, mock_searcher_class, capsys):
        """Test running analysis without indicator selected."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators']
        mock_searcher_class.return_value = mock_searcher
        
        interactive = InteractiveMode()
        interactive.current_selection['mode'] = 'demo'
        
        interactive._run_analysis()
        
        captured = capsys.readouterr()
        assert "Please select an indicator first" in captured.out
    
    @patch('builtins.input')
    def test_run_analysis_command_building(self, mock_input, mock_searcher_class, capsys):
        """Test command building without actually running analysis."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators']
        mock_searcher_class.return_value = mock_searcher
        
        mock_input.return_value = "n"  # Don't run analysis
        interactive = InteractiveMode()
        interactive.current_selection['mode'] = 'demo'
        
        mock_indicator = MagicMock()
        mock_indicator.name = "RSI"
        interactive.current_selection['indicator'] = mock_indicator
        
        interactive._run_analysis()
        
        captured = capsys.readouterr()
        assert "Running Analysis" in captured.out
        assert "Command: python run_analysis.py demo --rule RSI" in captured.out
        assert "Analysis cancelled" in captured.out
    
    def test_show_help(self, mock_searcher_class, capsys):
        """Test help display."""
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators']
        mock_searcher_class.return_value = mock_searcher
        
        interactive = InteractiveMode()
        
        interactive._show_help()
        
        captured = capsys.readouterr()
        assert "Interactive Mode Help" in captured.out
        assert "Select Analysis Mode" in captured.out
    
    def test_list_indicators(self, mock_searcher_class, capsys):
        """Test indicators listing with detailed information."""
        # Create mock indicators
        mock_indicator1 = MagicMock()
        mock_indicator1.name = "RSI"
        mock_indicator1.description = "Relative Strength Index"
        
        mock_indicator2 = MagicMock()
        mock_indicator2.name = "MACD"
        mock_indicator2.description = "Moving Average Convergence Divergence"
        
        mock_searcher = MagicMock()
        mock_searcher.list_categories.return_value = ['oscillators', 'momentum']
        mock_searcher.list_indicators.side_effect = lambda cat: {
            'oscillators': [mock_indicator1],
            'momentum': [mock_indicator2]
        }.get(cat, [])
        mock_searcher._get_category_emoji.return_value = "📊"
        mock_searcher_class.return_value = mock_searcher
        
        interactive = InteractiveMode()
        
        interactive._list_indicators()
        
        captured = capsys.readouterr()
        assert "Available Indicators" in captured.out
        assert "Available Indicator Categories" in captured.out
        assert "Detailed Indicator List" in captured.out
        assert "oscillators" in captured.out
        assert "momentum" in captured.out
        assert "RSI" in captured.out
        assert "MACD" in captured.out
        assert "Relative Strength Index" in captured.out
        assert "Moving Average Convergence Divergence" in captured.out
        assert "Tip: Use option 2" in captured.out


@patch('src.cli.interactive_mode.InteractiveMode')
def test_start_interactive_mode(mock_interactive_class):
    """Test start_interactive_mode function."""
    mock_interactive = MagicMock()
    mock_interactive_class.return_value = mock_interactive
    
    start_interactive_mode()
    
    mock_interactive_class.assert_called_once()
    mock_interactive.start.assert_called_once() 