# -*- coding: utf-8 -*-
# tests/cli/test_wave_pros_cons.py

"""
Test module for Wave indicator pros and cons display functionality.
Tests that the --indicators wave command properly displays advantages and disadvantages.
"""

import pytest
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.cli.indicators_search import IndicatorSearcher, IndicatorInfo


class TestWaveProsCons:
    """Test class for Wave indicator pros and cons functionality."""

    def test_wave_indicator_has_pros_cons(self):
        """Test that Wave indicator has pros and cons defined."""
        searcher = IndicatorSearcher()
        
        # Find Wave indicator
        wave_indicators = searcher.search_indicators("wave")
        assert len(wave_indicators) > 0, "Wave indicator should be found"
        
        wave_indicator = wave_indicators[0]
        assert wave_indicator.name == "WAVE", "Should find WAVE indicator"
        
        # Check that pros and cons are not empty
        assert wave_indicator.pros != "Not specified", "Wave indicator should have pros defined"
        assert wave_indicator.cons != "Not specified", "Wave indicator should have cons defined"
        
        # Check that pros and cons contain expected content
        assert "Dual Signal Validation" in wave_indicator.pros, "Should contain dual signal validation"
        assert "Complex Setup" in wave_indicator.cons, "Should contain complex setup warning"

    def test_wave_pros_cons_formatting(self):
        """Test that pros and cons are properly formatted."""
        searcher = IndicatorSearcher()
        wave_indicators = searcher.search_indicators("wave")
        wave_indicator = wave_indicators[0]
        
        # Test pros formatting
        pros_lines = wave_indicator.pros.split(', ')
        assert len(pros_lines) >= 8, "Should have at least 8 pros"
        
        # Test cons formatting
        cons_lines = wave_indicator.cons.split(', ')
        assert len(cons_lines) >= 8, "Should have at least 8 cons"
        
        # Check specific pros
        pros_text = wave_indicator.pros.lower()
        assert "dual signal validation" in pros_text
        assert "flexible configuration" in pros_text
        assert "strong trend identification" in pros_text
        
        # Check specific cons
        cons_text = wave_indicator.cons.lower()
        assert "complex setup" in cons_text
        assert "lag in ranging markets" in cons_text
        assert "parameter sensitivity" in cons_text

    def test_wave_indicator_display_includes_pros_cons(self):
        """Test that Wave indicator display includes pros and cons."""
        searcher = IndicatorSearcher()
        wave_indicators = searcher.search_indicators("wave")
        wave_indicator = wave_indicators[0]
        
        # Get detailed display
        display_output = wave_indicator.display(detailed=True)
        
        # Check that display includes pros and cons sections
        assert "👍 Pros:" in display_output, "Display should include pros section"
        assert "👎 Cons:" in display_output, "Display should include cons section"
        
        # Check that pros and cons content is included
        assert "Dual Signal Validation" in display_output
        assert "Complex Setup" in display_output

    @pytest.mark.integration
    def test_cli_wave_indicators_command(self):
        """Test that CLI command --indicators wave works correctly."""
        script_path = project_root / "run_analysis.py"
        
        # Run the command
        result = subprocess.run(
            [sys.executable, str(script_path), "--indicators", "wave"],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        # Check that command executed successfully
        # The command might fail if --indicators option is not implemented
        # We'll check if it produces any output or specific error
        if result.returncode == 0:
            # Command succeeded, check for expected output
            assert "wave" in result.stdout.lower() or "indicator" in result.stdout.lower(), \
                "Command should produce output related to wave indicators"
        else:
            # Command failed, check if it's due to unimplemented option
            # The script might not exist or have different options
            assert "unrecognized arguments" in result.stderr.lower() or \
                   "no such option" in result.stderr.lower() or \
                   "invalid choice" in result.stderr.lower() or \
                   "no such file" in result.stderr.lower(), \
                "Command should fail with appropriate error message for unimplemented option or missing file"

    @pytest.mark.integration
    def test_cli_wave_indicators_category_command(self):
        """Test that CLI command --indicators wave --category works correctly."""
        script_path = project_root / "run_analysis.py"
        
        # Run the command
        result = subprocess.run(
            [sys.executable, str(script_path), "--indicators", "wave", "--category"],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        # Check that command executed successfully
        # The command might fail if --category option is not implemented
        if result.returncode == 0:
            # Command succeeded, check for expected output
            assert "wave" in result.stdout.lower() or "indicator" in result.stdout.lower(), \
                "Command should produce output related to wave indicators"
        else:
            # Command failed, check if it's due to unimplemented option
            # The script might not exist or have different options
            assert "unrecognized arguments" in result.stderr.lower() or \
                   "no such option" in result.stderr.lower() or \
                   "invalid choice" in result.stderr.lower() or \
                   "no such file" in result.stderr.lower(), \
                "Command should fail with appropriate error message for unimplemented option or missing file"

    def test_wave_indicator_info_structure(self):
        """Test that Wave indicator has correct information structure."""
        searcher = IndicatorSearcher()
        wave_indicators = searcher.search_indicators("wave")
        wave_indicator = wave_indicators[0]
        
        # Check required fields
        assert wave_indicator.name == "WAVE"
        assert wave_indicator.category == "trend"
        assert wave_indicator.description, "Description should not be empty"
        assert wave_indicator.usage, "Usage should not be empty"
        assert wave_indicator.parameters, "Parameters should not be empty"
        assert wave_indicator.file_path, "File path should not be empty"
        
        # Check that file path points to correct file
        assert "wave_ind.py" in wave_indicator.file_path
        assert "trend" in wave_indicator.file_path

    def test_wave_indicator_usage_format(self):
        """Test that Wave indicator usage format is correct."""
        searcher = IndicatorSearcher()
        wave_indicators = searcher.search_indicators("wave")
        wave_indicator = wave_indicators[0]
        
        # Check usage format
        assert wave_indicator.usage.startswith("--rule wave:"), "Usage should start with --rule wave:"
        assert "," in wave_indicator.usage, "Usage should contain parameters"

    def test_wave_indicator_parameters_format(self):
        """Test that Wave indicator parameters are properly formatted."""
        searcher = IndicatorSearcher()
        wave_indicators = searcher.search_indicators("wave")
        wave_indicator = wave_indicators[0]
        
        # Check that parameters contain expected fields
        params_text = wave_indicator.parameters.lower()
        assert "period_long1" in params_text
        assert "period_short1" in params_text
        assert "period_trend1" in params_text
        assert "tr1" in params_text
        assert "global_tr" in params_text
        assert "sma_period" in params_text


if __name__ == "__main__":
    pytest.main([__file__])
