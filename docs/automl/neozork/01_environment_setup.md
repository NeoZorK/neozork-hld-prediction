# 01. Установка окружения на macOS M1 Pro

**Цель:** Создать оптимальное окружение для разработки робастных ML-систем на macOS M1 Pro.

## Почему macOS M1 Pro идеален для ML?

**M1 Pro чип революционизировал ML на Mac:**

### Unified Memory Architecture (UMA)
**Теория:** UMA позволяет CPU и GPU использовать общую память без копирования данных между устройствами. Это критично для ML-работ, где большие датасеты и модели требуют быстрого доступа к памяти.

**Практические преимущества:**
- **Скорость:** Данные не копируются между CPU и GPU, что ускоряет обработку в 3-5 раз
- **Эффективность памяти:** Один набор данных используется и CPU, и GPU одновременно
- **Масштабируемость:** До 32GB общей памяти для больших моделей
- **Простота программирования:** Не нужно управлять передачей данных между устройствами

**Минусы:**
- Ограниченная память по сравнению с дискретными GPU (до 32GB vs 80GB+ на RTX A100)
- Меньшая производительность для очень больших моделей

### Neural Engine
**Теория:** Специализированный 16-ядерный процессор для машинного обучения, оптимизированный для операций с матрицами и нейронными сетями.

**Преимущества:**
- **Специализация:** Оптимизирован именно для ML-операций
- **Энергоэффективность:** Потребляет в 10 раз меньше энергии чем GPU
- **Скорость:** До 11 TOPS (триллионов операций в секунду)
- **Автоматическая оптимизация:** Apple автоматически использует Neural Engine для подходящих операций

**Ограничения:**
- Работает только с определенными типами операций
- Меньшая гибкость по сравнению с CUDA
- Ограниченная поддержка пользовательских операций

### MLX Framework
**Теория:** Apple-специфичный фреймворк, разработанный для максимального использования возможностей M1/M2/M3 чипов.

**Ключевые особенности:**
- **Нативная интеграция:** Прямой доступ к Neural Engine и GPU
- **PyTorch-совместимость:** Легкая миграция существующего кода
- **Автоматическая оптимизация:** Автоматический выбор лучшего устройства для каждой операции
- **Unified API:** Единый интерфейс для CPU, GPU и Neural Engine

**Плюсы:**
- Максимальная производительность на Apple Silicon
- Простота использования
- Энергоэффективность
- Автоматическая оптимизация

**Минусы:**
- Привязка к экосистеме Apple
- Меньшее сообщество по сравнению с PyTorch/TensorFlow
- Ограниченная поддержка некоторых операций

## Системные требования

### Минимальные требования
**Теория:** Минимальные требования определяют базовую функциональность системы. Для робастных ML-систем критично иметь достаточные ресурсы для обработки данных и обучения моделей.

- **macOS:** 12.0+ (Monterey)
  - **Почему:** Поддержка MLX Framework и оптимизаций для M1
  - **Плюсы:** Стабильность, совместимость с ML-библиотеками
  - **Минусы:** Ограниченные возможности по сравнению с новыми версиями

- **RAM:** 16GB (рекомендуется 32GB)
  - **Теория:** ML-модели требуют значительной памяти для хранения данных и промежуточных вычислений
  - **16GB:** Минимум для небольших моделей и датасетов
  - **32GB:** Оптимально для большинства ML-задач, позволяет работать с большими датасетами
  - **Плюсы:** Быстрая обработка, возможность работы с большими моделями
  - **Минусы:** Высокая стоимость, ограниченная доступность

- **Storage:** 100GB свободного места
  - **Теория:** ML-проекты требуют много места для данных, моделей и кэша
  - **Плюсы:** Достаточно для небольших проектов
  - **Минусы:** Может быть недостаточно для больших датасетов

- **Internet:** Стабильное соединение
  - **Почему:** Загрузка больших датасетов, обновление библиотек, доступ к облачным сервисам
  - **Плюсы:** Возможность работы с внешними данными
  - **Минусы:** Зависимость от интернет-соединения

### Рекомендуемые требования
**Теория:** Рекомендуемые требования обеспечивают оптимальную производительность и комфортную работу с большими ML-проектами.

- **macOS:** 14.0+ (Sonoma)
  - **Почему:** Новейшие оптимизации для M1, улучшенная поддержка ML-фреймворков
  - **Плюсы:** Максимальная производительность, новые возможности
  - **Минусы:** Может быть менее стабильной на ранних этапах

