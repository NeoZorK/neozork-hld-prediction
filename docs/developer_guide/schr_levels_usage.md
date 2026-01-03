# SCHR Levels AutoML - guide on использованию

## 🎯 Обзор

SCHR Levels AutoML - это автоматизированный пайплайн машинного обучения for analysis данных SCHR Levels indicators. Пайплайн Solves 3 main tasks предсказания:

1. **`pressure_vector_sign`** - Prediction sign PRESSURE_VECTOR (положительный/отрицательный)
2. **`price_direction_5periods`** - Prediction price direction for 5 periods вперед
3. **`level_breakout`** - Prediction пробоя уровней PREDICTED_HIGH/PREDICTED_LOW

## 🚀 quick start

### 1. Простой тест
```bash
cd /Users/rostsh/Documents/DIS/REPO/neozork-hld-Prediction
uv run python test_schr_pipeline.py
```

### 2. Полный анализ
```bash
uv run python schr-levels-gluon.py
```

## 📊 Результаты последнего анализа

### Модель 1: pressure_vector_sign
- **Точность**: 61.76%
- **Precision**: 68.68%
- **Recall**: 61.76%
- **F1-score**: 56.23%
- **Walk Forward**: 61.90% ± 13.61%
- **Monte Carlo**: 63.57% ± 10.14%
- **Стабильность**: 84.05%

### Модель 2: price_direction_5periods
- **Точность**: 14.71%
- **Precision**: 2.16%
- **Recall**: 14.71%
- **F1-score**: 3.77%
- **Walk Forward**: 28.57% ± 7.01%
- **Monte Carlo**: 35.35% ± 16.40%
- **Стабильность**: 53.60%

### Модель 3: level_breakout
- **Точность**: 67.65%
- **Precision**: 68.26%
- **Recall**: 67.65%
- **F1-score**: 67.66%
- **Walk Forward**: 63.49% ± 2.24%
- **Monte Carlo**: 52.80% ± 12.09%
- **Стабильность**: 77.10%

## 🔧 Использование in коде

### Базовое использование
```python
from schr_levels_gluon import SCHRLevelsAutoMLPipeline

# Создаем пайплайн
pipeline = SCHRLevelsAutoMLPipeline()

# Загружаем данные
data = pipeline.load_schr_data('BTCUSD', 'MN1')

# Создаем целевые переменные
data = pipeline.create_target_variables(data)

# Создаем признаки
data = pipeline.create_features(data)

# Обучаем модель
results = pipeline.train_model(data, 'pressure_vector_sign')
print(f"Точность: {results['metrics']['accuracy']:.2%}")

# Делаем Prediction
Prediction = pipeline.predict(data.tail(1), 'pressure_vector_sign')
print(f"Prediction: {Prediction.iloc[0]}")
```

### Предсказания for trading
```python
# Детальные предсказания with вероятностями
trading_pred = pipeline.predict_for_trading(data.tail(1), 'pressure_vector_sign')
print(f"Prediction: {trading_pred['Predictions'].iloc[0]}")
print(f"Вероятности: {trading_pred['probabilities'].iloc[0].to_dict()}")
```

### Валидация моделей
```python
# Walk Forward валидация
wf_results = pipeline.walk_forward_validation(data, 'pressure_vector_sign', n_splits=5)
print(f"Средняя точность: {wf_results['mean_accuracy']:.2%}")

# Monte Carlo валидация
mc_results = pipeline.monte_carlo_validation(data, 'pressure_vector_sign', n_iterations=10)
print(f"Средняя точность: {mc_results['mean_accuracy']:.2%}")
```

## 📁 Структура файлов

```
models/schr_levels_production/
├── pressure_vector_sign_model.pkl # Модель for предсказания sign PRESSURE_VECTOR
├── price_direction_5periods_model.pkl # Модель for предсказания price direction
├── level_breakout_model.pkl # Модель for предсказания пробоя уровней
└── analysis_results.pkl # Результаты анализа

logs/
└── schr_levels_*.log # Логи работы пайплайна

results/
└── plots/ # Графики and визуализации
```

## 🎯 Доступные данные

### Символы
- BTCUSD, GBPUSD, EURUSD, and другие

