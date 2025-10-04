# Теория и основы AutoML

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему теория AutoML критически важна

**Почему 80% пользователей AutoML не понимают, что происходит под капотом?** Потому что они используют AutoML как "черный ящик", не понимая принципов его работы. Это как вождение автомобиля без понимания, как работает двигатель.

### Проблемы без понимания теории
- **Слепое использование**: Не понимают, почему модель работает или не работает
- **Неправильная настройка**: Не могут оптимизировать параметры
- **Плохие результаты**: Не знают, как улучшить производительность
- **Зависимость от инструмента**: Не могут решить проблемы самостоятельно

### Преимущества понимания теории
- **Осознанное использование**: Понимают, что и почему делает система
- **Эффективная настройка**: Могут оптимизировать параметры под задачу
- **Лучшие результаты**: Знают, как улучшить производительность
- **Независимость**: Могут решать проблемы и адаптировать систему

## Введение в теорию AutoML

<img src="images/optimized/automl_theory_overview.png" alt="Теория AutoML" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 15.1: Теоретические основы автоматизированного машинного обучения - основные компоненты и принципы работы*

**Почему AutoML - это не просто "нажать кнопку"?** Потому что это сложная система алгоритмов, которая автоматизирует процесс создания ML-моделей, но требует понимания принципов для эффективного использования.

**Ключевые компоненты AutoML:**
- **Neural Architecture Search (NAS)**: Автоматический поиск оптимальной архитектуры нейронных сетей
- **Hyperparameter Optimization**: Оптимизация гиперпараметров с помощью различных методов
- **Feature Engineering Automation**: Автоматическое создание и отбор признаков
- **Ensemble Methods**: Комбинирование множественных моделей для повышения точности
- **Performance Optimization**: Оптимизация производительности и ресурсов

AutoML (Automated Machine Learning) - это область машинного обучения, которая автоматизирует процесс создания ML-моделей. Понимание теоретических основ критически важно для эффективного использования AutoML Gluon.

## Основные концепции AutoML

### 1. Neural Architecture Search (NAS)

<img src="images/optimized/neural_architecture_search.png" alt="Neural Architecture Search" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 15.2: Neural Architecture Search - автоматический поиск оптимальной архитектуры нейронных сетей*

**Почему NAS - это революция в дизайне нейросетей?** Потому что он автоматически находит архитектуры, которые превосходят созданные человеком, экономя месяцы работы экспертов.

Neural Architecture Search - это процесс автоматического поиска оптимальной архитектуры нейронной сети.

**Как работает NAS:**
- **Поисковое пространство**: Тысячи возможных архитектур
- **Оценка производительности**: Тестирование каждой архитектуры
- **Оптимизация**: Выбор лучшей архитектуры
- **Методы поиска**: Random Search, Grid Search, Reinforcement Learning, Evolutionary Algorithms

**Почему NAS работает лучше человека?**
- **Объективность**: Не ограничен предрассудками и опытом
- **Эксплуатация**: Может тестировать тысячи архитектур
- **Оптимизация**: Находит архитектуры, оптимизированные под конкретную задачу
- **Инновации**: Может найти неожиданные решения

```python
# Пример NAS в AutoGluon - автоматический поиск архитектуры
from autogluon.vision import ImagePredictor

# NAS для поиска архитектуры - автоматический дизайн нейросети
predictor = ImagePredictor()
predictor.fit(
    train_data,
    hyperparameters={
        'model': 'resnet50',  # Базовая архитектура для начала поиска
        'nas': True,          # Включить NAS - автоматический поиск
        'nas_lr': 0.01,       # Learning rate для NAS - скорость обучения
        'nas_epochs': 50     # Количество эпох для NAS - время на поиск
    }
)
```

**Детальные описания NAS параметров:**

- **`model`**: Базовая архитектура для начала поиска
  - `'resnet50'`: ResNet-50 (стандартная архитектура)
  - `'resnet101'`: ResNet-101 (более глубокая)
  - `'efficientnet'`: EfficientNet (эффективная архитектура)
  - `'mobilenet'`: MobileNet (мобильная архитектура)

