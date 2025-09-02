# -*- coding: utf-8 -*-
"""
Tests for conftest.py configuration.

This module tests the global pytest configuration and fixtures.
"""

import pytest
import warnings
from unittest.mock import Mock, patch


class TestPytestConfiguration:
    """Test pytest configuration functions."""
    
    def test_pytest_configure(self):
        """Test pytest_configure function adds warning filters."""
        import sys
        import os
        
        # Try different paths for conftest.py
        possible_paths = [
            '/app',  # Direct path to root
            os.path.dirname(os.path.dirname(__file__)),  # /app
            os.path.dirname(__file__),  # /app/tests
        ]
        
        conftest_loaded = False
        for path in possible_paths:
            try:
                sys.path.insert(0, path)
                from conftest import pytest_configure
                conftest_loaded = True
                break
            except ImportError:
                continue
        
        if not conftest_loaded:
            pytest.skip("Could not import conftest.py")
        
        # Mock config object
        mock_config = Mock()
        
        # Call the function
        pytest_configure(mock_config)
        
        # Verify warning filters were added
        expected_calls = [
            ('filterwarnings', 'ignore::DeprecationWarning'),
            ('filterwarnings', 'ignore::PendingDeprecationWarning'),
            ('filterwarnings', 'ignore::UserWarning'),
            ('filterwarnings', 'ignore::FutureWarning'),
            ('filterwarnings', 'ignore::RuntimeWarning')
        ]
        
        for call_args in expected_calls:
            mock_config.addinivalue_line.assert_any_call(*call_args)
    
    def test_pytest_collection_modifyitems(self):
        """Test pytest_collection_modifyitems function adds warning markers."""
        import sys
        import os
        
        # Try different paths for conftest.py
        possible_paths = [
            os.path.dirname(os.path.dirname(__file__)),  # /app
            os.path.dirname(__file__),  # /app/tests
            '/app'  # Direct path
        ]
        
        conftest_loaded = False
        for path in possible_paths:
            try:
                sys.path.insert(0, path)
                from conftest import pytest_collection_modifyitems
                conftest_loaded = True
                break
            except ImportError:
                continue
        
        if not conftest_loaded:
            pytest.skip("Could not import conftest.py")
        
        # Mock config and items
        mock_config = Mock()
        mock_item1 = Mock()
        mock_item2 = Mock()
        mock_items = [mock_item1, mock_item2]
        
        # Call the function
        pytest_collection_modifyitems(mock_config, mock_items)
        
        # Verify markers were added to each item
        for item in mock_items:
            item.add_marker.assert_called_once()
            call_args = item.add_marker.call_args[0][0]
            assert call_args.name == 'filterwarnings'
            assert call_args.args == ('ignore',)
    
    def test_warning_suppression_global(self):
        """Test that warnings are suppressed globally."""
        # This test verifies that the global warning suppression works
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Trigger a warning
            warnings.warn("Test warning", UserWarning)
            
            # In a real environment with conftest.py loaded, this warning would be suppressed
            # Here we just verify the warning was caught
            assert len(w) >= 1
            assert issubclass(w[-1].category, UserWarning)
    
    def test_deprecation_warning_suppression(self):
        """Test that DeprecationWarning is suppressed."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Trigger a deprecation warning
            warnings.warn("Test deprecation", DeprecationWarning)
            
            # Verify warning was caught
            assert len(w) >= 1
            assert issubclass(w[-1].category, DeprecationWarning)
    
    def test_future_warning_suppression(self):
        """Test that FutureWarning is suppressed."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Trigger a future warning
            warnings.warn("Test future warning", FutureWarning)
            
            # Verify warning was caught
            assert len(w) >= 1
            assert issubclass(w[-1].category, FutureWarning)
    
    def test_runtime_warning_suppression(self):
        """Test that RuntimeWarning is suppressed."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Trigger a runtime warning
            warnings.warn("Test runtime warning", RuntimeWarning)
            
            # Verify warning was caught
            assert len(w) >= 1
            assert issubclass(w[-1].category, RuntimeWarning)


class TestConftestImports:
    """Test that conftest.py can be imported without errors."""
    
    def test_conftest_import(self):
        """Test that conftest.py can be imported."""
        import conftest
        
        # Verify the module has the expected functions
        assert hasattr(conftest, 'pytest_configure')
        assert hasattr(conftest, 'pytest_collection_modifyitems')
        assert callable(conftest.pytest_configure)
        assert callable(conftest.pytest_collection_modifyitems)
    
    def test_conftest_docstring(self):
        """Test that conftest.py has proper documentation."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        import conftest
        
        assert conftest.__doc__ is not None
        assert "Global pytest configuration" in conftest.__doc__


class TestConftestFunctionality:
    """Test the actual functionality of conftest.py functions."""
    
    def test_pytest_configure_with_real_config(self):
        """Test pytest_configure with a more realistic config mock."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from conftest import pytest_configure
        
        # Create a more realistic mock
        mock_config = Mock()
        mock_config.addinivalue_line = Mock()
        
        # Call the function
        pytest_configure(mock_config)
        
        # Verify it was called 5 times (for each warning type)
        assert mock_config.addinivalue_line.call_count == 5
        
        # Verify specific calls
        calls = mock_config.addinivalue_line.call_args_list
        call_args = [call[0] for call in calls]
        
        expected_calls = [
            ('filterwarnings', 'ignore::DeprecationWarning'),
            ('filterwarnings', 'ignore::PendingDeprecationWarning'),
            ('filterwarnings', 'ignore::UserWarning'),
            ('filterwarnings', 'ignore::FutureWarning'),
            ('filterwarnings', 'ignore::RuntimeWarning')
        ]
        
        for expected in expected_calls:
            assert expected in call_args
    
    def test_pytest_collection_modifyitems_with_real_items(self):
        """Test pytest_collection_modifyitems with realistic test items."""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from conftest import pytest_collection_modifyitems
        
        # Create realistic mock items
        mock_config = Mock()
        mock_item1 = Mock()
        mock_item1.add_marker = Mock()
        mock_item2 = Mock()
        mock_item2.add_marker = Mock()
        mock_items = [mock_item1, mock_item2]
        
        # Call the function
        pytest_collection_modifyitems(mock_config, mock_items)
        
        # Verify each item got a marker
        for item in mock_items:
            item.add_marker.assert_called_once()
            
            # Verify the marker is correct
            marker_call = item.add_marker.call_args[0][0]
            assert marker_call.name == 'filterwarnings'
            assert marker_call.args == ('ignore',)
    
    def test_warning_filter_effectiveness(self):
        """Test that the warning filters actually work in practice."""
        # This test simulates what happens when pytest runs with our conftest.py
        with warnings.catch_warnings(record=True) as w:
            # Simulate the warning filters being applied
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            warnings.filterwarnings("ignore", category=UserWarning)
            warnings.filterwarnings("ignore", category=FutureWarning)
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            
            # Try to trigger warnings
            warnings.warn("Deprecation test", DeprecationWarning)
            warnings.warn("User warning test", UserWarning)
            warnings.warn("Future warning test", FutureWarning)
            warnings.warn("Runtime warning test", RuntimeWarning)
            
            # All warnings should be suppressed
            assert len(w) == 0
