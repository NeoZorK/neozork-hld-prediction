"""
Base Data Pipeline Implementation

This module provides base classes for data processing pipelines.
"""

import pandas as pd
from typing import Dict, Any, List
from abc import abstractmethod

from ...core.base import BaseComponent
from ...core.interfaces import DataPipeline, AnalysisStep


class BaseDataPipeline(DataPipeline):
    """
    Base class for data processing pipelines.
    
    Provides orchestration for multiple data processing steps.
    """
    
    def __init__(self, name: str, steps: List[AnalysisStep], config: Dict[str, Any]):
        """
        Initialize base data pipeline.
        
        Args:
            name: Pipeline name
            steps: List of processing steps
            config: Configuration dictionary
        """
        self.name = name
        self.steps = steps
        self.config = config
    
    def execute(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Execute pipeline steps.
        
        Args:
            data: Input DataFrame
            
        Returns:
            Processed DataFrame
        """
        result = data
        
        for step in self.steps:
            result = step.process(result)
        
        return result
    
    def get_pipeline_info(self) -> Dict[str, Any]:
        """
        Get pipeline information.
        
        Returns:
            Dictionary containing pipeline information
        """
        return {
            "pipeline_name": self.name,
            "steps": [step.__class__.__name__ for step in self.steps],
            "config": self.config
        }


__all__ = ["BaseDataPipeline"]
