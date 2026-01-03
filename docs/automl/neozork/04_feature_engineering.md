# 04. 🔧 Инженерия признаков

**Goal:** Научиться создавать эффективные признаки for ML-моделей in финансовых данных.

## Необходимые библиотеки and импорты

**Theory:** Перед началом работы with инженерией признаков необходимо импортировать все необходимые библиотеки. in финансовом машинном обучении мы Use специализированные библиотеки for работы with временными рядами, техническими индикаторами and статистическими вычислениями.

**Почему важно правильно настроить импорты:**

- **Совместимость:** Правильные версии библиотек обеспечивают стабильность
- **Производительность:** Оптимизированные библиотеки ускоряют вычисления
- **Функциональность:** Специализированные библиотеки предоставляют необходимые functions
- **Отладка:** Правильные импорты упрощают поиск ошибок

```python
# Основные библиотеки for работы with data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Библиотеки for технических indicators
import talib
from scipy import stats
from scipy.signal import find_peaks

# Библиотеки for machine learning
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, classification_Report

# Библиотеки for автоматической инженерии признаков
import featuretools as ft
from tsfresh import extract_features, select_features
from tsfresh.utilities.dataframe_functions import impute
import tsfresh.feature_extraction.Settings

# Библиотеки for визуализации
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# configuration отображения
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
plt.style.Use('seaborn-v0_8')
sns.set_palette("husl")

print("✅ Все библиотеки успешно импортированы!")
print(f"📊 Pandas Version: {pd.__version__}")
print(f"🔢 NumPy Version: {np.__version__}")
print(f"📈 Matplotlib Version: {plt.matplotlib.__version__}")
```

## create testsых данных

**Theory:** for демонстрации инженерии признаков нам нужны реалистичные финансовые data. Мы создадим синтетические data, которые имитируют реальные рыночные условия, including тренды, волатильность, сезонность and шум.

**Почему синтетические data полезны:**
- **Контролируемость:** Мы знаем истинные паттерны in данных
- **Воспроизводимость:** Результаты можно повторить
- **Безопасность:** not нужно использовать реальные торговые data
- **Гибкость:** Можно тестировать различные сценарии

```python
def create_sample_trading_data(n_days=1000, start_date='2020-01-01'):
 """
 create синтетических торговых данных for демонстрации инженерии признаков

 parameters:
 - n_days: количество дней данных
 - start_date: начальная дата

 Возвращает:
 - dataFrame with OHLCV данными
 """
 np.random.seed(42) # for воспроизводимости

 # create временного indexа
 dates = pd.date_range(start=start_date, periods=n_days, freq='D')

 # Базовые parameters
 initial_price = 100.0
 trend = 0.0001 # Небольшой восходящий тренд
 volatility = 0.02 # 2% дневная волатильность

 # Генерация цен
 returns = np.random.normal(trend, volatility, n_days)
 prices = initial_price * np.exp(np.cumsum(returns))

 # create OHLCV данных
 data = []
 for i, (date, price) in enumerate(zip(dates, prices)):
 # add внутридневной волатильности
 intraday_vol = np.random.uniform(0.005, 0.015)

 # Open (открытие дня)
 open_price = price * (1 + np.random.normal(0, intraday_vol/2))

 # High (максимум дня)
 high_price = max(open_price, price) * (1 + np.random.uniform(0, intraday_vol))

 # Low (минимум дня)
 low_price = min(open_price, price) * (1 - np.random.uniform(0, intraday_vol))

 # Close (закрытие дня)
 close_price = price

 # Volume (объем торгов)
 base_volume = 1000000
 volume_multiplier = 1 + np.random.uniform(-0.5, 0.5)
 volume = int(base_volume * volume_multiplier * (1 + abs(returns[i]) * 10))

 data.append({
 'Date': date,
 'Open': round(open_price, 2),
 'High': round(high_price, 2),
 'Low': round(low_price, 2),
 'Close': round(close_price, 2),
 'Volume': volume
 })

 df = pd.dataFrame(data)
 df.set_index('Date', inplace=True)

 # add сезонности (например, еженедельные паттерны)
 df['DayOfWeek'] = df.index.dayofweek
 weekly_effect = np.sin(2 * np.pi * df['DayOfWeek'] / 7) * 0.01
 df['Close'] = df['Close'] * (1 + weekly_effect)

 return df

# create testsых данных
print("🔄 create синтетических торговых данных...")
sample_data = create_sample_trading_data(n_days=1000)
print(f"✅ Создано {len(sample_data)} дней данных")
print(f"📅 Период: {sample_data.index[0].strftime('%Y-%m-%d')} - {sample_data.index[-1].strftime('%Y-%m-%d')}")
print(f"💰 Цена: {sample_data['Close'].iloc[0]:.2f} → {sample_data['Close'].iloc[-1]:.2f}")
print(f"📊 Средний объем: {sample_data['Volume'].mean():,.0f}")
print("\n📋 Первые 5 строк данных:")
print(sample_data.head())
```

## Что такое инженерия признаков?

**Theory:** Инженерия признаков - это фундаментальный процесс in машинном обучении, который заключается in создании, трансформации and отборе признаков for улучшения производительности ML-моделей. in финансовой сфере это особенно критично, так как качество признаков напрямую влияет on точность торговых сигналов.

**Инженерия признаков** - это процесс создания новых признаков из существующих данных for улучшения производительности ML-моделей.

**Почему инженерия признаков критична for финансовых систем:**
- **Финансовые data сложны:** Требуют специальной обработки for выявления паттернов
- **Высокие риски:** Плохие признаки могут привести к значительным потерям
- **Конкурентное преимущество:** Качественные признаки дают преимущество on рынке
- **Регуляторные требования:** Финансовые регуляторы требуют прозрачности признаков

### Почему это важно?

**Theory:** Качество признаков является определяющим фактором успеха ML-моделей. Исследования показывают, что качественные признаки могут улучшить производительность модели больше, чем увеличение объема данных or сложности алгоритма.

- **Качество признаков** > **Количество данных**
 - **Почему:** Хорошие признаки содержат больше информации о целевой переменной
 - **Плюсы:** Более эффективное использование данных, лучшая интерпретируемость
 - **Disadvantages:** Требует экспертных знаний, больше времени on разработку

- **Правильные признаки** могут удвоить точность модели
 - **Почему:** Релевантные признаки напрямую связаны with целевой переменной
 - **Плюсы:** Значительное improve производительности, снижение рисков
 - **Disadvantages:** Сложность определения релевантных признаков

- **Плохие признаки** могут испортить даже лучшие алгоритмы
 - **Почему:** Шум in приsignх передается in модель and ухудшает её производительность
 - **Плюсы:** Понимание важности качества данных
 - **Disadvantages:** Необходимость тщательной валидации признаков

**Дополнительные аспекты важности:**
- **Интерпретируемость:** Хорошие признаки легко интерпретировать
- **Стабильность:** Качественные признаки стабильны во времени
- **Scalability:** Хорошие признаки Workingют on разных данных
- **Робастность:** Качественные признаки устойчивы к выбросам

## Типы признаков

**Theory:** Признаки in финансовых ML-моделях можно классифицировать on различным критериям. Понимание типов признаков критично for создания эффективных моделей and предотвращения ошибок.

### 1. Technical индикаторы

**Theory:** Technical индикаторы - это математические преобразования ценовых данных, которые помогают выявить паттерны and тренды. Они основаны on многолетнем опыте технических аналитиков and являются стандартом in финансовой индустрии.

**Почему Technical индикаторы важны:**
- **Проверенность временем:** Многолетний опыт использования
- **Стандартизация:** Универсальные метрики for Analysis
- **Интерпретируемость:** Легко понимать and объяснять
- **Эффективность:** Доказанная эффективность in торговле

**Типы технических indicators:**
- **Трендовые:** SMA, EMA, MACD - показывают направление тренда
- **Осцилляторы:** RSI, Stochastic - показывают перекупленность/перепроданность
- **Волатильность:** Bollinger Bands, ATR - показывают волатильность
- **Объемные:** OBV, VWAP - учитывают объем торгов

**Плюсы технических indicators:**
- Проверенная эффективность
- Стандартизированные метрики
- Легкая интерпретация
- Широкая поддержка in инструментах

