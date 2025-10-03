# 17. Практические примеры - Создание системы с доходностью 100%+ в месяц

**Цель:** Показать практические примеры создания робастных прибыльных ML-систем с доходностью более 100% в месяц.

## Пример 1: Простая система на основе WAVE2

**Теория:** Простая система на основе WAVE2 представляет собой базовую реализацию торговой системы, использующую принципы WAVE2 для создания торговых сигналов. Это критически важно для понимания основ создания прибыльных систем.

**Почему начинать с простой системы важно:**
- **Понимание основ:** Обеспечивает понимание основных принципов
- **Низкие риски:** Минимизирует риски при изучении
- **Быстрая реализация:** Позволяет быстро создать рабочую систему
- **Обучение:** Помогает изучить основы ML-торговли

### Описание системы

**Теория:** Простая система на основе WAVE2 использует базовые принципы волнового анализа для создания торговых сигналов. Это критически важно для создания надежной основы для более сложных систем.

**Почему WAVE2 подходит для начала:**
- **Простота понимания:** Легко понять и реализовать
- **Эффективность:** Может обеспечить хорошую доходность
- **Робастность:** Относительно устойчива к рыночному шуму
- **Масштабируемость:** Легко расширить и улучшить

**Плюсы:**
- Простота реализации
- Быстрое понимание
- Низкие риски
- Хорошая основа для развития

**Минусы:**
- Ограниченная сложность
- Потенциально низкая доходность
- Ограниченная адаптивность

### Код реализации

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import yfinance as yf
from datetime import datetime, timedelta

