# Troubleshooting AutoML Gluon

**Author:** Shcherbyna Rostyslav
**Дата:** 2024

## Why Troubleshooting критически важен

**Почему 80% времени ML-разработки тратится on решение проблем?** Потому что машинное обучение - это сложная система, где множество компонентов должны Workingть вместе. Это как диагностика автомобиля - нужно знать, где искать проблему.

### Катастрофические Consequences нерешенных проблем
- **Потеря времени**: Дни on решение простых проблем
- **Фрустрация team**: Разработчики бросают проект
- **Плохие результаты**: Модели Workingют неэффективно
- **Потеря доверия**: Заказчики теряют веру in ML

### Преимущества системного Troubleshooting
- **Быстрое решение**: Знание типичных проблем and их решений
- **Профилактика**: Предотвращение проблем to их возникновения
- **Эффективность**: Больше времени on разработку, меньше on отладку
- **Уверенность**: Команда знает, как решать проблемы

## Введение in Troubleshooting

<img src="images/optimized/Troubleshooting_flowchart.png" alt="Troubleshooting блок-схема" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 16.1: Блок-схема решения проблем AutoML Gluon - систематический подход к диагностике and решению*

**Почему Troubleshooting - это искусство, а not наука?** Потому что каждая проблема уникальна, но паттерны повторяются. Это как медицинская диагностика - симптомы похожи, но причины разные.

**Ключевые принципы Troubleshooting:**
- **Систематический подход**: Пошаговая диагностика проблем
- **Документирование**: Фиксация всех проблем and решений
- **Тестирование**: check эффективности решений
- **Профилактика**: Предотвращение повторных проблем
- **Обучение team**: Передача знаний and опыта

**Типы проблем in AutoML Gluon:**
- **Проблемы установки**: Конфликты зависимостей, версии Python
- **Проблемы данных**: Форматы, размеры, качество
- **Проблемы производительности**: Медленная Working, нехватка памяти
- **Проблемы моделей**: Плохая точность, переобучение

in этом разделе рассмотрим типичные проблемы, возникающие при работе with AutoML Gluon, and способы их решения. Каждая проблема включает description, причины возникновения and пошаговые instructions on устранению.

## Проблемы установки

<img src="images/optimized/installation_issues.png" alt="Проблемы установки" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 16.2: Диагностика and решение проблем установки AutoML Gluon - типы проблем and их решения*

**Почему проблемы установки - самые частые in ML?** Потому что ML-библиотеки имеют сложные dependencies между собой. Это как пазл, где каждая деталь должна точно подходить.

**Типы проблем установки:**
- **Dependency Conflicts**: Конфликты версий пакетов
- **Python Version Issues**: Неправильная версия Python
- **CUDA Problems**: Issues with GPU поддержкой
- **Memory Issues**: Нехватка памяти при установке
- **Permission Problems**: Недостаточные права доступа
- **Virtual Environment Issues**: Issues with виртуальными окружениями

**Ключевые аспекты проблем установки:**
- **Конфликты зависимостей**: Несовместимые версии пакетов
- **Issues with Python**: Неправильная версия Python
- **Issues with pip/conda**: Конфликты менеджеров пакетов
- **Issues with системными библиотеками**: Отсутствующие системные dependencies
- **Issues with виртуальными окружениями**: Неправильная configuration окружений
- **Issues with правами доступа**: Недостаточные права to install

### 1. Ошибки зависимостей

**Почему конфликты версий так распространены?** Потому что разные библиотеки требуют разные версии одних and тех же пакетов. Это как попытка использовать детали from разных моделей автомобилей.

#### Проблема: Конфликт версий пакетов
```bash
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
This behaviour is the source of the following dependency conflicts.
```

**Почему возникает эта ошибка?** Потому что pip пытается установить пакеты, которые конфликтуют друг with другом. Это как попытка установить simultaneously Windows and Linux.

**Решение:**
```bash
# create нового окружения - изоляция from других проектов
conda create -n autogluon python=3.9
conda activate autogluon

# installation in правильном порядке - сначала базовые, потом специфичные
pip install --upgrade pip
pip install autogluon

# or installation конкретных версий - фиксация совместимых версий
pip install autogluon==0.8.2
pip install torch==1.13.1
pip install torchvision==0.14.1
```

