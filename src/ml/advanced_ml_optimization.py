# -*- coding: utf-8 -*-
"""
Advanced ML Model Optimization System for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive ML model optimization, hyperparameter tuning, and performance enhancement.
"""

import numpy as np
import pandas as pd
import logging
from typing import Dict, Any, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import joblib
import warnings
warnings.filterwarnings('ignore')

# ML imports
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, TimeSeriesSplit, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.decomposition import PCA, FastICA
from sklearn.manifold import TSNE

# Advanced ML imports (conditional) - moved to function level to avoid import errors
OPTUNA_AVAILABLE = False
XGBOOST_AVAILABLE = False
LIGHTGBM_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptimizationMethod(Enum):
    """Optimization methods."""
    GRID_SEARCH = "grid_search"
    RANDOM_SEARCH = "random_search"
    BAYESIAN_OPTIMIZATION = "bayesian_optimization"
    GENETIC_ALGORITHM = "genetic_algorithm"
    PARTICLE_SWARM = "particle_swarm"
    OPTUNA = "optuna"

class ModelType(Enum):
    """Model types."""
    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    XGBOOST = "xgboost"
    LIGHTGBM = "lightgbm"
    NEURAL_NETWORK = "neural_network"
    RIDGE = "ridge"
    LASSO = "lasso"
    ELASTIC_NET = "elastic_net"
    ADABOOST = "adaboost"

class FeatureSelectionMethod(Enum):
    """Feature selection methods."""
    SELECT_K_BEST = "select_k_best"
    MUTUAL_INFO = "mutual_info"
    PCA = "pca"
    ICA = "ica"
    TSNE = "tsne"
    CORRELATION = "correlation"
    VARIANCE_THRESHOLD = "variance_threshold"

class OptimizationObjective(Enum):
    """Optimization objectives."""
    MINIMIZE_MSE = "minimize_mse"
    MINIMIZE_MAE = "minimize_mae"
    MAXIMIZE_R2 = "maximize_r2"
    MAXIMIZE_SHARPE = "maximize_sharpe"
    MINIMIZE_DRAWDOWN = "minimize_drawdown"
    MAXIMIZE_CALMAR = "maximize_calmar"
    CUSTOM = "custom"

@dataclass
class OptimizationConfig:
    """Optimization configuration."""
    method: OptimizationMethod
    model_type: ModelType
    objective: OptimizationObjective
    cv_folds: int = 5
    n_trials: int = 100
    timeout: int = 3600  # 1 hour
    n_jobs: int = -1
    random_state: int = 42
    early_stopping: bool = True
    feature_selection: bool = True
    feature_selection_method: FeatureSelectionMethod = FeatureSelectionMethod.SELECT_K_BEST
    n_features: int = 50

@dataclass
class OptimizationResult:
    """Optimization result."""
    best_model: Any
    best_params: Dict[str, Any]
    best_score: float
    optimization_time: float
    n_trials: int
    cv_scores: List[float]
    feature_importance: Dict[str, float] = field(default_factory=dict)
    optimization_history: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class ModelPerformance:
    """Model performance metrics."""
    model_name: str
    mse: float
    rmse: float
    mae: float
    r2: float
    sharpe_ratio: float
    max_drawdown: float
    calmar_ratio: float
    training_time: float
    prediction_time: float
    feature_count: int

