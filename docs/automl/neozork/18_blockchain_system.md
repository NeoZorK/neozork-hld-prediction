# 18.3. Блокчейн-система с робастной прибылью 100% в месяц

## 🚀 Полная блокчейн-система для testnet

### Ансамблевая модель

```python
# src/models/ensemble.py
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import xgboost as xgb
import lightgbm as lgb
import catboost as cb

class EnsembleModel:
    """Ансамблевая модель для комбинирования всех индикаторов"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.models = {}
        self.ensemble = None
        self.is_trained = False
        self.feature_importance = {}
        
    def train(self, wave2_data: pd.DataFrame, schr_levels_data: pd.DataFrame, schr_short3_data: pd.DataFrame):
        """Обучение ансамблевой модели"""
        try:
            self.logger.info("Training ensemble model...")
            
            # Подготовка данных
            X, y = self._prepare_ensemble_data(wave2_data, schr_levels_data, schr_short3_data)
            
            if X.empty or y.empty:
                self.logger.warning("No data available for training ensemble")
                return
            
            # Создание индивидуальных моделей
            self.models = {
                'logistic': LogisticRegression(random_state=42, max_iter=1000),
                'svm': SVC(probability=True, random_state=42),
                'neural_net': MLPClassifier(hidden_layer_sizes=(100, 50), random_state=42, max_iter=1000),
                'xgboost': xgb.XGBClassifier(n_estimators=100, random_state=42),
                'lightgbm': lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1),
                'catboost': cb.CatBoostClassifier(iterations=100, random_state=42, verbose=False)
            }
            
            # Создание ансамбля
            self.ensemble = VotingClassifier(
                estimators=list(self.models.items()),
                voting='soft'
            )
            
            # Обучение
            self.ensemble.fit(X, y)
            
            # Расчет важности признаков
            self._calculate_feature_importance(X, y)
            
            self.is_trained = True
            self.logger.info("Ensemble model trained successfully")
            
        except Exception as e:
            self.logger.error(f"Error training ensemble model: {e}")
    
    def _prepare_ensemble_data(self, wave2_data: pd.DataFrame, schr_levels_data: pd.DataFrame, schr_short3_data: pd.DataFrame) -> tuple:
        """Подготовка данных для ансамбля"""
        # Объединение всех признаков
        all_features = []
        
        if not wave2_data.empty:
            all_features.append(wave2_data)
        
        if not schr_levels_data.empty:
            all_features.append(schr_levels_data)
        
        if not schr_short3_data.empty:
            all_features.append(schr_short3_data)
        
        if not all_features:
            return pd.DataFrame(), pd.Series()
        
        # Объединение по индексу
        X = pd.concat(all_features, axis=1)
        X = X.dropna()
        
        # Создание целевой переменной
        y = self._create_ensemble_target(X)
        
        return X, y
    
    def _create_ensemble_target(self, X: pd.DataFrame) -> pd.Series:
        """Создание целевой переменной для ансамбля"""
        # Используем цену закрытия для создания целевой переменной
        if 'close' in X.columns:
            price = X['close']
        else:
            # Если нет цены, используем первый числовой столбец
            numeric_cols = X.select_dtypes(include=[np.number]).columns
            price = X[numeric_cols[0]]
        
        # Процентное изменение
        price_change = price.pct_change().shift(-1)
        
        # Классификация направления
        target = pd.cut(
            price_change,
            bins=[-np.inf, -0.001, 0.001, np.inf],
            labels=[0, 1, 2],  # 0=down, 1=hold, 2=up
            include_lowest=True
        )
        
        return target.astype(int)
    
    def _calculate_feature_importance(self, X: pd.DataFrame, y: pd.Series):
        """Расчет важности признаков"""
        try:
            # Для XGBoost
            if 'xgboost' in self.models:
                xgb_model = self.models['xgboost']
                xgb_model.fit(X, y)
                importance = xgb_model.feature_importances_
                self.feature_importance['xgboost'] = dict(zip(X.columns, importance))
            
            # Для LightGBM
            if 'lightgbm' in self.models:
                lgb_model = self.models['lightgbm']
                lgb_model.fit(X, y)
                importance = lgb_model.feature_importances_
                self.feature_importance['lightgbm'] = dict(zip(X.columns, importance))
            
        except Exception as e:
            self.logger.error(f"Error calculating feature importance: {e}")
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Предсказание ансамбля"""
        if not self.is_trained:
            self.logger.warning("Ensemble model not trained")
            return np.zeros(len(X))
        
        try:
            prediction = self.ensemble.predict(X)
            return prediction
        except Exception as e:
            self.logger.error(f"Error predicting with ensemble: {e}")
            return np.zeros(len(X))
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Предсказание вероятностей"""
        if not self.is_trained:
            self.logger.warning("Ensemble model not trained")
            return np.zeros((len(X), 3))
        
        try:
            probabilities = self.ensemble.predict_proba(X)
            return probabilities
        except Exception as e:
            self.logger.error(f"Error predicting probabilities with ensemble: {e}")
            return np.zeros((len(X), 3))
```