**Минусы технических indicators:**
- Могут быть запаздывающими
- Могут генерировать ложные сигналы
- Требуют Settings параметров
- Могут быть избыточными
```python
def calculate_rsi(prices, window=14):
 """
 Расчет Relative Strength index (RSI)

 Theory: RSI - это осциллятор, который измеряет скорость and изменение ценовых движений.
 Значения from 0 to 100, где:
 - RSI > 70: перекупленность (возможен разворот вниз)
 - RSI < 30: перепроданность (возможен разворот вверх)
 - RSI = 50: нейтральная зона

 Формула: RSI = 100 - (100 / (1 + RS))
 где RS = средний прирост / средний убыток за период

 parameters:
 - prices: Series цен закрытия
 - window: период расчета (on умолчанию 14)

 Возвращает:
 - Series with значениями RSI
 """
 delta = prices.diff()
 gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
 loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

 # Избегаем деления on ноль
 rs = gain / loss.replace(0, np.inf)
 rsi = 100 - (100 / (1 + rs))

 return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
 """
 Расчет MACD (Moving Average Convergence Divergence)

 Theory: MACD - это трендовый индикатор, который показывает связь между двумя
 экспоненциальными скользящими средними. Состоит из трех компонентов:
 - MACD линия: EMA(fast) - EMA(slow)
 - signal линия: EMA(MACD)
 - Histogram: MACD - signal

 Сигналы:
 - Пересечение MACD and signal: смена тренда
 - Дивергенция: расхождение между ценой and MACD
 - Нулевая линия: пересечение указывает on смену тренда

 parameters:
 - prices: Series цен закрытия
 - fast: период быстрой EMA (on умолчанию 12)
 - slow: период медленной EMA (on умолчанию 26)
 - signal: период сигнальной линии (on умолчанию 9)

 Возвращает:
 - tuple: (macd_line, signal_line, histogram)
 """
 ema_fast = prices.ewm(span=fast).mean()
 ema_slow = prices.ewm(span=slow).mean()
 macd_line = ema_fast - ema_slow
 signal_line = macd_line.ewm(span=signal).mean()
 histogram = macd_line - signal_line

 return macd_line, signal_line, histogram

def calculate_bollinger_bands(prices, window=20, num_std=2):
 """
 Расчет полос Боллинджера (Bollinger Bands)

 Theory: Полосы Боллинджера состоят из трех линий:
 - Средняя линия: SMA(period)
 - Верхняя полоса: SMA + (std * num_std)
 - Нижняя полоса: SMA - (std * num_std)

 Использование:
 - Цена касается верхней полосы: возможен разворот вниз
 - Цена касается нижней полосы: возможен разворот вверх
 - Сжатие полос: низкая волатильность, возможен прорыв
 - Расширение полос: высокая волатильность

 parameters:
 - prices: Series цен закрытия
 - window: период for SMA (on умолчанию 20)
 - num_std: количество стандартных отклонений (on умолчанию 2)

 Возвращает:
 - tuple: (upper_band, lower_band, middle_band)
 """
 middle_band = prices.rolling(window=window).mean()
 std = prices.rolling(window=window).std()
 upper_band = middle_band + (std * num_std)
 lower_band = middle_band - (std * num_std)

 return upper_band, lower_band, middle_band

def calculate_stochastic(high, low, close, k_window=14, d_window=3):
 """
 Расчет стохастического осциллятора (Stochastic Oscillator)

 Theory: Стохастик измеряет позицию текущей цены относительно диапазона
 цен за определенный период. Состоит из двух линий:
 - %K: (Close - Lowest Low) / (Highest High - Lowest Low) * 100
 - %D: SMA(%K) - сглаженная версия %K

 Интерпретация:
 - %K > 80: перекупленность
 - %K < 20: перепроданность
 - Пересечение %K and %D: торговые сигналы

 parameters:
 - high: Series максимальных цен
 - low: Series минимальных цен
 - close: Series цен закрытия
 - k_window: период for %K (on умолчанию 14)
 - d_window: период for %D (on умолчанию 3)

 Возвращает:
 - tuple: (stoch_k, stoch_d)
 """
 lowest_low = low.rolling(window=k_window).min()
 highest_high = high.rolling(window=k_window).max()

 stoch_k = ((close - lowest_low) / (highest_high - lowest_low)) * 100
 stoch_d = stoch_k.rolling(window=d_window).mean()

 return stoch_k, stoch_d

def calculate_atr(high, low, close, window=14):
 """
 Расчет Average True Range (ATR)

 Theory: ATR измеряет волатильность рынка, показывая средний диапазон
 движения цены за определенный период. Используется for:
 - Определения размера стоп-лосса
 - Оценки волатильности
 - Фильтрации слабых сигналов

 True Range = max(High-Low, |High-PrevClose|, |Low-PrevClose|)
 ATR = SMA(True Range)

 parameters:
 - high: Series максимальных цен
 - low: Series минимальных цен
 - close: Series цен закрытия
 - window: период for SMA (on умолчанию 14)

 Возвращает:
 - Series with значениями ATR
 """
 tr1 = high - low
 tr2 = abs(high - close.shift(1))
 tr3 = abs(low - close.shift(1))

 tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
 atr = tr.rolling(window=window).mean()

 return atr

def create_Technical_indicators(df):
 """
 create полного набора технических indicators

 Theory: Technical индикаторы помогают выявить паттерны in ценовых данных
 and генерировать торговые сигналы. Мы Creating разнообразные индикаторы for
 покрытия различных аспектов рыночного поведения:
 - Трендовые индикаторы (SMA, EMA, MACD)
 - Осцилляторы (RSI, Stochastic)
 - Волатильность (Bollinger Bands, ATR)
 - Объемные (OBV)

 parameters:
 - df: dataFrame with OHLCV данными

 Возвращает:
 - dataFrame with добавленными техническими индикаторами
 """
 print("🔄 create технических indicators...")

 # RSI (Relative Strength index)
 df['RSI'] = calculate_rsi(df['Close'])
 df['RSI_oversold'] = (df['RSI'] < 30).astype(int)
 df['RSI_overbought'] = (df['RSI'] > 70).astype(int)

 # MACD (Moving Average Convergence Divergence)
 macd_line, signal_line, histogram = calculate_macd(df['Close'])
 df['MACD'] = macd_line
 df['MACD_signal'] = signal_line
 df['MACD_Histogram'] = histogram
 df['MACD_Bullish'] = (macd_line > signal_line).astype(int)
 df['MACD_Bearish'] = (macd_line < signal_line).astype(int)

 # Bollinger Bands
 bb_upper, bb_lower, bb_middle = calculate_bollinger_bands(df['Close'])
 df['BB_Upper'] = bb_upper
 df['BB_lower'] = bb_lower
 df['BB_Middle'] = bb_middle
 df['BB_Width'] = (bb_upper - bb_lower) / bb_middle
 df['BB_Position'] = (df['Close'] - bb_lower) / (bb_upper - bb_lower)
 df['BB_Squeeze'] = (df['BB_Width'] < df['BB_Width'].rolling(20).mean()).astype(int)

 # Stochastic Oscillator
 stoch_k, stoch_d = calculate_stochastic(df['High'], df['Low'], df['Close'])
 df['Stoch_K'] = stoch_k
 df['Stoch_D'] = stoch_d
 df['Stoch_Oversold'] = (stoch_k < 20).astype(int)
 df['Stoch_Overbought'] = (stoch_k > 80).astype(int)

 # ATR (Average True Range)
 df['ATR'] = calculate_atr(df['High'], df['Low'], df['Close'])
 df['ATR_Percentile'] = df['ATR'].rolling(100).rank(pct=True)

 # Simple Moving Averages
 for window in [5, 10, 20, 50, 200]:
 df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
 df[f'Price_vs_SMA_{window}'] = df['Close'] / df[f'SMA_{window}']

 # Exponential Moving Averages
 for window in [5, 10, 20, 50]:
 df[f'EMA_{window}'] = df['Close'].ewm(span=window).mean()
 df[f'Price_vs_EMA_{window}'] = df['Close'] / df[f'EMA_{window}']

 # On-Balance Volume (OBV)
 df['OBV'] = (df['Volume'] * np.where(df['Close'] > df['Close'].shift(1), 1,
 np.where(df['Close'] < df['Close'].shift(1), -1, 0))).cumsum()

 # Williams %R
 df['Williams_R'] = ((df['High'].rolling(14).max() - df['Close']) /
 (df['High'].rolling(14).max() - df['Low'].rolling(14).min())) * -100

 # Commodity Channel index (CCI)
 typical_price = (df['High'] + df['Low'] + df['Close']) / 3
 sma_tp = typical_price.rolling(20).mean()
 mad = typical_price.rolling(20).apply(lambda x: np.mean(np.abs(x - x.mean())))
 df['CCI'] = (typical_price - sma_tp) / (0.015 * mad)

 print(f"✅ Создано {len([col for col in df.columns if col not in ['Open', 'High', 'Low', 'Close', 'Volume', 'DayOfWeek']])} технических indicators")

 return df

# Демонстрация создания технических indicators
print("\n" + "="*60)
print("🔧 ДЕМОНСТРАЦИЯ: create технических indicators")
print("="*60)

# create indicators for testsых данных
df_with_indicators = create_Technical_indicators(sample_data.copy())

# Показ статистики on индикаторам
print(f"\n📊 Статистика on основным индикаторам:")
print(f"RSI: {df_with_indicators['RSI'].mean():.2f} ± {df_with_indicators['RSI'].std():.2f}")
print(f"MACD: {df_with_indicators['MACD'].mean():.4f} ± {df_with_indicators['MACD'].std():.4f}")
print(f"BB Position: {df_with_indicators['BB_Position'].mean():.3f} ± {df_with_indicators['BB_Position'].std():.3f}")
print(f"Stochastic K: {df_with_indicators['Stoch_K'].mean():.2f} ± {df_with_indicators['Stoch_K'].std():.2f}")

# Показ сигналов
print(f"\n📈 Торговые сигналы (последние 5 дней):")
recent_signals = df_with_indicators[['RSI_oversold', 'RSI_overbought', 'MACD_Bullish',
 'MACD_Bearish', 'Stoch_Oversold', 'Stoch_Overbought']].tail()
print(recent_signals)
```

### 2. Статистические признаки

**Theory:** Статистические признаки основаны on математических свойствах данных and помогают выявить скрытые паттерны. Они особенно полезны for ML-моделей, так как основаны on статистических принципах.

**Почему статистические признаки важны:**
- **Математическая обоснованность:** Основаны on статистических принципах
- **Универсальность:** Workingют on разных типах данных
- **Интерпретируемость:** Легко понимать and объяснять
- **Стабильность:** Менее подвержены шуму

**Типы статистических признаков:**
- **Моменты распределения:** Среднее, дисперсия, асимметрия, эксцесс
- **Квантили:** Медиана, квартили, процентили
- **Корреляции:** Линейные and нелинейные dependencies
- **Автокорреляции:** dependencies во времени

**Плюсы статистических признаков:**
- Математическая обоснованность
- Универсальность применения
- Легкая интерпретация
- Стабильность к шуму

**Минусы статистических признаков:**
- Могут быть менее специфичными
- Требуют достаточного объема данных
- Могут not учитывать специфику финансовых данных
- Могут быть избыточными
```python
def create_statistical_features(df):
 """
 create статистических признаков for финансовых данных

 Theory: Статистические признаки основаны on математических свойствах данных
 and помогают выявить скрытые паттерны. Они особенно полезны for ML-моделей,
 так как основаны on статистических принципах and менее подвержены шуму.

 Типы статистических признаков:
 1. Моменты распределения (среднее, дисперсия, асимметрия, эксцесс)
 2. Квантили (медиана, квартили, процентили)
 3. Корреляции (линейные and нелинейные dependencies)
 4. Автокорреляции (dependencies во времени)
 5. Скользящие статистики (средние, стандартные отклонения)

 parameters:
 - df: dataFrame with OHLCV данными

 Возвращает:
 - dataFrame with добавленными статистическими приsignми
 """
 print("🔄 create статистических признаков...")

 # 1. Скользящие средние (различные периоды)
 for window in [5, 10, 20, 50, 100]:
 df[f'SMA_{window}'] = df['Close'].rolling(window).mean()
 df[f'EMA_{window}'] = df['Close'].ewm(span=window).mean()

 # Отношение цены к скользящим средним
 df[f'Price_vs_SMA_{window}'] = df['Close'] / df[f'SMA_{window}']
 df[f'Price_vs_EMA_{window}'] = df['Close'] / df[f'EMA_{window}']

 # Отклонение from скользящих средних
 df[f'Deviation_SMA_{window}'] = (df['Close'] - df[f'SMA_{window}']) / df[f'SMA_{window}']
 df[f'Deviation_EMA_{window}'] = (df['Close'] - df[f'EMA_{window}']) / df[f'EMA_{window}']

 # 2. Волатильность (различные периоды)
 for window in [5, 10, 20, 50]:
 df[f'Volatility_{window}'] = df['Close'].rolling(window).std()
 df[f'Volatility_Annualized_{window}'] = df[f'Volatility_{window}'] * np.sqrt(252)

 # Относительная волатильность
 df[f'Rel_Volatility_{window}'] = df[f'Volatility_{window}'] / df[f'SMA_{window}']

 # Волатильность волатильности
 df[f'Vol_of_Vol_{window}'] = df[f'Volatility_{window}'].rolling(window).std()

 # 3. Моменты распределения
 for window in [10, 20, 50]:
 # Асимметрия (skewness) - мера асимметрии распределения
 df[f'Skewness_{window}'] = df['Close'].rolling(window).skew()

 # Эксцесс (kurtosis) - мера "остроты" распределения
 df[f'Kurtosis_{window}'] = df['Close'].rolling(window).kurt()

 # Медиана
 df[f'Median_{window}'] = df['Close'].rolling(window).median()

 # Отношение цены к медиане
 df[f'Price_vs_Median_{window}'] = df['Close'] / df[f'Median_{window}']

 # 4. Квантили and процентили
 for window in [20, 50]:
 for percentile in [25, 50, 75, 90, 95]:
 df[f'Percentile_{percentile}_{window}'] = df['Close'].rolling(window).quantile(percentile/100)

 # Позиция цены относительно процентилей
 df[f'Position_P{percentile}_{window}'] = (df['Close'] - df[f'Percentile_{percentile}_{window}']) / df[f'Percentile_{percentile}_{window}']

 # 5. Моментум and Rate of Change
 for period in [1, 2, 5, 10, 20]:
 # Простые изменения
 df[f'Price_Change_{period}'] = df['Close'] - df['Close'].shift(period)
 df[f'Price_Change_Pct_{period}'] = df['Close'].pct_change(period)

 # Логарифмические изменения (более стабильные)
 df[f'Log_Return_{period}'] = np.log(df['Close'] / df['Close'].shift(period))

 # Моментум (отношение текущей цены к цене N periods назад)
 df[f'Momentum_{period}'] = df['Close'] / df['Close'].shift(period)

 # Rate of Change (ROC)
 df[f'ROC_{period}'] = ((df['Close'] - df['Close'].shift(period)) / df['Close'].shift(period)) * 100

 # 6. Автокорреляции (dependencies во времени)
 for lag in [1, 2, 5, 10]:
 df[f'Autocorr_{lag}'] = df['Close'].rolling(50).apply(
 lambda x: x.autocorr(lag=lag) if len(x) > lag else np.nan
 )

 # 7. Скользящие максимумы and минимумы
 for window in [10, 20, 50]:
 df[f'Max_{window}'] = df['High'].rolling(window).max()
 df[f'Min_{window}'] = df['Low'].rolling(window).min()

 # Позиция цены in диапазоне
 df[f'Position_in_Range_{window}'] = (df['Close'] - df[f'Min_{window}']) / (df[f'Max_{window}'] - df[f'Min_{window}'])

 # Расстояние to максимума and минимума
 df[f'Distance_to_Max_{window}'] = (df[f'Max_{window}'] - df['Close']) / df['Close']
 df[f'Distance_to_Min_{window}'] = (df['Close'] - df[f'Min_{window}']) / df['Close']

 # 8. Статистики объема
 for window in [5, 10, 20]:
 df[f'Volume_SMA_{window}'] = df['Volume'].rolling(window).mean()
 df[f'Volume_Std_{window}'] = df['Volume'].rolling(window).std()
 df[f'Volume_vs_Avg_{window}'] = df['Volume'] / df[f'Volume_SMA_{window}']

 # Объем-взвешенные цены
 df[f'VWAP_{window}'] = (df['Close'] * df['Volume']).rolling(window).sum() / df['Volume'].rolling(window).sum()
 df[f'Price_vs_VWAP_{window}'] = df['Close'] / df[f'VWAP_{window}']

 # 9. Статистики размаха (High - Low)
 for window in [5, 10, 20]:
 df[f'Range_{window}'] = (df['High'] - df['Low']).rolling(window).mean()
 df[f'Range_Std_{window}'] = (df['High'] - df['Low']).rolling(window).std()
 df[f'Range_vs_Price_{window}'] = df[f'Range_{window}'] / df['Close']

 # 10. Z-скор (стандартизация)
 for window in [20, 50]:
 rolling_mean = df['Close'].rolling(window).mean()
 rolling_std = df['Close'].rolling(window).std()
 df[f'Z_Score_{window}'] = (df['Close'] - rolling_mean) / rolling_std

 # Абсолютный Z-скор
 df[f'Abs_Z_Score_{window}'] = np.abs(df[f'Z_Score_{window}'])

 # 11. Статистики изменений (изменения изменений)
 for period in [1, 2, 5]:
 df[f'Change_of_Change_{period}'] = df['Close'].pct_change().pct_change(period)
 df[f'acceleration_{period}'] = df['Close'].diff().diff(period)

 # 12. Скользящие корреляции
 for window in [20, 50]:
 # Корреляция между ценой and объемом
 df[f'Price_Volume_Corr_{window}'] = df['Close'].rolling(window).corr(df['Volume'])

 # Корреляция между ценой and волатильностью
 df[f'Price_Vol_Corr_{window}'] = df['Close'].rolling(window).corr(df[f'Volatility_20'])

 print(f"✅ Создано {len([col for col in df.columns if 'SMA_' in col or 'Volatility_' in col or 'Momentum_' in col or 'ROC_' in col or 'Skewness_' in col or 'Kurtosis_' in col or 'Percentile_' in col or 'Autocorr_' in col or 'Z_Score_' in col])} статистических признаков")

 return df

# Демонстрация создания статистических признаков
print("\n" + "="*60)
print("📊 ДЕМОНСТРАЦИЯ: create статистических признаков")
print("="*60)

# create статистических признаков
df_with_stats = create_statistical_features(sample_data.copy())

# Показ статистики on основным приsignм
print(f"\n📈 Статистика on основным приsignм:")
print(f"Волатильность (20 дней): {df_with_stats['Volatility_20'].mean():.4f} ± {df_with_stats['Volatility_20'].std():.4f}")
print(f"Z-Score (20 дней): {df_with_stats['Z_Score_20'].mean():.3f} ± {df_with_stats['Z_Score_20'].std():.3f}")
print(f"Асимметрия (20 дней): {df_with_stats['Skewness_20'].mean():.3f} ± {df_with_stats['Skewness_20'].std():.3f}")
print(f"Эксцесс (20 дней): {df_with_stats['Kurtosis_20'].mean():.3f} ± {df_with_stats['Kurtosis_20'].std():.3f}")

# Показ примеров признаков
print(f"\n📋 examples статистических признаков (последние 5 дней):")
stats_examples = df_with_stats[['Volatility_20', 'Z_Score_20', 'Skewness_20', 'Position_in_Range_20', 'Price_Volume_Corr_20']].tail()
print(stats_examples)
```

