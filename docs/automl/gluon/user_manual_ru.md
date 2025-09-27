# Руководство пользователя по интеграции AutoGluon

## 📋 Содержание

1. [Обзор](#обзор)
2. [Установка](#установка)
3. [Быстрый старт](#быстрый-старт)
4. [Конфигурация](#конфигурация)
5. [Загрузка данных](#загрузка-данных)
6. [Обучение моделей](#обучение-моделей)
7. [Оценка моделей](#оценка-моделей)
8. [Деплой моделей](#деплой-моделей)
9. [Продвинутое использование](#продвинутое-использование)
10. [Устранение неполадок](#устранение-неполадок)

## 🎯 Обзор

Интеграция AutoGluon предоставляет комплексное решение для создания робастных и прибыльных ML моделей для торговых стратегий. Она использует мощные возможности AutoML AutoGluon, предоставляя специализированные функции для анализа финансовых данных.

### Ключевые возможности

- **Универсальная загрузка данных**: Поддержка форматов Parquet, CSV, JSON, Excel и HDF5
- **Обработка временных рядов**: Правильное хронологическое разделение train/validation/test
- **Архитектура AutoGluon-First**: Минимальная обертка, максимальное использование AutoGluon
- **Анализ Value Scores**: Торговые метрики (Profit Factor, Sharpe Ratio и др.)
- **Деплой моделей**: Экспорт для walk forward и Monte Carlo анализа
- **Мониторинг дрифта**: Автоматическое обнаружение дрифта моделей
- **Автоматическое переобучение**: Планируемое и дрифт-триггерное переобучение

## 🚀 Установка

### Предварительные требования

```bash
# Установка AutoGluon
uv add autogluon.tabular

# Установка дополнительных зависимостей
uv add openpyxl
```

### Проверка установки

```python
from src.automl.gluon import GluonAutoML

# Тест базовой функциональности
gluon = GluonAutoML()
print("✅ Интеграция AutoGluon готова!")
```

## ⚡ Быстрый старт

### Базовое использование

```python
from src.automl.gluon import GluonAutoML
import pandas as pd

# Инициализация AutoGluon
gluon = GluonAutoML()

# Загрузка данных из любого места в папке data/
data = gluon.load_data("data/cache/csv_converted/")

# Создание временного разделения
train, val, test = gluon.create_time_series_split(
    data, 
    target_column="target",
    train_ratio=0.6,
    val_ratio=0.2,
    test_ratio=0.2
)

# Обучение моделей
model = gluon.train_models(train, "target", val)

# Создание предсказаний
predictions = gluon.predict(model, test)
probabilities = gluon.predict_proba(model, test)

# Оценка моделей
evaluation = gluon.evaluate_models(model, test, "target")

# Анализ value scores
value_scores = gluon.analyze_value_scores(predictions, test["target"])

print(f"Точность модели: {evaluation['accuracy']:.3f}")
print(f"Profit factor: {value_scores['profit_factor']:.3f}")
```

## ⚙️ Конфигурация

### Конфигурация Gluon

Отредактируйте `src/automl/gluon/config/gluon_config.yaml`:

```yaml
# Настройки AutoGluon
presets: 'best_quality'  # Варианты: 'best_quality', 'high_quality', 'good_quality', 'medium_quality', 'fast_inference'
time_limit: 3600  # Лимит времени обучения в секундах
eval_metric: 'roc_auc'  # Метрика оценки
verbosity: 2  # Уровень логирования (0-4)

# Гиперпараметры (опционально)
hyperparameters:
  GBM: {}
  XGB: {}
  RF: {}
  NN_TORCH: {}
  FASTAI: {}

# Настройки ансамбля
num_bag_folds: 0
num_bag_sets: 1
num_stack_levels: 0
auto_stack: false
refit_full: true
save_space: false
```

### Конфигурация эксперимента

```python
from src.automl.gluon.config import ExperimentConfig

# Создание конфигурации эксперимента
experiment_config = ExperimentConfig({
    'experiment_name': 'trading_strategy_v1',
    'target_column': 'target',
    'problem_type': 'binary',  # 'binary', 'multiclass', 'regression'
    'time_limit': 1800,  # 30 минут
    'presets': 'high_quality'
})

# Инициализация с пользовательской конфигурацией
gluon = GluonAutoML(experiment_config=experiment_config)
```

### Конфигурация пользовательских признаков

Отредактируйте `src/automl/gluon/config/custom_features_config.yaml`:

```yaml
custom_features:
  - name: "SCHR_Trend_Direction"
    type: "categorical_prediction"
    description: "Вероятность тренда up/down/hold на основе SCHR Levels"
    
  - name: "Levels_Yellow_Breakout_Up"
    type: "binary_prediction"
    description: "Вероятность пробоя желтой линии вверх или отскока"
    
  - name: "Wave_Signal_5_Candles"
    type: "binary_prediction"
    description: "Если Signal=1, вероятность 5 свечей вверх или разворота"
    
  # Добавьте больше пользовательских признаков по необходимости
```

## 📊 Загрузка данных

### Поддерживаемые форматы

- **Parquet**: файлы `.parquet`
- **CSV**: файлы `.csv`
- **JSON**: файлы `.json`
- **Excel**: файлы `.xlsx`, `.xls`
- **HDF5**: файлы `.hdf5`, `.h5`

### Загрузка из разных источников

```python
# Загрузка из конкретного файла
data = gluon.load_data("data/cache/csv_converted/CSVExport.parquet")

# Загрузка из папки (рекурсивно)
data = gluon.load_data("data/indicators/")

# Загрузка из нескольких источников
data1 = gluon.load_data("data/cache/csv_converted/")
data2 = gluon.load_data("data/indicators/csv/")
combined_data = pd.concat([data1, data2], ignore_index=True)
```

### Валидация данных

```python
# Проверка качества данных
summary = gluon.data_loader.get_data_summary(data)
print(f"Размер данных: {summary['shape']}")
print(f"Пропущенные значения: {summary['missing_values']}")
print(f"Проблемы качества: {summary['quality_issues']}")
print(f"Готово для AutoGluon: {summary['is_ready_for_gluon']}")
```

## 🤖 Обучение моделей

### Базовое обучение

```python
# Обучение с настройками по умолчанию
model = gluon.train_models(train_data, "target")

# Обучение с валидационными данными
model = gluon.train_models(train_data, "target", validation_data=val_data)

# Обучение с пользовательской конфигурацией
experiment_config = ExperimentConfig({
    'target_column': 'target',
    'problem_type': 'binary',
    'time_limit': 1800,
    'presets': 'high_quality'
})
gluon = GluonAutoML(experiment_config=experiment_config)
model = gluon.train_models(train_data, "target")
```

### Продвинутые опции обучения

```python
# Пользовательские гиперпараметры
gluon_config = GluonConfig()
gluon_config.set('hyperparameters', {
    'GBM': {'num_leaves': 31, 'learning_rate': 0.05},
    'XGB': {'max_depth': 6, 'learning_rate': 0.1},
    'RF': {'n_estimators': 100, 'max_depth': 10}
})

# Настройки ансамбля
gluon_config.set('num_bag_folds', 5)
gluon_config.set('num_stack_levels', 2)
gluon_config.set('auto_stack', True)

gluon = GluonAutoML(gluon_config_path='custom_config.yaml')
model = gluon.train_models(train_data, "target")
```

## 📈 Оценка моделей

### Базовая оценка

```python
# Оценка производительности модели
evaluation = gluon.evaluate_models(model, test_data, "target")

print(f"Точность: {evaluation['accuracy']:.3f}")
print(f"ROC AUC: {evaluation['roc_auc']:.3f}")
print(f"Precision: {evaluation['precision']:.3f}")
print(f"Recall: {evaluation['recall']:.3f}")
```

### Анализ Value Scores

```python
# Анализ торговых метрик
predictions = gluon.predict(model, test_data)
probabilities = gluon.predict_proba(model, test_data)

value_scores = gluon.analyze_value_scores(
    predictions, 
    test_data["target"],
    returns=test_data["returns"],  # Опционально: фактические доходности
    trade_signals=test_data["signals"]  # Опционально: торговые сигналы
)

print(f"Profit Factor: {value_scores['profit_factor']:.3f}")
print(f"Sharpe Ratio: {value_scores['sharpe_ratio']:.3f}")
print(f"Max Drawdown: {value_scores['max_drawdown']:.3f}")
print(f"Win Rate: {value_scores['win_rate']:.3f}")
```

### Информация о модели

```python
# Получение лидерборда моделей
leaderboard = model.leaderboard()
print(leaderboard)

# Получение важности признаков
importance = model.feature_importance()
print(importance)

# Получение информации о модели
info = model.get_model_info()
print(f"Лучшая модель: {info['best_model']}")
print(f"Тип модели: {info['model_type']}")
```

## 🚀 Деплой моделей

### Экспорт для Walk Forward анализа

```python
# Экспорт модели для walk forward анализа
export_paths = gluon.export_models(model, "models/walk_forward/")

print(f"Модель экспортирована в: {export_paths['model_path']}")
print(f"Метаданные: {export_paths['metadata_path']}")
print(f"Конфигурация: {export_paths['config_path']}")
```

### Экспорт для Monte Carlo анализа

```python
# Экспорт модели для Monte Carlo анализа
export_paths = gluon.export_models(model, "models/monte_carlo/")

print(f"Модель экспортирована в: {export_paths['model_path']}")
print(f"Поддерживает вероятности: {export_paths['supports_probability']}")
```

### Полный пакет деплоя

```python
# Создание полного пакета деплоя
deployment_paths = gluon.export_models(model, "models/deployment/")

print(f"Модель: {deployment_paths['model_path']}")
print(f"Требования: {deployment_paths['requirements_path']}")
print(f"README: {deployment_paths['readme_path']}")
```

## 🔄 Переобучение моделей

### Автоматическое переобучение

```python
# Проверка необходимости переобучения
should_retrain = gluon.retrainer.should_retrain(
    baseline_performance=0.85,
    current_performance=0.82,
    new_data_size=1000
)

if should_retrain:
    print("Рекомендуется переобучение")
    
    # Переобучение модели
    new_model = gluon.retrain_model(model, new_data, "target")
    print("Модель переобучена успешно")
```

### Мониторинг дрифта

```python
# Мониторинг дрифта данных
drift_results = gluon.monitor_drift(model, current_data, reference_data)

if drift_results['overall_drift_alert']:
    print("Обнаружен дрифт данных!")
    for feature, result in drift_results.items():
        if isinstance(result, dict) and result.get('drift_detected'):
            print(f"Дрифт в {feature}: PSI = {result['psi']:.3f}")
```

## 🔧 Продвинутое использование

### Пользовательская инженерия признаков

```python
# Добавление пользовательских признаков перед обучением
def add_custom_features(df):
    # Пример: добавление технических индикаторов
    df['rsi'] = calculate_rsi(df['close'])
    df['sma_20'] = df['close'].rolling(20).mean()
    df['price_change'] = df['close'].pct_change()
    return df

# Применение пользовательских признаков
train_data = add_custom_features(train_data)
val_data = add_custom_features(val_data)
test_data = add_custom_features(test_data)

# Обучение с пользовательскими признаками
model = gluon.train_models(train_data, "target")
```

### Оптимизация гиперпараметров

```python
# Пользовательский поиск гиперпараметров
gluon_config = GluonConfig()
gluon_config.set('hyperparameters', {
    'GBM': {
        'num_leaves': [31, 63, 127],
        'learning_rate': [0.01, 0.05, 0.1],
        'feature_fraction': [0.8, 0.9, 1.0]
    },
    'XGB': {
        'max_depth': [4, 6, 8],
        'learning_rate': [0.05, 0.1, 0.2],
        'subsample': [0.8, 0.9, 1.0]
    }
})

gluon = GluonAutoML(gluon_config_path='custom_config.yaml')
model = gluon.train_models(train_data, "target")
```

### Ансамбль моделей

```python
# Настройка параметров ансамбля
gluon_config = GluonConfig()
gluon_config.set('num_bag_folds', 5)
gluon_config.set('num_stack_levels', 2)
gluon_config.set('auto_stack', True)
gluon_config.set('refit_full', True)

gluon = GluonAutoML(gluon_config_path='ensemble_config.yaml')
model = gluon.train_models(train_data, "target")
```

## 🐛 Устранение неполадок

### Частые проблемы

#### 1. Ошибки импорта

```python
# Если возникают ошибки импорта, проверьте установку
try:
    from autogluon.tabular import TabularPredictor
    print("✅ AutoGluon установлен корректно")
except ImportError:
    print("❌ AutoGluon не установлен. Выполните: uv add autogluon.tabular")
```

#### 2. Проблемы с памятью

```python
# Для больших наборов данных используйте эффективные настройки памяти
gluon_config = GluonConfig()
gluon_config.set('save_space', True)
gluon_config.set('num_bag_folds', 0)  # Отключить bagging для экономии памяти
gluon_config.set('time_limit', 1800)  # Ограничить время обучения
```

#### 3. Проблемы качества данных

```python
# Проверьте качество данных перед обучением
summary = gluon.data_loader.get_data_summary(data)

if not summary['is_ready_for_gluon']:
    print("Обнаружены проблемы качества данных:")
    for issue in summary['quality_issues']:
        print(f"- {issue}")
    
    # Очистка данных
    cleaned_data = gluon.data_loader.clean_data(data)
    summary = gluon.data_loader.get_data_summary(cleaned_data)
```

#### 4. Проблемы производительности модели

```python
# Если производительность модели низкая, попробуйте:
# 1. Увеличить время обучения
gluon_config.set('time_limit', 3600)  # 1 час

# 2. Использовать пресеты более высокого качества
gluon_config.set('presets', 'best_quality')

# 3. Добавить больше данных
# 4. Проверить инженерию признаков
# 5. Проверить качество целевой переменной
```

### Оптимизация производительности

```python
# Для быстрого вывода
gluon_config = GluonConfig()
gluon_config.set('presets', 'fast_inference')
gluon_config.set('save_space', True)

# Для лучшей точности
gluon_config.set('presets', 'best_quality')
gluon_config.set('time_limit', 7200)  # 2 часа
gluon_config.set('num_bag_folds', 5)
gluon_config.set('auto_stack', True)
```

### Логирование и отладка

```python
# Включить детальное логирование
import logging
logging.basicConfig(level=logging.DEBUG)

# Проверить прогресс обучения модели
gluon_config.set('verbosity', 4)  # Максимальная детализация
gluon = GluonAutoML(gluon_config_path='debug_config.yaml')
model = gluon.train_models(train_data, "target")
```

## 📚 Примеры

### Полный пример торговой стратегии

```python
from src.automl.gluon import GluonAutoML
import pandas as pd

# Инициализация AutoGluon
gluon = GluonAutoML()

# Загрузка торговых данных
data = gluon.load_data("data/cache/csv_converted/")

# Создание временного разделения
train, val, test = gluon.create_time_series_split(
    data, 
    target_column="target",
    train_ratio=0.6,
    val_ratio=0.2,
    test_ratio=0.2
)

# Обучение модели
model = gluon.train_models(train, "target", val)

# Оценка на тестовом наборе
evaluation = gluon.evaluate_models(model, test, "target")
print(f"Точность на тесте: {evaluation['accuracy']:.3f}")

# Анализ value scores
predictions = gluon.predict(model, test)
value_scores = gluon.analyze_value_scores(predictions, test["target"])
print(f"Profit factor: {value_scores['profit_factor']:.3f}")

# Экспорт для продакшена
export_paths = gluon.export_models(model, "models/production/")
print(f"Модель готова для продакшена: {export_paths['model_path']}")
```

## 📞 Поддержка

Для дополнительной поддержки и примеров обращайтесь к:

- **Документация**: `docs/automl/gluon/`
- **Примеры**: `src/automl/gluon/examples/`
- **Конфигурация**: `src/automl/gluon/config/`
- **Тесты**: `src/automl/gluon/tests/`

## 🎯 Лучшие практики

1. **Всегда используйте временное разделение** для финансовых данных
2. **Регулярно мониторьте дрифт данных**
3. **Используйте подходящие пресеты** для вашего случая использования
4. **Проверяйте качество данных** перед обучением
5. **Экспортируйте модели** для продакшен использования
6. **Мониторьте производительность модели** со временем
7. **Переобучайте модели** при обнаружении дрифта
8. **Используйте value scores** для оценки торговых стратегий
