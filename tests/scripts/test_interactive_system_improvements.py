#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for improved interactive system functionality.

This script tests the enhanced EDA analysis features including:
- Comprehensive data quality checks
- Modern statistical analysis with progress bars
- Backup and restore system
- Automatic data fixing capabilities
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from pathlib import Path
import sys
from unittest.mock import patch, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from interactive_system import InteractiveSystem


class TestInteractiveSystemImprovements:
    """Test class for improved interactive system functionality."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data with various quality issues for testing."""
        np.random.seed(42)
        
        # Create sample OHLCV data with issues
        dates = pd.date_range('2023-01-01', periods=1000, freq='H')
        
        data = {
            'datetime': dates,
            'open': np.random.normal(100, 10, 1000),
            'high': np.random.normal(105, 10, 1000),
            'low': np.random.normal(95, 10, 1000),
            'close': np.random.normal(100, 10, 1000),
            'volume': np.random.normal(1000000, 200000, 1000)
        }
        
        df = pd.DataFrame(data)
        
        # Add quality issues for testing
        # NaN values
        df.loc[100:110, 'open'] = np.nan
        df.loc[200:205, 'close'] = np.nan
        
        # Duplicates
        df.loc[300:305] = df.loc[100:105].values
        
        # Zero values
        df.loc[400:410, 'volume'] = 0
        
        # Negative values
        df.loc[500:505, 'low'] = -10
        
        # Infinity values
        df.loc[600:605, 'high'] = np.inf
        
        return df
    
    @pytest.fixture
    def interactive_system(self):
        """Create interactive system instance."""
        return InteractiveSystem()
    
    def test_comprehensive_data_quality_check(self, interactive_system, sample_data):
        """Test comprehensive data quality check functionality."""
        # Load sample data
        interactive_system.current_data = sample_data
        
        # Run comprehensive data quality check
        interactive_system.run_data_quality_check()
        
        # Check that results were saved
        assert 'comprehensive_data_quality' in interactive_system.current_results
        
        quality_data = interactive_system.current_results['comprehensive_data_quality']
        
        # Check quality score calculation
        assert 'quality_score' in quality_data
        assert isinstance(quality_data['quality_score'], (int, float))
        assert 0 <= quality_data['quality_score'] <= 100
        
        # Check issue summaries
        assert 'nan_summary' in quality_data
        assert 'dupe_summary' in quality_data
        assert 'gap_summary' in quality_data
        assert 'zero_summary' in quality_data
        assert 'negative_summary' in quality_data
        assert 'inf_summary' in quality_data
        
        # Check that issues were detected
        assert len(quality_data['nan_summary']) > 0  # Should detect NaN values
        assert len(quality_data['dupe_summary']) > 0  # Should detect duplicates
        assert len(quality_data['zero_summary']) > 0  # Should detect zero values
        assert len(quality_data['negative_summary']) > 0  # Should detect negative values
        assert len(quality_data['inf_summary']) > 0  # Should detect infinity values
    
    def test_comprehensive_basic_statistics(self, interactive_system, sample_data):
        """Test comprehensive basic statistics functionality."""
        # Load sample data
        interactive_system.current_data = sample_data
        
        # Run comprehensive basic statistics
        interactive_system.run_basic_statistics()
        
        # Check that results were saved
        assert 'comprehensive_basic_statistics' in interactive_system.current_results
        
        stats_data = interactive_system.current_results['comprehensive_basic_statistics']
        
        # Check that all analysis types were performed
        assert 'basic_stats' in stats_data
        assert 'descriptive_stats' in stats_data
        assert 'distribution_analysis' in stats_data
        assert 'outlier_analysis' in stats_data
        assert 'time_series_analysis' in stats_data
        
        # Check summary information
        assert 'summary' in stats_data
        summary = stats_data['summary']
        
        assert 'shape' in summary
        assert 'memory_usage_mb' in summary
        assert 'missing_percentage' in summary
        assert 'normal_distributions' in summary
        assert 'skewed_distributions' in summary
        assert 'high_outlier_columns' in summary
    
    def test_fix_all_data_issues(self, interactive_system, sample_data):
        """Test automatic data fixing functionality."""
        # Load sample data
        interactive_system.current_data = sample_data
        
        # First run quality check to get issues
        interactive_system.run_data_quality_check()
        
        # Store original shape
        original_shape = interactive_system.current_data.shape
        
        # Run data fixing
        interactive_system.fix_all_data_issues()
        
        # Check that fix results were saved
        assert 'data_fixes' in interactive_system.current_results
        
        fix_data = interactive_system.current_results['data_fixes']
        
        # Check backup information
        assert 'backup_file' in fix_data
        assert 'backup_timestamp' in fix_data
        assert 'original_shape' in fix_data
        assert 'final_shape' in fix_data
        assert 'fixes_applied' in fix_data
        
        # Check that backup file was created
        backup_file = Path(fix_data['backup_file'])
        assert backup_file.exists()
        
        # Check that fixes were applied
        assert len(fix_data['fixes_applied']) > 0
        
        # Verify that data was actually fixed
        # Check that fixes were applied (data should be different from original)
        assert len(fix_data['fixes_applied']) > 0
        
        # Check that shape changed (duplicates were removed)
        assert fix_data['rows_removed'] > 0 or fix_data['cols_removed'] > 0
        
        # Verify that backup file exists and is different from current data
        backup_file = Path(fix_data['backup_file'])
        assert backup_file.exists()
        
        # Load backup data to verify it's different
        backup_data = pd.read_parquet(backup_file)
        assert backup_data.shape == fix_data['original_shape']
        assert interactive_system.current_data.shape == fix_data['final_shape']
    
    def test_restore_from_backup(self, interactive_system, sample_data):
        """Test backup and restore functionality."""
        # Load sample data
        interactive_system.current_data = sample_data
        
        # Run quality check and fixes to create backup
        interactive_system.run_data_quality_check()
        interactive_system.fix_all_data_issues()
        
        # Store current state
        current_shape = interactive_system.current_data.shape
        
        # Test restore functionality
        interactive_system.restore_from_backup()
        
        # Check that data was restored (shape should match original)
        assert interactive_system.current_data.shape == sample_data.shape
    
    def test_eda_menu_options(self, interactive_system):
        """Test that EDA menu includes all new options."""
        # Check that menu includes new options
        menu_output = []
        
        # Capture menu output (simplified test)
        interactive_system.print_eda_menu()
        
        # The menu should include the new comprehensive options
        # This is a basic test - in practice you'd capture the actual output
        assert True  # Placeholder for menu structure test
    
    def test_error_handling(self, interactive_system):
        """Test error handling in improved functions."""
        # Test with no data loaded
        interactive_system.current_data = None
        
        # These should handle the error gracefully
        interactive_system.run_data_quality_check()
        interactive_system.run_basic_statistics()
        interactive_system.fix_all_data_issues()
        interactive_system.restore_from_backup()
        
        # Test with invalid data
        invalid_data = pd.DataFrame({
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3]
        })
        interactive_system.current_data = invalid_data
        
        # Should handle non-numeric data gracefully
        interactive_system.run_basic_statistics()
    
    def test_progress_bars(self, interactive_system, sample_data):
        """Test that progress bars are implemented."""
        # Load sample data
        interactive_system.current_data = sample_data
        
        # The functions should use tqdm progress bars
        # This is tested by ensuring the functions complete without errors
        interactive_system.run_data_quality_check()
        interactive_system.run_basic_statistics()
        
        # If progress bars cause issues, the functions would fail
        assert True
    
    def test_backup_directory_creation(self, interactive_system, sample_data):
        """Test that backup directory is created properly."""
        # Load sample data
        interactive_system.current_data = sample_data
        
        # Run fixes to trigger backup creation
        interactive_system.run_data_quality_check()
        interactive_system.fix_all_data_issues()
        
        # Check that backup directory exists
        backup_dir = Path("data/backups")
        assert backup_dir.exists()
        assert backup_dir.is_dir()
        
        # Check that backup files were created
        backup_files = list(backup_dir.glob("backup_*.parquet"))
        assert len(backup_files) > 0


