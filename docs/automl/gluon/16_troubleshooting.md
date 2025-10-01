# Troubleshooting AutoML Gluon

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему troubleshooting критически важен

**Почему 80% времени ML-разработки тратится на решение проблем?** Потому что машинное обучение - это сложная система, где множество компонентов должны работать вместе. Это как диагностика автомобиля - нужно знать, где искать проблему.

### Катастрофические последствия нерешенных проблем
- **Потеря времени**: Дни на решение простых проблем
- **Фрустрация команды**: Разработчики бросают проект
- **Плохие результаты**: Модели работают неэффективно
- **Потеря доверия**: Заказчики теряют веру в ML

### Преимущества системного troubleshooting
- **Быстрое решение**: Знание типичных проблем и их решений
- **Профилактика**: Предотвращение проблем до их возникновения
- **Эффективность**: Больше времени на разработку, меньше на отладку
- **Уверенность**: Команда знает, как решать проблемы

## Введение в troubleshooting

<img src="images/optimized/troubleshooting_flowchart.png" alt="Troubleshooting блок-схема" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 16.1: Блок-схема решения проблем AutoML Gluon - систематический подход к диагностике и решению*

**Почему troubleshooting - это искусство, а не наука?** Потому что каждая проблема уникальна, но паттерны повторяются. Это как медицинская диагностика - симптомы похожи, но причины разные.

**Ключевые принципы troubleshooting:**
- **Систематический подход**: Пошаговая диагностика проблем
- **Документирование**: Фиксация всех проблем и решений
- **Тестирование**: Проверка эффективности решений
- **Профилактика**: Предотвращение повторных проблем
- **Обучение команды**: Передача знаний и опыта

**Типы проблем в AutoML Gluon:**
- **Проблемы установки**: Конфликты зависимостей, версии Python
- **Проблемы данных**: Форматы, размеры, качество
- **Проблемы производительности**: Медленная работа, нехватка памяти
- **Проблемы моделей**: Плохая точность, переобучение

В этом разделе рассмотрим типичные проблемы, возникающие при работе с AutoML Gluon, и способы их решения. Каждая проблема включает описание, причины возникновения и пошаговые инструкции по устранению.

## Проблемы установки

<img src="images/optimized/installation_issues.png" alt="Проблемы установки" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 16.2: Диагностика и решение проблем установки AutoML Gluon - типы проблем и их решения*

**Почему проблемы установки - самые частые в ML?** Потому что ML-библиотеки имеют сложные зависимости между собой. Это как пазл, где каждая деталь должна точно подходить.

**Типы проблем установки:**
- **Dependency Conflicts**: Конфликты версий пакетов
- **Python Version Issues**: Неправильная версия Python
- **CUDA Problems**: Проблемы с GPU поддержкой
- **Memory Issues**: Нехватка памяти при установке
- **Permission Problems**: Недостаточные права доступа
- **Virtual Environment Issues**: Проблемы с виртуальными окружениями

**Ключевые аспекты проблем установки:**
- **Конфликты зависимостей**: Несовместимые версии пакетов
- **Проблемы с Python**: Неправильная версия Python
- **Проблемы с pip/conda**: Конфликты менеджеров пакетов
- **Проблемы с системными библиотеками**: Отсутствующие системные зависимости
- **Проблемы с виртуальными окружениями**: Неправильная настройка окружений
- **Проблемы с правами доступа**: Недостаточные права для установки

### 1. Ошибки зависимостей

**Почему конфликты версий так распространены?** Потому что разные библиотеки требуют разные версии одних и тех же пакетов. Это как попытка использовать детали от разных моделей автомобилей.

#### Проблема: Конфликт версий пакетов
```bash
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
This behaviour is the source of the following dependency conflicts.
```

**Почему возникает эта ошибка?** Потому что pip пытается установить пакеты, которые конфликтуют друг с другом. Это как попытка установить одновременно Windows и Linux.

**Решение:**
```bash
# Создание нового окружения - изоляция от других проектов
conda create -n autogluon python=3.9
conda activate autogluon

# Установка в правильном порядке - сначала базовые, потом специфичные
pip install --upgrade pip
pip install autogluon

# Или установка конкретных версий - фиксация совместимых версий
pip install autogluon==0.8.2
pip install torch==1.13.1
pip install torchvision==0.14.1
```

**Детальные описания параметров решения конфликтов зависимостей:**

- **`conda create -n autogluon python=3.9`**: Создание изолированного окружения
  - `-n autogluon`: Имя окружения (может быть любым)
  - `python=3.9`: Версия Python (3.8-3.11 поддерживаются)
  - Преимущества: полная изоляция от системных пакетов

