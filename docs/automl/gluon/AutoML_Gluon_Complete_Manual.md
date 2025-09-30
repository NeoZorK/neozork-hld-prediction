# AutoML Gluon - Полное руководство пользователя

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  
**Версия:** 1.0  

Добро пожаловать в исчерпывающее руководство по AutoML Gluon - мощному инструменту автоматизированного машинного обучения от Amazon.

## Содержание

1. [Введение и установка](./01_installation.md)
2. [Базовое использование](./02_basic_usage.md)
3. [Продвинутая конфигурация](./03_advanced_configuration.md)
4. [Метрики и оценка качества](./04_metrics.md)
5. [Валидация моделей](./05_validation.md)
6. [Продакшен и деплой](./06_production.md)
7. [Переобучение моделей](./07_retraining.md)
8. [Лучшие практики](./08_best_practices.md)
9. [Примеры использования](./09_examples.md)
10. [Troubleshooting](./10_troubleshooting.md)
11. [Оптимизация для Apple Silicon](./11_apple_silicon_optimization.md)

## Что такое AutoML Gluon?

AutoML Gluon - это библиотека от Amazon Web Services для автоматизированного машинного обучения, которая позволяет:

- Автоматически выбирать лучшие алгоритмы машинного обучения
- Настраивать гиперпараметры без ручного вмешательства
- Создавать ансамбли моделей
- Обрабатывать различные типы данных (табличные, временные ряды, изображения, текст)
- Масштабироваться на больших датасетах

## Ключевые особенности

- **Автоматический выбор модели**: Gluon автоматически тестирует множество алгоритмов
- **Эффективная настройка гиперпараметров**: Использует продвинутые методы оптимизации
- **Ансамблирование**: Автоматически создает и комбинирует несколько моделей
- **Обработка различных типов данных**: Поддержка табличных данных, временных рядов, изображений
- **Масштабируемость**: Работает как на CPU, так и на GPU
- **Интеграция с AWS**: Легкая интеграция с облачными сервисами Amazon

## Для кого этот мануал?

Этот мануал предназначен для:
- Data Scientists, которые хотят ускорить процесс создания ML-моделей
- ML Engineers, работающих с продакшен системами
- Аналитиков, изучающих автоматизированное машинное обучение
- Разработчиков, интегрирующих ML в приложения

## Предварительные требования

- Python 3.7+
- Базовые знания машинного обучения
- Понимание концепций валидации и метрик
- Опыт работы с pandas и numpy (рекомендуется)

## Специальные разделы

### Оптимизация для Apple Silicon
Раздел [11_apple_silicon_optimization.md](./11_apple_silicon_optimization.md) содержит специальные настройки для:
- **MLX интеграция** - использование Apple MLX фреймворка для ускорения
- **Ray настройка** - распределенные вычисления на Apple Silicon
- **OpenMP оптимизация** - параллельные вычисления с максимальной эффективностью
- **Отключение CUDA** - правильная настройка для Apple Silicon
- **MPS ускорение** - использование Metal Performance Shaders
- **Мониторинг производительности** - отслеживание эффективности на Apple Silicon

---

*Этот мануал содержит исчерпывающую информацию по всем аспектам работы с AutoML Gluon, от установки до продакшен деплоя, включая специальную оптимизацию для Apple Silicon.*

---

# Установка AutoML Gluon

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Системные требования

![Установка AutoML Gluon](images/installation_flowchart.png)
*Рисунок 1: Блок-схема процесса установки AutoML Gluon*

### Минимальные требования
- **Python**: 3.7, 3.8, 3.9, 3.10, 3.11
- **ОС**: Linux, macOS, Windows
- **RAM**: 4GB (рекомендуется 8GB+)
- **CPU**: 2 ядра (рекомендуется 4+ ядра)
- **Диск**: 2GB свободного места

### Рекомендуемые требования
- **Python**: 3.9 или 3.10
- **RAM**: 16GB+
- **CPU**: 8+ ядер
- **GPU**: NVIDIA GPU с CUDA поддержкой (опционально)
- **Диск**: 10GB+ свободного места

## Установка через pip

### Базовая установка
```bash
pip install autogluon
```

### Установка с дополнительными зависимостями
```bash
# Для работы с табличными данными
pip install autogluon.tabular

# Для работы с временными рядами
pip install autogluon.timeseries

# Для работы с изображениями
pip install autogluon.vision

# Для работы с текстом
pip install autogluon.text

# Полная установка всех компонентов
pip install autogluon[all]
```

## Установка через conda

### Создание нового окружения
```bash
# Создание окружения с Python 3.9
conda create -n autogluon python=3.9
conda activate autogluon

# Установка AutoGluon
conda install -c conda-forge autogluon
```

### Установка с GPU поддержкой
```bash
# Создание окружения с CUDA
conda create -n autogluon-gpu python=3.9
conda activate autogluon-gpu

# Установка PyTorch с CUDA
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

# Установка AutoGluon
pip install autogluon
```

## Установка из исходного кода

### Клонирование репозитория
```bash
git clone https://github.com/autogluon/autogluon.git
cd autogluon
```

### Установка в режиме разработки
```bash
# Установка зависимостей
pip install -e .

# Или для конкретного модуля
pip install -e ./tabular
```

## Проверка установки

### Базовый тест
```python
import autogluon as ag
print(f"AutoGluon version: {ag.__version__}")

# Тест импорта основных модулей
from autogluon.tabular import TabularPredictor
from autogluon.timeseries import TimeSeriesPredictor
from autogluon.vision import ImagePredictor
from autogluon.text import TextPredictor

print("All modules imported successfully!")
```

### Тест с простым примером
```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np

# Создание тестовых данных
data = pd.DataFrame({
    'feature1': np.random.randn(100),
    'feature2': np.random.randn(100),
    'target': np.random.randint(0, 2, 100)
})

# Тест обучения
predictor = TabularPredictor(label='target')
predictor.fit(data, time_limit=10)  # 10 секунд для быстрого теста
print("Installation test passed!")
```

## Установка дополнительных зависимостей

### Для работы с GPU
```bash
# Установка CUDA toolkit (Ubuntu/Debian)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda-repository-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
sudo dpkg -i cuda-repository-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
sudo apt-key add /var/cuda-repository-ubuntu2004-11-8-local/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda

# Установка PyTorch с CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Для работы с большими датасетами
```bash
# Установка дополнительных библиотек для обработки больших данных
pip install dask[complete]
pip install ray[default]
pip install modin[all]
```

### Для работы с временными рядами
```bash
# Специальные библиотеки для временных рядов
pip install gluonts
pip install mxnet
pip install statsmodels
```

## Настройка окружения

### Переменные окружения
```bash
# Установка переменных для оптимизации производительности
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4

# Для GPU
export CUDA_VISIBLE_DEVICES=0

# Для отладки
export AUTOGLUON_DEBUG=1
```

### Конфигурационный файл
Создайте файл `~/.autogluon/config.yaml`:
```yaml
# Конфигурация AutoGluon
default:
  time_limit: 3600  # 1 час по умолчанию
  memory_limit: 8  # 8GB RAM
  num_cpus: 4  # Количество CPU ядер
  num_gpus: 1  # Количество GPU

# Настройки для разных задач
tabular:
  presets: ['best_quality', 'high_quality', 'good_quality', 'medium_quality', 'optimize_for_deployment']
  hyperparameter_tune_kwargs:
    num_trials: 10
    scheduler: 'local'
    searcher: 'auto'

timeseries:
  prediction_length: 24
  freq: 'H'
  target_column: 'target'
```

## Устранение проблем при установке

### Проблемы с зависимостями
```bash
# Очистка кэша pip
pip cache purge

# Переустановка с игнорированием кэша
pip install --no-cache-dir autogluon

# Установка конкретной версии
pip install autogluon==0.8.2
```

### Проблемы с CUDA
```bash
# Проверка версии CUDA
nvidia-smi

# Проверка совместимости PyTorch
python -c "import torch; print(torch.cuda.is_available())"

# Установка совместимой версии PyTorch
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117
```

### Проблемы с памятью
```bash
# Установка с ограничением памяти
pip install --no-cache-dir --no-deps autogluon
pip install -r requirements.txt
```

## Проверка работоспособности

### Полный тест установки
```python
import autogluon as ag
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np

def test_installation():
    """Полный тест установки AutoGluon"""
    
    # Создание тестовых данных
    np.random.seed(42)
    n_samples = 1000
    data = pd.DataFrame({
        'feature1': np.random.randn(n_samples),
        'feature2': np.random.randn(n_samples),
        'feature3': np.random.randn(n_samples),
        'target': np.random.randint(0, 2, n_samples)
    })
    
    # Разделение на train/test
    train_data = data[:800]
    test_data = data[800:]
    
    # Создание и обучение модели
    predictor = TabularPredictor(
        label='target',
        problem_type='binary',
        eval_metric='accuracy'
    )
    
    # Обучение с ограничением времени
    predictor.fit(
        train_data,
        time_limit=60,  # 1 минута
        presets='medium_quality'
    )
    
    # Предсказания
    predictions = predictor.predict(test_data)
    
    # Оценка качества
    performance = predictor.evaluate(test_data)
    
    print(f"Model performance: {performance}")
    print("Installation test completed successfully!")
    
    return True

if __name__ == "__main__":
    test_installation()
```

## Следующие шаги

После успешной установки переходите к:
- [Базовому использованию](./02_basic_usage.md)
- [Продвинутой конфигурации](./03_advanced_configuration.md)
- [Работе с метриками](./04_metrics.md)

## Полезные ссылки

- [Официальная документация](https://auto.gluon.ai/)
- [GitHub репозиторий](https://github.com/autogluon/autogluon)
- [Примеры использования](https://github.com/autogluon/autogluon/tree/master/examples)
- [Форум сообщества](https://discuss.autogluon.ai/)


---

# Базовое использование AutoML Gluon

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Введение в TabularPredictor

![Архитектура AutoML Gluon](images/architecture_diagram.png)
*Рисунок 2: Архитектура AutoML Gluon с основными компонентами*

`TabularPredictor` - это основной класс для работы с табличными данными в AutoGluon. Он автоматически определяет тип задачи (классификация, регрессия) и выбирает лучшие алгоритмы.

### Импорт и создание базового предиктора

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np

# Создание предиктора
predictor = TabularPredictor(
    label='target_column',  # Название целевой переменной
    problem_type='auto',    # Автоматическое определение типа задачи
    eval_metric='auto'      # Автоматический выбор метрики
)
```

## Типы задач

### Классификация

```python
# Бинарная классификация
predictor = TabularPredictor(
    label='is_fraud',
    problem_type='binary',
    eval_metric='accuracy'
)

# Многоклассовая классификация
predictor = TabularPredictor(
    label='category',
    problem_type='multiclass',
    eval_metric='accuracy'
)
```

### Регрессия

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


---

# Продвинутая конфигурация AutoML Gluon

## Настройка гиперпараметров

### Создание кастомных гиперпараметров

```python
# Детальная настройка для каждого алгоритма
hyperparameters = {
    'GBM': [
        {
            'num_boost_round': 100,
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
        },
        {
            'num_boost_round': 200,
            'num_leaves': 63,
            'learning_rate': 0.05,
            'feature_fraction': 0.8,
            'bagging_fraction': 0.7,
            'bagging_freq': 5,
            'min_data_in_leaf': 10,
            'min_sum_hessian_in_leaf': 1e-3,
            'lambda_l1': 0.1,
            'lambda_l2': 0.1,
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
            'iterations': 100,
            'learning_rate': 0.1,
            'depth': 6,
            'l2_leaf_reg': 3.0,
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


---

# Метрики и оценка качества в AutoML Gluon

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Введение в метрики

![Сравнение метрик](images/metrics_comparison.png)
*Рисунок 3: Сравнение метрик для классификации и регрессии*

Метрики в AutoML Gluon используются для:
- Оценки качества моделей
- Сравнения различных алгоритмов
- Выбора лучшей модели
- Мониторинга производительности

## Метрики для классификации

### Базовые метрики

#### Accuracy (Точность)
```python
# Процент правильных предсказаний
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_true, y_pred)
print(f"Accuracy: {accuracy:.4f}")
```

#### Precision (Точность)
```python
# Доля правильно предсказанных положительных случаев
from sklearn.metrics import precision_score

precision = precision_score(y_true, y_pred, average='binary')
print(f"Precision: {precision:.4f}")

# Для многоклассовой классификации
precision_macro = precision_score(y_true, y_pred, average='macro')
precision_micro = precision_score(y_true, y_pred, average='micro')
```

#### Recall (Полнота)
```python
# Доля положительных случаев, которые были правильно предсказаны
from sklearn.metrics import recall_score

recall = recall_score(y_true, y_pred, average='binary')
print(f"Recall: {recall:.4f}")

# Для многоклассовой классификации
recall_macro = recall_score(y_true, y_pred, average='macro')
recall_micro = recall_score(y_true, y_pred, average='micro')
```

#### F1-Score
```python
# Гармоническое среднее precision и recall
from sklearn.metrics import f1_score

f1 = f1_score(y_true, y_pred, average='binary')
print(f"F1-Score: {f1:.4f}")

# Для многоклассовой классификации
f1_macro = f1_score(y_true, y_pred, average='macro')
f1_micro = f1_score(y_true, y_pred, average='micro')
```

### Продвинутые метрики

#### ROC AUC
```python
# Площадь под ROC кривой
from sklearn.metrics import roc_auc_score

# Для бинарной классификации
roc_auc = roc_auc_score(y_true, y_prob)
print(f"ROC AUC: {roc_auc:.4f}")

# Для многоклассовой классификации
roc_auc_ovo = roc_auc_score(y_true, y_prob, multi_class='ovo')
roc_auc_ovr = roc_auc_score(y_true, y_prob, multi_class='ovr')
```

#### PR AUC
```python
# Площадь под Precision-Recall кривой
from sklearn.metrics import average_precision_score

pr_auc = average_precision_score(y_true, y_prob)
print(f"PR AUC: {pr_auc:.4f}")
```

#### Log Loss
```python
# Логарифмическая функция потерь
from sklearn.metrics import log_loss

log_loss_score = log_loss(y_true, y_prob)
print(f"Log Loss: {log_loss_score:.4f}")
```

#### Balanced Accuracy
```python
# Сбалансированная точность для несбалансированных данных
from sklearn.metrics import balanced_accuracy_score

balanced_acc = balanced_accuracy_score(y_true, y_pred)
print(f"Balanced Accuracy: {balanced_acc:.4f}")
```

### Метрики для несбалансированных данных

#### Matthews Correlation Coefficient (MCC)
```python
from sklearn.metrics import matthews_corrcoef

mcc = matthews_corrcoef(y_true, y_pred)
print(f"MCC: {mcc:.4f}")
```

#### Cohen's Kappa
```python
from sklearn.metrics import cohen_kappa_score

kappa = cohen_kappa_score(y_true, y_pred)
print(f"Cohen's Kappa: {kappa:.4f}")
```

## Метрики для регрессии

### Базовые метрики

#### Mean Absolute Error (MAE)
```python
from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(y_true, y_pred)
print(f"MAE: {mae:.4f}")
```

#### Mean Squared Error (MSE)
```python
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(y_true, y_pred)
print(f"MSE: {mse:.4f}")
```

#### Root Mean Squared Error (RMSE)
```python
import numpy as np

rmse = np.sqrt(mean_squared_error(y_true, y_pred))
print(f"RMSE: {rmse:.4f}")
```

#### R² Score
```python
from sklearn.metrics import r2_score

r2 = r2_score(y_true, y_pred)
print(f"R² Score: {r2:.4f}")
```

### Продвинутые метрики

#### Mean Absolute Percentage Error (MAPE)
```python
def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

mape_score = mape(y_true, y_pred)
print(f"MAPE: {mape_score:.4f}%")
```

#### Symmetric Mean Absolute Percentage Error (SMAPE)
```python
def smape(y_true, y_pred):
    return np.mean(2 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred))) * 100

smape_score = smape(y_true, y_pred)
print(f"SMAPE: {smape_score:.4f}%")
```

#### Mean Absolute Scaled Error (MASE)
```python
def mase(y_true, y_pred, y_train):
    # Наивный прогноз (следующее значение)
    naive_forecast = np.roll(y_train, 1)
    naive_mae = np.mean(np.abs(y_train - naive_forecast))
    
    # MAE модели
    model_mae = np.mean(np.abs(y_true - y_pred))
    
    return model_mae / naive_mae

mase_score = mase(y_true, y_pred, y_train)
print(f"MASE: {mase_score:.4f}")
```

## Использование метрик в AutoGluon

### Настройка метрик для обучения

```python
from autogluon.tabular import TabularPredictor

# Для классификации
predictor = TabularPredictor(
    label='target',
    problem_type='binary',
    eval_metric='accuracy'  # или 'f1', 'roc_auc', 'log_loss'
)

# Для регрессии
predictor = TabularPredictor(
    label='target',
    problem_type='regression',
    eval_metric='rmse'  # или 'mae', 'r2'
)
```

### Множественные метрики

```python
# Обучение с несколькими метриками
predictor.fit(
    train_data,
    eval_metric=['accuracy', 'f1', 'roc_auc']
)

# Получение всех метрик
performance = predictor.evaluate(test_data)
print(performance)
```

### Кастомные метрики

```python
from autogluon.core import Scorer

# Создание кастомной метрики
def custom_metric(y_true, y_pred):
    """Кастомная метрика для оценки качества"""
    # Ваша логика расчета
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

## Анализ производительности

### Лидерборд моделей

```python
# Получение лидерборда
leaderboard = predictor.leaderboard(test_data)
print(leaderboard)

# Детальный лидерборд
leaderboard_detailed = predictor.leaderboard(
    test_data,
    extra_info=True,
    silent=False
)
```

### Анализ важности признаков

```python
# Важность признаков
feature_importance = predictor.feature_importance()
print(feature_importance)

# Визуализация важности признаков
import matplotlib.pyplot as plt

feature_importance.plot(kind='barh', figsize=(10, 8))
plt.title('Feature Importance')
plt.xlabel('Importance')
plt.show()
```

### Анализ ошибок

```python
# Анализ ошибок для классификации
from sklearn.metrics import classification_report, confusion_matrix

# Отчет по классификации
print(classification_report(y_true, y_pred))

# Матрица ошибок
cm = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:")
print(cm)

# Визуализация матрицы ошибок
import seaborn as sns
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.show()
```

## Метрики для временных рядов

### Метрики для прогнозирования

```python
# Mean Absolute Scaled Error (MASE)
def mase_time_series(y_true, y_pred, y_train, seasonal_period=1):
    """MASE для временных рядов"""
    # Наивный прогноз
    naive_forecast = np.roll(y_train, seasonal_period)
    naive_mae = np.mean(np.abs(y_train - naive_forecast))
    
    # MAE модели
    model_mae = np.mean(np.abs(y_true - y_pred))
    
    return model_mae / naive_mae

# Symmetric Mean Absolute Percentage Error (SMAPE)
def smape_time_series(y_true, y_pred):
    """SMAPE для временных рядов"""
    return np.mean(2 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred))) * 100
```

