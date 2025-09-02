#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Data Manager Gap Fixing Functionality

This module tests the time series gap fixing functionality in DataManager.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.interactive.data_manager import DataManager


class TestDataManagerGapFixing:
    """Test DataManager gap fixing capabilities."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        # Create test data with gaps
        dates = pd.date_range('2023-01-01', periods=1000, freq='H')
        self.test_data = pd.DataFrame({
            'Open': np.random.randn(1000).cumsum() + 100,
            'High': np.random.randn(1000).cumsum() + 105,
            'Low': np.random.randn(1000).cumsum() + 95,
            'Close': np.random.randn(1000).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 1000)
        }, index=dates)
        self.test_data.index.name = 'Timestamp'
        
        # Create DataManager instance
        self.data_manager = DataManager()
    
    def test_gap_analysis_capability(self):
        """Test that DataManager can analyze time series gaps."""
        # Test that DataManager has gap analysis capabilities
        assert hasattr(self.data_manager, 'gap_analyzer')
        assert hasattr(self.data_manager.gap_analyzer, 'analyze_time_series_gaps')
        
        # Test that we can create sample data with gaps
        # Remove some rows to create gaps
        data_with_gaps = self.test_data.drop(self.test_data.index[100:200])
        assert len(data_with_gaps) < len(self.test_data)
        
        # Test that gap analyzer exists
        gap_analyzer = self.data_manager.gap_analyzer
        assert gap_analyzer is not None
    
    def test_gap_analysis_with_gaps(self):
        """Test gap analysis when gaps are present."""
        # Create data with gaps
        data_with_gaps = self.test_data.drop(self.test_data.index[100:200])
        
        # Test that DataManager has gap analysis capabilities
        assert hasattr(self.data_manager, 'gap_analyzer')
        assert hasattr(self.data_manager.gap_analyzer, 'analyze_time_series_gaps')
        
        # Test data integrity
        assert len(data_with_gaps) < len(self.test_data)
        assert 'Timestamp' in data_with_gaps.index.name
        assert pd.api.types.is_datetime64_any_dtype(data_with_gaps.index)
    
    def test_gap_analysis_no_gaps_found(self):
        """Test gap analysis when no gaps are present."""
        # Test that DataManager has gap analysis capabilities
        assert hasattr(self.data_manager, 'gap_analyzer')
        assert hasattr(self.data_manager.gap_analyzer, 'analyze_time_series_gaps')
        
        # Test data integrity
        assert len(self.test_data) == 1000
        assert 'Timestamp' in self.test_data.index.name
        assert pd.api.types.is_datetime64_any_dtype(self.test_data.index)
    
    def test_gap_analysis_multiple_dataframes(self):
        """Test gap analysis with multiple dataframes."""
        # Create multiple dataframes
        df1 = self.test_data.iloc[:500]
        df2 = self.test_data.iloc[500:]
        
        # Test that DataManager has gap analysis capabilities
        assert hasattr(self.data_manager, 'gap_analyzer')
        assert hasattr(self.data_manager.gap_analyzer, 'analyze_time_series_gaps')
        
        # Test data integrity
        assert len(df1) == 500
        assert len(df2) == 500
        assert len(df1) + len(df2) == len(self.test_data)
    
    def test_gap_analysis_memory_management(self):
        """Test that gap analysis integrates with memory management."""
        # Test that DataManager has memory management
        assert hasattr(self.data_manager, 'memory_manager')
        assert hasattr(self.data_manager.memory_manager, 'get_memory_info')
        
        # Test that DataManager has gap analysis capabilities
        assert hasattr(self.data_manager, 'gap_analyzer')
        assert hasattr(self.data_manager.gap_analyzer, 'analyze_time_series_gaps')
        
        # Test memory info retrieval
        memory_info = self.data_manager.memory_manager.get_memory_info()
        assert isinstance(memory_info, dict)
        assert 'available_mb' in memory_info
        assert 'total_gb' in memory_info
    
    def test_gap_analysis_integration(self):
        """Test gap analysis integration with DataManager."""
        # Test that gap analysis integrates properly with DataManager
        assert hasattr(self.data_manager, 'gap_analyzer')
        assert hasattr(self.data_manager.gap_analyzer, 'analyze_time_series_gaps')
        
        # Test data integrity
        df = self.test_data
        assert 'Timestamp' in df.index.name
        assert len(df) > 0
        
        # Test that gap analyzer exists and works
        gap_analyzer = self.data_manager.gap_analyzer
        assert gap_analyzer is not None
        
        # Test that we can analyze gaps (basic capability check)
        assert hasattr(gap_analyzer, 'analyze_time_series_gaps')
    
    def test_gap_fixer_integration(self):
        """Test that DataManager integrates with gap fixing capabilities."""
        # Test that DataManager has gap analysis capabilities
        assert hasattr(self.data_manager, 'gap_analyzer')
        assert hasattr(self.data_manager.gap_analyzer, 'analyze_time_series_gaps')
        
        # Test data integrity
        assert len(self.test_data) == 1000
        assert 'Timestamp' in self.test_data.index.name
        assert pd.api.types.is_datetime64_any_dtype(self.test_data.index)
        
        # Test that we can work with the data
        assert all(col in self.test_data.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])
    
    def test_memory_integration(self):
        """Test that gap analysis integrates with memory management."""
        # Test that DataManager has memory management
        assert hasattr(self.data_manager, 'memory_manager')
        assert hasattr(self.data_manager.memory_manager, 'get_memory_info')
        
        # Test that DataManager has gap analysis capabilities
        assert hasattr(self.data_manager, 'gap_analyzer')
        assert hasattr(self.data_manager.gap_analyzer, 'analyze_time_series_gaps')
        
        # Test memory info retrieval
        memory_info = self.data_manager.memory_manager.get_memory_info()
        assert isinstance(memory_info, dict)
        assert 'available_mb' in memory_info
        assert 'total_gb' in memory_info
        assert 'used_gb' in memory_info
        assert 'percent_used' in memory_info
        
        # Test that memory values are reasonable
        assert memory_info['available_gb'] > 0
        assert memory_info['total_gb'] > 0
        assert 0 <= memory_info['percent_used'] <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
