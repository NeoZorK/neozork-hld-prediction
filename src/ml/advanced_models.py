# -*- coding: utf-8 -*-
"""
Advanced ML Models and Trading Strategies for NeoZork Interactive ML Trading Strategy Development.

This module provides advanced machine learning models and trading strategies.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Union
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
# XGBoost and LightGBM will be imported when needed
XGBOOST_AVAILABLE = False
LIGHTGBM_AVAILABLE = False
import joblib
import logging
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedModelType:
    """Advanced model type constants."""
    XGBOOST = "xgboost"
    LIGHTGBM = "lightgbm"
    ADABOOST = "adaboost"
    RIDGE = "ridge"
    LASSO = "lasso"
    ELASTIC_NET = "elastic_net"
    DECISION_TREE = "decision_tree"
    SVM_RBF = "svm_rbf"
    SVM_POLY = "svm_poly"
    NEURAL_NETWORK = "neural_network"
    ENSEMBLE_STACKING = "ensemble_stacking"
    ENSEMBLE_BLENDING = "ensemble_blending"

class TradingStrategyType:
    """Trading strategy type constants."""
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    ARBITRAGE = "arbitrage"
    PAIRS_TRADING = "pairs_trading"
    BREAKOUT = "breakout"
    SCALPING = "scalping"
    SWING_TRADING = "swing_trading"
    TREND_FOLLOWING = "trend_following"
    CONTRARIAN = "contrarian"
    VOLATILITY_TRADING = "volatility_trading"

class AdvancedMLModels:
    """Advanced ML models for trading strategy development."""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_columns = {}
        self.model_metrics = {}
        self.trained_models = {}
        self.strategies = {}
        
    def create_advanced_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create advanced features for ML models."""
        df = data.copy()
        
        # Price-based features
        df = self._create_price_features(df)
        
        # Technical indicators
        df = self._create_technical_indicators(df)
        
        # Volume features
        df = self._create_volume_features(df)
        
        # Time-based features
        df = self._create_time_features(df)
        
        # Statistical features
        df = self._create_statistical_features(df)
        
        # Cross-asset features
        df = self._create_cross_asset_features(df)
        
        # Market microstructure features
        df = self._create_microstructure_features(df)
        
        return df
    
    def _create_price_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create advanced price-based features."""
        # Price ratios and positions
        df['high_low_ratio'] = df['high'] / df['low']
        df['close_open_ratio'] = df['close'] / df['open']
        df['close_position'] = (df['close'] - df['low']) / (df['high'] - df['low'])
        
        # Price momentum
        for window in [5, 10, 20, 50]:
            df[f'price_momentum_{window}'] = df['close'].pct_change(window)
            df[f'price_acceleration_{window}'] = df[f'price_momentum_{window}'].diff()
        
        # Price volatility
        for window in [5, 10, 20]:
            df[f'price_volatility_{window}'] = df['close'].rolling(window).std()
            df[f'price_volatility_ratio_{window}'] = df[f'price_volatility_{window}'] / df['close'].rolling(window).mean()
        
        # Price patterns
        df['doji'] = (abs(df['open'] - df['close']) / (df['high'] - df['low'])) < 0.1
        df['hammer'] = ((df['close'] - df['low']) / (df['high'] - df['low'])) > 0.6
        df['shooting_star'] = ((df['high'] - df['close']) / (df['high'] - df['low'])) > 0.6
        
        return df
    
    def _create_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create advanced technical indicators."""
        # RSI variations
        for period in [14, 21, 34]:
            df[f'rsi_{period}'] = self._calculate_rsi(df['close'], period)
            df[f'rsi_divergence_{period}'] = self._calculate_rsi_divergence(df['close'], df[f'rsi_{period}'])
        
        # MACD variations
        macd_data = self._calculate_macd(df['close'])
        df['macd'] = macd_data['macd']
        df['macd_signal'] = macd_data['signal']
        df['macd_histogram'] = macd_data['histogram']
        df['macd_divergence'] = self._calculate_macd_divergence(df['close'], df['macd'])
        
        # Bollinger Bands variations
        for period in [20, 50]:
            bb_data = self._calculate_bollinger_bands(df['close'], period)
            df[f'bb_upper_{period}'] = bb_data['upper']
            df[f'bb_middle_{period}'] = bb_data['middle']
            df[f'bb_lower_{period}'] = bb_data['lower']
            df[f'bb_width_{period}'] = (bb_data['upper'] - bb_data['lower']) / bb_data['middle']
            df[f'bb_position_{period}'] = (df['close'] - bb_data['lower']) / (bb_data['upper'] - bb_data['lower'])
        
        # Stochastic variations
        stoch_data = self._calculate_stochastic(df['high'], df['low'], df['close'])
        df['stoch_k'] = stoch_data['k']
        df['stoch_d'] = stoch_data['d']
        df['stoch_divergence'] = self._calculate_stoch_divergence(df['close'], df['stoch_k'])
        
        # Williams %R
        df['williams_r'] = self._calculate_williams_r(df['high'], df['low'], df['close'])
        
        # Commodity Channel Index
        df['cci'] = self._calculate_cci(df['high'], df['low'], df['close'])
        
        # Average True Range
        df['atr'] = self._calculate_atr(df['high'], df['low'], df['close'])
        
        return df
    
    def _create_volume_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create advanced volume features."""
        # Volume indicators
        df['volume_sma'] = df['volume'].rolling(20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma']
        df['volume_price_trend'] = df['volume'] * df['close'].pct_change()
        
        # On-Balance Volume
        df['obv'] = self._calculate_obv(df['close'], df['volume'])
        df['obv_sma'] = df['obv'].rolling(20).mean()
        
        # Volume Rate of Change
        df['volume_roc'] = df['volume'].pct_change(10)
        
        # Accumulation/Distribution Line
        df['ad_line'] = self._calculate_ad_line(df['high'], df['low'], df['close'], df['volume'])
        
        # Money Flow Index
        df['mfi'] = self._calculate_mfi(df['high'], df['low'], df['close'], df['volume'])
        
        return df
    
    def _create_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create advanced time-based features."""
        if 'timestamp' in df.columns:
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
            df['day_of_month'] = df['timestamp'].dt.day
            df['month'] = df['timestamp'].dt.month
            df['quarter'] = df['timestamp'].dt.quarter
            
            # Cyclical encoding
            df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
            df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
            df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
            df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
            df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
            df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
            
            # Market session indicators
            df['asian_session'] = ((df['hour'] >= 0) & (df['hour'] < 8)).astype(int)
            df['european_session'] = ((df['hour'] >= 8) & (df['hour'] < 16)).astype(int)
            df['american_session'] = ((df['hour'] >= 16) & (df['hour'] < 24)).astype(int)
        
        return df
    
    def _create_statistical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create advanced statistical features."""
        # Rolling statistics
        for window in [5, 10, 20, 50]:
            df[f'returns_{window}'] = df['close'].pct_change(window)
            df[f'volatility_{window}'] = df['close'].pct_change().rolling(window).std()
            df[f'skewness_{window}'] = df['close'].pct_change().rolling(window).skew()
            df[f'kurtosis_{window}'] = df['close'].pct_change().rolling(window).kurt()
            
            # Z-scores
            df[f'zscore_{window}'] = (df['close'] - df['close'].rolling(window).mean()) / df['close'].rolling(window).std()
            
            # Percentile ranks
            df[f'percentile_rank_{window}'] = df['close'].rolling(window).rank(pct=True)
        
        # Autocorrelation
        for lag in [1, 5, 10]:
            df[f'autocorr_{lag}'] = df['close'].pct_change().rolling(20).apply(lambda x: x.autocorr(lag=lag))
        
        return df
    
    def _create_cross_asset_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create cross-asset features."""
        # In real implementation, this would use multiple asset data
        # For now, we'll simulate with synthetic data
        
        # Correlation with market
        df['market_correlation'] = np.random.uniform(-0.8, 0.8, len(df))
        
        # Relative strength
        df['relative_strength'] = df['close'].pct_change() - df['market_correlation'] * 0.01
        
        # Beta
        df['beta'] = np.random.uniform(0.5, 2.0, len(df))
        
        return df
    
    def _create_microstructure_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create market microstructure features."""
        # Bid-ask spread simulation
        df['spread'] = np.random.uniform(0.001, 0.01, len(df))
        
        # Order flow imbalance
        df['order_flow_imbalance'] = np.random.uniform(-1, 1, len(df))
        
        # Market depth
        df['market_depth'] = np.random.uniform(1000, 10000, len(df))
        
        # Tick direction
        df['tick_direction'] = np.sign(df['close'].diff())
        
        return df
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_rsi_divergence(self, prices: pd.Series, rsi: pd.Series) -> pd.Series:
        """Calculate RSI divergence."""
        price_trend = prices.rolling(20).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        rsi_trend = rsi.rolling(20).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        return np.sign(price_trend) != np.sign(rsi_trend)
    
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
    
    def _calculate_macd_divergence(self, prices: pd.Series, macd: pd.Series) -> pd.Series:
        """Calculate MACD divergence."""
        price_trend = prices.rolling(20).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        macd_trend = macd.rolling(20).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        return np.sign(price_trend) != np.sign(macd_trend)
    
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
    
    def _calculate_stoch_divergence(self, prices: pd.Series, stoch_k: pd.Series) -> pd.Series:
        """Calculate Stochastic divergence."""
        price_trend = prices.rolling(20).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        stoch_trend = stoch_k.rolling(20).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        return np.sign(price_trend) != np.sign(stoch_trend)
    
    def _calculate_williams_r(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Williams %R."""
        highest_high = high.rolling(window=period).max()
        lowest_low = low.rolling(window=period).min()
        williams_r = -100 * ((highest_high - close) / (highest_high - lowest_low))
        return williams_r
    
    def _calculate_cci(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 20) -> pd.Series:
        """Calculate Commodity Channel Index."""
        typical_price = (high + low + close) / 3
        sma = typical_price.rolling(window=period).mean()
        mad = typical_price.rolling(window=period).apply(lambda x: np.mean(np.abs(x - x.mean())))
        cci = (typical_price - sma) / (0.015 * mad)
        return cci
    
    def _calculate_atr(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Average True Range."""
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()
        return atr
    
    def _calculate_obv(self, close: pd.Series, volume: pd.Series) -> pd.Series:
        """Calculate On-Balance Volume."""
        price_change = close.diff()
        obv = volume.copy()
        obv[price_change < 0] = -volume[price_change < 0]
        obv[price_change == 0] = 0
        return obv.cumsum()
    
    def _calculate_ad_line(self, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series) -> pd.Series:
        """Calculate Accumulation/Distribution Line."""
        clv = ((close - low) - (high - close)) / (high - low)
        clv = clv.fillna(0)
        ad_line = (clv * volume).cumsum()
        return ad_line
    
    def _calculate_mfi(self, high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Money Flow Index."""
        typical_price = (high + low + close) / 3
        money_flow = typical_price * volume
        
        positive_flow = money_flow.where(typical_price > typical_price.shift(), 0).rolling(window=period).sum()
        negative_flow = money_flow.where(typical_price < typical_price.shift(), 0).rolling(window=period).sum()
        
        mfi = 100 - (100 / (1 + positive_flow / negative_flow))
        return mfi
    
    def train_advanced_model(self, model_type: str, X: pd.DataFrame, y: pd.Series, 
                           model_name: str = None, test_size: float = 0.2, 
                           random_state: int = 42) -> Dict[str, Any]:
        """Train an advanced ML model."""
        if model_name is None:
            model_name = f"{model_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Split data
            split_idx = int(len(X) * (1 - test_size))
            X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
            y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
            
            # Create and train model
            model = self._create_advanced_model(model_type)
            
            # Scale features
            scaler = RobustScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            start_time = time.time()
            model.fit(X_train_scaled, y_train)
            training_time = time.time() - start_time
            
            # Make predictions
            y_pred = model.predict(X_test_scaled)
            
            # Calculate metrics
            metrics = self._calculate_advanced_metrics(y_test, y_pred, model_type)
            
            # Store model and scaler
            self.trained_models[model_name] = {
                'model': model,
                'scaler': scaler,
                'feature_columns': X.columns.tolist(),
                'model_type': model_type,
                'metrics': metrics,
                'training_time': training_time,
                'trained_at': datetime.now()
            }
            
            result = {
                'status': 'success',
                'model_name': model_name,
                'model_type': model_type,
                'metrics': metrics,
                'training_time': training_time,
                'feature_count': len(X.columns),
                'train_samples': len(X_train),
                'test_samples': len(X_test),
                'message': f'Advanced model {model_name} trained successfully'
            }
            
            logger.info(f"Advanced model {model_name} trained successfully with metrics: {metrics}")
            return result
            
        except Exception as e:
            error_msg = f"Advanced model training failed: {str(e)}"
            logger.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg
            }
    
    def _create_advanced_model(self, model_type: str):
        """Create advanced model instance."""
        if model_type == AdvancedModelType.XGBOOST:
            try:
                import xgboost as xgb
                return xgb.XGBRegressor(
                    n_estimators=100,
                    max_depth=6,
                    learning_rate=0.1,
                    random_state=42,
                    n_jobs=-1
                )
            except ImportError as e:
                raise ImportError(f"XGBoost not available: {e}")
        elif model_type == AdvancedModelType.LIGHTGBM:
            try:
                import lightgbm as lgb
                return lgb.LGBMRegressor(
                    n_estimators=100,
                    max_depth=6,
                    learning_rate=0.1,
                    random_state=42,
                    n_jobs=-1,
                    verbose=-1
                )
            except ImportError as e:
                raise ImportError(f"LightGBM not available: {e}")
        elif model_type == AdvancedModelType.ADABOOST:
            return AdaBoostRegressor(
                n_estimators=100,
                learning_rate=0.1,
                random_state=42
            )
        elif model_type == AdvancedModelType.RIDGE:
            return Ridge(alpha=1.0, random_state=42)
        elif model_type == AdvancedModelType.LASSO:
            return Lasso(alpha=0.1, random_state=42)
        elif model_type == AdvancedModelType.ELASTIC_NET:
            return ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42)
        elif model_type == AdvancedModelType.DECISION_TREE:
            return DecisionTreeRegressor(max_depth=10, random_state=42)
        elif model_type == AdvancedModelType.SVM_RBF:
            return SVR(kernel='rbf', C=1.0, gamma='scale')
        elif model_type == AdvancedModelType.SVM_POLY:
            return SVR(kernel='poly', C=1.0, degree=3)
        elif model_type == AdvancedModelType.NEURAL_NETWORK:
            return MLPRegressor(
                hidden_layer_sizes=(100, 50, 25),
                activation='relu',
                solver='adam',
                alpha=0.001,
                random_state=42,
                max_iter=500
            )
        else:
            raise ValueError(f"Unsupported advanced model type: {model_type}")
    
    def _calculate_advanced_metrics(self, y_true: pd.Series, y_pred: np.ndarray, model_type: str) -> Dict[str, float]:
        """Calculate advanced model metrics."""
        metrics = {}
        
        # Basic regression metrics
        metrics['mse'] = mean_squared_error(y_true, y_pred)
        metrics['rmse'] = np.sqrt(metrics['mse'])
        metrics['mae'] = mean_absolute_error(y_true, y_pred)
        metrics['r2'] = r2_score(y_true, y_pred)
        
        # Direction accuracy
        direction_true = np.sign(y_true)
        direction_pred = np.sign(y_pred)
        metrics['direction_accuracy'] = np.mean(direction_true == direction_pred)
        
        # Additional metrics
        metrics['mape'] = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        metrics['smape'] = np.mean(2 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred))) * 100
        
        # Sharpe ratio (for trading)
        returns = y_pred
        if np.std(returns) != 0:
            metrics['sharpe_ratio'] = np.mean(returns) / np.std(returns) * np.sqrt(252)
        else:
            metrics['sharpe_ratio'] = 0
        
        # Maximum drawdown
        if len(returns) > 0:
            cumulative = np.cumprod(1 + returns)
            running_max = np.maximum.accumulate(cumulative)
            drawdown = (cumulative - running_max) / running_max
            metrics['max_drawdown'] = np.min(drawdown)
        else:
            metrics['max_drawdown'] = 0
        
        return metrics

