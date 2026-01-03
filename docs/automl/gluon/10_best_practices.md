# Лучшие практики AutoML Gluon

**Author:** Shcherbyna Rostyslav
**Дата:** 2024

## Why лучшие практики критически важны

**Почему 95% ML-проектов терпят неудачу из-за игнорирования лучших практик?** Потому что машинное обучение - это not просто "обучить модель", а комплексная дисциплина, требующая соблюдения множества правил and принципов.

### Катастрофические Consequences плохих практик
- **Amazon AI-рекрутинг**: Дискриминация из-за отсутствия разнообразия in данных
- **Microsoft Tay**: Расистские твиты из-за отсутствия модерации
- **Uber самоуправляемые авто**: Смерть пешехода из-за недостаточного тестирования
- **Facebook алгоритм**: Поляризация общества из-за неправильной оптимизации

### Преимущества следования лучшим практикам
- **Надежность**: Система Workingет стабильно in любых условиях
- **Масштабируемость**: Легко адаптируется к росту нагрузки
- **Поддерживаемость**: Команда может легко развивать system
- **Этичность**: Система Workingет справедливо and безопасно

## Введение in лучшие практики

<img src="images/optimized/performance_comparison.png" alt="Сравнение производительности" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 1: Сравнение производительности различных моделей*

<img src="images/optimized/robustness_Analysis.png" alt="Анализ робастности" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 2: Анализ робастности - робастные vs переобученные системы, стабильность производительности*

**Почему лучшие практики - это not просто "сделать хорошо"?** Это систематический подход к решению типичных проблем, основанный on опыте тысяч проектов. Это как медицинские протоколы - они спасают жизни.

**Почему 80% ML-проектов повторяют одни and те же ошибки?** Потому что team not знают о существовании проверенных решений:
- **Issues with data**: Неправильная подготовка, утечки, смещения
- **Issues with валидацией**: Неправильное разделение, переобучение
- **Issues with продакшеном**: Неготовность к реальным условиям
- **Issues with этикой**: Дискриминация, предвзятость, безопасность

Лучшие практики - это накопленный опыт использования AutoML Gluon, который поможет избежать типичных ошибок and достичь максимальной эффективности. in этом разделе рассмотрим все аспекты правильного использования инструмента.

## Подготовка данных

<img src="images/optimized/advanced_topics_overView.png" alt="Подготовка данных" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 3: Лучшие практики подготовки данных for ML*

**Почему критически важна правильная подготовка данных?** Потому что качество данных напрямую влияет on качество модели:

- **clean данных**: remove шума, fix ошибок
- **Обработка пропусков**: Стратегии заполнения отсутствующих значений
- **Нормализация**: Приведение данных к единому масштабу
- **Feature Engineering**: create новых признаков
- **Валидация данных**: check качества and консистентности
- **Документирование**: Фиксация all преобразований

### 1. Качество данных

**Почему "мусор on входе = мусор on выходе" особенно актуально for ML?** Потому что модель учится on данных, and если data плохие, модель будет делать плохие предсказания. Это как обучение врача on неправильных диагнозах.

**Почему 60% времени ML-проекта тратится on подготовку данных?** Потому что реальные data всегда "грязные":
- **Отсутствующие значения**: 30-50% данных могут быть пустыми
- **Некорректные значения**: Опечатки, неправильные форматы
- **Дубликаты**: Одинаковые записи in разных форматах
- **Выбросы**: Экстремальные значения, которые искажают модель

**Типы проблем with data:**
- **Структурные проблемы**: Неправильные типы данных, форматы
- **Семантические проблемы**: Некорректные значения, Logsческие ошибки
- **Статистические проблемы**: Смещения, корреляции, выбросы
- **Этические проблемы**: Дискриминация, предвзятость

```python
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import matplotlib.pyplot as plt
import seaborn as sns

def data_quality_check(data: pd.dataFrame) -> Dict[str, Any]:
 """
 Комплексная check качества данных - первый шаг к успешному ML

 Parameters:
 -----------
 data : pd.dataFrame
 Датафрейм for проверки качества данных. Должен содержать:
 - Числовые and категориальные колонки
 - Целевую переменную (if present)
 - Временные метки (for временных рядов)

 Returns:
 --------
 Dict[str, Any]
 Словарь with результатами проверки качества:
 - shape: tuple - размер датасета (строки, колонки)
 - Missing_values: dict - количество пропущенных значений on колонкам
 - Missing_percent: dict - процент пропущенных значений on колонкам
 - data_types: dict - типы данных on колонкам
 - duplicates: int - количество дублированных строк
 - outliers: dict - количество выбросов on числовым колонкам
 - correlations: dict - матрица корреляций между числовыми колонками

 Notes:
 ------
 function использует следующие методы детекции выбросов:
 - IQR (Interquartile Range): Q1 - 1.5*IQR to Q3 + 1.5*IQR
 - Корреляции рассчитываются только for числовых columns
 - Дубликаты определяются on полному совпадению all значений
 """

 quality_Report = {
 'shape': data.shape, # Размер датасета (строки, колонки)
 'Missing_values': data.isnull().sum().to_dict(), # Пропущенные значения on колонкам
 'data_types': data.dtypes.to_dict(), # Типы данных on колонкам
 'duplicates': data.duplicated().sum(), # Количество дублированных строк
 'outliers': {}, # Выбросы on числовым колонкам
 'correlations': {} # Корреляции между числовыми колонками
 }

 # check пропущенных значений
 Missing_percent = (data.isnull().sum() / len(data)) * 100
 quality_Report['Missing_percent'] = Missing_percent.to_dict()

 # check выбросов for числовых columns
 numeric_columns = data.select_dtypes(include=[np.number]).columns
 for col in numeric_columns:
 Q1 = data[col].quantile(0.25)
 Q3 = data[col].quantile(0.75)
 IQR = Q3 - Q1
 outliers = data[(data[col] < Q1 - 1.5 * IQR) | (data[col] > Q3 + 1.5 * IQR)]
 quality_Report['outliers'][col] = len(outliers)

 # check корреляций
 if len(numeric_columns) > 1:
 correlation_matrix = data[numeric_columns].corr()
 quality_Report['correlations'] = correlation_matrix.to_dict()

 return quality_Report

# Использование
quality_Report = data_quality_check(train_data)
print("data Quality Report:")
for key, value in quality_Report.items():
 print(f"{key}: {value}")
```

### 2. Обработка пропущенных значений