- **`conda activate autogluon`**: Активация окружения
  - Активирует созданное окружение
  - Изолирует установленные пакеты
  - Предотвращает конфликты с другими проектами

- **`pip install --upgrade pip`**: Обновление pip
  - Устанавливает последнюю версию pip
  - Улучшает разрешение зависимостей
  - Рекомендуется перед установкой пакетов

- **`pip install autogluon`**: Установка AutoGluon
  - Устанавливает последнюю стабильную версию
  - Автоматически разрешает зависимости
  - Может занять 5-15 минут

- **`pip install autogluon==0.8.2`**: Установка конкретной версии
  - `0.8.2`: Стабильная версия (рекомендуется)
  - `0.8.1`: Предыдущая версия
  - `0.9.0`: Бета-версия (не рекомендуется для продакшена)

- **`pip install torch==1.13.1`**: Установка PyTorch
  - `1.13.1`: Совместимая версия с AutoGluon
  - `1.12.1`: Предыдущая стабильная версия
  - `1.14.0`: Новая версия (может быть несовместима)

- **`pip install torchvision==0.14.1`**: Установка TorchVision
  - `0.14.1`: Совместимая версия с PyTorch 1.13.1
  - `0.13.1`: Предыдущая версия
  - `0.15.0`: Новая версия (может быть несовместима)

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

**Детальные описания параметров решения проблем CUDA:**

- **`torch.cuda.is_available()`**: Проверка доступности CUDA
  - `True`: CUDA доступна и работает
  - `False`: CUDA недоступна или не установлена
  - Причины False: неправильная установка, несовместимая версия

- **`torch.version.cuda`**: Версия CUDA
  - `11.7`: CUDA 11.7 (рекомендуется)
  - `11.6`: CUDA 11.6 (поддерживается)
  - `12.0`: CUDA 12.0 (может быть несовместима)

- **`pip install torch==1.13.1+cu117`**: Установка PyTorch с CUDA
  - `1.13.1`: Версия PyTorch
  - `+cu117`: Версия CUDA (11.7)
  - `--extra-index-url`: Дополнительный индекс пакетов

- **`torchvision==0.14.1+cu117`**: Установка TorchVision с CUDA
  - `0.14.1`: Версия TorchVision
  - `+cu117`: Версия CUDA (11.7)
  - Должна соответствовать версии PyTorch

- **`os.environ['CUDA_VISIBLE_DEVICES'] = ''`**: Отключение CUDA
  - `''`: Пустая строка отключает все GPU
  - `'0'`: Использовать только GPU 0
  - `'0,1'`: Использовать GPU 0 и 1
  - Применение: при проблемах с памятью GPU

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

**Детальные описания параметров решения проблем с памятью:**

- **`ag.set_config({'memory_limit': 4})`**: Ограничение памяти AutoGluon
  - `4`: Лимит памяти в GB (рекомендуется 4-8 GB)
  - `2`: Минимальный лимит для небольших данных
  - `8`: Максимальный лимит для больших данных
  - `16+`: Для очень больших данных

- **`os.environ['AUTOGLUON_MEMORY_LIMIT'] = '4'`**: Установка через переменные окружения
  - `'4'`: Лимит памяти в GB (строка)
  - `'2'`: Минимальный лимит
  - `'8'`: Максимальный лимит
  - Преимущества: глобальная настройка для всех процессов

- **`train_data.sample(frac=0.5)`**: Уменьшение размера данных
  - `0.5`: Использовать 50% данных (рекомендуется)
  - `0.3`: Использовать 30% данных (для очень больших датасетов)
  - `0.7`: Использовать 70% данных (компромисс между качеством и памятью)
  - `0.1`: Использовать 10% данных (только для тестирования)

**Дополнительные параметры оптимизации памяти:**

- **`ag.set_config({'num_cpus': 2})`**: Ограничение CPU
  - `2`: Использовать 2 CPU ядра
  - `4`: Использовать 4 CPU ядра (рекомендуется)
  - `8`: Использовать 8 CPU ядер (для мощных систем)

- **`ag.set_config({'time_limit': 300})`**: Ограничение времени обучения
  - `300`: 5 минут (для быстрого тестирования)
  - `600`: 10 минут (стандартное время)
  - `1800`: 30 минут (для качественных моделей)

## Проблемы обучения

<img src="images/optimized/training_issues.png" alt="Проблемы обучения" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 16.3: Диагностика и решение проблем обучения AutoML Gluon - типы проблем и методы решения*

**Почему проблемы обучения так критичны?** Потому что они влияют на качество и скорость получения результатов:

