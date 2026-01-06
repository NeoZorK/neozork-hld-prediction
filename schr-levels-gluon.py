# -*- coding: utf-8 -*-
"""
SCHR Levels AutoML Pipeline
Comprehensive solution for creating ML models on basis SCHR Levels indicators

Solves 3 main tasks:
1. Prediction sign PRESSURE_VECTOR (+ or -)
2. Prediction price direction for 5 periods (up/down/hold)
3. Prediction breakthrough PREDICTED_HIGH/PREDICTED_LOW or holding between them

Author: NeoZork HLDP
Version: 1.0
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
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["AUTOGLUON_Use_GPU"] = "false"
os.environ["AUTOGLUON_Use_GPU_TORCH"] = "false"
os.environ["AUTOGLUON_Use_GPU_FASTAI"] = "false"

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
 AUTOGLUON_available = True
except ImportError:
 AUTOGLUON_available = False
 TabularPredictor = None

warnings.filterwarnings('ignore')

# Initialize Rich console
console = Console()

# Setup logging with minimal verbosity
logging.basicConfig(
 level=logging.WARNING, # Minimal verbosity
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

# Function to suppress AutoGluon output
def suppress_autogluon_output():
 """Suppresses output AutoGluon including 'Preset alias specified' messages."""
 # Redirect stdout and stderr to devnull
 devnull = open(os.devnull, 'w')
 sys.stdout = devnull
 sys.stderr = devnull
 return devnull

def restore_output(devnull):
 """Restores standard output."""
 devnull.close()
 sys.stdout = sys.__stdout__
 sys.stderr = sys.__stderr__

# Custom print function to filter out preset messages
original_print = print
def filtered_print(*args, **kwargs):
 """Filters messages 'Preset alias specified'."""
 message = ' '.join(str(arg) for arg in args)
 if 'Preset alias specified' not in message:
 original_print(*args, **kwargs)

# Monkey patch print function
import builtins
builtins.print = filtered_print

# Ray import check
try:
 import ray
 RAY_available = True
 console.print("✅ Ray available - will be Used parallel training", style="green")
except ImportError:
 RAY_available = False
 console.print("⚠️ Ray not installed - will be used sequential training", style="yellow")
 console.print("💡 to install ray execute: pip install 'ray>=2.10.0,<2.45.0'", style="blue")

# File logging setup
os.makedirs('logs', exist_ok=True)
file_handler = logging.FileHandler('logs/schr_levels_automl.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


class SCHRLevelsAutoMLPipeline:
 """
 Comprehensive pipeline for creating ML models on basis SCHR Levels indicators.

 Solves 3 main tasks:
 1. Prediction sign PRESSURE_VECTOR (+ or -)
 2. Prediction price direction for 5 periods (up/down/hold)
 3. Prediction breakthrough PREDICTED_HIGH/PREDICTED_LOW or holding between them
 """

 def __init__(self, data_path: str = "data/cache/csv_converted/", data_file: Optional[str] = None):
 """
 Pipeline initialization.

 Args:
 data_path: Path to folder with data
 data_file: Specific data file for Analysis
 """
 if not AUTOGLUON_available:
 raise ImportError("AutoGluon not installed. install: pip install autogluon")

 self.data_path = Path(data_path)
 self.data_file = data_file
 self.models = {}
 self.results = {}
 self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

 # settings for different tasks
 self.task_configs = {
 'pressure_vector_sign': {
 'problem_type': 'binary',
 'eval_metric': 'roc_auc',
 'time_limit': 1800 # 30 minutes
 },
 'price_direction_1period': {
 'problem_type': 'multiclass',
 'eval_metric': 'accuracy',
 'time_limit': 1800 # 30 minutes
 },
 'level_breakout': {
 'problem_type': 'multiclass',
 'eval_metric': 'accuracy',
 'time_limit': 2400 # 40 minutes
 }
 }

 console.print("🚀 SCHR Levels AutoML Pipeline initialized", style="bold blue")

 # Informing about training mode
 if RAY_available:
 console.print("✅ Ray available - will be Used parallel training", style="green")
 else:
 console.print("⚠️ Ray not available - will be used sequential training", style="yellow")
 console.print("💡 for acceleration install ray: pip install 'ray>=2.10.0,<2.45.0'", style="blue")

 def load_schr_data(self, symbol: str = "BTCUSD", Timeframe: str = "MN1") -> pd.dataFrame:
 """
 Loading data SCHR Levels for specified symbol and Timeframe.

 Args:
 symbol: Trading symbol (BTCUSD, EURUSD, etc.)
 Timeframe: Timeframe (MN1, W1, D1, H4, H1, M15, M5, M1)

 Returns:
 dataFrame with data SCHR Levels
 """
 if self.data_file:
 # Use specific file if specified
 file_path = Path(self.data_file)
 if not file_path.exists():
 raise FileNotfoundError(f"data File not found: {file_path}")
 console.print(f"📁 Loading data: {file_path.name}", style="blue")
 else:
 # Use standard path
 filename = f"CSVExport_{symbol}_PERIOD_{Timeframe}.parquet"
 file_path = self.data_path / filename
 if not file_path.exists():
 raise FileNotfoundError(f"File not found: {file_path}")
 console.print(f"📁 Loading data: {filename}", style="blue")

 df = pd.read_parquet(file_path)

 # Checking presence of required columns
 required_cols = ['Close', 'High', 'Open', 'Low', 'Volume', 'predicted_low', 'predicted_high', 'pressure', 'pressure_vector']
 missing_cols = [col for col in required_cols if col not in df.columns]

 if missing_cols:
 logger.warning(f"Missing columns: {missing_cols}")

# Setting index as datetime if any
 if 'Date' in df.columns:
 df['Date'] = pd.to_datetime(df['Date'])
 df.set_index('Date', inplace=True)
 elif df.index.name != 'Date' and not isinstance(df.index, pd.DatetimeIndex):
# Creating temporary index if it is not available
 df.index = pd.date_range(start='2020-01-01', periods=len(df), freq='MS' if Timeframe == 'MN1' else 'D')

console.print(f"📊Uploaded {len(df)} records with {len(df.columns)} columns", style="green")
 return df

 def create_target_variables(self, df: pd.dataFrame) -> pd.dataFrame:
 """
