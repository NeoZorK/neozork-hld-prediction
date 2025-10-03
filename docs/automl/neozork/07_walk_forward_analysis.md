# 07. 🔄 Walk-Forward анализ

**Цель:** Научиться проводить Walk-Forward анализ для проверки стабильности торговых стратегий.

## Что такое Walk-Forward анализ?

**Теория:** Walk-Forward анализ - это продвинутый метод тестирования торговых стратегий, который имитирует реальные условия торговли. В отличие от простого бэктестинга, он учитывает необходимость переобучения модели на новых данных, что делает его более реалистичным и надежным.

**Walk-Forward анализ** - это метод тестирования торговых стратегий, который имитирует реальную торговлю, где модель переобучается на новых данных по мере их поступления.

**Почему Walk-Forward анализ критичен для финансовых систем:**
- **Реалистичность:** Имитирует реальные условия торговли
- **Стабильность:** Проверяет, как стратегия работает на новых данных
- **Адаптивность:** Оценивает способность модели адаптироваться к изменениям
- **Робастность:** Выявляет проблемы, которые не видны в простом бэктестинге

### Зачем нужен Walk-Forward анализ?

**Теория:** Walk-Forward анализ решает фундаментальные проблемы традиционного бэктестинга, связанные с переобучением и нереалистичностью. Он обеспечивает более честную оценку производительности стратегии.

- **Реалистичность** - имитирует реальную торговлю
  - **Почему важно:** В реальной торговле модель должна переобучаться на новых данных
  - **Плюсы:** Более честная оценка производительности, реалистичные результаты
  - **Минусы:** Более сложная реализация, требует больше вычислительных ресурсов

- **Проверка стабильности** - как стратегия работает на новых данных
  - **Почему важно:** Стратегия должна работать стабильно на новых данных
  - **Плюсы:** Выявление проблем стабильности, оценка долгосрочной производительности
  - **Минусы:** Может показать худшие результаты, чем простой бэктестинг

- **Избежание переобучения** - предотвращает оптимизацию на исторических данных
  - **Почему важно:** Переобучение приводит к нереалистичным результатам
  - **Плюсы:** Более честная оценка, снижение рисков
  - **Минусы:** Может показать худшие результаты, требует больше данных

- **Оценка адаптивности** - как модель адаптируется к изменениям
  - **Почему важно:** Рынки постоянно меняются, модель должна адаптироваться
  - **Плюсы:** Оценка способности к адаптации, выявление проблем адаптации
  - **Минусы:** Сложность оценки адаптивности, необходимость метрик адаптивности

**Дополнительные преимущества Walk-Forward анализа:**
- **Временная структура:** Учитывает временную структуру данных
- **Деградация:** Выявляет деградацию производительности со временем
- **Рыночные условия:** Позволяет анализировать производительность в разных рыночных условиях
- **Параметрическая стабильность:** Оценивает стабильность параметров стратегии

## Принципы Walk-Forward анализа

**Теория:** Walk-Forward анализ основан на нескольких ключевых принципах, которые обеспечивают его эффективность и реалистичность. Понимание этих принципов критично для правильного проведения анализа.

### 1. Разделение данных

**Теория:** Правильное разделение данных является основой Walk-Forward анализа. Данные должны быть разделены на обучающие и тестовые периоды таким образом, чтобы имитировать реальные условия торговли.

**Почему правильное разделение данных важно:**
- **Временная структура:** Учитывает временную структуру финансовых данных
- **Реалистичность:** Имитирует реальные условия торговли
- **Предотвращение утечек:** Избегает использования будущей информации
- **Стабильность:** Обеспечивает стабильную оценку производительности

**Плюсы правильного разделения:**
- Реалистичная оценка производительности
- Предотвращение утечек данных
- Учет временной структуры
- Стабильные результаты

**Минусы правильного разделения:**
- Сложность реализации
- Необходимость большего объема данных
- Возможное снижение производительности
- Сложность настройки параметров
```python
def create_walk_forward_splits(data, train_size=252, test_size=63, step_size=21):
    """Создание Walk-Forward разделов"""
    
    splits = []
    start_idx = 0
    
    while start_idx + train_size + test_size <= len(data):
        # Обучающий период
        train_start = start_idx
        train_end = start_idx + train_size
        
        # Тестовый период
        test_start = train_end
        test_end = train_end + test_size
        
        splits.append({
            'train_start': train_start,
            'train_end': train_end,
            'test_start': test_start,
            'test_end': test_end,
            'train_data': data.iloc[train_start:train_end],
            'test_data': data.iloc[test_start:test_end]
        })
        
        # Сдвигаемся на step_size
        start_idx += step_size
    
    return splits
```

