# 11. Анализ индикатора WAVE2 - Создание высокоточной ML-модели

**Цель:** Максимально использовать индикатор WAVE2 для создания робастной и прибыльной ML-модели с точностью более 95%.

## Что такое WAVE2?

### Определение и принцип работы

**WAVE2** - это продвинутый трендовый индикатор, который использует двойную волновую систему для генерации торговых сигналов. В отличие от простых индикаторов, WAVE2 анализирует структуру рынка, а не просто сглаживает цену.

### Ключевые особенности WAVE2

```python
class WAVE2Analyzer:
    def __init__(self):
        self.parameters = {
            'long1': 339,      # Первый длинный период
            'fast1': 10,       # Первый быстрый период
            'trend1': 2,       # Первый трендовый период
            'tr1': 'fast',     # Первое торговое правило
            'long2': 22,       # Второй длинный период
            'fast2': 11,       # Второй быстрый период
            'trend2': 4,       # Второй трендовый период
            'tr2': 'fast',     # Второе торговое правило
            'global_tr': 'prime',  # Глобальное торговое правило
            'sma_period': 22   # Период SMA
        }
```

### Структура данных WAVE2

```python
# Основные колонки WAVE2 в parquet файлах
WAVE2_COLUMNS = {
    # Основные волны
    'wave1': 'Первая волна - основной трендовый компонент',
    'wave2': 'Вторая волна - дополнительный трендовый компонент',
    'fastline1': 'Быстрая линия первой волны',
    'fastline2': 'Быстрая линия второй волны',
    
    # Торговые сигналы
    'Wave1': 'Сигнал первой волны (-1, 0, 1)',
    'Wave2': 'Сигнал второй волны (-1, 0, 1)',
    '_Signal': 'Финальный торговый сигнал',
    '_Direction': 'Направление сигнала',
    '_LastSignal': 'Последний подтвержденный сигнал',
    
    # Визуальные элементы
    '_Plot_Color': 'Цвет для отображения',
    '_Plot_Wave': 'Значение волны для отображения',
    '_Plot_FastLine': 'Значение быстрой линии для отображения',
    
    # Дополнительные компоненты
    'ecore1': 'Первый экор (экспоненциальное ядро)',
    'ecore2': 'Второй экор (экспоненциальное ядро)'
}
```

## Анализ WAVE2 по таймфреймам

### M1 (1 минута) - Скальпинг

```python
class WAVE2M1Analysis:
    """Анализ WAVE2 на 1-минутном таймфрейме для скальпинга"""
    
    def __init__(self):
        self.timeframe = 'M1'
        self.optimal_params = {
            'long1': 50,    # Более короткий период для M1
            'fast1': 5,      # Очень быстрый отклик
            'trend1': 1,    # Минимальный трендовый период
            'long2': 15,    # Короткий второй период
            'fast2': 3,     # Очень быстрая вторая волна
            'trend2': 1     # Минимальный тренд
        }
    
    def analyze_m1_features(self, data):
        """Анализ признаков для M1"""
        features = {}
        
        # Микро-тренды
        features['micro_trend'] = self._detect_micro_trend(data)
        
        # Быстрые развороты
        features['quick_reversal'] = self._detect_quick_reversal(data)
        
        # Скальпинг сигналы
        features['scalping_signal'] = self._detect_scalping_signal(data)
        
        # Микро-волатильность
        features['micro_volatility'] = self._calculate_micro_volatility(data)
        
        return features
    
    def _detect_micro_trend(self, data):
        """Детекция микро-трендов"""
        # Анализ пересечений wave1 и fastline1
        wave1 = data['wave1']
        fastline1 = data['fastline1']
        
        # Микро-тренд вверх
        uptrend = (wave1 > fastline1) & (wave1.shift(1) <= fastline1.shift(1))
        
        # Микро-тренд вниз
        downtrend = (wave1 < fastline1) & (wave1.shift(1) >= fastline1.shift(1))
        
        return {
            'uptrend': uptrend,
            'downtrend': downtrend,
            'strength': abs(wave1 - fastline1) / fastline1
        }
```

### M5 (5 минут) - Краткосрочная торговля