create target variables for all 3 tasks.

 Args:
df: Source data SCHR Levels

 Returns:
dataFrame with added target variables
 """
logger.info("Creating target variables for 3 tasks...")

 data = df.copy()

# Task 1: Sign PRESSURE_VECTOR in the next period
 if 'pressure_vector' in data.columns:
# Processing NaN and inf values
 pv_clean = data['pressure_vector'].replace([np.inf, -np.inf], np.nan)
 pv_sign = (pv_clean.shift(-1) > 0)
data['target_pv_sign'] = pv_sign.astype(float) # Use float for compatibility
logger.info("✅Created target_pv_sign (0=negative, 1=positive)")

# Task 2: Price direction on 1 period
 if 'Close' in data.columns:
 future_returns = data['Close'].pct_change(1).shift(-1)
# Processing NaN values
 future_returns_clean = future_returns.replace([np.inf, -np.inf], np.nan)
 price_direction = pd.cut(
 future_returns_clean,
 bins=[-np.inf, -0.01, 0.01, np.inf],
 labels=[0, 1, 2] # 0=down, 1=hold, 2=up
 )
data['target_price_direction'] = price_direction.astype(float) # Use float for compatibility
logger.info("✅Created target_price_direction (0=down, 1=hold, 2=up) on 1 period")

# Challenge 3: Breaking through levels or holding between them
 if all(col in data.columns for col in ['Close', 'predicted_high', 'predicted_low']):
 close_next = data['Close'].shift(-1)
 pred_high = data['predicted_high'].replace([np.inf, -np.inf], np.nan)
 pred_low = data['predicted_low'].replace([np.inf, -np.inf], np.nan)

# Handle cases with NaN in levels
 valid_levels = ~(pred_high.isna() | pred_low.isna() | close_next.isna())

 conditions = [
(close_next > pred_high) & valid_levels, # Breaking up
(close_next < pred_low) & valid_levels, # Breaking down
(close_next >= pred_low) & (close_next <= pred_high) & valid_levels # Between levels
 ]
choices = [2, 0, 1] # 2=breakout up, 0=breakout down, 1=between levels

 data['target_level_breakout'] = np.select(conditions, choices, default=1).astype(float)
logger.info("✅Created target_level_breakout (0=breakout down, 1=between levels, 2=breakout up)")

# Deleting rows with NaN in target variables
 target_cols = [col for col in data.columns if col.startswith('target_')]
 data = data.dropna(subset=target_cols)

logger.info(f"After creating target variables: {len(data)} records")
 return data

 def create_features(self, df: pd.dataFrame) -> pd.dataFrame:
 """
