# -*- coding: utf-8 -*-
# src/interactive/memory_manager.py
#!/usr/bin/env python3
"""
Memory management utilities for interactive data loading.
Handles memory monitoring, estimation, and optimization.
"""

import psutil
import gc
from typing import Dict
import pandas as pd


class MemoryManager:
    """Manages memory usage and optimization for data loading operations."""
    
    def __init__(self, max_memory_mb: int = 6144):
        """
        Initialize MemoryManager.
        
        Args:
            max_memory_mb: Maximum memory limit in MB
        """
        self.max_memory_mb = max_memory_mb
        self.enable_memory_optimization = True
    
    def get_memory_info(self) -> Dict[str, float]:
        """
        Get current memory usage information.
        
        Returns:
            Dict with memory usage details
        """
        memory = psutil.virtual_memory()
        return {
            'total_gb': memory.total / (1024**3),
            'available_gb': memory.available / (1024**3),
            'used_gb': memory.used / (1024**3),
            'percent_used': memory.percent,
            'available_mb': memory.available / (1024**2)
        }
    
    def check_memory_available(self, required_mb: int = None) -> bool:
        """
        Check if sufficient memory is available.
        
        Args:
            required_mb: Required memory in MB
            
        Returns:
            bool: True if memory is available
        """
        if not self.enable_memory_optimization:
            return True
            
        memory_info = self.get_memory_info()
        available_mb = memory_info['available_mb']
        
        if required_mb is None:
            # Use 80% of available memory as safe threshold
            safe_memory = available_mb * 0.8
            return safe_memory > 100  # At least 100MB available
        else:
            return available_mb > required_mb
    
    def estimate_memory_usage(self, df: pd.DataFrame) -> int:
        """
        Estimate memory usage of a DataFrame.
        
        Args:
            df: DataFrame to estimate memory for
            
        Returns:
            int: Estimated memory usage in MB
        """
        if df is None or df.empty:
            return 0
            
        # Get memory usage in bytes
        memory_bytes = df.memory_usage(deep=True).sum()
        
        # Convert to MB
        memory_mb = memory_bytes / (1024 * 1024)
        
        return int(memory_mb)
    
    def get_file_size_mb(self, file_path) -> float:
        """
        Get file size in MB.
        
        Args:
            file_path: Path to file
            
        Returns:
            float: File size in MB
        """
        try:
            size_bytes = file_path.stat().st_size
            return size_bytes / (1024 * 1024)
        except Exception:
            return 0.0
    
    def optimize_memory(self):
        """Force garbage collection to free memory."""
        if self.enable_memory_optimization:
            gc.collect()
    
    def should_use_chunked_loading(self, file_path, chunk_size: int = 50000) -> bool:
        """
        Determine if chunked loading should be used.
        
        Args:
            file_path: Path to file
            chunk_size: Size of chunks
            
        Returns:
            bool: True if chunked loading should be used
        """
        if not self.enable_memory_optimization:
            return False
            
        file_size_mb = self.get_file_size_mb(file_path)
        
        # Use chunked loading for files larger than 100MB
        return file_size_mb > 100
