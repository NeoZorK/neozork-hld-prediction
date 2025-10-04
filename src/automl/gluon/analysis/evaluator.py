"""
Model Evaluation Module for SCHR Levels AutoML

Provides model evaluation and comparison tools.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import logging


class SCHREvaluator:
    """Model evaluation tools for SCHR Levels"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def evaluate_model(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Evaluate model performance"""
        try:
            metrics = {
                'accuracy': accuracy_score(y_true, y_pred),
                'precision': precision_score(y_true, y_pred, average='weighted'),
                'recall': recall_score(y_true, y_pred, average='weighted'),
                'f1_score': f1_score(y_true, y_pred, average='weighted')
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Model evaluation failed: {e}")
            return {'accuracy': 0, 'precision': 0, 'recall': 0, 'f1_score': 0}
    
    def compare_models(self, results: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """Compare multiple models"""
        try:
            comparison = {}
            
            for model_name, metrics in results.items():
                comparison[model_name] = {
                    'accuracy': metrics.get('accuracy', 0),
                    'precision': metrics.get('precision', 0),
                    'recall': metrics.get('recall', 0),
                    'f1_score': metrics.get('f1_score', 0)
                }
            
            # Find best model
            best_model = max(comparison.keys(), 
                           key=lambda x: comparison[x]['accuracy'])
            
            return {
                'comparison': comparison,
                'best_model': best_model,
                'best_accuracy': comparison[best_model]['accuracy']
            }
            
        except Exception as e:
            self.logger.error(f"Model comparison failed: {e}")
            return {'comparison': {}, 'best_model': None, 'best_accuracy': 0}
