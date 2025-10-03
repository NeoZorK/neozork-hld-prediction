# 04. 🔧 Инженерия признаков

**Цель:** Научиться создавать эффективные признаки для ML-моделей в финансовых данных.

## Что такое инженерия признаков?

**Теория:** Инженерия признаков - это фундаментальный процесс в машинном обучении, который заключается в создании, трансформации и отборе признаков для улучшения производительности ML-моделей. В финансовой сфере это особенно критично, так как качество признаков напрямую влияет на точность торговых сигналов.

**Инженерия признаков** - это процесс создания новых признаков из существующих данных для улучшения производительности ML-моделей.

**Почему инженерия признаков критична для финансовых систем:**
- **Финансовые данные сложны:** Требуют специальной обработки для выявления паттернов
- **Высокие риски:** Плохие признаки могут привести к значительным потерям
- **Конкурентное преимущество:** Качественные признаки дают преимущество на рынке
- **Регуляторные требования:** Финансовые регуляторы требуют прозрачности признаков

### Почему это важно?

**Теория:** Качество признаков является определяющим фактором успеха ML-моделей. Исследования показывают, что качественные признаки могут улучшить производительность модели больше, чем увеличение объема данных или сложности алгоритма.

- **Качество признаков** > **Количество данных**
  - **Почему:** Хорошие признаки содержат больше информации о целевой переменной
  - **Плюсы:** Более эффективное использование данных, лучшая интерпретируемость
  - **Минусы:** Требует экспертных знаний, больше времени на разработку

- **Правильные признаки** могут удвоить точность модели
  - **Почему:** Релевантные признаки напрямую связаны с целевой переменной
  - **Плюсы:** Значительное улучшение производительности, снижение рисков
  - **Минусы:** Сложность определения релевантных признаков

- **Плохие признаки** могут испортить даже лучшие алгоритмы
  - **Почему:** Шум в признаках передается в модель и ухудшает её производительность
  - **Плюсы:** Понимание важности качества данных
  - **Минусы:** Необходимость тщательной валидации признаков

**Дополнительные аспекты важности:**
- **Интерпретируемость:** Хорошие признаки легко интерпретировать
- **Стабильность:** Качественные признаки стабильны во времени
- **Масштабируемость:** Хорошие признаки работают на разных данных
- **Робастность:** Качественные признаки устойчивы к выбросам

## Типы признаков

**Теория:** Признаки в финансовых ML-моделях можно классифицировать по различным критериям. Понимание типов признаков критично для создания эффективных моделей и предотвращения ошибок.

### 1. Технические индикаторы

**Теория:** Технические индикаторы - это математические преобразования ценовых данных, которые помогают выявить паттерны и тренды. Они основаны на многолетнем опыте технических аналитиков и являются стандартом в финансовой индустрии.

**Почему технические индикаторы важны:**
- **Проверенность временем:** Многолетний опыт использования
- **Стандартизация:** Универсальные метрики для анализа
- **Интерпретируемость:** Легко понимать и объяснять
- **Эффективность:** Доказанная эффективность в торговле

**Типы технических индикаторов:**
- **Трендовые:** SMA, EMA, MACD - показывают направление тренда
- **Осцилляторы:** RSI, Stochastic - показывают перекупленность/перепроданность
- **Волатильность:** Bollinger Bands, ATR - показывают волатильность
- **Объемные:** OBV, VWAP - учитывают объем торгов

**Плюсы технических индикаторов:**
- Проверенная эффективность
- Стандартизированные метрики
- Легкая интерпретация
- Широкая поддержка в инструментах

**Минусы технических индикаторов:**
- Могут быть запаздывающими
- Могут генерировать ложные сигналы
- Требуют настройки параметров
- Могут быть избыточными
```python
def create_technical_indicators(df):
    """Создание технических индикаторов"""
    
    # RSI
    df['RSI'] = calculate_rsi(df['Close'])
    
    # MACD
    df['MACD'] = calculate_macd(df['Close'])
    
    # Bollinger Bands
    df['BB_Upper'], df['BB_Lower'] = calculate_bollinger_bands(df['Close'])
    
    # Stochastic
    df['Stoch_K'], df['Stoch_D'] = calculate_stochastic(df['High'], df['Low'], df['Close'])
    
    return df

def calculate_rsi(prices, window=14):
    """Расчет RSI"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Расчет MACD"""
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram
```

### 2. Статистические признаки

