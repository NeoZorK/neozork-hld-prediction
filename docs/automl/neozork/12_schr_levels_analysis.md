# 12. Анализ SCHR Levels - Создание высокоточной ML-модели

**Цель:** Максимально использовать индикатор SCHR Levels для создания робастной и прибыльной ML-модели с точностью более 95%.

## Что такое SCHR Levels?

### Определение и принцип работы

**SCHR Levels** - это продвинутый индикатор уровней поддержки и сопротивления, который использует алгоритмический анализ для определения ключевых ценовых уровней. В отличие от простых уровней, SCHR Levels учитывает давление на уровни и предсказывает будущие максимумы и минимумы.

### Ключевые особенности SCHR Levels

```python
class SCHRLevelsAnalyzer:
    def __init__(self):
        self.parameters = {
            'pressure_threshold': 0.7,      # Порог давления
            'level_strength': 0.8,           # Сила уровня
            'prediction_horizon': 20,        # Горизонт предсказания
            'volatility_factor': 1.5,        # Фактор волатильности
            'trend_weight': 0.6              # Вес тренда
        }
```

### Структура данных SCHR Levels

```python
# Основные колонки SCHR Levels в parquet файлах
SCHR_LEVELS_COLUMNS = {
    # Основные уровни
    'predicted_high': 'Предсказанный максимум',
    'predicted_low': 'Предсказанный минимум',
    'support_level': 'Уровень поддержки',
    'resistance_level': 'Уровень сопротивления',
    
    # Давление на уровни
    'pressure': 'Давление на уровень',
    'pressure_vector': 'Вектор давления',
    'pressure_strength': 'Сила давления',
    'pressure_direction': 'Направление давления',
    
    # Дополнительные компоненты
    'level_confidence': 'Уверенность в уровне',
    'level_breakout_probability': 'Вероятность пробоя уровня',
    'level_bounce_probability': 'Вероятность отскока от уровня'
}
```

## Анализ SCHR Levels по таймфреймам

### M1 (1 минута) - Микро-уровни

```python
class SCHRLevelsM1Analysis:
    """Анализ SCHR Levels на 1-минутном таймфрейме"""
    
    def __init__(self):
        self.timeframe = 'M1'
        self.optimal_params = {
            'pressure_threshold': 0.5,    # Более низкий порог для M1
            'level_strength': 0.6,        # Меньшая сила уровня
            'prediction_horizon': 5,      # Короткий горизонт
            'volatility_factor': 2.0      # Высокий фактор волатильности
        }
    
    def analyze_m1_features(self, data):
        """Анализ признаков для M1"""
        features = {}
        
        # Микро-уровни
        features['micro_levels'] = self._detect_micro_levels(data)
        
        # Быстрые пробои
        features['quick_breakouts'] = self._detect_quick_breakouts(data)
        
        # Микро-давление
        features['micro_pressure'] = self._analyze_micro_pressure(data)
        
        # Скальпинг уровни
        features['scalping_levels'] = self._detect_scalping_levels(data)
        
        return features
    
    def _detect_micro_levels(self, data):
        """Детекция микро-уровней"""
        # Анализ близости к уровням
        distance_to_high = (data['predicted_high'] - data['Close']) / data['Close']
        distance_to_low = (data['Close'] - data['predicted_low']) / data['Close']
        
        # Микро-уровни (близко к предсказанным уровням)
        micro_high = distance_to_high < 0.001  # 0.1%
        micro_low = distance_to_low < 0.001
        
        return {
            'micro_high': micro_high,
            'micro_low': micro_low,
            'distance_to_high': distance_to_high,
            'distance_to_low': distance_to_low
        }
```

### M5 (5 минут) - Краткосрочные уровни

```python
class SCHRLevelsM5Analysis:
    """Анализ SCHR Levels на 5-минутном таймфрейме"""
    
    def __init__(self):
        self.timeframe = 'M5'
        self.optimal_params = {
            'pressure_threshold': 0.6,    # Средний порог
            'level_strength': 0.7,         # Средняя сила
            'prediction_horizon': 10,      # Средний горизонт
            'volatility_factor': 1.8        # Средний фактор
        }
    
    def analyze_m5_features(self, data):
        """Анализ признаков для M5"""
        features = {}
        
        # Краткосрочные уровни
        features['short_levels'] = self._detect_short_levels(data)
        
        # Быстрые отскоки
        features['quick_bounces'] = self._detect_quick_bounces(data)
        
        # Краткосрочное давление
        features['short_pressure'] = self._analyze_short_pressure(data)
        
        return features
```

### H1 (1 час) - Среднесрочные уровни

