# Лучшие практики AutoML Gluon

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему лучшие практики критически важны

**Почему 95% ML-проектов терпят неудачу из-за игнорирования лучших практик?** Потому что машинное обучение - это не просто "обучить модель", а комплексная дисциплина, требующая соблюдения множества правил и принципов.

### Катастрофические последствия плохих практик
- **Amazon AI-рекрутинг**: Дискриминация из-за отсутствия разнообразия в данных
- **Microsoft Tay**: Расистские твиты из-за отсутствия модерации
- **Uber самоуправляемые авто**: Смерть пешехода из-за недостаточного тестирования
- **Facebook алгоритм**: Поляризация общества из-за неправильной оптимизации

### Преимущества следования лучшим практикам
- **Надежность**: Система работает стабильно в любых условиях
- **Масштабируемость**: Легко адаптируется к росту нагрузки
- **Поддерживаемость**: Команда может легко развивать систему
- **Этичность**: Система работает справедливо и безопасно

## Введение в лучшие практики

<img src="images/optimized/performance_comparison.png" alt="Сравнение производительности" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 1: Сравнение производительности различных моделей*

<img src="images/optimized/robustness_analysis.png" alt="Анализ робастности" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 2: Анализ робастности - робастные vs переобученные системы, стабильность производительности*

**Почему лучшие практики - это не просто "сделать хорошо"?** Это систематический подход к решению типичных проблем, основанный на опыте тысяч проектов. Это как медицинские протоколы - они спасают жизни.

**Почему 80% ML-проектов повторяют одни и те же ошибки?** Потому что команды не знают о существовании проверенных решений:
- **Проблемы с данными**: Неправильная подготовка, утечки, смещения
- **Проблемы с валидацией**: Неправильное разделение, переобучение
- **Проблемы с продакшеном**: Неготовность к реальным условиям
- **Проблемы с этикой**: Дискриминация, предвзятость, безопасность

Лучшие практики - это накопленный опыт использования AutoML Gluon, который поможет избежать типичных ошибок и достичь максимальной эффективности. В этом разделе рассмотрим все аспекты правильного использования инструмента.

## Подготовка данных

<img src="images/optimized/advanced_topics_overview.png" alt="Подготовка данных" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 3: Лучшие практики подготовки данных для ML*

**Почему критически важна правильная подготовка данных?** Потому что качество данных напрямую влияет на качество модели:

- **Очистка данных**: Удаление шума, исправление ошибок
- **Обработка пропусков**: Стратегии заполнения отсутствующих значений
- **Нормализация**: Приведение данных к единому масштабу
- **Feature Engineering**: Создание новых признаков
- **Валидация данных**: Проверка качества и консистентности
- **Документирование**: Фиксация всех преобразований

### 1. Качество данных

**Почему "мусор на входе = мусор на выходе" особенно актуально для ML?** Потому что модель учится на данных, и если данные плохие, модель будет делать плохие предсказания. Это как обучение врача на неправильных диагнозах.

**Почему 60% времени ML-проекта тратится на подготовку данных?** Потому что реальные данные всегда "грязные":
- **Отсутствующие значения**: 30-50% данных могут быть пустыми
- **Некорректные значения**: Опечатки, неправильные форматы
- **Дубликаты**: Одинаковые записи в разных форматах
- **Выбросы**: Экстремальные значения, которые искажают модель

**Типы проблем с данными:**
- **Структурные проблемы**: Неправильные типы данных, форматы
- **Семантические проблемы**: Некорректные значения, логические ошибки
- **Статистические проблемы**: Смещения, корреляции, выбросы
- **Этические проблемы**: Дискриминация, предвзятость

