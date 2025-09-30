# Лучшие практики AutoML Gluon

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Введение в лучшие практики

![Сравнение производительности](images/performance_comparison.png)
*Рисунок 7: Сравнение производительности различных моделей*

Лучшие практики - это накопленный опыт использования AutoML Gluon, который поможет избежать типичных ошибок и достичь максимальной эффективности. В этом разделе рассмотрим все аспекты правильного использования инструмента.

## Подготовка данных

### 1. Качество данных

```python
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import matplotlib.pyplot as plt
import seaborn as sns

def data_quality_check(data: pd.DataFrame) -> Dict[str, Any]:
    """Комплексная проверка качества данных"""
    
    quality_report = {
        'shape': data.shape,
        'missing_values': data.isnull().sum().to_dict(),
        'data_types': data.dtypes.to_dict(),
        'duplicates': data.duplicated().sum(),
        'outliers': {},
        'correlations': {}
    }
    
    # Проверка пропущенных значений
    missing_percent = (data.isnull().sum() / len(data)) * 100
    quality_report['missing_percent'] = missing_percent.to_dict()
    
    # Проверка выбросов для числовых колонок
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = data[(data[col] < Q1 - 1.5 * IQR) | (data[col] > Q3 + 1.5 * IQR)]
        quality_report['outliers'][col] = len(outliers)
    
    # Проверка корреляций
    if len(numeric_columns) > 1:
        correlation_matrix = data[numeric_columns].corr()
        quality_report['correlations'] = correlation_matrix.to_dict()
    
    return quality_report

# Использование
quality_report = data_quality_check(train_data)
print("Data Quality Report:")
for key, value in quality_report.items():
    print(f"{key}: {value}")
```

### 2. Обработка пропущенных значений

```python
def handle_missing_values(data: pd.DataFrame, strategy: str = 'auto') -> pd.DataFrame:
    """Обработка пропущенных значений"""
    
    if strategy == 'auto':
        # Автоматическая стратегия
        for col in data.columns:
            if data[col].dtype == 'object':
                # Для категориальных переменных - мода
                data[col].fillna(data[col].mode()[0] if not data[col].mode().empty else 'Unknown', inplace=True)
            else:
                # Для числовых переменных - медиана
                data[col].fillna(data[col].median(), inplace=True)
    
    elif strategy == 'drop':
        # Удаление строк с пропущенными значениями
        data = data.dropna()
    
    elif strategy == 'interpolate':
        # Интерполяция для временных рядов
        data = data.interpolate(method='linear')
    
    return data

# Использование
train_data_clean = handle_missing_values(train_data, strategy='auto')
```

### 3. Обработка выбросов

```python
def handle_outliers(data: pd.DataFrame, method: str = 'iqr') -> pd.DataFrame:
    """Обработка выбросов"""
    
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    
    if method == 'iqr':
        # Метод межквартильного размаха
        for col in numeric_columns:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Замена выбросов на граничные значения
            data[col] = np.where(data[col] < lower_bound, lower_bound, data[col])
            data[col] = np.where(data[col] > upper_bound, upper_bound, data[col])
    
    elif method == 'zscore':
        # Метод Z-скор
        for col in numeric_columns:
            z_scores = np.abs((data[col] - data[col].mean()) / data[col].std())
            data = data[z_scores < 3]  # Удаление выбросов
    
    elif method == 'winsorize':
        # Винзоризация
        for col in numeric_columns:
            lower_percentile = data[col].quantile(0.05)
            upper_percentile = data[col].quantile(0.95)
            data[col] = np.where(data[col] < lower_percentile, lower_percentile, data[col])
            data[col] = np.where(data[col] > upper_percentile, upper_percentile, data[col])
    
    return data

# Использование
train_data_no_outliers = handle_outliers(train_data, method='iqr')
```

## Выбор метрик

### 1. Метрики для классификации