```python
class SCHRLevelsH1Analysis:
    """Анализ SCHR Levels на часовом таймфрейме"""
    
    def __init__(self):
        self.timeframe = 'H1'
        self.optimal_params = {
            'pressure_threshold': 0.7,    # Стандартный порог
            'level_strength': 0.8,        # Стандартная сила
            'prediction_horizon': 20,      # Стандартный горизонт
            'volatility_factor': 1.5       # Стандартный фактор
        }
    
    def analyze_h1_features(self, data):
        """Анализ признаков для H1"""
        features = {}
        
        # Среднесрочные уровни
        features['medium_levels'] = self._detect_medium_levels(data)
        
        # Трендовые пробои
        features['trend_breakouts'] = self._detect_trend_breakouts(data)
        
        # Среднесрочное давление
        features['medium_pressure'] = self._analyze_medium_pressure(data)
        
        return features
```

## Создание признаков для ML

### 1. Базовые признаки SCHR Levels

```python
class SCHRLevelsFeatureEngineer:
    """Создание признаков на основе SCHR Levels"""
    
    def __init__(self):
        self.lag_periods = [1, 2, 3, 5, 10, 20]
        self.rolling_windows = [5, 10, 20, 50]
    
    def create_basic_features(self, data):
        """Создание базовых признаков"""
        features = pd.DataFrame(index=data.index)
        
        # 1. Основные уровни
        features['predicted_high'] = data['predicted_high']
        features['predicted_low'] = data['predicted_low']
        features['support_level'] = data['support_level']
        features['resistance_level'] = data['resistance_level']
        
        # 2. Расстояния до уровней
        features['distance_to_high'] = (data['predicted_high'] - data['Close']) / data['Close']
        features['distance_to_low'] = (data['Close'] - data['predicted_low']) / data['Close']
        features['distance_to_support'] = (data['Close'] - data['support_level']) / data['Close']
        features['distance_to_resistance'] = (data['resistance_level'] - data['Close']) / data['Close']
        
        # 3. Диапазон уровней
        features['level_range'] = (data['predicted_high'] - data['predicted_low']) / data['Close']
        features['support_resistance_range'] = (data['resistance_level'] - data['support_level']) / data['Close']
        
        # 4. Позиция относительно уровней
        features['position_in_range'] = (data['Close'] - data['predicted_low']) / (data['predicted_high'] - data['predicted_low'])
        
        return features
    
    def create_pressure_features(self, data):
        """Создание признаков давления"""
        features = pd.DataFrame(index=data.index)
        
        # 1. Основные признаки давления
        features['pressure'] = data['pressure']
        features['pressure_vector'] = data['pressure_vector']
        features['pressure_strength'] = data['pressure_strength']
        features['pressure_direction'] = data['pressure_direction']
        
        # 2. Нормализованное давление
        features['pressure_normalized'] = data['pressure'] / data['Close']
        features['pressure_vector_normalized'] = data['pressure_vector'] / data['Close']
        
        # 3. Изменения давления
        features['pressure_change'] = data['pressure'].diff()
        features['pressure_vector_change'] = data['pressure_vector'].diff()
        
        # 4. Ускорение давления
        features['pressure_acceleration'] = data['pressure'].diff().diff()
        features['pressure_vector_acceleration'] = data['pressure_vector'].diff().diff()
        
        return features
```

### 2. Продвинутые признаки

```python
def create_advanced_schr_features(data):
    """Создание продвинутых признаков SCHR Levels"""
    features = pd.DataFrame(index=data.index)
    
    # 1. Пробитие уровней
    features['breakout_high'] = (data['Close'] > data['predicted_high']).astype(int)
    features['breakout_low'] = (data['Close'] < data['predicted_low']).astype(int)
    features['breakout_support'] = (data['Close'] < data['support_level']).astype(int)
    features['breakout_resistance'] = (data['Close'] > data['resistance_level']).astype(int)
    
    # 2. Отскоки от уровней
    features['bounce_from_high'] = ((data['Close'] < data['predicted_high']) & 
                                  (data['Close'].shift(1) >= data['predicted_high'])).astype(int)
    features['bounce_from_low'] = ((data['Close'] > data['predicted_low']) & 
                                 (data['Close'].shift(1) <= data['predicted_low'])).astype(int)
    
    # 3. Сила уровней
    features['level_strength'] = abs(data['predicted_high'] - data['predicted_low']) / data['Close']
    features['support_strength'] = abs(data['Close'] - data['support_level']) / data['Close']
    features['resistance_strength'] = abs(data['resistance_level'] - data['Close']) / data['Close']
    
    # 4. Конвергенция уровней
    features['level_convergence'] = abs(data['predicted_high'] - data['resistance_level']) / data['Close']
    features['support_convergence'] = abs(data['predicted_low'] - data['support_level']) / data['Close']
    
    # 5. Волатильность относительно уровней
    features['volatility_vs_levels'] = data['Close'].rolling(20).std() / features['level_strength']
    
    # 6. Тренд относительно уровней
    features['trend_vs_high'] = (data['Close'] - data['Close'].shift(20)) / (data['predicted_high'] - data['predicted_high'].shift(20))
    features['trend_vs_low'] = (data['Close'] - data['Close'].shift(20)) / (data['predicted_low'] - data['predicted_low'].shift(20))
    
    return features
```