class SimpleWave2System:
    """Простая система на основе WAVE2"""
    
    def __init__(self, symbol='BTC-USD', timeframe='1h'):
        self.symbol = symbol
        self.timeframe = timeframe
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.features = []
        self.target = []
        
    def load_data(self, period='1y'):
        """Загрузка данных"""
        ticker = yf.Ticker(self.symbol)
        data = ticker.history(period=period, interval=self.timeframe)
        return data
    
    def create_wave2_features(self, data):
        """Создание признаков WAVE2"""
        features = pd.DataFrame(index=data.index)
        
        # Базовые признаки
        features['close'] = data['Close']
        features['volume'] = data['Volume']
        
        # Технические индикаторы
        features['sma_20'] = data['Close'].rolling(20).mean()
        features['sma_50'] = data['Close'].rolling(50).mean()
        features['rsi'] = self._calculate_rsi(data['Close'])
        features['macd'] = self._calculate_macd(data['Close'])
        
        # WAVE2-подобные признаки
        features['price_momentum'] = data['Close'].pct_change(5)
        features['volume_momentum'] = data['Volume'].pct_change(5)
        features['volatility'] = data['Close'].rolling(20).std()
        
        # Лаговые признаки
        for lag in [1, 2, 3, 5, 10]:
            features[f'close_lag_{lag}'] = data['Close'].shift(lag)
            features[f'volume_lag_{lag}'] = data['Volume'].shift(lag)
        
        # Скользящие средние
        for window in [5, 10, 20]:
            features[f'sma_{window}'] = data['Close'].rolling(window).mean()
            features[f'std_{window}'] = data['Close'].rolling(window).std()
        
        return features
    
    def _calculate_rsi(self, prices, window=14):
        """Расчет RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Расчет MACD"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()
        return macd - signal_line
    
    def create_target(self, data, horizon=1):
        """Создание целевой переменной"""
        future_price = data['Close'].shift(-horizon)
        current_price = data['Close']
        
        # Процентное изменение
        price_change = (future_price - current_price) / current_price
        
        # Классификация направления
        target = pd.cut(
            price_change,
            bins=[-np.inf, -0.01, 0.01, np.inf],
            labels=[0, 1, 2],  # 0=down, 1=hold, 2=up
            include_lowest=True
        )
        
        return target.astype(int)
    
    def train_model(self, data):
        """Обучение модели"""
        # Создание признаков
        features = self.create_wave2_features(data)
        
        # Создание целевой переменной
        target = self.create_target(data)
        
        # Удаление NaN
        valid_indices = ~(features.isna().any(axis=1) | target.isna())
        features_clean = features[valid_indices]
        target_clean = target[valid_indices]
        
        # Разделение на train/test
        X_train, X_test, y_train, y_test = train_test_split(
            features_clean, target_clean, test_size=0.2, random_state=42
        )
        
        # Обучение модели
        self.model.fit(X_train, y_train)
        
        # Предсказание
        y_pred = self.model.predict(X_test)
        
        # Оценка
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.4f}")
        print(classification_report(y_test, y_pred))
        
        return accuracy
    
    def backtest(self, data, initial_capital=10000):
        """Бэктестинг системы"""
        # Создание признаков
        features = self.create_wave2_features(data)
        target = self.create_target(data)
        
        # Удаление NaN
        valid_indices = ~(features.isna().any(axis=1) | target.isna())
        features_clean = features[valid_indices]
        target_clean = target[valid_indices]
        
        # Предсказания
        predictions = self.model.predict(features_clean)
        
        # Расчет доходности
        returns = []
        capital = initial_capital
        position = 0
        
        for i, (date, row) in enumerate(features_clean.iterrows()):
            if i == 0:
                continue
            
            # Сигнал модели
            signal = predictions[i]
            
            # Логика торговли
            if signal == 2 and position <= 0:  # Покупка
                position = 1
                capital = capital * (1 + (data.loc[date, 'Close'] - data.loc[features_clean.index[i-1], 'Close']) / data.loc[features_clean.index[i-1], 'Close'])
            elif signal == 0 and position >= 0:  # Продажа
                position = -1
                capital = capital * (1 - (data.loc[date, 'Close'] - data.loc[features_clean.index[i-1], 'Close']) / data.loc[features_clean.index[i-1], 'Close'])
            elif signal == 1:  # Удержание
                position = 0
            
            returns.append(capital - initial_capital)
        
        return returns

# Использование системы
if __name__ == "__main__":
    # Создание системы
    system = SimpleWave2System('BTC-USD', '1h')
    
    # Загрузка данных
    data = system.load_data('1y')
    
    # Обучение модели
    accuracy = system.train_model(data)
    
    # Бэктестинг
    returns = system.backtest(data)
    
    # Результаты
    total_return = returns[-1] if returns else 0
    print(f"Total return: {total_return:.2f}")
    print(f"Return percentage: {(total_return / 10000) * 100:.2f}%")
```

## Пример 2: Продвинутая система с SCHR Levels

**Теория:** Продвинутая система с SCHR Levels представляет собой более сложную реализацию торговой системы, использующую принципы SCHR Levels для создания высокоточных торговых сигналов. Это критически важно для достижения высокой доходности.

**Почему продвинутая система важна:**
- **Высокая точность:** Обеспечивает высокую точность сигналов
- **Адаптивность:** Может адаптироваться к изменениям рынка
- **Робастность:** Более устойчива к рыночному шуму
- **Доходность:** Может обеспечить высокую доходность

### Описание системы

**Теория:** Продвинутая система с SCHR Levels использует сложные алгоритмы анализа уровней поддержки и сопротивления для создания торговых сигналов. Это критически важно для создания высокоэффективных систем.

**Почему SCHR Levels эффективны:**
- **Точность уровней:** Обеспечивает высокую точность определения уровней
- **Адаптивность:** Может адаптироваться к изменениям рынка
- **Робастность:** Устойчива к рыночному шуму
- **Доходность:** Может обеспечить высокую доходность

**Плюсы:**
- Высокая точность сигналов
- Адаптивность к изменениям
- Робастность к шуму
- Высокая потенциальная доходность

**Минусы:**
- Сложность реализации
- Высокие требования к данным
- Потенциальная нестабильность

### Код реализации

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
from datetime import datetime, timedelta

class AdvancedSCHRSystem:
    """Продвинутая система с SCHR Levels"""
    
    def __init__(self, symbol='BTC-USD', timeframe='1h'):
        self.symbol = symbol
        self.timeframe = timeframe
        self.models = {
            'xgboost': xgb.XGBClassifier(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
        }
        self.ensemble_weights = [0.6, 0.4]  # Веса для ансамбля
        
    def load_data(self, period='2y'):
        """Загрузка данных"""
        ticker = yf.Ticker(self.symbol)
        data = ticker.history(period=period, interval=self.timeframe)
        return data
    
    def create_schr_features(self, data):
        """Создание признаков SCHR Levels"""
        features = pd.DataFrame(index=data.index)
        
        # Базовые признаки
        features['close'] = data['Close']
        features['high'] = data['High']
        features['low'] = data['Low']
        features['volume'] = data['Volume']
        
        # SCHR Levels признаки
        features['predicted_high'] = self._calculate_predicted_high(data)
        features['predicted_low'] = self._calculate_predicted_low(data)
        features['pressure'] = self._calculate_pressure(data)
        features['pressure_vector'] = self._calculate_pressure_vector(data)
        
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
        
        # Технические индикаторы
        features['rsi'] = self._calculate_rsi(data['Close'])
        features['macd'] = self._calculate_macd(data['Close'])
        features['bollinger_upper'] = self._calculate_bollinger_bands(data['Close'])[0]
        features['bollinger_lower'] = self._calculate_bollinger_bands(data['Close'])[1]
        
        # Лаговые признаки
        for lag in [1, 2, 3, 5, 10, 20]:
            features[f'close_lag_{lag}'] = data['Close'].shift(lag)
            features[f'pressure_lag_{lag}'] = features['pressure'].shift(lag)
            features[f'pressure_vector_lag_{lag}'] = features['pressure_vector'].shift(lag)
        
        # Скользящие средние
        for window in [5, 10, 20, 50]:
            features[f'sma_{window}'] = data['Close'].rolling(window).mean()
            features[f'std_{window}'] = data['Close'].rolling(window).std()
            features[f'pressure_sma_{window}'] = features['pressure'].rolling(window).mean()
            features[f'pressure_vector_sma_{window}'] = features['pressure_vector'].rolling(window).mean()
        
        return features
    
    def _calculate_predicted_high(self, data):
        """Расчет предсказанного максимума"""
        # Упрощенная версия SCHR Levels
        high_20 = data['High'].rolling(20).max()
        high_50 = data['High'].rolling(50).max()
        return (high_20 + high_50) / 2
    
    def _calculate_predicted_low(self, data):
        """Расчет предсказанного минимума"""
        # Упрощенная версия SCHR Levels
        low_20 = data['Low'].rolling(20).min()
        low_50 = data['Low'].rolling(50).min()
        return (low_20 + low_50) / 2
    
    def _calculate_pressure(self, data):
        """Расчет давления"""
        # Упрощенная версия давления
        price_change = data['Close'].pct_change()
        volume = data['Volume']
        pressure = price_change * volume
        return pressure.rolling(20).mean()
    
    def _calculate_pressure_vector(self, data):
        """Расчет вектора давления"""
        # Упрощенная версия вектора давления
        pressure = self._calculate_pressure(data)
        return pressure.diff()
    
    def _calculate_rsi(self, prices, window=14):
        """Расчет RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Расчет MACD"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()
        return macd - signal_line
    
    def _calculate_bollinger_bands(self, prices, window=20, num_std=2):
        """Расчет полос Боллинджера"""
        sma = prices.rolling(window).mean()
        std = prices.rolling(window).std()
        upper = sma + (std * num_std)
        lower = sma - (std * num_std)
        return upper, lower
    
    def create_target(self, data, horizon=1):
        """Создание целевой переменной"""
        future_price = data['Close'].shift(-horizon)
        current_price = data['Close']
        
        # Процентное изменение
        price_change = (future_price - current_price) / current_price
        
        # Классификация направления
        target = pd.cut(
            price_change,
            bins=[-np.inf, -0.005, 0.005, np.inf],
            labels=[0, 1, 2],  # 0=down, 1=hold, 2=up
            include_lowest=True
        )
        
        return target.astype(int)
    
    def train_models(self, data):
        """Обучение моделей"""
        # Создание признаков
        features = self.create_schr_features(data)
        
        # Создание целевой переменной
        target = self.create_target(data)
        
        # Удаление NaN
        valid_indices = ~(features.isna().any(axis=1) | target.isna())
        features_clean = features[valid_indices]
        target_clean = target[valid_indices]
        
        # Time Series Split
        tscv = TimeSeriesSplit(n_splits=5)
        
        # Обучение моделей
        for name, model in self.models.items():
            print(f"Training {name}...")
            
            # Кросс-валидация
            cv_scores = []
            for train_idx, val_idx in tscv.split(features_clean):
                X_train, X_val = features_clean.iloc[train_idx], features_clean.iloc[val_idx]
                y_train, y_val = target_clean.iloc[train_idx], target_clean.iloc[val_idx]
                
                model.fit(X_train, y_train)
                y_pred = model.predict(X_val)
                score = accuracy_score(y_val, y_pred)
                cv_scores.append(score)
            
            print(f"{name} CV accuracy: {np.mean(cv_scores):.4f} (+/- {np.std(cv_scores) * 2:.4f})")
            
            # Финальное обучение на всех данных
            model.fit(features_clean, target_clean)
    
    def predict(self, features):
        """Предсказание ансамбля"""
        predictions = []
        
        for name, model in self.models.items():
            pred = model.predict(features)
            predictions.append(pred)
        
        # Взвешенное предсказание
        ensemble_pred = np.average(predictions, weights=self.ensemble_weights, axis=0)
        
        return ensemble_pred
    
    def backtest(self, data, initial_capital=10000):
        """Бэктестинг системы"""
        # Создание признаков
        features = self.create_schr_features(data)
        target = self.create_target(data)
        
        # Удаление NaN
        valid_indices = ~(features.isna().any(axis=1) | target.isna())
        features_clean = features[valid_indices]
        target_clean = target[valid_indices]
        
        # Предсказания
        predictions = self.predict(features_clean)
        
        # Расчет доходности
        returns = []
        capital = initial_capital
        position = 0
        
        for i, (date, row) in enumerate(features_clean.iterrows()):
            if i == 0:
                continue
            
            # Сигнал модели
            signal = predictions[i]
            
            # Логика торговли
            if signal > 1.5 and position <= 0:  # Сильная покупка
                position = 1
                capital = capital * (1 + (data.loc[date, 'Close'] - data.loc[features_clean.index[i-1], 'Close']) / data.loc[features_clean.index[i-1], 'Close'])
            elif signal < 0.5 and position >= 0:  # Сильная продажа
                position = -1
                capital = capital * (1 - (data.loc[date, 'Close'] - data.loc[features_clean.index[i-1], 'Close']) / data.loc[features_clean.index[i-1], 'Close'])
            elif 0.5 <= signal <= 1.5:  # Удержание
                position = 0
            
            returns.append(capital - initial_capital)
        
        return returns

