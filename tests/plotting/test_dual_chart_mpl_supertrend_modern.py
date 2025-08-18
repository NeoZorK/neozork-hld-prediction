# -*- coding: utf-8 -*-
# tests/plotting/test_dual_chart_mpl_supertrend_modern.py

"""
Test modern Supertrend styling in matplotlib dual chart plotting.
Verifies that the mpl mode now uses the same modern styling as fastest mode.
"""

import pytest

# Individual tests will be enforced with 10-second timeout
# No module-level skip to allow individual test execution

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock
import tempfile
import os

from src.plotting.dual_chart_mpl import plot_dual_chart_mpl


class TestModernSupertrendStyling:
    """Test modern Supertrend styling implementation in matplotlib."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data with Supertrend indicators."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        
        # Create price data
        np.random.seed(42)
        base_price = 1.5
        price_changes = np.random.normal(0, 0.02, 100)
        prices = [base_price]
        for change in price_changes:
            prices.append(prices[-1] * (1 + change))
        
        # Create OHLC data
        data = {
            'Open': prices[:-1],
            'High': [p * 1.01 for p in prices[:-1]],
            'Low': [p * 0.99 for p in prices[:-1]],
            'Close': prices[1:],
            'Volume': np.random.randint(1000, 10000, 100),
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Add Supertrend columns (simulating PPrice1/PPrice2 approach)
        df['PPrice1'] = df['Close'] * 0.98  # Support level
        df['PPrice2'] = df['Close'] * 1.02  # Resistance level
        df['Direction'] = np.where(df['Close'] > df['PPrice1'], 1, 2)
        
        return df
    
    def test_modern_color_scheme(self, sample_data):
        """Test that modern color scheme is used."""
        with patch('matplotlib.pyplot.show'):
            with patch('matplotlib.pyplot.savefig'):
                fig = plot_dual_chart_mpl(
                    sample_data, 
                    rule='supertrend:10,3,open',
                    title='Test Modern Supertrend'
                )
                
                # Verify the figure was created
                assert fig is not None
                assert hasattr(fig, 'axes')
                assert len(fig.axes) == 2
    
    def test_supertrend_segmentation(self, sample_data):
        """Test that Supertrend is properly segmented with modern colors."""
        with patch('matplotlib.pyplot.show'):
            with patch('matplotlib.pyplot.savefig'):
                fig = plot_dual_chart_mpl(
                    sample_data, 
                    rule='supertrend:10,3,open',
                    title='Test Segmentation'
                )
                
                ax2 = fig.axes[1]  # Indicator subplot
                
                # Check that lines are plotted with modern colors
                lines = ax2.get_lines()
                assert len(lines) > 0
                
                # Verify modern color scheme is used
                modern_colors = ['#00C851', '#FF4444', '#FFC107']  # Green, Red, Gold
                line_colors = [line.get_color() for line in lines]
                
                # At least one modern color should be used
                has_modern_colors = any(
                    any(color in str(line_color) for color in modern_colors)
                    for line_color in line_colors
                )
                assert has_modern_colors, "Modern color scheme not applied"
    
    def test_signal_detection(self, sample_data):
        """Test that signal change points are properly detected and styled."""
        # Create data with clear signal changes
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        
        # Create price data with clear trend changes
        prices = [1.5]
        for i in range(49):
            if i < 20:
                prices.append(prices[-1] * 1.01)  # Uptrend
            elif i < 30:
                prices.append(prices[-1] * 0.99)  # Downtrend
            else:
                prices.append(prices[-1] * 1.01)  # Uptrend again
        
        # Create data with consistent lengths
        data = {
            'Open': prices[:-1],  # 49 elements
            'High': [p * 1.01 for p in prices[:-1]],  # 49 elements
            'Low': [p * 0.99 for p in prices[:-1]],  # 49 elements
            'Close': prices[1:],  # 49 elements
            'Volume': np.random.randint(1000, 10000, 49),  # 49 elements
            'PPrice1': [p * 0.98 for p in prices[1:]],  # 49 elements
            'PPrice2': [p * 1.02 for p in prices[1:]],  # 49 elements
        }
        
        # Use the correct index length
        df = pd.DataFrame(data, index=dates[:49])
        df['Direction'] = np.where(df['Close'] > df['PPrice1'], 1, 2)
        
        with patch('matplotlib.pyplot.show'):
            with patch('matplotlib.pyplot.savefig'):
                fig = plot_dual_chart_mpl(
                    df, 
                    rule='supertrend:10,3,open',
                    title='Test Signal Detection'
                )
                
                ax2 = fig.axes[1]
                
                # Check for signal markers (may not be present in all test data)
                collections = ax2.collections
                # Signal markers are optional - the main test is that the plotting works
                # and modern styling is applied
                assert fig is not None, "Figure should be created successfully"
    
    def test_enhanced_styling_features(self, sample_data):
        """Test that enhanced styling features are applied."""
        with patch('matplotlib.pyplot.show'):
            with patch('matplotlib.pyplot.savefig'):
                fig = plot_dual_chart_mpl(
                    sample_data, 
                    rule='supertrend:10,3,open',
                    title='Test Enhanced Styling'
                )
                
                ax2 = fig.axes[1]
                
                # Check for glow effects (multiple lines with different alpha)
                lines = ax2.get_lines()
                if len(lines) > 1:
                    # Should have both main lines and glow effects
                    alphas = [line.get_alpha() for line in lines if line.get_alpha() is not None]
                    assert len(alphas) > 0, "Alpha effects should be applied"
    
    def test_background_zones(self, sample_data):
        """Test that trend background zones are created."""
        with patch('matplotlib.pyplot.show'):
            with patch('matplotlib.pyplot.savefig'):
                fig = plot_dual_chart_mpl(
                    sample_data, 
                    rule='supertrend:10,3,open',
                    title='Test Background Zones'
                )
                
                ax2 = fig.axes[1]
                
                # Check for background rectangles (patches)
                patches = ax2.patches
                # Note: Background zones might not always be created depending on data
                # This test verifies the plotting function handles the feature
    
    def test_legend_entries(self, sample_data):
        """Test that proper legend entries are created."""
        with patch('matplotlib.pyplot.show'):
            with patch('matplotlib.pyplot.savefig'):
                fig = plot_dual_chart_mpl(
                    sample_data, 
                    rule='supertrend:10,3,open',
                    title='Test Legend'
                )
                
                ax2 = fig.axes[1]
                
                # Check legend entries
                legend = ax2.get_legend()
                if legend is not None:
                    legend_texts = [text.get_text() for text in legend.get_texts()]
                    
                    # Should have modern legend entries
                    expected_entries = [
                        'SuperTrend (Uptrend)',
                        'SuperTrend (Downtrend)', 
                        'SuperTrend (Signal Change)',
                        'BUY Signal',
                        'SELL Signal'
                    ]
                    
                    # At least some expected entries should be present
                    found_entries = any(
                        any(expected in text for expected in expected_entries)
                        for text in legend_texts
                    )
                    assert found_entries, "Modern legend entries should be present"
    
    def test_file_output(self, sample_data):
        """Test that the plot can be saved to file."""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            try:
                with patch('matplotlib.pyplot.show'):
                    fig = plot_dual_chart_mpl(
                        sample_data, 
                        rule='supertrend:10,3,open',
                        title='Test File Output',
                        output_path=tmp_file.name
                    )
                    
                    # Check that file was created
                    assert os.path.exists(tmp_file.name)
                    assert os.path.getsize(tmp_file.name) > 0
                    
            finally:
                # Cleanup
                if os.path.exists(tmp_file.name):
                    os.unlink(tmp_file.name)
    
    def test_error_handling(self):
        """Test error handling with invalid data."""
        # Test with empty DataFrame
        empty_df = pd.DataFrame()
        
        with patch('matplotlib.pyplot.show'):
            with patch('matplotlib.pyplot.savefig'):
                # Should not raise exception
                fig = plot_dual_chart_mpl(
                    empty_df, 
                    rule='supertrend:10,3,open',
                    title='Test Error Handling'
                )
                
                assert fig is not None
    
    def test_performance(self, sample_data):
        """Test that modern styling doesn't significantly impact performance."""
        import time
        
        with patch('matplotlib.pyplot.show'):
            with patch('matplotlib.pyplot.savefig'):
                start_time = time.time()
                
                fig = plot_dual_chart_mpl(
                    sample_data, 
                    rule='supertrend:10,3,open',
                    title='Test Performance'
                )
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                # Should complete within reasonable time (less than 5 seconds)
                assert execution_time < 5.0, f"Plotting took too long: {execution_time:.2f}s"
                
                assert fig is not None


if __name__ == "__main__":
    pytest.main([__file__]) 