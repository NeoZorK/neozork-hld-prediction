# Углубленное описание Feature Generation and Apply

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему Feature Generation - это ключ к успеху в ML

**Почему 80% успеха машинного обучения зависит от качества признаков?** Потому что даже самый лучший алгоритм не сможет найти паттерны в плохих данных. Feature Generation - это искусство превращения сырых данных в золото для машинного обучения.

### Что дает правильная генерация признаков?

- **Точность**: Модели работают на 20-50% лучше
- **Интерпретируемость**: Понимание того, что влияет на результат
- **Робастность**: Модели работают стабильно на новых данных
- **Эффективность**: Меньше данных, лучшие результаты

### Что происходит без правильной генерации признаков?

- **Плохие результаты**: Модели не находят паттерны
- **Переобучение**: Модели запоминают данные вместо обучения
- **Нестабильность**: Модели работают по-разному на похожих данных
- **Разочарование**: Не понимаете, почему результаты не улучшаются

## Теоретические основы Feature Generation

### 🎯 Концепция генерации признаков

```mermaid
graph TD
    A[Сырые данные] --> B[Feature Generation]
    B --> C[Обработанные признаки]
    C --> D[ML Модель]
    D --> E[Предсказания]
    
    B --> F[Временные признаки]
    B --> G[Статистические признаки]
    B --> H[Технические индикаторы]
    B --> I[Категориальные признаки]
    B --> J[Текстовые признаки]
    
    F --> F1[Лаговые признаки]
    F --> F2[Скользящие окна]
    F --> F3[Сезонные признаки]
    
    G --> G1[Моменты распределения]
    G --> G2[Признаки изменений]
    G --> G3[Волатильность]
    
    H --> H1[Трендовые индикаторы]
    H --> H2[Моментум индикаторы]
    H --> H3[Волатильность индикаторы]
    
    I --> I1[One-hot encoding]
    I --> I2[Target encoding]
    I --> I3[Иерархические признаки]
    
    J --> J1[TF-IDF]
    J --> J2[Word2Vec]
    J --> J3[Базовые текстовые признаки]
    
    C --> K[Оценка качества]
    K --> L[Корреляция]
    K --> M[Важность признаков]
    K --> N[Стабильность]
    
    L --> O[Отбор признаков]
    M --> O
    N --> O
    
    O --> P[Финальный набор признаков]
    P --> D
    
    style A fill:#ffcdd2
    style C fill:#c8e6c9
    style E fill:#a5d6a7
    style B fill:#e3f2fd
    style K fill:#fff3e0
```

### Математические принципы

**Feature Engineering как оптимизационная задача:**

```math
F* = argmax P(Y|X, F(X))
```

Где:

- `F*` - оптимальная функция генерации признаков
- `Y` - целевая переменная
- `X` - исходные данные
- `F(X)` - сгенерированные признаки

**Критерии качества признаков:**

1. **Информативность**: I(X;Y) = H(Y) - H(Y|X)
2. **Стабильность**: Var(f(X)) < threshold
3. **Независимость**: Cov(f_i(X), f_j(X)) ≈ 0
4. **Масштабируемость**: f(X) ∈ [0,1] или стандартизовано

### Типы признаков по происхождению

### 📊 Классификация типов признаков

```mermaid
graph TD
    A[Типы признаков] --> B[Исходные признаки]
    A --> C[Производные признаки]
    A --> D[Интерактивные признаки]
    A --> E[Временные признаки]
    A --> F[Категориальные признаки]
    
    B --> B1[Необработанные данные]
    B --> B2[Требуют предобработки]
    B --> B3[Могут содержать шум]
    
    C --> C1[Математические преобразования]
    C --> C2[Статистические характеристики]
    C --> C3[Создаются из исходных]
    
    D --> D1[Комбинации признаков]
    D --> D2[Полиномиальные признаки]
    D --> D3[Логические операции]
    
    E --> E1[Зависят от времени]
    E --> E2[Лаговые признаки]
    E --> E3[Скользящие окна]
    
    F --> F1[Дискретные значения]
    F --> F2[Требуют кодирования]
    F --> F3[Могут быть иерархическими]
    
    B1 --> G[Критерии качества]
    B2 --> G
    B3 --> G
    C1 --> G
    C2 --> G
    C3 --> G
    D1 --> G
    D2 --> G
    D3 --> G
    E1 --> G
    E2 --> G
    E3 --> G
    F1 --> G
    F2 --> G
    F3 --> G
    
    G --> H[Информативность]
    G --> I[Стабильность]
    G --> J[Независимость]
    G --> K[Масштабируемость]
    
    H --> L[I(X;Y) = H(Y) - H(Y|X)]
    I --> M[Var(f(X)) < threshold]
    J --> N[Cov(f_i(X), f_j(X)) ≈ 0]
    K --> O[f(X) ∈ [0,1] или стандартизовано]
    
    style A fill:#e3f2fd
    style G fill:#c8e6c9
    style L fill:#fff3e0
    style M fill:#fff3e0
    style N fill:#fff3e0
    style O fill:#fff3e0
```

### 1. Исходные признаки (Raw Features)

- Необработанные данные из источника
- Часто требуют предобработки
- Могут содержать шум и выбросы

### 2. Производные признаки (Derived Features)

- Создаются из исходных признаков
- Математические преобразования
- Статистические характеристики

### 3. Интерактивные признаки (Interaction Features)

- Комбинации нескольких признаков
- Полиномиальные признаки
- Логические операции

### 4. Временные признаки (Temporal Features)

- Признаки, зависящие от времени
- Лаговые признаки
- Скользящие окна

### 5. Категориальные признаки (Categorical Features)

- Дискретные значения
- Требуют кодирования
- Могут быть иерархическими

## Продвинутые техники генерации признаков

### 1. Временные признаки (Time Series Features)

### ⏰ Процесс создания временных признаков

```mermaid
graph TD
    A[Временной ряд] --> B{Тип временных признаков}
    
    B -->|Лаговые| C[Лаговые признаки]
    B -->|Скользящие окна| D[Скользящие окна]
    B -->|Экспоненциальное сглаживание| E[Экспоненциальное сглаживание]
    B -->|Сезонные| F[Сезонные признаки]
    
    C --> C1[lag_1, lag_2, lag_3]
    C --> C2[lag_7, lag_14, lag_30]
    C --> C3[Сдвиг на N периодов]
    
    D --> D1[Скользящее среднее]
    D --> D2[Скользящее std]
    D --> D3[Скользящий min/max]
    D --> D4[Скользящая медиана]
    
    E --> E1[EWM с α=0.1]
    E --> E2[EWM с α=0.3]
    E --> E3[EWM с α=0.5]
    E --> E4[EWM с α=0.7]
    
    F --> F1[Год, месяц, день]
    F --> F2[День недели, квартал]
    F --> F3[Циклические признаки]
    F --> F4[sin/cos преобразования]
    
    C1 --> G[Временные признаки]
    C2 --> G
    C3 --> G
    D1 --> G
    D2 --> G
    D3 --> G
    D4 --> G
    E1 --> G
    E2 --> G
    E3 --> G
    E4 --> G
    F1 --> G
    F2 --> G
    F3 --> G
    F4 --> G
    
    G --> H[Оценка качества]
    H --> I[Корреляция с целевой]
    H --> J[Стабильность во времени]
    H --> K[Информативность]
    
    I --> L[Отбор лучших признаков]
    J --> L
    K --> L
    
    L --> M[Финальные временные признаки]
    
    style A fill:#e3f2fd
    style G fill:#c8e6c9
    style M fill:#a5d6a7
    style H fill:#fff3e0
```

**Лаговые признаки (Lag Features):**

```python
def create_lag_features(df, target_col, lags=[1, 2, 3, 7, 14, 30], fill_method='forward', 
                       include_original=False, lag_prefix='lag', config=None):
    """
    Создание лаговых признаков для временных рядов
    
    Args:
        df (pd.DataFrame): Исходный DataFrame с временными данными
        target_col (str): Название целевой колонки для создания лагов
        lags (list): Список лагов для создания (по умолчанию [1, 2, 3, 7, 14, 30])
            - 1: Предыдущий период
            - 2-3: Краткосрочные лаги
            - 7: Недельный лаг
            - 14: Двухнедельный лаг
            - 30: Месячный лаг
        fill_method (str): Метод заполнения пропусков ('forward', 'backward', 'interpolate', 'zero')
            - 'forward': Заполнение предыдущим значением (ffill)
            - 'backward': Заполнение следующим значением (bfill)
            - 'interpolate': Линейная интерполяция
            - 'zero': Заполнение нулями
        include_original (bool): Включать ли исходную колонку в результат
        lag_prefix (str): Префикс для названий лаговых признаков
        config (dict): Дополнительная конфигурация
            - max_lag: Максимальный лаг (по умолчанию max(lags))
            - min_lag: Минимальный лаг (по умолчанию min(lags))
            - lag_step: Шаг между лагами (по умолчанию 1)
            - validation: Валидация данных (True/False)
            - memory_efficient: Эффективное использование памяти (True/False)
    
    Returns:
        pd.DataFrame: DataFrame с добавленными лаговыми признаками
        
    Raises:
        ValueError: Если target_col не существует в DataFrame
        ValueError: Если lags содержит недопустимые значения
        TypeError: Если fill_method не поддерживается
    """
    if config is None:
        config = {
            'max_lag': max(lags) if lags else 1,
            'min_lag': min(lags) if lags else 1,
            'lag_step': 1,
            'validation': True,
            'memory_efficient': False
        }
    
    # Валидация входных данных
    if config['validation']:
        if target_col not in df.columns:
            raise ValueError(f"Column '{target_col}' not found in DataFrame")
        
        if not lags or not all(isinstance(lag, int) and lag > 0 for lag in lags):
            raise ValueError("lags must be a list of positive integers")
        
        if fill_method not in ['forward', 'backward', 'interpolate', 'zero']:
            raise ValueError("fill_method must be one of: 'forward', 'backward', 'interpolate', 'zero'")
    
    # Создание копии DataFrame для безопасности
    result_df = df.copy() if not config['memory_efficient'] else df
    
    # Создание лаговых признаков
    for lag in lags:
        # Создание лагового признака
        lag_col_name = f'{target_col}_{lag_prefix}_{lag}'
        result_df[lag_col_name] = result_df[target_col].shift(lag)
        
        # Заполнение пропусков в зависимости от метода
        if fill_method == 'forward':
            result_df[lag_col_name] = result_df[lag_col_name].fillna(method='ffill')
        elif fill_method == 'backward':
            result_df[lag_col_name] = result_df[lag_col_name].fillna(method='bfill')
        elif fill_method == 'interpolate':
            result_df[lag_col_name] = result_df[lag_col_name].interpolate(method='linear')
        elif fill_method == 'zero':
            result_df[lag_col_name] = result_df[lag_col_name].fillna(0)
    
    # Удаление исходной колонки если не требуется
    if not include_original and target_col in result_df.columns:
        result_df = result_df.drop(columns=[target_col])
    
    return result_df

# Пример использования с детальными параметрами
df = create_lag_features(
    df, 
    target_col='price', 
    lags=[1, 2, 3, 7, 14, 30],  # Лаги от 1 до 30 дней
    fill_method='forward',       # Заполнение предыдущим значением
    include_original=True,       # Сохранить исходную колонку
    lag_prefix='lag',           # Префикс для названий
    config={
        'max_lag': 30,          # Максимальный лаг
        'min_lag': 1,           # Минимальный лаг
        'validation': True,     # Включить валидацию
        'memory_efficient': False  # Не экономить память
    }
)
```

