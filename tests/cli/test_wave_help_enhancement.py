# -*- coding: utf-8 -*-
# tests/cli/test_wave_help_enhancement.py

"""
Test enhanced help functionality for Wave indicator with ENUM_MOM_TR and ENUM_GLOBAL_TR information.
"""

import pytest
import subprocess
import sys
from pathlib import Path

# Get project root
project_root = Path(__file__).parent.parent.parent


class TestWaveHelpEnhancement:
    """Test enhanced help functionality for Wave indicator."""

    @pytest.mark.integration
    def test_wave_indicators_command_with_enum_info(self):
        """Test that CLI command --indicators wave shows ENUM_MOM_TR and ENUM_GLOBAL_TR information."""
        script_path = project_root / "run_analysis.py"
        
        # Run the command
        result = subprocess.run(
            [sys.executable, str(script_path), "--indicators", "wave"],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        # Check that command executed successfully
        assert result.returncode == 0, f"Command failed with return code {result.returncode}"
        
        # Check that output contains expected content
        output = result.stdout
        assert "WAVE" in output, "Output should contain WAVE indicator name"
        assert "🎯 Trading Rules (ENUM_MOM_TR):" in output, "Output should show Trading Rules section"
        assert "🌐 Global Trading Rules (ENUM_GLOBAL_TR):" in output, "Output should show Global Trading Rules section"
        
        # Check for specific trading rules
        assert "fast: Basic momentum comparison" in output, "Should show fast trading rule"
        assert "zone: Simple zone-based signals" in output, "Should show zone trading rule"
        assert "strongtrend: Strong trend confirmation" in output, "Should show strongtrend trading rule"
        assert "weaktrend: Weak trend signals" in output, "Should show weaktrend trading rule"
        assert "fastzonereverse: Reverse signals in zones" in output, "Should show fastzonereverse trading rule"
        assert "bettertrend: Enhanced trend signals" in output, "Should show bettertrend trading rule"
        assert "betterfast: Improved fast trading" in output, "Should show betterfast trading rule"
        assert "rost: Reverse momentum signals" in output, "Should show rost trading rule"
        assert "trendrost: Trend-based reverse signals" in output, "Should show trendrost trading rule"
        assert "bettertrendrost: Enhanced trend reverse signals" in output, "Should show bettertrendrost trading rule"
        
        # Check for specific global rules
        assert "prime: Prime rule" in output, "Should show prime global rule"
        assert "reverse: Reverse rule" in output, "Should show reverse global rule"
        assert "primezone: Prime Zone rule" in output, "Should show primezone global rule"
        assert "reversezone: Reverse Zone rule" in output, "Should show reversezone global rule"
        assert "newzone: New Zone rule" in output, "Should show newzone global rule"
        assert "longzone: Long Zone rule" in output, "Should show longzone global rule"
        assert "longzonereverse: Long Zone Reverse rule" in output, "Should show longzonereverse global rule"

    @pytest.mark.integration
    def test_wave_error_help_with_enum_info(self):
        """Test that error help for wave indicator shows ENUM_MOM_TR and ENUM_GLOBAL_TR information."""
        script_path = project_root / "run_analysis.py"
        
        # Run the command with invalid parameters to trigger help
        result = subprocess.run(
            [sys.executable, str(script_path), "show", "csv", "mn1", "-d", "fastest", "--rule", "wave:invalid"],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        # Check that command executed (may fail due to invalid parameters, but should show help)
        output = result.stdout
        
        # Check that output contains expected content
        assert "WAVE (Wave Momentum Indicator) Help:" in output, "Output should contain Wave help header"
        assert "Individual Trading Rules (ENUM_MOM_TR):" in output, "Output should show Individual Trading Rules section"
        assert "Global Trading Rules (ENUM_GLOBAL_TR):" in output, "Output should show Global Trading Rules section"
        
        # Check for specific trading rules in help
        assert "fast (TR_Fast)" in output, "Should show fast trading rule in help"
        assert "zone (TR_Zone)" in output, "Should show zone trading rule in help"
        assert "strongtrend (TR_StrongTrend)" in output, "Should show strongtrend trading rule in help"
        assert "weaktrend (TR_WeakTrend)" in output, "Should show weaktrend trading rule in help"
        assert "fastzonereverse (TR_FastZoneReverse)" in output, "Should show fastzonereverse trading rule in help"
        assert "bettertrend (TR_BetterTrend)" in output, "Should show bettertrend trading rule in help"
        assert "betterfast (TR_BetterFast)" in output, "Should show betterfast trading rule in help"
        assert "rost (TR_Rost)" in output, "Should show rost trading rule in help"
        assert "trendrost (TR_TrendRost)" in output, "Should show trendrost trading rule in help"
        assert "bettertrendrost (TR_BetterTrendRost)" in output, "Should show bettertrendrost trading rule in help"
        
        # Check for specific global rules in help
        assert "prime (G_TR_PRIME)" in output, "Should show prime global rule in help"
        assert "reverse (G_TR_REVERSE)" in output, "Should show reverse global rule in help"
        assert "primezone (G_TR_PRIME_ZONE)" in output, "Should show primezone global rule in help"
        assert "reversezone (G_TR_REVERSE_ZONE)" in output, "Should show reversezone global rule in help"
        assert "newzone (G_TR_NEW_ZONE)" in output, "Should show newzone global rule in help"
        assert "longzone (G_TR_LONG_ZONE)" in output, "Should show longzone global rule in help"
        assert "longzonereverse (G_TR_LONG_ZONE_REVERSE)" in output, "Should show longzonereverse global rule in help"

    def test_indicator_searcher_enum_extraction(self):
        """Test that IndicatorSearcher correctly extracts ENUM_MOM_TR and ENUM_GLOBAL_TR information."""
        from src.cli.indicators_search import IndicatorSearcher
        
        searcher = IndicatorSearcher()
        wave_indicators = searcher.search_indicators("wave")
        
        assert len(wave_indicators) > 0, "Should find wave indicator"
        wave_indicator = wave_indicators[0]
        
        # Check that trading rules and global rules are extracted
        assert wave_indicator.trading_rules, "Trading rules should be extracted"
        assert wave_indicator.global_rules, "Global rules should be extracted"
        
        # Check that trading rules contain expected content
        trading_rules = wave_indicator.trading_rules
        assert "fast: Basic momentum comparison" in trading_rules, "Should contain fast rule"
        assert "zone: Simple zone-based signals" in trading_rules, "Should contain zone rule"
        assert "strongtrend: Strong trend confirmation" in trading_rules, "Should contain strongtrend rule"
        assert "weaktrend: Weak trend signals" in trading_rules, "Should contain weaktrend rule"
        assert "fastzonereverse: Reverse signals in zones" in trading_rules, "Should contain fastzonereverse rule"
        assert "bettertrend: Enhanced trend signals" in trading_rules, "Should contain bettertrend rule"
        assert "betterfast: Improved fast trading" in trading_rules, "Should contain betterfast rule"
        assert "rost: Reverse momentum signals" in trading_rules, "Should contain rost rule"
        assert "trendrost: Trend-based reverse signals" in trading_rules, "Should contain trendrost rule"
        assert "bettertrendrost: Enhanced trend reverse signals" in trading_rules, "Should contain bettertrendrost rule"
        
        # Check that global rules contain expected content
        global_rules = wave_indicator.global_rules
        assert "prime: Prime rule" in global_rules, "Should contain prime rule"
        assert "reverse: Reverse rule" in global_rules, "Should contain reverse rule"
        assert "primezone: Prime Zone rule" in global_rules, "Should contain primezone rule"
        assert "reversezone: Reverse Zone rule" in global_rules, "Should contain reversezone rule"
        assert "newzone: New Zone rule" in global_rules, "Should contain newzone rule"
        assert "longzone: Long Zone rule" in global_rules, "Should contain longzone rule"
        assert "longzonereverse: Long Zone Reverse rule" in global_rules, "Should contain longzonereverse rule"

    def test_wave_docstring_contains_enum_info(self):
        """Test that Wave indicator docstring contains ENUM_MOM_TR and ENUM_GLOBAL_TR information."""
        from src.calculation.indicators.trend.wave_ind import ENUM_MOM_TR, ENUM_GLOBAL_TR
        
        # Check that ENUM_MOM_TR contains all expected values
        expected_mom_tr_values = [
            "TR_Fast", "TR_Zone", "TR_StrongTrend", "TR_WeakTrend", "TR_FastZoneReverse",
            "TR_BetterTrend", "TR_BetterFast", "TR_Rost", "TR_TrendRost", "TR_BetterTrendRost"
        ]
        
        for value in expected_mom_tr_values:
            assert hasattr(ENUM_MOM_TR, value), f"ENUM_MOM_TR should contain {value}"
        
        # Check that ENUM_GLOBAL_TR contains all expected values
        expected_global_tr_values = [
            "G_TR_PRIME", "G_TR_REVERSE", "G_TR_PRIME_ZONE", "G_TR_REVERSE_ZONE",
            "G_TR_NEW_ZONE", "G_TR_LONG_ZONE", "G_TR_LONG_ZONE_REVERSE"
        ]
        
        for value in expected_global_tr_values:
            assert hasattr(ENUM_GLOBAL_TR, value), f"ENUM_GLOBAL_TR should contain {value}"

    def test_error_handling_enum_info(self):
        """Test that error handling system includes ENUM_MOM_TR and ENUM_GLOBAL_TR information."""
        from src.cli.error_handling import get_indicator_help_data
        
        # Get wave indicator help data
        wave_help = get_indicator_help_data("wave")
        
        assert wave_help is not None, "Should get wave help data"
        assert "enum_details" in wave_help, "Should contain enum_details"
        
        # Check ENUM_MOM_TR details
        assert "ENUM_MOM_TR" in wave_help["enum_details"], "Should contain ENUM_MOM_TR details"
        mom_tr_details = wave_help["enum_details"]["ENUM_MOM_TR"]
        assert "name" in mom_tr_details, "Should have name"
        assert "description" in mom_tr_details, "Should have description"
        assert "values" in mom_tr_details, "Should have values"
        
        # Check that all expected trading rules are present
        expected_mom_tr_values = [
            "fast", "zone", "strongtrend", "weaktrend", "fastzonereverse",
            "bettertrend", "betterfast", "rost", "trendrost", "bettertrendrost"
        ]
        
        actual_values = [value[0] for value in mom_tr_details["values"]]
        for expected_value in expected_mom_tr_values:
            assert expected_value in actual_values, f"Should contain {expected_value}"
        
        # Check ENUM_GLOBAL_TR details
        assert "ENUM_GLOBAL_TR" in wave_help["enum_details"], "Should contain ENUM_GLOBAL_TR details"
        global_tr_details = wave_help["enum_details"]["ENUM_GLOBAL_TR"]
        assert "name" in global_tr_details, "Should have name"
        assert "description" in global_tr_details, "Should have description"
        assert "values" in global_tr_details, "Should have values"
        
        # Check that all expected global rules are present
        expected_global_tr_values = [
            "prime", "reverse", "primezone", "reversezone", "newzone", "longzone", "longzonereverse"
        ]
        
        actual_values = [value[0] for value in global_tr_details["values"]]
        for expected_value in expected_global_tr_values:
            assert expected_value in actual_values, f"Should contain {expected_value}"
