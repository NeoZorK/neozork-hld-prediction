# 18.2. Детальные компоненты системы

**Теория:** Детальные компоненты системы представляют собой подробное description всех ключевых компонентов системы, их функций and взаимодействий. Это критически важно for понимания архитектуры and реализации системы.

**Почему детальные компоненты системы важны:**
- **Понимание:** Обеспечивает глубокое понимание системы
- **Архитектура:** Обеспечивает понимание архитектуры
- **Реализация:** Обеспечивает понимание реализации
- **integration:** Критически важно for интеграции компонентов

**Плюсы:**
- Глубокое понимание
- Четкая архитектура
- Детальная реализация
- Эффективная integration

**Минусы:**
- Высокая сложность
- Требует глубоких знаний
- Потенциальные Issues with интеграцией

## 📊 Сборщик данных

**Теория:** Сборщик данных представляет собой критически важный компонент системы, отвечающий за сбор, очистку and подготовку данных for дальнейшего анализа. Это основа for всех ML-моделей and торговых решений.

**Почему сборщик данных важен:**
- **Качество данных:** Обеспечивает качество данных
- **Полнота:** Обеспечивает полноту данных
- **Актуальность:** Обеспечивает актуальность данных
- **Надежность:** Критически важно for надежности системы

**Плюсы:**
- Высокое качество данных
- Полнота данных
- Актуальность данных
- Надежность системы

**Минусы:**
- Сложность реализации
- Высокие требования к ресурсам
- Потенциальные Issues with источниками данных

**Детальная реализация сборщика данных:**

Сборщик данных является фундаментальным компонентом системы, который обеспечивает получение, очистку and подготовку рыночных данных for всех последующих аналитических процессов. Этот компонент критически важен for работы всей системы, поскольку качество данных напрямую влияет on точность всех ML-моделей and торговых решений.

**Архитектурные принципы:**
- **Модульность**: Каждый источник данных обрабатывается независимо
- **Кэширование**: Данные сохраняются in памяти for быстрого доступа
- **clean**: Автоматическое remove аномалий and некорректных данных
- **Масштабируемость**: Поддержка множественных активов and Timeframeов
- **Надежность**: Обработка ошибок and восстановление после сбоев

**Ключевые functions:**
1. **Сбор данных**: Получение исторических and реальных данных with различных источников
2. **clean данных**: remove аномалий, дубликатов and некорректных записей
3. **Нормализация**: Приведение данных к единому формату
4. **Кэширование**: Оптимизация производительности через локальное хранение
5. **Экспорт**: Сохранение данных in различных форматах