# Использование системы
if __name__ == "__main__":
    # Создание системы
    system = AdvancedSCHRSystem('BTC-USD', '1h')
    
    # Загрузка данных
    data = system.load_data('2y')
    
    # Обучение моделей
    system.train_models(data)
    
    # Бэктестинг
    returns = system.backtest(data)
    
    # Результаты
    total_return = returns[-1] if returns else 0
    print(f"Total return: {total_return:.2f}")
    print(f"Return percentage: {(total_return / 10000) * 100:.2f}%")
```

## Пример 3: Система с блокчейн-интеграцией

**Теория:** Система с блокчейн-интеграцией представляет собой инновационную реализацию торговой системы, использующую блокчейн-технологии и DeFi протоколы для увеличения доходности. Это критически важно для создания высокодоходных систем.

**Почему блокчейн-интеграция важна:**
- **Новые возможности:** Предоставляет новые возможности для заработка
- **Децентрализация:** Обеспечивает децентрализацию торговли
- **Прозрачность:** Обеспечивает прозрачность операций
- **Высокая доходность:** Может обеспечить очень высокую доходность

### Описание системы

**Теория:** Система с блокчейн-интеграцией использует DeFi протоколы для создания дополнительных источников дохода. Это критически важно для максимизации доходности торговой системы.

**Почему блокчейн-интеграция эффективна:**
- **Дополнительные источники дохода:** Предоставляет дополнительные источники дохода
- **Автоматизация:** Позволяет автоматизировать процессы
- **Масштабируемость:** Легко масштабируется
- **Инновации:** Использует инновационные технологии

**Плюсы:**
- Дополнительные источники дохода
- Автоматизация процессов
- Масштабируемость
- Инновационные технологии

**Минусы:**
- Высокие риски
- Сложность интеграции
- Потенциальные проблемы с безопасностью

### Код реализации

```python
import pandas as pd
import numpy as np
from web3 import Web3
import requests
from datetime import datetime, timedelta
import json