- **RAM:** 32GB+
  - **Теория:** Большие ML-модели и датасеты требуют значительной памяти
  - **Плюсы:** Работа с большими моделями, параллельная обработка
  - **Минусы:** Высокая стоимость, избыточность для простых задач

- **Storage:** 500GB+ SSD
  - **Теория:** SSD обеспечивает быстрый доступ к данным, критично для ML-работ
  - **Плюсы:** Быстрая загрузка данных, быстрый доступ к моделям
  - **Минусы:** Высокая стоимость по сравнению с HDD

- **GPU:** M1 Pro/Max/Ultra
  - **Теория:** Более мощные чипы обеспечивают лучшую производительность для ML
  - **M1 Pro:** Хороший баланс производительности и стоимости
  - **M1 Max:** Максимальная производительность для профессиональных задач
  - **M1 Ultra:** Экстремальная производительность для исследовательских задач
  - **Плюсы:** Высокая производительность, энергоэффективность
  - **Минусы:** Высокая стоимость, ограниченная доступность

## Установка базового окружения

### 1. Установка Homebrew

**Теория:** Homebrew - это пакетный менеджер для macOS, который упрощает установку и управление программным обеспечением. Для ML-проектов критично иметь централизованное управление зависимостями.

**Почему Homebrew для ML:**
- **Централизованное управление:** Все зависимости в одном месте
- **Автоматическое разрешение конфликтов:** Умное управление версиями
- **Оптимизация для M1:** Нативная поддержка Apple Silicon
- **Богатая экосистема:** Тысячи пакетов для ML и научных вычислений

**Плюсы:**
- Простота установки и обновления
- Автоматическое разрешение зависимостей
- Оптимизация для M1
- Большое сообщество и поддержка

**Минусы:**
- Может конфликтовать с системными пакетами
- Требует регулярного обновления
- Некоторые пакеты могут быть устаревшими

```bash
# Установка Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Добавление в PATH для M1
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

**Важные моменты для M1:**
- **Путь установки:** `/opt/homebrew/` вместо `/usr/local/`
- **Архитектура:** Автоматическая установка ARM64 версий
- **Совместимость:** Поддержка как ARM64, так и x86_64 пакетов через Rosetta

### 2. Установка uv (Ultra-fast Python package manager)

**Теория:** uv - это современный менеджер пакетов Python, написанный на Rust, который обеспечивает максимальную скорость и надежность установки зависимостей. Для робастных ML-систем критично иметь быстрый и надежный менеджер пакетов.

**Почему uv вместо pip?**
- **Скорость:** В 10-100 раз быстрее pip благодаря Rust и параллельной обработке
- **Надежность:** Детерминированные сборки обеспечивают воспроизводимость
- **Совместимость:** Полная совместимость с pip и существующими проектами
- **Кэширование:** Умное кэширование зависимостей ускоряет повторные установки
- **Безопасность:** Автоматическая проверка целостности пакетов
- **Управление версиями:** Продвинутое разрешение конфликтов версий

**Плюсы uv:**
- Экстремальная скорость установки
- Надежность и воспроизводимость
- Современный подход к управлению зависимостями
- Отличная интеграция с существующими проектами
- Автоматическое управление виртуальными окружениями

**Минусы uv:**
- Относительно новый инструмент (меньше сообщества)
- Некоторые пакеты могут требовать дополнительной настройки
- Зависимость от Rust (больший размер установки)

```bash
# Установка uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Добавление в PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Проверка установки
uv --version
```

**Критически важно для ML-проектов:**
- **Воспроизводимость:** Детерминированные сборки обеспечивают одинаковые результаты на разных машинах
- **Скорость:** Быстрая установка критична для CI/CD и разработки
- **Надежность:** Минимизация ошибок установки зависимостей
- **Управление версиями:** Точное управление версиями ML-библиотек

### 3. Установка Python через uv

**Теория:** Выбор версии Python критичен для ML-проектов. Python 3.11 обеспечивает оптимальный баланс между производительностью, стабильностью и поддержкой ML-библиотек на M1.

**Почему Python 3.11 для M1:**
- **Производительность:** До 25% быстрее Python 3.10 благодаря оптимизациям
- **Совместимость:** Полная поддержка всех ML-библиотек
- **Стабильность:** Зрелая версия с исправленными багами
- **Оптимизация для M1:** Лучшая поддержка ARM64 архитектуры
- **Память:** Более эффективное использование памяти

**Плюсы Python 3.11:**
- Высокая производительность
- Отличная совместимость с ML-библиотеками
- Стабильность и надежность
- Оптимизация для M1
- Поддержка современных возможностей Python

**Минусы Python 3.11:**
- Некоторые старые библиотеки могут не поддерживаться
- Требует обновления существующего кода
- Больший размер по сравнению с более старыми версиями

```bash
# Установка Python 3.11 (оптимальная версия для M1)
uv python install 3.11