- **`nas`**: Включение Neural Architecture Search
  - `True`: Включить автоматический поиск архитектуры
  - `False`: Использовать фиксированную архитектуру

- **`nas_lr`**: Learning rate для NAS (0.001-0.1)
  - `0.001`: Медленное обучение, стабильность
  - `0.01`: Стандартная скорость (рекомендуется)
  - `0.1`: Быстрое обучение, риск нестабильности

- **`nas_epochs`**: Количество эпох для NAS (10-200)
  - `10-30`: Быстрый поиск, базовое качество
  - `50-100`: Стандартный поиск (рекомендуется)
  - `150-200`: Глубокий поиск, высокое качество

### 2. Hyperparameter Optimization

<img src="images/optimized/hyperparameter_optimization.png" alt="Оптимизация гиперпараметров" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 15.3: Методы оптимизации гиперпараметров - Grid Search, Random Search, Bayesian Optimization*

Автоматическая оптимизация гиперпараметров - ключевая функция AutoML.

**Сравнение методов оптимизации:**
- **Grid Search**: Систематический поиск по сетке параметров
- **Random Search**: Случайный поиск в пространстве параметров
- **Bayesian Optimization**: Использование предыдущих результатов для выбора следующих параметров

#### Методы оптимизации:

**Grid Search:**
```python
# Систематический поиск по сетке
hyperparameters = {
    'GBM': [
        {'num_boost_round': 100, 'learning_rate': 0.1},
        {'num_boost_round': 200, 'learning_rate': 0.05},
        {'num_boost_round': 300, 'learning_rate': 0.01}
    ]
}
```

**Детальные описания Grid Search параметров:**
- **`num_boost_round`**: Количество итераций бустинга (50-1000)
  - `100`: Быстрое обучение, базовое качество
  - `200`: Стандартное обучение (рекомендуется)
  - `300`: Глубокое обучение, высокое качество
- **`learning_rate`**: Скорость обучения (0.001-0.3)
  - `0.1`: Стандартная скорость (рекомендуется)
  - `0.05`: Медленное обучение, стабильность
  - `0.01`: Очень медленное, высокое качество

**Random Search:**
```python
# Случайный поиск
hyperparameters = {
    'GBM': {
        'num_boost_round': randint(50, 500),
        'learning_rate': uniform(0.01, 0.3),
        'max_depth': randint(3, 10)
    }
}
```

**Детальные описания Random Search параметров:**
- **`num_boost_round`**: Случайное количество итераций (50-500)
  - `randint(50, 500)`: Случайное целое число в диапазоне
- **`learning_rate`**: Случайная скорость обучения (0.01-0.3)
  - `uniform(0.01, 0.3)`: Случайное вещественное число
- **`max_depth`**: Случайная глубина дерева (3-10)
  - `randint(3, 10)`: Случайная глубина для предотвращения переобучения

**Bayesian Optimization:**
```python
# Байесовская оптимизация
from autogluon.core import space

hyperparameters = {
    'GBM': {
        'num_boost_round': space.Int(50, 500),
        'learning_rate': space.Real(0.01, 0.3),
        'max_depth': space.Int(3, 10)
    }
}
```

**Детальные описания Bayesian Optimization параметров:**
- **`space.Int(50, 500)`**: Целочисленное пространство поиска
  - Использует предыдущие результаты для выбора следующих параметров
  - Более эффективен чем Random Search
- **`space.Real(0.01, 0.3)`**: Вещественное пространство поиска
  - Гауссовский процесс для моделирования функции
  - Acquisition function для выбора следующей точки
- **`space.Int(3, 10)`**: Ограниченное пространство для предотвращения переобучения

### 3. Feature Engineering Automation

<img src="images/optimized/feature_engineering_automation.png" alt="Автоматическое создание признаков" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 15.4: Автоматическое создание признаков - преобразование исходных данных в эффективные признаки*

Автоматическое создание признаков - важная часть AutoML.