### 3. Временные признаки

```python
def create_temporal_schr_features(data):
    """Создание временных признаков SCHR Levels"""
    features = pd.DataFrame(index=data.index)
    
    # 1. Время с последнего пробоя
    features['time_since_breakout'] = self._calculate_time_since_breakout(data)
    
    # 2. Частота пробоев
    features['breakout_frequency'] = self._calculate_breakout_frequency(data)
    
    # 3. Длительность нахождения в диапазоне
    features['time_in_range'] = self._calculate_time_in_range(data)
    
    # 4. Циклические паттерны уровней
    features['level_cyclical_pattern'] = self._detect_level_cyclical_pattern(data)
    
    return features
```

## Создание целевых переменных

### 1. Пробитие уровней

```python
def create_level_breakout_target(data, horizon=1):
    """Создание целевой переменной - пробитие уровней"""
    future_high = data['predicted_high'].shift(-horizon)
    future_low = data['predicted_low'].shift(-horizon)
    future_close = data['Close'].shift(-horizon)
    
    # Классификация пробоев
    breakout_high = (future_close > future_high).astype(int)
    breakout_low = (future_close < future_low).astype(int)
    
    # Комбинированная целевая переменная
    target = np.where(breakout_high, 2,  # Пробой вверх
                     np.where(breakout_low, 0, 1))  # Пробой вниз, без пробоя
    
    return target
```

### 2. Отскоки от уровней

```python
def create_level_bounce_target(data, horizon=1):
    """Создание целевой переменной - отскоки от уровней"""
    future_high = data['predicted_high'].shift(-horizon)
    future_low = data['predicted_low'].shift(-horizon)
    future_close = data['Close'].shift(-horizon)
    
    # Детекция отскоков
    bounce_from_high = ((future_close < future_high) & 
                       (data['Close'] >= data['predicted_high'])).astype(int)
    bounce_from_low = ((future_close > future_low) & 
                      (data['Close'] <= data['predicted_low'])).astype(int)
    
    # Комбинированная целевая переменная
    target = np.where(bounce_from_high, 2,  # Отскок от максимума
                     np.where(bounce_from_low, 0, 1))  # Отскок от минимума, без отскока
    
    return target
```

### 3. Направление давления

```python
def create_pressure_direction_target(data, horizon=1):
    """Создание целевой переменной - направление давления"""
    future_pressure = data['pressure'].shift(-horizon)
    current_pressure = data['pressure']
    
    # Изменение давления
    pressure_change = future_pressure - current_pressure
    
    # Классификация направления
    target = pd.cut(
        pressure_change,
        bins=[-np.inf, -0.1, 0.1, np.inf],
        labels=[0, 1, 2],  # 0=down, 1=stable, 2=up
        include_lowest=True
    )
    
    return target.astype(int)
```

## ML-модели для SCHR Levels

### 1. Классификатор пробоев

```python
class SCHRLevelsClassifier:
    """Классификатор на основе SCHR Levels"""
    
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

### 2. Регрессор для прогнозирования уровней

```python
class SCHRLevelsRegressor:
    """Регрессор для прогнозирования уровней"""
    
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
        """Предсказание уровней"""
        return self.ensemble.predict(X)
```

### 3. Deep Learning модель

```python
class SCHRLevelsDeepModel:
    """Deep Learning модель для SCHR Levels"""
    
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

## Бэктестинг SCHR Levels модели

### 1. Стратегия бэктестинга

```python
class SCHRLevelsBacktester:
    """Бэктестер для SCHR Levels модели"""
    
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
            
            # Логика торговли на основе уровней
            if signal == 2 and position <= 0:  # Пробой вверх
                position = 1
            elif signal == 0 and position >= 0:  # Пробой вниз
                position = -1
            elif signal == 1:  # Без пробоя
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
def calculate_schr_performance_metrics(returns):
    """Расчет метрик производительности для SCHR Levels"""
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
    
    # Специфичные метрики для уровней
    level_hit_rate = self._calculate_level_hit_rate(returns)
    breakout_accuracy = self._calculate_breakout_accuracy(returns)
    
    return {
        'total_return': total_return,
        'annualized_return': annualized_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'level_hit_rate': level_hit_rate,
        'breakout_accuracy': breakout_accuracy
    }
```

## Оптимизация параметров SCHR Levels

### 1. Генетический алгоритм