**Скользящие окна (Rolling Windows):**

```python
def create_rolling_features(df, target_col, windows=[3, 7, 14, 30], 
                          statistics=['mean', 'std', 'min', 'max', 'median'],
                          min_periods=None, center=False, win_type=None,
                          on=None, axis=0, closed=None, config=None):
    """
    Создание признаков скользящих окон для временных рядов
    
    Args:
        df (pd.DataFrame): Исходный DataFrame с временными данными
        target_col (str): Название целевой колонки для создания скользящих окон
        windows (list): Список размеров окон (по умолчанию [3, 7, 14, 30])
            - 3: Краткосрочное окно (3 периода)
            - 7: Недельное окно (7 периодов)
            - 14: Двухнедельное окно (14 периодов)
            - 30: Месячное окно (30 периодов)
        statistics (list): Список статистик для вычисления
            - 'mean': Среднее значение
            - 'std': Стандартное отклонение
            - 'var': Дисперсия
            - 'min': Минимальное значение
            - 'max': Максимальное значение
            - 'median': Медиана
            - 'sum': Сумма
            - 'count': Количество значений
            - 'skew': Асимметрия
            - 'kurt': Эксцесс
            - 'quantile': Квантили (требует дополнительного параметра q)
        min_periods (int): Минимальное количество наблюдений в окне
            - None: Использовать размер окна
            - 1: Минимум 1 наблюдение
            - window//2: Половина размера окна
        center (bool): Центрировать окно (False для обычного, True для центрированного)
        win_type (str): Тип весового окна
            - None: Обычное окно
            - 'boxcar': Прямоугольное окно
            - 'triang': Треугольное окно
            - 'blackman': Окно Блэкмана
            - 'hamming': Окно Хэмминга
            - 'bartlett': Окно Бартлетта
        on (str): Колонка для группировки по времени
        axis (int): Ось для применения (0 для строк, 1 для колонок)
        closed (str): Какая сторона окна включена ('right', 'left', 'both', 'neither')
        config (dict): Дополнительная конфигурация
            - quantiles: Список квантилей для вычисления (по умолчанию [0.25, 0.5, 0.75])
            - custom_functions: Словарь пользовательских функций
            - fill_method: Метод заполнения пропусков ('forward', 'backward', 'interpolate', 'zero')
            - validation: Валидация данных (True/False)
            - memory_efficient: Эффективное использование памяти (True/False)
            - prefix: Префикс для названий признаков (по умолчанию 'rolling')
    
    Returns:
        pd.DataFrame: DataFrame с добавленными признаками скользящих окон
        
    Raises:
        ValueError: Если target_col не существует в DataFrame
        ValueError: Если windows содержит недопустимые значения
        ValueError: Если statistics содержит неподдерживаемые функции
        TypeError: Если параметры имеют неправильный тип
    """
    if config is None:
        config = {
            'quantiles': [0.25, 0.5, 0.75],
            'custom_functions': {},
            'fill_method': 'forward',
            'validation': True,
            'memory_efficient': False,
            'prefix': 'rolling'
        }
    
    # Валидация входных данных
    if config['validation']:
        if target_col not in df.columns:
            raise ValueError(f"Column '{target_col}' not found in DataFrame")
        
        if not windows or not all(isinstance(w, int) and w > 0 for w in windows):
            raise ValueError("windows must be a list of positive integers")
        
        valid_stats = ['mean', 'std', 'var', 'min', 'max', 'median', 'sum', 'count', 
                      'skew', 'kurt', 'quantile']
        invalid_stats = [s for s in statistics if s not in valid_stats and s not in config['custom_functions']]
        if invalid_stats:
            raise ValueError(f"Invalid statistics: {invalid_stats}. Valid options: {valid_stats}")
    
    # Создание копии DataFrame для безопасности
    result_df = df.copy() if not config['memory_efficient'] else df
    
    # Создание признаков скользящих окон
    for window in windows:
        # Создание объекта rolling
        rolling_obj = result_df[target_col].rolling(
            window=window,
            min_periods=min_periods or window,
            center=center,
            win_type=win_type,
            on=on,
            axis=axis,
            closed=closed
        )
        
        # Вычисление статистик
        for stat in statistics:
            if stat == 'mean':
                col_name = f'{target_col}_{config["prefix"]}_mean_{window}'
                result_df[col_name] = rolling_obj.mean()
            elif stat == 'std':
                col_name = f'{target_col}_{config["prefix"]}_std_{window}'
                result_df[col_name] = rolling_obj.std()
            elif stat == 'var':
                col_name = f'{target_col}_{config["prefix"]}_var_{window}'
                result_df[col_name] = rolling_obj.var()
            elif stat == 'min':
                col_name = f'{target_col}_{config["prefix"]}_min_{window}'
                result_df[col_name] = rolling_obj.min()
            elif stat == 'max':
                col_name = f'{target_col}_{config["prefix"]}_max_{window}'
                result_df[col_name] = rolling_obj.max()
            elif stat == 'median':
                col_name = f'{target_col}_{config["prefix"]}_median_{window}'
                result_df[col_name] = rolling_obj.median()
            elif stat == 'sum':
                col_name = f'{target_col}_{config["prefix"]}_sum_{window}'
                result_df[col_name] = rolling_obj.sum()
            elif stat == 'count':
                col_name = f'{target_col}_{config["prefix"]}_count_{window}'
                result_df[col_name] = rolling_obj.count()
            elif stat == 'skew':
                col_name = f'{target_col}_{config["prefix"]}_skew_{window}'
                result_df[col_name] = rolling_obj.skew()
            elif stat == 'kurt':
                col_name = f'{target_col}_{config["prefix"]}_kurt_{window}'
                result_df[col_name] = rolling_obj.kurt()
            elif stat == 'quantile':
                for q in config['quantiles']:
                    col_name = f'{target_col}_{config["prefix"]}_q{int(q*100)}_{window}'
                    result_df[col_name] = rolling_obj.quantile(q)
        
        # Применение пользовательских функций
        for func_name, func in config['custom_functions'].items():
            col_name = f'{target_col}_{config["prefix"]}_{func_name}_{window}'
            result_df[col_name] = rolling_obj.apply(func)
        
        # Заполнение пропусков
        if config['fill_method'] == 'forward':
            for col in result_df.columns:
                if col.startswith(f'{target_col}_{config["prefix"]}_'):
                    result_df[col] = result_df[col].fillna(method='ffill')
        elif config['fill_method'] == 'backward':
            for col in result_df.columns:
                if col.startswith(f'{target_col}_{config["prefix"]}_'):
                    result_df[col] = result_df[col].fillna(method='bfill')
        elif config['fill_method'] == 'interpolate':
            for col in result_df.columns:
                if col.startswith(f'{target_col}_{config["prefix"]}_'):
                    result_df[col] = result_df[col].interpolate(method='linear')
        elif config['fill_method'] == 'zero':
            for col in result_df.columns:
                if col.startswith(f'{target_col}_{config["prefix"]}_'):
                    result_df[col] = result_df[col].fillna(0)
    
    return result_df

# Пример использования с детальными параметрами
df = create_rolling_features(
    df, 
    target_col='price', 
    windows=[3, 7, 14, 30],  # Размеры окон
    statistics=['mean', 'std', 'min', 'max', 'median', 'quantile'],  # Статистики
    min_periods=1,           # Минимум 1 наблюдение
    center=False,            # Обычное окно
    win_type=None,           # Без весов
    config={
        'quantiles': [0.25, 0.5, 0.75, 0.9, 0.95],  # Квантили
        'custom_functions': {  # Пользовательские функции
            'range': lambda x: x.max() - x.min(),
            'iqr': lambda x: x.quantile(0.75) - x.quantile(0.25)
        },
        'fill_method': 'forward',  # Заполнение предыдущим значением
        'validation': True,        # Включить валидацию
        'memory_efficient': False, # Не экономить память
        'prefix': 'rolling'        # Префикс для названий
    }
)
```

**Экспоненциальное сглаживание (Exponential Smoothing):**

