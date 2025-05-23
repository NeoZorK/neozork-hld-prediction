import unittest
import pandas as pd
import numpy as np
import os
import tempfile
import shutil
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock

# Add the parent directory to the system path to import the module
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Импортируем функции из правильных модулей
from src.eda.correlation_analysis import (
    compute_feature_importance,
    generate_feature_importance_plot,
    print_feature_importance
)

from src.eda.feature_importance import (
    plot_feature_relationships,
    feature_importance_main,
    generate_feature_importance_report,
    print_colored_feature_importance_summary,
    save_feature_importance_to_json,
    generate_global_feature_importance_summary
)

class TestFeatureImportance(unittest.TestCase):
    """Unit tests for feature_importance.py module."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a sample DataFrame for testing
        np.random.seed(42)  # For reproducibility
        size = 100

        # Create a DataFrame with numeric features
        self.df = pd.DataFrame({
            'feature1': np.random.normal(0, 1, size),
            'feature2': np.random.normal(0, 1, size),
            'feature3': np.random.normal(0, 1, size),
            'feature4': np.random.normal(0, 1, size),
            'feature5': np.random.normal(0, 1, size),
            'target': np.random.normal(0, 1, size)
        })

        # Add correlation to some features
        self.df['feature1'] = self.df['target'] * 0.8 + np.random.normal(0, 0.5, size)  # High correlation
        self.df['feature2'] = self.df['target'] * 0.5 + np.random.normal(0, 0.8, size)  # Medium correlation

        # Create a categorical target for classification tests
        self.df_class = self.df.copy()
        self.df_class['target'] = (self.df_class['target'] > 0).astype(int)

        # Create a temporary directory for saving files
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up after each test method."""
        # Remove temporary directory
        try:
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            print(f"Error removing temporary directory: {e}")

    def test_compute_feature_importance_regression(self):
        """Test computing feature importance for regression problem."""
        result = compute_feature_importance(self.df, 'target')

        # Check if result contains expected keys
        self.assertIn('feature_importances', result)
        self.assertIn('top_features', result)
        self.assertIn('is_classification', result)
        self.assertFalse(result['is_classification'])
        self.assertEqual(result['target_column'], 'target')

        # Check if features are sorted by importance
        importances = [f['importance'] for f in result['feature_importances']]
        self.assertEqual(importances, sorted(importances, reverse=True))

        # Check if feature1 is in top features (as we designed it to be important)
        self.assertIn('feature1', result['top_features'])

    def test_compute_feature_importance_classification(self):
        """Test computing feature importance for classification problem."""
        result = compute_feature_importance(self.df_class, 'target')

        # Check if result contains expected keys
        self.assertIn('feature_importances', result)
        self.assertIn('top_features', result)
        self.assertIn('is_classification', result)
        self.assertTrue(result['is_classification'])

        # Check if at least one feature has importance > 0
        importances = [f['importance'] for f in result['feature_importances']]
        self.assertTrue(any(imp > 0 for imp in importances))

    def test_compute_feature_importance_error_handling(self):
        """Test error handling in compute_feature_importance function."""
        # Test with non-existent target column
        result = compute_feature_importance(self.df, 'non_existent_target')
        self.assertIn('error', result)

        # Test with empty DataFrame
        empty_df = pd.DataFrame()
        result = compute_feature_importance(empty_df, 'target')
        self.assertIn('error', result)

    def test_feature_importance_main(self):
        """Test the main feature importance function."""
        # Mock the report generation to avoid file operations
        with patch('src.eda.feature_importance.generate_feature_importance_report', return_value='mocked_path'):
            result, report_path = feature_importance_main(
                self.df,
                file_path='test_file.parquet',
                target_column='target',
                print_output=False,
                generate_report=True
            )

            # Check if the function returns expected output
            self.assertIn('feature_importances', result)
            self.assertEqual(report_path, 'mocked_path')

    @patch('matplotlib.pyplot.savefig')  # Mock savefig to avoid actual file operations
    def test_generate_feature_importance_plot(self, mock_savefig):
        """Test generation of feature importance plot."""
        result = compute_feature_importance(self.df, 'target')
        fig = generate_feature_importance_plot(result)

        # Verify that a figure was created
        self.assertIsInstance(fig, plt.Figure)

        # Check if figure has at least one axis
        self.assertGreater(len(fig.axes), 0)

        # Close the figure to free memory
        plt.close(fig)

    @patch('matplotlib.pyplot.savefig')  # Mock savefig to avoid actual file operations
    def test_plot_feature_relationships(self, mock_savefig):
        """Test plotting of feature relationships."""
        result = compute_feature_importance(self.df, 'target')
        figures = plot_feature_relationships(self.df, result)

        # Verify that figures were created
        self.assertIsInstance(figures, list)
        self.assertGreater(len(figures), 0)

        # Check if all items in the list are figures
        for fig in figures:
            self.assertIsInstance(fig, plt.Figure)
            plt.close(fig)  # Close the figure to free memory

    def test_error_handling_in_relationships_plot(self):
        """Test error handling in plot_feature_relationships function."""
        # Create an error result dict
        error_result = {'error': 'Test error message'}
        figures = plot_feature_relationships(self.df, error_result)

        # Should return a list with one figure showing error message
        self.assertEqual(len(figures), 1)
        self.assertIsInstance(figures[0], plt.Figure)

        # Close the figure
        plt.close(figures[0])

    @patch('src.eda.feature_importance.ensure_report_directory')
    @patch('src.eda.html_report_generator.HTMLReport')
    @patch('src.eda.correlation_analysis.compute_feature_importance')
    @patch('src.eda.feature_importance.generate_feature_importance_plot')
    @patch('src.eda.feature_importance.plot_feature_relationships')
    @patch('matplotlib.pyplot.close')  # Также добавляем патч для plt.close
    def test_generate_feature_importance_report(self, mock_close, mock_plot_relationships, mock_gen_plot, mock_compute_importance, mock_html_report, mock_ensure_dir):
        """Test generation of HTML report."""
        # Setup mocks
        mock_ensure_dir.return_value = self.temp_dir
        mock_report_instance = mock_html_report.return_value
        mock_report_instance.save.return_value = None

        # Mock для функции plot_feature_relationships
        mock_fig = plt.figure()
        mock_plot_relationships.return_value = [mock_fig]

        # Mock для функции generate_feature_importance_plot
        mock_gen_plot.return_value = mock_fig

        # Mock feature importance result
        mock_importance_result = {
            'target_column': 'target',
            'is_classification': False,
            'num_features': 5,
            'top_features': ['feature1', 'feature2'],
            'feature_importances': [
                {'feature': 'feature1', 'importance': 0.5, 'normalized_importance': 100.0, 'cumulative_importance': 0.5},
                {'feature': 'feature2', 'importance': 0.3, 'normalized_importance': 60.0, 'cumulative_importance': 0.8},
                {'feature': 'feature3', 'importance': 0.1, 'normalized_importance': 20.0, 'cumulative_importance': 0.9}
            ],
            'high_importance': [
                {'feature': 'feature1', 'importance': 0.5, 'normalized_importance': 100.0}
            ],
            'medium_importance': [
                {'feature': 'feature2', 'importance': 0.3, 'normalized_importance': 60.0}
            ],
            'low_importance': [
                {'feature': 'feature3', 'importance': 0.1, 'normalized_importance': 20.0}
            ]
        }
        mock_compute_importance.return_value = mock_importance_result

        # Generate a report
        report_path = generate_feature_importance_report(
            self.df,
            'test_file.parquet',
            target_column='target'
        )

        # Check if the ensure_report_directory was called
        mock_ensure_dir.assert_called_once_with('test_file.parquet')

        # Check if HTMLReport was created
        mock_html_report.assert_called_once()

        # Check if the save method was called
        mock_report_instance.save.assert_called_once()

        # Verify the report path
        self.assertEqual(report_path, os.path.join(self.temp_dir, "feature_importance_analysis.html"))

    @patch('builtins.print')
    def test_print_feature_importance(self, mock_print):
        """Test printing feature importance."""
        result = compute_feature_importance(self.df, 'target')
        print_feature_importance(result)

        # Verify that print was called
        self.assertTrue(mock_print.called)

    @patch('builtins.print')
    def test_print_colored_feature_importance_summary(self, mock_print):
        """Test printing colored feature importance summary."""
        result = compute_feature_importance(self.df, 'target')
        print_colored_feature_importance_summary(result, 'test_file.parquet')

        # Verify that print was called
        self.assertTrue(mock_print.called)

        # Test with error result
        error_result = {'error': 'Test error message'}
        print_colored_feature_importance_summary(error_result)
        self.assertTrue(mock_print.called)

    @patch('json.dump')
    @patch('builtins.open', create=True)
    @patch('os.makedirs')
    def test_save_feature_importance_to_json(self, mock_makedirs, mock_open, mock_json_dump):
        """Test saving feature importance to JSON."""
        result = compute_feature_importance(self.df, 'target')
        save_feature_importance_to_json(result, 'test_file.parquet')

        # Check if functions were called
        mock_makedirs.assert_called_once()
        mock_open.assert_called_once()
        mock_json_dump.assert_called_once()

        # Test with error result
        error_result = {'error': 'Test error message'}
        self.assertIsNone(save_feature_importance_to_json(error_result))

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_generate_global_feature_importance_summary(self, mock_makedirs, mock_path_exists):
        """Test generation of global feature importance summary."""
        mock_path_exists.return_value = False

        # Create multiple feature importance results
        results = [
            compute_feature_importance(self.df, 'target'),
            compute_feature_importance(self.df_class, 'target')
        ]
        file_paths = ['test_file1.parquet', 'test_file2.parquet']

        # Set output path to temp_dir
        output_path = os.path.join(self.temp_dir, 'global_summary.html')

        path = generate_global_feature_importance_summary(results, file_paths, output_path)

        # Verify function returned expected path
        self.assertEqual(path, output_path)

if __name__ == '__main__':
    unittest.main()
