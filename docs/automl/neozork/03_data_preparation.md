# 03. 📊 Подготовка данных

**Цель:** Научиться правильно подготавливать и очищать финансовые данные для ML-моделей.

## Зачем нужна качественная подготовка данных?

**Качество данных = Качество модели**

Плохие данные приводят к:
- Ложным сигналам
- Переобучению
- Нестабильным результатам
- Потере денег

## Типы финансовых данных

### 1. OHLCV данные
```python
# Структура OHLCV данных
data = {
    'Open': [100, 101, 102],    # Цена открытия
    'High': [105, 106, 107],    # Максимальная цена
    'Low': [99, 100, 101],      # Минимальная цена
    'Close': [104, 105, 106],   # Цена закрытия
    'Volume': [1000, 1200, 1100] # Объем торгов
}
```

### 2. Процентные изменения
```python
# Более стабильные для ML
data['price_change'] = data['Close'].pct_change()
data['volume_change'] = data['Volume'].pct_change()
```

### 3. Технические индикаторы
```python
# RSI, MACD, Bollinger Bands
data['RSI'] = calculate_rsi(data['Close'])
data['MACD'] = calculate_macd(data['Close'])
data['BB_Upper'] = calculate_bollinger_upper(data['Close'])
```

## Очистка данных

### 1. Удаление дубликатов
```python
def remove_duplicates(df):
    """Удаление дубликатов"""
    return df.drop_duplicates()
```

### 2. Обработка пропущенных значений
```python
def handle_missing_values(df):
    """Обработка пропущенных значений"""
    # Forward fill для цен
    df['Close'] = df['Close'].fillna(method='ffill')
    
    # Interpolation для объемов
    df['Volume'] = df['Volume'].interpolate()
    
    return df
```

### 3. Удаление выбросов
```python
def remove_outliers(df, threshold=3):
    """Удаление выбросов с помощью Z-score"""
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_columns:
        z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
        df = df[z_scores < threshold]
    
    return df
```

## Создание признаков

### 1. Технические индикаторы
```python
def create_technical_indicators(df):
    """Создание технических индикаторов"""
    
    # Скользящие средние
    df['SMA_5'] = df['Close'].rolling(5).mean()
    df['SMA_20'] = df['Close'].rolling(20).mean()
    df['SMA_50'] = df['Close'].rolling(50).mean()
    
    # Экспоненциальные средние
    df['EMA_12'] = df['Close'].ewm(span=12).mean()
    df['EMA_26'] = df['Close'].ewm(span=26).mean()
    
    # RSI
    df['RSI'] = calculate_rsi(df['Close'])
    
    # MACD
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
    
    return df
```

### 2. Статистические признаки
```python
def create_statistical_features(df):
    """Создание статистических признаков"""
    
    # Волатильность
    df['Volatility'] = df['Close'].rolling(20).std()
    
    # Момент
    df['Momentum'] = df['Close'] / df['Close'].shift(10)
    
    # Rate of Change
    df['ROC'] = df['Close'].pct_change(10)
    
    return df
```

### 3. Временные признаки
```python
def create_time_features(df):
    """Создание временных признаков"""
    
    # Лаги
    for lag in [1, 2, 3, 5, 10]:
        df[f'Close_lag_{lag}'] = df['Close'].shift(lag)
    
    # Разности
    for diff in [1, 2, 5]:
        df[f'Close_diff_{diff}'] = df['Close'].diff(diff)
    
    return df
```

## Нормализация данных

### 1. StandardScaler
```python
from sklearn.preprocessing import StandardScaler

def standardize_data(df):
    """Стандартизация данных"""
    scaler = StandardScaler()
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
    return df, scaler
```

### 2. MinMaxScaler
```python
from sklearn.preprocessing import MinMaxScaler

def normalize_data(df):
    """Нормализация данных"""
    scaler = MinMaxScaler()
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
    return df, scaler
```

## Создание целевых переменных

### 1. Классификация направления
```python
def create_direction_target(df, horizon=1):
    """Создание целевой переменной для направления"""
    future_price = df['Close'].shift(-horizon)
    current_price = df['Close']
    
    # Процентное изменение
    price_change = (future_price - current_price) / current_price
    
    # Классификация
    target = pd.cut(
        price_change,
        bins=[-np.inf, -0.001, 0.001, np.inf],
        labels=[0, 1, 2],  # 0=down, 1=hold, 2=up
        include_lowest=True
    )
    
    return target.astype(int)
```

### 2. Регрессия для цены
```python
def create_price_target(df, horizon=1):
    """Создание целевой переменной для цены"""
    return df['Close'].shift(-horizon)
```

## Валидация данных

### 1. Проверка качества
```python
def validate_data_quality(df):
    """Валидация качества данных"""
    
    # Проверка на пропущенные значения
    missing_ratio = df.isnull().sum() / len(df)
    
    # Проверка на выбросы
    outlier_ratio = (np.abs(df.select_dtypes(include=[np.number]) - 
                           df.select_dtypes(include=[np.number]).mean()) > 
                     3 * df.select_dtypes(include=[np.number]).std()).sum() / len(df)
    
    return {
        'missing_ratio': missing_ratio,
        'outlier_ratio': outlier_ratio
    }
```

### 2. Проверка стабильности
```python
def check_data_stability(df):
    """Проверка стабильности данных"""
    
    # Проверка на стационарность
    from statsmodels.tsa.stattools import adfuller
    
    adf_result = adfuller(df['Close'].dropna())
    
    return {
        'adf_statistic': adf_result[0],
        'p_value': adf_result[1],
        'is_stationary': adf_result[1] < 0.05
    }
```

## Сохранение данных

### 1. Parquet формат
```python
def save_data_parquet(df, filename):
    """Сохранение в Parquet формате"""
    df.to_parquet(filename, compression='snappy')
```

### 2. HDF5 формат
```python
def save_data_hdf5(df, filename):
    """Сохранение в HDF5 формате"""
    df.to_hdf(filename, 'data', mode='w', format='table')
```

## Практический пример

```python
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import StandardScaler

def prepare_trading_data(symbol, period='2y'):
    """Полная подготовка данных для торговли"""
    
    # 1. Загрузка данных
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period)
    
    # 2. Очистка
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = remove_outliers(df)
    
    # 3. Создание признаков
    df = create_technical_indicators(df)
    df = create_statistical_features(df)
    df = create_time_features(df)
    
    # 4. Создание целевой переменной
    df['target'] = create_direction_target(df)
    
    # 5. Удаление NaN
    df = df.dropna()
    
    # 6. Нормализация
    scaler = StandardScaler()
    feature_columns = df.select_dtypes(include=[np.number]).columns
    df[feature_columns] = scaler.fit_transform(df[feature_columns])
    
    return df, scaler

# Использование
data, scaler = prepare_trading_data('BTC-USD')
print(f"Подготовлено {len(data)} записей с {data.shape[1]} признаками")
```

## Следующие шаги

После подготовки данных переходите к:
- **[04_feature_engineering.md](04_feature_engineering.md)** - Инженерия признаков
- **[05_model_training.md](05_model_training.md)** - Обучение моделей

## Ключевые выводы

1. **Качество данных** критически важно для ML
2. **Очистка** должна быть тщательной
3. **Признаки** должны быть релевантными
4. **Нормализация** улучшает обучение
5. **Валидация** предотвращает ошибки

---

**Важно:** Потратьте время на качественную подготовку данных - это окупится в долгосрочной перспективе.