```python
def create_ewm_features(df, target_col, alphas=[0.1, 0.3, 0.5, 0.7], 
                       statistics=['mean'], adjust=True, ignore_na=False,
                       bias=False, config=None):
    """
    Создание признаков экспоненциального сглаживания для временных рядов
    
    Args:
        df (pd.DataFrame): Исходный DataFrame с временными данными
        target_col (str): Название целевой колонки для создания EWM признаков
        alphas (list): Список коэффициентов сглаживания (по умолчанию [0.1, 0.3, 0.5, 0.7])
            - 0.1: Медленное сглаживание (больше веса истории)
            - 0.3: Умеренное сглаживание
            - 0.5: Сбалансированное сглаживание
            - 0.7: Быстрое сглаживание (больше веса текущим значениям)
            - 0.9: Очень быстрое сглаживание
        statistics (list): Список статистик для вычисления
            - 'mean': Экспоненциально взвешенное среднее
            - 'std': Экспоненциально взвешенное стандартное отклонение
            - 'var': Экспоненциально взвешенная дисперсия
            - 'min': Экспоненциально взвешенный минимум
            - 'max': Экспоненциально взвешенный максимум
            - 'sum': Экспоненциально взвешенная сумма
            - 'count': Экспоненциально взвешенный счетчик
        adjust (bool): Использовать корректировку для учета начальных значений
            - True: Корректировка включена (рекомендуется)
            - False: Корректировка отключена
        ignore_na (bool): Игнорировать NaN значения при вычислении
            - True: Игнорировать NaN
            - False: Учитывать NaN
        bias (bool): Использовать смещенную оценку дисперсии
            - True: Смещенная оценка
            - False: Несмещенная оценка (рекомендуется)
        config (dict): Дополнительная конфигурация
            - span: Альтернатива alpha (span = 2/alpha - 1)
            - halflife: Альтернатива alpha (halflife = ln(2)/alpha)
            - com: Альтернатива alpha (com = 1/alpha - 1)
            - fill_method: Метод заполнения пропусков ('forward', 'backward', 'interpolate', 'zero')
            - validation: Валидация данных (True/False)
            - memory_efficient: Эффективное использование памяти (True/False)
            - prefix: Префикс для названий признаков (по умолчанию 'ewm')
            - custom_functions: Словарь пользовательских функций
    
    Returns:
        pd.DataFrame: DataFrame с добавленными признаками экспоненциального сглаживания
        
    Raises:
        ValueError: Если target_col не существует в DataFrame
        ValueError: Если alphas содержит недопустимые значения
        ValueError: Если statistics содержит неподдерживаемые функции
        TypeError: Если параметры имеют неправильный тип
    """
    if config is None:
        config = {
            'span': None,
            'halflife': None,
            'com': None,
            'fill_method': 'forward',
            'validation': True,
            'memory_efficient': False,
            'prefix': 'ewm',
            'custom_functions': {}
        }
    
    # Валидация входных данных
    if config['validation']:
        if target_col not in df.columns:
            raise ValueError(f"Column '{target_col}' not found in DataFrame")
        
        if not alphas or not all(isinstance(a, (int, float)) and 0 < a <= 1 for a in alphas):
            raise ValueError("alphas must be a list of numbers between 0 and 1")
        
        valid_stats = ['mean', 'std', 'var', 'min', 'max', 'sum', 'count']
        invalid_stats = [s for s in statistics if s not in valid_stats and s not in config['custom_functions']]
        if invalid_stats:
            raise ValueError(f"Invalid statistics: {invalid_stats}. Valid options: {valid_stats}")
    
    # Создание копии DataFrame для безопасности
    result_df = df.copy() if not config['memory_efficient'] else df
    
    # Создание признаков экспоненциального сглаживания
    for alpha in alphas:
        # Создание объекта EWM
        ewm_obj = result_df[target_col].ewm(
            alpha=alpha,
            adjust=adjust,
            ignore_na=ignore_na,
            bias=bias,
            span=config['span'],
            halflife=config['halflife'],
            com=config['com']
        )
        
        # Вычисление статистик
        for stat in statistics:
            if stat == 'mean':
                col_name = f'{target_col}_{config["prefix"]}_mean_{alpha}'
                result_df[col_name] = ewm_obj.mean()
            elif stat == 'std':
                col_name = f'{target_col}_{config["prefix"]}_std_{alpha}'
                result_df[col_name] = ewm_obj.std()
            elif stat == 'var':
                col_name = f'{target_col}_{config["prefix"]}_var_{alpha}'
                result_df[col_name] = ewm_obj.var()
            elif stat == 'min':
                col_name = f'{target_col}_{config["prefix"]}_min_{alpha}'
                result_df[col_name] = ewm_obj.min()
            elif stat == 'max':
                col_name = f'{target_col}_{config["prefix"]}_max_{alpha}'
                result_df[col_name] = ewm_obj.max()
            elif stat == 'sum':
                col_name = f'{target_col}_{config["prefix"]}_sum_{alpha}'
                result_df[col_name] = ewm_obj.sum()
            elif stat == 'count':
                col_name = f'{target_col}_{config["prefix"]}_count_{alpha}'
                result_df[col_name] = ewm_obj.count()
        
        # Применение пользовательских функций
        for func_name, func in config['custom_functions'].items():
            col_name = f'{target_col}_{config["prefix"]}_{func_name}_{alpha}'
            result_df[col_name] = ewm_obj.apply(func)
        
        # Заполнение пропусков
        if config['fill_method'] == 'forward':
            for col in result_df.columns:
                if col.startswith(f'{target_col}_{config["prefix"]}_'):
                    result_df[col] = result_df[col].fillna(method='ffill')
        elif config['fill_method'] == 'backward':
            for col in result_df.columns:
                if col.startswith(f'{target_col}_{config["prefix"]}_'):
                    result_df[col] = result_df[col].fillna(method='bfill')
        elif config['fill_method'] == 'interpolate':
            for col in result_df.columns:
                if col.startswith(f'{target_col}_{config["prefix"]}_'):
                    result_df[col] = result_df[col].interpolate(method='linear')
        elif config['fill_method'] == 'zero':
            for col in result_df.columns:
                if col.startswith(f'{target_col}_{config["prefix"]}_'):
                    result_df[col] = result_df[col].fillna(0)
    
    return result_df

# Пример использования с детальными параметрами
df = create_ewm_features(
    df, 
    target_col='price', 
    alphas=[0.1, 0.3, 0.5, 0.7],  # Коэффициенты сглаживания
    statistics=['mean', 'std', 'var'],  # Статистики
    adjust=True,                # Корректировка включена
    ignore_na=False,            # Учитывать NaN
    bias=False,                 # Несмещенная оценка
    config={
        'span': None,           # Не использовать span
        'halflife': None,       # Не использовать halflife
        'com': None,            # Не использовать com
        'fill_method': 'forward',  # Заполнение предыдущим значением
        'validation': True,     # Включить валидацию
        'memory_efficient': False,  # Не экономить память
        'prefix': 'ewm',        # Префикс для названий
        'custom_functions': {   # Пользовательские функции
            'trend': lambda x: x.iloc[-1] - x.iloc[0] if len(x) > 1 else 0,
            'volatility': lambda x: x.std() if len(x) > 1 else 0
        }
    }
)
```

**Сезонные признаки (Seasonal Features):**