```python
def handle_Missing_values(data: pd.dataFrame, strategy: str = 'auto') -> pd.dataFrame:
 """
 Обработка пропущенных значений in датасете

 Parameters:
 -----------
 data : pd.dataFrame
 Датафрейм with пропущенными значениями for обработки

 strategy : str, default='auto'
 Стратегия обработки пропущенных значений:
 - 'auto': Автоматический выбор стратегии on типу данных
 * for категориальных (object) - мода (наиболее частое значение)
 * for числовых - медиана (устойчива к выбросам)
 - 'drop': remove all строк with пропущенными значениями
 * Используется когда пропусков мало (< 5%)
 * Может значительно уменьшить размер датасета
 - 'interpolate': Линейная интерполяция for временных рядов
 * Подходит for временных данных with трендом
 * Сохраняет временную структуру данных
 - 'mean': Заполнение средним значением (только for числовых)
 - 'mode': Заполнение модой (наиболее частым значением)
 - 'forward_fill': Заполнение предыдущим значением
 - 'backward_fill': Заполнение следующим значением

 Returns:
 --------
 pd.dataFrame
 Датафрейм with обWorkingнными пропущенными значениями

 Notes:
 ------
 Рекомендации on выбору стратегии:
 - auto: Универсальная стратегия for большинства случаев
 - drop: Когда пропусков мало and data критически важны
 - interpolate: for временных рядов with трендом
 - mean/mode: Когда нужно сохранить статистические свойства
 """

 if strategy == 'auto':
 # Автоматическая стратегия - выбор on типу данных
 for col in data.columns:
 if data[col].dtype == 'object':
 # for категориальных переменных - мода (наиболее частое значение)
 # Если мода пустая, Use 'Unknown'
 data[col].fillna(data[col].mode()[0] if not data[col].mode().empty else 'Unknown', inplace=True)
 else:
 # for числовых переменных - медиана (устойчива к выбросам)
 data[col].fillna(data[col].median(), inplace=True)

 elif strategy == 'drop':
 # remove строк with пропущенными значениями
 # Используется когда пропусков мало (< 5%)
 data = data.dropna()

 elif strategy == 'interpolate':
 # Интерполяция for временных рядов
 # Сохраняет временную структуру данных
 data = data.interpolate(method='linear')

 elif strategy == 'mean':
 # Заполнение средним значением (только for числовых)
 numeric_cols = data.select_dtypes(include=[np.number]).columns
 data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())

 elif strategy == 'mode':
 # Заполнение модой (наиболее частым значением)
 for col in data.columns:
 mode_value = data[col].mode()[0] if not data[col].mode().empty else 'Unknown'
 data[col].fillna(mode_value, inplace=True)

 elif strategy == 'forward_fill':
 # Заполнение предыдущим значением
 data = data.fillna(method='ffill')

 elif strategy == 'backward_fill':
 # Заполнение следующим значением
 data = data.fillna(method='bfill')

 return data

# Использование
train_data_clean = handle_Missing_values(train_data, strategy='auto')
```

### 3. Обработка выбросов

```python
def handle_outliers(data: pd.dataFrame, method: str = 'iqr') -> pd.dataFrame:
 """
 Обработка выбросов in числовых данных

 Parameters:
 -----------
 data : pd.dataFrame
 Датафрейм with числовыми данными for обработки выбросов

 method : str, default='iqr'
 Метод обработки выбросов:
 - 'iqr': Межквартильный размах (IQR)
 * Выбросы: значения < Q1 - 1.5*IQR or > Q3 + 1.5*IQR
 * Заменяются on граничные значения (capping)
 * Умеренно консервативный подход
 - 'zscore': Z-скор метод
 * Выбросы: |z-score| > 3 (стандартное отклонение)
 * Полностью удаляются из датасета
 * Агрессивный подход, может потерять важную информацию
 - 'winsorize': Винзоризация (ограничение)
 * Заменяет 5% самых низких and 5% самых высоких значений
 * Сохраняет размер датасета
 * Консервативный подход
 - 'isolation_forest': Изоляционный лес
 * Использует ML for детекции аномалий
 * Более сложный, но точный метод
 - 'local_outlier_factor': LOF метод
 * Учитывает локальную плотность данных
 * Хорош for кластерных данных

 Returns:
 --------
 pd.dataFrame
 Датафрейм with обWorkingнными выбросами

 Notes:
 ------
 Рекомендации on выбору метода:
 - iqr: Универсальный метод for большинства случаев
 - zscore: Когда выбросы явно ошибочные
 - winsorize: Когда нужно сохранить все data
 - isolation_forest: for сложных паттернов выбросов
 - local_outlier_factor: for данных with кластерами
 """

 numeric_columns = data.select_dtypes(include=[np.number]).columns

 if method == 'iqr':
 # Метод межквартильного размаха (IQR)
 # Q1 = 25-й процентиль, Q3 = 75-й процентиль
 for col in numeric_columns:
 Q1 = data[col].quantile(0.25) # Первый квартиль
 Q3 = data[col].quantile(0.75) # Третий квартиль
 IQR = Q3 - Q1 # Межквартильный размах
 lower_bound = Q1 - 1.5 * IQR # Нижняя граница
 upper_bound = Q3 + 1.5 * IQR # Верхняя граница

 # Замена выбросов on граничные значения (capping)
 data[col] = np.where(data[col] < lower_bound, lower_bound, data[col])
 data[col] = np.where(data[col] > upper_bound, upper_bound, data[col])

 elif method == 'zscore':
 # Метод Z-скор (стандартизированные отклонения)
 # Z-score = (значение - среднее) / стандартное_отклонение
 for col in numeric_columns:
 z_scores = np.abs((data[col] - data[col].mean()) / data[col].std())
 # remove строк with |z-score| > 3 (агрессивный подход)
 data = data[z_scores < 3]

 elif method == 'winsorize':
 # Винзоризация - ограничение экстремальных значений
 # Заменяет 5% самых низких and 5% самых высоких значений
 for col in numeric_columns:
 lower_percentile = data[col].quantile(0.05) # 5-й процентиль
 upper_percentile = data[col].quantile(0.95) # 95-й процентиль
 # Замена экстремальных значений on процентили
 data[col] = np.where(data[col] < lower_percentile, lower_percentile, data[col])
 data[col] = np.where(data[col] > upper_percentile, upper_percentile, data[col])

 elif method == 'isolation_forest':
 # Изоляционный лес - ML метод for детекции аномалий
 from sklearn.ensemble import IsolationForest
 for col in numeric_columns:
 iso_forest = IsolationForest(contamination=0.1, random_state=42)
 outlier_mask = iso_forest.fit_predict(data[[col]]) == -1
 # Замена выбросов on медиану
 data.loc[outlier_mask, col] = data[col].median()

 elif method == 'local_outlier_factor':
 # Local Outlier Factor - учитывает локальную плотность
 from sklearn.neighbors import LocalOutlierFactor
 for col in numeric_columns:
 lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
 outlier_mask = lof.fit_predict(data[[col]]) == -1
 # Замена выбросов on медиану
 data.loc[outlier_mask, col] = data[col].median()

 return data

# Использование
train_data_no_outliers = handle_outliers(train_data, method='iqr')
```

