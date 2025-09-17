"""
Machine Learning Optimization System
Hyperparameter tuning, model selection, performance optimization
"""

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import uuid
import json
from abc import ABC, abstractmethod
import itertools
from scipy.optimize import minimize
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptimizationMethod(Enum):
    """Optimization method enumeration"""
    GRID_SEARCH = "grid_search"
    RANDOM_SEARCH = "random_search"
    BAYESIAN_OPTIMIZATION = "bayesian_optimization"
    GENETIC_ALGORITHM = "genetic_algorithm"
    GRADIENT_BASED = "gradient_based"
    EVOLUTIONARY = "evolutionary"

class OptimizationObjective(Enum):
    """Optimization objective enumeration"""
    MINIMIZE_LOSS = "minimize_loss"
    MAXIMIZE_ACCURACY = "maximize_accuracy"
    MAXIMIZE_F1_SCORE = "maximize_f1_score"
    MAXIMIZE_PRECISION = "maximize_precision"
    MAXIMIZE_RECALL = "maximize_recall"
    MINIMIZE_MAE = "minimize_mae"
    MINIMIZE_MSE = "minimize_mse"
    MAXIMIZE_R2 = "maximize_r2"
    CUSTOM = "custom"

@dataclass
class HyperparameterSpace:
    """Hyperparameter search space definition"""
    name: str
    param_type: str  # 'int', 'float', 'categorical', 'boolean'
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    step: Optional[float] = None
    choices: Optional[List[Any]] = None
    default_value: Any = None

@dataclass
class OptimizationConfig:
    """Optimization configuration"""
    config_id: str
    method: OptimizationMethod
    objective: OptimizationObjective
    hyperparameter_space: Dict[str, HyperparameterSpace]
    max_iterations: int
    cv_folds: int
    scoring_metric: str
    early_stopping: bool
    early_stopping_patience: int
    random_state: int
    n_jobs: int
    created_at: datetime

@dataclass
class OptimizationResult:
    """Optimization result"""
    result_id: str
    config_id: str
    best_params: Dict[str, Any]
    best_score: float
    optimization_history: List[Dict[str, Any]]
    total_iterations: int
    total_time: float
    cv_scores: List[float]
    start_time: datetime
    end_time: datetime
    status: str

class BaseOptimizer(ABC):
    """Base class for optimizers"""
    
    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.optimization_history = []
        self.best_score = float('-inf') if config.objective in [OptimizationObjective.MAXIMIZE_ACCURACY, OptimizationObjective.MAXIMIZE_F1_SCORE] else float('inf')
        self.best_params = None
        
    @abstractmethod
    async def optimize(self, model_func: Callable, X: np.ndarray, y: np.ndarray) -> OptimizationResult:
        """Perform optimization"""
        pass
    
    def _evaluate_params(self, params: Dict[str, Any], model_func: Callable, X: np.ndarray, y: np.ndarray) -> float:
        """Evaluate parameters using cross-validation"""
        try:
            # Create model with parameters
            model = model_func(**params)
            
            # Perform cross-validation
            cv_scores = cross_val_score(model, X, y, cv=self.config.cv_folds, scoring=self.config.scoring_metric)
            
            # Return mean score
            return np.mean(cv_scores)
            
        except Exception as e:
            logger.error(f"Error evaluating parameters {params}: {e}")
            return float('-inf') if self.config.objective in [OptimizationObjective.MAXIMIZE_ACCURACY, OptimizationObjective.MAXIMIZE_F1_SCORE] else float('inf')