```python
def select_classification_metrics(problem_type: str, data_balance: str = 'balanced') -> List[str]:
    """Выбор метрик для классификации"""
    
    if problem_type == 'binary':
        if data_balance == 'balanced':
            return ['accuracy', 'f1', 'roc_auc', 'precision', 'recall']
        elif data_balance == 'imbalanced':
            return ['f1', 'roc_auc', 'precision', 'recall', 'balanced_accuracy']
        else:
            return ['accuracy', 'f1', 'roc_auc']
    
    elif problem_type == 'multiclass':
        if data_balance == 'balanced':
            return ['accuracy', 'f1_macro', 'f1_micro', 'precision_macro', 'recall_macro']
        elif data_balance == 'imbalanced':
            return ['f1_macro', 'f1_micro', 'balanced_accuracy', 'precision_macro', 'recall_macro']
        else:
            return ['accuracy', 'f1_macro', 'f1_micro']
    
    else:
        return ['accuracy', 'f1', 'roc_auc']

# Использование
metrics = select_classification_metrics('binary', 'imbalanced')
predictor = TabularPredictor(
    label='target',
    problem_type='binary',
    eval_metric=metrics[0]  # Основная метрика
)
```

### 2. Метрики для регрессии

```python
def select_regression_metrics(problem_type: str, target_distribution: str = 'normal') -> List[str]:
    """Выбор метрик для регрессии"""
    
    if target_distribution == 'normal':
        return ['rmse', 'mae', 'r2']
    elif target_distribution == 'skewed':
        return ['mae', 'mape', 'smape']
    elif target_distribution == 'outliers':
        return ['mae', 'huber_loss']
    else:
        return ['rmse', 'mae']

# Использование
metrics = select_regression_metrics('regression', 'normal')
predictor = TabularPredictor(
    label='target',
    problem_type='regression',
    eval_metric=metrics[0]
)
```

## Настройка гиперпараметров

### 1. Стратегия поиска гиперпараметров

```python
def create_hyperparameter_strategy(data_size: int, problem_type: str) -> Dict[str, Any]:
    """Создание стратегии поиска гиперпараметров"""
    
    if data_size < 1000:
        # Маленький датасет - простые модели
        return {
            'GBM': [{'num_boost_round': 100, 'learning_rate': 0.1}],
            'RF': [{'n_estimators': 100, 'max_depth': 10}],
            'XGB': [{'n_estimators': 100, 'max_depth': 6}]
        }
    
    elif data_size < 10000:
        # Средний датасет - умеренная сложность
        return {
            'GBM': [
                {'num_boost_round': 200, 'learning_rate': 0.1},
                {'num_boost_round': 300, 'learning_rate': 0.05}
            ],
            'RF': [
                {'n_estimators': 200, 'max_depth': 15},
                {'n_estimators': 300, 'max_depth': 20}
            ],
            'XGB': [
                {'n_estimators': 200, 'max_depth': 8},
                {'n_estimators': 300, 'max_depth': 10}
            ]
        }
    
    else:
        # Большой датасет - сложные модели
        return {
            'GBM': [
                {'num_boost_round': 500, 'learning_rate': 0.1},
                {'num_boost_round': 1000, 'learning_rate': 0.05}
            ],
            'RF': [
                {'n_estimators': 500, 'max_depth': 20},
                {'n_estimators': 1000, 'max_depth': 25}
            ],
            'XGB': [
                {'n_estimators': 500, 'max_depth': 10},
                {'n_estimators': 1000, 'max_depth': 12}
            ],
            'CAT': [
                {'iterations': 500, 'learning_rate': 0.1},
                {'iterations': 1000, 'learning_rate': 0.05}
            ]
        }

# Использование
hyperparameters = create_hyperparameter_strategy(len(train_data), 'binary')
predictor.fit(train_data, hyperparameters=hyperparameters)
```

### 2. Оптимизация времени обучения

```python
def optimize_training_time(data_size: int, available_time: int) -> Dict[str, Any]:
    """Оптимизация времени обучения"""
    
    # Расчет времени на модель
    time_per_model = available_time / 10  # 10 моделей по умолчанию
    
    if data_size < 1000:
        # Быстрое обучение
        return {
            'time_limit': time_per_model,
            'presets': 'optimize_for_deployment',
            'num_bag_folds': 3,
            'num_bag_sets': 1
        }
    
    elif data_size < 10000:
        # Умеренное обучение
        return {
            'time_limit': time_per_model,
            'presets': 'medium_quality',
            'num_bag_folds': 5,
            'num_bag_sets': 1
        }
    
    else:
        # Качественное обучение
        return {
            'time_limit': time_per_model,
            'presets': 'high_quality',
            'num_bag_folds': 5,
            'num_bag_sets': 2
        }

# Использование
training_config = optimize_training_time(len(train_data), 3600)  # 1 час
predictor.fit(train_data, **training_config)
```