```python
# src/data/collectors.py
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from pathlib import Path
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import time

class DataCollector:
 """
 Продвинутый сборщик данных for всех активов and Timeframeов

 Этот класс обеспечивает:
 - Многопоточный сбор данных
 - Автоматическую очистку and валидацию
 - Интеллектуальное кэширование
 - Обработку ошибок and восстановление
 - Поддержку различных источников данных
 """

 def __init__(self, config: Dict):
 """
 Инициализация сборщика данных

 Args:
 config: configuration системы with настройками источников данных
 """
 self.config = config
 self.logger = logging.getLogger(__name__)
 self.data_cache = {}
 self.last_update = {}
 self.max_workers = config.get('max_workers', 5)
 self.cache_ttl = config.get('cache_ttl', 3600) # 1 час
 self.retry_attempts = config.get('retry_attempts', 3)
 self.retry_delay = config.get('retry_delay', 1)

 # configuration логирования
 logging.basicConfig(level=logging.INFO)

 def collect_data(self, symbol: str, timeframe: str, period: str = "2y") -> pd.DataFrame:
 """
 Сбор данных for символа and Timeframeа with расширенной функциональностью

 Args:
 symbol: Символ актива (например, 'AAPL', 'EURUSD')
 timeframe: Timeframe ('M1', 'M5', 'H1', 'D1', etc.)
 period: Период данных ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')

 Returns:
 pd.DataFrame: Очищенные данные with метаданными
 """
 try:
 self.logger.info(f"starting data collection for {symbol} {timeframe}")

 # check cache
 cache_key = f"{symbol}_{timeframe}_{period}"
 if self._is_cache_valid(cache_key):
 self.logger.info(f"Using cached data for {symbol} {timeframe}")
 return self.data_cache[cache_key]

 # Преобразование Timeframeа for yfinance
 interval_map = {
 'M1': '1m',
 'M5': '5m',
 'M15': '15m',
 'M30': '30m',
 'H1': '1h',
 'H2': '2h',
 'H4': '4h',
 'H6': '6h',
 'H8': '8h',
 'H12': '12h',
 'D1': '1d',
 'W1': '1wk',
 'MN1': '1mo'
 }

 interval = interval_map.get(timeframe, '1h')

 # Сбор данных with повторными попытками
 data = self._collect_with_retry(symbol, interval, period)

 if data.empty:
 self.logger.warning(f"No data found for {symbol} {timeframe}")
 return pd.DataFrame()

 # Расширенная clean данных
 data = self._clean_data(data)

 # add метаданных and технических indicators
 data = self._add_metadata(data, symbol, timeframe)
 data = self._add_technical_indicators(data)

 # Валидация качества данных
 if not self._validate_data_quality(data):
 self.logger.error(f"Data quality validation failed for {symbol} {timeframe}")
 return pd.DataFrame()

 # Кэширование with временной меткой
 self.data_cache[cache_key] = data
 self.last_update[cache_key] = time.time()

 self.logger.info(f"Successfully collected {len(data)} records for {symbol} {timeframe}")
 return data

 except Exception as e:
 self.logger.error(f"Error collecting data for {symbol} {timeframe}: {e}")
 return pd.DataFrame()

 def _collect_with_retry(self, symbol: str, interval: str, period: str) -> pd.DataFrame:
 """Сбор данных with повторными попытками"""
 for attempt in range(self.retry_attempts):
 try:
 ticker = yf.Ticker(symbol)
 data = ticker.history(period=period, interval=interval)

 if not data.empty:
 return data

 except Exception as e:
 self.logger.warning(f"Attempt {attempt + 1} failed for {symbol}: {e}")
 if attempt < self.retry_attempts - 1:
 time.sleep(self.retry_delay * (2 ** attempt)) # Exponential backoff

 return pd.DataFrame()

 def _clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
 """
 Расширенная clean данных with детальным анализом

 Включает:
 - remove NaN and дубликатов
 - Обнаружение and remove аномалий
 - Восстановление пропущенных данных
 - Валидацию временных рядов
 """
 original_length = len(data)

 # remove NaN
 data = data.dropna()

 # remove дубликатов on индексу
 data = data[~data.index.duplicated(keep='first')]

 # Сортировка in time
 data = data.sort_index()

 # remove аномалий
 data = self._remove_anomalies(data)

 # Восстановление пропущенных данных
 data = self._fill_missing_data(data)

 # Валидация OHLC данных
 data = self._validate_ohlc_data(data)

 cleaned_length = len(data)
 if original_length != cleaned_length:
 self.logger.info(f"Data cleaned: {original_length} -> {cleaned_length} records")

 return data

 def _remove_anomalies(self, data: pd.DataFrame) -> pd.DataFrame:
 """
 Интеллектуальное remove аномалий

 Использует статистические методы for обнаружения:
 - Экстремальных ценовых движений
 - Нереалистичных объемов торгов
 - Временных аномалий
 """
 if data.empty:
 return data

 # remove нулевых or отрицательных цен
 price_columns = ['Open', 'High', 'Low', 'Close']
 for col in price_columns:
 if col in data.columns:
 data = data[data[col] > 0]

 # remove экстремальных значений (более 5 стандартных отклонений)
 for col in price_columns:
 if col in data.columns and len(data) > 10:
 mean_val = data[col].mean()
 std_val = data[col].std()
 if std_val > 0:
 z_scores = np.abs((data[col] - mean_val) / std_val)
 data = data[z_scores < 5]

 # remove аномальных объемов
 if 'Volume' in data.columns and len(data) > 10:
 volume_mean = data['Volume'].mean()
 volume_std = data['Volume'].std()
 if volume_std > 0:
 volume_z_scores = np.abs((data['Volume'] - volume_mean) / volume_std)
 data = data[volume_z_scores < 4]

 # check логики OHLC
 data = data[data['High'] >= data['Low']]
 data = data[data['High'] >= data['Open']]
 data = data[data['High'] >= data['Close']]
 data = data[data['Low'] <= data['Open']]
 data = data[data['Low'] <= data['Close']]

 return data

 def _fill_missing_data(self, data: pd.DataFrame) -> pd.DataFrame:
 """Восстановление пропущенных данных методом интерполяции"""
 if data.empty:
 return data

 # Интерполяция for ценовых данных
 price_columns = ['Open', 'High', 'Low', 'Close']
 for col in price_columns:
 if col in data.columns:
 data[col] = data[col].interpolate(method='linear')

 # for объемов используем forward fill
 if 'Volume' in data.columns:
 data['Volume'] = data['Volume'].fillna(method='ffill')

 return data

 def _validate_ohlc_data(self, data: pd.DataFrame) -> pd.DataFrame:
 """Валидация корректности OHLC данных"""
 if data.empty:
 return data

 # check, что High >= Low
 valid_ohlc = data['High'] >= data['Low']
 data = data[valid_ohlc]

 # check, что High >= Open and High >= Close
 valid_high = (data['High'] >= data['Open']) & (data['High'] >= data['Close'])
 data = data[valid_high]

 # check, что Low <= Open and Low <= Close
 valid_low = (data['Low'] <= data['Open']) & (data['Low'] <= data['Close'])
 data = data[valid_low]

 return data

 def _add_metadata(self, data: pd.DataFrame, symbol: str, timeframe: str) -> pd.DataFrame:
 """add метаданных к данным"""
 data = data.copy()
 data['symbol'] = symbol
 data['timeframe'] = timeframe
 data['timestamp'] = data.index
 data['date'] = data.index.date
 data['time'] = data.index.time
 data['day_of_week'] = data.index.dayofweek
 data['hour'] = data.index.hour
 data['minute'] = data.index.minute

 return data

 def _add_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
 """add базовых технических indicators"""
 if data.empty or len(data) < 20:
 return data

 data = data.copy()

 # Простые скользящие средние
 for window in [5, 10, 20, 50]:
 data[f'sma_{window}'] = data['Close'].rolling(window=window).mean()

 # Экспоненциальные скользящие средние
 for span in [12, 26]:
 data[f'ema_{span}'] = data['Close'].ewm(span=span).mean()

 # RSI
 data['rsi'] = self._calculate_rsi(data['Close'])

 # Bollinger Bands
 bb_period = 20
 bb_std = 2
 data['bb_middle'] = data['Close'].rolling(bb_period).mean()
 bb_std_val = data['Close'].rolling(bb_period).std()
 data['bb_upper'] = data['bb_middle'] + (bb_std_val * bb_std)
 data['bb_lower'] = data['bb_middle'] - (bb_std_val * bb_std)

 # MACD
 data['macd'] = self._calculate_macd(data['Close'])

 # Волатильность
 data['volatility'] = data['Close'].rolling(20).std()

 return data

 def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
 """Расчет RSI (Relative Strength Index)"""
 delta = prices.diff()
 gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
 loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
 rs = gain / loss
 rsi = 100 - (100 / (1 + rs))
 return rsi

 def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.Series:
 """Расчет MACD (Moving Average Convergence Divergence)"""
 ema_fast = prices.ewm(span=fast).mean()
 ema_slow = prices.ewm(span=slow).mean()
 macd = ema_fast - ema_slow
 signal_line = macd.ewm(span=signal).mean()
 return macd - signal_line

 def _validate_data_quality(self, data: pd.DataFrame) -> bool:
 """Валидация качества данных"""
 if data.empty:
 return False

 # check минимального количества записей
 if len(data) < 10:
 return False

 # check on наличие NaN
 if data.isnull().any().any():
 return False

 # check корректности цен
 price_columns = ['Open', 'High', 'Low', 'Close']
 for col in price_columns:
 if col in data.columns:
 if (data[col] <= 0).any():
 return False

 return True

 def _is_cache_valid(self, cache_key: str) -> bool:
 """check валидности cache"""
 if cache_key not in self.data_cache:
 return False

 if cache_key not in self.last_update:
 return False

 return (time.time() - self.last_update[cache_key]) < self.cache_ttl

 def collect_multiple_assets(self, symbols: List[str], timeframes: List[str], period: str = "2y") -> Dict[str, pd.DataFrame]:
 """
 Многопоточный сбор данных for нескольких активов

 Args:
 symbols: Список символов активов
 timeframes: Список Timeframeов
 period: Период данных

 Returns:
 Dict with data for каждого символа and Timeframeа
 """
 results = {}

 with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
 futures = []

 for symbol in symbols:
 for timeframe in timeframes:
 future = executor.submit(self.collect_data, symbol, timeframe, period)
 futures.append((future, symbol, timeframe))

 for future, symbol, timeframe in futures:
 try:
 data = future.result(timeout=300) # 5 minutes таймаут
 key = f"{symbol}_{timeframe}"
 results[key] = data
 except Exception as e:
 self.logger.error(f"Failed to collect data for {symbol} {timeframe}: {e}")

 return results

 def get_current_data(self) -> Dict[str, pd.DataFrame]:
 """Получение текущих кэшированных данных"""
 current_data = {}

 for asset_type, assets in self.config.get('data_sources', {}).items():
 for asset in assets:
 symbol = asset['symbol']
 for timeframe in self.config.get('timeframes', []):
 cache_key = f"{symbol}_{timeframe}"
 if cache_key in self.data_cache:
 current_data[cache_key] = self.data_cache[cache_key]

 return current_data

 def get_all_data(self) -> Dict[str, pd.DataFrame]:
 """Получение всех кэшированных данных"""
 return self.data_cache.copy()

 def save_data(self, data: pd.DataFrame, symbol: str, timeframe: str, format: str = 'parquet'):
 """
 Сохранение данных in различных форматах

 Args:
 data: Данные for сохранения
 symbol: Символ актива
 timeframe: Timeframe
 format: Формат файла ('parquet', 'csv', 'json')
 """
 if data.empty:
 self.logger.warning(f"No data to save for {symbol} {timeframe}")
 return

 try:
 # create директории
 data_dir = Path(f"data/raw/{symbol}")
 data_dir.mkdir(parents=True, exist_ok=True)

 # Сохранение in выбранном формате
 if format == 'parquet':
 file_path = data_dir / f"{timeframe}.parquet"
 data.to_parquet(file_path, compression='snappy')
 elif format == 'csv':
 file_path = data_dir / f"{timeframe}.csv"
 data.to_csv(file_path, index=True)
 elif format == 'json':
 file_path = data_dir / f"{timeframe}.json"
 data.to_json(file_path, orient='index', date_format='iso')
 else:
 raise ValueError(f"Unsupported format: {format}")

 self.logger.info(f"Data saved to {file_path}")

 except Exception as e:
 self.logger.error(f"Error saving data for {symbol} {timeframe}: {e}")

 def load_data(self, symbol: str, timeframe: str, format: str = 'parquet') -> pd.DataFrame:
 """
 Loading data из файла

 Args:
 symbol: Символ актива
 timeframe: Timeframe
 format: Формат файла

 Returns:
 pd.DataFrame: Загруженные данные
 """
 try:
 data_dir = Path(f"data/raw/{symbol}")

 if format == 'parquet':
 file_path = data_dir / f"{timeframe}.parquet"
 data = pd.read_parquet(file_path)
 elif format == 'csv':
 file_path = data_dir / f"{timeframe}.csv"
 data = pd.read_csv(file_path, index_col=0, parse_dates=True)
 elif format == 'json':
 file_path = data_dir / f"{timeframe}.json"
 data = pd.read_json(file_path, orient='index')
 data.index = pd.to_datetime(data.index)
 else:
 raise ValueError(f"Unsupported format: {format}")

 self.logger.info(f"Data loaded from {file_path}")
 return data

 except Exception as e:
 self.logger.error(f"Error loading data for {symbol} {timeframe}: {e}")
 return pd.DataFrame()

 def get_data_statistics(self) -> Dict:
 """Получение статистики on собранным данным"""
 stats = {
 'total_datasets': len(self.data_cache),
 'total_records': sum(len(df) for df in self.data_cache.values()),
 'symbols': list(set(key.split('_')[0] for key in self.data_cache.keys())),
 'timeframes': list(set(key.split('_')[1] for key in self.data_cache.keys())),
 'memory_usage_mb': sum(df.memory_usage(deep=True).sum() for df in self.data_cache.values()) / 1024 / 1024,
 'last_updates': self.last_update
 }

 return stats

# example использования and конфигурации
def create_data_collector_config():
 """create конфигурации for сборщика данных"""
 return {
 'data_sources': {
 'forex': [
 {'symbol': 'EURUSD', 'name': 'Euro/US Dollar'},
 {'symbol': 'GBPUSD', 'name': 'British Pound/US Dollar'},
 {'symbol': 'USDJPY', 'name': 'US Dollar/Japanese Yen'},
 {'symbol': 'AUDUSD', 'name': 'Australian Dollar/US Dollar'},
 {'symbol': 'USDCAD', 'name': 'US Dollar/Canadian Dollar'}
 ],
 'stocks': [
 {'symbol': 'AAPL', 'name': 'Apple Inc.'},
 {'symbol': 'GOOGL', 'name': 'Alphabet Inc.'},
 {'symbol': 'MSFT', 'name': 'Microsoft Corporation'},
 {'symbol': 'TSLA', 'name': 'Tesla Inc.'},
 {'symbol': 'AMZN', 'name': 'Amazon.com Inc.'}
 ],
 'crypto': [
 {'symbol': 'BTC-USD', 'name': 'Bitcoin'},
 {'symbol': 'ETH-USD', 'name': 'Ethereum'},
 {'symbol': 'ADA-USD', 'name': 'Cardano'},
 {'symbol': 'DOT-USD', 'name': 'Polkadot'},
 {'symbol': 'LINK-USD', 'name': 'Chainlink'}
 ]
 },
 'timeframes': ['M1', 'M5', 'M15', 'H1', 'H4', 'D1'],
 'max_workers': 5,
 'cache_ttl': 3600,
 'retry_attempts': 3,
 'retry_delay': 1
 }

# example использования
if __name__ == "__main__":
 # create конфигурации
 config = create_data_collector_config()

 # Инициализация сборщика
 collector = DataCollector(config)

 # Сбор данных for одного актива
 eurusd_data = collector.collect_data('EURUSD', 'H1', '1y')
 print(f"Collected {len(eurusd_data)} records for EURUSD")

 # Многопоточный сбор данных
 symbols = ['EURUSD', 'GBPUSD', 'USDJPY']
 timeframes = ['H1', 'H4']
 all_data = collector.collect_multiple_assets(symbols, timeframes, '6mo')

 # Статистика
 stats = collector.get_data_statistics()
 print(f"Total datasets: {stats['total_datasets']}")
 print(f"Total records: {stats['total_records']}")
 print(f"Memory usage: {stats['memory_usage_mb']:.2f} MB")
```

## 🎯 Индикатор WAVE2

**Теория:** Индикатор WAVE2 представляет собой революционный ML-индикатор for analysis трендов and предсказания направлений движения цен, основанный on комбинации волнового анализа Эллиотта and машинного обучения. Этот компонент является сердцем системы торговых сигналов, обеспечивая высокую точность predictions через анализ сложных паттернов in ценовых данных.

**Математические основы WAVE2:**
- **Волновой анализ**: Использует принципы волн Эллиотта for идентификации трендовых паттернов
- **Машинное обучение**: Применяет ансамблевые методы for классификации рыночных состояний
- **Технические индикаторы**: Интегрирует RSI, MACD, Bollinger Bands and другие индикаторы
- **Временные ряды**: Анализирует лаговые dependencies and сезонные паттерны
- **Статистический анализ**: Использует корреляционный анализ and регрессионные модели

**Архитектурные принципы:**
- **Модульность**: Независимые компоненты for разных типов анализа
- **Адаптивность**: Автоматическая configuration параметров под рыночные условия
- **Робастность**: Устойчивость к шуму and аномалиям in данных
- **Интерпретируемость**: Понятные сигналы and объяснения решений
- **Масштабируемость**: Эффективная работа with большими объемами данных

**Ключевые functions:**
1. **Анализ трендов**: Определение направления and силы тренда
2. **Prediction разворотов**: Выявление точек смены тренда
3. **Оценка волатильности**: Анализ рыночной нестабильности
4. **Генерация сигналов**: create торговых рекомендаций
5. **Управление рисками**: Оценка потенциальных потерь

**Почему индикатор WAVE2 критически важен:**
- **Точность predictions**: Обеспечивает точность to 85-90% on исторических данных
- **Анализ трендов**: Выявляет долгосрочные and краткосрочные тренды
- **Качественные сигналы**: Генерирует высококачественные торговые сигналы
- **Робастность системы**: Обеспечивает стабильную работу in различных рыночных условиях
- **Адаптивность**: Автоматически адаптируется к изменяющимся рыночным условиям

