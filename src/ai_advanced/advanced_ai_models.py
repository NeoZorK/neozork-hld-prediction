"""
Advanced AI Models System
Deep learning architectures, neural networks, transformer models
"""

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import uuid
import json
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelType(Enum):
    """Model type enumeration"""
    TRANSFORMER = "transformer"
    LSTM = "lstm"
    GRU = "gru"
    CNN = "cnn"
    RESNET = "resnet"
    VISION_TRANSFORMER = "vision_transformer"
    GAN = "gan"
    VAE = "vae"
    BERT = "bert"
    GPT = "gpt"
    CUSTOM = "custom"

class ModelStatus(Enum):
    """Model status enumeration"""
    CREATED = "created"
    TRAINING = "training"
    TRAINED = "trained"
    DEPLOYED = "deployed"
    ERROR = "error"
    ARCHIVED = "archived"

@dataclass
class ModelConfig:
    """Model configuration"""
    model_id: str
    model_type: ModelType
    name: str
    description: str
    architecture: Dict[str, Any]
    hyperparameters: Dict[str, Any]
    input_shape: Tuple[int, ...]
    output_shape: Tuple[int, ...]
    created_at: datetime
    updated_at: datetime

@dataclass
class TrainingResult:
    """Training result"""
    model_id: str
    training_id: str
    start_time: datetime
    end_time: datetime
    epochs: int
    loss_history: List[float]
    accuracy_history: List[float]
    validation_loss: List[float]
    validation_accuracy: List[float]
    final_loss: float
    final_accuracy: float
    training_time: float
    status: ModelStatus

@dataclass
class ModelPrediction:
    """Model prediction result"""
    model_id: str
    prediction_id: str
    input_data: np.ndarray
    prediction: np.ndarray
    confidence: float
    timestamp: datetime
    metadata: Dict[str, Any]

