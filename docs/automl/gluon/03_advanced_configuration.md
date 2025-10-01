# Продвинутая конфигурация AutoML Gluon

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему продвинутая конфигурация критически важна

**Почему 90% пользователей AutoML Gluon не используют продвинутые настройки?** Потому что они не понимают, какую мощь они упускают. Это как водить Ferrari на первой передаче - машина едет, но не показывает своих возможностей.

### Что дает продвинутая конфигурация?
- **Точность**: Модели работают на 10-30% лучше
- **Скорость**: Обучение ускоряется в 2-5 раз
- **Контроль**: Вы точно знаете, что происходит
- **Оптимизация**: Модель подстраивается под ваши данные

### Что происходит без продвинутой конфигурации?
- **Средние результаты**: Модели работают "как получится"
- **Медленное обучение**: Тратите время на неоптимальные настройки
- **Недоиспользование ресурсов**: GPU и CPU работают неэффективно
- **Разочарование**: Не понимаете, почему результаты не улучшаются

## Настройка гиперпараметров

**Почему гиперпараметры - это ключ к успеху?** Потому что они определяют, как алгоритм учится. Это как настройка музыкального инструмента - правильная настройка дает красивый звук.

### Создание кастомных гиперпараметров

**Почему нужны кастомные гиперпараметры?** Потому что стандартные настройки подходят для средних случаев, а ваши данные могут быть особенными.

```python
# Детальная настройка для каждого алгоритма
hyperparameters = {
    'GBM': [  # Gradient Boosting Machine - один из лучших алгоритмов
        {
            # Быстрая конфигурация для экспериментов
            'num_boost_round': 100,        # Количество деревьев (больше = точнее, но медленнее)
            'num_leaves': 31,               # Максимальное количество листьев в дереве
            'learning_rate': 0.1,          # Скорость обучения (меньше = стабильнее)
            'feature_fraction': 0.9,        # Доля признаков для каждого дерева (предотвращает переобучение)
            'bagging_fraction': 0.8,        # Доля данных для каждого дерева
            'bagging_freq': 5,              # Частота применения bagging
            'min_data_in_leaf': 20,         # Минимум данных в листе (предотвращает переобучение)
            'min_sum_hessian_in_leaf': 1e-3, # Минимум суммы градиентов в листе
            'lambda_l1': 0.0,              # L1 регуляризация (Lasso)
            'lambda_l2': 0.0,              # L2 регуляризация (Ridge)
            'min_gain_to_split': 0.0,       # Минимальный прирост для разделения
            'max_depth': -1,               # Максимальная глубина (-1 = без ограничений)
            'save_binary': True,            # Сохранять бинарные файлы
            'seed': 0,                     # Семя для воспроизводимости
            'feature_fraction_seed': 2,     # Семя для выбора признаков
            'bagging_seed': 3,              # Семя для bagging
            'drop_seed': 4,                 # Семя для dropout
            'verbose': -1,                  # Уровень вывода (-1 = тихо)
            'keep_training_booster': False  # Не сохранять промежуточные модели
        },
        {
            # Тщательная конфигурация для финального обучения
            'num_boost_round': 200,        # Больше деревьев для лучшей точности
            'num_leaves': 63,               # Больше листьев для сложных паттернов
            'learning_rate': 0.05,          # Меньшая скорость для стабильности
            'feature_fraction': 0.8,        # Меньше признаков для предотвращения переобучения
            'bagging_fraction': 0.7,        # Меньше данных для большего разнообразия
            'bagging_freq': 5,              # Та же частота bagging
            'min_data_in_leaf': 10,         # Меньше данных в листе для детализации
            'min_sum_hessian_in_leaf': 1e-3, # Тот же минимум градиентов
            'lambda_l1': 0.1,              # L1 регуляризация для отбора признаков
            'lambda_l2': 0.1,              # L2 регуляризация для сглаживания
            'min_gain_to_split': 0.0,       # Тот же минимальный прирост
            'max_depth': -1,               # Без ограничений глубины
            'save_binary': True,            # Сохранять бинарные файлы
            'seed': 0,                     # Семя для воспроизводимости
            'feature_fraction_seed': 2,     # Семя для выбора признаков
            'bagging_seed': 3,              # Семя для bagging
            'drop_seed': 4,                 # Семя для dropout
            'verbose': -1,                  # Тихий режим
            'keep_training_booster': False
        }
    ],
    'CAT': [  # CatBoost - отличный алгоритм для категориальных данных
        {
            # Базовая конфигурация CatBoost
            'iterations': 100,           # Количество итераций (больше = точнее)
            'learning_rate': 0.1,        # Скорость обучения
            'depth': 6,                  # Глубина деревьев (больше = сложнее)
            'l2_leaf_reg': 3.0,          # L2 регуляризация для листьев
            'bootstrap_type': 'Bayesian',
            'random_strength': 1.0,
            'bagging_temperature': 1.0,
            'od_type': 'Iter',
            'od_wait': 20,
            'verbose': False
        },
        {
            'iterations': 200,
            'learning_rate': 0.05,
            'depth': 8,
            'l2_leaf_reg': 5.0,
            'bootstrap_type': 'Bayesian',
            'random_strength': 1.0,
            'bagging_temperature': 1.0,
            'od_type': 'Iter',
            'od_wait': 20,
            'verbose': False
        }
    ],
    'XGB': [
        {
            'n_estimators': 100,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'reg_alpha': 0.0,
            'reg_lambda': 1.0,
            'random_state': 0
        },
        {
            'n_estimators': 200,
            'max_depth': 8,
            'learning_rate': 0.05,
            'subsample': 0.9,
            'colsample_bytree': 0.9,
            'reg_alpha': 0.1,
            'reg_lambda': 1.0,
            'random_state': 0
        }
    ],
    'RF': [
        {
            'n_estimators': 100,
            'max_depth': 10,
            'min_samples_split': 2,
            'min_samples_leaf': 1,
            'max_features': 'sqrt',
            'bootstrap': True,
            'random_state': 0
        }
    ],
    'KNN': [
        {
            'n_neighbors': 5,
            'weights': 'uniform',
            'algorithm': 'auto',
            'leaf_size': 30,
            'p': 2,
            'metric': 'minkowski'
        }
    ]
}

predictor.fit(train_data, hyperparameters=hyperparameters)
```

