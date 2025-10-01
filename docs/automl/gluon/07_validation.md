# Валидация моделей в AutoML Gluon

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему валидация критически важна

**Почему 70% ML-проектов терпят неудачу в продакшене из-за плохой валидации?** Потому что валидация - это единственный способ убедиться, что ваша модель действительно работает. Это как тест-драйв автомобиля перед покупкой.

### Что происходит без правильной валидации?
- **Ложная уверенность**: Модель кажется хорошей, но проваливается на новых данных
- **Переобучение**: Модель запоминает тренировочные данные вместо изучения паттернов
- **Неправильные решения**: Выбираете плохую модель вместо хорошей
- **Бизнес-провалы**: Модель не работает в реальных условиях

### Что дает правильная валидация?
- **Реальная оценка**: Вы точно знаете, как модель поведет себя на новых данных
- **Предотвращение переобучения**: Модель учится обобщать, а не запоминать
- **Правильный выбор**: Выбираете лучшую модель для задачи
- **Уверенность в продакшене**: Модель действительно будет работать

## Введение в валидацию

<img src="images/optimized/validation_methods.png" alt="Методы валидации" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 4: Методы валидации в AutoML Gluon*

<img src="images/optimized/walk_forward_analysis.png" alt="Walk-Forward анализ" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 4.1: Walk-Forward валидация - схема, производительность, выбор параметров*

**Почему валидация - это не просто "проверка модели"?** Это процесс, который определяет, готова ли ваша модель к реальному миру. Представьте, что вы готовите пилота к полету - валидация это симулятор, который показывает, как он поведет себя в реальных условиях.

Валидация - это критически важный процесс для оценки качества ML-моделей и предотвращения переобучения. В AutoML Gluon доступны различные методы валидации для разных типов задач.

## Типы валидации

**Почему AutoML Gluon предлагает разные типы валидации?** Потому что разные задачи требуют разных подходов. Это как разные виды экзаменов для разных предметов.

### 1. Holdout валидация

**Почему Holdout валидация - самый простой и популярный метод?** Потому что она интуитивно понятна: вы просто разделяете данные на две части - одну для обучения, другую для проверки. Это как экзамен в школе - вы учитесь по учебнику, а экзамен сдаете по новым задачам.

**Преимущества Holdout валидации:**
- **Простота**: Легко понять и реализовать
- **Скорость**: Быстро выполняется
- **Эффективность**: Подходит для больших датасетов
- **Интуитивность**: Понятно заинтересованным сторонам

**Недостатки Holdout валидации:**
- **Нестабильность**: Результат зависит от случайного разделения
- **Неэффективность**: 20% данных не участвуют в обучении
- **Случайность**: Плохое разделение может исказить результаты

```python
from autogluon.tabular import TabularPredictor

# Простая holdout валидация
predictor = TabularPredictor(label='target')
predictor.fit(
    train_data,
    holdout_frac=0.2  # 20% данных для валидации
)
```

**Почему 20% для валидации?** Это компромисс между достаточным количеством данных для обучения и достаточным количеством для валидации.

### 2. K-Fold кросс-валидация

**Почему K-Fold кросс-валидация более надежна, чем Holdout?** Потому что она использует ВСЕ данные и для обучения, и для валидации. Это как сдать 5 экзаменов вместо одного - результат будет более точным.

**Как работает K-Fold кросс-валидация:**
1. **Разделение на K частей**: Данные делятся на K равных частей (обычно K=5 или K=10)
2. **K итераций**: В каждой итерации одна часть используется для валидации, остальные K-1 для обучения
3. **Обучение модели**: Модель обучается на K-1 частях
4. **Тестирование**: Модель тестируется на оставшейся части
5. **Усреднение результатов**: Итоговая оценка - среднее по всем K итерациям