```python
def create_seasonal_features(df, date_col, features=['year', 'month', 'day', 'dayofweek', 'dayofyear', 'week', 'quarter'],
                           cyclic_features=True, timezone=None, business_hours=False, 
                           holidays=None, config=None):
    """
    Создание сезонных признаков из временных данных
    
    Args:
        df (pd.DataFrame): Исходный DataFrame с временными данными
        date_col (str): Название колонки с датой/временем
        features (list): Список сезонных признаков для создания
            - 'year': Год (2020, 2021, 2022, ...)
            - 'month': Месяц (1-12)
            - 'day': День месяца (1-31)
            - 'dayofweek': День недели (0=понедельник, 6=воскресенье)
            - 'dayofyear': День года (1-366)
            - 'week': Неделя года (1-53)
            - 'quarter': Квартал (1-4)
            - 'hour': Час дня (0-23)
            - 'minute': Минута (0-59)
            - 'second': Секунда (0-59)
            - 'is_weekend': Выходной день (True/False)
            - 'is_month_start': Начало месяца (True/False)
            - 'is_month_end': Конец месяца (True/False)
            - 'is_quarter_start': Начало квартала (True/False)
            - 'is_quarter_end': Конец квартала (True/False)
            - 'is_year_start': Начало года (True/False)
            - 'is_year_end': Конец года (True/False)
        cyclic_features (bool): Создавать ли циклические признаки (sin/cos)
            - True: Создавать циклические признаки для периодических данных
            - False: Создавать только обычные признаки
        timezone (str): Часовой пояс для конвертации (например, 'UTC', 'Europe/Moscow')
        business_hours (bool): Создавать ли признаки рабочих часов
            - True: Создавать признаки рабочих часов (9-17, понедельник-пятница)
            - False: Не создавать признаки рабочих часов
        holidays (list): Список праздничных дней для создания признаков
            - None: Не учитывать праздники
            - ['2023-01-01', '2023-12-25']: Список дат праздников
        config (dict): Дополнительная конфигурация
            - cyclic_periods: Периоды для циклических признаков
                - 'month': 12 (месяцы)
                - 'dayofweek': 7 (дни недели)
                - 'hour': 24 (часы)
                - 'dayofyear': 365 (дни года)
            - business_hours_start: Начало рабочих часов (по умолчанию 9)
            - business_hours_end: Конец рабочих часов (по умолчанию 17)
            - business_days: Рабочие дни (по умолчанию [0,1,2,3,4] - пн-пт)
            - fill_method: Метод заполнения пропусков ('forward', 'backward', 'interpolate', 'zero')
            - validation: Валидация данных (True/False)
            - memory_efficient: Эффективное использование памяти (True/False)
            - prefix: Префикс для названий признаков (по умолчанию 'seasonal')
    
    Returns:
        pd.DataFrame: DataFrame с добавленными сезонными признаками
        
    Raises:
        ValueError: Если date_col не существует в DataFrame
        ValueError: Если date_col не является datetime
        ValueError: Если features содержит неподдерживаемые признаки
        TypeError: Если параметры имеют неправильный тип
    """
    if config is None:
        config = {
            'cyclic_periods': {
                'month': 12,
                'dayofweek': 7,
                'hour': 24,
                'dayofyear': 365
            },
            'business_hours_start': 9,
            'business_hours_end': 17,
            'business_days': [0, 1, 2, 3, 4],  # пн-пт
            'fill_method': 'forward',
            'validation': True,
            'memory_efficient': False,
            'prefix': 'seasonal'
        }
    
    # Валидация входных данных
    if config['validation']:
        if date_col not in df.columns:
            raise ValueError(f"Column '{date_col}' not found in DataFrame")
        
        if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
            raise ValueError(f"Column '{date_col}' must be datetime type")
        
        valid_features = ['year', 'month', 'day', 'dayofweek', 'dayofyear', 'week', 'quarter',
                         'hour', 'minute', 'second', 'is_weekend', 'is_month_start', 'is_month_end',
                         'is_quarter_start', 'is_quarter_end', 'is_year_start', 'is_year_end']
        invalid_features = [f for f in features if f not in valid_features]
        if invalid_features:
            raise ValueError(f"Invalid features: {invalid_features}. Valid options: {valid_features}")
    
    # Создание копии DataFrame для безопасности
    result_df = df.copy() if not config['memory_efficient'] else df
    
    # Конвертация в datetime если необходимо
    if not pd.api.types.is_datetime64_any_dtype(result_df[date_col]):
        result_df[date_col] = pd.to_datetime(result_df[date_col])
    
    # Конвертация часового пояса если указан
    if timezone:
        result_df[date_col] = result_df[date_col].dt.tz_convert(timezone)
    
    # Создание сезонных признаков
    for feature in features:
        if feature == 'year':
            col_name = f'{config["prefix"]}_year'
            result_df[col_name] = result_df[date_col].dt.year
        elif feature == 'month':
            col_name = f'{config["prefix"]}_month'
            result_df[col_name] = result_df[date_col].dt.month
        elif feature == 'day':
            col_name = f'{config["prefix"]}_day'
            result_df[col_name] = result_df[date_col].dt.day
        elif feature == 'dayofweek':
            col_name = f'{config["prefix"]}_dayofweek'
            result_df[col_name] = result_df[date_col].dt.dayofweek
        elif feature == 'dayofyear':
            col_name = f'{config["prefix"]}_dayofyear'
            result_df[col_name] = result_df[date_col].dt.dayofyear
        elif feature == 'week':
            col_name = f'{config["prefix"]}_week'
            result_df[col_name] = result_df[date_col].dt.isocalendar().week
        elif feature == 'quarter':
            col_name = f'{config["prefix"]}_quarter'
            result_df[col_name] = result_df[date_col].dt.quarter
        elif feature == 'hour':
            col_name = f'{config["prefix"]}_hour'
            result_df[col_name] = result_df[date_col].dt.hour
        elif feature == 'minute':
            col_name = f'{config["prefix"]}_minute'
            result_df[col_name] = result_df[date_col].dt.minute
        elif feature == 'second':
            col_name = f'{config["prefix"]}_second'
            result_df[col_name] = result_df[date_col].dt.second
        elif feature == 'is_weekend':
            col_name = f'{config["prefix"]}_is_weekend'
            result_df[col_name] = result_df[date_col].dt.dayofweek.isin([5, 6])
        elif feature == 'is_month_start':
            col_name = f'{config["prefix"]}_is_month_start'
            result_df[col_name] = result_df[date_col].dt.is_month_start
        elif feature == 'is_month_end':
            col_name = f'{config["prefix"]}_is_month_end'
            result_df[col_name] = result_df[date_col].dt.is_month_end
        elif feature == 'is_quarter_start':
            col_name = f'{config["prefix"]}_is_quarter_start'
            result_df[col_name] = result_df[date_col].dt.is_quarter_start
        elif feature == 'is_quarter_end':
            col_name = f'{config["prefix"]}_is_quarter_end'
            result_df[col_name] = result_df[date_col].dt.is_quarter_end
        elif feature == 'is_year_start':
            col_name = f'{config["prefix"]}_is_year_start'
            result_df[col_name] = result_df[date_col].dt.is_year_start
        elif feature == 'is_year_end':
            col_name = f'{config["prefix"]}_is_year_end'
            result_df[col_name] = result_df[date_col].dt.is_year_end
    
    # Создание циклических признаков
    if cyclic_features:
        for feature in features:
            if feature == 'month' and feature in features:
                period = config['cyclic_periods']['month']
                result_df[f'{config["prefix"]}_month_sin'] = np.sin(2 * np.pi * result_df[f'{config["prefix"]}_month'] / period)
                result_df[f'{config["prefix"]}_month_cos'] = np.cos(2 * np.pi * result_df[f'{config["prefix"]}_month'] / period)
            elif feature == 'dayofweek' and feature in features:
                period = config['cyclic_periods']['dayofweek']
                result_df[f'{config["prefix"]}_dayofweek_sin'] = np.sin(2 * np.pi * result_df[f'{config["prefix"]}_dayofweek'] / period)
                result_df[f'{config["prefix"]}_dayofweek_cos'] = np.cos(2 * np.pi * result_df[f'{config["prefix"]}_dayofweek'] / period)
            elif feature == 'hour' and feature in features:
                period = config['cyclic_periods']['hour']
                result_df[f'{config["prefix"]}_hour_sin'] = np.sin(2 * np.pi * result_df[f'{config["prefix"]}_hour'] / period)
                result_df[f'{config["prefix"]}_hour_cos'] = np.cos(2 * np.pi * result_df[f'{config["prefix"]}_hour'] / period)
            elif feature == 'dayofyear' and feature in features:
                period = config['cyclic_periods']['dayofyear']
                result_df[f'{config["prefix"]}_dayofyear_sin'] = np.sin(2 * np.pi * result_df[f'{config["prefix"]}_dayofyear'] / period)
                result_df[f'{config["prefix"]}_dayofyear_cos'] = np.cos(2 * np.pi * result_df[f'{config["prefix"]}_dayofyear'] / period)
    
    # Создание признаков рабочих часов
    if business_hours:
        result_df[f'{config["prefix"]}_is_business_hour'] = (
            (result_df[date_col].dt.hour >= config['business_hours_start']) &
            (result_df[date_col].dt.hour < config['business_hours_end']) &
            (result_df[date_col].dt.dayofweek.isin(config['business_days']))
        )
        result_df[f'{config["prefix"]}_is_business_day'] = result_df[date_col].dt.dayofweek.isin(config['business_days'])
    
    # Создание признаков праздников
    if holidays:
        result_df[f'{config["prefix"]}_is_holiday'] = result_df[date_col].dt.date.isin([pd.to_datetime(h).date() for h in holidays])
    
    # Заполнение пропусков
    if config['fill_method'] == 'forward':
        for col in result_df.columns:
            if col.startswith(f'{config["prefix"]}_'):
                result_df[col] = result_df[col].fillna(method='ffill')
    elif config['fill_method'] == 'backward':
        for col in result_df.columns:
            if col.startswith(f'{config["prefix"]}_'):
                result_df[col] = result_df[col].fillna(method='bfill')
    elif config['fill_method'] == 'interpolate':
        for col in result_df.columns:
            if col.startswith(f'{config["prefix"]}_'):
                result_df[col] = result_df[col].interpolate(method='linear')
    elif config['fill_method'] == 'zero':
        for col in result_df.columns:
            if col.startswith(f'{config["prefix"]}_'):
                result_df[col] = result_df[col].fillna(0)
    
    return result_df

# Пример использования с детальными параметрами
df = create_seasonal_features(
    df, 
    date_col='date',
    features=['year', 'month', 'day', 'dayofweek', 'dayofyear', 'week', 'quarter', 'hour', 'is_weekend'],
    cyclic_features=True,           # Создавать циклические признаки
    timezone='UTC',                # Часовой пояс UTC
    business_hours=True,           # Создавать признаки рабочих часов
    holidays=['2023-01-01', '2023-12-25'],  # Праздничные дни
    config={
        'cyclic_periods': {        # Периоды для циклических признаков
            'month': 12,
            'dayofweek': 7,
            'hour': 24,
            'dayofyear': 365
        },
        'business_hours_start': 9,  # Начало рабочих часов
        'business_hours_end': 17,   # Конец рабочих часов
        'business_days': [0, 1, 2, 3, 4],  # Рабочие дни (пн-пт)
        'fill_method': 'forward',   # Заполнение предыдущим значением
        'validation': True,         # Включить валидацию
        'memory_efficient': False,  # Не экономить память
        'prefix': 'seasonal'        # Префикс для названий
    }
)
```

### 2. Статистические признаки (Statistical Features)

### 📈 Статистические признаки и их применение

```mermaid
graph TD
    A[Исходные данные] --> B{Тип статистических признаков}
    
    B -->|Моменты распределения| C[Моменты распределения]
    B -->|Признаки изменений| D[Признаки изменений]
    B -->|Волатильность| E[Волатильность]
    
    C --> C1[Среднее, std, var]
    C --> C2[Skewness, Kurtosis]
    C --> C3[Квантили: q25, q50, q75, q90, q95, q99]
    
    D --> D1[Абсолютное изменение]
    D --> D2[Логарифмическое изменение]
    D --> D3[Разность значений]
    D --> D4[Процентное изменение]
    
    E --> E1[Реализованная волатильность]
    E --> E2[GARCH волатильность]
    E --> E3[Максимальная волатильность]
    E --> E4[Волатильность по окнам]
    
    C1 --> F[Статистические признаки]
    C2 --> F
    C3 --> F
    D1 --> F
    D2 --> F
    D3 --> F
    D4 --> F
    E1 --> F
    E2 --> F
    E3 --> F
    E4 --> F
    
    F --> G[Окна расчета]
    G --> G1[7 дней]
    G --> G2[14 дней]
    G --> G3[30 дней]
    G --> G4[90 дней]
    
    G1 --> H[Скользящие статистики]
    G2 --> H
    G3 --> H
    G4 --> H
    
    H --> I[Оценка качества]
    I --> J[Корреляция с целевой]
    I --> K[Стабильность распределения]
    I --> L[Информативность]
    
    J --> M[Отбор признаков]
    K --> M
    L --> M
    
    M --> N[Финальные статистические признаки]
    
    style A fill:#e3f2fd
    style F fill:#c8e6c9
    style N fill:#a5d6a7
    style I fill:#fff3e0
```

**Моменты распределения:**

```python
def create_moment_features(df, target_col, windows=[7, 14, 30]):
    """Создание признаков моментов распределения"""
    for window in windows:
        rolling = df[target_col].rolling(window)
        
        # Первые моменты
        df[f'{target_col}_mean_{window}'] = rolling.mean()
        df[f'{target_col}_std_{window}'] = rolling.std()
        df[f'{target_col}_var_{window}'] = rolling.var()
        
        # Высшие моменты
        df[f'{target_col}_skew_{window}'] = rolling.skew()
        df[f'{target_col}_kurt_{window}'] = rolling.kurt()
        
        # Квантили
        df[f'{target_col}_q25_{window}'] = rolling.quantile(0.25)
        df[f'{target_col}_q50_{window}'] = rolling.quantile(0.50)
        df[f'{target_col}_q75_{window}'] = rolling.quantile(0.75)
        df[f'{target_col}_q90_{window}'] = rolling.quantile(0.90)
        df[f'{target_col}_q95_{window}'] = rolling.quantile(0.95)
        df[f'{target_col}_q99_{window}'] = rolling.quantile(0.99)
        
    return df

# Пример использования
df = create_moment_features(df, 'price', windows=[7, 14, 30])
```

**Признаки изменений (Change Features):**