create additional features to improve the quality of the model.

 Args:
df: data with target variables

 Returns:
dataFrame with additional signatures
 """
logger.info("Creating additional features...")

 data = df.copy()

# Technical indicators on basis of price
 if 'Close' in data.columns:
Moving Averages:
 for window in [5, 10, 20]:
 data[f'sma_{window}'] = data['Close'].rolling(window).mean()
 data[f'close_sma_{window}_ratio'] = data['Close'] / data[f'sma_{window}']

Volatility
 data['volatility_5'] = data['Close'].pct_change().rolling(5).std()
 data['volatility_20'] = data['Close'].pct_change().rolling(20).std()

# RSI Simplified
 delta = data['Close'].diff()
 gain = (delta.where(delta > 0, 0)).rolling(14).mean()
 loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
 rs = gain / loss
 data['rsi'] = 100 - (100 / (1 + rs))

# Signs on basis of SCHR levels
 if all(col in data.columns for col in ['Close', 'predicted_high', 'predicted_low']):
# Distance to levels
 data['distance_to_high'] = (data['predicted_high'] - data['Close']) / data['Close']
 data['distance_to_low'] = (data['Close'] - data['predicted_low']) / data['Close']
 data['levels_spread'] = (data['predicted_high'] - data['predicted_low']) / data['Close']

# Position relative to levels (0-1, where 0.5 = in the middle)
 data['position_in_levels'] = (data['Close'] - data['predicted_low']) / (data['predicted_high'] - data['predicted_low'])

# Signs on basis of pressure
 if 'pressure' in data.columns:
# Pressure lags
 for lag in [1, 2, 3]:
 data[f'pressure_lag_{lag}'] = data['pressure'].shift(lag)

# Moving average pressures
 for window in [3, 5, 10]:
 data[f'pressure_sma_{window}'] = data['pressure'].rolling(window).mean()

 if 'pressure_vector' in data.columns:
# Pressure vector lags
 for lag in [1, 2, 3]:
 data[f'pv_lag_{lag}'] = data['pressure_vector'].shift(lag)

# Change the sign of the pressure vector
 data['pv_sign_change'] = (data['pressure_vector'] * data['pressure_vector'].shift(1) < 0).astype(int)

# Temporary signs if there is a datetime index
 if isinstance(data.index, pd.DatetimeIndex):
 data['month'] = data.index.month
 data['quarter'] = data.index.quarter
 data['year'] = data.index.year

# Deleting lines with NaN
# Processing infinite values
 data = data.replace([np.inf, -np.inf], np.nan)

# Fill in the NaN values instead of deleting
# for numeric columns, fill in the median
 numeric_cols = data.select_dtypes(include=[np.number]).columns
 for col in numeric_cols:
 if data[col].isna().any():
 data[col] = data[col].fillna(data[col].median())

# Delete only rows with all NaN values
 data = data.dropna(how='all')

# If there is still NaN, fill in 0
 data = data.fillna(0)

# Checking on remaining infinite values
 if np.isinf(data.select_dtypes(include=[np.number])).any().any():
logger.warning("Infinite values detected, replace on 0")
 data = data.replace([np.inf, -np.inf], 0)

logger.info(f"Created {len(data.columns)} attributes, {len(data)} records")
 return data

 def prepare_data_for_task(self, df: pd.dataFrame, task: str) -> Tuple[pd.dataFrame, str]:
 """
Preparation of data for a specific task.

 Args:
df: data with signs and target variables
Task title

 Returns:
 Tuple[dataFrame, target_column]
 """
 target_mapping = {
 'pressure_vector_sign': 'target_pv_sign',
 'price_direction_1period': 'target_price_direction',
 'level_breakout': 'target_level_breakout'
 }

 target_col = target_mapping[task]

 if target_col not in df.columns:
raise ValueError(f"Target variable {target_col} not found")

# Delete other target variables
 other_targets = [col for col in target_mapping.values() if col != target_col]
 data = df.drop(columns=other_targets, errors='ignore')

# Delete the rows where the target variable is NaN
 data = data.dropna(subset=[target_col])

logger.info(f"Prepared data for task {task}: {len(data)} records")
 return data, target_col

 def train_model(self, df: pd.dataFrame, task: str, test_size: float = 0.2, progress=None, task_id=None) -> Dict[str, Any]:
 """
