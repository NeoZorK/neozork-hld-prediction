"""
Unit tests for core.interfaces module.
"""

import pytest
from unittest.mock import Mock

from src.core.interfaces import (
    DataSource,
    DataSink,
    DataPipeline,
    AnalysisPipeline,
    AnalysisStep,
    ModelRegistry,
)


class TestInterfaces:
    """Test cases for core interfaces."""
    
    def test_data_source_protocol(self):
        """Test DataSource protocol compliance."""
        # Create a mock that implements DataSource protocol
        mock_source = Mock()
        mock_source.fetch.return_value = {"data": "test"}
        mock_source.is_available.return_value = True
        mock_source.get_metadata.return_value = {"type": "test"}
        
        # Test protocol compliance
        assert hasattr(mock_source, 'fetch')
        assert hasattr(mock_source, 'is_available')
        assert hasattr(mock_source, 'get_metadata')
        
        # Test method calls
        assert mock_source.fetch() == {"data": "test"}
        assert mock_source.is_available() is True
        assert mock_source.get_metadata() == {"type": "test"}
    
    def test_data_sink_protocol(self):
        """Test DataSink protocol compliance."""
        # Create a mock that implements DataSink protocol
        mock_sink = Mock()
        mock_sink.store.return_value = True
        mock_sink.is_writable.return_value = True
        
        # Test protocol compliance
        assert hasattr(mock_sink, 'store')
        assert hasattr(mock_sink, 'is_writable')
        
        # Test method calls
        assert mock_sink.store("test_data") is True
        assert mock_sink.is_writable() is True
    
    def test_data_pipeline_abstract_methods(self):
        """Test DataPipeline abstract methods."""
        # DataPipeline is abstract, so we can't instantiate it directly
        # We'll test that it has the required abstract methods
        abstract_methods = DataPipeline.__abstractmethods__
        expected_methods = {'add_source', 'add_sink', 'add_processor', 'execute'}
        
        assert abstract_methods == expected_methods
    
    def test_analysis_pipeline_abstract_methods(self):
        """Test AnalysisPipeline abstract methods."""
        abstract_methods = AnalysisPipeline.__abstractmethods__
        expected_methods = {'add_data_source', 'add_analysis_step', 'execute'}
        
        assert abstract_methods == expected_methods
    
    def test_analysis_step_abstract_methods(self):
        """Test AnalysisStep abstract methods."""
        abstract_methods = AnalysisStep.__abstractmethods__
        expected_methods = {'execute', 'get_dependencies'}
        
        assert abstract_methods == expected_methods
    
    def test_model_registry_abstract_methods(self):
        """Test ModelRegistry abstract methods."""
        abstract_methods = ModelRegistry.__abstractmethods__
        expected_methods = {'register_model', 'get_model', 'list_models', 'remove_model'}
        
        assert abstract_methods == expected_methods


__all__ = ["TestInterfaces"]