## Выбор метрик

### 1. Метрики for классификации

```python
def select_classification_metrics(problem_type: str, data_balance: str = 'balanced') -> List[str]:
 """
 Выбор оптимальных метрик for задач классификации

 Parameters:
 -----------
 problem_type : str
 Тип задачи классификации:
 - 'binary': Бинарная классификация (2 класса)
 - 'multiclass': Многоклассовая классификация (3+ классов)
 - 'multilabel': Многометочная классификация (несколько меток simultaneously)

 data_balance : str, default='balanced'
 Баланс классов in данных:
 - 'balanced': Сбалансированные классы (примерно равное количество)
 - 'imbalanced': Несбалансированные классы (один класс значительно больше)
 - 'highly_imbalanced': Сильно несбалансированные классы (соотношение 1:100+)

 Returns:
 --------
 List[str]
 List рекомендуемых метрик for оценки модели:

 for бинарной классификации:
 - accuracy: Общая точность (правильные предсказания / все предсказания)
 - f1: F1-мера (гармоническое среднее precision and recall)
 - roc_auc: Площадь под ROC-кривой (качество разделения классов)
 - precision: Точность (правильные положительные / все положительные)
 - recall: Полнота (правильные положительные / все реальные положительные)
 - balanced_accuracy: Сбалансированная точность (устойчива к дисбалансу)

 for многоклассовой классификации:
 - f1_macro: F1-мера with макро-усреднением (среднее on классам)
 - f1_micro: F1-мера with микро-усреднением (глобальные TP, FP, FN)
 - precision_macro/recall_macro: Макро-усредненные precision and recall

 Notes:
 ------
 Рекомендации on выбору метрик:
 - Сбалансированные data: accuracy, f1, roc_auc
 - Несбалансированные data: f1, roc_auc, balanced_accuracy
 - Критически важные случаи: precision (ложные срабатывания дороги)
 - Пропуск важных случаев недопустим: recall (ложные пропуски дороги)
 """

 if problem_type == 'binary':
 if data_balance == 'balanced':
 # Сбалансированные data - стандартные метрики
 return ['accuracy', 'f1', 'roc_auc', 'precision', 'recall']
 elif data_balance == 'imbalanced':
 # Несбалансированные data - метрики устойчивые к дисбалансу
 return ['f1', 'roc_auc', 'precision', 'recall', 'balanced_accuracy']
 else:
 # Универсальный набор for бинарной классификации
 return ['accuracy', 'f1', 'roc_auc']

 elif problem_type == 'multiclass':
 if data_balance == 'balanced':
 # Сбалансированные многоклассовые data
 return ['accuracy', 'f1_macro', 'f1_micro', 'precision_macro', 'recall_macro']
 elif data_balance == 'imbalanced':
 # Несбалансированные многоклассовые data
 return ['f1_macro', 'f1_micro', 'balanced_accuracy', 'precision_macro', 'recall_macro']
 else:
 # Универсальный набор for многоклассовой классификации
 return ['accuracy', 'f1_macro', 'f1_micro']

 else:
 # Fallback for неизвестных типов задач
 return ['accuracy', 'f1', 'roc_auc']

# Использование
metrics = select_classification_metrics('binary', 'imbalanced')
predictor = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric=metrics[0] # Основная метрика
)
```

### 2. Метрики for регрессии

```python
def select_regression_metrics(problem_type: str, target_distribution: str = 'normal') -> List[str]:
 """
 Выбор оптимальных метрик for задач регрессии

 Parameters:
 -----------
 problem_type : str
 Тип задачи регрессии (in данном контексте всегда 'regression')

 target_distribution : str, default='normal'
 Распределение целевой переменной:
 - 'normal': Нормальное распределение (симметричное, без выбросов)
 - 'skewed': Асимметричное распределение (логарифмическое, экспоненциальное)
 - 'outliers': Распределение with выбросами (экстремальные значения)
 - 'multimodal': Многомодальное распределение (несколько пиков)
 - 'uniform': Равномерное распределение

 Returns:
 --------
 List[str]
 List рекомендуемых метрик for оценки регрессионной модели:

 Основные метрики:
 - rmse: Root Mean Square Error (корень из среднеквадратичной ошибки)
 * Чувствительна к выбросам, in тех же единицах что and целевая переменная
 * Штрафует большие ошибки сильнее малых
 - mae: Mean Absolute Error (средняя абсолютная ошибка)
 * Устойчива к выбросам, простая for интерпретации
 * Все ошибки имеют одинаковый вес
 - r2: Коэффициент детерминации (R-squared)
 * Доля объясненной дисперсии (0-1, чем больше тем лучше)
 * Показывает качество модели относительно среднего значения

 Специализированные метрики:
 - mape: Mean Absolute Percentage Error (средняя абсолютная процентная ошибка)
 * Выражается in процентах, легко интерпретируется
 * Проблемы при делении on ноль and очень малых значениях
 - smape: Symmetric Mean Absolute Percentage Error
 * Симметричная версия MAPE, более стабильная
 - huber_loss: function потерь Хубера
 * Комбинация MAE and MSE, устойчива к выбросам
 - mape_log: MAPE on логарифмической шкале
 * for мультипликативных ошибок

 Notes:
 ------
 Рекомендации on выбору метрик:
 - Нормальное распределение: rmse, mae, r2 (стандартный набор)
 - Асимметричное распределение: mae, mape, smape (процентные метрики)
 - data with выбросами: mae, huber_loss (устойчивые метрики)
 - Многомодальное распределение: mae, r2 (базовые метрики)
 - Равномерное распределение: rmse, mae (стандартные метрики)
 """

 if target_distribution == 'normal':
 # Нормальное распределение - стандартные метрики
 return ['rmse', 'mae', 'r2']
 elif target_distribution == 'skewed':
 # Асимметричное распределение - процентные метрики
 return ['mae', 'mape', 'smape']
 elif target_distribution == 'outliers':
 # Распределение with выбросами - устойчивые метрики
 return ['mae', 'huber_loss']
 elif target_distribution == 'multimodal':
 # Многомодальное распределение - базовые метрики
 return ['mae', 'r2', 'rmse']
 elif target_distribution == 'uniform':
 # Равномерное распределение - стандартные метрики
 return ['rmse', 'mae', 'r2']
 else:
 # Fallback for неизвестных типов распределения
 return ['rmse', 'mae']

# Использование
metrics = select_regression_metrics('regression', 'normal')
predictor = TabularPredictor(
 label='target',
 problem_type='regression',
 eval_metric=metrics[0]
)
```