### 2. Структура анализа
```python
class WalkForwardAnalyzer:
    def __init__(self, train_size=252, test_size=63, step_size=21):
        self.train_size = train_size
        self.test_size = test_size
        self.step_size = step_size
        self.results = []
    
    def run_analysis(self, data, strategy):
        """Запуск Walk-Forward анализа"""
        
        # Создание разделов
        splits = create_walk_forward_splits(
            data, self.train_size, self.test_size, self.step_size
        )
        
        for i, split in enumerate(splits):
            print(f"Обработка периода {i+1}/{len(splits)}")
            
            # Обучение на train данных
            strategy.train(split['train_data'])
            
            # Тестирование на test данных
            backtester = Backtester()
            metrics = backtester.run_backtest(split['test_data'], strategy)
            
            # Сохранение результатов
            self.results.append({
                'period': i + 1,
                'train_start': split['train_start'],
                'train_end': split['train_end'],
                'test_start': split['test_start'],
                'test_end': split['test_end'],
                'metrics': metrics
            })
        
        return self.analyze_results()
    
    def analyze_results(self):
        """Анализ результатов Walk-Forward"""
        
        # Извлечение метрик
        returns = [r['metrics']['total_return'] for r in self.results]
        sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in self.results]
        max_drawdowns = [r['metrics']['max_drawdown'] for r in self.results]
        
        # Статистика
        analysis = {
            'total_periods': len(self.results),
            'mean_return': np.mean(returns),
            'std_return': np.std(returns),
            'mean_sharpe': np.mean(sharpe_ratios),
            'std_sharpe': np.std(sharpe_ratios),
            'mean_drawdown': np.mean(max_drawdowns),
            'worst_drawdown': np.min(max_drawdowns),
            'positive_periods': sum(1 for r in returns if r > 0),
            'negative_periods': sum(1 for r in returns if r < 0),
            'consistency': sum(1 for r in returns if r > 0) / len(returns)
        }
        
        return analysis
```

## Продвинутые техники Walk-Forward

### 1. Адаптивный размер окон
```python
def adaptive_walk_forward(data, strategy, min_train=126, max_train=504, test_size=63):
    """Walk-Forward с адаптивным размером окон"""
    
    results = []
    current_train_size = min_train
    
    start_idx = 0
    while start_idx + current_train_size + test_size <= len(data):
        # Обучающий период
        train_data = data.iloc[start_idx:start_idx + current_train_size]
        
        # Тестовый период
        test_data = data.iloc[start_idx + current_train_size:start_idx + current_train_size + test_size]
        
        # Обучение и тестирование
        strategy.train(train_data)
        backtester = Backtester()
        metrics = backtester.run_backtest(test_data, strategy)
        
        # Адаптация размера окна на основе производительности
        if metrics['total_return'] > 0.05:  # Хорошая производительность
            current_train_size = min(current_train_size + 21, max_train)
        elif metrics['total_return'] < -0.05:  # Плохая производительность
            current_train_size = max(current_train_size - 21, min_train)
        
        results.append({
            'train_size': current_train_size,
            'metrics': metrics
        })
        
        start_idx += test_size
    
    return results
```

### 2. Множественные стратегии
```python
def multi_strategy_walk_forward(data, strategies, train_size=252, test_size=63):
    """Walk-Forward с множественными стратегиями"""
    
    results = {}
    
    for strategy_name, strategy in strategies.items():
        print(f"Анализ стратегии: {strategy_name}")
        
        analyzer = WalkForwardAnalyzer(train_size, test_size)
        analysis = analyzer.run_analysis(data, strategy)
        
        results[strategy_name] = analysis
    
    # Сравнение стратегий
    comparison = compare_strategies(results)
    
    return results, comparison

def compare_strategies(results):
    """Сравнение стратегий"""
    
    comparison = {}
    
    for strategy_name, analysis in results.items():
        comparison[strategy_name] = {
            'mean_return': analysis['mean_return'],
            'consistency': analysis['consistency'],
            'mean_sharpe': analysis['mean_sharpe'],
            'worst_drawdown': analysis['worst_drawdown']
        }
    
    # Сортировка по средней доходности
    sorted_strategies = sorted(
        comparison.items(), 
        key=lambda x: x[1]['mean_return'], 
        reverse=True
    )
    
    return sorted_strategies
```