**Теория:** Статистические признаки основаны на математических свойствах данных и помогают выявить скрытые паттерны. Они особенно полезны для ML-моделей, так как основаны на статистических принципах.

**Почему статистические признаки важны:**
- **Математическая обоснованность:** Основаны на статистических принципах
- **Универсальность:** Работают на разных типах данных
- **Интерпретируемость:** Легко понимать и объяснять
- **Стабильность:** Менее подвержены шуму

**Типы статистических признаков:**
- **Моменты распределения:** Среднее, дисперсия, асимметрия, эксцесс
- **Квантили:** Медиана, квартили, процентили
- **Корреляции:** Линейные и нелинейные зависимости
- **Автокорреляции:** Зависимости во времени

**Плюсы статистических признаков:**
- Математическая обоснованность
- Универсальность применения
- Легкая интерпретация
- Стабильность к шуму

**Минусы статистических признаков:**
- Могут быть менее специфичными
- Требуют достаточного объема данных
- Могут не учитывать специфику финансовых данных
- Могут быть избыточными
```python
def create_statistical_features(df):
    """Создание статистических признаков"""
    
    # Скользящие средние
    for window in [5, 10, 20, 50]:
        df[f'SMA_{window}'] = df['Close'].rolling(window).mean()
        df[f'EMA_{window}'] = df['Close'].ewm(span=window).mean()
    
    # Волатильность
    df['Volatility_5'] = df['Close'].rolling(5).std()
    df['Volatility_20'] = df['Close'].rolling(20).std()
    
    # Момент
    df['Momentum_5'] = df['Close'] / df['Close'].shift(5)
    df['Momentum_10'] = df['Close'] / df['Close'].shift(10)
    
    # Rate of Change
    df['ROC_5'] = df['Close'].pct_change(5)
    df['ROC_10'] = df['Close'].pct_change(10)
    
    return df
```

### 3. Временные признаки

**Теория:** Временные признаки учитывают временную структуру данных и помогают выявить паттерны, связанные со временем. Они критичны для финансовых данных, которые имеют сильную временную зависимость.

**Почему временные признаки важны:**
- **Временная зависимость:** Финансовые данные сильно зависят от времени
- **Сезонность:** Многие паттерны повторяются во времени
- **Тренды:** Временные признаки помогают выявить тренды
- **Циклы:** Финансовые рынки имеют циклические паттерны

**Типы временных признаков:**
- **Лаги:** Значения в предыдущие моменты времени
- **Разности:** Изменения между моментами времени
- **Скользящие окна:** Статистики в окнах времени
- **Сезонные:** Признаки, связанные с сезонностью

**Плюсы временных признаков:**
- Учет временной структуры
- Выявление сезонных паттернов
- Улучшение предсказательной способности
- Более полное понимание данных

**Минусы временных признаков:**
- Могут создавать утечки данных
- Требуют осторожности при валидации
- Могут быть избыточными
- Сложность интерпретации
```python
def create_time_features(df):
    """Создание временных признаков"""
    
    # Лаги
    for lag in [1, 2, 3, 5, 10, 20]:
        df[f'Close_lag_{lag}'] = df['Close'].shift(lag)
        df[f'Volume_lag_{lag}'] = df['Volume'].shift(lag)
    
    # Разности
    for diff in [1, 2, 5, 10]:
        df[f'Close_diff_{diff}'] = df['Close'].diff(diff)
        df[f'Volume_diff_{diff}'] = df['Volume'].diff(diff)
    
    # Процентные изменения
    for period in [1, 2, 5, 10]:
        df[f'Close_pct_{period}'] = df['Close'].pct_change(period)
        df[f'Volume_pct_{period}'] = df['Volume'].pct_change(period)
    
    return df
```

### 4. Интерактивные признаки

**Теория:** Интерактивные признаки создаются путем комбинирования существующих признаков и помогают выявить сложные нелинейные зависимости. Они особенно важны для финансовых данных, где многие паттерны являются результатом взаимодействия различных факторов.

**Почему интерактивные признаки важны:**
- **Нелинейные зависимости:** Финансовые данные часто имеют нелинейные зависимости
- **Синергия:** Комбинация признаков может дать больше информации
- **Контекст:** Интерактивные признаки учитывают контекст
- **Сложность:** Помогают моделировать сложные паттерны

**Типы интерактивных признаков:**
- **Произведения:** Умножение признаков
- **Отношения:** Деление признаков
- **Степени:** Возведение в степень
- **Логические:** Логические комбинации