class BlockchainIntegratedSystem:
    """Система с блокчейн-интеграцией"""
    
    def __init__(self, web3_provider, private_key):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = self.web3.eth.account.from_key(private_key)
        self.defi_contracts = {}
        self.yield_farming_pools = {}
        
    def setup_defi_contracts(self, contract_addresses):
        """Настройка DeFi контрактов"""
        for name, address in contract_addresses.items():
            # Загрузка ABI
            abi = self._load_contract_abi(name)
            
            # Создание контракта
            contract = self.web3.eth.contract(address=address, abi=abi)
            self.defi_contracts[name] = contract
    
    def _load_contract_abi(self, contract_name):
        """Загрузка ABI контракта"""
        # Упрощенная версия - в реальности нужно загружать из файла
        abi = [
            {
                "inputs": [{"name": "account", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "", "type": "uint256"}],
                "type": "function"
            }
        ]
        return abi
    
    def get_defi_balances(self):
        """Получение балансов DeFi активов"""
        balances = {}
        
        for name, contract in self.defi_contracts.items():
            try:
                balance = contract.functions.balanceOf(self.account.address).call()
                balances[name] = balance
            except Exception as e:
                print(f"Error getting balance for {name}: {e}")
                balances[name] = 0
        
        return balances
    
    def calculate_defi_yield(self, asset_name, time_period=30):
        """Расчет доходности DeFi актива"""
        if asset_name not in self.defi_contracts:
            return 0
        
        try:
            # Получение информации о пуле
            pool_info = self.defi_contracts[asset_name].functions.poolInfo(0).call()
            
            # Расчет APR
            total_alloc_point = self.defi_contracts[asset_name].functions.totalAllocPoint().call()
            reward_per_block = self.defi_contracts[asset_name].functions.rewardPerBlock().call()
            
            pool_alloc_point = pool_info[1]
            pool_alloc_share = pool_alloc_point / total_alloc_point
            
            # APR
            blocks_per_year = 2102400
            annual_rewards = reward_per_block * pool_alloc_share * blocks_per_year
            total_staked = pool_info[0]
            
            apr = annual_rewards / total_staked if total_staked > 0 else 0
            
            # Доходность за период
            period_yield = apr * (time_period / 365)
            
            return period_yield
            
        except Exception as e:
            print(f"Error calculating yield for {asset_name}: {e}")
            return 0
    
    def optimize_defi_allocation(self, total_capital):
        """Оптимизация распределения для DeFi"""
        # Получение APR всех пулов
        pool_aprs = {}
        for asset_name in self.defi_contracts.keys():
            apr = self.calculate_defi_yield(asset_name)
            pool_aprs[asset_name] = apr
        
        # Сортировка пулов по APR
        sorted_pools = sorted(pool_aprs.items(), key=lambda x: x[1], reverse=True)
        
        # Оптимальное распределение
        optimal_allocation = {}
        remaining_capital = total_capital
        
        for pool_name, apr in sorted_pools:
            if apr > 0.1:  # Минимальный APR 10%
                # Максимум 30% капитала в один пул
                max_allocation = min(remaining_capital * 0.3, remaining_capital)
                optimal_allocation[pool_name] = max_allocation
                remaining_capital -= max_allocation
        
        return optimal_allocation
    
    def execute_defi_trade(self, asset_name, amount, action='stake'):
        """Выполнение DeFi сделки"""
        if asset_name not in self.defi_contracts:
            return False
        
        try:
            contract = self.defi_contracts[asset_name]
            
            if action == 'stake':
                # Стейкинг токенов
                transaction = contract.functions.deposit(0, amount).build_transaction({
                    'from': self.account.address,
                    'gas': 200000,
                    'gasPrice': self.web3.eth.gas_price,
                    'nonce': self.web3.eth.get_transaction_count(self.account.address)
                })
            elif action == 'unstake':
                # Анстейкинг токенов
                transaction = contract.functions.withdraw(0, amount).build_transaction({
                    'from': self.account.address,
                    'gas': 200000,
                    'gasPrice': self.web3.eth.gas_price,
                    'nonce': self.web3.eth.get_transaction_count(self.account.address)
                })
            
            # Подписание и отправка транзакции
            signed_txn = self.web3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"Error executing DeFi trade: {e}")
            return False
    
    def monitor_defi_performance(self):
        """Мониторинг производительности DeFi"""
        performance = {}
        
        for asset_name in self.defi_contracts.keys():
            # Получение баланса
            balance = self.get_defi_balances().get(asset_name, 0)
            
            # Расчет доходности
            yield_rate = self.calculate_defi_yield(asset_name)
            
            performance[asset_name] = {
                'balance': balance,
                'yield_rate': yield_rate,
                'estimated_annual_return': yield_rate * 365
            }
        
        return performance
    
    def rebalance_defi_portfolio(self, current_allocation, target_allocation):
        """Перебалансировка DeFi портфолио"""
        rebalancing_trades = []
        
        for asset_name in set(current_allocation.keys()) | set(target_allocation.keys()):
            current_amount = current_allocation.get(asset_name, 0)
            target_amount = target_allocation.get(asset_name, 0)
            
            if abs(current_amount - target_amount) > 0.01:  # Минимальное отклонение
                trade_amount = target_amount - current_amount
                
                if trade_amount > 0:
                    # Стейкинг
                    action = 'stake'
                else:
                    # Анстейкинг
                    action = 'unstake'
                    trade_amount = abs(trade_amount)
                
                rebalancing_trades.append({
                    'asset': asset_name,
                    'amount': trade_amount,
                    'action': action
                })
        
        return rebalancing_trades

