# -*- coding: utf-8 -*-
# tests/plotting/test_term_navigation.py

"""
Tests for terminal navigation system.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from plotting.term_navigation import (
    TerminalNavigator, 
    create_navigation_prompt, 
    parse_navigation_input, 
    validate_date_input
)


class TestTerminalNavigation:
    """Test cases for terminal navigation system."""

    def setup_method(self):
        """Set up test data."""
        # Create sample data
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        data = {
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 102,
            'Low': np.random.randn(100).cumsum() + 98,
            'Close': np.random.randn(100).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 100)
        }
        self.df = pd.DataFrame(data, index=dates)
        
        # Split into chunks
        chunk_size = 20
        self.chunks = []
        for i in range(0, len(self.df), chunk_size):
            self.chunks.append(self.df.iloc[i:i+chunk_size])

    def test_terminal_navigator_initialization(self):
        """Test TerminalNavigator initialization."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        
        assert navigator.chunks == self.chunks
        assert navigator.title == "Test Navigation"
        assert navigator.current_chunk_index == 0
        assert navigator.total_chunks == len(self.chunks)
        assert navigator.navigation_active is True

    def test_get_current_chunk(self):
        """Test getting current chunk."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        current_chunk = navigator.get_current_chunk()
        
        assert current_chunk.equals(self.chunks[0])

    def test_get_current_chunk_info(self):
        """Test getting current chunk information."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        info = navigator.get_current_chunk_info()
        
        assert info['index'] == 1
        assert info['total'] == len(self.chunks)
        assert info['rows'] == len(self.chunks[0])
        assert 'start_date' in info
        assert 'end_date' in info

    def test_next_chunk(self):
        """Test navigating to next chunk."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        
        # Move to next chunk
        result = navigator._next_chunk()
        assert result is True
        assert navigator.current_chunk_index == 1
        
        # Move to last chunk
        navigator.current_chunk_index = navigator.total_chunks - 1
        result = navigator._next_chunk()
        assert result is False  # Already at last chunk

    def test_previous_chunk(self):
        """Test navigating to previous chunk."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        
        # Move to next chunk first
        navigator.current_chunk_index = 1
        
        # Move back
        result = navigator._previous_chunk()
        assert result is True
        assert navigator.current_chunk_index == 0
        
        # Try to go back from first chunk
        result = navigator._previous_chunk()
        assert result is False  # Already at first chunk

    def test_start_chunk(self):
        """Test navigating to start chunk."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        navigator.current_chunk_index = 2
        
        result = navigator._start_chunk()
        assert result is True
        assert navigator.current_chunk_index == 0

    def test_end_chunk(self):
        """Test navigating to end chunk."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        
        result = navigator._end_chunk()
        assert result is True
        assert navigator.current_chunk_index == navigator.total_chunks - 1

    def test_quit_navigation(self):
        """Test quitting navigation."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        
        result = navigator._quit_navigation()
        assert result is True
        assert navigator.navigation_active is False

    @patch('builtins.input')
    def test_choose_chunk_valid(self, mock_input):
        """Test choosing chunk with valid input."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        mock_input.return_value = "3"
        
        result = navigator._choose_chunk()
        assert result is True
        assert navigator.current_chunk_index == 2  # 0-based index

    @patch('builtins.input')
    def test_choose_chunk_invalid(self, mock_input):
        """Test choosing chunk with invalid input."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        mock_input.return_value = "invalid"
        
        result = navigator._choose_chunk()
        assert result is False

    @patch('builtins.input')
    def test_choose_chunk_out_of_range(self, mock_input):
        """Test choosing chunk with out of range input."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        mock_input.return_value = "999"
        
        result = navigator._choose_chunk()
        assert result is False

    @patch('builtins.input')
    def test_choose_date_valid(self, mock_input):
        """Test choosing chunk by date with valid input."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        mock_input.return_value = "2024-01-15"
        
        result = navigator._choose_date()
        assert result is True

    @patch('builtins.input')
    def test_choose_date_invalid(self, mock_input):
        """Test choosing chunk by date with invalid input."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        mock_input.return_value = "invalid-date"
        
        result = navigator._choose_date()
        assert result is False

    def test_process_navigation_input_empty(self):
        """Test processing empty navigation input."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        
        result = navigator.process_navigation_input("")
        assert result is True  # Should move to next chunk

    def test_process_navigation_input_next(self):
        """Test processing 'n' command."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        
        result = navigator.process_navigation_input("n")
        assert result is True
        assert navigator.current_chunk_index == 1

    def test_process_navigation_input_previous(self):
        """Test processing 'p' command."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        navigator.current_chunk_index = 1
        
        result = navigator.process_navigation_input("p")
        assert result is True
        assert navigator.current_chunk_index == 0

    def test_process_navigation_input_unknown(self):
        """Test processing unknown command."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        
        result = navigator.process_navigation_input("x")
        assert result is False

    def test_process_navigation_input_previous_at_start(self):
        """Test processing 'p' command when already at start - should continue navigation."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        # Already at start (index 0)
        
        result = navigator.process_navigation_input("p")
        assert result is True  # Should continue navigation even if command fails
        assert navigator.current_chunk_index == 0  # Should stay at start

    def test_process_navigation_input_next_at_end(self):
        """Test processing 'n' command when already at end - should continue navigation."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        navigator.current_chunk_index = navigator.total_chunks - 1  # At end
        
        result = navigator.process_navigation_input("n")
        assert result is True  # Should continue navigation even if command fails
        assert navigator.current_chunk_index == navigator.total_chunks - 1  # Should stay at end

    def test_process_navigation_input_help(self):
        """Test processing 'h' command - should continue navigation."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        
        result = navigator.process_navigation_input("h")
        assert result is True  # Should continue navigation after showing help

    def test_process_navigation_input_quit(self):
        """Test processing 'q' command - should quit navigation."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        
        result = navigator.process_navigation_input("q")
        assert result is True  # Should continue navigation (quit is handled in navigate loop)
        assert navigator.navigation_active is False  # But navigation should be deactivated

    def test_create_navigation_prompt(self):
        """Test creating navigation prompt."""
        prompt = create_navigation_prompt(2, 5, "2024-01-01", "2024-01-20")
        
        assert "Navigation: type" in prompt
        assert "n/p/s/e/c/d/h/q" in prompt
        assert "Chunk 2/5" in prompt
        assert "2024-01-01 to 2024-01-20" in prompt

    def test_parse_navigation_input_empty(self):
        """Test parsing empty input."""
        result = parse_navigation_input("")
        assert result['command'] == 'next'
        assert result['valid'] is True

    def test_parse_navigation_input_valid_commands(self):
        """Test parsing valid commands."""
        commands = ['n', 'p', 's', 'e', 'h', 'q', '?']
        
        for cmd in commands:
            result = parse_navigation_input(cmd)
            assert result['command'] == cmd
            assert result['valid'] is True

    def test_parse_navigation_input_invalid(self):
        """Test parsing invalid input."""
        result = parse_navigation_input("x")
        assert result['valid'] is False
        assert 'error' in result

    def test_validate_date_input_valid_formats(self):
        """Test validating date input with valid formats."""
        valid_dates = [
            "2024-01-01",
            "2024-01-01 12:00",
            "2024-01-01 12:00:45"
        ]
        
        for date_str in valid_dates:
            result = validate_date_input(date_str)
            assert result is not None
            assert isinstance(result, datetime)

    def test_validate_date_input_invalid(self):
        """Test validating date input with invalid format."""
        result = validate_date_input("invalid-date")
        assert result is None

    @patch('builtins.input')
    def test_navigate_with_plot_function(self, mock_input):
        """Test navigation with plot function."""
        navigator = TerminalNavigator(self.chunks, "Test Navigation")
        mock_input.return_value = "q"  # Quit after first chunk
        
        plot_calls = []
        
        def mock_plot_function(chunk, chunk_index, chunk_info):
            plot_calls.append((chunk_index, chunk_info))
        
        navigator.navigate(mock_plot_function)
        
        assert len(plot_calls) == 1
        assert plot_calls[0][0] == 0  # First chunk index

    def test_navigation_with_empty_chunks(self):
        """Test navigation with empty chunks."""
        empty_chunks = [pd.DataFrame(), pd.DataFrame()]
        navigator = TerminalNavigator(empty_chunks, "Test Navigation")
        
        info = navigator.get_current_chunk_info()
        assert info['rows'] == 0
        assert info['start_date'] == 'N/A'
        assert info['end_date'] == 'N/A'


if __name__ == "__main__":
    pytest.main([__file__]) 