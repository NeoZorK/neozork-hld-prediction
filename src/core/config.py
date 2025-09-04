"""
Configuration management for the Neozork HLD Prediction system.

This module handles all configuration settings and environment variables.
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, Optional
from .exceptions import ConfigurationError


class Config:
    """Central configuration manager for the system."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self._config = {}
        self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path."""
        return os.path.join(os.path.dirname(__file__), "..", "..", "config.json")
    
    def _load_config(self):
        """Load configuration from file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self._config = json.load(f)
            else:
                self._config = self._get_default_config()
        except Exception as e:
            raise ConfigurationError(f"Failed to load config: {e}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values."""
        return {
            "data": {
                "cache_dir": "data/csv_converted",
                "raw_dir": "data/raw_parquet",
                "processed_dir": "data/cleaned_data",
                "mql5_dir": "data/mql5_feed",
                "samples_dir": "data/samples",
                "indicators_dir": "data/indicators",
                "max_file_size_mb": 100
            },
            "analysis": {
                "default_timeframe": "1H",
                "max_lookback_periods": 1000,
                "confidence_threshold": 0.8
            },
            "ml": {
                "model_dir": "models",
                "default_algorithm": "random_forest",
                "cross_validation_folds": 5
            },
            "export": {
                "default_format": "csv",
                "output_dir": "results"
            },
            "logging": {
                "level": "INFO",
                "file": "logs/system.log",
                "max_size_mb": 10
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by key."""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self):
        """Save current configuration to file."""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            raise ConfigurationError(f"Failed to save config: {e}")
    
    def get_data_dir(self, subdir: str = "") -> str:
        """Get data directory path."""
        base_dir = self.get("data.cache_dir", "data/cache")
        if subdir:
            return os.path.join(base_dir, subdir)
        return base_dir
    
    def get_model_dir(self) -> str:
        """Get model directory path."""
        return self.get("ml.model_dir", "models")
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self.get("logging", {})


# Global configuration instance
config = Config()
