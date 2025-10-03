# 06. 📈 Бэктестинг

**Цель:** Научиться правильно проводить бэктестинг торговых стратегий и избегать типичных ошибок.

## Что такое бэктестинг?

**Бэктестинг** - это тестирование торговой стратегии на исторических данных для оценки её потенциальной прибыльности.

### Зачем нужен бэктестинг?
- **Проверка стратегии** на исторических данных
- **Оценка рисков** и потенциальных потерь
- **Оптимизация параметров** стратегии
- **Сравнение** разных подходов

## Типичные ошибки бэктестинга

### 1. Look-ahead bias (Предвзятость будущего)
```python
# ❌ НЕПРАВИЛЬНО - используем будущие данные
def bad_backtest(df):
    for i in range(len(df)):
        # Используем данные из будущего!
        if df.iloc[i]['Close'] > df.iloc[i+1]['Close']:  # ОШИБКА!
            signal = 'BUY'
        else:
            signal = 'SELL'
    return signals

# ✅ ПРАВИЛЬНО - используем только прошлые данные
def good_backtest(df):
    signals = []
    for i in range(len(df)):
        # Используем только данные до текущего момента
        if i > 0 and df.iloc[i]['Close'] > df.iloc[i-1]['Close']:
            signal = 'BUY'
        else:
            signal = 'SELL'
        signals.append(signal)
    return signals
```

### 2. Survivorship bias (Выживания)
```python
# ❌ НЕПРАВИЛЬНО - тестируем только на "выживших" активах
def bad_survivorship_test():
    # Тестируем только на активах, которые существуют сейчас
    symbols = ['AAPL', 'GOOGL', 'MSFT']  # Все успешные компании
    return backtest_symbols(symbols)

# ✅ ПРАВИЛЬНО - включаем все активы, включая "мертвые"
def good_survivorship_test():
    # Включаем все активы, которые торговались в период
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'ENRON', 'LEHMAN']  # Включая банкротов
    return backtest_symbols(symbols)
```

### 3. Overfitting (Переобучение)
```python
# ❌ НЕПРАВИЛЬНО - оптимизируем на всех данных
def bad_optimization(df):
    # Оптимизируем параметры на всех данных
    best_params = optimize_parameters(df)  # Переобучение!
    return backtest_with_params(df, best_params)

# ✅ ПРАВИЛЬНО - разделяем на train/test
def good_optimization(df):
    # Разделяем данные
    train_data = df[:int(len(df)*0.7)]
    test_data = df[int(len(df)*0.7):]
    
    # Оптимизируем на train
    best_params = optimize_parameters(train_data)
    
    # Тестируем на test
    return backtest_with_params(test_data, best_params)
```

## Правильный бэктестинг

### 1. Структура бэктестинга
```python
class Backtester:
    def __init__(self, initial_capital=10000, commission=0.001):
        self.initial_capital = initial_capital
        self.commission = commission
        self.capital = initial_capital
        self.position = 0
        self.trades = []
        self.equity_curve = []
    
    def run_backtest(self, data, strategy):
        """Запуск бэктестинга"""
        
        for i, row in data.iterrows():
            # Получаем сигнал от стратегии
            signal = strategy.get_signal(data.iloc[:i+1])
            
            # Выполняем торговую операцию
            self.execute_trade(row, signal)
            
            # Записываем состояние
            self.equity_curve.append(self.capital)
        
        return self.calculate_metrics()
    
    def execute_trade(self, row, signal):
        """Выполнение торговой операции"""
        
        if signal == 'BUY' and self.position <= 0:
            # Покупка
            if self.position < 0:
                # Закрываем короткую позицию
                self.close_position(row['Close'])
            
            # Открываем длинную позицию
            self.open_position(row['Close'], 'LONG')
            
        elif signal == 'SELL' and self.position >= 0:
            # Продажа
            if self.position > 0:
                # Закрываем длинную позицию
                self.close_position(row['Close'])
            
            # Открываем короткую позицию
            self.open_position(row['Close'], 'SHORT')
    
    def open_position(self, price, direction):
        """Открытие позиции"""
        if direction == 'LONG':
            self.position = self.capital / price
            self.capital = 0
        else:  # SHORT
            self.position = -self.capital / price
            self.capital = 0
    
    def close_position(self, price):
        """Закрытие позиции"""
        if self.position > 0:  # Закрываем длинную позицию
            self.capital = self.position * price * (1 - self.commission)
        else:  # Закрываем короткую позицию
            self.capital = -self.position * price * (1 - self.commission)
        
        self.position = 0
```