AutoGluon model training for a specific task.

 Args:
df: Prepared data
Task title
test_size: Proportion of test data

 Returns:
Dictionary with learning outcomes
 """
# Model training for task: {task}
 task_name = task.replace('_', ' ').title()

 data, target_col = self.prepare_data_for_task(df, task)
 config = self.task_configs[task]

# Time separation of data (important for time series)
 split_idx = int(len(data) * (1 - test_size))
 train_data = data.iloc[:split_idx]
 test_data = data.iloc[split_idx:]

# Training sample: {len(train_data)} records
# Test sample: {len(test_data)} records

# Create a unique path for the model
 model_path = f"models/schr_levels_{task}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# AutoGluon Model Training
 predictor = TabularPredictor(
 label=target_col,
 problem_type=config['problem_type'],
 eval_metric=config['eval_metric'],
 path=model_path
 )

# settings for MacBook M1 (disable only GPU models)
 fit_args = {
 'time_limit': config['time_limit'],
 'presets': 'best_quality',
 'excluded_model_types': [
'NN_TORCH', 'NN_FASTAI', 'FASTAI', 'NeuralNetFastAI' # GPU models only
 ],
 'num_bag_folds': 5,
 'num_stack_levels': 1,
 'verbosity': 0,
 'ag_args_fit': {
 'Use_gpu': False,
 'num_gpus': 0
 },
# Special settings for XGBoost and LightGBM
 'hyperparameters': {
 'XGB': {
 'n_jobs': 1,
 'n_estimators': 100,
 'max_depth': 6,
 'learning_rate': 0.1
 },
 'GBM': {
 'n_jobs': 1,
 'n_estimators': 100,
 'max_depth': 6,
 'learning_rate': 0.1,
 'verbose': -1
 }
 }
 }

# If ray is not available, Use sequential training
 if not RAY_available:
 logger.warning("Ray not available - Use sequential training")
fit_args['num_bag_folds'] = 0 # Disable bagging for sequential learning
fit_args['num_stack_levels'] = 0 # Disable stacking

# Suppress AutoGluon output
 devnull = suppress_autogluon_output()
 try:
# Update progress bar after Ray initialization
 if progress and task_id:
progress.update(task_id, description=f"🚀Initializing Ray and training {task_name}...")

# Additionally redirect stdout/stderr to suppress preset messages
 old_stdout = sys.stdout
 old_stderr = sys.stderr
 sys.stdout = devnull
 sys.stderr = devnull

 predictor.fit(train_data, **fit_args)

# Restore stdout/stderr
 sys.stdout = old_stdout
 sys.stderr = old_stderr

# Update the progress bar after completing the training
 if progress and task_id:
progress.update(task_id, description=f"✅Training {task_name} COMPLETED")

 finally:
 restore_output(devnull)

# Predictions on test data
 Predictions = predictor.predict(test_data)
 probabilities = predictor.predict_proba(test_data) if predictor.can_predict_proba else None

Quality evaluation
 actual = test_data[target_col]

 if config['problem_type'] == 'binary':
 metrics = {
 'accuracy': accuracy_score(actual, Predictions),
 'precision': precision_score(actual, Predictions, average='weighted', zero_division=0),
 'recall': recall_score(actual, Predictions, average='weighted', zero_division=0),
 'f1': f1_score(actual, Predictions, average='weighted', zero_division=0)
 }
 else: # multiclass
 metrics = {
 'accuracy': accuracy_score(actual, Predictions),
 'precision': precision_score(actual, Predictions, average='weighted', zero_division=0),
 'recall': recall_score(actual, Predictions, average='weighted', zero_division=0),
 'f1': f1_score(actual, Predictions, average='weighted', zero_division=0)
 }

# Save the model and results
 self.models[task] = predictor

 results = {
 'task': task,
 'model_path': model_path,
 'metrics': metrics,
 'Predictions': Predictions,
 'probabilities': probabilities,
 'actual': actual,
 'feature_importance': predictor.feature_importance(test_data),
 'leaderboard': predictor.leaderboard(test_data, silent=True)
 }

 self.results[task] = results

logger.info(f"✅Model for task {task} trained successfully")
logger.info(f"📊Accuracy: {metrics['accuracy']:.4f}")

 return results

 def walk_forward_validation(self, df: pd.dataFrame, task: str, n_splits: int = 5) -> Dict[str, Any]:
 """
Walk Forward validation to verify the robustness of the model.

 Args:
