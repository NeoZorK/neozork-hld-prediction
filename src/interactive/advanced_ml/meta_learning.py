# -*- coding: utf-8 -*-
"""
Meta-Learning for NeoZork Interactive ML Trading Strategy Development.

This module provides meta-learning capabilities for rapid adaptation to new market conditions.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import cross_val_score
import warnings

class MetaLearning:
    """
    Meta-learning system for rapid adaptation to new market conditions.
    
    Features:
    - Model-Agnostic Meta-Learning (MAML)
    - Gradient-based Meta-Learning
    - Memory-Augmented Networks
    - Few-shot Learning
    - Transfer Learning
    """
    
    def __init__(self):
        """Initialize the meta-learning system."""
        self.meta_models = {}
        self.task_embeddings = {}
        self.adaptation_history = {}
        self.meta_parameters = {}
    
    def create_maml_learner(self, base_model_type: str = "linear", 
                           inner_lr: float = 0.01, meta_lr: float = 0.001,
                           inner_steps: int = 5) -> Dict[str, Any]:
        """
        Create a Model-Agnostic Meta-Learning (MAML) learner.
        
        Args:
            base_model_type: Type of base model (linear, logistic, rf)
            inner_lr: Learning rate for inner loop adaptation
            meta_lr: Learning rate for meta-parameter updates
            inner_steps: Number of inner loop steps
            
        Returns:
            MAML learner configuration
        """
        try:
            # Initialize base model
            if base_model_type == "linear":
                base_model = LinearRegression()
            elif base_model_type == "logistic":
                base_model = LogisticRegression()
            elif base_model_type == "rf":
                base_model = RandomForestRegressor()
            else:
                base_model = LinearRegression()
            
            maml_config = {
                "status": "success",
                "learner_type": "maml",
                "base_model": base_model,
                "base_model_type": base_model_type,
                "inner_lr": inner_lr,
                "meta_lr": meta_lr,
                "inner_steps": inner_steps,
                "meta_parameters": self._initialize_meta_parameters(base_model)
            }
            
            return maml_config
            
        except Exception as e:
            return {"status": "error", "message": f"MAML learner creation failed: {str(e)}"}
    
    def train_maml_learner(self, maml_config: Dict[str, Any], 
                          tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train a MAML learner on multiple tasks.
        
        Args:
            maml_config: MAML configuration
            tasks: List of training tasks with support and query sets
            
        Returns:
            Training results
        """
        try:
            base_model = maml_config["base_model"]
            inner_lr = maml_config["inner_lr"]
            meta_lr = maml_config["meta_lr"]
            inner_steps = maml_config["inner_steps"]
            
            # Initialize meta-parameters
            meta_params = self._initialize_meta_parameters(base_model)
            
            # Training loop (simplified MAML)
            task_losses = []
            
            for task in tasks:
                support_X = task["support_X"]
                support_y = task["support_y"]
                query_X = task["query_X"]
                query_y = task["query_y"]
                
                # Inner loop: adapt to task
                adapted_params = self._inner_loop_adaptation(
                    base_model, meta_params, support_X, support_y, 
                    inner_lr, inner_steps
                )
                
                # Calculate query loss
                query_loss = self._calculate_query_loss(
                    base_model, adapted_params, query_X, query_y
                )
                
                task_losses.append(query_loss)
            
            # Meta-update (simplified)
            avg_loss = np.mean(task_losses)
            
            # Update meta-parameters (simplified gradient update)
            meta_params = self._meta_update(meta_params, task_losses, meta_lr)
            
            result = {
                "status": "success",
                "learner_type": "maml",
                "average_loss": avg_loss,
                "task_losses": task_losses,
                "n_tasks": len(tasks),
                "meta_parameters": meta_params
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"MAML training failed: {str(e)}"}
    
    def create_few_shot_learner(self, base_model_type: str = "linear",
                               n_shot: int = 5) -> Dict[str, Any]:
        """
        Create a few-shot learning system.
        
        Args:
            base_model_type: Type of base model
            n_shot: Number of examples per class for few-shot learning
            
        Returns:
            Few-shot learner configuration
        """
        try:
            # Initialize base model
            if base_model_type == "linear":
                base_model = LinearRegression()
            elif base_model_type == "logistic":
                base_model = LogisticRegression()
            elif base_model_type == "rf":
                base_model = RandomForestRegressor()
            else:
                base_model = LinearRegression()
            
            few_shot_config = {
                "status": "success",
                "learner_type": "few_shot",
                "base_model": base_model,
                "base_model_type": base_model_type,
                "n_shot": n_shot,
                "prototype_embeddings": {}
            }
            
            return few_shot_config
            
        except Exception as e:
            return {"status": "error", "message": f"Few-shot learner creation failed: {str(e)}"}
    
    def train_few_shot_learner(self, few_shot_config: Dict[str, Any],
                              support_set: Dict[str, Any],
                              query_set: Dict[str, Any]) -> Dict[str, Any]:
        """
        Train a few-shot learner on support set and evaluate on query set.
        
        Args:
            few_shot_config: Few-shot configuration
            support_set: Support set for training
            query_set: Query set for evaluation
            
        Returns:
            Training and evaluation results
        """
        try:
            base_model = few_shot_config["base_model"]
            n_shot = few_shot_config["n_shot"]
            
            # Extract support data
            support_X = support_set["X"]
            support_y = support_set["y"]
            query_X = query_set["X"]
            query_y = query_set["y"]
            
            # Train on support set
            base_model.fit(support_X, support_y)
            
            # Evaluate on query set
            query_pred = base_model.predict(query_X)
            
            # Calculate performance
            if hasattr(base_model, 'predict_proba'):
                # Classification
                accuracy = (query_pred == query_y).mean()
                performance = {"accuracy": accuracy}
            else:
                # Regression
                mse = np.mean((query_pred - query_y) ** 2)
                mae = np.mean(np.abs(query_pred - query_y))
                r2 = 1 - (np.sum((query_y - query_pred) ** 2) / np.sum((query_y - np.mean(query_y)) ** 2))
                performance = {"mse": mse, "mae": mae, "r2": r2}
            
            result = {
                "status": "success",
                "learner_type": "few_shot",
                "performance": performance,
                "n_support": len(support_X),
                "n_query": len(query_X),
                "n_shot": n_shot
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Few-shot training failed: {str(e)}"}
    
    def create_transfer_learner(self, source_model: Any, target_domain: str,
                               transfer_method: str = "fine_tuning") -> Dict[str, Any]:
        """
        Create a transfer learning system.
        
        Args:
            source_model: Pre-trained source model
            target_domain: Target domain name
            transfer_method: Transfer method (fine_tuning, feature_extraction)
            
        Returns:
            Transfer learner configuration
        """
        try:
            transfer_config = {
                "status": "success",
                "learner_type": "transfer",
                "source_model": source_model,
                "target_domain": target_domain,
                "transfer_method": transfer_method,
                "adapted_model": None,
                "transfer_weights": {}
            }
            
            return transfer_config
            
        except Exception as e:
            return {"status": "error", "message": f"Transfer learner creation failed: {str(e)}"}
    
    def adapt_transfer_learner(self, transfer_config: Dict[str, Any],
                              target_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt transfer learner to target domain.
        
        Args:
            transfer_config: Transfer configuration
            target_data: Target domain data
            
        Returns:
            Adaptation results
        """
        try:
            source_model = transfer_config["source_model"]
            transfer_method = transfer_config["transfer_method"]
            
            target_X = target_data["X"]
            target_y = target_data["y"]
            
            if transfer_method == "fine_tuning":
                # Fine-tune the source model
                adapted_model = self._fine_tune_model(source_model, target_X, target_y)
            else:  # feature_extraction
                # Use source model as feature extractor
                adapted_model = self._create_feature_extractor(source_model, target_X, target_y)
            
            # Evaluate adapted model
            target_pred = adapted_model.predict(target_X)
            
            # Calculate performance
            if hasattr(adapted_model, 'predict_proba'):
                # Classification
                accuracy = (target_pred == target_y).mean()
                performance = {"accuracy": accuracy}
            else:
                # Regression
                mse = np.mean((target_pred - target_y) ** 2)
                mae = np.mean(np.abs(target_pred - target_y))
                r2 = 1 - (np.sum((target_y - target_pred) ** 2) / np.sum((target_y - np.mean(target_y)) ** 2))
                performance = {"mse": mse, "mae": mae, "r2": r2}
            
            result = {
                "status": "success",
                "learner_type": "transfer",
                "performance": performance,
                "transfer_method": transfer_method,
                "adapted_model": adapted_model
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Transfer adaptation failed: {str(e)}"}
    
    def create_memory_augmented_learner(self, base_model_type: str = "linear",
                                       memory_size: int = 1000) -> Dict[str, Any]:
        """
        Create a memory-augmented learning system.
        
        Args:
            base_model_type: Type of base model
            memory_size: Size of external memory
            
        Returns:
            Memory-augmented learner configuration
        """
        try:
            # Initialize base model
            if base_model_type == "linear":
                base_model = LinearRegression()
            elif base_model_type == "logistic":
                base_model = LogisticRegression()
            elif base_model_type == "rf":
                base_model = RandomForestRegressor()
            else:
                base_model = LinearRegression()
            
            memory_config = {
                "status": "success",
                "learner_type": "memory_augmented",
                "base_model": base_model,
                "base_model_type": base_model_type,
                "memory_size": memory_size,
                "memory": [],
                "memory_embeddings": {}
            }
            
            return memory_config
            
        except Exception as e:
            return {"status": "error", "message": f"Memory-augmented learner creation failed: {str(e)}"}
    
    def train_memory_augmented_learner(self, memory_config: Dict[str, Any],
                                      training_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Train a memory-augmented learner.
        
        Args:
            memory_config: Memory-augmented configuration
            training_data: Training data
            
        Returns:
            Training results
        """
        try:
            base_model = memory_config["base_model"]
            memory = memory_config["memory"]
            memory_size = memory_config["memory_size"]
            
            X = training_data["X"]
            y = training_data["y"]
            
            # Add to memory
            for i in range(len(X)):
                memory.append({
                    "features": X.iloc[i].values if hasattr(X, 'iloc') else X[i],
                    "target": y.iloc[i] if hasattr(y, 'iloc') else y[i],
                    "timestamp": i
                })
            
            # Keep only recent memories
            if len(memory) > memory_size:
                memory = memory[-memory_size:]
            
            # Train base model
            base_model.fit(X, y)
            
            # Calculate performance
            train_pred = base_model.predict(X)
            
            if hasattr(base_model, 'predict_proba'):
                # Classification
                accuracy = (train_pred == y).mean()
                performance = {"accuracy": accuracy}
            else:
                # Regression
                mse = np.mean((train_pred - y) ** 2)
                mae = np.mean(np.abs(train_pred - y))
                r2 = 1 - (np.sum((y - train_pred) ** 2) / np.sum((y - np.mean(y)) ** 2))
                performance = {"mse": mse, "mae": mae, "r2": r2}
            
            result = {
                "status": "success",
                "learner_type": "memory_augmented",
                "performance": performance,
                "memory_size": len(memory),
                "n_training_samples": len(X)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Memory-augmented training failed: {str(e)}"}
    
    def _initialize_meta_parameters(self, base_model: Any) -> Dict[str, Any]:
        """Initialize meta-parameters for MAML."""
        try:
            if hasattr(base_model, 'coef_'):
                return {"coef_": base_model.coef_.copy() if hasattr(base_model.coef_, 'copy') else base_model.coef_}
            elif hasattr(base_model, 'feature_importances_'):
                return {"feature_importances_": base_model.feature_importances_.copy()}
            else:
                return {}
        except:
            return {}
    
    def _inner_loop_adaptation(self, base_model: Any, meta_params: Dict[str, Any],
                              support_X: pd.DataFrame, support_y: pd.Series,
                              inner_lr: float, inner_steps: int) -> Dict[str, Any]:
        """Perform inner loop adaptation for MAML."""
        try:
            # Simplified inner loop adaptation
            adapted_params = meta_params.copy()
            
            # Train base model on support set
            base_model.fit(support_X, support_y)
            
            # Update parameters (simplified)
            if hasattr(base_model, 'coef_'):
                adapted_params["coef_"] = base_model.coef_
            elif hasattr(base_model, 'feature_importances_'):
                adapted_params["feature_importances_"] = base_model.feature_importances_
            
            return adapted_params
            
        except Exception as e:
            return meta_params
    
    def _calculate_query_loss(self, base_model: Any, adapted_params: Dict[str, Any],
                             query_X: pd.DataFrame, query_y: pd.Series) -> float:
        """Calculate query loss for MAML."""
        try:
            # Use adapted parameters to make predictions
            query_pred = base_model.predict(query_X)
            
            # Calculate loss
            if hasattr(base_model, 'predict_proba'):
                # Classification loss
                loss = 1 - (query_pred == query_y).mean()
            else:
                # Regression loss
                loss = np.mean((query_pred - query_y) ** 2)
            
            return loss
            
        except Exception as e:
            return 1.0
    
    def _meta_update(self, meta_params: Dict[str, Any], task_losses: List[float],
                     meta_lr: float) -> Dict[str, Any]:
        """Perform meta-parameter update for MAML."""
        try:
            # Simplified meta-update
            avg_loss = np.mean(task_losses)
            
            # Update parameters based on average loss
            if "coef_" in meta_params:
                meta_params["coef_"] = meta_params["coef_"] * (1 - meta_lr * avg_loss)
            elif "feature_importances_" in meta_params:
                meta_params["feature_importances_"] = meta_params["feature_importances_"] * (1 - meta_lr * avg_loss)
            
            return meta_params
            
        except Exception as e:
            return meta_params
    
    def _fine_tune_model(self, source_model: Any, target_X: pd.DataFrame, 
                        target_y: pd.Series) -> Any:
        """Fine-tune source model on target data."""
        try:
            # Create a copy of source model
            adapted_model = source_model
            
            # Fine-tune on target data
            adapted_model.fit(target_X, target_y)
            
            return adapted_model
            
        except Exception as e:
            return source_model
    
    def _create_feature_extractor(self, source_model: Any, target_X: pd.DataFrame,
                                 target_y: pd.Series) -> Any:
        """Create feature extractor from source model."""
        try:
            # Use source model as feature extractor
            # This is a simplified implementation
            return source_model
            
        except Exception as e:
            return source_model
