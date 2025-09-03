"""
Unit tests for base classes in core module.

This module tests the fundamental base classes and abstract interfaces.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from unittest.mock import Mock, patch

from src.core.base import (
    BaseComponent, 
    DataProcessor, 
    AnalysisEngine, 
    MLModel, 
    Exportable
)


class TestBaseComponent:
    """Test cases for BaseComponent class."""
    
    def test_init(self):
        """Test BaseComponent initialization."""
        component = BaseComponent("test_component")
        
        assert component.name == "test_component"
        assert component.config == {}
        assert component.created_at is not None
        assert component.logger is not None
    
    def test_init_with_config(self):
        """Test BaseComponent initialization with config."""
        config = {"param1": "value1", "param2": 42}
        component = BaseComponent("test_component", config)
        
        assert component.config == config
    
    def test_str_representation(self):
        """Test string representation."""
        component = BaseComponent("test_component")
        expected = "BaseComponent(test_component)"
        
        assert str(component) == expected
    
    def test_repr_representation(self):
        """Test repr representation."""
        component = BaseComponent("test_component")
        expected = "BaseComponent(test_component)"
        
        assert repr(component) == expected


class TestDataProcessor:
    """Test cases for DataProcessor class."""
    
    def test_init(self):
        """Test DataProcessor initialization."""
        # DataProcessor is abstract, test that it can't be instantiated
        with pytest.raises(TypeError):
            DataProcessor("test_processor")
    
    def test_abstract_methods(self):
        """Test that abstract methods are properly defined."""
        # Should not be able to instantiate abstract class
        with pytest.raises(TypeError):
            DataProcessor("test")


class TestAnalysisEngine:
    """Test cases for AnalysisEngine class."""
    
    def test_init(self):
        """Test AnalysisEngine initialization."""
        # AnalysisEngine is abstract, test that it can't be instantiated
        with pytest.raises(TypeError):
            AnalysisEngine("test_engine")
    
    def test_abstract_methods(self):
        """Test that abstract methods are properly defined."""
        # Should not be able to instantiate abstract class
        with pytest.raises(TypeError):
            AnalysisEngine("test")


class TestMLModel:
    """Test cases for MLModel class."""
    
    def test_init(self):
        """Test MLModel initialization."""
        model = MLModel("test_model")
        
        assert model.name == "test_model"
        assert isinstance(model, BaseComponent)
    
    def test_abstract_methods(self):
        """Test that abstract methods are properly defined."""
        # Should not be able to instantiate abstract class
        with pytest.raises(TypeError):
            MLModel("test")


class TestExportable:
    """Test cases for Exportable class."""
    
    def test_init(self):
        """Test Exportable initialization."""
        exportable = Exportable("test_exportable")
        
        assert exportable.name == "test_exportable"
        assert isinstance(exportable, BaseComponent)
    
    def test_abstract_methods(self):
        """Test that abstract methods are properly defined."""
        # Should not be able to instantiate abstract class
        with pytest.raises(TypeError):
            Exportable("test")


class TestComponentIntegration:
    """Test cases for component integration."""
    
    def test_component_hierarchy(self):
        """Test that components properly inherit from BaseComponent."""
        # All components should inherit from BaseComponent
        assert issubclass(DataProcessor, BaseComponent)
        assert issubclass(AnalysisEngine, BaseComponent)
        assert issubclass(MLModel, BaseComponent)
        assert issubclass(Exportable, BaseComponent)
    
    def test_component_creation_timestamp(self):
        """Test that components get creation timestamps."""
        before = datetime.now()
        component = BaseComponent("test")
        after = datetime.now()
        
        assert before <= component.created_at <= after
    
    def test_component_logging(self):
        """Test that components have proper logging setup."""
        component = BaseComponent("test")
        
        assert component.logger is not None
        assert component.logger.name == "BaseComponent.test"
