# Базовое использование AutoML Gluon

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему начинаем с базового использования

**Почему 80% пользователей начинают с базового использования?** Потому что это самый простой способ понять, как работает AutoML Gluon. Это как обучение вождению - сначала изучаете основы, потом переходите к сложным маневрам.

### Что дает базовое понимание?
- **Быстрый старт**: От данных до модели за несколько строк кода
- **Понимание принципов**: Как AutoML Gluon принимает решения
- **Уверенность**: Знание того, что все работает правильно
- **Фундамент**: Основа для изучения продвинутых техник

### Что происходит без базового понимания?
- **Фрустрация**: Не понимаете, почему модель работает не так
- **Ошибки**: Неправильное использование параметров
- **Неэффективность**: Тратите время на то, что можно сделать проще
- **Разочарование**: Сложность отпугивает от изучения

## Введение в TabularPredictor

![Архитектура AutoML Gluon](images/architecture_diagram.png)
*Рисунок 2: Архитектура AutoML Gluon с основными компонентами*

**Почему TabularPredictor - это сердце AutoML Gluon?** Потому что он объединяет все возможности в одном простом интерфейсе. Это как универсальный пульт управления - одна кнопка запускает сложные процессы.

`TabularPredictor` - это основной класс для работы с табличными данными в AutoGluon. Он автоматически определяет тип задачи (классификация, регрессия) и выбирает лучшие алгоритмы.

### Почему TabularPredictor так важен?
- **Автоматизация**: Не нужно выбирать алгоритмы вручную
- **Умность**: Сам определяет тип задачи и метрики
- **Гибкость**: Работает с любыми табличными данными
- **Простота**: Один класс решает все задачи

### Импорт и создание базового предиктора

**Почему начинаем с импорта?** Потому что это основа любого Python проекта. Правильный импорт - это как правильная настройка инструмента.

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np
```

**Почему именно эти импорты?**
- `TabularPredictor` - основной класс для работы с табличными данными
- `pandas` - для работы с данными в табличном формате
- `numpy` - для численных вычислений

**Почему не импортируем все сразу?** Потому что это замедляет загрузку и может вызвать конфликты.

```python
# Создание предиктора
predictor = TabularPredictor(
    label='target_column',  # Название целевой переменной
    problem_type='auto',    # Автоматическое определение типа задачи
    eval_metric='auto'      # Автоматический выбор метрики
)
```

**Объяснение параметров:**
- `label='target_column'` - название столбца с целевой переменной (что мы предсказываем)
- `problem_type='auto'` - AutoML Gluon сам определит, классификация это или регрессия
- `eval_metric='auto'` - автоматический выбор лучшей метрики для оценки

**Почему используем 'auto'?** Потому что AutoML Gluon умнее нас в выборе оптимальных параметров.

## Типы задач

**Почему важно понимать типы задач?** Потому что разные задачи требуют разных подходов. Это как разница между диагностикой болезни и измерением температуры - методы разные.

### Классификация

**Что такое классификация?** Это предсказание категории или класса. Например, спам/не спам, больной/здоровый, покупатель/не покупатель.

**Почему классификация так популярна?** Потому что большинство бизнес-задач - это классификация:
- Обнаружение мошенничества
- Медицинская диагностика
- Рекомендательные системы
- Анализ настроений

```python
# Бинарная классификация
predictor = TabularPredictor(
    label='is_fraud',
    problem_type='binary',
    eval_metric='accuracy'
)
```
**Почему бинарная классификация проще?** Потому что есть только два варианта ответа - да или нет.

```python
# Многоклассовая классификация
predictor = TabularPredictor(
    label='category',
    problem_type='multiclass',
    eval_metric='accuracy'
)
```
**Почему многоклассовая сложнее?** Потому что нужно выбрать из множества вариантов, и ошибки более дорогие.

### Регрессия

**Что такое регрессия?** Это предсказание численного значения. Например, цена дома, количество продаж, время до события.

**Почему регрессия важна?** Потому что многие бизнес-метрики - это числа:
- Прогнозирование продаж
- Оценка недвижимости
- Предсказание времени
- Финансовое моделирование

```python
# Регрессия
predictor = TabularPredictor(
    label='price',
    problem_type='regression',
    eval_metric='rmse'
)
```

## Обучение модели

### Базовое обучение

```python
# Загрузка данных
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# Обучение модели
predictor.fit(train_data)

# Предсказания
predictions = predictor.predict(test_data)
```

### Обучение с ограничением времени

```python
# Обучение с ограничением времени (в секундах)
predictor.fit(
    train_data,
    time_limit=3600  # 1 час
)

