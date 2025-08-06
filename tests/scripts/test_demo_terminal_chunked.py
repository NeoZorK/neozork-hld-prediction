#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for demo_terminal_chunked.py after moving to scripts/demos/ folder.
"""

import os
import sys
import pytest
from pathlib import Path


class TestDemoTerminalChunked:
    """Test class for demo_terminal_chunked.py functionality."""
    
    def test_file_exists_in_correct_location(self):
        """Test that the file exists in the correct location."""
        # Check that file exists in demos folder
        demos_path = Path("scripts/demos/demo_terminal_chunked.py")
        assert demos_path.exists(), f"File should exist at {demos_path}"
        
        # Check that file no longer exists in root scripts folder
        old_path = Path("scripts/demo_terminal_chunked.py")
        assert not old_path.exists(), f"File should not exist at {old_path}"
    
    def test_file_has_correct_header(self):
        """Test that the file has the correct header comment."""
        demos_path = Path("scripts/demos/demo_terminal_chunked.py")
        
        with open(demos_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check that the header comment reflects the new location
        assert "# scripts/demos/demo_terminal_chunked.py" in content, \
            "File should have updated header comment"
        
        # Check that old header comment is not present
        assert "# scripts/demo_terminal_chunked.py" not in content, \
            "File should not have old header comment"
    
    def test_file_syntax_is_valid(self):
        """Test that the file has valid Python syntax."""
        demos_path = Path("scripts/demos/demo_terminal_chunked.py")
        
        # This will raise SyntaxError if the file has syntax issues
        with open(demos_path, 'r', encoding='utf-8') as f:
            compile(f.read(), str(demos_path), 'exec')
    
    def test_file_imports_are_correct(self):
        """Test that the file has correct import structure."""
        demos_path = Path("scripts/demos/demo_terminal_chunked.py")
        
        with open(demos_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check that the path adjustment for src import is correct
        expected_path_adjustment = "sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))"
        assert expected_path_adjustment in content, \
            "File should have correct path adjustment for src import"
    
    def test_documentation_references_updated(self):
        """Test that documentation files have been updated."""
        # Check TERMINAL_PLOTTING_UPDATES_SUMMARY.md
        summary_path = Path("docs/development/TERMINAL_PLOTTING_UPDATES_SUMMARY.md")
        if summary_path.exists():
            with open(summary_path, 'r', encoding='utf-8') as f:
                content = f.read()
            assert "scripts/demos/demo_terminal_chunked.py" in content, \
                "Documentation should reference new location"
            assert "scripts/demo_terminal_chunked.py" not in content, \
                "Documentation should not reference old location"
        
        # Check TERMINAL_CHUNKED_PLOTTING_SUMMARY.md
        chunked_summary_path = Path("docs/development/TERMINAL_CHUNKED_PLOTTING_SUMMARY.md")
        if chunked_summary_path.exists():
            with open(chunked_summary_path, 'r', encoding='utf-8') as f:
                content = f.read()
            assert "python scripts/demos/demo_terminal_chunked.py" in content, \
                "Documentation should reference new location"
            assert "python scripts/demo_terminal_chunked.py" not in content, \
                "Documentation should not reference old location"


if __name__ == "__main__":
    pytest.main([__file__]) 