# 18.2. Детальные компоненты системы

## 📊 Сборщик данных

```python
# src/data/collectors.py
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

class DataCollector:
    """Сборщик данных для всех активов и таймфреймов"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.data_cache = {}
        
    def collect_data(self, symbol: str, timeframe: str, period: str = "2y") -> pd.DataFrame:
        """Сбор данных для символа и таймфрейма"""
        try:
            # Преобразование таймфрейма для yfinance
            interval_map = {
                'M1': '1m',
                'M5': '5m',
                'M15': '15m',
                'H1': '1h',
                'H4': '4h',
                'D1': '1d'
            }
            
            interval = interval_map.get(timeframe, '1h')
            
            # Сбор данных
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                self.logger.warning(f"No data found for {symbol} {timeframe}")
                return pd.DataFrame()
            
            # Очистка данных
            data = self._clean_data(data)
            
            # Добавление метаданных
            data['symbol'] = symbol
            data['timeframe'] = timeframe
            data['timestamp'] = data.index
            
            # Кэширование
            cache_key = f"{symbol}_{timeframe}"
            self.data_cache[cache_key] = data
            
            self.logger.info(f"Collected {len(data)} records for {symbol} {timeframe}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error collecting data for {symbol} {timeframe}: {e}")
            return pd.DataFrame()
    
    def _clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Очистка данных"""
        # Удаление NaN
        data = data.dropna()
        
        # Удаление дубликатов
        data = data[~data.index.duplicated(keep='first')]
        
        # Проверка на аномалии
        data = self._remove_anomalies(data)
        
        return data
    
    def _remove_anomalies(self, data: pd.DataFrame) -> pd.DataFrame:
        """Удаление аномалий"""
        # Удаление нулевых цен
        data = data[data['Close'] > 0]
        
        # Удаление экстремальных значений
        for col in ['Open', 'High', 'Low', 'Close']:
            if col in data.columns:
                q1 = data[col].quantile(0.01)
                q99 = data[col].quantile(0.99)
                data = data[(data[col] >= q1) & (data[col] <= q99)]
        
        return data
    
    def get_current_data(self) -> Dict[str, pd.DataFrame]:
        """Получение текущих данных"""
        current_data = {}
        
        for asset_type, assets in self.config['data_sources'].items():
            for asset in assets:
                symbol = asset['symbol']
                for timeframe in self.config['timeframes']:
                    cache_key = f"{symbol}_{timeframe}"
                    if cache_key in self.data_cache:
                        current_data[cache_key] = self.data_cache[cache_key]
        
        return current_data
    
    def get_all_data(self) -> Dict[str, pd.DataFrame]:
        """Получение всех данных"""
        return self.data_cache
    
    def save_data(self, data: pd.DataFrame, symbol: str, timeframe: str):
        """Сохранение данных"""
        if data.empty:
            return
        
        # Создание директории
        data_dir = Path(f"data/raw/{symbol}")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Сохранение в parquet
        file_path = data_dir / f"{timeframe}.parquet"
        data.to_parquet(file_path)
        
        self.logger.info(f"Data saved to {file_path}")
```

## 🎯 Индикатор WAVE2