**Преимущества K-Fold валидации:**
- **Использование всех данных**: Каждая точка данных участвует и в обучении, и в валидации
- **Стабильность**: Результат не зависит от случайного разделения
- **Оценка дисперсии**: Показывает, насколько стабильна модель
- **Надежность**: Более точная оценка качества модели

**Недостатки K-Fold валидации:**
- **Время**: Выполняется в K раз дольше
- **Сложность**: Требует больше вычислительных ресурсов
- **Память**: Нужно хранить K моделей

```python
# K-fold кросс-валидация
predictor.fit(
    train_data,
    num_bag_folds=5,  # 5-fold CV
    num_bag_sets=1
)
```

**Почему обычно используют 5 или 10 фолдов?** Потому что это оптимальный баланс между точностью и скоростью.

### 3. Стратифицированная валидация

**Почему стратифицированная валидация критически важна для несбалансированных данных?** Потому что обычная валидация может дать искаженные результаты, когда один класс представлен в 100 раз больше другого. Это как оценивать качество врача только по здоровым пациентам.

**Проблема несбалансированных данных:**
- **Медицинская диагностика**: 99% здоровых, 1% больных
- **Обнаружение мошенничества**: 99.9% легальных транзакций, 0.1% мошеннических
- **Спам-фильтры**: 90% обычных писем, 10% спама

**Как работает стратификация:**
1. **Анализ распределения**: AutoML Gluon анализирует пропорции классов
2. **Сохранение пропорций**: В каждом фолде сохраняется исходное распределение
3. **Сбалансированная оценка**: Модель оценивается на репрезентативных данных
4. **Корректные метрики**: Получаем точные оценки для всех классов

**Когда использовать стратификацию:**
- **Использовать**: Когда классы несбалансированы (соотношение > 10:1)
- **Использовать**: Когда важны все классы (медицина, безопасность)
- **Не использовать**: Когда данные сбалансированы
- **Не использовать**: Когда важны только мажоритарные классы

```python
# Стратифицированная валидация для несбалансированных данных
predictor.fit(
    train_data,
    num_bag_folds=5,
    num_bag_sets=1,
    stratify=True  # Сохранять пропорции классов в каждом фолде
)
```

**Почему стратификация нужна не всегда?** Потому что она добавляет сложность, но не всегда необходима.
```

## Backtest валидация

### Временная валидация для временных рядов

```python
from sklearn.model_selection import TimeSeriesSplit
import pandas as pd
import numpy as np

def time_series_backtest(data, target_col, n_splits=5):
    """Backtest валидация для временных рядов"""
    
    # Сортировка по времени
    data = data.sort_values('timestamp')
    
    # Создание временных фолдов
    tscv = TimeSeriesSplit(n_splits=n_splits)
    
    results = []
    
    for fold, (train_idx, val_idx) in enumerate(tscv.split(data)):
        print(f"Fold {fold + 1}/{n_splits}")
        
        # Разделение данных
        train_fold = data.iloc[train_idx]
        val_fold = data.iloc[val_idx]
        
        # Обучение модели
        predictor = TabularPredictor(label=target_col)
        predictor.fit(train_fold, time_limit=300)
        
        # Предсказания
        predictions = predictor.predict(val_fold)
        
        # Оценка качества
        performance = predictor.evaluate(val_fold)
        
        results.append({
            'fold': fold + 1,
            'performance': performance,
            'predictions': predictions
        })
    
    return results

# Использование
backtest_results = time_series_backtest(data, 'target', n_splits=5)
```

### Расширенный backtest

```python
def advanced_backtest(data, target_col, window_size=1000, step_size=100):
    """Расширенный backtest с скользящим окном"""
    
    results = []
    n_samples = len(data)
    
    for start in range(0, n_samples - window_size, step_size):
        end = start + window_size
        
        # Разделение на train/validation
        train_data = data.iloc[start:end-100]
        val_data = data.iloc[end-100:end]
        
        # Обучение модели
        predictor = TabularPredictor(label=target_col)
        predictor.fit(train_data, time_limit=300)
        
        # Предсказания
        predictions = predictor.predict(val_data)
        
        # Оценка качества
        performance = predictor.evaluate(val_data)
        
        results.append({
            'start': start,
            'end': end,
            'performance': performance,
            'predictions': predictions
        })
    
    return results
