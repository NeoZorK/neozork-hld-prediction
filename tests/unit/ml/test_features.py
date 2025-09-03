"""
Unit tests for ml.features module.
"""

import pytest
import pandas as pd
from typing import Dict, Any, List
from unittest.mock import Mock

from src.ml.features.base import BaseFeatureEngineer, TechnicalFeatures
from src.core.exceptions import ValidationError, DataError


class MockFeatureEngineer(BaseFeatureEngineer):
    """Mock feature engineer for testing."""
    
    def create_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Mock implementation of create_features."""
        result = data.copy()
        result['feature_1'] = data.iloc[:, 0] * 2
        return result
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Mock implementation of transform."""
        return self.create_features(data)


class TestBaseFeatureEngineer:
    """Test cases for BaseFeatureEngineer class."""
    
    def test_feature_engineer_initialization(self):
        """Test feature engineer initialization."""
        config = {"test": "value"}
        engineer = MockFeatureEngineer("test_engineer", config)
        
        assert engineer.name == "test_engineer"
        assert engineer.config == config
        assert isinstance(engineer, BaseFeatureEngineer)
    
    def test_base_feature_engineer_abstract_method(self):
        """Test that BaseFeatureEngineer is abstract."""
        abstract_methods = BaseFeatureEngineer.__abstractmethods__
        assert 'transform' in abstract_methods


class TestTechnicalFeatures:
    """Test cases for TechnicalFeatures class."""
    
    def test_technical_features_initialization(self):
        """Test technical features initialization."""
        config = {"test": "value"}
        features = TechnicalFeatures(config)
        
        assert features.config == config
        assert isinstance(features, TechnicalFeatures)
    
    def test_create_technical_features(self):
        """Test technical features creation."""
        features = TechnicalFeatures({})
        
        # Test with sample OHLCV data
        test_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [95, 96, 97, 98, 99],
            'close': [102, 103, 104, 105, 106],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        result = features.create_features(test_data)
        
        # Should have original columns plus new features
        assert 'open' in result.columns
        assert 'high' in result.columns
        assert 'low' in result.columns
        assert 'close' in result.columns
        assert 'volume' in result.columns
        # Should have some technical features
        assert len(result.columns) > 5


__all__ = ["TestBaseFeatureEngineer", "TestTechnicalFeatures"]
