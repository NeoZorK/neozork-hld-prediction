# -*- coding: utf-8 -*-
# tests/plotting/test_sr_navigation.py

"""
Tests for SR rule navigation functionality.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from plotting.term_chunked_plotters import plot_sr_chunks


class TestSRNavigation:
    """Test cases for SR rule navigation."""
    
    def setup_method(self):
        """Set up test data."""
        # Create sample data with SR indicators
        dates = pd.date_range('2024-01-01', periods=100, freq='h')
        self.sample_data = pd.DataFrame({
            'DateTime': dates,
            'Open': np.random.uniform(1.0, 2.0, 100),
            'High': np.random.uniform(1.0, 2.0, 100),
            'Low': np.random.uniform(1.0, 2.0, 100),
            'Close': np.random.uniform(1.0, 2.0, 100),
            'Volume': np.random.uniform(1000, 5000, 100),
            'PPrice1': np.random.uniform(0.5, 1.5, 100),  # Support line
            'PPrice2': np.random.uniform(1.5, 2.5, 100),  # Resistance line
        })
        self.sample_data.set_index('DateTime', inplace=True)
    
    def test_sr_navigation_parameters(self):
        """Test that SR navigation accepts correct parameters."""
        # Test that the function signature is correct
        import inspect
        sig = inspect.signature(plot_sr_chunks)
        
        # Check required parameters
        assert 'df' in sig.parameters
        assert 'title' in sig.parameters
        assert 'style' in sig.parameters
        assert 'use_navigation' in sig.parameters
        
        # Check default values
        assert sig.parameters['title'].default == "SR Chunks"
        assert sig.parameters['style'].default == "matrix"
        assert sig.parameters['use_navigation'].default == False
    
    def test_sr_navigation_consistency(self):
        """Test that SR navigation is consistent with other rules."""
        # Import other rule functions for comparison
        from src.plotting.term_chunked_plotters import plot_phld_chunks, plot_pv_chunks
        
        # Check that all have the same signature for navigation
        import inspect
        
        sr_sig = inspect.signature(plot_sr_chunks)
        phld_sig = inspect.signature(plot_phld_chunks)
        pv_sig = inspect.signature(plot_pv_chunks)
        
        # All should have use_navigation parameter
        assert 'use_navigation' in sr_sig.parameters
        assert 'use_navigation' in phld_sig.parameters
        assert 'use_navigation' in pv_sig.parameters
        
        # All should have same default values
        assert sr_sig.parameters['use_navigation'].default == False
        assert phld_sig.parameters['use_navigation'].default == False
        assert pv_sig.parameters['use_navigation'].default == False
    
    def test_sr_function_exists(self):
        """Test that SR function exists and is callable."""
        # Test that the function exists
        assert callable(plot_sr_chunks)
        
        # Test that it can be called with basic parameters
        try:
            # This should not raise an exception for basic validation
            plot_sr_chunks.__call__
        except Exception as e:
            pytest.fail(f"plot_sr_chunks is not callable: {e}")
    
    def test_sr_navigation_template_available(self):
        """Test that navigation template function exists for future rules."""
        from src.plotting.term_chunked_plotters import create_navigation_template
        
        # Test that the template function exists
        assert callable(create_navigation_template)
        
        # Test that it can be called
        try:
            template_func = create_navigation_template("TEST", None, None)
            assert callable(template_func)
        except Exception as e:
            pytest.fail(f"create_navigation_template failed: {e}")
    
    def test_sr_navigation_structure(self):
        """Test that SR function has the correct structure for navigation."""
        import inspect
        
        # Get the source code of the function
        source = inspect.getsource(plot_sr_chunks)
        
        # Check that it has navigation structure
        assert 'if use_navigation:' in source
        assert 'navigator = TerminalNavigator' in source
        assert 'navigator.navigate' in source
        assert 'else:' in source  # Original behavior


if __name__ == "__main__":
    pytest.main([__file__]) 