```python
def create_change_features(df, target_col, periods=[1, 2, 3, 7, 14, 30]):
    """Создание признаков изменений"""
    for period in periods:
        # Абсолютное изменение
        df[f'{target_col}_change_{period}'] = df[target_col].pct_change(period)
        # Логарифмическое изменение
        df[f'{target_col}_log_change_{period}'] = np.log(df[target_col] / df[target_col].shift(period))
        # Разность
        df[f'{target_col}_diff_{period}'] = df[target_col].diff(period)
        
    return df

# Пример использования
df = create_change_features(df, 'price', periods=[1, 2, 3, 7, 14, 30])
```

**Признаки волатильности (Volatility Features):**

```python
def create_volatility_features(df, target_col, windows=[7, 14, 30]):
    """Создание признаков волатильности"""
    for window in windows:
        # Реализованная волатильность
        returns = df[target_col].pct_change()
        df[f'{target_col}_vol_{window}'] = returns.rolling(window).std() * np.sqrt(252)
        
        # GARCH волатильность (упрощенная)
        df[f'{target_col}_garch_vol_{window}'] = returns.rolling(window).std() * np.sqrt(252) * 1.2
        
        # Максимальная волатильность
        df[f'{target_col}_max_vol_{window}'] = returns.rolling(window).std().rolling(window).max()
        
    return df

# Пример использования
df = create_volatility_features(df, 'price', windows=[7, 14, 30])
```

### 3. Технические индикаторы (Technical Indicators)

### 📊 Технические индикаторы и их классификация

```mermaid
graph TD
    A[Ценовые данные] --> B{Тип технических индикаторов}
    
    B -->|Трендовые| C[Трендовые индикаторы]
    B -->|Моментум| D[Моментум индикаторы]
    B -->|Волатильность| E[Волатильность индикаторы]
    
    C --> C1[SMA - Simple Moving Average]
    C --> C2[EMA - Exponential Moving Average]
    C --> C3[WMA - Weighted Moving Average]
    C --> C4[Trend - разность цены и SMA]
    
    D --> D1[RSI - Relative Strength Index]
    D --> D2[Stochastic Oscillator]
    D --> D3[Williams %R]
    D --> D4[ROC - Rate of Change]
    
    E --> E1[Bollinger Bands]
    E --> E2[ATR - Average True Range]
    E --> E3[Volatility по окнам]
    E --> E4[Position в Bollinger Bands]
    
    C1 --> F[Технические индикаторы]
    C2 --> F
    C3 --> F
    C4 --> F
    D1 --> F
    D2 --> F
    D3 --> F
    D4 --> F
    E1 --> F
    E2 --> F
    E3 --> F
    E4 --> F
    
    F --> G[Окна расчета]
    G --> G1[7 периодов]
    G --> G2[14 периодов]
    G --> G3[30 периодов]
    G --> G4[50 периодов]
    G --> G5[200 периодов]
    
    G1 --> H[Скользящие индикаторы]
    G2 --> H
    G3 --> H
    G4 --> H
    G5 --> H
    
    H --> I[Нормализация]
    I --> J[Масштабирование 0-1]
    I --> K[Z-score нормализация]
    I --> L[Min-Max нормализация]
    
    J --> M[Финальные индикаторы]
    K --> M
    L --> M
    
    M --> N[Оценка качества]
    N --> O[Корреляция с доходностью]
    N --> P[Стабильность сигналов]
    N --> Q[Информативность]
    
    O --> R[Отбор лучших индикаторов]
    P --> R
    Q --> R
    
    R --> S[Финальный набор индикаторов]
    
    style A fill:#e3f2fd
    style F fill:#c8e6c9
    style S fill:#a5d6a7
    style N fill:#fff3e0
```

**Трендовые индикаторы:**

```python
def create_trend_features(df, target_col, windows=[7, 14, 30, 50, 200]):
    """Создание трендовых индикаторов"""
    for window in windows:
        # Простое скользящее среднее
        df[f'{target_col}_sma_{window}'] = df[target_col].rolling(window).mean()
        
        # Экспоненциальное скользящее среднее
        df[f'{target_col}_ema_{window}'] = df[target_col].ewm(span=window).mean()
        
        # Взвешенное скользящее среднее
        weights = np.arange(1, window + 1)
        df[f'{target_col}_wma_{window}'] = df[target_col].rolling(window).apply(
            lambda x: np.average(x, weights=weights), raw=True
        )
        
        # Тренд (разность между ценой и SMA)
        df[f'{target_col}_trend_{window}'] = df[target_col] - df[f'{target_col}_sma_{window}']
        
    return df

# Пример использования
df = create_trend_features(df, 'price', windows=[7, 14, 30, 50, 200])
```

**Моментум индикаторы:**

```python
def create_momentum_features(df, target_col, windows=[7, 14, 30]):
    """Создание моментум индикаторов"""
    for window in windows:
        # RSI (Relative Strength Index)
        delta = df[target_col].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        df[f'{target_col}_rsi_{window}'] = 100 - (100 / (1 + rs))
        
        # Stochastic Oscillator
        low_min = df[target_col].rolling(window).min()
        high_max = df[target_col].rolling(window).max()
        df[f'{target_col}_stoch_{window}'] = 100 * (df[target_col] - low_min) / (high_max - low_min)
        
        # Williams %R
        df[f'{target_col}_williams_r_{window}'] = -100 * (high_max - df[target_col]) / (high_max - low_min)
        
        # Rate of Change
        df[f'{target_col}_roc_{window}'] = df[target_col].pct_change(window) * 100
        
    return df

# Пример использования
df = create_momentum_features(df, 'price', windows=[7, 14, 30])
```

**Волатильность индикаторы:**

```python
def create_volatility_indicators(df, target_col, windows=[7, 14, 30]):
    """Создание волатильность индикаторов"""
    for window in windows:
        # Bollinger Bands
        sma = df[target_col].rolling(window).mean()
        std = df[target_col].rolling(window).std()
        df[f'{target_col}_bb_upper_{window}'] = sma + (std * 2)
        df[f'{target_col}_bb_lower_{window}'] = sma - (std * 2)
        df[f'{target_col}_bb_width_{window}'] = df[f'{target_col}_bb_upper_{window}'] - df[f'{target_col}_bb_lower_{window}']
        df[f'{target_col}_bb_position_{window}'] = (df[target_col] - df[f'{target_col}_bb_lower_{window}']) / df[f'{target_col}_bb_width_{window}']
        
        # Average True Range (ATR)
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df[target_col].shift())
        low_close = np.abs(df['low'] - df[target_col].shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        df[f'{target_col}_atr_{window}'] = true_range.rolling(window).mean()
        
    return df

# Пример использования
df = create_volatility_indicators(df, 'price', windows=[7, 14, 30])
```

### 4. Категориальные признаки (Categorical Features)

**Кодирование категориальных признаков:**

```python
def create_categorical_features(df, categorical_cols):
    """Создание категориальных признаков"""
    for col in categorical_cols:
        # One-hot encoding
        dummies = pd.get_dummies(df[col], prefix=col)
        df = pd.concat([df, dummies], axis=1)
        
        # Label encoding
        df[f'{col}_label'] = df[col].astype('category').cat.codes
        
        # Target encoding (сглаженная)
        target_mean = df.groupby(col)['target'].mean()
        df[f'{col}_target_encoded'] = df[col].map(target_mean)
        
        # Frequency encoding
        freq = df[col].value_counts()
        df[f'{col}_freq'] = df[col].map(freq)
        
    return df

# Пример использования
df = create_categorical_features(df, ['category', 'region', 'type'])
```

**Иерархические признаки:**

```python
def create_hierarchical_features(df, hierarchical_cols):
    """Создание иерархических признаков"""
    for col in hierarchical_cols:
        # Уровни иерархии
        df[f'{col}_level_1'] = df[col].str.split('.').str[0]
        df[f'{col}_level_2'] = df[col].str.split('.').str[1]
        df[f'{col}_level_3'] = df[col].str.split('.').str[2]
        
        # Глубина иерархии
        df[f'{col}_depth'] = df[col].str.count('.') + 1
        
        # Родительские признаки
        df[f'{col}_parent'] = df[col].str.rsplit('.', 1).str[0]
        
    return df

# Пример использования
df = create_hierarchical_features(df, ['category_path', 'region_path'])
```

### 5. Текстовые признаки (Text Features)

**Базовые текстовые признаки:**

```python
def create_text_features(df, text_col):
    """Создание базовых текстовых признаков"""
    # Длина текста
    df[f'{text_col}_length'] = df[text_col].str.len()
    
    # Количество слов
    df[f'{text_col}_word_count'] = df[text_col].str.split().str.len()
    
    # Количество предложений
    df[f'{text_col}_sentence_count'] = df[text_col].str.count(r'[.!?]+')
    
    # Количество заглавных букв
    df[f'{text_col}_upper_count'] = df[text_col].str.count(r'[A-Z]')
    
    # Количество цифр
    df[f'{text_col}_digit_count'] = df[text_col].str.count(r'\d')
    
    # Количество знаков препинания
    df[f'{text_col}_punct_count'] = df[text_col].str.count(r'[^\w\s]')
    
    # Количество уникальных слов
    df[f'{text_col}_unique_words'] = df[text_col].str.split().apply(lambda x: len(set(x)))
    
    # Средняя длина слова
    df[f'{text_col}_avg_word_length'] = df[text_col].str.split().str.len().mean()
    
    return df

# Пример использования
df = create_text_features(df, 'description')
```

**TF-IDF признаки:**

```python
def create_tfidf_features(df, text_col, max_features=1000):
    """Создание TF-IDF признаков"""
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    # TF-IDF векторная модель
    tfidf = TfidfVectorizer(
        max_features=max_features,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    
    # Обучение и преобразование
    tfidf_matrix = tfidf.fit_transform(df[text_col].fillna(''))
    
    # Создание DataFrame с TF-IDF признаками
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(),
        columns=[f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])]
    )
    
    # Объединение с исходным DataFrame
    df = pd.concat([df, tfidf_df], axis=1)
    
    return df

# Пример использования
df = create_tfidf_features(df, 'description', max_features=1000)
```

**Word2Vec признаки:**

