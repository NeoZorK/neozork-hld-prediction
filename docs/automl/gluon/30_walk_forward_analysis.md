# Углубленное описание методик Walk-Forward анализа

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему Walk-Forward анализ - золотой стандарт валидации

**Почему Walk-Forward анализ считается самым реалистичным методом валидации?** Потому что он имитирует реальную торговлю - модель постоянно переобучается на новых данных и делает предсказания на будущее. Это единственный способ избежать "утечки данных из будущего".

### Что дает Walk-Forward анализ?
- **Реалистичность**: Имитирует реальную торговлю
- **Адаптивность**: Модель адаптируется к изменяющимся условиям
- **Стабильность**: Проверяет стабильность стратегии во времени
- **Робастность**: Выявляет слабые места стратегии

### Что происходит без Walk-Forward анализа?
- **Переобучение**: Модель запоминает исторические данные
- **Нестабильность**: Стратегия работает нестабильно во времени
- **Ложная уверенность**: Завышенные ожидания от стратегии
- **Реальные потери**: Стратегия не работает в реальной торговле

## Теоретические основы Walk-Forward анализа

### Математические принципы

**Walk-Forward как скользящее окно:**

```
For t = train_window to T - test_window:
    train_data = data[t-train_window:t]
    test_data = data[t:t+test_window]
    
    model.fit(train_data)
    predictions = model.predict(test_data)
    
    performance[t] = evaluate(predictions, test_data)
```

Где:
- `train_window` - размер окна обучения
- `test_window` - размер окна тестирования
- `T` - общая длина данных
- `performance[t]` - производительность на периоде t

**Критерии качества Walk-Forward:**

1. **Стабильность**: Var(performance) < threshold
2. **Тренд**: performance не ухудшается со временем
3. **Адаптивность**: модель адаптируется к новым условиям
4. **Робастность**: результаты стабильны на разных периодах

### Типы Walk-Forward анализа

**1. Фиксированное окно (Fixed Window)**
- Постоянный размер окна обучения
- Простой в реализации
- Может устаревать

**2. Расширяющееся окно (Expanding Window)**
- Окно обучения постоянно растет
- Использует всю доступную историю
- Может быть медленным

**3. Скользящее окно (Rolling Window)**
- Окно обучения сдвигается
- Баланс между историей и актуальностью
- Наиболее популярный

**4. Адаптивное окно (Adaptive Window)**
- Размер окна адаптируется к условиям
- Сложный в реализации
- Наиболее гибкий

## Продвинутые методики Walk-Forward анализа

### 1. Базовый Walk-Forward анализ

**Простая реализация:**

```python
def walk_forward_analysis(data, model, train_window=252, test_window=30, step=30):
    """Базовый Walk-Forward анализ"""
    results = []
    
    for i in range(train_window, len(data) - test_window, step):
        # Обучающие данные
        train_data = data[i-train_window:i]
        
        # Тестовые данные
        test_data = data[i:i+test_window]
        
        # Обучение модели
        model.fit(train_data)
        
        # Предсказания
        predictions = model.predict(test_data)
        
        # Оценка качества
        returns = test_data['returns']
        strategy_returns = predictions * returns
        
        # Метрики
        sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
        max_drawdown = calculate_max_drawdown(strategy_returns)
        total_return = strategy_returns.sum()
        
        results.append({
            'start_date': train_data.index[0],
            'end_date': train_data.index[-1],
            'test_start': test_data.index[0],
            'test_end': test_data.index[-1],
            'sharpe': sharpe,
            'max_drawdown': max_drawdown,
            'total_return': total_return,
            'predictions': predictions
        })
    
    return pd.DataFrame(results)

# Пример использования
wf_results = walk_forward_analysis(data, model, train_window=252, test_window=30, step=30)
```

**Расширяющееся окно:**