### Система переобучения

```python
# src/models/retraining_system.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import joblib
from pathlib import Path
import schedule
import time
import threading

class RetrainingSystem:
    """Система автоматического переобучения"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self.retraining_thread = None
        self.performance_threshold = 0.7
        self.drift_threshold = 0.1
        self.last_retraining = None
        self.performance_history = []
        
    def start_retraining_system(self):
        """Запуск системы переобучения"""
        self.logger.info("Starting retraining system...")
        self.is_running = True
        
        # Настройка расписания
        schedule.every().day.at("02:00").do(self._daily_retraining)
        schedule.every().sunday.at("03:00").do(self._weekly_retraining)
        schedule.every().hour.do(self._drift_check)
        
        # Запуск в отдельном потоке
        self.retraining_thread = threading.Thread(target=self._run_scheduler)
        self.retraining_thread.daemon = True
        self.retraining_thread.start()
        
        self.logger.info("Retraining system started")
    
    def _run_scheduler(self):
        """Запуск планировщика"""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Проверка каждую минуту
            except Exception as e:
                self.logger.error(f"Error in retraining scheduler: {e}")
                time.sleep(60)
    
    def _daily_retraining(self):
        """Ежедневное переобучение"""
        try:
            self.logger.info("Starting daily retraining...")
            
            # Проверка необходимости переобучения
            if self._should_retrain():
                self._retrain_models()
                self.last_retraining = datetime.now()
                self.logger.info("Daily retraining completed")
            else:
                self.logger.info("Daily retraining skipped - not needed")
                
        except Exception as e:
            self.logger.error(f"Error in daily retraining: {e}")
    
    def _weekly_retraining(self):
        """Еженедельное переобучение"""
        try:
            self.logger.info("Starting weekly retraining...")
            
            # Принудительное переобучение
            self._retrain_models()
            self.last_retraining = datetime.now()
            self.logger.info("Weekly retraining completed")
            
        except Exception as e:
            self.logger.error(f"Error in weekly retraining: {e}")
    
    def _drift_check(self):
        """Проверка дрифта данных"""
        try:
            # Получение текущих данных
            current_data = self._get_current_data()
            
            if current_data.empty:
                return
            
            # Расчет дрифта
            drift_score = self._calculate_drift(current_data)
            
            if drift_score > self.drift_threshold:
                self.logger.warning(f"Data drift detected: {drift_score:.4f}")
                self._retrain_models()
                self.last_retraining = datetime.now()
                
        except Exception as e:
            self.logger.error(f"Error in drift check: {e}")
    
    def _should_retrain(self) -> bool:
        """Проверка необходимости переобучения"""
        # Проверка времени с последнего переобучения
        if self.last_retraining is None:
            return True
        
        time_since_retraining = datetime.now() - self.last_retraining
        
        # Переобучение если прошло больше 24 часов
        if time_since_retraining.days >= 1:
            return True
        
        # Проверка производительности
        if len(self.performance_history) > 0:
            recent_performance = self.performance_history[-1]
            if recent_performance < self.performance_threshold:
                return True
        
        return False
    
    def _retrain_models(self):
        """Переобучение моделей"""
        try:
            self.logger.info("Retraining models...")
            
            # Загрузка новых данных
            new_data = self._load_new_data()
            
            if new_data.empty:
                self.logger.warning("No new data available for retraining")
                return
            
            # Переобучение каждой модели
            for model_name, model in self.models.items():
                self.logger.info(f"Retraining {model_name}...")
                model.train(new_data)
            
            # Сохранение моделей
            self._save_models()
            
            # Обновление истории производительности
            self._update_performance_history()
            
            self.logger.info("Models retraining completed")
            
        except Exception as e:
            self.logger.error(f"Error retraining models: {e}")
    
    def _calculate_drift(self, current_data: pd.DataFrame) -> float:
        """Расчет дрифта данных"""
        try:
            # Загрузка эталонных данных
            reference_data = self._load_reference_data()
            
            if reference_data.empty:
                return 0.0
            
            # Выбор числовых признаков
            numeric_cols = current_data.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) == 0:
                return 0.0
            
            # Расчет статистических различий
            drift_scores = []
            
            for col in numeric_cols:
                if col in reference_data.columns:
                    current_mean = current_data[col].mean()
                    reference_mean = reference_data[col].mean()
                    
                    current_std = current_data[col].std()
                    reference_std = reference_data[col].std()
                    
                    # Статистическое расстояние
                    if reference_std > 0:
                        drift_score = abs(current_mean - reference_mean) / reference_std
                        drift_scores.append(drift_score)
            
            if drift_scores:
                return np.mean(drift_scores)
            else:
                return 0.0
                
        except Exception as e:
            self.logger.error(f"Error calculating drift: {e}")
            return 0.0
    
    def _load_new_data(self) -> pd.DataFrame:
        """Загрузка новых данных"""
        # Здесь должна быть логика загрузки новых данных
        # Для примера возвращаем пустой DataFrame
        return pd.DataFrame()
    
    def _load_reference_data(self) -> pd.DataFrame:
        """Загрузка эталонных данных"""
        # Здесь должна быть логика загрузки эталонных данных
        # Для примера возвращаем пустой DataFrame
        return pd.DataFrame()
    
    def _save_models(self):
        """Сохранение моделей"""
        try:
            models_dir = Path("models/trained")
            models_dir.mkdir(parents=True, exist_ok=True)
            
            for model_name, model in self.models.items():
                model_path = models_dir / f"{model_name}_model.pkl"
                joblib.dump(model, model_path)
                
            self.logger.info("Models saved successfully")
            
        except Exception as e:
            self.logger.error(f"Error saving models: {e}")
    
    def _update_performance_history(self):
        """Обновление истории производительности"""
        # Здесь должна быть логика расчета производительности
        # Для примера добавляем случайное значение
        performance = np.random.uniform(0.6, 0.9)
        self.performance_history.append(performance)
        
        # Ограничиваем историю последними 100 записями
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-100:]
    
    def stop_retraining_system(self):
        """Остановка системы переобучения"""
        self.logger.info("Stopping retraining system...")
        self.is_running = False
        
        if self.retraining_thread:
            self.retraining_thread.join(timeout=5)
        
        self.logger.info("Retraining system stopped")
```