**Типы автоматического создания признаков:**
- **Text Features**: TF-IDF, N-grams, Word embeddings
- **DateTime Features**: Извлечение временных компонентов
- **Categorical Features**: One-hot encoding, Target encoding
- **Numerical Features**: Полиномиальные преобразования, логарифмирование

```python
# Автоматическое создание признаков
from autogluon.tabular import TabularPredictor

predictor = TabularPredictor(
    label='target',
    feature_generator_type='auto',  # Автоматическое создание признаков
    feature_generator_kwargs={
        'enable_text_special_features': True,
        'enable_text_ngram_features': True,
        'enable_datetime_features': True,
        'enable_categorical_features': True
    }
)
```

**Детальные описания параметров автоматического создания признаков:**

- **`feature_generator_type`**: Тип генератора признаков
  - `'auto'`: Автоматический выбор лучшего генератора
  - `'default'`: Стандартный генератор
  - `'fast'`: Быстрый генератор (меньше признаков)
  - `'best'`: Лучший генератор (больше признаков)

- **`enable_text_special_features`**: Специальные текстовые признаки
  - `True`: Включить извлечение специальных признаков из текста
  - `False`: Отключить специальные текстовые признаки
  - Включает: длина текста, количество слов, специальные символы

- **`enable_text_ngram_features`**: N-gram признаки для текста
  - `True`: Включить N-gram анализ (1-gram, 2-gram, 3-gram)
  - `False`: Отключить N-gram анализ
  - Полезно для: анализ тональности, классификация текста

- **`enable_datetime_features`**: Временные признаки
  - `True`: Извлечение компонентов времени (год, месяц, день, час)
  - `False`: Отключить временные признаки
  - Включает: день недели, сезон, праздники, рабочие дни

- **`enable_categorical_features`**: Категориальные признаки
  - `True`: Обработка категориальных переменных
  - `False`: Отключить обработку категориальных переменных
  - Включает: one-hot encoding, target encoding, frequency encoding

## Математические основы

### 1. Loss Functions

<img src="images/optimized/loss_functions_comparison.png" alt="Сравнение функций потерь" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 15.5: Сравнение функций потерь - MSE, Cross Entropy, Focal Loss, Huber Loss*

Понимание функций потерь критически важно:

**Типы функций потерь:**
- **MSE (Mean Squared Error)**: Для задач регрессии
- **Cross Entropy**: Для задач классификации
- **Focal Loss**: Для решения проблемы дисбаланса классов
- **Huber Loss**: Робастная функция для выбросов

```python
# Кастомная функция потерь
import torch
import torch.nn as nn

class FocalLoss(nn.Module):
    """Focal Loss для решения проблемы дисбаланса классов"""
    
    def __init__(self, alpha=1, gamma=2):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
    
    def forward(self, inputs, targets):
        ce_loss = nn.CrossEntropyLoss()(inputs, targets)
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1-pt)**self.gamma * ce_loss
        return focal_loss
```

**Детальные описания параметров Focal Loss:**

- **`alpha`**: Весовой коэффициент для балансировки классов (0.1-2.0)
  - `1.0`: Равные веса для всех классов (стандарт)
  - `0.5`: Уменьшить вес для частых классов
  - `2.0`: Увеличить вес для редких классов
  - Применение: дисбаланс классов, редкие события

- **`gamma`**: Фокусирующий параметр (0.5-5.0)
  - `1.0`: Слабая фокусировка (близко к Cross Entropy)
  - `2.0`: Стандартная фокусировка (рекомендуется)
  - `3.0`: Сильная фокусировка на сложных примерах
  - `5.0`: Очень сильная фокусировка (экстремальные случаи)

**Другие функции потерь:**

- **MSE (Mean Squared Error)**: Для регрессии
  - Формула: `MSE = (1/n) * Σ(y_true - y_pred)²`
  - Применение: непрерывные целевые переменные
  - Чувствительность: высокая к выбросам

- **Cross Entropy**: Для классификации
  - Формула: `CE = -Σ y_true * log(y_pred)`
  - Применение: бинарная и многоклассовая классификация
  - Чувствительность: низкая к выбросам