```python
def expanding_window_analysis(data, model, initial_train_window=252, test_window=30, step=30):
    """Walk-Forward анализ с расширяющимся окном"""
    results = []
    
    for i in range(initial_train_window, len(data) - test_window, step):
        # Обучающие данные (расширяющееся окно)
        train_data = data[:i]
        
        # Тестовые данные
        test_data = data[i:i+test_window]
        
        # Обучение модели
        model.fit(train_data)
        
        # Предсказания
        predictions = model.predict(test_data)
        
        # Оценка качества
        returns = test_data['returns']
        strategy_returns = predictions * returns
        
        # Метрики
        sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
        max_drawdown = calculate_max_drawdown(strategy_returns)
        total_return = strategy_returns.sum()
        
        results.append({
            'train_start': train_data.index[0],
            'train_end': train_data.index[-1],
            'test_start': test_data.index[0],
            'test_end': test_data.index[-1],
            'train_size': len(train_data),
            'sharpe': sharpe,
            'max_drawdown': max_drawdown,
            'total_return': total_return
        })
    
    return pd.DataFrame(results)

# Пример использования
expanding_results = expanding_window_analysis(data, model, initial_train_window=252, test_window=30)
```

### 2. Адаптивный Walk-Forward анализ

**Адаптация размера окна:**

```python
def adaptive_window_analysis(data, model, min_window=100, max_window=500, 
                           test_window=30, step=30, stability_threshold=0.1):
    """Walk-Forward анализ с адаптивным окном"""
    results = []
    current_window = min_window
    
    for i in range(min_window, len(data) - test_window, step):
        # Обучающие данные
        train_data = data[i-current_window:i]
        
        # Тестовые данные
        test_data = data[i:i+test_window]
        
        # Обучение модели
        model.fit(train_data)
        
        # Предсказания
        predictions = model.predict(test_data)
        
        # Оценка качества
        returns = test_data['returns']
        strategy_returns = predictions * returns
        
        # Метрики
        sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
        max_drawdown = calculate_max_drawdown(strategy_returns)
        total_return = strategy_returns.sum()
        
        # Адаптация размера окна
        if len(results) > 0:
            recent_sharpe = results[-1]['sharpe']
            current_sharpe = sharpe
            
            # Если производительность ухудшается, увеличиваем окно
            if current_sharpe < recent_sharpe * (1 - stability_threshold):
                current_window = min(current_window + 50, max_window)
            # Если производительность улучшается, уменьшаем окно
            elif current_sharpe > recent_sharpe * (1 + stability_threshold):
                current_window = max(current_window - 50, min_window)
        
        results.append({
            'train_start': train_data.index[0],
            'train_end': train_data.index[-1],
            'test_start': test_data.index[0],
            'test_end': test_data.index[-1],
            'window_size': current_window,
            'sharpe': sharpe,
            'max_drawdown': max_drawdown,
            'total_return': total_return
        })
    
    return pd.DataFrame(results)

# Пример использования
adaptive_results = adaptive_window_analysis(data, model, min_window=100, max_window=500)
```

**Адаптация на основе волатильности:**

```python
def volatility_adaptive_analysis(data, model, base_window=252, test_window=30, 
                                step=30, volatility_lookback=50):
    """Walk-Forward анализ с адаптацией к волатильности"""
    results = []
    
    for i in range(base_window, len(data) - test_window, step):
        # Расчет волатильности
        recent_volatility = data['returns'].iloc[i-volatility_lookback:i].std()
        long_term_volatility = data['returns'].iloc[:i].std()
        
        # Адаптация размера окна на основе волатильности
        volatility_ratio = recent_volatility / long_term_volatility
        
        if volatility_ratio > 1.5:  # Высокая волатильность
            window_size = int(base_window * 0.7)  # Меньше окно
        elif volatility_ratio < 0.7:  # Низкая волатильность
            window_size = int(base_window * 1.3)  # Больше окно
        else:
            window_size = base_window
        
        # Обучающие данные
        train_data = data[i-window_size:i]
        
        # Тестовые данные
        test_data = data[i:i+test_window]
        
        # Обучение модели
        model.fit(train_data)
        
        # Предсказания
        predictions = model.predict(test_data)
        
        # Оценка качества
        returns = test_data['returns']
        strategy_returns = predictions * returns
        
        # Метрики
        sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
        max_drawdown = calculate_max_drawdown(strategy_returns)
        total_return = strategy_returns.sum()
        
        results.append({
            'train_start': train_data.index[0],
            'train_end': train_data.index[-1],
            'test_start': test_data.index[0],
            'test_end': test_data.index[-1],
            'window_size': window_size,
            'volatility_ratio': volatility_ratio,
            'sharpe': sharpe,
            'max_drawdown': max_drawdown,
            'total_return': total_return
        })
    
    return pd.DataFrame(results)

# Пример использования
vol_adaptive_results = volatility_adaptive_analysis(data, model, base_window=252)
```