class GridSearchOptimizer(BaseOptimizer):
    """Grid search optimizer"""
    
    async def optimize(self, model_func: Callable, X: np.ndarray, y: np.ndarray) -> OptimizationResult:
        """Perform grid search optimization"""
        result_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        logger.info(f"Starting grid search optimization with {self.config.max_iterations} iterations")
        
        # Generate parameter grid
        param_grid = self._generate_param_grid()
        
        # Limit iterations if grid is too large
        total_combinations = len(list(itertools.product(*param_grid.values())))
        if total_combinations > self.config.max_iterations:
            logger.warning(f"Grid has {total_combinations} combinations, limiting to {self.config.max_iterations}")
        
        iteration = 0
        for param_combination in itertools.product(*param_grid.values()):
            if iteration >= self.config.max_iterations:
                break
                
            # Create parameter dictionary
            params = dict(zip(param_grid.keys(), param_combination))
            
            # Evaluate parameters
            score = self._evaluate_params(params, model_func, X, y)
            
            # Update best if better
            if self._is_better_score(score):
                self.best_score = score
                self.best_params = params.copy()
            
            # Record history
            self.optimization_history.append({
                "iteration": iteration,
                "params": params.copy(),
                "score": score,
                "timestamp": datetime.now()
            })
            
            iteration += 1
            
            if iteration % 10 == 0:
                logger.info(f"Grid search iteration {iteration}: Best score = {self.best_score:.4f}")
        
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()
        
        # Calculate CV scores for best parameters
        cv_scores = []
        if self.best_params:
            model = model_func(**self.best_params)
            cv_scores = cross_val_score(model, X, y, cv=self.config.cv_folds, scoring=self.config.scoring_metric).tolist()
        
        result = OptimizationResult(
            result_id=result_id,
            config_id=self.config.config_id,
            best_params=self.best_params or {},
            best_score=self.best_score,
            optimization_history=self.optimization_history,
            total_iterations=iteration,
            total_time=total_time,
            cv_scores=cv_scores,
            start_time=start_time,
            end_time=end_time,
            status="completed"
        )
        
        logger.info(f"Grid search completed: Best score = {self.best_score:.4f} in {total_time:.2f} seconds")
        return result
    
    def _generate_param_grid(self) -> Dict[str, List[Any]]:
        """Generate parameter grid from hyperparameter space"""
        param_grid = {}
        
        for param_name, param_space in self.config.hyperparameter_space.items():
            if param_space.param_type == 'int':
                param_grid[param_name] = list(range(
                    int(param_space.min_value),
                    int(param_space.max_value) + 1,
                    int(param_space.step or 1)
                ))
            elif param_space.param_type == 'float':
                param_grid[param_name] = np.arange(
                    param_space.min_value,
                    param_space.max_value + param_space.step,
                    param_space.step
                ).tolist()
            elif param_space.param_type == 'categorical':
                param_grid[param_name] = param_space.choices
            elif param_space.param_type == 'boolean':
                param_grid[param_name] = [True, False]
        
        return param_grid
    
    def _is_better_score(self, score: float) -> bool:
        """Check if score is better than current best"""
        if self.config.objective in [OptimizationObjective.MAXIMIZE_ACCURACY, OptimizationObjective.MAXIMIZE_F1_SCORE, OptimizationObjective.MAXIMIZE_R2]:
            return score > self.best_score
        else:
            return score < self.best_score