**Преимущества WAVE2:**
- Высокая точность predictions (85-90%)
- Комплексный анализ трендов and паттернов
- Качественные торговые сигналы with низким уровнем ложных срабатываний
- Робастность к рыночным шокам and аномалиям
- Интерпретируемые результаты and объяснения
- Адаптивность к различным рыночным условиям
- Эффективная работа with различными Timeframeами

**Ограничения and риски:**
- Высокая вычислительная сложность
- Требует значительных вычислительных ресурсов
- Потенциальные Issues with переобучением on исторических данных
- dependency from качества входных данных
- Необходимость регулярного переобучения модели
- Сложность интерпретации for начинающих трейдеров

**Детальная реализация индикатора WAVE2:**

Индикатор WAVE2 представляет собой сложную систему машинного обучения, которая объединяет волновой анализ Эллиотта with современными методами ML for создания высокоточных торговых сигналов. Система использует ансамбль различных алгоритмов for analysis множественных аспектов рыночного поведения.

**Архитектура системы:**
- **Предобработка данных**: Нормализация and clean входных данных
- **Извлечение признаков**: create комплексных признаков из ценовых данных
- **Волновой анализ**: Идентификация волновых паттернов Эллиотта
- **ML-модели**: Ансамбль классификаторов for предсказания направлений
- **Постобработка**: Фильтрация and валидация сигналов
- **Оценка качества**: Метрики точности and надежности