## configuration гиперпараметров

### 1. Стратегия поиска гиперпараметров

```python
def create_hyperparameter_strategy(data_size: int, problem_type: str) -> Dict[str, Any]:
 """
 create стратегии поиска гиперпараметров on basis размера данных

 Parameters:
 -----------
 data_size : int
 Размер обучающего датасета (количество строк):
 - < 1000: Маленький датасет - простые модели, быстрая конвергенция
 - 1000-10000: Средний датасет - умеренная сложность, баланс качества and скорости
 - > 10000: Большой датасет - сложные модели, высокое качество

 problem_type : str
 Тип задачи machine learning:
 - 'binary': Бинарная классификация
 - 'multiclass': Многоклассовая классификация
 - 'regression': Регрессия
 - 'multilabel': Многометочная классификация

 Returns:
 --------
 Dict[str, Any]
 Словарь with конфигурациями гиперпараметров for разных алгоритмов:

 GBM (Gradient Boosting Machine):
 - num_boost_round: Количество итераций бустинга (100-1000)
 - learning_rate: Скорость обучения (0.01-0.3)
 - max_depth: Максимальная глубина деревьев (3-12)
 - subsample: Доля образцов for каждой итерации (0.5-1.0)
 - colsample_bytree: Доля признаков for каждого дерева (0.5-1.0)

 RF (Random Forest):
 - n_estimators: Количество деревьев (100-1000)
 - max_depth: Максимальная глубина деревьев (5-25)
 - min_samples_split: Минимум образцов for разделения узла (2-20)
 - min_samples_leaf: Минимум образцов in листе (1-10)
 - max_features: Количество признаков for разделения ('sqrt', 'log2', None)

 XGB (XGBoost):
 - n_estimators: Количество итераций (100-1000)
 - max_depth: Максимальная глубина деревьев (3-12)
 - learning_rate: Скорость обучения (0.01-0.3)
 - subsample: Доля образцов (0.5-1.0)
 - colsample_bytree: Доля признаков (0.5-1.0)
 - reg_alpha: L1 регуляризация (0-10)
 - reg_lambda: L2 регуляризация (0-10)

 CAT (CatBoost):
 - iterations: Количество итераций (100-1000)
 - learning_rate: Скорость обучения (0.01-0.3)
 - depth: Глубина деревьев (3-12)
 - l2_leaf_reg: L2 регуляризация (1-10)
 - border_count: Количество границ for числовых признаков (32-255)

 Notes:
 ------
 Стратегия выбора гиперпараметров:
 - Маленькие датасеты: Простые модели, быстрая конвергенция, избегание переобучения
 - Средние датасеты: Баланс между качеством and скоростью, умеренная сложность
 - Большие датасеты: Сложные модели, высокое качество, использование all данных
 """

 if data_size < 1000:
 # Маленький датасет - простые модели, быстрая конвергенция
 # Избегаем переобучения, Use простые конфигурации
 return {
 'GBM': [{'num_boost_round': 100, 'learning_rate': 0.1, 'max_depth': 3}],
 'RF': [{'n_estimators': 100, 'max_depth': 10, 'min_samples_split': 5}],
 'XGB': [{'n_estimators': 100, 'max_depth': 6, 'learning_rate': 0.1}]
 }

 elif data_size < 10000:
 # Средний датасет - умеренная сложность, баланс качества and скорости
 # Use несколько конфигураций for поиска оптимальной
 return {
 'GBM': [
 {'num_boost_round': 200, 'learning_rate': 0.1, 'max_depth': 6},
 {'num_boost_round': 300, 'learning_rate': 0.05, 'max_depth': 8}
 ],
 'RF': [
 {'n_estimators': 200, 'max_depth': 15, 'min_samples_split': 3},
 {'n_estimators': 300, 'max_depth': 20, 'min_samples_split': 2}
 ],
 'XGB': [
 {'n_estimators': 200, 'max_depth': 8, 'learning_rate': 0.1},
 {'n_estimators': 300, 'max_depth': 10, 'learning_rate': 0.05}
 ]
 }

 else:
 # Большой датасет - сложные модели, высокое качество
 # Use все доступные алгоритмы with оптимальными параметрами
 return {
 'GBM': [
 {'num_boost_round': 500, 'learning_rate': 0.1, 'max_depth': 8},
 {'num_boost_round': 1000, 'learning_rate': 0.05, 'max_depth': 10}
 ],
 'RF': [
 {'n_estimators': 500, 'max_depth': 20, 'min_samples_split': 2},
 {'n_estimators': 1000, 'max_depth': 25, 'min_samples_split': 1}
 ],
 'XGB': [
 {'n_estimators': 500, 'max_depth': 10, 'learning_rate': 0.1},
 {'n_estimators': 1000, 'max_depth': 12, 'learning_rate': 0.05}
 ],
 'CAT': [
 {'iterations': 500, 'learning_rate': 0.1, 'depth': 8},
 {'iterations': 1000, 'learning_rate': 0.05, 'depth': 10}
 ]
 }

# Использование
hyperparameters = create_hyperparameter_strategy(len(train_data), 'binary')
predictor.fit(train_data, hyperparameters=hyperparameters)
```

### 2. Оптимизация времени обучения