### 3. Многоуровневый Walk-Forward анализ

**Иерархический анализ:**

```python
def hierarchical_walk_forward(data, models, train_window=252, test_window=30, step=30):
    """Многоуровневый Walk-Forward анализ"""
    results = []
    
    for i in range(train_window, len(data) - test_window, step):
        # Обучающие данные
        train_data = data[i-train_window:i]
        
        # Тестовые данные
        test_data = data[i:i+test_window]
        
        # Обучение всех моделей
        model_predictions = {}
        for name, model in models.items():
            model.fit(train_data)
            model_predictions[name] = model.predict(test_data)
        
        # Комбинирование предсказаний
        combined_predictions = np.mean(list(model_predictions.values()), axis=0)
        
        # Оценка качества
        returns = test_data['returns']
        strategy_returns = combined_predictions * returns
        
        # Метрики
        sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
        max_drawdown = calculate_max_drawdown(strategy_returns)
        total_return = strategy_returns.sum()
        
        # Индивидуальные метрики моделей
        individual_metrics = {}
        for name, predictions in model_predictions.items():
            individual_returns = predictions * returns
            individual_metrics[name] = {
                'sharpe': individual_returns.mean() / individual_returns.std() * np.sqrt(252),
                'max_drawdown': calculate_max_drawdown(individual_returns),
                'total_return': individual_returns.sum()
            }
        
        results.append({
            'train_start': train_data.index[0],
            'train_end': train_data.index[-1],
            'test_start': test_data.index[0],
            'test_end': test_data.index[-1],
            'combined_sharpe': sharpe,
            'combined_max_drawdown': max_drawdown,
            'combined_total_return': total_return,
            'individual_metrics': individual_metrics
        })
    
    return pd.DataFrame(results)

# Пример использования
models = {
    'model1': RandomForestRegressor(),
    'model2': XGBRegressor(),
    'model3': LGBMRegressor()
}
hierarchical_results = hierarchical_walk_forward(data, models, train_window=252)
```

**Ансамблевый анализ:**

```python
def ensemble_walk_forward(data, base_models, ensemble_model, train_window=252, 
                         test_window=30, step=30):
    """Walk-Forward анализ с ансамблем"""
    results = []
    
    for i in range(train_window, len(data) - test_window, step):
        # Обучающие данные
        train_data = data[i-train_window:i]
        
        # Тестовые данные
        test_data = data[i:i+test_window]
        
        # Обучение базовых моделей
        base_predictions = []
        for name, model in base_models.items():
            model.fit(train_data)
            predictions = model.predict(test_data)
            base_predictions.append(predictions)
        
        # Создание мета-признаков
        meta_features = np.column_stack(base_predictions)
        
        # Обучение ансамблевой модели
        ensemble_model.fit(meta_features, test_data['returns'])
        
        # Предсказания ансамбля
        ensemble_predictions = ensemble_model.predict(meta_features)
        
        # Оценка качества
        returns = test_data['returns']
        strategy_returns = ensemble_predictions * returns
        
        # Метрики
        sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
        max_drawdown = calculate_max_drawdown(strategy_returns)
        total_return = strategy_returns.sum()
        
        results.append({
            'train_start': train_data.index[0],
            'train_end': train_data.index[-1],
            'test_start': test_data.index[0],
            'test_end': test_data.index[-1],
            'sharpe': sharpe,
            'max_drawdown': max_drawdown,
            'total_return': total_return,
            'base_predictions': base_predictions,
            'ensemble_predictions': ensemble_predictions
        })
    
    return pd.DataFrame(results)

# Пример использования
base_models = {
    'rf': RandomForestRegressor(),
    'xgb': XGBRegressor(),
    'lgb': LGBMRegressor()
}
ensemble_model = LinearRegression()
ensemble_results = ensemble_walk_forward(data, base_models, ensemble_model)
```

