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
 raise FileNotfoundError(f"data file not found: {file_path}")
 console.print(f"📁 Loading data: {file_path.name}", style="blue")
 else:
 # Use standard path
 filename = f"CSVExport_{symbol}_PERIOD_{Timeframe}.parquet"
 file_path = self.data_path / filename
 if not file_path.exists():
 raise FileNotfoundError(f"File not found: {file_path}")
 console.print(f"📁 Loading data: {filename}", style="blue")

 df = pd.read_parquet(file_path)

 # checking presence of required columns
 required_cols = ['Close', 'High', 'Open', 'Low', 'Volume', 'predicted_low', 'predicted_high', 'pressure', 'pressure_vector']
 missing_cols = [col for col in required_cols if col not in df.columns]

 if missing_cols:
 logger.warning(f"Отсутствуют колонки: {missing_cols}")

 # Устанавливаем индекс как datetime если есть
 if 'Date' in df.columns:
 df['Date'] = pd.to_datetime(df['Date'])
 df.set_index('Date', inplace=True)
 elif df.index.name != 'Date' and not isinstance(df.index, pd.DatetimeIndex):
 # Создаем временной индекс если его нет
 df.index = pd.date_range(start='2020-01-01', periods=len(df), freq='MS' if Timeframe == 'MN1' else 'D')

 console.print(f"📊 Загружено {len(df)} записей with {len(df.columns)} колонками", style="green")
 return df

 def create_target_variables(self, df: pd.dataFrame) -> pd.dataFrame:
 """
 create целевых переменных for всех 3 задач.

 Args:
 df: Исходные data SCHR Levels

 Returns:
 dataFrame with добавленными целевыми переменными
 """
 logger.info("Создаем целевые переменные for 3 задач...")

 data = df.copy()

 # Задача 1: Знак PRESSURE_VECTOR in следующем периоде
 if 'pressure_vector' in data.columns:
 # Обрабатываем NaN and inf значения
 pv_clean = data['pressure_vector'].replace([np.inf, -np.inf], np.nan)
 pv_sign = (pv_clean.shift(-1) > 0)
 data['target_pv_sign'] = pv_sign.astype(float) # Use float for совместимости
 logger.info("✅ Создана target_pv_sign (0=отрицательный, 1=положительный)")

 # Задача 2: Направление цены on 1 период
 if 'Close' in data.columns:
 future_returns = data['Close'].pct_change(1).shift(-1)
 # Обрабатываем NaN значения
 future_returns_clean = future_returns.replace([np.inf, -np.inf], np.nan)
 price_direction = pd.cut(
 future_returns_clean,
 bins=[-np.inf, -0.01, 0.01, np.inf],
 labels=[0, 1, 2] # 0=down, 1=hold, 2=up
 )
 data['target_price_direction'] = price_direction.astype(float) # Use float for совместимости
 logger.info("✅ Создана target_price_direction (0=вниз, 1=удержание, 2=вверх) on 1 период")

 # Задача 3: Пробитие уровней or удержание between them
 if all(col in data.columns for col in ['Close', 'predicted_high', 'predicted_low']):
 close_next = data['Close'].shift(-1)
 pred_high = data['predicted_high'].replace([np.inf, -np.inf], np.nan)
 pred_low = data['predicted_low'].replace([np.inf, -np.inf], np.nan)

 # Обрабатываем случаи with NaN in уровнях
 valid_levels = ~(pred_high.isna() | pred_low.isna() | close_next.isna())

 conditions = [
 (close_next > pred_high) & valid_levels, # Пробитие вверх
 (close_next < pred_low) & valid_levels, # Пробитие вниз
 (close_next >= pred_low) & (close_next <= pred_high) & valid_levels # Между уровнями
 ]
 choices = [2, 0, 1] # 2=пробитие вверх, 0=пробитие вниз, 1=между уровнями

 data['target_level_breakout'] = np.select(conditions, choices, default=1).astype(float)
 logger.info("✅ Создана target_level_breakout (0=пробитие вниз, 1=между уровнями, 2=пробитие вверх)")

 # Удаляем строки with NaN in целевых переменных
 target_cols = [col for col in data.columns if col.startswith('target_')]
 data = data.dropna(subset=target_cols)

 logger.info(f"После создания целевых переменных: {len(data)} записей")
 return data

 def create_features(self, df: pd.dataFrame) -> pd.dataFrame:
 """
 create дополнительных признаков for улучшения качества модели.

 Args:
 df: data with целевыми переменными

 Returns:
 dataFrame with дополнительными приsignми
 """
 logger.info("Создаем дополнительные признаки...")

 data = df.copy()

 # Технические индикаторы on basis цены
 if 'Close' in data.columns:
 # Скользящие средние
 for window in [5, 10, 20]:
 data[f'sma_{window}'] = data['Close'].rolling(window).mean()
 data[f'close_sma_{window}_ratio'] = data['Close'] / data[f'sma_{window}']

 # Волатильность
 data['volatility_5'] = data['Close'].pct_change().rolling(5).std()
 data['volatility_20'] = data['Close'].pct_change().rolling(20).std()

 # RSI упрощенный
 delta = data['Close'].diff()
 gain = (delta.where(delta > 0, 0)).rolling(14).mean()
 loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
 rs = gain / loss
 data['rsi'] = 100 - (100 / (1 + rs))

 # Признаки on basis SCHR уровней
 if all(col in data.columns for col in ['Close', 'predicted_high', 'predicted_low']):
 # Расстояние to уровней
 data['distance_to_high'] = (data['predicted_high'] - data['Close']) / data['Close']
 data['distance_to_low'] = (data['Close'] - data['predicted_low']) / data['Close']
 data['levels_spread'] = (data['predicted_high'] - data['predicted_low']) / data['Close']

 # Позиция относительно уровней (0-1, где 0.5 = in середине)
 data['position_in_levels'] = (data['Close'] - data['predicted_low']) / (data['predicted_high'] - data['predicted_low'])

 # Признаки on basis давления
 if 'pressure' in data.columns:
 # Лаги давления
 for lag in [1, 2, 3]:
 data[f'pressure_lag_{lag}'] = data['pressure'].shift(lag)

 # Скользящие средние давления
 for window in [3, 5, 10]:
 data[f'pressure_sma_{window}'] = data['pressure'].rolling(window).mean()

 if 'pressure_vector' in data.columns:
 # Лаги вектора давления
 for lag in [1, 2, 3]:
 data[f'pv_lag_{lag}'] = data['pressure_vector'].shift(lag)

 # Изменение sign вектора давления
 data['pv_sign_change'] = (data['pressure_vector'] * data['pressure_vector'].shift(1) < 0).astype(int)

 # Временные признаки если есть datetime индекс
 if isinstance(data.index, pd.DatetimeIndex):
 data['month'] = data.index.month
 data['quarter'] = data.index.quarter
 data['year'] = data.index.year

 # Удаляем строки with NaN
 # Обрабатываем бесконечные значения
 data = data.replace([np.inf, -np.inf], np.nan)

 # Заполняем NaN значения вместо удаления
 # for числовых columns заполняем медианой
 numeric_cols = data.select_dtypes(include=[np.number]).columns
 for col in numeric_cols:
 if data[col].isna().any():
 data[col] = data[col].fillna(data[col].median())

 # Удаляем только строки где все значения NaN
 data = data.dropna(how='all')

 # Если все еще есть NaN, заполняем 0
 data = data.fillna(0)

 # checking on оставшиеся бесконечные значения
 if np.isinf(data.select_dtypes(include=[np.number])).any().any():
 logger.warning("Обнаружены бесконечные значения, заменяем on 0")
 data = data.replace([np.inf, -np.inf], 0)

 logger.info(f"Создано {len(data.columns)} признаков, {len(data)} записей")
 return data

 def prepare_data_for_task(self, df: pd.dataFrame, task: str) -> Tuple[pd.dataFrame, str]:
 """
 Подготовка данных for конкретной задачи.

 Args:
 df: data with приsignми and целевыми переменными
 task: Название задачи

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
 raise ValueError(f"Целевая переменная {target_col} not foundа")

 # Удаляем другие целевые переменные
 other_targets = [col for col in target_mapping.values() if col != target_col]
 data = df.drop(columns=other_targets, errors='ignore')

 # Удаляем строки где целевая переменная NaN
 data = data.dropna(subset=[target_col])

 logger.info(f"Подготовлены data for задачи {task}: {len(data)} записей")
 return data, target_col

 def train_model(self, df: pd.dataFrame, task: str, test_size: float = 0.2, progress=None, task_id=None) -> Dict[str, Any]:
 """
 Обучение модели AutoGluon for конкретной задачи.

 Args:
 df: Подготовленные data
 task: Название задачи
 test_size: Доля тестовых данных

 Returns:
 Словарь with результатами обучения
 """
 # Обучение модели for задачи: {task}
 task_name = task.replace('_', ' ').title()

 data, target_col = self.prepare_data_for_task(df, task)
 config = self.task_configs[task]

 # Временное разделение данных (важно for временных рядов)
 split_idx = int(len(data) * (1 - test_size))
 train_data = data.iloc[:split_idx]
 test_data = data.iloc[split_idx:]

 # Обучающая выборка: {len(train_data)} записей
 # Тестовая выборка: {len(test_data)} записей

 # Создаем уникальный путь for модели
 model_path = f"models/schr_levels_{task}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

 # Обучение модели AutoGluon
 predictor = TabularPredictor(
 label=target_col,
 problem_type=config['problem_type'],
 eval_metric=config['eval_metric'],
 path=model_path
 )

 # settings for MacBook M1 (отключаем только GPU модели)
 fit_args = {
 'time_limit': config['time_limit'],
 'presets': 'best_quality',
 'excluded_model_types': [
 'NN_TORCH', 'NN_FASTAI', 'FASTAI', 'NeuralNetFastAI' # Только GPU модели
 ],
 'num_bag_folds': 5,
 'num_stack_levels': 1,
 'verbosity': 0,
 'ag_args_fit': {
 'Use_gpu': False,
 'num_gpus': 0
 },
 # Специальные settings for XGBoost and LightGBM
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

 # Если ray not available, Use sequential training
 if not RAY_available:
 logger.warning("Ray not available - Use sequential training")
 fit_args['num_bag_folds'] = 0 # Отключаем bagging for последовательного обучения
 fit_args['num_stack_levels'] = 0 # Отключаем stacking

 # Подавляем вывод AutoGluon
 devnull = suppress_autogluon_output()
 try:
 # Обновляем progress bar после инициализации Ray
 if progress and task_id:
 progress.update(task_id, description=f"🚀 Инициализация Ray and обучение {task_name}...")

 # Дополнительно перенаправляем stdout/stderr for подавления preset сообщений
 old_stdout = sys.stdout
 old_stderr = sys.stderr
 sys.stdout = devnull
 sys.stderr = devnull

 predictor.fit(train_data, **fit_args)

 # Восстанавливаем stdout/stderr
 sys.stdout = old_stdout
 sys.stderr = old_stderr

 # Обновляем progress bar после завершения обучения
 if progress and task_id:
 progress.update(task_id, description=f"✅ Обучение {task_name} COMPLETED")

 finally:
 restore_output(devnull)

 # Предсказания on тестовых данных
 Predictions = predictor.predict(test_data)
 probabilities = predictor.predict_proba(test_data) if predictor.can_predict_proba else None

 # Оценка качества
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

 # Сохраняем модель and результаты
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

 logger.info(f"✅ Модель for задачи {task} обучена успешно")
 logger.info(f"📊 Точность: {metrics['accuracy']:.4f}")

 return results

 def walk_forward_validation(self, df: pd.dataFrame, task: str, n_splits: int = 5) -> Dict[str, Any]:
 """
 Walk Forward валидация for проверки робастности модели.

 Args:
 df: data for валидации
 task: Название задачи
 n_splits: Количество разделений

 Returns:
 Результаты валидации
 """
 # Walk Forward валидация (без дополнительных сообщений)

 data, target_col = self.prepare_data_for_task(df, task)
 config = self.task_configs[task]

 tscv = TimeSeriesSplit(n_splits=n_splits)
 fold_results = []

 for fold, (train_idx, test_idx) in enumerate(tscv.split(data)):
 logger.info(f"Обрабатываем fold {fold + 1}/{n_splits}")

 train_data = data.iloc[train_idx]
 test_data = data.iloc[test_idx]

 # Обучаем модель on fold
 model_path = f"models/wf_{task}_fold_{fold}_{datetime.now().strftime('%H%M%S')}"

 predictor = TabularPredictor(
 label=target_col,
 problem_type=config['problem_type'],
 eval_metric=config['eval_metric'],
 path=model_path
 )

 # Быстрое обучение for валидации (только без GPU)
 wf_fit_args = {
 'time_limit': 600, # 10 minutes on fold
 'presets': 'medium_quality_faster_train',
 'excluded_model_types': [
 'NN_TORCH', 'NN_FASTAI', 'FASTAI', 'NeuralNetFastAI' # Только GPU модели
 ],
 'verbosity': 0,
 'ag_args_fit': {
 'Use_gpu': False,
 'num_gpus': 0
 },
 # Специальные settings for XGBoost and LightGBM
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

 # Если ray not available, Use sequential training
 if not RAY_available:
 wf_fit_args['num_bag_folds'] = 0
 wf_fit_args['num_stack_levels'] = 0

 # Подавляем вывод AutoGluon
 devnull = suppress_autogluon_output()
 try:
 predictor.fit(train_data, **wf_fit_args)
 finally:
 restore_output(devnull)

 # Предсказания
 Predictions = predictor.predict(test_data)
 actual = test_data[target_col]

 # Метрики for fold
 accuracy = accuracy_score(actual, Predictions)
 fold_results.append({
 'fold': fold,
 'accuracy': accuracy,
 'train_size': len(train_data),
 'test_size': len(test_data)
 })

 logger.info(f"Fold {fold + 1} accuracy: {accuracy:.4f}")

 # Агрегированные результаты
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

 # Walk Forward валидация завершена
 logger.info(f"📊 Средняя точность: {wf_results['mean_accuracy']:.4f} ± {wf_results['std_accuracy']:.4f}")

 return wf_results

 def monte_carlo_validation(self, df: pd.dataFrame, task: str, n_iterations: int = 100, test_size: float = 0.2) -> Dict[str, Any]:
 """
 Monte Carlo валидация for оценки стабильности модели.

 Args:
 df: data for валидации
 task: Название задачи
 n_iterations: Количество итераций
 test_size: Доля тестовых данных

 Returns:
 Результаты Monte Carlo валидации
 """
 # Monte Carlo валидация (без дополнительных сообщений)

 data, target_col = self.prepare_data_for_task(df, task)
 config = self.task_configs[task]

 accuracies = []

 for i in range(n_iterations):
 if i % 10 == 0:
 logger.info(f"Итерация {i + 1}/{n_iterations}")

 # Случайное разделение with сохранением временного порядка
 split_idx = int(len(data) * (1 - test_size))
 # Добавляем случайный сдвиг in пределах 10% данных
 max_shift = int(len(data) * 0.1)
 shift = np.random.randint(-max_shift, max_shift)
 split_idx = max(int(len(data) * 0.5), min(int(len(data) * 0.9), split_idx + shift))

 train_data = data.iloc[:split_idx]
 test_data = data.iloc[split_idx:]

 if len(test_data) < 10: # Минимальный размер тестовой выборки
 continue

 # Быстрое обучение модели
 model_path = f"models/mc_{task}_iter_{i}_{datetime.now().strftime('%H%M%S')}"

 try:
 predictor = TabularPredictor(
 label=target_col,
 problem_type=config['problem_type'],
 eval_metric=config['eval_metric'],
 path=model_path
 )

 mc_fit_args = {
 'time_limit': 300, # 5 minutes on итерацию
 'presets': 'medium_quality_faster_train',
 'excluded_model_types': [
 'NN_TORCH', 'NN_FASTAI', 'FASTAI', 'NeuralNetFastAI' # Только GPU модели
 ],
 'verbosity': 0,
 'ag_args_fit': {
 'Use_gpu': False,
 'num_gpus': 0
 },
 # Специальные settings for XGBoost and LightGBM
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

 # Если ray not available, Use sequential training
 if not RAY_available:
 mc_fit_args['num_bag_folds'] = 0
 mc_fit_args['num_stack_levels'] = 0

 # Подавляем вывод AutoGluon
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
 logger.warning(f"Ошибка in итерации {i}: {e}")
 continue

 if not accuracies:
 raise ValueError("not удалось выполнить ни одной успешной итерации")

 # Статистики
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
 'stability_score': 1 - (np.std(accuracies) / np.mean(accuracies)) # Чем ближе к 1, тем стабильнее
 }

 # Monte Carlo валидация завершена
 logger.info(f"📊 Средняя точность: {mc_results['mean_accuracy']:.4f} ± {mc_results['std_accuracy']:.4f}")
 logger.info(f"📊 Стабильность: {mc_results['stability_score']:.4f}")

 return mc_results

 def run_complete_Analysis(self, symbol: str = "BTCUSD", Timeframe: str = "MN1") -> Dict[str, Any]:
 """
 Launch полного Analysis for всех трех задач.

 Args:
 symbol: Trading symbol
 Timeframe: Timeframe

 Returns:
 Полные результаты Analysis
 """
 console.print(f"🚀 Launchаем полный анализ for {symbol} {Timeframe}", style="bold blue")

 # Создаем progress bar
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

 # 2. create целевых переменных and признаков
 task2 = progress.add_task("🔧 create признаков...", total=2)
 data_with_targets = self.create_target_variables(raw_data)
 progress.update(task2, advance=1)
 final_data = self.create_features(data_with_targets)
 progress.update(task2, COMPLETED=2)

 console.print(f"📊 Итоговый датасет: {len(final_data)} записей, {len(final_data.columns)} признаков", style="green")

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

 # 3. Обучение моделей for всех задач
 tasks = List(self.task_configs.keys())
 task_progress = progress.add_task("🤖 Обучение моделей...", total=len(tasks))

 for i, task in enumerate(tasks):
 # Создаем отдельный progress bar for каждой задачи
 task_name = task.replace('_', ' ').title()
 task_progress_Detailed = progress.add_task(
 f"🎯 Обрабатываем задачу: {task_name}",
 total=3
 )

 try:
 # Обучение основной модели
 progress.update(task_progress_Detailed, description=f"🤖 Обучение модели {task_name}...")
 model_results = self.train_model(final_data, task, progress=progress, task_id=task_progress_Detailed)
 complete_results['models'][task] = model_results
 progress.update(task_progress_Detailed, advance=1)

 # Walk Forward валидация
 progress.update(task_progress_Detailed, description=f"🔄 Walk Forward валидация {task_name}...")
 wf_results = self.walk_forward_validation(final_data, task, n_splits=3)
 complete_results['validations'][f'{task}_walk_forward'] = wf_results
 progress.update(task_progress_Detailed, advance=1)

 # Monte Carlo валидация
 progress.update(task_progress_Detailed, description=f"🎲 Monte Carlo валидация {task_name}...")
 mc_results = self.monte_carlo_validation(final_data, task, n_iterations=20)
 complete_results['validations'][f'{task}_monte_carlo'] = mc_results
 progress.update(task_progress_Detailed, COMPLETED=3)

 progress.update(task_progress, advance=1)

 except Exception as e:
 console.print(f"❌ Ошибка при обработке задачи {task}: {e}", style="red")
 complete_results['models'][task] = {'error': str(e)}
 progress.update(task_progress, advance=1)

 # 4. Сводная оценка
 self._generate_summary_Report(complete_results)

 logger.info("🎉 Полный анализ завершен!")
 return complete_results

 def _generate_summary_Report(self, results: Dict[str, Any]):
 """Генерация сводного Reportа."""
 logger.info("\n" + "="*80)
 logger.info("📋 СВОДНЫЙ Report on МОДЕЛЯМ SCHR LEVELS")
 logger.info("="*80)

 for task, model_results in results['models'].items():
 if 'error' in model_results:
 logger.info(f"❌ {task}: ОШИБКА - {model_results['error']}")
 continue

 metrics = model_results['metrics']
 logger.info(f"\n🎯 ЗАДАЧА: {task}")
 logger.info(f" 📊 Точность: {metrics['accuracy']:.4f}")
 logger.info(f" 📊 Precision: {metrics['precision']:.4f}")
 logger.info(f" 📊 Recall: {metrics['recall']:.4f}")
 logger.info(f" 📊 F1-score: {metrics['f1']:.4f}")

 # Walk Forward результаты
 wf_key = f'{task}_walk_forward'
 if wf_key in results['validations']:
 wf = results['validations'][wf_key]
 logger.info(f" 🔄 Walk Forward: {wf['mean_accuracy']:.4f} ± {wf['std_accuracy']:.4f}")

 # Monte Carlo результаты
 mc_key = f'{task}_monte_carlo'
 if mc_key in results['validations']:
 mc = results['validations'][mc_key]
 logger.info(f" 🎲 Monte Carlo: {mc['mean_accuracy']:.4f} ± {mc['std_accuracy']:.4f}")
 logger.info(f" 🎲 Стабильность: {mc['stability_score']:.4f}")

 logger.info("\n" + "="*80)

 def predict(self, data: pd.dataFrame, task: str) -> pd.Series:
 """
 Простые предсказания for тестирования

 Args:
 data: data for предсказания
 task: Название задачи

 Returns:
 Предсказания
 """
 try:
 # Loading обученную модель
 model_path = f"models/schr_levels_{task}_{self.timestamp}"
 predictor = TabularPredictor.load(model_path)

 # Предсказания
 Predictions = predictor.predict(data)
 return Predictions

 except Exception as e:
 logger.error(f"Ошибка предсказания: {e}")
 raise

 def predict_for_trading(self, new_data: pd.dataFrame, task: str) -> Dict[str, Any]:
 """
 Предсказания for реальной торговли.

 Args:
 new_data: Новые data for предсказания
 task: Задача for предсказания

 Returns:
 Предсказания with вероятностями
 """
 if task not in self.models:
 raise ValueError(f"Модель for задачи {task} not обучена")

 predictor = self.models[task]

 # Создаем признаки for новых данных (без целевых переменных)
 features_data = self.create_features(new_data)

 # checking, что data not пустые
 if len(features_data) == 0:
 raise ValueError("Нет данных for предсказания после создания признаков")

 # Удаляем целевые переменные если они есть
 target_cols = [col for col in features_data.columns if col.startswith('target_')]
 features_data = features_data.drop(columns=target_cols, errors='ignore')

 # Предсказания
 Predictions = predictor.predict(features_data)
 probabilities = predictor.predict_proba(features_data) if predictor.can_predict_proba else None

 return {
 'Predictions': Predictions,
 'probabilities': probabilities,
 'confidence': probabilities.max(axis=1) if probabilities is not None else None
 }

 def save_models(self, save_path: str = "models/schr_levels_production/"):
 """Сохранение обученных моделей for продакшена."""
 save_path = Path(save_path)
 save_path.mkdir(parents=True, exist_ok=True)

 for task, predictor in self.models.items():
 model_file = save_path / f"{task}_model.pkl"
 joblib.dump(predictor, model_file)
 logger.info(f"💾 Модель {task} сохранена: {model_file}")

 # Сохраняем результаты
 results_file = save_path / "Analysis_results.pkl"
 joblib.dump(self.results, results_file)
 logger.info(f"💾 Результаты Analysis сохранены: {results_file}")

 def load_models(self, load_path: str = "models/schr_levels_production/"):
 """Загрузка сохраненных моделей."""
 load_path = Path(load_path)

 for task in self.task_configs.keys():
 model_file = load_path / f"{task}_model.pkl"
 if model_file.exists():
 self.models[task] = joblib.load(model_file)
 logger.info(f"📂 Модель {task} загружена: {model_file}")

 # Loading результаты
 results_file = load_path / "Analysis_results.pkl"
 if results_file.exists():
 self.results = joblib.load(results_file)
 logger.info(f"📂 Результаты Analysis загружены: {results_file}")




def parse_arguments():
 """Парсинг аргументов командной строки."""
 parser = argparse.ArgumentParser(
 description="SCHR Levels AutoML Pipeline - Comprehensive solution for creating ML models",
 formatter_class=argparse.RawDescriptionHelpFormatter,
 epilog="""