```

## Walk-Forward валидация

### Базовая Walk-Forward валидация

```python
def walk_forward_validation(data, target_col, train_size=1000, test_size=100):
    """Walk-Forward валидация"""
    
    results = []
    n_samples = len(data)
    
    for i in range(train_size, n_samples - test_size, test_size):
        # Обучающая выборка
        train_data = data.iloc[i-train_size:i]
        
        # Тестовая выборка
        test_data = data.iloc[i:i+test_size]
        
        # Обучение модели
        predictor = TabularPredictor(label=target_col)
        predictor.fit(train_data, time_limit=300)
        
        # Предсказания
        predictions = predictor.predict(test_data)
        
        # Оценка качества
        performance = predictor.evaluate(test_data)
        
        results.append({
            'train_start': i-train_size,
            'train_end': i,
            'test_start': i,
            'test_end': i+test_size,
            'performance': performance,
            'predictions': predictions
        })
    
    return results

# Использование
wf_results = walk_forward_validation(data, 'target', train_size=1000, test_size=100)
```

### Адаптивная Walk-Forward валидация

```python
def adaptive_walk_forward(data, target_col, min_train_size=500, max_train_size=2000):
    """Адаптивная Walk-Forward валидация с изменяющимся размером окна"""
    
    results = []
    n_samples = len(data)
    current_train_size = min_train_size
    
    for i in range(min_train_size, n_samples - 100, 100):
        # Адаптация размера обучающей выборки
        if i > n_samples // 2:
            current_train_size = min(max_train_size, current_train_size + 100)
        
        # Обучающая выборка
        train_data = data.iloc[i-current_train_size:i]
        
        # Тестовая выборка
        test_data = data.iloc[i:i+100]
        
        # Обучение модели
        predictor = TabularPredictor(label=target_col)
        predictor.fit(train_data, time_limit=300)
        
        # Предсказания
        predictions = predictor.predict(test_data)
        
        # Оценка качества
        performance = predictor.evaluate(test_data)
        
        results.append({
            'train_size': current_train_size,
            'performance': performance,
            'predictions': predictions
        })
    
    return results
```

## Monte Carlo валидация

### Базовый Monte Carlo

```python
def monte_carlo_validation(data, target_col, n_iterations=100, train_frac=0.8):
    """Monte Carlo валидация с случайным разделением данных"""
    
    results = []
    
    for iteration in range(n_iterations):
        # Случайное разделение данных
        train_data = data.sample(frac=train_frac, random_state=iteration)
        test_data = data.drop(train_data.index)
        
        # Обучение модели
        predictor = TabularPredictor(label=target_col)
        predictor.fit(train_data, time_limit=300)
        
        # Предсказания
        predictions = predictor.predict(test_data)
        
        # Оценка качества
        performance = predictor.evaluate(test_data)
        
        results.append({
            'iteration': iteration,
            'performance': performance,
            'predictions': predictions
        })
    
    return results

# Использование
mc_results = monte_carlo_validation(data, 'target', n_iterations=100)
```

### Bootstrap валидация

```python
def bootstrap_validation(data, target_col, n_bootstrap=100):
    """Bootstrap валидация"""
    
    results = []
    n_samples = len(data)
    
    for i in range(n_bootstrap):
        # Bootstrap выборка
        bootstrap_indices = np.random.choice(n_samples, size=n_samples, replace=True)
        bootstrap_data = data.iloc[bootstrap_indices]
        
        # Out-of-bag выборка
        oob_indices = np.setdiff1d(np.arange(n_samples), np.unique(bootstrap_indices))
        oob_data = data.iloc[oob_indices]
        
        if len(oob_data) == 0:
            continue
        
        # Обучение модели
        predictor = TabularPredictor(label=target_col)
        predictor.fit(bootstrap_data, time_limit=300)
        
        # Предсказания на OOB данных
        predictions = predictor.predict(oob_data)
        
        # Оценка качества
        performance = predictor.evaluate(oob_data)
        
        results.append({
            'bootstrap': i,
            'performance': performance,
            'predictions': predictions
        })
    
    return results