### Метрики для финансовых данных

```python
# Sharpe Ratio
def sharpe_ratio(returns, risk_free_rate=0.02):
    """Коэффициент Шарпа"""
    excess_returns = returns - risk_free_rate
    return np.mean(excess_returns) / np.std(excess_returns)

# Maximum Drawdown
def max_drawdown(cumulative_returns):
    """Максимальная просадка"""
    peak = np.maximum.accumulate(cumulative_returns)
    drawdown = (cumulative_returns - peak) / peak
    return np.min(drawdown)

# Calmar Ratio
def calmar_ratio(returns, max_dd):
    """Коэффициент Калмара"""
    annual_return = np.mean(returns) * 252
    return annual_return / abs(max_dd)
```

## Мониторинг метрик

### Отслеживание метрик в реальном времени

```python
import logging
from datetime import datetime

class MetricsLogger:
    def __init__(self, log_file='metrics.log'):
        self.log_file = log_file
        self.metrics_history = []
    
    def log_metrics(self, metrics_dict):
        """Логирование метрик"""
        timestamp = datetime.now()
        metrics_dict['timestamp'] = timestamp
        self.metrics_history.append(metrics_dict)
        
        # Запись в файл
        with open(self.log_file, 'a') as f:
            f.write(f"{timestamp}: {metrics_dict}\n")
    
    def get_metrics_trend(self, metric_name):
        """Получение тренда метрики"""
        return [m[metric_name] for m in self.metrics_history if metric_name in m]

# Использование
metrics_logger = MetricsLogger()

# Логирование метрик
metrics = {
    'accuracy': 0.85,
    'f1_score': 0.82,
    'roc_auc': 0.88
}
metrics_logger.log_metrics(metrics)
```

### Алерты по метрикам

```python
class MetricsAlert:
    def __init__(self, threshold=0.8, metric_name='accuracy'):
        self.threshold = threshold
        self.metric_name = metric_name
    
    def check_alert(self, current_metric):
        """Проверка алерта"""
        if current_metric < self.threshold:
            print(f"ALERT: {self.metric_name} = {current_metric} < {self.threshold}")
            return True
        return False

# Использование
alert = MetricsAlert(threshold=0.8, metric_name='accuracy')
if alert.check_alert(0.75):
    # Отправка уведомления
    pass
```

## Примеры использования метрик

### Полный пример оценки модели

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# Создание данных
X, y = make_classification(
    n_samples=10000,
    n_features=20,
    n_informative=15,
    n_redundant=5,
    n_classes=2,
    random_state=42
)

data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
data['target'] = y

# Разделение данных
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Создание и обучение модели
predictor = TabularPredictor(
    label='target',
    problem_type='binary',
    eval_metric='accuracy'
)

predictor.fit(train_data, time_limit=300)

# Предсказания
predictions = predictor.predict(test_data)
probabilities = predictor.predict_proba(test_data)

# Оценка качества
performance = predictor.evaluate(test_data)
print("Performance Metrics:")
for metric, value in performance.items():
    print(f"{metric}: {value:.4f}")

# Лидерборд
leaderboard = predictor.leaderboard(test_data)
print("\nLeaderboard:")
print(leaderboard)

# Важность признаков
feature_importance = predictor.feature_importance()
print("\nFeature Importance:")
print(feature_importance.head(10))

# Визуализация
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# ROC кривая
from sklearn.metrics import roc_curve, auc
fpr, tpr, _ = roc_curve(test_data['target'], probabilities[1])
roc_auc = auc(fpr, tpr)
axes[0, 0].plot(fpr, tpr, label=f'ROC AUC = {roc_auc:.3f}')
axes[0, 0].plot([0, 1], [0, 1], 'k--')
axes[0, 0].set_xlabel('False Positive Rate')
axes[0, 0].set_ylabel('True Positive Rate')
axes[0, 0].set_title('ROC Curve')
axes[0, 0].legend()

# Precision-Recall кривая
from sklearn.metrics import precision_recall_curve
precision, recall, _ = precision_recall_curve(test_data['target'], probabilities[1])
axes[0, 1].plot(recall, precision)
axes[0, 1].set_xlabel('Recall')
axes[0, 1].set_ylabel('Precision')
axes[0, 1].set_title('Precision-Recall Curve')

# Матрица ошибок
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(test_data['target'], predictions)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1, 0])
axes[1, 0].set_title('Confusion Matrix')

# Важность признаков
feature_importance.head(10).plot(kind='barh', ax=axes[1, 1])
axes[1, 1].set_title('Top 10 Feature Importance')

plt.tight_layout()
plt.show()
```

## Следующие шаги

После освоения работы с метриками переходите к:
- [Методам валидации](./05_validation.md)
- [Продакшен деплою](./06_production.md)
- [Переобучению моделей](./07_retraining.md)


---

# Валидация моделей в AutoML Gluon

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Введение в валидацию

![Методы валидации](images/validation_methods.png)
*Рисунок 4: Методы валидации в AutoML Gluon*

Валидация - это критически важный процесс для оценки качества ML-моделей и предотвращения переобучения. В AutoML Gluon доступны различные методы валидации для разных типов задач.

## Типы валидации

### 1. Holdout валидация

```python
from autogluon.tabular import TabularPredictor

# Простая holdout валидация
predictor = TabularPredictor(label='target')
predictor.fit(
    train_data,
    holdout_frac=0.2  # 20% данных для валидации
)
```

### 2. K-Fold кросс-валидация

```python
# K-fold кросс-валидация
predictor.fit(
    train_data,
    num_bag_folds=5,  # 5-fold CV
    num_bag_sets=1
)
```

### 3. Стратифицированная валидация

```python
# Стратифицированная валидация для несбалансированных данных
predictor.fit(
    train_data,
    num_bag_folds=5,
    num_bag_sets=1,
    stratify=True
)
```

## Backtest валидация

### Временная валидация для временных рядов

```python
from sklearn.model_selection import TimeSeriesSplit
import pandas as pd
import numpy as np

def time_series_backtest(data, target_col, n_splits=5):
    """Backtest валидация для временных рядов"""
    
    # Сортировка по времени
    data = data.sort_values('timestamp')
    
    # Создание временных фолдов
    tscv = TimeSeriesSplit(n_splits=n_splits)
    
    results = []
    
    for fold, (train_idx, val_idx) in enumerate(tscv.split(data)):
        print(f"Fold {fold + 1}/{n_splits}")
        
        # Разделение данных
        train_fold = data.iloc[train_idx]
        val_fold = data.iloc[val_idx]
        
        # Обучение модели
        predictor = TabularPredictor(label=target_col)
        predictor.fit(train_fold, time_limit=300)
        
        # Предсказания
        predictions = predictor.predict(val_fold)
        
        # Оценка качества
        performance = predictor.evaluate(val_fold)
        
        results.append({
            'fold': fold + 1,
            'performance': performance,
            'predictions': predictions
        })
    
    return results

# Использование
backtest_results = time_series_backtest(data, 'target', n_splits=5)
```

### Расширенный backtest

```python
def advanced_backtest(data, target_col, window_size=1000, step_size=100):
    """Расширенный backtest с скользящим окном"""
    
    results = []
    n_samples = len(data)
    
    for start in range(0, n_samples - window_size, step_size):
        end = start + window_size
        
        # Разделение на train/validation
        train_data = data.iloc[start:end-100]
        val_data = data.iloc[end-100:end]
        
        # Обучение модели
        predictor = TabularPredictor(label=target_col)
        predictor.fit(train_data, time_limit=300)
        
        # Предсказания
        predictions = predictor.predict(val_data)
        
        # Оценка качества
        performance = predictor.evaluate(val_data)
        
        results.append({
            'start': start,
            'end': end,
            'performance': performance,
            'predictions': predictions
        })
    
    return results
```

## Walk-Forward валидация

### Базовая Walk-Forward валидация

```python
def walk_forward_validation(data, target_col, train_size=1000, test_size=100):
    """Walk-Forward валидация"""
    
    results = []
    n_samples = len(data)
    
    for i in range(train_size, n_samples - test_size, test_size):
        # Обучающая выборка
        train_data = data.iloc[i-train_size:i]
        
        # Тестовая выборка
        test_data = data.iloc[i:i+test_size]
        
        # Обучение модели
        predictor = TabularPredictor(label=target_col)
        predictor.fit(train_data, time_limit=300)
        
        # Предсказания
        predictions = predictor.predict(test_data)
        
        # Оценка качества
        performance = predictor.evaluate(test_data)
        
        results.append({
            'train_start': i-train_size,
            'train_end': i,
            'test_start': i,
            'test_end': i+test_size,
            'performance': performance,
            'predictions': predictions
        })
    
    return results

# Использование
wf_results = walk_forward_validation(data, 'target', train_size=1000, test_size=100)
```

### Адаптивная Walk-Forward валидация

```python
def adaptive_walk_forward(data, target_col, min_train_size=500, max_train_size=2000):
    """Адаптивная Walk-Forward валидация с изменяющимся размером окна"""
    
    results = []
    n_samples = len(data)
    current_train_size = min_train_size
    
    for i in range(min_train_size, n_samples - 100, 100):
        # Адаптация размера обучающей выборки
        if i > n_samples // 2:
            current_train_size = min(max_train_size, current_train_size + 100)
        
        # Обучающая выборка
        train_data = data.iloc[i-current_train_size:i]
        
        # Тестовая выборка
        test_data = data.iloc[i:i+100]
        
        # Обучение модели
        predictor = TabularPredictor(label=target_col)
        predictor.fit(train_data, time_limit=300)
        
        # Предсказания
        predictions = predictor.predict(test_data)
        
        # Оценка качества
        performance = predictor.evaluate(test_data)
        
        results.append({
            'train_size': current_train_size,
            'performance': performance,
            'predictions': predictions
        })
    
    return results
```

## Monte Carlo валидация

### Базовый Monte Carlo

```python
def monte_carlo_validation(data, target_col, n_iterations=100, train_frac=0.8):
    """Monte Carlo валидация с случайным разделением данных"""
    
    results = []
    
    for iteration in range(n_iterations):
        # Случайное разделение данных
        train_data = data.sample(frac=train_frac, random_state=iteration)
        test_data = data.drop(train_data.index)
        
        # Обучение модели
        predictor = TabularPredictor(label=target_col)
        predictor.fit(train_data, time_limit=300)
        
        # Предсказания
        predictions = predictor.predict(test_data)
        
        # Оценка качества
        performance = predictor.evaluate(test_data)
        
        results.append({
            'iteration': iteration,
            'performance': performance,
            'predictions': predictions
        })
    
    return results

# Использование
mc_results = monte_carlo_validation(data, 'target', n_iterations=100)
```

### Bootstrap валидация

```python
def bootstrap_validation(data, target_col, n_bootstrap=100):
    """Bootstrap валидация"""
    
    results = []
    n_samples = len(data)
    
    for i in range(n_bootstrap):
        # Bootstrap выборка
        bootstrap_indices = np.random.choice(n_samples, size=n_samples, replace=True)
        bootstrap_data = data.iloc[bootstrap_indices]
        
        # Out-of-bag выборка
        oob_indices = np.setdiff1d(np.arange(n_samples), np.unique(bootstrap_indices))
        oob_data = data.iloc[oob_indices]
        
        if len(oob_data) == 0:
            continue
        
        # Обучение модели
        predictor = TabularPredictor(label=target_col)
        predictor.fit(bootstrap_data, time_limit=300)
        
        # Предсказания на OOB данных
        predictions = predictor.predict(oob_data)
        
        # Оценка качества
        performance = predictor.evaluate(oob_data)
        
        results.append({
            'bootstrap': i,
            'performance': performance,
            'predictions': predictions
        })
    
    return results
```

## Комбинированная валидация

### Ensemble валидация

```python
def ensemble_validation(data, target_col, validation_methods=['holdout', 'kfold', 'monte_carlo']):
    """Комбинированная валидация с несколькими методами"""
    
    results = {}
    
    # Holdout валидация
    if 'holdout' in validation_methods:
        predictor = TabularPredictor(label=target_col)
        predictor.fit(data, holdout_frac=0.2)
        results['holdout'] = predictor.evaluate(data)
    
    # K-fold валидация
    if 'kfold' in validation_methods:
        predictor = TabularPredictor(label=target_col)
        predictor.fit(data, num_bag_folds=5, num_bag_sets=1)
        results['kfold'] = predictor.evaluate(data)
    
    # Monte Carlo валидация
    if 'monte_carlo' in validation_methods:
        mc_results = monte_carlo_validation(data, target_col, n_iterations=50)
        results['monte_carlo'] = mc_results
    
    return results
```

## Валидация для финансовых данных

### Финансовая валидация

```python
def financial_validation(data, target_col, lookback_window=252, forward_window=21):
    """Специализированная валидация для финансовых данных"""
    
    results = []
    n_samples = len(data)
    
    for i in range(lookback_window, n_samples - forward_window, forward_window):
        # Обучающая выборка (lookback_window дней)
        train_data = data.iloc[i-lookback_window:i]
        
        # Тестовая выборка (forward_window дней)
        test_data = data.iloc[i:i+forward_window]
        
        # Обучение модели
        predictor = TabularPredictor(label=target_col)
        predictor.fit(train_data, time_limit=300)
        
        # Предсказания
        predictions = predictor.predict(test_data)
        
        # Финансовые метрики
        returns = test_data[target_col].pct_change().dropna()
        predicted_returns = predictions.pct_change().dropna()
        
        # Sharpe Ratio
        sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252)
        
        # Maximum Drawdown
        cumulative_returns = (1 + returns).cumprod()
        peak = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()
        
        results.append({
            'start_date': test_data.index[0],
            'end_date': test_data.index[-1],
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'predictions': predictions
        })
    
    return results
```

## Анализ результатов валидации

### Статистический анализ

```python
def analyze_validation_results(results):
    """Анализ результатов валидации"""
    
    # Извлечение метрик
    metrics = []
    for result in results:
        if 'performance' in result:
            metrics.append(result['performance'])
    
    # Статистический анализ
    analysis = {}
    
    for metric in metrics[0].keys():
        values = [m[metric] for m in metrics]
        analysis[metric] = {
            'mean': np.mean(values),
            'std': np.std(values),
            'min': np.min(values),
            'max': np.max(values),
            'median': np.median(values),
            'q25': np.percentile(values, 25),
            'q75': np.percentile(values, 75)
        }
    
    return analysis

# Использование
analysis = analyze_validation_results(backtest_results)
print("Validation Analysis:")
for metric, stats in analysis.items():
    print(f"{metric}: {stats['mean']:.4f} ± {stats['std']:.4f}")
```

### Визуализация результатов

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_validation_results(results, metric='accuracy'):
    """Визуализация результатов валидации"""
    
    # Извлечение метрик
    values = []
    for result in results:
        if 'performance' in result and metric in result['performance']:
            values.append(result['performance'][metric])
    
    # График
    plt.figure(figsize=(12, 8))
    
    # Временной ряд метрики
    plt.subplot(2, 2, 1)
    plt.plot(values)
    plt.title(f'{metric} over time')
    plt.xlabel('Fold/Iteration')
    plt.ylabel(metric)
    
    # Распределение метрики
    plt.subplot(2, 2, 2)
    plt.hist(values, bins=20, alpha=0.7)
    plt.title(f'Distribution of {metric}')
    plt.xlabel(metric)
    plt.ylabel('Frequency')
    
    # Box plot
    plt.subplot(2, 2, 3)
    plt.boxplot(values)
    plt.title(f'Box plot of {metric}')
    plt.ylabel(metric)
    
    # Статистики
    plt.subplot(2, 2, 4)
    stats_text = f"""
    Mean: {np.mean(values):.4f}
    Std: {np.std(values):.4f}
    Min: {np.min(values):.4f}
    Max: {np.max(values):.4f}
    """
    plt.text(0.1, 0.5, stats_text, transform=plt.gca().transAxes, fontsize=12)
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

# Использование
plot_validation_results(backtest_results, metric='accuracy')
```

## Практические примеры

### Полный пример валидации

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Создание данных
X, y = make_classification(
    n_samples=10000,
    n_features=20,
    n_informative=15,
    n_redundant=5,
    n_classes=2,
    random_state=42
)

data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
data['target'] = y

# Добавление временной метки
data['timestamp'] = pd.date_range('2020-01-01', periods=len(data), freq='D')
data = data.set_index('timestamp')

# Различные методы валидации
print("=== Holdout Validation ===")
predictor_holdout = TabularPredictor(label='target')
predictor_holdout.fit(data, holdout_frac=0.2, time_limit=300)
holdout_performance = predictor_holdout.evaluate(data)
print(f"Holdout Performance: {holdout_performance}")

print("\n=== K-Fold Validation ===")
predictor_kfold = TabularPredictor(label='target')
predictor_kfold.fit(data, num_bag_folds=5, num_bag_sets=1, time_limit=300)
kfold_performance = predictor_kfold.evaluate(data)
print(f"K-Fold Performance: {kfold_performance}")

print("\n=== Time Series Backtest ===")
backtest_results = time_series_backtest(data, 'target', n_splits=5)
backtest_analysis = analyze_validation_results(backtest_results)
print(f"Backtest Analysis: {backtest_analysis}")

print("\n=== Monte Carlo Validation ===")
mc_results = monte_carlo_validation(data, 'target', n_iterations=50)
mc_analysis = analyze_validation_results(mc_results)
print(f"Monte Carlo Analysis: {mc_analysis}")

# Визуализация результатов
plot_validation_results(backtest_results, metric='accuracy')
```

## Лучшие практики валидации

### Выбор метода валидации

```python
def choose_validation_method(data_type, problem_type, data_size):
    """Выбор оптимального метода валидации"""
    
    if data_type == 'time_series':
        return 'time_series_backtest'
    elif data_size < 1000:
        return 'kfold'
    elif data_size < 10000:
        return 'holdout'
    else:
        return 'monte_carlo'
