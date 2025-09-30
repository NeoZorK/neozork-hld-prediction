# Troubleshooting AutoML Gluon

## Введение в troubleshooting

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