## Метрики качества Walk-Forward анализа

### 1. Временные метрики

**Стабильность во времени:**

```python
def calculate_temporal_stability(results):
    """Расчет стабильности во времени"""
    # Стабильность коэффициента Шарпа
    sharpe_std = results['sharpe'].std()
    sharpe_mean = results['sharpe'].mean()
    sharpe_stability = 1 / (sharpe_std / sharpe_mean) if sharpe_mean != 0 else 0
    
    # Тренд производительности
    sharpe_trend = np.polyfit(range(len(results)), results['sharpe'], 1)[0]
    
    # Волатильность производительности
    performance_volatility = results['sharpe'].rolling(5).std().mean()
    
    # Коэффициент стабильности
    stability_coefficient = 1 / performance_volatility if performance_volatility > 0 else 0
    
    return {
        'sharpe_stability': sharpe_stability,
        'sharpe_trend': sharpe_trend,
        'performance_volatility': performance_volatility,
        'stability_coefficient': stability_coefficient
    }

# Пример использования
temporal_metrics = calculate_temporal_stability(wf_results)
```

**Адаптивность:**

```python
def calculate_adaptability(results, lookback=5):
    """Расчет адаптивности модели"""
    # Скорость адаптации
    adaptation_speed = []
    for i in range(lookback, len(results)):
        recent_performance = results['sharpe'].iloc[i-lookback:i].mean()
        current_performance = results['sharpe'].iloc[i]
        adaptation = abs(current_performance - recent_performance) / recent_performance
        adaptation_speed.append(adaptation)
    
    # Средняя скорость адаптации
    mean_adaptation_speed = np.mean(adaptation_speed)
    
    # Волатильность адаптации
    adaptation_volatility = np.std(adaptation_speed)
    
    # Коэффициент адаптивности
    adaptability_coefficient = mean_adaptation_speed / adaptation_volatility if adaptation_volatility > 0 else 0
    
    return {
        'mean_adaptation_speed': mean_adaptation_speed,
        'adaptation_volatility': adaptation_volatility,
        'adaptability_coefficient': adaptability_coefficient
    }

# Пример использования
adaptability_metrics = calculate_adaptability(wf_results, lookback=5)
```

### 2. Статистические метрики

**Статистическая значимость:**

```python
def calculate_statistical_significance(results, confidence_level=0.95):
    """Расчет статистической значимости"""
    from scipy import stats
    
    # Тест на нормальность
    shapiro_stat, shapiro_pvalue = stats.shapiro(results['sharpe'])
    
    # Тест на стационарность
    adf_stat, adf_pvalue = stats.adfuller(results['sharpe'])
    
    # Доверительный интервал
    mean_sharpe = results['sharpe'].mean()
    std_sharpe = results['sharpe'].std()
    n = len(results)
    
    t_value = stats.t.ppf((1 + confidence_level) / 2, n - 1)
    margin_error = t_value * std_sharpe / np.sqrt(n)
    
    confidence_interval = (mean_sharpe - margin_error, mean_sharpe + margin_error)
    
    # Статистическая значимость
    is_significant = adf_pvalue < 0.05 and shapiro_pvalue > 0.05
    
    return {
        'shapiro_statistic': shapiro_stat,
        'shapiro_pvalue': shapiro_pvalue,
        'adf_statistic': adf_stat,
        'adf_pvalue': adf_pvalue,
        'confidence_interval': confidence_interval,
        'is_significant': is_significant
    }

# Пример использования
statistical_metrics = calculate_statistical_significance(wf_results)
```

**Корреляция с рыночными условиями:**

