"""
Main Pipeline for SCHR Levels AutoML

Core pipeline implementation for data processing and model training.
"""

import os
import pandas as pd
import numpy as np
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from autogluon.tabular import TabularPredictor


class SCHRLevelsAutoMLPipeline:
    """Main pipeline for SCHR Levels AutoML analysis"""
    
    def __init__(self, data_path: str = "data/cache/csv_converted/"):
        self.data_path = data_path
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.models = {}
        self.task_configs = {
            'pressure_vector_sign': {
                'problem_type': 'binary',
                'eval_metric': 'roc_auc',
                'time_limit': 1800
            },
            'price_direction_1period': {
                'problem_type': 'multiclass', 
                'eval_metric': 'accuracy',
                'time_limit': 1800
            },
            'level_breakout': {
                'problem_type': 'multiclass',
                'eval_metric': 'accuracy', 
                'time_limit': 2400
            }
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def load_schr_data(self, symbol: str, timeframe: str) -> pd.DataFrame:
        """Load SCHR Levels data from parquet files"""
        filename = f"CSVExport_{symbol}_PERIOD_{timeframe}.parquet"
        file_path = os.path.join(self.data_path, filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        self.logger.info(f"Loading data: {filename}")
        df = pd.read_parquet(file_path)
        
        # Check required columns
        required_cols = ['Close', 'High', 'Open', 'Low', 'Volume', 
                        'predicted_low', 'predicted_high', 'pressure', 'pressure_vector']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            self.logger.warning(f"Missing columns: {missing_cols}")
        
        # Set datetime index
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
        elif df.index.name != 'Date' and not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.date_range(start='2020-01-01', periods=len(df), 
                                   freq='MS' if timeframe == 'MN1' else 'D')
        
        self.logger.info(f"Loaded {len(df)} records with {len(df.columns)} columns")
        return df
    
    def create_target_variables(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create target variables for all tasks"""
        # Task 1: PRESSURE_VECTOR sign prediction
        if 'pressure_vector' in data.columns:
            pv_clean = data['pressure_vector'].replace([np.inf, -np.inf], np.nan)
            pv_sign = (pv_clean.shift(-1) > 0)
            data['target_pv_sign'] = pv_sign.astype(float)
            self.logger.info("Created target_pv_sign (0=negative, 1=positive)")
        
        # Task 2: Price direction on 1 period
        if 'Close' in data.columns:
            future_returns = data['Close'].pct_change(1).shift(-1)
            future_returns_clean = future_returns.replace([np.inf, -np.inf], np.nan)
            price_direction = pd.cut(
                future_returns_clean, 
                bins=[-np.inf, -0.01, 0.01, np.inf], 
                labels=[0, 1, 2]  # 0=down, 1=hold, 2=up
            )
            data['target_price_direction'] = price_direction.astype(float)
            self.logger.info("Created target_price_direction (0=down, 1=hold, 2=up) on 1 period")
        
        # Task 3: Level breakout prediction
        if all(col in data.columns for col in ['Close', 'predicted_high', 'predicted_low']):
            close_next = data['Close'].shift(-1)
            pred_high = data['predicted_high'].replace([np.inf, -np.inf], np.nan)
            pred_low = data['predicted_low'].replace([np.inf, -np.inf], np.nan)
            
            valid_levels = ~(pred_high.isna() | pred_low.isna() | close_next.isna())
            
            level_breakout = np.where(
                valid_levels,
                np.where(close_next > pred_high, 2,  # Above high
                        np.where(close_next < pred_low, 0, 1)),  # Below low, Between
                np.nan
            )
            data['target_level_breakout'] = level_breakout.astype(float)
            self.logger.info("Created target_level_breakout (0=below_low, 1=between, 2=above_high)")
        
        return data
    
    def create_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create additional features for ML models"""
        # Handle infinite values
        data = data.replace([np.inf, -np.inf], np.nan)
        
        # Fill NaN values for numeric columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if data[col].isna().any():
                data[col] = data[col].fillna(data[col].median())
        
        # Remove rows where all values are NaN
        data = data.dropna(how='all')
        
        # Fill remaining NaN with 0
        data = data.fillna(0)
        
        # Check for remaining infinite values
        if np.isinf(data.select_dtypes(include=[np.number])).any().any():
            self.logger.warning("Found infinite values, replacing with 0")
            data = data.replace([np.inf, -np.inf], 0)
        
        # Create technical indicators
        if 'Close' in data.columns:
            # Moving averages
            for period in [5, 10, 20]:
                data[f'sma_{period}'] = data['Close'].rolling(window=period).mean()
                data[f'close_sma_{period}_ratio'] = data['Close'] / data[f'sma_{period}']
            
            # Volatility
            for period in [5, 20]:
                data[f'volatility_{period}'] = data['Close'].rolling(window=period).std()
            
            # RSI
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['rsi'] = 100 - (100 / (1 + rs))
            
            # Distance to levels
            if 'predicted_high' in data.columns and 'predicted_low' in data.columns:
                data['distance_to_high'] = (data['predicted_high'] - data['Close']) / data['Close']
                data['distance_to_low'] = (data['Close'] - data['predicted_low']) / data['Close']
        
        self.logger.info(f"Created {len(data.columns)} features, {len(data)} records")
        return data
    
    def train_model(self, data: pd.DataFrame, task: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Train model for specific task"""
        try:
            config = self.task_configs[task].copy()
            config.update(kwargs)
            
            # Prepare data
            target_col = self._get_target_column(task)
            if target_col not in data.columns:
                raise ValueError(f"Target column {target_col} not found")
            
            # Remove other target columns
            other_targets = [col for col in data.columns if col.startswith('target_') and col != target_col]
            feature_data = data.drop(columns=other_targets)
            
            # Train model
            model_path = f"models/schr_levels_{task}_{self.timestamp}"
            predictor = TabularPredictor(
                label=target_col,
                problem_type=config['problem_type'],
                eval_metric=config['eval_metric'],
                path=model_path
            )
            
            # Configure training
            fit_args = {
                'time_limit': config['time_limit'],
                'presets': 'best_quality',
                'excluded_model_types': ['NN_TORCH', 'NN_FASTAI', 'FASTAI', 'NeuralNetFastAI'],
                'num_bag_folds': 5,
                'num_stack_levels': 1,
                'verbosity': 2,
                'ag_args_fit': {
                    'use_gpu': False,
                    'num_gpus': 0
                }
            }
            
            predictor.fit(feature_data, **fit_args)
            
            # Evaluate model
            test_data = feature_data.sample(frac=0.2, random_state=42)
            train_data = feature_data.drop(test_data.index)
            
            predictions = predictor.predict(test_data)
            probabilities = predictor.predict_proba(test_data) if predictor.can_predict_proba else None
            
            # Calculate metrics
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
            
            metrics = {
                'accuracy': accuracy_score(test_data[target_col], predictions),
                'precision': precision_score(test_data[target_col], predictions, average='weighted'),
                'recall': recall_score(test_data[target_col], predictions, average='weighted'),
                'f1_score': f1_score(test_data[target_col], predictions, average='weighted')
            }
            
            self.models[task] = predictor
            self.logger.info(f"Model for task {task} trained successfully")
            self.logger.info(f"Accuracy: {metrics['accuracy']:.4f}")
            
            return {
                'model': predictor,
                'metrics': metrics,
                'predictions': predictions,
                'probabilities': probabilities
            }
            
        except Exception as e:
            self.logger.error(f"Error training model for {task}: {e}")
            return None
    
    def predict(self, data: pd.DataFrame, task: str) -> pd.Series:
        """Make predictions using trained model"""
        try:
            model_path = f"models/schr_levels_{task}_{self.timestamp}"
            predictor = TabularPredictor.load(model_path)
            predictions = predictor.predict(data)
            return predictions
        except Exception as e:
            self.logger.error(f"Prediction error: {e}")
            raise
    
    def predict_for_trading(self, data: pd.DataFrame, task: str) -> Dict[str, Any]:
        """Make predictions for trading with probabilities"""
        try:
            model_path = f"models/schr_levels_{task}_{self.timestamp}"
            predictor = TabularPredictor.load(model_path)
            
            # Prepare features
            features_data = self.create_features(data)
            if len(features_data) == 0:
                raise ValueError("No data for prediction after feature creation")
            
            # Make predictions
            predictions = predictor.predict(features_data)
            probabilities = predictor.predict_proba(features_data) if predictor.can_predict_proba else None
            
            return {
                'predictions': predictions,
                'probabilities': probabilities
            }
            
        except Exception as e:
            self.logger.error(f"Trading prediction error: {e}")
            raise
    
    def _get_target_column(self, task: str) -> str:
        """Get target column name for task"""
        mapping = {
            'pressure_vector_sign': 'target_pv_sign',
            'price_direction_1period': 'target_price_direction',
            'level_breakout': 'target_level_breakout'
        }
        return mapping[task]
    
    def save_results(self, results: Dict[str, Any], output_dir: str):
        """Save analysis results"""
        os.makedirs(output_dir, exist_ok=True)
        
        import pickle
        with open(os.path.join(output_dir, 'analysis_results.pkl'), 'wb') as f:
            pickle.dump(results, f)
        
        self.logger.info(f"Results saved to {output_dir}")