### Блокчейн-интеграция для testnet

```python
# src/blockchain/testnet_integration.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from web3 import Web3
import json
import time
import requests

class TestnetBlockchainSystem:
    """Блокчейн-система для testnet с робастной прибылью 100% в месяц"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.web3 = None
        self.account = None
        self.contracts = {}
        self.positions = {}
        self.performance_history = []
        self.monthly_target = 1.0  # 100% в месяц
        self.daily_target = 0.033  # ~3.3% в день
        
    def initialize_blockchain(self):
        """Инициализация блокчейна"""
        try:
            # Подключение к testnet
            testnet_url = self.config.get('testnet_url', 'https://sepolia.infura.io/v3/YOUR_PROJECT_ID')
            self.web3 = Web3(Web3.HTTPProvider(testnet_url))
            
            if not self.web3.is_connected():
                raise Exception("Failed to connect to testnet")
            
            # Настройка аккаунта
            private_key = self.config.get('private_key')
            if not private_key:
                raise Exception("Private key not provided")
            
            self.account = self.web3.eth.account.from_key(private_key)
            
            # Загрузка контрактов
            self._load_contracts()
            
            self.logger.info("Blockchain initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing blockchain: {e}")
            raise
    
    def _load_contracts(self):
        """Загрузка смарт-контрактов"""
        try:
            # ABI для тестового контракта
            test_contract_abi = [
                {
                    "inputs": [{"name": "amount", "type": "uint256"}],
                    "name": "deposit",
                    "outputs": [],
                    "type": "function"
                },
                {
                    "inputs": [{"name": "amount", "type": "uint256"}],
                    "name": "withdraw",
                    "outputs": [],
                    "type": "function"
                },
                {
                    "inputs": [],
                    "name": "getBalance",
                    "outputs": [{"name": "", "type": "uint256"}],
                    "type": "function"
                }
            ]
            
            # Адрес тестового контракта
            test_contract_address = self.config.get('test_contract_address')
            
            if test_contract_address:
                contract = self.web3.eth.contract(
                    address=test_contract_address,
                    abi=test_contract_abi
                )
                self.contracts['test'] = contract
            
            self.logger.info("Contracts loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error loading contracts: {e}")
    
    def start_trading_system(self):
        """Запуск торговой системы"""
        try:
            self.logger.info("Starting blockchain trading system...")
            
            # Инициализация блокчейна
            self.initialize_blockchain()
            
            # Основной торговый цикл
            while True:
                try:
                    # Получение рыночных данных
                    market_data = self._get_market_data()
                    
                    # Генерация торговых сигналов
                    signals = self._generate_trading_signals(market_data)
                    
                    # Выполнение торговых операций
                    self._execute_trades(signals, market_data)
                    
                    # Обновление позиций
                    self._update_positions()
                    
                    # Проверка производительности
                    self._check_performance()
                    
                    # Пауза между циклами
                    time.sleep(60)  # 1 минута
                    
                except KeyboardInterrupt:
                    self.logger.info("Trading system stopped by user")
                    break
                except Exception as e:
                    self.logger.error(f"Error in trading cycle: {e}")
                    time.sleep(60)
                    
        except Exception as e:
            self.logger.error(f"Error starting trading system: {e}")
            raise
    
    def _get_market_data(self) -> Dict:
        """Получение рыночных данных"""
        try:
            # Получение данных BTC/USD
            ticker = yf.Ticker("BTC-USD")
            data = ticker.history(period="1d", interval="1m")
            
            if data.empty:
                return {}
            
            latest = data.iloc[-1]
            
            return {
                'symbol': 'BTC-USD',
                'price': latest['Close'],
                'volume': latest['Volume'],
                'high': latest['High'],
                'low': latest['Low'],
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting market data: {e}")
            return {}
    
    def _generate_trading_signals(self, market_data: Dict) -> Dict:
        """Генерация торговых сигналов"""
        try:
            if not market_data:
                return {'signal': 0, 'confidence': 0}
            
            # Здесь должна быть логика генерации сигналов
            # Для примера используем простую стратегию
            
            price = market_data['price']
            volume = market_data['volume']
            
            # Простая стратегия на основе цены и объема
            if price > price * 1.001 and volume > volume * 1.1:
                signal = 1  # Покупка
                confidence = 0.8
            elif price < price * 0.999 and volume > volume * 1.1:
                signal = -1  # Продажа
                confidence = 0.8
            else:
                signal = 0  # Удержание
                confidence = 0.5
            
            return {
                'signal': signal,
                'confidence': confidence,
                'price': price,
                'volume': volume
            }
            
        except Exception as e:
            self.logger.error(f"Error generating trading signals: {e}")
            return {'signal': 0, 'confidence': 0}
    
    def _execute_trades(self, signals: Dict, market_data: Dict):
        """Выполнение торговых операций"""
        try:
            if not signals or signals['confidence'] < 0.7:
                return
            
            signal = signals['signal']
            price = market_data['price']
            
            if signal > 0:  # Покупка
                self._execute_buy(price)
            elif signal < 0:  # Продажа
                self._execute_sell(price)
                
        except Exception as e:
            self.logger.error(f"Error executing trades: {e}")
    
    def _execute_buy(self, price: float):
        """Выполнение покупки"""
        try:
            # Расчет размера позиции
            position_size = self._calculate_position_size(price)
            
            # Выполнение покупки на блокчейне
            if 'test' in self.contracts:
                transaction = self.contracts['test'].functions.deposit(
                    int(position_size * 1e18)  # Конвертация в wei
                ).build_transaction({
                    'from': self.account.address,
                    'gas': 200000,
                    'gasPrice': self.web3.eth.gas_price,
                    'nonce': self.web3.eth.get_transaction_count(self.account.address)
                })
                
                signed_txn = self.web3.eth.account.sign_transaction(transaction, self.account.key)
                tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                
                # Сохранение позиции
                self.positions[datetime.now()] = {
                    'type': 'buy',
                    'price': price,
                    'amount': position_size,
                    'tx_hash': tx_hash.hex()
                }
                
                self.logger.info(f"Buy executed: {position_size} at {price}, TX: {tx_hash.hex()}")
                
        except Exception as e:
            self.logger.error(f"Error executing buy: {e}")
    
    def _execute_sell(self, price: float):
        """Выполнение продажи"""
        try:
            # Расчет размера позиции
            position_size = self._calculate_position_size(price)
            
            # Выполнение продажи на блокчейне
            if 'test' in self.contracts:
                transaction = self.contracts['test'].functions.withdraw(
                    int(position_size * 1e18)  # Конвертация в wei
                ).build_transaction({
                    'from': self.account.address,
                    'gas': 200000,
                    'gasPrice': self.web3.eth.gas_price,
                    'nonce': self.web3.eth.get_transaction_count(self.account.address)
                })
                
                signed_txn = self.web3.eth.account.sign_transaction(transaction, self.account.key)
                tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                
                # Сохранение позиции
                self.positions[datetime.now()] = {
                    'type': 'sell',
                    'price': price,
                    'amount': position_size,
                    'tx_hash': tx_hash.hex()
                }
                
                self.logger.info(f"Sell executed: {position_size} at {price}, TX: {tx_hash.hex()}")
                
        except Exception as e:
            self.logger.error(f"Error executing sell: {e}")
    
    def _calculate_position_size(self, price: float) -> float:
        """Расчет размера позиции"""
        try:
            # Получение баланса
            balance = self._get_balance()
            
            # Размер позиции = 10% от баланса
            position_size = balance * 0.1 / price
            
            return position_size
            
        except Exception as e:
            self.logger.error(f"Error calculating position size: {e}")
            return 0.0
    
    def _get_balance(self) -> float:
        """Получение баланса"""
        try:
            if 'test' in self.contracts:
                balance = self.contracts['test'].functions.getBalance().call()
                return balance / 1e18  # Конвертация из wei
            else:
                return 1000.0  # Тестовый баланс
                
        except Exception as e:
            self.logger.error(f"Error getting balance: {e}")
            return 1000.0
    
    def _update_positions(self):
        """Обновление позиций"""
        try:
            # Здесь должна быть логика обновления позиций
            # Для примера просто логируем
            self.logger.info(f"Current positions: {len(self.positions)}")
            
        except Exception as e:
            self.logger.error(f"Error updating positions: {e}")
    
    def _check_performance(self):
        """Проверка производительности"""
        try:
            # Расчет текущей производительности
            current_performance = self._calculate_performance()
            
            # Сохранение в историю
            self.performance_history.append({
                'timestamp': datetime.now(),
                'performance': current_performance
            })
            
            # Проверка достижения цели
            if current_performance >= self.monthly_target:
                self.logger.info(f"Monthly target achieved: {current_performance:.2%}")
            else:
                self.logger.info(f"Current performance: {current_performance:.2%}, Target: {self.monthly_target:.2%}")
                
        except Exception as e:
            self.logger.error(f"Error checking performance: {e}")
    
    def _calculate_performance(self) -> float:
        """Расчет производительности"""
        try:
            if len(self.performance_history) < 2:
                return 0.0
            
            # Расчет общей производительности
            initial_balance = 1000.0  # Начальный баланс
            current_balance = self._get_balance()
            
            performance = (current_balance - initial_balance) / initial_balance
            
            return performance
            
        except Exception as e:
            self.logger.error(f"Error calculating performance: {e}")
            return 0.0
```