## Валидация и тестирование

### 1. Стратегия валидации

```python
def select_validation_strategy(data_size: int, problem_type: str, 
                             data_type: str = 'tabular') -> Dict[str, Any]:
    """Выбор стратегии валидации"""
    
    if data_type == 'time_series':
        return {
            'validation_strategy': 'time_series_split',
            'n_splits': 5,
            'test_size': 0.2
        }
    
    elif data_size < 1000:
        return {
            'validation_strategy': 'holdout',
            'holdout_frac': 0.3
        }
    
    elif data_size < 10000:
        return {
            'validation_strategy': 'kfold',
            'num_bag_folds': 5,
            'num_bag_sets': 1
        }
    
    else:
        return {
            'validation_strategy': 'kfold',
            'num_bag_folds': 10,
            'num_bag_sets': 1
        }

# Использование
validation_config = select_validation_strategy(len(train_data), 'binary')
predictor.fit(train_data, **validation_config)
```

### 2. Кросс-валидация

```python
def perform_cross_validation(predictor, data: pd.DataFrame, 
                           n_folds: int = 5) -> Dict[str, Any]:
    """Выполнение кросс-валидации"""
    
    from sklearn.model_selection import KFold
    import numpy as np
    
    kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
    
    fold_results = []
    
    for fold, (train_idx, val_idx) in enumerate(kf.split(data)):
        # Разделение данных
        train_fold = data.iloc[train_idx]
        val_fold = data.iloc[val_idx]
        
        # Обучение модели
        fold_predictor = TabularPredictor(
            label=predictor.label,
            problem_type=predictor.problem_type,
            eval_metric=predictor.eval_metric
        )
        
        fold_predictor.fit(train_fold, time_limit=300)
        
        # Предсказания
        predictions = fold_predictor.predict(val_fold)
        
        # Оценка качества
        performance = fold_predictor.evaluate(val_fold)
        
        fold_results.append({
            'fold': fold + 1,
            'performance': performance
        })
    
    # Агрегация результатов
    all_metrics = {}
    for result in fold_results:
        for metric, value in result['performance'].items():
            if metric not in all_metrics:
                all_metrics[metric] = []
            all_metrics[metric].append(value)
    
    # Статистика
    cv_results = {}
    for metric, values in all_metrics.items():
        cv_results[metric] = {
            'mean': np.mean(values),
            'std': np.std(values),
            'min': np.min(values),
            'max': np.max(values)
        }
    
    return cv_results

# Использование
cv_results = perform_cross_validation(predictor, train_data, n_folds=5)
print("Cross-validation results:")
for metric, stats in cv_results.items():
    print(f"{metric}: {stats['mean']:.4f} ± {stats['std']:.4f}")
```

## Работа с ансамблями

### 1. Настройка ансамблей

```python
def configure_ensemble(data_size: int, problem_type: str) -> Dict[str, Any]:
    """Настройка ансамбля"""
    
    if data_size < 1000:
        # Простой ансамбль
        return {
            'num_bag_folds': 3,
            'num_bag_sets': 1,
            'num_stack_levels': 0
        }
    
    elif data_size < 10000:
        # Умеренный ансамбль
        return {
            'num_bag_folds': 5,
            'num_bag_sets': 1,
            'num_stack_levels': 1
        }
    
    else:
        # Сложный ансамбль
        return {
            'num_bag_folds': 5,
            'num_bag_sets': 2,
            'num_stack_levels': 2
        }

# Использование
ensemble_config = configure_ensemble(len(train_data), 'binary')
predictor.fit(train_data, **ensemble_config)
```

### 2. Анализ ансамбля