```python
def optimize_training_time(data_size: int, available_time: int) -> Dict[str, Any]:
 """
 Оптимизация времени обучения on basis размера данных and доступного времени

 Parameters:
 -----------
 data_size : int
 Размер обучающего датасета (количество строк):
 - < 1000: Маленький датасет - быстрое обучение, простые модели
 - 1000-10000: Средний датасет - умеренное обучение, баланс качества and скорости
 - > 10000: Большой датасет - качественное обучение, сложные модели

 available_time : int
 Доступное время for обучения in секундах:
 - < 1800 (30 мин): Быстрое обучение, простые модели
 - 1800-7200 (30 мин - 2 часа): Умеренное обучение
 - > 7200 (2+ часа): Качественное обучение, сложные модели

 Returns:
 --------
 Dict[str, Any]
 configuration for оптимизации времени обучения:

 time_limit : int
 Максимальное время обучения одной модели in секундах
 Рассчитывается как available_time / количество_моделей

 presets : str
 Предустановленные конфигурации AutoGluon:
 - 'optimize_for_deployment': Быстрое обучение, простые модели
 * Минимальное время, базовое качество
 * Подходит for прототипов and быстрых экспериментов
 - 'medium_quality': Умеренное качество, баланс времени and качества
 * Хорошее качество за разумное время
 * Подходит for большинства задач
 - 'high_quality': Высокое качество, длительное обучение
 * Максимальное качество, больше времени
 * Подходит for продакшена and критически важных задач
 - 'best_quality': Лучшее качество, очень длительное обучение
 * Максимальное качество, очень много времени
 * Подходит for исследований and конкурсов

 num_bag_folds : int
 Количество фолдов for бэггинга (3-10):
 - 3: Быстрое обучение, базовое качество
 - 5: Стандартное качество, умеренное время
 - 10: Высокое качество, длительное время

 num_bag_sets : int
 Количество наборов бэггинга (1-3):
 - 1: Стандартный бэггинг
 - 2: Двойной бэггинг for лучшего качества
 - 3: Тройной бэггинг for максимального качества

 num_stack_levels : int
 Количество уровней стекинга (0-2):
 - 0: Без стекинга (быстрое обучение)
 - 1: Один уровень стекинга (умеренное качество)
 - 2: Два уровня стекинга (высокое качество)

 Notes:
 ------
 Стратегия оптимизации времени:
 - Маленькие датасеты: Быстрое обучение, избегание переобучения
 - Средние датасеты: Баланс между качеством and временем
 - Большие датасеты: Качественное обучение, использование all данных
 - Ограниченное время: Простые модели, быстрая конвергенция
 - Достаточно времени: Сложные модели, высокое качество
 """

 # Расчет времени on модель (10 моделей on умолчанию)
 # Можно настроить количество моделей in dependencies from доступного времени
 num_models = min(10, max(3, available_time // 300)) # 3-10 моделей, минимум 5 minutes on модель
 time_per_model = available_time // num_models

 if data_size < 1000:
 # Быстрое обучение for маленьких датасетов
 # Избегаем переобучения, Use простые модели
 return {
 'time_limit': time_per_model,
 'presets': 'optimize_for_deployment',
 'num_bag_folds': 3, # Минимальное количество фолдов
 'num_bag_sets': 1, # Один набор бэггинга
 'num_stack_levels': 0 # Без стекинга
 }

 elif data_size < 10000:
 # Умеренное обучение for средних датасетов
 # Баланс между качеством and временем
 return {
 'time_limit': time_per_model,
 'presets': 'medium_quality',
 'num_bag_folds': 5, # Стандартное количество фолдов
 'num_bag_sets': 1, # Один набор бэггинга
 'num_stack_levels': 1 # Один уровень стекинга
 }

 else:
 # Качественное обучение for больших датасетов
 # Максимальное качество, использование all данных
 return {
 'time_limit': time_per_model,
 'presets': 'high_quality',
 'num_bag_folds': 5, # Стандартное количество фолдов
 'num_bag_sets': 2, # Двойной бэггинг for лучшего качества
 'num_stack_levels': 2 # Два уровня стекинга
 }

# Использование
training_config = optimize_training_time(len(train_data), 3600) # 1 час
predictor.fit(train_data, **training_config)
```

## Валидация and тестирование

<img src="images/optimized/validation_methods.png" alt="Валидация and тестирование" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 4: Лучшие практики валидации and тестирования ML-моделей*

**Почему критически важна правильная валидация?** Потому что неправильная валидация приводит к переобучению and нереалистичным оценкам:

- **Стратегии валидации**: Выбор подходящего метода for задачи
- **Разделение данных**: Правильное разделение on train/validation/test
- **Кросс-валидация**: Надежная оценка производительности
- **Временные ряды**: Специальные методы for временных данных
- **A/B тестирование**: Сравнение моделей in реальных условиях
- **Статистические тесты**: check значимости различий

### 1. Стратегия валидации

```python
def select_validation_strategy(data_size: int, problem_type: str,
 data_type: str = 'tabular') -> Dict[str, Any]:
 """
 Выбор оптимальной стратегии валидации on basis характеристик данных

 Parameters:
 -----------
 data_size : int
 Размер обучающего датасета (количество строк):
 - < 1000: Маленький датасет - holdout валидация
 - 1000-10000: Средний датасет - k-fold валидация (5 фолдов)
 - > 10000: Большой датасет - k-fold валидация (10 фолдов)

 problem_type : str
 Тип задачи machine learning:
 - 'binary': Бинарная классификация
 - 'multiclass': Многоклассовая классификация
 - 'regression': Регрессия
 - 'multilabel': Многометочная классификация

 data_type : str, default='tabular'
 Тип данных:
 - 'tabular': Табличные data (стандартная валидация)
 - 'time_series': Временные ряды (временная валидация)
 - 'image': Изображения (стратифицированная валидация)
 - 'text': Текстовые data (случайная валидация)

 Returns:
 --------
 Dict[str, Any]
 configuration стратегии валидации:

 validation_strategy : str
 Тип стратегии валидации:
 - 'holdout': Простое разделение on train/validation
 * Быстрое, подходит for больших датасетов
 * Может быть нестабильным for маленьких датасетов
 - 'kfold': K-fold кросс-валидация
 * Более стабильная оценка производительности
 * Подходит for средних and больших датасетов
 - 'time_series_split': Временная валидация
 * Сохраняет временную структуру данных
 * Подходит for временных рядов and прогнозирования
 - 'stratified_kfold': Стратифицированная валидация
 * Сохраняет пропорции классов in каждом фолде
 * Подходит for несбалансированных данных

 n_splits : int
 Количество фолдов for k-fold валидации (3-10):
 - 3: Быстрая валидация, базовое качество
 - 5: Стандартная валидация, хорошее качество
 - 10: Тщательная валидация, высокое качество

 test_size : float
 Доля данных for тестирования (0.1-0.3):
 - 0.1: 10% for тестирования (больше данных for обучения)
 - 0.2: 20% for тестирования (стандартное разделение)
 - 0.3: 30% for тестирования (больше данных for тестирования)

 holdout_frac : float
 Доля данных for holdout валидации (0.2-0.4):
 - 0.2: 20% for валидации (больше данных for обучения)
 - 0.3: 30% for валидации (стандартное разделение)
 - 0.4: 40% for валидации (больше данных for валидации)

 num_bag_folds : int
 Количество фолдов for бэггинга (3-10):
 - 3: Быстрое обучение, базовое качество
 - 5: Стандартное качество, умеренное время
 - 10: Высокое качество, длительное время

 num_bag_sets : int
 Количество наборов бэггинга (1-3):
 - 1: Стандартный бэггинг
 - 2: Двойной бэггинг for лучшего качества
 - 3: Тройной бэггинг for максимального качества

 Notes:
 ------
 Рекомендации on выбору стратегии валидации:
 - Временные ряды: time_series_split (сохранение temporary структуры)
 - Маленькие датасеты: holdout (больше данных for обучения)
 - Средние датасеты: k-fold 5 (баланс стабильности and времени)
 - Большие датасеты: k-fold 10 (максимальная стабильность)
 - Несбалансированные data: stratified_kfold (сохранение пропорций)
 """

 if data_type == 'time_series':
 # Временные ряды - специальная валидация
 # Сохраняем временную структуру данных
 return {
 'validation_strategy': 'time_series_split',
 'n_splits': 5, # Стандартное количество фолдов
 'test_size': 0.2 # 20% for тестирования
 }

 elif data_size < 1000:
 # Маленький датасет - holdout валидация
 # Больше данных for обучения, простая валидация
 return {
 'validation_strategy': 'holdout',
 'holdout_frac': 0.3 # 30% for валидации
 }

 elif data_size < 10000:
 # Средний датасет - k-fold валидация
 # Баланс между стабильностью and временем
 return {
 'validation_strategy': 'kfold',
 'num_bag_folds': 5, # 5 фолдов for стабильности
 'num_bag_sets': 1 # Один набор бэггинга
 }

 else:
 # Большой датасет - расширенная k-fold валидация
 # Максимальная стабильность оценки
 return {
 'validation_strategy': 'kfold',
 'num_bag_folds': 10, # 10 фолдов for максимальной стабильности
 'num_bag_sets': 1 # Один набор бэггинга
 }

# Использование
validation_config = select_validation_strategy(len(train_data), 'binary')
predictor.fit(train_data, **validation_config)
```