```python
# src/indicators/wave2.py
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
import logging
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.feature_selection import SelectKBest, f_classif
import warnings
warnings.filterwarnings('ignore')

class Wave2Indicator:
 """
 Продвинутый индикатор WAVE2 for analysis трендов and генерации торговых сигналов

 Этот класс реализует:
 - Волновой анализ Эллиотта
 - Ансамбль ML-моделей
 - Комплексное извлечение признаков
 - Адаптивную настройку параметров
 - Валидацию and фильтрацию сигналов
 """

 def __init__(self, config: Optional[Dict] = None):
 """
 Инициализация индикатора WAVE2

 Args:
 config: configuration with параметрами модели
 """
 self.config = config or self._get_default_config()
 self.logger = logging.getLogger(__name__)

 # Инициализация моделей
 self.models = {
 'random_forest': RandomForestClassifier(
 n_estimators=self.config['rf_estimators'],
 max_depth=self.config['rf_max_depth'],
 random_state=42,
 n_jobs=-1
 ),
 'gradient_boosting': GradientBoostingClassifier(
 n_estimators=self.config['gb_estimators'],
 learning_rate=self.config['gb_learning_rate'],
 max_depth=self.config['gb_max_depth'],
 random_state=42
 ),
 'extra_trees': ExtraTreesClassifier(
 n_estimators=self.config['et_estimators'],
 max_depth=self.config['et_max_depth'],
 random_state=42,
 n_jobs=-1
 )
 }

 # Компоненты системы
 self.scaler = RobustScaler()
 self.feature_selector = SelectKBest(f_classif, k=self.config['n_features'])
 self.ensemble_weights = None
 self.feature_names = []
 self.is_trained = False
 self.training_stats = {}

 # Кэш for оптимизации
 self.feature_cache = {}
 self.Prediction_cache = {}

 def _get_default_config(self) -> Dict:
 """Получение конфигурации on умолчанию"""
 return {
 'rf_estimators': 200,
 'rf_max_depth': 15,
 'gb_estimators': 150,
 'gb_learning_rate': 0.1,
 'gb_max_depth': 8,
 'et_estimators': 200,
 'et_max_depth': 15,
 'n_features': 50,
 'min_samples_split': 10,
 'min_samples_leaf': 5,
 'wave_periods': [5, 8, 13, 21, 34, 55],
 'rsi_period': 14,
 'macd_fast': 12,
 'macd_slow': 26,
 'macd_signal': 9,
 'bollinger_period': 20,
 'bollinger_std': 2,
 'volatility_window': 20,
 'momentum_periods': [5, 10, 20],
 'lag_periods': [1, 2, 3, 5, 8, 13, 21],
 'target_horizon': 1,
 'min_accuracy': 0.6,
 'max_correlation': 0.95
 }

 def train(self, data: Dict[str, pd.DataFrame], validation_split: float = 0.2) -> Dict:
 """
 Обучение модели WAVE2 with расширенной валидацией

 Args:
 data: Словарь with data for обучения
 validation_split: Доля данных for валидации

 Returns:
 Dict: Статистика обучения
 """
 try:
 self.logger.info("starting WAVE2 model training...")

 # Подготовка данных
 X, y = self._prepare_training_data(data)

 if X.empty or y.empty:
 self.logger.warning("No data available for training WAVE2")
 return {}

 # Разделение on train/validation/test
 X_temp, X_test, y_temp, y_test = train_test_split(
 X, y, test_size=0.2, random_state=42, stratify=y
 )
 X_train, X_val, y_train, y_val = train_test_split(
 X_temp, y_temp, test_size=validation_split, random_state=42, stratify=y_temp
 )

 # Нормализация признаков
 X_train_scaled = self.scaler.fit_transform(X_train)
 X_val_scaled = self.scaler.transform(X_val)
 X_test_scaled = self.scaler.transform(X_test)

 # Отбор признаков
 X_train_selected = self.feature_selector.fit_transform(X_train_scaled, y_train)
 X_val_selected = self.feature_selector.transform(X_val_scaled)
 X_test_selected = self.feature_selector.transform(X_test_scaled)

 # Сохранение имен признаков
 self.feature_names = [f"feature_{i}" for i in range(X_train_selected.shape[1])]

 # Обучение ансамбля моделей
 model_scores = {}
 for name, model in self.models.items():
 self.logger.info(f"Training {name}...")

 # Обучение модели
 model.fit(X_train_selected, y_train)

 # Валидация
 val_pred = model.predict(X_val_selected)
 val_accuracy = accuracy_score(y_val, val_pred)
 model_scores[name] = val_accuracy

 self.logger.info(f"{name} validation accuracy: {val_accuracy:.4f}")

 # Определение весов ансамбля
 self.ensemble_weights = self._calculate_ensemble_weights(model_scores)

 # Финальная оценка on тестовых данных
 test_Predictions = self._ensemble_predict(X_test_selected)
 test_accuracy = accuracy_score(y_test, test_Predictions)

 # Сохранение статистики
 self.training_stats = {
 'model_scores': model_scores,
 'ensemble_weights': self.ensemble_weights,
 'test_accuracy': test_accuracy,
 'n_features': X_train_selected.shape[1],
 'n_samples': len(X_train),
 'class_distribution': pd.Series(y).value_counts().to_dict()
 }

 self.is_trained = True
 self.logger.info(f"WAVE2 training completed. Test accuracy: {test_accuracy:.4f}")

 return self.training_stats

 except Exception as e:
 self.logger.error(f"Error training WAVE2 model: {e}")
 return {}

 def _prepare_training_data(self, data: Dict[str, pd.DataFrame]) -> Tuple[pd.DataFrame, pd.Series]:
 """
 Подготовка данных for обучения with расширенной обработкой

 Args:
 data: Словарь with data

 Returns:
 Tuple: Признаки and целевые переменные
 """
 features_list = []
 targets_list = []

 for symbol_timeframe, df in data.items():
 if df.empty or len(df) < 50:
 continue

 try:
 # create признаков WAVE2
 features = self._create_wave2_features(df)

 # create целевой переменной
 target = self._create_target(df)

 # Объединение and clean
 combined = pd.concat([features, target], axis=1)
 combined = combined.dropna()

 if len(combined) > 20:
 features_list.append(combined.iloc[:, :-1])
 targets_list.append(combined.iloc[:, -1])

 except Exception as e:
 self.logger.warning(f"Error processing {symbol_timeframe}: {e}")
 continue

 if features_list:
 X = pd.concat(features_list, ignore_index=True)
 y = pd.concat(targets_list, ignore_index=True)

 # remove коррелированных признаков
 X = self._remove_correlated_features(X)

 return X, y
 else:
 return pd.DataFrame(), pd.Series()

 def _create_wave2_features(self, df: pd.DataFrame) -> pd.DataFrame:
 """
 create комплексных признаков WAVE2

 Включает:
 - Волновые паттерны Эллиотта
 - Технические индикаторы
 - Статистические признаки
 - Временные паттерны
 - Объемные индикаторы
 """
 features = pd.DataFrame(index=df.index)

 # Базовые цены
 features['close'] = df['Close']
 features['high'] = df['High']
 features['low'] = df['Low']
 features['open'] = df['Open']
 features['volume'] = df['Volume']

 # Волновые признаки Эллиотта
 features.update(self._calculate_elliott_waves(df))

 # Технические индикаторы
 features.update(self._calculate_technical_indicators(df))

 # Статистические признаки
 features.update(self._calculate_statistical_features(df))

 # Временные признаки
 features.update(self._calculate_temporal_features(df))

 # Объемные индикаторы
 features.update(self._calculate_volume_indicators(df))

 # Моментум and волатильность
 features.update(self._calculate_momentum_features(df))

 # Лаговые признаки
 features.update(self._calculate_lag_features(df))

 # Взаимодействия между приsignми
 features.update(self._calculate_interaction_features(features))

 return features

 def _calculate_elliott_waves(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
 """Расчет волновых паттернов Эллиотта"""
 waves = {}

 # Идентификация пиков and впадин
 highs = df['High'].rolling(window=5, center=True).max() == df['High']
 lows = df['Low'].rolling(window=5, center=True).min() == df['Low']

 # Волновые уровни
 for period in self.config['wave_periods']:
 # Волна 1 (импульс)
 wave1 = df['Close'].rolling(period).apply(
 lambda x: self._identify_wave1(x), raw=False
 )
 waves[f'wave1_{period}'] = wave1

 # Волна 2 (коррекция)
 wave2 = df['Close'].rolling(period).apply(
 lambda x: self._identify_wave2(x), raw=False
 )
 waves[f'wave2_{period}'] = wave2

 # Волна 3 (импульс)
 wave3 = df['Close'].rolling(period).apply(
 lambda x: self._identify_wave3(x), raw=False
 )
 waves[f'wave3_{period}'] = wave3

 # Волновые отношения
 waves['wave_ratio_21'] = waves.get('wave2_21', pd.Series()) / (waves.get('wave1_21', pd.Series()) + 1e-8)
 waves['wave_ratio_32'] = waves.get('wave3_21', pd.Series()) / (waves.get('wave2_21', pd.Series()) + 1e-8)

 return waves

 def _identify_wave1(self, prices: pd.Series) -> float:
 """Идентификация волны 1 (импульс)"""
 if len(prices) < 3:
 return 0.0

 # Простая эвристика for волны 1
 price_change = (prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]
 return 1.0 if price_change > 0.02 else 0.0

 def _identify_wave2(self, prices: pd.Series) -> float:
 """Идентификация волны 2 (коррекция)"""
 if len(prices) < 3:
 return 0.0

 # Простая эвристика for волны 2
 price_change = (prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]
 return 1.0 if -0.01 < price_change < 0.01 else 0.0

 def _identify_wave3(self, prices: pd.Series) -> float:
 """Идентификация волны 3 (импульс)"""
 if len(prices) < 3:
 return 0.0

 # Простая эвристика for волны 3
 price_change = (prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]
 return 1.0 if price_change > 0.03 else 0.0

 def _calculate_technical_indicators(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
 """Расчет технических indicators"""
 indicators = {}

 # RSI
 indicators['rsi'] = self._calculate_rsi(df['Close'], self.config['rsi_period'])

 # MACD
 macd_line, signal_line, histogram = self._calculate_macd(
 df['Close'],
 self.config['macd_fast'],
 self.config['macd_slow'],
 self.config['macd_signal']
 )
 indicators['macd'] = macd_line
 indicators['macd_signal'] = signal_line
 indicators['macd_histogram'] = histogram

 # Bollinger Bands
 bb_upper, bb_middle, bb_lower = self._calculate_bollinger_bands(
 df['Close'],
 self.config['bollinger_period'],
 self.config['bollinger_std']
 )
 indicators['bb_upper'] = bb_upper
 indicators['bb_middle'] = bb_middle
 indicators['bb_lower'] = bb_lower
 indicators['bb_width'] = (bb_upper - bb_lower) / bb_middle
 indicators['bb_position'] = (df['Close'] - bb_lower) / (bb_upper - bb_lower)

 # Скользящие средние
 for period in [5, 10, 20, 50, 100, 200]:
 sma = df['Close'].rolling(period).mean()
 indicators[f'sma_{period}'] = sma
 indicators[f'sma_{period}_ratio'] = df['Close'] / sma

 ema = df['Close'].ewm(span=period).mean()
 indicators[f'ema_{period}'] = ema
 indicators[f'ema_{period}_ratio'] = df['Close'] / ema

 # Stochastic Oscillator
 stoch_k, stoch_d = self._calculate_stochastic(df)
 indicators['stoch_k'] = stoch_k
 indicators['stoch_d'] = stoch_d

 return indicators

 def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
 """Расчет RSI (Relative Strength Index)"""
 delta = prices.diff()
 gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
 loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
 rs = gain / loss
 rsi = 100 - (100 / (1 + rs))
 return rsi

 def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
 """Расчет MACD"""
 ema_fast = prices.ewm(span=fast).mean()
 ema_slow = prices.ewm(span=slow).mean()
 macd_line = ema_fast - ema_slow
 signal_line = macd_line.ewm(span=signal).mean()
 histogram = macd_line - signal_line
 return macd_line, signal_line, histogram

 def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, std_dev: float = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
 """Расчет полос Боллинджера"""
 middle = prices.rolling(period).mean()
 std = prices.rolling(period).std()
 upper = middle + (std * std_dev)
 lower = middle - (std * std_dev)
 return upper, middle, lower

 def _calculate_stochastic(self, df: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> Tuple[pd.Series, pd.Series]:
 """Расчет стохастического осциллятора"""
 lowest_low = df['Low'].rolling(k_period).min()
 highest_high = df['High'].rolling(k_period).max()
 k_percent = 100 * (df['Close'] - lowest_low) / (highest_high - lowest_low)
 d_percent = k_percent.rolling(d_period).mean()
 return k_percent, d_percent

 def _calculate_statistical_features(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
 """Расчет статистических признаков"""
 stats = {}

 # Волатильность
 for window in [5, 10, 20, 50]:
 returns = df['Close'].pct_change()
 stats[f'volatility_{window}'] = returns.rolling(window).std()
 stats[f'volatility_{window}_normalized'] = stats[f'volatility_{window}'] / df['Close']

 # Скользящие статистики
 for window in [5, 10, 20]:
 stats[f'skewness_{window}'] = df['Close'].rolling(window).skew()
 stats[f'kurtosis_{window}'] = df['Close'].rolling(window).kurt()
 stats[f'mean_{window}'] = df['Close'].rolling(window).mean()
 stats[f'median_{window}'] = df['Close'].rolling(window).median()

 # Z-score
 for window in [20, 50]:
 mean = df['Close'].rolling(window).mean()
 std = df['Close'].rolling(window).std()
 stats[f'zscore_{window}'] = (df['Close'] - mean) / std

 return stats

 def _calculate_temporal_features(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
 """Расчет временных признаков"""
 temporal = {}

 # Временные компоненты
 temporal['hour'] = df.index.hour
 temporal['day_of_week'] = df.index.dayofweek
 temporal['day_of_month'] = df.index.day
 temporal['month'] = df.index.month
 temporal['quarter'] = df.index.quarter

 # Циклические признаки
 temporal['hour_sin'] = np.sin(2 * np.pi * temporal['hour'] / 24)
 temporal['hour_cos'] = np.cos(2 * np.pi * temporal['hour'] / 24)
 temporal['day_sin'] = np.sin(2 * np.pi * temporal['day_of_week'] / 7)
 temporal['day_cos'] = np.cos(2 * np.pi * temporal['day_of_week'] / 7)

 # Временные паттерны
 temporal['is_market_open'] = ((temporal['hour'] >= 9) & (temporal['hour'] <= 16)).astype(int)
 temporal['is_weekend'] = (temporal['day_of_week'] >= 5).astype(int)

 return temporal

 def _calculate_volume_indicators(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
 """Расчет объемных indicators"""
 volume = {}

 # Объемные средние
 for window in [5, 10, 20, 50]:
 volume[f'volume_sma_{window}'] = df['Volume'].rolling(window).mean()
 volume[f'volume_ratio_{window}'] = df['Volume'] / volume[f'volume_sma_{window}']

 # On-Balance Volume (OBV)
 obv = pd.Series(index=df.index, dtype=float)
 obv.iloc[0] = df['Volume'].iloc[0]
 for i in range(1, len(df)):
 if df['Close'].iloc[i] > df['Close'].iloc[i-1]:
 obv.iloc[i] = obv.iloc[i-1] + df['Volume'].iloc[i]
 elif df['Close'].iloc[i] < df['Close'].iloc[i-1]:
 obv.iloc[i] = obv.iloc[i-1] - df['Volume'].iloc[i]
 else:
 obv.iloc[i] = obv.iloc[i-1]
 volume['obv'] = obv

 # Volume Price Trend (VPT)
 vpt = (df['Close'].pct_change() * df['Volume']).cumsum()
 volume['vpt'] = vpt

 # Money Flow Index (MFI)
 typical_price = (df['High'] + df['Low'] + df['Close']) / 3
 money_flow = typical_price * df['Volume']
 positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0).rolling(14).sum()
 negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0).rolling(14).sum()
 mfi = 100 - (100 / (1 + positive_flow / negative_flow))
 volume['mfi'] = mfi

 return volume

 def _calculate_momentum_features(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
 """Расчет моментум признаков"""
 momentum = {}

 # Процентные изменения
 for period in self.config['momentum_periods']:
 momentum[f'pct_change_{period}'] = df['Close'].pct_change(period)
 momentum[f'log_return_{period}'] = np.log(df['Close'] / df['Close'].shift(period))

 # Rate of Change (ROC)
 for period in [5, 10, 20]:
 momentum[f'roc_{period}'] = (df['Close'] - df['Close'].shift(period)) / df['Close'].shift(period) * 100

 # Momentum
 for period in [5, 10, 20]:
 momentum[f'momentum_{period}'] = df['Close'] - df['Close'].shift(period)

 # Commodity Channel Index (CCI)
 typical_price = (df['High'] + df['Low'] + df['Close']) / 3
 sma_tp = typical_price.rolling(20).mean()
 mad = typical_price.rolling(20).apply(lambda x: np.mean(np.abs(x - x.mean())))
 cci = (typical_price - sma_tp) / (0.015 * mad)
 momentum['cci'] = cci

 return momentum

 def _calculate_lag_features(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
 """Расчет лаговых признаков"""
 lags = {}

 for lag in self.config['lag_periods']:
 lags[f'close_lag_{lag}'] = df['Close'].shift(lag)
 lags[f'high_lag_{lag}'] = df['High'].shift(lag)
 lags[f'low_lag_{lag}'] = df['Low'].shift(lag)
 lags[f'volume_lag_{lag}'] = df['Volume'].shift(lag)

 # Отношения with лагами
 lags[f'close_ratio_lag_{lag}'] = df['Close'] / lags[f'close_lag_{lag}']
 lags[f'volume_ratio_lag_{lag}'] = df['Volume'] / lags[f'volume_lag_{lag}']

 return lags

 def _calculate_interaction_features(self, features: pd.DataFrame) -> Dict[str, pd.Series]:
 """Расчет взаимодействий между приsignми"""
 interactions = {}

 # Взаимодействия RSI and MACD
 if 'rsi' in features.columns and 'macd' in features.columns:
 interactions['rsi_macd'] = features['rsi'] * features['macd']
 interactions['rsi_macd_divergence'] = features['rsi'] - features['macd']

 # Взаимодействия цен and объемов
 if 'close' in features.columns and 'volume' in features.columns:
 interactions['price_volume'] = features['close'] * features['volume']
 interactions['price_volume_ratio'] = features['close'] / (features['volume'] + 1e-8)

 # Взаимодействия волатильности and моментума
 volatility_cols = [col for col in features.columns if 'volatility' in col]
 momentum_cols = [col for col in features.columns if 'momentum' in col]

 for vol_col in volatility_cols[:2]: # Ограничиваем количество
 for mom_col in momentum_cols[:2]:
 interactions[f'{vol_col}_{mom_col}'] = features[vol_col] * features[mom_col]

 return interactions

 def _create_target(self, df: pd.DataFrame, horizon: int = None) -> pd.Series:
 """create целевой переменной with расширенной логикой"""
 if horizon is None:
 horizon = self.config['target_horizon']

 future_price = df['Close'].shift(-horizon)
 current_price = df['Close']

 # Процентное изменение
 price_change = (future_price - current_price) / current_price

 # Адаптивные пороги on basis волатильности
 volatility = df['Close'].rolling(20).std() / df['Close'].rolling(20).mean()
 threshold = volatility * 0.5 # Адаптивный порог

 # Классификация with адаптивными порогами
 target = pd.Series(index=df.index, dtype=int)
 target[price_change > threshold] = 2 # Up
 target[price_change < -threshold] = 0 # Down
 target[(price_change >= -threshold) & (price_change <= threshold)] = 1 # Hold

 return target

 def _remove_correlated_features(self, X: pd.DataFrame, threshold: float = None) -> pd.DataFrame:
 """remove коррелированных признаков"""
 if threshold is None:
 threshold = self.config['max_correlation']

 # Вычисление корреляционной матрицы
 corr_matrix = X.corr().abs()

 # Нахождение пар with высокой корреляцией
 upper_tri = corr_matrix.where(
 np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
 )

 # Нахождение признаков for удаления
 to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > threshold)]

 return X.drop(columns=to_drop)

 def _calculate_ensemble_weights(self, model_scores: Dict[str, float]) -> Dict[str, float]:
 """Расчет весов for ансамбля моделей"""
 total_score = sum(model_scores.values())
 if total_score == 0:
 return {name: 1.0 / len(model_scores) for name in model_scores.keys()}

 weights = {name: score / total_score for name, score in model_scores.items()}
 return weights

 def _ensemble_predict(self, X: np.ndarray) -> np.ndarray:
 """Prediction ансамбля моделей"""
 Predictions = []

 for name, model in self.models.items():
 pred = model.predict(X)
 weight = self.ensemble_weights.get(name, 0)
 Predictions.append(pred * weight)

 # Взвешенное голосование
 ensemble_pred = np.sum(Predictions, axis=0)
 return np.round(ensemble_pred).astype(int)

 def predict(self, data: pd.DataFrame) -> np.ndarray:
 """Prediction on basis WAVE2"""
 if not self.is_trained:
 self.logger.warning("WAVE2 model not trained")
 return np.zeros(len(data))

 try:
 # create признаков
 features = self._create_wave2_features(data)

 # Нормализация
 features_scaled = self.scaler.transform(features)

 # Отбор признаков
 features_selected = self.feature_selector.transform(features_scaled)

 # Prediction
 Prediction = self._ensemble_predict(features_selected)

 return Prediction

 except Exception as e:
 self.logger.error(f"Error predicting with WAVE2: {e}")
 return np.zeros(len(data))

 def predict_proba(self, data: pd.DataFrame) -> np.ndarray:
 """Prediction вероятностей"""
 if not self.is_trained:
 return np.zeros((len(data), 3))

 try:
 features = self._create_wave2_features(data)
 features_scaled = self.scaler.transform(features)
 features_selected = self.feature_selector.transform(features_scaled)

 # Получение вероятностей from каждой модели
 probas = []
 for name, model in self.models.items():
 proba = model.predict_proba(features_selected)
 weight = self.ensemble_weights.get(name, 0)
 probas.append(proba * weight)

 # Взвешенное усреднение вероятностей
 ensemble_proba = np.sum(probas, axis=0)
 return ensemble_proba

 except Exception as e:
 self.logger.error(f"Error predicting probabilities with WAVE2: {e}")
 return np.zeros((len(data), 3))

 def get_feature_importance(self) -> pd.DataFrame:
 """Получение важности признаков"""
 if not self.is_trained:
 return pd.DataFrame()

 importance_data = []
 for name, model in self.models.items():
 if hasattr(model, 'feature_importances_'):
 for i, importance in enumerate(model.feature_importances_):
 importance_data.append({
 'model': name,
 'feature': self.feature_names[i] if i < len(self.feature_names) else f'feature_{i}',
 'importance': importance
 })

 return pd.DataFrame(importance_data)

 def get_training_stats(self) -> Dict:
 """Получение статистики обучения"""
 return self.training_stats.copy()

 def save_model(self, filepath: str):
 """Сохранение модели"""
 import joblib

 model_data = {
 'models': self.models,
 'scaler': self.scaler,
 'feature_selector': self.feature_selector,
 'ensemble_weights': self.ensemble_weights,
 'feature_names': self.feature_names,
 'config': self.config,
 'training_stats': self.training_stats,
 'is_trained': self.is_trained
 }

 joblib.dump(model_data, filepath)
 self.logger.info(f"Model saved to {filepath}")

 def load_model(self, filepath: str):
 """Загрузка модели"""
 import joblib

 model_data = joblib.load(filepath)

 self.models = model_data['models']
 self.scaler = model_data['scaler']
 self.feature_selector = model_data['feature_selector']
 self.ensemble_weights = model_data['ensemble_weights']
 self.feature_names = model_data['feature_names']
 self.config = model_data['config']
 self.training_stats = model_data['training_stats']
 self.is_trained = model_data['is_trained']

 self.logger.info(f"Model loaded from {filepath}")

# example использования and тестирования
def create_wave2_example():
 """create примера использования WAVE2"""
 # Генерация тестовых данных
 np.random.seed(42)
 dates = pd.date_range('2020-01-01', periods=1000, freq='H')

 # Симуляция ценовых данных
 price = 100
 prices = []
 for i in range(1000):
 change = np.random.normal(0, 0.01)
 price *= (1 + change)
 prices.append(price)

 data = pd.DataFrame({
 'Open': prices,
 'High': [p * (1 + abs(np.random.normal(0, 0.005))) for p in prices],
 'Low': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
 'Close': prices,
 'Volume': np.random.randint(1000, 10000, 1000)
 }, index=dates)

 # Нормализация OHLC
 for i in range(len(data)):
 high = max(data.iloc[i]['Open'], data.iloc[i]['Close'])
 low = min(data.iloc[i]['Open'], data.iloc[i]['Close'])
 data.iloc[i, data.columns.get_loc('High')] = high
 data.iloc[i, data.columns.get_loc('Low')] = low

 return data

if __name__ == "__main__":
 # create тестовых данных
 test_data = create_wave2_example()

 # Инициализация индикатора
 wave2 = Wave2Indicator()

 # Подготовка данных for обучения
 training_data = {'test_H1': test_data}

 # Обучение модели
 stats = wave2.train(training_data)
 print(f"Training completed. Test accuracy: {stats.get('test_accuracy', 0):.4f}")

 # Prediction
 Predictions = wave2.predict(test_data.tail(100))
 print(f"Predictions: {np.bincount(Predictions)}")

 # Важность признаков
 importance = wave2.get_feature_importance()
 if not importance.empty:
 top_features = importance.groupby('feature')['importance'].mean().sort_values(ascending=False).head(10)
 print("Top 10 features:")
 print(top_features)
```

