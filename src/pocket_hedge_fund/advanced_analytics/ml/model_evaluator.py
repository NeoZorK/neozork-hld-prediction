"""
Model Evaluator

Evaluates ML model performance and provides metrics.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import pandas as pd

from ..models.analytics_models import ModelPerformance, ModelType, MarketData, PredictionResult

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """
    Evaluates ML model performance and provides comprehensive metrics.
    """
    
    def __init__(self):
        """Initialize model evaluator."""
        self.evaluation_metrics = self._setup_evaluation_metrics()
        self.benchmark_models = {}
    
    def _setup_evaluation_metrics(self) -> Dict[str, Any]:
        """Setup evaluation metrics for different model types."""
        return {
            'regression': {
                'primary_metrics': ['mse', 'mae', 'rmse', 'r2_score'],
                'secondary_metrics': ['mape', 'smape', 'directional_accuracy'],
                'thresholds': {
                    'good_r2': 0.7,
                    'good_mae': 0.05,
                    'good_mse': 0.01
                }
            },
            'classification': {
                'primary_metrics': ['accuracy', 'precision', 'recall', 'f1_score'],
                'secondary_metrics': ['auc_roc', 'auc_pr', 'confusion_matrix'],
                'thresholds': {
                    'good_accuracy': 0.8,
                    'good_precision': 0.75,
                    'good_recall': 0.75
                }
            },
            'time_series': {
                'primary_metrics': ['mse', 'mae', 'mape', 'directional_accuracy'],
                'secondary_metrics': ['theil_u', 'bias', 'efficiency'],
                'thresholds': {
                    'good_mape': 0.1,
                    'good_directional_accuracy': 0.6
                }
            }
        }
    
    async def evaluate_model(
        self,
        model_id: str,
        test_data: List[MarketData],
        predictions: List[PredictionResult] = None
    ) -> ModelPerformance:
        """
        Evaluate model performance on test data.
        
        Args:
            model_id: Model identifier
            test_data: Test market data
            predictions: Model predictions (optional)
            
        Returns:
            Model performance metrics
        """
        try:
            if not test_data:
                raise ValueError("Test data cannot be empty")
            
            # Generate predictions if not provided
            if predictions is None:
                predictions = await self._generate_test_predictions(model_id, test_data)
            
            # Extract actual values
            actual_values = self._extract_actual_values(test_data)
            predicted_values = self._extract_predicted_values(predictions)
            
            # Calculate metrics based on model type
            model_type = self._determine_model_type(model_id)
            metrics = await self._calculate_metrics(
                actual_values, predicted_values, model_type
            )
            
            # Create performance record
            performance = ModelPerformance(
                model_id=model_id,
                model_type=model_type,
                symbol=test_data[0].symbol if test_data else 'UNKNOWN',
                training_period={
                    'start': datetime.now() - timedelta(days=365),
                    'end': datetime.now() - timedelta(days=30)
                },
                test_period={
                    'start': test_data[0].timestamp if test_data else datetime.now(),
                    'end': test_data[-1].timestamp if test_data else datetime.now()
                },
                metrics=metrics,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_active=True
            )
            
            logger.info(f"Model {model_id} evaluated with {len(metrics)} metrics")
            return performance
            
        except Exception as e:
            logger.error(f"Failed to evaluate model {model_id}: {e}")
            raise
    
    async def _generate_test_predictions(
        self,
        model_id: str,
        test_data: List[MarketData]
    ) -> List[PredictionResult]:
        """Generate predictions for test data."""
        try:
            predictions = []
            
            # This is a simplified implementation
            # In practice, you would use the actual trained model
            
            for i, data in enumerate(test_data):
                # Simulate prediction
                predicted_value = float(data.close_price) * (1 + np.random.normal(0, 0.02))
                confidence = np.random.uniform(0.5, 0.9)
                
                prediction = PredictionResult(
                    model_id=model_id,
                    symbol=data.symbol,
                    prediction_type='price',
                    predicted_value=predicted_value,
                    confidence=confidence,
                    timestamp=data.timestamp,
                    prediction_horizon=1,
                    features_used=['close_price', 'volume'],
                    model_version="1.0.0"
                )
                predictions.append(prediction)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Failed to generate test predictions: {e}")
            raise
    
    def _extract_actual_values(self, test_data: List[MarketData]) -> np.ndarray:
        """Extract actual values from test data."""
        return np.array([float(data.close_price) for data in test_data])
    
    def _extract_predicted_values(self, predictions: List[PredictionResult]) -> np.ndarray:
        """Extract predicted values from predictions."""
        return np.array([float(pred.predicted_value) for pred in predictions])
    
    def _determine_model_type(self, model_id: str) -> ModelType:
        """Determine model type from model ID."""
        if 'price' in model_id.lower():
            return ModelType.LSTM
        elif 'volatility' in model_id.lower():
            return ModelType.NEURAL_NETWORK
        elif 'sentiment' in model_id.lower():
            return ModelType.TRANSFORMER
        elif 'risk' in model_id.lower():
            return ModelType.RANDOM_FOREST
        else:
            return ModelType.LINEAR_REGRESSION
    
    async def _calculate_metrics(
        self,
        actual: np.ndarray,
        predicted: np.ndarray,
        model_type: ModelType
    ) -> Dict[str, float]:
        """Calculate evaluation metrics."""
        try:
            metrics = {}
            
            # Basic regression metrics
            metrics['mse'] = float(np.mean((actual - predicted) ** 2))
            metrics['mae'] = float(np.mean(np.abs(actual - predicted)))
            metrics['rmse'] = float(np.sqrt(metrics['mse']))
            
            # R-squared
            ss_res = np.sum((actual - predicted) ** 2)
            ss_tot = np.sum((actual - np.mean(actual)) ** 2)
            metrics['r2_score'] = float(1 - (ss_res / ss_tot)) if ss_tot != 0 else 0.0
            
            # MAPE (Mean Absolute Percentage Error)
            mape = np.mean(np.abs((actual - predicted) / actual)) * 100
            metrics['mape'] = float(mape)
            
            # SMAPE (Symmetric Mean Absolute Percentage Error)
            smape = np.mean(2 * np.abs(actual - predicted) / (np.abs(actual) + np.abs(predicted))) * 100
            metrics['smape'] = float(smape)
            
            # Directional accuracy
            actual_direction = np.diff(actual) > 0
            predicted_direction = np.diff(predicted) > 0
            directional_accuracy = np.mean(actual_direction == predicted_direction)
            metrics['directional_accuracy'] = float(directional_accuracy)
            
            # Theil's U statistic
            theil_u = np.sqrt(np.mean((predicted - actual) ** 2)) / np.sqrt(np.mean(actual ** 2))
            metrics['theil_u'] = float(theil_u)
            
            # Bias
            bias = np.mean(predicted - actual)
            metrics['bias'] = float(bias)
            
            # Efficiency (Nash-Sutcliffe efficiency)
            efficiency = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0
            metrics['efficiency'] = float(efficiency)
            
            # Model-specific metrics
            if model_type in [ModelType.LSTM, ModelType.NEURAL_NETWORK]:
                metrics.update(await self._calculate_time_series_metrics(actual, predicted))
            elif model_type in [ModelType.RANDOM_FOREST, ModelType.SVM]:
                metrics.update(await self._calculate_classification_metrics(actual, predicted))
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to calculate metrics: {e}")
            raise
    
    async def _calculate_time_series_metrics(
        self,
        actual: np.ndarray,
        predicted: np.ndarray
    ) -> Dict[str, float]:
        """Calculate time series specific metrics."""
        try:
            metrics = {}
            
            # Lag-1 autocorrelation of residuals
            residuals = actual - predicted
            if len(residuals) > 1:
                lag1_autocorr = np.corrcoef(residuals[:-1], residuals[1:])[0, 1]
                metrics['lag1_autocorr'] = float(lag1_autocorr) if not np.isnan(lag1_autocorr) else 0.0
            
            # Ljung-Box test statistic (simplified)
            if len(residuals) > 10:
                lb_stat = len(residuals) * (len(residuals) + 2) * np.sum([
                    np.corrcoef(residuals[:-i], residuals[i:])[0, 1] ** 2 / (len(residuals) - i)
                    for i in range(1, min(10, len(residuals)))
                ])
                metrics['ljung_box_stat'] = float(lb_stat) if not np.isnan(lb_stat) else 0.0
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to calculate time series metrics: {e}")
            return {}
    
    async def _calculate_classification_metrics(
        self,
        actual: np.ndarray,
        predicted: np.ndarray
    ) -> Dict[str, float]:
        """Calculate classification specific metrics."""
        try:
            metrics = {}
            
            # Convert to binary classification (positive/negative returns)
            actual_binary = (actual > 0).astype(int)
            predicted_binary = (predicted > 0).astype(int)
            
            # Confusion matrix
            tp = np.sum((actual_binary == 1) & (predicted_binary == 1))
            tn = np.sum((actual_binary == 0) & (predicted_binary == 0))
            fp = np.sum((actual_binary == 0) & (predicted_binary == 1))
            fn = np.sum((actual_binary == 1) & (predicted_binary == 0))
            
            # Classification metrics
            accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0.0
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
            
            metrics['accuracy'] = float(accuracy)
            metrics['precision'] = float(precision)
            metrics['recall'] = float(recall)
            metrics['f1_score'] = float(f1_score)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to calculate classification metrics: {e}")
            return {}
    
    async def compare_models(
        self,
        model_performances: List[ModelPerformance]
    ) -> Dict[str, Any]:
        """
        Compare multiple model performances.
        
        Args:
            model_performances: List of model performance metrics
            
        Returns:
            Comparison results
        """
        try:
            if not model_performances:
                return {}
            
            comparison = {
                'models': [],
                'best_models': {},
                'summary': {}
            }
            
            # Extract metrics for comparison
            all_metrics = set()
            for perf in model_performances:
                all_metrics.update(perf.metrics.keys())
            
            # Compare each metric
            for metric in all_metrics:
                metric_values = {}
                for perf in model_performances:
                    if metric in perf.metrics:
                        metric_values[perf.model_id] = perf.metrics[metric]
                
                if metric_values:
                    # Find best model for this metric
                    if metric in ['mse', 'mae', 'rmse', 'mape', 'smape', 'theil_u', 'bias']:
                        # Lower is better
                        best_model = min(metric_values, key=metric_values.get)
                    else:
                        # Higher is better
                        best_model = max(metric_values, key=metric_values.get)
                    
                    comparison['best_models'][metric] = {
                        'model_id': best_model,
                        'value': metric_values[best_model]
                    }
            
            # Create summary
            comparison['summary'] = {
                'total_models': len(model_performances),
                'metrics_compared': len(all_metrics),
                'best_overall': self._find_best_overall_model(model_performances)
            }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Failed to compare models: {e}")
            raise
    
    def _find_best_overall_model(self, performances: List[ModelPerformance]) -> str:
        """Find the best overall model based on multiple metrics."""
        try:
            if not performances:
                return ""
            
            # Score each model based on key metrics
            model_scores = {}
            
            for perf in performances:
                score = 0
                metrics = perf.metrics
                
                # Weight different metrics
                if 'r2_score' in metrics:
                    score += metrics['r2_score'] * 0.3
                if 'directional_accuracy' in metrics:
                    score += metrics['directional_accuracy'] * 0.3
                if 'mape' in metrics:
                    score += (1 - min(metrics['mape'] / 100, 1)) * 0.2
                if 'f1_score' in metrics:
                    score += metrics['f1_score'] * 0.2
                
                model_scores[perf.model_id] = score
            
            return max(model_scores, key=model_scores.get)
            
        except Exception as e:
            logger.error(f"Failed to find best overall model: {e}")
            return ""
    
    async def generate_evaluation_report(
        self,
        performance: ModelPerformance
    ) -> Dict[str, Any]:
        """
        Generate comprehensive evaluation report.
        
        Args:
            performance: Model performance metrics
            
        Returns:
            Evaluation report
        """
        try:
            report = {
                'model_info': {
                    'model_id': performance.model_id,
                    'model_type': performance.model_type.value,
                    'symbol': performance.symbol,
                    'created_at': performance.created_at.isoformat(),
                    'is_active': performance.is_active
                },
                'performance_metrics': performance.metrics,
                'evaluation_summary': self._generate_summary(performance),
                'recommendations': self._generate_recommendations(performance)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate evaluation report: {e}")
            raise
    
    def _generate_summary(self, performance: ModelPerformance) -> Dict[str, Any]:
        """Generate performance summary."""
        try:
            metrics = performance.metrics
            summary = {
                'overall_rating': 'Good',
                'key_strengths': [],
                'key_weaknesses': [],
                'performance_grade': 'B'
            }
            
            # Evaluate based on key metrics
            if 'r2_score' in metrics:
                if metrics['r2_score'] > 0.8:
                    summary['key_strengths'].append('High R² score')
                elif metrics['r2_score'] < 0.5:
                    summary['key_weaknesses'].append('Low R² score')
            
            if 'directional_accuracy' in metrics:
                if metrics['directional_accuracy'] > 0.7:
                    summary['key_strengths'].append('Good directional accuracy')
                elif metrics['directional_accuracy'] < 0.6:
                    summary['key_weaknesses'].append('Poor directional accuracy')
            
            if 'mape' in metrics:
                if metrics['mape'] < 10:
                    summary['key_strengths'].append('Low prediction error')
                elif metrics['mape'] > 20:
                    summary['key_weaknesses'].append('High prediction error')
            
            # Determine overall rating
            if len(summary['key_strengths']) > len(summary['key_weaknesses']):
                summary['overall_rating'] = 'Good'
                summary['performance_grade'] = 'A' if len(summary['key_weaknesses']) == 0 else 'B'
            else:
                summary['overall_rating'] = 'Needs Improvement'
                summary['performance_grade'] = 'C'
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate summary: {e}")
            return {}
    
    def _generate_recommendations(self, performance: ModelPerformance) -> List[str]:
        """Generate improvement recommendations."""
        try:
            recommendations = []
            metrics = performance.metrics
            
            if 'r2_score' in metrics and metrics['r2_score'] < 0.6:
                recommendations.append("Consider feature engineering to improve model fit")
            
            if 'directional_accuracy' in metrics and metrics['directional_accuracy'] < 0.6:
                recommendations.append("Improve trend detection capabilities")
            
            if 'mape' in metrics and metrics['mape'] > 15:
                recommendations.append("Reduce prediction errors through better data preprocessing")
            
            if 'bias' in metrics and abs(metrics['bias']) > 0.05:
                recommendations.append("Address model bias through calibration")
            
            if not recommendations:
                recommendations.append("Model performance is satisfactory")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            return []
    
    async def cleanup(self):
        """Cleanup resources."""
        try:
            self.benchmark_models.clear()
            logger.info("Model evaluator cleanup completed")
        except Exception as e:
            logger.error(f"Error during model evaluator cleanup: {e}")
