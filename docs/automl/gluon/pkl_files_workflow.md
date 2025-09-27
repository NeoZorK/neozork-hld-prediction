# Работа с .pkl файлами AutoGluon

## Обзор

AutoGluon создает множество .pkl файлов при обучении моделей. Этот документ объясняет, что с ними делать дальше.

## Структура .pkl файлов

```
models/autogluon/
├── learner.pkl          # Основной learner
├── trainer.pkl           # Trainer объект
└── models/
    ├── WeightedEnsemble_L2_FULL/
    │   └── model.pkl    # Лучшая модель
    ├── RandomForest_r127_BAG_L1/
    │   └── model.pkl    # Отдельная модель
    └── ...              # Другие модели
```

## Что делать с .pkl файлами

### 1. Backtesting (Бэктестинг)

```python
from src.automl.gluon.analysis.model_analysis import ModelAnalyzer

# Загрузить модель
analyzer = ModelAnalyzer("models/autogluon/")
analyzer.load_model()

# Выполнить бэктестинг
backtest_results = analyzer.backtest_analysis(
    data=test_data,
    target_column="target",
    start_date="2023-01-01",
    end_date="2023-12-31"
)
```

### 2. Walk Forward Analysis

```python
# Выполнить walk forward анализ
walk_forward_results = analyzer.walk_forward_analysis(
    data=historical_data,
    target_column="target",
    train_window=1000,
    test_window=100,
    step_size=50
)
```

### 3. Monte Carlo Analysis

```python
# Выполнить Monte Carlo анализ
monte_carlo_results = analyzer.monte_carlo_analysis(
    data=historical_data,
    target_column="target",
    n_simulations=1000,
    sample_size=500
)
```

### 4. Переобучение модели

```python
# Проверить необходимость переобучения
retrain_needed = analyzer.retrain_model(
    new_data=recent_data,
    target_column="target",
    retrain_threshold=0.05
)
```

## Рекомендации по использованию

### 1. Один файл за раз
- **Да, рекомендуется брать один файл за раз** для обучения
- Это обеспечивает лучшую производительность и контроль
- Можно использовать `single_file_analysis.py` для анализа одного файла

### 2. Управление моделями

```bash
# Архивировать старые модели
python examples/automl/gluon/model_management.py --archive --days 30

# Очистить неиспользуемые модели
python examples/automl/gluon/model_management.py --cleanup

# Проверить размер моделей
python examples/automl/gluon/model_management.py --size
```

### 3. Мониторинг дрифта

```python
from src.automl.gluon.deployment.drift_monitor import DriftMonitor

# Создать монитор дрифта
monitor = DriftMonitor()

# Проверить дрифт
drift_detected = monitor.check_drift(
    model_path="models/autogluon/",
    new_data=recent_data,
    threshold=0.1
)
```

## Конфигурация для 13 признаков

### 1. Использование конфигурации

```python
from src.automl.gluon.features.custom_feature_engineer import CustomFeatureEngineer

# Создать инженер признаков
engineer = CustomFeatureEngineer("src/automl/gluon/config/custom_features_config.yaml")

# Создать все 13 признаков
data_with_features = engineer.create_all_features(data)
```

### 2. Настройка признаков

Файл `custom_features_config.yaml` содержит:
- SCHR признаки (4 признака)
- Wave признаки (6 признаков)  
- Short3 признаки (3 признака)

### 3. Интеграция с AutoGluon

```python
# В основном workflow
gluon = GluonAutoML()

# Загрузить данные
data = gluon.load_data("data/cache/csv_converted/CSVExport_BTCUSD_PERIOD_D1.parquet")

# Создать 13 пользовательских признаков
data_with_features = gluon.create_custom_features(data, use_13_features=True)

# Обучить модель
gluon.train_models(data_with_features, "target")
```

## Лучшие практики

### 1. Управление памятью
- Модели могут быть большими (100MB+)
- Регулярно архивируйте старые модели
- Используйте `model_management.py` для автоматизации

### 2. Версионирование
- Сохраняйте модели с временными метками
- Ведите лог производительности моделей
- Документируйте изменения в данных

### 3. Мониторинг
- Отслеживайте дрифт модели
- Мониторьте производительность
- Настройте автоматическое переобучение

## Примеры использования

### Полный workflow с 13 признаками

```bash
# Запустить расширенный демо
python examples/automl/gluon/enhanced_workflow_demo.py
```

### Анализ одного файла

```bash
# Анализ одного файла
python examples/automl/gluon/single_file_analysis.py \
    data/cache/csv_converted/CSVExport_BTCUSD_PERIOD_D1.parquet \
    --analysis full \
    --output results/btc_analysis.json
```

### Управление моделями

```bash
# Архивировать модели старше 30 дней
python examples/automl/gluon/model_management.py --archive --days 30

# Очистить неиспользуемые модели
python examples/automl/gluon/model_management.py --cleanup
```

## Заключение

.pkl файлы AutoGluon - это мощный инструмент для:
- Бэктестинга торговых стратегий
- Walk forward анализа
- Monte Carlo симуляций
- Мониторинга дрифта модели
- Автоматического переобучения

Используйте предоставленные инструменты для эффективного управления моделями и получения максимальной прибыли от торговых стратегий.
