"""
Test file to verify that the draw flag fix works correctly.
This test ensures that the error "Error calculating indicator: 'Namespace' object has no attribute 'draw'" is resolved.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.cli.cli import parse_arguments


class TestDrawFlagFix:
    """Test class to verify draw flag functionality."""
    
    def test_draw_flag_short_form(self):
        """Test that -d flag works and sets args.draw correctly."""
        with patch('sys.argv', ['run_analysis.py', 'demo', '-d', 'fastest']):
            args = parse_arguments()
            assert hasattr(args, 'draw')
            assert args.draw == 'fastest'
    
    def test_draw_flag_long_form(self):
        """Test that --draw flag works and sets args.draw correctly."""
        with patch('sys.argv', ['run_analysis.py', 'demo', '--draw', 'term']):
            args = parse_arguments()
            assert hasattr(args, 'draw')
            assert args.draw == 'term'
    
    def test_draw_flag_default_value(self):
        """Test that draw flag has correct default value."""
        with patch('sys.argv', ['run_analysis.py', 'demo']):
            args = parse_arguments()
            assert hasattr(args, 'draw')
            assert args.draw == 'fastest'
    
    def test_draw_flag_all_modes(self):
        """Test that all draw modes are accepted."""
        draw_modes = ['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl', 'seaborn', 'sb', 'term']
        
        for mode in draw_modes:
            with patch('sys.argv', ['run_analysis.py', 'demo', '-d', mode]):
                args = parse_arguments()
                assert hasattr(args, 'draw')
                assert args.draw == mode
    
    def test_draw_flag_invalid_mode(self):
        """Test that invalid draw mode raises appropriate error."""
        with patch('sys.argv', ['run_analysis.py', 'demo', '-d', 'invalid_mode']):
            with pytest.raises(SystemExit):
                parse_arguments()
    
    def test_draw_flag_with_other_args(self):
        """Test that draw flag works with other arguments."""
        with patch('sys.argv', ['run_analysis.py', 'demo', '--rule', 'OHLCV', '-d', 'plotly']):
            args = parse_arguments()
            assert hasattr(args, 'draw')
            assert args.draw == 'plotly'
            assert args.rule == 'OHLCV'
    
    def test_draw_flag_show_mode(self):
        """Test that draw flag works in show mode."""
        with patch('sys.argv', ['run_analysis.py', 'show', '-d', 'term']):
            args = parse_arguments()
            assert hasattr(args, 'draw')
            assert args.draw == 'term'
            assert args.mode == 'show'


if __name__ == '__main__':
    pytest.main([__file__, '-v']) 