# -*- coding: utf-8 -*-
"""
Tests for Data Management of NeoZork Interactive ML Trading Strategy Development.

This module contains tests for the data management components.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from interactive.data_management import DataLoader, DataValidator, DataProcessor

class TestDataLoader:
    """Test cases for DataLoader."""
    
    def test_data_loader_initialization(self):
        """Test data loader initialization."""
        loader = DataLoader()
        assert loader is not None
        assert hasattr(loader, 'project_root')
        assert hasattr(loader, 'data_root')
    
    def test_get_available_data_sources(self):
        """Test getting available data sources."""
        loader = DataLoader()
        sources = loader.get_available_data_sources()
        assert isinstance(sources, dict)
        assert 'csv_converted' in sources
        assert 'raw_parquet' in sources
        assert 'indicators' in sources
        assert 'cleaned_data' in sources

class TestDataValidator:
    """Test cases for DataValidator."""
    
    def test_data_validator_initialization(self):
        """Test data validator initialization."""
        validator = DataValidator()
        assert validator is not None
        assert hasattr(validator, 'validation_rules')
        assert hasattr(validator, 'quality_metrics')

class TestDataProcessor:
    """Test cases for DataProcessor."""
    
    def test_data_processor_initialization(self):
        """Test data processor initialization."""
        processor = DataProcessor()
        assert processor is not None
        assert hasattr(processor, 'processing_pipeline')
        assert hasattr(processor, 'transformation_rules')

if __name__ == "__main__":
    pytest.main([__file__])
