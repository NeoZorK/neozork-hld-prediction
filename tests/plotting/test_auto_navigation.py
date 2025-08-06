# -*- coding: utf-8 -*-
# tests/plotting/test_auto_navigation.py

"""
Tests for AUTO mode navigation with field switching.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Import the modules to test
try:
    from src.plotting.term_navigation import AutoTerminalNavigator
except ImportError:
    pytest.skip("Could not import AutoTerminalNavigator", allow_module_level=True)


class TestAutoTerminalNavigator:
    """Test cases for AutoTerminalNavigator class."""
    
    def setup_method(self):
        """Set up test data."""
        # Create sample data with multiple field types
        dates = pd.date_range('2024-01-01', periods=100, freq='H')
        self.sample_data = pd.DataFrame({
            'DateTime': dates,
            'Open': np.random.uniform(1.0, 2.0, 100),
            'High': np.random.uniform(1.0, 2.0, 100),
            'Low': np.random.uniform(1.0, 2.0, 100),
            'Close': np.random.uniform(1.0, 2.0, 100),
            'Volume': np.random.uniform(1000, 5000, 100),
            'pressure_high': np.random.uniform(1.5, 2.5, 100),
            'pressure_low': np.random.uniform(0.5, 1.5, 100),
            'pressure_vector': np.random.uniform(1.0, 2.0, 100),
            'predicted_high': np.random.uniform(1.8, 2.8, 100),
            'predicted_low': np.random.uniform(0.2, 1.2, 100),
            'HL': np.random.uniform(0.1, 0.5, 100),
            'Pressure': np.random.uniform(50, 150, 100),
            'PV': np.random.uniform(1.0, 2.0, 100),
        })
        self.sample_data.set_index('DateTime', inplace=True)
        
        # Create chunks
        chunk_size = 25
        self.chunks = []
        for i in range(0, len(self.sample_data), chunk_size):
            chunk = self.sample_data.iloc[i:i+chunk_size]
            self.chunks.append(chunk)
        
        # Field columns for testing
        self.field_columns = [
            'pressure_high', 'pressure_low', 'pressure_vector',
            'predicted_high', 'predicted_low', 'HL', 'Pressure', 'PV'
        ]
    
    def test_auto_navigator_initialization(self):
        """Test AutoTerminalNavigator initialization."""
        navigator = AutoTerminalNavigator(self.chunks, "Test AUTO", self.field_columns)
        
        assert navigator.chunks == self.chunks
        assert navigator.title == "Test AUTO"
        assert navigator.field_columns == self.field_columns
        assert navigator.current_chunk_index == 0
        assert navigator.current_field_index == 0
        assert navigator.current_group_index == 0
        assert len(navigator.field_groups) > 0
    
    def test_field_group_organization(self):
        """Test field group organization."""
        navigator = AutoTerminalNavigator(self.chunks, "Test AUTO", self.field_columns)
        
        # Check that groups are created
        assert len(navigator.field_groups) > 0
        
        # Check that Pressure group exists
        pressure_group = next((g for g in navigator.field_groups if g['name'] == 'Pressure'), None)
        assert pressure_group is not None
        assert 'pressure_high' in pressure_group['fields']
        assert 'pressure_low' in pressure_group['fields']
        assert 'pressure_vector' in pressure_group['fields']
        
        # Check that Predicted group exists
        predicted_group = next((g for g in navigator.field_groups if g['name'] == 'Predicted'), None)
        assert predicted_group is not None
        assert 'predicted_high' in predicted_group['fields']
        assert 'predicted_low' in predicted_group['fields']
    
    def test_next_field_navigation(self):
        """Test next field navigation."""
        navigator = AutoTerminalNavigator(self.chunks, "Test AUTO", self.field_columns)
        
        # Start with first field
        initial_field = navigator.get_current_field()
        assert initial_field is not None
        
        # Navigate to next field
        result = navigator._next_field()
        assert result is True
        
        # Check that field changed
        new_field = navigator.get_current_field()
        assert new_field != initial_field
    
    def test_previous_field_navigation(self):
        """Test previous field navigation."""
        navigator = AutoTerminalNavigator(self.chunks, "Test AUTO", self.field_columns)
        
        # Move to second field first
        navigator._next_field()
        second_field = navigator.get_current_field()
        
        # Navigate back
        result = navigator._previous_field()
        assert result is True
        
        # Check that field changed back
        first_field = navigator.get_current_field()
        assert first_field != second_field
    
    def test_next_group_navigation(self):
        """Test next group navigation."""
        navigator = AutoTerminalNavigator(self.chunks, "Test AUTO", self.field_columns)
        
        # Start with first group
        initial_group = navigator.get_current_group_info()
        
        # Navigate to next group
        result = navigator._next_group()
        assert result is True
        
        # Check that group changed
        new_group = navigator.get_current_group_info()
        assert new_group['name'] != initial_group['name']
    
    def test_previous_group_navigation(self):
        """Test previous group navigation."""
        navigator = AutoTerminalNavigator(self.chunks, "Test AUTO", self.field_columns)
        
        # Move to second group first
        navigator._next_group()
        second_group = navigator.get_current_group_info()
        
        # Navigate back
        result = navigator._previous_group()
        assert result is True
        
        # Check that group changed back
        first_group = navigator.get_current_group_info()
        assert first_group['name'] != second_group['name']
    
    def test_boundary_conditions(self):
        """Test navigation boundary conditions."""
        navigator = AutoTerminalNavigator(self.chunks, "Test AUTO", self.field_columns)
        
        # Test going back when at first field
        result = navigator._previous_field()
        assert result is False  # Should fail
        
        # Test going forward when at last field of last group
        # Move to last field of last group
        while navigator._next_field():
            pass
        
        result = navigator._next_field()
        assert result is False  # Should fail
    
    def test_get_current_field(self):
        """Test get_current_field method."""
        navigator = AutoTerminalNavigator(self.chunks, "Test AUTO", self.field_columns)
        
        field = navigator.get_current_field()
        assert field is not None
        assert field in self.field_columns
    
    def test_get_current_group_info(self):
        """Test get_current_group_info method."""
        navigator = AutoTerminalNavigator(self.chunks, "Test AUTO", self.field_columns)
        
        group_info = navigator.get_current_group_info()
        assert 'name' in group_info
        assert 'description' in group_info
        assert 'field_index' in group_info
        assert 'total_fields' in group_info
        assert 'current_field' in group_info
    
    def test_empty_field_columns(self):
        """Test navigator with empty field columns."""
        navigator = AutoTerminalNavigator(self.chunks, "Test AUTO", [])
        
        assert navigator.total_groups == 0
        assert navigator.get_current_field() is None
        
        group_info = navigator.get_current_group_info()
        assert group_info['name'] == 'None'
        assert group_info['description'] == 'No fields available'
    
    def test_show_navigation_prompt(self):
        """Test navigation prompt display."""
        navigator = AutoTerminalNavigator(self.chunks, "Test AUTO", self.field_columns)
        
        with patch('builtins.input', return_value='n'):
            prompt = navigator.show_navigation_prompt()
            assert prompt == 'n'
    
    def test_extended_commands(self):
        """Test extended navigation commands."""
        navigator = AutoTerminalNavigator(self.chunks, "Test AUTO", self.field_columns)
        
        # Test that extended commands are available
        assert 'f' in navigator.commands  # next field
        assert 'b' in navigator.commands  # previous field
        assert 'g' in navigator.commands  # next group
        assert 'h' in navigator.commands  # previous group
        assert '?' in navigator.commands  # help


if __name__ == "__main__":
    pytest.main([__file__]) 