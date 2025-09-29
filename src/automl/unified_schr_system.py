# -*- coding: utf-8 -*-
"""
Unified SCHR Levels AutoML System
Единая система SCHR Levels AutoML

Объединяет лучшие части из schr-levels-gluon.py и src/automl/gluon/
Создает robust profitable ML-model для торгового бота
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import logging
from pathlib import Path
import warnings
from datetime import datetime, timedelta
import joblib
import argparse
import sys
import os
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import TimeSeriesSplit
import matplotlib.pyplot as plt
import seaborn as sns
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn, MofNCompleteColumn
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

# Disable CUDA for MacBook M1 and set OpenMP paths
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["AUTOGLUON_USE_GPU"] = "false"
os.environ["AUTOGLUON_USE_GPU_TORCH"] = "false"
os.environ["AUTOGLUON_USE_GPU_FASTAI"] = "false"

# Set OpenMP paths for macOS
os.environ["LDFLAGS"] = "-L/opt/homebrew/opt/libomp/lib"
os.environ["CPPFLAGS"] = "-I/opt/homebrew/opt/libomp/include"

# Configure threading for XGBoost and LightGBM to avoid OpenMP issues
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['VECLIB_MAXIMUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'

# Suppress AutoGluon output
os.environ['AUTOGLUON_VERBOSITY'] = '0'
os.environ['AUTOGLUON_LOG_LEVEL'] = 'ERROR'
os.environ['AUTOGLUON_QUIET'] = '1'
os.environ['AUTOGLUON_SILENT'] = '1'

# AutoGluon imports
try:
    from autogluon.tabular import TabularPredictor
    AUTOGLUON_AVAILABLE = True
except ImportError:
    AUTOGLUON_AVAILABLE = False
    TabularPredictor = None

warnings.filterwarnings('ignore')

# Initialize Rich console
console = Console()

# Setup logging with minimal verbosity
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Suppress AutoGluon preset messages
logging.getLogger('autogluon').setLevel(logging.ERROR)
logging.getLogger('autogluon.tabular').setLevel(logging.ERROR)

# Suppress Ray messages
logging.getLogger('ray').setLevel(logging.ERROR)
os.environ['RAY_DISABLE_IMPORT_WARNING'] = '1'
os.environ['RAY_DEDUP_LOGS'] = '0'

# File logging setup
os.makedirs('logs', exist_ok=True)
file_handler = logging.FileHandler('logs/unified_schr_system.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


class UnifiedSCHRSystem:
    """
    Unified SCHR Levels AutoML System
    
    Объединяет лучшие части из обеих реализаций:
    - Простота использования из schr-levels-gluon.py
    - Модульность и расширяемость из src/automl/gluon/
    - Robust validation для profitable trading
    """
    
    def __init__(self, data_path: str = "data/cache/csv_converted/", data_file: Optional[str] = None):
        """
        Initialize Unified SCHR System.
        
        Args:
            data_path: Path to data directory
            data_file: Specific data file for analysis
        """
        if not AUTOGLUON_AVAILABLE:
            raise ImportError("AutoGluon не установлен. Установите: pip install autogluon")
        
        self.data_path = Path(data_path)
        self.data_file = data_file
        self.models = {}
        self.results = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Enhanced task configurations
        self.task_configs = {
            'pressure_vector_sign': {
                'problem_type': 'binary',
                'eval_metric': 'roc_auc',
                'time_limit': 1800,
                'description': 'Prediction of PRESSURE_VECTOR sign (+ or -)'
            },
            'price_direction_1period': {
                'problem_type': 'multiclass', 
                'eval_metric': 'accuracy',
                'time_limit': 1800,
                'description': 'Price direction prediction (up/down/hold) for 1 period'
            },
            'level_breakout': {
                'problem_type': 'multiclass',
                'eval_metric': 'accuracy', 
                'time_limit': 2400,
                'description': 'Level breakout prediction (break high/break low/between levels)'
            },
            'trading_signal': {
                'problem_type': 'multiclass',
                'eval_metric': 'accuracy',
                'time_limit': 2000,
                'description': 'Comprehensive trading signal (buy/sell/hold)'
            }
        }
        
        console.print("🚀 Unified SCHR Levels AutoML System initialized", style="bold blue")
    
    def load_data(self, symbol: str = "BTCUSD", timeframe: str = "MN1") -> pd.DataFrame:
        """
        Enhanced data loading with universal support.
        
        Args:
            symbol: Trading symbol
            timeframe: Timeframe
            
        Returns:
            DataFrame with SCHR Levels data
        """
        if self.data_file:
            file_path = Path(self.data_file)
            if not file_path.exists():
                raise FileNotFoundError(f"Файл данных не найден: {file_path}")
            console.print(f"📁 Загружаем данные: {file_path.name}", style="blue")
        else:
            filename = f"CSVExport_{symbol}_PERIOD_{timeframe}.parquet"
            file_path = self.data_path / filename
            if not file_path.exists():
                raise FileNotFoundError(f"Файл не найден: {file_path}")
            console.print(f"📁 Загружаем данные: {filename}", style="blue")
        
        df = pd.read_parquet(file_path)
        
        # Enhanced data validation
        required_cols = ['Close', 'High', 'Open', 'Low', 'Volume', 'predicted_low', 'predicted_high', 'pressure', 'pressure_vector']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            logger.warning(f"Отсутствуют колонки: {missing_cols}")
        
        # Set datetime index
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
        elif df.index.name != 'Date' and not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.date_range(start='2020-01-01', periods=len(df), freq='MS' if timeframe == 'MN1' else 'D')
        
        console.print(f"📊 Загружено {len(df)} записей с {len(df.columns)} колонками", style="green")
        return df
    
    def create_enhanced_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create enhanced features combining basic and advanced techniques.
        
        Args:
            df: Input data
            
        Returns:
            DataFrame with enhanced features
        """
        logger.info("Creating enhanced features...")
        
        data = df.copy()
        
        # Basic technical indicators
        if 'Close' in data.columns:
            # Moving averages
            for window in [5, 10, 20, 50]:
                data[f'sma_{window}'] = data['Close'].rolling(window).mean()
                data[f'close_sma_{window}_ratio'] = data['Close'] / data[f'sma_{window}']
            
            # Volatility indicators
            data['volatility_5'] = data['Close'].pct_change().rolling(5).std()
            data['volatility_20'] = data['Close'].pct_change().rolling(20).std()
            data['atr_14'] = self._calculate_atr(data, 14)
            
            # RSI
            data['rsi_14'] = self._calculate_rsi(data['Close'], 14)
            
            # MACD
            macd_data = self._calculate_macd(data['Close'])
            data['macd'] = macd_data['macd']
            data['macd_signal'] = macd_data['signal']
            data['macd_histogram'] = macd_data['histogram']
        
        # SCHR Levels features
        if all(col in data.columns for col in ['Close', 'predicted_high', 'predicted_low']):
            # Distance to levels
            data['distance_to_high'] = (data['predicted_high'] - data['Close']) / data['Close']
            data['distance_to_low'] = (data['Close'] - data['predicted_low']) / data['Close']
            data['levels_spread'] = (data['predicted_high'] - data['predicted_low']) / data['Close']
            
            # Position within levels (0-1, where 0.5 = middle)
            data['position_in_levels'] = (data['Close'] - data['predicted_low']) / (data['predicted_high'] - data['predicted_low'])
            
            # Level breakout indicators
            data['near_high'] = (data['distance_to_high'] < 0.01).astype(int)
            data['near_low'] = (data['distance_to_low'] < 0.01).astype(int)
        
        # Pressure features
        if 'pressure' in data.columns:
            for lag in [1, 2, 3, 5]:
                data[f'pressure_lag_{lag}'] = data['pressure'].shift(lag)
            
            for window in [3, 5, 10]:
                data[f'pressure_sma_{window}'] = data['pressure'].rolling(window).mean()
                data[f'pressure_std_{window}'] = data['pressure'].rolling(window).std()
        
        if 'pressure_vector' in data.columns:
            for lag in [1, 2, 3]:
                data[f'pv_lag_{lag}'] = data['pressure_vector'].shift(lag)
            
            data['pv_sign_change'] = (data['pressure_vector'] * data['pressure_vector'].shift(1) < 0).astype(int)
            data['pv_magnitude'] = np.abs(data['pressure_vector'])
        
        # Time-based features
        if isinstance(data.index, pd.DatetimeIndex):
            data['hour'] = data.index.hour
            data['day_of_week'] = data.index.dayofweek
            data['month'] = data.index.month
            data['quarter'] = data.index.quarter
            data['year'] = data.index.year
        
        # Clean data
        data = data.replace([np.inf, -np.inf], np.nan)
        
        # Fill NaN values
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if data[col].isna().any():
                data[col] = data[col].fillna(data[col].median())
        
        data = data.fillna(0)
        
        logger.info(f"Created {len(data.columns)} features, {len(data)} records")
        return data
    
    def create_target_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create comprehensive target variables for all tasks.
        
        Args:
            df: Input data
            
        Returns:
            DataFrame with target variables
        """
        logger.info("Creating target variables...")
        
        data = df.copy()
        
        # Task 1: PRESSURE_VECTOR sign prediction
        if 'pressure_vector' in data.columns:
            pv_clean = data['pressure_vector'].replace([np.inf, -np.inf], np.nan)
            pv_sign = (pv_clean.shift(-1) > 0)
            data['target_pv_sign'] = pv_sign.astype(float)
            logger.info("✅ Created target_pv_sign")
        
        # Task 2: Price direction prediction
        if 'Close' in data.columns:
            future_returns = data['Close'].pct_change(1).shift(-1)
            future_returns_clean = future_returns.replace([np.inf, -np.inf], np.nan)
            price_direction = pd.cut(
                future_returns_clean, 
                bins=[-np.inf, -0.01, 0.01, np.inf], 
                labels=[0, 1, 2]  # 0=down, 1=hold, 2=up
            )
            data['target_price_direction'] = price_direction.astype(float)
            logger.info("✅ Created target_price_direction")
        
        # Task 3: Level breakout prediction
        if all(col in data.columns for col in ['Close', 'predicted_high', 'predicted_low']):
            close_next = data['Close'].shift(-1)
            pred_high = data['predicted_high'].replace([np.inf, -np.inf], np.nan)
            pred_low = data['predicted_low'].replace([np.inf, -np.inf], np.nan)
            
            valid_levels = ~(pred_high.isna() | pred_low.isna() | close_next.isna())
            
            conditions = [
                (close_next > pred_high) & valid_levels,  # Break high
                (close_next < pred_low) & valid_levels,     # Break low
                (close_next >= pred_low) & (close_next <= pred_high) & valid_levels  # Between levels
            ]
            choices = [2, 0, 1]  # 2=break high, 0=break low, 1=between levels
            
            data['target_level_breakout'] = np.select(conditions, choices, default=1).astype(float)
            logger.info("✅ Created target_level_breakout")
        
        # Task 4: Comprehensive trading signal
        if 'Close' in data.columns:
            # Combine multiple signals for comprehensive trading signal
            future_returns = data['Close'].pct_change(1).shift(-1)
            future_returns_clean = future_returns.replace([np.inf, -np.inf], np.nan)
            
            # Create trading signal based on multiple factors
            trading_signal = np.where(
                future_returns_clean > 0.02, 2,  # Strong buy
                np.where(future_returns_clean < -0.02, 0, 1)  # Strong sell, hold
            )
            data['target_trading_signal'] = trading_signal.astype(float)
            logger.info("✅ Created target_trading_signal")
        
        # Remove rows with NaN targets
        target_cols = [col for col in data.columns if col.startswith('target_')]
        data = data.dropna(subset=target_cols)
        
        logger.info(f"After creating targets: {len(data)} records")
        return data
    
    def train_robust_models(self, df: pd.DataFrame, test_size: float = 0.2) -> Dict[str, Any]:
        """
        Train robust models with enhanced validation.
        
        Args:
            df: Prepared data
            test_size: Test data ratio
            
        Returns:
            Training results
        """
        logger.info("Training robust models...")
        
        results = {}
        
        for task, config in self.task_configs.items():
            try:
                console.print(f"🤖 Training model for {task}...", style="blue")
                
                # Prepare data for task
                target_col = f'target_{task}'
                if target_col not in df.columns:
                    logger.warning(f"Target column {target_col} not found, skipping {task}")
                    continue
                
                # Remove other targets
                other_targets = [col for col in df.columns if col.startswith('target_') and col != target_col]
                task_data = df.drop(columns=other_targets, errors='ignore')
                task_data = task_data.dropna(subset=[target_col])
                
                # Time series split
                split_idx = int(len(task_data) * (1 - test_size))
                train_data = task_data.iloc[:split_idx]
                test_data = task_data.iloc[split_idx:]
                
                # Create unique model path
                model_path = f"models/unified_schr_{task}_{self.timestamp}"
                
                # Train model
                predictor = TabularPredictor(
                    label=target_col,
                    problem_type=config['problem_type'],
                    eval_metric=config['eval_metric'],
                    path=model_path
                )
                
                # Enhanced training configuration
                fit_args = {
                    'time_limit': config['time_limit'],
                    'presets': 'best_quality',
                    'excluded_model_types': [
                        'NN_TORCH', 'NN_FASTAI', 'FASTAI', 'NeuralNetFastAI'
                    ],
                    'num_bag_folds': 5,
                    'num_stack_levels': 1,
                    'verbosity': 0,
                    'ag_args_fit': {
                        'use_gpu': False,
                        'num_gpus': 0
                    }
                }
                
                # Train model
                predictor.fit(train_data, **fit_args)
                
                # Evaluate model
                predictions = predictor.predict(test_data)
                actual = test_data[target_col]
                
                # Calculate metrics
                if config['problem_type'] == 'binary':
                    metrics = {
                        'accuracy': accuracy_score(actual, predictions),
                        'precision': precision_score(actual, predictions, average='weighted', zero_division=0),
                        'recall': recall_score(actual, predictions, average='weighted', zero_division=0),
                        'f1': f1_score(actual, predictions, average='weighted', zero_division=0)
                    }
                else:
                    metrics = {
                        'accuracy': accuracy_score(actual, predictions),
                        'precision': precision_score(actual, predictions, average='weighted', zero_division=0),
                        'recall': recall_score(actual, predictions, average='weighted', zero_division=0),
                        'f1': f1_score(actual, predictions, average='weighted', zero_division=0)
                    }
                
                # Store results
                self.models[task] = predictor
                results[task] = {
                    'model_path': model_path,
                    'metrics': metrics,
                    'predictions': predictions,
                    'actual': actual,
                    'feature_importance': predictor.feature_importance(test_data),
                    'leaderboard': predictor.leaderboard(test_data, silent=True)
                }
                
                console.print(f"✅ {task} trained successfully - Accuracy: {metrics['accuracy']:.4f}", style="green")
                
            except Exception as e:
                logger.error(f"Error training {task}: {e}")
                results[task] = {'error': str(e)}
        
        return results
    
    def run_comprehensive_validation(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Run comprehensive validation including backtest, walk-forward, and Monte Carlo.
        
        Args:
            df: Prepared data
            
        Returns:
            Validation results
        """
        logger.info("Running comprehensive validation...")
        
        validation_results = {}
        
        for task, config in self.task_configs.items():
            if task not in self.models:
                continue
                
            console.print(f"🔍 Validating {task}...", style="blue")
            
            try:
                # Walk Forward Validation
                wf_results = self._walk_forward_validation(df, task)
                
                # Monte Carlo Validation
                mc_results = self._monte_carlo_validation(df, task)
                
                # Backtesting
                backtest_results = self._backtest_validation(df, task)
                
                validation_results[task] = {
                    'walk_forward': wf_results,
                    'monte_carlo': mc_results,
                    'backtest': backtest_results
                }
                
                console.print(f"✅ {task} validation completed", style="green")
                
            except Exception as e:
                logger.error(f"Error validating {task}: {e}")
                validation_results[task] = {'error': str(e)}
        
        return validation_results
    
    def _walk_forward_validation(self, df: pd.DataFrame, task: str, n_splits: int = 5) -> Dict[str, Any]:
        """Walk Forward validation."""
        target_col = f'target_{task}'
        if target_col not in df.columns:
            return {'error': f'Target column {target_col} not found'}
        
        data = df.dropna(subset=[target_col])
        tscv = TimeSeriesSplit(n_splits=n_splits)
        fold_results = []
        
        for fold, (train_idx, test_idx) in enumerate(tscv.split(data)):
            train_data = data.iloc[train_idx]
            test_data = data.iloc[test_idx]
            
            # Quick training for validation
            model_path = f"models/wf_{task}_fold_{fold}_{datetime.now().strftime('%H%M%S')}"
            config = self.task_configs[task]
            
            predictor = TabularPredictor(
                label=target_col,
                problem_type=config['problem_type'],
                eval_metric=config['eval_metric'],
                path=model_path
            )
            
            # Quick training
            fit_args = {
                'time_limit': 300,  # 5 minutes per fold
                'presets': 'medium_quality_faster_train',
                'excluded_model_types': ['NN_TORCH', 'NN_FASTAI', 'FASTAI', 'NeuralNetFastAI'],
                'verbosity': 0
            }
            
            predictor.fit(train_data, **fit_args)
            predictions = predictor.predict(test_data)
            actual = test_data[target_col]
            accuracy = accuracy_score(actual, predictions)
            
            fold_results.append({
                'fold': fold,
                'accuracy': accuracy,
                'train_size': len(train_data),
                'test_size': len(test_data)
            })
        
        accuracies = [r['accuracy'] for r in fold_results]
        return {
            'n_splits': n_splits,
            'fold_results': fold_results,
            'mean_accuracy': np.mean(accuracies),
            'std_accuracy': np.std(accuracies),
            'min_accuracy': np.min(accuracies),
            'max_accuracy': np.max(accuracies)
        }
    
    def _monte_carlo_validation(self, df: pd.DataFrame, task: str, n_iterations: int = 100) -> Dict[str, Any]:
        """Monte Carlo validation."""
        target_col = f'target_{task}'
        if target_col not in df.columns:
            return {'error': f'Target column {target_col} not found'}
        
        data = df.dropna(subset=[target_col])
        accuracies = []
        
        for i in range(n_iterations):
            if i % 10 == 0:
                logger.info(f"Monte Carlo iteration {i + 1}/{n_iterations}")
            
            # Random split with time series constraint
            split_idx = int(len(data) * (0.6 + np.random.uniform(-0.1, 0.1)))
            split_idx = max(int(len(data) * 0.5), min(int(len(data) * 0.9), split_idx))
            
            train_data = data.iloc[:split_idx]
            test_data = data.iloc[split_idx:]
            
            if len(test_data) < 10:
                continue
            
            try:
                # Quick training
                model_path = f"models/mc_{task}_iter_{i}_{datetime.now().strftime('%H%M%S')}"
                config = self.task_configs[task]
                
                predictor = TabularPredictor(
                    label=target_col,
                    problem_type=config['problem_type'],
                    eval_metric=config['eval_metric'],
                    path=model_path
                )
                
                fit_args = {
                    'time_limit': 120,  # 2 minutes per iteration
                    'presets': 'medium_quality_faster_train',
                    'excluded_model_types': ['NN_TORCH', 'NN_FASTAI', 'FASTAI', 'NeuralNetFastAI'],
                    'verbosity': 0
                }
                
                predictor.fit(train_data, **fit_args)
                predictions = predictor.predict(test_data)
                actual = test_data[target_col]
                accuracy = accuracy_score(actual, predictions)
                accuracies.append(accuracy)
                
            except Exception as e:
                logger.warning(f"Monte Carlo iteration {i} failed: {e}")
                continue
        
        if not accuracies:
            return {'error': 'No successful iterations'}
        
        return {
            'n_iterations': len(accuracies),
            'accuracies': accuracies,
            'mean_accuracy': np.mean(accuracies),
            'std_accuracy': np.std(accuracies),
            'min_accuracy': np.min(accuracies),
            'max_accuracy': np.max(accuracies),
            'stability_score': 1 - (np.std(accuracies) / np.mean(accuracies))
        }
    
    def _backtest_validation(self, df: pd.DataFrame, task: str) -> Dict[str, Any]:
        """Backtesting validation."""
        target_col = f'target_{task}'
        if target_col not in df.columns:
            return {'error': f'Target column {target_col} not found'}
        
        data = df.dropna(subset=[target_col])
        
        # Simple backtesting
        if 'Close' in data.columns:
            # Calculate returns based on predictions
            predictions = self.models[task].predict(data)
            actual = data[target_col]
            
            # Simple strategy: buy when prediction > 1, sell when prediction < 1
            if task == 'trading_signal':
                returns = np.where(
                    predictions == 2, data['Close'].pct_change().shift(-1),  # Buy
                    np.where(predictions == 0, -data['Close'].pct_change().shift(-1), 0)  # Sell
                )
            else:
                returns = np.where(
                    predictions > 1, data['Close'].pct_change().shift(-1),  # Long
                    np.where(predictions < 1, -data['Close'].pct_change().shift(-1), 0)  # Short
                )
            
            returns = pd.Series(returns, index=data.index).fillna(0)
            
            # Calculate metrics
            total_return = returns.sum()
            sharpe_ratio = returns.mean() / returns.std() if returns.std() > 0 else 0
            max_drawdown = (returns.cumsum() - returns.cumsum().expanding().max()).min()
            
            return {
                'total_return': total_return,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown,
                'accuracy': accuracy_score(actual, predictions)
            }
        
        return {'error': 'Close price not available for backtesting'}
    
    def _calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range."""
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(period).mean()
        
        return atr
    
    def _calculate_rsi(self, close: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index."""
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, pd.Series]:
        """Calculate MACD."""
        ema_fast = close.ewm(span=fast).mean()
        ema_slow = close.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()
        histogram = macd - signal_line
        
        return {
            'macd': macd,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def run_complete_pipeline(self, symbol: str = "BTCUSD", timeframe: str = "MN1") -> Dict[str, Any]:
        """
        Run complete unified pipeline.
        
        Args:
            symbol: Trading symbol
            timeframe: Timeframe
            
        Returns:
            Complete pipeline results
        """
        console.print(f"🚀 Starting Unified SCHR Pipeline for {symbol} {timeframe}", style="bold blue")
        
        pipeline_start = time.time()
        results = {}
        
        try:
            # Step 1: Load data
            console.print("📊 Step 1: Loading data...", style="blue")
            raw_data = self.load_data(symbol, timeframe)
            results['data_loading'] = {
                'total_rows': len(raw_data),
                'total_columns': len(raw_data.columns),
                'symbol': symbol,
                'timeframe': timeframe
            }
            
            # Step 2: Create features
            console.print("🔧 Step 2: Creating enhanced features...", style="blue")
            data_with_features = self.create_enhanced_features(raw_data)
            results['feature_engineering'] = {
                'features_created': len(data_with_features.columns),
                'data_shape': data_with_features.shape
            }
            
            # Step 3: Create targets
            console.print("🎯 Step 3: Creating target variables...", style="blue")
            data_with_targets = self.create_target_variables(data_with_features)
            results['target_creation'] = {
                'targets_created': len([col for col in data_with_targets.columns if col.startswith('target_')]),
                'final_data_shape': data_with_targets.shape
            }
            
            # Step 4: Train models
            console.print("🤖 Step 4: Training robust models...", style="blue")
            training_results = self.train_robust_models(data_with_targets)
            results['model_training'] = training_results
            
            # Step 5: Comprehensive validation
            console.print("🔍 Step 5: Running comprehensive validation...", style="blue")
            validation_results = self.run_comprehensive_validation(data_with_targets)
            results['validation'] = validation_results
            
            # Step 6: Generate summary
            console.print("📊 Step 6: Generating summary report...", style="blue")
            summary = self._generate_summary_report(results)
            results['summary'] = summary
            
            # Final success
            pipeline_time = time.time() - pipeline_start
            results['pipeline_summary'] = {
                'total_time_minutes': pipeline_time / 60,
                'pipeline_successful': True,
                'completion_time': datetime.now().isoformat()
            }
            
            console.print(f"✅ Unified pipeline completed successfully in {pipeline_time/60:.1f} minutes", style="bold green")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            results['pipeline_summary'] = {
                'pipeline_successful': False,
                'error': str(e),
                'completion_time': datetime.now().isoformat()
            }
        
        return results
    
    def _generate_summary_report(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive summary report."""
        
        report = f"""
# 🚀 UNIFIED SCHR LEVELS AUTOML SYSTEM REPORT
# Отчет единой системы SCHR Levels AutoML

## 📊 Pipeline Summary / Сводка пайплайна

**Execution Time:** {results.get('pipeline_summary', {}).get('total_time_minutes', 0):.1f} minutes
**Status:** {'✅ SUCCESS' if results.get('pipeline_summary', {}).get('pipeline_successful', False) else '❌ FAILED'}

## 📈 Data Processing / Обработка данных

**Data Loading:**
- Total Rows: {results.get('data_loading', {}).get('total_rows', 0):,}
- Total Columns: {results.get('data_loading', {}).get('total_columns', 0)}
- Symbol: {results.get('data_loading', {}).get('symbol', 'N/A')}
- Timeframe: {results.get('data_loading', {}).get('timeframe', 'N/A')}

**Feature Engineering:**
- Features Created: {results.get('feature_engineering', {}).get('features_created', 0)}
- Final Data Shape: {results.get('feature_engineering', {}).get('data_shape', 'N/A')}

## 🤖 Model Performance / Производительность модели

{self._format_model_results(results.get('model_training', {}))}

## 🔍 Validation Results / Результаты валидации

{self._format_validation_results(results.get('validation', {}))}

## 🎯 Recommendations / Рекомендации

1. **Model Quality:** {'✅ High' if self._is_high_quality(results) else '⚠️ Needs Improvement'}
2. **Production Ready:** {'✅ Yes' if self._is_production_ready(results) else '❌ No'}
3. **Next Steps:** {self._get_next_steps(results)}

---
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    def _format_model_results(self, model_results: Dict[str, Any]) -> str:
        """Format model results for report."""
        if not model_results:
            return "No model results available"
        
        formatted = ""
        for task, result in model_results.items():
            if 'error' in result:
                formatted += f"**{task}:** ❌ Error - {result['error']}\n"
            else:
                metrics = result.get('metrics', {})
                formatted += f"**{task}:**\n"
                formatted += f"- Accuracy: {metrics.get('accuracy', 0):.4f}\n"
                formatted += f"- F1-Score: {metrics.get('f1', 0):.4f}\n"
        
        return formatted
    
    def _format_validation_results(self, validation_results: Dict[str, Any]) -> str:
        """Format validation results for report."""
        if not validation_results:
            return "No validation results available"
        
        formatted = ""
        for task, result in validation_results.items():
            if 'error' in result:
                formatted += f"**{task}:** ❌ Error - {result['error']}\n"
            else:
                formatted += f"**{task}:**\n"
                
                if 'walk_forward' in result:
                    wf = result['walk_forward']
                    formatted += f"- Walk Forward: {wf.get('mean_accuracy', 0):.4f} ± {wf.get('std_accuracy', 0):.4f}\n"
                
                if 'monte_carlo' in result:
                    mc = result['monte_carlo']
                    formatted += f"- Monte Carlo: {mc.get('mean_accuracy', 0):.4f} ± {mc.get('std_accuracy', 0):.4f}\n"
                    formatted += f"- Stability: {mc.get('stability_score', 0):.4f}\n"
                
                if 'backtest' in result:
                    bt = result['backtest']
                    formatted += f"- Backtest Return: {bt.get('total_return', 0):.4f}\n"
                    formatted += f"- Sharpe Ratio: {bt.get('sharpe_ratio', 0):.4f}\n"
        
        return formatted
    
    def _is_high_quality(self, results: Dict[str, Any]) -> bool:
        """Check if models are high quality."""
        model_results = results.get('model_training', {})
        for task, result in model_results.items():
            if 'error' not in result:
                accuracy = result.get('metrics', {}).get('accuracy', 0)
                if accuracy < 0.6:
                    return False
        return True
    
    def _is_production_ready(self, results: Dict[str, Any]) -> bool:
        """Check if system is production ready."""
        return (results.get('pipeline_summary', {}).get('pipeline_successful', False) and
                self._is_high_quality(results))
    
    def _get_next_steps(self, results: Dict[str, Any]) -> str:
        """Get next steps recommendations."""
        if results.get('pipeline_summary', {}).get('pipeline_successful', False):
            return "Deploy to production, set up monitoring, schedule retraining"
        else:
            return "Fix pipeline issues, check data quality, retry"
    
    def predict_for_trading(self, new_data: pd.DataFrame, task: str) -> Dict[str, Any]:
        """
        Make predictions for trading.
        
        Args:
            new_data: New data for prediction
            task: Task to predict
            
        Returns:
            Prediction results
        """
        if task not in self.models:
            raise ValueError(f"Model for task {task} not trained")
        
        predictor = self.models[task]
        
        # Create features for new data
        features_data = self.create_enhanced_features(new_data)
        
        # Remove target columns if present
        target_cols = [col for col in features_data.columns if col.startswith('target_')]
        features_data = features_data.drop(columns=target_cols, errors='ignore')
        
        # Make predictions
        predictions = predictor.predict(features_data)
        probabilities = predictor.predict_proba(features_data) if predictor.can_predict_proba else None
        
        return {
            'predictions': predictions,
            'probabilities': probabilities,
            'confidence': probabilities.max(axis=1) if probabilities is not None else None
        }
    
    def save_models(self, save_path: str = "models/unified_schr_production/"):
        """Save trained models for production."""
        save_path = Path(save_path)
        save_path.mkdir(parents=True, exist_ok=True)
        
        for task, predictor in self.models.items():
            model_file = save_path / f"{task}_model.pkl"
            joblib.dump(predictor, model_file)
            logger.info(f"💾 Model {task} saved: {model_file}")
        
        # Save results
        results_file = save_path / "pipeline_results.pkl"
        joblib.dump(self.results, results_file)
        logger.info(f"💾 Results saved: {results_file}")


def main():
    """Main function for unified system."""
    parser = argparse.ArgumentParser(description="Unified SCHR Levels AutoML System")
    parser.add_argument('-f', '--file', type=str, help='Path to specific data file')
    parser.add_argument('-s', '--symbol', type=str, default='BTCUSD', help='Trading symbol')
    parser.add_argument('-t', '--timeframe', type=str, default='MN1', help='Timeframe')
    parser.add_argument('--data-path', type=str, default='data/cache/csv_converted/', help='Data path')
    
    args = parser.parse_args()
    
    try:
        # Create unified system
        system = UnifiedSCHRSystem(data_path=args.data_path, data_file=args.file)
        
        # Run complete pipeline
        if args.file:
            console.print(f"🚀 Running analysis for file: {args.file}", style="bold blue")
            results = system.run_complete_pipeline("CUSTOM", "CUSTOM")
        else:
            console.print(f"🚀 Running analysis for {args.symbol} {args.timeframe}", style="bold blue")
            results = system.run_complete_pipeline(args.symbol, args.timeframe)
        
        # Save models
        system.save_models()
        
        # Print summary
        console.print("\n" + "="*80, style="bold blue")
        console.print("📊 PIPELINE SUMMARY", style="bold blue")
        console.print("="*80, style="bold blue")
        console.print(results.get('summary', 'No summary available'))
        
        console.print("✅ Unified SCHR System completed successfully!", style="bold green")
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        raise


if __name__ == "__main__":
    main()