```python
# src/indicators/wave2.py
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class Wave2Indicator:
    """Индикатор WAVE2 для анализа трендов"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.features = []
        self.is_trained = False
        
    def train(self, data: Dict[str, pd.DataFrame]):
        """Обучение модели WAVE2"""
        try:
            self.logger.info("Training WAVE2 model...")
            
            # Подготовка данных
            X, y = self._prepare_training_data(data)
            
            if X.empty or y.empty:
                self.logger.warning("No data available for training WAVE2")
                return
            
            # Разделение на train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Обучение модели
            self.model.fit(X_train, y_train)
            
            # Оценка
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            self.is_trained = True
            self.logger.info(f"WAVE2 model trained with accuracy: {accuracy:.4f}")
            
        except Exception as e:
            self.logger.error(f"Error training WAVE2 model: {e}")
    
    def _prepare_training_data(self, data: Dict[str, pd.DataFrame]) -> tuple:
        """Подготовка данных для обучения"""
        features_list = []
        targets_list = []
        
        for symbol_timeframe, df in data.items():
            if df.empty:
                continue
            
            # Создание признаков WAVE2
            features = self._create_wave2_features(df)
            
            # Создание целевой переменной
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
    
    def _create_wave2_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Создание признаков WAVE2"""
        features = pd.DataFrame(index=df.index)
        
        # Базовые цены
        features['close'] = df['Close']
        features['high'] = df['High']
        features['low'] = df['Low']
        features['volume'] = df['Volume']
        
        # WAVE2-подобные признаки
        features['price_momentum'] = df['Close'].pct_change(5)
        features['volume_momentum'] = df['Volume'].pct_change(5)
        features['volatility'] = df['Close'].rolling(20).std()
        
        # Скользящие средние
        for window in [5, 10, 20, 50]:
            features[f'sma_{window}'] = df['Close'].rolling(window).mean()
            features[f'std_{window}'] = df['Close'].rolling(window).std()
        
        # RSI
        features['rsi'] = self._calculate_rsi(df['Close'])
        
        # MACD
        features['macd'] = self._calculate_macd(df['Close'])
        
        # Лаговые признаки
        for lag in [1, 2, 3, 5, 10]:
            features[f'close_lag_{lag}'] = df['Close'].shift(lag)
            features[f'volume_lag_{lag}'] = df['Volume'].shift(lag)
        
        return features
    
    def _create_target(self, df: pd.DataFrame, horizon: int = 1) -> pd.Series:
        """Создание целевой переменной"""
        future_price = df['Close'].shift(-horizon)
        current_price = df['Close']
        
        # Процентное изменение
        price_change = (future_price - current_price) / current_price
        
        # Классификация направления
        target = pd.cut(
            price_change,
            bins=[-np.inf, -0.001, 0.001, np.inf],
            labels=[0, 1, 2],  # 0=down, 1=hold, 2=up
            include_lowest=True
        )
        
        return target.astype(int)
    
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
    
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """Предсказание на основе WAVE2"""
        if not self.is_trained:
            self.logger.warning("WAVE2 model not trained")
            return np.zeros(len(data))
        
        try:
            # Создание признаков
            features = self._create_wave2_features(data)
            
            # Предсказание
            prediction = self.model.predict(features)
            
            return prediction
            
        except Exception as e:
            self.logger.error(f"Error predicting with WAVE2: {e}")
            return np.zeros(len(data))
    
    def get_features(self) -> pd.DataFrame:
        """Получение признаков"""
        return self.features
```

## 📈 Индикатор SCHR Levels

