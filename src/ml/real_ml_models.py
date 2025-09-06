# -*- coding: utf-8 -*-
"""
Real ML Models Implementation for NeoZork Interactive ML Trading Strategy Development.

This module provides real machine learning models for trading strategy development.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Union
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.svm import SVR, SVC
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, classification_report
from sklearn.pipeline import Pipeline
import joblib
import logging
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelType:
    """Model type constants."""
    LINEAR_REGRESSION = "linear_regression"
    LOGISTIC_REGRESSION = "logistic_regression"
    RANDOM_FOREST_REGRESSOR = "random_forest_regressor"
    RANDOM_FOREST_CLASSIFIER = "random_forest_classifier"
    GRADIENT_BOOSTING = "gradient_boosting"
    SVM_REGRESSOR = "svm_regressor"
    SVM_CLASSIFIER = "svm_classifier"
    NEURAL_NETWORK_REGRESSOR = "neural_network_regressor"
    NEURAL_NETWORK_CLASSIFIER = "neural_network_classifier"

class FeatureType:
    """Feature type constants."""
    PRICE_FEATURES = "price_features"
    TECHNICAL_INDICATORS = "technical_indicators"
    VOLUME_FEATURES = "volume_features"
    TIME_FEATURES = "time_features"
    STATISTICAL_FEATURES = "statistical_features"

class RealMLModels:
    """Real ML models for trading strategy development."""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_columns = {}
        self.model_metrics = {}
        self.trained_models = {}
        
    def create_features(self, data: pd.DataFrame, feature_types: List[str] = None) -> pd.DataFrame:
        """Create features from raw data."""
        if feature_types is None:
            feature_types = [FeatureType.PRICE_FEATURES, FeatureType.TECHNICAL_INDICATORS]
        
        features_df = data.copy()
        
        # Price features
        if FeatureType.PRICE_FEATURES in feature_types:
            features_df = self._create_price_features(features_df)
        
        # Technical indicators
        if FeatureType.TECHNICAL_INDICATORS in feature_types:
            features_df = self._create_technical_indicators(features_df)
        
        # Volume features
        if FeatureType.VOLUME_FEATURES in feature_types:
            features_df = self._create_volume_features(features_df)
        
        # Time features
        if FeatureType.TIME_FEATURES in feature_types:
            features_df = self._create_time_features(features_df)
        
        # Statistical features
        if FeatureType.STATISTICAL_FEATURES in feature_types:
            features_df = self._create_statistical_features(features_df)
        
        return features_df
    
    def _create_price_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create price-based features."""
        df = data.copy()
        
        # Price changes
        df['price_change'] = df['close'].pct_change()
        df['price_change_abs'] = df['price_change'].abs()
        
        # Price ratios
        df['high_low_ratio'] = df['high'] / df['low']
        df['close_open_ratio'] = df['close'] / df['open']
        
        # Price positions
        df['close_position'] = (df['close'] - df['low']) / (df['high'] - df['low'])
        df['open_position'] = (df['open'] - df['low']) / (df['high'] - df['low'])
        
        # Rolling statistics
        for window in [5, 10, 20]:
            df[f'close_ma_{window}'] = df['close'].rolling(window=window).mean()
            df[f'close_std_{window}'] = df['close'].rolling(window=window).std()
            df[f'close_zscore_{window}'] = (df['close'] - df[f'close_ma_{window}']) / df[f'close_std_{window}']
        
        return df
    
    def _create_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create technical indicator features."""
        df = data.copy()
        
        # RSI
        df['rsi_14'] = self._calculate_rsi(df['close'], 14)
        df['rsi_21'] = self._calculate_rsi(df['close'], 21)
        
        # MACD
        macd_data = self._calculate_macd(df['close'])
        df['macd'] = macd_data['macd']
        df['macd_signal'] = macd_data['signal']
        df['macd_histogram'] = macd_data['histogram']
        
        # Bollinger Bands
        bb_data = self._calculate_bollinger_bands(df['close'])
        df['bb_upper'] = bb_data['upper']
        df['bb_middle'] = bb_data['middle']
        df['bb_lower'] = bb_data['lower']
        df['bb_width'] = (bb_data['upper'] - bb_data['lower']) / bb_data['middle']
        df['bb_position'] = (df['close'] - bb_data['lower']) / (bb_data['upper'] - bb_data['lower'])
        
        # Stochastic
        stoch_data = self._calculate_stochastic(df['high'], df['low'], df['close'])
        df['stoch_k'] = stoch_data['k']
        df['stoch_d'] = stoch_data['d']
        
        return df
    
    def _create_volume_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create volume-based features."""
        df = data.copy()
        
        # Volume changes
        df['volume_change'] = df['volume'].pct_change()
        df['volume_ma_ratio'] = df['volume'] / df['volume'].rolling(window=20).mean()
        
        # Price-volume features
        df['price_volume'] = df['close'] * df['volume']
        df['vwap'] = df['price_volume'].rolling(window=20).sum() / df['volume'].rolling(window=20).sum()
        
        return df
    
    def _create_time_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create time-based features."""
        df = data.copy()
        
        if 'timestamp' in df.columns:
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
            df['day_of_month'] = df['timestamp'].dt.day
            df['month'] = df['timestamp'].dt.month
            
            # Cyclical encoding
            df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
            df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
            df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
            df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        
        return df
    
    def _create_statistical_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create statistical features."""
        df = data.copy()
        
        # Rolling statistics
        for window in [5, 10, 20]:
            df[f'returns_{window}'] = df['close'].pct_change(window)
            df[f'volatility_{window}'] = df['close'].pct_change().rolling(window=window).std()
            df[f'skewness_{window}'] = df['close'].pct_change().rolling(window=window).skew()
            df[f'kurtosis_{window}'] = df['close'].pct_change().rolling(window=window).kurt()
        
        return df
    
    def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """Calculate RSI indicator."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, pd.Series]:
        """Calculate MACD indicator."""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()
        histogram = macd - signal_line
        
        return {
            'macd': macd,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def _calculate_bollinger_bands(self, prices: pd.Series, window: int = 20, std_dev: float = 2) -> Dict[str, pd.Series]:
        """Calculate Bollinger Bands."""
        middle = prices.rolling(window=window).mean()
        std = prices.rolling(window=window).std()
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        
        return {
            'upper': upper,
            'middle': middle,
            'lower': lower
        }
    
    def _calculate_stochastic(self, high: pd.Series, low: pd.Series, close: pd.Series, 
                            k_window: int = 14, d_window: int = 3) -> Dict[str, pd.Series]:
        """Calculate Stochastic oscillator."""
        lowest_low = low.rolling(window=k_window).min()
        highest_high = high.rolling(window=k_window).max()
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_window).mean()
        
        return {
            'k': k_percent,
            'd': d_percent
        }
    
    def prepare_data(self, data: pd.DataFrame, target_column: str = 'close', 
                    prediction_horizon: int = 1, feature_types: List[str] = None) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare data for ML training."""
        # Create features
        features_df = self.create_features(data, feature_types)
        
        # Create target variable (future price change)
        features_df['target'] = features_df[target_column].shift(-prediction_horizon)
        features_df['target_change'] = features_df['target'].pct_change()
        
        # Remove rows with NaN values
        features_df = features_df.dropna()
        
        # Separate features and target
        feature_columns = [col for col in features_df.columns 
                          if col not in ['target', 'target_change', 'timestamp', 'symbol', 'open_time', 'close_time']]
        
        # Select only numeric columns for ML
        numeric_columns = features_df[feature_columns].select_dtypes(include=[np.number]).columns.tolist()
        
        X = features_df[numeric_columns]
        y = features_df['target_change']
        
        # Store feature columns for later use
        self.feature_columns[target_column] = numeric_columns
        
        return X, y
    
    def train_model(self, model_type: str, X: pd.DataFrame, y: pd.Series, 
                   model_name: str = None, test_size: float = 0.2, 
                   random_state: int = 42) -> Dict[str, Any]:
        """Train a machine learning model."""
        if model_name is None:
            model_name = f"{model_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state, shuffle=False
            )
            
            # Create and train model
            model = self._create_model(model_type)
            
            # Scale features if needed
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model.fit(X_train_scaled, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test_scaled)
            
            # Calculate metrics
            metrics = self._calculate_metrics(y_test, y_pred, model_type)
            
            # Store model and scaler
            self.trained_models[model_name] = {
                'model': model,
                'scaler': scaler,
                'feature_columns': X.columns.tolist(),
                'model_type': model_type,
                'metrics': metrics,
                'trained_at': datetime.now()
            }
            
            # Store scaler separately
            self.scalers[model_name] = scaler
            
            result = {
                'status': 'success',
                'model_name': model_name,
                'model_type': model_type,
                'metrics': metrics,
                'feature_count': len(X.columns),
                'train_samples': len(X_train),
                'test_samples': len(X_test),
                'message': f'Model {model_name} trained successfully'
            }
            
            logger.info(f"Model {model_name} trained successfully with metrics: {metrics}")
            return result
            
        except Exception as e:
            error_msg = f"Model training failed: {str(e)}"
            logger.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg
            }
    
    def _create_model(self, model_type: str):
        """Create model instance based on type."""
        if model_type == ModelType.LINEAR_REGRESSION:
            return LinearRegression()
        elif model_type == ModelType.LOGISTIC_REGRESSION:
            return LogisticRegression(random_state=42, max_iter=1000)
        elif model_type == ModelType.RANDOM_FOREST_REGRESSOR:
            return RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        elif model_type == ModelType.RANDOM_FOREST_CLASSIFIER:
            return RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        elif model_type == ModelType.GRADIENT_BOOSTING:
            return GradientBoostingRegressor(n_estimators=100, random_state=42)
        elif model_type == ModelType.SVM_REGRESSOR:
            return SVR(kernel='rbf', C=1.0, gamma='scale')
        elif model_type == ModelType.SVM_CLASSIFIER:
            return SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
        elif model_type == ModelType.NEURAL_NETWORK_REGRESSOR:
            return MLPRegressor(hidden_layer_sizes=(100, 50), random_state=42, max_iter=500)
        elif model_type == ModelType.NEURAL_NETWORK_CLASSIFIER:
            return MLPClassifier(hidden_layer_sizes=(100, 50), random_state=42, max_iter=500)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    def _calculate_metrics(self, y_true: pd.Series, y_pred: np.ndarray, model_type: str) -> Dict[str, float]:
        """Calculate model metrics."""
        metrics = {}
        
        if 'regressor' in model_type or model_type in [ModelType.LINEAR_REGRESSION, ModelType.GRADIENT_BOOSTING]:
            # Regression metrics
            metrics['mse'] = mean_squared_error(y_true, y_pred)
            metrics['rmse'] = np.sqrt(metrics['mse'])
            metrics['mae'] = mean_absolute_error(y_true, y_pred)
            metrics['r2'] = r2_score(y_true, y_pred)
            
            # Direction accuracy (for trading)
            direction_true = np.sign(y_true)
            direction_pred = np.sign(y_pred)
            metrics['direction_accuracy'] = accuracy_score(direction_true, direction_pred)
            
        elif 'classifier' in model_type or model_type == ModelType.LOGISTIC_REGRESSION:
            # Classification metrics
            metrics['accuracy'] = accuracy_score(y_true, y_pred)
            
            # Additional classification metrics
            report = classification_report(y_true, y_pred, output_dict=True)
            metrics['precision'] = report['weighted avg']['precision']
            metrics['recall'] = report['weighted avg']['recall']
            metrics['f1_score'] = report['weighted avg']['f1-score']
        
        return metrics
    
    def predict(self, model_name: str, X: pd.DataFrame) -> Dict[str, Any]:
        """Make predictions using trained model."""
        if model_name not in self.trained_models:
            return {
                'status': 'error',
                'message': f'Model {model_name} not found'
            }
        
        try:
            model_info = self.trained_models[model_name]
            model = model_info['model']
            scaler = model_info['scaler']
            feature_columns = model_info['feature_columns']
            
            # Ensure we have the right features
            X_aligned = X[feature_columns]
            
            # Scale features
            X_scaled = scaler.transform(X_aligned)
            
            # Make predictions
            predictions = model.predict(X_scaled)
            
            return {
                'status': 'success',
                'predictions': predictions.tolist(),
                'model_name': model_name,
                'prediction_count': len(predictions)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Prediction failed: {str(e)}'
            }
    
    def get_model_info(self, model_name: str = None) -> Dict[str, Any]:
        """Get information about trained models."""
        if model_name:
            if model_name in self.trained_models:
                model_info = self.trained_models[model_name]
                return {
                    'status': 'success',
                    'model_name': model_name,
                    'model_type': model_info['model_type'],
                    'metrics': model_info['metrics'],
                    'feature_count': len(model_info['feature_columns']),
                    'trained_at': model_info['trained_at'].isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Model {model_name} not found'
                }
        else:
            # Return all models
            models_info = {}
            for name, info in self.trained_models.items():
                models_info[name] = {
                    'model_type': info['model_type'],
                    'metrics': info['metrics'],
                    'feature_count': len(info['feature_columns']),
                    'trained_at': info['trained_at'].isoformat()
                }
            
            return {
                'status': 'success',
                'models': models_info,
                'total_models': len(models_info)
            }
    
    def save_model(self, model_name: str, filepath: str) -> Dict[str, Any]:
        """Save trained model to file."""
        if model_name not in self.trained_models:
            return {
                'status': 'error',
                'message': f'Model {model_name} not found'
            }
        
        try:
            model_info = self.trained_models[model_name]
            joblib.dump(model_info, filepath)
            
            return {
                'status': 'success',
                'message': f'Model {model_name} saved to {filepath}'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to save model: {str(e)}'
            }
    
    def load_model(self, filepath: str, model_name: str = None) -> Dict[str, Any]:
        """Load trained model from file."""
        try:
            model_info = joblib.load(filepath)
            
            if model_name is None:
                model_name = f"loaded_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            self.trained_models[model_name] = model_info
            
            return {
                'status': 'success',
                'message': f'Model loaded as {model_name}',
                'model_name': model_name
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to load model: {str(e)}'
            }