examples использования:
 python schr-levels-gluon.py # Анализ on умолчанию (BTCUSD MN1)
 python schr-levels-gluon.py -f data/GBPUSD.parquet # Анализ конкретного файла
 python schr-levels-gluon.py -s EURUSD -t W1 # Анализ EURUSD недельные data
 python schr-levels-gluon.py --symbol GBPUSD --Timeframe D1 # Анализ GBPUSD дневные data
 """
 )

 parser.add_argument(
 '-f', '--file',
 type=str,
 help='Путь к конкретному файлу данных for Analysis'
 )

 parser.add_argument(
 '-s', '--symbol',
 type=str,
 default='BTCUSD',
 help='Trading symbol (on умолчанию: BTCUSD)'
 )

 parser.add_argument(
 '-t', '--Timeframe',
 type=str,
 default='MN1',
 help='Timeframe (on умолчанию: MN1)'
 )

 parser.add_argument(
 '--data-path',
 type=str,
 default='data/cache/csv_converted/',
 help='Path to folder with data (on умолчанию: data/cache/csv_converted/)'
 )

 parser.add_argument(
 '--models-path',
 type=str,
 default='models',
 help='Path to folder for сохранения моделей (on умолчанию: models)'
 )

 return parser.parse_args()


def main():
 """Основная function with поддержкой CLI аргументов."""
 args = parse_arguments()

 try:
 # Создаем пайплайн with переданными параметрами
 pipeline = SCHRLevelsAutoMLPipeline(
 data_path=args.data_path,
 data_file=args.file
 )

 # Launchаем анализ
 if args.file:
 console.print(f"🚀 Launchаем анализ файла: {args.file}", style="bold blue")
 results = pipeline.run_complete_Analysis("CUSTOM", "CUSTOM")
 else:
 console.print(f"🚀 Launchаем анализ for {args.symbol} {args.Timeframe}", style="bold blue")
 results = pipeline.run_complete_Analysis(args.symbol, args.Timeframe)

 # Сохраняем результаты
 pipeline.save_models()

 # example предсказания (Loading новые data)
 console.print("🔮 Тестируем предсказания...", style="blue")
 if args.file:
 new_data = pipeline.load_schr_data().tail(10)
 else:
 new_data = pipeline.load_schr_data(args.symbol, args.Timeframe).tail(10)

 # Создаем признаки for новых данных
 new_data = pipeline.create_features(new_data)

 # Предсказания for всех задач
 for task in pipeline.task_configs.keys():
 if task in pipeline.models:
 try:
 Prediction_results = pipeline.predict_for_trading(new_data, task)
 console.print(f"🔮 Prediction for {task}: {Prediction_results['Predictions']}", style="green")
 if Prediction_results['probabilities'] is not None:
 console.print(f"🔮 Вероятности: {Prediction_results['probabilities'].values}", style="cyan")
 except Exception as e:
 console.print(f"❌ Ошибка предсказания for {task}: {e}", style="red")

 console.print("✅ Анализ завершен успешно!", style="bold green")

 except Exception as e:
 console.print(f"❌ Ошибка in основном процессе: {e}", style="bold red")
 raise


if __name__ == "__main__":
 main()