class RandomSearchOptimizer(BaseOptimizer):
    """Random search optimizer"""
    
    async def optimize(self, model_func: Callable, X: np.ndarray, y: np.ndarray) -> OptimizationResult:
        """Perform random search optimization"""
        result_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        logger.info(f"Starting random search optimization with {self.config.max_iterations} iterations")
        
        np.random.seed(self.config.random_state)
        
        for iteration in range(self.config.max_iterations):
            # Generate random parameters
            params = self._generate_random_params()
            
            # Evaluate parameters
            score = self._evaluate_params(params, model_func, X, y)
            
            # Update best if better
            if self._is_better_score(score):
                self.best_score = score
                self.best_params = params.copy()
            
            # Record history
            self.optimization_history.append({
                "iteration": iteration,
                "params": params.copy(),
                "score": score,
                "timestamp": datetime.now()
            })
            
            if iteration % 10 == 0:
                logger.info(f"Random search iteration {iteration}: Best score = {self.best_score:.4f}")
        
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()
        
        # Calculate CV scores for best parameters
        cv_scores = []
        if self.best_params:
            model = model_func(**self.best_params)
            cv_scores = cross_val_score(model, X, y, cv=self.config.cv_folds, scoring=self.config.scoring_metric).tolist()
        
        result = OptimizationResult(
            result_id=result_id,
            config_id=self.config.config_id,
            best_params=self.best_params or {},
            best_score=self.best_score,
            optimization_history=self.optimization_history,
            total_iterations=self.config.max_iterations,
            total_time=total_time,
            cv_scores=cv_scores,
            start_time=start_time,
            end_time=end_time,
            status="completed"
        )
        
        logger.info(f"Random search completed: Best score = {self.best_score:.4f} in {total_time:.2f} seconds")
        return result
    
    def _generate_random_params(self) -> Dict[str, Any]:
        """Generate random parameters from hyperparameter space"""
        params = {}
        
        for param_name, param_space in self.config.hyperparameter_space.items():
            if param_space.param_type == 'int':
                params[param_name] = np.random.randint(
                    int(param_space.min_value),
                    int(param_space.max_value) + 1
                )
            elif param_space.param_type == 'float':
                params[param_name] = np.random.uniform(
                    param_space.min_value,
                    param_space.max_value
                )
            elif param_space.param_type == 'categorical':
                params[param_name] = np.random.choice(param_space.choices)
            elif param_space.param_type == 'boolean':
                params[param_name] = np.random.choice([True, False])
        
        return params
    
    def _is_better_score(self, score: float) -> bool:
        """Check if score is better than current best"""
        if self.config.objective in [OptimizationObjective.MAXIMIZE_ACCURACY, OptimizationObjective.MAXIMIZE_F1_SCORE, OptimizationObjective.MAXIMIZE_R2]:
            return score > self.best_score
        else:
            return score < self.best_score