**Детальные описания параметров решения конфликтов зависимостей:**

- **`conda create -n autogluon python=3.9`**: create изолированного окружения
 - `-n autogluon`: Имя окружения (может быть любым)
 - `python=3.9`: Версия Python (3.8-3.11 поддерживаются)
 - Преимущества: полная изоляция from системных пакетов

- **`conda activate autogluon`**: Активация окружения
 - Активирует созданное окружение
 - Изолирует установленные пакеты
 - Предотвращает конфликты with другими проектами

- **`pip install --upgrade pip`**: update pip
 - Устанавливает последнюю версию pip
 - Улучшает разрешение зависимостей
 - Рекомендуется перед установкой пакетов

- **`pip install autogluon`**: installation AutoGluon
 - Устанавливает последнюю стабильную версию
 - Автоматически разрешает dependencies
 - Может занять 5-15 minutes

- **`pip install autogluon==0.8.2`**: installation конкретной версии
 - `0.8.2`: Стабильная версия (рекомендуется)
 - `0.8.1`: Предыдущая версия
 - `0.9.0`: Бета-версия (not рекомендуется for продакшена)

- **`pip install torch==1.13.1`**: installation PyTorch
 - `1.13.1`: Совместимая версия with AutoGluon
 - `1.12.1`: Предыдущая стабильная версия
 - `1.14.0`: Новая версия (может быть несовместима)

- **`pip install torchvision==0.14.1`**: installation TorchVision
 - `0.14.1`: Совместимая версия with PyTorch 1.13.1
 - `0.13.1`: Предыдущая версия
 - `0.15.0`: Новая версия (может быть несовместима)

#### Проблема: Ошибки CUDA
```bash
RuntimeError: CUDA out of memory
```

**Решение:**
```python
# check CUDA
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA Version: {torch.version.cuda}")

# installation совместимой версии PyTorch
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117

# or отключение CUDA
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
```

**Детальные описания параметров решения проблем CUDA:**

- **`torch.cuda.is_available()`**: check доступности CUDA
 - `True`: CUDA доступна and Workingет
 - `False`: CUDA недоступна or not установлена
 - Причины False: неправильная installation, несовместимая версия

- **`torch.version.cuda`**: Версия CUDA
 - `11.7`: CUDA 11.7 (рекомендуется)
 - `11.6`: CUDA 11.6 (поддерживается)
 - `12.0`: CUDA 12.0 (может быть несовместима)

- **`pip install torch==1.13.1+cu117`**: installation PyTorch with CUDA
 - `1.13.1`: Версия PyTorch
 - `+cu117`: Версия CUDA (11.7)
 - `--extra-index-url`: Дополнительный индекс пакетов

- **`torchvision==0.14.1+cu117`**: installation TorchVision with CUDA
 - `0.14.1`: Версия TorchVision
 - `+cu117`: Версия CUDA (11.7)
 - Должна соответствовать версии PyTorch

- **`os.environ['CUDA_VISIBLE_DEVICES'] = ''`**: Отключение CUDA
 - `''`: Пустая строка отключает все GPU
 - `'0'`: Использовать только GPU 0
 - `'0,1'`: Использовать GPU 0 and 1
 - Применение: при проблемах with памятью GPU

### 2. Issues with памятью

#### Проблема: Out of memory
```bash
MemoryError: Unable to allocate array
```

**Решение:**
```python
# Ограничение использования памяти
import autogluon as ag
ag.set_config({'memory_limit': 4}) # 4GB

# or через переменные окружения
import os
os.environ['AUTOGLUON_MEMORY_LIMIT'] = '4'

# Уменьшение размера данных
train_data = train_data.sample(frac=0.5) # Использовать 50% данных
```

**Детальные описания параметров решения проблем with памятью:**

