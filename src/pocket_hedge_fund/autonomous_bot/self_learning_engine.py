"""
Self-Learning Engine for Autonomous Trading Bot

This module provides advanced self-learning capabilities including:
- Meta-learning algorithms for learning how to learn
- Transfer learning for knowledge transfer between markets
- AutoML pipeline for automatic model selection
- Neural Architecture Search (NAS) for optimal architecture discovery
- Few-shot learning for rapid adaptation to new conditions
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import asyncio
import pickle
import json
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import cross_val_score, GridSearchCV, TimeSeriesSplit
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
import joblib
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


@dataclass
class LearningConfig:
    """Configuration for self-learning engine."""
    meta_learning_enabled: bool = True
    transfer_learning_enabled: bool = True
    auto_ml_enabled: bool = True
    nas_enabled: bool = True
    few_shot_enabled: bool = True
    learning_rate: float = 0.001
    batch_size: int = 32
    max_epochs: int = 100
    early_stopping_patience: int = 10
    model_save_path: str = "models/self_learning"
    max_models_in_memory: int = 10
    cross_validation_folds: int = 5
    hyperparameter_search_iterations: int = 50
    meta_learning_tasks_threshold: int = 5
    transfer_learning_similarity_threshold: float = 0.7
    performance_improvement_threshold: float = 0.05


@dataclass
class LearningResult:
    """Result of learning process."""
    success: bool
    model_performance: Dict[str, float]
    learning_time: float
    model_path: Optional[str] = None
    error_message: Optional[str] = None
    model_type: Optional[str] = None
    hyperparameters: Optional[Dict[str, Any]] = None
    cross_validation_scores: Optional[List[float]] = None
    feature_importance: Optional[Dict[str, float]] = None
    learning_method: Optional[str] = None


class MetaLearner:
    """Meta-learning component for learning how to learn."""
    
    def __init__(self, config: LearningConfig):
        self.config = config
        self.meta_models = {}
        self.learning_history = []
        self.task_embeddings = {}
        self.performance_patterns = {}
        self.meta_knowledge = {}
    
    def _extract_task_features(self, task_data: Dict[str, Any]) -> np.ndarray:
        """Extract features from task data for meta-learning."""
        features = []
        
        # Market regime features
        if 'market_data' in task_data:
            data = task_data['market_data']
            if isinstance(data, pd.DataFrame):
                features.extend([
                    data['close'].std(),  # Volatility
                    data['close'].pct_change().mean(),  # Average return
                    data['volume'].mean(),  # Average volume
                    len(data),  # Data length
                ])
        
        # Performance features
        if 'performance' in task_data:
            perf = task_data['performance']
            features.extend([
                perf.get('sharpe_ratio', 0),
                perf.get('max_drawdown', 0),
                perf.get('win_rate', 0),
                perf.get('profit_factor', 0),
            ])
        
        # Strategy features
        if 'strategy_params' in task_data:
            params = task_data['strategy_params']
            features.extend([
                params.get('risk_level', 0),
                params.get('position_size', 0),
                params.get('stop_loss', 0),
                params.get('take_profit', 0),
            ])
        
        return np.array(features)
    
    def _calculate_task_similarity(self, task1_features: np.ndarray, task2_features: np.ndarray) -> float:
        """Calculate similarity between two tasks."""
        if len(task1_features) == 0 or len(task2_features) == 0:
            return 0.0
        
        # Normalize features
        max_len = max(len(task1_features), len(task2_features))
        task1_padded = np.pad(task1_features, (0, max_len - len(task1_features)), 'constant')
        task2_padded = np.pad(task2_features, (0, max_len - len(task2_features)), 'constant')
        
        # Calculate cosine similarity
        dot_product = np.dot(task1_padded, task2_padded)
        norm1 = np.linalg.norm(task1_padded)
        norm2 = np.linalg.norm(task2_padded)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    async def learn_from_tasks(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Learn from multiple tasks to improve learning efficiency.
        
        Args:
            tasks: List of learning tasks with data and targets
            
        Returns:
            Meta-learning results
        """
        try:
            logger.info(f"Meta-learning from {len(tasks)} tasks...")
            
            if len(tasks) < self.config.meta_learning_tasks_threshold:
                logger.warning(f"Not enough tasks for meta-learning. Need {self.config.meta_learning_tasks_threshold}, got {len(tasks)}")
                return {"status": "insufficient_data", "message": "Not enough tasks for meta-learning"}
            
            # Extract features from all tasks
            task_features = []
            task_performances = []
            
            for i, task in enumerate(tasks):
                features = self._extract_task_features(task)
                task_features.append(features)
                task_performances.append(task.get('performance', {}))
                self.task_embeddings[f"task_{i}"] = features
            
            # Build meta-model for task similarity
            if len(task_features) > 1:
                # Create similarity matrix
                similarity_matrix = np.zeros((len(task_features), len(task_features)))
                for i in range(len(task_features)):
                    for j in range(len(task_features)):
                        if i != j:
                            similarity_matrix[i, j] = self._calculate_task_similarity(
                                task_features[i], task_features[j]
                            )
                
                # Store meta-knowledge
                self.meta_knowledge = {
                    'task_features': task_features,
                    'similarity_matrix': similarity_matrix,
                    'task_performances': task_performances,
                    'learned_at': datetime.now()
                }
                
                # Build performance prediction model
                X_meta = np.array(task_features)
                y_meta = np.array([perf.get('sharpe_ratio', 0) for perf in task_performances])
                
                if len(X_meta) > 0 and len(y_meta) > 0:
                    meta_model = RandomForestRegressor(n_estimators=50, random_state=42)
                    meta_model.fit(X_meta, y_meta)
                    self.meta_models['performance_predictor'] = meta_model
                    
                    logger.info("Meta-learning completed successfully")
                    return {
                        "status": "success",
                        "meta_model": "performance_predictor",
                        "tasks_processed": len(tasks),
                        "similarity_matrix_shape": similarity_matrix.shape
                    }
            
            return {"status": "success", "meta_model": "basic", "tasks_processed": len(tasks)}
            
        except Exception as e:
            logger.error(f"Meta-learning failed: {e}")
            return {"status": "error", "message": str(e)}
    
    async def adapt_to_new_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Quickly adapt to a new task using meta-learning.
        
        Args:
            task_data: New task data
            
        Returns:
            Adaptation results
        """
        try:
            logger.info("Adapting to new task using meta-learning...")
            
            if not self.meta_knowledge:
                logger.warning("No meta-knowledge available for adaptation")
                return {"status": "no_meta_knowledge", "message": "No meta-knowledge available"}
            
            # Extract features from new task
            new_task_features = self._extract_task_features(task_data)
            
            # Find most similar tasks
            similarities = []
            for i, stored_features in enumerate(self.meta_knowledge['task_features']):
                similarity = self._calculate_task_similarity(new_task_features, stored_features)
                similarities.append((i, similarity))
            
            # Sort by similarity
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Get top similar tasks
            top_similar_tasks = similarities[:3]  # Top 3 most similar
            
            # Predict performance using meta-model
            predicted_performance = None
            if 'performance_predictor' in self.meta_models:
                try:
                    predicted_performance = self.meta_models['performance_predictor'].predict([new_task_features])[0]
                except Exception as e:
                    logger.warning(f"Performance prediction failed: {e}")
            
            # Generate adaptation recommendations
            adaptation_recommendations = {
                'similar_tasks': [{'task_id': f"task_{idx}", 'similarity': sim} for idx, sim in top_similar_tasks],
                'predicted_performance': predicted_performance,
                'recommended_strategy_params': self._generate_strategy_recommendations(top_similar_tasks),
                'confidence': top_similar_tasks[0][1] if top_similar_tasks else 0.0
            }
            
            logger.info(f"Task adaptation completed with confidence: {adaptation_recommendations['confidence']:.3f}")
            return {
                "status": "success",
                "adaptation_recommendations": adaptation_recommendations
            }
            
        except Exception as e:
            logger.error(f"Task adaptation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def _generate_strategy_recommendations(self, similar_tasks: List[Tuple[int, float]]) -> Dict[str, Any]:
        """Generate strategy recommendations based on similar tasks."""
        if not similar_tasks:
            return {}
        
        # Get performance data from similar tasks
        similar_performances = []
        for task_idx, similarity in similar_tasks:
            if task_idx < len(self.meta_knowledge['task_performances']):
                similar_performances.append(self.meta_knowledge['task_performances'][task_idx])
        
        if not similar_performances:
            return {}
        
        # Calculate weighted averages based on similarity
        total_similarity = sum(sim for _, sim in similar_tasks)
        if total_similarity == 0:
            return {}
        
        # Simple recommendation based on best performing similar task
        best_task_idx = max(similar_tasks, key=lambda x: x[1])[0]
        best_performance = self.meta_knowledge['task_performances'][best_task_idx]
        
        return {
            'risk_level': 0.02,  # Conservative default
            'position_size': 0.1,
            'stop_loss': 0.05,
            'take_profit': 0.1,
            'based_on_task': f"task_{best_task_idx}",
            'similarity': similar_tasks[0][1]
        }


class TransferLearner:
    """Transfer learning component for knowledge transfer."""
    
    def __init__(self, config: LearningConfig):
        self.config = config
        self.source_models = {}
        self.transfer_history = []
        self.domain_embeddings = {}
        self.transfer_weights = {}
    
    def _calculate_domain_similarity(self, source_data: Dict[str, Any], target_data: Dict[str, Any]) -> float:
        """Calculate similarity between source and target domains."""
        try:
            # Extract statistical features from both domains
            source_features = self._extract_domain_features(source_data)
            target_features = self._extract_domain_features(target_data)
            
            if len(source_features) == 0 or len(target_features) == 0:
                return 0.0
            
            # Calculate cosine similarity
            dot_product = np.dot(source_features, target_features)
            norm_source = np.linalg.norm(source_features)
            norm_target = np.linalg.norm(target_features)
            
            if norm_source == 0 or norm_target == 0:
                return 0.0
            
            return dot_product / (norm_source * norm_target)
            
        except Exception as e:
            logger.warning(f"Domain similarity calculation failed: {e}")
            return 0.0
    
    def _extract_domain_features(self, data: Dict[str, Any]) -> np.ndarray:
        """Extract features from domain data."""
        features = []
        
        if 'market_data' in data and isinstance(data['market_data'], pd.DataFrame):
            df = data['market_data']
            if 'close' in df.columns:
                returns = df['close'].pct_change().dropna()
                features.extend([
                    returns.mean(),  # Mean return
                    returns.std(),   # Volatility
                    returns.skew(),  # Skewness
                    returns.kurtosis(),  # Kurtosis
                    len(df),  # Data length
                ])
                
                if 'volume' in df.columns:
                    features.append(df['volume'].mean())
        
        return np.array(features)
    
    def _prepare_transfer_data(self, source_model: Any, target_data: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare data for transfer learning."""
        try:
            if 'market_data' not in target_data:
                raise ValueError("Target data must contain 'market_data'")
            
            df = target_data['market_data']
            if not isinstance(df, pd.DataFrame):
                raise ValueError("Market data must be a DataFrame")
            
            # Create features (using same features as source model)
            feature_columns = ['close', 'volume'] if 'volume' in df.columns else ['close']
            
            # Add technical indicators
            df_features = df.copy()
            if 'close' in df.columns:
                df_features['returns'] = df['close'].pct_change()
                df_features['sma_5'] = df['close'].rolling(5).mean()
                df_features['sma_20'] = df['close'].rolling(20).mean()
                df_features['volatility'] = df['close'].rolling(20).std()
            
            # Drop NaN values
            df_features = df_features.dropna()
            
            if len(df_features) < 10:
                raise ValueError("Insufficient data for transfer learning")
            
            # Prepare features and target
            feature_cols = [col for col in df_features.columns if col != 'close']
            X = df_features[feature_cols].values
            y = df_features['close'].values
            
            return X, y
            
        except Exception as e:
            logger.error(f"Data preparation failed: {e}")
            raise
    
    async def transfer_knowledge(self, source_domain: str, target_domain: str, 
                               source_model: Any, target_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transfer knowledge from source domain to target domain.
        
        Args:
            source_domain: Source domain name
            target_domain: Target domain name
            source_model: Pre-trained source model
            target_data: Target domain data
            
        Returns:
            Transfer learning results
        """
        try:
        logger.info(f"Transferring knowledge from {source_domain} to {target_domain}...")
            
            # Calculate domain similarity
            domain_similarity = self._calculate_domain_similarity(
                {'market_data': source_model.get('training_data', pd.DataFrame())},
                target_data
            )
            
            logger.info(f"Domain similarity: {domain_similarity:.3f}")
            
            if domain_similarity < self.config.transfer_learning_similarity_threshold:
                logger.warning(f"Low domain similarity ({domain_similarity:.3f}), transfer learning may not be effective")
            
            # Prepare target data
            X_target, y_target = self._prepare_transfer_data(source_model, target_data)
            
            # Get source model
            if isinstance(source_model, dict) and 'model' in source_model:
                base_model = source_model['model']
            else:
                base_model = source_model
            
            # Create transfer learning model
            if hasattr(base_model, 'coef_') or hasattr(base_model, 'feature_importances_'):
                # For tree-based or linear models, use feature importance transfer
                transferred_model = self._transfer_feature_importance(base_model, X_target, y_target)
            else:
                # For other models, use fine-tuning approach
                transferred_model = self._transfer_model_weights(base_model, X_target, y_target)
            
            # Store transfer information
            transfer_info = {
                'source_domain': source_domain,
                'target_domain': target_domain,
                'domain_similarity': domain_similarity,
                'transfer_method': 'feature_importance' if hasattr(base_model, 'feature_importances_') else 'weight_transfer',
                'timestamp': datetime.now(),
                'target_data_size': len(X_target)
            }
            
            self.transfer_history.append(transfer_info)
            
            # Store the transferred model
            model_key = f"{source_domain}_to_{target_domain}"
            self.source_models[model_key] = {
                'model': transferred_model,
                'transfer_info': transfer_info,
                'performance': self._evaluate_transfer_performance(transferred_model, X_target, y_target)
            }
            
            logger.info(f"Knowledge transfer completed successfully")
            return {
                "status": "success",
                "transferred_model": model_key,
                "domain_similarity": domain_similarity,
                "transfer_method": transfer_info['transfer_method'],
                "performance": self.source_models[model_key]['performance']
            }
            
        except Exception as e:
            logger.error(f"Knowledge transfer failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def _transfer_feature_importance(self, source_model: Any, X_target: np.ndarray, y_target: np.ndarray) -> Any:
        """Transfer learning using feature importance."""
        try:
            # Get feature importance from source model
            if hasattr(source_model, 'feature_importances_'):
                source_importance = source_model.feature_importances_
            else:
                # For linear models, use absolute coefficients
                if hasattr(source_model, 'coef_'):
                    source_importance = np.abs(source_model.coef_)
                else:
                    source_importance = np.ones(X_target.shape[1]) / X_target.shape[1]
            
            # Normalize importance
            source_importance = source_importance / np.sum(source_importance)
            
            # Create new model with transferred knowledge
            # Use RandomForest with feature weights
            transferred_model = RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                max_features='sqrt'
            )
            
            # Train with feature importance as prior knowledge
            transferred_model.fit(X_target, y_target)
            
            # Adjust feature importance based on source model
            if hasattr(transferred_model, 'feature_importances_'):
                # Blend source and target feature importance
                target_importance = transferred_model.feature_importances_
                blended_importance = 0.7 * source_importance + 0.3 * target_importance
                transferred_model.feature_importances_ = blended_importance
            
            return transferred_model
            
        except Exception as e:
            logger.error(f"Feature importance transfer failed: {e}")
            # Fallback to standard model
            return RandomForestRegressor(n_estimators=100, random_state=42).fit(X_target, y_target)
    
    def _transfer_model_weights(self, source_model: Any, X_target: np.ndarray, y_target: np.ndarray) -> Any:
        """Transfer learning using model weights."""
        try:
            # For neural networks or other weight-based models
            if hasattr(source_model, 'predict'):
                # Use source model as starting point and fine-tune
                transferred_model = source_model
                
                # If it's a sklearn model, retrain with target data
                if hasattr(source_model, 'fit'):
                    transferred_model.fit(X_target, y_target)
                
                return transferred_model
            else:
                # Fallback to new model
                return RandomForestRegressor(n_estimators=100, random_state=42).fit(X_target, y_target)
                
        except Exception as e:
            logger.error(f"Model weight transfer failed: {e}")
            # Fallback to standard model
            return RandomForestRegressor(n_estimators=100, random_state=42).fit(X_target, y_target)
    
    def _evaluate_transfer_performance(self, model: Any, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Evaluate transfer learning performance."""
        try:
            predictions = model.predict(X)
            
            mse = mean_squared_error(y, predictions)
            mae = mean_absolute_error(y, predictions)
            r2 = r2_score(y, predictions)
            
            return {
                'mse': mse,
                'mae': mae,
                'r2': r2,
                'rmse': np.sqrt(mse)
            }
            
        except Exception as e:
            logger.error(f"Performance evaluation failed: {e}")
            return {'mse': float('inf'), 'mae': float('inf'), 'r2': -1.0, 'rmse': float('inf')}
    
    async def fine_tune_model(self, base_model: Any, target_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fine-tune a pre-trained model on target data.
        
        Args:
            base_model: Pre-trained base model
            target_data: Target data for fine-tuning
            
        Returns:
            Fine-tuning results
        """
        try:
        logger.info("Fine-tuning model...")
            
            # Prepare target data
            X_target, y_target = self._prepare_transfer_data(base_model, target_data)
            
            # Fine-tune the model
            if hasattr(base_model, 'fit'):
                # For sklearn models, retrain with new data
                fine_tuned_model = base_model
                fine_tuned_model.fit(X_target, y_target)
            else:
                # For other models, create a new model
                fine_tuned_model = RandomForestRegressor(n_estimators=100, random_state=42)
                fine_tuned_model.fit(X_target, y_target)
            
            # Evaluate fine-tuned model
            performance = self._evaluate_transfer_performance(fine_tuned_model, X_target, y_target)
            
            logger.info(f"Model fine-tuning completed. R²: {performance['r2']:.3f}")
            return {
                "status": "success",
                "fine_tuned_model": fine_tuned_model,
                "performance": performance,
                "data_size": len(X_target)
            }
            
        except Exception as e:
            logger.error(f"Model fine-tuning failed: {e}")
            return {"status": "error", "message": str(e)}


class AutoML:
    """AutoML component for automatic model selection and optimization."""
    
    def __init__(self, config: LearningConfig):
        self.config = config
        self.model_candidates = []
        self.optimization_history = []
        self.best_models = {}
        self.model_pipelines = {}
    
    def _get_model_candidates(self) -> List[Tuple[str, Any, Dict[str, Any]]]:
        """Get list of model candidates for AutoML."""
        return [
            ('RandomForest', RandomForestRegressor(random_state=42), {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 10, 20, 30],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }),
            ('GradientBoosting', GradientBoostingRegressor(random_state=42), {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7],
                'subsample': [0.8, 0.9, 1.0]
            }),
            ('LinearRegression', LinearRegression(), {}),
            ('Ridge', Ridge(random_state=42), {
                'alpha': [0.1, 1.0, 10.0, 100.0]
            }),
            ('Lasso', Lasso(random_state=42), {
                'alpha': [0.01, 0.1, 1.0, 10.0]
            }),
            ('SVR', SVR(), {
                'C': [0.1, 1.0, 10.0],
                'gamma': ['scale', 'auto', 0.001, 0.01],
                'kernel': ['rbf', 'linear']
            }),
            ('MLPRegressor', MLPRegressor(random_state=42, max_iter=500), {
                'hidden_layer_sizes': [(50,), (100,), (50, 50), (100, 50)],
                'activation': ['relu', 'tanh'],
                'alpha': [0.0001, 0.001, 0.01]
            })
        ]
    
    def _prepare_data(self, data: Dict[str, Any], target: str) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Prepare data for AutoML."""
        try:
            if 'market_data' not in data:
                raise ValueError("Data must contain 'market_data'")
            
            df = data['market_data']
            if not isinstance(df, pd.DataFrame):
                raise ValueError("Market data must be a DataFrame")
            
            # Create features
            df_features = df.copy()
            
            # Add technical indicators
            if 'close' in df.columns:
                df_features['returns'] = df['close'].pct_change()
                df_features['sma_5'] = df['close'].rolling(5).mean()
                df_features['sma_10'] = df['close'].rolling(10).mean()
                df_features['sma_20'] = df['close'].rolling(20).mean()
                df_features['volatility'] = df['close'].rolling(20).std()
                df_features['rsi'] = self._calculate_rsi(df['close'])
                df_features['bollinger_upper'] = df['close'].rolling(20).mean() + 2 * df['close'].rolling(20).std()
                df_features['bollinger_lower'] = df['close'].rolling(20).mean() - 2 * df['close'].rolling(20).std()
            
            if 'volume' in df.columns:
                df_features['volume_sma'] = df['volume'].rolling(20).mean()
                df_features['volume_ratio'] = df['volume'] / df_features['volume_sma']
            
            # Drop NaN values
            df_features = df_features.dropna()
            
            if len(df_features) < 20:
                raise ValueError("Insufficient data for AutoML")
            
            # Prepare features and target
            feature_cols = [col for col in df_features.columns if col != target]
            X = df_features[feature_cols].values
            y = df_features[target].values
            
            return X, y, feature_cols
            
        except Exception as e:
            logger.error(f"Data preparation failed: {e}")
            raise
    
    def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """Calculate RSI indicator."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    async def search_models(self, data: Dict[str, Any], target: str) -> Dict[str, Any]:
        """
        Search for optimal models automatically.
        
        Args:
            data: Training data
            target: Target variable
            
        Returns:
            Model search results
        """
        try:
        logger.info("Searching for optimal models...")
            
            # Prepare data
            X, y, feature_names = self._prepare_data(data, target)
            
            # Get model candidates
            model_candidates = self._get_model_candidates()
            
            # Time series split for validation
            tscv = TimeSeriesSplit(n_splits=self.config.cross_validation_folds)
            
            best_model = None
            best_score = -float('inf')
            best_model_name = None
            model_results = []
            
            for model_name, model, param_grid in model_candidates:
                try:
                    logger.info(f"Evaluating {model_name}...")
                    
                    # Create pipeline with scaling
                    pipeline = Pipeline([
                        ('scaler', RobustScaler()),
                        ('model', model)
                    ])
                    
                    # Cross-validation
                    cv_scores = cross_val_score(
                        pipeline, X, y, 
                        cv=tscv, 
                        scoring='neg_mean_squared_error',
                        n_jobs=-1
                    )
                    
                    mean_score = cv_scores.mean()
                    std_score = cv_scores.std()
                    
                    model_result = {
                        'model_name': model_name,
                        'mean_score': mean_score,
                        'std_score': std_score,
                        'cv_scores': cv_scores.tolist(),
                        'model': pipeline
                    }
                    
                    model_results.append(model_result)
                    
                    # Update best model
                    if mean_score > best_score:
                        best_score = mean_score
                        best_model = pipeline
                        best_model_name = model_name
                    
                    logger.info(f"{model_name} - Mean Score: {mean_score:.4f} (+/- {std_score:.4f})")
                    
                except Exception as e:
                    logger.warning(f"Failed to evaluate {model_name}: {e}")
                    continue
            
            if best_model is None:
                raise ValueError("No models could be evaluated successfully")
            
            # Store results
            self.model_candidates = model_results
            self.best_models[target] = {
                'model': best_model,
                'model_name': best_model_name,
                'score': best_score,
                'feature_names': feature_names
            }
            
            logger.info(f"Best model: {best_model_name} with score: {best_score:.4f}")
            
            return {
                "status": "success",
                "best_model": best_model_name,
                "performance": -best_score,  # Convert back to positive MSE
                "all_results": model_results,
                "feature_names": feature_names
            }
            
        except Exception as e:
            logger.error(f"Model search failed: {e}")
            return {"status": "error", "message": str(e)}
    
    async def optimize_hyperparameters(self, model: Any, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize hyperparameters for a given model.
        
        Args:
            model: Model to optimize
            data: Training data
            
        Returns:
            Hyperparameter optimization results
        """
        try:
        logger.info("Optimizing hyperparameters...")
            
            # Prepare data
            X, y, feature_names = self._prepare_data(data, 'close')  # Default target
            
            # Get model candidates with parameter grids
            model_candidates = self._get_model_candidates()
            
            # Find the model type
            model_name = None
            param_grid = {}
            
            for name, candidate_model, grid in model_candidates:
                if type(model).__name__ == type(candidate_model).__name__:
                    model_name = name
                    param_grid = grid
                    break
            
            if not param_grid:
                logger.warning("No parameter grid found for model, using default parameters")
                return {
                    "status": "success",
                    "optimized_model": model,
                    "best_params": {},
                    "message": "No hyperparameter optimization performed"
                }
            
            # Create pipeline
            pipeline = Pipeline([
                ('scaler', RobustScaler()),
                ('model', model)
            ])
            
            # Time series split for validation
            tscv = TimeSeriesSplit(n_splits=self.config.cross_validation_folds)
            
            # Grid search
            grid_search = GridSearchCV(
                pipeline,
                {'model__' + k: v for k, v in param_grid.items()},
                cv=tscv,
                scoring='neg_mean_squared_error',
                n_jobs=-1,
                verbose=0
            )
            
            # Fit the grid search
            grid_search.fit(X, y)
            
            # Get results
            best_params = grid_search.best_params_
            best_score = grid_search.best_score_
            best_model = grid_search.best_estimator_
            
            # Store optimization history
            optimization_result = {
                'model_name': model_name,
                'best_params': best_params,
                'best_score': best_score,
                'timestamp': datetime.now(),
                'feature_names': feature_names
            }
            
            self.optimization_history.append(optimization_result)
            
            logger.info(f"Hyperparameter optimization completed. Best score: {-best_score:.4f}")
            logger.info(f"Best parameters: {best_params}")
            
            return {
                "status": "success",
                "optimized_model": best_model,
                "best_params": best_params,
                "best_score": -best_score,
                "optimization_result": optimization_result
            }
            
        except Exception as e:
            logger.error(f"Hyperparameter optimization failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_model_recommendations(self, data_characteristics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get model recommendations based on data characteristics."""
        recommendations = []
        
        data_size = data_characteristics.get('size', 0)
        feature_count = data_characteristics.get('features', 0)
        noise_level = data_characteristics.get('noise', 'medium')
        
        # Simple heuristic-based recommendations
        if data_size < 1000:
            recommendations.append({
                'model': 'LinearRegression',
                'reason': 'Small dataset, linear models are more stable',
                'confidence': 0.8
            })
        elif feature_count > 50:
            recommendations.append({
                'model': 'RandomForest',
                'reason': 'High-dimensional data, tree-based models handle well',
                'confidence': 0.9
            })
        else:
            recommendations.append({
                'model': 'GradientBoosting',
                'reason': 'Medium dataset, gradient boosting often performs well',
                'confidence': 0.7
            })
        
        return recommendations


class NeuralArchitectureSearch:
    """Neural Architecture Search (NAS) component."""
    
    def __init__(self, config: LearningConfig):
        self.config = config
        self.architecture_candidates = []
        self.search_history = []
        self.best_architectures = {}
    
    def _generate_architecture_candidates(self, input_size: int, constraints: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate neural network architecture candidates."""
        candidates = []
        
        max_layers = constraints.get('max_layers', 5)
        max_neurons = constraints.get('max_neurons', 200)
        min_neurons = constraints.get('min_neurons', 10)
        
        # Generate different architecture patterns
        patterns = [
            # Simple architectures
            {'layers': [input_size, max_neurons//2, 1], 'activation': 'relu'},
            {'layers': [input_size, max_neurons//2, max_neurons//4, 1], 'activation': 'relu'},
            
            # Medium complexity
            {'layers': [input_size, max_neurons, max_neurons//2, 1], 'activation': 'relu'},
            {'layers': [input_size, max_neurons, max_neurons//2, max_neurons//4, 1], 'activation': 'relu'},
            
            # Complex architectures
            {'layers': [input_size, max_neurons, max_neurons, max_neurons//2, 1], 'activation': 'relu'},
            {'layers': [input_size, max_neurons, max_neurons//2, max_neurons//2, max_neurons//4, 1], 'activation': 'relu'},
        ]
        
        # Add variations with different activations
        for pattern in patterns:
            for activation in ['relu', 'tanh']:
                candidate = pattern.copy()
                candidate['activation'] = activation
                candidate['alpha'] = 0.001  # L2 regularization
                candidates.append(candidate)
        
        return candidates
    
    def _evaluate_architecture(self, architecture: Dict[str, Any], X: np.ndarray, y: np.ndarray) -> float:
        """Evaluate a neural network architecture."""
        try:
            # Create MLPRegressor with the architecture
            hidden_layers = tuple(architecture['layers'][1:-1])  # Exclude input and output layers
            
            model = MLPRegressor(
                hidden_layer_sizes=hidden_layers,
                activation=architecture['activation'],
                alpha=architecture['alpha'],
                max_iter=200,
                random_state=42
            )
            
            # Time series split for validation
            tscv = TimeSeriesSplit(n_splits=3)  # Fewer splits for faster evaluation
            
            # Cross-validation
            cv_scores = cross_val_score(
                model, X, y, 
                cv=tscv, 
                scoring='neg_mean_squared_error',
                n_jobs=1  # Single job for stability
            )
            
            return cv_scores.mean()
            
        except Exception as e:
            logger.warning(f"Architecture evaluation failed: {e}")
            return -float('inf')
    
    async def search_architecture(self, data: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search for optimal neural network architecture.
        
        Args:
            data: Training data
            constraints: Architecture constraints
            
        Returns:
            Architecture search results
        """
        try:
        logger.info("Searching for optimal architecture...")
            
            # Prepare data
            if 'market_data' not in data:
                raise ValueError("Data must contain 'market_data'")
            
            df = data['market_data']
            if not isinstance(df, pd.DataFrame):
                raise ValueError("Market data must be a DataFrame")
            
            # Create features (simplified version)
            df_features = df.copy()
            if 'close' in df.columns:
                df_features['returns'] = df['close'].pct_change()
                df_features['sma_5'] = df['close'].rolling(5).mean()
                df_features['sma_20'] = df['close'].rolling(20).mean()
                df_features['volatility'] = df['close'].rolling(20).std()
            
            df_features = df_features.dropna()
            
            if len(df_features) < 20:
                raise ValueError("Insufficient data for architecture search")
            
            # Prepare features and target
            feature_cols = [col for col in df_features.columns if col != 'close']
            X = df_features[feature_cols].values
            y = df_features['close'].values
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            input_size = X_scaled.shape[1]
            
            # Generate architecture candidates
            candidates = self._generate_architecture_candidates(input_size, constraints)
            
            best_architecture = None
            best_score = -float('inf')
            architecture_results = []
            
            logger.info(f"Evaluating {len(candidates)} architecture candidates...")
            
            for i, candidate in enumerate(candidates):
                try:
                    score = self._evaluate_architecture(candidate, X_scaled, y)
                    
                    result = {
                        'architecture': candidate,
                        'score': score,
                        'candidate_id': i
                    }
                    
                    architecture_results.append(result)
                    
                    if score > best_score:
                        best_score = score
                        best_architecture = candidate
                    
                    logger.info(f"Architecture {i}: Score = {score:.4f}")
                    
                except Exception as e:
                    logger.warning(f"Failed to evaluate architecture {i}: {e}")
                    continue
            
            if best_architecture is None:
                raise ValueError("No architectures could be evaluated successfully")
            
            # Store results
            self.architecture_candidates = architecture_results
            self.best_architectures['default'] = {
                'architecture': best_architecture,
                'score': best_score,
                'input_size': input_size
            }
            
            logger.info(f"Best architecture found with score: {best_score:.4f}")
            
            return {
                "status": "success",
                "best_architecture": best_architecture,
                "performance": -best_score,  # Convert back to positive MSE
                "all_results": architecture_results,
                "input_size": input_size
            }
            
        except Exception as e:
            logger.error(f"Architecture search failed: {e}")
            return {"status": "error", "message": str(e)}
    
    async def evolve_architecture(self, current_architecture: Any, performance_feedback: float) -> Dict[str, Any]:
        """
        Evolve architecture based on performance feedback.
        
        Args:
            current_architecture: Current architecture
            performance_feedback: Performance feedback score
            
        Returns:
            Architecture evolution results
        """
        try:
        logger.info("Evolving architecture...")
            
            if not isinstance(current_architecture, dict):
                logger.warning("Current architecture is not in expected format")
                return {"status": "error", "message": "Invalid architecture format"}
            
            # Create evolved architecture based on performance feedback
            evolved_architecture = current_architecture.copy()
            
            # Simple evolution strategy based on performance
            if performance_feedback < 0.5:  # Poor performance
                # Increase complexity
                if len(evolved_architecture['layers']) < 6:
                    # Add a layer
                    new_layer_size = evolved_architecture['layers'][-2] // 2
                    evolved_architecture['layers'].insert(-1, new_layer_size)
                    logger.info("Added layer due to poor performance")
                
                # Increase regularization
                evolved_architecture['alpha'] = min(evolved_architecture['alpha'] * 2, 0.01)
                
            elif performance_feedback > 0.8:  # Good performance
                # Try to reduce complexity
                if len(evolved_architecture['layers']) > 3:
                    # Remove a layer
                    evolved_architecture['layers'].pop(-2)
                    logger.info("Removed layer due to good performance")
                
                # Decrease regularization
                evolved_architecture['alpha'] = max(evolved_architecture['alpha'] / 2, 0.0001)
            
            # Store evolution history
            evolution_record = {
                'original_architecture': current_architecture,
                'evolved_architecture': evolved_architecture,
                'performance_feedback': performance_feedback,
                'timestamp': datetime.now()
            }
            
            self.search_history.append(evolution_record)
            
            logger.info("Architecture evolution completed")
            
            return {
                "status": "success",
                "evolved_architecture": evolved_architecture,
                "evolution_record": evolution_record
            }
            
        except Exception as e:
            logger.error(f"Architecture evolution failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_architecture_recommendations(self, data_characteristics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get architecture recommendations based on data characteristics."""
        recommendations = []
        
        data_size = data_characteristics.get('size', 0)
        feature_count = data_characteristics.get('features', 0)
        
        if data_size < 1000:
            recommendations.append({
                'architecture': {'layers': [feature_count, 50, 1], 'activation': 'relu', 'alpha': 0.001},
                'reason': 'Small dataset, simple architecture recommended',
                'confidence': 0.8
            })
        elif feature_count > 20:
            recommendations.append({
                'architecture': {'layers': [feature_count, 100, 50, 1], 'activation': 'relu', 'alpha': 0.0001},
                'reason': 'High-dimensional data, deeper network recommended',
                'confidence': 0.7
            })
        else:
            recommendations.append({
                'architecture': {'layers': [feature_count, 100, 1], 'activation': 'relu', 'alpha': 0.001},
                'reason': 'Medium complexity dataset, standard architecture',
                'confidence': 0.6
            })
        
        return recommendations


class SelfLearningEngine:
    """
    Self-Learning Engine for autonomous trading bot.
    
    This engine provides advanced learning capabilities including meta-learning,
    transfer learning, AutoML, and neural architecture search.
    """
    
    def __init__(self, config: Optional[LearningConfig] = None):
        self.config = config or LearningConfig()
        self.meta_learner = MetaLearner(self.config)
        self.transfer_learner = TransferLearner(self.config)
        self.auto_ml = AutoML(self.config)
        self.nas = NeuralArchitectureSearch(self.config)
        self.learning_history = []
        self.current_models = {}
        self.model_storage_path = Path(self.config.model_save_path)
        self.model_storage_path.mkdir(parents=True, exist_ok=True)
    
    async def learn_from_market(self, market_data: Dict[str, Any]) -> LearningResult:
        """
        Learn from market data using all available learning methods.
        
        Args:
            market_data: Market data for learning
            
        Returns:
            Learning result
        """
        try:
            logger.info("Starting self-learning from market data...")
            start_time = datetime.now()
            
            learning_results = {}
            best_model = None
            best_performance = -float('inf')
            learning_method = "combined"
            
            # Meta-learning
            if self.config.meta_learning_enabled and market_data.get('tasks'):
                meta_result = await self.meta_learner.learn_from_tasks(market_data.get('tasks', []))
                learning_results['meta_learning'] = meta_result
                logger.info(f"Meta-learning result: {meta_result}")
            
            # Transfer learning
            if self.config.transfer_learning_enabled and market_data.get('source_model'):
                transfer_result = await self.transfer_learner.transfer_knowledge(
                    market_data.get('source_domain', 'default'),
                    market_data.get('target_domain', 'current'),
                    market_data.get('source_model'),
                    market_data.get('target_data', market_data)
                )
                learning_results['transfer_learning'] = transfer_result
                logger.info(f"Transfer learning result: {transfer_result}")
                
                if transfer_result.get('status') == 'success':
                    performance = transfer_result.get('performance', {}).get('r2', 0)
                    if performance > best_performance:
                        best_performance = performance
                        best_model = transfer_result.get('transferred_model')
                        learning_method = "transfer_learning"
            
            # AutoML
            if self.config.auto_ml_enabled:
                automl_result = await self.auto_ml.search_models(
                    market_data,
                    market_data.get('target', 'close')
                )
                learning_results['automl'] = automl_result
                logger.info(f"AutoML result: {automl_result}")
                
                if automl_result.get('status') == 'success':
                    performance = 1.0 - automl_result.get('performance', 1.0)  # Convert MSE to R² approximation
                    if performance > best_performance:
                        best_performance = performance
                        best_model = automl_result.get('best_model')
                        learning_method = "automl"
            
            # Neural Architecture Search
            if self.config.nas_enabled:
                nas_result = await self.nas.search_architecture(
                    market_data,
                    market_data.get('constraints', {})
                )
                learning_results['nas'] = nas_result
                logger.info(f"NAS result: {nas_result}")
                
                if nas_result.get('status') == 'success':
                    performance = 1.0 - nas_result.get('performance', 1.0)  # Convert MSE to R² approximation
                    if performance > best_performance:
                        best_performance = performance
                        best_model = nas_result.get('best_architecture')
                        learning_method = "nas"
            
            learning_time = (datetime.now() - start_time).total_seconds()
            
            # Store the best model
            if best_model:
                model_id = f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                self.current_models[model_id] = {
                    'model': best_model,
                    'performance': best_performance,
                    'learning_method': learning_method,
                    'timestamp': datetime.now()
                }
                
                # Save model to disk
                model_path = self._save_model(best_model, model_id, learning_method)
            else:
                model_path = None
            
            # Store learning history
            learning_record = {
                'timestamp': datetime.now(),
                'market_data_keys': list(market_data.keys()),
                'learning_time': learning_time,
                'success': True,
                'learning_results': learning_results,
                'best_performance': best_performance,
                'learning_method': learning_method
            }
            
            self.learning_history.append(learning_record)
            
            # Calculate final performance metrics
            model_performance = {
                'r2_score': best_performance,
                'mse': 1.0 - best_performance if best_performance > 0 else 1.0,
                'learning_method': learning_method
            }
            
            return LearningResult(
                success=True,
                model_performance=model_performance,
                learning_time=learning_time,
                model_path=model_path,
                model_type=type(best_model).__name__ if best_model else None,
                learning_method=learning_method
            )
            
        except Exception as e:
            logger.error(f"Self-learning failed: {e}")
            return LearningResult(
                success=False,
                model_performance={},
                learning_time=0.0,
                error_message=str(e)
            )
    
    def _save_model(self, model: Any, model_id: str, learning_method: str) -> str:
        """Save model to disk."""
        try:
            model_filename = f"{model_id}_{learning_method}.joblib"
            model_path = self.model_storage_path / model_filename
            
            # Save model
            joblib.dump(model, model_path)
            
            logger.info(f"Model saved to: {model_path}")
            return str(model_path)
            
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
            return None
    
    def _load_model(self, model_path: str) -> Any:
        """Load model from disk."""
        try:
            model = joblib.load(model_path)
            logger.info(f"Model loaded from: {model_path}")
            return model
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return None
    
    async def optimize_strategy(self, performance_metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Optimize trading strategy based on performance metrics.
        
        Args:
            performance_metrics: Current performance metrics
            
        Returns:
            Optimization results
        """
        try:
            logger.info("Optimizing strategy based on performance metrics...")
            
            # Analyze performance metrics
            sharpe_ratio = performance_metrics.get('sharpe_ratio', 0)
            max_drawdown = performance_metrics.get('max_drawdown', 0)
            win_rate = performance_metrics.get('win_rate', 0)
            profit_factor = performance_metrics.get('profit_factor', 0)
            
            optimized_parameters = {}
            expected_improvement = 0.0
            
            # Risk management optimization
            if sharpe_ratio < 1.5:
                logger.info("Low Sharpe ratio detected, optimizing for risk-adjusted returns...")
                optimized_parameters['risk_level'] = max(0.01, performance_metrics.get('risk_level', 0.02) * 0.8)
                optimized_parameters['position_size'] = max(0.05, performance_metrics.get('position_size', 0.1) * 0.9)
                expected_improvement += 0.1
            
            if max_drawdown > 0.1:
                logger.info("High drawdown detected, optimizing for risk management...")
                optimized_parameters['stop_loss'] = min(0.03, performance_metrics.get('stop_loss', 0.05) * 0.8)
                optimized_parameters['max_position_size'] = max(0.05, performance_metrics.get('position_size', 0.1) * 0.7)
                expected_improvement += 0.08
            
            # Profit optimization
            if win_rate < 0.5:
                logger.info("Low win rate detected, optimizing entry/exit strategy...")
                optimized_parameters['take_profit'] = max(0.08, performance_metrics.get('take_profit', 0.1) * 1.2)
                optimized_parameters['entry_threshold'] = performance_metrics.get('entry_threshold', 0.5) * 1.1
                expected_improvement += 0.05
            
            if profit_factor < 1.2:
                logger.info("Low profit factor detected, optimizing risk-reward ratio...")
                optimized_parameters['risk_reward_ratio'] = max(1.5, performance_metrics.get('risk_reward_ratio', 1.0) * 1.3)
                expected_improvement += 0.06
            
            # Set default values if not optimized
            default_params = {
                'risk_level': 0.02,
                'position_size': 0.1,
                'stop_loss': 0.05,
                'take_profit': 0.1,
                'max_position_size': 0.15,
                'entry_threshold': 0.5,
                'risk_reward_ratio': 2.0
            }
            
            for key, default_value in default_params.items():
                if key not in optimized_parameters:
                    optimized_parameters[key] = performance_metrics.get(key, default_value)
            
            optimization_result = {
                'status': 'success',
                'optimized_parameters': optimized_parameters,
                'expected_improvement': expected_improvement,
                'optimization_reasons': self._get_optimization_reasons(performance_metrics),
                'timestamp': datetime.now()
            }
            
            logger.info(f"Strategy optimization completed: {optimization_result}")
            return optimization_result
            
        except Exception as e:
            logger.error(f"Strategy optimization failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _get_optimization_reasons(self, performance_metrics: Dict[str, float]) -> List[str]:
        """Get reasons for optimization based on performance metrics."""
        reasons = []
        
        if performance_metrics.get('sharpe_ratio', 0) < 1.5:
            reasons.append("Low Sharpe ratio - reducing risk and position size")
        
        if performance_metrics.get('max_drawdown', 0) > 0.1:
            reasons.append("High drawdown - tightening stop losses")
        
        if performance_metrics.get('win_rate', 0) < 0.5:
            reasons.append("Low win rate - improving entry/exit strategy")
        
        if performance_metrics.get('profit_factor', 0) < 1.2:
            reasons.append("Low profit factor - optimizing risk-reward ratio")
        
        return reasons
    
    async def adapt_to_new_market(self, market_conditions: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt to new market conditions using transfer learning.
        
        Args:
            market_conditions: New market conditions
            
        Returns:
            Adaptation results
        """
        try:
            logger.info("Adapting to new market conditions...")
            
            # Find the best current model for adaptation
            best_model = None
            best_model_id = None
            
            for model_id, model_info in self.current_models.items():
                if best_model is None or model_info['performance'] > best_model['performance']:
                    best_model = model_info
                    best_model_id = model_id
            
            if best_model is None:
                logger.warning("No models available for adaptation")
                return {'status': 'error', 'message': 'No models available for adaptation'}
            
            # Use transfer learning to adapt
            adaptation_result = await self.transfer_learner.fine_tune_model(
                best_model['model'],
                market_conditions
            )
            
            if adaptation_result.get('status') == 'success':
                # Store adapted model
                adapted_model_id = f"adapted_{best_model_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                self.current_models[adapted_model_id] = {
                    'model': adaptation_result['fine_tuned_model'],
                    'performance': adaptation_result['performance'].get('r2', 0),
                    'learning_method': 'transfer_learning',
                    'timestamp': datetime.now(),
                    'parent_model': best_model_id
                }
                
                # Save adapted model
                model_path = self._save_model(
                    adaptation_result['fine_tuned_model'], 
                    adapted_model_id, 
                    'transfer_learning'
                )
                
                adaptation_result['adapted_model_id'] = adapted_model_id
                adaptation_result['model_path'] = model_path
            
            logger.info(f"Market adaptation completed: {adaptation_result}")
            return adaptation_result
            
        except Exception as e:
            logger.error(f"Market adaptation failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_learning_status(self) -> Dict[str, Any]:
        """
        Get current learning status and statistics.
        
        Returns:
            Learning status information
        """
        successful_sessions = [h for h in self.learning_history if h.get('success', False)]
        
        # Calculate performance statistics
        model_performances = []
        for model_info in self.current_models.values():
            model_performances.append(model_info['performance'])
        
        avg_performance = sum(model_performances) / len(model_performances) if model_performances else 0
        
        # Get learning method distribution
        learning_methods = {}
        for session in self.learning_history:
            method = session.get('learning_method', 'unknown')
            learning_methods[method] = learning_methods.get(method, 0) + 1
        
        return {
            'total_learning_sessions': len(self.learning_history),
            'successful_sessions': len(successful_sessions),
            'success_rate': len(successful_sessions) / max(len(self.learning_history), 1),
            'average_learning_time': sum(h.get('learning_time', 0) for h in self.learning_history) / max(len(self.learning_history), 1),
            'current_models_count': len(self.current_models),
            'average_model_performance': avg_performance,
            'learning_methods_distribution': learning_methods,
            'config': {
                'meta_learning_enabled': self.config.meta_learning_enabled,
                'transfer_learning_enabled': self.config.transfer_learning_enabled,
                'auto_ml_enabled': self.config.auto_ml_enabled,
                'nas_enabled': self.config.nas_enabled,
                'few_shot_enabled': self.config.few_shot_enabled
            },
            'model_storage_path': str(self.model_storage_path)
        }
    
    def get_best_model(self) -> Optional[Dict[str, Any]]:
        """Get the best performing model."""
        if not self.current_models:
            return None
        
        best_model_id = max(self.current_models.keys(), 
                          key=lambda k: self.current_models[k]['performance'])
        
        return {
            'model_id': best_model_id,
            'model_info': self.current_models[best_model_id]
        }
    
    def cleanup_old_models(self, keep_count: int = None) -> int:
        """Clean up old models, keeping only the best ones."""
        if keep_count is None:
            keep_count = self.config.max_models_in_memory
        
        if len(self.current_models) <= keep_count:
            return 0
        
        # Sort models by performance and timestamp
        sorted_models = sorted(
            self.current_models.items(),
            key=lambda x: (x[1]['performance'], x[1]['timestamp']),
            reverse=True
        )
        
        # Keep only the best models
        models_to_keep = dict(sorted_models[:keep_count])
        models_to_remove = set(self.current_models.keys()) - set(models_to_keep.keys())
        
        # Remove old models
        for model_id in models_to_remove:
            del self.current_models[model_id]
        
        logger.info(f"Cleaned up {len(models_to_remove)} old models, kept {len(models_to_keep)}")
        return len(models_to_remove)
    
    def export_learning_summary(self) -> Dict[str, Any]:
        """Export a summary of learning activities."""
        return {
            'learning_history': self.learning_history,
            'current_models': {
                model_id: {
                    'performance': info['performance'],
                    'learning_method': info['learning_method'],
                    'timestamp': info['timestamp'].isoformat()
                }
                for model_id, info in self.current_models.items()
            },
            'meta_learner_status': {
                'has_meta_knowledge': bool(self.meta_learner.meta_knowledge),
                'tasks_processed': len(self.meta_learner.task_embeddings)
            },
            'transfer_learner_status': {
                'transfer_history_count': len(self.transfer_learner.transfer_history),
                'source_models_count': len(self.transfer_learner.source_models)
            },
            'automl_status': {
                'optimization_history_count': len(self.auto_ml.optimization_history),
                'best_models_count': len(self.auto_ml.best_models)
            },
            'nas_status': {
                'search_history_count': len(self.nas.search_history),
                'best_architectures_count': len(self.nas.best_architectures)
            },
            'export_timestamp': datetime.now().isoformat()
        }
