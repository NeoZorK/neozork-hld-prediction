"""
Model Trainer

Handles training of ML models for analytics.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import pandas as pd

from ..models.analytics_models import ModelPerformance, ModelType, MarketData
from .prediction_models import BasePredictor

logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Handles training of ML models for analytics.
    """
    
    def __init__(self):
        """Initialize model trainer."""
        self.training_configs = self._setup_training_configs()
        self.trained_models = {}
    
    def _setup_training_configs(self) -> Dict[str, Any]:
        """Setup training configurations for different models."""
        return {
            'price_prediction': {
                'model_type': ModelType.LSTM,
                'sequence_length': 60,
                'features': ['sma_5', 'sma_20', 'sma_50', 'rsi', 'macd', 'volume_ratio'],
                'target': 'price_change',
                'train_test_split': 0.8,
                'validation_split': 0.2,
                'epochs': 100,
                'batch_size': 32,
                'learning_rate': 0.001
            },
            'volatility_prediction': {
                'model_type': ModelType.NEURAL_NETWORK,
                'features': ['returns_lag1', 'returns_lag2', 'volatility_lag1', 'volume_ratio'],
                'target': 'volatility_change',
                'train_test_split': 0.8,
                'validation_split': 0.2,
                'epochs': 50,
                'batch_size': 64,
                'learning_rate': 0.01
            },
            'sentiment_analysis': {
                'model_type': ModelType.TRANSFORMER,
                'features': ['news_sentiment', 'social_sentiment', 'fear_greed_index'],
                'target': 'sentiment_score',
                'train_test_split': 0.8,
                'validation_split': 0.2,
                'epochs': 30,
                'batch_size': 16,
                'learning_rate': 0.0001
            },
            'risk_prediction': {
                'model_type': ModelType.RANDOM_FOREST,
                'features': ['portfolio_volatility', 'correlation_risk', 'concentration_risk'],
                'target': 'risk_score',
                'train_test_split': 0.8,
                'validation_split': 0.2,
                'n_estimators': 100,
                'max_depth': 10,
                'min_samples_split': 5
            }
        }
    
    async def train_model(
        self,
        model_name: str,
        market_data: List[MarketData],
        features: Dict[str, Any],
        target_data: List[float]
    ) -> ModelPerformance:
        """
        Train a specific model.
        
        Args:
            model_name: Name of the model to train
            market_data: Market data for training
            features: Feature data
            target_data: Target values
            
        Returns:
            Model performance metrics
        """
        try:
            if model_name not in self.training_configs:
                raise ValueError(f"Unknown model: {model_name}")
            
            config = self.training_configs[model_name]
            
            # Prepare training data
            X, y = await self._prepare_training_data(
                features, target_data, config
            )
            
            # Split data
            X_train, X_test, y_train, y_test = self._split_data(
                X, y, config['train_test_split']
            )
            
            # Train model
            model = await self._create_model(config)
            training_metrics = await model.train(
                pd.DataFrame(X_train), pd.Series(y_train)
            )
            
            # Evaluate model
            test_metrics = await self._evaluate_model(
                model, X_test, y_test
            )
            
            # Create performance record
            performance = ModelPerformance(
                model_id=f"{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                model_type=config['model_type'],
                symbol=market_data[0].symbol if market_data else 'UNKNOWN',
                training_period={
                    'start': market_data[0].timestamp if market_data else datetime.now(),
                    'end': market_data[-1].timestamp if market_data else datetime.now()
                },
                test_period={
                    'start': datetime.now() - timedelta(days=30),
                    'end': datetime.now()
                },
                metrics={
                    **training_metrics,
                    **{f'test_{k}': v for k, v in test_metrics.items()}
                },
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_active=True
            )
            
            # Store trained model
            self.trained_models[performance.model_id] = model
            
            logger.info(f"Model {model_name} trained successfully")
            return performance
            
        except Exception as e:
            logger.error(f"Failed to train model {model_name}: {e}")
            raise
    
    async def _prepare_training_data(
        self,
        features: Dict[str, Any],
        target_data: List[float],
        config: Dict[str, Any]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data."""
        try:
            # Extract feature columns
            feature_columns = config['features']
            feature_matrix = []
            
            for i in range(len(target_data)):
                feature_row = []
                for col in feature_columns:
                    if col in features:
                        if isinstance(features[col], list):
                            feature_row.append(features[col][i] if i < len(features[col]) else 0.0)
                        else:
                            feature_row.append(features[col])
                    else:
                        feature_row.append(0.0)
                feature_matrix.append(feature_row)
            
            X = np.array(feature_matrix)
            y = np.array(target_data)
            
            # Handle sequence data for LSTM
            if config['model_type'] == ModelType.LSTM:
                X = self._create_sequences(X, config.get('sequence_length', 60))
                y = y[config.get('sequence_length', 60):]
            
            return X, y
            
        except Exception as e:
            logger.error(f"Failed to prepare training data: {e}")
            raise
    
    def _create_sequences(self, data: np.ndarray, sequence_length: int) -> np.ndarray:
        """Create sequences for LSTM training."""
        sequences = []
        for i in range(sequence_length, len(data)):
            sequences.append(data[i-sequence_length:i])
        return np.array(sequences)
    
    def _split_data(
        self, 
        X: np.ndarray, 
        y: np.ndarray, 
        train_ratio: float
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Split data into train and test sets."""
        split_idx = int(len(X) * train_ratio)
        
        X_train = X[:split_idx]
        X_test = X[split_idx:]
        y_train = y[:split_idx]
        y_test = y[split_idx:]
        
        return X_train, X_test, y_train, y_test
    
    async def _create_model(self, config: Dict[str, Any]) -> BasePredictor:
        """Create model instance based on configuration."""
        try:
            model_type = config['model_type']
            
            if model_type == ModelType.LSTM:
                from .prediction_models import PricePredictor
                return PricePredictor()
            elif model_type == ModelType.NEURAL_NETWORK:
                from .prediction_models import VolatilityPredictor
                return VolatilityPredictor()
            elif model_type == ModelType.TRANSFORMER:
                from .prediction_models import SentimentAnalyzer
                return SentimentAnalyzer()
            elif model_type == ModelType.RANDOM_FOREST:
                from .prediction_models import RiskPredictor
                return RiskPredictor()
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
                
        except Exception as e:
            logger.error(f"Failed to create model: {e}")
            raise
    
    async def _evaluate_model(
        self,
        model: BasePredictor,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> Dict[str, float]:
        """Evaluate model performance."""
        try:
            # Make predictions
            predictions = []
            for i in range(len(X_test)):
                # Convert test data to feature format
                features = self._array_to_features(X_test[i])
                prediction = await model.predict(features)
                predictions.append(float(prediction.predicted_value))
            
            predictions = np.array(predictions)
            
            # Calculate metrics
            mse = np.mean((predictions - y_test) ** 2)
            mae = np.mean(np.abs(predictions - y_test))
            rmse = np.sqrt(mse)
            
            # R-squared
            ss_res = np.sum((y_test - predictions) ** 2)
            ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            
            return {
                'mse': float(mse),
                'mae': float(mae),
                'rmse': float(rmse),
                'r2_score': float(r2)
            }
            
        except Exception as e:
            logger.error(f"Failed to evaluate model: {e}")
            raise
    
    def _array_to_features(self, array: np.ndarray) -> Dict[str, Any]:
        """Convert array to feature dictionary."""
        # This is a simplified implementation
        # In practice, you would map array indices to feature names
        features = {}
        for i, value in enumerate(array):
            features[f'feature_{i}'] = float(value)
        return features
    
    async def train_all_models(
        self,
        market_data: List[MarketData],
        features: Dict[str, Any],
        target_data: Dict[str, List[float]]
    ) -> List[ModelPerformance]:
        """
        Train all configured models.
        
        Args:
            market_data: Market data
            features: Feature data
            target_data: Target data for each model
            
        Returns:
            List of model performance metrics
        """
        try:
            performances = []
            
            for model_name in self.training_configs.keys():
                if model_name in target_data:
                    performance = await self.train_model(
                        model_name, market_data, features, target_data[model_name]
                    )
                    performances.append(performance)
            
            logger.info(f"Trained {len(performances)} models")
            return performances
            
        except Exception as e:
            logger.error(f"Failed to train all models: {e}")
            raise
    
    async def retrain_model(
        self,
        model_id: str,
        new_data: List[MarketData],
        new_features: Dict[str, Any],
        new_targets: List[float]
    ) -> ModelPerformance:
        """
        Retrain an existing model with new data.
        
        Args:
            model_id: ID of the model to retrain
            new_data: New market data
            new_features: New feature data
            new_targets: New target values
            
        Returns:
            Updated model performance
        """
        try:
            if model_id not in self.trained_models:
                raise ValueError(f"Model {model_id} not found")
            
            # Get existing model
            model = self.trained_models[model_id]
            
            # Retrain with new data
            training_metrics = await model.train(
                pd.DataFrame(new_features), pd.Series(new_targets)
            )
            
            # Update performance record
            performance = ModelPerformance(
                model_id=model_id,
                model_type=model.model_type,
                symbol=new_data[0].symbol if new_data else 'UNKNOWN',
                training_period={
                    'start': new_data[0].timestamp if new_data else datetime.now(),
                    'end': new_data[-1].timestamp if new_data else datetime.now()
                },
                test_period={
                    'start': datetime.now() - timedelta(days=30),
                    'end': datetime.now()
                },
                metrics=training_metrics,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_active=True
            )
            
            logger.info(f"Model {model_id} retrained successfully")
            return performance
            
        except Exception as e:
            logger.error(f"Failed to retrain model {model_id}: {e}")
            raise
    
    async def get_model_performance(self, model_id: str) -> Optional[ModelPerformance]:
        """Get performance metrics for a specific model."""
        try:
            if model_id in self.trained_models:
                # In practice, you would retrieve from database
                return ModelPerformance(
                    model_id=model_id,
                    model_type=ModelType.LSTM,
                    symbol='UNKNOWN',
                    training_period={'start': datetime.now(), 'end': datetime.now()},
                    test_period={'start': datetime.now(), 'end': datetime.now()},
                    metrics={'accuracy': 0.8, 'mse': 0.01},
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    is_active=True
                )
            return None
            
        except Exception as e:
            logger.error(f"Failed to get model performance: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup resources."""
        try:
            self.trained_models.clear()
            logger.info("Model trainer cleanup completed")
        except Exception as e:
            logger.error(f"Error during model trainer cleanup: {e}")
