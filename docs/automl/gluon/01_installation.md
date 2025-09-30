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