# Example usage and testing
def test_advanced_ml_models():
    """Test advanced ML models."""
    print("🧪 Testing Advanced ML Models...")
    
    # Create sample data
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', periods=2000, freq='1h')
    returns = np.random.normal(0, 0.02, 2000)
    prices = 100 * np.exp(np.cumsum(returns))
    
    data = pd.DataFrame({
        'timestamp': dates,
        'open': prices * (1 + np.random.normal(0, 0.001, 2000)),
        'high': prices * (1 + np.abs(np.random.normal(0, 0.01, 2000))),
        'low': prices * (1 - np.abs(np.random.normal(0, 0.01, 2000))),
        'close': prices,
        'volume': np.random.exponential(1000, 2000)
    })
    
    # Create advanced ML models instance
    ml_models = AdvancedMLModels()
    
    # Create advanced features
    features_df = ml_models.create_advanced_features(data)
    print(f"  • Advanced features created: {len(features_df.columns)} columns")
    
    # Prepare data for ML
    feature_columns = [col for col in features_df.columns 
                      if col not in ['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    feature_columns = features_df[feature_columns].select_dtypes(include=[np.number]).columns.tolist()
    
    X = features_df[feature_columns].dropna()
    y = features_df['close'].pct_change().shift(-1).dropna()
    
    # Align X and y
    common_idx = X.index.intersection(y.index)
    X = X.loc[common_idx]
    y = y.loc[common_idx]
    
    print(f"  • Data prepared for ML: {X.shape[0]} samples, {X.shape[1]} features")
    
    # Test advanced models
    models_to_test = [
        (AdvancedModelType.XGBOOST, "XGBoost"),
        (AdvancedModelType.LIGHTGBM, "LightGBM"),
        (AdvancedModelType.ADABOOST, "AdaBoost"),
        (AdvancedModelType.RIDGE, "Ridge"),
        (AdvancedModelType.NEURAL_NETWORK, "Neural Network")
    ]
    
    trained_models = 0
    for model_type, model_name in models_to_test:
        print(f"  • Training {model_name}...")
        result = ml_models.train_advanced_model(model_type, X, y)
        
        if result['status'] == 'success':
            metrics = result['metrics']
            print(f"    ✅ {model_name}: R² = {metrics['r2']:.3f}, Direction Accuracy = {metrics['direction_accuracy']:.3f}")
            print(f"        Training Time: {result['training_time']:.2f}s, Sharpe: {metrics['sharpe_ratio']:.3f}")
            trained_models += 1
        else:
            print(f"    ❌ {model_name}: {result['message']}")
    
    print(f"✅ Advanced ML Models test completed! {trained_models} models trained successfully.")
    
    return ml_models

if __name__ == "__main__":
    test_advanced_ml_models()