```python
def create_word2vec_features(df, text_col, vector_size=100):
    """Создание Word2Vec признаков"""
    from gensim.models import Word2Vec
    
    # Подготовка текста
    sentences = df[text_col].fillna('').str.split().tolist()
    
    # Обучение Word2Vec модели
    model = Word2Vec(
        sentences,
        vector_size=vector_size,
        window=5,
        min_count=2,
        workers=4
    )
    
    # Создание признаков для каждого документа
    def get_document_vector(words):
        vectors = []
        for word in words:
            if word in model.wv:
                vectors.append(model.wv[word])
        if vectors:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(vector_size)
    
    # Применение к каждому документу
    doc_vectors = df[text_col].fillna('').str.split().apply(get_document_vector)
    
    # Создание DataFrame с Word2Vec признаками
    w2v_df = pd.DataFrame(
        doc_vectors.tolist(),
        columns=[f'w2v_{i}' for i in range(vector_size)]
    )
    
    # Объединение с исходным DataFrame
    df = pd.concat([df, w2v_df], axis=1)
    
    return df

# Пример использования
df = create_word2vec_features(df, 'description', vector_size=100)
```

## Автоматическая генерация признаков

### 🤖 Автоматическая генерация признаков

```mermaid
graph TD
    A[Исходные данные] --> B{Метод автоматической генерации}
    
    B -->|Генетическое программирование| C[Генетическое программирование]
    B -->|Полиномиальные признаки| D[Полиномиальные признаки]
    B -->|Интерактивные признаки| E[Интерактивные признаки]
    
    C --> C1[Создание популяции]
    C --> C2[Мутации и кроссовер]
    C --> C3[Оценка фитнеса]
    C --> C4[Селекция лучших]
    
    D --> D1[Степень полинома]
    D --> D2[Взаимодействия признаков]
    D --> D3[Создание комбинаций]
    D --> D4[Отбор значимых]
    
    E --> E1[Бинарные взаимодействия]
    E --> E2[Тройные взаимодействия]
    E --> E3[Математические операции]
    E --> E4[Логические комбинации]
    
    C1 --> F[Автоматически сгенерированные признаки]
    C2 --> F
    C3 --> F
    C4 --> F
    D1 --> F
    D2 --> F
    D3 --> F
    D4 --> F
    E1 --> F
    E2 --> F
    E3 --> F
    E4 --> F
    
    F --> G[Оценка качества]
    G --> H[Корреляция с целевой]
    G --> I[Важность признаков]
    G --> J[Стабильность]
    G --> K[Мультиколлинеарность]
    
    H --> L[Отбор признаков]
    I --> L
    J --> L
    K --> L
    
    L --> M[Финальный набор признаков]
    
    M --> N[Применение в AutoML Gluon]
    N --> O[Обучение модели]
    O --> P[Оценка производительности]
    P --> Q[Оптимизация признаков]
    
    Q --> R{Улучшение результата?}
    R -->|Да| S[Использовать признаки]
    R -->|Нет| T[Пересмотр стратегии]
    T --> B
    
    style A fill:#e3f2fd
    style F fill:#c8e6c9
    style M fill:#a5d6a7
    style S fill:#4caf50
    style T fill:#ff9800
```

### 1. Генетическое программирование

```python
def genetic_feature_generation(df, target_col, generations=50, population_size=100):
    """Генетическое программирование для генерации признаков"""
    import random
    from deap import base, creator, tools, algorithms
    
    # Определение функций
    def add(x, y): return x + y
    def sub(x, y): return x - y
    def mul(x, y): return x * y
    def div(x, y): return x / (y + 1e-8)
    def sqrt(x): return np.sqrt(np.abs(x))
    def log(x): return np.log(np.abs(x) + 1e-8)
    def exp(x): return np.exp(np.clip(x, -10, 10))
    
    # Создание набора функций
    pset = base.PrimitiveSet("MAIN", 2)
    pset.addPrimitive(add, 2)
    pset.addPrimitive(sub, 2)
    pset.addPrimitive(mul, 2)
    pset.addPrimitive(div, 2)
    pset.addPrimitive(sqrt, 1)
    pset.addPrimitive(log, 1)
    pset.addPrimitive(exp, 1)
    
    # Создание классов
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    
    # Создание инструментов
    toolbox = base.Toolbox()
    toolbox.register("expr", tools.genHalfAndHalf, pset=pset, min_=1, max_=3)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    # Функция оценки
    def evaluate(individual):
        try:
            # Компиляция дерева
            tree = pset.compile(expr=individual)
            
            # Применение к данным
            feature = tree(df.iloc[:, 0], df.iloc[:, 1])
            
            # Проверка на валидность
            if np.isnan(feature).any() or np.isinf(feature).any():
                return (0,)
            
            # Корреляция с целевой переменной
            correlation = np.corrcoef(feature, df[target_col])[0, 1]
            
            return (abs(correlation),)
        except:
            return (0,)
    
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutUniform, expr=toolbox.expr, pset=pset)
    toolbox.register("select", tools.selTournament, tournsize=3)
    
    # Создание популяции
    population = toolbox.population(n=population_size)
    
    # Эволюция
    for gen in range(generations):
        # Оценка
        fitnesses = list(map(toolbox.evaluate, population))
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit
        
        # Селекция
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))
        
        # Кроссовер
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.5:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        
        # Мутация
        for mutant in offspring:
            if random.random() < 0.2:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        
        # Замена популяции
        population[:] = offspring
    
    return population

# Пример использования
population = genetic_feature_generation(df, 'target', generations=50, population_size=100)
```

### 2. Автоматическое создание полиномиальных признаков

```python
def create_polynomial_features(df, feature_cols, degree=2, interaction_only=False):
    """Создание полиномиальных признаков"""
    from sklearn.preprocessing import PolynomialFeatures
    
    # Выбор признаков
    X = df[feature_cols].fillna(0)
    
    # Создание полиномиальных признаков
    poly = PolynomialFeatures(
        degree=degree,
        interaction_only=interaction_only,
        include_bias=False
    )
    
    # Преобразование
    X_poly = poly.fit_transform(X)
    
    # Создание названий признаков
    feature_names = poly.get_feature_names_out(feature_cols)
    
    # Создание DataFrame
    poly_df = pd.DataFrame(X_poly, columns=feature_names, index=df.index)
    
    # Объединение с исходным DataFrame
    df = pd.concat([df, poly_df], axis=1)
    
    return df

# Пример использования
df = create_polynomial_features(df, ['feature1', 'feature2', 'feature3'], degree=2)
```

### 3. Автоматическое создание интерактивных признаков

```python
def create_interaction_features(df, feature_cols, max_interactions=10):
    """Создание интерактивных признаков"""
    from itertools import combinations
    
    # Создание всех возможных комбинаций
    interactions = []
    for r in range(2, min(len(feature_cols) + 1, max_interactions + 1)):
        interactions.extend(combinations(feature_cols, r))
    
    # Создание интерактивных признаков
    for interaction in interactions:
        if len(interaction) == 2:
            # Бинарные взаимодействия
            col1, col2 = interaction
            df[f'{col1}_x_{col2}'] = df[col1] * df[col2]
            df[f'{col1}_div_{col2}'] = df[col1] / (df[col2] + 1e-8)
            df[f'{col1}_plus_{col2}'] = df[col1] + df[col2]
            df[f'{col1}_minus_{col2}'] = df[col1] - df[col2]
        elif len(interaction) == 3:
            # Тройные взаимодействия
            col1, col2, col3 = interaction
            df[f'{col1}_x_{col2}_x_{col3}'] = df[col1] * df[col2] * df[col3]
            df[f'{col1}_x_{col2}_div_{col3}'] = (df[col1] * df[col2]) / (df[col3] + 1e-8)
    
    return df

# Пример использования
df = create_interaction_features(df, ['feature1', 'feature2', 'feature3'], max_interactions=5)
```

## Оценка качества признаков

### 📊 Метрики оценки качества признаков

```mermaid
graph TD
    A[Сгенерированные признаки] --> B{Тип оценки качества}
    
    B -->|Статистические тесты| C[Статистические тесты]
    B -->|ML тесты| D[ML тесты]
    B -->|Стабильность| E[Тесты стабильности]
    
    C --> C1[Корреляция с целевой]
    C --> C2[Мультиколлинеарность]
    C --> C3[Распределение признаков]
    C --> C4[Выбросы и аномалии]
    
    D --> D1[Важность признаков]
    D --> D2[Feature Selection]
    D --> D3[Cross-validation]
    D --> D4[Permutation importance]
    
    E --> E1[Временная стабильность]
    E --> E2[Распределительная стабильность]
    E --> E3[Корреляционная стабильность]
    E --> E4[Дрифт признаков]
    
    C1 --> F[Оценка качества]
    C2 --> F
    C3 --> F
    C4 --> F
    D1 --> F
    D2 --> F
    D3 --> F
    D4 --> F
    E1 --> F
    E2 --> F
    E3 --> F
    E4 --> F
    
    F --> G[Критерии отбора]
    G --> H[Высокая корреляция > 0.1]
    G --> I[Низкая мультиколлинеарность < 0.8]
    G --> J[Стабильность > 0.7]
    G --> K[Важность > 0.01]
    
    H --> L[Отбор признаков]
    I --> L
    J --> L
    K --> L
    
    L --> M[Финальный набор признаков]
    
    M --> N[Валидация на тестовых данных]
    N --> O[Проверка производительности]
    O --> P[Мониторинг в продакшене]
    
    P --> Q{Качество приемлемое?}
    Q -->|Да| R[Признаки готовы к использованию]
    Q -->|Нет| S[Пересмотр и улучшение]
    S --> A
    
    style A fill:#e3f2fd
    style F fill:#c8e6c9
    style M fill:#a5d6a7
    style R fill:#4caf50
    style S fill:#ff9800
```

### 1. Статистические тесты

**Тест корреляции:**

```python
def evaluate_correlation_features(df, target_col, threshold=0.1):
    """Оценка признаков по корреляции"""
    correlations = df.corr()[target_col].abs().sort_values(ascending=False)
    
    # Признаки с высокой корреляцией
    high_corr = correlations[correlations > threshold]
    
    # Признаки с низкой корреляцией
    low_corr = correlations[correlations <= threshold]
    
    return {
        'high_correlation': high_corr,
        'low_correlation': low_corr,
        'correlation_stats': {
            'mean': correlations.mean(),
            'std': correlations.std(),
            'min': correlations.min(),
            'max': correlations.max()
        }
    }

# Пример использования
correlation_results = evaluate_correlation_features(df, 'target', threshold=0.1)
```

**Тест мультиколлинеарности:**

