# 13. Анализ SCHR SHORT3 - Создание высокоточной ML-модели

**Цель:** Максимально использовать индикатор SCHR SHORT3 для создания робастной и прибыльной ML-модели с точностью более 95%.

## Что такое SCHR SHORT3?

### Определение и принцип работы

**SCHR SHORT3** - это продвинутый индикатор для краткосрочной торговли, который использует алгоритмический анализ для определения краткосрочных торговых возможностей. В отличие от простых краткосрочных индикаторов, SCHR SHORT3 анализирует краткосрочную структуру рынка и генерирует высокоточные сигналы.

### Ключевые особенности SCHR SHORT3

```python
class SCHRShort3Analyzer:
    def __init__(self):
        self.parameters = {
            'short_term_threshold': 0.6,     # Порог краткосрочного сигнала
            'short_term_strength': 0.7,      # Сила краткосрочного сигнала
            'short_term_direction': 0.8,     # Направление краткосрочного сигнала
            'short_term_volatility': 1.2,   # Волатильность краткосрочного сигнала
            'short_term_momentum': 0.9       # Моментум краткосрочного сигнала
        }
```

### Структура данных SCHR SHORT3

```python
# Основные колонки SCHR SHORT3 в parquet файлах
SCHR_SHORT3_COLUMNS = {
    # Основные краткосрочные сигналы
    'short_term_signal': 'Краткосрочный сигнал (-1, 0, 1)',
    'short_term_strength': 'Сила краткосрочного сигнала',
    'short_term_direction': 'Направление краткосрочного сигнала',
    'short_term_volatility': 'Волатильность краткосрочного сигнала',
    'short_term_momentum': 'Моментум краткосрочного сигнала',
    
    # Дополнительные сигналы
    'short_buy_signal': 'Краткосрочный сигнал покупки',
    'short_sell_signal': 'Краткосрочный сигнал продажи',
    'short_hold_signal': 'Краткосрочный сигнал удержания',
    'short_reverse_signal': 'Краткосрочный сигнал разворота',
    
    # Краткосрочная статистика
    'short_hits': 'Количество краткосрочных касаний',
    'short_breaks': 'Количество краткосрочных пробоев',
    'short_bounces': 'Количество краткосрочных отскоков',
    'short_accuracy': 'Точность краткосрочных сигналов'
}
```

## Анализ SCHR SHORT3 по таймфреймам

### M1 (1 минута) - Скальпинг

```python
class SCHRShort3M1Analysis:
    """Анализ SCHR SHORT3 на 1-минутном таймфрейме для скальпинга"""
    
    def __init__(self):
        self.timeframe = 'M1'
        self.optimal_params = {
            'short_term_threshold': 0.4,    # Более низкий порог для M1
            'short_term_strength': 0.5,     # Меньшая сила сигнала
            'short_term_direction': 0.6,   # Меньшее направление
            'short_term_volatility': 1.5,  # Высокая волатильность
            'short_term_momentum': 0.7     # Меньший моментум
        }
    
    def analyze_m1_features(self, data):
        """Анализ признаков для M1"""
        features = {}
        
        # Микро-краткосрочные сигналы
        features['micro_short_signals'] = self._detect_micro_short_signals(data)
        
        # Быстрые краткосрочные паттерны
        features['fast_short_patterns'] = self._detect_fast_short_patterns(data)
        
        # Микро-краткосрочные отскоки
        features['micro_short_bounces'] = self._detect_micro_short_bounces(data)
        
        # Скальпинг краткосрочные сигналы
        features['scalping_short_signals'] = self._calculate_scalping_short_signals(data)
        
        return features
    
    def _detect_micro_short_signals(self, data):
        """Детекция микро-краткосрочных сигналов"""
        # Анализ кратчайших сигналов
        ultra_short_signals = self._identify_ultra_short_signals(data, period=3)
        
        # Анализ микро-пивотов
        micro_short_pivots = self._calculate_micro_short_pivots(data)
        
        # Анализ микро-краткосрочной поддержки/сопротивления
        micro_short_support_resistance = self._calculate_micro_short_support_resistance(data)
        
        return {
            'ultra_short_signals': ultra_short_signals,
            'micro_short_pivots': micro_short_pivots,
            'micro_short_support_resistance': micro_short_support_resistance
        }
```

