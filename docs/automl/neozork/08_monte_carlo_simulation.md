# 08. 🎲 Монте-Карло симуляция

**Цель:** Научиться использовать Монте-Карло симуляцию для оценки рисков и неопределенности торговых стратегий.

## Что такое Монте-Карло симуляция?

**Теория:** Монте-Карло симуляция - это мощный статистический метод, который использует случайные выборки для моделирования сложных систем и оценки неопределенности. В финансовой сфере она особенно ценна для оценки рисков и планирования капитала.

**Монте-Карло симуляция** - это метод моделирования, который использует случайные выборки для получения численных результатов и оценки неопределенности.

**Почему Монте-Карло симуляция критична для финансовых систем:**
- **Оценка рисков:** Позволяет количественно оценить различные типы рисков
- **Планирование капитала:** Помогает определить оптимальный размер позиций
- **Стресс-тестирование:** Проверяет устойчивость стратегии в экстремальных условиях
- **Валидация стратегии:** Оценивает робастность торговых стратегий

### Зачем нужна Монте-Карло симуляция?

**Теория:** Монте-Карло симуляция решает фундаментальные проблемы финансового моделирования, связанные с неопределенностью и сложностью рыночных процессов. Она обеспечивает более полное понимание рисков и возможностей.

- **Оценка рисков** - понимание возможных потерь
  - **Почему важно:** Финансовые рынки полны неопределенности, необходимо понимать возможные потери
  - **Плюсы:** Количественная оценка рисков, планирование управления рисками
  - **Минусы:** Требует много вычислительных ресурсов, может быть сложной в интерпретации

- **Планирование капитала** - определение размера позиций
  - **Почему важно:** Правильное управление капиталом критично для выживания на рынке
  - **Плюсы:** Оптимизация размера позиций, снижение рисков
  - **Минусы:** Сложность расчета, необходимость точных данных

- **Стресс-тестирование** - проверка в экстремальных условиях
  - **Почему важно:** Рынки могут испытывать экстремальные события
  - **Плюсы:** Выявление уязвимостей, подготовка к кризисам
  - **Минусы:** Может показать худшие результаты, сложность настройки сценариев

- **Валидация стратегии** - проверка робастности
  - **Почему важно:** Стратегия должна работать в различных условиях
  - **Плюсы:** Оценка стабильности, выявление проблем
  - **Минусы:** Требует много времени, сложность интерпретации результатов

**Дополнительные преимущества Монте-Карло симуляции:**
- **Гибкость:** Можно моделировать различные сценарии
- **Реалистичность:** Учитывает сложность реальных рынков
- **Количественность:** Дает точные численные оценки
- **Визуализация:** Позволяет наглядно представить риски

## Основы Монте-Карло симуляции

**Теория:** Монте-Карло симуляция основана на принципе генерации множества случайных сценариев для оценки неопределенности. В финансовой сфере это особенно важно для понимания рисков и возможностей.

### 1. Простая симуляция

**Теория:** Простая Монте-Карло симуляция использует нормальное распределение для моделирования доходностей. Это базовый подход, который может быть расширен для учета более сложных зависимостей.

**Почему простая симуляция важна:**
- **Базовый подход:** Служит основой для более сложных методов
- **Понятность:** Легко понять и интерпретировать результаты
- **Быстрота:** Быстро выполняется даже на больших данных
- **Валидация:** Позволяет проверить правильность реализации

**Плюсы простой симуляции:**
- Простота реализации
- Быстрота выполнения
- Легкая интерпретация
- Хорошая база для расширения

**Минусы простой симуляции:**
- Может не учитывать сложные зависимости
- Предполагает нормальное распределение
- Может быть менее реалистичной
- Ограниченная гибкость
```python
import numpy as np
import pandas as pd
from scipy import stats

def monte_carlo_simulation(returns, n_simulations=10000, time_horizon=252):
    """Простая Монте-Карло симуляция"""
    
    # Параметры распределения доходности
    mean_return = returns.mean()
    std_return = returns.std()
    
    # Массив для хранения результатов
    simulation_results = []
    
    for _ in range(n_simulations):
        # Генерация случайных доходностей
        random_returns = np.random.normal(mean_return, std_return, time_horizon)
        
        # Расчет кумулятивной доходности
        cumulative_return = np.prod(1 + random_returns) - 1
        
        simulation_results.append(cumulative_return)
    
    return np.array(simulation_results)

def analyze_simulation_results(results):
    """Анализ результатов симуляции"""
    
    return {
        'mean_return': np.mean(results),
        'std_return': np.std(results),
        'percentile_5': np.percentile(results, 5),
        'percentile_25': np.percentile(results, 25),
        'percentile_50': np.percentile(results, 50),
        'percentile_75': np.percentile(results, 75),
        'percentile_95': np.percentile(results, 95),
        'probability_positive': np.mean(results > 0),
        'probability_loss': np.mean(results < 0),
        'max_loss': np.min(results),
        'max_gain': np.max(results)
    }
```

