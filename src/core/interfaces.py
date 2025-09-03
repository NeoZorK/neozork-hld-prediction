"""
Interface definitions for the Neozork HLD Prediction system.

This module defines abstract interfaces that components must implement.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable
from .base import BaseComponent


@runtime_checkable
class DataSource(Protocol):
    """Protocol for data sources."""
    
    def fetch(self, **kwargs) -> Any:
        """Fetch data from source."""
        ...
    
    def is_available(self) -> bool:
        """Check if data source is available."""
        ...
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the data source."""
        ...


@runtime_checkable
class DataSink(Protocol):
    """Protocol for data sinks."""
    
    def store(self, data: Any, **kwargs) -> bool:
        """Store data to sink."""
        ...
    
    def is_writable(self) -> bool:
        """Check if data sink is writable."""
        ...


class DataPipeline(BaseComponent):
    """Abstract base class for data pipelines."""
    
    @abstractmethod
    def add_source(self, source: DataSource):
        """Add a data source to the pipeline."""
        pass
    
    @abstractmethod
    def add_sink(self, sink: DataSink):
        """Add a data sink to the pipeline."""
        pass
    
    @abstractmethod
    def add_processor(self, processor: 'DataProcessor'):
        """Add a data processor to the pipeline."""
        pass
    
    @abstractmethod
    def execute(self) -> bool:
        """Execute the data pipeline."""
        pass


class AnalysisPipeline(BaseComponent):
    """Abstract base class for analysis pipelines."""
    
    @abstractmethod
    def add_data_source(self, source: DataSource):
        """Add a data source to the analysis pipeline."""
        pass
    
    @abstractmethod
    def add_analysis_step(self, step: 'AnalysisStep'):
        """Add an analysis step to the pipeline."""
        pass
    
    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """Execute the analysis pipeline."""
        pass


class AnalysisStep(BaseComponent):
    """Abstract base class for analysis steps."""
    
    @abstractmethod
    def execute(self, data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the analysis step."""
        pass
    
    @abstractmethod
    def get_dependencies(self) -> List[str]:
        """Get list of step dependencies."""
        pass


class ModelRegistry(BaseComponent):
    """Abstract base class for model registry."""
    
    @abstractmethod
    def register_model(self, model: 'MLModel', name: str):
        """Register a machine learning model."""
        pass
    
    @abstractmethod
    def get_model(self, name: str) -> Optional['MLModel']:
        """Get a registered model by name."""
        pass
    
    @abstractmethod
    def list_models(self) -> List[str]:
        """List all registered model names."""
        pass
    
    @abstractmethod
    def remove_model(self, name: str) -> bool:
        """Remove a registered model."""
        pass


class ResultExporter(BaseComponent):
    """Abstract base class for result exporters."""
    
    @abstractmethod
    def export(self, results: Dict[str, Any], format: str, path: str) -> bool:
        """Export results in specified format."""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Get list of supported export formats."""
        pass
    
    @abstractmethod
    def validate_format(self, format: str) -> bool:
        """Validate if format is supported."""
        pass