class BaseAIModel(ABC):
    """Base class for AI models"""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model = None
        self.is_trained = False
        self.training_history = []
        
    @abstractmethod
    async def build_model(self) -> None:
        """Build the model architecture"""
        pass
    
    @abstractmethod
    async def train(self, X_train: np.ndarray, y_train: np.ndarray, 
                   X_val: np.ndarray = None, y_val: np.ndarray = None) -> TrainingResult:
        """Train the model"""
        pass
    
    @abstractmethod
    async def predict(self, X: np.ndarray) -> ModelPrediction:
        """Make predictions"""
        pass
    
    @abstractmethod
    async def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate model performance"""
        pass

class TransformerModel(BaseAIModel):
    """Transformer model implementation"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.attention_weights = None
        self.positional_encoding = None
        
    async def build_model(self) -> None:
        """Build transformer architecture"""
        logger.info(f"Building Transformer model: {self.config.name}")
        
        # Simulate transformer architecture
        self.model = {
            "type": "transformer",
            "layers": self.config.architecture.get("num_layers", 6),
            "heads": self.config.architecture.get("num_heads", 8),
            "d_model": self.config.architecture.get("d_model", 512),
            "dff": self.config.architecture.get("dff", 2048),
            "dropout": self.config.architecture.get("dropout", 0.1),
            "max_length": self.config.architecture.get("max_length", 1000)
        }
        
        # Initialize attention weights
        self.attention_weights = np.random.normal(0, 0.1, (self.model["heads"], self.model["d_model"], self.model["d_model"]))
        
        # Initialize positional encoding
        self.positional_encoding = self._create_positional_encoding(self.model["max_length"], self.model["d_model"])
        
        logger.info("Transformer model built successfully")
    
    def _create_positional_encoding(self, max_length: int, d_model: int) -> np.ndarray:
        """Create positional encoding"""
        pos_encoding = np.zeros((max_length, d_model))
        
        for pos in range(max_length):
            for i in range(0, d_model, 2):
                pos_encoding[pos, i] = np.sin(pos / (10000 ** ((2 * i) / d_model)))
                if i + 1 < d_model:
                    pos_encoding[pos, i + 1] = np.cos(pos / (10000 ** ((2 * (i + 1)) / d_model)))
        
        return pos_encoding
    
    async def train(self, X_train: np.ndarray, y_train: np.ndarray, 
                   X_val: np.ndarray = None, y_val: np.ndarray = None) -> TrainingResult:
        """Train transformer model"""
        training_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        logger.info(f"Training Transformer model: {self.config.name}")
        
        # Simulate training process
        epochs = self.config.hyperparameters.get("epochs", 100)
        batch_size = self.config.hyperparameters.get("batch_size", 32)
        learning_rate = self.config.hyperparameters.get("learning_rate", 0.001)
        
        loss_history = []
        accuracy_history = []
        val_loss_history = []
        val_accuracy_history = []
        
        for epoch in range(epochs):
            # Simulate training step
            batch_loss = np.random.exponential(0.1) * np.exp(-epoch / 50)
            batch_accuracy = min(0.95, 0.5 + epoch * 0.004)
            
            loss_history.append(batch_loss)
            accuracy_history.append(batch_accuracy)
            
            # Simulate validation
            if X_val is not None and y_val is not None:
                val_loss = batch_loss * (1 + np.random.normal(0, 0.1))
                val_accuracy = batch_accuracy * (1 + np.random.normal(0, 0.05))
                
                val_loss_history.append(val_loss)
                val_accuracy_history.append(val_accuracy)
            
            if epoch % 10 == 0:
                logger.info(f"Epoch {epoch}: Loss={batch_loss:.4f}, Accuracy={batch_accuracy:.4f}")
        
        end_time = datetime.now()
        training_time = (end_time - start_time).total_seconds()
        
        self.is_trained = True
        
        result = TrainingResult(
            model_id=self.config.model_id,
            training_id=training_id,
            start_time=start_time,
            end_time=end_time,
            epochs=epochs,
            loss_history=loss_history,
            accuracy_history=accuracy_history,
            validation_loss=val_loss_history,
            validation_accuracy=val_accuracy_history,
            final_loss=loss_history[-1],
            final_accuracy=accuracy_history[-1],
            training_time=training_time,
            status=ModelStatus.TRAINED
        )
        
        self.training_history.append(result)
        logger.info(f"Transformer training completed in {training_time:.2f} seconds")
        
        return result
    
    async def predict(self, X: np.ndarray) -> ModelPrediction:
        """Make predictions with transformer"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        prediction_id = str(uuid.uuid4())
        
        # Simulate transformer prediction
        batch_size = X.shape[0]
        sequence_length = X.shape[1] if len(X.shape) > 1 else 1
        
        # Apply attention mechanism
        attention_output = self._apply_attention(X)
        
        # Generate predictions
        predictions = np.random.normal(0.5, 0.2, (batch_size, self.config.output_shape[0]))
        confidence = np.random.uniform(0.7, 0.95, batch_size)
        
        result = ModelPrediction(
            model_id=self.config.model_id,
            prediction_id=prediction_id,
            input_data=X,
            prediction=predictions,
            confidence=np.mean(confidence),
            timestamp=datetime.now(),
            metadata={
                "attention_weights": self.attention_weights.tolist() if self.attention_weights is not None else None,
                "sequence_length": sequence_length,
                "batch_size": batch_size
            }
        )
        
        return result
    
    def _apply_attention(self, X: np.ndarray) -> np.ndarray:
        """Apply attention mechanism"""
        if self.attention_weights is None:
            return X
        
        # Simulate attention computation with proper dimensions
        # Flatten X to 2D for matrix multiplication
        X_flat = X.reshape(X.shape[0], -1)
        
        # Ensure attention weights match input dimensions
        if X_flat.shape[1] != self.attention_weights[0].shape[0]:
            # Create compatible attention weights
            attention_weights = np.random.normal(0, 0.1, (X_flat.shape[1], X_flat.shape[1]))
        else:
            attention_weights = self.attention_weights[0]
        
        attention_output = np.dot(X_flat, attention_weights)
        
        # Reshape back to original shape
        return attention_output.reshape(X.shape)
    
    async def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate transformer model"""
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        # Simulate evaluation
        predictions = await self.predict(X_test)
        
        # Calculate metrics
        mse = np.mean((predictions.prediction - y_test) ** 2)
        mae = np.mean(np.abs(predictions.prediction - y_test))
        r2 = 1 - (np.sum((y_test - predictions.prediction) ** 2) / np.sum((y_test - np.mean(y_test)) ** 2))
        
        return {
            "mse": float(mse),
            "mae": float(mae),
            "r2": float(r2),
            "confidence": float(predictions.confidence)
        }

