# Установка AutoML Gluon

**Автор:** NeoZorK (Shcherbyna Rostyslav)  
**Дата:** 2025  
**Местоположение:** Ukraine, Zaporizhzhya  
**Версия:** 1.0

## Почему правильная установка критически важна

**Почему 70% проблем с AutoML Gluon связаны с неправильной установкой?** Потому что машинное обучение требует точной настройки окружения. Неправильная установка может привести к нестабильной работе, ошибкам и потере времени.

### 🚨 Реальные последствия неправильной установки

**Случай 1: Конфликт версий NumPy**
```python
# Что происходит при конфликте версий
import numpy as np
# Ошибка: "numpy.core.multiarray failed to import"
# Результат: AutoML Gluon не запускается
```

**Случай 2: Проблемы с CUDA**
```python
# Что происходит без правильной CUDA
import torch
print(torch.cuda.is_available())  # False
# Результат: Обучение в 100 раз медленнее
```

**Случай 3: Нехватка памяти**
```python
# Что происходит при нехватке RAM
import pandas as pd
df = pd.read_csv('large_dataset.csv')  # MemoryError
# Результат: Невозможно обработать большие данные
```

### Что происходит при неправильной установке?
- **Конфликты зависимостей**: Разные версии библиотек вызывают ошибки
  - *Пример*: NumPy 1.19 vs 1.21 - разные API, код ломается
  - *Решение*: Использовать виртуальные окружения
- **Проблемы с производительностью**: Модели работают медленно или не работают вообще
  - *Пример*: Обучение 1 час вместо 5 минут
  - *Причина*: Неоптимальные версии библиотек
- **Ошибки компиляции**: Некоторые алгоритмы не могут быть скомпилированы
  - *Пример*: XGBoost не компилируется на старых системах
  - *Решение*: Обновить компилятор и зависимости
- **Проблемы с GPU**: CUDA не работает, обучение идет только на CPU
  - *Пример*: Обучение 10 часов вместо 1 часа
  - *Решение*: Правильная установка CUDA и cuDNN

### Что дает правильная установка?
- **Стабильная работа**: Все компоненты работают без ошибок
  - *Результат*: 99.9% времени без сбоев
  - *Экономия*: Не тратите время на отладку
- **Оптимальная производительность**: Максимальная скорость обучения
  - *Результат*: Обучение в 10-100 раз быстрее
  - *Экономия*: Часы вместо дней
- **Простота использования**: Все функции доступны из коробки
  - *Результат*: Сразу можно начинать ML-проекты
  - *Экономия*: Не нужно изучать настройку
- **Легкость обновления**: Простое обновление до новых версий
  - *Результат*: Всегда актуальные возможности
  - *Экономия*: Не нужно переустанавливать все

## Системные требования

<img src="images/optimized/installation_flowchart.png" alt="Установка AutoML Gluon" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 1: Блок-схема процесса установки AutoML Gluon*

### 🏗️ Архитектура AutoML Gluon

<img src="images/optimized/architecture_diagram.png" alt="Архитектура AutoML Gluon" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 2: Архитектурная схема AutoML Gluon*

**Почему важно понимать архитектуру?** Потому что это помогает понять, как AutoML Gluon работает внутри и почему он так эффективен:

- **TabularPredictor**: Основной компонент для работы с табличными данными
- **TimeSeriesPredictor**: Специализированный компонент для временных рядов  
- **ImagePredictor**: Компонент для работы с изображениями
- **TextPredictor**: Компонент для обработки текста
- **Ensemble Methods**: Методы объединения моделей для повышения точности
- **Feature Engineering**: Автоматическое создание новых признаков
- **Hyperparameter Tuning**: Автоматическая настройка параметров моделей

### Минимальные требования
**Почему минимальные требования важны?** Потому что они определяют, сможете ли вы вообще запустить AutoML Gluon:

- **Python**: 3.7, 3.8, 3.9, 3.10, 3.11
  - *Почему именно эти версии?* Потому что AutoML Gluon использует современные возможности Python
  - *Что происходит с Python 3.6?* Ошибки компиляции, несовместимость библиотек
  - *Что происходит с Python 3.12?* Некоторые зависимости еще не поддерживают
  - *Рекомендация*: Используйте Python 3.9 или 3.10 для стабильности
- **ОС**: Linux, macOS, Windows
  - *Почему все ОС поддерживаются?* Потому что ML-разработка ведется на разных платформах
  - *Linux*: Лучшая производительность, больше возможностей
  - *macOS*: Удобство разработки, хорошая производительность
  - *Windows*: Простота использования, но возможны проблемы с некоторыми библиотеками
- **RAM**: 4GB (рекомендуется 8GB+)
  - *Почему нужно много памяти?* Потому что ML-модели загружают большие датасеты в память
  - *Что происходит с 2GB RAM?* Система зависает, обучение прерывается
  - *Что происходит с 16GB+ RAM?* Можно обрабатывать датасеты в 10 раз больше
  - *Практический пример*: Датасет 1GB требует 4GB RAM для обработки
- **CPU**: 2 ядра (рекомендуется 4+ ядра)
  - *Почему важны ядра?* Потому что AutoML Gluon использует параллельные вычисления
  - *Что происходит с 1 ядром?* Обучение в 4 раза медленнее
  - *Что происходит с 8+ ядрами?* Обучение в 4-8 раз быстрее
  - *Практический пример*: Обучение 1 час на 2 ядрах = 15 минут на 8 ядрах
- **Диск**: 2GB свободного места
  - *Почему нужно место?* Потому что модели и данные занимают много места
  - *Что занимает место?* Модели (500MB-2GB), кэш (1-5GB), данные (зависит от размера)
  - *Практический пример*: Проект с 10 моделями занимает 5-10GB

### 📊 Сравнение производительности

<img src="images/optimized/performance_comparison.png" alt="Сравнение производительности" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 3: Сравнение производительности AutoML Gluon на разных конфигурациях*

**Почему важно понимать производительность?** Потому что это помогает выбрать оптимальную конфигурацию для ваших задач:

- **CPU vs GPU**: GPU ускоряет обучение в 10-100 раз для нейронных сетей
- **Память**: Больше RAM = возможность обрабатывать большие датасеты
- **Ядра**: Больше ядер = параллельное обучение нескольких моделей
- **Время обучения**: От 10 минут до нескольких часов в зависимости от конфигурации

### 🎯 Метрики качества моделей

<img src="images/optimized/metrics_comparison.png" alt="Сравнение метрик" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 4: Сравнение различных метрик качества моделей*

