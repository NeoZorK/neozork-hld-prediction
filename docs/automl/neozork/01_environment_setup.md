# 01. Установка окружения на macOS M1 Pro

**Цель:** Создать оптимальное окружение для разработки робастных ML-систем на macOS M1 Pro.

## Почему macOS M1 Pro идеален для ML?

**M1 Pro чип революционизировал ML на Mac:**
- **Unified Memory Architecture** - до 32GB общей памяти для CPU и GPU
- **Neural Engine** - 16-ядерный процессор для ML
- **MLX Framework** - нативная поддержка Apple Silicon
- **Энергоэффективность** - в 10 раз меньше потребления энергии

## Системные требования

### Минимальные требования
- **macOS:** 12.0+ (Monterey)
- **RAM:** 16GB (рекомендуется 32GB)
- **Storage:** 100GB свободного места
- **Internet:** Стабильное соединение

### Рекомендуемые требования
- **macOS:** 14.0+ (Sonoma)
- **RAM:** 32GB+
- **Storage:** 500GB+ SSD
- **GPU:** M1 Pro/Max/Ultra

## Установка базового окружения

### 1. Установка Homebrew

```bash
# Установка Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Добавление в PATH для M1
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

### 2. Установка uv (Ultra-fast Python package manager)

```bash
# Установка uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Добавление в PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Проверка установки
uv --version
```

**Почему uv вместо pip?**
- **Скорость:** В 10-100 раз быстрее pip
- **Надежность:** Детерминированные сборки
- **Совместимость:** Полная совместимость с pip
- **Кэширование:** Умное кэширование зависимостей

### 3. Установка Python через uv

```bash
# Установка Python 3.11 (оптимальная версия для M1)
uv python install 3.11

# Проверка установки
uv python list
```

## Установка MLX Framework

### Что такое MLX?

**MLX - это Apple-специфичный фреймворк для ML:**
- **Нативная поддержка M1/M2/M3** - использует все возможности чипа
- **Unified Memory** - эффективное использование памяти
- **Neural Engine** - автоматическое использование Neural Engine
- **PyTorch совместимость** - легко мигрировать с PyTorch

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