```

## Комбинированная валидация

### Ensemble валидация

```python
def ensemble_validation(data, target_col, validation_methods=['holdout', 'kfold', 'monte_carlo']):
    """Комбинированная валидация с несколькими методами"""
    
    results = {}
    
    # Holdout валидация
    if 'holdout' in validation_methods:
        predictor = TabularPredictor(label=target_col)
        predictor.fit(data, holdout_frac=0.2)
        results['holdout'] = predictor.evaluate(data)
    
    # K-fold валидация
    if 'kfold' in validation_methods:
        predictor = TabularPredictor(label=target_col)
        predictor.fit(data, num_bag_folds=5, num_bag_sets=1)
        results['kfold'] = predictor.evaluate(data)
    
    # Monte Carlo валидация
    if 'monte_carlo' in validation_methods:
        mc_results = monte_carlo_validation(data, target_col, n_iterations=50)
        results['monte_carlo'] = mc_results
    
    return results
```

## Валидация для финансовых данных

### Финансовая валидация

```python
def financial_validation(data, target_col, lookback_window=252, forward_window=21):
    """Специализированная валидация для финансовых данных"""
    
    results = []
    n_samples = len(data)
    
    for i in range(lookback_window, n_samples - forward_window, forward_window):
        # Обучающая выборка (lookback_window дней)
        train_data = data.iloc[i-lookback_window:i]
        
        # Тестовая выборка (forward_window дней)
        test_data = data.iloc[i:i+forward_window]
        
        # Обучение модели
        predictor = TabularPredictor(label=target_col)
        predictor.fit(train_data, time_limit=300)
        
        # Предсказания
        predictions = predictor.predict(test_data)
        
        # Финансовые метрики
        returns = test_data[target_col].pct_change().dropna()
        predicted_returns = predictions.pct_change().dropna()
        
        # Sharpe Ratio
        sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252)
        
        # Maximum Drawdown
        cumulative_returns = (1 + returns).cumprod()
        peak = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()
        
        results.append({
            'start_date': test_data.index[0],
            'end_date': test_data.index[-1],
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'predictions': predictions
        })
    
    return results
```

## Анализ результатов валидации

### Статистический анализ

```python
def analyze_validation_results(results):
    """Анализ результатов валидации"""
    
    # Извлечение метрик
    metrics = []
    for result in results:
        if 'performance' in result:
            metrics.append(result['performance'])
    
    # Статистический анализ
    analysis = {}
    
    for metric in metrics[0].keys():
        values = [m[metric] for m in metrics]
        analysis[metric] = {
            'mean': np.mean(values),
            'std': np.std(values),
            'min': np.min(values),
            'max': np.max(values),
            'median': np.median(values),
            'q25': np.percentile(values, 25),
            'q75': np.percentile(values, 75)
        }
    
    return analysis

# Использование
analysis = analyze_validation_results(backtest_results)
print("Validation Analysis:")
for metric, stats in analysis.items():
    print(f"{metric}: {stats['mean']:.4f} ± {stats['std']:.4f}")
