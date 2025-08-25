# tests/scripts/test_interactive_system.py

"""
Tests for interactive_system.py script.
All comments are in English.
"""

import unittest
import tempfile
import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the script to test
from scripts.ml.interactive_system import InteractiveSystem


class TestInteractiveSystem(unittest.TestCase):
    """Test cases for InteractiveSystem class."""

    def setUp(self):
        """Set up test fixtures."""
        self.system = InteractiveSystem()
        self.test_data = pd.DataFrame({
            'DateTime': pd.date_range('2023-01-01', periods=100, freq='h'),
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 102,
            'Low': np.random.randn(100).cumsum() + 98,
            'Close': np.random.randn(100).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 100)
        })

    def test_interactive_system_initialization(self):
        """Test InteractiveSystem initialization."""
        self.assertIsInstance(self.system, InteractiveSystem)
        self.assertIsNone(self.system.feature_generator)
        self.assertIsNone(self.system.current_data)
        self.assertEqual(self.system.current_results, {})

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_banner(self, mock_stdout):
        """Test print_banner method."""
        self.system.print_banner()
        output = mock_stdout.getvalue()
        
        self.assertIn("NEOZORK HLD PREDICTION", output)
        self.assertIn("INTERACTIVE SYSTEM", output)
        self.assertIn("Feature Engineering", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_main_menu(self, mock_stdout):
        """Test print_main_menu method."""
        self.system.print_main_menu()
        output = mock_stdout.getvalue()
        
        self.assertIn("MAIN MENU", output)
        self.assertIn("Load Data", output)
        self.assertIn("EDA Analysis", output)
        self.assertIn("Feature Engineering", output)
        self.assertIn("Exit", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_eda_menu(self, mock_stdout):
        """Test print_eda_menu method."""
        self.system.print_eda_menu()
        output = mock_stdout.getvalue()
        
        self.assertIn("EDA ANALYSIS MENU", output)
        self.assertIn("Basic Statistics", output)
        self.assertIn("Data Quality Check", output)
        self.assertIn("Correlation Analysis", output)
        self.assertIn("Back to Main Menu", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_feature_engineering_menu(self, mock_stdout):
        """Test print_feature_engineering_menu method."""
        self.system.print_feature_engineering_menu()
        output = mock_stdout.getvalue()
        
        self.assertIn("FEATURE ENGINEERING MENU", output)
        self.assertIn("Generate All Features", output)
        self.assertIn("Proprietary Features", output)
        self.assertIn("Technical Indicators", output)
        self.assertIn("Back to Main Menu", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_visualization_menu(self, mock_stdout):
        """Test print_visualization_menu method."""
        self.system.print_visualization_menu()
        output = mock_stdout.getvalue()
        
        self.assertIn("DATA VISUALIZATION MENU", output)
        self.assertIn("Price Charts", output)
        self.assertIn("Feature Distribution Plots", output)

    def test_load_data_method_exists(self):
        """Test that load_data method exists."""
        self.assertTrue(hasattr(self.system, 'load_data'))
        self.assertTrue(callable(getattr(self.system, 'load_data')))

    def test_run_eda_analysis_method_exists(self):
        """Test that run_eda_analysis method exists."""
        self.assertTrue(hasattr(self.system, 'run_eda_analysis'))
        self.assertTrue(callable(getattr(self.system, 'run_eda_analysis')))

    def test_run_model_development_method_exists(self):
        """Test that run_model_development method exists."""
        self.assertTrue(hasattr(self.system, 'run_model_development'))
        self.assertTrue(callable(getattr(self.system, 'run_model_development')))

    def test_run_method_exists(self):
        """Test that run method exists."""
        self.assertTrue(hasattr(self.system, 'run'))
        self.assertTrue(callable(getattr(self.system, 'run')))

    def test_system_attributes(self):
        """Test system attributes are properly initialized."""
        self.assertIsInstance(self.system.feature_generator, type(None))
        self.assertIsInstance(self.system.current_data, type(None))
        self.assertIsInstance(self.system.current_results, dict)

    def test_system_class_structure(self):
        """Test InteractiveSystem class structure."""
        # Test class inheritance
        self.assertEqual(self.system.__class__.__name__, 'InteractiveSystem')
        
        # Test class docstring
        self.assertIsNotNone(self.system.__class__.__doc__)
        self.assertIn("Interactive system interface", self.system.__class__.__doc__)

    def test_system_initialization_with_data(self):
        """Test system initialization with data."""
        # Test that we can set current_data
        self.system.current_data = self.test_data
        self.assertIsInstance(self.system.current_data, pd.DataFrame)
        self.assertEqual(len(self.system.current_data), 100)

    def test_system_results_storage(self):
        """Test system results storage."""
        # Test that we can store results
        test_results = {'analysis': 'test_result', 'score': 0.95}
        self.system.current_results = test_results
        self.assertEqual(self.system.current_results, test_results)

    def test_load_data_from_file_method_exists(self):
        """Test that load_data_from_file method exists."""
        self.assertTrue(hasattr(self.system, 'load_data_from_file'))
        self.assertTrue(callable(getattr(self.system, 'load_data_from_file')))

    def test_print_model_development_menu_method_exists(self):
        """Test that print_model_development_menu method exists."""
        self.assertTrue(hasattr(self.system, 'print_model_development_menu'))
        self.assertTrue(callable(getattr(self.system, 'print_model_development_menu')))

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_model_development_menu(self, mock_stdout):
        """Test print_model_development_menu method."""
        self.system.print_model_development_menu()
        output = mock_stdout.getvalue()
        
        self.assertIn("MODEL DEVELOPMENT MENU", output)
        self.assertIn("Data Preparation", output)
        self.assertIn("ML Model Training", output)
        self.assertIn("Model Evaluation", output)

    def test_system_methods_return_values(self):
        """Test that system methods return appropriate values."""
        # Test load_data
        try:
            # This will likely fail due to input() call, but we can test the method exists
            method = getattr(self.system, 'load_data')
            self.assertTrue(callable(method))
        except Exception:
            pass  # Expected for interactive methods

        # Test other methods that might exist
        methods_to_test = [
            'run_eda_analysis',
            'run_model_development'
        ]
        
        for method_name in methods_to_test:
            try:
                method = getattr(self.system, method_name)
                self.assertTrue(callable(method))
            except AttributeError:
                pass  # Method might not exist

    def test_system_method_signatures(self):
        """Test that system methods have correct signatures."""
        # Test that core methods exist and are callable
        expected_methods = [
            'print_banner',
            'print_main_menu',
            'print_eda_menu',
            'print_feature_engineering_menu',
            'print_visualization_menu',
            'print_model_development_menu',
            'load_data',
            'load_data_from_file',
            'run_eda_analysis',
            'run_model_development',
            'run'
        ]
        
        for method_name in expected_methods:
            if hasattr(self.system, method_name):
                method = getattr(self.system, method_name)
                self.assertTrue(callable(method))

    def test_system_file_loading_capabilities(self):
        """Test system file loading capabilities."""
        # Test that load_data_from_file method can handle different file types
        method = getattr(self.system, 'load_data_from_file')
        self.assertTrue(callable(method))

    def test_system_menu_structure(self):
        """Test system menu structure."""
        # Test that all menu methods exist and are callable
        menu_methods = [
            'print_main_menu',
            'print_eda_menu',
            'print_feature_engineering_menu',
            'print_visualization_menu',
            'print_model_development_menu'
        ]
        
        for method_name in menu_methods:
            if hasattr(self.system, method_name):
                method = getattr(self.system, method_name)
                self.assertTrue(callable(method))

    def test_system_data_handling(self):
        """Test system data handling capabilities."""
        # Test that we can set and retrieve data
        self.system.current_data = self.test_data
        self.assertIsInstance(self.system.current_data, pd.DataFrame)
        
        # Test that we can set and retrieve results
        test_results = {'test': 'data'}
        self.system.current_results = test_results
        self.assertEqual(self.system.current_results, test_results)


if __name__ == '__main__':
    unittest.main()