```python
def analyze_ensemble(predictor) -> Dict[str, Any]:
    """Анализ ансамбля"""
    
    # Лидерборд моделей
    leaderboard = predictor.leaderboard()
    
    # Анализ производительности
    ensemble_analysis = {
        'total_models': len(leaderboard),
        'best_model': leaderboard.iloc[0]['model'],
        'best_score': leaderboard.iloc[0]['score_val'],
        'model_diversity': calculate_model_diversity(leaderboard),
        'performance_gap': leaderboard.iloc[0]['score_val'] - leaderboard.iloc[-1]['score_val']
    }
    
    return ensemble_analysis

def calculate_model_diversity(leaderboard: pd.DataFrame) -> float:
    """Расчет разнообразия моделей"""
    
    # Разнообразие по типам моделей
    model_types = leaderboard['model'].str.split('_').str[0].value_counts()
    diversity = len(model_types) / len(leaderboard)
    
    return diversity

# Использование
ensemble_analysis = analyze_ensemble(predictor)
print("Ensemble Analysis:")
for key, value in ensemble_analysis.items():
    print(f"{key}: {value}")
```

## Оптимизация производительности

### 1. Настройка ресурсов

```python
def optimize_resources(data_size: int, available_resources: Dict[str, int]) -> Dict[str, Any]:
    """Оптимизация ресурсов"""
    
    # Расчет оптимальных параметров
    if data_size < 1000:
        num_cpus = min(2, available_resources.get('cpus', 4))
        memory_limit = min(4, available_resources.get('memory', 8))
    elif data_size < 10000:
        num_cpus = min(4, available_resources.get('cpus', 8))
        memory_limit = min(8, available_resources.get('memory', 16))
    else:
        num_cpus = min(8, available_resources.get('cpus', 16))
        memory_limit = min(16, available_resources.get('memory', 32))
    
    return {
        'num_cpus': num_cpus,
        'num_gpus': available_resources.get('gpus', 0),
        'memory_limit': memory_limit
    }

# Использование
resources = optimize_resources(len(train_data), {'cpus': 8, 'memory': 16, 'gpus': 1})
predictor.fit(train_data, ag_args_fit=resources)
```

### 2. Параллелизация

```python
def configure_parallelization(data_size: int, problem_type: str) -> Dict[str, Any]:
    """Настройка параллелизации"""
    
    if data_size < 1000:
        # Последовательное обучение
        return {
            'parallel_folds': False,
            'parallel_models': False
        }
    
    elif data_size < 10000:
        # Умеренная параллелизация
        return {
            'parallel_folds': True,
            'parallel_models': False
        }
    
    else:
        # Полная параллелизация
        return {
            'parallel_folds': True,
            'parallel_models': True
        }

# Использование
parallel_config = configure_parallelization(len(train_data), 'binary')
# Применение конфигурации через ag_args_fit
```

## Мониторинг и логирование

### 1. Система логирования

```python
import logging
from datetime import datetime
import json

class AutoGluonLogger:
    """Система логирования для AutoGluon"""
    
    def __init__(self, log_file: str = 'autogluon.log'):
        self.log_file = log_file
        self.setup_logging()
    
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_training_start(self, data_info: Dict[str, Any]):
        """Логирование начала обучения"""
        self.logger.info(f"Training started: {data_info}")
    
    def log_training_progress(self, progress: Dict[str, Any]):
        """Логирование прогресса обучения"""
        self.logger.info(f"Training progress: {progress}")
    
    def log_training_complete(self, results: Dict[str, Any]):
        """Логирование завершения обучения"""
        self.logger.info(f"Training completed: {results}")
    
    def log_prediction(self, input_data: Dict, prediction: Any, 
                      processing_time: float):
        """Логирование предсказания"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'input_data': input_data,
            'prediction': prediction,
            'processing_time': processing_time
        }
        self.logger.info(f"Prediction: {log_entry}")
    
    def log_error(self, error: Exception, context: Dict[str, Any]):
        """Логирование ошибок"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'error': str(error),
            'context': context
        }
        self.logger.error(f"Error: {error_entry}")

# Использование
logger = AutoGluonLogger()
logger.log_training_start({'data_size': len(train_data), 'features': len(train_data.columns)})
```

### 2. Мониторинг производительности