```python
class WAVE2M5Analysis:
    """Анализ WAVE2 на 5-минутном таймфрейме"""
    
    def __init__(self):
        self.timeframe = 'M5'
        self.optimal_params = {
            'long1': 100,   # Оптимальный для M5
            'fast1': 10,    # Быстрый отклик
            'trend1': 2,    # Короткий тренд
            'long2': 30,    # Средний второй период
            'fast2': 8,     # Быстрая вторая волна
            'trend2': 2     # Короткий тренд
        }
    
    def analyze_m5_features(self, data):
        """Анализ признаков для M5"""
        features = {}
        
        # Краткосрочные паттерны
        features['short_pattern'] = self._detect_short_pattern(data)
        
        # Быстрые импульсы
        features['quick_impulse'] = self._detect_quick_impulse(data)
        
        # Краткосрочная волатильность
        features['short_volatility'] = self._calculate_short_volatility(data)
        
        return features
```

### H1 (1 час) - Среднесрочная торговля

```python
class WAVE2H1Analysis:
    """Анализ WAVE2 на часовом таймфрейме"""
    
    def __init__(self):
        self.timeframe = 'H1'
        self.optimal_params = {
            'long1': 200,   # Стандартный для H1
            'fast1': 20,    # Средний отклик
            'trend1': 5,    # Средний тренд
            'long2': 50,    # Средний второй период
            'fast2': 15,    # Средняя вторая волна
            'trend2': 3     # Средний тренд
        }
    
    def analyze_h1_features(self, data):
        """Анализ признаков для H1"""
        features = {}
        
        # Среднесрочные тренды
        features['medium_trend'] = self._detect_medium_trend(data)
        
        # Трендовые развороты
        features['trend_reversal'] = self._detect_trend_reversal(data)
        
        # Среднесрочная волатильность
        features['medium_volatility'] = self._calculate_medium_volatility(data)
        
        return features
```

## Создание признаков для ML

### 1. Базовые признаки WAVE2

```python
class WAVE2FeatureEngineer:
    """Создание признаков на основе WAVE2"""
    
    def __init__(self):
        self.lag_periods = [1, 2, 3, 5, 10, 20]
        self.rolling_windows = [5, 10, 20, 50]
    
    def create_basic_features(self, data):
        """Создание базовых признаков"""
        features = pd.DataFrame(index=data.index)
        
        # 1. Основные волны
        features['wave1'] = data['wave1']
        features['wave2'] = data['wave2']
        features['fastline1'] = data['fastline1']
        features['fastline2'] = data['fastline2']
        
        # 2. Разности волн
        features['wave_diff'] = data['wave1'] - data['wave2']
        features['fastline_diff'] = data['fastline1'] - data['fastline2']
        
        # 3. Отношения волн
        features['wave_ratio'] = data['wave1'] / data['wave2']
        features['fastline_ratio'] = data['fastline1'] / data['fastline2']
        
        # 4. Расстояния до нуля
        features['wave1_distance'] = abs(data['wave1'])
        features['wave2_distance'] = abs(data['wave2'])
        
        return features
    
    def create_lag_features(self, data):
        """Создание лаговых признаков"""
        features = pd.DataFrame(index=data.index)
        
        for lag in self.lag_periods:
            # Лаги волн
            features[f'wave1_lag_{lag}'] = data['wave1'].shift(lag)
            features[f'wave2_lag_{lag}'] = data['wave2'].shift(lag)
            
            # Лаги быстрых линий
            features[f'fastline1_lag_{lag}'] = data['fastline1'].shift(lag)
            features[f'fastline2_lag_{lag}'] = data['fastline2'].shift(lag)
            
            # Изменения волн
            features[f'wave1_change_{lag}'] = data['wave1'] - data['wave1'].shift(lag)
            features[f'wave2_change_{lag}'] = data['wave2'] - data['wave2'].shift(lag)
        
        return features
    
    def create_rolling_features(self, data):
        """Создание скользящих признаков"""
        features = pd.DataFrame(index=data.index)
        
        for window in self.rolling_windows:
            # Скользящие средние
            features[f'wave1_sma_{window}'] = data['wave1'].rolling(window).mean()
            features[f'wave2_sma_{window}'] = data['wave2'].rolling(window).mean()
            
            # Скользящие стандартные отклонения
            features[f'wave1_std_{window}'] = data['wave1'].rolling(window).std()
            features[f'wave2_std_{window}'] = data['wave2'].rolling(window).std()
            
            # Скользящие максимумы и минимумы
            features[f'wave1_max_{window}'] = data['wave1'].rolling(window).max()
            features[f'wave1_min_{window}'] = data['wave1'].rolling(window).min()
            
            # Скользящие квантили
            features[f'wave1_q25_{window}'] = data['wave1'].rolling(window).quantile(0.25)
            features[f'wave1_q75_{window}'] = data['wave1'].rolling(window).quantile(0.75)
        
        return features
```