**Типы проблем обучения:**
- **Slow Training**: Медленное обучение модели
- **Poor Model Quality**: Низкое качество модели
- **Validation Errors**: Ошибки валидации
- **Data Quality Issues**: Проблемы с качеством данных
- **Resource Shortage**: Нехватка вычислительных ресурсов
- **Configuration Problems**: Проблемы с конфигурацией

**Ключевые аспекты проблем обучения:**
- **Медленное обучение**: Неоптимальные настройки, нехватка ресурсов
- **Плохое качество модели**: Неправильные данные, переобучение
- **Ошибки валидации**: Неправильное разделение данных
- **Проблемы с данными**: Некачественные или неподходящие данные
- **Проблемы с ресурсами**: Нехватка памяти, CPU, GPU
- **Проблемы с конфигурацией**: Неправильные параметры обучения

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

**Детальные описания параметров оптимизации обучения:**

- **`presets='optimize_for_deployment'`**: Предустановка для быстрого обучения
  - `'optimize_for_deployment'`: Быстрое обучение (рекомендуется)
  - `'best_quality'`: Максимальное качество (медленно)
  - `'medium_quality_faster_train'`: Компромисс качества и скорости
  - `'fast'`: Очень быстрое обучение (низкое качество)

- **`time_limit=600`**: Ограничение времени обучения
  - `600`: 10 минут (стандартное время)
  - `300`: 5 минут (быстрое тестирование)
  - `1800`: 30 минут (качественные модели)
  - `3600`: 1 час (максимальное качество)

- **`num_bag_folds=3`**: Количество фолдов для bagging
  - `3`: Быстрое обучение (рекомендуется для оптимизации)
  - `5`: Стандартное значение
  - `10`: Высокое качество (медленно)
  - `1`: Минимальное значение (очень быстро)

- **`num_bag_sets=1`**: Количество наборов моделей
  - `1`: Один набор (быстрое обучение)
  - `2`: Два набора (стандартное значение)
  - `3`: Три набора (высокое качество)
  - `5`: Пять наборов (максимальное качество)

- **`ag_args_fit={'num_cpus': 2}`**: Дополнительные аргументы обучения
  - `'num_cpus': 2`: Использовать 2 CPU ядра
  - `'num_cpus': 4`: Использовать 4 CPU ядра (рекомендуется)
  - `'num_cpus': 8`: Использовать 8 CPU ядер (для мощных систем)

- **`ag_args_fit={'memory_limit': 4}`**: Ограничение памяти
  - `'memory_limit': 4`: 4 GB памяти
  - `'memory_limit': 8`: 8 GB памяти (рекомендуется)
  - `'memory_limit': 16`: 16 GB памяти (для больших данных)

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
```

**Детальные описания параметров диагностики качества данных:**

- **`data.shape`**: Размеры датасета
  - `(1000, 10)`: 1000 строк, 10 столбцов (малый датасет)
  - `(10000, 50)`: 10000 строк, 50 столбцов (средний датасет)
  - `(100000, 100)`: 100000 строк, 100 столбцов (большой датасет)
  - Применение: оценка размера данных для обучения

- **`data.isnull().sum().sum()`**: Общее количество пропущенных значений
  - `0`: Нет пропущенных значений (идеально)
  - `100`: 100 пропущенных значений (приемлемо)
  - `1000+`: Много пропущенных значений (требует обработки)
  - `> 10%`: Критический уровень пропущенных значений

- **`data.dtypes.value_counts()`**: Распределение типов данных
  - `int64`: Целочисленные данные
  - `float64`: Вещественные данные
  - `object`: Строковые/категориальные данные
  - `datetime64`: Временные данные

- **`target_counts`**: Распределение целевой переменной
  - `{0: 800, 1: 200}`: Дисбаланс 4:1 (приемлемо)
  - `{0: 900, 1: 100}`: Дисбаланс 9:1 (требует внимания)
  - `{0: 950, 1: 50}`: Дисбаланс 19:1 (критический)

- **`imbalance_ratio`**: Коэффициент дисбаланса классов
  - `1.0`: Идеальный баланс (1:1)
  - `2.0`: Легкий дисбаланс (2:1)
  - `5.0`: Умеренный дисбаланс (5:1)
  - `10.0+`: Сильный дисбаланс (10:1+)

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

<img src="images/optimized/prediction_issues.png" alt="Проблемы предсказаний" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 16.4: Диагностика и решение проблем предсказаний AutoML Gluon - типы ошибок и методы исправления*

**Типы проблем предсказаний:**
- **Prediction Errors**: Ошибки при выполнении предсказаний
- **Unstable Predictions**: Нестабильные результаты
- **Slow Predictions**: Медленные предсказания
- **Wrong Format**: Неправильный формат данных
- **Missing Features**: Отсутствующие признаки
- **Data Type Mismatch**: Несоответствие типов данных

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

<img src="images/optimized/performance_issues.png" alt="Проблемы производительности" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 16.5: Диагностика и решение проблем производительности AutoML Gluon - метрики и оптимизация*

**Почему проблемы производительности критичны для продакшена?** Потому что медленные системы неэффективны и дороги:

**Типы проблем производительности:**
- **Slow Predictions**: Медленные предсказания
- **High Memory Usage**: Высокое использование памяти
- **GPU Problems**: Проблемы с GPU
- **CPU Bottlenecks**: Узкие места CPU
- **Network Issues**: Проблемы с сетью
- **Disk I/O Problems**: Проблемы с диском

**Ключевые аспекты проблем производительности:**
- **Медленные предсказания**: Неоптимизированные модели, неэффективные алгоритмы
- **Высокое использование памяти**: Утечки памяти, неэффективное управление ресурсами
- **Проблемы с GPU**: Неправильная настройка GPU, неэффективное использование
- **Проблемы с CPU**: Неоптимальная настройка потоков, узкие места
- **Проблемы с сетью**: Медленная передача данных, неэффективные протоколы
- **Проблемы с диском**: Медленный I/O, неэффективное кэширование

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
```