```python
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import matplotlib.pyplot as plt
import seaborn as sns

def data_quality_check(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Комплексная проверка качества данных - первый шаг к успешному ML
    
    Parameters:
    -----------
    data : pd.DataFrame
        Датафрейм для проверки качества данных. Должен содержать:
        - Числовые и категориальные колонки
        - Целевую переменную (если есть)
        - Временные метки (для временных рядов)
        
    Returns:
    --------
    Dict[str, Any]
        Словарь с результатами проверки качества:
        - shape: tuple - размер датасета (строки, колонки)
        - missing_values: dict - количество пропущенных значений по колонкам
        - missing_percent: dict - процент пропущенных значений по колонкам
        - data_types: dict - типы данных по колонкам
        - duplicates: int - количество дублированных строк
        - outliers: dict - количество выбросов по числовым колонкам
        - correlations: dict - матрица корреляций между числовыми колонками
        
    Notes:
    ------
    Функция использует следующие методы детекции выбросов:
    - IQR (Interquartile Range): Q1 - 1.5*IQR до Q3 + 1.5*IQR
    - Корреляции рассчитываются только для числовых колонок
    - Дубликаты определяются по полному совпадению всех значений
    """
    
    quality_report = {
        'shape': data.shape,                    # Размер датасета (строки, колонки)
        'missing_values': data.isnull().sum().to_dict(),  # Пропущенные значения по колонкам
        'data_types': data.dtypes.to_dict(),   # Типы данных по колонкам
        'duplicates': data.duplicated().sum(),  # Количество дублированных строк
        'outliers': {},                         # Выбросы по числовым колонкам
        'correlations': {}                      # Корреляции между числовыми колонками
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
    """
    Обработка пропущенных значений в датасете
    
    Parameters:
    -----------
    data : pd.DataFrame
        Датафрейм с пропущенными значениями для обработки
        
    strategy : str, default='auto'
        Стратегия обработки пропущенных значений:
        - 'auto': Автоматический выбор стратегии по типу данных
          * Для категориальных (object) - мода (наиболее частое значение)
          * Для числовых - медиана (устойчива к выбросам)
        - 'drop': Удаление всех строк с пропущенными значениями
          * Используется когда пропусков мало (< 5%)
          * Может значительно уменьшить размер датасета
        - 'interpolate': Линейная интерполяция для временных рядов
          * Подходит для временных данных с трендом
          * Сохраняет временную структуру данных
        - 'mean': Заполнение средним значением (только для числовых)
        - 'mode': Заполнение модой (наиболее частым значением)
        - 'forward_fill': Заполнение предыдущим значением
        - 'backward_fill': Заполнение следующим значением
        
    Returns:
    --------
    pd.DataFrame
        Датафрейм с обработанными пропущенными значениями
        
    Notes:
    ------
    Рекомендации по выбору стратегии:
    - auto: Универсальная стратегия для большинства случаев
    - drop: Когда пропусков мало и данные критически важны
    - interpolate: Для временных рядов с трендом
    - mean/mode: Когда нужно сохранить статистические свойства
    """
    
    if strategy == 'auto':
        # Автоматическая стратегия - выбор по типу данных
        for col in data.columns:
            if data[col].dtype == 'object':
                # Для категориальных переменных - мода (наиболее частое значение)
                # Если мода пустая, используем 'Unknown'
                data[col].fillna(data[col].mode()[0] if not data[col].mode().empty else 'Unknown', inplace=True)
            else:
                # Для числовых переменных - медиана (устойчива к выбросам)
                data[col].fillna(data[col].median(), inplace=True)
    
    elif strategy == 'drop':
        # Удаление строк с пропущенными значениями
        # Используется когда пропусков мало (< 5%)
        data = data.dropna()
    
    elif strategy == 'interpolate':
        # Интерполяция для временных рядов
        # Сохраняет временную структуру данных
        data = data.interpolate(method='linear')
    
    elif strategy == 'mean':
        # Заполнение средним значением (только для числовых)
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
train_data_clean = handle_missing_values(train_data, strategy='auto')
```

### 3. Обработка выбросов

```python
def handle_outliers(data: pd.DataFrame, method: str = 'iqr') -> pd.DataFrame:
    """
    Обработка выбросов в числовых данных
    
    Parameters:
    -----------
    data : pd.DataFrame
        Датафрейм с числовыми данными для обработки выбросов
        
    method : str, default='iqr'
        Метод обработки выбросов:
        - 'iqr': Межквартильный размах (IQR)
          * Выбросы: значения < Q1 - 1.5*IQR или > Q3 + 1.5*IQR
          * Заменяются на граничные значения (capping)
          * Умеренно консервативный подход
        - 'zscore': Z-скор метод
          * Выбросы: |z-score| > 3 (стандартное отклонение)
          * Полностью удаляются из датасета
          * Агрессивный подход, может потерять важную информацию
        - 'winsorize': Винзоризация (ограничение)
          * Заменяет 5% самых низких и 5% самых высоких значений
          * Сохраняет размер датасета
          * Консервативный подход
        - 'isolation_forest': Изоляционный лес
          * Использует ML для детекции аномалий
          * Более сложный, но точный метод
        - 'local_outlier_factor': LOF метод
          * Учитывает локальную плотность данных
          * Хорош для кластерных данных
        
    Returns:
    --------
    pd.DataFrame
        Датафрейм с обработанными выбросами
        
    Notes:
    ------
    Рекомендации по выбору метода:
    - iqr: Универсальный метод для большинства случаев
    - zscore: Когда выбросы явно ошибочные
    - winsorize: Когда нужно сохранить все данные
    - isolation_forest: Для сложных паттернов выбросов
    - local_outlier_factor: Для данных с кластерами
    """
    
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    
    if method == 'iqr':
        # Метод межквартильного размаха (IQR)
        # Q1 = 25-й процентиль, Q3 = 75-й процентиль
        for col in numeric_columns:
            Q1 = data[col].quantile(0.25)  # Первый квартиль
            Q3 = data[col].quantile(0.75)  # Третий квартиль
            IQR = Q3 - Q1  # Межквартильный размах
            lower_bound = Q1 - 1.5 * IQR  # Нижняя граница
            upper_bound = Q3 + 1.5 * IQR  # Верхняя граница
            
            # Замена выбросов на граничные значения (capping)
            data[col] = np.where(data[col] < lower_bound, lower_bound, data[col])
            data[col] = np.where(data[col] > upper_bound, upper_bound, data[col])
    
    elif method == 'zscore':
        # Метод Z-скор (стандартизированные отклонения)
        # Z-score = (значение - среднее) / стандартное_отклонение
        for col in numeric_columns:
            z_scores = np.abs((data[col] - data[col].mean()) / data[col].std())
            # Удаление строк с |z-score| > 3 (агрессивный подход)
            data = data[z_scores < 3]
    
    elif method == 'winsorize':
        # Винзоризация - ограничение экстремальных значений
        # Заменяет 5% самых низких и 5% самых высоких значений
        for col in numeric_columns:
            lower_percentile = data[col].quantile(0.05)  # 5-й процентиль
            upper_percentile = data[col].quantile(0.95)  # 95-й процентиль
            # Замена экстремальных значений на процентили
            data[col] = np.where(data[col] < lower_percentile, lower_percentile, data[col])
            data[col] = np.where(data[col] > upper_percentile, upper_percentile, data[col])
    
    elif method == 'isolation_forest':
        # Изоляционный лес - ML метод для детекции аномалий
        from sklearn.ensemble import IsolationForest
        for col in numeric_columns:
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            outlier_mask = iso_forest.fit_predict(data[[col]]) == -1
            # Замена выбросов на медиану
            data.loc[outlier_mask, col] = data[col].median()
    
    elif method == 'local_outlier_factor':
        # Local Outlier Factor - учитывает локальную плотность
        from sklearn.neighbors import LocalOutlierFactor
        for col in numeric_columns:
            lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
            outlier_mask = lof.fit_predict(data[[col]]) == -1
            # Замена выбросов на медиану
            data.loc[outlier_mask, col] = data[col].median()
    
    return data

# Использование
train_data_no_outliers = handle_outliers(train_data, method='iqr')
```