**Почему важно понимать метрики?** Потому что разные задачи требуют разных метрик для оценки качества:

- **Accuracy**: Процент правильных предсказаний (для сбалансированных данных)
- **Precision**: Точность положительных предсказаний (важно при высокой стоимости ошибок)
- **Recall**: Полнота положительных предсказаний (важно не пропустить важные случаи)
- **F1-Score**: Гармоническое среднее precision и recall (сбалансированная метрика)
- **AUC-ROC**: Площадь под ROC кривой (качество разделения классов)
- **RMSE**: Корень из среднеквадратичной ошибки (для регрессии)

### Рекомендуемые требования
**Почему рекомендуемые требования дают лучший опыт?** Потому что они обеспечивают оптимальную производительность:

- **Python**: 3.9 или 3.10
  - *Почему именно эти версии?* Потому что они наиболее стабильны и быстры
  - *Преимущества*: Лучшая производительность, стабильность, совместимость
  - *Практический пример*: Обучение на Python 3.10 на 15% быстрее чем на 3.8
- **RAM**: 16GB+
  - *Почему много памяти?* Потому что большие датасеты требуют много RAM
  - *Что можно с 16GB?* Обрабатывать датасеты до 10GB, обучать сложные модели
  - *Что можно с 32GB+?* Обрабатывать датасеты до 50GB, обучать ансамбли моделей
  - *Практический пример*: Датасет 5GB требует 20GB RAM для комфортной работы
- **CPU**: 8+ ядер
  - *Почему много ядер?* Потому что AutoML Gluon использует все доступные ядра
  - *Что происходит с 8 ядрами?* Обучение в 4-8 раз быстрее чем с 2 ядрами
  - *Что происходит с 16+ ядрами?* Обучение в 8-16 раз быстрее
  - *Практический пример*: Обучение 1 час на 2 ядрах = 7 минут на 16 ядрах
- **GPU**: NVIDIA GPU с CUDA поддержкой (опционально)
  - *Почему GPU важен?* Потому что он ускоряет обучение в 10-100 раз
  - *Минимальные требования GPU*: GTX 1060 6GB или лучше
  - *Рекомендуемые GPU*: RTX 3070, RTX 4080, A100 для профессиональной работы
  - *Практический пример*: Обучение 10 часов на CPU = 1 час на RTX 3070
- **Диск**: 10GB+ свободного места
  - *Почему много места?* Потому что модели и кэш занимают много места
  - *SSD vs HDD*: SSD в 5-10 раз быстрее для загрузки данных
  - *Практический пример*: Проект с 50 моделями занимает 20-50GB

## 🔄 Рабочие процессы AutoML Gluon

<img src="images/optimized/retraining_workflow.png" alt="Рабочий процесс переобучения" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 5: Диаграмма рабочего процесса переобучения моделей*

**Почему важно понимать рабочие процессы?** Потому что это помогает понять, как AutoML Gluon автоматизирует весь процесс машинного обучения:

- **Подготовка данных**: Автоматическая очистка и предобработка
- **Feature Engineering**: Создание новых признаков из существующих
- **Выбор алгоритмов**: Автоматический выбор лучших алгоритмов для задачи
- **Обучение моделей**: Параллельное обучение множества моделей
- **Валидация**: Автоматическая оценка качества моделей
- **Ансамблирование**: Объединение лучших моделей для повышения точности
- **Деплой**: Готовые модели для продакшена

## Установка через pip

**Почему pip - самый популярный способ установки?** Потому что он простой, надежный и автоматически решает зависимости.

## 🚀 Установка через uv (Рекомендуется)

**Почему uv лучше pip?** Потому что uv в 10-100 раз быстрее, более надежен и лучше управляет зависимостями.

### Что такое uv?
**uv** - это современный менеджер пакетов Python, написанный на Rust. Он решает все проблемы pip:

- **Скорость**: В 10-100 раз быстрее pip
- **Надежность**: Лучше разрешает конфликты зависимостей
- **Безопасность**: Проверяет целостность пакетов
- **Совместимость**: Полная совместимость с pip

### Установка uv
```bash
# Установка uv через pip (если у вас уже есть Python)
pip install uv

# Или через curl (рекомендуется)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Или через homebrew на macOS
brew install uv
```

**Что происходит при установке uv?**
- Скачивается бинарный файл uv (5-10MB)
- Устанавливается в системный PATH
- Создается конфигурационный файл
- Настраивается кэш для пакетов

### Установка AutoML Gluon через uv
```bash
# Базовая установка
uv add autogluon

# Установка с дополнительными компонентами
uv add autogluon.tabular
uv add autogluon.timeseries
uv add autogluon.vision

# Установка в виртуальное окружение
uv venv
uv pip install autogluon
```

**Преимущества uv над pip:**
- **Скорость**: Установка в 10 раз быстрее
- **Надежность**: Меньше конфликтов зависимостей
- **Кэширование**: Умное кэширование пакетов
- **Параллелизм**: Установка нескольких пакетов одновременно

### 🚀 Базовая установка
**Почему начинаем с базовой установки?** Потому что она дает все необходимое для начала работы:

```bash
pip install autogluon
```

**Что происходит при этой команде?**
- Устанавливается основной пакет AutoML Gluon
- Автоматически устанавливаются все необходимые зависимости
- Создается окружение для работы с табличными данными
- Настраивается базовая конфигурация

**Детальный процесс установки:**
```python
# Что происходит внутри pip install autogluon
# 1. Скачивание пакета (50-100MB)
# 2. Установка зависимостей:
#    - numpy, pandas, scikit-learn
#    - xgboost, lightgbm, catboost
#    - torch, torchvision
#    - matplotlib, seaborn
# 3. Проверка совместимости версий
# 4. Создание конфигурационных файлов
# 5. Тестирование установки
```

**Время установки:**
- Быстрый интернет: 5-10 минут
- Медленный интернет: 30-60 минут
- Первая установка: Дольше из-за компиляции
- Последующие обновления: Быстрее

### 🎯 Установка с дополнительными зависимостями
**Почему нужны дополнительные компоненты?** Потому что разные задачи требуют разных инструментов:

#### 📊 Для работы с табличными данными
```bash
pip install autogluon.tabular
```

**Что дает autogluon.tabular?**
- Оптимизированные алгоритмы для табличных данных
- Автоматическая обработка категориальных переменных
- Встроенная валидация и метрики
- Поддержка больших датасетов