**Детальные описания параметров оптимизации производительности:**

- **`batch_size = 1000`**: Размер пакета для обработки
  - `1000`: Стандартный размер пакета (рекомендуется)
  - `500`: Меньший пакет (для ограниченной памяти)
  - `2000`: Больший пакет (для быстрых систем)
  - `100`: Минимальный пакет (для очень медленных систем)

- **`range(0, len(data), batch_size)`**: Итерация по данным
  - `0`: Начальный индекс
  - `len(data)`: Конечный индекс
  - `batch_size`: Шаг итерации
  - Применение: обработка данных по частям

- **`data.iloc[i:i+batch_size]`**: Выборка данных
  - `i`: Начальный индекс пакета
  - `i+batch_size`: Конечный индекс пакета
  - `iloc`: Позиционный доступ к данным
  - Преимущества: эффективная работа с большими датасетами

**Дополнительные параметры оптимизации:**

- **`predictor.predict(batch)`**: Предсказание для пакета
  - `batch`: Данные пакета
  - Возвращает: массив предсказаний
  - Оптимизация: обработка множественных образцов одновременно

- **`predictions.extend(batch_predictions)`**: Объединение результатов
  - `extend()`: Добавляет все элементы списка
  - `append()`: Добавляет один элемент
  - Преимущества: эффективное объединение массивов

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
```

**Детальные описания параметров создания быстрой модели:**

- **`label=predictor.label`**: Целевая переменная
  - Копирует целевую переменную из исходной модели
  - Обеспечивает совместимость с данными
  - Применение: сохранение структуры задачи

- **`problem_type=predictor.problem_type`**: Тип задачи
  - `'binary'`: Бинарная классификация
  - `'multiclass'`: Многоклассовая классификация
  - `'regression'`: Регрессия
  - `'quantile'`: Квантильная регрессия

- **`eval_metric=predictor.eval_metric`**: Метрика оценки
  - `'accuracy'`: Точность (классификация)
  - `'rmse'`: RMSE (регрессия)
  - `'mae'`: MAE (регрессия)
  - `'f1'`: F1-score (классификация)

- **`path='./fast_models'`**: Путь для сохранения модели
  - `'./fast_models'`: Локальная папка
  - `'./models/fast'`: Вложенная папка
  - `'/tmp/fast_models'`: Временная папка
  - Применение: изоляция быстрых моделей

- **`hyperparameters={'GBM': [{'num_boost_round': 50}]}`**: Гиперпараметры
  - `'GBM'`: Gradient Boosting Machine
  - `'num_boost_round': 50`: 50 итераций (быстро)
  - `'RF'`: Random Forest
  - `'n_estimators': 50`: 50 деревьев (быстро)

- **`time_limit=300`**: Ограничение времени обучения
  - `300`: 5 минут (быстрое обучение)
  - `600`: 10 минут (стандартное время)
  - `1800`: 30 минут (качественные модели)
  - Применение: контроль времени обучения

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

<img src="images/optimized/production_issues.png" alt="Проблемы продакшена" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 16.6: Диагностика и решение проблем продакшена AutoML Gluon - критичность и решения*

**Почему проблемы продакшена самые критичные?** Потому что они влияют на реальных пользователей и бизнес:

**Типы проблем продакшена:**
- **Model Loading Errors**: Ошибки загрузки модели
- **API Errors**: Ошибки API
- **Infrastructure Problems**: Проблемы с инфраструктурой
- **Monitoring Issues**: Проблемы с мониторингом
- **Security Vulnerabilities**: Уязвимости безопасности
- **Scaling Problems**: Проблемы масштабирования

**Ключевые аспекты проблем продакшена:**
- **Ошибки загрузки модели**: Проблемы с сериализацией, несовместимость версий
- **Ошибки API**: Неправильная настройка API, проблемы с форматами данных
- **Проблемы с инфраструктурой**: Нехватка ресурсов, проблемы с сетью
- **Проблемы с мониторингом**: Отсутствие алертов, неправильные метрики
- **Проблемы с безопасностью**: Уязвимости, неправильная аутентификация
- **Проблемы с масштабированием**: Неэффективное масштабирование, узкие места

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

<img src="images/optimized/diagnostic_tools.png" alt="Инструменты диагностики" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 16.7: Полезные инструменты диагностики и мониторинга AutoML Gluon - компоненты и преимущества*

**Почему важны инструменты диагностики?** Потому что они помогают быстро выявить и решить проблемы:

**Типы инструментов диагностики:**
- **System Monitoring**: Мониторинг системы в реальном времени
- **Logging System**: Система логирования событий
- **Performance Profiling**: Профилирование производительности
- **Metrics Collection**: Сбор метрик
- **Alerting System**: Система уведомлений
- **Dashboard Visualization**: Визуализация данных

**Ключевые аспекты инструментов диагностики:**
- **Система мониторинга**: Отслеживание производительности в реальном времени
- **Система логирования**: Детальная фиксация всех событий и ошибок
- **Профилирование**: Выявление узких мест в производительности
- **Метрики**: Количественные показатели качества системы
- **Алертинг**: Уведомления о проблемах в реальном времени
- **Дашборды**: Визуализация состояния системы

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
```

