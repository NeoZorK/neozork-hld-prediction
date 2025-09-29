# -*- coding: utf-8 -*-
"""
SCHR Levels AutoML Pipeline
Комплексное решение для создания ML-моделей на основе SCHR Levels индикаторов

Решает 3 основные задачи:
1. Предсказание знака PRESSURE_VECTOR (+ или -)
2. Предсказание направления цены на 5 периодов (вверх/вниз/hold)  
3. Предсказание пробития PREDICTED_HIGH/PREDICTED_LOW или удержания между ними

Автор: NeoZork HLDP
Версия: 1.0
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import logging
from pathlib import Path
import warnings
from datetime import datetime, timedelta
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import TimeSeriesSplit
import matplotlib.pyplot as plt
import seaborn as sns

# Disable CUDA for MacBook M1 and set OpenMP paths
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["AUTOGLUON_USE_GPU"] = "false"
os.environ["AUTOGLUON_USE_GPU_TORCH"] = "false"
os.environ["AUTOGLUON_USE_GPU_FASTAI"] = "false"

# Set OpenMP paths for macOS
os.environ["LDFLAGS"] = "-L/opt/homebrew/opt/libomp/lib"
os.environ["CPPFLAGS"] = "-I/opt/homebrew/opt/libomp/include"

# AutoGluon imports
try:
    from autogluon.tabular import TabularPredictor
    AUTOGLUON_AVAILABLE = True
except ImportError:
    AUTOGLUON_AVAILABLE = False
    TabularPredictor = None

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

# Ray import check
try:
    import ray
    RAY_AVAILABLE = True
    logger.info("Ray доступен - будет использоваться параллельное обучение")
except ImportError:
    RAY_AVAILABLE = False
    logger.warning("Ray не установлен - будет использоваться последовательное обучение")
    logger.info("Для установки ray выполните: pip install 'ray>=2.10.0,<2.45.0'")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/schr_levels_automl.log'),
        logging.StreamHandler()
    ]
)


class SCHRLevelsAutoMLPipeline:
    """
    Комплексный пайплайн для создания ML-моделей на основе SCHR Levels индикаторов.
    
    Решает 3 основные задачи:
    1. Предсказание знака PRESSURE_VECTOR (+ или -)
    2. Предсказание направления цены на 5 периодов (вверх/вниз/hold)  
    3. Предсказание пробития PREDICTED_HIGH/PREDICTED_LOW или удержания между ними
    """
    
    def __init__(self, data_path: str = "data/cache/csv_converted/"):
        """
        Инициализация пайплайна.
        
        Args:
            data_path: Путь к папке с данными
        """
        if not AUTOGLUON_AVAILABLE:
            raise ImportError("AutoGluon не установлен. Установите: pip install autogluon")
        
        self.data_path = Path(data_path)
        self.models = {}
        self.results = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Настройки для разных задач
        self.task_configs = {
            'pressure_vector_sign': {
                'problem_type': 'binary',
                'eval_metric': 'roc_auc',
                'time_limit': 1800  # 30 минут
            },
            'price_direction_1period': {
                'problem_type': 'multiclass', 
                'eval_metric': 'accuracy',
                'time_limit': 1800  # 30 минут
            },
            'level_breakout': {
                'problem_type': 'multiclass',
                'eval_metric': 'accuracy', 
                'time_limit': 2400  # 40 минут
            }
        }
        
        logger.info("SCHR Levels AutoML Pipeline инициализирован")
        
        # Информируем о режиме обучения
        if RAY_AVAILABLE:
            logger.info("✅ Ray доступен - будет использоваться параллельное обучение")
        else:
            logger.warning("⚠️  Ray недоступен - будет использоваться последовательное обучение")
            logger.info("💡 Для ускорения установите ray: pip install 'ray>=2.10.0,<2.45.0'")
    
    def load_schr_data(self, symbol: str = "BTCUSD", timeframe: str = "MN1") -> pd.DataFrame:
        """
        Загрузка данных SCHR Levels для указанного символа и таймфрейма.
        
        Args:
            symbol: Торговый символ (BTCUSD, EURUSD, etc.)
            timeframe: Таймфрейм (MN1, W1, D1, H4, H1, M15, M5, M1)
            
        Returns:
            DataFrame с данными SCHR Levels
        """
        filename = f"CSVExport_{symbol}_PERIOD_{timeframe}.parquet"
        file_path = self.data_path / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        
        logger.info(f"Загружаем данные: {filename}")
        df = pd.read_parquet(file_path)
        
        # Проверяем наличие необходимых колонок
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
            df.index = pd.date_range(start='2020-01-01', periods=len(df), freq='MS' if timeframe == 'MN1' else 'D')
        
        logger.info(f"Загружено {len(df)} записей с {len(df.columns)} колонками")
        return df
    
    def create_target_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Создание целевых переменных для всех 3 задач.
        
        Args:
            df: Исходные данные SCHR Levels
            
        Returns:
            DataFrame с добавленными целевыми переменными
        """
        logger.info("Создаем целевые переменные для 3 задач...")
        
        data = df.copy()
        
        # Задача 1: Знак PRESSURE_VECTOR в следующем периоде
        if 'pressure_vector' in data.columns:
            # Обрабатываем NaN и inf значения
            pv_clean = data['pressure_vector'].replace([np.inf, -np.inf], np.nan)
            pv_sign = (pv_clean.shift(-1) > 0)
            data['target_pv_sign'] = pv_sign.astype(float)  # Используем float для совместимости
            logger.info("✅ Создана target_pv_sign (0=отрицательный, 1=положительный)")
        
        # Задача 2: Направление цены на 1 период
        if 'Close' in data.columns:
            future_returns = data['Close'].pct_change(1).shift(-1)
            # Обрабатываем NaN значения
            future_returns_clean = future_returns.replace([np.inf, -np.inf], np.nan)
            price_direction = pd.cut(
                future_returns_clean, 
                bins=[-np.inf, -0.01, 0.01, np.inf], 
                labels=[0, 1, 2]  # 0=down, 1=hold, 2=up
            )
            data['target_price_direction'] = price_direction.astype(float)  # Используем float для совместимости
            logger.info("✅ Создана target_price_direction (0=вниз, 1=удержание, 2=вверх) на 1 период")
        
        # Задача 3: Пробитие уровней или удержание между ними
        if all(col in data.columns for col in ['Close', 'predicted_high', 'predicted_low']):
            close_next = data['Close'].shift(-1)
            pred_high = data['predicted_high'].replace([np.inf, -np.inf], np.nan)
            pred_low = data['predicted_low'].replace([np.inf, -np.inf], np.nan)
            
            # Обрабатываем случаи с NaN в уровнях
            valid_levels = ~(pred_high.isna() | pred_low.isna() | close_next.isna())
            
            conditions = [
                (close_next > pred_high) & valid_levels,  # Пробитие вверх
                (close_next < pred_low) & valid_levels,   # Пробитие вниз
                (close_next >= pred_low) & (close_next <= pred_high) & valid_levels  # Между уровнями
            ]
            choices = [2, 0, 1]  # 2=пробитие вверх, 0=пробитие вниз, 1=между уровнями
            
            data['target_level_breakout'] = np.select(conditions, choices, default=1).astype(float)
            logger.info("✅ Создана target_level_breakout (0=пробитие вниз, 1=между уровнями, 2=пробитие вверх)")
        
        # Удаляем строки с NaN в целевых переменных
        target_cols = [col for col in data.columns if col.startswith('target_')]
        data = data.dropna(subset=target_cols)
        
        logger.info(f"После создания целевых переменных: {len(data)} записей")
        return data
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Создание дополнительных признаков для улучшения качества модели.
        
        Args:
            df: Данные с целевыми переменными
            
        Returns:
            DataFrame с дополнительными признаками
        """
        logger.info("Создаем дополнительные признаки...")
        
        data = df.copy()
        
        # Технические индикаторы на основе цены
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
        
        # Признаки на основе SCHR уровней
        if all(col in data.columns for col in ['Close', 'predicted_high', 'predicted_low']):
            # Расстояние до уровней
            data['distance_to_high'] = (data['predicted_high'] - data['Close']) / data['Close']
            data['distance_to_low'] = (data['Close'] - data['predicted_low']) / data['Close']
            data['levels_spread'] = (data['predicted_high'] - data['predicted_low']) / data['Close']
            
            # Позиция относительно уровней (0-1, где 0.5 = в середине)
            data['position_in_levels'] = (data['Close'] - data['predicted_low']) / (data['predicted_high'] - data['predicted_low'])
        
        # Признаки на основе давления
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
            
            # Изменение знака вектора давления
            data['pv_sign_change'] = (data['pressure_vector'] * data['pressure_vector'].shift(1) < 0).astype(int)
        
        # Временные признаки если есть datetime индекс
        if isinstance(data.index, pd.DatetimeIndex):
            data['month'] = data.index.month
            data['quarter'] = data.index.quarter
            data['year'] = data.index.year
        
        # Удаляем строки с NaN
        # Обрабатываем бесконечные значения
        data = data.replace([np.inf, -np.inf], np.nan)
        
        # Заполняем NaN значения вместо удаления
        # Для числовых колонок заполняем медианой
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if data[col].isna().any():
                data[col] = data[col].fillna(data[col].median())
        
        # Удаляем только строки где все значения NaN
        data = data.dropna(how='all')
        
        # Если все еще есть NaN, заполняем 0
        data = data.fillna(0)
        
        # Проверяем на оставшиеся бесконечные значения
        if np.isinf(data.select_dtypes(include=[np.number])).any().any():
            logger.warning("Обнаружены бесконечные значения, заменяем на 0")
            data = data.replace([np.inf, -np.inf], 0)
        
        logger.info(f"Создано {len(data.columns)} признаков, {len(data)} записей")
        return data
    
    def prepare_data_for_task(self, df: pd.DataFrame, task: str) -> Tuple[pd.DataFrame, str]:
        """
        Подготовка данных для конкретной задачи.
        
        Args:
            df: Данные с признаками и целевыми переменными
            task: Название задачи
            
        Returns:
            Tuple[DataFrame, target_column]
        """
        target_mapping = {
            'pressure_vector_sign': 'target_pv_sign',
            'price_direction_1period': 'target_price_direction', 
            'level_breakout': 'target_level_breakout'
        }
        
        target_col = target_mapping[task]
        
        if target_col not in df.columns:
            raise ValueError(f"Целевая переменная {target_col} не найдена")
        
        # Удаляем другие целевые переменные
        other_targets = [col for col in target_mapping.values() if col != target_col]
        data = df.drop(columns=other_targets, errors='ignore')
        
        # Удаляем строки где целевая переменная NaN
        data = data.dropna(subset=[target_col])
        
        logger.info(f"Подготовлены данные для задачи {task}: {len(data)} записей")
        return data, target_col
    
    def train_model(self, df: pd.DataFrame, task: str, test_size: float = 0.2) -> Dict[str, Any]:
        """
        Обучение модели AutoGluon для конкретной задачи.
        
        Args:
            df: Подготовленные данные
            task: Название задачи
            test_size: Доля тестовых данных
            
        Returns:
            Словарь с результатами обучения
        """
        logger.info(f"Начинаем обучение модели для задачи: {task}")
        
        data, target_col = self.prepare_data_for_task(df, task)
        config = self.task_configs[task]
        
        # Временное разделение данных (важно для временных рядов)
        split_idx = int(len(data) * (1 - test_size))
        train_data = data.iloc[:split_idx]
        test_data = data.iloc[split_idx:]
        
        logger.info(f"Обучающая выборка: {len(train_data)} записей")
        logger.info(f"Тестовая выборка: {len(test_data)} записей")
        
        # Создаем уникальный путь для модели
        model_path = f"models/schr_levels_{task}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Обучение модели AutoGluon
        predictor = TabularPredictor(
            label=target_col,
            problem_type=config['problem_type'],
            eval_metric=config['eval_metric'],
            path=model_path
        )
        
        # Настройки для MacBook M1 (полностью отключаем GPU и проблемные модели)
        fit_args = {
            'time_limit': config['time_limit'],
            'presets': 'best_quality',
            'excluded_model_types': [
                'NN_TORCH', 'NN_FASTAI', 'FASTAI', 'NeuralNetFastAI',  # GPU модели
                'XGBoost', 'LightGBM',  # Модели с проблемами OpenMP на macOS
                'XGBoostLarge', 'LightGBMLarge'  # Большие версии
            ],
            'num_bag_folds': 5,
            'num_stack_levels': 1,
            'verbosity': 2,
            'ag_args_fit': {
                'use_gpu': False,
                'num_gpus': 0
            }
        }
        
        # Если ray недоступен, используем последовательное обучение
        if not RAY_AVAILABLE:
            logger.warning("Ray недоступен - используем последовательное обучение")
            fit_args['num_bag_folds'] = 0  # Отключаем bagging для последовательного обучения
            fit_args['num_stack_levels'] = 0  # Отключаем stacking
        
        logger.info("Запускаем обучение AutoGluon...")
        predictor.fit(train_data, **fit_args)
        
        # Предсказания на тестовых данных
        predictions = predictor.predict(test_data)
        probabilities = predictor.predict_proba(test_data) if predictor.can_predict_proba else None
        
        # Оценка качества
        actual = test_data[target_col]
        
        if config['problem_type'] == 'binary':
            metrics = {
                'accuracy': accuracy_score(actual, predictions),
                'precision': precision_score(actual, predictions, average='weighted', zero_division=0),
                'recall': recall_score(actual, predictions, average='weighted', zero_division=0),
                'f1': f1_score(actual, predictions, average='weighted', zero_division=0)
            }
        else:  # multiclass
            metrics = {
                'accuracy': accuracy_score(actual, predictions),
                'precision': precision_score(actual, predictions, average='weighted', zero_division=0),
                'recall': recall_score(actual, predictions, average='weighted', zero_division=0),
                'f1': f1_score(actual, predictions, average='weighted', zero_division=0)
            }
        
        # Сохраняем модель и результаты
        self.models[task] = predictor
        
        results = {
            'task': task,
            'model_path': model_path,
            'metrics': metrics,
            'predictions': predictions,
            'probabilities': probabilities,
            'actual': actual,
            'feature_importance': predictor.feature_importance(test_data),
            'leaderboard': predictor.leaderboard(test_data, silent=True)
        }
        
        self.results[task] = results
        
        logger.info(f"✅ Модель для задачи {task} обучена успешно")
        logger.info(f"📊 Точность: {metrics['accuracy']:.4f}")
        
        return results
    
    def walk_forward_validation(self, df: pd.DataFrame, task: str, n_splits: int = 5) -> Dict[str, Any]:
        """
        Walk Forward валидация для проверки робастности модели.
        
        Args:
            df: Данные для валидации
            task: Название задачи
            n_splits: Количество разделений
            
        Returns:
            Результаты валидации
        """
        logger.info(f"Запускаем Walk Forward валидацию для задачи {task}")
        
        data, target_col = self.prepare_data_for_task(df, task)
        config = self.task_configs[task]
        
        tscv = TimeSeriesSplit(n_splits=n_splits)
        fold_results = []
        
        for fold, (train_idx, test_idx) in enumerate(tscv.split(data)):
            logger.info(f"Обрабатываем fold {fold + 1}/{n_splits}")
            
            train_data = data.iloc[train_idx]
            test_data = data.iloc[test_idx]
            
            # Обучаем модель на fold
            model_path = f"models/wf_{task}_fold_{fold}_{datetime.now().strftime('%H%M%S')}"
            
            predictor = TabularPredictor(
                label=target_col,
                problem_type=config['problem_type'],
                eval_metric=config['eval_metric'],
                path=model_path
            )
            
            # Быстрое обучение для валидации (без GPU и проблемных моделей)
            wf_fit_args = {
                'time_limit': 600,  # 10 минут на fold
                'presets': 'medium_quality_faster_train',
                'excluded_model_types': [
                    'NN_TORCH', 'NN_FASTAI', 'FASTAI', 'NeuralNetFastAI',  # GPU модели
                    'XGBoost', 'LightGBM',  # Модели с проблемами OpenMP на macOS
                    'XGBoostLarge', 'LightGBMLarge'  # Большие версии
                ],
                'verbosity': 0,
                'ag_args_fit': {
                    'use_gpu': False,
                    'num_gpus': 0
                }
            }
            
            # Если ray недоступен, используем последовательное обучение
            if not RAY_AVAILABLE:
                wf_fit_args['num_bag_folds'] = 0
                wf_fit_args['num_stack_levels'] = 0
            
            predictor.fit(train_data, **wf_fit_args)
            
            # Предсказания
            predictions = predictor.predict(test_data)
            actual = test_data[target_col]
            
            # Метрики для fold
            accuracy = accuracy_score(actual, predictions)
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
        
        logger.info(f"✅ Walk Forward валидация завершена")
        logger.info(f"📊 Средняя точность: {wf_results['mean_accuracy']:.4f} ± {wf_results['std_accuracy']:.4f}")
        
        return wf_results
    
    def monte_carlo_validation(self, df: pd.DataFrame, task: str, n_iterations: int = 100, test_size: float = 0.2) -> Dict[str, Any]:
        """
        Monte Carlo валидация для оценки стабильности модели.
        
        Args:
            df: Данные для валидации
            task: Название задачи
            n_iterations: Количество итераций
            test_size: Доля тестовых данных
            
        Returns:
            Результаты Monte Carlo валидации
        """
        logger.info(f"Запускаем Monte Carlo валидацию для задачи {task} ({n_iterations} итераций)")
        
        data, target_col = self.prepare_data_for_task(df, task)
        config = self.task_configs[task]
        
        accuracies = []
        
        for i in range(n_iterations):
            if i % 10 == 0:
                logger.info(f"Итерация {i + 1}/{n_iterations}")
            
            # Случайное разделение с сохранением временного порядка
            split_idx = int(len(data) * (1 - test_size))
            # Добавляем случайный сдвиг в пределах 10% данных
            max_shift = int(len(data) * 0.1)
            shift = np.random.randint(-max_shift, max_shift)
            split_idx = max(int(len(data) * 0.5), min(int(len(data) * 0.9), split_idx + shift))
            
            train_data = data.iloc[:split_idx]
            test_data = data.iloc[split_idx:]
            
            if len(test_data) < 10:  # Минимальный размер тестовой выборки
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
                    'time_limit': 300,  # 5 минут на итерацию
                    'presets': 'medium_quality_faster_train',
                    'excluded_model_types': [
                        'NN_TORCH', 'NN_FASTAI', 'FASTAI', 'NeuralNetFastAI',  # GPU модели
                        'XGBoost', 'LightGBM',  # Модели с проблемами OpenMP на macOS
                        'XGBoostLarge', 'LightGBMLarge'  # Большие версии
                    ],
                    'verbosity': 0,
                    'ag_args_fit': {
                        'use_gpu': False,
                        'num_gpus': 0
                    }
                }
                
                # Если ray недоступен, используем последовательное обучение
                if not RAY_AVAILABLE:
                    mc_fit_args['num_bag_folds'] = 0
                    mc_fit_args['num_stack_levels'] = 0
                
                predictor.fit(train_data, **mc_fit_args)
                
                predictions = predictor.predict(test_data)
                actual = test_data[target_col]
                accuracy = accuracy_score(actual, predictions)
                accuracies.append(accuracy)
                
            except Exception as e:
                logger.warning(f"Ошибка в итерации {i}: {e}")
                continue
        
        if not accuracies:
            raise ValueError("Не удалось выполнить ни одной успешной итерации")
        
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
            'stability_score': 1 - (np.std(accuracies) / np.mean(accuracies))  # Чем ближе к 1, тем стабильнее
        }
        
        logger.info(f"✅ Monte Carlo валидация завершена")
        logger.info(f"📊 Средняя точность: {mc_results['mean_accuracy']:.4f} ± {mc_results['std_accuracy']:.4f}")
        logger.info(f"📊 Стабильность: {mc_results['stability_score']:.4f}")
        
        return mc_results
    
    def run_complete_analysis(self, symbol: str = "BTCUSD", timeframe: str = "MN1") -> Dict[str, Any]:
        """
        Запуск полного анализа для всех трех задач.
        
        Args:
            symbol: Торговый символ
            timeframe: Таймфрейм
            
        Returns:
            Полные результаты анализа
        """
        logger.info(f"🚀 Запускаем полный анализ для {symbol} {timeframe}")
        
        # 1. Загрузка данных
        raw_data = self.load_schr_data(symbol, timeframe)
        
        # 2. Создание целевых переменных и признаков
        data_with_targets = self.create_target_variables(raw_data)
        final_data = self.create_features(data_with_targets)
        
        logger.info(f"📊 Итоговый датасет: {len(final_data)} записей, {len(final_data.columns)} признаков")
        
        complete_results = {
            'symbol': symbol,
            'timeframe': timeframe,
            'data_info': {
                'total_records': len(final_data),
                'features_count': len(final_data.columns),
                'date_range': (final_data.index.min(), final_data.index.max()) if isinstance(final_data.index, pd.DatetimeIndex) else None
            },
            'models': {},
            'validations': {}
        }
        
        # 3. Обучение моделей для всех задач
        for task in self.task_configs.keys():
            logger.info(f"🎯 Обрабатываем задачу: {task}")
            
            try:
                # Обучение основной модели
                model_results = self.train_model(final_data, task)
                complete_results['models'][task] = model_results
                
                # Walk Forward валидация
                wf_results = self.walk_forward_validation(final_data, task, n_splits=3)
                complete_results['validations'][f'{task}_walk_forward'] = wf_results
                
                # Monte Carlo валидация (меньше итераций для экономии времени)
                mc_results = self.monte_carlo_validation(final_data, task, n_iterations=20)
                complete_results['validations'][f'{task}_monte_carlo'] = mc_results
                
            except Exception as e:
                logger.error(f"❌ Ошибка при обработке задачи {task}: {e}")
                complete_results['models'][task] = {'error': str(e)}
        
        # 4. Сводная оценка
        self._generate_summary_report(complete_results)
        
        logger.info("🎉 Полный анализ завершен!")
        return complete_results
    
    def _generate_summary_report(self, results: Dict[str, Any]):
        """Генерация сводного отчета."""
        logger.info("\n" + "="*80)
        logger.info("📋 СВОДНЫЙ ОТЧЕТ ПО МОДЕЛЯМ SCHR LEVELS")
        logger.info("="*80)
        
        for task, model_results in results['models'].items():
            if 'error' in model_results:
                logger.info(f"❌ {task}: ОШИБКА - {model_results['error']}")
                continue
            
            metrics = model_results['metrics']
            logger.info(f"\n🎯 ЗАДАЧА: {task}")
            logger.info(f"   📊 Точность: {metrics['accuracy']:.4f}")
            logger.info(f"   📊 Precision: {metrics['precision']:.4f}")
            logger.info(f"   📊 Recall: {metrics['recall']:.4f}")
            logger.info(f"   📊 F1-score: {metrics['f1']:.4f}")
            
            # Walk Forward результаты
            wf_key = f'{task}_walk_forward'
            if wf_key in results['validations']:
                wf = results['validations'][wf_key]
                logger.info(f"   🔄 Walk Forward: {wf['mean_accuracy']:.4f} ± {wf['std_accuracy']:.4f}")
            
            # Monte Carlo результаты
            mc_key = f'{task}_monte_carlo'
            if mc_key in results['validations']:
                mc = results['validations'][mc_key]
                logger.info(f"   🎲 Monte Carlo: {mc['mean_accuracy']:.4f} ± {mc['std_accuracy']:.4f}")
                logger.info(f"   🎲 Стабильность: {mc['stability_score']:.4f}")
        
        logger.info("\n" + "="*80)
    
    def predict(self, data: pd.DataFrame, task: str) -> pd.Series:
        """
        Простые предсказания для тестирования
        
        Args:
            data: Данные для предсказания
            task: Название задачи
            
        Returns:
            Предсказания
        """
        try:
            # Загружаем обученную модель
            model_path = f"models/schr_levels_{task}_{self.timestamp}"
            predictor = TabularPredictor.load(model_path)
            
            # Предсказания
            predictions = predictor.predict(data)
            return predictions
            
        except Exception as e:
            logger.error(f"Ошибка предсказания: {e}")
            raise

    def predict_for_trading(self, new_data: pd.DataFrame, task: str) -> Dict[str, Any]:
        """
        Предсказания для реальной торговли.
        
        Args:
            new_data: Новые данные для предсказания
            task: Задача для предсказания
            
        Returns:
            Предсказания с вероятностями
        """
        if task not in self.models:
            raise ValueError(f"Модель для задачи {task} не обучена")
        
        predictor = self.models[task]
        
        # Создаем признаки для новых данных (без целевых переменных)
        features_data = self.create_features(new_data)
        
        # Проверяем, что данные не пустые
        if len(features_data) == 0:
            raise ValueError("Нет данных для предсказания после создания признаков")
        
        # Удаляем целевые переменные если они есть
        target_cols = [col for col in features_data.columns if col.startswith('target_')]
        features_data = features_data.drop(columns=target_cols, errors='ignore')
        
        # Предсказания
        predictions = predictor.predict(features_data)
        probabilities = predictor.predict_proba(features_data) if predictor.can_predict_proba else None
        
        return {
            'predictions': predictions,
            'probabilities': probabilities,
            'confidence': probabilities.max(axis=1) if probabilities is not None else None
        }
    
    def save_models(self, save_path: str = "models/schr_levels_production/"):
        """Сохранение обученных моделей для продакшена."""
        save_path = Path(save_path)
        save_path.mkdir(parents=True, exist_ok=True)
        
        for task, predictor in self.models.items():
            model_file = save_path / f"{task}_model.pkl"
            joblib.dump(predictor, model_file)
            logger.info(f"💾 Модель {task} сохранена: {model_file}")
        
        # Сохраняем результаты
        results_file = save_path / "analysis_results.pkl"
        joblib.dump(self.results, results_file)
        logger.info(f"💾 Результаты анализа сохранены: {results_file}")
    
    def load_models(self, load_path: str = "models/schr_levels_production/"):
        """Загрузка сохраненных моделей."""
        load_path = Path(load_path)
        
        for task in self.task_configs.keys():
            model_file = load_path / f"{task}_model.pkl"
            if model_file.exists():
                self.models[task] = joblib.load(model_file)
                logger.info(f"📂 Модель {task} загружена: {model_file}")
        
        # Загружаем результаты
        results_file = load_path / "analysis_results.pkl"
        if results_file.exists():
            self.results = joblib.load(results_file)
            logger.info(f"📂 Результаты анализа загружены: {results_file}")


def main():
    """Пример использования пайплайна."""
    # Создаем папку для логов если её нет
    Path("logs").mkdir(exist_ok=True)
    
    # Инициализация пайплайна
    pipeline = SCHRLevelsAutoMLPipeline()
    
    try:
        # Запуск полного анализа для BTCUSD месячных данных
        logger.info("🚀 Запускаем полный анализ SCHR Levels...")
        results = pipeline.run_complete_analysis(symbol="BTCUSD", timeframe="MN1")
        
        # Сохранение моделей
        pipeline.save_models()
        
        # Пример предсказания (загружаем новые данные)
        logger.info("🔮 Тестируем предсказания...")
        new_data = pipeline.load_schr_data("BTCUSD", "MN1").tail(10)  # Последние 10 записей для надежности
        
        # Создаем признаки для новых данных
        new_data = pipeline.create_features(new_data)
        
        # Предсказания для всех задач
        for task in pipeline.task_configs.keys():
            if task in pipeline.models:
                try:
                    prediction_results = pipeline.predict_for_trading(new_data, task)
                    logger.info(f"🔮 Предсказание для {task}: {prediction_results['predictions']}")
                    if prediction_results['probabilities'] is not None:
                        logger.info(f"🔮 Вероятности: {prediction_results['probabilities'].values}")
                except Exception as e:
                    logger.error(f"❌ Ошибка предсказания для {task}: {e}")
        
        logger.info("✅ Анализ завершен успешно!")
        
    except Exception as e:
        logger.error(f"❌ Ошибка в основном процессе: {e}")
        raise


if __name__ == "__main__":
    main()