- **`ag.set_config({'memory_limit': 4})`**: Ограничение памяти AutoGluon
 - `4`: Лимит памяти in GB (рекомендуется 4-8 GB)
 - `2`: Минимальный лимит for небольших данных
 - `8`: Максимальный лимит for больших данных
 - `16+`: for очень больших данных

- **`os.environ['AUTOGLUON_MEMORY_LIMIT'] = '4'`**: installation через переменные окружения
 - `'4'`: Лимит памяти in GB (строка)
 - `'2'`: Минимальный лимит
 - `'8'`: Максимальный лимит
 - Преимущества: глобальная configuration for всех процессов

- **`train_data.sample(frac=0.5)`**: Уменьшение размера данных
 - `0.5`: Использовать 50% данных (рекомендуется)
 - `0.3`: Использовать 30% данных (for очень больших датасетов)
 - `0.7`: Использовать 70% данных (компромисс между качеством and памятью)
 - `0.1`: Использовать 10% данных (только for тестирования)

**Дополнительные parameters оптимизации памяти:**

- **`ag.set_config({'num_cpus': 2})`**: Ограничение CPU
 - `2`: Использовать 2 CPU ядра
 - `4`: Использовать 4 CPU ядра (рекомендуется)
 - `8`: Использовать 8 CPU ядер (for мощных систем)

- **`ag.set_config({'time_limit': 300})`**: Ограничение времени обучения
 - `300`: 5 minutes (for быстрого тестирования)
 - `600`: 10 minutes (стандартное время)
 - `1800`: 30 minutes (for качественных моделей)

## Проблемы обучения

<img src="images/optimized/training_issues.png" alt="Проблемы обучения" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 16.3: Диагностика and решение проблем обучения AutoML Gluon - типы проблем and методы решения*

**Почему проблемы обучения так критичны?** Потому что они influence качество and скорость получения результатов:

**Типы проблем обучения:**
- **Slow Training**: Медленное обучение модели
- **Poor Model Quality**: Низкое качество модели
- **Validation Errors**: Ошибки валидации
- **data Quality Issues**: Issues with качеством данных
- **Resource Shortage**: Нехватка вычислительных ресурсов
- **Configuration Problems**: Issues with конфигурацией

**Ключевые аспекты проблем обучения:**
- **Медленное обучение**: Неоптимальные settings, нехватка ресурсов
- **Плохое качество модели**: Неправильные data, переобучение
- **Ошибки валидации**: Неправильное разделение данных
- **Issues with data**: Некачественные or неподходящие data
- **Issues with ресурсами**: Нехватка памяти, CPU, GPU
- **Issues with конфигурацией**: Неправильные parameters обучения

### 1. Медленное обучение

#### Проблема: Обучение занимает слишком много времени
```python
# Диагностика
import time
start_time = time.time()

# Обучение with Monitoringом
predictor.fit(train_data, time_limit=300) # 5 minutes for теста

print(f"Training time: {time.time() - start_time:.2f} seconds")
```

**Решение:**
```python
# Оптимизация параметров
predictor.fit(
 train_data,
 presets='optimize_for_deployment', # Быстрое обучение
 time_limit=600, # 10 minutes
 num_bag_folds=3, # Меньше фолдов
 num_bag_sets=1,
 ag_args_fit={
 'num_cpus': 2, # Ограничение CPU
 'memory_limit': 4 # Ограничение памяти
 }
)
```

**Детальные описания параметров оптимизации обучения:**

- **`presets='optimize_for_deployment'`**: Предустановка for быстрого обучения
 - `'optimize_for_deployment'`: Быстрое обучение (рекомендуется)
 - `'best_quality'`: Максимальное качество (медленно)
 - `'medium_quality_faster_train'`: Компромисс качества and скорости
 - `'fast'`: Очень быстрое обучение (низкое качество)

- **`time_limit=600`**: Ограничение времени обучения
 - `600`: 10 minutes (стандартное время)
 - `300`: 5 minutes (быстрое тестирование)
 - `1800`: 30 minutes (качественные модели)
 - `3600`: 1 час (максимальное качество)

- **`num_bag_folds=3`**: Количество фолдов for bagging
 - `3`: Быстрое обучение (рекомендуется for оптимизации)
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
 - `'num_cpus': 8`: Использовать 8 CPU ядер (for мощных систем)

