"""
Test module for mplfinance plotting with different rules.

This module tests the functionality of mplfinance plotting with various rules
to ensure that charts are generated correctly without dimension mismatch errors.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from plotting.mplfinance_plot import plot_indicator_results_mplfinance


class TestMplfinanceRules:
    """Test class for mplfinance plotting with different rules."""
    
    def sample_data(self):
        """Create sample OHLCV data for testing."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        # Generate realistic OHLCV data
        base_price = 1.5000
        returns = np.random.normal(0, 0.01, 100)
        prices = [base_price]
        
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        data = []
        for i, price in enumerate(prices):
            high = price * (1 + abs(np.random.normal(0, 0.005)))
            low = price * (1 - abs(np.random.normal(0, 0.005)))
            open_price = prices[i-1] if i > 0 else price
            close = price
            volume = np.random.randint(10000, 100000)
            
            data.append({
                'Open': open_price,
                'High': high,
                'Low': low,
                'Close': close,
                'Volume': volume
            })
        
        df = pd.DataFrame(data, index=dates)
        return df
    
    def sample_data_with_indicators(self):
        """Create sample data with indicator columns."""
        df = self.sample_data()
        
        # Add indicator columns
        df['PPrice1'] = df['Close'] * 0.98
        df['PPrice2'] = df['Close'] * 1.02
        df['Direction'] = np.random.choice([0, 1, 2], size=len(df))
        df['PColor1'] = np.random.choice([1, 2], size=len(df))
        df['PColor2'] = np.random.choice([1, 2], size=len(df))
        df['Pressure'] = np.random.normal(1000, 500, len(df))
        df['PV'] = np.random.normal(0, 100, len(df))
        df['HL'] = df['High'] - df['Low']
        
        return df
    
    @patch('plotting.mplfinance_plot.mpf.plot')
    def test_plot_mplfinance_auto_rule(self, mock_plot):
        """Test mplfinance plotting with AUTO rule."""
        # Mock the mpf.plot function
        mock_plot.return_value = None
        
        # Test AUTO rule
        sample_data = self.sample_data()
        result = plot_indicator_results_mplfinance(sample_data, rule="AUTO", title="Test AUTO Rule")
        
        # Verify that mpf.plot was called
        mock_plot.assert_called_once()
        
        # Check that the call was made with correct parameters
        call_args = mock_plot.call_args
        assert call_args[0][0].equals(sample_data)  # First argument should be the dataframe
        assert call_args[1]['title'] == "Test AUTO Rule"
    
    @patch('plotting.mplfinance_plot.mpf.plot')
    def test_plot_mplfinance_phld_rule(self, mock_plot):
        """Test mplfinance plotting with PHLD rule."""
        # Mock the mpf.plot function
        mock_plot.return_value = None
        
        # Test PHLD rule
        sample_data_with_indicators = self.sample_data_with_indicators()
        result = plot_indicator_results_mplfinance(sample_data_with_indicators, rule="PHLD", title="Test PHLD Rule")
        
        # Verify that mpf.plot was called
        mock_plot.assert_called_once()
        
        # Check that the call was made with correct parameters
        call_args = mock_plot.call_args
        assert call_args[0][0].equals(sample_data_with_indicators)
        assert call_args[1]['title'] == "Test PHLD Rule"
    
    @patch('plotting.mplfinance_plot.mpf.plot')
    def test_plot_mplfinance_pv_rule(self, mock_plot):
        """Test mplfinance plotting with PV rule."""
        # Mock the mpf.plot function
        mock_plot.return_value = None
        
        # Test PV rule
        sample_data_with_indicators = self.sample_data_with_indicators()
        result = plot_indicator_results_mplfinance(sample_data_with_indicators, rule="PV", title="Test PV Rule")
        
        # Verify that mpf.plot was called
        mock_plot.assert_called_once()
        
        # Check that the call was made with correct parameters
        call_args = mock_plot.call_args
        assert call_args[0][0].equals(sample_data_with_indicators)
        assert call_args[1]['title'] == "Test PV Rule"
    
    @patch('plotting.mplfinance_plot.mpf.plot')
    def test_plot_mplfinance_sr_rule(self, mock_plot):
        """Test mplfinance plotting with SR rule."""
        # Mock the mpf.plot function
        mock_plot.return_value = None
        
        # Test SR rule
        sample_data_with_indicators = self.sample_data_with_indicators()
        result = plot_indicator_results_mplfinance(sample_data_with_indicators, rule="SR", title="Test SR Rule")
        
        # Verify that mpf.plot was called
        mock_plot.assert_called_once()
        
        # Check that the call was made with correct parameters
        call_args = mock_plot.call_args
        assert call_args[0][0].equals(sample_data_with_indicators)
        assert call_args[1]['title'] == "Test SR Rule"
    
    @patch('plotting.mplfinance_plot.mpf.plot')
    def test_plot_mplfinance_no_dimension_mismatch(self, mock_plot):
        """Test that plotting handles dimension mismatch errors gracefully."""
        # Mock the mpf.plot function to raise a dimension mismatch error
        mock_plot.side_effect = ValueError("x and y must have same first dimension")
        
        # Test that the function handles the error gracefully
        sample_data_with_indicators = self.sample_data_with_indicators()
        result = plot_indicator_results_mplfinance(sample_data_with_indicators, rule="PHLD", title="Test Error Handling")
        
        # Should return None when error occurs
        assert result is None
    
    def test_plot_mplfinance_dataframe_validation(self):
        """Test that the function validates input dataframe."""
        # Test with empty dataframe - should return early with warning
        empty_df = pd.DataFrame()
        result = plot_indicator_results_mplfinance(empty_df, rule="AUTO", title="Test Empty")
        assert result is None  # Should return None for empty dataframe
        
        # Test with missing required columns - should return early with warning
        sample_data = self.sample_data()
        incomplete_df = sample_data.drop(columns=['Open', 'High', 'Low', 'Close'])
        result = plot_indicator_results_mplfinance(incomplete_df, rule="AUTO", title="Test Incomplete")
        assert result is None  # Should return None for incomplete dataframe
    
    @patch('plotting.mplfinance_plot.mpf.plot')
    def test_plot_mplfinance_addplot_creation(self, mock_plot):
        """Test that addplot items are created correctly without dimension mismatches."""
        # Mock the mpf.plot function
        mock_plot.return_value = None
        
        # Test with PHLD rule which should create multiple addplot items
        sample_data_with_indicators = self.sample_data_with_indicators()
        result = plot_indicator_results_mplfinance(sample_data_with_indicators, rule="PHLD", title="Test Addplot")
        
        # Verify that mpf.plot was called
        mock_plot.assert_called_once()
        
        # Check that addplot parameter exists and is a list
        call_args = mock_plot.call_args
        assert 'addplot' in call_args[1]
        addplot_items = call_args[1]['addplot']
        assert isinstance(addplot_items, list)
        
        # Verify that all addplot items have consistent dimensions
        for item in addplot_items:
            if hasattr(item, 'data'):
                # Check that data has consistent dimensions
                assert len(item.data) == len(sample_data_with_indicators)
    
    def test_plot_mplfinance_rule_parameter_handling(self):
        """Test that different rule parameters are handled correctly."""
        # Test with rule object
        class MockRule:
            def __init__(self, name):
                self.name = name
        
        rule_obj = MockRule("TEST_RULE")
        sample_data = self.sample_data()
        
        with patch('plotting.mplfinance_plot.mpf.plot') as mock_plot:
            mock_plot.return_value = None
            result = plot_indicator_results_mplfinance(sample_data, rule=rule_obj, title="Test Rule Object")
            
            # Verify that the rule name was extracted correctly
            call_args = mock_plot.call_args
            assert call_args[1]['title'] == "Test Rule Object"
    
    @patch('plotting.mplfinance_plot.mpf.plot')
    def test_plot_mplfinance_volume_handling(self, mock_plot):
        """Test that volume is handled correctly in plotting."""
        # Mock the mpf.plot function
        mock_plot.return_value = None
        
        # Test with volume
        sample_data = self.sample_data()
        result = plot_indicator_results_mplfinance(sample_data, rule="AUTO", title="Test Volume")
        
        # Verify that mpf.plot was called
        mock_plot.assert_called_once()
        
        # Check that volume parameter is set correctly
        call_args = mock_plot.call_args
        assert 'volume' in call_args[1]
        assert call_args[1]['volume'] is True  # Should be True since Volume column exists
    
    @patch('plotting.mplfinance_plot.mpf.plot')
    def test_plot_mplfinance_no_volume(self, mock_plot):
        """Test plotting without volume column."""
        # Create data without volume
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        data = pd.DataFrame({
            'Open': np.random.uniform(1.4, 1.6, 50),
            'High': np.random.uniform(1.5, 1.7, 50),
            'Low': np.random.uniform(1.3, 1.5, 50),
            'Close': np.random.uniform(1.4, 1.6, 50)
        }, index=dates)
        
        # Mock the mpf.plot function
        mock_plot.return_value = None
        
        # Test without volume
        result = plot_indicator_results_mplfinance(data, rule="AUTO", title="Test No Volume")
        
        # Verify that mpf.plot was called
        mock_plot.assert_called_once()
        
        # Check that volume parameter is set correctly
        call_args = mock_plot.call_args
        assert 'volume' in call_args[1]
        assert call_args[1]['volume'] is False  # Should be False since no Volume column


if __name__ == "__main__":
    pytest.main([__file__])