- **Huber Loss**: Робастная функция для выбросов
  - Формула: `Huber = 0.5 * (y_true - y_pred)² if |y_true - y_pred| ≤ δ else δ * |y_true - y_pred| - 0.5 * δ²`
  - Параметр `δ`: порог переключения (1.0-5.0)
  - Применение: данные с выбросами

### 2. Optimization Algorithms

<img src="images/optimized/optimization_algorithms.png" alt="Алгоритмы оптимизации" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 15.6: Алгоритмы оптимизации - SGD, Adam, RMSprop, AdaGrad*

**Характеристики алгоритмов оптимизации:**
- **SGD**: Простой, медленный, базовый алгоритм
- **Adam**: Быстрый, адаптивный, популярен в глубоком обучении
- **RMSprop**: Хорош для рекуррентных сетей
- **AdaGrad**: Адаптивный learning rate для разреженных данных

```python
# Различные оптимизаторы
optimizers = {
    'adam': {
        'lr': 0.001,
        'betas': (0.9, 0.999),
        'eps': 1e-8
    },
    'sgd': {
        'lr': 0.01,
        'momentum': 0.9,
        'weight_decay': 1e-4
    },
    'rmsprop': {
        'lr': 0.01,
        'alpha': 0.99,
        'eps': 1e-8
    }
}
```

**Детальные описания параметров оптимизаторов:**

**Adam Optimizer:**
- **`lr`**: Learning rate (0.0001-0.01)
  - `0.001`: Стандартная скорость (рекомендуется)
  - `0.0001`: Медленное обучение, стабильность
  - `0.01`: Быстрое обучение, риск нестабильности
- **`betas`**: Коэффициенты для моментов (0.9, 0.999)
  - `(0.9, 0.999)`: Стандартные значения
  - `(0.95, 0.999)`: Более стабильное обучение
  - `(0.9, 0.99)`: Более быстрое обучение
- **`eps`**: Малое значение для численной стабильности (1e-8)
  - `1e-8`: Стандартное значение
  - `1e-6`: Менее точное, но более стабильное
  - `1e-10`: Более точное, но может быть нестабильным

**SGD Optimizer:**
- **`lr`**: Learning rate (0.001-0.1)
  - `0.01`: Стандартная скорость
  - `0.001`: Медленное обучение
  - `0.1`: Быстрое обучение
- **`momentum`**: Коэффициент момента (0.0-0.99)
  - `0.9`: Стандартное значение (рекомендуется)
  - `0.0`: Без момента (чистый SGD)
  - `0.99`: Высокий момент для стабильности
- **`weight_decay`**: L2 регуляризация (0.0-0.01)
  - `1e-4`: Слабая регуляризация
  - `1e-3`: Средняя регуляризация
  - `1e-2`: Сильная регуляризация

**RMSprop Optimizer:**
- **`lr`**: Learning rate (0.001-0.01)
  - `0.01`: Стандартная скорость
  - `0.001`: Медленное обучение
- **`alpha`**: Коэффициент затухания (0.9-0.999)
  - `0.99`: Стандартное значение
  - `0.9`: Быстрое затухание
  - `0.999`: Медленное затухание
- **`eps`**: Малое значение для стабильности (1e-8)

### 3. Regularization Techniques

```python
# Методы регуляризации
regularization = {
    'l1': 0.01,      # L1 regularization
    'l2': 0.01,      # L2 regularization
    'dropout': 0.5,  # Dropout
    'batch_norm': True,  # Batch normalization
    'early_stopping': {
        'patience': 10,
        'min_delta': 0.001
    }
}
```

**Детальные описания параметров регуляризации:**

**L1 Regularization (Lasso):**
- **`l1`**: Коэффициент L1 регуляризации (0.001-0.1)
  - `0.01`: Стандартное значение (рекомендуется)
  - `0.001`: Слабая регуляризация
  - `0.1`: Сильная регуляризация, отбор признаков
  - Эффект: обнуление неважных весов, отбор признаков

