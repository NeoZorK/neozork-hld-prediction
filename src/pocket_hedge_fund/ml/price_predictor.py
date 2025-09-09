"""
Price Predictor for Pocket Hedge Fund.

This module provides machine learning models for price prediction
using various algorithms and features.
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import asyncio
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class PricePredictor:
    """Machine learning price predictor for trading signals."""
    
    def __init__(self, model_type: str = "ensemble"):
        """Initialize PricePredictor with specified model type."""
        self.model_type = model_type
        self.models = {}
        self.scalers = {}
        self.feature_columns = []
        self.is_trained = False
        self.model_metrics = {}
        
        # Initialize models based on type
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize ML models based on model type."""
        if self.model_type == "ensemble":
            self.models = {
                'random_forest': RandomForestRegressor(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42,
                    n_jobs=-1
                ),
                'gradient_boosting': GradientBoostingRegressor(
                    n_estimators=100,
                    max_depth=6,
                    learning_rate=0.1,
                    random_state=42
                ),
                'linear_regression': LinearRegression(),
                'ridge': Ridge(alpha=1.0)
            }
        elif self.model_type == "tree_based":
            self.models = {
                'random_forest': RandomForestRegressor(
                    n_estimators=200,
                    max_depth=15,
                    random_state=42,
                    n_jobs=-1
                ),
                'gradient_boosting': GradientBoostingRegressor(
                    n_estimators=200,
                    max_depth=8,
                    learning_rate=0.05,
                    random_state=42
                )
            }
        elif self.model_type == "linear":
            self.models = {
                'linear_regression': LinearRegression(),
                'ridge': Ridge(alpha=1.0)
            }
        
        # Initialize scalers for each model
        for model_name in self.models.keys():
            self.scalers[model_name] = StandardScaler()
    
    async def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for machine learning models."""
        try:
            logger.info("Preparing features for ML models")
            
            if data.empty:
                raise ValueError("No data provided for feature preparation")
            
            # Create a copy to avoid modifying original data
            features_df = data.copy()
            
            # Technical indicators as features
            features_df['sma_5'] = features_df['close'].rolling(window=5).mean()
            features_df['sma_10'] = features_df['close'].rolling(window=10).mean()
            features_df['sma_20'] = features_df['close'].rolling(window=20).mean()
            features_df['ema_5'] = features_df['close'].ewm(span=5).mean()
            features_df['ema_10'] = features_df['close'].ewm(span=10).mean()
            features_df['ema_20'] = features_df['close'].ewm(span=20).mean()
            
            # Price-based features
            features_df['price_change'] = features_df['close'].pct_change()
            features_df['price_change_2'] = features_df['close'].pct_change(2)
            features_df['price_change_5'] = features_df['close'].pct_change(5)
            
            # Volatility features
            features_df['volatility_5'] = features_df['price_change'].rolling(window=5).std()
            features_df['volatility_10'] = features_df['price_change'].rolling(window=10).std()
            features_df['volatility_20'] = features_df['price_change'].rolling(window=20).std()
            
            # Volume features
            features_df['volume_sma_5'] = features_df['volume'].rolling(window=5).mean()
            features_df['volume_sma_10'] = features_df['volume'].rolling(window=10).mean()
            features_df['volume_ratio'] = features_df['volume'] / features_df['volume_sma_10']
            
            # High-Low features
            features_df['hl_ratio'] = features_df['high'] / features_df['low']
            features_df['oc_ratio'] = features_df['open'] / features_df['close']
            features_df['price_range'] = (features_df['high'] - features_df['low']) / features_df['close']
            
            # RSI
            delta = features_df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            features_df['rsi'] = 100 - (100 / (1 + rs))
            
            # MACD
            ema_12 = features_df['close'].ewm(span=12).mean()
            ema_26 = features_df['close'].ewm(span=26).mean()
            features_df['macd'] = ema_12 - ema_26
            features_df['macd_signal'] = features_df['macd'].ewm(span=9).mean()
            features_df['macd_histogram'] = features_df['macd'] - features_df['macd_signal']
            
            # Bollinger Bands
            bb_period = 20
            bb_std = 2
            features_df['bb_middle'] = features_df['close'].rolling(window=bb_period).mean()
            bb_std_dev = features_df['close'].rolling(window=bb_period).std()
            features_df['bb_upper'] = features_df['bb_middle'] + (bb_std_dev * bb_std)
            features_df['bb_lower'] = features_df['bb_middle'] - (bb_std_dev * bb_std)
            features_df['bb_position'] = (features_df['close'] - features_df['bb_lower']) / (features_df['bb_upper'] - features_df['bb_lower'])
            
            # Time-based features
            if 'Date' in features_df.columns:
                features_df['hour'] = pd.to_datetime(features_df['Date']).dt.hour
                features_df['day_of_week'] = pd.to_datetime(features_df['Date']).dt.dayofweek
                features_df['is_weekend'] = features_df['day_of_week'].isin([5, 6]).astype(int)
            elif features_df.index.dtype == 'datetime64[ns]':
                features_df['hour'] = features_df.index.hour
                features_df['day_of_week'] = features_df.index.dayofweek
                features_df['is_weekend'] = features_df['day_of_week'].isin([5, 6]).astype(int)
            
            # Lag features
            for lag in [1, 2, 3, 5]:
                features_df[f'close_lag_{lag}'] = features_df['close'].shift(lag)
                features_df[f'volume_lag_{lag}'] = features_df['volume'].shift(lag)
            
            # Future price targets (for training)
            features_df['future_price_1'] = features_df['close'].shift(-1)
            features_df['future_price_5'] = features_df['close'].shift(-5)
            features_df['future_return_1'] = (features_df['future_price_1'] - features_df['close']) / features_df['close']
            features_df['future_return_5'] = (features_df['future_price_5'] - features_df['close']) / features_df['close']
            
            # Remove rows with NaN values
            features_df = features_df.dropna()
            
            # Define feature columns (exclude target variables and original columns)
            exclude_columns = ['Date', 'open', 'high', 'low', 'close', 'volume', 
                             'future_price_1', 'future_price_5', 'future_return_1', 'future_return_5']
            self.feature_columns = [col for col in features_df.columns if col not in exclude_columns]
            
            logger.info(f"Prepared {len(self.feature_columns)} features for ML models")
            return features_df
            
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            raise
    
    async def train_models(self, data: pd.DataFrame, target_column: str = 'future_return_1') -> Dict[str, Any]:
        """Train all ML models on the provided data."""
        try:
            logger.info(f"Training {self.model_type} models for target: {target_column}")
            
            # Prepare features
            features_df = await self.prepare_features(data)
            
            if features_df.empty:
                raise ValueError("No features prepared for training")
            
            # Prepare training data
            X = features_df[self.feature_columns]
            y = features_df[target_column]
            
            # Remove any remaining NaN values
            mask = ~(X.isna().any(axis=1) | y.isna())
            X = X[mask]
            y = y[mask]
            
            if len(X) == 0:
                raise ValueError("No valid training data after cleaning")
            
            # Split data for training and validation
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, shuffle=False
            )
            
            training_results = {}
            
            # Train each model
            for model_name, model in self.models.items():
                try:
                    logger.info(f"Training {model_name} model")
                    
                    # Scale features
                    X_train_scaled = self.scalers[model_name].fit_transform(X_train)
                    X_test_scaled = self.scalers[model_name].transform(X_test)
                    
                    # Train model
                    model.fit(X_train_scaled, y_train)
                    
                    # Make predictions
                    y_pred_train = model.predict(X_train_scaled)
                    y_pred_test = model.predict(X_test_scaled)
                    
                    # Calculate metrics
                    train_mse = mean_squared_error(y_train, y_pred_train)
                    test_mse = mean_squared_error(y_test, y_pred_test)
                    train_mae = mean_absolute_error(y_train, y_pred_train)
                    test_mae = mean_absolute_error(y_test, y_pred_test)
                    train_r2 = r2_score(y_train, y_pred_train)
                    test_r2 = r2_score(y_test, y_pred_test)
                    
                    # Cross-validation score
                    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='neg_mean_squared_error')
                    cv_score = -cv_scores.mean()
                    
                    training_results[model_name] = {
                        'train_mse': train_mse,
                        'test_mse': test_mse,
                        'train_mae': train_mae,
                        'test_mae': test_mae,
                        'train_r2': train_r2,
                        'test_r2': test_r2,
                        'cv_score': cv_score,
                        'feature_importance': self._get_feature_importance(model, model_name)
                    }
                    
                    logger.info(f"{model_name} - Test R²: {test_r2:.4f}, Test MSE: {test_mse:.6f}")
                    
                except Exception as e:
                    logger.error(f"Error training {model_name}: {e}")
                    training_results[model_name] = {'error': str(e)}
            
            self.is_trained = True
            self.model_metrics = training_results
            
            # Save models
            await self.save_models()
            
            return {
                'status': 'success',
                'models_trained': len([r for r in training_results.values() if 'error' not in r]),
                'training_results': training_results,
                'feature_columns': self.feature_columns,
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
        except Exception as e:
            logger.error(f"Error training models: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _get_feature_importance(self, model, model_name: str) -> Dict[str, float]:
        """Get feature importance for tree-based models."""
        try:
            if hasattr(model, 'feature_importances_'):
                importance_dict = dict(zip(self.feature_columns, model.feature_importances_))
                # Sort by importance
                return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
            elif hasattr(model, 'coef_'):
                # For linear models, use absolute coefficients
                coef_dict = dict(zip(self.feature_columns, np.abs(model.coef_)))
                return dict(sorted(coef_dict.items(), key=lambda x: x[1], reverse=True))
            else:
                return {}
        except Exception as e:
            logger.error(f"Error getting feature importance for {model_name}: {e}")
            return {}
    
    async def predict(self, data: pd.DataFrame, model_name: Optional[str] = None) -> Dict[str, Any]:
        """Make predictions using trained models."""
        try:
            if not self.is_trained:
                raise ValueError("Models must be trained before making predictions")
            
            # Prepare features
            features_df = await self.prepare_features(data)
            
            if features_df.empty:
                raise ValueError("No features prepared for prediction")
            
            # Get latest features
            latest_features = features_df[self.feature_columns].iloc[-1:].values
            
            predictions = {}
            
            # Make predictions with specified model or all models
            models_to_use = [model_name] if model_name else self.models.keys()
            
            for model_name in models_to_use:
                if model_name in self.models and model_name in self.scalers:
                    try:
                        # Scale features
                        features_scaled = self.scalers[model_name].transform(latest_features)
                        
                        # Make prediction
                        prediction = self.models[model_name].predict(features_scaled)[0]
                        
                        predictions[model_name] = {
                            'prediction': float(prediction),
                            'confidence': self._calculate_confidence(model_name, prediction)
                        }
                        
                    except Exception as e:
                        logger.error(f"Error making prediction with {model_name}: {e}")
                        predictions[model_name] = {'error': str(e)}
            
            # Calculate ensemble prediction
            if len(predictions) > 1:
                valid_predictions = [p['prediction'] for p in predictions.values() if 'prediction' in p]
                if valid_predictions:
                    ensemble_prediction = np.mean(valid_predictions)
                    predictions['ensemble'] = {
                        'prediction': float(ensemble_prediction),
                        'confidence': self._calculate_ensemble_confidence(predictions)
                    }
            
            return {
                'status': 'success',
                'predictions': predictions,
                'timestamp': datetime.now().isoformat(),
                'features_used': len(self.feature_columns)
            }
            
        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _calculate_confidence(self, model_name: str, prediction: float) -> float:
        """Calculate confidence score for a prediction."""
        try:
            # Simple confidence based on model performance
            if model_name in self.model_metrics and 'test_r2' in self.model_metrics[model_name]:
                r2_score = self.model_metrics[model_name]['test_r2']
                # Convert R² to confidence (0-1 scale)
                confidence = max(0, min(1, (r2_score + 1) / 2))
                return confidence
            else:
                return 0.5  # Default confidence
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.5
    
    def _calculate_ensemble_confidence(self, predictions: Dict[str, Any]) -> float:
        """Calculate confidence for ensemble prediction."""
        try:
            valid_predictions = [p for p in predictions.values() if 'confidence' in p]
            if valid_predictions:
                return np.mean([p['confidence'] for p in valid_predictions])
            else:
                return 0.5
        except Exception as e:
            logger.error(f"Error calculating ensemble confidence: {e}")
            return 0.5
    
    async def save_models(self, model_dir: str = "models"):
        """Save trained models to disk."""
        try:
            model_path = Path(model_dir)
            model_path.mkdir(exist_ok=True)
            
            for model_name, model in self.models.items():
                model_file = model_path / f"{model_name}_{self.model_type}.joblib"
                joblib.dump(model, model_file)
                logger.info(f"Saved {model_name} model to {model_file}")
            
            # Save scalers
            for scaler_name, scaler in self.scalers.items():
                scaler_file = model_path / f"{scaler_name}_{self.model_type}_scaler.joblib"
                joblib.dump(scaler, scaler_file)
                logger.info(f"Saved {scaler_name} scaler to {scaler_file}")
            
            # Save feature columns
            features_file = model_path / f"features_{self.model_type}.joblib"
            joblib.dump(self.feature_columns, features_file)
            logger.info(f"Saved feature columns to {features_file}")
            
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    async def load_models(self, model_dir: str = "models"):
        """Load trained models from disk."""
        try:
            model_path = Path(model_dir)
            
            if not model_path.exists():
                logger.warning(f"Model directory {model_dir} does not exist")
                return False
            
            # Load feature columns
            features_file = model_path / f"features_{self.model_type}.joblib"
            if features_file.exists():
                self.feature_columns = joblib.load(features_file)
                logger.info(f"Loaded feature columns from {features_file}")
            
            # Load models and scalers
            for model_name in self.models.keys():
                model_file = model_path / f"{model_name}_{self.model_type}.joblib"
                scaler_file = model_path / f"{model_name}_{self.model_type}_scaler.joblib"
                
                if model_file.exists() and scaler_file.exists():
                    self.models[model_name] = joblib.load(model_file)
                    self.scalers[model_name] = joblib.load(scaler_file)
                    logger.info(f"Loaded {model_name} model and scaler")
            
            self.is_trained = True
            return True
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about trained models."""
        return {
            'model_type': self.model_type,
            'is_trained': self.is_trained,
            'models': list(self.models.keys()),
            'feature_columns': self.feature_columns,
            'metrics': self.model_metrics
        }