### 2. Bootstrap симуляция

**Теория:** Bootstrap симуляция использует исторические данные для создания новых сценариев путем случайной выборки с возвращением. Это более реалистичный подход, который сохраняет структуру исторических данных.

**Почему Bootstrap симуляция важна:**
- **Реалистичность:** Использует реальные исторические данные
- **Сохранение структуры:** Сохраняет зависимости в данных
- **Непараметричность:** Не требует предположений о распределении
- **Гибкость:** Может работать с любыми типами данных

**Плюсы Bootstrap симуляции:**
- Более реалистичные результаты
- Сохранение структуры данных
- Непараметрический подход
- Гибкость применения

**Минусы Bootstrap симуляции:**
- Может быть менее стабильной
- Требует больше вычислительных ресурсов
- Сложность интерпретации
- Возможные проблемы с зависимостями
```python
def bootstrap_monte_carlo(returns, n_simulations=10000, time_horizon=252):
    """Bootstrap Монте-Карло симуляция"""
    
    simulation_results = []
    
    for _ in range(n_simulations):
        # Случайная выборка с возвращением
        bootstrap_returns = np.random.choice(returns, size=time_horizon, replace=True)
        
        # Расчет кумулятивной доходности
        cumulative_return = np.prod(1 + bootstrap_returns) - 1
        
        simulation_results.append(cumulative_return)
    
    return np.array(simulation_results)
```

### 3. Block Bootstrap симуляция

**Теория:** Block Bootstrap симуляция расширяет обычный Bootstrap, учитывая временные зависимости в данных. Она использует блоки данных вместо отдельных наблюдений, что более реалистично для финансовых временных рядов.

**Почему Block Bootstrap симуляция важна:**
- **Временные зависимости:** Учитывает автокорреляцию в данных
- **Реалистичность:** Более точно моделирует финансовые данные
- **Сохранение структуры:** Сохраняет временную структуру данных
- **Гибкость:** Может настраиваться под различные типы данных

**Плюсы Block Bootstrap симуляции:**
- Учет временных зависимостей
- Более реалистичные результаты
- Сохранение структуры данных
- Гибкость настройки

**Минусы Block Bootstrap симуляции:**
- Сложность реализации
- Требует настройки размера блоков
- Может быть менее стабильной
- Высокие вычислительные затраты
```python
def block_bootstrap_monte_carlo(returns, n_simulations=10000, time_horizon=252, block_size=5):
    """Block Bootstrap Монте-Карло симуляция"""
    
    simulation_results = []
    
    for _ in range(n_simulations):
        # Создание блоков
        n_blocks = time_horizon // block_size
        bootstrap_returns = []
        
        for _ in range(n_blocks):
            # Случайный выбор блока
            start_idx = np.random.randint(0, len(returns) - block_size)
            block = returns[start_idx:start_idx + block_size]
            bootstrap_returns.extend(block)
        
        # Дополнение до нужной длины
        while len(bootstrap_returns) < time_horizon:
            start_idx = np.random.randint(0, len(returns) - block_size)
            block = returns[start_idx:start_idx + block_size]
            bootstrap_returns.extend(block)
        
        bootstrap_returns = np.array(bootstrap_returns[:time_horizon])
        
        # Расчет кумулятивной доходности
        cumulative_return = np.prod(1 + bootstrap_returns) - 1
        
        simulation_results.append(cumulative_return)
    
    return np.array(simulation_results)
```

## Продвинутые техники

### 1. Учет автокорреляции
```python
def autocorrelated_monte_carlo(returns, n_simulations=10000, time_horizon=252):
    """Монте-Карло с учетом автокорреляции"""
    
    # Расчет автокорреляции
    autocorr = pd.Series(returns).autocorr(lag=1)
    
    simulation_results = []
    
    for _ in range(n_simulations):
        # Генерация с учетом автокорреляции
        simulated_returns = []
        
        # Первое значение
        first_return = np.random.normal(returns.mean(), returns.std())
        simulated_returns.append(first_return)
        
        # Последующие значения с автокорреляцией
        for i in range(1, time_horizon):
            # AR(1) процесс
            next_return = (autocorr * simulated_returns[-1] + 
                          np.random.normal(0, returns.std() * np.sqrt(1 - autocorr**2)))
            simulated_returns.append(next_return)
        
        # Расчет кумулятивной доходности
        cumulative_return = np.prod(1 + simulated_returns) - 1
        simulation_results.append(cumulative_return)
    
    return np.array(simulation_results)
```