# Example usage and testing
def test_real_ml_models():
    """Test real ML models with sample data."""
    print("🧪 Testing Real ML Models...")
    
    # Create sample data
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', periods=1000, freq='1H')
    
    # Generate realistic price data
    returns = np.random.normal(0, 0.02, 1000)
    prices = 100 * np.exp(np.cumsum(returns))
    
    data = pd.DataFrame({
        'timestamp': dates,
        'open': prices * (1 + np.random.normal(0, 0.001, 1000)),
        'high': prices * (1 + np.abs(np.random.normal(0, 0.01, 1000))),
        'low': prices * (1 - np.abs(np.random.normal(0, 0.01, 1000))),
        'close': prices,
        'volume': np.random.exponential(1000, 1000)
    })
    
    # Create ML models instance
    ml_models = RealMLModels()
    
    # Prepare data
    X, y = ml_models.prepare_data(data, target_column='close', prediction_horizon=1)
    print(f"  • Data prepared: {X.shape[0]} samples, {X.shape[1]} features")
    
    # Test different models
    models_to_test = [
        ModelType.LINEAR_REGRESSION,
        ModelType.RANDOM_FOREST_REGRESSOR,
        ModelType.GRADIENT_BOOSTING
    ]
    
    results = {}
    for model_type in models_to_test:
        print(f"  • Training {model_type}...")
        result = ml_models.train_model(model_type, X, y)
        
        if result['status'] == 'success':
            print(f"    ✅ {model_type}: R² = {result['metrics']['r2']:.3f}, Direction Accuracy = {result['metrics']['direction_accuracy']:.3f}")
            results[model_type] = result
        else:
            print(f"    ❌ {model_type}: {result['message']}")
    
    # Test predictions
    if results:
        model_name = list(results.keys())[0]
        print(f"  • Testing predictions with {model_name}...")
        
        # Use last 10 samples for prediction
        X_test = X.tail(10)
        pred_result = ml_models.predict(model_name, X_test)
        
        if pred_result['status'] == 'success':
            print(f"    ✅ Predictions generated: {pred_result['prediction_count']} predictions")
        else:
            print(f"    ❌ Prediction failed: {pred_result['message']}")
    
    # Get model info
    model_info = ml_models.get_model_info()
    print(f"  • Total trained models: {model_info['total_models']}")
    
    print("✅ Real ML Models test completed!")
    
    return ml_models

if __name__ == "__main__":
    test_real_ml_models()