class BayesianOptimizer(BaseOptimizer):
    """Bayesian optimization"""
    
    def __init__(self, config: OptimizationConfig):
        super().__init__(config)
        self.acquisition_history = []
        self.gp_model = None
        
    async def optimize(self, model_func: Callable, X: np.ndarray, y: np.ndarray) -> OptimizationResult:
        """Perform Bayesian optimization"""
        result_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        logger.info(f"Starting Bayesian optimization with {self.config.max_iterations} iterations")
        
        # Initialize with random samples
        n_init = min(10, self.config.max_iterations // 2)
        
        for iteration in range(self.config.max_iterations):
            if iteration < n_init:
                # Random exploration phase
                params = self._generate_random_params()
            else:
                # Bayesian optimization phase
                params = self._acquisition_function()
            
            # Evaluate parameters
            score = self._evaluate_params(params, model_func, X, y)
            
            # Update best if better
            if self._is_better_score(score):
                self.best_score = score
                self.best_params = params.copy()
            
            # Record history
            self.optimization_history.append({
                "iteration": iteration,
                "params": params.copy(),
                "score": score,
                "timestamp": datetime.now()
            })
            
            # Update Gaussian Process model (simplified)
            self._update_gp_model(params, score)
            
            if iteration % 10 == 0:
                logger.info(f"Bayesian optimization iteration {iteration}: Best score = {self.best_score:.4f}")
        
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()
        
        # Calculate CV scores for best parameters
        cv_scores = []
        if self.best_params:
            model = model_func(**self.best_params)
            cv_scores = cross_val_score(model, X, y, cv=self.config.cv_folds, scoring=self.config.scoring_metric).tolist()
        
        result = OptimizationResult(
            result_id=result_id,
            config_id=self.config.config_id,
            best_params=self.best_params or {},
            best_score=self.best_score,
            optimization_history=self.optimization_history,
            total_iterations=self.config.max_iterations,
            total_time=total_time,
            cv_scores=cv_scores,
            start_time=start_time,
            end_time=end_time,
            status="completed"
        )
        
        logger.info(f"Bayesian optimization completed: Best score = {self.best_score:.4f} in {total_time:.2f} seconds")
        return result
    
    def _acquisition_function(self) -> Dict[str, Any]:
        """Acquisition function for Bayesian optimization"""
        # Simplified acquisition function (Expected Improvement)
        # In practice, this would use a proper Gaussian Process
        
        # For now, use random search with bias towards promising regions
        params = self._generate_random_params()
        
        # Add some bias based on previous good results
        if len(self.optimization_history) > 0:
            good_results = [h for h in self.optimization_history if h['score'] > np.mean([h['score'] for h in self.optimization_history])]
            if good_results:
                # Sample from good results with some noise
                best_result = max(good_results, key=lambda x: x['score'])
                for param_name in params:
                    if param_name in best_result['params']:
                        # Add noise to good parameters
                        if isinstance(best_result['params'][param_name], (int, float)):
                            noise = np.random.normal(0, 0.1)
                            params[param_name] = best_result['params'][param_name] + noise
        
        return params
    
    def _update_gp_model(self, params: Dict[str, Any], score: float) -> None:
        """Update Gaussian Process model"""
        # Simplified GP update
        # In practice, this would maintain a proper GP model
        pass
    
    def _generate_random_params(self) -> Dict[str, Any]:
        """Generate random parameters from hyperparameter space"""
        params = {}
        
        for param_name, param_space in self.config.hyperparameter_space.items():
            if param_space.param_type == 'int':
                params[param_name] = np.random.randint(
                    int(param_space.min_value),
                    int(param_space.max_value) + 1
                )
            elif param_space.param_type == 'float':
                params[param_name] = np.random.uniform(
                    param_space.min_value,
                    param_space.max_value
                )
            elif param_space.param_type == 'categorical':
                params[param_name] = np.random.choice(param_space.choices)
            elif param_space.param_type == 'boolean':
                params[param_name] = np.random.choice([True, False])
        
        return params
    
    def _is_better_score(self, score: float) -> bool:
        """Check if score is better than current best"""
        if self.config.objective in [OptimizationObjective.MAXIMIZE_ACCURACY, OptimizationObjective.MAXIMIZE_F1_SCORE, OptimizationObjective.MAXIMIZE_R2]:
            return score > self.best_score
        else:
            return score < self.best_score

class ModelSelectionManager:
    """Model selection and comparison manager"""
    
    def __init__(self):
        self.model_configs = {}
        self.selection_results = {}
        self.performance_history = {}
        
    async def add_model_config(self, name: str, model_func: Callable, 
                              hyperparameter_space: Dict[str, HyperparameterSpace]) -> str:
        """Add model configuration for selection"""
        config_id = str(uuid.uuid4())
        
        self.model_configs[config_id] = {
            "name": name,
            "model_func": model_func,
            "hyperparameter_space": hyperparameter_space,
            "created_at": datetime.now()
        }
        
        logger.info(f"Added model configuration: {name}")
        return config_id
    
    async def select_best_model(self, X: np.ndarray, y: np.ndarray, 
                               optimization_config: OptimizationConfig) -> Dict[str, Any]:
        """Select best model using optimization"""
        selection_id = str(uuid.uuid4())
        
        logger.info(f"Starting model selection with {len(self.model_configs)} models")
        
        best_overall_score = float('-inf') if optimization_config.objective in [OptimizationObjective.MAXIMIZE_ACCURACY, OptimizationObjective.MAXIMIZE_F1_SCORE] else float('inf')
        best_model_config = None
        best_optimization_result = None
        
        model_results = {}
        
        for config_id, config in self.model_configs.items():
            logger.info(f"Optimizing model: {config['name']}")
            
            # Create optimizer
            if optimization_config.method == OptimizationMethod.GRID_SEARCH:
                optimizer = GridSearchOptimizer(optimization_config)
            elif optimization_config.method == OptimizationMethod.RANDOM_SEARCH:
                optimizer = RandomSearchOptimizer(optimization_config)
            elif optimization_config.method == OptimizationMethod.BAYESIAN_OPTIMIZATION:
                optimizer = BayesianOptimizer(optimization_config)
            else:
                logger.warning(f"Unsupported optimization method: {optimization_config.method}")
                continue
            
            # Optimize model
            result = await optimizer.optimize(config['model_func'], X, y)
            
            model_results[config_id] = {
                "name": config['name'],
                "best_score": result.best_score,
                "best_params": result.best_params,
                "optimization_result": result
            }
            
            # Update best overall
            if optimization_config.objective in [OptimizationObjective.MAXIMIZE_ACCURACY, OptimizationObjective.MAXIMIZE_F1_SCORE, OptimizationObjective.MAXIMIZE_R2]:
                if result.best_score > best_overall_score:
                    best_overall_score = result.best_score
                    best_model_config = config_id
                    best_optimization_result = result
            else:
                if result.best_score < best_overall_score:
                    best_overall_score = result.best_score
                    best_model_config = config_id
                    best_optimization_result = result
        
        selection_result = {
            "selection_id": selection_id,
            "best_model_config": best_model_config,
            "best_model_name": self.model_configs[best_model_config]['name'] if best_model_config else None,
            "best_score": best_overall_score,
            "best_params": best_optimization_result.best_params if best_optimization_result else {},
            "model_results": model_results,
            "optimization_config": asdict(optimization_config),
            "selection_time": datetime.now()
        }
        
        self.selection_results[selection_id] = selection_result
        
        logger.info(f"Model selection completed: Best model = {selection_result['best_model_name']} with score = {best_overall_score:.4f}")
        
        return selection_result
    
    async def compare_models(self, X: np.ndarray, y: np.ndarray, 
                           test_size: float = 0.2) -> Dict[str, Any]:
        """Compare all models with default parameters"""
        comparison_id = str(uuid.uuid4())
        
        logger.info(f"Comparing {len(self.model_configs)} models")
        
        # Split data
        split_idx = int(len(X) * (1 - test_size))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        comparison_results = {}
        
        for config_id, config in self.model_configs.items():
            try:
                # Create model with default parameters
                default_params = {}
                for param_name, param_space in config['hyperparameter_space'].items():
                    if param_space.default_value is not None:
                        default_params[param_name] = param_space.default_value
                
                model = config['model_func'](**default_params)
                
                # Train model
                model.fit(X_train, y_train)
                
                # Make predictions
                y_pred = model.predict(X_test)
                
                # Calculate metrics
                metrics = {
                    "accuracy": accuracy_score(y_test, y_pred),
                    "precision": precision_score(y_test, y_pred, average='weighted'),
                    "recall": recall_score(y_test, y_pred, average='weighted'),
                    "f1_score": f1_score(y_test, y_pred, average='weighted')
                }
                
                comparison_results[config_id] = {
                    "name": config['name'],
                    "metrics": metrics,
                    "default_params": default_params
                }
                
            except Exception as e:
                logger.error(f"Error comparing model {config['name']}: {e}")
                comparison_results[config_id] = {
                    "name": config['name'],
                    "error": str(e)
                }
        
        comparison = {
            "comparison_id": comparison_id,
            "comparison_results": comparison_results,
            "test_size": test_size,
            "comparison_time": datetime.now()
        }
        
        logger.info(f"Model comparison completed")
        return comparison

class MLOptimizationManager:
    """Main ML optimization manager"""
    
    def __init__(self):
        self.optimization_configs = {}
        self.optimization_results = {}
        self.model_selection_manager = ModelSelectionManager()
        self.performance_tracker = {}
        
    async def create_optimization_config(self, method: OptimizationMethod, 
                                       objective: OptimizationObjective,
                                       hyperparameter_space: Dict[str, HyperparameterSpace],
                                       max_iterations: int = 100,
                                       cv_folds: int = 5,
                                       scoring_metric: str = 'accuracy') -> str:
        """Create optimization configuration"""
        config_id = str(uuid.uuid4())
        
        config = OptimizationConfig(
            config_id=config_id,
            method=method,
            objective=objective,
            hyperparameter_space=hyperparameter_space,
            max_iterations=max_iterations,
            cv_folds=cv_folds,
            scoring_metric=scoring_metric,
            early_stopping=True,
            early_stopping_patience=10,
            random_state=42,
            n_jobs=1,
            created_at=datetime.now()
        )
        
        self.optimization_configs[config_id] = config
        
        logger.info(f"Created optimization config: {method.value} for {objective.value}")
        return config_id
    
    async def optimize_model(self, config_id: str, model_func: Callable, 
                           X: np.ndarray, y: np.ndarray) -> OptimizationResult:
        """Optimize a model with given configuration"""
        if config_id not in self.optimization_configs:
            raise ValueError(f"Optimization config {config_id} not found")
        
        config = self.optimization_configs[config_id]
        
        # Create optimizer
        if config.method == OptimizationMethod.GRID_SEARCH:
            optimizer = GridSearchOptimizer(config)
        elif config.method == OptimizationMethod.RANDOM_SEARCH:
            optimizer = RandomSearchOptimizer(config)
        elif config.method == OptimizationMethod.BAYESIAN_OPTIMIZATION:
            optimizer = BayesianOptimizer(config)
        else:
            raise ValueError(f"Unsupported optimization method: {config.method}")
        
        # Perform optimization
        result = await optimizer.optimize(model_func, X, y)
        
        # Store result
        self.optimization_results[result.result_id] = result
        
        logger.info(f"Optimization completed: Best score = {result.best_score:.4f}")
        return result
    
    async def get_optimization_summary(self) -> Dict[str, Any]:
        """Get optimization summary"""
        total_configs = len(self.optimization_configs)
        total_results = len(self.optimization_results)
        
        # Calculate average performance
        if self.optimization_results:
            avg_score = np.mean([result.best_score for result in self.optimization_results.values()])
            best_score = max([result.best_score for result in self.optimization_results.values()])
        else:
            avg_score = 0.0
            best_score = 0.0
        
        return {
            "total_configs": total_configs,
            "total_results": total_results,
            "average_score": avg_score,
            "best_score": best_score,
            "optimization_methods": list(set(config.method.value for config in self.optimization_configs.values())),
            "last_update": datetime.now()
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get system summary"""
        return {
            "optimization_configs": len(self.optimization_configs),
            "optimization_results": len(self.optimization_results),
            "model_configs": len(self.model_selection_manager.model_configs),
            "selection_results": len(self.model_selection_manager.selection_results),
            "last_update": datetime.now()
        }

# Example usage and testing
async def main():
    """Example usage of MLOptimizationManager"""
    manager = MLOptimizationManager()
    
    # Create hyperparameter spaces
    hyperparameter_space = {
        "n_estimators": HyperparameterSpace("n_estimators", "int", 10, 200, 10, default_value=100),
        "max_depth": HyperparameterSpace("max_depth", "int", 3, 20, 1, default_value=10),
        "learning_rate": HyperparameterSpace("learning_rate", "float", 0.01, 0.3, 0.01, default_value=0.1),
        "subsample": HyperparameterSpace("subsample", "float", 0.5, 1.0, 0.1, default_value=0.8)
    }
    
    # Create optimization config
    config_id = await manager.create_optimization_config(
        method=OptimizationMethod.RANDOM_SEARCH,
        objective=OptimizationObjective.MAXIMIZE_ACCURACY,
        hyperparameter_space=hyperparameter_space,
        max_iterations=50,
        cv_folds=3
    )
    
    # Mock model function
    def mock_model_func(**params):
        class MockModel:
            def __init__(self, **kwargs):
                self.params = kwargs
            
            def fit(self, X, y):
                pass
            
            def predict(self, X):
                return np.random.randint(0, 2, len(X))
            
            def score(self, X, y):
                return np.random.uniform(0.7, 0.95)
        
        return MockModel(**params)
    
    # Generate sample data
    X = np.random.randn(1000, 10)
    y = np.random.randint(0, 2, 1000)
    
    # Optimize model
    result = await manager.optimize_model(config_id, mock_model_func, X, y)
    
    print(f"Optimization completed:")
    print(f"  Best score: {result.best_score:.4f}")
    print(f"  Best params: {result.best_params}")
    print(f"  Total time: {result.total_time:.2f} seconds")
    print(f"  Total iterations: {result.total_iterations}")
    
    # Get summary
    summary = manager.get_summary()
    print(f"System summary: {summary}")

if __name__ == "__main__":
    asyncio.run(main())