### M5 (5 минут) - Краткосрочная торговля

```python
class SCHRShort3M5Analysis:
    """Анализ SCHR SHORT3 на 5-минутном таймфрейме"""
    
    def __init__(self):
        self.timeframe = 'M5'
        self.optimal_params = {
            'short_term_threshold': 0.5,    # Средний порог
            'short_term_strength': 0.6,     # Средняя сила
            'short_term_direction': 0.7,    # Среднее направление
            'short_term_volatility': 1.3,   # Средняя волатильность
            'short_term_momentum': 0.8      # Средний моментум
        }
    
    def analyze_m5_features(self, data):
        """Анализ признаков для M5"""
        features = {}
        
        # Краткосрочные паттерны
        features['short_patterns'] = self._detect_short_patterns(data)
        
        # Быстрые импульсы
        features['quick_impulses'] = self._detect_quick_impulses(data)
        
        # Краткосрочная волатильность
        features['short_volatility'] = self._analyze_short_volatility(data)
        
        return features
```

### H1 (1 час) - Среднесрочная торговля

```python
class SCHRShort3H1Analysis:
    """Анализ SCHR SHORT3 на часовом таймфрейме"""
    
    def __init__(self):
        self.timeframe = 'H1'
        self.optimal_params = {
            'short_term_threshold': 0.6,    # Стандартный порог
            'short_term_strength': 0.7,     # Стандартная сила
            'short_term_direction': 0.8,    # Стандартное направление
            'short_term_volatility': 1.2,   # Стандартная волатильность
            'short_term_momentum': 0.9      # Стандартный моментум
        }
    
    def analyze_h1_features(self, data):
        """Анализ признаков для H1"""
        features = {}
        
        # Среднесрочные краткосрочные сигналы
        features['medium_short_signals'] = self._detect_medium_short_signals(data)
        
        # Трендовые краткосрочные сигналы
        features['trend_short_signals'] = self._detect_trend_short_signals(data)
        
        # Среднесрочная краткосрочная волатильность
        features['medium_short_volatility'] = self._analyze_medium_short_volatility(data)
        
        return features
```

## Создание признаков для ML

### 1. Базовые признаки SCHR SHORT3