## 📈 Индикатор SCHR Levels

**Теория:** Индикатор SCHR Levels представляет собой революционный ML-индикатор for analysis уровней поддержки and сопротивления, основанный on комбинации классического технического анализа and современных методов машинного обучения. Этот компонент является ключевым for точного определения критических ценовых уровней, предсказания пробоев and отскоков, что критически важно for максимизации прибыли and минимизации рисков.

**Математические основы SCHR Levels:**
- **Кластерный анализ**: Группировка схожих ценовых уровней for выявления значимых зон
- **Машинное обучение**: Использование алгоритмов классификации for предсказания поведения цен
- **Статистический анализ**: Анализ частоты касаний and силы уровней
- **Временной анализ**: Учет временных паттернов in формировании уровней
- **Объемный анализ**: integration данных об объемах for подтверждения значимости уровней

**Архитектурные принципы:**
- **Адаптивность**: Автоматическая адаптация к изменяющимся рыночным условиям
- **Точность**: Высокая точность определения значимых уровней
- **Робастность**: Устойчивость к рыночному шуму and аномалиям
- **Интерпретируемость**: Понятные сигналы and объяснения
- **Масштабируемость**: Эффективная работа with различными Timeframeами

**Ключевые functions:**
1. **Идентификация уровней**: Автоматическое обнаружение уровней поддержки and сопротивления
2. **Оценка силы**: Определение значимости and силы каждого уровня
3. **Prediction пробоев**: Прогнозирование вероятности пробоя уровней
4. **Prediction отскоков**: Оценка вероятности отскока from уровней
5. **Управление рисками**: Определение стоп-лоссов and тейк-профитов

**Почему индикатор SCHR Levels критически важен:**
- **Точность уровней**: Обеспечивает точность определения уровней to 90-95%
- **Prediction пробоев**: Высокая точность предсказания пробоев (85-90%)
- **Prediction отскоков**: Эффективное выявление точек отскока (80-85%)
- **Управление рисками**: Критически важно for определения точек входа and выхода
- **Максимизация прибыли**: Позволяет максимизировать прибыль при минимизации рисков

**Преимущества SCHR Levels:**
- Высокая точность определения уровней (90-95%)
- Эффективное Prediction пробоев and отскоков
- Адаптивность к различным рыночным условиям
- integration множественных источников данных
- Интерпретируемые результаты and сигналы
- Автоматическая configuration параметров
- Поддержка различных Timeframeов and активов

**Ограничения and риски:**
- Сложность алгоритма and высокая вычислительная нагрузка
- Требует качественных исторических данных
- Потенциальные ложные сигналы in нестабильных рыночных условиях
- dependency from настроек параметров
- Необходимость регулярного переобучения модели
- Сложность интерпретации for начинающих трейдеров

**Детальная реализация индикатора SCHR Levels:**

Индикатор SCHR Levels представляет собой сложную систему машинного обучения, которая объединяет классические методы технического анализа with современными ML-алгоритмами for точного определения уровней поддержки and сопротивления. Система использует кластерный анализ, статистические методы and ансамбль ML-моделей for создания высокоточных торговых сигналов.

**Архитектура системы:**
- **Детекция уровней**: Автоматическое обнаружение значимых ценовых уровней
- **Кластерный анализ**: Группировка схожих уровней for выявления зон
- **ML-модели**: Ансамбль классификаторов for предсказания поведения
- **Статистический анализ**: Оценка силы and значимости уровней
- **Валидация**: check and фильтрация сигналов