- **`ag_args_fit={'memory_limit': 4}`**: Ограничение памяти
 - `'memory_limit': 4`: 4 GB памяти
 - `'memory_limit': 8`: 8 GB памяти (рекомендуется)
 - `'memory_limit': 16`: 16 GB памяти (for больших данных)

### 2. Плохое качество модели

#### Проблема: Низкая точность модели
```python
# Диагностика качества данных
def diagnose_data_quality(data):
 """Диагностика качества данных"""

 print("data shape:", data.shape)
 print("Missing values:", data.isnull().sum().sum())
 print("data types:", data.dtypes.value_counts())

 # check целевой переменной
 if 'target' in data.columns:
 print("Target distribution:")
 print(data['target'].value_counts())

 # check on дисбаланс
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
 - Применение: оценка размера данных for обучения

- **`data.isnull().sum().sum()`**: Общее количество пропущенных значений
 - `0`: Нет пропущенных значений (идеально)
 - `100`: 100 пропущенных значений (приемлемо)
 - `1000+`: Много пропущенных значений (требует обработки)
 - `> 10%`: Критический уровень пропущенных значений

- **`data.dtypes.value_counts()`**: Распределение типов данных
 - `int64`: Целочисленные data
 - `float64`: Вещественные data
 - `object`: Строковые/категориальные data
 - `datetime64`: Временные data

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
# improve качества данных
def improve_data_quality(data):
 """improve качества данных"""

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

 # create новых признаков
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
 # check совместимости данных
 print("Test data shape:", test_data.shape)
 print("Test data columns:", test_data.columns.toList())

 # check типов данных
 print("data types:")
 print(test_data.dtypes)

 # check пропущенных значений
 print("Missing values:")
 print(test_data.isnull().sum())

 # Попытка предсказания
 Predictions = predictor.predict(test_data)
 print("Predictions shape:", Predictions.shape)

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
# fix проблем валидации
def fix_validation_issues(test_data):
 """fix проблем валидации"""

 # Обработка пропущенных значений
 test_data = test_data.fillna(test_data.median())

 # Приведение типов данных
 for col in test_data.columns:
 if test_data[col].dtype == 'object':
 # Попытка преобразования in числовой тип
 try:
 test_data[col] = pd.to_numeric(test_data[col])
 except:
 # Если not удается, оставляем как есть
 pass

 # remove константных columns
 constant_columns = test_data.columns[test_data.nunique() <= 1]
 test_data = test_data.drop(columns=constant_columns)

 return test_data

# Использование
test_data_fixed = fix_validation_issues(test_data)
```

## Проблемы Predictions

<img src="images/optimized/Prediction_issues.png" alt="Проблемы Predictions" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 16.4: Диагностика and решение проблем Predictions AutoML Gluon - типы ошибок and методы исправления*

**Типы проблем Predictions:**
- **Prediction Errors**: Ошибки при выполнении Predictions
- **Unstable Predictions**: Нестабильные результаты
- **Slow Predictions**: Медленные предсказания
- **Wrong Format**: Неправильный формат данных
- **Missing Features**: Отсутствующие признаки
- **data Type Mismatch**: Несоответствие типов данных

### 1. Ошибки Predictions

#### Проблема: Ошибки при предсказании
```python
# Диагностика Predictions
def diagnose_Prediction_issues(predictor, data):
 """Диагностика проблем Predictions"""

 try:
 # check входных данных
 print("Input data shape:", data.shape)
 print("Input data types:", data.dtypes)

 # check совместимости with моделью
 model_features = predictor.feature_importance().index.toList()
 data_features = data.columns.toList()

 missing_features = set(model_features) - set(data_features)
 extra_features = set(data_features) - set(model_features)

 if missing_features:
 print(f"Missing features: {missing_features}")
 if extra_features:
 print(f"Extra features: {extra_features}")

 # Попытка предсказания
 Predictions = predictor.predict(data)
 print("Predictions successful")

 return True

 except Exception as e:
 print(f"Prediction error: {e}")
 return False

# Использование
if not diagnose_Prediction_issues(predictor, new_data):
 print("Prediction issues detected")
```