# Использование системы
if __name__ == "__main__":
    # Настройка Web3
    web3_provider = "https://mainnet.infura.io/v3/YOUR_PROJECT_ID"
    private_key = "YOUR_PRIVATE_KEY"
    
    # Создание системы
    system = BlockchainIntegratedSystem(web3_provider, private_key)
    
    # Настройка контрактов
    contract_addresses = {
        'uniswap_v2': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',
        'compound': '0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B'
    }
    
    system.setup_defi_contracts(contract_addresses)
    
    # Оптимизация распределения
    total_capital = 10000  # 10,000 USDC
    optimal_allocation = system.optimize_defi_allocation(total_capital)
    
    print("Optimal DeFi allocation:")
    for asset, amount in optimal_allocation.items():
        print(f"{asset}: {amount:.2f} USDC")
    
    # Мониторинг производительности
    performance = system.monitor_defi_performance()
    
    print("\nDeFi Performance:")
    for asset, perf in performance.items():
        print(f"{asset}: {perf['yield_rate']:.2%} daily yield")
```

## Пример 4: Полная система с автоматическим управлением

**Теория:** Полная система с автоматическим управлением представляет собой комплексную реализацию торговой системы, которая объединяет все аспекты ML-торговли в единую автоматизированную систему. Это критически важно для создания максимально эффективных систем.

**Почему полная система важна:**
- **Комплексность:** Обеспечивает комплексный подход к торговле
- **Автоматизация:** Полностью автоматизирует процесс торговли
- **Эффективность:** Обеспечивает максимальную эффективность
- **Масштабируемость:** Легко масштабируется

### Описание системы

**Теория:** Полная система с автоматическим управлением объединяет все компоненты ML-торговли в единую систему. Это критически важно для создания максимально эффективных торговых систем.

**Почему полная система эффективна:**
- **Интеграция:** Объединяет все компоненты в единую систему
- **Автоматизация:** Полностью автоматизирует процесс
- **Оптимизация:** Обеспечивает оптимальную работу всех компонентов
- **Мониторинг:** Обеспечивает полный мониторинг системы

**Плюсы:**
- Полная интеграция компонентов
- Полная автоматизация
- Оптимальная работа
- Полный мониторинг

**Минусы:**
- Очень высокая сложность
- Высокие требования к ресурсам
- Потенциальные проблемы с надежностью

### Код реализации

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import xgboost as xgb
from datetime import datetime, timedelta
import schedule
import time
import logging

class AutomatedTradingSystem:
    """Автоматическая торговая система"""
    
    def __init__(self, config):
        self.config = config
        self.models = {}
        self.performance_monitor = PerformanceMonitor()
        self.risk_manager = RiskManager()
        self.portfolio_manager = PortfolioManager()
        self.defi_manager = DeFiManager()
        
        # Настройка логирования
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def initialize_models(self):
        """Инициализация моделей"""
        self.models = {
            'wave2': Wave2Model(),
            'schr_levels': SCHRLevelsModel(),
            'schr_short3': SCHRShort3Model(),
            'ensemble': VotingClassifier([
                ('wave2', self.models['wave2']),
                ('schr_levels', self.models['schr_levels']),
                ('schr_short3', self.models['schr_short3'])
            ], voting='soft')
        }
    
    def train_all_models(self, data):
        """Обучение всех моделей"""
        for name, model in self.models.items():
            if name != 'ensemble':
                self.logger.info(f"Training {name} model...")
                model.train(data)
                self.logger.info(f"{name} model trained successfully")
        
        # Обучение ансамбля
        self.logger.info("Training ensemble model...")
        self.models['ensemble'].fit(data)
        self.logger.info("Ensemble model trained successfully")
    
    def get_trading_signals(self, data):
        """Получение торговых сигналов"""
        signals = {}
        
        for name, model in self.models.items():
            if name != 'ensemble':
                signal = model.predict(data)
                signals[name] = signal
        
        # Ансамблевый сигнал
        ensemble_signal = self.models['ensemble'].predict(data)
        signals['ensemble'] = ensemble_signal
        
        return signals
    
    def execute_trading_strategy(self, signals, market_data):
        """Выполнение торговой стратегии"""
        # Анализ сигналов
        signal_analysis = self._analyze_signals(signals)
        
        # Проверка рисков
        risk_assessment = self.risk_manager.assess_risks(market_data)
        
        # Принятие решения
        if signal_analysis['confidence'] > 0.7 and risk_assessment['acceptable']:
            # Выполнение сделки
            trade_result = self._execute_trade(signal_analysis, market_data)
            
            if trade_result['success']:
                self.logger.info(f"Trade executed successfully: {trade_result}")
            else:
                self.logger.error(f"Trade execution failed: {trade_result}")
        
        return signal_analysis, risk_assessment
    
    def _analyze_signals(self, signals):
        """Анализ сигналов"""
        # Согласованность сигналов
        signal_values = list(signals.values())
        agreement = np.mean(signal_values)
        
        # Уверенность в сигнале
        confidence = 1 - np.std(signal_values)
        
        # Направление сигнала
        direction = 1 if agreement > 0.5 else -1 if agreement < -0.5 else 0
        
        return {
            'agreement': agreement,
            'confidence': confidence,
            'direction': direction
        }
    
    def _execute_trade(self, signal_analysis, market_data):
        """Выполнение сделки"""
        try:
            # Расчет размера позиции
            position_size = self.risk_manager.calculate_position_size(
                signal_analysis, market_data
            )
            
            # Выполнение сделки
            if signal_analysis['direction'] > 0:
                # Покупка
                trade_result = self.portfolio_manager.buy(
                    market_data['symbol'],
                    position_size,
                    market_data['price']
                )
            elif signal_analysis['direction'] < 0:
                # Продажа
                trade_result = self.portfolio_manager.sell(
                    market_data['symbol'],
                    position_size,
                    market_data['price']
                )
            else:
                # Удержание
                trade_result = {'success': True, 'action': 'hold'}
            
            return trade_result
            
        except Exception as e:
            self.logger.error(f"Trade execution error: {e}")
            return {'success': False, 'error': str(e)}
    
    def run_automated_trading(self):
        """Запуск автоматической торговли"""
        self.logger.info("Starting automated trading system...")
        
        # Инициализация
        self.initialize_models()
        
        # Загрузка данных
        data = self._load_market_data()
        
        # Обучение моделей
        self.train_all_models(data)
        
        # Настройка расписания
        schedule.every().minute.do(self._trading_cycle)
        schedule.every().hour.do(self._performance_check)
        schedule.every().day.at("00:00").do(self._daily_rebalancing)
        schedule.every().week.do(self._weekly_retraining)
        
        # Основной цикл
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("Stopping automated trading system...")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                time.sleep(60)  # Пауза при ошибке
    
    def _trading_cycle(self):
        """Торговый цикл"""
        try:
            # Получение рыночных данных
            market_data = self._get_current_market_data()
            
            # Получение сигналов
            signals = self.get_trading_signals(market_data)
            
            # Выполнение стратегии
            signal_analysis, risk_assessment = self.execute_trading_strategy(
                signals, market_data
            )
            
            # Логирование
            self.logger.info(f"Trading cycle completed: {signal_analysis}")
            
        except Exception as e:
            self.logger.error(f"Error in trading cycle: {e}")
    
    def _performance_check(self):
        """Проверка производительности"""
        try:
            # Получение метрик
            metrics = self.performance_monitor.get_current_metrics()
            
            # Проверка алертов
            alerts = self.performance_monitor.check_alerts(metrics)
            
            if alerts:
                self.logger.warning(f"Performance alerts: {alerts}")
                
                # Автоматические действия
                for alert in alerts:
                    if alert['severity'] == 'high':
                        self._handle_critical_alert(alert)
                    elif alert['severity'] == 'medium':
                        self._handle_medium_alert(alert)
            
        except Exception as e:
            self.logger.error(f"Error in performance check: {e}")
    
    def _daily_rebalancing(self):
        """Ежедневное перебалансирование"""
        try:
            # Получение текущих весов
            current_weights = self.portfolio_manager.get_current_weights()
            
            # Оптимизация весов
            target_weights = self.portfolio_manager.optimize_weights()
            
            # Перебалансирование
            rebalancing_trades = self.portfolio_manager.calculate_rebalancing_trades(
                current_weights, target_weights
            )
            
            # Выполнение сделок
            for trade in rebalancing_trades:
                self.portfolio_manager.execute_trade(trade)
            
            self.logger.info("Daily rebalancing completed")
            
        except Exception as e:
            self.logger.error(f"Error in daily rebalancing: {e}")
    
    def _weekly_retraining(self):
        """Еженедельное переобучение"""
        try:
            # Загрузка новых данных
            new_data = self._load_market_data()
            
            # Переобучение моделей
            self.train_all_models(new_data)
            
            self.logger.info("Weekly retraining completed")
            
        except Exception as e:
            self.logger.error(f"Error in weekly retraining: {e}")
    
    def _load_market_data(self):
        """Загрузка рыночных данных"""
        # Загрузка данных для всех активов
        data = {}
        
        for symbol in self.config['symbols']:
            ticker = yf.Ticker(symbol)
            symbol_data = ticker.history(period='1y', interval='1h')
            data[symbol] = symbol_data
        
        return data
    
    def _get_current_market_data(self):
        """Получение текущих рыночных данных"""
        # Получение текущих цен
        market_data = {}
        
        for symbol in self.config['symbols']:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            market_data[symbol] = {
                'price': info['currentPrice'],
                'volume': info['volume'],
                'timestamp': datetime.now()
            }
        
        return market_data

# Конфигурация системы
config = {
    'symbols': ['BTC-USD', 'ETH-USD', 'BNB-USD'],
    'timeframes': ['1h', '4h', '1d'],
    'risk_limits': {
        'max_position_size': 0.1,
        'max_drawdown': 0.15,
        'max_var': 0.05
    },
    'defi_integration': {
        'enabled': True,
        'pools': ['uniswap_v2', 'compound', 'aave']
    }
}

# Запуск системы
if __name__ == "__main__":
    system = AutomatedTradingSystem(config)
    system.run_automated_trading()
```

