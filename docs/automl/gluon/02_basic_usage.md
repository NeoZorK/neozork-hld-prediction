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

<img src="images/optimized/architecture_diagram.png" alt="Архитектура AutoML Gluon" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
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

#### 🔧 Детальное описание параметров TabularPredictor

**Параметр `label`:**
- **Что означает**: Название столбца с целевой переменной (что мы предсказываем)
- **Зачем нужен**: Указывает AutoML Gluon, какую переменную предсказывать
- **Обязательный параметр**: Да, без него AutoML Gluon не знает, что предсказывать
- **Правила именования**:
  - **Латинские буквы**: `target`, `label`, `y`
  - **С подчеркиваниями**: `target_column`, `prediction_target`
  - **Избегать**: Пробелы, специальные символы, кириллицу
- **Практические примеры**:
  - **Классификация**: `'is_fraud'`, `'category'`, `'class'`
  - **Регрессия**: `'price'`, `'sales'`, `'temperature'`
  - **Временные ряды**: `'value'`, `'forecast'`, `'target'`
- **Проверка существования**: AutoML Gluon автоматически проверит, что столбец существует
- **Обработка ошибок**: Если столбец не найден, AutoML Gluon выдаст понятную ошибку

**Параметр `problem_type`:**
- **Что означает**: Тип задачи машинного обучения
- **Зачем нужен**: Определяет, какие алгоритмы и метрики использовать
- **Автоматическое определение**: `'auto'` - AutoML Gluon сам определит тип
- **Ручное указание**: Можно явно указать тип задачи
- **Доступные значения**:
  - **`'auto'`** - автоматическое определение (рекомендуется)
  - **`'binary'`** - бинарная классификация (2 класса)
  - **`'multiclass'`** - многоклассовая классификация (3+ классов)
  - **`'regression'`** - регрессия (предсказание чисел)
- **Как AutoML Gluon определяет тип**:
  - **Анализ данных**: Смотрит на уникальные значения в target
  - **Тип данных**: Проверяет, числа это или строки
  - **Количество классов**: Считает уникальные значения
- **Практические примеры**:
  - **2 уникальных значения**: `'binary'` (да/нет, спам/не спам)
  - **3+ уникальных значения**: `'multiclass'` (категории, классы)
  - **Много уникальных чисел**: `'regression'` (цены, температуры)
- **Преимущества автоматического определения**:
  - **Простота**: Не нужно думать о типе задачи
  - **Точность**: AutoML Gluon редко ошибается
  - **Гибкость**: Работает с любыми данными
- **Когда указывать вручную**:
  - **Специфические задачи**: Когда auto определение неправильное
  - **Оптимизация**: Когда знаете точный тип задачи
  - **Отладка**: Когда нужно контролировать процесс

**Параметр `eval_metric`:**
- **Что означает**: Метрика для оценки качества модели
- **Зачем нужен**: Определяет, как измерять качество модели
- **Автоматический выбор**: `'auto'` - AutoML Gluon выберет лучшую метрику
- **Ручное указание**: Можно явно указать метрику
- **Доступные метрики по типам задач**:
  - **Классификация**: `'accuracy'`, `'f1'`, `'roc_auc'`, `'precision'`, `'recall'`
  - **Регрессия**: `'rmse'`, `'mae'`, `'r2'`, `'mape'`
- **Как AutoML Gluon выбирает метрику**:
  - **Бинарная классификация**: `'roc_auc'` (лучше для несбалансированных данных)
  - **Многоклассовая классификация**: `'accuracy'` (простая и понятная)
  - **Регрессия**: `'rmse'` (стандартная метрика)
- **Практические примеры выбора метрики**:
  - **Медицинская диагностика**: `'roc_auc'` (важна точность)
  - **Рекомендации**: `'f1'` (баланс точности и полноты)
  - **Прогнозирование цен**: `'rmse'` (средняя ошибка)
  - **Анализ настроений**: `'accuracy'` (простота интерпретации)
- **Влияние на обучение**:
  - **Разные метрики**: Могут дать разные лучшие модели
  - **Оптимизация**: AutoML Gluon оптимизирует выбранную метрику
  - **Сравнение**: Можно сравнить модели по разным метрикам

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

#### 🔧 Детальное описание параметров метода fit()

**Параметр `time_limit`:**
- **Что означает**: Максимальное время обучения в секундах
- **Зачем нужен**: Контролирует время обучения, предотвращает бесконечное обучение
- **По умолчанию**: `None` (без ограничений)
- **Рекомендуемые значения**:
  - **Быстрые эксперименты**: `600` (10 минут)
  - **Стандартные задачи**: `3600` (1 час)
  - **Важные задачи**: `7200` (2 часа)
  - **Максимальное качество**: `14400` (4 часа)
