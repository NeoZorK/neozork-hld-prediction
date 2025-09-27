# -*- coding: utf-8 -*-
"""
Experiment configuration module for AutoGluon integration.

This module provides experiment configuration management.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime


@dataclass
class ExperimentConfig:
    """Experiment configuration class."""
    
    # Experiment metadata
    experiment_name: str = "autogluon_experiment"
    description: str = "AutoGluon trading strategy experiment"
    created_at: datetime = field(default_factory=datetime.now)
    
    # Data configuration
    data_path: str = "data/"
    data_formats: List[str] = field(default_factory=lambda: ['parquet', 'csv', 'json'])
    recursive_search: bool = True
    
    # Time series split configuration
    train_ratio: float = 0.6
    validation_ratio: float = 0.2
    test_ratio: float = 0.2
    
    # Feature engineering configuration
    use_custom_features: bool = False
    custom_features_config: Optional[str] = None
    max_auto_features: int = 1000
    
    # Model configuration
    target_column: str = "target"
    problem_type: str = "regression"  # or "classification"
    eval_metric: str = "rmse"  # or "accuracy", "log_loss", etc.
    
    # Training configuration
    time_limit: int = 3600
    presets: List[str] = field(default_factory=lambda: ['best_quality'])
    
    # Validation configuration
    use_time_series_split: bool = True
    num_cv_folds: int = 5
    
    # Export configuration
    export_path: str = "models/autogluon/"
    export_formats: List[str] = field(default_factory=lambda: ['pickle', 'onnx'])
    
    # Monitoring configuration
    enable_drift_monitoring: bool = True
    drift_threshold: float = 0.1
    retrain_on_drift: bool = True
    
    # Logging configuration
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'experiment_name': self.experiment_name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'data_path': self.data_path,
            'data_formats': self.data_formats,
            'recursive_search': self.recursive_search,
            'train_ratio': self.train_ratio,
            'validation_ratio': self.validation_ratio,
            'test_ratio': self.test_ratio,
            'use_custom_features': self.use_custom_features,
            'custom_features_config': self.custom_features_config,
            'max_auto_features': self.max_auto_features,
            'target_column': self.target_column,
            'problem_type': self.problem_type,
            'eval_metric': self.eval_metric,
            'time_limit': self.time_limit,
            'presets': self.presets,
            'use_time_series_split': self.use_time_series_split,
            'num_cv_folds': self.num_cv_folds,
            'export_path': self.export_path,
            'export_formats': self.export_formats,
            'enable_drift_monitoring': self.enable_drift_monitoring,
            'drift_threshold': self.drift_threshold,
            'retrain_on_drift': self.retrain_on_drift,
            'log_level': self.log_level,
            'log_file': self.log_file
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ExperimentConfig':
        """Create configuration from dictionary."""
        # Handle datetime conversion
        if 'created_at' in config_dict and isinstance(config_dict['created_at'], str):
            config_dict['created_at'] = datetime.fromisoformat(config_dict['created_at'])
        
        return cls(**config_dict)