**Детальные возможности:**
```python
# Что включает autogluon.tabular
from autogluon.tabular import TabularPredictor

# Алгоритмы:
# - XGBoost, LightGBM, CatBoost
# - Random Forest, Extra Trees
# - Neural Networks
# - Linear Models
# - Ensemble Methods

# Автоматические возможности:
# - Feature Engineering
# - Hyperparameter Tuning
# - Model Selection
# - Cross-Validation
```

**Когда использовать:**
- Классификация и регрессия
- Табличные данные (CSV, Excel, SQL)
- Структурированные данные
- Бизнес-аналитика

#### ⏰ Для работы с временными рядами
```bash
pip install autogluon.timeseries
```

**Что дает autogluon.timeseries?**
- Специальные алгоритмы для временных рядов
- Автоматическое определение сезонности
- Поддержка многомерных временных рядов
- Встроенное прогнозирование

**Детальные возможности:**
```python
# Что включает autogluon.timeseries
from autogluon.timeseries import TimeSeriesPredictor

# Алгоритмы:
# - ARIMA, SARIMA
# - Prophet, ETS
# - Deep Learning (LSTM, Transformer)
# - Ensemble Methods

# Автоматические возможности:
# - Seasonality Detection
# - Trend Analysis
# - Anomaly Detection
# - Multi-step Forecasting
```

**Когда использовать:**
- Прогнозирование продаж
- Анализ временных рядов
- Финансовые данные
- IoT данные

#### 🖼️ Для работы с изображениями
```bash
pip install autogluon.vision
```

**Что дает autogluon.vision?**
- Готовые CNN архитектуры
- Автоматическое увеличение данных
- Предобученные модели
- Поддержка GPU ускорения

```bash
# Для работы с текстом
pip install autogluon.text
```
**Что дает autogluon.text?**
- Современные NLP модели
- Автоматическая токенизация
- Предобученные эмбеддинги
- Поддержка трансформеров

```bash
# Полная установка всех компонентов
pip install autogluon[all]
```
**Почему полная установка удобна?** Потому что вы получаете все возможности сразу, но это занимает больше места и времени.

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

## 📋 Методы валидации и тестирования

<img src="images/optimized/validation_methods.png" alt="Методы валидации" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 6: Различные методы валидации моделей*

**Почему важна валидация?** Потому что она обеспечивает надежность и качество моделей:

- **Holdout Validation**: Простое разделение на train/test (70/30)
- **Cross-Validation**: K-fold кросс-валидация для более надежной оценки
- **Time Series Split**: Специальная валидация для временных рядов
- **Stratified Split**: Сохранение пропорций классов при разделении
- **Walk-Forward Analysis**: Скользящее окно для временных рядов

### 🔧 Диаграмма устранения проблем

<img src="images/optimized/troubleshooting_flowchart.png" alt="Диаграмма устранения проблем" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 7: Пошаговая диаграмма устранения проблем при установке*

**Почему нужна диаграмма устранения проблем?** Потому что она помогает быстро решить 90% проблем:

- **Проблемы с зависимостями**: Конфликты версий библиотек
- **Проблемы с памятью**: Недостаток RAM для больших датасетов
- **Проблемы с GPU**: Неправильная настройка CUDA
- **Проблемы с производительностью**: Неоптимальные настройки

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

#### 📊 Детальное описание библиотек для больших датасетов

**Dask - Распределенные вычисления для больших данных**

**Назначение:**
- Параллельная обработка данных, которые не помещаются в память
- Распределенные вычисления на нескольких ядрах/узлах
- Интеграция с pandas, numpy, scikit-learn

**Преимущества:**
- **Масштабируемость**: Обработка данных в 10-100 раз больше доступной памяти
- **Совместимость**: API похож на pandas/numpy, легко мигрировать код
- **Гибкость**: Работает на одном компьютере или кластере
- **Интеграция**: Хорошо интегрируется с AutoML Gluon
- **Отказоустойчивость**: Автоматическое восстановление после сбоев

**Недостатки:**
- **Сложность настройки**: Требует понимания распределенных систем
- **Накладные расходы**: Для малых данных может быть медленнее pandas
- **Отладка**: Сложнее отлаживать распределенный код
- **Зависимости**: Много дополнительных пакетов

**Практические примеры использования:**
```python
# Обработка больших CSV файлов
import dask.dataframe as dd

# Загрузка файла 50GB (не помещается в RAM)
df = dd.read_csv('huge_dataset.csv')  # Загружается по частям

# Операции выполняются лениво
result = df.groupby('category').sum().compute()  # Выполняется только при compute()

# Интеграция с AutoML Gluon
from autogluon.tabular import TabularPredictor
predictor = TabularPredictor(label='target')
predictor.fit(df, time_limit=3600)  # Работает с Dask DataFrame
```

**Ray - Распределенный фреймворк для ML**

**Назначение:**
- Распределенное машинное обучение
- Параллельная обработка задач
- Управление ресурсами в кластере

**Преимущества:**
- **Производительность**: Очень быстрые распределенные вычисления
- **ML-оптимизация**: Специально создан для машинного обучения
- **Автоматическое масштабирование**: Автоматически использует доступные ресурсы
- **Отказоустойчивость**: Встроенная обработка ошибок
- **Гибкость**: Поддерживает любые Python функции

**Недостатки:**
- **Сложность**: Сложнее в освоении чем Dask
- **Ресурсы**: Требует больше памяти для координации
- **Отладка**: Сложнее отлаживать распределенные задачи
- **Зависимости**: Много системных зависимостей

**Практические примеры использования:**
```python
import ray
from autogluon.tabular import TabularPredictor

# Инициализация Ray
ray.init()

# Распределенное обучение моделей
@ray.remote
def train_model(data_chunk):
    predictor = TabularPredictor(label='target')
    predictor.fit(data_chunk, time_limit=1800)
    return predictor

# Параллельное обучение на разных частях данных
futures = [train_model.remote(chunk) for chunk in data_chunks]
models = ray.get(futures)

# Ансамбль моделей
ensemble_predictions = []
for model in models:
    pred = model.predict(test_data)
    ensemble_predictions.append(pred)
```

**Modin - Ускоренный pandas**

**Назначение:**
- Ускорение операций pandas в 2-10 раз
- Автоматическое использование всех доступных ядер
- Прозрачная замена pandas

**Преимущества:**
- **Простота**: Прямая замена pandas, минимум изменений в коде
- **Скорость**: Автоматическое ускорение pandas операций
- **Совместимость**: Полная совместимость с pandas API
- **Производительность**: Использует все доступные ядра
- **Интеграция**: Легко интегрируется с существующим кодом