### Timeframeы
- MN1 (месячные), W1 (недельные), D1 (дневные)
- H4 (4-часовые), H1 (часовые)
- M15 (15-minutesные), M5 (5-minutesные), M1 (minutesные)

### Загрузка разных данных
```python
# Разные символы
data_btc = pipeline.load_schr_data('BTCUSD', 'MN1')
data_gbp = pipeline.load_schr_data('GBPUSD', 'MN1')

# Разные Timeframeы
data_daily = pipeline.load_schr_data('BTCUSD', 'D1')
data_hourly = pipeline.load_schr_data('BTCUSD', 'H4')
```

## ⚙️ configuration параметров

### Время обучения
```python
# Быстрое обучение (5 minutes)
results = pipeline.train_model(data, 'pressure_vector_sign', time_limit=300)

# Качественное обучение (30 minutes)
results = pipeline.train_model(data, 'pressure_vector_sign', time_limit=1800)
```

### Исключение моделей
```python
# in файле schr-levels-gluon.py можно настроить:
fit_args = {
 'excluded_model_types': ['NN_TORCH', 'FASTAI'], # Исключить нейронные сети
 'use_gpu': False, # Отключить GPU
 'num_gpus': 0
}
```

## 🔍 Анализ результатов

### check качества данных
```python
# Статистика on целевым переменным
print("Распределение target_pv_sign:")
print(data['target_pv_sign'].value_counts())

print("Распределение target_price_direction:")
print(data['target_price_direction'].value_counts())
```

### Важность признаков
```python
# Получить важность признаков
feature_importance = pipeline.get_feature_importance('pressure_vector_sign')
print(feature_importance.head(10))
```

## 🚨 Устранение проблем

### Ошибка "No such file or directory"
```bash
# Проверьте наличие файлов данных
ls data/cache/csv_converted/
```

### Ошибка "Not enough data"
```python
# Проверьте размер данных
print(f"Размер данных: {len(data)} записей")
print(f"Колонки: {list(data.columns)}")
```

### Низкая точность модели
```python
# Попробуйте увеличить время обучения
results = pipeline.train_model(data, 'pressure_vector_sign', time_limit=3600) # 1 час
```

## 📈 examples использования

### Ежедневный анализ
```python
# Загружаем свежие данные
data = pipeline.load_schr_data('BTCUSD', 'D1')
data = pipeline.create_target_variables(data)
data = pipeline.create_features(data)

# Обучаем модель
results = pipeline.train_model(data, 'pressure_vector_sign')

# Делаем Prediction on завтра
tomorrow_Prediction = pipeline.predict(data.tail(1), 'pressure_vector_sign')
print(f"Завтра PRESSURE_VECTOR будет: {'положительным' if tomorrow_Prediction.iloc[0] == 1 else 'отрицательным'}")
```

### Анализ разных Timeframeов
```python
timeframes = ['MN1', 'W1', 'D1', 'H4']

for tf in timeframes:
 data = pipeline.load_schr_data('BTCUSD', tf)
 data = pipeline.create_target_variables(data)
 data = pipeline.create_features(data)

 results = pipeline.train_model(data, 'pressure_vector_sign')
 print(f"{tf}: Точность {results['metrics']['accuracy']:.2%}")
```

## 🎉 Готовые скрипты

### Быстрый тест
```bash
uv run python test_schr_pipeline.py
```

### Полный анализ
```bash
uv run python schr-levels-gluon.py
```

### Кастомный анализ
```python
# Создайте свой скрипт
from schr_levels_gluon import SCHRLevelsAutoMLPipeline

pipeline = SCHRLevelsAutoMLPipeline()
data = pipeline.load_schr_data('BTCUSD', 'MN1')
data = pipeline.create_target_variables(data)
data = pipeline.create_features(data)

# Обучаем все 3 модели
for task in ['pressure_vector_sign', 'price_direction_5periods', 'level_breakout']:
 results = pipeline.train_model(data, task)
 print(f"{task}: Точность {results['metrics']['accuracy']:.2%}")
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи in папке `logs/`
2. Убедитесь, что данные загружены корректно
3. Проверьте наличие всех зависимостей: `uv run pip list`

---

**Последнее update**: 28 сентября 2025
**Версия**: 1.0.0