**Решение:**
```python
# fix проблем Predictions
def fix_Prediction_issues(predictor, data):
 """fix проблем Predictions"""

 # Получение ожидаемых признаков
 expected_features = predictor.feature_importance().index.toList()

 # add недостающих признаков
 for feature in expected_features:
 if feature not in data.columns:
 data[feature] = 0 # Заполнение нулями

 # remove лишних признаков
 data = data[expected_features]

 # Обработка пропущенных значений
 data = data.fillna(0)

 return data

# Использование
new_data_fixed = fix_Prediction_issues(predictor, new_data)
Predictions = predictor.predict(new_data_fixed)
```

### 2. Нестабильные предсказания

#### Проблема: Нестабильные результаты
```python
# Диагностика стабильности
def diagnose_Prediction_stability(predictor, data, n_tests=5):
 """Диагностика стабильности Predictions"""

 Predictions = []

 for i in range(n_tests):
 pred = predictor.predict(data)
 Predictions.append(pred)

 # check согласованности
 Predictions_array = np.array(Predictions)
 consistency = np.mean(Predictions_array == Predictions_array[0])

 print(f"Prediction consistency: {consistency:.4f}")

 if consistency < 0.95:
 print("WARNING: Unstable Predictions detected")

 return consistency

# Использование
consistency = diagnose_Prediction_stability(predictor, test_data)
```

**Решение:**
```python
# Стабилизация Predictions
def stabilize_Predictions(predictor, data, n_samples=3):
 """Стабилизация Predictions"""

 Predictions = []

 for _ in range(n_samples):
 # add небольшого шума for стабилизации
 noisy_data = data.copy()
 for col in noisy_data.columns:
 if noisy_data[col].dtype in [np.float64, np.int64]:
 noise = np.random.normal(0, 0.01, len(noisy_data))
 noisy_data[col] += noise

 pred = predictor.predict(noisy_data)
 Predictions.append(pred)

 # Усреднение Predictions
 if predictor.problem_type == 'regression':
 stable_Predictions = np.mean(Predictions, axis=0)
 else:
 # for классификации - голосование
 stable_Predictions = []
 for i in range(len(Predictions[0])):
 votes = [pred[i] for pred in Predictions]
 stable_Predictions.append(max(set(votes), key=votes.count))

 return stable_Predictions

# Использование
stable_Predictions = stabilize_Predictions(predictor, test_data)
```

## Проблемы производительности

<img src="images/optimized/performance_issues.png" alt="Проблемы производительности" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 16.5: Диагностика and решение проблем производительности AutoML Gluon - метрики and оптимизация*

**Почему проблемы производительности критичны for продакшена?** Потому что медленные системы неэффективны and дороги:

**Типы проблем производительности:**
- **Slow Predictions**: Медленные предсказания
- **High Memory Usage**: Высокое использование памяти
- **GPU Problems**: Issues with GPU
- **CPU Bottlenecks**: Узкие места CPU
- **network Issues**: Issues with network
- **Disk I/O Problems**: Issues with диском

**Ключевые аспекты проблем производительности:**
- **Медленные предсказания**: Неоптимизированные модели, неэффективные алгоритмы
- **Высокое использование памяти**: Утечки памяти, неэффективное Management ресурсами
- **Issues with GPU**: Неправильная configuration GPU, неэффективное использование
- **Issues with CPU**: Неоптимальная configuration потоков, узкие места
- **Issues with network**: Медленная передача данных, неэффективные протоколы
- **Issues with диском**: Медленный I/O, неэффективное кэширование

### 1. Медленные предсказания