### 2. Кросс-валидация

```python
def perform_cross_validation(predictor, data: pd.dataFrame,
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

## Working with ансамблями

### 1. configuration ансамблей

```python
def configure_ensemble(data_size: int, problem_type: str) -> Dict[str, Any]:
 """configuration ансамбля"""

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
 ensemble_Analysis = {
 'total_models': len(leaderboard),
 'best_model': leaderboard.iloc[0]['model'],
 'best_score': leaderboard.iloc[0]['score_val'],
 'model_diversity': calculate_model_diversity(leaderboard),
 'performance_gap': leaderboard.iloc[0]['score_val'] - leaderboard.iloc[-1]['score_val']
 }

 return ensemble_Analysis

def calculate_model_diversity(leaderboard: pd.dataFrame) -> float:
 """Расчет разнообразия моделей"""

 # Разнообразие on типам моделей
 model_types = leaderboard['model'].str.split('_').str[0].value_counts()
 diversity = len(model_types) / len(leaderboard)

 return diversity

# Использование
ensemble_Analysis = analyze_ensemble(predictor)
print("Ensemble Analysis:")
for key, value in ensemble_Analysis.items():
 print(f"{key}: {value}")
```

## Оптимизация производительности

<img src="images/optimized/metrics_Detailed.png" alt="Оптимизация производительности" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 5: Лучшие практики оптимизации производительности ML-моделей*

**Почему важна оптимизация производительности?** Потому что медленные модели неэффективны in продакшене:

- **configuration ресурсов**: Оптимальное использование CPU, памяти, GPU
- **Параллелизация**: Ускорение обучения and инференса
- **Кэширование**: Сохранение результатов for повторного использования
- **Профилирование**: Выявление узких мест in производительности
- **Monitoring**: Отслеживание метрик производительности
- **Масштабирование**: Адаптация к росту нагрузки

### 1. configuration ресурсов

```python
def optimize_resources(data_size: int, available_resources: Dict[str, int]) -> Dict[str, Any]:
 """
 Оптимизация использования системных ресурсов for обучения AutoGluon

 Parameters:
 -----------
 data_size : int
 Размер обучающего датасета (количество строк):
 - < 1000: Маленький датасет - минимальные ресурсы
 - 1000-10000: Средний датасет - умеренные ресурсы
 - > 10000: Большой датасет - максимальные ресурсы

 available_resources : Dict[str, int]
 Доступные системные ресурсы:
 - 'cpus': int - количество доступных CPU ядер (1-64)
 - 'memory': int - доступная память in GB (4-256)
 - 'gpus': int - количество доступных GPU (0-8)
 - 'disk': int - доступное место on диске in GB (100-10000)

 Returns:
 --------
 Dict[str, Any]
 Оптимизированная configuration ресурсов:

 num_cpus : int
 Количество CPU ядер for обучения (1-8):
 - 1-2: Маленькие датасеты, быстрые эксперименты
 - 3-4: Средние датасеты, стандартное обучение
 - 5-8: Большие датасеты, интенсивное обучение
 - >8: Очень большие датасеты, максимальная производительность

 num_gpus : int
 Количество GPU for обучения (0-8):
 - 0: CPU-only обучение (универсально)
 - 1: Один GPU for acceleration (рекомендуется)
 - 2-4: Множественные GPU for large models
 - >4: Экстремально большие модели

 memory_limit : int
 Лимит памяти in GB (4-64):
 - 4-8: Маленькие датасеты, простые модели
 - 8-16: Средние датасеты, стандартные модели
 - 16-32: Большие датасеты, сложные модели
 - 32-64: Очень большие датасеты, максимальные модели

 disk_space : int
 Требуемое место on диске in GB (1-100):
 - 1-5: Простые модели, минимальное место
 - 5-20: Стандартные модели, умеренное место
 - 20-50: Сложные модели, много места
 - 50-100: Очень сложные модели, максимальное место

 parallel_folds : bool
 Параллельное выполнение фолдов:
 - True: Ускорение обучения, больше ресурсов
 - False: Последовательное выполнение, меньше ресурсов

 parallel_models : bool
 parallel training моделей:
 - True: Максимальное ускорение, много ресурсов
 - False: sequential training, меньше ресурсов

 Notes:
 ------
 Стратегия оптимизации ресурсов:
 - Маленькие датасеты: Минимальные ресурсы, избегание избыточности
 - Средние датасеты: Баланс между производительностью and ресурсами
 - Большие датасеты: Максимальное использование ресурсов
 - Ограниченные ресурсы: Последовательное выполнение, оптимизация памяти
 - Избыточные ресурсы: Параллельное выполнение, максимальная скорость
 """

 # Расчет оптимальных параметров on basis размера данных
 if data_size < 1000:
 # Маленький датасет - минимальные ресурсы
 # Избегаем избыточного использования ресурсов
 num_cpus = min(2, available_resources.get('cpus', 4))
 memory_limit = min(4, available_resources.get('memory', 8))
 parallel_folds = False # Последовательное выполнение
 parallel_models = False # sequential training
 disk_space = 5 # Минимальное место on диске

 elif data_size < 10000:
 # Средний датасет - умеренные ресурсы
 # Баланс между производительностью and ресурсами
 num_cpus = min(4, available_resources.get('cpus', 8))
 memory_limit = min(8, available_resources.get('memory', 16))
 parallel_folds = True # Параллельные фолды
 parallel_models = False # Последовательные модели
 disk_space = 20 # Умеренное место on диске

 else:
 # Большой датасет - максимальные ресурсы
 # Use все доступные ресурсы
 num_cpus = min(8, available_resources.get('cpus', 16))
 memory_limit = min(16, available_resources.get('memory', 32))
 parallel_folds = True # Параллельные фолды
 parallel_models = True # Параллельные модели
 disk_space = 50 # Много места on диске

 # Дополнительная оптимизация on basis доступных ресурсов
 if available_resources.get('cpus', 0) < 4:
 # Ограниченные CPU - отключаем параллелизм
 parallel_folds = False
 parallel_models = False
 elif available_resources.get('memory', 0) < 8:
 # Limited memory - уменьшаем лимиты
 memory_limit = min(memory_limit, 4)
 parallel_models = False

 return {
 'num_cpus': num_cpus,
 'num_gpus': available_resources.get('gpus', 0),
 'memory_limit': memory_limit,
 'disk_space': disk_space,
 'parallel_folds': parallel_folds,
 'parallel_models': parallel_models
 }

