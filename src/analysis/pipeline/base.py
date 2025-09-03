"""
Base Analysis Pipeline Components

This module provides base classes for analysis pipelines.
"""

import pandas as pd
from typing import Dict, Any, List, Optional
import numpy as np

from ...core.interfaces import AnalysisPipeline
from ...core.exceptions import DataError, ValidationError


class BaseAnalysisPipeline(AnalysisPipeline):
    """
    Base class for analysis pipelines.
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize analysis pipeline.
        
        Args:
            name: Name of the pipeline
            config: Configuration dictionary
        """
        super().__init__(name, config)
        self.steps = []
        self.results = {}
    
    def add_data_source(self, source: Any) -> None:
        """
        Add a data source to the analysis pipeline.
        
        Args:
            source: Data source to add
        """
        # Implementation for interface compliance
        pass
    
    def add_analysis_step(self, step: Any) -> None:
        """
        Add an analysis step to the pipeline.
        
        Args:
            step: Analysis step to add
        """
        self.steps.append(step)
        self.logger.debug(f"Added step {step} to pipeline")
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the analysis pipeline.
        
        Returns:
            Dictionary containing analysis results
        """
        # Implementation for interface compliance
        return self.results
    
    def add_step(self, step: Any) -> None:
        """
        Add analysis step to pipeline (convenience method).
        
        Args:
            step: Analysis step to add
        """
        self.add_analysis_step(step)
    
    def process(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Process data through analysis pipeline.
        
        Args:
            data: Input data
            
        Returns:
            Dictionary containing analysis results
        """
        if data.empty:
            raise DataError("Input data is empty")
        
        self.results = {}
        current_data = data.copy()
        
        for i, step in enumerate(self.steps):
            try:
                step_result = step.process(current_data)
                self.results[f"step_{i}_{step.__class__.__name__}"] = step_result
                
                # If step returns modified data, use it for next step
                if isinstance(step_result, pd.DataFrame):
                    current_data = step_result
                    
            except Exception as e:
                self.logger.error(f"Error in pipeline step {i}: {e}")
                raise DataError(f"Pipeline step {i} failed: {e}")
        
        self.logger.info(f"Completed analysis pipeline with {len(self.steps)} steps")
        return self.results


__all__ = ["BaseAnalysisPipeline"]