# Проверка установки
uv python list
```

**Альтернативные версии:**
- **Python 3.10:** Более стабильная, но медленнее
- **Python 3.12:** Новейшая, но может быть менее стабильной
- **Python 3.9:** Устаревшая, не рекомендуется для новых проектов

**Критически важно для ML:**
- **Воспроизводимость:** Одинаковая версия Python на всех машинах
- **Производительность:** Быстрое выполнение ML-алгоритмов
- **Совместимость:** Поддержка всех необходимых ML-библиотек
- **Стабильность:** Минимизация ошибок во время обучения моделей

## Установка MLX Framework

### Что такое MLX?

**Теория:** MLX (Machine Learning eXtended) - это специализированный фреймворк Apple для машинного обучения, разработанный для максимального использования возможностей Apple Silicon чипов. Это критично для робастных ML-систем, так как обеспечивает оптимальную производительность на M1/M2/M3.

**MLX - это Apple-специфичный фреймворк для ML:**

**Нативная поддержка M1/M2/M3:**
- **Теория:** MLX использует все возможности Apple Silicon чипов, включая CPU, GPU и Neural Engine
- **Практические преимущества:** До 10x ускорение по сравнению с PyTorch на M1
- **Автоматическая оптимизация:** Автоматический выбор лучшего устройства для каждой операции
- **Энергоэффективность:** Потребляет в 5-10 раз меньше энергии чем CUDA

**Unified Memory:**
- **Теория:** MLX использует единую память для CPU и GPU, что устраняет необходимость копирования данных
- **Практические преимущества:** Работа с большими моделями без ограничений памяти GPU
- **Скорость:** Данные доступны мгновенно для всех устройств
- **Простота:** Не нужно управлять передачей данных между устройствами

**Neural Engine:**
- **Теория:** Автоматическое использование Neural Engine для подходящих операций
- **Практические преимущества:** До 20x ускорение для определенных ML-операций
- **Энергоэффективность:** Neural Engine потребляет минимум энергии
- **Специализация:** Оптимизирован для операций с матрицами и нейронными сетями

**PyTorch совместимость:**
- **Теория:** MLX предоставляет API, похожий на PyTorch, что упрощает миграцию
- **Практические преимущества:** Легкая миграция существующего кода
- **Обратная совместимость:** Поддержка большинства PyTorch операций
- **Обучение:** Минимальное время на изучение нового API

**Плюсы MLX:**
- Максимальная производительность на Apple Silicon
- Энергоэффективность
- Простота использования
- Автоматическая оптимизация
- Отличная интеграция с Apple экосистемой

**Минусы MLX:**
- Привязка к Apple Silicon (нет поддержки других платформ)
- Меньшее сообщество по сравнению с PyTorch/TensorFlow
- Ограниченная поддержка некоторых операций
- Меньше готовых моделей и примеров

### Установка MLX

```bash
# Создание проекта
mkdir neozork-ml-system
cd neozork-ml-system

# Инициализация uv проекта
uv init --python 3.11

# Установка MLX
uv add mlx

# Установка дополнительных зависимостей
uv add mlx-lm  # Для языковых моделей
uv add mlx-examples  # Примеры использования
```

### Проверка MLX

```python
# test_mlx.py
import mlx.core as mx
import mlx.nn as nn

# Создание простой нейронной сети
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(10, 50)
        self.linear2 = nn.Linear(50, 1)
    
    def __call__(self, x):
        x = mx.tanh(self.linear1(x))
        return self.linear2(x)