### 3. Временные признаки

**Theory:** Временные признаки учитывают временную структуру данных and помогают выявить паттерны, связанные со временем. Они критичны for финансовых данных, которые имеют сильную временную dependency.

**Почему временные признаки важны:**
- **Временная dependency:** Финансовые data сильно зависят from времени
- **Сезонность:** Многие паттерны повторяются во времени
- **Тренды:** Временные признаки помогают выявить тренды
- **Циклы:** Финансовые рынки имеют циклические паттерны

**Типы временных признаков:**
- **Лаги:** Значения in предыдущие моменты времени
- **Разности:** Изменения между моментами времени
- **Скользящие окна:** Статистики in окнах времени
- **Сезонные:** Признаки, связанные with сезонностью

**Плюсы временных признаков:**
- Учет temporary структуры
- Выявление сезонных паттернов
- improve предсказательной способности
- Более полное понимание данных

**Минусы временных признаков:**
- Могут создавать утечки данных
- Требуют осторожности при валидации
- Могут быть избыточными
- Сложность интерпретации
```python
def create_time_features(df):
 """
 create временных признаков for финансовых данных

 Theory: Временные признаки учитывают временную структуру данных and помогают
 выявить паттерны, связанные со временем. Они критичны for финансовых данных,
 которые имеют сильную временную dependency.

 Типы временных признаков:
 1. Лаги (lag features) - значения in предыдущие моменты времени
 2. Разности (difference features) - изменения между моментами времени
 3. Скользящие окна - статистики in окнах времени
 4. Сезонные признаки - связанные with сезонностью
 5. Циклические признаки - for учета циклов
 6. Трендовые признаки - for выявления трендов

 parameters:
 - df: dataFrame with OHLCV данными and Datetimeindex

 Возвращает:
 - dataFrame with добавленными временными приsignми
 """
 print("🔄 create временных признаков...")

 # 1. Лаги (lag features) - значения in предыдущие моменты времени
 for lag in [1, 2, 3, 5, 10, 20, 50]:
 df[f'Close_lag_{lag}'] = df['Close'].shift(lag)
 df[f'Volume_lag_{lag}'] = df['Volume'].shift(lag)
 df[f'High_lag_{lag}'] = df['High'].shift(lag)
 df[f'Low_lag_{lag}'] = df['Low'].shift(lag)

 # Отношения к лагам
 df[f'Close_vs_lag_{lag}'] = df['Close'] / df[f'Close_lag_{lag}']
 df[f'Volume_vs_lag_{lag}'] = df['Volume'] / df[f'Volume_lag_{lag}']

 # 2. Разности (difference features) - изменения между моментами времени
 for diff in [1, 2, 5, 10, 20]:
 df[f'Close_diff_{diff}'] = df['Close'].diff(diff)
 df[f'Volume_diff_{diff}'] = df['Volume'].diff(diff)
 df[f'High_diff_{diff}'] = df['High'].diff(diff)
 df[f'Low_diff_{diff}'] = df['Low'].diff(diff)

 # Нормализованные разности
 df[f'Close_diff_norm_{diff}'] = df[f'Close_diff_{diff}'] / df['Close'].shift(diff)
 df[f'Volume_diff_norm_{diff}'] = df[f'Volume_diff_{diff}'] / df['Volume'].shift(diff)

 # 3. Процентные изменения
 for period in [1, 2, 5, 10, 20]:
 df[f'Close_pct_{period}'] = df['Close'].pct_change(period)
 df[f'Volume_pct_{period}'] = df['Volume'].pct_change(period)
 df[f'High_pct_{period}'] = df['High'].pct_change(period)
 df[f'Low_pct_{period}'] = df['Low'].pct_change(period)

 # Логарифмические изменения (более стабильные)
 df[f'Close_log_{period}'] = np.log(df['Close'] / df['Close'].shift(period))
 df[f'Volume_log_{period}'] = np.log(df['Volume'] / df['Volume'].shift(period))

 # 4. Скользящие окна - статистики in окнах времени
 for window in [5, 10, 20, 50]:
 # Скользящие средние
 df[f'Close_MA_{window}'] = df['Close'].rolling(window).mean()
 df[f'Volume_MA_{window}'] = df['Volume'].rolling(window).mean()

 # Скользящие стандартные отклонения
 df[f'Close_Std_{window}'] = df['Close'].rolling(window).std()
 df[f'Volume_Std_{window}'] = df['Volume'].rolling(window).std()

 # Скользящие минимумы and максимумы
 df[f'Close_Min_{window}'] = df['Close'].rolling(window).min()
 df[f'Close_Max_{window}'] = df['Close'].rolling(window).max()
 df[f'Volume_Min_{window}'] = df['Volume'].rolling(window).min()
 df[f'Volume_Max_{window}'] = df['Volume'].rolling(window).max()

 # Позиция in скользящем окне
 df[f'Close_Position_{window}'] = (df['Close'] - df[f'Close_Min_{window}']) / (df[f'Close_Max_{window}'] - df[f'Close_Min_{window}'])
 df[f'Volume_Position_{window}'] = (df['Volume'] - df[f'Volume_Min_{window}']) / (df[f'Volume_Max_{window}'] - df[f'Volume_Min_{window}'])

 # 5. Сезонные признаки - связанные with сезонностью
 if hasattr(df.index, 'hour'):
 # Час дня (for внутридневных данных)
 df['Hour'] = df.index.hour
 df['Hour_sin'] = np.sin(2 * np.pi * df['Hour'] / 24)
 df['Hour_cos'] = np.cos(2 * np.pi * df['Hour'] / 24)

 # День недели
 df['DayOfWeek'] = df.index.dayofweek
 df['DayOfWeek_sin'] = np.sin(2 * np.pi * df['DayOfWeek'] / 7)
 df['DayOfWeek_cos'] = np.cos(2 * np.pi * df['DayOfWeek'] / 7)

 # День месяца
 df['DayOfMonth'] = df.index.day
 df['DayOfMonth_sin'] = np.sin(2 * np.pi * df['DayOfMonth'] / 31)
 df['DayOfMonth_cos'] = np.cos(2 * np.pi * df['DayOfMonth'] / 31)

 # Месяц
 df['Month'] = df.index.month
 df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
 df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)

 # Квартал
 df['Quarter'] = df.index.quarter
 df['Quarter_sin'] = np.sin(2 * np.pi * df['Quarter'] / 4)
 df['Quarter_cos'] = np.cos(2 * np.pi * df['Quarter'] / 4)

 # День года
 df['DayOfYear'] = df.index.dayofyear
 df['DayOfYear_sin'] = np.sin(2 * np.pi * df['DayOfYear'] / 365)
 df['DayOfYear_cos'] = np.cos(2 * np.pi * df['DayOfYear'] / 365)

 # 6. Циклические признаки - for учета циклов
 # Недельные циклы
 df['WeekOfYear'] = df.index.isocalendar().week
 df['WeekOfYear_sin'] = np.sin(2 * np.pi * df['WeekOfYear'] / 52)
 df['WeekOfYear_cos'] = np.cos(2 * np.pi * df['WeekOfYear'] / 52)

 # 7. Трендовые признаки - for выявления трендов
 # Линейный тренд (коэффициент наклона)
 for window in [20, 50, 100]:
 df[f'Trend_{window}'] = df['Close'].rolling(window).apply(
 lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) == window else np.nan
 )

 # R-квадрат тренда
 df[f'Trend_R2_{window}'] = df['Close'].rolling(window).apply(
 lambda x: np.corrcoef(range(len(x)), x)[0, 1]**2 if len(x) == window else np.nan
 )

 # 8. Временные интервалы
 # Дни with последнего максимума/минимума
 for window in [20, 50]:
 df[f'Days_Since_High_{window}'] = df['Close'].rolling(window).apply(
 lambda x: len(x) - 1 - x.argmax() if len(x) == window else np.nan
 )
 df[f'Days_Since_Low_{window}'] = df['Close'].rolling(window).apply(
 lambda x: len(x) - 1 - x.argmin() if len(x) == window else np.nan
 )

 # 9. Временные паттерны
 # Количество дней подряд роста/падения
 df['Consecutive_Up'] = (df['Close'] > df['Close'].shift(1)).groupby(
 (df['Close'] > df['Close'].shift(1) != (df['Close'] > df['Close'].shift(1)).shift()).cumsum()
 ).cumsum()

 df['Consecutive_Down'] = (df['Close'] < df['Close'].shift(1)).groupby(
 (df['Close'] < df['Close'].shift(1) != (df['Close'] < df['Close'].shift(1)).shift()).cumsum()
 ).cumsum()

 # 10. Временные статистики
 # Скользящие корреляции with временем
 for window in [20, 50]:
 df[f'Time_Corr_{window}'] = df['Close'].rolling(window).apply(
 lambda x: np.corrcoef(range(len(x)), x)[0, 1] if len(x) == window else np.nan
 )

 # 11. Временные индикаторы
 # Является ли день концом недели/месяца/квартала
 df['Is_Weekend'] = (df['DayOfWeek'] >= 5).astype(int)
 df['Is_Month_End'] = (df.index.is_month_end).astype(int)
 df['Is_Quarter_End'] = (df.index.is_quarter_end).astype(int)
 df['Is_Year_End'] = (df.index.is_year_end).astype(int)

 # 12. Временные разности (разности между различными временными точками)
 # Разность между текущим and предыдущим днем недели
 df['DayOfWeek_Diff'] = df['DayOfWeek'].diff()

 # Разность между текущим and предыдущим месяцем
 df['Month_Diff'] = df['Month'].diff()

 print(f"✅ Создано {len([col for col in df.columns if 'lag_' in col or 'diff_' in col or 'pct_' in col or 'MA_' in col or 'sin' in col or 'cos' in col or 'Trend_' in col or 'Consecutive_' in col or 'Is_' in col])} временных признаков")

 return df

# Демонстрация создания временных признаков
print("\n" + "="*60)
print("⏰ ДЕМОНСТРАЦИЯ: create временных признаков")
print("="*60)

# create временных признаков
df_with_time = create_time_features(sample_data.copy())

# Показ статистики on основным временным приsignм
print(f"\n📅 Статистика on временным приsignм:")
print(f"День недели (средний): {df_with_time['DayOfWeek'].mean():.2f}")
print(f"Месяц (средний): {df_with_time['Month'].mean():.2f}")
print(f"Квартал (средний): {df_with_time['Quarter'].mean():.2f}")

# Показ примеров временных признаков
print(f"\n📋 examples временных признаков (последние 5 дней):")
time_examples = df_with_time[['DayOfWeek', 'Month', 'Close_lag_1', 'Close_pct_1', 'Close_MA_20', 'Trend_20']].tail()
print(time_examples)
```