### 2. Расчет метрик
```python
def calculate_metrics(self):
    """Расчет метрик бэктестинга"""
    
    # Общая доходность
    total_return = (self.capital - self.initial_capital) / self.initial_capital
    
    # Годовая доходность
    years = len(self.equity_curve) / 252  # 252 торговых дня в году
    annual_return = (1 + total_return) ** (1/years) - 1
    
    # Волатильность
    returns = pd.Series(self.equity_curve).pct_change().dropna()
    volatility = returns.std() * np.sqrt(252)
    
    # Sharpe Ratio
    risk_free_rate = 0.02  # 2% безрисковая ставка
    sharpe_ratio = (annual_return - risk_free_rate) / volatility
    
    # Максимальная просадка
    equity_series = pd.Series(self.equity_curve)
    running_max = equity_series.expanding().max()
    drawdown = (equity_series - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # Win Rate
    if self.trades:
        winning_trades = [t for t in self.trades if t['profit'] > 0]
        win_rate = len(winning_trades) / len(self.trades)
    else:
        win_rate = 0
    
    return {
        'total_return': total_return,
        'annual_return': annual_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'win_rate': win_rate,
        'total_trades': len(self.trades)
    }
```

## Продвинутые техники бэктестинга

### 1. Walk-Forward Analysis
```python
def walk_forward_analysis(data, strategy, train_period=252, test_period=63):
    """Walk-Forward анализ"""
    
    results = []
    
    for start_date in range(0, len(data) - train_period - test_period, test_period):
        # Обучающий период
        train_data = data.iloc[start_date:start_date + train_period]
        
        # Тестовый период
        test_data = data.iloc[start_date + train_period:start_date + train_period + test_period]
        
        # Обучение стратегии
        strategy.train(train_data)
        
        # Тестирование
        backtester = Backtester()
        metrics = backtester.run_backtest(test_data, strategy)
        
        results.append({
            'start_date': data.index[start_date],
            'end_date': data.index[start_date + train_period + test_period],
            'metrics': metrics
        })
    
    return results
```

### 2. Monte Carlo Simulation
```python
def monte_carlo_simulation(data, strategy, n_simulations=1000):
    """Монте-Карло симуляция"""
    
    results = []
    
    for _ in range(n_simulations):
        # Случайная перестановка данных
        shuffled_data = data.sample(frac=1).reset_index(drop=True)
        
        # Бэктестинг на переставленных данных
        backtester = Backtester()
        metrics = backtester.run_backtest(shuffled_data, strategy)
        
        results.append(metrics)
    
    return results

def analyze_monte_carlo_results(results):
    """Анализ результатов Монте-Карло"""
    
    returns = [r['total_return'] for r in results]
    
    return {
        'mean_return': np.mean(returns),
        'std_return': np.std(returns),
        'percentile_5': np.percentile(returns, 5),
        'percentile_95': np.percentile(returns, 95),
        'probability_positive': np.mean([r > 0 for r in returns])
    }
```

### 3. Bootstrap Analysis
```python
def bootstrap_analysis(data, strategy, n_bootstrap=1000, block_size=20):
    """Bootstrap анализ с блоками"""
    
    results = []
    
    for _ in range(n_bootstrap):
        # Создание бутстрап выборки с блоками
        bootstrap_data = []
        
        for _ in range(len(data) // block_size):
            # Случайный блок
            start_idx = np.random.randint(0, len(data) - block_size)
            block = data.iloc[start_idx:start_idx + block_size]
            bootstrap_data.append(block)
        
        bootstrap_data = pd.concat(bootstrap_data, ignore_index=True)
        
        # Бэктестинг
        backtester = Backtester()
        metrics = backtester.run_backtest(bootstrap_data, strategy)
        
        results.append(metrics)
    
    return results
```

## Учет реалистичности

### 1. Комиссии и спреды
```python
class RealisticBacktester(Backtester):
    def __init__(self, initial_capital=10000, commission=0.001, spread=0.0005):
        super().__init__(initial_capital, commission)
        self.spread = spread
    
    def execute_trade(self, row, signal):
        """Реалистичное выполнение торгов"""
        
        # Учитываем спред
        if signal == 'BUY':
            price = row['Close'] * (1 + self.spread)  # Покупаем дороже
        elif signal == 'SELL':
            price = row['Close'] * (1 - self.spread)  # Продаем дешевле
        else:
            return
        
        # Учитываем комиссию
        commission_cost = self.capital * self.commission
        
        # Выполняем сделку
        if signal == 'BUY' and self.position <= 0:
            if self.position < 0:
                self.close_position(price)
            self.open_position(price, 'LONG')
            self.capital -= commission_cost
            
        elif signal == 'SELL' and self.position >= 0:
            if self.position > 0:
                self.close_position(price)
            self.open_position(price, 'SHORT')
            self.capital -= commission_cost
```