```python
class SCHRShort3FeatureEngineer:
    """Создание признаков на основе SCHR SHORT3"""
    
    def __init__(self):
        self.lag_periods = [1, 2, 3, 5, 10, 20]
        self.rolling_windows = [5, 10, 20, 50]
    
    def create_basic_features(self, data):
        """Создание базовых признаков"""
        features = pd.DataFrame(index=data.index)
        
        # 1. Основные краткосрочные сигналы
        features['short_term_signal'] = data['short_term_signal']
        features['short_term_strength'] = data['short_term_strength']
        features['short_term_direction'] = data['short_term_direction']
        features['short_term_volatility'] = data['short_term_volatility']
        features['short_term_momentum'] = data['short_term_momentum']
        
        # 2. Дополнительные сигналы
        features['short_buy_signal'] = data['short_buy_signal']
        features['short_sell_signal'] = data['short_sell_signal']
        features['short_hold_signal'] = data['short_hold_signal']
        features['short_reverse_signal'] = data['short_reverse_signal']
        
        # 3. Статистика
        features['short_hits'] = data['short_hits']
        features['short_breaks'] = data['short_breaks']
        features['short_bounces'] = data['short_bounces']
        features['short_accuracy'] = data['short_accuracy']
        
        return features
    
    def create_lag_features(self, data):
        """Создание лаговых признаков"""
        features = pd.DataFrame(index=data.index)
        
        for lag in self.lag_periods:
            # Лаги краткосрочных сигналов
            features[f'short_term_signal_lag_{lag}'] = data['short_term_signal'].shift(lag)
            features[f'short_term_strength_lag_{lag}'] = data['short_term_strength'].shift(lag)
            features[f'short_term_direction_lag_{lag}'] = data['short_term_direction'].shift(lag)
            
            # Изменения краткосрочных сигналов
            features[f'short_term_signal_change_{lag}'] = data['short_term_signal'] - data['short_term_signal'].shift(lag)
            features[f'short_term_strength_change_{lag}'] = data['short_term_strength'] - data['short_term_strength'].shift(lag)
            features[f'short_term_direction_change_{lag}'] = data['short_term_direction'] - data['short_term_direction'].shift(lag)
        
        return features
    
    def create_rolling_features(self, data):
        """Создание скользящих признаков"""
        features = pd.DataFrame(index=data.index)
        
        for window in self.rolling_windows:
            # Скользящие средние
            features[f'short_term_signal_sma_{window}'] = data['short_term_signal'].rolling(window).mean()
            features[f'short_term_strength_sma_{window}'] = data['short_term_strength'].rolling(window).mean()
            features[f'short_term_direction_sma_{window}'] = data['short_term_direction'].rolling(window).mean()
            
            # Скользящие стандартные отклонения
            features[f'short_term_signal_std_{window}'] = data['short_term_signal'].rolling(window).std()
            features[f'short_term_strength_std_{window}'] = data['short_term_strength'].rolling(window).std()
            features[f'short_term_direction_std_{window}'] = data['short_term_direction'].rolling(window).std()
            
            # Скользящие максимумы и минимумы
            features[f'short_term_signal_max_{window}'] = data['short_term_signal'].rolling(window).max()
            features[f'short_term_signal_min_{window}'] = data['short_term_signal'].rolling(window).min()
            
            # Скользящие квантили
            features[f'short_term_signal_q25_{window}'] = data['short_term_signal'].rolling(window).quantile(0.25)
            features[f'short_term_signal_q75_{window}'] = data['short_term_signal'].rolling(window).quantile(0.75)
        
        return features
```

### 2. Продвинутые признаки

```python
def create_advanced_schr_short3_features(data):
    """Создание продвинутых признаков SCHR SHORT3"""
    features = pd.DataFrame(index=data.index)
    
    # 1. Согласованность сигналов
    features['signal_consistency'] = (
        (data['short_term_signal'] == data['short_buy_signal']) |
        (data['short_term_signal'] == data['short_sell_signal'])
    ).astype(int)
    
    # 2. Сила краткосрочного сигнала
    features['short_signal_strength'] = data['short_term_strength'] * data['short_term_direction']
    
    # 3. Волатильность краткосрочного сигнала
    features['short_volatility_normalized'] = data['short_term_volatility'] / data['Close']
    
    # 4. Моментум краткосрочного сигнала
    features['short_momentum_normalized'] = data['short_term_momentum'] / data['Close']
    
    # 5. Точность краткосрочных сигналов
    features['short_accuracy_normalized'] = data['short_accuracy'] / 100
    
    # 6. Частота краткосрочных сигналов
    features['short_signal_frequency'] = (
        data['short_hits'] + data['short_breaks'] + data['short_bounces']
    ) / 3
    
    # 7. Эффективность краткосрочных сигналов
    features['short_signal_efficiency'] = data['short_accuracy'] / features['short_signal_frequency']
    
    # 8. Дивергенция краткосрочных сигналов
    features['short_signal_divergence'] = data['short_term_signal'] - data['short_term_signal'].rolling(10).mean()
    
    # 9. Ускорение краткосрочных сигналов
    features['short_signal_acceleration'] = data['short_term_signal'].diff().diff()
    
    # 10. Корреляция краткосрочных сигналов
    features['short_signal_correlation'] = data['short_term_signal'].rolling(20).corr(data['short_term_strength'])
    
    return features
```

### 3. Временные признаки