# Тест на M1
x = mx.random.normal((100, 10))
model = SimpleNet()
output = model(x)
print(f"MLX работает! Output shape: {output.shape}")
```

## Установка основных ML библиотек

### 1. Основные зависимости

```bash
# Установка основных библиотек
uv add numpy pandas scikit-learn matplotlib seaborn
uv add jupyter notebook ipykernel
uv add plotly dash  # Для интерактивных графиков
```

### 2. Финансовые библиотеки

```bash
# Финансовые данные и анализ
uv add yfinance pandas-datareader
uv add ta-lib  # Технические индикаторы
uv add vectorbt  # Векторизованный бэктестинг
uv add backtrader  # Альтернативный бэктестер
```

### 3. Продвинутые ML библиотеки

```bash
# Продвинутые ML библиотеки
uv add xgboost lightgbm catboost
uv add optuna  # Гиперпараметрическая оптимизация
uv add mlflow  # MLOps
uv add wandb  # Эксперименты
```

### 4. Deep Learning

```bash
# Deep Learning (совместимость с M1)
uv add torch torchvision torchaudio
uv add tensorflow-macos tensorflow-metal  # Для M1
uv add transformers  # Hugging Face
```

## Настройка Jupyter Notebook

### Создание ядра для проекта

```bash
# Создание ядра Jupyter
uv run python -m ipykernel install --user --name neozork-ml --display-name "NeoZorK ML"

# Запуск Jupyter
uv run jupyter notebook
```

### Конфигурация Jupyter

```python
# jupyter_config.py
c = get_config()

# Настройки для M1
c.NotebookApp.allow_root = True
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False

# Оптимизация для M1
c.NotebookApp.iopub_data_rate_limit = 1000000000
c.NotebookApp.rate_limit_window = 3.0
```

## Оптимизация для M1 Pro

### 1. Настройка переменных окружения

```bash
# ~/.zshrc
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=8  # Оптимально для M1 Pro
export MKL_NUM_THREADS=8
export NUMEXPR_NUM_THREADS=8

# MLX оптимизации
export MLX_USE_METAL=1
export MLX_USE_NEURAL_ENGINE=1
```

### 2. Настройка NumPy для M1

```python
# numpy_config.py
import numpy as np

# Проверка оптимизации
print(f"NumPy version: {np.__version__}")
print(f"BLAS info: {np.show_config()}")

# Тест производительности
import time

# Тест матричных операций
size = 5000
a = np.random.rand(size, size)
b = np.random.rand(size, size)

start = time.time()
c = np.dot(a, b)
end = time.time()

print(f"Matrix multiplication time: {end - start:.2f} seconds")
```

### 3. Настройка PyTorch для M1

```python
# pytorch_m1_config.py
import torch

# Проверка MPS (Metal Performance Shaders)
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("MPS доступен!")
else:
    device = torch.device("cpu")
    print("MPS недоступен, используем CPU")

# Тест производительности
x = torch.randn(1000, 1000, device=device)
y = torch.randn(1000, 1000, device=device)

start = time.time()
z = torch.mm(x, y)
end = time.time()

print(f"PyTorch MPS time: {end - start:.2f} seconds")
```

## Создание проекта

### Структура проекта

```
neozork-ml-system/
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loaders.py
│   │   └── preprocessors.py
│   ├── features/
│   │   ├── __init__.py
│   │   ├── engineering.py
│   │   └── indicators.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── ml.py
│   │   └── deep.py
│   ├── backtesting/
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   └── metrics.py
│   └── deployment/
│       ├── __init__.py
│       ├── api.py
│       └── blockchain.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── features/
├── models/
│   ├── trained/
│   └── artifacts/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_backtesting.ipynb
├── tests/
│   ├── __init__.py
│   ├── test_data.py
│   ├── test_features.py
│   ├── test_models.py
│   └── test_backtesting.py
├── config/
│   ├── config.yaml
│   └── logging.yaml
├── scripts/
│   ├── train.py
│   ├── backtest.py
│   └── deploy.py
├── pyproject.toml
├── README.md
└── .gitignore
```

### Инициализация проекта

```bash
# Создание структуры
mkdir -p neozork-ml-system/{src/{data,features,models,backtesting,deployment},data/{raw,processed,features},models/{trained,artifacts},notebooks,tests,config,scripts}

# Переход в проект
cd neozork-ml-system

# Инициализация uv
uv init --python 3.11