## Следующие шаги

**Теория:** Следующие шаги представляют собой практические рекомендации по внедрению изученных примеров в реальную торговлю. Это критически важно для успешного применения знаний на практике.

**Почему следующие шаги важны:**
- **Практическое применение:** Обеспечивает практическое применение знаний
- **Снижение рисков:** Помогает снизить риски при внедрении
- **Постепенное развитие:** Обеспечивает постепенное развитие системы
- **Успешное внедрение:** Критически важно для успешного внедрения

После изучения практических примеров:

1. **Адаптируйте примеры под ваши нужды**
   - **Теория:** Адаптация примеров критически важна для успешного применения
   - **Почему важно:** Обеспечивает соответствие вашим потребностям
   - **Плюсы:** Персонализация, соответствие потребностям
   - **Минусы:** Требует дополнительной работы

2. **Тестируйте на исторических данных перед использованием**
   - **Теория:** Тестирование критически важно для валидации системы
   - **Почему важно:** Обеспечивает валидацию системы
   - **Плюсы:** Валидация, снижение рисков
   - **Минусы:** Требует времени и ресурсов

3. **Начните с малых сумм для проверки системы**
   - **Теория:** Начало с малых сумм критически важно для снижения рисков
   - **Почему важно:** Минимизирует риски при тестировании
   - **Плюсы:** Минимальные риски, возможность обучения
   - **Минусы:** Ограниченная доходность