#### Проблема: Медленные предсказания
```python
# Диагностика производительности
import time

def diagnose_Prediction_performance(predictor, data):
 """Диагностика производительности Predictions"""

 # Тест on небольшой выборке
 small_data = data.head(100)

 start_time = time.time()
 Predictions = predictor.predict(small_data)
 Prediction_time = time.time() - start_time

 print(f"Prediction time for 100 samples: {Prediction_time:.4f} seconds")
 print(f"Prediction time per sample: {Prediction_time/100:.6f} seconds")

 # Оценка времени for полного датасета
 estimated_time = Prediction_time * len(data) / 100
 print(f"Estimated time for full dataset: {estimated_time:.2f} seconds")

 return Prediction_time

# Использование
Prediction_time = diagnose_Prediction_performance(predictor, test_data)
```

**Решение:**
```python
# Оптимизация производительности
def optimize_Prediction_performance(predictor, data):
 """Оптимизация производительности Predictions"""

 # Пакетная обработка
 batch_size = 1000
 Predictions = []

 for i in range(0, len(data), batch_size):
 batch = data.iloc[i:i+batch_size]
 batch_Predictions = predictor.predict(batch)
 Predictions.extend(batch_Predictions)

 return Predictions
```

**Детальные описания параметров оптимизации производительности:**

- **`batch_size = 1000`**: Размер пакета for обработки
 - `1000`: Стандартный размер пакета (рекомендуется)
 - `500`: Меньший пакет (for ограниченной памяти)
 - `2000`: Больший пакет (for быстрых систем)
 - `100`: Минимальный пакет (for очень медленных систем)

- **`range(0, len(data), batch_size)`**: Итерация on данным
 - `0`: Начальный индекс
 - `len(data)`: Конечный индекс
 - `batch_size`: Шаг итерации
 - Применение: обработка данных on частям

- **`data.iloc[i:i+batch_size]`**: Выборка данных
 - `i`: Начальный индекс пакета
 - `i+batch_size`: Конечный индекс пакета
 - `iloc`: Позиционный доступ к данным
 - Преимущества: эффективная Working with большими датасетами

**Дополнительные parameters оптимизации:**

- **`predictor.predict(batch)`**: Prediction for пакета
 - `batch`: data пакета
 - Возвращает: массив Predictions
 - Оптимизация: обработка множественных образцов simultaneously

- **`Predictions.extend(batch_Predictions)`**: Объединение результатов
 - `extend()`: Добавляет все элементы списка
 - `append()`: Добавляет один элемент
 - Преимущества: эффективное объединение массивов

# or использование более простой модели
def create_fast_model(predictor, data):
 """create быстрой модели"""

 fast_predictor = TabularPredictor(
 label=predictor.label,
 problem_type=predictor.problem_type,
 eval_metric=predictor.eval_metric,
 path='./fast_models'
 )

 # Обучение только on быстрых алгоритмах
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
 - Обеспечивает совместимость with data
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

- **`path='./fast_models'`**: Путь for сохранения модели
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
 - `300`: 5 minutes (быстрое обучение)
 - `600`: 10 minutes (стандартное время)
 - `1800`: 30 minutes (качественные модели)
 - Применение: контроль времени обучения

# Использование
fast_predictor = create_fast_model(predictor, train_data)
fast_Predictions = fast_predictor.predict(test_data)
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

 # Обработка данных on частям
 chunk_size = 1000
 Predictions = []

 for i in range(0, len(data), chunk_size):
 chunk = data.iloc[i:i+chunk_size]
 chunk_Predictions = predictor.predict(chunk)
 Predictions.extend(chunk_Predictions)

 # clean памяти
 del chunk
 gc.collect()

 return Predictions

# or использование более эффективных типов данных
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
*Рисунок 16.6: Диагностика and решение проблем продакшена AutoML Gluon - критичность and решения*

**Почему проблемы продакшена самые критичные?** Потому что они influence реальных пользователей and бизнес:

**Типы проблем продакшена:**
- **Model Loading Errors**: Ошибки загрузки модели
- **API Errors**: Ошибки API
- **InfraStructure Problems**: Issues with инфраструктурой
- **Monitoring Issues**: Issues with Monitoringом
- **Security Vulnerabilities**: Уязвимости безопасности
- **Scaling Problems**: Проблемы масштабирования

