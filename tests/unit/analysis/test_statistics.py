"""
Unit tests for analysis.statistics module.
"""

import pytest
import pandas as pd
from typing import Dict, Any
from unittest.mock import Mock

from src.analysis.statistics.base import BaseStatistic, DescriptiveStatistics
from src.core.exceptions import ValidationError, DataError


class MockStatistic(BaseStatistic):
    """Mock statistic for testing."""
    
    def calculate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Mock implementation of calculate."""
        return {"mock_result": len(data)}


class TestBaseStatistic:
    """Test cases for BaseStatistic class."""
    
    def test_statistic_initialization(self):
        """Test statistic initialization."""
        config = {"test": "value"}
        statistic = MockStatistic("test_statistic", config)
        
        assert statistic.name == "test_statistic"
        assert statistic.config == config
        assert isinstance(statistic, BaseStatistic)
    
    def test_base_statistic_abstract_method(self):
        """Test that BaseStatistic is abstract."""
        abstract_methods = BaseStatistic.__abstractmethods__
        assert 'calculate' in abstract_methods


class TestDescriptiveStatistics:
    """Test cases for DescriptiveStatistics class."""
    
    def test_descriptive_statistics_initialization(self):
        """Test descriptive statistics initialization."""
        config = {"test": "value"}
        stats = DescriptiveStatistics(config)
        
        assert stats.config == config
        assert isinstance(stats, DescriptiveStatistics)
    
    def test_calculate_descriptive_statistics(self):
        """Test descriptive statistics calculation."""
        stats = DescriptiveStatistics({})
        
        # Test with sample data
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50]
        })
        
        result = stats.calculate(test_data)
        
        # Should have basic statistics
        assert 'count' in result
        assert 'mean' in result
        assert 'std' in result
        assert result['count'] == 5


__all__ = ["TestBaseStatistic", "TestDescriptiveStatistics"]