### 2. Учет волатильности
```python
def garch_monte_carlo(returns, n_simulations=10000, time_horizon=252):
    """Монте-Карло с GARCH моделью волатильности"""
    
    from arch import arch_model
    
    # Обучение GARCH модели
    model = arch_model(returns, vol='Garch', p=1, q=1)
    fitted_model = model.fit()
    
    simulation_results = []
    
    for _ in range(n_simulations):
        # Генерация с GARCH волатильностью
        simulated_returns = fitted_model.forecast(horizon=time_horizon, method='simulation')
        
        # Расчет кумулятивной доходности
        cumulative_return = np.prod(1 + simulated_returns.values.flatten()) - 1
        simulation_results.append(cumulative_return)
    
    return np.array(simulation_results)
```

### 3. Многомерная симуляция
```python
def multivariate_monte_carlo(returns_dict, n_simulations=10000, time_horizon=252):
    """Многомерная Монте-Карло симуляция"""
    
    # Объединение данных
    returns_df = pd.DataFrame(returns_dict)
    
    # Расчет корреляционной матрицы
    correlation_matrix = returns_df.corr()
    
    # Cholesky разложение
    chol_matrix = np.linalg.cholesky(correlation_matrix)
    
    simulation_results = {}
    
    for asset in returns_dict.keys():
        asset_returns = returns_dict[asset]
        mean_return = asset_returns.mean()
        std_return = asset_returns.std()
        
        asset_simulations = []
        
        for _ in range(n_simulations):
            # Генерация независимых случайных чисел
            independent_random = np.random.normal(0, 1, time_horizon)
            
            # Преобразование с учетом корреляций
            correlated_random = chol_matrix @ independent_random
            
            # Генерация доходностей
            simulated_returns = mean_return + std_return * correlated_random
            
            # Расчет кумулятивной доходности
            cumulative_return = np.prod(1 + simulated_returns) - 1
            asset_simulations.append(cumulative_return)
        
        simulation_results[asset] = np.array(asset_simulations)
    
    return simulation_results
```

## Анализ рисков

### 1. Value at Risk (VaR)
```python
def calculate_var(simulation_results, confidence_level=0.05):
    """Расчет Value at Risk"""
    
    var = np.percentile(simulation_results, confidence_level * 100)
    return var

def calculate_expected_shortfall(simulation_results, confidence_level=0.05):
    """Расчет Expected Shortfall (Conditional VaR)"""
    
    var = calculate_var(simulation_results, confidence_level)
    tail_losses = simulation_results[simulation_results <= var]
    expected_shortfall = np.mean(tail_losses)
    
    return expected_shortfall
```

### 2. Maximum Drawdown
```python
def calculate_max_drawdown_distribution(simulation_results, time_horizon=252):
    """Распределение максимальной просадки"""
    
    max_drawdowns = []
    
    for result in simulation_results:
        # Симуляция пути капитала
        cumulative_returns = np.cumprod(1 + np.random.normal(0, 0.02, time_horizon))
        
        # Расчет максимальной просадки
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = np.min(drawdown)
        
        max_drawdowns.append(max_drawdown)
    
    return np.array(max_drawdowns)
```

### 3. Stress Testing
```python
def stress_testing_monte_carlo(returns, stress_scenarios, n_simulations=10000):
    """Стресс-тестирование с Монте-Карло"""
    
    stress_results = {}
    
    for scenario_name, stress_params in stress_scenarios.items():
        # Параметры стресса
        stress_mean = stress_params.get('mean', returns.mean())
        stress_std = stress_params.get('std', returns.std() * stress_params.get('volatility_multiplier', 1))
        stress_correlation = stress_params.get('correlation', 1)
        
        scenario_results = []
        
        for _ in range(n_simulations):
            # Генерация с стрессовыми параметрами
            stress_returns = np.random.normal(stress_mean, stress_std, len(returns))
            
            # Применение корреляции
            if stress_correlation != 1:
                stress_returns = stress_correlation * returns + np.sqrt(1 - stress_correlation**2) * stress_returns
            
            # Расчет результата
            cumulative_return = np.prod(1 + stress_returns) - 1
            scenario_results.append(cumulative_return)
        
        stress_results[scenario_name] = np.array(scenario_results)
    
    return stress_results
```

## Визуализация результатов