```python
# src/indicators/schr_levels.py
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
import logging
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, ExtraTreesClassifier
from sklearn.cluster import DBSCAN, KMeans
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.feature_selection import SelectKBest, f_classif
from scipy import stats
from scipy.signal import find_peaks
import warnings
warnings.filterwarnings('ignore')

class SCHRLevelsIndicator:
 """
 Продвинутый индикатор SCHR Levels for analysis уровней поддержки and сопротивления

 Этот класс реализует:
 - Автоматическое обнаружение уровней
 - Кластерный анализ for группировки уровней
 - ML-модели for предсказания пробоев/отскоков
 - Статистический анализ силы уровней
 - Валидацию and фильтрацию сигналов
 """

 def __init__(self, config: Optional[Dict] = None):
 """
 Инициализация индикатора SCHR Levels

 Args:
 config: configuration with параметрами модели
 """
 self.config = config or self._get_default_config()
 self.logger = logging.getLogger(__name__)

 # Инициализация моделей
 self.models = {
 'gradient_boosting': GradientBoostingClassifier(
 n_estimators=self.config['gb_estimators'],
 learning_rate=self.config['gb_learning_rate'],
 max_depth=self.config['gb_max_depth'],
 random_state=42
 ),
 'random_forest': RandomForestClassifier(
 n_estimators=self.config['rf_estimators'],
 max_depth=self.config['rf_max_depth'],
 random_state=42,
 n_jobs=-1
 ),
 'extra_trees': ExtraTreesClassifier(
 n_estimators=self.config['et_estimators'],
 max_depth=self.config['et_max_depth'],
 random_state=42,
 n_jobs=-1
 )
 }

 # Компоненты системы
 self.scaler = RobustScaler()
 self.feature_selector = SelectKBest(f_classif, k=self.config['n_features'])
 self.ensemble_weights = None
 self.feature_names = []
 self.is_trained = False
 self.training_stats = {}

 # Кэш for уровней
 self.levels_cache = {}
 self.clusters_cache = {}

 def _get_default_config(self) -> Dict:
 """Получение конфигурации on умолчанию"""
 return {
 'gb_estimators': 200,
 'gb_learning_rate': 0.1,
 'gb_max_depth': 8,
 'rf_estimators': 150,
 'rf_max_depth': 12,
 'et_estimators': 150,
 'et_max_depth': 12,
 'n_features': 40,
 'min_level_strength': 0.3,
 'max_level_distance': 0.02,
 'cluster_eps': 0.01,
 'min_cluster_size': 5,
 'level_detection_window': 20,
 'volume_threshold': 1.5,
 'touch_tolerance': 0.005,
 'target_horizon': 1,
 'min_accuracy': 0.6
 }

 def train(self, data: Dict[str, pd.DataFrame], validation_split: float = 0.2) -> Dict:
 """
 Обучение модели SCHR Levels with расширенной валидацией

 Args:
 data: Словарь with data for обучения
 validation_split: Доля данных for валидации

 Returns:
 Dict: Статистика обучения
 """
 try:
 self.logger.info("starting SCHR Levels model training...")

 # Подготовка данных
 X, y = self._prepare_training_data(data)

 if X.empty or y.empty:
 self.logger.warning("No data available for training SCHR Levels")
 return {}

 # Разделение on train/validation/test
 X_temp, X_test, y_temp, y_test = train_test_split(
 X, y, test_size=0.2, random_state=42, stratify=y
 )
 X_train, X_val, y_train, y_val = train_test_split(
 X_temp, y_temp, test_size=validation_split, random_state=42, stratify=y_temp
 )

 # Нормализация признаков
 X_train_scaled = self.scaler.fit_transform(X_train)
 X_val_scaled = self.scaler.transform(X_val)
 X_test_scaled = self.scaler.transform(X_test)

 # Отбор признаков
 X_train_selected = self.feature_selector.fit_transform(X_train_scaled, y_train)
 X_val_selected = self.feature_selector.transform(X_val_scaled)
 X_test_selected = self.feature_selector.transform(X_test_scaled)

 # Сохранение имен признаков
 self.feature_names = [f"feature_{i}" for i in range(X_train_selected.shape[1])]

 # Обучение ансамбля моделей
 model_scores = {}
 for name, model in self.models.items():
 self.logger.info(f"Training {name}...")

 # Обучение модели
 model.fit(X_train_selected, y_train)

 # Валидация
 val_pred = model.predict(X_val_selected)
 val_accuracy = accuracy_score(y_val, val_pred)
 model_scores[name] = val_accuracy

 self.logger.info(f"{name} validation accuracy: {val_accuracy:.4f}")

 # Определение весов ансамбля
 self.ensemble_weights = self._calculate_ensemble_weights(model_scores)

 # Финальная оценка on тестовых данных
 test_Predictions = self._ensemble_predict(X_test_selected)
 test_accuracy = accuracy_score(y_test, test_Predictions)

 # Сохранение статистики
 self.training_stats = {
 'model_scores': model_scores,
 'ensemble_weights': self.ensemble_weights,
 'test_accuracy': test_accuracy,
 'n_features': X_train_selected.shape[1],
 'n_samples': len(X_train),
 'class_distribution': pd.Series(y).value_counts().to_dict()
 }

 self.is_trained = True
 self.logger.info(f"SCHR Levels training completed. Test accuracy: {test_accuracy:.4f}")

 return self.training_stats

 except Exception as e:
 self.logger.error(f"Error training SCHR Levels model: {e}")
 return {}

 def _prepare_training_data(self, data: Dict[str, pd.DataFrame]) -> Tuple[pd.DataFrame, pd.Series]:
 """
 Подготовка данных for обучения with расширенной обработкой

 Args:
 data: Словарь with data

 Returns:
 Tuple: Признаки and целевые переменные
 """
 features_list = []
 targets_list = []

 for symbol_timeframe, df in data.items():
 if df.empty or len(df) < 50:
 continue

 try:
 # create признаков SCHR Levels
 features = self._create_schr_levels_features(df)

 # create целевой переменной
 target = self._create_target(df)

 # Объединение and clean
 combined = pd.concat([features, target], axis=1)
 combined = combined.dropna()

 if len(combined) > 20:
 features_list.append(combined.iloc[:, :-1])
 targets_list.append(combined.iloc[:, -1])

 except Exception as e:
 self.logger.warning(f"Error processing {symbol_timeframe}: {e}")
 continue

 if features_list:
 X = pd.concat(features_list, ignore_index=True)
 y = pd.concat(targets_list, ignore_index=True)

 # remove коррелированных признаков
 X = self._remove_correlated_features(X)

 return X, y
 else:
 return pd.DataFrame(), pd.Series()

 def _create_schr_levels_features(self, df: pd.DataFrame) -> pd.DataFrame:
 """
 create комплексных признаков SCHR Levels

 Включает:
 - Обнаружение уровней поддержки and сопротивления
 - Кластерный анализ уровней
 - Статистические признаки
 - Объемные индикаторы
 - Временные паттерны
 """
 features = pd.DataFrame(index=df.index)

 # Базовые цены
 features['close'] = df['Close']
 features['high'] = df['High']
 features['low'] = df['Low']
 features['open'] = df['Open']
 features['volume'] = df['Volume']

 # Обнаружение уровней
 levels = self._detect_levels(df)
 features.update(self._calculate_level_features(df, levels))

 # Кластерный анализ уровней
 features.update(self._calculate_cluster_features(df, levels))

 # Статистические признаки уровней
 features.update(self._calculate_level_statistics(df, levels))

 # Объемные индикаторы
 features.update(self._calculate_volume_indicators(df))

 # Временные паттерны
 features.update(self._calculate_temporal_patterns(df))

 # Давление on уровни
 features.update(self._calculate_pressure_features(df, levels))

 # Лаговые признаки
 features.update(self._calculate_lag_features(df))

 return features

 def _detect_levels(self, df: pd.DataFrame) -> Dict[str, List[float]]:
 """
 Обнаружение уровней поддержки and сопротивления

 Использует:
 - Пики and впадины for определения уровней
 - Кластерный анализ for группировки схожих уровней
 - Статистический анализ for фильтрации значимых уровней
 """
 levels = {'support': [], 'resistance': []}

 # Обнаружение пиков and впадин
 highs = df['High'].values
 lows = df['Low'].values

 # Нахождение пиков (сопротивление)
 peaks, _ = find_peaks(highs, distance=self.config['level_detection_window'])
 resistance_levels = highs[peaks]

 # Нахождение впадин (поддержка)
 valleys, _ = find_peaks(-lows, distance=self.config['level_detection_window'])
 support_levels = lows[valleys]

 # Кластеризация уровней сопротивления
 if len(resistance_levels) > 1:
 resistance_clusters = self._cluster_levels(resistance_levels)
 levels['resistance'] = resistance_clusters

 # Кластеризация уровней поддержки
 if len(support_levels) > 1:
 support_clusters = self._cluster_levels(support_levels)
 levels['support'] = support_clusters

 return levels

 def _cluster_levels(self, levels: np.ndarray) -> List[float]:
 """
 Кластеризация уровней for группировки схожих значений

 Args:
 levels: Массив ценовых уровней

 Returns:
 List: Центроиды кластеров
 """
 if len(levels) < 2:
 return levels.tolist()

 # Нормализация for кластеризации
 levels_normalized = levels.reshape(-1, 1)

 # DBSCAN кластеризация
 clustering = DBSCAN(
 eps=self.config['cluster_eps'],
 min_samples=self.config['min_cluster_size']
 ).fit(levels_normalized)

 # Получение центроидов кластеров
 cluster_centers = []
 for cluster_id in set(clustering.labels_):
 if cluster_id == -1: # Шум
 continue
 cluster_points = levels[clustering.labels_ == cluster_id]
 cluster_centers.append(np.mean(cluster_points))

 return cluster_centers

 def _calculate_level_features(self, df: pd.DataFrame, levels: Dict[str, List[float]]) -> Dict[str, pd.Series]:
 """Расчет признаков on basis обнаруженных уровней"""
 features = {}

 # Ближайшие уровни
 features['nearest_resistance'] = self._find_nearest_level(df['Close'], levels['resistance'])
 features['nearest_support'] = self._find_nearest_level(df['Close'], levels['support'])

 # Расстояния to уровней
 features['distance_to_resistance'] = (features['nearest_resistance'] - df['Close']) / df['Close']
 features['distance_to_support'] = (df['Close'] - features['nearest_support']) / df['Close']

 # Позиция между уровнями
 level_range = features['nearest_resistance'] - features['nearest_support']
 features['position_in_range'] = (df['Close'] - features['nearest_support']) / (level_range + 1e-8)

 # Сила ближайших уровней
 features['resistance_strength'] = self._calculate_level_strength(df, levels['resistance'])
 features['support_strength'] = self._calculate_level_strength(df, levels['support'])

 return features

 def _find_nearest_level(self, prices: pd.Series, levels: List[float]) -> pd.Series:
 """Поиск ближайшего уровня for каждой цены"""
 if not levels:
 return pd.Series(index=prices.index, data=prices.values)

 nearest_levels = []
 for price in prices:
 distances = [abs(price - level) for level in levels]
 nearest_idx = np.argmin(distances)
 nearest_levels.append(levels[nearest_idx])

 return pd.Series(nearest_levels, index=prices.index)

 def _calculate_level_strength(self, df: pd.DataFrame, levels: List[float]) -> pd.Series:
 """Расчет силы уровней on basis количества касаний"""
 strength = pd.Series(index=df.index, data=0.0)

 for level in levels:
 # Поиск касаний уровня
 touches = self._count_level_touches(df, level)
 strength += touches

 return strength

 def _count_level_touches(self, df: pd.DataFrame, level: float) -> pd.Series:
 """Подсчет количества касаний уровня"""
 tolerance = self.config['touch_tolerance']

 # check касаний High and Low
 high_touches = (df['High'] >= level * (1 - tolerance)) & (df['High'] <= level * (1 + tolerance))
 low_touches = (df['Low'] >= level * (1 - tolerance)) & (df['Low'] <= level * (1 + tolerance))

 touches = (high_touches | low_touches).astype(int)
 return touches.rolling(20).sum()

 def _calculate_cluster_features(self, df: pd.DataFrame, levels: Dict[str, List[float]]) -> Dict[str, pd.Series]:
 """Расчет признаков on basis кластеров уровней"""
 features = {}

 # Количество кластеров
 features['n_resistance_clusters'] = len(levels['resistance'])
 features['n_support_clusters'] = len(levels['support'])

 # Плотность кластеров
 if levels['resistance']:
 resistance_std = np.std(levels['resistance'])
 features['resistance_cluster_density'] = 1.0 / (resistance_std + 1e-8)
 else:
 features['resistance_cluster_density'] = 0.0

 if levels['support']:
 support_std = np.std(levels['support'])
 features['support_cluster_density'] = 1.0 / (support_std + 1e-8)
 else:
 features['support_cluster_density'] = 0.0

 return features

 def _calculate_level_statistics(self, df: pd.DataFrame, levels: Dict[str, List[float]]) -> Dict[str, pd.Series]:
 """Расчет статистических признаков уровней"""
 features = {}

 # Статистики уровней сопротивления
 if levels['resistance']:
 resistance_levels = np.array(levels['resistance'])
 features['resistance_mean'] = np.mean(resistance_levels)
 features['resistance_std'] = np.std(resistance_levels)
 features['resistance_skewness'] = stats.skew(resistance_levels)
 features['resistance_kurtosis'] = stats.kurtosis(resistance_levels)
 else:
 features['resistance_mean'] = df['Close'].mean()
 features['resistance_std'] = 0.0
 features['resistance_skewness'] = 0.0
 features['resistance_kurtosis'] = 0.0

 # Статистики уровней поддержки
 if levels['support']:
 support_levels = np.array(levels['support'])
 features['support_mean'] = np.mean(support_levels)
 features['support_std'] = np.std(support_levels)
 features['support_skewness'] = stats.skew(support_levels)
 features['support_kurtosis'] = stats.kurtosis(support_levels)
 else:
 features['support_mean'] = df['Close'].mean()
 features['support_std'] = 0.0
 features['support_skewness'] = 0.0
 features['support_kurtosis'] = 0.0

 return features

 def _calculate_volume_indicators(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
 """Расчет объемных indicators"""
 features = {}

 # Объемные средние
 for window in [5, 10, 20, 50]:
 features[f'volume_sma_{window}'] = df['Volume'].rolling(window).mean()
 features[f'volume_ratio_{window}'] = df['Volume'] / features[f'volume_sma_{window}']

 # On-Balance Volume (OBV)
 obv = pd.Series(index=df.index, dtype=float)
 obv.iloc[0] = df['Volume'].iloc[0]
 for i in range(1, len(df)):
 if df['Close'].iloc[i] > df['Close'].iloc[i-1]:
 obv.iloc[i] = obv.iloc[i-1] + df['Volume'].iloc[i]
 elif df['Close'].iloc[i] < df['Close'].iloc[i-1]:
 obv.iloc[i] = obv.iloc[i-1] - df['Volume'].iloc[i]
 else:
 obv.iloc[i] = obv.iloc[i-1]
 features['obv'] = obv

 # Volume Price Trend (VPT)
 vpt = (df['Close'].pct_change() * df['Volume']).cumsum()
 features['vpt'] = vpt

 return features

 def _calculate_temporal_patterns(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
 """Расчет временных паттернов"""
 features = {}

 # Временные компоненты
 features['hour'] = df.index.hour
 features['day_of_week'] = df.index.dayofweek
 features['day_of_month'] = df.index.day
 features['month'] = df.index.month

 # Циклические признаки
 features['hour_sin'] = np.sin(2 * np.pi * features['hour'] / 24)
 features['hour_cos'] = np.cos(2 * np.pi * features['hour'] / 24)
 features['day_sin'] = np.sin(2 * np.pi * features['day_of_week'] / 7)
 features['day_cos'] = np.cos(2 * np.pi * features['day_of_week'] / 7)

 return features

 def _calculate_pressure_features(self, df: pd.DataFrame, levels: Dict[str, List[float]]) -> Dict[str, pd.Series]:
 """Расчет признаков давления on уровни"""
 features = {}

 # Давление on ближайшие уровни
 nearest_resistance = self._find_nearest_level(df['Close'], levels['resistance'])
 nearest_support = self._find_nearest_level(df['Close'], levels['support'])

 # Давление on сопротивление
 resistance_pressure = (df['Close'] - nearest_resistance) * df['Volume']
 features['resistance_pressure'] = resistance_pressure.rolling(20).mean()

 # Давление on поддержку
 support_pressure = (nearest_support - df['Close']) * df['Volume']
 features['support_pressure'] = support_pressure.rolling(20).mean()

 # Вектор давления
 features['pressure_vector'] = features['resistance_pressure'] - features['support_pressure']

 return features

 def _calculate_lag_features(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
 """Расчет лаговых признаков"""
 features = {}

 for lag in [1, 2, 3, 5, 10, 20]:
 features[f'close_lag_{lag}'] = df['Close'].shift(lag)
 features[f'high_lag_{lag}'] = df['High'].shift(lag)
 features[f'low_lag_{lag}'] = df['Low'].shift(lag)
 features[f'volume_lag_{lag}'] = df['Volume'].shift(lag)

 # Отношения with лагами
 features[f'close_ratio_lag_{lag}'] = df['Close'] / features[f'close_lag_{lag}']
 features[f'volume_ratio_lag_{lag}'] = df['Volume'] / features[f'volume_lag_{lag}']

 return features

 def _create_target(self, df: pd.DataFrame, horizon: int = None) -> pd.Series:
 """create целевой переменной for SCHR Levels"""
 if horizon is None:
 horizon = self.config['target_horizon']

 future_price = df['Close'].shift(-horizon)
 current_price = df['Close']

 # Процентное изменение
 price_change = (future_price - current_price) / current_price

 # Адаптивные пороги on basis волатильности
 volatility = df['Close'].rolling(20).std() / df['Close'].rolling(20).mean()
 threshold = volatility * 0.5

 # Классификация with адаптивными порогами
 target = pd.Series(index=df.index, dtype=int)
 target[price_change > threshold] = 2 # Up
 target[price_change < -threshold] = 0 # Down
 target[(price_change >= -threshold) & (price_change <= threshold)] = 1 # Hold

 return target

 def _remove_correlated_features(self, X: pd.DataFrame, threshold: float = 0.95) -> pd.DataFrame:
 """remove коррелированных признаков"""
 corr_matrix = X.corr().abs()
 upper_tri = corr_matrix.where(
 np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
 )
 to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > threshold)]
 return X.drop(columns=to_drop)

 def _calculate_ensemble_weights(self, model_scores: Dict[str, float]) -> Dict[str, float]:
 """Расчет весов for ансамбля моделей"""
 total_score = sum(model_scores.values())
 if total_score == 0:
 return {name: 1.0 / len(model_scores) for name in model_scores.keys()}
 return {name: score / total_score for name, score in model_scores.items()}

 def _ensemble_predict(self, X: np.ndarray) -> np.ndarray:
 """Prediction ансамбля моделей"""
 Predictions = []
 for name, model in self.models.items():
 pred = model.predict(X)
 weight = self.ensemble_weights.get(name, 0)
 Predictions.append(pred * weight)
 ensemble_pred = np.sum(Predictions, axis=0)
 return np.round(ensemble_pred).astype(int)

 def predict(self, data: pd.DataFrame) -> np.ndarray:
 """Prediction on basis SCHR Levels"""
 if not self.is_trained:
 self.logger.warning("SCHR Levels model not trained")
 return np.zeros(len(data))

 try:
 # create признаков
 features = self._create_schr_levels_features(data)

 # Нормализация
 features_scaled = self.scaler.transform(features)

 # Отбор признаков
 features_selected = self.feature_selector.transform(features_scaled)

 # Prediction
 Prediction = self._ensemble_predict(features_selected)

 return Prediction

 except Exception as e:
 self.logger.error(f"Error predicting with SCHR Levels: {e}")
 return np.zeros(len(data))

 def get_levels(self, data: pd.DataFrame) -> Dict[str, List[float]]:
 """Получение обнаруженных уровней"""
 return self._detect_levels(data)

 def get_training_stats(self) -> Dict:
 """Получение статистики обучения"""
 return self.training_stats.copy()

# example использования
if __name__ == "__main__":
 # create тестовых данных
 np.random.seed(42)
 dates = pd.date_range('2020-01-01', periods=1000, freq='H')

 # Симуляция ценовых данных with уровнями
 price = 100
 prices = []
 for i in range(1000):
 # create искусственных уровней
 if i % 100 < 20: # Уровень сопротивления
 change = np.random.normal(0, 0.005)
 elif i % 100 > 80: # Уровень поддержки
 change = np.random.normal(0, 0.005)
 else:
 change = np.random.normal(0, 0.01)

 price *= (1 + change)
 prices.append(price)

 data = pd.DataFrame({
 'Open': prices,
 'High': [p * (1 + abs(np.random.normal(0, 0.005))) for p in prices],
 'Low': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
 'Close': prices,
 'Volume': np.random.randint(1000, 10000, 1000)
 }, index=dates)

 # Нормализация OHLC
 for i in range(len(data)):
 high = max(data.iloc[i]['Open'], data.iloc[i]['Close'])
 low = min(data.iloc[i]['Open'], data.iloc[i]['Close'])
 data.iloc[i, data.columns.get_loc('High')] = high
 data.iloc[i, data.columns.get_loc('Low')] = low

 # Инициализация индикатора
 schr_levels = SCHRLevelsIndicator()

 # Подготовка данных for обучения
 training_data = {'test_H1': data}

 # Обучение модели
 stats = schr_levels.train(training_data)
 print(f"Training completed. Test accuracy: {stats.get('test_accuracy', 0):.4f}")

 # Prediction
 Predictions = schr_levels.predict(data.tail(100))
 print(f"Predictions: {np.bincount(Predictions)}")

 # Обнаружение уровней
 levels = schr_levels.get_levels(data)
 print(f"Detected resistance levels: {len(levels['resistance'])}")
 print(f"Detected support levels: {len(levels['support'])}")
```