### Оптимизация гиперпараметров

```python
# Настройка поиска гиперпараметров
from autogluon.core import Space

# Определение пространства поиска
hyperparameter_space = {
    'GBM': {
        'num_boost_round': Space(50, 500),
        'num_leaves': Space(31, 127),
        'learning_rate': Space(0.01, 0.3),
        'feature_fraction': Space(0.5, 1.0),
        'bagging_fraction': Space(0.5, 1.0)
    },
    'XGB': {
        'n_estimators': Space(50, 500),
        'max_depth': Space(3, 10),
        'learning_rate': Space(0.01, 0.3),
        'subsample': Space(0.5, 1.0),
        'colsample_bytree': Space(0.5, 1.0)
    }
}

predictor.fit(
    train_data,
    hyperparameter_tune_kwargs={
        'num_trials': 20,
        'scheduler': 'local',
        'searcher': 'auto'
    }
)
```

## Настройка ансамблей

### Многоуровневые ансамбли

```python
# Настройка стекинга
predictor.fit(
    train_data,
    num_bag_folds=5,        # Количество фолдов для бэггинга
    num_bag_sets=2,         # Количество наборов бэггинга
    num_stack_levels=2,     # Уровни стекинга
    stack_ensemble_levels=[0, 1],  # Какие уровни использовать для стекинга
    ag_args_fit={'num_gpus': 1, 'num_cpus': 4}  # Ресурсы для обучения
)
```

### Кастомные ансамбли