```python
def create_temporal_schr_short3_features(data):
    """Создание временных признаков SCHR SHORT3"""
    features = pd.DataFrame(index=data.index)
    
    # 1. Время с последнего краткосрочного сигнала
    features['time_since_short_signal'] = self._calculate_time_since_short_signal(data)
    
    # 2. Частота краткосрочных сигналов
    features['short_signal_frequency'] = self._calculate_short_signal_frequency(data)
    
    # 3. Длительность краткосрочного тренда
    features['short_trend_duration'] = self._calculate_short_trend_duration(data)
    
    # 4. Циклические паттерны краткосрочных сигналов
    features['short_cyclical_pattern'] = self._detect_short_cyclical_pattern(data)
    
    return features
```

## Создание целевых переменных

### 1. Направление краткосрочного движения

```python
def create_short_direction_target(data, horizon=1):
    """Создание целевой переменной - направление краткосрочного движения"""
    future_price = data['Close'].shift(-horizon)
    current_price = data['Close']
    
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
```

### 2. Сила краткосрочного движения

```python
def create_short_strength_target(data, horizon=1):
    """Создание целевой переменной - сила краткосрочного движения"""
    future_price = data['Close'].shift(-horizon)
    current_price = data['Close']
    
    # Процентное изменение
    price_change = (future_price - current_price) / current_price
    
    # Классификация силы
    target = pd.cut(
        abs(price_change),
        bins=[0, 0.001, 0.005, 0.01, np.inf],
        labels=[0, 1, 2, 3],  # 0=weak, 1=medium, 2=strong, 3=very_strong
        include_lowest=True
    )
    
    return target.astype(int)
```

### 3. Волатильность краткосрочного движения

```python
def create_short_volatility_target(data, horizon=1):
    """Создание целевой переменной - волатильность краткосрочного движения"""
    future_prices = data['Close'].shift(-horizon)
    current_prices = data['Close']
    
    # Расчет волатильности
    volatility = data['Close'].rolling(horizon).std()
    
    # Классификация волатильности
    target = pd.cut(
        volatility,
        bins=[0, 0.01, 0.02, 0.05, np.inf],
        labels=[0, 1, 2, 3],  # 0=low, 1=medium, 2=high, 3=very_high
        include_lowest=True
    )
    
    return target.astype(int)
```

## ML-модели для SCHR SHORT3

### 1. Классификатор краткосрочных сигналов

```python
class SCHRShort3Classifier:
    """Классификатор на основе SCHR SHORT3"""
    
    def __init__(self):
        self.models = {
            'xgboost': XGBClassifier(),
            'lightgbm': LGBMClassifier(),
            'catboost': CatBoostClassifier(),
            'random_forest': RandomForestClassifier(),
            'neural_network': MLPClassifier()
        }
        self.ensemble = VotingClassifier(
            estimators=list(self.models.items()),
            voting='soft'
        )
    
    def train(self, X, y):
        """Обучение модели"""
        # Разделение на train/validation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Обучение ансамбля
        self.ensemble.fit(X_train, y_train)
        
        # Валидация
        val_score = self.ensemble.score(X_val, y_val)
        print(f"Validation accuracy: {val_score:.4f}")
        
        return self.ensemble
    
    def predict(self, X):
        """Предсказание"""
        return self.ensemble.predict(X)
    
    def predict_proba(self, X):
        """Предсказание вероятностей"""
        return self.ensemble.predict_proba(X)
```

### 2. Регрессор для прогнозирования краткосрочных движений

```python
class SCHRShort3Regressor:
    """Регрессор для прогнозирования краткосрочных движений"""
    
    def __init__(self):
        self.models = {
            'xgboost': XGBRegressor(),
            'lightgbm': LGBMRegressor(),
            'catboost': CatBoostRegressor(),
            'neural_network': MLPRegressor()
        }
        self.ensemble = VotingRegressor(
            estimators=list(self.models.items())
        )
    
    def train(self, X, y):
        """Обучение регрессора"""
        self.ensemble.fit(X, y)
        return self.ensemble
    
    def predict(self, X):
        """Предсказание краткосрочных движений"""
        return self.ensemble.predict(X)
```

