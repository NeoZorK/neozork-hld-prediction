# 02. Основы робастных систем

**Цель:** Понять, что такое робастность в ML-системах и как создать систему, которая работает в любых рыночных условиях.

## Что такое робастность?

### Определение робастности

**Робастность** - это способность системы сохранять производительность при изменении входных данных, параметров или условий окружающей среды.

### Почему 90% торговых систем не робастны?

**Основные проблемы не робастных систем:**
1. **Переобучение** - система работает только на исторических данных
2. **Нестабильность** - малые изменения в данных приводят к большим изменениям в результатах
3. **Отсутствие адаптации** - система не адаптируется к изменяющимся условиям рынка
4. **Ложные сигналы** - система генерирует сигналы, которые не работают в реальности

### Характеристики робастной системы

#### 1. Стабильность
```python
# Не робастная система
def unstable_prediction(data):
    # Система, которая сильно зависит от конкретных значений
    if data['price'] > 100:
        return 'BUY'
    else:
        return 'SELL'

# Робастная система
def robust_prediction(data):
    # Система, которая учитывает контекст и тренды
    price_trend = data['price'].rolling(20).mean()
    volatility = data['price'].rolling(20).std()
    
    if price_trend.iloc[-1] > price_trend.iloc[-2] and volatility.iloc[-1] < threshold:
        return 'BUY'
    else:
        return 'HOLD'
```

#### 2. Адаптивность
```python
class AdaptiveSystem:
    def __init__(self):
        self.adaptation_rate = 0.01
        self.performance_threshold = 0.6
    
    def adapt(self, recent_performance):
        """Адаптация системы на основе недавней производительности"""
        if recent_performance < self.performance_threshold:
            # Увеличиваем адаптацию
            self.adaptation_rate *= 1.1
        else:
            # Уменьшаем адаптацию
            self.adaptation_rate *= 0.99
```

#### 3. Устойчивость к выбросам
```python
def robust_feature_extraction(data):
    """Извлечение признаков, устойчивых к выбросам"""
    
    # Использование медианы вместо среднего
    price_median = data['price'].rolling(20).median()
    
    # Использование квантилей
    price_q25 = data['price'].rolling(20).quantile(0.25)
    price_q75 = data['price'].rolling(20).quantile(0.75)
    
    # Устойчивые к выбросам признаки
    features = {
        'price_median': price_median,
        'price_iqr': price_q75 - price_q25,
        'price_robust_mean': price_median  # Медиана более устойчива
    }
    
    return features
```

## Типы робастности

### 1. Робастность к данным

**Проблема:** Система должна работать с разными типами данных и источниками.

```python
class DataRobustSystem:
    def __init__(self):
        self.data_validators = []
        self.data_cleaners = []
    
    def validate_data(self, data):
        """Валидация данных"""
        for validator in self.data_validators:
            if not validator.validate(data):
                return False
        return True
    
    def clean_data(self, data):
        """Очистка данных"""
        for cleaner in self.data_cleaners:
            data = cleaner.clean(data)
        return data
    
    def process_robust_data(self, data):
        """Обработка данных с проверкой робастности"""
        if not self.validate_data(data):
            raise ValueError("Data validation failed")
        
        cleaned_data = self.clean_data(data)
        return self.predict(cleaned_data)
```

### 2. Робастность к параметрам

**Проблема:** Система должна работать при изменении параметров.

```python
class ParameterRobustSystem:
    def __init__(self, base_params):
        self.base_params = base_params
        self.param_ranges = self._define_param_ranges()
    
    def _define_param_ranges(self):
        """Определение диапазонов параметров"""
        return {
            'learning_rate': (0.001, 0.1),
            'batch_size': (16, 256),
            'epochs': (10, 100)
        }
    
    def robust_training(self, data, param_variations=10):
        """Обучение с вариациями параметров"""
        best_model = None
        best_score = -float('inf')
        
        for _ in range(param_variations):
            # Случайные параметры в допустимых диапазонах
            params = self._generate_random_params()
            model = self._train_model(data, params)
            score = self._evaluate_model(model, data)
            
            if score > best_score:
                best_score = score
                best_model = model
        
        return best_model
```

### 3. Робастность к условиям

**Проблема:** Система должна работать в разных рыночных условиях.

```python
class MarketConditionRobustSystem:
    def __init__(self):
        self.condition_detectors = {
            'trending': self._detect_trending,
            'ranging': self._detect_ranging,
            'volatile': self._detect_volatile
        }
        self.condition_models = {}
    
    def detect_market_condition(self, data):
        """Определение рыночных условий"""
        for condition, detector in self.condition_detectors.items():
            if detector(data):
                return condition
        return 'unknown'
    
    def predict_robust(self, data):
        """Предсказание с учетом рыночных условий"""
        condition = self.detect_market_condition(data)
        
        if condition in self.condition_models:
            return self.condition_models[condition].predict(data)
        else:
            # Fallback к базовой модели
            return self.base_model.predict(data)
```

## Метрики робастности

### 1. Стабильность предсказаний