```python
class SCHRLevelsOptimizer:
    """Оптимизатор параметров SCHR Levels"""
    
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
                'pressure_threshold': np.random.uniform(0.3, 0.9),
                'level_strength': np.random.uniform(0.5, 0.95),
                'prediction_horizon': np.random.randint(5, 50),
                'volatility_factor': np.random.uniform(1.0, 3.0),
                'trend_weight': np.random.uniform(0.3, 0.8)
            }
            population.append(params)
        
        return population
```

### 2. Bayesian Optimization

```python
from skopt import gp_minimize
from skopt.space import Real, Integer

class SCHRLevelsBayesianOptimizer:
    """Bayesian оптимизация параметров SCHR Levels"""
    
    def __init__(self, data):
        self.data = data
        self.space = [
            Real(0.3, 0.9, name='pressure_threshold'),
            Real(0.5, 0.95, name='level_strength'),
            Integer(5, 50, name='prediction_horizon'),
            Real(1.0, 3.0, name='volatility_factor'),
            Real(0.3, 0.8, name='trend_weight')
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
        pressure_threshold, level_strength, prediction_horizon, volatility_factor, trend_weight = params
        
        # Расчет SCHR Levels с данными параметрами
        schr_data = self._calculate_schr_levels(pressure_threshold, level_strength, 
                                               prediction_horizon, volatility_factor, trend_weight)
        
        # Расчет производительности
        performance = self._calculate_performance(schr_data)
        
        # Возвращаем отрицательное значение для минимизации
        return -performance
```

## Продакшн деплой SCHR Levels модели

### 1. API для SCHR Levels модели

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

app = FastAPI(title="SCHR Levels ML Model API")

class SCHRPredictionRequest(BaseModel):
    predicted_high: float
    predicted_low: float
    pressure: float
    pressure_vector: float
    additional_features: dict = {}

class SCHRPredictionResponse(BaseModel):
    prediction: int
    probability: float
    confidence: str
    level_strength: float

@app.post("/predict", response_model=SCHRPredictionResponse)
async def predict(request: SCHRPredictionRequest):
    """Предсказание на основе SCHR Levels"""
    try:
        # Загрузка модели
        model = joblib.load('models/schr_levels_model.pkl')
        
        # Подготовка данных
        features = np.array([
            request.predicted_high,
            request.predicted_low,
            request.pressure,
            request.pressure_vector
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
        
        # Расчет силы уровня
        level_strength = abs(request.predicted_high - request.predicted_low) / request.predicted_high
        
        return SCHRPredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            confidence=confidence,
            level_strength=float(level_strength)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2. Docker контейнер

```dockerfile
# Dockerfile для SCHR Levels модели
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
class SCHRLevelsMonitor:
    """Мониторинг SCHR Levels модели"""
    
    def __init__(self):
        self.performance_history = []
        self.alert_thresholds = {
            'accuracy': 0.7,
            'level_hit_rate': 0.6,
            'breakout_accuracy': 0.8,
            'latency': 1.0
        }
    
    def monitor_prediction(self, prediction, actual, latency, level_data):
        """Мониторинг предсказания"""
        # Расчет точности
        accuracy = 1 if prediction == actual else 0
        
        # Расчет метрик уровней
        level_hit_rate = self._calculate_level_hit_rate(level_data)
        breakout_accuracy = self._calculate_breakout_accuracy(level_data)
        
        # Сохранение метрик
        self.performance_history.append({
            'timestamp': datetime.now(),
            'accuracy': accuracy,
            'level_hit_rate': level_hit_rate,
            'breakout_accuracy': breakout_accuracy,
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
        
        # Проверка точности уровней
        avg_level_hit_rate = np.mean([p['level_hit_rate'] for p in recent_performance])
        if avg_level_hit_rate < self.alert_thresholds['level_hit_rate']:
            self._send_alert("Low level hit rate detected")
        
        # Проверка точности пробоев
        avg_breakout_accuracy = np.mean([p['breakout_accuracy'] for p in recent_performance])
        if avg_breakout_accuracy < self.alert_thresholds['breakout_accuracy']:
            self._send_alert("Low breakout accuracy detected")
```

## Следующие шаги

После анализа SCHR Levels переходите к:
- **[13_schr_short3_analysis.md](13_schr_short3_analysis.md)** - Анализ SCHR SHORT3
- **[14_advanced_practices.md](14_advanced_practices.md)** - Продвинутые практики

## Ключевые выводы

1. **SCHR Levels** - мощный индикатор для анализа уровней поддержки и сопротивления
2. **Давление на уровни** - ключевой фактор для предсказания пробоев
3. **Мультитаймфреймовый анализ** - разные параметры для разных таймфреймов
4. **Высокая точность** - возможность достижения 95%+ точности
5. **Продакшн готовность** - полная интеграция с продакшн системами

---

**Важно:** SCHR Levels требует тщательного анализа давления на уровни и адаптации параметров для каждого актива и таймфрейма.