**Ключевые аспекты проблем продакшена:**
- **Ошибки загрузки модели**: Issues with сериализацией, несовместимость версий
- **Ошибки API**: Неправильная configuration API, Issues with форматами данных
- **Issues with инфраструктурой**: Нехватка ресурсов, Issues with network
- **Issues with Monitoringом**: Отсутствие алертов, неправильные метрики
- **Issues with безопасностью**: Уязвимости, неправильная Authentication
- **Issues with масштабированием**: Неэффективное масштабирование, узкие места

### 1. Ошибки загрузки модели

#### Проблема: Ошибки при загрузке модели
```python
# Диагностика загрузки модели
def diagnose_model_Loading(model_path):
 """Диагностика загрузки модели"""

 try:
 # check существования файлов
 import os
 if not os.path.exists(model_path):
 print(f"Model path does not exist: {model_path}")
 return False

 # check структуры модели
 required_files = ['predictor.pkl', 'metadata.json']
 for file in required_files:
 file_path = os.path.join(model_path, file)
 if not os.path.exists(file_path):
 print(f"required file missing: {file_path}")
 return False

 # Попытка загрузки
 predictor = TabularPredictor.load(model_path)
 print("Model loaded successfully")
 return True

 except Exception as e:
 print(f"Model Loading error: {e}")
 return False

# Использование
if not diagnose_model_Loading('./models'):
 print("Model Loading issues detected")
```

**Решение:**
```python
# fix проблем загрузки модели
def fix_model_Loading_issues(model_path):
 """fix проблем загрузки модели"""

 try:
 # check версии AutoGluon
 import autogluon as ag
 print(f"AutoGluon Version: {ag.__version__}")

 # Загрузка with проверкой совместимости
 predictor = TabularPredictor.load(
 model_path,
 require_version_match=False # Игнорировать несовпадение версий
 )

 return predictor

 except Exception as e:
 print(f"Failed to load model: {e}")

 # Попытка пересоздания модели
 print("Attempting to recreate model...")
 # Здесь должна быть логика пересоздания модели
 return None

# Использование
predictor = fix_model_Loading_issues('./models')
```

### 2. Ошибки API

#### Проблема: Ошибки in API
```python
# Диагностика API
def diagnose_api_issues(api_url, test_data):
 """Диагностика проблем API"""

 try:
 # health check
 response = requests.get(f"{api_url}/health")
 if response.status_code != 200:
 print(f"health check failed: {response.status_code}")
 return False

 # Тест предсказания
 response = requests.post(f"{api_url}/predict", json=test_data)
 if response.status_code != 200:
 print(f"Prediction failed: {response.status_code}")
 print(f"Error: {response.text}")
 return False

 print("API Working correctly")
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
# fix проблем API
def fix_api_issues(api_url, test_data):
 """fix проблем API"""

 try:
 # check доступности API
 response = requests.get(f"{api_url}/health", timeout=5)

 if response.status_code == 200:
 health_data = response.json()
 print(f"API Status: {health_data['status']}")

 # check загруженных моделей
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
*Рисунок 16.7: Полезные инструменты диагностики and Monitoringа AutoML Gluon - components and преимущества*

**Почему важны инструменты диагностики?** Потому что они помогают быстро выявить and решить проблемы:

**Типы инструментов диагностики:**
- **system Monitoring**: Monitoring системы in реальном времени
- **Logging system**: Система логирования событий
- **Performance Profiling**: Профилирование производительности
- **Metrics Collection**: Сбор метрик
- **Alerting system**: Система уведомлений
- **Dashboard Visualization**: Визуализация данных

**Ключевые аспекты инструментов диагностики:**
- **Система Monitoringа**: Отслеживание производительности in реальном времени
- **Система логирования**: Детальная фиксация всех событий and ошибок
- **Профилирование**: Выявление узких мест in производительности
- **Метрики**: Количественные показатели качества системы
- **Алертинг**: Уведомления о проблемах in реальном времени
- **Дашборды**: Визуализация состояния системы

### 1. Система Monitoringа
```python
class AutoGluonMonitor:
 """Monitoring AutoGluon системы"""

 def __init__(self):
 self.metrics = {}
 self.alerts = []

 def check_system_health(self):
 """health check системы"""

 # check памяти
 memory = psutil.virtual_memory()
 if memory.percent > 90:
 self.alerts.append("High memory usage")

 # check CPU
 cpu = psutil.cpu_percent()
 if cpu > 90:
 self.alerts.append("High CPU usage")

 # check диска
 disk = psutil.disk_usage('/')
 if disk.percent > 90:
 self.alerts.append("High disk usage")

 return len(self.alerts) == 0