# Использование
resources = optimize_resources(len(train_data), {'cpus': 8, 'memory': 16, 'gpus': 1})
predictor.fit(train_data, ag_args_fit=resources)
```

### 2. Параллелизация

```python
def configure_parallelization(data_size: int, problem_type: str) -> Dict[str, Any]:
 """configuration параллелизации"""

 if data_size < 1000:
 # sequential training
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

## Monitoring and Logsрование

<img src="images/optimized/production_architecture.png" alt="Monitoring and Logsрование" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 6: Лучшие практики Monitoringа and Logsрования ML-систем*

**Почему критически важен Monitoring ML-систем?** Потому что модели могут деградировать and Workingть некорректно:

- **Система Logsрования**: Детальная фиксация all events
- **Monitoring качества**: Отслеживание метрик производительности
- **Детекция дрейфа**: Обнаружение изменений in данных
- **Алертинг**: notifications о проблемах in реальном времени
- **Дашборды**: Визуализация состояния системы
- **Анализ логов**: Поиск причин проблем and оптимизация

### 1. Система Logsрования

```python
import logging
from datetime import datetime
import json

class AutoGluonLogger:
 """Система Logsрования for AutoGluon"""

 def __init__(self, log_file: str = 'autogluon.log'):
 self.log_file = log_file
 self.setup_logging()

 def setup_logging(self):
 """configuration Logsрования"""
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
 """Logsрование начала обучения"""
 self.logger.info(f"Training started: {data_info}")

 def log_training_progress(self, progress: Dict[str, Any]):
 """Logsрование прогресса обучения"""
 self.logger.info(f"Training progress: {progress}")

 def log_training_complete(self, results: Dict[str, Any]):
 """Logsрование завершения обучения"""
 self.logger.info(f"Training COMPLETED: {results}")

 def log_Prediction(self, input_data: Dict, Prediction: Any,
 processing_time: float):
 """Logsрование предсказания"""
 log_entry = {
 'timestamp': datetime.now().isoformat(),
 'input_data': input_data,
 'Prediction': Prediction,
 'processing_time': processing_time
 }
 self.logger.info(f"Prediction: {log_entry}")

 def log_error(self, error: Exception, context: Dict[str, Any]):
 """Logsрование ошибок"""
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

### 2. Monitoring производительности

```python
import psutil
import time
from typing import Dict, Any

