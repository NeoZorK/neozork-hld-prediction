#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test module for plot display fixes.

This module tests that plots remain open when using -d mpl and -d sb flags.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.plotting.plot_utils import smart_plot_display, file_based_plot_display


class TestPlotDisplayFix:
    """Test class for plot display fixes."""
    
    def test_file_based_plot_display_success(self):
        """Test that file_based_plot_display works correctly."""
        with patch('os.path.exists', return_value=True):
            with patch('tempfile.NamedTemporaryFile') as mock_temp:
                mock_temp.return_value.__enter__.return_value.name = '/tmp/test.png'
                with patch('matplotlib.pyplot.savefig') as mock_save:
                    with patch('subprocess.run') as mock_run:
                        with patch('platform.system', return_value='Darwin'):
                            file_based_plot_display()
                            mock_save.assert_called_once()
                            mock_run.assert_called_once()
    
    def test_file_based_plot_display_auto_close(self):
        """Test that file_based_plot_display works with auto_close."""
        with patch('os.path.exists', return_value=True):
            with patch('tempfile.NamedTemporaryFile') as mock_temp:
                mock_temp.return_value.__enter__.return_value.name = '/tmp/test.png'
                with patch('matplotlib.pyplot.savefig') as mock_save:
                    with patch('subprocess.run') as mock_run:
                        with patch('platform.system', return_value='Darwin'):
                            with patch('time.sleep') as mock_sleep:
                                with patch('os.unlink') as mock_unlink:
                                    file_based_plot_display(auto_close=True, pause_time=5.0)
                                    mock_save.assert_called_once()
                                    mock_run.assert_called_once()
                                    mock_sleep.assert_called_once_with(5.0)
                                    mock_unlink.assert_called_once()
    
    def test_file_based_plot_display_linux(self):
        """Test that file_based_plot_display works on Linux."""
        with patch('os.path.exists', return_value=True):
            with patch('tempfile.NamedTemporaryFile') as mock_temp:
                mock_temp.return_value.__enter__.return_value.name = '/tmp/test.png'
                with patch('matplotlib.pyplot.savefig') as mock_save:
                    with patch('subprocess.run') as mock_run:
                        with patch('platform.system', return_value='Linux'):
                            file_based_plot_display()
                            mock_save.assert_called_once()
                            mock_run.assert_called_once()
    
    def test_file_based_plot_display_windows(self):
        """Test that file_based_plot_display works on Windows."""
        with patch('os.path.exists', return_value=True):
            with patch('tempfile.NamedTemporaryFile') as mock_temp:
                mock_temp.return_value.__enter__.return_value.name = '/tmp/test.png'
                with patch('matplotlib.pyplot.savefig') as mock_save:
                    with patch('subprocess.run') as mock_run:
                        with patch('platform.system', return_value='Windows'):
                            file_based_plot_display()
                            mock_save.assert_called_once()
                            mock_run.assert_called_once()
    
    def test_file_based_plot_display_fallback(self):
        """Test that file_based_plot_display falls back to interactive display on error."""
        with patch('os.path.exists', return_value=True):
            with patch('tempfile.NamedTemporaryFile', side_effect=Exception("Test error")):
                with patch('matplotlib.use') as mock_use:
                    with patch('matplotlib.pyplot.ion') as mock_ion:
                        with patch('matplotlib.pyplot.show') as mock_show:
                            file_based_plot_display()
                            mock_use.assert_called_with('TkAgg')
                            mock_ion.assert_called_once()
                            mock_show.assert_called_once_with(block=True)
    
    def test_smart_plot_display_blocking_mode(self):
        """Test that smart_plot_display works in blocking mode."""
        with patch('src.plotting.plot_utils.setup_interactive_backend') as mock_setup:
            with patch('src.plotting.plot_utils.should_show_plot', return_value=True):
                with patch('src.plotting.plot_utils.open_latest_plot_file') as mock_open_file:
                    smart_plot_display(block=True)
                    mock_setup.assert_called_once()
                    mock_open_file.assert_called_once_with("plot")
    
    def test_smart_plot_display_non_blocking_mode(self):
        """Test that smart_plot_display works in non-blocking mode."""
        with patch('src.plotting.plot_utils.setup_interactive_backend') as mock_setup:
            with patch('src.plotting.plot_utils.should_show_plot', return_value=True):
                with patch('src.plotting.plot_utils.open_latest_plot_file') as mock_open_file:
                    with patch('time.sleep') as mock_sleep:
                        smart_plot_display(block=False, pause_time=5.0)
                        mock_setup.assert_called_once()
                        mock_open_file.assert_called_once_with("plot")
                        mock_sleep.assert_called_once_with(5.0)
    
    def test_smart_plot_display_no_show(self):
        """Test that smart_plot_display handles no show case."""
        with patch('src.plotting.plot_utils.setup_interactive_backend') as mock_setup:
            with patch('src.plotting.plot_utils.should_show_plot', return_value=False):
                with patch('matplotlib.pyplot.close') as mock_close:
                    smart_plot_display(show_plot=False)
                    mock_setup.assert_called_once()
                    mock_close.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