```python
import psutil
import time
from typing import Dict, Any

class PerformanceMonitor:
    """Мониторинг производительности"""
    
    def __init__(self):
        self.metrics_history = []
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Получение системных метрик"""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'timestamp': datetime.now().isoformat()
        }
    
    def monitor_training(self, predictor, data: pd.DataFrame):
        """Мониторинг обучения"""
        start_time = time.time()
        
        # Начальные метрики
        initial_metrics = self.get_system_metrics()
        self.metrics_history.append(initial_metrics)
        
        # Обучение с мониторингом
        predictor.fit(data, time_limit=3600)
        
        # Финальные метрики
        final_metrics = self.get_system_metrics()
        final_metrics['training_time'] = time.time() - start_time
        self.metrics_history.append(final_metrics)
        
        return final_metrics
    
    def analyze_performance(self) -> Dict[str, Any]:
        """Анализ производительности"""
        if len(self.metrics_history) < 2:
            return {}
        
        # Анализ использования ресурсов
        cpu_usage = [m['cpu_percent'] for m in self.metrics_history]
        memory_usage = [m['memory_percent'] for m in self.metrics_history]
        
        return {
            'avg_cpu_usage': sum(cpu_usage) / len(cpu_usage),
            'max_cpu_usage': max(cpu_usage),
            'avg_memory_usage': sum(memory_usage) / len(memory_usage),
            'max_memory_usage': max(memory_usage),
            'training_time': self.metrics_history[-1].get('training_time', 0)
        }

# Использование
monitor = PerformanceMonitor()
final_metrics = monitor.monitor_training(predictor, train_data)
performance_analysis = monitor.analyze_performance()
print(f"Performance analysis: {performance_analysis}")
```

## Обработка ошибок

### 1. Обработка исключений

```python
def safe_training(predictor, data: pd.DataFrame, **kwargs) -> Dict[str, Any]:
    """Безопасное обучение с обработкой ошибок"""
    
    try:
        # Обучение модели
        predictor.fit(data, **kwargs)
        
        # Валидация модели
        if hasattr(predictor, 'evaluate'):
            performance = predictor.evaluate(data)
            return {
                'status': 'success',
                'performance': performance,
                'error': None
            }
        else:
            return {
                'status': 'success',
                'performance': None,
                'error': None
            }
    
    except MemoryError as e:
        return {
            'status': 'error',
            'performance': None,
            'error': f'Memory error: {str(e)}',
            'suggestion': 'Reduce data size or increase memory'
        }
    
    except TimeoutError as e:
        return {
            'status': 'error',
            'performance': None,
            'error': f'Timeout error: {str(e)}',
            'suggestion': 'Increase time_limit or reduce model complexity'
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'performance': None,
            'error': f'Unexpected error: {str(e)}',
            'suggestion': 'Check data quality and parameters'
        }

# Использование
result = safe_training(predictor, train_data, time_limit=3600)
if result['status'] == 'success':
    print(f"Training successful: {result['performance']}")
else:
    print(f"Training failed: {result['error']}")
    print(f"Suggestion: {result['suggestion']}")
```

### 2. Восстановление после ошибок

```python
def resilient_training(predictor, data: pd.DataFrame, 
                      fallback_strategies: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Устойчивое обучение с fallback стратегиями"""
    
    for i, strategy in enumerate(fallback_strategies):
        try:
            # Попытка обучения с текущей стратегией
            predictor.fit(data, **strategy)
            
            # Валидация
            if validate_model(predictor):
                return {
                    'status': 'success',
                    'strategy_used': i,
                    'strategy_config': strategy
                }
            else:
                continue
        
        except Exception as e:
            print(f"Strategy {i} failed: {str(e)}")
            continue
    
    return {
        'status': 'error',
        'error': 'All strategies failed',
        'suggestions': [
            'Check data quality',
            'Reduce model complexity',
            'Increase time limits',
            'Use simpler algorithms'
        ]
    }

# Fallback стратегии
fallback_strategies = [
    {'presets': 'best_quality', 'time_limit': 3600},
    {'presets': 'high_quality', 'time_limit': 1800},
    {'presets': 'medium_quality', 'time_limit': 900},
    {'presets': 'optimize_for_deployment', 'time_limit': 300}
]

result = resilient_training(predictor, train_data, fallback_strategies)
```

## Оптимизация для продакшена

### 1. Сжатие модели