```

### Настройка параметров валидации

```python
def optimize_validation_params(data, target_col):
    """Оптимизация параметров валидации"""
    
    # Определение оптимального количества фолдов
    n_samples = len(data)
    if n_samples < 100:
        n_folds = 3
    elif n_samples < 1000:
        n_folds = 5
    else:
        n_folds = 10
    
    # Определение размера holdout
    if n_samples < 1000:
        holdout_frac = 0.3
    else:
        holdout_frac = 0.2
    
    return {
        'n_folds': n_folds,
        'holdout_frac': holdout_frac,
        'n_monte_carlo': min(100, n_samples // 10)
    }
```

## Следующие шаги

После освоения методов валидации переходите к:
- [Продакшен деплою](./06_production.md)
- [Переобучению моделей](./07_retraining.md)
- [Лучшим практикам](./08_best_practices.md)


---

# Продакшен и деплой AutoML Gluon моделей

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Введение в продакшен

![Продакшен архитектура](images/production_architecture.png)
*Рисунок 5: Архитектура продакшен системы AutoML Gluon*

Продакшен деплой ML-моделей - это критически важный этап, который требует тщательного планирования, мониторинга и поддержки. В этом разделе рассмотрим все аспекты деплоя AutoML Gluon моделей в продакшен.

## Подготовка модели к продакшену

### Оптимизация модели

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np

# Создание оптимизированной модели для продакшена
def create_production_model(train_data, target_col):
    """Создание модели, оптимизированной для продакшена"""
    
    predictor = TabularPredictor(
        label=target_col,
        problem_type='auto',
        eval_metric='auto',
        path='./production_models'
    )
    
    # Обучение с оптимизацией для деплоя
    predictor.fit(
        train_data,
        presets='optimize_for_deployment',
        time_limit=3600,  # 1 час
        num_bag_folds=3,   # Меньше фолдов для скорости
        num_bag_sets=1,
        ag_args_fit={
            'num_cpus': 4,
            'num_gpus': 0,
            'memory_limit': 8
        }
    )
    
    return predictor
```

### Сжатие модели

```python
def compress_model(predictor, model_name):
    """Сжатие модели для продакшена"""
    
    # Сохранение сжатой модели
    predictor.save(
        model_name,
        save_space=True,
        compress=True,
        save_info=True
    )
    
    # Получение размера модели
    import os
    model_size = os.path.getsize(f"{model_name}/predictor.pkl") / (1024 * 1024)  # MB
    print(f"Model size: {model_size:.2f} MB")
    
    return model_size
```

### Валидация модели

```python
def validate_production_model(predictor, test_data, performance_thresholds):
    """Валидация модели для продакшена"""
    
    # Предсказания
    predictions = predictor.predict(test_data)
    
    # Оценка качества
    performance = predictor.evaluate(test_data)
    
    # Проверка пороговых значений
    validation_results = {}
    for metric, threshold in performance_thresholds.items():
        if metric in performance:
            validation_results[metric] = performance[metric] >= threshold
        else:
            validation_results[metric] = False
    
    # Проверка стабильности предсказаний
    if hasattr(predictor, 'predict_proba'):
        probabilities = predictor.predict_proba(test_data)
        prob_std = probabilities.std().mean()
        validation_results['stability'] = prob_std < 0.1  # Стабильность вероятностей
    
    return validation_results, performance
```

## API сервер для продакшена

### FastAPI сервер

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import logging
from typing import Dict, List, Any
import asyncio
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание FastAPI приложения
app = FastAPI(title="AutoML Gluon Production API", version="1.0.0")

# Глобальная переменная для модели
model = None

class PredictionRequest(BaseModel):
    """Схема запроса для предсказания"""
    data: List[Dict[str, Any]]
    
class PredictionResponse(BaseModel):
    """Схема ответа с предсказаниями"""
    predictions: List[Any]
    probabilities: List[Dict[str, float]] = None
    model_info: Dict[str, Any]
    timestamp: str

class HealthResponse(BaseModel):
    """Схема ответа для health check"""
    status: str
    model_loaded: bool
    model_info: Dict[str, Any] = None

@app.on_event("startup")
async def load_model():
    """Загрузка модели при запуске сервера"""
    global model
    try:
        model = TabularPredictor.load('./production_models')
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        model = None

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    if model is None:
        return HealthResponse(
            status="unhealthy",
            model_loaded=False
        )
    
    return HealthResponse(
        status="healthy",
        model_loaded=True,
        model_info={
            "model_path": model.path,
            "problem_type": model.problem_type,
            "eval_metric": model.eval_metric
        }
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Endpoint для предсказаний"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Преобразование данных в DataFrame
        df = pd.DataFrame(request.data)
        
        # Предсказания
        predictions = model.predict(df)
        
        # Вероятности (если доступны)
        probabilities = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(df)
            probabilities = proba.to_dict('records')
        
        # Информация о модели
        model_info = {
            "model_path": model.path,
            "problem_type": model.problem_type,
            "eval_metric": model.eval_metric,
            "num_features": len(df.columns)
        }
        
        return PredictionResponse(
            predictions=predictions.tolist(),
            probabilities=probabilities,
            model_info=model_info,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/info")
async def model_info():
    """Информация о модели"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_path": model.path,
        "problem_type": model.problem_type,
        "eval_metric": model.eval_metric,
        "feature_importance": model.feature_importance().to_dict()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Flask сервер

```python
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import logging
from datetime import datetime
import traceback

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание Flask приложения
app = Flask(__name__)

# Глобальная переменная для модели
model = None

def load_model():
    """Загрузка модели"""
    global model
    try:
        model = TabularPredictor.load('./production_models')
        logger.info("Model loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    if model is None:
        return jsonify({
            "status": "unhealthy",
            "model_loaded": False
        }), 503
    
    return jsonify({
        "status": "healthy",
        "model_loaded": True,
        "model_info": {
            "model_path": model.path,
            "problem_type": model.problem_type,
            "eval_metric": model.eval_metric
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint для предсказаний"""
    if model is None:
        return jsonify({"error": "Model not loaded"}), 503
    
    try:
        # Получение данных
        data = request.get_json()
        
        if 'data' not in data:
            return jsonify({"error": "No data provided"}), 400
        
        # Преобразование в DataFrame
        df = pd.DataFrame(data['data'])
        
        # Предсказания
        predictions = model.predict(df)
        
        # Вероятности (если доступны)
        probabilities = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(df)
            probabilities = proba.to_dict('records')
        
        return jsonify({
            "predictions": predictions.tolist(),
            "probabilities": probabilities,
            "model_info": {
                "model_path": model.path,
                "problem_type": model.problem_type,
                "eval_metric": model.eval_metric
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/model/info', methods=['GET'])
def model_info():
    """Информация о модели"""
    if model is None:
        return jsonify({"error": "Model not loaded"}), 503
    
    return jsonify({
        "model_path": model.path,
        "problem_type": model.problem_type,
        "eval_metric": model.eval_metric,
        "feature_importance": model.feature_importance().to_dict()
    })

if __name__ == "__main__":
    if load_model():
        app.run(host="0.0.0.0", port=8000, debug=False)
    else:
        logger.error("Failed to start server - model not loaded")
```

## Docker контейнеризация

### Dockerfile для продакшена

```dockerfile
# Dockerfile для продакшена
FROM python:3.9-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание пользователя для безопасности
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["python", "app.py"]
```

### Docker Compose для продакшена

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  autogluon-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/app/models
      - LOG_LEVEL=INFO
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - autogluon-api
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

## Kubernetes деплой

### Deployment манифест

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: autogluon-api
  labels:
    app: autogluon-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: autogluon-api
  template:
    metadata:
      labels:
        app: autogluon-api
    spec:
      containers:
      - name: autogluon-api
        image: autogluon-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: MODEL_PATH
          value: "/app/models"
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: model-storage
          mountPath: /app/models
        - name: log-storage
          mountPath: /app/logs
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: model-pvc
      - name: log-storage
        persistentVolumeClaim:
          claimName: log-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: autogluon-api-service
spec:
  selector:
    app: autogluon-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: model-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: log-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

## Мониторинг и логирование

### Система мониторинга

```python
import logging
import time
from datetime import datetime
import psutil
import requests
from typing import Dict, Any

class ProductionMonitor:
    """Мониторинг продакшен системы"""
    
    def __init__(self, log_file='production.log'):
        self.log_file = log_file
        self.setup_logging()
        self.metrics = {}
    
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
    
    def log_prediction(self, input_data: Dict, prediction: Any, 
                      processing_time: float, model_info: Dict):
        """Логирование предсказания"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'input_data': input_data,
            'prediction': prediction,
            'processing_time': processing_time,
            'model_info': model_info
        }
        self.logger.info(f"Prediction: {log_entry}")
    
    def log_error(self, error: Exception, context: Dict):
        """Логирование ошибок"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'error': str(error),
            'context': context,
            'traceback': traceback.format_exc()
        }
        self.logger.error(f"Error: {error_entry}")
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Получение системных метрик"""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'timestamp': datetime.now().isoformat()
        }
    
    def check_model_health(self, model) -> Dict[str, Any]:
        """Проверка здоровья модели"""
        try:
            # Тестовое предсказание
            test_data = pd.DataFrame({'feature1': [1.0], 'feature2': [2.0]})
            start_time = time.time()
            prediction = model.predict(test_data)
            processing_time = time.time() - start_time
            
            return {
                'status': 'healthy',
                'processing_time': processing_time,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
```

### Алерты и уведомления

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

class AlertSystem:
    """Система алертов для продакшена"""
    
    def __init__(self, smtp_server, smtp_port, email, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
    
    def send_email_alert(self, subject: str, message: str, recipients: list):
        """Отправка email алерта"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            print(f"Email alert sent to {recipients}")
        except Exception as e:
            print(f"Failed to send email alert: {e}")
    
    def send_slack_alert(self, webhook_url: str, message: str):
        """Отправка Slack алерта"""
        try:
            payload = {
                "text": message,
                "username": "AutoML Gluon Monitor",
                "icon_emoji": ":robot_face:"
            }
            
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            
            print("Slack alert sent successfully")
        except Exception as e:
            print(f"Failed to send Slack alert: {e}")
    
    def check_performance_thresholds(self, metrics: Dict[str, float], 
                                   thresholds: Dict[str, float]):
        """Проверка пороговых значений производительности"""
        alerts = []
        
        for metric, threshold in thresholds.items():
            if metric in metrics and metrics[metric] < threshold:
                alerts.append(f"{metric} is below threshold: {metrics[metric]} < {threshold}")
        
        return alerts
```

## Масштабирование

### Горизонтальное масштабирование

```python
# Настройка для горизонтального масштабирования
import asyncio
from concurrent.futures import ThreadPoolExecutor
import queue
import threading

class ScalablePredictionService:
    """Масштабируемый сервис предсказаний"""
    
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.request_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
    async def process_prediction(self, data: Dict) -> Dict:
        """Асинхронная обработка предсказания"""
        loop = asyncio.get_event_loop()
        
        # Выполнение предсказания в отдельном потоке
        result = await loop.run_in_executor(
            self.executor, 
            self._predict_sync, 
            data
        )
        
        return result
    
    def _predict_sync(self, data: Dict) -> Dict:
        """Синхронное предсказание"""
        # Ваша логика предсказания
        pass
    
    def batch_predict(self, batch_data: List[Dict]) -> List[Dict]:
        """Пакетная обработка предсказаний"""
        results = []
        
        # Разделение на батчи
        batch_size = 100
        for i in range(0, len(batch_data), batch_size):
            batch = batch_data[i:i+batch_size]
            
            # Параллельная обработка батча
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self._predict_sync, data) for data in batch]
                batch_results = [future.result() for future in futures]
                results.extend(batch_results)
        
        return results
```

### Кэширование

```python
import redis
import json
import hashlib
from typing import Any, Optional

class PredictionCache:
    """Кэш для предсказаний"""
    
    def __init__(self, redis_host='localhost', redis_port=6379, ttl=3600):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.ttl = ttl
    
    def _generate_cache_key(self, data: Dict) -> str:
        """Генерация ключа кэша"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def get_prediction(self, data: Dict) -> Optional[Dict]:
        """Получение предсказания из кэша"""
        cache_key = self._generate_cache_key(data)
        cached_result = self.redis_client.get(cache_key)
        
        if cached_result:
            return json.loads(cached_result)
        
        return None
    
    def set_prediction(self, data: Dict, prediction: Dict):
        """Сохранение предсказания в кэш"""
        cache_key = self._generate_cache_key(data)
        self.redis_client.setex(
            cache_key, 
            self.ttl, 
            json.dumps(prediction)
        )
    
    def invalidate_cache(self, pattern: str = "*"):
        """Очистка кэша"""
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)
```

## Безопасность

### Аутентификация и авторизация

```python
from functools import wraps
import jwt
from datetime import datetime, timedelta
import secrets

class SecurityManager:
    """Менеджер безопасности"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.api_keys = {}
    
    def generate_api_key(self, user_id: str) -> str:
        """Генерация API ключа"""
        api_key = secrets.token_urlsafe(32)
        self.api_keys[api_key] = {
            'user_id': user_id,
            'created_at': datetime.now(),
            'permissions': ['predict', 'model_info']
        }
        return api_key
    
    def validate_api_key(self, api_key: str) -> bool:
        """Валидация API ключа"""
        return api_key in self.api_keys
    
    def get_user_permissions(self, api_key: str) -> list:
        """Получение разрешений пользователя"""
        if api_key in self.api_keys:
            return self.api_keys[api_key]['permissions']
        return []
    
    def require_auth(self, permissions: list = None):
        """Декоратор для проверки аутентификации"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Проверка API ключа
                api_key = request.headers.get('X-API-Key')
                if not api_key or not self.validate_api_key(api_key):
                    return jsonify({'error': 'Invalid API key'}), 401
                
                # Проверка разрешений
                if permissions:
                    user_permissions = self.get_user_permissions(api_key)
                    if not any(perm in user_permissions for perm in permissions):
                        return jsonify({'error': 'Insufficient permissions'}), 403
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator
```

### Валидация входных данных

```python
from pydantic import BaseModel, validator
from typing import List, Dict, Any, Union
import numpy as np

class InputValidator:
    """Валидатор входных данных"""
    
    def __init__(self, feature_schema: Dict[str, Any]):
        self.feature_schema = feature_schema
    
    def validate_input(self, data: List[Dict[str, Any]]) -> bool:
        """Валидация входных данных"""
        try:
            for record in data:
                # Проверка наличия всех обязательных признаков
                for feature, schema in self.feature_schema.items():
                    if feature not in record:
                        raise ValueError(f"Missing required feature: {feature}")
                    
                    # Проверка типа данных
                    if not isinstance(record[feature], schema['type']):
                        raise ValueError(f"Invalid type for feature {feature}")
                    
                    # Проверка диапазона значений
                    if 'min' in schema and record[feature] < schema['min']:
                        raise ValueError(f"Value too small for feature {feature}")
                    
                    if 'max' in schema and record[feature] > schema['max']:
                        raise ValueError(f"Value too large for feature {feature}")
            
            return True
        except Exception as e:
            print(f"Validation error: {e}")
            return False
    
    def sanitize_input(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Очистка входных данных"""
        sanitized_data = []
        
        for record in data:
            sanitized_record = {}
            for feature, value in record.items():
                # Очистка от потенциально опасных символов
                if isinstance(value, str):
                    sanitized_record[feature] = value.strip()
                else:
                    sanitized_record[feature] = value
            
            sanitized_data.append(sanitized_record)
        
        return sanitized_data
```

## Тестирование продакшен системы

### Нагрузочное тестирование

```python
import asyncio
import aiohttp
import time
from typing import List, Dict, Any
import statistics

class LoadTester:
    """Нагрузочное тестирование API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = []
    
    async def single_request(self, session: aiohttp.ClientSession, 
                           data: Dict[str, Any]) -> Dict[str, Any]:
        """Одиночный запрос"""
        start_time = time.time()
        
        try:
            async with session.post(
                f"{self.base_url}/predict",
                json={"data": [data]}
            ) as response:
                result = await response.json()
                processing_time = time.time() - start_time
                
                return {
                    'status_code': response.status,
                    'processing_time': processing_time,
                    'success': response.status == 200,
                    'result': result
                }
        except Exception as e:
            return {
                'status_code': 0,
                'processing_time': time.time() - start_time,
                'success': False,
                'error': str(e)
            }
    
    async def load_test(self, concurrent_users: int, 
                       requests_per_user: int, 
                       test_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Нагрузочное тестирование"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            for user in range(concurrent_users):
                for request in range(requests_per_user):
                    data = test_data[request % len(test_data)]
                    task = self.single_request(session, data)
                    tasks.append(task)
            
            results = await asyncio.gather(*tasks)
        
        # Анализ результатов
        successful_requests = [r for r in results if r['success']]
        failed_requests = [r for r in results if not r['success']]
        
        processing_times = [r['processing_time'] for r in successful_requests]
        
        return {
            'total_requests': len(results),
            'successful_requests': len(successful_requests),
            'failed_requests': len(failed_requests),
            'success_rate': len(successful_requests) / len(results),
            'avg_processing_time': statistics.mean(processing_times),
            'min_processing_time': min(processing_times),
            'max_processing_time': max(processing_times),
            'p95_processing_time': statistics.quantiles(processing_times, n=20)[18]
        }
```

## Следующие шаги

После освоения продакшен деплоя переходите к:
- [Переобучению моделей](./07_retraining.md)
- [Лучшим практикам](./08_best_practices.md)
- [Примерам использования](./09_examples.md)


---

# Переобучение моделей AutoML Gluon

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Введение в переобучение

![Процесс переобучения](images/retraining_workflow.png)
*Рисунок 6: Процесс переобучения моделей AutoML Gluon*

Переобучение (retraining) - это критически важный процесс для поддержания актуальности ML-моделей в продакшене. В этом разделе рассмотрим все аспекты автоматизированного переобучения моделей.

## Стратегии переобучения

### 1. Периодическое переобучение

```python
import schedule
import time
from datetime import datetime, timedelta
import pandas as pd
from autogluon.tabular import TabularPredictor
import logging

class PeriodicRetraining:
    """Периодическое переобучение моделей"""
    
    def __init__(self, model_path: str, retraining_interval: int = 7):
        self.model_path = model_path
        self.retraining_interval = retraining_interval  # дни
        self.logger = logging.getLogger(__name__)
    
    def schedule_retraining(self):
        """Планирование переобучения"""
        # Еженедельное переобучение
        schedule.every().week.do(self.retrain_model)
        
        # Ежедневная проверка необходимости переобучения
        schedule.every().day.do(self.check_retraining_need)
        
        # Запуск планировщика
        while True:
            schedule.run_pending()
            time.sleep(3600)  # Проверка каждый час
    
    def retrain_model(self):
        """Переобучение модели"""
        try:
            self.logger.info("Starting model retraining...")
            
            # Загрузка новых данных
            new_data = self.load_new_data()
            
            # Создание новой модели
            predictor = TabularPredictor(
                label='target',
                path=f"{self.model_path}_new"
            )
            
            # Обучение на новых данных
            predictor.fit(new_data, time_limit=3600)
            
            # Валидация новой модели
            if self.validate_new_model(predictor):
                # Замена старой модели
                self.deploy_new_model(predictor)
                self.logger.info("Model retraining completed successfully")
            else:
                self.logger.warning("New model validation failed, keeping old model")
                
        except Exception as e:
            self.logger.error(f"Model retraining failed: {e}")
    
    def check_retraining_need(self):
        """Проверка необходимости переобучения"""
        # Проверка качества текущей модели
        current_performance = self.evaluate_current_model()
        
        # Проверка дрейфа данных
        data_drift = self.check_data_drift()
        
        # Проверка времени последнего переобучения
        last_retraining = self.get_last_retraining_time()
        days_since_retraining = (datetime.now() - last_retraining).days
        
        # Критерии для переобучения
        if (current_performance < 0.8 or 
            data_drift > 0.1 or 
            days_since_retraining >= self.retraining_interval):
            self.logger.info("Retraining needed based on criteria")
            self.retrain_model()
```

### 2. Адаптивное переобучение

```python
class AdaptiveRetraining:
    """Адаптивное переобучение на основе производительности"""
    
    def __init__(self, model_path: str, performance_threshold: float = 0.8):
        self.model_path = model_path
        self.performance_threshold = performance_threshold
        self.performance_history = []
        self.logger = logging.getLogger(__name__)
    
    def monitor_performance(self, predictions: list, actuals: list):
        """Мониторинг производительности модели"""
        # Расчет текущей производительности
        current_performance = self.calculate_performance(predictions, actuals)
        
        # Добавление в историю
        self.performance_history.append({
            'timestamp': datetime.now(),
            'performance': current_performance
        })
        
        # Проверка тренда производительности
        if self.detect_performance_degradation():
            self.logger.warning("Performance degradation detected")
            self.trigger_retraining()
    
    def detect_performance_degradation(self) -> bool:
        """Обнаружение деградации производительности"""
        if len(self.performance_history) < 10:
            return False
        
        # Анализ тренда за последние 10 измерений
        recent_performance = [p['performance'] for p in self.performance_history[-10:]]
        
        # Проверка снижения производительности
        if (recent_performance[-1] < self.performance_threshold and
            recent_performance[-1] < recent_performance[0]):
            return True
        
        return False
    
    def trigger_retraining(self):
        """Запуск переобучения"""
        self.logger.info("Triggering adaptive retraining...")
        
        # Загрузка данных для переобучения
        retraining_data = self.load_retraining_data()
        
        # Создание и обучение новой модели
        predictor = TabularPredictor(
            label='target',
            path=f"{self.model_path}_adaptive"
        )
        
        predictor.fit(retraining_data, time_limit=3600)
        
        # Валидация и деплой
        if self.validate_new_model(predictor):
            self.deploy_new_model(predictor)
            self.performance_history = []  # Сброс истории
```

### 3. Инкрементальное переобучение

```python
class IncrementalRetraining:
    """Инкрементальное переобучение с сохранением знаний"""
    
    def __init__(self, model_path: str, batch_size: int = 1000):
        self.model_path = model_path
        self.batch_size = batch_size
        self.logger = logging.getLogger(__name__)
    
    def incremental_update(self, new_data: pd.DataFrame):
        """Инкрементальное обновление модели"""
        try:
            # Загрузка текущей модели
            current_predictor = TabularPredictor.load(self.model_path)
            
            # Объединение старых и новых данных
            combined_data = self.combine_data(current_predictor, new_data)
            
            # Обучение на объединенных данных
            updated_predictor = TabularPredictor(
                label='target',
                path=f"{self.model_path}_updated"
            )
            
            updated_predictor.fit(combined_data, time_limit=3600)
            
            # Валидация обновленной модели
            if self.validate_updated_model(updated_predictor):
                self.deploy_updated_model(updated_predictor)
                self.logger.info("Incremental update completed")
            else:
                self.logger.warning("Updated model validation failed")
                
        except Exception as e:
            self.logger.error(f"Incremental update failed: {e}")
    
    def combine_data(self, current_predictor, new_data: pd.DataFrame) -> pd.DataFrame:
        """Объединение старых и новых данных"""
        # Получение старых данных из модели (если доступно)
        old_data = self.extract_old_data(current_predictor)
        
        # Объединение данных
        if old_data is not None:
            combined_data = pd.concat([old_data, new_data], ignore_index=True)
        else:
            combined_data = new_data
        
        return combined_data
```

## Автоматизация переобучения

### Система автоматического переобучения

```python
import asyncio
import aiohttp
from typing import Dict, List, Any
import json
from datetime import datetime, timedelta

class AutomatedRetrainingSystem:
    """Система автоматического переобучения"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.retraining_queue = asyncio.Queue()
        self.is_retraining = False
    
    async def start_monitoring(self):
        """Запуск мониторинга системы"""
        tasks = [
            self.monitor_data_quality(),
            self.monitor_model_performance(),
            self.monitor_data_drift(),
            self.process_retraining_queue()
        ]
        
        await asyncio.gather(*tasks)
    
    async def monitor_data_quality(self):
        """Мониторинг качества данных"""
        while True:
            try:
                # Проверка качества новых данных
                data_quality = await self.check_data_quality()
                
                if data_quality['score'] < self.config['data_quality_threshold']:
                    self.logger.warning(f"Data quality issue: {data_quality}")
                    await self.trigger_retraining('data_quality')
                
                await asyncio.sleep(3600)  # Проверка каждый час
                
            except Exception as e:
                self.logger.error(f"Data quality monitoring error: {e}")
                await asyncio.sleep(300)
    
    async def monitor_model_performance(self):
        """Мониторинг производительности модели"""
        while True:
            try:
                # Получение метрик производительности
                performance = await self.get_model_performance()
                
                if performance['accuracy'] < self.config['performance_threshold']:
                    self.logger.warning(f"Performance degradation: {performance}")
                    await self.trigger_retraining('performance')
                
                await asyncio.sleep(1800)  # Проверка каждые 30 минут
                
            except Exception as e:
                self.logger.error(f"Performance monitoring error: {e}")
                await asyncio.sleep(300)
    
    async def monitor_data_drift(self):
        """Мониторинг дрейфа данных"""
        while True:
            try:
                # Проверка дрейфа данных
                drift_score = await self.check_data_drift()
                
                if drift_score > self.config['drift_threshold']:
                    self.logger.warning(f"Data drift detected: {drift_score}")
                    await self.trigger_retraining('data_drift')
                
                await asyncio.sleep(7200)  # Проверка каждые 2 часа
                
            except Exception as e:
                self.logger.error(f"Data drift monitoring error: {e}")
                await asyncio.sleep(300)
    
    async def trigger_retraining(self, reason: str):
        """Запуск переобучения"""
        if self.is_retraining:
            self.logger.info("Retraining already in progress")
            return
        
        retraining_request = {
            'timestamp': datetime.now().isoformat(),
            'reason': reason,
            'priority': self.get_retraining_priority(reason)
        }
        
        await self.retraining_queue.put(retraining_request)
        self.logger.info(f"Retraining queued: {retraining_request}")
    
    async def process_retraining_queue(self):
        """Обработка очереди переобучения"""
        while True:
            try:
                # Получение запроса на переобучение
                request = await self.retraining_queue.get()
                
                # Выполнение переобучения
                await self.execute_retraining(request)
                
                self.retraining_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"Retraining processing error: {e}")
                await asyncio.sleep(300)
    
    async def execute_retraining(self, request: Dict[str, Any]):
        """Выполнение переобучения"""
        self.is_retraining = True
        
        try:
            self.logger.info(f"Starting retraining: {request}")
            
            # Загрузка данных
            data = await self.load_retraining_data()
            
            # Создание новой модели
            predictor = TabularPredictor(
                label='target',
                path=f"./models/retrained_{request['timestamp']}"
            )
            
            # Обучение
            predictor.fit(data, time_limit=3600)
            
            # Валидация
            if await self.validate_new_model(predictor):
                # Деплой новой модели
                await self.deploy_new_model(predictor)
                self.logger.info("Retraining completed successfully")
            else:
                self.logger.warning("New model validation failed")
            
        except Exception as e:
            self.logger.error(f"Retraining execution failed: {e}")
        finally:
            self.is_retraining = False
```

## Валидация переобученных моделей

### Система валидации

```python
class RetrainingValidator:
    """Валидатор переобученных моделей"""
    
    def __init__(self, validation_config: Dict[str, Any]):
        self.config = validation_config
        self.logger = logging.getLogger(__name__)
    
    async def validate_new_model(self, new_predictor, old_predictor=None) -> bool:
        """Валидация новой модели"""
        try:
            # Загрузка тестовых данных
            test_data = await self.load_test_data()
            
            # Предсказания новой модели
            new_predictions = new_predictor.predict(test_data)
            new_performance = new_predictor.evaluate(test_data)
            
            # Сравнение с старой моделью (если доступна)
            if old_predictor is not None:
                old_predictions = old_predictor.predict(test_data)
                old_performance = old_predictor.evaluate(test_data)
                
                # Проверка улучшения производительности
                if not self.check_performance_improvement(new_performance, old_performance):
                    self.logger.warning("New model doesn't improve performance")
                    return False
            
            # Проверка минимальных требований
            if not self.check_minimum_requirements(new_performance):
                self.logger.warning("New model doesn't meet minimum requirements")
                return False
            
            # Проверка стабильности
            if not self.check_model_stability(new_predictor, test_data):
                self.logger.warning("New model is not stable")
                return False
            
            # Проверка совместимости
            if not self.check_compatibility(new_predictor):
                self.logger.warning("New model is not compatible")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Model validation failed: {e}")
            return False
    
    def check_performance_improvement(self, new_perf: Dict, old_perf: Dict) -> bool:
        """Проверка улучшения производительности"""
        improvement_threshold = self.config.get('improvement_threshold', 0.02)
        
        for metric in self.config['performance_metrics']:
            if metric in new_perf and metric in old_perf:
                improvement = new_perf[metric] - old_perf[metric]
                if improvement < improvement_threshold:
                    return False
        
        return True
    
    def check_minimum_requirements(self, performance: Dict) -> bool:
        """Проверка минимальных требований"""
        for metric, threshold in self.config['minimum_requirements'].items():
            if metric in performance and performance[metric] < threshold:
                return False
        
        return True
    
    def check_model_stability(self, predictor, test_data: pd.DataFrame) -> bool:
        """Проверка стабильности модели"""
        # Множественные предсказания на одних и тех же данных
        predictions = []
        for _ in range(5):
            pred = predictor.predict(test_data)
            predictions.append(pred)
        
        # Проверка согласованности
        consistency = self.calculate_prediction_consistency(predictions)
        return consistency > self.config.get('stability_threshold', 0.95)
    
    def check_compatibility(self, predictor) -> bool:
        """Проверка совместимости модели"""
        # Проверка версии AutoGluon
        if hasattr(predictor, 'version'):
            if predictor.version != self.config.get('required_version'):
                return False
        
        # Проверка формата модели
        if not self.check_model_format(predictor):
            return False
        
        return True
```

## Мониторинг переобучения

### Система мониторинга

```python
class RetrainingMonitor:
    """Мониторинг процесса переобучения"""
    
    def __init__(self, monitoring_config: Dict[str, Any]):
        self.config = monitoring_config
        self.logger = logging.getLogger(__name__)
        self.metrics = {}
    
    def start_monitoring(self, retraining_process):
        """Запуск мониторинга"""
        # Мониторинг ресурсов
        self.monitor_resources()
        
        # Мониторинг прогресса
        self.monitor_progress(retraining_process)
        
        # Мониторинг качества
        self.monitor_quality(retraining_process)
    
    def monitor_resources(self):
        """Мониторинг системных ресурсов"""
        import psutil
        
        while True:
            try:
                # CPU использование
                cpu_percent = psutil.cpu_percent()
                
                # Память
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                
                # Диск
                disk = psutil.disk_usage('/')
                disk_percent = disk.percent
                
                # Логирование метрик
                self.logger.info(f"Resources - CPU: {cpu_percent}%, Memory: {memory_percent}%, Disk: {disk_percent}%")
                
                # Проверка лимитов
                if cpu_percent > 90:
                    self.logger.warning("High CPU usage detected")
                
                if memory_percent > 90:
                    self.logger.warning("High memory usage detected")
                
                if disk_percent > 90:
                    self.logger.warning("High disk usage detected")
                
                time.sleep(60)  # Проверка каждую минуту
                
            except Exception as e:
                self.logger.error(f"Resource monitoring error: {e}")
                time.sleep(300)
    
    def monitor_progress(self, retraining_process):
        """Мониторинг прогресса переобучения"""
        start_time = datetime.now()
        
        while retraining_process.is_alive():
            elapsed_time = datetime.now() - start_time
            
            # Проверка времени выполнения
            if elapsed_time.total_seconds() > self.config.get('max_retraining_time', 7200):
                self.logger.error("Retraining timeout exceeded")
                retraining_process.terminate()
                break
            
            # Логирование прогресса
            self.logger.info(f"Retraining progress: {elapsed_time}")
            
            time.sleep(300)  # Проверка каждые 5 минут
    
    def monitor_quality(self, retraining_process):
        """Мониторинг качества переобучения"""
        # Мониторинг метрик качества
        quality_metrics = {
            'accuracy': [],
            'precision': [],
            'recall': [],
            'f1_score': []
        }
        
        while retraining_process.is_alive():
            try:
                # Получение текущих метрик
                current_metrics = self.get_current_metrics()
                
                # Добавление в историю
                for metric, value in current_metrics.items():
                    if metric in quality_metrics:
                        quality_metrics[metric].append(value)
                
                # Анализ тренда
                self.analyze_quality_trend(quality_metrics)
                
                time.sleep(600)  # Проверка каждые 10 минут
                
            except Exception as e:
                self.logger.error(f"Quality monitoring error: {e}")
                time.sleep(300)
```

## Откат моделей

### Система отката

```python
class ModelRollback:
    """Система отката моделей"""
    
    def __init__(self, rollback_config: Dict[str, Any]):
        self.config = rollback_config
        self.logger = logging.getLogger(__name__)
        self.model_versions = []
    
    def create_backup(self, model_path: str):
        """Создание резервной копии модели"""
        backup_path = f"{model_path}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Копирование модели
            import shutil
            shutil.copytree(model_path, backup_path)
            
            # Сохранение информации о версии
            version_info = {
                'timestamp': datetime.now().isoformat(),
                'path': backup_path,
                'original_path': model_path
            }
            
            self.model_versions.append(version_info)
            
            self.logger.info(f"Model backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            self.logger.error(f"Backup creation failed: {e}")
            return None
    
    def rollback_model(self, target_version: str = None):
        """Откат к предыдущей версии модели"""
        try:
            if target_version is None:
                # Откат к последней версии
                if len(self.model_versions) < 2:
                    self.logger.warning("No previous version available for rollback")
                    return False
                
                target_version = self.model_versions[-2]['path']
            else:
                # Откат к указанной версии
                target_version = self.find_version_path(target_version)
                if target_version is None:
                    self.logger.error(f"Version {target_version} not found")
                    return False
            
            # Восстановление модели
            current_path = self.config['current_model_path']
            backup_path = self.config['backup_model_path']
            
            # Создание резервной копии текущей модели
            self.create_backup(current_path)
            
            # Восстановление из резервной копии
            import shutil
            shutil.copytree(target_version, current_path, dirs_exist_ok=True)
            
            self.logger.info(f"Model rolled back to: {target_version}")
            return True
            
        except Exception as e:
            self.logger.error(f"Model rollback failed: {e}")
            return False
    
    def find_version_path(self, version_id: str) -> str:
        """Поиск пути к версии модели"""
        for version in self.model_versions:
            if version_id in version['path']:
                return version['path']
        return None
```

## Примеры использования

### Полный пример системы переобучения

```python
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from autogluon.tabular import TabularPredictor

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompleteRetrainingSystem:
    """Полная система переобучения"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.current_model = None
        self.retraining_history = []
    
    async def initialize(self):
        """Инициализация системы"""
        # Загрузка текущей модели
        self.current_model = TabularPredictor.load(self.config['model_path'])
        
        # Запуск мониторинга
        await self.start_monitoring()
    
    async def start_monitoring(self):
        """Запуск мониторинга"""
        tasks = [
            self.monitor_performance(),
            self.monitor_data_drift(),
            self.monitor_schedule()
        ]
        
        await asyncio.gather(*tasks)
    
    async def monitor_performance(self):
        """Мониторинг производительности"""
        while True:
            try:
                # Получение метрик производительности
                performance = await self.get_current_performance()
                
                # Проверка деградации
                if performance['accuracy'] < self.config['performance_threshold']:
                    self.logger.warning(f"Performance degradation detected: {performance}")
                    await self.trigger_retraining('performance_degradation')
                
                await asyncio.sleep(1800)  # Проверка каждые 30 минут
                
            except Exception as e:
                self.logger.error(f"Performance monitoring error: {e}")
                await asyncio.sleep(300)
    
    async def monitor_data_drift(self):
        """Мониторинг дрейфа данных"""
        while True:
            try:
                # Проверка дрейфа данных
                drift_score = await self.check_data_drift()
                
                if drift_score > self.config['drift_threshold']:
                    self.logger.warning(f"Data drift detected: {drift_score}")
                    await self.trigger_retraining('data_drift')
                
                await asyncio.sleep(3600)  # Проверка каждый час
                
            except Exception as e:
                self.logger.error(f"Data drift monitoring error: {e}")
                await asyncio.sleep(300)
    
    async def monitor_schedule(self):
        """Мониторинг расписания"""
        while True:
            try:
                # Проверка времени последнего переобучения
                last_retraining = self.get_last_retraining_time()
                days_since_retraining = (datetime.now() - last_retraining).days
                
                if days_since_retraining >= self.config['retraining_interval']:
                    self.logger.info("Scheduled retraining triggered")
                    await self.trigger_retraining('scheduled')
                
                await asyncio.sleep(3600)  # Проверка каждый час
                
            except Exception as e:
                self.logger.error(f"Schedule monitoring error: {e}")
                await asyncio.sleep(300)
    
    async def trigger_retraining(self, reason: str):
        """Запуск переобучения"""
        self.logger.info(f"Triggering retraining: {reason}")
        
        try:
            # Создание резервной копии
            backup_path = self.create_model_backup()
            
            # Загрузка новых данных
            new_data = await self.load_new_data()
            
            # Создание новой модели
            new_predictor = TabularPredictor(
                label=self.config['target_column'],
                path=f"{self.config['model_path']}_new"
            )
            
            # Обучение
            new_predictor.fit(new_data, time_limit=3600)
            
            # Валидация
            if await self.validate_new_model(new_predictor):
                # Деплой новой модели
                await self.deploy_new_model(new_predictor)
                
                # Обновление истории
                self.retraining_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'reason': reason,
                    'backup_path': backup_path,
                    'status': 'success'
                })
                
                self.logger.info("Retraining completed successfully")
            else:
                # Откат к предыдущей версии
                self.rollback_model(backup_path)
                
                self.retraining_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'reason': reason,
                    'backup_path': backup_path,
                    'status': 'failed'
                })
                
                self.logger.warning("Retraining failed, rolled back to previous version")
                
        except Exception as e:
            self.logger.error(f"Retraining failed: {e}")
            
            # Откат в случае ошибки
            if 'backup_path' in locals():
                self.rollback_model(backup_path)
    
    async def validate_new_model(self, new_predictor) -> bool:
        """Валидация новой модели"""
        try:
            # Загрузка тестовых данных
            test_data = await self.load_test_data()
            
            # Предсказания новой модели
            new_predictions = new_predictor.predict(test_data)
            new_performance = new_predictor.evaluate(test_data)
            
            # Сравнение с текущей моделью
            current_predictions = self.current_model.predict(test_data)
            current_performance = self.current_model.evaluate(test_data)
            
            # Проверка улучшения
            improvement = new_performance['accuracy'] - current_performance['accuracy']
            
            if improvement < self.config.get('improvement_threshold', 0.01):
                self.logger.warning(f"Insufficient improvement: {improvement}")
                return False
            
            # Проверка минимальных требований
            if new_performance['accuracy'] < self.config.get('minimum_accuracy', 0.8):
                self.logger.warning(f"Accuracy below minimum: {new_performance['accuracy']}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Model validation failed: {e}")
            return False
    
    async def deploy_new_model(self, new_predictor):
        """Деплой новой модели"""
        try:
            # Остановка текущего сервиса
            await self.stop_current_service()
            
            # Замена модели
            import shutil
            shutil.copytree(new_predictor.path, self.config['model_path'], dirs_exist_ok=True)
            
            # Обновление текущей модели
            self.current_model = new_predictor
            
            # Запуск обновленного сервиса
            await self.start_updated_service()
            
            self.logger.info("New model deployed successfully")
            
        except Exception as e:
            self.logger.error(f"Model deployment failed: {e}")
            raise
    
    def create_model_backup(self) -> str:
        """Создание резервной копии модели"""
        backup_path = f"{self.config['model_path']}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        import shutil
        shutil.copytree(self.config['model_path'], backup_path)
        
        return backup_path
    
    def rollback_model(self, backup_path: str):
        """Откат к предыдущей версии"""
        import shutil
        shutil.copytree(backup_path, self.config['model_path'], dirs_exist_ok=True)
        
        # Обновление текущей модели
        self.current_model = TabularPredictor.load(self.config['model_path'])
        
        self.logger.info(f"Model rolled back to: {backup_path}")

# Конфигурация системы
config = {
    'model_path': './production_models',
    'target_column': 'target',
    'performance_threshold': 0.8,
    'drift_threshold': 0.1,
    'retraining_interval': 7,  # дни
    'improvement_threshold': 0.01,
    'minimum_accuracy': 0.8
}

# Запуск системы
async def main():
    system = CompleteRetrainingSystem(config)
    await system.initialize()

if __name__ == "__main__":
    asyncio.run(main())
```

## Следующие шаги

После освоения переобучения моделей переходите к:
- [Лучшим практикам](./08_best_practices.md)
- [Примерам использования](./09_examples.md)
- [Troubleshooting](./10_troubleshooting.md)


---

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


---

# Примеры использования AutoML Gluon

## Введение в примеры

В этом разделе представлены практические примеры использования AutoML Gluon для различных задач машинного обучения. Каждый пример включает полный код, объяснения и лучшие практики.

## Пример 1: Классификация клиентов банка

### Задача
Предсказание вероятности дефолта клиента банка на основе финансовых показателей.

### Данные
```python
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularPredictor
import matplotlib.pyplot as plt
import seaborn as sns

# Создание синтетических данных для банковской задачи
def create_bank_data(n_samples=10000):
    """Создание синтетических банковских данных"""
    
    # Генерация данных
    X, y = make_classification(
        n_samples=n_samples,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        n_classes=2,
        random_state=42
    )
    
    # Создание DataFrame с осмысленными названиями
    feature_names = [
        'age', 'income', 'credit_score', 'debt_ratio', 'employment_years',
        'loan_amount', 'interest_rate', 'payment_history', 'savings_balance',
        'investment_value', 'credit_cards', 'late_payments', 'bankruptcies',
        'foreclosures', 'collections', 'inquiries', 'credit_utilization',
        'account_age', 'payment_frequency', 'credit_mix'
    ]
    
    data = pd.DataFrame(X, columns=feature_names)
    data['default_risk'] = y
    
    # Добавление категориальных переменных
    data['employment_status'] = np.random.choice(['employed', 'unemployed', 'self_employed'], n_samples)
    data['education'] = np.random.choice(['high_school', 'bachelor', 'master', 'phd'], n_samples)
    data['marital_status'] = np.random.choice(['single', 'married', 'divorced'], n_samples)
    
    # Добавление временных переменных
    data['application_date'] = pd.date_range('2020-01-01', periods=n_samples, freq='D')
    
    return data

# Создание данных
bank_data = create_bank_data(10000)
print("Bank data shape:", bank_data.shape)
print("Default rate:", bank_data['default_risk'].mean())
```

### Подготовка данных
```python
def prepare_bank_data(data):
    """Подготовка банковских данных"""
    
    # Обработка пропущенных значений
    data = data.fillna(data.median())
    
    # Создание новых признаков
    data['debt_to_income'] = data['debt_ratio'] * data['income']
    data['credit_utilization_ratio'] = data['credit_utilization'] / (data['credit_score'] + 1)
    data['payment_stability'] = data['payment_history'] / (data['late_payments'] + 1)
    
    # Обработка выбросов
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if col != 'default_risk':
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            data[col] = np.where(data[col] < Q1 - 1.5 * IQR, Q1 - 1.5 * IQR, data[col])
            data[col] = np.where(data[col] > Q3 + 1.5 * IQR, Q3 + 1.5 * IQR, data[col])
    
    return data

# Подготовка данных
bank_data_processed = prepare_bank_data(bank_data)
```

### Обучение модели
```python
def train_bank_model(data):
    """Обучение модели для банковской задачи"""
    
    # Разделение на train/test
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42, stratify=data['default_risk'])
    
    # Создание предиктора
    predictor = TabularPredictor(
        label='default_risk',
        problem_type='binary',
        eval_metric='roc_auc',
        path='./bank_models'
    )
    
    # Настройка гиперпараметров для банковской задачи
    hyperparameters = {
        'GBM': [
            {
                'num_boost_round': 200,
                'learning_rate': 0.1,
                'num_leaves': 31,
                'feature_fraction': 0.9,
                'bagging_fraction': 0.8,
                'min_data_in_leaf': 20
            }
        ],
        'XGB': [
            {
                'n_estimators': 200,
                'learning_rate': 0.1,
                'max_depth': 6,
                'subsample': 0.8,
                'colsample_bytree': 0.8
            }
        ],
        'CAT': [
            {
                'iterations': 200,
                'learning_rate': 0.1,
                'depth': 6,
                'l2_leaf_reg': 3.0
            }
        ]
    }
    
    # Обучение модели
    predictor.fit(
        train_data,
        hyperparameters=hyperparameters,
        time_limit=1800,  # 30 минут
        presets='high_quality',
        num_bag_folds=5,
        num_bag_sets=1
    )
    
    return predictor, test_data

# Обучение модели
bank_predictor, bank_test_data = train_bank_model(bank_data_processed)
```

### Оценка качества
```python
def evaluate_bank_model(predictor, test_data):
    """Оценка качества банковской модели"""
    
    # Предсказания
    predictions = predictor.predict(test_data)
    probabilities = predictor.predict_proba(test_data)
    
    # Оценка качества
    performance = predictor.evaluate(test_data)
    
    # Анализ важности признаков
    feature_importance = predictor.feature_importance()
    
    # Лидерборд моделей
    leaderboard = predictor.leaderboard(test_data)
    
    return {
        'performance': performance,
        'feature_importance': feature_importance,
        'leaderboard': leaderboard,
        'predictions': predictions,
        'probabilities': probabilities
    }

# Оценка модели
bank_results = evaluate_bank_model(bank_predictor, bank_test_data)

print("Bank Model Performance:")
for metric, value in bank_results['performance'].items():
    print(f"{metric}: {value:.4f}")

print("\nTop 10 Feature Importance:")
print(bank_results['feature_importance'].head(10))
```

### Визуализация результатов
```python
def visualize_bank_results(results, test_data):
    """Визуализация результатов банковской модели"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # ROC кривая
    from sklearn.metrics import roc_curve, auc
    fpr, tpr, _ = roc_curve(test_data['default_risk'], results['probabilities'][1])
    roc_auc = auc(fpr, tpr)
    
    axes[0, 0].plot(fpr, tpr, label=f'ROC AUC = {roc_auc:.3f}')
    axes[0, 0].plot([0, 1], [0, 1], 'k--')
    axes[0, 0].set_xlabel('False Positive Rate')
    axes[0, 0].set_ylabel('True Positive Rate')
    axes[0, 0].set_title('ROC Curve')
    axes[0, 0].legend()
    
    # Precision-Recall кривая
    from sklearn.metrics import precision_recall_curve
    precision, recall, _ = precision_recall_curve(test_data['default_risk'], results['probabilities'][1])
    
    axes[0, 1].plot(recall, precision)
    axes[0, 1].set_xlabel('Recall')
    axes[0, 1].set_ylabel('Precision')
    axes[0, 1].set_title('Precision-Recall Curve')
    
    # Важность признаков
    results['feature_importance'].head(10).plot(kind='barh', ax=axes[1, 0])
    axes[1, 0].set_title('Top 10 Feature Importance')
    
    # Распределение вероятностей
    axes[1, 1].hist(results['probabilities'][1], bins=50, alpha=0.7)
    axes[1, 1].set_xlabel('Default Probability')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].set_title('Distribution of Default Probabilities')
    
    plt.tight_layout()
    plt.show()

# Визуализация
visualize_bank_results(bank_results, bank_test_data)
```

## Пример 2: Прогнозирование цен на недвижимость

### Задача
Предсказание цены недвижимости на основе характеристик объекта.

### Данные
```python
def create_real_estate_data(n_samples=5000):
    """Создание синтетических данных о недвижимости"""
    
    np.random.seed(42)
    
    # Основные характеристики
    data = pd.DataFrame({
        'area': np.random.normal(120, 30, n_samples),
        'bedrooms': np.random.poisson(3, n_samples),
        'bathrooms': np.random.poisson(2, n_samples),
        'age': np.random.exponential(10, n_samples),
        'garage': np.random.binomial(1, 0.7, n_samples),
        'pool': np.random.binomial(1, 0.2, n_samples),
        'garden': np.random.binomial(1, 0.6, n_samples)
    })
    
    # Категориальные переменные
    data['location'] = np.random.choice(['downtown', 'suburbs', 'rural'], n_samples)
    data['property_type'] = np.random.choice(['house', 'apartment', 'townhouse'], n_samples)
    data['condition'] = np.random.choice(['excellent', 'good', 'fair', 'poor'], n_samples)
    
    # Создание целевой переменной (цена)
    base_price = 100000
    price = (base_price + 
             data['area'] * 1000 +
             data['bedrooms'] * 10000 +
             data['bathrooms'] * 5000 +
             data['garage'] * 15000 +
             data['pool'] * 25000 +
             data['garden'] * 10000 -
             data['age'] * 2000)
    
    # Добавление шума
    price += np.random.normal(0, 20000, n_samples)
    data['price'] = np.maximum(price, 50000)  # Минимальная цена
    
    return data

# Создание данных
real_estate_data = create_real_estate_data(5000)
print("Real estate data shape:", real_estate_data.shape)
print("Price statistics:")
print(real_estate_data['price'].describe())
```

### Подготовка данных
```python
def prepare_real_estate_data(data):
    """Подготовка данных о недвижимости"""
    
    # Создание новых признаков
    data['area_per_bedroom'] = data['area'] / (data['bedrooms'] + 1)
    data['total_rooms'] = data['bedrooms'] + data['bathrooms']
    data['age_category'] = pd.cut(data['age'], bins=[0, 5, 15, 30, 100], labels=['new', 'recent', 'old', 'very_old'])
    
    # Обработка выбросов
    data['area'] = np.where(data['area'] > 300, 300, data['area'])
    data['age'] = np.where(data['age'] > 50, 50, data['age'])
    
    return data

# Подготовка данных
real_estate_processed = prepare_real_estate_data(real_estate_data)
```

### Обучение модели
```python
def train_real_estate_model(data):
    """Обучение модели для недвижимости"""
    
    # Разделение на train/test
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
    
    # Создание предиктора
    predictor = TabularPredictor(
        label='price',
        problem_type='regression',
        eval_metric='rmse',
        path='./real_estate_models'
    )
    
    # Настройка гиперпараметров для регрессии
    hyperparameters = {
        'GBM': [
            {
                'num_boost_round': 300,
                'learning_rate': 0.1,
                'num_leaves': 31,
                'feature_fraction': 0.9,
                'bagging_fraction': 0.8,
                'min_data_in_leaf': 20
            }
        ],
        'XGB': [
            {
                'n_estimators': 300,
                'learning_rate': 0.1,
                'max_depth': 6,
                'subsample': 0.8,
                'colsample_bytree': 0.8
            }
        ],
        'RF': [
            {
                'n_estimators': 200,
                'max_depth': 15,
                'min_samples_split': 5,
                'min_samples_leaf': 2
            }
        ]
    }
    
    # Обучение модели
    predictor.fit(
        train_data,
        hyperparameters=hyperparameters,
        time_limit=1800,  # 30 минут
        presets='high_quality',
        num_bag_folds=5,
        num_bag_sets=1
    )
    
    return predictor, test_data

# Обучение модели
real_estate_predictor, real_estate_test_data = train_real_estate_model(real_estate_processed)
```

### Оценка качества
```python
def evaluate_real_estate_model(predictor, test_data):
    """Оценка качества модели недвижимости"""
    
    # Предсказания
    predictions = predictor.predict(test_data)
    
    # Оценка качества
    performance = predictor.evaluate(test_data)
    
    # Анализ важности признаков
    feature_importance = predictor.feature_importance()
    
    # Лидерборд моделей
    leaderboard = predictor.leaderboard(test_data)
    
    # Анализ ошибок
    errors = test_data['price'] - predictions
    mae = np.mean(np.abs(errors))
    mape = np.mean(np.abs(errors / test_data['price'])) * 100
    
    return {
        'performance': performance,
        'feature_importance': feature_importance,
        'leaderboard': leaderboard,
        'predictions': predictions,
        'mae': mae,
        'mape': mape,
        'errors': errors
    }

# Оценка модели
real_estate_results = evaluate_real_estate_model(real_estate_predictor, real_estate_test_data)

print("Real Estate Model Performance:")
for metric, value in real_estate_results['performance'].items():
    print(f"{metric}: {value:.4f}")

print(f"\nMAE: {real_estate_results['mae']:.2f}")
print(f"MAPE: {real_estate_results['mape']:.2f}%")
```

### Визуализация результатов
```python
def visualize_real_estate_results(results, test_data):
    """Визуализация результатов модели недвижимости"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Предсказания vs Фактические значения
    axes[0, 0].scatter(test_data['price'], results['predictions'], alpha=0.6)
    axes[0, 0].plot([test_data['price'].min(), test_data['price'].max()], 
                   [test_data['price'].min(), test_data['price'].max()], 'r--')
    axes[0, 0].set_xlabel('Actual Price')
    axes[0, 0].set_ylabel('Predicted Price')
    axes[0, 0].set_title('Predictions vs Actual')
    
    # Распределение ошибок
    axes[0, 1].hist(results['errors'], bins=50, alpha=0.7)
    axes[0, 1].set_xlabel('Prediction Error')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_title('Distribution of Prediction Errors')
    
    # Важность признаков
    results['feature_importance'].head(10).plot(kind='barh', ax=axes[1, 0])
    axes[1, 0].set_title('Top 10 Feature Importance')
    
    # Ошибки по цене
    axes[1, 1].scatter(test_data['price'], results['errors'], alpha=0.6)
    axes[1, 1].set_xlabel('Actual Price')
    axes[1, 1].set_ylabel('Prediction Error')
    axes[1, 1].set_title('Errors by Price Range')
    axes[1, 1].axhline(y=0, color='r', linestyle='--')
    
    plt.tight_layout()
    plt.show()

# Визуализация
visualize_real_estate_results(real_estate_results, real_estate_test_data)
```

## Пример 3: Анализ временных рядов

### Задача
Прогнозирование продаж товаров на основе исторических данных.

### Данные
```python
def create_sales_data(n_days=365, n_products=10):
    """Создание синтетических данных о продажах"""
    
    np.random.seed(42)
    
    # Создание временного ряда
    dates = pd.date_range('2023-01-01', periods=n_days, freq='D')
    
    data = []
    for product_id in range(n_products):
        # Базовый тренд
        trend = np.linspace(100, 150, n_days)
        
        # Сезонность (еженедельная)
        seasonality = 20 * np.sin(2 * np.pi * np.arange(n_days) / 7)
        
        # Случайный шум
        noise = np.random.normal(0, 10, n_days)
        
        # Продажи
        sales = trend + seasonality + noise
        sales = np.maximum(sales, 0)  # Негативные продажи невозможны
        
        # Создание записей
        for i, (date, sale) in enumerate(zip(dates, sales)):
            data.append({
                'date': date,
                'product_id': f'product_{product_id}',
                'sales': sale,
                'day_of_week': date.dayofweek,
                'month': date.month,
                'quarter': date.quarter
            })
    
    return pd.DataFrame(data)

# Создание данных
sales_data = create_sales_data(365, 10)
print("Sales data shape:", sales_data.shape)
print("Sales statistics:")
print(sales_data['sales'].describe())
```

### Подготовка данных для временных рядов
```python
def prepare_sales_data(data):
    """Подготовка данных о продажах для временных рядов"""
    
    # Создание лаговых признаков
    data = data.sort_values(['product_id', 'date'])
    
    for lag in [1, 2, 3, 7, 14, 30]:
        data[f'sales_lag_{lag}'] = data.groupby('product_id')['sales'].shift(lag)
    
    # Скользящие средние
    for window in [7, 14, 30]:
        data[f'sales_ma_{window}'] = data.groupby('product_id')['sales'].rolling(window=window).mean().reset_index(0, drop=True)
    
    # Тренды
    data['sales_trend'] = data.groupby('product_id')['sales'].rolling(window=7).mean().reset_index(0, drop=True)
    
    # Сезонные признаки
    data['is_weekend'] = (data['day_of_week'] >= 5).astype(int)
    data['is_month_start'] = (data['date'].dt.day <= 7).astype(int)
    data['is_month_end'] = (data['date'].dt.day >= 25).astype(int)
    
    return data

# Подготовка данных
sales_processed = prepare_sales_data(sales_data)
```

### Обучение модели временных рядов
```python
def train_sales_model(data):
    """Обучение модели для прогнозирования продаж"""
    
    # Разделение на train/test (последние 30 дней для теста)
    split_date = data['date'].max() - pd.Timedelta(days=30)
    train_data = data[data['date'] <= split_date]
    test_data = data[data['date'] > split_date]
    
    # Создание предиктора
    predictor = TabularPredictor(
        label='sales',
        problem_type='regression',
        eval_metric='rmse',
        path='./sales_models'
    )
    
    # Настройка гиперпараметров для временных рядов
    hyperparameters = {
        'GBM': [
            {
                'num_boost_round': 200,
                'learning_rate': 0.1,
                'num_leaves': 31,
                'feature_fraction': 0.9,
                'bagging_fraction': 0.8,
                'min_data_in_leaf': 20
            }
        ],
        'XGB': [
            {
                'n_estimators': 200,
                'learning_rate': 0.1,
                'max_depth': 6,
                'subsample': 0.8,
                'colsample_bytree': 0.8
            }
        ]
    }
    
    # Обучение модели
    predictor.fit(
        train_data,
        hyperparameters=hyperparameters,
        time_limit=1800,  # 30 минут
        presets='high_quality',
        num_bag_folds=3,  # Меньше фолдов для временных рядов
        num_bag_sets=1
    )
    
    return predictor, test_data

# Обучение модели
sales_predictor, sales_test_data = train_sales_model(sales_processed)
```

### Оценка качества временных рядов
```python
def evaluate_sales_model(predictor, test_data):
    """Оценка качества модели продаж"""
    
    # Предсказания
    predictions = predictor.predict(test_data)
    
    # Оценка качества
    performance = predictor.evaluate(test_data)
    
    # Анализ важности признаков
    feature_importance = predictor.feature_importance()
    
    # Анализ по продуктам
    product_performance = {}
    for product_id in test_data['product_id'].unique():
        product_data = test_data[test_data['product_id'] == product_id]
        product_predictions = predictions[test_data['product_id'] == product_id]
        
        mae = np.mean(np.abs(product_data['sales'] - product_predictions))
        mape = np.mean(np.abs((product_data['sales'] - product_predictions) / product_data['sales'])) * 100
        
        product_performance[product_id] = {
            'mae': mae,
            'mape': mape
        }
    
    return {
        'performance': performance,
        'feature_importance': feature_importance,
        'product_performance': product_performance,
        'predictions': predictions
    }

# Оценка модели
sales_results = evaluate_sales_model(sales_predictor, sales_test_data)

print("Sales Model Performance:")
for metric, value in sales_results['performance'].items():
    print(f"{metric}: {value:.4f}")

print("\nProduct Performance:")
for product, perf in sales_results['product_performance'].items():
    print(f"{product}: MAE={perf['mae']:.2f}, MAPE={perf['mape']:.2f}%")
```

### Визуализация временных рядов
```python
def visualize_sales_results(results, test_data):
    """Визуализация результатов модели продаж"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Временной ряд для одного продукта
    product_id = test_data['product_id'].iloc[0]
    product_data = test_data[test_data['product_id'] == product_id]
    product_predictions = results['predictions'][test_data['product_id'] == product_id]
    
    axes[0, 0].plot(product_data['date'], product_data['sales'], label='Actual', alpha=0.7)
    axes[0, 0].plot(product_data['date'], product_predictions, label='Predicted', alpha=0.7)
    axes[0, 0].set_title(f'Sales Forecast for {product_id}')
    axes[0, 0].set_xlabel('Date')
    axes[0, 0].set_ylabel('Sales')
    axes[0, 0].legend()
    
    # Распределение ошибок
    errors = test_data['sales'] - results['predictions']
    axes[0, 1].hist(errors, bins=30, alpha=0.7)
    axes[0, 1].set_xlabel('Prediction Error')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_title('Distribution of Prediction Errors')
    
    # Важность признаков
    results['feature_importance'].head(10).plot(kind='barh', ax=axes[1, 0])
    axes[1, 0].set_title('Top 10 Feature Importance')
    
    # Производительность по продуктам
    products = list(results['product_performance'].keys())
    maes = [results['product_performance'][p]['mae'] for p in products]
    
    axes[1, 1].bar(products, maes)
    axes[1, 1].set_xlabel('Product')
    axes[1, 1].set_ylabel('MAE')
    axes[1, 1].set_title('Performance by Product')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

# Визуализация
visualize_sales_results(sales_results, sales_test_data)
```

## Пример 4: Многоклассовая классификация

### Задача
Классификация изображений на основе извлеченных признаков.

### Данные
```python
def create_image_data(n_samples=5000, n_features=100):
    """Создание синтетических данных изображений"""
    
    np.random.seed(42)
    
    # Создание признаков изображений
    features = np.random.randn(n_samples, n_features)
    
    # Создание целевых классов
    n_classes = 5
    classes = ['cat', 'dog', 'bird', 'car', 'tree']
    y = np.random.choice(n_classes, n_samples)
    
    # Создание DataFrame
    feature_names = [f'feature_{i}' for i in range(n_features)]
    data = pd.DataFrame(features, columns=feature_names)
    data['class'] = [classes[i] for i in y]
    
    # Добавление метаданных
    data['image_size'] = np.random.choice(['small', 'medium', 'large'], n_samples)
    data['color_channels'] = np.random.choice([1, 3], n_samples)
    data['resolution'] = np.random.choice(['low', 'medium', 'high'], n_samples)
    
    return data

# Создание данных
image_data = create_image_data(5000, 100)
print("Image data shape:", image_data.shape)
print("Class distribution:")
print(image_data['class'].value_counts())
```

### Подготовка данных
```python
def prepare_image_data(data):
    """Подготовка данных изображений"""
    
    # Создание новых признаков
    data['feature_sum'] = data.select_dtypes(include=[np.number]).sum(axis=1)
    data['feature_mean'] = data.select_dtypes(include=[np.number]).mean(axis=1)
    data['feature_std'] = data.select_dtypes(include=[np.number]).std(axis=1)
    
    # Нормализация признаков
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if col != 'color_channels':
            data[col] = (data[col] - data[col].mean()) / data[col].std()
    
    return data

# Подготовка данных
image_processed = prepare_image_data(image_data)
```

### Обучение модели
```python
def train_image_model(data):
    """Обучение модели для классификации изображений"""
    
    # Разделение на train/test
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42, stratify=data['class'])
    
    # Создание предиктора
    predictor = TabularPredictor(
        label='class',
        problem_type='multiclass',
        eval_metric='accuracy',
        path='./image_models'
    )
    
    # Настройка гиперпараметров для многоклассовой классификации
    hyperparameters = {
        'GBM': [
            {
                'num_boost_round': 200,
                'learning_rate': 0.1,
                'num_leaves': 31,
                'feature_fraction': 0.9,
                'bagging_fraction': 0.8,
                'min_data_in_leaf': 20
            }
        ],
        'XGB': [
            {
                'n_estimators': 200,
                'learning_rate': 0.1,
                'max_depth': 6,
                'subsample': 0.8,
                'colsample_bytree': 0.8
            }
        ],
        'RF': [
            {
                'n_estimators': 200,
                'max_depth': 15,
                'min_samples_split': 5,
                'min_samples_leaf': 2
            }
        ]
    }
    
    # Обучение модели
    predictor.fit(
        train_data,
        hyperparameters=hyperparameters,
        time_limit=1800,  # 30 минут
        presets='high_quality',
        num_bag_folds=5,
        num_bag_sets=1
    )
    
    return predictor, test_data

# Обучение модели
image_predictor, image_test_data = train_image_model(image_processed)
```

### Оценка качества
```python
def evaluate_image_model(predictor, test_data):
    """Оценка качества модели классификации изображений"""
    
    # Предсказания
    predictions = predictor.predict(test_data)
    probabilities = predictor.predict_proba(test_data)
    
    # Оценка качества
    performance = predictor.evaluate(test_data)
    
    # Анализ важности признаков
    feature_importance = predictor.feature_importance()
    
    # Лидерборд моделей
    leaderboard = predictor.leaderboard(test_data)
    
    # Анализ по классам
    from sklearn.metrics import classification_report, confusion_matrix
    
    class_report = classification_report(test_data['class'], predictions, output_dict=True)
    conf_matrix = confusion_matrix(test_data['class'], predictions)
    
    return {
        'performance': performance,
        'feature_importance': feature_importance,
        'leaderboard': leaderboard,
        'predictions': predictions,
        'probabilities': probabilities,
        'classification_report': class_report,
        'confusion_matrix': conf_matrix
    }

# Оценка модели
image_results = evaluate_image_model(image_predictor, image_test_data)

print("Image Model Performance:")
for metric, value in image_results['performance'].items():
    print(f"{metric}: {value:.4f}")

print("\nClassification Report:")
for class_name, metrics in image_results['classification_report'].items():
    if isinstance(metrics, dict):
        print(f"{class_name}: {metrics}")
```

### Визуализация результатов
```python
def visualize_image_results(results, test_data):
    """Визуализация результатов модели классификации изображений"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Матрица ошибок
    import seaborn as sns
    sns.heatmap(results['confusion_matrix'], annot=True, fmt='d', cmap='Blues', ax=axes[0, 0])
    axes[0, 0].set_title('Confusion Matrix')
    axes[0, 0].set_xlabel('Predicted')
    axes[0, 0].set_ylabel('Actual')
    
    # Важность признаков
    results['feature_importance'].head(15).plot(kind='barh', ax=axes[0, 1])
    axes[0, 1].set_title('Top 15 Feature Importance')
    
    # Распределение предсказаний
    prediction_counts = pd.Series(results['predictions']).value_counts()
    prediction_counts.plot(kind='bar', ax=axes[1, 0])
    axes[1, 0].set_title('Distribution of Predictions')
    axes[1, 0].set_xlabel('Class')
    axes[1, 0].set_ylabel('Count')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Точность по классам
    class_accuracy = []
    for class_name in test_data['class'].unique():
        class_data = test_data[test_data['class'] == class_name]
        class_predictions = results['predictions'][test_data['class'] == class_name]
        accuracy = (class_data['class'] == class_predictions).mean()
        class_accuracy.append(accuracy)
    
    axes[1, 1].bar(test_data['class'].unique(), class_accuracy)
    axes[1, 1].set_title('Accuracy by Class')
    axes[1, 1].set_xlabel('Class')
    axes[1, 1].set_ylabel('Accuracy')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

# Визуализация
visualize_image_results(image_results, image_test_data)
```

## Пример 5: Продакшен система

### Полная продакшен система
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import logging
from datetime import datetime
from typing import Dict, List, Any
import asyncio
import aiohttp

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание FastAPI приложения
app = FastAPI(title="AutoML Gluon Production API", version="1.0.0")

# Глобальные переменные
models = {}
model_metadata = {}

class PredictionRequest(BaseModel):
    model_name: str
    data: List[Dict[str, Any]]

class PredictionResponse(BaseModel):
    predictions: List[Any]
    probabilities: List[Dict[str, float]] = None
    model_info: Dict[str, Any]
    timestamp: str

class ModelInfo(BaseModel):
    model_name: str
    model_type: str
    performance: Dict[str, float]
    features: List[str]
    created_at: str

@app.on_event("startup")
async def load_models():
    """Загрузка моделей при запуске"""
    global models, model_metadata
    
    # Загрузка банковской модели
    try:
        models['bank_default'] = TabularPredictor.load('./bank_models')
        model_metadata['bank_default'] = {
            'model_type': 'binary_classification',
            'target': 'default_risk',
            'features': ['age', 'income', 'credit_score', 'debt_ratio', 'employment_years']
        }
        logger.info("Bank model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load bank model: {e}")
    
    # Загрузка модели недвижимости
    try:
        models['real_estate'] = TabularPredictor.load('./real_estate_models')
        model_metadata['real_estate'] = {
            'model_type': 'regression',
            'target': 'price',
            'features': ['area', 'bedrooms', 'bathrooms', 'age', 'location']
        }
        logger.info("Real estate model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load real estate model: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    loaded_models = list(models.keys())
    return {
        "status": "healthy" if loaded_models else "unhealthy",
        "loaded_models": loaded_models,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Endpoint для предсказаний"""
    
    if request.model_name not in models:
        raise HTTPException(status_code=404, detail=f"Model {request.model_name} not found")
    
    try:
        model = models[request.model_name]
        metadata = model_metadata[request.model_name]
        
        # Преобразование данных
        df = pd.DataFrame(request.data)
        
        # Предсказания
        predictions = model.predict(df)
        
        # Вероятности (если доступны)
        probabilities = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(df)
            probabilities = proba.to_dict('records')
        
        return PredictionResponse(
            predictions=predictions.tolist(),
            probabilities=probabilities,
            model_info={
                "model_name": request.model_name,
                "model_type": metadata['model_type'],
                "target": metadata['target'],
                "features": metadata['features']
            },
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    """Список доступных моделей"""
    return {
        "models": list(models.keys()),
        "metadata": model_metadata
    }

@app.get("/models/{model_name}")
async def get_model_info(model_name: str):
    """Информация о модели"""
    if model_name not in models:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
    
    model = models[model_name]
    metadata = model_metadata[model_name]
    
    return {
        "model_name": model_name,
        "model_type": metadata['model_type'],
        "target": metadata['target'],
        "features": metadata['features'],
        "performance": model.evaluate(pd.DataFrame([{f: 0 for f in metadata['features']}]))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Клиент для тестирования
```python
import requests
import json

def test_production_api():
    """Тестирование продакшен API"""
    
    base_url = "http://localhost:8000"
    
    # Health check
    response = requests.get(f"{base_url}/health")
    print("Health check:", response.json())
    
    # Список моделей
    response = requests.get(f"{base_url}/models")
    print("Available models:", response.json())
    
    # Тест банковской модели
    bank_data = {
        "model_name": "bank_default",
        "data": [
            {
                "age": 35,
                "income": 50000,
                "credit_score": 750,
                "debt_ratio": 0.3,
                "employment_years": 5
            }
        ]
    }
    
    response = requests.post(f"{base_url}/predict", json=bank_data)
    print("Bank prediction:", response.json())
    
    # Тест модели недвижимости
    real_estate_data = {
        "model_name": "real_estate",
        "data": [
            {
                "area": 120,
                "bedrooms": 3,
                "bathrooms": 2,
                "age": 10,
                "location": "downtown"
            }
        ]
    }
    
    response = requests.post(f"{base_url}/predict", json=real_estate_data)
    print("Real estate prediction:", response.json())

# Запуск тестов
if __name__ == "__main__":
    test_production_api()
```

## Следующие шаги

После изучения примеров переходите к:
- [Troubleshooting](./10_troubleshooting.md)
- [Лучшим практикам](./08_best_practices.md)


---

# Troubleshooting AutoML Gluon

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Введение в troubleshooting

![Troubleshooting блок-схема](images/troubleshooting_flowchart.png)
*Рисунок 8: Блок-схема решения проблем AutoML Gluon*

В этом разделе рассмотрим типичные проблемы, возникающие при работе с AutoML Gluon, и способы их решения. Каждая проблема включает описание, причины возникновения и пошаговые инструкции по устранению.

## Проблемы установки

### 1. Ошибки зависимостей

#### Проблема: Конфликт версий пакетов
```bash
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
This behaviour is the source of the following dependency conflicts.
```

**Решение:**
```bash
# Создание нового окружения
conda create -n autogluon python=3.9
conda activate autogluon

# Установка в правильном порядке
pip install --upgrade pip
pip install autogluon

# Или установка конкретных версий
pip install autogluon==0.8.2
pip install torch==1.13.1
pip install torchvision==0.14.1
```

#### Проблема: Ошибки CUDA
```bash
RuntimeError: CUDA out of memory
```

**Решение:**
```python
# Проверка CUDA
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")

# Установка совместимой версии PyTorch
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117

# Или отключение CUDA
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
```

### 2. Проблемы с памятью

#### Проблема: Out of memory
```bash
MemoryError: Unable to allocate array
```

**Решение:**
```python
# Ограничение использования памяти
import autogluon as ag
ag.set_config({'memory_limit': 4})  # 4GB

# Или через переменные окружения
import os
os.environ['AUTOGLUON_MEMORY_LIMIT'] = '4'

# Уменьшение размера данных
train_data = train_data.sample(frac=0.5)  # Использовать 50% данных
```

## Проблемы обучения

### 1. Медленное обучение

#### Проблема: Обучение занимает слишком много времени
```python
# Диагностика
import time
start_time = time.time()

# Обучение с мониторингом
predictor.fit(train_data, time_limit=300)  # 5 минут для теста

print(f"Training time: {time.time() - start_time:.2f} seconds")
```

**Решение:**
```python
# Оптимизация параметров
predictor.fit(
    train_data,
    presets='optimize_for_deployment',  # Быстрое обучение
    time_limit=600,  # 10 минут
    num_bag_folds=3,  # Меньше фолдов
    num_bag_sets=1,
    ag_args_fit={
        'num_cpus': 2,  # Ограничение CPU
        'memory_limit': 4  # Ограничение памяти
    }
)
```

### 2. Плохое качество модели

#### Проблема: Низкая точность модели
```python
# Диагностика качества данных
def diagnose_data_quality(data):
    """Диагностика качества данных"""
    
    print("Data shape:", data.shape)
    print("Missing values:", data.isnull().sum().sum())
    print("Data types:", data.dtypes.value_counts())
    
    # Проверка целевой переменной
    if 'target' in data.columns:
        print("Target distribution:")
        print(data['target'].value_counts())
        
        # Проверка на дисбаланс
        target_counts = data['target'].value_counts()
        imbalance_ratio = target_counts.max() / target_counts.min()
        print(f"Imbalance ratio: {imbalance_ratio:.2f}")
        
        if imbalance_ratio > 10:
            print("WARNING: Severe class imbalance detected")
    
    return data

# Использование
diagnose_data_quality(train_data)
```

**Решение:**
```python
# Улучшение качества данных
def improve_data_quality(data):
    """Улучшение качества данных"""
    
    # Обработка пропущенных значений
    data = data.fillna(data.median())
    
    # Обработка выбросов
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if col != 'target':
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            data[col] = np.where(data[col] < Q1 - 1.5 * IQR, Q1 - 1.5 * IQR, data[col])
            data[col] = np.where(data[col] > Q3 + 1.5 * IQR, Q3 + 1.5 * IQR, data[col])
    
    # Создание новых признаков
    if 'feature1' in data.columns and 'feature2' in data.columns:
        data['feature_interaction'] = data['feature1'] * data['feature2']
        data['feature_ratio'] = data['feature1'] / (data['feature2'] + 1e-8)
    
    return data

# Использование
train_data_improved = improve_data_quality(train_data)
```

### 3. Ошибки валидации

#### Проблема: Ошибки при валидации
```python
# Диагностика валидации
def diagnose_validation_issues(predictor, test_data):
    """Диагностика проблем валидации"""
    
    try:
        # Проверка совместимости данных
        print("Test data shape:", test_data.shape)
        print("Test data columns:", test_data.columns.tolist())
        
        # Проверка типов данных
        print("Data types:")
        print(test_data.dtypes)
        
        # Проверка пропущенных значений
        print("Missing values:")
        print(test_data.isnull().sum())
        
        # Попытка предсказания
        predictions = predictor.predict(test_data)
        print("Predictions shape:", predictions.shape)
        
        return True
        
    except Exception as e:
        print(f"Validation error: {e}")
        return False

# Использование
if not diagnose_validation_issues(predictor, test_data):
    print("Validation issues detected")
```

**Решение:**
```python
# Исправление проблем валидации
def fix_validation_issues(test_data):
    """Исправление проблем валидации"""
    
    # Обработка пропущенных значений
    test_data = test_data.fillna(test_data.median())
    
    # Приведение типов данных
    for col in test_data.columns:
        if test_data[col].dtype == 'object':
            # Попытка преобразования в числовой тип
            try:
                test_data[col] = pd.to_numeric(test_data[col])
            except:
                # Если не удается, оставляем как есть
                pass
    
    # Удаление константных колонок
    constant_columns = test_data.columns[test_data.nunique() <= 1]
    test_data = test_data.drop(columns=constant_columns)
    
    return test_data

# Использование
test_data_fixed = fix_validation_issues(test_data)
```

## Проблемы предсказаний

### 1. Ошибки предсказаний

#### Проблема: Ошибки при предсказании
```python
# Диагностика предсказаний
def diagnose_prediction_issues(predictor, data):
    """Диагностика проблем предсказаний"""
    
    try:
        # Проверка входных данных
        print("Input data shape:", data.shape)
        print("Input data types:", data.dtypes)
        
        # Проверка совместимости с моделью
        model_features = predictor.feature_importance().index.tolist()
        data_features = data.columns.tolist()
        
        missing_features = set(model_features) - set(data_features)
        extra_features = set(data_features) - set(model_features)
        
        if missing_features:
            print(f"Missing features: {missing_features}")
        if extra_features:
            print(f"Extra features: {extra_features}")
        
        # Попытка предсказания
        predictions = predictor.predict(data)
        print("Predictions successful")
        
        return True
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return False

# Использование
if not diagnose_prediction_issues(predictor, new_data):
    print("Prediction issues detected")
```

**Решение:**
```python
# Исправление проблем предсказаний
def fix_prediction_issues(predictor, data):
    """Исправление проблем предсказаний"""
    
    # Получение ожидаемых признаков
    expected_features = predictor.feature_importance().index.tolist()
    
    # Добавление недостающих признаков
    for feature in expected_features:
        if feature not in data.columns:
            data[feature] = 0  # Заполнение нулями
    
    # Удаление лишних признаков
    data = data[expected_features]
    
    # Обработка пропущенных значений
    data = data.fillna(0)
    
    return data

# Использование
new_data_fixed = fix_prediction_issues(predictor, new_data)
predictions = predictor.predict(new_data_fixed)
```

### 2. Нестабильные предсказания

#### Проблема: Нестабильные результаты
```python
# Диагностика стабильности
def diagnose_prediction_stability(predictor, data, n_tests=5):
    """Диагностика стабильности предсказаний"""
    
    predictions = []
    
    for i in range(n_tests):
        pred = predictor.predict(data)
        predictions.append(pred)
    
    # Проверка согласованности
    predictions_array = np.array(predictions)
    consistency = np.mean(predictions_array == predictions_array[0])
    
    print(f"Prediction consistency: {consistency:.4f}")
    
    if consistency < 0.95:
        print("WARNING: Unstable predictions detected")
    
    return consistency

# Использование
consistency = diagnose_prediction_stability(predictor, test_data)
```

**Решение:**
```python
# Стабилизация предсказаний
def stabilize_predictions(predictor, data, n_samples=3):
    """Стабилизация предсказаний"""
    
    predictions = []
    
    for _ in range(n_samples):
        # Добавление небольшого шума для стабилизации
        noisy_data = data.copy()
        for col in noisy_data.columns:
            if noisy_data[col].dtype in [np.float64, np.int64]:
                noise = np.random.normal(0, 0.01, len(noisy_data))
                noisy_data[col] += noise
        
        pred = predictor.predict(noisy_data)
        predictions.append(pred)
    
    # Усреднение предсказаний
    if predictor.problem_type == 'regression':
        stable_predictions = np.mean(predictions, axis=0)
    else:
        # Для классификации - голосование
        stable_predictions = []
        for i in range(len(predictions[0])):
            votes = [pred[i] for pred in predictions]
            stable_predictions.append(max(set(votes), key=votes.count))
    
    return stable_predictions

# Использование
stable_predictions = stabilize_predictions(predictor, test_data)
```

## Проблемы производительности

### 1. Медленные предсказания

#### Проблема: Медленные предсказания
```python
# Диагностика производительности
import time

def diagnose_prediction_performance(predictor, data):
    """Диагностика производительности предсказаний"""
    
    # Тест на небольшой выборке
    small_data = data.head(100)
    
    start_time = time.time()
    predictions = predictor.predict(small_data)
    prediction_time = time.time() - start_time
    
    print(f"Prediction time for 100 samples: {prediction_time:.4f} seconds")
    print(f"Prediction time per sample: {prediction_time/100:.6f} seconds")
    
    # Оценка времени для полного датасета
    estimated_time = prediction_time * len(data) / 100
    print(f"Estimated time for full dataset: {estimated_time:.2f} seconds")
    
    return prediction_time

# Использование
prediction_time = diagnose_prediction_performance(predictor, test_data)
```

**Решение:**
```python
# Оптимизация производительности
def optimize_prediction_performance(predictor, data):
    """Оптимизация производительности предсказаний"""
    
    # Пакетная обработка
    batch_size = 1000
    predictions = []
    
    for i in range(0, len(data), batch_size):
        batch = data.iloc[i:i+batch_size]
        batch_predictions = predictor.predict(batch)
        predictions.extend(batch_predictions)
    
    return predictions

# Или использование более простой модели
def create_fast_model(predictor, data):
    """Создание быстрой модели"""
    
    fast_predictor = TabularPredictor(
        label=predictor.label,
        problem_type=predictor.problem_type,
        eval_metric=predictor.eval_metric,
        path='./fast_models'
    )
    
    # Обучение только на быстрых алгоритмах
    fast_predictor.fit(
        data,
        hyperparameters={
            'GBM': [{'num_boost_round': 50}],
            'RF': [{'n_estimators': 50}]
        },
        time_limit=300
    )
    
    return fast_predictor

# Использование
fast_predictor = create_fast_model(predictor, train_data)
fast_predictions = fast_predictor.predict(test_data)
```

### 2. Высокое использование памяти

#### Проблема: Высокое использование памяти
```python
# Диагностика памяти
import psutil
import gc

def diagnose_memory_usage():
    """Диагностика использования памяти"""
    
    process = psutil.Process()
    memory_info = process.memory_info()
    
    print(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"Memory percent: {process.memory_percent():.2f}%")
    
    return memory_info.rss / 1024 / 1024

# Использование
memory_usage = diagnose_memory_usage()
```

**Решение:**
```python
# Оптимизация памяти
def optimize_memory_usage(predictor, data):
    """Оптимизация использования памяти"""
    
    # Обработка данных по частям
    chunk_size = 1000
    predictions = []
    
    for i in range(0, len(data), chunk_size):
        chunk = data.iloc[i:i+chunk_size]
        chunk_predictions = predictor.predict(chunk)
        predictions.extend(chunk_predictions)
        
        # Очистка памяти
        del chunk
        gc.collect()
    
    return predictions

# Или использование более эффективных типов данных
def optimize_data_types(data):
    """Оптимизация типов данных"""
    
    for col in data.columns:
        if data[col].dtype == 'float64':
            data[col] = data[col].astype('float32')
        elif data[col].dtype == 'int64':
            data[col] = data[col].astype('int32')
    
    return data

# Использование
data_optimized = optimize_data_types(data)
```

## Проблемы продакшена

### 1. Ошибки загрузки модели

#### Проблема: Ошибки при загрузке модели
```python
# Диагностика загрузки модели
def diagnose_model_loading(model_path):
    """Диагностика загрузки модели"""
    
    try:
        # Проверка существования файлов
        import os
        if not os.path.exists(model_path):
            print(f"Model path does not exist: {model_path}")
            return False
        
        # Проверка структуры модели
        required_files = ['predictor.pkl', 'metadata.json']
        for file in required_files:
            file_path = os.path.join(model_path, file)
            if not os.path.exists(file_path):
                print(f"Required file missing: {file_path}")
                return False
        
        # Попытка загрузки
        predictor = TabularPredictor.load(model_path)
        print("Model loaded successfully")
        return True
        
    except Exception as e:
        print(f"Model loading error: {e}")
        return False

# Использование
if not diagnose_model_loading('./models'):
    print("Model loading issues detected")
```

**Решение:**
```python
# Исправление проблем загрузки модели
def fix_model_loading_issues(model_path):
    """Исправление проблем загрузки модели"""
    
    try:
        # Проверка версии AutoGluon
        import autogluon as ag
        print(f"AutoGluon version: {ag.__version__}")
        
        # Загрузка с проверкой совместимости
        predictor = TabularPredictor.load(
            model_path,
            require_version_match=False  # Игнорировать несовпадение версий
        )
        
        return predictor
        
    except Exception as e:
        print(f"Failed to load model: {e}")
        
        # Попытка пересоздания модели
        print("Attempting to recreate model...")
        # Здесь должна быть логика пересоздания модели
        return None

# Использование
predictor = fix_model_loading_issues('./models')
```

### 2. Ошибки API

#### Проблема: Ошибки в API
```python
# Диагностика API
def diagnose_api_issues(api_url, test_data):
    """Диагностика проблем API"""
    
    try:
        # Health check
        response = requests.get(f"{api_url}/health")
        if response.status_code != 200:
            print(f"Health check failed: {response.status_code}")
            return False
        
        # Тест предсказания
        response = requests.post(f"{api_url}/predict", json=test_data)
        if response.status_code != 200:
            print(f"Prediction failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
        
        print("API working correctly")
        return True
        
    except Exception as e:
        print(f"API error: {e}")
        return False

# Использование
if not diagnose_api_issues("http://localhost:8000", test_data):
    print("API issues detected")
```

**Решение:**
```python
# Исправление проблем API
def fix_api_issues(api_url, test_data):
    """Исправление проблем API"""
    
    try:
        # Проверка доступности API
        response = requests.get(f"{api_url}/health", timeout=5)
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"API status: {health_data['status']}")
            
            # Проверка загруженных моделей
            if 'loaded_models' in health_data:
                print(f"Loaded models: {health_data['loaded_models']}")
            
            return True
        else:
            print(f"API not healthy: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("API timeout - server may be overloaded")
        return False
    except requests.exceptions.ConnectionError:
        print("API connection error - server may be down")
        return False
    except Exception as e:
        print(f"API error: {e}")
        return False

# Использование
if fix_api_issues("http://localhost:8000", test_data):
    print("API issues resolved")
else:
    print("API issues persist")
```

## Полезные инструменты диагностики

### 1. Система мониторинга
```python
class AutoGluonMonitor:
    """Мониторинг AutoGluon системы"""
    
    def __init__(self):
        self.metrics = {}
        self.alerts = []
    
    def check_system_health(self):
        """Проверка здоровья системы"""
        
        # Проверка памяти
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            self.alerts.append("High memory usage")
        
        # Проверка CPU
        cpu = psutil.cpu_percent()
        if cpu > 90:
            self.alerts.append("High CPU usage")
        
        # Проверка диска
        disk = psutil.disk_usage('/')
        if disk.percent > 90:
            self.alerts.append("High disk usage")
        
        return len(self.alerts) == 0
    
    def check_model_performance(self, predictor, test_data):
        """Проверка производительности модели"""
        
        try:
            # Тест предсказания
            start_time = time.time()
            predictions = predictor.predict(test_data.head(100))
            prediction_time = time.time() - start_time
            
            # Проверка времени
            if prediction_time > 10:  # 10 секунд для 100 образцов
                self.alerts.append("Slow prediction performance")
            
            # Проверка качества
            performance = predictor.evaluate(test_data.head(100))
            if performance.get('accuracy', 0) < 0.8:
                self.alerts.append("Low model accuracy")
            
            return True
            
        except Exception as e:
            self.alerts.append(f"Model performance error: {e}")
            return False
    
    def generate_report(self):
        """Генерация отчета"""
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_health': self.check_system_health(),
            'alerts': self.alerts,
            'metrics': self.metrics
        }
        
        return report

# Использование
monitor = AutoGluonMonitor()
report = monitor.generate_report()
print("Monitoring report:", report)
```

### 2. Система логирования
```python
import logging
from datetime import datetime

class AutoGluonLogger:
    """Система логирования для AutoGluon"""
    
    def __init__(self, log_file='autogluon.log'):
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
    
    def log_training_start(self, data_info):
        """Логирование начала обучения"""
        self.logger.info(f"Training started: {data_info}")
    
    def log_training_complete(self, results):
        """Логирование завершения обучения"""
        self.logger.info(f"Training completed: {results}")
    
    def log_prediction(self, input_data, prediction, processing_time):
        """Логирование предсказания"""
        self.logger.info(f"Prediction: input={input_data}, prediction={prediction}, time={processing_time}")
    
    def log_error(self, error, context):
        """Логирование ошибок"""
        self.logger.error(f"Error: {error}, context: {context}")

# Использование
logger = AutoGluonLogger()
logger.log_training_start({'data_size': len(train_data)})
```

## Следующие шаги

После решения проблем переходите к:
- [Лучшим практикам](./08_best_practices.md)
- [Примерам использования](./09_examples.md)


---

# Оптимизация AutoML Gluon для Apple Silicon (M1/M2/M3)

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Введение в оптимизацию для Apple Silicon

![Оптимизация для Apple Silicon](images/apple_silicon_optimization.png)
*Рисунок 9: Оптимизация AutoML Gluon для Apple Silicon*

Apple Silicon MacBook с чипами M1, M2, M3 предоставляют уникальные возможности для ускорения машинного обучения через:
- **MLX** - фреймворк Apple для машинного обучения на Apple Silicon
- **Ray** - распределенные вычисления с поддержкой Apple Silicon
- **OpenMP** - параллельные вычисления
- **Metal Performance Shaders (MPS)** - GPU ускорение

## Установка для Apple Silicon

### 1. Базовая установка с оптимизацией

```bash
# Создание conda окружения с поддержкой Apple Silicon
conda create -n autogluon-m1 python=3.9
conda activate autogluon-m1

# Установка базовых зависимостей
conda install -c conda-forge numpy pandas scikit-learn matplotlib seaborn

# Установка PyTorch с поддержкой MPS (Metal Performance Shaders)
pip install torch torchvision torchaudio

# Установка AutoGluon
pip install autogluon
```

### 2. Установка MLX для Apple Silicon

```bash
# Установка MLX
pip install mlx mlx-lm

# Установка дополнительных MLX пакетов
pip install mlx-optimizers mlx-nn
```

### 3. Установка Ray для Apple Silicon

```bash
# Установка Ray с поддержкой Apple Silicon
pip install ray[default]

# Проверка поддержки Apple Silicon
python -c "import ray; print(ray.__version__)"
```

### 4. Настройка OpenMP

```bash
# Установка OpenMP для macOS
brew install libomp

# Установка Python биндингов
pip install openmp-python
```

## Конфигурация для Apple Silicon

### 1. Отключение CUDA и настройка MPS

```python
import os
import torch
import numpy as np

# Отключение CUDA
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

# Включение MPS (Metal Performance Shaders) для Apple Silicon
if torch.backends.mps.is_available():
    os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
    print("MPS (Metal Performance Shaders) доступен")
else:
    print("MPS недоступен")

# Настройка OpenMP для Apple Silicon
os.environ['OMP_NUM_THREADS'] = str(torch.get_num_threads())
os.environ['MKL_NUM_THREADS'] = str(torch.get_num_threads())
os.environ['OPENBLAS_NUM_THREADS'] = str(torch.get_num_threads())

# Проверка доступных устройств
print(f"PyTorch version: {torch.__version__}")
print(f"MPS available: {torch.backends.mps.is_available()}")
print(f"MPS built: {torch.backends.mps.is_built()}")
print(f"CPU threads: {torch.get_num_threads()}")
```

### 2. Настройка AutoGluon для Apple Silicon

```python
from autogluon.tabular import TabularPredictor
import autogluon as ag

# Конфигурация для Apple Silicon
def configure_apple_silicon():
    """Настройка AutoGluon для Apple Silicon"""
    
    # Отключение CUDA
    ag.set_config({
        'num_gpus': 0,
        'num_cpus': torch.get_num_threads(),
        'memory_limit': 8,  # GB
        'time_limit': 3600
    })
    
    # Настройка для MPS
    if torch.backends.mps.is_available():
        print("Используется MPS ускорение")
    else:
        print("Используется CPU")
    
    return ag

# Применение конфигурации
configure_apple_silicon()
```

## Интеграция с MLX

### 1. Создание MLX-оптимизированных моделей

```python
import mlx.core as mx
import mlx.nn as nn
from autogluon.tabular import TabularPredictor
import numpy as np

class MLXOptimizedPredictor:
    """MLX-оптимизированный предиктор для Apple Silicon"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.mlx_model = None
        self.feature_names = None
    
    def load_mlx_model(self):
        """Загрузка модели в MLX"""
        try:
            # Загрузка весов модели
            weights = mx.load(f"{self.model_path}/mlx_weights.npz")
            
            # Создание архитектуры модели
            self.mlx_model = self.create_mlx_architecture(weights)
            
            print("MLX модель загружена успешно")
            return True
            
        except Exception as e:
            print(f"Ошибка загрузки MLX модели: {e}")
            return False
    
    def create_mlx_architecture(self, weights):
        """Создание архитектуры MLX модели"""
        
        class MLXTabularModel(nn.Module):
            def __init__(self, input_size, hidden_sizes, output_size):
                super().__init__()
                self.layers = []
                
                # Входной слой
                self.layers.append(nn.Linear(input_size, hidden_sizes[0]))
                
                # Скрытые слои
                for i in range(len(hidden_sizes) - 1):
                    self.layers.append(nn.Linear(hidden_sizes[i], hidden_sizes[i + 1]))
                    self.layers.append(nn.ReLU())
                
                # Выходной слой
                self.layers.append(nn.Linear(hidden_sizes[-1], output_size))
            
            def __call__(self, x):
                for layer in self.layers:
                    x = layer(x)
                return x
        
        return MLXTabularModel
    
    def predict_mlx(self, data: np.ndarray) -> np.ndarray:
        """Предсказание с использованием MLX"""
        if self.mlx_model is None:
            raise ValueError("MLX модель не загружена")
        
        # Преобразование в MLX массив
        mlx_data = mx.array(data.astype(np.float32))
        
        # Предсказание
        with mx.eval():
            predictions = self.mlx_model(mlx_data)
        
        return np.array(predictions)

# Использование MLX предиктора
def create_mlx_predictor(model_path: str):
    """Создание MLX предиктора"""
    predictor = MLXOptimizedPredictor(model_path)
    
    if predictor.load_mlx_model():
        return predictor
    else:
        return None
```

### 2. Оптимизация данных для MLX

```python
def optimize_data_for_mlx(data: pd.DataFrame) -> np.ndarray:
    """Оптимизация данных для MLX"""
    
    # Преобразование в numpy с правильным типом
    data_array = data.select_dtypes(include=[np.number]).values.astype(np.float32)
    
    # Нормализация для MLX
    data_array = (data_array - data_array.mean(axis=0)) / (data_array.std(axis=0) + 1e-8)
    
    return data_array

# Использование
def train_with_mlx_optimization(train_data: pd.DataFrame):
    """Обучение с MLX оптимизацией"""
    
    # Оптимизация данных
    optimized_data = optimize_data_for_mlx(train_data)
    
    # Создание предиктора
    predictor = TabularPredictor(
        label='target',
        problem_type='auto',
        eval_metric='auto',
        path='./mlx_models'
    )
    
    # Обучение с оптимизацией для Apple Silicon
    predictor.fit(
        train_data,
        ag_args_fit={
            'num_cpus': torch.get_num_threads(),
            'num_gpus': 0,
            'memory_limit': 8
        },
        time_limit=3600
    )
    
    return predictor
```

## Настройка Ray для Apple Silicon

### 1. Конфигурация Ray кластера

```python
import ray
from ray import tune
import autogluon as ag

def configure_ray_apple_silicon():
    """Настройка Ray для Apple Silicon"""
    
    # Инициализация Ray с настройками для Apple Silicon
    ray.init(
        num_cpus=torch.get_num_threads(),
        num_gpus=0,  # Отключение GPU для Apple Silicon
        object_store_memory=2 * 1024 * 1024 * 1024,  # 2GB
        ignore_reinit_error=True
    )
    
    print(f"Ray кластер инициализирован: {ray.is_initialized()}")
    print(f"Доступные ресурсы: {ray.cluster_resources()}")
    
    return ray

# Инициализация Ray
ray_cluster = configure_ray_apple_silicon()
```

### 2. Распределенное обучение с Ray

```python
@ray.remote
def train_model_remote(data_chunk, model_config):
    """Удаленное обучение модели"""
    
    from autogluon.tabular import TabularPredictor
    
    # Создание предиктора
    predictor = TabularPredictor(
        label=model_config['label'],
        problem_type=model_config['problem_type'],
        eval_metric=model_config['eval_metric']
    )
    
    # Обучение на части данных
    predictor.fit(
        data_chunk,
        time_limit=model_config['time_limit'],
        presets=model_config['presets']
    )
    
    return predictor

def distributed_training_apple_silicon(data: pd.DataFrame, n_workers: int = 4):
    """Распределенное обучение для Apple Silicon"""
    
    # Разделение данных на части
    chunk_size = len(data) // n_workers
    data_chunks = [data.iloc[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    
    # Конфигурация модели
    model_config = {
        'label': 'target',
        'problem_type': 'auto',
        'eval_metric': 'auto',
        'time_limit': 1800,
        'presets': 'medium_quality'
    }
    
    # Запуск удаленных задач
    futures = []
    for chunk in data_chunks:
        future = train_model_remote.remote(chunk, model_config)
        futures.append(future)
    
    # Ожидание завершения
    results = ray.get(futures)
    
    return results

# Использование распределенного обучения
def run_distributed_training(data: pd.DataFrame):
    """Запуск распределенного обучения"""
    
    # Настройка Ray
    configure_ray_apple_silicon()
    
    # Запуск распределенного обучения
    models = distributed_training_apple_silicon(data, n_workers=4)
    
    print(f"Обучено {len(models)} моделей")
    
    return models
```

## Оптимизация OpenMP

### 1. Настройка OpenMP для Apple Silicon

```python
import os
import multiprocessing as mp

def configure_openmp_apple_silicon():
    """Настройка OpenMP для Apple Silicon"""
    
    # Получение количества ядер
    num_cores = mp.cpu_count()
    print(f"Доступно ядер: {num_cores}")
    
    # Настройка переменных окружения
    os.environ['OMP_NUM_THREADS'] = str(num_cores)
    os.environ['MKL_NUM_THREADS'] = str(num_cores)
    os.environ['OPENBLAS_NUM_THREADS'] = str(num_cores)
    os.environ['VECLIB_MAXIMUM_THREADS'] = str(num_cores)
    
    # Настройка для Apple Silicon
    os.environ['OMP_SCHEDULE'] = 'dynamic'
    os.environ['OMP_DYNAMIC'] = 'TRUE'
    os.environ['OMP_NESTED'] = 'TRUE'
    
    print("OpenMP настроен для Apple Silicon")
    
    return num_cores

# Применение настроек
num_cores = configure_openmp_apple_silicon()
```

### 2. Параллельная обработка данных

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import numpy as np

def parallel_data_processing(data: pd.DataFrame, n_workers: int = None):
    """Параллельная обработка данных для Apple Silicon"""
    
    if n_workers is None:
        n_workers = mp.cpu_count()
    
    def process_chunk(chunk):
        """Обработка части данных"""
        # Нормализация
        chunk = chunk.fillna(chunk.median())
        
        # Создание новых признаков
        if len(chunk.columns) > 1:
            chunk['feature_sum'] = chunk.sum(axis=1)
            chunk['feature_mean'] = chunk.mean(axis=1)
        
        return chunk
    
    # Разделение данных на части
    chunk_size = len(data) // n_workers
    chunks = [data.iloc[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    
    # Параллельная обработка
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        processed_chunks = list(executor.map(process_chunk, chunks))
    
    # Объединение результатов
    processed_data = pd.concat(processed_chunks, ignore_index=True)
    
    return processed_data

# Использование параллельной обработки
def optimize_data_processing(data: pd.DataFrame):
    """Оптимизация обработки данных"""
    
    # Настройка OpenMP
    configure_openmp_apple_silicon()
    
    # Параллельная обработка
    processed_data = parallel_data_processing(data)
    
    return processed_data
```

## Полная оптимизация для Apple Silicon

### 1. Комплексная настройка системы

```python
class AppleSiliconOptimizer:
    """Оптимизатор для Apple Silicon"""
    
    def __init__(self):
        self.num_cores = mp.cpu_count()
        self.mps_available = torch.backends.mps.is_available()
        self.ray_initialized = False
        
    def configure_system(self):
        """Комплексная настройка системы"""
        
        # Отключение CUDA
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
        
        # Настройка OpenMP
        self.configure_openmp()
        
        # Настройка PyTorch
        self.configure_pytorch()
        
        # Настройка AutoGluon
        self.configure_autogluon()
        
        # Настройка Ray
        self.configure_ray()
        
        print("Система оптимизирована для Apple Silicon")
    
    def configure_openmp(self):
        """Настройка OpenMP"""
        os.environ['OMP_NUM_THREADS'] = str(self.num_cores)
        os.environ['MKL_NUM_THREADS'] = str(self.num_cores)
        os.environ['OPENBLAS_NUM_THREADS'] = str(self.num_cores)
        os.environ['VECLIB_MAXIMUM_THREADS'] = str(self.num_cores)
    
    def configure_pytorch(self):
        """Настройка PyTorch"""
        if self.mps_available:
            os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
            print("MPS ускорение включено")
        else:
            print("MPS недоступен, используется CPU")
    
    def configure_autogluon(self):
        """Настройка AutoGluon"""
        ag.set_config({
            'num_cpus': self.num_cores,
            'num_gpus': 0,
            'memory_limit': 8,
            'time_limit': 3600
        })
    
    def configure_ray(self):
        """Настройка Ray"""
        try:
            ray.init(
                num_cpus=self.num_cores,
                num_gpus=0,
                object_store_memory=2 * 1024 * 1024 * 1024,
                ignore_reinit_error=True
            )
            self.ray_initialized = True
            print("Ray кластер инициализирован")
        except Exception as e:
            print(f"Ошибка инициализации Ray: {e}")
    
    def get_optimal_config(self, data_size: int) -> dict:
        """Получение оптимальной конфигурации"""
        
        if data_size < 1000:
            return {
                'presets': 'optimize_for_deployment',
                'num_bag_folds': 3,
                'num_bag_sets': 1,
                'time_limit': 600
            }
        elif data_size < 10000:
            return {
                'presets': 'medium_quality',
                'num_bag_folds': 5,
                'num_bag_sets': 1,
                'time_limit': 1800
            }
        else:
            return {
                'presets': 'high_quality',
                'num_bag_folds': 5,
                'num_bag_sets': 2,
                'time_limit': 3600
            }

# Использование оптимизатора
optimizer = AppleSiliconOptimizer()
optimizer.configure_system()
```

### 2. Оптимизированное обучение

```python
def train_optimized_apple_silicon(data: pd.DataFrame, target_col: str):
    """Оптимизированное обучение для Apple Silicon"""
    
    # Настройка системы
    optimizer = AppleSiliconOptimizer()
    optimizer.configure_system()
    
    # Получение оптимальной конфигурации
    config = optimizer.get_optimal_config(len(data))
    
    # Создание предиктора
    predictor = TabularPredictor(
        label=target_col,
        problem_type='auto',
        eval_metric='auto',
        path='./apple_silicon_models'
    )
    
    # Оптимизация данных
    optimized_data = optimize_data_for_mlx(data)
    
    # Обучение с оптимизацией
    predictor.fit(
        data,
        presets=config['presets'],
        num_bag_folds=config['num_bag_folds'],
        num_bag_sets=config['num_bag_sets'],
        time_limit=config['time_limit'],
        ag_args_fit={
            'num_cpus': optimizer.num_cores,
            'num_gpus': 0,
            'memory_limit': 8
        }
    )
    
    return predictor

# Использование
def run_optimized_training():
    """Запуск оптимизированного обучения"""
    
    # Создание тестовых данных
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=10000, n_features=20, n_classes=2, random_state=42)
    
    data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
    data['target'] = y
    
    # Оптимизированное обучение
    predictor = train_optimized_apple_silicon(data, 'target')
    
    # Тестирование
    test_data = data.sample(1000)
    predictions = predictor.predict(test_data)
    
    print(f"Обучение завершено, предсказания: {len(predictions)}")
    
    return predictor

# Запуск
if __name__ == "__main__":
    predictor = run_optimized_training()
```

## Мониторинг производительности

### 1. Система мониторинга для Apple Silicon

```python
import psutil
import time
from datetime import datetime

class AppleSiliconMonitor:
    """Мониторинг производительности для Apple Silicon"""
    
    def __init__(self):
        self.start_time = time.time()
        self.metrics = []
    
    def get_system_metrics(self):
        """Получение системных метрик"""
        
        # CPU метрики
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()
        
        # Память
        memory = psutil.virtual_memory()
        
        # Диск
        disk = psutil.disk_usage('/')
        
        # Температура (если доступна)
        try:
            temps = psutil.sensors_temperatures()
            cpu_temp = temps.get('cpu_thermal', [{}])[0].get('current', 0)
        except:
            cpu_temp = 0
        
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': cpu_percent,
            'cpu_freq': cpu_freq.current if cpu_freq else 0,
            'memory_percent': memory.percent,
            'memory_available': memory.available / (1024**3),  # GB
            'disk_percent': disk.percent,
            'cpu_temp': cpu_temp,
            'elapsed_time': time.time() - self.start_time
        }
    
    def monitor_training(self, predictor, data):
        """Мониторинг обучения"""
        
        print("Начало мониторинга обучения...")
        
        # Начальные метрики
        initial_metrics = self.get_system_metrics()
        self.metrics.append(initial_metrics)
        
        # Обучение с мониторингом
        start_time = time.time()
        predictor.fit(data, time_limit=3600)
        training_time = time.time() - start_time
        
        # Финальные метрики
        final_metrics = self.get_system_metrics()
        final_metrics['training_time'] = training_time
        self.metrics.append(final_metrics)
        
        print(f"Обучение завершено за {training_time:.2f} секунд")
        
        return final_metrics
    
    def generate_report(self):
        """Генерация отчета о производительности"""
        
        if not self.metrics:
            return "Нет данных для отчета"
        
        # Анализ метрик
        cpu_usage = [m['cpu_percent'] for m in self.metrics]
        memory_usage = [m['memory_percent'] for m in self.metrics]
        
        report = {
            'total_time': self.metrics[-1]['elapsed_time'],
            'training_time': self.metrics[-1].get('training_time', 0),
            'avg_cpu_usage': sum(cpu_usage) / len(cpu_usage),
            'max_cpu_usage': max(cpu_usage),
            'avg_memory_usage': sum(memory_usage) / len(memory_usage),
            'max_memory_usage': max(memory_usage),
            'cpu_temp': self.metrics[-1]['cpu_temp']
        }
        
        return report

# Использование мониторинга
def run_with_monitoring():
    """Запуск с мониторингом"""
    
    # Создание монитора
    monitor = AppleSiliconMonitor()
    
    # Создание данных
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=5000, n_features=20, n_classes=2, random_state=42)
    data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
    data['target'] = y
    
    # Создание предиктора
    predictor = TabularPredictor(
        label='target',
        problem_type='binary',
        eval_metric='accuracy'
    )
    
    # Обучение с мониторингом
    final_metrics = monitor.monitor_training(predictor, data)
    
    # Генерация отчета
    report = monitor.generate_report()
    print("Отчет о производительности:")
    for key, value in report.items():
        print(f"{key}: {value}")
    
    return predictor, report
```

## Примеры использования

### 1. Полный пример оптимизации

```python
def complete_apple_silicon_example():
    """Полный пример оптимизации для Apple Silicon"""
    
    print("=== Оптимизация AutoML Gluon для Apple Silicon ===")
    
    # 1. Настройка системы
    optimizer = AppleSiliconOptimizer()
    optimizer.configure_system()
    
    # 2. Создание данных
    from sklearn.datasets import make_classification
    X, y = make_classification(
        n_samples=10000,
        n_features=50,
        n_informative=30,
        n_redundant=10,
        n_classes=2,
        random_state=42
    )
    
    data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(50)])
    data['target'] = y
    
    print(f"Создан датасет: {data.shape}")
    
    # 3. Оптимизация данных
    optimized_data = optimize_data_for_mlx(data)
    print("Данные оптимизированы для MLX")
    
    # 4. Обучение с мониторингом
    monitor = AppleSiliconMonitor()
    
    predictor = TabularPredictor(
        label='target',
        problem_type='binary',
        eval_metric='accuracy',
        path='./apple_silicon_optimized'
    )
    
    # Обучение
    final_metrics = monitor.monitor_training(predictor, data)
    
    # 5. Тестирование
    test_data = data.sample(1000)
    predictions = predictor.predict(test_data)
    
    # 6. Оценка качества
    performance = predictor.evaluate(test_data)
    
    print("Результаты:")
    print(f"Производительность: {performance}")
    print(f"Время обучения: {final_metrics['training_time']:.2f} секунд")
    
    # 7. Отчет о производительности
    report = monitor.generate_report()
    print("Отчет о производительности:")
    for key, value in report.items():
        print(f"  {key}: {value}")
    
    return predictor, report