### 2. Продвинутые признаки

```python
def create_advanced_wave2_features(data):
    """Создание продвинутых признаков WAVE2"""
    features = pd.DataFrame(index=data.index)
    
    # 1. Пересечения волн
    features['wave1_cross_fastline1'] = (data['wave1'] > data['fastline1']).astype(int)
    features['wave2_cross_fastline2'] = (data['wave2'] > data['fastline2']).astype(int)
    
    # 2. Согласованность сигналов
    features['signal_consistency'] = (
        (data['Wave1'] == data['Wave2']).astype(int)
    )
    
    # 3. Сила тренда
    features['trend_strength'] = abs(data['wave1'] - data['fastline1']) / abs(data['fastline1'])
    
    # 4. Ускорение волн
    features['wave1_acceleration'] = data['wave1'].diff().diff()
    features['wave2_acceleration'] = data['wave2'].diff().diff()
    
    # 5. Дивергенция волн
    features['wave_divergence'] = data['wave1'] - data['wave2']
    features['fastline_divergence'] = data['fastline1'] - data['fastline2']
    
    # 6. Волатильность волн
    features['wave1_volatility'] = data['wave1'].rolling(20).std()
    features['wave2_volatility'] = data['wave2'].rolling(20).std()
    
    # 7. Корреляция волн
    features['wave_correlation'] = data['wave1'].rolling(20).corr(data['wave2'])
    
    # 8. Моментум волн
    features['wave1_momentum'] = data['wave1'] - data['wave1'].shift(10)
    features['wave2_momentum'] = data['wave2'] - data['wave2'].shift(10)
    
    return features
```

### 3. Временные признаки

```python
def create_temporal_wave2_features(data):
    """Создание временных признаков WAVE2"""
    features = pd.DataFrame(index=data.index)
    
    # 1. Время с последнего сигнала
    features['time_since_signal'] = self._calculate_time_since_signal(data)
    
    # 2. Частота сигналов
    features['signal_frequency'] = self._calculate_signal_frequency(data)
    
    # 3. Длительность тренда
    features['trend_duration'] = self._calculate_trend_duration(data)
    
    # 4. Циклические паттерны
    features['cyclical_pattern'] = self._detect_cyclical_pattern(data)
    
    return features
```

## Создание целевых переменных

### 1. Направление цены

```python
def create_price_direction_target(data, horizon=1):
    """Создание целевой переменной - направление цены"""
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

### 2. Сила движения

```python
def create_movement_strength_target(data, horizon=1):
    """Создание целевой переменной - сила движения"""
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

### 3. Волатильность

```python
def create_volatility_target(data, horizon=1):
    """Создание целевой переменной - волатильность"""
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

## ML-модели для WAVE2

### 1. Классификация сигналов

```python
class WAVE2Classifier:
    """Классификатор на основе WAVE2"""
    
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

### 2. Регрессия для прогнозирования цены

```python
class WAVE2Regressor:
    """Регрессор на основе WAVE2"""
    
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
        """Предсказание цены"""
        return self.ensemble.predict(X)
```

### 3. Deep Learning модель

```python
class WAVE2DeepModel:
    """Deep Learning модель для WAVE2"""
    
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

## Бэктестинг WAVE2 модели

### 1. Стратегия бэктестинга

```python
class WAVE2Backtester:
    """Бэктестер для WAVE2 модели"""
    
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
            
            # Изменение позиции
            if signal == 1 and position <= 0:  # Покупка
                position = 1
            elif signal == -1 and position >= 0:  # Продажа
                position = -1
            elif signal == 0:  # Удержание
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
def calculate_performance_metrics(returns):
    """Расчет метрик производительности"""
    returns = np.array(returns)
    
    # Базовая статистика
    total_return = np.sum(returns)
    annualized_return = total_return * 252  # Предполагаем 252 торговых дня
    
    # Волатильность
    volatility = np.std(returns) * np.sqrt(252)
    
    # Sharpe Ratio
    risk_free_rate = 0.02  # 2% безрисковая ставка
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
    
    return {
        'total_return': total_return,
        'annualized_return': annualized_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'win_rate': win_rate,
        'profit_factor': profit_factor
    }