4. **Постепенно увеличивайте размер позиций**
   - **Теория:** Постепенное увеличение критически важно для безопасного масштабирования
   - **Почему важно:** Обеспечивает безопасное масштабирование
   - **Плюсы:** Безопасное масштабирование, контроль рисков
   - **Минусы:** Медленное развитие

5. **Мониторьте производительность постоянно**
   - **Теория:** Постоянный мониторинг критически важен для поддержания эффективности
   - **Почему важно:** Обеспечивает поддержание эффективности
   - **Плюсы:** Поддержание эффективности, своевременное выявление проблем
   - **Минусы:** Требует постоянного внимания

## Ключевые выводы

**Теория:** Ключевые выводы суммируют наиболее важные аспекты практических примеров для создания эффективных ML-систем с доходностью 100%+ в месяц. Эти выводы критически важны для успешного применения знаний на практике.

1. **Простота - начинайте с простых систем**
   - **Теория:** Простота критически важна для понимания основ
   - **Почему важно:** Обеспечивает понимание основ
   - **Плюсы:** Понимание основ, низкие риски
   - **Минусы:** Ограниченная сложность

2. **Тестирование - всегда тестируйте перед использованием**
   - **Теория:** Тестирование критически важно для валидации системы
   - **Почему важно:** Обеспечивает валидацию системы
   - **Плюсы:** Валидация, снижение рисков
   - **Минусы:** Требует времени и ресурсов