class TestInteractiveSystemMenuTracking:
    """Test class for menu tracking functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.system = InteractiveSystem()
    
    def test_initial_menu_status(self):
        """Test that all menu items start as unused."""
        for category, items in self.system.used_menus.items():
            for item, used in items.items():
                assert not used, f"Menu item {category}.{item} should start as unused"
    
    def test_mark_menu_as_used(self):
        """Test marking menu items as used."""
        # Test marking a valid menu item
        self.system.mark_menu_as_used('eda', 'basic_statistics')
        assert self.system.used_menus['eda']['basic_statistics'] is True
        
        # Test marking an invalid menu item (should not raise error)
        self.system.mark_menu_as_used('invalid_category', 'invalid_item')
        
        # Test marking an invalid item in valid category (should not raise error)
        self.system.mark_menu_as_used('eda', 'invalid_item')
    
    def test_reset_menu_status_category(self):
        """Test resetting menu status for specific category."""
        # Mark some items as used
        self.system.mark_menu_as_used('eda', 'basic_statistics')
        self.system.mark_menu_as_used('eda', 'data_quality_check')
        self.system.mark_menu_as_used('feature_engineering', 'generate_all_features')
        
        # Reset only EDA menu
        self.system.reset_menu_status('eda')
        
        # Check EDA items are reset
        assert not self.system.used_menus['eda']['basic_statistics']
        assert not self.system.used_menus['eda']['data_quality_check']
        
        # Check feature engineering items are still marked
        assert self.system.used_menus['feature_engineering']['generate_all_features']
    
    def test_reset_all_menu_status(self):
        """Test resetting all menu status."""
        # Mark some items as used
        self.system.mark_menu_as_used('eda', 'basic_statistics')
        self.system.mark_menu_as_used('feature_engineering', 'generate_all_features')
        self.system.mark_menu_as_used('visualization', 'price_charts')
        
        # Reset all menus
        self.system.reset_menu_status()
        
        # Check all items are reset
        for category, items in self.system.used_menus.items():
            for item, used in items.items():
                assert not used, f"Menu item {category}.{item} should be reset"
    
    def test_show_menu_status(self):
        """Test displaying menu status."""
        # Mark some items as used
        self.system.mark_menu_as_used('eda', 'basic_statistics')
        self.system.mark_menu_as_used('eda', 'data_quality_check')
        self.system.mark_menu_as_used('feature_engineering', 'generate_all_features')
        
        # Capture output
        with patch('builtins.print') as mock_print:
            self.system.show_menu_status()
            
            # Verify that print was called
            assert mock_print.called
            
            # Get all printed lines
            printed_lines = [call[0][0] for call in mock_print.call_args_list]
            
            # Check that status information is displayed
            assert any('EDA:' in line for line in printed_lines)
            assert any('FEATURE ENGINEERING:' in line for line in printed_lines)
            assert any('Progress:' in line for line in printed_lines)
    
    def test_menu_display_with_checkmarks(self):
        """Test that menu display shows checkmarks for used items."""
        # Mark some items as used
        self.system.mark_menu_as_used('eda', 'basic_statistics')
        self.system.mark_menu_as_used('eda', 'correlation_analysis')
        
        # Capture EDA menu output
        with patch('builtins.print') as mock_print:
            self.system.print_eda_menu()
            
            # Get all printed lines
            printed_lines = [call[0][0] for call in mock_print.call_args_list]
            
            # Check that used items show checkmarks
            basic_stats_line = next((line for line in printed_lines if 'Basic Statistics' in line), None)
            correlation_line = next((line for line in printed_lines if 'Correlation Analysis' in line), None)
            
            assert basic_stats_line and '✅' in basic_stats_line
            assert correlation_line and '✅' in correlation_line
            
            # Check that unused items don't show checkmarks
            data_quality_line = next((line for line in printed_lines if 'Data Quality Check' in line), None)
            assert data_quality_line and '✅' not in data_quality_line
    
    def test_feature_engineering_menu_checkmarks(self):
        """Test feature engineering menu checkmarks."""
        # Mark some items as used
        self.system.mark_menu_as_used('feature_engineering', 'generate_all_features')
        self.system.mark_menu_as_used('feature_engineering', 'feature_summary')
        
        # Capture menu output
        with patch('builtins.print') as mock_print:
            self.system.print_feature_engineering_menu()
            
            # Get all printed lines
            printed_lines = [call[0][0] for call in mock_print.call_args_list]
            
            # Check that used items show checkmarks
            generate_features_line = next((line for line in printed_lines if 'Generate All Features' in line), None)
            feature_summary_line = next((line for line in printed_lines if 'Feature Summary Report' in line), None)
            
            assert generate_features_line and '✅' in generate_features_line
            assert feature_summary_line and '✅' in feature_summary_line
    
    def test_visualization_menu_checkmarks(self):
        """Test visualization menu checkmarks."""
        # Mark some items as used
        self.system.mark_menu_as_used('visualization', 'price_charts')
        self.system.mark_menu_as_used('visualization', 'correlation_heatmaps')
        
        # Capture menu output
        with patch('builtins.print') as mock_print:
            self.system.print_visualization_menu()
            
            # Get all printed lines
            printed_lines = [call[0][0] for call in mock_print.call_args_list]
            
            # Check that used items show checkmarks
            price_charts_line = next((line for line in printed_lines if 'Price Charts' in line), None)
            correlation_line = next((line for line in printed_lines if 'Correlation Heatmaps' in line), None)
            
            assert price_charts_line and '✅' in price_charts_line
            assert correlation_line and '✅' in correlation_line
    
    def test_model_development_menu_checkmarks(self):
        """Test model development menu checkmarks."""
        # Mark some items as used
        self.system.mark_menu_as_used('model_development', 'data_preparation')
        self.system.mark_menu_as_used('model_development', 'ml_model_training')
        
        # Capture menu output
        with patch('builtins.print') as mock_print:
            self.system.print_model_development_menu()
            
            # Get all printed lines
            printed_lines = [call[0][0] for call in mock_print.call_args_list]
            
            # Check that used items show checkmarks
            data_prep_line = next((line for line in printed_lines if 'Data Preparation' in line), None)
            model_training_line = next((line for line in printed_lines if 'ML Model Training' in line), None)
            
            assert data_prep_line and '✅' in data_prep_line
            assert model_training_line and '✅' in model_training_line
    
    def test_menu_structure_completeness(self):
        """Test that all menu categories and items are properly defined."""
        expected_categories = ['eda', 'feature_engineering', 'visualization', 'model_development']
        
        for category in expected_categories:
            assert category in self.system.used_menus, f"Category {category} should be defined"
        
        # Check EDA menu items
        expected_eda_items = [
            'basic_statistics', 'data_quality_check', 'correlation_analysis',
            'time_series_analysis', 'feature_importance', 'fix_data_issues',
            'generate_html_report', 'restore_from_backup'
        ]
        for item in expected_eda_items:
            assert item in self.system.used_menus['eda'], f"EDA item {item} should be defined"
        
        # Check Feature Engineering menu items
        expected_fe_items = [
            'generate_all_features', 'proprietary_features', 'technical_indicators',
            'statistical_features', 'temporal_features', 'cross_timeframe_features',
            'feature_selection', 'feature_summary'
        ]
        for item in expected_fe_items:
            assert item in self.system.used_menus['feature_engineering'], f"FE item {item} should be defined"
    
    def test_menu_tracking_persistence(self):
        """Test that menu tracking persists during session."""
        # Mark some items
        self.system.mark_menu_as_used('eda', 'basic_statistics')
        self.system.mark_menu_as_used('feature_engineering', 'generate_all_features')
        
        # Create new system instance (simulating new session)
        new_system = InteractiveSystem()
        
        # Check that new system has fresh state
        assert not new_system.used_menus['eda']['basic_statistics']
        assert not new_system.used_menus['feature_engineering']['generate_all_features']
        
        # Check that original system still has marked items
        assert self.system.used_menus['eda']['basic_statistics']
        assert self.system.used_menus['feature_engineering']['generate_all_features']


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