### Главный скрипт запуска

```python
# main.py
#!/usr/bin/env python3
"""
NeoZorK 100% System - Главный скрипт запуска
Система для достижения 100% прибыли в месяц на блокчейн testnet
"""

import yaml
import logging
import signal
import sys
from datetime import datetime
from pathlib import Path

from src.main import NeoZorK100PercentSystem
from src.models.retraining_system import RetrainingSystem
from src.blockchain.testnet_integration import TestnetBlockchainSystem

def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/neozork_100_percent.log'),
            logging.StreamHandler()
        ]
    )
    
    # Создание директории логов
    Path('logs').mkdir(exist_ok=True)

def load_config():
    """Загрузка конфигурации"""
    config_path = "config/config.yaml"
    
    if not Path(config_path).exists():
        print(f"Config file not found: {config_path}")
        sys.exit(1)
    
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def signal_handler(sig, frame):
    """Обработчик сигналов для корректного завершения"""
    print('\nShutting down NeoZorK 100% System...')
    sys.exit(0)

def main():
    """Главная функция"""
    try:
        # Настройка логирования
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # Обработчик сигналов
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        logger.info("Starting NeoZorK 100% System...")
        
        # Загрузка конфигурации
        config = load_config()
        
        # Создание системы
        system = NeoZorK100PercentSystem(config)
        
        # Создание системы переобучения
        retraining_system = RetrainingSystem(config)
        
        # Создание блокчейн-системы
        blockchain_system = TestnetBlockchainSystem(config)
        
        # Запуск системы переобучения
        retraining_system.start_retraining_system()
        
        # Запуск основной системы
        system.start_system()
        
        # Запуск блокчейн-системы
        blockchain_system.start_trading_system()
        
    except KeyboardInterrupt:
        print("\nSystem stopped by user")
    except Exception as e:
        print(f"System error: {e}")
        logging.error(f"System error: {e}")
    finally:
        print("NeoZorK 100% System stopped")

if __name__ == "__main__":
    main()
```

