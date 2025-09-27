# -*- coding: utf-8 -*-
"""
Main AutoGluon wrapper for NeoZork HLDP.

This module provides the main interface for AutoGluon integration
with minimal wrapper code and maximum AutoGluon utilization.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple, Union
import logging
from pathlib import Path
import warnings
import os

# Disable CUDA for MacBook M1
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["AUTOGLUON_USE_GPU"] = "false"

# AutoGluon imports
try:
    from autogluon.tabular import TabularPredictor
    AUTOGLUON_AVAILABLE = True
except ImportError:
    AUTOGLUON_AVAILABLE = False
    TabularPredictor = None

# Local imports
from .config import GluonConfig, load_gluon_config, ExperimentConfig
from .data import UniversalDataLoader, GluonPreprocessor
from .models import GluonTrainer, GluonPredictor, GluonEvaluator
from .deployment import GluonExporter, AutoRetrainer, DriftMonitor
from .utils import GluonLogger
from .analysis import ValueScoreAnalyzer
from .features.custom_feature_engineer import CustomFeatureEngineer

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class GluonAutoML:
    """
    Main AutoGluon wrapper class.
    
    This class provides a minimal wrapper around AutoGluon functionality,
    letting AutoGluon handle most of the work automatically.
    """
    
    def __init__(self, config_path: Optional[str] = None, experiment_config: Optional[Dict[str, Any]] = None):
        """
        Initialize GluonAutoML.
        
        Args:
            config_path: Path to configuration file
            experiment_config: Experiment configuration dictionary
        """
        if not AUTOGLUON_AVAILABLE:
            raise ImportError("AutoGluon is not available. Please install it with: pip install autogluon")
        
        # Load configuration
        self.config = load_gluon_config(config_path)
        self.experiment_config = ExperimentConfig.from_dict(experiment_config) if experiment_config else ExperimentConfig()
        
        # Initialize components
        self.data_loader = UniversalDataLoader(self.experiment_config.data_path, self.experiment_config.recursive_search)
        self.preprocessor = GluonPreprocessor()
        self.trainer = None
        self.predictor = None
        self.evaluator = None
        self.exporter = GluonExporter()
        self.retrainer = AutoRetrainer()
        self.drift_monitor = DriftMonitor()
        
        # Initialize logger
        self.logger = GluonLogger(self.experiment_config.log_level, self.experiment_config.log_file)
        self.logger.info("GluonAutoML initialized successfully")
    
    def load_data(self, data_path: Optional[str] = None, file_patterns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Load data from specified path or discover automatically.
        
        Args:
            data_path: Specific data path to load
            file_patterns: File patterns to match
            
        Returns:
            Loaded DataFrame
        """
        self.logger.info("Loading data...")
        
        if data_path:
            # Load specific file or directory
            data_path = Path(data_path)
            if data_path.is_file():
                df = self.data_loader.load_file(data_path)
            else:
                # Load all files in directory
                files = list(data_path.glob("**/*")) if data_path.is_dir() else []
                files = [f for f in files if f.suffix.lower() in self.data_loader.supported_formats]
                df = self.data_loader.load_multiple_files(files)
        else:
            # Auto-discover data files
            files = self.data_loader.discover_data_files()
            if file_patterns:
                files = [f for f in files if any(pattern in f.name for pattern in file_patterns)]
            df = self.data_loader.load_multiple_files(files)
        
        if df.empty:
            self.logger.warning("No data loaded")
            return df
        
        # Prepare data for AutoGluon
        df = self.preprocessor.prepare_for_gluon(df, self.experiment_config.target_column)
        
        self.logger.info(f"Data loaded successfully: {len(df)} rows, {len(df.columns)} columns")
        return df
    
    def train_models(self, train_data: pd.DataFrame, target_column: str, 
                    validation_data: Optional[pd.DataFrame] = None) -> 'GluonAutoML':
        """
        Train AutoGluon models.
        
        Args:
            train_data: Training data
            target_column: Target column name
            validation_data: Optional validation data
            
        Returns:
            Self for method chaining
        """
        self.logger.info("Starting model training...")
        
        # Create trainer
        self.trainer = GluonTrainer(self.config, self.experiment_config)
        
        # Train models
        self.predictor = self.trainer.train(train_data, target_column, validation_data)
        
        # Create evaluator
        self.evaluator = GluonEvaluator(self.predictor)
        
        self.logger.info("Model training completed successfully")
        return self
    
    def create_custom_features(self, data: pd.DataFrame, 
                              use_13_features: bool = True) -> pd.DataFrame:
        """
        Create custom features for trading strategy.
        
        Args:
            data: Input data
            use_13_features: Whether to create the 13 custom features
            
        Returns:
            Data with custom features added
        """
        if not use_13_features:
            return data
        
        self.logger.info("Creating custom trading features...")
        
        # Initialize custom feature engineer
        feature_engineer = CustomFeatureEngineer()
        
        # Create all custom features
        data_with_features = feature_engineer.create_all_features(data)
        
        # Log feature creation results
        original_features = len(data.columns)
        new_features = len(data_with_features.columns)
        custom_features = new_features - original_features
        
        self.logger.info(f"Created {custom_features} custom features")
        self.logger.info(f"Total features: {original_features} -> {new_features}")
        
        return data_with_features
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return 0.0
    
    def _get_model_info(self) -> Dict[str, Any]:
        """Get detailed model information."""
        if not self.predictor:
            return {}
        
        try:
            leaderboard = self.predictor.leaderboard(silent=True)
            return {
                "model_count": len(leaderboard),
                "best_model": leaderboard.iloc[0]['model'] if len(leaderboard) > 0 else "Unknown",
                "best_score": leaderboard.iloc[0]['score_val'] if len(leaderboard) > 0 else 0.0
            }
        except Exception:
            return {"model_count": 0, "best_model": "Unknown", "best_score": 0.0}
    
    def evaluate_models(self, test_data: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """
        Evaluate trained models.
        
        Args:
            test_data: Test data
            target_column: Target column name
            
        Returns:
            Evaluation results
        """
        if not self.predictor:
            raise ValueError("Models must be trained before evaluation")
        
        self.logger.info("Evaluating models...")
        
        # Make predictions
        predictions = self.predictor.predict(test_data)
        
        # Calculate basic metrics
        actual = test_data[target_column]
        
        # For regression, calculate RMSE instead of accuracy
        if self.predictor.problem_type == 'regression':
            from sklearn.metrics import mean_squared_error
            mse = mean_squared_error(actual, predictions)
            rmse = mse ** 0.5
            results = {
                'rmse': rmse,
                'predictions': predictions,
                'actual': actual
            }
        else:
            # For classification, calculate accuracy and probabilities
            accuracy = (predictions == actual).mean()
            probabilities = self.predictor.predict_proba(test_data) if self.predictor.can_predict_proba else None
            
            results = {
                'accuracy': accuracy,
                'predictions': predictions,
                'probabilities': probabilities,
                'actual': actual
            }
        
        # Add value scores analysis
        try:
            value_analyzer = ValueScoreAnalyzer()
            value_scores = value_analyzer.analyze(predictions, actual)
            results['value_scores'] = value_scores
        except Exception as e:
            self.logger.warning(f"Value scores analysis failed: {e}")
            results['value_scores'] = {}
        
        self.logger.info("Model evaluation completed")
        return results
    
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions on new data.
        
        Args:
            data: Input data for prediction
            
        Returns:
            Predictions DataFrame
        """
        if not self.predictor:
            raise ValueError("Models must be trained before prediction")
        
        self.logger.info("Making predictions...")
        
        # Make predictions
        predictions = self.predictor.predict(data)
        
        self.logger.info(f"Predictions completed: {len(predictions)} predictions")
        return predictions
    
    def predict_proba(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Make probability predictions on new data.
        
        Args:
            data: Input data for prediction
            
        Returns:
            Probability predictions DataFrame
        """
        if not self.predictor:
            raise ValueError("Models must be trained before prediction")
        
        if not self.predictor.can_predict_proba:
            raise ValueError(f"Probability predictions not supported for problem type: {self.predictor.problem_type}")
        
        self.logger.info("Making probability predictions...")
        
        # Make probability predictions
        probabilities = self.predictor.predict_proba(data)
        
        self.logger.info(f"Probability predictions completed: {len(probabilities)} predictions")
        return probabilities
    
    def export_models(self, export_path: Optional[str] = None) -> Dict[str, str]:
        """
        Export trained models.
        
        Args:
            export_path: Export directory path
            
        Returns:
            Export paths dictionary
        """
        if not self.predictor:
            raise ValueError("Models must be trained before export")
        
        export_path = export_path or self.experiment_config.export_path
        self.logger.info(f"Exporting models to {export_path}")
        
        # Export models
        export_paths = self.exporter.export(self.predictor, export_path, self.experiment_config.export_formats)
        
        self.logger.info("Model export completed")
        return export_paths
    
    def retrain_models(self, new_data: pd.DataFrame, target_column: str) -> 'GluonAutoML':
        """
        Retrain models with new data.
        
        Args:
            new_data: New training data
            target_column: Target column name
            
        Returns:
            Self for method chaining
        """
        self.logger.info("Retraining models with new data...")
        
        # Retrain models
        self.predictor = self.retrainer.retrain(
            self.predictor, new_data, target_column, self.config
        )
        
        # Update evaluator
        self.evaluator = GluonEvaluator(self.predictor)
        
        self.logger.info("Model retraining completed")
        return self
    
    def monitor_drift(self, new_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Monitor for data drift.
        
        Args:
            new_data: New data to check for drift
            
        Returns:
            Drift monitoring results
        """
        if not self.predictor:
            raise ValueError("Models must be trained before drift monitoring")
        
        self.logger.info("Monitoring for data drift...")
        
        # Check for drift
        drift_results = self.drift_monitor.check_drift(self.predictor, new_data)
        
        # Auto-retrain if drift detected
        if drift_results.get('drift_detected', False) and self.experiment_config.retrain_on_drift:
            self.logger.warning("Drift detected, initiating retraining...")
            # Note: This would need target data for retraining
            # self.retrain_models(new_data, target_column)
        
        self.logger.info("Drift monitoring completed")
        return drift_results
    
    def get_model_summary(self) -> Dict[str, Any]:
        """
        Get summary of trained models.
        
        Returns:
            Model summary dictionary
        """
        if not self.predictor:
            return {'error': 'No models trained'}
        
        return {
            'model_info': self.predictor.info(),
            'feature_importance': self.predictor.feature_importance(),
            'leaderboard': self.predictor.leaderboard(),
            'config': self.config.__dict__,
            'experiment_config': self.experiment_config.to_dict()
        }
    
    def create_time_series_split(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Create time series split for train/validation/test.
        
        Args:
            data: Input data
            
        Returns:
            Tuple of (train, validation, test) DataFrames
        """
        return self.preprocessor.create_time_series_split(
            data,
            self.experiment_config.train_ratio,
            self.experiment_config.validation_ratio,
            self.experiment_config.test_ratio
        )
    
    def get_data_summary(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Get data summary and quality information.
        
        Args:
            data: Input DataFrame
            
        Returns:
            Data summary dictionary
        """
        summary = self.preprocessor.get_data_summary(data)
        quality_issues = self.preprocessor.detect_data_quality_issues(data)
        
        summary['quality_issues'] = quality_issues
        summary['is_ready_for_gluon'] = len(quality_issues) == 0
        
        return summary