df: data for validation
Task title
n_splits: Number of splits

 Returns:
Validation Results
 """
# Walk Forward validation (no additional messages)

 data, target_col = self.prepare_data_for_task(df, task)
 config = self.task_configs[task]

 tscv = TimeSeriesSplit(n_splits=n_splits)
 fold_results = []

 for fold, (train_idx, test_idx) in enumerate(tscv.split(data)):
logger.info(f"Processing fold {fold + 1}/{n_splits}")

 train_data = data.iloc[train_idx]
 test_data = data.iloc[test_idx]

# Training the model on fold
 model_path = f"models/wf_{task}_fold_{fold}_{datetime.now().strftime('%H%M%S')}"

 predictor = TabularPredictor(
 label=target_col,
 problem_type=config['problem_type'],
 eval_metric=config['eval_metric'],
 path=model_path
 )

# Rapid training for validation (without GPU only)
 wf_fit_args = {
 'time_limit': 600, # 10 minutes on fold
 'presets': 'medium_quality_faster_train',
 'excluded_model_types': [
'NN_TORCH', 'NN_FASTAI', 'FASTAI', 'NeuralNetFastAI' # GPU models only
 ],
 'verbosity': 0,
 'ag_args_fit': {
 'Use_gpu': False,
 'num_gpus': 0
 },
# Special settings for XGBoost and LightGBM
 'hyperparameters': {
 'XGB': {
 'n_jobs': 1,
 'n_estimators': 50,
 'max_depth': 4,
 'learning_rate': 0.1
 },
 'GBM': {
 'n_jobs': 1,
 'n_estimators': 50,
 'max_depth': 4,
 'learning_rate': 0.1,
 'verbose': -1
 }
 }
 }

# If ray is not available, Use sequential training
 if not RAY_available:
 wf_fit_args['num_bag_folds'] = 0
 wf_fit_args['num_stack_levels'] = 0

# Suppress AutoGluon output
 devnull = suppress_autogluon_output()
 try:
 predictor.fit(train_data, **wf_fit_args)
 finally:
 restore_output(devnull)

of prediction,
 Predictions = predictor.predict(test_data)
 actual = test_data[target_col]

# Metrics for fold
 accuracy = accuracy_score(actual, Predictions)
 fold_results.append({
 'fold': fold,
 'accuracy': accuracy,
 'train_size': len(train_data),
 'test_size': len(test_data)
 })

 logger.info(f"Fold {fold + 1} accuracy: {accuracy:.4f}")

# Aggregated results
 accuracies = [r['accuracy'] for r in fold_results]
 wf_results = {
 'task': task,
 'n_splits': n_splits,
 'fold_results': fold_results,
 'mean_accuracy': np.mean(accuracies),
 'std_accuracy': np.std(accuracies),
 'min_accuracy': np.min(accuracies),
 'max_accuracy': np.max(accuracies)
 }

# Walk Forward validation completed
logger.info(f"📊Average accuracy: {wf_results['mean_accuracy']:.4f} ± {wf_results['std_accuracy']:.4f}")

 return wf_results

 def monte_carlo_validation(self, df: pd.dataFrame, task: str, n_iterations: int = 100, test_size: float = 0.2) -> Dict[str, Any]:
 """
Monte Carlo validation to assess the stability of the model.

 Args:
df: data for validation
Task title
n_iterations: Number of iterations
test_size: Proportion of test data

 Returns:
Monte Carlo validation results
 """
# Monte Carlo validation (no additional messages)

 data, target_col = self.prepare_data_for_task(df, task)
 config = self.task_configs[task]

 accuracies = []

 for i in range(n_iterations):
 if i % 10 == 0:
logger.info(f"Iteration {i + 1}/{n_iterations}")

# Random separation with preservation of temporary order
 split_idx = int(len(data) * (1 - test_size))
# Adding a random shift within 10% of the data
 max_shift = int(len(data) * 0.1)
 shift = np.random.randint(-max_shift, max_shift)
 split_idx = max(int(len(data) * 0.5), min(int(len(data) * 0.9), split_idx + shift))

 train_data = data.iloc[:split_idx]
 test_data = data.iloc[split_idx:]

if len(test_data) < 10: # Minimum test sample size
 continue

# Rapid Model Learning
 model_path = f"models/mc_{task}_iter_{i}_{datetime.now().strftime('%H%M%S')}"

 try:
 predictor = TabularPredictor(
 label=target_col,
 problem_type=config['problem_type'],
 eval_metric=config['eval_metric'],
 path=model_path
 )

 mc_fit_args = {
'time_limit': 300, # 5 minutes on iteration
 'presets': 'medium_quality_faster_train',
 'excluded_model_types': [
'NN_TORCH', 'NN_FASTAI', 'FASTAI', 'NeuralNetFastAI' # GPU models only
 ],
 'verbosity': 0,
 'ag_args_fit': {
 'Use_gpu': False,
 'num_gpus': 0
 },
# Special settings for XGBoost and LightGBM
 'hyperparameters': {
 'XGB': {
 'n_jobs': 1,
 'n_estimators': 30,
 'max_depth': 3,
 'learning_rate': 0.1
 },
 'GBM': {
 'n_jobs': 1,
 'n_estimators': 30,
 'max_depth': 3,
 'learning_rate': 0.1,
 'verbose': -1
 }
 }
 }

# If ray is not available, Use sequential training
 if not RAY_available:
 mc_fit_args['num_bag_folds'] = 0
 mc_fit_args['num_stack_levels'] = 0

# Suppress AutoGluon output
 devnull = suppress_autogluon_output()
 try:
 predictor.fit(train_data, **mc_fit_args)
 finally:
 restore_output(devnull)

 Predictions = predictor.predict(test_data)
 actual = test_data[target_col]
 accuracy = accuracy_score(actual, Predictions)
 accuracies.append(accuracy)

 except Exception as e:
logger.warning(f"Error in iteration {i}: {e}")
 continue

 if not accuracies:
raise ValueError("failed to perform any successful iteration")

Statistics Clerks
 mc_results = {
 'task': task,
 'n_iterations': len(accuracies),
 'accuracies': accuracies,
 'mean_accuracy': np.mean(accuracies),
 'std_accuracy': np.std(accuracies),
 'min_accuracy': np.min(accuracies),
 'max_accuracy': np.max(accuracies),
 'percentile_5': np.percentile(accuracies, 5),
 'percentile_95': np.percentile(accuracies, 95),
'stability_score': 1 - (np.std(accuracies) /np.mean (accuracies)) # The closer to 1, the more stable
 }

# Monte Carlo validation completed
logger.info(f"📊Average accuracy: {mc_results['mean_accuracy']:.4f} ± {mc_results['std_accuracy']:.4f}")
logger.info(f"📊Stability: {mc_results['stability_score']:.4f}")

 return mc_results

 def run_complete_Analysis(self, symbol: str = "BTCUSD", Timeframe: str = "MN1") -> Dict[str, Any]:
 """
Launch full Analysis for all three tasks.

 Args:
 symbol: Trading symbol
 Timeframe: Timeframe

 Returns:
Complete Analysis Results
 """
console.print(f"🚀Launch a full analysis for {symbol} {Timeframe}", style="bold blue")

# Creating a progress bar
 with Progress(
 SpinnerColumn(),
 TextColumn("[progress.description]{task.description}"),
 BarColumn(),
 MofNCompleteColumn(),
 TimeElapsedColumn(),
 TimeRemainingColumn(),
 console=console
 ) as progress:

 # 1. Loading data
 task1 = progress.add_task("📁 Loading data...", total=1)
 raw_data = self.load_schr_data(symbol, Timeframe)
 progress.update(task1, COMPLETED=1)

# 2. create target variables and features
task2 = progress.add_task("🔧create attributes...", total=2)
 data_with_targets = self.create_target_variables(raw_data)
 progress.update(task2, advance=1)
 final_data = self.create_features(data_with_targets)
 progress.update(task2, COMPLETED=2)

console.print(f"📊Final dataset: {len(final_data)} records, {len(final_data.columns)} attributes", style="green")

 complete_results = {
 'symbol': symbol,
 'Timeframe': Timeframe,
 'data_info': {
 'total_records': len(final_data),
 'features_count': len(final_data.columns),
 'date_range': (final_data.index.min(), final_data.index.max()) if isinstance(final_data.index, pd.DatetimeIndex) else None
 },
 'models': {},
 'validations': {}
 }

# 3. Training models for all tasks
 tasks = List(self.task_configs.keys())
task_progress = progress.add_task("🤖Training models...", total=len(tasks))

 for i, task in enumerate(tasks):
# Create a separate progress bar for each task
 task_name = task.replace('_', ' ').title()
 task_progress_Detailed = progress.add_task(
f"🎯Processing task: {task_name}",
 total=3
 )

 try:
# Basic Model Training
progress.update(task_progress_detailed, description=f"🤖Training model {task_name}...")
 model_results = self.train_model(final_data, task, progress=progress, task_id=task_progress_Detailed)
 complete_results['models'][task] = model_results
 progress.update(task_progress_Detailed, advance=1)

# Walk Forward validation
progress.update(task_progress_detailed, description=f"🔄walk forward validation {task_name}...")
 wf_results = self.walk_forward_validation(final_data, task, n_splits=3)
 complete_results['validations'][f'{task}_walk_forward'] = wf_results
 progress.update(task_progress_Detailed, advance=1)

# Monte Carlo validation
progress.update(task_progress_detailed, description=f"🎲Monte Carlo validation {task_name}...")
 mc_results = self.monte_carlo_validation(final_data, task, n_iterations=20)
 complete_results['validations'][f'{task}_monte_carlo'] = mc_results
 progress.update(task_progress_Detailed, COMPLETED=3)

 progress.update(task_progress, advance=1)

 except Exception as e:
console.print(f"❌Error processing task {task}: {e}", style="red")
 complete_results['models'][task] = {'error': str(e)}
 progress.update(task_progress, advance=1)

# 4. Summary Score
 self._generate_summary_Report(complete_results)

logger.info("🎉Full analysis completed!")
 return complete_results

 def _generate_summary_Report(self, results: Dict[str, Any]):
"""Generation of a consolidated Report."""
 logger.info("\n" + "="*80)
logger.info("📋SUMMARY Report on SCHR LEVELS MODELS")
 logger.info("="*80)

 for task, model_results in results['models'].items():
 if 'error' in model_results:
logger.info(f"❌{task}: ERROR - {model_results['error']}")
 continue

 metrics = model_results['metrics']
logger.info(f"\n🎯 TASK: {task}")
logger.info(f"📊Accuracy: {metrics['accuracy']:.4f}")
 logger.info(f" 📊 Precision: {metrics['precision']:.4f}")
 logger.info(f" 📊 Recall: {metrics['recall']:.4f}")
 logger.info(f" 📊 F1-score: {metrics['f1']:.4f}")

# Walk Forward results
 wf_key = f'{task}_walk_forward'
 if wf_key in results['validations']:
 wf = results['validations'][wf_key]
 logger.info(f" 🔄 Walk Forward: {wf['mean_accuracy']:.4f} ± {wf['std_accuracy']:.4f}")

# Monte Carlo results
 mc_key = f'{task}_monte_carlo'
 if mc_key in results['validations']:
 mc = results['validations'][mc_key]
 logger.info(f" 🎲 Monte Carlo: {mc['mean_accuracy']:.4f} ± {mc['std_accuracy']:.4f}")
logger.info(f"🎲Stability: {mc['stability_score']:.4f}")

 logger.info("\n" + "="*80)

 def predict(self, data: pd.dataFrame, task: str) -> pd.Series:
 """
Simple predictions for testing

 Args:
data: data for predictions
Task title

 Returns:
of prediction,
 """
 try:
# Loading a trained model
 model_path = f"models/schr_levels_{task}_{self.timestamp}"
 predictor = TabularPredictor.load(model_path)

of prediction,
 Predictions = predictor.predict(data)
 return Predictions

 except Exception as e:
logger.error(f"Prediction error: {e}")
 raise

 def predict_for_trading(self, new_data: pd.dataFrame, task: str) -> Dict[str, Any]:
 """
Predictions for real trading.

 Args:
new_data: New data for predictions
task: Prediction task

 Returns:
Predictions with probabilities
 """
 if task not in self.models:
raise ValueError(f"Model for {task} not trained")

 predictor = self.models[task]

# Create attributes for new data (without target variables)
 features_data = self.create_features(new_data)

# Checking that data is not empty
 if len(features_data) == 0:
raise ValueError("No data for prediction after feature creation")

# Delete target variables if any
 target_cols = [col for col in features_data.columns if col.startswith('target_')]
 features_data = features_data.drop(columns=target_cols, errors='ignore')

of prediction,
 Predictions = predictor.predict(features_data)
 probabilities = predictor.predict_proba(features_data) if predictor.can_predict_proba else None

 return {
 'Predictions': Predictions,
 'probabilities': probabilities,
 'confidence': probabilities.max(axis=1) if probabilities is not None else None
 }

 def save_models(self, save_path: str = "models/schr_levels_production/"):
"""Saving trained models for production."""
 save_path = Path(save_path)
 save_path.mkdir(parents=True, exist_ok=True)

 for task, predictor in self.models.items():
 model_file = save_path / f"{task}_model.pkl"
 joblib.dump(predictor, model_file)
logger.info(f"💾Model {task} saved: {model_file}")

# Save the results
 results_file = save_path / "Analysis_results.pkl"
 joblib.dump(self.results, results_file)
logger.info(f"Analysis💾 results saved: {results_file}")

 def load_models(self, load_path: str = "models/schr_levels_production/"):
"""Loading saved models."""
 load_path = Path(load_path)

 for task in self.task_configs.keys():
 model_file = load_path / f"{task}_model.pkl"
 if model_file.exists():
 self.models[task] = joblib.load(model_file)
logger.info(f"📂Model {task} loaded: {model_file}")

# Loading results
 results_file = load_path / "Analysis_results.pkl"
 if results_file.exists():
 self.results = joblib.load(results_file)
logger.info(f"Analysis📂 results uploaded: {results_file}")




def parse_arguments():
"""Parsing command line arguments."""
 parser = argparse.ArgumentParser(
 description="SCHR Levels AutoML Pipeline - Comprehensive solution for creating ML models",
 formatter_class=argparse.RawDescriptionHelpFormatter,
 epilog="""
examples of use:
python schr-levels-gluon.py # Analysis on Default (BTCUSD MN1)
python schr-levels-gluon.py -f data/GBPUSD.parquet # Analyze a specific file
python schr-levels-gluon.py -s EURUSD -t W1 # EURUSD weekly data analysis
python schr-levels-gluon.py --symbol GBPUSD --Timeframe D1 # GBPUSD daily data analysis
 """
 )

 parser.add_argument(
 '-f', '--file',
 type=str,
help='Path to a specific data file for Analysis'
 )

 parser.add_argument(
 '-s', '--symbol',
 type=str,
 default='BTCUSD',
help='Trading symbol (on default: BTCUSD)'
 )

 parser.add_argument(
 '-t', '--Timeframe',
 type=str,
 default='MN1',
help='Timeframe (on default: MN1)'
 )

 parser.add_argument(
 '--data-path',
 type=str,
 default='data/cache/csv_converted/',
help='Path to folder with data (on default: data/cache/csv_converted/)'
 )

 parser.add_argument(
 '--models-path',
 type=str,
 default='models',
help='Path to folder for saving models (on default: models)'
 )

 return parser.parse_args()


def main():
"""The main function with support for CLI arguments."""
 args = parse_arguments()

 try:
# Create a pipeline with the transmitted parameters
 pipeline = SCHRLevelsAutoMLPipeline(
 data_path=args.data_path,
 data_file=args.file
 )

# LaunchWe analyze
 if args.file:
console.print(f"🚀Launch file analysis: {args.file}", style="bold blue")
 results = pipeline.run_complete_Analysis("CUSTOM", "CUSTOM")
 else:
console.print(f"🚀Launch an analysis for {args.symbol} {args.Timeframe}", style="bold blue")
 results = pipeline.run_complete_Analysis(args.symbol, args.Timeframe)

# Save the results
 pipeline.save_models()

# example predictions (Loading new data)
console.print("🔮Testing predictions...", style="blue")
 if args.file:
 new_data = pipeline.load_schr_data().tail(10)
 else:
 new_data = pipeline.load_schr_data(args.symbol, args.Timeframe).tail(10)

# Creating features for new data
 new_data = pipeline.create_features(new_data)

# Predictions for all tasks
 for task in pipeline.task_configs.keys():
 if task in pipeline.models:
 try:
 Prediction_results = pipeline.predict_for_trading(new_data, task)
 console.print(f"🔮 Prediction for {task}: {Prediction_results['Predictions']}", style="green")
 if Prediction_results['probabilities'] is not None:
console.print(f"🔮Probabilities: {Prediction_results['probabilities'].values}", style="cyan")
 except Exception as e:
console.print(f"Prediction❌ error for {task}: {e}", style="red")

console.print("✅Analysis completed successfully!", style="bold green")

 except Exception as e:
console.print(f"❌Error in main process: {e}", style="bold red")
 raise


if __name__ == "__main__":
 main()