**Недостатки:**
- **Ограниченная функциональность**: Не все pandas функции поддерживаются
- **Память**: Может использовать больше памяти чем pandas
- **Стабильность**: Менее стабилен чем оригинальный pandas
- **Зависимости**: Требует Ray или Dask как backend

**Практические примеры использования:**
```python
# Простая замена pandas на modin
import modin.pandas as pd  # Вместо import pandas as pd

# Все операции автоматически ускоряются
df = pd.read_csv('large_dataset.csv')  # В 2-5 раз быстрее
result = df.groupby('category').sum()  # В 3-8 раз быстрее

# Интеграция с AutoML Gluon
from autogluon.tabular import TabularPredictor
predictor = TabularPredictor(label='target')
predictor.fit(df, time_limit=3600)  # Работает с Modin DataFrame
```

**Сравнение библиотек для больших данных:**

| Библиотека | Размер данных | Сложность | Скорость | Стабильность |
|------------|---------------|-----------|----------|--------------|
| **Dask** | 10GB - 1TB+ | Средняя | Высокая | Высокая |
| **Ray** | 1GB - 100GB+ | Высокая | Очень высокая | Средняя |
| **Modin** | 100MB - 10GB | Низкая | Средняя | Средняя |

**Рекомендации по выбору:**

**Используйте Dask если:**
- Данные больше доступной памяти
- Нужна максимальная совместимость с pandas
- Работаете с кластером
- Нужна отказоустойчивость

**Используйте Ray если:**
- Нужна максимальная производительность
- Работаете с ML задачами
- Есть опыт с распределенными системами
- Нужно автоматическое масштабирование

**Используйте Modin если:**
- Данные помещаются в память
- Нужно минимальное изменение кода
- Работаете на одном компьютере
- Нужно быстрое прототипирование

### Для работы с временными рядами
```bash
# Специальные библиотеки для временных рядов
pip install gluonts
pip install mxnet
pip install statsmodels
```

#### ⏰ Детальное описание библиотек для временных рядов

**GluonTS - Специализированная библиотека для временных рядов**

**Назначение:**
- Глубокое обучение для прогнозирования временных рядов
- Готовые модели для различных типов временных рядов
- Интеграция с MXNet и PyTorch
- Автоматическое определение сезонности и трендов

**Возможности:**
- **Готовые модели**: DeepAR, Transformer, WaveNet, MQ-CNN
- **Автоматическая обработка**: Определение сезонности, трендов, аномалий
- **Многомерные ряды**: Работа с несколькими связанными временными рядами
- **Неопределенность**: Квантильные прогнозы и доверительные интервалы
- **Масштабируемость**: Обработка тысяч временных рядов одновременно

**Практические примеры использования:**
```python
import gluonts
from gluonts.dataset import common
from gluonts.model.deepar import DeepAREstimator
from gluonts.trainer import Trainer

# Создание датасета для временных рядов
dataset = common.ListDataset(
    data_iter=[{"start": "2020-01-01", "target": [1, 2, 3, 4, 5]}],
    freq="D"
)

# Обучение модели DeepAR
estimator = DeepAREstimator(
    freq="D",
    prediction_length=7,
    trainer=Trainer(epochs=10)
)

# Обучение и прогнозирование
predictor = estimator.train(dataset)
forecast = predictor.predict(dataset)

# Интеграция с AutoML Gluon
from autogluon.timeseries import TimeSeriesPredictor
predictor = TimeSeriesPredictor(
    target="sales",
    prediction_length=24,
    freq="H"
)
predictor.fit(train_data, time_limit=3600)
```

**MXNet - Глубокое обучение для временных рядов**

**Назначение:**
- Гибкий фреймворк для глубокого обучения
- Оптимизация для временных рядов
- Поддержка GPU и распределенных вычислений
- Интеграция с GluonTS

**Возможности:**
- **Гибкая архитектура**: Создание кастомных моделей для временных рядов
- **GPU ускорение**: Быстрое обучение на GPU
- **Распределенность**: Обучение на кластере
- **Оптимизация**: Автоматическая оптимизация градиентов
- **Интеграция**: Хорошо работает с GluonTS

**Практические примеры использования:**
```python
import mxnet as mx
from mxnet import gluon, autograd
import numpy as np

# Создание LSTM модели для временных рядов
class LSTMPredictor(gluon.Block):
    def __init__(self, hidden_size, output_size):
        super(LSTMPredictor, self).__init__()
        self.lstm = gluon.rnn.LSTM(hidden_size)
        self.dense = gluon.nn.Dense(output_size)
    
    def forward(self, x):
        output = self.lstm(x)
        return self.dense(output[-1])

# Обучение модели
model = LSTMPredictor(hidden_size=50, output_size=1)
model.initialize()

# Интеграция с AutoML Gluon
from autogluon.timeseries import TimeSeriesPredictor
predictor = TimeSeriesPredictor(
    target="value",
    prediction_length=12,
    freq="M"
)
predictor.fit(train_data, time_limit=1800)
```

**Statsmodels - Статистические модели для временных рядов**

**Назначение:**
- Классические статистические модели
- Анализ временных рядов
- Тестирование стационарности
- Сезонная декомпозиция

**Возможности:**
- **ARIMA/SARIMA**: Классические модели авторегрессии
- **ETS**: Exponential Smoothing модели
- **Сезонная декомпозиция**: STL, X-13ARIMA-SEATS
- **Тестирование**: ADF, KPSS тесты стационарности
- **Диагностика**: ACF, PACF, Ljung-Box тесты

**Практические примеры использования:**
```python
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

# Анализ стационарности
def check_stationarity(timeseries):
    result = adfuller(timeseries)
    print(f'ADF Statistic: {result[0]}')
    print(f'p-value: {result[1]}')
    return result[1] < 0.05

# Сезонная декомпозиция
decomposition = seasonal_decompose(timeseries, model='additive')
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# ARIMA модель
model = ARIMA(timeseries, order=(1,1,1))
fitted_model = model.fit()
forecast = fitted_model.forecast(steps=12)

# Интеграция с AutoML Gluon
from autogluon.timeseries import TimeSeriesPredictor
predictor = TimeSeriesPredictor(
    target="price",
    prediction_length=30,
    freq="D"
)
predictor.fit(train_data, time_limit=3600)
```

**Сравнение библиотек для временных рядов:**