class AdvancedMLOptimizer:
    """Advanced ML model optimization system."""
    
    def __init__(self):
        self.models = {}
        self.optimization_results = {}
        self.performance_history = []
        self.feature_importance = {}
        
    def optimize_model(self, X: pd.DataFrame, y: pd.Series, 
                      config: OptimizationConfig) -> OptimizationResult:
        """Optimize ML model with specified configuration."""
        try:
            logger.info(f"Starting optimization for {config.model_type.value} using {config.method.value}")
            
            start_time = datetime.now()
            
            # Feature selection if enabled
            if config.feature_selection:
                X_selected, feature_names = self._select_features(
                    X, y, config.feature_selection_method, config.n_features
                )
            else:
                X_selected = X
                feature_names = X.columns.tolist()
            
            # Create model
            model = self._create_model(config.model_type)
            
            # Define parameter grid
            param_grid = self._get_parameter_grid(config.model_type)
            
            # Perform optimization
            if config.method == OptimizationMethod.GRID_SEARCH:
                result = self._grid_search_optimization(
                    model, X_selected, y, param_grid, config
                )
            elif config.method == OptimizationMethod.RANDOM_SEARCH:
                result = self._random_search_optimization(
                    model, X_selected, y, param_grid, config
                )
            elif config.method == OptimizationMethod.OPTUNA and OPTUNA_AVAILABLE:
                result = self._optuna_optimization(
                    model, X_selected, y, param_grid, config
                )
            else:
                result = self._grid_search_optimization(
                    model, X_selected, y, param_grid, config
                )
            
            # Calculate optimization time
            optimization_time = (datetime.now() - start_time).total_seconds()
            result.optimization_time = optimization_time
            
            # Store result
            self.optimization_results[f"{config.model_type.value}_{config.method.value}"] = result
            
            logger.info(f"Optimization completed in {optimization_time:.2f} seconds")
            logger.info(f"Best score: {result.best_score:.4f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to optimize model: {e}")
            return OptimizationResult(
                best_model=None,
                best_params={},
                best_score=0.0,
                optimization_time=0.0,
                n_trials=0,
                cv_scores=[]
            )
    
    def _create_model(self, model_type: ModelType):
        """Create model instance."""
        if model_type == ModelType.RANDOM_FOREST:
            return RandomForestRegressor(random_state=42, n_jobs=-1)
        elif model_type == ModelType.GRADIENT_BOOSTING:
            return GradientBoostingRegressor(random_state=42)
        elif model_type == ModelType.XGBOOST:
            try:
                import xgboost as xgb
                return xgb.XGBRegressor(random_state=42, n_jobs=-1)
            except Exception as e:
                logger.warning(f"XGBoost not available, falling back to RandomForest: {e}")
                return RandomForestRegressor(random_state=42, n_jobs=-1)
        elif model_type == ModelType.LIGHTGBM:
            try:
                import lightgbm as lgb
                return lgb.LGBMRegressor(random_state=42, n_jobs=-1, verbose=-1)
            except Exception as e:
                logger.warning(f"LightGBM not available, falling back to RandomForest: {e}")
                return RandomForestRegressor(random_state=42, n_jobs=-1)
        elif model_type == ModelType.NEURAL_NETWORK:
            return MLPRegressor(random_state=42, max_iter=1000)
        elif model_type == ModelType.RIDGE:
            return Ridge(random_state=42)
        elif model_type == ModelType.LASSO:
            return Lasso(random_state=42, max_iter=1000)
        elif model_type == ModelType.ELASTIC_NET:
            return ElasticNet(random_state=42, max_iter=1000)
        elif model_type == ModelType.ADABOOST:
            return AdaBoostRegressor(random_state=42)
        else:
            return RandomForestRegressor(random_state=42, n_jobs=-1)
    
    def _get_parameter_grid(self, model_type: ModelType) -> Dict[str, List]:
        """Get parameter grid for model type."""
        if model_type == ModelType.RANDOM_FOREST:
            return {
                'n_estimators': [50, 100, 200, 300],
                'max_depth': [None, 10, 20, 30],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'max_features': ['sqrt', 'log2', None]
            }
        elif model_type == ModelType.GRADIENT_BOOSTING:
            return {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
        elif model_type == ModelType.XGBOOST and XGBOOST_AVAILABLE:
            return {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7],
                'subsample': [0.8, 0.9, 1.0],
                'colsample_bytree': [0.8, 0.9, 1.0]
            }
        elif model_type == ModelType.LIGHTGBM and LIGHTGBM_AVAILABLE:
            return {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7],
                'subsample': [0.8, 0.9, 1.0],
                'colsample_bytree': [0.8, 0.9, 1.0]
            }
        elif model_type == ModelType.NEURAL_NETWORK:
            return {
                'hidden_layer_sizes': [(50,), (100,), (50, 50), (100, 50)],
                'activation': ['relu', 'tanh'],
                'alpha': [0.0001, 0.001, 0.01],
                'learning_rate': ['constant', 'adaptive']
            }
        elif model_type == ModelType.RIDGE:
            return {
                'alpha': [0.1, 1.0, 10.0, 100.0, 1000.0]
            }
        elif model_type == ModelType.LASSO:
            return {
                'alpha': [0.1, 1.0, 10.0, 100.0, 1000.0]
            }
        elif model_type == ModelType.ELASTIC_NET:
            return {
                'alpha': [0.1, 1.0, 10.0, 100.0],
                'l1_ratio': [0.1, 0.3, 0.5, 0.7, 0.9]
            }
        elif model_type == ModelType.ADABOOST:
            return {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.2, 0.5]
            }
        else:
            return {'n_estimators': [100]}
    
    def _select_features(self, X: pd.DataFrame, y: pd.Series, 
                        method: FeatureSelectionMethod, n_features: int) -> Tuple[pd.DataFrame, List[str]]:
        """Select features using specified method."""
        try:
            if method == FeatureSelectionMethod.SELECT_K_BEST:
                selector = SelectKBest(score_func=f_regression, k=n_features)
                X_selected = selector.fit_transform(X, y)
                feature_names = X.columns[selector.get_support()].tolist()
                return pd.DataFrame(X_selected, columns=feature_names, index=X.index), feature_names
            
            elif method == FeatureSelectionMethod.MUTUAL_INFO:
                selector = SelectKBest(score_func=mutual_info_regression, k=n_features)
                X_selected = selector.fit_transform(X, y)
                feature_names = X.columns[selector.get_support()].tolist()
                return pd.DataFrame(X_selected, columns=feature_names, index=X.index), feature_names
            
            elif method == FeatureSelectionMethod.PCA:
                pca = PCA(n_components=n_features)
                X_selected = pca.fit_transform(X)
                feature_names = [f'PC_{i+1}' for i in range(n_features)]
                return pd.DataFrame(X_selected, columns=feature_names, index=X.index), feature_names
            
            elif method == FeatureSelectionMethod.ICA:
                ica = FastICA(n_components=n_features, random_state=42)
                X_selected = ica.fit_transform(X)
                feature_names = [f'IC_{i+1}' for i in range(n_features)]
                return pd.DataFrame(X_selected, columns=feature_names, index=X.index), feature_names
            
            elif method == FeatureSelectionMethod.CORRELATION:
                # Select features with highest correlation to target
                correlations = X.corrwith(y).abs().sort_values(ascending=False)
                selected_features = correlations.head(n_features).index.tolist()
                return X[selected_features], selected_features
            
            else:
                # Default to SelectKBest
                selector = SelectKBest(score_func=f_regression, k=n_features)
                X_selected = selector.fit_transform(X, y)
                feature_names = X.columns[selector.get_support()].tolist()
                return pd.DataFrame(X_selected, columns=feature_names, index=X.index), feature_names
                
        except Exception as e:
            logger.error(f"Failed to select features: {e}")
            return X, X.columns.tolist()
    
    def _grid_search_optimization(self, model, X: pd.DataFrame, y: pd.Series, 
                                 param_grid: Dict[str, List], config: OptimizationConfig) -> OptimizationResult:
        """Perform grid search optimization."""
        try:
            cv = TimeSeriesSplit(n_splits=config.cv_folds)
            
            grid_search = GridSearchCV(
                estimator=model,
                param_grid=param_grid,
                cv=cv,
                scoring='neg_mean_squared_error',
                n_jobs=config.n_jobs,
                verbose=0
            )
            
            grid_search.fit(X, y)
            
            # Get feature importance if available
            feature_importance = {}
            if hasattr(grid_search.best_estimator_, 'feature_importances_'):
                feature_names = X.columns.tolist()
                importance_values = grid_search.best_estimator_.feature_importances_
                feature_importance = dict(zip(feature_names, importance_values))
            
            return OptimizationResult(
                best_model=grid_search.best_estimator_,
                best_params=grid_search.best_params_,
                best_score=abs(grid_search.best_score_),
                optimization_time=0.0,  # Will be set by caller
                n_trials=len(grid_search.cv_results_['params']),
                cv_scores=grid_search.cv_results_['mean_test_score'].tolist(),
                feature_importance=feature_importance
            )
            
        except Exception as e:
            logger.error(f"Grid search optimization failed: {e}")
            return OptimizationResult(
                best_model=None,
                best_params={},
                best_score=0.0,
                optimization_time=0.0,
                n_trials=0,
                cv_scores=[]
            )
    
    def _random_search_optimization(self, model, X: pd.DataFrame, y: pd.Series, 
                                   param_grid: Dict[str, List], config: OptimizationConfig) -> OptimizationResult:
        """Perform random search optimization."""
        try:
            cv = TimeSeriesSplit(n_splits=config.cv_folds)
            
            random_search = RandomizedSearchCV(
                estimator=model,
                param_distributions=param_grid,
                n_iter=config.n_trials,
                cv=cv,
                scoring='neg_mean_squared_error',
                n_jobs=config.n_jobs,
                random_state=config.random_state,
                verbose=0
            )
            
            random_search.fit(X, y)
            
            # Get feature importance if available
            feature_importance = {}
            if hasattr(random_search.best_estimator_, 'feature_importances_'):
                feature_names = X.columns.tolist()
                importance_values = random_search.best_estimator_.feature_importances_
                feature_importance = dict(zip(feature_names, importance_values))
            
            return OptimizationResult(
                best_model=random_search.best_estimator_,
                best_params=random_search.best_params_,
                best_score=abs(random_search.best_score_),
                optimization_time=0.0,  # Will be set by caller
                n_trials=len(random_search.cv_results_['params']),
                cv_scores=random_search.cv_results_['mean_test_score'].tolist(),
                feature_importance=feature_importance
            )
            
        except Exception as e:
            logger.error(f"Random search optimization failed: {e}")
            return OptimizationResult(
                best_model=None,
                best_params={},
                best_score=0.0,
                optimization_time=0.0,
                n_trials=0,
                cv_scores=[]
            )
    
    def _optuna_optimization(self, model, X: pd.DataFrame, y: pd.Series, 
                            param_grid: Dict[str, List], config: OptimizationConfig) -> OptimizationResult:
        """Perform Optuna optimization."""
        try:
            try:
                import optuna
            except ImportError:
                logger.warning("Optuna not available, falling back to random search")
                return self._random_search_optimization(model, X, y, param_grid, config)
            
            def objective(trial):
                # Create model with suggested parameters
                if isinstance(model, RandomForestRegressor):
                    params = {
                        'n_estimators': trial.suggest_int('n_estimators', 50, 300),
                        'max_depth': trial.suggest_int('max_depth', 5, 30),
                        'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
                        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
                        'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None])
                    }
                elif isinstance(model, GradientBoostingRegressor):
                    params = {
                        'n_estimators': trial.suggest_int('n_estimators', 50, 200),
                        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
                        'max_depth': trial.suggest_int('max_depth', 3, 10),
                        'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
                        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10)
                    }
                else:
                    params = {}
                
                # Create model with parameters
                model_instance = self._create_model_from_params(type(model), params)
                
                # Cross-validation
                cv = TimeSeriesSplit(n_splits=config.cv_folds)
                scores = cross_val_score(model_instance, X, y, cv=cv, scoring='neg_mean_squared_error')
                
                return scores.mean()
            
            study = optuna.create_study(direction='maximize')
            study.optimize(objective, n_trials=config.n_trials, timeout=config.timeout)
            
            # Get best parameters and create model
            best_params = study.best_params
            best_model = self._create_model_from_params(type(model), best_params)
            best_model.fit(X, y)
            
            # Get feature importance if available
            feature_importance = {}
            if hasattr(best_model, 'feature_importances_'):
                feature_names = X.columns.tolist()
                importance_values = best_model.feature_importances_
                feature_importance = dict(zip(feature_names, importance_values))
            
            return OptimizationResult(
                best_model=best_model,
                best_params=best_params,
                best_score=abs(study.best_value),
                optimization_time=0.0,  # Will be set by caller
                n_trials=len(study.trials),
                cv_scores=[trial.value for trial in study.trials if trial.value is not None],
                feature_importance=feature_importance,
                optimization_history=[{'trial': i, 'value': trial.value, 'params': trial.params} 
                                    for i, trial in enumerate(study.trials) if trial.value is not None]
            )
            
        except Exception as e:
            logger.error(f"Optuna optimization failed: {e}")
            return self._random_search_optimization(model, X, y, param_grid, config)
    
    def _create_model_from_params(self, model_class, params: Dict[str, Any]):
        """Create model instance with parameters."""
        try:
            return model_class(**params)
        except Exception as e:
            logger.error(f"Failed to create model with parameters: {e}")
            return model_class()
    
    def evaluate_model_performance(self, model, X_test: pd.DataFrame, y_test: pd.Series, 
                                  model_name: str = "Model") -> ModelPerformance:
        """Evaluate model performance on test data."""
        try:
            start_time = datetime.now()
            
            # Make predictions
            y_pred = model.predict(X_test)
            prediction_time = (datetime.now() - start_time).total_seconds()
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Calculate trading-specific metrics
            returns = y_test.pct_change().dropna()
            predicted_returns = pd.Series(y_pred).pct_change().dropna()
            
            # Sharpe ratio
            if len(returns) > 0 and returns.std() > 0:
                sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252)
            else:
                sharpe_ratio = 0.0
            
            # Max drawdown
            if len(returns) > 0:
                cumulative = (1 + returns).cumprod()
                running_max = cumulative.expanding().max()
                drawdown = (cumulative - running_max) / running_max
                max_drawdown = drawdown.min()
            else:
                max_drawdown = 0.0
            
            # Calmar ratio
            if max_drawdown != 0:
                calmar_ratio = abs(returns.mean() * 252) / abs(max_drawdown)
            else:
                calmar_ratio = 0.0
            
            performance = ModelPerformance(
                model_name=model_name,
                mse=mse,
                rmse=rmse,
                mae=mae,
                r2=r2,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                calmar_ratio=calmar_ratio,
                training_time=0.0,  # Not available in this context
                prediction_time=prediction_time,
                feature_count=len(X_test.columns)
            )
            
            # Store performance
            self.performance_history.append(performance)
            
            return performance
            
        except Exception as e:
            logger.error(f"Failed to evaluate model performance: {e}")
            return ModelPerformance(
                model_name=model_name,
                mse=float('inf'),
                rmse=float('inf'),
                mae=float('inf'),
                r2=0.0,
                sharpe_ratio=0.0,
                max_drawdown=0.0,
                calmar_ratio=0.0,
                training_time=0.0,
                prediction_time=0.0,
                feature_count=0
            )
    
    def compare_models(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, Any]:
        """Compare performance of all optimized models."""
        try:
            if not self.optimization_results:
                return {
                    'status': 'error',
                    'message': 'No optimization results available'
                }
            
            comparison_results = {}
            
            for result_name, result in self.optimization_results.items():
                if result.best_model is not None:
                    performance = self.evaluate_model_performance(
                        result.best_model, X_test, y_test, result_name
                    )
                    comparison_results[result_name] = {
                        'performance': performance,
                        'best_params': result.best_params,
                        'best_score': result.best_score,
                        'optimization_time': result.optimization_time,
                        'n_trials': result.n_trials
                    }
            
            # Find best model
            best_model_name = None
            best_r2 = -float('inf')
            
            for name, data in comparison_results.items():
                if data['performance'].r2 > best_r2:
                    best_r2 = data['performance'].r2
                    best_model_name = name
            
            return {
                'status': 'success',
                'comparison_results': comparison_results,
                'best_model': best_model_name,
                'best_r2': best_r2,
                'total_models': len(comparison_results),
                'message': f'Compared {len(comparison_results)} models'
            }
            
        except Exception as e:
            logger.error(f"Failed to compare models: {e}")
            return {
                'status': 'error',
                'message': f'Failed to compare models: {str(e)}'
            }
    
    def get_optimization_summary(self) -> Dict[str, Any]:
        """Get summary of all optimization results."""
        try:
            summary = {
                'total_optimizations': len(self.optimization_results),
                'total_performance_evaluations': len(self.performance_history),
                'optimization_results': {},
                'performance_ranking': []
            }
            
            # Add optimization results
            for name, result in self.optimization_results.items():
                summary['optimization_results'][name] = {
                    'best_score': result.best_score,
                    'optimization_time': result.optimization_time,
                    'n_trials': result.n_trials,
                    'best_params': result.best_params,
                    'feature_importance_count': len(result.feature_importance)
                }
            
            # Rank performance
            if self.performance_history:
                sorted_performance = sorted(
                    self.performance_history, 
                    key=lambda x: x.r2, 
                    reverse=True
                )
                summary['performance_ranking'] = [
                    {
                        'model_name': p.model_name,
                        'r2': p.r2,
                        'rmse': p.rmse,
                        'sharpe_ratio': p.sharpe_ratio,
                        'calmar_ratio': p.calmar_ratio
                    }
                    for p in sorted_performance
                ]
            
            return {
                'status': 'success',
                'summary': summary,
                'message': 'Optimization summary generated successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to get optimization summary: {e}")
            return {
                'status': 'error',
                'message': f'Failed to get optimization summary: {str(e)}'
            }
    
    def save_best_model(self, model_name: str, filepath: str) -> Dict[str, Any]:
        """Save the best model to file."""
        try:
            if model_name not in self.optimization_results:
                return {
                    'status': 'error',
                    'message': f'Model {model_name} not found in optimization results'
                }
            
            result = self.optimization_results[model_name]
            if result.best_model is None:
                return {
                    'status': 'error',
                    'message': f'No trained model available for {model_name}'
                }
            
            joblib.dump(result.best_model, filepath)
            
            return {
                'status': 'success',
                'model_name': model_name,
                'filepath': filepath,
                'message': f'Model {model_name} saved to {filepath}'
            }
            
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
            return {
                'status': 'error',
                'message': f'Failed to save model: {str(e)}'
            }

# Example usage and testing
def test_advanced_ml_optimization():
    """Test advanced ML optimization system."""
    print("🧪 Testing Advanced ML Optimization System...")
    
    # Create optimizer
    optimizer = AdvancedMLOptimizer()
    
    # Generate sample data
    np.random.seed(42)
    n_samples = 1000
    n_features = 50
    
    X = pd.DataFrame(
        np.random.randn(n_samples, n_features),
        columns=[f'feature_{i}' for i in range(n_features)]
    )
    
    # Create target with some relationship to features
    y = (X.iloc[:, :5].sum(axis=1) + 
         X.iloc[:, 5:10].sum(axis=1) * 0.5 + 
         np.random.randn(n_samples) * 0.1)
    
    # Split data
    split_idx = int(0.8 * n_samples)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    print(f"  • Sample data created: {n_samples} samples, {n_features} features")
    print(f"  • Train/Test split: {len(X_train)}/{len(X_test)}")
    
    # Test different model types and optimization methods
    model_types = [
        ModelType.RANDOM_FOREST,
        ModelType.GRADIENT_BOOSTING,
        ModelType.RIDGE,
        ModelType.NEURAL_NETWORK
    ]
    
    optimization_methods = [
        OptimizationMethod.GRID_SEARCH,
        OptimizationMethod.RANDOM_SEARCH
    ]
    
    print("  • Testing model optimization...")
    
    for model_type in model_types:
        for method in optimization_methods:
            config = OptimizationConfig(
                method=method,
                model_type=model_type,
                objective=OptimizationObjective.MINIMIZE_MSE,
                cv_folds=3,
                n_trials=20,
                feature_selection=True,
                n_features=20
            )
            
            result = optimizer.optimize_model(X_train, y_train, config)
            
            if result.best_model is not None:
                print(f"    ✅ {model_type.value} + {method.value}: Score {result.best_score:.4f}")
                print(f"        - Optimization time: {result.optimization_time:.2f}s")
                print(f"        - Trials: {result.n_trials}")
                print(f"        - Best params: {list(result.best_params.keys())}")
            else:
                print(f"    ❌ {model_type.value} + {method.value}: Failed")
    
    # Compare models
    comparison = optimizer.compare_models(X_test, y_test)
    if comparison['status'] == 'success':
        print(f"  • Model comparison: ✅ {comparison['total_models']} models compared")
        print(f"    - Best model: {comparison['best_model']}")
        print(f"    - Best R²: {comparison['best_r2']:.4f}")
    
    # Get optimization summary
    summary = optimizer.get_optimization_summary()
    if summary['status'] == 'success':
        print(f"  • Optimization summary: ✅")
        print(f"    - Total optimizations: {summary['summary']['total_optimizations']}")
        print(f"    - Performance evaluations: {summary['summary']['total_performance_evaluations']}")
        
        if summary['summary']['performance_ranking']:
            best_performance = summary['summary']['performance_ranking'][0]
            print(f"    - Best performing model: {best_performance['model_name']}")
            print(f"      R²: {best_performance['r2']:.4f}, RMSE: {best_performance['rmse']:.4f}")
    
    print("✅ Advanced ML Optimization System test completed!")
    
    return optimizer

if __name__ == "__main__":
    test_advanced_ml_optimization()