**Плюсы интерактивных признаков:**
- Выявление нелинейных зависимостей
- Улучшение предсказательной способности
- Учет контекста
- Более полное моделирование

**Минусы интерактивных признаков:**
- Могут создавать избыточность
- Сложность интерпретации
- Риск переобучения
- Высокие вычислительные затраты
```python
def create_interaction_features(df):
    """Создание интерактивных признаков"""
    
    # RSI * MACD
    df['RSI_MACD'] = df['RSI'] * df['MACD']
    
    # Volume * Price Change
    df['Volume_Price_Change'] = df['Volume'] * df['Close'].pct_change()
    
    # Bollinger Band Position
    df['BB_Position'] = (df['Close'] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])
    
    # Price vs Moving Averages
    df['Price_vs_SMA20'] = df['Close'] / df['SMA_20']
    df['Price_vs_SMA50'] = df['Close'] / df['SMA_50']
    
    # Volume vs Average
    df['Volume_vs_Avg'] = df['Volume'] / df['Volume'].rolling(20).mean()
    
    return df
```

## Специализированные признаки для торговли

### 1. Ценовые паттерны
```python
def create_price_patterns(df):
    """Создание признаков ценовых паттернов"""
    
    # Doji
    df['Doji'] = (abs(df['Open'] - df['Close']) <= 0.1 * (df['High'] - df['Low'])).astype(int)
    
    # Hammer
    df['Hammer'] = ((df['Close'] - df['Low']) > 2 * (df['Open'] - df['Close'])) & \
                   ((df['High'] - df['Close']) <= 0.1 * (df['Close'] - df['Low']))
    
    # Engulfing
    df['Bullish_Engulfing'] = (df['Close'] > df['Open']) & \
                             (df['Close'].shift(1) < df['Open'].shift(1)) & \
                             (df['Open'] < df['Close'].shift(1)) & \
                             (df['Close'] > df['Open'].shift(1))
    
    return df
```

### 2. Объемные признаки
```python
def create_volume_features(df):
    """Создание объемных признаков"""
    
    # Volume Rate of Change
    df['Volume_ROC'] = df['Volume'].pct_change()
    
    # Volume Moving Average
    df['Volume_SMA'] = df['Volume'].rolling(20).mean()
    df['Volume_EMA'] = df['Volume'].ewm(span=20).mean()
    
    # Volume vs Price
    df['Volume_Price_Correlation'] = df['Volume'].rolling(20).corr(df['Close'])
    
    # On-Balance Volume
    df['OBV'] = (df['Volume'] * np.where(df['Close'] > df['Close'].shift(1), 1, 
                                       np.where(df['Close'] < df['Close'].shift(1), -1, 0))).cumsum()
    
    return df
```

### 3. Волатильность признаки
```python
def create_volatility_features(df):
    """Создание признаков волатильности"""
    
    # Historical Volatility
    df['HV_5'] = df['Close'].rolling(5).std() * np.sqrt(252)
    df['HV_20'] = df['Close'].rolling(20).std() * np.sqrt(252)
    
    # Average True Range
    df['ATR'] = calculate_atr(df['High'], df['Low'], df['Close'])
    
    # Volatility Ratio
    df['Vol_Ratio'] = df['HV_5'] / df['HV_20']
    
    # Volatility Percentile
    df['Vol_Percentile'] = df['HV_20'].rolling(100).rank(pct=True)
    
    return df

def calculate_atr(high, low, close, window=14):
    """Расчет Average True Range"""
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window).mean()
    return atr
```

## Признаки для разных таймфреймов

### 1. Мультитаймфреймовые признаки
```python
def create_multitimeframe_features(df, timeframes=['1H', '4H', '1D']):
    """Создание мультитаймфреймовых признаков"""
    
    for tf in timeframes:
        # Resample для разных таймфреймов
        resampled = df.resample(tf).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        })
        
        # Создание признаков для каждого таймфрейма
        resampled[f'RSI_{tf}'] = calculate_rsi(resampled['Close'])
        resampled[f'MACD_{tf}'] = calculate_macd(resampled['Close'])[0]
        
        # Forward fill для синхронизации
        df[f'RSI_{tf}'] = resampled[f'RSI_{tf}'].reindex(df.index).fillna(method='ffill')
        df[f'MACD_{tf}'] = resampled[f'MACD_{tf}'].reindex(df.index).fillna(method='ffill')
    
    return df
```