| Библиотека | Тип моделей | Сложность | Производительность | Точность |
|------------|-------------|-----------|-------------------|----------|
| **GluonTS** | Deep Learning | Высокая | Очень высокая | Очень высокая |
| **MXNet** | Custom Deep Learning | Очень высокая | Высокая | Высокая |
| **Statsmodels** | Statistical | Низкая | Средняя | Средняя |

**Рекомендации по выбору:**

**Используйте GluonTS если:**
- Нужны современные deep learning модели
- Работаете с большими объемами данных
- Нужны квантильные прогнозы
- Требуется высокая точность

**Используйте MXNet если:**
- Нужны кастомные архитектуры
- Требуется максимальная гибкость
- Работаете с GPU
- Нужно распределенное обучение

**Используйте Statsmodels если:**
- Нужны классические статистические модели
- Требуется интерпретируемость
- Работаете с малыми данными
- Нужен детальный анализ

**Интеграция с AutoML Gluon для временных рядов:**

```python
from autogluon.timeseries import TimeSeriesPredictor
import pandas as pd

# Подготовка данных
train_data = pd.DataFrame({
    'timestamp': pd.date_range('2020-01-01', periods=1000, freq='H'),
    'target': np.random.randn(1000).cumsum(),
    'feature1': np.random.randn(1000),
    'feature2': np.random.randn(1000)
})

# Создание предиктора
predictor = TimeSeriesPredictor(
    target="target",
    prediction_length=24,  # Прогноз на 24 часа
    freq="H",  # Почасовые данные
    eval_metric="MAPE"
)

# Обучение с различными моделями
predictor.fit(
    train_data,
    time_limit=3600,  # 1 час
    presets="best_quality"  # Лучшее качество
)

# Прогнозирование
predictions = predictor.predict(train_data)
print(f"Predictions shape: {predictions.shape}")

# Оценка качества
performance = predictor.evaluate(train_data)
print(f"Model performance: {performance}")
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

#### 🔧 Детальное описание переменных окружения

**OMP_NUM_THREADS - Контроль OpenMP потоков**

**Назначение:**
- Контролирует количество потоков для OpenMP операций
- Влияет на производительность numpy, scipy, scikit-learn
- Оптимизирует использование CPU ядер

**Рекомендуемые значения:**
- **2-4 ядра**: `OMP_NUM_THREADS=2`
- **4-8 ядер**: `OMP_NUM_THREADS=4`
- **8+ ядер**: `OMP_NUM_THREADS=6-8`

**Практические примеры:**
```bash
# Для системы с 8 ядрами
export OMP_NUM_THREADS=6  # Оставляем 2 ядра для системы

# Для системы с 4 ядрами
export OMP_NUM_THREADS=3  # Оставляем 1 ядро для системы

# Для системы с 16 ядрами
export OMP_NUM_THREADS=12  # Оставляем 4 ядра для системы
```

**Влияние на производительность:**
- **Слишком мало потоков**: Недоиспользование CPU
- **Слишком много потоков**: Конкуренция за ресурсы, снижение производительности
- **Оптимальное значение**: 70-80% от доступных ядер

**Проверка эффективности:**
```python
import numpy as np
import time

# Тест производительности с разным количеством потоков
def test_omp_performance():
    # Создание большой матрицы
    size = 5000
    a = np.random.randn(size, size)
    b = np.random.randn(size, size)
    
    # Измерение времени умножения матриц
    start_time = time.time()
    result = np.dot(a, b)
    end_time = time.time()
    
    print(f"Matrix multiplication time: {end_time - start_time:.2f} seconds")
    print(f"OMP_NUM_THREADS: {np.getenv('OMP_NUM_THREADS', 'default')}")

# Запуск теста
test_omp_performance()
```

**MKL_NUM_THREADS - Контроль Intel MKL потоков**

**Назначение:**
- Контролирует количество потоков для Intel Math Kernel Library
- Влияет на производительность numpy, scipy, pandas
- Оптимизирует математические операции

**Рекомендуемые значения:**
- **Должно быть равно OMP_NUM_THREADS**: `MKL_NUM_THREADS=4`
- **Для избежания конфликтов**: Не должно превышать OMP_NUM_THREADS
- **Для максимальной производительности**: Равно количеству физических ядер

**Практические примеры:**
```bash
# Синхронизация с OMP_NUM_THREADS
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4

# Для систем с Intel CPU
export MKL_NUM_THREADS=4  # Используем 4 ядра

# Для систем с AMD CPU
export MKL_NUM_THREADS=2  # Меньше потоков для AMD
```

**Влияние на производительность:**
- **Синхронизация с OMP**: Предотвращает перегрузку системы
- **Оптимизация MKL**: Максимальная производительность математических операций
- **Избежание конфликтов**: Предотвращает конкуренцию за ресурсы

**Проверка настройки:**
```python
import numpy as np

# Проверка текущих настроек
print(f"OMP_NUM_THREADS: {np.getenv('OMP_NUM_THREADS', 'not set')}")
print(f"MKL_NUM_THREADS: {np.getenv('MKL_NUM_THREADS', 'not set')}")

# Тест производительности
def test_mkl_performance():
    # Создание больших массивов
    a = np.random.randn(3000, 3000)
    b = np.random.randn(3000, 3000)
    
    # Тест различных операций
    start = time.time()
    result1 = np.dot(a, b)  # Матричное умножение
    time1 = time.time() - start
    
    start = time.time()
    result2 = np.linalg.svd(a)  # SVD разложение
    time2 = time.time() - start
    
    print(f"Matrix multiplication: {time1:.2f}s")
    print(f"SVD decomposition: {time2:.2f}s")

test_mkl_performance()
```

**OPENBLAS_NUM_THREADS - Контроль OpenBLAS потоков**

**Назначение:**
- Контролирует количество потоков для OpenBLAS библиотеки
- Альтернатива Intel MKL для систем без Intel CPU
- Влияет на производительность линейной алгебры

**Рекомендуемые значения:**
- **Для систем с Intel MKL**: Не используется (MKL имеет приоритет)
- **Для систем без MKL**: `OPENBLAS_NUM_THREADS=4`
- **Для AMD систем**: `OPENBLAS_NUM_THREADS=2-4`

**Практические примеры:**
```bash
# Для систем с Intel CPU (используется MKL)
export MKL_NUM_THREADS=4
# OPENBLAS_NUM_THREADS не нужен

# Для систем с AMD CPU (используется OpenBLAS)
export OPENBLAS_NUM_THREADS=4
export OMP_NUM_THREADS=4

# Для систем без MKL
export OPENBLAS_NUM_THREADS=4
export OMP_NUM_THREADS=4
```

**Проверка используемой библиотеки:**
```python
import numpy as np