```python
# src/indicators/schr_levels.py
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class SCHRLevelsIndicator:
    """Индикатор SCHR Levels для анализа уровней поддержки и сопротивления"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.features = []
        self.is_trained = False
        
    def train(self, data: Dict[str, pd.DataFrame]):
        """Обучение модели SCHR Levels"""
        try:
            self.logger.info("Training SCHR Levels model...")
            
            # Подготовка данных
            X, y = self._prepare_training_data(data)
            
            if X.empty or y.empty:
                self.logger.warning("No data available for training SCHR Levels")
                return
            
            # Разделение на train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Обучение модели
            self.model.fit(X_train, y_train)
            
            # Оценка
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            self.is_trained = True
            self.logger.info(f"SCHR Levels model trained with accuracy: {accuracy:.4f}")
            
        except Exception as e:
            self.logger.error(f"Error training SCHR Levels model: {e}")
    
    def _prepare_training_data(self, data: Dict[str, pd.DataFrame]) -> tuple:
        """Подготовка данных для обучения"""
        features_list = []
        targets_list = []
        
        for symbol_timeframe, df in data.items():
            if df.empty:
                continue
            
            # Создание признаков SCHR Levels
            features = self._create_schr_levels_features(df)
            
            # Создание целевой переменной
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
    
    def _create_schr_levels_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Создание признаков SCHR Levels"""
        features = pd.DataFrame(index=df.index)
        
        # Базовые цены
        features['close'] = df['Close']
        features['high'] = df['High']
        features['low'] = df['Low']
        features['volume'] = df['Volume']
        
        # SCHR Levels признаки
        features['predicted_high'] = self._calculate_predicted_high(df)
        features['predicted_low'] = self._calculate_predicted_low(df)
        features['pressure'] = self._calculate_pressure(df)
        features['pressure_vector'] = self._calculate_pressure_vector(df)
        
        # Расстояния до уровней
        features['distance_to_high'] = (features['predicted_high'] - features['close']) / features['close']
        features['distance_to_low'] = (features['close'] - features['predicted_low']) / features['close']
        features['level_range'] = (features['predicted_high'] - features['predicted_low']) / features['close']
        
        # Позиция относительно уровней
        features['position_in_range'] = (features['close'] - features['predicted_low']) / (features['predicted_high'] - features['predicted_low'])
        
        # Давление на уровни
        features['pressure_normalized'] = features['pressure'] / features['close']
        features['pressure_vector_normalized'] = features['pressure_vector'] / features['close']
        
        # Изменения давления
        features['pressure_change'] = features['pressure'].diff()
        features['pressure_vector_change'] = features['pressure_vector'].diff()
        
        # Лаговые признаки
        for lag in [1, 2, 3, 5, 10]:
            features[f'pressure_lag_{lag}'] = features['pressure'].shift(lag)
            features[f'pressure_vector_lag_{lag}'] = features['pressure_vector'].shift(lag)
        
        return features
    
    def _calculate_predicted_high(self, df: pd.DataFrame) -> pd.Series:
        """Расчет предсказанного максимума"""
        high_20 = df['High'].rolling(20).max()
        high_50 = df['High'].rolling(50).max()
        return (high_20 + high_50) / 2
    
    def _calculate_predicted_low(self, df: pd.DataFrame) -> pd.Series:
        """Расчет предсказанного минимума"""
        low_20 = df['Low'].rolling(20).min()
        low_50 = df['Low'].rolling(50).min()
        return (low_20 + low_50) / 2
    
    def _calculate_pressure(self, df: pd.DataFrame) -> pd.Series:
        """Расчет давления"""
        price_change = df['Close'].pct_change()
        volume = df['Volume']
        pressure = price_change * volume
        return pressure.rolling(20).mean()
    
    def _calculate_pressure_vector(self, df: pd.DataFrame) -> pd.Series:
        """Расчет вектора давления"""
        pressure = self._calculate_pressure(df)
        return pressure.diff()
    
    def _create_target(self, df: pd.DataFrame, horizon: int = 1) -> pd.Series:
        """Создание целевой переменной"""
        future_price = df['Close'].shift(-horizon)
        current_price = df['Close']
        
        # Процентное изменение
        price_change = (future_price - current_price) / current_price
        
        # Классификация направления
        target = pd.cut(
            price_change,
            bins=[-np.inf, -0.001, 0.001, np.inf],
            labels=[0, 1, 2],  # 0=down, 1=hold, 2=up
            include_lowest=True
        )
        
        return target.astype(int)
    
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """Предсказание на основе SCHR Levels"""
        if not self.is_trained:
            self.logger.warning("SCHR Levels model not trained")
            return np.zeros(len(data))
        
        try:
            # Создание признаков
            features = self._create_schr_levels_features(data)
            
            # Предсказание
            prediction = self.model.predict(features)
            
            return prediction
            
        except Exception as e:
            self.logger.error(f"Error predicting with SCHR Levels: {e}")
            return np.zeros(len(data))
    
    def get_features(self) -> pd.DataFrame:
        """Получение признаков"""
        return self.features
```

## ⚡ Индикатор SCHR SHORT3

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
    """Индикатор SCHR SHORT3 для краткосрочной торговли"""
    
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
            
            # Разделение на train/test
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
        """Подготовка данных для обучения"""
        features_list = []
        targets_list = []
        
        for symbol_timeframe, df in data.items():
            if df.empty:
                continue
            
            # Создание признаков SCHR SHORT3
            features = self._create_schr_short3_features(df)
            
            # Создание целевой переменной
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
        """Создание признаков SCHR SHORT3"""
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
        # Комбинация RSI и MACD для краткосрочных сигналов
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
        correct_predictions = (abs(price_change) > 0.005).astype(int)
        return correct_predictions.rolling(20).mean()
    
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
        """Создание целевой переменной"""
        future_price = df['Close'].shift(-horizon)
        current_price = df['Close']
        
        # Процентное изменение
        price_change = (future_price - current_price) / current_price
        
        # Классификация направления
        target = pd.cut(
            price_change,
            bins=[-np.inf, -0.001, 0.001, np.inf],
            labels=[0, 1, 2],  # 0=down, 1=hold, 2=up
            include_lowest=True
        )
        
        return target.astype(int)
    
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """Предсказание на основе SCHR SHORT3"""
        if not self.is_trained:
            self.logger.warning("SCHR SHORT3 model not trained")
            return np.zeros(len(data))
        
        try:
            # Создание признаков
            features = self._create_schr_short3_features(data)
            
            # Предсказание
            prediction = self.model.predict(features)
            
            return prediction
            
        except Exception as e:
            self.logger.error(f"Error predicting with SCHR SHORT3: {e}")
            return np.zeros(len(data))
    
    def get_features(self) -> pd.DataFrame:
        """Получение признаков"""
        return self.features
```

Это вторая часть детального кода. Продолжу с остальными компонентами в следующих частях.