### 3. Rolling Window vs Expanding Window
```python
def rolling_walk_forward(data, strategy, window_size=252, test_size=63):
    """Rolling Window Walk-Forward"""
    
    results = []
    start_idx = 0
    
    while start_idx + window_size + test_size <= len(data):
        # Обучающий период (фиксированное окно)
        train_data = data.iloc[start_idx:start_idx + window_size]
        
        # Тестовый период
        test_data = data.iloc[start_idx + window_size:start_idx + window_size + test_size]
        
        # Обучение и тестирование
        strategy.train(train_data)
        backtester = Backtester()
        metrics = backtester.run_backtest(test_data, strategy)
        
        results.append(metrics)
        start_idx += test_size
    
    return results

def expanding_walk_forward(data, strategy, min_train=126, test_size=63):
    """Expanding Window Walk-Forward"""
    
    results = []
    start_idx = 0
    train_size = min_train
    
    while start_idx + train_size + test_size <= len(data):
        # Обучающий период (расширяющееся окно)
        train_data = data.iloc[:start_idx + train_size]
        
        # Тестовый период
        test_data = data.iloc[start_idx + train_size:start_idx + train_size + test_size]
        
        # Обучение и тестирование
        strategy.train(train_data)
        backtester = Backtester()
        metrics = backtester.run_backtest(test_data, strategy)
        
        results.append(metrics)
        start_idx += test_size
        train_size += test_size  # Расширяем окно
    
    return results
```

## Анализ стабильности

### 1. Стабильность производительности
```python
def analyze_stability(results):
    """Анализ стабильности результатов"""
    
    returns = [r['metrics']['total_return'] for r in results]
    
    # Коэффициент вариации
    cv = np.std(returns) / np.abs(np.mean(returns))
    
    # Тренд производительности
    x = np.arange(len(returns))
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, returns)
    
    # Стабильность Sharpe Ratio
    sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]
    sharpe_stability = 1 - np.std(sharpe_ratios) / np.abs(np.mean(sharpe_ratios))
    
    return {
        'coefficient_of_variation': cv,
        'performance_trend': slope,
        'trend_significance': p_value,
        'sharpe_stability': sharpe_stability,
        'return_consistency': 1 - cv
    }
```

### 2. Анализ деградации
```python
def analyze_degradation(results):
    """Анализ деградации производительности"""
    
    returns = [r['metrics']['total_return'] for r in results]
    
    # Разделение на периоды
    n_periods = len(returns)
    first_half = returns[:n_periods//2]
    second_half = returns[n_periods//2:]
    
    # Сравнение производительности
    first_half_mean = np.mean(first_half)
    second_half_mean = np.mean(second_half)
    
    degradation = (second_half_mean - first_half_mean) / abs(first_half_mean)
    
    # Статистический тест
    t_stat, p_value = stats.ttest_ind(first_half, second_half)
    
    return {
        'first_half_mean': first_half_mean,
        'second_half_mean': second_half_mean,
        'degradation': degradation,
        't_statistic': t_stat,
        'p_value': p_value,
        'significant_degradation': p_value < 0.05 and degradation < -0.1
    }
```

### 3. Анализ адаптивности
```python
def analyze_adaptability(results, market_conditions):
    """Анализ адаптивности к рыночным условиям"""
    
    adaptability_scores = []
    
    for i, result in enumerate(results):
        # Получаем рыночные условия для периода
        period_conditions = market_conditions[i]
        
        # Анализируем производительность в разных условиях
        if period_conditions['volatility'] > 0.3:  # Высокая волатильность
            volatility_performance = result['metrics']['total_return']
        else:
            volatility_performance = result['metrics']['total_return']
        
        if period_conditions['trend'] == 'bull':  # Бычий рынок
            trend_performance = result['metrics']['total_return']
        else:  # Медвежий рынок
            trend_performance = result['metrics']['total_return']
        
        # Оценка адаптивности
        adaptability = (volatility_performance + trend_performance) / 2
        adaptability_scores.append(adaptability)
    
    return {
        'mean_adaptability': np.mean(adaptability_scores),
        'adaptability_std': np.std(adaptability_scores),
        'adaptability_trend': np.polyfit(range(len(adaptability_scores)), adaptability_scores, 1)[0]
    }
```

