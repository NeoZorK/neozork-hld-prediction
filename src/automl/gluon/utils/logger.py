# -*- coding: utf-8 -*-
"""
AutoGluon logger utility.

This module provides logging capabilities for AutoGluon integration.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import json


class GluonLogger:
    """AutoGluon logger utility."""
    
    def __init__(self, log_level: str = "INFO", log_file: Optional[str] = None):
        """
        Initialize Gluon logger.
        
        Args:
            log_level: Logging level
            log_file: Log file path
        """
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.log_file = log_file
        
        # Create logger
        self.logger = logging.getLogger('gluon_automl')
        self.logger.setLevel(self.log_level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        if self.log_file:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)
    
    def log_experiment(self, experiment_data: Dict[str, Any]):
        """Log experiment data."""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'experiment': experiment_data
        }
        
        self.info(f"Experiment logged: {json.dumps(log_entry, indent=2)}")
    
    def log_performance(self, performance_data: Dict[str, Any]):
        """Log performance data."""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'performance': performance_data
        }
        
        self.info(f"Performance logged: {json.dumps(log_entry, indent=2)}")
    
    def log_drift(self, drift_data: Dict[str, Any]):
        """Log drift detection data."""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'drift': drift_data
        }
        
        self.info(f"Drift logged: {json.dumps(log_entry, indent=2)}")
