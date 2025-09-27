# -*- coding: utf-8 -*-
"""
AutoGluon evaluator wrapper.

This module provides evaluation capabilities for trained AutoGluon models.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Union, Tuple
import logging
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, classification_report
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


class GluonEvaluator:
    """AutoGluon evaluator wrapper."""
    
    def __init__(self, predictor: TabularPredictor):
        """
        Initialize Gluon evaluator.
        
        Args:
            predictor: Trained TabularPredictor
        """
        if not AUTOGLUON_AVAILABLE:
            raise ImportError("AutoGluon is not available")
        
        self.predictor = predictor
        
    def evaluate(self, test_data: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """
        Evaluate trained models on test data.
        
        Args:
            test_data: Test data
            target_column: Target column name
            
        Returns:
            Evaluation results dictionary
        """
        logger.info(f"Evaluating models on {len(test_data)} test samples...")
        
        # Get predictions
        predictions = self.predictor.predict(test_data)
        
        # Get true values
        y_true = test_data[target_column]
        
        # Calculate metrics
        metrics = self._calculate_metrics(y_true, predictions)
        
        # Get model performance
        performance = self.predictor.evaluate(test_data)
        
        # Get feature importance
        feature_importance = self.predictor.feature_importance()
        
        # Create results dictionary
        results = {
            'predictions': predictions,
            'metrics': metrics,
            'performance': performance,
            'feature_importance': feature_importance,
            'model_leaderboard': self.predictor.leaderboard()
        }
        
        logger.info("Model evaluation completed successfully")
        return results
    
    def _calculate_metrics(self, y_true: pd.Series, y_pred: pd.Series) -> Dict[str, float]:
        """
        Calculate evaluation metrics.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Metrics dictionary
        """
        metrics = {}
        
        # Handle missing values
        mask = ~(y_true.isna() | y_pred.isna())
        y_true_clean = y_true[mask]
        y_pred_clean = y_pred[mask]
        
        if len(y_true_clean) == 0:
            logger.warning("No valid data for metric calculation")
            return metrics
        
        # Check if it's a classification or regression problem
        if self.predictor.problem_type in ['binary', 'multiclass']:
            # Classification metrics
            metrics['accuracy'] = accuracy_score(y_true_clean, y_pred_clean)
            
            # Classification report
            try:
                report = classification_report(y_true_clean, y_pred_clean, output_dict=True)
                metrics['classification_report'] = report
            except Exception as e:
                logger.warning(f"Could not generate classification report: {e}")
        else:
            # Regression metrics
            metrics['mse'] = mean_squared_error(y_true_clean, y_pred_clean)
            metrics['rmse'] = np.sqrt(metrics['mse'])
            metrics['mae'] = mean_absolute_error(y_true_clean, y_pred_clean)
            metrics['r2'] = r2_score(y_true_clean, y_pred_clean)
        
        return metrics
    
    def cross_validate(self, data: pd.DataFrame, target_column: str, 
                      cv_folds: int = 5) -> Dict[str, Any]:
        """
        Perform cross-validation.
        
        Args:
            data: Input data
            target_column: Target column name
            cv_folds: Number of CV folds
            
        Returns:
            Cross-validation results
        """
        logger.info(f"Performing {cv_folds}-fold cross-validation...")
        
        try:
            # Perform cross-validation
            cv_results = self.predictor.evaluate_cv(data, cv_folds=cv_folds)
            
            logger.info("Cross-validation completed successfully")
            return cv_results
            
        except Exception as e:
            logger.error(f"Cross-validation failed: {e}")
            return {}
    
    def get_model_leaderboard(self) -> pd.DataFrame:
        """
        Get model leaderboard.
        
        Returns:
            Leaderboard DataFrame
        """
        return self.predictor.leaderboard()
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance.
        
        Returns:
            Feature importance DataFrame
        """
        return self.predictor.feature_importance()
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information.
        
        Returns:
            Model information dictionary
        """
        return self.predictor.info()
    
    def compare_models(self, test_data: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """
        Compare different models in the ensemble.
        
        Args:
            test_data: Test data
            target_column: Target column name
            
        Returns:
            Model comparison results
        """
        logger.info("Comparing models in ensemble...")
        
        try:
            # Get individual model predictions
            model_predictions = {}
            leaderboard = self.predictor.leaderboard()
            
            for model_name in leaderboard['model'].values:
                try:
                    # Get predictions from individual model
                    model_pred = self.predictor.predict(test_data, model=model_name)
                    model_predictions[model_name] = model_pred
                except Exception as e:
                    logger.warning(f"Could not get predictions for model {model_name}: {e}")
            
            # Calculate metrics for each model
            model_metrics = {}
            y_true = test_data[target_column]
            
            for model_name, predictions in model_predictions.items():
                metrics = self._calculate_metrics(y_true, predictions)
                model_metrics[model_name] = metrics
            
            logger.info("Model comparison completed successfully")
            return {
                'model_predictions': model_predictions,
                'model_metrics': model_metrics,
                'leaderboard': leaderboard
            }
            
        except Exception as e:
            logger.error(f"Model comparison failed: {e}")
            return {}