# Запуск полного примера
if __name__ == "__main__":
    predictor, report = complete_apple_silicon_example()
```

### 2. Сравнение производительности

```python
def compare_performance():
    """Сравнение производительности с оптимизацией и без"""
    
    # Создание данных
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=5000, n_features=20, n_classes=2, random_state=42)
    data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
    data['target'] = y
    
    # Тест без оптимизации
    print("=== Тест без оптимизации ===")
    start_time = time.time()
    
    predictor_basic = TabularPredictor(
        label='target',
        problem_type='binary',
        eval_metric='accuracy'
    )
    
    predictor_basic.fit(data, time_limit=600)
    basic_time = time.time() - start_time
    
    # Тест с оптимизацией
    print("=== Тест с оптимизацией ===")
    start_time = time.time()
    
    optimizer = AppleSiliconOptimizer()
    optimizer.configure_system()
    
    predictor_optimized = TabularPredictor(
        label='target',
        problem_type='binary',
        eval_metric='accuracy'
    )
    
    predictor_optimized.fit(
        data,
        time_limit=600,
        ag_args_fit={
            'num_cpus': optimizer.num_cores,
            'num_gpus': 0,
            'memory_limit': 8
        }
    )
    optimized_time = time.time() - start_time
    
    # Сравнение результатов
    print(f"Время без оптимизации: {basic_time:.2f} секунд")
    print(f"Время с оптимизацией: {optimized_time:.2f} секунд")
    print(f"Ускорение: {basic_time/optimized_time:.2f}x")
    
    return {
        'basic_time': basic_time,
        'optimized_time': optimized_time,
        'speedup': basic_time/optimized_time
    }