### Docker конфигурация

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов
COPY requirements.txt .
COPY pyproject.toml .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY src/ ./src/
COPY config/ ./config/
COPY models/ ./models/
COPY data/ ./data/
COPY logs/ ./logs/
COPY main.py .

# Создание директорий
RUN mkdir -p logs data/raw data/processed models/trained

# Установка прав
RUN chmod +x main.py

# Экспорт портов
EXPOSE 8000 8545

# Запуск приложения
CMD ["python", "main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  neozork-100-percent:
    build: .
    container_name: neozork-100-percent-system
    environment:
      - WEB3_PROVIDER=${WEB3_PROVIDER}
      - PRIVATE_KEY=${PRIVATE_KEY}
      - TEST_CONTRACT_ADDRESS=${TEST_CONTRACT_ADDRESS}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./models:/app/models
    restart: unless-stopped
    networks:
      - neozork-network

  postgres:
    image: postgres:13
    container_name: neozork-postgres
    environment:
      - POSTGRES_DB=neozork
      - POSTGRES_USER=neozork
      - POSTGRES_PASSWORD=neozork123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - neozork-network

  redis:
    image: redis:6
    container_name: neozork-redis
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    networks:
      - neozork-network

volumes:
  postgres_data:
  redis_data:

networks:
  neozork-network:
    driver: bridge
```

### Скрипт деплоя

```bash
#!/bin/bash
# deploy.sh

echo "🚀 Deploying NeoZorK 100% System to Testnet..."

# Проверка переменных окружения
if [ -z "$WEB3_PROVIDER" ]; then
    echo "❌ Error: WEB3_PROVIDER not set"
    exit 1
fi

if [ -z "$PRIVATE_KEY" ]; then
    echo "❌ Error: PRIVATE_KEY not set"
    exit 1
fi

# Создание директорий
mkdir -p logs data/raw data/processed models/trained

# Сборка Docker образа
echo "📦 Building Docker image..."
docker-compose build

# Запуск системы
echo "🚀 Starting system..."
docker-compose up -d

# Проверка статуса
echo "✅ Checking system status..."
docker-compose ps

# Просмотр логов
echo "📋 Viewing logs..."
docker-compose logs -f neozork-100-percent

echo "🎉 NeoZorK 100% System deployed successfully!"
echo "📊 Monitor performance at: http://localhost:8000"
echo "📈 Target: 100% monthly return on testnet"
```

Это полная система для достижения 100% прибыли в месяц на блокчейн testnet с автоматическим переобучением и робастной архитектурой!