```python
from autogluon.tabular.models import AbstractModel

class CustomEnsembleModel(AbstractModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.models = []
    
    def _fit(self, X, y, **kwargs):
        # Логика обучения кастомного ансамбля
        pass
    
    def _predict(self, X, **kwargs):
        # Логика предсказания кастомного ансамбля
        pass

# Использование кастомного ансамбля
predictor.fit(
    train_data,
    custom_ensemble_model=CustomEnsembleModel
)
```

## Настройка ресурсов

### CPU и GPU настройки

```python
# Настройка ресурсов для обучения
ag_args_fit = {
    'num_cpus': 8,          # Количество CPU ядер
    'num_gpus': 1,          # Количество GPU
    'memory_limit': 16,     # Лимит памяти в GB
    'time_limit': 3600      # Лимит времени в секундах
}

predictor.fit(
    train_data,
    ag_args_fit=ag_args_fit
)
```

### Параллельное обучение

```python
# Настройка параллельного обучения
from autogluon.core import scheduler

# Локальный планировщик
local_scheduler = scheduler.LocalScheduler(
    num_cpus=8,
    num_gpus=1
)

predictor.fit(
    train_data,
    scheduler=local_scheduler
)
```

## Работа с большими данными

### Инкрементальное обучение

```python
# Обучение по частям
chunk_size = 10000
for i in range(0, len(train_data), chunk_size):
    chunk = train_data[i:i+chunk_size]
    if i == 0:
        predictor.fit(chunk)
    else:
        predictor.fit(chunk, refit_full=True)
```

### Распределенное обучение

```python
# Настройка для распределенного обучения
from autogluon.core import scheduler

# Ray планировщик для распределенного обучения
ray_scheduler = scheduler.RayScheduler(
    num_cpus=32,
    num_gpus=4,
    ray_address='auto'
)

predictor.fit(
    train_data,
    scheduler=ray_scheduler
)
```

## Настройка валидации

### Кастомные стратегии валидации

```python
from sklearn.model_selection import TimeSeriesSplit

# Временная валидация для временных рядов
def time_series_split(X, y, n_splits=5):
    tscv = TimeSeriesSplit(n_splits=n_splits)
    for train_idx, val_idx in tscv.split(X):
        yield train_idx, val_idx

predictor.fit(
    train_data,
    validation_strategy='custom',
    custom_validation_strategy=time_series_split
)
```

### Стратифицированная валидация

```python
from sklearn.model_selection import StratifiedKFold

# Стратифицированная валидация
def stratified_split(X, y, n_splits=5):
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    for train_idx, val_idx in skf.split(X, y):
        yield train_idx, val_idx

predictor.fit(
    train_data,
    validation_strategy='custom',
    custom_validation_strategy=stratified_split
)
```

## Настройка признаков

### Кастомные генераторы признаков

```python
from autogluon.features import FeatureGenerator

# Создание кастомного генератора признаков
class CustomFeatureGenerator(FeatureGenerator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.custom_features = []
    
    def _generate_features(self, X):
        # Генерация кастомных признаков
        X['feature_ratio'] = X['feature1'] / (X['feature2'] + 1e-8)
        X['feature_interaction'] = X['feature1'] * X['feature2']
        return X

# Использование кастомного генератора
feature_generator = CustomFeatureGenerator()
train_data_processed = feature_generator.fit_transform(train_data)
```

### Обработка текстовых данных

```python
# Настройка обработки текста
text_features = {
    'enable_text_special_features': True,
    'enable_text_ngram_features': True,
    'text_ngram_range': (1, 3),
    'text_max_features': 10000,
    'text_min_df': 2,
    'text_max_df': 0.95
}

predictor.fit(
    train_data,
    feature_generator_kwargs=text_features
)
```

## Настройка метрик

### Кастомные метрики