```python
def optimize_for_production(predictor, target_size_mb: int = 100) -> Dict[str, Any]:
    """Оптимизация модели для продакшена"""
    
    # Получение размера текущей модели
    current_size = get_model_size(predictor)
    
    if current_size <= target_size_mb:
        return {
            'status': 'already_optimized',
            'current_size': current_size,
            'target_size': target_size_mb
        }
    
    # Стратегии оптимизации
    optimization_strategies = [
        {
            'name': 'reduce_models',
            'config': {
                'excluded_model_types': ['KNN', 'NN_TORCH'],
                'presets': 'optimize_for_deployment'
            }
        },
        {
            'name': 'compress_models',
            'config': {
                'save_space': True,
                'compress': True
            }
        },
        {
            'name': 'simplify_ensemble',
            'config': {
                'num_bag_folds': 3,
                'num_bag_sets': 1,
                'num_stack_levels': 0
            }
        }
    ]
    
    for strategy in optimization_strategies:
        try:
            # Применение стратегии
            optimized_predictor = apply_optimization_strategy(predictor, strategy)
            
            # Проверка размера
            optimized_size = get_model_size(optimized_predictor)
            
            if optimized_size <= target_size_mb:
                return {
                    'status': 'optimized',
                    'strategy': strategy['name'],
                    'original_size': current_size,
                    'optimized_size': optimized_size,
                    'compression_ratio': optimized_size / current_size
                }
        
        except Exception as e:
            print(f"Optimization strategy {strategy['name']} failed: {e}")
            continue
    
    return {
        'status': 'failed',
        'error': 'Could not achieve target size',
        'suggestions': [
            'Increase target size',
            'Use simpler algorithms',
            'Reduce training data',
            'Use model compression techniques'
        ]
    }

# Использование
optimization_result = optimize_for_production(predictor, target_size_mb=50)
print(f"Optimization result: {optimization_result}")
```

### 2. Кэширование предсказаний

```python
import hashlib
import json
from typing import Optional

class PredictionCache:
    """Кэш для предсказаний"""
    
    def __init__(self, cache_size: int = 1000):
        self.cache_size = cache_size
        self.cache = {}
        self.access_count = {}
    
    def _generate_cache_key(self, data: Dict) -> str:
        """Генерация ключа кэша"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def get_prediction(self, data: Dict) -> Optional[Any]:
        """Получение предсказания из кэша"""
        cache_key = self._generate_cache_key(data)
        
        if cache_key in self.cache:
            # Обновление счетчика доступа
            self.access_count[cache_key] = self.access_count.get(cache_key, 0) + 1
            return self.cache[cache_key]
        
        return None
    
    def set_prediction(self, data: Dict, prediction: Any):
        """Сохранение предсказания в кэш"""
        cache_key = self._generate_cache_key(data)
        
        # Проверка размера кэша
        if len(self.cache) >= self.cache_size:
            # Удаление наименее используемого элемента
            least_used_key = min(self.access_count.keys(), key=self.access_count.get)
            del self.cache[least_used_key]
            del self.access_count[least_used_key]
        
        # Добавление нового элемента
        self.cache[cache_key] = prediction
        self.access_count[cache_key] = 1
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Статистика кэша"""
        return {
            'cache_size': len(self.cache),
            'max_cache_size': self.cache_size,
            'hit_rate': self.calculate_hit_rate(),
            'most_accessed': max(self.access_count.items(), key=lambda x: x[1]) if self.access_count else None
        }
    
    def calculate_hit_rate(self) -> float:
        """Расчет hit rate кэша"""
        if not self.access_count:
            return 0.0
        
        total_accesses = sum(self.access_count.values())
        cache_hits = len(self.cache)
        return cache_hits / total_accesses if total_accesses > 0 else 0.0

# Использование
cache = PredictionCache(cache_size=1000)

def cached_predict(predictor, data: Dict) -> Any:
    """Кэшированное предсказание"""
    # Проверка кэша
    cached_prediction = cache.get_prediction(data)
    if cached_prediction is not None:
        return cached_prediction
    
    # Выполнение предсказания
    prediction = predictor.predict(pd.DataFrame([data]))
    
    # Сохранение в кэш
    cache.set_prediction(data, prediction)
    
    return prediction
```

## Следующие шаги

После освоения лучших практик переходите к:
- [Примерам использования](./09_examples.md)
- [Troubleshooting](./10_troubleshooting.md)