```python
def prediction_stability(model, data, n_iterations=100):
    """Измерение стабильности предсказаний"""
    predictions = []
    
    for _ in range(n_iterations):
        # Добавляем небольшой шум к данным
        noisy_data = add_noise(data, noise_level=0.01)
        pred = model.predict(noisy_data)
        predictions.append(pred)
    
    # Стабильность = 1 - стандартное отклонение
    stability = 1 - np.std(predictions)
    return stability
```

### 2. Устойчивость к выбросам

```python
def outlier_robustness(model, data, outlier_ratio=0.1):
    """Измерение устойчивости к выбросам"""
    # Создаем данные с выбросами
    outlier_data = add_outliers(data, ratio=outlier_ratio)
    
    # Предсказания на чистых данных
    clean_pred = model.predict(data)
    
    # Предсказания на данных с выбросами
    outlier_pred = model.predict(outlier_data)
    
    # Устойчивость = корреляция между предсказаниями
    robustness = np.corrcoef(clean_pred, outlier_pred)[0, 1]
    return robustness
```

### 3. Адаптивность

```python
def adaptability(model, data, change_point):
    """Измерение адаптивности системы"""
    # Данные до изменения
    before_data = data[:change_point]
    
    # Данные после изменения
    after_data = data[change_point:]
    
    # Производительность до изменения
    before_performance = model.evaluate(before_data)
    
    # Производительность после изменения
    after_performance = model.evaluate(after_data)
    
    # Адаптивность = сохранение производительности
    adaptability = after_performance / before_performance
    return adaptability
```

## Создание робастной системы

### 1. Архитектура робастной системы

```python
class RobustMLSystem:
    def __init__(self):
        self.data_validator = DataValidator()
        self.feature_engineer = RobustFeatureEngineer()
        self.model_ensemble = ModelEnsemble()
        self.performance_monitor = PerformanceMonitor()
        self.adaptation_engine = AdaptationEngine()
    
    def train(self, data):
        """Обучение робастной системы"""
        # 1. Валидация данных
        if not self.data_validator.validate(data):
            raise ValueError("Data validation failed")
        
        # 2. Инжиниринг признаков
        features = self.feature_engineer.create_robust_features(data)
        
        # 3. Обучение ансамбля моделей
        self.model_ensemble.train(features)
        
        # 4. Инициализация мониторинга
        self.performance_monitor.initialize(features)
        
        return self
    
    def predict(self, data):
        """Предсказание с робастностью"""
        # 1. Валидация входных данных
        if not self.data_validator.validate(data):
            return self._fallback_prediction()
        
        # 2. Создание признаков
        features = self.feature_engineer.create_robust_features(data)
        
        # 3. Предсказание ансамбля
        prediction = self.model_ensemble.predict(features)
        
        # 4. Мониторинг производительности
        self.performance_monitor.update(prediction, data)
        
        # 5. Адаптация при необходимости
        if self.performance_monitor.needs_adaptation():
            self.adaptation_engine.adapt(self.model_ensemble)
        
        return prediction
```

### 2. Робастная обработка данных

```python
class RobustDataProcessor:
    def __init__(self):
        self.outlier_detector = OutlierDetector()
        self.missing_handler = MissingValueHandler()
        self.normalizer = RobustNormalizer()
    
    def process(self, data):
        """Робастная обработка данных"""
        # 1. Обработка пропущенных значений
        data = self.missing_handler.handle(data)
        
        # 2. Обнаружение и обработка выбросов
        data = self.outlier_detector.handle(data)
        
        # 3. Нормализация
        data = self.normalizer.normalize(data)
        
        return data
    
    def validate_robustness(self, data):
        """Валидация робастности данных"""
        # Проверка стабильности
        stability = self._check_stability(data)
        
        # Проверка качества
        quality = self._check_quality(data)
        
        # Проверка консистентности
        consistency = self._check_consistency(data)
        
        return {
            'stability': stability,
            'quality': quality,
            'consistency': consistency,
            'overall': min(stability, quality, consistency)
        }
```

### 3. Робастное обучение модели

```python
class RobustModelTrainer:
    def __init__(self):
        self.cross_validator = RobustCrossValidator()
        self.regularizer = Regularizer()
        self.ensemble_builder = EnsembleBuilder()
    
    def train_robust(self, X, y):
        """Робастное обучение"""
        # 1. Кросс-валидация с робастными метриками
        cv_scores = self.cross_validator.cross_validate(X, y)
        
        # 2. Регуляризация для предотвращения переобучения
        regularized_models = []
        for alpha in [0.01, 0.1, 1.0, 10.0]:
            model = self._train_with_regularization(X, y, alpha)
            regularized_models.append(model)
        
        # 3. Создание ансамбля
        ensemble = self.ensemble_builder.build(regularized_models)
        
        # 4. Валидация робастности
        robustness_score = self._validate_robustness(ensemble, X, y)
        
        return ensemble, robustness_score
```

## Тестирование робастности

### 1. Стресс-тестирование

