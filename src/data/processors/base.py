"""
Base Data Processor Implementation

This module provides base classes for data processing components.
"""

import pandas as pd
from typing import Dict, Any
from abc import abstractmethod

from ...core.base import BaseComponent, DataProcessor


class BaseDataProcessor(DataProcessor):
    """
    Base class for data processors.
    
    Provides common functionality for data transformation and cleaning operations.
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize base data processor.
        
        Args:
            name: Processor name
            config: Configuration dictionary
        """
        super().__init__(name, config)
    
    @abstractmethod
    def process_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Process input data.
        
        Args:
            data: Input DataFrame to process
            
        Returns:
            Processed DataFrame
        """
        pass
    
    def get_processing_info(self) -> Dict[str, Any]:
        """
        Get processing information.
        
        Returns:
            Dictionary containing processing information
        """
        return {
            "processor_name": self.name,
            "processor_type": self.__class__.__name__,
            "config": self.config
        }


__all__ = ["BaseDataProcessor"]