**L2 Regularization (Ridge):**
- **`l2`**: Коэффициент L2 регуляризации (0.001-0.1)
  - `0.01`: Стандартное значение (рекомендуется)
  - `0.001`: Слабая регуляризация
  - `0.1`: Сильная регуляризация, сглаживание
  - Эффект: уменьшение весов, предотвращение переобучения

**Dropout:**
- **`dropout`**: Вероятность отключения нейронов (0.1-0.8)
  - `0.5`: Стандартное значение (рекомендуется)
  - `0.1`: Слабая регуляризация
  - `0.8`: Сильная регуляризация
  - Эффект: предотвращение коадаптации нейронов

**Batch Normalization:**
- **`batch_norm`**: Включение batch normalization
  - `True`: Включить batch normalization
  - `False`: Отключить batch normalization
  - Эффект: стабилизация обучения, ускорение сходимости

**Early Stopping:**
- **`patience`**: Количество эпох без улучшения (5-50)
  - `10`: Стандартное значение (рекомендуется)
  - `5`: Быстрая остановка
  - `20`: Терпеливая остановка
- **`min_delta`**: Минимальное улучшение для продолжения (0.0001-0.01)
  - `0.001`: Стандартное значение
  - `0.0001`: Чувствительная остановка
  - `0.01`: Менее чувствительная остановка

## Ensemble Methods

<img src="images/optimized/ensemble_methods.png" alt="Методы ансамблирования" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 15.7: Методы ансамблирования - Bagging, Boosting, Stacking*

**Типы методов ансамблирования:**
- **Bagging**: Параллельное обучение на bootstrap выборках
- **Boosting**: Последовательное обучение с весами ошибок
- **Stacking**: Мета-обучение для комбинирования предсказаний

### 1. Bagging

```python
# Bagging в AutoGluon
predictor = TabularPredictor(
    label='target',
    num_bag_folds=5,    # Количество фолдов для bagging
    num_bag_sets=2,     # Количество наборов
    num_stack_levels=1  # Уровни стекинга
)
```

**Детальные описания параметров Bagging:**

- **`num_bag_folds`**: Количество фолдов для bagging (3-10)
  - `3`: Быстрое обучение, базовое качество
  - `5`: Стандартное значение (рекомендуется)
  - `10`: Высокое качество, медленное обучение
  - Эффект: больше разнообразия = лучшая обобщающая способность

- **`num_bag_sets`**: Количество наборов моделей (1-5)
  - `1`: Один набор моделей
  - `2`: Стандартное значение (рекомендуется)
  - `3-5`: Множественные наборы для стабильности
  - Эффект: дополнительная стабильность и робастность

- **`num_stack_levels`**: Уровни стекинга (0-3)
  - `0`: Без стекинга (только bagging)
  - `1`: Один уровень стекинга (рекомендуется)
  - `2-3`: Многоуровневый стекинг
  - Эффект: мета-обучение для комбинирования предсказаний

### 2. Boosting

```python
# Boosting алгоритмы
hyperparameters = {
    'GBM': {
        'num_boost_round': 1000,
        'learning_rate': 0.1,
        'max_depth': 6
    },
    'XGB': {
        'n_estimators': 1000,
        'learning_rate': 0.1,
        'max_depth': 6
    },
    'LGB': {
        'n_estimators': 1000,
        'learning_rate': 0.1,
        'max_depth': 6
    }
}
```

**Детальные описания параметров Boosting:**

**GBM (Gradient Boosting Machine):**
- **`num_boost_round`**: Количество итераций бустинга (100-2000)
  - `1000`: Стандартное значение (рекомендуется)
  - `500`: Быстрое обучение, базовое качество
  - `2000`: Глубокое обучение, высокое качество
- **`learning_rate`**: Скорость обучения (0.01-0.3)
  - `0.1`: Стандартная скорость (рекомендуется)
  - `0.05`: Медленное обучение, стабильность
  - `0.2`: Быстрое обучение, риск переобучения
- **`max_depth`**: Максимальная глубина дерева (3-10)
  - `6`: Стандартная глубина (рекомендуется)
  - `3`: Неглубокие деревья, предотвращение переобучения
  - `10`: Глубокие деревья, риск переобучения