```python
def stress_test_system(system, data):
    """Стресс-тестирование системы"""
    results = {}
    
    # Тест 1: Добавление шума
    noise_levels = [0.01, 0.05, 0.1, 0.2]
    for noise in noise_levels:
        noisy_data = add_noise(data, noise)
        performance = system.evaluate(noisy_data)
        results[f'noise_{noise}'] = performance
    
    # Тест 2: Удаление данных
    missing_ratios = [0.1, 0.2, 0.3, 0.5]
    for ratio in missing_ratios:
        incomplete_data = remove_data(data, ratio)
        performance = system.evaluate(incomplete_data)
        results[f'missing_{ratio}'] = performance
    
    # Тест 3: Изменение распределения
    distribution_shifts = ['normal', 'uniform', 'exponential']
    for dist in distribution_shifts:
        shifted_data = change_distribution(data, dist)
        performance = system.evaluate(shifted_data)
        results[f'distribution_{dist}'] = performance
    
    return results
```

### 2. Тест на разных рыночных условиях

```python
def market_condition_test(system, data):
    """Тест на разных рыночных условиях"""
    conditions = {
        'bull_market': filter_bull_market(data),
        'bear_market': filter_bear_market(data),
        'sideways_market': filter_sideways_market(data),
        'volatile_market': filter_volatile_market(data)
    }
    
    results = {}
    for condition, condition_data in conditions.items():
        performance = system.evaluate(condition_data)
        results[condition] = performance
    
    return results
```

## Мониторинг робастности

### 1. Система мониторинга

```python
class RobustnessMonitor:
    def __init__(self):
        self.metrics = {}
        self.thresholds = {
            'stability': 0.8,
            'accuracy': 0.7,
            'consistency': 0.9
        }
    
    def monitor(self, predictions, actual):
        """Мониторинг робастности"""
        # Стабильность
        stability = self._calculate_stability(predictions)
        
        # Точность
        accuracy = self._calculate_accuracy(predictions, actual)
        
        # Консистентность
        consistency = self._calculate_consistency(predictions)
        
        # Обновление метрик
        self.metrics.update({
            'stability': stability,
            'accuracy': accuracy,
            'consistency': consistency,
            'timestamp': datetime.now()
        })
        
        # Проверка порогов
        alerts = self._check_thresholds()
        
        return {
            'metrics': self.metrics,
            'alerts': alerts
        }
```

### 2. Автоматическая адаптация

```python
class AutoAdaptation:
    def __init__(self, system):
        self.system = system
        self.adaptation_history = []
        self.performance_threshold = 0.7
    
    def check_adaptation_needed(self, recent_performance):
        """Проверка необходимости адаптации"""
        if recent_performance < self.performance_threshold:
            return True
        return False
    
    def adapt(self, data):
        """Автоматическая адаптация"""
        # 1. Анализ производительности
        performance_analysis = self._analyze_performance()
        
        # 2. Определение типа адаптации
        adaptation_type = self._determine_adaptation_type(performance_analysis)
        
        # 3. Применение адаптации
        if adaptation_type == 'retrain':
            self.system.retrain(data)
        elif adaptation_type == 'recalibrate':
            self.system.recalibrate(data)
        elif adaptation_type == 'ensemble_update':
            self.system.update_ensemble(data)
        
        # 4. Запись истории
        self.adaptation_history.append({
            'type': adaptation_type,
            'timestamp': datetime.now(),
            'performance': recent_performance
        })
```

## Практические рекомендации

### 1. Принципы создания робастных систем

1. **Модульность** - система должна состоять из независимых модулей
2. **Валидация** - каждый компонент должен быть валидирован
3. **Мониторинг** - постоянный мониторинг производительности
4. **Адаптация** - способность к самообучению и адаптации
5. **Резервирование** - наличие fallback механизмов

### 2. Избегание переобучения

```python
def prevent_overfitting(model, data):
    """Предотвращение переобучения"""
    # 1. Регуляризация
    model.add_regularization()
    
    # 2. Ранняя остановка
    model.set_early_stopping()
    
    # 3. Dropout
    model.add_dropout()
    
    # 4. Кросс-валидация
    cv_scores = cross_validate(model, data)
    
    return model
```

### 3. Обеспечение стабильности

```python
def ensure_stability(system, data):
    """Обеспечение стабильности системы"""
    # 1. Ансамблирование
    ensemble = create_ensemble(system)
    
    # 2. Бутстрап
    bootstrap_models = bootstrap_training(system, data)
    
    # 3. Бэггинг
    bagged_models = bagging_training(system, data)
    
    return ensemble
```

## Следующие шаги

После понимания основ робастности переходите к:
- **[03_data_preparation.md](03_data_preparation.md)** - Подготовка и очистка данных
- **[04_feature_engineering.md](04_feature_engineering.md)** - Создание признаков

## Ключевые выводы

1. **Робастность** - это способность системы работать в любых условиях
2. **Стабильность** - система должна давать стабильные результаты
3. **Адаптивность** - система должна адаптироваться к изменениям
4. **Мониторинг** - постоянный контроль производительности
5. **Тестирование** - всестороннее тестирование на разных условиях

---

**Важно:** Робастность - это не просто техническая характеристика, это философия создания систем, которые работают в реальном мире.