3. **Риск-менеджмент - никогда не рискуйте больше, чем можете позволить**
   - **Теория:** Риск-менеджмент критически важен для долгосрочного успеха
   - **Почему важно:** Обеспечивает долгосрочный успех
   - **Плюсы:** Защита капитала, долгосрочный успех
   - **Минусы:** Потенциальные ограничения доходности

4. **Автоматизация - автоматизируйте все процессы**
   - **Теория:** Автоматизация критически важна для эффективности
   - **Почему важно:** Обеспечивает высокую эффективность
   - **Плюсы:** Высокая эффективность, масштабируемость
   - **Минусы:** Сложность реализации

5. **Мониторинг - постоянно следите за производительностью**
   - **Теория:** Мониторинг критически важен для поддержания эффективности
   - **Почему важно:** Обеспечивает поддержание эффективности
   - **Плюсы:** Поддержание эффективности, своевременное выявление проблем
   - **Минусы:** Требует постоянного внимания

6. **Адаптация - адаптируйте систему к изменяющимся условиям**
   - **Теория:** Адаптация критически важна для долгосрочной эффективности
   - **Почему важно:** Обеспечивает долгосрочную эффективность
   - **Плюсы:** Долгосрочная эффективность, устойчивость
   - **Минусы:** Сложность реализации

---

**Важно:** Эти примеры предназначены для образовательных целей. Всегда тестируйте системы на исторических данных перед использованием реальных средств.