**XGBoost:**
- **`n_estimators`**: Количество деревьев (100-2000)
  - `1000`: Стандартное значение (рекомендуется)
  - `500`: Быстрое обучение
  - `2000`: Глубокое обучение
- **`learning_rate`**: Скорость обучения (0.01-0.3)
  - `0.1`: Стандартная скорость (рекомендуется)
  - `0.05`: Медленное обучение
  - `0.2`: Быстрое обучение
- **`max_depth`**: Максимальная глубина дерева (3-10)
  - `6`: Стандартная глубина (рекомендуется)
  - `3`: Неглубокие деревья
  - `10`: Глубокие деревья

**LightGBM:**
- **`n_estimators`**: Количество деревьев (100-2000)
  - `1000`: Стандартное значение (рекомендуется)
  - `500`: Быстрое обучение
  - `2000`: Глубокое обучение
- **`learning_rate`**: Скорость обучения (0.01-0.3)
  - `0.1`: Стандартная скорость (рекомендуется)
  - `0.05`: Медленное обучение
  - `0.2`: Быстрое обучение
- **`max_depth`**: Максимальная глубина дерева (3-10)
  - `6`: Стандартная глубина (рекомендуется)
  - `3`: Неглубокие деревья
  - `10`: Глубокие деревья

### 3. Stacking

```python
# Стекинг моделей
stacking_config = {
    'num_bag_folds': 5,
    'num_bag_sets': 2,
    'num_stack_levels': 2,
    'stacker_models': ['GBM', 'XGB', 'LGB'],
    'stacker_hyperparameters': {
        'GBM': {'num_boost_round': 100}
    }
}
```

**Детальные описания параметров Stacking:**

- **`num_bag_folds`**: Количество фолдов для базовых моделей (3-10)
  - `5`: Стандартное значение (рекомендуется)
  - `3`: Быстрое обучение, базовое качество
  - `10`: Высокое качество, медленное обучение

- **`num_bag_sets`**: Количество наборов базовых моделей (1-5)
  - `2`: Стандартное значение (рекомендуется)
  - `1`: Один набор моделей
  - `3-5`: Множественные наборы для стабильности

- **`num_stack_levels`**: Уровни стекинга (1-3)
  - `1`: Один уровень стекинга (рекомендуется)
  - `2`: Двухуровневый стекинг
  - `3`: Трехуровневый стекинг (риск переобучения)

- **`stacker_models`**: Модели для стекинга
  - `['GBM', 'XGB', 'LGB']`: Стандартный набор (рекомендуется)
  - `['GBM', 'XGB']`: Минимальный набор
  - `['GBM', 'XGB', 'LGB', 'CAT']`: Расширенный набор

- **`stacker_hyperparameters`**: Гиперпараметры для стекинга
  - `{'GBM': {'num_boost_round': 100}}`: Быстрое обучение стекинга
  - `{'GBM': {'num_boost_round': 500}}`: Стандартное обучение
  - `{'GBM': {'num_boost_round': 1000}}`: Глубокое обучение

## Advanced Concepts

### 1. Multi-Task Learning

```python
# Мультизадачное обучение
class MultiTaskPredictor:
    def __init__(self, tasks):
        self.tasks = tasks
        self.predictors = {}
        
        for task in tasks:
            self.predictors[task] = TabularPredictor(
                label=task['label'],
                problem_type=task['type']
            )
    
    def fit(self, data):
        for task_name, predictor in self.predictors.items():
            task_data = data[task['features'] + [task['label']]]
            predictor.fit(task_data)
```

### 2. Transfer Learning

```python
# Трансферное обучение
def transfer_learning(source_data, target_data, source_label, target_label):
    # Обучение на исходных данных
    source_predictor = TabularPredictor(label=source_label)
    source_predictor.fit(source_data)
    
    # Извлечение признаков
    source_features = source_predictor.extract_features(target_data)
    
    # Обучение на целевых данных с извлеченными признаками
    target_predictor = TabularPredictor(label=target_label)
    target_predictor.fit(source_features)
    
    return target_predictor
```

