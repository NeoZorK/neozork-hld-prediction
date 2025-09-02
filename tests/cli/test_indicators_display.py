"""
Test improved indicators display functionality.

This module contains tests to verify that the indicators display
shows category names and indicator names properly.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from io import StringIO
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from cli.indicators_search import IndicatorSearcher, IndicatorInfo


class TestIndicatorsDisplay:
    """Test indicators display functionality."""

    def test_display_categories_shows_indicator_names(self):
        """Test that display_categories shows indicator names."""
        # Create a mock searcher with sample data
        searcher = IndicatorSearcher()
        
        # Mock the indicators data
        searcher.indicators = {
            "trend": [
                IndicatorInfo("EMA", "trend", "Exponential Moving Average", "--rule ema", "", "", "", ""),
                IndicatorInfo("ADX", "trend", "Average Directional Index", "--rule adx", "", "", "", "")
            ],
            "oscillators": [
                IndicatorInfo("RSI", "oscillators", "Relative Strength Index", "--rule rsi", "", "", "", "")
            ]
        }
        
        # Capture output
        with patch('sys.stdout', new=StringIO()) as fake_out:
            searcher.display_categories()
            output = fake_out.getvalue()
        
        # Check that category names are shown
        assert "trend" in output
        assert "oscillators" in output
        
        # Check that indicator names are shown
        assert "EMA" in output
        assert "ADX" in output
        assert "RSI" in output
        
        # Check that the tree structure is shown
        assert "└─" in output

    def test_display_categories_empty_category(self):
        """Test display_categories with empty category."""
        searcher = IndicatorSearcher()
        searcher.indicators = {
            "empty": []
        }
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            searcher.display_categories()
            output = fake_out.getvalue()
        
        # Should show the category but no indicators
        assert "empty" in output
        assert "0 indicators" in output

    def test_display_categories_multiple_indicators(self):
        """Test display_categories with multiple indicators in one category."""
        searcher = IndicatorSearcher()
        searcher.indicators = {
            "momentum": [
                IndicatorInfo("MACD", "momentum", "Moving Average Convergence Divergence", "--rule macd", "", "", "", ""),
                IndicatorInfo("RSI", "momentum", "Relative Strength Index", "--rule rsi", "", "", "", ""),
                IndicatorInfo("STOCH", "momentum", "Stochastic Oscillator", "--rule stoch", "", "", "", "")
            ]
        }
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            searcher.display_categories()
            output = fake_out.getvalue()
        
        # Check that all indicator names are shown
        assert "MACD" in output
        assert "RSI" in output
        assert "STOCH" in output
        
        # Check that they are comma-separated
        assert "MACD, RSI, STOCH" in output or "MACD,RSI,STOCH" in output

    def test_indicator_info_display(self):
        """Test IndicatorInfo display method."""
        indicator = IndicatorInfo(
            name="RSI",
            category="oscillators",
            description="Relative Strength Index",
            usage="--rule rsi",
            parameters="period: 14",
            pros="Good for overbought/oversold detection",
            cons="Can give false signals in trending markets",
            file_path="src/calculation/indicators/oscillators/rsi_ind.py"
        )
        
        # Test basic display (doesn't include category)
        basic_display = indicator.display(detailed=False)
        assert "RSI" in basic_display
        assert "Relative Strength Index" in basic_display
        # Basic display doesn't include category
        assert "oscillators" not in basic_display
        
        # Test detailed display (includes category)
        detailed_display = indicator.display(detailed=True)
        assert "RSI" in detailed_display
        assert "Relative Strength Index" in detailed_display
        assert "oscillators" in detailed_display
        assert "period: 14" in detailed_display
        assert "Good for overbought/oversold detection" in detailed_display

    def test_category_emoji_mapping(self):
        """Test that category emojis are properly mapped."""
        searcher = IndicatorSearcher()
        
        # Test known categories
        assert searcher._get_category_emoji("trend") == "📈"
        assert searcher._get_category_emoji("momentum") == "⚡"
        assert searcher._get_category_emoji("oscillators") == "🔄"
        assert searcher._get_category_emoji("volatility") == "📊"
        assert searcher._get_category_emoji("volume") == "📦"
        assert searcher._get_category_emoji("suportresist") == "🎯"
        assert searcher._get_category_emoji("sentiment") == "😊"
        assert searcher._get_category_emoji("probability") == "🎲"
        assert searcher._get_category_emoji("predictive") == "🔮"
        
        # Test unknown category
        assert searcher._get_category_emoji("unknown") == "📋"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 