```python
def calculate_market_correlation(results, market_data):
    """Расчет корреляции с рыночными условиями"""
    # Корреляция с волатильностью рынка
    market_volatility = market_data['returns'].rolling(30).std()
    volatility_correlation = results['sharpe'].corr(market_volatility.iloc[results.index])
    
    # Корреляция с доходностью рынка
    market_returns = market_data['returns'].rolling(30).mean()
    returns_correlation = results['sharpe'].corr(market_returns.iloc[results.index])
    
    # Корреляция с трендом рынка
    market_trend = market_data['price'].rolling(30).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
    trend_correlation = results['sharpe'].corr(market_trend.iloc[results.index])
    
    return {
        'volatility_correlation': volatility_correlation,
        'returns_correlation': returns_correlation,
        'trend_correlation': trend_correlation
    }

# Пример использования
market_correlation = calculate_market_correlation(wf_results, market_data)
```

### 3. Экономические метрики

**Экономическая значимость:**

```python
def calculate_economic_significance(results, transaction_costs=0.001, 
                                  min_sharpe=1.0, max_drawdown=0.2):
    """Расчет экономической значимости"""
    # Учет транзакционных издержек
    net_returns = results['total_return'] - transaction_costs
    
    # Метрики
    mean_sharpe = results['sharpe'].mean()
    mean_max_drawdown = results['max_drawdown'].mean()
    success_rate = (results['sharpe'] > min_sharpe).mean()
    
    # Экономическая значимость
    economically_significant = (
        mean_sharpe >= min_sharpe and 
        abs(mean_max_drawdown) <= max_drawdown and
        success_rate >= 0.6
    )
    
    return {
        'mean_sharpe': mean_sharpe,
        'mean_max_drawdown': mean_max_drawdown,
        'success_rate': success_rate,
        'economically_significant': economically_significant
    }

# Пример использования
economic_metrics = calculate_economic_significance(wf_results, transaction_costs=0.001)
```

**Рентабельность:**

```python
def calculate_profitability(results, initial_capital=100000):
    """Расчет рентабельности"""
    # Кумулятивная доходность
    cumulative_returns = (1 + results['total_return']).cumprod()
    
    # Финальная стоимость портфеля
    final_value = initial_capital * cumulative_returns.iloc[-1]
    
    # Общая доходность
    total_return = (final_value - initial_capital) / initial_capital
    
    # Годовая доходность
    years = len(results) / 12  # Предполагаем месячные результаты
    annual_return = (final_value / initial_capital) ** (1 / years) - 1
    
    # Максимальная просадка
    max_drawdown = results['max_drawdown'].min()
    
    return {
        'final_value': final_value,
        'total_return': total_return,
        'annual_return': annual_return,
        'max_drawdown': max_drawdown
    }

# Пример использования
profitability_metrics = calculate_profitability(wf_results, initial_capital=100000)
```

## Визуализация Walk-Forward анализа

### 1. Временные графики

```python
def visualize_walk_forward_results(results, save_path=None):
    """Визуализация результатов Walk-Forward анализа"""
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Настройка стиля
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # Создание фигуры
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Коэффициент Шарпа во времени
    axes[0, 0].plot(results.index, results['sharpe'], marker='o')
    axes[0, 0].axhline(y=1.0, color='red', linestyle='--', label='Минимальный Sharpe')
    axes[0, 0].set_title('Коэффициент Шарпа во времени')
    axes[0, 0].set_xlabel('Период')
    axes[0, 0].set_ylabel('Коэффициент Шарпа')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # 2. Максимальная просадка во времени
    axes[0, 1].plot(results.index, results['max_drawdown'], marker='o', color='red')
    axes[0, 1].axhline(y=-0.2, color='red', linestyle='--', label='Максимальная просадка 20%')
    axes[0, 1].set_title('Максимальная просадка во времени')
    axes[0, 1].set_xlabel('Период')
    axes[0, 1].set_ylabel('Максимальная просадка')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # 3. Распределение коэффициента Шарпа
    axes[1, 0].hist(results['sharpe'], bins=20, alpha=0.7, edgecolor='black')
    axes[1, 0].axvline(results['sharpe'].mean(), color='red', linestyle='--', 
                      label=f'Среднее: {results["sharpe"].mean():.2f}')
    axes[1, 0].set_title('Распределение коэффициента Шарпа')
    axes[1, 0].set_xlabel('Коэффициент Шарпа')
    axes[1, 0].set_ylabel('Частота')
    axes[1, 0].legend()
    axes[1, 0].grid(True)
    
    # 4. Кумулятивная доходность
    cumulative_returns = (1 + results['total_return']).cumprod()
    axes[1, 1].plot(results.index, cumulative_returns, marker='o')
    axes[1, 1].set_title('Кумулятивная доходность')
    axes[1, 1].set_xlabel('Период')
    axes[1, 1].set_ylabel('Кумулятивная доходность')
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

# Пример использования
visualize_walk_forward_results(wf_results, save_path='walk_forward_results.png')
```