### 4. Интерактивные признаки

**Theory:** Интерактивные признаки создаются путем комбинирования существующих признаков and помогают выявить сложные нелинейные dependencies. Они особенно важны for финансовых данных, где многие паттерны являются результатом взаимодействия различных факторов.

**Почему интерактивные признаки важны:**
- **Нелинейные dependencies:** Финансовые data часто имеют нелинейные dependencies
- **Синергия:** Комбинация признаков может дать больше информации
- **Контекст:** Интерактивные признаки учитывают контекст
- **Сложность:** Помогают моделировать сложные паттерны

**Типы интерактивных признаков:**
- **Произведения:** Умножение признаков
- **Отношения:** Деление признаков
- **Степени:** Возведение in степень
- **Logsческие:** Logsческие комбинации

**Плюсы интерактивных признаков:**
- Выявление нелинейных dependencies
- improve предсказательной способности
- Учет контекста
- Более полное моделирование

**Минусы интерактивных признаков:**
- Могут создавать избыточность
- Сложность интерпретации
- Риск переобучения
- Высокие вычислительные затраты
```python
def create_interaction_features(df):
 """
 create интерактивных признаков for финансовых данных

 Theory: Интерактивные признаки создаются путем комбинирования существующих
 признаков and помогают выявить сложные нелинейные dependencies. Они особенно
 важны for финансовых данных, где многие паттерны являются результатом
 взаимодействия различных факторов.

 Типы интерактивных признаков:
 1. Произведения - умножение признаков
 2. Отношения - деление признаков
 3. Степени - возведение in степень
 4. Logsческие - Logsческие комбинации
 5. Полиномиальные - комбинации степеней
 6. Условные - признаки on basis условий

 parameters:
 - df: dataFrame with базовыми приsignми

 Возвращает:
 - dataFrame with добавленными интерактивными приsignми
 """
 print("🔄 create интерактивных признаков...")

 # 1. Произведения признаков (мультипликативные взаимодействия)
 # RSI * MACD - комбинация осциллятора and трендового индикатора
 if 'RSI' in df.columns and 'MACD' in df.columns:
 df['RSI_MACD'] = df['RSI'] * df['MACD']
 df['RSI_MACD_signal'] = df['RSI'] * df['MACD_signal']

 # Volume * Price Change - объем-взвешенные изменения цены
 df['Volume_Price_Change'] = df['Volume'] * df['Close'].pct_change()
 df['Volume_Price_Change_2'] = df['Volume'] * df['Close'].pct_change(2)

 # 2. Отношения признаков (делительные взаимодействия)
 # Bollinger Band Position - позиция цены in полосах
 if 'BB_Upper' in df.columns and 'BB_lower' in df.columns:
 df['BB_Position'] = (df['Close'] - df['BB_lower']) / (df['BB_Upper'] - df['BB_lower'])
 df['BB_Squeeze_Intensity'] = df['BB_Width'] / df['Close']

 # Price vs Moving Averages - отношения цены к скользящим средним
 for window in [20, 50, 200]:
 if f'SMA_{window}' in df.columns:
 df[f'Price_vs_SMA_{window}'] = df['Close'] / df[f'SMA_{window}']
 df[f'Price_vs_SMA_{window}_squared'] = (df[f'Price_vs_SMA_{window}'] - 1) ** 2

 # 3. Степенные признаки (полиномиальные взаимодействия)
 # Квадраты основных indicators
 if 'RSI' in df.columns:
 df['RSI_squared'] = df['RSI'] ** 2
 df['RSI_cubed'] = df['RSI'] ** 3
 df['RSI_sqrt'] = np.sqrt(df['RSI'])

 if 'MACD' in df.columns:
 df['MACD_squared'] = df['MACD'] ** 2
 df['MACD_abs'] = np.abs(df['MACD'])

 # 4. Logsческие комбинации
 # Комбинации условий перекупленности/перепроданности
 if 'RSI' in df.columns:
 df['RSI_Stoch_Overbought'] = ((df['RSI'] > 70) & (df['Stoch_K'] > 80)).astype(int)
 df['RSI_Stoch_Oversold'] = ((df['RSI'] < 30) & (df['Stoch_K'] < 20)).astype(int)

 # Комбинации трендовых сигналов
 if all(col in df.columns for col in ['SMA_20', 'SMA_50', 'SMA_200']):
 df['all_MA_Bullish'] = ((df['Close'] > df['SMA_20']) &
 (df['SMA_20'] > df['SMA_50']) &
 (df['SMA_50'] > df['SMA_200'])).astype(int)

 df['all_MA_Bearish'] = ((df['Close'] < df['SMA_20']) &
 (df['SMA_20'] < df['SMA_50']) &
 (df['SMA_50'] < df['SMA_200'])).astype(int)

 # 5. Условные признаки
 # Признаки on basis волатильности
 if 'Volatility_20' in df.columns:
 high_vol_mask = df['Volatility_20'] > df['Volatility_20'].rolling(50).quantile(0.8)
 df['High_Vol_RSI'] = df['RSI'].where(high_vol_mask, 0)
 df['Low_Vol_RSI'] = df['RSI'].where(~high_vol_mask, 0)

 # 6. Временные взаимодействия
 # Взаимодействие with днем недели
 if 'DayOfWeek' in df.columns:
 df['RSI_Weekend'] = df['RSI'] * (df['DayOfWeek'] >= 5).astype(int)
 df['Volume_Weekend'] = df['Volume'] * (df['DayOfWeek'] >= 5).astype(int)

 # 7. Объемно-ценовые взаимодействия
 # Объем-взвешенные индикаторы
 if 'Volume' in df.columns:
 df['Volume_Weighted_RSI'] = df['RSI'] * (df['Volume'] / df['Volume'].rolling(20).mean())
 df['Volume_Weighted_MACD'] = df['MACD'] * (df['Volume'] / df['Volume'].rolling(20).mean())

 # 8. Полиномиальные признаки
 # Взаимодействие RSI with его лагами
 if 'RSI' in df.columns:
 for lag in [1, 2, 5]:
 df[f'RSI_lag_{lag}'] = df['RSI'].shift(lag)
 df[f'RSI_RSI_lag_{lag}'] = df['RSI'] * df[f'RSI_lag_{lag}']
 df[f'RSI_minus_lag_{lag}'] = df['RSI'] - df[f'RSI_lag_{lag}']

 # 9. Статистические взаимодействия
 # Взаимодействие with Z-скором
 if 'Z_Score_20' in df.columns:
 df['RSI_Z_Score'] = df['RSI'] * df['Z_Score_20']
 df['MACD_Z_Score'] = df['MACD'] * df['Z_Score_20']

 # 10. Сложные комбинации
 # Комбинация тренда, волатильности and объема
 if all(col in df.columns for col in ['Trend_20', 'Volatility_20', 'Volume']):
 df['Trend_Vol_Volume'] = (df['Trend_20'] * df['Volatility_20'] *
 (df['Volume'] / df['Volume'].rolling(20).mean()))

 # Комбинация RSI, MACD and Bollinger Bands
 if all(col in df.columns for col in ['RSI', 'MACD', 'BB_Position']):
 df['RSI_MACD_BB'] = df['RSI'] * df['MACD'] * df['BB_Position']
 df['RSI_MACD_BB_norm'] = df['RSI_MACD_BB'] / df['RSI_MACD_BB'].rolling(20).std()

 print(f"✅ Создано {len([col for col in df.columns if any(x in col for x in ['_', 'Weighted', 'Combined', 'Interaction'])])} интерактивных признаков")

 return df

# Демонстрация создания интерактивных признаков
print("\n" + "="*60)
print("🔗 ДЕМОНСТРАЦИЯ: create интерактивных признаков")
print("="*60)

# create интерактивных признаков
df_with_interactions = create_interaction_features(df_with_time.copy())

# Показ статистики on интерактивным приsignм
print(f"\n📊 Статистика on интерактивным приsignм:")
interaction_cols = [col for col in df_with_interactions.columns if any(x in col for x in ['_', 'Weighted', 'Combined', 'Interaction'])]
print(f"Создано интерактивных признаков: {len(interaction_cols)}")

# Показ примеров интерактивных признаков
print(f"\n📋 examples интерактивных признаков (последние 5 дней):")
interaction_examples = df_with_interactions[['RSI_MACD', 'BB_Position', 'Price_vs_SMA_20', 'Volume_Weighted_RSI', 'RSI_Stoch_Overbought']].tail()
print(interaction_examples)
```

## Специализированные признаки for trading

**Theory:** Специализированные торговые признаки основаны on паттернах and стратегиях, которые используют профессиональные трейдеры. Эти признаки кодируют рыночную мудрость and проверенные временем торговые концепции.

**Почему специализированные признаки важны:**
- **Проверенность временем:** Основаны on многолетнем опыте трейдеров
- **Интерпретируемость:** Легко понимать and объяснять
- **Эффективность:** Доказанная эффективность in реальной торговле
- **Контекст:** Учитывают специфику финансовых рынков

### 1. Ценовые паттерны

**Theory:** Ценовые паттерны - это графические формации, которые повторяются on ценовых графиках and часто предвещают определенные движения цены. Они основаны on психоLogsи рынка and поведении участников.