# Проверка какой BLAS используется
print(f"NumPy BLAS info: {np.__config__.blas_opt_info}")
print(f"NumPy LAPACK info: {np.__config__.lapack_opt_info}")

# Тест производительности
def test_blas_performance():
    # Создание больших матриц
    size = 2000
    a = np.random.randn(size, size)
    b = np.random.randn(size, size)
    
    # Тест матричного умножения
    start = time.time()
    result = np.dot(a, b)
    end = time.time()
    
    print(f"Matrix multiplication time: {end - start:.2f} seconds")
    print(f"BLAS library: {np.__config__.blas_opt_info.get('libraries', ['unknown'])[0]}")

test_blas_performance()
```

**CUDA_VISIBLE_DEVICES - Контроль GPU устройств**

**Назначение:**
- Указывает какие GPU устройства использовать
- Позволяет выбирать конкретные GPU
- Контролирует доступ к GPU ресурсам

**Рекомендуемые значения:**
- **Одна GPU**: `CUDA_VISIBLE_DEVICES=0`
- **Несколько GPU**: `CUDA_VISIBLE_DEVICES=0,1`
- **Отключить GPU**: `CUDA_VISIBLE_DEVICES=""`
- **Все GPU**: `CUDA_VISIBLE_DEVICES=0,1,2,3`

**Практические примеры:**
```bash
# Использование первой GPU
export CUDA_VISIBLE_DEVICES=0

# Использование второй GPU
export CUDA_VISIBLE_DEVICES=1

# Использование двух GPU
export CUDA_VISIBLE_DEVICES=0,1

# Отключение GPU (только CPU)
export CUDA_VISIBLE_DEVICES=""

# Использование всех доступных GPU
export CUDA_VISIBLE_DEVICES=0,1,2,3
```

**Проверка GPU доступности:**
```python
import torch

# Проверка доступности CUDA
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device count: {torch.cuda.device_count()}")

# Информация о GPU
if torch.cuda.is_available():
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        print(f"GPU {i} memory: {torch.cuda.get_device_properties(i).total_memory / 1e9:.1f} GB")

# Тест производительности GPU
def test_gpu_performance():
    if torch.cuda.is_available():
        device = torch.device('cuda')
        
        # Создание больших тензоров
        size = 2000
        a = torch.randn(size, size, device=device)
        b = torch.randn(size, size, device=device)
        
        # Тест матричного умножения на GPU
        start = time.time()
        result = torch.mm(a, b)
        torch.cuda.synchronize()  # Ждем завершения
        end = time.time()
        
        print(f"GPU matrix multiplication: {end - start:.2f} seconds")
    else:
        print("GPU not available")

test_gpu_performance()
```

**AUTOGLUON_DEBUG - Режим отладки**

**Назначение:**
- Включает детальное логирование AutoML Gluon
- Помогает диагностировать проблемы
- Показывает внутренние процессы обучения

**Рекомендуемые значения:**
- **Для отладки**: `AUTOGLUON_DEBUG=1`
- **Для продакшена**: Не устанавливать (по умолчанию выключен)
- **Для разработки**: `AUTOGLUON_DEBUG=1`

**Практические примеры:**
```bash
# Включение отладки
export AUTOGLUON_DEBUG=1

# Отключение отладки
unset AUTOGLUON_DEBUG

# Временное включение для одного запуска
AUTOGLUON_DEBUG=1 python train_model.py
```

**Что показывает отладочный режим:**
```python
import os
os.environ['AUTOGLUON_DEBUG'] = '1'

from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np

# Создание тестовых данных
data = pd.DataFrame({
    'feature1': np.random.randn(100),
    'feature2': np.random.randn(100),
    'target': np.random.randint(0, 2, 100)
})

# Создание предиктора с отладкой
predictor = TabularPredictor(label='target')

# Обучение с детальным логированием
predictor.fit(data, time_limit=60)
# Выведет детальную информацию о:
# - Выборе алгоритмов
# - Процессе обучения
# - Валидации моделей
# - Создании ансамблей
```

**Полная настройка переменных окружения:**

```bash
#!/bin/bash
# Скрипт для оптимальной настройки AutoML Gluon

# Определение количества ядер
CPU_CORES=$(nproc)
RECOMMENDED_THREADS=$((CPU_CORES - 2))  # Оставляем 2 ядра для системы

# Настройка потоков
export OMP_NUM_THREADS=$RECOMMENDED_THREADS
export MKL_NUM_THREADS=$RECOMMENDED_THREADS
export OPENBLAS_NUM_THREADS=$RECOMMENDED_THREADS

# Настройка GPU
if command -v nvidia-smi &> /dev/null; then
    export CUDA_VISIBLE_DEVICES=0
    echo "GPU detected, CUDA_VISIBLE_DEVICES=0"
else
    export CUDA_VISIBLE_DEVICES=""
    echo "No GPU detected, using CPU only"
fi

# Отладочный режим (включить при необходимости)
# export AUTOGLUON_DEBUG=1

echo "Environment variables set:"
echo "OMP_NUM_THREADS=$OMP_NUM_THREADS"
echo "MKL_NUM_THREADS=$MKL_NUM_THREADS"
echo "OPENBLAS_NUM_THREADS=$OPENBLAS_NUM_THREADS"
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
```

**Проверка эффективности настроек:**

```python
import os
import time
import numpy as np
import pandas as pd
from autogluon.tabular import TabularPredictor

def benchmark_environment():
    """Тест производительности с текущими настройками"""
    
    print("=== Environment Benchmark ===")
    print(f"OMP_NUM_THREADS: {os.getenv('OMP_NUM_THREADS', 'default')}")
    print(f"MKL_NUM_THREADS: {os.getenv('MKL_NUM_THREADS', 'default')}")
    print(f"OPENBLAS_NUM_THREADS: {os.getenv('OPENBLAS_NUM_THREADS', 'default')}")
    print(f"CUDA_VISIBLE_DEVICES: {os.getenv('CUDA_VISIBLE_DEVICES', 'default')}")
    
    # Тест NumPy производительности
    print("\n=== NumPy Performance Test ===")
    size = 2000
    a = np.random.randn(size, size)
    b = np.random.randn(size, size)
    
    start = time.time()
    result = np.dot(a, b)
    numpy_time = time.time() - start
    print(f"Matrix multiplication: {numpy_time:.2f} seconds")
    
    # Тест AutoML Gluon
    print("\n=== AutoML Gluon Test ===")
    data = pd.DataFrame({
        'feature1': np.random.randn(1000),
        'feature2': np.random.randn(1000),
        'target': np.random.randint(0, 2, 1000)
    })
    
    predictor = TabularPredictor(label='target')
    
    start = time.time()
    predictor.fit(data, time_limit=30)
    autogluon_time = time.time() - start
    print(f"AutoML training: {autogluon_time:.2f} seconds")
    
    return numpy_time, autogluon_time

