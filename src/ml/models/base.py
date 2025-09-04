"""
Base classes for ML models in Neozork HLD Prediction system.

This module provides abstract base classes for all machine learning models.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, Tuple
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
from ...core.base import MLModel
from ...core.exceptions import MLError


class BaseMLModel(MLModel):
    """Base class for all machine learning models."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.model = None
        self.is_trained = False
        self.training_history = []
        self.feature_names = []
        self.target_name = ""
        self.model_type = self.__class__.__name__
        
    @abstractmethod
    def _create_model(self) -> Any:
        """Create the underlying ML model instance."""
        pass
    
    @abstractmethod
    def _validate_features(self, features: pd.DataFrame) -> bool:
        """Validate feature data before training/prediction."""
        pass
    
    def train(self, data: Any) -> bool:
        """Train the model with provided data."""
        try:
            if isinstance(data, dict):
                features = data.get("features")
                targets = data.get("targets")
            else:
                raise MLError("Data must be a dictionary with 'features' and 'targets' keys")
            
            if features is None or targets is None:
                raise MLError("Both features and targets must be provided")
            
            if not self._validate_features(features):
                raise MLError("Feature validation failed")
            
            self.feature_names = list(features.columns)
            self.target_name = targets.name if hasattr(targets, 'name') else "target"
            
            # Create and train model
            self.model = self._create_model()
            self._train_model(features, targets)
            
            self.is_trained = True
            self.training_history.append({
                "timestamp": datetime.now(),
                "features_count": len(self.feature_names),
                "samples_count": len(features)
            })
            
            self.logger.info(f"Model {self.name} trained successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Training failed: {e}")
            raise MLError(f"Training failed: {e}")
    
    @abstractmethod
    def _train_model(self, features: pd.DataFrame, targets: pd.Series):
        """Internal method to train the model."""
        pass
    
    def predict(self, data: Any) -> Any:
        """Make predictions using the trained model."""
        if not self.is_trained:
            raise MLError("Model must be trained before making predictions")
        
        if not self._validate_features(data):
            raise MLError("Feature validation failed for prediction data")
        
        try:
            predictions = self._make_predictions(data)
            self.logger.info(f"Made predictions for {len(data)} samples")
            return predictions
        except Exception as e:
            self.logger.error(f"Prediction failed: {e}")
            raise MLError(f"Prediction failed: {e}")
    
    @abstractmethod
    def _make_predictions(self, features: pd.DataFrame) -> Any:
        """Internal method to make predictions."""
        pass
    
    def evaluate(self, test_data: Any) -> Dict[str, float]:
        """Evaluate model performance on test data."""
        if not self.is_trained:
            raise MLError("Model must be trained before evaluation")
        
        try:
            if isinstance(test_data, dict):
                features = test_data.get("features")
                targets = test_data.get("targets")
            else:
                raise MLError("Test data must be a dictionary with 'features' and 'targets' keys")
            
            predictions = self.predict(features)
            metrics = self._calculate_metrics(targets, predictions)
            
            self.logger.info(f"Model evaluation completed: {metrics}")
            return metrics
            
        except Exception as e:
            self.logger.error(f"Evaluation failed: {e}")
            raise MLError(f"Evaluation failed: {e}")
    
    @abstractmethod
    def _calculate_metrics(self, targets: pd.Series, predictions: Any) -> Dict[str, float]:
        """Calculate evaluation metrics."""
        pass
    
    def save_model(self, path: str) -> bool:
        """Save the trained model to disk."""
        try:
            if not self.is_trained:
                raise MLError("Cannot save untrained model")
            
            os.makedirs(os.path.dirname(path), exist_ok=True)
            joblib.dump(self.model, path)
            
            # Save metadata
            metadata_path = path.replace('.joblib', '_metadata.json')
            metadata = {
                "name": self.name,
                "model_type": self.model_type,
                "feature_names": self.feature_names,
                "target_name": self.target_name,
                "training_history": self.training_history,
                "created_at": self.created_at.isoformat(),
                "saved_at": datetime.now().isoformat()
            }
            
            import json
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info(f"Model saved to {path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save model: {e}")
            raise MLError(f"Failed to save model: {e}")
    
    def load_model(self, path: str) -> bool:
        """Load a trained model from disk."""
        try:
            if not os.path.exists(path):
                raise MLError(f"Model file not found: {path}")
            
            self.model = joblib.load(path)
            
            # Load metadata
            metadata_path = path.replace('.joblib', '_metadata.json')
            if os.path.exists(metadata_path):
                import json
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                self.feature_names = metadata.get("feature_names", [])
                self.target_name = metadata.get("target_name", "")
                self.training_history = metadata.get("training_history", [])
            
            self.is_trained = True
            self.logger.info(f"Model loaded from {path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise MLError(f"Failed to load model: {e}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive information about the model."""
        return {
            "name": self.name,
            "model_type": self.model_type,
            "is_trained": self.is_trained,
            "feature_names": self.feature_names,
            "target_name": self.target_name,
            "training_history": self.training_history,
            "created_at": self.created_at.isoformat(),
            "parameters": self.parameters
        }