### 2. Тепловые карты

```python
def create_heatmap_analysis(results, save_path=None):
    """Создание тепловой карты анализа"""
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Создание матрицы корреляций
    correlation_matrix = results[['sharpe', 'max_drawdown', 'total_return']].corr()
    
    # Создание фигуры
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # 1. Тепловая карта корреляций
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, ax=axes[0])
    axes[0].set_title('Корреляционная матрица метрик')
    
    # 2. Тепловая карта производительности по периодам
    if 'window_size' in results.columns:
        pivot_table = results.pivot_table(values='sharpe', 
                                        index=results.index // 12,  # Годы
                                        columns=results.index % 12,  # Месяцы
                                        fill_value=0)
        sns.heatmap(pivot_table, annot=True, cmap='RdYlGn', center=1.0,
                    ax=axes[1])
        axes[1].set_title('Производительность по периодам')
        axes[1].set_xlabel('Месяц')
        axes[1].set_ylabel('Год')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

# Пример использования
create_heatmap_analysis(wf_results, save_path='walk_forward_heatmap.png')
```

## Автоматизация Walk-Forward анализа

### 1. Пайплайн Walk-Forward анализа

```python
class WalkForwardPipeline:
    """Пайплайн для автоматизации Walk-Forward анализа"""
    
    def __init__(self, data, model, metrics_calculator):
        self.data = data
        self.model = model
        self.metrics_calculator = metrics_calculator
        self.results = {}
    
    def run_fixed_window_analysis(self, train_window=252, test_window=30, step=30):
        """Анализ с фиксированным окном"""
        results = []
        
        for i in range(train_window, len(self.data) - test_window, step):
            # Обучающие данные
            train_data = self.data[i-train_window:i]
            
            # Тестовые данные
            test_data = self.data[i:i+test_window]
            
            # Обучение модели
            self.model.fit(train_data)
            
            # Предсказания
            predictions = self.model.predict(test_data)
            
            # Расчет метрик
            returns = test_data['returns']
            strategy_returns = predictions * returns
            
            metrics = self.metrics_calculator.calculate(strategy_returns)
            metrics.update({
                'train_start': train_data.index[0],
                'train_end': train_data.index[-1],
                'test_start': test_data.index[0],
                'test_end': test_data.index[-1],
                'window_size': train_window
            })
            
            results.append(metrics)
        
        self.results['fixed_window'] = pd.DataFrame(results)
        return self.results['fixed_window']
    
    def run_expanding_window_analysis(self, initial_train_window=252, test_window=30, step=30):
        """Анализ с расширяющимся окном"""
        results = []
        
        for i in range(initial_train_window, len(self.data) - test_window, step):
            # Обучающие данные (расширяющееся окно)
            train_data = self.data[:i]
            
            # Тестовые данные
            test_data = self.data[i:i+test_window]
            
            # Обучение модели
            self.model.fit(train_data)
            
            # Предсказания
            predictions = self.model.predict(test_data)
            
            # Расчет метрик
            returns = test_data['returns']
            strategy_returns = predictions * returns
            
            metrics = self.metrics_calculator.calculate(strategy_returns)
            metrics.update({
                'train_start': train_data.index[0],
                'train_end': train_data.index[-1],
                'test_start': test_data.index[0],
                'test_end': test_data.index[-1],
                'window_size': len(train_data)
            })
            
            results.append(metrics)
        
        self.results['expanding_window'] = pd.DataFrame(results)
        return self.results['expanding_window']
    
    def run_adaptive_window_analysis(self, min_window=100, max_window=500, 
                                   test_window=30, step=30):
        """Анализ с адаптивным окном"""
        results = []
        current_window = min_window
        
        for i in range(min_window, len(self.data) - test_window, step):
            # Обучающие данные
            train_data = self.data[i-current_window:i]
            
            # Тестовые данные
            test_data = self.data[i:i+test_window]
            
            # Обучение модели
            self.model.fit(train_data)
            
            # Предсказания
            predictions = self.model.predict(test_data)
            
            # Расчет метрик
            returns = test_data['returns']
            strategy_returns = predictions * returns
            
            metrics = self.metrics_calculator.calculate(strategy_returns)
            metrics.update({
                'train_start': train_data.index[0],
                'train_end': train_data.index[-1],
                'test_start': test_data.index[0],
                'test_end': test_data.index[-1],
                'window_size': current_window
            })
            
            # Адаптация размера окна
            if len(results) > 0:
                recent_sharpe = results[-1]['sharpe']
                current_sharpe = metrics['sharpe']
                
                if current_sharpe < recent_sharpe * 0.9:
                    current_window = min(current_window + 50, max_window)
                elif current_sharpe > recent_sharpe * 1.1:
                    current_window = max(current_window - 50, min_window)
            
            results.append(metrics)
        
        self.results['adaptive_window'] = pd.DataFrame(results)
        return self.results['adaptive_window']
    
    def generate_comprehensive_report(self):
        """Генерация комплексного отчета"""
        report = {
            'summary': {},
            'detailed_results': self.results,
            'recommendations': []
        }
        
        # Анализ каждого метода
        for method, results in self.results.items():
            if isinstance(results, pd.DataFrame):
                # Базовые метрики
                mean_sharpe = results['sharpe'].mean()
                std_sharpe = results['sharpe'].std()
                mean_max_drawdown = results['max_drawdown'].mean()
                success_rate = (results['sharpe'] > 1.0).mean()
                
                # Стабильность
                sharpe_stability = 1 / (std_sharpe / mean_sharpe) if mean_sharpe != 0 else 0
                
                # Тренд
                sharpe_trend = np.polyfit(range(len(results)), results['sharpe'], 1)[0]
                
                report['summary'][method] = {
                    'mean_sharpe': mean_sharpe,
                    'std_sharpe': std_sharpe,
                    'mean_max_drawdown': mean_max_drawdown,
                    'success_rate': success_rate,
                    'sharpe_stability': sharpe_stability,
                    'sharpe_trend': sharpe_trend
                }
                
                # Рекомендации
                if mean_sharpe > 1.5 and success_rate > 0.7:
                    report['recommendations'].append(f"{method}: Отличная производительность")
                elif mean_sharpe > 1.0 and success_rate > 0.5:
                    report['recommendations'].append(f"{method}: Хорошая производительность")
                else:
                    report['recommendations'].append(f"{method}: Требует улучшения")
        
        return report

# Пример использования
pipeline = WalkForwardPipeline(data, model, metrics_calculator)
pipeline.run_fixed_window_analysis()
pipeline.run_expanding_window_analysis()
pipeline.run_adaptive_window_analysis()
report = pipeline.generate_comprehensive_report()
```

## Заключение

Walk-Forward анализ - это золотой стандарт валидации ML-стратегий. Он позволяет:

1. **Имитировать реальную торговлю** - модель постоянно переобучается
2. **Проверять адаптивность** - модель должна работать в изменяющихся условиях
3. **Оценивать стабильность** - результаты должны быть стабильными во времени
4. **Выявлять переобучение** - модель не должна запоминать исторические данные

### Ключевые принципы:

1. **Реалистичность** - используйте реалистичные параметры
2. **Стабильность** - проверяйте стабильность результатов
3. **Адаптивность** - модель должна адаптироваться к новым условиям
4. **Статистическая значимость** - проверяйте значимость результатов
5. **Экономическая значимость** - учитывайте транзакционные издержки

### Следующие шаги:

После освоения Walk-Forward анализа переходите к:
- [Monte Carlo симуляциям](./29_monte_carlo_simulations.md)
- [Управлению портфолио](./30_portfolio_management.md)