```python
def create_price_patterns(df):
 """
 create признаков ценовых паттернов

 Theory: Ценовые паттерны отражают психоLogsю рынка and часто предвещают
 развороты or продолжения трендов. Они основаны on анализе соотношений
 между Open, High, Low, Close ценами.

 Типы паттернов:
 1. Разворотные - предвещают смену тренда
 2. Продолжающие - подтверждают текущий тренд
 3. Неопределенности - указывают on неопределенность рынка

 parameters:
 - df: dataFrame with OHLC данными

 Возвращает:
 - dataFrame with добавленными паттернами
 """
 print("🔄 create ценовых паттернов...")

 # 1. Разворотные паттерны

 # Doji - неопределенность рынка
 body_size = abs(df['Open'] - df['Close'])
 total_range = df['High'] - df['Low']
 df['Doji'] = (body_size <= 0.1 * total_range).astype(int)

 # Hammer - бычий разворот
 lower_shadow = df[['Open', 'Close']].min(axis=1) - df['Low']
 upper_shadow = df['High'] - df[['Open', 'Close']].max(axis=1)
 df['Hammer'] = ((lower_shadow > 2 * body_size) &
 (upper_shadow <= 0.1 * lower_shadow)).astype(int)

 # Shooting Star - медвежий разворот
 df['Shooting_Star'] = ((upper_shadow > 2 * body_size) &
 (lower_shadow <= 0.1 * upper_shadow)).astype(int)

 # Engulfing patterns
 # Бычий поглощение
 df['Bullish_Engulfing'] = ((df['Close'] > df['Open']) &
 (df['Close'].shift(1) < df['Open'].shift(1)) &
 (df['Open'] < df['Close'].shift(1)) &
 (df['Close'] > df['Open'].shift(1))).astype(int)

 # Медвежье поглощение
 df['Bearish_Engulfing'] = ((df['Close'] < df['Open']) &
 (df['Close'].shift(1) > df['Open'].shift(1)) &
 (df['Open'] > df['Close'].shift(1)) &
 (df['Close'] < df['Open'].shift(1))).astype(int)

 # 2. Продолжающие паттерны

 # Marubozu - сильный тренд
 df['Bullish_Marubozu'] = ((df['Close'] > df['Open']) &
 (df['Open'] == df['Low']) &
 (df['Close'] == df['High'])).astype(int)

 df['Bearish_Marubozu'] = ((df['Close'] < df['Open']) &
 (df['Open'] == df['High']) &
 (df['Close'] == df['Low'])).astype(int)

 # 3. Паттерны неопределенности

 # Spinning Top - неопределенность
 df['Spinning_Top'] = ((body_size < 0.3 * total_range) &
 (lower_shadow > body_size) &
 (upper_shadow > body_size)).astype(int)

 # 4. Комбинированные паттерны

 # Три белых солдата (3 дня роста подряд)
 df['Three_White_Soldiers'] = ((df['Close'] > df['Open']) &
 (df['Close'].shift(1) > df['Open'].shift(1)) &
 (df['Close'].shift(2) > df['Open'].shift(2)) &
 (df['Close'] > df['Close'].shift(1)) &
 (df['Close'].shift(1) > df['Close'].shift(2))).astype(int)

 # Три черных ворона (3 дня падения подряд)
 df['Three_Black_Crows'] = ((df['Close'] < df['Open']) &
 (df['Close'].shift(1) < df['Open'].shift(1)) &
 (df['Close'].shift(2) < df['Open'].shift(2)) &
 (df['Close'] < df['Close'].shift(1)) &
 (df['Close'].shift(1) < df['Close'].shift(2))).astype(int)

 # 5. Статистические паттерны

 # Высокая волатильность
 df['High_Volatility_Day'] = (total_range > total_range.rolling(20).quantile(0.8)).astype(int)

 # Низкая волатильность
 df['Low_Volatility_Day'] = (total_range < total_range.rolling(20).quantile(0.2)).astype(int)

 # 6. Паттерны размаха

 # Узкий диапазон
 df['Narrow_Range'] = (total_range < total_range.rolling(10).mean() * 0.5).astype(int)

 # Широкий диапазон
 df['Wide_Range'] = (total_range > total_range.rolling(10).mean() * 1.5).astype(int)

 print(f"✅ Создано {len([col for col in df.columns if col in ['Doji', 'Hammer', 'Shooting_Star', 'Bullish_Engulfing', 'Bearish_Engulfing', 'Bullish_Marubozu', 'Bearish_Marubozu', 'Spinning_Top', 'Three_White_Soldiers', 'Three_Black_Crows', 'High_Volatility_Day', 'Low_Volatility_Day', 'Narrow_Range', 'Wide_Range']])} ценовых паттернов")

 return df

# Демонстрация создания ценовых паттернов
print("\n" + "="*60)
print("📈 ДЕМОНСТРАЦИЯ: create ценовых паттернов")
print("="*60)

# create ценовых паттернов
df_with_patterns = create_price_patterns(sample_data.copy())

# Показ статистики on паттернам
print(f"\n📊 Статистика on ценовым паттернам:")
pattern_cols = [col for col in df_with_patterns.columns if col in ['Doji', 'Hammer', 'Shooting_Star', 'Bullish_Engulfing', 'Bearish_Engulfing']]
for col in pattern_cols:
 count = df_with_patterns[col].sum()
 print(f" {col}: {count} случаев ({count/len(df_with_patterns)*100:.1f}%)")

# Показ примеров паттернов
print(f"\n📋 examples паттернов (последние 10 дней):")
pattern_examples = df_with_patterns[['Doji', 'Hammer', 'Bullish_Engulfing', 'High_Volatility_Day', 'Narrow_Range']].tail(10)
print(pattern_examples)
```

### 2. Объемные признаки

**Theory:** Объемные признаки анализируют количество торгуемых акций/контрактов and помогают подтвердить силу ценовых движений. Объем часто предшествует изменениям цены and является важным индикатором настроений рынка.

```python
def create_volume_features(df):
 """
 create объемных признаков for финансовых данных

 Theory: Объем торгов является ключевым индикатором силы ценовых движений.
 Высокий объем подтверждает тренды, а низкий объем может указывать on
 слабость движения. Объемные индикаторы помогают:

 1. Подтвердить силу трендов
 2. Выявить дивергенции
 3. Определить точки входа/выхода
 4. Оценить ликвидность рынка

 parameters:
 - df: dataFrame with OHLCV данными

 Возвращает:
 - dataFrame with добавленными объемными приsignми
 """
 print("🔄 create объемных признаков...")

 # 1. Базовые объемные статистики

 # Volume Rate of Change - скорость изменения объема
 df['Volume_ROC'] = df['Volume'].pct_change()
 df['Volume_ROC_5'] = df['Volume'].pct_change(5)
 df['Volume_ROC_10'] = df['Volume'].pct_change(10)

 # Volume Moving Averages - скользящие средние объема
 for window in [5, 10, 20, 50]:
 df[f'Volume_SMA_{window}'] = df['Volume'].rolling(window).mean()
 df[f'Volume_EMA_{window}'] = df['Volume'].ewm(span=window).mean()

 # Отношение текущего объема к среднему
 df[f'Volume_vs_SMA_{window}'] = df['Volume'] / df[f'Volume_SMA_{window}']
 df[f'Volume_vs_EMA_{window}'] = df['Volume'] / df[f'Volume_EMA_{window}']

 # 2. Объемные индикаторы

 # On-Balance Volume (OBV) - накопительный объем
 price_change = df['Close'].diff()
 volume_direction = np.where(price_change > 0, 1,
 np.where(price_change < 0, -1, 0))
 df['OBV'] = (df['Volume'] * volume_direction).cumsum()

 # OBV Rate of Change
 df['OBV_ROC'] = df['OBV'].pct_change()
 df['OBV_ROC_5'] = df['OBV'].pct_change(5)

 # Volume Price Trend (VPT)
 df['VPT'] = (df['Volume'] * df['Close'].pct_change()).cumsum()

 # Money Flow index (MFI) - объемно-взвешенный RSI
 typical_price = (df['High'] + df['Low'] + df['Close']) / 3
 money_flow = typical_price * df['Volume']

 positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
 negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)

 positive_flow_ma = positive_flow.rolling(14).sum()
 negative_flow_ma = negative_flow.rolling(14).sum()

 mfi = 100 - (100 / (1 + positive_flow_ma / negative_flow_ma))
 df['MFI'] = mfi

 # 3. Объемно-ценовые соотношения

 # Volume vs Price Correlation - корреляция объема and цены
 for window in [10, 20, 50]:
 df[f'Volume_Price_Corr_{window}'] = df['Volume'].rolling(window).corr(df['Close'])
 df[f'Volume_Price_Corr_Change_{window}'] = df[f'Volume_Price_Corr_{window}'].pct_change()

 # Volume Weighted Average Price (VWAP)
 for window in [10, 20, 50]:
 typical_price = (df['High'] + df['Low'] + df['Close']) / 3
 df[f'VWAP_{window}'] = (typical_price * df['Volume']).rolling(window).sum() / df['Volume'].rolling(window).sum()
 df[f'Price_vs_VWAP_{window}'] = df['Close'] / df[f'VWAP_{window}']

 # 4. Объемные паттерны

 # Volume Spikes - всплески объема
 volume_mean = df['Volume'].rolling(20).mean()
 volume_std = df['Volume'].rolling(20).std()

 df['Volume_Spike'] = (df['Volume'] > volume_mean + 2 * volume_std).astype(int)
 df['Volume_Dry'] = (df['Volume'] < volume_mean - volume_std).astype(int)
 df['Volume_Extreme'] = (df['Volume'] > volume_mean + 3 * volume_std).astype(int)

 # Volume Breakout - прорыв объема
 df['Volume_Breakout'] = ((df['Volume'] > df['Volume'].rolling(20).quantile(0.8)) &
 (df['Close'] > df['High'].rolling(20).max().shift(1))).astype(int)

 # 5. Объемные дивергенции

 # Volume-Price Divergence
 price_trend = df['Close'].rolling(10).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
 volume_trend = df['Volume'].rolling(10).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])

 df['Volume_Price_Divergence'] = ((price_trend > 0) & (volume_trend < 0)).astype(int)
 df['Volume_Price_Convergence'] = ((price_trend > 0) & (volume_trend > 0)).astype(int)

 # 6. Объемные осцилляторы

 # Volume Oscillator
 df['Volume_Oscillator'] = df['Volume_EMA_10'] - df['Volume_EMA_20']
 df['Volume_Oscillator_Pct'] = df['Volume_Oscillator'] / df['Volume_EMA_20'] * 100

 # Volume Rate of Change Oscillator
 df['Volume_ROC_Oscillator'] = df['Volume_ROC'].rolling(5).mean() - df['Volume_ROC'].rolling(20).mean()

 # 7. Объемные процентили

 # Volume Percentile - позиция текущего объема
 for window in [20, 50, 100]:
 df[f'Volume_Percentile_{window}'] = df['Volume'].rolling(window).rank(pct=True)
 df[f'Volume_Percentile_Change_{window}'] = df[f'Volume_Percentile_{window}'].diff()

 # 8. Объемные тренды

 # Volume Trend Strength
 for window in [10, 20]:
 df[f'Volume_Trend_{window}'] = df['Volume'].rolling(window).apply(
 lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) == window else np.nan
 )
 df[f'Volume_Trend_R2_{window}'] = df['Volume'].rolling(window).apply(
 lambda x: np.corrcoef(range(len(x)), x)[0, 1]**2 if len(x) == window else np.nan
 )

 print(f"✅ Создано {len([col for col in df.columns if 'Volume' in col or 'OBV' in col or 'VPT' in col or 'MFI' in col or 'VWAP' in col])} объемных признаков")

 return df

# Демонстрация создания объемных признаков
print("\n" + "="*60)
print("📊 ДЕМОНСТРАЦИЯ: create объемных признаков")
print("="*60)

# create объемных признаков
df_with_volume = create_volume_features(sample_data.copy())

# Показ статистики on объемным приsignм
print(f"\n📈 Статистика on объемным приsignм:")
print(f"Средний объем: {df_with_volume['Volume'].mean():,.0f}")
print(f"Объемные всплески: {df_with_volume['Volume_Spike'].sum()} случаев")
print(f"Сухой объем: {df_with_volume['Volume_Dry'].sum()} случаев")
print(f"MFI (средний): {df_with_volume['MFI'].mean():.2f}")

# Показ примеров объемных признаков
print(f"\n📋 examples объемных признаков (последние 5 дней):")
volume_examples = df_with_volume[['Volume_ROC', 'Volume_vs_SMA_20', 'OBV_ROC', 'MFI', 'Volume_Spike']].tail()
print(volume_examples)
```

### 3. Волатильность признаки

**Theory:** Волатильность измеряет степень изменчивости цен and является ключевым фактором in оценке риска. Высокая волатильность указывает on нестабильность рынка, а низкая - on спокойствие. Волатильность имеет тенденцию к кластеризации and часто предшествует значительным движениям цены.