# Запуск сравнения
if __name__ == "__main__":
    results = compare_performance()
```

## Troubleshooting для Apple Silicon

### 1. Типичные проблемы и решения

```python
def troubleshoot_apple_silicon():
    """Решение типичных проблем для Apple Silicon"""
    
    print("=== Troubleshooting для Apple Silicon ===")
    
    # Проверка доступности MPS
    if torch.backends.mps.is_available():
        print("✓ MPS доступен")
    else:
        print("✗ MPS недоступен - используйте CPU")
    
    # Проверка Ray
    try:
        ray.init(ignore_reinit_error=True)
        print("✓ Ray инициализирован")
        ray.shutdown()
    except Exception as e:
        print(f"✗ Ошибка Ray: {e}")
    
    # Проверка OpenMP
    import os
    if 'OMP_NUM_THREADS' in os.environ:
        print(f"✓ OpenMP настроен: {os.environ['OMP_NUM_THREADS']} потоков")
    else:
        print("✗ OpenMP не настроен")
    
    # Проверка памяти
    memory = psutil.virtual_memory()
    print(f"Память: {memory.percent}% использовано, {memory.available/(1024**3):.1f}GB доступно")
    
    # Проверка CPU
    cpu_count = mp.cpu_count()
    print(f"CPU ядер: {cpu_count}")

