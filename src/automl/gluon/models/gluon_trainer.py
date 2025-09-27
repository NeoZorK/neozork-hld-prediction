# -*- coding: utf-8 -*-
"""
AutoGluon trainer wrapper.

This module provides training capabilities using AutoGluon TabularPredictor.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Union
import logging
from pathlib import Path
import warnings

# AutoGluon imports
try:
    from autogluon.tabular import TabularPredictor
    AUTOGLUON_AVAILABLE = True
except ImportError:
    AUTOGLUON_AVAILABLE = False
    TabularPredictor = None

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class GluonTrainer:
    """AutoGluon trainer wrapper."""
    
    def __init__(self, config: Any, experiment_config: Any):
        """
        Initialize Gluon trainer.
        
        Args:
            config: AutoGluon configuration
            experiment_config: Experiment configuration
        """
        if not AUTOGLUON_AVAILABLE:
            raise ImportError("AutoGluon is not available")
        
        self.config = config
        self.experiment_config = experiment_config
        self.predictor = None
        
    def train(self, train_data: pd.DataFrame, target_column: str, 
              validation_data: Optional[pd.DataFrame] = None) -> TabularPredictor:
        """
        Train AutoGluon models.
        
        Args:
            train_data: Training data
            target_column: Target column name
            validation_data: Optional validation data
            
        Returns:
            Trained TabularPredictor
        """
        logger.info("Starting AutoGluon training...")
        
        # Create output directory
        output_dir = Path("models/autogluon")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize TabularPredictor
        self.predictor = TabularPredictor(
            label=target_column,
            problem_type=self.experiment_config.problem_type,
            eval_metric=self.experiment_config.eval_metric,
            path=str(output_dir)
        )
        
        # Prepare training arguments
        fit_args = {
            'time_limit': self.config.time_limit,
            'presets': self.config.presets,
            # 'auto_clean': self.config.auto_clean,  # Not supported in AutoGluon
            # 'feature_generation': self.config.feature_generation,  # Not supported in AutoGluon
            'holdout_frac': self.config.holdout_frac,
            'num_bag_folds': self.config.num_bag_folds,
            'num_bag_sets': self.config.num_bag_sets,
            'excluded_model_types': self.config.excluded_model_types,
            # 'hyperparameter_tune_kwargs': self.config.hyperparameter_tune_kwargs  # Disabled for simplicity
        }
        
        # Add validation data if provided
        if validation_data is not None:
            fit_args['holdout_frac'] = None
            fit_args['tuning_data'] = validation_data  # Use 'tuning_data' instead of 'val_data'
        
        # Train models
        logger.info(f"Training with {len(train_data)} samples...")
        self.predictor.fit(train_data, **fit_args)
        
        logger.info("AutoGluon training completed successfully")
        return self.predictor
    
    def get_leaderboard(self) -> pd.DataFrame:
        """
        Get model leaderboard.
        
        Returns:
            Leaderboard DataFrame
        """
        if not self.predictor:
            raise ValueError("Models must be trained first")
        
        return self.predictor.leaderboard()
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance.
        
        Returns:
            Feature importance DataFrame
        """
        if not self.predictor:
            raise ValueError("Models must be trained first")
        
        return self.predictor.feature_importance()
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information.
        
        Returns:
            Model information dictionary
        """
        if not self.predictor:
            raise ValueError("Models must be trained first")
        
        return self.predictor.info()