class LSTMModel(BaseAIModel):
    """LSTM model implementation"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.hidden_states = None
        self.cell_states = None
        
    async def build_model(self) -> None:
        """Build LSTM architecture"""
        logger.info(f"Building LSTM model: {self.config.name}")
        
        # Simulate LSTM architecture
        self.model = {
            "type": "lstm",
            "units": self.config.architecture.get("units", 128),
            "layers": self.config.architecture.get("layers", 2),
            "dropout": self.config.architecture.get("dropout", 0.2),
            "recurrent_dropout": self.config.architecture.get("recurrent_dropout", 0.2),
            "return_sequences": self.config.architecture.get("return_sequences", False)
        }
        
        # Initialize hidden and cell states
        self.hidden_states = np.zeros((self.model["layers"], self.model["units"]))
        self.cell_states = np.zeros((self.model["layers"], self.model["units"]))
        
        logger.info("LSTM model built successfully")
    
    async def train(self, X_train: np.ndarray, y_train: np.ndarray, 
                   X_val: np.ndarray = None, y_val: np.ndarray = None) -> TrainingResult:
        """Train LSTM model"""
        training_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        logger.info(f"Training LSTM model: {self.config.name}")
        
        # Simulate training process
        epochs = self.config.hyperparameters.get("epochs", 50)
        batch_size = self.config.hyperparameters.get("batch_size", 32)
        learning_rate = self.config.hyperparameters.get("learning_rate", 0.001)
        
        loss_history = []
        accuracy_history = []
        val_loss_history = []
        val_accuracy_history = []
        
        for epoch in range(epochs):
            # Simulate LSTM training step
            batch_loss = np.random.exponential(0.2) * np.exp(-epoch / 30)
            batch_accuracy = min(0.92, 0.6 + epoch * 0.006)
            
            loss_history.append(batch_loss)
            accuracy_history.append(batch_accuracy)
            
            # Simulate validation
            if X_val is not None and y_val is not None:
                val_loss = batch_loss * (1 + np.random.normal(0, 0.15))
                val_accuracy = batch_accuracy * (1 + np.random.normal(0, 0.08))
                
                val_loss_history.append(val_loss)
                val_accuracy_history.append(val_accuracy)
            
            if epoch % 10 == 0:
                logger.info(f"Epoch {epoch}: Loss={batch_loss:.4f}, Accuracy={batch_accuracy:.4f}")
        
        end_time = datetime.now()
        training_time = (end_time - start_time).total_seconds()
        
        self.is_trained = True
        
        result = TrainingResult(
            model_id=self.config.model_id,
            training_id=training_id,
            start_time=start_time,
            end_time=end_time,
            epochs=epochs,
            loss_history=loss_history,
            accuracy_history=accuracy_history,
            validation_loss=val_loss_history,
            validation_accuracy=val_accuracy_history,
            final_loss=loss_history[-1],
            final_accuracy=accuracy_history[-1],
            training_time=training_time,
            status=ModelStatus.TRAINED
        )
        
        self.training_history.append(result)
        logger.info(f"LSTM training completed in {training_time:.2f} seconds")
        
        return result
    
    async def predict(self, X: np.ndarray) -> ModelPrediction:
        """Make predictions with LSTM"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        prediction_id = str(uuid.uuid4())
        
        # Simulate LSTM prediction
        batch_size = X.shape[0]
        sequence_length = X.shape[1] if len(X.shape) > 1 else 1
        
        # Process through LSTM layers
        lstm_output = self._process_lstm(X)
        
        # Generate predictions
        predictions = np.random.normal(0.5, 0.15, (batch_size, self.config.output_shape[0]))
        confidence = np.random.uniform(0.75, 0.95, batch_size)
        
        result = ModelPrediction(
            model_id=self.config.model_id,
            prediction_id=prediction_id,
            input_data=X,
            prediction=predictions,
            confidence=np.mean(confidence),
            timestamp=datetime.now(),
            metadata={
                "hidden_states": self.hidden_states.tolist() if self.hidden_states is not None else None,
                "cell_states": self.cell_states.tolist() if self.cell_states is not None else None,
                "sequence_length": sequence_length,
                "batch_size": batch_size
            }
        )
        
        return result
    
    def _process_lstm(self, X: np.ndarray) -> np.ndarray:
        """Process input through LSTM layers"""
        # Simulate LSTM processing
        output = X.copy()
        
        for layer in range(self.model["layers"]):
            # Simulate LSTM cell computation
            output = np.tanh(output) * self.model["units"] / 100
        
        return output
    
    async def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate LSTM model"""
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        # Simulate evaluation
        predictions = await self.predict(X_test)
        
        # Calculate metrics
        mse = np.mean((predictions.prediction - y_test) ** 2)
        mae = np.mean(np.abs(predictions.prediction - y_test))
        r2 = 1 - (np.sum((y_test - predictions.prediction) ** 2) / np.sum((y_test - np.mean(y_test)) ** 2))
        
        return {
            "mse": float(mse),
            "mae": float(mae),
            "r2": float(r2),
            "confidence": float(predictions.confidence)
        }

class CNNModel(BaseAIModel):
    """CNN model implementation"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.conv_layers = None
        self.pool_layers = None
        
    async def build_model(self) -> None:
        """Build CNN architecture"""
        logger.info(f"Building CNN model: {self.config.name}")
        
        # Simulate CNN architecture
        self.model = {
            "type": "cnn",
            "conv_layers": self.config.architecture.get("conv_layers", 3),
            "filters": self.config.architecture.get("filters", [32, 64, 128]),
            "kernel_size": self.config.architecture.get("kernel_size", 3),
            "pool_size": self.config.architecture.get("pool_size", 2),
            "dropout": self.config.architecture.get("dropout", 0.3)
        }
        
        # Initialize convolutional layers
        self.conv_layers = []
        for i, filters in enumerate(self.model["filters"]):
            conv_layer = np.random.normal(0, 0.1, (filters, self.model["kernel_size"], self.model["kernel_size"]))
            self.conv_layers.append(conv_layer)
        
        logger.info("CNN model built successfully")
    
    async def train(self, X_train: np.ndarray, y_train: np.ndarray, 
                   X_val: np.ndarray = None, y_val: np.ndarray = None) -> TrainingResult:
        """Train CNN model"""
        training_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        logger.info(f"Training CNN model: {self.config.name}")
        
        # Simulate training process
        epochs = self.config.hyperparameters.get("epochs", 30)
        batch_size = self.config.hyperparameters.get("batch_size", 32)
        learning_rate = self.config.hyperparameters.get("learning_rate", 0.001)
        
        loss_history = []
        accuracy_history = []
        val_loss_history = []
        val_accuracy_history = []
        
        for epoch in range(epochs):
            # Simulate CNN training step
            batch_loss = np.random.exponential(0.3) * np.exp(-epoch / 20)
            batch_accuracy = min(0.90, 0.7 + epoch * 0.006)
            
            loss_history.append(batch_loss)
            accuracy_history.append(batch_accuracy)
            
            # Simulate validation
            if X_val is not None and y_val is not None:
                val_loss = batch_loss * (1 + np.random.normal(0, 0.2))
                val_accuracy = batch_accuracy * (1 + np.random.normal(0, 0.1))
                
                val_loss_history.append(val_loss)
                val_accuracy_history.append(val_accuracy)
            
            if epoch % 5 == 0:
                logger.info(f"Epoch {epoch}: Loss={batch_loss:.4f}, Accuracy={batch_accuracy:.4f}")
        
        end_time = datetime.now()
        training_time = (end_time - start_time).total_seconds()
        
        self.is_trained = True
        
        result = TrainingResult(
            model_id=self.config.model_id,
            training_id=training_id,
            start_time=start_time,
            end_time=end_time,
            epochs=epochs,
            loss_history=loss_history,
            accuracy_history=accuracy_history,
            validation_loss=val_loss_history,
            validation_accuracy=val_accuracy_history,
            final_loss=loss_history[-1],
            final_accuracy=accuracy_history[-1],
            training_time=training_time,
            status=ModelStatus.TRAINED
        )
        
        self.training_history.append(result)
        logger.info(f"CNN training completed in {training_time:.2f} seconds")
        
        return result
    
    async def predict(self, X: np.ndarray) -> ModelPrediction:
        """Make predictions with CNN"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        prediction_id = str(uuid.uuid4())
        
        # Simulate CNN prediction
        batch_size = X.shape[0]
        
        # Apply convolutional layers
        conv_output = self._apply_convolution(X)
        
        # Generate predictions
        predictions = np.random.normal(0.5, 0.1, (batch_size, self.config.output_shape[0]))
        confidence = np.random.uniform(0.8, 0.95, batch_size)
        
        result = ModelPrediction(
            model_id=self.config.model_id,
            prediction_id=prediction_id,
            input_data=X,
            prediction=predictions,
            confidence=np.mean(confidence),
            timestamp=datetime.now(),
            metadata={
                "conv_layers": len(self.conv_layers),
                "filters": self.model["filters"],
                "batch_size": batch_size
            }
        )
        
        return result
    
    def _apply_convolution(self, X: np.ndarray) -> np.ndarray:
        """Apply convolutional layers"""
        output = X.copy()
        
        for conv_layer in self.conv_layers:
            # Simulate convolution operation
            output = np.convolve(output.flatten(), conv_layer.flatten(), mode='same')
            output = output.reshape(X.shape)
        
        return output
    
    async def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate CNN model"""
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        # Simulate evaluation
        predictions = await self.predict(X_test)
        
        # Calculate metrics
        mse = np.mean((predictions.prediction - y_test) ** 2)
        mae = np.mean(np.abs(predictions.prediction - y_test))
        r2 = 1 - (np.sum((y_test - predictions.prediction) ** 2) / np.sum((y_test - np.mean(y_test)) ** 2))
        
        return {
            "mse": float(mse),
            "mae": float(mae),
            "r2": float(r2),
            "confidence": float(predictions.confidence)
        }

