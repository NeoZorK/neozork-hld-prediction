# -*- coding: utf-8 -*-
# tests/plotting/test_field_colors.py

"""
Tests for field color assignment functionality.
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from plotting.term_chunked_plot import _get_field_color, _get_field_color_enhanced


class TestFieldColorAssignment:
    """Test cases for field color assignment."""
    
    def test_get_field_color_returns_valid_color(self):
        """Test that _get_field_color returns a valid color name."""
        field_name = "pressure"
        color = _get_field_color(field_name)
        
        # Check that color is a string
        assert isinstance(color, str)
        
        # Check that color ends with "+" (plotext bright colors)
        assert color.endswith("+")
        
        # Check that color is not empty
        assert len(color) > 0
    
    def test_get_field_color_consistent_for_same_field(self):
        """Test that the same field always gets the same color."""
        field_name = "predicted_high"
        color1 = _get_field_color(field_name)
        color2 = _get_field_color(field_name)
        
        assert color1 == color2
    
    def test_get_field_color_different_for_different_fields(self):
        """Test that different fields get different colors."""
        field1 = "pressure"
        field2 = "pressure_vector"
        field3 = "predicted_low"
        
        color1 = _get_field_color(field1)
        color2 = _get_field_color(field2)
        color3 = _get_field_color(field3)
        
        # At least some colors should be different
        colors = [color1, color2, color3]
        unique_colors = set(colors)
        assert len(unique_colors) > 1
    
    def test_get_field_color_valid_colors(self):
        """Test that all returned colors are from the valid color palette."""
        valid_colors = {
            "green+", "blue+", "red+", "yellow+", "magenta+", "cyan+",
            "white+", "orange+", "purple+", "pink+", "brown+", "gray+",
            "light_green+", "light_blue+", "light_red+", "light_yellow+",
            "light_magenta+", "light_cyan+", "light_white+", "light_orange+"
        }
        
        # Test multiple fields to ensure we get valid colors
        test_fields = ["pressure", "pressure_vector", "predicted_high", "predicted_low", "volume"]
        
        for field in test_fields:
            color = _get_field_color(field)
            assert color in valid_colors
    
    def test_get_field_color_case_sensitive(self):
        """Test that field names are case sensitive for color assignment."""
        field1 = "pressure"
        field2 = "Pressure"
        field3 = "PRESSURE"
        
        color1 = _get_field_color(field1)
        color2 = _get_field_color(field2)
        color3 = _get_field_color(field3)
        
        # Different cases should get different colors
        assert color1 != color2 or color2 != color3 or color1 != color3
    
    def test_get_field_color_special_characters(self):
        """Test that field names with special characters work correctly."""
        field1 = "pressure_high"
        field2 = "pressure-high"
        field3 = "pressure.high"
        
        # Should not raise exceptions
        color1 = _get_field_color(field1)
        color2 = _get_field_color(field2)
        color3 = _get_field_color(field3)
        
        assert isinstance(color1, str)
        assert isinstance(color2, str)
        assert isinstance(color3, str)
    
    def test_get_field_color_empty_string(self):
        """Test that empty field name works correctly."""
        color = _get_field_color("")
        
        assert isinstance(color, str)
        assert color.endswith("+")
    
    def test_get_field_color_unicode(self):
        """Test that unicode field names work correctly."""
        field = "давление_вектор"
        color = _get_field_color(field)
        
        assert isinstance(color, str)
        assert color.endswith("+")


class TestEnhancedFieldColorAssignment:
    """Test cases for enhanced field color assignment."""
    
    def test_get_field_color_enhanced_returns_valid_color(self):
        """Test that _get_field_color_enhanced returns a valid color name."""
        field_name = "pressure"
        color = _get_field_color_enhanced(field_name)
        
        # Check that color is a string
        assert isinstance(color, str)
        
        # Check that color ends with "+" (plotext bright colors)
        assert color.endswith("+")
        
        # Check that color is not empty
        assert len(color) > 0
    
    def test_get_field_color_enhanced_consistent_for_same_field(self):
        """Test that the same field always gets the same color in enhanced system."""
        field_name = "predicted_high"
        color1 = _get_field_color_enhanced(field_name)
        color2 = _get_field_color_enhanced(field_name)
        
        assert color1 == color2
    
    def test_get_field_color_enhanced_valid_colors(self):
        """Test that all returned colors are from the valid enhanced color palette."""
        valid_colors = {
            "green+", "blue+", "red+", "yellow+", "magenta+", "cyan+",
            "white+", "orange+", "purple+", "pink+", "brown+", "gray+",
            "light_green+", "light_blue+", "light_red+", "light_yellow+",
            "light_magenta+", "light_cyan+", "light_white+", "light_orange+"
        }
        
        # Test multiple fields to ensure we get valid colors
        test_fields = ["pressure", "pressure_vector", "predicted_high", "predicted_low", "volume"]
        
        for field in test_fields:
            color = _get_field_color_enhanced(field)
            assert color in valid_colors
    
    def test_enhanced_vs_original_system(self):
        """Test that enhanced system may give different colors than original."""
        test_fields = ["pressure", "pressure_vector", "predicted_high", "predicted_low"]
        
        for field in test_fields:
            original_color = _get_field_color(field)
            enhanced_color = _get_field_color_enhanced(field)
            
            # Both should be valid colors
            assert original_color.endswith("+")
            assert enhanced_color.endswith("+")
            
            # They may be the same or different, both are valid
            # (enhanced system prioritizes different colors but may have same hash results)


if __name__ == "__main__":
    pytest.main([__file__])
