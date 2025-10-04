# -*- coding: utf-8 -*-
"""
AutoGluon configuration module.

This module provides configuration management for AutoGluon integration.
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class GluonConfig:
    """AutoGluon configuration class."""
    
    # AutoGluon presets for maximum quality
    presets: list = None
    time_limit: int = 3600  # 1 hour
    
    # Automatic data cleaning
    auto_clean: bool = True
    
    # Feature generation settings
    feature_generation: bool = True
    max_features: int = 1000
    
    # Validation settings
    holdout_frac: float = 0.1
    num_bag_folds: int = 5
    num_bag_sets: int = 1
    
    # Model selection
    excluded_model_types: list = None
    
    # Hyperparameter optimization
    hyperparameter_tune_kwargs: dict = None
    
    # Dynamic stacking settings (to avoid "Learner is already fit" error)
    dynamic_stacking: bool = True
    num_stack_levels: int = 1
    
    # Problem type settings
    problem_type: str = 'regression'  # 'regression', 'binary', 'multiclass'
    eval_metric: str = None  # Auto-determined based on problem_type
    
    def __post_init__(self):
        """Initialize default values."""
        if self.presets is None:
            self.presets = ['best_quality', 'high_quality']
        
        if self.excluded_model_types is None:
            self.excluded_model_types = []
        
        if self.hyperparameter_tune_kwargs is None:
            self.hyperparameter_tune_kwargs = {
                'num_trials': 10,
                'search_strategy': 'auto'
            }


# Default AutoGluon configuration
AUTOGLUON_CONFIG = {
    'presets': ['best_quality', 'high_quality'],
    'time_limit': 3600,
    'auto_clean': True,
    'feature_generation': True,
    'max_features': 1000,
    'holdout_frac': 0.1,
    'num_bag_folds': 5,
    'num_bag_sets': 1,
    'excluded_model_types': [],
    'hyperparameter_tune_kwargs': {
        'num_trials': 10,
        'search_strategy': 'auto'
    }
}


def load_gluon_config(config_path: Optional[str] = None) -> GluonConfig:
    """
    Load AutoGluon configuration from YAML file or use defaults.
    
    Args:
        config_path: Path to YAML configuration file
        
    Returns:
        GluonConfig: Configuration object
    """
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        return GluonConfig(**config_data)
    else:
        return GluonConfig()


def save_gluon_config(config: GluonConfig, config_path: str) -> None:
    """
    Save AutoGluon configuration to YAML file.
    
    Args:
        config: GluonConfig object
        config_path: Path to save configuration
    """
    config_dict = {
        'presets': config.presets,
        'time_limit': config.time_limit,
        'auto_clean': config.auto_clean,
        'feature_generation': config.feature_generation,
        'max_features': config.max_features,
        'holdout_frac': config.holdout_frac,
        'num_bag_folds': config.num_bag_folds,
        'num_bag_sets': config.num_bag_sets,
        'excluded_model_types': config.excluded_model_types,
        'hyperparameter_tune_kwargs': config.hyperparameter_tune_kwargs
    }
    
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True)


def get_default_config_path() -> str:
    """Get default configuration file path."""
    return os.path.join(os.path.dirname(__file__), 'gluon_config.yaml')