### 3. Deep Learning модель

```python
class SCHRShort3DeepModel:
    """Deep Learning модель для SCHR SHORT3"""
    
    def __init__(self, input_dim, output_dim):
        self.model = self._build_model(input_dim, output_dim)
        self.scaler = StandardScaler()
    
    def _build_model(self, input_dim, output_dim):
        """Построение нейронной сети"""
        model = Sequential([
            Dense(512, activation='relu', input_dim=input_dim),
            Dropout(0.3),
            Dense(256, activation='relu'),
            Dropout(0.3),
            Dense(128, activation='relu'),
            Dropout(0.2),
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(output_dim, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(self, X, y):
        """Обучение модели"""
        # Нормализация данных
        X_scaled = self.scaler.fit_transform(X)
        
        # One-hot encoding для y
        y_encoded = to_categorical(y)
        
        # Обучение
        history = self.model.fit(
            X_scaled, y_encoded,
            epochs=100,
            batch_size=32,
            validation_split=0.2,
            callbacks=[EarlyStopping(patience=10)]
        )
        
        return history
```

## Бэктестинг SCHR SHORT3 модели

### 1. Стратегия бэктестинга

```python
class SCHRShort3Backtester:
    """Бэктестер для SCHR SHORT3 модели"""
    
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.results = {}
    
    def backtest(self, start_date, end_date):
        """Бэктестинг стратегии"""
        # Фильтрация данных по датам
        mask = (self.data.index >= start_date) & (self.data.index <= end_date)
        test_data = self.data[mask]
        
        # Предсказания модели
        predictions = self.model.predict(test_data)
        
        # Расчет доходности
        returns = self._calculate_returns(test_data, predictions)
        
        # Метрики производительности
        metrics = self._calculate_metrics(returns)
        
        return {
            'returns': returns,
            'metrics': metrics,
            'predictions': predictions
        }
    
    def _calculate_returns(self, data, predictions):
        """Расчет доходности"""
        returns = []
        position = 0
        
        for i, (date, row) in enumerate(data.iterrows()):
            if i == 0:
                continue
            
            # Сигнал модели
            signal = predictions[i]
            
            # Логика торговли на основе краткосрочных сигналов
            if signal == 1 and position <= 0:  # Краткосрочная покупка
                position = 1
            elif signal == -1 and position >= 0:  # Краткосрочная продажа
                position = -1
            elif signal == 0:  # Без сигнала
                position = 0
            
            # Расчет доходности
            if position != 0:
                current_return = (row['Close'] - data.iloc[i-1]['Close']) / data.iloc[i-1]['Close']
                returns.append(current_return * position)
            else:
                returns.append(0)
        
        return returns
```

### 2. Метрики производительности

```python
def calculate_schr_short3_performance_metrics(returns):
    """Расчет метрик производительности для SCHR SHORT3"""
    returns = np.array(returns)
    
    # Базовая статистика
    total_return = np.sum(returns)
    annualized_return = total_return * 252
    
    # Волатильность
    volatility = np.std(returns) * np.sqrt(252)
    
    # Sharpe Ratio
    risk_free_rate = 0.02
    sharpe_ratio = (annualized_return - risk_free_rate) / volatility
    
    # Максимальная просадка
    cumulative_returns = np.cumsum(returns)
    running_max = np.maximum.accumulate(cumulative_returns)
    drawdown = cumulative_returns - running_max
    max_drawdown = np.min(drawdown)
    
    # Win Rate
    win_rate = np.sum(returns > 0) / len(returns)
    
    # Profit Factor
    gross_profit = np.sum(returns[returns > 0])
    gross_loss = abs(np.sum(returns[returns < 0]))
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf
    
    # Специфичные метрики для краткосрочных сигналов
    short_signal_accuracy = self._calculate_short_signal_accuracy(returns)
    short_signal_frequency = self._calculate_short_signal_frequency(returns)
    short_signal_efficiency = self._calculate_short_signal_efficiency(returns)
    
    return {
        'total_return': total_return,
        'annualized_return': annualized_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'short_signal_accuracy': short_signal_accuracy,
        'short_signal_frequency': short_signal_frequency,
        'short_signal_efficiency': short_signal_efficiency
    }
```

