#!/usr/bin/env python3
"""
Test module for fastest_auto_plot.py
Tests the vertical scrollbar functionality for AUTO mode charts.
"""

import pytest
import pandas as pd
import numpy as np
import os
import tempfile
from pathlib import Path
import sys
import re

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.plotting.fastest_auto_plot import plot_auto_fastest_parquet


class TestFastestAutoPlot:
    """Test class for fastest_auto_plot.py functionality."""

    def setup_method(self):
        """Set up test data and temporary files."""
        # Create test data with multiple numeric columns
        dates = pd.date_range('2024-01-01', periods=100, freq='h')
        self.test_data = pd.DataFrame({
            'DateTime': dates,
            'Open': np.random.rand(100) * 100 + 100,
            'High': np.random.rand(100) * 100 + 150,
            'Low': np.random.rand(100) * 100 + 50,
            'Close': np.random.rand(100) * 100 + 100,
            'Volume': np.random.randint(1000, 10000, size=100),
            'RSI': np.random.rand(100) * 100,
            'MACD': np.random.randn(100) * 2,
            'EMA': np.random.rand(100) * 100 + 100,
            'BB_Upper': np.random.rand(100) * 100 + 120,
            'BB_Lower': np.random.rand(100) * 100 + 80,
            'ATR': np.random.rand(100) * 5,
            'Stochastic': np.random.rand(100) * 100,
            'CCI': np.random.randn(100) * 100,
            'ADX': np.random.rand(100) * 100,
            'OBV': np.random.randint(1000000, 10000000, size=100),
            'VWAP': np.random.rand(100) * 100 + 100,
            'Pressure': np.random.randn(100) * 1.5,
            'PV': np.random.randn(100) * 2,
            'HL': np.random.rand(100) * 10,
            'Direction': np.random.choice([1, 2], size=100, p=[0.5, 0.5]),
            'PPrice1': np.random.rand(100) * 100 + 80,
            'PPrice2': np.random.rand(100) * 100 + 120,
        })
        
        # Create temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.test_parquet_path = os.path.join(self.temp_dir, "test_data.parquet")
        self.test_data.to_parquet(self.test_parquet_path)
        
        # Output path for test plot
        self.output_html_path = os.path.join(self.temp_dir, "test_auto_plot.html")

    def teardown_method(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_plot_auto_fastest_parquet_basic_functionality(self):
        """Test basic functionality of plot_auto_fastest_parquet."""
        # Test that the function runs without errors
        fig = plot_auto_fastest_parquet(
            parquet_path=self.test_parquet_path,
            output_html_path=self.output_html_path,
            trading_rule_name="AUTO",
            title="Test AUTO Plot"
        )
        
        # Check that the figure was created
        assert fig is not None
        
        # Check that HTML file was created
        assert os.path.exists(self.output_html_path)
        
        # Check HTML file content
        with open(self.output_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Verify vertical scrollbar CSS is present
        assert 'overflow-y: auto' in html_content
        assert '.chart-container' in html_content
        assert '::-webkit-scrollbar' in html_content
        
        # Verify AUTO mode specific content
        assert 'AUTO Mode with Vertical Scrollbar' in html_content
        assert 'Trading Rule: AUTO' in html_content

    def test_plot_auto_fastest_parquet_with_different_columns(self):
        """Test plotting with different column combinations."""
        # Create data with only some columns
        limited_data = self.test_data[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'RSI', 'MACD']]
        limited_parquet_path = os.path.join(self.temp_dir, "limited_data.parquet")
        limited_data.to_parquet(limited_parquet_path)
        
        output_path = os.path.join(self.temp_dir, "limited_auto_plot.html")
        
        fig = plot_auto_fastest_parquet(
            parquet_path=limited_parquet_path,
            output_html_path=output_path,
            trading_rule_name="AUTO",
            title="Limited Columns Test"
        )
        
        assert fig is not None
        assert os.path.exists(output_path)
        
        # Check HTML content
        with open(output_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Should still have scrollbar functionality
        assert 'overflow-y: auto' in html_content
        assert 'RSI, MACD' in html_content

    def test_plot_auto_fastest_parquet_with_datetime_index(self):
        """Test plotting with DatetimeIndex instead of DateTime column."""
        # Create data with DatetimeIndex
        indexed_data = self.test_data.set_index('DateTime')
        indexed_parquet_path = os.path.join(self.temp_dir, "indexed_data.parquet")
        indexed_data.to_parquet(indexed_parquet_path)
        
        output_path = os.path.join(self.temp_dir, "indexed_auto_plot.html")
        
        fig = plot_auto_fastest_parquet(
            parquet_path=indexed_parquet_path,
            output_html_path=output_path,
            trading_rule_name="AUTO",
            title="DatetimeIndex Test"
        )
        
        assert fig is not None
        assert os.path.exists(output_path)

    def test_plot_auto_fastest_parquet_scrollbar_css(self):
        """Test that scrollbar CSS properties are correctly applied."""
        fig = plot_auto_fastest_parquet(
            parquet_path=self.test_parquet_path,
            output_html_path=self.output_html_path,
            trading_rule_name="AUTO",
            title="Scrollbar CSS Test"
        )
        
        with open(self.output_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check for all required scrollbar CSS properties
        scrollbar_properties = [
            'overflow-y: auto',
            '::-webkit-scrollbar',
            '::-webkit-scrollbar-track',
            '::-webkit-scrollbar-thumb',
            '::-webkit-scrollbar-thumb:hover',
        ]
        
        for prop in scrollbar_properties:
            assert prop in html_content, f"Missing scrollbar property: {prop}"
        
        # Проверяем, что в html_content есть строка height: <число>px;
        assert re.search(r'height: ?\d+px;', html_content), 'Missing dynamic height property in .chart-container'

    def test_plot_auto_fastest_parquet_info_panel(self):
        """Test that the info panel shows correct information."""
        fig = plot_auto_fastest_parquet(
            parquet_path=self.test_parquet_path,
            output_html_path=self.output_html_path,
            trading_rule_name="AUTO",
            title="Info Panel Test"
        )
        
        with open(self.output_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check for info panel content
        assert 'Chart Information:' in html_content
        assert 'Total panels:' in html_content
        assert 'Data points:' in html_content
        assert 'Columns displayed:' in html_content
        assert 'Use the vertical scrollbar' in html_content

    def test_plot_auto_fastest_parquet_error_handling(self):
        """Test error handling for invalid parquet files."""
        # Test with non-existent file
        with pytest.raises(FileNotFoundError):
            plot_auto_fastest_parquet(
                parquet_path="non_existent_file.parquet",
                output_html_path=self.output_html_path,
                trading_rule_name="AUTO"
            )

    def test_plot_auto_fastest_parquet_no_numeric_columns(self):
        """Test handling of parquet files with no numeric columns."""
        # Create data with only string columns
        string_data = pd.DataFrame({
            'DateTime': pd.date_range('2024-01-01', periods=10, freq='h'),
            'Symbol': ['AAPL'] * 10,
            'Exchange': ['NASDAQ'] * 10,
            'Description': ['Apple Inc'] * 10
        })
        
        string_parquet_path = os.path.join(self.temp_dir, "string_data.parquet")
        string_data.to_parquet(string_parquet_path)
        
        output_path = os.path.join(self.temp_dir, "string_auto_plot.html")
        
        # Should raise ValueError for no numeric columns
        with pytest.raises(ValueError, match="No numeric columns to plot"):
            plot_auto_fastest_parquet(
                parquet_path=string_parquet_path,
                output_html_path=output_path,
                trading_rule_name="AUTO"
            )

    def test_plot_auto_fastest_parquet_no_time_column(self):
        """Test handling of parquet files with no time column."""
        # Create data without time column and without DatetimeIndex
        no_time_data = pd.DataFrame({
            'Open': np.random.rand(10) * 100,
            'High': np.random.rand(10) * 100,
            'Low': np.random.rand(10) * 100,
            'Close': np.random.rand(10) * 100,
            'Volume': np.random.randint(1000, 10000, size=10),
            'RSI': np.random.rand(10) * 100
        })
        
        no_time_parquet_path = os.path.join(self.temp_dir, "no_time_data.parquet")
        no_time_data.to_parquet(no_time_parquet_path)
        
        output_path = os.path.join(self.temp_dir, "no_time_auto_plot.html")
        
        # Should raise ValueError for no time column
        with pytest.raises(ValueError, match="No time column found"):
            plot_auto_fastest_parquet(
                parquet_path=no_time_parquet_path,
                output_html_path=output_path,
                trading_rule_name="AUTO"
            )


if __name__ == "__main__":
    pytest.main([__file__])