**Детальные описания параметров системы мониторинга:**

- **`memory.percent > 90`**: Проверка использования памяти
  - `90`: Критический порог (90% использования)
  - `80`: Предупреждающий порог (80% использования)
  - `95`: Экстремальный порог (95% использования)
  - Применение: предотвращение нехватки памяти

- **`cpu > 90`**: Проверка использования CPU
  - `90`: Критический порог (90% использования)
  - `80`: Предупреждающий порог (80% использования)
  - `95`: Экстремальный порог (95% использования)
  - Применение: предотвращение перегрузки CPU

- **`disk.percent > 90`**: Проверка использования диска
  - `90`: Критический порог (90% использования)
  - `80`: Предупреждающий порог (80% использования)
  - `95`: Экстремальный порог (95% использования)
  - Применение: предотвращение нехватки места на диске

- **`self.alerts.append()`**: Добавление алертов
  - `"High memory usage"`: Алерт о высокой памяти
  - `"High CPU usage"`: Алерт о высокой загрузке CPU
  - `"High disk usage"`: Алерт о высокой загрузке диска
  - Применение: уведомления о проблемах

- **`len(self.alerts) == 0`**: Проверка наличия алертов
  - `True`: Нет алертов (система здорова)
  - `False`: Есть алерты (система нездорова)
  - Применение: общая оценка состояния системы
    
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
```

**Детальные описания параметров системы логирования:**

- **`level=logging.INFO`**: Уровень логирования
  - `logging.DEBUG`: Отладочная информация (все сообщения)
  - `logging.INFO`: Информационные сообщения (рекомендуется)
  - `logging.WARNING`: Предупреждения и ошибки
  - `logging.ERROR`: Только ошибки
  - `logging.CRITICAL`: Только критические ошибки

- **`format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'`**: Формат логов
  - `%(asctime)s`: Время события
  - `%(name)s`: Имя логгера
  - `%(levelname)s`: Уровень логирования
  - `%(message)s`: Сообщение
  - Применение: структурированное логирование

- **`logging.FileHandler(self.log_file)`**: Обработчик файла
  - `self.log_file`: Путь к файлу лога
  - `'autogluon.log'`: Стандартное имя файла
  - `'./logs/autogluon.log'`: Вложенная папка
  - Применение: сохранение логов в файл

- **`logging.StreamHandler()`**: Обработчик консоли
  - Выводит логи в консоль
  - Полезно для отладки
  - Применение: мониторинг в реальном времени

- **`logging.getLogger(__name__)`**: Создание логгера
  - `__name__`: Имя текущего модуля
  - Создает уникальный логгер
  - Применение: идентификация источника логов
    
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