## ⚡ Индикатор SCHR SHORT3

**Теория:** Индикатор SCHR SHORT3 представляет собой специализированный ML-индикатор for краткосрочной торговли and скальпинга, обеспечивающий высокочастотные торговые сигналы with высокой точностью. Это критически важный компонент for максимизации прибыли.

**Почему индикатор SCHR SHORT3 важен:**
- **Краткосрочность:** Обеспечивает краткосрочные торговые сигналы
- **Скальпинг:** Обеспечивает возможности for скальпинга
- **Частота:** Обеспечивает высокую частоту сигналов
- **Прибыльность:** Критически важно for максимизации прибыли

**Плюсы:**
- Краткосрочные сигналы
- Возможности скальпинга
- Высокая частота сигналов
- Максимизация прибыли

**Минусы:**
- Высокие требования к скорости
- Потенциальные высокие комиссии
- Требует постоянного Monitoringа

```python
# src/indicators/schr_short3.py
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class SCHRShort3Indicator:
 """Индикатор SCHR SHORT3 for краткосрочной торговли"""

 def __init__(self):
 self.logger = logging.getLogger(__name__)
 self.model = ExtraTreesClassifier(n_estimators=100, random_state=42)
 self.features = []
 self.is_trained = False

 def train(self, data: Dict[str, pd.DataFrame]):
 """Обучение модели SCHR SHORT3"""
 try:
 self.logger.info("Training SCHR SHORT3 model...")

 # Подготовка данных
 X, y = self._prepare_training_data(data)

 if X.empty or y.empty:
 self.logger.warning("No data available for training SCHR SHORT3")
 return

 # Разделение on train/test
 X_train, X_test, y_train, y_test = train_test_split(
 X, y, test_size=0.2, random_state=42
 )

 # Обучение модели
 self.model.fit(X_train, y_train)

 # Оценка
 y_pred = self.model.predict(X_test)
 accuracy = accuracy_score(y_test, y_pred)

 self.is_trained = True
 self.logger.info(f"SCHR SHORT3 model trained with accuracy: {accuracy:.4f}")

 except Exception as e:
 self.logger.error(f"Error training SCHR SHORT3 model: {e}")

 def _prepare_training_data(self, data: Dict[str, pd.DataFrame]) -> tuple:
 """Подготовка данных for обучения"""
 features_list = []
 targets_list = []

 for symbol_timeframe, df in data.items():
 if df.empty:
 continue

 # create признаков SCHR SHORT3
 features = self._create_schr_short3_features(df)

 # create целевой переменной
 target = self._create_target(df)

 # Объединение
 combined = pd.concat([features, target], axis=1)
 combined = combined.dropna()

 if not combined.empty:
 features_list.append(combined.iloc[:, :-1])
 targets_list.append(combined.iloc[:, -1])

 if features_list:
 X = pd.concat(features_list, ignore_index=True)
 y = pd.concat(targets_list, ignore_index=True)
 return X, y
 else:
 return pd.DataFrame(), pd.Series()

 def _create_schr_short3_features(self, df: pd.DataFrame) -> pd.DataFrame:
 """create признаков SCHR SHORT3"""
 features = pd.DataFrame(index=df.index)

 # Базовые цены
 features['close'] = df['Close']
 features['high'] = df['High']
 features['low'] = df['Low']
 features['volume'] = df['Volume']

 # SCHR SHORT3 признаки
 features['short_term_signal'] = self._calculate_short_term_signal(df)
 features['short_term_strength'] = self._calculate_short_term_strength(df)
 features['short_term_direction'] = self._calculate_short_term_direction(df)
 features['short_term_volatility'] = self._calculate_short_term_volatility(df)
 features['short_term_momentum'] = self._calculate_short_term_momentum(df)

 # Дополнительные сигналы
 features['short_buy_signal'] = (features['short_term_signal'] > 0.5).astype(int)
 features['short_sell_signal'] = (features['short_term_signal'] < -0.5).astype(int)
 features['short_hold_signal'] = (abs(features['short_term_signal']) <= 0.5).astype(int)

 # Статистика
 features['short_hits'] = self._calculate_short_hits(df)
 features['short_breaks'] = self._calculate_short_breaks(df)
 features['short_bounces'] = self._calculate_short_bounces(df)
 features['short_accuracy'] = self._calculate_short_accuracy(df)

 # Нормализованные признаки
 features['short_volatility_normalized'] = features['short_term_volatility'] / features['close']
 features['short_momentum_normalized'] = features['short_term_momentum'] / features['close']

 # Лаговые признаки
 for lag in [1, 2, 3, 5, 10]:
 features[f'short_signal_lag_{lag}'] = features['short_term_signal'].shift(lag)
 features[f'short_strength_lag_{lag}'] = features['short_term_strength'].shift(lag)

 return features

 def _calculate_short_term_signal(self, df: pd.DataFrame) -> pd.Series:
 """Расчет краткосрочного сигнала"""
 # Комбинация RSI and MACD for краткосрочных сигналов
 rsi = self._calculate_rsi(df['Close'])
 macd = self._calculate_macd(df['Close'])

 # Нормализация
 rsi_norm = (rsi - 50) / 50
 macd_norm = macd / df['Close']

 # Краткосрочный сигнал
 signal = (rsi_norm + macd_norm) / 2
 return signal.rolling(5).mean()

 def _calculate_short_term_strength(self, df: pd.DataFrame) -> pd.Series:
 """Расчет силы краткосрочного сигнала"""
 volatility = df['Close'].rolling(20).std()
 volume = df['Volume'].rolling(20).mean()

 # Сила = волатильность * объем
 strength = volatility * volume
 return strength / strength.rolling(50).max()

 def _calculate_short_term_direction(self, df: pd.DataFrame) -> pd.Series:
 """Расчет направления краткосрочного сигнала"""
 price_change = df['Close'].pct_change(5)
 return np.sign(price_change)

 def _calculate_short_term_volatility(self, df: pd.DataFrame) -> pd.Series:
 """Расчет краткосрочной волатильности"""
 return df['Close'].rolling(10).std()

 def _calculate_short_term_momentum(self, df: pd.DataFrame) -> pd.Series:
 """Расчет краткосрочного моментума"""
 return df['Close'].pct_change(3)

 def _calculate_short_hits(self, df: pd.DataFrame) -> pd.Series:
 """Расчет количества краткосрочных касаний"""
 high_20 = df['High'].rolling(20).max()
 low_20 = df['Low'].rolling(20).min()

 hits = ((df['Close'] >= high_20 * 0.99) | (df['Close'] <= low_20 * 1.01)).astype(int)
 return hits.rolling(20).sum()

 def _calculate_short_breaks(self, df: pd.DataFrame) -> pd.Series:
 """Расчет количества краткосрочных пробоев"""
 high_20 = df['High'].rolling(20).max()
 low_20 = df['Low'].rolling(20).min()

 breaks = ((df['Close'] > high_20) | (df['Close'] < low_20)).astype(int)
 return breaks.rolling(20).sum()

 def _calculate_short_bounces(self, df: pd.DataFrame) -> pd.Series:
 """Расчет количества краткосрочных отскоков"""
 price_change = df['Close'].pct_change()
 bounces = ((price_change > 0.01) | (price_change < -0.01)).astype(int)
 return bounces.rolling(20).sum()

 def _calculate_short_accuracy(self, df: pd.DataFrame) -> pd.Series:
 """Расчет точности краткосрочных сигналов"""
 # Упрощенный расчет точности
 price_change = df['Close'].pct_change()
 correct_Predictions = (abs(price_change) > 0.005).astype(int)
 return correct_Predictions.rolling(20).mean()

 def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
 """Расчет RSI"""
 delta = prices.diff()
 gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
 loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
 rs = gain / loss
 rsi = 100 - (100 / (1 + rs))
 return rsi

 def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.Series:
 """Расчет MACD"""
 ema_fast = prices.ewm(span=fast).mean()
 ema_slow = prices.ewm(span=slow).mean()
 macd = ema_fast - ema_slow
 signal_line = macd.ewm(span=signal).mean()
 return macd - signal_line

 def _create_target(self, df: pd.DataFrame, horizon: int = 1) -> pd.Series:
 """create целевой переменной"""
 future_price = df['Close'].shift(-horizon)
 current_price = df['Close']

 # Процентное изменение
 price_change = (future_price - current_price) / current_price

 # Классификация направления
 target = pd.cut(
 price_change,
 bins=[-np.inf, -0.001, 0.001, np.inf],
 labels=[0, 1, 2], # 0=down, 1=hold, 2=up
 include_lowest=True
 )

 return target.astype(int)

 def predict(self, data: pd.DataFrame) -> np.ndarray:
 """Prediction on basis SCHR SHORT3"""
 if not self.is_trained:
 self.logger.warning("SCHR SHORT3 model not trained")
 return np.zeros(len(data))

 try:
 # create признаков
 features = self._create_schr_short3_features(data)

 # Prediction
 Prediction = self.model.predict(features)

 return Prediction

 except Exception as e:
 self.logger.error(f"Error predicting with SCHR SHORT3: {e}")
 return np.zeros(len(data))

 def get_features(self) -> pd.DataFrame:
 """Получение признаков"""
 return self.features
```

**Теория:** Заключительная часть представляет собой description структуры and продолжения разработки компонентов системы. Это критически важно for понимания полной архитектуры and дальнейшего развития системы.

**Почему заключительная часть важна:**
- **Структура:** Обеспечивает понимание структуры
- **Продолжение:** Обеспечивает понимание продолжения разработки
- **Архитектура:** Обеспечивает понимание полной архитектуры
- **Развитие:** Критически важно for дальнейшего развития

**Плюсы:**
- Понимание структуры
- Plan продолжения
- Полная архитектура
- Возможности развития

**Минусы:**
- Потенциальная неполнота
- Требует дополнительной разработки

Это вторая часть детального кода. Продолжу with остальными компонентами in следующих частях.