```

**Детальные описания параметров системы Monitoringа:**

- **`memory.percent > 90`**: check использования памяти
 - `90`: Критический порог (90% использования)
 - `80`: Предупреждающий порог (80% использования)
 - `95`: Экстремальный порог (95% использования)
 - Применение: предотвращение нехватки памяти

- **`cpu > 90`**: check использования CPU
 - `90`: Критический порог (90% использования)
 - `80`: Предупреждающий порог (80% использования)
 - `95`: Экстремальный порог (95% использования)
 - Применение: предотвращение перегрузки CPU

- **`disk.percent > 90`**: check использования диска
 - `90`: Критический порог (90% использования)
 - `80`: Предупреждающий порог (80% использования)
 - `95`: Экстремальный порог (95% использования)
 - Применение: предотвращение нехватки места on диске

- **`self.alerts.append()`**: add алертов
 - `"High memory usage"`: Алерт о высокой памяти
 - `"High CPU usage"`: Алерт о высокой загрузке CPU
 - `"High disk usage"`: Алерт о высокой загрузке диска
 - Применение: уведомления о проблемах

- **`len(self.alerts) == 0`**: check наличия алертов
 - `True`: Нет алертов (система здорова)
 - `False`: Есть алерты (система нездорова)
 - Применение: общая оценка состояния системы

 def check_model_performance(self, predictor, test_data):
 """check производительности модели"""

 try:
 # Тест предсказания
 start_time = time.time()
 Predictions = predictor.predict(test_data.head(100))
 Prediction_time = time.time() - start_time

 # check времени
 if Prediction_time > 10: # 10 секунд for 100 образцов
 self.alerts.append("Slow Prediction performance")

 # check качества
 performance = predictor.evaluate(test_data.head(100))
 if performance.get('accuracy', 0) < 0.8:
 self.alerts.append("Low model accuracy")

 return True

 except Exception as e:
 self.alerts.append(f"Model performance error: {e}")
 return False

 def generate_Report(self):
 """Генерация Reportа"""

 Report = {
 'timestamp': datetime.now().isoformat(),
 'system_health': self.check_system_health(),
 'alerts': self.alerts,
 'metrics': self.metrics
 }

 return Report

# Использование
monitor = AutoGluonMonitor()
Report = monitor.generate_Report()
print("Monitoring Report:", Report)
```

### 2. Система логирования
```python
import logging
from datetime import datetime

class AutoGluonLogger:
 """Система логирования for AutoGluon"""

 def __init__(self, log_file='autogluon.log'):
 self.log_file = log_file
 self.setup_logging()

 def setup_logging(self):
 """configuration логирования"""

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
 - `logging.DEBUG`: Отладочная информация (все messages)
 - `logging.INFO`: Информационные messages (рекомендуется)
 - `logging.WARNING`: Предупреждения and ошибки
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
 - Применение: сохранение логов in файл

- **`logging.StreamHandler()`**: Обработчик консоли
 - Выводит логи in консоль
 - Полезно for отладки
 - Применение: Monitoring in реальном времени

- **`logging.getLogger(__name__)`**: create логгера
 - `__name__`: Имя текущего модуля
 - Создает уникальный логгер
 - Применение: идентификация источника логов

 def log_training_start(self, data_info):
 """Логирование начала обучения"""
 self.logger.info(f"Training started: {data_info}")

 def log_training_complete(self, results):
 """Логирование завершения обучения"""
 self.logger.info(f"Training COMPLETED: {results}")

 def log_Prediction(self, input_data, Prediction, processing_time):
 """Логирование предсказания"""
 self.logger.info(f"Prediction: input={input_data}, Prediction={Prediction}, time={processing_time}")

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