### 1. Распределение результатов
```python
import matplotlib.pyplot as plt

def plot_simulation_distribution(simulation_results, title="Монте-Карло симуляция"):
    """График распределения результатов симуляции"""
    
    plt.figure(figsize=(12, 8))
    
    # Гистограмма
    plt.hist(simulation_results, bins=50, alpha=0.7, density=True, edgecolor='black')
    
    # Нормальное распределение для сравнения
    mu, sigma = np.mean(simulation_results), np.std(simulation_results)
    x = np.linspace(simulation_results.min(), simulation_results.max(), 100)
    plt.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', linewidth=2, label='Нормальное распределение')
    
    # Квантили
    percentiles = [5, 25, 50, 75, 95]
    for p in percentiles:
        value = np.percentile(simulation_results, p)
        plt.axvline(value, color='red', linestyle='--', alpha=0.7, label=f'{p}%: {value:.3f}')
    
    plt.title(title)
    plt.xlabel('Доходность')
    plt.ylabel('Плотность')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
```

### 2. Кривая риска
```python
def plot_risk_curve(simulation_results, confidence_levels):
    """Кривая риска (VaR)"""
    
    var_values = []
    
    for cl in confidence_levels:
        var = np.percentile(simulation_results, cl * 100)
        var_values.append(var)
    
    plt.figure(figsize=(10, 6))
    plt.plot(confidence_levels, var_values, marker='o', linewidth=2)
    plt.title('Кривая риска (VaR)')
    plt.xlabel('Уровень доверия')
    plt.ylabel('VaR')
    plt.grid(True, alpha=0.3)
    plt.show()
```

### 3. Сравнение сценариев
```python
def plot_scenario_comparison(stress_results):
    """Сравнение стрессовых сценариев"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, (scenario_name, results) in enumerate(stress_results.items()):
        if i < len(axes):
            axes[i].hist(results, bins=30, alpha=0.7, edgecolor='black')
            axes[i].set_title(f'Сценарий: {scenario_name}')
            axes[i].set_xlabel('Доходность')
            axes[i].set_ylabel('Частота')
            axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
```

## Практический пример

```python
def complete_monte_carlo_analysis(returns, n_simulations=10000):
    """Полный Монте-Карло анализ"""
    
    # 1. Простая симуляция
    simple_results = monte_carlo_simulation(returns, n_simulations)
    
    # 2. Bootstrap симуляция
    bootstrap_results = bootstrap_monte_carlo(returns, n_simulations)
    
    # 3. Block Bootstrap симуляция
    block_bootstrap_results = block_bootstrap_monte_carlo(returns, n_simulations)
    
    # 4. Анализ рисков
    var_95 = calculate_var(simple_results, 0.05)
    var_99 = calculate_var(simple_results, 0.01)
    es_95 = calculate_expected_shortfall(simple_results, 0.05)
    
    # 5. Стресс-тестирование
    stress_scenarios = {
        'Кризис': {'volatility_multiplier': 2.0, 'mean': -0.01},
        'Высокая волатильность': {'volatility_multiplier': 1.5},
        'Низкая доходность': {'mean': 0.001}
    }
    
    stress_results = stress_testing_monte_carlo(returns, stress_scenarios)
    
    # 6. Визуализация
    plot_simulation_distribution(simple_results, "Простая симуляция")
    plot_simulation_distribution(bootstrap_results, "Bootstrap симуляция")
    plot_scenario_comparison(stress_results)
    
    # 7. Отчет
    analysis = analyze_simulation_results(simple_results)
    
    print("=== Монте-Карло анализ ===")
    print(f"Средняя доходность: {analysis['mean_return']:.2%}")
    print(f"Стандартное отклонение: {analysis['std_return']:.2%}")
    print(f"5% VaR: {var_95:.2%}")
    print(f"1% VaR: {var_99:.2%}")
    print(f"Expected Shortfall (95%): {es_95:.2%}")
    print(f"Вероятность прибыли: {analysis['probability_positive']:.2%}")
    print(f"Вероятность убытка: {analysis['probability_loss']:.2%}")
    
    return {
        'simple_results': simple_results,
        'bootstrap_results': bootstrap_results,
        'block_bootstrap_results': block_bootstrap_results,
        'stress_results': stress_results,
        'risk_metrics': {
            'var_95': var_95,
            'var_99': var_99,
            'es_95': es_95
        },
        'analysis': analysis
    }
```

## Следующие шаги

После Монте-Карло симуляции переходите к:
- **[09_risk_management.md](09_risk_management.md)** - Управление рисками
- **[10_blockchain_deployment.md](10_blockchain_deployment.md)** - Блокчейн деплой

## Ключевые выводы

1. **Монте-Карло** - мощный инструмент оценки рисков
2. **Bootstrap** сохраняет структуру данных
3. **Стресс-тестирование** проверяет устойчивость
4. **VaR и ES** - ключевые метрики риска
5. **Визуализация** помогает понять распределение рисков

---

**Важно:** Монте-Карло симуляция показывает не только возможную прибыль, но и риски потерь!