## Выбор метрик

### 1. Метрики для классификации

```python
def select_classification_metrics(problem_type: str, data_balance: str = 'balanced') -> List[str]:
    """
    Выбор оптимальных метрик для задач классификации
    
    Parameters:
    -----------
    problem_type : str
        Тип задачи классификации:
        - 'binary': Бинарная классификация (2 класса)
        - 'multiclass': Многоклассовая классификация (3+ классов)
        - 'multilabel': Многометочная классификация (несколько меток одновременно)
        
    data_balance : str, default='balanced'
        Баланс классов в данных:
        - 'balanced': Сбалансированные классы (примерно равное количество)
        - 'imbalanced': Несбалансированные классы (один класс значительно больше)
        - 'highly_imbalanced': Сильно несбалансированные классы (соотношение 1:100+)
        
    Returns:
    --------
    List[str]
        Список рекомендуемых метрик для оценки модели:
        
        Для бинарной классификации:
        - accuracy: Общая точность (правильные предсказания / все предсказания)
        - f1: F1-мера (гармоническое среднее precision и recall)
        - roc_auc: Площадь под ROC-кривой (качество разделения классов)
        - precision: Точность (правильные положительные / все положительные)
        - recall: Полнота (правильные положительные / все реальные положительные)
        - balanced_accuracy: Сбалансированная точность (устойчива к дисбалансу)
        
        Для многоклассовой классификации:
        - f1_macro: F1-мера с макро-усреднением (среднее по классам)
        - f1_micro: F1-мера с микро-усреднением (глобальные TP, FP, FN)
        - precision_macro/recall_macro: Макро-усредненные precision и recall
        
    Notes:
    ------
    Рекомендации по выбору метрик:
    - Сбалансированные данные: accuracy, f1, roc_auc
    - Несбалансированные данные: f1, roc_auc, balanced_accuracy
    - Критически важные случаи: precision (ложные срабатывания дороги)
    - Пропуск важных случаев недопустим: recall (ложные пропуски дороги)
    """
    
    if problem_type == 'binary':
        if data_balance == 'balanced':
            # Сбалансированные данные - стандартные метрики
            return ['accuracy', 'f1', 'roc_auc', 'precision', 'recall']
        elif data_balance == 'imbalanced':
            # Несбалансированные данные - метрики устойчивые к дисбалансу
            return ['f1', 'roc_auc', 'precision', 'recall', 'balanced_accuracy']
        else:
            # Универсальный набор для бинарной классификации
            return ['accuracy', 'f1', 'roc_auc']
    
    elif problem_type == 'multiclass':
        if data_balance == 'balanced':
            # Сбалансированные многоклассовые данные
            return ['accuracy', 'f1_macro', 'f1_micro', 'precision_macro', 'recall_macro']
        elif data_balance == 'imbalanced':
            # Несбалансированные многоклассовые данные
            return ['f1_macro', 'f1_micro', 'balanced_accuracy', 'precision_macro', 'recall_macro']
        else:
            # Универсальный набор для многоклассовой классификации
            return ['accuracy', 'f1_macro', 'f1_micro']
    
    else:
        # Fallback для неизвестных типов задач
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
    """
    Выбор оптимальных метрик для задач регрессии
    
    Parameters:
    -----------
    problem_type : str
        Тип задачи регрессии (в данном контексте всегда 'regression')
        
    target_distribution : str, default='normal'
        Распределение целевой переменной:
        - 'normal': Нормальное распределение (симметричное, без выбросов)
        - 'skewed': Асимметричное распределение (логарифмическое, экспоненциальное)
        - 'outliers': Распределение с выбросами (экстремальные значения)
        - 'multimodal': Многомодальное распределение (несколько пиков)
        - 'uniform': Равномерное распределение
        
    Returns:
    --------
    List[str]
        Список рекомендуемых метрик для оценки регрессионной модели:
        
        Основные метрики:
        - rmse: Root Mean Square Error (корень из среднеквадратичной ошибки)
          * Чувствительна к выбросам, в тех же единицах что и целевая переменная
          * Штрафует большие ошибки сильнее малых
        - mae: Mean Absolute Error (средняя абсолютная ошибка)
          * Устойчива к выбросам, простая для интерпретации
          * Все ошибки имеют одинаковый вес
        - r2: Коэффициент детерминации (R-squared)
          * Доля объясненной дисперсии (0-1, чем больше тем лучше)
          * Показывает качество модели относительно среднего значения
        
        Специализированные метрики:
        - mape: Mean Absolute Percentage Error (средняя абсолютная процентная ошибка)
          * Выражается в процентах, легко интерпретируется
          * Проблемы при делении на ноль и очень малых значениях
        - smape: Symmetric Mean Absolute Percentage Error
          * Симметричная версия MAPE, более стабильная
        - huber_loss: Функция потерь Хубера
          * Комбинация MAE и MSE, устойчива к выбросам
        - mape_log: MAPE на логарифмической шкале
          * Для мультипликативных ошибок
        
    Notes:
    ------
    Рекомендации по выбору метрик:
    - Нормальное распределение: rmse, mae, r2 (стандартный набор)
    - Асимметричное распределение: mae, mape, smape (процентные метрики)
    - Данные с выбросами: mae, huber_loss (устойчивые метрики)
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
        # Распределение с выбросами - устойчивые метрики
        return ['mae', 'huber_loss']
    elif target_distribution == 'multimodal':
        # Многомодальное распределение - базовые метрики
        return ['mae', 'r2', 'rmse']
    elif target_distribution == 'uniform':
        # Равномерное распределение - стандартные метрики
        return ['rmse', 'mae', 'r2']
    else:
        # Fallback для неизвестных типов распределения
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
    """
    Создание стратегии поиска гиперпараметров на основе размера данных
    
    Parameters:
    -----------
    data_size : int
        Размер обучающего датасета (количество строк):
        - < 1000: Маленький датасет - простые модели, быстрая конвергенция
        - 1000-10000: Средний датасет - умеренная сложность, баланс качества и скорости
        - > 10000: Большой датасет - сложные модели, высокое качество
        
    problem_type : str
        Тип задачи машинного обучения:
        - 'binary': Бинарная классификация
        - 'multiclass': Многоклассовая классификация
        - 'regression': Регрессия
        - 'multilabel': Многометочная классификация
        
    Returns:
    --------
    Dict[str, Any]
        Словарь с конфигурациями гиперпараметров для разных алгоритмов:
        
        GBM (Gradient Boosting Machine):
        - num_boost_round: Количество итераций бустинга (100-1000)
        - learning_rate: Скорость обучения (0.01-0.3)
        - max_depth: Максимальная глубина деревьев (3-12)
        - subsample: Доля образцов для каждой итерации (0.5-1.0)
        - colsample_bytree: Доля признаков для каждого дерева (0.5-1.0)
        
        RF (Random Forest):
        - n_estimators: Количество деревьев (100-1000)
        - max_depth: Максимальная глубина деревьев (5-25)
        - min_samples_split: Минимум образцов для разделения узла (2-20)
        - min_samples_leaf: Минимум образцов в листе (1-10)
        - max_features: Количество признаков для разделения ('sqrt', 'log2', None)
        
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
        - border_count: Количество границ для числовых признаков (32-255)
        
    Notes:
    ------
    Стратегия выбора гиперпараметров:
    - Маленькие датасеты: Простые модели, быстрая конвергенция, избегание переобучения
    - Средние датасеты: Баланс между качеством и скоростью, умеренная сложность
    - Большие датасеты: Сложные модели, высокое качество, использование всех данных
    """
    
    if data_size < 1000:
        # Маленький датасет - простые модели, быстрая конвергенция
        # Избегаем переобучения, используем простые конфигурации
        return {
            'GBM': [{'num_boost_round': 100, 'learning_rate': 0.1, 'max_depth': 3}],
            'RF': [{'n_estimators': 100, 'max_depth': 10, 'min_samples_split': 5}],
            'XGB': [{'n_estimators': 100, 'max_depth': 6, 'learning_rate': 0.1}]
        }
    
    elif data_size < 10000:
        # Средний датасет - умеренная сложность, баланс качества и скорости
        # Используем несколько конфигураций для поиска оптимальной
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
        # Используем все доступные алгоритмы с оптимальными параметрами
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
    Оптимизация времени обучения на основе размера данных и доступного времени
    
    Parameters:
    -----------
    data_size : int
        Размер обучающего датасета (количество строк):
        - < 1000: Маленький датасет - быстрое обучение, простые модели
        - 1000-10000: Средний датасет - умеренное обучение, баланс качества и скорости
        - > 10000: Большой датасет - качественное обучение, сложные модели
        
    available_time : int
        Доступное время для обучения в секундах:
        - < 1800 (30 мин): Быстрое обучение, простые модели
        - 1800-7200 (30 мин - 2 часа): Умеренное обучение
        - > 7200 (2+ часа): Качественное обучение, сложные модели
        
    Returns:
    --------
    Dict[str, Any]
        Конфигурация для оптимизации времени обучения:
        
        time_limit : int
            Максимальное время обучения одной модели в секундах
            Рассчитывается как available_time / количество_моделей
            
        presets : str
            Предустановленные конфигурации AutoGluon:
            - 'optimize_for_deployment': Быстрое обучение, простые модели
              * Минимальное время, базовое качество
              * Подходит для прототипов и быстрых экспериментов
            - 'medium_quality': Умеренное качество, баланс времени и качества
              * Хорошее качество за разумное время
              * Подходит для большинства задач
            - 'high_quality': Высокое качество, длительное обучение
              * Максимальное качество, больше времени
              * Подходит для продакшена и критически важных задач
            - 'best_quality': Лучшее качество, очень длительное обучение
              * Максимальное качество, очень много времени
              * Подходит для исследований и конкурсов
              
        num_bag_folds : int
            Количество фолдов для бэггинга (3-10):
            - 3: Быстрое обучение, базовое качество
            - 5: Стандартное качество, умеренное время
            - 10: Высокое качество, длительное время
            
        num_bag_sets : int
            Количество наборов бэггинга (1-3):
            - 1: Стандартный бэггинг
            - 2: Двойной бэггинг для лучшего качества
            - 3: Тройной бэггинг для максимального качества
            
        num_stack_levels : int
            Количество уровней стекинга (0-2):
            - 0: Без стекинга (быстрое обучение)
            - 1: Один уровень стекинга (умеренное качество)
            - 2: Два уровня стекинга (высокое качество)
            
    Notes:
    ------
    Стратегия оптимизации времени:
    - Маленькие датасеты: Быстрое обучение, избегание переобучения
    - Средние датасеты: Баланс между качеством и временем
    - Большие датасеты: Качественное обучение, использование всех данных
    - Ограниченное время: Простые модели, быстрая конвергенция
    - Достаточно времени: Сложные модели, высокое качество
    """
    
    # Расчет времени на модель (10 моделей по умолчанию)
    # Можно настроить количество моделей в зависимости от доступного времени
    num_models = min(10, max(3, available_time // 300))  # 3-10 моделей, минимум 5 минут на модель
    time_per_model = available_time // num_models
    
    if data_size < 1000:
        # Быстрое обучение для маленьких датасетов
        # Избегаем переобучения, используем простые модели
        return {
            'time_limit': time_per_model,
            'presets': 'optimize_for_deployment',
            'num_bag_folds': 3,  # Минимальное количество фолдов
            'num_bag_sets': 1,   # Один набор бэггинга
            'num_stack_levels': 0  # Без стекинга
        }
    
    elif data_size < 10000:
        # Умеренное обучение для средних датасетов
        # Баланс между качеством и временем
        return {
            'time_limit': time_per_model,
            'presets': 'medium_quality',
            'num_bag_folds': 5,  # Стандартное количество фолдов
            'num_bag_sets': 1,   # Один набор бэггинга
            'num_stack_levels': 1  # Один уровень стекинга
        }
    
    else:
        # Качественное обучение для больших датасетов
        # Максимальное качество, использование всех данных
        return {
            'time_limit': time_per_model,
            'presets': 'high_quality',
            'num_bag_folds': 5,  # Стандартное количество фолдов
            'num_bag_sets': 2,   # Двойной бэггинг для лучшего качества
            'num_stack_levels': 2  # Два уровня стекинга
        }

# Использование
training_config = optimize_training_time(len(train_data), 3600)  # 1 час
predictor.fit(train_data, **training_config)
```