### 3. Meta-Learning

```python
# Мета-обучение для выбора алгоритмов
class MetaLearner:
    def __init__(self):
        self.meta_features = {}
        self.algorithm_performance = {}
    
    def extract_meta_features(self, dataset):
        """Извлечение мета-признаков датасета"""
        features = {
            'n_samples': len(dataset),
            'n_features': len(dataset.columns) - 1,
            'n_classes': len(dataset['target'].unique()),
            'missing_ratio': dataset.isnull().sum().sum() / (len(dataset) * len(dataset.columns)),
            'categorical_ratio': len(dataset.select_dtypes(include=['object']).columns) / len(dataset.columns)
        }
        return features
    
    def recommend_algorithm(self, dataset):
        """Рекомендация алгоритма на основе мета-признаков"""
        meta_features = self.extract_meta_features(dataset)
        
        # Простая эвристика
        if meta_features['n_samples'] < 1000:
            return 'GBM'
        elif meta_features['categorical_ratio'] > 0.5:
            return 'CAT'
        else:
            return 'XGB'
```

## Performance Optimization

<img src="images/optimized/performance_optimization.png" alt="Оптимизация производительности" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 15.8: Оптимизация производительности - память, вычисления, данные и модели*

**Компоненты оптимизации производительности:**
- **Memory Optimization**: Оптимизация использования памяти
- **Computational Optimization**: Параллелизация и GPU ускорение
- **Data Optimization**: Очистка и предобработка данных
- **Model Optimization**: Обрезка и квантование моделей

### 1. Memory Optimization

```python
# Оптимизация памяти
def optimize_memory(data):
    """Оптимизация использования памяти"""
    
    # Изменение типов данных
    for col in data.select_dtypes(include=['int64']).columns:
        if data[col].min() >= 0 and data[col].max() < 255:
            data[col] = data[col].astype('uint8')
        elif data[col].min() >= -128 and data[col].max() < 127:
            data[col] = data[col].astype('int8')
        elif data[col].min() >= 0 and data[col].max() < 65535:
            data[col] = data[col].astype('uint16')
        elif data[col].min() >= -32768 and data[col].max() < 32767:
            data[col] = data[col].astype('int16')
        else:
            data[col] = data[col].astype('int32')
    
    # Оптимизация float типов
    for col in data.select_dtypes(include=['float64']).columns:
        data[col] = data[col].astype('float32')
    
    return data
```

**Детальные описания оптимизации памяти:**

**Целочисленные типы:**
- **`uint8`**: Беззнаковые 8-битные (0-255)
  - Экономия: 8x по сравнению с int64
  - Применение: категориальные переменные, флаги
- **`int8`**: Знаковые 8-битные (-128 до 127)
  - Экономия: 8x по сравнению с int64
  - Применение: небольшие числовые значения
- **`uint16`**: Беззнаковые 16-битные (0-65535)
  - Экономия: 4x по сравнению с int64
  - Применение: средние числовые значения
- **`int16`**: Знаковые 16-битные (-32768 до 32767)
  - Экономия: 4x по сравнению с int64
  - Применение: средние числовые значения
- **`int32`**: Знаковые 32-битные (стандарт)
  - Экономия: 2x по сравнению с int64
  - Применение: большие числовые значения

**Вещественные типы:**
- **`float32`**: 32-битные с плавающей точкой
  - Экономия: 2x по сравнению с float64
  - Точность: достаточная для большинства задач
  - Применение: все вещественные значения

**Экономия памяти:**
- **int64 → int32**: 50% экономия
- **int64 → int16**: 75% экономия
- **int64 → int8**: 87.5% экономия
- **float64 → float32**: 50% экономия

### 2. Computational Optimization

```python
# Оптимизация вычислений
import multiprocessing as mp

def parallel_processing(data, n_jobs=-1):
    """Параллельная обработка данных"""
    
    if n_jobs == -1:
        n_jobs = mp.cpu_count()
    
    # Разделение данных на части
    chunk_size = len(data) // n_jobs
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    
    # Параллельная обработка
    with mp.Pool(n_jobs) as pool:
        results = pool.map(process_chunk, chunks)
    
    return pd.concat(results)
```

