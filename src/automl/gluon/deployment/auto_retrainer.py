# -*- coding: utf-8 -*-
"""
AutoGluon auto-retrainer.

This module provides automatic retraining capabilities for AutoGluon models.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Union
import logging
from datetime import datetime, timedelta
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


class AutoRetrainer:
    """AutoGluon auto-retrainer."""
    
    def __init__(self, retrain_threshold: float = 0.1, 
                 min_samples: int = 100, 
                 max_retrain_frequency: int = 7):
        """
        Initialize auto-retrainer.
        
        Args:
            retrain_threshold: Performance degradation threshold
            min_samples: Minimum samples for retraining
            max_retrain_frequency: Maximum retrain frequency (days)
        """
        if not AUTOGLUON_AVAILABLE:
            raise ImportError("AutoGluon is not available")
        
        self.retrain_threshold = retrain_threshold
        self.min_samples = min_samples
        self.max_retrain_frequency = max_retrain_frequency
        self.last_retrain = None
        
    def should_retrain(self, current_performance: float, 
                      baseline_performance: float,
                      new_data_size: int) -> bool:
        """
        Determine if model should be retrained.
        
        Args:
            current_performance: Current model performance
            baseline_performance: Baseline performance
            new_data_size: Size of new data
            
        Returns:
            True if retraining is recommended
        """
        # Check if enough new data
        if new_data_size < self.min_samples:
            logger.info(f"Not enough new data for retraining: {new_data_size} < {self.min_samples}")
            return False
        
        # Check performance degradation
        performance_drop = baseline_performance - current_performance
        if performance_drop > self.retrain_threshold:
            logger.info(f"Performance degradation detected: {performance_drop:.3f} > {self.retrain_threshold}")
            return True
        
        # Check retrain frequency
        if self.last_retrain:
            days_since_retrain = (datetime.now() - self.last_retrain).days
            if days_since_retrain < self.max_retrain_frequency:
                logger.info(f"Retraining too frequent: {days_since_retrain} days < {self.max_retrain_frequency}")
                return False
        
        # If no performance degradation, don't retrain
        logger.info("No performance degradation detected, no retraining needed")
        return False
    
    def retrain(self, predictor: TabularPredictor, 
                new_data: pd.DataFrame, 
                target_column: str,
                config: Any) -> TabularPredictor:
        """
        Retrain model with new data.
        
        Args:
            predictor: Current trained predictor
            new_data: New training data
            target_column: Target column name
            config: Training configuration
            
        Returns:
            Retrained predictor
        """
        logger.info(f"Retraining model with {len(new_data)} new samples...")
        
        # Create new predictor
        new_predictor = TabularPredictor(
            label=target_column,
            problem_type=predictor.problem_type,
            eval_metric=predictor.eval_metric,
            path=predictor.path + "_retrained"
        )
        
        # Prepare training arguments
        fit_args = {
            'time_limit': config.time_limit,
            'presets': config.presets,
            'auto_clean': config.auto_clean,
            'feature_generation': config.feature_generation,
            'holdout_frac': config.holdout_frac,
            'num_bag_folds': config.num_bag_folds,
            'num_bag_sets': config.num_bag_sets,
            'excluded_model_types': config.excluded_model_types,
            'hyperparameter_tune_kwargs': config.hyperparameter_tune_kwargs
        }
        
        # Retrain model
        new_predictor.fit(new_data, **fit_args)
        
        # Update retrain timestamp
        self.last_retrain = datetime.now()
        
        logger.info("Model retraining completed successfully")
        return new_predictor
    
    def incremental_retrain(self, predictor: TabularPredictor,
                          new_data: pd.DataFrame,
                          target_column: str) -> TabularPredictor:
        """
        Perform incremental retraining.
        
        Args:
            predictor: Current trained predictor
            new_data: New training data
            target_column: Target column name
            
        Returns:
            Updated predictor
        """
        logger.info("Performing incremental retraining...")
        
        try:
            # Use AutoGluon's built-in retraining
            updated_predictor = predictor.fit(
                new_data,
                time_limit=3600,  # 1 hour
                presets=['medium_quality_faster_train']
            )
            
            logger.info("Incremental retraining completed successfully")
            return updated_predictor
            
        except Exception as e:
            logger.error(f"Incremental retraining failed: {e}")
            return predictor
    
    def schedule_retrain(self, predictor: TabularPredictor,
                        retrain_schedule: str = "daily") -> Dict[str, Any]:
        """
        Schedule automatic retraining.
        
        Args:
            predictor: Current trained predictor
            retrain_schedule: Retraining schedule (daily, weekly, monthly)
            
        Returns:
            Schedule configuration
        """
        schedule_config = {
            'schedule': retrain_schedule,
            'last_retrain': self.last_retrain,
            'next_retrain': self._calculate_next_retrain(retrain_schedule),
            'enabled': True
        }
        
        logger.info(f"Retraining scheduled: {retrain_schedule}")
        return schedule_config
    
    def _calculate_next_retrain(self, schedule: str) -> datetime:
        """Calculate next retrain time."""
        now = datetime.now()
        
        if schedule == "daily":
            return now + timedelta(days=1)
        elif schedule == "weekly":
            return now + timedelta(weeks=1)
        elif schedule == "monthly":
            return now + timedelta(days=30)
        else:
            return now + timedelta(days=1)
    
    def get_retrain_status(self) -> Dict[str, Any]:
        """
        Get retraining status.
        
        Returns:
            Status dictionary
        """
        return {
            'last_retrain': self.last_retrain,
            'retrain_threshold': self.retrain_threshold,
            'min_samples': self.min_samples,
            'max_retrain_frequency': self.max_retrain_frequency,
            'ready_for_retrain': self.last_retrain is None or 
                               (datetime.now() - self.last_retrain).days >= self.max_retrain_frequency
        }