# Запуск теста
benchmark_environment()
```

### 📋 Конфигурационный файл
**Почему нужен конфигурационный файл?** Потому что он позволяет настроить AutoML Gluon под ваши ресурсы и задачи без изменения кода.

Создайте файл `~/.autogluon/config.yaml`:
```yaml
# Конфигурация AutoGluon
default:
  time_limit: 3600  # 1 час по умолчанию
  memory_limit: 8  # 8GB RAM
  num_cpus: 4  # Количество CPU ядер
  num_gpus: 1  # Количество GPU

# Настройки для разных задач
```

#### 🔧 Детальное описание параметров конфигурации

**Параметр `time_limit`:**

- **Что означает**: Максимальное время обучения в секундах
- **Зачем нужен**: Предотвращает бесконечное обучение, контролирует ресурсы
- **Рекомендуемые значения**:
  - `3600` (1 час) - для быстрых экспериментов
  - `7200` (2 часа) - для средних задач
  - `14400` (4 часа) - для сложных задач
- **Что происходит при превышении**: Обучение останавливается, возвращается лучшая модель
- **Практический пример**: Если у вас есть 2 часа на задачу, установите `time_limit: 7200`
- **Детальная настройка по типам задач**:
  - **Классификация (малые данные < 10K строк)**: `1800` (30 минут)
- **Классификация (средние данные 10K-100K строк)**: `3600` (1 час)
- **Классификация (большие данные > 100K строк)**: `7200` (2 часа)
- **Регрессия (малые данные < 10K строк)**: `1800` (30 минут)
- **Регрессия (средние данные 10K-100K строк)**: `5400` (1.5 часа)
- **Регрессия (большие данные > 100K строк)**: `10800` (3 часа)
- **Временные ряды (короткие серии < 1K точек)**: `3600` (1 час)
- **Временные ряды (длинные серии > 1K точек)**: `7200` (2 часа)
- **Влияние на качество модели**:
  - **Короткое время (30 мин)**: Базовая точность, быстрые результаты
- **Среднее время (1-2 часа)**: Хорошая точность, сбалансированный подход
- **Длинное время (4+ часов)**: Максимальная точность, лучшие модели
- **Оптимизация по ресурсам**:
  - **CPU только**: Увеличить время в 2-3 раза
- **GPU доступна**: Уменьшить время в 2-3 раза
- **Много ядер (8+)**: Уменьшить время на 30-50%
- **Мало памяти (< 8GB)**: Увеличить время из-за ограничений

**Параметр `memory_limit`:**

- **Что означает**: Максимальное использование RAM в гигабайтах
- **Зачем нужен**: Предотвращает переполнение памяти, контролирует ресурсы
- **Рекомендуемые значения**:
  - `4` - для систем с 8GB RAM
  - `8` - для систем с 16GB RAM
  - `16` - для систем с 32GB RAM
- **Что происходит при превышении**: Обучение останавливается с ошибкой памяти
- **Практический пример**: Если у вас 16GB RAM, установите `memory_limit: 12` (оставляя 4GB для системы)
- **Детальная настройка по размеру данных**:
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
- **Изображения**: 6-10x размер данных
- **Мониторинг использования памяти**:
  - **Проверка**: `import psutil; print(f"RAM usage: {psutil.virtual_memory().percent}%")`
- **Оптимальное использование**: 70-80% от доступной памяти
- **Критическое использование**: > 90% от доступной памяти

**Параметр `num_cpus`:**

- **Что означает**: Количество CPU ядер для параллельных вычислений
- **Зачем нужен**: Ускоряет обучение, использует все доступные ядра
- **Рекомендуемые значения**:
  - `2` - для систем с 4 ядрами
  - `4` - для систем с 8 ядрами
  - `8` - для систем с 16+ ядрами
- **Что происходит при превышении**: Используется только доступное количество ядер
- **Практический пример**: Если у вас 8 ядер, установите `num_cpus: 6` (оставляя 2 для системы)
- **Детальная настройка по типам задач**:
  - **Классификация (малые данные)**: `2-4` ядра
- **Классификация (большие данные)**: `4-8` ядер
- **Регрессия (малые данные)**: `2-4` ядра
- **Регрессия (большие данные)**: `6-12` ядер
- **Временные ряды**: `4-8` ядер
- **Изображения**: `8-16` ядер
- **Влияние на скорость обучения**:
  - **1 ядро**: Базовая скорость (100%)
- **2 ядра**: Ускорение в 1.5-1.8 раза
- **4 ядра**: Ускорение в 2.5-3.5 раза
- **8 ядер**: Ускорение в 4-6 раз
- **16+ ядер**: Ускорение в 6-10 раз
- **Оптимизация по алгоритмам**:
  - **XGBoost**: Эффективно использует 4-8 ядер
- **LightGBM**: Эффективно использует 4-12 ядер
- **CatBoost**: Эффективно использует 2-8 ядер
- **Neural Networks**: Эффективно использует 8-16 ядер
- **Мониторинг использования CPU**:
  - **Проверка**: `import psutil; print(f"CPU usage: {psutil.cpu_percent()}%")`
- **Оптимальное использование**: 80-90% от доступных ядер
- **Перегрузка**: > 95% от доступных ядер

**Параметр `num_gpus`:**

- **Что означает**: Количество GPU для ускорения обучения
- **Зачем нужен**: Ускоряет обучение нейронных сетей в 10-100 раз
- **Рекомендуемые значения**:
  - `0` - если нет GPU или для CPU-only задач
  - `1` - для одной GPU
  - `2+` - для нескольких GPU (требует специальной настройки)
- **Что происходит при неправильном значении**: AutoML Gluon автоматически определяет доступные GPU
- **Практический пример**: Если у вас RTX 3070, установите `num_gpus: 1`
- **Детальная настройка по типам GPU**:
  - **Нет GPU**: `num_gpus: 0` - обучение только на CPU
- **GTX 1060 6GB**: `num_gpus: 1` - базовая поддержка GPU
- **RTX 3070 8GB**: `num_gpus: 1` - хорошая производительность
- **RTX 4080 16GB**: `num_gpus: 1` - высокая производительность
- **A100 40GB**: `num_gpus: 1` - профессиональная работа
- **Несколько GPU**: `num_gpus: 2+` - для больших моделей
- **Влияние на скорость обучения**:
  - **CPU только**: Базовая скорость (100%)
- **GTX 1060**: Ускорение в 3-5 раз
- **RTX 3070**: Ускорение в 8-15 раз
- **RTX 4080**: Ускорение в 15-25 раз
- **A100**: Ускорение в 25-50 раз
- **Оптимизация по типам задач**:
  - **Классификация (табличные данные)**: GPU не критична
- **Регрессия (табличные данные)**: GPU не критична
- **Временные ряды**: GPU ускоряет в 2-5 раз
- **Изображения**: GPU критична, ускорение в 10-50 раз
- **Текст**: GPU ускоряет в 5-20 раз
- **Требования к памяти GPU**:
  - **Малые модели (< 1M параметров)**: 2-4 GB VRAM
- **Средние модели (1-10M параметров)**: 4-8 GB VRAM
- **Большие модели (10-100M параметров)**: 8-16 GB VRAM
- **Очень большие модели (> 100M параметров)**: 16+ GB VRAM
- **Проверка доступности GPU**:
  - **Проверка CUDA**: `python -c "import torch; print(torch.cuda.is_available())"`
- **Количество GPU**: `python -c "import torch; print(torch.cuda.device_count())"`
- **Информация о GPU**: `python -c "import torch; print(torch.cuda.get_device_name(0))"`
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

#### 🎯 Детальное описание параметров для табличных данных

**Параметр `presets`:**

- **Что означает**: Предустановленные конфигурации качества модели
- **Зачем нужен**: Упрощает выбор между скоростью и качеством
- **Детальное описание каждого preset**: **`best_quality`:**
- **Что делает**: Максимальное качество модели
- **Время обучения**: 4-8 часов
- **Использует**: Все доступные алгоритмы, ансамбли, тюнинг гиперпараметров
- **Когда использовать**: Для продакшена, когда качество критично
- **Результат**: Лучшая точность, но долгое обучение

  **`high_quality`:**
- **Что делает**: Высокое качество с разумным временем
- **Время обучения**: 2-4 часа
- **Использует**: Основные алгоритмы + ансамбли
- **Когда использовать**: Для большинства задач
- **Результат**: Хорошая точность за разумное время

  **`good_quality`:**
- **Что делает**: Хорошее качество за короткое время
- **Время обучения**: 30-60 минут
- **Использует**: Основные алгоритмы без ансамблей
- **Когда использовать**: Для быстрых экспериментов
- **Результат**: Приемлемая точность быстро

  **`medium_quality`:**
- **Что делает**: Среднее качество за очень короткое время
- **Время обучения**: 10-30 минут
- **Использует**: Только быстрые алгоритмы
- **Когда использовать**: Для прототипирования
- **Результат**: Базовая точность очень быстро

  **`optimize_for_deployment`:**
- **Что делает**: Оптимизация для продакшена
- **Время обучения**: 1-2 часа
- **Использует**: Быстрые алгоритмы с оптимизацией
- **Когда использовать**: Для продакшена с ограничениями ресурсов
- **Результат**: Быстрые предсказания, хорошая точность

**Параметр `num_trials`:**

- **Что означает**: Количество попыток тюнинга гиперпараметров
- **Зачем нужен**: Больше попыток = лучше качество, но дольше время
- **Рекомендуемые значения**:
  - `5` - для быстрых экспериментов
  - `10` - для стандартных задач
  - `20` - для важных задач
  - `50+` - для максимального качества
- **Практический пример**: Если у вас есть 2 часа, установите `num_trials: 10`

**Параметр `scheduler`:**

- **Что означает**: Планировщик для распределения задач
- **Зачем нужен**: Управляет параллельным выполнением
- **Доступные значения**:
  - `'local'` - локальное выполнение (по умолчанию)
  - `'ray'` - распределенное выполнение через Ray
  - `'dask'` - распределенное выполнение через Dask
- **Практический пример**: Для одного компьютера используйте `'local'`

#### ⏰ Детальное описание параметров для временных рядов

**Параметр `prediction_length`:**

- **Что означает**: Количество будущих точек для прогнозирования
- **Зачем нужен**: Определяет горизонт прогнозирования
- **Рекомендуемые значения**:
  - `24` - для почасовых данных (прогноз на сутки)
  - `7` - для дневных данных (прогноз на неделю)
  - `30` - для дневных данных (прогноз на месяц)
- **Практический пример**: Для прогноза продаж на неделю установите `prediction_length: 7`

**Параметр `freq`:**

- **Что означает**: Частота временного ряда
- **Зачем нужен**: Определяет интервал между точками
- **Доступные значения**:
  - `'H'` - почасовые данные
  - `'D'` - дневные данные
  - `'W'` - недельные данные
  - `'M'` - месячные данные
- **Практический пример**: Для дневных продаж установите `freq: 'D'`

**Параметр `target_column`:**

- **Что означает**: Название столбца с целевой переменной
- **Зачем нужен**: Указывает, что предсказывать
- **Практический пример**: Если у вас есть столбец 'sales', установите `target_column: 'sales'`
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

## 🚀 Архитектура продакшена

<img src="images/optimized/production_architecture.png" alt="Архитектура продакшена" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 8: Архитектура развертывания AutoML Gluon в продакшене*

**Почему важно понимать архитектуру продакшена?** Потому что это помогает правильно спланировать развертывание:

- **Модель**: Обученная модель AutoML Gluon
- **API Gateway**: Точка входа для запросов
- **Load Balancer**: Распределение нагрузки между инстансами
- **Monitoring**: Мониторинг производительности и качества
- **Scaling**: Автоматическое масштабирование под нагрузку
- **Data Pipeline**: Поток данных для переобучения

### 📊 Сравнение продакшен решений

<img src="images/optimized/production_comparison.png" alt="Сравнение продакшен решений" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 9: Сравнение различных подходов к развертыванию*

**Почему важно сравнивать решения?** Потому что разные задачи требуют разных подходов:

- **Batch Processing**: Обработка данных пакетами (для больших объемов)
- **Real-time API**: Мгновенные предсказания (для интерактивных приложений)
- **Edge Deployment**: Развертывание на периферийных устройствах
- **Cloud Deployment**: Развертывание в облаке (масштабируемость)
- **Hybrid Approach**: Комбинированный подход (гибкость)

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