```

### Визуализация результатов

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_validation_results(results, metric='accuracy'):
    """Визуализация результатов валидации"""
    
    # Извлечение метрик
    values = []
    for result in results:
        if 'performance' in result and metric in result['performance']:
            values.append(result['performance'][metric])
    
    # График
    plt.figure(figsize=(12, 8))
    
    # Временной ряд метрики
    plt.subplot(2, 2, 1)
    plt.plot(values)
    plt.title(f'{metric} over time')
    plt.xlabel('Fold/Iteration')
    plt.ylabel(metric)
    
    # Распределение метрики
    plt.subplot(2, 2, 2)
    plt.hist(values, bins=20, alpha=0.7)
    plt.title(f'Distribution of {metric}')
    plt.xlabel(metric)
    plt.ylabel('Frequency')
    
    # Box plot
    plt.subplot(2, 2, 3)
    plt.boxplot(values)
    plt.title(f'Box plot of {metric}')
    plt.ylabel(metric)
    
    # Статистики
    plt.subplot(2, 2, 4)
    stats_text = f"""
    Mean: {np.mean(values):.4f}
    Std: {np.std(values):.4f}
    Min: {np.min(values):.4f}
    Max: {np.max(values):.4f}
    """
    plt.text(0.1, 0.5, stats_text, transform=plt.gca().transAxes, fontsize=12)
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

# Использование
plot_validation_results(backtest_results, metric='accuracy')
```

## Практические примеры

### Полный пример валидации

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Создание данных
X, y = make_classification(
    n_samples=10000,
    n_features=20,
    n_informative=15,
    n_redundant=5,
    n_classes=2,
    random_state=42
)

data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
data['target'] = y

# Добавление временной метки
data['timestamp'] = pd.date_range('2020-01-01', periods=len(data), freq='D')
data = data.set_index('timestamp')

# Различные методы валидации
print("=== Holdout Validation ===")
predictor_holdout = TabularPredictor(label='target')
predictor_holdout.fit(data, holdout_frac=0.2, time_limit=300)
holdout_performance = predictor_holdout.evaluate(data)
print(f"Holdout Performance: {holdout_performance}")

print("\n=== K-Fold Validation ===")
predictor_kfold = TabularPredictor(label='target')
predictor_kfold.fit(data, num_bag_folds=5, num_bag_sets=1, time_limit=300)
kfold_performance = predictor_kfold.evaluate(data)
print(f"K-Fold Performance: {kfold_performance}")

print("\n=== Time Series Backtest ===")
backtest_results = time_series_backtest(data, 'target', n_splits=5)
backtest_analysis = analyze_validation_results(backtest_results)
print(f"Backtest Analysis: {backtest_analysis}")

print("\n=== Monte Carlo Validation ===")
mc_results = monte_carlo_validation(data, 'target', n_iterations=50)
mc_analysis = analyze_validation_results(mc_results)
print(f"Monte Carlo Analysis: {mc_analysis}")

# Визуализация результатов
plot_validation_results(backtest_results, metric='accuracy')
```

## Лучшие практики валидации

### Выбор метода валидации

```python
def choose_validation_method(data_type, problem_type, data_size):
    """Выбор оптимального метода валидации"""
    
    if data_type == 'time_series':
        return 'time_series_backtest'
    elif data_size < 1000:
        return 'kfold'
    elif data_size < 10000:
        return 'holdout'
    else:
        return 'monte_carlo'
```

### Настройка параметров валидации

```python
def optimize_validation_params(data, target_col):
    """Оптимизация параметров валидации"""
    
    # Определение оптимального количества фолдов
    n_samples = len(data)
    if n_samples < 100:
        n_folds = 3
    elif n_samples < 1000:
        n_folds = 5
    else:
        n_folds = 10
    
    # Определение размера holdout
    if n_samples < 1000:
        holdout_frac = 0.3
    else:
        holdout_frac = 0.2
    
    return {
        'n_folds': n_folds,
        'holdout_frac': holdout_frac,
        'n_monte_carlo': min(100, n_samples // 10)
    }
```

## Следующие шаги

После освоения методов валидации переходите к:
- [Продакшен деплою](./06_production.md)
- [Переобучению моделей](./07_retraining.md)
- [Лучшим практикам](./08_best_practices.md)
