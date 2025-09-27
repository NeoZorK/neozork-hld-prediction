"""
Value Score Analyzer for Trading Strategy Evaluation
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Union
import logging

logger = logging.getLogger(__name__)


class ValueScoreAnalyzer:
    """
    Analyzes trading strategy value scores for ML model predictions.
    """
    
    def __init__(self):
        """Initialize the Value Score Analyzer."""
        self.logger = logging.getLogger(__name__)
    
    def analyze(self, predictions: Union[np.ndarray, pd.Series], 
                actual: Union[np.ndarray, pd.Series]) -> Dict[str, float]:
        """
        Analyze value scores for trading strategy predictions.
        
        Args:
            predictions: Model predictions
            actual: Actual values
            
        Returns:
            Dictionary of value scores
        """
        try:
            # Convert to numpy arrays if needed
            if isinstance(predictions, pd.Series):
                predictions = predictions.values
            if isinstance(actual, pd.Series):
                actual = actual.values
            
            # Calculate basic trading metrics
            results = {}
            
            # For regression problems (continuous predictions)
            if len(np.unique(predictions)) > 2:
                # Calculate directional accuracy
                pred_direction = np.sign(predictions - 0.5)  # Assuming 0.5 is neutral
                actual_direction = np.sign(actual - 0.5)
                directional_accuracy = np.mean(pred_direction == actual_direction)
                results['directional_accuracy'] = directional_accuracy
                
                # Calculate correlation
                correlation = np.corrcoef(predictions, actual)[0, 1]
                results['correlation'] = correlation
                
                # Calculate MAE and RMSE
                mae = np.mean(np.abs(predictions - actual))
                rmse = np.sqrt(np.mean((predictions - actual) ** 2))
                results['mae'] = mae
                results['rmse'] = rmse
                
            else:
                # For classification problems
                accuracy = np.mean(predictions == actual)
                results['accuracy'] = accuracy
                
                # Calculate precision, recall, F1 for binary classification
                if len(np.unique(actual)) == 2:
                    from sklearn.metrics import precision_score, recall_score, f1_score
                    precision = precision_score(actual, predictions, average='binary')
                    recall = recall_score(actual, predictions, average='binary')
                    f1 = f1_score(actual, predictions, average='binary')
                    
                    results['precision'] = precision
                    results['recall'] = recall
                    results['f1_score'] = f1
            
            # Calculate profit factor (simplified)
            # This is a basic implementation - in real trading, you'd need price data
            returns = predictions - actual
            positive_returns = returns[returns > 0]
            negative_returns = returns[returns < 0]
            
            if len(positive_returns) > 0 and len(negative_returns) > 0:
                profit_factor = np.mean(positive_returns) / abs(np.mean(negative_returns))
                results['profit_factor'] = profit_factor
            
            # Calculate Sharpe ratio (simplified)
            if len(returns) > 1:
                sharpe_ratio = np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0
                results['sharpe_ratio'] = sharpe_ratio
            
            # Calculate win rate
            win_rate = np.mean(returns > 0)
            results['win_rate'] = win_rate
            
            self.logger.info(f"Value scores calculated: {len(results)} metrics")
            return results
            
        except Exception as e:
            self.logger.error(f"Error calculating value scores: {e}")
            return {
                'error': str(e),
                'directional_accuracy': 0.0,
                'correlation': 0.0,
                'mae': 0.0,
                'rmse': 0.0,
                'win_rate': 0.0
            }