### 2. Ликвидность и проскальзывание
```python
def calculate_slippage(volume, market_volume, price):
    """Расчет проскальзывания"""
    
    # Проскальзывание зависит от объема относительно рыночного
    volume_ratio = volume / market_volume
    
    if volume_ratio < 0.01:  # Малый объем
        slippage = 0.0001
    elif volume_ratio < 0.1:  # Средний объем
        slippage = 0.0005
    else:  # Большой объем
        slippage = 0.002
    
    return price * slippage

class LiquidityAwareBacktester(RealisticBacktester):
    def execute_trade(self, row, signal, volume=1000):
        """Учет ликвидности"""
        
        # Расчет проскальзывания
        slippage = calculate_slippage(volume, row['Volume'], row['Close'])
        
        # Корректировка цены
        if signal == 'BUY':
            price = row['Close'] + slippage
        elif signal == 'SELL':
            price = row['Close'] - slippage
        else:
            return
        
        # Выполнение с учетом проскальзывания
        super().execute_trade(pd.Series({'Close': price}), signal)
```

## Визуализация результатов

### 1. Equity Curve
```python
import matplotlib.pyplot as plt

def plot_equity_curve(equity_curve, benchmark=None):
    """Построение кривой капитала"""
    
    plt.figure(figsize=(12, 6))
    
    # Кривая капитала
    plt.plot(equity_curve, label='Strategy', linewidth=2)
    
    # Бенчмарк
    if benchmark is not None:
        plt.plot(benchmark, label='Benchmark', linewidth=2, alpha=0.7)
    
    plt.title('Equity Curve')
    plt.xlabel('Time')
    plt.ylabel('Capital')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
```

### 2. Drawdown Chart
```python
def plot_drawdown(equity_curve):
    """Построение графика просадок"""
    
    equity_series = pd.Series(equity_curve)
    running_max = equity_series.expanding().max()
    drawdown = (equity_series - running_max) / running_max
    
    plt.figure(figsize=(12, 4))
    plt.fill_between(range(len(drawdown)), drawdown, 0, alpha=0.3, color='red')
    plt.plot(drawdown, color='red', linewidth=1)
    plt.title('Drawdown')
    plt.xlabel('Time')
    plt.ylabel('Drawdown %')
    plt.grid(True, alpha=0.3)
    plt.show()
```

### 3. Returns Distribution
```python
def plot_returns_distribution(returns):
    """Построение распределения доходностей"""
    
    plt.figure(figsize=(10, 6))
    
    plt.hist(returns, bins=50, alpha=0.7, density=True, label='Returns')
    
    # Нормальное распределение для сравнения
    mu, sigma = returns.mean(), returns.std()
    x = np.linspace(returns.min(), returns.max(), 100)
    plt.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', label='Normal')
    
    plt.title('Returns Distribution')
    plt.xlabel('Returns')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
```

## Практический пример

```python
def complete_backtest(data, strategy):
    """Полный бэктестинг с анализом"""
    
    # 1. Основной бэктестинг
    backtester = RealisticBacktester()
    metrics = backtester.run_backtest(data, strategy)
    
    # 2. Walk-Forward анализ
    wf_results = walk_forward_analysis(data, strategy)
    
    # 3. Монте-Карло симуляция
    mc_results = monte_carlo_simulation(data, strategy)
    mc_analysis = analyze_monte_carlo_results(mc_results)
    
    # 4. Визуализация
    plot_equity_curve(backtester.equity_curve)
    plot_drawdown(backtester.equity_curve)
    
    # 5. Отчет
    print("=== Результаты бэктестинга ===")
    print(f"Общая доходность: {metrics['total_return']:.2%}")
    print(f"Годовая доходность: {metrics['annual_return']:.2%}")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Максимальная просадка: {metrics['max_drawdown']:.2%}")
    print(f"Win Rate: {metrics['win_rate']:.2%}")
    
    print("\n=== Монте-Карло анализ ===")
    print(f"Средняя доходность: {mc_analysis['mean_return']:.2%}")
    print(f"Вероятность прибыли: {mc_analysis['probability_positive']:.2%}")
    print(f"5-й перцентиль: {mc_analysis['percentile_5']:.2%}")
    print(f"95-й перцентиль: {mc_analysis['percentile_95']:.2%}")
    
    return {
        'metrics': metrics,
        'walk_forward': wf_results,
        'monte_carlo': mc_analysis
    }
```

## Следующие шаги

После бэктестинга переходите к:
- **[07_walk_forward_analysis.md](07_walk_forward_analysis.md)** - Walk-forward анализ
- **[08_monte_carlo_simulation.md](08_monte_carlo_simulation.md)** - Монте-Карло симуляция

## Ключевые выводы

1. **Избегайте look-ahead bias** - используйте только прошлые данные
2. **Учитывайте реалистичность** - комиссии, спреды, ликвидность
3. **Используйте Walk-Forward** - для проверки стабильности
4. **Монте-Карло** - для оценки рисков
5. **Визуализация** - для понимания поведения стратегии

---

**Важно:** Хороший бэктестинг - это не просто высокая доходность, а стабильная и реалистичная прибыльность!
