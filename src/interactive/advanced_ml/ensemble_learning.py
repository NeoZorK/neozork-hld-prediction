# -*- coding: utf-8 -*-
"""
Ensemble Learning for NeoZork Interactive ML Trading Strategy Development.

This module provides ensemble learning capabilities for robust model predictions.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.model_selection import cross_val_score
import warnings

class EnsembleLearning:
    """
    Ensemble learning system for combining multiple models.
    
    Features:
    - Stacking with meta-learning
    - Blending with dynamic weights
    - Bayesian Model Averaging
    - Dynamic Ensemble Selection
    - Model diversity analysis
    """
    
    def __init__(self):
        """Initialize the ensemble learning system."""
        self.base_models = {}
        self.meta_models = {}
        self.ensemble_weights = {}
        self.performance_history = {}
    
    def create_stacking_ensemble(self, base_models: List[Dict[str, Any]], 
                                meta_model_type: str = "logistic") -> Dict[str, Any]:
        """
        Create a stacking ensemble with meta-learning.
        
        Args:
            base_models: List of base model configurations
            meta_model_type: Type of meta-model (logistic, linear, rf)
            
        Returns:
            Stacking ensemble configuration
        """
        try:
            # Initialize base models
            initialized_models = {}
            for i, model_config in enumerate(base_models):
                model_name = f"base_model_{i}"
                model_type = model_config.get("type", "random_forest")
                params = model_config.get("parameters", {})
                
                if model_type == "random_forest":
                    if model_config.get("task") == "classification":
                        model = RandomForestClassifier(**params)
                    else:
                        model = RandomForestRegressor(**params)
                elif model_type == "logistic_regression":
                    model = LogisticRegression(**params)
                elif model_type == "linear_regression":
                    model = LinearRegression(**params)
                elif model_type == "svm":
                    if model_config.get("task") == "classification":
                        model = SVC(**params)
                    else:
                        model = SVR(**params)
                else:
                    continue
                
                initialized_models[model_name] = {
                    "model": model,
                    "type": model_type,
                    "task": model_config.get("task", "regression"),
                    "config": model_config
                }
            
            # Initialize meta-model
            if meta_model_type == "logistic":
                meta_model = LogisticRegression()
            elif meta_model_type == "linear":
                meta_model = LinearRegression()
            elif meta_model_type == "random_forest":
                meta_model = RandomForestClassifier() if base_models[0].get("task") == "classification" else RandomForestRegressor()
            else:
                meta_model = LogisticRegression()
            
            ensemble_config = {
                "status": "success",
                "ensemble_type": "stacking",
                "base_models": initialized_models,
                "meta_model": meta_model,
                "meta_model_type": meta_model_type,
                "n_base_models": len(initialized_models)
            }
            
            return ensemble_config
            
        except Exception as e:
            return {"status": "error", "message": f"Stacking ensemble creation failed: {str(e)}"}
    
    def train_stacking_ensemble(self, ensemble_config: Dict[str, Any], 
                               X_train: pd.DataFrame, y_train: pd.Series,
                               X_val: pd.DataFrame, y_val: pd.Series) -> Dict[str, Any]:
        """
        Train a stacking ensemble.
        
        Args:
            ensemble_config: Ensemble configuration
            X_train: Training features
            y_train: Training targets
            X_val: Validation features
            y_val: Validation targets
            
        Returns:
            Training results
        """
        try:
            base_models = ensemble_config["base_models"]
            meta_model = ensemble_config["meta_model"]
            
            # Train base models
            base_predictions_train = []
            base_predictions_val = []
            
            for model_name, model_info in base_models.items():
                model = model_info["model"]
                
                # Train base model
                model.fit(X_train, y_train)
                
                # Get predictions for meta-model training
                train_pred = model.predict(X_train)
                val_pred = model.predict(X_val)
                
                base_predictions_train.append(train_pred)
                base_predictions_val.append(val_pred)
            
            # Create meta-features
            meta_features_train = np.column_stack(base_predictions_train)
            meta_features_val = np.column_stack(base_predictions_val)
            
            # Train meta-model
            meta_model.fit(meta_features_train, y_train)
            
            # Evaluate ensemble
            val_pred = meta_model.predict(meta_features_val)
            
            # Calculate performance metrics
            if ensemble_config["meta_model_type"] in ["logistic", "random_forest"]:
                # Classification metrics
                accuracy = (val_pred == y_val).mean()
                performance = {"accuracy": accuracy}
            else:
                # Regression metrics
                mse = np.mean((val_pred - y_val) ** 2)
                mae = np.mean(np.abs(val_pred - y_val))
                r2 = 1 - (np.sum((y_val - val_pred) ** 2) / np.sum((y_val - np.mean(y_val)) ** 2))
                performance = {"mse": mse, "mae": mae, "r2": r2}
            
            result = {
                "status": "success",
                "ensemble_type": "stacking",
                "performance": performance,
                "n_base_models": len(base_models),
                "meta_model_type": ensemble_config["meta_model_type"]
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Stacking ensemble training failed: {str(e)}"}
    
    def create_blending_ensemble(self, base_models: List[Dict[str, Any]], 
                                weight_method: str = "equal") -> Dict[str, Any]:
        """
        Create a blending ensemble with dynamic weights.
        
        Args:
            base_models: List of base model configurations
            weight_method: Method for calculating weights (equal, performance, dynamic)
            
        Returns:
            Blending ensemble configuration
        """
        try:
            # Initialize base models
            initialized_models = {}
            for i, model_config in enumerate(base_models):
                model_name = f"base_model_{i}"
                model_type = model_config.get("type", "random_forest")
                params = model_config.get("parameters", {})
                
                if model_type == "random_forest":
                    if model_config.get("task") == "classification":
                        model = RandomForestClassifier(**params)
                    else:
                        model = RandomForestRegressor(**params)
                elif model_type == "logistic_regression":
                    model = LogisticRegression(**params)
                elif model_type == "linear_regression":
                    model = LinearRegression(**params)
                elif model_type == "svm":
                    if model_config.get("task") == "classification":
                        model = SVC(**params)
                    else:
                        model = SVR(**params)
                else:
                    continue
                
                initialized_models[model_name] = {
                    "model": model,
                    "type": model_type,
                    "task": model_config.get("task", "regression"),
                    "config": model_config,
                    "weight": 1.0 / len(base_models)  # Equal weights initially
                }
            
            ensemble_config = {
                "status": "success",
                "ensemble_type": "blending",
                "base_models": initialized_models,
                "weight_method": weight_method,
                "n_base_models": len(initialized_models)
            }
            
            return ensemble_config
            
        except Exception as e:
            return {"status": "error", "message": f"Blending ensemble creation failed: {str(e)}"}
    
    def train_blending_ensemble(self, ensemble_config: Dict[str, Any], 
                               X_train: pd.DataFrame, y_train: pd.Series,
                               X_val: pd.DataFrame, y_val: pd.Series) -> Dict[str, Any]:
        """
        Train a blending ensemble with dynamic weights.
        
        Args:
            ensemble_config: Ensemble configuration
            X_train: Training features
            y_train: Training targets
            X_val: Validation features
            y_val: Validation targets
            
        Returns:
            Training results
        """
        try:
            base_models = ensemble_config["base_models"]
            weight_method = ensemble_config["weight_method"]
            
            # Train base models and calculate individual performance
            model_performances = {}
            model_predictions = {}
            
            for model_name, model_info in base_models.items():
                model = model_info["model"]
                
                # Train base model
                model.fit(X_train, y_train)
                
                # Get predictions
                val_pred = model.predict(X_val)
                model_predictions[model_name] = val_pred
                
                # Calculate performance
                if model_info["task"] == "classification":
                    accuracy = (val_pred == y_val).mean()
                    model_performances[model_name] = accuracy
                else:
                    mse = np.mean((val_pred - y_val) ** 2)
                    model_performances[model_name] = 1 / (1 + mse)  # Convert to higher is better
                
                # Update model info
                base_models[model_name]["performance"] = model_performances[model_name]
            
            # Calculate weights based on method
            if weight_method == "equal":
                weights = {name: 1.0 / len(base_models) for name in base_models.keys()}
            elif weight_method == "performance":
                total_performance = sum(model_performances.values())
                weights = {name: perf / total_performance for name, perf in model_performances.items()}
            else:  # dynamic
                # Use performance-based weights with some equal weighting
                total_performance = sum(model_performances.values())
                weights = {}
                for name, perf in model_performances.items():
                    weights[name] = 0.7 * (perf / total_performance) + 0.3 * (1.0 / len(base_models))
            
            # Update weights in ensemble config
            for model_name, weight in weights.items():
                base_models[model_name]["weight"] = weight
            
            # Calculate blended predictions
            blended_pred = np.zeros(len(y_val))
            for model_name, pred in model_predictions.items():
                blended_pred += weights[model_name] * pred
            
            # Calculate ensemble performance
            if base_models[list(base_models.keys())[0]]["task"] == "classification":
                accuracy = (blended_pred.round() == y_val).mean()
                performance = {"accuracy": accuracy}
            else:
                mse = np.mean((blended_pred - y_val) ** 2)
                mae = np.mean(np.abs(blended_pred - y_val))
                r2 = 1 - (np.sum((y_val - blended_pred) ** 2) / np.sum((y_val - np.mean(y_val)) ** 2))
                performance = {"mse": mse, "mae": mae, "r2": r2}
            
            result = {
                "status": "success",
                "ensemble_type": "blending",
                "performance": performance,
                "weights": weights,
                "individual_performances": model_performances,
                "n_base_models": len(base_models)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Blending ensemble training failed: {str(e)}"}
    
    def bayesian_model_averaging(self, models: List[Dict[str, Any]], 
                                X_train: pd.DataFrame, y_train: pd.Series,
                                X_val: pd.DataFrame, y_val: pd.Series) -> Dict[str, Any]:
        """
        Perform Bayesian Model Averaging.
        
        Args:
            models: List of model configurations
            X_train: Training features
            y_train: Training targets
            X_val: Validation features
            y_val: Validation targets
            
        Returns:
            Bayesian Model Averaging results
        """
        try:
            # Train models and calculate likelihoods
            model_likelihoods = {}
            model_predictions = {}
            
            for i, model_config in enumerate(models):
                model_name = f"model_{i}"
                model_type = model_config.get("type", "random_forest")
                params = model_config.get("parameters", {})
                
                # Initialize model
                if model_type == "random_forest":
                    if model_config.get("task") == "classification":
                        model = RandomForestClassifier(**params)
                    else:
                        model = RandomForestRegressor(**params)
                elif model_type == "logistic_regression":
                    model = LogisticRegression(**params)
                elif model_type == "linear_regression":
                    model = LinearRegression(**params)
                else:
                    continue
                
                # Train model
                model.fit(X_train, y_train)
                
                # Get predictions
                val_pred = model.predict(X_val)
                model_predictions[model_name] = val_pred
                
                # Calculate likelihood (simplified)
                if model_config.get("task") == "classification":
                    accuracy = (val_pred == y_val).mean()
                    likelihood = accuracy
                else:
                    mse = np.mean((val_pred - y_val) ** 2)
                    likelihood = np.exp(-mse)  # Exponential likelihood
                
                model_likelihoods[model_name] = likelihood
            
            # Calculate posterior probabilities (Bayesian weights)
            total_likelihood = sum(model_likelihoods.values())
            if total_likelihood == 0:
                # Equal weights if no likelihood
                posterior_probs = {name: 1.0 / len(models) for name in model_likelihoods.keys()}
            else:
                posterior_probs = {name: likelihood / total_likelihood for name, likelihood in model_likelihoods.items()}
            
            # Calculate Bayesian averaged predictions
            bayesian_pred = np.zeros(len(y_val))
            for model_name, pred in model_predictions.items():
                bayesian_pred += posterior_probs[model_name] * pred
            
            # Calculate performance
            if models[0].get("task") == "classification":
                accuracy = (bayesian_pred.round() == y_val).mean()
                performance = {"accuracy": accuracy}
            else:
                mse = np.mean((bayesian_pred - y_val) ** 2)
                mae = np.mean(np.abs(bayesian_pred - y_val))
                r2 = 1 - (np.sum((y_val - bayesian_pred) ** 2) / np.sum((y_val - np.mean(y_val)) ** 2))
                performance = {"mse": mse, "mae": mae, "r2": r2}
            
            result = {
                "status": "success",
                "ensemble_type": "bayesian_averaging",
                "performance": performance,
                "posterior_probabilities": posterior_probs,
                "likelihoods": model_likelihoods,
                "n_models": len(models)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Bayesian Model Averaging failed: {str(e)}"}
    
    def dynamic_ensemble_selection(self, models: List[Dict[str, Any]], 
                                  X_train: pd.DataFrame, y_train: pd.Series,
                                  X_val: pd.DataFrame, y_val: pd.Series,
                                  selection_method: str = "best_k") -> Dict[str, Any]:
        """
        Perform dynamic ensemble selection.
        
        Args:
            models: List of model configurations
            X_train: Training features
            y_train: Training targets
            X_val: Validation features
            y_val: Validation targets
            selection_method: Selection method (best_k, performance_threshold, diversity)
            
        Returns:
            Dynamic ensemble selection results
        """
        try:
            # Train all models
            model_performances = {}
            model_predictions = {}
            
            for i, model_config in enumerate(models):
                model_name = f"model_{i}"
                model_type = model_config.get("type", "random_forest")
                params = model_config.get("parameters", {})
                
                # Initialize model
                if model_type == "random_forest":
                    if model_config.get("task") == "classification":
                        model = RandomForestClassifier(**params)
                    else:
                        model = RandomForestRegressor(**params)
                elif model_type == "logistic_regression":
                    model = LogisticRegression(**params)
                elif model_type == "linear_regression":
                    model = LinearRegression(**params)
                else:
                    continue
                
                # Train model
                model.fit(X_train, y_train)
                
                # Get predictions
                val_pred = model.predict(X_val)
                model_predictions[model_name] = val_pred
                
                # Calculate performance
                if model_config.get("task") == "classification":
                    accuracy = (val_pred == y_val).mean()
                    model_performances[model_name] = accuracy
                else:
                    mse = np.mean((val_pred - y_val) ** 2)
                    model_performances[model_name] = 1 / (1 + mse)
            
            # Select models based on method
            if selection_method == "best_k":
                k = min(3, len(models))  # Select top 3 models
                selected_models = sorted(model_performances.items(), key=lambda x: x[1], reverse=True)[:k]
            elif selection_method == "performance_threshold":
                threshold = 0.5  # Performance threshold
                selected_models = [(name, perf) for name, perf in model_performances.items() if perf >= threshold]
            else:  # diversity
                # Select models with diverse predictions
                selected_models = self._select_diverse_models(model_predictions, model_performances)
            
            # Calculate weights for selected models
            if not selected_models:
                # Fallback to all models with equal weights
                selected_models = list(model_performances.items())
            
            total_performance = sum(perf for _, perf in selected_models)
            weights = {name: perf / total_performance for name, perf in selected_models}
            
            # Calculate ensemble predictions
            ensemble_pred = np.zeros(len(y_val))
            for model_name, pred in model_predictions.items():
                if model_name in weights:
                    ensemble_pred += weights[model_name] * pred
            
            # Calculate performance
            if models[0].get("task") == "classification":
                accuracy = (ensemble_pred.round() == y_val).mean()
                performance = {"accuracy": accuracy}
            else:
                mse = np.mean((ensemble_pred - y_val) ** 2)
                mae = np.mean(np.abs(ensemble_pred - y_val))
                r2 = 1 - (np.sum((y_val - ensemble_pred) ** 2) / np.sum((y_val - np.mean(y_val)) ** 2))
                performance = {"mse": mse, "mae": mae, "r2": r2}
            
            result = {
                "status": "success",
                "ensemble_type": "dynamic_selection",
                "performance": performance,
                "selected_models": [name for name, _ in selected_models],
                "weights": weights,
                "selection_method": selection_method,
                "n_selected": len(selected_models)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Dynamic ensemble selection failed: {str(e)}"}
    
    def _select_diverse_models(self, model_predictions: Dict[str, np.ndarray], 
                              model_performances: Dict[str, float]) -> List[Tuple[str, float]]:
        """Select diverse models based on prediction correlation."""
        try:
            # Calculate correlation matrix between model predictions
            pred_matrix = np.column_stack(list(model_predictions.values()))
            corr_matrix = np.corrcoef(pred_matrix.T)
            
            # Select models with low correlation
            selected_models = []
            model_names = list(model_predictions.keys())
            
            # Start with best performing model
            best_model = max(model_performances.items(), key=lambda x: x[1])
            selected_models.append(best_model)
            
            # Add models with low correlation to selected ones
            for i, model_name in enumerate(model_names):
                if model_name == best_model[0]:
                    continue
                
                # Check correlation with already selected models
                max_corr = 0
                for selected_name, _ in selected_models:
                    selected_idx = model_names.index(selected_name)
                    corr = abs(corr_matrix[i, selected_idx])
                    max_corr = max(max_corr, corr)
                
                # Add if correlation is low enough
                if max_corr < 0.7:  # Threshold for diversity
                    selected_models.append((model_name, model_performances[model_name]))
            
            return selected_models
            
        except Exception as e:
            # Fallback to best performing models
            return sorted(model_performances.items(), key=lambda x: x[1], reverse=True)[:3]
