"""
Base Data Validation Implementation

This module provides base classes for data validation components.
"""

import pandas as pd
from typing import Dict, Any, List
from abc import abstractmethod

from ...core.base import BaseComponent


class BaseDataValidator(BaseComponent):
    """
    Base class for data validators.
    
    Provides common functionality for data quality and integrity checks.
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize base data validator.
        
        Args:
            name: Validator name
            config: Configuration dictionary
        """
        super().__init__(name, config)
    
    @abstractmethod
    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate input data.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            Validation results dictionary
        """
        pass
    
    def get_validation_info(self) -> Dict[str, Any]:
        """
        Get validation information.
        
        Returns:
            Dictionary containing validation information
        """
        return {
            "validator_name": self.name,
            "validator_type": self.__class__.__name__,
            "config": self.config
        }


__all__ = ["BaseDataValidator"]