# Запуск диагностики
if __name__ == "__main__":
    troubleshoot_apple_silicon()
```

### 2. Оптимизация для разных размеров данных

```python
def get_optimal_config_apple_silicon(data_size: int, data_type: str = 'tabular'):
    """Получение оптимальной конфигурации для Apple Silicon"""
    
    if data_size < 1000:
        return {
            'presets': 'optimize_for_deployment',
            'num_bag_folds': 3,
            'num_bag_sets': 1,
            'time_limit': 300,
            'ag_args_fit': {
                'num_cpus': min(4, mp.cpu_count()),
                'num_gpus': 0,
                'memory_limit': 4
            }
        }
    elif data_size < 10000:
        return {
            'presets': 'medium_quality',
            'num_bag_folds': 5,
            'num_bag_sets': 1,
            'time_limit': 1800,
            'ag_args_fit': {
                'num_cpus': min(8, mp.cpu_count()),
                'num_gpus': 0,
                'memory_limit': 8
            }
        }
    else:
        return {
            'presets': 'high_quality',
            'num_bag_folds': 5,
            'num_bag_sets': 2,
            'time_limit': 3600,
            'ag_args_fit': {
                'num_cpus': mp.cpu_count(),
                'num_gpus': 0,
                'memory_limit': 16
            }
        }

