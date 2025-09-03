"""
Base classes and abstract interfaces for the Neozork HLD Prediction system.

This module provides the foundation classes that other components inherit from.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import logging
from datetime import datetime


class BaseComponent(ABC):
    """Base class for all system components."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
        self.created_at = datetime.now()
        
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"
    
    def __repr__(self) -> str:
        return self.__str__()


class DataProcessor(BaseComponent):
    """Base class for data processing components."""
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process input data and return processed result."""
        pass
    
    @abstractmethod
    def validate_input(self, data: Any) -> bool:
        """Validate input data before processing."""
        pass


class AnalysisEngine(BaseComponent):
    """Base class for analysis engines."""
    
    @abstractmethod
    def analyze(self, data: Any) -> Dict[str, Any]:
        """Perform analysis on input data."""
        pass
    
    @abstractmethod
    def get_metrics(self) -> Dict[str, Any]:
        """Get current analysis metrics."""
        pass


class MLModel(BaseComponent):
    """Base class for machine learning models."""
    
    @abstractmethod
    def train(self, data: Any) -> bool:
        """Train the model with provided data."""
        pass
    
    @abstractmethod
    def predict(self, data: Any) -> Any:
        """Make predictions using the trained model."""
        pass
    
    @abstractmethod
    def evaluate(self, test_data: Any) -> Dict[str, float]:
        """Evaluate model performance on test data."""
        pass


class Exportable(BaseComponent):
    """Base class for components that can export their results."""
    
    @abstractmethod
    def export(self, format: str, path: str) -> bool:
        """Export results in specified format to given path."""
        pass
    
    @abstractmethod
    def get_export_formats(self) -> List[str]:
        """Get list of supported export formats."""
        pass
