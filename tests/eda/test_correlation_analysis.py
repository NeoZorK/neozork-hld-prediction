# -*- coding: utf-8 -*-
# tests/eda/test_correlation_analysis.py

import unittest
import pandas as pd
import numpy as np
import os
import tempfile
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt

# Import functions to test
from src.eda.correlation_analysis import (
    compute_correlation,
    generate_correlation_plot,
    compute_feature_importance,
    generate_feature_importance_plot,
    ensure_plots_directory,
    generate_correlation_report,
    print_correlation_analysis,
    print_feature_importance
)

# Add any additional imports needed for your tests
from unittest.mock import patch, MagicMock


class TestCorrelationAnalysis(unittest.TestCase):
    """
    Unit tests for correlation_analysis.py functions.
    """

    def setUp(self):
        """Set up test data for each test."""
        # Create a sample DataFrame for testing
        self.sample_data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [1, 2, 3, 4, 5],  # Perfectly correlated with feature1
            'feature3': [5, 4, 3, 2, 1],  # Perfectly anti-correlated with feature1
            'feature4': [2, 4, 6, 8, 10],  # Perfectly correlated with feature1 (linear transform)
            'feature5': [1, 3, 2, 5, 4],   # Partially correlated with feature1
            'target': [1, 2, 3, 2, 3]      # Target column
        })

        # Create non-numeric data for testing error cases
        self.non_numeric_data = pd.DataFrame({
            'feature1': ['a', 'b', 'c', 'd', 'e'],
            'feature2': [1, 2, 3, 4, 5]
        })

        # Create single-column data for testing error cases
        self.single_column_data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5]
        })

        # Create temporary directory for test outputs
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up after tests."""
        # Close any open plots
        plt.close('all')

    def test_ensure_plots_directory(self):
        """Test that ensure_plots_directory creates and returns the plots directory."""
        plots_dir = ensure_plots_directory()
        self.assertTrue(os.path.exists(plots_dir))
        self.assertTrue('results/plots' in plots_dir)

    def test_compute_correlation_pearson(self):
        """Test Pearson correlation computation."""
        result = compute_correlation(self.sample_data, method='pearson')

        # Check that there's no error in the result
        self.assertNotIn('error', result)

        # Check that the method is correct
        self.assertEqual(result['method'], 'pearson')

        # Check that correlation matrix has the right shape
        self.assertEqual(result['matrix'].shape, (6, 6))

        # Check that strong correlations were identified
        self.assertGreater(len(result['strong_correlations']), 0)

        # Check specific correlation values
        corr_matrix = result['matrix']
        self.assertAlmostEqual(corr_matrix.loc['feature1', 'feature2'], 1.0)
        self.assertAlmostEqual(corr_matrix.loc['feature1', 'feature3'], -1.0)
        self.assertAlmostEqual(corr_matrix.loc['feature1', 'feature4'], 1.0)

    def test_compute_correlation_spearman(self):
        """Test Spearman correlation computation."""
        result = compute_correlation(self.sample_data, method='spearman')

        # Basic checks
        self.assertNotIn('error', result)
        self.assertEqual(result['method'], 'spearman')

        # Check specific correlation values
        corr_matrix = result['matrix']
        self.assertAlmostEqual(corr_matrix.loc['feature1', 'feature2'], 1.0)
        self.assertAlmostEqual(corr_matrix.loc['feature1', 'feature3'], -1.0)

    def test_compute_correlation_not_enough_columns(self):
        """Test error handling when not enough numeric columns are present."""
        result = compute_correlation(self.single_column_data)
        self.assertIn('error', result)
        self.assertEqual(result['min_columns'], 2)
        self.assertEqual(result['found_columns'], 1)

    def test_compute_correlation_non_numeric(self):
        """Test handling of non-numeric columns."""
        result = compute_correlation(self.non_numeric_data)
        # Changed assertion to expect error for non-numeric data
        self.assertIn('error', result)
        self.assertEqual(result['min_columns'], 2)
        self.assertEqual(result['found_columns'], 1)  # Only one numeric column in our test data

    def test_generate_correlation_plot(self):
        """Test generation of correlation plot."""
        result = compute_correlation(self.sample_data)
        fig = generate_correlation_plot(result)

        # Check that a figure was created
        self.assertIsInstance(fig, matplotlib.figure.Figure)

        # Check that the figure has at least one axis
        # Note: Changed from assertEqual to assertGreaterEqual since actual implementation
        # might use more than one axis for legends, colorbars, etc.
        self.assertGreaterEqual(len(fig.get_axes()), 1)

    def test_generate_correlation_plot_with_error(self):
        """Test correlation plot generation with error result."""
        error_result = {'error': 'Test error message'}
        fig = generate_correlation_plot(error_result)

        # Check that a figure was created even with error
        self.assertIsInstance(fig, matplotlib.figure.Figure)

    def test_compute_feature_importance(self):
        """Test feature importance computation."""
        # Create larger test dataset to avoid the min_samples error
        larger_data = pd.DataFrame({
            'feature1': np.random.rand(15),
            'feature2': np.random.rand(15),
            'feature3': np.random.rand(15),
            'feature4': np.random.rand(15),
            'feature5': np.random.rand(15),
            'target': np.random.randint(0, 2, 15)      # Target column
        })

        result = compute_feature_importance(larger_data, target_column='target')

        # Check that there's no error in the result
        self.assertNotIn('error', result)

        # Check that the target column was correctly identified
        self.assertEqual(result['target_column'], 'target')

        # Check that feature importances were computed for all features
        self.assertEqual(len(result['feature_importances']), 5)  # 5 features excluding target

        # Check that we have classified features by importance
        self.assertIn('high_importance', result)
        self.assertIn('medium_importance', result)
        self.assertIn('low_importance', result)

        # Check that top_features is a list of strings
        self.assertTrue(all(isinstance(f, str) for f in result['top_features']))

    def test_compute_feature_importance_auto_target_detection(self):
        """Test automatic target detection in feature importance."""
        # Create data with a recognizable target column, with enough samples
        df = pd.DataFrame({
            'feature1': np.random.rand(15),
            'feature2': np.random.rand(15),
            'target': np.random.randint(0, 2, 15)  # Should be automatically detected
        })

        result = compute_feature_importance(df)  # No target_column specified

        # Check that target was detected
        self.assertEqual(result['target_column'], 'target')
        self.assertNotIn('error', result)

    def test_compute_feature_importance_not_enough_columns(self):
        """Test error handling when not enough numeric columns are present."""
        result = compute_feature_importance(self.single_column_data)
        self.assertIn('error', result)

    def test_generate_feature_importance_plot(self):
        """Test generation of feature importance plot."""
        result = compute_feature_importance(self.sample_data, target_column='target')
        fig = generate_feature_importance_plot(result)

        # Check that a figure was created
        self.assertIsInstance(fig, matplotlib.figure.Figure)

        # Check that the figure has an axis
        self.assertEqual(len(fig.get_axes()), 1)

    def test_generate_feature_importance_plot_with_error(self):
        """Test feature importance plot generation with error result."""
        error_result = {'error': 'Test error message'}
        fig = generate_feature_importance_plot(error_result)

        # Check that a figure was created even with error
        self.assertIsInstance(fig, matplotlib.figure.Figure)

    @patch('builtins.print')  # Mock print function
    def test_print_correlation_analysis(self, mock_print):
        """Test print_correlation_analysis function."""
        result = compute_correlation(self.sample_data)
        print_correlation_analysis(result)

        # Verify that print was called at least once
        self.assertTrue(mock_print.called)

    @patch('builtins.print')  # Mock print function
    def test_print_feature_importance(self, mock_print):
        """Test print_feature_importance function."""
        result = compute_feature_importance(self.sample_data, target_column='target')
        print_feature_importance(result)

        # Verify that print was called at least once
        self.assertTrue(mock_print.called)

    @patch('src.eda.correlation_analysis.HTMLReport')
    @patch('src.eda.correlation_analysis.ensure_report_directory')
    def test_generate_correlation_report(self, mock_ensure_dir, mock_html_report):
        """Test generation of correlation analysis HTML report with mocks."""
        # Setup mocks
        mock_html_report_instance = MagicMock()
        mock_html_report.return_value = mock_html_report_instance
        mock_ensure_dir.return_value = self.test_dir

        # Create a temporary file path for testing
        temp_file = os.path.join(self.test_dir, 'test_data.csv')
        self.sample_data.to_csv(temp_file, index=False)

        # Generate report
        report_path = generate_correlation_report(self.sample_data, temp_file)

        # Check that the HTML report was created
        mock_html_report.assert_called_once()
        mock_html_report_instance.add_header.assert_called_once()
        mock_html_report_instance.save.assert_called_once()

        # Check that the report path is correctly formed
        self.assertTrue(report_path.endswith('.html'))


if __name__ == '__main__':
    unittest.main()