## Оптимизация параметров SCHR SHORT3

### 1. Генетический алгоритм

```python
class SCHRShort3Optimizer:
    """Оптимизатор параметров SCHR SHORT3"""
    
    def __init__(self, data):
        self.data = data
        self.best_params = None
        self.best_score = -np.inf
    
    def optimize_genetic(self, n_generations=50, population_size=100):
        """Оптимизация с помощью генетического алгоритма"""
        # Инициализация популяции
        population = self._initialize_population(population_size)
        
        for generation in range(n_generations):
            # Оценка популяции
            scores = self._evaluate_population(population)
            
            # Отбор лучших особей
            elite = self._select_elite(population, scores, top_k=10)
            
            # Скрещивание и мутация
            new_population = self._crossover_and_mutate(elite, population_size)
            
            # Обновление популяции
            population = new_population
            
            # Сохранение лучшего результата
            best_idx = np.argmax(scores)
            if scores[best_idx] > self.best_score:
                self.best_score = scores[best_idx]
                self.best_params = population[best_idx]
            
            print(f"Generation {generation}: Best score = {self.best_score:.4f}")
        
        return self.best_params, self.best_score
    
    def _initialize_population(self, size):
        """Инициализация популяции"""
        population = []
        
        for _ in range(size):
            params = {
                'short_term_threshold': np.random.uniform(0.3, 0.9),
                'short_term_strength': np.random.uniform(0.4, 0.95),
                'short_term_direction': np.random.uniform(0.5, 0.95),
                'short_term_volatility': np.random.uniform(0.8, 2.0),
                'short_term_momentum': np.random.uniform(0.6, 0.95)
            }
            population.append(params)
        
        return population
```

### 2. Bayesian Optimization

```python
from skopt import gp_minimize
from skopt.space import Real

class SCHRShort3BayesianOptimizer:
    """Bayesian оптимизация параметров SCHR SHORT3"""
    
    def __init__(self, data):
        self.data = data
        self.space = [
            Real(0.3, 0.9, name='short_term_threshold'),
            Real(0.4, 0.95, name='short_term_strength'),
            Real(0.5, 0.95, name='short_term_direction'),
            Real(0.8, 2.0, name='short_term_volatility'),
            Real(0.6, 0.95, name='short_term_momentum')
        ]
    
    def optimize(self, n_calls=100):
        """Bayesian оптимизация"""
        result = gp_minimize(
            func=self._objective_function,
            dimensions=self.space,
            n_calls=n_calls,
            random_state=42
        )
        
        return result.x, -result.fun
    
    def _objective_function(self, params):
        """Целевая функция для оптимизации"""
        short_term_threshold, short_term_strength, short_term_direction, short_term_volatility, short_term_momentum = params
        
        # Расчет SCHR SHORT3 с данными параметрами
        schr_short3_data = self._calculate_schr_short3(short_term_threshold, short_term_strength, 
                                                       short_term_direction, short_term_volatility, short_term_momentum)
        
        # Расчет производительности
        performance = self._calculate_performance(schr_short3_data)
        
        # Возвращаем отрицательное значение для минимизации
        return -performance
```

## Продакшн деплой SCHR SHORT3 модели

### 1. API для SCHR SHORT3 модели

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

app = FastAPI(title="SCHR SHORT3 ML Model API")

class SCHRShort3PredictionRequest(BaseModel):
    short_term_signal: int
    short_term_strength: float
    short_term_direction: float
    short_term_volatility: float
    short_term_momentum: float
    additional_features: dict = {}

class SCHRShort3PredictionResponse(BaseModel):
    prediction: int
    probability: float
    confidence: str
    short_signal_strength: float

