# -*- coding: utf-8 -*-
"""
Data State Manager for NeoZork Interactive ML Trading Strategy Development.

This module manages the global state of loaded data in memory.
"""

from typing import Dict, Any, Optional
import pandas as pd
from datetime import datetime


class DataStateManager:
    """
    Manages the global state of loaded data in memory.
    
    Features:
    - Track loaded data in memory
    - Store metadata about loaded data
    - Provide access to current data state
    - Memory usage tracking
    """
    
    def __init__(self):
        """Initialize the data state manager."""
        self.current_data = None
        self.current_features = None
        self.current_model = None
        self.loaded_data_info = None
        self.loaded_at = None
        self.memory_used = 0.0
    
    def set_loaded_data(self, data: Dict[str, Any], metadata: Dict[str, Any], 
                       memory_used: float = 0.0):
        """
        Set the currently loaded data in memory.
        
        Args:
            data: Dictionary containing loaded data
            metadata: Metadata about the loaded data
            memory_used: Memory used in MB
        """
        self.current_data = data
        self.loaded_data_info = metadata
        self.memory_used = memory_used
        self.loaded_at = datetime.now()
    
    def get_loaded_data(self) -> Optional[Dict[str, Any]]:
        """Get the currently loaded data."""
        return self.current_data
    
    def get_loaded_data_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the currently loaded data."""
        return self.loaded_data_info
    
    def is_data_loaded(self) -> bool:
        """Check if data is currently loaded in memory."""
        return self.current_data is not None
    
    def get_memory_usage(self) -> float:
        """Get memory usage of loaded data in MB."""
        return self.memory_used
    
    def get_loaded_at(self) -> Optional[datetime]:
        """Get when data was loaded."""
        return self.loaded_at
    
    def clear_loaded_data(self):
        """Clear the currently loaded data."""
        self.current_data = None
        self.current_features = None
        self.current_model = None
        self.loaded_data_info = None
        self.loaded_at = None
        self.memory_used = 0.0
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get a summary of the currently loaded data."""
        if not self.is_data_loaded():
            return {
                'status': 'no_data',
                'message': 'No data loaded in memory'
            }
        
        return {
            'status': 'loaded',
            'symbol': self.loaded_data_info.get('symbol', 'Unknown'),
            'source': self.loaded_data_info.get('source', 'Unknown'),
            'main_timeframe': self.loaded_data_info.get('main_timeframe', 'Unknown'),
            'timeframes': self.loaded_data_info.get('timeframes', []),
            'total_rows': self.loaded_data_info.get('total_rows', 0),
            'main_data_shape': self.loaded_data_info.get('main_data_shape', [0, 0]),
            'cross_timeframes': self.loaded_data_info.get('cross_timeframes', []),
            'created_at': self.loaded_data_info.get('created_at', 'Unknown'),
            'size_mb': self.loaded_data_info.get('size_mb', 0.0),
            'memory_used': self.memory_used,
            'loaded_at': self.loaded_at.isoformat() if self.loaded_at else 'Unknown'
        }


# Global instance
data_state_manager = DataStateManager()