# Использование
def train_with_optimal_config(data: pd.DataFrame, target_col: str):
    """Обучение с оптимальной конфигурацией"""
    
    # Получение конфигурации
    config = get_optimal_config_apple_silicon(len(data))
    
    # Создание предиктора
    predictor = TabularPredictor(
        label=target_col,
        problem_type='auto',
        eval_metric='auto'
    )
    
    # Обучение с оптимальной конфигурацией
    predictor.fit(
        data,
        presets=config['presets'],
        num_bag_folds=config['num_bag_folds'],
        num_bag_sets=config['num_bag_sets'],
        time_limit=config['time_limit'],
        ag_args_fit=config['ag_args_fit']
    )
    
    return predictor
```

## Заключение

Этот раздел предоставляет полную оптимизацию AutoML Gluon для Apple Silicon MacBook M1/M2/M3, включая:

- **MLX интеграцию** для ускорения вычислений
- **Ray настройку** для распределенных вычислений
- **OpenMP оптимизацию** для параллельных вычислений
- **Отключение CUDA** и настройку MPS
- **Мониторинг производительности** для Apple Silicon
- **Troubleshooting** типичных проблем

Все настройки оптимизированы для максимальной производительности на Apple Silicon с учетом особенностей архитектуры M1/M2/M3 чипов.