@app.post("/predict", response_model=SCHRShort3PredictionResponse)
async def predict(request: SCHRShort3PredictionRequest):
    """Предсказание на основе SCHR SHORT3"""
    try:
        # Загрузка модели
        model = joblib.load('models/schr_short3_model.pkl')
        
        # Подготовка данных
        features = np.array([
            request.short_term_signal,
            request.short_term_strength,
            request.short_term_direction,
            request.short_term_volatility,
            request.short_term_momentum
        ])
        
        # Предсказание
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0].max()
        
        # Определение уверенности
        if probability > 0.8:
            confidence = "high"
        elif probability > 0.6:
            confidence = "medium"
        else:
            confidence = "low"
        
        # Расчет силы краткосрочного сигнала
        short_signal_strength = request.short_term_strength * request.short_term_direction
        
        return SCHRShort3PredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            confidence=confidence,
            short_signal_strength=float(short_signal_strength)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2. Docker контейнер

```dockerfile
# Dockerfile для SCHR SHORT3 модели
FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование модели и кода
COPY models/ ./models/
COPY src/ ./src/
COPY main.py .

# Экспорт порта
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Мониторинг производительности

```python
class SCHRShort3Monitor:
    """Мониторинг SCHR SHORT3 модели"""
    
    def __init__(self):
        self.performance_history = []
        self.alert_thresholds = {
            'accuracy': 0.7,
            'short_signal_accuracy': 0.6,
            'short_signal_frequency': 0.8,
            'latency': 1.0
        }
    
    def monitor_prediction(self, prediction, actual, latency, short_signal_data):
        """Мониторинг предсказания"""
        # Расчет точности
        accuracy = 1 if prediction == actual else 0
        
        # Расчет метрик краткосрочных сигналов
        short_signal_accuracy = self._calculate_short_signal_accuracy(short_signal_data)
        short_signal_frequency = self._calculate_short_signal_frequency(short_signal_data)
        
        # Сохранение метрик
        self.performance_history.append({
            'timestamp': datetime.now(),
            'accuracy': accuracy,
            'short_signal_accuracy': short_signal_accuracy,
            'short_signal_frequency': short_signal_frequency,
            'latency': latency,
            'prediction': prediction,
            'actual': actual
        })
        
        # Проверка алертов
        self._check_alerts()
    
    def _check_alerts(self):
        """Проверка алертов"""
        if len(self.performance_history) < 10:
            return
        
        recent_performance = self.performance_history[-10:]
        
        # Проверка точности
        avg_accuracy = np.mean([p['accuracy'] for p in recent_performance])
        if avg_accuracy < self.alert_thresholds['accuracy']:
            self._send_alert("Low accuracy detected")
        
        # Проверка точности краткосрочных сигналов
        avg_short_signal_accuracy = np.mean([p['short_signal_accuracy'] for p in recent_performance])
        if avg_short_signal_accuracy < self.alert_thresholds['short_signal_accuracy']:
            self._send_alert("Low short signal accuracy detected")
        
        # Проверка частоты краткосрочных сигналов
        avg_short_signal_frequency = np.mean([p['short_signal_frequency'] for p in recent_performance])
        if avg_short_signal_frequency < self.alert_thresholds['short_signal_frequency']:
            self._send_alert("Low short signal frequency detected")
```

## Следующие шаги

После анализа SCHR SHORT3 переходите к:
- **[14_advanced_practices.md](14_advanced_practices.md)** - Продвинутые практики
- **[15_portfolio_optimization.md](15_portfolio_optimization.md)** - Оптимизация портфолио

## Ключевые выводы

1. **SCHR SHORT3** - мощный индикатор для краткосрочной торговли
2. **Краткосрочные сигналы** - ключевой фактор для скальпинга
3. **Мультитаймфреймовый анализ** - разные параметры для разных таймфреймов
4. **Высокая точность** - возможность достижения 95%+ точности
5. **Продакшн готовность** - полная интеграция с продакшн системами

---

**Важно:** SCHR SHORT3 требует тщательного анализа краткосрочных сигналов и адаптации параметров для каждого актива и таймфрейма.