```

## Оптимизация параметров WAVE2

### 1. Генетический алгоритм

```python
class WAVE2Optimizer:
    """Оптимизатор параметров WAVE2"""
    
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
                'long1': np.random.randint(50, 500),
                'fast1': np.random.randint(5, 50),
                'trend1': np.random.randint(1, 10),
                'long2': np.random.randint(20, 200),
                'fast2': np.random.randint(5, 50),
                'trend2': np.random.randint(1, 10)
            }
            population.append(params)
        
        return population
```

### 2. Bayesian Optimization

```python
from skopt import gp_minimize
from skopt.space import Real, Integer

class WAVE2BayesianOptimizer:
    """Bayesian оптимизация параметров WAVE2"""
    
    def __init__(self, data):
        self.data = data
        self.space = [
            Integer(50, 500, name='long1'),
            Integer(5, 50, name='fast1'),
            Integer(1, 10, name='trend1'),
            Integer(20, 200, name='long2'),
            Integer(5, 50, name='fast2'),
            Integer(1, 10, name='trend2')
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
        long1, fast1, trend1, long2, fast2, trend2 = params
        
        # Расчет WAVE2 с данными параметрами
        wave2_data = self._calculate_wave2(long1, fast1, trend1, long2, fast2, trend2)
        
        # Расчет производительности
        performance = self._calculate_performance(wave2_data)
        
        # Возвращаем отрицательное значение для минимизации
        return -performance
```

## Продакшн деплой WAVE2 модели

### 1. API для WAVE2 модели

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

app = FastAPI(title="WAVE2 ML Model API")

class PredictionRequest(BaseModel):
    wave1: float
    wave2: float
    fastline1: float
    fastline2: float
    additional_features: dict = {}

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    confidence: str

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Предсказание на основе WAVE2"""
    try:
        # Загрузка модели
        model = joblib.load('models/wave2_model.pkl')
        
        # Подготовка данных
        features = np.array([
            request.wave1,
            request.wave2,
            request.fastline1,
            request.fastline2
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
        
        return PredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            confidence=confidence
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2. Docker контейнер

```dockerfile
# Dockerfile для WAVE2 модели
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
class WAVE2Monitor:
    """Мониторинг WAVE2 модели"""
    
    def __init__(self):
        self.performance_history = []
        self.alert_thresholds = {
            'accuracy': 0.7,
            'latency': 1.0,  # секунды
            'throughput': 100  # запросов в минуту
        }
    
    def monitor_prediction(self, prediction, actual, latency):
        """Мониторинг предсказания"""
        # Расчет точности
        accuracy = 1 if prediction == actual else 0
        
        # Сохранение метрик
        self.performance_history.append({
            'timestamp': datetime.now(),
            'accuracy': accuracy,
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
        
        # Проверка латентности
        avg_latency = np.mean([p['latency'] for p in recent_performance])
        if avg_latency > self.alert_thresholds['latency']:
            self._send_alert("High latency detected")
```

## Следующие шаги

После анализа WAVE2 переходите к:
- **[12_schr_levels_analysis.md](12_schr_levels_analysis.md)** - Анализ SCHR Levels
- **[13_schr_short3_analysis.md](13_schr_short3_analysis.md)** - Анализ SCHR SHORT3

## Ключевые выводы

1. **WAVE2** - мощный индикатор для анализа трендов
2. **Мультитаймфреймовый анализ** - разные параметры для разных таймфреймов
3. **Богатые признаки** - множество возможностей для создания признаков
4. **Высокая точность** - возможность достижения 95%+ точности
5. **Продакшн готовность** - полная интеграция с продакшн системами

---

**Важно:** WAVE2 требует тщательной настройки параметров для каждого таймфрейма и актива. Используйте оптимизацию для достижения максимальной производительности.
