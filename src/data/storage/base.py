"""
Base Data Storage Implementation

This module provides base classes for data storage components.
"""

import pandas as pd
from typing import Dict, Any
from abc import abstractmethod

from ...core.base import BaseComponent


class BaseDataStorage(BaseComponent):
    """
    Base class for data storage components.
    
    Provides common functionality for data persistence operations.
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize base data storage.
        
        Args:
            name: Storage name
            config: Configuration dictionary
        """
        super().__init__(name, config)
    
    @abstractmethod
    def store_data(self, data: pd.DataFrame, **kwargs) -> None:
        """
        Store data to storage backend.
        
        Args:
            data: DataFrame to store
            **kwargs: Additional storage parameters
        """
        pass
    
    @abstractmethod
    def load_data(self, **kwargs) -> pd.DataFrame:
        """
        Load data from storage backend.
        
        Args:
            **kwargs: Additional loading parameters
            
        Returns:
            Loaded DataFrame
        """
        pass
    
    @abstractmethod
    def is_writable(self) -> bool:
        """
        Check if storage is writable.
        
        Returns:
            True if storage is writable, False otherwise
        """
        pass


__all__ = ["BaseDataStorage"]