# Обучение с ограничением памяти
predictor.fit(
    train_data,
    memory_limit=8  # 8GB RAM
)
```

### Обучение с пресетами

```python
# Различные пресеты качества
presets = [
    'best_quality',      # Лучшее качество (долго)
    'high_quality',      # Высокое качество
    'good_quality',      # Хорошее качество
    'medium_quality',    # Среднее качество
    'optimize_for_deployment'  # Оптимизация для деплоя
]

predictor.fit(
    train_data,
    presets='high_quality',
    time_limit=1800  # 30 минут
)
```

## Оценка качества модели

### Базовые метрики

```python
# Оценка на тестовых данных
performance = predictor.evaluate(test_data)
print(f"Model performance: {performance}")

# Получение детального отчета
performance = predictor.evaluate(
    test_data,
    detailed_report=True
)
```

### Валидация

```python
# Holdout валидация
predictor.fit(
    train_data,
    holdout_frac=0.2  # 20% данных для валидации
)

# K-fold кросс-валидация
predictor.fit(
    train_data,
    num_bag_folds=5,  # 5-fold CV
    num_bag_sets=1
)
```

## Предсказания

### Базовые предсказания

```python
# Предсказания классов/значений
predictions = predictor.predict(test_data)

# Вероятности (для классификации)
probabilities = predictor.predict_proba(test_data)
```

### Предсказания с дополнительной информацией

```python
# Предсказания с доверительными интервалами
predictions_with_intervals = predictor.predict(
    test_data,
    include_confidence=True
)

# Предсказания от отдельных моделей
individual_predictions = predictor.predict_multi(test_data)
```

## Работа с признаками

### Автоматическая обработка признаков

```python
# AutoGluon автоматически обрабатывает:
# - Категориальные переменные (one-hot encoding, label encoding)
# - Пропущенные значения (заполнение, индикаторы)
# - Числовые переменные (нормализация, масштабирование)
# - Текстовые переменные (TF-IDF, embeddings)
```

### Ручная настройка признаков

```python
from autogluon.features import FeatureGenerator

# Создание генератора признаков
feature_generator = FeatureGenerator(
    enable_nan_handling=True,
    enable_categorical_encoding=True,
    enable_text_special_features=True,
    enable_text_ngram_features=True
)

# Применение к данным
train_data_processed = feature_generator.fit_transform(train_data)
test_data_processed = feature_generator.transform(test_data)
```

## Сохранение и загрузка моделей

### Сохранение модели

```python
# Сохранение модели
predictor.save('my_model')

# Сохранение с дополнительной информацией
predictor.save(
    'my_model',
    save_space=True,  # Экономия места
    save_info=True   # Сохранение метаданных
)
```

### Загрузка модели

```python
# Загрузка сохраненной модели
predictor = TabularPredictor.load('my_model')

# Загрузка с проверкой совместимости
predictor = TabularPredictor.load(
    'my_model',
    require_version_match=True
)
```

## Работа с ансамблями

### Настройка ансамбля

```python
# Обучение с ансамблем
predictor.fit(
    train_data,
    num_bag_folds=5,      # Количество фолдов для бэггинга
    num_bag_sets=2,       # Количество наборов бэггинга
    num_stack_levels=1    # Уровни стекинга
)
```

### Анализ ансамбля

```python
# Информация о моделях в ансамбле
leaderboard = predictor.leaderboard()
print(leaderboard)

# Детальная информация о производительности
leaderboard = predictor.leaderboard(
    test_data,
    extra_info=True,
    silent=False
)
```

## Продвинутые настройки

### Настройка гиперпараметров

```python
# Словарь с настройками для разных алгоритмов
hyperparameters = {
    'GBM': [
        {'num_boost_round': 100, 'num_leaves': 31},
        {'num_boost_round': 200, 'num_leaves': 63}
    ],
    'CAT': [
        {'iterations': 100, 'learning_rate': 0.1},
        {'iterations': 200, 'learning_rate': 0.05}
    ],
    'XGB': [
        {'n_estimators': 100, 'max_depth': 6},
        {'n_estimators': 200, 'max_depth': 8}
    ]
}

predictor.fit(
    train_data,
    hyperparameters=hyperparameters
)
```

### Исключение алгоритмов

```python
# Исключение определенных алгоритмов
excluded_model_types = ['KNN', 'NN_TORCH']

predictor.fit(
    train_data,
    excluded_model_types=excluded_model_types
)
```

### Настройка валидации

```python
# Настройка стратегии валидации
from autogluon.tabular.models import AbstractModel