- **Влияние на качество**:
  - **Короткое время**: Базовая точность, быстрые результаты
  - **Среднее время**: Хорошая точность, сбалансированный подход
  - **Длинное время**: Максимальная точность, лучшие модели
- **Оптимизация по ресурсам**:
  - **CPU только**: Увеличить время в 2-3 раза
  - **GPU доступна**: Уменьшить время в 2-3 раза
  - **Много ядер**: Уменьшить время на 30-50%
- **Практические примеры**:
  - **Прототипирование**: `time_limit=300` (5 минут)
  - **Разработка**: `time_limit=1800` (30 минут)
  - **Продакшен**: `time_limit=7200` (2 часа)

**Параметр `memory_limit`:**
- **Что означает**: Максимальное использование RAM в гигабайтах
- **Зачем нужен**: Предотвращает переполнение памяти, контролирует ресурсы
- **По умолчанию**: `None` (без ограничений)
- **Рекомендуемые значения**:
  - **Малые данные (< 1MB)**: `2-4` GB
  - **Средние данные (1-100MB)**: `4-8` GB
  - **Большие данные (100MB-1GB)**: `8-16` GB
  - **Очень большие данные (> 1GB)**: `16-32` GB
- **Влияние на производительность**:
  - **Мало памяти**: Медленная работа, возможные ошибки
  - **Достаточно памяти**: Быстрая работа, стабильность
  - **Много памяти**: Максимальная скорость, обработка больших данных
- **Оптимизация по типу задач**:
  - **Классификация**: 2-4x размер данных
  - **Регрессия**: 3-5x размер данных
  - **Временные ряды**: 4-6x размер данных
- **Мониторинг использования**:
  - **Проверка**: `import psutil; print(f"RAM: {psutil.virtual_memory().percent}%")`
  - **Оптимальное**: 70-80% от доступной памяти
  - **Критическое**: > 90% от доступной памяти

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

#### 🔧 Детальное описание параметров пресетов

**Параметр `presets`:**
- **Что означает**: Предустановленные конфигурации качества модели
- **Зачем нужен**: Упрощает выбор между скоростью и качеством
- **По умолчанию**: `None` (стандартная конфигурация)
- **Доступные пресеты**:

**`'best_quality'`:**
- **Что делает**: Максимальное качество модели
- **Время обучения**: 4-8 часов
- **Использует**: Все доступные алгоритмы, ансамбли, тюнинг гиперпараметров
- **Когда использовать**: Для продакшена, когда качество критично
- **Результат**: Лучшая точность, но долгое обучение
- **Алгоритмы**: XGBoost, LightGBM, CatBoost, Neural Networks, Ensemble
- **Валидация**: 5-fold CV + Holdout
- **Тюнинг**: 50+ попыток оптимизации

**`'high_quality'`:**
- **Что делает**: Высокое качество с разумным временем
- **Время обучения**: 2-4 часа
- **Использует**: Основные алгоритмы + ансамбли
- **Когда использовать**: Для большинства задач
- **Результат**: Хорошая точность за разумное время
- **Алгоритмы**: XGBoost, LightGBM, CatBoost, Ensemble
- **Валидация**: 3-fold CV + Holdout
- **Тюнинг**: 20+ попыток оптимизации

**`'good_quality'`:**
- **Что делает**: Хорошее качество за короткое время
- **Время обучения**: 30-60 минут
- **Использует**: Основные алгоритмы без ансамблей
- **Когда использовать**: Для быстрых экспериментов
- **Результат**: Приемлемая точность быстро
- **Алгоритмы**: XGBoost, LightGBM, CatBoost
- **Валидация**: 3-fold CV
- **Тюнинг**: 10+ попыток оптимизации

**`'medium_quality'`:**
- **Что делает**: Среднее качество за очень короткое время
- **Время обучения**: 10-30 минут
- **Использует**: Только быстрые алгоритмы
- **Когда использовать**: Для прототипирования
- **Результат**: Базовая точность очень быстро
- **Алгоритмы**: XGBoost, LightGBM
- **Валидация**: Holdout
- **Тюнинг**: 5+ попыток оптимизации

**`'optimize_for_deployment'`:**
- **Что делает**: Оптимизация для продакшена
- **Время обучения**: 1-2 часа
- **Использует**: Быстрые алгоритмы с оптимизацией
- **Когда использовать**: Для продакшена с ограничениями ресурсов
- **Результат**: Быстрые предсказания, хорошая точность
- **Алгоритмы**: XGBoost, LightGBM (оптимизированные)
- **Валидация**: 3-fold CV
- **Тюнинг**: 15+ попыток оптимизации
- **Особенности**: Меньший размер модели, быстрые предсказания

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
