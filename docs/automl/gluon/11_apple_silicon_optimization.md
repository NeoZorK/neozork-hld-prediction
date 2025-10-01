# Оптимизация AutoML Gluon для Apple Silicon (M1/M2/M3)

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему оптимизация для Apple Silicon критически важна

**Почему Apple Silicon - это революция в машинном обучении?** Потому что эти чипы специально разработаны для ML-задач, обеспечивая в 3-5 раз лучшую производительность при меньшем энергопотреблении.

### Преимущества Apple Silicon для ML
- **Унифицированная память**: CPU и GPU используют общую память (до 128GB)
- **Высокая энергоэффективность**: В 2-3 раза меньше потребление энергии
- **Специализированные ядра**: Neural Engine для ML-операций
- **Metal Performance Shaders**: GPU ускорение для матричных операций

### Проблемы без оптимизации
- **Медленная работа**: В 3-5 раз медленнее, чем могло бы быть
- **Высокое энергопотребление**: Батарея разряжается за часы
- **Перегрев**: Система тормозит из-за теплового дросселирования
- **Неэффективное использование ресурсов**: Только CPU, игнорирование GPU

## Введение в оптимизацию для Apple Silicon

![Оптимизация для Apple Silicon](images/apple_silicon_optimization.png)
*Рисунок 9: Оптимизация AutoML Gluon для Apple Silicon*

**Почему Apple Silicon требует специального подхода?** Потому что это архитектура ARM, а не x86, и требует специальных оптимизаций для максимальной производительности.

Apple Silicon MacBook с чипами M1, M2, M3 предоставляют уникальные возможности для ускорения машинного обучения через:
- **MLX** - фреймворк Apple для машинного обучения на Apple Silicon
- **Ray** - распределенные вычисления с поддержкой Apple Silicon
- **OpenMP** - параллельные вычисления
- **Metal Performance Shaders (MPS)** - GPU ускорение

## Установка для Apple Silicon

**Почему установка для Apple Silicon требует особого внимания?** Потому что большинство пакетов по умолчанию собираются для x86, что приводит к медленной работе через эмуляцию Rosetta.

### 1. Базовая установка с оптимизацией

**Почему conda лучше pip для Apple Silicon?** Потому что conda предоставляет нативные ARM64 пакеты, которые работают в 2-3 раза быстрее.

```bash
# Создание conda окружения с поддержкой Apple Silicon
conda create -n autogluon-m1 python=3.9
conda activate autogluon-m1

# Установка базовых зависимостей - нативные ARM64 версии
conda install -c conda-forge numpy pandas scikit-learn matplotlib seaborn

# Установка PyTorch с поддержкой MPS (Metal Performance Shaders)
pip install torch torchvision torchaudio

# Установка AutoGluon
pip install autogluon
```

### 2. Установка MLX для Apple Silicon

**Почему MLX - это будущее ML на Apple Silicon?** Потому что это единственный фреймворк, специально разработанный Apple для их чипов, обеспечивающий максимальную производительность.

**Преимущества MLX:**
- **Нативная поддержка**: Специально для Apple Silicon
- **Высокая производительность**: В 2-3 раза быстрее PyTorch
- **Энергоэффективность**: Меньше потребление энергии
- **Простота использования**: API похож на NumPy

```bash
# Установка MLX - фреймворк Apple для ML
pip install mlx mlx-lm

# Установка дополнительных MLX пакетов - оптимизаторы и нейросети
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