class CustomValidationStrategy(AbstractModel):
    def _get_default_resources(self):
        return {'num_cpus': 2, 'num_gpus': 0}

predictor.fit(
    train_data,
    validation_strategy='custom',
    custom_validation_strategy=CustomValidationStrategy()
)
```

## Работа с различными типами данных

### Категориальные данные

```python
# AutoGluon автоматически определяет категориальные переменные
# Но можно указать их явно
categorical_columns = ['category', 'brand', 'region']

predictor.fit(
    train_data,
    categorical_columns=categorical_columns
)
```

### Текстовые данные

```python
# Для текстовых колонок AutoGluon автоматически создает признаки
text_columns = ['description', 'review_text']

predictor.fit(
    train_data,
    text_columns=text_columns
)
```

### Временные данные

```python
# Указание временных колонок
time_columns = ['date', 'timestamp']

predictor.fit(
    train_data,
    time_columns=time_columns
)
```

## Мониторинг обучения

### Логирование

```python
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Обучение с подробным логированием
predictor.fit(
    train_data,
    verbosity=2  # Подробное логирование
)
```

### Callback функции

```python
def training_callback(model_name, model_path, model_info):
    """Callback функция для мониторинга обучения"""
    print(f"Training {model_name}...")
    print(f"Model path: {model_path}")
    print(f"Model info: {model_info}")

predictor.fit(
    train_data,
    callbacks=[training_callback]
)
```

## Примеры использования

### Полный пример классификации

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Создание синтетических данных
X, y = make_classification(
    n_samples=10000,
    n_features=20,
    n_informative=15,
    n_redundant=5,
    n_classes=2,
    random_state=42
)

# Создание DataFrame
data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
data['target'] = y

# Разделение на train/test
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Создание и обучение предиктора
predictor = TabularPredictor(
    label='target',
    problem_type='binary',
    eval_metric='accuracy'
)

# Обучение
predictor.fit(
    train_data,
    time_limit=300,  # 5 минут
    presets='medium_quality'
)

# Предсказания
predictions = predictor.predict(test_data)
probabilities = predictor.predict_proba(test_data)

# Оценка качества
performance = predictor.evaluate(test_data)
print(f"Accuracy: {performance['accuracy']}")

# Анализ лидерборда
leaderboard = predictor.leaderboard()
print(leaderboard)
```

### Полный пример регрессии

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

# Создание синтетических данных
X, y = make_regression(
    n_samples=10000,
    n_features=20,
    n_informative=15,
    noise=0.1,
    random_state=42
)

# Создание DataFrame
data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
data['target'] = y

# Разделение на train/test
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Создание и обучение предиктора
predictor = TabularPredictor(
    label='target',
    problem_type='regression',
    eval_metric='rmse'
)

# Обучение
predictor.fit(
    train_data,
    time_limit=300,  # 5 минут
    presets='high_quality'
)

# Предсказания
predictions = predictor.predict(test_data)

# Оценка качества
performance = predictor.evaluate(test_data)
print(f"RMSE: {performance['rmse']}")
print(f"MAE: {performance['mae']}")

# Анализ важности признаков
feature_importance = predictor.feature_importance()
print(feature_importance)
```

## Лучшие практики

### Подготовка данных

```python
# 1. Проверка качества данных
print("Data shape:", train_data.shape)
print("Missing values:", train_data.isnull().sum().sum())
print("Data types:", train_data.dtypes.value_counts())

# 2. Обработка пропущенных значений
train_data = train_data.dropna()  # Или заполнение

# 3. Удаление константных признаков
constant_columns = train_data.columns[train_data.nunique() <= 1]
train_data = train_data.drop(columns=constant_columns)
```

### Выбор метрик

```python
# Для классификации
classification_metrics = [
    'accuracy', 'balanced_accuracy', 'f1', 'f1_macro', 'f1_micro',
    'precision', 'precision_macro', 'recall', 'recall_macro',
    'roc_auc', 'log_loss'
]

# Для регрессии
regression_metrics = [
    'rmse', 'mae', 'mape', 'smape', 'r2', 'pearsonr', 'spearmanr'
]
```

### Оптимизация времени обучения

```python
# Быстрое обучение для экспериментов
predictor.fit(
    train_data,
    time_limit=60,  # 1 минута
    presets='optimize_for_deployment'
)

# Качественное обучение для финальной модели
predictor.fit(
    train_data,
    time_limit=3600,  # 1 час
    presets='best_quality'
)
```

## Следующие шаги

После освоения базового использования переходите к:
- [Продвинутой конфигурации](./03_advanced_configuration.md)
- [Работе с метриками](./04_metrics.md)
- [Методам валидации](./05_validation.md)