# Установка зависимостей
uv add numpy pandas scikit-learn matplotlib seaborn
uv add jupyter notebook ipykernel
uv add yfinance ta-lib vectorbt
uv add xgboost lightgbm catboost
uv add torch torchvision
uv add mlx
uv add optuna mlflow wandb
```

## Проверка установки

### Тест производительности

```python
# performance_test.py
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import torch

def test_numpy_performance():
    """Тест производительности NumPy на M1"""
    print("Testing NumPy performance...")
    
    # Большая матрица
    size = 10000
    a = np.random.rand(size, size)
    b = np.random.rand(size, size)
    
    start = time.time()
    c = np.dot(a, b)
    end = time.time()
    
    print(f"NumPy matrix multiplication: {end - start:.2f} seconds")
    return end - start

def test_pandas_performance():
    """Тест производительности Pandas на M1"""
    print("Testing Pandas performance...")
    
    # Большой DataFrame
    n_rows = 1000000
    df = pd.DataFrame({
        'A': np.random.randn(n_rows),
        'B': np.random.randn(n_rows),
        'C': np.random.randn(n_rows)
    })
    
    start = time.time()
    result = df.groupby('A').agg({'B': 'mean', 'C': 'std'})
    end = time.time()
    
    print(f"Pandas groupby operation: {end - start:.2f} seconds")
    return end - start

def test_sklearn_performance():
    """Тест производительности scikit-learn на M1"""
    print("Testing scikit-learn performance...")
    
    # Большой датасет
    n_samples = 100000
    n_features = 100
    
    X = np.random.randn(n_samples, n_features)
    y = np.random.randn(n_samples)
    
    model = RandomForestRegressor(n_estimators=100, n_jobs=-1)
    
    start = time.time()
    model.fit(X, y)
    end = time.time()
    
    print(f"RandomForest training: {end - start:.2f} seconds")
    return end - start

def test_pytorch_performance():
    """Тест производительности PyTorch на M1"""
    print("Testing PyTorch performance...")
    
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print("Using MPS (Metal Performance Shaders)")
    else:
        device = torch.device("cpu")
        print("Using CPU")
    
    # Большие тензоры
    size = 5000
    a = torch.randn(size, size, device=device)
    b = torch.randn(size, size, device=device)
    
    start = time.time()
    c = torch.mm(a, b)
    end = time.time()
    
    print(f"PyTorch matrix multiplication: {end - start:.2f} seconds")
    return end - start

if __name__ == "__main__":
    print("=== NeoZorK ML Performance Test ===")
    print("Testing on macOS M1 Pro...")
    print()
    
    numpy_time = test_numpy_performance()
    pandas_time = test_pandas_performance()
    sklearn_time = test_sklearn_performance()
    pytorch_time = test_pytorch_performance()
    
    print()
    print("=== Performance Summary ===")
    print(f"NumPy: {numpy_time:.2f}s")
    print(f"Pandas: {pandas_time:.2f}s")
    print(f"Scikit-learn: {sklearn_time:.2f}s")
    print(f"PyTorch: {pytorch_time:.2f}s")
    
    total_time = numpy_time + pandas_time + sklearn_time + pytorch_time
    print(f"Total time: {total_time:.2f}s")
```

## Устранение проблем

### Проблема 1: Ошибки компиляции

```bash
# Установка Xcode Command Line Tools
xcode-select --install

# Установка дополнительных инструментов
brew install cmake pkg-config
```

### Проблема 2: Проблемы с ta-lib

```bash
# Установка ta-lib через Homebrew
brew install ta-lib

# Установка Python binding
uv add TA-Lib
```

### Проблема 3: Проблемы с PyTorch

```bash
# Установка правильной версии PyTorch для M1
uv add torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## Следующие шаги

После успешной установки окружения переходите к разделу:
- **[02_robust_systems_fundamentals.md](02_robust_systems_fundamentals.md)** - Основы робастных систем

## Полезные команды

```bash
# Проверка версий
uv run python --version
uv run python -c "import numpy; print(numpy.__version__)"
uv run python -c "import torch; print(torch.__version__)"

# Запуск Jupyter
uv run jupyter notebook

# Запуск тестов
uv run python -m pytest tests/

# Установка новых зависимостей
uv add package_name

# Обновление зависимостей
uv sync --upgrade
```

---

**Важно:** Убедитесь, что все тесты производительности проходят успешно перед переходом к следующему разделу.
