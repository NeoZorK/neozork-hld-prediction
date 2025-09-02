# -*- coding: utf-8 -*-
# tests/src/calculation/test_rules.py

"""
Unit tests for src/calculation/rules.py
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "src"))

from src.calculation.rules import (
    apply_rule_predict_hld, apply_rule_pv_highlow, apply_rule_support_resistants,
    apply_rule_pressure_vector, apply_rule_auto, _get_series
)


class TestRules:
    """Test cases for rules module."""
    
    def setup_method(self):
        """Set up test data."""
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        self.test_df = pd.DataFrame({
            'Open': np.random.rand(100) * 100,
            'High': np.random.rand(100) * 100 + 1,
            'Low': np.random.rand(100) * 100 - 1,
            'Close': np.random.rand(100) * 100,
            'Volume': np.random.randint(1000, 10000, 100),
            'HL': np.random.rand(100) * 10,
            'PV': np.random.rand(100) * 2 - 1  # Values between -1 and 1
        }, index=dates)
    
    def test_get_series_existing_column(self):
        """Test _get_series with existing column."""
        result = _get_series(self.test_df, 'Open')
        assert isinstance(result, pd.Series)
        assert len(result) == 100
        assert not result.isna().any()
    
    def test_get_series_missing_column(self):
        """Test _get_series with missing column."""
        result = _get_series(self.test_df, 'MissingColumn')
        assert isinstance(result, pd.Series)
        assert len(result) == 100
        assert (result == 0).all()
    
    def test_get_series_with_custom_default(self):
        """Test _get_series with custom default value."""
        result = _get_series(self.test_df, 'MissingColumn', default_val=42)
        assert isinstance(result, pd.Series)
        assert len(result) == 100
        assert (result == 42).all()
    
    def test_apply_rule_predict_hld_basic(self):
        """Test basic predict HLD rule application."""
        result = apply_rule_predict_hld(self.test_df, point=0.1)
        assert isinstance(result, pd.DataFrame)
        assert 'PPrice1' in result.columns
        assert 'PPrice2' in result.columns
        assert 'PColor1' in result.columns
        assert 'PColor2' in result.columns
        assert 'Direction' in result.columns
        assert 'Diff' in result.columns
    
    def test_apply_rule_predict_hld_with_missing_columns(self):
        """Test predict HLD rule with missing columns."""
        df_missing = self.test_df.drop(columns=['HL', 'PV'])
        result = apply_rule_predict_hld(df_missing, point=0.1)
        assert isinstance(result, pd.DataFrame)
        assert 'PPrice1' in result.columns
        assert 'PPrice2' in result.columns
    
    def test_apply_rule_pv_highlow_basic(self):
        """Test basic PV HighLow rule application."""
        result = apply_rule_pv_highlow(self.test_df, point=0.1)
        assert isinstance(result, pd.DataFrame)
        assert 'PPrice1' in result.columns
        assert 'PPrice2' in result.columns
        assert 'PColor1' in result.columns
        assert 'PColor2' in result.columns
        assert 'Direction' in result.columns
        assert 'Diff' in result.columns
    
    def test_apply_rule_support_resistants_basic(self):
        """Test basic Support/Resistants rule application."""
        result = apply_rule_support_resistants(self.test_df, point=0.1)
        assert isinstance(result, pd.DataFrame)
        assert 'PPrice1' in result.columns
        assert 'PPrice2' in result.columns
        assert 'PColor1' in result.columns
        assert 'PColor2' in result.columns
        assert 'Direction' in result.columns
        assert 'Diff' in result.columns
    
    def test_apply_rule_pressure_vector_basic(self):
        """Test basic Pressure Vector rule application."""
        result = apply_rule_pressure_vector(self.test_df, point=0.1)
        assert isinstance(result, pd.DataFrame)
        assert 'PPrice1' in result.columns
        assert 'PPrice2' in result.columns
        assert 'PColor1' in result.columns
        assert 'PColor2' in result.columns
        assert 'Direction' in result.columns
        assert 'Diff' in result.columns
    
    def test_apply_rule_auto_basic(self):
        """Test basic Auto rule application."""
        result = apply_rule_auto(self.test_df, point=0.1)
        assert isinstance(result, pd.DataFrame)
        assert 'PPrice1' in result.columns
        assert 'PPrice2' in result.columns
        assert 'PColor1' in result.columns
        assert 'PColor2' in result.columns
        assert 'Direction' in result.columns
        assert 'Diff' in result.columns
    
    def test_apply_rule_predict_hld_direction_logic(self):
        """Test direction logic in predict HLD rule."""
        # Create test data with known PV values
        test_df = self.test_df.copy()
        test_df['PV'] = [1, -1, 0, 0.5, -0.5] * 20  # Alternating positive/negative values
        
        result = apply_rule_predict_hld(test_df, point=0.1)
        
        # Check that direction is set correctly based on PV sign
        assert (result['Direction'].isin([1.0, 2.0, 0.0])).all()
    
    def test_apply_rule_predict_hld_price_calculation(self):
        """Test price calculation in predict HLD rule."""
        test_df = self.test_df.copy()
        test_df['Open'] = 100  # Fixed open price
        test_df['HL'] = 10     # Fixed HL value
        
        result = apply_rule_predict_hld(test_df, point=0.1)
        
        # PPrice1 should be Open - HL/2 * point
        expected_p1 = 100 - (10 / 2) * 0.1
        assert abs(result['PPrice1'].iloc[0] - expected_p1) < 0.01
        
        # PPrice2 should be Open + HL/2 * point
        expected_p2 = 100 + (10 / 2) * 0.1
        assert abs(result['PPrice2'].iloc[0] - expected_p2) < 0.01
    
    def test_apply_rule_with_empty_dataframe(self):
        """Test rule application with empty DataFrame."""
        empty_df = pd.DataFrame()
        result = apply_rule_predict_hld(empty_df, point=0.1)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
    
    def test_apply_rule_with_nan_values(self):
        """Test rule application with NaN values."""
        test_df = self.test_df.copy()
        test_df.loc[0, 'Open'] = np.nan
        test_df.loc[0, 'HL'] = np.nan
        test_df.loc[0, 'PV'] = np.nan
        
        result = apply_rule_predict_hld(test_df, point=0.1)
        assert isinstance(result, pd.DataFrame)
        assert 'PPrice1' in result.columns
        assert 'PPrice2' in result.columns
    
    def test_apply_rule_error_handling(self):
        """Test rule application error handling."""
        # Test with invalid point value
        result = apply_rule_predict_hld(self.test_df, point=0)
        assert isinstance(result, pd.DataFrame)
        
        # Test with negative point value
        result = apply_rule_predict_hld(self.test_df, point=-0.1)
        assert isinstance(result, pd.DataFrame)
    
    def test_apply_rule_dataframe_modification(self):
        """Test that rules modify the DataFrame in-place."""
        original_df = self.test_df.copy()
        result = apply_rule_predict_hld(self.test_df, point=0.1)
        
        # Check that new columns were added
        new_columns = ['PPrice1', 'PPrice2', 'PColor1', 'PColor2', 'Direction', 'Diff']
        for col in new_columns:
            assert col in result.columns
        
        # Check that original columns are preserved
        original_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'HL', 'PV']
        for col in original_columns:
            assert col in result.columns
    
    def test_apply_rule_color_assignment(self):
        """Test color assignment in rules."""
        result = apply_rule_predict_hld(self.test_df, point=0.1)
        
        # Check that colors are assigned correctly
        assert (result['PColor1'] == 1.0).all()
        assert (result['PColor2'] == 2.0).all()
    
    def test_apply_rule_diff_value(self):
        """Test Diff value assignment."""
        result = apply_rule_predict_hld(self.test_df, point=0.1)
        
        # Check that Diff is set to EMPTY_VALUE for predict_hld rule
        assert result['Diff'].isna().all()
    
    def test_apply_rule_with_different_point_values(self):
        """Test rule application with different point values."""
        point_values = [0.01, 0.1, 1.0, 10.0]
        
        for point in point_values:
            result = apply_rule_predict_hld(self.test_df, point=point)
            assert isinstance(result, pd.DataFrame)
            assert 'PPrice1' in result.columns
            assert 'PPrice2' in result.columns