```python
def evaluate_multicollinearity(df, threshold=0.8):
    """Оценка мультиколлинеарности"""
    from sklearn.feature_selection import VarianceThreshold
    
    # Вычисление корреляционной матрицы
    corr_matrix = df.corr().abs()
    
    # Поиск высоко коррелированных пар
    high_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if corr_matrix.iloc[i, j] > threshold:
                high_corr_pairs.append((
                    corr_matrix.columns[i],
                    corr_matrix.columns[j],
                    corr_matrix.iloc[i, j]
                ))
    
    # Удаление признаков с низкой дисперсией
    selector = VarianceThreshold(threshold=0.01)
    X = df.select_dtypes(include=[np.number])
    X_selected = selector.fit_transform(X)
    
    return {
        'high_correlation_pairs': high_corr_pairs,
        'low_variance_features': X.columns[~selector.get_support()].tolist(),
        'selected_features': X.columns[selector.get_support()].tolist()
    }

# Пример использования
multicollinearity_results = evaluate_multicollinearity(df, threshold=0.8)
```

### 2. Машинное обучение тесты

**Тест важности признаков:**

```python
def evaluate_feature_importance(df, target_col, n_features=20):
    """Оценка важности признаков"""
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    
    # Подготовка данных
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Разделение на train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Обучение модели
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Важность признаков
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    # Топ признаков
    top_features = feature_importance.head(n_features)
    
    return {
        'feature_importance': feature_importance,
        'top_features': top_features,
        'model_score': model.score(X_test, y_test)
    }

# Пример использования
importance_results = evaluate_feature_importance(df, 'target', n_features=20)
```

**Тест стабильности признаков:**

```python
def evaluate_feature_stability(df, target_col, n_splits=5):
    """Оценка стабильности признаков"""
    from sklearn.model_selection import KFold
    from sklearn.ensemble import RandomForestRegressor
    
    # Подготовка данных
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # K-fold кросс-валидация
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    # Список для хранения важности признаков
    feature_importances = []
    
    for train_idx, val_idx in kf.split(X):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        
        # Обучение модели
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Сохранение важности признаков
        feature_importances.append(model.feature_importances_)
    
    # Вычисление стабильности
    feature_importances = np.array(feature_importances)
    stability = np.std(feature_importances, axis=0)
    
    # Создание DataFrame
    stability_df = pd.DataFrame({
        'feature': X.columns,
        'stability': stability,
        'mean_importance': np.mean(feature_importances, axis=0)
    }).sort_values('stability')
    
    return stability_df

# Пример использования
stability_results = evaluate_feature_stability(df, 'target', n_splits=5)
```

## Применение признаков в AutoML Gluon

### 🔗 Интеграция с AutoML Gluon

```mermaid
graph TD
    A[Сгенерированные признаки] --> B[Подготовка данных]
    B --> C[Разделение train/test]
    C --> D[Создание TabularPredictor]
    
    D --> E[Настройка параметров]
    E --> F[problem_type: regression/classification]
    E --> G[eval_metric: rmse/accuracy]
    E --> H[presets: best_quality]
    
    F --> I[Обучение модели]
    G --> I
    H --> I
    
    I --> J[Автоматический выбор признаков]
    J --> K[Mutual Information]
    J --> L[F-regression]
    J --> M[Random Forest importance]
    
    K --> N[Отбор лучших признаков]
    L --> N
    M --> N
    
    N --> O[Обучение финальной модели]
    O --> P[Предсказания на тесте]
    P --> Q[Оценка качества]
    
    Q --> R[MSE/RMSE]
    Q --> S[R² Score]
    Q --> T[Feature Importance]
    
    R --> U[Результаты]
    S --> U
    T --> U
    
    U --> V{Качество приемлемое?}
    V -->|Да| W[Деплой модели]
    V -->|Нет| X[Оптимизация признаков]
    
    X --> Y[Добавление новых признаков]
    Y --> Z[Удаление плохих признаков]
    Z --> AA[Настройка параметров]
    
    Y --> B
    Z --> B
    AA --> B
    
    W --> BB[Мониторинг в продакшене]
    BB --> CC[Отслеживание дрифта]
    CC --> DD[Переобучение при необходимости]
    
    style A fill:#e3f2fd
    style I fill:#c8e6c9
    style U fill:#a5d6a7
    style W fill:#4caf50
    style X fill:#ff9800
```

### 1. Интеграция с AutoML Gluon

```python
def apply_features_to_autogluon(df, target_col, feature_cols, test_size=0.2):
    """Применение признаков в AutoML Gluon"""
    from autogluon.tabular import TabularPredictor
    
    # Подготовка данных
    X = df[feature_cols]
    y = df[target_col]
    
    # Разделение на train/test
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    # Создание train_data
    train_data = X_train.copy()
    train_data[target_col] = y_train
    
    # Создание предиктора
    predictor = TabularPredictor(
        label=target_col,
        problem_type='regression',
        eval_metric='rmse'
    )
    
    # Обучение
    predictor.fit(
        train_data,
        time_limit=3600,  # 1 час
        presets='best_quality'
    )
    
    # Предсказание
    predictions = predictor.predict(X_test)
    
    # Оценка качества
    from sklearn.metrics import mean_squared_error, r2_score
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    return {
        'predictor': predictor,
        'predictions': predictions,
        'mse': mse,
        'r2': r2,
        'feature_importance': predictor.feature_importance()
    }

# Пример использования
results = apply_features_to_autogluon(df, 'target', feature_cols, test_size=0.2)
```

### 2. Автоматический выбор признаков

```python
def automatic_feature_selection(df, target_col, method='mutual_info', k=20):
    """Автоматический выбор признаков"""
    from sklearn.feature_selection import (
        SelectKBest, mutual_info_regression, f_regression, 
        SelectFromModel, RandomForestRegressor
    )
    
    # Подготовка данных
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    if method == 'mutual_info':
        # Mutual Information
        selector = SelectKBest(score_func=mutual_info_regression, k=k)
    elif method == 'f_regression':
        # F-regression
        selector = SelectKBest(score_func=f_regression, k=k)
    elif method == 'random_forest':
        # Random Forest
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        selector = SelectFromModel(model, max_features=k)
    else:
        raise ValueError("Method must be 'mutual_info', 'f_regression', or 'random_forest'")
    
    # Применение селектора
    X_selected = selector.fit_transform(X, y)
    
    # Получение выбранных признаков
    selected_features = X.columns[selector.get_support()].tolist()
    
    return {
        'selected_features': selected_features,
        'X_selected': X_selected,
        'selector': selector
    }

# Пример использования
selected_features = automatic_feature_selection(df, 'target', method='mutual_info', k=20)
```

### 3. Пайплайн генерации признаков

### 🔄 Пайплайн генерации признаков

```mermaid
graph TD
    A[Исходные данные] --> B[Feature Generation Pipeline]
    
    B --> C[Генераторы признаков]
    C --> D[Временные признаки]
    C --> E[Статистические признаки]
    C --> F[Технические индикаторы]
    C --> G[Категориальные признаки]
    C --> H[Текстовые признаки]
    
    D --> I[Объединение признаков]
    E --> I
    F --> I
    G --> I
    H --> I
    
    I --> J[Селекторы признаков]
    J --> K[Mutual Information]
    J --> L[F-regression]
    J --> M[Random Forest]
    J --> N[Variance Threshold]
    
    K --> O[Отбор признаков]
    L --> O
    M --> O
    N --> O
    
    O --> P[Валидация признаков]
    P --> Q[Cross-validation]
    P --> R[Stability testing]
    P --> S[Drift detection]
    
    Q --> T[Финальный набор признаков]
    R --> T
    S --> T
    
    T --> U[Применение в AutoML Gluon]
    U --> V[Обучение модели]
    V --> W[Оценка производительности]
    
    W --> X{Результат приемлемый?}
    X -->|Да| Y[Деплой в продакшен]
    X -->|Нет| Z[Оптимизация пайплайна]
    
    Z --> AA[Настройка генераторов]
    Z --> BB[Настройка селекторов]
    Z --> CC[Добавление новых методов]
    
    AA --> B
    BB --> B
    CC --> B
    
    Y --> DD[Мониторинг в продакшене]
    DD --> EE[Отслеживание качества]
    EE --> FF[Автоматическое переобучение]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style T fill:#a5d6a7
    style Y fill:#4caf50
    style Z fill:#ff9800
```

```python
class FeatureGenerationPipeline:
    """Пайплайн генерации признаков"""
    
    def __init__(self):
        self.feature_generators = []
        self.feature_selectors = []
        self.fitted = False
    
    def add_generator(self, generator_func, **kwargs):
        """Добавление генератора признаков"""
        self.feature_generators.append((generator_func, kwargs))
    
    def add_selector(self, selector_func, **kwargs):
        """Добавление селектора признаков"""
        self.feature_selectors.append((selector_func, kwargs))
    
    def fit_transform(self, df, target_col):
        """Обучение и преобразование"""
        result_df = df.copy()
        
        # Применение генераторов
        for generator_func, kwargs in self.feature_generators:
            result_df = generator_func(result_df, **kwargs)
        
        # Применение селекторов
        for selector_func, kwargs in self.feature_selectors:
            result_df = selector_func(result_df, target_col, **kwargs)
        
        self.fitted = True
        return result_df
    
    def transform(self, df):
        """Только преобразование"""
        if not self.fitted:
            raise ValueError("Pipeline must be fitted first")
        
        result_df = df.copy()
        
        # Применение генераторов
        for generator_func, kwargs in self.feature_generators:
            result_df = generator_func(result_df, **kwargs)
        
        return result_df

# Пример использования
pipeline = FeatureGenerationPipeline()

# Добавление генераторов
pipeline.add_generator(create_lag_features, target_col='price', lags=[1, 2, 3, 7, 14, 30])
pipeline.add_generator(create_rolling_features, target_col='price', windows=[3, 7, 14, 30])
pipeline.add_generator(create_trend_features, target_col='price', windows=[7, 14, 30, 50, 200])

# Добавление селекторов
pipeline.add_selector(automatic_feature_selection, method='mutual_info', k=50)

# Обучение и преобразование
df_transformed = pipeline.fit_transform(df, 'target')
```

## Мониторинг и валидация признаков

### 1. Мониторинг дрейфа признаков

