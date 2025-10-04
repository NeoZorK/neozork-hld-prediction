"""
Model Analysis Module for Trading Strategy Evaluation
"""

import pandas as pd
import numpy as np
import pickle
import os
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ModelAnalyzer:
    """
    Analyzes trained models for backtesting, walk forward, and Monte Carlo analysis.
    """
    
    def __init__(self, model_path: str):
        """
        Initialize Model Analyzer.
        
        Args:
            model_path: Path to the trained model directory
        """
        self.model_path = Path(model_path)
        self.predictor = None
        self.model_info = {}
        
    def load_model(self) -> bool:
        """
        Load the trained model.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            from autogluon.tabular import TabularPredictor
            self.predictor = TabularPredictor.load(str(self.model_path))
            self.model_info = self._extract_model_info()
            logger.info(f"Model loaded successfully from {self.model_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def _extract_model_info(self) -> Dict[str, Any]:
        """Extract model information."""
        if not self.predictor:
            return {}
        
        try:
            leaderboard = self.predictor.leaderboard(silent=True)
            return {
                "model_count": len(leaderboard),
                "best_model": leaderboard.iloc[0]['model'] if len(leaderboard) > 0 else "Unknown",
                "best_score": leaderboard.iloc[0]['score_val'] if len(leaderboard) > 0 else 0.0,
                "problem_type": self.predictor.problem_type,
                "feature_count": len(self.predictor.feature_metadata_in.feature_metadata),
                "training_time": leaderboard.iloc[0]['fit_time'] if len(leaderboard) > 0 else 0.0
            }
        except Exception as e:
            logger.warning(f"Could not extract model info: {e}")
            return {}
    
    def backtest_analysis(self, data: pd.DataFrame, 
                         target_column: str,
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform backtesting analysis.
        
        Args:
            data: Historical data for backtesting
            target_column: Target column name
            start_date: Start date for backtesting
            end_date: End date for backtesting
            
        Returns:
            Backtesting results
        """
        if not self.predictor:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        logger.info("Starting backtesting analysis...")
        
        # Filter data by date range if provided
        if start_date or end_date:
            data = self._filter_by_date(data, start_date, end_date)
        
        # Make predictions
        predictions = self.predictor.predict(data)
        probabilities = self.predictor.predict_proba(data) if hasattr(self.predictor, 'predict_proba') else None
        
        # Calculate backtesting metrics
        results = {
            "total_trades": len(data),
            "predictions": predictions,
            "probabilities": probabilities,
            "data_period": {
                "start": data.index.min() if hasattr(data.index, 'min') else "Unknown",
                "end": data.index.max() if hasattr(data.index, 'max') else "Unknown"
            },
            "model_performance": self._calculate_performance_metrics(data[target_column], predictions)
        }
        
        logger.info("Backtesting analysis completed")
        return results
    
    def walk_forward_analysis(self, data: pd.DataFrame,
                             target_column: str,
                             train_window: int = 1000,
                             test_window: int = 100,
                             step_size: int = 50) -> Dict[str, Any]:
        """
        Perform walk forward analysis.
        
        Args:
            data: Historical data
            target_column: Target column name
            train_window: Training window size
            test_window: Test window size
            step_size: Step size for moving window
            
        Returns:
            Walk forward analysis results
        """
        if not self.predictor:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        logger.info("Starting walk forward analysis...")
        
        results = []
        total_windows = (len(data) - train_window - test_window) // step_size + 1
        
        for i in range(0, len(data) - train_window - test_window + 1, step_size):
            # Define windows
            train_start = i
            train_end = i + train_window
            test_start = train_end
            test_end = test_start + test_window
            
            if test_end > len(data):
                break
            
            # Get train and test data
            train_data = data.iloc[train_start:train_end]
            test_data = data.iloc[test_start:test_end]
            
            # Make predictions on test data
            test_predictions = self.predictor.predict(test_data)
            
            # Calculate performance for this window
            window_performance = self._calculate_performance_metrics(
                test_data[target_column], test_predictions
            )
            
            results.append({
                "window": i // step_size + 1,
                "train_period": (train_start, train_end),
                "test_period": (test_start, test_end),
                "performance": window_performance
            })
        
        logger.info(f"Walk forward analysis completed: {len(results)} windows")
        return {
            "total_windows": len(results),
            "window_results": results,
            "summary": self._summarize_walk_forward(results)
        }
    
    def monte_carlo_analysis(self, data: pd.DataFrame,
                            target_column: str,
                            n_simulations: int = 1000,
                            sample_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Perform Monte Carlo analysis.
        
        Args:
            data: Historical data
            target_column: Target column name
            n_simulations: Number of Monte Carlo simulations
            sample_size: Size of each sample (default: 20% of data)
            
        Returns:
            Monte Carlo analysis results
        """
        if not self.predictor:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        logger.info(f"Starting Monte Carlo analysis with {n_simulations} simulations...")
        
        if sample_size is None:
            sample_size = len(data) // 5
        
        results = []
        
        for i in range(n_simulations):
            # Random sampling
            sample_indices = np.random.choice(len(data), size=sample_size, replace=False)
            sample_data = data.iloc[sample_indices]
            
            # Make predictions
            predictions = self.predictor.predict(sample_data)
            
            # Calculate performance
            performance = self._calculate_performance_metrics(
                sample_data[target_column], predictions
            )
            
            results.append(performance)
        
        # Analyze results
        monte_carlo_results = {
            "n_simulations": n_simulations,
            "sample_size": sample_size,
            "results": results,
            "statistics": self._calculate_monte_carlo_statistics(results)
        }
        
        logger.info("Monte Carlo analysis completed")
        return monte_carlo_results
    
    def retrain_model(self, new_data: pd.DataFrame,
                     target_column: str,
                     retrain_threshold: float = 0.05) -> bool:
        """
        Retrain model if performance degradation is detected.
        
        Args:
            new_data: New data for retraining
            target_column: Target column name
            retrain_threshold: Performance degradation threshold
            
        Returns:
            True if retraining was performed, False otherwise
        """
        if not self.predictor:
            logger.error("Model not loaded")
            return False
        
        logger.info("Checking if model retraining is needed...")
        
        # Evaluate current model performance on new data
        current_predictions = self.predictor.predict(new_data)
        current_performance = self._calculate_performance_metrics(
            new_data[target_column], current_predictions
        )
        
        # Compare with historical performance
        if current_performance.get('accuracy', 0) < (1 - retrain_threshold):
            logger.info("Performance degradation detected. Retraining model...")
            
            # Retrain model
            try:
                self.predictor.fit(new_data, label=target_column)
                logger.info("Model retraining completed successfully")
                return True
            except Exception as e:
                logger.error(f"Model retraining failed: {e}")
                return False
        else:
            logger.info("No retraining needed. Model performance is acceptable.")
            return False
    
    def _filter_by_date(self, data: pd.DataFrame, 
                       start_date: Optional[str], 
                       end_date: Optional[str]) -> pd.DataFrame:
        """Filter data by date range."""
        if 'timestamp' in data.columns:
            data = data.copy()
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            data = data.set_index('timestamp')
        
        if start_date:
            data = data[data.index >= start_date]
        if end_date:
            data = data[data.index <= end_date]
        
        return data
    
    def _calculate_performance_metrics(self, actual: pd.Series, 
                                    predictions: pd.Series) -> Dict[str, float]:
        """Calculate performance metrics."""
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        try:
            return {
                "accuracy": accuracy_score(actual, predictions),
                "precision": precision_score(actual, predictions, average='weighted', zero_division=0),
                "recall": recall_score(actual, predictions, average='weighted', zero_division=0),
                "f1_score": f1_score(actual, predictions, average='weighted', zero_division=0)
            }
        except Exception as e:
            logger.warning(f"Could not calculate metrics: {e}")
            return {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1_score": 0.0}
    
    def _summarize_walk_forward(self, results: List[Dict]) -> Dict[str, Any]:
        """Summarize walk forward results."""
        if not results:
            return {}
        
        accuracies = [r["performance"]["accuracy"] for r in results]
        
        return {
            "mean_accuracy": np.mean(accuracies),
            "std_accuracy": np.std(accuracies),
            "min_accuracy": np.min(accuracies),
            "max_accuracy": np.max(accuracies),
            "stability": 1 - np.std(accuracies)  # Higher is more stable
        }
    
    def _calculate_monte_carlo_statistics(self, results: List[Dict]) -> Dict[str, Any]:
        """Calculate Monte Carlo statistics."""
        if not results:
            return {}
        
        accuracies = [r["accuracy"] for r in results]
        
        return {
            "mean_accuracy": np.mean(accuracies),
            "std_accuracy": np.std(accuracies),
            "confidence_interval_95": {
                "lower": np.percentile(accuracies, 2.5),
                "upper": np.percentile(accuracies, 97.5)
            },
            "confidence_interval_99": {
                "lower": np.percentile(accuracies, 0.5),
                "upper": np.percentile(accuracies, 99.5)
            }
        }