## Визуализация результатов

### 1. График производительности по периодам
```python
def plot_performance_by_period(results):
    """График производительности по периодам"""
    
    periods = [r['period'] for r in results]
    returns = [r['metrics']['total_return'] for r in results]
    sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Доходность
    ax1.plot(periods, returns, marker='o', linewidth=2)
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    ax1.set_title('Доходность по периодам')
    ax1.set_ylabel('Доходность')
    ax1.grid(True, alpha=0.3)
    
    # Sharpe Ratio
    ax2.plot(periods, sharpe_ratios, marker='s', color='green', linewidth=2)
    ax2.axhline(y=1, color='r', linestyle='--', alpha=0.5)
    ax2.set_title('Sharpe Ratio по периодам')
    ax2.set_xlabel('Период')
    ax2.set_ylabel('Sharpe Ratio')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
```

### 2. Распределение результатов
```python
def plot_results_distribution(results):
    """Распределение результатов"""
    
    returns = [r['metrics']['total_return'] for r in results]
    sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Распределение доходности
    ax1.hist(returns, bins=20, alpha=0.7, edgecolor='black')
    ax1.axvline(np.mean(returns), color='r', linestyle='--', label=f'Среднее: {np.mean(returns):.3f}')
    ax1.set_title('Распределение доходности')
    ax1.set_xlabel('Доходность')
    ax1.set_ylabel('Частота')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Распределение Sharpe Ratio
    ax2.hist(sharpe_ratios, bins=20, alpha=0.7, edgecolor='black', color='green')
    ax2.axvline(np.mean(sharpe_ratios), color='r', linestyle='--', label=f'Среднее: {np.mean(sharpe_ratios):.3f}')
    ax2.set_title('Распределение Sharpe Ratio')
    ax2.set_xlabel('Sharpe Ratio')
    ax2.set_ylabel('Частота')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
```

## Практический пример

```python
def complete_walk_forward_analysis(data, strategy):
    """Полный Walk-Forward анализ"""
    
    # 1. Создание анализатора
    analyzer = WalkForwardAnalyzer(train_size=252, test_size=63, step_size=21)
    
    # 2. Запуск анализа
    analysis = analyzer.run_analysis(data, strategy)
    
    # 3. Анализ стабильности
    stability = analyze_stability(analyzer.results)
    
    # 4. Анализ деградации
    degradation = analyze_degradation(analyzer.results)
    
    # 5. Визуализация
    plot_performance_by_period(analyzer.results)
    plot_results_distribution(analyzer.results)
    
    # 6. Отчет
    print("=== Walk-Forward анализ ===")
    print(f"Всего периодов: {analysis['total_periods']}")
    print(f"Средняя доходность: {analysis['mean_return']:.2%}")
    print(f"Стандартное отклонение: {analysis['std_return']:.2%}")
    print(f"Консистентность: {analysis['consistency']:.2%}")
    print(f"Средний Sharpe: {analysis['mean_sharpe']:.2f}")
    
    print("\n=== Анализ стабильности ===")
    print(f"Коэффициент вариации: {stability['coefficient_of_variation']:.3f}")
    print(f"Тренд производительности: {stability['performance_trend']:.4f}")
    print(f"Стабильность Sharpe: {stability['sharpe_stability']:.3f}")
    
    print("\n=== Анализ деградации ===")
    print(f"Деградация: {degradation['degradation']:.2%}")
    print(f"Значимая деградация: {degradation['significant_degradation']}")
    
    return {
        'analysis': analysis,
        'stability': stability,
        'degradation': degradation,
        'results': analyzer.results
    }
```

## Следующие шаги

После Walk-Forward анализа переходите к:
- **[08_monte_carlo_simulation.md](08_monte_carlo_simulation.md)** - Монте-Карло симуляция
- **[09_risk_management.md](09_risk_management.md)** - Управление рисками

## Ключевые выводы

1. **Walk-Forward** - самый реалистичный метод тестирования
2. **Стабильность** важнее максимальной доходности
3. **Адаптивность** - ключ к долгосрочному успеху
4. **Деградация** - нормальное явление, нужно учитывать
5. **Визуализация** помогает понять поведение стратегии

---

**Важно:** Хорошая стратегия должна работать стабильно на новых данных, а не только на исторических!
