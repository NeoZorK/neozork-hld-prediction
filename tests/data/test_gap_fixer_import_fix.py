#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test GapFixer import fix.

This test verifies that the import issues in GapFixer have been resolved.
"""

import pytest
import pandas as pd
from pathlib import Path


class TestGapFixerImportFix:
    """Test that GapFixer imports and initializes correctly."""
    
    def test_gap_fixer_import(self):
        """Test that GapFixer can be imported from src.data."""
        try:
            from src.data import GapFixer
            assert GapFixer is not None
        except ImportError as e:
            pytest.fail(f"Failed to import GapFixer: {e}")
    
    def test_gap_fixer_initialization(self):
        """Test that GapFixer can be initialized."""
        try:
            from src.data import GapFixer
            gap_fixer = GapFixer(memory_limit_mb=1024)
            assert gap_fixer is not None
            assert hasattr(gap_fixer, 'memory_limit_mb')
            assert gap_fixer.memory_limit_mb == 1024
        except Exception as e:
            pytest.fail(f"Failed to initialize GapFixer: {e}")
    
    def test_gap_fixer_components(self):
        """Test that GapFixer has all required components."""
        try:
            from src.data import GapFixer
            gap_fixer = GapFixer()
            
            # Check that algorithms module is available
            assert hasattr(gap_fixer, 'algorithms')
            assert gap_fixer.algorithms is not None
            
            # Check that utils module is available
            assert hasattr(gap_fixer, 'utils')
            assert gap_fixer.utils is not None
            
        except Exception as e:
            pytest.fail(f"Failed to access GapFixer components: {e}")
    
    def test_gap_fixer_from_gap_fixing_package(self):
        """Test that GapFixer can be imported directly from gap_fixing package."""
        try:
            from src.data.gap_fixing import GapFixer
            gap_fixer = GapFixer()
            assert gap_fixer is not None
        except ImportError as e:
            pytest.fail(f"Failed to import GapFixer from gap_fixing package: {e}")
    
    def test_gap_fixer_utils_import(self):
        """Test that GapFixingUtils can be imported."""
        try:
            from src.data.gap_fixing import GapFixingUtils
            utils = GapFixingUtils()
            assert utils is not None
        except ImportError as e:
            pytest.fail(f"Failed to import GapFixingUtils: {e}")
    
    def test_gap_fixer_strategy_import(self):
        """Test that GapFixingStrategy can be imported."""
        try:
            from src.data.gap_fixing import GapFixingStrategy
            strategy = GapFixingStrategy()
            assert strategy is not None
        except ImportError as e:
            pytest.fail(f"Failed to import GapFixingStrategy: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