```python
def create_volatility_features(df):
 """
 create признаков волатильности for финансовых данных

 Theory: Волатильность является мерой риска and неопределенности on рынке.
 Она помогает:

 1. Оценить риск инвестиций
 2. Определить размер позиций
 3. Выявить периоды нестабильности
 4. Предсказать будущие движения цены
 5. Настроить торговые стратегии

 Типы волатильности:
 1. Историческая - on basis прошлых данных
 2. Подразумеваемая - из опционов
 3. Реализованная - фактическая волатильность
 4. Относительная - волатильность относительно цены

 parameters:
 - df: dataFrame with OHLCV данными

 Возвращает:
 - dataFrame with добавленными приsignми волатильности
 """
 print("🔄 create признаков волатильности...")

 # 1. Историческая волатильность (Historical Volatility)

 # Простая волатильность (стандартное отклонение)
 for window in [5, 10, 20, 50, 100]:
 df[f'HV_{window}'] = df['Close'].rolling(window).std()
 df[f'HV_Annualized_{window}'] = df[f'HV_{window}'] * np.sqrt(252)

 # Логарифмическая волатильность (более точная)
 log_returns = np.log(df['Close'] / df['Close'].shift(1))
 df[f'Log_HV_{window}'] = log_returns.rolling(window).std()
 df[f'Log_HV_Annualized_{window}'] = df[f'Log_HV_{window}'] * np.sqrt(252)

 # 2. Average True Range (ATR) - средний истинный диапазон

 # ATR for разных periods
 for window in [5, 10, 14, 20]:
 df[f'ATR_{window}'] = calculate_atr(df['High'], df['Low'], df['Close'], window)
 df[f'ATR_Percent_{window}'] = df[f'ATR_{window}'] / df['Close'] * 100

 # 3. Волатильность волатильности (Volatility of Volatility)

 # VoV - изменчивость самой волатильности
 for window in [10, 20]:
 df[f'VoV_{window}'] = df['HV_20'].rolling(window).std()
 df[f'VoV_Percentile_{window}'] = df[f'VoV_{window}'].rolling(50).rank(pct=True)

 # 4. Относительная волатильность

 # Volatility Ratio - отношение краткосрочной к долгосрочной волатильности
 df['Vol_Ratio_5_20'] = df['HV_5'] / df['HV_20']
 df['Vol_Ratio_10_50'] = df['HV_10'] / df['HV_50']
 df['Vol_Ratio_20_100'] = df['HV_20'] / df['HV_100']

 # Volatility Percentile - позиция текущей волатильности
 for window in [20, 50, 100]:
 df[f'Vol_Percentile_{window}'] = df['HV_20'].rolling(window).rank(pct=True)
 df[f'Vol_Percentile_Change_{window}'] = df[f'Vol_Percentile_{window}'].diff()

 # 5. Волатильность on basis размаха (Range-based Volatility)

 # Parkinson Volatility - использует High and Low
 for window in [5, 10, 20]:
 df[f'Parkinson_Vol_{window}'] = np.sqrt(
 (1 / (4 * np.log(2))) *
 (np.log(df['High'] / df['Low']) ** 2).rolling(window).mean()
 )

 # Garman-Klass Volatility - использует OHLC
 for window in [5, 10, 20]:
 df[f'GK_Vol_{window}'] = np.sqrt(
 (0.5 * (np.log(df['High'] / df['Low']) ** 2) -
 (2 * np.log(2) - 1) * (np.log(df['Close'] / df['Open']) ** 2)
 ).rolling(window).mean()
 )

 # 6. Волатильность on basis внутридневных данных

 # Realized Volatility - реализованная волатильность
 for window in [5, 10, 20]:
 df[f'Realized_Vol_{window}'] = np.sqrt(
 (df['Close'].pct_change() ** 2).rolling(window).sum()
 )

 # 7. Волатильность кластеров

 # Volatility Clustering - склонность волатильности к кластеризации
 for window in [10, 20]:
 vol_returns = df['HV_20'].pct_change()
 df[f'Vol_Clustering_{window}'] = vol_returns.rolling(window).std()
 df[f'Vol_Clustering_Autocorr_{window}'] = vol_returns.rolling(window).apply(
 lambda x: x.autocorr(lag=1) if len(x) > 1 else np.nan
 )

 # 8. Волатильность трендов

 # Volatility Trend - тренд волатильности
 for window in [10, 20]:
 df[f'Vol_Trend_{window}'] = df['HV_20'].rolling(window).apply(
 lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) == window else np.nan
 )
 df[f'Vol_Trend_R2_{window}'] = df['HV_20'].rolling(window).apply(
 lambda x: np.corrcoef(range(len(x)), x)[0, 1]**2 if len(x) == window else np.nan
 )

 # 9. Волатильность разрывов (Gaps)

 # Gap Volatility - волатильность разрывов
 gap = df['Open'] - df['Close'].shift(1)
 df['Gap_Volatility'] = gap.rolling(20).std()
 df['Gap_Volatility_Pct'] = df['Gap_Volatility'] / df['Close'] * 100

 # 10. Волатильность объемов

 # Volume-Weighted Volatility
 for window in [10, 20]:
 df[f'Volume_Weighted_Vol_{window}'] = (
 (df['Close'].pct_change() ** 2 * df['Volume']).rolling(window).sum() /
 df['Volume'].rolling(window).sum()
 )

 # 11. Волатильность паттернов

 # High Volatility Days - дни высокой волатильности
 df['High_Vol_Day'] = (df['HV_20'] > df['HV_20'].rolling(50).quantile(0.8)).astype(int)
 df['Low_Vol_Day'] = (df['HV_20'] < df['HV_20'].rolling(50).quantile(0.2)).astype(int)

 # Volatility Breakout - прорыв волатильности
 df['Vol_Breakout'] = (df['HV_20'] > df['HV_20'].rolling(20).max().shift(1)).astype(int)
 df['Vol_Breakdown'] = (df['HV_20'] < df['HV_20'].rolling(20).min().shift(1)).astype(int)

 # 12. Волатильность корреляций

 # Volatility-Price Correlation
 for window in [20, 50]:
 df[f'Vol_Price_Corr_{window}'] = df['HV_20'].rolling(window).corr(df['Close'])
 df[f'Vol_Volume_Corr_{window}'] = df['HV_20'].rolling(window).corr(df['Volume'])

 print(f"✅ Создано {len([col for col in df.columns if 'HV_' in col or 'ATR_' in col or 'Vol_' in col or 'VoV_' in col or 'Parkinson_' in col or 'GK_' in col or 'Realized_' in col])} признаков волатильности")

 return df

def calculate_atr(high, low, close, window=14):
 """
 Расчет Average True Range (ATR)

 Theory: ATR измеряет волатильность рынка, показывая средний диапазон
 движения цены за определенный период. Используется for:
 - Определения размера стоп-лосса
 - Оценки волатильности
 - Фильтрации слабых сигналов

 True Range = max(High-Low, |High-PrevClose|, |Low-PrevClose|)
 ATR = SMA(True Range)

 parameters:
 - high: Series максимальных цен
 - low: Series минимальных цен
 - close: Series цен закрытия
 - window: период for SMA (on умолчанию 14)

 Возвращает:
 - Series with значениями ATR
 """
 tr1 = high - low
 tr2 = abs(high - close.shift(1))
 tr3 = abs(low - close.shift(1))

 tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
 atr = tr.rolling(window=window).mean()

 return atr

# Демонстрация создания признаков волатильности
print("\n" + "="*60)
print("📊 ДЕМОНСТРАЦИЯ: create признаков волатильности")
print("="*60)

# create признаков волатильности
df_with_volatility = create_volatility_features(sample_data.copy())

# Показ статистики on волатильности
print(f"\n📈 Статистика on волатильности:")
print(f"Средняя волатильность (20 дней): {df_with_volatility['HV_20'].mean():.4f}")
print(f"ATR (14 дней): {df_with_volatility['ATR_14'].mean():.4f}")
print(f"Дни высокой волатильности: {df_with_volatility['High_Vol_Day'].sum()}")
print(f"Дни низкой волатильности: {df_with_volatility['Low_Vol_Day'].sum()}")

# Показ примеров признаков волатильности
print(f"\n📋 examples признаков волатильности (последние 5 дней):")
volatility_examples = df_with_volatility[['HV_20', 'ATR_14', 'Vol_Ratio_5_20', 'Vol_Percentile_50', 'High_Vol_Day']].tail()
print(volatility_examples)
```

## Признаки for разных Timeframes

**Theory:** МультиTimeframesый анализ является мощным инструментом in техническом анализе and машинном обучении. Он позволяет учитывать различные временные горизонты and выявлять паттерны, которые видны только on определенных Timeframes.

**Почему мультиTimeframesый анализ важен:**
- **Полная картина:** Разные Timeframeы показывают разные аспекты рынка
- **Подтверждение сигналов:** Сигналы on разных Timeframes подтверждают друг друга
- **Фильтрация шума:** Долгосрочные тренды фильтруют краткосрочный шум
- **Лучшие точки входа:** Комбинация Timeframes дает лучшие точки входа

### 1. МультиTimeframesые признаки

```python
def create_multiTimeframe_features(df, Timeframes=['1H', '4H', '1D']):
 """
 create мультиTimeframesых признаков

 Theory: МультиTimeframesый анализ позволяет учитывать различные
 временные горизонты in одном наборе признаков. Это помогает:

 1. Увидеть полную картину рынка
 2. Подтвердить сигналы on разных уровнях
 3. Фильтровать шум краткосрочных движений
 4. Найти лучшие точки входа and выхода

 Принципы:
 - Более высокие Timeframeы определяют общий тренд
 - Средние Timeframeы дают точки входа
 - Низкие Timeframeы обеспечивают точность

 parameters:
 - df: dataFrame with OHLCV данными
 - Timeframes: List Timeframes for Analysis

 Возвращает:
 - dataFrame with мультиTimeframesыми приsignми
 """
 print("🔄 create мультиTimeframesых признаков...")

 # create копии for работы
 result_df = df.copy()

 for tf in timeframes:
 print(f" 📊 Обработка Timeframe: {tf}")

 # Resample for разных Timeframes
 resampled = df.resample(tf).agg({
 'Open': 'first',
 'High': 'max',
 'Low': 'min',
 'Close': 'last',
 'Volume': 'sum'
 })

 # remove строк with NaN
 resampled = resampled.dropna()

 if len(resampled) < 50: # Минимум данных for indicators
 print(f" ⚠️ Недостаточно данных for Timeframe {tf}")
 continue

 # 1. Technical индикаторы for каждого Timeframe
 resampled[f'RSI_{tf}'] = calculate_rsi(resampled['Close'])
 macd_line, signal_line, histogram = calculate_macd(resampled['Close'])
 resampled[f'MACD_{tf}'] = macd_line
 resampled[f'MACD_signal_{tf}'] = signal_line
 resampled[f'MACD_Histogram_{tf}'] = histogram

 # Bollinger Bands
 bb_upper, bb_lower, bb_middle = calculate_bollinger_bands(resampled['Close'])
 resampled[f'BB_Upper_{tf}'] = bb_upper
 resampled[f'BB_lower_{tf}'] = bb_lower
 resampled[f'BB_Middle_{tf}'] = bb_middle
 resampled[f'BB_Position_{tf}'] = (resampled['Close'] - bb_lower) / (bb_upper - bb_lower)

 # Stochastic
 stoch_k, stoch_d = calculate_stochastic(resampled['High'], resampled['Low'], resampled['Close'])
 resampled[f'Stoch_K_{tf}'] = stoch_k
 resampled[f'Stoch_D_{tf}'] = stoch_d

 # 2. Скользящие средние
 for window in [10, 20, 50]:
 resampled[f'SMA_{window}_{tf}'] = resampled['Close'].rolling(window).mean()
 resampled[f'EMA_{window}_{tf}'] = resampled['Close'].ewm(span=window).mean()

 # 3. Волатильность
 resampled[f'Volatility_{tf}'] = resampled['Close'].rolling(20).std()
 resampled[f'ATR_{tf}'] = calculate_atr(resampled['High'], resampled['Low'], resampled['Close'])

 # 4. Объемные индикаторы
 resampled[f'Volume_SMA_{tf}'] = resampled['Volume'].rolling(20).mean()
 resampled[f'Volume_vs_Avg_{tf}'] = resampled['Volume'] / resampled[f'Volume_SMA_{tf}']

 # 5. Трендовые признаки
 resampled[f'Trend_{tf}'] = resampled['Close'].rolling(20).apply(
 lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) == 20 else np.nan
 )

 # 6. Synchronization with исходным Timeframeом
 for col in resampled.columns:
 if col not in ['Open', 'High', 'Low', 'Close', 'Volume']:
 # Forward fill for синхронизации
 result_df[col] = resampled[col].reindex(df.index).fillna(method='ffill')

 # 7. МежTimeframesые соотношения
 if 'RSI_1D' in result_df.columns and 'RSI_1H' in result_df.columns:
 result_df['RSI_Daily_vs_Hourly'] = result_df['RSI_1D'] / result_df['RSI_1H']
 result_df['RSI_Divergence'] = (result_df['RSI_1D'] > 70) & (result_df['RSI_1H'] < 30)

 if 'MACD_1D' in result_df.columns and 'MACD_1H' in result_df.columns:
 result_df['MACD_Daily_vs_Hourly'] = result_df['MACD_1D'] / result_df['MACD_1H']

 # 8. Трендовые согласованности
 trend_cols = [col for col in result_df.columns if 'Trend_' in col]
 if len(trend_cols) >= 2:
 result_df['Trend_Consistency'] = result_df[trend_cols].apply(
 lambda x: (x > 0).sum() if x.notna().all() else np.nan, axis=1
 )

 print(f"✅ Создано мультиTimeframesых признаков for {len(Timeframes)} Timeframes")

 return result_df

# Демонстрация создания мультиTimeframesых признаков
print("\n" + "="*60)
print("⏰ ДЕМОНСТРАЦИЯ: create мультиTimeframesых признаков")
print("="*60)

# create мультиTimeframesых признаков
df_multiTimeframe = create_multiTimeframe_features(sample_data.copy(), ['1D', '1W'])

# Показ статистики on мультиTimeframesым приsignм
print(f"\n📊 Статистика on мультиTimeframesым приsignм:")
multiTimeframe_cols = [col for col in df_multiTimeframe.columns if any(tf in col for tf in ['_1D', '_1W', '_1H', '_4H'])]
print(f"Создано мультиTimeframesых признаков: {len(multiTimeframe_cols)}")

# Показ примеров мультиTimeframesых признаков
print(f"\n📋 examples мультиTimeframesых признаков (последние 5 дней):")
multiTimeframe_examples = df_multiTimeframe[['RSI_1D', 'MACD_1D', 'RSI_1W', 'MACD_1W', 'Trend_Consistency']].tail()
print(multiTimeframe_examples)
```