**Детальные описания параметров параллельной обработки:**

- **`n_jobs`**: Количество параллельных процессов
  - `-1`: Использовать все доступные CPU ядра (рекомендуется)
  - `1`: Последовательная обработка (без параллелизма)
  - `2-8`: Фиксированное количество процессов
  - `mp.cpu_count()`: Количество CPU ядер в системе

- **`chunk_size`**: Размер части данных для обработки
  - `len(data) // n_jobs`: Равномерное разделение (рекомендуется)
  - `1000`: Фиксированный размер для небольших данных
  - `10000`: Фиксированный размер для больших данных

**Оптимизация производительности:**
- **CPU-bound задачи**: Используйте `n_jobs = mp.cpu_count()`
- **I/O-bound задачи**: Используйте `n_jobs = mp.cpu_count() * 2`
- **Memory-bound задачи**: Используйте `n_jobs = mp.cpu_count() // 2`

**Рекомендации по выбору n_jobs:**
- **Малые данные (< 10K строк)**: `n_jobs = 2-4`
- **Средние данные (10K-100K строк)**: `n_jobs = 4-8`
- **Большие данные (> 100K строк)**: `n_jobs = 8-16`
- **Очень большие данные (> 1M строк)**: `n_jobs = 16+`

## Theoretical Guarantees

### 1. Convergence Guarantees

```python
# Гарантии сходимости для различных алгоритмов
convergence_guarantees = {
    'GBM': {
        'convergence_rate': 'O(1/sqrt(T))',
        'conditions': ['convex_loss', 'bounded_gradients'],
        'theorem': 'GBM converges to global optimum for convex loss'
    },
    'XGB': {
        'convergence_rate': 'O(log(T)/T)',
        'conditions': ['strongly_convex_loss', 'bounded_hessian'],
        'theorem': 'XGB converges with rate O(log(T)/T)'
    }
}
```

### 2. Generalization Bounds

```python
# Границы обобщения
def generalization_bound(n, d, delta):
    """Граница обобщения для алгоритма"""
    import math
    
    # VC dimension bound
    vc_bound = math.sqrt((d * math.log(n) + math.log(1/delta)) / n)
    
    # Rademacher complexity bound
    rademacher_bound = math.sqrt(math.log(n) / n)
    
    return min(vc_bound, rademacher_bound)
```

## Research Frontiers

### 1. Neural Architecture Search

```python
# Современные методы NAS
class DARTS:
    """Differentiable Architecture Search"""
    
    def __init__(self, search_space):
        self.search_space = search_space
        self.architecture_weights = {}
    
    def search(self, data, epochs=50):
        """Поиск архитектуры"""
        for epoch in range(epochs):
            # Обновление весов архитектуры
            self.update_architecture_weights(data)
            
            # Обновление весов модели
            self.update_model_weights(data)
    
    def update_architecture_weights(self, data):
        """Обновление весов архитектуры"""
        # Реализация DARTS
        pass
```

### 2. AutoML for Time Series

```python
# AutoML для временных рядов
from autogluon.timeseries import TimeSeriesPredictor

def time_series_automl(data, prediction_length):
    """AutoML для временных рядов"""
    
    predictor = TimeSeriesPredictor(
        prediction_length=prediction_length,
        target="target",
        time_limit=3600  # 1 час
    )
    
    predictor.fit(data)
    return predictor
```

## Заключение

Понимание теоретических основ AutoML критически важно для:

1. **Правильного выбора алгоритмов** - знание сильных и слабых сторон
2. **Оптимизации производительности** - понимание вычислительной сложности
3. **Интерпретации результатов** - понимание статистических свойств
4. **Разработки новых методов** - основа для инноваций

Эти знания позволяют использовать AutoML Gluon не как "черный ящик", а как мощный инструмент с пониманием его внутренних механизмов.