class PerformanceMonitor:
 """Monitoring производительности"""

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

 def monitor_training(self, predictor, data: pd.dataFrame):
 """Monitoring обучения"""
 start_time = time.time()

 # Начальные метрики
 initial_metrics = self.get_system_metrics()
 self.metrics_history.append(initial_metrics)

 # Обучение with Monitoringом
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
performance_Analysis = monitor.analyze_performance()
print(f"Performance Analysis: {performance_Analysis}")
```

## Обработка ошибок

### 1. Обработка исключений

```python
def safe_training(predictor, data: pd.dataFrame, **kwargs) -> Dict[str, Any]:
 """Безопасное обучение with обработкой ошибок"""

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
 'suggestion': 'check data quality and parameters'
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
def resilient_training(predictor, data: pd.dataFrame,
 fallback_strategies: List[Dict[str, Any]]) -> Dict[str, Any]:
 """Устойчивое обучение with fallback стратегиями"""

 for i, strategy in enumerate(fallback_strategies):
 try:
 # Попытка обучения with текущей стратегией
 predictor.fit(data, **strategy)

 # Валидация
 if validate_model(predictor):
 return {
 'status': 'success',
 'strategy_Used': i,
 'strategy_config': strategy
 }
 else:
 continue

 except Exception as e:
 print(f"Strategy {i} failed: {str(e)}")
 continue

 return {
 'status': 'error',
 'error': 'all strategies failed',
 'suggestions': [
 'check data quality',
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

## Оптимизация for продакшена

### 1. Сжатие модели

```python
def optimize_for_production(predictor, target_size_mb: int = 100) -> Dict[str, Any]:
 """Оптимизация модели for продакшена"""

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

 # check размера
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

### 2. Кэширование predictions

```python
import hashlib
import json
from typing import Optional

class Predictioncache:
 """
 Система кэширования predictions for acceleration инференса

 Parameters:
 -----------
 cache_size : int, default=1000
 Максимальный размер cache (количество predictions):
 - 100-500: Маленький кэш for простых систем
 - 500-1000: Стандартный кэш for большинства задач
 - 1000-5000: Большой кэш for высоконагруженных систем
 - 5000+: Очень большой кэш for экстремальных нагрузок

 Attributes:
 -----------
 cache : Dict[str, Any]
 Словарь кэшированных predictions
 Ключ: MD5 хеш входных данных
 Значение: Результат предсказания

 access_count : Dict[str, int]
 Счетчик обращений к каждому элементу cache
 Используется for LRU (Least Recently Used) политики

 cache_size : int
 Максимальный размер cache

 Notes:
 ------
 Стратегия кэширования:
 - LRU (Least Recently Used): remove наименее Useых элементов
 - MD5 хеширование: Быстрое сравнение входных данных
 - Автоматическое Management размером: Предотвращение переполнения памяти
 - Статистика использования: Monitoring эффективности cache
 """

 def __init__(self, cache_size: int = 1000):
 self.cache_size = cache_size
 self.cache = {}
 self.access_count = {}

 def _generate_cache_key(self, data: Dict) -> str:
 """
 Генерация уникального ключа cache on basis входных данных

 Parameters:
 -----------
 data : Dict
 Входные data for предсказания

 Returns:
 --------
 str
 MD5 хеш входных данных, Useый как ключ cache

 Notes:
 ------
 Алгоритм генерации ключа:
 1. Сериализация данных in JSON with сортировкой ключей
 2. Кодирование in UTF-8
 3. Вычисление MD5 хеша
 4. Возврат шестнадцатеричного представления

 Преимущества MD5:
 - Быстрое вычисление
 - Фиксированная длина (32 symbol)
 - Низкая вероятность коллизий
 - Детерминистичность (одинаковые data = одинаковый хеш)
 """
 data_str = json.dumps(data, sort_keys=True)
 return hashlib.md5(data_str.encode()).hexdigest()

 def get_Prediction(self, data: Dict) -> Optional[Any]:
 """
 Получение предсказания из cache

 Parameters:
 -----------
 data : Dict
 Входные data for поиска in кэше

 Returns:
 --------
 Optional[Any]
 Кэшированное Prediction or None если not foundо

 Notes:
 ------
 Алгоритм поиска:
 1. Генерация ключа cache из входных данных
 2. Поиск ключа in словаре cache
 3. update счетчика обращений (LRU)
 4. Возврат результата or None
 """
 cache_key = self._generate_cache_key(data)

 if cache_key in self.cache:
 # update счетчика доступа for LRU политики
 self.access_count[cache_key] = self.access_count.get(cache_key, 0) + 1
 return self.cache[cache_key]

 return None

 def set_Prediction(self, data: Dict, Prediction: Any):
 """
 Сохранение предсказания in кэш

 Parameters:
 -----------
 data : Dict
 Входные data for кэширования

 Prediction : Any
 Результат предсказания for сохранения

 Notes:
 ------
 Алгоритм сохранения:
 1. Генерация ключа cache из входных данных
 2. check размера cache
 3. remove наименее Useого элемента (LRU) если нужно
 4. Сохранение нового предсказания
 5. Инициализация счетчика обращений
 """
 cache_key = self._generate_cache_key(data)

 # check размера cache
 if len(self.cache) >= self.cache_size:
 # remove наименее Useого элемента (LRU)
 least_Used_key = min(self.access_count.keys(), key=self.access_count.get)
 del self.cache[least_Used_key]
 del self.access_count[least_Used_key]

 # add нового элемента
 self.cache[cache_key] = Prediction
 self.access_count[cache_key] = 1

 def get_cache_stats(self) -> Dict[str, Any]:
 """
 Получение статистики использования cache

 Returns:
 --------
 Dict[str, Any]
 Словарь со статистикой cache:
 - cache_size: int - текущий размер cache
 - max_cache_size: int - максимальный размер cache
 - hit_rate: float - коэффициент попаданий (0.0-1.0)
 - most_accessed: tuple - наиболее Useый элемент
 - total_accesses: int - общее количество обращений
 - memory_usage: float - примерное использование памяти in MB

 Notes:
 ------
 Метрики эффективности cache:
 - hit_rate: Доля запросов, которые были foundы in кэше
 - most_accessed: Самый популярный элемент cache
 - memory_usage: Оценка использования памяти
 """
 return {
 'cache_size': len(self.cache),
 'max_cache_size': self.cache_size,
 'hit_rate': self.calculate_hit_rate(),
 'most_accessed': max(self.access_count.items(), key=lambda x: x[1]) if self.access_count else None,
 'total_accesses': sum(self.access_count.values()) if self.access_count else 0,
 'memory_usage': self.estimate_memory_usage()
 }

 def calculate_hit_rate(self) -> float:
 """
 Расчет коэффициента попаданий cache (hit rate)

 Returns:
 --------
 float
 Коэффициент попаданий (0.0-1.0):
 - 0.0: Нет попаданий (кэш неэффективен)
 - 0.5: 50% попаданий (умеренная эффективность)
 - 0.8: 80% попаданий (хорошая эффективность)
 - 0.9+: 90%+ попаданий (отличная эффективность)

 Notes:
 ------
 Формула расчета:
 hit_rate = количество_попаданий / общее_количество_обращений

 Где:
 - количество_попаданий = размер_cache
 - общее_количество_обращений = сумма_all_счетчиков_обращений
 """
 if not self.access_count:
 return 0.0

 total_accesses = sum(self.access_count.values())
 cache_hits = len(self.cache)
 return cache_hits / total_accesses if total_accesses > 0 else 0.0

 def estimate_memory_usage(self) -> float:
 """
 Оценка использования памяти кэшем

 Returns:
 --------
 float
 Примерное использование памяти in MB

 Notes:
 ------
 Оценка основана on:
 - Размере словаря cache
 - Среднем размере предсказания (приблизительно 1KB)
 - Накладных расходах on ключи and счетчики
 """
 # Примерная оценка: 1KB on Prediction + накладные расходы
 estimated_size_per_item = 1024 # 1KB
 total_items = len(self.cache)
 return (total_items * estimated_size_per_item) / (1024 * 1024) # MB

# Использование
cache = Predictioncache(cache_size=1000)

def cached_predict(predictor, data: Dict) -> Any:
 """Кэшированное Prediction"""
 # check cache
 cached_Prediction = cache.get_Prediction(data)
 if cached_Prediction is not None:
 return cached_Prediction

 # Выполнение предсказания
 Prediction = predictor.predict(pd.dataFrame([data]))

 # Сохранение in кэш
 cache.set_Prediction(data, Prediction)

 return Prediction
```

## Этика and безопасность

<img src="images/optimized/metrics_comparison.png" alt="Этика and безопасность" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 7: Лучшие практики этики and безопасности in ML*

**Почему критически важны этика and безопасность in ML?** Потому что неправильные решения могут нанести серьезный вред:

- **Справедливость**: Предотвращение дискриминации and предвзятости
- **Прозрачность**: Объяснимость решений модели
- **Конфиденциальность**: Защита персональных данных
- **Безопасность**: Защита from атак and злоупотреблений
- **Ответственность**: Четкое определение ответственности за решения
- **Регулирование**: Соблюдение правовых требований

### 🎯 Ключевые принципы этичного ML

**Почему следуют этическим принципам?** Потому что это основа доверия and долгосрочного успеха:

- **Принцип "Справедливости"**: Равное отношение ко all группам
- **Принцип "Прозрачности"**: Понятность решений for пользователей
- **Принцип "Конфиденциальности"**: Защита личных данных
- **Принцип "Безопасности"**: Защита from злонамеренного использования
- **Принцип "Ответственности"**: Четкое определение ответственности
- **Принцип "Человечности"**: Уважение к правам and достоинству людей

## Следующие шаги

После освоения лучших практик переходите к:
- [Примерам использования](./09_examples.md)
- [Troubleshooting](./10_Troubleshooting.md)