## Валидация и тестирование

<img src="images/optimized/validation_methods.png" alt="Валидация и тестирование" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 4: Лучшие практики валидации и тестирования ML-моделей*

**Почему критически важна правильная валидация?** Потому что неправильная валидация приводит к переобучению и нереалистичным оценкам:

- **Стратегии валидации**: Выбор подходящего метода для задачи
- **Разделение данных**: Правильное разделение на train/validation/test
- **Кросс-валидация**: Надежная оценка производительности
- **Временные ряды**: Специальные методы для временных данных
- **A/B тестирование**: Сравнение моделей в реальных условиях
- **Статистические тесты**: Проверка значимости различий

### 1. Стратегия валидации

```python
def select_validation_strategy(data_size: int, problem_type: str, 
                             data_type: str = 'tabular') -> Dict[str, Any]:
    """
    Выбор оптимальной стратегии валидации на основе характеристик данных
    
    Parameters:
    -----------
    data_size : int
        Размер обучающего датасета (количество строк):
        - < 1000: Маленький датасет - holdout валидация
        - 1000-10000: Средний датасет - k-fold валидация (5 фолдов)
        - > 10000: Большой датасет - k-fold валидация (10 фолдов)
        
    problem_type : str
        Тип задачи машинного обучения:
        - 'binary': Бинарная классификация
        - 'multiclass': Многоклассовая классификация
        - 'regression': Регрессия
        - 'multilabel': Многометочная классификация
        
    data_type : str, default='tabular'
        Тип данных:
        - 'tabular': Табличные данные (стандартная валидация)
        - 'time_series': Временные ряды (временная валидация)
        - 'image': Изображения (стратифицированная валидация)
        - 'text': Текстовые данные (случайная валидация)
        
    Returns:
    --------
    Dict[str, Any]
        Конфигурация стратегии валидации:
        
        validation_strategy : str
            Тип стратегии валидации:
            - 'holdout': Простое разделение на train/validation
              * Быстрое, подходит для больших датасетов
              * Может быть нестабильным для маленьких датасетов
            - 'kfold': K-fold кросс-валидация
              * Более стабильная оценка производительности
              * Подходит для средних и больших датасетов
            - 'time_series_split': Временная валидация
              * Сохраняет временную структуру данных
              * Подходит для временных рядов и прогнозирования
            - 'stratified_kfold': Стратифицированная валидация
              * Сохраняет пропорции классов в каждом фолде
              * Подходит для несбалансированных данных
              
        n_splits : int
            Количество фолдов для k-fold валидации (3-10):
            - 3: Быстрая валидация, базовое качество
            - 5: Стандартная валидация, хорошее качество
            - 10: Тщательная валидация, высокое качество
            
        test_size : float
            Доля данных для тестирования (0.1-0.3):
            - 0.1: 10% для тестирования (больше данных для обучения)
            - 0.2: 20% для тестирования (стандартное разделение)
            - 0.3: 30% для тестирования (больше данных для тестирования)
            
        holdout_frac : float
            Доля данных для holdout валидации (0.2-0.4):
            - 0.2: 20% для валидации (больше данных для обучения)
            - 0.3: 30% для валидации (стандартное разделение)
            - 0.4: 40% для валидации (больше данных для валидации)
            
        num_bag_folds : int
            Количество фолдов для бэггинга (3-10):
            - 3: Быстрое обучение, базовое качество
            - 5: Стандартное качество, умеренное время
            - 10: Высокое качество, длительное время
            
        num_bag_sets : int
            Количество наборов бэггинга (1-3):
            - 1: Стандартный бэггинг
            - 2: Двойной бэггинг для лучшего качества
            - 3: Тройной бэггинг для максимального качества
            
    Notes:
    ------
    Рекомендации по выбору стратегии валидации:
    - Временные ряды: time_series_split (сохранение временной структуры)
    - Маленькие датасеты: holdout (больше данных для обучения)
    - Средние датасеты: k-fold 5 (баланс стабильности и времени)
    - Большие датасеты: k-fold 10 (максимальная стабильность)
    - Несбалансированные данные: stratified_kfold (сохранение пропорций)
    """
    
    if data_type == 'time_series':
        # Временные ряды - специальная валидация
        # Сохраняем временную структуру данных
        return {
            'validation_strategy': 'time_series_split',
            'n_splits': 5,  # Стандартное количество фолдов
            'test_size': 0.2  # 20% для тестирования
        }
    
    elif data_size < 1000:
        # Маленький датасет - holdout валидация
        # Больше данных для обучения, простая валидация
        return {
            'validation_strategy': 'holdout',
            'holdout_frac': 0.3  # 30% для валидации
        }
    
    elif data_size < 10000:
        # Средний датасет - k-fold валидация
        # Баланс между стабильностью и временем
        return {
            'validation_strategy': 'kfold',
            'num_bag_folds': 5,  # 5 фолдов для стабильности
            'num_bag_sets': 1    # Один набор бэггинга
        }
    
    else:
        # Большой датасет - расширенная k-fold валидация
        # Максимальная стабильность оценки
        return {
            'validation_strategy': 'kfold',
            'num_bag_folds': 10,  # 10 фолдов для максимальной стабильности
            'num_bag_sets': 1     # Один набор бэггинга
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

<img src="images/optimized/metrics_detailed.png" alt="Оптимизация производительности" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 5: Лучшие практики оптимизации производительности ML-моделей*

**Почему важна оптимизация производительности?** Потому что медленные модели неэффективны в продакшене:

- **Настройка ресурсов**: Оптимальное использование CPU, памяти, GPU
- **Параллелизация**: Ускорение обучения и инференса
- **Кэширование**: Сохранение результатов для повторного использования
- **Профилирование**: Выявление узких мест в производительности
- **Мониторинг**: Отслеживание метрик производительности
- **Масштабирование**: Адаптация к росту нагрузки

### 1. Настройка ресурсов

```python
def optimize_resources(data_size: int, available_resources: Dict[str, int]) -> Dict[str, Any]:
    """
    Оптимизация использования системных ресурсов для обучения AutoGluon
    
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
        - 'memory': int - доступная память в GB (4-256)
        - 'gpus': int - количество доступных GPU (0-8)
        - 'disk': int - доступное место на диске в GB (100-10000)
        
    Returns:
    --------
    Dict[str, Any]
        Оптимизированная конфигурация ресурсов:
        
        num_cpus : int
            Количество CPU ядер для обучения (1-8):
            - 1-2: Маленькие датасеты, быстрые эксперименты
            - 3-4: Средние датасеты, стандартное обучение
            - 5-8: Большие датасеты, интенсивное обучение
            - >8: Очень большие датасеты, максимальная производительность
            
        num_gpus : int
            Количество GPU для обучения (0-8):
            - 0: CPU-only обучение (универсально)
            - 1: Один GPU для ускорения (рекомендуется)
            - 2-4: Множественные GPU для больших моделей
            - >4: Экстремально большие модели
            
        memory_limit : int
            Лимит памяти в GB (4-64):
            - 4-8: Маленькие датасеты, простые модели
            - 8-16: Средние датасеты, стандартные модели
            - 16-32: Большие датасеты, сложные модели
            - 32-64: Очень большие датасеты, максимальные модели
            
        disk_space : int
            Требуемое место на диске в GB (1-100):
            - 1-5: Простые модели, минимальное место
            - 5-20: Стандартные модели, умеренное место
            - 20-50: Сложные модели, много места
            - 50-100: Очень сложные модели, максимальное место
            
        parallel_folds : bool
            Параллельное выполнение фолдов:
            - True: Ускорение обучения, больше ресурсов
            - False: Последовательное выполнение, меньше ресурсов
            
        parallel_models : bool
            Параллельное обучение моделей:
            - True: Максимальное ускорение, много ресурсов
            - False: Последовательное обучение, меньше ресурсов
            
    Notes:
    ------
    Стратегия оптимизации ресурсов:
    - Маленькие датасеты: Минимальные ресурсы, избегание избыточности
    - Средние датасеты: Баланс между производительностью и ресурсами
    - Большие датасеты: Максимальное использование ресурсов
    - Ограниченные ресурсы: Последовательное выполнение, оптимизация памяти
    - Избыточные ресурсы: Параллельное выполнение, максимальная скорость
    """
    
    # Расчет оптимальных параметров на основе размера данных
    if data_size < 1000:
        # Маленький датасет - минимальные ресурсы
        # Избегаем избыточного использования ресурсов
        num_cpus = min(2, available_resources.get('cpus', 4))
        memory_limit = min(4, available_resources.get('memory', 8))
        parallel_folds = False  # Последовательное выполнение
        parallel_models = False  # Последовательное обучение
        disk_space = 5  # Минимальное место на диске
        
    elif data_size < 10000:
        # Средний датасет - умеренные ресурсы
        # Баланс между производительностью и ресурсами
        num_cpus = min(4, available_resources.get('cpus', 8))
        memory_limit = min(8, available_resources.get('memory', 16))
        parallel_folds = True   # Параллельные фолды
        parallel_models = False  # Последовательные модели
        disk_space = 20  # Умеренное место на диске
        
    else:
        # Большой датасет - максимальные ресурсы
        # Используем все доступные ресурсы
        num_cpus = min(8, available_resources.get('cpus', 16))
        memory_limit = min(16, available_resources.get('memory', 32))
        parallel_folds = True   # Параллельные фолды
        parallel_models = True  # Параллельные модели
        disk_space = 50  # Много места на диске
    
    # Дополнительная оптимизация на основе доступных ресурсов
    if available_resources.get('cpus', 0) < 4:
        # Ограниченные CPU - отключаем параллелизм
        parallel_folds = False
        parallel_models = False
    elif available_resources.get('memory', 0) < 8:
        # Ограниченная память - уменьшаем лимиты
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

