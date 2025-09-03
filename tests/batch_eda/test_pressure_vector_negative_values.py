#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test that pressure_vector can contain negative values and is not automatically fixed.

This test verifies that:
1. pressure_vector negative values are not flagged as issues
2. pressure_vector is not automatically fixed during data quality checks
3. Other columns still get proper negative value detection
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os

from src.batch_eda.data_quality import negative_check
from src.batch_eda.fix_files import fix_negatives


class TestPressureVectorNegativeValues:
    """Test handling of negative values in pressure_vector column."""
    
    def setup_method(self):
        """Set up test data with negative pressure_vector values."""
        # Create test data with negative pressure_vector values
        dates = pd.date_range('2023-01-01', periods=100, freq='H')
        self.test_data = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 100),
            'High': np.random.uniform(110, 120, 100),
            'Low': np.random.uniform(90, 100, 100),
            'Close': np.random.uniform(100, 110, 100),
            'Volume': np.random.randint(1000, 10000, 100),
            'pressure': np.random.uniform(-5, 5, 100),
            'pressure_vector': np.random.uniform(-10, 10, 100),  # Can be negative
            'predicted_low': np.random.uniform(90, 100, 100),
            'predicted_high': np.random.uniform(110, 120, 100)
        }, index=dates)
        
        # Add some negative values to pressure_vector (this should be allowed)
        self.test_data.iloc[10:20, self.test_data.columns.get_loc('pressure_vector')] = -5.0
        self.test_data.iloc[30:40, self.test_data.columns.get_loc('pressure_vector')] = -3.0
        
        # Add some negative values to other columns (these should be flagged)
        self.test_data.iloc[50:55, self.test_data.columns.get_loc('Open')] = -100.0  # This should be flagged
        self.test_data.iloc[60:65, self.test_data.columns.get_loc('Volume')] = -1000  # This should be flagged
    
    def test_pressure_vector_negative_values_not_flagged(self):
        """Test that pressure_vector negative values are not flagged as issues."""
        from colorama import Fore, Style
        
        negative_summary = []
        negative_check(self.test_data, negative_summary, Fore, Style)
        
        # Check that pressure_vector is not in the negative_summary
        pressure_vector_issues = [item for item in negative_summary if item['column'] == 'pressure_vector']
        assert len(pressure_vector_issues) == 0, "pressure_vector should not be flagged for negative values"
        
        # Check that other columns with negative values are flagged
        open_issues = [item for item in negative_summary if item['column'] == 'Open']
        volume_issues = [item for item in negative_summary if item['column'] == 'Volume']
        
        assert len(open_issues) > 0, "Open column should be flagged for negative values"
        assert len(volume_issues) > 0, "Volume column should be flagged for negative values"
    
    def test_fix_negatives_skips_pressure_vector(self):
        """Test that fix_negatives function skips pressure_vector column."""
        # Create data with negative values in pressure_vector and other columns
        test_df = self.test_data.copy()
        
        # Apply fix_negatives
        fixed_df = fix_negatives(test_df)
        
        # Check that pressure_vector negative values are preserved
        original_negatives = (test_df['pressure_vector'] < 0).sum()
        fixed_negatives = (fixed_df['pressure_vector'] < 0).sum()
        
        assert original_negatives == fixed_negatives, "pressure_vector negative values should be preserved"
        
        # Check that other columns are fixed
        original_open_negatives = (test_df['Open'] < 0).sum()
        fixed_open_negatives = (fixed_df['Open'] < 0).sum()
        
        assert original_open_negatives > 0, "Test data should have negative Open values"
        assert fixed_open_negatives == 0, "Open column negative values should be fixed"
    
    def test_pressure_vector_negative_values_are_expected(self):
        """Test that pressure_vector negative values are marked as expected."""
        from colorama import Fore, Style
        
        # Create a smaller dataset to test direct processing
        small_data = self.test_data.head(50).copy()
        
        negative_summary = []
        negative_check(small_data, negative_summary, Fore, Style)
        
        # pressure_vector should not be in negative_summary
        pressure_vector_issues = [item for item in negative_summary if item['column'] == 'pressure_vector']
        assert len(pressure_vector_issues) == 0, "pressure_vector should not be in negative_summary"
    
    def test_large_dataset_pressure_vector_handling(self):
        """Test pressure_vector handling in large datasets with sampling."""
        from colorama import Fore, Style
        
        # Create a large dataset
        large_data = pd.concat([self.test_data] * 100, ignore_index=True)
        
        negative_summary = []
        negative_check(large_data, negative_summary, Fore, Style)
        
        # pressure_vector should not be in negative_summary
        pressure_vector_issues = [item for item in negative_summary if item['column'] == 'pressure_vector']
        assert len(pressure_vector_issues) == 0, "pressure_vector should not be flagged even in large datasets"
    
    def test_pressure_vector_with_summary(self):
        """Test that pressure_vector is still skipped even when explicitly provided in summary."""
        # Create a negative summary that includes pressure_vector
        negative_summary = [
            {'column': 'pressure_vector', 'negatives': 10, 'percent': 10.0},
            {'column': 'Open', 'negatives': 5, 'percent': 5.0}
        ]
        
        test_df = self.test_data.copy()
        fixed_df = fix_negatives(test_df, negative_summary)
        
        # pressure_vector should still be skipped
        original_negatives = (test_df['pressure_vector'] < 0).sum()
        fixed_negatives = (fixed_df['pressure_vector'] < 0).sum()
        
        assert original_negatives == fixed_negatives, "pressure_vector should be skipped even when in summary"
        
        # Open should be fixed
        original_open_negatives = (test_df['Open'] < 0).sum()
        fixed_open_negatives = (fixed_df['Open'] < 0).sum()
        
        assert fixed_open_negatives == 0, "Open column should still be fixed"
    
    def test_pressure_vector_case_insensitive(self):
        """Test that pressure_vector is recognized regardless of case."""
        # Create data with different case variations
        test_df = self.test_data.copy()
        test_df = test_df.rename(columns={'pressure_vector': 'Pressure_Vector'})
        
        negative_summary = []
        from colorama import Fore, Style
        negative_check(test_df, negative_summary, Fore, Style)
        
        # Pressure_Vector should not be in negative_summary
        pressure_vector_issues = [item for item in negative_summary if item['column'] == 'Pressure_Vector']
        assert len(pressure_vector_issues) == 0, "Pressure_Vector should not be flagged regardless of case"
    
    def test_other_columns_still_processed(self):
        """Test that other columns are still properly processed for negative values."""
        from colorama import Fore, Style
        
        negative_summary = []
        negative_check(self.test_data, negative_summary, Fore, Style)
        
        # Should have issues for Open and Volume
        assert len(negative_summary) > 0, "Should detect negative values in other columns"
        
        # Check that we have the expected columns
        columns_with_issues = [item['column'] for item in negative_summary]
        assert 'Open' in columns_with_issues, "Open should be detected"
        assert 'Volume' in columns_with_issues, "Volume should be detected"
        assert 'pressure_vector' not in columns_with_issues, "pressure_vector should not be detected"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
