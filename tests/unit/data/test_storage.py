"""
Unit tests for data.storage module.
"""

import pytest
import pandas as pd
from unittest.mock import Mock

from src.data.storage.base import BaseDataStorage
from src.core.exceptions import ValidationError, DataError


class MockDataStorage(BaseDataStorage):
    """Mock data storage for testing."""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self._data = {}
        self._writable = True
    
    def store_data(self, data: pd.DataFrame, key: str) -> bool:
        """Mock implementation of store_data."""
        self._data[key] = data
        return True
    
    def load_data(self, key: str) -> pd.DataFrame:
        """Mock implementation of load_data."""
        if key not in self._data:
            raise DataError(f"Data not found for key: {key}")
        return self._data[key]
    
    def is_writable(self) -> bool:
        """Mock implementation of is_writable."""
        return self._writable


class TestBaseDataStorage:
    """Test cases for BaseDataStorage class."""
    
    def test_storage_initialization(self):
        """Test storage initialization."""
        config = {"test": "value"}
        storage = MockDataStorage("test_storage", config)
        
        assert storage.name == "test_storage"
        assert storage.config == config
        assert storage.get_info()["name"] == "test_storage"
    
    def test_abstract_methods(self):
        """Test that required methods are abstract."""
        abstract_methods = BaseDataStorage.__abstractmethods__
        expected_methods = {'store_data', 'load_data', 'is_writable'}
        assert abstract_methods == expected_methods
    
    def test_mock_storage_functionality(self):
        """Test mock storage functionality."""
        storage = MockDataStorage("test", {})
        
        # Test data
        test_data = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })
        
        # Test storing data
        assert storage.store_data(test_data, "test_key") is True
        assert storage.is_writable() is True
        
        # Test loading data
        loaded_data = storage.load_data("test_key")
        pd.testing.assert_frame_equal(loaded_data, test_data)
        
        # Test loading non-existent data
        with pytest.raises(DataError):
            storage.load_data("non_existent_key")


__all__ = ["TestBaseDataStorage"]