### 2. Сезонные признаки

**Theory:** Сезонные признаки учитывают циклические паттерны in финансовых данных, связанные with временем. Финансовые рынки демонстрируют различные сезонные эффекты, которые могут быть использованы for улучшения предсказательной способности моделей.

```python
def create_seasonal_features(df):
 """
 create сезонных признаков for финансовых данных

 Theory: Сезонные признаки учитывают циклические паттерны in финансовых
 данных, связанные with временем. Финансовые рынки демонстрируют различные
 сезонные эффекты:

 1. Внутридневные паттерны (часы торгов)
 2. Еженедельные паттерны (дни недели)
 3. Месячные паттерны (дни месяца)
 4. Квартальные паттерны (сезоны)
 5. Годовые паттерны (месяцы года)

 parameters:
 - df: dataFrame with Datetimeindex

 Возвращает:
 - dataFrame with добавленными сезонными приsignми
 """
 print("🔄 create сезонных признаков...")

 # 1. Базовые временные признаки

 # Час дня (for внутридневных данных)
 if hasattr(df.index, 'hour'):
 df['Hour'] = df.index.hour
 df['Hour_sin'] = np.sin(2 * np.pi * df['Hour'] / 24)
 df['Hour_cos'] = np.cos(2 * np.pi * df['Hour'] / 24)

 # Периоды дня
 df['Morning'] = ((df['Hour'] >= 6) & (df['Hour'] < 12)).astype(int)
 df['Afternoon'] = ((df['Hour'] >= 12) & (df['Hour'] < 18)).astype(int)
 df['Evening'] = ((df['Hour'] >= 18) & (df['Hour'] < 24)).astype(int)
 df['Night'] = ((df['Hour'] >= 0) & (df['Hour'] < 6)).astype(int)

 # День недели
 df['DayOfWeek'] = df.index.dayofweek
 df['DayOfWeek_sin'] = np.sin(2 * np.pi * df['DayOfWeek'] / 7)
 df['DayOfWeek_cos'] = np.cos(2 * np.pi * df['DayOfWeek'] / 7)

 # День месяца
 df['DayOfMonth'] = df.index.day
 df['DayOfMonth_sin'] = np.sin(2 * np.pi * df['DayOfMonth'] / 31)
 df['DayOfMonth_cos'] = np.cos(2 * np.pi * df['DayOfMonth'] / 31)

 # Месяц
 df['Month'] = df.index.month
 df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
 df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)

 # Квартал
 df['Quarter'] = df.index.quarter
 df['Quarter_sin'] = np.sin(2 * np.pi * df['Quarter'] / 4)
 df['Quarter_cos'] = np.cos(2 * np.pi * df['Quarter'] / 4)

 # День года
 df['DayOfYear'] = df.index.dayofyear
 df['DayOfYear_sin'] = np.sin(2 * np.pi * df['DayOfYear'] / 365)
 df['DayOfYear_cos'] = np.cos(2 * np.pi * df['DayOfYear'] / 365)

 # 2. Специальные календарные признаки

 # Неделя года
 df['WeekOfYear'] = df.index.isocalendar().week
 df['WeekOfYear_sin'] = np.sin(2 * np.pi * df['WeekOfYear'] / 52)
 df['WeekOfYear_cos'] = np.cos(2 * np.pi * df['WeekOfYear'] / 52)

 # 3. Торговые дни and выходные

 # Выходные
 df['Is_Weekend'] = (df['DayOfWeek'] >= 5).astype(int)
 df['Is_Monday'] = (df['DayOfWeek'] == 0).astype(int)
 df['Is_Friday'] = (df['DayOfWeek'] == 4).astype(int)

 # Конец месяца/квартала/года
 df['Is_Month_End'] = (df.index.is_month_end).astype(int)
 df['Is_Quarter_End'] = (df.index.is_quarter_end).astype(int)
 df['Is_Year_End'] = (df.index.is_year_end).astype(int)

 # 4. Сезонные периоды

 # Времена года (for северного полушария)
 df['Spring'] = ((df['Month'] >= 3) & (df['Month'] <= 5)).astype(int)
 df['Summer'] = ((df['Month'] >= 6) & (df['Month'] <= 8)).astype(int)
 df['Autumn'] = ((df['Month'] >= 9) & (df['Month'] <= 11)).astype(int)
 df['Winter'] = ((df['Month'] == 12) | (df['Month'] <= 2)).astype(int)

 # 5. Финансовые сезоны

 # Квартальные Reportы (последний месяц квартала)
 df['Earnings_Season'] = ((df['Month'] % 3 == 0) & (df['DayOfMonth'] >= 15)).astype(int)

 # Январский эффект (первые дни января)
 df['January_Effect'] = ((df['Month'] == 1) & (df['DayOfMonth'] <= 15)).astype(int)

 # Летний спад (июль-август)
 df['Summer_Doldrums'] = ((df['Month'] >= 7) & (df['Month'] <= 8)).astype(int)

 # 6. Праздничные периоды

 # Рождественский период (декабрь)
 df['Holiday_Season'] = (df['Month'] == 12).astype(int)

 # 7. Сезонные статистики

 # Средние показатели on дням недели
 for col in ['Close', 'Volume']:
 if col in df.columns:
 for day in range(7):
 day_mask = df['DayOfWeek'] == day
 df[f'{col}_DayOfWeek_{day}_Mean'] = df[col].where(day_mask).rolling(50).mean()
 df[f'{col}_DayOfWeek_{day}_Std'] = df[col].where(day_mask).rolling(50).std()

 # 8. Сезонные де-трендинг

 # remove сезонных трендов
 for col in ['Close', 'Volume']:
 if col in df.columns:
 # Сезонное разложение (упрощенное)
 monthly_avg = df[col].groupby(df.index.month).transform('mean')
 df[f'{col}_Deseasonalized'] = df[col] - monthly_avg + df[col].mean()

 # 9. Сезонные индикаторы

 # Сезонная сила (изменчивость on сезонам)
 for season_col in ['Spring', 'Summer', 'Autumn', 'Winter']:
 if season_col in df.columns:
 season_mask = df[season_col] == 1
 if 'Close' in df.columns:
 df[f'Seasonal_Strength_{season_col}'] = df['Close'].where(season_mask).rolling(50).std()

 print(f"✅ Создано {len([col for col in df.columns if any(x in col for x in ['Hour', 'DayOfWeek', 'Month', 'Quarter', 'Season', 'Holiday', 'Deseasonalized'])])} сезонных признаков")

 return df

# Демонстрация создания сезонных признаков
print("\n" + "="*60)
print("📅 ДЕМОНСТРАЦИЯ: create сезонных признаков")
print("="*60)

# create сезонных признаков
df_seasonal = create_seasonal_features(sample_data.copy())

# Показ статистики on сезонным приsignм
print(f"\n📊 Статистика on сезонным приsignм:")
print(f"День недели (средний): {df_seasonal['DayOfWeek'].mean():.2f}")
print(f"Месяц (средний): {df_seasonal['Month'].mean():.2f}")
print(f"Выходные: {df_seasonal['Is_Weekend'].sum()} дней")
print(f"Конец месяца: {df_seasonal['Is_Month_End'].sum()} дней")

# Показ примеров сезонных признаков
print(f"\n📋 examples сезонных признаков (последние 5 дней):")
seasonal_examples = df_seasonal[['DayOfWeek', 'Month', 'Is_Weekend', 'Spring', 'Summer', 'Holiday_Season']].tail()
print(seasonal_examples)
```

## Отбор признаков

### 1. Корреляционный анализ
```python
def remove_correlated_features(df, threshold=0.95):
 """remove коррелированных признаков"""

 # Вычисление корреляционной матрицы
 corr_matrix = df.select_dtypes(include=[np.number]).corr().abs()

 # Нахождение пар with высокой корреляцией
 upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

 # remove признаков with высокой корреляцией
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
 """Автоматическая инженерия признаков with FeatureTools"""

 # create EntitySet
 es = ft.EntitySet(id="trading_data")
 es = es.add_dataframe(
 dataframe_name="trades",
 dataframe=df,
 index="timestamp",
 time_index="timestamp"
 )

 # create признаков
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
 default_fc_parameters=tsfresh.feature_extraction.Settings.ComprehensiveFCParameters()
 )

 # Импутация пропущенных значений
 extracted_features = impute(extracted_features)

 return extracted_features
```

## Полный рабочий example: Комплексная инженерия признаков

**Theory:** Теперь мы объединим все изученные техники инженерии признаков in один комплексный example. Это покажет, как правильно применять различные методы for создания эффективного набора признаков for финансового machine learning.

**Почему важен комплексный подход:**
- **Синергия:** Различные типы признаков дополняют друг друга
- **Робастность:** Разнообразие признаков повышает устойчивость модели
- **Интерпретируемость:** Различные типы признаков помогают понять поведение модели
- **Адаптивность:** Комплексный подход Workingет on разных типах данных