<img src="images/optimized/production_architecture.png" alt="Мониторинг и логирование" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 6: Лучшие практики мониторинга и логирования ML-систем*

**Почему критически важен мониторинг ML-систем?** Потому что модели могут деградировать и работать некорректно:

- **Система логирования**: Детальная фиксация всех событий
- **Мониторинг качества**: Отслеживание метрик производительности
- **Детекция дрейфа**: Обнаружение изменений в данных
- **Алертинг**: Уведомления о проблемах в реальном времени
- **Дашборды**: Визуализация состояния системы
- **Анализ логов**: Поиск причин проблем и оптимизация

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
    """
    Система кэширования предсказаний для ускорения инференса
    
    Parameters:
    -----------
    cache_size : int, default=1000
        Максимальный размер кэша (количество предсказаний):
        - 100-500: Маленький кэш для простых систем
        - 500-1000: Стандартный кэш для большинства задач
        - 1000-5000: Большой кэш для высоконагруженных систем
        - 5000+: Очень большой кэш для экстремальных нагрузок
        
    Attributes:
    -----------
    cache : Dict[str, Any]
        Словарь кэшированных предсказаний
        Ключ: MD5 хеш входных данных
        Значение: Результат предсказания
        
    access_count : Dict[str, int]
        Счетчик обращений к каждому элементу кэша
        Используется для LRU (Least Recently Used) политики
        
    cache_size : int
        Максимальный размер кэша
        
    Notes:
    ------
    Стратегия кэширования:
    - LRU (Least Recently Used): Удаление наименее используемых элементов
    - MD5 хеширование: Быстрое сравнение входных данных
    - Автоматическое управление размером: Предотвращение переполнения памяти
    - Статистика использования: Мониторинг эффективности кэша
    """
    
    def __init__(self, cache_size: int = 1000):
        self.cache_size = cache_size
        self.cache = {}
        self.access_count = {}
    
    def _generate_cache_key(self, data: Dict) -> str:
        """
        Генерация уникального ключа кэша на основе входных данных
        
        Parameters:
        -----------
        data : Dict
            Входные данные для предсказания
            
        Returns:
        --------
        str
            MD5 хеш входных данных, используемый как ключ кэша
            
        Notes:
        ------
        Алгоритм генерации ключа:
        1. Сериализация данных в JSON с сортировкой ключей
        2. Кодирование в UTF-8
        3. Вычисление MD5 хеша
        4. Возврат шестнадцатеричного представления
        
        Преимущества MD5:
        - Быстрое вычисление
        - Фиксированная длина (32 символа)
        - Низкая вероятность коллизий
        - Детерминистичность (одинаковые данные = одинаковый хеш)
        """
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def get_prediction(self, data: Dict) -> Optional[Any]:
        """
        Получение предсказания из кэша
        
        Parameters:
        -----------
        data : Dict
            Входные данные для поиска в кэше
            
        Returns:
        --------
        Optional[Any]
            Кэшированное предсказание или None если не найдено
            
        Notes:
        ------
        Алгоритм поиска:
        1. Генерация ключа кэша из входных данных
        2. Поиск ключа в словаре кэша
        3. Обновление счетчика обращений (LRU)
        4. Возврат результата или None
        """
        cache_key = self._generate_cache_key(data)
        
        if cache_key in self.cache:
            # Обновление счетчика доступа для LRU политики
            self.access_count[cache_key] = self.access_count.get(cache_key, 0) + 1
            return self.cache[cache_key]
        
        return None
    
    def set_prediction(self, data: Dict, prediction: Any):
        """
        Сохранение предсказания в кэш
        
        Parameters:
        -----------
        data : Dict
            Входные данные для кэширования
            
        prediction : Any
            Результат предсказания для сохранения
            
        Notes:
        ------
        Алгоритм сохранения:
        1. Генерация ключа кэша из входных данных
        2. Проверка размера кэша
        3. Удаление наименее используемого элемента (LRU) если нужно
        4. Сохранение нового предсказания
        5. Инициализация счетчика обращений
        """
        cache_key = self._generate_cache_key(data)
        
        # Проверка размера кэша
        if len(self.cache) >= self.cache_size:
            # Удаление наименее используемого элемента (LRU)
            least_used_key = min(self.access_count.keys(), key=self.access_count.get)
            del self.cache[least_used_key]
            del self.access_count[least_used_key]
        
        # Добавление нового элемента
        self.cache[cache_key] = prediction
        self.access_count[cache_key] = 1
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Получение статистики использования кэша
        
        Returns:
        --------
        Dict[str, Any]
            Словарь со статистикой кэша:
            - cache_size: int - текущий размер кэша
            - max_cache_size: int - максимальный размер кэша
            - hit_rate: float - коэффициент попаданий (0.0-1.0)
            - most_accessed: tuple - наиболее используемый элемент
            - total_accesses: int - общее количество обращений
            - memory_usage: float - примерное использование памяти в MB
            
        Notes:
        ------
        Метрики эффективности кэша:
        - hit_rate: Доля запросов, которые были найдены в кэше
        - most_accessed: Самый популярный элемент кэша
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
        Расчет коэффициента попаданий кэша (hit rate)
        
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
        - количество_попаданий = размер_кэша
        - общее_количество_обращений = сумма_всех_счетчиков_обращений
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
            Примерное использование памяти в MB
            
        Notes:
        ------
        Оценка основана на:
        - Размере словаря кэша
        - Среднем размере предсказания (приблизительно 1KB)
        - Накладных расходах на ключи и счетчики
        """
        # Примерная оценка: 1KB на предсказание + накладные расходы
        estimated_size_per_item = 1024  # 1KB
        total_items = len(self.cache)
        return (total_items * estimated_size_per_item) / (1024 * 1024)  # MB

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

## Этика и безопасность

<img src="images/optimized/metrics_comparison.png" alt="Этика и безопасность" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 7: Лучшие практики этики и безопасности в ML*

**Почему критически важны этика и безопасность в ML?** Потому что неправильные решения могут нанести серьезный вред:

- **Справедливость**: Предотвращение дискриминации и предвзятости
- **Прозрачность**: Объяснимость решений модели
- **Конфиденциальность**: Защита персональных данных
- **Безопасность**: Защита от атак и злоупотреблений
- **Ответственность**: Четкое определение ответственности за решения
- **Регулирование**: Соблюдение правовых требований

### 🎯 Ключевые принципы этичного ML

**Почему следуют этическим принципам?** Потому что это основа доверия и долгосрочного успеха:

- **Принцип "Справедливости"**: Равное отношение ко всем группам
- **Принцип "Прозрачности"**: Понятность решений для пользователей
- **Принцип "Конфиденциальности"**: Защита личных данных
- **Принцип "Безопасности"**: Защита от злонамеренного использования
- **Принцип "Ответственности"**: Четкое определение ответственности
- **Принцип "Человечности"**: Уважение к правам и достоинству людей

## Следующие шаги

После освоения лучших практик переходите к:
- [Примерам использования](./09_examples.md)
- [Troubleshooting](./10_troubleshooting.md)