```python
from autogluon.core import Scorer

# Создание кастомной метрики
def custom_metric(y_true, y_pred):
    """Кастомная метрика для оценки качества"""
    # Ваша логика расчета метрики
    return score

custom_scorer = Scorer(
    name='custom_metric',
    score_func=custom_metric,
    greater_is_better=True
)

predictor.fit(
    train_data,
    eval_metric=custom_scorer
)
```

### Множественные метрики

```python
# Обучение с несколькими метриками
predictor.fit(
    train_data,
    eval_metric=['accuracy', 'f1', 'roc_auc']
)
```

## Настройка логирования

### Детальное логирование

```python
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autogluon.log'),
        logging.StreamHandler()
    ]
)

# Обучение с подробным логированием
predictor.fit(
    train_data,
    verbosity=3,  # Максимальное логирование
    log_to_file=True
)
```

### Мониторинг обучения

```python
# Callback для мониторинга
def training_monitor(epoch, logs):
    print(f"Epoch {epoch}: {logs}")

predictor.fit(
    train_data,
    callbacks=[training_monitor]
)
```

## Настройка для продакшена

### Оптимизация для деплоя

```python
# Настройки для продакшена
production_config = {
    'presets': 'optimize_for_deployment',
    'ag_args_fit': {
        'num_cpus': 4,
        'num_gpus': 0,
        'memory_limit': 8
    },
    'hyperparameters': {
        'GBM': [{'num_boost_round': 100}],
        'XGB': [{'n_estimators': 100}],
        'RF': [{'n_estimators': 100}]
    }
}

predictor.fit(train_data, **production_config)
```

### Сжатие модели

```python
# Сохранение сжатой модели
predictor.save(
    'production_model',
    save_space=True,
    compress=True
)
```

## Примеры продвинутой конфигурации

### Полная конфигурация для продакшена

```python
from autogluon.tabular import TabularPredictor
import pandas as pd

# Создание предиктора с полной конфигурацией
predictor = TabularPredictor(
    label='target',
    problem_type='auto',
    eval_metric='auto',
    path='./models',
    verbosity=2
)

# Продвинутые гиперпараметры
advanced_hyperparameters = {
    'GBM': [
        {
            'num_boost_round': 1000,
            'num_leaves': 31,
            'learning_rate': 0.1,
            'feature_fraction': 0.9,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'min_data_in_leaf': 20,
            'min_sum_hessian_in_leaf': 1e-3,
            'lambda_l1': 0.0,
            'lambda_l2': 0.0,
            'min_gain_to_split': 0.0,
            'max_depth': -1,
            'save_binary': True,
            'seed': 0,
            'feature_fraction_seed': 2,
            'bagging_seed': 3,
            'drop_seed': 4,
            'verbose': -1,
            'keep_training_booster': False
        }
    ],
    'CAT': [
        {
            'iterations': 1000,
            'learning_rate': 0.1,
            'depth': 6,
            'l2_leaf_reg': 3.0,
            'bootstrap_type': 'Bayesian',
            'random_strength': 1.0,
            'bagging_temperature': 1.0,
            'od_type': 'Iter',
            'od_wait': 20,
            'verbose': False
        }
    ],
    'XGB': [
        {
            'n_estimators': 1000,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'reg_alpha': 0.0,
            'reg_lambda': 1.0,
            'random_state': 0
        }
    ]
}

# Настройки ресурсов
ag_args_fit = {
    'num_cpus': 8,
    'num_gpus': 1,
    'memory_limit': 16,
    'time_limit': 3600
}

# Обучение с полной конфигурацией
predictor.fit(
    train_data,
    hyperparameters=advanced_hyperparameters,
    num_bag_folds=5,
    num_bag_sets=2,
    num_stack_levels=1,
    ag_args_fit=ag_args_fit,
    presets='best_quality',
    time_limit=3600,
    holdout_frac=0.2,
    verbosity=2
)
```

## Следующие шаги

После освоения продвинутой конфигурации переходите к:
- [Работе с метриками](./04_metrics.md)
- [Методам валидации](./05_validation.md)
- [Продакшен деплою](./06_production.md)
