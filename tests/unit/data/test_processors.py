"""
Unit tests for data.processors module.
"""

import pytest
import pandas as pd
from typing import Any
from unittest.mock import Mock

from src.data.processors.base import BaseDataProcessor
from src.core.exceptions import ValidationError, DataError


class MockDataProcessor(BaseDataProcessor):
    """Mock data processor for testing."""
    
    def process_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Mock implementation of process_data."""
        # Simple transformation: add a new column
        result = data.copy()
        result['processed'] = True
        return result
    
    def process(self, data: Any) -> Any:
        """Mock implementation of process method from core.base.DataProcessor."""
        return self.process_data(data)
    
    def validate_input(self, data: Any) -> bool:
        """Mock implementation of validate_input method from core.base.DataProcessor."""
        return data is not None and not data.empty if hasattr(data, 'empty') else data is not None


class TestBaseDataProcessor:
    """Test cases for BaseDataProcessor class."""
    
    def test_processor_initialization(self):
        """Test processor initialization."""
        config = {"test": "value"}
        processor = MockDataProcessor("test_processor", config)
        
        assert processor.name == "test_processor"
        assert processor.config == config
        assert isinstance(processor, BaseDataProcessor)
    
    def test_process_data_abstract_method(self):
        """Test that process_data is abstract."""
        # BaseDataProcessor is abstract, can't instantiate directly
        abstract_methods = BaseDataProcessor.__abstractmethods__
        assert 'process_data' in abstract_methods
    
    def test_mock_processor_functionality(self):
        """Test mock processor functionality."""
        processor = MockDataProcessor("test", {})
        
        # Test with sample data
        test_data = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })
        
        result = processor.process_data(test_data)
        
        # Should have original columns plus 'processed'
        assert 'A' in result.columns
        assert 'B' in result.columns
        assert 'processed' in result.columns
        assert all(result['processed'] == True)


__all__ = ["TestBaseDataProcessor"]