### 2. Сезонные признаки
```python
def create_seasonal_features(df):
    """Создание сезонных признаков"""
    
    # Временные признаки
    df['Hour'] = df.index.hour
    df['DayOfWeek'] = df.index.dayofweek
    df['DayOfMonth'] = df.index.day
    df['Month'] = df.index.month
    df['Quarter'] = df.index.quarter
    
    # Циклические признаки
    df['Hour_sin'] = np.sin(2 * np.pi * df['Hour'] / 24)
    df['Hour_cos'] = np.cos(2 * np.pi * df['Hour'] / 24)
    df['DayOfWeek_sin'] = np.sin(2 * np.pi * df['DayOfWeek'] / 7)
    df['DayOfWeek_cos'] = np.cos(2 * np.pi * df['DayOfWeek'] / 7)
    
    return df
```

## Отбор признаков

### 1. Корреляционный анализ
```python
def remove_correlated_features(df, threshold=0.95):
    """Удаление коррелированных признаков"""
    
    # Вычисление корреляционной матрицы
    corr_matrix = df.select_dtypes(include=[np.number]).corr().abs()
    
    # Нахождение пар с высокой корреляцией
    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    
    # Удаление признаков с высокой корреляцией
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > threshold)]
    
    return df.drop(columns=to_drop)
```

### 2. Важность признаков
```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression

def select_important_features(X, y, k=20):
    """Отбор важных признаков"""
    
    # Random Forest важность
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    feature_importance = rf.feature_importances_
    
    # F-тест
    selector = SelectKBest(score_func=f_regression, k=k)
    X_selected = selector.fit_transform(X, y)
    
    return X_selected, selector.get_support()
```

## Автоматическая инженерия признаков

### 1. FeatureTools
```python
import featuretools as ft

def automated_feature_engineering(df):
    """Автоматическая инженерия признаков с FeatureTools"""
    
    # Создание EntitySet
    es = ft.EntitySet(id="trading_data")
    es = es.add_dataframe(
        dataframe_name="trades",
        dataframe=df,
        index="timestamp",
        time_index="timestamp"
    )
    
    # Создание признаков
    feature_matrix, feature_defs = ft.dfs(
        entityset=es,
        target_dataframe_name="trades",
        max_depth=2,
        verbose=True
    )
    
    return feature_matrix, feature_defs
```

### 2. TSFresh
```python
from tsfresh import extract_features, select_features
from tsfresh.utilities.dataframe_functions import impute

def extract_time_series_features(df):
    """Извлечение признаков временных рядов"""
    
    # Извлечение признаков
    extracted_features = extract_features(
        df, 
        column_id="id", 
        column_sort="timestamp",
        default_fc_parameters=tsfresh.feature_extraction.settings.ComprehensiveFCParameters()
    )
    
    # Импутация пропущенных значений
    extracted_features = impute(extracted_features)
    
    return extracted_features
```

## Практический пример

```python
def create_comprehensive_features(df):
    """Создание комплексных признаков для торговли"""
    
    # 1. Технические индикаторы
    df = create_technical_indicators(df)
    
    # 2. Статистические признаки
    df = create_statistical_features(df)
    
    # 3. Временные признаки
    df = create_time_features(df)
    
    # 4. Интерактивные признаки
    df = create_interaction_features(df)
    
    # 5. Ценовые паттерны
    df = create_price_patterns(df)
    
    # 6. Объемные признаки
    df = create_volume_features(df)
    
    # 7. Волатильность признаки
    df = create_volatility_features(df)
    
    # 8. Сезонные признаки
    df = create_seasonal_features(df)
    
    # 9. Удаление коррелированных признаков
    df = remove_correlated_features(df)
    
    return df

# Использование
enhanced_data = create_comprehensive_features(original_data)
print(f"Создано {enhanced_data.shape[1]} признаков")
```

## Следующие шаги

После создания признаков переходите к:
- **[05_model_training.md](05_model_training.md)** - Обучение моделей
- **[06_backtesting.md](06_backtesting.md)** - Бэктестинг

## Ключевые выводы

1. **Качество признаков** важнее количества
2. **Доменные знания** критически важны
3. **Автоматизация** может помочь, но не заменить экспертизу
4. **Валидация** признаков обязательна
5. **Интерпретируемость** признаков важна

---

**Важно:** Хорошие признаки - это основа успешной ML-модели. Инвестируйте время в их создание!