```python
def create_comprehensive_features(df):
 """
 create комплексных признаков for финансового machine learning

 Theory: Эта function объединяет все изученные техники инженерии признаков
 for создания максимально информативного набора признаков. Она включает:

 1. Technical индикаторы (RSI, MACD, Bollinger Bands, etc.)
 2. Статистические признаки (моменты, квантили, корреляции)
 3. Временные признаки (лаги, сезонность, тренды)
 4. Интерактивные признаки (комбинации признаков)
 5. Специализированные торговые признаки
 6. Отбор and clean признаков

 parameters:
 - df: dataFrame with OHLCV данными and Datetimeindex

 Возвращает:
 - dataFrame with комплексным набором признаков
 - Словарь with информацией о созданных приsignх
 """
 print("🚀 Начало комплексной инженерии признаков...")
 print("="*60)

 # Сохранение исходных данных
 original_columns = df.columns.toList()
 feature_info = {
 'original_features': len(original_columns),
 'Technical_indicators': 0,
 'statistical_features': 0,
 'time_features': 0,
 'interaction_features': 0,
 'trading_features': 0,
 'final_features': 0
 }

 # 1. Technical индикаторы
 print("📊 1. create технических indicators...")
 df = create_Technical_indicators(df)
 Technical_cols = [col for col in df.columns if col not in original_columns]
 feature_info['Technical_indicators'] = len(Technical_cols)
 print(f" ✅ Создано {len(Technical_cols)} технических indicators")

 # 2. Статистические признаки
 print("📈 2. create статистических признаков...")
 df = create_statistical_features(df)
 stats_cols = [col for col in df.columns if col not in original_columns + Technical_cols]
 feature_info['statistical_features'] = len(stats_cols)
 print(f" ✅ Создано {len(stats_cols)} статистических признаков")

 # 3. Временные признаки
 print("⏰ 3. create временных признаков...")
 df = create_time_features(df)
 time_cols = [col for col in df.columns if col not in original_columns + Technical_cols + stats_cols]
 feature_info['time_features'] = len(time_cols)
 print(f" ✅ Создано {len(time_cols)} временных признаков")

 # 4. Интерактивные признаки
 print("🔗 4. create интерактивных признаков...")
 df = create_interaction_features(df)
 interaction_cols = [col for col in df.columns if col not in original_columns + Technical_cols + stats_cols + time_cols]
 feature_info['interaction_features'] = len(interaction_cols)
 print(f" ✅ Создано {len(interaction_cols)} интерактивных признаков")

 # 5. Специализированные торговые признаки
 print("💰 5. create торговых признаков...")
 df = create_trading_features(df)
 trading_cols = [col for col in df.columns if col not in original_columns + Technical_cols + stats_cols + time_cols + interaction_cols]
 feature_info['trading_features'] = len(trading_cols)
 print(f" ✅ Создано {len(trading_cols)} торговых признаков")

 # 6. clean and отбор признаков
 print("🧹 6. clean and отбор признаков...")
 df_cleaned = clean_and_select_features(df)
 feature_info['final_features'] = len(df_cleaned.columns)
 print(f" ✅ Оставлено {len(df_cleaned.columns)} финальных признаков")

 print("="*60)
 print("🎉 Комплексная инженерия признаков завершена!")
 print(f"📊 Итого создано: {feature_info['final_features']} признаков")
 print(f" - Technical индикаторы: {feature_info['Technical_indicators']}")
 print(f" - Статистические признаки: {feature_info['statistical_features']}")
 print(f" - Временные признаки: {feature_info['time_features']}")
 print(f" - Интерактивные признаки: {feature_info['interaction_features']}")
 print(f" - Торговые признаки: {feature_info['trading_features']}")

 return df_cleaned, feature_info

def create_trading_features(df):
 """
 create специализированных торговых признаков

 Theory: Торговые признаки специфичны for финансовых рынков and включают
 паттерны, которые трейдеры используют for принятия решений.
 """
 print(" 🔄 create торговых признаков...")

 # Ценовые паттерны
 # Doji (маленькое тело свечи)
 df['Doji'] = (abs(df['Open'] - df['Close']) <= 0.1 * (df['High'] - df['Low'])).astype(int)

 # Hammer (молот)
 body = abs(df['Close'] - df['Open'])
 lower_shadow = df[['Open', 'Close']].min(axis=1) - df['Low']
 upper_shadow = df['High'] - df[['Open', 'Close']].max(axis=1)

 df['Hammer'] = ((lower_shadow > 2 * body) & (upper_shadow <= 0.1 * lower_shadow)).astype(int)

 # Engulfing patterns
 df['Bullish_Engulfing'] = ((df['Close'] > df['Open']) &
 (df['Close'].shift(1) < df['Open'].shift(1)) &
 (df['Open'] < df['Close'].shift(1)) &
 (df['Close'] > df['Open'].shift(1))).astype(int)

 df['Bearish_Engulfing'] = ((df['Close'] < df['Open']) &
 (df['Close'].shift(1) > df['Open'].shift(1)) &
 (df['Open'] > df['Close'].shift(1)) &
 (df['Close'] < df['Open'].shift(1))).astype(int)

 # Объемные признаки
 df['Volume_Spike'] = (df['Volume'] > df['Volume'].rolling(20).mean() * 2).astype(int)
 df['Volume_Dry'] = (df['Volume'] < df['Volume'].rolling(20).mean() * 0.5).astype(int)

 # Волатильность признаки
 df['High_Volatility'] = (df['Volatility_20'] > df['Volatility_20'].rolling(50).quantile(0.8)).astype(int)
 df['Low_Volatility'] = (df['Volatility_20'] < df['Volatility_20'].rolling(50).quantile(0.2)).astype(int)

 # Трендовые признаки
 df['Strong_Uptrend'] = ((df['Close'] > df['SMA_20']) &
 (df['SMA_20'] > df['SMA_50']) &
 (df['SMA_50'] > df['SMA_200'])).astype(int)

 df['Strong_Downtrend'] = ((df['Close'] < df['SMA_20']) &
 (df['SMA_20'] < df['SMA_50']) &
 (df['SMA_50'] < df['SMA_200'])).astype(int)

 return df

def clean_and_select_features(df, correlation_threshold=0.95, Missing_threshold=0.5):
 """
 clean and отбор признаков

 Theory: После создания большого количества признаков необходимо:
 1. Удалить признаки with большим количеством пропущенных значений
 2. Удалить коррелированные признаки
 3. Удалить константные признаки
 4. Удалить признаки with бесконечными значениями
 """
 print(" 🔄 clean and отбор признаков...")

 # 1. remove признаков with большим количеством пропущенных значений
 Missing_ratio = df.isnull().sum() / len(df)
 cols_to_drop = Missing_ratio[Missing_ratio > Missing_threshold].index
 df = df.drop(columns=cols_to_drop)
 print(f" 🗑️ Удалено {len(cols_to_drop)} признаков with >{Missing_threshold*100}% пропусков")

 # 2. remove константных признаков
 constant_cols = df.columns[df.nunique() <= 1]
 df = df.drop(columns=constant_cols)
 print(f" 🗑️ Удалено {len(constant_cols)} константных признаков")

 # 3. remove признаков with бесконечными значениями
 inf_cols = df.columns[df.isin([np.inf, -np.inf]).any()]
 df = df.drop(columns=inf_cols)
 print(f" 🗑️ Удалено {len(inf_cols)} признаков with бесконечными значениями")

 # 4. Заполнение оставшихся пропусков
 numeric_cols = df.select_dtypes(include=[np.number]).columns
 df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

 # 5. remove коррелированных признаков
 corr_matrix = df[numeric_cols].corr().abs()
 upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
 high_corr_cols = [column for column in upper_tri.columns if any(upper_tri[column] > correlation_threshold)]
 df = df.drop(columns=high_corr_cols)
 print(f" 🗑️ Удалено {len(high_corr_cols)} коррелированных признаков (>{correlation_threshold*100}%)")

 return df

# Демонстрация комплексной инженерии признаков
print("\n" + "="*80)
print("🚀 ДЕМОНСТРАЦИЯ: Комплексная инженерия признаков")
print("="*80)

# create комплексного набора признаков
enhanced_data, feature_info = create_comprehensive_features(sample_data.copy())

# Анализ результатов
print(f"\n📊 АНАЛИЗ РЕЗУЛЬТАТОВ:")
print(f"Исходных признаков: {feature_info['original_features']}")
print(f"Финальных признаков: {feature_info['final_features']}")
print(f"Коэффициент расширения: {feature_info['final_features'] / feature_info['original_features']:.1f}x")

# Показ примеров финальных признаков
print(f"\n📋 examples финальных признаков (последние 5 дней):")
final_examples = enhanced_data.select_dtypes(include=[np.number]).iloc[:, :10].tail()
print(final_examples)

# Статистика on типам признаков
print(f"\n📈 Статистика on типам признаков:")
print(f"Technical индикаторы: {feature_info['Technical_indicators']}")
print(f"Статистические признаки: {feature_info['statistical_features']}")
print(f"Временные признаки: {feature_info['time_features']}")
print(f"Интерактивные признаки: {feature_info['interaction_features']}")
print(f"Торговые признаки: {feature_info['trading_features']}")

# check качества данных
print(f"\n🔍 КАЧЕСТВО ДАННЫХ:")
print(f"Пропущенные значения: {enhanced_data.isnull().sum().sum()}")
print(f"Бесконечные значения: {np.isinf(enhanced_data.select_dtypes(include=[np.number])).sum().sum()}")
print(f"Константные признаки: {(enhanced_data.nunique() <= 1).sum()}")

print(f"\n✅ Комплексная инженерия признаков успешно завершена!")
print(f"📁 data готовы for обучения ML-моделей")
```

## Валидация and тестирование признаков

**Theory:** После создания признаков необходимо их валидировать, чтобы убедиться in их качестве and пригодности for machine learning.

```python
def validate_features(df, target_col='Close'):
 """
 Валидация созданных признаков

 Theory: Валидация признаков включает проверку:
 1. Качества данных (пропуски, выбросы, распределения)
 2. Статистических свойств (корреляции, стационарность)
 3. Информативности (важность for целевой переменной)
 4. Стабильности (изменения во времени)
 """
 print("🔍 Валидация признаков...")

 # 1. Базовая статистика
 print("\n📊 1. Базовая статистика:")
 print(f" Размер данных: {df.shape}")
 print(f" Пропущенные значения: {df.isnull().sum().sum()}")
 print(f" Бесконечные значения: {np.isinf(df.select_dtypes(include=[np.number])).sum().sum()}")

 # 2. Анализ корреляций
 print("\n📈 2. Анализ корреляций:")
 numeric_cols = df.select_dtypes(include=[np.number]).columns
 corr_matrix = df[numeric_cols].corr()

 # Найти высокие корреляции
 high_corr_pairs = []
 for i in range(len(corr_matrix.columns)):
 for j in range(i+1, len(corr_matrix.columns)):
 if abs(corr_matrix.iloc[i, j]) > 0.9:
 high_corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))

 print(f" Высококоррелированных пар (>0.9): {len(high_corr_pairs)}")

 # 3. Анализ важности признаков
 if target_col in df.columns:
 print("\n🎯 3. Анализ важности признаков:")

 # Подготовка данных
 feature_cols = [col for col in numeric_cols if col != target_col]
 X = df[feature_cols].fillna(0)
 y = df[target_col]

 # remove строк with пропусками in целевой переменной
 mask = ~y.isnull()
 X = X[mask]
 y = y[mask]

 if len(X) > 0:
 # Random Forest важность
 rf = RandomForestRegressor(n_estimators=100, random_state=42)
 rf.fit(X, y)

 # Топ-10 важных признаков
 feature_importance = pd.dataFrame({
 'feature': feature_cols,
 'importance': rf.feature_importances_
 }).sort_values('importance', ascending=False)

 print(" Топ-10 важных признаков:")
 for i, (_, row) in enumerate(feature_importance.head(10).iterrows()):
 print(f" {i+1:2d}. {row['feature']:<30} {row['importance']:.4f}")

 # 4. Анализ распределений
 print("\n📊 4. Анализ распределений:")
 for col in feature_cols[:5]: # Показываем только первые 5
 if col in df.columns:
 print(f" {col}:")
 print(f" Среднее: {df[col].mean():.4f}")
 print(f" Стд.откл: {df[col].std():.4f}")
 print(f" Мин: {df[col].min():.4f}")
 print(f" Макс: {df[col].max():.4f}")
 print(f" Асимметрия: {df[col].skew():.4f}")
 print(f" Эксцесс: {df[col].kurtosis():.4f}")

 return {
 'shape': df.shape,
 'Missing_values': df.isnull().sum().sum(),
 'infinite_values': np.isinf(df.select_dtypes(include=[np.number])).sum().sum(),
 'high_correlations': len(high_corr_pairs),
 'feature_importance': feature_importance if 'feature_importance' in locals() else None
 }

# Валидация созданных признаков
print("\n" + "="*60)
print("🔍 ВАЛИДАЦИЯ ПРИЗНАКОВ")
print("="*60)

validation_results = validate_features(enhanced_data)
```

## Следующие шаги

После создания and валидации признаков переходите к:
- **[05_model_training.md](05_model_training.md)** - Обучение ML-моделей
- **[06_backtesting.md](06_backtesting.md)** - Бэктестинг стратегий

## Ключевые выводы

1. **Качество признаков** важнее количества
2. **Доменные знания** критически важны for создания эффективных признаков
3. **Автоматизация** может помочь, но not заменить экспертизу
4. **Валидация** признаков обязательна перед обучением моделей
5. **Интерпретируемость** признаков важна for понимания модели
6. **Комплексный подход** дает лучшие результаты, чем отдельные техники

---

**Важно:** Хорошие признаки - это основа успешной ML-модели. Инвестируйте время in их create and валидацию!