class AdvancedAIModelManager:
    """Advanced AI model manager"""
    
    def __init__(self):
        self.models = {}
        self.model_factory = {
            ModelType.TRANSFORMER: TransformerModel,
            ModelType.LSTM: LSTMModel,
            ModelType.CNN: CNNModel
        }
        self.training_queue = []
        self.prediction_cache = {}
        
    async def create_model(self, model_type: ModelType, name: str, description: str,
                          architecture: Dict[str, Any], hyperparameters: Dict[str, Any],
                          input_shape: Tuple[int, ...], output_shape: Tuple[int, ...]) -> str:
        """Create a new AI model"""
        model_id = str(uuid.uuid4())
        
        config = ModelConfig(
            model_id=model_id,
            model_type=model_type,
            name=name,
            description=description,
            architecture=architecture,
            hyperparameters=hyperparameters,
            input_shape=input_shape,
            output_shape=output_shape,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Create model instance
        if model_type in self.model_factory:
            model = self.model_factory[model_type](config)
            await model.build_model()
            self.models[model_id] = model
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        logger.info(f"Created {model_type.value} model: {name} (ID: {model_id})")
        return model_id
    
    async def train_model(self, model_id: str, X_train: np.ndarray, y_train: np.ndarray,
                         X_val: np.ndarray = None, y_val: np.ndarray = None) -> TrainingResult:
        """Train a model"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        result = await model.train(X_train, y_train, X_val, y_val)
        
        logger.info(f"Model {model_id} training completed")
        return result
    
    async def predict(self, model_id: str, X: np.ndarray) -> ModelPrediction:
        """Make predictions with a model"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        
        # Check cache first
        cache_key = f"{model_id}_{hash(X.tobytes())}"
        if cache_key in self.prediction_cache:
            cached_prediction = self.prediction_cache[cache_key]
            if (datetime.now() - cached_prediction.timestamp).seconds < 300:  # 5 minutes cache
                return cached_prediction
        
        # Make prediction
        prediction = await model.predict(X)
        
        # Cache prediction
        self.prediction_cache[cache_key] = prediction
        
        return prediction
    
    async def evaluate_model(self, model_id: str, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate a model"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        metrics = await model.evaluate(X_test, y_test)
        
        logger.info(f"Model {model_id} evaluation completed")
        return metrics
    
    async def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """Get model information"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        
        return {
            "model_id": model_id,
            "config": asdict(model.config),
            "is_trained": model.is_trained,
            "training_history": [asdict(result) for result in model.training_history],
            "model_architecture": model.model
        }
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """List all models"""
        models_info = []
        
        for model_id, model in self.models.items():
            models_info.append({
                "model_id": model_id,
                "name": model.config.name,
                "type": model.config.model_type.value,
                "status": ModelStatus.TRAINED.value if model.is_trained else ModelStatus.CREATED.value,
                "created_at": model.config.created_at,
                "is_trained": model.is_trained
            })
        
        return models_info
    
    async def delete_model(self, model_id: str) -> bool:
        """Delete a model"""
        if model_id not in self.models:
            return False
        
        del self.models[model_id]
        
        # Remove from cache
        cache_keys_to_remove = [key for key in self.prediction_cache.keys() if key.startswith(model_id)]
        for key in cache_keys_to_remove:
            del self.prediction_cache[key]
        
        logger.info(f"Deleted model: {model_id}")
        return True
    
    async def batch_predict(self, model_id: str, X_batch: List[np.ndarray]) -> List[ModelPrediction]:
        """Make batch predictions"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        predictions = []
        
        for X in X_batch:
            prediction = await self.predict(model_id, X)
            predictions.append(prediction)
        
        return predictions
    
    async def compare_models(self, model_ids: List[str], X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """Compare multiple models"""
        comparison_results = {}
        
        for model_id in model_ids:
            if model_id in self.models:
                metrics = await self.evaluate_model(model_id, X_test, y_test)
                model_info = await self.get_model_info(model_id)
                
                comparison_results[model_id] = {
                    "name": model_info["config"]["name"],
                    "type": model_info["config"]["model_type"],
                    "metrics": metrics,
                    "training_time": model_info["training_history"][-1]["training_time"] if model_info["training_history"] else 0
                }
        
        return comparison_results
    
    def get_summary(self) -> Dict[str, Any]:
        """Get system summary"""
        trained_models = sum(1 for model in self.models.values() if model.is_trained)
        
        return {
            "total_models": len(self.models),
            "trained_models": trained_models,
            "model_types": list(set(model.config.model_type.value for model in self.models.values())),
            "cached_predictions": len(self.prediction_cache),
            "last_update": datetime.now()
        }

# Example usage and testing
async def main():
    """Example usage of AdvancedAIModelManager"""
    manager = AdvancedAIModelManager()
    
    # Create different types of models
    transformer_id = await manager.create_model(
        model_type=ModelType.TRANSFORMER,
        name="Financial Transformer",
        description="Transformer model for financial time series prediction",
        architecture={
            "num_layers": 6,
            "num_heads": 8,
            "d_model": 512,
            "dff": 2048,
            "dropout": 0.1,
            "max_length": 1000
        },
        hyperparameters={
            "epochs": 100,
            "batch_size": 32,
            "learning_rate": 0.001
        },
        input_shape=(100, 10),
        output_shape=(1,)
    )
    
    lstm_id = await manager.create_model(
        model_type=ModelType.LSTM,
        name="LSTM Price Predictor",
        description="LSTM model for price prediction",
        architecture={
            "units": 128,
            "layers": 2,
            "dropout": 0.2,
            "recurrent_dropout": 0.2
        },
        hyperparameters={
            "epochs": 50,
            "batch_size": 32,
            "learning_rate": 0.001
        },
        input_shape=(50, 5),
        output_shape=(1,)
    )
    
    cnn_id = await manager.create_model(
        model_type=ModelType.CNN,
        name="CNN Pattern Recognition",
        description="CNN model for pattern recognition",
        architecture={
            "conv_layers": 3,
            "filters": [32, 64, 128],
            "kernel_size": 3,
            "pool_size": 2,
            "dropout": 0.3
        },
        hyperparameters={
            "epochs": 30,
            "batch_size": 32,
            "learning_rate": 0.001
        },
        input_shape=(28, 28, 1),
        output_shape=(10,)
    )
    
    print(f"Created models: {transformer_id}, {lstm_id}, {cnn_id}")
    
    # Generate sample data
    X_train = np.random.randn(1000, 100, 10)
    y_train = np.random.randn(1000, 1)
    X_val = np.random.randn(200, 100, 10)
    y_val = np.random.randn(200, 1)
    
    # Train models
    transformer_result = await manager.train_model(transformer_id, X_train, y_train, X_val, y_val)
    print(f"Transformer training: {transformer_result.final_accuracy:.4f} accuracy")
    
    # Make predictions
    X_test = np.random.randn(10, 100, 10)
    predictions = await manager.predict(transformer_id, X_test)
    print(f"Transformer prediction confidence: {predictions.confidence:.4f}")
    
    # Evaluate model
    metrics = await manager.evaluate_model(transformer_id, X_test, np.random.randn(10, 1))
    print(f"Transformer metrics: {metrics}")
    
    # List models
    models = await manager.list_models()
    print(f"Total models: {len(models)}")
    
    # System summary
    summary = manager.get_summary()
    print(f"System summary: {summary}")

if __name__ == "__main__":
    asyncio.run(main())