```python
def monitor_feature_drift(df_baseline, df_current, feature_cols, threshold=0.1):
    """Мониторинг дрейфа признаков"""
    from scipy import stats
    
    drift_results = {}
    
    for col in feature_cols:
        # Статистические тесты
        ks_stat, ks_pvalue = stats.ks_2samp(df_baseline[col], df_current[col])
        chi2_stat, chi2_pvalue = stats.chi2_contingency(
            pd.crosstab(df_baseline[col], df_current[col])
        )[0:2]
        
        # Вычисление дрейфа
        baseline_mean = df_baseline[col].mean()
        current_mean = df_current[col].mean()
        drift = abs(current_mean - baseline_mean) / baseline_mean
        
        # Определение статуса
        if drift > threshold:
            status = 'DRIFT'
        elif ks_pvalue < 0.05:
            status = 'DISTRIBUTION_CHANGE'
        else:
            status = 'STABLE'
        
        drift_results[col] = {
            'drift': drift,
            'ks_stat': ks_stat,
            'ks_pvalue': ks_pvalue,
            'chi2_stat': chi2_stat,
            'chi2_pvalue': chi2_pvalue,
            'status': status
        }
    
    return drift_results

# Пример использования
drift_results = monitor_feature_drift(df_baseline, df_current, feature_cols, threshold=0.1)
```

### 2. Валидация признаков

```python
def validate_features(df, target_col, feature_cols, validation_method='cross_validation'):
    """Валидация признаков"""
    from sklearn.model_selection import cross_val_score
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LinearRegression
    
    # Подготовка данных
    X = df[feature_cols]
    y = df[target_col]
    
    # Модели для валидации
    models = {
        'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
        'LinearRegression': LinearRegression()
    }
    
    validation_results = {}
    
    for model_name, model in models.items():
        # Кросс-валидация
        scores = cross_val_score(model, X, y, cv=5, scoring='r2')
        
        validation_results[model_name] = {
            'mean_score': scores.mean(),
            'std_score': scores.std(),
            'scores': scores
        }
    
    return validation_results

# Пример использования
validation_results = validate_features(df, 'target', feature_cols, validation_method='cross_validation')
```

## Сводная таблица параметров генерации признаков

### 📊 Основные параметры функций генерации признаков

| Функция | Параметр | Значение по умолчанию | Описание | Диапазон/Влияние |
|---------|----------|----------------------|----------|------------------|
| **create_lag_features** | | | | |
| | `lags` | [1, 2, 3, 7, 14, 30] | Список лагов для создания | 1-365 дней |
| | `fill_method` | 'forward' | Метод заполнения пропусков | forward, backward, interpolate, zero |
| | `include_original` | False | Включать исходную колонку | True, False |
| | `lag_prefix` | 'lag' | Префикс для названий | str |
| | `config.max_lag` | max(lags) | Максимальный лаг | 1-365 |
| | `config.min_lag` | min(lags) | Минимальный лаг | 1-365 |
| | `config.validation` | True | Валидация данных | True, False |
| | `config.memory_efficient` | False | Эффективное использование памяти | True, False |
| **create_rolling_features** | | | | |
| | `windows` | [3, 7, 14, 30] | Размеры окон | 1-365 периодов |
| | `statistics` | ['mean', 'std', 'min', 'max', 'median'] | Статистики для вычисления | mean, std, var, min, max, median, sum, count, skew, kurt, quantile |
| | `min_periods` | None | Минимальное количество наблюдений | 1-window |
| | `center` | False | Центрировать окно | True, False |
| | `win_type` | None | Тип весового окна | None, boxcar, triang, blackman, hamming, bartlett |
| | `config.quantiles` | [0.25, 0.5, 0.75] | Квантили для вычисления | 0.0-1.0 |
| | `config.custom_functions` | {} | Пользовательские функции | dict |
| | `config.fill_method` | 'forward' | Метод заполнения пропусков | forward, backward, interpolate, zero |
| | `config.prefix` | 'rolling' | Префикс для названий | str |
| **create_ewm_features** | | | | |
| | `alphas` | [0.1, 0.3, 0.5, 0.7] | Коэффициенты сглаживания | 0.0-1.0 |
| | `statistics` | ['mean'] | Статистики для вычисления | mean, std, var, min, max, sum, count |
| | `adjust` | True | Корректировка для начальных значений | True, False |
| | `ignore_na` | False | Игнорировать NaN | True, False |
| | `bias` | False | Смещенная оценка дисперсии | True, False |
| | `config.span` | None | Альтернатива alpha | 1-1000 |
| | `config.halflife` | None | Альтернатива alpha | 1-1000 |
| | `config.com` | None | Альтернатива alpha | 1-1000 |
| | `config.prefix` | 'ewm' | Префикс для названий | str |
| **create_seasonal_features** | | | | |
| | `features` | ['year', 'month', 'day', 'dayofweek', 'dayofyear', 'week', 'quarter'] | Сезонные признаки | year, month, day, dayofweek, dayofyear, week, quarter, hour, minute, second, is_weekend, is_month_start, is_month_end, is_quarter_start, is_quarter_end, is_year_start, is_year_end |
| | `cyclic_features` | True | Создавать циклические признаки | True, False |
| | `timezone` | None | Часовой пояс | str (UTC, Europe/Moscow, etc.) |
| | `business_hours` | False | Создавать признаки рабочих часов | True, False |
| | `holidays` | None | Список праздничных дней | list of dates |
| | `config.cyclic_periods` | {'month': 12, 'dayofweek': 7, 'hour': 24, 'dayofyear': 365} | Периоды для циклических признаков | dict |
| | `config.business_hours_start` | 9 | Начало рабочих часов | 0-23 |
| | `config.business_hours_end` | 17 | Конец рабочих часов | 0-23 |
| | `config.business_days` | [0, 1, 2, 3, 4] | Рабочие дни | list of int (0-6) |
| | `config.prefix` | 'seasonal' | Префикс для названий | str |
| **create_moment_features** | | | | |
| | `windows` | [7, 14, 30] | Окна для вычисления | 1-365 периодов |
| | `config.prefix` | 'moment' | Префикс для названий | str |
| **create_change_features** | | | | |
| | `periods` | [1, 2, 3, 7, 14, 30] | Периоды для изменений | 1-365 периодов |
| | `config.prefix` | 'change' | Префикс для названий | str |
| **create_volatility_features** | | | | |
| | `windows` | [7, 14, 30] | Окна для волатильности | 1-365 периодов |
| | `config.prefix` | 'vol' | Префикс для названий | str |
| **create_trend_features** | | | | |
| | `windows` | [7, 14, 30, 50, 200] | Окна для трендовых индикаторов | 1-365 периодов |
| | `config.prefix` | 'trend' | Префикс для названий | str |
| **create_momentum_features** | | | | |
| | `windows` | [7, 14, 30] | Окна для моментум индикаторов | 1-365 периодов |
| | `config.prefix` | 'momentum' | Префикс для названий | str |
| **create_volatility_indicators** | | | | |
| | `windows` | [7, 14, 30] | Окна для волатильность индикаторов | 1-365 периодов |
| | `config.prefix` | 'vol_ind' | Префикс для названий | str |
| **create_categorical_features** | | | | |
| | `categorical_cols` | [] | Список категориальных колонок | list of str |
| | `config.prefix` | 'cat' | Префикс для названий | str |
| **create_hierarchical_features** | | | | |
| | `hierarchical_cols` | [] | Список иерархических колонок | list of str |
| | `config.prefix` | 'hier' | Префикс для названий | str |
| **create_text_features** | | | | |
| | `text_col` | '' | Название текстовой колонки | str |
| | `config.prefix` | 'text' | Префикс для названий | str |
| **create_tfidf_features** | | | | |
| | `text_col` | '' | Название текстовой колонки | str |
| | `max_features` | 1000 | Максимальное количество признаков | 100-10000 |
| | `config.prefix` | 'tfidf' | Префикс для названий | str |
| **create_word2vec_features** | | | | |
| | `text_col` | '' | Название текстовой колонки | str |
| | `vector_size` | 100 | Размер вектора | 50-500 |
| | `config.prefix` | 'w2v' | Префикс для названий | str |
| **genetic_feature_generation** | | | | |
| | `generations` | 50 | Количество поколений | 10-1000 |
| | `population_size` | 100 | Размер популяции | 50-1000 |
| | `config.prefix` | 'genetic' | Префикс для названий | str |
| **create_polynomial_features** | | | | |
| | `feature_cols` | [] | Список признаков для полиномиальных | list of str |
| | `degree` | 2 | Степень полинома | 1-5 |
| | `interaction_only` | False | Только взаимодействия | True, False |
| | `config.prefix` | 'poly' | Префикс для названий | str |
| **create_interaction_features** | | | | |
| | `feature_cols` | [] | Список признаков для взаимодействий | list of str |
| | `max_interactions` | 10 | Максимальное количество взаимодействий | 2-50 |
| | `config.prefix` | 'interaction' | Префикс для названий | str |

### 🎯 Рекомендации по настройке параметров

#### Для начинающих

- Используйте значения по умолчанию для большинства параметров
- Настройте только основные параметры (lags, windows, alphas)
- Включите базовые статистики (mean, std, min, max)
- Используйте простые методы заполнения пропусков (forward)

#### Для опытных пользователей

- Настройте все параметры в соответствии с вашими данными
- Добавьте пользовательские функции и циклические признаки
- Используйте расширенные статистики (skew, kurt, quantile)
- Настройте валидацию и эффективное использование памяти

#### Для продакшена

- Настройте все параметры в соответствии с требованиями SLA
- Включите все типы признаков (временные, статистические, технические, категориальные, текстовые)
- Используйте автоматическую генерацию признаков
- Настройте мониторинг и валидацию признаков
- Включите все проверки безопасности и производительности

## Заключение

Feature Generation - это основа успешного машинного обучения. Правильная генерация признаков может:

1. **Увеличить точность** моделей на 20-50%
2. **Улучшить интерпретируемость** результатов
3. **Повысить робастность** моделей
4. **Сократить время** обучения

### Ключевые принципы

1. **Понимание данных** - знайте, с чем работаете
2. **Доменные знания** - используйте экспертизу в предметной области
3. **Автоматизация** - автоматизируйте рутинные процессы
4. **Валидация** - всегда проверяйте качество признаков
5. **Мониторинг** - следите за стабильностью признаков

### Следующие шаги

После освоения генерации признаков переходите к:

- [Методикам бэктестинга](./27_backtesting_methods.md)
- [Walk-forward анализу](./28_walk_forward_analysis.md)
- [Monte Carlo симуляциям](./29_monte_carlo_simulations.md)
- [Управлению портфолио](./30_portfolio_management.md)
